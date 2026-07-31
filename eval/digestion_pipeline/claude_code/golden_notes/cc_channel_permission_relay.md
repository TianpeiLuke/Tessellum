---
tags:
  - resource
  - documentation
  - claude_code
  - channels
  - permission_relay
keywords:
  - permission relay
  - claude/channel/permission capability
  - permission_request notification
  - request_id verdict
  - allow deny behavior
  - gate inbound messages
  - sender allowlist
  - remote tool approval
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

# Channels — Relay Permission Prompts

## Overview

When Claude calls a tool that needs approval (`Bash`, `Write`, `Edit`), the local terminal dialog opens and the session waits. A two-way channel can opt in to **permission relay**: it receives the same prompt in parallel and forwards it to a remote device, so you can approve or deny tool use from your phone. Both the local dialog and the remote prompt stay live; Claude Code applies whichever answer arrives first and closes the other. This note is the build-your-own procedure for adding relay to a channel server, plus the **gate-inbound-messages** sender check that is its security prerequisite. Because anyone who can reply through a channel can approve tool use, relay must only be declared on a channel that authenticates the sender. The reply-tool foundation this extends is documented at [Channels reference — Expose a reply tool](https://code.claude.com/docs/en/channels-reference#expose-a-reply-tool); the base one-way server is in [`cc_build_a_channel`](cc_build_a_channel.md); the operator-facing allowlist controls are in [`cc_channels_security_and_enterprise_controls`](cc_channels_security_and_enterprise_controls.md).

Permission relay requires Claude Code v2.1.81 or later. Earlier versions ignore the `claude/channel/permission` capability. Relay covers tool-use approvals like `Bash`, `Write`, and `Edit`; project-trust and MCP-server-consent dialogs do not relay and appear only in the local terminal.

## Gate Inbound Messages (Prerequisite)

An ungated channel is a prompt-injection vector: anyone who can reach the endpoint can put text in front of Claude. A channel listening to a chat platform or a public endpoint needs a real sender check before it emits anything. Check the sender against an allowlist before calling `mcp.notification()`, and drop any message from a sender not in the set:

```ts
const allowed = new Set(loadAllowlist())  // from your access.json or equivalent

// inside your message handler, before emitting:
if (!allowed.has(message.from.id)) {  // sender, not room
  return  // drop silently
}
await mcp.notification({ ... })
```

Gate on the sender's identity (`message.from.id`), **not** the chat or room identity (`message.chat.id`). In group chats these differ, and gating on the room would let anyone in an allowlisted group inject messages into the session. The Telegram and Discord channels gate on a sender allowlist this way, bootstrapping it by pairing; the iMessage channel detects the user's own addresses from the Messages database at startup and lets them through automatically, with other senders added by handle. This sender gate is mandatory before relay is enabled, because relay grants approval authority.

## How Relay Works

When a permission prompt opens, the relay loop has four steps:

1. Claude Code generates a short request ID and notifies your server.
2. Your server forwards the prompt and ID to your chat app.
3. The remote user replies with a yes or no and that ID.
4. Your inbound handler parses the reply into a verdict, and Claude Code applies it only if the ID matches an open request.

The local terminal dialog stays open through all of this. If someone at the terminal answers before the remote verdict arrives, that answer is applied instead and the pending remote request is dropped.

## Permission Request Fields

The outbound notification from Claude Code is `notifications/claude/channel/permission_request`. Like the channel notification, the transport is standard MCP but the method and schema are Claude Code extensions. The `params` object has four string fields your server formats into the outgoing prompt:

| Field | Description |
| :--- | :--- |
| `request_id` | Five lowercase letters drawn from `a`-`z` without `l`, so it never reads as a `1` or `I` when typed on a phone. Include it in your outgoing prompt so it can be echoed in the reply. Claude Code only accepts a verdict that carries an ID it issued. The local terminal dialog doesn't display this ID, so your outbound handler is the only way to learn it. |
| `tool_name` | Name of the tool Claude wants to use, for example `Bash` or `Write`. |
| `description` | Human-readable summary of what this specific tool call does, the same text the local terminal dialog shows. For a Bash call this is Claude's description of the command, or the command itself if none was given. |
| `input_preview` | The tool's arguments as a JSON string, truncated to 200 characters. For Bash this is the command; for Write it's the file path and a prefix of the content. Omit it from your prompt if you only have room for a one-line message. |

The verdict your server sends back is `notifications/claude/channel/permission` with two fields: `request_id` echoing the ID above, and `behavior` set to `'allow'` or `'deny'`. Allow lets the tool call proceed; deny rejects it, the same as answering No in the local dialog. Neither verdict affects future calls.

## Add Relay to a Chat Bridge

Adding permission relay to a two-way channel takes three components: a `claude/channel/permission: {}` entry under `experimental` capabilities; a notification handler for `permission_request` that formats and sends the prompt; and a check in the inbound message handler that recognizes a `yes <id>` / `no <id>` reply and emits a verdict instead of forwarding the text to Claude. **Only declare the capability if your channel authenticates the sender** (see [Gate Inbound Messages](#gate-inbound-messages)), because anyone who can reply through your channel can approve or deny tool use in your session.

First, declare the capability alongside `claude/channel` under `experimental`:

```ts
capabilities: {
  experimental: {
    'claude/channel': {},
    'claude/channel/permission': {},  // opt in to permission relay
  },
  tools: {},
},
```

Next, register a notification handler (between the `Server` constructor and `mcp.connect()`) that Claude Code calls with the four request fields when a permission dialog opens. It formats the prompt and includes the ID so the user can echo it back:

```ts
import { z } from 'zod'

// setNotificationHandler routes by z.literal on the method field,
// so this schema is both the validator and the dispatch key
const PermissionRequestSchema = z.object({
  method: z.literal('notifications/claude/channel/permission_request'),
  params: z.object({
    request_id: z.string(),     // five lowercase letters, include verbatim in your prompt
    tool_name: z.string(),      // e.g. "Bash", "Write"
    description: z.string(),    // human-readable summary of this call
    input_preview: z.string(),  // tool args as JSON, truncated to ~200 chars
  }),
})

mcp.setNotificationHandler(PermissionRequestSchema, async ({ params }) => {
  send(
    `Claude wants to run ${params.tool_name}: ${params.description}\n\n` +
    // the ID in the instruction is what your inbound handler parses
    `Reply "yes ${params.request_id}" or "no ${params.request_id}"`,
  )
})
```

Finally, add a verdict check to the inbound handler before the chat-forwarding call. The regex matches the ID format Claude Code generates: five letters, never `l`. The `/i` flag tolerates phone autocorrect capitalizing the reply; lowercase the captured ID before sending it back:

```ts
// matches "y abcde", "yes abcde", "n abcde", "no abcde"
// [a-km-z] is the ID alphabet Claude Code uses (lowercase, skips 'l')
const PERMISSION_REPLY_RE = /^\s*(y|yes|n|no)\s+([a-km-z]{5})\s*$/i

async function onInbound(message: PlatformMessage) {
  if (!allowed.has(message.from.id)) return  // gate on sender first

  const m = PERMISSION_REPLY_RE.exec(message.text)
  if (m) {
    // m[1] is the verdict word, m[2] is the request ID
    await mcp.notification({
      method: 'notifications/claude/channel/permission',
      params: {
        request_id: m[2].toLowerCase(),  // normalize in case of autocorrect caps
        behavior: m[1].toLowerCase().startsWith('y') ? 'allow' : 'deny',
      },
    })
    return  // handled as verdict, don't also forward as chat
  }
  // didn't match verdict format: fall through to the normal chat path
  await mcp.notification({
    method: 'notifications/claude/channel',
    params: { content: message.text, meta: { chat_id: String(message.chat.id) } },
  })
}
```

A remote reply that does not exactly match the expected format fails safe in one of two ways, and in both cases the dialog stays open:

* **Different format** — the regex fails to match, so text like `approve it` or a bare `yes` without an ID falls through as a normal message to Claude.
* **Right format, wrong ID** — your server emits a verdict, but Claude Code finds no open request with that ID and drops it silently.

## Full Example and Three-Terminal Test

The reference page assembles a complete `webhook.ts` combining the reply tool, sender gating, and permission relay; that full assembly is verbatim at the [Channels reference — Full example](https://code.claude.com/docs/en/channels-reference#full-example) (it serves `GET /events` as an SSE stream for `curl -N` and gates `POST /` on the `X-Sender` header). To exercise the verdict path, run three terminals — a Claude Code session started with the development flag (so it spawns `webhook.ts`), an SSE listener, and an inbound sender:

```bash
# terminal 1: Claude Code session that spawns webhook.ts
claude --dangerously-load-development-channels server:webhook
# terminal 2: stream the outbound side (replies + permission prompts)
curl -N localhost:8788/events
# terminal 3: send a message that makes Claude try to run a command
curl -d "list the files in this directory" -H "X-Sender: dev" localhost:8788
```

Listing files is read-only, so Claude runs it without approval. The permission dialog opens when Claude calls the `reply` tool to send its answer back: the local dialog opens in the Claude Code terminal, and a moment later the prompt for `mcp__webhook__reply` appears in the `/events` stream including the five-letter ID. Approve it from the remote side with `curl -d "yes <id>" -H "X-Sender: dev" localhost:8788`. The local dialog closes, the `reply` tool runs, and Claude's reply lands in the stream.

**Source**: https://code.claude.com/docs/en/channels-reference
**Last Updated**: 2026-06-13
**Status**: Active
