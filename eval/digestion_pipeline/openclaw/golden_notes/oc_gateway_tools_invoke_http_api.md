---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - tools_invoke
keywords:
  - openclaw tools invoke
  - post /tools/invoke
  - gateway http tool endpoint
  - shared-secret bearer operator access
  - tool policy hard deny list
  - x-openclaw-scopes
  - gateway.tools allow deny
  - exec spawn shell rce deny
topics:
  - OpenClaw
  - Gateway Tools Invoke HTTP API
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/tools-invoke-http-api
access_control_group: ["general"]
---

# OpenClaw — Gateway `POST /tools/invoke` HTTP Endpoint

## Overview

This note is the operator procedure for OpenClaw's Gateway `POST /tools/invoke` HTTP endpoint: the always-enabled surface for invoking a single tool directly without running a full agent turn. It mirrors the `gateway/tools-invoke-http-api` source page, covering the three auth paths (shared-secret bearer / trusted-proxy / none), the full-operator-access security boundary, the request-body schema, the tool-policy filter chain, the default hard deny list, the `gateway.tools` allow/deny overrides, and the HTTP response codes. The endpoint is served on the same port as the Gateway via a WS + HTTP multiplex (`http://<gateway-host>:<port>/tools/invoke`), and its default maximum payload size is 2 MB. Like the OpenAI-compatible `/v1/*` surface, shared-secret bearer auth here is treated as trusted operator access for the whole gateway.

## Authentication

The endpoint uses the Gateway auth configuration. The three common HTTP auth paths are:

- **shared-secret auth** (`gateway.auth.mode="token"` or `"password"`) — send `Authorization: Bearer <token-or-password>`. When mode is `"token"`, use `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`); when mode is `"password"`, use `gateway.auth.password` (or `OPENCLAW_GATEWAY_PASSWORD`).
- **trusted identity-bearing HTTP auth** (`gateway.auth.mode="trusted-proxy"`) — route the request through the configured identity-aware proxy and let it inject the required identity headers. The HTTP request must come from a configured trusted proxy source; same-host loopback proxies require explicitly setting `gateway.auth.trustedProxy.allowLoopback = true`.
- **private-ingress open auth** (`gateway.auth.mode="none"`) — no auth header is required.

Internal same-host callers that bypass the proxy can use `gateway.auth.password` / `OPENCLAW_GATEWAY_PASSWORD` as a local direct fallback. Any `Forwarded`, `X-Forwarded-*`, or `X-Real-IP` header evidence keeps the request on the trusted-proxy path instead. If `gateway.auth.rateLimit` is configured and too many auth failures occur, the endpoint returns `429` with `Retry-After`.

## Security Boundary (important)

Treat this endpoint as a **full operator-access** surface for the gateway instance. HTTP bearer auth here is not a narrow per-user scope model, and a valid Gateway token/password for this endpoint should be treated like an owner/operator credential. The page is explicit that keeping the endpoint reachable on loopback/tailnet/private ingress only — and never exposing it directly to the public internet — is part of the boundary. The behavior differs by auth mode:

- For shared-secret auth modes (`token` and `password`), the endpoint restores the normal full operator defaults even if the caller sends a narrower `x-openclaw-scopes` header, and it treats direct tool invokes on this endpoint as owner-sender turns.
- Trusted identity-bearing HTTP modes (for example trusted-proxy auth, or `gateway.auth.mode="none"` on a private ingress) honor `x-openclaw-scopes` when present and otherwise fall back to the normal operator default scope set.

The auth matrix from the source page makes the two branches precise:

- `gateway.auth.mode="token"` or `"password"` + `Authorization: Bearer ...` — proves possession of the shared gateway operator secret, ignores narrower `x-openclaw-scopes`, restores the full default operator scope set (`operator.admin`, `operator.approvals`, `operator.pairing`, `operator.read`, `operator.talk.secrets`, `operator.write`), and treats direct tool invokes on this endpoint as owner-sender turns.
- trusted identity-bearing HTTP modes (for example trusted-proxy auth, or `gateway.auth.mode="none"` on private ingress) — authenticate some outer trusted identity or deployment boundary, honor `x-openclaw-scopes` when the header is present, fall back to the normal operator default scope set when the header is absent, and only lose owner semantics when the caller explicitly narrows scopes and omits `operator.admin`.

## Request Body

The request body is a JSON object:

```json
{
  "tool": "sessions_list",
  "action": "json",
  "args": {},
  "sessionKey": "main",
  "dryRun": false
}
```

Fields:

- `tool` (string, **required**) — tool name to invoke.
- `action` (string, optional) — mapped into args if the tool schema supports `action` and the args payload omitted it.
- `args` (object, optional) — tool-specific arguments.
- `sessionKey` (string, optional) — target session key. If omitted or `"main"`, the Gateway uses the configured main session key (honors `session.mainKey` and default agent, or `global` in global scope).
- `dryRun` (boolean, optional) — reserved for future use; currently ignored.

To help group policies resolve context, you can optionally set `x-openclaw-message-channel: <channel>` (example: `slack`, `telegram`) and `x-openclaw-account-id: <accountId>` (when multiple accounts exist).

## Policy + Routing Behavior (hard deny list)

Tool availability is filtered through the same policy chain used by Gateway agents, evaluated in this order: `tools.profile` / `tools.byProvider.profile`; then `tools.allow` / `tools.byProvider.allow`; then `agents.<id>.tools.allow` / `agents.<id>.tools.byProvider.allow`; then group policies (if the session key maps to a group or channel); then subagent policy (when invoking with a subagent session key). If a tool is not allowed by policy, the endpoint returns **404**.

Important boundary notes from the source: exec approvals are operator guardrails, not a separate authorization boundary for this HTTP endpoint — if a tool is reachable here via Gateway auth + tool policy, `/tools/invoke` does not add an extra per-call approval prompt. If `exec` is reachable here, treat it as a mutating shell surface; denying `write`, `edit`, `apply_patch`, or HTTP filesystem-write tools does not make shell execution read-only. Do not share Gateway bearer credentials with untrusted callers — if you need separation across trust boundaries, run separate gateways (and ideally separate OS users/hosts).

Gateway HTTP also applies a **hard deny list by default** (even if session policy allows the tool):

- `exec` — direct command execution (RCE surface)
- `spawn` — arbitrary child process creation (RCE surface)
- `shell` — shell command execution (RCE surface)
- `fs_write` — arbitrary file mutation on the host
- `fs_delete` — arbitrary file deletion on the host
- `fs_move` — arbitrary file move/rename on the host
- `apply_patch` — patch application can rewrite arbitrary files
- `sessions_spawn` — session orchestration; spawning agents remotely is RCE
- `sessions_send` — cross-session message injection
- `cron` — persistent automation control plane
- `gateway` — gateway control plane; prevents reconfiguration via HTTP
- `nodes` — node command relay can reach system.run on paired hosts
- `whatsapp_login` — interactive setup requiring terminal QR scan; hangs on HTTP

You can customize this deny list via `gateway.tools`:

```json5
{
  gateway: {
    tools: {
      // Additional tools to block over HTTP /tools/invoke
      deny: ["browser"],
      // Remove tools from the default deny list for owner/admin callers
      allow: ["gateway"],
    },
  },
}
```

`gateway.tools.allow` is an exposure override, not a scope upgrade. In identity-bearing HTTP modes, `cron`, `gateway`, and `nodes` remain unavailable to callers that do not have owner/admin identity (`operator.admin`) even when they are listed in `gateway.tools.allow`. Shared-secret bearer auth still follows the full trusted-operator rule above.

## Responses

The endpoint returns these HTTP status codes:

- `200` → `{ ok: true, result }`
- `400` → `{ ok: false, error: { type, message } }` (invalid request or tool input error)
- `401` → unauthorized
- `429` → auth rate-limited (`Retry-After` set)
- `404` → tool not available (not found or not allowlisted)
- `405` → method not allowed
- `500` → `{ ok: false, error: { type, message } }` (unexpected tool execution error; sanitized message)

## Example

A minimal shared-secret invocation of the `sessions_list` tool:

```bash
curl -sS http://127.0.0.1:18789/tools/invoke \
  -H 'Authorization: Bearer secret' \
  -H 'Content-Type: application/json' \
  -d '{
    "tool": "sessions_list",
    "action": "json",
    "args": {}
  }'
```

**Source**: OpenClaw documentation — `gateway/tools-invoke-http-api` (mirror `inbox/openclaw_docs/gateway/tools-invoke-http-api.md`)
**Last Updated**: 2026-06-22
**Status**: Active
