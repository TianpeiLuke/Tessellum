---
tags:
  - resource
  - documentation
  - openclaw
  - nodes
  - voicewake
keywords:
  - openclaw voice wake
  - voicewake.json global trigger list
  - voicewake.get voicewake.set rpc
  - voicewake.routing.get voicewake.routing.set
  - VoiceWakeRoutingConfig route target
  - voicewake.changed voicewake.routing.changed events
  - gateway-owned wake words
  - VoiceWakeRuntime VoiceWakeManager
topics:
  - OpenClaw
  - Voice Wake
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/nodes/voicewake
access_control_group: ["general"]
---

# OpenClaw — Voice Wake Protocol (Gateway-Owned Global Trigger List)

## Overview

This note models the OpenClaw **voice-wake** subsystem: wake words are a single Gateway-owned global list (no per-node customization) plus a typed `voicewake.*` RPC protocol that reads, writes, routes, and broadcasts that list across all nodes. It covers the global-list ownership model, the `voicewake.json` storage shape on the Gateway host, the get/set and routing RPC methods, the `VoiceWakeRoutingConfig` route-target schema, the change-broadcast events and their delivery fan-out, and the per-platform (macOS/iOS/Android) client behavior — mirroring the `nodes/voicewake` source page.

## Global-List Ownership Model

OpenClaw treats **wake words as a single global list** owned by the **Gateway**. There are **no per-node custom wake words** — every node draws from the same Gateway-held set. **Any node/app UI may edit** the list; changes are persisted by the Gateway and broadcast to everyone, so editing on one client propagates to all connected clients and nodes. macOS and iOS keep local **Voice Wake enabled/disabled** toggles (local UX + permissions differ), while Android currently keeps Voice Wake off and uses a manual mic flow in the Voice tab. The enable/disable toggle is local-only state; the trigger list itself remains the single authoritative Gateway-owned value.

## Storage (Gateway Host)

Wake words are stored on the gateway machine at `~/.openclaw/settings/voicewake.json`. The stored shape is a `triggers` string array plus an `updatedAtMs` timestamp:

```json
{ "triggers": ["openclaw", "claude", "computer"], "updatedAtMs": 1730000000000 }
```

## Protocol

The `voicewake.*` surface has two method families — the trigger-list `get`/`set` pair and the routing `get`/`set` pair — plus two change-broadcast events.

### Methods

- `voicewake.get` → `{ triggers: string[] }`
- `voicewake.set` with params `{ triggers: string[] }` → `{ triggers: string[] }`

Behavior notes from the source: Triggers are normalized (trimmed, empties dropped). Empty lists fall back to defaults. Limits are enforced for safety (count/length caps). *(Specific cap values are not specified in source.)*

### Routing Methods (Trigger → Target)

The routing methods map an individual trigger to a delivery target so a detected wake word can be routed to a specific session/agent rather than always the current one:

- `voicewake.routing.get` → `{ config: VoiceWakeRoutingConfig }`
- `voicewake.routing.set` with params `{ config: VoiceWakeRoutingConfig }` → `{ config: VoiceWakeRoutingConfig }`

The `VoiceWakeRoutingConfig` shape carries a `version`, a `defaultTarget`, an array of per-trigger `routes` (each binding a `trigger` string to a `target`), and an `updatedAtMs` timestamp:

```json
{
  "version": 1,
  "defaultTarget": { "mode": "current" },
  "routes": [{ "trigger": "robot wake", "target": { "sessionKey": "agent:main:main" } }],
  "updatedAtMs": 1730000000000
}
```

Route targets support exactly one of three forms: `{ "mode": "current" }` (route to the current session), `{ "agentId": "main" }` (route to a named agent), or `{ "sessionKey": "agent:main:main" }` (route to an explicit session key).

### Events

The Gateway emits two change-broadcast events whose payloads mirror the get-method returns:

- `voicewake.changed` payload `{ triggers: string[] }`
- `voicewake.routing.changed` payload `{ config: VoiceWakeRoutingConfig }`

Who receives it: all WebSocket clients (macOS app, WebChat, etc.) and all connected nodes (iOS/Android), and also on node connect as an initial "current state" push. The on-connect push means a newly connected node is synced to the current global list immediately, without waiting for the next edit.

## Client Behavior (macOS / iOS / Android)

### macOS app

- Uses the global list to gate `VoiceWakeRuntime` triggers.
- Editing "Trigger words" in Voice Wake settings calls `voicewake.set` and then relies on the broadcast to keep other clients in sync.

### iOS node

- Uses the global list for `VoiceWakeManager` trigger detection.
- Editing Wake Words in Settings calls `voicewake.set` (over the Gateway WS) and also keeps local wake-word detection responsive.

### Android node

- Voice Wake is currently disabled in Android runtime/Settings.
- Android voice uses manual mic capture in the Voice tab instead of wake-word triggers.

**Source**: OpenClaw documentation — `nodes/voicewake` (mirror `inbox/openclaw_docs/nodes/voicewake.md`)
**Last Updated**: 2026-06-22
**Status**: Active
