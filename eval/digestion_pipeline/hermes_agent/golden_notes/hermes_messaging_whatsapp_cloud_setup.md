---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - whatsapp
keywords:
  - whatsapp business cloud api
  - meta app webhook setup
  - phone number id access token
  - cloudflared tunnel public https
  - verify token handshake
  - hermes whatsapp-cloud wizard
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp-cloud
access_control_group: ["general"]
---

# Hermes Messaging — WhatsApp Business Cloud API Setup

## Overview

This is the **setup runbook** for connecting Hermes Agent to WhatsApp through Meta's **official WhatsApp Business Cloud API** — the production-grade path with no Node.js bridge subprocess, no QR codes, and no account-ban risk. It is the procedural half of the `whatsapp-cloud` source page; the capability/configuration **model** (full env-var reference, inbound/outbound/interactive feature matrix, known limitations, and the Baileys-vs-Cloud trade-off table) lives in its sibling [hermes_messaging_whatsapp_cloud_model](hermes_messaging_whatsapp_cloud_model.md).

The trade-off versus the unofficial [Baileys bridge](hermes_messaging_whatsapp_baileys.md): the Cloud path requires a **Meta Business account** (not personal WhatsApp), runs on a dedicated business phone number, needs a **public HTTPS URL** so Meta can POST inbound messages to a webhook, and is bound by Meta's 24-hour "customer service window" rule. The source frames the choice as: Cloud API for a real business bot wanting stability; Baileys for personal projects, quick demos, and single-user setups willing to risk the bot number's account.

The whole arc below — credentials, public tunnel, Meta-side webhook verification, the dual Meta-side + Hermes-side allowlists — is what the `hermes whatsapp-cloud` wizard automates; the rest of this note is the manual reference for what the wizard does.

## Quick start

```bash
hermes whatsapp-cloud
```

The wizard walks you through every credential, validates each one as you paste it (catches the #1 setup trap — pasting a phone number into the Phone Number ID field), and prints exact follow-up instructions for the parts that need to happen outside the wizard (starting cloudflared, configuring Meta's webhook dashboard).

## Prerequisites

1. **A Meta Business account** — create one at `business.facebook.com`.
2. **A Meta app with WhatsApp enabled** — see "Creating the Meta app" below.
3. **A way to expose a local port to the public internet** with HTTPS. Cloudflare Tunnel (`cloudflared`) is recommended — free, no port forwarding, no domain required. ngrok, your own domain with a reverse proxy + TLS, or a VPS with the gateway directly bound to a public IP all work too.
4. **Optional but recommended**: ffmpeg on `PATH` so outbound voice messages render as native WhatsApp voice-note bubbles instead of MP3 attachments. Hermes degrades gracefully if absent.

## Creating the Meta app

In `developers.facebook.com/apps`, **Create App** → choose use case **"Connect with customers through WhatsApp"** → pick or create a business portfolio → **Create app**. After creation you land on **Customize use case → Connect on WhatsApp → Quickstart**; click **Start using the API** to reach the **API Setup** page. Verify that a WhatsApp Business Account (WABA) is linked (one is auto-created if you created a new portfolio).

The wizard prompts for these dashboard values in this order:

| Value | Where in dashboard | Field shape | Notes |
|---|---|---|---|
| **Phone Number ID** | WhatsApp → API Setup → below the "From" dropdown | Numeric, 15–17 digits | **NOT** the phone number itself. Pasting the actual number here is the #1 setup mistake. |
| **Access Token** | WhatsApp → API Setup → "Generate access token" | Starts with `EAA`, 100+ chars | Temp tokens last 24h — see "Permanent token" for production. |
| **App Secret** | Settings → Basic → "Show" next to App secret | 32-char lowercase hex | Verifies incoming webhook signatures. Without it, inbound delivery is refused with 503. |
| **App ID** (optional) | Settings → Basic | Numeric, 15–16 digits | Not required for messaging; useful for analytics. |
| **WABA ID** (optional) | WhatsApp → API Setup → near the top | Numeric, 15+ digits | Not required for messaging; useful for analytics. |

## Permanent token (production)

Temporary access tokens expire after **24 hours**. For production use a **System User permanent token**:

1. Go to `business.facebook.com/latest/settings` → **System users**.
2. **Add** → name (e.g. `hermes-bot`) → role: **Admin**.
3. Select the new user → **Assign Assets**: toggle **Manage app** (Full control) on your app and **Manage WhatsApp Business Accounts** (Full control) on your WhatsApp account → **Assign assets**.
4. **Generate token** with permissions `business_management`, `whatsapp_business_messaging`, `whatsapp_business_management`.
5. Set **token expiration: Never**.
6. Copy the token → update `WHATSAPP_CLOUD_ACCESS_TOKEN` in `~/.hermes/.env` → restart the gateway.

System User tokens don't expire unless you explicitly revoke them.

## Exposing Hermes to the internet

The Cloud API delivers inbound messages by HTTPS POST to your webhook URL, so the Hermes gateway must be reachable from Meta's servers. Three common ways:

**Cloudflare Tunnel (recommended)** — free, no port forwarding, runs as a separate process alongside the gateway. Install with `winget install Cloudflare.cloudflared` (Windows), `brew install cloudflared` (macOS), or the release binary (Linux), then run a quick tunnel:

```bash
cloudflared tunnel --url http://localhost:8090
```

Note the printed `https://<random>.trycloudflare.com` URL — that is what you give Meta. Quick-tunnel URLs **rotate** on every restart of `cloudflared`; for a stable URL, run `cloudflared tunnel login` and create a named tunnel (free Cloudflare accounts get unlimited named tunnels).

**ngrok** — `ngrok http 8090`; free tier shows a different URL each restart, paid tier gives a stable subdomain. **Your own domain + reverse proxy** — if you already have a server with a TLS cert (Caddy, nginx, etc.), point a route at `localhost:8090`; most stable for production but requires existing infrastructure.

## Configuring the webhook on Meta's side

Once the tunnel is running:

1. Note the public URL printed by the tunnel — say `https://abc123.trycloudflare.com`.
2. Generate a **Verify Token** — the wizard does this with `secrets.token_urlsafe(32)`; manually:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   Save it as `WHATSAPP_CLOUD_VERIFY_TOKEN` in `~/.hermes/.env`.
3. Start the gateway: `hermes gateway`.
4. In the Meta App Dashboard → **WhatsApp → Configuration** → **Edit** on the Webhook section.
5. Fill in **Callback URL** `https://abc123.trycloudflare.com/whatsapp/webhook` and **Verify Token** (the string from step 2, must match exactly).
6. Click **Verify and save** — Meta hits your URL with a GET request, the gateway echoes back the challenge, and Meta marks the webhook verified.
7. Under **Webhook fields**, click **Manage** → subscribe to the **messages** field. This tells Meta to actually deliver inbound messages.

**To verify the loop manually** (from a third terminal):

```bash
TUNNEL="https://abc123.trycloudflare.com"
VERIFY="<your verify token>"

# Should print HTTP 200 with body "hello"
curl -i "$TUNNEL/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=$VERIFY&hub.challenge=hello"

# Health endpoint — should show verify_token_configured: true and app_secret_configured: true
curl "$TUNNEL/health"
```

## Recipient whitelist (Meta-side)

In development mode (before App Review), Meta restricts which numbers your bot can message: App Dashboard → WhatsApp → API Setup → **To** dropdown → **Manage phone number list** → add the numbers (Meta sends each a 6-digit verification code). Up to **5 numbers** in dev mode; going through App Review removes the limit.

## Allowlist (Hermes-side)

In addition to Meta's recipient whitelist, Hermes has its own per-platform allowlist controlling **which incoming messages the agent processes**. Add to `~/.hermes/.env`:

```bash
# Comma-separated phone numbers, country code, no '+' / spaces / dashes
WHATSAPP_CLOUD_ALLOWED_USERS=15551234567,15557654321

# Or allow everyone (only safe in combination with Meta's recipient whitelist)
# WHATSAPP_CLOUD_ALLOW_ALL_USERS=true
```

The wizard sets this in step 6. Without an allowlist, **every inbound message is denied** — intentional, so the bot can't be invoked by random numbers if the recipient whitelist is ever loosened.

## Polishing your bot's WhatsApp profile

WhatsApp displays a **name and profile picture** for the bot in the chat header and contact list. These can't be set via the Cloud API — they live in Meta's Business Manager at `business.facebook.com/wa/manage/phone-numbers`. Click your phone number to find: **Display name** (changes go through Meta's name-review, ~24–48h), **Profile picture** (square, ≥640×640px, updates immediately), **About / description / website / email / hours / category** (cosmetic info pane), and the **Verified badge** (green checkmark, requires Meta's separate business verification). The wizard prints these links at the end of setup; none of it is required for the bot to work.

## Troubleshooting (graph errors)

**Setup verification fails ("URL couldn't be validated")** — almost always a stale/wrong tunnel URL (cloudflared quick tunnels rotate — refresh both `.env` and Meta's dashboard), a verify-token mismatch (`WHATSAPP_CLOUD_VERIFY_TOKEN` must match exactly; run the curl probe to confirm the handshake locally first), the gateway not running, or the **App Secret not set** (without it, Hermes refuses inbound POSTs with 503 and Meta reads that as "can't validate").

- **`graph error 100`: Object with ID '…' does not exist** — you pasted your phone number (10–11 digits) into `WHATSAPP_CLOUD_PHONE_NUMBER_ID` instead of the Phone Number ID (Meta's 15–17 digit internal ID, shown *below* the "From" dropdown). The wizard catches this with a validator.
- **`graph error 190`: Authentication Error** — invalid access token. Subcode `463` = expired (temp tokens last 24h; regenerate or switch to a System User permanent token); `467` = invalidated (revoked or password changed); other `190` = the token lacked the required permissions when generated (ensure all three: `business_management`, `whatsapp_business_messaging`, `whatsapp_business_management`).
- **`graph error 131047`: Re-engagement message** — the 24-hour conversation window expired (see [the model note's Known limitations](hermes_messaging_whatsapp_cloud_model.md)). Ask the user to DM the bot first to reopen the window, or wait for template support.
- **Inbound `media metadata fetch failed (status=401)`** — same root cause as `graph error 190`; the access token is invalid or expired.
- **Bot replies appear as raw JSON / tool-call leakage** — the toolset configured for `whatsapp_cloud` is missing the tools the agent wants; check `hermes tools list` and verify the platform uses `hermes-whatsapp` (the default Cloud adapter toolset). See `hermes_cli/platforms.py` for the platform → default toolset mapping.
- **STT returns empty / "could not transcribe"** — the default `stt.provider: local` requires `pip install faster-whisper`; Nous subscribers can route STT through the managed gateway (`hermes config set stt.provider openai` / `stt.use_gateway true` / `hermes gateway restart`).

## Security notes

- **Treat the App Secret like a password** — anyone with it can forge webhook payloads Hermes will accept as authentic.
- **The verify token is a shared secret** — leaks are lower-stakes (worst case someone re-subscribes Meta's webhook to a URL of theirs) but still avoid committing it.
- **The access token is the bot's identity** — System User tokens are long-lived API keys; rotate immediately if a deployment is compromised.
- **The webhook endpoint accepts only signed requests when `WHATSAPP_CLOUD_APP_SECRET` is set** — leave it set even in development; without it the gateway refuses inbound delivery with HTTP 503.
- **The `/health` endpoint is unauthenticated** — safe to expose because it reports only config-presence booleans, not the values; restrict it at the reverse-proxy/tunnel layer if you'd rather not surface it.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/whatsapp-cloud.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp-cloud
**Last Updated**: 2026-06-19
**Status**: Active
