---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - messaging
keywords:
  - team telegram assistant
  - botfather bot setup
  - gateway dm pairing
  - per-user authorization allowlist
  - docker terminal backend
  - soul.md agents.md context
topics:
  - Hermes Agent
  - Messaging Gateway
  - Automation & Bots
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/team-telegram-assistant
access_control_group: ["general"]
---

# Set Up a Team Telegram Assistant

## Overview

This is the end-to-end recipe for standing up a **multi-user Telegram bot** powered by Hermes Agent that a whole team shares for code help, research, system administration, and debugging. The result is a single AI assistant any authorized teammate can DM, running on a server or VPS (not a laptop — the bot must stay up) with full tool access (terminal, file editing, web search, code execution), **per-user sessions** so each person keeps their own conversation context, and **per-user authorization** so only approved people can interact. The procedure composes already-documented primitives — the messaging gateway, DM pairing, scheduled cron tasks, and context files — so most of the depth lives in those feature references; this guide is the assembly sequence: create the bot with BotFather, configure the gateway (wizard or `.env`), install it as a persistent service, authorize teammates (static allowlist vs DM pairing), tune the bot (home channel, tool-progress, SOUL.md/AGENTS.md), schedule team tasks, and harden it with a Docker terminal backend. Prerequisites: Hermes installed on a server, a Telegram account, and an LLM-provider API key in `~/.hermes/.env` (a $5/month VPS is plenty — the LLM API calls are the cost, and they happen remotely).

## Step 1: Create a Telegram Bot

Every Telegram bot starts with **@BotFather**, Telegram's official bot for creating bots. Open Telegram, search `@BotFather`, and send `/newbot`; BotFather asks for a **display name** (what users see, e.g. `Team Hermes Assistant`) and a **username** that must end in `bot` (e.g. `myteam_hermes_bot`). It then replies with the bot token — a string like `7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...` — which you save for the next step. Optionally set a description with `/setdescription` and a slash-command menu with `/setcommands` (commands such as `new`, `model`, `status`, `help`, `stop`). The token is a secret: anyone holding it can control the bot, so if it leaks, use `/revoke` in BotFather to rotate it.

## Step 2: Configure the Gateway

Two paths. **Option A (recommended)** is the interactive wizard, which walks through everything with arrow-key selection — pick **Telegram**, paste the bot token, and enter your user ID:

```bash
hermes gateway setup
```

**Option B** is manual configuration in `~/.hermes/.env` — the bot token plus your numeric Telegram user ID as the initial allowlist:

```bash
# Telegram bot token from BotFather
TELEGRAM_BOT_TOKEN=7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...

# Your Telegram user ID (numeric)
TELEGRAM_ALLOWED_USERS=123456789
```

The Telegram **user ID** is a permanent numeric value (like `123456789`), distinct from your `@username` (which can change) — always use the numeric ID for allowlists. To find it, message [@userinfobot](https://t.me/userinfobot), which instantly replies with your numeric ID.

## Step 3: Start the Gateway

Run the gateway in the foreground first to confirm it works (`hermes gateway`); on success you see the Telegram adapter connect and the cron scheduler start its 60s tick. Send the bot a message — if it replies, you're set — then `Ctrl+C` to stop. For a persistent deployment that survives reboots, install it as a background service:

```bash
hermes gateway install
sudo hermes gateway install --system   # Linux only: boot-time system service
```

This creates a user-level **systemd** service on Linux by default, a **launchd** service on macOS, or a boot-time Linux system service with `--system`. Manage it with `hermes gateway start|stop|status`; tail logs with `journalctl --user -u hermes-gateway -f` (Linux) or `tail -f ~/.hermes/logs/gateway.log` (macOS). Critically, run `sudo loginctl enable-linger $USER` so the user service keeps running after SSH logout. On macOS the launchd plist captures the shell PATH at install time so gateway subprocesses can find tools like Node.js and ffmpeg — re-run `hermes gateway install` after installing new tools. Verify with `hermes gateway status` and a test message.

## Step 4: Set Up Team Access

Two authorization approaches. **Approach A — static allowlist**: collect each teammate's numeric Telegram user ID (have them message [@userinfobot](https://t.me/userinfobot)) and set them as a comma-separated `TELEGRAM_ALLOWED_USERS=123456789,987654321,555555555` in `~/.hermes/.env`, then restart with `hermes gateway stop && hermes gateway start`.

**Approach B — DM pairing (recommended for teams)** avoids collecting IDs upfront. When a not-yet-authorized teammate DMs the bot, it replies with a one-time pairing code; the teammate sends you the code (Slack, email, in person) and you approve it on the server, after which the bot responds to them immediately:

```bash
hermes pairing approve telegram XKGH5N7P   # approve a code

hermes pairing list                        # see pending + approved users
hermes pairing revoke telegram 987654321   # revoke access
hermes pairing clear-pending               # clear expired pending codes
```

Pairing's advantage is that approvals take effect without a gateway restart. **Security considerations**: never set `GATEWAY_ALLOW_ALL_USERS=true` on a bot with terminal access (anyone who finds the bot could run commands on your server); pairing codes expire after **1 hour** and use cryptographic randomness; rate limiting throttles brute-force (1 request per user per 10 minutes, max 3 pending codes per platform); after 5 failed approval attempts the platform enters a 1-hour lockout; and all pairing data is stored with `chmod 0600`.

## Step 5: Configure the Bot

A **home channel** is where the bot delivers cron-job results and proactive messages — without one, scheduled tasks have nowhere to send output. Set it with the `/sethome` command in any group/chat where the bot is a member, or manually via `TELEGRAM_HOME_CHANNEL` / `TELEGRAM_HOME_CHANNEL_NAME` in `.env` (add [@userinfobot](https://t.me/userinfobot) to a group to learn its chat ID). **Tool-progress display** controls how much tool activity the bot shows, in `~/.hermes/config.yaml`:

```yaml
display:
  tool_progress: new    # off | new | all | verbose
```

`off` shows clean responses only; `new` shows a brief status per new tool call (recommended for messaging); `all` shows every tool call with details; `verbose` shows full tool output including command results. Users can change this per-session with `/verbose`. **Personality** is set by editing `~/.hermes/SOUL.md` (e.g. "be concise and technical, use code blocks, skip pleasantries, ask for error logs before guessing" — a dedicated Use SOUL.md with Hermes guide covers it in full). **Project context** goes in `~/.hermes/AGENTS.md` (stack, CI/CD, deploy target, testing conventions). Context files are injected into every session's system prompt, so keep them concise — every character counts against the token budget.

## Step 6: Set Up Scheduled Tasks

With the gateway running, schedule recurring tasks that deliver to the team channel by messaging the bot in natural language — the agent creates a cron job automatically and delivers results to the chat where you asked (or the home channel). Two examples: a **daily standup** ("Every weekday at 9am, check `github.com/myorg/myproject` for PRs opened/merged in the last 24h, issues created/closed, and CI failures on main; format as a brief standup summary") and a **server health check** ("Every 6 hours, check disk with `df -h`, memory with `free -h`, and container status with `docker ps`; report partitions above 80%, restarted containers, or high memory"). Manage jobs from the CLI (`hermes cron list`, `hermes cron status`) or from chat (`/cron list`, `/cron remove <job_id>`). Cron prompts run in **completely fresh sessions** with no memory of prior conversations — each prompt must carry all needed context (file paths, URLs, server addresses, clear instructions).

## Production Tips

On a shared team bot, **use Docker as the terminal backend** so agent commands run in a container instead of on the host — even a destructive request leaves the host protected:

```bash
# In ~/.hermes/.env
TERMINAL_BACKEND=docker
TERMINAL_DOCKER_IMAGE=nikolaik/python-nodejs:python3.11-nodejs20
```

Equivalently in `~/.hermes/config.yaml`, the `terminal` block sets `backend: docker` plus `container_cpu`, `container_memory`, and `container_persistent`. **Monitor** with `hermes gateway status` and live logs (`journalctl --user -u hermes-gateway -f` on Linux, `tail -f ~/.hermes/logs/gateway.log` on macOS). **Keep Hermes updated** by sending `/update` to the bot (it pulls and restarts) or running `hermes update && hermes gateway stop && hermes gateway start` on the server. **Log locations**: gateway logs via journalctl/`~/.hermes/logs/gateway.log`; cron output under `~/.hermes/cron/output/{job_id}/{timestamp}.md`; cron definitions in `~/.hermes/cron/jobs.json`; pairing data in `~/.hermes/pairing/`; session history in `~/.hermes/sessions/`. **Going further**: the security guide, full messaging-gateway reference, Telegram platform details, advanced cron, context files, personality presets, and adding Discord/Slack/WhatsApp on the same gateway.

**Source**: `inbox/hermes_agent_docs/guides/team-telegram-assistant.md` · https://hermes-agent.nousresearch.com/docs/guides/team-telegram-assistant
**Last Updated**: 2026-06-19
**Status**: Active
