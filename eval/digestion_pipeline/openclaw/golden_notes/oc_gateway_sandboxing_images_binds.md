---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - sandboxing
keywords:
  - openclaw sandbox docker image
  - docker.binds custom bind mounts
  - bind security blocked sources
  - openclaw-sandbox bookworm-slim image
  - setupCommand one-time container setup
  - sandbox-setup.sh build image
  - sandbox docker network none
topics:
  - OpenClaw
  - Sandboxing Backends
language: markdown
date of note: 2026-06-23
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/sandboxing
access_control_group: ["general"]
---

# OpenClaw — Sandbox Images, Bind Mounts & setupCommand

## Overview

This note is the **operational procedure** for a Docker sandbox backend, mirroring the image/binds/setup sections of the `gateway/sandboxing` source page: adding custom bind mounts (with the bind-security rules), building the sandbox Docker image, configuring network, running a one-time `setupCommand`, and a minimal enable example. It is split from the backend-selection + workspace-access procedure in the sibling [oc_gateway_sandboxing_backends](oc_gateway_sandboxing_backends.md); the conceptual model is in [oc_gateway_sandboxing_model](oc_gateway_sandboxing_model.md). These settings apply to the Docker backend (`sandbox.docker.*` knobs do not apply to the SSH/OpenShell backends).

## Custom bind mounts

`agents.defaults.sandbox.docker.binds` mounts additional host directories into the container in the format `host:container:mode` (e.g., `"/home/user/source:/source:rw"`). Global and per-agent binds are **merged** (not replaced), but under `scope: "shared"` per-agent binds are ignored. `agents.defaults.sandbox.browser.binds` mounts directories into the **sandbox browser** container only: when set (including `[]`) it replaces `docker.binds` for the browser container; when omitted, the browser falls back to `docker.binds` (backwards compatible).

```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          binds: ["/home/user/source:/source:ro", "/var/data/myapp:/data:ro"],
        },
      },
    },
    list: [
      {
        id: "build",
        sandbox: {
          docker: {
            binds: ["/mnt/cache:/cache:rw"],
          },
        },
      },
    ],
  },
}
```

**Bind security** rules: binds bypass the sandbox filesystem and expose host paths with whatever mode you set (`:ro` or `:rw`). OpenClaw blocks dangerous bind sources (e.g. `docker.sock`, `/etc`, `/proc`, `/sys`, `/dev`, and parent mounts exposing them) and common home-directory credential roots (`~/.aws`, `~/.cargo`, `~/.config`, `~/.docker`, `~/.gnupg`, `~/.netrc`, `~/.npm`, `~/.ssh`). Validation is not just string matching — OpenClaw normalizes the source path, then resolves it through the deepest existing ancestor before re-checking blocked paths and allowed roots, so symlink-parent escapes fail closed even when the final leaf does not exist yet (e.g. `/workspace/run-link/new-file` resolves as `/var/run/...` if `run-link` points there); allowed source roots are canonicalized the same way, so a path that only looks inside the allowlist before symlink resolution is still rejected as `outside allowed roots`. Sensitive mounts (secrets, SSH keys, service credentials) should be `:ro` unless absolutely required, and you can combine with `workspaceAccess: "ro"` (bind modes stay independent).

## Images and setup

The default Docker image is `openclaw-sandbox:bookworm-slim`. The `scripts/sandbox-setup.sh`, `scripts/sandbox-common-setup.sh`, and `scripts/sandbox-browser-setup.sh` helper scripts are only available from a source checkout (not in the npm package), so if you installed via `npm install -g openclaw`, use the inline `docker build` commands instead. Build the default image from a source checkout with `scripts/sandbox-setup.sh`, or from npm with the inline Dockerfile:

```bash
docker build -t openclaw-sandbox:bookworm-slim - <<'DOCKERFILE'
FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
  bash ca-certificates curl git jq python3 ripgrep \
  && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home --shell /bin/bash sandbox
USER sandbox
WORKDIR /home/sandbox
CMD ["sleep", "infinity"]
DOCKERFILE
```

The default image does **not** include Node; if a skill needs Node (or other runtimes), bake a custom image or install via `sandbox.docker.setupCommand` (requires network egress + writable root + root user). OpenClaw does not silently substitute plain `debian:bookworm-slim` when `openclaw-sandbox:bookworm-slim` is missing — runs targeting the default image fail fast with a build instruction, because the bundled image carries `python3` for sandbox write/edit helpers. For a common image with tooling (`curl`, `jq`, `nodejs`, `python3`, `git`), run `scripts/sandbox-common-setup.sh` from a source checkout (from npm, build the default image first then the common image on top via the repository's `scripts/docker/sandbox/Dockerfile.common`), then set `agents.defaults.sandbox.docker.image` to `openclaw-sandbox-common:bookworm-slim`. The optional sandbox browser image is built with `scripts/sandbox-browser-setup.sh` (source) or `scripts/docker/sandbox/Dockerfile.browser` (npm).

By default, Docker sandbox containers run with **no network**; override with `agents.defaults.sandbox.docker.network`. For network security, `network: "host"` is blocked and `network: "container:<id>"` is blocked by default (namespace-join bypass risk), with a break-glass override of `agents.defaults.sandbox.docker.dangerouslyAllowContainerNamespaceJoin: true`. For Docker gateway deployments, `scripts/docker/setup.sh` can bootstrap sandbox config — set `OPENCLAW_SANDBOX=1` (or `true`/`yes`/`on`) to enable it, and override the socket location with `OPENCLAW_DOCKER_SOCKET`.

## setupCommand (one-time container setup)

`setupCommand` runs **once** after the sandbox container is created (not on every run), executing inside the container via `sh -lc`. Set it globally at `agents.defaults.sandbox.docker.setupCommand` or per-agent at `agents.list[].sandbox.docker.setupCommand`. Common pitfalls: the default `docker.network` is `"none"` (no egress) so package installs fail; `docker.network: "container:<id>"` requires `dangerouslyAllowContainerNamespaceJoin: true` and is break-glass only; `readOnlyRoot: true` prevents writes (set `readOnlyRoot: false` or bake a custom image); `user` must be root for package installs (omit `user` or set `user: "0:0"`); and sandbox exec does **not** inherit host `process.env` — use `agents.defaults.sandbox.docker.env` (or a custom image) for skill API keys. Values in `agents.defaults.sandbox.docker.env` are passed as explicit Docker container env vars, so anyone with Docker daemon access can read them via `docker inspect` — use a custom image, mounted secret file, or another secret-delivery path if that exposure is not acceptable.

## Minimal enable example

The smallest configuration that enables a sandbox backend (Docker by default, since no `backend` is set) is:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
      },
    },
  },
}
```

**Source**: OpenClaw documentation — `gateway/sandboxing` (images/binds/setupCommand sections; mirror `inbox/openclaw_docs/gateway/sandboxing.md`)
**Last Updated**: 2026-06-23
**Status**: Active
