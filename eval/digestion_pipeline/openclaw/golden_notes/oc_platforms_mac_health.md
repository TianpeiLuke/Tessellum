---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - health
keywords:
  - openclaw macos health
  - baileys health status dot
  - openclaw health --json probe
  - shellexecutor health probe
  - health card settings
  - channels tab whatsapp telegram
  - cached snapshot offline fallback
  - run health check menu item
topics:
  - OpenClaw
  - macOS App Health
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/mac/health
access_control_group: ["general"]
---

# OpenClaw — macOS App Health Checks (Linked-Channel / Baileys Status)

## Overview

This note is the procedure for seeing whether the linked channel is healthy from the OpenClaw **macOS menu bar app**, mirroring the `platforms/mac/health` source page. It covers the four surfaces the app uses to report Gateway/Baileys health: the menu-bar status dot (Green/Orange/Red) plus its secondary line and "Run Health Check" item; the Settings General-tab Health card and the Channels-tab per-channel controls; how the periodic `openclaw health --json` probe runs via `ShellExecutor` (~60s and on demand) with a cached-snapshot anti-flicker design; and the CLI fallback flow to use "when in doubt". Every command, label, color, path, and timing below is reproduced verbatim from the source page.

## Menu bar

The menu-bar status dot reflects **Baileys health**, with three colors:

- **Green**: linked + socket opened recently.
- **Orange**: connecting/retrying.
- **Red**: logged out or probe failed.

Below the dot, a secondary line reads `"linked · auth 12m"` (a healthy linked state with the auth age) or shows the failure reason when unhealthy. The menu also exposes a **"Run Health Check"** menu item, which triggers an on-demand probe (the same probe described in "How the probe works", run immediately rather than waiting for the next periodic cycle).

## Settings

Two Settings tabs surface health:

- **General tab** gains a **Health card** showing: linked auth age, session-store path/count, last check time, last error/status code, and buttons for **Run Health Check** / **Reveal Logs**. The card uses a cached snapshot so the UI loads instantly and falls back gracefully when offline (it renders the last good snapshot rather than blocking on a live probe).
- **Channels tab** surfaces channel status + controls for **WhatsApp/Telegram**: login QR, logout, probe, and last disconnect/error.

## How the probe works

The app runs `openclaw health --json` via `ShellExecutor` every **~60s and on demand**. The probe loads creds and reports status **without sending messages** (it is a read-only liveness check, not a message round-trip). To avoid flicker, the app caches the **last good snapshot** and the **last error** separately, and shows the timestamp of each — so a single transient probe failure does not blank out a previously-healthy display, and a recovered probe does not erase the last-error context.

## When in doubt

If the menu-bar/Settings indicators are inconclusive, fall back to the CLI flow documented in the Gateway health reference (the external Gateway-health doc linked below and the sibling `oc_gateway_health` note):

- `openclaw status`
- `openclaw status --deep`
- `openclaw health --json`

Additionally, tail `/tmp/openclaw/openclaw-*.log` for `web-heartbeat` / `web-reconnect` lines to watch the live socket liveness/reconnect activity directly.

**Source**: OpenClaw documentation — `platforms/mac/health` (mirror `inbox/openclaw_docs/platforms/mac/health.md`)
**Last Updated**: 2026-06-22
**Status**: Active
