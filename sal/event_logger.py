"""Event logger — SQLite-backed, append-only.

DB-first design for durable event tracking across runs.
"""

import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Optional


def _resolve_db_path(db_path: Optional[str] = None) -> Path:
    if db_path:
        return Path(db_path)
    env = os.environ.get("SAL_EVENT_DB_PATH")
    if env:
        return Path(env)
    return Path(".state") / "events.db"


class EventLogger:
    """SQLite-backed event logger.

    Table schema:
        events(id, ts, event, payload)
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        resolved = _resolve_db_path(db_path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = resolved
        self.conn = sqlite3.connect(str(resolved))
        self._init_tables()

    def _init_tables(self) -> None:
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts REAL,
                event TEXT,
                payload TEXT
            )
        """)
        self.conn.commit()

    def log_event(self, event: str, payload: dict) -> dict:
        """Append an event entry.

        Args:
            event: Event name, e.g. "brainstorm".
            payload: Arbitrary JSON-serializable dict.
        """
        ts = time.time()
        self.conn.execute(
            "INSERT INTO events (ts, event, payload) VALUES (?, ?, ?)",
            (ts, event, json.dumps(payload, ensure_ascii=False)),
        )
        self.conn.commit()
        return {"ts": ts, "event": event, "payload": payload}

    def close(self) -> None:
        self.conn.close()
