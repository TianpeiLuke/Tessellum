---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - signal
keywords:
  - signal-cli daemon
  - linked device
  - SSE streaming
  - JSON-RPC
  - allowlist access control
  - phone number redaction
  - Note to Self
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/signal
access_control_group: ["general"]
---

# Hermes Messaging — Signal Setup

## Overview

This is the runbook for connecting Hermes Agent to **Signal** as a messenger bot. Hermes does not speak the Signal protocol directly — it drives the external [signal-cli](https://github.com/AsamK/signal-cli) daemon running in HTTP mode, streaming inbound messages in real time over **SSE (Server-Sent Events)** and sending replies via **JSON-RPC**. The adapter uses `httpx` (already a core Hermes dependency), so the Signal platform adds **no new Python packages** — you only need signal-cli installed externally. Signal is the most privacy-focused mainstream messenger (end-to-end encrypted by default, open-source protocol, minimal metadata), which the source positions as ideal for security-sensitive agent workflows.

The setup arc is: install signal-cli (Java 17+) → link Hermes as a **secondary device** of your phone → run the `--http` daemon → point Hermes at it via `~/.hermes/.env` → configure DM/group access control → start the gateway. The gateway concept, DM-pairing handshake, and the silence-token convention are shared messaging-gateway concepts documented elsewhere; this note covers the Signal-specific procedure and behavior only.

## Prerequisites

- **signal-cli** — Java-based Signal client ([GitHub](https://github.com/AsamK/signal-cli)).
- **Java 17+** runtime — required by signal-cli.
- **A phone number** with Signal installed (for linking as a secondary device).

### Installing signal-cli

signal-cli is **not** in apt or snap repositories — the Linux install downloads directly from [GitHub releases](https://github.com/AsamK/signal-cli/releases).

```bash
# macOS
brew install signal-cli

# Linux (download latest release)
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} \
  https://github.com/AsamK/signal-cli/releases/latest | sed 's/^.*\/v//')
curl -L -O "https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}.tar.gz"
sudo tar xf "signal-cli-${VERSION}.tar.gz" -C /opt
sudo ln -sf "/opt/signal-cli-${VERSION}/bin/signal-cli" /usr/local/bin/
```

## Step 1: Link Your Signal Account

signal-cli works as a **linked device** — like WhatsApp Web, but for Signal. Your phone stays the primary device. Generate a linking URI (it displays a QR code or link):

```bash
# Generate a linking URI (displays a QR code or link)
signal-cli link -n "HermesAgent"
```

Then on your phone: open **Signal** → **Settings → Linked Devices** → tap **Link New Device** → scan the QR code or enter the URI.

## Step 2: Start the signal-cli Daemon

Run the daemon in HTTP mode and keep it running in the background (`systemd`, `tmux`, `screen`, or as a service):

```bash
# Replace +1234567890 with your Signal phone number (E.164 format)
signal-cli --account +1234567890 daemon --http 127.0.0.1:8080
```

Verify it is running:

```bash
curl http://127.0.0.1:8080/api/v1/check
# Should return: {"versions":{"signal-cli":...}}
```

## Step 3: Configure Hermes

The easiest path is `hermes gateway setup` → select **Signal** from the platform menu. The wizard checks whether signal-cli is installed, prompts for the HTTP URL (default `http://127.0.0.1:8080`), tests connectivity to the daemon, asks for your account phone number, and configures allowed users and access policies.

For manual configuration, add the following to `~/.hermes/.env`, then start the gateway (`hermes gateway` for foreground, `hermes gateway install` for a user service, or `sudo hermes gateway install --system` for a Linux boot-time system service):

```bash
# Required
SIGNAL_HTTP_URL=http://127.0.0.1:8080
SIGNAL_ACCOUNT=+1234567890

# Security (recommended)
SIGNAL_ALLOWED_USERS=+1234567890,+0987654321    # Comma-separated E.164 numbers or UUIDs

# Optional
SIGNAL_GROUP_ALLOWED_USERS=groupId1,groupId2     # Enable groups (omit to disable, * for all)
SIGNAL_HOME_CHANNEL=+1234567890                  # Default delivery target for cron jobs
```

## Access Control

**DM access** follows the same pattern as all other Hermes platforms:

1. **`SIGNAL_ALLOWED_USERS` set** → only those users can message.
2. **No allowlist set** → unknown users get a DM pairing code (approve via `hermes pairing approve signal CODE`).
3. **`SIGNAL_ALLOW_ALL_USERS=true`** → anyone can message (use with caution).

**Group access** is controlled by `SIGNAL_GROUP_ALLOWED_USERS`:

| Configuration | Behavior |
|---------------|----------|
| Not set (default) | All group messages are ignored. The bot only responds to DMs. |
| Set with group IDs | Only listed groups are monitored (e.g., `groupId1,groupId2`). |
| Set to `*` | The bot responds in any group it's a member of. |

## Features

### Attachments

The adapter supports sending and receiving media in both directions. **Incoming** (user → agent): images (PNG, JPEG, GIF, WebP, auto-detected via magic bytes), audio (MP3, OGG, WAV, M4A — voice messages transcribed if Whisper is configured; see [hermes_stt_transcription](hermes_stt_transcription.md)), and documents (PDF, ZIP, and others). **Outgoing** (agent → user): the agent sends media via `MEDIA:` tags in responses — `send_multiple_images`/`send_image_file` (images), `send_voice` (audio), `send_video` (MP4), and `send_document` (any file type). All outgoing media goes through Signal's standard attachment API; unlike some platforms, Signal does not distinguish voice messages from file attachments at the protocol level.

Attachment size limit is **100 MB** (both directions). Because Signal servers rate-limit attachment uploads, the adapter uses a scheduler for multiple-image sending that **batches images in groups of 32** and throttles uploads to match the Signal server policy.

### Native Formatting, Reply Quotes, and Reactions

Signal messages render with **native formatting** rather than literal markdown characters. The adapter converts markdown (`**bold**`, `*italic*`, `` `code` ``, `~~strike~~`, `||spoiler||`, headings) into Signal **`bodyRanges`** so text shows real styling on the recipient's client. When Hermes replies to a specific message it posts a **native reply quote** (the same affordance Signal users get from "Reply"), automatic for replies to an inbound message. The agent can also add **reactions** via the standard reaction API, surfacing as emoji reactions rather than extra text. None of this requires extra config — it ships on by default in recent signal-cli builds; if your signal-cli is too old, Hermes falls back to plaintext delivery and logs a one-time warning.

### Typing Indicators and Tool Progress

The bot sends typing indicators while processing, refreshing every 8 seconds. Signal does **not** support editing already-sent messages, so Hermes **suppresses gateway tool-progress bubbles** on Signal even when `/verbose` is enabled (and it saves a non-`off` mode for the platform). Tool activity is still visible in the CLI, and final Signal replies can include normal assistant output; if you need live per-tool progress in chat, use a platform with message editing.

### Phone Number Redaction

All phone numbers are automatically redacted in logs — e.g., `+15551234567` → `+155****4567` — applied to both Hermes gateway logs and the global redaction system.

### Note to Self (Single-Number Setup)

If you run signal-cli as a **linked secondary device on your own phone number** (rather than a separate bot number), you can talk to Hermes through Signal's "Note to Self" feature: just send a message to yourself and signal-cli picks it up, with Hermes responding in the same conversation. Mechanically, "Note to Self" messages arrive as `syncMessage.sentMessage` envelopes; the adapter detects when these are addressed to the bot's own account and processes them as regular inbound messages, while **echo-back protection** (sent-timestamp tracking) prevents infinite loops by filtering out the bot's own replies. No extra configuration is needed as long as `SIGNAL_ACCOUNT` matches your phone number.

### Health Monitoring

The adapter monitors the SSE connection and automatically reconnects if the connection drops (with **exponential backoff: 2s → 60s**) or if no activity is detected for **120 seconds** (it pings signal-cli to verify).

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Cannot reach signal-cli"** during setup | Ensure the signal-cli daemon is running: `signal-cli --account +YOUR_NUMBER daemon --http 127.0.0.1:8080`. |
| **Messages not received** | Check that `SIGNAL_ALLOWED_USERS` includes the sender's number in E.164 format (with `+` prefix). |
| **"signal-cli not found on PATH"** | Install signal-cli and ensure it's in your PATH, or use Docker. |
| **Connection keeps dropping** | Check signal-cli logs for errors. Ensure Java 17+ is installed. |
| **Group messages ignored** | Configure `SIGNAL_GROUP_ALLOWED_USERS` with specific group IDs, or `*` to allow all groups. |
| **Bot responds to no one** | Configure `SIGNAL_ALLOWED_USERS`, use DM pairing, or explicitly allow all users through gateway policy. |
| **Duplicate messages** | Ensure only one signal-cli instance is listening on your phone number. |

## Security

**Always configure access controls.** The bot has terminal access by default; without `SIGNAL_ALLOWED_USERS` or DM pairing, the gateway **denies all incoming messages** as a safety measure. Additional guidance from the source:

- Phone numbers are redacted in all log output.
- Use DM pairing or explicit allowlists for safe onboarding of new users.
- Keep groups disabled unless you specifically need group support, or allowlist only the groups you trust.
- Signal's end-to-end encryption protects message content in transit.
- The signal-cli session data in `~/.local/share/signal-cli/` contains account credentials — protect it like a password.

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SIGNAL_HTTP_URL` | Yes | — | signal-cli HTTP endpoint |
| `SIGNAL_ACCOUNT` | Yes | — | Bot phone number (E.164) |
| `SIGNAL_ALLOWED_USERS` | No | — | Comma-separated phone numbers/UUIDs |
| `SIGNAL_GROUP_ALLOWED_USERS` | No | — | Group IDs to monitor, or `*` for all (omit to disable groups) |
| `SIGNAL_ALLOW_ALL_USERS` | No | `false` | Allow any user to interact (skip allowlist) |
| `SIGNAL_HOME_CHANNEL` | No | — | Default delivery target for cron jobs |

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/signal.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/signal
**Last Updated**: 2026-06-19
**Status**: Active
