---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - discovery
keywords:
  - openclaw gateway discovery
  - bonjour dns-sd service beacon
  - direct ws vs ssh transport
  - tailnet magicdns discovery
  - gateway pairing and acls
  - transport selection client policy
  - _openclaw-gw._tcp beacon
  - tls pinning gatewaytlssha256
topics:
  - OpenClaw
  - Gateway Discovery
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/gateway/discovery
access_control_group: ["general"]
---

# OpenClaw — Gateway Discovery and Transports

## Overview

This note describes OpenClaw's **node-discovery and transport design**: how clients (the macOS menu bar app, iOS/Android nodes) find a long-running gateway and choose how to reach it, mirroring the `gateway/discovery` source page. The design separates two surface-similar problems — **operator remote control** (the macOS app controlling a gateway running elsewhere) and **node pairing** (mobile/future nodes finding a gateway and pairing securely) — and resolves both with one rule: keep all network discovery/advertising inside the **Node Gateway** (`openclaw gateway`), treating clients as consumers. It covers the discovery vocabulary, why both a direct WebSocket transport and an SSH fallback exist, the three discovery inputs (Bonjour/DNS-SD beacon, Tailnet, manual SSH), the client transport-selection policy, gateway-owned pairing and auth, and the responsibility split across components.

## Terms

OpenClaw's discovery design uses a small, precise vocabulary:

- **Gateway** — a single long-running gateway process that owns state (sessions, pairing, node registry) and runs channels. Most setups use one per host; isolated multi-gateway setups are possible.
- **Gateway WS (control plane)** — the WebSocket endpoint on `127.0.0.1:18789` by default; can be bound to LAN/tailnet via `gateway.bind`.
- **Direct WS transport** — a LAN/tailnet-facing Gateway WS endpoint (no SSH).
- **SSH transport (fallback)** — remote control by forwarding `127.0.0.1:18789` over SSH.
- **Legacy TCP bridge (removed)** — an older node transport; no longer advertised for discovery and no longer part of current builds.

Protocol details for the live transport and the removed bridge are documented on separate pages (`/gateway/protocol` and `/gateway/bridge-protocol`).

## Why we keep both direct and SSH

OpenClaw deliberately keeps two transports because each wins in a different setting. **Direct WS** is the best UX on the same network and within a tailnet: it supports auto-discovery on LAN via Bonjour, pairing tokens plus ACLs owned by the gateway, and requires no shell access — so the protocol surface can stay tight and auditable. **SSH** remains the universal fallback: it works anywhere SSH access exists (even across unrelated networks), survives multicast/mDNS issues, and requires no new inbound ports besides SSH.

## Discovery inputs (how clients learn where the gateway is)

Clients learn the gateway's location through three inputs: a Bonjour/DNS-SD beacon, a tailnet hint, or a manual SSH target.

### Bonjour / DNS-SD discovery

Multicast Bonjour is best-effort and does not cross networks. OpenClaw can also browse the same gateway beacon via a configured **wide-area DNS-SD domain**, so discovery can cover `local.` on the same LAN plus a configured unicast DNS-SD domain for cross-network discovery. In terms of direction: the **gateway** advertises its WS endpoint via Bonjour when the bundled `bonjour` plugin is enabled (the plugin auto-starts on macOS hosts and is opt-in elsewhere), and **clients** browse and show a "pick a gateway" list, then store the chosen endpoint.

The service beacon advertises one service type, `_openclaw-gw._tcp` (the gateway transport beacon), with these non-secret TXT keys:

- `role=gateway`
- `transport=gateway`
- `displayName=<friendly name>` (operator-configured display name)
- `lanHost=<hostname>.local`
- `gatewayPort=18789` (Gateway WS + HTTP)
- `gatewayTls=1` (only when TLS is enabled)
- `gatewayTlsSha256=<sha256>` (only when TLS is enabled and fingerprint is available)
- `canvasPort=<port>` (canvas host port; currently the same as `gatewayPort` when the canvas host is enabled)
- `tailnetDns=<magicdns>` (optional hint; auto-detected when Tailscale is available)
- `sshPort=<port>` (mDNS full mode only; wide-area DNS-SD may omit it, in which case SSH defaults stay at `22`)
- `cliPath=<path>` (mDNS full mode only; wide-area DNS-SD still writes it as a remote-install hint)

The security model for these records is explicit: Bonjour/mDNS TXT records are **unauthenticated**, so clients must treat TXT values as UX hints only. Routing (host/port) should prefer the **resolved service endpoint** (SRV + A/AAAA) over TXT-provided `lanHost`, `tailnetDns`, or `gatewayPort`. TLS pinning must never allow an advertised `gatewayTlsSha256` to override a previously stored pin. iOS/Android nodes should require an explicit "trust this fingerprint" confirmation before storing a first-time pin (out-of-band verification) whenever the chosen route is secure/TLS-based.

Advertising is controlled by a set of commands and environment variables. `openclaw plugins enable bonjour` enables LAN multicast advertising, and `OPENCLAW_DISABLE_BONJOUR=1` disables advertising. When the Bonjour plugin is enabled and `OPENCLAW_DISABLE_BONJOUR` is unset, Bonjour advertises on normal hosts and auto-disables inside detected containers; empty-config macOS Gateway startup enables the plugin automatically, while Linux, Windows, and containerized deployments need explicit enablement (use `0` only on host, macvlan, or another mDNS-capable network, and `1` to force-disable). `gateway.bind` in `~/.openclaw/openclaw.json` controls the Gateway bind mode, `OPENCLAW_SSH_PORT` overrides the SSH port advertised when `sshPort` is emitted, `OPENCLAW_TAILNET_DNS` publishes a `tailnetDns` hint (MagicDNS), and `OPENCLAW_CLI_PATH` overrides the advertised CLI path.

### Tailnet (cross-network)

For cross-network (e.g. London/Vienna style) setups, Bonjour won't help, so the recommended "direct" target is a Tailscale MagicDNS name (preferred) or a stable tailnet IP. If the gateway can detect it is running under Tailscale, it publishes `tailnetDns` as an optional hint for clients (including wide-area beacons). The macOS app now prefers MagicDNS names over raw Tailscale IPs for gateway discovery, which improves reliability when tailnet IPs change (for example after node restarts or CGNAT reassignment) because MagicDNS names resolve to the current IP automatically.

For mobile node pairing, discovery hints do not relax transport security on tailnet/public routes: iOS/Android still require a secure first-time tailnet/public connect path (`wss://` or Tailscale Serve/Funnel); a discovered raw tailnet IP is a routing hint, not permission to use plaintext remote `ws://`; private LAN direct-connect `ws://` remains supported; and the simplest Tailscale path for mobile nodes is to use Tailscale Serve so discovery and the setup code both resolve to the same secure MagicDNS endpoint.

### Manual / SSH target

When there is no direct route (or direct is disabled), clients can always connect via SSH by forwarding the loopback gateway port.

## Transport selection (client policy)

The recommended client behavior is an ordered fallback chain:

1. If a paired direct endpoint is configured and reachable, use it.
2. Else, if discovery finds a gateway on `local.` or the configured wide-area domain, offer a one-tap "Use this gateway" choice and save it as the direct endpoint.
3. Else, if a tailnet DNS/IP is configured, try direct. For mobile nodes on tailnet/public routes, direct means a secure endpoint, not plaintext remote `ws://`.
4. Else, fall back to SSH.

## Pairing + auth (direct transport)

The gateway is the source of truth for node/client admission. Pairing requests are created, approved, or rejected in the gateway, and the gateway enforces auth (token / keypair), scopes/ACLs (the gateway is **not** a raw proxy to every method), and rate limits.

## Responsibilities by component

The discovery/transport responsibilities are split cleanly across three components: the **Gateway** advertises discovery beacons, owns pairing decisions, and hosts the WS endpoint; the **macOS app** helps you pick a gateway, shows pairing prompts, and uses SSH only as a fallback; and **iOS/Android nodes** browse Bonjour as a convenience and connect to the paired Gateway WS.

## Related Notes

**Terms**

- **[Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md)** — mDNS/DNS-SD service discovery; relevance: the primary discovery input (`_openclaw-gw._tcp` beacon, TXT keys).
- **[DNS](../../term_dictionary/term_dns.md)** — domain name system; relevance: wide-area DNS-SD + MagicDNS cross-network discovery.
- **[WebSocket](../../term_dictionary/term_websocket.md)** — full-duplex transport; relevance: the Gateway WS endpoint clients discover and connect to.
- **[TLS Pinning](../../term_dictionary/term_tls_pinning.md)** — fingerprint pinning; relevance: `gatewayTlsSha256` must never override a stored pin (security note).
- **[TLS](../../term_dictionary/term_tls.md)** — transport-layer security; relevance: secure first-time tailnet/public connect (`wss://`) requirement.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — the gateway product; relevance: the gateway advertising the discovery beacon.
- **[Authentication](../../term_dictionary/term_authentication.md)** — identity verification; relevance: pairing token/keypair auth on the direct transport.
- **[Access Control](../../term_dictionary/term_access_control.md)** — authorization policy; relevance: gateway-owned pairing scopes/ACLs (not a raw proxy).

**Docs**

- **[Claude Code — Remote Control](../claude_code/cc_remote_control.md)** — remote-gateway control; relevance: the operator-remote-control problem (mac app controlling a remote gateway).
- **[Claude Code — Network, TLS and Access](../claude_code/cc_network_tls_and_access.md)** — network/TLS access; relevance: the secure transport-selection + TLS-pinning policy.
- **[Hermes — OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md)** — SSH-forwarded auth; relevance: the SSH-transport fallback (forwarding loopback gateway port).
- **[Band — WebSocket Overview](../band/band_websocket_overview.md)** — WS transport design; relevance: the direct-WS transport clients discover.
- **[Band — A2A Gateway](../band/band_a2a_gateway.md)** — gateway discovery/transport; relevance: gateway-as-discovery-owner design analog.
- **[Hermes — Desktop Remote Backend](../hermes_agent/hermes_desktop_remote_backend.md)** — desktop→remote-gateway link; relevance: the macOS-app-picks-a-gateway transport-selection flow.
- **[oc_gateway_config_reference_platform](oc_gateway_config_reference_platform.md)** — Discovery mDNS/DNS-SD config fields (planned, this series); relevance: the config that drives this discovery design.
- **[oc_gateway_configuration_overview](oc_gateway_configuration_overview.md)** — `gateway.bind` config (planned, this series); relevance: the bind-mode config that controls beacon advertising.
- **[oc_gateway_doctor](oc_gateway_doctor.md)** — pairing/port diagnostics (planned, this series); relevance: doctor detects pairing trouble + gateway port collisions.
- **[oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md)** — auth/identity config (planned, this series); relevance: the auth/identity surface pairing relies on.

**Repos**

- **[repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md)** — gateway runtime; relevance: advertises beacons, owns pairing/auth, hosts the WS endpoint.
- **[repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md)** — apps; relevance: the macOS app that picks a gateway / shows pairing prompts.
- **[repo_openclaw](../../../areas/code_repos/repo_openclaw.md)** — monorepo; relevance: the `bonjour` bundled plugin + bind modes.

**Snippets**

- **[snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md)** — mDNS browse client; relevance: the client-side Bonjour/DNS-SD browse + "pick a gateway" flow.
- **[snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md)** — iOS pairing; relevance: the iOS/Android node pairing + first-time fingerprint trust.
- **[snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md)** — gateway pairing decisions; relevance: gateway as source of truth for node admission.
- **[snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md)** — method scopes/ACLs; relevance: the scopes/ACLs (not a raw proxy) the gateway enforces.
- **[snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md)** — client connect/SSH proxy; relevance: the SSH-transport fallback connect path.
- **[snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md)** — TLS pinning; relevance: pinning the discovered `gatewayTlsSha256` fingerprint.
- **[snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md)** — client TLS identity; relevance: secure direct-WS transport identity.
- **[snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md)** — node session; relevance: the paired Gateway-WS node session after discovery.
- **[snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md)** — gateway WS channel; relevance: the direct-WS endpoint discovery resolves to.
- **[snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md)** — WS session client; relevance: connecting to the discovered/paired Gateway WS.

## References

- [OpenClaw Docs — Discovery and transports](https://docs.openclaw.ai/gateway/discovery)
- [OpenClaw Docs — Gateway protocol](https://docs.openclaw.ai/gateway/protocol)
- [OpenClaw Docs — Bridge protocol (legacy)](https://docs.openclaw.ai/gateway/bridge-protocol)
- [OpenClaw Docs — Bonjour](https://docs.openclaw.ai/gateway/bonjour)
- [OpenClaw Docs — Remote access](https://docs.openclaw.ai/gateway/remote)
- [OpenClaw Docs — Tailscale](https://docs.openclaw.ai/gateway/tailscale)
- [OpenClaw Docs — Gateway pairing](https://docs.openclaw.ai/gateway/pairing)

**Source**: OpenClaw documentation — `gateway/discovery` (mirror `inbox/openclaw_docs/gateway/discovery.md`)
**Last Updated**: 2026-06-22
**Status**: Active
