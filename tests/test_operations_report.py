import json
from datetime import datetime, timezone

from src.services.operations_report import (
    _fetch_supabase_feedback,
    build_operations_report,
    generate_operations_report,
)


def _manifest() -> dict:
    return {
        "schema_version": 1,
        "run_date": "2026-07-22",
        "language": "zh",
        "generated_at": "2026-07-22T00:45:30+00:00",
        "status": "drafted",
        "fetched_count": 12,
        "unique_count": 10,
        "analyzed_count": 10,
        "selected_count": 5,
        "score_threshold": 6.0,
        "fetched_source_counts": {
            "reddit_promptengineering": 8,
            "hackernews": 4,
        },
        "source_counts": {"reddit_promptengineering": 5},
        "signal_counts": {"TUTORIAL": 4, "PRODUCTIVITY_TIP": 1},
        "group_counts": {"community": 5},
        "cards": [
            {
                "card_id": "reddit:one",
                "title": "提示词工程实操",
            }
        ],
    }


def test_operations_report_surfaces_source_and_delivery_health() -> None:
    report = build_operations_report(
        _manifest(),
        deliveries=[
            {
                "channel_id": "review",
                "channel_name": "信先行·内容审核群",
                "destination_type": "free",
                "item_count": 5,
                "status": "success",
                "delivered_at": "2026-07-22T00:00:00+00:00",
            },
            {
                "channel_id": "ai_tools",
                "channel_name": "信先行·AI工具日报",
                "destination_type": "free",
                "item_count": 5,
                "status": "failed",
                "error": "POST https://example.test/secret failed",
                "delivered_at": "2026-07-22T00:01:00+00:00",
            },
        ],
        feedback_rows=[
            {"card_id": "reddit:one", "button_type": "useful"},
            {"card_id": "reddit:one", "button_type": "favorite"},
            {"card_id": "reddit:other", "button_type": "ignore"},
        ],
        feedback_days=7,
    )

    assert report["source_health"]["top_selected_source_id"] == "reddit_promptengineering"
    assert report["source_health"]["top_selected_source_share"] == 1.0
    assert any("过度集中" in warning for warning in report["warnings"])
    assert report["deliveries"]["status_counts"] == {"failed": 1, "success": 1}
    assert report["deliveries"]["items"][1]["error"] == "POST [redacted URL] failed"
    assert report["feedback"]["totals"] == {
        "useful": 1,
        "favorite": 1,
        "ignore": 1,
    }
    assert report["feedback"]["top_cards"][0]["title"] == "提示词工程实操"


def test_generate_operations_report_writes_report_without_supabase(tmp_path) -> None:
    runs_dir = tmp_path / "data" / "runs"
    runs_dir.mkdir(parents=True)
    (runs_dir / "xinxianxing-2026-07-22-zh.json").write_text(
        json.dumps(_manifest()),
        encoding="utf-8",
    )

    def unavailable_feedback(_, __):
        return [], "Supabase is not configured"

    output_dir = tmp_path / "reports"
    path = generate_operations_report(
        date="2026-07-22",
        data_dir=tmp_path / "data",
        output_dir=output_dir,
        feedback_fetcher=unavailable_feedback,
        now=datetime(2026, 7, 22, tzinfo=timezone.utc),
    )
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert path == output_dir / "xinxianxing-2026-07-22-zh-operations.json"
    assert payload["feedback"]["available"] is False
    assert payload["feedback"]["note"] == "Supabase is not configured"
    assert payload["deliveries"]["items"] == []


def test_feedback_fetch_is_optional_when_server_credentials_are_missing(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)

    rows, warning = _fetch_supabase_feedback(
        tmp_path / "data",
        datetime(2026, 7, 22, tzinfo=timezone.utc),
    )

    assert rows == []
    assert "未配置" in (warning or "")
