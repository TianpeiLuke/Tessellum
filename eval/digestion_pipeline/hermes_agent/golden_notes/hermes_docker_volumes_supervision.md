---
tags:
  - resource
  - documentation
  - hermes_agent
  - docker
  - deployment
keywords:
  - opt data volume
  - s6-overlay supervision
  - multi-profile gateways
  - per-profile auto-restart
  - non-root hermes user
  - boot reconciler
topics:
  - Hermes Agent
  - Docker Deployment
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/docker
access_control_group: ["general"]
---

# Hermes Agent — Docker Volumes & Supervision Model

## Overview

This is the **runtime model** of a Hermes Agent container: how its state is persisted and how its processes are supervised. A single `/opt/data` volume (mounted from the host's `~/.hermes/`) is the single source of truth for all mutable state — config, keys, sessions, skills, memories, per-profile HOME — while the installed `/opt/hermes` tree is immutable. Inside the official image, `s6-overlay` v3 runs as PID 1 and supervises the dashboard plus a per-profile gateway service, with state-persistent auto-restart across container restarts. The model also covers the four log surfaces, the non-root `hermes` (UID 10000) privilege boundary plus the `docker exec` shim, and the per-profile-vs-per-container tradeoff.

## Persistent Volumes

The `/opt/data` volume is the single source of truth for all Hermes state. It maps to your host's `~/.hermes/` directory and contains:

| Path | Contents |
|------|----------|
| `.env` | API keys and secrets |
| `config.yaml` | All Hermes configuration |
| `SOUL.md` | Agent personality/identity |
| `sessions/` | Conversation history |
| `memories/` | Persistent memory store |
| `skills/` | Installed skills |
| `home/` | Per-profile HOME for tool subprocesses (`git`, `ssh`, `gh`, `npm`, skill CLIs) |
| `cron/` | Scheduled job definitions |
| `hooks/` | Event hooks |
| `logs/` | Runtime logs |
| `skins/` | Custom CLI skins |

### Immutable install tree

In hosted and published Docker images, `/opt/hermes` is the installed application tree. It is root-owned and read-only to the runtime `hermes` user, so agent turns, gateway sessions, dashboard actions, and normal `docker exec hermes hermes ...` commands cannot edit the core source, bundled `.venv`, `node_modules`, or TUI bundle in place. All mutable state belongs under `/opt/data`: config, `.env`, profiles, skills, memories, sessions, logs, dashboard uploads, and plugins. The image also disables runtime `.pyc` writes and lazy dependency installs into `/opt/hermes`; optional platform dependencies should be baked into the image or installed through a new image build.

Agent self-improvement is scoped to skills, memory, plugins, and config under `/opt/data`. The core source under `/opt/hermes` is immutable; core changes ship via PRs that update the image, not by live-editing the running install. Skill CLIs that store credentials under `~` must be initialized against the subprocess HOME, not the data-volume root (e.g. the xurl skill stores OAuth state in `~/.xurl`, read as `/opt/data/home/.xurl`; run manual auth with `HOME=/opt/data/home`).

> Never run two Hermes **gateway** containers against the same data directory simultaneously — session files and memory stores are not designed for concurrent write access.

## Multi-profile Support

Hermes supports multiple profiles — separate `~/.hermes/` subdirectories that run independent agents (different SOUL, skills, memory, sessions, credentials) from a single installation. **Inside the official Docker image, the s6 supervision tree treats each profile as a first-class supervised service**, so the recommended deployment is **one container hosting all profiles**. Each profile created with `hermes profile create <name>` gets:

- A dedicated s6 service slot at `/run/service/gateway-<name>/`, registered dynamically by the runtime — no container rebuild required.
- Auto-restart on crash, backoff-managed by `s6-supervise`.
- Per-profile rotated logs at `${HERMES_HOME}/logs/gateways/<name>/current` (10 archives × 1 MB each).
- State persistence across container restarts: the boot-time reconciler reads `gateway_state.json` from each profile directory and brings the slot back up only for profiles whose last recorded state was `running`. Only a gateway you explicitly stopped (`hermes gateway stop`) stays down across a restart.

The lifecycle commands you'd run on the host work the same way from inside the container:

```sh
# Create a profile — registers the gateway-<name> s6 slot.
docker exec hermes hermes profile create coder

# Start / stop / restart — dispatches s6-svc; the gateway lifecycle survives docker restart.
docker exec hermes hermes -p coder gateway start
docker exec hermes hermes -p coder gateway stop
docker exec hermes hermes -p coder gateway restart

# Status — reports `Manager: s6 (container supervisor)` inside the container.
docker exec hermes hermes -p coder gateway status

# Remove a profile — tears down the s6 slot too.
docker exec hermes hermes profile delete coder
```

Under the hood, `hermes gateway start/stop/restart` inside the container is intercepted and routed to `s6-svc` against the right service directory; you don't learn the s6 commands directly. For raw supervisor state, use `/command/s6-svstat /run/service/gateway-<name>` (`/command/` is on PATH only for supervision-tree processes — from `docker exec`, pass the absolute path).

### Reaching more than one profile from outside the container

Two surfaces reach a profile's gateway from outside, and they differ. **Hermes Desktop (and the web dashboard)** talk to a `hermes dashboard` backend (default **port 9119**, enabled by `HERMES_DASHBOARD=1`) — *not* the OpenAI API server. One dashboard backend serves **every** co-located profile via the app's profile switcher, so you do **not** need a second port per profile for Desktop. **OpenAI-compatible API clients** (Open WebUI, LobeChat, `/v1/...`) talk to each profile's **API server**, which binds **port 8642 for every profile** (resolved from `API_SERVER_PORT` / `platforms.api_server.extra.port`). To reach a specific second profile, give it a distinct `API_SERVER_PORT` in **its own** `.env`:

```sh
# Point its API server at a free port (write to the profile's own .env)
cat >> /opt/data/profiles/work/.env <<'EOF'
API_SERVER_ENABLED=true
API_SERVER_PORT=8643
EOF

docker exec hermes hermes -p work gateway restart
```

Keep `API_SERVER_PORT` in each profile's own `.env`, never in the container-wide `environment:` block — a global value would force every profile onto the same port and collide.

### Why one container with many profiles, not many containers

Before the s6 migration, "one container per profile" was recommended because there was no in-container supervisor. With s6 as PID 1 that's no longer necessary, and the single-container layout is simpler in almost every dimension:

| | One container, many profiles | One container per profile |
|---|---|---|
| Disk overhead | One image, one bundled venv, one Playwright cache | N images / N caches |
| Memory overhead | Shared interpreter cache + node_modules | Duplicated per container |
| Profile creation | `docker exec ... profile create <name>` (seconds) | New `docker run` + port + bind-mount |
| Crash recovery | `s6-supervise` auto-restart | Docker `--restart unless-stopped` (slower) |
| Logs | Per-profile rotated `s6-log` + boot audit log | `docker logs <name>` — no built-in rotation |
| Backup | One `~/.hermes` directory | N directories to coordinate |

The default profile (`default`) is always registered on first boot. Run a **separate container per profile** only for a specific reason: resource isolation per workload (`--memory` / `--cpus`), independent image pinning, network segmentation, or compliance/blast-radius (distinct credentials never share an OS-level process tree). In those cases declare one service per profile with distinct `container_name`, `volumes`, and `ports`; never point two containers at the same `~/.hermes` directory.

## Where the Logs Go

The s6 container has four distinct log surfaces, and "why isn't my gateway showing anything in `docker logs`" is a common surprise.

| Source | Where it lands | How to read it |
|---|---|---|
| **Per-profile gateway** (`hermes gateway run` and per-profile gateways under s6) | Tee'd to two places: `docker logs <container>` (real time, no extra prefix) **and** `${HERMES_HOME}/logs/gateways/<profile>/current` (rotated, ISO-8601 timestamped, 10 archives × 1 MB each) | `docker logs -f hermes` or `tail -F ~/.hermes/logs/gateways/default/current` on the host |
| **Dashboard** (when `HERMES_DASHBOARD=1`) | `docker logs <container>` (no prefix) | `docker logs -f hermes` — interleaved with gateway lines |
| **Boot reconciler** (records which profile gateways were restored on each container start) | `${HERMES_HOME}/logs/container-boot.log` (append-only audit log) | `tail -F ~/.hermes/logs/container-boot.log` |
| **Generic Hermes logs** (`agent.log`, `errors.log`) | `${HERMES_HOME}/logs/` (profile-aware) | `docker exec hermes hermes logs --follow [--level WARNING] [--session <id>]` |

The file copy at `logs/gateways/<profile>/current` survives container restarts — `docker logs` only retains output from the current container's lifetime (wiped on `docker rm`); the rotated files persist on the bind-mounted volume. The boot reconciler's audit line shape is `<iso-timestamp> profile=<name> prior_state=<state> action=<registered|started>`, so `grep profile=coder ~/.hermes/logs/container-boot.log` reveals when a profile was restored and whether s6 auto-started it.

## What the Dockerfile Does

The official image is based on `debian:13.4` and includes Python 3 with all Hermes dependencies (`uv pip install -e ".[all]"`), Node.js + npm, Playwright with Chromium, ripgrep/ffmpeg/git/`xz-utils`, **`docker-cli`** (in-container agents drive the host's Docker daemon via a bind-mounted `/var/run/docker.sock`), **`openssh-client`** (enables the SSH terminal backend), the WhatsApp bridge, and **`s6-overlay` v3** as PID 1 (replaces `tini`) which supervises the dashboard and per-profile gateways with auto-restart on crash, reaps zombies, and forwards signals.

The container's `ENTRYPOINT` is s6-overlay's `/init`. On boot it:

1. Runs `/etc/cont-init.d/01-hermes-setup` (= `docker/stage2-hook.sh`) as root: optional UID/GID remap, fixes volume ownership, seeds `.env` / `config.yaml` / `SOUL.md` on first boot, runs non-interactive config-schema migrations unless `HERMES_SKIP_CONFIG_MIGRATION=1`, syncs bundled skills.
2. Runs `/etc/cont-init.d/02-reconcile-profiles` (= `hermes_cli.container_boot`): walks `$HERMES_HOME/profiles/<name>/`, recreates the per-profile gateway s6 service slot under `/run/service/gateway-<profile>/`, and auto-starts only those whose last recorded state was `running`.
3. Starts the static `main-hermes` and `dashboard` s6-rc services.
4. Exec's the container's CMD as the main program (`/opt/hermes/docker/main-wrapper.sh`), which routes the args passed to `docker run` (no args → `hermes`; first arg is an executable on PATH → exec it directly; anything else → `hermes <args>`). The container exits when this main program exits, with its exit code.

**Privilege model.** s6-overlay's `/init` runs as root so it can chown the volume on first boot, then drops to the `hermes` user via `s6-setuidgid` for every supervised service AND the main program. Starting `hermes gateway run` as root is refused by default because it can leave root-owned files in `/opt/data`; set `HERMES_ALLOW_ROOT_GATEWAY=1` only when you accept that risk. Do not override the image entrypoint unless you keep `/init` in the command chain.

### `docker exec` automatically drops to the `hermes` user

`docker exec hermes <cmd>` defaults to running as root, but the image ships a thin shim at `/opt/hermes/bin/hermes` (earliest on PATH) that detects root callers and transparently re-execs through `s6-setuidgid hermes`. So `docker exec hermes login`, `... profile create …`, `... setup`, etc. all write files owned by UID 10000 — readable by the supervised gateway — with no `--user` flag. Non-root callers short-circuit to exec the venv binary directly, so there's no overhead on hot paths. To retain root semantics per-invocation:

```sh
docker exec -e HERMES_DOCKER_EXEC_AS_ROOT=1 hermes <cmd>
```

The shim accepts `1` / `true` / `yes` (case-insensitive); anything else falls through to the drop, so silent opt-outs aren't possible. If `s6-setuidgid` isn't available (custom builds that stripped s6-overlay), the shim refuses to run as root and exits 126, surfacing the broken privilege model loudly rather than regressing to the footgun where `docker exec hermes login` would write `auth.json` as `root:root` and break the supervised gateway's auth.

### Per-profile gateway supervision

Each profile gets an s6-supervised gateway service at `/run/service/gateway-<name>/` with state-persistent auto-restart. Benefits over the pre-s6 image: gateway crashes are auto-restarted by `s6-supervise` after a ~1s backoff; the dashboard (when `HERMES_DASHBOARD=1`) is supervised on the same tree; `docker restart`, image upgrades, and unexpected exits preserve running gateways (the cont-init reconciler reads `$HERMES_HOME/profiles/<name>/gateway_state.json` and brings the slot back up if the last recorded state was `running` — only an explicit `hermes gateway stop` records `stopped`); and per-profile gateway logs persist under `$HERMES_HOME/logs/gateways/<profile>/current` (rotated by `s6-log`). `hermes status` reports `Manager: s6 (container supervisor)`; use `/command/s6-svstat /run/service/gateway-<name>` for the raw supervisor view.

## Skills and Credential Files

When Docker is the execution environment (the agent runs commands inside a Docker sandbox — a separate config concern), Hermes reuses a single long-lived container for all tool calls and automatically bind-mounts the skills directory (`~/.hermes/skills/`) and any credential files declared by skills into that container as read-only volumes. Skill scripts, templates, and references are available inside the sandbox without manual configuration, and because the container persists for the life of the Hermes process, dependencies you install stay for the next tool call. The same syncing happens for SSH and Modal backends — skills and credential files are uploaded via rsync or the Modal mount API before each command.

**Source**: `inbox/hermes_agent_docs/user-guide/docker.md` · https://hermes-agent.nousresearch.com/docs/user-guide/docker
**Last Updated**: 2026-06-19
**Status**: Active
