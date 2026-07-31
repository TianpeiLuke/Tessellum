---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - nodes
keywords:
  - windows node mode
  - windows hub node
  - local mcp mode
  - openclaw mcp server loopback
  - gateway.nodes.allowCommands
  - openclaw devices approve
  - node mode mcp mode matrix
  - windows troubleshooting runbook
  - screen.snapshot camera audio fail
  - openclaw nodes status
topics:
  - OpenClaw
  - Windows Platform
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/windows
access_control_group: ["general"]
---

# OpenClaw — Windows Node Mode, Local MCP Mode, and Troubleshooting

## Overview

This note is the operate-after-install half of the OpenClaw `platforms/windows` source page: how to run Windows Hub as a first-class OpenClaw **node** (declaring Windows-native capabilities the agent can drive through the Gateway), how to expose the same capability registry as a **local MCP server** on loopback, the off/on **mode matrix** crossing those two switches, and the Windows **troubleshooting** runbook (tray icon, local setup, pairing, remote web chat, `screen.snapshot`/camera/audio, and Git/GitHub connectivity). It assumes Windows Hub is already installed; the three install paths (Windows Hub, native PowerShell CLI/Gateway, WSL2 Gateway) plus auto-start and LAN port-proxy live in the companion install note. Every command, capability name, config key, and log path is copied verbatim from the mirror page `platforms/windows.md`.

## Windows Node Mode

Windows Hub can register as a first-class OpenClaw node. Once registered, the agent can use declared Windows-native capabilities through the Gateway. The page groups the common node commands by capability surface:

- `canvas.present`, `canvas.hide`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot`
- `screen.snapshot` and, with explicit opt-in, `screen.record`
- `camera.list` and, with explicit opt-in, `camera.snap`, `camera.clip`
- `system.notify`, `system.run`, `system.run.prepare`, `system.which`
- `location.get`, `device.info`, `device.status`
- `stt.transcribe`, `tts.speak`

### Pairing the node

Node mode **requires Gateway pairing**. If the app shows a pairing request, approve it from the Gateway host:

```powershell
openclaw devices list
openclaw devices approve <request-id>
openclaw nodes status
```

`openclaw devices list` enumerates pending operator/node requests, `openclaw devices approve <request-id>` authorizes a specific request, and `openclaw nodes status` confirms the node is registered and reachable.

### Command-forwarding policy

The Gateway only forwards commands that the node declares **and** server policy allows — declaration alone is not sufficient. Privacy-sensitive commands — specifically `screen.record`, `camera.snap`, and `camera.clip` — require explicit `gateway.nodes.allowCommands` opt-in before the Gateway will forward them, even after the node declares the capability and pairing is approved.

## Local MCP Mode

Windows Hub can expose the same Windows-native capability registry as a local **MCP server on loopback**. The page frames this as useful when you want local MCP clients to drive Windows capabilities without a running OpenClaw Gateway — i.e., it is an alternative to node mode rather than a dependency on it. Named MCP clients include Claude Desktop, Claude Code, and Cursor.

Enable local MCP mode in **Windows Hub Settings** under the developer/advanced section. After the server is enabled, the app shows the **loopback endpoint** and the **bearer token** that MCP clients use to connect.

### Mode matrix

Node mode and the MCP server are two independent switches, giving four operating combinations:

| Node mode | MCP server | Behavior                           |
| --------- | ---------- | ---------------------------------- |
| off       | off        | Operator-only desktop app          |
| on        | off        | Gateway-connected Windows node     |
| off       | on         | Local MCP server only              |
| on        | on         | Gateway node plus local MCP server |

## Troubleshooting

The page closes with a Windows troubleshooting runbook of six independent symptom-to-fix entries.

### The tray icon does not appear

Check Task Manager for `OpenClaw.Tray.WinUI.exe`. If it is running, open the hidden tray-icons area and pin it. If it is not running, launch **OpenClaw Companion** from the Start menu.

### Local setup fails

Open the setup log from Windows Hub, or inspect the latest setup log directly:

```powershell
notepad "$env:LOCALAPPDATA\OpenClawTray\Logs\Setup\easy-setup-latest.txt"
```

Common causes are disabled WSL, blocked virtualization, stale app-owned WSL state, or a network failure while installing the Gateway package.

### The app says pairing is required

Approve the operator or node request from the Gateway:

```powershell
openclaw devices list
openclaw devices approve <request-id>
```

If the device already had a token, reconnect from the Connections tab after approval.

### Web chat cannot reach a remote Gateway

Remote web chat needs HTTPS or localhost. For self-signed certificates, trust the certificate in Windows, or use an SSH tunnel to a localhost URL.

### `screen.snapshot`, camera, or audio commands fail

Confirm Windows permissions for camera, microphone, screen capture, and notifications. Packaged installs declare the protected capabilities, but Windows may still prompt the first time a command uses them.

### Git or GitHub connectivity fails

Some networks block or throttle HTTPS to GitHub. If `git clone` or `gh auth login` fails, try another network, a VPN, or an HTTP/HTTPS proxy. For token-based `gh` auth in the current session:

```powershell
$env:GH_TOKEN="<your-token>"
gh auth status
gh auth setup-git
```

The page warns: never commit tokens or paste them into issues or pull requests.

**Source**: OpenClaw documentation — `platforms/windows` (mirror `inbox/openclaw_docs/platforms/windows.md`)
**Last Updated**: 2026-06-22
**Status**: Active
