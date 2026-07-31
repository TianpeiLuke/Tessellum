---
tags:
  - resource
  - documentation
  - openclaw
  - nodes
  - camera
keywords:
  - openclaw camera capture
  - camera.snap camera.clip camera.list
  - node.invoke camera command
  - camera.enabled ios android macos
  - openclaw nodes camera cli
  - base64 payload guard 5mb
  - camera_disabled node_background_unavailable
  - macos screen recording tcc
topics:
  - OpenClaw
  - Camera Capture
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/nodes/camera
access_control_group: ["general"]
---

# OpenClaw — Camera Capture on iOS / Android / macOS Nodes

## Overview

This note is the procedure for capturing photos and short video clips from paired OpenClaw device nodes — the iOS node, the Android node, and the macOS companion app — so that captured media can feed agent workflows. It mirrors the `nodes/camera` source page: the three `node.invoke` commands (`camera.list`, `camera.snap`, `camera.clip`) with their params and response payloads, the per-platform user setting + Android runtime permissions, the foreground-only requirement, the base64 payload guard, the `openclaw nodes camera` CLI helper, the safety/practical limits, and the macOS OS-level screen-recording capture path. All camera access is gated behind user-controlled settings.

## Capture Surface (all platforms)

Camera capture is available for agent workflows on three node types, each paired to the Gateway and invoked via `node.invoke`:

- **iOS node** (paired via Gateway): capture a photo (`jpg`) or a short video clip (`mp4`, with optional audio) via `node.invoke`.
- **Android node** (paired via Gateway): capture a photo (`jpg`) or a short video clip (`mp4`, with optional audio) via `node.invoke`.
- **macOS app** (node via Gateway): capture a photo (`jpg`) or a short video clip (`mp4`, with optional audio) via `node.invoke`.

All camera access is gated behind **user-controlled settings**. The available commands are `camera.list` (enumerate devices), `camera.snap` (capture a photo), and `camera.clip` (capture a video clip).

## iOS Node

### User setting (default on)

The iOS user controls camera access at iOS Settings tab → **Camera** → **Allow Camera** (`camera.enabled`). The default is **on** — a missing key is treated as enabled. When off, `camera.*` commands return `CAMERA_DISABLED`.

### Commands (via Gateway `node.invoke`)

`camera.list` returns a response payload with `devices`: an array of `{ id, name, position, deviceType }`.

`camera.snap` captures a photo. Its params are:

- `facing`: `front|back` (default: `front`)
- `maxWidth`: number (optional; default `1600` on the iOS node)
- `quality`: `0..1` (optional; default `0.9`)
- `format`: currently `jpg`
- `delayMs`: number (optional; default `0`)
- `deviceId`: string (optional; from `camera.list`)

Its response payload is `format: "jpg"`, `base64: "<...>"`, plus `width` and `height`. Payload guard: photos are recompressed to keep the base64 payload under 5 MB.

`camera.clip` captures a short video clip. Its params are:

- `facing`: `front|back` (default: `front`)
- `durationMs`: number (default `3000`, clamped to a max of `60000`)
- `includeAudio`: boolean (default `true`)
- `format`: currently `mp4`
- `deviceId`: string (optional; from `camera.list`)

Its response payload is `format: "mp4"`, `base64: "<...>"`, plus `durationMs` and `hasAudio`.

### Foreground requirement

Like `canvas.*`, the iOS node only allows `camera.*` commands in the **foreground**. Background invocations return `NODE_BACKGROUND_UNAVAILABLE`.

### CLI helper

The easiest way to get media files is via the CLI helper, which writes decoded media to a temp file and prints the saved path:

```bash
openclaw nodes camera snap --node <id>               # default: both front + back (2 MEDIA lines)
openclaw nodes camera snap --node <id> --facing front
openclaw nodes camera clip --node <id> --duration 3000
openclaw nodes camera clip --node <id> --no-audio
```

Notes: `nodes camera snap` defaults to **both** facings to give the agent both views; output files are temporary (in the OS temp directory) unless you build your own wrapper.

## Android Node

### Android user setting (default on)

The Android user controls camera access at Android Settings sheet → **Camera** → **Allow Camera** (`camera.enabled`). The default is **on** — a missing key is treated as enabled. When off, `camera.*` commands return `CAMERA_DISABLED`.

### Permissions

Android requires runtime permissions: `CAMERA` for both `camera.snap` and `camera.clip`, and `RECORD_AUDIO` for `camera.clip` when `includeAudio=true`. If permissions are missing, the app will prompt when possible; if denied, `camera.*` requests fail with a `*_PERMISSION_REQUIRED` error.

### Android foreground requirement

Like `canvas.*`, the Android node only allows `camera.*` commands in the **foreground**. Background invocations return `NODE_BACKGROUND_UNAVAILABLE`.

### Android commands (via Gateway `node.invoke`)

`camera.list` returns a response payload with `devices`: an array of `{ id, name, position, deviceType }`.

### Payload guard

Photos are recompressed to keep the base64 payload under 5 MB.

## macOS App

### User setting (default off)

The macOS companion app exposes a checkbox at **Settings → General → Allow Camera** (`openclaw.cameraEnabled`). The default is **off**. When off, camera requests return "Camera disabled by user".

### CLI helper (node invoke)

Use the main `openclaw` CLI to invoke camera commands on the macOS node:

```bash
openclaw nodes camera list --node <id>            # list camera ids
openclaw nodes camera snap --node <id>            # prints saved path
openclaw nodes camera snap --node <id> --max-width 1280
openclaw nodes camera snap --node <id> --delay-ms 2000
openclaw nodes camera snap --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --duration 10s          # prints saved path
openclaw nodes camera clip --node <id> --duration-ms 3000      # prints saved path (legacy flag)
openclaw nodes camera clip --node <id> --device-id <id>
openclaw nodes camera clip --node <id> --no-audio
```

Notes: `openclaw nodes camera snap` defaults to `maxWidth=1600` unless overridden; on macOS, `camera.snap` waits `delayMs` (default 2000ms) after warm-up/exposure settle before capturing; photo payloads are recompressed to keep base64 under 5 MB.

## Safety + Practical Limits

Camera and microphone access trigger the usual OS permission prompts (and require usage strings in Info.plist). Video clips are capped (currently `<= 60s`) to avoid oversized node payloads (base64 overhead + message limits).

## macOS Screen Video (OS-level)

For *screen* video (not camera), use the macOS companion:

```bash
openclaw nodes screen record --node <id> --duration 10s --fps 15   # prints saved path
```

This requires macOS **Screen Recording** permission (TCC).

**Source**: OpenClaw documentation — `nodes/camera` (mirror `inbox/openclaw_docs/nodes/camera.md`)
**Last Updated**: 2026-06-22
**Status**: Active
