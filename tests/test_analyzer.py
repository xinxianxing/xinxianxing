import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

import src.ai.analyzer as analyzer_module
from src.ai.analyzer import ContentAnalyzer
from src.models import ContentItem, SourceType


def _make_item(item_id: str) -> ContentItem:
    return ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title=f"Item {item_id}",
        url="https://example.com/item",
        published_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
    )


def test_analyze_batch_does_not_sleep_by_default(monkeypatch):
    analyzer = ContentAnalyzer(SimpleNamespace())
    items = [_make_item("rss:test:1"), _make_item("rss:test:2")]
    sleep_calls = []

    async def fake_analyze_item(item):
        item.ai_score = 8.0

    async def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)
    monkeypatch.setattr(analyzer_module.asyncio, "sleep", fake_sleep)

    result = asyncio.run(analyzer.analyze_batch(items))

    assert len(result) == 2
    assert sleep_calls == []


def test_analyze_batch_sleeps_between_items_when_throttle_configured(monkeypatch):
    client = SimpleNamespace(config=SimpleNamespace(throttle_sec=1.5))
    analyzer = ContentAnalyzer(client)
    items = [_make_item("rss:test:1"), _make_item("rss:test:2"), _make_item("rss:test:3")]
    sleep_calls = []

    async def fake_analyze_item(item):
        item.ai_score = 8.0

    async def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)
    monkeypatch.setattr(analyzer_module.asyncio, "sleep", fake_sleep)

    asyncio.run(analyzer.analyze_batch(items))

    assert sleep_calls == [1.5, 1.5]


def test_analyze_batch_concurrent_processing(monkeypatch):
    """Verify that higher concurrency allows overlapping item processing."""
    client = SimpleNamespace(config=SimpleNamespace(analysis_concurrency=3))
    analyzer = ContentAnalyzer(client)
    items = [_make_item(f"rss:test:{i}") for i in range(5)]
    active_count = 0
    max_active = 0

    async def fake_analyze_item(item):
        nonlocal active_count, max_active
        active_count += 1
        max_active = max(max_active, active_count)
        await asyncio.sleep(0.05)  # Small delay to allow overlap
        active_count -= 1

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)

    asyncio.run(analyzer.analyze_batch(items))

    assert max_active == 3
    assert all(item.ai_score is None for item in items)  # None because fake_analyze_item doesn't set it


def test_analyze_batch_concurrent_preserves_order(monkeypatch):
    """Verify that analyze_batch preserves input order in results."""
    client = SimpleNamespace(config=SimpleNamespace(analysis_concurrency=3))
    analyzer = ContentAnalyzer(client)
    items = [_make_item(f"rss:test:{i}") for i in range(5)]

    async def fake_analyze_item(item):
        item.ai_score = float(item.id.split(":")[-1]) * 10

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)

    result = asyncio.run(analyzer.analyze_batch(items))

    assert [item.id for item in result] == [item.id for item in items]


def test_analyze_item_populates_action_card_fields():
    item = _make_item("rss:test:action")

    class FakeClient:
        config = SimpleNamespace()

        async def complete(self, system, user):
            return """
            {
              "title": "AI客服工具推出企业版",
              "what_happened": "某AI客服工具发布企业版，新增知识库和工单联动。",
              "why_it_matters": "这会降低中小企业部署自动客服的门槛。",
              "who_should_care": ["AI创业者", "SaaS产品经理"],
              "opportunities": ["拆解其定价页，验证垂直行业客服场景"],
              "suggested_actions": ["跟踪该产品30天内的客户案例"],
              "risk": "市场竞争较强，需验证真实留存。",
              "score": 8.5,
              "signal_type": "TOOL"
            }
            """

    analyzer = ContentAnalyzer(FakeClient())
    asyncio.run(analyzer._analyze_item(item))

    assert item.title == "AI客服工具推出企业版"
    assert item.what_happened.startswith("某AI客服工具")
    assert item.why_it_matters.startswith("这会降低")
    assert item.who_should_care == ["AI创业者", "SaaS产品经理"]
    assert item.opportunities == ["拆解其定价页，验证垂直行业客服场景"]
    assert item.suggested_actions == ["跟踪该产品30天内的客户案例"]
    assert item.risk == "市场竞争较强，需验证真实留存。"
    assert item.score == 8.5
    assert item.ai_score == 8.5
    assert item.ai_summary == item.what_happened
    assert item.intro == item.what_happened
    assert item.how_to == item.opportunities
    assert item.suitable_for == item.who_should_care
    assert item.evidence == item.why_it_matters
    assert item.credibility_risk == item.risk
    assert item.utility_score == item.score
    assert item.metadata["action_card"]["signal_type"] == "TOOL"


def test_money_case_includes_survivorship_bias_warning():
    item = _make_item("rss:test:money")

    class FakeClient:
        config = SimpleNamespace()

        async def complete(self, system, user):
            return """
            {
              "title": "用AI模板副业接单",
              "intro": "作者分享用AI模板接单的副业案例。",
              "how_to": ["整理模板", "发布到接单平台"],
              "suitable_for": ["AI副业研究者"],
              "evidence": "未提供具体数据",
              "credibility_risk": "原文未说明获客成本。",
              "score": 6,
              "signal_type": "MONEY_CASE",
              "source_url": "https://example.com/item"
            }
            """

    analyzer = ContentAnalyzer(FakeClient())
    asyncio.run(analyzer._analyze_item(item))

    assert item.signal_type.value == "MONEY_CASE"
    assert "网络案例可能存在夸大或幸存者偏差，请自行甄别" in item.credibility_risk
    assert item.metadata["action_card"]["credibility_risk"] == item.credibility_risk
