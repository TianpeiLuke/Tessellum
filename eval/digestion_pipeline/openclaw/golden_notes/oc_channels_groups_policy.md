---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - access_control
keywords:
  - openclaw group policy
  - groupPolicy allowlist open disabled
  - groupAllowFrom group allowlist
  - mention gating requireMention
  - mentionPatterns scope allowIn denyIn
  - group channel tool restrictions toolsBySender
  - activation owner-only command
  - group sender authorization
topics:
  - OpenClaw
  - Group Access Control
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/groups
access_control_group: ["general"]
---

# OpenClaw — Configuring Group Access Policy, Mention Gating, and Tool Restrictions

## Overview

This note is the configuration procedure for gating who can drive an OpenClaw agent in a group/room and when it replies, mirroring the `channels/groups` source page sections **Group policy**, **Mention gating (default)**, **Scope configured mention patterns**, **Group/channel tool restrictions (optional)**, **Group allowlists**, and **Activation (owner-only)**. It covers the three-tier evaluation order — `groupPolicy` → group/sender allowlists → mention gating — plus per-group/per-sender `tools`/`toolsBySender` restrictions and the owner-only `/activation` toggle. The behavior model (visible replies, session keys, context visibility, surface specifics) is the concept-side counterpart in [oc_channels_groups_model](oc_channels_groups_model.md); this note is the procedural "how to configure gating" half.

## Evaluation order (mental model)

A group message is evaluated in three ordered stages: first `groupPolicy` (`open` / `disabled` / `allowlist`), then group allowlists (`*.groups`, `*.groupAllowFrom`, channel-specific allowlist), then mention gating (`requireMention`, `/activation`). Trigger authorization (who can trigger the agent) is a separate concern from mention gating (when the agent replies): `groupPolicy` is separate from mention-gating, which requires @mentions. Allowlisting a group or sender does NOT disable mention gating — set that group's `requireMention` to `false` when all messages should trigger.

## Group policy

`groupPolicy` controls how group/room messages are handled per channel and takes one of three values:

| Policy        | Behavior                                                     |
| ------------- | ------------------------------------------------------------ |
| `"open"`      | Groups bypass allowlists; mention-gating still applies.      |
| `"disabled"`  | Block all group messages entirely.                           |
| `"allowlist"` | Only allow groups/rooms that match the configured allowlist. |

The default is `groupPolicy: "allowlist"`; if your group allowlist is empty, group messages are blocked. As a runtime safety measure, when a provider block is completely missing (`channels.<provider>` absent), group policy falls back to a fail-closed mode (typically `allowlist`) instead of inheriting `channels.defaults.groupPolicy`. The per-channel configuration shape (note the channel-specific allowlist keys: `groupAllowFrom`, Discord `guilds`, Slack `channels`, Matrix `groups`):

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "disabled", // "open" | "disabled" | "allowlist"
      groupAllowFrom: ["+15551234567"],
    },
    telegram: {
      groupPolicy: "disabled",
      groupAllowFrom: ["123456789"], // numeric Telegram user id (wizard can resolve @username)
    },
    signal: {
      groupPolicy: "disabled",
      groupAllowFrom: ["+15551234567"],
    },
    imessage: {
      groupPolicy: "disabled",
      groupAllowFrom: ["chat_id:123"],
    },
    msteams: {
      groupPolicy: "disabled",
      groupAllowFrom: ["user@org.com"],
    },
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        GUILD_ID: { channels: { help: { allow: true } } },
      },
    },
    slack: {
      groupPolicy: "allowlist",
      channels: { "#general": { allow: true } },
    },
    matrix: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["@owner:example.org"],
      groups: {
        "!roomId:example.org": { enabled: true },
        "#alias:example.org": { enabled: true },
      },
    },
  },
}
```

### Per-channel allowlist notes

- WhatsApp/Telegram/Signal/iMessage/Microsoft Teams/Zalo use `groupAllowFrom` (fallback: explicit `allowFrom`).
- Signal: `groupAllowFrom` can match either the inbound Signal group id or the sender phone/UUID.
- Discord: allowlist uses `channels.discord.guilds.<id>.channels`. Slack: allowlist uses `channels.slack.channels`.
- Matrix: allowlist uses `channels.matrix.groups` — prefer room IDs or aliases (joined-room name lookup is best-effort, and unresolved names are ignored at runtime); restrict senders with `channels.matrix.groupAllowFrom`, and per-room `users` allowlists are also supported.
- DM pairing approvals (`*-allowFrom` store entries) apply to DM access only; group sender authorization stays explicit to group allowlists.
- Group DMs are controlled separately (`channels.discord.dm.*`, `channels.slack.dm.*`).
- Telegram allowlist can match user IDs (`"123456789"`, `"telegram:123456789"`, `"tg:123456789"`) or usernames (`"@alice"` or `"alice"`); prefixes are case-insensitive.

## Mention gating (default)

Group messages require a mention unless overridden per group; defaults live per subsystem under `*.groups."*"`. Replying to a bot message counts as an implicit mention when the channel supports reply metadata, and quoting a bot message can also count as an implicit mention on channels that expose quote metadata — current built-in cases include Telegram, WhatsApp, Slack, Discord, Microsoft Teams, and ZaloUser. Per-group `requireMention` plus per-agent `mentionPatterns`:

```json5
{
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true },
        "123@g.us": { requireMention: false },
      },
    },
    telegram: {
      groups: {
        "*": { requireMention: true },
        "123456789": { requireMention: false },
      },
    },
    imessage: {
      groups: {
        "*": { requireMention: true },
        "123": { requireMention: false },
      },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          mentionPatterns: ["@openclaw", "openclaw", "\\+15555550123"],
          historyLimit: 50,
        },
      },
    ],
  },
}
```

## Scope configured mention patterns

Configured `mentionPatterns` are regex fallback triggers — use them when the platform does not expose a native bot mention, or when you want plain text such as `openclaw:` to count as a mention. Native platform mentions are separate: when Discord, Slack, Telegram, Matrix, or another channel can prove the message explicitly mentioned the bot, that native mention still triggers even if configured regex patterns are denied. By default, configured mention patterns apply everywhere that channel passes provider and conversation facts into mention detection; to keep broad patterns from waking the agent in every group, scope them per channel with `channels.<channel>.mentionPatterns`.

Use `mode: "deny"` when regex mention patterns should be off by default for a channel, then opt in specific rooms with `allowIn`:

```json5
{
  messages: {
    groupChat: {
      mentionPatterns: ["\\bopenclaw\\b", "\\bops bot\\b"],
    },
  },
  channels: {
    slack: {
      mentionPatterns: {
        mode: "deny",
        allowIn: ["C0123OPS"],
      },
    },
  },
}
```

Use the default `mode: "allow"` (or omit `mode`) when regex mention patterns should apply broadly, then turn them off in noisy rooms with `denyIn` (e.g. `channels.telegram.mentionPatterns: { denyIn: ["-1001234567890", "-1001234567890:topic:42"] }`).

### Policy resolution

| Field           | Effect                                                                                                                |
| --------------- | --------------------------------------------------------------------------------------------------------------------- |
| `mode: "allow"` | Regex mention patterns are enabled unless the conversation ID is in `denyIn`. This is the default.                    |
| `mode: "deny"`  | Regex mention patterns are disabled unless the conversation ID is in `allowIn`.                                       |
| `allowIn`       | Conversation IDs where regex mention patterns are enabled in deny mode.                                               |
| `denyIn`        | Conversation IDs where regex mention patterns are disabled. `denyIn` wins over `allowIn` if both include the same ID. |

The conversation IDs used in `allowIn` / `denyIn` are per-channel: Discord channel IDs, Matrix room IDs, Slack channel IDs, Telegram group chat IDs (or `chatId:topic:threadId` for forum topics), and WhatsApp conversation IDs such as `123@g.us`. Account-level channel configs can set the same policy under `channels.<channel>.accounts.<accountId>.mentionPatterns` when that channel supports multiple accounts; account policy takes precedence over the top-level channel policy for that account.

### Mention gating notes

- `mentionPatterns` are case-insensitive safe regex patterns; invalid patterns and unsafe nested-repetition forms are ignored.
- Surfaces that provide explicit mentions still pass; configured regex patterns are a fallback.
- Per-agent override: `agents.list[].groupChat.mentionPatterns` (useful when multiple agents share a group).
- Mention gating is only enforced when mention detection is possible (native mentions or `mentionPatterns` are configured).
- Allowlisting a group or sender does not disable mention gating; set that group's `requireMention` to `false` when all messages should trigger.
- Discord defaults live in `channels.discord.guilds."*"` (overridable per guild/channel).
- Group history context is wrapped uniformly across channels: use `messages.groupChat.historyLimit` for the global default and `channels.<channel>.historyLimit` (or `channels.<channel>.accounts.*.historyLimit`) for overrides; set `0` to disable.

## Group/channel tool restrictions (optional)

Some channel configs support restricting which tools are available inside a specific group/room/channel. `tools` allows/denies tools for the whole group, while `toolsBySender` provides per-sender overrides within the group. `toolsBySender` keys use explicit prefixes: `channel:<channelId>:<senderId>`, `id:<senderId>`, `e164:<phone>`, `username:<handle>`, `name:<displayName>`, and `"*"` wildcard — channel ids use canonical OpenClaw channel ids (aliases such as `teams` normalize to `msteams`), and legacy unprefixed keys are still accepted and matched as `id:` only.

Resolution order (most specific wins): (1) group/channel `toolsBySender` match, (2) group/channel `tools`, (3) default (`"*"`) `toolsBySender` match, (4) default (`"*"`) `tools`. Example (Telegram), where a group denies `exec` for everyone but re-allows it for one sender:

```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { tools: { deny: ["exec"] } },
        "-1001234567890": {
          tools: { deny: ["exec", "read", "write"] },
          toolsBySender: {
            "id:123456789": { alsoAllow: ["exec"] },
          },
        },
      },
    },
  },
}
```

Group/channel tool restrictions are applied in addition to global/agent tool policy (deny still wins). Some channels use different nesting for rooms/channels, e.g. Discord `guilds.*.channels.*`, Slack `channels.*`, Microsoft Teams `teams.*.channels.*`.

## Group allowlists

When `channels.whatsapp.groups`, `channels.telegram.groups`, or `channels.imessage.groups` is configured, the keys act as a group allowlist; use `"*"` to allow all groups while still setting default mention behavior. A common confusion to avoid: DM pairing approval is NOT the same as group authorization — for channels that support DM pairing, the pairing store unlocks DMs only, and group commands still require explicit group sender authorization from config allowlists such as `groupAllowFrom` or the documented config fallback for that channel. The owner-only-triggers WhatsApp intent (combining `groupPolicy: "allowlist"` + `groupAllowFrom` + per-group `requireMention`):

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
      groups: { "*": { requireMention: true } },
    },
  },
}
```

Other copy/paste intents from the source: disable all group replies — `channels.whatsapp.groupPolicy: "disabled"`; allow only specific groups — `channels.whatsapp.groups: { "123@g.us": { requireMention: true }, "456@g.us": { requireMention: false } }`; allow all groups but require mention — `channels.whatsapp.groups: { "*": { requireMention: true } }`.

## Activation (owner-only)

Group owners can toggle per-group activation with two commands: `/activation mention` and `/activation always`. Owner is determined by `channels.whatsapp.allowFrom` (or the bot's self E.164 when unset); send the command as a standalone message. Other surfaces currently ignore `/activation`.

**Source**: OpenClaw documentation — `channels/groups` (mirror `inbox/openclaw_docs/channels/groups.md`)
**Last Updated**: 2026-06-22
**Status**: Active
