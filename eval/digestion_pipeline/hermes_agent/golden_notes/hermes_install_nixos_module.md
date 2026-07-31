---
tags:
  - resource
  - documentation
  - hermes_agent
  - nix_install
  - deployment
keywords:
  - nixos module
  - declarative settings
  - secrets management sops-nix agenix
  - mcp servers declarative
  - oauth seeding authfile
  - hermes-agent nixos service
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

# Hermes Agent — NixOS Module (Declarative Deploy)

## Overview

The NixOS module is the declarative deployment path for Hermes Agent on NixOS servers: the flake exports `nixosModules.default`, a full NixOS service module that manages user creation, directories, config generation, secrets, documents, and service lifecycle. Unlike the non-NixOS `nix profile install` tier — where `hermes setup`/config editing work normally — under the module the entire lifecycle is different: configuration lives in `configuration.nix`, secrets go through sops-nix/agenix, the gateway is a systemd unit, and CLI config commands are blocked to prevent drift. This note covers the native (hardened systemd) declarative deployment surface: module input, declarative `settings`, secrets, OAuth seeding, declarative `mcpServers`, and declarative plugins. The container deployment model (`container.enable`), Managed Mode blocking, the Options Reference, updating, and troubleshooting are documented in [hermes_nixos_container_mode](hermes_nixos_container_mode.md); the simpler non-NixOS tier in [hermes_install_nix_quickstart](hermes_install_nix_quickstart.md).

## NixOS Module — Add the Flake Input

The flake exports `nixosModules.default`. Add it as an input and include the module plus your `configuration.nix` in the system's module list. The module requires NixOS; non-NixOS systems use `nix profile install` and the standard CLI workflow instead.

```nix
# /etc/nixos/flake.nix (or your system flake)
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    hermes-agent.url = "github:NousResearch/hermes-agent";
  };

  outputs = { nixpkgs, hermes-agent, ... }: {
    nixosConfigurations.your-host = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        hermes-agent.nixosModules.default
        ./configuration.nix
      ];
    };
  };
}
```

### Minimal Configuration

```nix
# configuration.nix
{ config, ... }: {
  services.hermes-agent = {
    enable = true;
    settings.model.default = "anthropic/claude-sonnet-4";
    environmentFiles = [ config.sops.secrets."hermes-env".path ];
    addToSystemPackages = true;
  };
}
```

`nixos-rebuild switch` then creates the `hermes` user, generates `config.yaml`, wires up secrets, and starts the gateway — a long-running service that connects the agent to messaging platforms (Telegram, Discord, etc.) and listens for incoming messages. `addToSystemPackages = true` does two things: it puts the `hermes` CLI on the system PATH **and** sets `HERMES_HOME` system-wide, so the interactive CLI shares state (sessions, skills, cron) with the gateway service. Without it, running `hermes` in your shell creates a separate `~/.hermes/` directory. After rebuild, verify with `systemctl status hermes-agent`, `journalctl -u hermes-agent -f`, and (if `addToSystemPackages`) `hermes version` / `hermes config`.

The source notes a `container.enable` deployment mode toggle on this same module and a "Choosing a Deployment Mode" comparison (native hardened systemd vs persistent Ubuntu container); the container mode, its architecture, and the deployment-mode trade-off are covered in [hermes_nixos_container_mode](hermes_nixos_container_mode.md).

## Configuration — Declarative Settings

The `settings` option accepts an arbitrary attrset that is rendered as `config.yaml`. It supports deep merging across multiple module definitions (via `lib.recursiveUpdate`), so you can split config across files; both are deep-merged at evaluation time.

```nix
# base.nix
services.hermes-agent.settings = {
  model.default = "anthropic/claude-sonnet-4";
  toolsets = [ "all" ];
  terminal = { backend = "local"; timeout = 180; };
};

# personality.nix
services.hermes-agent.settings = {
  display = { compact = false; personality = "kawaii"; };
  memory = { memory_enabled = true; user_profile_enabled = true; };
};
```

Nix-declared keys always win over keys in an existing `config.yaml` on disk, but **user-added keys that Nix doesn't touch are preserved** — so keys the agent or a manual edit adds (e.g., `skills.disabled`, `streaming.enabled`) survive `nixos-rebuild switch`. `settings.model.default` uses the identifier your provider expects: with OpenRouter (the default) these look like `"anthropic/claude-sonnet-4"`; using a provider directly sets `settings.model.base_url` and uses their native model IDs. Run `nix build .#configKeys && cat result` to list every leaf config key from Python's `DEFAULT_CONFIG`; an existing `config.yaml` maps 1:1 into the `settings` attrset.

**Escape hatch — bring your own config:** `services.hermes-agent.configFile = /etc/hermes/config.yaml;` bypasses `settings` entirely (no merge, no generation) and copies the file as-is to `$HERMES_HOME/config.yaml` on each activation. A Customization Cheatsheet in the source maps common goals to options (`settings.model.default`, `environmentFiles`, `mcpServers.<name>`, `extraDependencyGroups`, `extraPackages`, `package`, `stateDir`, `workingDirectory`); the per-option types/defaults live in the Options Reference (see [hermes_nixos_container_mode](hermes_nixos_container_mode.md)).

The `documents` option installs files into the agent's `workingDirectory` (its workspace) on every rebuild; values are inline strings or path references. Hermes loads by convention — `USER.md` is context about the user — and the primary persona `SOUL.md` is loaded separately from `$HERMES_HOME/SOUL.md` (`${services.hermes-agent.stateDir}/.hermes/SOUL.md`), so putting `SOUL.md` in `documents` only creates a workspace file, not the main persona.

## Secrets Management (sops-nix / agenix)

**Never put API keys in `settings` or `environment`** — values in Nix expressions end up in `/nix/store`, which is world-readable. Always use `environmentFiles` with a secrets manager. Both `environment` (non-secret vars) and `environmentFiles` (secret files) are merged into `$HERMES_HOME/.env` at activation time; Hermes reads this file on every startup, so changes take effect with `systemctl restart hermes-agent` — no container recreation needed.

```nix
# sops-nix
{
  sops = {
    defaultSopsFile = ./secrets/hermes.yaml;
    age.keyFile = "/home/user/.config/sops/age/keys.txt";
    secrets."hermes-env" = { format = "yaml"; };
  };
  services.hermes-agent.environmentFiles = [ config.sops.secrets."hermes-env".path ];
}

# agenix
{
  age.secrets.hermes-env.file = ./secrets/hermes-env.age;
  services.hermes-agent.environmentFiles = [ config.age.secrets.hermes-env.path ];
}
```

The decrypted secrets file holds key=value lines (e.g., `OPENROUTER_API_KEY=sk-or-...`, `TELEGRAM_BOT_TOKEN=...`, `ANTHROPIC_API_KEY=sk-ant-...`). Without a secrets manager yet, a plain non-world-readable file works as a starting point: `echo "OPENROUTER_API_KEY=sk-or-your-key" | sudo install -m 0600 -o hermes /dev/stdin /var/lib/hermes/env` then point `environmentFiles` at it.

### OAuth / Auth Seeding

For platforms requiring OAuth (e.g., Discord), `authFile` seeds credentials on first deploy — e.g. `services.hermes-agent.authFile = config.sops.secrets."hermes/auth.json".path;`. The file is only copied if `auth.json` doesn't already exist (unless `authFileForceOverwrite = true`, which overwrites it on every activation); runtime OAuth token refreshes are written to the state directory and preserved across rebuilds.

## MCP Servers (Declarative)

The `mcpServers` option declaratively configures Model Context Protocol servers, merged into `settings.mcp_servers`. Each server uses either **stdio** (local command) or **HTTP** (remote URL) transport. For HTTP servers, `auth = "oauth"` enables the full PKCE flow (metadata discovery, dynamic client registration, token exchange, automatic refresh). Environment variables in `env`/`headers` values are resolved from `$HERMES_HOME/.env` at runtime — inject secrets via `environmentFiles`, never inline tokens. OAuth tokens are stored in `$HERMES_HOME/mcp-tokens/<server-name>.json` and persist across restarts and rebuilds.

```nix
{
  services.hermes-agent.mcpServers = {
    # stdio (local command)
    filesystem = {
      command = "npx";
      args = [ "-y" "@modelcontextprotocol/server-filesystem" "/data/workspace" ];
    };
    # HTTP with OAuth 2.1 PKCE
    my-oauth-server = {
      url = "https://mcp.example.com/mcp";
      auth = "oauth";
    };
    # Sampling: server-initiated LLM requests
    analysis = {
      command = "npx";
      args = [ "-y" "analysis-server" ];
      sampling = { enabled = true; model = "google/gemini-3-flash"; max_tokens_cap = 4096; timeout = 30; max_rpm = 10; };
    };
  };
}
```

HTTP transport also supports `headers` (e.g., `Authorization = "Bearer \${MCP_REMOTE_API_KEY}"`) and a `timeout`. The first OAuth authorization needs a browser-based consent flow; on headless servers Hermes prints the authorization URL to stdout/logs. Bootstrap options: run the flow once via `docker exec` (container) or `sudo -u hermes` (native), or pre-seed tokens by completing the flow on a workstation and copying `~/.hermes/mcp-tokens/<server>{,.client}.json` (then `chown hermes:hermes`, `chmod 0600`).

## Plugins (Declarative)

The module supports declarative plugin installation — no imperative `hermes plugins install`. Three mechanisms: **`extraPlugins`** symlinks directory plugins (source tree with `plugin.yaml` + `__init__.py`) into `$HERMES_HOME/plugins/` at activation, discovered by Hermes's normal directory scan. **`extraPythonPackages`** adds pip-packaged entry-point plugins (registered via `[project.entry-points."hermes_agent.plugins"]`, built with `python312Packages`); their `site-packages` is added to PYTHONPATH and `importlib.metadata` discovers the entry point at session start. **`extraDependencyGroups`** includes `pyproject.toml` optional extras (e.g., `messaging`, `honcho`, `hindsight`, `voice`) in the sealed venv at build time, resolved by uv with no PYTHONPATH patching or collision risk — required because runtime install into the read-only store is impossible on Nix.

```nix
services.hermes-agent = {
  extraPlugins = [ (pkgs.fetchFromGitHub { owner = "stephenschoettler"; repo = "hermes-lcm"; rev = "v0.7.0"; hash = "sha256-..."; }) ];
  extraDependencyGroups = [ "messaging" ];   # Discord, Telegram, Slack
  settings.plugins.enabled = [ "hermes-lcm" "rtk-rewrite" ];
};
```

Plugins still need to be enabled in `config.yaml` via `settings.plugins.enabled`. A build-time collision check fails `nixos-rebuild` with a clear error if a plugin shadows a core hermes dependency. To add a system binary the agent needs, use `extraPackages` (e.g., `[ pkgs.pandoc pkgs.imagemagick ]`); a directory plugin with third-party Python deps needs `extraPlugins` + `extraPythonPackages` (+ `extraPackages` for any system binary). External flakes can override the package directly via `hermes-agent.overlays.default` (`pkgs.hermes-agent.override { ... }`).

## Development — Dev Shell

The flake provides a development shell with Python 3.12, uv, Node.js 22, and all runtime tools (ripgrep, git, openssh, ffmpeg) on PATH; `nix develop` installs deps into `.venv` on first entry, with stamp-file optimization making re-entry near-instant if deps haven't changed. The included `.envrc` activates the dev shell automatically after a one-time `direnv allow`. `nix flake check` runs build-time verification (also in CI): individual checks include `package-contents`, `entry-points-sync` (pyproject.toml ↔ Nix package sync), `cli-commands`, `managed-guard` (HERMES_MANAGED blocks mutation), `bundled-skills`, and `config-roundtrip` (7 merge scenarios incl. user-key preservation and MCP additive merge).

**Source**: `inbox/hermes_agent_docs/getting-started/nix-setup.md` · https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup
**Last Updated**: 2026-06-19
**Status**: Active
