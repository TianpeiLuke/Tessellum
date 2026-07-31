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

**Source**: `inbox/hermes_agent_docs/getting-started/nix-setup.md` · https://hermes-agent.nousresearch.com/docs/getting-started/nix-setup
**Last Updated**: 2026-06-19
**Status**: Active
