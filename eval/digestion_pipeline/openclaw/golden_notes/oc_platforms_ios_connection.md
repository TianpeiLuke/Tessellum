---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - ios
keywords:
  - openclaw ios node connection
  - ios pair connect gateway
  - bonjour tailnet manual host discovery
  - background alive beacons node.presence.alive
  - wkwebview canvas a2ui ios
  - canvas.navigate eval snapshot
  - voice wake talk mode push-to-talk
  - autoApproveCidrs ios pairing
  - node_background_unavailable a2ui_host_unavailable
topics:
  - OpenClaw
  - Platforms
  - iOS
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/ios
access_control_group: ["general"]
---

# OpenClaw — Connecting and Operating the iOS Companion Node

## Overview

This note is the runbook for pairing and operating the OpenClaw **iOS companion node**: how the iPhone app connects to a Gateway running elsewhere, the three discovery paths (Bonjour LAN, tailnet unicast DNS-SD, manual host), the pair-and-approve quick start, background alive beacons, the WKWebView Canvas + A2UI surface, the iOS-node-vs-Computer-Use boundary, voice wake / talk mode (push-to-talk), and the common foreground/reconnect errors. It mirrors the `platforms/ios` source page, EXCLUDING the relay-backed push and authentication/trust-flow design, which is documented in its sibling argument note `oc_platforms_ios_push_relay_trust`.

## What it does

iPhone app builds are distributed through Apple channels when enabled for a release; local development builds can also run from source. As a companion node the iOS app does three things: it **connects to a Gateway over WebSocket (LAN or tailnet)**; it **exposes node capabilities** — Canvas, Screen snapshot, Camera capture, Location, Talk mode, Voice wake; and it **receives `node.invoke` commands and reports node status events**.

## Requirements

The iOS app is a node only — it requires a **Gateway running on another device (macOS, Linux, or Windows via WSL2)**. It then needs one of three network paths to reach that Gateway: same LAN via Bonjour; tailnet via unicast DNS-SD (example domain: `openclaw.internal.`); or a manual host/port fallback.

## Quick start (pair + connect)

1. Start the Gateway:

```bash
openclaw gateway --port 18789
```

2. In the iOS app, open Settings and pick a discovered gateway (or enable Manual Host and enter host/port).

3. Approve the pairing request on the gateway host:

```bash
openclaw devices list
openclaw devices approve <requestId>
```

If the app retries pairing with changed auth details (role/scopes/public key), the previous pending request is **superseded** and a new `requestId` is created — run `openclaw devices list` again before approval.

Optionally, if the iOS node always connects from a tightly controlled subnet, you can opt in to first-time node auto-approval with explicit CIDRs or exact IPs:

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

This is disabled by default. It applies only to fresh `role: node` pairing with no requested scopes; operator/browser pairing and any role, scope, metadata, or public-key change still require manual approval.

4. Verify connection:

```bash
openclaw nodes status
openclaw gateway call node.list --params "{}"
```

## Background alive beacons

When iOS wakes the app for a silent push, background refresh, or significant-location event, the app attempts a short node reconnect and then calls `node.event` with `event: "node.presence.alive"`. The gateway records this as `lastSeenAtMs`/`lastSeenReason` on the paired node/device metadata only after the authenticated node device identity is known. The app treats a background wake as successfully recorded only when the gateway response includes `handled: true`; older gateways may acknowledge `node.event` with `{ "ok": true }`, which is compatible but does not count as a durable last-seen update.

## Discovery paths

The iOS app can reach a Gateway by three paths, tried in roughly this order.

### Bonjour (LAN)

The iOS app browses `_openclaw-gw._tcp` on `local.` and, when configured, the same wide-area DNS-SD discovery domain. Same-LAN gateways appear automatically from `local.`; cross-network discovery can use the configured wide-area domain without changing the beacon type.

### Tailnet (cross-network)

If mDNS is blocked, use a unicast DNS-SD zone (choose a domain; example: `openclaw.internal.`) and Tailscale split DNS. See the Bonjour gateway docs for the CoreDNS example.

### Manual host/port

In Settings, enable **Manual Host** and enter the gateway host + port (default `18789`).

## Canvas + A2UI

The iOS node renders a **WKWebView canvas**. Drive it with `node.invoke`:

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.navigate --params '{"url":"http://<gateway-host>:18789/__openclaw__/canvas/"}'
```

Key behaviors: the Gateway canvas host serves `/__openclaw__/canvas/` and `/__openclaw__/a2ui/`, served from the Gateway HTTP server (same port as `gateway.port`, default `18789`). The iOS node keeps the built-in scaffold as the connected default view; `canvas.a2ui.push` and `canvas.a2ui.reset` use the bundled app-owned A2UI page. Remote Gateway A2UI pages are render-only on iOS — native A2UI button actions are accepted only from bundled app-owned pages. Return to the built-in scaffold with `canvas.navigate` and `{"url":""}`.

## Computer Use relationship

The iOS app is a **mobile node surface, not a Codex Computer Use backend**. Codex Computer Use and `cua-driver mcp` control a local macOS desktop through MCP tools; the iOS app exposes iPhone capabilities through OpenClaw node commands such as `canvas.*`, `camera.*`, `screen.*`, `location.*`, and `talk.*`. Agents can still operate the iOS app through OpenClaw by invoking node commands, but those calls go through the gateway node protocol and follow iOS foreground/background limits. Use Codex Computer Use for local desktop control and this node surface for iOS capabilities.

### Canvas eval / snapshot

Run JavaScript inside the canvas WebView with the `canvas.eval` command (e.g. `openclaw nodes invoke --node "iOS Node" --command canvas.eval --params '{"javaScript":"…"}'`, where the script reads `const {ctx} = window.__openclaw;` to draw on the canvas and returns `"ok"`), and capture the rendered canvas with `canvas.snapshot`:

```bash
openclaw nodes invoke --node "iOS Node" --command canvas.snapshot --params '{"maxWidth":900,"format":"jpeg"}'
```

## Voice wake + talk mode

Voice wake and talk mode are available in Settings. Talk-capable iOS nodes advertise the `talk` capability and can declare `talk.ptt.start`, `talk.ptt.stop`, `talk.ptt.cancel`, and `talk.ptt.once`; the Gateway allows those push-to-talk commands by default for trusted Talk-capable nodes. iOS may suspend background audio, so treat voice features as best-effort when the app is not active.

## Common errors

- `NODE_BACKGROUND_UNAVAILABLE` — bring the iOS app to the foreground (canvas/camera/screen commands require it).
- `A2UI_HOST_UNAVAILABLE` — the bundled A2UI page was not reachable in the app WebView; keep the app foregrounded on the Screen tab and retry.
- Pairing prompt never appears — run `openclaw devices list` and approve manually.
- Reconnect fails after reinstall — the Keychain pairing token was cleared; re-pair the node.

**Source**: OpenClaw documentation — `platforms/ios` (mirror `inbox/openclaw_docs/platforms/ios.md`)
**Last Updated**: 2026-06-22
**Status**: Active
