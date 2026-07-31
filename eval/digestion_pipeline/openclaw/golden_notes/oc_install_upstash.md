---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - upstash
keywords:
  - openclaw upstash box
  - upstash keep-alive box
  - ssh tunnel dashboard
  - openclaw gateway bind lan
  - nohup openclaw gateway
  - openclaw onboard install-daemon
  - box init script auto-restart
  - frozen ssh tunnel clean config
topics:
  - OpenClaw
  - Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/upstash
access_control_group: ["general"]
---

# OpenClaw — Hosting on an Upstash Box

## Overview

This note is the step-by-step procedure for running a persistent OpenClaw Gateway on an **Upstash Box** — a managed Linux environment with keep-alive lifecycle support — mirroring the `install/upstash` source page. The path is: create a keep-alive Box, forward the dashboard port to your local machine over an **SSH tunnel** (never expose the Gateway port to the public internet), `npm install -g openclaw` inside the Box, run `openclaw onboard --install-daemon`, bind the Gateway to the LAN and launch it backgrounded with `nohup`, set the same launch command as the Box init script for auto-restart, and recover a frozen SSH tunnel with a clean SSH config. All commands and the dashboard URL are reproduced verbatim from the source.

## Prerequisites

The source lists three prerequisites: an **Upstash account**, a **keep-alive Upstash Box**, and an **SSH client** on your local machine. The keep-alive lifecycle is what lets the Box (and therefore the Gateway) keep running persistently.

## Create a Box

Create a **keep-alive Box** in the **Upstash Console**. Note two values: the **Box ID** (such as `right-flamingo-14486`) and your **Box API key**. The Box ID is used as the SSH user, and the Box API key is used as the SSH password when you open the tunnel. Upstash maintains its current OpenClaw Box walkthrough at the [OpenClaw Setup](https://upstash.com/docs/box/guides/openclaw-setup) guide.

## Connect with an SSH tunnel

Forward the OpenClaw dashboard port to your local machine, using your Box API key as the SSH password when prompted:

```bash
ssh -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -L 18789:127.0.0.1:18789 <box-id>@us-east-1.box.upstash.com
```

This forwards local port `18789` to `127.0.0.1:18789` on the Box (where the Gateway dashboard listens). The `ServerAliveInterval=15` / `ServerAliveCountMax=3` keepalive options reduce idle tunnel drops during onboarding. The source is explicit that you should use this SSH tunnel for dashboard access and must **not** expose the Gateway port directly to the public internet.

## Install OpenClaw

Inside the Box, install OpenClaw globally with npm:

```bash
sudo npm install -g openclaw
```

## Run onboarding

Still inside the Box, run onboarding with the daemon-install flag and follow the prompts:

```bash
openclaw onboard --install-daemon
```

When onboarding finishes, **copy the dashboard URL and token** — you will use both to reach the dashboard locally over the tunnel.

## Start the Gateway

Configure the Gateway for the Box network and start it in the background. First bind the Gateway to the LAN, then launch it backgrounded with `nohup`, redirecting output to `gateway.log`:

```bash
openclaw config set gateway.bind lan
nohup openclaw gateway > gateway.log 2>&1 &
```

With the SSH tunnel active, open the dashboard URL locally in your browser. The token is carried in the URL fragment:

```text
http://127.0.0.1:18789/#token=<your-token>
```

## Auto-restart

Set the same backgrounded launch command — `nohup openclaw gateway > gateway.log 2>&1 &` (identical to the one in "Start the Gateway") — as the **Box init script** so the Gateway restarts when the Box starts.

## Troubleshooting

If SSH freezes during onboarding, reconnect with a clean SSH config plus keepalives:

```bash
ssh -F /dev/null -o ControlMaster=no -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -L 18789:127.0.0.1:18789 <box-id>@us-east-1.box.upstash.com
```

The `-F /dev/null` and `-o ControlMaster=no` flags bypass stale local `~/.ssh/config` settings, and the keepalive options keep the tunnel active through idle network periods.

**Source**: OpenClaw documentation — `install/upstash` (mirror `inbox/openclaw_docs/install/upstash.md`)
**Last Updated**: 2026-06-22
**Status**: Active
