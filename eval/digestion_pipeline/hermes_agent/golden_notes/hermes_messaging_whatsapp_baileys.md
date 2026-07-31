---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - whatsapp
keywords:
  - whatsapp baileys bridge
  - whatsapp web session
  - hermes whatsapp qr pairing
  - whatsapp allowed users allowlist
  - whatsapp message chunking debounce
  - whatsapp ban risk
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp
access_control_group: ["general"]
---

# WhatsApp Setup (Baileys Bridge)

## Overview

This is the **runbook for connecting Hermes Agent to WhatsApp through its built-in, unofficial Baileys bridge** — the adapter that emulates a WhatsApp Web session rather than going through Meta's official WhatsApp Business API. Because it rides the Web protocol, **no Meta developer account or Business verification is required**, setup is fast, and no public URL is needed; the trade-off is a small **account-ban risk** and occasional breakage when WhatsApp updates its Web protocol. The arc is the standard Hermes "connect to platform X" procedure: choose a mode (dedicated bot number vs personal self-chat), scan a QR code via `hermes whatsapp`, optionally provision a second phone number, wire `.env` access control plus `config.yaml` behavior, then start the gateway. Delivery behavior (streaming edits, 4,096-char chunking, Markdown→WhatsApp conversion, tool-progress indicators, and a debounce buffer) and security guidance round it out. For the official, stable, business path instead see the **WhatsApp Business Cloud API** sibling notes; the two adapters can run in parallel against different numbers. Voice transcription/TTS and the DM-pairing concept are owned elsewhere (linked below), not redefined here.

## Two Modes

| Mode | How it works | Best for |
|------|-------------|----------|
| **Separate bot number** (recommended) | Dedicate a phone number to the bot. People message that number directly. | Clean UX, multiple users, lower ban risk |
| **Personal self-chat** | Use your own WhatsApp. You message yourself to talk to the agent. | Quick setup, single user, testing |

Run `hermes gateway setup` and pick **WhatsApp** for a guided walk-through.

**Ban-risk caveats (source warnings):** WhatsApp does not officially support third-party bots outside the Business API, so a bridge carries a small risk of account restrictions. To minimize it: use a dedicated phone number (not your personal one), don't send bulk/spam messages (keep usage conversational), and don't automate outbound messaging to people who haven't messaged first. Separately, WhatsApp periodically updates its Web protocol, which can temporarily break third-party bridges — when that happens, pull the latest Hermes version (which updates the bridge dependency) and re-pair.

## Prerequisites

- **Node.js v18+** and **npm** — the WhatsApp bridge runs as a Node.js process.
- **A phone with WhatsApp** installed (for scanning the QR code).

Unlike older browser-driven bridges, the current Baileys-based bridge does **not** require a local Chromium or Puppeteer dependency stack.

## Step 1: Run the Setup Wizard

```bash
hermes whatsapp
```

The wizard asks which mode you want (**bot** or **self-chat**), installs bridge dependencies if needed, displays a **QR code** in your terminal, and waits for you to scan it.

To scan the QR code: open WhatsApp on your phone → **Settings → Linked Devices** → tap **Link a Device** → point your camera at the terminal QR code. Once paired, the wizard confirms the connection and exits; your session is saved automatically. If the QR code looks garbled, make sure your terminal is at least 60 columns wide and supports Unicode, or try a different terminal emulator.

## Step 2: Getting a Second Phone Number (Bot Mode)

For bot mode you need a number not already registered with WhatsApp. Three options: **Google Voice** (free, US only — verify WhatsApp via SMS through the Google Voice app), a **prepaid SIM** ($5–15 one-time, any carrier — the SIM can then sit in a drawer but the number must stay active with a call every 90 days), or **VoIP services** (free–$5/month, e.g. TextNow/TextFree — some VoIP numbers are blocked by WhatsApp, so try a few). After getting the number: install WhatsApp on a phone (or use the WhatsApp Business app with dual-SIM), register the new number, then run `hermes whatsapp` and scan the QR code from that account.

## Step 3: Configure Hermes

Add the following to your `~/.hermes/.env` file:

```bash
# Required
WHATSAPP_ENABLED=true
WHATSAPP_MODE=bot                          # "bot" or "self-chat"

# Access control — pick ONE of these options:
WHATSAPP_ALLOWED_USERS=15551234567         # Comma-separated phone numbers (with country code, no +)
# WHATSAPP_ALLOWED_USERS=*                 # OR use * to allow everyone
# WHATSAPP_ALLOW_ALL_USERS=true            # OR set this flag instead (same effect as *)
```

Setting `WHATSAPP_ALLOWED_USERS=*` allows **all** senders (equivalent to `WHATSAPP_ALLOW_ALL_USERS=true`). To use the pairing flow instead, remove both variables and rely on the DM pairing system (the platform↔agent authorization handshake owned by the gateway docs, linked below).

Optional behavior settings go in `~/.hermes/config.yaml`:

```yaml
unauthorized_dm_behavior: pair

whatsapp:
  unauthorized_dm_behavior: ignore
```

- `unauthorized_dm_behavior: pair` is the global default — unknown DM senders get a pairing code.
- `whatsapp.unauthorized_dm_behavior: ignore` makes WhatsApp stay silent for unauthorized DMs, which is usually the better choice for a private number.

Then start the gateway:

```bash
hermes gateway              # Foreground
hermes gateway install      # Install as a user service
sudo hermes gateway install --system   # Linux only: boot-time system service
```

The gateway starts the WhatsApp bridge automatically using the saved session.

## Session Persistence & Re-pairing

The Baileys bridge saves its session under `~/.hermes/platforms/whatsapp/session`. **Sessions survive restarts** — you don't re-scan the QR code every time. The session data includes encryption keys and device credentials, so **do not share or commit this directory** — it grants full access to the WhatsApp account.

If the session breaks (phone reset, WhatsApp update, manual unlink), connection errors appear in the gateway logs. Re-run `hermes whatsapp` to generate a fresh QR code, scan it, and the session is re-established. The gateway handles **temporary** disconnections (network blips, phone briefly offline) automatically with reconnection logic.

## Voice Messages

Hermes supports voice on WhatsApp. **Incoming** voice messages (`.ogg` opus) are automatically transcribed using the configured STT provider (local `faster-whisper`, Groq Whisper via `GROQ_API_KEY`, or OpenAI Whisper via `VOICE_TOOLS_OPENAI_KEY`). **Outgoing** TTS responses are sent as MP3 audio file attachments. (The voice transcription/TTS subsystem itself is owned by the media notes, linked below.) Agent responses are prefixed with `⚕ **Hermes Agent**` by default; customize or disable it in `config.yaml`:

```yaml
# ~/.hermes/config.yaml
whatsapp:
  reply_prefix: ""                          # Empty string disables the header
  # reply_prefix: "🤖 *My Bot*\n──────\n"  # Custom prefix (supports \n for newlines)
```

## Message Formatting & Delivery

WhatsApp supports **streaming (progressive) responses** — the bot edits its message in real-time as the AI generates text, like Discord and Telegram. Internally, WhatsApp is classified as a **TIER_MEDIUM** platform for delivery capabilities.

- **Chunking:** Long responses are automatically split into multiple messages at **4,096 characters** per chunk (WhatsApp's practical display limit). The gateway handles splitting and sends chunks sequentially — no configuration needed.
- **WhatsApp-compatible Markdown:** Standard Markdown in AI responses is auto-converted to WhatsApp's native formatting — `**bold**`→`*bold*`, `~~strikethrough~~`→`~strikethrough~`, `# Heading`→`*Heading*` (bold text, no native headings), `[link text](url)`→`link text (url)`. Code blocks and inline code are preserved as-is since WhatsApp supports triple-backtick formatting natively.
- **Tool progress:** When the agent calls tools (web search, file operations, etc.), WhatsApp displays real-time progress indicators showing which tool is running — enabled by default.
- **Message batching (debounce):** WhatsApp delivers each message individually, so a rapid burst (forwarded batches, paste-splits, multi-line text) would otherwise trigger a separate agent invocation per fragment. The adapter buffers successive text messages from the same chat and dispatches them as one combined request after a short quiet period (default **5s**, extended to **10s** for very long fragments):

```yaml
# ~/.hermes/config.yaml
gateway:
  platforms:
    whatsapp:
      extra:
        text_batch_delay_seconds: 5.0         # quiet period before flushing a batch
        text_batch_split_delay_seconds: 10.0  # extended delay near the split threshold
```

Set `text_batch_delay_seconds: 0` to dispatch each message immediately (disables batching).

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **QR code not scanning** | Ensure terminal is wide enough (60+ columns). Try a different terminal. Scan from the correct WhatsApp account (bot number, not personal). |
| **QR code expires** | QR codes refresh every ~20 seconds. If it times out, restart `hermes whatsapp`. |
| **Session not persisting** | Check that `~/.hermes/platforms/whatsapp/session` exists and is writable. If containerized, mount it as a persistent volume. |
| **Logged out unexpectedly** | WhatsApp unlinks devices after long inactivity. Keep the phone on and networked, then re-pair with `hermes whatsapp`. |
| **Bridge crashes or reconnect loops** | Restart the gateway, update Hermes, and re-pair if the session was invalidated by a protocol change. |
| **Bot stops working after WhatsApp update** | Update Hermes for the latest bridge version, then re-pair. |
| **macOS: "Node.js not installed" but node works in terminal** | launchd services don't inherit your shell PATH. Run `hermes gateway install` to re-snapshot PATH into the plist, then `hermes gateway start`. |
| **Messages not being received** | Verify `WHATSAPP_ALLOWED_USERS` includes the sender's number (country code, no `+`/spaces), or set `*`. Set `WHATSAPP_DEBUG=true` and restart to see raw events in `bridge.log`. |
| **Bot replies to strangers with a pairing code** | Set `whatsapp.unauthorized_dm_behavior: ignore` to silently ignore unauthorized DMs. |

## Security

**Configure access control before going live.** Set `WHATSAPP_ALLOWED_USERS` with specific phone numbers (with country code, without `+`), use `*` to allow everyone, or set `WHATSAPP_ALLOW_ALL_USERS=true`. Without any of these, the gateway **denies all incoming messages** as a safety measure. By default, unauthorized DMs still receive a pairing-code reply; for a private number that should stay completely silent to strangers, set `whatsapp.unauthorized_dm_behavior: ignore`.

Additional hardening from the source:

- The `~/.hermes/platforms/whatsapp/session` directory contains full session credentials — protect it like a password.
- Set file permissions: `chmod 700 ~/.hermes/platforms/whatsapp/session`.
- Use a **dedicated phone number** for the bot to isolate risk from your personal account.
- If you suspect compromise, unlink the device from WhatsApp → Settings → Linked Devices.
- Phone numbers in logs are partially redacted, but review your log retention policy.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/whatsapp.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp
**Last Updated**: 2026-06-19
**Status**: Active
