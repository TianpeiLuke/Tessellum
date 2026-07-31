---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - support_matrix
keywords:
  - openclaw platform model
  - gateway host vs companion node
  - per-os support matrix
  - node recommended runtime bun not recommended
  - gateway service install launchd systemd scheduled task
  - companion node requires running gateway
  - openclaw platform roles
topics:
  - OpenClaw
  - Platforms
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/platforms
access_control_group: ["general"]
---

# OpenClaw — Platform Model: Gateway-Host vs Companion-Node Roles

## Overview

This note models OpenClaw's **platform model** — the recurring role split, runtime recommendation, per-OS support matrix, and gateway-service-install framing that appears on every per-OS Platforms page (`platforms`, `platforms/android`, `platforms/ios`, `platforms/linux`, `platforms/mac/bundled-gateway`). It is the indexable hub for the Platforms series: it defines the two roles a platform can play (**gateway host** vs **companion node**), the recommended TypeScript runtime (Node, not Bun), the per-OS availability matrix, the per-OS gateway-service-install targets, and the shared pair/connect/discover lifecycle every platform note specializes. It does NOT repeat each page's runbook — those are in the per-OS sibling notes; this hub captures only the cross-page model, sourced from the recurring "Platform support overview" / "Support snapshot" / "Requirements" framing.

## The Two Platform Roles

OpenClaw splits every platform into one of two roles, and the distinction is the load-bearing idea of the whole series. The **gateway host** runs the OpenClaw Gateway — the long-lived TypeScript process that owns sessions, channels, and the agent runtime; per `platforms`, "the Gateway is fully supported today" on macOS, Linux, and Windows (via WSL2 or native). A **companion node** is a per-OS client app that connects *to* a Gateway over WebSocket and exposes that OS's capabilities (Canvas, camera, voice, notifications) to the agent; it does not host the Gateway. The mobile apps are node-only: `platforms/android` states "Role: companion node app (Android does not host the Gateway)" with "Gateway required: yes (run it on macOS, Linux, or Windows via WSL2)", and `platforms/ios` lists under **Requirements** a "Gateway running on another device (macOS, Linux, or Windows via WSL2)." macOS and Windows are dual: their desktop apps are companions (macOS is the "menu-bar companion" exposing macOS capabilities as a node) but the same OS can also host the Gateway. So a node always needs a *running Gateway elsewhere*, while a host can run the Gateway with or without a local companion app attached.

## Per-OS Support Matrix

The recurring "Support snapshot" / "Choose your OS" framing resolves to this matrix (all claims sourced verbatim from the platform pages):

| OS | Hosts the Gateway? | Companion / node app | Notes (verbatim) |
|---|---|---|---|
| macOS | Yes (external launchd-managed CLI) | Yes — menu-bar companion app | `OpenClaw.app no longer bundles Node/Bun or the Gateway runtime`; expects an external `openclaw` CLI |
| Linux | Yes — `The Gateway is fully supported on Linux` | Planned — `Native Linux companion apps are planned` | Node recommended; Bun not recommended |
| Windows | Yes — native or WSL2 | Yes — native `Windows Hub` companion app | "choose Windows Hub for the desktop app, native PowerShell install for terminal-first use, or WSL2 for the most Linux-compatible Gateway runtime" |
| iOS | No | Yes — node-only companion | `Gateway running on another device (macOS, Linux, or Windows via WSL2)` |
| Android | No | Yes — node-only companion | `Android does not host the Gateway`; run the Gateway on macOS/Linux/Windows-via-WSL2 |

Beyond per-OS clients, the model also covers **hosted / VPS deployments** of the gateway host: `platforms` links a "VPS and hosting" cluster (Fly.io, Hetzner via Docker, GCP, Azure, exe.dev, and EasyRunner via Podman + Caddy) — these are gateway-host deployments on managed infrastructure, not new roles.

## Runtime Recommendation (Node vs Bun)

The runtime guidance recurs verbatim across `platforms` and `platforms/linux`: "OpenClaw core is written in TypeScript. **Node is the recommended runtime**." Bun is explicitly not recommended for the Gateway because of "known issues with WhatsApp and Telegram channels" (`platforms/linux` phrases it "WhatsApp/Telegram bugs"); see the install page's Bun (experimental) entry for details. The macOS page reinforces this: "Node 24 is the default runtime on the Mac. Node 22 LTS, currently `22.19+`, still works for compatibility", and "Node remains the recommended Gateway runtime." The macOS **Install CLI** flow and the Linux quick path install the CLI globally and prefer npm, then pnpm, then bun only if it is the only detected package manager. This recommendation applies to the **gateway-host** role; companion-node apps are native per-OS builds (Android/iOS app, macOS menu-bar app, Windows Hub) and do not run a TypeScript runtime of their own.

## Gateway Service Install and Per-OS Service Targets

Every gateway-host OS installs the Gateway as a managed background service, and `platforms` documents one CLI surface with four equivalent entry points: the wizard `openclaw onboard --install-daemon` (recommended), the direct `openclaw gateway install`, the `openclaw configure` flow (select **Gateway service**), and `openclaw doctor` for repair/migrate (it "offers to install or fix the service"). The **service target depends on OS**, sourced verbatim from `platforms`:

- macOS: LaunchAgent (`ai.openclaw.gateway` or `ai.openclaw.<profile>`; legacy `com.openclaw.*`)
- Linux/WSL2: systemd user service (`openclaw-gateway[-<profile>].service`)
- Native Windows: Scheduled Task (`OpenClaw Gateway` or `OpenClaw Gateway (<profile>)`), with a per-user Startup-folder login item fallback if task creation is denied

This is why the per-OS notes specialize: `oc_platforms_mac_bundled_gateway` covers the launchd LaunchAgent, `oc_platforms_linux` covers the systemd user unit, and the macOS app "owns LaunchAgent install/update in Local mode." Service status is checked the same way on every host: `openclaw gateway status`.

## Shared Connect / Pair / Discover Lifecycle

Each companion-node platform specializes one shared lifecycle, which is the second reason this hub exists: a node always (1) reaches a Gateway WebSocket — `platforms/android` "Android connects directly to the Gateway WebSocket and uses device pairing (`role: node`)", `platforms/ios` "Connects to a Gateway over WebSocket (LAN or tailnet)"; (2) discovers the Gateway over one of the same three paths — same-LAN mDNS/NSD/Bonjour (`_openclaw-gw._tcp` on `local.`), cross-network unicast DNS-SD over a tailnet (example domain `openclaw.internal.`), or a manual host/port fallback (default port `18789`); (3) pairs as a `role: node` device that an operator approves with `openclaw devices list` / `openclaw devices approve <requestId>` (with optional `gateway.nodes.pairing.autoApproveCidrs` for a tightly-controlled subnet); and (4) reports liveness via `node.event` with `event: "node.presence.alive"`. Secure endpoints recur as a constraint: tailnet/public mobile pairing requires a real TLS endpoint (`wss://` or Tailscale Serve), with cleartext `ws://` allowed only on private LAN / `.local` / loopback / the Android emulator bridge `10.0.2.2`. The per-OS notes (`oc_platforms_android_connection`, `oc_platforms_ios_connection`) carry the full step-by-step runbooks; this hub records only that the lifecycle is the same shape everywhere.

**Source**: OpenClaw documentation — cross-page Platforms model (`platforms` + `platforms/android` + `platforms/ios` + `platforms/linux` + `platforms/mac/bundled-gateway`; mirror `inbox/openclaw_docs/platforms.md` and `inbox/openclaw_docs/platforms/`)
**Last Updated**: 2026-06-22
**Status**: Active
