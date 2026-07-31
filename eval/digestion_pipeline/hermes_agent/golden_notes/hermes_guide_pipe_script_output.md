---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - messaging
keywords:
  - hermes send
  - scriptable cross-platform notifier
  - target format grammar
  - body resolution order
  - unix exit codes
  - gateway-free delivery
topics:
  - Hermes Agent
  - Automation & Bots
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/pipe-script-output
access_control_group: ["general"]
---

# Hermes Agent — Guide: Pipe Script Output to Messaging Platforms

## Overview

`hermes send` is a small, scriptable CLI that pushes a message to any messaging platform Hermes is already configured for — think of it as a **cross-platform `curl` for notifications**. The defining property is that it needs *no running gateway*, *no LLM*, and *no re-pasting of bot tokens*: it reuses the same credentials and platform adapters that `hermes gateway` already uses, so there is no second configuration surface to maintain. This guide is the procedural reference for wiring `hermes send` into shell scripts, cron jobs, CI hooks, and monitoring daemons.

It is the simplest delivery surface in the Hermes automation toolkit. Use it for system monitoring (memory, disk, GPU temp, long-running job finished), CI/CD notifications (deploy done, test failure), cron scripts that need to ping you with results, quick one-shot terminal messages, and piping any tool's output anywhere (`make | hermes send --to slack:#builds`). The deeper subsystems it leans on — the delivery router, the channel directory, and the per-platform REST adapters — are owned by their own reference pages and are linked, not re-explained here. The §Comparison section positions `hermes send` against raw `curl`, cron `--deliver`, and the in-agent `send_message` tool so you can pick the right surface for each job.

## Quick Start

The fastest path is a one-liner. The body can be a positional string, piped stdin, or a file, and the target can be a bare platform (home channel) or a fully-qualified chat/thread:

```bash
# Plain text to the home channel for a platform
hermes send --to telegram "deploy finished"

# Pipe in stdout from anything
echo "RAM 92%" | hermes send --to telegram:-1001234567890

# Send a file
hermes send --to discord:#ops --file /tmp/report.md

# Attach a subject/header line
hermes send --to slack:#eng --subject "[CI] build.log" --file build.log

# Thread target (Telegram topic, Discord thread)
hermes send --to telegram:-1001234567890:17585 "threaded reply"

# List every configured target / filter by platform
hermes send --list
hermes send --list telegram
```

## Argument Reference

| Flag | Description |
|------|-------------|
| `-t, --to TARGET` | Destination. See Target Formats below. |
| `message` (positional) | Message text. Omit to read from `--file` or stdin. |
| `-f, --file PATH` | Read the body from a file. `--file -` forces stdin. |
| `-s, --subject LINE` | Prepend a header/subject line before the body. |
| `-l, --list` | List available targets. Optional positional platform filter. |
| `-q, --quiet` | No stdout on success (exit code only — ideal for scripts). |
| `--json` | Emit the raw JSON result of the send. |
| `-h, --help` | Show the built-in help text. |

### Target Formats

The `--to` value is a colon-delimited grammar `platform[:chat[:thread]]`, with two special chat forms — a human-friendly `#channel` name and a `+E164` phone address:

| Format | Example | Meaning |
|--------|---------|---------|
| `platform` | `telegram` | Send to the platform's configured home channel |
| `platform:chat_id` | `telegram:-1001234567890` | Specific numeric chat / group / user |
| `platform:chat_id:thread_id` | `telegram:-1001234567890:17585` | Specific thread or Telegram forum topic |
| `platform:#channel` | `discord:#ops` | Human-friendly channel name (resolved against the channel directory) |
| `platform:+E164` | `signal:+15551234567` | Phone-addressed platforms: Signal, SMS, WhatsApp |

Any platform Hermes ships adapters for works as a target: `telegram`, `discord`, `slack`, `signal`, `sms`, `whatsapp`, `matrix`, `mattermost`, `feishu`, `dingtalk`, `wecom`, `weixin`, `email`, and others.

### Exit Codes

`hermes send` follows the standard Unix exit-code convention so scripts can branch on the result the same way they would on `curl` or `grep`:

| Code | Meaning |
|------|---------|
| `0` | Send (or list) succeeded |
| `1` | Delivery failed at the platform level (auth, permissions, network) |
| `2` | Usage / argument / config error |

## Message Body Resolution

The message body is resolved in a fixed precedence order — the first source present wins:

1. **Positional argument** — `hermes send --to telegram "hi"`
2. **`--file PATH`** — `hermes send --to telegram --file msg.txt`
3. **Piped stdin** — `echo hi | hermes send --to telegram`

A critical guard: when stdin is a TTY (no pipe), Hermes does **not** wait for input — it returns a clear usage error instead. This keeps scripts from hanging indefinitely if they accidentally omit the body.

## Real-World Examples

The same portable line replaces ad-hoc per-platform `curl` calls across monitoring, CI/CD, cron, long-running-task, and scripted-result use cases. Because the command reuses your Hermes config, an identical script works on any host where Hermes is installed — no manual bot-token export per machine. Two representative scripts (memory watchdog with a subject header; deterministic `--quiet`/`--json` scripting) capture the load-bearing patterns:

```bash
#!/usr/bin/env bash
# Monitoring: memory alert with a subject header line
ram_pct=$(free | awk '/^Mem:/ {printf "%d", $3 * 100 / $2}')
if [ "$ram_pct" -ge 85 ]; then
  hermes send --to telegram --subject "⚠ MEMORY WARNING" \
    "RAM ${ram_pct}% on $(hostname)"
fi
```

```bash
# Scripting: hard-fail on delivery failure; capture the message id via --json
hermes send --to telegram --quiet "keepalive" || {
  echo "Telegram delivery failed" >&2
  exit 1
}
msg_id=$(hermes send --to discord:#ops --json "build started" | jq -r .message_id)
```

The remaining source examples follow the same shape: a **CI/CD** branch sends `✅ ${CI_COMMIT_SHA:0:7} deployed` on success or pipes `tail -n 100 deploy.log` to `slack:#deploys` with a failure subject on error; a **cron** crontab entry pipes `generate-metrics.sh` output to `hermes send --to telegram --subject "Daily metrics $(date +%Y-%m-%d)"`; and a **long-running task** chains `./train.py … && hermes send --to telegram "training done" || hermes send --to telegram "training failed (exit $?)"`.

> **Watchdog caveat (don't alert the gateway about itself):** for watchdogs that might fire when the gateway itself is struggling (OOM alerts, disk-full alerts), keep using a minimal `curl` call instead of `hermes send`. If the Python interpreter can't load because the box is thrashing, you still want that alert to go out.

## Does `hermes send` Need the Gateway Running?

**Usually no.** For any bot-token platform — Telegram, Discord, Slack, Signal, SMS, WhatsApp Cloud API, and most others — `hermes send` calls the platform's REST endpoint directly using credentials from `~/.hermes/.env` and `~/.hermes/config.yaml`. It is a standalone subprocess that exits as soon as the message is delivered.

A live gateway is only required for **plugin platforms** that rely on a persistent adapter connection (for example, a custom plugin that keeps a long-lived WebSocket open). In that case you get a clear error pointing at the gateway; start it with `hermes gateway start` and retry.

## Listing and Discovering Targets

Before sending to a specific channel you can inspect what's available — every target, a per-platform filter, or machine-readable JSON:

```bash
hermes send --list             # every target across every configured platform
hermes send --list telegram    # just Telegram targets
hermes send --list --json      # machine-readable
```

The listing is built from `~/.hermes/channel_directory.json`, which the gateway refreshes every few minutes while it is running. If you see "no channels discovered yet", start the gateway once (`hermes gateway start`) so it can populate the cache. Human-friendly names (`discord:#ops`, `slack:#engineering`) are resolved against this cache at send time, so you don't need to memorize numeric IDs.

## Comparison with Other Approaches

`hermes send` is intentionally the simplest possible surface. The source's decision table contrasts it with raw `curl`, scheduled cron delivery, and the in-agent send tool:

| Approach | Multi-platform | Reuses Hermes creds | Needs gateway | Best for |
|----------|----------------|---------------------|---------------|----------|
| `hermes send` | ✅ | ✅ | No (bot-token) | Everything below |
| Raw `curl` to each platform | Each scripted separately | Manual | No | Critical watchdogs |
| `cron` job with `--deliver` | ✅ | ✅ | No | Scheduled agent tasks |
| `send_message` agent tool | ✅ | ✅ | No | Inside an agent loop |

The decision rule: if you need an **agent to decide what to say**, use the `send_message` tool from within a chat or cron job; if you need a **scheduled run with LLM-generated content**, use `cronjob(action='create', prompt=...)` with `deliver='telegram:...'`; if you just need to **pipe a raw string**, reach for `hermes send`.

**Source**: `inbox/hermes_agent_docs/guides/pipe-script-output.md` · https://hermes-agent.nousresearch.com/docs/guides/pipe-script-output
**Last Updated**: 2026-06-19
**Status**: Active
