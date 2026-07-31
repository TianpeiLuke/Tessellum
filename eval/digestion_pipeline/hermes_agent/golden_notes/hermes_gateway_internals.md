---
tags:
  - resource
  - documentation
  - hermes_agent
  - gateway
  - messaging
keywords:
  - gateway runner boot
  - session key format
  - two-level message guard
  - multi-layer authorization
  - dm pairing flow
  - platform adapters token locks
  - gateway hook events
  - memory provider flush lifecycle
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals
access_control_group: ["general"]
---

# Hermes Agent — Gateway Internals

## Overview

The Hermes messaging gateway is the long-running process that connects one `AIAgent` to 20+ external messaging platforms (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, email, SMS, and more) through a unified architecture. A single `GatewayRunner` boots one adapter per configured platform, normalizes every inbound event into a `MessageEvent`, resolves a routing-encoded session key, authorizes the sender, dispatches slash commands or spawns an `AIAgent` per message, and delivers the response back through the originating (or an explicitly targeted) platform — all while running periodic background maintenance (cron ticking, session expiry, memory flush, cache refresh). This note documents *how that runtime behaves*; the per-platform setup pages live in the messaging user guide, and the concrete session store lives in [hermes_session_storage](hermes_session_storage.md).

## Key Files

| File | Purpose |
|------|---------|
| `gateway/run.py` | `GatewayRunner` — main loop, slash commands, message dispatch (large file) |
| `gateway/session.py` | `SessionStore` — conversation persistence and session key construction |
| `gateway/delivery.py` | Outbound message delivery to target platforms/channels |
| `gateway/pairing.py` | DM pairing flow for user authorization |
| `gateway/channel_directory.py` | Maps chat IDs to human-readable names for cron delivery |
| `gateway/hooks.py` | Hook discovery, loading, and lifecycle event dispatch |
| `gateway/mirror.py` | Cross-session message mirroring for `send_message` |
| `gateway/status.py` | Token lock management for profile-scoped gateway instances |
| `gateway/builtin_hooks/` | Extension point for always-registered hooks (none shipped) |
| `gateway/platforms/` | Platform adapters (one per messaging platform) |

## Architecture Overview

All platform adapters feed a single `_handle_message()` dispatch path inside the `GatewayRunner`, which branches into slash-command dispatch, `AIAgent` creation, or queue/background sessions, then persists conversation state to the SQLite `SessionStore`:

```text
┌─────────────────────────────────────────────────┐
│                  GatewayRunner                  │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Telegram │  │ Discord  │  │  Slack   │       │
│  │ Adapter  │  │ Adapter  │  │ Adapter  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │             │             │
│       └─────────────┼─────────────┘             │
│                     ▼                           │
│              _handle_message()                  │
│                     │                           │
│         ┌───────────┼───────────┐               │
│         ▼           ▼           ▼               │
│  Slash command   AIAgent    Queue/BG            │
│    dispatch      creation   sessions            │
│                     │                           │
│                     ▼                           │
│                 SessionStore                    │
│              (SQLite persistence)               │
└───────┴─────────────┴─────────────┴─────────────┘
```

## Message Flow

When a message arrives from any platform:

1. **Platform adapter** receives the raw event and normalizes it into a `MessageEvent`.
2. **Base adapter** checks the active session guard: if an agent is running for this session it queues the message and sets an interrupt event, while `/approve`, `/deny`, and `/stop` bypass the guard (dispatched inline).
3. **`GatewayRunner._handle_message()`** receives the event, resolves the session key via `_session_key_for_source()`, checks authorization, intercepts slash commands (and running-agent commands like `/stop`/`/status`), and otherwise creates an `AIAgent` instance to run the conversation.
4. **Response** is sent back through the platform adapter.

### Session Key Format

Session keys encode the full routing context and **must never be constructed manually** — always use `build_session_key()` from `gateway/session.py`:

```text
agent:main:{platform}:{chat_type}:{chat_id}
```

For example: `agent:main:telegram:private:123456789`. Thread-aware platforms (Telegram forum topics, Discord threads, Slack threads) may include thread IDs in the `chat_id` portion.

### Two-Level Message Guard

When an agent is actively running, incoming messages pass through two sequential guards:

1. **Level 1 — Base adapter** (`gateway/platforms/base.py`): checks `_active_sessions`; if the session is active it queues the message in `_pending_messages` and sets an interrupt event, catching messages *before* they reach the gateway runner.
2. **Level 2 — Gateway runner** (`gateway/run.py`): checks `_running_agents`, intercepts specific commands (`/stop`, `/new`, `/queue`, `/status`, `/approve`, `/deny`), and routes everything else to `running_agent.interrupt()`.

Commands that must reach the runner while the agent is blocked (like `/approve`) are dispatched **inline** via `await self._message_handler(event)`, bypassing the background task system to avoid race conditions.

## Authorization

The gateway uses a multi-layer authorization check, evaluated in order:

1. **Per-platform allow-all flag** (e.g., `TELEGRAM_ALLOW_ALL_USERS`) — if set, all users on that platform are authorized.
2. **Platform allowlist** (e.g., `TELEGRAM_ALLOWED_USERS`) — comma-separated user IDs.
3. **DM pairing** — authenticated users can pair new users via a pairing code.
4. **Global allow-all** (`GATEWAY_ALLOW_ALL_USERS`) — if set, all users across all platforms are authorized.
5. **Default: deny** — unauthorized users are rejected.

### DM Pairing Flow

An admin issues `/pair`, the gateway returns a one-time pairing code, the new user sends the code back, and the gateway marks them authorized. Pairing state is persisted in `gateway/pairing.py` and survives restarts.

## Slash Command Dispatch

All slash commands flow through the same resolution pipeline: `resolve_command()` from `hermes_cli/commands.py` maps input to a canonical name (handling aliases and prefix matching), the canonical name is checked against `GATEWAY_KNOWN_COMMANDS`, the handler in `_handle_message()` dispatches on it, and some commands are gated on config via `gateway_config_gate` on the `CommandDef`.

### Running-Agent Guard

Commands that must NOT execute while the agent is processing are rejected early; bypass commands (`/stop`, `/new`, `/approve`, `/deny`, `/queue`, `/status`) have special handling:

```python
if _quick_key in self._running_agents:
    if canonical == "model":
        return "⏳ Agent is running — wait for it to finish or /stop first."
```

## Config Sources

The gateway reads configuration from `~/.hermes/.env` (API keys, bot tokens, platform credentials), `~/.hermes/config.yaml` (model settings, tool configuration, display options), and environment variables (overriding either). Unlike the CLI — which uses `load_cli_config()` with hardcoded defaults — the gateway reads `config.yaml` directly via a YAML loader, so config keys present in the CLI's defaults dict but absent from the user's file may behave differently between CLI and gateway.

## Platform Adapters

Each messaging platform has an adapter in `gateway/platforms/` (base `base.py` plus `telegram.py`, `discord.py`, `slack.py`, `whatsapp.py`, `signal.py`, `matrix.py`, `mattermost.py`, `email.py`, `sms.py`, `dingtalk.py`, `feishu.py`, `wecom.py`, `weixin.py`, `bluebubbles.py`, the `qqbot/` sub-package, `yuanbao.py`, `feishu_comment.py`, `msgraph_webhook.py`, `webhook.py`, `api_server.py`, and `homeassistant.py`). Adapters implement a common interface: `connect()` / `disconnect()` for lifecycle management, `send_message()` for outbound delivery, and `on_message()` for normalizing inbound events into a `MessageEvent`.

### Token Locks

Adapters that connect with unique credentials call `acquire_scoped_lock()` in `connect()` and `release_scoped_lock()` in `disconnect()`. This prevents two profiles from using the same bot token simultaneously.

## Delivery Path

Outgoing deliveries (`gateway/delivery.py`) handle a **direct reply** back to the originating chat, **home channel delivery** routing cron-job outputs and background results to a configured home channel, **explicit target delivery** via the `send_message` tool (e.g., `telegram:-1001234567890`) or the `hermes send` CLI wrapping the same tool for shell scripts, and **cross-platform delivery** to a different platform than the originating message. Cron job deliveries are NOT mirrored into gateway session history — they live in their own cron session only, a deliberate design choice to avoid message-alternation violations.

## Hooks

Gateway hooks are Python modules that respond to lifecycle events:

| Event | When fired |
|-------|-----------|
| `gateway:startup` | Gateway process starts |
| `session:start` | New conversation session begins |
| `session:end` | Session completes or times out |
| `session:reset` | User resets session with `/new` |
| `agent:start` | Agent begins processing a message |
| `agent:step` | Agent completes one tool-calling iteration |
| `agent:end` | Agent finishes and returns response |
| `command:*` | Any slash command is executed |

Hooks are discovered from `gateway/builtin_hooks/` (an extension point, currently empty in the shipped distribution — `_register_builtin_hooks()` is a no-op stub) and from `~/.hermes/hooks/` (user-installed). Each hook is a directory with a `HOOK.yaml` manifest and `handler.py`.

## Memory Provider Integration

When a memory provider plugin (e.g., Honcho) is enabled, the gateway creates an `AIAgent` per message with the session ID, the `MemoryManager` initializes the provider with the session context, and provider tools (e.g., `honcho_profile`, `viking_search`) are routed through the tool-invocation chain:

```text
AIAgent._invoke_tool()
  → self._memory_manager.handle_tool_call(name, args)
    → provider.handle_tool_call(name, args)
```

On session end/reset, `on_session_end()` fires for cleanup and a final data flush.

### Memory Flush Lifecycle

When a session is reset, resumed, or expires: built-in memories are flushed to disk, the memory provider's `on_session_end()` hook fires, a temporary `AIAgent` runs a memory-only conversation turn, and the context is then discarded or archived.

## Background Maintenance

The gateway runs periodic maintenance alongside message handling: **cron ticking** (checks job schedules and fires due jobs), **session expiry** (cleans up abandoned sessions after timeout), **memory flush** (proactively flushes memory before session expiry), and **cache refresh** (refreshes model lists and provider status).

## Process Management

The gateway runs as a long-lived process managed via `hermes gateway start` / `hermes gateway stop` (manual control), `systemctl` (Linux) or `launchctl` (macOS) for service management, and a PID file at `~/.hermes/gateway.pid` for profile-scoped process tracking. **Profile-scoped vs global**: `start_gateway()` uses profile-scoped PID files and `hermes gateway stop` stops only the current profile's gateway, while `hermes gateway stop --all` uses a global `ps aux` scan to kill all gateway processes (used during updates).

**Source**: `inbox/hermes_agent_docs/developer-guide/gateway-internals.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals
**Last Updated**: 2026-06-19
**Status**: Active
