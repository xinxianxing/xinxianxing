import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

import httpx
import pytest

from src.ai.summarizer import DailySummarizer
from src.models import ContentItem, SignalType, SourceType
from src.services.manual_add import (
    ManualAddError,
    append_item_to_drafts,
    extract_readable_content,
    fetch_url_as_item,
)
from src.storage.manager import StorageManager


def _make_card(title: str, url: str, score: float = 8.0) -> ContentItem:
    item = ContentItem(
        id=f"manual:url:{title}",
        source_type=SourceType.MANUAL,
        title=title,
        url=url,
        content="正文",
        author="example.com",
        published_at=datetime(2026, 7, 4, tzinfo=timezone.utc),
        fetched_at=datetime(2026, 7, 4, tzinfo=timezone.utc),
        ai_score=score,
        ai_summary="一句话简介",
        signal_type=SignalType.TUTORIAL,
        intro="一句话简介",
        how_to=["第一步", "第二步"],
        suitable_for=["产品经理"],
        evidence="未提供具体数据",
        credibility_risk="需要自行验证。",
    )
    item.metadata["action_card"] = {"title": title}
    return item


def test_extract_readable_content_prefers_article_text():
    html = """
    <html>
      <head>
        <meta property="og:title" content="测试文章">
        <meta property="article:published_time" content="2026-07-04T09:00:00Z">
      </head>
      <body>
        <nav>导航链接不应进入正文</nav>
        <article>
          <h1>测试文章</h1>
          <p>第一段正文，包含足够的信息密度，用于生成 Action Card，并且说明这个方法适合怎样的 AI 工作流。</p>
          <p>第二段正文，说明具体做法和适用场景，包括先整理输入材料、再交给模型处理、最后人工复核结果。</p>
        </article>
      </body>
    </html>
    """
    title, body, published_at = extract_readable_content(html, "https://example.com/a")

    assert title == "测试文章"
    assert "第一段正文" in body
    assert "第二段正文" in body
    assert "导航链接" not in body
    assert published_at == datetime(2026, 7, 4, 9, 0, tzinfo=timezone.utc)


def test_extract_readable_content_raises_for_too_short_body():
    html = "<html><head><title>短页</title></head><body><main><p>太短</p></main></body></html>"

    with pytest.raises(ManualAddError, match="正文太短"):
        extract_readable_content(html, "https://example.com/short")


def test_fetch_url_as_item_rejects_invalid_url():
    with pytest.raises(ManualAddError, match="完整的 http/https 链接"):
        asyncio.run(fetch_url_as_item("not-a-url"))


def test_fetch_url_as_item_raises_clear_error_for_forbidden():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(403, text="forbidden")
    )
    client = httpx.AsyncClient(transport=transport)
    try:
        with pytest.raises(ManualAddError, match="HTTP 403"):
            asyncio.run(fetch_url_as_item("https://example.com/private", client=client))
    finally:
        asyncio.run(client.aclose())


def test_fetch_url_as_item_rejects_non_page_content_type():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            content=b"%PDF-1.4",
            headers={"content-type": "application/pdf"},
            request=request,
        )
    )
    client = httpx.AsyncClient(transport=transport)
    try:
        with pytest.raises(ManualAddError, match="不是可解析的网页正文类型"):
            asyncio.run(fetch_url_as_item("https://example.com/file.pdf", client=client))
    finally:
        asyncio.run(client.aclose())


def test_fetch_url_as_item_timeout_has_clear_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("timed out", request=request)

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    try:
        with pytest.raises(ManualAddError, match="抓取超时"):
            asyncio.run(fetch_url_as_item("https://example.com/slow", client=client))
    finally:
        asyncio.run(client.aclose())


def test_fetch_url_as_item_builds_manual_content_item():
    html = """
    <html>
      <head><title>Manual Test</title></head>
      <body>
        <main>
          <p>This article explains a practical AI workflow with enough text to parse.</p>
          <p>It includes concrete steps and expected outcomes for operators.</p>
        </main>
      </body>
    </html>
    """
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            text=html,
            headers={"content-type": "text/html; charset=utf-8"},
            request=request,
        )
    )
    client = httpx.AsyncClient(transport=transport, follow_redirects=True)
    try:
        item = asyncio.run(fetch_url_as_item("https://example.com/manual", client=client))
    finally:
        asyncio.run(client.aclose())

    assert item.source_type == SourceType.MANUAL
    assert item.title == "Manual Test"
    assert "practical AI workflow" in item.content
    assert item.metadata["feed_name"] == "Manual Add"


def test_append_item_to_new_draft_creates_data_and_docs_copy(tmp_path):
    storage = StorageManager(data_dir=str(tmp_path / "data"))
    item = _make_card("新卡片", "https://example.com/new", score=8.5)

    data_path, docs_path, card = asyncio.run(
        append_item_to_drafts(item, storage, "2026-07-05", language="zh")
    )

    assert data_path.name == "xinxianxing-2026-07-05-zh.md"
    assert data_path.exists()
    assert docs_path is not None
    assert docs_path.name == "2026-07-05-summary-zh.md"
    assert docs_path.read_text(encoding="utf-8").startswith("---\nlayout: default")
    preview_path = tmp_path / "docs" / "drafts" / "2026-07-05-summary-zh.md"
    assert preview_path.exists()
    assert preview_path.read_text(encoding="utf-8") == docs_path.read_text(
        encoding="utf-8"
    )
    assert "新卡片" in card


def test_append_item_to_existing_draft_updates_toc_and_docs_copy(tmp_path):
    storage = StorageManager(data_dir=str(tmp_path / "data"))
    first = _make_card("第一张卡片", "https://example.com/first", score=8.5)
    second = _make_card("第二张卡片", "https://example.com/second", score=7.5)
    summarizer = DailySummarizer()
    initial = asyncio.run(
        summarizer.generate_summary(
            [first],
            "2026-07-04",
            total_fetched=1,
            language="zh",
        )
    )
    storage.save_daily_draft("2026-07-04", initial, language="zh")

    data_path, docs_path, card = asyncio.run(
        append_item_to_drafts(second, storage, "2026-07-04", language="zh")
    )

    data = data_path.read_text(encoding="utf-8")
    docs = docs_path.read_text(encoding="utf-8")
    assert "从 2 条内容中筛选出 2 条教程/案例/技巧。" in data
    assert "2. [第二张卡片](#item-2)" in data
    assert '<a id="item-2"></a>' in data
    assert "第二张卡片" in card
    assert docs.startswith("---\nlayout: default")
    assert "第二张卡片" in docs
    preview_path = tmp_path / "docs" / "drafts" / "2026-07-04-summary-zh.md"
    assert preview_path.exists()
    assert preview_path.read_text(encoding="utf-8") == docs


def test_add_url_raises_when_ai_returns_no_action_card(monkeypatch, tmp_path):
    from src.services import manual_add

    item = ContentItem(
        id="manual:url:missing-card",
        source_type=SourceType.MANUAL,
        title="No Card",
        url="https://example.com/no-card",
        content="Enough extracted content for analysis.",
        author="example.com",
        published_at=datetime(2026, 7, 5, tzinfo=timezone.utc),
    )

    async def fake_fetch_url_as_item(url: str) -> ContentItem:
        return item

    class FakeAnalyzer:
        def __init__(self, ai_client):
            self.ai_client = ai_client

        async def analyze_batch(self, items):
            return items

    monkeypatch.setattr(manual_add, "fetch_url_as_item", fake_fetch_url_as_item)
    monkeypatch.setattr(manual_add, "create_ai_client", lambda ai_config: object())
    monkeypatch.setattr(manual_add, "ContentAnalyzer", FakeAnalyzer)

    storage = StorageManager(data_dir=str(tmp_path / "data"))
    config = SimpleNamespace(ai=object())

    with pytest.raises(ManualAddError, match="没有生成可用的 Action Card"):
        asyncio.run(manual_add.add_url("https://example.com/no-card", config, storage))
