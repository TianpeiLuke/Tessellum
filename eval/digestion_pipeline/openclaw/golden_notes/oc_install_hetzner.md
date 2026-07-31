---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - hetzner
keywords:
  - openclaw hetzner vps
  - run openclaw 24/7 docker
  - hetzner docker compose gateway
  - openclaw ssh tunnel control ui
  - bake binaries persistent openclaw
  - hetzner terraform infrastructure as code
  - allowtcpforwarding local
topics:
  - OpenClaw
  - Install — Hetzner
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/hetzner
access_control_group: ["general"]
---

# OpenClaw — Install on a Hetzner VPS (Docker, 24/7)

## Overview

This note is the **procedure** for running a persistent OpenClaw Gateway 24/7 on a cheap Hetzner VPS using Docker, with durable state, baked-in binaries, and safe restart behavior — mirroring the `install/hetzner` source page. It covers the goal and security-model reminder, the plain-terms summary, the experienced-operator quick path, prerequisites, the eight inline `<Steps>` (provision the VPS → install Docker → clone the repo → create persistent host directories → configure `.env` → write `docker-compose.yml` → run the shared Docker-VM-runtime steps → Hetzner-specific SSH-tunnel access), the Terraform Infrastructure-as-Code alternative, and next steps. The shared bake/build/persist/update sub-steps are deferred to `oc_install_docker_vm_runtime` exactly as the source defers them to `/install/docker-vm-runtime`.

## Goal and Security Model

Run a persistent OpenClaw Gateway on a Hetzner VPS using Docker, with durable state, baked-in binaries, and safe restart behavior. The source frames this as "OpenClaw 24/7 for ~$5" — the simplest reliable always-on setup. Hetzner pricing changes, so pick the smallest Debian/Ubuntu VPS and scale up if you hit OOMs.

The **security-model reminder** (deploy this only inside a sound trust boundary): company-shared agents are fine when everyone is in the same trust boundary and the runtime is business-only; keep strict separation — a dedicated VPS/runtime plus dedicated accounts, with **no** personal Apple/Google/browser/password-manager profiles on that host; if users are adversarial to each other, split by gateway/host/OS user. The source links out to its `/gateway/security` and `/vps` pages for the full posture.

## What Are We Doing (Simple Terms)

The deploy in plain terms: rent a small Linux server (Hetzner VPS); install Docker (the isolated app runtime); start the OpenClaw Gateway in Docker; persist `~/.openclaw` + `~/.openclaw/workspace` on the host so state survives restarts/rebuilds; and access the Control UI from your laptop via an SSH tunnel. That mounted `~/.openclaw` state includes `openclaw.json`, per-agent `agents/<agentId>/agent/auth-profiles.json`, and `.env`.

The Gateway can be reached two ways: **SSH port forwarding** from your laptop (the recommended default), or **direct port exposure** if you manage firewalling and tokens yourself. This guide assumes Ubuntu or Debian on Hetzner; on another Linux VPS, map packages accordingly. For the generic containerized-gateway flow this build extends, the source points to its `/install/docker` page.

## Quick Path (Experienced Operators)

The eight-step quick path for operators who do not need the detailed walkthrough: (1) Provision Hetzner VPS; (2) Install Docker; (3) Clone OpenClaw repository; (4) Create persistent host directories; (5) Configure `.env` and `docker-compose.yml`; (6) Bake required binaries into the image; (7) `docker compose up -d`; (8) Verify persistence and Gateway access.

## What You Need

Prerequisites before starting: a Hetzner VPS with root access; SSH access from your laptop; basic comfort with SSH + copy/paste; ~20 minutes; Docker and Docker Compose; model auth credentials; and optional provider credentials (WhatsApp QR, Telegram bot token, Gmail OAuth).

## Step-by-Step Deploy (`<Steps>`)

**Step 1 — Provision the VPS.** Create an Ubuntu or Debian VPS in Hetzner and connect as root. The source notes the VPS is treated as **stateful** — do not treat it as disposable infrastructure.

```bash
ssh root@YOUR_VPS_IP
```

**Step 2 — Install Docker (on the VPS).** Install git/curl/CA certificates, then install Docker via the official convenience script, and verify both Docker and the Compose plugin:

```bash
apt-get update
apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sh
# Verify:
docker --version
docker compose version
```

**Step 3 — Clone the OpenClaw repository.** Clone `https://github.com/openclaw/openclaw.git` and `cd openclaw`. This guide assumes you will **build a custom image** (not just run a pre-built one) to guarantee binary persistence.

**Step 4 — Create persistent host directories.** Docker containers are ephemeral, so all long-lived state must live on the host. Create the config + workspace directories and set ownership to the container user (uid `1000`):

```bash
mkdir -p /root/.openclaw/workspace
# Set ownership to the container user (uid 1000):
chown -R 1000:1000 /root/.openclaw
```

**Step 5 — Configure environment variables.** Create `.env` in the repository root. Set `OPENCLAW_GATEWAY_TOKEN` when you want to manage the stable gateway token through `.env`; otherwise configure `gateway.auth.token` before relying on clients across restarts — if neither source exists, OpenClaw uses a runtime-only token for that startup. Generate a keyring password with `openssl rand -hex 32` and paste it into `GOG_KEYRING_PASSWORD`. **Do not commit this file.** The `.env` is for container/runtime env such as `OPENCLAW_GATEWAY_TOKEN`; stored provider OAuth/API-key auth lives in the mounted `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`.

```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/root/.openclaw
OPENCLAW_WORKSPACE_DIR=/root/.openclaw/workspace

GOG_KEYRING_PASSWORD=
XDG_CONFIG_HOME=/home/node/.openclaw
```

**Step 6 — Docker Compose configuration.** Create or update `docker-compose.yml`. The service builds from the local repo (`build: .`), runs with `restart: unless-stopped`, loads `.env`, mounts the host config + workspace directories into `/home/node/.openclaw` and `/home/node/.openclaw/workspace`, and publishes the port loopback-only by default. The `127.0.0.1:` prefix keeps the Gateway loopback-only on the VPS (access via SSH tunnel); to expose it publicly, remove the `127.0.0.1:` prefix and firewall accordingly.

```yaml
services:
  openclaw-gateway:
    image: ${OPENCLAW_IMAGE}
    build: .
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - HOME=/home/node
      - NODE_ENV=production
      - TERM=xterm-256color
      - OPENCLAW_GATEWAY_BIND=${OPENCLAW_GATEWAY_BIND}
      - OPENCLAW_GATEWAY_PORT=${OPENCLAW_GATEWAY_PORT}
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
      - GOG_KEYRING_PASSWORD=${GOG_KEYRING_PASSWORD}
      - XDG_CONFIG_HOME=${XDG_CONFIG_HOME}
      - PATH=/home/linuxbrew/.linuxbrew/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    volumes:
      - ${OPENCLAW_CONFIG_DIR}:/home/node/.openclaw
      - ${OPENCLAW_WORKSPACE_DIR}:/home/node/.openclaw/workspace
    ports:
      # Recommended: keep the Gateway loopback-only on the VPS; access via SSH tunnel.
      # To expose it publicly, remove the `127.0.0.1:` prefix and firewall accordingly.
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"
    command:
      [
        "node",
        "dist/index.js",
        "gateway",
        "--bind",
        "${OPENCLAW_GATEWAY_BIND}",
        "--port",
        "${OPENCLAW_GATEWAY_PORT}",
        "--allow-unconfigured",
      ]
```

The source warns that `--allow-unconfigured` is only for bootstrap convenience — it is **not** a replacement for a proper gateway configuration; still set auth (`gateway.auth.token` or password) and use safe bind settings for your deployment.

**Step 7 — Shared Docker VM runtime steps.** This guide hands off the common Docker-host flow to the shared runtime guide rather than repeating it: bake required binaries into the image, build and launch, what persists where, and updates. See the `oc_install_docker_vm_runtime` note below (source: `/install/docker-vm-runtime`).

**Step 8 — Hetzner-specific access.** After the shared build and launch steps, open the SSH tunnel. **Prerequisite:** ensure your VPS sshd config allows TCP forwarding. If you hardened your SSH config, check `/etc/ssh/sshd_config` and set `AllowTcpForwarding local` — `local` allows `ssh -L` local forwards from your laptop while blocking remote forwards from the server; setting it to `no` will fail the tunnel with `channel 3: open failed: administratively prohibited: open failed`. After confirming TCP forwarding is enabled, restart the SSH service (`systemctl restart ssh`) and run the tunnel from your laptop, then open `http://127.0.0.1:18789/` and paste the configured shared secret (this guide uses the gateway token by default; if you switched to password auth, use that password instead).

```bash
# /etc/ssh/sshd_config
AllowTcpForwarding local

# From your laptop:
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP
```

The shared persistence map lives in the `oc_install_docker_vm_runtime` "what persists where" section (source: `/install/docker-vm-runtime#what-persists-where`).

## Infrastructure as Code (Terraform)

For teams preferring infrastructure-as-code workflows, a **community-maintained** Terraform setup provides: modular Terraform configuration with remote state management; automated provisioning via cloud-init; deployment scripts (bootstrap, deploy, backup/restore); security hardening (firewall, UFW, SSH-only access); and SSH-tunnel configuration for gateway access. The source lists two repositories — Infrastructure: `openclaw-terraform-hetzner`; Docker config: `openclaw-docker-config` (both under the `andreesg` GitHub org). This approach complements the manual Docker setup above with reproducible deployments, version-controlled infrastructure, and automated disaster recovery. The source flags it as community-maintained and directs issues/contributions to the repository links.

## Next Steps

After the gateway is running, the source points to three follow-ups: set up messaging channels (`/channels`), configure the Gateway (`/gateway/configuration`), and keep OpenClaw up to date (`/install/updating`). Its Related section also cross-links the Install overview (`/install`), the sibling Fly.io guide (`/install/fly`), the generic Docker guide (`/install/docker`), and VPS hosting (`/vps`).

**Source**: OpenClaw documentation — `install/hetzner` (mirror `inbox/openclaw_docs/install/hetzner.md`)
**Last Updated**: 2026-06-22
**Status**: Active
