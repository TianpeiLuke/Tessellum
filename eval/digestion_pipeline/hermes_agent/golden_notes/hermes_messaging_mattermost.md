---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - mattermost
keywords:
  - hermes mattermost bot
  - mattermost rest api v4
  - mattermost websocket gateway
  - mattermost allowed users
  - mattermost reply mode thread
  - self-hosted slack alternative
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/mattermost
access_control_group: ["general"]
---

# Hermes Agent — Mattermost Setup

## Overview

Mattermost setup is the procedure for running Hermes Agent as a **bot inside a self-hosted Mattermost instance**, letting you chat with the agent through direct messages or team channels. Mattermost is a self-hosted, open-source Slack alternative — you run it on your own infrastructure and keep full control of your data. The bot connects via Mattermost's **REST API (v4)** for sending messages and a **WebSocket** for real-time events, processes each message through the Hermes Agent pipeline (tool use, memory, reasoning), and responds in real time. It supports text, file attachments, images, and slash commands.

No external Mattermost library is required — the adapter uses `aiohttp`, which is already a Hermes dependency. The setup arc is: enable bot accounts → create the bot → add it to channels → find your 26-character user ID → configure Hermes → start the gateway. Access is allowlist-gated (`MATTERMOST_ALLOWED_USERS`), sessions isolate per user by default, and channel responses require an `@mention` unless you relax it.

## How Hermes Behaves

| Context | Behavior |
|---------|----------|
| **DMs** | Hermes responds to every message. No `@mention` needed. Each DM has its own session. |
| **Public/private channels** | Hermes responds when you `@mention` it. Without a mention, Hermes ignores the message. |
| **Threads** | If `MATTERMOST_REPLY_MODE=thread`, Hermes replies in a thread under your message. Thread context stays isolated from the parent channel. |
| **Shared channels with multiple users** | By default, Hermes isolates session history per user inside the channel. Two people talking in the same channel do not share one transcript unless you explicitly disable that. |

To reply as threaded conversations (nested under your original message), set `MATTERMOST_REPLY_MODE=thread`. The default is `off`, which sends flat messages in the channel.

### Session Model in Mattermost

By default each DM gets its own session, each thread gets its own session namespace, and each user in a shared channel gets their own session inside that channel. This is controlled by `config.yaml` via `group_sessions_per_user: true`. Set it to `false` only if you explicitly want one shared conversation for the entire channel — but then users share context growth and token costs, one person's long tool-heavy task can bloat everyone else's context, and one person's in-flight run can interrupt another person's follow-up in the same channel. (The gateway session model is shared across platforms — see the SP02 config-reference cluster.)

## Step 1: Enable Bot Accounts

Bot accounts must be enabled on your Mattermost server before you can create one:

1. Log in to Mattermost as a **System Admin**.
2. Go to **System Console** → **Integrations** → **Bot Accounts**.
3. Set **Enable Bot Account Creation** to **true**.
4. Click **Save**.

If you don't have System Admin access, ask your Mattermost administrator to enable bot accounts and create one for you.

## Step 2: Create a Bot Account

1. Click the **☰** menu (top-left) → **Integrations** → **Bot Accounts**.
2. Click **Add Bot Account**.
3. Fill in the details — **Username** (e.g., `hermes`), **Display Name** (e.g., `Hermes Agent`), optional **Description**, and **Role** (`Member` is sufficient).
4. Click **Create Bot Account**.
5. Mattermost displays the **bot token**. **Copy it immediately.**

The bot token is only displayed once when you create the bot account; if you lose it you must regenerate it from the bot account settings. Never share the token publicly or commit it to Git — anyone with this token has full control of the bot. Store it somewhere safe (a password manager); you need it in Step 5.

You can also use a **personal access token** instead of a bot account (**Profile** → **Security** → **Personal Access Tokens** → **Create Token**). This is useful if you want Hermes to post as your own user rather than a separate bot user.

## Step 3: Add the Bot to Channels

The bot must be a member of any channel where you want it to respond: open the channel → click the channel name → **Add Members** → search for your bot username (e.g., `hermes`) and add it. For DMs, simply open a direct message with the bot — it can respond immediately.

## Step 4: Find Your Mattermost User ID

Hermes uses your Mattermost User ID to control who can interact with the bot. Click your **avatar** (top-left corner) → **Profile**; your User ID is displayed in the profile dialog (click it to copy). The User ID is a **26-character alphanumeric string** like `3uo8dkh1p7g1mfk49ear5fzs5c` — it is **not** your username (the username is what appears after `@`, e.g., `@alice`). You can also get it via the API:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-mattermost-server/api/v4/users/me | jq .id
```

To get a **Channel ID** (needed for a manual home channel): click the channel name → **View Info**.

## Step 5: Configure Hermes Agent

**Option A: Interactive Setup (Recommended)** — run `hermes gateway setup`, select **Mattermost** when prompted, then paste your server URL, bot token, and user ID when asked.

**Option B: Manual Configuration** — add the following to your `~/.hermes/.env` file:

```bash
# Required
MATTERMOST_URL=https://mm.example.com
MATTERMOST_TOKEN=***
MATTERMOST_ALLOWED_USERS=3uo8dkh1p7g1mfk49ear5fzs5c

# Multiple allowed users (comma-separated)
# MATTERMOST_ALLOWED_USERS=3uo8dkh1p7g1mfk49ear5fzs5c,8fk2jd9s0a7bncm1xqw4tp6r3e

# Optional: reply mode (thread or off, default: off)
# MATTERMOST_REPLY_MODE=thread

# Optional: respond without @mention (default: true = require mention)
# MATTERMOST_REQUIRE_MENTION=false

# Optional: channels where bot responds without @mention (comma-separated channel IDs)
# MATTERMOST_FREE_RESPONSE_CHANNELS=channel_id_1,channel_id_2
```

Optional behavior settings go in `~/.hermes/config.yaml` — `group_sessions_per_user: true` keeps each participant's context isolated inside shared channels and threads.

### Start the Gateway

Once configured, start the gateway with `hermes gateway`. The bot should connect to your Mattermost server within a few seconds — send it a message (a DM or in a channel where it's been added) to test. You can run `hermes gateway` in the background or as a systemd service for persistent operation.

## Home Channel

You can designate a "home channel" where the bot sends proactive messages (cron job output, reminders, notifications). Two ways: type `/sethome` in any Mattermost channel where the bot is present (that channel becomes the home channel), or add `MATTERMOST_HOME_CHANNEL=abc123def456ghi789jkl012mn` to `~/.hermes/.env` (replace the ID with the actual channel ID via the channel name → View Info).

## Reply Mode

`MATTERMOST_REPLY_MODE` controls how Hermes posts responses:

| Mode | Behavior |
|------|----------|
| `off` (default) | Hermes posts flat messages in the channel, like a normal user. |
| `thread` | Hermes replies in a thread under your original message. Keeps channels clean when there's lots of back-and-forth. |

## Mention Behavior

By default the bot only responds in channels when `@mentioned`. Two variables change this:

| Variable | Default | Description |
|----------|---------|-------------|
| `MATTERMOST_REQUIRE_MENTION` | `true` | Set to `false` to respond to all messages in channels (DMs always work). |
| `MATTERMOST_FREE_RESPONSE_CHANNELS` | _(none)_ | Comma-separated channel IDs where the bot responds without `@mention`, even when require_mention is true. |

When the bot is `@mentioned`, the mention is automatically stripped from the message before processing.

## Channel allowlist (`allowed_channels`)

Restrict the bot to a fixed set of Mattermost channels. When set, the bot **only** responds in channels whose ID appears in the list — messages from any other channel are silently ignored, even if the bot is `@mentioned`. **DMs are exempt** from this filter, so authorized users can always reach the bot in a direct message.

```yaml
mattermost:
  allowed_channels:
    - "abc123def456ghi789jkl012mno"   # #ops
    - "xyz987uvw654rst321opq098nml"   # #incident-response
```

Or via env var: `MATTERMOST_ALLOWED_CHANNELS="abc123def456ghi789jkl012mno,xyz987uvw654rst321opq098nml"`. Empty/unset → no restriction (fully backward compatible); non-empty → the channel ID must be on the list, or the message is dropped before any other gating (mention requirement, `MATTERMOST_FREE_RESPONSE_CHANNELS`, etc.) runs.

## Troubleshooting

- **Bot is not responding to messages** — the bot is not a member of the channel, or `MATTERMOST_ALLOWED_USERS` doesn't include your User ID. Add the bot to the channel, verify your User ID is in the allowlist, restart the gateway.
- **403 Forbidden errors** — the bot token is invalid, or the bot lacks permission to post. Check `MATTERMOST_TOKEN`, confirm the bot account isn't deactivated, verify it's in the channel; for a personal access token, ensure your account has the required permissions.
- **WebSocket disconnects / reconnection loops** — network instability, server restarts, or firewall/proxy issues. The adapter automatically reconnects with **exponential backoff (2s → 60s)**. Reverse proxies (nginx, Apache) need WebSocket upgrade headers configured. For nginx:

```nginx
location /api/v4/websocket {
    proxy_pass http://mattermost-backend;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 600s;
}
```

- **"Failed to authenticate" on startup** — the token or server URL is incorrect. Verify `MATTERMOST_URL` (include `https://`, no trailing slash) and test `MATTERMOST_TOKEN` with `curl -H "Authorization: Bearer YOUR_TOKEN" https://your-server/api/v4/users/me`.
- **Bot is offline** — the gateway isn't running or failed to connect. Check `hermes gateway` is running and read the terminal output (wrong URL, expired token, unreachable server).
- **"User not allowed" / Bot ignores you** — your User ID isn't in `MATTERMOST_ALLOWED_USERS`. Add it and restart. Remember it is a 26-character alphanumeric string, not your `@username`.

## Per-Channel Prompts

Assign ephemeral system prompts to specific Mattermost channels. The prompt is injected at runtime on every turn — never persisted to transcript history — so changes take effect immediately. Keys are Mattermost channel IDs; all messages in the matching channel get the prompt injected as an ephemeral system instruction.

```yaml
mattermost:
  channel_prompts:
    "channel_id_abc123": |
      You are a research assistant. Focus on academic sources,
      citations, and concise synthesis.
    "channel_id_def456": |
      Code review mode. Be precise about edge cases and
      performance implications.
```

## Security

Always set `MATTERMOST_ALLOWED_USERS` to restrict who can interact with the bot. Without it, the gateway **denies all users by default** as a safety measure. Only add User IDs of people you trust — authorized users have full access to the agent's capabilities, including tool use and system access.

## Notes

- **Self-hosted friendly**: Works with any self-hosted Mattermost instance. No Mattermost Cloud account or subscription required.
- **No extra dependencies**: The adapter uses `aiohttp` for HTTP and WebSocket, which is already included with Hermes Agent.
- **Team Edition compatible**: Works with both Mattermost Team Edition (free) and Enterprise Edition.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/mattermost.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/mattermost
**Last Updated**: 2026-06-19
**Status**: Active
