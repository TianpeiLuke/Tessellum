---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - admin_http_rpc
keywords:
  - openclaw admin http rpc plugin
  - admin-http-rpc enable
  - POST /api/v1/admin/rpc
  - gateway control-plane rpc over http
  - gateway http auth bearer token
  - allowed gateway methods allowlist
  - gatewayMethodDispatch authenticated-request
  - x-openclaw-scopes
  - websocket rpc vs http rpc
topics:
  - OpenClaw
  - Plugins
  - Gateway Admin HTTP RPC
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/admin-http-rpc
access_control_group: ["general"]
---

# OpenClaw — Admin HTTP RPC Plugin

## Overview

This note is the procedure for enabling and operating OpenClaw's bundled, opt-in `admin-http-rpc` plugin, which exposes selected Gateway control-plane methods over an HTTP request/response surface for trusted host automation that cannot use the normal Gateway WebSocket RPC client. It mirrors the `plugins/admin-http-rpc` source page end to end: the pre-enable trust checklist, enabling/disabling the bundled plugin, verifying the route, the authentication paths, the security model, the request/response shape, the allowed-method allowlist, the WebSocket comparison, and HTTP-status troubleshooting. The plugin is included with OpenClaw but is off by default; when disabled the route is not registered. When enabled it adds `POST /api/v1/admin/rpc` on the same listener as the Gateway: `http://<gateway-host>:<port>/api/v1/admin/rpc`. Enable it only for private host tooling, tailnet automation, or a trusted internal ingress — do not expose this route directly to the public internet.

## Before You Enable It

Admin HTTP RPC is a full operator control-plane surface: any caller that passes Gateway HTTP auth can invoke the allowlisted methods. Enable it only when ALL of these are true: the caller is trusted to operate the Gateway; the caller cannot use the WebSocket RPC client; the route is reachable only on loopback, a tailnet, or a private authenticated ingress; and you have reviewed the allowed methods and they match the automation you plan to run. Use the WebSocket RPC path for OpenClaw clients and interactive tools that can keep a Gateway WebSocket connection open.

## Enable

The plugin is bundled, so enabling it is a single command (or config) plus a Gateway restart — the route is registered during plugin startup, so you must restart the Gateway after changing plugin config. Enable via the CLI, then disable it the same way when you no longer need the HTTP surface (disabling re-removes the route):

```bash
openclaw plugins enable admin-http-rpc
openclaw gateway restart

openclaw plugins disable admin-http-rpc
openclaw gateway restart
```

Or enable via config, setting `plugins.entries."admin-http-rpc".enabled` to `true` (a json5 block: `{ plugins: { entries: { "admin-http-rpc": { enabled: true } } } }`).

## Verify the Route

Use `health` as the smallest safe request to confirm the route is live:

```bash
curl -sS http://<gateway-host>:<port>/api/v1/admin/rpc \
  -H 'Authorization: Bearer <gateway-token>' \
  -H 'Content-Type: application/json' \
  -d '{"method":"health","params":{}}'
```

A successful response has `ok: true` (for `health`, `payload.status` is `"ok"`):

```json
{
  "id": "generated-request-id",
  "ok": true,
  "payload": {
    "status": "ok"
  }
}
```

When the plugin is disabled, the route returns `404` because it is not registered.

## Authentication

The plugin route uses Gateway HTTP auth — there is no separate plugin-specific auth. The common authentication paths are: shared-secret auth (`gateway.auth.mode="token"` or `"password"`) via the `Authorization: Bearer <token-or-password>` header; trusted identity-bearing HTTP auth (`gateway.auth.mode="trusted-proxy"`) where you route through the configured identity-aware proxy and let it inject the required identity headers; and private-ingress open auth (`gateway.auth.mode="none"`) where no auth header is required.

## Security Model

Treat this plugin as a full Gateway operator surface. The source page states the security posture explicitly:

- Enabling the plugin intentionally offers access to the allowlisted admin RPC methods at `/api/v1/admin/rpc`.
- The plugin declares the reserved `contracts.gatewayMethodDispatch: ["authenticated-request"]` manifest contract so its Gateway-authenticated HTTP route can dispatch control-plane methods in process.
- Shared-secret bearer auth proves possession of the gateway operator secret.
- For `token` and `password` auth, narrower `x-openclaw-scopes` headers are ignored and the normal full operator defaults are restored.
- Trusted identity-bearing HTTP modes honor `x-openclaw-scopes` when present.
- `gateway.auth.mode="none"` means this route is unauthenticated if the plugin is enabled. Use that only behind a private ingress you fully trust.
- Requests dispatch through the same Gateway method handlers and scope checks as WebSocket RPC after the plugin route auth passes.
- Keep this route on loopback, tailnet, or a private trusted ingress. Do not expose it directly to the public internet.
- Plugin manifest contracts are not a sandbox. They prevent accidental use of reserved SDK helpers; trusted plugins still run in the Gateway process.

Use separate gateways when callers cross trust boundaries.

## Request

A request is an HTTP `POST /api/v1/admin/rpc` with headers `Authorization: Bearer <gateway-token>` and `Content-Type: application/json`, and a JSON body carrying the Gateway RPC method and params:

```json
{
  "id": "optional-request-id",
  "method": "health",
  "params": {}
}
```

The body fields are: `id` (string, optional) — copied into the response, and a UUID is generated when omitted; `method` (string, required) — an allowed Gateway method name; `params` (any, optional) — method-specific params. The default max request body size is 1 MB.

## Response

Success responses use the Gateway RPC shape (`ok: true` with a method-specific `payload`):

```json
{
  "id": "optional-request-id",
  "ok": true,
  "payload": {}
}
```

Gateway method errors return `ok: false` with an `error` object carrying a `code` and `message`:

```json
{
  "id": "optional-request-id",
  "ok": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "bad params"
  }
}
```

HTTP status follows the Gateway error when possible — for example, `INVALID_REQUEST` returns `400`, and `UNAVAILABLE` returns `503`.

## Allowed Methods

The plugin enforces a method allowlist; other Gateway methods are blocked until they are intentionally added. The discovery method `commands.list` returns the HTTP RPC method names allowed by this plugin. The full allowlist, grouped as in the source:

- **discovery**: `commands.list` (returns the HTTP RPC method names allowed by this plugin)
- **gateway**: `health`, `status`, `logs.tail`, `usage.status`, `usage.cost`, `gateway.restart.request`
- **config**: `config.get`, `config.schema`, `config.schema.lookup`, `config.set`, `config.patch`, `config.apply`
- **channels**: `channels.status`, `channels.start`, `channels.stop`, `channels.logout`
- **web**: `web.login.start`, `web.login.wait`
- **models**: `models.list`, `models.authStatus`
- **agents**: `agents.list`, `agents.create`, `agents.update`, `agents.delete`
- **approvals**: `exec.approvals.get`, `exec.approvals.set`, `exec.approvals.node.get`, `exec.approvals.node.set`
- **cron**: `cron.status`, `cron.list`, `cron.get`, `cron.runs`, `cron.add`, `cron.update`, `cron.remove`, `cron.run`
- **devices**: `device.pair.list`, `device.pair.approve`, `device.pair.reject`, `device.pair.remove`
- **nodes**: `node.list`, `node.describe`, `node.pair.list`, `node.pair.approve`, `node.pair.reject`, `node.pair.remove`, `node.rename`
- **tasks**: `tasks.list`, `tasks.get`, `tasks.cancel`
- **diagnostics**: `doctor.memory.status`, `update.status`

## WebSocket Comparison

The normal Gateway WebSocket RPC path remains the preferred control-plane API for OpenClaw clients; use admin HTTP RPC only for host tooling that needs a request/response HTTP surface. The reason the HTTP path exists as a distinct operator surface: shared-token WebSocket clients without a trusted device identity cannot self-declare admin scopes during connect, so admin HTTP RPC deliberately follows the existing trusted HTTP operator model — when the plugin is enabled, shared-secret bearer auth is treated as full operator access for this admin surface.

## Troubleshooting

The HTTP status code identifies the failure mode:

- **`404 Not Found`** — the plugin is disabled, the Gateway has not restarted since enabling it, or the request is going to a different Gateway process.
- **`401 Unauthorized`** — the request did not satisfy Gateway HTTP auth; check the bearer token or the trusted-proxy identity headers.
- **`400 INVALID_REQUEST`** — the request body is not valid JSON, the `method` field is missing, or the method is not in the plugin allowlist.
- **`503 UNAVAILABLE`** — the Gateway method handler is unavailable; check Gateway logs and retry after the Gateway finishes startup.

**Source**: OpenClaw documentation — `plugins/admin-http-rpc` (mirror `inbox/openclaw_docs/plugins/admin-http-rpc.md`)
**Last Updated**: 2026-06-22
**Status**: Active
