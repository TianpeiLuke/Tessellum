---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - bonjour
keywords:
  - openclaw bonjour discovery
  - wide-area dns-sd tailscale
  - _openclaw-gw._tcp service type
  - bonjour txt keys hints
  - discovery.mdns.mode minimal full
  - openclaw dns setup coredns
  - gateway listener security bind tailnet
  - openclaw_disable_bonjour env var
topics:
  - OpenClaw
  - Bonjour Discovery
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/bonjour
access_control_group: ["general"]
---

# OpenClaw — Configuring Bonjour (DNS-SD) Gateway Discovery

## Overview

This note is the **setup-and-configuration procedure** for OpenClaw's Bonjour (mDNS / DNS-SD) Gateway discovery, mirroring the configuration half of the `gateway/bonjour` source page. OpenClaw can use Bonjour to discover an active Gateway's WebSocket endpoint: multicast `local.` browsing is a **LAN-only convenience** owned by the bundled `bonjour` plugin, and a **wide-area Unicast DNS-SD** path over Tailscale extends the same discovery UX across networks. It covers the wide-area setup (Gateway config, one-time DNS server install, Tailscale split DNS, and listener security), what the Gateway advertises (the single service type and its non-secret TXT hint keys), when to enable versus disable Bonjour, and the enable/disable/configuration knobs (plugin commands and environment overrides). Discovery is **best-effort** and does **not** replace SSH or Tailnet-based connectivity. The debugging and failure-mode material is captured separately in [oc_gateway_bonjour_troubleshooting](oc_gateway_bonjour_troubleshooting.md).

The bundled `bonjour` plugin owns LAN advertising. It **auto-starts on macOS hosts** and is **opt-in** on Linux, Windows, and containerized Gateway deployments. For cross-network discovery, the same beacon can also be published through a configured wide-area DNS-SD domain.

## Wide-area Bonjour (Unicast DNS-SD) over Tailscale

If the node and gateway are on different networks, multicast mDNS won't cross the boundary. You can keep the same discovery UX by switching to **unicast DNS-SD** ("Wide-Area Bonjour") over Tailscale. The high-level steps are:

1. Run a DNS server on the gateway host (reachable over Tailnet).
2. Publish DNS-SD records for `_openclaw-gw._tcp` under a dedicated zone (example: `openclaw.internal.`).
3. Configure Tailscale **split DNS** so your chosen domain resolves via that DNS server for clients (including iOS).

OpenClaw supports any discovery domain; `openclaw.internal.` is just an example. iOS/Android nodes browse both `local.` and your configured wide-area domain.

### Gateway config (recommended)

Set the Gateway to bind tailnet-only and enable wide-area DNS-SD publishing:

```json5
{
  gateway: { bind: "tailnet" }, // tailnet-only (recommended)
  discovery: { wideArea: { enabled: true } }, // enables wide-area DNS-SD publishing
}
```

### One-time DNS server setup (gateway host)

Run the one-time DNS setup on the gateway host:

```bash
openclaw dns setup --apply
```

This installs **CoreDNS** and configures it to listen on **port 53 only on the gateway's Tailscale interfaces**, and to serve your chosen domain (example: `openclaw.internal.`) from `~/.openclaw/dns/<domain>.db`. Validate from a tailnet-connected machine:

```bash
dns-sd -B _openclaw-gw._tcp openclaw.internal.
dig @<TAILNET_IPV4> -p 53 _openclaw-gw._tcp.openclaw.internal PTR +short
```

### Tailscale DNS settings

In the Tailscale admin console, add a nameserver pointing at the gateway's tailnet IP (UDP/TCP 53), and add split DNS so your discovery domain uses that nameserver. Once clients accept tailnet DNS, iOS nodes and CLI discovery can browse `_openclaw-gw._tcp` in your discovery domain without multicast.

### Gateway listener security (recommended)

The Gateway WS port (default `18789`) binds to **loopback by default**. For LAN/tailnet access, bind explicitly and keep auth enabled. For tailnet-only setups, set `gateway.bind: "tailnet"` in `~/.openclaw/openclaw.json` and restart the Gateway (or restart the macOS menubar app).

## What advertises

Only the **Gateway** advertises `_openclaw-gw._tcp`. LAN multicast advertising is provided by the bundled `bonjour` plugin when the plugin is enabled; wide-area DNS-SD publishing remains **Gateway-owned**.

## Service types

- `_openclaw-gw._tcp` — gateway transport beacon (used by macOS/iOS/Android nodes).

## TXT keys (non-secret hints)

The Gateway advertises small non-secret hints to make UI flows convenient:

- `role=gateway`
- `displayName=<friendly name>`
- `lanHost=<hostname>.local`
- `gatewayPort=<port>` (Gateway WS + HTTP)
- `gatewayTls=1` (only when TLS is enabled)
- `gatewayTlsSha256=<sha256>` (only when TLS is enabled and fingerprint is available)
- `canvasPort=<port>` (only when the canvas host is enabled; currently the same as `gatewayPort`)
- `transport=gateway`
- `tailnetDns=<magicdns>` (mDNS full mode only, optional hint when Tailnet is available)
- `sshPort=<port>` (full mode only; omitted in minimal and off modes)
- `cliPath=<path>` (full mode only; omitted in minimal and off modes)

**Security notes** (verbatim from source):

- Bonjour/mDNS TXT records are **unauthenticated**. Clients must not treat TXT as authoritative routing.
- Clients should route using the resolved service endpoint (SRV + A/AAAA). Treat `lanHost`, `tailnetDns`, `gatewayPort`, and `gatewayTlsSha256` as hints only.
- SSH auto-targeting should likewise use the resolved service host, not TXT-only hints.
- TLS pinning **must never** allow an advertised `gatewayTlsSha256` to override a previously stored pin.
- iOS/Android nodes should treat discovery-based direct connects as **TLS-only** and require explicit user confirmation before trusting a first-time fingerprint.

## When to enable Bonjour

Bonjour **auto-starts for empty-config Gateway startup on macOS hosts** because the local app and nearby iOS/Android nodes commonly rely on same-LAN discovery. Enable Bonjour explicitly when same-LAN auto-discovery is useful on Linux, Windows, or another non-macOS host:

```bash
openclaw plugins enable bonjour
```

When enabled, Bonjour uses `discovery.mdns.mode` to decide how much TXT metadata to publish; the same mode controls optional TXT hints in wide-area DNS-SD records. The default mode is `minimal`; use `full` only when clients need `cliPath` or `sshPort` hints. Use `off` to suppress LAN multicast without changing plugin enablement — wide-area DNS-SD can still publish the minimal Gateway beacon when `discovery.wideArea.enabled` is true.

## When to disable Bonjour

Leave Bonjour disabled when LAN multicast advertising is unnecessary, unavailable, or harmful. The common cases are **non-macOS servers, Docker bridge networking, WSL, or a network policy that drops mDNS multicast**. In those environments the Gateway is still reachable through its published URL, SSH, Tailnet, or wide-area DNS-SD, but LAN auto-discovery is not reliable.

Prefer the existing **environment override** when the problem is deployment-scoped, because the setting disappears when the environment does (safe for Docker images, service files, launch scripts, and one-off debugging):

```bash
OPENCLAW_DISABLE_BONJOUR=1
```

Use **plugin configuration** when you intentionally want to turn off the bundled LAN discovery plugin for that OpenClaw config:

```bash
openclaw plugins disable bonjour
```

## Enabling / disabling / configuration

The complete set of enable/disable/configuration knobs:

- macOS hosts auto-start the bundled LAN discovery plugin by default.
- `openclaw plugins enable bonjour` enables the bundled LAN discovery plugin on hosts where it is not default-enabled.
- `openclaw plugins disable bonjour` disables LAN multicast advertising by disabling the bundled plugin.
- `OPENCLAW_DISABLE_BONJOUR=1` disables LAN multicast advertising without changing plugin config; accepted truthy values are `1`, `true`, `yes`, and `on` (legacy: `OPENCLAW_DISABLE_BONJOUR`).
- `OPENCLAW_DISABLE_BONJOUR=0` forces LAN multicast advertising on, including inside detected containers; accepted falsy values are `0`, `false`, `no`, and `off`.
- When the Bonjour plugin is enabled and `OPENCLAW_DISABLE_BONJOUR` is unset, Bonjour advertises on normal hosts and auto-disables inside detected containers.
- `gateway.bind` in `~/.openclaw/openclaw.json` controls the Gateway bind mode.
- `OPENCLAW_SSH_PORT` overrides the SSH port when `sshPort` is advertised (legacy: `OPENCLAW_SSH_PORT`).
- `OPENCLAW_TAILNET_DNS` publishes a MagicDNS hint in TXT when mDNS full mode is enabled (legacy: `OPENCLAW_TAILNET_DNS`).
- `OPENCLAW_CLI_PATH` overrides the advertised CLI path (legacy: `OPENCLAW_CLI_PATH`).

**Source**: OpenClaw documentation — `gateway/bonjour` (mirror `inbox/openclaw_docs/gateway/bonjour.md`)
**Last Updated**: 2026-06-22
**Status**: Active
