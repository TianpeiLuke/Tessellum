---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - weixin
keywords:
  - weixin wechat gateway
  - ilink bot api
  - long-poll transport
  - aes-128-ecb cdn
  - context token persistence
  - qr login wizard
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/weixin
access_control_group: ["general"]
---

# Hermes Gateway — Weixin (WeChat) Setup

## Overview

This is the procedure for connecting the Hermes Agent messaging gateway to **personal WeChat / Weixin** (微信) accounts via Tencent's **iLink Bot API**. It is distinct from the WeCom (Enterprise WeChat) adapter — Weixin targets personal accounts, WeCom targets corporate ones. The adapter receives messages over **HTTP long-polling** (not WebSocket and not a public webhook), so no public endpoint is required: the gateway calls `getupdates` and the server holds the request open until messages arrive. Setup is QR-login based (`hermes gateway setup`), credentials persist to `~/.hermes/weixin/accounts/`, and the run loop adds AES-128-ECB encrypted CDN media, disk-backed `context_token` reply continuity, smart chunking, typing indicators, and 5-minute deduplication.

The most important operational caveat is the **iLink bot identity limitation**: QR login binds Hermes to an iLink bot identity (e.g. `a5ace6fd482e@im.bot`), not a fully scriptable personal account. That identity generally cannot be invited into ordinary WeChat groups and typically does not receive ordinary group events, so in practice most deployments only get reliable DMs. The `WEIXIN_GROUP_POLICY` settings only matter when iLink actually delivers group events for your account type, which is often not the case.

## Prerequisites

- A personal WeChat account.
- Python packages `aiohttp` and `cryptography`.
- Terminal QR rendering, included when Hermes is installed with the `messaging` extra.

```bash
pip install aiohttp cryptography
# Optional: for terminal QR code display
pip install hermes-agent[messaging]
```

## Setup

### 1. Run the Setup Wizard

The interactive setup is the easiest path. Run `hermes gateway setup` and select **Weixin** when prompted. The wizard requests a QR code from the iLink Bot API, displays it in your terminal (or provides a URL), waits for you to scan it with the WeChat mobile app, prompts you to confirm the login on your phone, and saves credentials automatically to `~/.hermes/weixin/accounts/`. On success you see `微信连接成功，account_id=your-account-id`. The wizard stores the `account_id`, `token`, and `base_url` so you do not configure them manually.

```bash
hermes gateway setup
```

### 2. Configure Environment Variables

After the initial QR login, set at minimum the account ID in `~/.hermes/.env`. The token is normally auto-saved from QR login; access restriction, legacy multiline splitting, and a cron home channel are optional.

```bash
WEIXIN_ACCOUNT_ID=your-account-id

# Optional: override the token (normally auto-saved from QR login)
# WEIXIN_TOKEN=your-bot-token

# Optional: restrict access
WEIXIN_DM_POLICY=open
WEIXIN_ALLOWED_USERS=user_id_1,user_id_2

# Optional: home channel for cron/notifications
WEIXIN_HOME_CHANNEL=chat_id
WEIXIN_HOME_CHANNEL_NAME=Home
```

### 3. Start the Gateway

```bash
hermes gateway
```

The adapter restores saved credentials, connects to the iLink API, and begins long-polling for messages.

## Features

The adapter offers long-poll transport (no public endpoint, webhook, or WebSocket needed), QR-code scan-to-connect login, DM messaging with configurable access policies (group messaging depends on iLink delivering group events for the connected identity, often not the case), media support (images, video, files, voice), **AES-128-ECB encrypted CDN** with automatic encryption/decryption for all media transfers, **context-token persistence** (disk-backed reply continuity across restarts), Markdown preservation (headers, tables, code fences), smart message chunking, typing indicators, **SSRF protection** (outbound media URLs validated before download), 5-minute-window message deduplication, and automatic retry with backoff.

## Configuration Options

Set these in `config.yaml` under `platforms.weixin.extra`:

| Key | Default | Description |
|-----|---------|-------------|
| `account_id` | — | iLink Bot account ID (required) |
| `token` | — | iLink Bot token (required, auto-saved from QR login) |
| `base_url` | `https://ilinkai.weixin.qq.com` | iLink API base URL |
| `cdn_base_url` | `https://novac2c.cdn.weixin.qq.com/c2c` | CDN base URL for media transfer |
| `dm_policy` | `open` | DM access: `open`, `allowlist`, `disabled`, `pairing` |
| `group_policy` | `disabled` | Group access: `open`, `allowlist`, `disabled` |
| `allow_from` | `[]` | User IDs allowed for DMs (when dm_policy=allowlist) |
| `group_allow_from` | `[]` | Group IDs allowed (when group_policy=allowlist) |
| `split_multiline_messages` | `false` | When `true`, split multi-line replies into multiple messages (legacy); when `false`, keep multi-line replies as one message unless they exceed the length limit |
| `text_batch_delay_seconds` | `3.0` | Quiet period before a buffered burst of rapid text messages is flushed as one combined request (iLink delivers individually); `0` dispatches each immediately |
| `text_batch_split_delay_seconds` | `5.0` | Extended flush delay when the latest fragment is near the split threshold |

## Access Policies

### DM Policy

`WEIXIN_DM_POLICY` controls who can DM the bot: `open` (anyone, default), `allowlist` (only IDs in `allow_from`), `disabled` (all DMs ignored), `pairing` (initial-setup pairing mode).

```bash
WEIXIN_DM_POLICY=allowlist
WEIXIN_ALLOWED_USERS=user_id_1,user_id_2
```

`WEIXIN_ALLOWED_USERS` is an **inbound filter**, not an invitation system. QR login connects one iLink bot identity to Hermes; other people do not scan the Hermes QR code with their own accounts — they message the connected iLink bot/contact through WeChat, and Hermes processes the DM only if the sender's Weixin user ID is present in `WEIXIN_ALLOWED_USERS`. A practical flow: pair once with `hermes gateway setup`, have each allowed user DM that bot, read the sender/user ID from the gateway logs or inbound event payload, add those IDs to `WEIXIN_ALLOWED_USERS`, then restart. If only the QR-scanning account can talk to Hermes, verify others are messaging the iLink bot identity itself (a separate identity), not the personal account that performed the login.

### Group Policy

`WEIXIN_GROUP_POLICY` controls which groups the bot responds in **when iLink delivers group events for the connected identity**: `open`, `allowlist` (limited to `group_allow_from`), `disabled` (default). For QR-login iLink bot identities (`...@im.bot`), group events are typically not delivered at all, so this policy may have no effect.

```bash
WEIXIN_GROUP_POLICY=allowlist
# NOTE: this is a comma-separated list of group chat IDs, NOT member user IDs,
# despite the variable name containing "USERS". Keep this in mind when configuring.
WEIXIN_GROUP_ALLOWED_USERS=group_id_1,group_id_2
```

The default group policy is `disabled` for Weixin (unlike WeCom, which defaults to `open`) — intentional, since personal accounts may be in many groups and iLink bot identities typically cannot receive ordinary group messages. The gateway logs a `WARNING` at startup whenever `WEIXIN_GROUP_POLICY` is set to anything other than `disabled`.

## Media Support

**Inbound:** the adapter receives attachments, downloads them from the WeChat CDN, AES-decrypts them, and caches locally — images as JPEG, video as MP4, files (original filename preserved), and voice (text transcription extracted if available, otherwise the SILK-format audio is cached). Media from quoted (replied-to) messages is also extracted for context.

**AES-128-ECB Encrypted CDN:** WeChat media transfers through an encrypted CDN, handled transparently. Inbound encrypted media is downloaded via `encrypted_query_param` URLs and decrypted with AES-128-ECB using the per-file 16-byte (128-bit) key in the message payload (keys arrive as raw base64 or hex — both handled). Outbound files are encrypted locally with a random AES-128-ECB key, uploaded to the CDN, and the encrypted reference is included in the message. This requires the `cryptography` package; no configuration is needed.

**Outbound:** methods are `send` (text with Markdown), `send_image` / `send_image_file`, `send_document`, and `send_video`. All outbound media follows the encrypted CDN upload flow: generate a random AES-128 key, encrypt the file with AES-128-ECB + PKCS#7 padding, request an upload URL from the iLink API (`getuploadurl`), upload the ciphertext to the CDN, and send the message with the encrypted media reference.

## Context Token Persistence

The iLink Bot API requires a `context_token` echoed back with each outbound message for a given peer. The adapter maintains a disk-backed store: tokens are saved per account+peer to `~/.hermes/weixin/accounts/<account_id>.context-tokens.json`, restored on startup, updated by every inbound message, and automatically included on outbound messages — ensuring reply continuity even after gateway restarts.

## Markdown and Message Chunking

WeChat clients connected through iLink can render Markdown directly, so the adapter preserves it: headers stay as Markdown headings, tables stay as Markdown tables, code fences stay fenced, and excessive blank lines are collapsed to double newlines outside fenced code blocks. Messages are delivered as a single chat bubble whenever they fit within the platform limit (maximum **4000 characters**). Only oversized payloads split — at logical boundaries (paragraphs, blank lines, code fences), keeping code fences intact whenever possible (never splitting mid-block unless the fence itself exceeds the limit), falling back to the base adapter's truncation for oversized individual blocks, with a 0.3 s inter-chunk delay to prevent WeChat rate-limit drops.

## Typing Indicators

The adapter shows typing status in the WeChat client. When a message arrives it fetches a `typing_ticket` via the `getconfig` API; typing tickets are cached for 10 minutes per user; `send_typing` sends a typing-start signal and `stop_typing` sends a typing-stop signal; and the gateway automatically triggers typing indicators while the agent processes a message.

## Long-Poll Connection

The adapter uses HTTP long-polling (not WebSocket) to receive messages. **How it works:** connect validates credentials and starts the poll loop; poll calls `getupdates` with a 35-second timeout (the server holds the request until messages arrive or the timeout expires); inbound messages are dispatched concurrently via `asyncio.create_task`; and a persistent sync cursor (`get_updates_buf`) is saved to disk so the adapter resumes from the correct position after restarts.

**Retry behavior:** transient errors (1st–2nd) retry after 2 seconds; repeated errors (3+) back off for 30 seconds then reset the counter; session-expired (`errcode=-14`) pauses for 10 minutes (re-login may be needed); a timeout immediately re-polls (normal long-poll behavior).

**Deduplication** uses message IDs with a 5-minute window to prevent double-processing during network hiccups or overlapping poll responses. **Token lock:** only one Weixin gateway instance can use a given token at a time — the adapter acquires a scoped lock on startup and releases it on shutdown; if another gateway already uses the same token, startup fails with an informative error.

## All Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WEIXIN_ACCOUNT_ID` | ✅ | — | iLink Bot account ID (from QR login) |
| `WEIXIN_TOKEN` | ✅ | — | iLink Bot token (auto-saved from QR login) |
| `WEIXIN_BASE_URL` | — | `https://ilinkai.weixin.qq.com` | iLink API base URL |
| `WEIXIN_CDN_BASE_URL` | — | `https://novac2c.cdn.weixin.qq.com/c2c` | CDN base URL for media transfer |
| `WEIXIN_DM_POLICY` | — | `open` | DM access policy: `open`, `allowlist`, `disabled`, `pairing` |
| `WEIXIN_GROUP_POLICY` | — | `disabled` | Group access policy: `open`, `allowlist`, `disabled` |
| `WEIXIN_ALLOWED_USERS` | — | _(empty)_ | Comma-separated user IDs for DM allowlist |
| `WEIXIN_GROUP_ALLOWED_USERS` | — | _(empty)_ | Comma-separated **group chat IDs** (not member user IDs); the name is legacy |
| `WEIXIN_HOME_CHANNEL` | — | — | Chat ID for cron/notification output |
| `WEIXIN_HOME_CHANNEL_NAME` | — | `Home` | Display name for the home channel |
| `WEIXIN_ALLOW_ALL_USERS` | — | — | Gateway-level flag to allow all users (used by setup wizard) |

## Troubleshooting

Common failures and fixes (from the source troubleshooting table): missing-deps startup failure → `pip install aiohttp cryptography`; `WEIXIN_TOKEN`/`WEIXIN_ACCOUNT_ID is required` → run `hermes gateway setup` or set manually; "another local gateway already using this token" → stop the other instance (one poller per token); session expired (`errcode=-14`) → re-run `hermes gateway setup` for a fresh QR; QR expired during setup → it auto-refreshes up to 3 times, otherwise check network; bot ignores DMs → check `WEIXIN_DM_POLICY` (allowlist requires the sender in `WEIXIN_ALLOWED_USERS`); bot ignores group messages → group policy defaults to `disabled`, and QR-login iLink bot identities typically cannot receive ordinary group messages at all (limitation is on the iLink side); media download/upload fails → ensure `cryptography` is installed and check CDN network access; `Blocked unsafe URL (SSRF protection)` → outbound URL points to a private address (only public URLs allowed); duplicated messages → check for multiple gateway instances; terminal QR doesn't render → reinstall with the `messaging` extra or open the printed URL.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/weixin.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/weixin
**Last Updated**: 2026-06-19
**Status**: Active
