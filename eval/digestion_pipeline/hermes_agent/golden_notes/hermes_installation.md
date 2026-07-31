---
tags:
  - resource
  - documentation
  - hermes_agent
  - getting_started
  - installation
keywords:
  - hermes agent installation
  - one-line installer
  - install layout fhs
  - non-sudo service user install
  - install method auto-detection
  - hermes doctor troubleshooting
topics:
  - Hermes Agent
  - Getting Started
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/getting-started/installation
access_control_group: ["general"]
---

# Hermes Agent — Installation

## Overview

This is the **full install reference** for Hermes Agent: the procedure for getting the command-line agent (and optional Desktop app) running on Linux, macOS, WSL2, native Windows, or Android via Termux. The headline path is a single `curl … | bash` (or PowerShell `iex`) command that auto-provisions every dependency, clones the repo, builds a virtualenv, and configures an LLM provider — "up and running in under two minutes." Beyond the happy path it documents the per-user vs root **FHS install layout**, the prerequisites the installer auto-handles, unprivileged
**service-user** installs, a troubleshooting table, and how `hermes update` auto-detects which
install method you used. By the end of the installer you are ready to chat.

## Quick Install

### With the Hermes Desktop installer on macOS or Windows (recommended)

Download the [Hermes Desktop installer](https://hermes-agent.nousresearch.com/) from the website and run it — this installs both the command-line and desktop applications.

### Without Hermes Desktop

For a command-line only install, run the one-line installer for your platform.

**Linux / macOS / WSL2 / Android (Termux):**

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

**Windows (native)** — run in PowerShell:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1) 
```

If you later want the Desktop app after a command-line-only install, run `hermes desktop`.

### What the Installer Does

The installer handles everything automatically — all dependencies (Python, Node.js, ripgrep, ffmpeg), the repo clone, virtual environment, global `hermes` command setup, and LLM provider configuration. By the end, you're ready to chat.

### Install Layout

Where the installer puts things depends on whether you install as a normal user or as root:

| Installer | Code lives at | `hermes` binary | Data directory |
|---|---|---|---|
| pip install | Python site-packages | `~/.local/bin/hermes` (console_scripts) | `~/.hermes/` |
| Per-user (git installer) | `~/.hermes/hermes-agent/` | `~/.local/bin/hermes` (symlink) | `~/.hermes/` |
| Root-mode (`sudo curl … \| sudo bash`) | `/usr/local/lib/hermes-agent/` | `/usr/local/bin/hermes` | `/root/.hermes/` (or `$HERMES_HOME`) |

The root-mode **FHS layout** (`/usr/local/lib/…`, `/usr/local/bin/hermes`) matches where other system-wide developer tools land on Linux. It's useful for shared-machine deployments where one system install should serve every user. Per-user config (auth, skills, sessions) still lives under each user's `~/.hermes/` or explicit `HERMES_HOME`.

### After Installation

Reload your shell and start chatting, then use the dedicated commands to reconfigure individual settings later (or `hermes setup` to run the full wizard at once):

```bash
source ~/.bashrc      # or: source ~/.zshrc
hermes                # Start chatting!
hermes model          # Choose your LLM provider and model
hermes tools          # Configure which tools are enabled
hermes gateway setup  # Set up messaging platforms
hermes config set     # Set individual config values
```

**Fastest path — Nous Portal:** one subscription covers 300+ models plus the Tool Gateway (web
search, image generation, TTS, cloud browser). `hermes setup --portal` logs you in, sets Nous as your provider, and turns on the Tool Gateway in one command — skipping per-tool key juggling.

## Prerequisites

On non-Windows platforms, the only prerequisite is **Git** (`git --version`). The installer automatically detects what's missing and installs everything else for you — you do **not** need to install Python, Node.js, ripgrep, or ffmpeg manually:

- **uv** — fast Python package manager
- **Python 3.11** — via uv, no sudo needed
- **Node.js v22** — for browser automation and the WhatsApp bridge
- **ripgrep** — fast file search
- **ffmpeg** — audio format conversion for TTS

**Nix users:** if you use Nix (on NixOS, macOS, or Linux), there's a dedicated setup path with a
Nix flake, declarative NixOS module, and optional container mode — see the [Nix & NixOS Setup](hermes_install_nix_quickstart.md) guide instead.

## Manual / Developer Installation

To clone the repo and install from source — for contributing, running from a specific branch, or having full control over the virtual environment — see the **Development Setup** section in the Contributing guide (developer guide). This page covers only the end-user installers.

## Non-Sudo / System Service User Installs

Running Hermes as a dedicated unprivileged user (e.g. a `hermes` systemd service account, or any user without `sudo`) is supported. The only step on the install path that genuinely needs root is Playwright's `--with-deps`, which `apt`-installs the shared libraries Chromium uses (`libnss3`, `libxkbcommon`, etc.). The installer detects whether sudo is available and gracefully degrades when it isn't — it installs the Chromium binary into the service user's own Playwright cache and prints the exact command an administrator must run separately.

**Recommended split (Debian/Ubuntu):**

1. **One time, as an admin user with sudo**, install the system libraries Chromium needs: `sudo npx playwright install-deps chromium` (runnable from anywhere; `npx` fetches Playwright on the fly).
2. **As the unprivileged service user**, run the regular installer. It detects the missing sudo, skips `--with-deps`, and installs Chromium into the user's local Playwright cache. If you're running headless and don't need browser automation, skip Playwright entirely with `--skip-browser`:
   ```bash
   curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-browser
   ```
3. **Make `hermes` available to the service user's shells.** The launcher is written to `~/.local/bin/hermes`; service accounts often have a minimal PATH that excludes it. Either add it to the user's profile (`echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc`) or symlink the venv launcher system-wide as an admin (`sudo ln -s /home/hermes/.hermes/hermes-agent/venv/bin/hermes /usr/local/bin/hermes`).
4. **Verify** with `hermes doctor`. A `ModuleNotFoundError: No module named 'dotenv'` means you're invoking the repo-source `hermes` file (`~/.hermes/hermes-agent/hermes`) with system Python instead of the venv launcher (`~/.hermes/hermes-agent/venv/bin/hermes`) — fix step 3.

The same pattern works on Arch (the installer uses pacman with the same sudo-detection logic), Fedora/RHEL, and openSUSE — those distros don't support `--with-deps` at all, so an administrator always installs the system libraries separately. The relevant `dnf`/`zypper` commands are printed by the installer.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `hermes: command not found` | Reload your shell (`source ~/.bashrc`) or check PATH |
| `API key not set` | Run `hermes model` to configure your provider, or `hermes config set OPENROUTER_API_KEY your_key` |
| Missing config after update | Run `hermes config check` then `hermes config migrate` |

For more diagnostics, run `hermes doctor` — it tells you exactly what's missing and how to fix it.

## Install Method Auto-Detection

Hermes auto-detects whether it was installed via `pip`, the git installer, Homebrew, or NixOS, and `hermes update` prints the matching update command for that path. There's no env var to set — the detection is based on the install layout (Python site-packages, `~/.hermes/hermes-agent/`, Homebrew prefix, or Nix store path). `hermes doctor` also surfaces the detected method under its environment summary.

**Source**: `inbox/hermes_agent_docs/getting-started/installation.md` · https://hermes-agent.nousresearch.com/docs/getting-started/installation
**Last Updated**: 2026-06-19
**Status**: Active
