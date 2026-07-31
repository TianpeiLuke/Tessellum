---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - nodes
keywords:
  - openclaw nodes
  - nodes list pending approve reject
  - nodes remove rename status
  - nodes invoke command params
  - node pairing approval scope
  - autoApproveCidrs
  - system.run blocked invoke
  - exec host node
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/nodes
access_control_group: ["general"]
---

# OpenClaw — `openclaw nodes` (Paired-Node Management and Invoke)

## Overview

This note is the procedure reference for `openclaw nodes`, the CLI surface that manages paired nodes (devices) and invokes node capabilities. It mirrors the `cli/nodes` source page: the common options shared across subcommands, the `list`/`pending`/`approve`/`reject`/`remove`/`rename`/`status` command catalog with its connection filters and pairing-removal semantics, the scope requirements that `approve` inherits from each pending request, and `nodes invoke` for direct node RPC (with `system.run` family blocked and routed to the sandboxed `exec` tool instead).

## Common Options

The following options are shared across the `nodes` subcommands: `--url`, `--token`, `--timeout`, `--json`. (`--url`/`--token` connect to the gateway WebSocket for RPC; `--json` requests machine-readable output. Per-command behavior of `--timeout` is *not specified in source* beyond being a common option.)

## Common Commands

```bash
openclaw nodes list
openclaw nodes list --connected
openclaw nodes list --last-connected 24h
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
openclaw nodes remove --node <id|name|ip>
openclaw nodes rename --node <id|name|ip> --name <displayName>
openclaw nodes status
openclaw nodes status --connected
openclaw nodes status --last-connected 24h
```

`nodes list` prints pending/paired tables, and paired rows include the most recent connect age (Last Connect). Use `--connected` to only show currently-connected nodes, and use `--last-connected <duration>` to filter to nodes that connected within a duration (e.g. `24h`, `7d`).

### Removing a node pairing

Use `nodes remove --node <id|name|ip>` to remove a node pairing. For a device-backed node this revokes the device's `node` role in `devices/paired.json` and disconnects its node-role sessions — a mixed-role device keeps its row and only loses the `node` role, while a node-only device is deleted; it also clears any matching legacy gateway-owned node pairing record. `operator.pairing` can remove non-operator node rows; a device-token caller revoking its own node role on a mixed-role device additionally needs `operator.admin`.

## Approval Scope

`openclaw nodes pending` only needs pairing scope. The `gateway.nodes.pairing.autoApproveCidrs` setting can skip the pending step only for explicitly trusted, first-time `role: node` device pairing; it is off by default and does not approve upgrades. `openclaw nodes approve <requestId>` inherits extra scope requirements from the pending request:

- commandless request: pairing only
- non-exec node commands: pairing + write
- `system.run` / `system.run.prepare` / `system.which`: pairing + admin

## Invoke

```bash
openclaw nodes invoke --node <id|name|ip> --command <command> --params <json>
```

Invoke flags:

- `--params <json>`: JSON object string (default `{}`).
- `--invoke-timeout <ms>`: node invoke timeout (default `15000`).
- `--idempotency-key <key>`: optional idempotency key.
- `system.run` and `system.run.prepare` are blocked here; use the `exec` tool with `host=node` for shell execution.

For shell execution on a node, use the `exec` tool with `host=node` instead of `openclaw nodes run`. The `nodes` CLI is now capability-focused: direct RPC via `nodes invoke`, plus pairing, camera, screen, location, Canvas, and notifications. Canvas commands are implemented by the bundled experimental Canvas plugin, and core keeps a compatibility hook so they remain under `openclaw nodes canvas`.

**Source**: OpenClaw documentation — `cli/nodes` (mirror `inbox/openclaw_docs/cli/nodes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
