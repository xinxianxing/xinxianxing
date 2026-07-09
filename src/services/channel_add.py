"""Interactive CLI for adding a channel configuration."""

from __future__ import annotations

import json
import re
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Confirm, FloatPrompt, Prompt

from ..models import SignalType

console = Console()

CONTENT_TAG_OPTIONS = [
    "ai",
    "tutorial",
    "monetization",
    "money_case",
    "productivity",
    "productivity_tip",
    "ecommerce",
    "trend",
    "tool",
    "news",
]


def _slug_source_id(prefix: str, value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return f"{prefix}_{slug}" if slug else prefix


def _secret_name_for_channel(channel_id: str) -> str:
    suffix = re.sub(r"[^A-Za-z0-9]+", "_", channel_id.upper()).strip("_")
    return f"CHANNEL_{suffix}_WEBHOOK"


def _collect_source_ids(config: dict) -> list[str]:
    sources = config.get("sources", {})
    ids: list[str] = []

    hackernews = sources.get("hackernews") or {}
    if hackernews.get("enabled", True):
        ids.append(str(hackernews.get("id") or "hackernews"))

    for feed in sources.get("rss") or []:
        if not feed.get("enabled", True):
            continue
        ids.append(str(feed.get("id") or _slug_source_id("rss", feed.get("name", ""))))

    reddit = sources.get("reddit") or {}
    if reddit.get("enabled", True):
        for sub in reddit.get("subreddits") or []:
            if sub.get("enabled", True):
                ids.append(
                    str(sub.get("id") or _slug_source_id("reddit", sub.get("subreddit", "")))
                )
        for user in reddit.get("users") or []:
            if user.get("enabled", True):
                ids.append(
                    str(user.get("id") or _slug_source_id("reddit_user", user.get("username", "")))
                )

    telegram = sources.get("telegram") or {}
    if telegram.get("enabled", True):
        for channel in telegram.get("channels") or []:
            if channel.get("enabled", True):
                ids.append(
                    str(channel.get("id") or _slug_source_id("telegram", channel.get("channel", "")))
                )

    twitter = sources.get("twitter") or {}
    if twitter.get("enabled", False):
        ids.append(str(twitter.get("id") or "twitter"))

    openbb = sources.get("openbb") or {}
    if openbb.get("enabled", False):
        for watchlist in openbb.get("watchlists") or []:
            if watchlist.get("enabled", True):
                ids.append(
                    str(watchlist.get("id") or _slug_source_id("openbb", watchlist.get("name", "")))
                )

    ossinsight = sources.get("ossinsight") or {}
    if ossinsight.get("enabled", False):
        ids.append(str(ossinsight.get("id") or "ossinsight"))

    seen: set[str] = set()
    unique_ids = []
    for source_id in ids:
        if source_id and source_id not in seen:
            seen.add(source_id)
            unique_ids.append(source_id)
    return unique_ids


def _parse_choices(raw: str, options: list[str]) -> list[str]:
    selected: list[str] = []
    for part in raw.split(","):
        token = part.strip()
        if not token:
            continue
        if token.isdigit():
            index = int(token) - 1
            if 0 <= index < len(options):
                selected.append(options[index])
                continue
        selected.append(token)

    seen: set[str] = set()
    return [value for value in selected if not (value in seen or seen.add(value))]


def _prompt_multi_select(title: str, options: list[str]) -> list[str]:
    console.print(f"\n[bold]{title}[/bold]")
    for index, option in enumerate(options, start=1):
        console.print(f"  {index}. {option}")
    raw = Prompt.ask("输入编号或名称，多个用英文逗号分隔")
    return _parse_choices(raw, options)


def main() -> None:
    """CLI entry point for horizon-channel-add."""
    load_dotenv()
    config_path = Path("data/config.json")
    if not config_path.exists():
        raise SystemExit("data/config.json 不存在，请先在项目根目录运行。")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    channels = config.setdefault("channels", [])
    existing_ids = {channel.get("id") for channel in channels}

    console.print("[bold cyan]新增信先行 Channel[/bold cyan]")
    channel_id = Prompt.ask("channel id，例如 ai-tools 或 ecommerce").strip()
    if not channel_id:
        raise SystemExit("channel id 不能为空。")
    if channel_id in existing_ids:
        raise SystemExit(f"channel id 已存在：{channel_id}")

    name = Prompt.ask("群名称，用于推送标题").strip()
    if not name:
        raise SystemExit("群名称不能为空。")

    source_ids = _collect_source_ids(config)
    selected_sources = _prompt_multi_select("选择信源 source id", source_ids)
    content_tags = _prompt_multi_select("选择内容标签 content_tags", CONTENT_TAG_OPTIONS)
    signal_options = [signal.value for signal in SignalType]
    selected_signals = _prompt_multi_select("选择 signal_types", signal_options)
    min_score = FloatPrompt.ask("最低评分 min_score", default=6.0)
    active = Confirm.ask("是否立即启用 active", default=True)

    secret_name = _secret_name_for_channel(channel_id)
    channels.append(
        {
            "id": channel_id,
            "name": name,
            "webhook_url": f"${{{secret_name}}}",
            "content_tags": content_tags,
            "sources": selected_sources,
            "signal_types": selected_signals,
            "min_score": min_score,
            "active": active,
        }
    )

    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    console.print(f"\n[green]已写入：{config_path}[/green]")
    console.print(f"[yellow]请在 GitHub Actions Secrets 新增：{secret_name}[/yellow]")


if __name__ == "__main__":
    main()
