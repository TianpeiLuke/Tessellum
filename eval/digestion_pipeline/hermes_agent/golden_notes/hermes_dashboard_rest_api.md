---
tags:
  - resource
  - documentation
  - hermes_agent
  - rest_api
  - web_dashboard
keywords:
  - hermes dashboard REST API
  - profile-scoped endpoints
  - admin endpoints
  - localhost CORS
  - Vite dev proxy
  - automatic build on update
topics:
  - Hermes Agent
  - Web Dashboard
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard
access_control_group: ["general"]
---

# Hermes Dashboard REST API

## Overview

The dashboard REST API is the HTTP surface the `hermes dashboard` web frontend (a React SPA) consumes — and the same surface you can call directly for automation. It is **not** a feature procedure; it is a *model* of the FastAPI server's endpoint contract: a set of read/write endpoint families (`/api/config`, `/api/env`, `/api/sessions`, `/api/skills`, `/api/cron`, `/api/logs`, `/api/analytics`, …), a larger admin-endpoints table behind the auth gate (MCP, messaging, pairing, webhooks, credentials, memory, gateway, ops, system, hermes-update, curator, portal), and two WebSockets (`/api/pty`, `/api/ws`) that the Chat tab and Hermes Desktop use. The management families accept an optional `?profile=<name>` query parameter that scopes the read/write to a profile's `HERMES_HOME`; CORS is locked to localhost origins; a Vite dev proxy fronts the SPA during development; and the frontend rebuilds automatically on `hermes update`. The endpoints sit behind the same auth gate documented in the gated-mode and remote-backend procedures.

## Profile-scoped endpoints

The management endpoint families — `/api/config`, `/api/env`, `/api/skills`, `/api/tools/toolsets`, `/api/mcp`, and `/api/model/{info,options,auxiliary,set}` — accept an optional `?profile=<name>` query parameter (or `"profile"` in the JSON body for writes) that scopes the read/write to that profile's `HERMES_HOME`. Omitting it targets the dashboard's own profile. Unknown profile names return `404`. The `/api/pty` WebSocket accepts the same parameter to spawn a chat under the selected profile.

## Read/write endpoint families

The frontend SPA consumes these endpoints; they are also directly callable for automation. Each maps to one of the dashboard's pages.

| Method & path | Purpose |
|---------------|---------|
| `GET /api/status` | Agent version, gateway status, platform states, active session count (public endpoint) |
| `GET /api/sessions` | The 20 most recent sessions with metadata (model, token counts, timestamps, preview) |
| `GET /api/sessions/{session_id}` | Metadata for a single session |
| `GET /api/sessions/{session_id}/messages` | Full message history for a session, including tool calls and timestamps |
| `GET /api/sessions/search` | Full-text search across message content (query param `q`); returns session IDs + highlighted snippets |
| `DELETE /api/sessions/{session_id}` | Delete a session and its message history |
| `GET /api/config` | Current `config.yaml` contents as JSON |
| `GET /api/config/defaults` | Default configuration values |
| `GET /api/config/schema` | Schema for every config field — type, description, category, select options (drives the input widgets) |
| `PUT /api/config` | Save a new configuration. Body: `{"config": {...}}` |
| `GET /api/env` | All known env vars with set/unset status, redacted values, descriptions, categories |
| `PUT /api/env` | Set an env var. Body: `{"key": "VAR_NAME", "value": "secret"}` |
| `DELETE /api/env` | Remove an env var. Body: `{"key": "VAR_NAME"}` |
| `GET /api/logs` | Log lines. Query params: `file` (agent/errors/gateway), `lines`, `level`, `component` |
| `GET /api/analytics/usage` | Token usage, cost, session analytics. Query param `days` (default 30); daily breakdowns + per-model aggregates |
| `GET /api/cron/jobs` | All cron jobs with state, schedule, run history |
| `POST /api/cron/jobs` | Create a cron job. Body: `{"prompt", "schedule", "name", "deliver"}` |
| `POST /api/cron/jobs/{job_id}/{pause,resume,trigger}` | Pause, resume, or immediately trigger a job |
| `DELETE /api/cron/jobs/{job_id}` | Delete a cron job |
| `GET /api/skills` | All skills with name, description, category, enabled status |
| `PUT /api/skills/toggle` | Enable/disable a skill. Body: `{"name", "enabled"}` |
| `GET /api/tools/toolsets` | All toolsets with label, description, tools list, active/configured status |

A representative write — saving the config edited by the Config page — illustrates the body shape:

```
PUT /api/config
{"config": {"model": {"name": "..."}, "approvals": {"mode": "ask"}, ...}}
```

## Admin endpoints

These power the MCP, Channels, Webhooks, Pairing, and System pages. **All sit behind the same auth gate as the rest of `/api/`** (see the gated-mode auth note).

| Method & path | Purpose |
|---------------|---------|
| `GET /api/mcp/servers` | List configured MCP servers (env values redacted) |
| `POST /api/mcp/servers` | Add a server. Body: `{name, url?, command?, args?, env?, auth?}` |
| `POST /api/mcp/servers/{name}/test` | Connect, list tools, disconnect |
| `PUT /api/mcp/servers/{name}/enabled` | Enable / disable a server |
| `DELETE /api/mcp/servers/{name}` | Remove a server |
| `GET /api/mcp/catalog` · `POST /api/mcp/catalog/install` | Browse the Nous-approved catalog · install an entry (with required env) |
| `GET /api/messaging/platforms` | List every channel with status + per-platform setup fields |
| `PUT /api/messaging/platforms/{id}` | Configure a channel. Body: `{enabled?, env?, clear_env?}` (env → `.env`, enabled → `config.yaml`) |
| `POST /api/messaging/platforms/{id}/test` | Report whether a channel is configured, enabled, connected |
| `GET /api/pairing` · `POST /api/pairing/{approve,revoke,clear-pending}` | List pending+approved users · approve/revoke/clear |
| `GET /api/webhooks` · `POST /api/webhooks` · `DELETE /api/webhooks/{name}` · `PUT /api/webhooks/{name}/enabled` | List · create (returns one-time secret) · remove · enable/disable a subscription |
| `GET /api/credentials/pool` · `POST /api/credentials/pool` · `DELETE /api/credentials/pool/{provider}/{index}` | List redacted rotation keys · add a key · remove a key (1-based index) |
| `GET /api/memory` · `PUT /api/memory/provider` · `POST /api/memory/reset` | Active+available providers + file sizes · select provider · reset built-in (`{target: all\|memory\|user}`) |
| `POST /api/gateway/{start,stop,restart}` | Gateway lifecycle (backgrounded) |
| `POST /api/ops/{doctor,security-audit,backup,import,prompt-size,dump,config-migrate}` | Diagnostics & maintenance (backgrounded; tail via `/api/actions/{name}/status`) |
| `GET /api/ops/hooks` · `POST /api/ops/hooks` · `DELETE /api/ops/hooks` | List shell hooks + allowlist status · create / remove a hook (consent-gated) |
| `GET /api/ops/checkpoints` · `POST /api/ops/checkpoints/prune` | Inspect / prune the `/rollback` store |
| `GET /api/system/stats` | Host stats — OS, CPU, memory, disk, uptime |
| `GET /api/hermes/update/check` | Update availability (commits behind, install method) without applying; behind installs also return a `commits` list (`sha`, `summary`, `author`, `at`); `?force=1` busts the 6h cache |
| `GET /api/curator` · `PUT /api/curator/paused` · `POST /api/curator/run` | Skill-curator status · pause/resume · run |
| `GET /api/portal` | Nous Portal auth + Tool Gateway routing (read-only) |
| `POST /api/skills/hub/{install,uninstall,update}` · `GET /api/skills/hub/search` | Skills-hub actions (backgrounded) · search the hub across all sources |
| `GET /api/sessions/stats` · `PATCH /api/sessions/{id}` · `GET /api/sessions/{id}/export` · `POST /api/sessions/prune` | Session-store stats · rename/archive · export JSON · prune ended sessions older than N days |
| `PUT /api/cron/jobs/{id}` | Edit a cron job's prompt / schedule / name / deliver |

## CORS

The web server restricts CORS to localhost origins only:

- `http://localhost:9119` / `http://127.0.0.1:9119` (production)
- `http://localhost:3000` / `http://127.0.0.1:3000`
- `http://localhost:5173` / `http://127.0.0.1:5173` (Vite dev server)

If you run the server on a custom port, that origin is added automatically.

## Development

If you're contributing to the web dashboard frontend:

```bash
# Terminal 1: start the backend API
hermes dashboard --no-open

# Terminal 2: start the Vite dev server with HMR
cd web/
npm install
npm run dev
```

The Vite dev server at `http://localhost:5173` proxies `/api` requests to the FastAPI backend at `http://127.0.0.1:9119`. The frontend is built with React 19, TypeScript, Tailwind CSS v4, and shadcn/ui-style components. Production builds output to `hermes_cli/web_dist/`, which the FastAPI server serves as a static SPA.

## Automatic Build on Update

When you run `hermes update`, the web frontend is automatically rebuilt if `npm` is available, keeping the dashboard in sync with code updates. If `npm` isn't installed, the update skips the frontend build and `hermes dashboard` will build it on first launch.

**Source**: `inbox/hermes_agent_docs/user-guide/features/web-dashboard.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard
**Last Updated**: 2026-06-19
**Status**: Active
