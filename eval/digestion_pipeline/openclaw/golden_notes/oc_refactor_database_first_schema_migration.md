---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - database_first
keywords:
  - openclaw database-first schema
  - global per-agent sqlite database
  - doctor migration openclaw doctor --fix
  - migration_runs migration_sources
  - legacy json jsonl import idempotent
  - target schema shape sessions transcript_events
  - backup vacuum into integrity_check
  - migration plan phases 0-7
topics:
  - OpenClaw
  - Database-First Refactor
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/refactor/database-first
access_control_group: ["general"]
---

# OpenClaw — Database-First Target Schema, Doctor Migrations, and Backup

## Overview

This note argues the *build-and-move* half of the OpenClaw database-first refactor: the concrete two-level SQLite schema the decision mandates, the doctor-driven import of legacy JSON/JSONL state into it, the inventory of what moves where, the phased migration plan (Phases 0–7), and SQLite-native backup/restore. It mirrors the `Target Schema Shape`, `Doctor Migration Shape`, `Migration Inventory`, `Migration Plan`, and `Backup And Restore` sections of the `refactor/database-first` source page. The *why* (decision + hard contract) lives in `oc_refactor_database_first_decision.md`; the *runtime cut-over* (runtime refactor plan, performance rules, static bans, done criteria) lives in `oc_refactor_database_first_runtime.md`. The per-file Migration Inventory enumeration is distilled to its pattern here; the full per-channel file list stays on the source page and the `repo_openclaw_*` code notes.

## Target Schema Shape

The schema is kept explicit: host-owned runtime state uses typed tables, and plugin-owned opaque state uses `plugin_state_entries` / `plugin_blob_entries` rows — there is deliberately no generic host `kv` table. Large values use `blob` columns rather than JSON string encoding; `value_json` is reserved for small structured data that must stay inspectable with plain SQLite tooling. `agent_databases` is the canonical agent registry for this branch, and no `agents` table is added until a real agent-record owner exists (agent config remains in `openclaw.json`).

The **global (control-plane) database** owns shared coordination state. Its key tables (column lists abbreviated; full DDL on the source page):

```text
state_leases(scope, lease_key, owner, expires_at, heartbeat_at, payload_json, created_at, updated_at)
schema_meta(meta_key, role, schema_version, agent_id, app_version, created_at, updated_at)
agent_databases(agent_id, path, schema_version, last_seen_at, size_bytes)
task_runs(...)  task_delivery_state(...)  flow_runs(...)  subagent_runs(...)
current_conversation_bindings(...)  plugin_binding_approvals(...)  tui_last_sessions(...)
plugin_state_entries(plugin_id, namespace, entry_key, value_json, created_at, expires_at)
plugin_blob_entries(plugin_id, namespace, entry_key, metadata_json, blob, created_at, expires_at)
media_blobs(...)  skill_uploads(...)  managed_outgoing_image_records(...)
web_push_subscriptions(...)  web_push_vapid_keys(...)  apns_registrations(...)
node_host_config(...)  device_identities(...)  device_auth_tokens(...)
macos_port_guardian_records(...)  workspace_setup_state(...)  native_hook_relay_bridges(...)
model_capability_cache(...)  agent_model_catalogs(catalog_key, agent_dir, raw_json, updated_at)
exec_approvals_config(...)  sandbox_registry_entries(...)  channel_pairing_requests(...)
channel_pairing_allow_entries(...)  voicewake_triggers(...)  voicewake_routing_config(...)
voicewake_routing_routes(...)  update_check_state(...)  config_health_entries(...)
gateway_restart_sentinel(...)  cron_jobs(...)  cron_run_logs(...)  delivery_queue_entries(...)
commitments(...)
migration_runs(id, started_at, finished_at, status, report_json)
migration_sources(source_key, migration_kind, source_path, target_table, source_sha256, source_size_bytes, source_record_count, last_run_id, status, imported_at, removed_source, report_json)
backup_runs(id, created_at, archive_path, status, manifest_json)
```

The **agent (data-plane) database** — one per agent at `agents/<agentId>/agent/openclaw-agent.sqlite` — owns session, transcript, VFS, artifact, cache, and memory-index state:

```text
schema_meta(meta_key, role, schema_version, agent_id, app_version, created_at, updated_at)
sessions(session_id, session_key, session_scope, created_at, updated_at, started_at, ended_at, status, chat_type, channel, account_id, primary_conversation_id, model_provider, model, agent_harness_id, parent_session_key, spawned_by, display_name)
conversations(conversation_id, channel, account_id, kind, peer_id, parent_conversation_id, thread_id, native_channel_id, native_direct_user_id, label, metadata_json, created_at, updated_at)
session_conversations(session_id, conversation_id, role, first_seen_at, last_seen_at)
session_routes(session_key, session_id, updated_at)
session_entries(session_id, session_key, entry_json, updated_at)
transcript_events(session_id, seq, event_json, created_at)
transcript_event_identities(session_id, event_id, seq, event_type, has_parent, parent_id, message_idempotency_key, created_at)
transcript_snapshots(session_id, snapshot_id, reason, event_count, created_at, metadata_json)
vfs_entries(namespace, path, kind, content_blob, metadata_json, updated_at)
tool_artifacts(run_id, artifact_id, kind, metadata_json, blob, created_at)
run_artifacts(run_id, path, kind, metadata_json, blob, created_at)
trajectory_runtime_events(session_id, run_id, seq, event_json, created_at)
memory_index_meta / memory_index_sources / memory_index_chunks / memory_embedding_cache / memory_index_state
cache_entries(scope, key, value_json, blob, expires_at, updated_at)
```

`sessions` is the canonical session root keyed by `session_id`; `session_entries.entry_json` hangs off it by foreign key as a compatibility shadow, and `session_routes` is the unique active `session_key`→`session_id` index so a route key can move to a fresh session without duplicate-row ambiguity. Future full-text search can add `transcript_events_fts(session_id, seq, text)` and `vfs_entries_fts(namespace, path, text)` side tables *without changing the canonical event tables* — the schema is designed so FTS is additive.

## Doctor Migration Shape

Legacy file-to-database import is owned exclusively by one explicit, reportable, rerun-safe doctor step:

```bash
openclaw doctor --fix
```

`openclaw doctor --fix` invokes the state-migration implementation after ordinary config preflight and creates a verified backup before import. Runtime startup and `openclaw migrate` must *not* import legacy OpenClaw state files. The migration has these properties: one pass discovers all legacy file sources and produces a plan before mutating anything; doctor creates a verified pre-migration backup archive before importing; imports are idempotent and keyed by source path, mtime, size, hash, and target table; successful source files are removed or archived only after the target database has committed; failed imports leave the source untouched and record a warning in `migration_runs`; runtime reads SQLite only after the migration exists; and no downgrade/export-to-runtime-files path is required.

## Migration Inventory

The inventory is a deletion-and-relocation map distilled to its three rules below — what moves to the global DB, what moves to agent DBs, and what stays file-backed. The per-channel source list (Telegram, Discord, Matrix, Microsoft Teams, iMessage, BlueBubbles, Nostr, QQBot, Skill Workshop, ACPX, etc., each with its retired JSON/JSONL filenames and target `plugin_state_entries`/`plugin_blob_entries` namespace) is long; the exhaustive enumeration stays on the source page and is linked to the `repo_openclaw_*` code notes rather than transcribed here.

**Move into the global database** — control-plane and gateway-scoped state: task registry and Task Flow runtime writes (deleting the unshipped `tasks/runs.sqlite` and `tasks/flows/registry.sqlite` sidecar importers); plugin state (deleting the unshipped `plugin-state/state.sqlite` sidecar); sandbox container/browser registries (from monolithic and sharded JSON); cron job definitions, schedule state, and run history (importing/removing `jobs.json`, `jobs-state.json`, `cron/runs/*.jsonl`); device identity/auth, push, update-check, commitments, OpenRouter model cache, installed plugin index, app-server bindings; device/node pairing and bootstrap records; outbound and session delivery queues (sharing `delivery_queue_entries` under `outbound-delivery` / `session-delivery` queue names); ACPX process leases (under the `acpx/process-leases` namespace); plus per-channel plugin caches/dedupe/credentials as SQLite plugin-state rows; and backup and migration run metadata. The pattern: hot routing/state fields become typed columns, while the JSON payload is retained only as a replay/debug copy.

**Move into agent databases** — data-plane per-agent state: agent session roots plus compatibility-shaped `session_entries` payloads; transcript events; compaction checkpoints and `transcript_snapshots`; agent VFS scratch/workspace namespaces; subagent attachment payloads (as VFS seed entries, never durable workspace files); tool artifacts; run artifacts; agent-local runtime caches (gateway-wide model caches stay global unless they become agent-specific); ACP parent stream logs; ACP replay-ledger sessions (`acp_replay_sessions`/`acp_replay_events`, with `acp/event-ledger.json` as doctor input only); ACP session metadata (`acp_sessions`, with `entry.acp` blocks in `sessions.json` as doctor input); and trajectory sidecars when they are not explicit export files.

**Keep file-backed for now** — `openclaw.json`; provider or CLI credential files; plugin/package manifests; user workspaces and Git repositories when disk mode is selected; and logs intended for operator tailing (unless a specific log surface is explicitly moved).

## Migration Plan (Phases 0–7)

The migration plan sequences the move so the boundary is frozen before more rows shift, and the old world is deleted last. Most phases are marked partly or fully `Done` for runtime writes on the current branch.

- **Phase 0 — Freeze the boundary.** Add the `migration_runs` table; add a single doctor-owned state-migration service for file-to-database import; make `plan` read-only and make `apply` create a backup, import, verify, then delete or quarantine old files; and add static bans so new runtime code cannot write legacy state files while migration code and tests can still seed/read them.
- **Phase 1 — Finish the global control plane.** Keep shared coordination state in `state/openclaw.sqlite`: agent/agent-database registry, task and Task Flow ledgers, plugin state, sandbox registry, cron/scheduler run history, pairing/device/push/update-check/TUI/model caches and other small gateway-scoped state, backup/migration metadata, gateway media attachment bytes (in `media_blobs`, with direct paths as temp materializations), and debug-proxy capture sessions/events/payload blobs. This phase also deletes duplicate sidecar openers, permission helpers, WAL setup, filesystem pruning, and compatibility writers from those subsystems.
- **Phase 2 — Introduce per-agent databases.** Create one database per agent at `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite` and register it via the global `agent_databases` row (path, schema version, last-seen, size/integrity). Runtime asks the registry for the agent DB instead of deriving file paths. The agent DB owns `sessions` (root) + `session_entries` (compatibility) + `session_routes`, `conversations`/`session_conversations`, `transcript_events`, snapshots/checkpoints, `vfs_entries`, `tool_artifacts`/run artifacts, agent-local caches, ACP parent stream events, and trajectory runtime events.
- **Phase 3 — Replace session store APIs.** `Done` for runtime: the file-shaped session-store surface is no longer an active contract. Runtime no longer calls `loadSessionStore(storePath)` or treats `storePath` as identity; row ops are `getSessionEntry`, `upsertSessionEntry`, `patchSessionEntry`, `deleteSessionEntry`, `listSessionEntries`; whole-store rewriters/file writers/queue tests/alias pruning are gone from runtime; `sessions.json` parsing remains only in doctor migration code.
- **Phase 4 — Move transcripts, ACP streams, trajectories, and VFS.** Make every agent data stream database-native: transcript append goes through one SQLite transaction that ensures the session header, checks message idempotency, selects the parent tail, inserts into `transcript_events`, and records identity metadata in `transcript_event_identities`. ACP parent stream logs become rows (not `.acp-stream.jsonl`); ACP spawn stops persisting transcript JSONL paths; trajectory capture writes rows/artifacts directly; disk workspaces stay on disk in disk mode; VFS scratch uses the agent DB. The migration imports old JSONL once, records counts/hashes in `migration_runs`, and removes imported files after integrity checks.
- **Phase 5 — Backup, restore, vacuum, and verify.** Backups remain one archive file: checkpoint every global and agent database; snapshot each with SQLite backup semantics or `VACUUM INTO`; archive compact DB snapshots, config, external credentials, and requested workspace exports; omit raw live `*.sqlite-wal`/`*.sqlite-shm`; verify by opening every DB snapshot and running `PRAGMA integrity_check`. `openclaw backup create` verifies by default (`--no-verify` skips only the post-write archive pass, not the snapshot integrity check); restore copies snapshots back to their target paths.
- **Phase 6 — Worker runtime.** Keep worker mode experimental while the split lands: workers receive agent id, run id, filesystem mode, and DB registry identity; each opens its own SQLite connection; the parent keeps channel delivery, approvals, config, and cancellation authority; start with one worker per active run and add pooling only after lifecycle and connection ownership are stable.
- **Phase 7 — Delete the old world.** `Done` for runtime session management. The old world is allowed only as explicit doctor input or support/export output: no runtime `sessions.json`, transcript JSONL, sandbox registry JSON, task sidecar SQLite, or plugin-state sidecar SQLite writes; no JSON/session-file pruning, file transcript truncation, session file locks, or lock-shaped tests; no runtime compatibility exports whose purpose is keeping old files current.

## Backup And Restore

Backups are one archive file, but database capture is SQLite-native rather than raw live-file copies. The procedure: (1) stop long-running write activity or enter a short backup barrier; (2) checkpoint every global and agent database; (3) snapshot each database using SQLite backup semantics or `VACUUM INTO` into a temporary backup directory; (4) archive the compacted DB snapshots, config file, credentials directory, selected workspaces, and a manifest; (5) verify the archive by opening every included SQLite snapshot and running `PRAGMA integrity_check`. The source argues you must *not* rely on raw live `*.sqlite`, `*.sqlite-wal`, and `*.sqlite-shm` copies as the primary backup format. The archive manifest records database role, agent id, schema version, source path, snapshot path, byte size, and integrity status. Restore rebuilds the global and agent database files from the archive snapshots: because the SQLite layout has not shipped, this refactor keeps only the version-1 schema plus doctor file-to-database import — the restore command validates the archive first, then replaces each manifest asset from the verified extracted payload.

**Source**: OpenClaw documentation — `refactor/database-first` (mirror `inbox/openclaw_docs/refactor/database-first.md`)
**Last Updated**: 2026-06-22
**Status**: Active
