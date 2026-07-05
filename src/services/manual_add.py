"""Manual URL ingestion for generating one 信先行 Action Card."""

import argparse
import asyncio
import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date
from dotenv import load_dotenv
from rich.console import Console

from ..ai.analyzer import ContentAnalyzer
from ..ai.client import create_ai_client
from ..ai.summarizer import DailySummarizer, _pangu
from ..models import Config, ContentItem, SourceType
from ..storage.manager import ConfigError, StorageManager


console = Console()

_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)
_MIN_CONTENT_CHARS = 60
_MAX_CONTENT_CHARS = 12000
_ACTION_CARD_SECTION_RE = re.compile(r'<section\s+class="action-card"', re.I)
_HR_RE = re.compile(r"(?m)^---\s*$")


class ManualAddError(RuntimeError):
    """Raised when manual URL ingestion cannot produce a usable Action Card."""


@dataclass
class ManualAddResult:
    """Result of manually adding one URL."""

    item: ContentItem
    draft_path: Path
    docs_draft_path: Path | None
    card_markdown: str


def _clean_text(value: str) -> str:
    """Normalize whitespace while preserving paragraph breaks."""
    lines = [re.sub(r"\s+", " ", line).strip() for line in value.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines).strip()


def _first_meta(soup: BeautifulSoup, *names: str) -> str:
    """Return the first matching meta content for name/property keys."""
    for name in names:
        tag = soup.find("meta", attrs={"property": name}) or soup.find(
            "meta", attrs={"name": name}
        )
        if tag and tag.get("content"):
            return _clean_text(str(tag["content"]))
    return ""


def _extract_title(soup: BeautifulSoup, fallback_url: str) -> str:
    title = _first_meta(soup, "og:title", "twitter:title")
    if title:
        return title

    if soup.title and soup.title.string:
        title = _clean_text(soup.title.string)
        if title:
            return title

    h1 = soup.find("h1")
    if h1:
        title = _clean_text(h1.get_text(" "))
        if title:
            return title

    parsed = urlparse(fallback_url)
    return parsed.path.rstrip("/").split("/")[-1] or parsed.netloc or fallback_url


def _extract_published_at(soup: BeautifulSoup) -> datetime:
    raw = _first_meta(
        soup,
        "article:published_time",
        "article:modified_time",
        "date",
        "datePublished",
        "pubdate",
    )
    if raw:
        try:
            parsed = parse_date(raw)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except Exception:
            pass

    return datetime.now(timezone.utc)


def _candidate_texts(node) -> list[str]:
    """Extract readable block-level text from a BeautifulSoup node."""
    texts: list[str] = []
    seen: set[str] = set()
    for element in node.find_all(
        ["h1", "h2", "h3", "p", "li", "blockquote", "pre"],
        recursive=True,
    ):
        text = _clean_text(element.get_text(" "))
        if len(text) < 8 or text in seen:
            continue
        seen.add(text)
        texts.append(text)

    if not texts:
        fallback = _clean_text(node.get_text("\n"))
        if fallback:
            texts.append(fallback)

    return texts


def _candidate_score(texts: Iterable[str]) -> int:
    values = list(texts)
    return sum(min(len(text), 2000) for text in values) + len(values) * 20


def extract_readable_content(html: str, url: str) -> tuple[str, str, datetime]:
    """Extract title, body text, and publication date from an HTML page."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "svg",
            "iframe",
            "form",
            "nav",
            "header",
            "footer",
            "aside",
        ]
    ):
        tag.decompose()

    title = _extract_title(soup, url)
    published_at = _extract_published_at(soup)
    meta_description = _first_meta(
        soup,
        "og:description",
        "twitter:description",
        "description",
    )

    candidates = []
    selectors = [
        "article",
        "main",
        "[role='main']",
        ".post-content",
        ".entry-content",
        ".article-content",
        ".content",
    ]
    for selector in selectors:
        candidates.extend(soup.select(selector))

    if soup.body:
        candidates.append(soup.body)

    best_texts: list[str] = []
    best_score = 0
    seen_nodes: set[int] = set()
    for node in candidates:
        node_id = id(node)
        if node_id in seen_nodes:
            continue
        seen_nodes.add(node_id)
        texts = _candidate_texts(node)
        score = _candidate_score(texts)
        if score > best_score:
            best_score = score
            best_texts = texts

    body = "\n\n".join(best_texts).strip()
    if len(body) < len(meta_description):
        body = meta_description

    body = _clean_text(body)
    if len(body) > _MAX_CONTENT_CHARS:
        body = body[:_MAX_CONTENT_CHARS].rsplit("\n", 1)[0].strip() or body[:_MAX_CONTENT_CHARS]

    if len(body) < _MIN_CONTENT_CHARS:
        raise ManualAddError(
            "链接打开成功，但正文太短，可能是反爬、登录页、纯图片页，或页面需要 JavaScript 渲染。"
        )

    return title, body, published_at


async def fetch_url_as_item(url: str, client: httpx.AsyncClient | None = None) -> ContentItem:
    """Fetch a URL and convert its readable content into a manual ContentItem."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ManualAddError("请输入完整的 http/https 链接。")

    owns_client = client is None
    if client is None:
        client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": _USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            },
        )

    try:
        response = await client.get(url)
        if response.status_code in {401, 403}:
            raise ManualAddError(
                f"链接抓取失败：HTTP {response.status_code}。页面可能需要登录或拦截了机器人访问。"
            )
        response.raise_for_status()

        content_type = response.headers.get("content-type", "").lower()
        if content_type and not any(
            allowed in content_type
            for allowed in ("text/html", "application/xhtml+xml", "text/plain")
        ):
            raise ManualAddError(
                f"链接不是可解析的网页正文类型：{content_type}。"
            )

        title, body, published_at = extract_readable_content(response.text, str(response.url))
    except ManualAddError:
        raise
    except httpx.TimeoutException as exc:
        raise ManualAddError("链接抓取超时，请稍后重试或换一个可公开访问的链接。") from exc
    except httpx.HTTPStatusError as exc:
        raise ManualAddError(
            f"链接抓取失败：HTTP {exc.response.status_code}。"
        ) from exc
    except httpx.HTTPError as exc:
        raise ManualAddError(f"链接抓取失败：{exc}") from exc
    finally:
        if owns_client:
            await client.aclose()

    digest = hashlib.sha256(str(response.url).encode("utf-8")).hexdigest()[:16]
    return ContentItem(
        id=f"manual:url:{digest}",
        source_type=SourceType.MANUAL,
        title=title,
        url=str(response.url),
        content=body,
        author=parsed.netloc,
        published_at=published_at,
        metadata={
            "category": "manual",
            "feed_name": "Manual Add",
            "manual_url": url,
            "extracted_chars": len(body),
        },
    )


def _toc_entry(item: ContentItem, language: str, index: int) -> str:
    title = str(item.metadata.get(f"title_{language}") or item.title)
    title = title.replace("[", "(").replace("]", ")")
    if language == "zh":
        title = _pangu(title)
    score = item.ai_score or "?"
    signal_type = item.signal_type.value if item.signal_type else "NEWS"
    return f"{index}. [{title}](#item-{index}) · {signal_type} · Score: {score} / 10"


def _increment_summary_counts(markdown: str) -> str:
    """Bump the visible selected/total counts in an existing draft when possible."""
    def zh_repl(match: re.Match) -> str:
        total = int(match.group(2)) + 1
        selected = int(match.group(4)) + 1
        return f"{match.group(1)}{total}{match.group(3)}{selected}{match.group(5)}"

    markdown, zh_count = re.subn(
        r"(从\s+)(\d+)(\s+条内容中筛选出\s+)(\d+)(\s+条教程/案例/技巧。)",
        zh_repl,
        markdown,
        count=1,
    )
    if zh_count:
        return markdown

    def en_repl(match: re.Match) -> str:
        total = int(match.group(2)) + 1
        selected = int(match.group(4)) + 1
        return f"{match.group(1)}{total}{match.group(3)}{selected}{match.group(5)}"

    markdown = re.sub(
        r"(From\s+)(\d+)(\s+items,\s+)(\d+)(\s+tutorial/case/tip cards were selected)",
        en_repl,
        markdown,
        count=1,
    )
    return markdown


def _insert_toc_entry(markdown: str, entry: str) -> str:
    dividers = list(_HR_RE.finditer(markdown))
    if len(dividers) < 2:
        return markdown

    insert_at = dividers[1].start()
    before = markdown[:insert_at].rstrip()
    after = markdown[insert_at:].lstrip("\n")
    return f"{before}\n{entry}\n\n{after}"


def _append_card_to_markdown(path: Path, item: ContentItem, language: str) -> str:
    summarizer = DailySummarizer()
    original = path.read_text(encoding="utf-8")
    index = len(_ACTION_CARD_SECTION_RE.findall(original)) + 1
    card = summarizer.render_action_card(item, language=language, index=index)
    updated = _increment_summary_counts(original)
    updated = _insert_toc_entry(updated, _toc_entry(item, language, index))
    updated = updated.rstrip() + "\n\n" + card
    path.write_text(updated, encoding="utf-8")
    return card


def _docs_draft_path(root: Path, date: str, language: str) -> Path:
    return root / "docs" / "_drafts" / f"{date}-summary-{language}.md"


def _docs_front_matter(date: str, language: str) -> str:
    page_title = f"信先行 Action Cards: {date} ({language.upper()})"
    return (
        "---\n"
        "layout: default\n"
        f'title: "{page_title}"\n'
        f"date: {date}\n"
        f"lang: {language}\n"
        "---\n\n"
    )


def _strip_h1(markdown: str) -> str:
    first_line = markdown.strip().split("\n")[0]
    if first_line.startswith("# "):
        parts = markdown.split("\n", 1)
        if len(parts) > 1:
            return parts[1].strip()
    return markdown


async def append_item_to_drafts(
    item: ContentItem,
    storage: StorageManager,
    date: str,
    language: str = "zh",
) -> tuple[Path, Path | None, str]:
    """Append one analyzed item to today's data draft and docs review draft."""
    data_path = storage.drafts_dir / f"xinxianxing-{date}-{language}.md"
    summarizer = DailySummarizer()

    if data_path.exists():
        card_markdown = _append_card_to_markdown(data_path, item, language)
    else:
        summary = await summarizer.generate_summary(
            [item],
            date,
            total_fetched=1,
            language=language,
        )
        data_path = storage.save_daily_draft(date, summary, language=language)
        card_markdown = summarizer.render_action_card(item, language=language, index=1)

    docs_path = _docs_draft_path(storage.data_dir.parent, date, language)
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    if docs_path.exists():
        _append_card_to_markdown(docs_path, item, language)
    else:
        data_markdown = data_path.read_text(encoding="utf-8")
        docs_path.write_text(
            _docs_front_matter(date, language) + _strip_h1(data_markdown),
            encoding="utf-8",
        )

    return data_path, docs_path, card_markdown


async def add_url(
    url: str,
    config: Config,
    storage: StorageManager,
    *,
    date: str | None = None,
    language: str = "zh",
) -> ManualAddResult:
    """Fetch one URL, generate an Action Card, and append it to today's draft."""
    item = await fetch_url_as_item(url)

    ai_client = create_ai_client(config.ai)
    analyzer = ContentAnalyzer(ai_client)
    analyzed = await analyzer.analyze_batch([item])
    item = analyzed[0]
    if not item.metadata.get("action_card"):
        raise ManualAddError("AI 已返回结果，但没有生成可用的 Action Card。")

    date = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    draft_path, docs_draft_path, card_markdown = await append_item_to_drafts(
        item,
        storage,
        date,
        language=language,
    )

    return ManualAddResult(
        item=item,
        draft_path=draft_path,
        docs_draft_path=docs_draft_path,
        card_markdown=card_markdown,
    )


def main() -> None:
    """CLI entry point for `horizon-add`."""
    parser = argparse.ArgumentParser(
        description="Manually add one article/tweet URL and generate a 信先行 Action Card."
    )
    parser.add_argument("url", help="Article or tweet URL to add")
    parser.add_argument("--date", help="Draft date, defaults to 信先行's UTC day")
    parser.add_argument("--lang", default="zh", help="Draft language, defaults to zh")
    args = parser.parse_args()

    load_dotenv()
    storage = StorageManager(data_dir="data")
    try:
        config = storage.load_config()
    except (FileNotFoundError, ConfigError) as exc:
        console.print(f"[bold red]配置加载失败：{exc}[/bold red]")
        sys.exit(1)

    try:
        result = asyncio.run(
            add_url(
                args.url,
                config,
                storage,
                date=args.date,
                language=args.lang,
            )
        )
    except ManualAddError as exc:
        console.print(f"[bold red]手动添加失败：{exc}[/bold red]")
        sys.exit(1)
    except Exception as exc:
        console.print(f"[bold red]手动添加失败：{type(exc).__name__}: {exc}[/bold red]")
        sys.exit(1)

    console.print(f"[green]已生成 Action Card 并写入：{result.draft_path}[/green]")
    if result.docs_draft_path:
        console.print(f"[green]已同步到 review draft：{result.docs_draft_path}[/green]")
    console.print("")
    console.print(result.card_markdown)


if __name__ == "__main__":
    main()
