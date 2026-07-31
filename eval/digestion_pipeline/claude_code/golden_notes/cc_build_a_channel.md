---
tags:
  - resource
  - documentation
  - claude_code
  - channels
  - mcp
keywords:
  - build a channel
  - webhook receiver
  - claude/channel capability
  - notifications/claude/channel
  - stdio transport
  - mcp server channel
  - notification format
  - channel content meta
  - development flag
  - package channel as plugin
topics:
  - Claude Code
  - Channels
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/channels-reference
access_control_group: ["general"]
---

# Build a One-Way Channel (Webhook Receiver)

## Overview

A **channel** is an MCP server that Claude Code spawns as a stdio subprocess and that **pushes** events into the running session. This note is the build-your-own walkthrough for a **one-way** channel: a single-file server that forwards external events (a CI failure, a monitoring alert, a `curl` POST) into Claude's context so Claude can act on them. To make a channel two-way (send messages back), add a [reply tool](https://code.claude.com/docs/en/channels-reference#expose-a-reply-tool); to forward tool-approval prompts to a remote device, add the [permission relay](cc_channel_permission_relay.md).

The contract has three obligations and two payload fields. The server must declare the `claude/channel` capability, emit `notifications/claude/channel` events, and connect over stdio. Each event carries a `content` string (the body of a `<channel>` tag) and an optional `meta` map (each entry becomes a tag attribute). The only hard dependency is the `@modelcontextprotocol/sdk` package on a Node.js-compatible runtime.

## What You Need

The only hard requirement is the [`@modelcontextprotocol/sdk`](https://www.npmjs.com/package/@modelcontextprotocol/sdk) package and a Node.js-compatible runtime — Bun, Node, and Deno all work. The pre-built research-preview plugins use Bun, but your channel does not have to.

Your server needs to do three things:

1. **Declare the `claude/channel` capability** so Claude Code registers a notification listener.
2. **Emit `notifications/claude/channel` events** when something happens.
3. **Connect over stdio transport** — Claude Code spawns your server as a subprocess.

During the research preview, custom channels are not on the approved allowlist, so use `--dangerously-load-development-channels` to test locally (see [Test During the Research Preview](#test-during-the-research-preview)).

## Example: Build a Webhook Receiver

This walkthrough builds a single-file server that listens for HTTP requests and forwards them into your session. By the end, anything that can send an HTTP POST — a CI pipeline, a monitoring alert, or a `curl` command — can push events to Claude. The example uses Bun for its built-in HTTP server and TypeScript support; Node or Deno work too, the only requirement being the MCP SDK.

**Step 1 — Create the project.** Make a directory and install the MCP SDK:

```bash
mkdir webhook-channel && cd webhook-channel
bun add @modelcontextprotocol/sdk
```

**Step 2 — Write the channel server.** Create `webhook.ts`. This is the entire channel server: it connects to Claude Code over stdio and listens for HTTP POSTs on port 8788. When a request arrives, it pushes the body to Claude as a channel event.

```ts
#!/usr/bin/env bun
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

// Create the MCP server and declare it as a channel
const mcp = new Server(
  { name: 'webhook', version: '0.0.1' },
  {
    // this key is what makes it a channel — Claude Code registers a listener for it
    capabilities: { experimental: { 'claude/channel': {} } },
    // added to Claude's system prompt so it knows how to handle these events
    instructions: 'Events from the webhook channel arrive as <channel source="webhook" ...>. They are one-way: read them and act, no reply expected.',
  },
)

// Connect to Claude Code over stdio (Claude Code spawns this process)
await mcp.connect(new StdioServerTransport())

// Start an HTTP server that forwards every POST to Claude
Bun.serve({
  port: 8788,  // any open port works
  // localhost-only: nothing outside this machine can POST
  hostname: '127.0.0.1',
  async fetch(req) {
    const body = await req.text()
    await mcp.notification({
      method: 'notifications/claude/channel',
      params: {
        content: body,  // becomes the body of the <channel> tag
        // each key becomes a tag attribute, e.g. <channel path="/" method="POST">
        meta: { path: new URL(req.url).pathname, method: req.method },
      },
    })
    return new Response('ok')
  },
})
```

The file does three things in order: **server configuration** (creates the MCP server with `claude/channel` in its capabilities — what tells Claude Code this is a channel — and an `instructions` string that goes into Claude's system prompt); **stdio connection** (connects over stdin/stdout, standard for any MCP server Claude Code spawns as a subprocess); and an **HTTP listener** (a local web server on port 8788 whose every POST body is forwarded to Claude via `mcp.notification()`). The listener needs the `mcp` instance, so it runs in the same process.

**Step 3 — Register your server with Claude Code.** Add the server to your MCP config so Claude Code knows how to start it. For a project-level `.mcp.json` in the same directory, use a relative path; for user-level config in `~/.claude.json`, use the full absolute path so the server can be found from any project:

```json
{
  "mcpServers": {
    "webhook": { "command": "bun", "args": ["./webhook.ts"] }
  }
}
```

Claude Code reads your MCP config at startup and spawns each server as a subprocess. (The `.mcp.json` format and MCP config layering are detailed in [the MCP page](https://code.claude.com/docs/en/mcp).)

**Step 4 — Test it.** Because custom channels are not on the research-preview allowlist, start Claude Code with the development flag:

```bash
claude --dangerously-load-development-channels server:webhook
```

The first time you start a session in this project, Claude Code asks for consent before using the new server from `.mcp.json` ("New MCP server found in this project: webhook" — select **Use this MCP server**). On startup Claude Code reads the config, spawns `webhook.ts` as a subprocess, and the HTTP listener starts automatically on the configured port — you do not run the server yourself. A dim notice confirms the channel is registered. If you see "blocked by org policy," an admin must [enable channels](https://code.claude.com/docs/en/channels#enterprise-controls) first.

In a separate terminal, simulate a webhook with an HTTP POST. The payload then arrives in your session wrapped in a `<channel>` tag, and Claude acts on it without sending anything back (this is a one-way channel):

```bash
curl -X POST localhost:8788 -d "build failed on main: https://ci.example.com/run/1234"
# arrives as:
# <channel source="webhook" path="/" method="POST">build failed on main: https://ci.example.com/run/1234</channel>
```

If the event does not arrive: when `curl` succeeds but nothing reaches Claude, run `/mcp` to check the server's status ("Failed to connect" usually means a dependency or import error; check `~/.claude/debug/<session-id>.txt`). When `curl` fails with "connection refused," the port is not bound yet or a stale process holds it — `lsof -i :<port>` shows what is listening, then `kill` it before restarting.

## Test During the Research Preview

During the research preview every channel must be on the approved allowlist to register. The `--dangerously-load-development-channels` flag bypasses the allowlist for specific entries after a confirmation prompt. It accepts two entry types — a plugin you are developing (`plugin:yourplugin@yourmarketplace`) or a bare `.mcp.json` server with no plugin wrapper yet (`server:webhook`). The bypass is **per-entry**: combining the flag with `--channels` does not extend the bypass to the `--channels` entries. The flag skips the **allowlist only** — the `channelsEnabled` organization policy still applies, and the docs warn against using it to run channels from untrusted sources.

## Server Options

A channel sets these options in the `Server` constructor. `instructions` and `capabilities.tools` are standard MCP; `capabilities.experimental['claude/channel']` and `['claude/channel/permission']` are the channel-specific additions:

| Field | Type | Description |
| :--- | :--- | :--- |
| `capabilities.experimental['claude/channel']` | `object` | Required. Always `{}`. Presence registers the notification listener. |
| `capabilities.experimental['claude/channel/permission']` | `object` | Optional. Always `{}`. Declares the channel can receive permission-relay requests (see [permission relay](cc_channel_permission_relay.md)). |
| `capabilities.tools` | `object` | Two-way only. Always `{}`. Standard MCP tool capability (see [reply tool](https://code.claude.com/docs/en/channels-reference#expose-a-reply-tool)). |
| `instructions` | `string` | Recommended. Added to Claude's system prompt: tell Claude what events to expect, what the `<channel>` tag attributes mean, whether to reply, and which tool/attribute to pass back (like `chat_id`). |

To create a one-way channel, omit `capabilities.tools`. To push an event, call `mcp.notification()` with method `notifications/claude/channel`.

## Notification Format

Your server emits `notifications/claude/channel` with two params:

| Field | Type | Description |
| :--- | :--- | :--- |
| `content` | `string` | The event body. Delivered as the body of the `<channel>` tag. |
| `meta` | `Record<string, string>` | Optional. Each entry becomes an attribute on the `<channel>` tag for routing context (chat ID, sender name, alert severity). Keys must be identifiers — letters, digits, and underscores only; keys with hyphens or other characters are silently dropped. |

The event arrives in Claude's context wrapped in a `<channel>` tag; the `source` attribute is set automatically from the server's configured name. For example, a notification with `content: 'build failed on main: ...'` and `meta: { severity: 'high', run_id: '1234' }` arrives as:

```text
<channel source="your-channel" severity="high" run_id="1234">
build failed on main: https://ci.example.com/run/1234
</channel>
```

Delivery is fire-and-forget. **Notifications are not acknowledged** — the `await` on `mcp.notification()` resolves when the message is written to the transport, not when Claude has processed it. If the session has not loaded your server as a channel, or the organization policy blocks it, events are dropped silently with no error returned. For delivery confirmation, track event state in your server and expose a [reply tool](https://code.claude.com/docs/en/channels-reference#expose-a-reply-tool) Claude can call to report status. Events queue into the session and are processed in order; several notifications arriving while Claude is busy are delivered together on the next turn and handled as a group. To process independent event streams concurrently, run separate sessions.

## Package as a Plugin

To make your channel installable and shareable, wrap it in a plugin and publish it to a marketplace; users install it with `/plugin install`, then enable it per session with `--channels plugin:<name>@<marketplace>` (plugin packaging and marketplace mechanics are owned by [the Plugins](https://code.claude.com/docs/en/plugins) and [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) pages). A channel published to your own marketplace still needs `--dangerously-load-development-channels` to run, since it is not on the approved allowlist. The default allowlist is the channel plugins in `claude-plugins-official`, which Anthropic curates at its discretion; the in-app community-marketplace submission forms add plugins to a marketplace that is not on the channel allowlist. For an official-marketplace listing, coordinate with an Anthropic partner contact; on Team and Enterprise plans an admin can instead include your plugin in the organization's own `allowedChannelPlugins` list (see [security and enterprise controls](cc_channels_security_and_enterprise_controls.md)).

**Source**: https://code.claude.com/docs/en/channels-reference
**Last Updated**: 2026-06-13
**Status**: Active
