"""Alert administrators when a configured content column stays empty.

This service reads existing daily run manifests only. It never generates
content, sends messages to subscriber channels, or treats an empty category as
an error for the rest of the pipeline.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from dataclasses import dataclass
from datetime import date as date_type
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from rich.console import Console

from ..models import SignalType
from ..storage.manager import StorageManager
from .webhook import send_admin_notice


console = Console()

SIGNAL_LABELS = {
    SignalType.TUTORIAL: "教程技巧",
    SignalType.MONEY_CASE: "AI变现",
    SignalType.PRODUCTIVITY_TIP: "效率技巧",
}


@dataclass(frozen=True)
class MissingSignalStreak:
    """One category absent from each manifest in a consecutive-day window."""

    signal_type: SignalType
    dates: tuple[date_type, ...]

    @property
    def key(self) -> str:
        return f"{self.signal_type.value}:{self.dates[0].isoformat()}"


def _default_date() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")


def _manifest_path(base: Path, run_date: date_type, language: str) -> Path:
    return base / "runs" / f"xinxianxing-{run_date.isoformat()}-{language}.json"


def _state_path(base: Path, language: str) -> Path:
    return base / "runs" / f"xinxianxing-content-health-{language}-state.json"


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _signal_count(manifest: Mapping[str, Any], signal_type: SignalType) -> int:
    signal_counts = manifest.get("signal_counts")
    if not isinstance(signal_counts, Mapping):
        return 0
    try:
        return int(signal_counts.get(signal_type.value) or 0)
    except (TypeError, ValueError):
        return 0


def _missing_dates_for_signal(
    *,
    base: Path,
    end_date: date_type,
    language: str,
    signal_type: SignalType,
) -> tuple[date_type, ...]:
    """Return the current uninterrupted absence for one signal type."""
    dates: list[date_type] = []
    current_date = end_date
    while True:
        manifest = _read_json(_manifest_path(base, current_date, language))
        if manifest is None or _signal_count(manifest, signal_type) > 0:
            break
        dates.append(current_date)
        current_date = date_type.fromordinal(current_date.toordinal() - 1)
    return tuple(reversed(dates))


def find_missing_signal_streaks(
    *,
    data_dir: str | Path,
    run_date: str,
    language: str,
    signal_types: Iterable[SignalType],
    consecutive_days: int,
) -> list[MissingSignalStreak]:
    """Find current gaps that have reached the configured alert threshold.

    A missing manifest is deliberately not treated as empty content. The
    health check waits for a complete series so scraper or workflow failures do
    not become a misleading editorial alert.
    """
    if consecutive_days < 2:
        raise ValueError("consecutive_days 必须至少为 2")
    try:
        end_date = date_type.fromisoformat(run_date)
    except ValueError as exc:
        raise ValueError("run_date 必须使用 YYYY-MM-DD") from exc

    base = Path(data_dir)
    streaks: list[MissingSignalStreak] = []
    for signal_type in signal_types:
        dates = _missing_dates_for_signal(
            base=base,
            end_date=end_date,
            language=language,
            signal_type=signal_type,
        )
        if len(dates) < consecutive_days:
            continue
        streaks.append(MissingSignalStreak(signal_type=signal_type, dates=dates))
    return streaks


def _load_alert_state(path: Path) -> dict[str, Any]:
    state = _read_json(path)
    if state is None:
        return {"schema_version": 1, "alerts": []}
    alerts = state.get("alerts")
    if not isinstance(alerts, list):
        state["alerts"] = []
    return state


def _sent_alert_keys(state: Mapping[str, Any]) -> set[str]:
    alerts = state.get("alerts")
    if not isinstance(alerts, list):
        return set()
    return {
        str(alert.get("key"))
        for alert in alerts
        if isinstance(alert, Mapping) and alert.get("key")
    }


def _write_alert_state(
    path: Path,
    *,
    run_date: str,
    language: str,
    state: Mapping[str, Any],
) -> None:
    payload = dict(state)
    payload["last_checked_date"] = run_date
    payload["language"] = language
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


async def alert_missing_signal_streaks(
    *,
    data_dir: str | Path,
    run_date: str,
    language: str,
    signal_types: Iterable[SignalType],
    consecutive_days: int,
    admin_webhook_url: str | None,
) -> list[MissingSignalStreak]:
    """Notify the admin webhook once per newly completed missing-content streak."""
    streaks = find_missing_signal_streaks(
        data_dir=data_dir,
        run_date=run_date,
        language=language,
        signal_types=signal_types,
        consecutive_days=consecutive_days,
    )
    if not streaks:
        return []

    base = Path(data_dir)
    state_path = _state_path(base, language)
    state = _load_alert_state(state_path)
    sent_keys = _sent_alert_keys(state)
    sent: list[MissingSignalStreak] = []
    alerts = state["alerts"]

    for streak in streaks:
        if streak.key in sent_keys:
            continue
        label = SIGNAL_LABELS.get(streak.signal_type, streak.signal_type.value)
        if len(streak.dates) <= 3:
            dates = "、".join(current.isoformat() for current in streak.dates)
        else:
            dates = (
                f"{streak.dates[0].isoformat()} 至 {streak.dates[-1].isoformat()}"
                f"（{len(streak.dates)} 天）"
            )
        delivered = await send_admin_notice(
            admin_webhook_url,
            title="信先行栏目连续缺内容",
            template="orange",
            lines=[
                f"**栏目**: {label} (`{streak.signal_type.value}`)",
                f"**连续无入选内容**: {dates}",
                "**用户群处理**: 未发送“今日无内容”消息。",
                "**建议**: 检查对应信源、评分门槛与内容供给。",
            ],
        )
        if not delivered:
            console.print(
                f"[yellow]管理员告警未发送：{label}（请检查 XINXIANXING_ADMIN_WEBHOOK）[/yellow]"
            )
            continue
        alerts.append(
            {
                "key": streak.key,
                "signal_type": streak.signal_type.value,
                "dates": [current.isoformat() for current in streak.dates],
                "sent_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        sent.append(streak)

    if sent:
        _write_alert_state(
            state_path,
            run_date=run_date,
            language=language,
            state=state,
        )
    return sent


async def run_content_health_check(
    *,
    data_dir: str | Path,
    run_date: str,
    language: str = "zh",
    admin_webhook_url: str | None = None,
) -> list[MissingSignalStreak]:
    """Load configured editorial health rules and send admin-only notices."""
    config = StorageManager(data_dir=str(data_dir)).load_config()
    settings = config.filtering.missing_signal_alert
    if settings is None:
        console.print("[dim]未配置 missing_signal_alert，跳过栏目健康检查。[/dim]")
        return []
    return await alert_missing_signal_streaks(
        data_dir=data_dir,
        run_date=run_date,
        language=language,
        signal_types=settings.signal_types,
        consecutive_days=settings.consecutive_days,
        admin_webhook_url=admin_webhook_url,
    )


def main() -> None:
    """CLI entry point for the admin-only content health check."""
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Alert the admin when configured 信先行 columns stay empty",
    )
    parser.add_argument("--date", default=_default_date(), help="Run date, YYYY-MM-DD")
    parser.add_argument("--language", default="zh", help="Run language, default zh")
    parser.add_argument("--data-dir", default="data", help="Data directory, default data")
    args = parser.parse_args()

    sent = asyncio.run(
        run_content_health_check(
            data_dir=args.data_dir,
            run_date=args.date,
            language=args.language,
            admin_webhook_url=os.getenv("XINXIANXING_ADMIN_WEBHOOK"),
        )
    )
    if sent:
        labels = ", ".join(
            SIGNAL_LABELS.get(streak.signal_type, streak.signal_type.value)
            for streak in sent
        )
        console.print(f"[yellow]已发送栏目健康告警：{labels}[/yellow]")
    else:
        console.print("[green]栏目健康检查完成，无新增管理员告警。[/green]")


if __name__ == "__main__":
    main()
