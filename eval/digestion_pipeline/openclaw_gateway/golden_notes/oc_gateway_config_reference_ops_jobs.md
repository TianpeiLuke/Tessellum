---
tags:
  - resource
  - documentation
  - openclaw
  - gateway
  - configuration
keywords:
  - openclaw config reference jobs
  - cron retry failurealert failuredestination
  - acp runtime config block
  - update channel auto-update
  - media model template variables
  - config includes $include
  - cli banner wizard metadata
  - bridge legacy removed
topics:
  - OpenClaw
  - Gateway Configuration Reference
language: markdown
date of note: 2026-06-23
status: active
building_block: model
source_url: https://docs.openclaw.ai/gateway/configuration-reference
access_control_group: ["general"]
---

# OpenClaw — Gateway Config Reference: Update, ACP, CLI, Cron, Media & Includes

## Overview

This note is the field-level reference for the **jobs/operations surfaces** of the OpenClaw Gateway config in `~/.openclaw/openclaw.json` (JSON5; all fields optional with safe defaults). It models the `update.*`, `acp.*`, `cli.*`, `wizard.*`, identity, the removed legacy `bridge.*`, the `cron.*` block (`cron.retry` / `cron.failureAlert` / `cron.failureDestination`), the media model template variables, and config includes (`$include`) — split from the secrets/auth/logging/diagnostics surfaces in the sibling [oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md). The runtime and platform clusters of the same `gateway/configuration-reference` source page live in the other sibling reference notes.

## Update

The `update` block controls release-channel auto-update behavior. `channel` is the release channel for npm/git installs — `"stable"`, `"beta"`, or `"dev"`; `checkOnStart` checks for npm updates when the gateway starts (default: `true`); `auto.enabled` enables background auto-update for package installs (default: `false`); `auto.stableDelayHours` is the minimum delay in hours before stable-channel auto-apply (default: `6`; max: `168`); `auto.stableJitterHours` is the extra stable-channel rollout spread window in hours (default: `12`; max: `168`); and `auto.betaCheckIntervalHours` is how often beta-channel checks run in hours (default: `1`; max: `24`).

## ACP

The `acp` block configures the Agent Client Protocol runtime — feature gating, dispatch, backend selection, agent allowlist, concurrency, stream projection, and runtime TTL:

- `enabled`: global ACP feature gate (default: `true`; `false` hides ACP dispatch and spawn affordances).
- `dispatch.enabled`: independent gate for ACP session turn dispatch (default: `true`; `false` keeps ACP commands available while blocking execution).
- `backend`: default ACP runtime backend id (must match a registered ACP runtime plugin — install it first, and if `plugins.allow` is set include the backend plugin id such as `acpx`, or the backend will not load).
- `defaultAgent`: fallback ACP target agent id when spawns omit a target; `allowedAgents`: allowlist of agent ids for ACP sessions (empty = no extra restriction); `maxConcurrentSessions`: max concurrently active ACP sessions.
- `stream.coalesceIdleMs` (idle flush window in ms), `stream.maxChunkChars` (max chunk before splitting streamed block projection), `stream.repeatSuppression` (suppress repeated status/tool lines per turn, default: `true`), `stream.deliveryMode` (`"live"` streams incrementally, `"final_only"` buffers until turn-terminal events), `stream.hiddenBoundarySeparator` (separator before visible text after hidden tool events, default: `"paragraph"`), `stream.maxOutputChars`, `stream.maxSessionUpdateChars`, `stream.tagVisibility` (tag-name → boolean visibility overrides).
- `runtime.ttlMinutes`: idle TTL in minutes for ACP session workers before eligible cleanup; `runtime.installCommand`: optional install command for bootstrapping an ACP runtime environment.

## CLI

The `cli.banner.taglineMode` controls banner tagline style: `"random"` (default — rotating funny/seasonal taglines), `"default"` (fixed neutral tagline, `All your chats, one OpenClaw.`), or `"off"` (no tagline text — banner title/version still shown). To hide the entire banner (not just taglines), set env `OPENCLAW_HIDE_BANNER=1`.

## Wizard

The `wizard` block is metadata written by CLI guided setup flows (`onboard`, `configure`, `doctor`) and records `lastRunAt`, `lastRunVersion`, `lastRunCommit`, `lastRunCommand`, and `lastRunMode`.

## Identity

Identity is not a standalone block here: the source page points to `agents.list` identity fields under [Agent defaults](https://docs.openclaw.ai/gateway/config-agents#agent-defaults).

## Bridge (legacy, removed)

Current builds no longer include the TCP bridge — nodes connect over the Gateway WebSocket. `bridge.*` keys are no longer part of the config schema (validation fails until removed; `openclaw doctor --fix` can strip unknown keys). The historical legacy bridge config used `bridge.enabled`, `bridge.port` (`18790`), `bridge.bind` (`tailnet`), and `bridge.tls` (`enabled` / `autoGenerate`).

## Cron

The top-level `cron` block configures scheduled-job execution and run logging:

```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 8, // default; cron dispatch + isolated cron agent-turn execution
    webhook: "https://example.invalid/legacy", // deprecated fallback for stored notify:true jobs
    webhookToken: "replace-with-dedicated-token", // optional bearer token for outbound webhook auth
    sessionRetention: "24h", // duration string or false
    runLog: {
      maxBytes: "2mb", // default 2_000_000 bytes
      keepLines: 2000, // default 2000
    },
  },
}
```

Field semantics from source: `maxConcurrentRuns` (default `8`) governs cron dispatch + isolated cron agent-turn execution; `sessionRetention` is how long to keep completed isolated cron run sessions before pruning from `sessions.json` (also cleans archived deleted cron transcripts; default: `24h`; `false` disables); `runLog.maxBytes` is accepted for compatibility with older file-backed cron run logs (default: `2_000_000` bytes); `runLog.keepLines` is the newest SQLite run-history rows retained per job (default: `2000`); `webhookToken` is the bearer token for cron webhook POST delivery (`delivery.mode = "webhook"`; omitted → no auth header); and `webhook` is the deprecated legacy fallback URL used by `openclaw doctor --fix` to migrate stored jobs still carrying `notify: true`. Runtime delivery uses per-job `delivery.mode="webhook"` plus `delivery.to`, or `delivery.completionDestination` to preserve announce delivery.

### `cron.retry`

The `cron.retry` block governs transient-error retry: `maxAttempts` is the max retries on transient errors (default: `3`; range: `0`-`10`); `backoffMs` is the array of backoff delays in ms per attempt (default: `[30000, 60000, 300000]`; 1-10 entries); and `retryOn` is the error types that trigger retries — `"rate_limit"`, `"overloaded"`, `"network"`, `"timeout"`, `"server_error"` (omit to retry all transient types). One-shot jobs stay enabled until retries exhaust, then disable while keeping the final error state; recurring jobs apply the same policy to re-run after backoff before their next slot, and permanent errors or exhausted retries fall back to the normal recurring schedule with error backoff.

### `cron.failureAlert`

The `cron.failureAlert` block configures failure alerting: `enabled` (default: `false`); `after` is the consecutive failures before an alert fires (positive integer, min: `1`); `cooldownMs` is the min ms between repeated alerts for the same job (non-negative integer); `includeSkipped` counts consecutive skipped runs toward the threshold (default: `false` — skipped runs are tracked separately and do not affect execution-error backoff); `mode` is the delivery mode (`"announce"` via channel message, `"webhook"` posts to the configured webhook); `accountId` optionally scopes alert delivery to an account/channel id.

### `cron.failureDestination`

The `cron.failureDestination` block is the global default destination for cron failure notifications: `mode` is `"announce"` or `"webhook"` (defaults to `"announce"` when enough target data exists); `channel` overrides the announce channel (`"last"` reuses the last known delivery channel); `to` is the explicit announce target or webhook URL (required for webhook mode); `accountId` is an optional account override. Per-job `delivery.failureDestination` overrides this default; when neither is set, jobs that already deliver via `announce` fall back to that primary announce target on failure. `delivery.failureDestination` is only supported for `sessionTarget="isolated"` jobs unless the job's primary `delivery.mode` is `"webhook"`. Isolated cron executions are tracked as background tasks (see [Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs) and [tasks](https://docs.openclaw.ai/automation/tasks)).

## Media model template variables

Template placeholders are expanded in `tools.media.models[].args`. The full set from source:

| Variable           | Description                                       |
| ------------------ | ------------------------------------------------- |
| `{{Body}}`         | Full inbound message body                         |
| `{{RawBody}}`      | Raw body (no history/sender wrappers)             |
| `{{BodyStripped}}` | Body with group mentions stripped                 |
| `{{From}}`         | Sender identifier                                 |
| `{{To}}`           | Destination identifier                            |
| `{{MessageSid}}`   | Channel message id                                |
| `{{SessionId}}`    | Current session UUID                              |
| `{{IsNewSession}}` | `"true"` when new session created                 |
| `{{MediaUrl}}`     | Inbound media pseudo-URL                          |
| `{{MediaPath}}`    | Local media path                                  |
| `{{MediaType}}`    | Media type (image/audio/document/…)               |
| `{{Transcript}}`   | Audio transcript                                  |
| `{{Prompt}}`       | Resolved media prompt for CLI entries             |
| `{{MaxChars}}`     | Resolved max output chars for CLI entries         |
| `{{ChatType}}`     | `"direct"` or `"group"`                           |
| `{{GroupSubject}}` | Group subject (best effort)                       |
| `{{GroupMembers}}` | Group members preview (best effort)               |
| `{{SenderName}}`   | Sender display name (best effort)                 |
| `{{SenderE164}}`   | Sender phone number (best effort)                 |
| `{{Provider}}`     | Provider hint (whatsapp, telegram, discord, etc.) |

## Config includes (`$include`)

The `$include` directive splits config across files, e.g. `agents: { $include: "./agents.json5" }` or the array form `broadcast: { $include: ["./clients/mueller.json5", "./clients/schmidt.json5"] }`. Merge behavior from source: a single file replaces the containing object; an array is deep-merged in order (later overrides earlier); sibling keys are merged after includes (overriding included values); nested includes go up to 10 levels deep; paths resolve relative to the including file but must stay inside the top-level config directory (`dirname` of `openclaw.json`) — absolute/`../` forms allowed only when they still resolve inside that boundary, no null bytes, and strictly shorter than 4096 characters before and after resolution. OpenClaw-owned writes changing only one top-level section backed by a single-file include write through to that file (e.g. `plugins install` updates `plugins: { $include: "./plugins.json5" }` in `plugins.json5`, leaving `openclaw.json` intact); root includes, include arrays, and includes with sibling overrides are read-only for such writes, which fail closed rather than flatten the config. Errors give clear messages for missing files, parse errors, circular includes, invalid path format, and excessive length. (`$include` also works with env-var substitution.)

## Related Notes

**Terms**

- **[Cron](../../term_dictionary/term_cron.md)** — scheduled jobs; relevance: the `cron` block (retry/failureAlert/failureDestination).
- **[ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md)** — agent client protocol; relevance: the `acp` runtime config block.
- **[JSON-RPC](../../term_dictionary/term_json_rpc.md)** — RPC-over-JSON; relevance: the CLI/RPC/ACP config surface.
- **[Webhook](../../term_dictionary/term_webhook.md)** — HTTP callback; relevance: cron `delivery.mode="webhook"` + failure webhooks.
- **[OpenClaw](../../term_dictionary/term_openclaw.md)** — the gateway product; relevance: the jobs/ops surfaces being configured.
- **[Idempotency](../../term_dictionary/term_idempotency.md)** — safe re-execution; relevance: cron retry/backoff + one-shot vs recurring semantics.
- **[Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md)** — agent runtimes; relevance: ACP backends drive external coding-agent runtimes.
- **[Cline](../../term_dictionary/term_cline.md)** — an ACP-capable editor/agent; relevance: ACP backend/agent allowlist target.

**Docs**

- **[oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md)** — secrets/auth/logging/diagnostics (this series, split sibling); relevance: the security/observability half of the same source page.
- **[oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md)** — runtime cluster (this series); relevance: sibling field-reference cluster.
- **[oc_gateway_config_reference_platform](oc_gateway_config_reference_platform.md)** — platform cluster (this series); relevance: sibling field-reference cluster.
- **[Hermes — Cron Internals](../hermes_agent/hermes_cron_internals.md)** — cron job model; relevance: the `cron` retry/failure config in another tool.
- **[Hermes — Advanced Cron Jobs](../hermes_agent/hermes_cron_advanced_jobs.md)** — cron cost/data-flow; relevance: cron failure/delivery analog.
- **[Hermes — ACP Editor Integration](../hermes_agent/hermes_acp_editor_integration.md)** — ACP integration; relevance: analog of the `acp` runtime config.
- **[Claude Code — ACP Internals](../claude_code/cc_agent_sdk_overview.md)** — agent protocol surface; relevance: ACP backend/runtime analog.
- **[oc_gateway_doctor](oc_gateway_doctor.md)** — repair tool (this series); relevance: `doctor --fix` strips legacy `bridge.*` and migrates cron `notify:true` jobs.
- **[oc_concepts_commitments](oc_concepts_commitments.md)** — scheduled commitments (this series); relevance: cron-adjacent scheduled execution.

**Repos**

- **[repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md)** — gateway runtime; relevance: cron/acp/update/`$include` config validation.
- **[repo_openclaw](../../../areas/code_repos/repo_openclaw.md)** — monorepo; relevance: config includes (`$include`) root + media template variables.
- **[repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md)** — agent runtime; relevance: ACP backend dispatch + media model args.

**Snippets**

- **[snippet_hermes_agent_cron_run_job_execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md)** — cron job execution; relevance: the `cron` retry/failure config in action.
- **[snippet_openclaw_acp_translator_init_session](../../code_snippets/snippet_openclaw_acp_translator_init_session.md)** — ACP session init; relevance: the `acp` runtime backend/session config.
- **[snippet_openclaw_acp_translator_rate_limit](../../code_snippets/snippet_openclaw_acp_translator_rate_limit.md)** — ACP rate limiting; relevance: `acp` concurrency/stream config.
- **[snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md)** — process orchestration; relevance: isolated cron agent-turn execution.
- **[snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md)** — gateway RPC methods; relevance: the CLI/ACP/RPC config surface.
- **[snippet_hermes_agent_core_config_loader](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md)** — config startup/validation; relevance: `$include` resolution + update/startup config.
- **[snippet_openclaw_agents_model_fallback_observation](../../code_snippets/snippet_openclaw_agents_model_fallback_observation.md)** — model fallback; relevance: media model args + provider selection.
- **[snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md)** — chat send/delivery; relevance: cron `delivery`/announce destination behavior.
- **[snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md)** — manifest/config format; relevance: JSON5 config-block parsing analog.
- **[snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md)** — plugin runtime load; relevance: `plugins install` write-through to `$include` files.

## References

- [OpenClaw Docs — Configuration reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw Docs — Configuration](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw Docs — Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs)
- [OpenClaw Docs — Background tasks](https://docs.openclaw.ai/automation/tasks)
- [OpenClaw Docs — config-agents (Agent defaults)](https://docs.openclaw.ai/gateway/config-agents)

**Source**: OpenClaw documentation — `gateway/configuration-reference` (jobs/operations cluster; mirror `inbox/openclaw_docs/gateway/configuration-reference.md`)
**Last Updated**: 2026-06-23
**Status**: Active
