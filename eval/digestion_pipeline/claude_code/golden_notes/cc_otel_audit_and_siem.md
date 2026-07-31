---
tags:
  - resource
  - documentation
  - claude_code
  - monitoring
  - audit
keywords:
  - audit security events
  - send events to siem
  - attribute actions to users
  - otel log tool details
  - audit mcp activity
  - security questions to events
  - otlp logs exporter
  - user identity attribution
topics:
  - Claude Code
  - Monitoring
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/monitoring-usage
access_control_group: ["general"]
---

# Claude Code — Audit Security Events and SIEM Export

## Overview

Claude Code's OpenTelemetry **events** are the audit data source for Claude Code activity. Every event carries identity attributes that tie tool calls, MCP activity, and permission decisions back to the user who triggered them, and the OTLP **logs exporter** can deliver these events to any Security Information and Event Management (SIEM) platform with an OTLP receiver — or to an OpenTelemetry Collector that forwards to your SIEM.

This note is the procedure for turning the event stream into an audit source: how actions attribute to users, how to surface full MCP/tool detail with `OTEL_LOG_TOOL_DETAILS`, how to map security questions to specific events, and how to point the logs exporter at a SIEM. For the full events catalog see [OTel Events Reference](cc_otel_events_reference.md); for enabling the exporter see [OTel Setup](cc_monitoring_opentelemetry_setup.md).

## Attribute actions to users

The standard attributes on each event include the authenticated user's identity: `user.email`, `user.account_uuid`, `user.account_id`, and `organization.id` when signed in with a Claude account, plus the installation-scoped `user.id` and the per-session `session.id`.

MCP tool calls, Bash commands, and file edits are therefore attributed to the developer who started the session. Claude Code does not act under a separate service account; the identity recorded on each event is the developer's own Claude account.

When Claude Code authenticates with a direct API key, or against Bedrock, Vertex AI, or Microsoft Foundry, there is no Claude account in the session and only `user.id` and `session.id` are populated. In these deployments, attach user identity yourself with `OTEL_RESOURCE_ATTRIBUTES`, set per user through the managed settings file or a launch wrapper:

```bash
export OTEL_RESOURCE_ATTRIBUTES="enduser.id=jdoe@example.com,enduser.directory_id=S-1-5-21-..."
```

## Audit MCP activity

To capture MCP server activity with full call detail, enable the logs exporter and set `OTEL_LOG_TOOL_DETAILS=1`. Each MCP operation then produces structured events that carry the server name, tool name, and call arguments alongside the standard identity attributes:

| Event | What it records for MCP |
|---|---|
| `mcp_server_connection` | Server connect, disconnect, and connection failure with `server_name`, `transport_type`, `server_scope`, and error detail |
| `tool_result` | Each MCP tool call with `tool_name` and `mcp_server_scope`, a `tool_parameters` payload containing `mcp_server_name` and `mcp_tool_name`, and a `tool_input` payload containing the call arguments |
| `tool_decision` | Whether the call was allowed or denied, whether the decision came from config, a hook, or the user, and a `tool_parameters` payload containing `mcp_server_name` and `mcp_tool_name` |

Without `OTEL_LOG_TOOL_DETAILS`, these events drop the identifying detail:

- `tool_result`: keeps `tool_name` and `mcp_server_scope`, omits `mcp_server_name`, `mcp_tool_name`, and arguments
- `tool_decision`: keeps `tool_name`, omits `tool_parameters`
- `mcp_server_connection`: omits `server_name` and the error message, but keeps `is_plugin`, `plugin_id_hash`, and `plugin.name`, with non-Anthropic plugin names redacted to the literal `"third-party"`, so plugin-provided servers remain distinguishable without detailed logging

## Map security questions to events

When building detection rules, look up the signal you want to monitor and query your backend for the corresponding event and attributes:

| Signal | Event | Key attributes |
|---|---|---|
| Tool call allowed or denied, and by what | `tool_decision` | `decision`, `source`, `tool_name`, `tool_parameters` |
| Permission mode escalation | `permission_mode_changed` | `from_mode`, `to_mode`, `trigger` |
| Policy hook blocked an action | `hook_execution_complete` | `hook_event`, `num_blocking` |
| Login, logout, and authentication failure | `auth` | `action`, `success`, `error_category` |
| MCP server connect or failure | `mcp_server_connection` | `status`, `server_name`, `is_plugin`, `error_code` |
| Plugin installed and its source | `plugin_installed` | `plugin.name`, `marketplace.name`, `marketplace.is_official` |
| Commands run and files touched | `tool_result` (executed) or `tool_decision` (rejected) with `OTEL_LOG_TOOL_DETAILS=1` | `tool_parameters`; `tool_input` (`tool_result` only) |

Claude Code emits the raw event stream only. Anomaly detection, baselining, correlation across sessions, and alerting are the responsibility of your SIEM or observability backend.

## Send events to a SIEM

Point `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` at your SIEM's OTLP receiver, or at an OpenTelemetry Collector that forwards to your SIEM's native ingest API. The following managed-settings example exports events only, with full tool detail enabled for MCP and Bash auditing:

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_LOG_TOOL_DETAILS": "1",
    "OTEL_EXPORTER_OTLP_LOGS_PROTOCOL": "http/protobuf",
    "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT": "https://siem.example.com:4318/v1/logs",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer your-siem-token"
  }
}
```

> Permission-mode and tool-decision semantics referenced in the question-mapping table are defined in the permissions docs (see https://code.claude.com/docs/en/iam). The privacy implications of enabling `OTEL_LOG_TOOL_DETAILS` — what each `OTEL_LOG_*` flag exposes and the default-redaction model — are covered by the data-usage docs (see https://code.claude.com/docs/en/data-usage) and the monitoring page's own Security and privacy section (see https://code.claude.com/docs/en/monitoring-usage).

**Source**: https://code.claude.com/docs/en/monitoring-usage
**Last Updated**: 2026-06-13
**Status**: Active
