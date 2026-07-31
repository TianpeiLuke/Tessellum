---
tags:
  - resource
  - documentation
  - openclaw
  - security
  - network_proxy
keywords:
  - openclaw proxy hardening
  - ssrf denylist blocked destinations
  - proxy requirements fail-closed
  - openclaw proxy validate
  - proxy.tls.caFile node_extra_ca_certs
  - ssrf.ts ip.ts parity hooks
  - cloud metadata 169.254.169.254
  - managed proxy limits irc raw sockets
topics:
  - OpenClaw
  - Network Proxy Hardening
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/security/network-proxy
access_control_group: ["general"]
---

# OpenClaw — Hardening the Forward Proxy (Requirements, SSRF Denylist, Validation, CA Trust, Limits)

## Overview

This note is the operator hardening procedure for OpenClaw's managed forward proxy — the second half of the `security/network-proxy` source page (the routing/configuration half is its sibling [oc_security_network_proxy_routing](oc_security_network_proxy_routing.md)). It covers what the proxy MUST do to be a real security boundary (Proxy Requirements), the recommended SSRF denylist of loopback / RFC1918 / link-local / cloud-metadata / NAT64 / 6to4 / Teredo ranges (mirroring the `ssrf.ts` parity hooks), how to validate the proxy with `openclaw proxy validate` (JSON + `curl`), how to trust a private-CA proxy endpoint with `proxy.tls.caFile` vs `NODE_EXTRA_CA_CERTS`, and the coverage Limits (raw sockets, IRC, debug proxy, loopback bypass). The premise throughout: **the proxy policy is the security boundary, and OpenClaw cannot verify that the proxy blocks the right targets** — so hardening is the operator's responsibility.

## Proxy Requirements

The proxy policy is the security boundary; OpenClaw cannot verify that the proxy blocks the right targets, so the operator must configure the proxy correctly. Configure the proxy to:

- **Bind only to loopback or a private trusted interface.**
- **Restrict access** so only the OpenClaw process, host, container, or service account can use it.
- **Resolve destinations itself and block destination IPs after DNS resolution** — i.e. post-DNS IP blocking, which closes the DNS-rebinding gap.
- **Apply policy at connect time** for both plain HTTP requests and HTTPS `CONNECT` tunnels.
- **Reject destination-based bypasses** for loopback, private, link-local, metadata, multicast, reserved, or documentation ranges.
- **Avoid hostname allowlists** unless you fully trust the DNS resolution path.
- **Log destination, decision, status, and reason** without logging request bodies, authorization headers, cookies, or other secrets.
- **Keep proxy policy under version control** and review changes like security-sensitive configuration.

These requirements are fail-closed in spirit: they instruct the proxy to deny bypasses and apply policy before opening the upstream connection rather than after.

## Recommended blocked destinations

Use this denylist as the starting point for any forward proxy, firewall, or egress policy. OpenClaw's own application-level SSRF classifier logic lives in `src/infra/net/ssrf.ts` and `packages/net-policy/src/ip.ts`. The relevant parity hooks are `BLOCKED_HOSTNAMES`, `BLOCKED_IPV4_SPECIAL_USE_RANGES`, `BLOCKED_IPV6_SPECIAL_USE_RANGES`, `RFC2544_BENCHMARK_PREFIX`, and the embedded IPv4 sentinel handling for NAT64, 6to4, Teredo, ISATAP, and IPv4-mapped forms. Those files are useful references when maintaining an external proxy policy, but **OpenClaw does not automatically export or enforce those rules in your proxy** — you replicate them in the proxy yourself.

| Range or host | Why to block |
| --- | --- |
| `127.0.0.0/8`, `localhost`, `localhost.localdomain` | IPv4 loopback |
| `::1/128` | IPv6 loopback |
| `0.0.0.0/8`, `::/128` | Unspecified and this-network addresses |
| `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` | RFC1918 private networks |
| `169.254.0.0/16`, `fe80::/10` | Link-local addresses and common cloud metadata paths |
| `169.254.169.254`, `metadata.google.internal` | Cloud metadata services |
| `100.64.0.0/10` | Carrier-grade NAT shared address space |
| `198.18.0.0/15`, `2001:2::/48` | Benchmarking ranges |
| `192.0.0.0/24`, `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32` | Special-use and documentation ranges |
| `224.0.0.0/4`, `ff00::/8` | Multicast |
| `240.0.0.0/4` | Reserved IPv4 |
| `fc00::/7`, `fec0::/10` | IPv6 local/private ranges |
| `100::/64`, `2001:20::/28` | IPv6 discard and ORCHIDv2 ranges |
| `64:ff9b::/96`, `64:ff9b:1::/48` | NAT64 prefixes with embedded IPv4 |
| `2002::/16`, `2001::/32` | 6to4 and Teredo with embedded IPv4 |
| `::/96`, `::ffff:0:0/96` | IPv4-compatible and IPv4-mapped IPv6 |

If your cloud provider or network platform documents additional metadata hosts or reserved ranges, add those too.

## Validation

Validate the proxy from the same host, container, or service account that runs OpenClaw:

```bash
openclaw proxy validate --proxy-url http://127.0.0.1:3128
```

For an HTTPS proxy endpoint signed by a private CA, pass the CA file too:

```bash
openclaw proxy validate --proxy-url https://proxy.corp.example:8443 --proxy-ca-file /etc/openclaw/proxy-ca.pem
```

By default, when no custom destinations are provided, the command checks that `https://example.com/` succeeds and starts a temporary loopback canary that the proxy must NOT reach. The default denied check passes when the proxy returns a non-2xx denial response or blocks the canary with a transport failure; it fails if a successful response reaches the canary. If no proxy is enabled and configured, validation reports a config problem; use `--proxy-url` for a one-off preflight before changing config. Use `--allowed-url` and `--denied-url` to test deployment-specific expectations. Add `--apns-reachable` to also verify direct APNs HTTP/2 delivery can open a `CONNECT` tunnel through the proxy and receive a sandbox APNs response; the probe uses an intentionally invalid provider token, so `403 InvalidProviderToken` is expected and counts as reachable. Custom denied destinations are fail-closed: any HTTP response means the destination was reachable through the proxy, and any transport error is reported as inconclusive because OpenClaw cannot prove the proxy blocked a reachable origin. On validation failure, the command exits with code 1.

Use `--json` for automation. The JSON output contains the overall result, the effective proxy config source, any config errors, and each destination check. Proxy URL credentials are redacted in text and JSON output:

```json
{
  "ok": true,
  "config": {
    "enabled": true,
    "proxyUrl": "http://127.0.0.1:3128/",
    "source": "override",
    "errors": []
  },
  "checks": [
    {
      "kind": "allowed",
      "url": "https://example.com/",
      "ok": true,
      "status": 200
    },
    {
      "kind": "apns",
      "url": "https://api.sandbox.push.apple.com",
      "ok": true,
      "status": 403
    }
  ]
}
```

You can also validate manually with `curl`, expecting the public request to succeed and the loopback and metadata requests to be blocked by the proxy:

```bash
curl -x http://127.0.0.1:3128 https://example.com/
curl -x http://127.0.0.1:3128 http://127.0.0.1/
curl -x http://127.0.0.1:3128 http://169.254.169.254/
```

For `openclaw proxy validate`, the built-in loopback canary can distinguish a proxy denial from a reachable origin. Custom `--denied-url` checks do NOT have that canary, so treat both HTTP responses and ambiguous transport failures as validation failures unless your proxy exposes a deployment-specific denial signal you can verify separately.

## Proxy CA trust

Use managed `proxy.tls.caFile` when the proxy endpoint itself uses a certificate signed by a private CA:

```yaml
proxy:
  enabled: true
  proxyUrl: https://proxy.corp.example:8443
  tls:
    caFile: /etc/openclaw/proxy-ca.pem
```

That CA is used for TLS verification of the proxy endpoint. It is NOT a destination MITM trust setting, a client certificate, or a replacement for the proxy's destination policy. Use `NODE_EXTRA_CA_CERTS` only when the whole Node process must trust an additional CA from process startup — for example when an enterprise TLS inspection system re-signs destination certificates for every HTTPS client in the process. `NODE_EXTRA_CA_CERTS` is process-global and must be present before Node starts. Prefer `proxy.tls.caFile` for HTTPS proxy endpoint trust because it is scoped to managed proxy routing. To enable the private-CA proxy, set the three config keys and run the gateway:

```bash
openclaw config set proxy.enabled true
openclaw config set proxy.proxyUrl https://proxy.corp.example:8443
openclaw config set proxy.tls.caFile /etc/openclaw/proxy-ca.pem
openclaw gateway run
```

## Limits

Managed proxy routing improves coverage for process-local JavaScript HTTP and WebSocket clients, but it is NOT an OS-level network sandbox. The documented coverage limits are:

- **Loopback bypass default:** Gateway loopback control-plane traffic defaults to direct local bypass through `proxy.loopbackMode: "gateway-only"`, implemented by registering the active Gateway loopback authority in Proxyline's managed bypass policy. Operators can set `proxy.loopbackMode: "proxy"` to send Gateway loopback traffic through the managed proxy, or `proxy.loopbackMode: "block"` to deny loopback Gateway connections (see [oc_security_network_proxy_routing](oc_security_network_proxy_routing.md) for the remote-proxy caveat).
- **Raw sockets and native code:** Raw `net`, `tls`, and `http2` sockets, native addons, and non-OpenClaw child processes may bypass Node-level proxy routing unless they inherit and respect proxy environment variables. Forked OpenClaw child CLIs inherit the managed proxy URL and `proxy.loopbackMode` state.
- **IRC:** IRC is a raw TCP/TLS channel outside operator-managed forward proxy routing. In deployments that require all egress through that forward proxy, set `channels.irc.enabled=false` unless direct IRC egress is explicitly approved.
- **Debug proxy:** The local debug proxy is diagnostic tooling and its direct upstream forwarding for proxy requests and `CONNECT` tunnels is disabled by default while managed proxy mode is active; enable direct forwarding only for approved local diagnostics.
- **Local WebUIs / model servers:** User local WebUIs and local model servers should be allowlisted in the operator proxy policy when needed; OpenClaw does not expose a general local-network bypass for them. The bundled Ollama memory embedding provider is narrower — it can use a guarded direct path only for the exact host-local loopback embedding origin derived from the configured `baseUrl`, so host-local embeddings keep working when the managed proxy cannot reach host loopback; LAN, tailnet, private-network, and public Ollama embedding hosts still use the managed proxy path. `proxy.loopbackMode: "proxy"` sends this Ollama loopback traffic through the managed proxy, and `proxy.loopbackMode: "block"` denies it before opening a connection.
- **Gateway control-plane bypass scope:** Gateway control-plane proxy bypass is intentionally limited to `localhost` and literal loopback IP URLs — use `ws://127.0.0.1:18789`, `ws://[::1]:18789`, or `ws://localhost:18789`; other hostnames route like ordinary hostname-based traffic.
- OpenClaw does not inspect, test, or certify your proxy policy, and proxy policy changes should be treated as security-sensitive operational changes.

The per-surface managed-proxy status table summarizes which egress paths are covered:

| Surface | Managed proxy status |
| --- | --- |
| `fetch`, `node:http`, `node:https`, common WebSocket clients | Routed through managed proxy hooks when configured. |
| APNs direct HTTP/2 | Routed through the APNs managed `CONNECT` helper. |
| Gateway control-plane loopback | Direct only for the configured local loopback Gateway URL. |
| Debug proxy upstream forwarding | Disabled while managed proxy mode is active unless explicitly enabled for local diagnostics. |
| IRC | Raw TCP/TLS; not proxied by managed HTTP proxy mode. Disable unless direct IRC egress is approved. |
| Other raw `net`, `tls`, or `http2` client calls | Must be classified by the raw socket guard before landing. |

**Source**: OpenClaw documentation — `security/network-proxy` (mirror `inbox/openclaw_docs/security/network-proxy.md`)
**Last Updated**: 2026-06-22
**Status**: Active
