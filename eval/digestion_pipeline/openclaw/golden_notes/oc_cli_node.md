---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - node_host
keywords:
  - openclaw node run
  - openclaw node install
  - headless node host
  - gateway websocket node
  - system.run system.which
  - node host gateway auth
  - node pairing role node
  - exec approvals systemRunPlan
  - tls fingerprint node
topics:
  - OpenClaw
  - CLI
  - Node Host
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/node
access_control_group: ["general"]
---

# OpenClaw — `openclaw node` (Headless Node Host)

## Overview

This note documents the `openclaw node` CLI command, which runs a **headless node host** that connects to the Gateway WebSocket and exposes `system.run` / `system.which` on the local machine — letting agents run commands on other machines in the network without installing a full macOS companion app there. It mirrors the `cli/node` source page in full: why you would use a node host, the zero-config browser proxy, foreground `run` vs background `install` (service) modes and their options, how a node host resolves Gateway auth from env/config (fail-closed on unresolved SecretRefs), first-connection device pairing (`role: node`), and the local exec-approval gating that protects `system.run`.

## Why use a node host?

Use a node host when you want agents to **run commands on other machines** in your network without installing a full macOS companion app there. Common use cases listed in the source are: running commands on remote Linux/Windows boxes (build servers, lab machines, NAS); keeping exec **sandboxed** on the gateway while delegating approved runs to other hosts; and providing a lightweight, headless execution target for automation or CI nodes. Execution is still guarded by **exec approvals** and per-agent allowlists on the node host, so you can keep command access scoped and explicit.

## Browser proxy (zero-config)

Node hosts automatically advertise a browser proxy if `browser.enabled` is not disabled on the node, which lets the agent use browser automation on that node without extra configuration. By default the proxy exposes the node's normal browser profile surface. If you set `nodeHost.browserProxy.allowProfiles`, the proxy becomes restrictive: non-allowlisted profile targeting is rejected, and persistent profile create/delete routes are blocked through the proxy. Disable it on the node if needed:

```json5
{
  nodeHost: {
    browserProxy: {
      enabled: false,
    },
  },
}
```

## Run (foreground)

Start a foreground node host (no service) with:

```bash
openclaw node run --host <gateway-host> --port 18789
```

Options:

- `--host <host>`: Gateway WebSocket host (default: `127.0.0.1`)
- `--port <port>`: Gateway WebSocket port (default: `18789`)
- `--tls`: Use TLS for the gateway connection
- `--tls-fingerprint <sha256>`: Expected TLS certificate fingerprint (sha256)
- `--node-id <id>`: Override node id (clears pairing token)
- `--display-name <name>`: Override the node display name

## Gateway auth for node host

`openclaw node run` and `openclaw node install` resolve gateway auth from config/env — there are **no `--token` / `--password` flags on node commands**. The resolution order and rules from the source are:

- `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD` are checked first.
- Then local config fallback: `gateway.auth.token` / `gateway.auth.password`.
- In local mode, the node host intentionally does **not** inherit `gateway.remote.token` / `gateway.remote.password`.
- If `gateway.auth.token` / `gateway.auth.password` is explicitly configured via SecretRef and unresolved, node auth resolution **fails closed** (no remote fallback masking).
- In `gateway.mode=remote`, the remote client fields (`gateway.remote.token` / `gateway.remote.password`) are also eligible per remote precedence rules.
- Node host auth resolution only honors `OPENCLAW_GATEWAY_*` env vars.

For a node connecting to a plaintext `ws://` Gateway, loopback, private IP literals, `.local`, and Tailnet `*.ts.net` hosts are accepted. For other trusted private-DNS names, set `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1`; without it, node startup **fails closed** and asks you to use `wss://`, an SSH tunnel, or Tailscale. This is a process-environment opt-in, not an `openclaw.json` config key. `openclaw node install` persists it into the supervised node service when it is present in the install command environment.

## Service (background)

Install a headless node host as a user service:

```bash
openclaw node install --host <gateway-host> --port 18789
```

Options (the foreground options plus two service-only flags):

- `--host <host>`: Gateway WebSocket host (default: `127.0.0.1`)
- `--port <port>`: Gateway WebSocket port (default: `18789`)
- `--tls`: Use TLS for the gateway connection
- `--tls-fingerprint <sha256>`: Expected TLS certificate fingerprint (sha256)
- `--node-id <id>`: Override node id (clears pairing token)
- `--display-name <name>`: Override the node display name
- `--runtime <runtime>`: Service runtime (`node` or `bun`)
- `--force`: Reinstall/overwrite if already installed

Manage the service:

```bash
openclaw node status
openclaw node start
openclaw node stop
openclaw node restart
openclaw node uninstall
```

Use `openclaw node run` for a foreground node host (no service). Service commands accept `--json` for machine-readable output. The node host retries Gateway restart and network closes in-process. If the Gateway reports a terminal token/password/bootstrap auth pause, the node host logs the close detail and exits non-zero so launchd/systemd can restart it with fresh config and credentials. Pairing-required pauses stay in the foreground flow so the pending request can be approved.

## Pairing

The first connection creates a pending device pairing request (`role: node`) on the Gateway. Approve it via:

```bash
openclaw devices list
openclaw devices approve <requestId>
```

On tightly controlled node networks, the Gateway operator can explicitly opt in to auto-approving first-time node pairing from trusted CIDRs:

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

This is disabled by default. It only applies to fresh `role: node` pairing with no requested scopes. Operator/browser clients, Control UI, WebChat, and role, scope, metadata, or public-key upgrades still require manual approval. If the node retries pairing with changed auth details (role/scopes/public key), the previous pending request is superseded and a new `requestId` is created — run `openclaw devices list` again before approval. The node host stores its node id, token, display name, and gateway connection info in `~/.openclaw/node.json`.

## Exec approvals

`system.run` is gated by local exec approvals. The source lists the approval surface as:

- `$OPENCLAW_STATE_DIR/exec-approvals.json`, or `~/.openclaw/exec-approvals.json` when the variable is unset
- the `/tools/exec-approvals` reference
- `openclaw approvals --node <id|name|ip>` (edit from the Gateway)

For approved async node exec, OpenClaw prepares a canonical `systemRunPlan` before prompting. The later approved `system.run` forward reuses that stored plan, so edits to command/cwd/session fields made after the approval request was created are **rejected** instead of changing what the node executes.

**Source**: OpenClaw documentation — `cli/node` (mirror `inbox/openclaw_docs/cli/node.md`)
**Last Updated**: 2026-06-22
**Status**: Active
