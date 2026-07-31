---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - discord
keywords:
  - openclaw discord setup
  - discord bot token intents
  - discord developer portal application
  - oauth2 invite applications.commands
  - discord dm pairing approve
  - guild allowlist workspace
  - DISCORD_BOT_TOKEN secretref
  - openclaw config patch discord
topics:
  - OpenClaw
  - Discord Channel Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/discord
access_control_group: ["general"]
---

# OpenClaw — Connecting Discord: Bot Setup and Guild Workspace

## Overview

This note is the connect-and-pair procedure for the OpenClaw Discord channel, mirroring the **Quick setup** and **Recommended: Set up a guild workspace** sections of the `channels/discord` source page. It covers creating a Discord application + bot in the Developer Portal, enabling the privileged gateway intents Discord requires, copying the bot token, generating an OAuth2 invite URL with the right scopes/permissions, collecting your Server ID and User ID, securely setting `DISCORD_BOT_TOKEN` and patching the gateway config, approving the first DM pairing code, and then promoting the server to a full guild workspace (guild allowlist, responding without an `@mention`, and the MEMORY.md-in-channels caveat). Discord is ready for DMs and guild channels via the official Discord gateway; DMs default to pairing mode. Routing/access-control depth, feature/components reference, voice, and ops/config-reference are covered by the sibling notes linked below — this note stays scoped to first-connection setup.

## Quick setup

You will need to create a new application with a bot, add the bot to your server, and pair it to OpenClaw. OpenClaw recommends adding your bot to your own private server (in Discord, **Create My Own > For me and my friends**). The setup is an 8-step flow.

### 1. Create a Discord application and bot

Go to the Discord Developer Portal and click **New Application**. Name it something like "OpenClaw". Click **Bot** on the sidebar and set the **Username** to whatever you call your OpenClaw agent.

### 2. Enable privileged intents

Still on the **Bot** page, scroll down to **Privileged Gateway Intents** and enable:

- **Message Content Intent** (required)
- **Server Members Intent** (recommended; required for role allowlists and name-to-ID matching)
- **Presence Intent** (optional; only needed for presence updates)

### 3. Copy your bot token

On the **Bot** page click **Reset Token**. Despite the name, this generates your first token — nothing is being "reset." Copy the token and save it; this is your **Bot Token** and you will need it shortly.

### 4. Generate an invite URL and add the bot to your server

Click **OAuth2** on the sidebar, then scroll to **OAuth2 URL Generator** and enable the `bot` and `applications.commands` scopes. A **Bot Permissions** section appears below; enable at least:

- **General Permissions** — View Channels
- **Text Permissions** — Send Messages, Read Message History, Embed Links, Attach Files, Add Reactions (optional)

This is the baseline set for normal text channels. If you plan to post in Discord threads — including forum or media channel workflows that create or continue a thread — also enable **Send Messages in Threads**. Copy the generated URL at the bottom, paste it into your browser, select your server, and click **Continue** to connect; the bot should now appear in the server.

### 5. Enable Developer Mode and collect your IDs

Enable Developer Mode to copy internal IDs: **User Settings** (gear icon) → **Advanced** → toggle **Developer Mode**. Then right-click your **server icon** → **Copy Server ID**, and right-click your **own avatar** → **Copy User ID**. Save the **Server ID** and **User ID** alongside the Bot Token — all three go to OpenClaw in the next step.

### 6. Allow DMs from server members

For pairing to work, Discord must allow the bot to DM you. Right-click your **server icon** → **Privacy Settings** → toggle on **Direct Messages**. This lets server members (including bots) DM you. Keep it enabled to use Discord DMs with OpenClaw; if you only plan to use guild channels, you can disable DMs after pairing.

### 7. Set the bot token securely and patch the gateway

The Discord bot token is a secret (like a password); set it on the machine running OpenClaw before messaging your agent. The source uses an env-sourced SecretRef and a config patch:

```bash
export DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN"
cat > discord.patch.json5 <<'JSON5'
{
  channels: {
    discord: {
      enabled: true,
      token: { source: "env", provider: "default", id: "DISCORD_BOT_TOKEN" },
    },
  },
}
JSON5
openclaw config patch --file ./discord.patch.json5 --dry-run
openclaw config patch --file ./discord.patch.json5
openclaw gateway
```

If OpenClaw is already running as a background service, restart it via the OpenClaw Mac app or by stopping and restarting the `openclaw gateway run` process. For managed service installs, run `openclaw gateway install` from a shell where `DISCORD_BOT_TOKEN` is present, or store the variable in `~/.openclaw/.env`, so the service can resolve the env SecretRef after restart. If your host is blocked or rate-limited by Discord's startup application lookup, set the Discord application/client ID from the Developer Portal so startup can skip that REST call: use `channels.discord.applicationId` for the default account, or `channels.discord.accounts.<accountId>.applicationId` when you run multiple Discord bots.

### 8. Configure OpenClaw and pair

You can finish setup by asking your agent on an existing channel (e.g. Telegram) — *"I already set my Discord bot token in config. Please finish Discord setup with User ID `<user_id>` and Server ID `<server_id>`."* — or via file-based config. The base CLI/config block enables Discord and resolves the token from env:

```json5
{
  channels: {
    discord: {
      enabled: true,
      token: {
        source: "env",
        provider: "default",
        id: "DISCORD_BOT_TOKEN",
      },
    },
  },
}
```

Env fallback for the default account is `DISCORD_BOT_TOKEN=...`. For scripted or remote setup, write the same JSON5 block with `openclaw config patch --file ./discord.patch.json5 --dry-run` and then rerun without `--dry-run`. Plaintext `token` values are supported; SecretRef values are also supported for `channels.discord.token` across env/file/exec providers (see Secrets Management). For multiple Discord bots, keep each bot token and application ID under its account — a top-level `channels.discord.applicationId` is inherited by accounts, so only set it there when every account should use the same application ID:

```json5
{
  channels: {
    discord: {
      enabled: true,
      accounts: {
        personal: {
          token: { source: "env", provider: "default", id: "DISCORD_PERSONAL_TOKEN" },
          applicationId: "111111111111111111",
        },
        work: {
          token: { source: "env", provider: "default", id: "DISCORD_WORK_TOKEN" },
          applicationId: "222222222222222222",
        },
      },
    },
  },
}
```

### Approve the first DM pairing

Wait until the gateway is running, then DM your bot in Discord; it responds with a pairing code. Either tell your agent on an existing channel — *"Approve this Discord pairing code: `<CODE>`"* — or use the CLI:

```bash
openclaw pairing list discord
openclaw pairing approve discord <CODE>
```

Pairing codes expire after 1 hour. After approval you can chat with your agent in Discord via DM.

### Token resolution notes

Token resolution is account-aware: config token values win over env fallback, and `DISCORD_BOT_TOKEN` is only used for the default account. If two enabled Discord accounts resolve to the same bot token, OpenClaw starts only one gateway monitor for that token — a config-sourced token wins over the default env fallback; otherwise the first enabled account wins and the duplicate account is reported disabled. For advanced outbound calls (message tool/channel actions), an explicit per-call `token` is used for that call; this applies to send and read/probe-style actions (read/search/fetch/thread/pins/permissions), while account policy/retry settings still come from the selected account in the active runtime snapshot.

## Recommended: Set up a guild workspace

Once DMs are working, you can set up your Discord server as a full workspace where each channel gets its own agent session with its own context. This is recommended for private servers where it is just you and your bot. The flow is three steps.

### 1. Add your server to the guild allowlist

This enables your agent to respond in any channel on your server, not just DMs. Ask your agent (*"Add my Discord Server ID `<server_id>` to the guild allowlist"*) or set config:

```json5
{
  channels: {
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        YOUR_SERVER_ID: {
          requireMention: true,
          users: ["YOUR_USER_ID"],
        },
      },
    },
  },
}
```

### 2. Allow responses without @mention

By default the agent only responds in guild channels when `@mentioned`; for a private server you probably want it to respond to every message. In guild channels, normal replies post automatically by default. For shared always-on rooms, opt into `messages.groupChat.visibleReplies: "message_tool"` so the agent can lurk and only post when it decides a channel reply is useful — this works best with latest-generation, tool-reliable models such as GPT 5.5, and ambient room events stay quiet unless the tool sends (see the ambient-room-events sibling note for the full lurk-mode config). If Discord shows typing and the logs show token usage but no posted message, check whether the turn was configured as an ambient room event or opted into message-tool visible replies. To respond without a mention, set `requireMention: false` in your guild config:

```json5
{
  channels: {
    discord: {
      guilds: {
        YOUR_SERVER_ID: {
          requireMention: false,
        },
      },
    },
  },
}
```

To require message-tool sends for visible group/channel replies, set `messages.groupChat.visibleReplies: "message_tool"`.

### 3. Plan for memory in guild channels

By default, long-term memory (`MEMORY.md`) only loads in DM sessions; guild channels do not auto-load `MEMORY.md`. Either instruct the agent to fetch on demand (*"When I ask questions in Discord channels, use memory_search or memory_get if you need long-term context from MEMORY.md."*) or, for shared context in every channel, put stable instructions in `AGENTS.md` or `USER.md` (they are injected for every session) and keep long-term notes in `MEMORY.md`, accessed on demand with memory tools. Now create channels on your Discord server and start chatting: the agent can see the channel name, and each channel gets its own isolated session — so you can set up `#coding`, `#home`, `#research`, or whatever fits your workflow.

**Source**: OpenClaw documentation — `channels/discord` (mirror `inbox/openclaw_docs/channels/discord.md`, Quick setup + Recommended: Set up a guild workspace sections)
**Last Updated**: 2026-06-22
**Status**: Active
