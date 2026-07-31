---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - hostinger
keywords:
  - openclaw hostinger
  - 1-click openclaw managed
  - openclaw on vps docker manager
  - ready-to-use ai credits
  - hpanel docker manager
  - gateway token whatsapp telegram
  - openclaw dashboard hpanel
  - telegram pairing code
topics:
  - OpenClaw
  - Install
  - Hostinger
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/hostinger
access_control_group: ["general"]
---

# OpenClaw — Hosting on Hostinger (1-Click and VPS)

## Overview

This note is the procedure for running a persistent OpenClaw Gateway on Hostinger, mirroring the `install/hostinger` source page. Hostinger offers two deployment paths: **Option A — 1-Click OpenClaw**, a fully managed deployment where Hostinger handles infrastructure, Docker, and automatic updates; and **Option B — OpenClaw on VPS**, where Hostinger deploys OpenClaw via Docker on your VPS and you manage it through the **Docker Manager** in hPanel. Both paths take roughly 5-10 minutes, let you connect a messaging channel (WhatsApp or Telegram), and finish by accessing the OpenClaw dashboard from hPanel. The page also covers verifying the setup, common troubleshooting, and next steps. This note covers the Prerequisites, both deployment options, Verify, Troubleshooting, and the Next-steps / Related link-outs.

## Prerequisites

- A Hostinger account ([signup](https://www.hostinger.com/openclaw)).
- About 5-10 minutes.

## Option A: 1-Click OpenClaw

This is the fastest way to get started; Hostinger handles infrastructure, Docker, and automatic updates. The flow has three steps.

### Step 1 — Purchase and launch

From the [Hostinger OpenClaw page](https://www.hostinger.com/openclaw), choose a **Managed OpenClaw** plan and complete checkout. During checkout you can select **Ready-to-Use AI** credits — these are pre-purchased and integrated instantly inside OpenClaw, so no external accounts or API keys from other providers are needed and you can start chatting right away. Alternatively, you can provide your own key from **Anthropic, OpenAI, Google Gemini, or xAI** during setup.

### Step 2 — Select a messaging channel

Choose one or more channels to connect:

- **WhatsApp** — scan the QR code shown in the setup wizard.
- **Telegram** — paste the bot token from [BotFather](https://t.me/BotFather).

### Step 3 — Complete installation

Click **Finish** to deploy the instance. Once ready, access the OpenClaw dashboard from **OpenClaw Overview** in hPanel.

## Option B: OpenClaw on VPS

This path gives you more control over your server. Hostinger deploys OpenClaw via Docker on your VPS, and you manage it through the **Docker Manager** in hPanel. The flow has three steps.

### Step 1 — Purchase a VPS

From the [Hostinger OpenClaw page](https://www.hostinger.com/openclaw), choose an **OpenClaw on VPS** plan and complete checkout. As with Option A, you can select **Ready-to-Use AI** credits during checkout — pre-purchased and integrated instantly inside OpenClaw — so you can start chatting without any external accounts or API keys from other providers.

### Step 2 — Configure OpenClaw

Once the VPS is provisioned, fill in the configuration fields:

- **Gateway token** — auto-generated; save it for later use.
- **WhatsApp number** — your number with country code (optional).
- **Telegram bot token** — from [BotFather](https://t.me/BotFather) (optional).
- **API keys** — only needed if you did not select Ready-to-Use AI credits during checkout.

### Step 3 — Start OpenClaw

Click **Deploy**. Once running, open the OpenClaw dashboard from hPanel by clicking on **Open**.

### Managing the VPS container (logs, restarts, updates)

Logs, restarts, and updates are managed directly from the **Docker Manager** interface in hPanel. To update, press on **Update** in Docker Manager, which pulls the latest image.

## Verify your setup

Send "Hi" to your assistant on the channel you connected. OpenClaw will reply and walk you through initial preferences.

## Troubleshooting

- **Dashboard not loading** — wait a few minutes for the container to finish provisioning, then check the Docker Manager logs in hPanel.
- **Docker container keeps restarting** — open the Docker Manager logs and look for configuration errors (missing tokens, invalid API keys).
- **Telegram bot not responding** — send your pairing code message from Telegram directly as a message inside your OpenClaw chat to complete the connection.

## Next steps

- [Channels](https://docs.openclaw.ai/channels) — connect Telegram, WhatsApp, Discord, and more (owned by the Channels docs).
- [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) — all config options (owned by the Gateway docs).

The Install-overview, VPS, and DigitalOcean pages are related deployment paths (see References / sibling Install notes below).

**Source**: OpenClaw documentation — `install/hostinger` (mirror `inbox/openclaw_docs/install/hostinger.md`)
**Last Updated**: 2026-06-22
**Status**: Active
