---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - uninstall
keywords:
  - openclaw uninstall
  - openclaw gateway uninstall
  - remove openclaw cli
  - launchd systemd schtasks service removal
  - openclaw state dir workspace deletion
  - openclaw dry-run all non-interactive
  - openclaw profile remote uninstall
topics:
  - OpenClaw
  - Install / Uninstall
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/uninstall
access_control_group: ["general"]
---

# OpenClaw — Uninstalling OpenClaw Completely

## Overview

This procedure covers completely removing OpenClaw from a machine — the CLI, the gateway service, persisted state/config, and the agent workspace — mirroring the `install/uninstall` source page. It documents the two top-level paths the page offers: the **easy path** (`openclaw uninstall`) when the CLI is still installed, and **manual service removal** when the CLI is gone but the launchd / systemd / schtasks service keeps running. It also reproduces the equivalent manual steps (stop + uninstall the gateway service, delete state/config/workspace, remove the CLI per package manager), the profile and remote-mode caveats, and the normal-install vs source-checkout distinction.

## Two Paths

The source page presents two top-level paths: the **Easy path** when `openclaw` is still installed (use the built-in uninstaller), and **Manual service removal** when the CLI is gone but the service is still running. Pick the easy path whenever the CLI is present; fall back to manual removal only when `openclaw` is missing yet the gateway service keeps running.

## Easy Path (CLI Still Installed)

The recommended approach is the built-in uninstaller, `openclaw uninstall`. When invoked through the CLI, state removal **preserves configured workspace directories unless you also select `--workspace`**. To preview what would be removed without changing anything (safe), run `openclaw uninstall --dry-run --all`. For automation / `npx`, a non-interactive form is available — use it with caution and only after confirming scopes:

```bash
openclaw uninstall --all --yes --non-interactive
npx -y openclaw uninstall --all --yes --non-interactive
```

### Manual Steps (Same Result)

The source page enumerates six manual steps that achieve the same result as `openclaw uninstall`:

1. Stop the gateway service: `openclaw gateway stop`.
2. Uninstall the gateway service (launchd / systemd / schtasks): `openclaw gateway uninstall`.
3. Delete state + config (this is the load-bearing removal of persisted state):

```bash
rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

If you set `OPENCLAW_CONFIG_PATH` to a custom location **outside** the state dir, delete that file too. If you want to keep a workspace inside the state dir, such as `~/.openclaw/workspace`, move it aside before running `rm -rf` or delete state contents selectively.

4. Delete your workspace (optional, removes agent files): `rm -rf ~/.openclaw/workspace`.
5. Remove the CLI install — pick the one you used:

```bash
npm rm -g openclaw
pnpm remove -g openclaw
bun remove -g openclaw
```

6. If you installed the macOS app: `rm -rf /Applications/OpenClaw.app`.

**Notes from the source page.** If you used profiles (`--profile` / `OPENCLAW_PROFILE`), repeat step 3 for **each** state dir (the defaults are `~/.openclaw-<profile>`). In **remote mode**, the state dir lives on the **gateway host**, so run steps 1-4 there too.

## Manual Service Removal (CLI Not Installed)

Use this section when the gateway service keeps running but `openclaw` is missing. The procedure differs per OS service manager.

### macOS (launchd)

The default label is `ai.openclaw.gateway` (or `ai.openclaw.<profile>`; legacy `com.openclaw.*` labels may still exist). Boot the service out and remove its LaunchAgent plist:

```bash
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

If you used a profile, replace the label and plist name with `ai.openclaw.<profile>`. Remove any legacy `com.openclaw.*` plists if present.

### Linux (systemd user unit)

The default unit name is `openclaw-gateway.service` (or `openclaw-gateway-<profile>.service`). Disable and stop the user unit, delete its file, then reload:

```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

### Windows (Scheduled Task)

The default task name is `OpenClaw Gateway` (or `OpenClaw Gateway (<profile>)`); the task script lives under your state dir. Delete the Scheduled Task and remove the launcher script:

```powershell
schtasks /Delete /F /TN "OpenClaw Gateway"
Remove-Item -Force "$env:USERPROFILE\.openclaw\gateway.cmd"
```

If you used a profile, delete the matching task name and `~\.openclaw-<profile>\gateway.cmd`.

## Normal Install vs Source Checkout

The page distinguishes how the CLI was originally installed, because that determines how to remove it.

### Normal install (install.sh / npm / pnpm / bun)

If you used `https://openclaw.ai/install.sh` or `install.ps1`, the CLI was installed with `npm install -g openclaw@latest`. Remove it with `npm rm -g openclaw` (or `pnpm remove -g` / `bun remove -g` if you installed that way) — the same package-manager removal as step 5 of the easy path.

### Source checkout (git clone)

If you run from a repo checkout (`git clone` + `openclaw ...` / `bun run openclaw ...`), the source page prescribes a specific order: (1) **uninstall the gateway service before deleting the repo** — use the easy path above or the manual service removal — then (2) delete the repo directory, and (3) remove state + workspace as shown above. Removing the repo first would strip the CLI you need to cleanly uninstall the still-registered service.

**Source**: OpenClaw documentation — `install/uninstall` (mirror `inbox/openclaw_docs/install/uninstall.md`)
**Last Updated**: 2026-06-22
**Status**: Active
