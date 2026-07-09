import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from src.models import SignalType, SourceType
from src.services.channel_push import (
    ChannelPushError,
    parse_draft_cards,
    push_draft_channels,
)
from src.services.webhook import WebhookDeliveryError, WebhookNotifier


SAMPLE_DRAFT = """# 信先行实用卡片 - 2026-07-09

> 从 12 条内容中筛选出 1 条教程/案例/技巧。

<section class="action-card" data-card-id="reddit:subreddit-rss:t3_test" markdown="1">
<a id="item-1"></a>
## [提示词测试集教程](https://www.reddit.com/r/PromptEngineering/comments/test/post/)

**栏目分类**: `TUTORIAL`

**一句话简介**: 用冻结测试集判断提示词是否真的变好。

**具体怎么做**:
- 准备一批固定样本
- 优化提示词时不要把样本泄漏给模型

**适合谁/适用场景**: `提示词工程师`, `AI应用开发者`

**效果或数据**: 未提供具体数据

**可信度/风险提示**: 方法有效性取决于测试集代表性。

**实用度评分**: Score: 8.0 / 10

**来源链接**: [原文](https://www.reddit.com/r/PromptEngineering/comments/test/post/)

reddit · r/PromptEngineering · /u/tester · 7月9日 06:00

</section>
"""


def test_parse_draft_cards_restores_routing_fields() -> None:
    items, total = parse_draft_cards(SAMPLE_DRAFT)

    assert total == 12
    assert len(items) == 1
    item = items[0]
    assert item.id == "reddit:subreddit-rss:t3_test"
    assert item.source_type is SourceType.REDDIT
    assert item.signal_type is SignalType.TUTORIAL
    assert item.ai_score == 8.0
    assert item.intro == "用冻结测试集判断提示词是否真的变好。"
    assert item.how_to == [
        "准备一批固定样本",
        "优化提示词时不要把样本泄漏给模型",
    ]
    assert item.metadata["subreddit"] == "PromptEngineering"
    assert item.metadata["source_id"] == "reddit_promptengineering"
    assert "tutorial" in item.metadata["content_tags"]


def test_push_draft_channels_alerts_admin_when_channel_fails(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    drafts_dir = data_dir / "drafts"
    drafts_dir.mkdir(parents=True)
    (drafts_dir / "xinxianxing-2026-07-09-zh.md").write_text(
        SAMPLE_DRAFT,
        encoding="utf-8",
    )
    config = {
        "version": "1.0",
        "site": {"base_url": "https://xinxianxing.com"},
        "ai": {
            "provider": "deepseek",
            "model": "deepseek-chat",
            "api_key_env": "DEEPSEEK_API_KEY",
        },
        "sources": {},
        "filtering": {
            "ai_score_threshold": 6.0,
            "time_window_hours": 24,
            "category_groups": {},
            "default_group": "other",
        },
        "publishing": {"auto_publish": False},
        "webhook": {
            "enabled": True,
            "url_env": None,
            "platform": "generic",
            "layout": "markdown",
        },
        "channels": [
            {
                "id": "ai-tools-partner-a",
                "name": "信先行·AI工具(合作方A)",
                "webhook_url": "https://example.com/channel",
                "content_tags": ["ai", "tutorial"],
                "sources": ["reddit_promptengineering"],
                "signal_types": ["TUTORIAL"],
                "min_score": 6.0,
                "active": True,
            }
        ],
    }
    (data_dir / "config.json").write_text(
        json.dumps(config, ensure_ascii=False),
        encoding="utf-8",
    )

    with (
        patch.object(
            WebhookNotifier,
            "notify_channel_feishu",
            new_callable=AsyncMock,
            side_effect=WebhookDeliveryError("invalid token"),
        ) as mock_push,
        patch("src.services.channel_push.send_admin_alert", new_callable=AsyncMock) as mock_alert,
    ):
        with pytest.raises(ChannelPushError):
            import asyncio

            asyncio.run(
                push_draft_channels(
                    date="2026-07-09",
                    language="zh",
                    data_dir=data_dir,
                    admin_webhook_url="https://example.com/admin",
                )
            )

    mock_push.assert_awaited_once()
    mock_alert.assert_awaited_once()
    assert mock_alert.call_args.kwargs["channel_id"] == "ai-tools-partner-a"
    assert "invalid token" in mock_alert.call_args.kwargs["reason"]
