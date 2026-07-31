---
tags:
  - resource
  - documentation
  - claude_code
  - channels
  - setup
keywords:
  - install a channel
  - plugin install
  - --channels flag
  - telegram discord imessage
  - bot token pairing
  - fakechat quickstart
  - bun runtime
  - sender allowlist
topics:
  - Claude Code
  - Channels
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/channels
access_control_group: ["general"]
---

# Install and Run a Channel

## Overview

A **channel** is an MCP server that pushes events into a running Claude Code session. This note is the install-and-run procedure for the channels shipped with the research preview: the three real platform plugins (**Telegram**, **Discord**, **iMessage**) and **fakechat**, a localhost demo with nothing to authenticate. Every channel is distributed as a plugin, requires the [Bun](https://bun.sh) runtime, and is started for the session with the `--channels` flag (being installed is not enough — see [Security and Enterprise Controls](cc_channels_security_and_enterprise_controls.md)).

The general flow is the same across platforms: create platform credentials (a bot token, for Telegram and Discord) or grant local access (Full Disk Access, for iMessage), `/plugin install` the channel, restart Claude Code with `--channels`, then pair your account so only you can push messages. The conceptual model these steps configure is covered in [Channels Overview](cc_channels_overview.md); the build-your-own contract is in [Build a Channel](cc_build_a_channel.md).

## Prerequisites

- Claude Code [installed and authenticated](https://code.claude.com/docs/en/quickstart) with a claude.ai account or a Claude Console API key. Channels require Claude Code v2.1.80 or later and Anthropic authentication (not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry).
- **Bun** installed — the pre-built channel plugins are Bun scripts. Check with `bun --version`; if that fails, [install Bun](https://bun.sh/docs/installation).
- **Team, Enterprise, or managed Console org**: your admin must [enable channels](cc_channels_security_and_enterprise_controls.md) in managed settings first.

## Common pattern: install, enable, pair

Each supported channel is a plugin from the `claude-plugins-official` marketplace. The procedure follows four moves; the per-platform specifics vary only in credential creation and pairing.

1. **Install the plugin** with `/plugin install <name>@claude-plugins-official`. If Claude Code reports the plugin is not found in any marketplace, the marketplace is missing or outdated — run `/plugin marketplace update claude-plugins-official` to refresh it, or `/plugin marketplace add anthropics/claude-plugins-official` if you have not added it before, then retry. (Plugin and marketplace mechanics are owned by the [plugins](https://code.claude.com/docs/en/plugins) and [plugin-marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) docs.) For Telegram and Discord, run `/reload-plugins` after installing to activate the plugin's configure command.
2. **Enable it for the session** by exiting and restarting Claude Code with the channel flag, naming the installed plugin:

   ```bash
   claude --channels plugin:telegram@claude-plugins-official
   ```

   You can pass several plugins to `--channels`, space-separated.
3. **Configure credentials** (Telegram/Discord) with the platform's configure command.
4. **Pair your account** so only your sender ID can push messages.

## Telegram and Discord

Telegram and Discord both run a bot that polls the platform's API for messages. The difference is in how you obtain the token and provision the bot.

**Create the bot and get a token.** For **Telegram**, open [BotFather](https://t.me/BotFather), send `/newbot`, give it a display name and a unique username ending in `bot`, and copy the returned token. For **Discord**, go to the [Discord Developer Portal](https://discord.com/developers/applications), create a **New Application**, create a bot username in the **Bot** section, click **Reset Token** and copy it; additionally enable **Message Content Intent** under **Privileged Gateway Intents**, then under **OAuth2 > URL Generator** select the `bot` scope with View Channels, Send Messages, Send Messages in Threads, Read Message History, Attach Files, and Add Reactions, and open the generated URL to add the bot to your server.

**Configure the token** after install + `/reload-plugins`, running the plugin's configure command with the token you copied:

```
/telegram:configure <token>
```

This saves the token to `~/.claude/channels/telegram/.env` (Discord saves to `~/.claude/channels/discord/.env` via `/discord:configure <token>`). You can also set `TELEGRAM_BOT_TOKEN` / `DISCORD_BOT_TOKEN` in your shell environment before launching Claude Code.

**Restart with channels enabled** so the plugin starts polling: `claude --channels plugin:telegram@claude-plugins-official` (substitute `discord` for Discord).

**Pair your account.** Send any message to your bot (Telegram) or DM it (Discord); the bot replies with a pairing code. If the bot does not respond, confirm Claude Code is running with `--channels` from the previous step — the bot can only reply while the channel is active. Back in Claude Code, approve the code and lock down access so only your account can send:

```
/telegram:access pair <code>
/telegram:access policy allowlist
```

(Discord uses `/discord:access pair <code>` and `/discord:access policy allowlist`.)

## iMessage

The iMessage channel works differently: it reads your Messages database at `~/Library/Messages/chat.db` directly and sends replies through AppleScript. It requires macOS and needs no bot token or external service.

- **Grant Full Disk Access.** The Messages database is protected by macOS. The first time the server reads it, macOS prompts for access — click **Allow**. The prompt names whichever app launched Bun (Terminal, iTerm, or your IDE). If the prompt does not appear or you clicked Don't Allow, grant access manually under **System Settings > Privacy & Security > Full Disk Access** and add your terminal. Without this, the server exits immediately with `authorization denied`.
- **Install and restart.** `/plugin install imessage@claude-plugins-official` (no `/reload-plugins` step listed for iMessage), then restart with `claude --channels plugin:imessage@claude-plugins-official`.
- **Text yourself.** Send a message to yourself from any device signed into your Apple ID; it reaches Claude immediately — self-chat bypasses access control with no setup. The first reply Claude sends triggers a macOS Automation prompt asking if your terminal can control Messages; click **OK**.
- **Allow other senders.** By default only your own messages pass through. To let another contact reach Claude, add their handle (phone numbers in `+country` format, or Apple ID emails):

  ```
  /imessage:access allow +15551234567
  ```

## Quickstart: fakechat

Fakechat is an officially supported demo channel that runs a chat UI on localhost — nothing to authenticate, no external service to configure. Once installed and enabled, you type in the browser, the message arrives in your Claude Code session, Claude replies, and the reply shows up back in the browser. It is the recommended first run before connecting a real platform.

1. **Install the fakechat channel plugin** (same marketplace-recovery note as above applies if not found):

   ```text
   /plugin install fakechat@claude-plugins-official
   ```

2. **Restart with the channel enabled**, passing the installed plugin. The fakechat server starts automatically:

   ```bash
   claude --channels plugin:fakechat@claude-plugins-official
   ```

3. **Push a message in.** Open the fakechat UI at `http://localhost:8787` and type a message. It arrives in your session as a `<channel source="fakechat">` event; Claude reads it, does the work, calls fakechat's `reply` tool, and the answer shows up in the chat UI.

## Permission prompts while away

If Claude hits a permission prompt while you are away from the terminal, the session pauses until you respond. Channel servers that declare the [permission relay capability](cc_channel_permission_relay.md) can forward these prompts so you can approve or deny remotely. For unattended use, [`--dangerously-skip-permissions`](https://code.claude.com/docs/en/permission-modes) bypasses prompts other than explicit ask rules — only use it in environments you trust. When you run channels in non-interactive mode with `-p` (see [headless mode](https://code.claude.com/docs/en/headless)), tools that need terminal input (multiple-choice questions, plan-mode approval) are disabled so the session never stalls.

**Source**: https://code.claude.com/docs/en/channels
**Last Updated**: 2026-06-13
**Status**: Active
