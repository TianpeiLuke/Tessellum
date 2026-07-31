---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - feishu
keywords:
  - feishu lark setup
  - hermes gateway bot
  - websocket webhook connection mode
  - feishu app credentials scopes
  - feishu group policy allowlist
  - webhook encrypt key verification token
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/feishu
access_control_group: ["general"]
---

# Hermes Gateway — Feishu / Lark Setup

## Overview

This note is the **base setup procedure** for running Hermes Agent as a Feishu / Lark bot through the messaging gateway. It covers the get-the-bot-running arc: create the Feishu/Lark app and grant scopes, choose a connection transport, configure credentials, start the gateway, and secure it with an allowlist and group policy. Once connected, the bot answers direct messages and @-mentions in group chats, can deliver cron results to a home chat, and exchanges text/images/audio/files through the normal gateway flow. The Feishu adapter supports two connection modes: `websocket` (recommended — Hermes opens an outbound connection via the official Lark SDK, no public endpoint needed) and `webhook` (Feishu/Lark pushes events to your gateway over HTTP). The advanced feature surface (interactive cards, document-comment reply, meeting auto-join, media, batching, rate limiting, the full env-var table, and the toolset preset) is documented separately in [hermes_gateway_feishu_features](hermes_gateway_feishu_features.md); this note documents only the platform-setup base.

## How Hermes Behaves

| Context | Behavior |
|---------|----------|
| Direct messages | Hermes responds to every message. |
| Group chats | Hermes responds only when the bot is @mentioned in the chat. |
| Shared group chats | By default, session history is isolated per user inside a shared chat. |

Shared-chat session isolation is controlled in `config.yaml`:

```yaml
group_sessions_per_user: true
```

Set it to `false` only to use one shared conversation per chat. The per-user session-isolation model is the gateway's, not Feishu-specific — see [hermes_messaging_gateway_architecture](hermes_messaging_gateway_architecture.md) and [hermes_session_search_storage](hermes_session_search_storage.md) for the cross-platform session model.

## Step 1: Create a Feishu / Lark App

**Recommended — scan-to-create (one command):** run `hermes gateway setup`, select **Feishu / Lark**, and scan the QR code with your Feishu/Lark mobile app. Hermes creates the bot application with the correct permissions and saves the credentials automatically.

**Alternative — manual setup:** if scan-to-create is unavailable, the wizard falls back to manual input. Open the developer console (Feishu: `https://open.feishu.cn/`, Lark: `https://open.larksuite.com/`), create a new app, copy the **App ID** and **App Secret** from **Credentials & Basic Info**, enable the **Bot** capability, then run `hermes gateway setup` and enter the credentials when prompted. Keep the App Secret private — anyone with it can impersonate your app.

**Configure Permissions** — in **Permission Management**, add (bulk-import supported):

- Required: `im:message` (receive/read messages), `im:message:send_as_bot` (send as bot), `im:resource` (images/files/audio), `im:chat` (chat/group metadata), `im:chat:readonly` (chat list/membership).
- Recommended: `im:message.reactions:readonly` (reaction events), `admin:app.info:readonly` (auto-detect bot identity for @mention gating), `contact:user.id:readonly` (resolve user IDs for allowlist matching).

**Configure Events** — in **Events and Callbacks**, set the connection mode to **Long Connection (WebSocket)** (recommended) or configure a webhook URL, then subscribe to `im.message.receive_v1` (required for receiving messages).

**Publish the App** — in **Version Management**, publish a new version. Permissions do not take effect until a version is published and approved (enterprise apps may require admin approval).

## Step 2: Choose a Connection Mode

**WebSocket mode (recommended)** — set `FEISHU_CONNECTION_MODE=websocket`. Use when Hermes runs on a laptop, workstation, or private server; no public URL is required. The official Lark SDK opens and maintains a persistent outbound WebSocket connection with automatic reconnection (handling lifecycle, heartbeats, and reconnect internally). The adapter runs the SDK's WebSocket client in a background executor thread and dispatches inbound events to the main asyncio loop. The `websockets` Python package must be installed.

**Webhook mode (optional)** — use only when Hermes already runs behind a reachable HTTP endpoint. Hermes starts an `aiohttp` HTTP server serving the endpoint `/feishu/webhook`. The `aiohttp` package must be installed. You can customize the bind address and path:

```bash
FEISHU_CONNECTION_MODE=webhook
FEISHU_WEBHOOK_HOST=127.0.0.1        # default: 127.0.0.1
FEISHU_WEBHOOK_PORT=8765             # default: 8765
FEISHU_WEBHOOK_PATH=/feishu/webhook  # default: /feishu/webhook
```

When Feishu sends a URL verification challenge (`type: url_verification`), the webhook responds automatically so you can complete the subscription in the developer console. The challenge response is gated on `FEISHU_VERIFICATION_TOKEN` when set — challenge requests with a missing or mismatched token are rejected so an unauthenticated remote cannot prove endpoint control by echoing attacker-controlled challenge data.

## Step 3: Configure Hermes

**Interactive:** run `hermes gateway setup`, select **Feishu / Lark**, and fill in the prompts.

**Manual:** add the following to `~/.hermes/.env`:

```bash
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=secret_xxx
FEISHU_DOMAIN=feishu
FEISHU_CONNECTION_MODE=websocket

# Optional but strongly recommended
FEISHU_ALLOWED_USERS=ou_xxx,ou_yyy
FEISHU_HOME_CHANNEL=oc_xxx
```

`FEISHU_DOMAIN` accepts `feishu` (Feishu China) or `lark` (Lark international).

## Step 4: Start the Gateway

```bash
hermes gateway
```

Then message the bot from Feishu/Lark to confirm the connection is live. The `hermes gateway setup` and `hermes gateway` commands are documented in [hermes_cli_interface](hermes_cli_interface.md).

## Home Chat

Use `/set-home` in a Feishu/Lark chat to mark it as the home channel for cron job results and cross-platform notifications. You can also preconfigure `FEISHU_HOME_CHANNEL=oc_xxx`. Cron delivery into the home channel is the cron subsystem's concern — see hermes_messaging_overview for the gateway-level home-channel model.

## Security

**User Allowlist** — for production, set an allowlist of Feishu Open IDs with `FEISHU_ALLOWED_USERS=ou_xxx,ou_yyy`. If the allowlist is empty, anyone who can reach the bot may use it. In group chats, the allowlist is checked against the sender's `open_id` before the message is processed.

**Webhook Encryption Key** — in webhook mode, set `FEISHU_ENCRYPT_KEY=your-encrypt-key` (found in the app's **Event Subscriptions** section) to enable signature verification of inbound payloads. The adapter verifies every webhook request using:

```text
SHA256(timestamp + nonce + encrypt_key + body)
```

The computed hash is compared against the `x-lark-signature` header using timing-safe comparison; requests with invalid or missing signatures are rejected with HTTP 401. In WebSocket mode, signature verification is handled by the SDK itself, so `FEISHU_ENCRYPT_KEY` is optional; in webhook mode it is strongly recommended for production.

**Verification Token** — set `FEISHU_VERIFICATION_TOKEN=your-verification-token` (also in **Event Subscriptions**) as an additional auth layer that checks the `token` field inside webhook payloads. Every inbound payload must contain a matching `token` in its `header` object; mismatched tokens are rejected with HTTP 401. Both keys can be used together for defense in depth.

## Group Message Policy

`FEISHU_GROUP_POLICY` controls whether and how Hermes responds in group chats (default `allowlist`):

| Value | Behavior |
|-------|----------|
| `open` | Hermes responds to @mentions from any user in any group. |
| `allowlist` | Hermes only responds to @mentions from users in `FEISHU_ALLOWED_USERS`. |
| `disabled` | Hermes ignores all group messages entirely. |

In all modes the bot must be explicitly @mentioned (or @all) before processing; direct messages always bypass this gate. Set `FEISHU_REQUIRE_MENTION=false` to let Hermes read all group traffic without requiring an @mention. For per-chat control, set `require_mention` on a `group_rules` entry (below).

## Per-Group Access Control

Beyond the global policy, set fine-grained per-group rules via `group_rules` in `config.yaml`:

```yaml
platforms:
  feishu:
    extra:
      default_group_policy: "open"     # Default for groups not in group_rules
      admins:                          # Users who can manage bot settings
        - "ou_admin_open_id"
      group_rules:
        "oc_group_chat_id_1":
          policy: "allowlist"          # open | allowlist | blacklist | admin_only | disabled
          allowlist:
            - "ou_user_open_id_1"
            - "ou_user_open_id_2"
        "oc_group_chat_id_2":
          policy: "admin_only"
        "oc_free_chat":
          policy: "open"
          require_mention: false       # overrides FEISHU_REQUIRE_MENTION for this chat
```

Per-group policy values: `open` (anyone in the group), `allowlist` (only users in the group's `allowlist`), `blacklist` (everyone except the group's `blacklist`), `admin_only` (only global `admins`), `disabled` (ignore all messages). Set `require_mention: false` on an entry to skip the @-mention requirement for that chat. Groups not listed fall back to `default_group_policy` (which defaults to `FEISHU_GROUP_POLICY`). The full `platforms.feishu.extra` config block (WebSocket tuning, batching) is covered in [hermes_messaging_media_settings](hermes_messaging_media_settings.md) and [hermes_gateway_feishu_features](hermes_gateway_feishu_features.md).

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `lark-oapi not installed` | `pip install lark-oapi` |
| `websockets not installed; websocket mode unavailable` | `pip install websockets` |
| `aiohttp not installed; webhook mode unavailable` | `pip install aiohttp` |
| `FEISHU_APP_ID or FEISHU_APP_SECRET not set` | Set both env vars or configure via `hermes gateway setup` |
| `Another local Hermes gateway is already using this Feishu app_id` | Only one Hermes instance can use the same app_id at a time. Stop the other gateway first. |
| Bot doesn't respond in groups | Ensure the bot is @mentioned, check `FEISHU_GROUP_POLICY`, and verify the sender is in `FEISHU_ALLOWED_USERS` if policy is `allowlist`. |
| `Webhook rejected: invalid verification token` | Ensure `FEISHU_VERIFICATION_TOKEN` matches the token in your app's Event Subscriptions config. |
| `Webhook rejected: invalid signature` | Ensure `FEISHU_ENCRYPT_KEY` matches the encrypt key in your app config. |
| Images/files not received by bot | Grant `im:message` and `im:resource` permission scopes to your app. |

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/feishu.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/feishu
**Last Updated**: 2026-06-19
**Status**: Active
