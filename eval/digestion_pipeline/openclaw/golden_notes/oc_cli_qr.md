---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - pairing
keywords:
  - openclaw qr
  - mobile pairing qr
  - setup code bootstraptoken
  - operator handoff token scopes
  - gateway remote url tailscale
  - wss ws fail closed pairing
  - secretref auth resolution
  - devices approve requestid
topics:
  - OpenClaw
  - CLI
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/qr
access_control_group: ["general"]
---

# OpenClaw — `openclaw qr` (Mobile Pairing QR + Setup Code)

## Overview

This note is the procedure reference for the `openclaw qr` CLI command, which generates a mobile pairing QR and setup code from the current Gateway configuration so a mobile node app can pair with the gateway. It mirrors the whole `cli/qr` source page — the usage forms, the full option list (`--remote` / `--url` / `--public-url` / `--token` / `--password` / `--setup-code-only` / `--no-ascii` / `--json`), and the Notes covering the opaque short-lived `bootstrapToken`, the bounded operator-handoff token scopes, the Tailscale / public-`ws://` fail-closed pairing rule, SecretRef resolution for local and remote gateway auth, and the post-scan `devices approve` step.

## Usage

`openclaw qr` builds the pairing payload from the active gateway configuration. The documented invocation forms are:

```bash
openclaw qr
openclaw qr --setup-code-only
openclaw qr --json
openclaw qr --remote
openclaw qr --url wss://gateway.example/ws
```

The plain `openclaw qr` form renders the ASCII QR plus the setup code; the flags below narrow the URL source, the auth material, or the output format.

## Options

- `--remote` — prefer `gateway.remote.url`; if it is unset, `gateway.tailscale.mode=serve|funnel` can still provide the remote public URL.
- `--url <url>` — override the gateway URL used in the payload.
- `--public-url <url>` — override the public URL used in the payload.
- `--token <token>` — override which gateway token the bootstrap flow authenticates against.
- `--password <password>` — override which gateway password the bootstrap flow authenticates against.
- `--setup-code-only` — print only the setup code (no QR).
- `--no-ascii` — skip ASCII QR rendering.
- `--json` — emit JSON with the fields `setupCode`, `gatewayUrl`, `auth`, and `urlSource`.

## Notes

- `--token` and `--password` are mutually exclusive.
- The setup code itself now carries an opaque short-lived `bootstrapToken`, not the shared gateway token/password.
- Built-in setup-code bootstrap returns a primary `node` token with `scopes: []` plus a bounded `operator` handoff token for trusted mobile onboarding.
- The handed-off operator token is limited to `operator.approvals`, `operator.read`, `operator.talk.secrets`, and `operator.write`; `operator.admin` and `operator.pairing` require a separate approved operator pairing or token flow.
- Mobile pairing fails closed for Tailscale / public `ws://` gateway URLs. Private LAN addresses and `.local` Bonjour hosts remain supported over `ws://`, but Tailscale / public mobile routes should use Tailscale Serve/Funnel or a `wss://` gateway URL.
- With `--remote`, OpenClaw requires either `gateway.remote.url` or `gateway.tailscale.mode=serve|funnel`.
- With `--remote`, if effectively active remote credentials are configured as SecretRefs and you do not pass `--token` or `--password`, the command resolves them from the active gateway snapshot; if the gateway is unavailable, the command fails fast.

### Local SecretRef auth resolution (without `--remote`)

Without `--remote`, local gateway auth SecretRefs are resolved when no CLI auth override is passed:

- `gateway.auth.token` resolves when token auth can win (explicit `gateway.auth.mode="token"`, or an inferred mode where no password source wins).
- `gateway.auth.password` resolves when password auth can win (explicit `gateway.auth.mode="password"`, or an inferred mode with no winning token from auth/env).

If both `gateway.auth.token` and `gateway.auth.password` are configured (including SecretRefs) and `gateway.auth.mode` is unset, setup-code resolution fails until the mode is set explicitly. Gateway version skew note: this command path requires a gateway that supports `secrets.resolve`; older gateways return an unknown-method error.

### After scanning

After scanning the QR, approve the device pairing with:

- `openclaw devices list`
- `openclaw devices approve <requestId>`

**Source**: OpenClaw documentation — `cli/qr` (mirror `inbox/openclaw_docs/cli/qr.md`)
**Last Updated**: 2026-06-22
**Status**: Active
