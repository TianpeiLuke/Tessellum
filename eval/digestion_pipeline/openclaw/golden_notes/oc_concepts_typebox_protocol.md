---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - typebox
keywords:
  - openclaw typebox gateway protocol
  - gateway websocket frames
  - req res event frame
  - connect hello-ok handshake
  - ajv runtime validation
  - protocol version negotiation
  - gatewayframe discriminator
  - idempotencykey side-effect methods
topics:
  - OpenClaw
  - Gateway Protocol
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/concepts/typebox
access_control_group: ["general"]
---

# OpenClaw — TypeBox Gateway WebSocket Protocol Model

## Overview

This note models the OpenClaw **Gateway WebSocket protocol** as it is defined by **TypeBox**, a TypeScript-first schema library used as the single source of truth: the schemas drive runtime validation, JSON Schema export, and Swift codegen, and everything else is generated. It covers the three frame types (request / response / event), the `connect`/`hello-ok` connection flow, the advertised method-and-event inventory, where the schemas live, how they are validated at runtime, the example frames, the minimal Node.js client, the Swift codegen output, version negotiation, and the schema conventions — mirroring the model half of the `concepts/typebox` source page. The companion codegen workflow (the `pnpm protocol:gen` pipeline, the add-a-method procedure, and the schema-change checklist) is documented separately in [oc_concepts_typebox_codegen](oc_concepts_typebox_codegen.md).

## The Three Frame Types

Every Gateway WS message is exactly one of three frames, each tagged by a `type` field:

- **Request**: `{ type: "req", id, method, params }` — a client-to-server call naming a `method` plus its `params`.
- **Response**: `{ type: "res", id, ok, payload | error }` — the server's reply to a request `id`, carrying either a `payload` (on `ok`) or an `error`.
- **Event**: `{ type: "event", event, payload, seq?, stateVersion? }` — a server push naming an `event`, with optional `seq` and `stateVersion` for ordering/state tracking.

These three frames are the entire wire vocabulary; the TypeBox schemas in `schema.ts` define their shapes and the generated artifacts enforce them on both ends.

## Connection Flow

The first frame on a connection **must** be a `connect` request. After the server accepts it, clients can call methods (e.g. `health`, `send`, `chat.send`) and subscribe to events (e.g. `presence`, `tick`, `agent`). The minimal connection flow is:

```
Client                    Gateway
  |---- req:connect -------->|
  |<---- res:hello-ok --------|
  |<---- event:tick ----------|
  |---- req:health ---------->|
  |<---- res:health ----------|
```

The `connect` request carries protocol-version bounds (`minProtocol`/`maxProtocol`) and a `client` descriptor; the server answers with a `hello-ok` response that advertises supported features and an initial snapshot, then begins emitting events such as `tick`.

## Common Methods and Events

The advertised protocol surface groups callable methods and pushed events by category:

| Category   | Examples                                                   | Notes                              |
| ---------- | ---------------------------------------------------------- | ---------------------------------- |
| Core       | `connect`, `health`, `status`                              | `connect` must be first            |
| Messaging  | `send`, `agent`, `agent.wait`, `system-event`, `logs.tail` | side-effects need `idempotencyKey` |
| Chat       | `chat.history`, `chat.send`, `chat.abort`                  | WebChat uses these                 |
| Sessions   | `sessions.list`, `sessions.patch`, `sessions.delete`       | session admin                      |
| Automation | `wake`, `cron.list`, `cron.run`, `cron.runs`               | wake + cron control                |
| Nodes      | `node.list`, `node.invoke`, `node.pair.*`                  | Gateway WS + node actions          |
| Events     | `tick`, `presence`, `agent`, `chat`, `health`, `shutdown`  | server push                        |

The authoritative advertised **discovery** inventory lives in `src/gateway/server-methods-list.ts` (`listGatewayMethods`, `GATEWAY_EVENTS`).

## Where the Schemas Live

The protocol's source-of-truth schemas and their generated/runtime artifacts are split across fixed locations:

- Source: `packages/gateway-protocol/src/schema.ts`
- Runtime validators (AJV): `packages/gateway-protocol/src/index.ts`
- Advertised feature/discovery registry: `src/gateway/server-methods-list.ts`
- Server handshake + method dispatch: `src/gateway/server.impl.ts`
- Node client: `src/gateway/client.ts`
- Generated JSON Schema: `dist/protocol.schema.json`
- Generated Swift models: `apps/macos/Sources/OpenClawProtocol/GatewayModels.swift`

## How the Schemas Are Used at Runtime

The TypeBox schemas are enforced on every side of the protocol:

- **Server side**: every inbound frame is validated with AJV. The handshake only accepts a `connect` request whose params match `ConnectParams`.
- **Client side**: the JS client validates event and response frames before using them.
- **Feature discovery**: the Gateway sends a conservative `features.methods` and `features.events` list in `hello-ok` from `listGatewayMethods()` and `GATEWAY_EVENTS`.
- That discovery list is **not** a generated dump of every callable helper in `coreGatewayHandlers`; some helper RPCs are implemented in `src/gateway/server-methods/*.ts` without being enumerated in the advertised feature list.

## Example Frames

The frames below are the canonical wire shapes. The `connect` request (the required first message) negotiates a protocol range and identifies the client:

```json
{
  "type": "req",
  "id": "c1",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 4,
    "client": {
      "id": "openclaw-macos",
      "displayName": "macos",
      "version": "1.0.0",
      "platform": "macos 15.1",
      "mode": "ui",
      "instanceId": "A1B2"
    }
  }
}
```

The `hello-ok` response confirms the negotiated `protocol`, identifies the server/connection, advertises `features` (methods + events), supplies an initial `snapshot` (presence, health, `stateVersion`, `uptimeMs`), and states the connection `policy` (`maxPayload`, `maxBufferedBytes`, `tickIntervalMs`):

```json
{
  "type": "res",
  "id": "c1",
  "ok": true,
  "payload": {
    "type": "hello-ok",
    "protocol": 4,
    "server": { "version": "dev", "connId": "ws-1" },
    "features": { "methods": ["health"], "events": ["tick"] },
    "snapshot": {
      "presence": [],
      "health": {},
      "stateVersion": { "presence": 0, "health": 0 },
      "uptimeMs": 0
    },
    "policy": { "maxPayload": 1048576, "maxBufferedBytes": 1048576, "tickIntervalMs": 30000 }
  }
}
```

A request and its matching response correlate by `id` (`health` request → `{ ok: true }` payload), and an event frame (`tick`) carries a `payload` plus an ordering `seq`:

```json
{ "type": "req", "id": "r1", "method": "health" }
{ "type": "res", "id": "r1", "ok": true, "payload": { "ok": true } }
{ "type": "event", "event": "tick", "payload": { "ts": 1730000000 }, "seq": 12 }
```

## Minimal Client (Node.js)

The smallest useful flow over the protocol is connect-then-health: open a WebSocket, send a `connect` request, and on the `ok` response for that `id` issue a `health` request, reading its payload from the matching `res` frame.

```ts
import { WebSocket } from "ws";

const ws = new WebSocket("ws://127.0.0.1:18789");

ws.on("open", () => {
  ws.send(
    JSON.stringify({
      type: "req",
      id: "c1",
      method: "connect",
      params: {
        minProtocol: 4,
        maxProtocol: 4,
        client: {
          id: "cli",
          displayName: "example",
          version: "dev",
          platform: "node",
          mode: "cli",
        },
      },
    }),
  );
});

ws.on("message", (data) => {
  const msg = JSON.parse(String(data));
  if (msg.type === "res" && msg.id === "c1" && msg.ok) {
    ws.send(JSON.stringify({ type: "req", id: "h1", method: "health" }));
  }
  if (msg.type === "res" && msg.id === "h1") {
    console.log("health:", msg.payload);
    ws.close();
  }
});
```

## Swift Codegen Behavior

The Swift generator (for the macOS app) emits, from the same schemas:

- A `GatewayFrame` enum with `req`, `res`, `event`, and `unknown` cases.
- Strongly typed payload structs/enums.
- `ErrorCode` values, `GATEWAY_PROTOCOL_VERSION`, and `GATEWAY_MIN_PROTOCOL_VERSION`.

Unknown frame types are preserved as raw payloads for forward compatibility, so an older Swift client can still receive frames it does not yet model.

## Versioning and Compatibility

Protocol versioning is explicit and negotiated per connection:

- `PROTOCOL_VERSION` lives in `packages/gateway-protocol/src/version.ts`.
- Clients send `minProtocol` + `maxProtocol`; the server rejects ranges that do not include its current protocol.
- The Swift models keep unknown frame types to avoid breaking older clients.

## Schema Patterns and Conventions

The TypeBox schemas follow consistent conventions that the model relies on:

- Most objects use `additionalProperties: false` for strict payloads.
- `NonEmptyString` is the default for IDs and method/event names.
- The top-level `GatewayFrame` uses a **discriminator** on `type` (req / res / event).
- Methods with side effects usually require an `idempotencyKey` in params (example: `send`, `poll`, `agent`, `chat.send`).
- `agent` accepts an optional `internalEvents` for runtime-generated orchestration context (for example subagent/cron task completion handoff); treat this as internal API surface.

## Live Schema JSON

The generated JSON Schema is committed in the repo at `dist/protocol.schema.json`, and the published raw file is typically available externally (see References).

**Source**: OpenClaw documentation — `concepts/typebox` (mirror `inbox/openclaw_docs/concepts/typebox.md`)
**Last Updated**: 2026-06-22
**Status**: Active
