---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - system
keywords:
  - openclaw system command
  - system event enqueue
  - system heartbeat enable disable
  - system presence
  - session-key targeted wake
  - mode now next-heartbeat
  - gateway system rpc
  - shared client flags
topics:
  - OpenClaw
  - CLI System Commands
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/system
access_control_group: ["general"]
---

# OpenClaw — `openclaw system` CLI (Events, Heartbeat, Presence)

## Overview

This note documents the `openclaw system` command — the gateway system-level helper surface that lets an operator enqueue system events, control heartbeats, and view presence — mirroring the `cli/system` source page. All `system` subcommands run over Gateway RPC and accept a common set of shared client flags. The three subcommands are `system event` (enqueue a `System:` line for injection at the next heartbeat, with a `--session-key` targeted-wake timing exception), `system heartbeat last|enable|disable` (inspect and toggle the heartbeat tick), and `system presence` (list nodes/instances the gateway knows about). A running gateway is required, and system events are ephemeral (not persisted across restarts).

## Shared client flags

Every `system` subcommand uses Gateway RPC and accepts these shared client flags:

- `--url <url>` — gateway WebSocket URL to connect to (e.g. `ws://127.0.0.1:18789`).
- `--token <token>` — gateway auth token (e.g. `$OPENCLAW_GATEWAY_TOKEN`).
- `--timeout <ms>` — RPC timeout in milliseconds.
- `--expect-final` — await the final pushed gateway response for streaming RPCs.

## Common commands

```bash
openclaw system event --text "Check for urgent follow-ups" --mode now
openclaw system event --text "Check for urgent follow-ups" --url ws://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"
openclaw system heartbeat enable
openclaw system heartbeat last
openclaw system presence
```

## `system event`

`system event` enqueues a system event on the **main** session by default; the next heartbeat injects it as a `System:` line in the prompt. Use `--mode now` to trigger the heartbeat immediately, while `next-heartbeat` (the default) waits for the next scheduled tick. Pass `--session-key` to target a specific session — for example to relay an async-task completion back to the channel that started it.

### `--session-key` timing exception

When `--session-key` is supplied, `--mode next-heartbeat` collapses to an immediate targeted wake instead of waiting for the next scheduled tick. Targeted wakes use heartbeat intent `immediate` so they bypass the runner's not-due gate that would otherwise defer (and effectively drop) an `event`-intent wake. If you want delayed delivery, omit `--session-key` so the event lands on the main session and rides the next regular heartbeat.

### Flags

- `--text <text>` — required system event text.
- `--mode <mode>` — `now` or `next-heartbeat` (default).
- `--session-key <sessionKey>` — optional; target a specific agent session instead of the agent's main session. Keys that do not belong to the resolved agent fall back to the agent's main session.
- `--json` — machine-readable output.
- `--url`, `--token`, `--timeout`, `--expect-final` — shared Gateway RPC flags.

## `system heartbeat last|enable|disable`

Heartbeat controls toggle and inspect the periodic gateway tick that drives heartbeat-injected events:

- `last` — show the last heartbeat event.
- `enable` — turn heartbeats back on (use this if they were disabled).
- `disable` — pause heartbeats.

### Flags

- `--json` — machine-readable output.
- `--url`, `--token`, `--timeout`, `--expect-final` — shared Gateway RPC flags.

## `system presence`

`system presence` lists the current system presence entries the gateway knows about (nodes, instances, and similar status lines).

### Flags

- `--json` — machine-readable output.
- `--url`, `--token`, `--timeout`, `--expect-final` — shared Gateway RPC flags.

## Notes

- Requires a running gateway reachable by your current config (local or remote).
- System events are ephemeral and not persisted across restarts.

**Source**: OpenClaw documentation — `cli/system` (mirror `inbox/openclaw_docs/cli/system.md`)
**Last Updated**: 2026-06-22
**Status**: Active
