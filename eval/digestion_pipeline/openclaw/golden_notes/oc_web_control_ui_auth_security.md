---
tags:
  - resource
  - documentation
  - openclaw
  - web
  - security
keywords:
  - control ui auth
  - websocket handshake auth
  - device pairing approval
  - tailscale serve identity
  - trusted-proxy auth
  - insecure http break-glass
  - content security policy img-src
  - avatar route auth
  - assistant media ticket
  - disconnected 1008 pairing required
topics:
  - OpenClaw
  - Control UI Security
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/web/control-ui
access_control_group: ["general"]
---

# OpenClaw — Securing and Connecting to the Control UI

## Overview

This note is the **procedure** for authenticating and securing the OpenClaw Control UI — the Vite + Lit browser SPA the Gateway serves and that speaks directly to the Gateway WebSocket on the same port. It covers the four WebSocket-handshake auth modes (token / password / Tailscale Serve identity / trusted-proxy), the one-time device-pairing approval (and scope-upgrade re-approval), browser-local personal/assistant identity, the auth-gated runtime-config endpoint, Tailnet access via Serve vs bind+token, the insecure-HTTP break-glass toggles, the fixed `img-src` Content Security Policy, and the authenticated avatar and assistant-media routes. It mirrors the auth/security sections of the `web/control-ui` source page; what the UI *is* and its capability map live in `oc_web_control_ui_overview`, and the chat/talk + embed-sandbox behavior lives in `oc_web_control_ui_chat_talk`.

## WebSocket-Handshake Auth

The Control UI is served at `http://<host>:18789/` by default (optional prefix via `gateway.controlUi.basePath`, e.g. `/openclaw`). If the page fails to load, start the Gateway first with `openclaw gateway`. Auth is supplied during the WebSocket handshake via one of these mechanisms:

- `connect.params.auth.token`
- `connect.params.auth.password`
- Tailscale Serve identity headers when `gateway.auth.allowTailscale: true`
- trusted-proxy identity headers when `gateway.auth.mode: "trusted-proxy"`

The dashboard settings panel keeps a token for the current browser tab session and the selected gateway URL; passwords are **not** persisted. Onboarding usually generates a gateway token for shared-secret auth on first connect, but password auth works too when `gateway.auth.mode` is `"password"`.

The Control UI fetches its runtime settings from `/control-ui-config.json`, resolved relative to the Gateway's Control UI base path (for example `/__openclaw__/control-ui-config.json` when the UI is served under `/__openclaw__/`). That endpoint is gated by the **same gateway auth** as the rest of the HTTP surface: unauthenticated browsers cannot fetch it, and a successful fetch requires either an already-valid gateway token/password, Tailscale Serve identity, or a trusted-proxy identity.

## Device Pairing (First Connection)

When you connect to the Control UI from a new browser or device, the Gateway usually requires a **one-time pairing approval** to prevent unauthorized access. The browser shows `disconnected (1008): pairing required`. Approve from a terminal in two steps:

```bash
openclaw devices list
openclaw devices approve <requestId>
```

If the browser retries pairing with changed auth details (role / scopes / public key), the previous pending request is **superseded** and a new `requestId` is created — re-run `openclaw devices list` before approval. If the browser is already paired and you change it from read access to write/admin access, this is treated as an **approval upgrade**, not a silent reconnect: OpenClaw keeps the old approval active, blocks the broader reconnect, and asks you to approve the new scope set explicitly. Once approved, the device is remembered and won't require re-approval unless you revoke it with `openclaw devices revoke --device <id> --role <role>`; see the Devices CLI page (`/cli/devices`) for token rotation and revocation.

Paperclip agents that connect through the `openclaw_gateway` adapter use the same first-run approval flow. After the initial connection attempt, run `openclaw devices approve --latest` to preview the pending request, then rerun the printed `openclaw devices approve <requestId>` command to approve it. Pass explicit `--url` and `--token` values for a remote gateway. To keep approvals stable across restarts, configure a persistent `adapterConfig.devicePrivateKeyPem` in Paperclip instead of letting it generate a new ephemeral device identity each run.

**Pairing exceptions and notes:** Direct local loopback browser connections (`127.0.0.1` / `localhost`) are **auto-approved**. Tailscale Serve can skip the pairing round trip for Control UI operator sessions when `gateway.auth.allowTailscale: true`, Tailscale identity verifies, and the browser presents its device identity. Direct Tailnet binds, LAN browser connects, and browser profiles without device identity still require explicit approval. Each browser profile generates a unique device ID, so switching browsers or clearing browser data requires re-pairing.

## Personal Identity (Browser-Local)

The Control UI supports a per-browser **personal identity** (display name and avatar) attached to outgoing messages for attribution in shared sessions. It lives in browser storage, is scoped to the current browser profile, and is not synced to other devices or persisted server-side beyond the normal transcript-authorship metadata on messages you actually send. Clearing site data or switching browsers resets it to empty.

The same browser-local pattern applies to the **assistant avatar override**. Uploaded assistant avatars overlay the gateway-resolved identity on the local browser only and never round-trip through `config.patch`. The shared `ui.assistant.avatar` config field is still available for non-UI clients writing the field directly (such as scripted gateways or custom dashboards).

## Tailnet Access (Recommended)

Two Tailnet access paths are documented. **Integrated Tailscale Serve (preferred)** keeps the Gateway on loopback and lets Tailscale Serve proxy it with HTTPS:

```bash
openclaw gateway --tailscale serve
```

Then open `https://<magicdns>/` (or your configured `gateway.controlUi.basePath`). By default, Control UI / WebSocket Serve requests can authenticate via Tailscale identity headers (`tailscale-user-login`) when `gateway.auth.allowTailscale` is `true`. OpenClaw verifies the identity by resolving the `x-forwarded-for` address with `tailscale whois` and matching it to the header, and only accepts these when the request hits loopback with Tailscale's `x-forwarded-*` headers. For Control UI operator sessions with browser device identity, this verified Serve path **also skips the device-pairing round trip**; device-less browsers and node-role connections still follow the normal device checks. Set `gateway.auth.allowTailscale: false` if you want to require explicit shared-secret credentials even for Serve traffic, then use `gateway.auth.mode: "token"` or `"password"`. For the async Serve identity path, failed auth attempts for the same client IP and auth scope are serialized before rate-limit writes, so concurrent bad retries from the same browser can show `retry later` on the second request instead of two plain mismatches racing in parallel. (Tokenless Serve auth assumes the gateway host is trusted; if untrusted local code may run on that host, require token/password auth.)

The alternative **Bind to tailnet + token** path exposes the Gateway directly on the Tailnet:

```bash
openclaw gateway --bind tailnet --token "$(openssl rand -hex 32)"
```

Then open `http://<tailscale-ip>:18789/` (or your configured `gateway.controlUi.basePath`) and paste the matching shared secret into the UI settings (sent as `connect.params.auth.token` or `connect.params.auth.password`). See the Tailscale page (`/gateway/tailscale`) for HTTPS setup guidance.

## Insecure HTTP (Break-Glass)

If you open the dashboard over plain HTTP (`http://<lan-ip>` or `http://<tailscale-ip>`), the browser runs in a **non-secure context** and blocks WebCrypto. By default, OpenClaw **blocks** Control UI connections without device identity. There are three documented exceptions:

- localhost-only insecure-HTTP compatibility with `gateway.controlUi.allowInsecureAuth=true`
- successful operator Control UI auth through `gateway.auth.mode: "trusted-proxy"`
- break-glass `gateway.controlUi.dangerouslyDisableDeviceAuth=true`

The **recommended fix** is to use HTTPS (Tailscale Serve, `https://<magicdns>/`) or open the UI locally on the gateway host (`http://127.0.0.1:18789/`). The `allowInsecureAuth` toggle is a **local compatibility toggle only**: it allows localhost Control UI sessions to proceed without device identity in non-secure HTTP contexts, does **not** bypass pairing checks, and does **not** relax remote (non-localhost) device-identity requirements. The `dangerouslyDisableDeviceAuth` toggle disables Control UI device-identity checks entirely and is a **severe security downgrade** — revert quickly after emergency use. Successful **trusted-proxy** auth can admit operator Control UI sessions without device identity, but this does not extend to node-role Control UI sessions, and same-host loopback reverse proxies still do not satisfy trusted-proxy auth (see the Trusted proxy auth page, `/gateway/trusted-proxy-auth`). The two break-glass config shapes are:

```json5
{
  gateway: {
    controlUi: { allowInsecureAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

```json5
{
  gateway: {
    controlUi: { dangerouslyDisableDeviceAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

## Content Security Policy

The Control UI ships with a tight `img-src` policy: only **same-origin** assets, `data:` URLs, and locally generated `blob:` URLs are allowed. Remote `http(s)` and protocol-relative image URLs are rejected by the browser and do not issue network fetches. In practice: avatars and images served under relative paths (for example `/avatars/<id>`) still render, including authenticated avatar routes the UI fetches and converts into local `blob:` URLs; inline `data:image/...` URLs still render (useful for in-protocol payloads); local `blob:` URLs created by the Control UI still render; and remote avatar URLs emitted by channel metadata are stripped at the Control UI's avatar helpers and replaced with the built-in logo/badge, so a compromised or malicious channel cannot force arbitrary remote image fetches from an operator browser. You do not need to change anything to get this behavior — it is **always on and not configurable**.

## Avatar Route Auth

When gateway auth is configured, the Control UI avatar endpoint requires the **same gateway token** as the rest of the API:

- `GET /avatar/<agentId>` returns the avatar image only to authenticated callers. `GET /avatar/<agentId>?meta=1` returns the avatar metadata under the same rule.
- Unauthenticated requests to either route are rejected (matching the sibling assistant-media route). This prevents the avatar route from leaking agent identity on hosts that are otherwise protected.
- The Control UI itself forwards the gateway token as a bearer header when fetching avatars, and uses authenticated blob URLs so the image still renders in dashboards.

If you disable gateway auth (not recommended on shared hosts), the avatar route also becomes unauthenticated, in line with the rest of the gateway.

## Assistant Media Route Auth

When gateway auth is configured, assistant local-media previews use a **two-step route**:

- `GET /__openclaw__/assistant-media?meta=1&source=<path>` requires the normal Control UI operator auth. The browser sends the gateway token as a bearer header when checking availability.
- Successful metadata responses include a short-lived `mediaTicket` scoped to that exact source path.
- Browser-rendered image, audio, video, and document URLs use `mediaTicket=<ticket>` instead of the active gateway token or password. The ticket expires quickly and cannot authorize a different source.

This keeps normal media rendering compatible with browser-native media elements without putting reusable gateway credentials in visible media URLs.

**Source**: OpenClaw documentation — `web/control-ui` (mirror `inbox/openclaw_docs/web/control-ui.md`)
**Last Updated**: 2026-06-22
**Status**: Active
