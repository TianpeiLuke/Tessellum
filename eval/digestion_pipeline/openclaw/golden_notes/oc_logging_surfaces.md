---
tags:
  - resource
  - documentation
  - openclaw
  - top_level
  - logging
keywords:
  - openclaw log surfaces
  - openclaw logs --follow
  - jsonl file logs
  - control ui logs tab
  - gateway websocket protocol logging
  - channels logs --channel
  - logs.tail rpc
  - /tmp/openclaw rolling log
topics:
  - OpenClaw
  - Logging Surfaces
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/logging
access_control_group: ["general"]
---

# OpenClaw — Log Surfaces: Finding and Reading Logs

## Overview

This note is the operator procedure for **finding and reading** OpenClaw logs — the first half of the `logging` source page. OpenClaw has two main log surfaces: **file logs** (JSON lines) written by the Gateway, and **console output** shown in terminals and the Gateway Debug UI; the Control UI **Logs** tab tails the gateway file log. This note covers where the rolling JSONL file lives and rotates, how to read it via `openclaw logs --follow` (output modes, JSON `type`-tagged objects, and fallback behavior), the Control UI Logs tab, channel-only logs, the three log formats (File JSONL, Console, Gateway WebSocket), and quick troubleshooting tips. The companion note `oc_logging_configuration` owns the *configuring* half (log levels, `OPENCLAW_DEBUG_*` flags, trace correlation, redaction, diagnostics/OpenTelemetry).

## Where logs live

By default, the Gateway writes a rolling log file under:

`/tmp/openclaw/openclaw-YYYY-MM-DD.log`

The date uses the gateway host's local timezone. Each file rotates when it reaches `logging.maxFileBytes` (default: 100 MB). OpenClaw keeps up to five numbered archives beside the active file, such as `openclaw-YYYY-MM-DD.1.log`, and keeps writing to a fresh active log instead of suppressing diagnostics. You can override the path in `~/.openclaw/openclaw.json`:

```json
{
  "logging": {
    "file": "/path/to/openclaw.log"
  }
}
```

## How to read logs

### CLI: live tail (recommended)

Use the CLI to tail the gateway log file via RPC:

```bash
openclaw logs --follow
```

Useful current options:

- `--local-time`: render timestamps in your local timezone
- `--url <url>` / `--token <token>` / `--timeout <ms>`: standard Gateway RPC flags
- `--expect-final`: agent-backed RPC final-response wait flag (accepted here via the shared client layer)

Output modes:

- **TTY sessions**: pretty, colorized, structured log lines.
- **Non-TTY sessions**: plain text.
- `--json`: line-delimited JSON (one log event per line).
- `--plain`: force plain text in TTY sessions.
- `--no-color`: disable ANSI colors.

When you pass an explicit `--url`, the CLI does not auto-apply config or environment credentials; include `--token` yourself if the target Gateway requires auth. In JSON mode, the CLI emits `type`-tagged objects: `meta` (stream metadata — file, cursor, size), `log` (parsed log entry), `notice` (truncation / rotation hints), and `raw` (unparsed log line).

If the implicit local loopback Gateway asks for pairing, closes during connect, or times out before `logs.tail` answers, `openclaw logs` falls back to the configured Gateway file log automatically. Explicit `--url` targets do not use this fallback. `openclaw logs --follow` is stricter: on Linux it uses the active user-systemd Gateway journal by PID when available, and otherwise keeps retrying the live Gateway instead of following a potentially stale side-by-side file. If the Gateway is unreachable, the CLI prints a short hint to run:

```bash
openclaw doctor
```

### Control UI (web)

The Control UI's **Logs** tab tails the same file using `logs.tail`. See the Control UI docs for how to open it.

### Channel-only logs

To filter channel activity (WhatsApp/Telegram/etc), use:

```bash
openclaw channels logs --channel whatsapp
```

## Log formats

### File logs (JSONL)

Each line in the log file is a JSON object. The CLI and Control UI parse these entries to render structured output (time, level, subsystem, message). File-log JSONL records also include machine-filterable top-level fields when available:

- `hostname`: gateway host name.
- `message`: flattened log message text for full-text search.
- `agent_id`: active agent id when the log call carries agent context.
- `session_id`: active session id/key when the log call carries session context.
- `channel`: active channel when the log call carries channel context.

OpenClaw preserves the original structured log arguments alongside these fields so existing parsers that read numbered tslog argument keys keep working. Talk, realtime voice, and managed-room activity emits bounded lifecycle log records through this same file-log pipeline. These records include event type, mode, transport, provider, and size/timing measurements when available, but omit transcript text, audio payloads, turn ids, call ids, and provider item ids.

### Console output

Console logs are **TTY-aware** and formatted for readability: subsystem prefixes (e.g. `gateway/channels/whatsapp`), level coloring (info/warn/error), and an optional compact or JSON mode. Console formatting is controlled by `logging.consoleStyle` (configured in the companion note `oc_logging_configuration`).

### Gateway WebSocket logs

`openclaw gateway` also has WebSocket protocol logging for RPC traffic:

- normal mode: only interesting results (errors, parse errors, slow calls)
- `--verbose`: all request/response traffic
- `--ws-log auto|compact|full`: pick the verbose rendering style
- `--compact`: alias for `--ws-log compact`

Examples:

```bash
openclaw gateway
openclaw gateway --verbose --ws-log compact
openclaw gateway --verbose --ws-log full
```

## Troubleshooting tips

- **Gateway not reachable?** Run `openclaw doctor` first.
- **Logs empty?** Check that the Gateway is running and writing to the file path in `logging.file`.
- **Need more detail?** Set `logging.level` to `debug` or `trace` and retry (see `oc_logging_configuration`).

**Source**: OpenClaw documentation — `logging` (mirror `inbox/openclaw_docs/logging.md`), sections: Where logs live, How to read logs, Log formats, Troubleshooting tips
**Last Updated**: 2026-06-22
**Status**: Active
