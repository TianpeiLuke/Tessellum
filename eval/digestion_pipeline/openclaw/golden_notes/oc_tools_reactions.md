---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - reactions
keywords:
  - openclaw reactions tool
  - message tool react action
  - emoji reaction add remove
  - tracktoolcalls status reactions
  - per-channel reaction behavior
  - reactionlevel config
  - imessage tapback
  - feishu_reaction tool
topics:
  - OpenClaw
  - Reactions Tool
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/reactions
access_control_group: ["general"]
---

# OpenClaw — The `react` Action (Emoji Reactions Across Channels)

## Overview

This note documents the OpenClaw **reactions** procedure: how an agent adds and removes emoji reactions on messages using the `message` tool with the `react` action, and how that behavior varies by channel and transport — mirroring the `tools/reactions` source page. It covers the `react` action shape, the `emoji` / `remove` / `trackToolCalls` semantics, the per-channel behavior matrix (Discord, Slack, Google Chat, Nextcloud Talk, Telegram, WhatsApp, Zalo Personal, Feishu/Lark, Signal, iMessage), and the per-channel `reactionLevel` config that tunes how broadly the agent reacts. The page is channel-agnostic at the action level: one `react` action, with each channel adapter applying its own add/remove/notification rules.

## How it works

The agent adds and removes emoji reactions on messages using the `message` tool with the `react` action. The minimal call shape is:

```json
{
  "action": "react",
  "messageId": "msg-123",
  "emoji": "thumbsup"
}
```

The action semantics, copied from source:

- `emoji` is required when adding a reaction.
- Set `emoji` to an empty string (`""`) to remove the bot's reaction(s).
- Set `remove: true` to remove a specific emoji (requires non-empty `emoji`).
- On channels that support status reactions, `trackToolCalls: true` on a reaction lets the runtime use that reacted message for subsequent tool progress reactions during the same turn.

So there are three distinct gestures: **add** (non-empty `emoji`, no `remove`), **remove-all** (empty `emoji`), and **remove-specific** (`remove: true` with a non-empty `emoji`). The `trackToolCalls: true` flag is a progress-reaction affordance — it pins the reacted message as the anchor the runtime updates with tool-call progress reactions for the rest of the turn, on channels that support status reactions.

## Channel behavior

Reaction behavior varies by channel and transport. The source documents each supported channel's add/remove and notification rules in a per-channel accordion; each is reproduced below.

**Discord and Slack** — Empty `emoji` removes all of the bot's reactions on the message. `remove: true` removes just the specified emoji.

**Google Chat** — Empty `emoji` removes the app's reactions on the message. `remove: true` removes just the specified emoji.

**Nextcloud Talk** — Adding reactions only: `emoji` is required and must be non-empty. Reaction removal is not supported yet; calls with `remove: true` (or empty `emoji`) are rejected with a clear error rather than silently no-oping. Requires the Talk bot to be registered with the `reaction` feature (see the Nextcloud Talk channel docs).

**Telegram** — Empty `emoji` removes the bot's reactions. `remove: true` also removes reactions but still requires a non-empty `emoji` for tool validation.

**WhatsApp** — Empty `emoji` removes the bot reaction. `remove: true` maps to empty emoji internally (still requires `emoji` in the tool call). WhatsApp has one bot reaction slot per message; status reaction updates replace that slot rather than stacking multiple emoji.

**Zalo Personal (zalouser)** — Requires non-empty `emoji`. `remove: true` removes that specific emoji reaction.

**Feishu/Lark** — Use the `feishu_reaction` tool with actions `add`, `remove`, and `list`. Add/remove requires `emoji_type`; remove also requires `reaction_id`. (Feishu/Lark is the one channel that uses a dedicated tool rather than the `message` tool `react` action.)

**Signal** — Inbound reaction notifications are controlled by `channels.signal.reactionNotifications`: `"off"` disables them, `"own"` (default) emits events when users react to bot messages, and `"all"` emits events for all reactions.

**iMessage** — Outbound reactions are iMessage tapbacks (`love`, `like`, `dislike`, `laugh`, `emphasize`, and `question`). Inbound tapback notifications are controlled by `channels.imessage.reactionNotifications`: `"off"` disables them, `"own"` (default) emits events when users react to bot-authored messages, and `"all"` emits events for all tapbacks from authorized senders.

## Reaction level

Per-channel `reactionLevel` config controls how broadly the agent uses reactions. Values are typically `off`, `ack`, `minimal`, or `extensive`. The source names two concrete per-channel knobs: `channels.telegram.reactionLevel` (Telegram reactionLevel) and `channels.whatsapp.reactionLevel` (WhatsApp reactionLevel). Set `reactionLevel` on individual channels to tune how actively the agent reacts to messages on each platform.

**Source**: OpenClaw documentation — `tools/reactions` (mirror `inbox/openclaw_docs/tools/reactions.md`)
**Last Updated**: 2026-06-22
**Status**: Active
