---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - updating
keywords:
  - openclaw update command
  - update channel beta dev stable
  - switch npm git install
  - re-run installer recovery
  - manual npm pnpm bun update
  - staged temp-prefix swap eacces
  - post-update doctor restart health
  - rollback pin version commit
topics:
  - OpenClaw
  - Install
  - Updating
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/updating
access_control_group: ["general"]
---

# OpenClaw — Updating Safely (Update Command, Channel Switch, Manual Update, Rollback)

## Overview

This note is the hands-on **procedure** for updating an existing OpenClaw install and recovering from a bad update, mirroring the `install/updating` source page (minus its Auto-updater configuration model, which is captured separately in `oc_install_updating_auto_updater`). It covers the recommended `openclaw update` command (install-type detection, channel/version targeting, dry-run/json diagnostics), switching an install between npm and git, re-running the installer for recovery, supervised manual `npm`/`pnpm`/`bun` updates (stop the Gateway first, the staged temp-prefix swap, EACCES recovery), the post-update doctor/restart/verify sequence, and rollback by pinning a version or commit. Throughout, the updater preserves your state, config, credentials, and workspace in `~/.openclaw` — only the OpenClaw code install changes.

## Recommended: `openclaw update`

The fastest way to update is to run `openclaw update` — it detects your install type (npm or git), fetches the latest version, runs `openclaw doctor`, and restarts the gateway.

To switch channels or target a specific version:

```bash
openclaw update --channel beta
openclaw update --channel dev
openclaw update --dry-run   # preview without applying
```

`openclaw update` does **not** accept `--verbose`. For update diagnostics, use `--dry-run` to preview the planned actions, `--json` for structured results, or `openclaw update status --json` to inspect channel and availability state. The installer has its own `--verbose` flag, but that flag is not part of `openclaw update`.

`--channel beta` prefers beta, but the runtime falls back to stable/latest when the beta tag is missing or older than the latest stable release. Use `--tag beta` if you want the raw npm beta dist-tag for a one-off package update. Use `--channel dev` for a persistent moving GitHub `main` checkout. For package updates, `--tag main` maps to `github:openclaw/openclaw#main` for one run, and GitHub/git source specs are packed into a temporary tarball before the staged npm install. For managed plugins, beta-channel fallback is a warning: the core update can still succeed while a plugin uses its recorded default/latest release because no plugin beta is available. See Development channels (`/install/development-channels`) for channel semantics.

## Switch between npm and git installs

Use channels when you want to change the install type. The updater keeps your state, config, credentials, and workspace in `~/.openclaw`; it only changes which OpenClaw code install the CLI and gateway use.

```bash
# npm package install -> editable git checkout
openclaw update --channel dev

# git checkout -> npm package install
openclaw update --channel stable
```

Run with `--dry-run` first to preview the exact install-mode switch (`openclaw update --channel dev --dry-run` or `openclaw update --channel stable --dry-run`). The `dev` channel ensures a git checkout, builds it, and installs the global CLI from that checkout. The `stable` and `beta` channels use package installs. If the gateway is already installed, `openclaw update` refreshes the service metadata and restarts it unless you pass `--no-restart`.

For package installs with a managed Gateway service, `openclaw update` targets the package root used by that service. If the shell `openclaw` command comes from a different install, the updater prints both roots and the managed service Node path. The package update uses the package manager that owns the service root and checks the managed service Node against the target release engine before replacing the package.

## Alternative: re-run the installer

Re-run the installer with `curl -fsSL https://openclaw.ai/install.sh | bash`. Add `--no-onboard` to skip onboarding. To force a specific install type through the installer, pass `--install-method git --no-onboard` or `--install-method npm --no-onboard`. If `openclaw update` fails after the npm package install phase, re-run the installer: the installer does not call the old updater; it runs the global package install directly and can recover a partially updated npm install — for example `curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method npm`. To pin the recovery to a specific version or dist-tag, add `--version`: `curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method npm --version <version-or-dist-tag>`.

## Alternative: manual npm, pnpm, or bun

The base manual command is `npm i -g openclaw@latest`. Prefer `openclaw update` for supervised installs because it can coordinate the package swap with the running Gateway service. If you update manually on a supervised install, **stop the managed Gateway before the package manager starts** — package managers replace files in place, and a running Gateway can otherwise try to load core or plugin files while the package tree is temporarily half-swapped. Restart the Gateway after the package manager finishes so the service picks up the new install.

For a root-owned Linux system-global install, if `openclaw update` fails with `EACCES` and you recover with system npm, keep the Gateway stopped through the manual package replacement. Use the same `openclaw` profile flags or environment you normally use for that Gateway. Replace `/usr/bin/npm` with the system npm that owns the root-owned global prefix on your host:

```bash
openclaw gateway stop
sudo /usr/bin/npm i -g openclaw@latest
openclaw gateway install --force
openclaw gateway restart
```

Then verify the service:

```bash
openclaw --version
curl -fsS http://127.0.0.1:18789/readyz
openclaw plugins list --json
openclaw gateway status --deep --json
openclaw doctor --lint --json
```

When `openclaw update` manages a global npm install, it installs the target into a temporary npm prefix first, verifies the packaged `dist` inventory, then swaps the clean package tree into the real global prefix. That avoids npm overlaying a new package onto stale files from the old package. If the install command fails, OpenClaw retries once with `--omit=optional`. That retry helps hosts where native optional dependencies cannot compile, while keeping the original failure visible if the fallback also fails. OpenClaw-managed npm update and plugin-update commands also clear npm `min-release-age` quarantine for the child npm process. npm may report that policy as a derived `before` cutoff; both are useful for general supply-chain quarantine policies, but an explicit OpenClaw update means "install the selected OpenClaw release now." For other package managers the equivalents are `pnpm add -g openclaw@latest` and `bun add -g openclaw@latest`.

### Advanced npm install topics

**Read-only package tree.** OpenClaw treats packaged global installs as read-only at runtime, even when the global package directory is writable by the current user. Plugin package installs live in OpenClaw-owned npm/git roots under the user config directory, and Gateway startup does not mutate the OpenClaw package tree. Some Linux npm setups install global packages under root-owned directories such as `/usr/lib/node_modules/openclaw`. OpenClaw supports that layout because plugin install/update commands write outside that global package directory.

**Hardened systemd units.** Give OpenClaw write access to its config/state roots so explicit plugin installs, plugin updates, and doctor cleanup can persist their changes — set `ReadWritePaths=/var/lib/openclaw /home/openclaw/.openclaw /tmp` in the unit.

**Disk-space preflight.** Before package updates and explicit plugin installs, OpenClaw tries a best-effort disk-space check for the target volume. Low space produces a warning with the checked path, but does not block the update because filesystem quotas, snapshots, and network volumes can change after the check. The actual package-manager install and post-install verification remain authoritative.

## After updating

Run the three post-update steps in order. First run `openclaw doctor` — it migrates config, audits DM policies, and checks gateway health (details: Doctor, `/gateway/doctor`). Then restart the gateway with `openclaw gateway restart`, and verify health with `openclaw health`.

## Rollback

**Pin a version (npm).** `npm view openclaw version` shows the current published version; pin the global package to a known-good version, then re-run doctor and restart:

```bash
npm i -g openclaw@<version>
openclaw doctor
openclaw gateway restart
```

**Pin a commit (source).** For a git/source checkout, fetch and check out a known-good commit, rebuild, and restart the gateway:

```bash
git fetch origin
git checkout "$(git rev-list -n 1 --before=\"2026-01-01\" origin/main)"
pnpm install && pnpm build
openclaw gateway restart
```

To return to latest: `git checkout main && git pull`.

## If you are stuck

- Run `openclaw doctor` again and read the output carefully.
- For `openclaw update --channel dev` on source checkouts, the updater auto-bootstraps `pnpm` when needed. If you see a pnpm/corepack bootstrap error, install `pnpm` manually (or re-enable `corepack`) and rerun the update.
- Check: Troubleshooting (`/gateway/troubleshooting`).
- Ask in Discord: https://discord.gg/clawd

**Source**: OpenClaw documentation — `install/updating` (mirror `inbox/openclaw_docs/install/updating.md`)
**Last Updated**: 2026-06-22
**Status**: Active
