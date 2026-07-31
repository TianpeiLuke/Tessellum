---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - bridge_protocol
keywords:
  - openclaw bridge protocol
  - legacy tcp jsonl bridge
  - node pairing pair-request pair-ok
  - scoped gateway rpc req res
  - exec lifecycle events exec.finished
  - bridge tls bridgeTlsSha256
  - tailnet bridge bind
  - gateway protocol successor
topics:
  - OpenClaw
  - Gateway Bridge Protocol
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/bridge-protocol
access_control_group: ["general"]
---

# OpenClaw — The Legacy Gateway Bridge Wire Protocol

## Overview

This note models the **legacy gateway bridge protocol**: the now-removed TCP/JSONL wire protocol OpenClaw used to admit and talk to node clients (iOS/Android/macOS node mode) before the WebSocket Gateway Protocol replaced it. It mirrors the `gateway/bridge-protocol` source page, which is kept for historical reference only — the TCP bridge has been **removed**, current builds do not ship the bridge listener, and the `bridge.*` config keys are no longer in the schema. The page directs all current node/operator clients to the WebSocket [Gateway Protocol](https://docs.openclaw.ai/gateway/protocol). This model covers why the bridge existed, its transport, the handshake/pairing exchange, the frame taxonomy, the exec-lifecycle events it carried, historical tailnet usage, and its (implicit v1) versioning.

## Why It Existed

The bridge was a deliberately narrow node-facing surface with four design motivations, copied from the source:

- **Security boundary** — the bridge exposes a small allowlist instead of the full gateway API surface.
- **Pairing + node identity** — node admission is owned by the gateway and tied to a per-node token.
- **Discovery UX** — nodes can discover gateways via Bonjour on LAN, or connect directly over a tailnet.
- **Loopback WS** — the full WS control plane stays local unless tunneled via SSH.

## Transport

The bridge wire transport was a line-delimited JSON stream over TCP:

- TCP, one JSON object per line (JSONL).
- Optional TLS (when `bridge.tls.enabled` is true).
- Historical default listener port was `18790` (current builds do not start a TCP bridge).

When TLS is enabled, discovery TXT records include `bridgeTls=1` plus `bridgeTlsSha256` as a non-secret hint. Bonjour/mDNS TXT records are unauthenticated; clients must not treat the advertised fingerprint as an authoritative pin without explicit user intent or other out-of-band verification.

## Handshake + Pairing

Node admission followed a four-step token-based handshake, verbatim from the source:

1. Client sends `hello` with node metadata + token (if already paired).
2. If not paired, gateway replies `error` (`NOT_PAIRED`/`UNAUTHORIZED`).
3. Client sends `pair-request`.
4. Gateway waits for approval, then sends `pair-ok` and `hello-ok`.

Historically, `hello-ok` returned `serverName`; hosted plugin surfaces are now advertised through `pluginSurfaceUrls`. Canvas/A2UI uses `pluginSurfaceUrls.canvas`; the deprecated `canvasHostUrl` alias is not part of the refactored protocol.

## Frames

The bridge carried a small, directional set of frame types. Client → Gateway frames:

- `req` / `res`: scoped gateway RPC (chat, sessions, config, health, voicewake, skills.bins).
- `event`: node signals (voice transcript, agent request, chat subscribe, exec lifecycle).

Gateway → Client frames:

- `invoke` / `invoke-res`: node commands (`canvas.*`, `camera.*`, `screen.record`, `location.get`, `sms.send`).
- `event`: chat updates for subscribed sessions.
- `ping` / `pong`: keepalive.

Legacy allowlist enforcement lived in `src/gateway/server-bridge.ts` (removed).

## Exec Lifecycle Events

Nodes could emit `exec.finished` events to surface completed `system.run` activity; these are mapped to system events in the gateway. Legacy nodes may still emit `exec.started`. Nodes may emit `exec.denied` for denied `system.run` attempts; the gateway accepts the event as a terminal denial and does not enqueue a system event or wake agent work.

Payload fields (all optional unless noted):

- `sessionKey` (required): agent session for event correlation and, for `exec.finished`, system event delivery.
- `runId`: unique exec id for grouping.
- `command`: raw or formatted command string.
- `exitCode`, `timedOut`, `success`, `output`: completion details (finished only).
- `reason`: denial reason (denied only).

## Historical Tailnet Usage

The bridge could be bound onto a tailnet for cross-network node connectivity, copied from the source:

- Bind the bridge to a tailnet IP: `bridge.bind: "tailnet"` in `~/.openclaw/openclaw.json` (historical only; `bridge.*` is no longer valid).
- Clients connect via MagicDNS name or tailnet IP.
- Bonjour does **not** cross networks; use manual host/port or wide-area DNS-SD when needed.

## Versioning

The bridge was **implicit v1** (no min/max negotiation). This section is historical reference only; current node/operator clients use the WebSocket [Gateway Protocol](https://docs.openclaw.ai/gateway/protocol).

**Source**: OpenClaw documentation — `gateway/bridge-protocol` (mirror `inbox/openclaw_docs/gateway/bridge-protocol.md`)
**Last Updated**: 2026-06-22
**Status**: Active
