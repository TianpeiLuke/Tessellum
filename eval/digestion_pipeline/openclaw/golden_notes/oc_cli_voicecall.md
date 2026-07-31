---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - voice_call
keywords:
  - openclaw voicecall command
  - voice call plugin cli
  - voicecall setup smoke
  - call start continue speak dtmf end status
  - voicecall tail latency calls.jsonl
  - voicecall expose tailscale funnel
  - conversation vs notify mode
  - voice webhook public url
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/voicecall
access_control_group: ["general"]
---

# OpenClaw — The `openclaw voicecall` Command

## Overview

This note documents the `openclaw voicecall` CLI command — the plugin-provided command surface for placing and operating outbound voice calls, mirroring the `cli/voicecall` source page. It covers the full subcommand set (`setup`, `smoke`, `call`, `start`, `continue`, `speak`, `dtmf`, `end`, `status`, `tail`, `latency`, `expose`), the readiness/smoke checks, the call lifecycle with each subcommand's flag table and defaults, the `calls.jsonl` log/metric inspectors, and the Tailscale serve/funnel webhook-exposure toggle. The command only appears when the voice-call plugin is installed and enabled, and operational subcommands route to a running Gateway's voice-call runtime when one is reachable.

## Command Routing (plugin-provided)

`voicecall` is a plugin-provided command: it only appears when the voice-call plugin is installed and enabled. When the Gateway is running, the operational commands (`call`, `start`, `continue`, `speak`, `dtmf`, `end`, `status`) are routed to that Gateway's voice-call runtime. If no Gateway is reachable, they fall back to a standalone CLI runtime.

## Subcommands

The full invocation surface, copied verbatim from source:

```bash
openclaw voicecall setup    [--json]
openclaw voicecall smoke    [-t <phone>] [--message <text>] [--mode <m>] [--yes] [--json]
openclaw voicecall call     -m <text> [-t <phone>] [--mode <m>]
openclaw voicecall start    --to <phone> [--message <text>] [--mode <m>]
openclaw voicecall continue --call-id <id> --message <text>
openclaw voicecall speak    --call-id <id> --message <text>
openclaw voicecall dtmf     --call-id <id> --digits <digits>
openclaw voicecall end      --call-id <id>
openclaw voicecall status   [--call-id <id>] [--json]
openclaw voicecall tail     [--file <path>] [--since <n>] [--poll <ms>]
openclaw voicecall latency  [--file <path>] [--last <n>]
openclaw voicecall expose   [--mode <m>] [--path <p>] [--port <port>] [--serve-path <p>]
```

| Subcommand | Description |
| ---------- | --------------------------------------------------------------- |
| `setup`    | Show provider and webhook readiness checks. |
| `smoke`    | Run readiness checks; place a live test call only with `--yes`. |
| `call`     | Initiate an outbound voice call. |
| `start`    | Alias for `call` with `--to` required and `--message` optional. |
| `continue` | Speak a message and wait for the next response. |
| `speak`    | Speak a message without waiting for a response. |
| `dtmf`     | Send DTMF digits to an active call. |
| `end`      | Hang up an active call. |
| `status`   | Inspect active calls (or one by `--call-id`). |
| `tail`     | Tail `calls.jsonl` (useful during provider tests). |
| `latency`  | Summarize turn-latency metrics from `calls.jsonl`. |
| `expose`   | Toggle Tailscale serve/funnel for the webhook endpoint. |

## Setup and smoke

### `setup`

`setup` prints human-readable readiness checks by default; pass `--json` for scripts. It shows provider and webhook readiness checks.

```bash
openclaw voicecall setup
openclaw voicecall setup --json
```

### `smoke`

`smoke` runs the same readiness checks. It will not place a real phone call unless both `--to` and `--yes` are present.

| Flag | Default | Description |
| ------------------ | --------------------------------- | --------------------------------------- |
| `-t, --to <phone>` | (none) | Phone number to call for a live smoke. |
| `--message <text>` | `OpenClaw voice call smoke test.` | Message to speak during the smoke call. |
| `--mode <mode>`    | `notify` | Call mode: `notify` or `conversation`. |
| `--yes`            | `false` | Actually place the live outbound call. |
| `--json`           | `false` | Print machine-readable JSON. |

```bash
openclaw voicecall smoke
openclaw voicecall smoke --to "+15555550123"        # dry run
openclaw voicecall smoke --to "+15555550123" --yes  # live notify call
```

For external providers (`twilio`, `telnyx`, `plivo`), `setup` and `smoke` require a public webhook URL from `publicUrl`, a tunnel, or Tailscale exposure. A loopback or private serve fallback is rejected because carriers cannot reach it.

## Call lifecycle

### `call`

`call` initiates an outbound voice call.

| Flag | Required | Default | Description |
| ---------------------- | -------- | ----------------- | -------------------------------------------------------------------------- |
| `-m, --message <text>` | yes | (none) | Message to speak when the call connects. |
| `-t, --to <phone>`     | no | config `toNumber` | E.164 phone number to call. |
| `--mode <mode>`        | no | `conversation` | Call mode: `notify` (hang up after message) or `conversation` (stay open). |

```bash
openclaw voicecall call --to "+15555550123" --message "Hello"
openclaw voicecall call -m "Heads up" --mode notify
```

### `start`

`start` is an alias for `call` with a different default flag shape (`--to` required, `--message` optional).

| Flag | Required | Default | Description |
| ------------------ | -------- | -------------- | ---------------------------------------- |
| `--to <phone>`     | yes | (none) | Phone number to call. |
| `--message <text>` | no | (none) | Message to speak when the call connects. |
| `--mode <mode>`    | no | `conversation` | Call mode: `notify` or `conversation`. |

### `continue`

`continue` speaks a message and waits for a response.

| Flag | Required | Description |
| ------------------ | -------- | ----------------- |
| `--call-id <id>`   | yes | Call ID. |
| `--message <text>` | yes | Message to speak. |

### `speak`

`speak` speaks a message without waiting for a response.

| Flag | Required | Description |
| ------------------ | -------- | ----------------- |
| `--call-id <id>`   | yes | Call ID. |
| `--message <text>` | yes | Message to speak. |

### `dtmf`

`dtmf` sends DTMF digits to an active call.

| Flag | Required | Description |
| ------------------- | -------- | ----------------------------------------- |
| `--call-id <id>`    | yes | Call ID. |
| `--digits <digits>` | yes | DTMF digits (e.g. `ww123456#` for waits). |

### `end`

`end` hangs up an active call.

| Flag | Required | Description |
| ---------------- | -------- | ----------- |
| `--call-id <id>` | yes | Call ID. |

### `status`

`status` inspects active calls (or one by `--call-id`).

| Flag | Default | Description |
| ---------------- | ------- | ---------------------------- |
| `--call-id <id>` | (none) | Restrict output to one call. |
| `--json`         | `false` | Print machine-readable JSON. |

```bash
openclaw voicecall status
openclaw voicecall status --json
openclaw voicecall status --call-id <id>
```

## Logs and metrics

### `tail`

`tail` tails the voice-call JSONL log. It prints the last `--since` lines on start, then streams new lines as they are written. It is useful during provider tests.

| Flag | Default | Description |
| --------------- | -------------------------- | ------------------------------ |
| `--file <path>` | resolved from plugin store | Path to `calls.jsonl`. |
| `--since <n>`   | `25` | Lines to print before tailing. |
| `--poll <ms>`   | `250` (minimum 50) | Poll interval in milliseconds. |

### `latency`

`latency` summarizes turn-latency and listen-wait metrics from `calls.jsonl`. Output is JSON with `recordsScanned`, `turnLatency`, and `listenWait` summaries.

| Flag | Default | Description |
| --------------- | -------------------------- | ------------------------------------ |
| `--file <path>` | resolved from plugin store | Path to `calls.jsonl`. |
| `--last <n>`    | `200` (minimum 1) | Number of recent records to analyze. |

## Exposing webhooks

### `expose`

`expose` enables, disables, or changes the Tailscale serve/funnel configuration for the voice webhook.

| Flag | Default | Description |
| --------------------- | ----------------------------------------- | ----------------------------------------------- |
| `--mode <mode>`       | `funnel` | `off`, `serve` (tailnet), or `funnel` (public). |
| `--path <path>`       | config `tailscale.path` or `--serve-path` | Tailscale path to expose. |
| `--port <port>`       | config `serve.port` or `3334` | Local webhook port. |
| `--serve-path <path>` | config `serve.path` or `/voice/webhook` | Local webhook path. |

```bash
openclaw voicecall expose --mode serve
openclaw voicecall expose --mode funnel
openclaw voicecall expose --mode off
```

Only expose the webhook endpoint to networks you trust. Prefer Tailscale Serve over Funnel when possible.

**Source**: OpenClaw documentation — `cli/voicecall` (mirror `inbox/openclaw_docs/cli/voicecall.md`)
**Last Updated**: 2026-06-22
**Status**: Active
