---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - update
keywords:
  - openclaw update command
  - update channel stable beta dev
  - update status repair wizard
  - update dry-run no-restart json
  - update tag dist-tag spec
  - update timeout yes
  - nix mode update disabled
  - openclaw --update shorthand
topics:
  - OpenClaw
  - CLI update command surface
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/update
access_control_group: ["general"]
---

# OpenClaw — `openclaw update` Command Surface

## Overview

This note documents the operator-facing command and option surface of `openclaw update` — the CLI command that safely updates OpenClaw and switches between the stable/beta/dev channels with a Gateway auto-restart. It mirrors the operator half of the `cli/update` source page: the npm/pnpm/bun pointer, `Usage`, `Options`, the `update status` / `update repair` / `update wizard` subcommands, the Nix-mode and downgrade guards, and the `--update` shorthand. The internal mechanics (what `update` does under the hood, the control-plane `update.run` response shapes, and the git-checkout flow) are documented separately in the sibling note **[oc_cli_update_flow](oc_cli_update_flow.md)**.

If you installed OpenClaw via **npm/pnpm/bun** (a global install with no git metadata), updates happen via the package-manager flow described on the `/install/updating` page rather than through a source checkout.

## Usage

The command takes a bare invocation, three named subcommands (`status`, `repair`, `wizard`), and a set of flags that can be combined with the bare update:

```bash
openclaw update
openclaw update status
openclaw update repair
openclaw update wizard
openclaw update --channel beta
openclaw update --channel dev
openclaw update --tag beta
openclaw update --tag main
openclaw update --dry-run
openclaw update --no-restart
openclaw update --yes
openclaw update --json
openclaw --update
```

## Options

The bare `openclaw update` accepts these flags:

- `--no-restart`: skip restarting the Gateway service after a successful update. Package-manager updates that do restart the Gateway verify the restarted service reports the expected updated version before the command succeeds.
- `--channel <stable|beta|dev>`: set the update channel (git + npm; persisted in config).
- `--tag <dist-tag|version|spec>`: override the package target for this update only. For package installs, `main` maps to `github:openclaw/openclaw#main`; GitHub/git source specs are packed into a temporary tarball before the staged global npm install.
- `--dry-run`: preview planned update actions (channel/tag/target/restart flow) without writing config, installing, syncing plugins, or restarting.
- `--json`: print machine-readable `UpdateRunResult` JSON, including `postUpdate.plugins.warnings` when corrupt or unloadable managed plugins need repair after the core update succeeds, beta-channel plugin fallback details when a plugin has no beta release, and `postUpdate.plugins.integrityDrifts` when npm plugin artifact drift is detected during post-update plugin sync.
- `--timeout <seconds>`: per-step timeout (default is 1800s).
- `--yes`: skip confirmation prompts (for example downgrade confirmation).

There is no `--verbose` flag on `openclaw update`. Per source, use `--dry-run` to preview the planned channel/tag/install/restart actions, `--json` for machine-readable results, and `openclaw update status --json` when you only need channel and availability details. For debugging Gateway logs around an update, console verbosity and file log level are separate: Gateway `--verbose` affects terminal/WebSocket output, while file logs require `logging.level: "debug"` or `"trace"` in config (see the `/gateway/logging` page).

### Guards: Nix mode and downgrades

In Nix mode (`OPENCLAW_NIX_MODE=1`), mutating `openclaw update` runs are disabled — update the Nix source or flake input for this install instead (for nix-openclaw, the source points to the agent-first nix-openclaw Quick Start). Read-only `openclaw update status` and `openclaw update --dry-run` remain available in Nix mode. Separately, downgrades require confirmation because older versions can break configuration (the `--yes` flag skips this confirmation prompt).

## `update status`

`openclaw update status` shows the active update channel plus the git tag/branch/SHA (for source checkouts) and reports update availability. It is read-only.

```bash
openclaw update status
openclaw update status --json
openclaw update status --timeout 10
```

Options for `update status`:

- `--json`: print machine-readable status JSON.
- `--timeout <seconds>`: timeout for checks (default is 3s).

## `update repair`

`openclaw update repair` reruns update finalization after the core package already changed but later repair work did not finish cleanly. Per source, it is the supported recovery path when `openclaw update` installed the new core package but post-core plugin sync, managed npm plugin metadata, registry refresh, or doctor repair still needs to converge.

```bash
openclaw update repair
openclaw update repair --channel beta
openclaw update repair --json
```

Options for `update repair`:

- `--channel <stable|beta|dev>`: persist the update channel before repair and run plugin convergence against that channel.
- `--json`: print machine-readable finalization JSON.
- `--timeout <seconds>`: timeout for repair steps (default `1800`).
- `--yes`: skip confirmation prompts.
- `--no-restart`: accepted for update command parity; repair never restarts the Gateway.

Per source, `openclaw update repair` runs `openclaw doctor --fix`, reloads the repaired config and install records, syncs tracked plugins for the active update channel, updates managed npm plugin installs, repairs missing configured plugin payloads, refreshes the plugin registry, and writes the converged install-record metadata. It does not install a new core package and does not restart the Gateway.

## `update wizard`

`openclaw update wizard` is an interactive flow to pick an update channel and confirm whether to restart the Gateway after updating (the default is to restart). If you select `dev` without a git checkout, the wizard offers to create one.

Options for `update wizard`:

- `--timeout <seconds>`: timeout for each update step (default `1800`).

## `--update` shorthand

`openclaw --update` rewrites to `openclaw update` (per source, useful for shells and launcher scripts).

**Source**: OpenClaw documentation — `cli/update` (mirror `inbox/openclaw_docs/cli/update.md`), operator command-surface half
**Last Updated**: 2026-06-22
**Status**: Active
