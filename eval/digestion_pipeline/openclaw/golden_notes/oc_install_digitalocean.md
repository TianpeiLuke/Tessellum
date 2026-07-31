---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - digitalocean
keywords:
  - openclaw digitalocean droplet
  - persistent gateway vps
  - openclaw onboard install-daemon
  - systemd-user openclaw-gateway service
  - droplet swap 1 gb ram
  - control ui ssh tunnel tailscale serve
  - openclaw backup create
  - loginctl enable-linger
topics:
  - OpenClaw
  - Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/digitalocean
access_control_group: ["general"]
---

# OpenClaw — Install on a DigitalOcean Droplet

## Overview

This note is the procedure for hosting a persistent OpenClaw Gateway on a DigitalOcean Droplet (~$6/month for the 1 GB Basic plan), mirroring the `install/digitalocean` source page. It covers the prerequisites, the six-step Setup flow (create a Droplet, connect and install, run onboarding, add swap, verify the gateway, and access the Control UI via three options), state persistence and backups, 1 GB RAM tuning, and troubleshooting. DigitalOcean is presented as the simplest paid VPS path; the source also points to [Hetzner](https://docs.openclaw.ai/install/hetzner) (€3.79/mo, more cores/RAM per dollar) and [Oracle Cloud](https://docs.openclaw.ai/install/oracle) (Always Free ARM, up to 4 OCPU / 24 GB RAM, but ARM-only and finicky signup) as cheaper or free alternatives.

## Prerequisites

The source lists three prerequisites for the deploy:

- A DigitalOcean account (the page links the [signup](https://cloud.digitalocean.com/registrations/new) form).
- An SSH key pair (or willingness to use password auth).
- About 20 minutes.

## Setup

The Setup section is a six-step `<Steps>` walkthrough.

### Step 1 — Create a Droplet

The source warns to use a clean base image (Ubuntu 24.04 LTS) and to avoid third-party Marketplace 1-click images unless you have reviewed their startup scripts and firewall defaults. To create the Droplet: log into [DigitalOcean](https://cloud.digitalocean.com/), click **Create > Droplets**, and choose **Region:** closest to you, **Image:** Ubuntu 24.04 LTS, **Size:** Basic, Regular, 1 vCPU / 1 GB RAM / 25 GB SSD, and **Authentication:** SSH key (recommended) or password. Then click **Create Droplet** and note the IP address.

### Step 2 — Connect and install

SSH in as root, update the system, install Node.js 24 from NodeSource, run the OpenClaw install script, then create and switch to a non-root `openclaw` user:

```bash
ssh root@YOUR_DROPLET_IP

apt update && apt upgrade -y

# Install Node.js 24
curl -fsSL https://deb.nodesource.com/setup_24.x | bash -
apt install -y nodejs

# Install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# Create the non-root user that will own OpenClaw state and services.
adduser openclaw
usermod -aG sudo openclaw
loginctl enable-linger openclaw

su - openclaw
openclaw --version
```

Per the source, use the root shell only for system bootstrap. Run OpenClaw commands as the non-root `openclaw` user so state lives under `/home/openclaw/.openclaw/` and the Gateway installs as that user's systemd service. The `loginctl enable-linger openclaw` call is what allows that user's systemd services to keep running when the user is not logged in.

### Step 3 — Run onboarding

Run the onboarding wizard with the daemon-install flag:

```bash
openclaw onboard --install-daemon
```

The source states the wizard walks you through model auth, channel setup, gateway token generation, and daemon installation (systemd).

### Step 4 — Add swap (recommended for 1 GB Droplets)

Allocate a 2 GB swap file, enable it, and persist it in `/etc/fstab` so it survives reboots:

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Step 5 — Verify the gateway

Check OpenClaw status and the systemd-user service, and follow its logs:

```bash
openclaw status
systemctl --user status openclaw-gateway.service
journalctl --user -u openclaw-gateway.service -f
```

### Step 6 — Access the Control UI

The source says the gateway binds to loopback by default, then offers three options to reach the Control UI. **Option A: SSH tunnel (simplest)** — from your local machine, forward the local port over SSH, then open `http://localhost:18789`. **Option B: Tailscale Serve** — install Tailscale, bring it up, set the gateway's Tailscale mode to `serve`, and restart the gateway; then open `https://<magicdns>/` from any device on your tailnet. **Option C: Tailnet bind (no Serve)** — bind the gateway directly to the tailnet and restart it, then open `http://<tailscale-ip>:18789` (token required).

```bash
# Option A: SSH tunnel (from your local machine)
ssh -L 18789:localhost:18789 root@YOUR_DROPLET_IP

# Option B: Tailscale Serve
curl -fsSL https://tailscale.com/install.sh | sudo sh
sudo tailscale up
openclaw config set gateway.tailscale.mode serve
openclaw gateway restart

# Option C: Tailnet bind (no Serve)
openclaw config set gateway.bind tailnet
openclaw gateway restart
```

Per the source, Tailscale Serve authenticates Control UI and WebSocket traffic via tailnet identity headers, which assumes the gateway host itself is trusted. HTTP API endpoints follow the gateway's normal auth mode (token/password) regardless. To require explicit shared-secret credentials over Serve, set `gateway.auth.allowTailscale: false` and use `gateway.auth.mode: "token"` or `"password"`.

## Persistence and backups

The source states OpenClaw state lives under `~/.openclaw/` (which holds `openclaw.json`, per-agent `auth-profiles.json`, channel/provider state, and session data) and `~/.openclaw/workspace/` (the agent workspace — SOUL.md, memory, artifacts). These survive Droplet reboots. To take a portable snapshot, run:

```bash
openclaw backup create
```

The page contrasts the two backup paths: DigitalOcean snapshots back up the whole Droplet, whereas `openclaw backup create` is portable across hosts.

## 1 GB RAM tips

The $6 Droplet only has 1 GB RAM. The source lists four tuning tips to keep things smooth:

- Make sure the swap step above is in `/etc/fstab` so it survives reboots.
- Prefer API-based models (Claude, GPT) over local ones — local LLM inference does not fit in 1 GB.
- Set `agents.defaults.model.primary` to a smaller model if you hit OOMs on large prompts.
- Monitor with `free -h` and `htop`.

## Troubleshooting

The source documents three failure modes:

- **Gateway will not start** — run `openclaw doctor --non-interactive` and check logs with `journalctl --user -u openclaw-gateway.service -n 50`.
- **Port already in use** — run `lsof -i :18789` to find the process, then stop it.
- **Out of memory** — verify swap is active with `free -h`. If still hitting OOM, use API-based models (Claude, GPT) rather than local models, or upgrade to a 2 GB Droplet.

## Next steps

The source page links onward to: [Channels](https://docs.openclaw.ai/channels) (connect Telegram, WhatsApp, Discord, and more), [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) (all config options), and [Updating](https://docs.openclaw.ai/install/updating) (keep OpenClaw up to date). Its Related card group also points to the [Install overview](https://docs.openclaw.ai/install), [Fly.io](https://docs.openclaw.ai/install/fly), [Hetzner](https://docs.openclaw.ai/install/hetzner), and [VPS hosting](https://docs.openclaw.ai/vps) pages.

**Source**: OpenClaw documentation — `install/digitalocean` (mirror `inbox/openclaw_docs/install/digitalocean.md`)
**Last Updated**: 2026-06-22
**Status**: Active
