---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - wecom
keywords:
  - wecom enterprise wechat
  - ai bot websocket gateway
  - aibot_subscribe authentication
  - aes-256-cbc media decryption
  - per-group sender allowlist
  - exponential backoff reconnection
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/wecom
access_control_group: ["general"]
---

# WeCom (Enterprise WeChat) Gateway Setup

## Overview

This note is the **setup-and-run procedure** for connecting Hermes Agent to **WeCom** (企业微信 / Enterprise WeChat), Tencent's enterprise messaging platform, through WeCom's **AI Bot WebSocket gateway**. Unlike the [WeCom Callback adapter](hermes_gateway_wecom_callback_setup.md) — which receives inbound webhooks on a public HTTP endpoint — this adapter opens a persistent outbound WebSocket to `wss://openws.work.weixin.qq.com` for real-time bidirectional communication, so **no public endpoint or webhook is needed**. The procedure is: create an AI Bot in the WeCom Admin Console (scan-to-create or manual), configure credentials and access policies, then start the gateway. The note covers the connection lifecycle (`aibot_subscribe` auth + 30s heartbeat), DM/group access policies with per-group sender allowlists, AES-256-CBC inbound media decryption with size-based outbound downgrade, reply-mode response correlation (`aibot_respond_msg`), and exponential-backoff reconnection. It plugs into the shared messaging gateway concept (link-out) and is implemented by the `gw_platform_wecom_*` adapter code.

## Prerequisites

- A WeCom organization account
- An AI Bot created in the WeCom Admin Console
- The Bot ID and Secret from the bot's credentials page
- Python packages: `aiohttp` and `httpx`

## Setup

### Step 1: Create an AI Bot

**Recommended — scan-to-create (one command):** run `hermes gateway setup`, select **WeCom**, and scan the QR code with your WeCom mobile app. Hermes automatically creates a bot application with the correct permissions and saves the credentials. The wizard displays a QR code in your terminal, waits for the scan, retrieves the Bot ID and Secret, and guides you through access-control configuration.

**Alternative — manual setup:** if scan-to-create is unavailable, the wizard falls back to manual input: log in to the WeCom Admin Console, navigate to **Applications → Create Application → AI Bot**, configure the bot name and description, copy the **Bot ID** and **Secret** from the credentials page, then run `hermes gateway setup`, select **WeCom**, and enter the credentials when prompted. Keep the Bot Secret private — anyone with it can impersonate your bot.

### Step 2: Configure Hermes

Interactive setup (recommended) runs `hermes gateway setup`, select **WeCom**, and the wizard guides you through bot credentials (QR scan or manual entry), access-control settings (allowlist, pairing mode, or open access), and a home channel for notifications. For manual configuration, add the following to `~/.hermes/.env`:

```bash
WECOM_BOT_ID=your-bot-id
WECOM_SECRET=your-secret

# Optional: restrict access
WECOM_ALLOWED_USERS=user_id_1,user_id_2

# Optional: home channel for cron/notifications
WECOM_HOME_CHANNEL=chat_id
```

### Step 3: Start the gateway

```bash
hermes gateway
```

## Features

- **WebSocket transport** — persistent connection, no public endpoint needed
- **DM and group messaging** — configurable access policies
- **Per-group sender allowlists** — fine-grained control over who can interact in each group
- **Media support** — images, files, voice, video upload and download
- **AES-encrypted media** — automatic decryption for inbound attachments
- **Quote context** — preserves reply threading
- **Markdown rendering** — rich text responses
- **Reply correlation** — responses are correlated to the inbound message context
- **Auto-reconnect** — exponential backoff on connection drops

The WeCom adapter delivers each response as a single complete message — it does **not** stream responses token-by-token, and it does **not** show a typing indicator. "Reply correlation" only threads a response to its inbound request; it is not live streaming.

## Configuration Options

Set these in `config.yaml` under `platforms.wecom.extra`: `bot_id` (required WeCom AI Bot ID), `secret` (required AI Bot Secret), `websocket_url` (default `wss://openws.work.weixin.qq.com`), `dm_policy` (default `open`; one of `open`, `allowlist`, `disabled`, `pairing`), `group_policy` (default `open`; one of `open`, `allowlist`, `disabled`), `allow_from` (default `[]`, user IDs allowed for DMs when `dm_policy=allowlist`), `group_allow_from` (default `[]`, group IDs allowed when `group_policy=allowlist`), and `groups` (default `{}`, per-group configuration — see Access Policies).

## Access Policies

**DM policy** controls who can direct-message the bot: `open` (anyone, default), `allowlist` (only user IDs in `allow_from`), `disabled` (all DMs ignored), or `pairing` (pairing mode for initial setup). Set with `WECOM_DM_POLICY=allowlist`.

**Group policy** controls which groups the bot responds in: `open` (all groups, default), `allowlist` (only group IDs in `group_allow_from`), or `disabled` (all group messages ignored). Set with `WECOM_GROUP_POLICY=allowlist`.

**Per-group sender allowlists** add fine-grained control over which users can interact with the bot within specific groups, configured in `config.yaml`:

```yaml
platforms:
  wecom:
    enabled: true
    extra:
      bot_id: "your-bot-id"
      secret: "your-secret"
      group_policy: "allowlist"
      group_allow_from:
        - "group_id_1"
        - "group_id_2"
      groups:
        group_id_1:
          allow_from:
            - "user_alice"
            - "user_bob"
        group_id_2:
          allow_from:
            - "user_charlie"
        "*":
          allow_from:
            - "user_admin"
```

How it works: (1) `group_policy` and `group_allow_from` determine whether a group is allowed at all; (2) if a group passes the top-level check, its `groups.<group_id>.allow_from` list (if present) further restricts which senders within that group can interact; (3) a wildcard `"*"` group entry serves as a default for groups not explicitly listed; (4) allowlist entries support the `*` wildcard to allow all users, and entries are case-insensitive; (5) entries can optionally use the `wecom:user:` or `wecom:group:` prefix format — the prefix is stripped automatically. If no `allow_from` is configured for a group, all users in that group are allowed (assuming the group passes the top-level policy check).

## Media Support

**Inbound (receiving):** the adapter receives media attachments and caches them locally for agent processing — **images** (URL-based and base64-encoded, downloaded and cached), **files** (downloaded with original filename preserved), **voice** (text transcription extracted if available), and **mixed messages** (text + images parsed and all components extracted). Media from quoted (replied-to) messages is also extracted so the agent has reply context.

**AES-encrypted media decryption:** WeCom encrypts some inbound media with AES-256-CBC, handled automatically — when an inbound media item includes an `aeskey` field, the adapter downloads the encrypted bytes and decrypts them using AES-256-CBC with PKCS#7 padding. The AES key is the base64-decoded value of `aeskey` (must be exactly 32 bytes), and the IV is derived from the first 16 bytes of the key. This requires the `cryptography` Python package (`pip install cryptography`). No configuration is needed.

**Outbound (sending):** `send` sends Markdown text (4000 chars), `send_image` / `send_image_file` send native images (10 MB), `send_document` sends file attachments (20 MB), `send_voice` sends voice (AMR format only, 2 MB), and `send_video` sends video (10 MB). Files are uploaded in 512 KB chunks via a three-step protocol (init → chunks → finish), handled automatically. **Automatic downgrade:** when media exceeds the native type's size limit but is under the absolute 20 MB file limit, it is sent as a generic file attachment instead — images > 10 MB → file, videos > 10 MB → file, voice > 2 MB → file, non-AMR audio → file (WeCom only supports AMR for native voice). Files exceeding the absolute 20 MB limit are rejected with an informational message sent to the chat.

## Reply-Mode Responses

When the bot receives a message via the WeCom callback, the adapter remembers the inbound request ID. If a response is sent while the request context is still active, the adapter uses WeCom's reply-mode (`aibot_respond_msg`) to correlate the response directly to the inbound message, for a more natural conversation experience. The full response is delivered as a single message — the adapter does not stream tokens incrementally. If the inbound request context has expired or is unavailable, the adapter falls back to proactive message sending via `aibot_send_msg`. Reply-mode also works for media: uploaded media can be sent as a reply to the originating message.

## Connection and Reconnection

The adapter maintains a persistent WebSocket connection to WeCom's gateway at `wss://openws.work.weixin.qq.com`. The **connection lifecycle** is: (1) **Connect** — opens a WebSocket and sends an `aibot_subscribe` authentication frame with the `bot_id` and `secret`; (2) **Heartbeat** — sends application-level ping frames every 30 seconds to keep the connection alive; (3) **Listen** — continuously reads inbound frames and dispatches message callbacks.

On connection loss, the adapter uses exponential backoff to reconnect — 1st retry 2 s, 2nd 5 s, 3rd 10 s, 4th 30 s, 5th+ 60 s. After each successful reconnection the backoff counter resets to zero, and all pending request futures are failed on disconnect so callers don't hang indefinitely.

**Deduplication:** inbound messages are deduplicated using message IDs with a 5-minute window and a maximum cache of 1000 entries, preventing double-processing during reconnection or network hiccups.

## All Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WECOM_BOT_ID` | ✅ | — | WeCom AI Bot ID |
| `WECOM_SECRET` | ✅ | — | WeCom AI Bot Secret |
| `WECOM_ALLOWED_USERS` | — | _(empty)_ | Comma-separated user IDs for the gateway-level allowlist |
| `WECOM_HOME_CHANNEL` | — | — | Chat ID for cron/notification output |
| `WECOM_WEBSOCKET_URL` | — | `wss://openws.work.weixin.qq.com` | WebSocket gateway URL |
| `WECOM_DM_POLICY` | — | `open` | DM access policy |
| `WECOM_GROUP_POLICY` | — | `open` | Group access policy |

## Troubleshooting

- `WECOM_BOT_ID and WECOM_SECRET are required` → set both env vars or configure in the setup wizard.
- `WeCom startup failed: aiohttp not installed` / `httpx not installed` → `pip install aiohttp` / `pip install httpx`.
- `invalid secret (errcode=40013)` → verify the secret matches your bot's credentials.
- `Timed out waiting for subscribe acknowledgement` → check network connectivity to `openws.work.weixin.qq.com`.
- Bot doesn't respond in groups → check `group_policy` and ensure the group ID is in `group_allow_from`; bot ignores certain users in a group → check per-group `allow_from` lists in `groups`.
- Media decryption fails / `cryptography is required for WeCom media decryption` → `pip install cryptography`.
- Voice messages or images sent as files → WeCom only supports AMR for native voice; images > 10 MB exceed the native image limit; both auto-downgrade to file. `File too large` → WeCom enforces a 20 MB absolute upload limit; compress or split.
- `Timeout sending message to WeCom` / `WeCom websocket closed during authentication` → the WebSocket may have disconnected (check logs for reconnection messages) or credentials are incorrect.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/wecom.md`
**Last Updated**: 2026-06-19
**Status**: Active
