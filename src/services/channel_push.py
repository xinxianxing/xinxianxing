"""Push existing daily draft cards to configured Feishu channels."""

from __future__ import annotations

import argparse
import asyncio
import html
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from rich.console import Console

from ..ai.summarizer import DailySummarizer
from ..models import ContentItem, SignalType, SourceType, WebhookConfig
from ..storage.manager import StorageManager
from .webhook import (
    WebhookDeliveryError,
    WebhookNotifier,
    send_admin_alert,
)


console = Console()

_SECTION_RE = re.compile(
    r'<section[^>]*class="action-card"[^>]*data-card-id="(?P<id>[^"]+)"[^>]*>'
    r"(?P<body>.*?)</section>",
    re.DOTALL,
)
_TITLE_RE = re.compile(r"^## \[(?P<title>.+?)\]\((?P<url>.+?)\)", re.MULTILINE)
_TYPE_RE = re.compile(r"\*\*栏目分类\*\*: `(?P<type>[A-Z_]+)`")
_SCORE_RE = re.compile(r"\*\*实用度评分\*\*: Score: (?P<score>[0-9.]+) / 10")
_TOTAL_RE = re.compile(r"从\s*(?P<total>\d+)\s*条内容中筛选出")
_DATE_FROM_DRAFT_RE = re.compile(r"xinxianxing-(?P<date>\d{4}-\d{2}-\d{2})-(?P<lang>[a-z]+)\.md$")


@dataclass(frozen=True)
class ChannelPushFailure:
    """One failed channel push result."""

    channel_id: str
    channel_name: str
    reason: str
    failed_at: datetime


class ChannelPushError(RuntimeError):
    """Raised after attempting all channel pushes when at least one failed."""

    def __init__(self, failures: list[ChannelPushFailure]):
        self.failures = failures
        joined = "; ".join(
            f"{failure.channel_id}: {failure.reason}" for failure in failures
        )
        super().__init__(f"{len(failures)} channel push(es) failed: {joined}")


def parse_draft_cards(markdown_text: str) -> tuple[list[ContentItem], int]:
    """Parse generated daily draft Markdown back into ContentItems."""
    total_match = _TOTAL_RE.search(markdown_text)
    total_fetched = int(total_match.group("total")) if total_match else 0
    items: list[ContentItem] = []

    for index, match in enumerate(_SECTION_RE.finditer(markdown_text), start=1):
        section = match.group("body")
        title_match = _TITLE_RE.search(section)
        if not title_match:
            continue

        card_id = html.unescape(match.group("id"))
        title = _clean_text(title_match.group("title"))
        url = title_match.group("url").strip()
        signal = _parse_signal_type(_first_match(_TYPE_RE, section, "type"))
        intro = _extract_field(section, "一句话简介")
        how_to = _extract_list_field(section, "具体怎么做")
        suitable_for = _extract_tags_field(section, "适合谁/适用场景")
        evidence = _extract_field(section, "效果或数据")
        risk = _extract_field(section, "可信度/风险提示")
        score = _parse_score(section)
        source_type = _source_type_from_card_id(card_id)
        source_line = _extract_source_line(section)
        metadata = _metadata_from_source_line(source_type, source_line, url)
        metadata.update(
            {
                "title_zh": title,
                "signal_type": signal.value if signal else None,
                "action_card_index": index,
                "content_tags": _content_tags_for_signal(signal),
            }
        )

        try:
            item = ContentItem(
                id=card_id,
                source_type=source_type,
                title=title,
                url=url,
                content=intro,
                author=metadata.get("author") or metadata.get("feed_name"),
                published_at=datetime.now(timezone.utc),
                metadata=metadata,
                ai_score=score,
                ai_summary=intro,
                ai_tags=suitable_for,
                score=score,
                signal_type=signal,
                intro=intro,
                how_to=how_to,
                suitable_for=suitable_for,
                evidence=evidence,
                credibility_risk=risk,
                utility_score=score,
            )
        except Exception as exc:
            console.print(
                f"[yellow]跳过无法解析的 draft 卡片 {card_id}: {exc}[/yellow]"
            )
            continue

        items.append(item)

    return items, total_fetched or len(items)


async def push_draft_channels(
    *,
    date: str,
    language: str = "zh",
    data_dir: str | Path = "data",
    admin_webhook_url: str | None = None,
    channel_ids: set[str] | None = None,
    exclude_channel_ids: set[str] | None = None,
) -> int:
    """Push one daily draft to all matching active channels.

    Returns the number of channel messages sent. Raises ChannelPushError after
    all attempts if any configured channel returns an error.
    """
    storage = StorageManager(data_dir=str(data_dir))
    config = storage.load_config()
    include = {channel_id.strip() for channel_id in (channel_ids or set()) if channel_id.strip()}
    exclude = {
        channel_id.strip()
        for channel_id in (exclude_channel_ids or set())
        if channel_id.strip()
    }
    if include or exclude:
        def _channel_keys(channel) -> set[str]:
            keys = {channel.id}
            if channel.logical_channel_id:
                keys.add(channel.logical_channel_id)
            return keys

        config.channels = [
            channel
            for channel in config.channels
            if (not include or not _channel_keys(channel).isdisjoint(include))
            and _channel_keys(channel).isdisjoint(exclude)
        ]
    draft_path = storage.drafts_dir / f"xinxianxing-{date}-{language}.md"
    if not draft_path.exists():
        raise FileNotFoundError(f"Daily draft not found: {draft_path}")

    summary = draft_path.read_text(encoding="utf-8")
    items, total_fetched = parse_draft_cards(summary)
    if not items:
        raise ValueError(f"No Action Cards found in draft: {draft_path}")

    webhook_config = config.webhook or WebhookConfig(
        enabled=True,
        url_env=None,
        platform="generic",
        layout="markdown",
    )
    webhook_config.enabled = True

    notifier = WebhookNotifier(
        webhook_config,
        console=console,
        site_base_url=config.site.base_url,
        draft_preview_links=not config.publishing.auto_publish,
        channels=config.channels,
    )
    messages = notifier.build_channel_feishu_messages(
        important_items=items,
        paid_items=items,
        date=date,
        lang=language,
    )
    if not messages:
        console.print("[yellow]没有可推送的 active channel 消息。[/yellow]")
        return 0

    failures: list[ChannelPushFailure] = []
    sent_count = 0
    for channel, message in messages:
        try:
            await notifier.notify_channel_feishu(
                channel,
                message,
                raise_on_error=True,
            )
            sent_count += 1
        except WebhookDeliveryError as exc:
            failed_at = datetime.now(timezone.utc)
            failure = ChannelPushFailure(
                channel_id=channel.id,
                channel_name=channel.name,
                reason=str(exc),
                failed_at=failed_at,
            )
            failures.append(failure)
            await send_admin_alert(
                admin_webhook_url,
                channel_id=channel.id,
                channel_name=channel.name,
                reason=str(exc),
                failed_at=failed_at,
            )

    if failures:
        raise ChannelPushError(failures)
    return sent_count


def _default_date() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")


def _clean_text(value: object) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _first_match(pattern: re.Pattern[str], text: str, group: str) -> str:
    match = pattern.search(text)
    return match.group(group) if match else ""


def _extract_field(section: str, label: str) -> str:
    pattern = re.compile(
        rf"\*\*{re.escape(label)}\*\*:\s*(?P<value>.*?)(?=\n\n\*\*|\n\n<|\n</section>|\Z)",
        re.DOTALL,
    )
    match = pattern.search(section)
    if not match:
        return ""
    return _clean_text(_strip_markdown_list(match.group("value")))


def _extract_list_field(section: str, label: str) -> list[str]:
    raw = _extract_raw_field(section, label)
    if not raw:
        return []
    items: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        stripped = re.sub(r"^[-*]\s+", "", stripped)
        items.append(_clean_text(stripped))
    return items


def _extract_raw_field(section: str, label: str) -> str:
    pattern = re.compile(
        rf"\*\*{re.escape(label)}\*\*:\s*(?P<value>.*?)(?=\n\n\*\*|\n\n<|\Z)",
        re.DOTALL,
    )
    match = pattern.search(section)
    return match.group("value").strip() if match else ""


def _extract_tags_field(section: str, label: str) -> list[str]:
    raw = _extract_raw_field(section, label)
    tags = re.findall(r"`([^`]+)`", raw)
    if tags:
        return [_clean_text(tag.lstrip("#")) for tag in tags if _clean_text(tag)]
    return [_clean_text(raw)] if raw else []


def _strip_markdown_list(value: str) -> str:
    lines = []
    for line in value.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        stripped = re.sub(r"^[-*]\s+", "", stripped)
        lines.append(stripped)
    return " ".join(lines)


def _parse_signal_type(value: str) -> SignalType | None:
    if not value:
        return None
    try:
        return SignalType(value.strip().upper())
    except ValueError:
        return None


def _parse_score(section: str) -> float | None:
    score_text = _first_match(_SCORE_RE, section, "score")
    if not score_text:
        return None
    try:
        return float(score_text)
    except ValueError:
        return None


def _source_type_from_card_id(card_id: str) -> SourceType:
    raw = card_id.split(":", 1)[0].strip().lower()
    mapping = {
        "manual": SourceType.MANUAL,
        "github": SourceType.GITHUB,
        "hackernews": SourceType.HACKERNEWS,
        "rss": SourceType.RSS,
        "reddit": SourceType.REDDIT,
        "telegram": SourceType.TELEGRAM,
        "twitter": SourceType.TWITTER,
        "openbb": SourceType.OPENBB,
        "ossinsight": SourceType.OSSINSIGHT,
    }
    return mapping.get(raw, SourceType.RSS)


def _extract_source_line(section: str) -> str:
    marker = "**来源链接**"
    if marker not in section:
        return ""
    tail = section.split(marker, 1)[1].splitlines()[1:]
    for line in tail:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("**", "<", "-", "#")):
            continue
        return stripped
    return ""


def _metadata_from_source_line(
    source_type: SourceType,
    source_line: str,
    url: str,
) -> dict[str, object]:
    parts = [_clean_text(part) for part in source_line.split("·") if _clean_text(part)]
    metadata: dict[str, object] = {"source_ids": [source_type.value]}
    if source_type is SourceType.HACKERNEWS:
        metadata["source_id"] = "hackernews"
        metadata["source_ids"].append("hackernews")
    elif source_type is SourceType.TWITTER:
        metadata["source_id"] = "twitter"
        metadata["source_ids"].append("twitter")
        if len(parts) >= 2:
            metadata["author"] = parts[1]
    elif source_type is SourceType.REDDIT:
        subreddit = _subreddit_from_parts_or_url(parts, url)
        if subreddit:
            metadata["subreddit"] = subreddit
            metadata["source_id"] = f"reddit_{_slug(subreddit)}"
            metadata["source_ids"].append(metadata["source_id"])
        if len(parts) >= 3:
            metadata["author"] = parts[2]
    elif source_type is SourceType.RSS:
        feed_name = parts[1] if len(parts) >= 2 and parts[0].lower() == "rss" else ""
        if feed_name:
            metadata["feed_name"] = feed_name
            metadata["source_id"] = _slug(feed_name)
            metadata["source_ids"].append(metadata["source_id"])
    elif len(parts) >= 2:
        metadata["author"] = parts[1]
    return metadata


def _subreddit_from_parts_or_url(parts: list[str], url: str) -> str:
    for part in parts:
        if part.lower().startswith("r/"):
            return part[2:]
    match = re.search(r"/r/([^/]+)/", url)
    return match.group(1) if match else ""


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _content_tags_for_signal(signal: SignalType | None) -> list[str]:
    if signal is SignalType.TUTORIAL:
        return ["ai", "tutorial"]
    if signal is SignalType.MONEY_CASE:
        return ["ai", "monetization", "money_case"]
    if signal is SignalType.PRODUCTIVITY_TIP:
        return ["ai", "productivity", "productivity_tip"]
    if signal is SignalType.TREND:
        return ["trend"]
    if signal is SignalType.TOOL:
        return ["ai", "tool"]
    return []


def main() -> None:
    """CLI entry point for pushing the existing daily draft to channels."""
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Push today's generated 信先行 draft to configured channels",
    )
    parser.add_argument("--date", default=_default_date(), help="Draft date, YYYY-MM-DD")
    parser.add_argument("--language", default="zh", help="Draft language, default zh")
    parser.add_argument("--data-dir", default="data", help="Data directory, default data")
    parser.add_argument(
        "--channel-id",
        action="append",
        default=[],
        help="Only push the specified channel id. Repeat for multiple ids.",
    )
    parser.add_argument(
        "--exclude-channel-id",
        action="append",
        default=[],
        help="Skip the specified channel id. Repeat for multiple ids.",
    )
    args = parser.parse_args()

    try:
        sent = asyncio.run(
            push_draft_channels(
                date=args.date,
                language=args.language,
                data_dir=args.data_dir,
                admin_webhook_url=os.getenv("XINXIANXING_ADMIN_WEBHOOK"),
                channel_ids=set(args.channel_id),
                exclude_channel_ids=set(args.exclude_channel_id),
            )
        )
    except Exception as exc:
        console.print(f"[bold red]频道推送失败：{exc}[/bold red]")
        raise SystemExit(1) from exc

    console.print(f"[bold green]频道推送完成，共发送 {sent} 条频道消息。[/bold green]")


if __name__ == "__main__":
    main()
