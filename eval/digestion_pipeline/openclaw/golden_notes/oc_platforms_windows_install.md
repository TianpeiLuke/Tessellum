---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - install
keywords:
  - openclaw windows install
  - windows hub companion app
  - native windows cli gateway
  - wsl2 gateway openclaw
  - install.ps1 powershell installer
  - gateway auto-start scheduled tasks
  - wsl systemd linger dbus-launch
  - netsh portproxy wsl lan
topics:
  - OpenClaw
  - Windows Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/windows
access_control_group: ["general"]
---

# OpenClaw — Installing on Windows (Hub, Native CLI, WSL2)

## Overview

This note is the install/setup procedure for running OpenClaw on Windows, mirroring the first half of the `platforms/windows` source page (intro through "Expose WSL services over LAN"). It walks the three install paths — the signed **Windows Hub** WinUI companion app, the **native PowerShell CLI/Gateway** install, and a manual **WSL2 Gateway** — plus headless auto-start before Windows login and exposing a WSL-hosted Gateway over the LAN. The node-mode, local-MCP-mode, and troubleshooting half of the same page lives in the companion note **[oc_platforms_windows_node_modes](oc_platforms_windows_node_modes.md)**.

OpenClaw ships a native Windows Hub companion app plus Windows CLI support. Choose Windows Hub for a desktop app with setup, tray status, chat, Command Center diagnostics, and Windows node capabilities; the PowerShell installer when you want the CLI/Gateway directly; and WSL2 when you want the most Linux-compatible Gateway runtime.

## Recommended: Windows Hub

Windows Hub is the native WinUI companion app for **Windows 10 20H2+ and Windows 11**. It installs without administrator privileges and is published with signed **x64 and ARM64** installers on OpenClaw releases. Download the latest stable installer from the [OpenClaw releases page](https://github.com/openclaw/openclaw/releases): the assets are `OpenClawCompanion-Setup-x64.exe`, `OpenClawCompanion-Setup-arm64.exe`, and an `OpenClawCompanion-SHA256SUMS.txt` checksums file (the source links these at release tag `v2026.6.5`). If a download link returns a 404, visit the releases page and look for the `OpenClawCompanion-Setup-*` assets on the latest release.

After install, launch **OpenClaw Companion** from the Start menu or the system tray. The installer also adds shortcuts for Gateway Setup, Chat, Settings, Check for Updates, and uninstall.

### What Windows Hub includes

Per the source, a Windows Hub install bundles:

- system tray status and launch-at-login
- first-run setup for a local app-owned WSL Gateway
- connection settings for local, remote, and SSH-tunneled Gateways
- native chat window plus access to the browser Control UI
- Command Center diagnostics for sessions, usage, channels, nodes, pairing, and repair commands
- Windows node mode for agent-controlled canvas, screen, camera, notifications, device status, text-to-speech, speech-to-text, and controlled `system.run`
- local MCP server mode for MCP clients such as Claude Desktop, Claude Code, and Cursor

(The last two — node mode and local MCP mode — are operated/configured in the companion note **[oc_platforms_windows_node_modes](oc_platforms_windows_node_modes.md)**.)

### First launch

On first launch, Windows Hub opens setup when there is no usable saved Gateway. The fastest path is **Set up locally**, which provisions an app-owned `OpenClawGateway` WSL distro, installs the Gateway inside it, and pairs the app; this does not export or mutate your existing Ubuntu distro. Choose **Advanced setup** (or open the Connections tab) when you already have a Gateway — you can connect to a local Gateway on this PC, a WSL Gateway on this PC, a remote Gateway by URL and token or setup code, or a Gateway reached through an SSH tunnel. When setup finishes, the tray icon turns green; open **Command Center** from the tray to confirm connection, pairing, node status, and channel health.

## Native Windows CLI and Gateway

For terminal-first use, install OpenClaw from PowerShell with the one-line bootstrap installer:

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Verify the install with `openclaw --version`, `openclaw doctor`, and `openclaw gateway status --json`. Native Windows CLI and Gateway flows are supported and continue to improve. Managed startup uses **Windows Scheduled Tasks** when available and falls back to a per-user **Startup-folder login item** if task creation is denied.

To install the Gateway as a managed service (then confirm its status):

```powershell
openclaw gateway install
openclaw gateway status --json
```

If you only want CLI use without a managed Gateway service, onboard non-interactively and run the Gateway in the foreground:

```powershell
openclaw onboard --non-interactive --skip-health
openclaw gateway run
```

## WSL2 Gateway

WSL2 remains the most Linux-compatible Gateway runtime on Windows. Windows Hub can set up an app-owned WSL Gateway for you (see First launch above), or you can install manually inside your own distro. Manual setup from PowerShell installs WSL — `wsl --install` for the default distro, or `wsl --list --online` to browse and `wsl --install -d Ubuntu-24.04` to pick one explicitly.

Enable systemd inside the WSL distro by writing `/etc/wsl.conf`:

```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```

Restart WSL from PowerShell with `wsl --shutdown`, then install OpenClaw inside WSL with the Linux quickstart (`curl -fsSL https://openclaw.ai/install.sh | bash`) and confirm with `openclaw gateway status`.

## Gateway auto-start before Windows login

For headless WSL setups, ensure the full boot chain runs even when no one logs into Windows. Inside WSL, install the D-Bus tooling, enable user-service lingering, and install the Gateway service: `sudo apt-get install -y dbus-x11`, then `sudo loginctl enable-linger "$(whoami)"`, then `openclaw gateway install`.

In PowerShell **as Administrator**, register an on-start Scheduled Task that keeps the WSL distro alive:

```powershell
schtasks /create /tn "WSL Boot" /tr "wsl.exe -d Ubuntu --exec dbus-launch true" /sc onstart /ru "$env:USERNAME"
```

Replace `Ubuntu` with your distro name from `wsl --list --verbose`. The source flags two changes from older recipes: (1) **`dbus-launch true` instead of `/bin/true`** — on WSL ≥ 2.6.1.0 a regression ([microsoft/WSL #13416](https://github.com/microsoft/WSL/issues/13416)) causes the distro to idle-terminate 15–20 seconds after the last client exits even with linger enabled, and `dbus-launch true` keeps a child-of-init process alive as a workaround; (2) **`/ru "$env:USERNAME"` instead of `/ru SYSTEM`** — per-user WSL distros (the default) are not visible to the SYSTEM account, so the task appears to run but the distro never starts, and Windows will prompt for your password when the task is created. After reboot, verify from WSL with `systemctl --user is-enabled openclaw-gateway.service` and `systemctl --user status openclaw-gateway.service --no-pager`.

## Expose WSL services over LAN

WSL has its own virtual network. If another machine must reach a service inside WSL, forward a Windows port to the current WSL IP; the WSL IP can change after restarts, so refresh the forwarding rule when needed. The source's PowerShell example (run as Administrator) resolves the WSL IP and adds a `netsh` v4-to-v4 portproxy plus an inbound firewall rule:

```powershell
$Distro = "Ubuntu-24.04"
$ListenPort = 2222
$TargetPort = 22

$WslIp = (wsl -d $Distro -- hostname -I).Trim().Split(" ")[0]
if (-not $WslIp) { throw "WSL IP not found." }

netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=$ListenPort `
  connectaddress=$WslIp connectport=$TargetPort

New-NetFirewallRule -DisplayName "WSL SSH $ListenPort" -Direction Inbound `
  -Protocol TCP -LocalPort $ListenPort -Action Allow
```

Source notes on this pattern: SSH from another machine targets the Windows host IP (e.g., `ssh user@windows-host -p 2222`); remote nodes must point at a reachable Gateway URL, not `127.0.0.1`; and use `listenaddress=0.0.0.0` for LAN access or `127.0.0.1` for local-only access.

**Source**: OpenClaw documentation — `platforms/windows` (mirror `inbox/openclaw_docs/platforms/windows.md`), install/setup half
**Last Updated**: 2026-06-22
**Status**: Active
