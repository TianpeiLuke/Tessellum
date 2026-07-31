---
tags:
  - resource
  - terminology
  - bonjour
  - mdns
  - zero-config-networking
  - dns-sd
  - openclaw
keywords:
  - Bonjour
  - mDNS
  - Multicast DNS
  - DNS-SD
  - NWBrowser
  - NetService
  - NSD
  - Zeroconf
topics:
  - Network discovery
  - Local-first networking
  - OpenClaw mobile pairing
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://en.wikipedia.org/wiki/Bonjour_(software)
access_control_group: ["general"]
---

# Bonjour / mDNS Discovery

## Definition

**Bonjour** is Apple's marketing name (originally "Rendezvous") for its implementation of **Zeroconf** — a trio of zero-configuration networking technologies that lets devices on a local link find each other, resolve names, and discover services without a configured DNS server, DHCP-distributed service catalog, or operator intervention. The underlying protocols are two IETF Standards-Track RFCs published in 2013: **RFC 6762 (Multicast DNS)**, which carries DNS-style queries and responses over IP multicast on the local link, and **RFC 6763 (DNS-Based Service Discovery, DNS-SD)**, which specifies how DNS resource records are named so clients can browse for service *instances* of a given type. Together with link-local IP autoconfiguration (RFC 3927 / RFC 7404), they form the Zeroconf stack; Bonjour, Linux Avahi, Windows 10+ built-in mDNS, and Android NSD are interoperable peers speaking the same wire protocol.

The conceptual split that the name "Bonjour" hides is important: **mDNS is the transport** (UDP multicast on `224.0.0.251` / `FF02::FB` port 5353, queries and answers in standard DNS-record format, scoped to the `.local.` top-level domain), while **DNS-SD is the naming convention** (services advertised under PTR records pointing to instance names, with SRV records giving host+port and TXT records carrying free-form metadata). A Bonjour-using application speaks both layers: it issues an mDNS multicast PTR query for a service type like `_openclaw-gateway._tcp.local.`, receives PTR answers naming instances, then resolves each instance via SRV + A/AAAA + TXT.

## Context

Every major mobile and desktop OS ships an mDNS responder. On Apple platforms (iOS, macOS, tvOS), the modern API is **`NWBrowser`** in the Network framework — `NWBrowser.Descriptor.bonjour(type:domain:)` returns a typed descriptor that, when wrapped in `NWBrowser`, surfaces discovered endpoints with their TXT records pre-decoded; the legacy `NetService` / `NetServiceBrowser` Foundation API is still used when SRV+A/AAAA resolution must run on a Foundation `RunLoop`. On Android, **`NsdManager`** exposes equivalent functionality, with API 34 (UPSIDE_DOWN_CAKE) introducing `registerServiceInfoCallback` and deprecating the old `resolveService` path. Linux distributions ship **Avahi** (LGPL) as the default responder; Java apps use **JmDNS**; cross-language libraries include `mdnsjava`, `homebridge/ciao`, and `grandcat/zeroconf`. Common Bonjour-discovered service types in the wild include AirPlay (`_airplay._tcp`), printers (`_ipp._tcp`), file shares (`_smb._tcp`), SSH (`_ssh._tcp`), and increasingly IoT control planes and developer tools.

[OpenClaw](term_openclaw.md) uses Bonjour/mDNS for **local-first gateway pairing**: a node's gateway (which hosts the user's local agent runtime) advertises itself under a service type like `_openclaw-gw._tcp.local.` on every reachable interface, and the iOS or Android companion app's discovery layer browses for that type so the user never has to enter a manual IP address. The iOS pairing path spins up parallel `NWBrowser` instances per service domain — one for `local`, one per attached tailnet — and decodes TXT keys (`displayName`, `lanHost`, `gatewayPort`, `gatewayTls`, `gatewayTlsSha256`) into snapshots; resolution is delegated to a `NetService`-based `GatewayServiceResolver` whose `didFinish` latch collapses success / failure / timeout into a single one-shot callback. The Android counterpart runs `NsdManager` discovery against the link-local domain concurrently with a 5-second-cadence unicast DNS-SD loop against a wide-area zone (using `dnsjava` PTR/SRV/TXT chase) and merges both producers into a single `StateFlow<List<GatewayEndpoint>>` for the UI. In both clients, TXT-record metadata is treated as a cosmetic *hint only* — the security-load-bearing host+port comes from SRV + A/AAAA, never TXT — because mDNS responses are unauthenticated and any host on the link can spoof a TXT record.

## Key Characteristics

- **Transport**: UDP multicast on `224.0.0.251` (IPv4) / `FF02::FB` (IPv6), port `5353`; same DNS message format as unicast DNS so wire decoders are reusable.
- **Link-local scope**: the `.local.` pseudo-TLD is reserved (RFC 6762 §3); responses outside the local link are invalid, which makes mDNS unroutable across L3 segments by design (Bonjour Gateway / Avahi reflector are the bridging workarounds).
- **Resource record types used**: `A` / `AAAA` for IPv4 / IPv6 host resolution, `SRV` for host+port of a service instance, `PTR` for browsing all instances of a service type, `TXT` for instance metadata key-value pairs, `NSEC` for negative responses.
- **DNS-SD naming convention (RFC 6763)**: a service type is `_<service>._<proto>` (e.g., `_http._tcp`); browsing means querying `PTR <service-type>.<domain>`; each PTR answer points to an instance label that resolves via SRV+TXT.
- **Conflict-resolution probing**: a host claiming a name first multicasts a probe query and only announces if no response arrives — this is how name collisions on the link are avoided without coordination.
- **TXT records are cosmetic / unauthenticated**: any device on the link can respond; production clients must treat TXT as a UI hint and route via SRV+A/AAAA plus an out-of-band trust artifact (e.g., a pinned TLS fingerprint, as in OpenClaw's iOS pairing flow).
- **Cross-implementation interop**: Bonjour (Apple, Apache 2.0 `mDNSResponder`), Avahi (Linux, LGPL), Windows 10+ built-in, Android `NsdManager`, Java JmDNS, Go `grandcat/zeroconf`, TypeScript `homebridge/ciao` are all wire-compatible because they implement RFC 6762 + RFC 6763.
- **Parallel browsing across domains**: clients with multiple service domains (link-local `local.` plus zero or more wide-area DNS-SD zones for tailnets) typically run one browser per domain and merge results — pattern documented in the OpenClaw iOS pairing snippet.
- **Resolution as a separate step from browsing**: `NWBrowser` / `NetServiceBrowser` / `NsdManager.discoverServices` deliver instance *labels*; converting a label into a usable `(host, port)` requires a second resolve call (Foundation `NetService.resolve`, `NsdManager.resolveService` / `registerServiceInfoCallback`, or a manual SRV+A/AAAA chase).

## Related Terms


## Related Code Snippets

- **[OpenClaw iOS Gateway Pairing](../code_snippets/snippet_openclaw_ios_gateway_pairing.md)**: parallel `NWBrowser` per service domain decoding TXT into `DiscoveredGateway` snapshots, plus a Foundation `NetService` resolver with a finalize-once latch — the canonical iOS-side example of Bonjour discovery feeding a TOFU TLS-pin pairing flow.
- **[OpenClaw Android Gateway Session — mDNS + DNS-SD](../code_snippets/snippet_openclaw_android_gateway_session_mdns.md)**: concurrent `NsdManager` mDNS (with API-tiered modern callback + legacy reflection branches) and 5-second-cadence unicast DNS-SD via `dnsjava`, merged into a single `StateFlow<List<GatewayEndpoint>>`.

## References

- [Bonjour (software) — Wikipedia](https://en.wikipedia.org/wiki/Bonjour_(software))
- [Multicast DNS — Wikipedia](https://en.wikipedia.org/wiki/Multicast_DNS)
- [Zero-configuration networking — Wikipedia](https://en.wikipedia.org/wiki/Zero-configuration_networking)
- [RFC 6762 — Multicast DNS (IETF Datatracker)](https://datatracker.ietf.org/doc/html/rfc6762)
- [RFC 6763 — DNS-Based Service Discovery (IETF Datatracker)](https://datatracker.ietf.org/doc/html/rfc6763)
- [Bonjour — Apple Developer Documentation](https://developer.apple.com/documentation/foundation/bonjour)
- [Use network service discovery (NsdManager) — Android Developers](https://developer.android.com/develop/connectivity/wifi/use-nsd)
- [multicastdns.org — Multicast DNS](https://multicastdns.org/)
- [Avahi (software) — Wikipedia](https://en.wikipedia.org/wiki/Avahi_(software))
