---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - slash_commands
keywords:
  - openclaw slash command model
  - commands directives inline shortcuts
  - commands.allowFrom useAccessGroups
  - commands.native nativeSkills
  - directive persist vs inline hint
  - owner-only config mcp debug plugins
  - per-surface session scoping
  - acp routing standalone command
  - provider usage status
topics:
  - OpenClaw
  - Slash Commands
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/slash-commands
access_control_group: ["general"]
---

# OpenClaw — Slash Command Model, Routing, and Configuration

## Overview

This note documents the OpenClaw **slash-command model**: the three command kinds the Gateway recognizes, how a `/...` message is routed (including under an ACP session binding and the `! <cmd>` host-bash form), the `commands.*` configuration schema that gates and authorizes them, per-surface session scoping, and what `/status` reports for provider usage and runtime. It mirrors the `tools/slash-commands` page header, the "Three command types", "Configuration", "Surface notes", and "Provider usage and status" sections. The full per-command catalog (core built-ins, dock, bundled-plugin, skill commands, and the owner-only `/config` `/mcp` `/debug` `/plugins` write commands) lives in the sibling catalog note.

## Routing: Standalone Commands, Bash, and ACP Sessions

The Gateway handles commands sent as **standalone messages starting with `/`**. Host-only bash commands use `! <cmd>`, with `/bash <cmd>` as an alias. When a conversation is bound to an ACP session, normal text routes to the ACP harness, but Gateway management commands remain local: `/acp ...` always reaches the OpenClaw command handler, and `/status` plus `/unfocus` stay local whenever command handling is enabled for the surface.

## Three Command Types

OpenClaw distinguishes three kinds of `/...` input, which differ in whether they persist session settings and whether they reach the model:

1. **Commands** — standalone `/...` messages handled by the Gateway; they must be sent as the only content in the message.
2. **Directives** — `/think`, `/fast`, `/verbose`, `/trace`, `/reasoning`, `/elevated`, `/exec`, `/model`, `/queue`. Directives are stripped from the message before the model sees it. They **persist session settings when sent alone** (a directive-only message), and **act as inline hints when sent with other text** (without persisting).
3. **Inline shortcuts** — `/help`, `/commands`, `/status`, `/whoami`. They run immediately and are stripped before the model sees the remaining text. Authorized senders only.

### Directive Behavior Details

The directive rules are precise: directives are stripped from the message before the model sees it; in **directive-only** messages they persist to the session and reply with an acknowledgement; in **normal chat** messages with other text they act as inline hints and do **not** persist session settings. Directives only apply for **authorized senders** — if `commands.allowFrom` is set, it is the only allowlist used; otherwise authorization comes from channel allowlists/pairing plus `commands.useAccessGroups`. Unauthorized senders see directives treated as plain text.

## Configuration (`commands.*`)

The `commands` block gates which command surfaces are enabled, how native registration behaves, and who is authorized. The page's example configuration:

```json5
{
  commands: {
    native: "auto",
    nativeSkills: "auto",
    text: true,
    bash: false,
    bashForegroundMs: 2000,
    config: false,
    mcp: false,
    plugins: false,
    debug: false,
    restart: true,
    ownerAllowFrom: ["discord:123456789012345678"],
    ownerDisplay: "raw",
    ownerDisplaySecret: "${OWNER_ID_HASH_SECRET}",
    allowFrom: {
      "*": ["user1"],
      discord: ["user:123"],
    },
    useAccessGroups: true,
  },
}
```

### Parsing and Native Registration

- `commands.text` (boolean, default `true`) — enables parsing `/...` in chat messages. On surfaces without native commands (WhatsApp, WebChat, Signal, iMessage, Google Chat, Microsoft Teams), text commands work even when set to `false`.
- `commands.native` (`boolean | "auto"`, default `"auto"`) — registers native commands. Auto means on for Discord/Telegram, off for Slack, and ignored for providers without native support. Override per-channel with `channels.<provider>.commands.native`. On Discord, `false` skips slash-command registration; previously registered commands may stay visible until removed.
- `commands.nativeSkills` (`boolean | "auto"`, default `"auto"`) — registers skill commands natively when supported. Auto: on for Discord/Telegram, off for Slack. Override with `channels.<provider>.commands.nativeSkills`.

### Bash and Owner-Only Write Surfaces

- `commands.bash` (boolean, default `false`) — enables `! <cmd>` to run host shell commands (`/bash <cmd>` alias); requires `tools.elevated` allowlists.
- `commands.bashForegroundMs` (number, default `2000`) — how long bash waits before switching to background mode (`0` backgrounds immediately).
- `commands.config` (boolean, default `false`) — enables `/config` (reads/writes `openclaw.json`); owner-only.
- `commands.mcp` (boolean, default `false`) — enables `/mcp` (reads/writes OpenClaw-managed MCP config under `mcp.servers`); owner-only.
- `commands.plugins` (boolean, default `false`) — enables `/plugins` (plugin discovery/status plus install + enable/disable); owner-only for writes.
- `commands.debug` (boolean, default `false`) — enables `/debug` (runtime-only config overrides); owner-only.
- `commands.restart` (boolean, default `true`) — enables `/restart` and gateway restart tool actions.

### Authorization and Owner Identity

- `commands.ownerAllowFrom` (`string[]`) — explicit owner allowlist for owner-only command surfaces; separate from `commands.allowFrom` and DM pairing access.
- `channels.<channel>.commands.enforceOwnerForCommands` (boolean, default `false`) — per-channel; requires owner identity for owner-only commands. When `true`, the sender must match `commands.ownerAllowFrom` or hold internal `operator.admin` scope; a wildcard `allowFrom` entry is **not** sufficient.
- `commands.ownerDisplay` (`"raw" | "hash"`) — controls how owner ids appear in the system prompt.
- `commands.ownerDisplaySecret` (string) — HMAC secret used when `commands.ownerDisplay: "hash"`.
- `commands.allowFrom` (object) — per-provider allowlist for command authorization. When configured, it is the **only** authorization source for commands and directives. Use `"*"` for a global default; provider-specific keys override it.
- `commands.useAccessGroups` (boolean, default `true`) — enforces allowlists/policies for commands when `commands.allowFrom` is not set.

## Surface Notes (Per-Surface Session Scoping)

Where a command runs determines which session it targets. Text commands run in the normal chat session (DMs share `main`; groups have their own session). Native command sessions are surface-scoped: native Discord commands use `agent:<agentId>:discord:slash:<userId>`; native Slack commands use `agent:<agentId>:slack:slash:<userId>` (prefix configurable via `channels.slack.slashCommand.sessionPrefix`); native Telegram commands use `telegram:slash:<userId>` (targeting the chat session via `CommandTargetSessionKey`). `/stop` targets the active chat session to abort the current run.

### Slack Specifics

`channels.slack.slashCommand` supports a single `/openclaw`-style command. With `commands.native: true`, create one Slack slash command per built-in command. Register `/agentstatus` (not `/status`) because Slack reserves `/status`; text `/status` still works in Slack messages.

### Fast Path and Inline Shortcuts

Command-only messages from allowlisted senders are handled immediately (bypass queue + model). Inline shortcuts (`/help`, `/commands`, `/status`, `/whoami`) also work embedded in normal messages and are stripped before the model sees the remaining text. Unauthorized command-only messages are silently ignored; inline `/...` tokens are treated as plain text.

### Argument Notes

Commands accept an optional `:` between the command and args (`/think: high`, `/send: on`). `/new <model>` accepts a model alias, `provider/model`, or a provider name (fuzzy match); if no match, the text is treated as the message body. `/allowlist add|remove` requires `commands.config: true` and honors channel `configWrites`.

## Provider Usage and Status (`/status` Reporting)

`/status` surfaces provider and runtime reporting alongside command handling: provider usage/quota (e.g., "Claude 80% left") shows in `/status` for the current model provider when usage tracking is enabled. Token/cache lines in `/status` can fall back to the latest transcript usage entry when the live session snapshot is sparse. For execution vs runtime, `/status` reports `Execution` for the effective sandbox path and `Runtime` for who is running the session: `OpenClaw Default`, `OpenAI Codex`, a CLI backend, or an ACP backend. Per-response tokens/cost are controlled by `/usage off|tokens|full`, and `/model status` is about models/auth/endpoints, not usage.

**Source**: OpenClaw documentation — `tools/slash-commands` (mirror `inbox/openclaw_docs/tools/slash-commands.md`)
**Last Updated**: 2026-06-22
**Status**: Active
