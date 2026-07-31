---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - logging
keywords:
  - openclaw gateway logging
  - json lines file logger
  - logging.level logging.file
  - logging redaction redactSensitive redactPatterns
  - gateway websocket protocol logs
  - ws-log compact full
  - console capture consoleStyle
  - subsystem console formatting
topics:
  - OpenClaw
  - Gateway Logging
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/logging
access_control_group: ["general"]
---

# OpenClaw — Gateway Logging Surfaces

## Overview

This note is a procedure for operating OpenClaw's two logging surfaces — **console output** (terminal / Debug UI) and **file logs** (JSON lines written by the gateway logger) — mirroring the `gateway/logging` source page. It covers the file-based JSON-lines logger (path, level, rotation), how the CLI captures `console.*` to file logs with independent console verbosity, the secret-redaction policy (`redactSensitive` / `redactPatterns` and the always-redact safety boundaries including payment fields), the Gateway WebSocket protocol log modes and `--ws-log` style switch, and the TTY-aware subsystem console formatter.

## Logging Surfaces and Startup Summary

OpenClaw has two log surfaces: **console output** (what you see in the terminal / Debug UI) and **file logs** (JSON lines) written by the gateway logger. For a user-facing overview (CLI + Control UI + config) see the `/logging` page (link-out, not duplicated here). At startup the Gateway logs the resolved default agent model together with the mode defaults that affect new sessions, for example `agent model: openai/gpt-5.5 (thinking=medium, fast=on)`. `thinking` comes from the default agent, model params, or global agent default; when it is unset, the startup summary shows `medium`. `fast` comes from the default agent or model `fastMode` params.

## File-Based Logger

The file-based logger writes one JSON object per line, with these properties:

- The default rolling log file is under `/tmp/openclaw/`, one file per day: `openclaw-YYYY-MM-DD.log`. The date uses the gateway host's local timezone.
- Active log files rotate at `logging.maxFileBytes` (default `100 MB`), keeping up to **five** numbered archives and continuing to write a fresh active file.
- The log file path and level are configured via `~/.openclaw/openclaw.json` using `logging.file` (path) and `logging.level` (level).

Talk, realtime voice, and managed-room code paths use the shared file logger for **bounded lifecycle records** intended for operational debugging and OTLP log export; transcript text, audio payloads, turn ids, call ids, and provider item ids are **not** copied into the log record.

The Control UI Logs tab tails this file via the gateway (`logs.tail`); the CLI can do the same:

```bash
openclaw logs --follow
```

### Verbose vs. Log Levels

The file log level and console verbosity are governed separately:

- **File logs** are controlled exclusively by `logging.level`.
- `--verbose` only affects **console verbosity** (and WS log style); it does **not** raise the file log level.
- To capture verbose-only details in file logs, set `logging.level` to `debug` or `trace`.
- Trace logging also includes diagnostic timing summaries for selected hot paths, such as plugin tool factory preparation (see the `/tools/plugin#slow-plugin-tool-setup` reference).

## Console Capture

The CLI captures `console.log/info/warn/error/debug/trace` and writes them to file logs, while still printing to stdout/stderr. You can tune console verbosity independently of the file log level via:

- `logging.consoleLevel` (default `info`)
- `logging.consoleStyle` (`pretty` | `compact` | `json`)

## Redaction

OpenClaw can mask sensitive tokens before log or transcript output leaves the process. This logging redaction policy is applied at the **console, file-log, OTLP log-record, and session transcript text sinks**, so matching secret values are masked before JSONL lines or messages are written to disk. The configurable knobs are:

- `logging.redactSensitive`: `off` | `tools` (default `tools`).
- `logging.redactPatterns`: array of regex strings (overrides defaults). Use raw regex strings (auto `gi`), or `/pattern/flags` if you need custom flags. Matches are masked by keeping the first 6 + last 4 chars (length `>= 18`), otherwise `***`. Defaults cover common key assignments, CLI flags, JSON fields, bearer headers, PEM blocks, popular token prefixes, and payment credential field names such as **card number, CVC/CVV, shared payment token, and payment credential**.

Some safety boundaries **always redact regardless of `logging.redactSensitive`**: Control UI tool-call events, `sessions_history` tool output, diagnostics support exports, provider error observations, exec approval command display, and Gateway WebSocket protocol logs. These surfaces may still use `logging.redactPatterns` as additional patterns, but `redactSensitive: "off"` does not make them emit raw secrets.

## Gateway WebSocket Logs

The gateway prints WebSocket protocol logs in two modes:

- **Normal mode (no `--verbose`)** prints only "interesting" RPC results: errors (`ok=false`), slow calls (default threshold `>= 50ms`), and parse errors.
- **Verbose mode (`--verbose`)** prints all WS request/response traffic.

### WS Log Style

`openclaw gateway` supports a per-gateway style switch controlling how WS traffic is rendered:

- `--ws-log auto` (default): normal mode is optimized; verbose mode uses compact output.
- `--ws-log compact`: compact output (paired request/response) when verbose.
- `--ws-log full`: full per-frame output when verbose.
- `--compact`: alias for `--ws-log compact`.

Examples:

```bash
# optimized (only errors/slow)
openclaw gateway

# show all WS traffic (paired)
openclaw gateway --verbose --ws-log compact

# show all WS traffic (full meta)
openclaw gateway --verbose --ws-log full
```

## Console Formatting (Subsystem Logging)

The console formatter is **TTY-aware** and prints consistent, prefixed lines; subsystem loggers keep output grouped and scannable. Its behavior:

- **Subsystem prefixes** on every line (e.g. `[gateway]`, `[canvas]`, `[tailscale]`).
- **Subsystem colors** (stable per subsystem) plus level coloring.
- **Color when output is a TTY or the environment looks like a rich terminal** (`TERM` / `COLORTERM` / `TERM_PROGRAM`), respecting `NO_COLOR`.
- **Shortened subsystem prefixes**: drops leading `gateway/` + `channels/`, keeps the last 2 segments (e.g. `whatsapp/outbound`).
- **Sub-loggers by subsystem** (auto prefix + structured field `{ subsystem }`).
- **`logRaw()`** for QR/UX output (no prefix, no formatting).
- **Console styles** (e.g. `pretty | compact | json`).
- **Console log level** separate from the file log level (file keeps full detail when `logging.level` is set to `debug`/`trace`).
- **WhatsApp message bodies** are logged at `debug` (use `--verbose` to see them).

This keeps existing file logs stable while making interactive output scannable.

**Source**: OpenClaw documentation — `gateway/logging` (mirror `inbox/openclaw_docs/gateway/logging.md`)
**Last Updated**: 2026-06-22
**Status**: Active
