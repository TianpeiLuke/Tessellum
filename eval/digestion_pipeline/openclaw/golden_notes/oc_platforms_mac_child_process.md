---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - macos
keywords:
  - openclaw gateway lifecycle macos
  - launchd ai.openclaw.gateway launchagent
  - attach-only no-launchd mode
  - remote mode ssh tunnel gateway
  - disable-launchagent unsigned dev build
  - launchctl kickstart bootout
  - child-process mode not in use
topics:
  - OpenClaw
  - macOS Platform
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/mac/child-process
access_control_group: ["general"]
---

# OpenClaw — macOS Gateway Lifecycle (launchd, Attach-Only, Remote)

## Overview

This note documents the procedure by which the OpenClaw **macOS app manages the Gateway lifecycle**, mirroring the `platforms/mac/child-process` source page. By default the app does NOT spawn the Gateway as a child process; instead it attaches to an already-running Gateway and otherwise enables a per-user **launchd** service (`ai.openclaw.gateway`) via the external `openclaw` CLI. It covers the default attach-then-launchd flow, the common `launchctl` commands, the `--no-sign` unsigned-dev-build override that disables the LaunchAgent, attach-only and remote (SSH-tunnel) modes, and why launchd is preferred over a true child-process mode (which is not in use today).

## Default behavior (launchd)

The macOS app **manages the Gateway via launchd** by default and does not spawn the Gateway as a child process. It first tries to **attach to an already-running Gateway** on the configured port; if none is reachable, it enables the launchd service via the external `openclaw` CLI (no embedded runtime). This gives reliable auto-start at login and restart on crashes. Specifically:

- The app installs a per-user **LaunchAgent labeled `ai.openclaw.gateway`** (or `ai.openclaw.<profile>` when using `--profile`/`OPENCLAW_PROFILE`; legacy `com.openclaw.*` is supported).
- When **Local mode** is enabled, the app ensures the LaunchAgent is loaded and starts the Gateway if needed.
- Logs are written to the launchd gateway log path (visible in **Debug Settings**).

Common commands to kickstart (start/restart) or bootout (stop/unload) the service:

```bash
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
launchctl bootout gui/$UID/ai.openclaw.gateway
```

Replace the label with `ai.openclaw.<profile>` when running a named profile.

## Unsigned dev builds

`scripts/restart-mac.sh --no-sign` is for fast local builds when you do not have signing keys. To prevent launchd from pointing at an unsigned relay binary, it:

- Writes `~/.openclaw/disable-launchagent`.

Signed runs of `scripts/restart-mac.sh` clear this override if the marker is present. To reset the override manually, remove the marker file:

```bash
rm ~/.openclaw/disable-launchagent
```

## Attach-only mode

To force the macOS app to **never install or manage launchd**, launch it with `--attach-only` (or the equivalent `--no-launchd`). This sets `~/.openclaw/disable-launchagent`, so the app only attaches to an already-running Gateway. The same behavior can be toggled in **Debug Settings**.

## Remote mode

Remote mode **never starts a local Gateway**. The app uses an **SSH tunnel** to the remote host and connects over that tunnel.

## Why we prefer launchd

The page gives three reasons launchd is preferred over a true child-process mode:

- **Auto-start at login.**
- **Built-in restart/KeepAlive semantics.**
- **Predictable logs and supervision.**

Child-process mode (the Gateway spawned directly by the app) is **not in use** today; if you need tighter coupling to the UI, run the Gateway manually in a terminal. If a true child-process mode is ever needed again, it should be documented as a separate, explicit **dev-only** mode.

**Source**: OpenClaw documentation — `platforms/mac/child-process` (mirror `inbox/openclaw_docs/platforms/mac/child-process.md`)
**Last Updated**: 2026-06-22
**Status**: Active
