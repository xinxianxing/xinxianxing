"""Local feedback API for Action Card review clicks."""

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ALLOWED_ACTIONS = {"useful", "favorite", "ignore"}


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS card_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id TEXT NOT NULL,
                button_type TEXT NOT NULL,
                clicked_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_card_feedback_card_id "
            "ON card_feedback(card_id)"
        )


def record_feedback(db_path: Path, card_id: str, button_type: str) -> dict[str, str]:
    if not card_id.strip():
        raise ValueError("card_id is required")
    if button_type not in ALLOWED_ACTIONS:
        raise ValueError("button_type must be useful, favorite, or ignore")

    clicked_at = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO card_feedback (card_id, button_type, clicked_at)
            VALUES (?, ?, ?)
            """,
            (card_id, button_type, clicked_at),
        )

    return {
        "card_id": card_id,
        "button_type": button_type,
        "clicked_at": clicked_at,
    }


def make_handler(db_path: Path):
    class FeedbackHandler(BaseHTTPRequestHandler):
        def _send_json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self) -> None:
            self._send_json(200, {"ok": True})

        def do_POST(self) -> None:
            if self.path.rstrip("/") != "/api/feedback":
                self._send_json(404, {"ok": False, "error": "not found"})
                return

            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                result = record_feedback(
                    db_path=db_path,
                    card_id=str(payload.get("card_id", "")),
                    button_type=str(payload.get("button_type", payload.get("action", ""))),
                )
            except Exception as exc:
                self._send_json(400, {"ok": False, "error": str(exc)})
                return

            self._send_json(200, {"ok": True, "feedback": result})

    return FeedbackHandler


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the local Action Card feedback API."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--db", default="data/feedback.sqlite3")
    args = parser.parse_args()

    db_path = Path(args.db)
    init_db(db_path)
    server = ThreadingHTTPServer((args.host, args.port), make_handler(db_path))
    print(
        f"Feedback API running at http://{args.host}:{args.port}/api/feedback "
        f"(db: {db_path})"
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
