---
tags:
  - resource
  - documentation
  - openclaw
  - web
  - control_ui
keywords:
  - openclaw control ui
  - gateway web surfaces
  - tailscale serve funnel
  - gateway bind modes
  - admin http rpc
  - gateway auth modes
  - controlui allowedorigins
  - pnpm ui:build
topics:
  - OpenClaw
  - Gateway Web Surfaces
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/web
access_control_group: ["general"]
---

# OpenClaw — Gateway Web Surfaces and Control UI

## Overview

This note is the procedure for OpenClaw's **Gateway web surfaces**: the browser **Control UI** (Vite + Lit) served from the same port as the Gateway WebSocket (`:18789`), the webhook and Admin-HTTP-RPC endpoints exposed on that same HTTP server, the default-on Control UI config, the three Tailscale access modes (Integrated Serve, tailnet bind + token, public Funnel), the auth/security model (token / password / trusted-proxy / Tailscale identity), and building the UI assets. It mirrors the `web` source page; the in-UI capabilities themselves live behind the `/web/control-ui` link and are not duplicated here. Each step below is grounded in `inbox/openclaw_docs/web.md`; config keys, CLI commands, and ports are copied verbatim.

## Control UI bind URL

The Gateway serves a small browser Control UI from the same port as the Gateway WebSocket. The reachable URL depends on TLS and an optional path prefix:

- default: `http://<host>:18789/`
- with `gateway.tls.enabled: true`: `https://<host>:18789/`
- optional prefix: set `gateway.controlUi.basePath` (e.g. `/openclaw`)

Capabilities live in the [Control UI](https://docs.openclaw.ai/web/control-ui) page; this page focuses on bind modes, security, and web-facing surfaces.

## Webhooks

When `hooks.enabled=true`, the Gateway also exposes a small webhook endpoint on the same HTTP server. See [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) → `hooks` for the auth model and payloads.

## Admin HTTP RPC

Admin HTTP RPC exposes selected Gateway control-plane methods at `POST /api/v1/admin/rpc`. It is **off by default** and is registered only when the `admin-http-rpc` plugin is enabled. See [Admin HTTP RPC](https://docs.openclaw.ai/plugins/admin-http-rpc) for the auth model, allowed methods, and the WebSocket comparison.

## Config (default-on)

The Control UI is **enabled by default** when assets are present (`dist/control-ui`). Control it via config:

```json5
{
  gateway: {
    controlUi: { enabled: true, basePath: "/openclaw" }, // basePath optional
  },
}
```

## Tailscale access

Three bind/access modes expose the Control UI over Tailscale. Each is configured in `gateway` config and then started with the same `openclaw gateway` command:

```bash
openclaw gateway
```

### Integrated Serve (recommended)

Keep the Gateway on loopback and let Tailscale Serve proxy it:

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```

After starting `openclaw gateway`, open `https://<magicdns>/` (or your configured `gateway.controlUi.basePath`).

### Tailnet bind + token

Bind directly to the tailnet and require shared-secret token auth (this non-loopback example uses token auth):

```json5
{
  gateway: {
    bind: "tailnet",
    controlUi: { enabled: true },
    auth: { mode: "token", token: "your-token" },
  },
}
```

After starting `openclaw gateway`, open `http://<tailscale-ip>:18789/` (or your configured `gateway.controlUi.basePath`).

### Public internet (Funnel)

Expose the loopback Gateway to the public internet via Tailscale Funnel, which **requires** password auth:

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password" }, // or OPENCLAW_GATEWAY_PASSWORD
  },
}
```

`gateway.tailscale.mode: "funnel"` requires `gateway.auth.mode: "password"` (shared password).

## Security notes

The Gateway's web auth/origin/TLS model has the following rules (all from the source page):

- Gateway auth is required by default (token, password, trusted-proxy, or Tailscale Serve identity headers when enabled).
- Non-loopback binds still **require** gateway auth. In practice that means token/password auth or an identity-aware reverse proxy with `gateway.auth.mode: "trusted-proxy"`.
- The wizard creates shared-secret auth by default and usually generates a gateway token (even on loopback).
- In shared-secret mode, the UI sends `connect.params.auth.token` or `connect.params.auth.password`.
- When `gateway.tls.enabled: true`, local dashboard and status helpers render `https://` dashboard URLs and `wss://` WebSocket URLs.
- In identity-bearing modes such as Tailscale Serve or `trusted-proxy`, the WebSocket auth check is satisfied from request headers instead.
- For public non-loopback Control UI deployments, set `gateway.controlUi.allowedOrigins` explicitly (full origins). Private same-origin LAN/Tailnet loads are accepted for loopback, RFC1918/link-local, `.local`, `.ts.net`, and Tailscale CGNAT hosts.
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true` enables Host-header origin fallback mode, but is a dangerous security downgrade.
- With Serve, Tailscale identity headers can satisfy Control UI/WebSocket auth when `gateway.auth.allowTailscale` is `true` (no token/password required). HTTP API endpoints do not use those Tailscale identity headers; they follow the gateway's normal HTTP auth mode instead. Set `gateway.auth.allowTailscale: false` to require explicit credentials. This tokenless flow assumes the gateway host is trusted. See [Tailscale](https://docs.openclaw.ai/gateway/tailscale) and [Security](https://docs.openclaw.ai/gateway/security).

## Building the UI

The Gateway serves static files from `dist/control-ui`. Build them with:

```bash
pnpm ui:build
```

**Source**: OpenClaw documentation — `web` (mirror `inbox/openclaw_docs/web.md`)
**Last Updated**: 2026-06-22
**Status**: Active
