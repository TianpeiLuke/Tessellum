---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - uninstall
keywords:
  - openclaw uninstall
  - remove gateway service
  - uninstall state config workspace
  - uninstall macos app
  - uninstall dry-run
  - uninstall non-interactive yes
  - backup create before uninstall
topics:
  - OpenClaw
  - CLI Uninstall
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/uninstall
access_control_group: ["general"]
---

# OpenClaw — The `openclaw uninstall` Command

## Overview

This note documents the `openclaw uninstall` command, which removes the OpenClaw gateway service and local data while leaving the CLI itself installed. It mirrors the `cli/uninstall` source page: the selective-removal options (`--service`/`--state`/`--workspace`/`--app`/`--all`), the confirmation/automation flags (`--yes`/`--non-interactive`/`--dry-run`), the example invocations, and the operational notes — including the recommendation to run `openclaw backup create` first for a restorable snapshot.

## What It Removes

`openclaw uninstall` removes the gateway service plus local data; the CLI binary itself remains installed after the command runs. Removal is selective: each target is opted in with its own flag, so a bare `openclaw uninstall` (no target flags) does not blanket-remove everything. The package-manager uninstall of the CLI is a separate step not covered by this command (the command's stated effect is "the CLI remains").

## Options

The command exposes the following options (verbatim from the source page):

- `--service`: remove the gateway service
- `--state`: remove state and config
- `--workspace`: remove workspace directories
- `--app`: remove the macOS app
- `--all`: remove service, state, workspace, and app
- `--yes`: skip confirmation prompts
- `--non-interactive`: disable prompts; requires `--yes`
- `--dry-run`: print actions without removing files

`--all` is shorthand for removing service, state, workspace, and app together. `--dry-run` prints the actions that would be taken without removing any files, making it a safe preview of what a given flag combination would delete.

## Examples

```bash
openclaw backup create
openclaw uninstall
openclaw uninstall --service --yes --non-interactive
openclaw uninstall --state --workspace --yes --non-interactive
openclaw uninstall --all --yes
openclaw uninstall --dry-run
```

## Notes

The following operational notes apply (faithful to the source page):

- Run `openclaw backup create` first if you want a restorable snapshot before removing state or workspaces.
- `--state` preserves configured workspace directories unless `--workspace` is also selected.
- `--all` is shorthand for removing service, state, workspace, and app together.
- `--non-interactive` requires `--yes` — disabling prompts without also passing `--yes` is not valid, since there would be no way to confirm a destructive removal.

**Source**: OpenClaw documentation — `cli/uninstall` (mirror `inbox/openclaw_docs/cli/uninstall.md`)
**Last Updated**: 2026-06-22
**Status**: Active
