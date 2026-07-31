---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - docker
keywords:
  - openclaw docker vm runtime
  - bake binaries at build time
  - docker compose build up -d
  - what persists where openclaw
  - home node openclaw host mount
  - gog goplaces wacli binaries
  - openclaw vm update flow
  - exit code 137 oom build
topics:
  - OpenClaw
  - Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/docker-vm-runtime
access_control_group: ["general"]
---

# OpenClaw — Docker VM Runtime (Bake, Build, Persist, Update)

## Overview

This note is the **shared Docker-on-VM runtime contract** for long-lived OpenClaw Gateway hosts — the steps reused verbatim by VM-based Docker installs such as GCP, Hetzner, and similar VPS providers. It mirrors the `install/docker-vm-runtime` source page and covers four operations: baking every external skill binary into the image at build time (never at runtime), building and launching the gateway container, the host-volume persistence map ("what persists where"), and the rebuild-and-relaunch update flow. The single governing principle is that the Docker container is **ephemeral** and is not the source of truth — anything installed at runtime is lost on restart, so all long-lived state lives on host-volume mounts and all binaries are baked into the image.

## Bake required binaries into the image

Installing binaries inside a running container is a trap — anything installed at runtime will be lost on restart. **All external binaries required by skills must be installed at image build time.** The source page shows three common binaries only as examples (not a complete list): `gog` (from `gogcli`) for Gmail access, `goplaces` for Google Places, and `wacli` for WhatsApp. You may install as many binaries as needed using the same pattern.

If you add new skills later that depend on additional binaries, you must (1) update the Dockerfile, (2) rebuild the image, and (3) restart the containers.

The example Dockerfile bakes the binaries from `node:24-bookworm`, installs `socat`, downloads each Linux asset with `curl -L ... | tar -xzO <name> > /usr/local/bin/<name>` then `chmod +x`, and builds the app and UI with `corepack enable` + `pnpm install --frozen-lockfile` + `pnpm build` / `pnpm ui:install` / `pnpm ui:build`:

```dockerfile
FROM node:24-bookworm

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Example binary 1: Gmail CLI (gogcli — installs as `gog`)
# Copy the current Linux asset URL from https://github.com/steipete/gogcli/releases
RUN curl -L https://github.com/steipete/gogcli/releases/latest/download/gogcli_linux_amd64.tar.gz \
  | tar -xzO gog > /usr/local/bin/gog; \
  chmod +x /usr/local/bin/gog

# Example binary 2: Google Places CLI
# Copy the current Linux asset URL from https://github.com/steipete/goplaces/releases
RUN curl -L https://github.com/steipete/goplaces/releases/latest/download/goplaces_linux_amd64.tar.gz \
  | tar -xzO goplaces > /usr/local/bin/goplaces; \
  chmod +x /usr/local/bin/goplaces

# Example binary 3: WhatsApp CLI
# Copy the current Linux asset URL from https://github.com/steipete/wacli/releases
RUN curl -L https://github.com/steipete/wacli/releases/latest/download/wacli-linux-amd64.tar.gz \
  | tar -xzO wacli > /usr/local/bin/wacli; \
  chmod +x /usr/local/bin/wacli

# Add more binaries below using the same pattern

WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN corepack enable
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

The source adds a note that the URLs above are examples: for ARM-based VMs, choose the `arm64` assets, and for reproducible builds, pin versioned release URLs.

## Build and launch

Build the image and start the gateway service detached:

```bash
docker compose build
docker compose up -d openclaw-gateway
```

If the build fails with `Killed` or `exit code 137` during `pnpm install --frozen-lockfile`, the VM is **out of memory** — use a larger machine class before retrying. After launch, verify the baked binaries resolve inside the container, then verify the gateway is listening:

```bash
docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli
```

Expected output is the baked paths `/usr/local/bin/gog`, `/usr/local/bin/goplaces`, and `/usr/local/bin/wacli`. Tailing the gateway logs with `docker compose logs -f openclaw-gateway` should show the listen line `[gateway] listening on ws://0.0.0.0:18789`.

## What persists where

OpenClaw runs in Docker, but Docker is **not** the source of truth: all long-lived state must survive restarts, rebuilds, and reboots. State is split between host-volume mounts (durable) and the Docker image / container filesystem (rebuilt or ephemeral). The source persistence table:

| Component           | Location                                               | Persistence mechanism  | Notes                                                         |
| ------------------- | ------------------------------------------------------ | ---------------------- | ------------------------------------------------------------- |
| Gateway config      | `/home/node/.openclaw/`                                | Host volume mount      | Includes `openclaw.json`, `.env`                              |
| Model auth profiles | `/home/node/.openclaw/agents/`                         | Host volume mount      | `agents/<agentId>/agent/auth-profiles.json` (OAuth, API keys) |
| Auth profile key    | `/home/node/.config/openclaw/`                         | Host volume mount      | Local encryption key for OAuth auth profile token material    |
| Skill configs       | `/home/node/.openclaw/skills/`                         | Host volume mount      | Skill-level state                                             |
| Agent workspace     | `/home/node/.openclaw/workspace/`                      | Host volume mount      | Code and agent artifacts                                      |
| WhatsApp session    | `/home/node/.openclaw/`                                | Host volume mount      | Preserves QR login                                            |
| Gmail keyring       | `/home/node/.openclaw/`                                | Host volume + password | Requires `GOG_KEYRING_PASSWORD`                               |
| Plugin packages     | `/home/node/.openclaw/npm`, `/home/node/.openclaw/git` | Host volume mount      | Downloadable plugin package roots                             |
| External binaries   | `/usr/local/bin/`                                      | Docker image           | Must be baked at build time                                   |
| Node runtime        | Container filesystem                                   | Docker image           | Rebuilt every image build                                     |
| OS packages         | Container filesystem                                   | Docker image           | Do not install at runtime                                     |
| Docker container    | Ephemeral                                              | Restartable            | Safe to destroy                                               |

The dividing line: everything under `/home/node/.openclaw/` (and the auth profile key under `/home/node/.config/openclaw/`) is a host volume mount that outlives the container, while external binaries, the Node runtime, and OS packages belong to the Docker image (rebuilt every build, never installed at runtime), and the container itself is ephemeral and safe to destroy.

## Updates

To update OpenClaw on the VM, pull the latest source, rebuild the image, and relaunch — the host-mounted state under `/home/node/.openclaw/` carries over unchanged:

```bash
git pull
docker compose build
docker compose up -d
```

**Source**: OpenClaw documentation — `install/docker-vm-runtime` (mirror `inbox/openclaw_docs/install/docker-vm-runtime.md`)
**Last Updated**: 2026-06-22
**Status**: Active
