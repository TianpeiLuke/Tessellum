---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - railway
keywords:
  - openclaw railway deploy
  - railway one-click template
  - openclaw control ui
  - railway http proxy 8080
  - railway volume /data
  - openclaw_gateway_token
  - openclaw_gateway_port
  - openclaw backup create
topics:
  - OpenClaw
  - Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/railway
access_control_group: ["general"]
---

# OpenClaw — Deploy on Railway (One-Click Template)

## Overview

This note is the procedure for deploying OpenClaw on **Railway** using its one-click template and reaching the hosted Gateway through the browser-based Control UI — mirroring the `install/railway` source page. It is the easiest "no terminal on the server" path: Railway runs the Gateway for you. The procedure covers the quick checklist, the one-click deploy + finding the public URL, what the deployment provides, the three required Railway settings (Public Networking HTTP Proxy on port `8080`, a `/data` Volume, and the `OPENCLAW_*` Variables), connecting a messaging channel, taking a portable backup, and the documented next steps. All commands, ports, and environment variables are reproduced verbatim from the source page.

## Quick checklist (new users)

The fastest end-to-end path, in order:

1. Click **Deploy on Railway** (the one-click template, below).
2. Add a **Volume** mounted at `/data`.
3. Set the required **Variables** (at least `OPENCLAW_GATEWAY_PORT` and `OPENCLAW_GATEWAY_TOKEN`).
4. Enable **HTTP Proxy** on port `8080`.
5. Open `https://<your-railway-domain>/openclaw` and connect using the configured shared secret. This template uses `OPENCLAW_GATEWAY_TOKEN` by default; if you replace it with password auth, use that password instead.

## One-click deploy

Deploy from the Railway template at `https://railway.com/deploy/clawdbot-railway-template` (the page's **Deploy on Railway** button). After deploy, find your public URL in **Railway → your service → Settings → Domains**. Railway will either give you a generated domain (often `https://<something>.up.railway.app`) or use your custom domain if you attached one. Then open `https://<your-railway-domain>/openclaw` — the Control UI.

## What you get

The deployment provides a hosted OpenClaw Gateway plus Control UI, and persistent storage via the Railway Volume (`/data`) so that `openclaw.json`, per-agent `auth-profiles.json`, channel/provider state, sessions, and workspace survive redeploys. The `/data` Volume is the load-bearing piece: without it, a Railway redeploy would reset all of that state.

## Required Railway settings

Three settings on the service are required for a working deployment.

### Public Networking

Enable **HTTP Proxy** for the service.

- Port: `8080`

### Volume (required)

Attach a volume mounted at:

- `/data`

### Variables

Set these variables on the service:

- `OPENCLAW_GATEWAY_PORT=8080` (required — must match the port in Public Networking)
- `OPENCLAW_GATEWAY_TOKEN` (required; treat as an admin secret)
- `OPENCLAW_STATE_DIR=/data/.openclaw` (recommended)
- `OPENCLAW_WORKSPACE_DIR=/data/workspace` (recommended)

The two recommended state/workspace variables point OpenClaw's state and workspace into the attached `/data` Volume so they persist; `OPENCLAW_GATEWAY_PORT` must match the port enabled in Public Networking (`8080`).

## Connect a channel

Use the Control UI at `/openclaw` or run `openclaw onboard` via Railway's shell for channel setup instructions. The source page links the channel docs for Telegram (`/channels/telegram`, fastest — just a bot token), Discord (`/channels/discord`), and all channels (`/channels`). Channel setup detail lives in the `/channels/*` docs and is not duplicated here.

## Backups & migration

Export your state, config, auth profiles, and workspace:

```bash
openclaw backup create
```

This creates a portable backup archive with OpenClaw state plus any configured workspace. See the `/cli/backup` doc for details.

## Next steps

The source page closes with three follow-ups:

- Set up messaging channels — `/channels`.
- Configure the Gateway — `/gateway/configuration`.
- Keep OpenClaw up to date — `/install/updating`.

**Source**: OpenClaw documentation — `install/railway` (mirror `inbox/openclaw_docs/install/railway.md`)
**Last Updated**: 2026-06-22
**Status**: Active
