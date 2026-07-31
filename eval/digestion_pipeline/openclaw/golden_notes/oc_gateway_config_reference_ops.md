---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - configuration
keywords:
  - openclaw config reference secrets
  - secretref credential surface
  - secrets providers config
  - auth storage cooldowns
  - auth.cooldowns backoff
  - logging redact patterns config
  - diagnostics otel export config
  - stuck session classifier thresholds
topics:
  - OpenClaw
  - Gateway Configuration Reference
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/configuration-reference
access_control_group: ["general"]
---

# OpenClaw — Gateway Config Reference: Secrets, Auth Storage, Logging & Diagnostics

## Overview

This note is the field-level reference for the **security/observability surfaces** of the OpenClaw Gateway config in `~/.openclaw/openclaw.json` (format **JSON5** — comments and trailing commas allowed; all fields optional with safe defaults). It models the `secrets.*` (SecretRef + providers), `auth.*` (storage + `cooldowns`), `logging.*`, and `diagnostics.*` (incl. the `otel` export pipeline) sections of the `gateway/configuration-reference` source page. The jobs/operations surfaces of the same page (`update`, `acp`, `cli`, `wizard`, identity, legacy `bridge`, `cron.*`, media template variables, `$include`) are in the sibling [oc_gateway_config_reference_ops_jobs](oc_gateway_config_reference_ops_jobs.md); the runtime (channels/agents/tools/models/MCP/skills/plugins) and platform (browser/UI/gateway/hooks/canvas/discovery/env) clusters live in the other sibling reference notes.

## Secrets

Secret refs are additive: plaintext values still work. A `SecretRef` uses one object shape with `source`, `provider`, and `id`:

```json5
{ source: "env" | "file" | "exec", provider: "default", id: "..." }
```

`SecretRef` validation: `provider` matches `^[a-z][a-z0-9_-]{0,63}$`; `source: "env"` `id` matches `^[A-Z][A-Z0-9_]{0,127}$`; `source: "file"` `id` is an absolute JSON pointer (e.g. `"/providers/openai/apiKey"`); `source: "exec"` `id` matches `^[A-Za-z0-9][A-Za-z0-9._:/#-]{0,255}$` (supports AWS-style `secret#json_key` selectors) and must not contain `.` or `..` slash-delimited path segments (e.g. `a/../b` is rejected).

The canonical credential surface matrix lives at [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface): `secrets apply` targets supported `openclaw.json` credential paths, and `auth-profiles.json` refs are covered by runtime resolution and audit.

### Secret providers config

The `secrets.providers` block declares the resolution backends (`env`, `file`, `exec`) and the `secrets.defaults` block names the default provider per source kind:

```json5
{
  secrets: {
    providers: {
      default: { source: "env" }, // optional explicit env provider
      filemain: {
        source: "file",
        path: "~/.openclaw/secrets.json",
        mode: "json",
        timeoutMs: 5000,
      },
      vault: {
        source: "exec",
        command: "/usr/local/bin/openclaw-vault-resolver",
        passEnv: ["PATH", "VAULT_ADDR"],
      },
    },
    defaults: {
      env: "default",
      file: "filemain",
      exec: "vault",
    },
  },
}
```

Provider notes from source: the `file` provider supports `mode: "json"` and `mode: "singleValue"` (`id` must be `"value"` in singleValue mode); `file`/`exec` paths fail closed when Windows ACL verification is unavailable, with `allowInsecurePath: true` only for trusted unverifiable paths. The `exec` provider requires an absolute `command` path and uses protocol payloads on stdin/stdout; symlink command paths are rejected unless `allowSymlinkCommand: true` (which validates the resolved target), and any configured `trustedDirs` check applies to that resolved target; its child environment is minimal, so required variables are passed via `passEnv`. Secret refs resolve at activation time into a read-only in-memory snapshot, and active-surface filtering fails startup/reload on unresolved refs for enabled surfaces while skipping inactive surfaces with diagnostics.

## Auth storage

Per-agent auth profiles live under `auth.profiles` (keyed `provider:label`), with `auth.order` giving the per-provider resolution order, stored at `<agentDir>/auth-profiles.json` and supporting value-level refs (`keyRef` for `api_key`, `tokenRef` for `token`) in static credential modes. Legacy flat maps such as `{ "provider": { "apiKey": "..." } }` are not a runtime format; `openclaw doctor --fix` rewrites them to canonical `provider:default` API-key profiles with a `.legacy-flat.*.bak` backup. OAuth-mode profiles (`auth.profiles.<id>.mode = "oauth"`) do not support SecretRef-backed credentials. Static runtime credentials come from in-memory resolved snapshots; legacy static `auth.json` entries are scrubbed when discovered, and legacy OAuth imports come from `~/.openclaw/credentials/oauth.json`. Secrets runtime behavior and `audit`/`configure`/`apply` tooling is at [Secrets Management](https://docs.openclaw.ai/gateway/secrets).

### `auth.cooldowns`

The `auth.cooldowns` block governs provider/auth-profile backoff on billing, auth-permanent, overloaded, and rate-limit failures. Field semantics from source:

- `billingBackoffHours`: base backoff (hours) on true billing/insufficient-credit errors (default: `5`). Explicit billing text can land here even on `401`/`403`, but provider-specific matchers stay scoped to their provider (e.g. OpenRouter `Key limit exceeded`); retryable HTTP `402` usage-window or org/workspace spend-limit messages go to the `rate_limit` path instead.
- `billingBackoffHoursByProvider`: optional per-provider overrides for billing backoff hours.
- `billingMaxHours`: cap (hours) for billing backoff exponential growth (default: `24`).
- `authPermanentBackoffMinutes`: base backoff (minutes) for high-confidence `auth_permanent` failures (default: `10`).
- `authPermanentMaxMinutes`: cap (minutes) for `auth_permanent` backoff growth (default: `60`).
- `failureWindowHours`: rolling window (hours) for backoff counters (default: `24`).
- `overloadedProfileRotations`: max same-provider auth-profile rotations for overloaded errors before model fallback (default: `1`); provider-busy shapes such as `ModelNotReadyException` land here.
- `overloadedBackoffMs`: fixed delay before retrying an overloaded provider/profile rotation (default: `0`).
- `rateLimitedProfileRotations`: max same-provider rotations for rate-limit errors before model fallback (default: `1`); the rate-limit bucket includes provider text such as `Too many concurrent requests`, `ThrottlingException`, `concurrency limit reached`, `workers_ai ... quota limit exceeded`, and `resource exhausted`.

## Logging

The `logging` block controls level, file path, console style, and redaction. Default log file is `/tmp/openclaw/openclaw-YYYY-MM-DD.log`; set `logging.file` for a stable path; `consoleLevel` bumps to `debug` when `--verbose`. `maxFileBytes` is the max active log file size in bytes before rotation (positive integer; default: `104857600` = 100 MB), and up to five numbered archives are kept beside the active file. `redactSensitive` / `redactPatterns` are best-effort masking for console output, file logs, OTLP log records, and persisted session transcript text — `redactSensitive: "off"` only disables this general log/transcript policy, while UI/tool/diagnostic safety surfaces still redact secrets before emission.

```json5
{
  logging: {
    level: "info",
    file: "/tmp/openclaw/openclaw.log",
    consoleLevel: "info",
    consoleStyle: "pretty", // pretty | compact | json
    redactSensitive: "tools", // off | tools
    redactPatterns: ["\\bTOKEN\\b\\s*[=:]\\s*([\"']?)([^\\s\"']+)\\1"],
  },
}
```

## Diagnostics

The `diagnostics` block is the instrumentation/observability surface: a master `enabled` toggle (default: `true`), `flags` (array of flag strings for targeted log output, supporting wildcards like `"telegram.*"` or `"*"`), stuck-session classifier thresholds, the memory-pressure snapshot, the OpenTelemetry (`otel`) export pipeline, and the cache trace. Threshold semantics: `stuckSessionWarnMs` is the no-progress age (ms) for classifying long-running sessions as `session.long_running`, `session.stalled`, or `session.stuck` (reply/tool/status/block/ACP progress resets the timer; repeated `session.stuck` diagnostics back off while unchanged); `stuckSessionAbortMs` is the no-progress age (ms) before eligible stalled work may be abort-drained for recovery, defaulting when unset to the safer extended embedded-run window of at least 5 minutes and 3x `stuckSessionWarnMs`; `memoryPressureSnapshot` captures a redacted pre-OOM stability snapshot when memory pressure reaches `critical` (default: `false`).

OTel (`diagnostics.otel`) field semantics from source:

- `otel.enabled`: enables the OpenTelemetry export pipeline (default: `false`; full config/signal catalog/privacy model at [OpenTelemetry export](https://docs.openclaw.ai/gateway/opentelemetry)).
- `otel.endpoint`: collector URL; `otel.tracesEndpoint` / `otel.metricsEndpoint` / `otel.logsEndpoint` are optional signal-specific OTLP endpoints overriding `otel.endpoint` for that signal only.
- `otel.protocol`: `"http/protobuf"` (default) or `"grpc"`; `otel.headers`: extra HTTP/gRPC metadata headers; `otel.serviceName`: resource-attribute service name.
- `otel.traces` / `otel.metrics` / `otel.logs`: enable each signal; `otel.logsExporter`: `"otlp"` (default), `"stdout"`, or `"both"`; `otel.sampleRate`: trace sampling `0`-`1`; `otel.flushIntervalMs`: periodic flush interval.
- `otel.captureContent`: opt-in raw content capture (default off; boolean `true` captures non-system message/tool content, or the object form enables `inputMessages`, `outputMessages`, `toolInputs`, `toolOutputs`, `systemPrompt`, `toolDefinitions` explicitly).

Three OTel environment toggles exist: `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` (latest experimental GenAI inference span shape — `{gen_ai.operation.name} {gen_ai.request.model}` span names, `CLIENT` span kind, `gen_ai.provider.name` instead of legacy `gen_ai.system`; by default spans keep `openclaw.model.call` and `gen_ai.system`); `OPENCLAW_OTEL_PRELOADED=1` (host already has a global OpenTelemetry SDK registered — OpenClaw skips plugin-owned SDK startup/shutdown but keeps diagnostic listeners active); and `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` / `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` / `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` (signal-specific endpoints used when the matching config key is unset). The `cacheTrace` sub-block: `enabled` logs cache trace snapshots for embedded runs (default: `false`); `filePath` is the JSONL output path (default: `$OPENCLAW_STATE_DIR/logs/cache-trace.jsonl`); `includeMessages` / `includePrompt` / `includeSystem` control inclusion (all default: `true`).

**Source**: OpenClaw documentation — `gateway/configuration-reference` (mirror `inbox/openclaw_docs/gateway/configuration-reference.md`)
**Last Updated**: 2026-06-22
**Status**: Active
