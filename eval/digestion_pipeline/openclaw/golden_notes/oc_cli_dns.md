---
tags:
  - resource
  - documentation
  - openclaw
  - cli
  - dns
keywords:
  - openclaw dns setup
  - wide-area discovery dns-sd
  - tailscale coredns
  - split dns nameserver
  - discovery.widearea.domain
  - homebrew coredns brew service
  - openclaw.json discovery config
  - dns setup --apply --domain
topics:
  - OpenClaw
  - CLI
  - Wide-Area Discovery
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/cli/dns
access_control_group: ["general"]
---

# OpenClaw — `openclaw dns` Wide-Area Discovery Setup

## Overview

This note documents the `openclaw dns` CLI command, which provides DNS helpers for wide-area discovery over Tailscale + CoreDNS. It mirrors the `cli/dns` source page and covers the single subcommand `dns setup`, which plans (or, with `--apply`, applies) CoreDNS configuration for unicast DNS-SD discovery. The command is currently focused on macOS + Homebrew CoreDNS. The procedure below covers the `--domain` and `--apply` options, what the planning output shows (resolved domain, zone file path, tailnet IPs, recommended `openclaw.json` discovery config, and Tailscale Split DNS values), and the macOS apply behavior.

## Setup

`openclaw dns` exposes DNS helpers for wide-area discovery (Tailscale + CoreDNS). Per the source, support is currently focused on **macOS + Homebrew CoreDNS**. The setup invocations are:

```bash
openclaw dns setup
openclaw dns setup --domain openclaw.internal
openclaw dns setup --apply
```

The first form plans the setup for the configured discovery domain; the second overrides the domain (here `openclaw.internal`); the third applies the configuration.

## `dns setup`

`dns setup` plans or applies CoreDNS setup for **unicast DNS-SD discovery**.

### Options

- `--domain <domain>` — wide-area discovery domain (for example `openclaw.internal`).
- `--apply` — install or update CoreDNS config and restart the service (requires sudo; macOS only).

### What it shows

When run as a planning helper, `dns setup` shows:

- resolved discovery domain
- zone file path
- current tailnet IPs
- recommended `openclaw.json` discovery config
- the Tailscale Split DNS nameserver/domain values to set

### Notes

- Without `--apply`, the command is a **planning helper only** and prints the recommended setup.
- If `--domain` is omitted, OpenClaw uses `discovery.wideArea.domain` from config.
- `--apply` currently supports **macOS only** and expects **Homebrew CoreDNS**.
- `--apply` bootstraps the zone file if needed, ensures the CoreDNS import stanza exists, and restarts the `coredns` brew service.

**Source**: OpenClaw documentation — `cli/dns` (mirror `inbox/openclaw_docs/cli/dns.md`)
**Last Updated**: 2026-06-22
**Status**: Active
