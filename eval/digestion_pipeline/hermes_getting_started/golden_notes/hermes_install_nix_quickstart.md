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

## Related Notes

**Terms**
- [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — the agent being installed; relevance: page's subject.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent category; relevance: framing of what you install.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: post-install `hermes setup` works identically (incl. `--portal` login).
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: standard MCP workflow available after `nix profile install`.
- [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — terminal/runtime backend; relevance: messaging libs moved to on-demand, hence the `#messaging`/`#full` variants.
- [term_llm](../../term_dictionary/term_llm.md) — underlying model; relevance: §Prerequisites need an OpenRouter/Anthropic key.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — provider/model list; relevance: `hermes setup` provider selection post-install.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider adapter; relevance: provider selection identical to the standard install.

**Code-Repos**
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — flake + packaging; relevance: the Nix flake, `nix run`/`profile install`, and `#messaging`/`#full` variants are part of the repo.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — CLI package; relevance: post-install workflow (`hermes setup`/`gateway install`) is identical CLI code.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider adapters; relevance: `hermes setup` provider config works identically post-install.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — messaging adapters; relevance: why messaging libs need the `#messaging` variant in Nix's read-only env.
- [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP client/toolsets; relevance: standard MCP config works after Nix install.

**Snippets**
- [snippet_hermes_agent_setup_hermes_sh](../../code_snippets/snippet_hermes_agent_setup_hermes_sh.md) — installer (non-Nix); relevance: the standard install Nix mirrors.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer step; relevance: post-`nix profile install` setup path.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — `hermes setup`; relevance: §Quick Start "workflow identical after Nix".
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: provider selection identical post-install.
- [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — `hermes model`; relevance: §Prerequisites provider/model selection.
- [snippet_hermes_agent_acp_bootstrap_sh](../../code_snippets/snippet_hermes_agent_acp_bootstrap_sh.md) — ACP bootstrap; relevance: optional extras built on demand under Nix.
- [snippet_hermes_agent_cli_mcp_config](../../code_snippets/snippet_hermes_agent_cli_mcp_config.md) — MCP config; relevance: standard MCP config works after Nix install.
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — `config set`; relevance: config in `~/.hermes/` post-install.
- [snippet_hermes_agent_cli_gateway_dispatch](../../code_snippets/snippet_hermes_agent_cli_gateway_dispatch.md) — gateway dispatch; relevance: why messaging libs need the `#messaging` variant.
- [snippet_hermes_agent_gw_config_load](../../code_snippets/snippet_hermes_agent_gw_config_load.md) — gateway config load; relevance: `#messaging`/`#full` on-demand messaging variants.

**Docs**
- [hermes_installation](hermes_installation.md) — standard install reference; relevance: §Quick Start says the workflow is identical after Nix.
- [hermes_install_nixos_module](hermes_install_nixos_module.md) — sibling NixOS module; relevance: next level up (declarative deploy).
- [hermes_nixos_container_mode](hermes_nixos_container_mode.md) — sibling container mode; relevance: third Nix integration level.
- [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — first-chat quickstart; relevance: post-`nix profile install` first chat.
- [hermes_updating_uninstalling](hermes_updating_uninstalling.md) — update/uninstall; relevance: `nix flake update`/`profile upgrade`/`rollback`.
- [hermes_configuration](hermes_config_files_precedence.md) — config/secrets; relevance: config in `~/.hermes/` post-install.
- [cc_install](../claude_code/cc_install.md) — analogous Claude Code install; relevance: alternative-channel install parallel.
- [cc_advanced_install_and_verification](../claude_code/cc_advanced_install_and_verification.md) — analogous advanced install + verify; relevance: parallels building from a local clone + verify.
- [cc_quickstart](../claude_code/cc_quickstart.md) — analogous quickstart; relevance: post-install first run.
- [cc_enterprise_deployment_options](../claude_code/cc_enterprise_deployment_options.md) — analogous deployment channels; relevance: parallels per-environment install channels (Nix as one).

**Source**: `inbox/hermes_agent_docs/getting-started/nix-setup.md` · https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup
**Last Updated**: 2026-06-19
**Status**: Active
