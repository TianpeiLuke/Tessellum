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

## Related Notes

**Terms**
- [term_authentication](../../term_dictionary/term_authentication.md) — identity proof; relevance: bearer-token auth required on every deploy incl. loopback.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — bearer token; relevance: `API_SERVER_KEY` is the bearer presented in `Authorization`.
- [term_rest](../../term_dictionary/term_rest.md) — HTTP surface; relevance: setup stands up the REST endpoints behind one auth.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — forwarding proxy; relevance: proxy mode (`GATEWAY_PROXY_URL`) forwards to another gateway.
- [term_proxy_pattern](../../term_dictionary/term_proxy_pattern.md) — proxy design pattern; relevance: the split-deployment relay (Docker Matrix → host agent).
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: per-profile isolation gives each user a separate session/memory store.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — request dedup; relevance: `Idempotency-Key` is an allowed CORS request header.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: the API server gives full toolset access incl. terminal — the security warning.
- [term_oauth](../../term_dictionary/term_oauth.md) — OAuth 2.1 framework; relevance: portal-backed provider setup feeds the server's credentials.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — terminal coding agent; relevance: the toolset the server exposes is a full coding agent.

**Code-Repos**
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway hosting the API server; relevance: `hermes gateway` boots the API server, applies auth middleware + security headers + CORS.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes profile create` / `hermes -p <profile> gateway`; relevance: per-profile multi-user setup on separate ports.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider boot; relevance: the API server needs a configured provider before it is useful.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — agent turn dispatch; relevance: authenticated requests dispatch into the core agent.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties env-var enablement (`API_SERVER_*`) into startup.

**Snippets**
- [gw_platform_api_server_middleware](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_middleware.md) — auth/CORS/security-header middleware; relevance: the bearer-token auth + CORS allowlist + security headers this page configures.
- [gw_platform_api_server_connect](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_connect.md) — server boot; relevance: `API_SERVER_*` env enablement + gateway boot.
- [gw_platform_api_server_routes](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_routes.md) — protected routes; relevance: the REST routes that sit behind the single bearer auth.
- [gw_runner_provider_boot](../../code_snippets/snippet_hermes_agent_gw_runner_provider_boot.md) — provider boot; relevance: a configured provider is required before the API server is useful.
- [gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — per-profile sessions; relevance: per-profile multi-user isolation gives each user a separate session store.
- [gw_run_helpers](../../code_snippets/snippet_hermes_agent_gw_run_helpers.md) — run dispatch; relevance: authenticated requests dispatch into runs.
- [gw_runner_acl](../../code_snippets/snippet_hermes_agent_gw_runner_acl.md) — access control; relevance: the full-toolset-access security warning + per-profile ACL.
- [gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — outbound proxy forward; relevance: gateway proxy mode (`GATEWAY_PROXY_URL`) forwards to another gateway.
- [gw_start_gateway_main](../../code_snippets/snippet_hermes_agent_gw_start_gateway_main.md) — `hermes gateway` main; relevance: the gateway entrypoint that starts the API server on a chosen port.
- [gw_runner_init](../../code_snippets/snippet_hermes_agent_gw_runner_init.md) — runner init; relevance: per-profile runner init on separate ports for multi-user setup.

**Docs**
- [hermes_api_server_endpoints](hermes_api_server_endpoints.md) — endpoint surface; relevance: same server, data-model half.
- [hermes_subscription_proxy](hermes_subscription_proxy.md) — contrasting proxy; relevance: the page explicitly contrasts API server vs proxy auth.
- [hermes_mcp_concept_config](hermes_mcp_concept_config.md) — config surface; relevance: shares the `~/.hermes/.env` + config model.
- [hermes_config_files_precedence](hermes_config_files_precedence.md) — env-var/config reference; relevance: SP02/SP21 own the `API_SERVER_*` env catalog this links out to.
- [hermes_credential_pools](hermes_credential_pools.md) — provider credentials; relevance: per-profile providers feed credential pools.
- [cc_authentication](../claude_code/cc_authentication.md) — agent auth; relevance: analogous bearer/token auth setup.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network/TLS controls; relevance: analogous CORS/security-header hardening.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: direct analogue to gateway proxy mode.
- [cc_sdk_hosting_provisioning_and_scaling](../claude_code/cc_sdk_hosting_provisioning_and_scaling.md) — hosting/scaling; relevance: analogous multi-user deployment topology.
- [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure deploy; relevance: analogous "auth required on every deploy" guidance.

**Source**: `inbox/hermes_agent_docs/user-guide/features/api-server.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
**Last Updated**: 2026-06-19
**Status**: Active
