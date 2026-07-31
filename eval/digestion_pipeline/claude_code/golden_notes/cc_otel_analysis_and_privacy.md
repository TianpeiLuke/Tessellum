---
tags:
  - resource
  - documentation
  - claude_code
  - monitoring
  - privacy
keywords:
  - interpret metrics and events
  - usage monitoring
  - cost monitoring
  - detect retry exhaustion
  - backend considerations
  - roi measurement
  - security and privacy
  - otel log flags redaction
topics:
  - Claude Code
  - Monitoring
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/monitoring-usage
access_control_group: ["general"]
---

# Claude Code — Telemetry Analysis, Backends, and Privacy

## Overview

Once Claude Code is exporting OpenTelemetry **metrics** and **events**, the operator has to decide what analyses to run, which backend to send each signal to, and how much sensitive content to expose. This note is the "now-use-the-data" layer over the metrics and events the other monitoring notes catalog: the analyses the data supports (usage, cost, alerting, retry-exhaustion detection, event analysis), the backend-selection trade-offs per signal type, the ROI-measurement resource, and — most importantly — the **opt-in privacy model** that governs what each `OTEL_LOG_*` flag reveals.

The recurring argument across these sections is a trade-off: richer telemetry (prompts, tool arguments, raw API bodies) buys deeper analysis and audit capability but increases the sensitive-data footprint, so Claude Code redacts content **by default** and makes each disclosure a deliberate opt-in scoped to the operator's own backend. For the metric and event definitions referenced here see [OTel Metrics Reference](cc_otel_metrics_reference.md) and [OTel Events Reference](cc_otel_events_reference.md); for enabling export see [OTel Setup](cc_monitoring_opentelemetry_setup.md).

## Interpret metrics and events data

The exported metrics and events support a range of analyses.

### Usage monitoring

| Metric | Analysis Opportunity |
|---|---|
| `claude_code.token.usage` | Break down by `type` (input/output), user, team, model, `skill.name`, `plugin.name`, or `agent.name` |
| `claude_code.session.count` | Track adoption and engagement over time |
| `claude_code.lines_of_code.count` | Measure productivity by tracking code additions and removals, broken down by model |
| `claude_code.commit.count` & `claude_code.pull_request.count` | Understand impact on development workflows |

### Cost monitoring

The `claude_code.cost.usage` metric helps with tracking usage trends across teams or individuals, identifying high-usage sessions for optimization, and attributing spend to specific skills, plugins, or subagent types via the `skill.name`, `plugin.name`, and `agent.name` attributes. Cost metrics are **approximations** — for official billing data, refer to your API provider (Claude Console, Amazon Bedrock, or Google Cloud Vertex). Spend-limit configuration and token-usage optimization are out of scope here; see the costs docs (https://code.claude.com/docs/en/costs).

### Alerting and segmentation

Common alerts to consider are cost spikes, unusual token consumption, and high session volume from specific users. All metrics can be segmented by the standard attributes. The `model` attribute is available on `claude_code.token.usage`, `claude_code.cost.usage`, and (from v2.1.172) `claude_code.lines_of_code.count`. Per-model breakdowns of commits can only be **approximated** by joining against the token or cost metrics on `session.id`, since one session can span multiple models.

### Detect retry exhaustion

Claude Code retries failed API requests internally and emits a single `claude_code.api_error` event only after it gives up, so the event itself is the terminal signal for that request — intermediate retry attempts are not logged as separate events. The `attempt` attribute on the event records how many attempts were made in total: a value **greater than** `CLAUDE_CODE_MAX_RETRIES` (default `10`) indicates the request exhausted all retries on a transient error, while a lower value indicates a non-retryable error such as a `400` response. To distinguish a session that recovered from one that stalled, group events by `session.id` and check whether a later `api_request` event exists after the error.

### Event analysis

The event data provides detailed insights into Claude Code interactions:

- **Tool Usage Patterns**: analyze `tool_result` events to identify the most frequently used tools, tool success rates, average tool execution times, and error patterns by tool type.
- **Performance Monitoring**: track API request durations and tool execution times to identify performance bottlenecks.

## Backend considerations

Your choice of metrics, logs, and traces backends determines the types of analyses you can perform.

**For metrics:**

- **Time series databases** (for example, Prometheus): rate calculations, aggregated metrics
- **Columnar stores** (for example, ClickHouse): complex queries, unique user analysis
- **Full-featured observability platforms** (for example, Honeycomb, Datadog, Grafana Cloud): advanced querying, visualization, alerting

**For events/logs:**

- **Log aggregation systems** (for example, Elasticsearch, Loki): full-text search, log analysis
- **Columnar stores** (for example, ClickHouse): structured event analysis
- **Full-featured observability platforms** (for example, Honeycomb, Datadog, Grafana Cloud): correlation between metrics and events

**For traces:** choose a backend that supports distributed trace storage and span correlation:

- **Distributed tracing systems** (for example, Jaeger, Zipkin, Grafana Tempo): span visualization, request waterfalls, latency analysis
- **Full-featured observability platforms** (for example, Honeycomb, Datadog, Grafana Cloud): trace search and correlation with metrics and logs

For organizations requiring Daily/Weekly/Monthly Active User (DAU/WAU/MAU) metrics, consider backends that support efficient unique value queries.

## ROI measurement resources

For a comprehensive guide on measuring return on investment for Claude Code — including telemetry setup, cost analysis, productivity metrics, and automated reporting — see the [Claude Code ROI Measurement Guide](https://github.com/anthropics/claude-code-monitoring-guide). That repository provides ready-to-use Docker Compose configurations, Prometheus and OpenTelemetry setups, and templates for generating productivity reports integrated with tools like Linear.

## Security and privacy

The privacy model is **opt-in by default**: content is redacted unless the operator deliberately enables a flag, and any enabled content is sent only to the operator's configured backend, never to Anthropic.

- OpenTelemetry export to your backend is opt-in and requires explicit configuration. For Anthropic's separate operational telemetry and how to disable it, see the data-usage docs (https://code.claude.com/docs/en/data-usage).
- Raw file contents and code snippets are **not** included in metrics or events. Trace spans are a separate data path (see the `OTEL_LOG_TOOL_CONTENT` flag below).
- When authenticated via OAuth, `user.email` is included in telemetry attributes. If this is a concern, work with your telemetry backend to filter or redact this field.
- **User prompt content** is not collected by default — only prompt length is recorded. To include prompt content, set `OTEL_LOG_USER_PROMPTS=1`.
- **Tool input arguments and parameters** are not logged by default. To include them, set `OTEL_LOG_TOOL_DETAILS=1`. This data is sent only to the OTEL endpoint you configure, never to Anthropic; arguments may still contain sensitive values, so configure your backend to filter or redact as needed. When enabled: `tool_result` and `tool_decision` events include a `tool_parameters` attribute (Bash commands, MCP server and tool names, skill names — `full_command` is emitted untruncated); `tool_result` events additionally include a `tool_input` attribute (file paths, URLs, search patterns, other arguments — individual values over 512 characters truncated, total bounded to ~4 K characters); `user_prompt` events include the verbatim `command_name` for custom, plugin, and MCP commands; trace spans include the same `tool_input` attribute and input-derived attributes such as `file_path`.
- **Tool input and output content** is not logged in trace spans by default. To include it, set `OTEL_LOG_TOOL_CONTENT=1` — span events then include full tool input and output content truncated at 60 KB per span, which can include raw file contents from Read tool results and Bash command output.
- **Raw Anthropic Messages API request and response bodies** are not logged by default. To include them, set `OTEL_LOG_RAW_API_BODIES`. With `=1`, each API call emits `api_request_body` and `api_response_body` log events whose `body` attribute is the JSON-serialized payload truncated at 60 KB; with `=file:<dir>`, untruncated bodies are written to `.request.json` and `.response.json` files under that directory and the events carry a `body_ref` path instead. In both modes bodies contain the **full conversation history** (system prompt, every prior user and assistant turn, tool results), so enabling this implies consent to everything the other `OTEL_LOG_*` content flags would reveal. Claude's extended-thinking content is always redacted from these bodies regardless of other settings.

> The data-usage / zero-data-retention policy this redaction model serves is owned by the data-usage docs (see https://code.claude.com/docs/en/data-usage and https://code.claude.com/docs/en/zero-data-retention).

## Monitor Claude Code on Amazon Bedrock

For detailed Claude Code usage monitoring guidance for Amazon Bedrock, see [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md). Bedrock-specific deployment configuration is otherwise out of scope here (see https://code.claude.com/docs/en/bedrock-vertex-proxies).

**Source**: https://code.claude.com/docs/en/monitoring-usage
**Last Updated**: 2026-06-13
**Status**: Active
