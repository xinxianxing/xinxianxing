"""Operational state for daily runs and channel delivery.

The pipeline remains file-first: every generated run has a JSON manifest in
``data/runs`` and channel delivery state has a local SQLite fallback.  When
``SUPABASE_URL`` and ``SUPABASE_SERVICE_ROLE_KEY`` are configured, the same
state is mirrored to Supabase through its PostgREST API.

No webhook or AI credentials are stored here.  Supabase is observability and
delivery state only; it must never become a source of secrets.
"""

from __future__ import annotations

import json
import os
import sqlite3
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

import httpx

from ..models import ContentItem


SUPABASE_URL_ENV = "SUPABASE_URL"
SUPABASE_SERVICE_ROLE_KEY_ENV = "SUPABASE_SERVICE_ROLE_KEY"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _item_source_id(item: ContentItem) -> str:
    return str(item.metadata.get("source_id") or item.source_type.value)


def _item_score(item: ContentItem) -> float | None:
    for value in (item.utility_score, item.score, item.ai_score):
        if value is None:
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return None


def card_snapshot(item: ContentItem) -> dict[str, Any]:
    """Return the compact, structured Action Card representation for a run."""
    return {
        "card_id": item.id,
        "source_type": item.source_type.value,
        "source_id": _item_source_id(item),
        "title": str(item.metadata.get("title_zh") or item.title),
        "source_url": str(item.url),
        "signal_type": item.signal_type.value if item.signal_type else None,
        "score": _item_score(item),
        "intro": item.intro or item.ai_summary,
        "how_to": list(item.how_to),
        "suitable_for": list(item.suitable_for or item.ai_tags),
        "evidence": item.evidence,
        "credibility_risk": item.credibility_risk or item.risk,
        "content_tags": list(item.metadata.get("content_tags") or []),
        "published_at": item.published_at.isoformat(),
    }


def build_run_manifest(
    *,
    run_date: str,
    language: str,
    fetched_count: int,
    unique_count: int,
    analyzed_count: int,
    score_threshold: float,
    selected_items: Iterable[ContentItem],
    group_counts: Mapping[str, int] | None = None,
) -> dict[str, Any]:
    """Build a versioned, renderer-independent manifest for one daily run."""
    cards = [card_snapshot(item) for item in selected_items]
    source_counts = Counter(card["source_id"] for card in cards)
    signal_counts = Counter(
        card["signal_type"] for card in cards if card.get("signal_type")
    )
    return {
        "schema_version": 1,
        "run_date": run_date,
        "language": language,
        "generated_at": _utc_now(),
        "status": "drafted",
        "fetched_count": fetched_count,
        "unique_count": unique_count,
        "analyzed_count": analyzed_count,
        "selected_count": len(cards),
        "score_threshold": score_threshold,
        "source_counts": dict(sorted(source_counts.items())),
        "signal_counts": dict(sorted(signal_counts.items())),
        "group_counts": dict(sorted((group_counts or {}).items())),
        "cards": cards,
    }


@dataclass(frozen=True)
class DeliveryKey:
    """Unique daily destination used for idempotent channel delivery."""

    run_date: str
    language: str
    channel_id: str
    destination_type: str


class OperationsLedger:
    """Persist run manifests and per-channel delivery state.

    SQLite is always updated first so an unavailable Supabase project never
    prevents a daily push.  Supabase mirrors the state when configured.
    """

    def __init__(
        self,
        data_dir: str | Path = "data",
        *,
        env: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.sqlite_path = self.data_dir / "operations.sqlite3"
        self.env = env if env is not None else os.environ
        self.supabase_url = str(self.env.get(SUPABASE_URL_ENV, "")).rstrip("/")
        self.supabase_key = str(
            self.env.get(SUPABASE_SERVICE_ROLE_KEY_ENV, "")
        ).strip()
        self.timeout = timeout
        self._warning: str | None = None
        self._supabase_disabled = False
        self._init_sqlite()

    @property
    def supabase_enabled(self) -> bool:
        return bool(
            self.supabase_url and self.supabase_key and not self._supabase_disabled
        )

    def take_warning(self) -> str | None:
        """Return one non-fatal remote-sync warning, if there was one."""
        warning, self._warning = self._warning, None
        return warning

    def record_run(self, manifest: Mapping[str, Any]) -> None:
        """Upsert one run locally and mirror it to Supabase when available."""
        payload = dict(manifest)
        run_date = str(payload["run_date"])
        language = str(payload["language"])
        with self._sqlite_connection() as conn:
            conn.execute(
                """
                INSERT INTO pipeline_runs (
                    run_date, language, generated_at, status, fetched_count,
                    unique_count, analyzed_count, selected_count, manifest_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(run_date, language) DO UPDATE SET
                    generated_at=excluded.generated_at,
                    status=excluded.status,
                    fetched_count=excluded.fetched_count,
                    unique_count=excluded.unique_count,
                    analyzed_count=excluded.analyzed_count,
                    selected_count=excluded.selected_count,
                    manifest_json=excluded.manifest_json
                """,
                (
                    run_date,
                    language,
                    str(payload.get("generated_at") or _utc_now()),
                    str(payload.get("status") or "drafted"),
                    int(payload.get("fetched_count") or 0),
                    int(payload.get("unique_count") or 0),
                    int(payload.get("analyzed_count") or 0),
                    int(payload.get("selected_count") or 0),
                    json.dumps(payload, ensure_ascii=False, default=str),
                ),
            )

        if not self.supabase_enabled:
            return
        try:
            self._supabase_upsert("pipeline_runs", payload, "run_date,language")
            card_rows = [
                {
                    "run_date": run_date,
                    "language": language,
                    "card_id": card["card_id"],
                    "signal_type": card.get("signal_type"),
                    "score": card.get("score"),
                    "source_id": card.get("source_id"),
                    "card": card,
                }
                for card in payload.get("cards", [])
            ]
            if card_rows:
                self._supabase_upsert(
                    "action_cards",
                    card_rows,
                    "run_date,language,card_id",
                )
        except (httpx.HTTPError, ValueError) as exc:
            self._disable_supabase(f"Supabase 运行台账同步失败，已保留本地记录：{exc}")

    def already_delivered(self, key: DeliveryKey) -> bool:
        """Return true only for an already successful delivery."""
        local_result = self._sqlite_delivery_succeeded(key)
        file_result = self._file_delivery_succeeded(key)
        if not self.supabase_enabled:
            return local_result or file_result
        try:
            response = self._supabase_request(
                "GET",
                "channel_deliveries",
                params={
                    "run_date": f"eq.{key.run_date}",
                    "language": f"eq.{key.language}",
                    "channel_id": f"eq.{key.channel_id}",
                    "destination_type": f"eq.{key.destination_type}",
                    "status": "eq.success",
                    "select": "channel_id",
                    "limit": "1",
                },
            )
            remote_result = bool(response.json())
            return local_result or file_result or remote_result
        except (httpx.HTTPError, ValueError) as exc:
            self._disable_supabase(f"Supabase 投递查询失败，已改用本地台账：{exc}")
            return local_result or file_result

    def record_delivery(
        self,
        key: DeliveryKey,
        *,
        channel_name: str,
        item_count: int,
        status: str,
        error: str | None = None,
    ) -> None:
        """Record a delivery attempt without exposing the webhook URL."""
        delivered_at = _utc_now()
        row = {
            "run_date": key.run_date,
            "language": key.language,
            "channel_id": key.channel_id,
            "destination_type": key.destination_type,
            "channel_name": channel_name,
            "item_count": item_count,
            "status": status,
            "error": error,
            "delivered_at": delivered_at,
        }
        self.sync_delivery_row(row)

    def sync_delivery_row(self, row: Mapping[str, Any]) -> None:
        """Upsert one existing delivery row locally and to Supabase.

        This is used by operations sync jobs that mirror already-recorded
        delivery state without resending a webhook or changing the timestamp.
        """
        normalized = {
            "run_date": str(row["run_date"]),
            "language": str(row["language"]),
            "channel_id": str(row["channel_id"]),
            "destination_type": str(row["destination_type"]),
            "channel_name": str(row["channel_name"]),
            "item_count": int(row["item_count"]),
            "status": str(row["status"]),
            "error": row.get("error"),
            "delivered_at": str(row["delivered_at"]),
        }
        with self._sqlite_connection() as conn:
            conn.execute(
                """
                INSERT INTO channel_deliveries (
                    run_date, language, channel_id, destination_type, channel_name,
                    item_count, status, error, delivered_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(run_date, language, channel_id, destination_type)
                DO UPDATE SET
                    channel_name=excluded.channel_name,
                    item_count=excluded.item_count,
                    status=excluded.status,
                    error=excluded.error,
                    delivered_at=excluded.delivered_at
                """,
                (
                    normalized["run_date"],
                    normalized["language"],
                    normalized["channel_id"],
                    normalized["destination_type"],
                    normalized["channel_name"],
                    normalized["item_count"],
                    normalized["status"],
                    normalized["error"],
                    normalized["delivered_at"],
                ),
            )
        self._write_delivery_state_file(normalized)

        if not self.supabase_enabled:
            return
        try:
            self._supabase_upsert(
                "channel_deliveries",
                normalized,
                "run_date,language,channel_id,destination_type",
            )
        except (httpx.HTTPError, ValueError) as exc:
            self._disable_supabase(f"Supabase 投递台账同步失败，已保留本地记录：{exc}")

    def _init_sqlite(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with self._sqlite_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS pipeline_runs (
                    run_date TEXT NOT NULL,
                    language TEXT NOT NULL,
                    generated_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    fetched_count INTEGER NOT NULL,
                    unique_count INTEGER NOT NULL,
                    analyzed_count INTEGER NOT NULL,
                    selected_count INTEGER NOT NULL,
                    manifest_json TEXT NOT NULL,
                    PRIMARY KEY (run_date, language)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS channel_deliveries (
                    run_date TEXT NOT NULL,
                    language TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    destination_type TEXT NOT NULL,
                    channel_name TEXT NOT NULL,
                    item_count INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    error TEXT,
                    delivered_at TEXT NOT NULL,
                    PRIMARY KEY (run_date, language, channel_id, destination_type)
                )
                """
            )

    def _sqlite_delivery_succeeded(self, key: DeliveryKey) -> bool:
        with self._sqlite_connection() as conn:
            row = conn.execute(
                """
                SELECT status FROM channel_deliveries
                WHERE run_date=? AND language=? AND channel_id=?
                AND destination_type=?
                """,
                (
                    key.run_date,
                    key.language,
                    key.channel_id,
                    key.destination_type,
                ),
            ).fetchone()
        return bool(row and row[0] == "success")

    @contextmanager
    def _sqlite_connection(self):
        """Yield one committed SQLite connection and always close it."""
        conn = sqlite3.connect(self.sqlite_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _delivery_state_path(self, key: DeliveryKey) -> Path:
        return (
            self.data_dir
            / "runs"
            / f"xinxianxing-{key.run_date}-{key.language}-deliveries.json"
        )

    @staticmethod
    def _delivery_state_id(key: DeliveryKey) -> str:
        return f"{key.channel_id}:{key.destination_type}"

    def _file_delivery_succeeded(self, key: DeliveryKey) -> bool:
        path = self._delivery_state_path(key)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return False
        delivery = (payload.get("deliveries") or {}).get(self._delivery_state_id(key))
        return bool(isinstance(delivery, dict) and delivery.get("status") == "success")

    def _write_delivery_state_file(self, row: Mapping[str, Any]) -> None:
        key = DeliveryKey(
            run_date=str(row["run_date"]),
            language=str(row["language"]),
            channel_id=str(row["channel_id"]),
            destination_type=str(row["destination_type"]),
        )
        path = self._delivery_state_path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {
                "schema_version": 1,
                "run_date": key.run_date,
                "language": key.language,
                "deliveries": {},
            }
        deliveries = payload.setdefault("deliveries", {})
        deliveries[self._delivery_state_id(key)] = dict(row)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _supabase_upsert(
        self,
        table: str,
        payload: dict[str, Any] | list[dict[str, Any]],
        conflict_target: str,
    ) -> None:
        self._supabase_request(
            "POST",
            table,
            params={"on_conflict": conflict_target},
            json_payload=payload,
            extra_headers={"Prefer": "resolution=merge-duplicates,return=minimal"},
        )

    def _supabase_request(
        self,
        method: str,
        table: str,
        *,
        params: Mapping[str, str] | None = None,
        json_payload: Any | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> httpx.Response:
        if not self.supabase_enabled:
            raise ValueError("Supabase is not configured")
        headers = self._supabase_headers()
        headers.update(extra_headers or {})
        with httpx.Client(timeout=self.timeout) as client:
            response = client.request(
                method,
                f"{self.supabase_url}/rest/v1/{table}",
                params=params,
                json=json_payload,
                headers=headers,
            )
        response.raise_for_status()
        return response

    def _supabase_headers(self) -> dict[str, str]:
        """Build headers for both new secret keys and legacy service-role JWTs."""
        headers = {
            "apikey": self.supabase_key,
            "Content-Type": "application/json",
        }
        # New sb_secret keys are API keys, not JWTs. Supabase rejects them in
        # Authorization headers; legacy service_role JWTs still require it.
        if not self.supabase_key.startswith("sb_secret_"):
            headers["Authorization"] = f"Bearer {self.supabase_key}"
        return headers

    def _disable_supabase(self, message: str) -> None:
        self._supabase_disabled = True
        self._warning = message
