# Plan: SQLite email store for the toy splitter

> **Markdown review file.** Open in any previewer (`Ctrl+Shift+V` in VS Code/Cursor).
>
> Lives in `learning/self/email_query_project/plan.md`.

## Recommendation (this revision)

**Agree with you.** Username-only search is the wrong key once `johnp@gmail.com` and `johnp@yahoo.com` are both valid. “Johnp” is not an identity; **the pair (username, domain)** — i.e. the full `email_id` — is.

What we keep and drop:

| Function | Keep? | Why |
|---|---|---|
| `init_db` | Yes | Create SQLite file + schema. |
| `_split_address` | Yes | Separate helper: split `user@domain` into parts. |
| `save_email` | Yes | Insert; UNIQUE on `email_id`; alert if that exact address is already stored. |
| `find_email` | Yes | Full address only: found or not found (0 or 1 row). Does not insert. |
| `fetch_emails_by_domain` | Yes | **Domain only.** List all users on that domain. |
| `search_for_username` | **No** | Ambiguous when the same local part exists on multiple domains. |

**`fetch` is not the full-address lookup.** `find_email` answers “is this exact email already stored?” `fetch_emails_by_domain` answers “who is on this domain?” `save_email` still hits UNIQUE on insert and alerts.

## Context

`learning/self/email_query_project/split_email.py` is a one-shot CLI that splits on the first `@`. Schema SQL is in `email.sql` in this folder.

This plan is **module creation**: schema + store API + thin CLI wiring.

## Goals

- Persist parsed emails in a **new SQLite** file.
- Enforce **`UNIQUE` on `email_id` only** so the same full address cannot be stored twice.
- **Allow** the same username on different domains (`johnp@gmail.com` and `johnp@yahoo.com` are two rows).
- **Alert** when the user enters an email that is already stored; do not insert again.
- Look up a **specific email** (username + domain) and **list by domain**.
- Stdlib `sqlite3` only.

## Naming (this revision)

| Name | Role |
|---|---|
| `parse_email.py` | CLI file (renamed from `split_email.py`). |
| `_split_address(raw)` | **Separate function** that splits `user@domain`. Leading `_` = helper, not the public store API. |
| `save_email` | Write/insert one full address. |
| `find_email` | Read **one full address**. Found → row; not found → `None`. |
| `fetch_emails_by_domain` | Read **by domain only**. 0 or more rows. |
| `init_db` | Create schema. |
| `email_db.py` | Store module. |

Two different read operations, two names on purpose:

- **find** = look up this exact email (identity check).
- **fetch** = pull the set of emails for a domain.

## Proposed file layout

All under `learning/self/email_query_project/`:

| File | Role |
|---|---|
| `email_db.py` | `_split_address`, `init_db`, `save_email`, `find_email`, `fetch_emails_by_domain`. |
| `parse_email.py` | CLI (renamed from `split_email.py`). |
| `email.sql` | Schema + sample inserts (already present). |

Optional later: `test_email_db.py` with a tempfile DB.

## Schema

Table `emails`:

| Column | Type | Constraints |
|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` |
| `email_id` | `TEXT` | `NOT NULL UNIQUE` — full address, e.g. `johnp@gmail.com` |
| `username` | `TEXT` | `NOT NULL` — **not unique** (same local part, many domains) |
| `domain` | `TEXT` | `NOT NULL` — may repeat (many users on `gmail.com`) |
| `created_at` | `TEXT` | `NOT NULL DEFAULT (datetime('now'))` |

```sql
CREATE TABLE IF NOT EXISTS emails (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id   TEXT    NOT NULL UNIQUE,
    username   TEXT    NOT NULL,
    domain     TEXT    NOT NULL,
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_emails_domain ON emails(domain);
```

- Uniqueness is **only** the full address. That is the identity.
- Normalize `email_id`, `username`, and `domain` with `strip().lower()` so `JohnP@Gmail.com` matches `johnp@gmail.com`.
- Default DB file: `learning/self/email_query_project/emails.db`. Optionally gitignore `*.db`.

## Module API (`email_db.py`)

### `init_db(db_path: str | Path | None = None) -> Path`

- Default path: `emails.db` beside the module.
- `CREATE TABLE IF NOT EXISTS` + domain index.
- Idempotent. Return the resolved path.

### `_split_address(raw: str) -> tuple[str, str, str]`

Separate helper (not a DB call). `strip().lower()`, split on first `@`, reject empty parts. Returns `(email_id, username, domain)` or raises `ValueError`. Used by `save_email` and `find_email`.

### `save_email(email_id: str, *, db_path: ... = None) -> dict`

1. Normalize and validate via `_split_address`.
2. `INSERT INTO emails (email_id, username, domain) VALUES (?, ?, ?)`.
3. Success: `{"ok": True, "email_id", "username", "domain", "id": lastrowid}`.
4. `sqlite3.IntegrityError` (duplicate `email_id`): **do not insert**. Return `{"ok": False, "duplicate": True, "email_id": ...}`. CLI alerts.

### `find_email(email_id: str, *, db_path: ... = None) -> dict | None`

Lookup by the **full** address only. Does not insert.

- Same `_split_address` rules.
- `SELECT ... FROM emails WHERE email_id = ?`
- **Found:** one dict. **Not found:** `None`.

This is the “is this input already in the database?” check.

### `fetch_emails_by_domain(domain: str, *, db_path: ... = None) -> list[dict]`

**Input:** domain with **one or more `.`** (e.g. `gmail.com`). No spaces, no `@`. Reject `gmail` or `.com`.

```sql
SELECT id, email_id, username, domain, created_at
FROM emails
WHERE domain = ?
ORDER BY username
```

Exact domain match: `gmail.com` returns only Gmail rows. Empty list if none. Fine for a handful of users.

### Shared helpers

- `_connect` with `sqlite3.Row`.

## CLI (`parse_email.py`)

1. `init_db()` on start.
2. Prompt for a full email.
3. Invalid `_split_address` → error, no write.
4. `find_email` first **or** `save_email` and handle duplicate:
   - Found / duplicate → **alert**: that username+domain is already stored; do not insert.
   - Not found → `save_email`; print username/domain + “saved”.
5. Optional prompt: domain → `fetch_emails_by_domain` → print all users on that domain (or none).

No username-only prompt.

## Duplicate-alert behavior

| User action | Result |
|---|---|
| New `johnp@gmail.com` | Insert |
| Same `johnp@gmail.com` again (any casing) | Alert; no second row |
| New `johnp@yahoo.com` | Insert (different `email_id`; username may repeat) |
| Invalid string | No write |
| Domain search `gmail.com` | All stored `*@gmail.com` rows |

No upsert.

## Out of scope

- `search_for_username`
- UNIQUE on `username`
- Migrations, soft delete, tests (next step), LLM lessons

## Implementation order

1. Add `email_db.py`: schema, `_split_address`, `init_db`, `save_email`, `find_email`, `fetch_emails_by_domain`.
2. Rename `split_email.py` → `parse_email.py` and wire the CLI.
3. Smoke: insert `johnp@gmail.com` and `johnp@yahoo.com`; repeat gmail → alert; domain search returns only that domain.
4. Optionally gitignore `*.db`.

## Defaults unless you object

- Lowercase normalize.
- UNIQUE **only** on `email_id`.
- One module `email_db.py`.
- `find_email` returns the row or `None`. `fetch_emails_by_domain` returns a list.

---

## Appendix — Dropped idea (`search_for_username`)

Earlier revision proposed UNIQUE on username and 0-or-1 username search. Dropped: the same local part on two domains is allowed, so username is not a unique key and a username-only search is not useful for “is this person already stored?”
