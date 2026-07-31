---
tags:
  - resource
  - documentation
  - claude_code
  - monitoring
  - metrics
keywords:
  - claude code metrics
  - otel metrics reference
  - standard attributes
  - token usage metric
  - cost usage metric
  - session count
  - code edit tool decision
  - active time counter
  - metric cardinality attributes
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

# Claude Code — OTel Metrics Reference

## Overview

Claude Code exports **eight metrics** via the OpenTelemetry metrics protocol (time-series data) when telemetry is enabled. These counters cover session activity, code output, version-control impact, spend, token consumption, code-edit permission decisions, and active engagement time. Every metric datapoint carries a shared set of **standard attributes** (identity, session, version, terminal, and any custom resource-attribute keys), and several metrics add their own context-specific attributes. This note catalogs the standard attribute set, the eight metric series, and the per-metric attributes that become queryable labels in your metrics backend.

This is the metrics half of the source page's "Available metrics and events" section. The events/logs catalog (the `~26` event types) is documented in the sibling note [OTel Events Reference](cc_otel_events_reference.md). The `Standard attributes` table is defined here once and referenced by that note. For how to enable telemetry and choose exporters, see [OpenTelemetry Setup](cc_monitoring_opentelemetry_setup.md); the cardinality-control variables that toggle several standard attributes are in [OTel Configuration Variables](cc_otel_configuration_variables.md).

## Standard attributes

All metrics and events share these standard attributes:

| Attribute | Description | Controlled By |
| --- | --- | --- |
| `session.id` | Unique session identifier | `OTEL_METRICS_INCLUDE_SESSION_ID` (default: true) |
| `app.version` | Current Claude Code version | `OTEL_METRICS_INCLUDE_VERSION` (default: false) |
| `app.entrypoint` | How the session was launched, such as `cli`, `sdk-cli`, `sdk-ts`, `sdk-py`, or `claude-vscode` | `OTEL_METRICS_INCLUDE_ENTRYPOINT` (default: false) |
| `organization.id` | Organization UUID (when authenticated) | Always included when available |
| `user.account_uuid` | Account UUID (when authenticated) | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (default: true) |
| `user.account_id` | Account ID in tagged format matching Anthropic admin APIs (when authenticated), such as `user_01BWBeN28...` | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (default: true) |
| `user.id` | Random anonymous identifier generated on first run and persisted in `~/.claude.json`. Contains no personal information and is not derived from your Claude account. Deleting the file produces a new unrelated value on next run. | Always included |
| `user.email` | User email address (when authenticated via OAuth) | Always included when available |
| `terminal.type` | Terminal type, such as `iTerm.app`, `vscode`, `cursor`, or `tmux` | Always included when detected |
| Keys from `OTEL_RESOURCE_ATTRIBUTES` | Custom attributes you set, such as `department` or `team.id` | `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES` (default: true) |

Events additionally include attributes that are never attached to metrics because they would cause unbounded cardinality: `prompt.id` (a UUID correlating a user prompt with all subsequent events until the next prompt) and `workspace.host_paths` (host workspace directories selected in the desktop app, as a string array). These are covered in [OTel Events Reference](cc_otel_events_reference.md).

## Metrics

Claude Code exports the following metrics:

| Metric Name | Description | Unit |
| --- | --- | --- |
| `claude_code.session.count` | Count of CLI sessions started | count |
| `claude_code.lines_of_code.count` | Count of lines of code modified | count |
| `claude_code.pull_request.count` | Number of pull requests created | count |
| `claude_code.commit.count` | Number of git commits created | count |
| `claude_code.cost.usage` | Cost of the Claude Code session | USD |
| `claude_code.token.usage` | Number of tokens used | tokens |
| `claude_code.code_edit_tool.decision` | Count of code editing tool permission decisions | count |
| `claude_code.active_time.total` | Total active time in seconds | s |

## Metric details

Each metric includes the standard attributes above. Metrics with additional context-specific attributes are noted below.

### Session counter

Incremented at the start of each session. Adds `start_type`: how the session was started — one of `"fresh"`, `"resume"`, or `"continue"`.

### Lines of code counter

Incremented when code is added or removed. Adds:

- `type`: (`"added"`, `"removed"`)
- `model`: Model identifier for the model that made the change (for example, `"claude-sonnet-4-6"`). Requires Claude Code v2.1.172 or later.

### Pull request counter

Incremented when Claude Code creates a pull request or merge request through a shell command or an MCP tool. Adds only the standard attributes.

### Commit counter

Incremented when creating git commits via Claude Code. Adds only the standard attributes.

### Cost counter

Incremented after each API request. Beyond the standard attributes it adds:

- `model`: Model identifier (for example, `"claude-sonnet-4-6"`)
- `query_source`: Category of the subsystem that issued the request — one of `"main"`, `"subagent"`, or `"auxiliary"`
- `speed`: `"fast"` when the request used fast mode; absent otherwise
- `effort`: Effort level applied to the request: `"low"`, `"medium"`, `"high"`, `"xhigh"`, or `"max"`; absent when the model does not support effort
- `agent.name`: Subagent type that issued the request. Built-in agent names and agents from official-marketplace plugins appear verbatim; other user-defined agent names are replaced with `"custom"`; absent when the request was not issued by a named subagent type
- `skill.name`: Skill active for the request, set by the Skill tool, a `/` command, or inherited by a spawned subagent. Built-in, bundled, user-defined, and official-marketplace plugin skill names appear verbatim; third-party plugin skill names are replaced with `"third-party"`; absent when no skill is active
- `plugin.name`: Owning plugin when the active skill or subagent is provided by a plugin. Official-marketplace plugin names appear verbatim; third-party plugin names are replaced with `"third-party"`; absent when neither the skill nor the subagent has an owning plugin
- `marketplace.name`: Marketplace the owning plugin was installed from. Only emitted for official-marketplace plugins; absent otherwise
- `mcp_server.name`: MCP server whose tool ran in the turn that produced this request. Built-in, claude.ai-proxied, and official-registry server names appear verbatim; user-configured server names are replaced with `"custom"`; absent when no MCP tool ran
- `mcp_tool.name`: MCP tool that ran in the turn that produced this request, with the same redaction as `mcp_server.name`; absent when no MCP tool ran

### Token counter

Incremented after each API request. Beyond the standard attributes it adds:

- `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
- `model`: Model identifier (for example, `"claude-sonnet-4-6"`)
- `query_source`: Category of the subsystem that issued the request — one of `"main"`, `"subagent"`, or `"auxiliary"`
- `speed`: `"fast"` when the request used fast mode; absent otherwise
- `effort`: Effort level applied to the request (see Cost counter)
- `agent.name`, `skill.name`, `plugin.name`, `marketplace.name`, `mcp_server.name`, `mcp_tool.name`: skill, plugin, agent, and MCP attribution for the request, with the same definitions and redaction behavior as on the Cost counter

### Code edit tool decision counter

Incremented when the user accepts or rejects Edit, Write, or NotebookEdit tool usage. Beyond the standard attributes it adds:

- `tool_name`: Tool name (`"Edit"`, `"Write"`, `"NotebookEdit"`)
- `decision`: User decision (`"accept"`, `"reject"`)
- `source`: Where the decision came from — one of `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, or `"user_reject"` (see the Tool decision event in [OTel Events Reference](cc_otel_events_reference.md) for what each value means)
- `language`: Programming language of the edited file, such as `"TypeScript"`, `"Python"`, `"JavaScript"`, or `"Markdown"`; returns `"unknown"` for unrecognized file extensions

### Active time counter

Tracks actual time spent actively using Claude Code, excluding idle time. Incremented during user interactions (typing, reading responses) and during CLI processing (tool execution, AI response generation). Adds `type`: `"user"` for keyboard interactions, `"cli"` for tool execution and AI responses.

**Source**: https://code.claude.com/docs/en/monitoring-usage
**Last Updated**: 2026-06-13
**Status**: Active
