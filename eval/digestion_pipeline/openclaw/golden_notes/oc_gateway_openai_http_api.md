---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - http_api
keywords:
  - openclaw openai http api
  - v1 chat completions endpoint
  - agent-first model contract
  - openclaw agentId routing
  - x-openclaw-model override
  - gateway auth bearer token
  - full operator-access surface
  - sse streaming chat completions
  - chat tool contract function-tools
  - open webui openclaw setup
topics:
  - OpenClaw
  - Gateway OpenAI HTTP API
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/openai-http-api
access_control_group: ["general"]
---

# OpenClaw — OpenAI-Compatible Chat Completions HTTP API

## Overview

This note is the operational procedure for exposing OpenClaw's Gateway **OpenAI-compatible `/v1/chat/completions`** endpoint and the companion surfaces served with it, mirroring the `gateway/openai-http-api` source page: enabling/disabling the endpoint, the Gateway auth paths and **full operator-access** security boundary, the agent-first `model` contract (`openclaw/<agentId>` + `x-openclaw-*` headers), session behavior, SSE streaming, the function-tool subset, and Open WebUI setup. The endpoint is **disabled by default**; every request runs as a normal Gateway agent run (the same codepath as `openclaw agent`), so routing, permissions, and config match the Gateway.

## Endpoints Served

When enabled, the OpenAI-compatible HTTP surface serves `POST /v1/chat/completions` on the **same port as the Gateway** (WS + HTTP multiplex): `http://<gateway-host>:<port>/v1/chat/completions`. Enabling it also serves `GET /v1/models`, `GET /v1/models/{id}`, `POST /v1/embeddings`, and `POST /v1/responses` (documented separately as the OpenResponses endpoint). All run as a normal Gateway agent run.

## Enabling and Disabling the Endpoint

Set `gateway.http.endpoints.chatCompletions.enabled` to `true` to enable, or `false` to disable:

```json5
{
  gateway: {
    http: {
      endpoints: {
        chatCompletions: { enabled: true },
      },
    },
  },
}
```

The same `gateway.http.endpoints.chatCompletions.enabled` key set to `false` disables the endpoint.

## Authentication

The endpoint uses the Gateway auth configuration. The common HTTP auth paths are:

- **Shared-secret auth** (`gateway.auth.mode="token"` or `"password"`): `Authorization: Bearer <token-or-password>`. Use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`) for `token` mode, and `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`) for `password` mode.
- **Trusted identity-bearing HTTP auth** (`gateway.auth.mode="trusted-proxy"`): route through the configured identity-aware proxy, which injects the required identity headers. The request must come from a configured trusted proxy source; same-host loopback proxies require explicit `gateway.auth.trustedProxy.allowLoopback = true`. Same-host callers that bypass the proxy can use `gateway.auth.password` / `OPENCLAW_GATEWAY_PASSWORD` as a local direct fallback. Any `Forwarded`, `X-Forwarded-*`, or `X-Real-IP` header evidence keeps the request on the trusted-proxy path instead.
- **Private-ingress open auth** (`gateway.auth.mode="none"`): no auth header required.

If `gateway.auth.rateLimit` is configured and too many auth failures occur, the endpoint returns `429` with `Retry-After`.

## Security Boundary (Full Operator-Access)

Treat this endpoint as a **full operator-access** surface for the gateway instance. HTTP bearer auth here is not a narrow per-user scope model; a valid Gateway token/password should be treated like an owner/operator credential. Requests run through the same control-plane agent path as trusted operator actions, with no separate non-owner/per-user tool boundary — once a caller passes Gateway auth, OpenClaw treats it as a trusted operator for this gateway, and if the target agent policy allows sensitive tools the endpoint can use them. Keep this endpoint on loopback/tailnet/private ingress only; never expose it to the public internet.

For shared-secret auth modes (`token` and `password`), the endpoint **restores the normal full operator defaults even if the caller sends a narrower `x-openclaw-scopes` header**. Trusted identity-bearing HTTP modes honor `x-openclaw-scopes` when present and otherwise fall back to the normal operator default scope set. The auth matrix from source:

| Auth path | Identity proven | `x-openclaw-scopes` | Resulting scopes | Sender semantics |
|---|---|---|---|---|
| `mode="token"` / `"password"` + `Authorization: Bearer ...` | possession of the shared gateway operator secret | ignored | restores the full default operator scope set: `operator.admin`, `operator.approvals`, `operator.pairing`, `operator.read`, `operator.talk.secrets`, `operator.write` | chat turns treated as owner-sender turns |
| trusted identity-bearing HTTP modes (e.g. trusted proxy auth, or `mode="none"` on private ingress) | some outer trusted identity or deployment boundary | honored when present | falls back to the normal operator default scope set when absent | only loses owner semantics when the caller explicitly narrows scopes and omits `operator.admin`; requires `operator.admin` for owner-level controls such as `x-openclaw-model` |

## When to Use This Endpoint

Use `/v1/chat/completions` when integrating tooling or a trusted app-side backend with an existing gateway and you can safely hold gateway operator credentials. Prefer it over a new built-in channel when the integration is just another operator/client surface for the same gateway. For native mobile clients connecting directly to a remote gateway, prefer WebChat or the Gateway Protocol with the paired-device bootstrap/device-token flow so the device needs no shared HTTP token/password. Build a channel plugin instead when integrating an external messaging network with its own users, rooms, webhook delivery, or outbound transport.

## Agent-First Model Contract

OpenClaw treats the OpenAI `model` field as an **agent target**, not a raw provider model id. `model: "openclaw"` and `model: "openclaw/default"` both route to the configured default agent; `model: "openclaw/<agentId>"` routes to a specific agent. Compatibility aliases still accepted: `model: "openclaw:<agentId>"` and `model: "agent:<agentId>"`. Optional request headers shape routing and overrides:

- `x-openclaw-model: <provider/model-or-bare-id>` overrides the backend model for the selected agent. Shared-secret bearer callers can use this header. Identity-bearing callers (trusted-proxy or private no-auth ingress requests with `x-openclaw-scopes`) need `operator.admin`; write-only callers get `403 missing scope: operator.admin`.
- `x-openclaw-agent-id: <agentId>` remains supported as a compatibility override.
- `x-openclaw-session-key: <sessionKey>` explicitly controls session routing. The value must not use reserved internal session namespaces such as `subagent:`, `cron:`, or `acp:`; those requests are rejected with `400 invalid_request_error`.
- `x-openclaw-message-channel: <channel>` sets the synthetic ingress channel context for channel-aware prompts and policies.

## Model List and Agent Routing

`/v1/models` returns an **OpenClaw agent-target list**: the ids are `openclaw`, `openclaw/default`, and `openclaw/<agentId>` entries, used directly as OpenAI `model` values. It lists top-level agent targets — not backend provider models and not sub-agents (sub-agents stay internal execution topology, not pseudo-models). `openclaw/default` is the stable alias for the configured default agent, so clients keep one predictable id even if the real default agent id changes between environments. To override the backend model use `x-openclaw-model` (owner-level: works on the shared-secret bearer path, requires `operator.admin` on identity-bearing HTTP paths) — e.g. `x-openclaw-model: openai/gpt-5.4` or `x-openclaw-model: gpt-5.5`; if omitted, the agent runs with its normal configured model. `/v1/embeddings` uses the same agent-target `model` ids; send a specific embedding model in `x-openclaw-model` from a shared-secret caller or an `operator.admin` identity-bearing caller, otherwise the request uses the agent's normal embedding setup.

## Session Behavior

By default the endpoint is **stateless per request** (a new session key is generated each call). If the request includes an OpenAI `user` string, the Gateway derives a stable session key from it, so repeated calls can share an agent session. The safest default for custom apps is to reuse the same `user` value per conversation thread; avoid account-level identifiers unless you want multiple conversations/devices to share one OpenClaw session. Use `x-openclaw-session-key` only for explicit routing control across clients/threads, with application-owned keys that do not start with reserved internal namespaces (`subagent:`, `cron:`, `acp:`).

## Why This Surface Matters

This is the highest-leverage compatibility set for self-hosted frontends and tooling: Open WebUI, LobeChat, and LibreChat setups expect `/v1/models`; RAG systems expect `/v1/embeddings`; OpenAI chat clients start with `/v1/chat/completions`; agent-native clients increasingly prefer `/v1/responses`.

## Streaming (SSE)

Set `stream: true` to receive Server-Sent Events. The response uses `Content-Type: text/event-stream`, each event line is `data: <json>`, and the stream ends with `data: [DONE]`.

## Chat Tool Contract

`/v1/chat/completions` supports a function-tool subset compatible with common OpenAI Chat clients.

### Supported Request Fields

- `tools`: array of `{ "type": "function", "function": { ... } }`.
- `tool_choice`: `"auto"`, `"none"`, `"required"`, or `{ "type": "function", "function": { "name": "..." } }`.
- `messages[*].role: "tool"` follow-up turns; `messages[*].tool_call_id` for binding tool results back to a prior tool call.
- `max_completion_tokens`: number; per-call cap for total completion tokens (reasoning tokens included). Current OpenAI Chat Completions field name; preferred when both `max_completion_tokens` and `max_tokens` are sent.
- `max_tokens`: number; legacy alias accepted for backwards compatibility. Ignored when `max_completion_tokens` is also present.
- `temperature`, `top_p`: numbers; best-effort sampling / nucleus sampling forwarded to the upstream provider via the agent stream-param channel.
- `frequency_penalty`, `presence_penalty`: numbers; best-effort penalties forwarded via the agent stream-param channel. Validated range: -2.0 to 2.0. Returns `400 invalid_request_error` for out-of-range values.
- `seed`: number (integer); best-effort seed forwarded via the agent stream-param channel. Returns `400 invalid_request_error` for non-integer values.
- `stop`: string or array of up to 4 strings; best-effort stop sequences forwarded via the agent stream-param channel. Returns `400 invalid_request_error` for more than 4 sequences or non-string/empty entries.

All these fields ride the agent stream-param channel; the actual wire field name is chosen by the provider transport. Token caps map to `max_completion_tokens` for OpenAI-family endpoints and `max_tokens` for providers that only accept the legacy name (such as Mistral and Chutes). The ChatGPT-based Codex Responses backend strips sampling fields server-side since it uses fixed sampling. `stop` maps to `stop` for Chat Completions backends and `stop_sequences` for Anthropic; the OpenAI Responses API has no stop parameter, so `stop` is not applied on Responses-backed models.

### Unsupported Variants

The endpoint returns `400 invalid_request_error` for unsupported tool variants: non-array `tools`, non-function tool entries, missing `tool.function.name`, `tool_choice` variants such as `allowed_tools` and `custom`, and `tool_choice.function.name` values not matching provided `tools`. For `tool_choice: "required"` and function-pinned `tool_choice`, the endpoint narrows the exposed client function-tool set, instructs the runtime to call a client tool before responding, and errors if the agent response lacks a matching structured client-tool call. This contract applies to the caller-supplied HTTP `tools` list, not every internal OpenClaw agent tool.

### Non-Streaming and Streaming Tool Response Shapes

Non-streaming: the response uses `choices[0].finish_reason = "tool_calls"` and `choices[0].message.tool_calls[]` entries with `id`, `type: "function"`, `function.name`, and `function.arguments` (a JSON string); assistant commentary before the tool call is in `choices[0].message.content` (possibly empty). Streaming (`stream: true`): tool calls are emitted as incremental SSE chunks — an initial assistant role delta, optional commentary deltas, one or more `delta.tool_calls` chunks carrying tool identity and argument fragments, a final chunk with `finish_reason: "tool_calls"`, and `data: [DONE]`. If `stream_options.include_usage=true`, a trailing usage chunk precedes `[DONE]`.

### Tool Follow-Up Loop

After receiving `tool_calls`, the client executes the requested function(s) and sends a follow-up request including the prior assistant tool-call message plus one or more `role: "tool"` messages with matching `tool_call_id`. This lets the gateway agent run continue the same reasoning loop and produce the final answer.

## Open WebUI Quick Setup

For a basic Open WebUI connection, set the Base URL to `http://127.0.0.1:18789/v1` (Docker on macOS uses `http://host.docker.internal:18789/v1`), the API key to your Gateway bearer token, and the Model to `openclaw/default`. Expected: `GET /v1/models` lists `openclaw/default` and Open WebUI uses it as the chat model id; for a specific backend provider/model, set the agent's default model or send `x-openclaw-model` (shared-secret, or `operator.admin` identity-bearing caller). Quick smoke:

```bash
curl -sS http://127.0.0.1:18789/v1/models \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

If that returns `openclaw/default`, most Open WebUI setups can connect with the same base URL and token.

## Examples

Stable session for one app conversation (reuse the same `user` value on later calls for that conversation to continue the same agent session):

```bash
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "openclaw/default",
    "user": "conv:YOUR_CONVERSATION_ID",
    "messages": [{"role":"user","content":"Summarize my tasks for today"}]
  }'
```

Streaming, overriding the backend model with `x-openclaw-model`:

```bash
curl -N http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-model: openai/gpt-5.4' \
  -d '{
    "model": "openclaw/research",
    "stream": true,
    "messages": [{"role":"user","content":"hi"}]
  }'
```

Create embeddings (the `model` field carries the agent target; `x-openclaw-model` carries the backend embedding model):

```bash
curl -sS http://127.0.0.1:18789/v1/embeddings \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-model: openai/text-embedding-3-small' \
  -d '{
    "model": "openclaw/default",
    "input": ["alpha", "beta"]
  }'
```

A non-streaming chat call omits `stream`; `GET /v1/models/openclaw%2Fdefault` fetches one model (the `/` is URL-encoded). Source reiterates: `/v1/models` returns OpenClaw agent targets, not raw provider catalogs; `openclaw/default` is always present; backend overrides belong in `x-openclaw-model`, not the OpenAI `model` field; and `/v1/embeddings` accepts `input` as a string or array of strings.

**Source**: OpenClaw documentation — `gateway/openai-http-api` (mirror `inbox/openclaw_docs/gateway/openai-http-api.md`)
**Last Updated**: 2026-06-22
**Status**: Active
