---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - remote
keywords:
  - openclaw remote gateway access
  - gateway loopback bind 18789
  - ssh tunnel localforward gateway
  - tailscale serve gateway
  - gateway remote credential precedence
  - gateway.remote.token transport direct
  - macos persistent ssh tunnel launchagent
  - remote vpn security rules wss
topics:
  - OpenClaw
  - Gateway Remote Access
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/remote
access_control_group: ["general"]
---

# OpenClaw — Remote Gateway Access (VPN, Tailnet, SSH Tunnel)

## Overview

This note is the procedure for accessing a single OpenClaw Gateway (the master) remotely while it runs on a dedicated host, mirroring the `gateway/remote` source page. The Gateway WebSocket normally binds to **loopback** on port `18789`, so remote use means exposing it through Tailscale Serve, a trusted LAN/tailnet bind, or an SSH-forwarded loopback port — then pointing operator and node clients at it. It covers the single-gateway core idea, the three VPN/tailnet deployment topologies, where commands actually run, the SSH tunnel for the CLI and tools, CLI remote defaults, the shared credential-precedence contract, chat-UI and macOS app remote modes, the remote/VPN security rules, and a persistent macOS SSH-tunnel LaunchAgent runbook.

## The Core Idea

OpenClaw runs **one Gateway (the master)** on a dedicated host (desktop or server) and connects clients to it; operators (you / the macOS app) use direct LAN/tailnet WebSocket when the gateway is reachable, with SSH tunneling as the universal fallback, and nodes (iOS/Android and future devices) connect to the Gateway **WebSocket** over LAN/tailnet or an SSH tunnel as needed. The Gateway WebSocket usually binds to **loopback** on your configured port (defaults to `18789`). For remote use, expose it through Tailscale Serve or a trusted LAN/Tailnet bind, or forward the loopback port over SSH.

## Common VPN and Tailnet Setups

Treat the **Gateway host** as where the agent lives — it owns sessions, auth profiles, channels, and state — and your laptop, desktop, and nodes connect to that host. There are three deployment topologies.

**Always-on Gateway in your tailnet** — run the Gateway on a persistent host (VPS or home server) and reach it via Tailscale or SSH. Best UX is to keep `gateway.bind: "loopback"` and use **Tailscale Serve** for the Control UI; a trusted LAN/Tailnet option binds the gateway to a private interface and connects directly with `gateway.remote.transport: "direct"`; the fallback keeps loopback plus an SSH tunnel from any machine that needs access. Examples are exe.dev (easy VM) or Hetzner (production VPS). This is ideal when your laptop sleeps often but you want the agent always-on.

**Home desktop runs the Gateway** — the laptop does **not** run the agent; it connects remotely via the macOS app's remote mode (Settings → General → OpenClaw runs). The app connects directly when the gateway is reachable on LAN/Tailnet, or opens and manages an SSH tunnel when you choose SSH.

**Laptop runs the Gateway** — keep the Gateway local but expose it safely by either SSH-tunneling to the laptop from other machines, or Tailscale-Serving the Control UI while keeping the Gateway loopback-only.

## Command Flow (What Runs Where)

One gateway service owns state and channels; nodes are peripherals. In the Telegram → node flow example: a Telegram message arrives at the **Gateway**; the Gateway runs the **agent** and decides whether to call a node tool; the Gateway calls the **node** over the Gateway WebSocket (`node.*` RPC); the node returns the result and the Gateway replies back out to Telegram. **Nodes do not run the gateway service** — only one gateway should run per host unless you intentionally run isolated profiles (see Multiple gateways), and the macOS app "node mode" is just a node client over the Gateway WebSocket.

## SSH Tunnel (CLI + Tools)

Create a local tunnel to the remote Gateway WS:

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

With the tunnel up, `openclaw health` and `openclaw status --deep` now reach the remote gateway via `ws://127.0.0.1:18789`, and `openclaw gateway status`, `openclaw gateway health`, `openclaw gateway probe`, and `openclaw gateway call` can also target the forwarded URL via `--url` when needed. Replace `18789` with your configured `gateway.port` (or `--port` or `OPENCLAW_GATEWAY_PORT`). When you pass `--url`, the CLI does **not** fall back to config or environment credentials — include `--token` or `--password` explicitly, since missing explicit credentials is an error.

## CLI Remote Defaults

You can persist a remote target so CLI commands use it by default. When the gateway is loopback-only, keep the URL at `ws://127.0.0.1:18789` and open the SSH tunnel first:

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      url: "ws://127.0.0.1:18789",
      token: "your-token",
    },
  },
}
```

In the macOS app's SSH tunnel transport, discovered gateway hostnames belong in `gateway.remote.sshTarget`; `gateway.remote.url` remains the local tunnel URL. If those ports differ, set `gateway.remote.remotePort` to the gateway port on the SSH host. For a gateway already reachable on a trusted LAN or Tailnet, use direct mode:

```json5
{
  gateway: {
    mode: "remote",
    remote: {
      transport: "direct",
      url: "ws://192.168.0.202:18789",
      token: "your-token",
    },
  },
}
```

## Credential Precedence

Gateway credential resolution follows one shared contract across call/probe/status paths and Discord exec-approval monitoring; node-host uses the same base contract with one local-mode exception (it intentionally ignores `gateway.remote.*`). Explicit credentials (`--token`, `--password`, or tool `gatewayToken`) always win on call paths that accept explicit auth. For URL-override safety, CLI URL overrides (`--url`) never reuse implicit config/env credentials, while env URL overrides (`OPENCLAW_GATEWAY_URL`) may use env credentials only (`OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`).

The mode-specific defaults are:

- **Local mode** — token: `OPENCLAW_GATEWAY_TOKEN` -> `gateway.auth.token` -> `gateway.remote.token` (remote fallback applies only when local auth token input is unset); password: `OPENCLAW_GATEWAY_PASSWORD` -> `gateway.auth.password` -> `gateway.remote.password` (remote fallback applies only when local auth password input is unset).
- **Remote mode** — token: `gateway.remote.token` -> `OPENCLAW_GATEWAY_TOKEN` -> `gateway.auth.token`; password: `OPENCLAW_GATEWAY_PASSWORD` -> `gateway.remote.password` -> `gateway.auth.password`.
- **Node-host local-mode exception** — `gateway.remote.token` / `gateway.remote.password` are ignored.
- **Remote probe/status token checks** are strict by default: they use `gateway.remote.token` only (no local token fallback) when targeting remote mode.
- **Gateway env overrides** use `OPENCLAW_GATEWAY_*` only.

## Chat UI Remote Access

WebChat no longer uses a separate HTTP port; the SwiftUI chat UI connects directly to the Gateway WebSocket. Forward `18789` over SSH (see above), then connect clients to `ws://127.0.0.1:18789`; for LAN/Tailnet direct mode, connect clients to the configured private `ws://` or secure `wss://` URL. On macOS, prefer the app's remote mode, which manages the selected transport automatically.

## macOS App Remote Mode

The macOS menu bar app can drive the same setup end-to-end (remote status checks, WebChat, and Voice Wake forwarding). See the macOS remote access runbook for the app-specific steps.

## Security Rules (Remote/VPN)

The short version is **keep the Gateway loopback-only** unless you're sure you need a bind. Loopback + SSH/Tailscale Serve is the safest default (no public exposure). Plaintext `ws://` is accepted for loopback, LAN, link-local, `.local`, `.ts.net`, and Tailscale CGNAT hosts; **public remote hosts must use `wss://`**. **Non-loopback binds** (`lan`/`tailnet`/`custom`, or `auto` when loopback is unavailable) must use gateway auth: token, password, or an identity-aware reverse proxy with `gateway.auth.mode: "trusted-proxy"`.

The remaining rules govern client credentials, TLS pinning, and proxy trust:

- `gateway.remote.token` / `.password` are **client** credential sources — they do **not** configure server auth by themselves.
- Local call paths can use `gateway.remote.*` as fallback only when `gateway.auth.*` is unset.
- If `gateway.auth.token` / `gateway.auth.password` is explicitly configured via SecretRef and unresolved, resolution fails closed (no remote fallback masking).
- `gateway.remote.tlsFingerprint` pins the remote TLS cert when using `wss://`, including macOS direct mode. Without a configured or previously stored pin, macOS only pins a first-use certificate after normal system trust passes; self-signed or private-CA gateways that macOS does not already trust need an explicit fingerprint or Remote over SSH.
- **Tailscale Serve** can authenticate Control UI/WebSocket traffic via identity headers when `gateway.auth.allowTailscale: true`; HTTP API endpoints do not use that Tailscale header auth and instead follow the gateway's normal HTTP auth mode. This tokenless flow assumes the gateway host is trusted; set it to `false` if you want shared-secret auth everywhere.
- **Trusted-proxy** auth expects non-loopback identity-aware proxy setups by default; same-host loopback reverse proxies require explicit `gateway.auth.trustedProxy.allowLoopback = true`.
- Treat browser control like operator access: tailnet-only + deliberate node pairing.

### macOS: Persistent SSH Tunnel via LaunchAgent

For macOS clients connecting to a remote gateway, the easiest persistent setup uses an SSH `LocalForward` config entry plus a LaunchAgent to keep the tunnel alive across reboots and crashes.

**Step 1 — add SSH config.** Edit `~/.ssh/config`, replacing `<REMOTE_IP>` and `<REMOTE_USER>` with your values:

```ssh
Host remote-gateway
    HostName <REMOTE_IP>
    User <REMOTE_USER>
    LocalForward 18789 127.0.0.1:18789
    IdentityFile ~/.ssh/id_rsa
```

**Step 2 — copy SSH key (one-time):** `ssh-copy-id -i ~/.ssh/id_rsa <REMOTE_USER>@<REMOTE_IP>`.

**Step 3 — configure the gateway token** so it persists across restarts: `openclaw config set gateway.remote.token "<your-token>"`.

**Step 4 — create the LaunchAgent.** Save this as `~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.ssh-tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/ssh</string>
        <string>-N</string>
        <string>remote-gateway</string>
    </array>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

**Step 5 — load the LaunchAgent:** `launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist`. The tunnel then starts automatically at login, restarts on crash, and keeps the forwarded port live. If you have a leftover `com.openclaw.ssh-tunnel` LaunchAgent from an older setup, unload and delete it.

**Troubleshooting.** Check if the tunnel is running with `ps aux | grep "ssh -N remote-gateway" | grep -v grep` and `lsof -i :18789`; restart it with `launchctl kickstart -k gui/$UID/ai.openclaw.ssh-tunnel`; stop it with `launchctl bootout gui/$UID/ai.openclaw.ssh-tunnel`.

The four config entries and their effects:

| Config entry                         | What it does                                                 |
| ------------------------------------ | ------------------------------------------------------------ |
| `LocalForward 18789 127.0.0.1:18789` | Forwards local port 18789 to remote port 18789               |
| `ssh -N`                             | SSH without executing remote commands (port-forwarding only) |
| `KeepAlive`                          | Automatically restarts the tunnel if it crashes              |
| `RunAtLoad`                          | Starts the tunnel when the LaunchAgent loads at login        |

**Source**: OpenClaw documentation — `gateway/remote` (mirror `inbox/openclaw_docs/gateway/remote.md`)
**Last Updated**: 2026-06-22
**Status**: Active
