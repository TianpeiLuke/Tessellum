---
tags:
  - resource
  - documentation
  - openclaw
  - nodes
  - troubleshooting
keywords:
  - openclaw node troubleshooting
  - node pairing versus approvals
  - foreground only node tools
  - node permissions matrix
  - system.run exec approvals
  - node error codes
  - gateway node command policy
  - fast recovery loop
topics:
  - OpenClaw
  - Node Troubleshooting
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/nodes/troubleshooting
access_control_group: ["general"]
---

# OpenClaw — Node Troubleshooting (Pairing, Foreground, Permissions, Exec Approvals)

## Overview

This note is the procedure for diagnosing OpenClaw nodes that are visible in status but whose node tools fail — `camera.*`, `canvas.*`, `screen.*`, `location.*`, and `system.run`. It mirrors the `nodes/troubleshooting` source page: the diagnostic command ladder, the foreground-only capability rule for mobile nodes, the per-platform permissions matrix, the three-gate mental model (device pairing vs gateway node command policy vs exec approvals), the common node error codes, and the fast recovery loop.

Use this page when a node is connected and paired but a node tool call still fails. The central idea is that "connected" is not "allowed": a node tool can fail at three independent gates, and each gate has its own check and its own fix. Identifying which gate is failing — pairing, command policy, or exec approvals — is the diagnostic backbone of every section below.

## Command Ladder

Start with the general gateway/channel diagnostics, top to bottom, before narrowing to node-specific checks:

```bash
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Then run the node-specific checks:

```bash
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>
```

Healthy signals to confirm before going deeper:

- The node is connected and paired for role `node`.
- `nodes describe` includes the capability you are calling.
- Exec approvals show the expected mode/allowlist.

## Foreground Requirements

`canvas.*`, `camera.*`, and `screen.*` are **foreground only** on iOS/Android nodes. If the node app is backgrounded, these capabilities are unavailable even when the node is connected and paired.

Quick check and fix:

```bash
openclaw nodes describe --node <idOrNameOrIp>
openclaw nodes canvas snapshot --node <idOrNameOrIp>
openclaw logs --follow
```

If you see `NODE_BACKGROUND_UNAVAILABLE`, bring the node app to the foreground and retry.

## Permissions Matrix

Each node capability maps to an OS-level permission that differs by platform, and a typical failure code when that permission is missing or denied:

| Capability                   | iOS                                     | Android                                      | macOS node app                | Typical failure code           |
| ---------------------------- | --------------------------------------- | -------------------------------------------- | ----------------------------- | ------------------------------ |
| `camera.snap`, `camera.clip` | Camera (+ mic for clip audio)           | Camera (+ mic for clip audio)                | Camera (+ mic for clip audio) | `*_PERMISSION_REQUIRED`        |
| `screen.record`              | Screen Recording (+ mic optional)       | Screen capture prompt (+ mic optional)       | Screen Recording              | `*_PERMISSION_REQUIRED`        |
| `location.get`               | While Using or Always (depends on mode) | Foreground/Background location based on mode | Location permission           | `LOCATION_PERMISSION_REQUIRED` |
| `system.run`                 | n/a (node host path)                    | n/a (node host path)                         | Exec approvals required       | `SYSTEM_RUN_DENIED`            |

Note that `system.run` is not gated by an OS permission prompt on mobile (it is a node host path); on macOS it requires exec approvals rather than an OS toggle.

## Pairing Versus Approvals

These are three different gates — the central mental model of this page:

1. **Device pairing**: can this node connect to the gateway?
2. **Gateway node command policy**: is the RPC command ID allowed by `gateway.nodes.allowCommands` / `denyCommands` and platform defaults?
3. **Exec approvals**: can this node run a specific shell command locally?

Quick checks:

```bash
openclaw devices list
openclaw nodes status
openclaw approvals get --node <idOrNameOrIp>
openclaw approvals allowlist add --node <idOrNameOrIp> "/usr/bin/uname"
```

Resolution rules, by which gate is failing:

- If pairing is missing, approve the node device first.
- If `nodes describe` is missing a command, check the gateway node command policy and whether the node actually declared that command on connect.
- If pairing is fine but `system.run` fails, fix exec approvals/allowlist on that node.

Node pairing is an identity/trust gate, not a per-command approval surface. For `system.run`, the per-node policy lives in that node's exec approvals file (`openclaw approvals get --node ...`), not in the gateway pairing record.

For approval-backed `host=node` runs, the gateway also binds execution to the prepared canonical `systemRunPlan`. If a later caller mutates command/cwd or session metadata before the approved run is forwarded, the gateway rejects the run as an approval mismatch instead of trusting the edited payload.

## Common Node Error Codes

- `NODE_BACKGROUND_UNAVAILABLE` → app is backgrounded; bring it foreground.
- `CAMERA_DISABLED` → camera toggle disabled in node settings.
- `*_PERMISSION_REQUIRED` → OS permission missing/denied.
- `LOCATION_DISABLED` → location mode is off.
- `LOCATION_PERMISSION_REQUIRED` → requested location mode not granted.
- `LOCATION_BACKGROUND_UNAVAILABLE` → app is backgrounded but only While Using permission exists.
- `SYSTEM_RUN_DENIED: approval required` → exec request needs explicit approval.
- `SYSTEM_RUN_DENIED: allowlist miss` → command blocked by allowlist mode. On Windows node hosts, shell-wrapper forms like `cmd.exe /c ...` are treated as allowlist misses in allowlist mode unless approved via ask flow.

## Fast Recovery Loop

Run the node-state probes, watching logs for the specific failure code:

```bash
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>
openclaw logs --follow
```

If still stuck, work through the gates and OS permissions:

- Re-approve device pairing.
- Re-open the node app (foreground).
- Re-grant OS permissions.
- Recreate/adjust the exec approval policy.

**Source**: OpenClaw documentation — `nodes/troubleshooting` (mirror `inbox/openclaw_docs/nodes/troubleshooting.md`)
**Last Updated**: 2026-06-22
**Status**: Active
