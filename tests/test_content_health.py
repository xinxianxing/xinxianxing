import asyncio
import json

from src.models import SignalType
from src.services import content_health


def _write_manifest(tmp_path, run_date: str, signal_counts: dict[str, int]) -> None:
    runs_dir = tmp_path / "data" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_date": run_date,
        "language": "zh",
        "signal_counts": signal_counts,
    }
    (runs_dir / f"xinxianxing-{run_date}-zh.json").write_text(
        json.dumps(payload),
        encoding="utf-8",
    )


def test_missing_signal_streak_requires_three_complete_daily_manifests(tmp_path) -> None:
    for run_date in ("2026-07-20", "2026-07-21", "2026-07-22"):
        _write_manifest(tmp_path, run_date, {"TUTORIAL": 2})

    streaks = content_health.find_missing_signal_streaks(
        data_dir=tmp_path / "data",
        run_date="2026-07-22",
        language="zh",
        signal_types=[SignalType.TUTORIAL, SignalType.MONEY_CASE],
        consecutive_days=3,
    )

    assert [(streak.signal_type, [day.isoformat() for day in streak.dates]) for streak in streaks] == [
        (
            SignalType.MONEY_CASE,
            ["2026-07-20", "2026-07-21", "2026-07-22"],
        )
    ]


def test_missing_signal_streak_includes_an_existing_longer_gap(tmp_path) -> None:
    for run_date in ("2026-07-19", "2026-07-20", "2026-07-21", "2026-07-22"):
        _write_manifest(tmp_path, run_date, {"TUTORIAL": 2})

    streaks = content_health.find_missing_signal_streaks(
        data_dir=tmp_path / "data",
        run_date="2026-07-22",
        language="zh",
        signal_types=[SignalType.MONEY_CASE],
        consecutive_days=3,
    )

    assert [(streak.signal_type, len(streak.dates)) for streak in streaks] == [
        (SignalType.MONEY_CASE, 4)
    ]


def test_missing_signal_alert_is_admin_only_and_idempotent(tmp_path, monkeypatch) -> None:
    for run_date in ("2026-07-20", "2026-07-21", "2026-07-22"):
        _write_manifest(tmp_path, run_date, {"TUTORIAL": 2})

    sent_lines: list[list[str]] = []

    async def fake_notice(_, *, title, lines, template):  # type: ignore[no-untyped-def]
        assert title == "信先行栏目连续缺内容"
        assert template == "orange"
        sent_lines.append(lines)
        return True

    monkeypatch.setattr(content_health, "send_admin_notice", fake_notice)
    kwargs = {
        "data_dir": tmp_path / "data",
        "run_date": "2026-07-22",
        "language": "zh",
        "signal_types": [SignalType.MONEY_CASE],
        "consecutive_days": 3,
        "admin_webhook_url": "https://example.com/admin",
    }

    sent = asyncio.run(content_health.alert_missing_signal_streaks(**kwargs))
    _write_manifest(tmp_path, "2026-07-23", {"TUTORIAL": 2})
    repeated = asyncio.run(
        content_health.alert_missing_signal_streaks(
            **{**kwargs, "run_date": "2026-07-23"}
        )
    )
    state_path = tmp_path / "data" / "runs" / "xinxianxing-content-health-zh-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))

    assert [streak.signal_type for streak in sent] == [SignalType.MONEY_CASE]
    assert repeated == []
    assert len(sent_lines) == 1
    assert "未发送“今日无内容”消息" in sent_lines[0][2]
    assert state["alerts"][0]["signal_type"] == "MONEY_CASE"
