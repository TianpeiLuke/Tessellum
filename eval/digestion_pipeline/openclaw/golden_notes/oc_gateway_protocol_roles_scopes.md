---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - protocol
keywords:
  - openclaw gateway roles scopes
  - operator scopes operator.read operator.write
  - node caps commands permissions
  - broadcast event scoping
  - system-presence node.presence.alive
  - operator.admin reserved prefixes
  - node.pair.approve approval-time scope
  - fail-closed broadcast gating
topics:
  - OpenClaw
  - Gateway Protocol Capability Model
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/protocol
access_control_group: ["general"]
---

# OpenClaw — Gateway Protocol Roles, Scopes, Presence, and Broadcast Scoping

## Overview

This note models the **connection capability surface** of the OpenClaw Gateway WebSocket protocol: the two client roles (`operator`, `node`), the operator scope set, the node `caps`/`commands`/`permissions` claims, presence keyed by device identity, the node background-alive event, and the scope-gating of server-pushed broadcast events. It mirrors the `Roles + scopes`, `Presence`, `Broadcast event scoping`, and `Scope` sections of the `gateway/protocol` source page. Roles and scopes are declared at WS `connect` time (covered in the sibling transport note); this note models what those declarations *mean* and how the Gateway enforces them server-side. The full operator scope model, approval-time checks, and shared-secret semantics live in the source's link-out [Operator scopes](https://docs.openclaw.ai/gateway/operator-scopes) page.

## Roles

A connection declares one of two roles at `connect`:

- `operator` = control plane client (CLI / UI / automation).
- `node` = capability host (camera / screen / canvas / `system.run`).

The role chosen determines whether the connection drives the control plane (operator) or hosts device capabilities the Gateway can invoke (node). Presence is keyed by device identity, so a single device that connects as both operator and node surfaces as one row (see Presence).

## Scopes (operator)

Operator connections carry a scope set that gates which methods and broadcasts they may use. The common scopes are:

- `operator.read`
- `operator.write`
- `operator.admin`
- `operator.approvals`
- `operator.pairing`
- `operator.talk.secrets`

`talk.config` with `includeSecrets: true` requires `operator.talk.secrets` (or `operator.admin`). Plugin-registered gateway RPC methods may request their own operator scope, but the reserved core admin prefixes `config.*`, `exec.approvals.*`, `wizard.*`, and `update.*` always resolve to `operator.admin`.

**Method scope is only the first gate.** Some slash commands reached through `chat.send` apply stricter command-level checks on top of the method scope. For example, persistent `/config set` and `/config unset` writes require `operator.admin`.

`node.pair.approve` also has an extra approval-time scope check layered on top of the base method scope, scaled to what the pairing request grants:

- commandless requests: `operator.pairing`
- requests with non-exec node commands: `operator.pairing` + `operator.write`
- requests that include `system.run`, `system.run.prepare`, or `system.which`: `operator.pairing` + `operator.admin`

## Caps / commands / permissions (node)

Nodes declare three capability claims at connect time:

- `caps`: high-level capability categories such as `camera`, `canvas`, `screen`, `location`, `voice`, and `talk`.
- `commands`: command allowlist for invoke.
- `permissions`: granular toggles (e.g. `screen.record`, `camera.capture`).

The Gateway treats all three as **claims** and enforces server-side allowlists against them — a node cannot expand its effective capability surface simply by declaring more. This separates what a node *asserts* it can do from what the Gateway *permits* it to do.

## Presence

Presence is the Gateway's view of which device identities are currently reachable:

- `system-presence` returns entries keyed by device identity.
- Presence entries include `deviceId`, `roles`, and `scopes` so UIs can show a single row per device even when it connects as both **operator** and **node**.
- `node.list` includes optional `lastSeenAtMs` and `lastSeenReason` fields. Connected nodes report their current connection time as `lastSeenAtMs` with reason `connect`; paired nodes can also report durable background presence when a trusted node event updates their pairing metadata.

### Node background alive event

Nodes may call `node.event` with `event: "node.presence.alive"` to record that a paired node was alive during a background wake **without** marking it connected. The event payload is carried as a JSON string in `payloadJSON`:

```json
{
  "event": "node.presence.alive",
  "payloadJSON": "{\"trigger\":\"silent_push\",\"sentAtMs\":1737264000000,\"displayName\":\"Peter's iPhone\",\"version\":\"2026.4.28\",\"platform\":\"iOS 18.4.0\",\"deviceFamily\":\"iPhone\",\"modelIdentifier\":\"iPhone17,1\",\"pushTransport\":\"relay\"}"
}
```

`trigger` is a closed enum: `background`, `silent_push`, `bg_app_refresh`, `significant_location`, `manual`, or `connect`. Unknown trigger strings are normalized to `background` by the gateway before persistence. The event is durable only for authenticated node device sessions; device-less or unpaired sessions return `handled: false`.

Successful gateways return a structured result:

```json
{
  "ok": true,
  "event": "node.presence.alive",
  "handled": true,
  "reason": "persisted"
}
```

Older gateways may still return `{ "ok": true }` for `node.event`; clients should treat that as an acknowledged RPC, not as durable presence persistence.

## Broadcast event scoping

Server-pushed WebSocket broadcast events are scope-gated so that pairing-scoped or node-only sessions do not passively receive session content. The gating rules by event family are:

- **Chat, agent, and tool-result frames** (including streamed `agent` events and tool call results) require at least `operator.read`. Sessions without `operator.read` skip these frames entirely.
- **Plugin-defined `plugin.*` broadcasts** are gated to `operator.write` or `operator.admin`, depending on how the plugin registered them.
- **Status and transport events** (`heartbeat`, `presence`, `tick`, connect/disconnect lifecycle, etc.) remain unrestricted so transport health stays observable to every authenticated session.
- **Unknown broadcast event families** are scope-gated by default (**fail-closed**) unless a registered handler explicitly relaxes them.

Each client connection keeps its own per-client sequence number, so broadcasts preserve monotonic ordering on that socket even when different clients see different scope-filtered subsets of the event stream.

## Scope (full surface)

The protocol exposes the **full gateway API** — status, channels, models, chat, agent, sessions, nodes, approvals, and more. The exact surface is defined by the TypeBox schemas in `packages/gateway-protocol/src/schema.ts`. The roles/scopes model above is the access-control layer that decides which slice of this full surface a given connection may reach.

**Source**: OpenClaw documentation — `gateway/protocol` (mirror `inbox/openclaw_docs/gateway/protocol.md`), sections Roles + scopes / Presence / Broadcast event scoping / Scope
**Last Updated**: 2026-06-22
**Status**: Active
