---
tags:
  - resource
  - documentation
  - openclaw
  - web
  - dashboard
keywords:
  - openclaw dashboard
  - openclaw dashboard command
  - gateway dashboard control ui
  - dashboard auth basics
  - unauthorized 1008
  - auth_token_mismatch auth_scope_mismatch
  - gateway.auth.token sessionstorage
  - ssh tunnel dashboard remote
topics:
  - OpenClaw
  - Web Dashboard
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/web/dashboard
access_control_group: ["general"]
---

# OpenClaw — Opening and Authenticating the Gateway Dashboard

## Overview

This note is the operator procedure for opening and authenticating the OpenClaw **Gateway dashboard** — the browser Control UI served at `/` by default (override with `gateway.controlUi.basePath`). It mirrors the `web/dashboard` source page: the quick-open URLs, the `openclaw dashboard` fast-path link/launch, the local-vs-remote auth basics (localhost, gateway TLS `wss://`, shared-secret token/password, SecretRef-managed non-tokenized URLs, Tailscale Serve and trusted-proxy identity modes, SSH tunnel), and the `unauthorized` / `1008` + scope-mismatch troubleshooting checklist. The dashboard IS the Control UI under an auth/launch lens; UI capabilities and the full handshake-auth/security model are documented in the sibling Control UI notes and linked here, not redefined.

## Quick open (local Gateway)

Authentication is enforced at the WebSocket handshake, but opening the dashboard locally is a direct browser navigation:

- [http://127.0.0.1:18789/](http://127.0.0.1:18789/) (or [http://localhost:18789/](http://localhost:18789/)).
- With `gateway.tls.enabled: true`, use `https://127.0.0.1:18789/` and `wss://127.0.0.1:18789` for the WebSocket endpoint.

Key references on the source page: the [Control UI](https://docs.openclaw.ai/web/control-ui) page for usage and UI capabilities; [Tailscale](https://docs.openclaw.ai/gateway/tailscale) for Serve/Funnel automation; and [Web surfaces](https://docs.openclaw.ai/web) for bind modes and security notes.

**Security note (source-stated):** the Control UI is an **admin surface** (chat, config, exec approvals). Do not expose it publicly. The UI keeps dashboard URL tokens in `sessionStorage` for the current browser tab session and selected gateway URL, and strips them from the URL after load. Prefer localhost, Tailscale Serve, or an SSH tunnel.

## Fast path (recommended)

The fast path avoids hand-building a tokenized URL:

- After onboarding, the CLI auto-opens the dashboard and prints a clean (non-tokenized) link.
- Re-open anytime with `openclaw dashboard` — it copies the link, opens the browser if possible, and shows an SSH hint if headless.
- If clipboard and browser delivery fail, `openclaw dashboard` still prints the clean URL and tells you to use the token from `OPENCLAW_GATEWAY_TOKEN` or `gateway.auth.token` as the URL fragment key `token`; it does not print token values in logs.
- If the UI prompts for shared-secret auth, paste the configured token or password into Control UI settings.

## Auth basics (local vs remote)

The dashboard authenticates at the WebSocket handshake via the configured gateway auth path. The source page enumerates these handshake auth inputs: `connect.params.auth.token`, `connect.params.auth.password`, Tailscale Serve identity headers when `gateway.auth.allowTailscale: true`, and trusted-proxy identity headers when `gateway.auth.mode: "trusted-proxy"` (see `gateway.auth` in [Gateway configuration](https://docs.openclaw.ai/gateway/configuration)). The local-vs-remote choices are:

- **Localhost**: open `http://127.0.0.1:18789/`.
- **Gateway TLS**: when `gateway.tls.enabled: true`, dashboard/status links use `https://` and Control UI WebSocket links use `wss://`.
- **Shared-secret token source**: `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`); `openclaw dashboard` can pass it via URL fragment for one-time bootstrap, and the Control UI keeps it in `sessionStorage` for the current browser tab session and selected gateway URL instead of `localStorage`.
- **SecretRef-managed token**: if `gateway.auth.token` is SecretRef-managed, `openclaw dashboard` prints/copies/opens a non-tokenized URL **by design** — this avoids exposing externally managed tokens in shell logs, clipboard history, or browser-launch arguments. If the SecretRef is configured but unresolved in your current shell, `openclaw dashboard` still prints a non-tokenized URL plus actionable auth setup guidance.
- **Shared-secret password**: use the configured `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`). The dashboard does not persist passwords across reloads.
- **Identity-bearing modes**: Tailscale Serve can satisfy Control UI/WebSocket auth via identity headers when `gateway.auth.allowTailscale: true`, and a non-loopback identity-aware reverse proxy can satisfy `gateway.auth.mode: "trusted-proxy"`. In those modes the dashboard does not need a pasted shared secret for the WebSocket.
- **Not localhost**: use Tailscale Serve, a non-loopback shared-secret bind, a non-loopback identity-aware reverse proxy with `gateway.auth.mode: "trusted-proxy"`, or an SSH tunnel. HTTP APIs still use shared-secret auth unless you intentionally run private-ingress `gateway.auth.mode: "none"` or trusted-proxy HTTP auth (see [Web surfaces](https://docs.openclaw.ai/web)).

## If you see "unauthorized" / 1008

When the dashboard reports `unauthorized` or the WebSocket closes with `1008`, work this checklist (verbatim from source):

- Ensure the gateway is reachable — local: `openclaw status`; remote: open an SSH tunnel and then the local URL:

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
# then open http://127.0.0.1:18789/
```

- For `AUTH_TOKEN_MISMATCH`, clients may do **one** trusted retry with a cached device token when the gateway returns retry hints. That cached-token retry reuses the token's cached approved scopes; explicit `deviceToken` / explicit `scopes` callers keep their requested scope set. If auth still fails after that retry, resolve token drift manually.
- For `AUTH_SCOPE_MISMATCH`, the device token was recognized but does not carry the dashboard's requested scopes; **re-pair or approve the requested scope contract** instead of rotating the shared gateway token.
- Outside that retry path, connect auth precedence is explicit shared token/password first, then explicit `deviceToken`, then stored device token, then bootstrap token.
- On the async Tailscale Serve Control UI path, failed attempts for the same `{scope, ip}` are serialized before the failed-auth limiter records them, so the second concurrent bad retry can already show `retry later`.
- For token drift repair steps, follow the [Token drift recovery checklist](https://docs.openclaw.ai/cli/devices#token-drift-recovery-checklist).
- Retrieve or supply the shared secret from the gateway host:
  - Token: `openclaw config get gateway.auth.token`
  - Password: resolve the configured `gateway.auth.password` or `OPENCLAW_GATEWAY_PASSWORD`
  - SecretRef-managed token: resolve the external secret provider or export `OPENCLAW_GATEWAY_TOKEN` in this shell, then rerun `openclaw dashboard`
  - No shared secret configured: `openclaw doctor --generate-gateway-token`
- In the dashboard settings, paste the token or password into the auth field, then connect.
- The UI language picker is in **Overview -> Gateway Access -> Language**. It is part of the access card, not the Appearance section.

**Source**: OpenClaw documentation — `web/dashboard` (mirror `inbox/openclaw_docs/web/dashboard.md`)
**Last Updated**: 2026-06-22
**Status**: Active
