---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - opentelemetry
keywords:
  - openclaw exported metrics
  - openclaw exported spans
  - diagnostic event catalog
  - openclaw.model.usage span
  - openclaw.tokens counter
  - session liveness telemetry
  - gen_ai semantic conventions
  - openclaw.model.failover
  - bounded redacted attributes
topics:
  - OpenClaw
  - OpenTelemetry Signals Catalog
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/opentelemetry
access_control_group: ["general"]
---

# OpenClaw — OpenTelemetry Signals Catalog (Metrics, Spans, Events)

## Overview

This note models the exact telemetry that OpenClaw's `diagnostics-otel` plugin exports over OTLP/HTTP: every metric (name, instrument type, attribute list), every span (name + attribute set), and the underlying diagnostic event catalog that backs them. It mirrors the **Exported metrics**, **Exported spans**, and **Diagnostic event catalog** sections of the `gateway/opentelemetry` source page — the reference data shapes operators need to build dashboards and alerts. How to enable, configure, sample, and privacy-control the export is a separate procedure note ([oc_gateway_opentelemetry_setup](oc_gateway_opentelemetry_setup.md)); this note documents only the signal shapes themselves. Throughout, spans carry only bounded identifiers and never raw prompt/response/tool content unless content capture is explicitly opted in.

## Exported Metrics

Metrics are OpenTelemetry counters and histograms. Each is listed below with its instrument type and attribute keys, copied verbatim from the source catalog. They are grouped into the families the source page defines: model usage, message flow, Talk, queues and sessions, session liveness, harness lifecycle, tool execution, exec, and diagnostics internals.

### Model usage

- `openclaw.tokens` — counter; attrs: `openclaw.token`, `openclaw.channel`, `openclaw.provider`, `openclaw.model`, `openclaw.agent`.
- `openclaw.cost.usd` — counter; attrs: `openclaw.channel`, `openclaw.provider`, `openclaw.model`.
- `openclaw.run.duration_ms` — histogram; attrs: `openclaw.channel`, `openclaw.provider`, `openclaw.model`.
- `openclaw.context.tokens` — histogram; attrs: `openclaw.context`, `openclaw.channel`, `openclaw.provider`, `openclaw.model`.
- `gen_ai.client.token.usage` — histogram, GenAI semantic-conventions metric; attrs: `gen_ai.token.type` = `input`/`output`, `gen_ai.provider.name`, `gen_ai.operation.name`, `gen_ai.request.model`.
- `gen_ai.client.operation.duration` — histogram (seconds), GenAI semantic-conventions metric; attrs: `gen_ai.provider.name`, `gen_ai.operation.name`, `gen_ai.request.model`, optional `error.type`.
- `openclaw.model_call.duration_ms` — histogram; attrs: `openclaw.provider`, `openclaw.model`, `openclaw.api`, `openclaw.transport`, plus `openclaw.errorCategory` and `openclaw.failureKind` on classified errors.
- `openclaw.model_call.request_bytes` — histogram; UTF-8 byte size of the final model request payload (no raw payload content).
- `openclaw.model_call.response_bytes` — histogram; UTF-8 byte size of streamed response chunk payloads — high-frequency text, thinking, and tool-call deltas count only incremental `delta` bytes (no raw response content).
- `openclaw.model_call.time_to_first_byte_ms` — histogram; elapsed time before the first streamed response event.
- `openclaw.model.failover` — counter; attrs: `openclaw.provider`, `openclaw.model`, `openclaw.failover.to_provider`, `openclaw.failover.to_model`, `openclaw.failover.reason`, `openclaw.failover.suspended`, `openclaw.lane`.
- `openclaw.skill.used` — counter; attrs: `openclaw.skill.name`, `openclaw.skill.source`, `openclaw.skill.activation`, optional `openclaw.agent`, optional `openclaw.toolName`.

### Message flow

- `openclaw.webhook.received` — counter; attrs: `openclaw.channel`, `openclaw.webhook`.
- `openclaw.webhook.error` — counter; attrs: `openclaw.channel`, `openclaw.webhook`.
- `openclaw.webhook.duration_ms` — histogram; attrs: `openclaw.channel`, `openclaw.webhook`.
- `openclaw.message.queued` — counter; attrs: `openclaw.channel`, `openclaw.source`.
- `openclaw.message.received` — counter; attrs: `openclaw.channel`, `openclaw.source`.
- `openclaw.message.dispatch.started` — counter; attrs: `openclaw.channel`, `openclaw.source`.
- `openclaw.message.dispatch.completed` — counter; attrs: `openclaw.channel`, `openclaw.outcome`, `openclaw.reason`, `openclaw.source`.
- `openclaw.message.dispatch.duration_ms` — histogram; attrs: `openclaw.channel`, `openclaw.outcome`, `openclaw.reason`, `openclaw.source`.
- `openclaw.message.processed` — counter; attrs: `openclaw.channel`, `openclaw.outcome`.
- `openclaw.message.duration_ms` — histogram; attrs: `openclaw.channel`, `openclaw.outcome`.
- `openclaw.message.delivery.started` — counter; attrs: `openclaw.channel`, `openclaw.delivery.kind`.
- `openclaw.message.delivery.duration_ms` — histogram; attrs: `openclaw.channel`, `openclaw.delivery.kind`, `openclaw.outcome`, `openclaw.errorCategory`.

### Talk

Talk metrics export only bounded event metadata (mode, transport, provider, event type) and never include transcripts, audio payloads, or session/turn/call/room ids or handoff tokens.

- `openclaw.talk.event` — counter; attrs: `openclaw.talk.event_type`, `openclaw.talk.mode`, `openclaw.talk.transport`, `openclaw.talk.brain`, `openclaw.talk.provider`.
- `openclaw.talk.event.duration_ms` — histogram; attrs: same as `openclaw.talk.event`; emitted when a Talk event reports duration.
- `openclaw.talk.audio.bytes` — histogram; attrs: same as `openclaw.talk.event`; emitted for Talk audio frame events that report byte length.

### Queues and sessions

- `openclaw.queue.lane.enqueue` — counter; attrs: `openclaw.lane`.
- `openclaw.queue.lane.dequeue` — counter; attrs: `openclaw.lane`.
- `openclaw.queue.depth` — histogram; attrs: `openclaw.lane` or `openclaw.channel=heartbeat`.
- `openclaw.queue.wait_ms` — histogram; attrs: `openclaw.lane`.
- `openclaw.session.state` — counter; attrs: `openclaw.state`, `openclaw.reason`.
- `openclaw.session.stuck` — counter; attrs: `openclaw.state`; emitted for recoverable stale session bookkeeping.
- `openclaw.session.stuck_age_ms` — histogram; attrs: `openclaw.state`; emitted for recoverable stale session bookkeeping.
- `openclaw.session.turn.created` — counter; attrs: `openclaw.agent`, `openclaw.channel`, `openclaw.trigger`.
- `openclaw.session.recovery.requested` — counter; attrs: `openclaw.state`, `openclaw.action`, `openclaw.active_work_kind`, `openclaw.reason`.
- `openclaw.session.recovery.completed` — counter; attrs: `openclaw.state`, `openclaw.action`, `openclaw.status`, `openclaw.active_work_kind`, `openclaw.reason`.
- `openclaw.session.recovery.age_ms` — histogram; attrs: same as the matching recovery counter.
- `openclaw.run.attempt` — counter; attrs: `openclaw.attempt`.

### Session liveness state model

`diagnostics.stuckSessionWarnMs` is the no-progress age threshold for session liveness diagnostics. A `processing` session does not age toward this threshold while OpenClaw observes reply, tool, status, block, or ACP runtime progress; typing keepalives are not counted as progress, so a silent model or harness can still be detected. OpenClaw classifies sessions by the work it can still observe:

- `session.long_running`: active embedded work, model calls, or tool calls are still making progress. Owned model calls that stay silent past `diagnostics.stuckSessionWarnMs` also report as long-running before `diagnostics.stuckSessionAbortMs`, so slow or non-streaming model providers do not look like stalled gateway sessions while they remain abort-observable.
- `session.stalled`: active work exists, but the active run has not reported recent progress. Owned model calls switch from `session.long_running` to `session.stalled` at or after `diagnostics.stuckSessionAbortMs`; ownerless stale model/tool activity is not treated as harmless long-running work. Stalled embedded runs stay observe-only at first, then abort-drain after `diagnostics.stuckSessionAbortMs` with no progress so queued turns behind the lane can resume. When unset, the abort threshold defaults to the safer extended window of at least 5 minutes and 3x `diagnostics.stuckSessionWarnMs`.
- `session.stuck`: stale session bookkeeping with no active work, or an idle queued session with stale ownerless model/tool activity. This releases the affected session lane immediately after recovery gates pass.

Recovery emits structured `session.recovery.requested` and `session.recovery.completed` events; diagnostic session state is marked idle only after a mutating recovery outcome (`aborted` or `released`) and only if the same processing generation is still current. Only `session.stuck` emits the `openclaw.session.stuck` counter, the `openclaw.session.stuck_age_ms` histogram, and the `openclaw.session.stuck` span. Repeated `session.stuck` diagnostics back off while the session remains unchanged, so dashboards should alert on sustained increases rather than every heartbeat tick.

Liveness warnings also emit:

- `openclaw.liveness.warning` — counter; attrs: `openclaw.liveness.reason`.
- `openclaw.liveness.event_loop_delay_p99_ms` — histogram; attrs: `openclaw.liveness.reason`.
- `openclaw.liveness.event_loop_delay_max_ms` — histogram; attrs: `openclaw.liveness.reason`.
- `openclaw.liveness.event_loop_utilization` — histogram; attrs: `openclaw.liveness.reason`.
- `openclaw.liveness.cpu_core_ratio` — histogram; attrs: `openclaw.liveness.reason`.

### Harness lifecycle

- `openclaw.harness.duration_ms` — histogram; attrs: `openclaw.harness.id`, `openclaw.harness.plugin`, `openclaw.outcome`, `openclaw.harness.phase` on errors.

### Tool execution

- `openclaw.tool.execution.duration_ms` — histogram; attrs: `gen_ai.tool.name`, `openclaw.toolName`, `openclaw.tool.source`, `openclaw.tool.owner`, `openclaw.tool.params.kind`, plus `openclaw.errorCategory` on errors.
- `openclaw.tool.execution.blocked` — counter; attrs: `gen_ai.tool.name`, `openclaw.toolName`, `openclaw.tool.source`, `openclaw.tool.owner`, `openclaw.tool.params.kind`, `openclaw.deniedReason`.

### Exec

- `openclaw.exec.duration_ms` — histogram; attrs: `openclaw.exec.target`, `openclaw.exec.mode`, `openclaw.outcome`, `openclaw.failureKind`.

### Diagnostics internals (memory and tool loop)

- `openclaw.payload.large` — counter; attrs: `openclaw.payload.surface`, `openclaw.payload.action`, `openclaw.channel`, `openclaw.plugin`, `openclaw.reason`.
- `openclaw.payload.large_bytes` — histogram; attrs: same as `openclaw.payload.large`.
- `openclaw.memory.heap_used_bytes` — histogram; attrs: `openclaw.memory.kind`.
- `openclaw.memory.rss_bytes` — histogram.
- `openclaw.memory.pressure` — counter; attrs: `openclaw.memory.level`.
- `openclaw.tool.loop.iterations` — counter; attrs: `openclaw.toolName`, `openclaw.outcome`.
- `openclaw.tool.loop.duration_ms` — histogram; attrs: `openclaw.toolName`, `openclaw.outcome`.

## Exported Spans

Spans cover model usage, model calls, harness lifecycle, skill usage, tool execution, exec, webhook/message processing, context assembly, and tool loops. Each span below is listed with its name and bounded attribute set, verbatim from source.

- `openclaw.model.usage` — `openclaw.channel`, `openclaw.provider`, `openclaw.model`; `openclaw.tokens.*` (input/output/cache_read/cache_write/total); `gen_ai.system` by default, or `gen_ai.provider.name` when the latest GenAI semantic conventions are opted in; `gen_ai.request.model`, `gen_ai.operation.name`, `gen_ai.usage.*`.
- `openclaw.run` — `openclaw.outcome`, `openclaw.channel`, `openclaw.provider`, `openclaw.model`, `openclaw.errorCategory`.
- `openclaw.model.call` — `gen_ai.system` by default, or `gen_ai.provider.name` when the latest GenAI semantic conventions are opted in; `gen_ai.request.model`, `gen_ai.operation.name`, `openclaw.provider`, `openclaw.model`, `openclaw.api`, `openclaw.transport`; `openclaw.errorCategory` and optional `openclaw.failureKind` on errors; `openclaw.model_call.request_bytes`, `openclaw.model_call.response_bytes`, `openclaw.model_call.time_to_first_byte_ms`; `openclaw.provider.request_id_hash` (bounded SHA-based hash of the upstream provider request id — raw ids are not exported). With `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`, model-call spans use the latest GenAI inference span name `{gen_ai.operation.name} {gen_ai.request.model}` and `CLIENT` span kind instead of `openclaw.model.call`.
- `openclaw.harness.run` — `openclaw.harness.id`, `openclaw.harness.plugin`, `openclaw.outcome`, `openclaw.provider`, `openclaw.model`, `openclaw.channel`; on completion: `openclaw.harness.result_classification`, `openclaw.harness.yield_detected`, `openclaw.harness.items.started`, `openclaw.harness.items.completed`, `openclaw.harness.items.active`; on error: `openclaw.harness.phase`, `openclaw.errorCategory`, optional `openclaw.harness.cleanup_failed`.
- `openclaw.tool.execution` — `gen_ai.tool.name`, `openclaw.toolName`, `openclaw.errorCategory`, `openclaw.tool.params.*`.
- `openclaw.exec` — `openclaw.exec.target`, `openclaw.exec.mode`, `openclaw.outcome`, `openclaw.failureKind`, `openclaw.exec.command_length`, `openclaw.exec.exit_code`, `openclaw.exec.timed_out`.
- `openclaw.webhook.processed` — `openclaw.channel`, `openclaw.webhook`.
- `openclaw.webhook.error` — `openclaw.channel`, `openclaw.webhook`, `openclaw.error`.
- `openclaw.message.processed` — `openclaw.channel`, `openclaw.outcome`, `openclaw.reason`.
- `openclaw.message.delivery` — `openclaw.channel`, `openclaw.delivery.kind`, `openclaw.outcome`, `openclaw.errorCategory`, `openclaw.delivery.result_count`.
- `openclaw.session.stuck` — `openclaw.state`, `openclaw.ageMs`, `openclaw.queueDepth`.
- `openclaw.context.assembled` — `openclaw.prompt.size`, `openclaw.history.size`, `openclaw.context.tokens`, `openclaw.errorCategory` (no prompt, history, response, or session-key content).
- `openclaw.tool.loop` — `openclaw.toolName`, `openclaw.outcome`, `openclaw.iterations`, `openclaw.errorCategory` (no loop messages, params, or tool output).
- `openclaw.memory.pressure` — `openclaw.memory.level`, `openclaw.memory.heap_used_bytes`, `openclaw.memory.rss_bytes`.

When content capture is explicitly enabled, model and tool spans can also include bounded, redacted `openclaw.content.*` attributes for the specific content classes you opted into.

## Diagnostic Event Catalog

The events below are the structured in-process diagnostic records that back the metrics and spans above; plugins can also subscribe to them directly without OTLP export.

**Model usage**

- `model.usage` — tokens, cost, duration, context, provider/model/channel, session ids. `usage` is provider/turn accounting for cost and telemetry; `context.used` is the current prompt/context snapshot and can be lower than provider `usage.total` when cached input or tool-loop calls are involved.

**Message flow**

- `webhook.received` / `webhook.processed` / `webhook.error`
- `message.queued` / `message.processed`
- `message.delivery.started` / `message.delivery.completed` / `message.delivery.error`

**Queue and session**

- `queue.lane.enqueue` / `queue.lane.dequeue`
- `session.state` / `session.long_running` / `session.stalled` / `session.stuck`
- `run.attempt` / `run.progress`
- `diagnostic.heartbeat` — aggregate counters (webhooks/queue/session).

**Harness lifecycle**

- `harness.run.started` / `harness.run.completed` / `harness.run.error` — per-run lifecycle for the agent harness. Includes `harnessId`, optional `pluginId`, provider/model/channel, and run id. Completion adds `durationMs`, `outcome`, optional `resultClassification`, `yieldDetected`, and `itemLifecycle` counts. Errors add `phase` (`prepare`/`start`/`send`/`resolve`/`cleanup`), `errorCategory`, and optional `cleanupFailed`.

**Exec**

- `exec.process.completed` — terminal outcome, duration, target, mode, exit code, and failure kind. Command text and working directories are not included.

**Source**: OpenClaw documentation — `gateway/opentelemetry` (mirror `inbox/openclaw_docs/gateway/opentelemetry.md`), Exported metrics / Exported spans / Diagnostic event catalog sections
**Last Updated**: 2026-06-22
**Status**: Active
