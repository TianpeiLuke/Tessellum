---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - gateway_service_install
keywords:
  - openclaw platform support
  - node recommended runtime
  - bun not recommended gateway
  - companion apps windows hub macos
  - choose your os
  - gateway service install cli
  - launchagent systemd scheduled task
  - openclaw onboard install-daemon
topics:
  - OpenClaw
  - Platform Support
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms
access_control_group: ["general"]
---

# OpenClaw — Platform Support and Gateway Service Install

## Overview

This note is the platform-support overview procedure for OpenClaw, mirroring the `platforms` source page: it covers the runtime recommendation (TypeScript core, Node recommended, Bun not recommended for the Gateway), the companion-app surface (Windows Hub, macOS menu-bar, iOS/Android nodes), the per-OS picker, the VPS/hosting link-out, the common Gateway links, and the four CLI paths to install the Gateway as an OS service with their per-OS service targets. It mirrors the source page's `(intro)`, `## Choose your OS`, `## VPS and hosting`, `## Common links`, and `## Gateway service install (CLI)` sections; the detailed OS/host/install pages it links to are owned by other note series and are linked, not duplicated.

## Runtime and Companion Apps

OpenClaw core is written in TypeScript, and **Node is the recommended runtime**. Bun is not recommended for the Gateway — the source page cites known issues with WhatsApp and Telegram channels and points to the `Bun (experimental)` install page (`/install/bun`) for details.

Companion apps exist for **Windows Hub**, **macOS** (a menu-bar app), and **mobile nodes** (iOS/Android). Linux companion apps are planned, but the Gateway itself is fully supported on Linux today. On Windows there are three choices: Windows Hub for the desktop app, native PowerShell install for terminal-first use, or WSL2 for the most Linux-compatible Gateway runtime.

## Choose your OS

The per-OS picker links to the dedicated platform pages (owned by other note series; linked, not inlined):

- macOS: `/platforms/macos`
- iOS: `/platforms/ios`
- Android: `/platforms/android`
- Windows: `/platforms/windows`
- Linux: `/platforms/linux`

## VPS and hosting

For running the Gateway on a server, the page links to the VPS hub and per-host install pages:

- VPS hub: `/vps`
- Fly.io: `/install/fly`
- Hetzner (Docker): `/install/hetzner`
- GCP (Compute Engine): `/install/gcp`
- Azure (Linux VM): `/install/azure`
- exe.dev (VM + HTTPS proxy): `/install/exe-dev`
- EasyRunner (Podman + Caddy): `/platforms/easyrunner`

## Common links

The page surfaces a set of common Gateway links and one status command:

- Install guide: `/start/getting-started`
- Windows Hub: `/platforms/windows`
- Gateway runbook: `/gateway`
- Gateway configuration: `/gateway/configuration`
- Service status: `openclaw gateway status`

## Gateway service install (CLI)

To install the Gateway as a managed OS service, use one of these four CLI paths (all supported):

- Wizard (recommended): `openclaw onboard --install-daemon`
- Direct: `openclaw gateway install`
- Configure flow: `openclaw configure` → select **Gateway service**
- Repair/migrate: `openclaw doctor` (offers to install or fix the service)

### Service target per OS

The service target the install path creates depends on the OS:

- macOS: LaunchAgent (`ai.openclaw.gateway` or `ai.openclaw.<profile>`; legacy `com.openclaw.*`).
- Linux/WSL2: systemd user service (`openclaw-gateway[-<profile>].service`).
- Native Windows: Scheduled Task (`OpenClaw Gateway` or `OpenClaw Gateway (<profile>)`), with a per-user Startup-folder login item fallback if task creation is denied.

**Source**: OpenClaw documentation — `platforms` (mirror `inbox/openclaw_docs/platforms.md`)
**Last Updated**: 2026-06-22
**Status**: Active
