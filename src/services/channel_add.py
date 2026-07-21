"""CLI for creating file-backed channel configuration."""

from __future__ import annotations

import argparse

from dotenv import load_dotenv
from rich.console import Console

from ..models import ChannelFileConfig
from .channel_registry import (
    default_free_secret_name,
    default_paid_secret_name,
    normalize_channel_id,
    write_channel_file,
)


console = Console()


def _csv_values(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _bool_arg(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y", "on"}:
        return True
    if normalized in {"false", "0", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError("active must be true or false")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a 信先行 channel config")
    parser.add_argument("--channel-id", required=True, help="Channel id, e.g. ai_tools_partner_001")
    parser.add_argument("--name", required=True, help="Channel display name")
    parser.add_argument("--partner", default="", help="Partner name")
    parser.add_argument("--description", default="", help="Channel description")
    parser.add_argument("--category", required=True, help="Channel category, e.g. ai_tools")
    parser.add_argument("--template", default="action_card", help="Template type")
    parser.add_argument("--schedule", default="daily_8am", help="Push schedule")
    parser.add_argument("--max-items", type=int, default=10, help="Max cards per push")
    parser.add_argument("--min-score", type=float, default=7.0, help="Minimum score")
    parser.add_argument("--active", type=_bool_arg, default=False, help="true or false; default false")
    parser.add_argument("--sources", default="", help="Comma-separated source ids")
    parser.add_argument("--signal-types", default="", help="Comma-separated signal types")
    parser.add_argument("--content-tags", default="", help="Comma-separated content tags")
    parser.add_argument("--dedupe-enabled", type=_bool_arg, default=True, help="true or false; default true")
    parser.add_argument("--admin-secret", default="XINXIANXING_ADMIN_WEBHOOK", help="Admin alert secret name")
    parser.add_argument("--free-secret", default="", help="Override free webhook secret name")
    parser.add_argument("--paid-secret", default="", help="Override paid webhook secret name")
    return parser


def main() -> None:
    """CLI entry point for xinxianxing-channel-add."""
    load_dotenv()
    args = build_parser().parse_args()
    channel_id = normalize_channel_id(args.channel_id)
    channel = ChannelFileConfig(
        channel_id=channel_id,
        channel_name=args.name,
        description=args.description,
        partner_name=args.partner,
        active=args.active,
        category=args.category,
        template_type=args.template,
        free_webhook_secret_name=args.free_secret or default_free_secret_name(channel_id),
        paid_webhook_secret_name=args.paid_secret or default_paid_secret_name(channel_id),
        admin_webhook_secret_name=args.admin_secret,
        sources=_csv_values(args.sources),
        signal_types=_csv_values(args.signal_types),
        schedule=args.schedule,
        max_items_per_push=args.max_items,
        min_score=args.min_score,
        dedupe_enabled=args.dedupe_enabled,
        content_tags=_csv_values(args.content_tags),
    )
    path = write_channel_file(channel)
    console.print(f"[green]已创建频道配置：{path}[/green]")
    console.print("[yellow]默认不会自动启用；启用前请配置 GitHub Secrets 并运行 check。[/yellow]")
    console.print("需要新增 GitHub Secrets：")
    console.print(f"- {channel.free_webhook_secret_name}")
    console.print(f"- {channel.paid_webhook_secret_name}（可选，会员群启用时再填）")
    console.print(f"- {channel.admin_webhook_secret_name}")


if __name__ == "__main__":
    main()
