---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - session
keywords:
  - openclaw session management
  - session routing isolation
  - dmscope dm isolation
  - daily reset idle reset
  - sessions.json transcripts jsonl
  - session maintenance prune
  - inspecting sessions cli
  - gateway owned session state
topics:
  - OpenClaw
  - Session Management
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/session
access_control_group: ["general"]
---

# OpenClaw — Session Management (Routing, Isolation, Lifecycle, State)

## Overview

This note covers OpenClaw's **session** model as documented on the `concepts/session` source page: how OpenClaw organizes conversations into sessions, how each inbound message is routed to a session by its source, how DM isolation is controlled with `dmScope`, the daily/idle/manual reset lifecycle, where session state lives on disk (the gateway-owned `sessions.json` store and per-session `<sessionId>.jsonl` transcripts), how automatic session maintenance bounds storage over time, and the CLI/chat commands for inspecting sessions. A session is the conversation construct OpenClaw reuses across messages until it expires; all session state is owned by the gateway, and UI clients query the gateway for it.

## How messages are routed

OpenClaw organizes conversations into **sessions**, and each message is routed to a session based on where it came from — DMs, group chats, cron jobs, etc. The per-source routing behavior is:

| Source          | Behavior                  |
| --------------- | ------------------------- |
| Direct messages | Shared session by default |
| Group chats     | Isolated per group        |
| Rooms/channels  | Isolated per room         |
| Cron jobs       | Fresh session per run     |
| Webhooks        | Isolated per hook         |

## DM isolation

By default, all DMs share one session for continuity, which is fine for single-user setups. The source warns that if multiple people can message your agent you should enable DM isolation: without it, all users share the same conversation context — Alice's private messages would be visible to Bob. The fix is to set `session.dmScope`:

```json5
{
  session: {
    dmScope: "per-channel-peer", // isolate by channel + sender
  },
}
```

The available `dmScope` options are: `main` (default) — all DMs share one session; `per-peer` — isolate by sender (across channels); `per-channel-peer` — isolate by channel + sender (recommended); `per-account-channel-peer` — isolate by account + channel + sender. If the same person contacts you from multiple channels, use `session.identityLinks` to link their identities so they share one session.

### Dock linked channels

Dock commands let a user move the current direct-chat session's reply route to another linked channel without starting a new session. The source points to [Channel docking](https://docs.openclaw.ai/concepts/channel-docking) for examples, config, and troubleshooting. Verify your setup with `openclaw security audit`.

## Session lifecycle

Sessions are reused until they expire, through three reset mechanisms:

- **Daily reset** (default) — a new session at 4:00 AM local time on the gateway host. Daily freshness is based on when the current `sessionId` started, not on later metadata writes.
- **Idle reset** (optional) — a new session after a period of inactivity, set via `session.reset.idleMinutes`. Idle freshness is based on the last real user/channel interaction, so heartbeat, cron, and exec system events do not keep the session alive.
- **Manual reset** — type `/new` or `/reset` in chat; `/new <model>` also switches the model.

When both daily and idle resets are configured, whichever expires first wins. Heartbeat, cron, exec, and other system-event turns may write session metadata, but those writes do not extend daily or idle reset freshness. When a reset rolls the session, queued system-event notices for the old session are discarded so stale background updates are not prepended to the first prompt in the new session. Sessions with an active provider-owned CLI session are not cut by the implicit daily default; use `/reset` or configure `session.reset` explicitly when those sessions should expire on a timer.

## Where state lives

All session state is owned by the **gateway**, and UI clients query the gateway for session data. The on-disk layout is:

- **Store:** `~/.openclaw/agents/<agentId>/sessions/sessions.json`
- **Transcripts:** `~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`

`sessions.json` keeps separate lifecycle timestamps: `sessionStartedAt` — when the current `sessionId` began (daily reset uses this); `lastInteractionAt` — the last user/channel interaction that extends idle lifetime; and `updatedAt` — the last store-row mutation, useful for listing and pruning but not authoritative for daily/idle reset freshness. Older rows without `sessionStartedAt` are resolved from the transcript JSONL session header when available. If an older row also lacks `lastInteractionAt`, idle freshness falls back to that session start time, not to later bookkeeping writes.

## Session maintenance

OpenClaw automatically bounds session storage over time. By default it runs in `enforce` mode and applies cleanup during maintenance; set `session.maintenance.mode` to `"warn"` to report what would be cleaned without mutating the store/files:

```json5
{
  session: {
    maintenance: {
      mode: "enforce",
      pruneAfter: "30d",
      maxEntries: 500,
    },
  },
}
```

For production-sized `maxEntries` limits, Gateway runtime writes use a small high-water buffer and clean back down to the configured cap in batches. Session store reads do not prune or cap entries during Gateway startup, which avoids running full store cleanup on every startup or isolated cron session; `openclaw sessions cleanup --enforce` applies the cap immediately. Maintenance preserves durable external conversation pointers, including group sessions and thread-scoped chat sessions, while still allowing synthetic cron, hook, heartbeat, ACP, and sub-agent entries to age out. If you previously used direct-message isolation and later returned `session.dmScope` to `main`, preview stale peer-keyed DM rows with `openclaw sessions cleanup --dry-run --fix-dm-scope`; applying the same flag retires those old direct-DM rows and keeps their transcripts as deleted archives. Preview general maintenance with `openclaw sessions cleanup --dry-run`.

## Inspecting sessions

The source lists these inspection commands:

- `openclaw status` — session store path and recent activity.
- `openclaw sessions --json` — all sessions (filter with `--active <minutes>`).
- `/status` in chat — context usage, model, and toggles.
- `/context list` — what is in the system prompt.

**Source**: OpenClaw documentation — `concepts/session` (mirror `inbox/openclaw_docs/concepts/session.md`)
**Last Updated**: 2026-06-22
**Status**: Active
