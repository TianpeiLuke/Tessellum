---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - qqbot
keywords:
  - openclaw qqbot channel
  - qq bot setup appid appsecret
  - openclaw channels add qqbot
  - qqbot multi-account websocket
  - qqbot group chat allowlist
  - qqbot voice stt tts
  - qqbot target formats c2c group channel
  - qqbot slash commands bot-approve
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/qqbot
access_control_group: ["general"]
---

# OpenClaw — Connecting QQ Bot (Tencent QQ)

## Overview

This note is the operator procedure for connecting Tencent QQ to OpenClaw through the QQ Bot channel, mirroring the `channels/qqbot` source page. QQ Bot connects to OpenClaw via the official QQ Bot API (a WebSocket gateway); the plugin supports C2C private chat, group @messages, and guild channel messages with rich media (images, voice, video, files). It is a downloadable plugin — direct messages, group chats, guild channels, and media are supported, while reactions and threads are not. This note covers install, credential setup (AppID/AppSecret), configuration including multi-account and group-chat handling, voice STT/TTS, target formats, slash commands, the self-contained engine architecture, QR-code onboarding, and troubleshooting.

## Install

Install the QQ Bot plugin before setup:

```bash
openclaw plugins install @openclaw/qqbot
```

## Setup

1. Go to the [QQ Open Platform](https://q.qq.com/) and scan the QR code with your phone QQ to register / log in.
2. Click **Create Bot** to create a new QQ bot.
3. Find **AppID** and **AppSecret** on the bot's settings page and copy them. Note: AppSecret is not stored in plaintext — if you leave the page without saving it, you have to regenerate a new one.
4. Add the channel:

```bash
openclaw channels add --channel qqbot --token "AppID:AppSecret"
```

5. Restart the Gateway.

Interactive setup paths are also available via `openclaw channels add` (no flags) and `openclaw configure --section channels`.

## Configure

Minimal config supplies the AppID and AppSecret directly:

```json5
{
  channels: {
    qqbot: {
      enabled: true,
      appId: "YOUR_APP_ID",
      clientSecret: "YOUR_APP_SECRET",
    },
  },
}
```

The AppSecret can instead come from a file (`clientSecretFile: "/path/to/qqbot-secret.txt"`) or a structured env SecretRef (`clientSecret: { source: "env", provider: "default", id: "QQBOT_CLIENT_SECRET" }`). Default-account env vars are `QQBOT_APP_ID` and `QQBOT_CLIENT_SECRET`. Key behavior notes from source: env fallback applies to the default QQ Bot account only; `openclaw channels add --channel qqbot --token-file ...` provides the AppSecret only — the AppID must already be set in config or `QQBOT_APP_ID`; `clientSecret` also accepts SecretRef input, not just a plaintext string; and legacy `secretref:/...` marker strings are not valid `clientSecret` values — use structured SecretRef objects instead.

### Multi-account setup

Multiple QQ bots can run under a single OpenClaw instance by nesting additional accounts under `accounts`:

```json5
{
  channels: {
    qqbot: {
      enabled: true,
      appId: "111111111",
      clientSecret: "secret-of-bot-1",
      accounts: {
        bot2: {
          enabled: true,
          appId: "222222222",
          clientSecret: "secret-of-bot-2",
        },
      },
    },
  },
}
```

Each account launches its own WebSocket connection and maintains an independent token cache (isolated by `appId`). A second bot can also be added via CLI: `openclaw channels add --channel qqbot --account bot2 --token "222222222:secret-of-bot-2"`.

### Group chats

QQ Bot group chat support uses QQ group OpenIDs, not display names. Add the bot to a group, then mention it or configure the group to run without a mention. `groups["*"]` sets defaults for every group, and a concrete `groups.GROUP_OPENID` entry overrides those defaults for one group. Group settings: `requireMention` (require an @mention before the bot replies; default `true`); `ignoreOtherMentions` (drop messages that mention someone else but not the bot); `historyLimit` (keep recent non-mention group messages as context for the next mentioned turn — set `0` to disable); `tools` (allow/deny tools for the whole group); `toolsBySender` (per-sender group tool overrides); `name` (friendly label used in logs and group context); and `prompt` (per-group behavior prompt appended to the agent context). Old QQBot `toolPolicy` entries are retired — run `openclaw doctor --fix` to migrate them to `tools`. Activation modes are `mention` and `always`: `requireMention: true` maps to `mention`, `requireMention: false` maps to `always`, and a session-level activation override, when present, wins over config. The inbound queue is per peer — group peers get a larger queue cap, keep human messages ahead of bot-authored chatter when full, and merge bursts of normal group messages into one attributed turn; slash commands still run one by one.

### Voice (STT / TTS)

STT and TTS support two-level configuration with priority fallback. STT resolves from plugin-specific `channels.qqbot.stt`, falling back to framework `tools.media.audio.models[0]`; TTS resolves from `channels.qqbot.tts` / `channels.qqbot.accounts.<id>.tts`, falling back to `messages.tts`. Set `enabled: false` on either to disable. Account-level TTS overrides use the same shape as `messages.tts` and deep-merge over the channel/global TTS config. Inbound QQ voice attachments are exposed to agents as audio media metadata while keeping raw voice files out of generic `MediaPaths`; `[[audio_as_voice]]` plain-text replies synthesize TTS and send a native QQ voice message when TTS is configured. Outbound audio upload/transcode behavior is tuned with `channels.qqbot.audioFormatPolicy` via `sttDirectFormats`, `uploadDirectFormats`, and `transcodeEnabled`.

## Target formats

Outbound delivery targets address one of three QQ surfaces:

| Format                     | Description        |
| -------------------------- | ------------------ |
| `qqbot:c2c:OPENID`         | Private chat (C2C) |
| `qqbot:group:GROUP_OPENID` | Group chat         |
| `qqbot:channel:CHANNEL_ID` | Guild channel      |

Each bot has its own set of user OpenIDs: an OpenID received by Bot A **cannot** be used to send messages via Bot B.

## Slash commands

Built-in commands are intercepted before the AI queue: `/bot-ping` (latency test), `/bot-version` (show the OpenClaw framework version), `/bot-help` (list all commands), `/bot-me` (show the sender's QQ user ID / openid for `allowFrom`/`groupAllowFrom` setup), `/bot-upgrade` (show the QQBot upgrade guide link), `/bot-logs` (export recent gateway logs as a file), and `/bot-approve` (approve a pending QQ Bot action — for example, confirming a C2C or group upload — through the native flow). Append `?` to any command for usage help (for example `/bot-upgrade ?`).

Admin commands (`/bot-me`, `/bot-upgrade`, `/bot-logs`, `/bot-clear-storage`, `/bot-streaming`, `/bot-approve`) are direct-message-only and require the sender's openid in an explicit non-wildcard `allowFrom` list. A wildcard `allowFrom: ["*"]` permits chat but does not grant admin command access. Group messages match against `groupAllowFrom` first and fall back to `allowFrom`; running an admin command in a group returns a hint rather than silently dropping. When QQ Bot exec approvals use the default same-chat fallback, native approval button clicks follow the same explicit non-wildcard command allowlist — to grant approval-only access without broader command access, configure `channels.qqbot.execApprovals.approvers`.

## Engine architecture

QQ Bot ships as a self-contained engine inside the plugin. Each account owns an isolated resource stack (WebSocket connection, API client, token cache, media storage root) keyed by `appId`, and accounts never share inbound/outbound state. The multi-account logger tags log lines with the owning account so diagnostics stay separable when several bots run under one gateway. Inbound, outbound, and gateway bridge paths share a single media payload root under `~/.openclaw/media`, so uploads, downloads, and transcode caches land under one guarded directory instead of a per-subsystem tree. Rich media delivery goes through one `sendMedia` path for C2C and group targets: local files and buffers above the large-file threshold use QQ's chunked upload endpoints, while smaller payloads use the one-shot media API. Credentials can be backed up and restored as part of standard OpenClaw credential snapshots, and the engine re-attaches each account's resource stack on restore without requiring a fresh QR-code pair.

## QR-code onboarding

As an alternative to pasting `AppID:AppSecret` manually, the engine supports a QR-code onboarding flow for linking a QQ Bot to OpenClaw: (1) run the QQ Bot setup path (for example `openclaw channels add --channel qqbot`) and pick the QR-code flow when prompted; (2) scan the generated QR code with the phone app tied to the target QQ Bot; (3) approve the pairing on the phone — OpenClaw persists the returned credentials into `credentials/` under the right account scope. Approval prompts generated by the bot itself (for example, "allow this action?" flows exposed by the QQ Bot API) surface as native OpenClaw prompts that you can accept with `/bot-approve` rather than replying through the raw QQ client.

## Troubleshooting

- **Bot replies "gone to Mars":** credentials not configured or Gateway not started.
- **No inbound messages:** verify `appId` and `clientSecret` are correct, and the bot is enabled on the QQ Open Platform.
- **Repeated self-replies:** OpenClaw records QQ outbound ref indexes as bot-authored and ignores inbound events whose current `msgIdx` matches that same bot account. This prevents platform echo loops while still allowing users to quote or reply to previous bot messages.
- **Setup with `--token-file` still shows unconfigured:** `--token-file` only sets the AppSecret. You still need `appId` in config or `QQBOT_APP_ID`.
- **Proactive messages not arriving:** QQ may intercept bot-initiated messages if the user hasn't interacted recently.
- **Voice not transcribed:** ensure STT is configured and the provider is reachable.

**Source**: OpenClaw documentation — `channels/qqbot` (mirror `inbox/openclaw_docs/channels/qqbot.md`)
**Last Updated**: 2026-06-22
**Status**: Active
