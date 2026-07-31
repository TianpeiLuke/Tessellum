---
tags:
  - resource
  - documentation
  - claude_code
  - monitoring
  - events
keywords:
  - claude code events
  - otel logs events
  - prompt.id correlation
  - tool_result event
  - tool_decision event
  - mcp_server_connection event
  - skill_activated event
  - compaction event
  - event.sequence
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

# Claude Code — OTel Events Reference

## Overview

Beyond [metrics](cc_otel_metrics_reference.md), Claude Code exports a structured stream of **events** via the OpenTelemetry logs/events protocol whenever `OTEL_LOGS_EXPORTER` is configured. Events are the log half of Claude Code's observable surface — the per-action records every audit and analysis query reads. Each event carries all of the [standard attributes](cc_otel_metrics_reference.md) shared with metrics, plus per-event `event.name`, an ISO 8601 `event.timestamp`, and `event.sequence` (a monotonically increasing counter for ordering events within a session). This note catalogs the event-correlation key `prompt.id` and each event type and its distinctive attributes.

## Event correlation attributes

When a user submits a prompt, Claude Code may make multiple API calls and run several tools. The `prompt.id` attribute lets you tie all of those events back to the single prompt that triggered them.

| Attribute | Description |
|-----------|-------------|
| `prompt.id` | UUID v4 identifier linking all events produced while processing a single user prompt |

To trace all activity triggered by a single prompt, filter your events by a specific `prompt.id` value: this returns the `user_prompt` event, any `api_request` events, and any `tool_result` events that occurred while processing that prompt. `prompt.id` is intentionally excluded from metrics because each prompt generates a unique ID, which would create an ever-growing number of time series — use it for event-level analysis and audit trails only.

## Prompt and tool lifecycle events

| Event Name | When logged | Distinctive attributes |
|------------|-------------|------------------------|
| `claude_code.user_prompt` | A user submits a prompt | `prompt_length`; `prompt` (redacted by default, enable with `OTEL_LOG_USER_PROMPTS=1`); `command_name` (built-in/bundled emitted as-is; custom/plugin/MCP collapse to `custom`/`mcp` unless `OTEL_LOG_TOOL_DETAILS=1`); `command_source` (`builtin`, `custom`, or `mcp`) |
| `claude_code.tool_result` | A tool completes execution (not emitted if the call was rejected) | `tool_name`, `tool_use_id`, `success`, `duration_ms`, `error_type`, `error` (gated), `decision_type` (always `"accept"`), `decision_source`, `tool_input_size_bytes`, `tool_result_size_bytes`, `mcp_server_scope`; `tool_parameters` and `tool_input` (both gated by `OTEL_LOG_TOOL_DETAILS=1`) |
| `claude_code.tool_decision` | A tool permission decision is made (accept/reject) | `tool_name`, `tool_use_id`, `decision` (`accept`/`reject`), `source`, and gated `tool_parameters` |

The `tool_use_id` on `tool_result` and `tool_decision` matches the id passed to hooks and the `tool_use_id` on the [`claude_code.tool` span](cc_otel_traces.md), allowing correlation between OTel events, traces, and hook-captured data. The `tool_decision` `source` value is one of `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, or `"user_reject"` — the same decision-source vocabulary documented for the permission system (see [permissions](https://code.claude.com/docs/en/permissions)).

## API request events

| Event Name | When logged | Distinctive attributes |
|------------|-------------|------------------------|
| `claude_code.api_request` | Each API request to Claude | `model`, `cost_usd`, `duration_ms`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`, `request_id`, `speed`, `query_source`, `effort`, plus skill/plugin/agent/MCP attribution |
| `claude_code.api_error` | An API request to Claude fails | `model`, `error`, `status_code`, `duration_ms`, `attempt`, `request_id`, `speed`, `query_source`, `effort`, plus attribution |
| `claude_code.api_refusal` | A request returns `stop_reason: "refusal"` (arrives on a successful stream, so no `api_error` fires) | `model`, `request_id` |
| `claude_code.api_retries_exhausted` | Once when a request fails after more than one attempt, alongside the final `api_error` | `model`, `error`, `status_code`, `total_attempts`, `total_retry_duration_ms`, `speed` |
| `claude_code.api_request_body` | Each request attempt when `OTEL_LOG_RAW_API_BODIES` is set (one per attempt) | `body` (inline, ≤60 KB) or `body_ref` (file mode), `body_length`, `body_truncated`, `model`, `query_source` |
| `claude_code.api_response_body` | Each successful response when `OTEL_LOG_RAW_API_BODIES` is set | `body` or `body_ref`, `body_length`, `body_truncated`, `model`, `query_source`, `request_id` |

Extended-thinking content is redacted from `api_request_body`/`api_response_body`. In file mode (`OTEL_LOG_RAW_API_BODIES=file:<dir>`) untruncated bodies are written to `.request.json` / `.response.json` files and the event carries a `body_ref` path instead of an inline body.

## Session, auth, and mode events

| Event Name | When logged | Distinctive attributes |
|------------|-------------|------------------------|
| `claude_code.permission_mode_changed` | The permission mode changes (Shift+Tab cycling, exiting plan mode, auto-mode gate check) | `from_mode`, `to_mode` (e.g. `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"bypassPermissions"`); `trigger` (`"shift_tab"`, `"exit_plan_mode"`, `"auto_gate_denied"`, or `"auto_opt_in"`) |
| `claude_code.auth` | `/login` or `/logout` completes | `action` (`"login"`/`"logout"`), `success`, `auth_method` (e.g. `"oauth"`), `error_category`, `status_code` |
| `claude_code.compaction` | Conversation compaction completes | `trigger` (`"auto"`/`"manual"`), `success`, `duration_ms`, `pre_tokens`, `post_tokens`, `error`, `precompute_reuse` (manual only: `"hit"` / `"miss_*"`) |
| `claude_code.feedback_survey` | A session quality survey is shown or answered | `event_type` (e.g. `"appeared"`, `"responded"`, `"transcript_prompt_appeared"`), `appearance_id`, `survey_type` (`"session"` = "How is Claude doing?"), `response`, `enabled_via_override` |

## MCP, mention, and internal-error events

| Event Name | When logged | Distinctive attributes |
|------------|-------------|------------------------|
| `claude_code.mcp_server_connection` | An MCP server connects, disconnects, or fails to connect | `status` (`"connected"`/`"failed"`/`"disconnected"`), `transport_type` (`"stdio"`/`"sse"`/`"http"`), `server_scope` (`"user"`/`"project"`/`"local"`), `duration_ms`, `error_code`, `is_plugin`, `plugin_id_hash`/`plugin.name` (when `is_plugin`); `server_name` and `error` gated by `OTEL_LOG_TOOL_DETAILS=1` |
| `claude_code.at_mention` | Claude Code resolves an `@`-mention (early-exit paths like permission denials, oversized files, PDF reference attachments, and directory-listing failures do not log) | `mention_type` (`"file"`, `"directory"`, `"agent"`, `"mcp_resource"`), `success` |
| `claude_code.internal_error` | Claude Code catches an unexpected internal error (not emitted on Bedrock/Vertex/Foundry or when `DISABLE_ERROR_REPORTING` is set) | `error_name` (class name, e.g. `"TypeError"`); `error_code` (Node.js errno such as `"ENOENT"`). Error message and stack trace are never included |

## Plugin, skill, and hook inventory events

| Event Name | When logged | Distinctive attributes |
|------------|-------------|------------------------|
| `claude_code.plugin_installed` | A plugin finishes installing (from `claude plugin install` or the `/plugin` UI) | `marketplace.is_official`, `install.trigger` (`"cli"`/`"ui"`), `plugin.name`, `plugin.version`, `marketplace.name` (last three gated for third-party marketplaces) |
| `claude_code.plugin_loaded` | Once per enabled plugin at session start (fleet inventory) | `plugin.name`, `marketplace.name`, `plugin.version`, `plugin.scope`, `enabled_via`, `plugin_id_hash`, `has_hooks`, `has_mcp`, `host_owned_mcp`, `skill_path_count`, `command_path_count`, `agent_path_count`, `safe_mode` |
| `claude_code.skill_activated` | A skill is invoked via the Skill tool or a `/` command | `skill.name` (placeholder `"custom_skill"` for user-defined/third-party unless `OTEL_LOG_TOOL_DETAILS=1`), `invocation_trigger` (`"user-slash"`/`"claude-proactive"`/`"nested-skill"`), `skill.source`, `skill.kind`, gated `plugin.name`/`marketplace.name` |
| `claude_code.hook_registered` | Once per configured hook at session start (fleet inventory) | `hook_event`, `hook_type` (`"command"`/`"prompt"`/`"mcp_tool"`/`"http"`/`"agent"`), `hook_source`, `safe_mode`, gated `hook_matcher`, plugin attribution |
| `claude_code.hook_execution_start` | One or more hooks begin executing for a hook event | `hook_event`, `hook_name`, `num_hooks`, `managed_only`, `hook_source`, `safe_mode`, `hook_definitions` (detailed-beta + gated) |
| `claude_code.hook_execution_complete` | All hooks for a hook event have finished | `hook_event`, `hook_name`, `num_hooks`, `num_success`, `num_blocking`, `num_non_blocking_error`, `num_cancelled`, `total_duration_ms`, `managed_only`, `hook_source`, `safe_mode` |
| `claude_code.hook_plugin_metrics` | An official-marketplace plugin hook emits per-invocation metrics (third-party/user hooks do not emit) | `plugin_id` (`<name>@<marketplace>`), `hook_event`, plus up to 20 plugin-emitted metric keys matching `^[a-z][a-z0-9_]{0,39}$` with boolean or number values |

**Source**: https://code.claude.com/docs/en/monitoring-usage
**Last Updated**: 2026-06-13
**Status**: Active
