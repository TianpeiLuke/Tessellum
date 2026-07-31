---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - zaloclawbot
keywords:
  - openclaw zalo clawbot channel
  - openclaw-zaloclawbot plugin install
  - zalo mini app qr login
  - owner-bound personal assistant bot
  - getupdates long-polling runtime
  - catalog integrity-hash verified install
  - zbsk login token timeout
topics:
  - OpenClaw
  - Channels
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/zaloclawbot
access_control_group: ["general"]
---

# OpenClaw — Connecting Zalo ClawBot (`openclaw-zaloclawbot`)

## Overview

This note is the setup procedure for the **Zalo ClawBot** channel, mirroring the `channels/zaloclawbot` source page. OpenClaw connects to Zalo ClawBot through the catalog-listed external `@zalo-platforms/openclaw-zaloclawbot` plugin, with login via a Zalo Mini App QR code. It covers version compatibility, prerequisites, the recommended `openclaw onboard` install, the four-step manual install (install → enable → QR login → restart), the owner-bound personal-assistant model on shared official OA infrastructure, the long-polling `getUpdates` runtime under the hood, and QR/version troubleshooting. Unlike the standard developer Zalo channel (`oc_channels_zalo`), which requires registering your own Zalo Official Account (OA) and pasting static developer credentials, Zalo ClawBot provisions a private owner-bound bot through a secure Mini App flow.

## Compatibility

The plugin tracks a single supported line: plugin version `0.1.x` requires OpenClaw `>=2026.4.10`, installs from the `latest` npm dist-tag, and is "Active / Beta" status. (The page documents only this one row.)

## Prerequisites

Three prerequisites must be met before install:

- **Node.js >= 22**.
- **OpenClaw** must be installed (the `openclaw` CLI must be available).
- A **Zalo account on a mobile device** to scan the login QR code.

## Install with onboard (recommended)

The recommended path is the OpenClaw onboarding wizard. Run it and pick **Zalo ClawBot** from the channel menu:

```bash
openclaw onboard
```

The wizard installs the plugin from the official catalog (integrity-verified), renders the login QR right in the terminal, and finishes the channel once you scan it with the Zalo app. No extra commands are needed.

## Manual Installation

To add the channel to an already-onboarded gateway, follow these four steps in order.

### 1. Install the plugin

```bash
openclaw plugins install "@zalo-platforms/openclaw-zaloclawbot@0.1.4"
```

Use the exact pinned version shown above (it matches the official catalog entry), so OpenClaw verifies the package against the catalog integrity hash during install.

### 2. Enable the plugin in config

```bash
openclaw config set plugins.entries.openclaw-zaloclawbot.enabled true
```

### 3. Generate QR code and log in

```bash
openclaw channels login --channel openclaw-zaloclawbot
```

Scan the terminal-rendered QR code using the Zalo mobile app, accept the Terms of Use inside the Zalo Mini App, and authorize the session.

### 4. Restart the gateway

```bash
openclaw gateway restart
```

## How It Works

Unlike the standard developer Zalo channel — which requires you to register your own Zalo Official Account (OA) and paste static developer credentials — Zalo ClawBot operates as an **owner-bound personal assistant** using a shared, official infrastructure:

1. **Secure Onboarding** — the QR code resolves to a secure Zalo Mini App that binds a newly-provisioned, private bot under a shared official OA directly to your Zalo User ID.
2. **Owner-Bound Privacy** — by design, the bot is restricted to communicating *only* with its owner; messages from other users are dropped at the platform level, making the connection private and secure.
3. **Official API path** — the plugin uses Zalo Bot Platform APIs instead of browser or web-session automation.

## Under the Hood

The Zalo ClawBot plugin communicates with Zalo APIs via a persistent long-polling message loop. To maintain a clean and lightweight runtime:

- Long-poll connections utilize the `getUpdates` endpoint.
- Webhooks are disabled by default for local desktop/terminal gateway runs.
- Messages are processed client-side and mapped directly to your local agent runtime.

The external plugin manages bot credentials under the OpenClaw state directory. Treat that directory as sensitive and include it in the same access-control and backup policy as the rest of your OpenClaw state.

## Troubleshooting

- **QR Login Timeout** — the login token (`zbsk`) expires after 5 minutes for security reasons. If the QR code expires before you scan it, simply rerun the login command to generate a new one.
- **Gateway Fails to Load** — ensure your OpenClaw host version is `2026.4.10` or higher. Older versions do not support the external npm-plugin installation ledger.

**Source**: OpenClaw documentation — `channels/zaloclawbot` (mirror `inbox/openclaw_docs/channels/zaloclawbot.md`)
**Last Updated**: 2026-06-22
**Status**: Active
