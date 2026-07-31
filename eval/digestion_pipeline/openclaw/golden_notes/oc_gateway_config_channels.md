---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - channels
keywords:
  - openclaw channels config
  - channels dm policy group policy
  - channels.modelByChannel
  - channels.defaults heartbeat
  - per-channel config keys
  - slack discord telegram whatsapp config
  - multi-account channels
  - imessage matrix signal mattermost
topics:
  - OpenClaw
  - Channel Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/config-channels
access_control_group: ["general"]
---

# OpenClaw — Per-Channel Transport Configuration

## Overview

This note is the per-channel transport configuration procedure under the `channels.*` config tree, mirroring the `gateway/config-channels` source page (the `## Channels` H2 minus the mention-gating/commands half, which lives in `oc_gateway_config_channels_routing_commands`). It covers the shared DM/group access policies, channel-to-model pinning, channel defaults and heartbeat, the per-platform config blocks (WhatsApp, Telegram, Discord, Google Chat, Slack, Mattermost, Signal, iMessage, Matrix, Microsoft Teams, IRC), and the cross-channel multi-account setup. Each channel starts automatically when its config section exists unless `enabled: false`. Top-level keys for agents, tools, and gateway runtime live in the separate Configuration reference page.

## DM and group access (shared across channels)

All channels support DM policies and group policies. The DM policy values are `pairing` (default — unknown senders get a one-time pairing code the owner must approve), `allowlist` (only senders in `allowFrom` or the paired allow store), `open` (allow all inbound DMs; requires `allowFrom: ["*"]`), and `disabled` (ignore all inbound DMs). The group policy values are `allowlist` (default — only groups matching the configured allowlist), `open` (bypass group allowlists; mention-gating still applies), and `disabled` (block all group/room messages). `channels.defaults.groupPolicy` sets the default when a provider's `groupPolicy` is unset. Pairing codes expire after 1 hour, and pending DM pairing requests are capped at 3 per channel. If a provider block is missing entirely (`channels.<provider>` absent), runtime group policy falls back to `allowlist` (fail-closed) with a startup warning.

## Channel model overrides

Use `channels.modelByChannel` to pin specific channel IDs to a model. Values accept `provider/model` or configured model aliases, and the channel mapping applies only when a session does not already have a model override (for example one set via `/model`).

```json5
{
  channels: {
    modelByChannel: {
      discord: { "123456789012345678": "anthropic/claude-opus-4-6" },
      slack: { C1234567890: "openai/gpt-5.5" },
      telegram: {
        "-1001234567890": "openai/gpt-5.4-mini",
        "-1001234567890:topic:99": "anthropic/claude-sonnet-4-6",
      },
    },
  },
}
```

## Channel defaults and heartbeat

`channels.defaults` carries shared group-policy and heartbeat behavior across providers: `groupPolicy` is the fallback when a provider-level `groupPolicy` is unset; `contextVisibility` is the default supplemental-context mode (`all` includes all quoted/thread/history context, `allowlist` includes context only from allowlisted senders, `allowlist_quote` is allowlist but keeps explicit quote/reply context — per-channel override `channels.<channel>.contextVisibility`); and the `heartbeat` block controls `showOk` (include healthy statuses), `showAlerts` (include degraded/error statuses), and `useIndicator` (compact indicator-style output).

```json5
{
  channels: {
    defaults: {
      groupPolicy: "allowlist", // open | allowlist | disabled
      contextVisibility: "all", // all | allowlist | allowlist_quote
      heartbeat: { showOk: false, showAlerts: true, useIndicator: true },
    },
  },
}
```

## Per-platform config blocks

Each platform exposes its own keys under `channels.<provider>`. Common patterns across platforms: an `enabled` switch, a token/credential key, `dmPolicy` + `allowFrom`, `groups`/`groupPolicy` with per-group `requireMention`, `historyLimit`, `mediaMaxMb`, `chunkMode`/`textChunkLimit`, `streaming` mode, `actions.*` capability toggles, `retry`, and an optional `defaultAccount`. Tokens accept plaintext or SecretRef objects, and env-var fallbacks apply only to the default account.

- **WhatsApp** — runs through the gateway's `web` channel (Baileys Web) and starts when a linked session exists; transport tuning (`keepAliveIntervalMs`, `connectTimeoutMs`, `reconnect`) lives under `web`, while access/policy keys (`dmPolicy`, `allowFrom`, `textChunkLimit`, `chunkMode`, `mediaMaxMb`, `sendReadReceipts`, `groups`, `groupPolicy`, `groupAllowFrom`) live under `channels.whatsapp`. Legacy single-account Baileys auth dir is migrated by `openclaw doctor` into `whatsapp/default`.
- **Telegram** — `botToken` or `tokenFile` (symlinks rejected), `TELEGRAM_BOT_TOKEN` fallback for the default account; `apiRoot` is the Bot API root only (not the `/bot<TOKEN>` URL — `openclaw doctor --fix` strips an accidental suffix); supports `customCommands`, `streaming` (default `off`; opt into `partial`/`block`/`progress` to avoid preview-edit rate limits), `network` tuning, `webhookUrl`/`webhookSecret`/`webhookPath`, and `configWrites: false` to block Telegram-initiated config writes.
- **Discord** — `token` with `DISCORD_BOT_TOKEN` fallback; rich `actions.*`, `guilds.<id>` with per-channel overrides, `threadBindings` (`/focus`/`/unfocus` thread-bound routing, `spawnSessions`, `defaultSpawnContext`), `voice` (auto-join, DAVE encryption, TTS), `execApprovals`, `streaming.mode` default `progress`, `suppressEmbeds` default `true`, `maxLinesPerMessage` default 17, and `mentionAliases`. Use `user:<id>` (DM) or `channel:<id>` delivery targets; bare numeric IDs are rejected.
- **Google Chat** — `serviceAccount`/`serviceAccountFile`/`serviceAccountRef` (env fallbacks `GOOGLE_CHAT_SERVICE_ACCOUNT`/`_FILE`), `audienceType` (`app-url`|`project-number`), `audience`, `webhookPath`, `botUser`, `dm` block, `groupPolicy`/`groups`; delivery targets `spaces/<spaceId>` or `users/<userId>`.
- **Slack** — socket mode requires `botToken` + `appToken` (env `SLACK_BOT_TOKEN`/`SLACK_APP_TOKEN`), HTTP mode requires `botToken` + `signingSecret`; tokens accept SecretRef; `socketMode` transport tuning (`clientPingTimeout` default `15000`), `thread.historyScope`/`inheritParent` isolation, `slashCommand` block, `streaming.mode` + `nativeTransport`, `unfurlLinks`/`unfurlMedia` (default `false`), `typingReaction`, and `execApprovals`. Account snapshots expose `botTokenStatus`/`appTokenStatus`/`signingSecretStatus`.
- **Mattermost** — bundled plugin (`openclaw plugins install @openclaw/mattermost` for older builds); `botToken`, `baseUrl`, `chatmode` (`oncall` default | `onmessage` | `onchar` with `oncharPrefixes`), `commands` (`native` opt-in, `callbackPath`/`callbackUrl`), `requireMention`, per-channel `groups.<channelId>.requireMention`.
- **Signal** — `account` (pin a Signal identity), `dmPolicy`, `allowFrom` (phone or `uuid:`), `configWrites`, `reactionNotifications`/`reactionAllowlist`, `historyLimit`.
- **iMessage** — spawns `imsg rpc` (JSON-RPC over stdio; no daemon/port). BlueBubbles support was removed (`channels.bluebubbles` is not a supported surface — migrate to `channels.imessage`). Keys: `cliPath` (can be an SSH wrapper; set `remoteHost` for SCP), `dbPath`, `dmPolicy`, `allowFrom`, `includeAttachments` (off by default), `attachmentRoots`/`remoteAttachmentRoots`, `sendTransport` (`auto`|`bridge`|`applescript`), `actions.*`. Requires Full Disk Access to the Messages DB; prefer `chat_id:<id>` targets.
- **Matrix** — plugin-backed; token auth (`accessToken`) or password auth (`userId` + `password`), `homeserver`, `proxy` (per-account overridable), `encryption`, `initialSyncLimit`, `defaultAccount`, `autoJoin` (default `off`), `dm.sessionScope` (`per-user` default | `per-room`), `execApprovals`. Full config in the Matrix channel page.
- **Microsoft Teams** — plugin-backed under `channels.msteams`; core keys `channels.msteams` and `channels.msteams.configWrites`; full credentials/webhook/policy config in the Microsoft Teams page.
- **IRC** — plugin-backed under `channels.irc`; core keys `channels.irc.dmPolicy`, `channels.irc.configWrites`, `channels.irc.nickserv.*`; full host/port/TLS/channels config in the IRC page.

## Multi-account (all channels)

Run multiple accounts per channel, each keyed by its own `accountId` under `channels.<provider>.accounts`:

```json5
{
  channels: {
    telegram: {
      accounts: {
        default: { name: "Primary bot", botToken: "123456:ABC..." },
        alerts: { name: "Alerts bot", botToken: "987654:XYZ..." },
      },
    },
  },
}
```

The `default` account is used when `accountId` is omitted (CLI + routing), env tokens only apply to the default account, and base channel settings apply to all accounts unless overridden per account. Use `bindings[].match.accountId` to route each account to a different agent. When you add a non-default account (`openclaw channels add` or onboarding) while still on a single-account top-level config, OpenClaw promotes account-scoped top-level single-account values into the channel account map first (most channels into `accounts.default`; Matrix can preserve an existing matching named/default target). `openclaw doctor --fix` repairs mixed shapes the same way. Existing channel-only bindings (no `accountId`) keep matching the default account.

## Other plugin channels

Many plugin channels are configured as `channels.<id>` and documented in their dedicated channel pages — for example Feishu, Matrix, LINE, Nostr, Zalo, Nextcloud Talk, Synology Chat, and Twitch. See the full channel index for the complete catalog.

**Source**: OpenClaw documentation — `gateway/config-channels` (mirror `inbox/openclaw_docs/gateway/config-channels.md`)
**Last Updated**: 2026-06-22
**Status**: Active
