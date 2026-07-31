---
tags:
  - resource
  - documentation
  - openclaw
  - install
  - docker
keywords:
  - openclaw docker gateway
  - containerized gateway setup.sh
  - openclaw image build airgapped
  - docker compose openclaw-gateway openclaw-cli
  - openclaw env vars OPENCLAW_IMAGE OPENCLAW_SANDBOX
  - control ui 18789 health checks healthz readyz
  - lan vs loopback gateway bind
  - host.docker.internal host local providers
  - bonjour mdns docker disable
  - openclaw storage persistence clawdock
topics:
  - OpenClaw
  - Install
  - Docker
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/install/docker
access_control_group: ["general"]
---

# OpenClaw — Running the Gateway as a Docker Container

## Overview

This note is the procedure for running the OpenClaw **Gateway** as a Docker container: building (or loading a pre-built/airgapped) image, onboarding, the manual Compose flow, environment variables, observability and health checks, LAN-vs-loopback exposure, host-local providers, Bonjour/mDNS, persistence, shell helpers, the VPS pointer, and troubleshooting. It mirrors the `install/docker` source page **except** the *Agent sandbox* feature, captured separately in [oc_install_docker_agent_sandbox](oc_install_docker_agent_sandbox.md). Docker is **optional** — use it only for an isolated/throwaway containerized gateway or to validate the Docker flow; for the fastest dev loop, use the normal install flow.

## Is Docker right for me?

- **Yes**: you want an isolated, throwaway gateway environment, or to run OpenClaw on a host without local installs.
- **No**: you are on your own machine and just want the fastest dev loop — use the normal install flow.
- **Sandboxing note**: the default sandbox backend uses Docker when sandboxing is enabled, but sandboxing is off by default and does **not** require the full gateway to run in Docker (SSH and OpenShell backends also exist). See [oc_install_docker_agent_sandbox](oc_install_docker_agent_sandbox.md) and source `/gateway/sandboxing`.

## Prerequisites

- Docker Desktop (or Docker Engine) + Docker Compose v2.
- At least 2 GB RAM for the image build (`pnpm install` may be OOM-killed on 1 GB hosts with `exit 137`).
- Enough disk for images and logs.
- On a VPS/public host, review the source's `/gateway/security` network-exposure hardening, especially the Docker `DOCKER-USER` firewall policy.

## Containerized gateway

The source's ordered `<Steps>` sequence is **Build the image → Airgapped rerun → Complete onboarding → Open the Control UI → Configure channels (optional)**.

**Build the image** — from the repo root, run the setup script; to use a pre-built image instead, set `OPENCLAW_IMAGE` first:

```bash
./scripts/docker/setup.sh

# or use a pre-built image instead of building locally
export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"
./scripts/docker/setup.sh
```

Pre-built images are published at the GitHub Container Registry; common tags are `main`, `latest`, and `<version>` (e.g. `2026.2.26`).

**Airgapped rerun** — on offline hosts, transfer and load the image first, then rerun setup with `--offline`:

```bash
docker load -i openclaw-image.tar
export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"
./scripts/docker/setup.sh --offline
```

`--offline` verifies that `OPENCLAW_IMAGE` already exists locally, disables implicit Compose pulls and builds, then runs the normal setup flow (`.env` sync, permission fixes, onboarding, gateway config sync, Compose startup). If `OPENCLAW_SANDBOX=1`, offline setup also checks the configured default and active per-agent sandbox images on the daemon behind `OPENCLAW_DOCKER_SOCKET` (Docker-backed browser images must carry the current OpenClaw browser contract label); when a required image is missing or incompatible, setup exits without changing sandbox configuration rather than reporting an unusable sandbox.

**Complete onboarding** — the setup script runs onboarding automatically: it prompts for provider API keys, generates a gateway token (written to `.env`), creates the auth-profile secret key directory, and starts the gateway via Docker Compose. Pre-start onboarding and config writes run through `openclaw-gateway` directly; `openclaw-cli` is for commands run **after** the gateway container exists.

**Open the Control UI** — open `http://127.0.0.1:18789/` and paste the configured shared secret into Settings (the setup script writes a token to `.env` by default; if you switch to password auth, use that password). Re-fetch the URL with `docker compose run --rm openclaw-cli dashboard --no-open`.

**Configure channels (optional)** — use the CLI container to add messaging channels: WhatsApp via QR `channels login`, Telegram/Discord via `channels add --channel <name> --token "<token>"` (source `/channels/whatsapp`, `/channels/telegram`, `/channels/discord`).

### Manual flow

To run each step yourself instead of the setup script:

```bash
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js onboard --mode local --no-install-daemon
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js config set --batch-json '[{"path":"gateway.mode","value":"local"},{"path":"gateway.bind","value":"lan"},{"path":"gateway.controlUi.allowedOrigins","value":["http://localhost:18789","http://127.0.0.1:18789"]}]'
docker compose up -d openclaw-gateway
```

Run `docker compose` from the repo root. If you enabled `OPENCLAW_EXTRA_MOUNTS` or `OPENCLAW_HOME_VOLUME`, the setup script writes `docker-compose.extra.yml`; include it after any standard override file. Because `openclaw-cli` shares `openclaw-gateway`'s network namespace it is a **post-start** tool — before `docker compose up -d openclaw-gateway`, run onboarding and setup-time config writes through `openclaw-gateway` with `--no-deps --entrypoint node`.

### Environment variables

The setup script accepts these optional environment variables (verbatim):

| Variable | Purpose |
| --- | --- |
| `OPENCLAW_IMAGE` | Use a remote image instead of building locally |
| `OPENCLAW_IMAGE_APT_PACKAGES` | Extra apt packages during build (space-separated) |
| `OPENCLAW_IMAGE_PIP_PACKAGES` | Extra Python packages during build (space-separated) |
| `OPENCLAW_EXTENSIONS` | Pre-install plugin deps at build time (space-separated names) |
| `OPENCLAW_EXTRA_MOUNTS` | Extra host bind mounts (comma-separated `source:target[:opts]`) |
| `OPENCLAW_HOME_VOLUME` | Persist `/home/node` in a named Docker volume |
| `OPENCLAW_SANDBOX` | Opt in to sandbox bootstrap (`1`, `true`, `yes`, `on`) |
| `OPENCLAW_SKIP_ONBOARDING` | Skip interactive onboarding (`1`, `true`, `yes`, `on`) |
| `OPENCLAW_DOCKER_SOCKET` | Override Docker socket path |
| `OPENCLAW_DISABLE_BONJOUR` | Disable Bonjour/mDNS advertising (defaults `1` for Docker) |
| `OPENCLAW_DISABLE_BUNDLED_SOURCE_OVERLAYS` | Disable bundled plugin source bind-mount overlays |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Shared OTLP/HTTP collector endpoint for OpenTelemetry export |
| `OTEL_EXPORTER_OTLP_*_ENDPOINT` | Signal-specific OTLP endpoints (traces, metrics, logs) |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol override (only `http/protobuf` supported today) |
| `OTEL_SERVICE_NAME` | Service name for OpenTelemetry resources |
| `OTEL_SEMCONV_STABILITY_OPT_IN` | Opt in to latest experimental GenAI semantic attributes |
| `OPENCLAW_OTEL_PRELOADED` | Skip a second OpenTelemetry SDK when one is preloaded |

The official image ships no Homebrew, so onboarding hides brew-only skill dependency installers in a Linux container without `brew` (provide those via a custom image). Debian dependencies go through `OPENCLAW_IMAGE_APT_PACKAGES` (legacy `OPENCLAW_DOCKER_APT_PACKAGES` still accepted); Python through `OPENCLAW_IMAGE_PIP_PACKAGES`, which runs `python3 -m pip install --break-system-packages` at build (pin versions, trusted indexes only). Maintainers can test bundled plugin source by mounting a source dir over its packaged path via `OPENCLAW_EXTRA_MOUNTS`.

### Observability

OpenTelemetry export is **outbound** from the Gateway container to your OTLP collector and needs no published Docker port. To make the bundled exporter available inside a locally-built image, include its runtime deps via the `diagnostics-otel` extension:

```bash
export OPENCLAW_EXTENSIONS="diagnostics-otel"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4318"
export OTEL_SERVICE_NAME="openclaw-gateway"
./scripts/docker/setup.sh
```

In packaged installs, install the official `@openclaw/diagnostics-otel` plugin from ClawHub first; then allow + enable it and set `diagnostics.otel.enabled=true` (config example in source `/gateway/opentelemetry`). Collector auth headers go through `diagnostics.otel.headers`, **not** Docker env vars. Prometheus metrics use the already-published Gateway port: install `clawhub:@openclaw/diagnostics-prometheus`, enable `diagnostics-prometheus`, then scrape `http://<gateway-host>:18789/api/diagnostics/prometheus`. That route is protected by Gateway authentication — do not expose a separate public `/metrics` port (source `/gateway/prometheus`).

### Health checks

Container probe endpoints require no auth (`/healthz` liveness, `/readyz` readiness); the authenticated deep snapshot runs `health` inside the container:

```bash
curl -fsS http://127.0.0.1:18789/healthz   # liveness
curl -fsS http://127.0.0.1:18789/readyz     # readiness
docker compose exec openclaw-gateway node dist/index.js health --token "$OPENCLAW_GATEWAY_TOKEN"
```

The Docker image includes a built-in `HEALTHCHECK` that pings `/healthz`; if checks keep failing, Docker marks the container `unhealthy` and orchestration can restart or replace it.

### LAN vs loopback

`scripts/docker/setup.sh` defaults `OPENCLAW_GATEWAY_BIND=lan` so host access to `http://127.0.0.1:18789` works with Docker port publishing. `lan` (default) lets the host browser and CLI reach the published gateway port; `loopback` means only processes inside the container network namespace reach it directly. Use bind **mode** values in `gateway.bind` (`lan` / `loopback` / `custom` / `tailnet` / `auto`), not host aliases like `0.0.0.0` or `127.0.0.1`.

### Host Local Providers

In Docker, `127.0.0.1` inside the container is the container itself, not your host — use `host.docker.internal` for AI providers running on the host:

| Provider | Host default URL | Docker setup URL |
| --- | --- | --- |
| LM Studio | `http://127.0.0.1:1234` | `http://host.docker.internal:1234` |
| Ollama | `http://127.0.0.1:11434` | `http://host.docker.internal:11434` |

The bundled setup uses those host URLs as the LM Studio/Ollama onboarding defaults, and `docker-compose.yml` maps `host.docker.internal` to Docker's host gateway on Linux Docker Engine (Docker Desktop provides the hostname on macOS/Windows). Host services must also listen on a Docker-reachable address, e.g. `lms server start --port 1234 --bind 0.0.0.0` or `OLLAMA_HOST=0.0.0.0:11434 ollama serve`. With your own Compose file or `docker run`, add `--add-host=host.docker.internal:host-gateway` yourself.

### Bonjour / mDNS

Docker bridge networking usually does not forward Bonjour/mDNS multicast (`224.0.0.251:5353`) reliably, so the bundled Compose setup defaults `OPENCLAW_DISABLE_BONJOUR=1` to keep the Gateway from crash-looping when the bridge drops multicast. Use the published Gateway URL, Tailscale, or wide-area DNS-SD for Docker hosts; set `OPENCLAW_DISABLE_BONJOUR=0` only with host networking, macvlan, or another network where mDNS multicast works (source `/gateway/bonjour`).

### Storage and persistence

Docker Compose bind-mounts `OPENCLAW_CONFIG_DIR` to `/home/node/.openclaw`, `OPENCLAW_WORKSPACE_DIR` to `/home/node/.openclaw/workspace`, and `OPENCLAW_AUTH_PROFILE_SECRET_DIR` to `/home/node/.config/openclaw`, so those paths survive container replacement (when any is unset, the bundled `docker-compose.yml` falls back under `${HOME}`, or `/tmp` when `HOME` is also missing). The mounted config directory holds `openclaw.json` (behavior config), `agents/<agentId>/agent/auth-profiles.json` (stored provider OAuth/API-key auth), and `.env` (env-backed secrets such as `OPENCLAW_GATEWAY_TOKEN`). The auth-profile secret key directory stores the local encryption key for OAuth-backed token material — keep it with Docker host state but separate from `OPENCLAW_CONFIG_DIR`. Installed downloadable plugins store package state under the mounted home so install records survive container replacement. For full VM persistence the source defers to `/install/docker-vm-runtime#what-persists-where` — captured as [oc_install_docker_vm_runtime](oc_install_docker_vm_runtime.md). **Disk-growth hotspots**: `media/`, session JSONL files, the shared SQLite state database, plugin package roots, and rolling logs under `/tmp/openclaw/`.

### Shell helpers (optional)

For easier day-to-day Docker management, install `ClawDock`:

```bash
mkdir -p ~/.clawdock && curl -sL https://raw.githubusercontent.com/openclaw/openclaw/main/scripts/clawdock/clawdock-helpers.sh -o ~/.clawdock/clawdock-helpers.sh
echo 'source ~/.clawdock/clawdock-helpers.sh' >> ~/.zshrc && source ~/.zshrc
```

If you installed ClawDock from the older `scripts/shell-helpers/clawdock-helpers.sh` path, rerun the install command above. Then use `clawdock-start`, `clawdock-stop`, `clawdock-dashboard`, etc. (`clawdock-help` for all); see source `/install/clawdock`. The source's accordions in this section also cover automation/CI non-interactive runs (`docker compose run -T`), the shared-network security note (`openclaw-cli` uses `network_mode: "service:openclaw-gateway"`, dropping `NET_RAW`/`NET_ADMIN`, setting `no-new-privileges`), Docker Desktop DNS failures (`EAI_AGAIN`), `node` uid-1000 permissions (`EACCES`), faster rebuilds via Dockerfile layer caching, dep-baking, persisting `/home/node` (`OPENCLAW_HOME_VOLUME`), headless OpenAI Codex OAuth, and base-image metadata (`node:24-bookworm-slim`, `tini` as PID 1). The `OPENCLAW_SANDBOX=1` accordion is captured in [oc_install_docker_agent_sandbox](oc_install_docker_agent_sandbox.md).

### Running on a VPS?

For shared VM deployment steps (binary baking, persistence, updates) the source defers to `/install/hetzner` and `/install/docker-vm-runtime`, captured as [oc_install_hetzner](oc_install_hetzner.md) and [oc_install_docker_vm_runtime](oc_install_docker_vm_runtime.md).

## Troubleshooting

The source groups troubleshooting into accordions:

- **Image missing / sandbox container not starting** — build the sandbox image with `scripts/sandbox-setup.sh` (source checkout) or the inline `docker build` from `/gateway/sandboxing#images-and-setup` (npm), or set `agents.defaults.sandbox.docker.image` to a custom image; containers auto-create per session on demand.
- **Permission errors in sandbox** — set `docker.user` to a UID:GID matching mounted workspace ownership, or chown the folder.
- **Custom tools not found in sandbox** — OpenClaw runs commands with `sh -lc` (login shell), which sources `/etc/profile` and may reset PATH; set `docker.env.PATH` to prepend custom tool paths.
- **OOM-killed during image build (`exit 137`)** — the VM needs at least 2 GB RAM; use a larger machine class.
- **Unauthorized or pairing required in Control UI** — fetch a fresh dashboard link and approve the browser device by running `docker compose run --rm openclaw-cli dashboard --no-open`, then `devices list`, then `devices approve <requestId>` (see source `/web/dashboard`, `/cli/devices`).
- **Gateway target shows `ws://172.x.x.x` or pairing errors from the Docker CLI** — reset gateway mode and bind via `config set --batch-json '[{"path":"gateway.mode","value":"local"},{"path":"gateway.bind","value":"lan"}]'`, then `devices list --url ws://127.0.0.1:18789`.

**Source**: OpenClaw documentation — `install/docker` (mirror `inbox/openclaw_docs/install/docker.md`)
**Last Updated**: 2026-06-22
**Status**: Active
