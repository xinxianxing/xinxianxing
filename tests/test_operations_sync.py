import json

import pytest

from src.services import operations_sync


def test_sync_operations_requires_supabase_config(tmp_path) -> None:
    runs = tmp_path / "data" / "runs"
    runs.mkdir(parents=True)
    (runs / "xinxianxing-2026-07-21-zh.json").write_text(
        json.dumps(
            {
                "run_date": "2026-07-21",
                "language": "zh",
                "generated_at": "2026-07-21T00:00:00+00:00",
                "status": "drafted",
                "fetched_count": 1,
                "unique_count": 1,
                "analyzed_count": 1,
                "selected_count": 0,
                "score_threshold": 6,
                "source_counts": {},
                "signal_counts": {},
                "group_counts": {},
                "cards": [],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="SUPABASE_URL"):
        operations_sync.sync_operations(
            date="2026-07-21",
            language="zh",
            data_dir=tmp_path / "data",
        )


def test_sync_operations_reads_manifest_and_deliveries(tmp_path, monkeypatch) -> None:
    runs = tmp_path / "data" / "runs"
    runs.mkdir(parents=True)
    manifest = {
        "run_date": "2026-07-21",
        "language": "zh",
        "generated_at": "2026-07-21T00:00:00+00:00",
        "status": "drafted",
        "fetched_count": 3,
        "unique_count": 2,
        "analyzed_count": 2,
        "selected_count": 1,
        "score_threshold": 6,
        "source_counts": {},
        "signal_counts": {},
        "group_counts": {},
        "cards": [],
    }
    deliveries = {
        "schema_version": 1,
        "run_date": "2026-07-21",
        "language": "zh",
        "deliveries": {
            "review:free": {
                "run_date": "2026-07-21",
                "language": "zh",
                "channel_id": "review",
                "destination_type": "free",
                "channel_name": "信先行·内容审核群",
                "item_count": 1,
                "status": "success",
                "error": None,
                "delivered_at": "2026-07-21T22:48:03.017210+00:00",
            }
        },
    }
    (runs / "xinxianxing-2026-07-21-zh.json").write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )
    (runs / "xinxianxing-2026-07-21-zh-deliveries.json").write_text(
        json.dumps(deliveries),
        encoding="utf-8",
    )

    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "sb_secret_example")
    upserts = []
    monkeypatch.setattr(
        operations_sync.OperationsLedger,
        "_supabase_upsert",
        lambda self, table, payload, conflict_target: upserts.append(table),
    )

    assert operations_sync.sync_operations(
        date="2026-07-21",
        language="zh",
        data_dir=tmp_path / "data",
    ) == (1, 1)
    assert upserts == ["pipeline_runs", "channel_deliveries"]
