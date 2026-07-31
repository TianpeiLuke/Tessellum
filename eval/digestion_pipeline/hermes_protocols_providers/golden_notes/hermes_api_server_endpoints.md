---
tags:
  - resource
  - documentation
  - hermes_agent
  - api_server
  - protocols
keywords:
  - hermes api server endpoints
  - openai-compatible api
  - chat completions responses
  - runs jobs sessions api
  - x-hermes-session-key
  - previous_response_id
topics:
  - Hermes Agent
  - API Server
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
access_control_group: ["general"]
---

# Hermes Agent — API Server Endpoints

## Overview

The API server endpoint surface is the **OpenAI-compatible HTTP data model** that exposes hermes-agent as a backend any OpenAI-format frontend (Open WebUI, LobeChat, LibreChat, NextChat, ChatBox, and hundreds more) can drive. It is a REST surface spanning chat-completions, a stateful Responses API, a runs API, jobs CRUD, sessions-over-REST, and capability/skills/toolsets discovery — each request handled by the agent with its full toolset (terminal, file operations, web search, memory, skills) returning the final response. This note documents the request/response *shapes* and behaviors; standing the server up, securing it, and deploying it are covered in the [setup/auth counterpart](hermes_api_server_setup_auth.md).

## Endpoints

### POST /v1/chat/completions

Standard OpenAI Chat Completions format. Stateless — the full conversation is included in each request via the `messages` array.

```json
{
  "model": "hermes-agent",
  "messages": [
    {"role": "system", "content": "You are a Python expert."},
    {"role": "user", "content": "Write a fibonacci function"}
  ],
  "stream": false
}
```

The response is a standard `chat.completion` object carrying `id`, `object`, `created`, `model`, a `choices` array (each with `index`, `message`, `finish_reason`), and a `usage` block (`prompt_tokens` / `completion_tokens` / `total_tokens`).

**Inline image input:** user messages may send `content` as an array of `text` and `image_url` parts. Both remote `http(s)` URLs and `data:image/...` URLs are supported. Uploaded files (`file` / `input_file` / `file_id`) and non-image `data:` URLs return `400 unsupported_content_type`.

**Streaming** (`"stream": true`): Returns Server-Sent Events (SSE) with token-by-token response chunks. For **Chat Completions**, the stream uses standard `chat.completion.chunk` events plus Hermes' custom `hermes.tool.progress` event for tool-start UX — emitted for tool-start visibility without polluting persisted assistant text. For **Responses**, the stream uses OpenAI Responses event types such as `response.created`, `response.output_text.delta`, `response.output_item.added`, `response.output_item.done`, and `response.completed`, and Hermes emits spec-native `function_call` and `function_call_output` output items so clients can render structured tool UI in real time.

### POST /v1/responses

OpenAI Responses API format. Supports server-side conversation state via `previous_response_id` — the server stores full conversation history (including tool calls and results) so multi-turn context is preserved without the client managing it.

```json
{
  "id": "resp_abc123",
  "object": "response",
  "status": "completed",
  "model": "hermes-agent",
  "output": [
    {"type": "function_call", "name": "terminal", "arguments": "{\"command\": \"ls\"}", "call_id": "call_1"},
    {"type": "function_call_output", "call_id": "call_1", "output": "README.md src/ tests/"},
    {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "Your project has..."}]}
  ],
  "usage": {"input_tokens": 50, "output_tokens": 200, "total_tokens": 250}
}
```

The request takes `model`, `input` (string or an `input[].content` array of `input_text` / `input_image` parts — remote URLs and `data:image/...` supported), an optional `instructions` field, and `store`. Uploaded files (`input_file` / `file_id`) and non-image `data:` URLs return `400 unsupported_content_type`.

- **Multi-turn with `previous_response_id`** — chaining a request with `previous_response_id` reconstructs the full conversation from the stored response chain; all previous tool calls and results are preserved, and chained requests share the same session so a multi-turn conversation appears as a single entry in the dashboard and session history.
- **Named conversations** — passing a `conversation` parameter (e.g. `"conversation": "my-project"`) instead of tracking response IDs makes the server automatically chain to the latest response in that conversation, like the `/title` command for gateway sessions.
- **`GET /v1/responses/{id}`** retrieves a previously stored response by ID; **`DELETE /v1/responses/{id}`** deletes a stored response.

### Models, capabilities, and health

- **`GET /v1/models`** — lists the agent as an available model. The advertised model name defaults to the profile name (or `hermes-agent` for the default profile). Required by most frontends for model discovery.
- **`GET /v1/capabilities`** — returns a machine-readable description of the API server's stable surface for external UIs, orchestrators, and plugin bridges, so they can discover whether the running Hermes version supports runs, streaming, cancellation, and session continuity without depending on private Python internals.

```json
{
  "object": "hermes.api_server.capabilities",
  "platform": "hermes-agent",
  "model": "hermes-agent",
  "auth": {"type": "bearer", "required": true},
  "features": {
    "chat_completions": true,
    "responses_api": true,
    "run_submission": true,
    "run_status": true,
    "run_events_sse": true,
    "run_stop": true
  }
}
```

- **`GET /health`** — health check returning `{"status": "ok"}`; also available at **`GET /v1/health`** for clients expecting the `/v1/` prefix.
- **`GET /health/detailed`** — extended health check that also reports active sessions, running agents, and resource usage, for monitoring/observability tooling.

## Runs API (streaming-friendly alternative)

In addition to `/v1/chat/completions` and `/v1/responses`, the server exposes a **runs** API for long-form sessions where the client wants to subscribe to progress events instead of managing streaming themselves.

- **`POST /v1/runs`** — create a new agent run; returns a `run_id` (with `status: "started"`) used to subscribe to progress events. Runs accept a simple `input` string and optional `session_id`, `instructions`, `conversation_history`, or `previous_response_id`. When `session_id` is provided, Hermes surfaces it in the run status so external UIs can correlate runs with their own conversation IDs.
- **`GET /v1/runs/{run_id}`** — poll the current run state (a `hermes.run` object carrying `status`, `session_id`, `model`, `output`, `usage`). Useful for dashboards that need status without holding an SSE connection open, or UIs that reconnect after navigation. Statuses are retained briefly after terminal states (`completed`, `failed`, or `cancelled`) for polling and UI reconciliation.
- **`GET /v1/runs/{run_id}/events`** — Server-Sent Events stream of the run's tool-call progress, token deltas, and lifecycle events. Designed for dashboards and thick clients that want to attach/detach without losing state.
- **`POST /v1/runs/{run_id}/stop`** — interrupt a running agent turn. Returns immediately with `{"status": "stopping"}` while Hermes asks the active agent to stop at the next safe interruption point.
- **`POST /v1/runs/{run_id}/approval`** — resolve a pending approval for a run waiting on a human decision (e.g. a tool call gated behind an approval policy). The body carries the approval decision; the run resumes once it is recorded. Advertised in `/v1/capabilities` as the `run_approval` feature so external UIs can detect support before surfacing an approval prompt.

## Jobs API (background scheduled work)

The server exposes a lightweight jobs CRUD surface for managing scheduled / background agent runs from a remote client. All endpoints are gated behind the same bearer auth.

- **`GET /api/jobs`** — list all scheduled jobs.
- **`POST /api/jobs`** — create a new scheduled job. Body accepts the same shape as `hermes cron` — prompt, schedule, skills, provider override, delivery target.
- **`GET /api/jobs/{job_id}`** — fetch a single job's definition and last-run state.
- **`PATCH /api/jobs/{job_id}`** — update fields on an existing job (prompt, schedule, etc.); partial updates are merged.
- **`DELETE /api/jobs/{job_id}`** — remove a job; also cancels any in-flight run.
- **`POST /api/jobs/{job_id}/pause`** — pause a job without deleting it; next-scheduled-run timestamps are suspended until resumed.
- **`POST /api/jobs/{job_id}/resume`** — resume a previously paused job.
- **`POST /api/jobs/{job_id}/run`** — trigger the job to run immediately, out of schedule.

## Sessions API (session control over REST)

External UIs can manage Hermes sessions over REST without standing up the dashboard. All endpoints are gated by `API_SERVER_KEY` and live under `/api/sessions/*`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/sessions` | List sessions (paginated — `limit`, `offset`, `source`, `include_children`) |
| `POST` | `/api/sessions` | Create an empty session |
| `GET` | `/api/sessions/{id}` | Read session metadata |
| `PATCH` | `/api/sessions/{id}` | Update title or `end_reason` |
| `DELETE` | `/api/sessions/{id}` | Delete a session |
| `GET` | `/api/sessions/{id}/messages` | Message history for a session |
| `POST` | `/api/sessions/{id}/fork` | Branch the session via `SessionDB` lineage (matches CLI `/branch` semantics) |
| `POST` | `/api/sessions/{id}/chat` | Run one synchronous agent turn |
| `POST` | `/api/sessions/{id}/chat/stream` | SSE wrapper over a single turn — emits `assistant.delta`, `tool.started`, `tool.completed`, `run.completed` events |

`/v1/capabilities` advertises the full surface via `session_*` feature flags and `endpoints.session_*` entries so external UIs can detect support and fall back safely. Inline images are supported in `chat` and `chat/stream` payloads (multimodal-aware path).

```bash
# fork a session and run one turn
curl -X POST http://localhost:8642/api/sessions/$ID/fork \
  -H "Authorization: Bearer $API_SERVER_KEY" \
  -d '{"title": "explore alt path"}'

# stream a turn over SSE
curl -N -X POST http://localhost:8642/api/sessions/$ID/chat/stream \
  -H "Authorization: Bearer $API_SERVER_KEY" \
  -d '{"input": "what files changed in the last hour?"}'
```

## Skills and Toolsets Discovery

`GET /v1/skills` and `GET /v1/toolsets` let external clients enumerate the agent's capabilities deterministically over REST instead of asking the model. Both are read-only and gated by `API_SERVER_KEY`.

```bash
curl http://localhost:8642/v1/skills \
  -H "Authorization: Bearer $API_SERVER_KEY"
# → [{"name": "github-pr-workflow", "description": "...", "category": "..."}, ...]

curl http://localhost:8642/v1/toolsets \
  -H "Authorization: Bearer $API_SERVER_KEY"
# → [{"name": "core", "label": "...", "description": "...", "enabled": true,
#     "configured": true, "tools": ["read_file", "write_file", ...]}, ...]
```

`/v1/skills` returns the same metadata the skills hub uses internally. `/v1/toolsets` returns toolsets resolved for the `api_server` platform with the concrete `tools` list each one expands to. Both are advertised under `endpoints.*` in `/v1/capabilities`.

## Long-term Memory Scoping (`X-Hermes-Session-Key`)

Multi-user frontends like Open WebUI need a stable per-channel identifier for long-term memory (Honcho, etc.) that is **independent** of the transcript-scoped `X-Hermes-Session-Id` (which rotates on `/new`). Pass `X-Hermes-Session-Key` on `/v1/chat/completions`, `/v1/responses`, or `/v1/runs` and Hermes threads it through to `AIAgent(gateway_session_key=...)`, where the Honcho memory provider uses it to derive a stable scope.

```http
POST /v1/chat/completions HTTP/1.1
Authorization: Bearer ***
X-Hermes-Session-Id: transcript-alpha
X-Hermes-Session-Key: agent:main:webui:dm:user-42
```

Rules: max 256 chars, control characters (`\r`, `\n`, `\x00`) are rejected, and the value is echoed back on responses (JSON + SSE). `/v1/capabilities` advertises support via `"session_key_header": "X-Hermes-Session-Key"`. Without the key, Honcho's `per-session` strategy produces a different scope per `session_id` — exactly the behavior Hermes had before.

## System Prompt Handling

When a frontend sends a `system` message (Chat Completions) or `instructions` field (Responses API), hermes-agent **layers it on top** of its core system prompt. The agent keeps all its tools, memory, and skills — the frontend's system prompt adds extra instructions. This means behavior can be customized per-frontend without losing capabilities: e.g. an Open WebUI system prompt "You are a Python expert. Always include type hints." while the agent still has terminal, file tools, web search, memory, etc.

## Related Notes

**Terms**
- [term_rest](../../term_dictionary/term_rest.md) — REST/HTTP resource model; relevance: the whole surface is a REST data model (chat/responses/runs/jobs/sessions).
- [term_sse](../../term_dictionary/term_sse.md) — Server-Sent Events; relevance: streaming responses + runs `/events` + `/chat/stream` emit SSE event types.
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: `/v1/responses` stores chains via `previous_response_id`; sessions API persists over REST.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — multi-input model; relevance: inline `image_url`/`input_image` parts on chat/responses/sessions payloads.
- [term_computer_vision](../../term_dictionary/term_computer_vision.md) — image understanding; relevance: the multimodal image path feeds vision analysis.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — request dedup; relevance: `Idempotency-Key` cached 5 min for dedup.
- [term_caching](../../term_dictionary/term_caching.md) — response cache; relevance: stored responses use LRU eviction (max 100).
- [term_lru_cache](../../term_dictionary/term_lru_cache.md) — least-recently-used eviction; relevance: the exact eviction policy for stored responses.
- [term_subagent](../../term_dictionary/term_subagent.md) — delegated agent; relevance: run events are push-style and runs can spawn delegated work.
- [term_webhook](../../term_dictionary/term_webhook.md) — server-push notifications; relevance: run events are push-style. (+Phase 0: [term_pkce](../../term_dictionary/term_pkce.md); +fin: term_nous_portal, term_tool_gateway)

**Code-Repos**
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the gateway that hosts the API server; relevance: `hermes gateway` exposes the OpenAI-compatible routes, runs/jobs/sessions APIs.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `AIAgent` + conversation loop; relevance: each endpoint dispatches into the core agent turn (incl. `gateway_session_key`).
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — skills/toolsets discovery; relevance: `/v1/skills` + `/v1/toolsets` enumerate the registry.
- [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — jobs CRUD backing; relevance: `/api/jobs/*` mirrors `hermes cron` shape.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties the API-server routing into the agent runtime.

**Snippets**
- [snippet_hermes_agent_gw_platform_api_server_routes](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_routes.md) — route table; relevance: the `/v1/chat/completions` + `/v1/responses` + runs/jobs/sessions/skills/toolsets endpoint surface.
- [snippet_hermes_agent_gw_platform_api_server_connect](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_connect.md) — API-server connect/boot; relevance: stands up the OpenAI-compatible server inside the gateway.
- [snippet_hermes_agent_gw_run_helpers](../../code_snippets/snippet_hermes_agent_gw_run_helpers.md) — runs API helpers; relevance: create/poll/SSE-events/stop/approval for the runs API.
- [snippet_hermes_agent_gw_runner_session_key](../../code_snippets/snippet_hermes_agent_gw_runner_session_key.md) — session-key derivation; relevance: `X-Hermes-Session-Key` long-term-memory scoping.
- [snippet_hermes_agent_gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — session lifecycle; relevance: the sessions-over-REST table + fork/chat/stream persistence.
- [snippet_hermes_agent_gw_stream_consumer](../../code_snippets/snippet_hermes_agent_gw_stream_consumer.md) — SSE stream consumer; relevance: streaming responses + runs `/events` + `/chat/stream` event emission.
- [snippet_hermes_agent_gw_stream_backpressure](../../code_snippets/snippet_hermes_agent_gw_stream_backpressure.md) — stream backpressure; relevance: SSE flow control for long-running streamed turns.
- [snippet_hermes_agent_core_conversation_loop_api_dispatch](../../code_snippets/snippet_hermes_agent_core_conversation_loop_api_dispatch.md) — API→agent dispatch; relevance: each endpoint dispatches into the core agent turn (incl. `gateway_session_key`).
- [snippet_hermes_agent_gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — session state store; relevance: backs the sessions API + `previous_response_id`/named-conversation chains.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — health endpoints; relevance: `/health` + `/health/detailed` + capabilities reporting.

**Docs**
- [hermes_api_server_setup_auth](hermes_api_server_setup_auth.md) — setup/auth counterpart; relevance: same server, deployment half (+fin).
- [hermes_mcp_filtering_serving](hermes_mcp_filtering_serving.md) — `/v1/toolsets` source; relevance: the served toolsets are the MCP/runtime toolsets (+fin).
- [hermes_subscription_proxy](hermes_subscription_proxy.md) — contrasting server; relevance: agent-backend vs raw-model passthrough (+fin).
- [hermes_session_search_storage](hermes_session_search_storage.md) — session storage; relevance: sessions API reads/writes the session store (+fin).
- [hermes_sessions_lifecycle_resume](hermes_sessions_lifecycle_resume.md) — fork/resume semantics; relevance: `/api/sessions/{id}/fork` matches CLI `/branch` (+fin).
- [cc_headless_mode](../claude_code/cc_headless_mode.md) — programmatic agent surface; relevance: analogous "drive the agent over an API" model.
- [cc_sdk_session_management_api](../claude_code/cc_sdk_session_management_api.md) — session REST/API; relevance: analogous sessions-over-API surface.
- [cc_sdk_streaming_output](../claude_code/cc_sdk_streaming_output.md) — streaming output; relevance: analogous SSE token/tool-progress streaming.
- [cc_sdk_stream_text_and_tool_calls](../claude_code/cc_sdk_stream_text_and_tool_calls.md) — streamed tool calls; relevance: matches `function_call`/`function_call_output` stream items.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — hosting agent sessions; relevance: analogous to runs API for detached progress.

**Source**: `inbox/hermes_agent_docs/user-guide/features/api-server.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
**Last Updated**: 2026-06-19
**Status**: Active
