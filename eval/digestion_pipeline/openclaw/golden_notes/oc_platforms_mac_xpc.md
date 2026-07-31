---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - macos
keywords:
  - openclaw macos ipc
  - node host service unix socket
  - node.invoke system.run
  - peekaboobridge bridge.sock teamid
  - hmac challenge response uds
  - tcc owning gui app
  - exec approvals ipc flow
topics:
  - OpenClaw
  - macOS IPC
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/platforms/mac/xpc
access_control_group: ["general"]
---

# OpenClaw — macOS IPC Architecture (Node Host Service ↔ App ↔ PeekabooBridge)

## Overview

This note models the **macOS IPC architecture** of the OpenClaw app — the cross-process structure that lets an agent drive TCC-facing macOS work safely, mirroring the `platforms/mac/xpc` source page. In the current model, a **local Unix socket connects the node host service to the macOS app** for exec approvals and `system.run`, agent actions still flow through the **Gateway WebSocket** via `node.invoke`, an `openclaw-mac` debug CLI exists for discovery/connect checks, and **UI automation uses PeekabooBridge**. The model has three structural layers — the Gateway + node transport, the node-service↔app IPC (a local Unix domain socket hardened with token + HMAC + TTL), and the separate PeekabooBridge socket — plus the operational restart/rebuild flow and the hardening invariants that keep the privileged surface single, signed, and local-only.

## Goals

The architecture is organized around three goals stated by the source page. First, a **single GUI app instance that owns all TCC-facing work** — notifications, screen recording, mic, speech, and AppleScript — so the trust-prompt surface stays in one place. Second, a **small surface for automation**: Gateway + node commands, plus PeekabooBridge for UI automation. Third, **predictable permissions**: always the same signed bundle ID, launched by launchd, so TCC grants stick across runs.

## How It Works

### Gateway + Node Transport

The app runs the Gateway in **local mode** and connects to it **as a node**. Agent actions are performed via `node.invoke` (for example `system.run`, `system.notify`, `canvas.*`). This is the primary agent-facing path: commands the agent issues reach the macOS host as `node.invoke` calls carried over the Gateway WebSocket, rather than over any direct app-to-agent channel.

### Node Service + App IPC

A **headless node host service** connects to the Gateway WebSocket. When a `system.run` request arrives, it is **forwarded to the macOS app over a local Unix socket**; the app then performs the exec in UI context, prompts if needed, and returns output. This split keeps the privileged execution (which may need TCC-gated UI context and operator approval) inside the single signed GUI app, while the node host service remains a thin headless relay between the Gateway transport and that app. The end-to-end shape is captured by the source page's SCI diagram:

```
Agent -> Gateway -> Node Service (WS)
                      |  IPC (UDS + token + HMAC + TTL)
                      v
                  Mac App (UI + TCC + system.run)
```

The IPC edge between the node service and the Mac App is a Unix domain socket (UDS) hardened with a token, an HMAC challenge/response, and a short TTL — the same hardening primitives enumerated under [Hardening Notes](#hardening-notes) below.

### PeekabooBridge (UI Automation)

UI automation does not reuse the node-service↔app socket; it uses a **separate UNIX socket named `bridge.sock`** speaking the **PeekabooBridge JSON protocol**. The client-side **host preference order** is `Peekaboo.app → Claude.app → OpenClaw.app → local execution` — the first available bridge host wins, falling back to local execution if none is present. Security: bridge hosts **require an allowed TeamID**; a DEBUG-only same-UID escape hatch is guarded by the environment variable `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (a Peekaboo convention). The source page defers the bridge protocol details to the dedicated PeekabooBridge usage page.

## Operational Flows

**Restart/rebuild** is driven by a single script invocation with a signing identity, copied verbatim from the source:

`SIGN_IDENTITY="Apple Development: <Developer Name> (<TEAMID>)" scripts/restart-mac.sh`

That flow kills existing instances, performs a **Swift build + package**, and **writes/bootstraps/kickstarts the LaunchAgent**. The architecture also enforces a **single instance**: the app **exits early if another instance with the same bundle ID is running**, which preserves the "one GUI app owns TCC" invariant even across rebuild/restart cycles.

## Hardening Notes

The source page lists the hardening posture that protects the privileged surface. Prefer **requiring a TeamID match for all privileged surfaces**. For PeekabooBridge, `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (DEBUG-only) may allow same-UID callers for local development. **All communication remains local-only; no network sockets are exposed.** **TCC prompts originate only from the GUI app bundle**, so the signed bundle ID must stay stable across rebuilds for grants to persist. The node-service↔app IPC itself is hardened with **socket mode `0600`, a token, peer-UID checks, an HMAC challenge/response, and a short TTL** — the layered controls shown on the IPC edge of the SCI diagram.

**Source**: OpenClaw documentation — `platforms/mac/xpc` (mirror `inbox/openclaw_docs/platforms/mac/xpc.md`)
**Last Updated**: 2026-06-22
**Status**: Active
