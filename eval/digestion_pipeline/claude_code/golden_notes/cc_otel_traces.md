---
tags:
  - resource
  - documentation
  - claude_code
  - monitoring
  - tracing
keywords:
  - claude code traces
  - distributed tracing beta
  - claude_code.interaction span
  - span hierarchy
  - traceparent propagation
  - w3c trace context
  - otel_traces_exporter
  - enhanced telemetry beta
  - span attributes
topics:
  - Claude Code
  - Monitoring
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/monitoring-usage
access_control_group: ["general"]
---

# Claude Code — Distributed Tracing (Beta)

## Overview

Claude Code can optionally export **distributed traces** (beta) in addition to its metrics and logs/events signals. Distributed tracing exports **spans** that link each user prompt to the API requests and tool executions it triggers, so an operator can view a full request as a single trace in their tracing backend. Tracing is **off by default**; it is enabled by setting both `CLAUDE_CODE_ENABLE_TELEMETRY=1` and `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, then choosing where spans are sent with `OTEL_TRACES_EXPORTER`. Traces reuse the common OTLP configuration (endpoint, protocol, headers, mTLS) used by the metrics and logs exporters.

This note covers the trace enable flags, the `claude_code.interaction` span tree, W3C `traceparent`/`TRACEPARENT`/`TRACESTATE` context propagation both into and out of Claude Code, and the additional attributes set on each span. The shared OTLP knobs (endpoint/protocol/headers/cardinality) are documented in [cc_otel_configuration_variables](cc_otel_configuration_variables.md), and the privacy implications of the content-gating flags in the [Security and privacy](https://code.claude.com/docs/en/monitoring-usage) section of the monitoring-usage docs.

## Enabling traces

Tracing requires two enable flags plus an exporter choice. Spans reuse the [common OTLP configuration](cc_otel_configuration_variables.md) for endpoint, protocol, headers, and mTLS; the trace-specific variables override the general OTLP settings.

| Environment Variable | Description | Example Values |
|---|---|---|
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | Enable span tracing (required). `ENABLE_ENHANCED_TELEMETRY_BETA` is also accepted | `1` |
| `OTEL_TRACES_EXPORTER` | Traces exporter types, comma-separated. Use `none` to disable | `console`, `otlp`, `none` |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL` | Protocol for traces, overrides `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | OTLP traces endpoint, overrides `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4318/v1/traces` |
| `OTEL_TRACES_EXPORT_INTERVAL` | Span batch export interval in milliseconds (default: 5000) | `1000`, `10000` |

Spans **redact** user prompt text, tool input details, and tool content by default. Set `OTEL_LOG_USER_PROMPTS=1`, `OTEL_LOG_TOOL_DETAILS=1`, and `OTEL_LOG_TOOL_CONTENT=1` to include them (`OTEL_LOG_TOOL_CONTENT` requires tracing and truncates content at 60 KB).

## Context propagation

When tracing is active, Bash and PowerShell subprocesses automatically inherit a `TRACEPARENT` environment variable containing the W3C trace context of the active tool execution span. Any subprocess that reads `TRACEPARENT` can parent its own spans under the same trace, enabling end-to-end distributed tracing through scripts and commands that Claude runs.

When tracing is active and Claude Code is connected directly to the Anthropic API, each model request carries a W3C `traceparent` header set to the `claude_code.llm_request` span's context, and the API's `traceresponse` header is recorded as a span link. Together these connect Claude Code's client-side spans to the server-side trace through any compliant intermediary. Outbound HTTP MCP requests carry `traceparent` the same way. The header is not sent to third-party providers.

By default, the `traceparent` header on model and HTTP MCP requests is sent only when `ANTHROPIC_BASE_URL` is unset or points at the Anthropic API, since some proxies reject unrecognized headers. The subprocess `TRACEPARENT` variable is controlled by the same switch for consistency. To propagate trace context through a custom `ANTHROPIC_BASE_URL` proxy, set `CLAUDE_CODE_PROPAGATE_TRACEPARENT=1`.

In Agent SDK and non-interactive sessions started with `-p`, Claude Code also **reads** `TRACEPARENT` and `TRACESTATE` from its own environment when starting each interaction span. This lets an embedding process pass its active W3C trace context into the subprocess so Claude Code's spans appear as children of the caller's distributed trace. Interactive sessions ignore inbound `TRACEPARENT` to avoid accidentally inheriting ambient values from CI or container environments.

## Span hierarchy

Each user prompt starts a `claude_code.interaction` root span. API calls, tool calls, and hook executions are recorded as its children. Tool spans have two child spans of their own: one for the time spent waiting on a permission decision and one for the execution itself. When the Agent tool, or legacy Task tool, spawns a subagent, the subagent's API and tool spans nest under the parent's `claude_code.tool` span.

```text
claude_code.interaction
├── claude_code.llm_request
├── claude_code.hook                    (requires detailed beta tracing)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user
    ├── claude_code.tool.execution
    └── (Agent tool) subagent claude_code.llm_request / claude_code.tool spans
```

In Agent SDK and `claude -p` sessions, `claude_code.interaction` itself becomes a child of the caller's span when `TRACEPARENT` is set in the environment.

## Span attributes

Every span carries the [standard attributes](cc_otel_metrics_reference.md) plus a `span.type` attribute matching its name. The tables below list the *additional* attributes set on each span. The `llm_request`, `tool.execution`, and `hook` spans set OpenTelemetry status `ERROR` when they record a failure; the other spans always end with status `UNSET`.

### `claude_code.interaction`

| Attribute | Description | Gated by |
|---|---|---|
| `user_prompt` | Prompt text. Value is `<REDACTED>` unless the gate is set | `OTEL_LOG_USER_PROMPTS` |
| `user_prompt_length` | Prompt length in characters | |
| `interaction.sequence` | 1-based counter of interactions in this session | |
| `interaction.duration_ms` | Wall-clock duration of the turn | |

### `claude_code.llm_request`

Key attributes (selected): `model` and the OpenTelemetry GenAI conventions `gen_ai.system` (always `anthropic`), `gen_ai.request.model` (= `model`), `gen_ai.response.id` (= `request_id`), and `gen_ai.response.finish_reasons` (= `stop_reason` wrapped in a string array). `query_source` names the subsystem that issued the request (such as `repl_main_thread` or a subagent name); `agent_id` / `parent_agent_id` identify the subagent or teammate (absent on the main session). `speed` is `fast` or `normal`; `llm_request.context` is `interaction`, `tool`, or `standalone` depending on the parent span. Timing/usage: `duration_ms` (includes retries), `ttft_ms` (time to first token), `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`. Identity/outcome: `request_id` (from the `request-id` response header), `client_request_id` (`x-client-request-id` of the final attempt), `attempt` (total attempts), `success` (`true`/`false`), `status_code` and `error` (when the request failed), `response.has_tool_call`, and `stop_reason` (such as `end_turn`, `tool_use`, `max_tokens`, `stop_sequence`, `pause_turn`, or `refusal`). Each retry attempt is also recorded as a `gen_ai.request.attempt` span event with `attempt` and `client_request_id` attributes.

### `claude_code.tool`

| Attribute | Description | Gated by |
|---|---|---|
| `tool_name` | Tool name | |
| `duration_ms` | Wall-clock duration including permission wait and execution | |
| `result_tokens` | Approximate token size of the tool result | |
| `agent_id` | Subagent or teammate that ran the tool. Absent on the main session | |
| `parent_agent_id` | Agent that spawned this one. Absent for the main session and for agents spawned directly from it | |
| `tool_use_id` | The model's `tool_use` block id; matches `tool_use_id` on the [tool_result](cc_otel_events_reference.md) / [tool_decision](cc_otel_events_reference.md) events and in hook payloads, so you can join the span to those records | |
| `gen_ai.tool.call.id` | Same value as `tool_use_id`. OpenTelemetry GenAI convention | |
| `file_path` | Target file path for Read, Edit, and Write tools | `OTEL_LOG_TOOL_DETAILS` |
| `full_command` | Command string for the Bash tool | `OTEL_LOG_TOOL_DETAILS` |
| `skill_name` | Skill name for the Skill tool | `OTEL_LOG_TOOL_DETAILS` |
| `subagent_type` | Subagent type for the Agent tool or legacy Task tool | `OTEL_LOG_TOOL_DETAILS` |

When `OTEL_LOG_TOOL_CONTENT=1`, this span also records a `tool.output` span event whose attributes contain the tool's input and output bodies, truncated at 60 KB per attribute.

### `claude_code.tool.blocked_on_user`

`duration_ms` (time spent waiting for the permission decision), `decision` (`accept` or `reject`), and `source` (decision source, matching the [Tool decision event](cc_otel_events_reference.md)).

### `claude_code.tool.execution`

`duration_ms` (time spent running the tool body), `tool_use_id` and `gen_ai.tool.call.id` (same value as the parent `claude_code.tool` span), `success` (`true`/`false`), and `error` — an error category string when execution failed, such as `Error:ENOENT` or `ShellError`, which contains the full error message instead when `OTEL_LOG_TOOL_DETAILS` is set.

### `claude_code.hook`

This span is emitted only when **detailed beta tracing** is active, which requires `ENABLE_BETA_TRACING_DETAILED=1` and `BETA_TRACING_ENDPOINT` in addition to the trace exporter configuration above. In interactive CLI sessions, this also requires your organization to be allowlisted for the feature; Agent SDK and non-interactive `-p` sessions are not gated. It is not emitted when only `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` is set.

| Attribute | Description | Gated by |
|---|---|---|
| `hook_event` | Hook event type, such as `PreToolUse` | |
| `hook_name` | Full hook name, such as `PreToolUse:Write` | |
| `num_hooks` | Number of matching hook commands executed | |
| `hook_definitions` | JSON-serialized hook configuration | `OTEL_LOG_TOOL_DETAILS` |
| `duration_ms` | Wall-clock duration of all matching hooks | |
| `num_success` | Count of hooks that completed successfully | |
| `num_blocking` | Count of hooks that returned a blocking decision | |
| `num_non_blocking_error` | Count of hooks that failed without blocking | |
| `num_cancelled` | Count of hooks cancelled before completion | |

Additional content-bearing attributes (`new_context`, `system_prompt_preview`, `user_system_prompt`, `tool_input`, `response.model_output`) are emitted only when detailed beta tracing is active and are not part of the stable span schema. `user_system_prompt` additionally requires `OTEL_LOG_USER_PROMPTS=1`; it carries only the system prompt text you provide via the `systemPrompt` SDK option or `--system-prompt`/`--append-system-prompt` flags, truncated at 60 KB, and is emitted once per session rather than per request.

**Source**: https://code.claude.com/docs/en/monitoring-usage
**Last Updated**: 2026-06-13
**Status**: Active
