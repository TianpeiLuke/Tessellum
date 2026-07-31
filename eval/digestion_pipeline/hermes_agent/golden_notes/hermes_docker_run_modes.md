---
tags:
  - resource
  - documentation
  - hermes_agent
  - docker
  - deployment
keywords:
  - hermes in docker
  - gateway run mode
  - dashboard container
  - docker run setup wizard
  - docker compose hermes
  - image upgrade migration
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

# Hermes Agent — Docker Run Modes

## Overview

This note is the procedure for **running Hermes Agent itself inside a Docker container** — the first of the two distinct ways Docker intersects with Hermes (the second, Docker as a *terminal backend* where the host-resident agent executes commands inside a sandbox, is a separate config block owned elsewhere — see Related Notes). The container is stateless; all user data (config, API keys, sessions, skills, memories) lives in a single host directory mounted at `/opt/data`, so the image can be upgraded by pulling a new version without losing configuration. It covers first-run `setup`, persistent `gateway run`, the web dashboard, interactive CLI chat, environment-variable forwarding, the canonical `docker-compose.yaml`, upgrading, and resource sizing. The `/opt/data` volume + s6 supervision model and the tool-extension / local-inference procedures are documented in sibling notes (link-outs below) and are NOT repeated here.

## Quick start (first-run setup wizard)

For a first run, create a host data directory and start the container interactively to run the setup wizard. (For VPS providers with browser-based consoles, connect over SSH instead — those consoles silently corrupt special characters in `docker run` arguments like `-v ~/.hermes:/opt/data`, `-e KEY=value`, and pasted keys.)

```sh
mkdir -p ~/.hermes
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent setup
```

This drops you into the setup wizard, which prompts for your API keys and writes them to `~/.hermes/.env`. You only need to do this once, and it is recommended to configure a chat system for the gateway at this point. Inside the container, run `hermes setup --portal` once — the refresh token persists in the mounted `~/.hermes` volume (see Nous Portal).

## Running in gateway mode

Once configured, run the container in the background as a persistent gateway (Telegram, Discord, Slack, WhatsApp, etc.):

```sh
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  -p 8642:8642 \
  nousresearch/hermes-agent gateway run
```

Port 8642 exposes the gateway's OpenAI-compatible API server and health endpoint. It is optional if you only use chat platforms, but required if you want the dashboard or external tools to reach the gateway.

Inside the official Docker image, `gateway run` is **automatically supervised by s6-overlay** (the run modes here write into the s6/`/opt/data` runtime model documented in the volumes/supervision sibling note): a crashed gateway is restarted within seconds without losing the container, the `gateway run` CMD process is a `sleep infinity` heartbeat that keeps the container alive while s6 manages the actual gateway process, so `docker stop` still shuts everything down cleanly. To opt out and get the historical "gateway is the container's main process, container exit = gateway exit" semantics, pass `--no-supervise` or set `HERMES_GATEWAY_NO_SUPERVISE=1` (useful for CI smoke tests that want the container to exit with the gateway's status code).

The API server is gated on `API_SERVER_ENABLED=true`. To expose it beyond `127.0.0.1` inside the container, add `-e API_SERVER_ENABLED=true`, `-e API_SERVER_HOST=0.0.0.0`, an `-e API_SERVER_KEY="$(openssl rand -hex 32)"` (minimum 8 characters), and `-e API_SERVER_CORS_ORIGINS='*'` to the `gateway run` invocation above. Opening any port on an internet-facing machine is a security risk; do not do it unless you understand the risks.

## Running the dashboard

The built-in web dashboard runs as a supervised s6-rc service alongside the gateway in the same container. Set `HERMES_DASHBOARD=1` to bring it up, publishing port 9119:

```sh
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  -p 8642:8642 \
  -p 9119:9119 \
  -e HERMES_DASHBOARD=1 \
  nousresearch/hermes-agent gateway run
```

The dashboard is supervised by s6 — if it crashes, `s6-supervise` restarts it after a short backoff — and its stdout/stderr is forwarded to `docker logs <container>`. The relevant control env vars: `HERMES_DASHBOARD` (set `1`/`true`/`yes` to enable the supervised service; default unset), `HERMES_DASHBOARD_HOST` (bind address; default `0.0.0.0`), `HERMES_DASHBOARD_PORT` (default `9119`), and `HERMES_DASHBOARD_INSECURE` (set `1`/`true`/`yes` to bind without the OAuth auth gate; default unset). The dashboard inside the container defaults to binding `0.0.0.0`, otherwise the published `-p 9119:9119` port would not be reachable from the host; set `HERMES_DASHBOARD_HOST=127.0.0.1` to restrict the bind to loopback for sidecar/reverse-proxy setups.

The dashboard's auth gate engages automatically when the bind host is non-loopback **and** a `DashboardAuthProvider` plugin is registered (bundled providers: username/password, OAuth via Nous Portal, and self-hosted OIDC). If no provider is registered and the bind is non-loopback, the dashboard **fails closed at startup**; `HERMES_DASHBOARD_INSECURE=1` is the explicit escape hatch (serves an unauthenticated dashboard — only use behind your own auth layer). The auth-provider details (the three bundled providers and their env vars) belong to the Web Dashboard feature doc — see the link-out in Related Notes.

## Running interactively (CLI chat)

To open an interactive chat session against a running data directory, run `docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent` (no subcommand → defaults to `hermes`). Or, if you have already opened a terminal in your running container (via Docker Desktop, for instance), run the venv binary directly: `/opt/hermes/.venv/bin/hermes`.

## Environment variable forwarding

API keys are read from `/opt/data/.env` inside the container, but you can also pass environment variables directly with `-e` flags — e.g. `-e ANTHROPIC_API_KEY="sk-ant-..."` and `-e OPENAI_API_KEY="sk-..."` on the `docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent` invocation. Direct `-e` flags override values from `.env`. This is useful for CI/CD or secrets-manager integrations where you don't want keys on disk.

## Docker Compose example

For persistent deployment with both the gateway and dashboard, a `docker-compose.yaml` is convenient:

```yaml
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    ports:
      - "8642:8642"   # gateway API
      - "9119:9119"   # dashboard (only reached when HERMES_DASHBOARD=1)
    volumes:
      - ~/.hermes:/opt/data
    environment:
      - HERMES_DASHBOARD=1
      # Uncomment to forward specific env vars instead of using .env file:
      # - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      # - OPENAI_API_KEY=${OPENAI_API_KEY}
      # - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
```

Start with `docker compose up -d` and view logs with `docker compose logs -f`.

## Upgrading

Pull the latest image and recreate the container. Your data directory is preserved, and the container runs non-interactive config-schema migrations against the mounted `$HERMES_HOME/config.yaml` before starting the gateway; when a migration is needed, Hermes writes timestamped backups next to `config.yaml` and `.env` first.

```sh
docker pull nousresearch/hermes-agent:latest
docker rm -f hermes
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

Or with Docker Compose: `docker compose pull` then `docker compose up -d`. Set `HERMES_SKIP_CONFIG_MIGRATION=1` only if you need to inspect or migrate the persisted config manually before letting the new image rewrite it.

## Resource limits

The Hermes container needs moderate resources. Recommended minimums: Memory 1 GB minimum / 2–4 GB recommended; CPU 1 core minimum / 2 cores recommended; data-volume disk 500 MB minimum / 2+ GB recommended (grows with sessions/skills). Browser automation (Playwright/Chromium) is the most memory-hungry feature — without browser tools 1 GB suffices, with them active allocate at least 2 GB. Set limits via Docker flags:

```sh
docker run -d \
  --name hermes \
  --restart unless-stopped \
  --memory=4g --cpus=2 \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent gateway run
```

**Source**: `inbox/hermes_agent_docs/user-guide/docker.md` · https://hermes-agent.nousresearch.com/docs/user-guide/docker
**Last Updated**: 2026-06-19
**Status**: Active
