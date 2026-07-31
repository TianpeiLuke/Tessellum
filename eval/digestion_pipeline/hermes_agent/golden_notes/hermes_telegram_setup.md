---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - telegram
keywords:
  - Telegram setup
  - BotFather bot token
  - privacy mode
  - polling vs webhook
  - TELEGRAM_ALLOWED_USERS
  - DNS-over-HTTPS fallback IPs
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram
access_control_group: ["general"]
---

# Telegram Setup

## Overview

Telegram setup is the end-to-end procedure for standing up Hermes Agent as a full-featured Telegram bot — a conversational chat front-end you can reach from any device. The integration is built on [python-telegram-bot](https://python-telegram-bot.org/) and supports text, voice, images, and file attachments. The setup arc is: create and customize a bot via [@BotFather](https://t.me/BotFather), handle the privacy-mode gotcha (the single most common group-chat confusion), find your numeric user ID for the allowlist, configure Hermes (interactive wizard or manual `.env`), then choose a deployment transport (polling by default, or webhook for sleep-when-idle cloud hosts). The page also covers proxy support, the `/sethome` home channel for cron deliveries, a DNS-over-HTTPS fallback-IP mechanism for restricted networks, troubleshooting, and token security.

This note owns the **first-bot setup** procedure. Advanced operation — `MEDIA:` attachment delivery, voice STT/TTS, the local Bot API server for large files, group triggering, DM/group forum topics, Bot-API streaming/rich messages, slash-command access tiers, reactions, and per-channel prompts — lives in the sibling [hermes_telegram_advanced](hermes_telegram_advanced.md). The Telegram adapter is one platform wired into the shared [hermes_messaging_gateway_architecture](hermes_messaging_gateway_architecture.md), governed by the day-2 ops in [hermes_gateway_operations](hermes_gateway_operations.md).

## Step 1: Create a Bot via BotFather

Every Telegram bot requires an API token issued by [@BotFather](https://t.me/BotFather), Telegram's official bot management tool.

1. Open Telegram and search for **@BotFather**, or visit [t.me/BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a **display name** (e.g., "Hermes Agent") — this can be anything
4. Choose a **username** — this must be unique and end in `bot` (e.g., `my_hermes_bot`)
5. BotFather replies with your **API token**. It looks like this:

```
123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```

Keep your bot token secret — anyone with this token can control your bot. If it leaks, revoke it immediately via `/revoke` in BotFather.

## Step 2: Customize Your Bot (Optional)

BotFather commands that improve the user experience: `/setdescription` (the "What can this bot do?" text), `/setabouttext` (profile-page text), `/setuserpic` (avatar), `/setcommands` (the `/` command menu), and `/setprivacy` (group message visibility, see Step 3). A useful starting command set: `help`, `new`, `sethome`.

Optionally, enable `status_indicator` so Hermes sets the bot's short profile description to **Online** when the gateway connects and **Offline** on a clean shutdown. Telegram exposes no real online/offline presence dot for bots; the short description is the closest surface. It is **global** to the bot (visible to all users on the profile page, not a live in-chat badge), only a clean shutdown (`/stop`, `disconnect`) writes "Offline" (a hard crash leaves the last-known status), and it is off by default since it mutates the global profile.

## Step 3: Privacy Mode (Critical for Groups)

Telegram bots have a **privacy mode** that is **enabled by default** — the single most common source of confusion when using bots in groups. With privacy mode ON, the bot only sees messages starting with `/`, replies directly to the bot's own messages, service messages (joins/leaves/pins), and messages in channels where the bot is an admin. With privacy mode OFF, the bot receives every group message.

To disable it: message **@BotFather** → `/mybots` → select your bot → **Bot Settings → Group Privacy → Turn off**. You **must remove and re-add the bot to any group** after changing the privacy setting — Telegram caches the privacy state when a bot joins and will not update until the bot is removed and re-added. An alternative to disabling privacy mode is promoting the bot to **group admin**, since admin bots always receive all messages regardless of the privacy setting.

For OpenClaw/Yuanbao-style behavior — the bot can **see** ordinary group messages but only **responds** when triggered — set `observe_unmentioned_group_messages: true` alongside `require_mention: true`. Unmentioned messages from allowlisted chats are appended to the shared session transcript as observed context but do not dispatch the agent; a later mention, reply, or pattern match can use that context. This still requires Telegram to deliver ordinary group messages (disable privacy mode or promote to admin).

## Step 4: Find Your User ID

Hermes Agent uses numeric Telegram user IDs to control access. Your user ID is **not** your username — it's a number like `123456789`. Message [@userinfobot](https://t.me/userinfobot) (recommended — it instantly replies with your user ID) or [@get_id_bot](https://t.me/get_id_bot). Save this number for the next step.

## Step 5: Configure Hermes

**Option A: Interactive Setup (recommended).** Run `hermes gateway setup` and select **Telegram** when prompted. The wizard asks for your bot token and allowed user IDs, then writes the configuration for you.

**Option B: Manual Configuration.** Add the following to `~/.hermes/.env`:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_ALLOWED_USERS=123456789    # Comma-separated for multiple users
```

**Start the gateway** with `hermes gateway`. The bot should come online within seconds — send it a message on Telegram to verify.

## Webhook Mode

By default, Hermes connects using **long polling** — the gateway makes outbound requests to Telegram's servers to fetch new updates, which works well for local and always-on deployments. For **cloud deployments** (Fly.io, Railway, Render, etc.), **webhook mode** is more cost-effective: those platforms auto-wake suspended machines on inbound HTTP traffic but not on outbound connections, so a polling bot can never sleep. Webhook mode flips the direction — Telegram pushes updates to your bot's HTTPS URL, enabling sleep-when-idle deployments.

Add the following to `~/.hermes/.env`:

```bash
TELEGRAM_WEBHOOK_URL=https://my-app.fly.dev/telegram
TELEGRAM_WEBHOOK_SECRET="$(openssl rand -hex 32)"  # required
# TELEGRAM_WEBHOOK_PORT=8443        # optional, default 8443
```

`TELEGRAM_WEBHOOK_URL` is the public HTTPS URL where Telegram sends updates (the path is auto-extracted). `TELEGRAM_WEBHOOK_SECRET` is **required** when the URL is set — Telegram echoes it in every webhook request for verification and the gateway refuses to start without it (see advisory [GHSA-3vpc-7q5r-276h](https://github.com/NousResearch/hermes-agent/security/advisories/GHSA-3vpc-7q5r-276h)). `TELEGRAM_WEBHOOK_PORT` is the local listen port (default `8443`). When `TELEGRAM_WEBHOOK_URL` is set the gateway starts an HTTP webhook server instead of polling; when unset, polling mode is used with no behavior change.

For Fly.io: set the env vars as app secrets (`fly secrets set …`), expose the webhook port in `fly.toml`, then `fly deploy`. The `fly.toml` service block:

```toml
[[services]]
  internal_port = 8443
  protocol = "tcp"

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

The gateway log should show `[telegram] Connected to Telegram (webhook mode)`.

## Proxy Support

If Telegram's API is blocked or you need to route traffic through a proxy, set a Telegram-specific proxy URL — this takes priority over the generic `HTTPS_PROXY` / `HTTP_PROXY` env vars. In `config.yaml` (recommended), set `telegram.proxy_url: "socks5://127.0.0.1:1080"`; or via env var, `TELEGRAM_PROXY=socks5://127.0.0.1:1080`. Supported schemes are `http://`, `https://`, and `socks5://`. The proxy applies to both the main Telegram connection and the fallback IP transport. If no Telegram-specific proxy is set, the gateway falls back to `HTTPS_PROXY` / `HTTP_PROXY` / `ALL_PROXY` (or macOS system proxy auto-detection). The Telegram adapter checks `HTTPS_PROXY`, `HTTP_PROXY`, `ALL_PROXY` (and lowercase variants) in order, using the first one set; the standard `httpx` client used elsewhere already respects proxy env vars natively.

## Home Channel

Use `/sethome` in any Telegram chat (DM or group) to designate it as the **home channel** — scheduled tasks (cron jobs) deliver their results there. You can also set it manually in `~/.hermes/.env` with `TELEGRAM_HOME_CHANNEL=-1001234567890` and `TELEGRAM_HOME_CHANNEL_NAME="My Notes"`. Group chat IDs are negative numbers; your personal DM chat ID is the same as your user ID.

If topic mode is enabled in your bot DM, cron messages delivered to the root chat land in the system-only lobby. Create a dedicated forum topic (e.g. `Cron`) and set `TELEGRAM_CRON_THREAD_ID=<topic_thread_id>`, which overrides `TELEGRAM_HOME_CHANNEL_THREAD_ID` for cron deliveries only; replies in that topic continue the topic's existing session.

## DNS-over-HTTPS Fallback IPs

In some restricted networks, `api.telegram.org` may resolve to an unreachable IP. The Telegram adapter includes a **fallback IP** mechanism that transparently retries connections against alternative IPs while preserving the correct TLS hostname and SNI. How it works: (1) if `TELEGRAM_FALLBACK_IPS` is set, those IPs are used directly; (2) otherwise the adapter queries **Google DNS** and **Cloudflare DNS** via DNS-over-HTTPS (DoH) to discover alternative IPs; (3) DoH IPs that differ from the system DNS result are used as fallbacks; (4) if DoH is also blocked, a hardcoded seed IP (`149.154.167.220`) is used as a last resort; (5) once a fallback IP succeeds it becomes "sticky" for subsequent requests. You usually don't need to configure this — auto-discovery via DoH handles most scenarios. To set explicit fallback IPs:

```bash
TELEGRAM_FALLBACK_IPS=149.154.167.220,149.154.167.221
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Bot not responding at all | Verify `TELEGRAM_BOT_TOKEN` is correct. Check `hermes gateway` logs for errors. |
| Bot responds with "unauthorized" | Your user ID is not in `TELEGRAM_ALLOWED_USERS`. Double-check with @userinfobot. |
| Bot ignores group messages | Privacy mode is likely on. Disable it (Step 3) or make the bot a group admin. **Remember to remove and re-add the bot after changing privacy.** |
| Bot token revoked/invalid | Generate a new token via `/revoke` then `/newbot` or `/token` in BotFather. Update your `.env` file. |
| Webhook not receiving updates | Verify `TELEGRAM_WEBHOOK_URL` is publicly reachable (test with `curl`). Ensure your platform/reverse proxy routes inbound HTTPS to the local listen port (`TELEGRAM_WEBHOOK_PORT`; they need not be the same number). Ensure SSL/TLS is active — Telegram only sends to HTTPS URLs. Check firewall rules. |

(Voice-transcription and voice-bubble troubleshooting rows are covered with the voice feature in [hermes_telegram_advanced](hermes_telegram_advanced.md).)

## Security

Always set `TELEGRAM_ALLOWED_USERS` to restrict who can interact with your bot. Without it, the gateway **denies all users by default** as a safety measure. Never share your bot token publicly; if compromised, revoke it immediately via BotFather's `/revoke` command. For the full gateway security model see [hermes_gateway_operations](hermes_gateway_operations.md) and the Hermes [Security documentation](https://hermes-agent.nousresearch.com/docs/user-guide/security); you can also use [DM pairing](https://hermes-agent.nousresearch.com/docs/user-guide/messaging#dm-pairing-alternative-to-allowlists) for a more dynamic approach to user authorization.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/telegram.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram
**Last Updated**: 2026-06-19
**Status**: Active
