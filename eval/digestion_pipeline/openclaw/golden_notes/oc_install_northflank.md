---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - northflank
keywords:
  - openclaw northflank deploy
  - one-click cloud deploy
  - browser control ui
  - openclaw_gateway_token
  - deploy stack template
  - persistent /data volume
  - no terminal on the server
  - connect a channel onboard
topics:
  - OpenClaw
  - Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/northflank
access_control_group: ["general"]
---

# OpenClaw — Deploying on Northflank (One-Click Cloud Deploy)

## Overview

This note is the step-by-step procedure for deploying OpenClaw on **Northflank** using its one-click template and accessing the running Gateway through the browser **Control UI** — the easiest "no terminal on the server" path, where Northflank runs the Gateway for you. It mirrors the `install/northflank` source page: the eight-step deploy flow (open the template, create an account, deploy, set the required `OPENCLAW_GATEWAY_TOKEN`, build and run, view resources, open the service, open the public `/openclaw` URL), what the hosted deployment provides (Gateway + Control UI and a persistent `/data` volume), how to connect a messaging channel, and the next-step pointers.

## How to Get Started

Follow the deploy template's eight steps in order. The template builds and runs OpenClaw with the Gateway hosted by Northflank, so no server terminal is required.

1. Click [Deploy OpenClaw](https://northflank.com/stacks/deploy-openclaw) to open the template.
2. Create an [account on Northflank](https://app.northflank.com/signup) if you don't already have one.
3. Click **Deploy OpenClaw now**.
4. Set the required environment variable: `OPENCLAW_GATEWAY_TOKEN` (use a strong random value).
5. Click **Deploy stack** to build and run the OpenClaw template.
6. Wait for the deployment to complete, then click **View resources**.
7. Open the OpenClaw service.
8. Open the public OpenClaw URL at `/openclaw` and connect using the configured shared secret. This template uses `OPENCLAW_GATEWAY_TOKEN` by default; if you replace it with password auth, use that password instead.

The `OPENCLAW_GATEWAY_TOKEN` value set in step 4 is the shared secret you authenticate the Control UI with in step 8 — the source states the template uses this token by default, and that if you replace it with password auth you use that password instead. The source does not specify any further configuration beyond these steps.

## What You Get

The hosted Northflank deployment provides:

- Hosted OpenClaw Gateway + Control UI.
- Persistent storage via a Northflank Volume (`/data`) so `openclaw.json`, per-agent `auth-profiles.json`, channel/provider state, sessions, and workspace survive redeploys.

The `/data` volume is what makes the deployment durable across redeploys: per the source, that volume is where the gateway config (`openclaw.json`), each agent's `auth-profiles.json`, channel and provider state, sessions, and the workspace persist.

## Connect a Channel

To wire a messaging channel to the hosted Gateway, use the Control UI at `/openclaw`, or run `openclaw onboard` via SSH for channel setup instructions. The source lists three channel options:

- [Telegram](https://docs.openclaw.ai/channels/telegram) (fastest — just a bot token).
- [Discord](https://docs.openclaw.ai/channels/discord).
- [All channels](https://docs.openclaw.ai/channels).

## Next Steps

The source page closes with three follow-up pointers (link-outs, not re-documented here):

- Set up messaging channels: [Channels](https://docs.openclaw.ai/channels).
- Configure the Gateway: [Gateway configuration](https://docs.openclaw.ai/gateway/configuration).
- Keep OpenClaw up to date: [Updating](https://docs.openclaw.ai/install/updating).

**Source**: OpenClaw documentation — `install/northflank` (mirror `inbox/openclaw_docs/install/northflank.md`)
**Last Updated**: 2026-06-22
**Status**: Active
