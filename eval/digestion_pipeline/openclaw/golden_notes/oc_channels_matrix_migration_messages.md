---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - matrix
keywords:
  - matrix migration messages
  - openclaw doctor --fix matrix
  - matrix verify backup restore
  - matrix recovery key required
  - legacy matrix encrypted state
  - matrix migration snapshot
  - room key backup restore
  - defaultaccount not set
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

# OpenClaw — Matrix Migration Messages and Recovery Procedures

## Overview

This note is the diagnostic-message procedure for the OpenClaw Matrix in-place upgrade: it catalogs the log/console messages emitted during migration (by gateway startup and `openclaw doctor --fix`) and, for each, gives the meaning and the exact remediation command. It covers the four message groups from the source's "Common messages and what they mean" section — upgrade/detection, encrypted-state recovery, manual recovery, and custom-plugin-install — plus the two closing checklists. It mirrors the `channels/matrix-migration` page from "Common messages and what they mean" to the end; the upgrade flow and how-it-works mechanism live in the companion note `oc_channels_matrix_migration`.

## How to read these messages

Most messages name a state and an action: run the action for the matching account, then rerun `openclaw doctor --fix` or restart the gateway. For multi-account installs, append `--account <name>` to the verify commands and use a per-account recovery-key variable (e.g. `MATRIX_RECOVERY_KEY_ASSISTANT` with `--account assistant`). The recovery key is always supplied over stdin via `--recovery-key-stdin`.

## Upgrade and detection messages

Whether old on-disk Matrix state was found and whether it could be mapped to a current account.

- `Matrix plugin upgraded in place.` — old on-disk state was detected and migrated into the current layout. Fix: nothing unless the same output includes warnings.
- `Matrix migration snapshot created before applying Matrix upgrades.` — a recovery archive was created before mutating Matrix state. Fix: keep the printed archive path until you confirm migration succeeded.
- `Matrix migration snapshot reused before applying Matrix upgrades.` — an existing snapshot archive was reused instead of creating a duplicate. Fix: keep the printed archive path until you confirm migration succeeded.
- `Legacy Matrix state detected at ... but channels.matrix is not configured yet.` — old state exists but cannot be mapped to a current account because Matrix is not configured. Fix: configure `channels.matrix`, then rerun `openclaw doctor --fix` or restart the gateway.
- `Legacy Matrix state detected at ... but the new account-scoped target could not be resolved yet (need homeserver, userId, and access token for channels.matrix...).` — old state found, but the exact current account/device root is undetermined. Fix: start the gateway once with a working Matrix login, or rerun `openclaw doctor --fix` after cached credentials exist.
- `Legacy Matrix state detected at ... but multiple Matrix accounts are configured and channels.matrix.defaultAccount is not set.` — one shared flat Matrix store exists, but OpenClaw refuses to guess which named account should receive it. Fix: set `channels.matrix.defaultAccount` to the intended account, then rerun `openclaw doctor --fix` or restart the gateway.
- `Matrix legacy sync store not migrated because the target already exists (...)` — the new account-scoped location already has a sync or crypto store, so it was not overwritten. Fix: verify the current account is correct before manually removing or moving the conflicting target.
- `Failed migrating Matrix legacy sync store (...)` or `Failed migrating Matrix legacy crypto store (...)` — moving old Matrix state failed at the filesystem level. Fix: inspect filesystem permissions and disk state, then rerun `openclaw doctor --fix`.
- `Legacy Matrix encrypted state detected at ... but channels.matrix is not configured yet.` — an old encrypted store exists but there is no current config to attach it to. Fix: configure `channels.matrix`, then rerun `openclaw doctor --fix` or restart the gateway.
- `Legacy Matrix encrypted state detected at ... but the account-scoped target could not be resolved yet (need homeserver, userId, and access token for channels.matrix...).` — the encrypted store exists, but the current account/device it belongs to cannot be safely decided. Fix: start the gateway once with a working Matrix login, or rerun `openclaw doctor --fix` after cached credentials are available.
- `Legacy Matrix encrypted state detected at ... but multiple Matrix accounts are configured and channels.matrix.defaultAccount is not set.` — one shared flat legacy crypto store exists, but OpenClaw refuses to guess which named account should receive it. Fix: set `channels.matrix.defaultAccount` to the intended account, then rerun `openclaw doctor --fix` or restart the gateway.
- `Matrix migration warnings are present, but no on-disk Matrix mutation is actionable yet. No pre-migration snapshot was needed.` — old state was detected but migration is still blocked on missing identity or credential data. Fix: finish Matrix login or config setup, then rerun `openclaw doctor --fix` or restart the gateway.
- `Legacy Matrix encrypted state was detected, but the Matrix plugin helper is unavailable. Install or repair @openclaw/matrix so OpenClaw can inspect the old rust crypto store before upgrading.` — old encrypted state found, but the helper entrypoint that inspects that store could not load. Fix: reinstall/repair the plugin (`openclaw plugins install @openclaw/matrix`, or `openclaw plugins install ./path/to/local/matrix-plugin` for a repo checkout), then rerun `openclaw doctor --fix` or restart the gateway.
- `Matrix plugin helper path is unsafe: ... Reinstall @openclaw/matrix and try again.` — the helper file path escapes the plugin root or fails plugin boundary checks, so it was not imported. Fix: reinstall the Matrix plugin from a trusted path, then rerun `openclaw doctor --fix` or restart the gateway.
- `- Failed creating a Matrix migration snapshot before repair: ...` followed by `- Skipping Matrix migration changes for now. Resolve the snapshot failure, then rerun "openclaw doctor --fix".` — state mutation was refused because the recovery snapshot could not be created. Fix: resolve the backup error, then rerun `openclaw doctor --fix` or restart the gateway.
- `Failed migrating legacy Matrix client storage: ...` — the client-side fallback found old flat storage but the move failed; OpenClaw now aborts that fallback instead of silently starting fresh. Fix: inspect filesystem permissions or conflicts, keep the old state intact, and retry after fixing the error.
- `Matrix is installed from a custom path: ...` — Matrix is pinned to a path install, so mainline updates do not replace it with the standard package. Fix: reinstall with `openclaw plugins install @openclaw/matrix` to return to the default Matrix plugin.

## Encrypted-state recovery messages

The outcome of restoring room keys from the legacy encrypted-state backup into the new crypto store.

- `matrix: restored X/Y room key(s) from legacy encrypted-state backup` — backed-up room keys restored successfully into the new crypto store. Fix: usually nothing.
- `matrix: N legacy local-only room key(s) were never backed up and could not be restored automatically` — some old room keys existed only locally and were never uploaded to Matrix backup. Fix: expect some old encrypted history to remain unavailable unless you recover those keys manually from another verified client.
- `Legacy Matrix encrypted state for account "..." has backed-up room keys, but no local backup decryption key was found. Ask the operator to run "openclaw matrix verify backup restore --recovery-key-stdin" after upgrade if they have the recovery key.` — backup exists, but OpenClaw could not recover the recovery key automatically. Fix: run `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin`.
- `Failed inspecting legacy Matrix encrypted state for account "..." (...): ...` — the old encrypted store was found but could not be inspected safely enough to prepare recovery. Fix: rerun `openclaw doctor --fix`. If it repeats, keep the old state directory intact and recover using another verified Matrix client plus `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin`.
- `Legacy Matrix backup key was found for account "...", but .../recovery-key.json already contains a different recovery key. Leaving the existing file unchanged.` — a backup key conflict was detected, so the current recovery-key file was not overwritten. Fix: verify which recovery key is correct before retrying any restore command.
- `Legacy Matrix encrypted state for account "..." cannot be fully converted automatically because the old rust crypto store does not expose all local room keys for export.` — the hard limit of the old storage format. Fix: backed-up keys can still be restored, but local-only encrypted history may remain unavailable.
- `matrix: failed restoring room keys from legacy encrypted-state backup: ...` — restore was attempted but Matrix returned an error. Fix: run `openclaw matrix verify backup status`, then retry with `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin` if needed.

## Manual recovery messages

When a verify command needs you to load or fix the device's recovery key before it can restore room keys.

- `Backup key is not loaded on this device. Run 'openclaw matrix verify backup restore' to load it and restore old room keys.` — a backup key exists but is not active here. Fix: run `openclaw matrix verify backup restore`, or set `MATRIX_RECOVERY_KEY` and run `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin` if needed.
- `Store a recovery key with 'openclaw matrix verify device --recovery-key-stdin', then run 'openclaw matrix verify backup restore'.` — no recovery key is stored on this device. Fix: set `MATRIX_RECOVERY_KEY`, run `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin`, then restore the backup.
- `Backup key mismatch on this device. Re-run 'openclaw matrix verify device --recovery-key-stdin' with the matching recovery key.` — the stored key does not match the active Matrix backup. Fix: set `MATRIX_RECOVERY_KEY` to the correct key and run `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin`. Or, to abandon unrecoverable history, reset the baseline with `openclaw matrix verify backup reset --yes`; if the stored backup secret is broken, that reset may also recreate secret storage so the new key loads after restart.
- `Backup trust chain is not verified on this device. Re-run 'openclaw matrix verify device --recovery-key-stdin'.` — the backup exists but this device does not trust the cross-signing chain yet. Fix: set `MATRIX_RECOVERY_KEY` and run `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin`.
- `Matrix recovery key is required` — a recovery step ran without supplying the required recovery key. Fix: rerun with `--recovery-key-stdin`, e.g. `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin`.
- `Invalid Matrix recovery key: ...` — the provided key could not be parsed or matched the expected format. Fix: retry with the exact recovery key from your Matrix client or recovery-key file.
- `Matrix recovery key was applied, but this device still lacks full Matrix identity trust.` — the recovery key applied, but full cross-signing identity trust is not yet established; check the output for `Recovery key accepted`, `Backup usable`, `Cross-signing verified`, and `Device verified by owner`. Fix: run `openclaw matrix verify self`, accept the request in another Matrix client, compare the SAS, and type `yes` only when it matches (the command waits for full identity trust before reporting success). Use `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify bootstrap --recovery-key-stdin --force-reset-cross-signing` only when intentionally replacing the cross-signing identity.
- `Matrix key backup is not active on this device after loading from secret storage.` — secret storage did not produce an active backup session. Fix: verify the device first, then recheck with `openclaw matrix verify backup status`.
- `Matrix crypto backend cannot load backup keys from secret storage. Verify this device with 'openclaw matrix verify device --recovery-key-stdin' first.` — restore from secret storage is blocked until device verification completes. Fix: run `printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin` first.

## Custom plugin install messages

- `Matrix is installed from a custom path that no longer exists: ...` — the plugin install record points at a local path that is gone. Fix: reinstall with `openclaw plugins install @openclaw/matrix`, or from a repo checkout `openclaw plugins install ./path/to/local/matrix-plugin`.

## If encrypted history still does not come back

Run these checks in order. If the backup restores but some old rooms are still missing history, those keys were probably never backed up by the previous plugin.

```bash
openclaw matrix verify status --verbose
openclaw matrix verify backup status --verbose
printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin --verbose
```

## If you want to start fresh for future messages

If you accept losing unrecoverable old encrypted history and only want a clean backup baseline going forward, run these commands in order. If the device is still unverified afterward, finish verification from your Matrix client by comparing the SAS emoji or decimal codes and confirming they match.

```bash
openclaw matrix verify backup reset --yes
openclaw matrix verify backup status --verbose
openclaw matrix verify status
```

**Source**: OpenClaw documentation — `channels/matrix-migration` (mirror `inbox/openclaw_docs/channels/matrix-migration.md`), "Common messages and what they mean" through end
**Last Updated**: 2026-06-22
**Status**: Active
