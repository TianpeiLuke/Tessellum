---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - discord
keywords:
  - discord runtime model
  - discord access control routing
  - dmPolicy groupPolicy allowlist
  - guild allowlist users roles
  - role-based agent routing bindings
  - accessGroup discord channelAudience
  - native slash commands command auth
  - forum channel thread posts
  - discord session keys
  - requireMention ignoreOtherMentions
topics:
  - OpenClaw
  - Discord Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/discord
access_control_group: ["general"]
---

# OpenClaw — Discord Runtime Model, Access Control, and Routing

## Overview

This note is the procedure for how OpenClaw maps Discord inbound messages to agent sessions and gates who may trigger the agent: the runtime model (connection ownership, deterministic reply routing, session-key shapes), forum-channel handling, DM and guild access control (`dmPolicy` / `groupPolicy` / allowlists / shared `accessGroup` entries), role-based agent routing via `bindings`, and native (slash) command registration plus command auth. It mirrors the Runtime model, Forum channels, Access control and routing (incl. Role-based agent routing), and Native commands and command auth sections of the `channels/discord` source page. Setup/pairing is in `oc_channels_discord_setup`; feature/components reference is in `oc_channels_discord_features`; troubleshooting and the config reference are in `oc_channels_discord_operations`.

## Runtime Model

The gateway owns the Discord connection, and reply routing is deterministic — Discord inbound replies back to Discord. Discord guild/channel metadata is added to the model prompt as untrusted context, not as a user-visible reply prefix; if a model copies that envelope back, OpenClaw strips the copied metadata from outbound replies and from future replay context. Session mapping follows fixed rules:

- By default (`session.dmScope=main`), direct chats share the agent main session (`agent:main:main`).
- Guild channels are isolated session keys (`agent:<agentId>:discord:channel:<channelId>`).
- Group DMs are ignored by default (`channels.discord.dm.groupEnabled=false`).
- Native slash commands run in isolated command sessions (`agent:<agentId>:discord:slash:<userId>`), while still carrying `CommandTargetSessionKey` to the routed conversation session.
- Text-only cron/heartbeat announce delivery to Discord uses the final assistant-visible answer once. Media and structured component payloads remain multi-message when the agent emits multiple deliverable payloads.

## Forum Channels

Discord forum and media channels only accept thread posts. OpenClaw supports two ways to create them: send a message to the forum parent (`channel:<forumId>`) to auto-create a thread (the thread title uses the first non-empty line of your message), or use `openclaw message thread create` to create a thread directly (do not pass `--message-id` for forum channels). Forum parents do not accept Discord components; if you need components, send to the thread itself (`channel:<threadId>`).

```bash
# Send to forum parent to auto-create a thread
openclaw message send --channel discord --target channel:<forumId> \
  --message "Topic title\nBody of the post"

# Create a forum thread explicitly
openclaw message thread create --channel discord --target channel:<forumId> \
  --thread-name "Topic title" --message "Body of the post"
```

## Access Control and Routing

Access control for Discord is split across DM policy, dynamic access groups, guild policy, and mention gating.

### DM Policy

`channels.discord.dmPolicy` controls DM access; `channels.discord.allowFrom` is the canonical DM allowlist. Values are `pairing` (default), `allowlist`, `open` (requires `channels.discord.allowFrom` to include `"*"`), and `disabled`. If DM policy is not open, unknown users are blocked (or prompted for pairing in `pairing` mode). Multi-account precedence: `channels.discord.accounts.default.allowFrom` applies only to the `default` account; for one account, `allowFrom` takes precedence over legacy `dm.allowFrom`; named accounts inherit `channels.discord.allowFrom` when their own `allowFrom` and legacy `dm.allowFrom` are unset; named accounts do not inherit `channels.discord.accounts.default.allowFrom`. Legacy `channels.discord.dm.policy` and `channels.discord.dm.allowFrom` still read for compatibility, and `openclaw doctor --fix` migrates them to `dmPolicy` and `allowFrom` when it can do so without changing access. DM target formats for delivery are `user:<id>` and `<@id>` mention; bare numeric IDs normally resolve as channel IDs when a channel default is active, but IDs listed in the account's effective DM `allowFrom` are treated as user DM targets for compatibility.

### Access Groups

Discord DMs and text command authorization can use dynamic `accessGroup:<name>` entries in `channels.discord.allowFrom`. Access group names are shared across message channels: use `type: "message.senders"` for a static group whose members are expressed in each channel's normal `allowFrom` syntax, or `type: "discord.channelAudience"` when a Discord channel's current `ViewChannel` audience should define membership dynamically. A Discord text channel has no separate member list, so `type: "discord.channelAudience"` models membership as: the DM sender is a member of the configured guild and currently has effective `ViewChannel` permission on the configured channel after role and channel overwrites are applied. Lookups fail closed — if Discord returns `Missing Access`, the member lookup fails, or the channel belongs to a different guild, the DM sender is treated as unauthorized. Enable the Discord Developer Portal **Server Members Intent** for the bot when using channel-audience access groups, because DMs do not include guild member state and OpenClaw resolves the member through Discord REST at authorization time. Shared access-group behavior is documented in `oc_channels_access_groups`.

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

### Guild Policy

Guild handling is controlled by `channels.discord.groupPolicy`, with values `open`, `allowlist`, and `disabled`. The secure baseline when `channels.discord` exists is `allowlist`. Under `allowlist`: the guild must match `channels.discord.guilds` (`id` preferred, slug accepted); optional sender allowlists are `users` (stable IDs recommended) and `roles` (role IDs only), and if either is configured, senders are allowed when they match `users` OR `roles`; direct name/tag matching is disabled by default, so enable `channels.discord.dangerouslyAllowNameMatching: true` only as break-glass compatibility mode; names/tags are supported for `users` but IDs are safer, and `openclaw security audit` warns when name/tag entries are used; if a guild has `channels` configured, non-listed channels are denied; if a guild has no `channels` block, all channels in that allowlisted guild are allowed. If you only set `DISCORD_BOT_TOKEN` and do not create a `channels.discord` block, runtime fallback is `groupPolicy="allowlist"` (with a warning in logs), even if `channels.defaults.groupPolicy` is `open`.

```json5
{
  channels: {
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        "123456789012345678": {
          requireMention: true,
          ignoreOtherMentions: true,
          users: ["987654321098765432"],
          roles: ["123456789012345678"],
          channels: {
            general: { allow: true },
            help: { allow: true, requireMention: true },
          },
        },
      },
    },
  },
}
```

### Mentions and Group DMs

Guild messages are mention-gated by default. Mention detection includes explicit bot mention, configured mention patterns (`agents.list[].groupChat.mentionPatterns`, fallback `messages.groupChat.mentionPatterns`), and implicit reply-to-bot behavior in supported cases. When writing outbound Discord messages, use canonical mention syntax — `<@USER_ID>` for users, `<#CHANNEL_ID>` for channels, and `<@&ROLE_ID>` for roles — and do not use the legacy `<@!USER_ID>` nickname mention form. `requireMention` is configured per guild/channel (`channels.discord.guilds...`), and `ignoreOtherMentions` optionally drops messages that mention another user/role but not the bot (excluding @everyone/@here). For group DMs, the default is ignored (`dm.groupEnabled=false`), with an optional allowlist via `dm.groupChannels` (channel IDs or slugs).

## Role-Based Agent Routing

Use `bindings[].match.roles` to route Discord guild members to different agents by role ID. Role-based bindings accept role IDs only and are evaluated after peer or parent-peer bindings and before guild-only bindings. If a binding also sets other match fields (for example `peer` + `guildId` + `roles`), all configured fields must match.

```json5
{
  bindings: [
    {
      agentId: "opus",
      match: {
        channel: "discord",
        guildId: "123456789012345678",
        roles: ["111111111111111111"],
      },
    },
    {
      agentId: "sonnet",
      match: {
        channel: "discord",
        guildId: "123456789012345678",
      },
    },
  ],
}
```

## Native Commands and Command Auth

`commands.native` defaults to `"auto"` and is enabled for Discord, with the per-channel override `channels.discord.commands.native`. `commands.native=false` skips Discord slash-command registration and cleanup during startup, and previously registered commands may remain visible in Discord until you remove them from the Discord app. Native command auth uses the same Discord allowlists/policies as normal message handling; commands may still be visible in the Discord UI for users who are not authorized, but execution still enforces OpenClaw auth and returns "not authorized". The default slash command setting is `ephemeral: true`. See the OpenClaw Slash commands docs for the command catalog and behavior.

**Source**: OpenClaw documentation — `channels/discord` (mirror `inbox/openclaw_docs/channels/discord.md`), sections Runtime model / Forum channels / Access control and routing / Role-based agent routing / Native commands and command auth
**Last Updated**: 2026-06-22
**Status**: Active
