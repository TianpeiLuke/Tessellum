---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - yuanbao
keywords:
  - yuanbao gateway setup
  - tencent enterprise messaging
  - hmac websocket authentication
  - cos media upload
  - sethome home channel
  - dm group access policy
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/yuanbao
access_control_group: ["general"]
---

# Hermes Agent — Yuanbao Gateway Setup

## Overview

This is the platform-setup procedure for connecting Hermes Agent to **Yuanbao**, Tencent's enterprise messaging platform. The Yuanbao adapter is a **WebSocket-gateway** connector: it opens a single outbound WebSocket to the Yuanbao API, authenticates with **HMAC-signed** requests derived from an `APP_ID`/`APP_SECRET` pair, and then receives and sends messages in real time across both direct (C2C) and group conversations. It is one of the Chinese-platform adapters that plug into the shared Hermes messaging gateway; this note documents *how to configure and run it* (create a bot → run the setup wizard → set env vars → start the gateway → secure access), while the gateway concept, session model, voice/media subsystem, and cron-delivery machinery live in their own notes (link-outs below).

Per the source, Yuanbao "uses WebSocket for real-time communication, HMAC-based authentication, and supports rich media including images, files, and voice messages." Media is uploaded through **COS** (Tencent Cloud Object Storage), and scheduled-task (cron) output is delivered to a designated **home channel** set via `/sethome` or auto-detected from the first user to message the bot.

## Prerequisites

- A Yuanbao account with bot creation permissions
- Yuanbao APP_ID and APP_SECRET (from platform admin)
- Python packages: `websockets` and `httpx`
- For media support: `aiofiles`

Install the required dependencies:

```bash
pip install websockets httpx aiofiles
```

## Setup

**1. Create a Bot in Yuanbao** — Download the Yuanbao app from `https://yuanbao.tencent.com/`, go to **PAI → My Bot**, create a new bot, then copy its **APP_ID** and **APP_SECRET**.

**2. Run the Setup Wizard** — The easiest path is the interactive setup; select **Yuanbao** when prompted, and the wizard asks for APP_ID and APP_SECRET, then saves the configuration automatically. The WebSocket URL and API Domain have sensible defaults built in, so only APP_ID and APP_SECRET are required to get started.

```bash
hermes gateway setup
```

**3. Configure Environment Variables** — After initial setup, verify these in `~/.hermes/.env`:

```bash
# Required
YUANBAO_APP_ID=your-app-id
YUANBAO_APP_SECRET=your-app-secret
YUANBAO_WS_URL=wss://api.yuanbao.example.com/ws
YUANBAO_API_DOMAIN=https://api.yuanbao.example.com

# Optional: bot account ID (normally obtained automatically from sign-token)
# YUANBAO_BOT_ID=your-bot-id

# Optional: internal routing environment (e.g. test/staging/production)
# YUANBAO_ROUTE_ENV=production

# Optional: home channel for cron/notifications (format: direct:<account> or group:<group_code>)
YUANBAO_HOME_CHANNEL=direct:bot_account_id
YUANBAO_HOME_CHANNEL_NAME="Bot Notifications"

# Optional: restrict access (legacy, see Access Control below for fine-grained policies)
YUANBAO_ALLOWED_USERS=user_account_1,user_account_2
```

**4. Start the Gateway** — The adapter connects to the Yuanbao WebSocket gateway, authenticates using HMAC signatures, and begins processing messages.

```bash
hermes gateway
```

## Features

The adapter supports: a **WebSocket gateway** for real-time bidirectional communication; **HMAC authentication** (secure request signing with APP_ID/APP_SECRET); **C2C** (direct user-to-bot) and **group** messaging; **media support** for images, files, and voice via COS; **Markdown formatting** with automatic chunking for Yuanbao's size limits; **message deduplication** to prevent duplicate processing; **heartbeat/keep-alive** for connection stability; **typing indicators**; **automatic reconnection** with exponential backoff; **group information queries** (group details and member lists); **sticker/emoji support** (TIMFaceElem stickers); **auto-sethome** (first user to message the bot becomes the home-channel owner); and **slow-response notification** (a waiting message when the agent takes longer than expected).

## Configuration Options

### Chat ID Formats

Yuanbao uses prefixed identifiers depending on conversation type:

| Chat Type | Format | Example |
|-----------|--------|---------|
| Direct message (C2C) | `direct:<account>` | `direct:user123` |
| Group message | `group:<group_code>` | `group:grp456` |

### Media Uploads

The adapter automatically handles media uploads via COS (Tencent Cloud Object Storage): **images** (JPEG, PNG, GIF, WebP), **files** (all common document types), and **voice** (WAV, MP3, OGG). Per the source, "Media URLs are automatically validated and downloaded before upload to prevent SSRF attacks." (Voice/STT media handling itself is the SP08 voice subsystem — link-out, not duplicated here.)

## Home Channel

Use the `/sethome` command in any Yuanbao chat (DM or group) to designate it as the **home channel**; scheduled tasks (cron jobs) deliver their results there. With auto-sethome, if no home channel is configured the first user to message the bot is automatically set as the home-channel owner, and if the current home channel is a group chat, the first DM upgrades it to a direct channel. It can also be set manually in `~/.hermes/.env`:

```bash
YUANBAO_HOME_CHANNEL=direct:user_account_id
# or for a group:
# YUANBAO_HOME_CHANNEL=group:group_code
YUANBAO_HOME_CHANNEL_NAME="My Bot Updates"
```

Setting it interactively: start a conversation with the bot, send `/sethome`, and the bot responds "Home channel set to [chat_name] with ID [chat_id]. Cron jobs will deliver to this location." Future cron jobs and notifications are then sent to that channel. The cron scheduling subsystem itself is documented separately (link-out).

## Usage Tips

Send any message (e.g. `hello`) to the bot and it responds in the same conversation thread. Standard Hermes slash commands work on Yuanbao — `/new` (start a fresh conversation), `/model [provider:model]` (show or change the model), `/sethome` (set this chat as the home channel), `/status` (show session info), and `/help` (show available commands); the full slash-command reference is link-out detail. To send a file, attach it directly in the Yuanbao chat — the bot downloads and processes the attachment, optionally with an accompanying message. When you ask the bot to create or export a file, it sends the file directly back to your Yuanbao chat.

## Troubleshooting

- **Bot is online but not responding** — authentication failed during the WebSocket handshake: verify APP_ID/APP_SECRET, check the WebSocket URL is accessible, ensure the bot account has proper permissions, and review `~/.hermes/logs/gateway.log`.
- **"Connection refused"** — the WebSocket URL is unreachable or incorrect: verify the URL begins with `wss://`, check connectivity to the API domain, confirm the firewall allows WebSocket connections, and test with `curl -I https://[YUANBAO_API_DOMAIN]`.
- **Media uploads fail** — COS credentials are invalid or the media server is unreachable: verify API_DOMAIN, check media-upload permissions for your bot, ensure the file is accessible and uncorrupted, and review the COS bucket configuration with platform admin.
- **Messages not delivered to home channel** — the home-channel ID format is wrong or the cron job hasn't triggered: verify `YUANBAO_HOME_CHANNEL` format, use `/sethome` to auto-detect, check the schedule with `/status`, and verify send permissions in the target chat.
- **Frequent disconnections** — an unstable WebSocket/network: check logs for error patterns, increase the heartbeat timeout, ensure a stable network, and consider verbose logging (`HERMES_LOG_LEVEL=debug`).

## Access Control

Yuanbao supports fine-grained access control for both DM and group conversations via environment variables:

```bash
# DM policy: open (default) | allowlist | disabled
YUANBAO_DM_POLICY=open
# Comma-separated user IDs allowed to DM the bot (only used when DM_POLICY=allowlist)
YUANBAO_DM_ALLOW_FROM=user_id_1,user_id_2

# Group policy: open (default) | allowlist | disabled
YUANBAO_GROUP_POLICY=open
# Comma-separated group codes allowed (only used when GROUP_POLICY=allowlist)
YUANBAO_GROUP_ALLOW_FROM=group_code_1,group_code_2
```

These can also be set in `config.yaml` under the `platforms.yuanbao.extra` block (e.g. `dm_policy: allowlist`, `dm_allow_from: "user1,user2"`, `group_policy: open`, `group_allow_from: ""`). The `platforms.*` config-block schema and group-session isolation model are owned by the messaging-media-settings note (link-out).

## Advanced Configuration

**Message Chunking** — Yuanbao has a maximum message size; Hermes automatically chunks large responses with Markdown-aware splitting that respects code fences, tables, and paragraph boundaries.

**Connection Parameters** — the adapter ships with built-in defaults (not configurable via environment variables; optimized for typical Yuanbao deployments):

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| WebSocket connect timeout | 15 seconds | Time to wait for WS handshake |
| Heartbeat interval | 30 seconds | Ping frequency to keep connection alive |
| Max reconnect attempts | 100 | Maximum number of reconnection tries |
| Reconnect backoff | 1s → 60s (exponential) | Wait time between reconnect attempts |
| Reply heartbeat interval | 2 seconds | RUNNING status send frequency |
| Send timeout | 30 seconds | Timeout for outbound WS messages |

**Verbose Logging** — enable debug logging to troubleshoot connection issues by running the gateway with `HERMES_LOG_LEVEL=debug hermes gateway`.

## Integration with Other Features

Yuanbao integrates with the broader Hermes feature set: **cron jobs** scheduled with the `/cron` slash command (e.g. `/cron "0 */4 * * *" Report system health`) deliver results to the home channel; **background tasks** (`/background Analyze all files in the archive`) run long operations without blocking the conversation; and **cross-platform messages** can be sent from the CLI to Yuanbao with `hermes chat -q "Send 'Hello from CLI' to yuanbao:group:group_code"`. The cron/background subsystems are documented in their own notes (link-outs below).

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/yuanbao.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/yuanbao
**Last Updated**: 2026-06-19
**Status**: Active
