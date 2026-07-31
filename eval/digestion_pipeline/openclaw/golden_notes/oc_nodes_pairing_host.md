---
tags:
  - resource
  - documentation
  - openclaw
  - nodes
  - pairing
keywords:
  - openclaw node pairing
  - device pairing role node
  - openclaw node run node install
  - remote node host system.run
  - ssh tunnel loopback gateway bind
  - exec approvals allowlist node
  - tools.exec.host node
  - headless node host
  - mac node mode
  - openclaw devices approve
topics:
  - OpenClaw
  - Nodes
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/nodes
access_control_group: ["general"]
---

# OpenClaw — Pairing and Running Nodes (Device Pairing + Remote Node Host)

## Overview

This procedure note covers how to pair OpenClaw **nodes** to a Gateway and how to stand up a **remote node host** so that `system.run` / `system.which` execute on a different machine than the one running the Gateway. It mirrors the intro and the pairing/host-setup half of the `nodes` source page: device pairing + approval scopes, the remote node host model (what runs where), starting a node host in foreground or as a service, connecting to a loopback-bound Gateway through an SSH tunnel, naming nodes, per-node-host exec allowlists, pointing `tools.exec` at a node, the cross-platform headless node host, and Mac node mode. The node *capability/command surface* (canvas, camera, location, SMS, device commands) and the *command-policy/config schema* are split into the sibling notes [oc_nodes_capabilities](oc_nodes_capabilities.md) and [oc_nodes_command_policy](oc_nodes_command_policy.md).

## What a Node Is

A **node** is a companion device (macOS / iOS / Android / headless) that connects to the Gateway **WebSocket** (the same port operators use) with `role: "node"` and exposes a command surface (e.g. `canvas.*`, `camera.*`, `device.*`, `notifications.*`, `system.*`) via `node.invoke`. Nodes are **peripherals, not gateways** — they do not run the gateway service, and messages from Telegram / WhatsApp / etc. land on the **gateway**, not on nodes. A legacy transport, the Bridge protocol (TCP JSONL), is historical only for current nodes. macOS can also run in **node mode**: the menubar app connects to the Gateway's WS server and exposes its local canvas/camera commands as a node, so `openclaw nodes …` works against that Mac; in remote gateway mode, browser automation is handled by the CLI node host (`openclaw node run` or the installed node service), not by the native app node.

## Pairing + Status

WS nodes use **device pairing**: a node presents a device identity during `connect`, and the Gateway creates a device pairing request for `role: node`. Approve it via the devices CLI (or the UI):

```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
```

If a node retries with changed auth details (role / scopes / public key), the prior pending request is superseded and a new `requestId` is created, so re-run `openclaw devices list` before approving. Key pairing behaviors:

- `nodes status` marks a node as **paired** when its device pairing role includes `node`.
- The device pairing record is the durable approved-role contract. Token rotation stays inside that contract; it cannot upgrade a paired node into a different role that pairing approval never granted.
- `node.pair.*` (CLI: `openclaw nodes pending/approve/reject/remove/rename`) is a separate gateway-owned node pairing store; it does **not** gate the WS `connect` handshake.
- `openclaw nodes remove --node <id|name|ip>` removes a node pairing. For a device-backed node it revokes the device's `node` role in `devices/paired.json` and disconnects that device's node-role sessions — a mixed-role device keeps its row and only loses the `node` role, while a node-only device row is deleted. It also clears any matching entry from the separate gateway-owned node pairing store. `operator.pairing` may remove non-operator node rows; a device-token caller revoking its own node role on a mixed-role device additionally needs `operator.admin`.

**Approval scope** follows the pending request's declared commands: a commandless request needs `operator.pairing`; non-exec node commands need `operator.pairing` + `operator.write`; and `system.run` / `system.run.prepare` / `system.which` need `operator.pairing` + `operator.admin`.

## Remote Node Host (`system.run`)

Use a **node host** when your Gateway runs on one machine and you want commands to execute on another. The model still talks to the **gateway**; the gateway forwards `exec` calls to the **node host** when `host=node` is selected. The split of responsibilities is:

- **Gateway host**: receives messages, runs the model, routes tool calls.
- **Node host**: executes `system.run` / `system.which` on the node machine.
- **Approvals**: enforced on the node host via `~/.openclaw/exec-approvals.json`.

Approval binding is strict: approval-backed node runs bind exact request context. For direct shell/runtime file executions, OpenClaw also best-effort binds one concrete local file operand and denies the run if that file changes before execution. If OpenClaw cannot identify exactly one concrete local file for an interpreter/runtime command, approval-backed execution is denied instead of pretending full runtime coverage — use sandboxing, separate hosts, or an explicit trusted allowlist/full workflow for broader interpreter semantics.

### Start a Node Host (Foreground)

On the node machine:

```bash
openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
```

### Remote Gateway via SSH Tunnel (Loopback Bind)

If the Gateway binds to loopback (`gateway.bind=loopback`, the default in local mode), remote node hosts cannot connect directly. Create an SSH tunnel and point the node host at the local end of the tunnel:

```bash
# Terminal A (keep running): forward local 18790 -> gateway 127.0.0.1:18789
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host

# Terminal B: export the gateway token and connect through the tunnel
export OPENCLAW_GATEWAY_TOKEN="<gateway-token>"
openclaw node run --host 127.0.0.1 --port 18790 --display-name "Build Node"
```

Authentication rules for the node host connection:

- `openclaw node run` supports token or password auth.
- Env vars are preferred: `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`.
- Config fallback is `gateway.auth.token` / `gateway.auth.password`.
- In local mode, the node host intentionally ignores `gateway.remote.token` / `gateway.remote.password`.
- In remote mode, `gateway.remote.token` / `gateway.remote.password` are eligible per remote precedence rules.
- If active local `gateway.auth.*` SecretRefs are configured but unresolved, node-host auth fails closed.
- Node-host auth resolution only honors `OPENCLAW_GATEWAY_*` env vars.

### Start a Node Host (Service)

```bash
openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node start
openclaw node restart
```

### Pair + Name

On the gateway host, list and approve the request with the same pairing commands shown above (`openclaw devices list`, `openclaw devices approve <requestId>`, `openclaw nodes status`). If the node retries with changed auth details, re-run `openclaw devices list` and approve the current `requestId`. Naming options: `--display-name` on `openclaw node run` / `openclaw node install` (persists in `~/.openclaw/node.json` on the node), or `openclaw nodes rename --node <id|name|ip> --name "Build Node"` (a gateway override).

### Allowlist the Commands

Exec approvals are **per node host**. Add allowlist entries from the gateway:

```bash
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/uname"
openclaw approvals allowlist add --node <id|name|ip> "/usr/bin/sw_vers"
```

Approvals live on the node host at `~/.openclaw/exec-approvals.json`.

### Point Exec at the Node

Configure defaults in the gateway config:

```bash
openclaw config set tools.exec.host node
openclaw config set tools.exec.security allowlist
openclaw config set tools.exec.node "<id-or-name>"
```

Or set it per session with `/exec host=node security=allowlist node=<id-or-name>`. Once set, any `exec` call with `host=node` runs on the node host (subject to the node allowlist/approvals). `host=auto` will not implicitly choose the node on its own, but an explicit per-call `host=node` request is allowed from `auto`; to make node exec the session default, set `tools.exec.host=node` or use `/exec host=node ...` explicitly. Related link-outs: [Node host CLI](https://docs.openclaw.ai/cli/node), [Exec tool](https://docs.openclaw.ai/tools/exec), [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals).

## Headless Node Host (Cross-Platform)

OpenClaw can run a **headless node host** (no UI) that connects to the Gateway WebSocket and exposes `system.run` / `system.which`. This is useful on Linux/Windows or for running a minimal node alongside a server; start it with the same foreground command minus the display name, `openclaw node run --host <gateway-host> --port 18789`. Operational notes for the headless host:

- Pairing is still required (the Gateway will show a device pairing prompt).
- The node host stores its node id, token, display name, and gateway connection info in `~/.openclaw/node.json`.
- Exec approvals are enforced locally via `~/.openclaw/exec-approvals.json`.
- On macOS, the headless node host executes `system.run` locally by default. Set `OPENCLAW_NODE_EXEC_HOST=app` to route `system.run` through the companion app exec host; add `OPENCLAW_NODE_EXEC_FALLBACK=0` to require the app host and fail closed if it is unavailable.
- Add `--tls` / `--tls-fingerprint` when the Gateway WS uses TLS.

## Mac Node Mode

The macOS menubar app connects to the Gateway WS server as a node, so `openclaw nodes …` works against this Mac. In remote mode, the app opens an SSH tunnel for the Gateway port and connects to `localhost`.

**Source**: OpenClaw documentation — `nodes` (mirror `inbox/openclaw_docs/nodes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
