---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - imessage
keywords:
  - bluebubbles imessage
  - hermes messaging gateway
  - webhook push inbound
  - bluebubbles rest api
  - dm pairing authorization
  - require_mention group gating
  - private api helper
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/bluebubbles
access_control_group: ["general"]
---

# BlueBubbles (iMessage)

## Overview

This page is the setup procedure for connecting Hermes to **Apple iMessage** via [BlueBubbles](https://bluebubbles.app/) — a free, open-source macOS server that bridges iMessage to any device. Because Apple has no official iMessage API, the integration relies on an always-on Mac running BlueBubbles Server (signed into Messages.app) that Hermes talks to over the network: **inbound** messages arrive as webhook pushes (no polling), and **outbound** messages are sent through the BlueBubbles REST API. Authorization is by DM pairing or an allowlist, group chats can be made opt-in via mention gating, and rich features (tapbacks, typing indicators, read receipts, create-chat-by-address) require the BlueBubbles Private API helper. It is one of several consumer/private-messenger platforms wired into the shared messaging gateway — the iMessage-via-Mac-relay counterpart to the managed-line-pool [Photon path](hermes_photon_imessage.md).

## Prerequisites

- A **Mac** (always on) running [BlueBubbles Server](https://bluebubbles.app/)
- Apple ID signed into Messages.app on that Mac
- BlueBubbles Server v1.0.0+ (webhooks require this version)
- Network connectivity between Hermes and the BlueBubbles server

## Setup

The source walks through five steps:

1. **Install BlueBubbles Server** — download and install from [bluebubbles.app](https://bluebubbles.app/), complete the wizard (sign in with the Apple ID, pick a connection method: local network, Ngrok, Cloudflare, or Dynamic DNS).
2. **Get the Server URL and Password** — in BlueBubbles Server → **Settings → API**, note the Server URL (e.g., `http://192.168.1.10:1234`) and the Server Password.
3. **Configure Hermes** — run `hermes gateway setup`, select **BlueBubbles (iMessage)**, and enter the URL and password (or set the env vars directly).
4. **Authorize Users** — DM pairing (recommended), a pre-authorized allowlist, or open access.
5. **Start the Gateway** — `hermes gateway run`; Hermes connects, registers a webhook, and listens for messages.

The setup wizard and direct env-var configuration are equivalent:

```bash
hermes gateway setup
# Or set environment variables directly in ~/.hermes/.env:
BLUEBUBBLES_SERVER_URL=http://192.168.1.10:1234
BLUEBUBBLES_PASSWORD=your-server-password
```

### Optional: Require mentions in group chats

By default Hermes responds to every authorized DM or group message. To make group chats opt-in, enable mention gating. With `require_mention: true`, DMs still work normally but group-chat messages are ignored unless they match a mention pattern; without custom patterns Hermes uses conservative defaults for `Hermes`/`@Hermes agent` variants. For a custom agent name, set regex `mention_patterns`:

```yaml
platforms:
  bluebubbles:
    enabled: true
    extra:
      require_mention: true
      mention_patterns:
        - '(?<![\w@])@?amos\b[,:\-]?'
```

### Authorize Users

Three approaches. DM pairing auto-sends a code to anyone who messages the iMessage; approve it (or list pending/approved users) via the CLI:

```bash
hermes pairing approve bluebubbles <CODE>
hermes pairing list
```

Alternatively pre-authorize or open access via `~/.hermes/.env`:

```bash
BLUEBUBBLES_ALLOWED_USERS=user@icloud.com,+15551234567
BLUEBUBBLES_ALLOW_ALL_USERS=true
```

## How It Works

```
iMessage → Messages.app → BlueBubbles Server → Webhook → Hermes
Hermes → BlueBubbles REST API → Messages.app → iMessage
```

- **Inbound:** BlueBubbles sends webhook events to a local listener when new messages arrive — no polling, instant delivery.
- **Outbound:** Hermes sends messages via the BlueBubbles REST API.
- **Media:** Images, voice messages, videos, and documents are supported both directions. Inbound attachments are downloaded and cached locally for the agent to process.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BLUEBUBBLES_SERVER_URL` | Yes | — | BlueBubbles server URL |
| `BLUEBUBBLES_PASSWORD` | Yes | — | Server password |
| `BLUEBUBBLES_WEBHOOK_HOST` | No | `127.0.0.1` | Webhook listener bind address |
| `BLUEBUBBLES_WEBHOOK_PORT` | No | `8645` | Webhook listener port |
| `BLUEBUBBLES_WEBHOOK_PATH` | No | `/bluebubbles-webhook` | Webhook URL path |
| `BLUEBUBBLES_HOME_CHANNEL` | No | — | Phone/email for cron delivery |
| `BLUEBUBBLES_ALLOWED_USERS` | No | — | Comma-separated authorized users |
| `BLUEBUBBLES_ALLOW_ALL_USERS` | No | `false` | Allow all users |
| `BLUEBUBBLES_REQUIRE_MENTION` | No | `false` | Require a mention pattern before responding in group chats |
| `BLUEBUBBLES_MENTION_PATTERNS` | No | Hermes wake words | JSON array, newline-separated, or comma-separated regex patterns for group mention matching |

Auto-marking messages as read is controlled by the `send_read_receipts` key under `platforms.bluebubbles.extra` in `~/.hermes/config.yaml` (default: `true`). There is no corresponding environment variable.

## Features

- **Text Messaging** — send and receive iMessages; markdown is automatically stripped for clean plain-text delivery.
- **Rich Media** — images appear natively in the conversation; voice messages sent as iMessage voice messages; videos and documents sent as attachments.
- **Tapback Reactions** — love, like, dislike, laugh, emphasize, and question reactions (requires Private API helper).
- **Typing Indicators** — shows "typing..." while the agent is processing (requires Private API).
- **Read Receipts** — automatically marks messages as read after processing (requires Private API).
- **Chat Addressing** — address chats by email or phone number; Hermes resolves them to BlueBubbles chat GUIDs automatically (no raw GUID needed).

## Private API

Some features require the BlueBubbles [Private API helper](https://docs.bluebubbles.app/helper-bundle/installation): tapback reactions, typing indicators, read receipts, and creating new chats by address. Without the Private API, basic text messaging and media still work.

## Troubleshooting

- **"Cannot reach server"** — verify the server URL is correct and the Mac is on; check that BlueBubbles Server is running; ensure network connectivity (firewall, port forwarding).
- **Messages not arriving** — check that the webhook is registered in BlueBubbles Server → Settings → API → Webhooks; verify the webhook URL is reachable from the Mac; check `hermes logs gateway` for webhook errors (or `hermes logs -f` to follow in real time).
- **"Private API helper not connected"** — install the Private API helper; basic messaging works without it — only reactions, typing, and read receipts require it.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/bluebubbles.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/bluebubbles
**Last Updated**: 2026-06-19
**Status**: Active
