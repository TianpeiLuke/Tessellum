---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - nix
keywords:
  - openclaw nix install
  - nix-openclaw home manager module
  - openclaw_nix_mode declarative install
  - home-manager switch rollback
  - openclaw immutable openclaw.json
  - openclaw_state_dir openclaw_config_path
  - nix_profiles service path discovery
  - openclaw launchd systemd nix mode
topics:
  - OpenClaw
  - Nix Install
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/nix
access_control_group: ["general"]
---

# OpenClaw — Declarative Install with Nix

## Overview

This note is the procedure for installing OpenClaw declaratively with Nix via the first-party, batteries-included **[nix-openclaw](https://github.com/openclaw/nix-openclaw)** Home Manager module, mirroring the `install/nix` source page. It covers what the Nix install gives you, the five-step flake quick start, and the Nix-mode runtime behavior that turns on once the module is active — what changes under Nix mode, the config/state path environment variables, and how the gateway service discovers Nix-profile binaries. The page itself is a quick overview; per its own `<Info>` note, the `nix-openclaw` repo is the source of truth for Nix installation, so the full module options live there and are linked from References.

## What you get

The Nix install path is for operators who want reproducible, rollback-able installs, who already use Nix / NixOS / Home Manager, or who want everything pinned and managed declaratively. Installing via the `nix-openclaw` Home Manager module gives you:

- Gateway + macOS app + tools (whisper, spotify, cameras) — all pinned.
- A launchd service that survives reboots.
- A plugin system with declarative config.
- Instant rollback via `home-manager switch --rollback`.

## Quick start

The page presents installation as five ordered steps:

1. **Install Determinate Nix** — if Nix is not already installed, follow the [Determinate Nix installer](https://github.com/DeterminateSystems/nix-installer) instructions.
2. **Create a local flake** — use the agent-first template from the `nix-openclaw` repo, copying `templates/agent-first/flake.nix` from that repo into a local directory:

```bash
mkdir -p ~/code/openclaw-local
# Copy templates/agent-first/flake.nix from the nix-openclaw repo
```

3. **Configure secrets** — set up your messaging bot token and model provider API key. Plain files at `~/.secrets/` work fine.
4. **Fill in template placeholders and switch** — after filling in the template placeholders, apply the configuration:

```bash
home-manager switch
```

5. **Verify** — confirm the launchd service is running and your bot responds to messages.

See the [nix-openclaw README](https://github.com/openclaw/nix-openclaw) for full module options and examples.

## Nix-mode runtime behavior

When `OPENCLAW_NIX_MODE=1` is set (automatic with `nix-openclaw`), OpenClaw enters a deterministic mode for Nix-managed installs. Other Nix packages can set the same mode; `nix-openclaw` is the first-party reference. You can also set it manually:

```bash
export OPENCLAW_NIX_MODE=1
```

On macOS, the GUI app does not automatically inherit shell environment variables. Enable Nix mode via `defaults` instead:

```bash
defaults write ai.openclaw.mac openclaw.nixMode -bool true
```

### What changes in Nix mode

When Nix mode is active, the runtime behavior changes as follows:

- Auto-install and self-mutation flows are disabled.
- `openclaw.json` is treated as immutable. Startup-derived defaults stay runtime-only, and config writers such as setup, onboarding, mutating `openclaw update`, plugin install/update/uninstall/enable, `doctor --fix`, `doctor --generate-gateway-token`, and `openclaw config set` refuse to edit the file.
- Agents should edit the Nix source instead. For `nix-openclaw`, use the agent-first [Quick Start](https://github.com/openclaw/nix-openclaw#quick-start) and set config under `programs.openclaw.config` or `instances.<name>.config`.
- Missing dependencies surface Nix-specific remediation messages.
- The UI surfaces a read-only Nix mode banner.

### Config and state paths

OpenClaw reads JSON5 config from `OPENCLAW_CONFIG_PATH` and stores mutable data in `OPENCLAW_STATE_DIR`. When running under Nix, set these explicitly to Nix-managed locations so runtime state and config stay out of the immutable store. The defaults are:

| Variable | Default |
| --- | --- |
| `OPENCLAW_HOME` | `HOME` / `USERPROFILE` / `os.homedir()` |
| `OPENCLAW_STATE_DIR` | `~/.openclaw` |
| `OPENCLAW_CONFIG_PATH` | `$OPENCLAW_STATE_DIR/openclaw.json` |

### Service PATH discovery

The launchd/systemd gateway service auto-discovers Nix-profile binaries so that plugins and tools that shell out to `nix`-installed executables work without manual PATH setup:

- When `NIX_PROFILES` is set, every entry is added to the service PATH in right-to-left precedence (matches Nix shell precedence — rightmost wins).
- When `NIX_PROFILES` is unset, `~/.nix-profile/bin` is added as a fallback.

This applies to both macOS launchd and Linux systemd service environments.

**Source**: OpenClaw documentation — `install/nix` (mirror `inbox/openclaw_docs/install/nix.md`)
**Last Updated**: 2026-06-22
**Status**: Active
