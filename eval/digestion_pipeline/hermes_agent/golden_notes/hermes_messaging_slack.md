---
tags:
  - resource
  - documentation
  - hermes_agent
  - messaging
  - slack
keywords:
  - hermes slack bot
  - socket mode setup
  - slack app manifest
  - bot token scopes
  - event subscriptions
  - cmd thread prefix
topics:
  - Hermes Agent
  - Messaging Gateway
  - Slack
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack
access_control_group: ["general"]
---

# Hermes Agent — Slack Setup

## Overview

This note is the **one-time setup procedure** for connecting Hermes Agent to Slack as a bot using **Socket Mode**. Socket Mode uses WebSockets instead of public HTTP endpoints, so the Hermes instance does not need to be publicly accessible — it works behind firewalls, on a laptop, or on a private server. The procedure walks the nine Slack-app creation steps (manifest or manual), the eleven required bot-token scopes, the App-Level + Bot token pair, the four event subscriptions, the Messages Tab gate, install/invite, finding Member IDs for the allowlist, and the minimal `~/.hermes/.env` wiring; it then covers slash commands (including the `!cmd` thread workaround), how the bot decides to respond, the channel-not-working troubleshooting checklist, and security. The ongoing `config.yaml` behavior reference (threading, mention/free-response gating, multi-workspace, per-channel prompts/skills) lives in its companion note [hermes_messaging_slack_config](hermes_messaging_slack_config.md).

The source warns that **classic Slack apps (RTM API) were fully deprecated in March 2025**. Hermes uses the modern Bolt SDK with Socket Mode; an old classic app must be re-created following the steps below.

| Component | Value |
|-----------|-------|
| **Library** | `slack-bolt` / `slack_sdk` for Python (Socket Mode) |
| **Connection** | WebSocket — no public URL required |
| **Auth tokens needed** | Bot Token (`xoxb-`) + App-Level Token (`xapp-`) |
| **User identification** | Slack Member IDs (e.g., `U01ABC2DEF3`) |

## Step 1: Create a Slack App

The fastest path is to paste a manifest Hermes generates for you. The manifest declares every built-in slash command (`/btw`, `/stop`, `/model`, …), every required OAuth scope, every event subscription, and enables Socket Mode — all at once.

**Option A — from a Hermes-generated manifest (recommended):** generate it, then create the app from it.

```bash
hermes slack manifest --write
```

This writes `~/.hermes/slack-manifest.json` and prints paste-in instructions. Then go to [https://api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From an app manifest**, pick the workspace, paste the JSON, review, **Next** → **Create**. Because the manifest already handled scopes, events, and slash commands, skip ahead to **Step 6: Install App to Workspace**.

**Option B — from scratch (manual):** go to [https://api.slack.com/apps](https://api.slack.com/apps), **Create New App** → **From scratch**, enter an app name (e.g. "Hermes Agent"), select the workspace, **Create App**. You land on **Basic Information**; continue with Steps 2–6 below.

## Step 2: Configure Bot Token Scopes

Navigate to **Features → OAuth & Permissions → Scopes → Bot Token Scopes** and add the eleven required scopes: `chat:write` (send messages), `app_mentions:read` (detect @mentions in channels), `channels:history` (read public-channel messages), `channels:read` (list/info public channels), `groups:history` (read private-channel messages the bot is invited to), `im:history` (DM history), `im:read` (basic DM info), `im:write` (open/manage DMs), `users:read` (look up users), `files:read` (read/download attached files including voice notes), and `files:write` (upload images/audio/documents). The one **optional** scope is `groups:read` (list/info private channels).

The most commonly missed scopes are `channels:history` and `groups:history` — without them the bot **will not receive messages in channels** and only works in DMs. Without `files:read`, Hermes can chat but cannot reliably read user-uploaded attachments.

## Step 3: Enable Socket Mode

Socket Mode lets the bot connect via WebSocket instead of a public URL. In the sidebar go to **Settings → Socket Mode** and toggle **Enable Socket Mode** ON. You are prompted to create an **App-Level Token**: name it anything (e.g. `hermes-socket`), add the **`connections:write`** scope, and **Generate**. Copy the token — it starts with `xapp-` and is your `SLACK_APP_TOKEN`. App-level tokens can later be found or regenerated under **Settings → Basic Information → App-Level Tokens**.

## Step 4: Subscribe to Events

This step is critical — it controls what messages the bot can see. Go to **Features → Event Subscriptions**, toggle **Enable Events** ON, expand **Subscribe to bot events**, add the four events below, and **Save Changes**.

| Event | Required? | Purpose |
|-------|-----------|---------|
| `message.im` | **Yes** | Bot receives direct messages |
| `message.channels` | **Yes** | Bot receives messages in **public** channels it's added to |
| `message.groups` | **Recommended** | Bot receives messages in **private** channels it's invited to |
| `app_mention` | **Yes** | Prevents Bolt SDK errors when bot is @mentioned |

Missing event subscriptions is the #1 setup issue: if the bot works in DMs but not in channels, `message.channels` (public) and/or `message.groups` (private) were almost certainly forgotten — Slack simply never delivers channel messages without them.

## Step 5: Enable the Messages Tab

This step enables direct messages to the bot. Without it, users see *"Sending messages to this app has been turned off"* when trying to DM the bot. Go to **Features → App Home → Show Tabs**, toggle **Messages Tab** ON, and check **"Allow users to send Slash commands and messages from the messages tab"**. Even with all correct scopes and events, Slack blocks DMs until the Messages Tab is enabled — this is a Slack platform requirement, not a Hermes config issue.

## Step 6: Install App to Workspace

Go to **Settings → Install App** → **Install to Workspace**, review the permissions, and **Allow**. After authorization a **Bot User OAuth Token** starting with `xoxb-` is shown — copy it; this is your `SLACK_BOT_TOKEN`. If scopes or event subscriptions change later, the app **must be reinstalled** for changes to take effect (the Install App page shows a prompting banner).

## Step 7: Find User IDs for the Allowlist

Hermes uses Slack **Member IDs** (not usernames or display names) for the allowlist. To find one: click the user's name/avatar → **View full profile** → the **⋮** (more) button → **Copy member ID**. Member IDs look like `U01ABC2DEF3`. At minimum you need your own Member ID.

## Step 8: Configure Hermes

Add the tokens and allowlist to `~/.hermes/.env`:

```bash
# Required
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
SLACK_ALLOWED_USERS=U01ABC2DEF3              # Comma-separated Member IDs

# Optional
SLACK_HOME_CHANNEL=C01234567890              # Default channel for cron/scheduled messages
SLACK_HOME_CHANNEL_NAME=general              # Human-readable name for the home channel (optional)
```

Alternatively run the interactive `hermes gateway setup` (select Slack when prompted). Then start the gateway:

```bash
hermes gateway              # Foreground
hermes gateway install      # Install as a user service
sudo hermes gateway install --system   # Linux only: boot-time system service
```

## Step 9: Invite the Bot to Channels

After starting the gateway, invite the bot to any channel where it should respond — it will **not** auto-join, and must be invited to each channel individually:

```
/invite @Hermes Agent
```

## Slash Commands

Every Hermes command (`/btw`, `/stop`, `/new`, `/model`, `/help`, …) is a native Slack slash command — exactly the way they work on Telegram and Discord. Typing `/` in Slack lists every Hermes command in the autocomplete picker. Under the hood, the generated manifest (Step 1, Option A) declares every command in `COMMAND_REGISTRY` as a slash command; in Socket Mode, Slack routes the command event through the WebSocket regardless of the manifest's `url` field. When Hermes adds new commands (e.g. after `hermes update`), regenerate `~/.hermes/slack-manifest.json` with `hermes slack manifest --write`, then in Slack paste the new contents into **Features → App Manifest → Edit** → **Save** (reinstalling if scopes/commands changed). For backward compatibility, `/hermes btw run the tests` is still routed identically to `/btw run the tests`, and free-form `/hermes what's the weather?` is treated as a regular message.

**Using commands inside threads (the `!cmd` prefix):** Slack itself blocks native slash commands inside thread replies — `/queue` in a thread returns *"/queue is not supported in threads. Sorry!"* and there is no app-side setting to re-enable it. As a workaround, Hermes recognises a leading `!` as an alternate command prefix that works in threads (and anywhere): type `!queue`, `!stop`, `!model gpt-5.4`, etc. as a regular thread reply and Hermes treats it identically to the slash form, replying in the same thread. Only the first token is checked against the known command list, so casual messages like `!nice work` pass through to the agent unchanged. When interactive approval buttons (dangerous-command / `execute_code` approval) cannot be delivered and Hermes falls back to a text prompt, the prompt instructs replying with `!approve` / `!deny` — the forms that work inside threads.

To emit just the slash-commands array for a hand-maintained manifest:

```bash
hermes slack manifest --slashes-only > /tmp/slashes.json
```

Paste that array into the `features.slash_commands` key of the existing manifest.

## How the Bot Responds

| Context | Behavior |
|---------|----------|
| **DMs** | Bot responds to every message — no @mention needed |
| **Channels** | Bot **only responds when @mentioned** (e.g. `@Hermes Agent what time is it?`). In channels, Hermes replies in a thread attached to that message. |
| **Threads** | An @mention inside an existing thread replies in that same thread. Once the bot has an active session in a thread, **subsequent replies in that thread do not require @mention** — the bot follows the conversation naturally. |

In channels, always @mention the bot to start a conversation; outside of threads, messages without @mention are ignored to prevent noise in busy channels. (The full mention/strict-mention/free-response gating knobs are in [hermes_messaging_slack_config](hermes_messaging_slack_config.md).)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Bot doesn't respond to DMs | Verify `message.im` is subscribed and the app is reinstalled |
| Bot works in DMs but not in channels | **Most common issue.** Add `message.channels` and `message.groups`, reinstall the app, and `/invite @Hermes Agent` |
| No response to @mentions in channels | 1) Check `message.channels` is subscribed. 2) Bot must be invited. 3) Ensure `channels:history` scope. 4) Reinstall after scope/event changes |
| Ignores private-channel messages | Add the `message.groups` event + `groups:history` scope, reinstall, and `/invite` the bot |
| "Sending messages to this app has been turned off" in DMs | Enable the **Messages Tab** in App Home (Step 5) |
| "not_authed" / "invalid_auth" errors | Regenerate Bot Token and App Token, update `.env` |
| Bot responds but can't post in a channel | `/invite @Hermes Agent` to the channel |
| Can chat but can't read uploaded images/files | Add `files:read`, then **reinstall**; Hermes surfaces attachment-access diagnostics in-chat on scope/auth failures |
| `missing_scope` error | Add the scope in OAuth & Permissions, then **reinstall** |
| Socket disconnects frequently | Check network; Bolt auto-reconnects but unstable connections cause lag |
| Changed scopes/events but nothing changed | You **must reinstall** the app after any scope/event change |

**Quick Checklist** — if the bot isn't working in channels, verify all eight: (1) `message.channels` subscribed (public), (2) `message.groups` subscribed (private), (3) `app_mention` subscribed, (4) `channels:history` scope added (public), (5) `groups:history` scope added (private), (6) app **reinstalled** after adding scopes/events, (7) bot **invited** to the channel (`/invite @Hermes Agent`), (8) you are **@mentioning** the bot.

## Security

**Always set `SLACK_ALLOWED_USERS`** with the Member IDs of authorized users — without it the gateway **denies all messages by default** as a safety measure. Never share bot tokens; treat them like passwords. Additional guidance: store tokens in `~/.hermes/.env` (file permissions `600`); rotate tokens periodically via Slack app settings; audit who has access to the Hermes config directory; and note that Socket Mode exposes no public endpoint, which is one less attack surface.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/slack.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack
**Last Updated**: 2026-06-19
**Status**: Active
