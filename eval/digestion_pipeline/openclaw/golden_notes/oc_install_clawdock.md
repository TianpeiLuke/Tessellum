---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - clawdock
keywords:
  - clawdock shell helpers
  - docker-based openclaw install
  - clawdock-start clawdock-dashboard
  - clawdock-fix-token gateway token
  - clawdock-devices clawdock-approve pairing
  - clawdock-show-config redacted secrets
  - openclaw docker config split
  - clawdock-helpers.sh
topics:
  - OpenClaw
  - Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/clawdock
access_control_group: ["general"]
---

# OpenClaw — Installing and Using ClawDock (Docker Shell Helpers)

## Overview

This note is the install/use procedure for **ClawDock**, a small shell-helper layer for Docker-based OpenClaw installs that gives short commands like `clawdock-start`, `clawdock-dashboard`, and `clawdock-fix-token` instead of longer `docker compose ...` invocations. It mirrors the `install/clawdock` source page: the canonical helper-path install, the full `clawdock-*` command catalog (basic operations, container access, web UI + pairing, setup + maintenance, utilities), the first-time pairing flow, and the Docker config/secrets split ClawDock works against. ClawDock assumes Docker is already set up — if not, the source page directs you to the [Docker](https://docs.openclaw.ai/install/docker) install first (owned by another sub-plan; linked, not duplicated here).

## Install

Use the canonical helper path — create the `~/.clawdock` directory, download the helper script with `curl`, then source it from your shell rc:

```bash
mkdir -p ~/.clawdock && curl -sL https://raw.githubusercontent.com/openclaw/openclaw/main/scripts/clawdock/clawdock-helpers.sh -o ~/.clawdock/clawdock-helpers.sh
echo 'source ~/.clawdock/clawdock-helpers.sh' >> ~/.zshrc && source ~/.zshrc
```

If you previously installed ClawDock from `scripts/shell-helpers/clawdock-helpers.sh`, reinstall from the new `scripts/clawdock/clawdock-helpers.sh` path; the old raw GitHub path was removed.

## What you get

The helper layer registers the following `clawdock-*` commands, grouped by purpose. Descriptions are reproduced verbatim from the source command tables.

### Basic operations

| Command | Description |
| --- | --- |
| `clawdock-start` | Start the gateway |
| `clawdock-stop` | Stop the gateway |
| `clawdock-restart` | Restart the gateway |
| `clawdock-status` | Check container status |
| `clawdock-logs` | Follow gateway logs |

### Container access

| Command | Description |
| --- | --- |
| `clawdock-shell` | Open a shell inside the gateway container |
| `clawdock-cli <command>` | Run OpenClaw CLI commands in Docker |
| `clawdock-exec <command>` | Execute an arbitrary command in the container |

### Web UI and pairing

| Command | Description |
| --- | --- |
| `clawdock-dashboard` | Open the Control UI URL |
| `clawdock-devices` | List pending device pairings |
| `clawdock-approve <id>` | Approve a pairing request |

### Setup and maintenance

| Command | Description |
| --- | --- |
| `clawdock-fix-token` | Configure the gateway token inside the container |
| `clawdock-update` | Pull, rebuild, and restart |
| `clawdock-rebuild` | Rebuild the Docker image only |
| `clawdock-clean` | Remove containers and volumes |

### Utilities

| Command | Description |
| --- | --- |
| `clawdock-health` | Run a gateway health check |
| `clawdock-token` | Print the gateway token |
| `clawdock-cd` | Jump to the OpenClaw project directory |
| `clawdock-config` | Open `~/.openclaw` |
| `clawdock-show-config` | Print config files with redacted values |
| `clawdock-workspace` | Open the workspace directory |

## First-time flow

On first run, start the gateway, configure its token, then open the Control UI:

```bash
clawdock-start
clawdock-fix-token
clawdock-dashboard
```

If the browser says pairing is required, list the pending device pairings and approve the request by its id:

```bash
clawdock-devices
clawdock-approve <request-id>
```

## Config and secrets

ClawDock works with the same Docker config split described in the [Docker](https://docs.openclaw.ai/install/docker) install. The four config/secret locations are:

- `<project>/.env` — Docker-specific values like image name, ports, and the gateway token.
- `~/.openclaw/.env` — env-backed provider keys and bot tokens.
- `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` — stored provider OAuth/API-key auth.
- `~/.openclaw/openclaw.json` — behavior config.

Use `clawdock-show-config` to inspect the `.env` files and `openclaw.json` quickly; it redacts `.env` values in its printed output.

**Source**: OpenClaw documentation — `install/clawdock` (mirror `inbox/openclaw_docs/install/clawdock.md`)
**Last Updated**: 2026-06-22
**Status**: Active
