---
tags:
  - resource
  - documentation
  - openclaw
  - start
  - setup
keywords:
  - openclaw advanced setup
  - openclaw developer workflow
  - pnpm gateway:watch
  - openclaw stable vs bleeding edge
  - openclaw credential storage map
  - openclaw config outside repo
  - openclaw systemd user service linger
  - openclaw.json workspace tailoring
topics:
  - OpenClaw
  - Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/start/setup
access_control_group: ["general"]
---

# OpenClaw — Advanced and Developer Setup Workflows

## Overview

This note is the OpenClaw advanced + developer **setup procedure**: how to pick a setup workflow, keep your tailoring outside the repo so updates do not break it, run the Gateway yourself from a source checkout, and know where every credential and state file lives. It mirrors the `start/setup` source page (9 H2 + 5 H3), covering the TL;DR decision, prereqs, the tailoring strategy, running the Gateway from this repo, the stable (macOS-app-first) workflow, the bleeding-edge (`pnpm gateway:watch`) workflow with its 4 numbered steps and footguns, the credential storage map, updating without wrecking your setup, and the Linux systemd-user-service lingering note. First-time users should start with Getting Started; this page is for setting up a new machine or running the latest dev build alongside a stable personal setup.

## TL;DR

Pick a setup workflow based on how often you want updates and whether you want to run the Gateway yourself:

- **Tailoring lives outside the repo:** keep your config and workspace in `~/.openclaw/openclaw.json` and `~/.openclaw/workspace/` so repo updates don't touch them.
- **Stable workflow (recommended for most):** install the macOS app and let it run the bundled Gateway.
- **Bleeding edge workflow (dev):** run the Gateway yourself via `pnpm gateway:watch`, then let the macOS app attach in Local mode.

## Prereqs (from source)

- Node 24 recommended (Node 22 LTS, currently `22.19+`, still supported).
- `pnpm` required for source checkouts. OpenClaw loads bundled plugins from the `extensions/*` pnpm workspace packages in dev mode, so a root `npm install` does NOT prepare the full source tree.
- Docker (optional; only for containerized setup/e2e — see the Docker install doc).

## Tailoring strategy (so updates do not hurt)

If you want "100% tailored to me" _and_ easy updates, keep your customization in two places outside the repo:

- **Config:** `~/.openclaw/openclaw.json` (JSON/JSON5-ish).
- **Workspace:** `~/.openclaw/workspace` (skills, prompts, memories; make it a private git repo).

Bootstrap once with the setup command. From inside this repo, use the local CLI entry (also `openclaw setup`); if you don't have a global install yet, run it via `pnpm openclaw setup`.

```bash
openclaw setup
```

## Run the Gateway from this repo

After `pnpm build`, you can run the packaged CLI directly:

```bash
node openclaw.mjs gateway --port 18789 --verbose
```

## Stable workflow (macOS app first)

The recommended path for most users — the macOS app manages the bundled Gateway:

1. Install + launch **OpenClaw.app** (menu bar).
2. Complete the onboarding/permissions checklist (TCC prompts).
3. Ensure Gateway is **Local** and running (the app manages it).
4. Link surfaces (example: WhatsApp) with `openclaw channels login`.
5. Sanity check with `openclaw health`.

```bash
openclaw channels login
openclaw health
```

If onboarding is not available in your build: run `openclaw setup`, then `openclaw channels login`, then start the Gateway manually (`openclaw gateway`).

## Bleeding edge workflow (Gateway in a terminal)

Goal: work on the TypeScript Gateway, get hot reload, and keep the macOS app UI attached. The four numbered steps below mirror the source.

### 0) (Optional) Run the macOS app from source too

If you also want the macOS app on the bleeding edge, restart it from source:

```bash
./scripts/restart-mac.sh
```

### 1) Start the dev Gateway

Install dependencies, run the one-time local setup (first run only, or after resetting local OpenClaw config/workspace), then start the watch process:

```bash
pnpm install
# First run only (or after resetting local OpenClaw config/workspace)
pnpm openclaw setup
pnpm gateway:watch
```

`gateway:watch` starts or restarts the Gateway watch process in a named tmux session and auto-attaches from interactive terminals. Non-interactive shells stay detached and print `tmux attach -t openclaw-gateway-watch-main`; use `OPENCLAW_GATEWAY_WATCH_ATTACH=0 pnpm gateway:watch` to keep an interactive run detached, or `pnpm gateway:watch:raw` for foreground watch mode. The watcher reloads on relevant source, config, and bundled-plugin metadata changes. If the watched Gateway exits during startup, `gateway:watch` runs `openclaw doctor --fix --non-interactive` once and retries; set `OPENCLAW_GATEWAY_WATCH_AUTO_DOCTOR=0` to disable that dev-only repair pass. `pnpm openclaw setup` is the one-time local config/workspace initialization step for a fresh checkout. `pnpm gateway:watch` does not rebuild `dist/control-ui`, so rerun `pnpm ui:build` after `ui/` changes or use `pnpm ui:dev` while developing the Control UI.

### 2) Point the macOS app at your running Gateway

In **OpenClaw.app**, set Connection Mode to **Local**. The app will attach to the running gateway on the configured port.

### 3) Verify

The in-app Gateway status should read **"Using existing gateway …"**, or you can verify via CLI by running `openclaw health` (same command as the stable-workflow sanity check above).

### Common footguns

- **Wrong port:** Gateway WS defaults to `ws://127.0.0.1:18789`; keep app + CLI on the same port.
- **Where state lives:**
  - Channel/provider state: `~/.openclaw/credentials/`
  - Model auth profiles: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
  - Sessions: `~/.openclaw/agents/<agentId>/sessions/`
  - Logs: `/tmp/openclaw/`

## Credential storage map

Use this map when debugging auth or deciding what to back up:

- **WhatsApp**: `~/.openclaw/credentials/whatsapp/<accountId>/creds.json`
- **Telegram bot token**: config/env or `channels.telegram.tokenFile` (regular file only; symlinks rejected)
- **Discord bot token**: config/env or SecretRef (env/file/exec providers)
- **Slack tokens**: config/env (`channels.slack.*`)
- **Pairing allowlists**: `~/.openclaw/credentials/<channel>-allowFrom.json` (default account) and `~/.openclaw/credentials/<channel>-<accountId>-allowFrom.json` (non-default accounts)
- **Model auth profiles**: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- **File-backed secrets payload (optional)**: `~/.openclaw/secrets.json`
- **Legacy OAuth import**: `~/.openclaw/credentials/oauth.json`

More detail is in the Security credential-storage-map section of the gateway docs.

## Updating (without wrecking your setup)

- Keep `~/.openclaw/workspace` and `~/.openclaw/` as "your stuff"; don't put personal prompts/config into the `openclaw` repo.
- Updating source: `git pull` + `pnpm install` + keep using `pnpm gateway:watch`.

## Linux (systemd user service)

Linux installs use a systemd **user** service. By default, systemd stops user services on logout/idle, which kills the Gateway. Onboarding attempts to enable lingering for you (may prompt for sudo). If it's still off, enable it manually:

```bash
sudo loginctl enable-linger $USER
```

For always-on or multi-user servers, consider a **system** service instead of a user service (no lingering needed). See the Gateway runbook for the systemd notes.

**Source**: OpenClaw documentation — `start/setup` (mirror `inbox/openclaw_docs/start/setup.md`)
**Last Updated**: 2026-06-22
**Status**: Active
