---
tags:
  - resource
  - documentation
  - hermes_agent
  - sessions
  - storage
keywords:
  - session search tool
  - fts5 full-text search
  - gateway session keys
  - shared vs isolated group sessions
  - state.db schema
  - session reset policies
  - auto-prune vacuum
  - wal mode
topics:
  - Hermes Agent
  - Sessions
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/sessions
access_control_group: ["general"]
---

# Hermes Agent — Session Search & Storage

## Overview

This is the **session data model** of Hermes Agent: the on-disk store that every conversation persists to, the agent tool that searches it, and the rules that key, reset, and prune it. All sessions live in a single SQLite file (`~/.hermes/state.db`) with an FTS5 full-text index over message content; the built-in `session_search` tool reads that index in three calling shapes (discovery / scroll / browse) and returns actual stored messages with no LLM calls. On messaging platforms, sessions are addressed by a deterministic gateway session key (shared-vs-isolated per group), auto-reset by configurable policies, and optionally auto-pruned on startup. (The procedural side — resume/title/handoff/`hermes sessions` commands — is its sibling [hermes_sessions_lifecycle_resume](hermes_sessions_lifecycle_resume.md).)

## Session Search Tool

The agent has a built-in `session_search` tool that performs full-text search across all past conversations using SQLite's FTS5 engine — and lets the agent scroll through any session it finds. No LLM calls, no summarization, no truncation. Every shape returns actual messages from the DB.

### Three calling shapes

The tool infers what you want from which arguments you set. There's no `mode` parameter.

**1. Discovery — pass `query`:**

```python
session_search(query="auth refactor", limit=3)
```

Runs FTS5, dedupes hits by session lineage, returns the top N sessions. Each result carries:

- `session_id`, `title`, `when`, `source`
- `snippet` — FTS5-highlighted match excerpt
- `bookend_start` — first 3 user+assistant messages of the session (the goal/kickoff)
- `messages` — ±5 messages around the FTS5 match, with the anchor message flagged (the hit in context)
- `bookend_end` — last 3 user+assistant messages of the session (the resolution/decisions)
- `match_message_id`, `messages_before`, `messages_after`

Bookends + window together reconstruct goal → match → resolution without paying for the whole transcript. Typical wall time: 15–50ms on a real session DB.

**2. Scroll — pass `session_id` + `around_message_id`:**

```python
session_search(session_id="20260510_174648_805cc2", around_message_id=590803, window=10)
```

Returns a window of ±`window` messages centered on the anchor. No FTS5, no bookends — just the slice. Use after a discovery call when you need more context than the ±5 default window. To scroll **forward** pass `messages[-1].id` back as `around_message_id`; to scroll **backward** pass `messages[0].id`. The boundary message appears in both windows as an orientation marker, and when `messages_before` or `messages_after` is less than `window` you're at the start or end of the session. Typical wall time: 1–2ms per scroll call.

**3. Browse — no args:**

```python
session_search()
```

Returns recent sessions chronologically (titles, previews, timestamps). Useful when the user asks "what was I working on" without naming a topic.

### FTS5 query syntax

The keyword mode supports standard FTS5 query syntax:

- Simple keywords: `docker deployment` (FTS5 defaults to AND)
- Phrases: `"exact phrase"`
- Boolean: `docker OR kubernetes`, `python NOT java`
- Prefix: `deploy*`

### Optional parameters

- `sort` — `newest` or `oldest`, on top of FTS5 ranking. Omit for relevance-only ordering (the default; suitable for exploratory recall). Use `newest` for "where did we leave X" questions, `oldest` for "how did X start" questions.
- `role_filter` — comma-separated roles to include. Discovery defaults to `user,assistant` (tool output is usually noise). Pass `user,assistant,tool` to include tool output (debugging tool behaviour) or `tool` to search tool output only.

### When It's Used

The agent is prompted to use session search automatically:

> *"When the user references something from a past conversation or you suspect relevant prior context exists, use session_search to recall it before asking them to repeat themselves."*

Typical triggers: "we did this before", "remember when", "last time", "as I mentioned", or any reference to a project/person/concept that isn't in the current window.

## Per-Platform Session Tracking

### Gateway Sessions

On messaging platforms, sessions are keyed by a deterministic session key built from the message source:

| Chat Type | Default Key Format | Behavior |
|-----------|--------------------|----------|
| Telegram DM | `agent:main:telegram:dm:<chat_id>` | One session per DM chat |
| Discord DM | `agent:main:discord:dm:<chat_id>` | One session per DM chat |
| WhatsApp DM | `agent:main:whatsapp:dm:<canonical_identifier>` | One session per DM user (LID/phone aliases collapse to one identity when mapping exists) |
| Group chat | `agent:main:<platform>:group:<chat_id>:<user_id>` | Per-user inside the group when the platform exposes a user ID |
| Group thread/topic | `agent:main:<platform>:group:<chat_id>:<thread_id>` | Shared session for all thread participants (default). Per-user with `thread_sessions_per_user: true`. |
| Channel | `agent:main:<platform>:channel:<chat_id>:<user_id>` | Per-user inside the channel when the platform exposes a user ID |

When Hermes cannot get a participant identifier for a shared chat, it falls back to one shared session for that room.

### Shared vs Isolated Group Sessions

By default, Hermes uses `group_sessions_per_user: true` in `config.yaml`. That means Alice and Bob can both talk to Hermes in the same Discord channel without sharing transcript history; one user's long tool-heavy task does not pollute another user's context window; and interrupt handling also stays per-user because the running-agent key matches the isolated session key.

If you want one shared "room brain" instead, set:

```yaml
group_sessions_per_user: false
```

That reverts groups/channels to a single shared session per room, which preserves shared conversational context but also shares token costs, interrupt state, and context growth.

### Session Reset Policies

Gateway sessions are automatically reset based on configurable policies:

- **idle** — reset after N minutes of inactivity
- **daily** — reset at a specific hour each day
- **both** — reset on whichever comes first (idle or daily)
- **none** — never auto-reset

Before a session is auto-reset, the agent is given a turn to save any important memories or skills from the conversation. Sessions with **active background processes** are never auto-reset, regardless of policy.

## Storage Locations

| What | Path | Description |
|------|------|-------------|
| SQLite database | `~/.hermes/state.db` | All session metadata + messages with FTS5 |
| Gateway messages | `~/.hermes/state.db` | SQLite — canonical store for all session messages |
| Gateway routing index | `~/.hermes/sessions/sessions.json` | Maps session keys to active session IDs (origin metadata, expiry flags) |

The SQLite database uses WAL mode for concurrent readers and a single writer, which suits the gateway's multi-platform architecture well.

> **Legacy JSONL transcripts** — Sessions created before `state.db` became canonical may have leftover `*.jsonl` files in `~/.hermes/sessions/`. They are no longer written or read by Hermes. Safe to delete after verifying the corresponding session exists in `state.db`.

### Database Schema

Key tables in `state.db`:

- **sessions** — session metadata (id, source, user_id, model, title, timestamps, token counts). Titles have a unique index (NULL titles allowed, only non-NULL must be unique).
- **messages** — full message history (role, content, tool_calls, tool_name, token_count)
- **messages_fts** — FTS5 virtual table for full-text search across message content

## Session Expiry and Cleanup

### Automatic Cleanup

- Gateway sessions auto-reset based on the configured reset policy
- Before reset, the agent saves memories and skills from the expiring session
- Opt-in auto-pruning: when `sessions.auto_prune` is `true`, ended sessions older than `sessions.retention_days` (default 90) are pruned at CLI/gateway startup
- After a prune that actually removed rows, `state.db` is `VACUUM`ed to reclaim disk space (SQLite does not shrink the file on plain DELETE)
- Pruning runs at most once per `sessions.min_interval_hours` (default 24); the last-run timestamp is tracked inside `state.db` itself so it's shared across every Hermes process in the same `HERMES_HOME`

Default is **off** — session history is valuable for `session_search` recall, and silently deleting it could surprise users. Enable in `~/.hermes/config.yaml`:

```yaml
sessions:
  auto_prune: true          # opt in — default is false
  retention_days: 90        # keep ended sessions this many days
  vacuum_after_prune: true  # reclaim disk space after a pruning sweep
  min_interval_hours: 24    # don't re-run the sweep more often than this
```

Active sessions are never auto-pruned, regardless of age.

### Manual Cleanup

Manual cleanup uses the same `hermes sessions prune` / `delete` / `export` commands (documented in [hermes_sessions_lifecycle_resume](hermes_sessions_lifecycle_resume.md)) for one-off cleanup without turning on the automatic sweep. The database grows slowly (typical: 10–15 MB for hundreds of sessions); enable auto-prune only on heavy gateway/cron workloads where `state.db` meaningfully affects performance (observed failure mode: a 384 MB `state.db` with ~1000 sessions slowing down FTS5 inserts and `/resume` listing).

**Source**: `inbox/hermes_agent_docs/user-guide/sessions.md` · https://hermes-agent.nousresearch.com/docs/user-guide/sessions
**Last Updated**: 2026-06-19
**Status**: Active
