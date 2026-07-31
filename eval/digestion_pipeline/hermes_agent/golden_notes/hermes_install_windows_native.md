---
tags:
  - resource
  - documentation
  - hermes_agent
  - installation
  - windows
keywords:
  - windows native install
  - powershell installer
  - dep_ensure bootstrap
  - gateway at login schtasks
  - localappdata hermes data layout
  - hermes uninstall
topics:
  - Hermes Agent
  - Deployment & Platforms
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/windows-native
access_control_group: ["general"]
---

# Hermes Agent — Native Windows Install

## Overview

This is the install/deploy procedure for running Hermes Agent **natively** on Windows 10 / 11 — no WSL, no Cygwin, no Docker. A single PowerShell `irm | iex` one-liner provisions the whole agent harness without admin rights: it bootstraps `uv`, installs Python 3.11 / Node.js 22 / PortableGit, clones the repo into `%LOCALAPPDATA%\hermes\hermes-agent`, runs a tiered `uv pip install`, wires User PATH + `HERMES_HOME`, and runs the first-run `hermes setup` wizard. The gateway is kept alive across logins as a `schtasks /SC ONLOGON` Scheduled Task (not a Windows Service) spawned detached via `pythonw.exe`. This note covers install, the on-demand `dep_ensure` bootstrap, gateway-at-login, the `%LOCALAPPDATA%\hermes` data layout, and clean uninstall; the day-to-day Windows runtime surface (Git Bash, UTF-8 console, editor, pitfalls) lives in [hermes_windows_native_runtime](hermes_windows_native_runtime.md).

## Quick install

Open **PowerShell** (or Windows Terminal) and run:

```powershell
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```

No admin rights required. The installer goes to `%LOCALAPPDATA%\hermes\` and adds `hermes` to your **User PATH** — open a new terminal after it finishes.

**Installer options** require the scriptblock form to pass parameters:

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1))) -NoVenv -SkipSetup -Branch main
```

| Parameter | Default | Purpose |
|---|---|---|
| `-Branch` | `main` | Clone a specific branch (useful for testing PRs) |
| `-Commit` | unset | Pin install to a specific commit SHA (overrides `-Branch`) |
| `-Tag` | unset | Pin install to a specific git tag (e.g. `v0.14.0`) |
| `-NoVenv` | off | Skip venv creation (advanced — you manage Python yourself) |
| `-SkipSetup` | off | Skip the post-install `hermes setup` wizard |
| `-HermesHome` | `%LOCALAPPDATA%\hermes` | Override data directory |
| `-InstallDir` | `%LOCALAPPDATA%\hermes\hermes-agent` | Override code location |

The installer auto-retries flaky git fetches and strips BOM from any downloaded `install.ps1` payload, so a UTF-8 BOM picked up during HTTP transit no longer breaks the `[scriptblock]::Create((irm ...))` form.

### Desktop installer (alternative)

A thin GUI installer is also available — useful if you'd rather double-click an `.exe` than open PowerShell. Download Hermes Desktop, run the installer, and on first launch the GUI calls `install.ps1` under the hood to provision Python (via `uv`), Node, PortableGit, and the rest of the dependency bootstrap. After the first run, the desktop app and the PowerShell-installed `hermes` CLI share the same `%LOCALAPPDATA%\hermes\hermes-agent` install and `%LOCALAPPDATA%\hermes` data directory — switch between the GUI and the CLI freely. Use the desktop installer when you want a familiar Windows install experience or you're handing Hermes to a non-developer; use the PowerShell one-liner when you're already in a terminal. (The Desktop app surface itself is documented in [hermes_desktop_app](hermes_desktop_app.md).)

### Dependency bootstrap (`dep_ensure`)

On first launch (and on demand when a missing tool is detected), Hermes runs a small Python bootstrapper — `hermes_cli/dep_ensure.py` — that checks for and lazily installs the non-Python dependencies it needs. On Windows, the relevant ones are:

| Dependency | Why Hermes needs it |
|---|---|
| **PortableGit** | Provides `bash.exe` for the terminal tool and `git` for in-session clones. Provisioned at install time, not by `dep_ensure`. |
| **Node.js 22** | Required for the browser tool (`agent-browser`), the TUI's web bridge, and the WhatsApp bridge. |
| **ffmpeg** | Audio format conversion for TTS / voice messages. |
| **ripgrep** | Fast file search — falls back to `grep` if unavailable. |
| **npm packages** | `agent-browser`, Playwright Chromium, and any per-toolset Node deps are installed once at first browser-tool use. |

Each dep has a `shutil.which(...)`-style check; if a binary is missing and the run is interactive, `dep_ensure` offers to install it (deferring to `scripts\install.ps1 -ensure <dep>` for the actual install logic). Non-interactive runs (gateway, cron, headless desktop launches) skip the prompt and surface a clear `this feature needs <dep>` error instead.

## What the installer actually does

Top-to-bottom, in order:

1. **Bootstraps `uv`** — Astral's fast Python manager. Installed to `%USERPROFILE%\.local\bin`.
2. **Installs Python 3.11** via `uv`. No existing Python needed.
3. **Installs Node.js 22** (winget if available, else a portable Node tarball unpacked under `%LOCALAPPDATA%\hermes\node`). Used for the browser tool and the WhatsApp bridge.
4. **Installs portable Git** — if `git` is already on PATH the installer uses it; otherwise it downloads a trimmed, self-contained **PortableGit** (~45 MB, from the official `git-for-windows` release) to `%LOCALAPPDATA%\hermes\git`. No admin, no Windows installer registry, no interference with anything else on the box.
5. **Clones the repo** to `%LOCALAPPDATA%\hermes\hermes-agent` and creates a virtualenv inside it.
6. **Tiered `uv pip install`** — tries `.[all]` first, falls back to progressively smaller sets (`[messaging,dashboard,ext]` → `[messaging]` → `.`) if a `git+https` dep flakes on rate-limited GitHub. Prevents the "single flake drops you to a bare install" failure mode.
7. **Auto-installs messaging SDKs** keyed off `.env` — if `TELEGRAM_BOT_TOKEN` / `DISCORD_BOT_TOKEN` / `SLACK_BOT_TOKEN` / `SLACK_APP_TOKEN` / `WHATSAPP_ENABLED` are present, runs `python -m ensurepip --upgrade` and targeted `pip install` calls so each platform's SDK is actually importable.
8. **Sets `HERMES_GIT_BASH_PATH`** to the resolved `bash.exe` so Hermes finds it deterministically in fresh shells (the Git Bash resolution order is detailed in [hermes_windows_native_runtime](hermes_windows_native_runtime.md)).
9. **Adds `%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts` to User PATH and sets `HERMES_HOME=%LOCALAPPDATA%\hermes`** — exposes the `hermes` command (and points it at your data dir) after you open a new terminal.
10. **Runs `hermes setup`** — the normal first-run wizard (model, provider, toolsets). Skip with `-SkipSetup`.

On Windows, per-tool API key setup (Firecrawl, FAL, Browser Use, OpenAI TTS) is the highest-friction part of getting a useful agent. A Nous Portal subscription covers the model **and** all of those tools through one OAuth login. After the installer finishes, run `hermes setup --portal` to wire everything up.

## Running the gateway at Windows login

`hermes gateway install` on Windows uses **Scheduled Tasks** with a Startup-folder fallback — no admin required.

### Install

```powershell
hermes gateway install
```

What happens under the hood:

1. `schtasks /Create /SC ONLOGON /RL LIMITED /TN HermesGateway` — registers a task that runs at your login with standard (non-elevated) permissions. No UAC prompt.
2. If schtasks is blocked by group policy, falls back to writing a `start /min cmd.exe /d /c <wrapper>` shortcut into `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`. Same effect, slightly cruder.
3. Spawns the gateway **detached via `pythonw.exe`** — not `python.exe`. `pythonw.exe` has no console attached, which immunizes it against `CTRL_C_EVENT` broadcasts from sibling processes (a real issue that used to kill the gateway when you Ctrl+C'd anything in the same process group).

Flags used when spawning: `DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW | CREATE_BREAKAWAY_FROM_JOB`.

### Manage

```powershell
hermes gateway status      # Merged view: schtasks + Startup folder + running PID
hermes gateway start       # Starts the scheduled task now
hermes gateway stop        # Graceful SIGTERM equivalent (TerminateProcess via psutil)
hermes gateway restart
hermes gateway uninstall   # Removes schtasks entry, Startup shortcut, pid file
```

`hermes gateway status` is idempotent — call it a thousand times in a row and it will never accidentally kill the gateway. (The `os.kill(pid, 0)` → `CTRL_C_EVENT` footgun behind the earlier behavior, and the psutil-based fix, are covered in the runtime note's process-management internals: [hermes_windows_native_runtime](hermes_windows_native_runtime.md).)

### Why not a Windows Service?

Services require admin rights to install and tie the gateway's lifecycle to machine boot, not user login. The typical Hermes user wants: log in → gateway available, log out → gateway gone. Scheduled Tasks do exactly that without elevation. If you genuinely want a service, use `nssm` or `sc create` manually — but you probably don't.

## Data layout

| Path | Contents |
|---|---|
| `%LOCALAPPDATA%\hermes\hermes-agent\` | Git checkout + venv. `venv\Scripts\hermes.exe` is the command added to User PATH. Safe to `Remove-Item -Recurse` and reinstall. |
| `%LOCALAPPDATA%\hermes\git\` | PortableGit (only if the installer provisioned it). |
| `%LOCALAPPDATA%\hermes\node\` | Portable Node.js (only if the installer provisioned it). |
| `%LOCALAPPDATA%\hermes\bin\` | Hermes's managed `uv.exe` (the Python manager it uses for updates). |
| `%LOCALAPPDATA%\hermes\` (root) | Your config, auth, skills, sessions, logs (`config.yaml`, `.env`, `skills\`, `sessions\`, `logs\`, …). **Survives reinstalls.** |

On native Windows the installer sets `HERMES_HOME=%LOCALAPPDATA%\hermes`, so your data and the disposable install live under the **same** `%LOCALAPPDATA%\hermes` root: the install/runtime is the `hermes-agent\`, `git\`, `node\`, and `bin\` subdirectories, while your data files sit directly in `%LOCALAPPDATA%\hermes`. Reinstalling only replaces the `hermes-agent\` checkout, so your data survives — but because the two share a root, **don't** `Remove-Item -Recurse %LOCALAPPDATA%\hermes` if you want to keep your data; delete the `hermes-agent\` subdirectory instead. Your data directory is identical in shape to a Linux `~/.hermes`, so you can mirror it between machines.

**Override `HERMES_HOME`:** set the environment variable to point at a different data dir (e.g. `%USERPROFILE%\.hermes` to match a Linux/WSL layout). Works the same as on Linux.

## Uninstall

From PowerShell:

```powershell
hermes uninstall
```

That's the clean path — removes the schtasks entry, Startup folder shortcut, `hermes.cmd` shim, deletes `%LOCALAPPDATA%\hermes\hermes-agent\`, and trims the User PATH. It leaves the rest of `%LOCALAPPDATA%\hermes\` alone (your config, auth, skills, sessions, logs) in case you're reinstalling.

To nuke everything:

```powershell
hermes uninstall
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\hermes"
# Also remove a legacy CLI/WSL data dir if you ever used one:
Remove-Item -Recurse -Force "$env:USERPROFILE\.hermes"
```

The `hermes uninstall` CLI subcommand also handles the case where the schtasks entry was registered under a different task name (older installs) — it searches by install path rather than by hardcoded task name.

## Where to go next

- The full install page, including Linux / macOS / WSL2 / Termux (installation base → SP01).
- [hermes_install_windows_wsl2](hermes_install_windows_wsl2.md) — the alternative Windows path if you want POSIX semantics or the dashboard terminal pane (both coexist under separate data roots).
- The CLI Reference for every `hermes` subcommand, and the FAQ for common non-Windows-specific questions.
- The Messaging Gateway docs for running Telegram / Discord / Slack on Windows.

**Source**: `inbox/hermes_agent_docs/user-guide/windows-native.md` · https://hermes-agent.nousresearch.com/docs/user-guide/windows-native
**Last Updated**: 2026-06-19
**Status**: Active
