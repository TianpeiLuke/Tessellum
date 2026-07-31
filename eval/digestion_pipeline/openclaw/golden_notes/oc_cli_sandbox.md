---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - sandbox
keywords:
  - openclaw sandbox cli
  - sandbox explain list recreate
  - sandbox runtime recreation
  - docker ssh openshell backend
  - agents.defaults.sandbox config
  - sandbox registry migration sqlite
  - openclaw doctor --fix sandbox
topics:
  - OpenClaw
  - Sandbox CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/sandbox
access_control_group: ["general"]
---

# OpenClaw — Managing Sandbox Runtimes (`openclaw sandbox`)

## Overview

This note is the procedure for `openclaw sandbox`, the CLI that manages the isolated sandbox runtimes OpenClaw runs agents in for security. It mirrors the `cli/sandbox` source page: the three subcommands (`explain` to inspect effective policy, `list` to enumerate runtimes, `recreate` to force recreation with updated config), the use cases that require a recreate (Docker image, sandbox config, SSH target/auth, OpenShell source/policy/mode, and `setupCommand` changes), why recreation is needed (old runtimes survive config changes until pruned), the SQLite registry migration via `openclaw doctor --fix`, and the `agents.defaults.sandbox` configuration block. Deep sandboxing config semantics live in the `gateway/sandboxing` doc and are linked, not duplicated here.

## What the Sandbox Commands Are For

OpenClaw can run agents in isolated sandbox runtimes for security. The `sandbox` commands help you inspect and recreate those runtimes after updates or configuration changes. Today that usually means one of three backends:

- Docker sandbox containers.
- SSH sandbox runtimes when `agents.defaults.sandbox.backend = "ssh"`.
- OpenShell sandbox runtimes when `agents.defaults.sandbox.backend = "openshell"`.

For `ssh` and OpenShell `remote`, recreate matters more than with Docker: the remote workspace is canonical after the initial seed; `openclaw sandbox recreate` deletes that canonical remote workspace for the selected scope; and the next use seeds it again from the current local workspace.

## Commands

### `openclaw sandbox explain`

Inspect the **effective** sandbox mode/scope/workspace access, sandbox tool policy, and elevated gates (with fix-it config key paths). It accepts session/agent selectors and a JSON output mode:

```bash
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

### `openclaw sandbox list`

List all sandbox runtimes with their status and configuration. `--browser` narrows to browser containers only, and `--json` switches to JSON output:

```bash
openclaw sandbox list
openclaw sandbox list --browser  # List only browser containers
openclaw sandbox list --json     # JSON output
```

The output includes, per runtime: runtime name and status; backend (`docker`, `openshell`, etc.); config label and whether it matches current config; age (time since creation); idle time (time since last use); and associated session/agent.

### `openclaw sandbox recreate`

Remove sandbox runtimes to force recreation with updated config:

```bash
openclaw sandbox recreate --all                # Recreate all containers
openclaw sandbox recreate --session main       # Specific session
openclaw sandbox recreate --agent mybot        # Specific agent
openclaw sandbox recreate --browser            # Only browser containers
openclaw sandbox recreate --all --force        # Skip confirmation
```

The options are: `--all` (recreate all sandbox containers); `--session <key>` (recreate the container for a specific session); `--agent <id>` (recreate containers for a specific agent); `--browser` (only recreate browser containers); and `--force` (skip the confirmation prompt). Per the source page's Note, runtimes are automatically recreated when the agent is next used — `recreate` only removes them.

## Use cases

The source page enumerates the configuration changes that require a `recreate` so the new settings take effect.

**After updating a Docker image** — pull and tag the new image, point the config at it, then recreate:

```bash
# Pull new image
docker pull openclaw-sandbox:latest
docker tag openclaw-sandbox:latest openclaw-sandbox:bookworm-slim

# Update config to use new image
# Edit config: agents.defaults.sandbox.docker.image (or agents.list[].sandbox.docker.image)

# Recreate containers
openclaw sandbox recreate --all
```

**After changing sandbox configuration** — edit `agents.defaults.sandbox.*` (or `agents.list[].sandbox.*`), then `openclaw sandbox recreate --all` to apply the new config.

**After changing SSH target or SSH auth material** — edit `agents.defaults.sandbox.backend`, `agents.defaults.sandbox.ssh.target`, `agents.defaults.sandbox.ssh.workspaceRoot`, and the SSH auth keys (`ssh.identityFile` / `certificateFile` / `knownHostsFile`, or the inline `ssh.identityData` / `certificateData` / `knownHostsData`), then recreate. For the core `ssh` backend, recreate deletes the per-scope remote workspace root on the SSH target; the next run seeds it again from the local workspace.

**After changing OpenShell source, policy, or mode** — edit `agents.defaults.sandbox.backend`, `plugins.entries.openshell.config.from`, `plugins.entries.openshell.config.mode`, and `plugins.entries.openshell.config.policy`, then recreate. For OpenShell `remote` mode, recreate deletes the canonical remote workspace for that scope; the next run seeds it again from the local workspace.

**After changing `setupCommand`** — `openclaw sandbox recreate --all`, or scope to one agent with `openclaw sandbox recreate --agent family`.

**For a specific agent only** — update just one agent's containers with `openclaw sandbox recreate --agent alfred`.

## Why this is needed

When you update sandbox configuration, existing runtimes continue running with the old settings; runtimes are only pruned after 24h of inactivity; and regularly-used agents keep old runtimes alive indefinitely. Use `openclaw sandbox recreate` to force removal of old runtimes — they are recreated automatically with current settings when next needed. The source page's Tip recommends preferring `openclaw sandbox recreate` over manual backend-specific cleanup, because it uses the Gateway's runtime registry and avoids mismatches when scope or session keys change.

## Registry migration

OpenClaw stores sandbox runtime metadata in the shared SQLite state database. Older installs may still have legacy sandbox registry files at `~/.openclaw/sandbox/containers.json` and `~/.openclaw/sandbox/browsers.json`. Some upgrades may also have one JSON shard per container/browser under `~/.openclaw/sandbox/containers/` or `~/.openclaw/sandbox/browsers/`. Regular sandbox runtime reads do not rewrite those legacy sources. Run `openclaw doctor --fix` to migrate valid legacy entries into SQLite; invalid legacy files are quarantined so one bad old registry cannot hide current runtime entries.

## Configuration

Sandbox settings live in `~/.openclaw/openclaw.json` under `agents.defaults.sandbox` (per-agent overrides go in `agents.list[].sandbox`):

```jsonc
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all", // off, non-main, all
        "backend": "docker", // docker, ssh, openshell
        "scope": "agent", // session, agent, shared
        "docker": {
          "image": "openclaw-sandbox:bookworm-slim",
          "containerPrefix": "openclaw-sbx-",
          // ... more Docker options
        },
        "prune": {
          "idleHours": 24, // Auto-prune after 24h idle
          "maxAgeDays": 7, // Auto-prune after 7 days
        },
      },
    },
  },
}
```

**Source**: OpenClaw documentation — `cli/sandbox` (mirror `inbox/openclaw_docs/cli/sandbox.md`)
**Last Updated**: 2026-06-22
**Status**: Active
