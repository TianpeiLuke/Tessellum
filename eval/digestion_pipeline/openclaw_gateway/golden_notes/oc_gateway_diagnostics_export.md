---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - diagnostics
keywords:
  - openclaw gateway diagnostics export
  - openclaw gateway diagnostics export json
  - diagnostics chat command
  - diagnostics privacy redaction model
  - stability recorder bundle
  - diagnostic liveness warning
  - memorypressuresnapshot
  - disable diagnostics enabled false
  - codex harness feedback upload
topics:
  - OpenClaw
  - Gateway Diagnostics
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/gateway/diagnostics
access_control_group: ["general"]
---

# OpenClaw — Gateway Diagnostics Export

## Overview

This note is a procedure for creating shareable OpenClaw **Gateway diagnostics bundles** for bug reports and support requests, mirroring the `gateway/diagnostics` source page. OpenClaw can create a local diagnostics zip that combines sanitized Gateway status, health, logs, config shape, and recent payload-free stability events. It covers the `openclaw gateway diagnostics export` command and its options, the `/diagnostics` chat command and its single-exec-approval flow (including the Codex-harness feedback-upload path), the contents of the export zip, the redaction/privacy model that makes a bundle shareable, the always-on stability recorder and its `diagnostic.liveness.warning` / `diagnostic.phase.completed` events, and how to disable diagnostics or enable the critical-memory-pressure snapshot. Per the source, treat diagnostics bundles like secrets until reviewed: they are designed to omit or redact payloads and credentials, but they still summarize local Gateway logs and host-level runtime state.

## Quick start

Create a local diagnostics zip with the export command; it prints the written zip path:

```bash
openclaw gateway diagnostics export
```

To choose a path, pass `--output`; for automation, pass `--json` to print machine-readable export metadata:

```bash
openclaw gateway diagnostics export --output openclaw-diagnostics.zip
openclaw gateway diagnostics export --json
```

## Chat command

Owners can use `/diagnostics [note]` in chat to request a local Gateway export. Use this when the bug happened in a real conversation and you want one copy-pasteable report for support. The flow is:

1. Send `/diagnostics` in the conversation where you noticed the problem. Add a short note if it helps, for example `/diagnostics bad tool choice`.
2. OpenClaw sends the diagnostics preamble and asks for one explicit exec approval. The approval runs `openclaw gateway diagnostics export --json`. **Do not approve diagnostics through an allow-all rule.**
3. After approval, OpenClaw replies with a pasteable report containing the local bundle path, manifest summary, privacy notes, and relevant session ids.

In group chats, an owner can still run `/diagnostics`, but OpenClaw does not post the diagnostic details back into the shared chat. It sends the preamble, approval prompts, Gateway export result, and Codex session/thread breakdown to the owner through the private approval route. The group only gets a short notice that the diagnostics flow was sent privately. If OpenClaw cannot find a private owner route, the command fails closed and asks the owner to run it from a DM.

When the active OpenClaw session is using the native OpenAI Codex harness, the same exec approval also covers an OpenAI feedback upload for the Codex runtime threads OpenClaw knows about. That upload is separate from the local Gateway zip and appears only for Codex harness sessions. Before approval, the prompt explains that approving diagnostics will also send Codex feedback, but it does not list Codex session or thread ids. After approval, the chat reply lists the channels, OpenClaw session ids, Codex thread ids, and local resume commands for the threads that were sent to OpenAI servers. If you deny or ignore the approval, OpenClaw does not run the export, does not send Codex feedback, and does not print the Codex ids. The common Codex debugging loop is therefore short: notice the bad behavior in a channel, run `/diagnostics`, approve once, share the report with support, then run the printed `codex resume <thread-id>` command locally if you want to inspect the native Codex thread yourself.

## What the export contains

The zip includes a human-readable `summary.md` overview for support; a machine-readable `diagnostics.json` summary of config, logs, status, health, and stability data; a `manifest.json` of export metadata and the file list; the sanitized config shape and non-secret config details; sanitized log summaries and recent redacted log lines; best-effort Gateway status and health snapshots; and `stability/latest.json`, the newest persisted stability bundle, when available. The export is useful even when the Gateway is unhealthy: if the Gateway cannot answer status or health requests, the local logs, config shape, and latest stability bundle are still collected when available.

## Privacy model

Diagnostics are designed to be shareable. The export **keeps** operational data that helps debugging: subsystem names, plugin ids, provider ids, channel ids, and configured modes; status codes, durations, byte counts, queue state, and memory readings; sanitized log metadata and redacted operational messages; and config shape and non-secret feature settings. The export **omits or redacts**: chat text, prompts, instructions, webhook bodies, and tool outputs; credentials, API keys, tokens, cookies, and secret values; raw request or response bodies; and account ids, message ids, raw session ids, hostnames, and local usernames. When a log message looks like user, chat, prompt, or tool payload text, the export keeps only that a message was omitted and the byte count.

## Stability recorder

The Gateway records a bounded, payload-free stability stream by default when diagnostics are enabled; it is for operational facts, not content. The same diagnostic heartbeat records liveness samples when the Gateway keeps running but the Node.js event loop or CPU looks saturated. These `diagnostic.liveness.warning` events include event-loop delay, event-loop utilization, CPU-core ratio, active/waiting/queued session counts, the current startup/runtime phase when known, recent phase spans, and bounded active/queued work labels. Idle samples stay in telemetry at `info` level. Liveness samples become Gateway warnings only when work is waiting or queued, or when active work overlaps with sustained event-loop delay. Transient max-delay spikes during otherwise healthy background work stay in debug logs and do not restart the Gateway by themselves. Startup phases also emit `diagnostic.phase.completed` events with wall-clock and CPU timing. Stalled embedded-run diagnostics mark `terminalProgressStale=true` when the last bridge progress looked terminal, such as a raw response item or response completion event, but the Gateway still considers the embedded run active.

Inspect the live recorder, and the newest persisted stability bundle after a fatal exit, shutdown timeout, or restart startup failure:

```bash
openclaw gateway stability
openclaw gateway stability --type payload.large
openclaw gateway stability --json
openclaw gateway stability --bundle latest
openclaw gateway stability --bundle latest --export
```

`openclaw gateway stability --bundle latest --export` creates a diagnostics zip from the newest persisted bundle. Persisted bundles live under `~/.openclaw/logs/stability/` when events exist.

## Useful options

```bash
openclaw gateway diagnostics export \
  --output openclaw-diagnostics.zip \
  --log-lines 5000 \
  --log-bytes 1000000
```

- `--output <path>`: write to a specific zip path.
- `--log-lines <count>`: maximum sanitized log lines to include.
- `--log-bytes <bytes>`: maximum log bytes to inspect.
- `--url <url>`: Gateway WebSocket URL for status and health snapshots.
- `--token <token>`: Gateway token for status and health snapshots.
- `--password <password>`: Gateway password for status and health snapshots.
- `--timeout <ms>`: status and health snapshot timeout.
- `--no-stability-bundle`: skip persisted stability bundle lookup.
- `--json`: print machine-readable export metadata.

## Disable diagnostics

Diagnostics are enabled by default. To disable the stability recorder and diagnostic event collection, set `diagnostics.enabled` to `false`:

```json5
{
  diagnostics: {
    enabled: false,
  },
}
```

Disabling diagnostics reduces bug-report detail; it does not affect normal Gateway logging. Critical memory pressure snapshots are off by default. To keep diagnostics events and also capture the pre-OOM stability snapshot, set `diagnostics.memoryPressureSnapshot` to `true`:

```json5
{
  diagnostics: {
    memoryPressureSnapshot: true,
  },
}
```

Use this only on hosts that can tolerate the extra file-system scan and snapshot write during critical memory pressure. Normal memory pressure events still record RSS, heap, threshold, and growth facts when the snapshot is off.

## Related Notes

**Terms**

- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — the gateway product; relevance: the Gateway being diagnosed/exported.
- **[Health Check](../../term_dictionary/term_health_check.md)** — liveness/health probe; relevance: status/health snapshots included in the bundle.
- **[Access Control](../../term_dictionary/term_access_control.md)** — authorization policy; relevance: the exec-approval gate on `/diagnostics` (never allow-all).
- **[OAuth Token](../../term_dictionary/term_oauth_token.md)** — credential token; relevance: `--token` + credential/token redaction in the privacy model.
- **[PII](../../term_dictionary/term_pii.md)** — personally identifiable info; relevance: the redaction model strips usernames/hostnames/account ids.
- **[Observability of Agent Systems](../../term_dictionary/term_observability_agent_systems.md)** — agent monitoring; relevance: the stability recorder + liveness/phase telemetry.
- **[Agent Trajectory](../../term_dictionary/term_agent_trajectory.md)** — agent run trace; relevance: Codex-harness session/thread breakdown in the report.
- **[Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md)** — self-driving coding agents; relevance: the Codex-harness feedback-upload path.

**Docs**

- **[Claude Code — OTel Analysis and Privacy](../claude_code/cc_otel_analysis_and_privacy.md)** — telemetry privacy/redaction; relevance: direct analog to the diagnostics privacy/redaction model.
- **[Claude Code — Data Usage and Telemetry](../claude_code/cc_data_usage_and_telemetry.md)** — what's collected/redacted; relevance: the export's keep/omit/redact contract.
- **[Claude Code — Monitoring (OpenTelemetry Setup)](../claude_code/cc_monitoring_opentelemetry_setup.md)** — operational metrics; relevance: the stability recorder's operational-facts stream.
- **[Claude Code — OTel Configuration Variables](../claude_code/cc_otel_configuration_variables.md)** — telemetry config; relevance: the `diagnostics.*` enable/snapshot config knobs.
- **[Hermes — CLI Commands (Ops/Maintenance/Auth)](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md)** — ops/diagnostics CLI; relevance: analog to `openclaw gateway diagnostics export`.
- **[Band — Agent API Context Activity](../band/band_agent_api_context_activity.md)** — activity/observability surface; relevance: the operational activity captured in the bundle.
- **[oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md)** — the `diagnostics.*` config block (planned, this series); relevance: where enabled/memoryPressureSnapshot are configured.
- **[oc_gateway_doctor](oc_gateway_doctor.md)** — companion health/repair tool (planned, this series); relevance: doctor + diagnostics are the paired support tools.
- **[oc_gateway_config_reference_platform](oc_gateway_config_reference_platform.md)** — logging/gateway config (planned, this series); relevance: the logging surface diagnostics summarizes.
- **[oc_gateway_configuration_overview](oc_gateway_configuration_overview.md)** — diagnostic-commands-when-invalid path (planned, this series); relevance: diagnostics is one of the few commands that work when config is invalid.

**Repos**

- **[repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md)** — gateway runtime; relevance: the diagnostics export + stability recorder.
- **[repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md)** — security layer; relevance: the redaction/privacy model for credentials.
- **[repo_openclaw](../../../areas/code_repos/repo_openclaw.md)** — monorepo; relevance: the logs/state layout (`~/.openclaw/logs/stability/`).

**Snippets**

- **[snippet_hermes_agent_gw_memory_monitor](../../code_snippets/snippet_hermes_agent_gw_memory_monitor.md)** — memory-pressure monitor; relevance: the memoryPressureSnapshot + memory-readings the bundle records.
- **[snippet_hermes_agent_gw_status_snapshot](../../code_snippets/snippet_hermes_agent_gw_status_snapshot.md)** — status snapshot; relevance: the sanitized Gateway status in the export.
- **[snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md)** — health status; relevance: the health snapshot included in the bundle.
- **[snippet_hermes_agent_gw_shutdown_forensics](../../code_snippets/snippet_hermes_agent_gw_shutdown_forensics.md)** — shutdown forensics; relevance: the persisted stability bundle after a fatal exit/restart.
- **[snippet_hermes_agent_core_auxiliary_diagnostics](../../code_snippets/snippet_hermes_agent_core_auxiliary_diagnostics.md)** — diagnostics assembly; relevance: how a diagnostics bundle is composed.
- **[snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md)** — redaction patterns; relevance: the credential/payload redaction the privacy model applies.
- **[snippet_hermes_agent_trajectory_redact_export](../../code_snippets/snippet_hermes_agent_trajectory_redact_export.md)** — redacted trajectory export; relevance: the Codex session/thread breakdown with redaction.
- **[snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md)** — shutdown handling; relevance: the shutdown-timeout/restart events the stability recorder captures.
- **[snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md)** — exec runtime audit; relevance: the exec-approval gate on the `/diagnostics` command.
- **[snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md)** — gateway RPC methods; relevance: where `gateway diagnostics`/`gateway stability` methods register.

## References

- [OpenClaw Docs — Diagnostics export](https://docs.openclaw.ai/gateway/diagnostics)
- [OpenClaw Docs — Health checks](https://docs.openclaw.ai/gateway/health)
- [OpenClaw Docs — Gateway CLI (gateway diagnostics export)](https://docs.openclaw.ai/cli/gateway#gateway-diagnostics-export)
- [OpenClaw Docs — Gateway protocol (system and identity)](https://docs.openclaw.ai/gateway/protocol#system-and-identity)
- [OpenClaw Docs — Logging](https://docs.openclaw.ai/logging)
- [OpenClaw Docs — OpenTelemetry export](https://docs.openclaw.ai/gateway/opentelemetry)
- [OpenClaw Docs — Codex harness (inspect Codex threads locally)](https://docs.openclaw.ai/plugins/codex-harness#inspect-codex-threads-locally)

**Source**: OpenClaw documentation — `gateway/diagnostics` (mirror `inbox/openclaw_docs/gateway/diagnostics.md`)
**Last Updated**: 2026-06-22
**Status**: Active
