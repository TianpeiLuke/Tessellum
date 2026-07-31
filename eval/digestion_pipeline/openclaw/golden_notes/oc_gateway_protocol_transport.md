---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - protocol
keywords:
  - openclaw gateway protocol
  - gateway websocket transport
  - connect handshake hello-ok
  - connect.challenge nonce
  - frame envelope req res event
  - protocol versioning minprotocol maxprotocol
  - maxpayload maxbufferedbytes
  - gateway client constants
topics:
  - OpenClaw
  - Gateway Protocol
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/protocol
access_control_group: ["general"]
---

# OpenClaw — Gateway WebSocket Wire Transport

## Overview

This note models the **Gateway WS protocol transport** — the wire-level model for OpenClaw's "single control plane + node transport," as documented in the `gateway/protocol` source page (Transport, Handshake, Framing, Versioning sections). It covers the WebSocket text/JSON frame transport, the mandatory `connect` first frame and the `connect.challenge` → `hello-ok` handshake (with role+scope declaration and a node example), the pre-connect 64 KiB cap plus the negotiated `policy.maxPayload`/`maxBufferedBytes` limits, the request/response/event frame envelope, protocol versioning (`minProtocol`/`maxProtocol`, current v4), and the reference-client constants table. The deeper capability model (roles/scopes/presence/broadcast), the full RPC method surface, and auth/device-pairing/TLS detail are split into sibling notes and only referenced here.

## Transport

The Gateway WS protocol is the **single control plane + node transport** for OpenClaw. All clients — CLI, web UI, macOS app, iOS/Android nodes, and headless nodes — connect over WebSocket and declare their **role** + **scope** at handshake time. The transport rules are:

- WebSocket, **text frames with JSON payloads**.
- The first frame **must** be a `connect` request.
- Pre-connect frames are capped at **64 KiB**. After a successful handshake, clients should follow the `hello-ok.policy.maxPayload` and `hello-ok.policy.maxBufferedBytes` limits.

With diagnostics enabled, oversized inbound frames and slow outbound buffers emit `payload.large` events before the gateway closes or drops the affected frame. These events keep sizes, limits, surfaces, and safe reason codes. They do **not** keep the message body, attachment contents, raw frame body, tokens, cookies, or secret values.

## Handshake (connect)

The handshake is a challenge/response exchange: the Gateway pushes a pre-connect `connect.challenge` event carrying a `nonce` and `ts`, the client replies with a `connect` request declaring its `minProtocol`/`maxProtocol`, `client` descriptor, `role`, `scopes`, node `caps`/`commands`/`permissions`, `auth`, and `device` identity, and the Gateway answers with a `hello-ok` response. The challenge and the operator `connect` request look like:

```json
{
  "type": "event",
  "event": "connect.challenge",
  "payload": { "nonce": "…", "ts": 1737264000000 }
}
```

```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 4,
    "client": { "id": "cli", "version": "1.2.3", "platform": "macos", "mode": "operator" },
    "role": "operator",
    "scopes": ["operator.read", "operator.write"],
    "caps": [],
    "commands": [],
    "permissions": {},
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-cli/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

The Gateway's successful response is a `hello-ok` payload:

```json
{
  "type": "res",
  "id": "…",
  "ok": true,
  "payload": {
    "type": "hello-ok",
    "protocol": 4,
    "server": { "version": "…", "connId": "…" },
    "features": { "methods": ["…"], "events": ["…"] },
    "snapshot": { "…": "…" },
    "auth": { "role": "operator", "scopes": ["operator.read", "operator.write"] },
    "policy": { "maxPayload": 26214400, "maxBufferedBytes": 52428800, "tickIntervalMs": 15000 }
  }
}
```

`server`, `features`, `snapshot`, and `policy` are all **required** by the schema (`packages/gateway-protocol/src/schema/frames.ts`). `auth` is also required and reports the negotiated role/scopes. `pluginSurfaceUrls` is optional and maps plugin surface names, such as `canvas`, to scoped hosted URLs; scoped plugin surface URLs may expire, and nodes can call `node.pluginSurface.refresh` with `{ "surface": "canvas" }` to receive a fresh entry. The experimental Canvas plugin refactor does **not** support the deprecated `canvasHostUrl`, `canvasCapability`, or `node.canvas.capability.refresh` compatibility path; current native clients and gateways must use plugin surfaces.

While the Gateway is still finishing startup sidecars, the `connect` request can return a retryable `UNAVAILABLE` error with `details.reason` set to `"startup-sidecars"` and `retryAfterMs`. Clients should retry that response within their overall connection budget instead of surfacing it as a terminal handshake failure.

The `hello-ok.auth` shape varies by what the connect produced. When no device token is issued, `auth` reports only the negotiated `role` + `scopes` (no token fields). When a device token is issued, `auth` also includes a `deviceToken`. Built-in QR/setup-code bootstrap is a fresh mobile handoff path: a successful baseline setup-code connect returns a primary node token plus one bounded operator token, e.g.:

```json
{
  "auth": {
    "deviceToken": "…",
    "role": "node",
    "scopes": [],
    "deviceTokens": [
      {
        "deviceToken": "…",
        "role": "operator",
        "scopes": ["operator.approvals", "operator.read", "operator.talk.secrets", "operator.write"]
      }
    ]
  }
}
```

The operator handoff is intentionally bounded so QR onboarding can start the mobile operator loop without granting `operator.admin` or `operator.pairing`; it does include `operator.talk.secrets` so the native client can read the Talk configuration it needs after bootstrap. Clients should persist `hello-ok.auth.deviceTokens` only when the connect used bootstrap auth on a trusted transport such as `wss://` or loopback/local pairing. Trusted same-process backend clients (`client.id: "gateway-client"`, `client.mode: "backend"`) may omit `device` on direct loopback connections when they authenticate with the shared gateway token/password; that path is reserved for internal control-plane RPCs (e.g. subagent session updates). Remote, browser-origin, node, and explicit device-token/device-identity clients still use the normal pairing and scope-upgrade checks (detailed in the auth/pairing sibling note).

### Node example

A node `connect` declares capability claims (`caps`, `commands`, `permissions`) and a `node` role/empty scopes rather than operator scopes:

```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 4,
    "client": { "id": "ios-node", "version": "1.2.3", "platform": "ios", "mode": "node" },
    "role": "node",
    "scopes": [],
    "caps": ["camera", "canvas", "screen", "location", "voice"],
    "commands": ["camera.snap", "canvas.navigate", "screen.record", "location.get"],
    "permissions": { "camera.capture": true, "screen.record": false },
    "auth": { "token": "…" },
    "locale": "en-US",
    "userAgent": "openclaw-ios/1.2.3",
    "device": {
      "id": "device_fingerprint",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

## Framing

After the handshake, all traffic uses one of three frame envelope shapes:

- **Request**: `{type:"req", id, method, params}`
- **Response**: `{type:"res", id, ok, payload|error}`
- **Event**: `{type:"event", event, payload, seq?, stateVersion?}`

Side-effecting methods require **idempotency keys** (see schema). The optional `seq` / `stateVersion` fields on events carry per-client ordering and state-version information for broadcast streams.

## Versioning

- `PROTOCOL_VERSION` lives in `packages/gateway-protocol/src/version.ts`.
- Clients send `minProtocol` + `maxProtocol`; the server **rejects ranges that do not include its current protocol**. Current clients and servers require **protocol v4**.
- Schemas + models are generated from TypeBox definitions via the codegen targets:
  - `pnpm protocol:gen`
  - `pnpm protocol:gen:swift`
  - `pnpm protocol:check`

### Client constants

The reference client in `src/gateway/client.ts` uses these defaults. Values are stable across protocol v4 and are the expected baseline for third-party clients.

| Constant                                  | Default                                               | Source                                                       |
| ----------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| `PROTOCOL_VERSION`                        | `4`                                                   | `packages/gateway-protocol/src/version.ts`                   |
| `MIN_CLIENT_PROTOCOL_VERSION`             | `4`                                                   | `packages/gateway-protocol/src/version.ts`                   |
| Request timeout (per RPC)                 | `30_000` ms                                           | `src/gateway/client.ts` (`requestTimeoutMs`)                 |
| Preauth / connect-challenge timeout       | `15_000` ms                                           | `src/gateway/handshake-timeouts.ts`                          |
| Initial reconnect backoff                 | `1_000` ms                                            | `src/gateway/client.ts` (`backoffMs`)                        |
| Max reconnect backoff                     | `30_000` ms                                           | `src/gateway/client.ts` (`scheduleReconnect`)                |
| Fast-retry clamp after device-token close | `250` ms                                              | `src/gateway/client.ts`                                      |
| Force-stop grace before `terminate()`     | `250` ms                                              | `FORCE_STOP_TERMINATE_GRACE_MS`                              |
| `stopAndWait()` default timeout           | `1_000` ms                                            | `STOP_AND_WAIT_TIMEOUT_MS`                                   |
| Default tick interval (pre `hello-ok`)    | `30_000` ms                                           | `src/gateway/client.ts`                                      |
| Tick-timeout close                        | code `4000` when silence exceeds `tickIntervalMs * 2` | `src/gateway/client.ts`                                      |
| `MAX_PAYLOAD_BYTES`                       | `25 * 1024 * 1024` (25 MB)                            | `src/gateway/server-constants.ts`                            |

The server advertises the effective `policy.tickIntervalMs`, `policy.maxPayload`, and `policy.maxBufferedBytes` in `hello-ok`; clients should honor those negotiated values rather than the pre-handshake defaults.

**Source**: OpenClaw documentation — `gateway/protocol` (mirror `inbox/openclaw_docs/gateway/protocol.md`)
**Last Updated**: 2026-06-22
**Status**: Active
