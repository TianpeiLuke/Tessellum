---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - sms
keywords:
  - hermes sms twilio gateway
  - twilio account sid auth token
  - x-twilio-signature webhook validation
  - sms allowlist deny by default
  - 1600 character sms chunking
  - sms home channel cron delivery
topics:
  - Hermes Agent
  - Messaging
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/sms
access_control_group: ["general"]
---

# Hermes Agent — SMS Setup (Twilio)

## Overview

This is the **runbook for connecting Hermes Agent to SMS through the [Twilio](https://www.twilio.com/) API** — people text your Twilio phone number and get AI responses back, the same conversational experience as Telegram or Discord but over standard text messages. The setup arc is: get Twilio credentials → put them plus an allowlist in `~/.hermes/.env` → point the Twilio number's webhook at Hermes' `/webhooks/twilio` endpoint → start the gateway. Inbound SMS arrives as a webhook POST from Twilio, so Hermes runs a small aiohttp webhook server (default port `8080`) that must be publicly reachable; for local hosts the page recommends a `cloudflared` or `ngrok` tunnel. SMS shares its Twilio credentials with the optional telephony skill (same `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` / `TWILIO_PHONE_NUMBER`). Security rests on two pillars the page stresses: the `X-Twilio-Signature` HMAC-SHA1 webhook-signature check (so forged inbound messages are rejected) and a deny-by-default user allowlist. SMS has no built-in encryption, so the page warns against sensitive operations over SMS and points to Signal or Telegram instead. The shared gateway concepts — the platform↔agent bridge, DM-pairing — are documented elsewhere; this note owns only the Twilio-specific setup.

## Prerequisites

- **Twilio account** — sign up at twilio.com (free trial available).
- **A Twilio phone number** with SMS capability.
- **A publicly accessible server** — Twilio sends webhooks to your server when SMS arrives.
- **aiohttp** — install the SMS extra with `pip install 'hermes-agent[sms]'`.

The SMS gateway shares credentials with the optional telephony skill: if you have already set up Twilio for voice calls or one-off SMS, the gateway works with the same `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_PHONE_NUMBER`.

## Step 1: Get Your Twilio Credentials

1. Go to the Twilio Console.
2. Copy your **Account SID** and **Auth Token** from the dashboard.
3. Go to **Phone Numbers → Manage → Active Numbers** — note your phone number in E.164 format (e.g., `+15551234567`).

## Step 2: Configure Hermes

The recommended path is the interactive wizard, which prompts for credentials after you pick **SMS (Twilio)** from the platform list:

```bash
hermes gateway setup
```

For manual setup, add the credentials, allowlist, and optional home channel to `~/.hermes/.env`:

```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+15551234567

# Security: restrict to specific phone numbers (recommended)
SMS_ALLOWED_USERS=+15559876543,+15551112222

# Optional: set a home channel for cron job delivery
SMS_HOME_CHANNEL=+15559876543
```

## Step 3: Configure Twilio Webhook

Twilio needs to know where to send incoming messages. In the Twilio Console:

1. Go to **Phone Numbers → Manage → Active Numbers**.
2. Click your phone number.
3. Under **Messaging → A MESSAGE COMES IN**, set **Webhook** to `https://your-server:8080/webhooks/twilio` and **HTTP Method** to `POST`.

If Hermes runs locally, expose the webhook with a tunnel and set the resulting public URL as your Twilio webhook:

```bash
# Using cloudflared
cloudflared tunnel --url http://localhost:8080

# Using ngrok
ngrok http 8080
```

Then set `SMS_WEBHOOK_URL` to the *same* URL you configured in Twilio — it is required for Twilio signature validation, and the adapter will refuse to start without it. The webhook port defaults to `8080` (override with `SMS_WEBHOOK_PORT`):

```bash
# Must match the webhook URL in your Twilio Console
SMS_WEBHOOK_URL=https://your-server:8080/webhooks/twilio
```

## Step 4: Start the Gateway

```bash
hermes gateway
```

On a healthy start you should see the listener line (the source number is partially redacted):

```
[sms] Twilio webhook server listening on 127.0.0.1:8080, from: +1555***4567
```

If you instead see `Refusing to start: SMS_WEBHOOK_URL is required`, set `SMS_WEBHOOK_URL` to the public URL configured in your Twilio Console (see Step 3). Once running, text your Twilio number — Hermes will respond via SMS.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TWILIO_ACCOUNT_SID` | Yes | Twilio Account SID (starts with `AC`) |
| `TWILIO_AUTH_TOKEN` | Yes | Twilio Auth Token (also used for webhook signature validation) |
| `TWILIO_PHONE_NUMBER` | Yes | Your Twilio phone number (E.164 format) |
| `SMS_WEBHOOK_URL` | Yes | Public URL for Twilio signature validation — must match the webhook URL in your Twilio Console |
| `SMS_WEBHOOK_PORT` | No | Webhook listener port (default: `8080`) |
| `SMS_WEBHOOK_HOST` | No | Webhook bind address (default: `127.0.0.1`) |
| `SMS_INSECURE_NO_SIGNATURE` | No | Set to `true` to disable signature validation (local dev only — **not for production**) |
| `SMS_ALLOWED_USERS` | No | Comma-separated E.164 phone numbers allowed to chat |
| `SMS_ALLOW_ALL_USERS` | No | Set to `true` to allow anyone (not recommended) |
| `SMS_HOME_CHANNEL` | No | Phone number for cron job / notification delivery |
| `SMS_HOME_CHANNEL_NAME` | No | Display name for the home channel (default: `Home`) |

## SMS-Specific Behavior

- **Plain text only** — Markdown is automatically stripped since SMS renders it as literal characters.
- **1600 character limit** — Longer responses are split across multiple messages at natural boundaries (newlines, then spaces).
- **Echo prevention** — Messages from your own Twilio number are ignored to prevent loops.
- **Phone number redaction** — Phone numbers are redacted in logs for privacy.

## Security

**Webhook signature validation.** Hermes validates that inbound webhooks genuinely originate from Twilio by verifying the `X-Twilio-Signature` header (HMAC-SHA1), preventing attackers from injecting forged messages. `SMS_WEBHOOK_URL` is required — set it to the public URL configured in your Twilio Console; the adapter refuses to start without it. For local development without a public URL, validation can be disabled with `SMS_INSECURE_NO_SIGNATURE=true` (local dev only — **not for production**).

**User allowlists.** The gateway denies all users by default. Configure an allowlist with `SMS_ALLOWED_USERS` (comma-separated E.164 numbers), or `SMS_ALLOW_ALL_USERS=true` to allow anyone — not recommended for bots with terminal access. The page warns that SMS has no built-in encryption: do not use it for sensitive operations unless you understand the implications, and prefer Signal or Telegram for sensitive use cases.

## Troubleshooting

- **Messages not arriving** — confirm the Twilio webhook URL is correct and publicly accessible; verify `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`; check the Twilio Console **Monitor → Logs → Messaging** for delivery errors; ensure your number is in `SMS_ALLOWED_USERS` (or `SMS_ALLOW_ALL_USERS=true`).
- **Replies not sending** — confirm `TWILIO_PHONE_NUMBER` is set in E.164 format with `+`; verify the Twilio account has SMS-capable numbers; check Hermes gateway logs for Twilio API errors.
- **Webhook port conflicts** — if port `8080` is in use, change it with `SMS_WEBHOOK_PORT=3001` and update the webhook URL in the Twilio Console to match.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/sms.md`
**Last Updated**: 2026-06-19
**Status**: Active
