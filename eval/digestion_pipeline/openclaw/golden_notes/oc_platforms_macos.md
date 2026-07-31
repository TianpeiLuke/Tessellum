---
tags:
  - resource
  - documentation
  - openclaw
  - platforms
  - macos
keywords:
  - openclaw macos app
  - menu bar companion gateway broker
  - ai.openclaw.gateway launchagent
  - launchctl kickstart bootout
  - exec-approvals.json system.run
  - openclaw://agent deep link
  - openclaw-mac debug cli
  - remote mode ssh control tunnel
  - openclaw_state_dir
topics:
  - OpenClaw
  - Platforms (macOS)
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/platforms/macos
access_control_group: ["general"]
---

# OpenClaw — macOS Companion App (Menu-Bar Gateway Broker)

## Overview

This note is the operational procedure for the OpenClaw **macOS app** — the menu-bar companion that owns the Mac's TCC permissions, manages or attaches to the local Gateway, and exposes macOS capabilities to the agent as a node. It mirrors the `platforms/macos` source page end to end: what the app does, the Local-vs-Remote mode choice, launchd control of the `ai.openclaw.gateway` LaunchAgent, the node command surface, Exec approvals governing `system.run` via `~/.openclaw/exec-approvals.json`, the `openclaw://agent` deep-link scheme, the typical onboarding flow, state-dir placement guidance, the native build/dev workflow, the `openclaw-mac` debug CLI, and the Remote-mode SSH control tunnel. Permission/TCC detail, Canvas, PeekabooBridge, the bundled Gateway, and remote-access setup live on sibling pages and are linked rather than redefined here.

## What it does

The macOS app is the **menu-bar companion** for OpenClaw: it owns permissions, manages or attaches to the Gateway locally (launchd or manual), and exposes macOS capabilities to the agent as a node. Its responsibilities are:

- Shows native notifications and status in the menu bar.
- Owns TCC prompts — Notifications, Accessibility, Screen Recording, Microphone, Speech Recognition, Automation/AppleScript.
- Runs or connects to the Gateway (local or remote).
- Exposes macOS-only tools — Canvas, Camera, Screen Recording, `system.run`.
- Starts the local node host service in **remote** mode (launchd), and stops it in **local** mode.
- Optionally hosts **PeekabooBridge** for UI automation.
- Installs the global CLI (`openclaw`) on request via npm, pnpm, or bun — the app prefers npm, then pnpm, then bun (Node remains the recommended Gateway runtime).

## Local vs remote mode

The app runs in one of two Gateway-management modes:

- **Local** (default): the app attaches to a running local Gateway if present; otherwise it enables the launchd service via `openclaw gateway install`.
- **Remote**: the app connects to a Gateway over SSH/Tailscale and never starts a local process. In this mode the app starts the local **node host service** so the remote Gateway can reach this Mac; the app does **not** spawn the Gateway as a child process. Gateway discovery prefers Tailscale MagicDNS names over raw tailnet IPs, so the Mac app recovers more reliably when tailnet IPs change.

## Launchd control

The app manages a per-user LaunchAgent labeled `ai.openclaw.gateway` (or `ai.openclaw.<profile>` when using `--profile`/`OPENCLAW_PROFILE`; legacy `com.openclaw.*` still unloads). Control it with:

```bash
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
launchctl bootout gui/$UID/ai.openclaw.gateway
```

Replace the label with `ai.openclaw.<profile>` when running a named profile. If the LaunchAgent isn't installed, enable it from the app or run `openclaw gateway install`. If the gateway repeatedly disappears for minutes to hours and only resumes when you touch the Control UI or SSH into the host, see the troubleshooting note for macOS Maintenance Sleep / `ENETDOWN` crashes and launchd's respawn-protection gate (linked under Related Notes).

## Node capabilities (mac)

The macOS app presents itself as a node and reports a `permissions` map so agents can decide what's allowed. Common commands are:

- **Canvas**: `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot`, `canvas.a2ui.*`
- **Camera**: `camera.snap`, `camera.clip`
- **Screen**: `screen.snapshot`, `screen.record`
- **System**: `system.run`, `system.notify`

For node service ↔ app IPC: when the headless node host service is running (remote mode), it connects to the Gateway WS as a node, and `system.run` executes in the macOS app (UI/TCC context) over a local Unix socket — prompts and output stay in-app. The full single-component-interface (SCI) transport diagram (`Gateway → Node Service (WS) → Mac App` over a UDS with token + HMAC + TTL) is documented in the macOS IPC note linked under Related Notes.

## Exec approvals (system.run)

`system.run` is controlled by **Exec approvals** in the macOS app (Settings → Exec approvals). Security + ask + allowlist are stored locally on the Mac in `~/.openclaw/exec-approvals.json`. Example:

```json
{
  "version": 1,
  "defaults": {
    "security": "deny",
    "ask": "on-miss"
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "allowlist": [{ "pattern": "/opt/homebrew/bin/rg" }]
    }
  }
}
```

The enforcement rules are:

- `allowlist` entries are glob patterns for resolved binary paths, or bare command names for PATH-invoked commands.
- Raw shell command text containing shell control or expansion syntax (`&&`, `||`, `;`, `|`, `` ` ``, `$`, `<`, `>`, `(`, `)`) is treated as an allowlist miss and requires explicit approval (or allowlisting the shell binary).
- Choosing "Always Allow" in the prompt adds that command to the allowlist.
- `system.run` environment overrides are filtered — it drops `PATH`, `DYLD_*`, `LD_*`, `BASHOPTS`, `FPATH`, `KSH_ENV`, `NODE_OPTIONS`, `NODE_REDIRECT_WARNINGS`, `NODE_REPL_EXTERNAL_MODULE`, `NODE_REPL_HISTORY`, `NODE_V8_COVERAGE`, `PYTHON*`, `PERL*`, `RUBYOPT`, `SHELLOPTS`, `PS4`, `TCLLIBPATH` — and then merges the remainder with the app's environment.
- For shell wrappers (`bash|sh|zsh ... -c/-lc`), request-scoped environment overrides are reduced to a small explicit allowlist: `TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`.
- For allow-always decisions in allowlist mode, known dispatch wrappers (`env`, `flock`, `nice`, `nohup`, `stdbuf`, `timeout`) persist inner executable paths instead of wrapper paths; if unwrapping is not safe, no allowlist entry is persisted automatically.

## Deep links

The app registers the `openclaw://` URL scheme for local actions. The `openclaw://agent` action triggers a Gateway `agent` request:

```bash
open 'openclaw://agent?message=Hello%20from%20deep%20link'
```

Its query parameters are `message` (required), `sessionKey` (optional), `thinking` (optional), `deliver` / `to` / `channel` (optional), `timeoutSeconds` (optional), and `key` (optional unattended-mode key). For safety: without `key` the app prompts for confirmation, enforces a short message limit for the confirmation prompt, and ignores `deliver` / `to` / `channel`; with a valid `key` the run is unattended (intended for personal automations).

## Onboarding flow (typical)

1. Install and launch **OpenClaw.app**.
2. Complete the permissions checklist (TCC prompts).
3. Ensure **Local** mode is active and the Gateway is running.
4. Install the CLI if you want terminal access.

## State dir placement (macOS)

Avoid putting your OpenClaw state dir in iCloud or other cloud-synced folders — sync-backed paths can add latency and occasionally cause file-lock/sync races for sessions and credentials. Prefer a local non-synced state path such as:

```bash
OPENCLAW_STATE_DIR=~/.openclaw
```

If `openclaw doctor` detects state under `~/Library/Mobile Documents/com~apple~CloudDocs/...` or `~/Library/CloudStorage/...`, it will warn and recommend moving back to a local path.

## Build and dev workflow (native)

The native macOS app builds with Swift: `cd apps/macos && swift build`, then `swift run OpenClaw` (or use Xcode). Package the app with `scripts/package-mac-app.sh`.

## Debug gateway connectivity (macOS CLI)

Use the `openclaw-mac` debug CLI to exercise the same Gateway WebSocket handshake and discovery logic the macOS app uses, without launching the app:

```bash
cd apps/macos
swift run openclaw-mac connect --json
swift run openclaw-mac discover --timeout 3000 --json
```

The `connect` options are `--url <ws://host:port>` (override config), `--mode <local|remote>` (resolve from config; default: config or local), `--probe` (force a fresh health probe), `--timeout <ms>` (request timeout, default `15000`), and `--json` (structured output for diffing). The `discover` options are `--include-local` (include gateways that would be filtered as "local"), `--timeout <ms>` (overall discovery window, default `2000`), and `--json`. Compare against `openclaw gateway discover --json` to see whether the macOS app's discovery pipeline (`local.` plus the configured wide-area domain, with wide-area and Tailscale Serve fallbacks) differs from the Node CLI's `dns-sd`-based discovery.

## Remote connection plumbing (SSH tunnels)

When the macOS app runs in **Remote** mode, it opens an SSH tunnel so local UI components can talk to a remote Gateway as if it were on localhost. The **control tunnel** (Gateway WebSocket port) has these properties:

- **Purpose:** health checks, status, Web Chat, config, and other control-plane calls.
- **Local port:** the Gateway port (default `18789`), always stable.
- **Remote port:** the same Gateway port on the remote host.
- **Behavior:** no random local port; the app reuses an existing healthy tunnel or restarts it if needed.
- **SSH shape:** `ssh -N -L <local>:127.0.0.1:<remote>` with BatchMode + ExitOnForwardFailure + keepalive options.
- **IP reporting:** the SSH tunnel uses loopback, so the gateway will see the node IP as `127.0.0.1`. Use **Direct (ws/wss)** transport if you want the real client IP to appear (see macOS remote access, linked under Related Notes).

**Source**: OpenClaw documentation — `platforms/macos` (mirror `inbox/openclaw_docs/platforms/macos.md`)
**Last Updated**: 2026-06-22
**Status**: Active
