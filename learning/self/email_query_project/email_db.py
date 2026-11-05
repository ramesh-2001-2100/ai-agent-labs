"""SQLite email store: schema + CRUD helpers for the toy splitter."""

from __future__ import annotations

import sqlite3
from pathlib import Path

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS emails (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id   TEXT    NOT NULL UNIQUE,
    username   TEXT    NOT NULL,
    domain     TEXT    NOT NULL,
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_emails_domain ON emails(domain);
"""


def _default_db_path() -> Path:
    return Path(__file__).resolve().parent / "data" / "emails.db"


def _resolve_db_path(db_path: str | Path | None) -> Path:
    return Path(db_path) if db_path is not None else _default_db_path()


def _connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str | Path | None = None) -> Path:
    """Create the SQLite file and emails schema if missing. Idempotent."""
    path = _resolve_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with _connect(path) as conn:
        conn.executescript(_SCHEMA_SQL)
    return path.resolve()


def _split_address(raw: str) -> tuple[str, str, str]:
    """Normalize and split ``user@domain`` into ``(email_id, username, domain)``."""
    normalized = raw.strip().lower()
    if "@" not in normalized:
        raise ValueError(f"not a valid email address: {raw!r}")
    username, domain = normalized.split("@", 1)
    if not username or not domain:
        raise ValueError(f"not a valid email address: {raw!r}")
    email_id = f"{username}@{domain}"
    return email_id, username, domain


def _normalize_domain(raw: str) -> str:
    """Require a dotted domain like ``gmail.com`` (no spaces, no ``@``)."""
    domain = raw.strip().lower()
    if not domain or " " in domain or "@" in domain:
        raise ValueError(f"not a valid domain: {raw!r}")
    parts = domain.split(".")
    if len(parts) < 2 or any(part == "" for part in parts):
        raise ValueError(f"not a valid domain: {raw!r}")
    return domain


def _row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


def save_email(email_id: str, *, db_path: str | Path | None = None) -> dict:
    """Insert one full address. On duplicate ``email_id``, do not insert again."""
    path = init_db(db_path)
    normalized_id, username, domain = _split_address(email_id)
    try:
        with _connect(path) as conn:
            cur = conn.execute(
                "INSERT INTO emails (email_id, username, domain) VALUES (?, ?, ?)",
                (normalized_id, username, domain),
            )
            return {
                "ok": True,
                "email_id": normalized_id,
                "username": username,
                "domain": domain,
                "id": cur.lastrowid,
            }
    except sqlite3.IntegrityError:
        return {
            "ok": False,
            "duplicate": True,
            "email_id": normalized_id,
        }


def find_email(email_id: str, *, db_path: str | Path | None = None) -> dict | None:
    """Look up one full address. Returns the row dict, or ``None`` if missing."""
    path = init_db(db_path)
    normalized_id, _, _ = _split_address(email_id)
    with _connect(path) as conn:
        row = conn.execute(
            "SELECT id, email_id, username, domain, created_at "
            "FROM emails WHERE email_id = ?",
            (normalized_id,),
        ).fetchone()
    return _row_to_dict(row) if row is not None else None


def fetch_emails_by_domain(
    domain: str, *, db_path: str | Path | None = None
) -> list[dict]:
    """Return all stored emails for an exact domain, ordered by username."""
    path = init_db(db_path)
    normalized_domain = _normalize_domain(domain)
    with _connect(path) as conn:
        rows = conn.execute(
            "SELECT id, email_id, username, domain, created_at "
            "FROM emails WHERE domain = ? ORDER BY username",
            (normalized_domain,),
        ).fetchall()
    return [_row_to_dict(row) for row in rows]
