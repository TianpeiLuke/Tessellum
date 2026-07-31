---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - browser
keywords:
  - openclaw browser troubleshooting linux
  - failed to start chrome cdp port 18800
  - snap chromium apparmor confinement
  - install google chrome deb nosandbox
  - attach-only mode remote debugging port
  - openclaw.json browser config reference
  - no chrome tabs found for profile
  - singleton lock headless display
topics:
  - OpenClaw
  - Browser Control
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/browser-linux-troubleshooting
access_control_group: ["general"]
---

# OpenClaw — Fixing Chrome/Chromium CDP Startup Failures for Browser Control on Linux

## Overview

This note is the operational runbook for fixing OpenClaw browser-control startup failures on Linux, mirroring the `tools/browser-linux-troubleshooting` source page. It covers the canonical failure (`Failed to start Chrome CDP on port 18800`), its root cause (snap Chromium AppArmor confinement), two fixes (install a `.deb` Google Chrome, or run snap Chromium in attach-only mode with an optional `systemd` user service), how to verify the browser works, the `browser.*` config reference, and the related `No Chrome tabs found for profile="user"` problem. Every command, config key, and error string below is reproduced verbatim from the source.

## Problem: "Failed to start Chrome CDP on port 18800"

OpenClaw's browser-control server fails to launch Chrome/Brave/Edge/Chromium with the error `{"error":"Error: Failed to start Chrome CDP on port 18800 for profile \"openclaw\"."}`.

### Root cause

On Ubuntu (and many Linux distros), the default Chromium installation is a **snap package**. Snap's AppArmor confinement interferes with how OpenClaw spawns and monitors the browser process. The `apt install chromium` command installs a stub package that redirects to snap (output: `Note, selecting 'chromium-browser' instead of 'chromium'` / `chromium-browser is already the newest version (2:1snap1-0ubuntu2).`) — this is NOT a real browser, just a wrapper.

Other common Linux launch failures and their fixes:

- `The profile appears to be in use by another Chromium process` means Chrome found stale `Singleton*` lock files in the managed profile directory. OpenClaw removes those locks and retries once when the lock points at a dead or different-host process.
- `Missing X server or $DISPLAY` means a visible browser was explicitly requested on a host without a desktop session. By default, local managed profiles now fall back to headless mode on Linux when `DISPLAY` and `WAYLAND_DISPLAY` are both unset. If you set `OPENCLAW_BROWSER_HEADLESS=0`, `browser.headless: false`, or `browser.profiles.<name>.headless: false`, remove that headed override, set `OPENCLAW_BROWSER_HEADLESS=1`, start `Xvfb`, run `openclaw browser start --headless` for a one-shot managed launch, or run OpenClaw in a real desktop session.

### Solution 1: Install Google Chrome (Recommended)

Install the official Google Chrome `.deb` package, which is not sandboxed by snap:

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # if there are dependency errors
```

Then update your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true
  }
}
```

### Solution 2: Use Snap Chromium with Attach-Only Mode

If you must use snap Chromium, configure OpenClaw to attach to a manually-started browser. First update config to set `attachOnly: true`, then start Chromium manually on the CDP port, then optionally install a `systemd` user service to auto-start it:

```json
{
  "browser": {
    "enabled": true,
    "attachOnly": true,
    "headless": true,
    "noSandbox": true
  }
}
```

```bash
chromium-browser --headless --no-sandbox --disable-gpu \
  --remote-debugging-port=18800 \
  --user-data-dir=$HOME/.openclaw/browser/openclaw/user-data \
  about:blank &
```

The optional `systemd` user unit (`~/.config/systemd/user/openclaw-browser.service`) launches `/snap/bin/chromium` with the same flags, `Restart=on-failure`, and `RestartSec=5`; enable it with `systemctl --user enable --now openclaw-browser.service`:

```ini
# ~/.config/systemd/user/openclaw-browser.service
[Unit]
Description=OpenClaw Browser (Chrome CDP)
After=network.target

[Service]
ExecStart=/snap/bin/chromium --headless --no-sandbox --disable-gpu --remote-debugging-port=18800 --user-data-dir=%h/.openclaw/browser/openclaw/user-data about:blank
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

### Verifying the Browser Works

Check status via the browser-control HTTP endpoint on `:18791`, then test browsing by starting the browser and listing tabs:

```bash
curl -s http://127.0.0.1:18791/ | jq '{running, pid, chosenBrowser}'
curl -s -X POST http://127.0.0.1:18791/start
curl -s http://127.0.0.1:18791/tabs
```

### Config reference

| Option | Description | Default |
| --- | --- | --- |
| `browser.enabled` | Enable browser control | `true` |
| `browser.executablePath` | Path to a Chromium-based browser binary (Chrome/Brave/Edge/Chromium) | auto-detected (prefers default browser when Chromium-based) |
| `browser.headless` | Run without GUI | `false` |
| `OPENCLAW_BROWSER_HEADLESS` | Per-process override for local managed browser headless mode | unset |
| `browser.noSandbox` | Add `--no-sandbox` flag (needed for some Linux setups) | `false` |
| `browser.attachOnly` | Don't launch browser, only attach to existing | `false` |
| `browser.cdpPort` | Chrome DevTools Protocol port | `18800` |
| `browser.localLaunchTimeoutMs` | Local managed Chrome discovery timeout | `15000` |
| `browser.localCdpReadyTimeoutMs` | Local managed post-launch CDP readiness timeout | `8000` |

On Raspberry Pi, older VPS hosts, or slow storage, raise `browser.localLaunchTimeoutMs` when Chrome needs more time to expose its CDP HTTP endpoint. Raise `browser.localCdpReadyTimeoutMs` when launch succeeds but `openclaw browser start` still reports `not reachable after start`. Values must be positive integers up to `120000` ms; invalid config values are rejected.

### Problem: "No Chrome tabs found for profile=\"user\""

This means you're using an `existing-session` / Chrome MCP profile: OpenClaw can see local Chrome, but there are no open tabs available to attach to. Fix options: (1) **Use the managed browser** with `openclaw browser start --browser-profile openclaw` (or set `browser.defaultProfile: "openclaw"`); or (2) **Use Chrome MCP** — make sure local Chrome is running with at least one open tab, then retry with `--browser-profile user`.

Notes on profile behavior:

- `user` is host-only. For Linux servers, containers, or remote hosts, prefer CDP profiles.
- `user` / other `existing-session` profiles keep the current Chrome MCP limits: ref-driven actions, one-file upload hooks, no dialog timeout overrides, no `wait --load networkidle`, and no `responsebody`, PDF export, download interception, or batch actions.
- Local `openclaw` profiles auto-assign `cdpPort`/`cdpUrl`; only set those for remote CDP.
- Remote CDP profiles accept `http://`, `https://`, `ws://`, and `wss://`. Use HTTP(S) for `/json/version` discovery, or WS(S) when your browser service gives you a direct DevTools socket URL.

**Source**: OpenClaw documentation — `tools/browser-linux-troubleshooting` (mirror `inbox/openclaw_docs/tools/browser-linux-troubleshooting.md`)
**Last Updated**: 2026-06-22
**Status**: Active
