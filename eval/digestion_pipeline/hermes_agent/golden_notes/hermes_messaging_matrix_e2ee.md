---
tags:
  - resource
  - documentation
  - hermes_agent
  - matrix
  - encryption
keywords:
  - matrix end-to-end encryption
  - mautrix encryption libolm
  - MATRIX_E2EE_MODE off optional required
  - cross-signing MATRIX_RECOVERY_KEY
  - crypto store crypto.db recovery
  - new access token migration
topics:
  - Hermes Agent
  - Matrix
  - End-to-End Encryption
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/matrix
access_control_group: ["general"]
---

# Hermes Matrix — End-to-End Encryption

## Overview

This note is the **end-to-end encryption (E2EE) subsystem** of the Hermes Matrix bot — the part of Matrix setup that lets Hermes chat inside encrypted Matrix rooms. It is split out of the base Matrix setup procedure ([hermes_messaging_matrix](hermes_messaging_matrix.md)) because E2EE is a self-contained subsystem with its own dependency stack (the `mautrix` library's encryption extras plus the `libolm` C library), its own three-way mode switch (`off` / `optional` / `required`), its own key-storage and device-key model, and its own failure-and-recovery procedures (cross-signing verification, the stale-one-time-key crypto-store recovery, and the new-access-token migration to the SQLite crypto store). When E2EE is enabled, Hermes uploads device keys on first connection, decrypts incoming messages and encrypts outgoing messages automatically, and auto-joins encrypted rooms when invited. The macOS deployment story for E2EE — where `libolm` cannot compile on Apple Silicon — is documented separately in [hermes_messaging_matrix_proxy_mode](hermes_messaging_matrix_proxy_mode.md).

## Requirements

E2EE requires the `mautrix` library with encryption extras and the `libolm` C library:

```bash
# Install mautrix with E2EE support
pip install 'mautrix[encryption]'

# Or install with hermes extras
pip install 'hermes-agent[matrix]'
```

You also need `libolm` installed on your system (Debian/Ubuntu `sudo apt install libolm-dev`, macOS `brew install libolm`, Fedora `sudo dnf install libolm-devel`).

## Enable E2EE

Add to your `~/.hermes/.env`:

```bash
MATRIX_E2EE_MODE=required
```

`MATRIX_E2EE_MODE` accepts three modes:

| Mode | Behavior |
|------|----------|
| `off` | Do not initialize Matrix E2EE. |
| `optional` | Try E2EE when dependencies are available, but keep unencrypted rooms working if crypto cannot initialize. |
| `required` | Fail closed if E2EE dependencies or crypto setup are not available. |

Optional mode may fall back to non-E2EE operation when crypto setup is unavailable; required mode fails closed instead of silently downgrading. For backwards compatibility, `MATRIX_ENCRYPTION=true` still enables required E2EE behavior. If `mautrix[encryption]` is not installed or `libolm` is missing, the bot falls back to a plain (unencrypted) client automatically and logs a warning.

When E2EE is enabled, Hermes:

- Stores encryption keys in `~/.hermes/platforms/matrix/store/` (legacy installs: `~/.hermes/matrix/store/`)
- Uploads device keys on first connection
- Decrypts incoming messages and encrypts outgoing messages automatically
- Auto-joins encrypted rooms when invited

## Synapse Integration Tests

Hermes includes an opt-in Synapse harness for local validation:

```bash
docker compose -f tests/e2e/matrix_synapse_gateway/docker-compose.yml up -d
HERMES_MATRIX_SYNAPSE_INTEGRATION=1 \
  scripts/run_tests.sh -m "integration and matrix_synapse" \
  tests/e2e/matrix_synapse_gateway/test_gateway.py
docker compose -f tests/e2e/matrix_synapse_gateway/docker-compose.yml down -v
```

The harness creates temporary users through Synapse shared-secret registration and covers private-room send/receive, named-room invite/join, media upload/download, bot response delivery, and startup old-event filtering. E2EE smoke coverage is separately marked with `matrix_e2ee` so it can stay opt-in on developer machines.

## Cross-Signing Verification (Recommended)

If your Matrix account has cross-signing enabled (the default in Element), set the recovery key so the bot can self-sign its device on startup. Without this, other Matrix clients may refuse to share encryption sessions with the bot after a device key rotation.

```bash
MATRIX_RECOVERY_KEY=EsT... your recovery key here
```

**Where to find it:** In Element, go to **Settings** → **Security & Privacy** → **Encryption** → your recovery key (also called the "Security Key"). This is the key you were asked to save when you first set up cross-signing.

On each startup, if `MATRIX_RECOVERY_KEY` is set, Hermes imports cross-signing keys from the homeserver's secure secret storage and signs the current device. This is **idempotent** and safe to leave enabled permanently. If Hermes bootstraps a new Matrix recovery key it never logs the raw key; set `MATRIX_RECOVERY_KEY_OUTPUT_FILE=/secure/path/matrix-recovery-key.txt` before startup to write a generated key once with file mode `0600` (the file is not overwritten if it already exists).

## Deleting the Crypto Store (Recovery)

If you delete `~/.hermes/platforms/matrix/store/crypto.db`, the bot loses its encryption identity. Simply restarting with the same device ID will **not** fully recover — the homeserver still holds one-time keys signed with the old identity key, and peers cannot establish new Olm sessions.

Hermes detects this condition on startup and refuses to enable E2EE, logging: `device XXXX has stale one-time keys on the server signed with a previous identity key`.

**Easiest recovery: generate a new access token** (which gets a fresh device ID with no stale key history) — see the migration procedure below. This is the most reliable path and avoids touching the homeserver database.

**Manual recovery** (advanced — keeps the same device ID): stop Synapse and delete the old device from its database (`e2e_device_keys_json`, `e2e_one_time_keys_json`, `e2e_fallback_keys_json`, and `devices` rows for that `device_id`/`user_id`), or use the Synapse admin API `DELETE /_synapse/admin/v2/users/<urlencoded-user>/devices/DEVICE_ID` (which may also invalidate the associated access token). Then delete the local crypto store and restart:

```bash
rm -f ~/.hermes/platforms/matrix/store/crypto.db*
# restart hermes
```

Other Matrix clients (Element, matrix-commander) may cache the old device keys; after recovery, type `/discardsession` in Element to force a new encryption session with the bot.

## Upgrading from a Previous Version with E2EE

If you previously used Hermes with `MATRIX_ENCRYPTION=true` and are upgrading to a version that uses the new SQLite-based crypto store, the bot's encryption identity has changed. Your Matrix client (Element) may cache the old device keys and refuse to share encryption sessions with the bot.

**Symptoms:** The bot connects and shows "E2EE enabled" in the logs, but all messages show "could not decrypt event" and the bot never responds. The old encryption state (from the previous `matrix-nio` or serialization-based `mautrix` backend) is incompatible with the new SQLite crypto store. Clients treat changed identity keys for the same device as suspicious — a Matrix security feature.

**Fix** (one-time migration):

1. **Generate a new access token** to get a fresh device ID, then update `MATRIX_ACCESS_TOKEN` in `~/.hermes/.env`:

```bash
curl -X POST https://your-server/_matrix/client/v3/login \
  -H "Content-Type: application/json" \
  -d '{
    "type": "m.login.password",
    "identifier": {"type": "m.id.user", "user": "@hermes:your-server.org"},
    "password": "***",
    "initial_device_display_name": "Hermes Agent"
  }'
```

2. **Delete old encryption state:** `rm -f ~/.hermes/platforms/matrix/store/crypto.db` and `rm -f ~/.hermes/platforms/matrix/store/crypto_store.*`.
3. **Set your recovery key** (if you use cross-signing) — add `MATRIX_RECOVERY_KEY=EsT...` so the bot self-signs on startup and Element trusts the new device immediately.
4. **Force the client to rotate the session:** in Element, open the DM room with the bot and type `/discardsession`.
5. **Restart the gateway** with `hermes gateway run`. If `MATRIX_RECOVERY_KEY` is set you should see `Matrix: cross-signing verified via recovery key` in the logs.
6. **Send a new message.** The bot should decrypt and respond normally.

Messages sent before the upgrade cannot be decrypted (the old keys are gone) — this only affects the transition. New installations are not affected. **Why a new access token?** Each Matrix access token is bound to a specific device ID; reusing the same device ID with new encryption keys causes other clients to distrust the device, so a new token gets a new device ID with no stale key history.

## Troubleshooting: "could not decrypt event"

**Cause:** Missing encryption keys, `libolm` not installed, or the bot's device isn't trusted. **Fix:** verify `libolm` is installed, set `MATRIX_ENCRYPTION=true` in `.env`, verify/trust the bot's device in Element (its profile → Sessions), and remember the bot can only decrypt messages sent *after* it joined an encrypted room — older messages are inaccessible.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/matrix.md` · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/matrix
**Last Updated**: 2026-06-19
**Status**: Active
