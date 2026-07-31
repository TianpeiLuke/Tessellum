---
tags:
  - resource
  - documentation
  - claude_code
  - channels
  - concept
keywords:
  - channel
  - mcp server pushes events
  - one-way vs two-way channel
  - chat bridge
  - push vs poll
  - always-on session
  - research preview
  - how channels compare
topics:
  - Claude Code
  - Channels
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/channels
access_control_group: ["general"]
---

# Claude Code — Channels Overview

## Overview

A **channel** is an MCP server that pushes events into your running Claude Code session, so Claude can react to things that happen while you are not at the terminal. Channels can be **two-way**: Claude reads the event and replies back through the same channel, like a chat bridge. Events only arrive while the session is open, so for an always-on setup you run Claude in a background process or persistent terminal. Unlike integrations that spawn a fresh cloud session or wait to be polled, the event arrives in the session you already have open.

Channels are a **research preview** feature and require Claude Code v2.1.80 or later. They require Anthropic authentication through claude.ai or a Console API key, and are not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry. Team and Enterprise organizations must explicitly enable them. You install a channel as a plugin and configure it with your own credentials; Telegram, Discord, and iMessage are included in the research preview. This note defines what a channel is, the one-way vs two-way contract, how channels compare to other Claude Code surfaces, and the research-preview status; the per-platform setup, the security controls, and the build-your-own contract live in the sibling notes.

## What a Channel Is

A channel is an MCP server that runs on the same machine as Claude Code. Claude Code spawns it as a subprocess and communicates over stdio. The channel server is the bridge between external systems and the Claude Code session:

- **Chat platforms** (Telegram, Discord): the plugin runs locally and polls the platform's API for new messages. When someone DMs your bot, the plugin receives the message and forwards it to Claude. No URL to expose.
- **Webhooks** (CI, monitoring): the server listens on a local HTTP port. External systems POST to that port, and the server pushes the payload to Claude.

The event arrives in Claude's context wrapped in a `<channel>` tag — the `source` attribute is set automatically from the server's configured name, and each `meta` entry becomes an attribute on the tag:

```text
<channel source="webhook" path="/" method="POST">build failed on main: https://ci.example.com/run/1234</channel>
```

When Claude replies through a channel, you see the inbound message in your terminal but not the reply text. The terminal shows the tool call and a confirmation (like "sent"), and the actual reply appears on the other platform.

## One-Way vs Two-Way

You can build a one-way or two-way channel:

- **One-way channels** forward alerts, webhooks, or monitoring events for Claude to act on. Claude reads them and acts in your session, but does not send anything back through the channel.
- **Two-way channels** (like chat bridges) also expose a [reply tool](https://code.claude.com/docs/en/channels-reference#expose-a-reply-tool) so Claude can send messages back. A two-way channel with a trusted sender path can additionally opt in to [relay permission prompts](cc_channel_permission_relay.md) so you can approve or deny tool use remotely.

The two headline patterns the docs call out are the **chat bridge** — ask Claude something from your phone via Telegram, Discord, or iMessage, and the answer comes back in the same chat while the work runs on your machine against your real files — and the **webhook receiver**, where a webhook from CI, an error tracker, a deploy pipeline, or another external service arrives where Claude already has your files open and remembers what you were debugging.

## How Channels Compare

Several Claude Code features connect to systems outside the terminal, each suited to a different kind of work:

| Feature | What it does | Good for |
| --- | --- | --- |
| Claude Code on the web | Runs tasks in a fresh cloud sandbox, cloned from GitHub | Delegating self-contained async work you check on later |
| Claude in Slack | Spawns a web session from an `@Claude` mention in a channel or thread | Starting tasks directly from team conversation context |
| Standard MCP server | Claude queries it during a task; nothing is pushed to the session | Giving Claude on-demand access to read or query a system |
| Remote Control | You drive your local session from claude.ai or the Claude mobile app | Steering an in-progress session while away from your desk |

Channels fill the gap in that list by **pushing events from non-Claude sources into your already-running local session**. The key distinction is the push-vs-poll event model: a standard MCP server waits to be queried during a task and pushes nothing, whereas a channel injects events into the open session as they happen.

For details on the linked surfaces, see [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web), [Claude in Slack](https://code.claude.com/docs/en/slack), the [standard MCP server](https://code.claude.com/docs/en/mcp), [Remote Control](https://code.claude.com/docs/en/remote-control), and [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) (poll on a timer instead of reacting to pushed events).

## Research Preview Status

Channels are a research preview feature. Availability is rolling out gradually, and the `--channels` flag syntax and protocol contract may change based on feedback. During the preview, `--channels` only accepts plugins from an Anthropic-maintained allowlist, or from your organization's allowlist if an admin has set `allowedChannelPlugins`. The channel plugins in `claude-plugins-official` are the default approved set; if you pass something that is not on the effective allowlist, Claude Code starts normally but the channel does not register, and the startup notice tells you why.

To test a channel you are building (which is not on the approved allowlist), use the `--dangerously-load-development-channels` flag — see [Build a Channel](cc_build_a_channel.md). Issues and feedback go to the Claude Code GitHub repository.

**Source**: https://code.claude.com/docs/en/channels
**Last Updated**: 2026-06-13
**Status**: Active
