---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - gcp
keywords:
  - openclaw gcp install
  - compute engine vm gateway
  - docker compose openclaw gateway
  - openclaw_gateway_token env
  - ssh tunnel control ui 18789
  - gcp service account least privilege
  - exit 137 oom docker build
  - persistent openclaw config dir
topics:
  - OpenClaw
  - GCP Compute Engine Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/gcp
access_control_group: ["general"]
---

# OpenClaw — Install on GCP Compute Engine (Docker)

## Overview

This note is the **procedure** for running a persistent, 24/7 OpenClaw Gateway on a **GCP Compute Engine VM** using Docker, with durable state, baked-in binaries, and safe restart behavior. It mirrors the `install/gcp` source page: create a GCP project and enable billing, create a Compute Engine VM, install Docker, persist `~/.openclaw` + `~/.openclaw/workspace` on the host, configure `.env` and `docker-compose.yml`, bake binaries and launch, reach the Control UI over an SSH tunnel, troubleshoot, and (for automation) provision a least-privilege service account. The shared bake/build/persist/update mechanics are deferred to `oc_install_docker_vm_runtime`; this note covers only the GCP-specific create-VM and access steps. The guide uses Debian on GCP Compute Engine (Ubuntu also works, with packages mapped accordingly), and quotes a target cost of roughly **$5–12/mo** depending on machine type and region.

## What are we doing (simple terms)?

The deployment, in plain terms, is: create a GCP project and enable billing; create a Compute Engine VM; install Docker (the isolated app runtime); start the OpenClaw Gateway in Docker; persist `~/.openclaw` + `~/.openclaw/workspace` on the host so state survives restarts/rebuilds; and access the Control UI from your laptop via an SSH tunnel. That mounted `~/.openclaw` state includes `openclaw.json`, per-agent `agents/<agentId>/agent/auth-profiles.json`, and `.env`. The Gateway can be accessed either via **SSH port forwarding** from your laptop, or via **direct port exposure** if you manage firewalling and tokens yourself.

## Quick path (experienced operators)

The source lists the condensed sequence: (1) create GCP project + enable Compute Engine API; (2) create Compute Engine VM (`e2-small`, Debian 12, 20GB); (3) SSH into the VM; (4) install Docker; (5) clone OpenClaw repository; (6) create persistent host directories; (7) configure `.env` and `docker-compose.yml`; (8) bake required binaries, build, and launch.

## What you need

Prerequisites: a GCP account (free tier eligible for `e2-micro`); the gcloud CLI installed (or use the Cloud Console); SSH access from your laptop; basic comfort with SSH + copy/paste; ~20–30 minutes; Docker and Docker Compose; model auth credentials; and optional provider credentials (WhatsApp QR, Telegram bot token, Gmail OAuth).

## Provision the VM (gcloud CLI)

Install gcloud from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install) (Option A, recommended for automation; Option B is the Cloud Console UI at [console.cloud.google.com](https://console.cloud.google.com)), then create the project, enable billing, enable the Compute Engine API, and create the VM. Initialize and authenticate with `gcloud init` and `gcloud auth login`.

```bash
# Project + API
gcloud projects create my-openclaw-project --name="OpenClaw Gateway"
gcloud config set project my-openclaw-project
gcloud services enable compute.googleapis.com

# Create the VM
gcloud compute instances create openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --boot-disk-size=20GB \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

Billing must be enabled at [console.cloud.google.com/billing](https://console.cloud.google.com/billing) (required for Compute Engine). The Console equivalent is: IAM & Admin > Create Project (name + create + enable billing), then APIs & Services > Enable APIs > "Compute Engine API" > Enable; and Compute Engine > VM instances > Create instance (name `openclaw-gateway`, region `us-central1`, zone `us-central1-a`, machine type `e2-small`, boot disk Debian 12 20GB).

**Machine types** (source table): `e2-medium` — 2 vCPU, 4GB RAM, ~$25/mo, most reliable for local Docker builds; `e2-small` — 2 vCPU, 2GB RAM, ~$12/mo, minimum recommended for Docker build; `e2-micro` — 2 vCPU (shared), 1GB RAM, free tier eligible, but often fails with Docker build OOM (exit 137).

## Install Docker on the VM

SSH in with `gcloud compute ssh openclaw-gateway --zone=us-central1-a` (or the Console "SSH" button). SSH key propagation can take 1–2 minutes after VM creation — if the connection is refused, wait and retry. Then install Docker, add your user to the `docker` group, log out and back in for the group change to take effect, and verify.

```bash
sudo apt-get update
sudo apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
exit
# SSH back in, then verify:
docker --version
docker compose version
```

Next, clone the OpenClaw repository (`git clone https://github.com/openclaw/openclaw.git` then `cd openclaw`); the guide assumes you will build a custom image to guarantee binary persistence. Create the persistent host directories (`mkdir -p ~/.openclaw` and `mkdir -p ~/.openclaw/workspace`) because Docker containers are ephemeral and all long-lived state must live on the host.

## Configure environment variables (`.env`)

Create `.env` in the repository root. Set `OPENCLAW_GATEWAY_TOKEN` when you want to manage the stable gateway token through `.env`; otherwise configure `gateway.auth.token` before relying on clients across restarts. If neither source exists, OpenClaw uses a runtime-only token for that startup. Generate a keyring password with `openssl rand -hex 32` and paste it into `GOG_KEYRING_PASSWORD`. **Do not commit this file.** This `.env` is for container/runtime env such as `OPENCLAW_GATEWAY_TOKEN`; stored provider OAuth/API-key auth lives in the mounted `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`.

```bash
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/home/$USER/.openclaw
OPENCLAW_WORKSPACE_DIR=/home/$USER/.openclaw/workspace

GOG_KEYRING_PASSWORD=
XDG_CONFIG_HOME=/home/node/.openclaw
```

## Docker Compose configuration

Create or update `docker-compose.yml`. The recommended `ports` mapping keeps the Gateway loopback-only on the VM (`127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789`) — to expose it publicly, remove the `127.0.0.1:` prefix and firewall accordingly. The container mounts the persistent host directories as volumes and passes the env through `env_file` plus an explicit `environment` block.

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
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"
    command:
      ["node", "dist/index.js", "gateway", "--bind", "${OPENCLAW_GATEWAY_BIND}",
       "--port", "${OPENCLAW_GATEWAY_PORT}", "--allow-unconfigured"]
```

`--allow-unconfigured` is only for bootstrap convenience, **not** a replacement for a proper gateway configuration — still set auth (`gateway.auth.token` or password) and use safe bind settings for your deployment.

## Bake binaries, build, launch, and GCP-specific notes

For the common Docker host flow, the source defers to the shared **Docker VM Runtime** guide (see the `oc_install_docker_vm_runtime` note below; source: `/install/docker-vm-runtime`): bake required binaries into the image (`/install/docker-vm-runtime#bake-required-binaries-into-the-image`), build and launch (`/install/docker-vm-runtime#build-and-launch`), what persists where (`/install/docker-vm-runtime#what-persists-where`), and updates (`/install/docker-vm-runtime#updates`). GCP-specific launch note: if the build fails with `Killed` or `exit code 137` during `pnpm install --frozen-lockfile`, the VM is out of memory — use `e2-small` minimum, or `e2-medium` for more reliable first builds. When binding to LAN (`OPENCLAW_GATEWAY_BIND=lan`), configure a trusted browser origin before continuing by running `docker compose run --rm openclaw-cli config set gateway.controlUi.allowedOrigins '["http://127.0.0.1:18789"]' --strict-json` (replace `18789` with your configured port if changed).

## Access from your laptop (SSH tunnel)

Create an SSH tunnel to forward the Gateway port, then open `http://127.0.0.1:18789/` in your browser. Reprint a clean dashboard link with `docker compose run --rm openclaw-cli dashboard --no-open`. If the UI prompts for shared-secret auth, paste the configured token or password into Control UI settings (this Docker flow writes a token by default; if you switch the container config to password auth, use that password instead). If Control UI shows `unauthorized` or `disconnected (1008): pairing required`, approve the browser device.

```bash
gcloud compute ssh openclaw-gateway --zone=us-central1-a -- -L 18789:127.0.0.1:18789
# then, if pairing is required:
docker compose run --rm openclaw-cli devices list
docker compose run --rm openclaw-cli devices approve <requestId>
```

For the shared persistence and update reference again, the source links the `oc_install_docker_vm_runtime` "what persists where" section (source: `/install/docker-vm-runtime#what-persists-where`) and its updates section (source: `/install/docker-vm-runtime#updates`).

## Troubleshooting

The source lists three GCP issues. **SSH connection refused** — SSH key propagation can take 1–2 minutes after VM creation; wait and retry. **OS Login issues** — check your OS Login profile with `gcloud compute os-login describe-profile`, and ensure your account has the required IAM permissions (Compute OS Login or Compute OS Admin Login). **Out of memory (OOM)** — if the Docker build fails with `Killed` and `exit code 137`, the VM was OOM-killed; upgrade to `e2-small` (minimum) or `e2-medium` (recommended for reliable local builds) by stopping the VM, changing the machine type, and starting it again.

```bash
gcloud compute instances stop openclaw-gateway --zone=us-central1-a
gcloud compute instances set-machine-type openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small
gcloud compute instances start openclaw-gateway --zone=us-central1-a
```

## Service accounts (security best practice)

For personal use, your default user account works fine. For automation or CI/CD pipelines, create a dedicated service account with minimal permissions: create the account with `gcloud iam service-accounts create openclaw-deploy --display-name="OpenClaw Deployment"`, then grant the Compute Instance Admin role (or a narrower custom role) by binding `serviceAccount:openclaw-deploy@my-openclaw-project.iam.gserviceaccount.com` to `roles/compute.instanceAdmin.v1` on the project. **Avoid using the Owner role for automation; use the principle of least privilege.** See [cloud.google.com/iam/docs/understanding-roles](https://cloud.google.com/iam/docs/understanding-roles) for IAM role details.

## Next steps

The source points to: set up messaging channels (`/channels`); pair local devices as nodes (`/nodes`); and configure the Gateway (`/gateway/configuration`). The Related section also links the Install overview (`/install`), Azure (`/install/azure`), and VPS hosting (`/vps`).

**Source**: OpenClaw documentation — `install/gcp` (mirror `inbox/openclaw_docs/install/gcp.md`)
**Last Updated**: 2026-06-22
**Status**: Active
