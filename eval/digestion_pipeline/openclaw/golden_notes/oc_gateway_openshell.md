---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - sandbox
keywords:
  - openclaw openshell backend
  - managed sandbox backend
  - mirror vs remote workspace mode
  - openshell-sandbox plugin
  - openclaw sandbox recreate
  - plugins.entries.openshell.config
  - ssh remote filesystem bridge
  - per-agent sandbox openshell
topics:
  - OpenClaw
  - Gateway Sandbox
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/openshell
access_control_group: ["general"]
---

# OpenClaw — Using OpenShell as a Managed Sandbox Backend

## Overview

This note is the operational procedure for running OpenShell as OpenClaw's managed sandbox backend instead of running Docker containers locally, mirroring the `gateway/openshell` source page. OpenShell delegates sandbox lifecycle to the `openshell` CLI, which provisions remote environments with SSH-based command execution; the OpenClaw plugin reuses the same core SSH transport and remote filesystem bridge as the generic SSH backend and adds OpenShell-specific lifecycle (`sandbox create/get/delete`, `sandbox ssh-config`) plus an optional `mirror` workspace mode. It walks through prerequisites, the quick-start enable flow, the load-bearing choice between `mirror` and `remote` workspace modes, the full `plugins.entries.openshell.config` reference, example configurations, sandbox lifecycle and when to recreate, the SSH-bridge security hardening, current limitations, and the internal create→ssh-config→bridge sequence.

## Prerequisites

Before enabling the backend you need: the OpenShell plugin installed (`openclaw plugins install @openclaw/openshell-sandbox`); the `openshell` CLI installed and on `PATH` (or a custom path set via `plugins.entries.openshell.config.command`); an OpenShell account with sandbox access; and the OpenClaw Gateway running on the host.

## Quick start

1. Install and enable the plugin, then set the sandbox backend. First install the plugin:

```bash
openclaw plugins install @openclaw/openshell-sandbox
```

Then set `agents.defaults.sandbox` to use the `openshell` backend and enable the plugin entry:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        backend: "openshell",
        scope: "session",
        workspaceAccess: "rw",
      },
    },
  },
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: {
          from: "openclaw",
          mode: "remote",
        },
      },
    },
  },
}
```

2. Restart the Gateway. On the next agent turn, OpenClaw creates an OpenShell sandbox and routes tool execution through it.
3. Verify with `openclaw sandbox list` and `openclaw sandbox explain`.

## Workspace modes

The workspace mode is the most important decision when using OpenShell, set via `plugins.entries.openshell.config.mode`.

### `mirror`

Use `mode: "mirror"` when you want the **local workspace to stay canonical**. Behavior: before `exec`, OpenClaw syncs the local workspace into the OpenShell sandbox; after `exec`, OpenClaw syncs the remote workspace back to the local workspace; file tools still operate through the sandbox bridge, but the local workspace remains the source of truth between turns. Best for: editing files locally outside OpenClaw and wanting those changes visible in the sandbox automatically; wanting the OpenShell sandbox to behave as much like the Docker backend as possible; and wanting the host workspace to reflect sandbox writes after each exec turn. The tradeoff is extra sync cost before and after each exec.

### `remote`

Use `mode: "remote"` when you want the **OpenShell workspace to become canonical**. Behavior: when the sandbox is first created, OpenClaw seeds the remote workspace from the local workspace once; after that, `exec`, `read`, `write`, `edit`, and `apply_patch` operate directly against the remote OpenShell workspace; OpenClaw does **not** sync remote changes back into the local workspace; and prompt-time media reads still work because file and media tools read through the sandbox bridge. Best for: when the sandbox should live primarily on the remote side, when you want lower per-turn sync overhead, and when you do not want host-local edits to silently overwrite remote sandbox state. Source warning: if you edit files on the host outside OpenClaw after the initial seed, the remote sandbox does **not** see those changes — use `openclaw sandbox recreate` to re-seed.

### Choosing a mode

| | `mirror` | `remote` |
| --- | --- | --- |
| **Canonical workspace** | Local host | Remote OpenShell |
| **Sync direction** | Bidirectional (each exec) | One-time seed |
| **Per-turn overhead** | Higher (upload + download) | Lower (direct remote ops) |
| **Local edits visible?** | Yes, on next exec | No, until recreate |
| **Best for** | Development workflows | Long-running agents, CI |

## Configuration reference

All OpenShell config lives under `plugins.entries.openshell.config`:

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `mode` | `"mirror"` or `"remote"` | `"mirror"` | Workspace sync mode |
| `command` | `string` | `"openshell"` | Path or name of the `openshell` CLI |
| `from` | `string` | `"openclaw"` | Sandbox source for first-time create |
| `gateway` | `string` | — | OpenShell gateway name (`--gateway`) |
| `gatewayEndpoint` | `string` | — | OpenShell gateway endpoint URL (`--gateway-endpoint`) |
| `policy` | `string` | — | OpenShell policy ID for sandbox creation |
| `providers` | `string[]` | `[]` | Provider names to attach when sandbox is created |
| `gpu` | `boolean` | `false` | Request GPU resources |
| `autoProviders` | `boolean` | `true` | Pass `--auto-providers` during sandbox create |
| `remoteWorkspaceDir` | `string` | `"/sandbox"` | Primary writable workspace inside the sandbox |
| `remoteAgentWorkspaceDir` | `string` | `"/agent"` | Agent workspace mount path (for read-only access) |
| `timeoutSeconds` | `number` | `120` | Timeout for `openshell` CLI operations |

Sandbox-level settings (`mode`, `scope`, `workspaceAccess`) are configured under `agents.defaults.sandbox` as with any backend; see the Sandboxing doc for the full matrix.

## Examples

The source page gives three configurations. The minimal `remote` setup needs only `backend: "openshell"` under `agents.defaults.sandbox` plus the enabled plugin entry with `from: "openclaw"` and `mode: "remote"`. A mirror-mode-with-GPU variant adds `scope: "agent"`, `workspaceAccess: "rw"`, and config `mode: "mirror"`, `gpu: true`, `providers: ["openai"]`, `timeoutSeconds: 180`. The per-agent example below sets `agents.defaults.sandbox` to `mode: "off"` and enables OpenShell only for one agent in `agents.list[]`, with a custom OpenShell `gateway`, `gatewayEndpoint`, and `policy`:

```json5
{
  agents: {
    defaults: {
      sandbox: { mode: "off" },
    },
    list: [
      {
        id: "researcher",
        sandbox: {
          mode: "all",
          backend: "openshell",
          scope: "agent",
          workspaceAccess: "rw",
        },
      },
    ],
  },
  plugins: {
    entries: {
      openshell: {
        enabled: true,
        config: {
          from: "openclaw",
          mode: "remote",
          gateway: "lab",
          gatewayEndpoint: "https://lab.example",
          policy: "strict",
        },
      },
    },
  },
}
```

## Lifecycle management

OpenShell sandboxes are managed through the normal sandbox CLI: `openclaw sandbox list` lists all sandbox runtimes (Docker + OpenShell), `openclaw sandbox explain` inspects the effective policy, and `openclaw sandbox recreate --all` recreates (deletes the remote workspace and re-seeds on next use):

```bash
openclaw sandbox list
openclaw sandbox explain
openclaw sandbox recreate --all
```

For `remote` mode, recreate is especially important: it deletes the canonical remote workspace for that scope, and the next use seeds a fresh remote workspace from the local workspace. For `mirror` mode, recreate mainly resets the remote execution environment because the local workspace remains canonical.

### When to recreate

Recreate (`openclaw sandbox recreate --all`) after changing any of these: `agents.defaults.sandbox.backend`, `plugins.entries.openshell.config.from`, `plugins.entries.openshell.config.mode`, or `plugins.entries.openshell.config.policy`.

## Security hardening

OpenShell pins the workspace root fd and rechecks sandbox identity before each read, so symlink swaps or a remounted workspace cannot redirect reads out of the intended remote workspace.

## Current limitations

- Sandbox browser is not supported on the OpenShell backend.
- `sandbox.docker.binds` does not apply to OpenShell.
- Docker-specific runtime knobs under `sandbox.docker.*` apply only to the Docker backend.

## How it works

The internal sequence is: (1) OpenClaw calls `openshell sandbox create` (with `--from`, `--gateway`, `--policy`, `--providers`, `--gpu` flags as configured); (2) OpenClaw calls `openshell sandbox ssh-config <name>` to get SSH connection details for the sandbox; (3) core writes the SSH config to a temp file and opens an SSH session using the same remote filesystem bridge as the generic SSH backend; (4) in `mirror` mode it syncs local to remote before exec, runs, then syncs back after exec; (5) in `remote` mode it seeds once on create, then operates directly on the remote workspace.

**Source**: OpenClaw documentation — `gateway/openshell` (mirror `inbox/openclaw_docs/gateway/openshell.md`)
**Last Updated**: 2026-06-22
**Status**: Active
