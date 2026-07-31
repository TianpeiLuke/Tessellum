---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - deployment
keywords:
  - openclaw install
  - openclaw installer script
  - install.sh install.ps1
  - npm pnpm bun install openclaw
  - install from source pnpm build
  - openclaw doctor gateway status
  - openclaw not found path fix
  - install-daemon managed startup
topics:
  - OpenClaw
  - Installation
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install
access_control_group: ["general"]
---

# OpenClaw — Installing OpenClaw (Beyond the Quickstart)

## Overview

This note is the procedure for installing OpenClaw beyond the Getting Started quickstart, mirroring the `install` source page. It covers system requirements, the recommended `install.sh` / `install.ps1` installer script (with the `--no-onboard` variant), the alternative install methods (local-prefix `install-cli.sh`, npm/pnpm/bun, from source, the GitHub `main` checkout, and containers/package managers), how to verify the install, the hosting/deployment targets, the update/migrate/uninstall pointers, and the `openclaw not found` PATH fix. Read it when you need an install method other than the quickstart, want to deploy to a cloud platform, or need to update/migrate/uninstall.

## System Requirements

OpenClaw's requirements are minimal and the installer script handles the runtime automatically:

- **Node 24** (recommended) or **Node 22.19+** — the installer script handles this automatically.
- **macOS, Linux, or Windows** — Windows users can start with the native Windows Hub app, the PowerShell CLI installer, or a WSL2 Gateway. See the Windows platform page (`/platforms/windows`).
- `pnpm` is only needed if you build from source.

## Recommended: Installer Script

The installer script is the fastest way to install: it detects your OS, installs Node if needed, installs OpenClaw, and launches onboarding. (Windows desktop users can also install the native Windows Hub companion app, which includes setup, tray status, chat, node mode, and local MCP mode.) Run the installer for your platform; to install **without running onboarding**, pass `--no-onboard` (macOS/Linux/WSL2) or `-NoOnboard` (Windows PowerShell):

```bash
# macOS / Linux / WSL2
curl -fsSL https://openclaw.ai/install.sh | bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard

# Windows (PowerShell)
iwr -useb https://openclaw.ai/install.ps1 | iex
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
```

For all flags and CI/automation options, see Installer internals (`/install/installer`).

## Alternative Install Methods

### Local Prefix Installer (`install-cli.sh`)

Use this when you want OpenClaw and Node kept under a local prefix such as `~/.openclaw`, without depending on a system-wide Node install:

```bash
curl -fsSL https://openclaw.ai/install-cli.sh | bash
```

It supports npm installs by default, plus git-checkout installs under the same prefix flow (full reference: Installer internals `/install/installer#install-clish`). Already installed? Switch between package and git installs with `openclaw update --channel dev` and `openclaw update --channel stable` (see Updating `/install/updating#switch-between-npm-and-git-installs`).

### npm, pnpm, or bun

If you already manage Node yourself, install the global CLI with your package manager and then run onboarding with `--install-daemon`:

```bash
# npm
npm install -g openclaw@latest
openclaw onboard --install-daemon

# pnpm
pnpm add -g openclaw@latest
pnpm approve-builds -g
openclaw onboard --install-daemon

# bun
bun add -g openclaw@latest
openclaw onboard --install-daemon
```

Per-manager notes from source: the **hosted installer** clears npm freshness filters such as `min-release-age` for the OpenClaw package install, but if you install manually with npm your own npm policy still applies. **pnpm** requires explicit approval for packages with build scripts, so run `pnpm approve-builds -g` after the first install. **Bun** is supported for the global CLI install path; for the Gateway runtime, Node remains the recommended daemon runtime.

### From Source

For contributors or anyone who wants to run from a local checkout:

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install && pnpm build && pnpm ui:build
pnpm link --global
openclaw onboard --install-daemon
```

Or skip the link and use `pnpm openclaw ...` from inside the repo. See Setup (`/start/setup`) for full development workflows.

### Install From the GitHub `main` Checkout

To install tracking the GitHub `main` branch, pass `--install-method git --version main` to the installer script: `curl -fsSL --proto '=https' --tlsv1.2 https://openclaw.ai/install.sh | bash -s -- --install-method git --version main`

### Containers and Package Managers

The source page links out (it does not redefine these inline) to container and package-manager install paths: **Docker** (`/install/docker`, containerized or headless deployments), **Podman** (`/install/podman`, rootless container alternative to Docker), **Nix** (`/install/nix`, declarative install via Nix flake), **Ansible** (`/install/ansible`, automated fleet provisioning), and **Bun** (`/install/bun`, CLI-only usage via the Bun runtime).

## Verify the Install

After installing, confirm the CLI, configuration, and Gateway:

```bash
openclaw --version      # confirm the CLI is available
openclaw doctor         # check for config issues
openclaw gateway status # verify the Gateway is running
```

If you want **managed startup** after install, the supervisor differs by OS:

- **macOS**: LaunchAgent via `openclaw onboard --install-daemon` or `openclaw gateway install`.
- **Linux/WSL2**: systemd user service via the same commands.
- **Native Windows**: Scheduled Task first, with a per-user Startup-folder login item fallback if task creation is denied.

## Hosting and Deployment

To deploy OpenClaw on a cloud server or VPS, the source page links out to per-target runbooks (digested by the `in0*` install sub-plans and the `rt03` VPS note, not duplicated here): **VPS** (`/vps`, any Linux VPS), **Docker VM** (`/install/docker-vm-runtime`, shared Docker steps), **Kubernetes** (`/install/kubernetes`), **Fly.io** (`/install/fly`), **Hetzner** (`/install/hetzner`), **GCP** (`/install/gcp`, Google Cloud), **Azure** (`/install/azure`), **Railway** (`/install/railway`), **Render** (`/install/render`), and **Northflank** (`/install/northflank`).

## Update, Migrate, or Uninstall

The source page points to three day-2 runbooks (owned by the `in0*` install sub-plans): **Updating** (`/install/updating`, keep OpenClaw up to date), **Migrating** (`/install/migrating`, move to a new machine), and **Uninstall** (`/install/uninstall`, remove OpenClaw completely).

## Troubleshooting: `openclaw` Not Found

If the install succeeded but `openclaw` is not found in your terminal, check Node, the global package prefix, and your `PATH`; if `$(npm prefix -g)/bin` is not in your `$PATH`, add it to your shell startup file (`~/.zshrc` or `~/.bashrc`):

```bash
node -v           # Node installed?
npm prefix -g     # Where are global packages?
echo "$PATH"      # Is the global bin dir in PATH?

# If $(npm prefix -g)/bin is missing from $PATH, add it to ~/.zshrc or ~/.bashrc:
export PATH="$(npm prefix -g)/bin:$PATH"
```

Then open a new terminal. See Node setup (`/install/node`) for more details.

**Source**: OpenClaw documentation — `install` (mirror `inbox/openclaw_docs/install.md`)
**Last Updated**: 2026-06-22
**Status**: Active
