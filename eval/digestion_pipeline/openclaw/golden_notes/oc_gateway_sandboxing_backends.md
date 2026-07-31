---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - sandboxing
keywords:
  - openclaw sandbox backend
  - docker ssh openshell backend
  - agents.defaults.sandbox.backend
  - sandbox workspace access
  - docker.binds custom bind mounts
  - openclaw-sandbox bookworm-slim image
  - setupCommand one-time container setup
  - sandbox-setup.sh build image
  - openshell mirror remote workspace mode
topics:
  - OpenClaw
  - Sandboxing Backends
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/sandboxing
access_control_group: ["general"]
---

# OpenClaw — Configuring a Sandbox Backend

## Overview

This note is the **procedure** for choosing and configuring an OpenClaw sandbox backend, mirroring the `gateway/sandboxing` source page: selecting among the Docker / SSH / OpenShell backends and granting workspace access. The image-building, custom bind mounts, one-time `setupCommand`, and minimal enable example are split into the sibling [oc_gateway_sandboxing_images_binds](oc_gateway_sandboxing_images_binds.md); the conceptual model (what gets sandboxed, modes, scope, tool policy/escape hatches, multi-agent overrides) is in [oc_gateway_sandboxing_model](oc_gateway_sandboxing_model.md). Backend selection is config-driven via `agents.defaults.sandbox.backend` (or per-agent `agents.list[].sandbox`).

## Choosing a backend

`agents.defaults.sandbox.backend` controls **which runtime** provides the sandbox: `"docker"` (the default when sandboxing is enabled), `"ssh"` (generic SSH-backed remote sandbox runtime), or `"openshell"` (OpenShell-backed sandbox runtime). SSH-specific config lives under `agents.defaults.sandbox.ssh`; OpenShell-specific config lives under `plugins.entries.openshell.config`. The source decision matrix:

| | Docker | SSH | OpenShell |
| --- | --- | --- | --- |
| **Where it runs** | Local container | Any SSH-accessible host | OpenShell managed sandbox |
| **Setup** | `scripts/sandbox-setup.sh` | SSH key + target host | OpenShell plugin enabled |
| **Workspace model** | Bind-mount or copy | Remote-canonical (seed once) | `mirror` or `remote` |
| **Network control** | `docker.network` (default: none) | Depends on remote host | Depends on OpenShell |
| **Browser sandbox** | Supported | Not supported | Not supported yet |
| **Bind mounts** | `docker.binds` | N/A | N/A |
| **Best for** | Local dev, full isolation | Offloading to a remote machine | Managed remote sandboxes with optional two-way sync |

### Docker backend

Sandboxing is off by default; if you enable it without choosing a backend, OpenClaw uses Docker. It executes tools and sandbox browsers locally via the Docker daemon socket (`/var/run/docker.sock`); container isolation is determined by Docker namespaces. To expose host GPUs, set `agents.defaults.sandbox.docker.gpus` (or per-agent `agents.list[].sandbox.docker.gpus`); the value is passed to Docker's `--gpus` flag as a separate argument (e.g. `"all"` or `"device=GPU-uuid"`) and requires a compatible host runtime such as NVIDIA Container Toolkit.

**Docker-out-of-Docker (DooD) constraints** apply if you deploy the Gateway itself as a Docker container that orchestrates sibling sandbox containers via the host's Docker socket. The `openclaw.json` `workspace` config MUST contain the **host's absolute path** (e.g. `/home/user/.openclaw/workspaces`), not the internal container path, because the Docker daemon evaluates paths in the host OS namespace. For FS-bridge parity the Gateway deployment MUST include an identical volume map linking the host namespace natively (`-v /home/user/.openclaw:/home/user/.openclaw`), since the Gateway evaluates the exact same host-path string from within its own container. When an OpenClaw sandbox is active, OpenClaw disables Codex app-server native Code Mode, user MCP servers, and app-backed plugin execution for that turn (those surfaces run from the Gateway-host app-server process, not the sandbox backend); shell access is exposed through sandbox-backed tools such as `sandbox_exec` and `sandbox_process`, and you must not mount the host Docker socket into agent sandbox containers or custom Codex sandboxes.

On Ubuntu/AppArmor hosts, native Codex `workspace-write` (run without active OpenClaw sandboxing) can fail before shell startup if the service user cannot create unprivileged user namespaces; when Docker sandbox egress is disabled (`network: "none"`, the default), Codex also needs an unprivileged network namespace. Common symptoms are `bwrap: setting up uid map: Permission denied` and `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` — run `openclaw doctor`, and if it reports a Codex bwrap namespace probe failure, prefer an AppArmor profile granting the required namespaces to the OpenClaw service process (`kernel.apparmor_restrict_unprivileged_userns=0` is a host-wide fallback with security tradeoffs). If you map paths internally without absolute host parity, OpenClaw throws an `EACCES` error writing its heartbeat because the fully qualified path string doesn't exist natively.

### SSH backend

Use `backend: "ssh"` to sandbox `exec`, file tools, and media reads on an arbitrary SSH-accessible machine. OpenClaw creates a per-scope remote root under `sandbox.ssh.workspaceRoot`; on first use after create or recreate it seeds that remote workspace from local once, after which `exec`, `read`, `write`, `edit`, `apply_patch`, prompt media reads, and inbound media staging run directly against the remote workspace over SSH. OpenClaw does **not** sync remote changes back automatically — this is a **remote-canonical** model where the remote SSH workspace becomes the real sandbox state after the initial seed. Host-local edits made outside OpenClaw after the seed are not visible remotely until recreate; `openclaw sandbox recreate` deletes the per-scope remote root and seeds again from local on next use. Browser sandboxing is not supported, and `sandbox.docker.*` settings do not apply.

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        backend: "ssh",
        scope: "session",
        workspaceAccess: "rw",
        ssh: {
          target: "user@gateway-host:22",
          workspaceRoot: "/tmp/openclaw-sandboxes",
          strictHostKeyChecking: true,
          updateHostKeys: true,
          identityFile: "~/.ssh/id_ed25519",
          certificateFile: "~/.ssh/id_ed25519-cert.pub",
          knownHostsFile: "~/.ssh/known_hosts",
          // Or use SecretRefs / inline contents instead of local files:
          // identityData: { source: "env", provider: "default", id: "SSH_IDENTITY" },
          // certificateData: { source: "env", provider: "default", id: "SSH_CERTIFICATE" },
          // knownHostsData: { source: "env", provider: "default", id: "SSH_KNOWN_HOSTS" },
        },
      },
    },
  },
}
```

For authentication material: `identityFile`/`certificateFile`/`knownHostsFile` use existing local files passed through OpenSSH config; `identityData`/`certificateData`/`knownHostsData` use inline strings or SecretRefs, which OpenClaw resolves through the normal secrets runtime snapshot, writes to temp files with mode `0600`, and deletes when the SSH session ends. If both `*File` and `*Data` are set for the same item, `*Data` wins for that SSH session.

### OpenShell backend

Use `backend: "openshell"` to sandbox tools in an OpenShell-managed remote environment (full setup, config reference, and workspace-mode comparison live on the dedicated OpenShell page). OpenShell reuses the same core SSH transport and remote filesystem bridge as the SSH backend, adding OpenShell-specific lifecycle (`sandbox create/get/delete`, `sandbox ssh-config`) plus the optional `mirror` workspace mode. OpenClaw asks OpenShell for sandbox-specific SSH config via `openshell sandbox ssh-config <name>`, writes it to a temp file, opens the SSH session, and reuses the `backend: "ssh"` remote filesystem bridge. Current limitations: sandbox browser not supported yet, `sandbox.docker.binds` not supported, and `sandbox.docker.*` runtime knobs apply only to the Docker backend.

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
          mode: "remote", // mirror | remote
          remoteWorkspaceDir: "/sandbox",
          remoteAgentWorkspaceDir: "/agent",
        },
      },
    },
  },
}
```

OpenShell has two workspace modes via `plugins.entries.openshell.config.mode`. With `mirror` (default), the local workspace stays canonical: OpenClaw syncs local files into OpenShell before exec and syncs the remote workspace back after exec (tradeoff: extra sync cost before and after exec). With `remote`, the OpenShell workspace is canonical after creation: OpenClaw seeds it once from local, then `exec`, `read`, `write`, `edit`, and `apply_patch` run directly against the remote workspace without syncing back (host-local edits after the seed are not seen until recreate, and recreate re-seeds from local). Choose `mirror` for a temporary execution environment, `remote` when the sandbox is the real workspace. OpenShell uses the normal lifecycle (`openclaw sandbox list` shows OpenShell and Docker runtimes; `openclaw sandbox recreate` deletes and recreates on next use; prune is backend-aware) — for `remote` mode, recreate deletes the canonical remote workspace and re-seeds from local; for `mirror` mode, recreate mainly resets the remote execution environment.

## Workspace access

`agents.defaults.sandbox.workspaceAccess` controls **what the sandbox can see**: `"none"` (default) — tools see a sandbox workspace under `~/.openclaw/sandboxes`; `"ro"` — mounts the agent workspace read-only at `/agent` (disables `write`/`edit`/`apply_patch`); `"rw"` — mounts it read/write at `/workspace`. With the OpenShell backend, `mirror` mode uses the local workspace as canonical between exec turns, `remote` mode uses the remote OpenShell workspace as canonical after the seed, and `"ro"`/`"none"` still restrict write behavior the same way. Inbound media is copied into the active sandbox workspace (`media/inbound/*`). The `read` tool is sandbox-rooted: with `"none"`, OpenClaw mirrors eligible skills into the sandbox workspace (`.../skills`); with `"rw"`, workspace skills are readable from `/workspace/skills` and eligible managed/bundled/plugin skills are materialized into the generated read-only path `/workspace/.openclaw/sandbox-skills/skills`.

The image-building, custom bind mounts (`docker.binds` + bind security), one-time `setupCommand`, network config, and the minimal enable example are documented in the sibling [oc_gateway_sandboxing_images_binds](oc_gateway_sandboxing_images_binds.md).

**Source**: OpenClaw documentation — `gateway/sandboxing` (mirror `inbox/openclaw_docs/gateway/sandboxing.md`), backend/workspace/binds/images/setupCommand sections
**Last Updated**: 2026-06-22
**Status**: Active
