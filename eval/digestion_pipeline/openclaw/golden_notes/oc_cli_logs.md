---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - logs
keywords:
  - openclaw logs
  - tail gateway logs
  - logs.tail rpc
  - openclaw logs follow
  - remote log tail
  - gateway log json
  - implicit loopback fallback
  - logs reconnect backoff
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/logs
access_control_group: ["general"]
---

# OpenClaw — `openclaw logs` (Tail Gateway Logs via RPC)

## Overview

This note is the procedure for `openclaw logs`, the OpenClaw CLI command that tails the Gateway's file logs over RPC and works in remote mode (no SSH required). It mirrors the `cli/logs` source page: the line/byte/follow/interval/output flags under **Options**, the **Shared Gateway RPC options** (`--url`/`--token`/`--timeout`/`--expect-final`) and their explicit-credential rule, representative **Examples**, and the **Notes** covering timezone defaults, the implicit-local-loopback file-log fallback, Linux `--follow` journal-by-PID behavior, and `--follow` reconnect-with-backoff.

## What `openclaw logs` does

`openclaw logs` tails Gateway file logs over RPC and works in remote mode. The Gateway exposes the log tail as the `logs.tail` RPC call, so the command can read logs from a Gateway it is not co-located with — including over an explicit remote `--url` — instead of requiring direct filesystem or SSH access to the log file. By default it renders timestamps in your local timezone.

## Options

These flags shape how many log lines are returned, whether the stream is followed, and how output is rendered:

- `--limit <n>`: maximum number of log lines to return (default `200`)
- `--max-bytes <n>`: maximum bytes to read from the log file (default `250000`)
- `--follow`: follow the log stream
- `--interval <ms>`: polling interval while following (default `1000`)
- `--json`: emit line-delimited JSON events
- `--plain`: plain text output without styled formatting
- `--no-color`: disable ANSI colors
- `--local-time`: render timestamps in your local timezone (default)
- `--utc`: render timestamps in UTC

## Shared Gateway RPC options

`openclaw logs` also accepts the standard Gateway client flags shared across the Gateway-RPC CLI surface:

- `--url <url>`: Gateway WebSocket URL
- `--token <token>`: Gateway token
- `--timeout <ms>`: timeout in ms (default `30000`)
- `--expect-final`: wait for a final response when the Gateway call is agent-backed

When you pass `--url`, the CLI does not auto-apply config or environment credentials. Include `--token` explicitly if the target Gateway requires auth.

## Examples

The source page lists the following representative invocations — a basic tail, follow modes, larger limits/byte budgets, the machine-readable and plain/no-color output modes, the timezone toggles, and an explicit remote target with a token:

```bash
openclaw logs
openclaw logs --follow
openclaw logs --follow --interval 2000
openclaw logs --limit 500 --max-bytes 500000
openclaw logs --json
openclaw logs --plain
openclaw logs --no-color
openclaw logs --limit 500
openclaw logs --local-time
openclaw logs --utc
openclaw logs --follow --local-time
openclaw logs --url ws://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"
```

## Notes (timezone, fallback, follow behavior)

The source page records four behavioral notes that govern timezone rendering, the implicit-loopback fallback, Linux follow behavior, and reconnect-with-backoff:

- **Timezone default.** Timestamps render in your local timezone by default. Use `--utc` for UTC output.
- **Implicit-loopback file-log fallback.** If the implicit local loopback Gateway asks for pairing, closes during connect, or times out before `logs.tail` answers, `openclaw logs` falls back to the configured Gateway file log automatically. Explicit `--url` targets do not use this fallback.
- **`--follow` does not fall back to files.** `openclaw logs --follow` does not follow configured-file fallbacks after implicit local Gateway RPC failures. On Linux, it uses the active user-systemd Gateway journal by PID when available and prints the selected log source; otherwise it keeps retrying the live Gateway instead of tailing a potentially stale side-by-side file.
- **Reconnect with exponential backoff.** When using `--follow`, transient gateway disconnects (WebSocket close, timeout, connection drop) trigger automatic reconnection with exponential backoff (up to 8 retries, capped at 30 s between attempts). A warning is printed to stderr on each retry, and a `[logs] gateway reconnected` notice is printed once a poll succeeds. In `--json` mode both the retry warning and the reconnect transition are emitted as `{"type":"notice"}` records on stderr. Non-recoverable errors (auth failure, bad configuration) still exit immediately.

**Source**: OpenClaw documentation — `cli/logs` (mirror `inbox/openclaw_docs/cli/logs.md`)
**Last Updated**: 2026-06-22
**Status**: Active
