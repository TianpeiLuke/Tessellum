---
tags:
  - resource
  - documentation
  - openclaw
  - channels
  - matrix
keywords:
  - openclaw matrix encryption setup
  - matrix e2ee cross-signing
  - matrix verify device recovery key
  - matrix verify bootstrap backup
  - matrix sas verification
  - startupVerification matrix
  - matrix crypto store layout
  - dangerouslyAllowPrivateNetwork ssrf
  - channels.matrix.proxy
topics:
  - OpenClaw
  - Matrix Channel
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/channels/matrix
access_control_group: ["general"]
---

# OpenClaw — Matrix End-to-End Encryption and Verification Operations

## Overview

This note is the operator procedure for OpenClaw's Matrix end-to-end-encryption (E2EE) surface: the `openclaw matrix encryption setup` bootstrap, the three independent trust signals reported by `verify status`, recovery-key device verification over stdin, cross-signing bootstrap/repair, room-key backup status/restore/reset, the SAS verification command set, self-profile management, the startup-verification and crypto-store behavior of E2EE accounts, and the SSRF / proxy hardening for private homeservers. It mirrors the "Encryption and verification", "Profile management", the startup/crypto-store "Multi-account notes" accordions, "Private/LAN homeservers", and "Proxying Matrix traffic" sections of the `channels/matrix` source page. Per-account behavior, the flat config-key reference, runtime message behavior, and install/setup live in the sibling Matrix notes.

## Common command flags

All `openclaw matrix` commands accept `--verbose` (full diagnostics), `--json` (machine-readable output), and `--account <id>` (multi-account setups). Output is concise by default with quiet internal SDK logging; the examples below show the canonical form and you add the flags as needed. In encrypted (E2EE) rooms, outbound image events use `thumbnail_file` so image previews are encrypted alongside the full attachment, while unencrypted rooms still use plain `thumbnail_url` — no configuration is needed because the plugin detects E2EE state automatically.

## Enable encryption, status, and device verification

```bash
openclaw matrix encryption setup
openclaw matrix verify status
openclaw matrix verify status --include-recovery-key --json
printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify device --recovery-key-stdin
openclaw matrix verify self
```

`encryption setup` bootstraps secret storage and cross-signing, creates a room-key backup if needed, then prints status and next steps. Useful flags: `--recovery-key <key>` applies a recovery key before bootstrapping (prefer the stdin form below); `--force-reset-cross-signing` discards the current cross-signing identity and creates a new one (use only intentionally). For a new account you can enable E2EE at creation time with `openclaw matrix account add --homeserver https://matrix.example.org --access-token syt_xxx --enable-e2ee` (`--encryption` is an alias for `--enable-e2ee`). The manual config equivalent is the `channels.matrix` block with `encryption: true` alongside `homeserver`, `accessToken`, and `dm: { policy: "pairing" }`. The interactive setup wizard, when E2EE is enabled, writes the config and runs this same bootstrap.

`verify status` reports three independent trust signals (`--verbose` shows all of them): `Locally trusted` (trusted by this client only), `Cross-signing verified` (the SDK reports verification via cross-signing), and `Signed by owner` (signed by your own self-signing key — diagnostic only). `Verified by owner` becomes `yes` only when `Cross-signing verified` is `yes`; local trust or an owner signature alone is not enough. `--allow-degraded-local-state` returns best-effort diagnostics without preparing the Matrix account first, which is useful for offline or partially-configured probes.

The recovery key is sensitive — pipe it via stdin instead of passing it on the command line. Set `MATRIX_RECOVERY_KEY` (or `MATRIX_<ID>_RECOVERY_KEY` for a named account) and run `verify device --recovery-key-stdin`. The command reports three states: `Recovery key accepted` (Matrix accepted the key for secret storage or device trust), `Backup usable` (room-key backup can be loaded with the trusted recovery material), and `Device verified by owner` (this device has full Matrix cross-signing identity trust). It exits non-zero when full identity trust is incomplete, even if the recovery key unlocked backup material; in that case, finish self-verification from another Matrix client with `openclaw matrix verify self`, which waits for `Cross-signing verified: yes` before it exits successfully (tune the wait with `--timeout-ms <ms>`). The literal-key form `openclaw matrix verify device "<recovery-key>"` is also accepted, but the key ends up in your shell history.

## Bootstrap cross-signing and room-key backup

```bash
openclaw matrix verify bootstrap
openclaw matrix verify backup status
printf '%s\n' "$MATRIX_RECOVERY_KEY" | openclaw matrix verify backup restore --recovery-key-stdin
openclaw matrix verify backup reset --yes
```

`verify bootstrap` is the repair and setup command for encrypted accounts. In order, it: bootstraps secret storage (reusing an existing recovery key when possible); bootstraps cross-signing and uploads missing public keys; marks and cross-signs the current device; and creates a server-side room-key backup if one does not already exist. If the homeserver requires UIA to upload cross-signing keys, OpenClaw tries no-auth first, then `m.login.dummy`, then `m.login.password` (which requires `channels.matrix.password`). Useful flags: `--recovery-key-stdin` (pair with `printf '%s\n' "$MATRIX_RECOVERY_KEY" | …`) or `--recovery-key <key>`; and `--force-reset-cross-signing` to discard the current cross-signing identity (intentional only).

`backup status` shows whether a server-side backup exists and whether this device can decrypt it. `backup restore` imports backed-up room keys into the local crypto store; if the recovery key is already on disk you can omit `--recovery-key-stdin`. To replace a broken backup with a fresh baseline — which accepts losing unrecoverable old history and can also recreate secret storage if the current backup secret is unloadable — run `verify backup reset --yes`. Add `--rotate-recovery-key` only when you intentionally want the previous recovery key to stop unlocking the fresh backup baseline.

## Listing, requesting, and responding to verifications

`openclaw matrix verify list` lists pending verification requests for the selected account. `openclaw matrix verify request` sends a verification request from this OpenClaw account: `--own-user` requests self-verification (you accept the prompt in another Matrix client of the same user — e.g. `openclaw matrix verify request --own-user`), while `--user-id`/`--device-id`/`--room-id` target someone else (e.g. `openclaw matrix verify request --user-id @ops:example.org --device-id ABCDEF`); `--own-user` cannot be combined with the other targeting flags. For lower-level lifecycle handling — typically while shadowing inbound requests from another client — the following commands act on a specific request `<id>` (printed by `verify list` and `verify request`):

| Command | Purpose |
| --- | --- |
| `openclaw matrix verify accept <id>` | Accept an inbound request |
| `openclaw matrix verify start <id>` | Start the SAS flow |
| `openclaw matrix verify sas <id>` | Print the SAS emoji or decimals |
| `openclaw matrix verify confirm-sas <id>` | Confirm that the SAS matches what the other client shows |
| `openclaw matrix verify mismatch-sas <id>` | Reject the SAS when the emoji or decimals do not match |
| `openclaw matrix verify cancel <id>` | Cancel; takes optional `--reason <text>` and `--code <matrix-code>` |

`accept`, `start`, `sas`, `confirm-sas`, `mismatch-sas`, and `cancel` all accept `--user-id` and `--room-id` as DM follow-up hints when the verification is anchored to a specific direct-message room.

## Startup verification behavior

With `encryption: true`, `startupVerification` defaults to `"if-unverified"`. On startup an unverified device requests self-verification in another Matrix client, skipping duplicates and applying a cooldown (24 hours by default); tune with `startupVerificationCooldownHours` or disable with `startupVerification: "off"`. Startup also runs a conservative crypto bootstrap pass that reuses the current secret storage and cross-signing identity: if bootstrap state is broken, OpenClaw attempts a guarded repair even without `channels.matrix.password`, and if the homeserver requires password UIA, startup logs a warning and stays non-fatal; already-owner-signed devices are preserved. Matrix posts verification lifecycle notices into the strict DM verification room as `m.notice` messages — request, ready (with "Verify by emoji" guidance), start/completion, and SAS (emoji/decimal) details when available. Incoming requests from another Matrix client are tracked and auto-accepted, and for self-verification OpenClaw starts the SAS flow automatically and confirms its own side once emoji verification is available — you still need to compare and confirm "They match" in your Matrix client. Verification system notices are not forwarded to the agent chat pipeline.

## Deleted device and device hygiene

If `verify status` says the current device is no longer listed on the homeserver, create a new OpenClaw Matrix device. For password login:

```bash
openclaw matrix account add \
  --account assistant \
  --homeserver https://matrix.example.org \
  --user-id '@assistant:example.org' \
  --password '<password>' \
  --device-name OpenClaw-Gateway
```

For token auth, create a fresh access token in your Matrix client or admin UI, then re-run `openclaw matrix account add --account assistant --homeserver https://matrix.example.org --access-token '<token>'`. Replace `assistant` with the account ID from the failed command, or omit `--account` for the default account. Old OpenClaw-managed devices can accumulate; list and prune them with `openclaw matrix devices list` and `openclaw matrix devices prune-stale`.

## Crypto store layout

Matrix E2EE uses the official `matrix-js-sdk` Rust crypto path with `fake-indexeddb` as the IndexedDB shim; crypto state persists to `crypto-idb-snapshot.json` (restrictive file permissions). Encrypted runtime state lives under `~/.openclaw/matrix/accounts/<account>/<homeserver>__<user>/<token-hash>/` and includes the sync store, crypto store, recovery key, IDB snapshot, thread bindings, and startup verification state. When the token changes but the account identity stays the same, OpenClaw reuses the best existing root so prior state remains visible.

## Profile management

Update the Matrix self-profile for the selected account:

```bash
openclaw matrix profile set --name "OpenClaw Assistant"
openclaw matrix profile set --avatar-url https://cdn.example.org/avatar.png
```

You can pass both options in one call. Matrix accepts `mxc://` avatar URLs directly; when you pass `http://` or `https://`, OpenClaw uploads the file first and stores the resolved `mxc://` URL into `channels.matrix.avatarUrl` (or the per-account override).

## Private/LAN homeservers

By default, OpenClaw blocks private/internal Matrix homeservers for SSRF protection unless you explicitly opt in per account. If your homeserver runs on localhost, a LAN/Tailscale IP, or an internal hostname, enable `network.dangerouslyAllowPrivateNetwork` for that Matrix account:

```json5
{
  channels: {
    matrix: {
      homeserver: "http://matrix-synapse:8008",
      network: {
        dangerouslyAllowPrivateNetwork: true,
      },
      accessToken: "syt_internal_xxx",
    },
  },
}
```

The CLI setup equivalent is `openclaw matrix account add --account ops --homeserver http://matrix-synapse:8008 --allow-private-network --access-token syt_ops_xxx`. This opt-in only allows trusted private/internal targets: public cleartext homeservers such as `http://matrix.example.org:8008` remain blocked. Prefer `https://` whenever possible.

## Proxying Matrix traffic

If your Matrix deployment needs an explicit outbound HTTP(S) proxy, set `channels.matrix.proxy`. Named accounts can override the top-level default with `channels.matrix.accounts.<id>.proxy`, and OpenClaw uses the same proxy setting for runtime Matrix traffic and account status probes.

```json5
{
  channels: {
    matrix: {
      homeserver: "https://matrix.example.org",
      accessToken: "syt_bot_xxx",
      proxy: "http://127.0.0.1:7890",
    },
  },
}
```

**Source**: OpenClaw documentation — `channels/matrix` (mirror `inbox/openclaw_docs/channels/matrix.md`)
**Last Updated**: 2026-06-22
**Status**: Active
