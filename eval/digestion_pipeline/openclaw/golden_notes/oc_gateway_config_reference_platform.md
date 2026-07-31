---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - reference
keywords:
  - openclaw config reference platform
  - browser config block ssrf profiles
  - gateway server bind auth config
  - gateway.tls gateway.reload config
  - control ui config assistant identity
  - gateway tailscale push relay
  - gateway nodes pairing tools deny
  - gateway rate limit handshake timeout
topics:
  - OpenClaw
  - Gateway Configuration Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/configuration-reference
access_control_group: ["general"]
---

# OpenClaw — Gateway Configuration Reference: Browser, UI & Gateway Server

## Overview

This note is the field-level reference for the **browser / Control-UI / gateway-server surfaces** of the OpenClaw Gateway config (`~/.openclaw/openclaw.json`, JSON5 format), drawn from the `gateway/configuration-reference` source page. It documents the `browser` automation block, the `ui`/Control-UI identity block, and the `gateway` server block (mode/port/bind/auth/Tailscale/Control-UI/remote/push/nodes/tools), including the `gateway.tls` and `gateway.reload` sub-blocks. The remaining platform surfaces — `hooks` (incl. Gmail integration), the `canvas` plugin host, the `discovery` block (mDNS/Bonjour + wide-area DNS-SD), and the `env` environment surface — are split into the sibling [oc_gateway_config_reference_surfaces](oc_gateway_config_reference_surfaces.md). Agent-runtime surfaces (`channels`/`agents`/`models`/`mcp`/`skills`/`plugins`/`commitments`) and ops/security surfaces (`secrets`/`auth`/`logging`/`diagnostics`/`cron`) are in the other sibling reference notes. Config truth: `openclaw config schema` prints the live JSON Schema used for validation, and `config.schema.lookup` returns one path-scoped schema node. All fields are optional — OpenClaw uses safe defaults when omitted.

## Browser

The `browser` block configures programmatic Chromium control: profiles, SSRF policy, tab cleanup, and per-profile CDP endpoints.

```json5
{
  browser: {
    enabled: true,
    evaluateEnabled: true,
    defaultProfile: "user",
    ssrfPolicy: {
      // dangerouslyAllowPrivateNetwork: true, // opt in only for trusted private-network access
      // hostnameAllowlist: ["*.example.com", "example.com"],
    },
    tabCleanup: { enabled: true, idleMinutes: 120, maxTabsPerSession: 8, sweepMinutes: 5 },
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      user: { driver: "existing-session", attachOnly: true, color: "#00AA00" },
      remote: { cdpUrl: "http://10.0.0.42:9222", color: "#00AA00" },
    },
    color: "#FF4500",
  },
}
```

- `evaluateEnabled: false` disables `act:evaluate` and `wait --fn`.
- `tabCleanup` reclaims tracked primary-agent tabs after idle time or when a session exceeds its cap. Set `idleMinutes: 0` or `maxTabsPerSession: 0` to disable those individual cleanup modes.
- `ssrfPolicy.dangerouslyAllowPrivateNetwork` is disabled when unset, so browser navigation stays strict by default; set it to `true` only when you intentionally trust private-network browser navigation. `ssrfPolicy.allowPrivateNetwork` remains supported as a legacy alias. In strict mode, remote CDP profile endpoints (`profiles.*.cdpUrl`) are subject to the same private-network blocking, and you use `ssrfPolicy.hostnameAllowlist` and `ssrfPolicy.allowedHostnames` for explicit exceptions.
- Remote profiles are attach-only (start/stop/reset disabled). `profiles.*.cdpUrl` accepts `http://`, `https://`, `ws://`, and `wss://` — use HTTP(S) when you want OpenClaw to discover `/json/version`; use WS(S) for a direct DevTools WebSocket URL. `remoteCdpTimeoutMs` and `remoteCdpHandshakeTimeoutMs` apply to remote and `attachOnly` CDP reachability plus tab-opening requests; managed loopback profiles keep local CDP defaults.
- If an externally managed CDP service is reachable through loopback, set that profile's `attachOnly: true`; otherwise OpenClaw treats the loopback port as a local managed browser profile and may report local port ownership errors.
- `existing-session` profiles use Chrome MCP instead of CDP and can attach on the selected host or through a connected browser node; they can set `userDataDir` to target a specific Chromium-based profile (Brave, Edge), and `cdpUrl` when Chrome is already running behind a DevTools HTTP(S) or WS(S) endpoint (in that mode `userDataDir` is ignored for launch arguments). They keep Chrome MCP route limits: snapshot/ref-driven actions instead of CSS-selector targeting, one-file upload hooks, no dialog timeout overrides, no `wait --load networkidle`, and no `responsebody`, PDF export, download interception, or batch actions.
- Local managed `openclaw` profiles auto-assign `cdpPort` and `cdpUrl`; set `cdpUrl` explicitly only for remote CDP profiles or existing-session endpoint attach. Local managed profiles can set `executablePath` to override the global `browser.executablePath` for that profile (run one profile in Chrome and another in Brave), and use `browser.localLaunchTimeoutMs` (Chrome CDP HTTP discovery after process start) and `browser.localCdpReadyTimeoutMs` (post-launch CDP websocket readiness) — both must be positive integers up to `120000` ms; invalid values are rejected.
- Auto-detect order: default browser if Chromium-based → Chrome → Brave → Edge → Chromium → Chrome Canary. `browser.executablePath` and `browser.profiles.<name>.executablePath` both accept `~` and `~/...` (per-profile `userDataDir` on `existing-session` profiles is also tilde-expanded).
- Control service: loopback only (port derived from `gateway.port`, default `18791`). `extraArgs` appends extra launch flags to local Chromium startup (for example `--disable-gpu`, window sizing, or debug flags).

## UI

The `ui` block sets Control UI chrome and assistant identity.

- `seamColor`: accent color for native app UI chrome (Talk Mode bubble tint, etc.).
- `assistant`: Control UI identity override (`name`, `avatar` accepting an emoji, short text, image URL, or data URI). Falls back to active agent identity.

## Gateway

The `gateway` block configures the server itself: mode, port, bind, auth, Tailscale, Control UI, remote-client credentials, node command shaping, HTTP tool denies, and push relay. Selected field details:

- `mode`: `local` (run gateway) or `remote` (connect to a remote gateway); the gateway refuses to start unless `local`.
- `port`: single multiplexed port for WS + HTTP. Precedence: `--port` > `OPENCLAW_GATEWAY_PORT` > `gateway.port` > `18789`.
- `bind`: `auto`, `loopback` (default), `lan` (`0.0.0.0`), `tailnet` (Tailscale IP only), or `custom`. Use bind-mode values, not host aliases. Docker note: the default `loopback` bind listens on `127.0.0.1` inside the container; with bridge networking (`-p 18789:18789`) traffic arrives on `eth0` and is unreachable — use `--network host`, `bind: "lan"`, or `bind: "custom"` with `customBindHost: "0.0.0.0"`.
- Auth is required by default; non-loopback binds require gateway auth (a shared token/password or `gateway.auth.mode: "trusted-proxy"`). If both `gateway.auth.token` and `gateway.auth.password` are configured, set `gateway.auth.mode` explicitly to `token` or `password` (startup/install fails when both are set and mode is unset). `gateway.auth.mode: "none"` is explicit no-auth (trusted local loopback only). `gateway.auth.mode: "trusted-proxy"` delegates browser/user auth to an identity-aware reverse proxy and trusts identity headers from `gateway.trustedProxies`; it expects a non-loopback proxy source by default (same-host loopback requires `gateway.auth.trustedProxy.allowLoopback = true`).
- `gateway.auth.allowTailscale`: when `true`, Tailscale Serve identity headers can satisfy Control UI/WebSocket auth (verified via `tailscale whois`); HTTP API endpoints do not use that header auth and follow the normal HTTP auth mode. Defaults to `true` when `tailscale.mode = "serve"`.
- `gateway.auth.rateLimit`: optional failed-auth limiter, per client IP and per auth scope (shared-secret and device-token tracked independently); blocked attempts return `429` + `Retry-After`. `rateLimit.exemptLoopback` defaults to `true`; set `false` to rate-limit localhost too. Browser-origin WS auth attempts are always throttled with loopback exemption disabled, isolated per normalized `Origin` value on loopback.
- `tailscale.mode`: `serve` (tailnet only, loopback bind) or `funnel` (public, requires auth); `tailscale.serviceName` is an optional `svc:<dns-label>` Service name for Serve mode; `tailscale.preserveFunnel` skips re-applying Serve at startup if an externally configured Funnel already covers the port (default `false`).
- `controlUi.allowedOrigins`: explicit browser-origin allowlist required for public non-loopback origins. `controlUi.chatMessageMaxWidth` accepts constrained CSS widths (e.g. `min(1280px, 82%)`). `controlUi.dangerouslyAllowHostHeaderOriginFallback` is a dangerous Host-header origin fallback mode.
- `remote.transport`: `ssh` (default) or `direct` (ws/wss); for `direct`, `remote.url` must be `wss://` for public hosts. `remote.remotePort` is the gateway port on the remote SSH host (default `18789`). `gateway.remote.token`/`.password` are remote-client credential fields and do not configure gateway auth by themselves.
- `gateway.push.apns.relay.baseUrl`: base HTTPS URL for the external APNs relay used by official/TestFlight iOS builds (must match the relay URL compiled into the iOS build); `gateway.push.apns.relay.timeoutMs` defaults to `10000`. `OPENCLAW_APNS_RELAY_BASE_URL`/`_TIMEOUT_MS` are temporary env overrides; `OPENCLAW_APNS_RELAY_ALLOW_HTTP=true` is a development-only escape hatch for loopback HTTP relay URLs.
- `gateway.handshakeTimeoutMs`: pre-auth WebSocket handshake timeout (default `15000`; `OPENCLAW_HANDSHAKE_TIMEOUT_MS` takes precedence). `gateway.channelHealthCheckMinutes` (default `5`; `0` disables), `gateway.channelStaleEventThresholdMinutes` (default `30`, keep ≥ health-check), and `gateway.channelMaxRestartsPerHour` (default `10`) control channel health-monitor restarts; per-channel/account `healthMonitor.enabled` opt-outs apply.
- `trustedProxies`: reverse-proxy IPs that terminate TLS or inject forwarded-client headers (list only proxies you control; loopback entries are valid for same-host detection but do not make loopback requests eligible for trusted-proxy mode). `allowRealIpFallback` (default `false`): accept `X-Real-IP` when `X-Forwarded-For` is missing.
- `gateway.nodes.pairing.autoApproveCidrs`: optional CIDR/IP allowlist for auto-approving first-time no-scope node pairing (disabled when unset; does not auto-approve operator/browser/Control UI/WebChat pairing or role/scope upgrades). `gateway.nodes.allowCommands`/`denyCommands` shape declared node commands (opt into dangerous commands like `camera.snap`/`screen.record` via `allowCommands`; `denyCommands` removes a command even if otherwise allowed).
- `gateway.tools.deny`: extra tool names blocked for HTTP `POST /tools/invoke` (extends default deny). `gateway.tools.allow`: removes tool names from the default HTTP deny list for owner/admin callers; this does not upgrade `operator.write` callers into owner/admin access (`cron`, `gateway`, `nodes` remain unavailable to non-owner callers even when allowlisted).
- OpenAI-compatible endpoints and multi-instance isolation are documented in the runtime sibling reference; the `gateway.http.endpoints.*` and `OPENCLAW_CONFIG_PATH`/`OPENCLAW_STATE_DIR` surfaces live there.

### `gateway.tls`

```json5
{
  gateway: {
    tls: {
      enabled: false,
      autoGenerate: false,
      certPath: "/etc/openclaw/tls/server.crt",
      keyPath: "/etc/openclaw/tls/server.key",
      caPath: "/etc/openclaw/tls/ca-bundle.crt",
    },
  },
}
```

- `enabled`: enables TLS termination at the gateway listener (HTTPS/WSS) (default: `false`).
- `autoGenerate`: auto-generates a local self-signed cert/key pair when explicit files are not configured; for local/dev use only.
- `certPath`: filesystem path to the TLS certificate file.
- `keyPath`: filesystem path to the TLS private key file; keep permission-restricted.
- `caPath`: optional CA bundle path for client verification or custom trust chains.

### `gateway.reload`

- `mode`: controls how config edits are applied at runtime — `"off"` (ignore live edits; changes require an explicit restart), `"restart"` (always restart the process on config change), `"hot"` (apply in-process without restarting), or `"hybrid"` (default; try hot reload first, fall back to restart if required).
- `debounceMs`: debounce window in ms before config changes are applied (non-negative integer).
- `deferralTimeoutMs`: optional maximum time in ms to wait for in-flight operations before forcing a restart or channel hot reload. Omit it to use the default bounded wait (`300000`); set `0` to wait indefinitely and log periodic still-pending warnings.

**Source**: OpenClaw documentation — `gateway/configuration-reference` (mirror `inbox/openclaw_docs/gateway/configuration-reference.md`), platform/surface cluster
**Last Updated**: 2026-06-22
**Status**: Active
