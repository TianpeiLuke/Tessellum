---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - network_proxy
keywords:
  - openclaw forward proxy
  - proxy.enabled proxyUrl
  - openclaw runtime egress routing
  - proxyline process routing
  - proxy loopbackmode gateway-only
  - openclaw_proxy_url env fallback
  - no_proxy clearing ssrf
  - http vs https proxy endpoint
topics:
  - OpenClaw
  - Network Proxy
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/security/network-proxy
access_control_group: ["general"]
---

# OpenClaw — Routing Runtime Egress Through a Forward Proxy

## Overview

This note is the **routing and configuration** procedure for OpenClaw's operator-managed forward proxy — the first half of the `security/network-proxy` source page (intro → Why use a proxy → How OpenClaw routes traffic → Related proxy terms → Configuration incl. Gateway Loopback Mode). It covers why an operator would route runtime HTTP and WebSocket egress through a filtering proxy, how OpenClaw routes that traffic via Proxyline (including the `http://` vs `https://` proxy-endpoint distinction, `no_proxy` clearing, and plugin custom transports), how to configure it via `proxy.enabled` / `proxy.proxyUrl` / the `OPENCLAW_PROXY_URL` env fallback, and the `proxy.loopbackMode` Gateway control-plane exception. The proxy-policy **requirements, the recommended SSRF denylist, validation, CA trust, and the coverage limits** are the hardening half — see the sibling note `oc_security_network_proxy_hardening.md`.

## Why use a proxy

OpenClaw can route runtime HTTP and WebSocket traffic through an **operator-managed forward proxy**. This is *optional defense in depth* for deployments that want central egress control, stronger SSRF protection, and better network auditability. OpenClaw does not ship, download, start, configure, or certify a proxy: the operator runs the proxy technology that fits their environment, and OpenClaw routes normal process-local HTTP and WebSocket clients through it. A proxy gives operators one network control point for outbound HTTP and WebSocket traffic, which is useful even outside SSRF hardening:

- **Central policy** — maintain one egress policy instead of relying on every application HTTP call site to get network rules right.
- **Connect-time checks** — evaluate the destination after DNS resolution and immediately before the proxy opens the upstream connection.
- **DNS rebinding defense** — reduce the gap between an application-level DNS check and the actual outbound connection.
- **Broader JavaScript coverage** — route ordinary `fetch`, `node:http`, `node:https`, WebSocket, axios, got, node-fetch, and similar clients through the same path.
- **Auditability** — log allowed and denied destinations at the egress boundary.
- **Operational control** — enforce destination rules, network segmentation, rate limits, or outbound allowlists without rebuilding OpenClaw.

Proxy routing is a **process-level guardrail** for normal HTTP and WebSocket egress. It gives operators a *fail-closed* path for routing supported JavaScript HTTP clients through their own filtering proxy, but it is **not an OS-level network sandbox** and does not make OpenClaw certify the proxy's destination policy.

## How OpenClaw routes traffic

When `proxy.enabled=true` and a proxy URL is configured, protected runtime processes such as `openclaw gateway run`, `openclaw node run`, and `openclaw agent --local` route normal HTTP and WebSocket egress through the configured proxy:

```text
OpenClaw process
  fetch                  -> operator-managed filtering proxy -> public internet
  node:http and https    -> operator-managed filtering proxy -> public internet
  WebSocket clients      -> operator-managed filtering proxy -> public internet
```

The public contract is the **routing behavior**, not the internal Node hooks used to implement it. OpenClaw Gateway control-plane WebSocket clients use a narrow direct path for local loopback Gateway RPC traffic when the Gateway URL uses `localhost` or a literal loopback IP such as `127.0.0.1` or `[::1]`. That control-plane path must be able to reach loopback Gateways even when the operator proxy blocks loopback destinations; normal runtime HTTP and WebSocket requests still use the configured proxy.

Internally, OpenClaw installs **Proxyline** as the process-level routing runtime for this feature. Proxyline covers `fetch`, undici-backed clients, Node core `node:http` / `node:https` callers, common WebSocket clients, and helper-created CONNECT tunnels. Managed proxy mode replaces caller-provided Node HTTP agents so explicit agents do not accidentally bypass the operator proxy. Some plugins own custom transports that need explicit proxy wiring even when process-level routing exists — for example, Telegram's Bot API transport uses its own HTTP/1 undici dispatcher and therefore honors process proxy env plus the managed `OPENCLAW_PROXY_URL` fallback in that owner-specific transport path.

### `http://` vs `https://` proxy endpoint

The proxy URL itself can use either `http://` or `https://`. These schemes describe the connection **from OpenClaw to the proxy endpoint** (not to the destination):

- `http://proxy.example:3128` — OpenClaw opens a plain TCP connection to the forward proxy and sends HTTP proxy requests, including `CONNECT` for HTTPS destinations.
- `https://proxy.example:8443` — OpenClaw opens TLS to the proxy endpoint, verifies the proxy certificate, and then sends HTTP proxy requests inside that TLS session.

Destination HTTPS is **separate** from proxy endpoint TLS: for an HTTPS destination, OpenClaw still asks the proxy for an HTTP `CONNECT` tunnel and then starts destination TLS through that tunnel.

While the proxy is active, OpenClaw **clears `no_proxy` and `NO_PROXY`**. Those bypass lists are destination-based, so leaving `localhost` or `127.0.0.1` there would let high-risk SSRF targets skip the filtering proxy. On shutdown, OpenClaw restores the previous proxy environment and resets cached process routing state.

**Source**: OpenClaw documentation — `security/network-proxy` (mirror `inbox/openclaw_docs/security/network-proxy.md`), routing/config half
**Last Updated**: 2026-06-22
**Status**: Active
