---
title: Sub-Plan pl09 — OpenClaw Docs: Plugins (Reference D-batch — diagnostics, diffs, discord, document-extract, duckduckgo)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - plugins/reference/diagnostics-otel
  - plugins/reference/diagnostics-prometheus
  - plugins/reference/diffs
  - plugins/reference/diffs-language-pack
  - plugins/reference/discord
  - plugins/reference/document-extract
  - plugins/reference/duckduckgo
---

# Sub-Plan pl09: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, `oc_*` prefix), format (YAML field order + `## Overview` → `## Related Notes` → `## References` + bold footer), dedup (3-way: term_dictionary + documentation/ + repo_openclaw*), 9-GATE validation, cross-references, and entry-point wiring are ALL inherited from the master and applied verbatim here.
> This batch is the `plugins/reference/` "D" run: 7 thin, single-purpose plugin-reference stub pages (50–151 words each, 0 code fences). Each page → exactly 1 `concept` note; no splits. Phase C (P3, plugin reference sprawl).

## Scope

The 7 OpenClaw plugin-reference pages covering diagnostics exporters, the diff viewer family, the Discord channel plugin, the document-extract tool plugin, and the DuckDuckGo web-search provider plugin. Each `plugins/reference/<name>` page is the canonical per-plugin reference card (npm package name, ClawHub install route, contract/channel/skill surface, and — where present — added languages or pointers to the full feature doc). P3 priority (Phase C): these are the catalog-card layer the richer concept/tools/channels docs reference. The code-side counterparts (`repo_openclaw_extensions`, `repo_openclaw_channels`, `repo_openclaw_extensions_llm_providers`) are LINKED, never recreated.

**Source**: OpenClaw docs, 7 pages, 485 measured words (verbatim mirror `inbox/openclaw_docs/plugins/reference/`). **Planned: 7 notes** (1 per page; below the master's nominal 11/sub-plan estimate because these are stub-class reference cards).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Diagnostics OpenTelemetry plugin | `plugins/reference/diagnostics-otel` | 54 | 0 | 2 | 0 | concept |
| Diagnostics Prometheus plugin | `plugins/reference/diagnostics-prometheus` | 50 | 0 | 2 | 0 | concept |
| Diffs plugin | `plugins/reference/diffs` | 55 | 0 | 2 | 0 | concept |
| Diffs Language Pack plugin | `plugins/reference/diffs-language-pack` | 151 | 0 | 3 | 0 | concept |
| Discord plugin | `plugins/reference/discord` | 63 | 0 | 3 | 0 | concept |
| Document Extract plugin | `plugins/reference/document-extract` | 62 | 0 | 3 | 0 | concept |
| DuckDuckGo plugin | `plugins/reference/duckduckgo` | 50 | 0 | 3 | 0 | concept |

Shared H2 across all 7 pages: `## Distribution` (package name + install route) and `## Surface` (the plugin contracts/channels/skills it provides). `diffs-language-pack` adds `## Added languages` (the Shiki language list); `discord`/`document-extract`/`duckduckgo` add `## Related docs` (a pointer to the full feature page under `channels/` or `tools/`). Total: 485 words, 0 code fences, 0 H3.

## Content Strategy

- **Prioritize**: faithful reproduction of each plugin's identity card — package name (`@openclaw/<name>`), install route (npm + ClawHub vs "included in OpenClaw"), and surface (the contract IDs it implements: `tools`, `skills`, `channels: discord`, `contracts: documentExtractors`, `contracts: webSearchProviders`, `contracts: transcriptSourceProviders`). These distribution+surface facts are the load-bearing content; the `## Overview` paragraph paraphrases the page summary.
- **Split**: NONE. Every page is 50–151 words, 0 code fences, single-BB (a descriptive reference card = `concept`). All sit far below the ≤2500w / ≤6-fence / one-BB caps. Per the master ("Most reference pages = 1 note"), each page = 1 note. See Split Decisions.
- **Link-out (do NOT inline)**: the full feature docs each stub points at live in OTHER sub-plans — `channels/discord` (ch01), `tools/pdf` / `tools/duckduckgo-search` (to06/to03), `tools/diffs` (to02), `gateway/opentelemetry` + `gateway/prometheus` (gw04/gw05), and the SDK/architecture plugin docs (pl01–pl04, pl23–pl25). Each note cross-links these as siblings/"(planned)" rather than reproducing them. Plugin vocabulary (plugin, contract, surface, ClawHub, diagnostics exporter) → linked to existing `term_*` / sibling `oc_*`, never promoted to new term notes.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_diagnostics_otel.md` | concept | diagnostics-otel.md: summary, Distribution, Surface | 220 | The `@openclaw/diagnostics-otel` plugin: an OpenTelemetry exporter that ships OpenClaw runtime metrics, traces, and logs to an OTel collector. Documents the npm/ClawHub install route and its plugin surface; points to the gateway OpenTelemetry config doc. |
| 2 | `oc_plugins_reference_diagnostics_prometheus.md` | concept | diagnostics-prometheus.md: summary, Distribution, Surface | 210 | The `@openclaw/diagnostics-prometheus` plugin: a Prometheus exporter for OpenClaw runtime metrics (scrape endpoint). Documents the npm/ClawHub install route and plugin surface; points to the gateway Prometheus config doc. |
| 3 | `oc_plugins_reference_diffs.md` | concept | diffs.md: summary, Distribution, Surface | 210 | The `@openclaw/diffs` plugin: a read-only diff viewer and file renderer for agents, providing both a `tools` contract and `skills`. Documents the npm/ClawHub install route and surface; points to the full Diffs tool doc. |
| 4 | `oc_plugins_reference_diffs_language_pack.md` | concept | diffs-language-pack.md: summary, Distribution, Surface, Added languages | 320 | The `@openclaw/diffs-language-pack` plugin: adds Shiki syntax highlighting for languages outside the base `diffs` set (Astro, Vue, Svelte, GraphQL, Terraform, Nix, Elixir, Solidity, etc.). Documents install route, the added-language list, and the graceful plain-text fallback when absent. |
| 5 | `oc_plugins_reference_discord.md` | concept | discord.md: summary, Distribution, Surface, Related docs | 230 | The `@openclaw/discord` channel plugin: connects OpenClaw to Discord channels, DMs, slash commands, and app events, providing the `channels: discord` and `transcriptSourceProviders` contracts. Documents install route and surface; points to the full Discord channel doc. |
| 6 | `oc_plugins_reference_document_extract.md` | concept | document-extract.md: summary, Distribution, Surface, Related docs | 230 | The `@openclaw/document-extract-plugin`: extracts text and fallback page images from local document attachments, providing the `documentExtractors` contract. Bundled with OpenClaw; documents surface and points to the PDF tool doc. |
| 7 | `oc_plugins_reference_duckduckgo.md` | concept | duckduckgo.md: summary, Distribution, Surface, Related docs | 210 | The `@openclaw/duckduckgo-plugin`: adds DuckDuckGo as a web-search provider via the `webSearchProviders` contract. Bundled with OpenClaw; documents surface and points to the DuckDuckGo search tool doc. |

Filename rule applied: `oc_` + full slug with `/` and `-` → `_`. E.g. `plugins/reference/diagnostics-otel` → `oc_plugins_reference_diagnostics_otel.md`; `plugins/reference/diffs-language-pack` → `oc_plugins_reference_diffs_language_pack.md`.

## Section Coverage Map

```
plugins/reference/diagnostics-otel.md
├── summary / intro paragraph ───────────────────── → note 1 (oc_plugins_reference_diagnostics_otel) Overview
├── ## Distribution (@openclaw/diagnostics-otel, npm + ClawHub) → note 1
└── ## Surface (plugin) ──────────────────────────── → note 1
plugins/reference/diagnostics-prometheus.md
├── summary / intro paragraph ───────────────────── → note 2 (oc_plugins_reference_diagnostics_prometheus) Overview
├── ## Distribution (@openclaw/diagnostics-prometheus) → note 2
└── ## Surface (plugin) ──────────────────────────── → note 2
plugins/reference/diffs.md
├── summary / intro paragraph ───────────────────── → note 3 (oc_plugins_reference_diffs) Overview
├── ## Distribution (@openclaw/diffs, npm + ClawHub) → note 3
└── ## Surface (contracts: tools; skills) ────────── → note 3
plugins/reference/diffs-language-pack.md
├── summary / intro paragraph ───────────────────── → note 4 (oc_plugins_reference_diffs_language_pack) Overview
├── ## Distribution (@openclaw/diffs-language-pack) ─ → note 4
├── ## Surface (plugin) ──────────────────────────── → note 4
└── ## Added languages (Shiki set + fallback note) ─ → note 4
plugins/reference/discord.md
├── summary / intro paragraph ───────────────────── → note 5 (oc_plugins_reference_discord) Overview
├── ## Distribution (@openclaw/discord, npm + ClawHub) → note 5
├── ## Surface (channels: discord; transcriptSourceProviders) → note 5
└── ## Related docs (/channels/discord pointer) ──── → note 5 (cross-link to ch01, not inlined)
plugins/reference/document-extract.md
├── summary / intro paragraph ───────────────────── → note 6 (oc_plugins_reference_document_extract) Overview
├── ## Distribution (@openclaw/document-extract-plugin, included) → note 6
├── ## Surface (contracts: documentExtractors) ───── → note 6
└── ## Related docs (/tools/pdf pointer) ─────────── → note 6 (cross-link to to06, not inlined)
plugins/reference/duckduckgo.md
├── summary / intro paragraph ───────────────────── → note 7 (oc_plugins_reference_duckduckgo) Overview
├── ## Distribution (@openclaw/duckduckgo-plugin, included) → note 7
├── ## Surface (contracts: webSearchProviders) ───── → note 7
└── ## Related docs (/tools/duckduckgo-search pointer) → note 7 (cross-link to to03, not inlined)
```
No orphaned sections. Every H2/H3 of all 7 pages maps to its note. The `Related docs` pointers (channels/discord, tools/pdf, tools/duckduckgo-search) and the gateway OTel/Prometheus docs are cross-linked to their owning sub-plans, NOT duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are 50–151 words, 0 code fences, single descriptive BB (a plugin reference card = `concept`). None approaches the ≤2500w / ≤6-fence / one-BB caps, so each page → exactly 1 note per the master "most reference pages = 1 note" rule. |

## Summary Statistics & Building Block Distribution

- Source pages: 7 (485 measured words). New `oc_*` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: concept ×7 (notes 1–7). No procedure/model/argument notes (these are descriptive reference cards, not step-by-step procedures).
- Est. digest words ~1,630 (avg ~233/note). The digest notes are intentionally larger than their 50–151-word sources because each adds an `## Overview`, a `## Related Notes` block (≥6 relevance-selected terms + siblings/repos), and a `## References` block per the shared format — none approaches the 2,500-word / 6-fence / 400-line caps. 0 source code fences ⇒ 0 reproduced fences.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_plugins_reference_diagnostics_otel (8t · 10s · 10d)

**Terms** (8)
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — observability of agent runtimes; relevance: OTel metrics/traces/logs are the agent-observability signals this exporter emits.
- [Data Observability](../../term_dictionary/term_data_observability.md) — observability discipline; relevance: the exporter is OpenClaw's OpenTelemetry instrumentation surface.
- [Trace](../../term_dictionary/term_trace.md) — distributed trace; relevance: "traces" is one of the three OTel signal types this plugin exports.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — observer/exporter pattern; relevance: a diagnostics exporter observes runtime events and forwards them to an OTel collector.
- [Model Monitoring](../../term_dictionary/term_model_monitoring.md) — runtime/model monitoring; relevance: agent runtime metrics this exporter ships feed monitoring dashboards.
- [Context Propagation](../../term_dictionary/term_context_propagation.md) — trace-context propagation; relevance: OTel spans propagate trace context across the runtime calls this exporter captures.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: the host product whose runtime this plugin instruments.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: tool/MCP calls are among the agent operations whose traces/metrics get exported.

**Docs** (11)
- [Claude Code — Monitoring with OpenTelemetry Setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — CC OTel exporter config; relevance: the closest existing doc for the same "ship agent telemetry over OTel" pattern this plugin implements.
- [Claude Code — OTel Analysis and Privacy](../claude_code/cc_otel_analysis_and_privacy.md) — OTel signal analysis + privacy; relevance: what consumers do with the metrics/traces this exporter emits, and the privacy considerations.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — sibling-ecosystem plugin system; relevance: the plugin packaging/loading model the OpenClaw diagnostics plugin follows.
- [Hermes — Plugin Types and Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the "plugin" surface this exporter declares in `## Surface`.
- [Bedrock AgentCore — Observability Telemetry](../aws_bedrock_agentcore/bedrock_agentcore_observability_telemetry.md) — agent telemetry pipeline; relevance: the OTel-based agent telemetry model parallel to this exporter.
- [Bedrock AgentCore — Observability Overview](../aws_bedrock_agentcore/bedrock_agentcore_observability_overview.md) — agent observability overview; relevance: framing for the metrics/traces/logs triad this plugin exports.
- [CloudWatch — OTel Overview](../aws_cloudwatch/cloudwatch_otel_overview.md) — OTel collector ingest; relevance: a concrete OTel-collector backend the exporter's OTLP output can target.
- [OpenSearch — Trace Analytics](../aws_opensearch/opensearch_trace_analytics.md) — trace storage/analytics; relevance: a backend that consumes the traces this exporter ships.
- `oc_plugins_reference_diagnostics_prometheus.md` — (planned, this series) Prometheus exporter; relevance: the sibling diagnostics exporter (pull/scrape) vs OTel's push/OTLP pipeline.
- `../openclaw/oc_gateway_opentelemetry.md` — (planned, gw04) gateway OTel config; relevance: the full gateway-side OTel configuration this plugin reference card points at.
- `../../../0_entry_points/entry_openclaw_docs.md` — (planned, master W1 pre-step) docs hub; relevance: navigation hub that links every `oc_*` note (G7/G8 inbound link).

- [oc_plugins_reference_diagnostics_prometheus](oc_plugins_reference_diagnostics_prometheus.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.
- [oc_plugins_reference_diffs](oc_plugins_reference_diffs.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos** (2)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions/plugins repo; relevance: the diagnostics-otel plugin is one of these extensions (code-side counterpart).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway repo; relevance: the gateway runtime is the source of the metrics/traces/logs this exporter ships.

**Snippets** (10)
- [snippet_hermes_agent_plugins_observability_langfuse](../../code_snippets/snippet_hermes_agent_plugins_observability_langfuse.md) — observability plugin wiring (Langfuse); relevance: the closest code-level pattern for an observability-exporter plugin.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — runtime logging setup; relevance: the "logs" signal this exporter forwards is produced by this logging layer.
- [snippet_hermes_agent_cli_logs](../../code_snippets/snippet_hermes_agent_cli_logs.md) — CLI logs surface; relevance: operational logs comparable to the log signal this exporter ships.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: the runtime whose env/metrics this exporter instruments.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway plugin config loader; relevance: how a diagnostics plugin like this one is registered/loaded into the gateway.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — session/transcript events; relevance: the runtime events that become traces/spans this exporter emits.
- [snippet_hermes_agent_core_account_usage](../../code_snippets/snippet_hermes_agent_core_account_usage.md) — usage/accounting counters; relevance: example runtime metrics of the kind this exporter would ship.
- [snippet_hermes_agent_core_rate_limit_tracker](../../code_snippets/snippet_hermes_agent_core_rate_limit_tracker.md) — rate-limit metrics tracking; relevance: another runtime counter category exposed via telemetry export.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — process/exec orchestration; relevance: a runtime subsystem whose spans/metrics flow into the OTel pipeline.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the SDK entry contract this diagnostics plugin registers through.

### oc_plugins_reference_diagnostics_prometheus (8t · 10s · 10d)

**Terms** (8)
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — agent observability; relevance: Prometheus metrics are the agent-runtime observability signal this exporter exposes.
- [Data Observability](../../term_dictionary/term_data_observability.md) — observability discipline; relevance: the plugin is OpenClaw's pull-based metrics instrumentation.
- [Model Monitoring](../../term_dictionary/term_model_monitoring.md) — runtime monitoring; relevance: Prometheus scrape metrics drive runtime/model monitoring and alerting.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — observer/exporter pattern; relevance: a metrics exporter publishes observed runtime counters for a scraper to pull.
- [Time Series Database](../../term_dictionary/term_time_series_database.md) — TSDB; relevance: Prometheus stores the scraped runtime metrics as a time series.
- [Service Level Indicator](../../term_dictionary/term_sli.md) — SLI; relevance: the runtime counters this exporter exposes are the raw signals SLIs are computed from.
- [Mean Time To Recovery](../../term_dictionary/term_mttr.md) — MTTR; relevance: an operational metric derived from the alerting built on these scraped counters.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: the host product whose runtime metrics this plugin exposes.

**Docs** (11)
- [CloudWatch — Metrics Overview](../aws_cloudwatch/cloudwatch_metrics_overview.md) — metrics model; relevance: the scrape-style runtime-metrics surface this exporter exposes maps to the same metric concepts.
- [CloudWatch — Container Insights Overview](../aws_cloudwatch/cloudwatch_container_insights_overview.md) — runtime/container metrics; relevance: the container/runtime metric category a Prometheus scrape endpoint surfaces.
- [Claude Code — Monitoring with OpenTelemetry Setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — agent metrics export; relevance: the sibling "export agent runtime metrics" pattern (OTLP) vs this plugin's Prometheus scrape model.
- [Bedrock AgentCore — Observability Overview](../aws_bedrock_agentcore/bedrock_agentcore_observability_overview.md) — agent observability; relevance: framing for the runtime-metrics surface this exporter exposes.
- [Bedrock AgentCore — Observability Setup](../aws_bedrock_agentcore/bedrock_agentcore_observability_setup.md) — observability wiring; relevance: how an agent runtime is wired for metrics scraping/collection.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin packaging/loading; relevance: the plugin model this Prometheus exporter follows.
- [Hermes — Plugin Types and Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the "plugin" surface this exporter declares.
- `oc_plugins_reference_diagnostics_otel.md` — (planned, this series) OTel exporter; relevance: the sibling diagnostics exporter (push/OTLP) vs Prometheus's pull/scrape model.
- `../openclaw/oc_gateway_prometheus.md` — (planned, gw05) gateway Prometheus config; relevance: the full gateway-side Prometheus configuration this card points at.
- `../../../0_entry_points/entry_openclaw_docs.md` — (planned, master W1 pre-step) docs hub; relevance: inbound navigation link for G7/G8.

- [oc_plugins_reference_diagnostics_otel](oc_plugins_reference_diagnostics_otel.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.
- [oc_plugins_reference_diffs](oc_plugins_reference_diffs.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos** (2)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions/plugins repo; relevance: the diagnostics-prometheus plugin lives among these extensions.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway repo; relevance: the gateway runtime is the metrics source scraped via this exporter.

**Snippets** (10)
- [snippet_hermes_agent_plugins_observability_langfuse](../../code_snippets/snippet_hermes_agent_plugins_observability_langfuse.md) — observability plugin wiring; relevance: the code-level pattern for an observability-exporter plugin.
- [snippet_hermes_agent_core_account_usage](../../code_snippets/snippet_hermes_agent_core_account_usage.md) — usage/accounting counters; relevance: example runtime metrics a Prometheus endpoint would expose.
- [snippet_hermes_agent_core_rate_limit_tracker](../../code_snippets/snippet_hermes_agent_core_rate_limit_tracker.md) — rate-limit metrics; relevance: a runtime counter category surfaced via the scrape endpoint.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — runtime logging setup; relevance: the runtime that produces the operational signals adjacent to these metrics.
- [snippet_hermes_agent_cli_logs](../../code_snippets/snippet_hermes_agent_cli_logs.md) — CLI logs surface; relevance: operational telemetry comparable to the metrics surface this plugin exposes.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: the runtime whose metrics this exporter exposes for scraping.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway plugin config loader; relevance: how this diagnostics plugin is registered/loaded into the gateway.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — session/transcript events; relevance: runtime events whose counts become scrape-able metrics.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — process/exec orchestration; relevance: a runtime subsystem whose counters the Prometheus endpoint exposes.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the SDK entry contract this diagnostics plugin registers through.

### oc_plugins_reference_diffs (8t · 10s · 10d)

**Terms** (8)
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — registry of agent tools; relevance: the diffs plugin contributes a `tools` contract registered for agent use (its `## Surface`).
- [Skills](../../term_dictionary/term_skills.md) — agent skills; relevance: the plugin also provides `skills` — the second half of its declared surface.
- [Atomic Skill](../../term_dictionary/term_atomic_skill.md) — atomic skill unit; relevance: the diff-viewer skill is a discrete capability the plugin packages.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/function calls; relevance: the diff viewer is invoked as an agent tool call.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — read-only render/observe; relevance: a read-only diff viewer observes and renders file changes without mutating them.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool descriptor/schema; relevance: the `tools` contract entry the diffs plugin registers is described by a tool descriptor.
- [npm](../../term_dictionary/term_npm.md) — npm package distribution; relevance: install route is npm (plus ClawHub) per `## Distribution`.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: the host product the diffs tool plugs into.

**Docs** (11)
- [Hermes — Tool Gateway](../hermes_agent/hermes_tool_gateway.md) — tool registration/dispatch; relevance: the `tools` contract this plugin contributes is registered and dispatched through this layer.
- [Hermes — Toolsets Reference](../hermes_agent/hermes_toolsets_reference.md) — built-in tool catalog; relevance: catalog context for a read-only file-rendering tool like diffs.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin packaging/loading; relevance: the plugin model the diffs tool+skill plugin follows.
- [Hermes — Plugin Types and Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the `tools` + `skills` dual surface this plugin declares.
- [Hermes — Build Plugin Tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — how to author a plugin; relevance: the authoring path for a tools/skills plugin like diffs.
- [pi — Skills](../pi/pi_skills.md) — coding-agent skills model; relevance: the `skills` surface the diffs plugin contributes, in a sibling agent.
- [Claude Code — Channels Setup](../claude_code/cc_channels_setup.md) — coding-agent surface setup; relevance: cross-corpus precedent for how an agent surfaces tool/skill capabilities (loose).
- `oc_plugins_reference_diffs_language_pack.md` — (planned, this series) language pack; relevance: the companion plugin that extends this viewer's syntax-highlighting language set.
- `../openclaw/oc_tools_diffs.md` — (planned, to02) full diffs tool doc; relevance: the complete tool reference this card points at.
- `../../../0_entry_points/entry_openclaw_docs.md` — (planned, master W1 pre-step) docs hub; relevance: inbound navigation link for G7/G8.

- [oc_plugins_reference_diagnostics_otel](oc_plugins_reference_diagnostics_otel.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.
- [oc_plugins_reference_diagnostics_prometheus](oc_plugins_reference_diagnostics_prometheus.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos** (2)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions/plugins repo; relevance: code-side home of the diffs plugin/tool.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — OpenClaw skills repo; relevance: the `skills` half of the plugin's surface.

**Snippets** (10)
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry impl; relevance: how a `tools` contract entry like the diff viewer is registered.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the manifest that declares this plugin's tools/skills surface.
- [snippet_hermes_agent_skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — skills vs plugins distinction; relevance: clarifies the dual `tools` + `skills` surface this plugin exposes.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK structure a tools/skills plugin is built on.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: the entry-point contract the diffs plugin registers through.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skills manifest format; relevance: the `skills` half of the plugin's surface is declared in this format.
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — tool registration over ACP; relevance: another tool-registration path comparable to the diffs `tools` contract.
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — plugin discovery; relevance: how an installed plugin like diffs is discovered/listed.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway plugin config; relevance: how the diffs plugin is loaded/configured into the gateway.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — a concrete tool-plugin impl; relevance: worked example of a plugin contributing a tool contract (parallel to diffs).

### oc_plugins_reference_diffs_language_pack (8t · 10s · 10d)

**Terms** (8)
- [Skills](../../term_dictionary/term_skills.md) — agent skills; relevance: the language pack augments the diffs viewer skill's rendering capability.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — tool registry; relevance: it extends the registered diffs tool's supported file types.
- [Atomic Skill](../../term_dictionary/term_atomic_skill.md) — atomic capability; relevance: the language pack is a discrete add-on capability bundled as a plugin.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — render/observe; relevance: syntax highlighting is part of the read-only render path the base viewer performs.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: the broadened highlighting applies whenever the diffs tool is invoked on a now-supported language.
- [Markdown](../../term_dictionary/term_markdown.md) — markup/rendering; relevance: a representative text format whose Shiki-based highlighting/rendering the pack broadens (markup-family languages like MDX/Mermaid are in its set).
- [npm](../../term_dictionary/term_npm.md) — npm distribution; relevance: install route is npm + ClawHub per `## Distribution`.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: the host whose diffs viewer this pack extends.

**Docs** (11)
- [Hermes — Toolsets Reference](../hermes_agent/hermes_toolsets_reference.md) — tool catalog; relevance: catalog context for the file-rendering tool this pack extends.
- [Hermes — Tool Gateway](../hermes_agent/hermes_tool_gateway.md) — tool dispatch; relevance: the tool layer the broadened highlighting plugs into when diffs renders a file.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin packaging/loading; relevance: the plugin model this add-on pack follows.
- [Hermes — Plugin Types and Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the "plugin" surface the language pack declares.
- [Hermes — Build Plugin Tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — plugin authoring; relevance: the authoring path for an extension plugin like this language pack.
- [pi — Skills](../pi/pi_skills.md) — coding-agent skills; relevance: the diffs viewer skill the pack augments, in a sibling agent.
- [Hermes — Skill MD Format Bundles](../hermes_agent/hermes_skill_md_format_bundles.md) — skill/bundle packaging; relevance: how an add-on capability bundle is packaged and shipped.
- `oc_plugins_reference_diffs.md` — (planned, this series) base diffs plugin; relevance: the parent plugin this pack extends with Shiki languages outside the default set.
- `../openclaw/oc_tools_diffs.md` — (planned, to02) full diffs tool doc; relevance: the base-viewer doc whose default language set this pack broadens.
- `../../../0_entry_points/entry_openclaw_docs.md` — (planned, master W1 pre-step) docs hub; relevance: inbound navigation link for G7/G8.

- [oc_plugins_reference_diagnostics_otel](oc_plugins_reference_diagnostics_otel.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.
- [oc_plugins_reference_diagnostics_prometheus](oc_plugins_reference_diagnostics_prometheus.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos** (2)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions/plugins repo; relevance: code-side home of the language-pack plugin.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — OpenClaw skills repo; relevance: the skills surface the diffs viewer is part of.

**Snippets** (10)
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skills manifest format; relevance: the manifest format an add-on like this language pack ships with.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the manifest that declares the language pack as a plugin.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: the SDK entry contract the pack registers through.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK structure an extension plugin is built on.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry impl; relevance: the diffs tool whose language coverage this pack extends is registered here.
- [snippet_hermes_agent_skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — skills vs plugins; relevance: clarifies how a skill-augmenting pack relates to the base plugin.
- [snippet_hermes_agent_cli_plugins_discover](../../code_snippets/snippet_hermes_agent_cli_plugins_discover.md) — plugin discovery; relevance: how the installed language pack is discovered/listed.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway plugin config; relevance: how the pack is loaded/enabled into the gateway.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — concrete tool-plugin impl; relevance: worked example of a plugin extending agent capability (parallel pattern).
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — tool registration; relevance: registration path for the diffs tool the pack augments.

### oc_plugins_reference_discord (9t · 10s · 10d)

**Terms** (9)
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — channel adapter; relevance: the Discord plugin is a channel adapter bridging OpenClaw to Discord channels/DMs.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — messaging gateway; relevance: it routes messages between OpenClaw and the Discord platform.
- [Omnichannel](../../term_dictionary/term_omnichannel.md) — omnichannel messaging; relevance: Discord is one of OpenClaw's 11+ supported chat platforms in the omnichannel surface.
- [Bot](../../term_dictionary/term_bot.md) — chat bot; relevance: the plugin operates OpenClaw as a Discord bot handling commands and app events.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — channel kernel; relevance: the channel-runtime abstraction the Discord adapter registers into.
- [WebSocket](../../term_dictionary/term_websocket.md) — WebSocket transport; relevance: Discord's gateway connection (channels, DMs, app events) runs over a WebSocket.
- [Phoenix Channels](../../term_dictionary/term_phoenix_channels.md) — channel/pub-sub abstraction; relevance: a comparable channel-subscription model for real-time message delivery.
- [npm](../../term_dictionary/term_npm.md) — npm distribution; relevance: install route is npm + ClawHub per `## Distribution`.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: the host product the Discord channel plugs into.

**Docs** (11)
- [Hermes — Discord Setup](../hermes_agent/hermes_discord_setup.md) — Discord channel setup; relevance: the sibling-ecosystem Discord channel doc for the same platform this plugin connects.
- [Hermes — Discord Advanced](../hermes_agent/hermes_discord_advanced.md) — advanced Discord features; relevance: deeper coverage of the channels/DMs/commands surface this plugin provides.
- [Hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging gateway design; relevance: the gateway architecture a channel adapter like Discord registers into.
- [Hermes — Messaging Slack](../hermes_agent/hermes_messaging_slack.md) — a sibling channel adapter; relevance: parallel chat-platform adapter (same channel-plugin contract family).
- [Hermes — Slash Commands Messaging](../hermes_agent/hermes_slash_commands_messaging.md) — slash commands; relevance: the slash-command surface this Discord plugin exposes.
- [Hermes — Voice Gateway Discord VC](../hermes_agent/hermes_voice_gateway_discord_vc.md) — Discord voice channels; relevance: the voice-channel side of the same Discord integration.
- [Claude Code — Channels Overview](../claude_code/cc_channels_overview.md) — coding-agent channels; relevance: cross-corpus precedent for chat-channel integration surfaces.
- [Hermes — Plugin Types and Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the `channels` + `transcriptSourceProviders` surface this plugin declares.
- `oc_plugins_reference_diffs.md` — (planned, this series) sibling reference card; relevance: same `plugins/reference/` distribution+surface card structure (a different contract family).
- `../openclaw/oc_channels_discord.md` — (planned, ch01) full Discord channel doc; relevance: the complete channel reference this card points at.
- `../../../0_entry_points/entry_openclaw_docs.md` — (planned, master W1 pre-step) docs hub; relevance: inbound navigation link for G7/G8.

- [oc_plugins_reference_diagnostics_otel](oc_plugins_reference_diagnostics_otel.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.
- [oc_plugins_reference_diagnostics_prometheus](oc_plugins_reference_diagnostics_prometheus.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos** (2)
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — OpenClaw channels repo; relevance: code-side home of the Discord channel plugin.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — OpenClaw messaging-channels repo; relevance: the messaging-channel subsystem Discord belongs to (DMs, channels, commands).

**Snippets** (10)
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord gateway intents; relevance: the exact OpenClaw-side Discord channel implementation this card documents.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the `channels` contract the Discord plugin implements.
- [snippet_hermes_agent_gw_platform_discord_connect](../../code_snippets/snippet_hermes_agent_gw_platform_discord_connect.md) — Discord connect/gateway; relevance: how a Discord adapter establishes its platform connection.
- [snippet_hermes_agent_gw_platform_discord_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_discord_normalize.md) — Discord message normalize; relevance: inbound Discord events normalized into the channel pipeline.
- [snippet_hermes_agent_gw_platform_discord_slash](../../code_snippets/snippet_hermes_agent_gw_platform_discord_slash.md) — Discord slash commands; relevance: the commands surface this plugin provides.
- [snippet_hermes_agent_gw_platform_discord_thread](../../code_snippets/snippet_hermes_agent_gw_platform_discord_thread.md) — Discord threads; relevance: thread/channel handling within the Discord adapter.
- [snippet_hermes_agent_gw_platform_discord_attachment](../../code_snippets/snippet_hermes_agent_gw_platform_discord_attachment.md) — Discord attachments; relevance: media/app-event handling on the Discord channel.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — base platform adapter; relevance: the abstract adapter every channel plugin (incl. Discord) implements.
- [snippet_hermes_agent_gw_platform_registry](../../code_snippets/snippet_hermes_agent_gw_platform_registry.md) — platform/channel registry; relevance: where a Discord channel adapter registers itself.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory/routing; relevance: routing of messages to/from the Discord channel.

### oc_plugins_reference_document_extract (8t · 10s · 10d)

**Terms** (8)
- [Document Understanding](../../term_dictionary/term_document_understanding.md) — document understanding; relevance: extracting text/images from attachments is the ingestion step before document understanding.
- [Document VLM](../../term_dictionary/term_document_vlm.md) — document vision-language model; relevance: fallback page images feed a VLM when text extraction is insufficient.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multimodal inputs; relevance: the plugin produces both text and image outputs for multimodal agent consumption.
- [OCR](../../term_dictionary/term_ocr.md) — optical character recognition; relevance: extracting text from page images is an OCR-class capability.
- [Data Contract](../../term_dictionary/term_data_contract.md) — contract surface; relevance: the plugin implements the `documentExtractors` contract (its `## Surface`).
- [Document Automation](../../term_dictionary/term_document_automation.md) — automated document processing; relevance: attachment text/image extraction is a document-automation step.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: extraction runs as part of the agent's PDF/attachment tool flow.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: bundled with OpenClaw; the host whose attachment pipeline it serves.

**Docs** (11)
- [Hermes — Web Search and Extract](../hermes_agent/hermes_web_search_extract.md) — content extraction; relevance: the sibling text-extraction surface comparable to document extraction.
- [Hermes — Tools Reference: Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — media/attachment tools; relevance: handling of attachments/media this plugin extracts from.
- [Hermes — Built-in Plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled plugins catalog; relevance: document-extract is bundled/"included in OpenClaw" — same built-in plugin pattern.
- [Hermes — Plugin Types and Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the contract (`documentExtractors`) surface this plugin declares.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin packaging/loading; relevance: the plugin model this included extractor follows.
- [Hermes — Memory Provider Plugin](../hermes_agent/hermes_memory_provider_plugin.md) — contract-based provider plugin; relevance: a parallel contract-implementing plugin (different contract, same surface mechanism).
- [Hermes — Integrations Overview](../hermes_agent/hermes_integrations_overview.md) — integrations/tools overview; relevance: where the document/attachment extraction integration fits in the tool surface.
- [pi — Custom Provider Registration](../pi/pi_custom_provider_registration.md) — provider/contract registration; relevance: how a contract implementation (like `documentExtractors`) is registered.
- `oc_plugins_reference_duckduckgo.md` — (planned, this series) sibling included plugin; relevance: same "included in OpenClaw" distribution pattern + contract-surface card.
- `../openclaw/oc_tools_pdf.md` — (planned, to06) full PDF tool doc; relevance: the complete tool reference this card points at.
- `../../../0_entry_points/entry_openclaw_docs.md` — (planned, master W1 pre-step) docs hub; relevance: inbound navigation link for G7/G8.

- [oc_plugins_reference_diagnostics_otel](oc_plugins_reference_diagnostics_otel.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.
- [oc_plugins_reference_diagnostics_prometheus](oc_plugins_reference_diagnostics_prometheus.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos** (2)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions/plugins repo; relevance: code-side home of the document-extract plugin (included extension).
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — OpenClaw apps repo; relevance: the app/runtime layer that consumes extracted document content.

**Snippets** (10)
- [snippet_brp_agent_tools_extract](../../code_snippets/snippet_brp_agent_tools_extract.md) — content-extraction tool; relevance: the closest code-level pattern for a text/content extractor.
- [snippet_brp_agent_tools_crawl](../../code_snippets/snippet_brp_agent_tools_crawl.md) — crawl/fetch + extract; relevance: fetch-then-extract pipeline comparable to attachment extraction.
- [snippet_hermes_agent_cli_attachment_input_bindings](../../code_snippets/snippet_hermes_agent_cli_attachment_input_bindings.md) — attachment input bindings; relevance: how local document attachments enter the pipeline this plugin extracts from.
- [snippet_hermes_agent_tools_send_attach](../../code_snippets/snippet_hermes_agent_tools_send_attach.md) — attachment send/handling; relevance: attachment-handling code adjacent to extraction.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider/contract registry; relevance: how a `documentExtractors`-style contract implementation is registered.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: the SDK entry contract this included plugin registers through.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the manifest declaring the document-extract plugin and its contract.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway plugin config; relevance: how a bundled plugin like document-extract is loaded.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — concrete tool-plugin impl; relevance: worked example of a plugin contributing a tool/contract.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK structure an included contract plugin is built on.

### oc_plugins_reference_duckduckgo (8t · 10s · 10d)

**Terms** (8)
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — information retrieval; relevance: web search is the IR capability this provider adds to the agent.
- [Internal Search](../../term_dictionary/term_internal_search.md) — search subsystem; relevance: DuckDuckGo plugs into OpenClaw's pluggable search-provider layer.
- [Hybrid Search](../../term_dictionary/term_hybrid_search.md) — multi-source search; relevance: DuckDuckGo is one selectable provider among OpenClaw's web-search providers.
- [Deep Research Agent](../../term_dictionary/term_deep_research_agent.md) — research agent; relevance: web-search providers like this one power agent research/grounding flows.
- [Data Contract](../../term_dictionary/term_data_contract.md) — contract surface; relevance: the plugin implements the `webSearchProviders` contract (its `## Surface`).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin pattern; relevance: DuckDuckGo is registered as a pluggable web-search provider via this pattern.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: web search is invoked as an agent tool call routed to this provider.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: bundled with OpenClaw; the host whose web tool it serves.

**Docs** (11)
- [Hermes — Web Search Provider Plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — web-search provider plugin; relevance: the sibling-ecosystem doc for exactly this "register a web-search provider plugin" pattern.
- [Hermes — Web Search and Extract](../hermes_agent/hermes_web_search_extract.md) — web search + extract; relevance: the web-search capability this provider contributes.
- [Hermes — Built-in Plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled plugins catalog; relevance: duckduckgo is "included in OpenClaw" — same built-in plugin pattern.
- [Hermes — Integrations Overview](../hermes_agent/hermes_integrations_overview.md) — integrations/tools overview; relevance: where a web-search provider fits in the agent's tool surface.
- [Hermes — Plugin Types and Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the `webSearchProviders` contract surface this plugin declares.
- [Hermes — Image Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — provider-plugin precedent; relevance: a parallel pluggable-provider implementation (different contract, same registration pattern).
- [pi — Custom Provider Registration](../pi/pi_custom_provider_registration.md) — provider registration; relevance: how a provider like this web-search provider is registered into the runtime.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin packaging/loading; relevance: the plugin model this included provider follows.
- `oc_plugins_reference_document_extract.md` — (planned, this series) sibling included plugin; relevance: same "included in OpenClaw" distribution + contract-surface card.
- `../openclaw/oc_tools_duckduckgo_search.md` — (planned, to03) full DuckDuckGo search tool doc; relevance: the complete tool reference this card points at.
- `../../../0_entry_points/entry_openclaw_docs.md` — (planned, master W1 pre-step) docs hub; relevance: inbound navigation link for G7/G8.

- [oc_plugins_reference_diagnostics_otel](oc_plugins_reference_diagnostics_otel.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.
- [oc_plugins_reference_diagnostics_prometheus](oc_plugins_reference_diagnostics_prometheus.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos** (2)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions/plugins repo; relevance: code-side home of the duckduckgo provider plugin (included extension).
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — OpenClaw provider-extensions repo; relevance: the pluggable provider-registration pattern this web-search provider follows.

**Snippets** (10)
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web/search tool impl; relevance: the code-level web-search tool the provider backs.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web plugin impl; relevance: a worked web-tool plugin parallel to the duckduckgo provider.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: how a `webSearchProviders` implementation registers itself.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: provider initialization/selection the web-search provider plugs into.
- [snippet_brp_agent_tools_crawl](../../code_snippets/snippet_brp_agent_tools_crawl.md) — crawl/fetch; relevance: web fetch/crawl adjacent to web-search result retrieval.
- [snippet_brp_agent_tools_extract](../../code_snippets/snippet_brp_agent_tools_extract.md) — content extract; relevance: extracting content from web-search results.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entries; relevance: the SDK entry contract this included provider plugin registers through.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the manifest declaring the duckduckgo provider plugin and its contract.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway plugin config; relevance: how a bundled provider plugin is loaded into the gateway.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK structure a provider plugin is built on.

### DB-Verification Commands (run 2026-06-21)

```bash
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
# Every EXISTING note_id cited above returned 1:
for id in <all term_/snippet_/doc/repo note_ids above>; do
done
# Sibling oc_* (this series), gw04/gw05/ch01/to02/to03/to06 docs, and entry_openclaw_docs.md → NOT yet in DB (planned).
```

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc notes by their home sub-plan, NOT as new `term_dictionary` entries; the only term-dictionary interaction is LINKING existing terms. **pl09 creates 0 new `term_dictionary` notes.**

| Term (appears in source) | Disposition |
|---|---|
| OpenTelemetry / OTel exporter | Documented in `oc_plugins_reference_diagnostics_otel` (oc_ doc note); link existing `term_observability_agent_systems` / `term_trace` / `term_data_observability`. Not promoted (the full OTel config lives in `gateway/opentelemetry`, gw04). |
| Prometheus exporter / metrics | Documented in `oc_plugins_reference_diagnostics_prometheus`; link `term_observability_agent_systems` / `term_model_monitoring`. Full config in `gateway/prometheus` (gw05). Not a new term. |
| diagnostics exporter | Generic concept; captured inline in notes 1–2; link `term_observer_pattern`. Not a new term. |
| diff viewer / file renderer | Documented in `oc_plugins_reference_diffs`; link `term_tool_registry` / `term_skills`. Full tool doc in `tools/diffs` (to02). Not a new term. |
| Shiki / syntax highlighting / language pack | Documented in `oc_plugins_reference_diffs_language_pack` (Shiki named as external dep, linked in References). Not a vault-reusable cross-cutting term → not promoted. |
| Discord (platform) | Documented in `oc_plugins_reference_discord`; link `term_channel_adapter` / `term_omnichannel` / `term_bot`. Platform name is config, not a term note. Full channel doc in `channels/discord` (ch01). |
| document extract / documentExtractors contract | Documented in `oc_plugins_reference_document_extract`; link `term_document_understanding` / `term_ocr` / `term_multimodal` / `term_data_contract`. Not a new term. |
| DuckDuckGo / webSearchProviders contract | Documented in `oc_plugins_reference_duckduckgo`; link `term_information_retrieval` / `term_internal_search` / `term_data_contract`. Provider name is config, not a term note. Full tool doc in `tools/duckduckgo-search` (to03). |
| ClawHub / install route / surface / contract | OpenClaw plugin-system vocabulary; captured inline across notes 1–7; link `term_data_contract` / `term_npm` / sibling ClawHub sub-plans (cw01–cw03). Not new terms. |

**New-term candidates: NONE.** No genuinely reusable cross-cutting term lacks an existing note (observability, monitoring, IR, document understanding, channel adapter, tool registry, contract, OCR, multimodal all already exist and are linked). Augment Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** pl09 authors zero `term_dictionary` notes; it only links existing terms. Inherited from master (Undigested Terms — Corpus-Wide Inventory: OpenClaw vocab → `oc_*` doc notes; no term definition inlined in an `oc_*` note). Should augment Step 2d surface a genuinely reusable cross-cutting term with no existing note, capture it via `/tessellum-capture-term-note` and add it to the best-fit `acronym_glossary_*.md` (expected: none).

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P3). Gate table identical to the master's 9-GATE definition; all must pass before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format (`/tessellum-check-note-format` + `check_yaml_frontmatter.py`) | YAML field order/forbidden-fields clean; `# OpenClaw — …` H1; `## Overview`/`## Related Notes`/`## References`; bold `**Source**`/`**Last Updated**`/`**Status**` footer; no ERROR/LINK-003. |
| G2 | Grounding (diff vs `inbox/openclaw_docs/plugins/reference/<page>`) | Every distribution/surface/added-language/related-doc fact traces to the source page; no invented packages, contracts, or languages. |
| G3 | Density + Coverage | ≤400 lines, ≤2500 words, ≤6 code blocks, one `building_block: concept` per note; every source H2/H3 covered (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevance-selected `term_dictionary` links + sibling `oc_*` + `repo_openclaw*`, each with a relevance statement. |
| G6 | Broken-link fix (`/tessellum-fix-broken-links`) | 0 broken relative links after incremental reindex. |
| G7/G8 | Discoverability / in-degree ≥1 | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md`); anti-island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_diagnostics_otel oc_plugins_reference_diagnostics_prometheus oc_plugins_reference_diffs oc_plugins_reference_diffs_language_pack oc_plugins_reference_discord oc_plugins_reference_document_extract oc_plugins_reference_duckduckgo"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' && echo "FORMAT FAIL: $n"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec': $n"; done
  # source_url present in YAML
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"; }
  # at least one sibling oc_ cross-link
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NO SIBLING LINK: $n"
  # density caps
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb cb / $lines L)"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_diagnostics_otel | concept | 220 | 0 | ✅ |
| 2 | oc_plugins_reference_diagnostics_prometheus | concept | 210 | 0 | ✅ |
| 3 | oc_plugins_reference_diffs | concept | 210 | 0 | ✅ |
| 4 | oc_plugins_reference_diffs_language_pack | concept | 320 | 0 | ✅ |
| 5 | oc_plugins_reference_discord | concept | 230 | 0 | ✅ |
| 6 | oc_plugins_reference_document_extract | concept | 230 | 0 | ✅ |
| 7 | oc_plugins_reference_duckduckgo | concept | 210 | 0 | ✅ |

No note approaches any cap (all ≤320 words, 0 code fences, well under 400 lines / 2500 words / 6 fences). These are deliberately compact reference cards; the floor concern (over-compression) is N/A because the source pages are themselves 50–151-word stubs — the digest faithfully reproduces all source facts plus the required `## Overview` / `## Related Notes` / `## References` scaffolding.

## Entry Point Decision (inherited from master)

Contributes 7 rows to `entry_openclaw_docs.md` (created as the master W1 pre-step before any sub-plan executes), under a "Plugins → Reference (D-batch)" cluster. Each of the 7 notes receives its entry-point back-link at finalization (this is the G7/G8 inbound-link source). No separate entry point is created for this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfies G7/G8 in-degree ≥1):

- `entry_openclaw_docs.md` (master pre-step) → all 7 notes (primary inbound source).
- `repo_openclaw_extensions.md` → notes 1, 2, 3, 4, 6, 7 (the extension/plugin code home).
- `repo_openclaw_gateway.md` → notes 1, 2 (diagnostics exporters instrument the gateway runtime).
- `repo_openclaw_channels.md` + `repo_openclaw_channels_messaging.md` → note 5 (Discord channel plugin).
- `repo_openclaw_skills.md` → notes 3, 4 (diffs viewer skills surface).
- `repo_openclaw_extensions_llm_providers.md` → note 7 (provider-registration pattern).
- `term_observability_agent_systems.md` → notes 1, 2; `term_channel_adapter.md` → note 5; `term_document_understanding.md` → note 6; `term_information_retrieval.md` → note 7 (reciprocal term back-links).

## Pacing Rules (inherited from master)

One execution phase; 8 gates before commit. Re-read each of the 7 source pages at execution; reproduce distribution/surface/related-doc facts verbatim (0 code fences to reproduce). One BB (concept) per note. Cap dynamic-workflow fan-out ≤30 agents/run; `git pull --rebase --autostash` first; no Claude co-author trailer; reindex incrementally and verify `note_links` + 0 broken links before commit+push.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (plan `status: ready`) |

## Augmentation Report (2026-06-21)

**Scope**: xref-augment of pl09 (7 plugin-reference stub pages → 7 `concept` notes). Re-read all 7 source pages under `inbox/openclaw_docs/plugins/reference/` (diagnostics-otel, diagnostics-prometheus, diffs, diffs-language-pack, discord, document-extract, duckduckgo). All facts in the planned-notes table (package names, install routes, contract surfaces, added-language list, related-doc pointers) confirmed against source — no over-compression risk (sources are 25-121 body-words; the digest faithfully reproduces every distribution/surface/related-doc fact plus required scaffolding).


**Per-note counts**:

| Note | Terms | Snippets | Docs (existing / planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_diagnostics_otel | 8 | 10 | 11 (8 / 3) | 2 | ✅ |
| oc_plugins_reference_diagnostics_prometheus | 8 | 10 | 11 (8 / 3) | 2 | ✅ |
| oc_plugins_reference_diffs | 8 | 10 | 11 (8 / 3) | 2 | ✅ |
| oc_plugins_reference_diffs_language_pack | 8 | 10 | 11 (8 / 3) | 2 | ✅ |
| oc_plugins_reference_discord | 9 | 10 | 11 (8 / 3) | 2 | ✅ |
| oc_plugins_reference_document_extract | 8 | 10 | 11 (8 / 3) | 2 | ✅ |
| oc_plugins_reference_duckduckgo | 8 | 10 | 11 (8 / 3) | 2 | ✅ |


**New-term candidates**: NONE. Re-read Step 2d re-scan confirms every cross-cutting concept the source pages touch (observability, monitoring, distributed trace, context propagation, time-series DB, SLI/MTTR, channel adapter, messaging gateway, omnichannel, bot, channel kernel, websocket, tool registry, skills, atomic skill, function calling, tool descriptor, npm, markdown, document understanding, document VLM, multimodal, OCR, document automation, data contract, information retrieval, internal/hybrid search, deep research agent, provider plugin) already has a substantive `term_dictionary` note — all are LINKED, none promoted. Per master design decision, OpenClaw plugin vocabulary (plugin, ClawHub, surface, contract IDs, Shiki, Discord/DuckDuckGo as platform/provider names) is config/identity captured inline in the `oc_*` notes, never a new term note. Best-fit glossary: N/A (0 new terms; the agentic/LLM glossary is already rich).

**Issues / amendments**: None blocking. The mapping deliberately exceeds the master's plan-stage ≥6-term floor (now ≥8) and adds the ≥10-snippet / ≥10-doc floors; densities remain far under caps (each digest note ~210-320 words, 0 code fences). The collision/specificity audit (below) confirms no planned `oc_*` note duplicates an existing `term_*` or doc note.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review against the 9 mandatory checkpoints. Evidence is from the locked plan + DB verification + source re-read.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance-stated) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; every note ≥8 terms (note 5 = 9), ≥10 snippets, ≥10 docs; each link carries `— <what>; relevance: <why THIS note>`. No bare links. |
| CP2 | 9-GATE present per batch (G1-G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present for the single P3 phase; G5 ghost-detect + G6 broken-link-fix + G7/G8 discoverability all listed with pass criteria. |
| CP3 | Entry point update specified (inherited) | **PASS** | `## Entry Point Decision` inherits master W1 `entry_openclaw_docs.md` (created pre-step); contributes 7 rows under "Plugins → Reference (D-batch)"; each note gets its entry-point back-link (G7/G8 source). `entry_openclaw_docs.md` DB-checked = NOT yet present (correctly cited as planned W1). |
| CP4 | Plan size (≤30 or split) | **PASS** | 7 notes, single phase — well under 30. |
| CP5 | Note format aligned + DERIVED from existing | **PASS** | Master Format Definition derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` → source-mirrored H2/H3 → `## Related Notes` → `## References` → bold footer); same YAML field order + forbidden-field list; pl09 inherits verbatim. Confirmed against existing target-sibling docs in DB. |
| CP6 | Borderline density → split promoted | **PASS** | `## Density Re-Assessment`: all 7 notes 210-320 words, 0 code fences, far under ≤400L/≤2500w/≤6-fence caps. No borderline cases. Source pages are 25-121 body-words; no over-compression. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 source pages re-read 2026-06-21; `wc -w` body-only = 27/25/28/121/35/34/28 (plan's 54/50/55/151/63/62/50 incl. YAML frontmatter). Within range, not under-estimated — stub-class pages. |
| CP8 | Undigested Terms Plan + Authoring Reqs present | **PASS** | `## Undigested Terms Plan` (9-row disposition table, all → link existing or inline; New-term candidates: NONE) + `## Term-Note Authoring Requirements` (N/A, 0 new terms; inherited from master) both present. |
| CP8f | Term-slug / all-notes dedup + collision audit | **PASS** | 0 new term slugs → no specificity rename needed. Collision audit generalized to all 7 planned `oc_*` notes: each is a per-plugin reference card with a unique full-slug filename; none duplicates an existing `term_*` (terms are LINKED, not recreated) or existing doc note (no `openclaw/` docs exist yet). Naming Notes: — (audit performed, nothing flagged). |
| CP9 | Discoverability — inbound links executed (G8) | **PASS** | `## Inlinks (existing → new notes)` maps every one of the 7 notes to ≥1 outside-folder inbound source (entry_openclaw_docs → all 7; repo_openclaw_extensions → 1/2/3/4/6/7; repo_openclaw_gateway → 1/2; repo_openclaw_channels(+_messaging) → 5; repo_openclaw_skills → 3/4; repo_openclaw_extensions_llm_providers → 7; reciprocal term back-links). G7/G8 in the gate table; in-degree ≥1 verified at execution. |

**RESULT: 9/9 CP pass → READY FOR EXECUTION.** Plan `status` advanced `pending → ready`.
