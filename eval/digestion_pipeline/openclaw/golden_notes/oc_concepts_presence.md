---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - presence
keywords:
  - openclaw presence
  - instances tab presence
  - system-presence system-event
  - instanceId merge dedupe
  - presence ttl bounded size
  - gateway self entry
  - websocket connect presence
  - loopback ip caveat
topics:
  - OpenClaw
  - Presence
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/concepts/presence
access_control_group: ["general"]
---

# OpenClaw — The Presence Model

## Overview

This note models OpenClaw **presence**: a lightweight, best-effort view of the Gateway itself plus the clients connected to it (mac app, WebChat, CLI, etc.), used primarily to render the macOS app's **Instances** tab and to give operators quick visibility. It covers the presence-entry field schema, the four producer sources (Gateway self entry, WebSocket `connect`, `system-event` beacons, and `role: node` connects), the `instanceId`-keyed merge/dedupe rules, the 5-minute TTL and 200-entry bound, the loopback-IP remote/tunnel caveat, the `system-presence` consumer and its Active/Idle/Stale indicator, and debugging tips — mirroring the `concepts/presence` source page.

## Presence Fields (what shows up)

Presence entries are structured objects whose fields describe one Gateway or client instance. The documented fields are:

- `instanceId` (optional but strongly recommended): a stable client identity, usually `connect.client.instanceId`.
- `host`: a human-friendly host name.
- `ip`: a best-effort IP address.
- `version`: the client version string.
- `deviceFamily` / `modelIdentifier`: hardware hints.
- `mode`: one of `ui`, `webchat`, `cli`, `backend`, `probe`, `test`, `node`, ... (the source list is open-ended).
- `lastInputSeconds`: "seconds since last user input" (if known).
- `reason`: one of `self`, `connect`, `node-connected`, `periodic`, ... (also open-ended in the source).
- `ts`: the last update timestamp, in milliseconds since epoch.

The model is best-effort, so a given producer may populate only a subset of these fields (for example, `instanceId` is "optional but strongly recommended" rather than required, and `lastInputSeconds` is reported only "if known").

## Producers (where presence comes from)

Presence entries are produced by multiple sources and then **merged** into a single view. The source page enumerates four producers.

### 1) Gateway self entry

The Gateway always seeds a "self" entry at startup so that UIs show the gateway host even before any clients connect. This is the entry carried with `reason: self`.

### 2) WebSocket connect

Every WS client begins with a `connect` request; on a successful handshake the Gateway upserts a presence entry for that connection (carried with `reason: connect`). One documented exception governs short-lived CLI use: because the CLI often connects for short, one-off commands, a connection with `client.mode === "cli"` is **not** turned into a presence entry, which avoids spamming the Instances list with transient one-off command connections.

### 3) `system-event` beacons

Clients can send richer periodic beacons via the `system-event` method. The mac app uses these beacons to report its host name, IP, and `lastInputSeconds` (these periodic updates carry `reason: periodic`).

### 4) Node connects (role: node)

When a node connects over the Gateway WebSocket with `role: node`, the Gateway upserts a presence entry for that node, following the same flow as other WS clients (carried with `reason: node-connected`).

## Merge + Dedupe Rules (why `instanceId` matters)

Presence entries are stored in a single **in-memory map**, with the following keying and merge behavior:

- Entries are keyed by a **presence key**.
- The best key is a stable `instanceId` (from `connect.client.instanceId`) that survives restarts.
- Keys are **case-insensitive**.

Because the map is keyed this way, multiple producers reporting the same stable `instanceId` (for example, the initial WS `connect` entry and the later `system-event` periodic beacons from the same mac app) collapse onto one row. The caveat is that if a client reconnects without a stable `instanceId`, it may show up as a **duplicate** row — the model has no other way to recognize the reconnection as the same instance.

## TTL and Bounded Size

Presence is intentionally ephemeral, so the in-memory map is bounded along two axes:

- **TTL:** entries older than 5 minutes are pruned.
- **Max entries:** 200 (the oldest are dropped first).

Together these keep the list fresh and avoid unbounded memory growth. Combined with the `ts` field (the last-update timestamp), the TTL is what makes a stale entry eventually disappear rather than lingering after a client goes away.

## Remote/Tunnel Caveat (loopback IPs)

When a client connects over an SSH tunnel or a local port forward, the Gateway may see the remote address as `127.0.0.1`. To avoid overwriting a good client-reported `ip` with a meaningless loopback address, loopback remote addresses are ignored. This preserves the client-reported IP in the presence entry instead of replacing it with the tunnel's local endpoint.

## Consumers

### macOS Instances tab

The macOS app renders the output of the `system-presence` method and applies a small status indicator — **Active / Idle / Stale** — based on the age of the last update (i.e., how old the entry's `ts` is relative to now). This is the primary consumer of the presence model and the reason most of the field schema exists (host, IP, `lastInputSeconds`, and freshness all feed this view).

## Debugging Tips

The source page gives a short operational playbook for inspecting and fixing presence:

- To see the raw list, call `system-presence` against the Gateway.
- If you see duplicates: confirm clients send a stable `client.instanceId` in the handshake; confirm periodic beacons use the **same** `instanceId`; and check whether the connection-derived entry is missing `instanceId` (in that case duplicates are expected, per the merge/dedupe rules above).

**Source**: OpenClaw documentation — `concepts/presence` (mirror `inbox/openclaw_docs/concepts/presence.md`)
**Last Updated**: 2026-06-22
**Status**: Active
