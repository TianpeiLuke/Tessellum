---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - peekaboo
keywords:
  - openclaw peekaboo bridge
  - peekaboobridge host macos
  - peekaboo cli ui automation
  - cua-driver mcp computer use
  - codex computer-use mcp
  - teamid allowlist code signature
  - peekaboo_bridge_socket
  - client discovery order
  - tcc permission aware broker
topics:
  - OpenClaw
  - macOS UI Automation
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/platforms/mac/peekaboo
access_control_group: ["general"]
---

# OpenClaw — PeekabooBridge Host for macOS UI Automation

## Overview

This note explains the concept of **PeekabooBridge** as hosted by OpenClaw.app: a local, permission-aware UI-automation broker on macOS that lets the `peekaboo` CLI drive UI automation while reusing the macOS app's TCC permissions. It mirrors the `platforms/mac/peekaboo` source page — covering what the broker is and is not, how it relates to the three distinct desktop-control paths (PeekabooBridge host vs Codex Computer Use vs direct `cua-driver` MCP), how to enable the local UNIX socket, the client discovery order, the code-signature / TeamID-allowlist security posture, snapshot behavior, and troubleshooting. The "Enable the bridge" steps appear as a short inline sub-procedure inside this concept frame; the dominant building block is the conceptual model of the broker and the choice between the three control paths.

## What this is (and is not)

OpenClaw can host **PeekabooBridge** as a local, permission-aware UI-automation broker, which lets the `peekaboo` CLI drive UI automation while reusing the macOS app's TCC permissions. The roles are split three ways:

- **Host**: OpenClaw.app can act as a PeekabooBridge host.
- **Client**: use the `peekaboo` CLI (there is no separate `openclaw ui ...` surface).
- **UI**: visual overlays stay in Peekaboo.app; OpenClaw is a thin broker host.

The key concept is that OpenClaw does not own the automation UX — Peekaboo.app keeps the visual overlays, and OpenClaw contributes only the permission-aware bridge host so the `peekaboo` client can reuse the app's macOS permissions.

## Relationship to Computer Use

OpenClaw has three desktop-control paths, and they intentionally stay separate:

- **PeekabooBridge host**: OpenClaw.app can host the local PeekabooBridge socket. The `peekaboo` CLI remains the client and uses OpenClaw.app's macOS permissions for Peekaboo automation primitives such as screenshots, clicks, menus, dialogs, Dock actions, and window management.
- **Codex Computer Use**: the bundled `codex` plugin prepares Codex app-server, verifies that Codex's `computer-use` MCP server is available, and then lets Codex own native desktop-control tool calls during Codex-mode turns. OpenClaw does not proxy those actions through PeekabooBridge.
- **Direct `cua-driver` MCP**: OpenClaw can register TryCua's upstream `cua-driver mcp` server as a normal MCP server. That gives agents the CUA driver's own schemas and pid/window/element-index workflow without routing through the Codex marketplace or the PeekabooBridge socket.

The page frames the decision as: use Peekaboo when you want the broad macOS automation surface and OpenClaw.app's permission-aware bridge host; use Codex Computer Use when a Codex-mode agent should rely on Codex's native computer-use plugin; use direct `cua-driver mcp` when you want the CUA driver exposed to any OpenClaw-managed runtime as a normal MCP server.

## Enable the bridge

In the macOS app, the bridge is enabled from the settings UI:

- Settings → **Enable Peekaboo Bridge**

When enabled, OpenClaw starts a local UNIX socket server. If disabled, the host is stopped and `peekaboo` will fall back to other available hosts.

## Client discovery order

Peekaboo clients typically try hosts in this order:

1. Peekaboo.app (full UX)
2. Claude.app (if installed)
3. OpenClaw.app (thin broker)

Use `peekaboo bridge status --verbose` to see which host is active and which socket path is in use. You can override the socket path with the `PEEKABOO_BRIDGE_SOCKET` environment variable:

```bash
export PEEKABOO_BRIDGE_SOCKET=/path/to/bridge.sock
```

## Security and permissions

The broker is permission-aware and enforces caller identity rather than granting raw GUI access:

- The bridge validates **caller code signatures**; an allowlist of TeamIDs is enforced (the Peekaboo host TeamID plus the OpenClaw app TeamID).
- Prefer the signed bridge/app identity over a generic `node` runtime for Accessibility. Granting Accessibility to `node` lets any package launched by that Node executable inherit GUI automation access (see the macOS permissions page's Accessibility-grants-for-Node-and-CLI-runtimes section).
- Requests time out after ~10 seconds.
- If required permissions are missing, the bridge returns a clear error message rather than launching System Settings.

## Snapshot behavior (automation)

Snapshots are stored in memory and expire automatically after a short window. If you need longer retention, re-capture from the client.

## Troubleshooting

- If `peekaboo` reports "bridge client is not authorized", ensure the client is properly signed, or run the host with `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` in **debug** mode only.
- If no hosts are found, open one of the host apps (Peekaboo.app or OpenClaw.app) and confirm permissions are granted.

**Source**: OpenClaw documentation — `platforms/mac/peekaboo` (mirror `inbox/openclaw_docs/platforms/mac/peekaboo.md`)
**Last Updated**: 2026-06-22
**Status**: Active
