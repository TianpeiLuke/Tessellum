---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - android
keywords:
  - openclaw android node
  - android gateway pairing
  - mdns nsd discovery
  - tailnet unicast dns-sd
  - wss serve secure endpoint
  - node presence alive beacon
  - devices approve autoapprovecidrs
  - openclaw nodes status
topics:
  - OpenClaw
  - Android Platform
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/android
access_control_group: ["general"]
---

# OpenClaw — Android Companion Node Connection Runbook

## Overview

This note is the step-by-step procedure for pairing and reconnecting the OpenClaw **Android companion node** against a running Gateway, mirroring the connection half of the `platforms/android` source page (Support snapshot, System control, and the Connection runbook steps 1–5 plus presence beacons). The Android app is a companion node — it does NOT host the Gateway and requires a running OpenClaw Gateway on macOS, Linux, or Windows (via WSL2). It connects directly to the Gateway WebSocket as a `role: node`, using mDNS/NSD on LAN or unicast DNS-SD over Tailscale, and authenticates via device pairing approved from the gateway CLI. The post-connection command surface (Chat, Canvas/camera, Voice/Talk, assistant entrypoints, notification forwarding) is documented separately in the sibling note `oc_platforms_android_node_surface.md`.

## Support Snapshot

- **Role:** companion node app — Android does not host the Gateway.
- **Gateway required:** yes (run it on macOS, Linux, or Windows via WSL2).
- **Install:** the app from Google Play; the Gateway via Getting Started, then Pairing.
- **Gateway:** Runbook + Configuration pages on the gateway side.
- **Protocols:** the Gateway protocol (nodes + control plane).

The connection topology is: `Android node app ⇄ (mDNS/NSD + WebSocket) ⇄ Gateway`. Android connects directly to the Gateway WebSocket and uses device pairing (`role: node`).

## System Control

System control (launchd/systemd) lives on the **Gateway host**, not on the Android device. Service management of the gateway process is a gateway-host concern documented on the Gateway runbook page — Android itself runs no service supervisor.

## Secure-Endpoint Requirement

For Tailscale or public hosts, Android requires a secure endpoint:

- **Preferred:** Tailscale Serve / Funnel with `https://<magicdns>` / `wss://<magicdns>`.
- **Also supported:** any other `wss://` Gateway URL with a real TLS endpoint.
- **Cleartext `ws://`** remains supported on private LAN addresses / `.local` hosts, plus `localhost`, `127.0.0.1`, and the Android emulator bridge (`10.0.2.2`).

Tailnet/public mobile pairing does **not** use raw tailnet IP `ws://` endpoints — use Tailscale Serve or another `wss://` URL instead.

## Prerequisites

- You can run the Gateway on the "master" machine.
- The Android device/emulator can reach the gateway WebSocket via one of: same LAN with mDNS/NSD; **or** the same Tailscale tailnet using Wide-Area Bonjour / unicast DNS-SD (see step 2); **or** a manual gateway host/port (fallback).
- Tailnet/public mobile pairing does **not** use raw tailnet IP `ws://` endpoints — use Tailscale Serve or another `wss://` URL instead.
- You can run the CLI (`openclaw`) on the gateway machine (or via SSH).

## 1) Start the Gateway

Start the Gateway on the gateway-host machine:

```bash
openclaw gateway --port 18789 --verbose
```

Confirm in the logs you see something like `listening on ws://0.0.0.0:18789`. For remote Android access over Tailscale, prefer Serve/Funnel instead of a raw tailnet bind:

```bash
openclaw gateway --tailscale serve
```

This gives Android a secure `wss://` / `https://` endpoint. A plain `gateway.bind: "tailnet"` setup is **not** enough for first-time remote Android pairing unless you also terminate TLS separately.

## 2) Verify Discovery (optional)

From the gateway machine, browse for the advertised service over multicast DNS:

```bash
dns-sd -B _openclaw-gw._tcp local.
```

If you also configured a wide-area discovery domain, compare against `openclaw gateway discover --json`. That command shows `local.` plus the configured wide-area domain in one pass and uses the resolved service endpoint instead of TXT-only hints. More debugging notes live on the Bonjour page.

### Tailnet (Vienna ⇄ London) discovery via unicast DNS-SD

Android NSD/mDNS discovery won't cross networks. If your Android node and the gateway are on different networks but connected via Tailscale, use Wide-Area Bonjour / unicast DNS-SD instead. Discovery alone is **not** sufficient for tailnet/public Android pairing — the discovered route still needs a secure endpoint (`wss://` or Tailscale Serve). Two setup steps:

1. Set up a DNS-SD zone (example `openclaw.internal.`) on the gateway host and publish `_openclaw-gw._tcp` records.
2. Configure Tailscale split DNS for your chosen domain pointing at that DNS server.

Details and example CoreDNS config are on the Bonjour page.

## 3) Connect from Android

In the Android app:

- The app keeps its gateway connection alive via a **foreground service** (persistent notification).
- Open the **Connect** tab.
- Use **Setup Code** or **Manual** mode.
- If discovery is blocked, use manual host/port in **Advanced controls**. For private LAN hosts, `ws://` still works; for Tailscale/public hosts, turn on TLS and use a `wss://` / Tailscale Serve endpoint.

After the first successful pairing, Android auto-reconnects on launch to the manual endpoint (if enabled), otherwise to the last discovered gateway (best-effort).

## Presence Alive Beacons

After the authenticated node session connects, and when the app moves to the background while the foreground service is still connected, Android calls `node.event` with `event: "node.presence.alive"`. The gateway records this as `lastSeenAtMs`/`lastSeenReason` on the paired node/device metadata only after the authenticated node device identity is known. The app counts the beacon as successfully recorded only when the gateway response includes `handled: true`. Older gateways may acknowledge `node.event` with `{ "ok": true }`; that response is compatible but does **not** count as a durable last-seen update.

## 4) Approve Pairing (CLI)

On the gateway machine, list pending requests and approve or reject by `requestId`:

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

Optionally, if the Android node always connects from a tightly controlled subnet, you can opt in to first-time node auto-approval with explicit CIDRs or exact IPs:

```json5
{
  gateway: {
    nodes: {
      pairing: {
        autoApproveCidrs: ["192.168.1.0/24"],
      },
    },
  },
}
```

This is **disabled by default**. It applies only to fresh `role: node` pairing with no requested scopes. Operator/browser pairing and any role, scope, metadata, or public-key change still require manual approval.

## 5) Verify the Node Is Connected

Verify either via node status or via a direct Gateway call:

```bash
openclaw nodes status
openclaw gateway call node.list --params "{}"
```

**Source**: OpenClaw documentation — `platforms/android` (mirror `inbox/openclaw_docs/platforms/android.md`), connection sections only
**Last Updated**: 2026-06-22
**Status**: Active
