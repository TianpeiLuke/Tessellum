---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - matrix
keywords:
  - openclaw matrix migration
  - matrix plugin upgrade in place
  - openclaw doctor --fix matrix
  - matrix pre-migration snapshot
  - matrix recovery key restore
  - matrix verify backup bootstrap
  - encrypted matrix migration
  - matrix room-key backup restore
topics:
  - OpenClaw
  - Matrix Channel Migration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/matrix-migration
access_control_group: ["general"]
---

# OpenClaw — Matrix Channel In-Place Migration

## Overview

This note is the operator procedure for upgrading from the previous public `matrix` plugin to the current OpenClaw Matrix implementation, mirroring the `channels/matrix-migration` source page (intro through "How encrypted migration works"). It covers the in-place upgrade contract, what the migration repairs automatically (pre-migration snapshots, sync/crypto store moves, room-key backup restore), the encrypted-state limits the migration cannot recover, the step-by-step recommended upgrade flow (`doctor --fix` → verify status → recovery-key restore → device/self verify → backup reset/bootstrap), and the two-stage encrypted-migration mechanism. The full catalog of migration log/console messages (meaning + remediation), the "history still missing" checks, and the "start fresh" baseline are the companion note [oc_channels_matrix_migration_messages](oc_channels_matrix_migration_messages.md).

## In-Place Upgrade

For most users the upgrade from the previous public `matrix` plugin is in place — nothing is renamed or reinstalled under a new name. Specifically: the plugin stays `@openclaw/matrix`; the channel stays `matrix`; your config stays under `channels.matrix`; cached credentials stay under `~/.openclaw/credentials/matrix/`; and runtime state stays under `~/.openclaw/matrix/`.

The root `openclaw` package no longer bundles Matrix runtime code or Matrix SDK dependencies. If `openclaw channels status` shows Matrix is configured but the plugin is missing after an update, run `openclaw doctor --fix` or `openclaw plugins install @openclaw/matrix`. Do **not** install Matrix SDK packages into the root OpenClaw package.

## What the Migration Does Automatically

When the gateway starts, and when you run `openclaw doctor --fix`, OpenClaw tries to repair old Matrix state automatically. Before any actionable Matrix migration step mutates on-disk state, OpenClaw creates or reuses a focused recovery snapshot.

When you use `openclaw update`, the exact trigger depends on how OpenClaw is installed: source installs run `openclaw doctor --fix` during the update flow, then restart the gateway by default; package-manager installs update the package, run a non-interactive doctor pass, then rely on the default gateway restart so startup can finish Matrix migration; and `openclaw update --no-restart` defers startup-backed Matrix migration until you later run `openclaw doctor --fix` and restart the gateway.

Automatic migration covers: creating or reusing a pre-migration snapshot under `~/Backups/openclaw-migrations/`; reusing your cached Matrix credentials; keeping the same account selection and `channels.matrix` config; moving the oldest flat Matrix sync store into the current account-scoped location; moving the oldest flat Matrix crypto store into the current account-scoped location when the target account can be resolved safely; extracting a previously saved Matrix room-key backup decryption key from the old rust crypto store when that key exists locally; reusing the most complete existing token-hash storage root for the same Matrix account, homeserver, and user when the access token changes later; scanning sibling token-hash storage roots for pending encrypted-state restore metadata when the access token changed but the account/device identity stayed the same; and restoring backed-up room keys into the new crypto store on the next Matrix startup.

### Snapshot Details

OpenClaw writes a marker file at `~/.openclaw/matrix/migration-snapshot.json` after a successful snapshot so later startup and repair passes can reuse the same archive. These automatic Matrix migration snapshots back up config + state only (`includeWorkspace: false`). If Matrix only has warning-only migration state — for example because `userId` or `accessToken` is still missing — OpenClaw does not create the snapshot yet because no Matrix mutation is actionable. If the snapshot step fails, OpenClaw skips Matrix migration for that run instead of mutating state without a recovery point.

### Multi-Account Upgrades

The oldest flat Matrix store (`~/.openclaw/matrix/bot-storage.json` and `~/.openclaw/matrix/crypto/`) came from a single-store layout, so OpenClaw can only migrate it into one resolved Matrix account target. Already account-scoped legacy Matrix stores are detected and prepared per configured Matrix account.

## What the Migration Cannot Do Automatically

The previous public Matrix plugin did **not** automatically create Matrix room-key backups. It persisted local crypto state and requested device verification, but it did not guarantee that your room keys were backed up to the homeserver. That means some encrypted installs can only be migrated partially.

OpenClaw cannot automatically recover: local-only room keys that were never backed up; encrypted state when the target Matrix account cannot be resolved yet because `homeserver`, `userId`, or `accessToken` are still unavailable; automatic migration of one shared flat Matrix store when multiple Matrix accounts are configured but `channels.matrix.defaultAccount` is not set; custom plugin path installs that are pinned to a repo path instead of the standard Matrix package; and a missing recovery key when the old store had backed-up keys but did not keep the decryption key locally.

Current warning scope: custom Matrix plugin path installs are surfaced by both gateway startup and `openclaw doctor`. If your old installation had local-only encrypted history that was never backed up, some older encrypted messages may remain unreadable after the upgrade.

## Recommended Upgrade Flow

1. **Update OpenClaw and the Matrix plugin normally.** Prefer plain `openclaw update` without `--no-restart` so startup can finish the Matrix migration immediately.
2. **Run doctor.** If Matrix has actionable migration work, doctor will create or reuse the pre-migration snapshot first and print the archive path.

   ```bash
   openclaw doctor --fix
   ```

3. **Start or restart the gateway.**
4. **Check current verification and backup state:**

   ```bash
   openclaw matrix verify status
   openclaw matrix verify backup status
   ```

5. **Provide the recovery key.** Put the recovery key for the Matrix account you are repairing in an account-specific environment variable. For a single default account, `MATRIX_RECOVERY_KEY` is fine. For multiple accounts, use one variable per account, for example `MATRIX_RECOVERY_KEY_ASSISTANT`, and add `--account assistant` to the command.
6. **Restore the backup if a recovery key is needed.** If OpenClaw tells you a recovery key is needed, run the command for the matching account:

   ```bash
   printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin
   printf '%s\n' "$MATRIX_RECOVERY_KEY_ASSISTANT" | openclaw matrix verify backup restore --recovery-key-stdin --account assistant
   ```

7. **Verify the device (and self-verify cross-signing).** If this device is still unverified, run the command for the matching account:

   ```bash
   printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin
   printf '%s\n' "$MATRIX_RECOVERY_KEY_ASSISTANT" | openclaw matrix verify device --recovery-key-stdin --account assistant
   ```

   If the recovery key is accepted and backup is usable, but `Cross-signing verified` is still `no`, complete self-verification from another Matrix client with `openclaw matrix verify self`. Accept the request in another Matrix client, compare the emoji or decimals, and type `yes` only when they match. The command exits successfully only after `Cross-signing verified` becomes `yes`.
8. **(Optional) Start fresh for future messages.** If you are intentionally abandoning unrecoverable old history and want a fresh backup baseline, run `openclaw matrix verify backup reset --yes`.
9. **(Optional) Bootstrap a server-side backup.** If no server-side key backup exists yet, create one for future recoveries with `openclaw matrix verify bootstrap`.

## How Encrypted Migration Works

Encrypted migration is a two-stage process driven by startup or `openclaw doctor --fix`:

1. Startup or `openclaw doctor --fix` creates or reuses the pre-migration snapshot if encrypted migration is actionable.
2. Startup or `openclaw doctor --fix` inspects the old Matrix crypto store through the active Matrix plugin install.
3. If a backup decryption key is found, OpenClaw writes it into the new recovery-key flow and marks room-key restore as pending.
4. On the next Matrix startup, OpenClaw restores backed-up room keys into the new crypto store automatically.

If the old store reports room keys that were never backed up, OpenClaw warns instead of pretending recovery succeeded.

**Source**: OpenClaw documentation — `channels/matrix-migration` (mirror `inbox/openclaw_docs/channels/matrix-migration.md`)
**Last Updated**: 2026-06-22
**Status**: Active
