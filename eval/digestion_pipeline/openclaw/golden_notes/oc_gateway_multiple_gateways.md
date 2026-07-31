---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - multi_gateway
keywords:
  - openclaw multiple gateways
  - rescue bot profile
  - gateway profile isolation
  - openclaw state dir config path
  - derived browser cdp ports
  - gateway status deep probe
  - per-profile base port
topics:
  - OpenClaw
  - Gateway
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/multiple-gateways
access_control_group: ["general"]
---

# OpenClaw — Running Multiple Gateways on One Host

## Overview

This note is the procedure for running more than one OpenClaw Gateway on a single host with isolated profiles, state, workspaces, and ports — mirroring the `gateway/multiple-gateways` source page. The source page's guidance is that most setups should use one Gateway, because a single Gateway can handle multiple messaging connections and agents; you run separate Gateways only when you need stronger isolation or redundancy (for example, a rescue bot). The note covers the recommended rescue-bot setup, the rescue-bot quickstart, why the isolation works, what `--profile rescue onboard` changes, the general multi-gateway profile pattern, the per-instance isolation checklist, the derived browser/canvas/CDP port mapping, the common browser/CDP footgun, a manual environment-variable example, and the quick verification checks (`gateway status --deep`, `gateway probe`).

## Best recommended setup

For most users, the simplest rescue-bot setup is to keep the main bot on the default profile, run the rescue bot on `--profile rescue`, use a completely separate Telegram bot for the rescue account, and keep the rescue bot on a different base port such as `19789`. This keeps the rescue bot isolated from the main bot so it can debug or apply config changes if the primary bot is down. Leave at least 20 ports between base ports so the derived browser/canvas/CDP ports never collide.

## Rescue-Bot Quickstart

Use this as the default path unless you have a strong reason to do something else:

```bash
# Rescue bot (separate Telegram bot, separate profile, port 19789)
openclaw --profile rescue onboard
openclaw --profile rescue gateway install --port 19789
```

If your main bot is already running, that is usually all you need. During `openclaw --profile rescue onboard`, the source instructs you to use the separate Telegram bot token, keep the `rescue` profile, use a base port at least 20 higher than the main bot, and accept the default rescue workspace unless you already manage one yourself. If onboarding already installed the rescue service for you, the final `gateway install` is not needed.

## Why this works

The rescue bot stays independent because it has its own profile/config, state directory, workspace, base port (plus derived ports), and Telegram bot token. For most setups, the source recommends using a completely separate Telegram bot for the rescue profile because it is easy to keep operator-only, has a separate bot token and identity, is independent from the main bot's channel/app install, and gives a simple DM-based recovery path when the main bot is broken.

## What `--profile rescue onboard` Changes

`openclaw --profile rescue onboard` uses the normal onboarding flow, but it writes everything into a separate profile. In practice, that means the rescue bot gets its own config file, state directory, workspace (by default `~/.openclaw/workspace-rescue`), and managed service name. The prompts are otherwise the same as normal onboarding.

## General multi-gateway setup

The rescue-bot layout above is the easiest default, but the same isolation pattern works for any pair or group of Gateways on one host. For a more general setup, give each extra Gateway its own named profile and its own base port:

```bash
# main (default profile)
openclaw setup
openclaw gateway --port 18789

# extra gateway
openclaw --profile ops setup
openclaw --profile ops gateway --port 19789
```

If you want both Gateways to use named profiles, that also works:

```bash
openclaw --profile main setup
openclaw --profile main gateway --port 18789

openclaw --profile ops setup
openclaw --profile ops gateway --port 19789
```

Services follow the same pattern — install one service per profile, each on its own port:

```bash
openclaw gateway install
openclaw --profile ops gateway install --port 19789
```

Use the rescue-bot quickstart when you want a fallback operator lane. Use the general profile pattern when you want multiple long-lived Gateways for different channels, tenants, workspaces, or operational roles.

## Isolation checklist

Keep these unique per Gateway instance:

- `OPENCLAW_CONFIG_PATH` — per-instance config file
- `OPENCLAW_STATE_DIR` — per-instance sessions, creds, caches
- `agents.defaults.workspace` — per-instance workspace root
- `gateway.port` (or `--port`) — unique per instance
- derived browser/canvas/CDP ports

If these are shared, you will hit config races and port conflicts.

## Port mapping (derived)

The base port is `gateway.port` (or `OPENCLAW_GATEWAY_PORT` / `--port`). From that base, the source documents the derived port mapping as:

- browser control service port = base + 2 (loopback only)
- canvas host is served on the Gateway HTTP server (same port as `gateway.port`)
- Browser profile CDP ports auto-allocate from `browser.controlPort + 9 .. + 108`

If you override any of these in config or env, you must keep them unique per instance.

## Browser/CDP notes (common footgun)

The source flags the browser/CDP ports as a common footgun when running multiple instances:

- Do **not** pin `browser.cdpUrl` to the same values on multiple instances.
- Each instance needs its own browser control port and CDP range (derived from its gateway port).
- If you need explicit CDP ports, set `browser.profiles.<name>.cdpPort` per instance.
- Remote Chrome: use `browser.profiles.<name>.cdpUrl` (per profile, per instance).

## Manual env example

Instead of named profiles, you can isolate instances purely through environment variables — distinct `OPENCLAW_CONFIG_PATH`, `OPENCLAW_STATE_DIR`, and `--port` per instance:

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/main.json \
OPENCLAW_STATE_DIR=~/.openclaw \
openclaw gateway --port 18789

OPENCLAW_CONFIG_PATH=~/.openclaw/rescue.json \
OPENCLAW_STATE_DIR=~/.openclaw-rescue \
openclaw gateway --port 19789
```

## Quick checks

After bringing up multiple Gateways, verify each instance with the deep status and probe checks (run them per profile):

```bash
openclaw gateway status --deep
openclaw --profile rescue gateway status --deep
openclaw --profile rescue gateway probe
openclaw status
openclaw --profile rescue status
openclaw --profile rescue browser status
```

Interpretation, per the source: `gateway status --deep` helps catch stale launchd/systemd/schtasks services from older installs. `gateway probe` warning text such as `multiple reachable gateway identities detected` is expected only when you intentionally run more than one isolated gateway, or when OpenClaw cannot prove reachable probe targets are the same gateway. An SSH tunnel, proxy URL, or configured remote URL to the same gateway is one gateway with multiple transports, even when transport ports differ.

**Source**: OpenClaw documentation — `gateway/multiple-gateways` (mirror `inbox/openclaw_docs/gateway/multiple-gateways.md`)
**Last Updated**: 2026-06-22
**Status**: Active
