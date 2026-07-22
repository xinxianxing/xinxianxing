from datetime import datetime, timezone
from contextlib import closing
import json
import sqlite3

import httpx

from src.models import ContentItem, SignalType, SourceType
from src.services.operations import (
    DeliveryKey,
    OperationsLedger,
    build_run_manifest,
)


def _item() -> ContentItem:
    return ContentItem(
        id="reddit:subreddit-rss:t3_operations",
        source_type=SourceType.REDDIT,
        title="提示词测试集教程",
        url="https://www.reddit.com/r/PromptEngineering/comments/test/post/",
        content="source body is intentionally omitted from manifests",
        published_at=datetime(2026, 7, 21, tzinfo=timezone.utc),
        metadata={
            "source_id": "reddit_promptengineering",
            "content_tags": ["ai", "tutorial"],
        },
        ai_score=8.0,
        intro="用固定样本验证提示词改动。",
        how_to=["准备样本", "对比输出"],
        suitable_for=["提示词工程师"],
        evidence="未提供具体数据",
        credibility_risk="依赖测试集质量。",
        utility_score=8.0,
        signal_type=SignalType.TUTORIAL,
    )


def test_manifest_is_compact_and_does_not_include_source_body() -> None:
    manifest = build_run_manifest(
        run_date="2026-07-21",
        language="zh",
        fetched_count=20,
        unique_count=18,
        analyzed_count=18,
        score_threshold=6.0,
        selected_items=[_item()],
        fetched_items=[_item()],
        group_counts={"tutorials": 1},
    )

    assert manifest["selected_count"] == 1
    assert manifest["fetched_source_counts"] == {"reddit_promptengineering": 1}
    assert manifest["source_counts"] == {"reddit_promptengineering": 1}
    assert manifest["signal_counts"] == {"TUTORIAL": 1}
    assert manifest["cards"][0]["how_to"] == ["准备样本", "对比输出"]
    assert "content" not in manifest["cards"][0]


def test_operations_ledger_keeps_local_delivery_state(tmp_path) -> None:
    ledger = OperationsLedger(tmp_path / "data", env={})
    manifest = build_run_manifest(
        run_date="2026-07-21",
        language="zh",
        fetched_count=20,
        unique_count=18,
        analyzed_count=18,
        score_threshold=6.0,
        selected_items=[_item()],
    )
    ledger.record_run(manifest)

    key = DeliveryKey("2026-07-21", "zh", "ai_tools", "free")
    assert ledger.already_delivered(key) is False
    ledger.record_delivery(
        key,
        channel_name="信先行·AI工具日报",
        item_count=1,
        status="success",
    )
    assert ledger.already_delivered(key) is True

    with closing(sqlite3.connect(ledger.sqlite_path)) as conn:
        run = conn.execute("SELECT selected_count FROM pipeline_runs").fetchone()
        delivery = conn.execute("SELECT status FROM channel_deliveries").fetchone()
    assert run == (1,)
    assert delivery == ("success",)

    ledger.sqlite_path.unlink()
    assert OperationsLedger(tmp_path / "data", env={}).already_delivered(key) is True


def test_sync_delivery_row_preserves_existing_timestamp(tmp_path, monkeypatch) -> None:
    ledger = OperationsLedger(
        tmp_path / "data",
        env={
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SERVICE_ROLE_KEY": "sb_secret_example",
        },
    )
    calls = []
    monkeypatch.setattr(
        ledger,
        "_supabase_upsert",
        lambda table, payload, conflict_target: calls.append(
            (table, payload, conflict_target)
        ),
    )

    row = {
        "run_date": "2026-07-21",
        "language": "zh",
        "channel_id": "review",
        "destination_type": "free",
        "channel_name": "信先行·内容审核群",
        "item_count": 3,
        "status": "success",
        "error": None,
        "delivered_at": "2026-07-21T22:48:03.017210+00:00",
    }
    ledger.sync_delivery_row(row)

    with closing(sqlite3.connect(ledger.sqlite_path)) as conn:
        stored = conn.execute(
            "SELECT delivered_at FROM channel_deliveries"
        ).fetchone()
    delivery_file = (
        tmp_path / "data" / "runs" / "xinxianxing-2026-07-21-zh-deliveries.json"
    )
    payload = json.loads(delivery_file.read_text(encoding="utf-8"))

    assert stored == ("2026-07-21T22:48:03.017210+00:00",)
    assert payload["deliveries"]["review:free"]["delivered_at"] == row["delivered_at"]
    assert calls == [
        (
            "channel_deliveries",
            row,
            "run_date,language,channel_id,destination_type",
        )
    ]


def test_operations_ledger_falls_back_when_supabase_is_unavailable(
    tmp_path, monkeypatch
) -> None:
    ledger = OperationsLedger(
        tmp_path / "data",
        env={
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SERVICE_ROLE_KEY": "secret",
        },
    )

    def fail(*args, **kwargs):
        raise httpx.ConnectError("network unavailable")

    monkeypatch.setattr(ledger, "_supabase_upsert", fail)
    ledger.record_run(
        build_run_manifest(
            run_date="2026-07-21",
            language="zh",
            fetched_count=1,
            unique_count=1,
            analyzed_count=1,
            score_threshold=6.0,
            selected_items=[_item()],
        )
    )

    assert ledger.supabase_enabled is False
    assert "已保留本地记录" in (ledger.take_warning() or "")
    with closing(sqlite3.connect(ledger.sqlite_path)) as conn:
        assert conn.execute("SELECT COUNT(*) FROM pipeline_runs").fetchone() == (1,)


def test_operations_ledger_sends_only_table_columns_to_supabase(
    tmp_path, monkeypatch
) -> None:
    ledger = OperationsLedger(
        tmp_path / "data",
        env={
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SERVICE_ROLE_KEY": "sb_secret_example",
        },
    )
    calls = []
    monkeypatch.setattr(
        ledger,
        "_supabase_upsert",
        lambda table, payload, conflict_target: calls.append(
            (table, payload, conflict_target)
        ),
    )

    manifest = build_run_manifest(
        run_date="2026-07-21",
        language="zh",
        fetched_count=1,
        unique_count=1,
        analyzed_count=1,
        score_threshold=6.0,
        selected_items=[_item()],
    )
    ledger.record_run(manifest)

    table, run_payload, conflict_target = calls[0]
    assert table == "pipeline_runs"
    assert conflict_target == "run_date,language"
    assert "schema_version" not in run_payload
    assert run_payload["run_date"] == "2026-07-21"
    assert run_payload["cards"] == manifest["cards"]
    assert calls[1][0] == "action_cards"


def test_supabase_headers_support_new_and_legacy_server_keys(tmp_path) -> None:
    new_key_ledger = OperationsLedger(
        tmp_path / "new",
        env={
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SERVICE_ROLE_KEY": "sb_secret_example",
        },
    )
    legacy_key_ledger = OperationsLedger(
        tmp_path / "legacy",
        env={
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SERVICE_ROLE_KEY": "legacy-service-role-jwt",
        },
    )

    assert new_key_ledger._supabase_headers() == {
        "apikey": "sb_secret_example",
        "Content-Type": "application/json",
    }
    assert legacy_key_ledger._supabase_headers()["Authorization"] == (
        "Bearer legacy-service-role-jwt"
    )
