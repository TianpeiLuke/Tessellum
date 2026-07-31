---
tags:
  - resource
  - documentation
  - openclaw
  - nodes
  - command_policy
keywords:
  - openclaw node command policy
  - two-gate command check
  - gateway.nodes allowCommands denyCommands
  - deny-wins command policy
  - plugin node-invoke policy
  - autoApproveCidrs node pairing
  - tools.exec host security node
  - dangerous node command opt-in
topics:
  - OpenClaw
  - Node Command Policy
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/nodes
access_control_group: ["general"]
---

# OpenClaw — Node Command Policy and `gateway.nodes` / `tools.exec` Config

## Overview

This note models the OpenClaw **node command-policy / permission model** and the `openclaw.json` config schema that backs it, mirroring the "Command policy" and "Config (`openclaw.json`)" sections of the `nodes` source page. A node command can only be invoked after passing a **two-gate** authorization check; default-allowed commands differ from dangerous/privacy-heavy commands that need explicit opt-in; plugin-owned node commands add a third gate; and first-time pairing can be auto-approved from trusted CIDRs. The config schema (`gateway.nodes.pairing.autoApproveCidrs` / `allowCommands` / `denyCommands` and `tools.exec.host` / `security` / `node`, plus a per-agent exec-node override) declares all of this.

## The two-gate command policy

Node commands must pass **two gates** before they can be invoked:

1. The node must declare the command in its WebSocket `connect.commands` list.
2. The gateway's platform policy must allow the declared command.

Both must be satisfied: a command the node never declared is not invocable, and a declared command the platform policy does not allow is also blocked. This is the authorization boundary applied to every authenticated, paired node before any command (raw `node.invoke`, `openclaw nodes …` CLI helpers, or agent tools) is forwarded.

## Default-allowed vs opt-in dangerous commands

Windows and macOS companion nodes allow safe declared commands such as `canvas.*`, `camera.list`, `location.get`, and `screen.snapshot` by default. Trusted nodes that advertise the `talk` capability or declare `talk.*` commands also allow declared push-to-talk commands (`talk.ptt.start`, `talk.ptt.stop`, `talk.ptt.cancel`, `talk.ptt.once`) by default, independent of platform label. Dangerous or privacy-heavy commands such as `camera.snap`, `camera.clip`, and `screen.record` still require explicit opt-in with `gateway.nodes.allowCommands`. `gateway.nodes.denyCommands` always wins over defaults and extra allowlist entries (**deny-wins**) — a `denyCommands` entry removes a command even when a platform default or an `allowCommands` entry would otherwise allow it.

## Plugin node-invoke policy

Plugin-owned node commands can add a **Gateway node-invoke policy**. That policy runs after the allowlist check and before forwarding to the node, so raw `node.invoke`, CLI helpers, and dedicated agent tools share the same plugin permission boundary. Dangerous plugin node commands still require explicit `gateway.nodes.allowCommands` opt-in — the plugin policy is an additional gate, not a bypass of the allowCommands opt-in for dangerous commands.

## Re-snapshotting on declared-command changes

After a node changes its declared command list, reject the old device pairing and approve the new request so the gateway stores the updated command snapshot. The gateway evaluates the platform policy against the snapshot it stored at pairing approval; re-approval is what refreshes that stored `connect.commands` snapshot so policy decisions reflect the node's current capabilities.

## CIDR auto-approve pairing

The `gateway.nodes.pairing.autoApproveCidrs` setting can auto-approve first-time node pairing from trusted networks (a CIDR list). It is **disabled when unset**. It **only** applies to first-time `role: node` requests **with no requested scopes**, and it does **not** auto-approve upgrades. This narrows auto-approve to the least-privileged first-pairing case from a trusted network segment, leaving scope upgrades to explicit operator approval.

## Config (`openclaw.json`)

Node-related settings live under `gateway.nodes` and `tools.exec`:

```json5
{
  gateway: {
    nodes: {
      // Auto-approve first-time node pairing from trusted networks (CIDR list).
      // Disabled when unset. Only applies to first-time role:node requests
      // with no requested scopes; does not auto-approve upgrades.
      pairing: {
        autoApproveCidrs: ["192.168.1.0/24"],
      },
      // Opt into dangerous/privacy-heavy node commands (camera.snap, etc.).
      allowCommands: ["camera.snap", "screen.record"],
      // Block exact command names even if defaults or allowCommands include them.
      denyCommands: ["camera.clip"],
    },
  },
  tools: {
    exec: {
      // Default exec host: "node" routes all exec calls to a paired node.
      host: "node",
      // Security mode for node exec: allow only approved/allowlisted commands.
      security: "allowlist",
      // Pin exec to a specific node (id or name). Omit to allow any node.
      node: "build-node",
    },
  },
}
```

Use exact node command names. `denyCommands` removes a command even when a platform default or `allowCommands` entry would otherwise allow it. The gateway configuration reference (`/gateway/configuration-reference#gateway-field-details`) documents the gateway node pairing and command-policy field details.

The `gateway.nodes` block governs **pairing and command policy**: `pairing.autoApproveCidrs` (trusted-CIDR first-pairing auto-approve), `allowCommands` (opt-in for dangerous/privacy-heavy commands), and `denyCommands` (exact-name block, deny-wins). The `tools.exec` block governs **where exec runs**: `host` (`"node"` routes all exec calls to a paired node), `security` (`"allowlist"` allows only approved/allowlisted commands), and `node` (pins exec to a specific node id or name; omit to allow any node).

### Per-agent exec node override

```json5
{
  agents: {
    list: [
      {
        id: "main",
        tools: { exec: { node: "build-node" } },
      },
    ],
  },
}
```

A per-agent `tools.exec.node` under `agents.list[]` overrides the global `tools.exec.node` for that agent, pinning that agent's `exec host=node` calls to the named node.

**Source**: OpenClaw documentation — `nodes` (mirror `inbox/openclaw_docs/nodes.md`), sections "Command policy" and "Config (`openclaw.json`)"
**Last Updated**: 2026-06-22
**Status**: Active
