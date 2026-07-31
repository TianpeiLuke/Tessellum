---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - gateway
keywords:
  - openclaw gateway port
  - gateway already running EADDRINUSE
  - GatewayLockError
  - gateway remote mode
  - nodes pairing gateway websocket
  - tailscale serve gateway
  - openclaw devices approve
  - invalid handshake code 1008
  - media attachments openclaw
topics:
  - OpenClaw
  - Gateway & Remote Mode
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/faq
access_control_group: ["general"]
---

# OpenClaw — FAQ: Gateway Ports, Remote Mode, Nodes, and Media

## Overview

This note answers the OpenClaw FAQ questions about reaching and running the Gateway across machines: the single multiplexed Gateway port and its precedence, resolving "already running" port conflicts (`GatewayLockError` / `EADDRINUSE`), running the Gateway in **remote mode** so a client connects to a Gateway elsewhere, pairing **nodes** (peripheral devices) to a remote Gateway over the Gateway WebSocket, the Tailscale Serve / SSH-tunnel access paths, and how outbound **media and attachments** are sent. It mirrors three H2 sections of the `help/faq` source page — "Remote gateways and nodes", "Gateway: ports, 'already running', and remote mode", and "Media and attachments" — and is the gateway/remote slice of the larger FAQ split. Deeper how-tos (full gateway protocol, Tailscale setup, security model) are linked out to their owning sub-plans and external docs rather than re-digested here.

## Gateway Port and Precedence

`gateway.port` controls the **single multiplexed port** used for both WebSocket and HTTP (the Control UI, hooks, etc.). The port resolution precedence, highest to lowest, is:

```
--port > OPENCLAW_GATEWAY_PORT > gateway.port > default 18789
```

The default Gateway listener binds at `ws://127.0.0.1:18789`.

## "Already Running" and Port Conflicts

OpenClaw enforces a runtime lock by binding the WebSocket listener immediately on startup (default `ws://127.0.0.1:18789`). If the bind fails with `EADDRINUSE`, it throws `GatewayLockError` indicating another instance is already listening. To fix the `"another gateway instance is already listening"` error, stop the other instance, free the port, or run with `openclaw gateway --port <port>`.

A related distinction is the difference between `openclaw gateway restart` and `openclaw gateway`: `openclaw gateway restart` restarts the **background service** (launchd/systemd), whereas `openclaw gateway` runs the gateway **in the foreground** for that terminal session. If the service is installed, use the gateway service commands; use `openclaw gateway` only for a one-off foreground run.

## Running Multiple Gateways on One Host

Usually you do **not** need multiple Gateways on one host — one Gateway can run multiple messaging channels and agents. Use multiple Gateways only for redundancy (e.g. a rescue bot) or hard isolation. If you do run more than one, you must isolate four things per instance:

- `OPENCLAW_CONFIG_PATH` (per-instance config)
- `OPENCLAW_STATE_DIR` (per-instance state)
- `agents.defaults.workspace` (workspace isolation)
- `gateway.port` (unique ports)

The recommended quick setup is to use `openclaw --profile <name> ...` per instance (which auto-creates `~/.openclaw-<name>`), set a unique `gateway.port` in each profile config (or pass `--port` for manual runs), and install a per-profile service with `openclaw --profile <name> gateway install`. Profiles also suffix service names (`ai.openclaw.<profile>`; legacy `com.openclaw.*`, `openclaw-gateway-<profile>.service`, `OpenClaw Gateway (<profile>)`). Note that a separate node host does **not** run a gateway service — only **one gateway** should run per host unless you intentionally run isolated profiles; a full restart is required for `gateway`, `discovery`, and hosted plugin surface changes.

## Remote Mode (Client Connects to a Gateway Elsewhere)

To run OpenClaw in remote mode, set `gateway.mode: "remote"` and point to a remote WebSocket URL, optionally with shared-secret remote credentials:

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://gateway.tailnet:18789",
      token: "your-token",
      password: "your-password",
    },
  },
}
```

Three behaviors are worth noting: `openclaw gateway` only starts when `gateway.mode` is `local` (or you pass the override flag); the macOS app watches the config file and switches modes live when these values change; and `gateway.remote.token` / `.password` are **client-side remote credentials only** — they do not enable local gateway auth by themselves.

## Nodes: Reaching Your Computer from a Remote Gateway

When the Gateway is hosted remotely, the way to let the agent reach your local machine is to **pair your computer as a node**. The Gateway runs elsewhere but can call `node.*` tools (screen, camera, system) on your local machine over the Gateway WebSocket. The typical setup is:

1. Run the Gateway on the always-on host (VPS/home server).
2. Put the Gateway host and your computer on the same tailnet.
3. Ensure the Gateway WS is reachable (tailnet bind or SSH tunnel).
4. Open the macOS app locally and connect in **Remote over SSH** mode (or direct tailnet) so it can register as a node.
5. Approve the node on the Gateway:

```bash
openclaw devices list
openclaw devices approve <requestId>
```

No separate TCP bridge is required; nodes connect over the Gateway WebSocket. The command propagation path for a node tool call is `Telegram → Gateway → Agent → node.* → Node → Gateway → Telegram` — nodes never see inbound provider traffic; they only receive node RPC calls. A security reminder applies: pairing a macOS node allows `system.run` on that machine, so only pair devices you trust.

Compared to SSH-from-a-VPS, nodes are the first-class way to reach a laptop from a remote Gateway and unlock more than shell access: no inbound SSH is required (nodes connect **out** to the Gateway WebSocket and use device pairing), `system.run` is gated by node allowlists/approvals on that laptop, nodes expose `canvas`, `camera`, and `screen` in addition to `system.run`, and local browser automation can run Chrome locally through a node host. If you only need local tools on a second machine, add it as a **node** rather than installing a second Gateway; install a second Gateway only when you need hard isolation or two fully separate bots. (Local node tools are currently macOS-only.)

## Tailscale Serve, SSH Tunnels, and "no replies" Triage

To reach a VPS Gateway from a Mac, install and log in to Tailscale on both ends, enable MagicDNS for a stable name, then use the tailnet hostname — SSH as `ssh user@your-vps.tailnet-xxxx.ts.net` or the Gateway WS as `ws://your-vps.tailnet-xxxx.ts.net:18789`. For the Control UI without SSH, use Tailscale Serve on the VPS with `openclaw gateway --tailscale serve`, which keeps the gateway bound to loopback and exposes HTTPS via Tailscale. To connect a Mac **node** to a remote Gateway over Tailscale Serve, put the VPS and Mac on the same tailnet, use the macOS app in Remote mode (SSH target can be the tailnet hostname) so it tunnels the Gateway port and connects as a node, then run `openclaw devices list` and `openclaw devices approve <requestId>`.

If Tailscale is connected but you get no replies, check the basics first — `openclaw gateway status`, `openclaw status`, and `openclaw channels status` — then verify auth and routing: if you use Tailscale Serve make sure `gateway.auth.allowTailscale` is set correctly, if you connect via SSH tunnel confirm the local tunnel is up and points at the right port, and confirm your allowlists (DM or group) include your account.

## Gateway Status Probe and Handshake Errors

`openclaw gateway status` can show `Runtime: running` but `Connectivity probe: failed` because "running" is the **supervisor's** view (launchd/systemd/schtasks) while the connectivity probe is the CLI actually connecting to the gateway WebSocket; trust the `Probe target:`, `Listening:`, and `Last gateway error:` lines. If `Config (cli)` and `Config (service)` differ, you are editing one config file while the service runs another (often a `--profile` / `OPENCLAW_STATE_DIR` mismatch); fix it by running `openclaw gateway install --force` from the same `--profile`/environment the service should use.

An `"invalid handshake" / code 1008` error means the Gateway (a WebSocket server) expected the very first message to be a `connect` frame and received something else, so it closed the connection with **code 1008** (policy violation). Common causes are opening the **HTTP** URL in a browser instead of a WS client, using the wrong port or path, or a proxy/tunnel stripping auth headers. Quick fixes: use the WS URL `ws://<host>:18789` (or `wss://...` if HTTPS), don't open the WS port in a normal browser tab, and if auth is on include the token/password in the `connect` frame. For the CLI or TUI the URL should look like `openclaw tui --url ws://<host>:18789 --token <token>`.

For a `gateway.bind: "tailnet"` that cannot bind, the `tailnet` bind picks a Tailscale IP from your interfaces (100.64.0.0/10); if the machine isn't on Tailscale (or the interface is down) there is nothing to bind to — start Tailscale on that host or switch to `gateway.bind: "loopback"` / `"lan"`. Note that `tailnet` is explicit while `auto` prefers loopback.

## Media and Attachments

Outbound attachments from the agent must use structured media fields such as `media`, `mediaUrl`, `path`, or `filePath`. CLI sending uses:

```bash
openclaw message send --target +15555550123 --message "Here you go" --media /path/to/file.png
```

If a skill generated an image/PDF but nothing was sent, also check: the target channel supports outbound media and isn't blocked by allowlists; the file is within the provider's size limits (images are resized to max 2048px); `tools.fs.workspaceOnly=true` keeps local-path sends limited to workspace, temp/media-store, and sandbox-validated files; and `tools.fs.workspaceOnly=false` lets structured local media sends use host-local files the agent can already read, but only for media plus safe document types (images, audio, video, PDF, Office docs, and validated text documents such as Markdown/MD, TXT, JSON, YAML, and YML). The source warns this is **not a secret scanner** — an agent-readable `secret.txt` or `config.json` can be attached when the extension and content validation match, so keep sensitive files outside agent-readable paths or keep `tools.fs.workspaceOnly=true` for stricter local-path sends.

**Source**: OpenClaw documentation — `help/faq` (mirror `inbox/openclaw_docs/help/faq.md`), sections "Remote gateways and nodes", "Gateway: ports, 'already running', and remote mode", "Media and attachments"
**Last Updated**: 2026-06-22
**Status**: Active
