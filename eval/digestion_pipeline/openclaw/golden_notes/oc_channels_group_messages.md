---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - whatsapp_groups
keywords:
  - openclaw whatsapp group messages
  - whatsapp group activation mention always
  - groupchat mentionpatterns
  - whatsapp grouppolicy groupallowfrom
  - per-group session keys whatsapp
  - pending-message context injection
  - /activation owner-only command
  - no_reply silent token
topics:
  - OpenClaw
  - Channels
  - WhatsApp Groups
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/group-messages
access_control_group: ["general"]
---

# OpenClaw — WhatsApp Group Messages: Activation, Allowlists, and Context

## Overview

This note is the procedure for letting an OpenClaw agent participate in existing **WhatsApp** group chats: it sits in the group on the operator's own WhatsApp account, wakes only when pinged, and keeps the group thread separate from the personal DM session. It mirrors the `channels/group-messages` source page, which layers WhatsApp-specific behavior on top of the cross-channel groups model (the general behavior/visibility model lives in [oc_channels_groups_model](oc_channels_groups_model.md)). It covers the activation modes, group policy/allowlist gating, per-group session keys, pending-message context injection, the WhatsApp `groupChat` config example, the owner-only `/activation` command, how to use it, verification, and known considerations.

## Behavior

OpenClaw's WhatsApp group behavior is governed by several config surfaces under `channels.whatsapp` and per-agent `groupChat` blocks:

- **Activation modes** — `mention` (default) or `always`. `mention` requires a ping: a real WhatsApp @-mention via `mentionedJids`, a safe regex pattern, or the bot's E.164 number appearing anywhere in the text. `always` wakes the agent on every message but it should reply only when it can add meaningful value; otherwise it returns the exact silent token `NO_REPLY` / `no_reply`. Defaults are set in config (`channels.whatsapp.groups`) and overridden per group via `/activation`. When `channels.whatsapp.groups` is set it also acts as a **group allowlist** (include `"*"` to allow all).
- **Group policy** — `channels.whatsapp.groupPolicy` controls whether group messages are accepted, with values `open | disabled | allowlist`. `allowlist` uses `channels.whatsapp.groupAllowFrom` (fallback: explicit `channels.whatsapp.allowFrom`). The default is `allowlist` (groups are blocked until you add senders).
- **Per-group sessions** — session keys look like `agent:<agentId>:whatsapp:group:<jid>`, so directives such as `/verbose on`, `/trace on`, or `/think high` (sent as standalone messages) are scoped to that group; the personal DM state is untouched. Heartbeats are skipped for group threads.
- **Context injection** — **pending-only** group messages (default 50) that _did not_ trigger a run are prefixed under `[Chat messages since your last reply - for context]`, with the triggering line under `[Current message - respond to this]`. Messages already in the session are not re-injected.
- **Sender surfacing** — every group batch ends with a `[from: Sender Name (+E164)]` marker so OpenClaw knows who is speaking.
- **Ephemeral / view-once** — OpenClaw unwraps ephemeral and view-once messages before extracting text/mentions, so pings inside them still trigger.
- **Group system prompt** — on the first turn of a group session (and whenever `/activation` changes the mode) OpenClaw injects a short blurb into the system prompt, e.g. `You are replying inside the WhatsApp group "<subject>". Group members: Alice (+44...), Bob (+43...), ... Activation: trigger-only ... Address the specific sender noted in the message context.` If metadata isn't available it still tells the agent it is a group chat.

> The per-agent field `agents.list[].groupChat.mentionPatterns` is also used by Telegram, Discord, Slack, and iMessage. For multi-agent setups, set it per agent, or use `messages.groupChat.mentionPatterns` as a global fallback.

## Config example (WhatsApp)

Add a `groupChat` block to `~/.openclaw/openclaw.json` so display-name pings work even when WhatsApp strips the visual `@` from the text body:

```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
      },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          historyLimit: 50,
          mentionPatterns: ["@?openclaw", "\\+?15555550123"],
        },
      },
    ],
  },
}
```

Notes on this config:

- The regexes are case-insensitive and use the same safe-regex guardrails as other config regex surfaces; invalid patterns and unsafe nested repetition are ignored.
- WhatsApp still sends canonical mentions via `mentionedJids` when someone taps the contact, so the number fallback is rarely needed but is a useful safety net.

### Activation command (owner-only)

Change the per-group activation mode with the group-chat command:

- `/activation mention`
- `/activation always`

Only the **owner number** (from `channels.whatsapp.allowFrom`, or the bot's own E.164 when unset) can change this. Send `/status` as a standalone message in the group to see the current activation mode.

## How to use

1. Add your WhatsApp account (the one running OpenClaw) to the group.
2. Say `@openclaw …` (or include the number). Only allowlisted senders can trigger it unless you set `groupPolicy: "open"`.
3. The agent prompt will include recent group context plus the trailing `[from: …]` marker so it can address the right person.
4. Session-level directives (`/verbose on`, `/trace on`, `/think high`, `/new` or `/reset`, `/compact`) apply only to that group's session; send them as standalone messages so they register. The personal DM session remains independent.

## Testing / verification

- **Manual smoke test:**
  - Send an `@openclaw` ping in the group and confirm a reply that references the sender name.
  - Send a second ping and verify the history block is included, then cleared on the next turn.
- **Check gateway logs** (run with `--verbose`) to see `inbound web message` entries showing `from: <groupJid>` and the `[from: …]` suffix.

## Known considerations

- Heartbeats are intentionally skipped for groups to avoid noisy broadcasts.
- Echo suppression uses the combined batch string: if you send identical text twice without mentions, only the first will get a response.
- Session-store entries appear as `agent:<agentId>:whatsapp:group:<jid>` in the session store (`~/.openclaw/agents/<agentId>/sessions/sessions.json` by default); a missing entry just means the group hasn't triggered a run yet.
- Typing indicators in groups follow `agents.defaults.typingMode`. When visible replies are opted into message-tool-only mode, typing starts immediately by default so group members can see the agent is working even if no automatic final reply is posted. Explicit typing-mode config still wins.

**Source**: OpenClaw documentation — `channels/group-messages` (mirror `inbox/openclaw_docs/channels/group-messages.md`)
**Last Updated**: 2026-06-22
**Status**: Active
