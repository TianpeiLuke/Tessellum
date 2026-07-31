---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - webhooks
keywords:
  - openclaw webhooks plugin
  - taskflow ingress webhook
  - plugins.entries.webhooks.config routes
  - shared-secret webhook authentication
  - secretref webhook secret
  - create_flow run_task action
  - managedflows.bindsession
  - bearer x-openclaw-webhook-secret header
topics:
  - OpenClaw
  - Webhooks Plugin
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/webhooks
access_control_group: ["general"]
---

# OpenClaw — Configuring the Webhooks Plugin (Authenticated TaskFlow Ingress)

## Overview

This note is the operator procedure for the bundled OpenClaw **Webhooks plugin**, which adds authenticated HTTP routes that bind external automation to OpenClaw TaskFlows. Use it when a trusted system — Zapier, n8n, a CI job, or an internal service — needs to create and drive managed TaskFlows without first writing a custom plugin. It mirrors the `plugins/webhooks` source page end to end: where the plugin runs, how to configure routes under `plugins.entries.webhooks.config`, the per-route security model, the request format and authentication headers, the supported JSON `action` set (with `create_flow` and `run_task` worked examples), and the response shape.

## Where it runs

The Webhooks plugin runs inside the **Gateway process**. If your Gateway runs on another machine, install and configure the plugin on that Gateway host, then **restart the Gateway** so the new routes are served.

## Configure routes

Set config under `plugins.entries.webhooks.config`. Each entry under `routes` defines one authenticated HTTP route; the example below defines a single `zapier` route bound to the `agent:main:main` session, authenticated by an `env`-sourced SecretRef:

```json5
{
  plugins: {
    entries: {
      webhooks: {
        enabled: true,
        config: {
          routes: {
            zapier: {
              path: "/plugins/webhooks/zapier",
              sessionKey: "agent:main:main",
              secret: {
                source: "env",
                provider: "default",
                id: "OPENCLAW_WEBHOOK_SECRET",
              },
              controllerId: "webhooks/zapier",
              description: "Zapier TaskFlow bridge",
            },
          },
        },
      },
    },
  },
}
```

Each route accepts these fields (verbatim from source):

- `enabled` — optional, defaults to `true`.
- `path` — optional, defaults to `/plugins/webhooks/<routeId>`.
- `sessionKey` — **required**; the session that owns the bound TaskFlows.
- `secret` — **required**; the shared secret or SecretRef.
- `controllerId` — optional controller id for created managed flows.
- `description` — optional operator note.

Supported `secret` inputs are a **plain string** or a **SecretRef with `source: "env" | "file" | "exec"`**. If a secret-backed route cannot resolve its secret at startup, the plugin **skips that route and logs a warning** instead of exposing a broken endpoint.

## Security model

Each route is trusted to act with the **TaskFlow authority of its configured `sessionKey`** — the route can inspect and mutate TaskFlows owned by that session. Because of that authority, the source prescribes these operator practices:

- Use a strong, unique secret per route.
- Prefer secret references over inline plaintext secrets.
- Bind routes to the narrowest session that fits the workflow.
- Expose only the specific webhook path you need.

Independently of operator configuration, the plugin itself applies the following protections to every route: **shared-secret authentication**; **request body size and timeout guards**; **fixed-window rate limiting**; **in-flight request limiting**; and **owner-bound TaskFlow access** through `api.runtime.tasks.managedFlows.bindSession(...)`.

## Request format

Send `POST` requests with `Content-Type: application/json` and authenticate with **either** an `Authorization: Bearer <secret>` header **or** an `x-openclaw-webhook-secret: <secret>` header. The JSON body carries the `action` and its parameters. Worked `curl` example:

```bash
curl -X POST https://gateway.example.com/plugins/webhooks/zapier \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_SHARED_SECRET' \
  -d '{"action":"create_flow","goal":"Review inbound queue"}'
```

## Supported actions

The plugin currently accepts these JSON `action` values: `create_flow`, `get_flow`, `list_flows`, `find_latest_flow`, `resolve_flow`, `get_task_summary`, `set_waiting`, `resume_flow`, `finish_flow`, `fail_flow`, `request_cancel`, `cancel_flow`, and `run_task`. The source documents two of these in detail.

### `create_flow`

Creates a managed TaskFlow for the route's bound session. Example body:

```json
{
  "action": "create_flow",
  "goal": "Review inbound queue",
  "status": "queued",
  "notifyPolicy": "done_only"
}
```

### `run_task`

Creates a managed child task inside an existing managed TaskFlow. The allowed runtimes are `subagent` and `acp`. Example body:

```json
{
  "action": "run_task",
  "flowId": "flow_123",
  "runtime": "acp",
  "childSessionKey": "agent:main:acp:worker",
  "task": "Inspect the next message batch"
}
```

## Response shape

Successful responses return `ok: true` with the `routeId` and a `result` object:

```json
{
  "ok": true,
  "routeId": "zapier",
  "result": {}
}
```

Rejected requests return `ok: false` with the `routeId`, a `code`, an `error` message, and a `result` object:

```json
{
  "ok": false,
  "routeId": "zapier",
  "code": "not_found",
  "error": "TaskFlow not found.",
  "result": {}
}
```

The plugin intentionally **scrubs owner/session metadata** from webhook responses.

**Source**: OpenClaw documentation — `plugins/webhooks` (mirror `inbox/openclaw_docs/plugins/webhooks.md`)
**Last Updated**: 2026-06-22
**Status**: Active
