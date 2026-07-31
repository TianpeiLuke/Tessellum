---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - prometheus
keywords:
  - openclaw prometheus metrics
  - diagnostics-prometheus plugin
  - /api/diagnostics/prometheus endpoint
  - openclaw metric families labels
  - prometheus scrape config openclaw
  - promql recipes openclaw
  - prometheus series cardinality cap
  - prometheus vs opentelemetry export
topics:
  - OpenClaw
  - Gateway Observability
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/prometheus
access_control_group: ["general"]
---

# OpenClaw — Exposing and Scraping Gateway Prometheus Metrics

## Overview

This note is the operational procedure for exporting OpenClaw Gateway diagnostics as Prometheus text metrics through the official `diagnostics-prometheus` plugin, mirroring the `gateway/prometheus` source page. The plugin listens to trusted diagnostics plus core-emitted gateway stability events and renders a Prometheus text endpoint at `GET /api/diagnostics/prometheus`, with content type `text/plain; version=0.0.4; charset=utf-8` (the standard Prometheus exposition format). It covers the quick-start (install, enable, restart, authenticated scrape, Prometheus wiring), the full exported-metrics catalog, the bounded low-cardinality label policy, PromQL recipe snippets, when to choose Prometheus over OpenTelemetry, and troubleshooting. For traces, logs, OTLP push, and OpenTelemetry GenAI semantic attributes, the source defers to the separate OpenTelemetry export page.

## Quick Start

The source page gives a five-step `<Steps>` runbook for standing up the exporter.

**Step 1 — Install the plugin.** Install the official ClawHub plugin:

```bash
openclaw plugins install clawhub:@openclaw/diagnostics-prometheus
```

**Step 2 — Enable the plugin.** Either declare it in config (allowlist plus an enabled entry, and turn diagnostics on) or enable it via the CLI:

```json5
{
  plugins: {
    allow: ["diagnostics-prometheus"],
    entries: {
      "diagnostics-prometheus": { enabled: true },
    },
  },
  diagnostics: {
    enabled: true,
  },
}
```

The CLI equivalent for enabling is `openclaw plugins enable diagnostics-prometheus`. The source carries a `<Note>`: `diagnostics.enabled: true` is **required** — without it the plugin still registers the HTTP route but no diagnostic events flow into the exporter, so the response is empty.

**Step 3 — Restart the Gateway.** The HTTP route is registered at plugin startup, so reload after enabling.

**Step 4 — Scrape the protected route.** Send the same gateway auth your operator clients use:

```bash
curl -H "Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN" \
  http://127.0.0.1:18789/api/diagnostics/prometheus
```

**Step 5 — Wire Prometheus.** Point a scrape job at the protected metrics path, supplying the operator token via a credentials file:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: openclaw
    scrape_interval: 30s
    metrics_path: /api/diagnostics/prometheus
    authorization:
      credentials_file: /etc/prometheus/openclaw-gateway-token
    static_configs:
      - targets: ["openclaw-gateway:18789"]
```

The source wraps the route in a `<Warning>`: the route uses Gateway authentication (operator scope); do not expose it as a public unauthenticated `/metrics` endpoint, and scrape it through the same auth path used for other operator APIs.

## Metrics Exported

The exporter emits the following metric families. Each row is the metric name, its Prometheus type (counter / gauge / histogram), and its bounded label set (verbatim from source).

| Metric | Type | Labels |
| --- | --- | --- |
| `openclaw_run_completed_total` | counter | `channel`, `model`, `outcome`, `provider`, `trigger` |
| `openclaw_run_duration_seconds` | histogram | `channel`, `model`, `outcome`, `provider`, `trigger` |
| `openclaw_model_call_total` | counter | `api`, `error_category`, `model`, `outcome`, `provider`, `transport` |
| `openclaw_model_call_duration_seconds` | histogram | `api`, `error_category`, `model`, `outcome`, `provider`, `transport` |
| `openclaw_model_failover_total` | counter | `from_model`, `from_provider`, `lane`, `reason`, `suspended`, `to_model`, `to_provider` |
| `openclaw_model_tokens_total` | counter | `agent`, `channel`, `model`, `provider`, `token_type` |
| `openclaw_gen_ai_client_token_usage` | histogram | `model`, `provider`, `token_type` |
| `openclaw_model_cost_usd_total` | counter | `agent`, `channel`, `model`, `provider` |
| `openclaw_skill_used_total` | counter | `activation`, `agent`, `skill`, `source` |
| `openclaw_tool_execution_total` | counter | `error_category`, `outcome`, `params_kind`, `tool`, `tool_owner`, `tool_source` |
| `openclaw_tool_execution_duration_seconds` | histogram | `error_category`, `outcome`, `params_kind`, `tool`, `tool_owner`, `tool_source` |
| `openclaw_tool_execution_blocked_total` | counter | `denied_reason`, `params_kind`, `tool`, `tool_owner`, `tool_source` |
| `openclaw_harness_run_total` | counter | `channel`, `error_category`, `harness`, `model`, `outcome`, `phase`, `plugin`, `provider` |
| `openclaw_harness_run_duration_seconds` | histogram | `channel`, `error_category`, `harness`, `model`, `outcome`, `phase`, `plugin`, `provider` |
| `openclaw_webhook_received_total` | counter | `channel`, `webhook` |
| `openclaw_webhook_error_total` | counter | `channel`, `webhook` |
| `openclaw_webhook_duration_seconds` | histogram | `channel`, `webhook` |
| `openclaw_message_received_total` | counter | `channel`, `source` |
| `openclaw_message_dispatch_started_total` | counter | `channel`, `source` |
| `openclaw_message_dispatch_completed_total` | counter | `channel`, `outcome`, `reason`, `source` |
| `openclaw_message_dispatch_duration_seconds` | histogram | `channel`, `outcome`, `reason`, `source` |
| `openclaw_message_processed_total` | counter | `channel`, `outcome`, `reason` |
| `openclaw_message_processed_duration_seconds` | histogram | `channel`, `outcome`, `reason` |
| `openclaw_message_delivery_started_total` | counter | `channel`, `delivery_kind` |
| `openclaw_message_delivery_total` | counter | `channel`, `delivery_kind`, `error_category`, `outcome` |
| `openclaw_message_delivery_duration_seconds` | histogram | `channel`, `delivery_kind`, `error_category`, `outcome` |
| `openclaw_talk_event_total` | counter | `brain`, `event_type`, `mode`, `provider`, `transport` |
| `openclaw_talk_event_duration_seconds` | histogram | `brain`, `event_type`, `mode`, `provider`, `transport` |
| `openclaw_talk_audio_bytes` | histogram | `brain`, `event_type`, `mode`, `provider`, `transport` |
| `openclaw_queue_lane_size` | gauge | `lane` |
| `openclaw_queue_lane_wait_seconds` | histogram | `lane` |
| `openclaw_session_state_total` | counter | `reason`, `state` |
| `openclaw_session_queue_depth` | gauge | `state` |
| `openclaw_session_turn_created_total` | counter | `agent`, `channel`, `trigger` |
| `openclaw_session_stuck_total` | counter | `reason`, `state` |
| `openclaw_session_stuck_age_seconds` | histogram | `reason`, `state` |
| `openclaw_session_recovery_total` | counter | `action`, `active_work_kind`, `state`, `status` |
| `openclaw_session_recovery_age_seconds` | histogram | `action`, `active_work_kind`, `state`, `status` |
| `openclaw_liveness_warning_total` | counter | `reason` |
| `openclaw_liveness_sessions` | gauge | `state` |
| `openclaw_liveness_event_loop_delay_p99_seconds` | histogram | `reason` |
| `openclaw_liveness_event_loop_delay_max_seconds` | histogram | `reason` |
| `openclaw_liveness_event_loop_utilization_ratio` | histogram | `reason` |
| `openclaw_liveness_cpu_core_ratio` | histogram | `reason` |
| `openclaw_payload_large_total` | counter | `action`, `channel`, `plugin`, `reason`, `surface` |
| `openclaw_payload_large_bytes` | histogram | `action`, `channel`, `plugin`, `reason`, `surface` |
| `openclaw_memory_bytes` | gauge | `kind` |
| `openclaw_memory_rss_bytes` | histogram | none |
| `openclaw_memory_pressure_total` | counter | `level`, `reason` |
| `openclaw_telemetry_exporter_total` | counter | `exporter`, `reason`, `signal`, `status` |
| `openclaw_prometheus_series_dropped_total` | counter | none |

## Label Policy

The source documents the label policy as three accordion sections, all enforcing bounded, low-cardinality, redacted labels.

**Bounded, low-cardinality labels.** Prometheus labels stay bounded and low-cardinality. The exporter does not emit raw diagnostic identifiers such as `runId`, `sessionKey`, `sessionId`, `callId`, `toolCallId`, message IDs, chat IDs, or provider request IDs. Label values are redacted and must match OpenClaw's low-cardinality character policy; values that fail the policy are replaced with `unknown`, `other`, or `none`, depending on the metric. Labels that look like scoped agent session keys are also replaced with `unknown`.

**Series cap and overflow accounting.** The exporter caps retained time series in memory at **2048** series across counters, gauges, and histograms combined. New series beyond that cap are dropped, and `openclaw_prometheus_series_dropped_total` increments by one each time. Watch this counter as a hard signal that an attribute upstream is leaking high-cardinality values; the exporter never lifts the cap automatically, so if it climbs, fix the source rather than disabling the cap.

**What never appears in Prometheus output.** The source enumerates the categories that are never exported: prompt text, response text, tool inputs, tool outputs, system prompts; Talk transcripts, audio payloads, call ids, room ids, handoff tokens, turn ids, and raw session ids; raw provider request IDs (only bounded hashes, where applicable, on spans — never on metrics); session keys and session IDs; and hostnames, file paths, secret values.

## PromQL Recipes

The source page supplies a set of ready-made PromQL queries against the scraped series (verbatim):

```promql
# Tokens per minute, split by provider
sum by (provider) (rate(openclaw_model_tokens_total[1m]))

# Spend (USD) over the last hour, by model
sum by (model) (increase(openclaw_model_cost_usd_total[1h]))

# 95th percentile model run duration
histogram_quantile(
  0.95,
  sum by (le, provider, model)
    (rate(openclaw_run_duration_seconds_bucket[5m]))
)

# Queue wait time SLO (95p under 2s)
histogram_quantile(
  0.95,
  sum by (le, lane) (rate(openclaw_queue_lane_wait_seconds_bucket[5m]))
) < 2

# Skill usage, split by bounded source
sum by (skill, source) (increase(openclaw_skill_used_total[24h]))

# Dropped Prometheus series (cardinality alarm)
increase(openclaw_prometheus_series_dropped_total[15m]) > 0
```

The source adds a `<Tip>`: prefer `gen_ai_client_token_usage` for cross-provider dashboards because it follows the OpenTelemetry GenAI semantic conventions and is consistent with metrics from non-OpenClaw GenAI services.

## Choosing Between Prometheus and OpenTelemetry Export

OpenClaw supports both surfaces independently — you can run either, both, or neither. The `diagnostics-prometheus` surface is a **Pull** model: Prometheus scrapes `/api/diagnostics/prometheus`, no external collector is required, it is authenticated through normal Gateway auth, its surface is metrics only (no traces or logs), and it is best for stacks already standardized on Prometheus + Grafana. The `diagnostics-otel` surface is a **Push** model: OpenClaw sends OTLP/HTTP to a collector or OTLP-compatible backend, its surface includes metrics, traces, and logs, and it bridges to Prometheus through an OpenTelemetry Collector (`prometheus` or `prometheusremotewrite` exporter) when both are needed. The source defers the full OTel catalog to the OpenTelemetry export page.

## Troubleshooting

The source lists four troubleshooting accordions:

- **Empty response body** — check `diagnostics.enabled: true` in config; confirm the plugin is enabled and loaded with `openclaw plugins list --enabled`; and generate some traffic, since counters and histograms only emit lines after at least one event.
- **401 / unauthorized** — the endpoint requires the Gateway operator scope (`auth: "gateway"` with `gatewayRuntimeScopeSurface: "trusted-operator"`); use the same token or password Prometheus uses for any other Gateway operator route. There is no public unauthenticated mode.
- **`openclaw_prometheus_series_dropped_total` is climbing** — a new attribute is exceeding the **2048**-series cap; inspect recent metrics for an unexpectedly high-cardinality label and fix it at the source. The exporter intentionally drops new series instead of silently rewriting labels.
- **Prometheus shows stale series after a restart** — the plugin keeps state in memory only, so after a Gateway restart counters reset to zero and gauges restart at their next reported value; use PromQL `rate()` and `increase()` to handle resets cleanly.

**Source**: OpenClaw documentation — `gateway/prometheus` (mirror `inbox/openclaw_docs/gateway/prometheus.md`)
**Last Updated**: 2026-06-22
**Status**: Active
