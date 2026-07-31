---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - macos
keywords:
  - openclaw macos dev setup
  - build openclaw mac app from source
  - package-mac-app.sh ad-hoc signing
  - install openclaw cli globally
  - xcode 26.2 swift 6.2 toolchain
  - tccutil reset ai.openclaw.mac.debug
  - gateway starting zombie port 18789
  - pnpm install openclaw
topics:
  - OpenClaw
  - macOS Developer Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/mac/dev-setup
access_control_group: ["general"]
---

# OpenClaw — macOS Developer Setup (Build, Package, and Run From Source)

## Overview

This note is the **procedure** for building and running the OpenClaw macOS application (`apps/macos`) from source, mirroring the `platforms/mac/dev-setup` source page. It covers the toolchain prerequisites (Xcode 26.2+, Node.js 24 & pnpm), installing project-wide dependencies, building/packaging the app into `dist/OpenClaw.app` with `package-mac-app.sh` (which falls back to ad-hoc signing), installing the global `openclaw` CLI the app needs for background tasks, and three troubleshooting recipes — toolchain/SDK mismatch, a permission-grant crash, and a Gateway stuck on "Starting...". Every command, path, bundle ID, and port below is reproduced verbatim from the source page.

## Prerequisites

Before building the app, ensure the following are installed:

1. **Xcode 26.2+** — required for Swift development.
2. **Node.js 24 & pnpm** — recommended for the gateway, CLI, and packaging scripts. Node 22 LTS, currently `22.19+`, remains supported for compatibility.

## 1. Install Dependencies

Install the project-wide dependencies:

```bash
pnpm install
```

## 2. Build and Package the App

To build the macOS app and package it into `dist/OpenClaw.app`, run the packaging script:

```bash
./scripts/package-mac-app.sh
```

If you don't have an Apple Developer ID certificate, the script automatically uses **ad-hoc signing** (`-`). For dev run modes, signing flags, and Team ID troubleshooting, the source page refers to the macOS app README at `https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md`. The page also warns that ad-hoc-signed apps may trigger security prompts, and that if the app crashes immediately with "Abort trap 6" you should consult the Troubleshooting section below.

## 3. Install the CLI

The macOS app expects a **global `openclaw` CLI install** to manage background tasks. The recommended in-app path is: open the OpenClaw app, go to the **General** settings tab, and click **"Install CLI"**. Alternatively, install it manually:

```bash
npm install -g openclaw@<version>
```

The source page notes that `pnpm add -g openclaw@<version>` and `bun add -g openclaw@<version>` also work, and that for the Gateway runtime **Node remains the recommended path**.

## Troubleshooting

The source page documents three recipes for the most common dev-setup failures.

### Build fails: toolchain or SDK mismatch

The macOS app build expects the latest macOS SDK and the Swift 6.2 toolchain. The required system dependencies are the **latest macOS version available in Software Update** (required by the Xcode 26.2 SDKs) and **Xcode 26.2** (Swift 6.2 toolchain). Verify the installed versions:

```bash
xcodebuild -version
xcrun swift --version
```

If the versions don't match, update macOS/Xcode and re-run the build.

### App crashes on permission grant

If the app crashes when you try to allow **Speech Recognition** or **Microphone** access, the page attributes it to a corrupted TCC cache or signature mismatch. The fix is to reset the TCC permissions for the debug bundle:

```bash
tccutil reset All ai.openclaw.mac.debug
```

If that fails, the page advises temporarily changing the `BUNDLE_ID` in `scripts/package-mac-app.sh` (`https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh`) to force a "clean slate" from macOS.

### Gateway "Starting..." indefinitely

If the gateway status stays on "Starting...", check whether a zombie process is holding the port. Query and stop the gateway, then — only when not using a LaunchAgent (dev mode / manual runs) — find the listener on port `18789`:

```bash
openclaw gateway status
openclaw gateway stop

# If you're not using a LaunchAgent (dev mode / manual runs), find the listener:
lsof -nP -iTCP:18789 -sTCP:LISTEN
```

If a manual run is holding the port, stop that process with `Ctrl+C`; as a last resort, kill the PID found above.

**Source**: OpenClaw documentation — `platforms/mac/dev-setup` (mirror `inbox/openclaw_docs/platforms/mac/dev-setup.md`)
**Last Updated**: 2026-06-22
**Status**: Active
