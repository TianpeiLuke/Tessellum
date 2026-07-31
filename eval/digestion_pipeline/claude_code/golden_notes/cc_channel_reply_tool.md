---
tags:
  - resource
  - documentation
  - claude_code
  - channels
  - reply_tool
keywords:
  - reply tool
  - two-way channel
  - tools capability
  - ListToolsRequestSchema
  - CallToolRequestSchema
  - reply inputSchema chat_id text
  - instructions routing
  - sse outbound stream
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

# Channels — Expose a Reply Tool

## Overview

A **two-way channel** (a chat bridge rather than a one-way alert forwarder) exposes a standard [MCP tool](https://code.claude.com/docs/en/mcp) that Claude can call to send messages back. Nothing about the tool registration is channel-specific — it is ordinary MCP tool wiring layered on the one-way [webhook receiver](cc_build_a_channel.md). This note is the build-your-own procedure for adding a `reply` tool: declare the `tools: {}` capability, register the tool's schema and send logic, and update the `instructions` string so Claude knows when and how to route replies.

A reply tool has three components: (1) a `tools: {}` entry in the `Server` constructor capabilities so Claude Code discovers the tool, (2) tool handlers that define the schema and implement the send logic, and (3) an `instructions` string that tells Claude when and how to call the tool. To make a two-way channel forward tool-approval prompts to a remote device, extend it with the [permission relay](cc_channel_permission_relay.md).

## Step 1 — Enable Tool Discovery

In the `Server` constructor in `webhook.ts`, add `tools: {}` to the capabilities so Claude Code knows your server offers tools:

```ts
capabilities: {
  experimental: { 'claude/channel': {} },
  tools: {},  // enables tool discovery
},
```

## Step 2 — Register the Reply Tool

Add two request handlers between the `Server` constructor and `mcp.connect()`, with the import at the top of `webhook.ts`. The `ListToolsRequestSchema` handler is what Claude queries at startup to discover the tools; the `CallToolRequestSchema` handler is what Claude calls when it wants to invoke one. This registers a `reply` tool that Claude can call with a `chat_id` and `text`:

```ts
// Add this import at the top of webhook.ts
import { ListToolsRequestSchema, CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js'

// Claude queries this at startup to discover what tools your server offers
mcp.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'reply',
    description: 'Send a message back over this channel',
    // inputSchema tells Claude what arguments to pass
    inputSchema: {
      type: 'object',
      properties: {
        chat_id: { type: 'string', description: 'The conversation to reply in' },
        text: { type: 'string', description: 'The message to send' },
      },
      required: ['chat_id', 'text'],
    },
  }],
}))

// Claude calls this when it wants to invoke a tool
mcp.setRequestHandler(CallToolRequestSchema, async req => {
  if (req.params.name === 'reply') {
    const { chat_id, text } = req.params.arguments as { chat_id: string; text: string }
    // send() is your outbound: POST to your chat platform, or for local
    // testing the SSE broadcast shown in the full example below.
    send(`Reply to ${chat_id}: ${text}`)
    return { content: [{ type: 'text', text: 'sent' }] }
  }
  throw new Error(`unknown tool: ${req.params.name}`)
})
```

## Step 3 — Update the Instructions

Update the `instructions` string in the `Server` constructor so Claude routes replies back through the tool. This example tells Claude to pass `chat_id` from the inbound tag:

```ts
instructions: 'Messages arrive as <channel source="webhook" chat_id="...">. Reply with the reply tool, passing the chat_id from the tag.'
```

## Outbound and Local Testing

The `send()` function called by the `CallToolRequestSchema` handler is your outbound path: a real bridge POSTs to its chat platform. For local testing, the reference page's complete `webhook.ts` streams outbound replies over `GET /events` using [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) (SSE), so `curl -N localhost:8788/events` can watch Claude's replies live while inbound chat arrives on `POST /`. The SSE `send()` formats each line as a `data:` chunk and broadcasts it to every connected `/events` listener:

```ts
const listeners = new Set<(chunk: string) => void>()
function send(text: string) {
  const chunk = text.split('\n').map(l => `data: ${l}\n`).join('') + '\n'
  for (const emit of listeners) emit(chunk)
}
```

The full single-file `webhook.ts` with two-way support (the `Server` constructor, both handlers, the SSE-backed `Bun.serve` listener with `idleTimeout: 0`, and the inbound `POST` that assigns a `chat_id`) is verbatim at the [Channels reference — Expose a reply tool](https://code.claude.com/docs/en/channels-reference#expose-a-reply-tool) section. The [fakechat server](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/fakechat) shows a more complete example with file attachments and message editing.

**Source**: https://code.claude.com/docs/en/channels-reference
**Last Updated**: 2026-06-13
**Status**: Active
