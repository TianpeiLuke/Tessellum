---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - telegram
keywords:
  - openclaw telegram setup
  - botfather token dmpolicy
  - telegram allowfrom groupallowfrom
  - telegram groups grouppolicy allowlist
  - telegram pairing approve
  - telegram privacy mode group identity
  - long polling vs webhook telegram
  - telegram getme has_topics_enabled
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/telegram
access_control_group: ["general"]
---

# OpenClaw — Setting Up the Telegram Channel

## Overview

This note is the setup + access-control procedure for the OpenClaw **Telegram** channel (production-ready for bot DMs and groups via grammY), mirroring the `channels/telegram` source page sections **Quick setup**, **Telegram side settings**, **Access control and activation**, and **Runtime behavior**. It covers creating the BotFather token, the minimal `channels.telegram` config and env fallback, gateway start + first-DM pairing approval, adding the bot to a group, the Telegram-side privacy/admin/BotFather toggles, the DM-policy and group/sender allowlist model (`dmPolicy`, `allowFrom`, `groupPolicy`, `groupAllowFrom`, `groups`), group bot identity, and the runtime transport behavior (deterministic routing, group/topic session isolation, long-polling watchdog, long polling vs webhook). The Telegram **feature reference, error-reply controls, full configuration reference, and troubleshooting** live in the sibling note [oc_channels_telegram_features](oc_channels_telegram_features.md).

## Quick setup

Telegram is **production-ready for bot DMs and groups via grammY**. **Long polling is the default mode; webhook mode is optional.** The default DM policy for Telegram is `pairing`. Setup is a four-step flow:

1. **Create the bot token in BotFather.** Open Telegram and chat with **@BotFather** (confirm the handle is exactly `@BotFather`). Run `/newbot`, follow the prompts, and save the token.
2. **Configure token and DM policy.** Add a `channels.telegram` block with the token, DM policy, and a default group rule:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

The env fallback `TELEGRAM_BOT_TOKEN=...` applies to the default account only. Telegram does **not** use `openclaw channels login telegram`; you configure the token in config/env, then start the gateway.

3. **Start gateway and approve the first DM.** Run the gateway, list pending pairings, and approve by code:

```bash
openclaw gateway
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

Pairing codes expire after 1 hour.

4. **Add the bot to a group.** Add the bot to your group, then get both IDs that group access needs: your Telegram user ID (used in `allowFrom` / `groupAllowFrom`) and the Telegram group chat ID (used as the key under `channels.telegram.groups`). For first-time setup, get the group chat ID from `openclaw logs --follow`, a forwarded-ID bot, or Bot API `getUpdates`; after the group is allowed, `/whoami@<bot_username>` can confirm the user and group IDs. Negative Telegram supergroup IDs that start with `-100` are group chat IDs — put them under `channels.telegram.groups`, **not** under `groupAllowFrom`.

**Token resolution** is account-aware: config values win over env fallback, and `TELEGRAM_BOT_TOKEN` only applies to the default account. After a successful startup, OpenClaw caches the bot identity in the state directory for up to 24 hours so restarts can avoid an extra Telegram `getMe` call; changing or removing the token clears that cache.

## Telegram side settings

These are the Telegram-platform-side toggles you set in BotFather / group settings, independent of OpenClaw config:

- **Privacy mode and group visibility** — Telegram bots default to **Privacy Mode**, which limits what group messages they receive. If the bot must see all group messages, either disable privacy mode via `/setprivacy`, or make the bot a group admin. When toggling privacy mode, remove + re-add the bot in each group so Telegram applies the change.
- **Group permissions** — admin status is controlled in Telegram group settings. Admin bots receive all group messages, which is useful for always-on group behavior.
- **Helpful BotFather toggles** — `/setjoingroups` to allow/deny group adds; `/setprivacy` for group visibility behavior.

## Access control and activation

### Group bot identity

In Telegram groups and forum topics, an explicit mention of the configured bot handle (for example `@my_bot`) is treated as addressing the selected OpenClaw agent, even when the agent persona name differs from the Telegram username. The group silence policy still applies to unrelated group traffic, but the bot handle itself is not considered "someone else."

### DM policy

`channels.telegram.dmPolicy` controls direct-message access: `pairing` (default), `allowlist` (requires at least one sender ID in `allowFrom`), `open` (requires `allowFrom` to include `"*"`), or `disabled`. `dmPolicy: "open"` with `allowFrom: ["*"]` lets any Telegram account that finds or guesses the bot username command the bot — use it only for intentionally public bots with tightly restricted tools; one-owner bots should use `allowlist` with numeric user IDs.

`channels.telegram.allowFrom` accepts numeric Telegram user IDs; `telegram:` / `tg:` prefixes are accepted and normalized. In multi-account configs, a restrictive top-level `channels.telegram.allowFrom` is treated as a safety boundary: account-level `allowFrom: ["*"]` entries do not make that account public unless the effective account allowlist still contains an explicit wildcard after merging. `dmPolicy: "allowlist"` with empty `allowFrom` blocks all DMs and is rejected by config validation. Setup asks for numeric user IDs only. If you upgraded and your config contains `@username` allowlist entries, run `openclaw doctor --fix` to resolve them (best-effort; requires a Telegram bot token); the same command can recover prior pairing-store allowlist entries into `channels.telegram.allowFrom` in allowlist flows.

For one-owner bots, prefer `dmPolicy: "allowlist"` with explicit numeric `allowFrom` IDs to keep access policy durable in config (instead of depending on previous pairing approvals). A common confusion: DM pairing approval does not mean "this sender is authorized everywhere" — pairing grants **DM** access only. If no command owner exists yet, the first approved pairing also sets `commands.ownerAllowFrom` so owner-only commands and exec approvals have an explicit operator account. Group sender authorization still comes from explicit config allowlists; to make one identity work for both DMs and group commands, put your numeric Telegram user ID in `channels.telegram.allowFrom` and ensure `commands.ownerAllowFrom` contains `telegram:<your user id>`.

**Finding your Telegram user ID** — the safer method (no third-party bot): (1) DM your bot, (2) run `openclaw logs --follow`, (3) read `from.id`. The official Bot API method:

```bash
curl "https://api.telegram.org/bot<bot_token>/getUpdates"
```

A less-private third-party method is `@userinfobot` or `@getidsbot`.

### Group policy and allowlists

Two controls apply together. **Which groups are allowed** is governed by `channels.telegram.groups`: with no `groups` config, `groupPolicy: "open"` lets any group pass group-ID checks while `groupPolicy: "allowlist"` (the default) blocks groups until you add `groups` entries (or `"*"`); a configured `groups` acts as an allowlist (explicit IDs or `"*"`). **Which senders are allowed in groups** is governed by `channels.telegram.groupPolicy`: `open`, `allowlist` (default), or `disabled`.

`groupAllowFrom` is used for group sender filtering; if not set, Telegram falls back to `allowFrom`. Its entries should be numeric Telegram user IDs (`telegram:` / `tg:` prefixes are normalized); non-numeric entries are ignored for sender authorization. Do **not** put Telegram group or supergroup chat IDs in `groupAllowFrom` — negative chat IDs belong under `channels.telegram.groups`. As a security boundary (`2026.2.25+`), group sender auth does **not** inherit DM pairing-store approvals: pairing stays DM-only, so for groups you set `groupAllowFrom` or per-group/per-topic `allowFrom`. Runtime note: if `channels.telegram` is completely missing, runtime defaults to fail-closed `groupPolicy="allowlist"` unless `channels.defaults.groupPolicy` is explicitly set.

The practical one-owner pattern is to set your user ID in `channels.telegram.allowFrom`, leave `groupAllowFrom` unset, and allow the target groups under `channels.telegram.groups`:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      dmPolicy: "pairing",
      allowFrom: ["<YOUR_TELEGRAM_USER_ID>"],
      groupPolicy: "allowlist",
      groups: {
        "<GROUP_CHAT_ID>": {
          requireMention: true,
        },
      },
    },
  },
}
```

Test it from the group with `@<bot_username> ping`; plain group messages do not trigger the bot while `requireMention: true`. To allow only specific users inside one specific group, set a per-group `allowFrom`:

```json5
{
  channels: {
    telegram: {
      groups: {
        "-1001234567890": {
          requireMention: true,
          allowFrom: ["8734062810", "745123456"],
        },
      },
    },
  },
}
```

A common mistake: `groupAllowFrom` is **not** a Telegram group allowlist. Put negative group/supergroup chat IDs like `-1001234567890` under `channels.telegram.groups`; put Telegram user IDs like `8734062810` under `groupAllowFrom` to limit which people inside an allowed group can trigger the bot; use `groupAllowFrom: ["*"]` only when any member of an allowed group should be able to talk to the bot.

### Mention behavior

Group replies require mention by default. A mention can come from a native `@botusername` mention, or from mention patterns in `agents.list[].groupChat.mentionPatterns` or `messages.groupChat.mentionPatterns`. Session-level command toggles `/activation always` and `/activation mention` update session state only — use config for persistence (for example `groups: { "*": { requireMention: false } }`). Group history context defaults to `mention-only` (prior group messages are included only when addressed to the bot, replies to the bot, or the bot's own messages); set `includeGroupHistoryContext: "recent"` to include recent room history for trusted groups, or `"none"` to send no prior Telegram group history with the next turn. To get the group chat ID, forward a group message to `@userinfobot` / `@getidsbot`, read `chat.id` from `openclaw logs --follow`, inspect Bot API `getUpdates`, or run `/whoami@<bot_username>` after the group is allowed (if native commands are enabled).

## Runtime behavior

Once set up, the Telegram channel runs with this transport behavior (owned by the gateway process):

- Telegram is owned by the gateway process; **routing is deterministic** — Telegram inbound replies back to Telegram (the model does not pick channels).
- Inbound messages normalize into the shared channel envelope with reply metadata, media placeholders, and persisted reply-chain context for Telegram replies the gateway has observed.
- **Group sessions are isolated by group ID.** Forum topics append `:topic:<threadId>` to keep topics isolated. DM messages can carry `message_thread_id`, which OpenClaw preserves for replies; DM topic sessions split only when Telegram `getMe` reports `has_topics_enabled: true` for the bot, otherwise DMs stay on the flat session.
- Long polling uses the grammY runner with per-chat/per-thread sequencing; overall runner sink concurrency uses `agents.defaults.maxConcurrent`. Multi-account startup bounds concurrent Telegram `getMe` probes so large bot fleets do not fan out every account probe at once.
- Long polling is guarded inside each gateway process so only one active poller can use a bot token at a time. If you still see `getUpdates` 409 conflicts, another OpenClaw gateway, script, or external poller is likely using the same token.
- The **long-polling watchdog** restarts after 120 seconds without completed `getUpdates` liveness by default; increase `channels.telegram.pollingStallThresholdMs` only if your deployment still sees false polling-stall restarts during long-running work — the value is in milliseconds, allowed from `30000` to `600000`, with per-account overrides supported.
- The Telegram Bot API has no read-receipt support, so `sendReadReceipts` does not apply.

The removed keys `channels.telegram.dm.threadReplies` and `channels.telegram.direct.<chatId>.threadReplies` no longer exist — run `openclaw doctor --fix` after upgrading if your config still has them. DM topic routing now follows the bot capability from Telegram `getMe.has_topics_enabled`, which is controlled by BotFather threaded mode: topics-enabled bots use thread-scoped DM sessions when Telegram sends `message_thread_id`; other DMs stay on the flat session.

**Long polling vs webhook (transport mode).** The default is long polling. For webhook mode, set `channels.telegram.webhookUrl` and `channels.telegram.webhookSecret`; optional `webhookPath`, `webhookHost`, `webhookPort` (defaults `/telegram-webhook`, `127.0.0.1`, `8787`). The local listener binds to `127.0.0.1:8787`; for public ingress, put a reverse proxy in front of the local port or set `webhookHost: "0.0.0.0"` intentionally. Webhook mode validates request guards, the Telegram secret token, and the JSON body before returning `200` to Telegram, then processes the update asynchronously through the same per-chat/per-topic bot lanes used by long polling, so slow agent turns do not hold Telegram's delivery ACK. (Detailed streaming/media/command/feature config lives in [oc_channels_telegram_features](oc_channels_telegram_features.md).)

**Source**: OpenClaw documentation — `channels/telegram` (mirror `inbox/openclaw_docs/channels/telegram.md`)
**Last Updated**: 2026-06-22
**Status**: Active
