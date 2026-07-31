---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - sessions
keywords:
  - openclaw sessions list
  - sessions tail follow
  - export-trajectory bundle
  - session scope flags
  - configuredAgentsOnly discovery
  - bounded sessions.list rpc
  - trajectory progress redaction
  - session liveness caveat
topics:
  - OpenClaw
  - CLI Sessions Inspection
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/sessions
access_control_group: ["general"]
---

# OpenClaw — Listing and Inspecting Stored Sessions (`openclaw sessions`)

## Overview

This note documents the read-only discovery and inspection half of the `openclaw sessions` command, mirroring the listing, scope-selection, `tail`, and `export-trajectory` portions of the `cli/sessions` source page. It covers bounded session listing (`--limit`, `totalCount`/`limitApplied`/`hasMore`), scope flags (`--agent` / `--all-agents` / `--store` / `--active`), the `configuredAgentsOnly` RPC mode, disk-only store discovery, redacted trajectory tailing (`tail` / `--follow` / `--session-key` / `--tail`), and exporting a trajectory bundle. The destructive state-maintenance half of the same page (`cleanup` and `compact`, and the `sessions.compact` RPC) is documented separately in the sibling note **[oc_cli_sessions_maintenance](oc_cli_sessions_maintenance.md)**.

## What `openclaw sessions` Lists (and the Liveness Caveat)

`openclaw sessions` lists stored conversation sessions — the persisted conversation rows held in session stores, NOT a channel/provider liveness check. A quiet Discord, Slack, Telegram, or other channel can reconnect successfully without creating a new session row until a message is processed. For live channel connectivity, the source page directs you to `openclaw channels status --probe`, `openclaw status --deep`, or `openclaw health --verbose` instead — a session list answers "what conversation state is persisted on disk," not "what channel is connected now."

## Bounded Listing and `configuredAgentsOnly`

`openclaw sessions` and the Gateway `sessions.list` responses are bounded by default so that large long-lived stores cannot monopolize the CLI process or Gateway event loop. The CLI returns the newest **100** sessions by default. Pass `--limit <n>` for a smaller or larger window, or `--limit all` when you intentionally need the full store. JSON responses include `totalCount`, `limitApplied`, and `hasMore` so callers can show that more rows exist beyond the returned window.

RPC clients can pass `configuredAgentsOnly: true` to keep the broad combined discovery source while returning only rows for agents currently present in config. The Control UI uses that mode by default so deleted or disk-only agent stores do not reappear in the Sessions view.

```bash
openclaw sessions
openclaw sessions --agent work
openclaw sessions --all-agents
openclaw sessions --active 120
openclaw sessions --limit 25
openclaw sessions --verbose
openclaw sessions --json
```

## Scope Selection Flags

Scope selection controls which store(s) the listing reads:

- default: configured default agent store
- `--verbose`: verbose logging
- `--agent <id>`: one configured agent store
- `--all-agents`: aggregate all configured agent stores
- `--store <path>`: explicit store path (cannot be combined with `--agent` or `--all-agents`)
- `--limit <n|all>`: max rows to output (default `100`; `all` restores full output)

### Disk-Only Store Discovery (`--all-agents`)

`openclaw sessions --all-agents` reads configured agent stores. Gateway and ACP session discovery are broader: they also include disk-only stores found under the default `agents/` root or a templated `session.store` root. Those discovered stores must resolve to regular `sessions.json` files inside the agent root; symlinks and out-of-root paths are skipped.

The `--all-agents --json` form returns a `stores` array (each `{ agentId, path }`) plus the bounding fields and a `sessions` array of per-row `{ agentId, key, model }`:

```json
{
  "path": null,
  "stores": [
    { "agentId": "main", "path": "/home/user/.openclaw/agents/main/sessions/sessions.json" },
    { "agentId": "work", "path": "/home/user/.openclaw/agents/work/sessions/sessions.json" }
  ],
  "allAgents": true,
  "count": 2,
  "totalCount": 2,
  "limitApplied": 100,
  "hasMore": false,
  "activeMinutes": null,
  "sessions": [
    { "agentId": "main", "key": "agent:main:main", "model": "gpt-5" },
    { "agentId": "work", "key": "agent:work:main", "model": "claude-opus-4-6" }
  ]
}
```

## Tailing Trajectory Progress (`sessions tail`)

`openclaw sessions tail` renders recent trajectory JSONL events as compact progress lines for stored sessions. Without `--session-key`, it tails running sessions first, then the latest stored session. `--tail <count>` controls how many existing events print before follow mode; the default is `80`, and `0` starts at the current end. `--follow` keeps watching the selected trajectory files, including relocated files referenced by `<session>.trajectory-path.json`.

```bash
openclaw sessions tail
openclaw sessions tail --follow
openclaw sessions tail --session-key "agent:main:telegram:direct:123" --tail 25
openclaw sessions --agent work tail --follow
openclaw sessions --all-agents tail --follow
```

The progress view is intentionally conservative: prompt text, tool arguments, and tool result bodies are not printed. Tool calls show the tool name with `{...redacted...}`; tool results show status such as `ok`, `error`, or `done`; model completion lines show provider/model and terminal status.

## Exporting a Trajectory Bundle (`sessions export-trajectory`)

`openclaw sessions export-trajectory` exports a trajectory bundle for a stored session, keyed by `--session-key`:

```bash
openclaw sessions export-trajectory --session-key "agent:main:telegram:direct:123" --workspace .
openclaw sessions export-trajectory --session-key "agent:main:telegram:direct:123" --output bug-123 --json
```

This is the command path used by the `/export-trajectory` slash command after the owner approves the exec request. The output directory is always resolved inside `.openclaw/trajectory-exports/` under the selected workspace.

**Source**: OpenClaw documentation — `cli/sessions` (mirror `inbox/openclaw_docs/cli/sessions.md`), discovery/inspection half
**Last Updated**: 2026-06-22
**Status**: Active
