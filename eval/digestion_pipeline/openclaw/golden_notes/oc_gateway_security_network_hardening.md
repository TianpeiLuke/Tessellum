---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - network_hardening
keywords:
  - openclaw gateway network hardening
  - gateway bind loopback lan tailnet
  - docker ufw docker-user firewall
  - mdns bonjour minimal mode
  - lock down gateway websocket auth
  - gateway.trustedProxies x-forwarded-for
  - tailscale serve identity headers
  - control ui over http secure context
  - hsts allowedorigins
  - gateway.auth token password trusted-proxy
topics:
  - OpenClaw
  - Gateway Network Hardening
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/security
access_control_group: ["general"]
---

# OpenClaw — Gateway Network & Transport Hardening

## Overview

This note is the network/transport-layer hardening procedure for the OpenClaw Gateway, mirroring the network-facing sections of the `gateway/security` source page: how the Gateway binds and firewalls its single WebSocket+HTTP port, how to align Docker-published ports with the host firewall via `DOCKER-USER`, how to suppress mDNS/Bonjour reconnaissance leakage, how to lock down and authenticate the Gateway WebSocket (auth modes plus a rotation checklist), Tailscale Serve identity-header behavior, reverse-proxy `trustedProxies`/forwarded-header handling, HSTS/origin policy, and the Control-UI-over-HTTP secure-context rules. These are the controls that resolve `gateway.*` audit findings before any non-loopback exposure.

## Network exposure (bind, port, firewall)

The Gateway multiplexes **WebSocket + HTTP** on a single port. Default port `18789`; configurable via `gateway.port`, `--port`, or `OPENCLAW_GATEWAY_PORT`. This HTTP surface includes the **Control UI** (SPA assets, default base path `/`) and the **canvas host** (`/__openclaw__/canvas/` and `/__openclaw__/a2ui/`, which serve arbitrary HTML/JS and must be treated as untrusted content). Treat canvas content like any untrusted web page: do not expose the canvas host to untrusted networks/users, and do not let canvas content share the same origin as privileged web surfaces unless you fully understand the implications.

Bind mode controls where the Gateway listens. `gateway.bind: "loopback"` (default) allows only local clients. Non-loopback binds (`"lan"`, `"tailnet"`, `"custom"`) expand the attack surface and must be used only with gateway auth (shared token/password or a correctly configured trusted proxy) and a real firewall. Rules of thumb: prefer Tailscale Serve over LAN binds (Serve keeps the Gateway on loopback and Tailscale handles access); if you must bind to LAN, firewall the port to a tight allowlist of source IPs and do not port-forward it broadly; **never expose the Gateway unauthenticated on `0.0.0.0`**.

## Docker port publishing with UFW

If you run OpenClaw with Docker on a VPS, published container ports (`-p HOST:CONTAINER` or Compose `ports:`) route through Docker's forwarding chains, **not** only host `INPUT` rules. To keep Docker traffic aligned with your firewall policy, enforce rules in `DOCKER-USER` (evaluated before Docker's own accept rules). On many modern distros, `iptables`/`ip6tables` use the `iptables-nft` frontend and still apply these rules to the nftables backend.

Minimal allowlist example (IPv4):

```bash
# /etc/ufw/after.rules (append as its own *filter section)
*filter
:DOCKER-USER - [0:0]
-A DOCKER-USER -m conntrack --ctstate ESTABLISHED,RELATED -j RETURN
-A DOCKER-USER -s 127.0.0.0/8 -j RETURN
-A DOCKER-USER -s 10.0.0.0/8 -j RETURN
-A DOCKER-USER -s 172.16.0.0/12 -j RETURN
-A DOCKER-USER -s 192.168.0.0/16 -j RETURN
-A DOCKER-USER -s 100.64.0.0/10 -j RETURN
-A DOCKER-USER -p tcp --dport 80 -j RETURN
-A DOCKER-USER -p tcp --dport 443 -j RETURN
-A DOCKER-USER -m conntrack --ctstate NEW -j DROP
-A DOCKER-USER -j RETURN
COMMIT
```

IPv6 has separate tables: add a matching policy in `/etc/ufw/after6.rules` if Docker IPv6 is enabled. Avoid hardcoding interface names like `eth0` — they vary across VPS images (`ens3`, `enp*`, etc.) and mismatches can accidentally skip your deny rule. After reload, validate with `ufw reload`, `iptables -S DOCKER-USER`, `ip6tables -S DOCKER-USER`, and `nmap -sT -p 1-65535 <public-ip> --open`; expected external ports should be only what you intentionally expose (for most setups: SSH + your reverse proxy ports).

## mDNS/Bonjour discovery

When the bundled `bonjour` plugin is enabled, the Gateway broadcasts its presence via mDNS (`_openclaw-gw._tcp` on port 5353) for local device discovery. In **full mode** this includes TXT records that may expose operational details: `cliPath` (full filesystem path to the CLI binary, revealing username and install location), `sshPort` (advertises SSH availability), and `displayName`/`lanHost` (hostname information). Broadcasting these details makes reconnaissance easier for anyone on the local network — even "harmless" info like filesystem paths and SSH availability helps attackers map the environment.

Recommendations: (1) **Keep Bonjour disabled unless LAN discovery is needed** — Bonjour auto-starts on macOS hosts and is opt-in elsewhere; direct Gateway URLs, Tailnet, SSH, or wide-area DNS-SD avoid local multicast. (2) **Minimal mode** is the default when Bonjour is enabled and is recommended for exposed gateways — it omits sensitive fields. (3) **Disable mDNS mode** to keep the plugin enabled but suppress discovery. (4) **Full mode** is opt-in. (5) Alternatively, set env `OPENCLAW_DISABLE_BONJOUR=1` to disable mDNS without config changes. In minimal mode the Gateway broadcasts enough for device discovery (`role`, `gatewayPort`, `transport`) but omits `cliPath` and `sshPort`; apps needing the CLI path fetch it via the authenticated WebSocket instead.

```json5
{
  discovery: {
    mdns: { mode: "minimal" }, // or "off" to suppress, "full" to opt into cliPath + sshPort
  },
}
```

## Lock down the Gateway WebSocket (local auth)

Gateway auth is **required by default**: if no valid gateway auth path is configured, the Gateway refuses WebSocket connections (fail-closed). Onboarding generates a token by default (even for loopback) so local clients must authenticate. Set a token so **all** WS clients must authenticate; `openclaw doctor --generate-gateway-token` can generate one for you.

```json5
{
  gateway: {
    auth: { mode: "token", token: "your-token" },
  },
}
```

`gateway.remote.token` and `gateway.remote.password` are **client** credential sources — they do not protect local WS access by themselves. Local call paths can use `gateway.remote.*` as fallback only when `gateway.auth.*` is unset; if `gateway.auth.token` or `gateway.auth.password` is explicitly configured via SecretRef and unresolved, resolution fails closed (no remote-fallback masking). Optionally pin remote TLS with `gateway.remote.tlsFingerprint` when using `wss://`. Plaintext `ws://` is accepted for loopback, private IP literals, `.local`, and Tailnet `*.ts.net` gateway URLs; for other trusted private-DNS names, set `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` on the **client process** as break-glass (intentionally process-environment only, not an `openclaw.json` key). Mobile pairing and Android manual/scanned gateway routes are stricter: cleartext is accepted for loopback, but private-LAN, link-local, `.local`, and dotless hostnames must use TLS unless you explicitly opt into the trusted private-network cleartext path.

Local device pairing: device pairing is auto-approved for direct local loopback connects to keep same-host clients smooth; there is a narrow backend/container-local self-connect path for trusted shared-secret helper flows; Tailnet and LAN connects (including same-host tailnet binds) are treated as remote and still need approval; forwarded-header evidence on a loopback request disqualifies loopback locality, and metadata-upgrade auto-approval is scoped narrowly.

### Auth modes and rotation

The three auth modes are: `gateway.auth.mode: "token"` (shared bearer token, recommended for most setups); `gateway.auth.mode: "password"` (prefer setting via env `OPENCLAW_GATEWAY_PASSWORD`); and `gateway.auth.mode: "trusted-proxy"` (trust an identity-aware reverse proxy to authenticate users and pass identity via headers). The token/password rotation checklist: (1) generate/set a new secret (`gateway.auth.token` or `OPENCLAW_GATEWAY_PASSWORD`); (2) restart the Gateway (or the macOS app if it supervises it); (3) update any remote clients (`gateway.remote.token` / `.password`); (4) verify you can no longer connect with the old credentials.

## Tailscale Serve identity headers

When `gateway.auth.allowTailscale` is `true` (default for Serve), OpenClaw accepts Tailscale Serve identity headers (`tailscale-user-login`) for Control UI/WebSocket authentication. OpenClaw verifies the identity by resolving the `x-forwarded-for` address through the local Tailscale daemon (`tailscale whois`) and matching it to the header. This only triggers for requests that hit loopback and include `x-forwarded-for`, `x-forwarded-proto`, and `x-forwarded-host` as injected by Tailscale. For this async identity-check path, failed attempts for the same `{scope, ip}` are serialized before the limiter records the failure, so concurrent bad retries from one Serve client can lock out the second attempt immediately instead of racing through as two plain mismatches. HTTP API endpoints (for example `/v1/*`, `/tools/invoke`, and `/api/channels/*`) do **not** use Tailscale identity-header auth — they still follow the gateway's configured HTTP auth mode.

Important boundary note: Gateway HTTP bearer auth is effectively all-or-nothing operator access. Treat credentials that can call `/v1/chat/completions`, `/v1/responses`, plugin routes such as `/api/v1/admin/rpc`, or `/api/channels/*` as full-access operator secrets. On the OpenAI-compatible HTTP surface, shared-secret bearer auth restores the full default operator scopes (`operator.admin`, `operator.approvals`, `operator.pairing`, `operator.read`, `operator.talk.secrets`, `operator.write`) and owner semantics for agent turns; narrower `x-openclaw-scopes` values do not reduce that shared-secret path. Per-request scope semantics on HTTP only apply from an identity-bearing mode (trusted-proxy auth, or an explicitly no-auth private ingress); there, omitting `x-openclaw-scopes` falls back to the normal operator default scope set, and owner-level headers such as `x-openclaw-model` require `operator.admin` when scopes are narrowed. `/tools/invoke` and HTTP session-history endpoints follow the same shared-secret rule.

**Trust assumption:** tokenless Serve auth assumes the gateway host is trusted; it is not protection against hostile same-host processes. If untrusted local code may run on the gateway host, disable `gateway.auth.allowTailscale` and require explicit shared-secret auth (`gateway.auth.mode: "token"` or `"password"`). **Security rule:** do not forward these headers from your own reverse proxy; if you terminate TLS or proxy in front of the gateway, disable `gateway.auth.allowTailscale` and use shared-secret auth or Trusted Proxy Auth instead. (The full Serve/Funnel doc lives in the [OpenClaw — Tailscale](oc_gateway_tailscale.md) note.)

## Reverse proxy configuration

If you run the Gateway behind a reverse proxy (nginx, Caddy, Traefik, etc.), configure `gateway.trustedProxies` for proper forwarded-client-IP handling. When the Gateway detects proxy headers from an address that is **not** in `trustedProxies`, it will not treat connections as local clients; if gateway auth is disabled, those connections are rejected — this prevents authentication bypass where proxied connections would otherwise appear to come from localhost and receive automatic trust.

`gateway.trustedProxies` also feeds `gateway.auth.mode: "trusted-proxy"`, but that auth mode is stricter: trusted-proxy auth **fails closed on loopback-source proxies by default**; same-host loopback reverse proxies can use `gateway.trustedProxies` for local-client detection and forwarded-IP handling; and same-host loopback reverse proxies can satisfy `gateway.auth.mode: "trusted-proxy"` only when `gateway.auth.trustedProxy.allowLoopback = true` (otherwise use token/password auth).

```yaml
gateway:
  trustedProxies:
    - "10.0.0.1" # reverse proxy IP
  # Optional. Default false.
  # Only enable if your proxy cannot provide X-Forwarded-For.
  allowRealIpFallback: false
  auth:
    mode: password
    password: ${OPENCLAW_GATEWAY_PASSWORD}
```

When `trustedProxies` is configured, the Gateway uses `X-Forwarded-For` to determine the client IP; `X-Real-IP` is ignored by default unless `gateway.allowRealIpFallback: true` is explicitly set. Trusted proxy headers do not make node device pairing automatically trusted: `gateway.nodes.pairing.autoApproveCidrs` is a separate, disabled-by-default operator policy, and even when enabled, loopback-source trusted-proxy header paths are excluded from node auto-approval because local callers can forge those headers. Good reverse-proxy behavior **overwrites** incoming forwarding headers; bad behavior appends/preserves untrusted forwarding headers:

```nginx
# Good (overwrite incoming forwarding headers):
proxy_set_header X-Forwarded-For $remote_addr;
proxy_set_header X-Real-IP $remote_addr;
# Bad (append/preserve untrusted forwarding headers):
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

## HSTS and origin notes

The OpenClaw gateway is local/loopback first. If you terminate TLS at a reverse proxy, set HSTS on the proxy-facing HTTPS domain there. If the gateway itself terminates HTTPS, set `gateway.http.securityHeaders.strictTransportSecurity` to emit the HSTS header from OpenClaw responses (detailed guidance in Trusted Proxy Auth → TLS termination and HSTS). For non-loopback Control UI deployments, `gateway.controlUi.allowedOrigins` is required by default; `gateway.controlUi.allowedOrigins: ["*"]` is an explicit allow-all browser-origin policy, not a hardened default — avoid it outside tightly controlled local testing. Browser-origin auth failures on loopback are still rate-limited even when the general loopback exemption is enabled, but the lockout key is scoped per normalized `Origin` value instead of one shared localhost bucket. `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true` enables Host-header origin-fallback mode and is a dangerous operator-selected policy. Treat DNS rebinding and proxy-host header behavior as deployment hardening concerns; keep `trustedProxies` tight and avoid exposing the gateway directly to the public internet.

## Control UI over HTTP

The Control UI needs a **secure context** (HTTPS or localhost) to generate device identity. `gateway.controlUi.allowInsecureAuth` is a local compatibility toggle: on localhost it allows Control UI auth without device identity when the page loads over non-secure HTTP; it does not bypass pairing checks and does not relax remote (non-localhost) device-identity requirements. Prefer HTTPS (Tailscale Serve) or open the UI on `127.0.0.1`. For break-glass only, `gateway.controlUi.dangerouslyDisableDeviceAuth` disables device-identity checks entirely — a severe security downgrade; keep it off unless you are actively debugging and can revert quickly. Separately, a successful `gateway.auth.mode: "trusted-proxy"` can admit **operator** Control UI sessions without device identity; that is intentional auth-mode behavior, not an `allowInsecureAuth` shortcut, and still does not extend to node-role Control UI sessions. `openclaw security audit` warns when `allowInsecureAuth` is enabled.

**Source**: OpenClaw documentation — `gateway/security` (mirror `inbox/openclaw_docs/gateway/security.md`)
**Last Updated**: 2026-06-22
**Status**: Active
