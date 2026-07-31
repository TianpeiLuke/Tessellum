---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - logging
keywords:
  - openclaw logging configuration
  - logging.level consoleLevel
  - OPENCLAW_LOG_LEVEL log-level precedence
  - OPENCLAW_DEBUG_MODEL_TRANSPORT
  - trace correlation traceid spanid
  - model call size timing
  - redactSensitive redactPatterns
  - diagnostics opentelemetry otlp
topics:
  - OpenClaw
  - Logging Configuration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/logging
access_control_group: ["general"]
---

# OpenClaw — Configuring Logging (Levels, Diagnostics, Redaction, OpenTelemetry)

## Overview

This note is the configuration half of OpenClaw logging: how to set log levels and console styles, raise targeted model-transport diagnostics without flooding all logs, correlate logs with traces, read bounded model-call size/timing fields, redact secrets, and route diagnostics to OpenTelemetry. It mirrors the `logging` source page sections from **Configuring logging** through **Diagnostics and OpenTelemetry**. The companion note [oc_logging_surfaces](oc_logging_surfaces.md) covers where logs live and how to read them. All logging configuration lives under the `logging` key in `~/.openclaw/openclaw.json`.

## Configuring logging

All logging configuration lives under `logging` in `~/.openclaw/openclaw.json`. The full set of fields is:

```json
{
  "logging": {
    "level": "info",
    "file": "/tmp/openclaw/openclaw-YYYY-MM-DD.log",
    "consoleLevel": "info",
    "consoleStyle": "pretty",
    "redactSensitive": "tools",
    "redactPatterns": ["sk-.*"]
  }
}
```

## Log levels

OpenClaw separates the file-log level from the console level:

- `logging.level`: **file logs** (JSONL) level.
- `logging.consoleLevel`: **console** verbosity level.

You can override both via the **`OPENCLAW_LOG_LEVEL`** environment variable (e.g. `OPENCLAW_LOG_LEVEL=debug`). The env var takes precedence over the config file, so you can raise verbosity for a single run without editing `openclaw.json`. You can also pass the global CLI option **`--log-level <level>`** (for example, `openclaw --log-level debug gateway run`), which overrides the environment variable for that command. The resulting precedence ladder is therefore config file < `OPENCLAW_LOG_LEVEL` env var < `--log-level` CLI flag.

`--verbose` only affects console output and WS log verbosity; it does not change file log levels.

## Targeted model transport diagnostics

When debugging provider calls, use targeted environment flags instead of raising all logs to `debug`:

```bash
OPENCLAW_DEBUG_MODEL_TRANSPORT=1 openclaw gateway
OPENCLAW_DEBUG_MODEL_PAYLOAD=tools OPENCLAW_DEBUG_SSE=events openclaw gateway
```

Available flags:

- `OPENCLAW_DEBUG_MODEL_TRANSPORT=1`: emit request start, fetch response, SDK headers, first streaming event, stream completion, and transport errors at `info` level.
- `OPENCLAW_DEBUG_MODEL_PAYLOAD=summary`: include a bounded request payload summary in model request logs.
- `OPENCLAW_DEBUG_MODEL_PAYLOAD=tools`: include all model-facing tool names in the payload summary.
- `OPENCLAW_DEBUG_MODEL_PAYLOAD=full-redacted`: include a redacted, capped JSON payload snapshot. Use only while debugging; secrets are redacted but prompts and message text may still be present.
- `OPENCLAW_DEBUG_SSE=events`: emit first-event and stream-completion timing.
- `OPENCLAW_DEBUG_SSE=peek`: also emit the first five redacted SSE event payloads, capped per event.
- `OPENCLAW_DEBUG_CODE_MODE=1`: emit code-mode model-surface diagnostics, including when native provider tools are hidden because code mode owns the tool surface.

These flags log through normal OpenClaw logging, so `openclaw logs --follow` and the Control UI Logs tab show them. Without the flags, the same diagnostics remain available at `debug` level.

## Trace correlation

File logs are JSONL. When a log call carries a valid diagnostic trace context, OpenClaw writes the trace fields as top-level JSON keys (`traceId`, `spanId`, `parentSpanId`, `traceFlags`) so external log processors can correlate the line with OTEL spans and provider `traceparent` propagation.

Gateway HTTP requests and Gateway WebSocket frames establish an internal request trace scope. Logs and diagnostic events emitted inside that async scope inherit the request trace when they do not pass an explicit trace context. Agent run and model-call traces become children of the active request trace, so local logs, diagnostic snapshots, OTEL spans, and trusted provider `traceparent` headers can be joined by `traceId` without logging raw request or model content.

Talk lifecycle log records also flow to diagnostics-otel log export when OpenTelemetry log export is enabled, using the same bounded attributes as file logs. Configure `diagnostics.otel.logsExporter` to choose OTLP, stdout JSONL, or both sinks.

## Model call size and timing

Model-call diagnostics record bounded request/response measurements without capturing raw prompt or response content:

- `requestPayloadBytes`: UTF-8 byte size of the final model request payload
- `responseStreamBytes`: UTF-8 byte size of streamed model response chunk payloads. High-frequency text, thinking, and tool-call delta events count only the incremental `delta` bytes instead of full `partial` snapshots.
- `timeToFirstByteMs`: elapsed time before the first streamed response event
- `durationMs`: total model-call duration

These fields are available to diagnostic snapshots, model-call plugin hooks, and OTEL model-call spans/metrics when diagnostics export is enabled.

## Console styles

`logging.consoleStyle`:

- `pretty`: human-friendly, colored, with timestamps.
- `compact`: tighter output (best for long sessions).
- `json`: JSON per line (for log processors).

## Redaction

OpenClaw can redact sensitive tokens before they hit console output, file logs, OTLP log records, persisted session transcript text, or Control UI tool event payloads (tool start args, partial/final result payloads, derived exec output, and patch summaries):

- `logging.redactSensitive`: `off` | `tools` (default: `tools`)
- `logging.redactPatterns`: list of regex strings to override the default set. Custom patterns apply on top of the built-in defaults for Control UI tool payloads, so adding a pattern never weakens redaction of values already caught by the defaults.

File logs and session transcripts stay JSONL, but matching secret values are masked before the line or message is written to disk. Redaction is best-effort: it applies to text-bearing message content and log strings, not every identifier or binary payload field.

The built-in defaults cover common API credentials and payment-credential field names such as card number, CVC/CVV, shared payment token, and payment credential when they appear as JSON fields, URL parameters, CLI flags, or assignments.

`logging.redactSensitive: "off"` only disables this general log/transcript policy. OpenClaw still redacts safety-boundary payloads that can be shown to UI clients, support bundles, diagnostics observers, approval prompts, or agent tools. Examples include Control UI tool-call events, `sessions_history` output, diagnostics support exports, provider error observations, exec approval command display, and Gateway WebSocket protocol logs. Custom `logging.redactPatterns` can still add project-specific patterns on those surfaces.

## Diagnostics and OpenTelemetry

Diagnostics are structured, machine-readable events for model runs and message-flow telemetry (webhooks, queueing, session state). They do **not** replace logs — they feed metrics, traces, and exporters. Events are emitted in-process whether or not you export them.

Two adjacent surfaces:

- **OpenTelemetry export** — send metrics, traces, and logs over OTLP/HTTP to any OpenTelemetry-compatible collector or backend (Grafana, Datadog, Honeycomb, New Relic, Tempo, etc.). Full configuration, signal catalog, metric/span names, env vars, and privacy model live on a dedicated page: [OpenTelemetry export](https://docs.openclaw.ai/gateway/opentelemetry).
- **Diagnostics flags** — targeted debug-log flags that route extra logs to `logging.file` without raising `logging.level`. Flags are case-insensitive and support wildcards (`telegram.*`, `*`). Configure under `diagnostics.flags` or via the `OPENCLAW_DIAGNOSTICS=...` env override. Full guide: [Diagnostics flags](https://docs.openclaw.ai/diagnostics/flags).

To enable diagnostics events for plugins or custom sinks without OTLP export:

```json5
{
  diagnostics: { enabled: true },
}
```

For OTLP export to a collector, see [OpenTelemetry export](https://docs.openclaw.ai/gateway/opentelemetry).

**Source**: OpenClaw documentation — `logging` (mirror `inbox/openclaw_docs/logging.md`), sections "Configuring logging" through "Diagnostics and OpenTelemetry"
**Last Updated**: 2026-06-22
**Status**: Active
