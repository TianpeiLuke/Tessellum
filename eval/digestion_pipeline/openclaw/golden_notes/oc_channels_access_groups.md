---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - access_groups
keywords:
  - openclaw access groups
  - accessgroup reference
  - message.senders group
  - allowfrom groupallowfrom allowlist
  - discord.channelaudience
  - dmpolicy grouppolicy
  - resolveaccessgroupallowfromstate
  - fail closed allowlist
topics:
  - OpenClaw
  - Channel Access Groups
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/access-groups
access_control_group: ["general"]
---

# OpenClaw — Channel Access Groups (Reusable Sender Allowlists)

## Overview

This note is the procedure for configuring OpenClaw **access groups**: named sender lists you define once and reference from channel allowlists with `accessGroup:<name>`, so the same trusted set can apply across several message channels and to both DMs and group sender authorization. It mirrors the `channels/access-groups` source page in full — defining static `message.senders` groups, referencing them from per-channel `allowFrom` / `groupAllowFrom` (and per-room) allowlists, the supported channel paths and bundled-support list, plugin diagnostics, the dynamic `discord.channelAudience` group type, the fail-closed security rules, and troubleshooting. The load-bearing rule throughout: an access group grants nothing by itself; it only matters when an allowlist field references it.

## Static message sender groups

Static sender groups use `type: "message.senders"`. Define them under a top-level `accessGroups` map, where each named group lists `members` keyed by message-channel id:

```json5
{
  accessGroups: {
    operators: {
      type: "message.senders",
      members: {
        "*": ["global-owner-id"],
        discord: ["discord:123456789012345678"],
        telegram: ["987654321"],
        whatsapp: ["+15551234567"],
      },
    },
  },
}
```

Member lists are keyed by message-channel id. The `"*"` key holds shared entries checked for every message channel that references the group; a channel-specific key (e.g. `discord`, `telegram`, `whatsapp`) holds entries checked only for that channel's allowlist matching. Entries are matched with the destination channel's normal `allowFrom` rules, and **OpenClaw does not translate sender ids between channels** — if Alice has both a Telegram id and a Discord id, you must list both ids under the appropriate keys.

## Reference groups from allowlists

Reference a group with `accessGroup:<name>` anywhere the message-channel path supports sender allowlists. A DM allowlist reference sets `dmPolicy: "allowlist"` and puts the group in `allowFrom`:

```json5
{
  channels: {
    discord: {
      dmPolicy: "allowlist",
      allowFrom: ["accessGroup:operators"],
    },
    telegram: {
      dmPolicy: "allowlist",
      allowFrom: ["accessGroup:operators"],
    },
  },
}
```

A group sender (group-chat) allowlist reference sets `groupPolicy: "allowlist"` and puts the group in `groupAllowFrom`; channels with per-room sender allowlists (e.g. Google Chat `spaces.<id>.users`) accept the same `accessGroup:<name>` reference:

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["accessGroup:oncall"],
    },
    googlechat: {
      spaces: {
        "spaces/AAA": {
          users: ["accessGroup:oncall"],
        },
      },
    },
  },
}
```

You can mix groups and direct entries in the same allowlist array — for example `allowFrom: ["accessGroup:operators", "discord:123456789012345678"]`.

## Supported message-channel paths

Access groups are available in shared message-channel authorization paths, including: DM sender allowlists such as `channels.<channel>.allowFrom`; group sender allowlists such as `channels.<channel>.groupAllowFrom`; channel-specific per-room sender allowlists that use the same sender matching rules; and command authorization paths that reuse message-channel sender allowlists. Channel support depends on whether that channel is wired through the shared OpenClaw sender-authorization helpers. Current bundled support includes **Discord, Feishu, Google Chat, iMessage, LINE, Mattermost, Microsoft Teams, Nextcloud Talk, Nostr, QQBot, Signal, WhatsApp, Zalo, and Zalo Personal**. Static `message.senders` groups are designed to be channel-agnostic, so new message channels should support them by using the shared plugin SDK helpers instead of custom allowlist expansion.

## Plugin diagnostics

Plugin authors can inspect structured access-group state without expanding it back into a flat allowlist by calling `resolveAccessGroupAllowFromState` from `openclaw/plugin-sdk/security-runtime`:

```typescript
import { resolveAccessGroupAllowFromState } from "openclaw/plugin-sdk/security-runtime";

const state = await resolveAccessGroupAllowFromState({
  accessGroups: cfg.accessGroups,
  allowFrom: channelConfig.allowFrom,
  channel: "my-channel",
  accountId: "default",
  senderId,
  isSenderAllowed,
});
```

The result reports **referenced, matched, missing, unsupported, and failed** groups; use this when you need diagnostics or conformance tests. Use `expandAllowFromWithAccessGroups(...)` only for compatibility paths that still expect a flat `allowFrom` array.

## Discord channel audiences

Discord also supports a dynamic access group type, `type: "discord.channelAudience"`, which references a guild channel by `guildId` / `channelId` and a `membership` predicate (e.g. `"canViewChannel"`) rather than a static member list:

```json5
{
  accessGroups: {
    maintainers: {
      type: "discord.channelAudience",
      guildId: "1456350064065904867",
      channelId: "1456744319972282449",
      membership: "canViewChannel",
    },
  },
  channels: {
    discord: {
      dmPolicy: "allowlist",
      allowFrom: ["accessGroup:maintainers"],
    },
  },
}
```

`discord.channelAudience` means "allow Discord DM senders who can currently view this guild channel." OpenClaw resolves the sender through Discord at authorization time and applies Discord `ViewChannel` permission rules. Use it when a Discord channel is already the source of truth for a team, such as `#maintainers` or `#on-call`. Requirements and failure behavior: the bot needs access to the guild and channel; the bot needs the Discord Developer Portal **Server Members Intent**; and the access group **fails closed** when Discord returns `Missing Access`, the sender cannot be resolved as a guild member, or the channel belongs to another guild. (More Discord-specific examples live in the Discord access-control documentation.)

## Security notes

Access groups are **allowlist aliases, not roles** — they do not create owners, approve pairing requests, or grant tool permissions by themselves. `dmPolicy: "open"` still requires `"*"` in the effective DM allowlist; referencing an access group is not the same as public access. **Missing group names fail closed**: if `allowFrom` contains `accessGroup:operators` and `accessGroups.operators` is absent, that entry authorizes nobody. Keep channel ids stable, and prefer numeric/user ids over display names when the channel supports both.

## Troubleshooting

If a sender should match but is blocked, work through these checks in order: (1) confirm the allowlist field contains the exact `accessGroup:<name>` reference; (2) confirm `accessGroups.<name>.type` is correct; (3) confirm the sender id is listed under the matching channel key, or under `"*"`; (4) confirm the entry uses that channel's normal allowlist syntax; (5) for Discord channel audiences, confirm the bot can see the guild channel and has Server Members Intent enabled. Run `openclaw doctor` after editing access-control config — it catches many invalid allowlist and policy combinations before runtime.

**Source**: OpenClaw documentation — `channels/access-groups` (mirror `inbox/openclaw_docs/channels/access-groups.md`)
**Last Updated**: 2026-06-22
**Status**: Active
