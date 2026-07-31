---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - dingtalk
keywords:
  - dingtalk stream mode setup
  - hermes gateway dingtalk
  - DINGTALK_ALLOWED_USERS allowlist
  - QR device flow credentials
  - AI Cards streaming reply
  - session webhook reply model
topics:
  - Hermes Agent
  - Messaging Gateway
  - DingTalk
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/dingtalk
access_control_group: ["general"]
---

# DingTalk Setup

## Overview

This is the platform-setup procedure for running Hermes Agent as a **DingTalk (钉钉) chatbot** — letting you chat with the agent through DingTalk direct messages or group chats. The adapter connects through DingTalk's **Stream Mode**, a long-lived WebSocket connection initiated from your machine that needs no public URL, domain, or webhook server, so it works behind NAT and firewalls. The bot replies with markdown-formatted messages through DingTalk's **session webhook API** — a reply URL that arrives with each inbound message. End-to-end the procedure is: create a DingTalk app, enable the Robot capability in Stream Mode, find your DingTalk User ID, configure credentials and the deny-by-default allowlist (interactively via `hermes gateway setup` or manually in `~/.hermes/.env`), then start the gateway with `hermes gateway`. Optional features layer on top: AI Cards with streaming, 🤔/🥳 emoji status reactions, and per-platform display settings.

The broader gateway concept (the platform↔agent bridge, DM pairing, silence token, group-session isolation) and the `hermes gateway` CLI itself are documented by their owning notes — this note links out to them rather than re-explaining them.

## How Hermes Behaves

| Context | Behavior |
|---------|----------|
| **DMs (1:1 chat)** | Hermes responds to every message. No `@mention` needed. Each DM has its own session. |
| **Group chats** | Hermes responds when you `@mention` it. Without a mention, Hermes ignores the message. |
| **Shared groups with multiple users** | By default, Hermes isolates session history per user inside the group. Two people talking in the same group do not share one transcript unless you explicitly disable that. |

### Session Model in DingTalk

By default each DM gets its own session, and each user in a shared group chat gets their own session inside that group. This is controlled by `config.yaml`:

```yaml
group_sessions_per_user: true
```

Set it to `false` only if you explicitly want one shared conversation for the entire group.

## Prerequisites

Install the required Python packages:

```bash
pip install "hermes-agent[dingtalk]"
```

The `hermes-agent[dingtalk]` extra pulls in the SDK trio: `dingtalk-stream` (DingTalk's official SDK for Stream Mode / WebSocket-based real-time messaging), `httpx` (async HTTP client used for sending replies via session webhooks), and `alibabacloud-dingtalk` (DingTalk OpenAPI SDK for AI Cards, emoji reactions, and media downloads). They can also be installed individually with `pip install dingtalk-stream httpx alibabacloud-dingtalk`.

## Step 1: Create a DingTalk App

In the [DingTalk Developer Console](https://open-dev.dingtalk.com/), log in with your DingTalk admin account, then go to **Application Development → Custom Apps → Create App via H5 Micro-App** (or **Robot**, depending on console version). Fill in an **App Name** (e.g., `Hermes Agent`) and optional description. After creating, navigate to **Credentials & Basic Info** to find your **Client ID** (AppKey) and **Client Secret** (AppSecret) — copy both.

> **Credentials shown only once:** The Client Secret is only displayed once when you create the app. If you lose it, you'll need to regenerate it. Never share these credentials publicly or commit them to Git.

## Step 2: Enable the Robot Capability

In your app's settings page, go to **Add Capability → Robot** and enable the robot capability. Under **Message Reception Mode**, select **Stream Mode** (recommended — no public URL needed). Stream Mode uses a long-lived WebSocket connection initiated from your machine, so you don't need a public IP, domain name, or webhook endpoint; it works behind NAT, firewalls, and on local machines.

## Step 3: Find Your DingTalk User ID

Hermes uses your DingTalk **User ID** to control who can interact with the bot. DingTalk User IDs are alphanumeric strings set by your organization's admin. To find yours, either ask your DingTalk organization admin (User IDs are configured in the admin console under **Contacts → Members**), or start the gateway, send the bot a message, and read the `sender_id` the bot logs for each incoming message.

## Step 4: Configure Hermes Agent

### Option A: Interactive Setup (Recommended)

Run the guided setup command and select **DingTalk** when prompted:

```bash
hermes gateway setup
```

The wizard authorizes via one of two paths:

- **QR-code device flow (recommended).** Scan the QR that prints in your terminal with the DingTalk mobile app — your Client ID and Client Secret are returned automatically and written to `~/.hermes/.env`. No developer-console trip needed.
- **Manual paste.** If you already have credentials (or QR scanning isn't convenient), paste your Client ID, Client Secret, and allowed user IDs when prompted.

> **openClaw branding disclosure:** Because DingTalk's `verification_uri_complete` is hardcoded to the openClaw identity at the API layer, the QR currently authorizes under an `openClaw` source string until Alibaba / DingTalk-Real-AI registers a Hermes-specific template server-side. This is purely how DingTalk presents the consent screen — the bot you create is fully yours and private to your tenant.

### Option B: Manual Configuration

Add the credentials and security settings to `~/.hermes/.env`:

```bash
# Required
DINGTALK_CLIENT_ID=your-app-key
DINGTALK_CLIENT_SECRET=your-app-secret

# Security: restrict who can interact with the bot
DINGTALK_ALLOWED_USERS=user-id-1
# Multiple allowed users (comma-separated)
# DINGTALK_ALLOWED_USERS=user-id-1,user-id-2

# Optional: group-chat gating (mirrors Slack/Telegram/Discord/WhatsApp)
# DINGTALK_REQUIRE_MENTION=true
# DINGTALK_FREE_RESPONSE_CHATS=cidABC==,cidDEF==
# DINGTALK_MENTION_PATTERNS=^小马
# DINGTALK_HOME_CHANNEL=cidXXXX==
# DINGTALK_ALLOW_ALL_USERS=true
```

Optional behavior settings live in `~/.hermes/config.yaml` under `gateway.platforms.dingtalk.extra`: `require_mention: true` makes the bot answer in groups only when @-mentioned (DMs ignore this and always reply), and an `allowed_users` list is an alternative to `DINGTALK_ALLOWED_USERS` (if both are set, they're merged). `group_sessions_per_user: true` keeps each participant's context isolated inside shared group chats.

### Start the Gateway

Once configured, start the DingTalk gateway:

```bash
hermes gateway
```

The bot should connect to DingTalk's Stream Mode within a few seconds. Send it a DM or a message in a group where it's been added to test. You can run `hermes gateway` in the background or as a systemd service for persistent operation (see the deployment docs).

## Features

### AI Cards

Hermes can reply using DingTalk **AI Cards** instead of plain markdown messages. Cards provide a richer, more structured display and support **streaming updates** as the agent generates its response. To enable, configure a card template ID in `config.yaml` under `platforms.dingtalk.extra.card_template_id` (find the ID in the DingTalk Developer Console under your app's AI Card settings). When AI Cards are enabled, all replies are sent as cards with streaming text updates.

### Emoji Reactions

Hermes automatically adds emoji reactions to show processing status — 🤔 **Thinking** when the bot starts processing your message, and 🥳 **Done** when the response is complete (replacing the Thinking reaction). These reactions work in both DMs and group chats.

### Display Settings

You can customize DingTalk's display behavior independently from other platforms:

```yaml
display:
  platforms:
    dingtalk:
      show_reasoning: false   # Show model reasoning/thinking in replies
      streaming: true         # Enable streaming responses (works with AI Cards)
      tool_progress: all      # Show tool execution progress (all/new/off)
      interim_assistant_messages: true  # Show intermediate commentary messages
```

For a cleaner experience, set `tool_progress: off` and `interim_assistant_messages: false`.

## Troubleshooting

- **Bot is not responding to messages** — The robot capability isn't enabled, or `DINGTALK_ALLOWED_USERS` doesn't include your User ID. Verify the robot capability is enabled and Stream Mode is selected, confirm your User ID is in `DINGTALK_ALLOWED_USERS`, and restart the gateway.
- **"dingtalk-stream not installed" error** — The `dingtalk-stream` package is missing; install it with `pip install dingtalk-stream httpx`.
- **"DINGTALK_CLIENT_ID and DINGTALK_CLIENT_SECRET required"** — The credentials aren't set; verify both are correct in `~/.hermes/.env` (Client ID = AppKey, Client Secret = AppSecret).
- **Stream disconnects / reconnection loops** — Network instability, DingTalk maintenance, or credential issues. The adapter automatically reconnects with exponential backoff (2s → 5s → 10s → 30s → 60s); check that credentials are valid, the app isn't deactivated, and your network allows outbound WebSocket connections.
- **Bot is offline** — The gateway isn't running or failed to connect. Check that `hermes gateway` is running and inspect the terminal output (common causes: wrong credentials, app deactivated, `dingtalk-stream`/`httpx` not installed).
- **"No session_webhook available"** — The bot tried to reply but has no session webhook URL, typically because it expired or the bot restarted between receiving and replying. Send a new message — each incoming message provides a fresh session webhook for replies. This is a normal DingTalk limitation: the bot can only reply to messages it has received recently.

## Security

Always set `DINGTALK_ALLOWED_USERS` to restrict who can interact with the bot. Without it, the gateway **denies all users by default** as a safety measure. Only add User IDs of people you trust — authorized users have full access to the agent's capabilities, including tool use and system access.

## Notes

- **Stream Mode**: No public URL, domain name, or webhook server needed; the WebSocket connection is initiated from your machine, so it works behind NAT and firewalls.
- **AI Cards**: Optionally reply with rich AI Cards instead of plain markdown, configured via `card_template_id`.
- **Emoji Reactions**: Automatic 🤔Thinking/🥳Done reactions for processing status.
- **Markdown responses**: Replies are formatted in DingTalk's markdown format for rich text display.
- **Media support**: Images and files in incoming messages are automatically resolved and can be processed by vision tools.
- **Message deduplication**: The adapter deduplicates messages with a 5-minute window to prevent processing the same message twice.
- **Auto-reconnection**: If the stream connection drops, the adapter automatically reconnects with exponential backoff.
- **Message length limit**: Responses are capped at 20,000 characters per message; longer responses are truncated.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/dingtalk.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/dingtalk
**Last Updated**: 2026-06-19
**Status**: Active
