---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - discord
keywords:
  - hermes discord bot setup
  - privileged gateway intents
  - DISCORD_BOT_TOKEN
  - DISCORD_ALLOWED_USERS
  - oauth2 invite url
  - DISCORD_ALLOWED_ROLES
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord
access_control_group: ["general"]
---

# Hermes Agent — Discord Setup

## Overview

This is the **end-to-end procedure for standing up Hermes Agent as a Discord bot** — the steps that take you from an empty Discord Developer Portal to a bot that is online in your server and answering messages. Hermes integrates with Discord as a bot reachable through direct messages or server channels: it receives a message, runs it through the full Hermes pipeline (tool use, memory, reasoning), and replies in real time, supporting text, voice messages, file attachments, and slash commands. The eight-step arc is: create an Application, create the Bot, enable the **Privileged Gateway Intents** (the single most failure-prone step), grab the bot token, build an OAuth2 invite URL, invite the bot to a server, find your Discord User ID, then configure Hermes (interactive wizard or manual `.env`). This note also captures the behavioral preview ("How Hermes Behaves"), the troubleshooting catalog, and the security model including role-based access. The deeper runtime model (gateway session isolation, the full configuration reference, media, `voice_fx`, forum channels) lives in [hermes_discord_advanced](hermes_discord_advanced.md); the cross-cutting gateway concepts and ops live in [hermes_messaging_gateway_architecture](hermes_messaging_gateway_architecture.md) and [hermes_gateway_operations](hermes_gateway_operations.md).

## How Hermes Behaves

Before setup, the behavior most people want to know once the bot is in a server:

- **DMs** — Hermes responds to every message; no `@mention` needed; each DM has its own session.
- **Server channels** — by default Hermes only responds when you `@mention` it; an un-mentioned post is ignored.
- **Free-response channels** — make specific channels mention-free with `DISCORD_FREE_RESPONSE_CHANNELS`, or disable mentions globally with `DISCORD_REQUIRE_MENTION=false`; these channels answer inline and skip auto-threading so the channel stays a lightweight chat.
- **Threads** — Hermes replies in the same thread; mention rules still apply unless the thread or its parent channel is free-response; threads stay isolated from the parent channel for session history.
- **Shared channels with multiple users** — by default Hermes isolates session history per user inside the channel; two people in the same channel do not share one transcript unless you explicitly disable that.
- **Messages mentioning other users** — when `DISCORD_IGNORE_NO_MENTION` is `true` (the default), Hermes stays silent if a message `@mentions` other users but not the bot, so it does not jump into conversations directed at other people (server channels only, not DMs).

The session-isolation and config knobs behind these behaviors (the Discord Gateway Model, `group_sessions_per_user`, the full env-var/`config.yaml` reference) are documented in [hermes_discord_advanced](hermes_discord_advanced.md).

## Step 1: Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and sign in.
2. Click **New Application** in the top-right corner.
3. Enter a name (e.g., "Hermes Agent") and accept the Developer Terms of Service.
4. Click **Create**.

On the **General Information** page, note the **Application ID** — you need it later to build the invite URL.

## Step 2: Create the Bot

1. In the left sidebar, click **Bot**.
2. Discord automatically creates a bot user; you can customize the username.
3. Under **Authorization Flow**, set **Public Bot** to **ON** (required to use the Discord-provided invite link — recommended; this enables the Installation tab to generate a default authorization URL) and leave **Require OAuth2 Code Grant** **OFF**.

If you keep the bot private (Public Bot = OFF), you **must** use the **Manual URL** method in Step 5 instead of the Installation tab.

## Step 3: Enable Privileged Gateway Intents

> This is the most critical step in the entire setup. Without the correct intents enabled, your bot will connect to Discord but **will not be able to read message content**.

On the **Bot** page, scroll to **Privileged Gateway Intents** — three toggles:

| Intent | Purpose | Required? |
|--------|---------|-----------|
| **Presence Intent** | See user online/offline status | Optional |
| **Server Members Intent** | Access the member list, resolve usernames | **Required** |
| **Message Content Intent** | Read the text content of messages | **Required** |

Enable **both Server Members Intent and Message Content Intent**, then click **Save Changes**. Without **Message Content Intent** the bot receives message events but the text is empty — it literally cannot see what you typed (this is the #1 reason Discord bots don't respond). Without **Server Members Intent** it cannot resolve usernames for the allowed-users list. If a bot is in **100 or more servers**, Discord requires a verification application to use privileged intents; for personal use (under 100 servers) you toggle them freely.

## Step 4: Get the Bot Token

The bot token is the credential Hermes uses to log in as the bot. Still on the **Bot** page:

1. Under **Token**, click **Reset Token**.
2. Enter your 2FA code if enabled.
3. Discord displays the new token. **Copy it immediately** — it is shown only once.

Never share the token or commit it to Git — anyone with it has full control of your bot. Store it safely (a password manager); you need it in Step 8.

## Step 5: Generate the Invite URL

You need an OAuth2 URL to invite the bot. **Option A (recommended, requires Public Bot = ON):** in the sidebar click **Installation** → under **Installation Contexts** enable **Guild Install** → for **Install Link** select **Discord Provided Link** → under **Default Install Settings** set **Scopes** = `bot` and `applications.commands`, and select the permissions below. **Option B (Manual URL):** construct it directly, replacing `YOUR_APP_ID` with the Application ID from Step 1:

```
https://discord.com/oauth2/authorize?client_id=YOUR_APP_ID&scope=bot+applications.commands&permissions=274878286912
```

Minimum permissions: **View Channels**, **Send Messages**, **Embed Links**, **Attach Files**, **Read Message History**. Recommended additions: **Send Messages in Threads**, **Add Reactions**. The two ready-made permission integers:

| Level | Permissions Integer | What's Included |
|-------|---------------------|-----------------|
| Minimal | `117760` | View Channels, Send Messages, Read Message History, Attach Files |
| Recommended | `274878286912` | All of the above plus Embed Links, Send Messages in Threads, Add Reactions |

## Step 6: Invite to Your Server

1. Open the invite URL (Installation tab or your manual URL) in a browser.
2. In the **Add to Server** dropdown, select your server.
3. Click **Continue**, then **Authorize**.
4. Complete the CAPTCHA if prompted.

You need the **Manage Server** permission to invite a bot; if your server is not in the dropdown, ask a server admin to use the link. After authorizing, the bot appears in the member list (showing offline until you start the Hermes gateway).

## Step 7: Find Your Discord User ID

Hermes uses your Discord User ID to control who can interact with the bot:

1. Open Discord (desktop or web).
2. **Settings** → **Advanced** → toggle **Developer Mode** to **ON**.
3. Close settings.
4. Right-click your username (in a message, the member list, or your profile) → **Copy User ID**.

Your User ID is a long number like `284102345871466496`. Developer Mode also lets you copy **Channel IDs** and **Server IDs** the same way — you need a Channel ID for a manual home channel.

## Step 8: Configure Hermes Agent

**Option A — Interactive Setup (recommended):**

```bash
hermes gateway setup
```

Select **Discord** when prompted, then paste your bot token and user ID. **Option B — Manual Configuration:** add to `~/.hermes/.env`:

```bash
# Required
DISCORD_BOT_TOKEN=your-bot-token
DISCORD_ALLOWED_USERS=284102345871466496

# Multiple allowed users (comma-separated)
# DISCORD_ALLOWED_USERS=284102345871466496,198765432109876543
```

Then start the gateway with `hermes gateway`. The bot comes online within a few seconds — send it a DM or a message in a channel it can see to test. You can run `hermes gateway` in the background or as a systemd service for persistent operation (see [hermes_gateway_operations](hermes_gateway_operations.md)). The full Discord configuration reference (mention/threading/backfill/media knobs in `.env` and `config.yaml`) is in [hermes_discord_advanced](hermes_discord_advanced.md).

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Bot is online but not responding | **Message Content Intent** is disabled | Developer Portal → app → Bot → Privileged Gateway Intents → enable **Message Content Intent** → Save → restart the gateway |
| "Disallowed Intents" error on startup | Code requests intents not enabled in the portal | Enable all three Privileged Gateway Intents (Presence, Server Members, Message Content), then restart |
| Bot can't see messages in a specific channel | Bot's role lacks permission to view that channel | Channel settings → Permissions → add the bot's role with **View Channel** and **Read Message History** |
| 403 Forbidden errors | Bot is missing required permissions | Re-invite with the correct permissions (Step 5) or adjust the bot's role in Server Settings → Roles |
| Bot is offline | Gateway not running, or token incorrect | Check `hermes gateway` is running; verify `DISCORD_BOT_TOKEN` in `.env` (update it if you reset the token) |
| "User not allowed" / bot ignores you | Your User ID is not in `DISCORD_ALLOWED_USERS` | Add your User ID to `DISCORD_ALLOWED_USERS` and restart |
| Users in the same channel share context unexpectedly | `group_sessions_per_user` is disabled, or no user ID is available for those messages | Set `group_sessions_per_user: true` in `config.yaml` and restart (leave it off only if you want a shared room — see [hermes_discord_advanced](hermes_discord_advanced.md)) |

## Security

> Always set `DISCORD_ALLOWED_USERS` (or `DISCORD_ALLOWED_ROLES`) to restrict who can interact with the bot. Without either, the gateway **denies all users by default** as a safety measure. Only authorize people you trust — authorized users have full access to the agent's capabilities, including tool use and system access.

### Role-Based Access Control

For servers where access is managed by roles instead of individual user lists (moderator teams, support staff, internal tooling), use `DISCORD_ALLOWED_ROLES` — a comma-separated list of role IDs; any member with one of those roles is authorized:

```bash
# ~/.hermes/.env — works alongside or instead of DISCORD_ALLOWED_USERS
DISCORD_ALLOWED_ROLES=987654321098765432,876543210987654321
```

Semantics: it is **OR** with the user allowlist (authorized if the ID is in `DISCORD_ALLOWED_USERS` **or** the member has a role in `DISCORD_ALLOWED_ROLES`); setting it **auto-enables the Server Members Intent** on connect (required for Discord to send role info); use **role IDs, not names** (Developer Mode ON → right-click a role → **Copy Role ID**); in DMs the role check scans mutual guilds, so a user with an allowed role in any shared server is authorized in DMs too. This is the preferred pattern when a moderation team churns — new mods get access the moment the role is granted, with no `.env` edit or gateway restart.

### Mention Control

By default Hermes blocks the bot from pinging `@everyone`, `@here`, and role mentions even if its reply contains those tokens (preventing a poorly-worded prompt or echoed user content from spamming a whole server); individual `@user` pings and reply-reference pings stay enabled. The full `allow_mentions` env-var/`config.yaml` reference is in [hermes_discord_advanced](hermes_discord_advanced.md). For broader deployment security, the source page links out to the Hermes Security Guide (`../security.md`, owned by SP03's `hermes_security_skill_memory_settings`).

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/discord.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord
**Last Updated**: 2026-06-19
**Status**: Active
