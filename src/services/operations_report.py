"""Build file-first health reports for daily 信先行 operations.

The report deliberately reads existing manifests and delivery ledgers instead
of touching the generation pipeline. Supabase feedback is optional: a missing
or temporarily unavailable project is reported as a non-fatal data gap.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from rich.console import Console

from .operations import OperationsLedger


console = Console()
FeedbackFetcher = Callable[[Path, datetime], tuple[list[dict[str, Any]], str | None]]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _default_date() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"找不到运行台账：{path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"运行台账 JSON 格式错误：{path}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"运行台账必须是 JSON 对象：{path}")
    return payload


def _count_map(value: object) -> dict[str, int]:
    if not isinstance(value, Mapping):
        return {}
    counts: dict[str, int] = {}
    for raw_key, raw_count in value.items():
        key = str(raw_key).strip()
        if not key:
            continue
        try:
            count = int(raw_count)
        except (TypeError, ValueError):
            continue
        if count > 0:
            counts[key] = count
    return dict(sorted(counts.items()))


def _delivery_rows(payload: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    deliveries = (payload or {}).get("deliveries")
    if not isinstance(deliveries, Mapping):
        return []
    rows = [dict(row) for row in deliveries.values() if isinstance(row, Mapping)]
    return sorted(
        rows,
        key=lambda row: (
            str(row.get("channel_id") or ""),
            str(row.get("destination_type") or ""),
        ),
    )


def _safe_error(value: object) -> str | None:
    """Keep report logs useful without copying webhook URLs into Git files."""
    if not value:
        return None
    text = str(value)
    for prefix in ("https://", "http://"):
        start = text.find(prefix)
        while start >= 0:
            end = start
            while end < len(text) and not text[end].isspace():
                end += 1
            text = f"{text[:start]}[redacted URL]{text[end:]}"
            start = text.find(prefix)
    return text[:300]


def _source_health(
    *,
    fetched_count: int,
    selected_count: int,
    fetched_source_counts: Mapping[str, int],
    selected_source_counts: Mapping[str, int],
) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    selected_counts = dict(selected_source_counts)
    fetched_counts = dict(fetched_source_counts)
    top_source_id: str | None = None
    top_source_share = 0.0

    if selected_count <= 0:
        warnings.append("本次没有选出可发布的 Action Card。")
    elif not selected_counts:
        warnings.append("入选卡片缺少信源标识，无法判断内容来源分布。")
    else:
        top_source_id, top_count = max(
            selected_counts.items(), key=lambda item: (item[1], item[0])
        )
        top_source_share = round(top_count / selected_count, 4)
        if selected_count >= 3 and top_source_share >= 0.8:
            warnings.append(
                f"入选内容过度集中于 {top_source_id}（{top_source_share:.0%}）；"
                "请检查其他信源是否失效或当天内容是否不足。"
            )

    if fetched_count > 0 and not fetched_counts:
        warnings.append("本次运行缺少原始抓取的分信源统计；下次生成会自动补齐。")

    return (
        {
            "fetched_source_counts": fetched_counts,
            "selected_source_counts": selected_counts,
            "top_selected_source_id": top_source_id,
            "top_selected_source_share": top_source_share,
        },
        warnings,
    )


def _feedback_summary(
    feedback_rows: Iterable[Mapping[str, Any]],
    cards: Iterable[Mapping[str, Any]],
    *,
    days: int,
    warning: str | None,
) -> dict[str, Any]:
    totals = Counter({"useful": 0, "favorite": 0, "ignore": 0})
    by_card: dict[str, Counter[str]] = defaultdict(Counter)
    titles = {
        str(card.get("card_id")): str(card.get("title") or "")
        for card in cards
        if card.get("card_id")
    }

    for row in feedback_rows:
        card_id = str(row.get("card_id") or "").strip()
        button_type = str(row.get("button_type") or "").strip()
        if not card_id or button_type not in totals:
            continue
        totals[button_type] += 1
        by_card[card_id][button_type] += 1

    top_cards = []
    for card_id, counts in sorted(
        by_card.items(),
        key=lambda item: (
            -(item[1]["useful"] + item[1]["favorite"]),
            -sum(item[1].values()),
            item[0],
        ),
    )[:10]:
        top_cards.append(
            {
                "card_id": card_id,
                "title": titles.get(card_id) or None,
                "useful": counts["useful"],
                "favorite": counts["favorite"],
                "ignore": counts["ignore"],
            }
        )

    return {
        "available": warning is None,
        "period_days": days,
        "totals": dict(totals),
        "top_cards": top_cards,
        "note": warning,
    }


def build_operations_report(
    manifest: Mapping[str, Any],
    *,
    deliveries: Iterable[Mapping[str, Any]] = (),
    feedback_rows: Iterable[Mapping[str, Any]] = (),
    feedback_days: int = 7,
    feedback_warning: str | None = None,
) -> dict[str, Any]:
    """Return a serializable daily report from already-recorded operations data."""
    fetched_count = int(manifest.get("fetched_count") or 0)
    unique_count = int(manifest.get("unique_count") or 0)
    analyzed_count = int(manifest.get("analyzed_count") or 0)
    selected_count = int(manifest.get("selected_count") or 0)
    cards = [card for card in manifest.get("cards", []) if isinstance(card, Mapping)]
    source_health, warnings = _source_health(
        fetched_count=fetched_count,
        selected_count=selected_count,
        fetched_source_counts=_count_map(manifest.get("fetched_source_counts")),
        selected_source_counts=_count_map(manifest.get("source_counts")),
    )

    delivery_rows = [dict(row) for row in deliveries]
    delivery_statuses = Counter(
        str(row.get("status") or "unknown") for row in delivery_rows
    )
    delivery_details = []
    for row in delivery_rows:
        status = str(row.get("status") or "unknown")
        error = _safe_error(row.get("error"))
        delivery_details.append(
            {
                "channel_id": str(row.get("channel_id") or ""),
                "channel_name": str(row.get("channel_name") or ""),
                "destination_type": str(row.get("destination_type") or ""),
                "item_count": int(row.get("item_count") or 0),
                "status": status,
                "delivered_at": row.get("delivered_at"),
                "error": error,
            }
        )
        if status == "failed":
            label = str(row.get("channel_name") or row.get("channel_id") or "未知频道")
            warnings.append(f"频道投递失败：{label}。{error or '未提供失败原因'}")

    return {
        "schema_version": 1,
        "run_date": str(manifest.get("run_date") or ""),
        "language": str(manifest.get("language") or "zh"),
        "generated_at": _utc_now().isoformat(),
        "run": {
            "status": str(manifest.get("status") or "unknown"),
            "fetched_count": fetched_count,
            "unique_count": unique_count,
            "analyzed_count": analyzed_count,
            "selected_count": selected_count,
            "score_threshold": manifest.get("score_threshold"),
        },
        "source_health": source_health,
        "signal_distribution": _count_map(manifest.get("signal_counts")),
        "group_distribution": _count_map(manifest.get("group_counts")),
        "deliveries": {
            "status_counts": dict(sorted(delivery_statuses.items())),
            "items": delivery_details,
        },
        "feedback": _feedback_summary(
            feedback_rows,
            cards,
            days=feedback_days,
            warning=feedback_warning,
        ),
        "warnings": warnings,
    }


def _fetch_supabase_feedback(
    data_dir: Path,
    since: datetime,
) -> tuple[list[dict[str, Any]], str | None]:
    ledger = OperationsLedger(data_dir)
    if not ledger.supabase_enabled:
        return [], "未配置 SUPABASE_URL 或 SUPABASE_SERVICE_ROLE_KEY，未读取网站反馈。"
    try:
        response = ledger._supabase_request(
            "GET",
            "card_feedback",
            params={
                "select": "card_id,button_type,clicked_at",
                "clicked_at": f"gte.{since.isoformat()}",
                "order": "clicked_at.desc",
                "limit": "1000",
            },
        )
        payload = response.json()
    except Exception as exc:  # The report must not disrupt daily operations.
        return [], f"读取 Supabase 反馈失败：{exc}"
    if not isinstance(payload, list):
        return [], "Supabase 反馈接口返回了非列表数据。"
    return [dict(row) for row in payload if isinstance(row, Mapping)], None


def generate_operations_report(
    *,
    date: str,
    language: str = "zh",
    data_dir: str | Path = "data",
    output_dir: str | Path | None = None,
    feedback_days: int = 7,
    feedback_fetcher: FeedbackFetcher = _fetch_supabase_feedback,
    now: datetime | None = None,
) -> Path:
    """Read one run and write its operations health report to disk."""
    if feedback_days <= 0:
        raise ValueError("feedback_days 必须大于 0")
    base = Path(data_dir)
    manifest = _read_json(base / "runs" / f"xinxianxing-{date}-{language}.json")
    delivery_path = base / "runs" / f"xinxianxing-{date}-{language}-deliveries.json"
    deliveries = _delivery_rows(_read_json(delivery_path)) if delivery_path.exists() else []
    report_now = now or _utc_now()
    feedback_rows, feedback_warning = feedback_fetcher(
        base, report_now - timedelta(days=feedback_days)
    )
    report = build_operations_report(
        manifest,
        deliveries=deliveries,
        feedback_rows=feedback_rows,
        feedback_days=feedback_days,
        feedback_warning=feedback_warning,
    )
    target_dir = Path(output_dir) if output_dir is not None else base / "reports"
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"xinxianxing-{date}-{language}-operations.json"
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def main() -> None:
    """CLI entry point for generating a daily operations report."""
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Generate a file-first 信先行 daily operations report",
    )
    parser.add_argument("--date", default=_default_date(), help="Run date, YYYY-MM-DD")
    parser.add_argument("--language", default="zh", help="Run language, default zh")
    parser.add_argument("--data-dir", default="data", help="Data directory, default data")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Report output directory, default data/reports",
    )
    parser.add_argument(
        "--feedback-days",
        type=int,
        default=7,
        help="Feedback lookback window in days, default 7",
    )
    args = parser.parse_args()

    try:
        path = generate_operations_report(
            date=args.date,
            language=args.language,
            data_dir=args.data_dir,
            output_dir=args.output_dir,
            feedback_days=args.feedback_days,
        )
    except Exception as exc:
        console.print(f"[bold red]运营报告生成失败：{exc}[/bold red]")
        raise SystemExit(1) from exc

    console.print(f"[bold green]运营报告已生成：{path}[/bold green]")


if __name__ == "__main__":
    main()
