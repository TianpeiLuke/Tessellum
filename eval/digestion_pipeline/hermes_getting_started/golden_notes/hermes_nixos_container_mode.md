---
tags:
  - resource
  - documentation
  - hermes_agent
  - nixos_container
  - deployment
keywords:
  - nixos container mode
  - persistent ubuntu container
  - self-modifying agent
  - what persists across rebuilds
  - gc root protection
  - container identity hash
topics:
  - Hermes Agent
  - Nix Deployment
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup
access_control_group: ["general"]
---

# Hermes Agent — NixOS Container Mode

## Overview

Container mode is the third Nix integration level: it runs Hermes inside a **persistent Ubuntu container** with the Nix-built binary bind-mounted read-only from the host, so the agent can `apt`/`pip`/`npm install` at runtime and have those installs persist. It is enabled with one line — `services.hermes-agent.container.enable = true` — on the same NixOS module that drives native mode. This note is the **deployment model**: it documents the host↔container mount architecture, the persistence semantics ("what survives what"), GC-root protection, the container options reference, and the container troubleshooting surface. The trade-off versus native mode is mutability for isolation: choose container mode when the agent needs a writable, self-modifying environment; choose [native mode](hermes_install_nixos_module.md) for maximum security and reproducibility.

## Choosing a Deployment Mode

The NixOS module supports two modes, controlled by `container.enable`. This table frames why container mode exists:

| | **Native** (default) | **Container** |
|---|---|---|
| How it runs | Hardened systemd service on the host | Persistent Ubuntu container with `/nix/store` bind-mounted |
| Security | `NoNewPrivileges`, `ProtectSystem=strict`, `PrivateTmp` | Container isolation, runs as unprivileged user inside |
| Agent can self-install packages | No — only tools on the Nix-provided PATH | Yes — `apt`, `pip`, `npm` installs persist across restarts |
| Config surface | Same | Same |
| When to choose | Standard deployments, maximum security, reproducibility | Agent needs runtime package installation, mutable environment, experimental tools |

Enabling it adds one line; the rest of the config is identical:

```nix
{
  services.hermes-agent = {
    enable = true;
    container.enable = true;
    # ... rest of config is identical
  };
}
```

Container mode auto-enables `virtualisation.docker.enable` via `mkDefault`. To use Podman instead, set `container.backend = "podman"` and `virtualisation.docker.enable = false`. When `container.enable = true` and `addToSystemPackages = true`, **every** host `hermes` command transparently `exec`s into the managed container (`hermes chat`, `hermes sessions list`, `hermes version`); set `HERMES_DEV=1` to bypass routing. The NixOS service runs the container as root — Docker users get access via the `docker` group socket, but Podman's rootful containers require passwordless sudo for the runtime binary.

## Container Architecture

When container mode is enabled, hermes runs inside a persistent Ubuntu container with the Nix-built binary bind-mounted read-only from the host:

```
Host                                    Container
────                                    ─────────
/nix/store/...-hermes-agent-0.1.0  ──►  /nix/store/... (ro)
~/.hermes -> /var/lib/hermes/.hermes       (symlink bridge, per hostUsers)
/var/lib/hermes/                    ──►  /data/          (rw)
  ├── current-package -> /nix/store/...    (symlink, updated each rebuild)
  ├── .gc-root -> /nix/store/...           (prevents nix-collect-garbage)
  ├── .container-identity                  (sha256 hash, triggers recreation)
  ├── .hermes/                             (HERMES_HOME)
  │   ├── .env                             (merged from environment + environmentFiles)
  │   ├── config.yaml                      (Nix-generated, deep-merged by activation)
  │   ├── .managed                         (marker file)
  │   ├── .container-mode                  (routing metadata: backend, exec_user, etc.)
  │   ├── state.db, sessions/, memories/   (runtime state)
  │   └── mcp-tokens/                      (OAuth tokens for MCP servers)
  ├── home/                                ──►  /home/hermes    (rw)
  └── workspace/                           (agent working directory)
      ├── SOUL.md                          (from documents option)
      └── (agent-created files)

Container writable layer (apt/pip/npm):   /usr, /usr/local, /tmp
```

The Nix-built binary works inside the Ubuntu container because `/nix/store` is bind-mounted — it brings its own interpreter and all dependencies, so there's no reliance on the container's system libraries. The container entrypoint resolves through a `current-package` symlink: `/data/current-package/bin/hermes gateway run --replace`. On `nixos-rebuild switch`, only the symlink is updated — the container keeps running.

## What Persists Across What

The persistence model is the heart of container mode: bind-mounted state (`/data`, `/home/hermes`) always survives; the writable layer survives everything **except** container recreation.

| Event | Container recreated? | `/data` (state) | `/home/hermes` | Writable layer (`apt`/`pip`/`npm`) |
|---|---|---|---|---|
| `systemctl restart hermes-agent` | No | Persists | Persists | Persists |
| `nixos-rebuild switch` (code change) | No (symlink updated) | Persists | Persists | Persists |
| Host reboot | No | Persists | Persists | Persists |
| `nix-collect-garbage` | No (GC root) | Persists | Persists | Persists |
| Image change (`container.image`) | **Yes** | Persists | Persists | **Lost** |
| Volume/options change | **Yes** | Persists | Persists | **Lost** |
| `environment`/`environmentFiles` change | No | Persists | Persists | Persists |

The container is only recreated when its **identity hash** changes. The hash covers: schema version, image, `extraVolumes`, `extraOptions`, and the entrypoint script. Changes to environment variables, settings, documents, or the hermes package itself do **not** trigger recreation.

When the identity hash changes (image upgrade, new volumes, new container options), the container is destroyed and recreated from a fresh pull of `container.image`. Any `apt install`, `pip install`, or `npm install` packages in the writable layer are **lost** — state in `/data` and `/home/hermes` is preserved because they are bind mounts. If the agent relies on specific packages, bake them into a custom image (`container.image = "my-registry/hermes-base:latest"`) or script their installation in the agent's `SOUL.md`.

## GC Root Protection

The `preStart` script creates a GC root at `${stateDir}/.gc-root` pointing to the current hermes package. This prevents `nix-collect-garbage` from removing the running binary. If the GC root somehow breaks, restarting the service recreates it.

## Directory Layout (Container Mode)

The container mounts the same on-disk layout as native mode (`/var/lib/hermes` is `0750 hermes:hermes`) into the container:

| Container path | Host path | Mode | Notes |
|---|---|---|---|
| `/nix/store` | `/nix/store` | `ro` | Hermes binary + all Nix deps |
| `/data` | `/var/lib/hermes` | `rw` | All state, config, workspace |
| `/home/hermes` | `${stateDir}/home` | `rw` | Persistent agent home — `pip install --user`, tool caches |
| `/usr`, `/usr/local`, `/tmp` | (writable layer) | `rw` | `apt`/`pip`/`npm` installs — persists across restarts, lost on recreation |

## Options Reference (Container)

The container-specific module options (full module reference is in [the NixOS module note](hermes_install_nixos_module.md)):

| Option | Type | Default | Description |
|---|---|---|---|
| `container.enable` | `bool` | `false` | Enable OCI container mode |
| `container.backend` | `enum ["docker" "podman"]` | `"docker"` | Container runtime |
| `container.image` | `str` | `"ubuntu:24.04"` | Base image (pulled at runtime) |
| `container.extraVolumes` | `listOf str` | `[]` | Extra volume mounts (`host:container:mode`) |
| `container.extraOptions` | `listOf str` | `[]` | Extra args passed to `docker create` |
| `container.hostUsers` | `listOf str` | `[]` | Interactive users who get a `~/.hermes` symlink to the service stateDir and are auto-added to the `hermes` group |

## Updating

In container mode, the `current-package` symlink is updated and the agent picks up the new binary on restart — **no container recreation, no loss of installed packages**:

```bash
# Update the flake input (run from the directory containing flake.nix)
cd /etc/nixos && nix flake update hermes-agent

# Rebuild
sudo nixos-rebuild switch
```

## Troubleshooting

All `docker` commands below work the same with `podman` — substitute accordingly if `container.backend = "podman"`. Inspect a running container and force a fresh writable layer:

```bash
# Inspect the running container
docker ps -a --filter name=hermes-agent
docker exec -it hermes-agent bash
docker exec hermes-agent readlink /data/current-package
docker exec hermes-agent cat /data/.container-identity

# Force container recreation (reset the writable layer to a fresh Ubuntu)
sudo systemctl stop hermes-agent
docker rm -f hermes-agent
sudo rm /var/lib/hermes/.container-identity
sudo systemctl start hermes-agent
```

Verify the GC root protects the running binary with `nix-store --query --roots $(docker exec hermes-agent readlink /data/current-package)`. Common container-mode issues:

| Symptom | Cause | Fix |
|---|---|---|
| Container recreated unexpectedly | `extraVolumes`, `extraOptions`, or `image` changed | Expected — writable layer resets. Reinstall packages or use a custom image |
| `hermes version` shows old version | Container not restarted | `systemctl restart hermes-agent` |
| `nix-collect-garbage` removed hermes | GC root missing | Restart the service (preStart recreates the GC root) |
| `no container with name or ID "hermes-agent"` (Podman) | Podman rootful container not visible to regular user | Add passwordless sudo for podman |
| `unable to find user hermes` | Container still starting (entrypoint hasn't created user yet) | Wait a few seconds and retry — the CLI retries automatically |

## Related Notes

**Terms**:
- [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — container isolation; relevance: persistent Ubuntu container as the terminal/runtime backend.
- [term_docker](../../term_dictionary/term_docker.md) — Docker/Podman runtime; relevance: `container.backend = docker|podman`, root-vs-rootful access.
- [term_hermes_agent](../../term_dictionary/term_hermes_agent.md) — agent inside container; relevance: the bind-mounted Nix binary runs the agent.
- [term_self_evolving_agent](../../term_dictionary/term_self_evolving_agent.md) — self-modifying agent; relevance: container mode exists so the agent can `apt`/`pip`/`npm install` at runtime.
- [term_regular_checkpointing](../../term_dictionary/term_regular_checkpointing.md) — persistence semantics; relevance: §What Persists Across What table + GC-root protection.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent category; relevance: framing.
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — `/data` state; relevance: sessions/memories persist in the `/data` bind mount across rebuilds.
- [term_iframe_sandbox](../../term_dictionary/term_iframe_sandbox.md) — isolation model; relevance: contrast with native hardened-systemd isolation in §Deployment Mode table.

**Code-Repos**:
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — flake/module + container entrypoint; relevance: container identity hash, `/data/current-package` symlink, GC-root preStart script.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — runtime startup; relevance: the bound Nix binary brings its own interpreter to bootstrap inside Ubuntu.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway service; relevance: container entrypoint runs `hermes gateway run --replace`.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — container-aware CLI; relevance: host `hermes` commands transparently `exec` into the container.
- [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP token store; relevance: `mcp-tokens/` persist in `/data` across recreation.

**Snippets**:
- [snippet_hermes_agent_setup_hermes_sh](../../code_snippets/snippet_hermes_agent_setup_hermes_sh.md) — installer; relevance: container entrypoint runs the bound Nix binary's install/bootstrap.
- [snippet_hermes_agent_core_bootstrap_utf8](../../code_snippets/snippet_hermes_agent_core_bootstrap_utf8.md) — startup bootstrap; relevance: bound Nix binary brings its own interpreter to bootstrap inside Ubuntu.
- [snippet_hermes_agent_cli_config_schema](../../code_snippets/snippet_hermes_agent_cli_config_schema.md) — config schema; relevance: §Options Reference container settings.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base; relevance: provider runtime inside the container.
- [snippet_hermes_agent_acp_server_module_helpers](../../code_snippets/snippet_hermes_agent_acp_server_module_helpers.md) — server helpers; relevance: agent process running in the persistent container.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — installer step; relevance: container identity hash / `/data/current-package` symlink.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — logging setup; relevance: container runtime diagnostics.
- [snippet_hermes_agent_cron_tick](../../code_snippets/snippet_hermes_agent_cron_tick.md) — cron tick; relevance: scheduled work persisting via `/data` across recreation.
- [snippet_hermes_agent_gw_start_gateway_main](../../code_snippets/snippet_hermes_agent_gw_start_gateway_main.md) — gateway main; relevance: container entrypoint `hermes gateway run --replace`.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker/Podman backend; relevance: `container.backend = docker|podman` isolation runtime.

**Docs**:
- [hermes_install_nixos_module](hermes_install_nixos_module.md) — sibling module; relevance: container mode is `container.enable` on that module.
- [hermes_install_nix_quickstart](hermes_install_nix_quickstart.md) — sibling Nix install; relevance: the base Nix integration.
- [hermes_updating_uninstalling](hermes_updating_uninstalling.md) — update; relevance: §Updating (symlink update, no recreation, package loss rules).
- [hermes_quickstart_first_chat](hermes_quickstart_first_chat.md) — first chat; relevance: chatting against a container deployment.
- [hermes_docker](hermes_docker_run_modes.md) — Docker backend; relevance: the container runtime concept link-out.
- [hermes_architecture](hermes_architecture.md) — architecture; relevance: native-vs-container runtime layout.
- [hermes_security](hermes_security_isolation_credentials.md) — security; relevance: container isolation vs hardened-systemd trade-off.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — analogous container runtime; relevance: parallels persistent-container deployment model.
- [cc_devcontainer_hardening](../claude_code/cc_devcontainer_hardening.md) — analogous hardened container; relevance: parallels native hardened-systemd vs container security.
- [cc_execution_environments](../claude_code/cc_execution_environments.md) — analogous execution env; relevance: parallels self-modifying mutable-environment choice.

**Source**: `inbox/hermes_agent_docs/getting-started/nix-setup.md` · https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup
**Last Updated**: 2026-06-19
**Status**: Active
