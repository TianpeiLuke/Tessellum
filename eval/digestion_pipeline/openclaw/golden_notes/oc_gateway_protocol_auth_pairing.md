---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - protocol
keywords:
  - openclaw gateway auth
  - connect auth token password
  - device token issuance rotation
  - device identity pairing
  - device auth migration diagnostics
  - tls certificate pinning gateway
  - selectConnectAuth token priority
  - auth_token_mismatch auth_scope_mismatch
  - pairing_required recommended next step
topics:
  - OpenClaw
  - Gateway Protocol Auth and Pairing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/protocol
access_control_group: ["general"]
---

# OpenClaw — Gateway Protocol Auth, Device Pairing, and TLS Pinning

## Overview

This note is the procedure for authenticating and pairing a Gateway WebSocket connection and for pinning its TLS certificate, mirroring the **Auth**, **Device identity + pairing** (including **Device auth migration diagnostics**), and **TLS + pinning** sections of the `gateway/protocol` source page. It covers the shared-secret and identity-bearing connect-auth modes, client-side connect-auth assembly (`selectConnectAuth`) and its token priority, device-token issuance / rotation / revocation, the pairing-approval flow and device-less operator trust paths, the challenge-nonce signing requirement, the `DEVICE_AUTH_*` migration diagnostics for legacy clients, and optional cert-fingerprint pinning. It is the auth/pairing/TLS leg of the four protocol notes; the wire envelope, capability model, and RPC surface are covered by the sibling `oc_gateway_protocol_*` notes.

## Connect Auth Modes

The auth check runs at the WS `connect` handshake. There are three operator-facing modes the gateway can be configured for:

- **Shared-secret gateway auth** uses `connect.params.auth.token` or `connect.params.auth.password`, depending on the configured auth mode.
- **Identity-bearing modes** such as Tailscale Serve (`gateway.auth.allowTailscale: true`) or non-loopback `gateway.auth.mode: "trusted-proxy"` satisfy the connect-auth check from request headers instead of `connect.params.auth.*`.
- **Private-ingress `gateway.auth.mode: "none"`** skips shared-secret connect auth entirely. Do not expose that mode on public/untrusted ingress.

## Device Token Issuance and Persistence

After pairing, the Gateway issues a **device token** scoped to the connection role + scopes. It is returned in `hello-ok.auth.deviceToken` and should be persisted by the client for future connects. Clients should persist the primary `hello-ok.auth.deviceToken` after any successful connect. Reconnecting with that **stored** device token should also reuse the stored approved scope set for that token — this preserves read/probe/status access that was already granted and avoids silently collapsing reconnects to a narrower implicit admin-only scope.

Built-in setup-code bootstrap returns the primary node `hello-ok.auth.deviceToken` plus a bounded operator token in `hello-ok.auth.deviceTokens` for trusted mobile handoff. The operator token includes `operator.talk.secrets` for native Talk configuration reads and excludes `operator.admin` and `operator.pairing`. Persist `hello-ok.auth.deviceTokens` only when the connect used bootstrap auth on a trusted transport such as `wss://` or loopback/local pairing. While a non-baseline setup-code bootstrap is waiting for approval, `PAIRING_REQUIRED` details include `recommendedNextStep: "wait_then_retry"`, `retryable: true`, and `pauseReconnect: false`; clients should keep reconnecting with the same bootstrap token until the request is approved or the token becomes invalid.

If a client supplies an **explicit** `deviceToken` or explicit `scopes`, that caller-requested scope set remains authoritative; cached scopes are only reused when the client is reusing the stored per-device token.

## Client-Side Connect Auth Assembly (`selectConnectAuth`)

Client-side connect auth is assembled by `selectConnectAuth` in `src/gateway/client.ts`:

- `auth.password` is orthogonal and is always forwarded when set.
- `auth.token` is populated in priority order: explicit shared token first, then an explicit `deviceToken`, then a stored per-device token (keyed by `deviceId` + `role`).
- `auth.bootstrapToken` is sent only when none of the above resolved an `auth.token`. A shared token or any resolved device token suppresses it.
- Auto-promotion of a stored device token on the one-shot `AUTH_TOKEN_MISMATCH` retry is gated to **trusted endpoints only** — loopback, or `wss://` with a pinned `tlsFingerprint`. Public `wss://` without pinning does not qualify.

## Device Token Rotation and Revocation

Device tokens can be rotated/revoked via `device.token.rotate` and `device.token.revoke` (requires `operator.pairing` scope). Rotating or revoking a node or other non-operator role also requires `operator.admin`.

- `device.token.rotate` returns rotation metadata. It echoes the replacement bearer token only for same-device calls that are already authenticated with that device token, so token-only clients can persist their replacement before reconnecting. Shared/admin rotations do not echo the bearer token.
- Token issuance, rotation, and revocation stay bounded to the approved role set recorded in that device's pairing entry; token mutation cannot expand or target a device role that pairing approval never granted.
- For paired-device token sessions, device management is self-scoped unless the caller also has `operator.admin`: non-admin callers can manage only the operator token for their **own** device entry. Node and other non-operator token management is admin-only, even for the caller's own device.
- `device.token.rotate` and `device.token.revoke` also check the target operator token scope set against the caller's current session scopes. Non-admin callers cannot rotate or revoke a broader operator token than they already hold.

## Auth Failure Codes and Client Recovery

Auth failures include `error.details.code` plus recovery hints:

- `error.details.canRetryWithDeviceToken` (boolean)
- `error.details.recommendedNextStep` — one of `retry_with_device_token`, `update_auth_configuration`, `update_auth_credentials`, `wait_then_retry`, `review_auth_configuration`.

Client behavior for `AUTH_TOKEN_MISMATCH`: trusted clients may attempt one bounded retry with a cached per-device token; if that retry fails, clients should stop automatic reconnect loops and surface operator action guidance. `AUTH_SCOPE_MISMATCH` means the device token was recognized but does not cover the requested role/scopes — clients should not present this as a bad token; instead they should prompt the operator to re-pair or approve the narrower/broader scope contract.

## Device Identity and Pairing

Nodes should include a stable device identity (`device.id`) derived from a keypair fingerprint, and Gateways issue tokens per device + role. Pairing approvals are required for new device IDs unless local auto-approval is enabled. Pairing auto-approval is centered on direct local loopback connects. OpenClaw also has a narrow backend/container-local self-connect path for trusted shared-secret helper flows. Same-host tailnet or LAN connects are still treated as remote for pairing and require approval. All connections must sign the server-provided `connect.challenge` nonce.

WS clients normally include `device` identity during `connect` (operator + node). The only device-less operator exceptions are explicit trust paths:

- `gateway.controlUi.allowInsecureAuth=true` for localhost-only insecure HTTP compatibility.
- successful `gateway.auth.mode: "trusted-proxy"` operator Control UI auth.
- `gateway.controlUi.dangerouslyDisableDeviceAuth=true` (break-glass, severe security downgrade).
- direct-loopback `gateway-client` backend RPCs on the reserved internal helper path.

Omitting device identity has scope consequences. When a device-less operator connection is allowed through an explicit trust path, OpenClaw still clears self-declared scopes to an empty set unless that path has a named scope-preservation exception, and scope-gated methods then fail with `missing scope`. `gateway.controlUi.dangerouslyDisableDeviceAuth=true` is a Control UI break-glass scope-preservation path; it does not grant scopes to arbitrary custom backend or CLI-shaped WebSocket clients. The reserved direct-loopback `gateway-client` backend helper path preserves scopes only for internal local control-plane RPCs; custom backend IDs do not receive this exception.

## Device Auth Migration Diagnostics

For legacy clients that still use pre-challenge signing behavior, `connect` now returns `DEVICE_AUTH_*` detail codes under `error.details.code` with a stable `error.details.reason`. Common migration failures:

| Message | details.code | details.reason | Meaning |
| --- | --- | --- | --- |
| `device nonce required` | `DEVICE_AUTH_NONCE_REQUIRED` | `device-nonce-missing` | Client omitted `device.nonce` (or sent blank). |
| `device nonce mismatch` | `DEVICE_AUTH_NONCE_MISMATCH` | `device-nonce-mismatch` | Client signed with a stale/wrong nonce. |
| `device signature invalid` | `DEVICE_AUTH_SIGNATURE_INVALID` | `device-signature` | Signature payload does not match v2 payload. |
| `device signature expired` | `DEVICE_AUTH_SIGNATURE_EXPIRED` | `device-signature-stale` | Signed timestamp is outside allowed skew. |
| `device identity mismatch` | `DEVICE_AUTH_DEVICE_ID_MISMATCH` | `device-id-mismatch` | `device.id` does not match public key fingerprint. |
| `device public key invalid` | `DEVICE_AUTH_PUBLIC_KEY_INVALID` | `device-public-key` | Public key format/canonicalization failed. |

Migration target steps:

- Always wait for `connect.challenge`.
- Sign the v2 payload that includes the server nonce.
- Send the same nonce in `connect.params.device.nonce`.
- Preferred signature payload is `v3`, which binds `platform` and `deviceFamily` in addition to device/client/role/scopes/token/nonce fields.
- Legacy `v2` signatures remain accepted for compatibility, but paired-device metadata pinning still controls command policy on reconnect.

## TLS + Pinning

TLS is supported for WS connections. Clients may optionally pin the gateway cert fingerprint (see `gateway.tls` config plus `gateway.remote.tlsFingerprint` or CLI `--tls-fingerprint`). This pin is what makes a public `wss://` endpoint qualify as a "trusted endpoint" for the one-shot `AUTH_TOKEN_MISMATCH` device-token auto-promotion retry above; public `wss://` without pinning does not qualify.

**Source**: OpenClaw documentation — `gateway/protocol` (Auth, Device identity + pairing, TLS + pinning) (mirror `inbox/openclaw_docs/gateway/protocol.md`)
**Last Updated**: 2026-06-22
**Status**: Active
