---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - session_store
keywords:
  - openclaw session store
  - sessions.json sessionentry
  - sessionkey sessionid
  - transcript jsonl structure
  - session write lock
  - store maintenance disk controls
  - cron session retention
  - context window vs tracked tokens
  - daily idle reset
topics:
  - OpenClaw
  - Session Management
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/reference/session-management-compaction
access_control_group: ["general"]
---

# OpenClaw — Session Persistence Data Model (Store, Transcript, Lifecycle)

## Overview

This note models the OpenClaw **session persistence data model** as defined by the `reference/session-management-compaction` deep-dive: the Gateway as the single source of truth, the two persistence layers (the `sessions.json` store and the per-`sessionId` JSONL transcript), the on-disk paths, store-maintenance/disk-budget controls plus the session write lock, isolated cron-run sessions, `sessionKey` routing patterns, the `sessionId` reset/idle/daily lifecycle, the `SessionEntry` store schema, the JSONL transcript entry types, and the distinction between the model context window and the store's tracked-token counters. The compaction **operation** (settings, triggers, providers, memory flush, troubleshooting) is the sibling procedure note [`oc_reference_session_management_compaction`](oc_reference_session_management_compaction.md); this note covers only the static store/transcript/lifecycle model that compaction reads and writes.

## Source of Truth: the Gateway

OpenClaw is designed around a single **Gateway process** that owns session state. UIs — the macOS app, the web Control UI, and the TUI — should query the Gateway for session lists and token counts rather than reading files directly. In remote mode the session files live on the remote host, so "checking your local Mac files" will not reflect what the Gateway is actually using.

## Two Persistence Layers

OpenClaw persists sessions in two layers. The **session store (`sessions.json`)** is a key/value map `sessionKey -> SessionEntry`: it is small, mutable, and safe to edit (or to delete entries), and it tracks session metadata such as the current session id, last activity, toggles, and token counters. The **transcript (`<sessionId>.jsonl`)** is an append-only file with a tree structure — entries carry both an `id` and a `parentId` — storing the actual conversation plus tool calls and compaction summaries, and is used to rebuild the model context for future turns. Compaction checkpoints are metadata over the compacted successor transcript; new compactions do not write a second `.checkpoint.*.jsonl` copy.

Gateway history readers should avoid materializing the whole transcript unless the surface explicitly needs arbitrary historical access. First-page history, embedded chat history, restart recovery, and token/usage checks use **bounded tail reads**. Full transcript scans go through the async transcript index, which is cached by file path plus `mtimeMs`/`size` and shared across concurrent readers.

## On-Disk Locations

Per agent, on the Gateway host, OpenClaw resolves the store and transcripts via `src/config/sessions.ts` at these paths:

```
~/.openclaw/agents/<agentId>/sessions/sessions.json          # store
~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl       # transcript
~/.openclaw/agents/<agentId>/sessions/<sessionId>-topic-<threadId>.jsonl   # Telegram topic sessions
```

## Store Maintenance and Disk Controls

Session persistence has automatic maintenance controls under `session.maintenance` covering `sessions.json`, transcript artifacts, and trajectory sidecars: `mode` is `enforce` (default) or `warn`; `pruneAfter` is the stale-entry age cutoff (default `30d`); `maxEntries` caps entries in `sessions.json` (default `500`); `resetArchiveRetention` is retention for `*.reset.<timestamp>` transcript archives (default: same as `pruneAfter`; `false` disables cleanup); `maxDiskBytes` is an optional sessions-directory budget; and `highWaterBytes` is an optional target after cleanup (default `80%` of `maxDiskBytes`).

Normal Gateway writes flow through a per-store session writer that serializes in-process mutations without taking a runtime file lock. Hot-path patch helpers borrow the validated mutable cache while they hold that writer slot, so large `sessions.json` files are not cloned or reread for every metadata update. Runtime code should prefer `updateSessionStore(...)` or `updateSessionStoreEntry(...)`; direct whole-store saves are compatibility and offline-maintenance tools. When a Gateway is reachable, non-dry-run `openclaw sessions cleanup` and `openclaw agents delete` delegate store mutations to the Gateway so cleanup joins the same writer queue; `--store <path>` is the explicit offline repair path for direct file maintenance. `maxEntries` cleanup is batched for production-sized caps, so a store may briefly exceed the configured cap before the next high-water cleanup rewrites it back down. Session store reads do not prune or cap entries during Gateway startup — use writes or `openclaw sessions cleanup --enforce` for cleanup; `openclaw sessions cleanup --enforce` applies the configured cap immediately and prunes old unreferenced transcript, checkpoint, and trajectory artifacts even when no disk budget is configured.

Maintenance keeps durable external conversation pointers such as group sessions and thread-scoped chat sessions, but synthetic runtime entries for cron, hooks, heartbeat, ACP, and sub-agents can still be removed when they exceed the configured age, count, or disk budget. OpenClaw no longer creates automatic `sessions.json.bak.*` rotation backups during Gateway writes; the legacy `session.maintenance.rotateBytes` key is ignored and `openclaw doctor --fix` removes it from older configs.

Transcript mutations use a **session write lock** on the transcript file. Lock acquisition waits up to `session.writeLock.acquireTimeoutMs` before surfacing a busy-session error (default `60000` ms) — raise this only when legitimate prep, cleanup, compaction, or transcript-mirror work contends longer on slow machines. `session.writeLock.staleMs` controls when an existing lock can be reclaimed as stale (default `1800000` ms), and `session.writeLock.maxHoldMs` controls the in-process watchdog release threshold (default `300000` ms). The emergency env overrides are `OPENCLAW_SESSION_WRITE_LOCK_ACQUIRE_TIMEOUT_MS`, `OPENCLAW_SESSION_WRITE_LOCK_STALE_MS`, and `OPENCLAW_SESSION_WRITE_LOCK_MAX_HOLD_MS`.

Enforcement order for disk-budget cleanup in `mode: "enforce"` is: (1) remove the oldest archived, orphan-transcript, or orphan-trajectory artifacts first; (2) if still above target, evict the oldest session entries and their transcript/trajectory files; (3) keep going until usage is at or below `highWaterBytes`. In `mode: "warn"`, OpenClaw reports potential evictions but does not mutate the store/files. Maintenance can be run on demand with `openclaw sessions cleanup --dry-run` and `openclaw sessions cleanup --enforce`.

## Cron Sessions and Run Logs

Isolated cron runs also create session entries/transcripts and have dedicated retention controls: `cron.sessionRetention` (default `24h`) prunes old isolated cron-run sessions from the session store (`false` disables); `cron.runLog.keepLines` prunes retained SQLite run-history rows per cron job (default `2000`), while `cron.runLog.maxBytes` remains accepted for older file-backed run logs.

When cron force-creates a new isolated run session, it sanitizes the previous `cron:<jobId>` session entry before writing the new row. It carries safe preferences such as thinking/fast/verbose settings, labels, and explicit user-selected model/auth overrides, but it drops ambient conversation context — channel/group routing, send or queue policy, elevation, origin, and ACP runtime binding — so a fresh isolated run cannot inherit stale delivery or runtime authority from an older run.

## Session Keys (`sessionKey`)

A `sessionKey` identifies *which conversation bucket* you are in (routing plus isolation). Common patterns are: main/direct chat per agent `agent:<agentId>:<mainKey>` (default `main`); group `agent:<agentId>:<channel>:group:<id>`; room/channel for Discord/Slack `agent:<agentId>:<channel>:channel:<id>` or `...:room:<id>`; cron `cron:<job.id>`; and webhook `hook:<uuid>` (unless overridden). The canonical rules are documented at the `/concepts/session` page.

## Session Ids (`sessionId`)

Each `sessionKey` points at a current `sessionId` — the transcript file that continues the conversation. The lifecycle rules of thumb are:

- **Reset** (`/new`, `/reset`) creates a new `sessionId` for that `sessionKey`.
- **Daily reset** (default 4:00 AM local time on the gateway host) creates a new `sessionId` on the next message after the reset boundary.
- **Idle expiry** (`session.reset.idleMinutes` or legacy `session.idleMinutes`) creates a new `sessionId` when a message arrives after the idle window; when daily + idle are both configured, whichever expires first wins.
- **System events** (heartbeat, cron wakeups, exec notifications, gateway bookkeeping) may mutate the session row but do not extend daily/idle reset freshness. Reset rollover discards queued system-event notices for the previous session before the fresh prompt is built.
- **Parent fork policy** uses OpenClaw's active branch when creating a thread or subagent fork; if that branch is too large, OpenClaw starts the child with isolated context instead of failing or inheriting unusable history. The sizing policy is automatic, and the legacy `session.parentForkMaxTokens` config is removed by `openclaw doctor --fix`.

The decision happens in `initSessionState()` in `src/auto-reply/reply/session.ts`.

## Session Store Schema (`sessions.json`)

The store's value type is `SessionEntry` in `src/config/sessions.ts`. Key fields (not exhaustive):

- `sessionId`: current transcript id (the filename is derived from this unless `sessionFile` is set).
- `sessionStartedAt`: start timestamp for the current `sessionId`; daily-reset freshness uses this, and legacy rows may derive it from the JSONL session header.
- `lastInteractionAt`: last real user/channel interaction timestamp; idle-reset freshness uses this so heartbeat, cron, and exec events do not keep sessions alive (legacy rows without it fall back to the recovered session start time).
- `updatedAt`: last store-row mutation timestamp, used for listing, pruning, and bookkeeping — *not* the authority for daily/idle reset freshness.
- `sessionFile`: optional explicit transcript path override.
- `chatType`: `direct | group | room` (helps UIs and send policy).
- `provider`, `subject`, `room`, `space`, `displayName`: metadata for group/channel labeling.
- Toggles: `thinkingLevel`, `verboseLevel`, `reasoningLevel`, `elevatedLevel`, and `sendPolicy` (per-session override).
- Model selection: `providerOverride`, `modelOverride`, `authProfileOverride`.
- Token counters (best-effort / provider-dependent): `inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`.
- `compactionCount`: how often auto-compaction completed for this session key.
- `memoryFlushAt`: timestamp for the last pre-compaction memory flush.
- `memoryFlushCompactionCount`: compaction count when the last flush ran.

The store is safe to edit, but the Gateway is the authority: it may rewrite or rehydrate entries as sessions run.

## Transcript Structure (`*.jsonl`)

Transcripts are managed by `openclaw/plugin-sdk/agent-sessions`'s `SessionManager`. The file is JSONL: the first line is a session header (`type: "session"`, including `id`, `cwd`, `timestamp`, and optional `parentSession`), then session entries each carrying `id` + `parentId` (forming a tree). Notable entry types are:

- `message`: user/assistant/toolResult messages.
- `custom_message`: extension-injected messages that *do* enter model context (can be hidden from UI).
- `custom`: extension state that does *not* enter model context.
- `compaction`: a persisted compaction summary with `firstKeptEntryId` and `tokensBefore`.
- `branch_summary`: a persisted summary written when navigating a tree branch.

OpenClaw intentionally does **not** "fix up" transcripts; the Gateway uses `SessionManager` to read/write them.

## Context Windows vs Tracked Tokens

Two distinct concepts matter. The **model context window** is the hard per-model cap — the tokens visible to the model. The **session store counters** are rolling stats written into `sessions.json` (used for `/status` and dashboards). When tuning limits, the context window comes from the model catalog (and can be overridden via config), while `contextTokens` in the store is a runtime estimate/reporting value and should not be treated as a strict guarantee. For more, see the `/reference/token-use` page.

**Source**: OpenClaw documentation — `reference/session-management-compaction` (mirror `inbox/openclaw_docs/reference/session-management-compaction.md`)
**Last Updated**: 2026-06-22
**Status**: Active
