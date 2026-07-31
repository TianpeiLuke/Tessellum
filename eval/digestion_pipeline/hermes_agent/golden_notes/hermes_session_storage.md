---
tags:
  - resource
  - documentation
  - hermes_agent
  - session_storage
  - persistence
keywords:
  - hermes session storage
  - state.db sqlite wal mode
  - messages_fts fts5 virtual table
  - schema version migrations
  - write contention handling
  - parent_session_id lineage
  - full-text search sanitization
  - export prune cleanup
topics:
  - Hermes Agent
  - Session Storage
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage
access_control_group: ["general"]
---

# Hermes Agent — Session Storage

## Overview

Session storage in Hermes Agent is a single **WAL-mode SQLite database** at `~/.hermes/state.db`, managed by the `SessionDB` class in `hermes_state.py`, that persists session metadata, full message history, and model configuration across both CLI and gateway sessions. It replaces the earlier per-session JSONL file approach with one shared, queryable, full-text-searchable store. The database is built around six objects — a `sessions` metadata table, a `messages` history table, two FTS5 virtual tables (`messages_fts` and a CJK/substring `messages_fts_trigram`), a `state_meta` key/value table, and a single-row `schema_version` table — and is engineered for many concurrent processes (gateway multi-platform writers, CLI sessions, worktree agents) sharing one file.

This note documents the concrete storage *model*: the WAL design decisions, the `sessions`/`messages`/FTS5 schema with its INSERT/UPDATE/DELETE sync triggers, the 11-version migration chain plus declarative `_reconcile_columns()`, the convoy-avoiding write-contention strategy, the common `SessionDB` operations, the FTS5 query syntax and sanitizer, `parent_session_id` lineage chains spawned by compression splits, and export/prune/cleanup. Batch-runner and RL trajectory data are explicitly NOT stored here (separate systems).

## Architecture Overview

The store is a single SQLite file in WAL mode holding six objects:

```
~/.hermes/state.db (SQLite, WAL mode)
├── sessions              — Session metadata, token counts, billing
├── messages              — Full message history per session
├── messages_fts          — FTS5 virtual table (content + tool_name + tool_calls)
├── messages_fts_trigram  — FTS5 virtual table with trigram tokenizer (CJK / substring search)
├── state_meta            — Key/value metadata table
└── schema_version        — Single-row table tracking migration state
```

Key design decisions: **WAL mode** allows concurrent readers plus one writer (the gateway is multi-platform); the **FTS5 virtual table** gives fast text search across all session messages; **session lineage** via `parent_session_id` chains captures compression-triggered splits; **source tagging** (`cli`, `telegram`, `discord`, etc.) supports platform filtering; and batch-runner / RL trajectories are deliberately kept in separate systems.

## SQLite Schema

The `sessions` table is the metadata + token-accounting + billing record, keyed by session `id`, source-tagged, and self-referential through `parent_session_id` (for lineage). It carries per-session token counters (`input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`, `reasoning_tokens`) and a full billing block (`billing_provider`/`billing_base_url`/`billing_mode`/`estimated_cost_usd`/`actual_cost_usd`/`cost_status`/`cost_source`/`pricing_version`), plus a unique-when-non-NULL `title`:

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    user_id TEXT,
    model TEXT,
    model_config TEXT,
    system_prompt TEXT,
    parent_session_id TEXT,
    started_at REAL NOT NULL,
    ended_at REAL,
    end_reason TEXT,
    message_count INTEGER DEFAULT 0,
    tool_call_count INTEGER DEFAULT 0,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    cache_read_tokens INTEGER DEFAULT 0,
    cache_write_tokens INTEGER DEFAULT 0,
    reasoning_tokens INTEGER DEFAULT 0,
    billing_provider TEXT,
    billing_base_url TEXT,
    billing_mode TEXT,
    estimated_cost_usd REAL,
    actual_cost_usd REAL,
    cost_status TEXT,
    cost_source TEXT,
    pricing_version TEXT,
    title TEXT,
    api_call_count INTEGER DEFAULT 0,
    FOREIGN KEY (parent_session_id) REFERENCES sessions(id)
);
```

Four indexes back the common access paths: `idx_sessions_source` (platform filter), `idx_sessions_parent` (lineage walks), `idx_sessions_started` (recent-first listing, `started_at DESC`), and a `UNIQUE` index on `title WHERE title IS NOT NULL` (titles must be unique among non-NULL values, NULLs allowed).

The `messages` table is the per-session history, ordered by `timestamp` (Unix epoch floats from `time.time()`) and indexed by `idx_messages_session(session_id, timestamp)`. It stores role/content/tool-call fields plus per-message token counts and several reasoning columns:

```sql
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    role TEXT NOT NULL,
    content TEXT,
    tool_call_id TEXT,
    tool_calls TEXT,
    tool_name TEXT,
    timestamp REAL NOT NULL,
    token_count INTEGER,
    finish_reason TEXT,
    reasoning TEXT,
    reasoning_content TEXT,
    reasoning_details TEXT,
    codex_reasoning_items TEXT,
    codex_message_items TEXT
);
```

`tool_calls` is a JSON string (serialized list of tool-call objects); `reasoning_details`, `codex_reasoning_items`, and `codex_message_items` are likewise JSON strings; and `reasoning` holds the raw reasoning text for providers that expose it.

### FTS5 Full-Text Search Table

`messages_fts` is an FTS5 virtual table mirroring message content, kept in sync by three triggers firing on `messages` INSERT / UPDATE / DELETE. The INSERT trigger is representative; UPDATE deletes the old rowid then re-inserts, and DELETE emits the FTS5 `'delete'` directive:

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
    content,
    content=messages,
    content_rowid=id
);

CREATE TRIGGER IF NOT EXISTS messages_fts_insert AFTER INSERT ON messages BEGIN
    INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);
END;
```

A second virtual table, `messages_fts_trigram`, uses the trigram tokenizer to support CJK and arbitrary substring search (added in migration v10). As of schema v11 both FTS tables also index `tool_name` and `tool_calls` and run in inline (rather than external-content) mode.

## Schema Version and Migrations

The current schema version is **11**, stored as a single integer in the `schema_version` table. Simple column additions are handled *declaratively* by `_reconcile_columns()`, which diffs live columns against `SCHEMA_SQL` and `ALTER TABLE ADD COLUMN`s any missing ones (wrapped in try/except so an already-existing column is a no-op — idempotent). The version-gated migration chain is reserved for data migrations and index/FTS changes that cannot be expressed declaratively; the version number is bumped after each successful migration block:

| Version | Change |
|---------|--------|
| 1 | Initial schema (sessions, messages, FTS5) |
| 2 | Add `finish_reason` column to messages |
| 3 | Add `title` column to sessions |
| 4 | Add unique index on `title` (NULLs allowed, non-NULL must be unique) |
| 5 | Add billing columns (`cache_read_tokens`, `cache_write_tokens`, `reasoning_tokens`, `billing_provider`, `billing_base_url`, `billing_mode`, `estimated_cost_usd`, `actual_cost_usd`, `cost_status`, `cost_source`, `pricing_version`) |
| 6 | Add reasoning columns to messages (`reasoning`, `reasoning_details`, `codex_reasoning_items`) |
| 7 | Add `reasoning_content` column to messages |
| 8 | Add `api_call_count` column to sessions |
| 9 | Add `codex_message_items` column for Codex Responses message id/phase replay |
| 10 | Add `messages_fts_trigram` virtual table (trigram tokenizer, CJK / substring) and backfill existing rows |
| 11 | Re-index both FTS tables to cover `tool_name` + `tool_calls`, switch from external-content to inline mode, drop old triggers, and backfill every message row |

## Write Contention Handling

Many Hermes processes (gateway + CLI sessions + worktree agents) share one `state.db`, so `SessionDB` handles write contention without the "convoy effect" — where SQLite's deterministic internal backoff makes all competing writers retry on the same intervals. The strategy: a **short 1-second SQLite timeout** (instead of the default 30s); **application-level retry with random jitter** (20–150ms, up to 15 retries); **`BEGIN IMMEDIATE`** transactions to surface lock contention at transaction start; and **periodic PASSIVE WAL checkpoints** every 50 successful writes. The tunables are constants on the class:

```python
_WRITE_MAX_RETRIES = 15
_WRITE_RETRY_MIN_S = 0.020   # 20ms
_WRITE_RETRY_MAX_S = 0.150   # 150ms
_CHECKPOINT_EVERY_N_WRITES = 50
```

## Common Operations

`SessionDB()` opens the default `~/.hermes/state.db` (or a custom path via `db_path=`). Session lifecycle is `create_session(session_id, source, model, user_id, parent_session_id=...)` (pass a previous session id to chain lineage), `end_session(id, end_reason=...)`, and `reopen_session(id)` (clears `ended_at`/`end_reason`). Messages are appended with `append_message(session_id, role, content, tool_calls=..., token_count=..., finish_reason=..., reasoning=...)` and read back either raw with all metadata via `get_messages(id)` or in OpenAI conversation format for API replay via `get_messages_as_conversation(id)`. Titles are managed with `set_session_title(id, title)` (must be unique among non-NULL titles), `resolve_session_by_title(title)` (returns the most recent in lineage), and `get_next_title_in_lineage(title)` (auto-numbers, e.g. `"Fix Docker Build"` → `"Fix Docker Build #2"`).

## Full-Text Search

`search_messages()` accepts FTS5 query syntax with automatic sanitization of user input: keywords are implicit AND (`docker deployment`), quoted strings are exact phrases (`"exact phrase"`), and `OR`/`NOT`/prefix-`*` are supported. Filters narrow the scope — `source_filter=["cli"]`, `exclude_sources=["telegram","discord"]`, and `role_filter=["user"]`. Each result carries `id`/`session_id`/`role`/`timestamp`, an FTS5 `snippet` with `>>>match<<<` markers, a `context` of one message before and after (truncated to 200 chars), and `source`/`model`/`session_started` from the parent session. The `_sanitize_fts5_query()` helper strips unmatched quotes and special characters, wraps hyphenated terms in quotes (`chat-send` → `"chat-send"`), and removes dangling boolean operators (`hello AND` → `hello`).

## Session Lineage

Sessions can form chains via `parent_session_id`, which happens when context compression triggers a session split in the gateway. Lineage is walked with recursive CTEs in both directions — ancestors and descendants:

```sql
-- Find all ancestors of a session
WITH RECURSIVE lineage AS (
    SELECT * FROM sessions WHERE id = ?
    UNION ALL
    SELECT s.* FROM sessions s
    JOIN lineage l ON s.id = l.parent_session_id
)
SELECT id, title, started_at, parent_session_id FROM lineage;
```

The descendants query mirrors this (joining `s.parent_session_id = d.id`). Other read-side queries documented on the page include a recent-sessions listing with a user-message preview (`SUBSTR(m.content, 1, 63)`) and a `last_active` MAX-timestamp, and token-usage statistics (per-model `SUM(input_tokens)`/`SUM(output_tokens)`/`SUM(estimated_cost_usd)`, and a highest-token-usage leaderboard).

## Export, Cleanup, and Database Location

Export with `export_session(id)` (one session + messages) or `export_all(source=...)` (all sessions as list of dicts). Cleanup with `prune_sessions(older_than_days=..., source=...)` (only ended sessions are pruned), `clear_messages(id)` (drops messages but keeps the session record), and `delete_session(id)` (removes the session and all its messages). The default database path is `~/.hermes/state.db`, derived from `hermes_constants.get_hermes_home()` (which resolves to `~/.hermes/` or the `HERMES_HOME` environment variable); the WAL file (`state.db-wal`) and shared-memory file (`state.db-shm`) live in the same directory.

**Source**: `inbox/hermes_agent_docs/developer-guide/session-storage.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage
**Last Updated**: 2026-06-19
**Status**: Active
