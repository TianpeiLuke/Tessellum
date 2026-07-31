---
tags:
  - resource
  - documentation
  - claude_code
  - monitoring
  - opentelemetry
keywords:
  - opentelemetry setup
  - claude_code_enable_telemetry
  - otlp exporter
  - managed settings telemetry
  - mdm fleet rollout
  - export interval
  - service resource attributes
  - otel metrics exporter
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

# Claude Code — Enable OpenTelemetry Telemetry

## Overview

Claude Code can export usage, cost, and tool-activity telemetry to your own monitoring stack through OpenTelemetry (OTel). It emits **metrics** as time-series data, **events** via the logs/events protocol, and optionally distributed **traces**. This note is the operator-facing setup path: turn telemetry on, choose exporters, point at an OTLP endpoint, and supply authentication — either per-user via environment variables or fleet-wide via a managed settings file.

The configuration is entirely environment-variable driven. This note covers the quick-start variables, administrator (MDM) rollout, the per-scenario example export blocks, and the service-level resource attributes attached to every signal. The full variable catalog (per-signal overrides, cardinality control, mTLS, dynamic headers) lives in [OTel Configuration Variables](cc_otel_configuration_variables.md); the metrics and events catalogs live in [OTel Metrics Reference](cc_otel_metrics_reference.md) and [OTel Events Reference](cc_otel_events_reference.md).

## Quick start

Configure OpenTelemetry using environment variables:

```bash theme={null}
# 1. Enable telemetry
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Choose exporters (both are optional - configure only what you need)
export OTEL_METRICS_EXPORTER=otlp       # Options: otlp, prometheus, console, none
export OTEL_LOGS_EXPORTER=otlp          # Options: otlp, console, none

# 3. Configure OTLP endpoint (for OTLP exporter)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Set authentication (if required)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. For debugging: reduce export intervals
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 seconds (default: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 seconds (default: 5000ms)

# 6. Run Claude Code
claude
```

`CLAUDE_CODE_ENABLE_TELEMETRY=1` is the master switch; the two exporter variables are independently optional, so you can configure only metrics, only events, or both. The default export intervals are 60 seconds for metrics and 5 seconds for logs. Shorter intervals are useful for debugging during setup; reset them for production use. For full configuration options, see the [OpenTelemetry specification](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## Administrator configuration

Administrators can configure OpenTelemetry settings for all users through the [managed settings file](https://code.claude.com/docs/en/settings#settings-files), giving centralized control across an organization. Settings precedence governs how these are applied (see [settings](https://code.claude.com/docs/en/settings#settings-precedence)).

Example managed settings configuration:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

Managed settings can be distributed via MDM (Mobile Device Management) or other device management solutions. Environment variables defined in the managed settings file have high precedence and **cannot be overridden by users** — the mechanism for enforcing telemetry across a fleet.

Claude Code does **not** pass `OTEL_*` environment variables to the subprocesses it spawns, including the Bash tool, hooks, MCP servers, and language servers. An OpenTelemetry-instrumented application that you run through the Bash tool does not inherit Claude Code's exporter endpoint or headers, so set those variables directly in the command if that application needs to export its own telemetry.

## Example configurations

Set these environment variables before running `claude`. Each block is a complete configuration for a different exporter or deployment scenario. The console-debugging, Prometheus, multiple-exporter, split-endpoint, metrics-only, and events-only variants all build on the same `CLAUDE_CODE_ENABLE_TELEMETRY=1` switch:

```bash theme={null}
# Console debugging (1-second intervals)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# Multiple exporters
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json
```

For deployments that need to split signals across backends, point metrics and logs at different endpoints with the per-signal override variables:

```bash theme={null}
# Different endpoints/backends for metrics and logs
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317

# Metrics only (no events/logs)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Events/logs only (no metrics)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

The per-signal override variables (`OTEL_EXPORTER_OTLP_METRICS_*`, `OTEL_EXPORTER_OTLP_LOGS_*`) and the rest of the configuration knobs are documented in [OTel Configuration Variables](cc_otel_configuration_variables.md). To enable distributed tracing on top of this setup, see [OTel Traces](cc_otel_traces.md).

## Service information

All metrics and events are exported with the following resource attributes, which identify the emitting service and host to your backend:

* `service.name`: `claude-code`
* `service.version`: Current Claude Code version
* `os.type`: Operating system type (for example, `linux`, `darwin`, `windows`)
* `os.version`: Operating system version string
* `host.arch`: Host architecture (for example, `amd64`, `arm64`)
* `wsl.version`: WSL version number (only present when running on Windows Subsystem for Linux)
* Meter Name: `com.anthropic.claude_code`

These resource-level attributes are distinct from the per-signal standard attributes (`session.id`, `user.id`, etc.) catalogued in [OTel Metrics Reference](cc_otel_metrics_reference.md). For using the event stream as a security audit/SIEM source, see [OTel Audit and SIEM](cc_otel_audit_and_siem.md); for analysis, backend choice, and the privacy model, see the source page's [Interpret metrics and events data / Backend considerations / Security and privacy](https://code.claude.com/docs/en/monitoring-usage) sections.

**Source**: https://code.claude.com/docs/en/monitoring-usage
**Last Updated**: 2026-06-13
**Status**: Active
