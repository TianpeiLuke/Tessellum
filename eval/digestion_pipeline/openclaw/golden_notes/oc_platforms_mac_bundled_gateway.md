---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - macos
keywords:
  - openclaw macos gateway
  - external openclaw cli install
  - launchd launchagent gateway
  - ai.openclaw.gateway plist
  - openclaw gateway install
  - gateway version compatibility
  - gateway smoke check health
  - openclaw skip channels canvas host
topics:
  - OpenClaw
  - Platforms
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/mac/bundled-gateway
access_control_group: ["general"]
---

# OpenClaw — Gateway on macOS (External CLI + launchd LaunchAgent)

## Overview

This note is the procedure for running the OpenClaw Gateway on macOS, mirroring the `platforms/mac/bundled-gateway` source page. The headline change it documents: OpenClaw.app no longer bundles Node/Bun or the Gateway runtime — the macOS app instead expects an **external** `openclaw` CLI install, does not spawn the Gateway as a child process, and manages a per-user launchd service to keep the Gateway running (or attaches to an existing local Gateway if one is already running). It covers four operational steps: installing the global CLI (required for local mode), the launchd LaunchAgent (label, plist location, manager, behavior, logging), the app↔gateway version-compatibility check, and the smoke-check commands.

## Install the CLI (required for local mode)

Node 24 is the default runtime on the Mac. Node 22 LTS, currently `22.19+`, still works for compatibility. Then install `openclaw` globally:

```bash
npm install -g openclaw@<version>
```

The macOS app's **Install CLI** button runs the same global install flow the app uses internally: it prefers npm first, then pnpm, then bun if that is the only detected package manager. Node remains the recommended Gateway runtime.

## Launchd (Gateway as LaunchAgent)

**Label** — the LaunchAgent is labeled `ai.openclaw.gateway` (or `ai.openclaw.<profile>`; legacy `com.openclaw.*` may remain).

**Plist location (per-user)** — `~/Library/LaunchAgents/ai.openclaw.gateway.plist` (or `~/Library/LaunchAgents/ai.openclaw.<profile>.plist`).

**Manager** — the macOS app owns LaunchAgent install/update in Local mode. The CLI can also install it: `openclaw gateway install`.

**Behavior:**

- "OpenClaw Active" enables/disables the LaunchAgent.
- App quit does **not** stop the gateway (launchd keeps it alive).
- If a Gateway is already running on the configured port, the app attaches to it instead of starting a new one.

**Logging:**

- launchd stdout: `~/Library/Logs/openclaw/gateway.log` (profiles use `gateway-<profile>.log`).
- launchd stderr: suppressed.

## Version compatibility

The macOS app checks the gateway version against its own version. If they're incompatible, update the global CLI to match the app version.

## Smoke check

First check the installed CLI version, then start a throwaway loopback-bound Gateway on a non-default port with channels and the Canvas host skipped:

```bash
openclaw --version

OPENCLAW_SKIP_CHANNELS=1 \
OPENCLAW_SKIP_CANVAS_HOST=1 \
openclaw gateway --port 18999 --bind loopback
```

Then call the health endpoint against that loopback Gateway over WebSocket:

```bash
openclaw gateway call health --url ws://127.0.0.1:18999 --timeout 3000
```

**Source**: OpenClaw documentation — `platforms/mac/bundled-gateway` (mirror `inbox/openclaw_docs/platforms/mac/bundled-gateway.md`)
**Last Updated**: 2026-06-22
**Status**: Active
