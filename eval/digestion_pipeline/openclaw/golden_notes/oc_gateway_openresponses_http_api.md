---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - http_api
keywords:
  - openclaw openresponses api
  - v1 responses endpoint
  - item-based input
  - input_image input_file
  - response sse events
  - function_call_output tools
  - untrusted external content wrapping
  - usage normalization aliases
topics:
  - OpenClaw
  - Gateway OpenResponses HTTP API
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/openresponses-http-api
access_control_group: ["general"]
---

# OpenClaw — Gateway OpenResponses `/v1/responses` HTTP API

## Overview

This procedure note covers exposing the OpenClaw Gateway's OpenResponses-compatible `POST /v1/responses` HTTP endpoint, mirroring the `gateway/openresponses-http-api` source page. The endpoint is disabled by default and served on the same port as the Gateway (WS + HTTP multiplex) at `http://<gateway-host>:<port>/v1/responses`; under the hood each request is executed as a normal Gateway agent run (the same codepath as `openclaw agent`), so routing, permissions, and config match the Gateway instance. It documents the shared auth/security/routing contract (deferred where shared with `/v1/chat/completions`), stateless-per-request session behavior, the supported item-based `input` request shape, the `message` / `function_call_output` / `reasoning` / `item_reference` item types, client-side function tools, `input_image` and `input_file` handling (MIME allowlists, size limits, untrusted-content wrapping, PDF extraction), the `gateway.http.endpoints.responses` config limits, the `response.*` SSE event sequence, usage normalization, the error taxonomy, and worked `curl` examples.

## Authentication, security, and routing

Operational behavior matches OpenAI Chat Completions (`/v1/chat/completions`); the full auth/security/agent-target-model contract is shared with that sibling endpoint and deferred to it. Use the matching Gateway HTTP auth path:

- shared-secret auth (`gateway.auth.mode="token"` or `"password"`): `Authorization: Bearer <token-or-password>`.
- trusted-proxy auth (`gateway.auth.mode="trusted-proxy"`): identity-aware proxy headers from a configured trusted proxy source; same-host loopback proxies require explicit `gateway.auth.trustedProxy.allowLoopback = true`.
- trusted-proxy local direct fallback: same-host callers with no `Forwarded`, `X-Forwarded-*`, or `X-Real-IP` headers can use `gateway.auth.password` / `OPENCLAW_GATEWAY_PASSWORD`.
- private-ingress open auth (`gateway.auth.mode="none"`): no auth header.

The endpoint is treated as **full operator access** for the gateway instance. For shared-secret auth modes (`token` and `password`), narrower bearer-declared `x-openclaw-scopes` values are ignored and the normal full operator defaults are restored: `operator.admin`, `operator.approvals`, `operator.pairing`, `operator.read`, `operator.talk.secrets`, `operator.write` — and chat turns are treated as owner-sender turns. For trusted identity-bearing HTTP modes (for example trusted proxy auth or `gateway.auth.mode="none"`), `x-openclaw-scopes` is honored when present and otherwise falls back to the normal operator default scope set; owner semantics are lost only when the caller explicitly narrows scopes and omits `operator.admin`.

Agent and routing selection uses: `model: "openclaw"`, `model: "openclaw/default"`, `model: "openclaw/<agentId>"`, or `x-openclaw-agent-id` to select agents; `x-openclaw-model` to override the selected agent's backend model; `x-openclaw-session-key` for explicit session routing; and `x-openclaw-message-channel` for a non-default synthetic ingress channel context. Enable or disable this endpoint with `gateway.http.endpoints.responses.enabled`. The same compatibility surface also includes `GET /v1/models`, `GET /v1/models/{id}`, `POST /v1/embeddings`, and `POST /v1/chat/completions`; the canonical explanation of agent-target models, `openclaw/default`, embeddings pass-through, and backend model overrides lives on the OpenAI Chat Completions page.

## Session behavior

By default the endpoint is **stateless per request** — a new session key is generated on each call. If the request includes an OpenResponses `user` string, the Gateway derives a stable session key from it, so repeated calls can share an agent session.

## Request shape (supported)

The request follows the OpenResponses API with item-based input. Current support:

- `input`: string or array of item objects.
- `instructions`: merged into the system prompt.
- `tools`: client tool definitions (function tools).
- `tool_choice`: `"auto"`, `"none"`, `"required"`, or `{ "type": "function", "name": "..." }` to filter or require client tools.
- `stream`: enables SSE streaming.
- `max_output_tokens`: best-effort output limit (provider dependent).
- `temperature`: best-effort sampling temperature forwarded to the provider. Ignored by the ChatGPT-based Codex Responses backend, which uses fixed server-side sampling.
- `top_p`: best-effort nucleus sampling forwarded to the provider. Same Codex Responses caveat as `temperature`.
- `user`: stable session routing.

Accepted but **currently ignored**: `max_tool_calls`, `reasoning`, `metadata`, `store`, `truncation`. Supported: `previous_response_id` — OpenClaw reuses the earlier response session when the request stays within the same agent/user/requested-session scope.

## Items (input)

### `message`

Roles: `system`, `developer`, `user`, `assistant`. `system` and `developer` are appended to the system prompt. The most recent `user` or `function_call_output` item becomes the "current message." Earlier user/assistant messages are included as history for context.

### `function_call_output` (turn-based tools)

Send tool results back to the model with a `function_call_output` item:

```json
{
  "type": "function_call_output",
  "call_id": "call_123",
  "output": "{\"temperature\": \"72F\"}"
}
```

### `reasoning` and `item_reference`

Accepted for schema compatibility but ignored when building the prompt.

## Tools (client-side function tools)

Provide tools with `tools: [{ type: "function", name, description?, parameters? }]`. If the agent decides to call a tool, the response returns a `function_call` output item; you then send a follow-up request with `function_call_output` to continue the turn. For `tool_choice: "required"` and function-pinned `tool_choice`, the endpoint narrows the exposed client function-tool set, instructs the runtime to call a client tool before responding, and rejects the turn if it does not include a matching structured client-tool call. This contract applies to the caller-supplied HTTP `tools` list, not every internal OpenClaw agent tool. Non-streaming requests return `502` with an `api_error`; streaming requests emit a `response.failed` event. This matches the `/v1/chat/completions` contract.

## Images (`input_image`)

`input_image` supports base64 or URL sources:

```json
{
  "type": "input_image",
  "source": { "type": "url", "url": "https://example.com/image.png" }
}
```

Allowed MIME types (current): `image/jpeg`, `image/png`, `image/gif`, `image/webp`, `image/heic`, `image/heif`. Max size (current): 10MB. HEIC/HEIF `input_image` sources are accepted when a system converter is available and are normalized to JPEG before provider delivery; supported converters are macOS `sips`, ImageMagick, GraphicsMagick, or ffmpeg.

## Files (`input_file`)

`input_file` supports base64 or URL sources, e.g. a base64 `media_type: "text/plain"` part with `data` and `filename`. Allowed MIME types (current): `text/plain`, `text/markdown`, `text/html`, `text/csv`, `application/json`, `application/pdf`. Max size (current): 5MB. Current behavior:

- File content is decoded and added to the **system prompt**, not the user message, so it stays ephemeral (not persisted in session history).
- Decoded file text is wrapped as **untrusted external content** before it is added, so file bytes are treated as data, not trusted instructions.
- The injected block uses explicit boundary markers like `<<<EXTERNAL_UNTRUSTED_CONTENT id="...">>>` / `<<<END_EXTERNAL_UNTRUSTED_CONTENT id="...">>>` and includes a `Source: External` metadata line.
- This file-input path intentionally omits the long `SECURITY NOTICE:` banner to preserve prompt budget; the boundary markers and metadata still stay in place.
- PDFs are parsed for text first. If little text is found, the first pages are rasterized into images and passed to the model, and the injected file block uses the placeholder `[PDF content rendered to images]`.

PDF parsing is provided by the bundled `document-extract` plugin, which uses `clawpdf` and its packaged PDFium WebAssembly runtime for text extraction and page rendering.

URL fetch defaults: `files.allowUrl` is `true`, `images.allowUrl` is `true`, and `maxUrlParts` is `8` (total URL-based `input_file` + `input_image` parts per request). Requests are guarded (DNS resolution, private IP blocking, redirect caps, timeouts). Optional per-input-type hostname allowlists are supported (`files.urlAllowlist`, `images.urlAllowlist`): exact host `"cdn.example.com"`, wildcard subdomains `"*.assets.example.com"` (does not match apex); empty or omitted allowlists mean no hostname allowlist restriction. To disable URL-based fetches entirely, set `files.allowUrl: false` and/or `images.allowUrl: false`.

## File + image limits (config)

Defaults can be tuned under `gateway.http.endpoints.responses`:

```json5
{
  gateway: {
    http: {
      endpoints: {
        responses: {
          enabled: true,
          maxBodyBytes: 20000000,
          maxUrlParts: 8,
          files: {
            allowUrl: true,
            urlAllowlist: ["cdn.example.com", "*.assets.example.com"],
            allowedMimes: [
              "text/plain",
              "text/markdown",
              "text/html",
              "text/csv",
              "application/json",
              "application/pdf",
            ],
            maxBytes: 5242880,
            maxChars: 200000,
            maxRedirects: 3,
            timeoutMs: 10000,
            pdf: {
              maxPages: 4,
              maxPixels: 4000000,
              minTextChars: 200,
            },
          },
          images: {
            allowUrl: true,
            urlAllowlist: ["images.example.com"],
            allowedMimes: [
              "image/jpeg",
              "image/png",
              "image/gif",
              "image/webp",
              "image/heic",
              "image/heif",
            ],
            maxBytes: 10485760,
            maxRedirects: 3,
            timeoutMs: 10000,
          },
        },
      },
    },
  },
}
```

Defaults when omitted: `maxBodyBytes` 20MB; `maxUrlParts` 8; `files.maxBytes` 5MB; `files.maxChars` 200k; `files.maxRedirects` 3; `files.timeoutMs` 10s; `files.pdf.maxPages` 4; `files.pdf.maxPixels` 4,000,000; `files.pdf.minTextChars` 200; `images.maxBytes` 10MB; `images.maxRedirects` 3; `images.timeoutMs` 10s. Security note: URL allowlists are enforced before fetch and on redirect hops; allowlisting a hostname does not bypass private/internal IP blocking; for internet-exposed gateways, apply network egress controls in addition to app-level guards (see the Security page).

## Streaming (SSE)

Set `stream: true` to receive Server-Sent Events: `Content-Type: text/event-stream`, each event line is `event: <type>` and `data: <json>`, and the stream ends with `data: [DONE]`. Event types currently emitted, in sequence: `response.created`, `response.in_progress`, `response.output_item.added`, `response.content_part.added`, `response.output_text.delta`, `response.output_text.done`, `response.content_part.done`, `response.output_item.done`, `response.completed`, and `response.failed` (on error).

## Usage

`usage` is populated when the underlying provider reports token counts. OpenClaw normalizes common OpenAI-style aliases before those counters reach downstream status/session surfaces, including `input_tokens` / `output_tokens` and `prompt_tokens` / `completion_tokens`.

## Errors

Errors use a JSON object like `{ "error": { "message": "...", "type": "invalid_request_error" } }`. Common cases: `401` missing/invalid auth; `400` invalid request body; `405` wrong method (a `502` `api_error` is also returned for non-streaming `tool_choice` enforcement failures, per the Tools section).

## Examples

Non-streaming request against a local Gateway on port `18789`:

```bash
curl -sS http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "input": "hi"
  }'
```

Streaming request (note the `-N` flag and `"stream": true`):

```bash
curl -N http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-agent-id: main' \
  -d '{
    "model": "openclaw",
    "stream": true,
    "input": "hi"
  }'
```

**Source**: OpenClaw documentation — `gateway/openresponses-http-api` (mirror `inbox/openclaw_docs/gateway/openresponses-http-api.md`)
**Last Updated**: 2026-06-22
**Status**: Active
