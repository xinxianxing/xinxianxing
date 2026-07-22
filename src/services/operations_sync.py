"""Sync existing run manifests and delivery state to Supabase."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from rich.console import Console

from .operations import OperationsLedger


console = Console()


def _default_date() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"找不到台账文件：{path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"台账 JSON 格式错误：{path}") from exc


def sync_operations(
    *,
    date: str,
    language: str = "zh",
    data_dir: str | Path = "data",
    include_deliveries: bool = True,
) -> tuple[int, int]:
    """Mirror one existing daily run and optional deliveries to Supabase."""
    base = Path(data_dir)
    ledger = OperationsLedger(base)
    if not ledger.supabase_enabled:
        raise RuntimeError("需要配置 SUPABASE_URL 和 SUPABASE_SERVICE_ROLE_KEY")

    run_path = base / "runs" / f"xinxianxing-{date}-{language}.json"
    manifest = _read_json(run_path)
    ledger.record_run(manifest)
    if warning := ledger.take_warning():
        raise RuntimeError(warning)

    delivery_count = 0
    if include_deliveries:
        delivery_path = base / "runs" / f"xinxianxing-{date}-{language}-deliveries.json"
        if delivery_path.exists():
            payload = _read_json(delivery_path)
            for delivery in (payload.get("deliveries") or {}).values():
                if isinstance(delivery, dict):
                    ledger.sync_delivery_row(delivery)
                    delivery_count += 1
                    if warning := ledger.take_warning():
                        raise RuntimeError(warning)

    return int(manifest.get("selected_count") or 0), delivery_count


def main() -> None:
    """CLI entry point for Supabase operations sync."""
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Sync an existing 信先行 run manifest to Supabase",
    )
    parser.add_argument("--date", default=_default_date(), help="Run date, YYYY-MM-DD")
    parser.add_argument("--language", default="zh", help="Run language, default zh")
    parser.add_argument("--data-dir", default="data", help="Data directory, default data")
    parser.add_argument(
        "--skip-deliveries",
        action="store_true",
        help="Only sync the run manifest and action cards.",
    )
    args = parser.parse_args()

    try:
        selected_count, delivery_count = sync_operations(
            date=args.date,
            language=args.language,
            data_dir=args.data_dir,
            include_deliveries=not args.skip_deliveries,
        )
    except Exception as exc:
        console.print(f"[bold red]Supabase 台账同步失败：{exc}[/bold red]")
        raise SystemExit(1) from exc

    console.print(
        "[bold green]Supabase 台账同步完成："
        f"{selected_count} 张卡片，{delivery_count} 条投递记录。[/bold green]"
    )


if __name__ == "__main__":
    main()
