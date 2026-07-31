---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - mcp
keywords:
  - openclaw mcp serve
  - openclaw as mcp server
  - mcp channel bridge
  - bridge tools conversations_list messages_send
  - events_poll events_wait
  - claude channel mode notifications
  - mcp client config stdio
  - serve trust boundary
topics:
  - OpenClaw
  - MCP CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/mcp
access_control_group: ["general"]
---

# OpenClaw — `openclaw mcp serve` (OpenClaw as an MCP Server)

## Overview

This note covers the `openclaw mcp serve` half of the `cli/mcp` source page: running OpenClaw itself as a stdio MCP server that bridges Gateway-routed channel conversations to an external MCP client (Codex, Claude Code, or any other). It mirrors the page intro, the "Choose the right MCP path" decision table, the entire "OpenClaw as an MCP server" section (when to use, how it works, client modes, exposed conversations, usage, bridge tools, event model, Claude channel notifications, MCP client config, options, security/trust boundary, testing, troubleshooting), and "Current limits". The sibling MCP-client-registry subcommands (`list`/`add`/`set`/`doctor`/`probe`/`login`/etc.), the transport/JSON-shape schemas, and the Control UI are documented in the sibling notes linked under Related Notes.

`openclaw mcp` has two jobs: run OpenClaw as an MCP server with `openclaw mcp serve`, and manage OpenClaw-managed outbound MCP server definitions with the registry subcommands. `serve` is OpenClaw acting as an MCP server; the other subcommands are OpenClaw acting as an MCP client-side registry for MCP servers its runtimes may consume later. Use [`openclaw acp`](https://docs.openclaw.ai/cli/acp) instead when OpenClaw should host a coding harness session itself and route that runtime through ACP.

## Choose the right MCP path

OpenClaw has several MCP surfaces; pick the one that matches who owns the agent runtime and who owns the tools.

| Goal | Use | Why |
|---|---|---|
| Let an external MCP client read/send OpenClaw channel conversations | `openclaw mcp serve` | OpenClaw is the MCP server and exposes Gateway-backed conversations over stdio. |
| Save third-party MCP servers for OpenClaw-managed agent runs | `openclaw mcp add`, `set`, `configure`, `tools`, `login` | OpenClaw is the MCP client-side registry and later projects those servers into eligible runtimes. |
| Check a saved server without running an agent turn | `openclaw mcp status`, `doctor`, `probe` | `status` and `doctor` inspect config; `probe` opens a live MCP connection and lists capabilities. |
| Edit MCP config from a browser | Control UI `/mcp` | The page shows inventory, enablement, OAuth/filter summaries, command hints, and a scoped `mcp` editor. |
| Give Codex app-server a scoped native MCP server | `mcp.servers.<name>.codex` | The `codex` block only affects Codex app-server thread projection and is stripped before native config handoff. |
| Run ACP-hosted harness sessions | `openclaw acp` and ACP Agents | ACP bridge mode does not accept per-session MCP server injection; configure gateway/plugin bridges instead. |

If you are not sure which path you need, start with `openclaw mcp status --verbose` — it shows what OpenClaw has saved without starting any MCP servers.

## When to use `serve`

Use `openclaw mcp serve` when: Codex, Claude Code, or another MCP client should talk directly to OpenClaw-backed channel conversations; you already have a local or remote OpenClaw Gateway with routed sessions; or you want one MCP server that works across OpenClaw's channel backends instead of running separate per-channel bridges. Use [`openclaw acp`](https://docs.openclaw.ai/cli/acp) instead when OpenClaw should host the coding runtime itself and keep the agent session inside OpenClaw.

## How it works

`openclaw mcp serve` starts a stdio MCP server. The MCP client owns that process. While the client keeps the stdio session open, the bridge connects to a local or remote OpenClaw Gateway over WebSocket and exposes routed channel conversations over MCP. The five-step flow is: (1) the MCP client spawns `openclaw mcp serve`; (2) the bridge connects to the OpenClaw Gateway over WebSocket; (3) routed sessions become MCP conversations and transcript/history tools; (4) live events are queued in memory while the bridge is connected; (5) optionally, if Claude channel mode is enabled, the same session can also receive Claude-specific push notifications.

Important behavior of the live bridge: the live queue state starts when the bridge connects; older transcript history is read with `messages_read`; Claude push notifications only exist while the MCP session is alive; when the client disconnects, the bridge exits and the live queue is gone. One-shot agent entry points such as `openclaw agent` and `openclaw infer model run` retire any bundled MCP runtimes they open when the reply completes, so repeated scripted runs do not accumulate stdio MCP child processes. Stdio MCP servers launched by OpenClaw (bundled or user-configured) are torn down as a process tree on shutdown, so child subprocesses started by the server do not survive after the parent stdio client exits. Deleting or resetting a session disposes that session's MCP clients through the shared runtime cleanup path, so there are no lingering stdio connections tied to a removed session.

## Choose a client mode

Use the same bridge in two different ways. **Generic MCP clients** use standard MCP tools only: `conversations_list`, `messages_read`, `events_poll`, `events_wait`, `messages_send`, and the approval tools. **Claude Code** uses the standard MCP tools plus the Claude-specific channel adapter — enable `--claude-channel-mode on` or leave the default `auto`. Today, `auto` behaves the same as `on`; there is no client capability detection yet.

## What `serve` exposes

The bridge uses existing Gateway session route metadata to expose channel-backed conversations. A conversation appears when OpenClaw already has session state with a known route such as: `channel`; recipient or destination metadata; optional `accountId`; optional `threadId`. This gives MCP clients one place to: list recent routed conversations; read recent transcript history; wait for new inbound events; send a reply back through the same route; and see approval requests that arrive while the bridge is connected.

## Usage

Run the bridge against a local Gateway, a remote Gateway with token or password auth, or with verbose logging / Claude mode off:

```bash
# Local Gateway
openclaw mcp serve

# Remote Gateway (token)
openclaw mcp serve --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token

# Remote Gateway (password)
openclaw mcp serve --url wss://gateway-host:18789 --password-file ~/.openclaw/gateway.password

# Verbose / Claude off
openclaw mcp serve --verbose
openclaw mcp serve --claude-channel-mode off
```

## Bridge tools

The current bridge exposes these MCP tools:

- `conversations_list` — lists recent session-backed conversations that already have route metadata in Gateway session state. Useful filters: `limit`, `search`, `channel`, `includeDerivedTitles`, `includeLastMessage`.
- `conversation_get` — returns one conversation by `session_key` using a direct Gateway session lookup.
- `messages_read` — reads recent transcript messages for one session-backed conversation.
- `attachments_fetch` — extracts non-text message content blocks from one transcript message. This is a metadata view over transcript content, not a standalone durable attachment blob store.
- `events_poll` — reads queued live events since a numeric cursor.
- `events_wait` — long-polls until the next matching queued event arrives or a timeout expires. Use this when a generic MCP client needs near-real-time delivery without a Claude-specific push protocol.
- `messages_send` — sends text back through the same route already recorded on the session. Current behavior: requires an existing conversation route; uses the session's channel, recipient, account id, and thread id; sends text only.
- `permissions_list_open` — lists pending exec/plugin approval requests the bridge has observed since it connected to the Gateway.
- `permissions_respond` — resolves one pending exec/plugin approval request with `allow-once`, `allow-always`, or `deny`.

## Event model

The bridge keeps an in-memory event queue while it is connected. Current event types are: `message`, `exec_approval_requested`, `exec_approval_resolved`, `plugin_approval_requested`, `plugin_approval_resolved`, and `claude_permission_request`. The queue is live-only — it starts when the MCP bridge starts; `events_poll` and `events_wait` do not replay older Gateway history by themselves; durable backlog should be read with `messages_read`.

## Claude channel notifications

The bridge can also expose Claude-specific channel notifications. This is the OpenClaw equivalent of a Claude Code channel adapter: standard MCP tools remain available, but live inbound messages can also arrive as Claude-specific MCP notifications. The mode is set by `--claude-channel-mode off` (standard MCP tools only), `--claude-channel-mode on` (enable Claude channel notifications), or `--claude-channel-mode auto` (current default; same bridge behavior as `on`).

When Claude channel mode is enabled, the server advertises Claude experimental capabilities and can emit `notifications/claude/channel` and `notifications/claude/channel/permission`. Current bridge behavior: inbound `user` transcript messages are forwarded as `notifications/claude/channel`; Claude permission requests received over MCP are tracked in-memory; if the linked conversation later sends `yes abcde` or `no abcde`, the bridge converts that to `notifications/claude/channel/permission`; and these notifications are live-session only — if the MCP client disconnects, there is no push target. This is intentionally client-specific; generic MCP clients should rely on the standard polling tools.

## MCP client config

Example stdio client config:

```json
{
  "mcpServers": {
    "openclaw": {
      "command": "openclaw",
      "args": [
        "mcp",
        "serve",
        "--url",
        "wss://gateway-host:18789",
        "--token-file",
        "/path/to/gateway.token"
      ]
    }
  }
}
```

For most generic MCP clients, start with the standard tool surface and ignore Claude mode. Turn Claude mode on only for clients that actually understand the Claude-specific notification methods.

## Options

`openclaw mcp serve` supports: `--url` (string — Gateway WebSocket URL); `--token` (string — Gateway token); `--token-file` (string — read token from file); `--password` (string — Gateway password); `--password-file` (string — read password from file); `--claude-channel-mode` (`"auto" | "on" | "off"` — Claude notification mode); and `-v, --verbose` (boolean — verbose logs on stderr). Prefer `--token-file` or `--password-file` over inline secrets when possible.

## Security and trust boundary

The bridge does not invent routing. It only exposes conversations that Gateway already knows how to route. That means: sender allowlists, pairing, and channel-level trust still belong to the underlying OpenClaw channel configuration; `messages_send` can only reply through an existing stored route; approval state is live/in-memory only for the current bridge session; and bridge auth should use the same Gateway token or password controls you would trust for any other remote Gateway client. If a conversation is missing from `conversations_list`, the usual cause is not MCP configuration — it is missing or incomplete route metadata in the underlying Gateway session.

## Testing

OpenClaw ships a deterministic Docker smoke for this bridge:

```bash
pnpm test:docker:mcp-channels
```

That smoke starts a seeded Gateway container, starts a second container that spawns `openclaw mcp serve`, verifies conversation discovery / transcript reads / attachment metadata reads / live event queue behavior / outbound send routing, and validates Claude-style channel and permission notifications over the real stdio MCP bridge. This is the fastest way to prove the bridge works without wiring a real Telegram, Discord, or iMessage account into the test run. For broader testing context, see [Testing](https://docs.openclaw.ai/help/testing).

## Troubleshooting

- **No conversations returned** — usually means the Gateway session is not already routable. Confirm that the underlying session has stored channel/provider, recipient, and optional account/thread route metadata.
- **`events_poll` or `events_wait` misses older messages** — expected. The live queue starts when the bridge connects. Read older transcript history with `messages_read`.
- **Claude notifications do not show up** — check all of these: the client kept the stdio MCP session open; `--claude-channel-mode` is `on` or `auto`; the client actually understands the Claude-specific notification methods; and the inbound message happened after the bridge connected.
- **Approvals are missing** — `permissions_list_open` only shows approval requests observed while the bridge was connected. It is not a durable approval history API.

## Current limits

This page documents the bridge as shipped today. Current limits: conversation discovery depends on existing Gateway session route metadata; no generic push protocol beyond the Claude-specific adapter; no message edit or react tools yet; HTTP/SSE/streamable-http transport connects to a single remote server (no multiplexed upstream yet); and `permissions_list_open` only includes approvals observed while the bridge is connected.

**Source**: OpenClaw documentation — `cli/mcp` (mirror `inbox/openclaw_docs/cli/mcp.md`), `serve` half + Choose-the-right-MCP-path + Current limits
**Last Updated**: 2026-06-22
**Status**: Active
