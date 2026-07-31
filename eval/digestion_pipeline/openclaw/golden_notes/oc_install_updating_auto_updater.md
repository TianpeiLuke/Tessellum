---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - auto_updater
keywords:
  - openclaw auto-updater
  - update.auto config schema
  - stable beta dev channel behavior
  - stableDelayHours stableJitterHours
  - betaCheckIntervalHours
  - OPENCLAW_NO_AUTO_UPDATE
  - update.checkOnStart
  - control-plane detached handoff
topics:
  - OpenClaw
  - Auto-updater
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/install/updating
access_control_group: ["general"]
---

# OpenClaw — Auto-Updater Configuration Model

## Overview

This note models the OpenClaw **auto-updater**: the configuration-driven self-update mechanism declared in the `update.auto` JSON5 block of `~/.openclaw/openclaw.json`. It mirrors the "Auto-updater" section of the `install/updating` source page and covers the config schema (`enabled`, `stableDelayHours`, `stableJitterHours`, `betaCheckIntervalHours`), the per-channel apply behavior (stable jittered spread rollout / beta hourly / dev manual-only), the startup update hint (`update.checkOnStart`), the `OPENCLAW_NO_AUTO_UPDATE` override, and the detached control-plane handoff that the Gateway uses to apply package-manager updates out-of-process. The hands-on manual update/rollback steps from the same page are the procedure sibling **[oc_install_updating](oc_install_updating.md)**; this note is the configuration-model half only.

## Default State and Enabling

The auto-updater is **off by default**. It is turned on by adding an `update.auto` block to `~/.openclaw/openclaw.json` (JSON5):

```json5
{
  update: {
    channel: "stable",
    auto: {
      enabled: true,
      stableDelayHours: 6,
      stableJitterHours: 12,
      betaCheckIntervalHours: 1,
    },
  },
}
```

The `update.channel` field selects which release channel the auto-updater follows (`stable`, `beta`, or `dev`), and the nested `update.auto` object holds the apply-timing parameters. The values shown above are the source page's documented example settings — the page does not state independent built-in defaults for `stableDelayHours` or `stableJitterHours`. The one explicit default the source gives is for `betaCheckIntervalHours`, which defaults to hourly.

## Per-Channel Apply Behavior

The configured `update.channel` determines how (and whether) the auto-updater applies a new release once `update.auto.enabled` is true:

| Channel  | Behavior |
| -------- | -------- |
| `stable` | Waits `stableDelayHours`, then applies with deterministic jitter across `stableJitterHours` (spread rollout). |
| `beta`   | Checks every `betaCheckIntervalHours` (default: hourly) and applies immediately. |
| `dev`    | No automatic apply. Use `openclaw update` manually. |

The `stable` channel deliberately delays and then staggers application across the jitter window so a fleet does not all swap to a new release at the same instant — a deterministic spread rollout. The `beta` channel polls on the configured interval and applies as soon as a newer beta is found. The `dev` channel never auto-applies; a moving GitHub `main` checkout is updated only by running `openclaw update` by hand (see the procedure sibling).

## Startup Update Hint and Overrides

Independent of the auto-apply schedule, the Gateway **logs an update hint on startup**. This hint is controlled by `update.checkOnStart`: set `update.checkOnStart: false` to disable the startup hint.

For downgrade or incident recovery, set `OPENCLAW_NO_AUTO_UPDATE=1` in the gateway environment. This blocks automatic applies even when `update.auto.enabled` is configured. The two controls are layered: `OPENCLAW_NO_AUTO_UPDATE=1` stops the automatic *applies*, but **startup update hints can still run** unless `update.checkOnStart` is *also* disabled. So to fully silence both the apply path and the startup hint, an operator disables the auto-apply (via the env var or `update.auto.enabled: false`) and sets `update.checkOnStart: false`.

## Control-Plane Detached Handoff

Package-manager updates requested through the **live Gateway control-plane handler** do *not* replace the package tree inside the running Gateway process — replacing files under the running process would risk loading core or plugin files from a half-swapped package tree. Instead, on managed-service installs the Gateway performs a **detached handoff**: it starts a detached process, exits, and lets the normal `openclaw update --yes --json` CLI path do the work. That CLI path stops the service, replaces the package, refreshes service metadata, restarts, verifies the Gateway version and reachability, and recovers an installed-but-unloaded macOS LaunchAgent when possible.

If the Gateway cannot make that handoff safely, the `update.run` control-plane handler does **not** run the package manager in-process; instead it **reports a safe shell command** for the operator to run manually. This keeps the in-process Gateway from ever mutating its own live package tree, deferring the actual swap to the out-of-process CLI path or to the operator.

**Source**: OpenClaw documentation — `install/updating` (Auto-updater section) (mirror `inbox/openclaw_docs/install/updating.md`)
**Last Updated**: 2026-06-22
**Status**: Active
