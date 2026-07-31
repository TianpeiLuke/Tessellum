---
tags:
  - resource
  - documentation
  - hermes_agent
  - terminal_backend
  - sandboxing
keywords:
  - terminal backend configuration
  - docker ssh modal daytona singularity local
  - container lifecycle and hardening
  - home_mode subprocess HOME policy
  - remote-to-host file sync
  - persistent shell
topics:
  - Hermes Agent
  - Configuration
  - Terminal Backends
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/configuration
access_control_group: ["general"]
---

# Hermes Agent — Terminal Backend Configuration

## Overview

A Hermes **terminal backend** is the execution substrate that determines *where* the agent's shell commands, file tools, and `execute_code` calls actually run. Hermes supports **six backends** — `local`, `docker`, `ssh`, `modal`, `daytona`, and `singularity` — each trading isolation against convenience, all selected through the single `terminal.backend` key in `config.yaml`. This note models that backend system: per-backend setup and isolation, the Docker container's single-persistent-container lifecycle (labels, reuse, reaping, hardening), the `home_mode` subprocess-`HOME` policy, remote-to-host file sync on teardown, and the persistent shell. Detailed code-execution policy and the per-tool README live in their owning sub-plans (link-outs, not duplicated here).

## Terminal Backend Configuration

Hermes supports six terminal backends. Each determines where the agent's shell commands actually execute — your local machine, a Docker container, a remote server via SSH, a Modal cloud sandbox (direct or via the Nous-managed gateway), a Daytona workspace, or a Singularity/Apptainer container.

```yaml
terminal:
  backend: local    # local | docker | ssh | modal | daytona | singularity
  cwd: "."          # Gateway/cron working directory (CLI always uses launch dir)
  timeout: 180      # Per-command timeout in seconds
  home_mode: auto   # auto | real | profile — subprocess HOME policy
  env_passthrough: []  # Env var names to forward to sandboxed execution (terminal + execute_code)
  singularity_image: "docker://nikolaik/python-nodejs:python3.11-nodejs20"  # Container image for Singularity backend
  modal_image: "nikolaik/python-nodejs:python3.11-nodejs20"                 # Container image for Modal backend
  daytona_image: "nikolaik/python-nodejs:python3.11-nodejs20"               # Container image for Daytona backend
```

For cloud sandboxes such as Modal and Daytona, `container_persistent: true` means Hermes will try to preserve filesystem state across sandbox recreation. It does not promise that the same live sandbox, PID space, or background processes will still be running later.

## Backend Overview

| Backend | Where commands run | Isolation | Best for |
|---------|-------------------|-----------|----------|
| **local** | Your machine directly | None | Development, personal use |
| **docker** | Single persistent Docker container (shared across session, `/new`, subagents) | Full (namespaces, cap-drop) | Safe sandboxing, CI/CD |
| **ssh** | Remote server via SSH | Network boundary | Remote dev, powerful hardware |
| **modal** | Modal cloud sandbox | Full (cloud VM) | Ephemeral cloud compute, evals |
| **daytona** | Daytona workspace | Full (cloud container) | Managed cloud dev environments |
| **singularity** | Singularity/Apptainer container | Namespaces (--containall) | HPC clusters, shared machines |

## Local Backend and `home_mode`

The **local** backend is the default: commands run directly on your machine with no isolation and no special setup (`terminal: { backend: local }`). Local tool subprocesses keep your real OS-user `HOME` by default so external CLIs (`git`, `ssh`, `gh`, `az`, `npm`, Claude Code, Codex) find the credentials and config they already use. Hermes state stays profile-scoped through `HERMES_HOME`; `HOME` is not how profiles select config, memory, sessions, or skills. Hermes does **not** change your system-wide `HOME`, shell startup files, or the OS account home — this only controls the environment passed to subprocesses Hermes launches through `terminal`, background terminal processes, `execute_code`, and ACP helper processes.

The `terminal.home_mode` key chooses the subprocess `HOME` policy (auto/real/profile):

| Mode | Host installs | Containers | Tradeoff |
|---|---|---|---|
| `auto` | Keep the real OS-user `HOME` | Use `{HERMES_HOME}/home` | Recommended default. Host CLIs keep working; container state persists. |
| `real` | Force the real OS-user `HOME` | Force the real OS-user `HOME` if visible | Useful if a parent process accidentally started with `HOME` pointed at a profile home. |
| `profile` | Use `{HERMES_HOME}/home` when it exists | Use `{HERMES_HOME}/home` when it exists | Strict per-profile CLI config isolation, but normal `~/.ssh`, `~/.gitconfig`, `~/.azure`, `~/.config/gh`, Claude/Codex auth, npm state, etc. will not be visible unless you initialize or link them inside the profile home. |

In `profile` mode tool subprocesses use `{HERMES_HOME}/home` as `HOME`, and Hermes also sets `HERMES_REAL_HOME` so scripts can still locate the actual user home. Container backends keep using `{HERMES_HOME}/home` in `auto` mode because that directory lives on the persistent Hermes data volume. The agent has the same filesystem access as your user account; use `hermes tools` to disable tools you don't want, or switch to Docker for sandboxing.

## Docker Backend, Lifecycle, and Hardening

Runs commands inside a Docker container with security hardening (all capabilities dropped, no privilege escalation, PID limits). **Single persistent container, shared across Hermes processes.** Hermes starts ONE long-lived container on first use and routes every terminal, file, and `execute_code` call through `docker exec` into that same container — across sessions, `/new`, `/reset`, and `delegate_task` subagents. Working-directory changes, installed packages, files in `/workspace`, and **background processes** all carry over from one tool call and one Hermes process to the next.

```yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  docker_mount_cwd_to_workspace: false  # Mount launch dir into /workspace
  docker_run_as_host_user: false   # See "Running container as host user" below
  docker_forward_env:              # Host env vars to forward into container
    - "GITHUB_TOKEN"
  docker_env:                      # Literal env vars to inject (KEY=value)
    DEBUG: "1"
    PYTHONUNBUFFERED: "1"
  docker_volumes:                  # Host directory mounts
    - "/home/user/projects:/workspace/projects"
    - "/home/user/data:/data:ro"   # :ro for read-only
  docker_extra_args:               # Extra flags appended verbatim to `docker run`
    - "--gpus=all"
    - "--network=host"

  # Resource limits
  container_cpu: 1                 # CPU cores (0 = unlimited)
  container_memory: 5120           # MB (0 = unlimited)
  container_disk: 51200            # MB (requires overlay2 on XFS+pquota)
  container_persistent: true       # Persist /workspace and /root bind-mount dirs

  # Cross-process container reuse (defaults match the "one long-lived
  # container shared across sessions" contract — see Container lifecycle).
  docker_persist_across_processes: true   # Reuse container across Hermes restarts
  docker_orphan_reaper: true              # Sweep abandoned Exited containers at startup

  # Cross-backend lifecycle settings (apply to docker as well)
  timeout: 180                     # Per-command timeout in seconds
  lifetime_seconds: 300            # Idle-reaper window; also feeds 2× orphan-reaper threshold
```

`docker_env` injects literal `KEY=value` pairs from config (also via `TERMINAL_DOCKER_ENV='{"DEBUG":"1"}'`); `docker_forward_env` forwards values from your shell or `~/.hermes/.env` so the secret never appears in config — use it for tokens, `docker_env` for static knobs. `docker_extra_args` passes arbitrary `docker run` flags (`--gpus`, `--network`, `--add-host`, …) appended last so they can override Hermes defaults; flags conflicting with the hardening silently weaken isolation. Requirements: Docker Desktop/Engine running (Hermes probes `$PATH` plus common macOS locations); Podman works via `HERMES_DOCKER_BINARY=podman`.

**Container lifecycle.** Every Hermes-managed container carries three labels — `hermes-agent=1`, `hermes-task-id=<sanitized task_id>`, `hermes-profile=<sanitized profile name>` — so subsequent processes and the orphan reaper can identify it. On startup Hermes runs `docker ps --filter label=hermes-task-id=<id> --filter label=hermes-profile=<profile>` and **attaches to the existing container**; an `exited` container is `docker start`'d and reused (filesystem + installed packages survive, in-container background processes do not). On process exit (`/quit`, TUI close, gateway shutdown, even SIGKILL) cleanup is a **no-op for the container in default mode** — it keeps running so background processes survive, and the next process re-attaches via the label probe in milliseconds.

The container is only torn down (stopped + `docker rm -f`'d) in these cases:

| Trigger | When it fires |
|---|---|
| `docker_persist_across_processes: false` | Explicit per-process isolation. Every `cleanup()` does `stop` + `rm -f`. Matches pre-issue-#20561 behavior. |
| Idle reaper (`lifetime_seconds`, default 300s) | Only when the env is `persist_across_processes=false`. Persist-mode envs are no-op'd; container survives the idle sweep. |
| Orphan reaper at next startup | Sweeps **Exited** hermes-labeled containers older than `2 × lifetime_seconds` (default 600s = 10 min), scoped to the current profile. **Running containers are never touched** — sibling-process safety. Set `docker_orphan_reaper: false` to disable. |
| Direct user action | `docker rm -f`, `docker system prune`, Docker Desktop restart. We don't set `--restart=always`, so a host reboot leaves the container `Exited` (its CoW layer survives and gets reused on next startup, but bg processes are gone). |

An OOM kill of in-container PID 1 transitions the container to `Exited` (reuse `docker start`s it; filesystem survives, bg processes do not). Switching profiles isolates containers — a `hermes-profile=work` container is invisible to a `hermes-profile=research` process, and the orphan reaper is profile-scoped. Parallel subagents from `delegate_task(tasks=[...])` share the one container, so concurrent `cd`/env mutations/same-path writes collide; a subagent needing isolation registers a per-task image override via `register_task_env_overrides()` (RL/benchmark environments like TerminalBench2, HermesSweEnv do this automatically). Security hardening: `--cap-drop ALL` with only `DAC_OVERRIDE`, `CHOWN`, `FOWNER` added back; `--security-opt no-new-privileges`; `--pids-limit 256`; size-limited tmpfs for `/tmp` (512MB), `/var/tmp` (256MB), `/run` (64MB). Every `terminal:` key has a `TERMINAL_<KEY_UPPERCASE>` env override (e.g. `TERMINAL_DOCKER_IMAGE`, `TERMINAL_DOCKER_PERSIST_ACROSS_PROCESSES` default `true`, `HERMES_DOCKER_BINARY`).

### Docker Volume Mounts, Host-User, and Workspace Opt-in

`docker_volumes` shares host directories using standard Docker `-v` syntax `host_path:container_path[:options]` — for providing files (datasets/configs), receiving generated files, and shared workspaces. For gateway `MEDIA:/...` sends, prefer a host-visible export mount such as `/home/user/.hermes/cache/documents:/output`, write to `/output/...`, and emit the **host path** (not `/workspace/...`). YAML duplicate keys silently override, so merge new mounts into one `docker_volumes:` list. `docker_run_as_host_user: true` appends `--user $(id -u):$(id -g)` so bind-mounted files are owned by your host user (not root), at the cost of losing `apt install`/root-owned writes. `docker_mount_cwd_to_workspace: true` bind-mounts your launch directory to `/workspace` (and starts there) — otherwise sandboxes stay isolated; opt in only when you want the container to work on live host files.

## SSH, Modal, Daytona, and Singularity Backends

- **SSH** — runs commands on a remote server over SSH, using ControlMaster for connection reuse (5-minute idle keepalive); persistent shell is enabled by default so cwd/env survive across commands. Set `terminal: { backend: ssh, persistent_shell: true }`; required env `TERMINAL_SSH_HOST`/`TERMINAL_SSH_USER`; optional `TERMINAL_SSH_PORT` (22), `TERMINAL_SSH_KEY`, `TERMINAL_SSH_PERSISTENT` (true). Connects at init with `BatchMode=yes` and `StrictHostKeyChecking=accept-new`, keeps a single `bash -l` process alive via temp files; `stdin_data`/`sudo` commands fall back to one-shot mode.
- **Modal** — runs in a Modal cloud sandbox; each task gets an isolated VM with configurable `container_cpu`/`container_memory`/`container_disk` and `container_persistent: true` snapshot/restore. Requires `MODAL_TOKEN_ID` + `MODAL_TOKEN_SECRET` or `~/.modal.toml`. Snapshots are tracked in `~/.hermes/modal_snapshots.json` and preserve filesystem state, not live processes/PID space/background jobs. Credential files auto-mount from `~/.hermes/` and sync before each command.
- **Daytona** — runs in a Daytona managed workspace with stop/resume persistence. Requires `DAYTONA_API_KEY`. When persistent, sandboxes are stopped (not deleted) on cleanup and resumed next session; names follow `hermes-{task_id}`. Disk is capped at a 10 GiB maximum (over-requests capped with a warning).
- **Singularity/Apptainer** — runs in a Singularity/Apptainer container for HPC clusters and shared machines without Docker. Requires `apptainer`/`singularity` in `$PATH`; `docker://...` URLs auto-convert to cached SIF files. Scratch dir resolves `TERMINAL_SCRATCH_DIR` → `TERMINAL_SANDBOX_DIR/singularity` → `/scratch/$USER/hermes-agent` → `~/.hermes/sandboxes/singularity`. Uses `--containall --no-home` for full namespace isolation without mounting the host home.

**Common Terminal Backend Issues** — if commands fail immediately or the tool is reported disabled: **Local** has no special requirements (safest default); **Docker** — run `docker version`, else fix Docker or `hermes config set terminal.backend local`; **SSH** needs both `TERMINAL_SSH_HOST` and `TERMINAL_SSH_USER`; **Modal** needs `MODAL_TOKEN_ID` or `~/.modal.toml` (`hermes doctor` checks); **Daytona** needs `DAYTONA_API_KEY`; **Singularity** needs `apptainer`/`singularity` in `$PATH`. When in doubt, set `terminal.backend` to `local` and verify commands run there first.

## Remote-to-Host File Sync and Persistent Shell

For the **SSH**, **Modal**, and **Daytona** backends (where the agent's working tree lives on a different machine than the Hermes host), Hermes tracks files the agent touched inside the remote sandbox and, on teardown/cleanup, **syncs modified files back to the host** under `~/.hermes/cache/remote-syncs/<session-id>/`. It triggers on session close, `/new`, `/reset`, gateway message timeout, and `delegate_task` subagent completion with a remote backend; covers the whole modified tree (additions, edits, deletions); and the local copy is the authoritative record since the remote sandbox may already be torn down. Files over `file_sync_max_mb` (default `100`) are skipped.

```yaml
terminal:
  file_sync_max_mb: 100     # default — sync files up to 100 MB each
  file_sync_enabled: true   # default — set false to skip the sync entirely
```

This recovers results from ephemeral cloud sandboxes destroyed after the session, without explicit `scp`/`modal volume put`. **Persistent shell**: by default each command runs in its own subprocess (cwd/env/shell vars reset between commands); enabling persistent shell keeps a single long-lived bash process alive across `execute()` calls so working directory (`cd /tmp`), exported env vars (`export FOO=bar`), and shell variables (`MY_VAR=hello`) persist. It is most useful for SSH (where it also removes per-command connection overhead) — **enabled by default for SSH**, disabled for local. Precedence: config `terminal.persistent_shell` (default `true`) < SSH override `TERMINAL_SSH_PERSISTENT` (follows config) < local override `TERMINAL_LOCAL_PERSISTENT` (default `false`); per-backend env vars take highest precedence (`export TERMINAL_LOCAL_PERSISTENT=true` to enable on local). Commands requiring `stdin_data` or sudo fall back to one-shot mode since the persistent shell's stdin is occupied by the IPC protocol.

**Source**: `inbox/hermes_agent_docs/user-guide/configuration.md` §Terminal Backend Configuration · https://hermes-agent.nousresearch.com/docs/user-guide/configuration
**Last Updated**: 2026-06-19
**Status**: Active
