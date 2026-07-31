---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - agent_send
keywords:
  - openclaw agent send cli
  - openclaw agent command single turn
  - agent-send scripted agent turn
  - session-key agent id resolution
  - deliver reply channel slack whatsapp
  - local embedded runtime fallback
  - thinking verbose flags persist session
  - json delivery status output
topics:
  - OpenClaw
  - Agent Tools
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/agent-send
access_control_group: ["general"]
---

# OpenClaw — `agent-send`: One-Shot Agent Turns from the CLI

## Overview

This note is the operator procedure for the OpenClaw `agent-send` tool — the `openclaw agent` command that runs a single agent turn from the command line without an inbound chat message. It mirrors the `tools/agent-send` source page: the quick-start invocations, the full flag table, the turn behavior (Gateway-vs-local routing, session-key resolution, flag persistence, output modes), and worked examples. Use `agent-send` for scripted workflows, testing, and programmatic delivery, including optionally delivering the generated reply to a chat channel.

## Quick start

`openclaw agent` sends the message through the Gateway and prints the reply. The page documents three escalating usages.

Run a simple agent turn:

```bash
openclaw agent --agent main --message "What is the weather today?"
```

Target a specific agent or session — by configured agent id, by a `--to` destination that derives the session key, by reusing an existing `--session-id`, or by an exact `--session-key`:

```bash
# Target a specific agent
openclaw agent --agent ops --message "Summarize logs"

# Target a phone number (derives session key)
openclaw agent --to +15555550123 --message "Status update"

# Reuse an existing session
openclaw agent --session-id abc123 --message "Continue the task"

# Target an exact session key
openclaw agent --session-key agent:ops:incident-42 --message "Summarize status"
```

Deliver the reply to a channel — `--deliver` sends the reply to a chat channel (WhatsApp is the default channel), and `--reply-channel` / `--reply-to` override the destination:

```bash
# Deliver to WhatsApp (default channel)
openclaw agent --to +15555550123 --message "Report ready" --deliver

# Deliver to Slack
openclaw agent --agent ops --message "Generate report" \
  --deliver --reply-channel slack --reply-to "#reports"
```

## Flags

The page documents the following flags (`--message` is the only required flag):

| Flag | Description |
| --- | --- |
| `--message <text>` | Message to send (required) |
| `--to <dest>` | Derive session key from a target (phone, chat id) |
| `--session-key <key>` | Use an explicit session key |
| `--agent <id>` | Target a configured agent (uses its `main` session) |
| `--session-id <id>` | Reuse an existing session by id |
| `--local` | Force local embedded runtime (skip Gateway) |
| `--deliver` | Send the reply to a chat channel |
| `--channel <name>` | Delivery channel (whatsapp, telegram, discord, slack, etc.) |
| `--reply-to <target>` | Delivery target override |
| `--reply-channel <name>` | Delivery channel override |
| `--reply-account <id>` | Delivery account id override |
| `--thinking <level>` | Set thinking level for the selected model profile |
| `--verbose <on\|full\|off>` | Set verbose level |
| `--timeout <seconds>` | Override agent timeout |
| `--json` | Output structured JSON |

## Behavior

- **Routing**: by default the CLI goes **through the Gateway**; add `--local` to force the embedded runtime on the current machine. If the Gateway is unreachable, the CLI **falls back** to the local embedded run.
- **Session selection via `--to`**: `--to` derives the session key — group/channel targets preserve isolation, while direct chats collapse to `main`.
- **Session selection via `--session-key`**: `--session-key` selects an explicit key. Agent-prefixed keys must use the form `agent:<agent-id>:<session-key>`, and `--agent` must match that agent id when both are supplied. Bare non-sentinel keys are scoped to `--agent` when supplied — for example, `--agent ops --session-key incident-42` routes to `agent:ops:incident-42`. Without `--agent`, bare non-sentinel keys are scoped to the configured default agent. The literal keys `global` and `unknown` remain unscoped only when no `--agent` is supplied; in that case, embedded fallback and store ownership use the configured default agent.
- **Flag persistence**: thinking and verbose flags persist into the session store.
- **Output**: plain text by default, or `--json` for a structured payload plus metadata.
- **JSON delivery status**: with `--json --deliver`, the JSON includes delivery status for sent, suppressed, partial, and failed sends (see the `/cli/agent` JSON delivery-status reference).

## Examples

The page's worked examples combine the flags above for scripted invocation:

```bash
# Simple turn with JSON output
openclaw agent --to +15555550123 --message "Trace logs" --verbose on --json

# Turn with thinking level
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium

# Exact session key
openclaw agent --session-key agent:ops:incident-42 --message "Summarize status"

# Legacy key scoped to an agent
openclaw agent --agent ops --session-key incident-42 --message "Summarize status"

# Deliver to a different channel than the session
openclaw agent --agent ops --message "Alert" --deliver --reply-channel telegram --reply-to "@admin"
```

**Source**: OpenClaw documentation — `tools/agent-send` (mirror `inbox/openclaw_docs/tools/agent-send.md`)
**Last Updated**: 2026-06-22
**Status**: Active
