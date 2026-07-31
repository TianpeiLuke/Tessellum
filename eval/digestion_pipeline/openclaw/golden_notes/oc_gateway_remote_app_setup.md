---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - remote_app
keywords:
  - openclaw.app remote gateway
  - ssh tunnel localforward 18789
  - gateway.remote.token config
  - launchagent ssh tunnel plist
  - keepalive runatload tunnel
  - ssh-copy-id remote auth
  - launchctl bootstrap kickstart bootout
topics:
  - OpenClaw
  - Remote Gateway Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/remote-gateway-readme
access_control_group: ["general"]
---

# OpenClaw — Running OpenClaw.app with a Remote Gateway (SSH-Tunnel Runbook)

## Overview

This note is the step-by-step runbook for pointing **OpenClaw.app** (the macOS app) at a remote Gateway over an **SSH tunnel**, mirroring the `gateway/remote-gateway-readme` source page. OpenClaw.app connects only to a local loopback port (`ws://127.0.0.1:18789`); an SSH tunnel forwards that local port to the same port on the remote machine where the Gateway WebSocket is running, so the app never needs the remote Gateway exposed on a public address. The runbook covers the five quick-setup steps (SSH config, copy key, remote-auth config, start tunnel, restart the app), auto-starting the tunnel on login via a launchd LaunchAgent PLIST, troubleshooting commands, and a "how it works" mapping. The source page carries a banner noting it has been **merged into** the [Remote Access](https://docs.openclaw.ai/gateway/remote#macos-persistent-ssh-tunnel-via-launchagent) page, which is now the current guide.

## Quick setup

The end-to-end flow forwards local port `18789` to the remote Gateway, configures durable remote-client auth, starts the tunnel, and restarts the app so it picks up the forwarded connection.

### Step 1: Add SSH Config

Edit `~/.ssh/config` and add a `Host` block whose `LocalForward` forwards the local Gateway port to the remote loopback Gateway port:

```ssh
Host remote-gateway
    HostName <REMOTE_IP>          # e.g., 172.27.187.184
    User <REMOTE_USER>            # e.g., jefferson
    LocalForward 18789 127.0.0.1:18789
    IdentityFile ~/.ssh/id_rsa
```

Replace `<REMOTE_IP>` and `<REMOTE_USER>` with your values.

### Steps 2–5: Copy key, configure auth, start tunnel, restart app

Copy your public key to the remote machine (enter the password once), set the durable remote-client auth token, start the port-forward-only tunnel (`-N` runs SSH without executing remote commands), then quit (⌘Q) and reopen OpenClaw.app so it reconnects through the tunnel:

```bash
# Step 2: Copy SSH Key (enter password once)
ssh-copy-id -i ~/.ssh/id_rsa <REMOTE_USER>@<REMOTE_IP>

# Step 3: Configure Remote Gateway Auth
openclaw config set gateway.remote.token "<your-token>"

# Step 4: Start SSH Tunnel
ssh -N remote-gateway &

# Step 5: Quit OpenClaw.app (⌘Q), then reopen:
open /path/to/OpenClaw.app
```

For Step 3, use `gateway.remote.password` instead if your remote gateway uses password auth. `OPENCLAW_GATEWAY_TOKEN` is still valid as a shell-level override, but the durable remote-client setup is `gateway.remote.token` / `gateway.remote.password`. After Step 5 the app will connect to the remote gateway through the SSH tunnel.

## Auto-Start Tunnel on Login

To have the SSH tunnel start automatically when you log in, create a launchd **Launch Agent**. Save the following as `~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist`:

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

Load the Launch Agent:

```bash
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.ssh-tunnel.plist
```

The tunnel will now start automatically when you log in, restart if it crashes, and keep running in the background. **Legacy note**: remove any leftover `com.openclaw.ssh-tunnel` LaunchAgent if present.

## Troubleshooting

Check if the tunnel is running, then kick it (restart) or boot it out (stop) via `launchctl`:

```bash
# Check if tunnel is running:
ps aux | grep "ssh -N remote-gateway" | grep -v grep
lsof -i :18789

# Restart the tunnel:
launchctl kickstart -k gui/$UID/ai.openclaw.ssh-tunnel

# Stop the tunnel:
launchctl bootout gui/$UID/ai.openclaw.ssh-tunnel
```

## How it works

OpenClaw.app connects to `ws://127.0.0.1:18789` on your client machine. The SSH tunnel forwards that connection to port `18789` on the remote machine where the Gateway is running. The configuration components map to the following roles:

| Component | What It Does |
| --- | --- |
| `LocalForward 18789 127.0.0.1:18789` | Forwards local port 18789 to remote port 18789 |
| `ssh -N` | SSH without executing remote commands (just port forwarding) |
| `KeepAlive` | Automatically restarts tunnel if it crashes |
| `RunAtLoad` | Starts tunnel when the agent loads |

**Source**: OpenClaw documentation — `gateway/remote-gateway-readme` (mirror `inbox/openclaw_docs/gateway/remote-gateway-readme.md`)
**Last Updated**: 2026-06-22
**Status**: Active
