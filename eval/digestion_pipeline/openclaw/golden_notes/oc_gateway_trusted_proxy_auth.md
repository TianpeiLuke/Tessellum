---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - security
keywords:
  - openclaw trusted proxy auth
  - gateway.auth.mode trusted-proxy
  - identity-aware reverse proxy
  - trustedProxies userHeader allowUsers
  - x-openclaw-scopes scope cap
  - websocket 1008 unauthorized
  - mixed_trusted_proxy_token
  - hsts tls termination proxy
  - openclaw security audit critical
topics:
  - OpenClaw
  - Gateway Trusted-Proxy Auth
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/trusted-proxy-auth
access_control_group: ["general"]
---

# OpenClaw — Trusted-Proxy Gateway Authentication

## Overview

This note is the procedure for delegating OpenClaw Gateway authentication to a **trusted identity-aware reverse proxy** by setting `gateway.auth.mode = "trusted-proxy"`, mirroring the `gateway/trusted-proxy-auth` source page. In this mode the proxy (Pomerium, Caddy + OAuth, nginx + oauth2-proxy, or Traefik + forward auth) performs all user authentication and forwards the identity as an HTTP header; the Gateway only verifies the request came from a trusted proxy IP and extracts the identity. The page is flagged security-sensitive — misconfiguration can expose the Gateway to unauthorized access — and `openclaw security audit` deliberately reports this mode as a **critical** finding. The sections below cover use/avoid criteria, trust flow, Control UI device-less scope behavior, configuration + `ParamField` reference, TLS/HSTS placement, proxy examples, mixed-token rejection, the `x-openclaw-scopes` cap, security checklist + audit, the `trusted_proxy_*` codes, and migration.

## When to use / When NOT to use

Use `trusted-proxy` mode when you run OpenClaw behind an **identity-aware proxy** (Pomerium, Caddy + OAuth, nginx + oauth2-proxy, Traefik + forward auth), the proxy handles all authentication and passes user identity via headers, you are in a Kubernetes/container environment where the proxy is the only path to the Gateway, or you hit WebSocket `1008 unauthorized` errors because browsers cannot pass tokens in WS payloads.

Do **NOT** use it if the proxy does not authenticate users (just a TLS terminator or load balancer), any path to the Gateway bypasses the proxy (firewall holes, internal network access), you are unsure the proxy correctly strips/overwrites forwarded headers, or you only need personal single-user access (the source recommends Tailscale Serve + loopback).

## How it works

The trust flow is a five-step sequence: (1) **Proxy authenticates the user** via OAuth, OIDC, SAML, etc.; (2) **Proxy adds an identity header** carrying the authenticated user identity (e.g. `x-forwarded-user: nick@example.com`); (3) **Gateway verifies trusted source** — checks the request came from a trusted proxy IP configured in `gateway.trustedProxies`; (4) **Gateway extracts identity** from the configured header; (5) **Authorize** if everything checks out. OAuth/OIDC/SAML are proxy-side protocols (prose only; no OpenClaw-specific term); the Gateway trusts only the source IP plus the header evidence.

## Control UI pairing behavior

When `gateway.auth.mode = "trusted-proxy"` is active and the request passes trusted-proxy checks, Control UI WebSocket sessions can connect **without device pairing identity**, but the scope behavior is deliberately restrictive: such device-less sessions receive **no operator scopes by default** — OpenClaw clears the requested scope list to `[]` so a session not bound to an approved paired device/token cannot self-declare permissions. If methods fail with `missing scope` after a successful connect, use HTTPS so the browser can generate device identity and complete pairing. As break-glass only, `gateway.controlUi.dangerouslyDisableDeviceAuth=true` preserves requested scopes without device identity — a severe security downgrade to revert quickly.

If your proxy sends `x-openclaw-scopes` on the Control UI WebSocket upgrade, OpenClaw caps the session scopes to the **intersection** of requested and declared scopes (the header does **not** grant scopes, only narrows them). So pairing is no longer the primary gate for Control UI access here, your reverse-proxy auth policy and `allowUsers` become the effective access control, and gateway ingress must stay locked to trusted proxy IPs (`gateway.trustedProxies` + firewall). Custom WebSocket clients are **not** Control UI sessions: `dangerouslyDisableDeviceAuth` grants no scopes to arbitrary `client.mode: "backend"` or CLI-shaped clients — such automation should use device identity/pairing, the reserved direct-local `client.id: "gateway-client"` backend helper path, or the admin HTTP RPC plugin.

## Configuration

The minimal config sets a non-loopback bind, the trusted proxy IP allowlist, the auth mode, and the identity header (a **non-loopback** trusted proxy source is expected by default):

```json5
{
  gateway: {
    bind: "lan", // non-loopback trusted proxy source expected by default

    trustedProxies: ["10.0.0.1", "172.17.0.1"], // CRITICAL: only your proxy's IP(s)

    auth: {
      mode: "trusted-proxy",
      trustedProxy: {
        userHeader: "x-forwarded-user", // authenticated user identity (required)
        requiredHeaders: ["x-forwarded-proto", "x-forwarded-host"], // optional: must be present
        allowUsers: ["nick@example.com", "admin@company.org"], // optional: empty = allow all
        allowLoopback: false, // optional: opt-in for same-host loopback proxy
      },
    },
  },
}
```

The source's runtime rules: it **rejects loopback-source requests** (`127.0.0.1`, `::1`, loopback CIDRs) by default; same-host loopback proxies do **not** satisfy it unless you set `gateway.auth.trustedProxy.allowLoopback = true` **and** include the loopback address in `gateway.trustedProxies`; `allowLoopback` trusts local host processes as much as the proxy, so enable it only when the Gateway is firewalled from direct remote access and the local proxy strips/overwrites client-supplied identity headers; internal clients bypassing the proxy should use `gateway.auth.password` / `OPENCLAW_GATEWAY_PASSWORD`, not identity headers; non-loopback Control UI deployments still need explicit `gateway.controlUi.allowedOrigins`. Finally, **forwarded-header evidence overrides loopback locality for local direct fallback** — a loopback request carrying `Forwarded`, any `X-Forwarded-*`, or `X-Real-IP` is disqualified from local-direct password fallback and device-identity gating; with `allowLoopback: true` it can still be accepted as a same-host proxy request, while `requiredHeaders` and `allowUsers` still apply.

### Configuration reference

The source's `ParamField` entries: `gateway.trustedProxies` (`string[]`, **required**) — proxy IPs to trust; others rejected. `gateway.auth.mode` (`string`, **required**) — must be `"trusted-proxy"`. `gateway.auth.trustedProxy.userHeader` (`string`, **required**) — header with the authenticated user identity. `gateway.auth.trustedProxy.requiredHeaders` (`string[]`) — headers that must be present for the request to be trusted. `gateway.auth.trustedProxy.allowUsers` (`string[]`) — allowlist of user identities; empty = allow all authenticated users. `gateway.auth.trustedProxy.allowLoopback` (`boolean`, default `false`) — opt-in for same-host loopback proxies. Enable `allowLoopback` only when the local proxy is the intended trust boundary — any local process that can connect can try to send proxy identity headers, so keep direct Gateway access private and require proxy-owned headers such as `x-forwarded-proto` or a signed assertion header where supported.

## TLS termination and HSTS

Use **one** TLS termination point and apply HSTS there. **Proxy TLS termination (recommended):** when the proxy handles HTTPS for `https://control.example.com`, set `Strict-Transport-Security` at the proxy for that domain — good for internet-facing deployments, keeps cert + HTTP-hardening policy in one place, and lets OpenClaw stay on loopback HTTP behind the proxy (example value `Strict-Transport-Security: max-age=31536000; includeSubDomains`). **Gateway TLS termination:** if OpenClaw serves HTTPS directly, set `gateway.tls.enabled = true` and `gateway.http.securityHeaders.strictTransportSecurity = "max-age=31536000; includeSubDomains"`; `strictTransportSecurity` accepts a string value, or `false` to disable explicitly.

### Rollout guidance

HSTS rollout guidance: start with a short max age (e.g. `max-age=300`) while validating; raise to long-lived values (e.g. `max-age=31536000`) only after confidence is high; add `includeSubDomains` only if every subdomain is HTTPS-ready; use preload only if you intentionally meet preload requirements for your full domain set; loopback-only local dev does not benefit from HSTS. (HSTS maps to existing `term_tls`; no new term.)

## Proxy setup examples

All four examples share the same OpenClaw side (`bind: "lan"`, single-IP `trustedProxies`, `auth.mode: "trusted-proxy"`, a `trustedProxy.userHeader`), differing only in the injected identity header (compressed per the sub-plan to distinct lines):

- **Pomerium** — `userHeader: "x-pomerium-claim-email"`, `requiredHeaders: ["x-pomerium-jwt-assertion"]`; JWT in `x-pomerium-jwt-assertion`; route sets `pass_identity_headers: true`, forwards `https://openclaw.example.com` → `http://openclaw-gateway:18789`.
- **Caddy with OAuth** — `userHeader: "x-forwarded-user"`; the `caddy-security` plugin authenticates and the Caddyfile sets `header_up X-Forwarded-User {http.auth.user.email}` on `reverse_proxy openclaw:18789`.
- **nginx + oauth2-proxy** — `userHeader: "x-auth-request-email"`; nginx uses `auth_request /oauth2/auth`, `auth_request_set $user $upstream_http_x_auth_request_email`, forwards `X-Auth-Request-Email` (with `Upgrade`/`Connection: upgrade` for WS).
- **Traefik with forward auth** — `userHeader: "x-forwarded-user"`, `trustedProxies: ["172.17.0.1"]` (the Traefik container IP).

## Mixed token configuration

OpenClaw **rejects** configs where both a `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`) and `trusted-proxy` mode are active, since mixed token configs can cause loopback requests to silently authenticate on the wrong auth path. On a `mixed_trusted_proxy_token` startup error, either remove the shared token (trusted-proxy mode) or switch `gateway.auth.mode` to `"token"`. Loopback trusted-proxy identity headers still **fail closed** — same-host callers are not silently authenticated as proxy users; internal callers bypassing the proxy may use `gateway.auth.password` / `OPENCLAW_GATEWAY_PASSWORD` instead, since token fallback is intentionally unsupported in this mode.

## Operator scopes header

Trusted-proxy auth is an **identity-bearing** HTTP mode, so callers may optionally declare operator scopes with `x-openclaw-scopes` on HTTP API requests (e.g. `operator.read`, `operator.read,operator.write`, `operator.admin,operator.write`); WebSocket scopes are instead set by the protocol handshake and device identity binding, where the header on a Control UI upgrade is only a **cap**, not a grant.

Behavior per source: present → OpenClaw honors the declared set; present but empty → **no** operator scopes; absent → identity-bearing HTTP APIs fall back to the standard operator default scope set; gateway-auth **plugin HTTP routes** are narrower — when absent their runtime scope falls back to `operator.write`; browser-origin HTTP requests must still pass `gateway.controlUi.allowedOrigins` (or deliberate Host-header fallback) even after auth succeeds.

## Security checklist

The source's pre-enable checklist: **Proxy is the only path** — Gateway port firewalled from everything except the proxy; **trustedProxies is minimal** — only actual proxy IPs, not entire subnets; **Loopback proxy source is deliberate** — fails closed for loopback-source requests unless `allowLoopback` is explicitly enabled; **Proxy strips headers** — overwrites (not appends) `x-forwarded-*` from clients; **TLS termination** — proxy handles TLS, users connect via HTTPS; **allowedOrigins is explicit** — non-loopback Control UI uses explicit `gateway.controlUi.allowedOrigins`; **allowUsers is set** (recommended) — restrict to known users; **No mixed token config** — never both `gateway.auth.token` and `mode: "trusted-proxy"`; **Local password fallback is private** — if `gateway.auth.password` is set for internal callers, keep the port firewalled so non-proxy remote clients cannot reach it directly.

## Security audit

`openclaw security audit` flags trusted-proxy auth with a **critical** severity finding intentionally — a reminder that you are delegating security to your proxy. The audit checks for: the base `gateway.trusted_proxy_auth` reminder; missing `trustedProxies`; missing `userHeader`; empty `allowUsers` (allows any authenticated user); enabled `allowLoopback` for same-host proxy sources; and wildcard or missing browser-origin policy on exposed Control UI surfaces.

## Troubleshooting (trusted_proxy_* codes)

The source's error codes and fixes: `trusted_proxy_untrusted_source` — request did not come from an IP in `gateway.trustedProxies`; verify the proxy IP (Docker IPs can change), check for a load balancer in front, use `docker inspect` / `kubectl get pods -o wide` to find actual IPs. `trusted_proxy_loopback_source` — a loopback-source request was rejected; fix by preferring token/password auth for internal same-host clients, routing through a non-loopback trusted proxy address, or (deliberate same-host proxy) setting `allowLoopback = true`, keeping the loopback address in `gateway.trustedProxies`, and ensuring the proxy strips/overwrites identity headers. `trusted_proxy_user_missing` — user header empty/missing; check the proxy passes identity headers, the header name is correct (case-insensitive, spelling matters), and the user is authenticated. `trusted_proxy_missing_header_*` — a required header absent; check proxy config and whether headers are stripped in the chain. `trusted_proxy_user_not_allowed` — authenticated but not in `allowUsers`; add them or remove the allowlist. `trusted_proxy_origin_not_allowed` — auth succeeded but the browser `Origin` failed Control UI checks; ensure `gateway.controlUi.allowedOrigins` includes the exact origin, avoid unintended wildcards, and if using Host-header fallback set `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true` deliberately.

Two non-coded symptoms: **Connection succeeds but methods report `missing scope`** — WS connects but `chat.history`, `sessions.list`, or `models.list` fails with `missing scope: operator.read`; causes are a device-less Control UI session, a custom backend client, or an overly narrow `x-openclaw-scopes` cap; fixes are the same as Control UI pairing behavior above (HTTPS for device identity; device identity/pairing, `gateway-client`, or admin HTTP RPC for automation). **WebSocket still failing** — ensure the proxy supports WS upgrades (`Upgrade: websocket`, `Connection: upgrade`), passes identity headers on WS upgrades (not just HTTP), and has no separate WebSocket auth path.

## Migration from token auth

The source's six-step migration from token auth: (1) configure the proxy to authenticate users and pass headers; (2) test the proxy independently (curl with headers); (3) update OpenClaw config to trusted-proxy auth; (4) restart the Gateway; (5) test Control UI WebSocket connections; (6) run `openclaw security audit`.

**Source**: OpenClaw documentation — `gateway/trusted-proxy-auth` (mirror `inbox/openclaw_docs/gateway/trusted-proxy-auth.md`)
**Last Updated**: 2026-06-22
**Status**: Active
