---
tags:
  - resource
  - documentation
  - hermes_agent
  - docker
  - deployment
keywords:
  - installing tools in the hermes container
  - local inference server networking
  - vllm ollama base_url
  - host.docker.internal network host
  - linux desktop audio bridge
  - docker troubleshooting
topics:
  - Hermes Agent
  - Docker Deployment
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/docker
access_control_group: ["general"]
---

# Hermes Agent — Extending a Docker Deployment: Tools, Local Inference & Troubleshooting

## Overview

This is the operational procedure for **extending an already-running Hermes-in-Docker deployment**: adding tools the official image doesn't ship, pointing Hermes at a self-hosted inference server (vLLM, Ollama, text-generation-inference), bridging Linux desktop audio for CLI voice mode, and triaging a misbehaving container. It builds on the base run modes (see `hermes_docker_run_modes`) and the runtime/persistence model (see `hermes_docker_volumes_supervision`) — those notes cover how the container boots and what the `/opt/data` volume holds. The official image is based on `debian:13.4` and ships a curated utility set, so most extension is additive: install-on-demand, reach a neighbouring service over the Docker network, or build a derived image. Networking is the recurring footgun — inside the container `localhost` means the Hermes container itself, so a host or sibling-container inference server is reached by container name, `host.docker.internal`, or `--network host`.

## Installing more tools in the container

The official image ships with a curated set of utilities (see [What the Dockerfile does](#) — covered in `hermes_docker_volumes_supervision`), but not every tool an agent might want is preinstalled. There are **five recommended approaches, in increasing order of effort and durability**.

**1. npm or Python tools — use `npx` or `uvx`.** For any tool published to npm or PyPI, instruct Hermes to run it via `npx` (npm) or `uvx` (Python) and to remember that command in its persistent memory. If the tool needs a config file or credentials, instruct it to drop those under `/opt/data` (e.g. `/opt/data/<tool>/config.yaml`). Dependencies are fetched on demand and cached for the life of the container; configuration written under `/opt/data` survives container restarts because it lives on the bind-mounted host directory. The package cache itself is rebuilt after a `docker rm`, but `npx` and `uvx` re-fetch transparently the next time the tool runs.

**2. Other tools (apt packages, binaries) — install and remember.** For anything outside npm or PyPI — `apt` packages, prebuilt binaries, language runtimes not already in the image — instruct Hermes how to install it (e.g. `apt-get update && apt-get install -y <package>`) and tell it to remember the install command. The tool persists for the rest of the container's lifetime, and Hermes re-runs the install command after a container restart when it next needs the tool. Good for tools that are quick to install and used occasionally; for tools used constantly, prefer the next approach.

**3. Durable installs — build a derived image.** When a tool must be available immediately on every container start with no re-install delay, build a new image that inherits from `nousresearch/hermes-agent` and installs the tool in a layer:

```dockerfile
FROM nousresearch/hermes-agent:latest

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends <your-package> \
    && rm -rf /var/lib/apt/lists/*
USER hermes
```

Build it (`docker build -t my-hermes:latest .`) and use it in place of the official image in the same `docker run -d --name hermes --restart unless-stopped -v ~/.hermes:/opt/data -p 8642:8642 my-hermes:latest gateway run` invocation. The entrypoint script and `/opt/data` semantics are inherited unchanged, so the rest of this page still applies. Remember to rebuild the image when pulling a newer upstream `nousresearch/hermes-agent`.

**4. Complex tools or multi-service stacks — run a sidecar container.** For tools that bring their own service (a database, a web server, a queue, a headless browser farm) or that are too heavy to live inside the Hermes container, run them as a separate container on a shared Docker network. Hermes reaches the sidecar by container name, the same way it reaches a local inference server. From inside the Hermes container, the sidecar is reachable at `http://my-tool:<port>` (or whatever protocol it serves). This pattern keeps each service's lifecycle, resource limits, and upgrade cadence independent, and avoids bloating the Hermes image with dependencies only one tool needs.

**5. Broadly useful tools — open an issue or pull request.** If a tool is likely to be useful to most Hermes Agent users, consider contributing it upstream rather than carrying it in a private derived image. Open an issue or pull request on the [hermes-agent repository](https://github.com/NousResearch/hermes-agent) describing the tool and its use case. Tools bundled into the official image benefit every user and avoid the maintenance overhead of a downstream fork.

## Connecting to local inference servers (vLLM, Ollama, etc.)

When running Hermes in Docker and your inference server (vLLM, Ollama, text-generation-inference, etc.) is also running on the host or in another container, networking requires extra attention.

### Docker Compose (recommended)

Put both services on the same Docker network — the most reliable approach. Then in `~/.hermes/config.yaml`, use the **container name** as the hostname:

```yaml
model:
  provider: custom
  model: my-model
  base_url: http://vllm:8000/v1
  api_key: "none"
```

Key points (verbatim from source):

- Use the **container name** (`vllm`) as the hostname — not `localhost` or `127.0.0.1`, which refer to the Hermes container itself.
- The `model` value must match the `--served-model-name` you passed to vLLM.
- Set `api_key` to any non-empty string (vLLM requires the header but doesn't validate it by default).
- Do **not** include a trailing slash in `base_url`.

### Standalone Docker run (no Compose)

If your inference server runs directly on the host (not in Docker), the `config.yaml` differs only in `base_url`:

- **macOS / Windows** — keep the default `docker run` (with `-p 8642:8642`) and set `base_url: http://host.docker.internal:8000/v1` (provider `custom`, `api_key: "none"`).
- **Linux** — start the container with `--network host` and set `base_url: http://127.0.0.1:8000/v1`. With `--network host`, the `-p` flag is ignored — all container ports are directly exposed on the host.

### Verifying connectivity

From inside the Hermes container, confirm the inference server is reachable:

```sh
docker exec hermes curl -s http://vllm:8000/v1/models
```

You should see a JSON response listing your served model. If this fails, check: (1) both containers are on the same Docker network (`docker network inspect hermes-net`); (2) the inference server is listening on `0.0.0.0`, not `127.0.0.1`; (3) the port number matches.

### Ollama

Ollama works the same way. If Ollama runs on the host, use `host.docker.internal:11434` (macOS/Windows) or `127.0.0.1:11434` (Linux with `--network host`). If Ollama runs in its own container on the same Docker network, point `base_url` at `http://ollama:11434/v1` (with `model: llama3`, `api_key: "none"`).

## Optional: Linux desktop audio bridge

Voice mode in Docker needs two separate things to work: Hermes must be allowed to probe audio devices inside the container, and the container must be able to reach your host audio server. The setup below covers the host audio plumbing for Linux desktops that expose a PulseAudio-compatible socket, including many PipeWire setups. This is a Linux desktop workaround, not a general Docker Desktop feature — useful when you already have host audio working and want CLI voice mode inside the container. If Hermes reports `Running inside Docker container -- no audio devices`, use a build that includes Docker audio probing support for `PULSE_SERVER` / `PIPEWIRE_REMOTE`.

First, create an ALSA config next to your Compose file (`asound.conf`) that routes `pcm.!default` through the PulseAudio plugin. Then build a small derived image (`Dockerfile.audio`) with the ALSA PulseAudio plugin installed, and use it in Compose, passing through the host user's PulseAudio socket and cookie:

```yaml
services:
  hermes:
    build:
      context: .
      dockerfile: Dockerfile.audio
    image: hermes-agent-audio
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    volumes:
      - ~/.hermes:/opt/data
      - /run/user/${HERMES_UID}/pulse:/run/user/${HERMES_UID}/pulse
      - ~/.config/pulse/cookie:/tmp/pulse-cookie:ro
      - ./asound.conf:/etc/asound.conf:ro
    environment:
      - HERMES_UID=${HERMES_UID}
      - HERMES_GID=${HERMES_GID}
      - XDG_RUNTIME_DIR=/run/user/${HERMES_UID}
      - PULSE_SERVER=unix:/run/user/${HERMES_UID}/pulse/native
      - PULSE_COOKIE=/tmp/pulse-cookie
```

Start it with your host UID/GID so the container process can access the per-user audio socket, then verify what PortAudio sees inside the container:

```sh
export HERMES_UID="$(id -u)"
export HERMES_GID="$(id -g)"
docker compose up -d --build
docker exec hermes /opt/hermes/.venv/bin/python -c "import sounddevice as sd; print(sd.query_devices())"
```

## Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| **Container exits immediately** | Check `docker logs hermes`. Common causes: missing or invalid `.env` (run interactively first to complete setup); port conflicts if running with exposed ports. |
| **"Permission denied" errors** | The stage2 hook drops privileges to the non-root `hermes` user (UID 10000) via `s6-setuidgid`. If host `~/.hermes/` is owned by a different UID, set `HERMES_UID`/`HERMES_GID` — or their `PUID`/`PGID` aliases (LinuxServer.io / NAS parity) — to match, or `chmod -R 755 ~/.hermes`. On a NAS (UGOS, Synology, unRAID) the data dir is a bind mount the container cannot `chown`, so set `PUID`/`PGID` to that host user. |
| **Browser tools not working** | Playwright needs shared memory — add `--shm-size=1g` to the `docker run` command. |
| **Gateway not reconnecting after network issues** | `--restart unless-stopped` handles most transient failures; if the gateway is stuck, `docker restart hermes`. |
| **Checking container health** | `docker logs --tail 50 hermes` (recent logs); `docker run -it --rm nousresearch/hermes-agent:latest version` (verify version); `docker stats hermes` (resource usage). |

For the NAS permission case, the source gives a concrete invocation:

```sh
docker run -d \
  --name hermes \
  -e PUID=1000 -e PGID=10 \
  -v /volume1/docker/hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

`docker exec hermes <cmd>` automatically drops to UID 10000 too (see `hermes_docker_volumes_supervision` for the `docker exec` shim and its per-invocation root opt-out).

**Source**: `inbox/hermes_agent_docs/user-guide/docker.md` · https://hermes-agent.nousresearch.com/docs/user-guide/docker
**Last Updated**: 2026-06-19
**Status**: Active
