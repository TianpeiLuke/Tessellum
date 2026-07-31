---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - opentelemetry
keywords:
  - openclaw opentelemetry export
  - diagnostics-otel plugin
  - otlp http protobuf
  - diagnostics.otel config
  - otel_exporter_otlp_endpoint
  - content capture privacy
  - samplerate flushintervalms
  - logsexporter stdout jsonl
  - openclaw_otel_preloaded
topics:
  - OpenClaw
  - OpenTelemetry Setup
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/opentelemetry
access_control_group: ["general"]
---

# OpenClaw — OpenTelemetry Export Setup

## Overview

This note is the operational procedure for enabling and tuning OpenClaw's OpenTelemetry export via the official `diagnostics-otel` plugin, which exports diagnostics over **OTLP/HTTP (protobuf)** and can also mirror diagnostic log records to stdout JSONL. It mirrors the setup half of the `gateway/opentelemetry` source page: how the diagnostics surface and plugin fit together, the install/quick-start config, the three independently toggled signals (traces/metrics/logs), the full `diagnostics.otel` configuration reference plus its `OTEL_*` environment-variable overrides, the privacy / content-capture controls, sampling/flushing tuning, running diagnostics without an exporter, and disabling. The exact exported metric, span, and diagnostic-event catalog lives in the sibling model note `oc_gateway_opentelemetry_signals` and is not repeated here.

## How It Fits Together

OpenClaw layers the export over an in-process diagnostics surface. **Diagnostics events** are structured, in-process records emitted by the Gateway and bundled plugins for model runs, message flow, sessions, queues, and exec. The **`diagnostics-otel` plugin** subscribes to those events and exports them as OpenTelemetry **metrics**, **traces**, and **logs** over OTLP/HTTP; it can also mirror diagnostic log records to stdout JSONL. **Provider calls** receive a W3C `traceparent` header from OpenClaw's trusted model-call span context when the provider transport accepts custom headers; plugin-emitted trace context is not propagated. Exporters only attach when **both** the diagnostics surface and the plugin are enabled, so the in-process cost stays near zero by default. Any collector or backend that accepts OTLP/HTTP works without code changes (the source names Grafana, Datadog, Honeycomb, New Relic, and Tempo as example backends). For local file logs and how to read them, the source defers to the Logging page.

## Quick Start

For packaged installs, install the plugin first, then enable it and the diagnostics surface in config. The plugin must appear in `plugins.allow` and be enabled under `plugins.entries`, and `diagnostics.enabled` plus `diagnostics.otel.enabled` must both be `true`.

```bash
openclaw plugins install clawhub:@openclaw/diagnostics-otel
```

```json5
{
  plugins: {
    allow: ["diagnostics-otel"],
    entries: {
      "diagnostics-otel": { enabled: true },
    },
  },
  diagnostics: {
    enabled: true,
    otel: {
      enabled: true,
      endpoint: "http://otel-collector:4318",
      protocol: "http/protobuf",
      serviceName: "openclaw-gateway",
      traces: true,
      metrics: true,
      logs: true,
      sampleRate: 0.2,
      flushIntervalMs: 60000,
    },
  },
}
```

You can also enable the plugin from the CLI instead of editing the `plugins.entries` block with `openclaw plugins enable diagnostics-otel`. Note from source: `protocol` currently supports `http/protobuf` only; `grpc` is ignored.

## Signals Exported

Three signal classes are emitted, each toggled independently via `diagnostics.otel.traces`, `diagnostics.otel.metrics`, and `diagnostics.otel.logs`:

| Signal | What goes in it |
|---|---|
| **Metrics** | Counters and histograms for token usage, cost, run duration, failover, skill usage, message flow, Talk events, queue lanes, session state/recovery, tool execution, oversized payloads, exec, and memory pressure. |
| **Traces** | Spans for model usage, model calls, harness lifecycle, skill usage, tool execution, exec, webhook/message processing, context assembly, and tool loops. |
| **Logs** | Structured `logging.file` records exported over OTLP or stdout JSONL when `diagnostics.otel.logs` is enabled; log bodies are withheld unless content capture is explicitly enabled. |

Traces and metrics default to **on** when `diagnostics.otel.enabled` is `true`. Logs default to **off** and are exported only when `diagnostics.otel.logs` is explicitly `true`. Log export defaults to OTLP; set `diagnostics.otel.logsExporter` to `stdout` for JSONL on stdout, or `both` to send each diagnostic log record to OTLP and stdout. (The exact metric/span names that travel in each signal are catalogued in the sibling signals note.)

## Configuration Reference

The full `diagnostics.otel` field block, reproduced verbatim from source:

```json5
{
  diagnostics: {
    enabled: true,
    otel: {
      enabled: true,
      endpoint: "http://otel-collector:4318",
      tracesEndpoint: "http://otel-collector:4318/v1/traces",
      metricsEndpoint: "http://otel-collector:4318/v1/metrics",
      logsEndpoint: "http://otel-collector:4318/v1/logs",
      protocol: "http/protobuf", // grpc is ignored
      serviceName: "openclaw-gateway",
      headers: { "x-collector-token": "..." },
      traces: true,
      metrics: true,
      logs: true,
      logsExporter: "otlp", // otlp | stdout | both
      sampleRate: 0.2, // root-span sampler, 0.0..1.0
      flushIntervalMs: 60000, // metric export interval (min 1000ms)
      captureContent: {
        enabled: false,
        inputMessages: false,
        outputMessages: false,
        toolInputs: false,
        toolOutputs: false,
        systemPrompt: false,
        toolDefinitions: false,
      },
    },
  },
}
```

`endpoint` is the shared OTLP/HTTP base; `tracesEndpoint` / `metricsEndpoint` / `logsEndpoint` are signal-specific overrides; `headers` carries collector auth (e.g. `x-collector-token`); `logsExporter` selects `otlp | stdout | both`; `sampleRate` and `flushIntervalMs` are covered under Sampling and flushing; `captureContent.*` is covered under Privacy and content capture.

### Environment Variables

These env vars override config at startup. For endpoints, the precedence is **signal-specific config > signal-specific env > shared endpoint**.

| Variable | Purpose |
|---|---|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Override `diagnostics.otel.endpoint`. If the value already contains `/v1/traces`, `/v1/metrics`, or `/v1/logs`, it is used as-is. |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` / `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` / `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` | Signal-specific endpoint overrides used when the matching `diagnostics.otel.*Endpoint` config key is unset. Signal-specific config wins over signal-specific env, which wins over the shared endpoint. |
| `OTEL_SERVICE_NAME` | Override `diagnostics.otel.serviceName`. |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | Override the wire protocol (only `http/protobuf` is honored today). |
| `OTEL_SEMCONV_STABILITY_OPT_IN` | Set to `gen_ai_latest_experimental` to emit the latest experimental GenAI inference span shape, including `{gen_ai.operation.name} {gen_ai.request.model}` span names, `CLIENT` span kind, and `gen_ai.provider.name` instead of the legacy `gen_ai.system`. GenAI metrics always use bounded, low-cardinality semantic attributes regardless. |
| `OPENCLAW_OTEL_PRELOADED` | Set to `1` when another preload or host process already registered the global OpenTelemetry SDK. The plugin then skips its own NodeSDK lifecycle but still wires diagnostic listeners and honors `traces`/`metrics`/`logs`. |

## Privacy and Content Capture

Raw model/tool content is **not** exported by default. Spans carry bounded identifiers (channel, provider, model, error category, hash-only request ids, tool source, tool owner, and skill name/source) and never include prompt text, response text, tool inputs, tool outputs, skill file paths, or session keys. OTLP log records keep severity, logger, code location, trusted trace context, and sanitized attributes by default, but the raw log message body is exported only when `diagnostics.otel.captureContent` is set to boolean `true`; granular `captureContent.*` subkeys do **not** enable log bodies. Labels that look like scoped agent session keys are replaced with `unknown`. Talk metrics export only bounded event metadata such as mode, transport, provider, and event type — they do not include transcripts, audio payloads, session ids, turn ids, call ids, room ids, or handoff tokens.

Outbound model requests may include a W3C `traceparent` header generated only from OpenClaw-owned diagnostic trace context for the active model call. Existing caller-supplied `traceparent` headers are replaced, so plugins or custom provider options cannot spoof cross-service trace ancestry.

Set `diagnostics.otel.captureContent.*` to `true` only when your collector and retention policy are approved for prompt, response, tool, or system-prompt text. Each subkey is opt-in independently:

- `inputMessages` — user prompt content.
- `outputMessages` — model response content.
- `toolInputs` — tool argument payloads.
- `toolOutputs` — tool result payloads.
- `systemPrompt` — assembled system/developer prompt.
- `toolDefinitions` — model tool names, descriptions, and schemas.

When any subkey is enabled, model and tool spans get bounded, redacted `openclaw.content.*` attributes for that class only. Use boolean `captureContent: true` only for broad diagnostics captures where OTLP log message bodies are also approved for export. `toolInputs`/`toolOutputs` content is captured for the built-in agent runtime's tool executions (`openclaw.content.tool_input` on completed/error spans, `openclaw.content.tool_output` on completed spans); external harness tool calls (Codex, Claude CLI) emit `tool.execution.*` spans without content payloads. Captured content travels on a trusted, listener-only channel and is never placed on the public diagnostic event bus.

## Sampling and Flushing

- **Traces:** `diagnostics.otel.sampleRate` is a root-span-only sampler — `0.0` drops all, `1.0` keeps all.
- **Metrics:** `diagnostics.otel.flushIntervalMs` is the metric export interval, with a minimum of `1000` ms.
- **Logs:** OTLP logs respect `logging.level` (the file log level). They use the diagnostic log-record redaction path, not console formatting. High-volume installs should prefer OTLP collector sampling/filtering over local sampling. Set `diagnostics.otel.logsExporter: "stdout"` when your platform already ships stdout/stderr to a log processor and you do not have an OTLP logs collector. Stdout records are one JSON object per line with `ts`, `signal`, `service.name`, severity, body, redacted attributes, and trusted trace fields when available.
- **File-log correlation:** JSONL file logs include top-level `traceId`, `spanId`, `parentSpanId`, and `traceFlags` when the log call carries a valid diagnostic trace context, which lets log processors join local log lines with exported spans.
- **Request correlation:** Gateway HTTP requests and WebSocket frames create an internal request trace scope. Logs and diagnostic events inside that scope inherit the request trace by default, while agent run and model-call spans are created as children so provider `traceparent` headers stay on the same trace.

## Without an Exporter

You can keep diagnostics events available to plugins or custom sinks without running `diagnostics-otel` — enable only the diagnostics surface:

```json5
{
  diagnostics: { enabled: true },
}
```

For targeted debug output without raising `logging.level`, use diagnostics flags. Flags are case-insensitive and support wildcards (e.g. `telegram.*` or `*`), and can be set in config:

```json5
{
  diagnostics: { flags: ["telegram.http"] },
}
```

Or as a one-off env override: `OPENCLAW_DIAGNOSTICS=telegram.http,telegram.payload openclaw gateway`. Flag output goes to the standard log file (`logging.file`) and is still redacted by `logging.redactSensitive`.

## Disable

Turn the OTLP export off by setting `diagnostics.otel.enabled` to `false`:

```json5
{
  diagnostics: { otel: { enabled: false } },
}
```

You can also leave `diagnostics-otel` out of `plugins.allow`, or run `openclaw plugins disable diagnostics-otel`.

**Source**: OpenClaw documentation — `gateway/opentelemetry` (mirror `inbox/openclaw_docs/gateway/opentelemetry.md`)
**Last Updated**: 2026-06-22
**Status**: Active
