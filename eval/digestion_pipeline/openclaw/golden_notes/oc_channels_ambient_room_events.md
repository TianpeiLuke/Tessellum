---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - ambient_room_events
keywords:
  - openclaw ambient room events
  - unmentionedInbound room_event
  - visibleReplies message_tool
  - messages.groupChat config
  - always-on group chat
  - quiet room context
  - requireMention false
  - historyLimit group history
  - suppressed delivery metadata
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/ambient-room-events
access_control_group: ["general"]
---

# OpenClaw — Channels: Ambient Room Events

## Overview

This note is the procedure for enabling OpenClaw **ambient room events**: letting an agent process unmentioned group or channel chatter as quiet context (updating memory and session state) while the room stays silent unless the agent explicitly calls the `message` tool. It mirrors the `channels/ambient-room-events` source page end to end — the recommended `messages.groupChat` setup, what changes in message flow, per-platform examples (Discord, Slack, Telegram), the agent-specific override, the `visibleReplies` modes, group history (`historyLimit`), and the troubleshooting flow.

Ambient room events are the recommended mode for always-on group chats: the agent listens, decides when a reply is useful, and avoids the old prompt pattern of answering `NO_REPLY`. Supported today: Discord guild channels, Slack channels and private channels, Slack multi-person DMs, and Telegram groups or supergroups. Other group channels keep their existing group behavior unless their own channel page says they support ambient room events.

## Recommended setup

Set the global group-chat behavior by combining `messages.groupChat.unmentionedInbound: "room_event"` with `messages.groupChat.visibleReplies: "message_tool"`:

```json5
{
  messages: {
    groupChat: {
      unmentionedInbound: "room_event",
      visibleReplies: "message_tool",
      historyLimit: 50,
    },
  },
}
```

Then configure the room itself as always-on by disabling mention gating for that room (`requireMention: false`). The channel must still be allowed by its normal `groupPolicy`, room allowlist, and sender allowlist — ambient mode does not bypass those gates. After saving the config, the Gateway hot-reloads `messages` settings; restart only when file watching or config reload is disabled.

## What changes

With `messages.groupChat.unmentionedInbound: "room_event"`, inbound classification changes as follows:

- unmentioned allowed group or channel messages become **quiet room events**
- mentioned messages stay user requests
- text commands and native commands stay user requests
- abort or stop requests stay user requests
- direct messages stay user requests

Room events use **strict visible delivery**: final assistant text is private, and the agent must call `message(action=send)` to post in the room.

## Discord example

Configure a Discord guild as ambient by setting `groupPolicy: "allowlist"`, `requireMention: false`, and the allowed `users` list:

```json5
{
  messages: {
    groupChat: {
      unmentionedInbound: "room_event",
      visibleReplies: "message_tool",
      historyLimit: 50,
    },
  },
  channels: {
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        "<DISCORD_SERVER_ID>": {
          requireMention: false,
          users: ["<YOUR_DISCORD_USER_ID>"],
        },
      },
    },
  },
}
```

Use per-channel Discord config when only one channel should be ambient — set `allow: true` and `requireMention: false` on that channel under `guilds.<server>.channels.<channel>`:

```json5
{
  channels: {
    discord: {
      guilds: {
        "<DISCORD_SERVER_ID>": {
          channels: {
            "<DISCORD_CHANNEL_ID_OR_NAME>": {
              allow: true,
              requireMention: false,
            },
          },
        },
      },
    },
  },
}
```

## Slack example

Slack channel allowlists are ID-first: use channel IDs such as `C12345678`, not `#channel-name`. Set `groupPolicy: "allowlist"` plus the channel's `allow: true` and `requireMention: false`:

```json5
{
  messages: {
    groupChat: {
      unmentionedInbound: "room_event",
      visibleReplies: "message_tool",
      historyLimit: 50,
    },
  },
  channels: {
    slack: {
      groupPolicy: "allowlist",
      channels: {
        "<SLACK_CHANNEL_ID>": {
          allow: true,
          requireMention: false,
        },
      },
    },
  },
}
```

## Telegram example

For Telegram groups, the bot must be able to see normal group messages. If `requireMention: false`, disable BotFather privacy mode or use another Telegram setup that delivers full group traffic to the bot. Set the group's `groupPolicy: "open"` and `requireMention: false`:

```json5
{
  messages: {
    groupChat: {
      unmentionedInbound: "room_event",
      visibleReplies: "message_tool",
      historyLimit: 50,
    },
  },
  channels: {
    telegram: {
      groups: {
        "<TELEGRAM_GROUP_CHAT_ID>": {
          groupPolicy: "open",
          requireMention: false,
        },
      },
    },
  },
}
```

Telegram group IDs are usually negative numbers such as `-1001234567890`. Read `chat.id` from `openclaw logs --follow`, forward a group message to an ID helper bot, or inspect Bot API `getUpdates`.

## Agent specific policy

Use an agent override when several agents share the same room but only one should treat unmentioned chatter as ambient context. Keep the shared `messages.groupChat.visibleReplies` setting, then set `unmentionedInbound: "room_event"` (and any `mentionPatterns`) on the individual agent in `agents.list`:

```json5
{
  messages: {
    groupChat: {
      visibleReplies: "message_tool",
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          unmentionedInbound: "room_event",
          mentionPatterns: ["@openclaw", "openclaw"],
        },
      },
    ],
  },
}
```

The agent-specific `agents.list[].groupChat.unmentionedInbound` value overrides `messages.groupChat.unmentionedInbound` for that agent.

## Visible reply modes

`messages.groupChat.visibleReplies` defaults to `"automatic"` for normal group/channel user requests. Keep that default when you want final assistant text to post visibly without requiring an explicit message-tool call.

For ambient always-on rooms, `messages.groupChat.visibleReplies: "message_tool"` is still recommended, especially with latest-generation, tool-reliable models such as GPT 5.5. It lets the agent decide when to speak by calling the message tool. If the model returns final text without calling the tool, OpenClaw keeps that final text private and logs suppressed delivery metadata.

Room events stay strict even when other group requests use automatic replies: unmentioned ambient room events still require `message(action=send)` for visible output.

## History

`messages.groupChat.historyLimit` controls the global group history default. Channels can override it with `channels.<channel>.historyLimit`, and some channels also support per-account history limits. Set `historyLimit: 0` to disable group history context.

Supported room-event channels keep recent ambient room messages as context. Discord keeps room-event history until a visible Discord send succeeds, so quiet context is not lost before message-tool delivery.

## Troubleshooting

If the room shows typing or token usage but no visible message:

1. Confirm the room is allowed by the channel allowlist and sender allowlist.
2. Confirm `requireMention: false` is set at the room level you expect.
3. Check whether `messages.groupChat.unmentionedInbound` or the agent override is `"room_event"`.
4. Inspect logs for suppressed final payload metadata or `didSendViaMessagingTool: false`.
5. For normal group requests, keep or restore `messages.groupChat.visibleReplies: "automatic"` if you want final replies posted automatically. For ambient rooms using `message_tool`, use a model/runtime that reliably calls tools.

If Telegram ambient rooms do not trigger at all, check BotFather privacy mode and verify the Gateway is receiving normal group messages. If Slack ambient rooms do not trigger, verify the channel key is the Slack channel ID and the app has the required `channels:history` or `groups:history` scope for that room type.

**Source**: OpenClaw documentation — `channels/ambient-room-events` (mirror `inbox/openclaw_docs/channels/ambient-room-events.md`)
**Last Updated**: 2026-06-22
**Status**: Active
