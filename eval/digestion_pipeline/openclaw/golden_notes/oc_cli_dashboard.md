---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - dashboard
keywords:
  - openclaw dashboard command
  - control ui launch
  - gateway.auth.token secretref
  - gateway.tls.enabled https wss
  - non-tokenized url secretref
  - openclaw_gateway_token manual auth hint
  - dashboard --no-open
topics:
  - OpenClaw
  - CLI Dashboard
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/dashboard
access_control_group: ["general"]
---

# OpenClaw — `openclaw dashboard` (Open the Control UI)

## Overview

This note is the procedure reference for the `openclaw dashboard` CLI command, which opens the OpenClaw **Control UI** using your current auth. It mirrors the `cli/dashboard` source page: the two invocations (open in browser, or `--no-open` to print the URL), TLS-following URL emission (`https://` / `wss://`), `gateway.auth.token` SecretRef resolution, the safe manual-auth hint when clipboard/browser delivery fails, and the non-tokenized-URL safety behavior for SecretRef-managed tokens (resolved or unresolved). Operator scope, Control-UI internals, and gateway auth configuration are owned by other docs and are linked, not redefined here.

## Command and Usage

`openclaw dashboard` opens the Control UI using your current auth. The page documents two invocations:

```bash
openclaw dashboard
openclaw dashboard --no-open
```

`openclaw dashboard` (no flag) opens the Control UI; `openclaw dashboard --no-open` prints the URL without launching a browser. (The exact resolved auth source — configured token, SecretRef, or auth profile — is whatever the current auth provides; the source page documents the behavior, not a per-flag matrix beyond `--no-open`.)

## Notes (Auth, TLS, and SecretRef Behavior)

The source page enumerates the following behaviors verbatim:

- `dashboard` resolves configured `gateway.auth.token` SecretRefs when possible.
- `dashboard` follows `gateway.tls.enabled`: TLS-enabled gateways print/open `https://` Control UI URLs and connect over `wss://`.
- If clipboard/browser delivery fails for a token-authenticated dashboard URL, `dashboard` logs a safe manual-auth hint naming `OPENCLAW_GATEWAY_TOKEN`, `gateway.auth.token`, and fragment key `token` **without** printing the token value.
- For SecretRef-managed tokens (resolved or unresolved), `dashboard` prints/copies/opens a **non-tokenized URL** to avoid exposing external secrets in terminal output, clipboard history, or browser-launch arguments.
- If `gateway.auth.token` is SecretRef-managed but **unresolved** in this command path, the command prints a non-tokenized URL **and explicit remediation guidance** instead of embedding an invalid token placeholder.

The throughline is secret-safety: a SecretRef-managed token is never embedded into the emitted URL (in either the resolved or unresolved case), and a token-authenticated URL whose delivery fails surfaces a hint that names the relevant env var (`OPENCLAW_GATEWAY_TOKEN`), config key (`gateway.auth.token`), and URL fragment key (`token`) rather than leaking the token itself.

**Source**: OpenClaw documentation — `cli/dashboard` (mirror `inbox/openclaw_docs/cli/dashboard.md`)
**Last Updated**: 2026-06-22
**Status**: Active
