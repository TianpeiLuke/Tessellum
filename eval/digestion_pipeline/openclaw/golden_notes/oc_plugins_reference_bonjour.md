---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - bonjour
keywords:
  - openclaw bonjour plugin
  - bonjour mdns gateway advertisement
  - "@openclaw/bonjour"
  - included in openclaw
  - plain plugin surface
  - lan gateway auto-discovery
  - zero-config service discovery
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/reference/bonjour
access_control_group: ["general"]
---

# OpenClaw — Bonjour Plugin Reference

## Overview

This note is the reference card for the OpenClaw **bonjour** plugin, mirroring the `plugins/reference/bonjour` source page. The plugin's single stated purpose is to "Advertise the local OpenClaw gateway over Bonjour/mDNS" so that clients on the same LAN can auto-discover the gateway with zero configuration. As a concept-level plugin-identity card it captures the three load-bearing facts the source page records — the distribution package, the install route, and the runtime *surface* the plugin registers — without redefining Bonjour/mDNS itself (linked) or duplicating the gateway-side discovery configuration (a separate `gw*`-series doc, linked below).

## Distribution

The bonjour plugin's distribution facts, copied verbatim from the source page's `## Distribution` section:

- **Package**: `@openclaw/bonjour`
- **Install route**: included in OpenClaw

Because it is *included in OpenClaw*, the plugin ships with the gateway distribution rather than being fetched separately from npm or ClawHub — no install command is documented on the source page. Any further install/enable detail beyond "included in OpenClaw" is **not specified in source**.

## Surface

The source page's `## Surface` section consists of the single token `plugin`. This is the simplest plugin surface form in OpenClaw's plugin model: bonjour registers as a plain `plugin` (not a model `providers:` name and not a `contracts:` capability such as `speechProviders` or `webSearchProviders`). A plain `plugin` surface participates in plugin lifecycle (start/stop) rather than contributing a named provider or contract to a runtime registry; here that lifecycle work is publishing — and withdrawing — the local gateway's Bonjour/mDNS advertisement so LAN clients can find it. The source page documents no configuration keys, options, or environment variables for this plugin; any such settings are **not specified in source**.

**Source**: OpenClaw documentation — `plugins/reference/bonjour` (mirror `inbox/openclaw_docs/plugins/reference/bonjour.md`)
**Last Updated**: 2026-06-22
**Status**: Active
