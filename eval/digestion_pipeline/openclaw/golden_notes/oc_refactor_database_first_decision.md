---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - database_first
keywords:
  - openclaw database-first refactor
  - sqlite primary durable state
  - two-level sqlite layout
  - global control-plane database
  - per-agent data-plane database
  - hard contract no transcript locators
  - agentId sessionId transcript identity
  - goal states sqlite-runtime clean
  - doctor migration legacy json jsonl
  - config stays file-backed
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

# OpenClaw — Database-First State Refactor: The Decision and Hard Contract

## Overview

This note captures the *decision and rationale* half of OpenClaw's **database-first state refactor** — the design argument that SQLite should be the primary durable state and cache layer for runtime data while configuration stays file-backed. It mirrors the `refactor/database-first` source page's opening sections: the two-level SQLite Decision, the Hard Contract that pins the one canonical runtime shape, the Goal state and progress ladder (hard goal, goal states, current state, remaining work, do-not-regress), the Code-Read Assumptions and Findings that justify "this is no longer a SQLite-vs-files choice", and a distilled summary of the ~1,145-line Current Code Shape inventory. The *target schema + doctor migrations* live in [oc_refactor_database_first_schema_migration](oc_refactor_database_first_schema_migration.md), and the *runtime cut-over + performance rules + static bans + done criteria* live in [oc_refactor_database_first_runtime](oc_refactor_database_first_runtime.md); this note is one coherent `argument` — why SQLite-first, and what "clean" means.

## Decision: A Two-Level SQLite Layout

The refactor adopts a **two-level SQLite layout** with one durable global view that does not force large agent workspaces, transcripts, and binary scratch into the shared gateway write lane:

- **Global database** — `~/.openclaw/state/openclaw.sqlite`. This is the **control-plane database**. It owns agent discovery, shared gateway state, pairing, device/node state, task and flow ledgers, plugin state, scheduler runtime state, backup metadata, and migration state.
- **Agent database** — one SQLite database per agent (`agents/<agentId>/agent/openclaw-agent.sqlite`) for agent-owned workspace, transcript, VFS, artifact, and large per-agent runtime state. This is the **data-plane database**. It owns the agent's session metadata, transcript event stream, VFS workspace or scratch namespace, tool artifacts, run artifacts, and searchable/indexable agent-local cache data.
- **Configuration stays file-backed** — `openclaw.json` remains *outside* the database. Runtime auth profiles move to SQLite; external provider or CLI credential files remain owner-managed outside OpenClaw's database.

## Hard Contract: One Canonical Runtime Shape

The migration has **one canonical runtime shape**, stated as a set of invariants. Implementation work keeps deleting code until these statements are true without exceptions outside doctor/import/export/debug boundaries. The load-bearing rules (identifiers verbatim from source):

- **Session rows persist session metadata only.** They must not persist `transcriptLocator`, transcript file paths, sibling JSONL paths, lock paths, pruning metadata, or file-era compatibility pointers.
- **Transcript identity is always SQLite identity:** `{agentId, sessionId}` plus optional topic metadata where the protocol needs it.
- **`sqlite-transcript://...` is not a runtime or protocol identity.** New code must not derive, persist, pass, parse, or migrate transcript locators. Runtime and tests should not contain pseudo-locators at all; docs may mention the string only to ban it.
- **Legacy state is doctor-only:** `sessions.json`, transcript JSONL, `.jsonl.lock`, pruning, truncation, and old session-path logic belong only to the doctor migration/import path. Legacy session config aliases (`session.idleMinutes`, `session.resetByType.dm`, cross-agent `agent:main:*` aliases) belong only to doctor migration; runtime does not interpret them.
- **Session routing identity is typed relational state.** Hot runtime and UI paths should read `sessions.session_scope`, `sessions.account_id`, `sessions.primary_conversation_id`, `conversations`, and `session_conversations`; they must not parse `session_key` or mine `session_entries.entry_json` for provider identity except as a compatibility shadow while old call sites are being deleted.
- **Hooks run through discovered directories + `HOOK.md` metadata only;** runtime must not load `hooks.internal.handlers` (legacy hook config is a doctor warning/migration surface).
- **`{agentId, sessionId}` flows everywhere:** runtime startup, hot reply paths, compaction, reset, recovery, diagnostics, TTS, memory hooks, subagents, plugin command routing, protocol boundaries, and hooks all pass it through.
- **The runner cannot be tricked into files:** `runEmbeddedPiAgent(...)`, prepared worker runs, and the inner embedded attempt must not accept transcript locators — they open the SQLite transcript manager by `{agentId, sessionId}`.
- **Diagnostics and raw logging are SQLite rows:** runner diagnostics store runtime/cache/payload trace records in SQLite; raw stream logging uses `OPENCLAW_RAW_STREAM=1` plus SQLite diagnostics rows. The old pi-mono `PI_RAW_STREAM`, `PI_RAW_STREAM_PATH`, and `raw-openai-completions.jsonl` file logger contract is out.
- **Memory indexing does not re-export transcripts to markdown:** QMD indexes configured memory files only; session transcript search stays SQLite-backed via `memory-core-host-engine-session-transcripts`. Built-in memory indexes live in the owning agent database; runtime must not expose `memorySearch.store.path` (doctor deletes that legacy key; current code passes the agent `databasePath` internally).
- **Tests assert SQLite rows:** tests seed and assert SQLite transcript rows through `{agentId, sessionId}`; tests that only prove JSONL path forwarding, caller-supplied locator preservation, or transcript-file compatibility are deleted unless they cover doctor import, non-session support/debug materialization, or protocol shape.

## Goal State and Progress

### Hard goal

One global SQLite control-plane database (`state/openclaw.sqlite`) and one per-agent data-plane database (`agents/<agentId>/agent/openclaw-agent.sqlite`); config remains file-backed (`openclaw.json` is not part of this refactor); legacy files are doctor migration inputs only; **runtime never writes or reads session or transcript JSONL as active state.**

### Goal states (the progress ladder)

The plan grades each subsystem on a fixed ladder:

- **`not-started`** — file-era runtime code still writes active state.
- **`migrating`** — doctor/import code can move file data into SQLite.
- **`dual-read`** — a temporary bridge reads *both* SQLite and legacy files. **This state is forbidden for this refactor** unless explicitly documented as doctor-only.
- **`sqlite-runtime`** — runtime reads and writes SQLite only.
- **`clean`** — legacy runtime APIs and tests are removed, and the guard prevents regressions.
- **`done`** — docs, tests, backup, doctor migration, and changed checks prove the clean state.

### Current state (per subsystem)

Most subsystems are already `clean` or `sqlite-runtime`: **Sessions** `clean` (rows in the per-agent DB, runtime APIs use `{agentId, sessionId}`/`{agentId, sessionKey}`, `sessions.json` doctor-only); **Transcripts** `clean` (events/identities/snapshots/trajectory rows in the per-agent DB, no locators or JSONL paths accepted); **PI embedded runner** `clean` (SQLite session scope, rejects stale handles); **Cron** `clean` (`cron_jobs`/`cron_run_logs`); **Task registry** `clean` (rows in `state/openclaw.sqlite`); **Plugin state** `clean` (rows in the shared global DB); **Memory** `sqlite-runtime` (index tables in the per-agent DB, plugin memory uses shared plugin-state rows); **Backup** `sqlite-runtime` (compact snapshots, omits live WAL/SHM, verifies integrity, records runs); **E2E scripts** `clean` for runtime coverage. The one deliberately incomplete state is **Doctor migration**, which is `migrating` *intentionally* — doctor imports legacy JSON/JSONL and retired sidecar stores into SQLite, records migration runs/sources, and removes successful sources.

### Remaining work and do-not-regress

The Remaining-work checklist is fully checked off `[x]` (cron store-variable renames, obsolete export test mocks removed, the Docker legacy-JSONL seed made obviously doctor-only via `seedBrokenLegacySessionForDoctorMigration`, Kysely generated types kept aligned, focused tests re-run, and a final changed-gate proof on a Hetzner Crabbox run). The standing **Do not regress** rules: no transcript locators; no active session files; no fake JSONL test fixtures except doctor legacy migration tests; no raw SQLite access where Kysely is expected; and **no new legacy DB migrations** — because this layout has not shipped, schema version stays at `1` unless there is a strong reason.

## Code-Read Assumptions

No follow-up product decisions block the plan; implementation proceeds under these assumptions: use `node:sqlite` directly and require the Node 22+ runtime for this storage path; keep exactly one normal configuration file (do not move config, plugin manifests, or Git workspaces into SQLite); runtime compatibility files are not required (legacy JSON/JSONL are migration inputs only, and branch-local SQLite sidecars never shipped, so they are deleted not imported); `openclaw doctor --fix` owns the legacy file-to-database migration step (runtime startup and `openclaw migrate` carry no legacy DB-upgrade paths); credential compatibility follows the same rule (runtime credentials live in SQLite; `auth-profiles.json`, per-agent `auth.json`, and shared `credentials/oauth.json` are doctor inputs, removed after import); generated model catalog state is DB-backed in `agent_model_catalogs` (runtime must not write `agents/<agentId>/agent/models.json`); runtime must not migrate/normalize/bridge transcript locators (`sqlite-transcript://...` must *disappear*, not become a boundary handle); Codex app-server bindings use the OpenClaw `sessionId` as the canonical key (`sessionKey` is routing/display metadata only); backup output remains one archive file with DB contents as compact SQLite snapshots; transcript search is useful-but-not-required for the first cut (schema designed so FTS can be added later); and worker execution stays experimental behind settings while the DB boundary settles.

## Code-Read Findings

The current branch is **already past proof-of-concept**: the shared database exists, `node:sqlite` is wired through a small runtime helper, and former stores now write to `state/openclaw.sqlite` or the owning `openclaw-agent.sqlite`. The remaining work is therefore **not choosing SQLite** — it is keeping the new boundary clean and deleting any compatibility-shaped interface that still looks like the old file world. Concretely: session `storePath` is no longer a runtime identity, fixture shape, or status-payload field (doctor/migration owns that vocabulary); session writes no longer pass the old in-process `store-writer.ts` queue (SQLite patch writes use conflict detection + bounded retry); legacy path discovery keeps valid *migration* uses, but runtime stops treating `sessions.json` and transcript JSONL as write targets; agent-owned tables live in per-agent SQLite DBs while the global DB keeps registry/control-plane rows; and doctor's several legacy-file imports are to be consolidated into a single explicit migration implementation with a durable migration report. **No additional product questions are blocking implementation.**

## Current Code Shape (Distilled)

> The source page enumerates the current shape across a ~1,145-line per-file/per-subsystem inventory (over 150 bullet points). Per the digestion plan this is **distilled to its pattern and rule**, not transcribed; the per-file detail is linked to the source URL and the OpenClaw code notes ([repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md), [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md), [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md), and the `snippet_openclaw_*` corpus).

The inventory establishes a **real shared SQLite base** and one recurring conversion pattern. The base: the runtime floor is **Node 22+** (package, CLI guard, installer, macOS locator, CI, docs all agree); `src/state/openclaw-state-db.ts` opens `openclaw.sqlite` with `WAL`, `synchronous=NORMAL`, `busy_timeout=30000`, `foreign_keys=ON` and applies the schema module generated from `src/state/openclaw-state-schema.sql`; **Kysely** table types are generated from disposable SQLite DBs built from committed `.sql` files (no copy-pasted schema strings, raw SQL limited to schema application, pragmas, and migration-only DDL); both schemas collapse to **`user_version = 1`** (this layout has not shipped); and `src/state/openclaw-agent-db.ts` opens the per-agent `openclaw-agent.sqlite`, registers it in the global `agent_databases` registry, and owns agent-local session/transcript/VFS/artifact/cache/memory-index tables. A `schema_meta` row in each database records role, schema version, timestamps, and (for agent DBs) agent id.

The recurring pattern across every subsystem is identical: **move a whole-file JSON/JSONL blob to a typed SQLite row, reconcile (upsert/delete-missing) by primary key instead of truncate-and-reinsert, keep an `entry_json`/`record_json`/`payload_json` copy only as a replay/debug shadow, and route the legacy file through doctor as an import-then-remove input.** This pattern is applied to dozens of stores — sessions, transcripts (the largest cluster: dropping `transcriptLocator`, `sqlite-transcript://...`, `storePath`, and static `SessionManager` facades in favor of `{agentId, sessionId}` row APIs), cron, tasks/flows, plugin state, memory indexes, subagent runs, conversation/delivery bindings, delivery queue, TUI restore pointers, TTS prefs, device identity/auth (TS + Swift `OpenClawKit` + Android sharing the same `state/openclaw.sqlite` rows, with a fail-closed legacy `identity/device.json` gate), auth profiles, gateway singleton locks (typed `state_leases` under `gateway_locks`, replacing temp-dir lock files), restart sentinel/intent/handoff, sandbox registry, commitments, media blobs (`media_blobs` canonical byte store), diagnostics (`diagnostic_events`/`diagnostic_stability_bundles`, removing `OPENCLAW_*` JSONL override env vars), and per-channel/plugin state (Matrix, Microsoft Teams, Telegram, Discord, iMessage, Feishu, Zalo, BlueBubbles, Nostr, QQBot, ClawHub, Memory Wiki, Canvas, ACPX leases + gateway-instance identity). Two further rules recur: **arbitrary plugin state does not get host-owned typed tables** (plugins use `plugin_state_entries` for versioned JSON and `plugin_blob_entries` for bytes, with namespace/key ownership, TTL cleanup, backup, and plugin migration records; host typed tables exist only where the host owns the query contract, e.g. `plugin_binding_approvals`); and **relational ownership cascades are enforced where the boundary is canonical** (source migration rows cascade from `migration_runs`, task delivery from `task_runs`, transcript identity from transcript events). The net argument: the system is one consolidation/deletion pass away from `clean`, and the contract above is the finish line.

**Source**: OpenClaw documentation — `refactor/database-first` (Decision · Hard Contract · Goal state and progress · Code-Read Assumptions · Code-Read Findings · Current Code Shape) (mirror `inbox/openclaw_docs/refactor/database-first.md`)
**Last Updated**: 2026-06-22
**Status**: Active
