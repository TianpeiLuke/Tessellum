---
tags:
  - resource
  - documentation
  - hermes_agent
  - api_server
  - deployment
keywords:
  - hermes api server setup
  - api_server_key bearer auth
  - api_server_cors_origins
  - multi-user profiles
  - gateway proxy mode
  - security headers
topics:
  - Hermes Agent
  - API Server
  - Deployment & Security
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
access_control_group: ["general"]
---

# Hermes API Server — Setup & Authentication

## Overview

This is the deployment-and-security half of the Hermes OpenAI-compatible API server: how to stand it up, lock it down, and run it for more than one user. The server is enabled and configured entirely through `API_SERVER_*` environment variables (config.yaml support is not yet available), guarded by a single required bearer token (`API_SERVER_KEY`), and hardened with fixed security headers plus an opt-in CORS allowlist. The same server also acts as the backend for gateway **proxy mode**, letting one Hermes instance forward all traffic to another. The endpoint data model itself (`/v1/chat/completions`, `/v1/responses`, runs/jobs/sessions, discovery, memory scoping) is documented separately in [hermes_api_server_endpoints](hermes_api_server_endpoints.md) — this note covers enablement, auth, CORS, multi-user, limits, and proxy mode.

## Quick Start

### 1. Enable the API server

Add to `~/.hermes/.env`:

```bash
API_SERVER_ENABLED=true
API_SERVER_KEY=change-me-local-dev
# Optional: only if a browser must call Hermes directly
# API_SERVER_CORS_ORIGINS=http://localhost:3000
```

### 2. Start the gateway

```bash
hermes gateway
```

You'll see `[API Server] API server listening on http://127.0.0.1:8642`.

### 3. Connect a frontend

Point any OpenAI-compatible client at `http://localhost:8642/v1`:

```bash
# Test with curl
curl http://localhost:8642/v1/chat/completions \
  -H "Authorization: Bearer change-me-local-dev" \
  -H "Content-Type: application/json" \
  -d '{"model": "hermes-agent", "messages": [{"role": "user", "content": "Hello!"}]}'
```

Or connect Open WebUI, LobeChat, or any other frontend — the Open WebUI integration guide (`/user-guide/messaging/open-webui`) has step-by-step instructions.

> Hermes itself needs a configured provider and tool backends for the API server to be useful. A Nous Portal subscription handles both — 300+ models plus web/image/TTS/browser via the Tool Gateway. Run `hermes setup --portal` once before starting the API server and frontends like Open WebUI or LobeChat get a fully tool-equipped backend.

## Authentication

Bearer token auth via the `Authorization` header:

```
Authorization: Bearer ***
```

Configure the key via the `API_SERVER_KEY` env var. If you need a browser to call Hermes directly, also set `API_SERVER_CORS_ORIGINS` to an explicit allowlist.

**Security warning (from source):** The API server gives full access to hermes-agent's toolset, **including terminal commands**. `API_SERVER_KEY` is **required for every deployment**, including the default loopback bind on `127.0.0.1`. Keep `API_SERVER_CORS_ORIGINS` narrow to control browser access when you explicitly allow browser callers.

## Configuration

The API server is configured through environment variables — config.yaml support is "Not yet supported … coming in a future release." Write `API_SERVER_*` variables to `~/.hermes/.env` (or a profile's `.env`).

| Variable | Default | Description |
|----------|---------|-------------|
| `API_SERVER_ENABLED` | `false` | Enable the API server |
| `API_SERVER_PORT` | `8642` | HTTP server port |
| `API_SERVER_HOST` | `127.0.0.1` | Bind address (localhost only by default) |
| `API_SERVER_KEY` | _(required)_ | Bearer token for auth |
| `API_SERVER_CORS_ORIGINS` | _(none)_ | Comma-separated allowed browser origins |
| `API_SERVER_MODEL_NAME` | _(profile name)_ | Model name on `/v1/models`. Defaults to profile name, or `hermes-agent` for default profile. |

The full env-var catalog reference is owned by the configuration sub-plan (SP02/SP21) — see [hermes_config_files_precedence](hermes_config_files_precedence.md).

## Security Headers

All responses include security headers:

- `X-Content-Type-Options: nosniff` — prevents MIME type sniffing
- `Referrer-Policy: no-referrer` — prevents referrer leakage

## CORS

The API server does **not** enable browser CORS by default. For direct browser access, set an explicit allowlist:

```bash
API_SERVER_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

When CORS is enabled:

- **Preflight responses** include `Access-Control-Max-Age: 600` (10 minute cache).
- **SSE streaming responses** include CORS headers so browser `EventSource` clients work correctly.
- **`Idempotency-Key`** is an allowed request header — clients can send it for deduplication (responses are cached by key for 5 minutes).

Most documented frontends such as Open WebUI connect server-to-server and do not need CORS at all.

## Compatible Frontends

Any frontend that supports the OpenAI API format works. Tested/documented integrations:

| Frontend | Stars | Connection |
|----------|-------|------------|
| Open WebUI | 126k | Full guide available |
| LobeChat | 73k | Custom provider endpoint |
| LibreChat | 34k | Custom endpoint in `librechat.yaml` |
| AnythingLLM | 56k | Generic OpenAI provider |
| NextChat | 87k | `BASE_URL` env var |
| ChatBox | 39k | API Host setting |
| Jan | 26k | Remote model config |
| HF Chat-UI | 8k | `OPENAI_BASE_URL` |
| big-AGI | 7k | Custom endpoint |
| OpenAI Python SDK | — | `OpenAI(base_url="http://localhost:8642/v1")` |
| curl | — | Direct HTTP requests |

## Multi-User Setup with Profiles

To give multiple users their own isolated Hermes instance (separate config, memory, skills), use profiles. Because `API_SERVER_*` are env vars (not config.yaml keys), each profile's settings are written to its own `.env`, and each profile's API server runs on a different port:

```bash
# Create a profile per user
hermes profile create alice
hermes profile create bob

# Configure each profile's API server on a different port. API_SERVER_* are env
# vars (not config.yaml keys), so write them to each profile's .env:
cat >> ~/.hermes/profiles/alice/.env <<EOF
API_SERVER_ENABLED=true
API_SERVER_PORT=8643
API_SERVER_KEY=alice-secret
EOF

cat >> ~/.hermes/profiles/bob/.env <<EOF
API_SERVER_ENABLED=true
API_SERVER_PORT=8644
API_SERVER_KEY=bob-secret
EOF

# Start each profile's gateway
hermes -p alice gateway &
hermes -p bob gateway &
```

Each profile's API server automatically advertises the profile name as the model ID — `http://localhost:8643/v1/models` → model `alice`, `http://localhost:8644/v1/models` → model `bob`. In Open WebUI, add each as a separate connection; the model dropdown shows `alice` and `bob` as distinct models, each backed by a fully isolated Hermes instance. (Profiles themselves are owned by SP04; the Open WebUI multi-user guide lives at `/user-guide/messaging/open-webui#multi-user-setup-with-profiles`.)

## Limitations

- **Response storage** — stored responses (for `previous_response_id`) are persisted in SQLite and survive gateway restarts. Max 100 stored responses (LRU eviction).
- **No file upload** — inline images are supported on both `/v1/chat/completions` and `/v1/responses`, but uploaded files (`file`, `input_file`, `file_id`) and non-image document inputs are not supported through the API.
- **Model field is cosmetic** — the `model` field in requests is accepted but the actual LLM model used is configured server-side in config.yaml.

## Proxy Mode

The API server also serves as the backend for **gateway proxy mode**. When another Hermes gateway instance is configured with `GATEWAY_PROXY_URL` pointing at this API server, it forwards all messages here instead of running its own agent. This enables split deployments — for example, a Docker container handling Matrix E2EE that relays to a host-side agent. The full Matrix proxy setup guide (`/user-guide/messaging/matrix#proxy-mode-e2ee-on-macos`) is owned by the messaging sub-plan (SP11).

**Source**: `inbox/hermes_agent_docs/user-guide/features/api-server.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
**Last Updated**: 2026-06-19
**Status**: Active
