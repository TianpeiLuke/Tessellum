---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - reset
keywords:
  - openclaw reset
  - reset local state
  - reset scope config creds sessions full
  - reset dry-run
  - reset non-interactive
  - backup create before reset
  - wipe config keep cli
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/reset
access_control_group: ["general"]
---

# OpenClaw — `openclaw reset` (Reset Local State)

## Overview

This note is the procedure for `openclaw reset`, the CLI command that resets OpenClaw's local config and state while keeping the CLI itself installed, mirroring the `cli/reset` source page. It covers the `--scope` choices (`config`, `config+creds+sessions`, `full`), the confirmation flags `--yes` and `--non-interactive`, the `--dry-run` preview, the worked example invocations, and the backup-first guidance — use it when you want to wipe local state without uninstalling, or to preview what a reset would remove before committing.

## What `openclaw reset` Does

`openclaw reset` resets local config/state and keeps the CLI installed. It is the local-state teardown verb: it removes the chosen tier of local data (config, and optionally credentials and sessions, up to a full wipe) but does not remove the `openclaw` binary, distinguishing it from an uninstall. Because it is destructive, the command is confirmation-gated by default and offers a non-destructive preview path.

## Options

The command exposes four options that select the destruction scope and govern confirmation behavior:

- `--scope <scope>` — selects what to remove. Accepted values are `config`, `config+creds+sessions`, or `full`. `config` resets local config; `config+creds+sessions` additionally removes credential stores and persisted sessions; `full` is the broadest state/retention wipe.
- `--yes` — skips confirmation prompts.
- `--non-interactive` — disables prompts; it requires `--scope` and `--yes`.
- `--dry-run` — prints the actions that would be taken without removing any files.

If you omit `--scope`, `openclaw reset` uses an interactive prompt to choose what to remove, and `--non-interactive` is only valid when both `--scope` and `--yes` are set.

## Examples

The source page lists the following invocations, including a backup-first preamble and one example per scope:

```bash
openclaw backup create
openclaw reset
openclaw reset --dry-run
openclaw reset --scope config --yes --non-interactive
openclaw reset --scope config+creds+sessions --yes --non-interactive
openclaw reset --scope full --yes --non-interactive
```

`openclaw reset` with no flags falls through to the interactive scope prompt; `openclaw reset --dry-run` previews the removal without deleting anything; the three `--scope ... --yes --non-interactive` forms run an unattended reset at the `config`, `config+creds+sessions`, and `full` tiers respectively (each satisfying the `--non-interactive` requirement that `--scope` and `--yes` both be set).

## Notes

The source page records three operational notes governing safe use:

- Run `openclaw backup create` first if you want a restorable snapshot before removing local state.
- If you omit `--scope`, `openclaw reset` uses an interactive prompt to choose what to remove.
- `--non-interactive` is only valid when both `--scope` and `--yes` are set.

**Source**: OpenClaw documentation — `cli/reset` (mirror `inbox/openclaw_docs/cli/reset.md`)
**Last Updated**: 2026-06-22
**Status**: Active
