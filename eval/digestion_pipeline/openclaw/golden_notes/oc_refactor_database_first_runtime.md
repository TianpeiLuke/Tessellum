---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - database_first
keywords:
  - openclaw database-first runtime refactor
  - per-agent sqlite database
  - session store row apis
  - sqlite performance rules wal busy_timeout
  - static bans legacy state files
  - worker runtime sqlite connection
  - delivery_queue_entries cron_jobs subagent_runs
  - done criteria sqlite-only runtime
topics:
  - OpenClaw
  - Database-First State Refactor
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/refactor/database-first
access_control_group: ["general"]
---

# OpenClaw — Database-First Runtime Refactor, Performance Rules, and Static Bans

## Overview

This note captures the runtime cut-over half of OpenClaw's database-first state refactor — the argument for *how* runtime state access is moved onto the new SQLite databases, and the guardrails that keep it from regressing — mirroring the `refactor/database-first` source page's "Runtime Refactor Plan", "Performance Rules", "Static Bans", and "Done Criteria" sections. The decision and hard contract (why SQLite-primary) live in [oc_refactor_database_first_decision](oc_refactor_database_first_decision.md), and the target schema plus the doctor "Migration Plan" (Phases 0–7) live in [oc_refactor_database_first_schema_migration](oc_refactor_database_first_schema_migration.md); this note is specifically the 10-step "Runtime Refactor Plan" numbered work list plus its performance/ban/done-criteria contract. The argument: replace file-shaped runtime state with per-agent SQLite databases and row-level APIs, enforce a small set of performance invariants on those databases, and add a repo check (`check:database-first-legacy-stores`) that bans new runtime writes to a long list of legacy file paths so the clean state cannot erode.

## Runtime Refactor Plan

The source frames the runtime cut-over as a 10-step numbered plan (distinct from the doctor-facing "Migration Plan" Phases 0–7 in the schema-migration note). Many steps are already marked `Done` for runtime; the plan's standing instruction is to keep deleting compatibility-shaped code until the contract holds without exceptions outside doctor/import/export/debug boundaries.

### Step 1 — Add database registry APIs

Resolve global-DB and per-agent-DB paths through a registry; keep the unshipped schemas at `user_version = 1` and do not add a schema migration runner until a shipped schema needs one; and add `close`/`checkpoint`/`integrity` helpers used by tests, backup, and doctor.

### Step 2 — Collapse sidecar SQLite stores

Move plugin-state tables, task-registry tables, and Task Flow tables into the global database, and move builtin memory-search tables into each agent database — each `Done` for runtime writes with its unshipped legacy sidecar importer deleted. The explicit custom `memorySearch.store.path` is removed by doctor config migration; full reindex runs in place against memory tables only, so the old whole-file swap path and sidecar index-swap helper are deleted. The step also deletes duplicate database openers, WAL setup, permission helpers, and close paths from those subsystems.

### Step 3 — Move agent-owned tables into per-agent databases

Create the agent DB on demand through the global database registry (`Done`), and move runtime session entries, transcript events, VFS rows, and tool artifacts to agent DBs (`Done`). Branch-local shared-DB session entries, transcript events, VFS rows, and tool artifacts are NOT migrated because that layout never shipped — only legacy file-to-database import is kept in doctor.

### Step 4 — Replace session store APIs

Remove `storePath` as the runtime identity (`Done` for runtime and guarded by `check:database-first-legacy-stores`): session metadata, route updates, command persistence, CLI session cleanup, Feishu reasoning previews, transcript-state persistence, subagent depth, auth profile session overrides, parent-fork logic, and QA-lab inspection now resolve the database from canonical agent/session keys. Gateway/TUI/UI/macOS session-list responses expose `databasePath` instead of legacy `path`. The runtime row operations are `getSessionEntry`, `upsertSessionEntry`, `deleteSessionEntry`, `patchSessionEntry`, and `listSessionEntries`, keyed by `{ agentId, sessionKey }` and requiring no session-store path. Whole-store delete/insert is replaced with `upsertSessionEntry`, `deleteSessionEntry`, `listSessionEntries`, and SQL cleanup queries using conflict-retried row patches; `store-writer.ts` and writer-queue tests are deleted, and runtime legacy-key pruning and alias-delete parameters are removed from session row upserts/patches. Hot call sites use `resolveSessionRowEntry`; the old `resolveSessionStoreEntry` compatibility alias is removed from runtime and the plugin SDK.

### Step 5 — Delete runtime JSON registry behavior

Make sandbox-registry reads and writes SQLite-only (`Done`), import monolithic and sharded JSON only from the migration step (`Done`), and remove sharded registry locks and JSON writes (`Done`). Keep one typed registry table rather than storing rows as generic opaque JSON when the shape remains hot-path operational state.

### Step 6 — Delete file-lock-shaped session mutation

`Done` for runtime lock creation and runtime lock APIs. The standalone legacy `.jsonl.lock` doctor cleanup lane is removed; `session.writeLock` is doctor-migrated legacy config, not a typed runtime setting; state integrity no longer has a separate orphan transcript-file pruning path; gateway singleton coordination uses typed SQLite `state_leases` rows under `gateway_locks` and exposes no file-lock directory seam; the generic plugin-SDK dedupe persistence writes shared SQLite plugin-state rows instead of file locks/JSON; and QMD embed coordination uses a SQLite state lease instead of `qmd/embed.lock`.

### Step 7 — Make workers database-aware

Workers open their own SQLite connections; the parent owns delivery, channel callbacks, and config; the worker receives agent id, run id, filesystem mode, and DB registry identity, NOT live handles. `vfs-only` stays experimental and uses the agent database as its storage root. Keep one worker per active run first — pooling waits until DB connection lifetime and cancellation behavior are boring.

### Step 8 — Backup integration

Teach backup to snapshot global and agent databases via SQLite backup or `VACUUM INTO` (`Done` for discovered `*.sqlite` files under the state asset), add SQLite integrity + schema-version verification (`Done`, with default archive verification), record backup-run metadata in the shared `backup_runs` table with archive path/status/manifest JSON (`Done`), and add restore from verified archive snapshots — `openclaw backup restore` validates before extraction, uses the verifier's normalized manifest, supports `--dry-run`, and requires `--yes` before replacing recorded source paths (`Done`). Include VFS/workspace export only when requested; do NOT export session internals as JSON or JSONL.

### Step 9 — Delete obsolete tests and code

`Done` for the known runtime session surfaces: tests that assert runtime creation of `sessions.json` or transcript JSONL are removed across core session store, chat, gateway transcript events, preview, lifecycle, command session-entry updates, auto-reply reset/trace, and many channel/memory paths. `sessions.delete` no longer returns a file-era `archived: []` field and the `deleteTranscript` option is gone — deleting a session removes the canonical `sessions` root and lets SQLite cascade session-owned transcript, snapshot, and trajectory rows, so no caller can leave transcript orphans. PI overflow recovery no longer has a SessionManager rewrite/truncation fallback: tool-result truncation and context-engine transcript rewrites mutate SQLite transcript rows, then refresh active prompt state from the database. The standing rule: keep tests that seed legacy files ONLY for migration; JSON-file proof is replaced with SQL row proof for active runtime surfaces; and static bans cover runtime writes to legacy session/cache JSON paths.

### Step 10 — Make the migration report auditable

Record migration runs in SQLite (started/finished timestamps, source paths, source hashes, counts, warnings, backup path) — `Done` via a `migration_runs` report plus per-source `migration_sources` rows for source-level audit and skip/backfill decisions. Make apply idempotent: re-running after a partial import either skips an already-imported source or merges by stable key (`Done` for session indexes, transcripts, delivery queues, plugin state, task ledgers, and agent-owned global rows). Failed imports must keep the original source file in place — a failed transcript import leaves the original JSONL at its detected path, and `migration_sources` records the source as `warning` with `removed_source=0` for the next doctor run.

## Performance Rules

The refactor mandates a small, explicit set of SQLite performance invariants for the new databases:

- One connection per thread/process is fine; do NOT share handles across workers.
- Use WAL, `foreign_keys=ON`, a 30s busy timeout, and short `BEGIN IMMEDIATE` write transactions.
- Keep write-transaction helpers synchronous unless/until an async transaction API adds explicit mutex/backpressure semantics.
- Keep parent delivery writes small and transactional.
- Avoid whole-store rewrites; use row-level upsert/delete.
- Add indexes for list-by-agent, list-by-session, updated-at, run id, and expiration paths before moving hot code.
- Store large artifacts, media, and vectors as BLOBs or chunked BLOB rows, not base64 or numeric-array JSON.
- Keep opaque plugin-state entries small and scoped.
- Add SQL cleanup for TTL/expiration instead of filesystem pruning — `Done` for database-owned runtime stores (media, plugin state, plugin blobs, persistent dedupe, and agent cache all expire through SQLite rows); remaining filesystem cleanup is limited to temporary materializations or explicit removal commands.

## Static Bans

The refactor adds a repo check (`check:database-first-legacy-stores`) that fails new runtime writes to legacy state paths and reintroduction of the retired transcript-bridge markers `transcriptLocator` and `sqlite-transcript://...`. The ban must still allow tests to create legacy fixtures and allow migration code to read/import/remove legacy file sources; unshipped SQLite sidecars stay banned with no doctor-import allowance. Rather than transcribe the full ~115-entry path list (it is the source's catalog of every retired file — see References + the `repo_openclaw_*` code notes for per-subsystem detail), the rule is captured by category with representative verbatim names:

- **Core session/transcript files:** `sessions.json`, `*.trajectory.jsonl` (except materialized support-bundle outputs), `.acp-stream.jsonl`, `acp/event-ledger.json`, `cache/*.json` runtime cache files.
- **Credentials/auth files:** `agents/<agentId>/agent/auth.json`, `agents/<agentId>/agent/models.json`, `credentials/oauth.json`, `github-copilot.token.json`, `openrouter-models.json`, `auth-profiles.json`, `auth-state.json`, `exec-approvals.json`, `workspace-state.json`.
- **Device/node/pairing/push files:** `devices/pending.json`, `devices/paired.json`, `devices/bootstrap.json`, `nodes/pending.json`, `nodes/paired.json`, `identity/device.json`, `identity/device-auth.json`, `device-pair-notify.json`, `push/web-push-subscriptions.json`, `push/vapid-keys.json`, `push/apns-registrations.json`, `process-leases.json`, `gateway-instance-id`.
- **Cron/scheduler files:** `cron/runs/*.jsonl`, `cron/jobs.json`, `jobs-state.json`.
- **Gateway control files:** `restart-sentinel.json`, `gateway-restart-intent.json`, `gateway-supervisor-restart-handoff.json`, `gateway.<hash>.lock`, `qmd/embed.lock`, `port-guard.json`, `config-health.json`, `plugin-binding-approvals.json`, `plugins/installs.json`, `bindings/current-conversations.json`, `commands.log`.
- **Unshipped SQLite sidecars (no import allowance):** `plugin-state/state.sqlite`, ad-hoc `openclaw-state.sqlite` runtime sidecars, `tasks/runs.sqlite`, `tasks/flows/registry.sqlite`.
- **Per-plugin/per-channel files** (Matrix `bot-storage.json` / `crypto-idb-snapshot.json`, Telegram `*.telegram-messages.json` / `thread-bindings-*.json`, Discord `model-picker-preferences.json`, Microsoft Teams `msteams-sso-tokens.json`, iMessage `reply-cache.jsonl`, QQBot `session-*.json`, Memory Wiki `.openclaw-wiki/log.jsonl`, ClawHub `.clawhub/lock.json`, etc.) plus memory-core `.dreams/*` files (`events.jsonl`, `session-corpus/`).
- **SessionManager file-era facades:** `SessionManager.open(...)` file-backed openers; `SessionManager.listAll(...)` / `TranscriptSessionManager.listAll(...)` listing facades; `forkFromSession(...)`, `newSession(...)`, and `createBranchedSession(...)` facades on both managers.

## Done Criteria

The refactor's runtime cut-over is "done" when:

- Runtime data and cache writes go to the global or agent SQLite database.
- Runtime no longer writes session indexes, transcript JSONL, sandbox registry JSON, task sidecar SQLite, or plugin-state sidecar SQLite — and the unshipped task and plugin-state sidecar SQLite importers are deleted.
- Legacy file import is doctor-only.
- Backup produces one archive with compact SQLite snapshots and integrity proof.
- Agent workers can run with disk, VFS scratch, or experimental VFS-only storage.
- Config and explicit credential files remain the only expected persistent non-database control files.
- Repo checks prevent reintroducing legacy runtime file stores.

**Source**: OpenClaw documentation — `refactor/database-first` (mirror `inbox/openclaw_docs/refactor/database-first.md`), sections "Runtime Refactor Plan", "Performance Rules", "Static Bans", "Done Criteria"
**Last Updated**: 2026-06-22
**Status**: Active
