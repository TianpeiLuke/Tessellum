---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - migration
keywords:
  - openclaw migrate command
  - migration provider plugin
  - preview-first apply
  - dry-run migration plan
  - include-secrets credential import
  - migrate apply overwrite conflicts
  - registerMigrationProvider detect plan apply
  - onboard flow import
topics:
  - OpenClaw
  - CLI Migration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/migrate
access_control_group: ["general"]
---

# OpenClaw — `openclaw migrate` Workflow, Flags, and Safety Model

## Overview

This note documents the `openclaw migrate` CLI command — how an operator imports state from another agent system INTO OpenClaw through a plugin-owned migration provider. It mirrors the generic-workflow portion of the `cli/migrate` source page: the command surface and every `--flag`, the preview-first safety model (itemized plan, secret redaction, verified backups, conflict refusal, `--overwrite`), the migration-provider plugin contract (`detect`/`plan`/`apply`), and onboarding integration. The per-provider import matrix — what the bundled Claude, Codex, and Hermes providers each import, the supported Hermes `.env` keys, and per-provider manual-review state — is documented in the sibling note `oc_cli_migrate_providers`, not here.

`openclaw migrate` imports state from another agent system through a plugin-owned migration provider. Bundled providers cover Codex CLI state, Claude, and Hermes; third-party plugins can register additional providers. For user-facing walkthroughs, the source page points to `Migrating from Claude` (`/install/migrating-claude`), `Migrating from Hermes` (`/install/migrating-hermes`), and the migration hub (`/install/migrating`).

## Commands

The command surface spans a plan/preview phase (`migrate <provider>`) and a mutating phase (`migrate apply <provider>`), plus the `migrate list` discovery command and the onboarding-driven import entry points. The documented examples are reproduced verbatim:

```bash
openclaw migrate list
openclaw migrate claude --dry-run
openclaw migrate codex --dry-run
openclaw migrate codex --skill gog-vault77-google-workspace
openclaw migrate codex --plugin google-calendar --dry-run
openclaw migrate codex --plugin google-calendar --verify-plugin-apps --dry-run
openclaw migrate hermes --dry-run
openclaw migrate hermes
openclaw migrate apply codex --yes --skill gog-vault77-google-workspace
openclaw migrate apply codex --yes --plugin google-calendar
openclaw migrate apply codex --yes
openclaw migrate apply claude --yes
openclaw migrate apply hermes --yes
openclaw migrate apply hermes --include-secrets --yes
openclaw onboard --flow import
openclaw onboard --import-from claude --import-source ~/.claude
openclaw onboard --import-from hermes --import-source ~/.hermes
```

`openclaw migrate list` shows installed providers. Run `openclaw migrate <provider>` (optionally with `--dry-run`) to build and inspect the plan; run `openclaw migrate apply <provider>` to mutate state (which still previews and prompts unless `--yes` is set).

## Flags

Every documented `<ParamField>` flag, verbatim from source:

- **`<provider>`** (string) — Name of a registered migration provider, for example `hermes`. Run `openclaw migrate list` to see installed providers.
- **`--dry-run`** (boolean) — Build the plan and exit without changing state.
- **`--from <path>`** (string) — Override the source state directory. Hermes defaults to `~/.hermes`.
- **`--include-secrets`** (boolean) — Import supported credentials without prompting. Interactive apply asks before importing detected auth credentials, with yes selected by default; non-interactive `--yes` requires `--include-secrets` to import them.
- **`--no-auth-credentials`** (boolean) — Skip auth credential import, including the interactive prompt.
- **`--overwrite`** (boolean) — Allow apply to replace existing targets when the plan reports conflicts.
- **`--yes`** (boolean) — Skip the confirmation prompt. Required in non-interactive mode.
- **`--skill <name>`** (string) — Select one skill copy item by skill name or item id. Repeat the flag to migrate multiple skills. When omitted, interactive Codex migrations show a checkbox selector and non-interactive migrations keep all planned skills.
- **`--plugin <name>`** (string) — Select one Codex plugin install item by plugin name or item id. Repeat the flag to migrate multiple Codex plugins. When omitted, interactive Codex migrations show a native Codex plugin checkbox selector and non-interactive migrations keep all planned plugins. This only applies to source-installed `openai-curated` Codex plugins discovered by the Codex app-server inventory.
- **`--verify-plugin-apps`** (boolean) — Codex only. Force a fresh source Codex app-server `app/list` traversal before planning native plugin activation. Off by default to keep migration planning fast.
- **`--no-backup`** (boolean) — Skip the pre-apply backup. Requires `--force` when local OpenClaw state exists.
- **`--force`** (boolean) — Required alongside `--no-backup` when apply would otherwise refuse to skip backup.
- **`--json`** (boolean) — Print the plan or apply result as JSON. With `--json` and no `--yes`, apply prints the plan and does not mutate state.

## Safety model

`openclaw migrate` is preview-first. The safety model has four guarantees (each is a source `Accordion`):

**Preview before apply.** The provider returns an itemized plan before anything changes, including conflicts, skipped items, and sensitive items. JSON plans, apply output, and migration reports redact nested secret-looking keys such as API keys, tokens, authorization headers, cookies, and passwords. `openclaw migrate apply <provider>` previews the plan and prompts before changing state unless `--yes` is set. In non-interactive mode, apply requires `--yes`.

**Backups.** Apply creates and verifies an OpenClaw backup before applying the migration. If no local OpenClaw state exists yet, the backup step is skipped and the migration can continue. To skip a backup when state exists, pass both `--no-backup` and `--force`.

**Conflicts.** Apply refuses to continue when the plan has conflicts. Review the plan, then rerun with `--overwrite` if replacing existing targets is intentional. Providers may still write item-level backups for overwritten files in the migration report directory.

**Secrets.** Interactive apply asks whether to import detected auth credentials, with yes selected by default. Use `--no-auth-credentials` to skip them, or use `--include-secrets` for unattended credential import with `--yes`.

## Plugin contract

Migration sources are plugins. A plugin declares its provider ids in `openclaw.plugin.json`:

```json
{
  "contracts": {
    "migrationProviders": ["hermes"]
  }
}
```

At runtime the plugin calls `api.registerMigrationProvider(...)`. The provider implements `detect`, `plan`, and `apply`. Core owns CLI orchestration, backup policy, prompts, JSON output, and conflict preflight. Core passes the reviewed plan into `apply(ctx, plan)`, and providers may rebuild the plan only when that argument is absent for compatibility.

Provider plugins can use `openclaw/plugin-sdk/migration` for item construction and summary counts, plus `openclaw/plugin-sdk/migration-runtime` for conflict-aware file copies, archive-only report copies, cached config-runtime wrappers, and migration reports.

## Onboarding integration

Onboarding can offer migration when a provider detects a known source. Both `openclaw onboard --flow import` and `openclaw setup --wizard --import-from hermes` use the same plugin migration provider and still show a preview before applying.

Onboarding imports require a fresh OpenClaw setup. Reset config, credentials, sessions, and the workspace first if you already have local state. Backup-plus-overwrite or merge imports are feature-gated for existing setups.

**Source**: OpenClaw documentation — `cli/migrate` (mirror `inbox/openclaw_docs/cli/migrate.md`)
**Last Updated**: 2026-06-22
**Status**: Active
