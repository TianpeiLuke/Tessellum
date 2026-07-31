---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - channel_docking
keywords:
  - openclaw channel docking
  - dock command reply route
  - session identitylinks
  - dock-discord dock-slack
  - lastchannel lastto lastaccountid
  - cross-channel session forwarding
  - channel-prefixed peer id
topics:
  - OpenClaw
  - Channel Docking
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/channel-docking
access_control_group: ["general"]
---

# OpenClaw — Channel Docking (Move a Session's Reply Route)

## Overview

This note is the operator procedure for **channel docking** in OpenClaw: keeping one session's conversation context while moving where its future replies are delivered between linked chat channels (Telegram, Discord, Slack, Mattermost). It mirrors the `concepts/channel-docking` source page — the call-forwarding analogy, the required `session.identityLinks` identity group, the bundled `/dock-<channel>` commands and their underscore aliases, the session delivery fields that change (`lastChannel`, `lastTo`, `lastAccountId`), what docking deliberately does **not** change, and the troubleshooting cases.

## What docking does

Channel docking is **call forwarding for one OpenClaw session**: it keeps the same conversation context but changes where future replies for that session are delivered. The session is **not recreated** and the transcript history stays attached to the same session — only the delivery route changes.

In the source example, Alice can message OpenClaw on both Telegram and Discord. If she sends `/dock_discord` from her Telegram session, OpenClaw keeps the current session context and changes the reply route: before docking, replies go to Telegram `123`; after `/dock_discord`, replies go to Discord `456`.

## Why use it

Use docking when a task starts in one chat app but the next replies should land somewhere else. The common flow from the source is:

1. Start an agent task from Telegram.
2. Move to Discord where you are coordinating work.
3. Send `/dock_discord` from the Telegram session.
4. Keep the same OpenClaw session, but receive future replies in Discord.

## Required config — `session.identityLinks`

Docking requires `session.identityLinks`. The **source sender and target peer must be in the same identity group**. Example config:

```json5
{
  session: {
    identityLinks: {
      alice: ["telegram:123", "discord:456", "slack:U123"],
    },
  },
}
```

The values are **channel-prefixed peer ids**:

| Value          | Meaning                      |
| -------------- | ---------------------------- |
| `telegram:123` | Telegram sender id `123`     |
| `discord:456`  | Discord direct peer id `456` |
| `slack:U123`   | Slack user id `U123`         |

The canonical key (`alice` above) is **only the shared identity group name**. Dock commands use the channel-prefixed values to prove that the source sender and target peer are the same person.

## Commands — `/dock-<channel>`

Dock commands are **generated from loaded channel plugins that support native commands**. The current bundled commands are:

| Target channel | Command            | Alias              |
| -------------- | ------------------ | ------------------ |
| Discord        | `/dock-discord`    | `/dock_discord`    |
| Mattermost     | `/dock-mattermost` | `/dock_mattermost` |
| Slack          | `/dock-slack`      | `/dock_slack`      |
| Telegram       | `/dock-telegram`   | `/dock_telegram`   |

The underscore aliases (`/dock_discord`, etc.) are useful on native command surfaces such as Telegram.

## What changes — session delivery fields

Docking updates the active session **delivery fields**:

| Session field   | Example after `/dock_discord`            |
| --------------- | ---------------------------------------- |
| `lastChannel`   | `discord`                                |
| `lastTo`        | `456`                                    |
| `lastAccountId` | the target channel account, or `default` |

Those fields are persisted in the session store and used by later reply delivery for that session.

## What does not change

Docking only changes the delivery route for the current session. It does **not**:

- create channel accounts
- connect a new Discord, Telegram, Slack, or Mattermost bot
- grant access to a user
- bypass channel allowlists or DM policies
- move transcript history to another session
- make unrelated users share a session

## Troubleshooting

**The command says the sender is not linked.** Add both the current sender and the target peer to the same `session.identityLinks` group. For example, if Telegram sender `123` should dock to Discord peer `456`, include both `telegram:123` and `discord:456`.

**The command says no active session exists.** Dock from an existing direct-chat session. The command needs an active session entry so it can persist the new route.

**Replies still go to the old channel.** Check that the command replied with a success message, and confirm the target peer id matches the id used by that channel. Docking only changes the active session route; another session may still route elsewhere.

**I need to switch back.** Send the matching command for the original channel, such as `/dock_telegram` or `/dock-telegram`, from a linked sender.

**Source**: OpenClaw documentation — `concepts/channel-docking` (mirror `inbox/openclaw_docs/concepts/channel-docking.md`)
**Last Updated**: 2026-06-22
**Status**: Active
