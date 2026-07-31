---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - podman
keywords:
  - openclaw podman rootless container
  - run-openclaw-podman.sh launch
  - openclaw container host cli control plane
  - podman quadlet systemd user auto-start
  - openclaw_gateway_token env file
  - userns keep-id bind mount openclaw state
  - podman publish 127.0.0.1 tailscale serve
  - gateway.mode local selinux Z bind mount
topics:
  - OpenClaw
  - Install — Podman
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/podman
access_control_group: ["general"]
---

# OpenClaw — Install in a Rootless Podman Container

## Overview

This note is the procedure for running the OpenClaw Gateway in a **rootless Podman container** managed by your current non-root user, mirroring the `install/podman` source page. The intended model has four parts: Podman runs the gateway container; your host `openclaw` CLI is the control plane; persistent state lives on the host under `~/.openclaw` by default; and day-to-day management uses `openclaw --container <name> ...` instead of `sudo -u openclaw`, `podman exec`, or a separate service user. It covers prerequisites, the four-step quick start with the `setup.sh` / `run-openclaw-podman.sh` helper scripts and their build/setup/launch env vars, in-container model auth, the host-CLI default (`OPENCLAW_CONTAINER`), Podman-and-Tailscale notes, optional Quadlet/systemd-user auto-start, config/env/storage bind-mounts, useful commands, and troubleshooting (EACCES, missing `gateway.mode=local`, SELinux).

## Prerequisites

- **Podman** in rootless mode.
- **OpenClaw CLI** installed on the host.
- **Optional:** `systemd --user` if you want Quadlet-managed auto-start.
- **Optional:** `sudo` only if you want `loginctl enable-linger "$(whoami)"` for boot persistence on a headless host.

## Quick start

The four-step flow drives the whole setup from the repo root, then hands ongoing management to the host CLI:

1. **One-time setup** — from the repo root, run `./scripts/podman/setup.sh`.
2. **Start the Gateway container** — start the container with `./scripts/run-openclaw-podman.sh launch`.
3. **Run onboarding inside the container** — run `./scripts/run-openclaw-podman.sh launch setup`, then open `http://127.0.0.1:18789/`.
4. **Manage the running container from the host CLI** — set `OPENCLAW_CONTAINER=openclaw`, then use normal `openclaw` commands from the host.

What the setup step does: `./scripts/podman/setup.sh` builds `openclaw:local` in your rootless Podman store by default, or uses `OPENCLAW_IMAGE` / `OPENCLAW_PODMAN_IMAGE` if you set one. It creates `~/.openclaw/openclaw.json` with `gateway.mode: "local"` if missing, and creates `~/.openclaw/.env` with `OPENCLAW_GATEWAY_TOKEN` if missing. For manual launches, the helper reads only a small allowlist of Podman-related keys from `~/.openclaw/.env` and passes explicit runtime env vars to the container; it does not hand the full env file to Podman.

For Quadlet-managed setup, add the `--quadlet` flag (or set `OPENCLAW_PODMAN_QUADLET=1`); Quadlet is a Linux-only option because it depends on systemd user services:

```bash
./scripts/podman/setup.sh --quadlet
```

Optional build/setup env vars control how the image is produced:

- `OPENCLAW_IMAGE` or `OPENCLAW_PODMAN_IMAGE` — use an existing/pulled image instead of building `openclaw:local`.
- `OPENCLAW_IMAGE_APT_PACKAGES` — install extra apt packages during image build (also accepts legacy `OPENCLAW_DOCKER_APT_PACKAGES`).
- `OPENCLAW_IMAGE_PIP_PACKAGES` — install extra Python packages during image build; pin versions and use only package indexes you trust.
- `OPENCLAW_EXTENSIONS` — pre-install plugin dependencies at build time.
- `OPENCLAW_INSTALL_BROWSER` — pre-install Chromium and Xvfb for browser automation (set to `1` to enable).

The container start (`./scripts/run-openclaw-podman.sh launch`) starts the container as your current uid/gid with `--userns=keep-id` and bind-mounts your OpenClaw state into the container. Onboarding (`./scripts/run-openclaw-podman.sh launch setup`) is then reached by opening `http://127.0.0.1:18789/` and using the token from `~/.openclaw/.env`.

### Model auth in Podman

- Use OpenClaw-managed auth during setup: Anthropic API keys for Anthropic, or OpenAI Codex browser OAuth/device-code auth for Codex-backed OpenAI.
- The Podman launcher does not mount host CLI credential homes such as `~/.claude` or `~/.codex` into the setup or gateway container.
- Existing host CLI logins are same-host convenience paths. For container installs, keep provider auth in the mounted `~/.openclaw` state that setup manages.

### Host CLI default

Export the container name once so subsequent `openclaw` commands route into that container automatically:

```bash
export OPENCLAW_CONTAINER=openclaw
```

Then commands such as `openclaw dashboard --no-open`, `openclaw gateway status --deep` (includes an extra service scan), `openclaw doctor`, and `openclaw channels login` will run inside that container automatically. On macOS, Podman machine may make the browser appear non-local to the gateway; if the Control UI reports device-auth errors after launch, use the Tailscale guidance in the **Podman and Tailscale** section below.

## Podman and Tailscale

For HTTPS or remote browser access, follow the main Tailscale docs. The Podman-specific notes are:

- Keep the Podman publish host at `127.0.0.1`.
- Prefer host-managed `tailscale serve` over `openclaw gateway --tailscale serve`.
- On macOS, if local browser device-auth context is unreliable, use Tailscale access instead of ad hoc local tunnel workarounds.

## Systemd (Quadlet, optional)

If you ran `./scripts/podman/setup.sh --quadlet`, setup installs a Quadlet file at `~/.config/containers/systemd/openclaw.container`. The useful systemd-user commands are: **Start** `systemctl --user start openclaw.service`; **Stop** `systemctl --user stop openclaw.service`; **Status** `systemctl --user status openclaw.service`; **Logs** `journalctl --user -u openclaw.service -f`.

After editing the Quadlet file, reload and restart the unit:

```bash
systemctl --user daemon-reload
systemctl --user restart openclaw.service
```

For boot persistence on SSH/headless hosts, enable lingering for your current user with `sudo loginctl enable-linger "$(whoami)"`.

## Config, env, and storage

The key host paths and helper are: **Config dir** `~/.openclaw`; **Workspace dir** `~/.openclaw/workspace`; **Token file** `~/.openclaw/.env`; **Launch helper** `./scripts/run-openclaw-podman.sh`.

The launch script and Quadlet bind-mount host state into the container, mapping `OPENCLAW_CONFIG_DIR` -> `/home/node/.openclaw` and `OPENCLAW_WORKSPACE_DIR` -> `/home/node/.openclaw/workspace`. By default those are host directories, not anonymous container state, so `openclaw.json`, per-agent `auth-profiles.json`, channel/provider state, sessions, and workspace survive container replacement. The Podman setup also seeds `gateway.controlUi.allowedOrigins` for `127.0.0.1` and `localhost` on the published gateway port so the local dashboard works with the container's non-loopback bind.

Useful env vars for the manual launcher:

- `OPENCLAW_PODMAN_CONTAINER` — container name (`openclaw` by default).
- `OPENCLAW_PODMAN_IMAGE` / `OPENCLAW_IMAGE` — image to run.
- `OPENCLAW_PODMAN_GATEWAY_HOST_PORT` — host port mapped to container `18789`.
- `OPENCLAW_PODMAN_BRIDGE_HOST_PORT` — host port mapped to container `18790`.
- `OPENCLAW_PODMAN_PUBLISH_HOST` — host interface for published ports; default is `127.0.0.1`.
- `OPENCLAW_GATEWAY_BIND` — gateway bind mode inside the container; default is `lan`.
- `OPENCLAW_PODMAN_USERNS` — `keep-id` (default), `auto`, or `host`.

The manual launcher reads `~/.openclaw/.env` before finalizing container/image defaults, so you can persist these there. If you use a non-default `OPENCLAW_CONFIG_DIR` or `OPENCLAW_WORKSPACE_DIR`, set the same variables for both `./scripts/podman/setup.sh` and later `./scripts/run-openclaw-podman.sh launch` commands; the repo-local launcher does not persist custom path overrides across shells.

The generated Quadlet service intentionally keeps a fixed, hardened default shape: `127.0.0.1` published ports, `--bind lan` inside the container, and `keep-id` user namespace. It pins `OPENCLAW_NO_RESPAWN=1`, `Restart=on-failure`, and `TimeoutStartSec=300`. It publishes both `127.0.0.1:18789:18789` (gateway) and `127.0.0.1:18790:18790` (bridge). It reads `~/.openclaw/.env` as a runtime `EnvironmentFile` for values such as `OPENCLAW_GATEWAY_TOKEN`, but it does not consume the manual launcher's Podman-specific override allowlist. If you need custom publish ports, publish host, or other container-run flags, use the manual launcher or edit `~/.config/containers/systemd/openclaw.container` directly, then reload and restart the service.

## Useful commands

- **Container logs:** `podman logs -f openclaw`
- **Stop container:** `podman stop openclaw`
- **Remove container:** `podman rm -f openclaw`
- **Open dashboard URL from host CLI:** `openclaw dashboard --no-open`
- **Health/status via host CLI:** `openclaw gateway status --deep` (RPC probe + extra service scan)

## Troubleshooting

- **Permission denied (EACCES) on config or workspace:** The container runs with `--userns=keep-id` and `--user <your uid>:<your gid>` by default. Ensure the host config/workspace paths are owned by your current user.
- **Gateway start blocked (missing `gateway.mode=local`):** Ensure `~/.openclaw/openclaw.json` exists and sets `gateway.mode="local"`. `scripts/podman/setup.sh` creates this if missing.
- **Container CLI commands hit the wrong target:** Use `openclaw --container <name> ...` explicitly, or export `OPENCLAW_CONTAINER=<name>` in your shell.
- **`openclaw update` fails with `--container`:** Expected. Rebuild/pull the image, then restart the container or the Quadlet service.
- **Quadlet service does not start:** Run `systemctl --user daemon-reload`, then `systemctl --user start openclaw.service`. On headless systems you may also need `sudo loginctl enable-linger "$(whoami)"`.
- **SELinux blocks bind mounts:** Leave the default mount behavior alone; the launcher auto-adds `:Z` on Linux when SELinux is enforcing or permissive.

**Source**: OpenClaw documentation — `install/podman` (mirror `inbox/openclaw_docs/install/podman.md`)
**Last Updated**: 2026-06-22
**Status**: Active
