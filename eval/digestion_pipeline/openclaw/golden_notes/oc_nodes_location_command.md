---
tags:
  - resource
  - documentation
  - openclaw
  - nodes
  - location
keywords:
  - openclaw location.get node command
  - location enabledMode whileUsing
  - location preciseEnabled toggle
  - node.permissions location grant
  - location.get params response schema
  - location stable error codes
  - android foreground location only
  - nodes tool location_get action
topics:
  - OpenClaw
  - Node Location Command
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/nodes/location-command
access_control_group: ["general"]
---

# OpenClaw — The `location.get` Node Command

## Overview

This note documents the OpenClaw **`location.get` node command** procedure: how a paired device node exposes its current location to the agent through the Gateway `node.invoke` surface, with location off by default and gated behind a selector plus a separate Precise toggle. It covers the privacy rationale for using a selector instead of a switch, the per-node settings model (`location.enabledMode` / `location.preciseEnabled`), the OS-permission mapping via `node.permissions`, the `location.get` request params, response payload, and stable error codes, Android foreground-only behavior, the `nodes` tool `location_get` action and CLI helper, and suggested UX copy — mirroring the `nodes/location-command` source page. The page embeds a small request/response schema as a sub-section, but the dominant building block is the procedure of invoking the command.

## TL;DR

- `location.get` is a node command, invoked via `node.invoke`.
- It is **off by default**.
- The Android app settings use a selector: **Off / While Using**.
- A separate toggle controls **Precise Location**.

## Why a Selector (Not Just a Switch)

OS location permissions are multi-level, so OpenClaw exposes a selector in-app, but the OS still decides the actual grant. The platform behaviors that motivate the selector are:

- iOS/macOS may expose **While Using** or **Always** in system prompts/Settings.
- The Android app currently supports **foreground location only**.
- Precise location is a **separate grant** (iOS 14+ "Precise", Android "fine" vs "coarse").

The selector in the UI drives the *requested* mode, while the *actual* grant lives in OS settings. This is the source page's core design point: requested mode and granted mode are distinct, and the OS grant always wins.

## Settings Model

The location settings are stored per node device:

- `location.enabledMode`: `off | whileUsing`
- `location.preciseEnabled`: bool

The documented UI behavior around these settings:

- Selecting `whileUsing` requests foreground permission.
- If the OS denies the requested level, the app reverts to the **highest granted level** and shows status.

## Permissions Mapping (`node.permissions`)

Reporting location through the permissions map is **optional**. The macOS node reports `location` via the `node.permissions` map; iOS/Android may omit it.

## Command: `location.get`

`location.get` is called via `node.invoke`.

**Params (suggested):**

```json
{
  "timeoutMs": 10000,
  "maxAgeMs": 15000,
  "desiredAccuracy": "coarse|balanced|precise"
}
```

**Response payload:**

```json
{
  "lat": 48.20849,
  "lon": 16.37208,
  "accuracyMeters": 12.5,
  "altitudeMeters": 182.0,
  "speedMps": 0.0,
  "headingDeg": 270.0,
  "timestamp": "2026-01-03T12:34:56.000Z",
  "isPrecise": true,
  "source": "gps|wifi|cell|unknown"
}
```

**Errors (stable codes):**

- `LOCATION_DISABLED`: selector is off.
- `LOCATION_PERMISSION_REQUIRED`: permission missing for requested mode.
- `LOCATION_BACKGROUND_UNAVAILABLE`: app is backgrounded but only While Using allowed.
- `LOCATION_TIMEOUT`: no fix in time.
- `LOCATION_UNAVAILABLE`: system failure / no providers.

## Background Behavior

- The Android app denies `location.get` while backgrounded.
- Keep OpenClaw open when requesting location on Android.
- Other node platforms may differ.

## Model / Tooling Integration

- **Tool surface**: the `nodes` tool adds a `location_get` action (a node is required).
- **CLI**: `openclaw nodes location get --node <id>`.
- **Agent guidelines**: only call `location_get` when the user has enabled location and understands the scope.

## UX Copy (Suggested)

The source page suggests the following user-facing copy for each setting state:

- **Off**: "Location sharing is disabled."
- **While Using**: "Only when OpenClaw is open."
- **Precise**: "Use precise GPS location. Toggle off to share approximate location."

**Source**: OpenClaw documentation — `nodes/location-command` (mirror `inbox/openclaw_docs/nodes/location-command.md`)
**Last Updated**: 2026-06-22
**Status**: Active
