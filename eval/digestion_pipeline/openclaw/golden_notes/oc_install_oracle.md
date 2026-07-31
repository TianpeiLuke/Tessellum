---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - oracle_cloud
keywords:
  - openclaw oracle cloud install
  - always free arm tier
  - tailscale serve gateway
  - gateway token auth loopback
  - vcn security list lockdown
  - openclaw security audit posture
  - aarch64 arm self host
  - ssh tunnel fallback 18789
topics:
  - OpenClaw
  - Oracle Cloud Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/oracle
access_control_group: ["general"]
---

# OpenClaw — Self-Host on Oracle Cloud (Always Free ARM Tier)

## Overview

This note is the step-by-step **procedure** for running a persistent OpenClaw Gateway for free on Oracle Cloud's **Always Free** ARM tier (up to 4 OCPU, 24 GB RAM, 200 GB storage), mirroring the `install/oracle` source page. The runbook creates an Oracle Cloud Infrastructure (OCI) Ampere ARM (`aarch64`) instance, installs Tailscale SSH and OpenClaw, configures the gateway to bind to loopback behind token auth and Tailscale Serve, locks the VCN Security List down to only Tailscale UDP traffic, and then verifies the resulting security posture. It also covers ARM-specific notes, persistence/backups, an SSH-tunnel fallback when Tailscale Serve fails, and troubleshooting. The canonical Tailscale and gateway-config detail lives in the sibling docs linked under Related Notes; this note documents only the Oracle-specific deploy path.

## Prerequisites

The page lists four prerequisites before starting (estimated time ~30 minutes):

- An **Oracle Cloud account** ([signup](https://www.oracle.com/cloud/free/)); a [community signup guide](https://gist.github.com/rssnyder/51e3cfedd730e7dd5f4a816143b25dbd) is linked for signup issues.
- A **Tailscale account** (free at [tailscale.com](https://tailscale.com)).
- An **SSH key pair**.
- **About 30 minutes**.

## Setup

The setup is an 8-step `<Steps>` sequence.

**Step 1 — Create an OCI instance.** Log into the [Oracle Cloud Console](https://cloud.oracle.com/), navigate to **Compute > Instances > Create Instance**, and configure: **Name** `openclaw`; **Image** Ubuntu 24.04 (aarch64); **Shape** `VM.Standard.A1.Flex` (Ampere ARM); **OCPUs** 2 (or up to 4); **Memory** 12 GB (or up to 24 GB); **Boot volume** 50 GB (up to 200 GB free); **SSH key** add your public key. Click **Create** and note the public IP address. The page warns: if creation fails with "Out of capacity", try a different availability domain or retry later, because free-tier capacity is limited.

**Step 2 — Connect and update the system.** SSH in with the public IP, update packages, and install `build-essential` (required for ARM compilation of some dependencies). **Step 3 — Configure user and hostname.** Set the hostname, set a password for `ubuntu`, and enable linger so user services keep running after logout (the page bundles these two steps' commands shown together below):

```bash
ssh ubuntu@YOUR_PUBLIC_IP

sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential

sudo hostnamectl set-hostname openclaw
sudo passwd ubuntu
sudo loginctl enable-linger ubuntu
```

**Step 4 — Install Tailscale.** Install Tailscale and bring it up with SSH and a hostname; from then on connect via Tailscale (`ssh ubuntu@openclaw`):

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh --hostname=openclaw
```

**Step 5 — Install OpenClaw.** Run the installer and re-source the shell. When prompted "How do you want to hatch your bot?", select **Do this later**:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
source ~/.bashrc
```

**Step 6 — Configure the gateway.** Use token auth with Tailscale Serve for secure remote access. Set the gateway to bind to loopback, set `auth.mode` to `token`, generate a gateway token via `openclaw doctor --generate-gateway-token`, set Tailscale mode to `serve`, set `trustedProxies` to `["127.0.0.1"]`, then restart the gateway service:

```bash
openclaw config set gateway.bind loopback
openclaw config set gateway.auth.mode token
openclaw doctor --generate-gateway-token
openclaw config set gateway.tailscale.mode serve
openclaw config set gateway.trustedProxies '["127.0.0.1"]'

systemctl --user restart openclaw-gateway.service
```

The page is explicit that `gateway.trustedProxies=["127.0.0.1"]` here is **only** for the local Tailscale Serve proxy's forwarded-IP/local-client handling — it is **not** `gateway.auth.mode: "trusted-proxy"`. It also notes a behavioral caveat: diff-viewer routes keep fail-closed behavior in this setup, so raw `127.0.0.1` viewer requests without forwarded proxy headers can return `Diff not found`; use `mode=file` / `mode=both` for attachments, or intentionally enable remote viewers and set `plugins.entries.diffs.config.viewerBaseUrl` (or pass a proxy `baseUrl`) if you need shareable viewer links.

**Step 7 — Lock down VCN security.** Block all traffic except Tailscale at the network edge: go to **Networking > Virtual Cloud Networks** in the OCI Console, click your VCN, then **Security Lists > Default Security List**; **remove** all ingress rules except `0.0.0.0/0 UDP 41641` (Tailscale); keep default egress rules (allow all outbound). The page states this blocks SSH on port 22, HTTP, HTTPS, and everything else at the network edge — from this point on you can only connect via Tailscale.

**Step 8 — Verify.** Check version, service status, Tailscale Serve status, and the loopback gateway:

```bash
openclaw --version
systemctl --user status openclaw-gateway.service
tailscale serve status
curl http://localhost:18789
```

Access the Control UI from any tailnet device at `https://openclaw.<tailnet-name>.ts.net/`, replacing `<tailnet-name>` with your tailnet name (visible in `tailscale status`).

## Verify the security posture

With the VCN locked down (only UDP 41641 open) and the Gateway bound to loopback, public traffic is blocked at the network edge and admin access is tailnet-only. Per the page, that removes the need for several traditional VPS hardening steps:

| Traditional step   | Needed?     | Why                                                                       |
| ------------------ | ----------- | ------------------------------------------------------------------------- |
| UFW firewall       | No          | The VCN blocks traffic before it reaches the instance.                    |
| fail2ban           | No          | Port 22 is blocked at the VCN; no brute-force surface.                    |
| sshd hardening     | No          | Tailscale SSH does not use sshd.                                          |
| Disable root login | No          | Tailscale authenticates by tailnet identity, not system users.            |
| SSH key-only auth  | No          | Same — tailnet identity replaces system SSH keys.                         |
| IPv6 hardening     | Usually not | Depends on VCN/subnet settings; verify what is actually assigned/exposed. |

Still recommended by the page: `chmod 700 ~/.openclaw` to restrict credential file permissions; `openclaw security audit` for an OpenClaw-specific posture check; regular `sudo apt update && sudo apt upgrade` for OS patches; and reviewing devices in the [Tailscale admin console](https://login.tailscale.com/admin) periodically. The page also gives quick verification commands: confirm no public ports are listening with `sudo ss -tlnp | grep -v '127.0.0.1\|::1'`; verify Tailscale SSH is active with `tailscale status | grep -q 'offers: ssh' && echo "Tailscale SSH active"`; and, optionally, once Tailscale SSH is confirmed working, disable sshd entirely with `sudo systemctl disable --now ssh`.

## ARM notes

The Always Free tier is ARM (`aarch64`). The page states most OpenClaw features work fine and only a small number of native binaries need ARM builds: Node.js, Telegram, and WhatsApp (Baileys) are pure JavaScript with no issues; most npm packages with native code have pre-built `linux-arm64` artifacts available; optional CLI helpers (e.g. Go/Rust binaries shipped by skills) should be checked for an `aarch64` / `linux-arm64` release before installing. Verify the architecture with `uname -m` (should print `aarch64`). For binaries without an ARM build, install from source or skip them.

## Persistence and backups

OpenClaw state lives under `~/.openclaw/` (`openclaw.json`, per-agent `auth-profiles.json`, channel/provider state, and session data) and `~/.openclaw/workspace/` (the agent workspace: SOUL.md, memory, artifacts). The page notes these survive reboots. To take a portable snapshot, run `openclaw backup create`.

## Fallback: SSH tunnel

If Tailscale Serve is not working, the page documents an SSH tunnel from your local machine, then opening `http://localhost:18789`:

```bash
ssh -L 18789:127.0.0.1:18789 ubuntu@openclaw
```

## Troubleshooting

The page lists four troubleshooting items: **Instance creation fails ("Out of capacity")** — free-tier ARM instances are popular, so try a different availability domain or retry during off-peak hours. **Tailscale will not connect** — run `sudo tailscale up --ssh --hostname=openclaw --reset` to re-authenticate. **Gateway will not start** — run `openclaw doctor --non-interactive` and check logs with `journalctl --user -u openclaw-gateway.service -n 50`. **ARM binary issues** — most npm packages work on ARM64; for native binaries look for `linux-arm64` or `aarch64` releases, and verify architecture with `uname -m`.

## Next steps

The page's "Next steps" links: connect channels (Telegram, WhatsApp, Discord, and more) via `/channels`; review all config options via `/gateway/configuration`; and keep OpenClaw up to date via `/install/updating`. Its "Related" links point to the [Install overview](https://docs.openclaw.ai/install), [GCP](https://docs.openclaw.ai/install/gcp), and [VPS hosting](https://docs.openclaw.ai/vps) pages.

**Source**: OpenClaw documentation — `install/oracle` (mirror `inbox/openclaw_docs/install/oracle.md`)
**Last Updated**: 2026-06-22
**Status**: Active
