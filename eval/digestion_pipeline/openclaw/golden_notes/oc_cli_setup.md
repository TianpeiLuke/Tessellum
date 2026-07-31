---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - setup
keywords:
  - openclaw setup command
  - initialize baseline config workspace
  - agents.defaults.workspace
  - wizard auto-trigger
  - non-interactive accept-risk onboarding
  - import-from hermes migration
  - remote gateway setup
  - nix mode setup refusal
topics:
  - OpenClaw
  - CLI Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/setup
access_control_group: ["general"]
---

# OpenClaw — `openclaw setup` (Initialize Config + Workspace)

## Overview

This note documents the `openclaw setup` command procedure: how it initializes OpenClaw's baseline config file and agent workspace, when it switches into the interactive onboarding wizard, why it refuses to write in Nix mode, and how it relates to the neighboring `onboard`, `configure`, `channels add`, and `migrate` commands. It mirrors the `cli/setup` source page — the short, first-run-oriented reference that an operator uses before exposing a gateway. Plain `openclaw setup` is the minimal baseline initializer; any onboarding flag escalates it into the full wizard journey.

## Purpose and Nix-Mode Refusal

`openclaw setup` initializes the baseline config and the agent workspace. With any onboarding flag present, it also runs the wizard. The command is intended for **mutable config installs** only. In Nix mode (environment variable `OPENCLAW_NIX_MODE=1`) OpenClaw refuses setup writes because the config file is managed by Nix; for Nix installs the page directs operators to the first-party nix-openclaw Quick Start (or the equivalent source config for another Nix package) rather than running `setup`.

## Options

The full flag surface, copied verbatim from the source Options table, is:

| Flag | Description |
| --- | --- |
| `--workspace <dir>` | Agent workspace directory (default `~/.openclaw/workspace`; stored as `agents.defaults.workspace`). |
| `--wizard` | Run interactive onboarding. |
| `--non-interactive` | Run onboarding without prompts. |
| `--accept-risk` | Acknowledge full-system agent access risk; required with `--non-interactive`. |
| `--mode <mode>` | Onboarding mode: `local` or `remote`. |
| `--import-from <provider>` | Migration provider to run during onboarding. |
| `--import-source <path>` | Source agent home for `--import-from`. |
| `--import-secrets` | Import supported secrets during onboarding migration. |
| `--remote-url <url>` | Remote Gateway WebSocket URL. |
| `--remote-token <token>` | Remote Gateway token (optional). |

The default workspace directory is `~/.openclaw/workspace`, persisted into config as `agents.defaults.workspace`. The `--accept-risk` flag (acknowledging full-system agent access risk) is **required** whenever `--non-interactive` is used. The `--mode` flag selects between `local` and `remote` onboarding, and `--remote-url`/`--remote-token` supply the remote Gateway WebSocket endpoint and optional token for `remote` mode.

### Wizard auto-trigger

`openclaw setup` runs the wizard when any of the following flags are explicitly present, **even without `--wizard`**:

`--wizard`, `--non-interactive`, `--accept-risk`, `--mode`, `--import-from`, `--import-source`, `--import-secrets`, `--remote-url`, `--remote-token`.

In other words, presence of any onboarding-related flag escalates a plain baseline initialization into the full interactive onboarding journey; only an entirely bare `openclaw setup` (or `openclaw setup --workspace ...`) stays in baseline-only mode.

## Examples

The source page gives the following invocation examples verbatim:

```bash
openclaw setup
openclaw setup --workspace ~/.openclaw/workspace
openclaw setup --wizard
openclaw setup --wizard --import-from hermes --import-source ~/.hermes
openclaw setup --non-interactive --accept-risk --mode remote --remote-url wss://gateway-host:18789 --remote-token <token>
```

These show, in order: bare baseline initialization; baseline initialization with an explicit workspace path; launching the interactive wizard; a wizard run migrating Hermes state from `~/.hermes`; and a fully non-interactive remote-mode onboarding that acknowledges the access risk and connects to a remote Gateway at `wss://gateway-host:18789`.

## Notes

- Plain `openclaw setup` initializes config and workspace **without** running the full onboarding flow.
- After plain setup, run `openclaw onboard` for the full guided journey, `openclaw configure` for targeted changes, or `openclaw channels add` to add channel accounts.
- If Hermes state is detected, interactive onboarding can offer migration automatically. Import onboarding requires a fresh setup; use `migrate` (`/cli/migrate`) for dry-run plans, backups, and overwrite mode outside onboarding.

**Source**: OpenClaw documentation — `cli/setup` (mirror `inbox/openclaw_docs/cli/setup.md`)
**Last Updated**: 2026-06-22
**Status**: Active
