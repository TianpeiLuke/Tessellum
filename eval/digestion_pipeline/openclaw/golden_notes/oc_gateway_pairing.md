---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - pairing
keywords:
  - openclaw gateway node pairing
  - node.pair methods events
  - openclaw nodes cli approve reject
  - pending paired token rotation
  - node command gating 2026.3.31
  - trusted cidr auto-approval
  - forwarded header locality pairing
topics:
  - OpenClaw
  - Gateway Pairing
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/pairing
access_control_group: ["general"]
---

# OpenClaw — Gateway-Owned Node Pairing

## Overview

This note documents OpenClaw's **Gateway-owned node pairing** procedure (Option B): how iOS and other remote nodes request to join, get approved/rejected, receive a rotated auth token, and what trust boundaries and auto-approval paths govern the flow. It mirrors the `gateway/pairing` source page section-for-section — the pending/paired/token lifecycle, the `openclaw nodes` CLI, the `node.pair.*` gateway-protocol methods/events, the `2026.3.31+` node-command-gating and node-event trust-boundary breaking changes, the three auto-approval paths (silent macOS, trusted-CIDR, metadata-upgrade), forwarded-header locality rules, the local private storage layout, and stateless transport behavior. In Gateway-owned pairing the **Gateway is the source of truth** for which nodes are allowed to join; UIs (the macOS app, future clients) are just frontends that approve or reject pending requests.

## Concepts

A node-pairing decision is built from three pieces. A **pending request** is a node that asked to join and requires approval. A **paired node** is an approved node with an issued auth token. The **transport** — the Gateway WS endpoint — forwards requests but does not decide membership (legacy TCP bridge support has been removed).

**Important distinction (not the same as device pairing):** WS nodes use **device pairing** (role `node`) during `connect`. `node.pair.*` is a separate pairing store and does **not** gate the WS handshake. Only clients that explicitly call `node.pair.*` use this flow.

## How pairing works

The end-to-end flow is five steps, after which a node holds a token it reconnects with:

1. A node connects to the Gateway WS and requests pairing.
2. The Gateway stores a **pending request** and emits `node.pair.requested`.
3. You approve or reject the request (CLI or UI).
4. On approval, the Gateway issues a **new token** (tokens are rotated on re-pair).
5. The node reconnects using the token and is now "paired".

Pending requests expire automatically after **5 minutes**.

## CLI workflow (headless friendly)

The `openclaw nodes` subcommands drive the whole lifecycle without a UI:

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
openclaw nodes status
openclaw nodes remove --node <id|name|ip>
openclaw nodes rename --node <id|name|ip> --name "Living Room iPad"
```

`nodes status` shows paired/connected nodes and their capabilities.

## API surface (gateway protocol)

Two **events** are emitted on the gateway protocol: `node.pair.requested` (emitted when a new pending request is created) and `node.pair.resolved` (emitted when a request is approved/rejected/expired).

The **methods** are:

- `node.pair.request` — create or reuse a pending request.
- `node.pair.list` — list pending + paired nodes (`operator.pairing`).
- `node.pair.approve` — approve a pending request (issues token).
- `node.pair.reject` — reject a pending request.
- `node.pair.remove` — remove a paired node. For device-backed pairings this revokes the device's `node` role: it mutates `devices/paired.json` and invalidates/disconnects that device's node-role sessions. A **mixed-role** device (e.g. it also holds `operator`) keeps its row and only loses the `node` role; a node-only device row is deleted. It also removes any matching legacy gateway-owned node pairing entry. Authz: `operator.pairing` may remove non-operator node rows; a device-token caller revoking its **own** node role on a mixed-role device additionally needs `operator.admin`.
- `node.pair.verify` — verify `{ nodeId, token }`.

Behavioral notes: `node.pair.request` is **idempotent per node** (repeated calls return the same pending request), and repeated requests for the same pending node also refresh the stored node metadata and the latest allowlisted declared command snapshot for operator visibility. Approval **always** generates a fresh token; **no token is ever returned from `node.pair.request`**. Requests may include `silent: true` as a hint for auto-approval flows. Operator scope levels and approval-time checks are summarized in the operator-scopes doc. The `node.pair.approve` method uses the pending request's declared commands to enforce extra approval scopes: a commandless request needs `operator.pairing`; a non-exec command request needs `operator.pairing` + `operator.write`; and a `system.run` / `system.run.prepare` / `system.which` request needs `operator.pairing` + `operator.admin`.

**Warning (live command surface is NOT pinned by pairing):** Node pairing is a trust and identity flow plus token issuance; it does **not** pin the live node command surface per node. Live node commands come from what the node declares on connect after the gateway's global node command policy (`gateway.nodes.allowCommands` and `denyCommands`) is applied. Per-node `system.run` allow and ask policy lives on the node in `exec.approvals.node.*`, not in the pairing record.

## Node command gating (2026.3.31+)

**Breaking change:** Starting with `2026.3.31`, node commands are **disabled until node pairing is approved**. Device pairing alone is no longer enough to expose declared node commands. When a node connects for the first time, pairing is requested automatically; until the pairing request is approved, all pending node commands from that node are filtered and will not execute. Once trust is established through pairing approval, the node's declared commands become available subject to the normal command policy. Concretely: nodes that previously relied on device pairing alone to expose commands must now complete node pairing, and commands queued before pairing approval are **dropped, not deferred**.

## Node event trust boundaries (2026.3.31+)

**Breaking change:** Node-originated runs now stay on a **reduced trusted surface**. Node-originated summaries and related session events are restricted to the intended trusted surface; notification-driven or node-triggered flows that previously relied on broader host or session tool access may need adjustment. This hardening ensures that node events cannot escalate into host-level tool access beyond what the node's trust boundary permits. Durable node presence updates follow the same identity boundary: the `node.presence.alive` event is accepted only from authenticated node device sessions and updates pairing metadata only when the device/node identity is already paired. Self-declared `client.id` values are not enough to write last-seen state.

## Auto-approval (macOS app)

The macOS app can optionally attempt a **silent approval** when both conditions hold: the request is marked `silent`, AND the app can verify an SSH connection to the gateway host using the same user. If silent approval fails, it falls back to the normal "Approve/Reject" prompt.

## Trusted-CIDR device auto-approval

WS device pairing for `role: node` remains manual by default. For private node networks where the Gateway already trusts the network path, operators can opt in with explicit CIDRs or exact IPs:

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

The security boundary on this opt-in is narrow: it is disabled when `gateway.nodes.pairing.autoApproveCidrs` is unset; no blanket LAN or private-network auto-approve mode exists; only fresh `role: node` device pairing with no requested scopes is eligible; operator, browser, Control UI, and WebChat clients stay manual; role, scope, metadata, and public-key upgrades stay manual; and same-host loopback trusted-proxy header paths are **not** eligible because that path can be spoofed by local callers.

## Metadata-upgrade auto-approval

When an already paired device reconnects with only non-sensitive metadata changes (for example, display name or client platform hints), OpenClaw treats that as a `metadata-upgrade`. Silent auto-approval here is narrow: it applies only to trusted non-browser local reconnects that already proved possession of local or shared credentials, including same-host native app reconnects after OS version metadata changes. Browser/Control UI clients and remote clients still use the explicit re-approval flow. Scope upgrades (read to write/admin) and public key changes are **not** eligible for metadata-upgrade auto-approval — they stay as explicit re-approval requests.

## QR pairing helpers

`/pair qr` renders the pairing payload as structured media so mobile and browser clients can scan it directly. Deleting a device also sweeps any stale pending pairing requests for that device id, so `nodes pending` does not show orphaned rows after a revoke.

## Locality and forwarded headers

Gateway pairing treats a connection as loopback only when **both** the raw socket **and** any upstream proxy evidence agree. If a request arrives on loopback but carries `Forwarded`, any `X-Forwarded-*`, or `X-Real-IP` header evidence, that forwarded-header evidence disqualifies the loopback locality claim. The pairing path then requires **explicit approval** instead of silently treating the request as a same-host connect. The trusted-proxy-auth doc covers the equivalent rule on operator auth.

## Storage (local, private)

Pairing state is stored under the Gateway state directory (default `~/.openclaw`):

- `~/.openclaw/nodes/paired.json`
- `~/.openclaw/nodes/pending.json`

If you override `OPENCLAW_STATE_DIR`, the `nodes/` folder moves with it. Security notes: tokens are secrets, so treat `paired.json` as sensitive; and rotating a token requires re-approval (or deleting the node entry).

## Transport behavior

The transport is **stateless** — it does not store membership. If the Gateway is offline or pairing is disabled, nodes cannot pair. If the Gateway is in remote mode, pairing still happens against the **remote Gateway's store**.

**Source**: OpenClaw documentation — `gateway/pairing` (mirror `inbox/openclaw_docs/gateway/pairing.md`)
**Last Updated**: 2026-06-22
**Status**: Active
