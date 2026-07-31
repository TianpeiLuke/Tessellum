---
tags:
  - resource
  - documentation
  - claude_code
  - monitoring
  - opentelemetry
keywords:
  - otel configuration variables
  - otlp exporter endpoint protocol
  - per-signal override
  - metrics cardinality control
  - mtls client certificate
  - dynamic headers helper
  - otel_resource_attributes
  - multi-team attributes
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

# Claude Code — OpenTelemetry Configuration Variables

## Overview

Once telemetry is enabled, Claude Code's OpenTelemetry (OTel) export is shaped by a set of environment variables and one settings key. This note is the reference for those configuration knobs: the **common OTLP variables** (protocol, endpoint, export intervals, and per-signal overrides), the **mTLS client-certificate** variables that secure the exporter connection, the **metrics cardinality-control** toggles that decide which attributes ride along on each datapoint, the **dynamic-headers helper** script for enterprise token auth, and the **`OTEL_RESOURCE_ATTRIBUTES`** mechanism for multi-team labeling.

These are the configuration details that sit between turning telemetry on (see [Monitoring setup](https://code.claude.com/docs/en/monitoring-usage)) and reading the metrics/events catalogs. The same OTLP settings here also apply to [traces (beta)](https://code.claude.com/docs/en/monitoring-usage). For the canonical Claude Code environment-variable reference and the managed-settings/network mTLS treatment, this note links out rather than duplicating.

## Common configuration variables

These variables configure exporter selection, the OTLP endpoint and protocol, export intervals, content-logging gates, and metrics temporality. The endpoint/protocol can be set once for all signals (`OTEL_EXPORTER_OTLP_PROTOCOL`, `OTEL_EXPORTER_OTLP_ENDPOINT`) or overridden per signal (the `*_METRICS_*` and `*_LOGS_*` variants).

| Environment Variable | Description | Example Values |
| --- | --- | --- |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enables telemetry collection (required) | `1` |
| `OTEL_METRICS_EXPORTER` | Metrics exporter types, comma-separated. Use `none` to disable | `console`, `otlp`, `prometheus`, `none` |
| `OTEL_LOGS_EXPORTER` | Logs/events exporter types, comma-separated. Use `none` to disable | `console`, `otlp`, `none` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | Protocol for OTLP exporter, applies to all signals | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint for all signals | `http://localhost:4317` |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL` | Protocol for metrics, overrides general setting | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` | OTLP metrics endpoint, overrides general setting | `http://localhost:4318/v1/metrics` |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL` | Protocol for logs, overrides general setting | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` | OTLP logs endpoint, overrides general setting | `http://localhost:4318/v1/logs` |
| `OTEL_EXPORTER_OTLP_HEADERS` | Authentication headers for OTLP | `Authorization=Bearer token` |
| `OTEL_METRIC_EXPORT_INTERVAL` | Export interval in milliseconds (default: 60000) | `5000`, `60000` |
| `OTEL_LOGS_EXPORT_INTERVAL` | Logs export interval in milliseconds (default: 5000) | `1000`, `10000` |
| `OTEL_LOG_USER_PROMPTS` | Enable logging of user prompt content (default: disabled) | `1` to enable |
| `OTEL_LOG_TOOL_DETAILS` | Enable logging of tool parameters and input arguments in tool events and trace span attributes: Bash commands, MCP server and tool names, skill names, and tool input. Also enables custom, plugin, and MCP command names on `user_prompt` events (default: disabled) | `1` to enable |
| `OTEL_LOG_TOOL_CONTENT` | Enable logging of tool input and output content in span events (default: disabled). Requires tracing. Content is truncated at 60 KB | `1` to enable |
| `OTEL_LOG_RAW_API_BODIES` | Emit the full Anthropic Messages API request and response JSON as `api_request_body` / `api_response_body` log events (default: disabled). Bodies include the entire conversation history | `1` for inline bodies truncated at 60 KB, or `file:<dir>` for untruncated bodies on disk with a `body_ref` pointer in the event |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Metrics temporality preference (default: `delta`). Set to `cumulative` if your backend expects cumulative temporality | `delta`, `cumulative` |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` | Interval for refreshing dynamic headers (default: 1740000ms / 29 minutes) | `900000` |

The content-logging gates (`OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS`, `OTEL_LOG_TOOL_CONTENT`, `OTEL_LOG_RAW_API_BODIES`) are off by default; their privacy implications are covered in the analysis-and-privacy note. For the canonical Claude Code env-var reference, see [`env-vars`](https://code.claude.com/docs/en/env-vars).

## mTLS authentication

How you configure client certificates for the OTLP exporter depends on the OTLP protocol in use for that signal, set via `OTEL_EXPORTER_OTLP_PROTOCOL` or the per-signal override. The same configuration applies to metrics, logs, and traces.

| Protocol | Client certificate variables | Trust the collector's CA with |
| --- | --- | --- |
| `http/protobuf`, `http/json` | `CLAUDE_CODE_CLIENT_CERT`, `CLAUDE_CODE_CLIENT_KEY`, and optionally `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`. See [Network configuration](https://code.claude.com/docs/en/network-config) | `NODE_EXTRA_CA_CERTS` |
| `grpc` | `OTEL_EXPORTER_OTLP_CLIENT_KEY` and `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE`, or the per-signal variants such as `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY` to use a different certificate per signal | `OTEL_EXPORTER_OTLP_CERTIFICATE` |

For `grpc`, the OpenTelemetry SDK reads the standard OTLP variables directly, so existing configurations that set the per-signal metrics variables continue to work. The canonical mTLS treatment lives in the network-config docs ([`network-config`](https://code.claude.com/docs/en/network-config)).

## Metrics cardinality control

The following environment variables control which attributes are included in metrics to manage cardinality. Lower cardinality generally means better performance and lower storage costs in your metrics backend, but less granular data for analysis.

| Environment Variable | Description | Default Value | Example to Disable |
| --- | --- | --- | --- |
| `OTEL_METRICS_INCLUDE_SESSION_ID` | Include session.id attribute in metrics | `true` | `false` |
| `OTEL_METRICS_INCLUDE_VERSION` | Include app.version attribute in metrics | `false` | `true` |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Include user.account_uuid and user.account_id attributes in metrics | `true` | `false` |
| `OTEL_METRICS_INCLUDE_ENTRYPOINT` | Include app.entrypoint attribute in metrics | `false` | `true` |
| `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES` | Include keys from `OTEL_RESOURCE_ATTRIBUTES` as attributes on metric datapoints | `true` | `false` |

These toggles trade granularity against the storage and query cost of high-cardinality label sets in the metrics backend.

## Dynamic headers

For enterprise environments that require dynamic authentication, you can configure a script to generate headers dynamically. Dynamic headers apply only to the `http/protobuf` and `http/json` protocols. The `grpc` exporter uses only the static `OTEL_EXPORTER_OTLP_HEADERS` value.

**Settings configuration** — add the helper to your `.claude/settings.json`:

```json
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

The value can be the path to an executable file, including a path that contains spaces, or a shell command line with arguments. On Windows, the value always runs through the shell, so quote a path that contains spaces inside the JSON value.

**Script requirements** — the script must output valid JSON with string key-value pairs representing HTTP headers (for example, `echo "{\"Authorization\": \"Bearer $(get-token.sh)\"}"`). If the helper fails or prints output that doesn't meet these requirements, Claude Code reports the error in `/doctor` output, the debug log (when running with `--debug` or after `/debug`), and stderr in non-interactive sessions started with `-p`.

**Refresh behavior** — the headers helper script runs at startup and periodically thereafter to support token refresh. By default, the script runs every 29 minutes; customize the interval with the `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` environment variable.

## Multi-team organization support

Organizations with multiple teams or departments can add custom attributes to distinguish between different groups using the `OTEL_RESOURCE_ATTRIBUTES` environment variable:

```bash
# Add custom attributes for team identification
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

These custom attributes are included in all metrics and events, allowing you to filter metrics by team or department, track costs per cost center, create team-specific dashboards, and set up alerts for specific teams. Claude Code attaches these values as attributes on every metric datapoint and event record, in addition to sending them in the OTLP resource block; because most metrics backends expose datapoint attributes as queryable labels, you can group and filter by your custom keys directly. Custom keys never override the standard attributes such as `user.id` or `session.id`: when a key collides, Claude Code keeps the built-in value.

Each custom key becomes a label on every metric series, so high-cardinality values increase storage cost. To send custom attributes in the resource block only and omit them from datapoint labels, set `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES=false` (see Metrics cardinality control above).

**Formatting requirements for `OTEL_RESOURCE_ATTRIBUTES`** — the variable uses comma-separated `key=value` pairs with strict rules: **no spaces allowed** in values (for example, `user.organizationName=My Company` is invalid); the format must be comma-separated `key1=value1,key2=value2`; only US-ASCII characters are allowed, excluding control characters, whitespace, double quotes, commas, semicolons, and backslashes; and characters outside the allowed range must be percent-encoded. Use underscores or camelCase instead of spaces (`org.name=Johns_Organization` or `org.name=JohnsOrganization`), or percent-encode (`org.name=John%27s%20Organization`). Wrapping values in quotes does not escape spaces — `org.name="My Company"` results in the literal value `"My Company"` with quotes included.

**Source**: https://code.claude.com/docs/en/monitoring-usage
**Last Updated**: 2026-06-13
**Status**: Active
