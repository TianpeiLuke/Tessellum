---
tags:
  - resource
  - documentation
  - hermes_agent
  - matrix
  - deployment
keywords:
  - matrix proxy mode
  - e2ee on macos
  - gateway proxy url
  - api_server host agent
  - thin docker matrix adapter
  - x-hermes-session-id continuity
topics:
  - Hermes Agent
  - Messaging Gateway
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/matrix
access_control_group: ["general"]
---

# Hermes Messaging — Matrix Proxy Mode (E2EE on macOS)

## Overview

Proxy mode is a **two-process deployment model** for running Matrix end-to-end encryption (E2EE) on macOS. It exists because Matrix E2EE requires `libolm`, which does not compile on macOS ARM64 (Apple Silicon) — the `hermes-agent[matrix]` extra is gated to Linux only. Rather than give up E2EE on a Mac, proxy mode **splits the gateway across two machines**: a thin Hermes instance runs the Matrix adapter (E2EE decrypt/encrypt only) inside a Docker container on a Linux VM, and the real agent — `AIAgent`, sessions, memory, skills, and local file access — runs natively on macOS. The container decrypts an inbound Matrix message, HTTP-forwards the plaintext to the host's `api_server` (port 8642), the host runs the full agent turn, streams the response back, and the container re-encrypts and sends it to Matrix. The container holds **no LLM API keys, no agent, and no inference** — it is purely a Matrix-protocol + crypto front-end. The model is **not limited to Matrix**: setting `GATEWAY_PROXY_URL` on any gateway instance forwards to a remote agent, so the same host↔adapter split works for any platform that needs to run in a different environment from the agent (network isolation, E2EE requirements, resource constraints).

## How It Works

The host (macOS) runs the full gateway and is the single source of truth; the Linux VM container runs only the Matrix adapter and forwards over HTTP:

```
macOS (Host):
  └─ hermes gateway
       ├─ api_server adapter ← listens on 0.0.0.0:8642
       ├─ AIAgent ← single source of truth
       ├─ Sessions, memory, skills
       └─ Local file access (Obsidian, projects, etc.)

Linux VM (Docker):
  └─ hermes gateway (proxy mode)
       ├─ Matrix adapter ← E2EE decryption/encryption
       └─ HTTP forward → macOS:8642/v1/chat/completions
           (no LLM API keys, no agent, no inference)
```

The Docker container only handles the Matrix protocol plus E2EE. When a message arrives it decrypts the text and forwards it to the host via a standard HTTP request. The host runs the agent, calls tools, generates a response, and streams it back; the container then encrypts and sends the response to Matrix. **All sessions are unified** — CLI, Matrix, Telegram, and any other platform share the same memory and conversation history on the host.

## Step 1: Configure the Host (macOS)

Enable the API server so the host accepts incoming requests from the Docker container. Add to `~/.hermes/.env`:

```bash
API_SERVER_ENABLED=true
API_SERVER_KEY=your-secret-key-here
API_SERVER_HOST=0.0.0.0
```

- `API_SERVER_HOST=0.0.0.0` binds to all interfaces so the Docker container can reach it.
- `API_SERVER_KEY` is required for non-loopback binding. Pick a strong random string.
- The API server runs on port 8642 by default (change with `API_SERVER_PORT` if needed).

Start the gateway with `hermes gateway`. You should see the API server start alongside any other platforms you have configured. Verify it is reachable from the VM:

```bash
# From the Linux VM
curl http://<mac-ip>:8642/health
```

## Step 2: Configure the Docker Container (Linux VM)

The container needs Matrix credentials and the proxy URL. It does **not** need LLM API keys.

`docker-compose.yml`:

```yaml
services:
  hermes-matrix:
    build: .
    environment:
      # Matrix credentials
      MATRIX_HOMESERVER: "https://matrix.example.org"
      MATRIX_ACCESS_TOKEN: "syt_..."
      MATRIX_ALLOWED_USERS: "@you:matrix.example.org"
      MATRIX_ENCRYPTION: "true"
      MATRIX_DEVICE_ID: "HERMES_BOT"

      # Proxy mode — forward to host agent
      GATEWAY_PROXY_URL: "http://192.168.1.100:8642"
      GATEWAY_PROXY_KEY: "your-secret-key-here"
    volumes:
      - ./matrix-store:/root/.hermes/platforms/matrix/store
```

`Dockerfile`:

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y libolm-dev && rm -rf /var/lib/apt/lists/*
RUN pip install 'hermes-agent[matrix]'

CMD ["hermes", "gateway"]
```

That is the entire container — no API keys for OpenRouter, Anthropic, or any inference provider.

## Step 3: Start Both

1. Start the host gateway first: `hermes gateway`
2. Start the Docker container: `docker compose up -d`
3. Send a message in an encrypted Matrix room. The container decrypts it, forwards it to the host, and streams the response back.

## Configuration Reference

Proxy mode is configured on the **container side** (the thin gateway):

| Setting | Description |
|---------|-------------|
| `GATEWAY_PROXY_URL` | URL of the remote Hermes API server (e.g., `http://192.168.1.100:8642`) |
| `GATEWAY_PROXY_KEY` | Bearer token for authentication (must match `API_SERVER_KEY` on the host) |
| `gateway.proxy_url` | Same as `GATEWAY_PROXY_URL` but in `config.yaml` |

The **host side** needs:

| Setting | Description |
|---------|-------------|
| `API_SERVER_ENABLED` | Set to `true` |
| `API_SERVER_KEY` | Bearer token (shared with the container) |
| `API_SERVER_HOST` | Set to `0.0.0.0` for network access |
| `API_SERVER_PORT` | Port number (default: `8642`) |

## Works for Any Platform

Proxy mode is not limited to Matrix. Any platform adapter can use it — set `GATEWAY_PROXY_URL` on any gateway instance and it will forward to the remote agent instead of running one locally. This is useful for any deployment where the platform adapter needs to run in a different environment from the agent (network isolation, E2EE requirements, resource constraints).

**Session continuity** is maintained via the `X-Hermes-Session-Id` header. The host's API server tracks sessions by this ID, so conversations persist across messages just like they would with a local agent.

**Limitations (v1):** Tool progress messages from the remote agent are not relayed back — the user sees the streamed final response only, not individual tool calls. Dangerous-command approval prompts are handled on the host side, not relayed to the Matrix user. These can be addressed in future updates.

## Troubleshooting: Sync

### Bot connects and sends, but ignores inbound messages

**Cause**: Matrix event handlers only fire when sync payloads are dispatched through mautrix's `handle_sync()` machinery. A raw `client.sync()` poll that never calls `handle_sync()` can leave the adapter connected (send works) while inbound messages never reach `_on_room_message`.

**Fix**: Hermes uses an explicit sync loop that calls `client.handle_sync()` on both the initial sync and every incremental sync response. This matches the diagnosis in upstream issue #7914 and closed PR #37807, but keeps Hermes's own background maintenance tasks (joined-room tracking, invite handling, E2EE key share) instead of delegating the full lifecycle to `client.start()`. If inbound messages still fail after a gateway restart, verify handlers are registered before the first sync and check logs for `sync event dispatch error`.

### Sync issues / bot falls behind

**Cause**: Long-running tool executions can delay the sync loop, or the homeserver is slow.

**Fix**: The sync loop automatically retries every 5 seconds on error. Check the Hermes logs for sync-related warnings. If the bot consistently falls behind, ensure your homeserver has adequate resources.

**Source**: `inbox/hermes_agent_docs/user-guide/messaging/matrix.md` (§Proxy Mode) · https://hermes-agent.nousresearch.com/docs/user-guide/messaging/matrix
**Last Updated**: 2026-06-19
**Status**: Active
