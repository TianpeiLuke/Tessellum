---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - protocol
keywords:
  - openclaw gateway event families
  - task ledger rpcs tasks.list
  - operator helper methods
  - tools.catalog tools.effective tools.invoke
  - models.list views configured all
  - exec.approval.request exec.approval.resolve
  - agent delivery fallback bestEffortDeliver
  - node helper skills.bins
topics:
  - OpenClaw
  - Gateway Protocol
language: markdown
date of note: 2026-06-23
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/protocol
access_control_group: ["general"]
---

# OpenClaw — Gateway Protocol Event Families & Helper RPCs

## Overview

This note models the **event families and helper-RPC tail** of the OpenClaw Gateway WebSocket protocol — the server→client event families, the node-helper / task-ledger / operator-helper RPCs, the `models.list` view parameter, exec approvals, and agent delivery fallback. It is split from the RPC method-family catalog in the sibling [oc_gateway_protocol_rpc_methods](oc_gateway_protocol_rpc_methods.md) (both halves mirror the `gateway/protocol` page). Transport/framing is in `oc_gateway_protocol_transport`, role/scope in `oc_gateway_protocol_roles_scopes`, auth/pairing in `oc_gateway_protocol_auth_pairing`.

## Common Event Families

- `chat` — UI chat updates (e.g. `chat.inject`). In protocol v4, delta payloads carry `deltaText`; `message` is the cumulative assistant snapshot; non-prefix replacements set `replace=true` with `deltaText` as the replacement text.
- `session.message`, `session.operation`, and `session.tool` — transcript, in-flight session operation, and event-stream updates for a subscribed session; `sessions.changed` — session index/metadata changed.
- `presence`, `tick` (keepalive/liveness), `health`, `heartbeat`, `cron`, and `shutdown` — presence, liveness, health, heartbeat, cron change, and shutdown notifications.
- `node.pair.requested` / `node.pair.resolved` (node pairing), `node.invoke.request` (invoke broadcast), `device.pair.requested` / `device.pair.resolved` (paired-device), `voicewake.changed`, `exec.approval.requested` / `exec.approval.resolved`, and `plugin.approval.requested` / `plugin.approval.resolved`.

## Node Helper Methods

- Nodes may call `skills.bins` to fetch the current list of skill executables for auto-allow checks.

## Task Ledger RPCs

Operator clients inspect and cancel Gateway background task records through these RPCs, which return **sanitized task summaries**, not raw runtime state:

- `tasks.list` (`operator.read`) — params: optional `status` (`"queued"`, `"running"`, `"completed"`, `"failed"`, `"cancelled"`, `"timed_out"`) or array, optional `agentId`, `sessionKey`, `limit` (`1`–`500`), `cursor`. Result: `{ "tasks": TaskSummary[], "nextCursor"?: string }`.
- `tasks.get` (`operator.read`) — params `{ "taskId": string }`; result `{ "task": TaskSummary }` (missing ids return the not-found shape).
- `tasks.cancel` (`operator.write`) — params `{ "taskId": string, "reason"?: string }`; result `{ "found": boolean, "cancelled": boolean, "reason"?: string, "task"?: TaskSummary }` (`found` = ledger match; `cancelled` = runtime accepted/recorded).

`TaskSummary` includes `id`, `status`, and optional metadata such as `kind`, `runtime`, `title`, `agentId`, `sessionKey`, `childSessionKey`, `ownerKey`, `runId`, `taskId`, `flowId`, `parentTaskId`, `sourceId`, timestamps, progress, terminal summary, and sanitized error text. `agentId` is the executing agent; `sessionKey`/`ownerKey` preserve requester/control context.

## Operator Helper Methods

- `commands.list` (`operator.read`) fetches the runtime command inventory (`agentId` optional). `scope` selects the primary `name` surface (`text` = token without `/`; `native`/default `both` = provider-aware names); `textAliases` carries slash aliases (`/model`, `/m`); `nativeName` the native name; `includeArgs=false` omits argument metadata.
- `tools.catalog` (`operator.read`) fetches the runtime tool catalog — grouped tools plus provenance: `source` (`core` or `plugin`), `pluginId` (when `source="plugin"`), `optional`.
- `tools.effective` (`operator.read`) fetches the runtime-effective tool inventory for a session (`sessionKey` required; runtime context derived server-side) — a projection of core, plugin, channel, and already-discovered MCP tools. It is **read-only for MCP**: it may project a warm session MCP catalog through final tool policy but does not create MCP runtimes, connect transports, or issue `tools/list`; absent a warm catalog the response may include `mcp-not-yet-connected`, `mcp-not-yet-listed`, or `mcp-stale-catalog`. Entries use `source="core"`, `"plugin"`, `"channel"`, or `"mcp"`.
- `tools.invoke` (`operator.write`) invokes one tool through the same gateway policy path as `/tools/invoke`. `name` required; `args`, `sessionKey`, `agentId`, `confirm`, `idempotencyKey` optional; if both `sessionKey` and `agentId` are present the resolved session agent must match `agentId`. Owner-only core wrappers (`cron`, `gateway`, `nodes`) require `operator.admin`. The response is an SDK envelope (`ok`, `toolName`, optional `output`, typed `error`); approval/policy refusals return `ok:false` rather than bypass the policy pipeline.
- `skills.status` (`operator.read`) fetches the visible skill inventory (eligibility, missing requirements, config checks, sanitized install options); `skills.search` / `skills.detail` (`operator.read`) give ClawHub discovery metadata.
- `skills.upload.begin`, `skills.upload.chunk`, `skills.upload.commit` (`operator.admin`) stage a private skill archive (admin path, disabled unless `skills.install.allowUploadedArchives`); commit only finalizes, archives are zips with a `SKILL.md` root, and the internal directory name never selects the target.
- `skills.install` (`operator.admin`) has three modes: ClawHub (`{ source: "clawhub", slug, version?, force? }`), Upload (`{ source: "upload", uploadId, slug, force?, sha256?, timeoutMs? }`, gated by `skills.install.allowUploadedArchives`), and Gateway installer (`{ name, installId, timeoutMs? }`, running a `metadata.openclaw.install` action). The deprecated `dangerouslyForceUnsafeInstall` is accepted but ignored — use `security.installPolicy`. `skills.update` (`operator.admin`) runs ClawHub mode (one/all tracked slugs) or Config mode (patches `skills.entries.<skillKey>` values such as `enabled`, `apiKey`, `env`).

## `models.list` Views

`models.list` accepts an optional `view` parameter:

- Omitted / `"default"`: if `agents.defaults.models` is configured, the allowed catalog (with dynamically discovered models for `provider/*` entries); otherwise the full Gateway catalog.
- `"configured"`: picker-sized — `agents.defaults.models` still wins (provider-scoped discovery for `provider/*`); without an allowlist it uses explicit `models.providers.*.models` entries, falling back to the full catalog only when no configured rows exist.
- `"all"`: full Gateway catalog, bypassing `agents.defaults.models`; for diagnostics/discovery UIs, not normal pickers.

## Exec Approvals

- When an exec request needs approval the gateway broadcasts `exec.approval.requested`; operators resolve via `exec.approval.resolve` (requires `operator.approvals` scope).
- For `host=node`, `exec.approval.request` must include `systemRunPlan` (canonical `argv`/`cwd`/`rawCommand`/session metadata; missing → rejected); forwarded `node.invoke system.run` calls reuse that canonical `systemRunPlan` as the authoritative command/cwd/session context.
- If a caller mutates `command`, `rawCommand`, `cwd`, `agentId`, or `sessionKey` between prepare and the final approved `system.run` forward, the gateway rejects the run rather than trust the mutated payload.

## Agent Delivery Fallback

- `agent` requests can include `deliver=true` for outbound delivery. `bestEffortDeliver=false` is strict: unresolved/internal-only targets return `INVALID_REQUEST`; `bestEffortDeliver=true` falls back to session-only execution when no external route resolves (e.g. internal/webchat sessions or ambiguous multi-channel configs).
- Final `agent` results may include `result.deliveryStatus` when delivery was requested, using the same `sent`, `suppressed`, `partial_failed`, and `failed` statuses documented for the `openclaw agent --json --deliver` CLI path.

**Source**: OpenClaw documentation — `gateway/protocol` (event-families + helper-RPC cluster; mirror `inbox/openclaw_docs/gateway/protocol.md`)
**Last Updated**: 2026-06-23
**Status**: Active
