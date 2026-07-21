import json
from pathlib import Path

from src.services.channel_registry import (
    check_channel,
    default_free_secret_name,
    default_paid_secret_name,
    load_runtime_channels,
    write_channel_file,
)
from src.models import ChannelConfig, ChannelFileConfig


def test_default_secret_names_follow_channel_id_convention() -> None:
    assert (
        default_free_secret_name("ai_tools_partner_001")
        == "CHANNEL_AI_TOOLS_PARTNER_001_FREE_WEBHOOK"
    )
    assert (
        default_paid_secret_name("ai-tools-partner-001")
        == "CHANNEL_AI_TOOLS_PARTNER_001_PAID_WEBHOOK"
    )


def test_file_backed_channel_expands_to_free_and_paid_runtime_channels(tmp_path: Path) -> None:
    channels_dir = tmp_path / "config" / "channels"
    channel = ChannelFileConfig(
        channel_id="ai_tools_partner_001",
        channel_name="信先行·AI工具日报",
        description="频道说明",
        partner_name="合作方名称",
        active=True,
        category="ai_tools",
        template_type="action_card",
        free_webhook_secret_name="CHANNEL_AI_TOOLS_PARTNER_001_FREE_WEBHOOK",
        paid_webhook_secret_name="CHANNEL_AI_TOOLS_PARTNER_001_PAID_WEBHOOK",
        sources=["hackernews"],
        signal_types=["TUTORIAL"],
        max_items_per_push=10,
        min_score=7.0,
        content_tags=["ai", "tutorial"],
    )
    write_channel_file(channel, channels_dir=channels_dir)

    runtime = load_runtime_channels(
        channels_dir=channels_dir,
        env={
            "CHANNEL_AI_TOOLS_PARTNER_001_FREE_WEBHOOK": "https://example.com/free",
            "CHANNEL_AI_TOOLS_PARTNER_001_PAID_WEBHOOK": "https://example.com/paid",
        },
    )

    assert [item.id for item in runtime] == [
        "ai_tools_partner_001",
        "ai_tools_partner_001_paid",
    ]
    assert runtime[0].webhook_url == "https://example.com/free"
    assert runtime[1].webhook_url == "https://example.com/paid"
    assert runtime[1].destination_type == "paid"
    assert runtime[0].logical_channel_id == "ai_tools_partner_001"


def test_load_runtime_channels_falls_back_to_legacy_channels(tmp_path: Path) -> None:
    fallback = [ChannelConfig(id="legacy", name="Legacy", webhook_url="https://example.com")]

    runtime = load_runtime_channels(
        channels_dir=tmp_path / "missing" / "channels",
        fallback_channels=fallback,
    )

    assert runtime == fallback


def test_check_channel_lists_missing_secrets(tmp_path: Path) -> None:
    channels_dir = tmp_path / "config" / "channels"
    write_channel_file(
        ChannelFileConfig(
            channel_id="ai_tools_partner_001",
            channel_name="信先行·AI工具日报",
            active=False,
            category="ai_tools",
            template_type="action_card",
            free_webhook_secret_name="CHANNEL_AI_TOOLS_PARTNER_001_FREE_WEBHOOK",
            paid_webhook_secret_name="CHANNEL_AI_TOOLS_PARTNER_001_PAID_WEBHOOK",
            sources=["hackernews"],
            signal_types=["TUTORIAL"],
        ),
        channels_dir=channels_dir,
    )

    result = check_channel(
        "ai_tools_partner_001",
        channels_dir=channels_dir,
        env={},
    )

    assert result.status == "未启用"
    assert result.errors == []
    assert result.missing_secrets == [
        "CHANNEL_AI_TOOLS_PARTNER_001_FREE_WEBHOOK",
    ]
    assert (
        "会员（可选）未配置：CHANNEL_AI_TOOLS_PARTNER_001_PAID_WEBHOOK"
        in result.warnings
    )


def test_check_channel_rejects_unknown_source_when_enabling(tmp_path: Path) -> None:
    channels_dir = tmp_path / "config" / "channels"
    write_channel_file(
        ChannelFileConfig(
            channel_id="ecommerce",
            channel_name="信先行·电商运营",
            active=False,
            category="ecommerce",
            free_webhook_secret_name="CHANNEL_ECOMMERCE_FREE_WEBHOOK",
            paid_webhook_secret_name="",
            sources=["reddit_ecommerce"],
            signal_types=["TUTORIAL"],
        ),
        channels_dir=channels_dir,
    )

    result = check_channel(
        "ecommerce",
        channels_dir=channels_dir,
        env={"CHANNEL_ECOMMERCE_FREE_WEBHOOK": "https://example.com/free"},
        for_enable=True,
        source_ids={"twitter", "reddit_artificial"},
    )

    assert any("reddit_ecommerce" in error for error in result.errors)
    assert result.can_enable is False


def test_runtime_channels_accept_legacy_self_operated_secret_aliases(tmp_path: Path) -> None:
    channels_dir = tmp_path / "config" / "channels"
    write_channel_file(
        ChannelFileConfig(
            channel_id="ai_tools",
            channel_name="信先行·AI工具日报",
            active=True,
            category="ai_tools",
            template_type="action_card",
            free_webhook_secret_name="CHANNEL_AI_TOOLS_FREE_WEBHOOK",
            paid_webhook_secret_name="CHANNEL_AI_TOOLS_PAID_WEBHOOK",
            sources=["hackernews"],
            signal_types=["TUTORIAL"],
        ),
        channels_dir=channels_dir,
    )

    runtime = load_runtime_channels(
        channels_dir=channels_dir,
        env={
            "XINXIANXING_WEBHOOK_URL": "https://example.com/legacy-free",
            "XINXIANXING_PAID_FEISHU_URL": "https://example.com/legacy-paid",
        },
    )

    assert runtime[0].webhook_url == "https://example.com/legacy-free"
    assert runtime[1].webhook_url == "https://example.com/legacy-paid"


def test_review_channel_can_use_open_routing_when_enabled(tmp_path: Path) -> None:
    channels_dir = tmp_path / "config" / "channels"
    channel_data = {
        "channel_id": "review",
        "channel_name": "信先行·内容审核群",
        "description": "全部 Action Card 审核",
        "partner_name": "内部",
        "active": True,
        "category": "review",
        "template_type": "action_card",
        "free_webhook_secret_name": "CHANNEL_REVIEW_FREE_WEBHOOK",
        "paid_webhook_secret_name": "CHANNEL_REVIEW_PAID_WEBHOOK",
        "admin_webhook_secret_name": "XINXIANXING_ADMIN_WEBHOOK",
        "sources": [],
        "signal_types": [],
        "schedule": "daily_8am",
        "max_items_per_push": 20,
        "min_score": 0.0,
        "dedupe_enabled": True,
        "content_tags": [],
    }
    channels_dir.mkdir(parents=True)
    (channels_dir / "review.json").write_text(
        json.dumps(channel_data, ensure_ascii=False),
        encoding="utf-8",
    )

    result = check_channel(
        "review",
        channels_dir=channels_dir,
        env={
            "CHANNEL_REVIEW_FREE_WEBHOOK": "https://example.com/free",
            "CHANNEL_REVIEW_PAID_WEBHOOK": "https://example.com/paid",
        },
    )

    assert result.status == "已启用"
    assert result.errors == []
    assert result.missing_secrets == []
