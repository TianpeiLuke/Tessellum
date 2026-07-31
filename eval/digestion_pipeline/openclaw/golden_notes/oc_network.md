---
tags:
  - resource
  - documentation
  - openclaw
  - top_level
  - network
keywords:
  - openclaw network architecture
  - gateway loopback first bind
  - ws control plane 127.0.0.1:18789
  - pairing and identity local trust
  - tailnet lan pairing approval
  - discovery transports bonjour mdns
  - nodes as peripherals
  - trusted-proxy non-loopback
topics:
  - OpenClaw
  - Network Architecture
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/network
access_control_group: ["general"]
---

# OpenClaw — Network Architecture and Security Hub

## Overview

This note captures the OpenClaw **network** hub — the conceptual model of how OpenClaw connects, pairs, and secures devices across localhost, LAN, and tailnet. It mirrors the `network` source page, a navigation/architecture hub that links the core networking docs and summarizes the loopback-first Gateway core model, the pairing + identity (local-trust) posture, discovery + transports, nodes-as-peripherals, and the security surface. The page itself is a hub: it states the architectural principles and then points to the deeper `/gateway/*`, `/channels/*`, `/concepts/*`, `/platforms/*`, and `/web` docs that own the operational detail.

## Core Model

Most operations flow through the **Gateway** (`openclaw gateway`), a single long-running process that owns channel connections and the WebSocket control plane. The hub states four core architectural facts:

- **Loopback first**: the Gateway WS defaults to `ws://127.0.0.1:18789`. Non-loopback binds require a valid gateway auth path — shared-secret token/password auth, or a correctly configured non-loopback `trusted-proxy` deployment.
- **One Gateway per host** is recommended. For isolation, run multiple gateways with isolated profiles and ports (link-out: Multiple Gateways, `/gateway/multiple-gateways`).
- **Canvas host** is served on the same port as the Gateway (`/__openclaw__/canvas/`, `/__openclaw__/a2ui/`), protected by Gateway auth when bound beyond loopback.
- **Remote access** is typically SSH tunnel or Tailscale VPN (link-out: Remote Access, `/gateway/remote`).

The hub provides a set of key references for the core model that are owned by other sub-plans/leaf pages: Gateway architecture (`/concepts/architecture`), Gateway protocol (`/gateway/protocol`), the Gateway runbook (`/gateway`), and Web surfaces + bind modes (`/web`). These are link-outs from this hub, not redefined here.

## Pairing + Identity

The hub points to the pairing and identity surface across DM and node pairing: Pairing overview (DM + nodes, `/channels/pairing`), Gateway-owned node pairing (`/gateway/pairing`), the Devices CLI (pairing + token rotation, `/cli/devices`), and the Pairing CLI (DM approvals, `/cli/pairing`).

It defines the **local trust** posture in three points:

- Direct local loopback connects can be **auto-approved** for pairing to keep same-host UX smooth.
- OpenClaw also has a narrow backend/container-local self-connect path for trusted shared-secret helper flows.
- **Tailnet and LAN clients, including same-host tailnet binds, still require explicit pairing approval** — local-trust auto-approve does not extend beyond direct loopback.

## Discovery + Transports

The hub lists the discovery and transport docs that own the connection/announcement mechanics: Discovery and transports (`/gateway/discovery`), Bonjour / mDNS (`/gateway/bonjour`), Remote access over SSH (`/gateway/remote`), and Tailscale (`/gateway/tailscale`). These are the canonical surfaces a client uses to find and reach a Gateway across loopback, LAN, and tailnet.

## Nodes + Transports

Nodes are treated as **peripherals** that attach to the Gateway. The hub links the node-side transport docs: the Nodes overview (`/nodes`), the Bridge protocol for legacy nodes (historical, `/gateway/bridge-protocol`), and the per-platform node runbooks — Node runbook: iOS (`/platforms/ios`) and Node runbook: Android (`/platforms/android`). The pairing/identity model from above applies to nodes as well as DM clients.

## Security

The security surface is summarized as a set of canonical references: Security overview (`/gateway/security`), the Gateway config reference (`/gateway/configuration`), Troubleshooting (`/gateway/troubleshooting`), and Doctor (`/gateway/doctor`). Together with the loopback-first bind default and the explicit-approval-beyond-loopback pairing posture, these define OpenClaw's network security boundary: auth required beyond loopback, explicit pairing approval for tailnet/LAN, and a single audited control plane per host.

**Source**: OpenClaw documentation — `network` (mirror `inbox/openclaw_docs/network.md`)
**Last Updated**: 2026-06-22
**Status**: Active
