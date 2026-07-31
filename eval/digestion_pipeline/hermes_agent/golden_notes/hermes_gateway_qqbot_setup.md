---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - qq_bot
keywords:
  - qq bot setup
  - official qq bot api v2
  - websocket gateway rest api
  - voice transcription stt fallback
  - dm group access policy
  - sandbox production routing
topics:
  - Hermes Agent
  - Messaging Platforms
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/qqbot
access_control_group: ["general"]
---

# QQ Bot Setup

## Overview

This note is the **setup-and-run procedure for Hermes's QQ Bot adapter** — the messaging adapter that bridges QQ (Tencent's consumer chat platform) to a Hermes agent through the **Official QQ Bot API (v2)**. It covers registering a QQ Bot application, enabling the required message intents, wiring credentials into `~/.hermes/.env` (or `config.yaml`), choosing sandbox vs production routing, configuring DM/group access policy, enabling two-stage voice transcription, and troubleshooting connection and delivery failures. The adapter receives messages over a persistent WebSocket connection to the QQ Gateway and sends text/markdown replies back via the REST API, spanning four conversation surfaces: private (C2C), group @-mentions, guild, and direct messages.

The adapter is one of the per-platform plug-ins that registers with Hermes's messaging gateway; the shared gateway concept, DM pairing, and group-session isolation are documented in the messaging gateway/overview notes (link-outs below), and this page focuses only on *how to configure and run* the QQ surface. Start the adapter the same way as any other platform — interactively via `hermes gateway setup` or by setting the required environment variables and running the gateway.

## Prerequisites

Register a QQ Bot Application at [q.qq.com](https://q.qq.com):

- Create a new application and note your **App ID** and **App Secret**.
- Enable the required intents: **C2C messages, Group @-messages, Guild messages**.
- Configure your bot in **sandbox mode** for testing, or **publish** for production.

The adapter requires the `aiohttp` and `httpx` Python dependencies:

```bash
pip install aiohttp httpx
```

## Configuration

### Interactive setup

```bash
hermes gateway setup
```

Select **QQ Bot** from the platform list and follow the prompts.

### Manual configuration

Set the required environment variables in `~/.hermes/.env`:

```bash
QQ_APP_ID=your-app-id
QQ_CLIENT_SECRET=your-app-secret
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `QQ_APP_ID` | QQ Bot App ID (required) | — |
| `QQ_CLIENT_SECRET` | QQ Bot App Secret (required) | — |
| `QQBOT_HOME_CHANNEL` | OpenID for cron/notification delivery | — |
| `QQBOT_HOME_CHANNEL_NAME` | Display name for home channel | `Home` |
| `QQ_ALLOWED_USERS` | Comma-separated user OpenIDs for DM access | open (all users) |
| `QQ_GROUP_ALLOWED_USERS` | Comma-separated group OpenIDs for group access | — |
| `QQ_ALLOW_ALL_USERS` | Set to `true` to allow all DMs | `false` |
| `QQ_PORTAL_HOST` | Override the QQ portal host (set to `sandbox.q.qq.com` for sandbox routing) | `q.qq.com` |
| `QQ_STT_API_KEY` | API key for voice-to-text provider | — |
| `QQ_STT_BASE_URL` | (Not read directly — set `platforms.qqbot.extra.stt.baseUrl` in `config.yaml` instead) | n/a |
| `QQ_STT_MODEL` | STT model name | `glm-asr` |

Credential auth (App ID + App Secret) backs the WebSocket Gateway connection and REST sends. Setting `QQ_PORTAL_HOST` to `sandbox.q.qq.com` routes a sandbox-only bot to QQ's test channel; the production default is `q.qq.com`. Access is gated by the DM/group allowlist variables above.

## Advanced Configuration

For fine-grained control, add platform settings to `~/.hermes/config.yaml`:

```yaml
platforms:
  qqbot:
    enabled: true
    extra:
      app_id: "your-app-id"
      client_secret: "your-secret"
      markdown_support: true       # enable QQ markdown (msg_type 2). Config-only; no env-var equivalent.
      dm_policy: "open"          # open | allowlist | disabled
      allow_from:
        - "user_openid_1"
      group_policy: "open"       # open | allowlist | disabled
      group_allow_from:
        - "group_openid_1"
      stt:
        provider: "zai"          # zai (GLM-ASR), openai (Whisper), etc.
        baseUrl: "https://open.bigmodel.cn/api/coding/paas/v4"
        apiKey: "your-stt-key"
        model: "glm-asr"
```

QQ markdown rendering (`markdown_support`, message type 2) is config-only with no env-var equivalent. `dm_policy` and `group_policy` each accept `open | allowlist | disabled`, with `allow_from` / `group_allow_from` listing the permitted user/group OpenIDs under each policy.

## Voice Messages (STT)

Voice transcription works in **two stages**:

1. **QQ built-in ASR** (free, always tried first) — QQ provides `asr_refer_text` in voice message attachments, which uses Tencent's own speech recognition.
2. **Configured STT provider** (fallback) — If QQ's ASR doesn't return text, the adapter calls an OpenAI-compatible STT API:
   - **Zhipu/GLM (`zai`)**: Default provider, uses the `glm-asr` model.
   - **OpenAI Whisper**: Set `QQ_STT_BASE_URL` and `QQ_STT_MODEL`.
   - Any OpenAI-compatible STT endpoint.

The broader voice/STT subsystem (real-time transcription, voice mode) is owned by the media/voice notes linked below; this page only documents the QQ-specific two-stage fallback chain.

## Troubleshooting

**Bot disconnects immediately (quick disconnect)** — usually means: invalid App ID / Secret (double-check credentials at q.qq.com); missing permissions (ensure the required intents are enabled); or a sandbox-only bot (a bot in sandbox mode can only receive messages from QQ's sandbox test channel).

**Voice messages not transcribed** — check if QQ's built-in `asr_refer_text` is present in the attachment data; if using a custom STT provider, verify `QQ_STT_API_KEY` is set correctly; check gateway logs for STT error messages.

**Messages not delivered** — verify the bot's **intents** are enabled at q.qq.com; check `QQ_ALLOWED_USERS` if DM access is restricted; for group messages, ensure the bot is **@mentioned** (group policy may require allowlisting); check `QQBOT_HOME_CHANNEL` for cron/notification delivery.

**Connection errors** — ensure `aiohttp` and `httpx` are installed (`pip install aiohttp httpx`); check network connectivity to `api.sgroup.qq.com` and the WebSocket gateway; review gateway logs for detailed error and reconnect behavior.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/qqbot.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/qqbot
**Last Updated**: 2026-06-19
**Status**: Active
