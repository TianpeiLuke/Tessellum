---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - secrets
keywords:
  - openclaw secrets command
  - secrets reload rpc
  - secrets audit findings
  - secretref configure planner
  - secrets apply scrub plan
  - plaintext residue audit
  - allow-exec secretref
  - no rollback backups
topics:
  - OpenClaw
  - Secrets CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/secrets
access_control_group: ["general"]
---

# OpenClaw — The `openclaw secrets` Command

## Overview

This note is the operator procedure for `openclaw secrets`, the CLI used to manage SecretRefs and keep the active runtime snapshot healthy. It covers the four command roles (`reload`, `audit`, `configure`, `apply`), the recommended operator loop, and per-subcommand mechanics — the `secrets.reload` gateway RPC and its atomic snapshot swap, the read-only `audit` scan targets and finding codes, the interactive `configure` planner, applying a saved scrub plan with `apply`, the deliberate no-rollback-backup safety model, and the worked example. It mirrors the `cli/secrets` source page; commands, flags, RPC names, config keys, and finding codes are copied verbatim from the source. Gateway-side and reference content (`/gateway/secrets`, `/reference/secretref-credential-surface`, `/gateway/secrets-plan-contract`, `/gateway/security`) is linked, not duplicated.

## Command Roles and the Operator Loop

`openclaw secrets` manages SecretRefs and keeps the active runtime snapshot healthy. The page defines four command roles:

- **`reload`** — gateway RPC (`secrets.reload`) that re-resolves refs and swaps the runtime snapshot only on full success (no config writes).
- **`audit`** — read-only scan of configuration/auth/generated-model stores and legacy residues for plaintext, unresolved refs, and precedence drift (exec refs are skipped unless `--allow-exec` is set).
- **`configure`** — interactive planner for provider setup, target mapping, and preflight (TTY required).
- **`apply`** — execute a saved plan (`--dry-run` for validation only; dry-run skips exec checks by default, and write mode rejects exec-containing plans unless `--allow-exec` is set), then scrub targeted plaintext residues.

The recommended operator loop runs audit, configure, dry-run apply, write apply, re-audit, then reload:

```bash
openclaw secrets audit --check
openclaw secrets configure
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets audit --check
openclaw secrets reload
```

If your plan includes `exec` SecretRefs/providers, pass `--allow-exec` on both dry-run and write apply commands. For CI/gates the exit codes matter: `audit --check` returns `1` on findings, and unresolved refs return `2`. The page links the [Secrets Management](https://docs.openclaw.ai/gateway/secrets) guide, the [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface), and the [Security](https://docs.openclaw.ai/gateway/security) guide for the broader model.

## Reload Runtime Snapshot

`secrets reload` re-resolves secret refs and atomically swaps the runtime snapshot:

```bash
openclaw secrets reload
openclaw secrets reload --json
openclaw secrets reload --url ws://127.0.0.1:18789 --token <token>
```

It uses gateway RPC method `secrets.reload`. If resolution fails, the gateway keeps the last-known-good snapshot and returns an error (no partial activation). The JSON response includes `warningCount`. Options are `--url <url>`, `--token <token>`, `--timeout <ms>`, and `--json`.

## Audit

`secrets audit` is a read-only scan of OpenClaw state for: plaintext secret storage; unresolved refs; precedence drift (`auth-profiles.json` credentials shadowing `openclaw.json` refs); generated `agents/*/agent/models.json` residues (provider `apiKey` values and sensitive provider headers); and legacy residues (legacy auth store entries, OAuth reminders). Sensitive provider header detection is name-heuristic based, matching common auth/credential header names and fragments such as `authorization`, `x-api-key`, `token`, `secret`, `password`, and `credential`.

```bash
openclaw secrets audit
openclaw secrets audit --check
openclaw secrets audit --json
openclaw secrets audit --allow-exec
```

Exit behavior: `--check` exits non-zero on findings; unresolved refs exit with a higher-priority non-zero code. The report shape highlights are: `status` (`clean | findings | unresolved`); `resolution` (`refsChecked`, `skippedExecRefs`, `resolvabilityComplete`); and `summary` (`plaintextCount`, `unresolvedRefCount`, `shadowedRefCount`, `legacyResidueCount`). The finding codes are `PLAINTEXT_FOUND`, `REF_UNRESOLVED`, `REF_SHADOWED`, and `LEGACY_RESIDUE`.

## Configure (Interactive Helper)

`secrets configure` builds provider and SecretRef changes interactively, runs preflight, and optionally applies them:

```bash
openclaw secrets configure
openclaw secrets configure --plan-out /tmp/openclaw-secrets-plan.json
openclaw secrets configure --apply --yes
openclaw secrets configure --providers-only
openclaw secrets configure --skip-provider-setup
openclaw secrets configure --agent ops
openclaw secrets configure --json
```

The flow runs in three stages: provider setup first (`add/edit/remove` for `secrets.providers` aliases); credential mapping second (select fields and assign `{source, provider, id}` refs); preflight and optional apply last. The flags are: `--providers-only` (configure `secrets.providers` only, skip credential mapping); `--skip-provider-setup` (skip provider setup and map credentials to existing providers); `--agent <id>` (scope `auth-profiles.json` target discovery and writes to one agent store); and `--allow-exec` (allow exec SecretRef checks during preflight/apply, which may execute provider commands).

Key notes from the source: `configure` requires an interactive TTY; you cannot combine `--providers-only` with `--skip-provider-setup`; it targets secret-bearing fields in `openclaw.json` plus `auth-profiles.json` for the selected agent scope, and supports creating new `auth-profiles.json` mappings directly in the picker flow; the canonical supported surface is the [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface); it performs preflight resolution before apply, and if preflight/apply includes exec refs you keep `--allow-exec` set for both steps. Generated plans default to scrub options (`scrubEnv`, `scrubAuthProfilesForProviderTargets`, `scrubLegacyAuthJson` all enabled), and the apply path is one-way for scrubbed plaintext values. Without `--apply`, the CLI still prompts `Apply this plan now?` after preflight; with `--apply` (and no `--yes`) it prompts an extra irreversible confirmation; `--json` prints the plan + preflight report, but the command still requires an interactive TTY.

The exec provider safety note covers path security: Homebrew installs often expose symlinked binaries under `/opt/homebrew/bin/*`; set `allowSymlinkCommand: true` only when needed for trusted package-manager paths, and pair it with `trustedDirs` (for example `["/opt/homebrew"]`); on Windows, if ACL verification is unavailable for a provider path OpenClaw fails closed, and for trusted paths only you can set `allowInsecurePath: true` on that provider to bypass path security checks.

## Apply a Saved Plan

`secrets apply` applies or preflights a plan generated previously:

```bash
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --allow-exec
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run --allow-exec
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --json
```

Exec behavior: `--dry-run` validates preflight without writing files; exec SecretRef checks are skipped by default in dry-run; write mode rejects plans that contain exec SecretRefs/providers unless `--allow-exec` is set; use `--allow-exec` to opt in to exec provider checks/execution in either mode. Plan contract details (allowed target paths, validation rules, and failure semantics) are in the [Secrets Apply Plan Contract](https://docs.openclaw.ai/gateway/secrets-plan-contract). What `apply` may update: `openclaw.json` (SecretRef targets + provider upserts/deletes); `auth-profiles.json` (provider-target scrubbing); legacy `auth.json` residues; and `~/.openclaw/.env` known secret keys whose values were migrated.

## Why No Rollback Backups

`secrets apply` intentionally does not write rollback backups containing old plaintext values. Safety comes from strict preflight + atomic-ish apply with best-effort in-memory restore on failure.

## Example

The page's worked example audits, configures, then re-audits:

```bash
openclaw secrets audit --check
openclaw secrets configure
openclaw secrets audit --check
```

If `audit --check` still reports plaintext findings, update the remaining reported target paths and rerun audit.

**Source**: OpenClaw documentation — `cli/secrets` (mirror `inbox/openclaw_docs/cli/secrets.md`)
**Last Updated**: 2026-06-22
**Status**: Active
