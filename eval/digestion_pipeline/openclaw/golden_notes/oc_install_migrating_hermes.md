---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - migration
keywords:
  - openclaw migrating from hermes
  - openclaw migrate hermes
  - openclaw onboard flow import
  - hermes state import
  - migration provider preview backup
  - import secrets auth credentials
  - migrate dry-run json
  - conflict overwrite skipped
topics:
  - OpenClaw
  - Install / Migration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/migrating-hermes
access_control_group: ["general"]
---

# OpenClaw — Migrating from Hermes

## Overview

This note is the procedure for migrating an existing Hermes setup into a fresh OpenClaw install, mirroring the `install/migrating-hermes` source page. OpenClaw imports Hermes state through a **bundled migration provider** that previews everything before changing state, redacts secrets in plans and reports, and creates a verified backup before apply. The procedure covers the two import entry points (onboarding wizard vs the `openclaw migrate` CLI), what gets imported into live config vs what stays archive-only for manual review, the recommended preview → apply-with-backup → doctor → restart flow, conflict handling, the secret/credential-import flags, JSON output for CI/automation, and troubleshooting.

Imports require a fresh OpenClaw setup. If you already have local OpenClaw state, reset config, credentials, sessions, and the workspace first, or use `openclaw migrate` directly with `--overwrite` after reviewing the plan.

## Two ways to import

There are two paths into the same migration provider:

- **Onboarding wizard** — the fastest path. The wizard detects Hermes at `~/.hermes` and shows a preview before applying. Run `openclaw onboard --flow import`. To point at a specific source instead, run `openclaw onboard --import-from hermes --import-source ~/.hermes`.
- **CLI** — use `openclaw migrate` for scripted or repeatable runs (CI, fresh laptop, automation); see the `openclaw migrate` reference for full details. The two core commands are shown below. Add `--from <path>` when Hermes lives outside `~/.hermes`.

```bash
openclaw onboard --flow import                 # wizard: auto-detect ~/.hermes, preview, apply
openclaw migrate hermes --dry-run              # CLI: preview only
openclaw migrate apply hermes --yes            # CLI: apply with confirmation skipped
```

## What gets imported

The provider loads the following Hermes state into live OpenClaw config:

- **Model configuration** — the default model selection from Hermes `config.yaml`, plus configured model providers and custom OpenAI-compatible endpoints from `providers` and `custom_providers`.
- **MCP servers** — MCP server definitions from `mcp_servers` or `mcp.servers`.
- **Workspace files** — `SOUL.md` and `AGENTS.md` are copied into the OpenClaw agent workspace; `memories/MEMORY.md` and `memories/USER.md` are **appended** to the matching OpenClaw memory files instead of overwriting them.
- **Memory configuration** — memory config defaults for OpenClaw file memory. External memory providers such as Honcho are recorded as archive or manual-review items so you can move them deliberately.
- **Skills** — skills with a `SKILL.md` file under `skills/<name>/` are copied, along with per-skill config values from `skills.config`.
- **Auth credentials** — interactive `openclaw migrate` asks before importing auth credentials, with yes selected by default. Accepted imports include OpenCode OpenAI OAuth credentials from OpenCode `auth.json`, OpenCode and GitHub Copilot entries from OpenCode `auth.json`, and the supported `.env` keys. Hermes `auth.json` OAuth entries are legacy state and are surfaced as manual reauth/doctor work instead of imported into live auth. Use `--include-secrets` for non-interactive `openclaw migrate` credential import, `--no-auth-credentials` to skip it, or onboarding `--import-secrets` when importing from the onboarding wizard.

## What stays archive-only

The provider copies these into the migration report directory for manual review, but does **not** load them into live OpenClaw config or credentials: `plugins/`, `sessions/`, `logs/`, `cron/`, `mcp-tokens/`, and `state.db`. OpenClaw refuses to execute or trust this state automatically because the formats and trust assumptions can drift between systems. Move what you need by hand after reviewing the archive.

## Recommended flow

The recommended migration runs in four steps:

1. **Preview the plan** — `openclaw migrate hermes --dry-run`. The plan lists everything that will change, including conflicts, skipped items, and any sensitive items. Plan output redacts nested secret-looking keys.
2. **Apply with backup** — `openclaw migrate apply hermes --yes`. OpenClaw creates and verifies a backup before applying. This non-interactive example imports non-secret state. Run without `--yes` to answer the credential prompt, or add `--include-secrets` to include supported credentials in unattended runs.
3. **Run doctor** — `openclaw doctor`. Doctor reapplies any pending config migrations and checks for issues introduced during the import.
4. **Restart and verify** — `openclaw gateway restart` then `openclaw status`. Confirm the gateway is healthy and your imported model, memory, and skills are loaded.

```bash
openclaw migrate hermes --dry-run        # 1. preview (redacts secret-looking keys)
openclaw migrate apply hermes --yes      # 2. apply (verified backup created first)
openclaw doctor                          # 3. reapply pending migrations, check issues
openclaw gateway restart && openclaw status   # 4. restart + verify health
```

## Conflict handling

Apply refuses to continue when the plan reports conflicts (a file or config value already exists at the target). Rerun with `--overwrite` **only** when replacing the existing target is intentional; providers may still write item-level backups for overwritten files in the migration report directory. For a fresh OpenClaw install, conflicts are unusual — they typically appear when you re-run the import on a setup that already has user edits.

If a conflict surfaces mid-apply (for example, an unexpected race on a config file), Hermes marks remaining dependent config items as `skipped` with reason `blocked by earlier apply conflict` instead of writing them partially. The migration report records each blocked item so you can resolve the original conflict and rerun the import.

## Secrets

Interactive `openclaw migrate` asks whether to import detected auth credentials, with yes selected by default. The flag-driven options are:

- **Accept the prompt** — imports OpenCode OpenAI OAuth credentials from OpenCode `auth.json`, OpenCode and GitHub Copilot entries from OpenCode `auth.json`, and the supported `.env` keys. Hermes `auth.json` OAuth entries are reported for manual OpenAI reauth or doctor repair.
- **`--no-auth-credentials`** (or choose no at the prompt) — imports non-secret state only.
- **`--include-secrets`** — use when running unattended with `--yes`.
- **`--import-secrets`** (onboarding) — use when importing credentials from the onboarding wizard.
- **SecretRef-managed credentials** — configure the SecretRef source after the import completes.

## JSON output for automation

For CI and shared scripts, add `--json`. With `--json` and no `--yes`, apply prints the plan and does **not** mutate state — the safest mode for CI and shared scripts.

```bash
openclaw migrate hermes --dry-run --json
openclaw migrate apply hermes --json --yes
```

## Troubleshooting

- **Apply refuses with conflicts** — inspect the plan output. Each conflict identifies the source path and the existing target. Decide per item whether to skip, edit the target, or rerun with `--overwrite`.
- **Hermes lives outside `~/.hermes`** — pass `--from /actual/path` (CLI) or `--import-source /actual/path` (onboarding).
- **Onboarding refuses to import on an existing setup** — onboarding imports require a fresh setup. Either reset state and re-onboard, or use `openclaw migrate apply hermes` directly, which supports `--overwrite` and explicit backup control.
- **API keys did not import** — interactive `openclaw migrate` imports API keys only when you accept the credential prompt. Non-interactive `--yes` runs require `--include-secrets`; onboarding imports require `--import-secrets`. Only the supported `.env` keys are recognized; other variables in `.env` are ignored.

**Source**: OpenClaw documentation — `install/migrating-hermes` (mirror `inbox/openclaw_docs/install/migrating-hermes.md`)
**Last Updated**: 2026-06-22
**Status**: Active
