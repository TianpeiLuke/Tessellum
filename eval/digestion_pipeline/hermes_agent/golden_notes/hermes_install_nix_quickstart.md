---
tags:
  - resource
  - documentation
  - hermes_agent
  - getting_started
  - installation
keywords:
  - nix run hermes agent
  - nix profile install
  - messaging full flake variants
  - non-nixos nix install
  - nix flake closure
  - determinate nix flakes
topics:
  - Hermes Agent
  - Getting Started
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup
access_control_group: ["general"]
---

# Hermes Agent — Nix Install (Any Nix User)

## Overview

This is the **non-NixOS Nix install path** for Hermes Agent: how any Nix user on macOS or Linux gets a working `hermes` binary via `nix run` or `nix profile install`, with no clone, no `pip`, and no venv. Hermes ships a Nix flake whose every Python dependency is a Nix derivation (built by uv2nix) and whose runtime tools (Node.js, git, ripgrep, ffmpeg) are wrapped into the binary's PATH. For non-NixOS users this changes only the **install step** — everything after (`hermes setup`, `hermes gateway install`, config editing) works identically to the [standard installation](hermes_installation.md). Messaging-platform libraries were moved to on-demand installation, which cannot work in Nix's read-only store, so connecting to Discord/Telegram/Slack requires the `#messaging` (or `#full`) flake variant.

## Three Levels of Nix Integration

Hermes Agent's Nix flake offers three integration levels; this note covers the first (the `nix run` / `nix profile install` quick path). The other two are NixOS-only and are documented in sibling notes.

| Level | Who it's for | What you get |
|-------|-------------|--------------|
| **`nix run` / `nix profile install`** | Any Nix user (macOS, Linux) | Pre-built binary with all deps — then use the standard CLI workflow |
| **NixOS module (native)** | NixOS server deployments | Declarative config, hardened systemd service, managed secrets |
| **NixOS module (container)** | Agents that need self-modification | Everything above, plus a persistent Ubuntu container where the agent can `apt`/`pip`/`npm install` |

The NixOS module (native) is covered in [NixOS Module deploy](hermes_install_nixos_module.md); the container level in [NixOS container mode](hermes_nixos_container_mode.md). This note is the entry point all three share.

### What's Different from the Standard Install

The `curl | bash` installer manages Python, Node, and dependencies itself. The Nix flake replaces all of that — every Python dependency is a Nix derivation built by uv2nix, and runtime tools (Node.js, git, ripgrep, ffmpeg) are wrapped into the binary's PATH. There is no runtime pip, no venv activation, no `npm install`.

**For non-NixOS users**, this only changes the install step. Everything after (`hermes setup`, `hermes gateway install`, config editing) works identically to the standard install. (NixOS-module users have a different lifecycle entirely — config in `configuration.nix`, secrets via sops-nix/agenix, a managed systemd unit — see [NixOS Module deploy](hermes_install_nixos_module.md).)

## Prerequisites

- **Nix with flakes enabled** — Determinate Nix (install.determinate.systems) recommended (enables flakes by default).
- **API keys** for the services you want to use (at minimum: an OpenRouter or Anthropic key).

## Quick Start (Any Nix User)

No clone needed. Nix fetches, builds, and runs everything:

```bash
# Run directly (builds on first use, cached after)
nix run github:NousResearch/hermes-agent -- setup
nix run github:NousResearch/hermes-agent -- chat

# Or install persistently
nix profile install github:NousResearch/hermes-agent
hermes setup
hermes chat
```

After `nix profile install`, `hermes`, `hermes-agent`, and `hermes-acp` are on your PATH. From here, the workflow is identical to the [standard installation](hermes_installation.md) — `hermes setup` walks you through provider selection, `hermes gateway install` sets up a launchd (macOS) or systemd user service, and config lives in `~/.hermes/`.

### Building from a Local Clone

If you would rather build the package from a checkout:

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
nix build
./result/bin/hermes setup
```

## Messaging Platforms: `#messaging` / `#full` Variants

The default package **does not include messaging platform libraries** (Discord, Telegram, Slack). They were moved to on-demand installation, which cannot work in Nix's read-only environment. If you plan to connect the agent to one of those platforms, install the `messaging` variant:

```bash
# Messaging platforms only (Discord, Telegram, Slack)
nix profile install github:NousResearch/hermes-agent#messaging

# All optional extras (voice, all providers, all platforms)
nix profile install github:NousResearch/hermes-agent#full
```

The `full` variant adds ~700 MB to the closure. If you only need messaging platforms, `#messaging` adds just ~33 MB. (On the NixOS module, the declarative equivalent is `extraDependencyGroups = [ "messaging" ]` — see [NixOS Module deploy](hermes_install_nixos_module.md).) If a messaging adapter is missing you will see `No adapter available for discord` (or telegram/slack) — the fix is the `#messaging` variant.

## Post-Install Workflow

Because only the install step changes, everything downstream is the standard CLI flow:

- `hermes setup` walks through provider/model selection (`hermes setup --portal` for the Nous Portal one-OAuth path).
- `hermes gateway install` sets up a launchd (macOS) or systemd user service for bot/shared-assistant use.
- Configuration lives in `~/.hermes/` and is edited the same way as on a standard install (see [Configuration](hermes_config_files_precedence.md)).
- Updating uses the Nix toolchain — `nix flake update` then `nix profile upgrade` (or `nix profile rollback`) rather than `hermes update` (see [Updating & uninstalling](hermes_updating_uninstalling.md)).

For declarative, server-grade deployment on NixOS — declarative config, hardened systemd service, managed secrets, declarative MCP servers — graduate to the [NixOS Module deploy](hermes_install_nixos_module.md) and, for self-modifying agents, the [NixOS container mode](hermes_nixos_container_mode.md).

**Source**: `inbox/hermes_agent_docs/getting-started/nix-setup.md` · https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup
**Last Updated**: 2026-06-19
**Status**: Active
