---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - operator_scopes
keywords:
  - openclaw operator scopes
  - operator role node role
  - operator.read write admin scope levels
  - method scope first gate
  - approval-time checks
  - device pairing approvals scopes
  - node.pair.approve derived scopes
  - shared-secret auth full operator scope
topics:
  - OpenClaw
  - Operator Scopes
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/gateway/operator-scopes
access_control_group: ["general"]
---

# OpenClaw — Gateway Operator Scopes (Authorization Model)

## Overview

This note defines the OpenClaw **Gateway operator-scope authorization model**: the vocabulary that controls what an authenticated Gateway client may do on the control plane. Mirroring the `gateway/operator-scopes` source page, it covers the two connection **roles** (`operator`, `node`), the six `operator.*` **scope levels**, the **two-stage gate** (method scope first, then handler approval-time checks), how **device** and **node** pairing approvals derive the scopes they require, and how **shared-secret auth** restores the full default operator scope set. Crucially, scopes are a control-plane guardrail inside one trusted Gateway operator domain — they are **not hostile multi-tenant isolation**. If you need strong separation between people, teams, or machines, the documented answer is to run separate Gateways under separate OS users or hosts.

## Roles

Gateway WebSocket clients connect with one role:

- `operator` — control-plane clients such as CLI, Control UI, automation, and trusted helper processes.
- `node` — capability hosts such as macOS, iOS, Android, or headless nodes that expose commands through `node.invoke`.

Operator RPC methods require the `operator` role; node-originated methods require the `node` role. The role a client connects with therefore gates which method family it can call before any finer scope check applies.

## Scope Levels

There are six `operator.*` scope levels. They form an authorization vocabulary the whole Gateway control plane uses, with `operator.admin` sitting at the top (it satisfies every other `operator.*` scope):

| Scope | Meaning |
| --- | --- |
| `operator.read` | Read-only status, lists, catalog, logs, session reads, and other non-mutating control-plane calls. |
| `operator.write` | Normal mutating operator actions such as sending messages, invoking tools, updating talk/voice settings, and node command relay. Also satisfies `operator.read`. |
| `operator.admin` | Administrative control-plane access. Satisfies every `operator.*` scope. Required for config mutation, updates, native hooks, sensitive reserved namespaces, and high-risk approvals. |
| `operator.pairing` | Device and node pairing management, including listing, approving, rejecting, removing, rotating, and revoking pairing records or device tokens. |
| `operator.approvals` | Exec and plugin approval APIs. |
| `operator.talk.secrets` | Reading Talk configuration with secrets included. |

Two implications follow from the table. First, the scopes are partially ordered by privilege: `operator.write` also satisfies `operator.read`, and `operator.admin` satisfies every `operator.*` scope. Second, **unknown future `operator.*` scopes require an exact match unless the caller has `operator.admin`** — admin is the only scope that automatically covers a scope name the Gateway does not yet recognize.

## Method Scope Is Only the First Gate

Authorization is a two-stage gate, not a single check. Each Gateway RPC has a **least-privilege method scope**, and that method scope decides only whether the request can *reach* the handler. Some handlers then apply stricter **approval-time checks** based on the concrete thing being approved or mutated. The source gives three examples of this second gate:

- `device.pair.approve` is reachable with `operator.pairing`, but approving an operator device can only mint or preserve scopes the caller already holds.
- `node.pair.approve` is reachable with `operator.pairing`, then derives extra approval scopes from the pending node command list.
- `chat.send` is normally a write-scoped method, but persistent `/config set` and `/config unset` require `operator.admin` at command level.

The design intent is explicit: this two-stage model lets lower-scope operators perform low-risk pairing actions without making all pairing approval admin-only. The method scope keeps the surface broadly reachable; the approval-time check tightens it for the specific high-risk action.

## Device Pairing Approvals

Device pairing records are the **durable source of approved roles and scopes**. Already-paired devices do not get broader access silently: a reconnect that asks for a broader role or broader scopes creates a new pending upgrade request rather than being granted implicitly. When approving a device request, the required caller scope is derived from what the request asks for:

- A request with no operator role does not need operator token scope approval.
- A request for a non-operator device role, such as `node`, requires `operator.admin` — even when `device.pair.approve` is itself reachable with `operator.pairing`.
- A request for `operator.read`, `operator.write`, `operator.approvals`, `operator.pairing`, or `operator.talk.secrets` requires the caller to hold those same scopes, or `operator.admin`.
- A request for `operator.admin` requires `operator.admin`.
- A repair request with no explicit scopes can inherit the existing operator token scopes; if that existing token is admin-scoped, approval still requires `operator.admin`.

Two narrowing rules apply to less-privileged session types. **Non-admin shared-secret and trusted-proxy sessions** can approve operator-device requests only inside their own declared operator scopes, and approving non-operator roles remains admin-only even when those sessions can otherwise use `operator.pairing`. **Paired-device token sessions** are self-scoped unless the caller has `operator.admin`: a non-admin caller sees only its own pairing entries, can approve or reject only its own pending request, and can rotate, revoke, or remove only its own device entry.

## Node Pairing Approvals

Legacy `node.pair.*` uses a separate Gateway-owned node pairing store. WS nodes use device pairing with `role: node`, but the same approval-level vocabulary applies to both paths. For the legacy path, `node.pair.approve` uses the **pending request command list** to derive the additional required scopes:

- Commandless request → `operator.pairing`.
- Non-exec node commands → `operator.pairing` + `operator.write`.
- `system.run`, `system.run.prepare`, or `system.which` → `operator.pairing` + `operator.admin`.

The boundary here is deliberate: node pairing establishes identity and trust, but it **does not replace the node's own `system.run` exec approval policy**. Pairing a node grants the trust relationship; the node's exec policy still governs whether a given command actually runs.

## Shared-Secret Auth

Shared gateway token/password auth is treated as **trusted operator access for that Gateway**. The OpenAI-compatible HTTP surfaces, `/tools/invoke`, and the HTTP session-history endpoints restore the normal full operator default scope set for shared-secret bearer auth — even if a caller sends narrower declared scopes. In other words, a shared secret is a full-operator credential, and narrower scopes claimed on a shared-secret request do not constrain it on these surfaces.

By contrast, **identity-bearing modes** — such as trusted-proxy auth or private-ingress `none` — can still honor explicit declared scopes, because they carry a real identity rather than a single shared secret. The source closes with the same boundary guidance that opened it: scopes guard one operator domain, so for real trust-boundary separation use separate Gateways.

**Source**: OpenClaw documentation — `gateway/operator-scopes` (mirror `inbox/openclaw_docs/gateway/operator-scopes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
