---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - devices
keywords:
  - openclaw devices command
  - device pairing approval
  - device token rotate revoke
  - operator.admin operator.pairing scope
  - paperclip first-run pairing
  - autoApproveCidrs node pairing
  - AUTH_TOKEN_MISMATCH token drift recovery
  - device scope containment self-only
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/devices
access_control_group: ["general"]
---

# OpenClaw — `openclaw devices` (Device Pairing and Token Management)

## Overview

This note documents the `openclaw devices` CLI command, which manages device pairing requests and device-scoped tokens. It mirrors the `cli/devices` source page: the seven subcommands (`list`, `remove`, `clear`, `approve`, `reject`, `rotate`, `revoke`), the Paperclip / `openclaw_gateway` first-run approval flow, the common connection options, the scope-containment and self-only management notes, and the `AUTH_*_MISMATCH` token-drift recovery checklist. It is a procedure note: the operational steps an operator runs to approve devices and rotate or revoke their tokens, plus the authority and scope rules those steps enforce.

## Commands

The seven subcommands share a common shape — the representative invocations are consolidated into one block; the prose below each heading carries the per-subcommand authority and scope rules verbatim from source.

```
openclaw devices list                                              # also: --json
openclaw devices remove <deviceId>                                 # also: --json
openclaw devices clear --yes [--pending] [--json]
openclaw devices approve [<requestId>] [--latest]
openclaw devices reject <requestId>
openclaw devices rotate --device <deviceId> --role operator --scope operator.read --scope operator.write
openclaw devices revoke --device <deviceId> --role node
```

### `openclaw devices list`

List pending pairing requests and paired devices. Pending request output shows the requested access next to the device's current approved access when the device is already paired, which makes scope/role upgrades explicit instead of looking like the pairing was lost.

### `openclaw devices remove <deviceId>`

Remove one paired device entry. When you are authenticated with a paired device token, non-admin callers can remove only **their own** device entry; removing some other device requires `operator.admin`.

### `openclaw devices clear --yes [--pending]`

Clear paired devices in bulk. This command is intentionally gated by `--yes`. Add `--pending` to clear pending pairing requests, and `--json` for machine-readable output.

### `openclaw devices approve [requestId] [--latest]`

Approve a pending device pairing request by exact `requestId`. If `requestId` is omitted or `--latest` is passed, OpenClaw only prints the selected pending request and exits; rerun approval with the exact request ID after verifying the details. `devices approve` requires an explicit request ID before minting tokens — omitting `requestId` or passing `--latest` only previews the newest pending request.

If a device retries pairing with changed auth details (role, scopes, or public key), OpenClaw supersedes the previous pending entry and issues a new `requestId`; run `openclaw devices list` right before approval to use the current ID. If the device is already paired and asks for broader scopes or a broader role, OpenClaw keeps the existing approval in place and creates a new pending upgrade request — review the `Requested` vs `Approved` columns in `openclaw devices list` or use `openclaw devices approve --latest` to preview the exact upgrade before approving it.

If the Gateway is explicitly configured with `gateway.nodes.pairing.autoApproveCidrs`, first-time `role: node` requests from matching client IPs can be approved before they appear in this list. That policy is disabled by default and never applies to operator/browser clients or upgrade requests.

Approving node or other non-operator device roles requires `operator.admin`. `operator.pairing` is enough for operator-device approvals only when the requested operator scopes stay within the caller's own scopes (see Operator scopes for the approval-time checks).

### `openclaw devices reject <requestId>`

Reject a pending device pairing request.

### `openclaw devices rotate --device <id> --role <role> [--scope <scope...>]`

Rotate a device token for a specific role (optionally updating scopes), e.g. `openclaw devices rotate --device <deviceId> --role operator --scope operator.read --scope operator.write`. The target role must already exist in that device's approved pairing contract — rotation cannot mint a new unapproved role. If you omit `--scope`, later reconnects with the stored rotated token reuse that token's cached approved scopes; if you pass explicit `--scope` values, those become the stored scope set for future cached-token reconnects. Non-admin paired-device callers can rotate only their **own** device token, and the target token scope set must stay within the caller session's own operator scopes — rotation cannot mint or preserve a broader operator token than the caller already has. Rotation returns rotation metadata as JSON; if the caller is rotating its own token while authenticated with that device token, the response also includes the replacement token so the client can persist it before reconnecting, whereas shared/admin rotations do not echo the bearer token.

### `openclaw devices revoke --device <id> --role <role>`

Revoke a device token for a specific role, e.g. `openclaw devices revoke --device <deviceId> --role node`. Non-admin paired-device callers can revoke only their **own** device token; revoking some other device's token requires `operator.admin`. The target token scope set must also fit within the caller session's own operator scopes — pairing-only callers cannot revoke admin/write operator tokens. Revoke returns the revoke result as JSON.

## Paperclip / `openclaw_gateway` First-Run Approval

When a new Paperclip agent connects through the `openclaw_gateway` adapter for the first time, the Gateway may require a one-time device pairing approval before runs can succeed. If Paperclip reports `openclaw_gateway_pairing_required`, approve the pending device and retry. For local gateways, preview the latest pending request with `openclaw devices approve --latest`; the preview prints the exact `openclaw devices approve <requestId>` command, which you verify and then rerun with the request ID to approve. For remote gateways or explicit credentials, pass the same options while previewing and approving:

```bash
openclaw devices approve --latest --url <gateway-ws-url> --token <gateway-token>
```

To avoid re-approving after restarts, keep a persistent device key in the Paperclip adapter config instead of generating a new ephemeral identity each run:

```json
{
  "adapterConfig": {
    "devicePrivateKeyPem": "<ed25519-private-key-pkcs8-pem>"
  }
}
```

If approval keeps failing, run `openclaw devices list` first to confirm a pending request exists.

## Common Options

- `--url <url>`: Gateway WebSocket URL (defaults to `gateway.remote.url` when configured).
- `--token <token>`: Gateway token (if required).
- `--password <password>`: Gateway password (password auth).
- `--timeout <ms>`: RPC timeout.
- `--json`: JSON output (recommended for scripting).

When you set `--url`, the CLI does not fall back to config or environment credentials — pass `--token` or `--password` explicitly; missing explicit credentials is an error.

## Notes (Scope Containment, Self-Only, `--yes` Gate)

- Token rotation returns a new token (sensitive); treat it like a secret.
- These commands require `operator.pairing` (or `operator.admin`) scope. Some approvals also require the caller to hold the operator scopes that the target device would mint or inherit. Non-operator device roles require `operator.admin` (see Operator scopes).
- `gateway.nodes.pairing.autoApproveCidrs` is an opt-in Gateway policy for fresh node device pairing only; it does not change CLI approval authority.
- Token rotation and revocation stay inside the approved pairing role set and approved scope baseline for that device. A stray cached token entry does not grant a token-management target.
- For paired-device token sessions, cross-device management is admin-only: `remove`, `rotate`, and `revoke` are self-only unless the caller has `operator.admin`.
- Token mutation is also caller-scope contained: a pairing-only session cannot rotate or revoke a token that currently carries `operator.admin` or `operator.write`.
- `devices clear` is intentionally gated by `--yes`.
- If pairing scope is unavailable on local loopback (and no explicit `--url` is passed), list/approve can use a local pairing fallback.
- `devices approve` requires an explicit request ID before minting tokens; omitting `requestId` or passing `--latest` only previews the newest pending request.

## Token Drift Recovery Checklist

Use this when Control UI or other clients keep failing with `AUTH_TOKEN_MISMATCH`, `AUTH_DEVICE_TOKEN_MISMATCH`, or `AUTH_SCOPE_MISMATCH`.

1. Confirm current gateway token source: `openclaw config get gateway.auth.token`.
2. List paired devices and identify the affected device id: `openclaw devices list`.
3. Rotate operator token for the affected device: `openclaw devices rotate --device <deviceId> --role operator`.
4. If rotation is not enough, remove stale pairing and approve again — `openclaw devices remove <deviceId>`, then `openclaw devices list`, then `openclaw devices approve <requestId>`.
5. Retry client connection with the current shared token/password.

```bash
openclaw config get gateway.auth.token
openclaw devices rotate --device <deviceId> --role operator
openclaw devices remove <deviceId>
openclaw devices approve <requestId>
```

Recovery notes: normal reconnect auth precedence is explicit shared token/password first, then explicit `deviceToken`, then stored device token, then bootstrap token. Trusted `AUTH_TOKEN_MISMATCH` recovery can temporarily send both the shared token and the stored device token together for the one bounded retry. `AUTH_SCOPE_MISMATCH` means the device token was recognized but does not carry the requested scope set — fix the pairing/scope approval contract before changing shared gateway auth.

**Source**: OpenClaw documentation — `cli/devices` (mirror `inbox/openclaw_docs/cli/devices.md`)
**Last Updated**: 2026-06-22
**Status**: Active
