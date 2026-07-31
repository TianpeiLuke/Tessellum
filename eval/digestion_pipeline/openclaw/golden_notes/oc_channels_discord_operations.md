---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - discord
keywords:
  - openclaw discord troubleshooting
  - discord gateway ready timeout
  - discord event queue listener timeout
  - openclaw doctor channels status probe
  - discord bot loop protection allowbots
  - discord configuration reference fields
  - discord decryptionfailed voice recovery
  - discord safety operations least privilege
topics:
  - OpenClaw
  - Discord Channel Operations
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/discord
access_control_group: ["general"]
---

# OpenClaw — Operating a Discord Channel (Troubleshooting, Config Reference, Safety)

## Overview

This note is the operations runbook for an OpenClaw Discord channel: how to diagnose common Discord failures, where the high-signal configuration fields live, and the safety guidance for running the bot. It mirrors the closing three sections of the `channels/discord` source page — **Troubleshooting**, **Configuration reference**, and **Safety and operations** — and is the procedure companion to the setup (`oc_channels_discord_setup`), runtime/access (`oc_channels_discord_routing_access`), feature (`oc_channels_discord_features`), and voice (`oc_channels_discord_voice`) notes. Use it when an already-configured Discord bot misbehaves at runtime: missing guild messages, blocked messages, slow or duplicate turns, gateway timeouts, permission-probe mismatches, DM/pairing failures, bot-to-bot loops, or voice decrypt drops.

## Troubleshooting common failures

The source page presents troubleshooting as an accordion of named symptoms, each with a fix list. The useful first-line diagnostic commands are `openclaw doctor`, `openclaw channels status --probe`, and `openclaw logs --follow`.

```bash
openclaw doctor
openclaw channels status --probe
openclaw logs --follow
```

- **Used disallowed intents or bot sees no guild messages** — enable the Message Content Intent; enable the Server Members Intent when you depend on user/member resolution; restart the gateway after changing intents.
- **Guild messages blocked unexpectedly** — verify `groupPolicy`; verify the guild allowlist under `channels.discord.guilds`; if a guild `channels` map exists, only listed channels are allowed; verify `requireMention` behavior and mention patterns.
- **Require mention false but still blocked** — common causes are `groupPolicy="allowlist"` without a matching guild/channel allowlist, `requireMention` configured in the wrong place (it must be under `channels.discord.guilds` or a channel entry), or a sender blocked by the guild/channel `users` allowlist.
- **Long-running Discord turns or duplicate replies** — typical logs are `Slow listener detected ...` and `stuck session: sessionKey=agent:...:discord:... state=processing ...`. Discord does **not** apply a channel-owned timeout to queued agent turns: message listeners hand off immediately, and queued Discord runs preserve per-session ordering until the session/tool/runtime lifecycle completes or aborts the work. The gateway queue knob `channels.discord.eventQueue.listenerTimeout` (or `channels.discord.accounts.<accountId>.eventQueue.listenerTimeout` for multi-account) controls only Discord gateway listener work, not agent turn lifetime.

```json5
{
  channels: {
    discord: {
      accounts: {
        default: {
          eventQueue: {
            listenerTimeout: 120000,
          },
        },
      },
    },
  },
}
```

- **Gateway metadata lookup timeout warnings** — OpenClaw fetches Discord `/gateway/bot` metadata before connecting; transient failures fall back to Discord's default gateway URL and are rate-limited in logs. Knobs: `channels.discord.gatewayInfoTimeoutMs` (single-account), `channels.discord.accounts.<accountId>.gatewayInfoTimeoutMs` (multi-account), env fallback `OPENCLAW_DISCORD_GATEWAY_INFO_TIMEOUT_MS`; default `30000` (30 seconds), max `120000`.
- **Gateway READY timeout restarts** — OpenClaw waits for Discord's gateway `READY` event during startup and after runtime reconnects; multi-account setups with startup staggering can need a longer window. Startup knobs: `channels.discord.gatewayReadyTimeoutMs`, `channels.discord.accounts.<accountId>.gatewayReadyTimeoutMs`, env fallback `OPENCLAW_DISCORD_READY_TIMEOUT_MS`; startup default `15000` (15 seconds), max `120000`. Runtime knobs: `channels.discord.gatewayRuntimeReadyTimeoutMs`, `channels.discord.accounts.<accountId>.gatewayRuntimeReadyTimeoutMs`, env fallback `OPENCLAW_DISCORD_RUNTIME_READY_TIMEOUT_MS`; runtime default `30000` (30 seconds), max `120000`.
- **Permissions audit mismatches** — `channels status --probe` permission checks only work for numeric channel IDs; with slug keys runtime matching can still work but the probe cannot fully verify permissions.
- **DM and pairing issues** — DM disabled via `channels.discord.dm.enabled=false`; DM policy disabled via `channels.discord.dmPolicy="disabled"` (legacy: `channels.discord.dm.policy`); or the request is awaiting pairing approval in `pairing` mode.
- **Voice STT drops with `DecryptionFailed(...)`** — keep OpenClaw current (`openclaw update`) so the Discord voice receive-recovery logic is present; confirm `channels.discord.voice.daveEncryption=true` (default); start from `channels.discord.voice.decryptionFailureTolerance=24` (upstream default) and tune only if needed; watch for `discord voice: DAVE decrypt failures detected` and `discord voice: repeated decrypt failures; attempting rejoin`.

### Bot-to-bot loop suppression

By default bot-authored messages are ignored. If you set `channels.discord.allowBots=true`, use strict mention and allowlist rules to avoid loop behavior; prefer `channels.discord.allowBots="mentions"` to accept only bot messages that mention the bot. OpenClaw also ships shared bot loop protection: whenever `allowBots` lets bot-authored messages reach dispatch, Discord maps the inbound event to `(account, channel, bot pair)` facts and the generic pair guard suppresses the pair after it crosses the configured event budget (it does not affect single-bot deployments or one-shot replies under budget). Default settings active when `allowBots` is set: `maxEventsPerWindow: 20` (messages a pair may exchange within the window), `windowSeconds: 60` (sliding window length), `cooldownSeconds: 60` (drop window once the budget trips). Configure the shared default once under `channels.defaults.botLoopProtection`, then override Discord when a legitimate workflow needs more headroom; precedence is `channels.discord.accounts.<account>.botLoopProtection` → `channels.discord.botLoopProtection` → `channels.defaults.botLoopProtection` → built-in defaults. Discord uses the generic `maxEventsPerWindow`, `windowSeconds`, and `cooldownSeconds` keys.

```json5
{
  channels: {
    defaults: {
      botLoopProtection: {
        maxEventsPerWindow: 20,
        windowSeconds: 60,
        cooldownSeconds: 60,
      },
    },
    discord: {
      botLoopProtection: { maxEventsPerWindow: 4 },
      accounts: {
        molty: {
          allowBots: true,
          botLoopProtection: {
            maxEventsPerWindow: 5,
            windowSeconds: 60,
            cooldownSeconds: 90,
          },
        },
      },
    },
  },
}
```

## Configuration reference

The primary reference is the gateway docs at `/gateway/config-channels#discord`. The source page groups the high-signal Discord fields by concern:

- **startup/auth**: `enabled`, `token`, `accounts.*`, `allowBots`
- **policy**: `groupPolicy`, `dm.*`, `guilds.*`, `guilds.*.channels.*`
- **command**: `commands.native`, `commands.useAccessGroups`, `configWrites`, `slashCommand.*`
- **event queue**: `eventQueue.listenerTimeout` (listener budget), `eventQueue.maxQueueSize`, `eventQueue.maxConcurrency`
- **gateway**: `gatewayInfoTimeoutMs`, `gatewayReadyTimeoutMs`, `gatewayRuntimeReadyTimeoutMs`
- **reply/history**: `replyToMode`, `historyLimit`, `dmHistoryLimit`, `dms.*.historyLimit`
- **delivery**: `textChunkLimit`, `chunkMode`, `maxLinesPerMessage`
- **streaming**: `streaming` (legacy alias: `streamMode`), `streaming.preview.toolProgress`, `draftChunk`, `blockStreaming`, `blockStreamingCoalesce`
- **media/retry**: `mediaMaxMb` (caps outbound Discord uploads, default `100MB`), `retry`
- **actions**: `actions.*`
- **presence**: `activity`, `status`, `activityType`, `activityUrl`
- **UI**: `ui.components.accentColor`
- **features**: `threadBindings`, top-level `bindings[]` (`type: "acp"`), `pluralkit`, `execApprovals`, `intents`, `agentComponents.enabled`, `agentComponents.ttlMs`, `heartbeat`, `responsePrefix`

## Safety and operations

The source page closes with three operational rules: treat bot tokens as secrets (`DISCORD_BOT_TOKEN` is preferred in supervised environments); grant least-privilege Discord permissions; and if command deploy/state is stale, restart the gateway and re-check with `openclaw channels status --probe`.

**Source**: OpenClaw documentation — `channels/discord` (Troubleshooting / Configuration reference / Safety and operations) (mirror `inbox/openclaw_docs/channels/discord.md`)
**Last Updated**: 2026-06-22
**Status**: Active
