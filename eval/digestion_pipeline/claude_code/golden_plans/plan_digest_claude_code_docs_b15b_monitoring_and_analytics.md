---
title: Sub-Plan B15B — Claude Code Docs: Monitoring & Analytics
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["monitoring-usage", "analytics"]
---

# Sub-Plan B15B: Monitoring & Analytics

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides. P3 (Phase C).

## Scope

The 2 enterprise observability pages: how to export Claude Code telemetry through OpenTelemetry
(metrics, logs/events, beta traces) to your own monitoring/SIEM stack, and how to read the hosted
analytics dashboards (Team/Enterprise + API Console) that track adoption, contribution, and spend.
`monitoring-usage.md` is a large reference page (9,858 words, ~70 sections) and is split heavily;
`analytics.md` is a compact product-feature page. P3 — references the context/permission/MCP/skill/hook
vocabulary defined by Phase-A sub-plans, so it links them rather than redefining them.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 2 pages, 11,448 measured words. **Planned: 9 notes.**

## Content Strategy

- **Prioritize**: the operator-facing setup path (env vars → exporters → endpoint) and the two big
  reference catalogs (metrics, events) that every dashboard/alert query depends on.
- **Group**: split `monitoring-usage` by signal type and task — setup (procedure) vs config-variable
  reference (concept) vs metrics catalog (concept) vs events catalog (concept) vs traces (concept) vs
  audit/SIEM (procedure) vs interpretation/backends (argument). Keep `analytics` as a dashboards pair
  (read-the-dashboard concept + PR-attribution algorithm concept).
- **Skip / link-out (own other sub-plans)**: env-var canonical reference → B03A (`settings.md`/`env-vars.md`);
  managed/policy settings precedence → B14B (`server-managed-settings.md`); permission modes & decision
  semantics → B05A; hooks payload schema → B07A; MCP transport/scope → B08A; cost/spend-limit guidance →
  B02A (`costs.md`); network mTLS canonical → B14B (`network-config.md`); data-usage/ZDR/telemetry-services
  → B16 (`data-usage.md`/`zero-data-retention.md`). These are referenced via links, never duplicated.
- **Glossary/terms**: no new `cc_` term re-digestion — observability terms route to existing
  `term_dictionary/` notes (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

Both pages re-read in full from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| monitoring-usage | /monitoring-usage | 9,858 | 9 | 9 | 60 | concept/procedure (reference) |
| analytics | /analytics | 1,590 | 0 | 3 | 19 | concept |

> H3 count for monitoring-usage includes `###` and `####` heading levels (the per-metric / per-event
> sub-sections). Code count is true ```` ``` ```` fence pairs (9 blocks: 5 bash, 3 json, 1 text).

> **H2 lists (document order):**
> - **monitoring-usage**: Quick start · Administrator configuration · Configuration details (H3 Common configuration variables, mTLS authentication, Metrics cardinality control, Traces (beta) [H4 Span hierarchy, Span attributes], Dynamic headers [H4 Settings configuration, Script requirements, Refresh behavior], Multi-team organization support, Example configurations) · Available metrics and events (H3 Standard attributes, Metrics, Metric details [H4 Session/Lines-of-code/Pull-request/Commit/Cost/Token/Code-edit-tool-decision/Active-time counters], Events [H4 Event correlation attributes + ~26 per-event sub-sections]) · Interpret metrics and events data (H3 Usage monitoring, Cost monitoring, Alerting and segmentation, Detect retry exhaustion, Event analysis) · Audit security events (H3 Attribute actions to users, Audit MCP activity, Map security questions to events, Send events to a SIEM) · Backend considerations (H3 For metrics, For events/logs, For traces) · Service information · ROI measurement resources · Security and privacy · Monitor Claude Code on Amazon Bedrock
> - **analytics**: Access analytics for Team and Enterprise (H3 Enable contribution metrics, Review summary metrics, Explore the charts [H4 Track adoption, Measure PRs per user, View pull requests breakdown, Find top contributors], PR attribution [H4 Tagging criteria, Attribution process, Time window, Excluded files, Attribution notes], Get the most from analytics [H4 Monitor adoption, Measure ROI, Identify power users, Access data programmatically]) · Access analytics for API customers (H3 View team insights) · Related resources

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. Prefix `cc_`, target
`resources/documentation/claude_code/`. **9 notes** (master estimate was 7; the two reference catalogs —
metrics and events — plus traces force the split to stay under the density caps; see Split Decisions).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_monitoring_opentelemetry_setup.md` | procedure | monitoring-usage: Quick start, Administrator configuration, Example configurations, Service information | 550 | How to turn on OTel telemetry: `CLAUDE_CODE_ENABLE_TELEMETRY=1`, choose exporters, set OTLP endpoint/auth; managed-settings (MDM) fleet rollout; per-scenario export blocks; service-info resource attributes. Env-var canon → B03A; managed settings → B14B. |
| 2 | `cc_otel_configuration_variables.md` | concept | monitoring-usage: Configuration details — Common config vars, mTLS, Metrics cardinality control, Dynamic headers, Multi-team org support | 600 | The OTel configuration knobs: common OTLP variables (protocol/endpoint/intervals/per-signal overrides), mTLS client-cert variables per protocol, cardinality-control toggles, the `otelHeadersHelper` dynamic-header script + refresh, and `OTEL_RESOURCE_ATTRIBUTES` multi-team labels. mTLS canon → B14B. |
| 3 | `cc_otel_metrics_reference.md` | concept | monitoring-usage: Available metrics and events — Standard attributes, Metrics, Metric details | 650 | The 8 exported metrics (session/lines-of-code/PR/commit/cost/token/code-edit-decision/active-time counters) with their per-metric attributes, plus the standard attribute set shared by all metrics and events. |
| 4 | `cc_otel_events_reference.md` | concept | monitoring-usage: Available metrics and events — Events (correlation attributes + ~26 event types) | 700 | The logs/events catalog: `prompt.id` correlation, then the event families — prompt/tool/API (request/error/refusal/body/retries), tool_decision, permission_mode_changed, auth, MCP connection, internal_error, plugin installed/loaded, skill_activated, at_mention, hook registered/start/complete/plugin-metrics, compaction, feedback_survey. |
| 5 | `cc_otel_traces.md` | concept | monitoring-usage: Configuration details — Traces (beta) (Span hierarchy, Span attributes) | 550 | Beta distributed tracing: enable flags (`CLAUDE_CODE_ENHANCED_TELEMETRY_BETA`, `OTEL_TRACES_EXPORTER`), the `claude_code.interaction` span tree, W3C `traceparent`/`TRACEPARENT` propagation in/out, and per-span attribute tables. |
| 6 | `cc_otel_audit_and_siem.md` | procedure | monitoring-usage: Audit security events — Attribute actions to users, Audit MCP activity, Map security questions to events, Send events to a SIEM | 550 | Using the event stream as an audit source: identity attributes per event, `OTEL_LOG_TOOL_DETAILS` for full MCP/Bash detail, the security-question→event mapping table, and pointing the logs exporter at a SIEM. Permission semantics → B05A; data-usage → B16. |
| 7 | `cc_otel_analysis_and_privacy.md` | argument | monitoring-usage: Interpret metrics and events data, Backend considerations, ROI measurement resources, Security and privacy, Monitor on Amazon Bedrock | 550 | How to use the data and its trade-offs: usage/cost/alerting analyses, retry-exhaustion detection, backend selection by signal type, and the opt-in privacy model (default redaction; what each `OTEL_LOG_*` flag exposes). Cost guidance → B02A; data-usage/ZDR → B16; Bedrock → B14A. |
| 8 | `cc_analytics_dashboards.md` | concept | analytics: intro table, Access for Team/Enterprise (summary metrics + charts), Access for API customers (team insights), Related resources | 600 | The two hosted analytics dashboards: Team/Enterprise (`claude.ai/analytics/claude-code`) usage+contribution+leaderboard+CSV export, and API Console (`platform.claude.com/claude-code`) usage+spend+team-insights; roles, the summary metric definitions, and the trend charts. |
| 9 | `cc_pr_attribution.md` | concept | analytics: Enable contribution metrics, PR attribution (tagging/process/time-window/excluded-files/notes), Get the most from analytics | 450 | How merged PRs get tagged `claude-code-assisted`: GitHub-app setup, the conservative matching algorithm (extract→match→normalize), 21-day window, excluded auto-generated files, >20%-rewrite exclusion; and the ROI/adoption/power-user reading guidance. ZDR limitation → B16. |

**Estimate: 9 notes** — concept ×6 (notes 3,4,5,8,9 + cfg note 2), procedure ×2 (notes 1,6), argument ×1 (note 7). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 2 (11,448 words). New `cc_` notes: 9. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~5,200 (avg ~580/note). Code blocks: distributed from the 9 source blocks
  (setup note carries the most; events/metrics/analytics notes are table-only, 0 code).
- **Building Block Distribution**: concept ×6 (notes 2,3,4,5,8,9) · procedure ×2 (notes 1,6) · argument ×1 (note 7). No model/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_monitoring_opentelemetry_setup` (6 term notes)
- [Observability in Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — What it is: the practice of instrumenting LLM-agent systems with metrics/logs/traces; relevance: this note IS the entry point for making Claude Code observable, exporting exactly that telemetry triad.
- [OpenTelemetry / Time-Series Database](../../term_dictionary/term_time_series_database.md) — What it is: a store optimized for timestamped metric series (Prometheus-style); relevance: the metrics exporter this setup configures emits time-series data the operator points at such a backend.
- [CloudWatch](../../term_dictionary/term_cloudwatch.md) — What it is: AWS metrics/logs observability service; relevance: a representative managed backend an operator can target with the OTLP endpoint this note sets, grounding "configure your backend".
- [EMF (Embedded Metric Format)](../../term_dictionary/term_emf.md) — What it is: a structured metric-emission format for log-based metrics; relevance: contextualizes the exporter-format choice (otlp/prometheus/console) this setup makes when wiring metrics into a pipeline.
- [Data Observability](../../term_dictionary/term_data_observability.md) — What it is: monitoring data-pipeline health/freshness/volume; relevance: the export interval and exporter selection in this setup are the data-observability plumbing that keeps the telemetry feed healthy.
- [Claude Code](../../term_dictionary/term_claude_code.md) — What it is: the agentic coding tool; relevance: this note documents how to enable telemetry on Claude Code itself via `CLAUDE_CODE_ENABLE_TELEMETRY` and the `claude-code` service resource attributes.

### 2. `cc_otel_configuration_variables` (6 term notes)
- [Observability in Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — What it is: instrumenting agent systems with telemetry; relevance: every variable in this note (exporter, endpoint, cardinality, headers, resource attributes) is an observability-configuration knob for the Claude Code agent.
- [Context Propagation](../../term_dictionary/term_context_propagation.md) — What it is: carrying request/trace context across service boundaries; relevance: the per-signal OTLP overrides and `OTEL_RESOURCE_ATTRIBUTES` labels this note covers are how Claude Code propagates identity/team context into the telemetry backend.
- [mTLS / IAM](../../term_dictionary/term_iam.md) — What it is: identity-and-access management primitives; relevance: the mTLS client-certificate variables and dynamic-header (bearer-token) auth this note documents are the access-control layer guarding the telemetry endpoint.
- [Time-Series Database](../../term_dictionary/term_time_series_database.md) — What it is: a metrics store keyed by time; relevance: the cardinality-control toggles in this note (session.id, account_uuid, resource attributes) directly trade off storage cost/query performance in such a backend.
- [Trust Policy](../../term_dictionary/term_trust_policy.md) — What it is: a policy declaring who/what may assume access; relevance: contextualizes the mTLS CA-trust variables (`NODE_EXTRA_CA_CERTS`, `OTEL_EXPORTER_OTLP_CERTIFICATE`) that establish which collector certificate the exporter trusts.

### 3. `cc_otel_metrics_reference` (6 term notes)
- [Observability in Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — What it is: telemetry instrumentation for agents; relevance: this note is the catalog of the eight metrics that constitute Claude Code's observable surface (sessions, tokens, cost, code lines, decisions, active time).
- [Time-Series Database](../../term_dictionary/term_time_series_database.md) — What it is: a timestamped-metric store; relevance: each counter in this note is a metric series the operator queries in a time-series backend, and the standard attributes become its labels.
- [Session ID](../../term_dictionary/term_sessionid.md) — What it is: a unique per-session identifier; relevance: `session.id` is the primary standard attribute in this note's metric label set and the join key for per-session breakdowns the catalog enables.
- [Langfuse](../../term_dictionary/term_langfuse.md) — What it is: an LLM observability platform tracking token usage and cost; relevance: a representative consumer for this note's `token.usage` and `cost.usage` counters and their model/skill/agent attribution.
- [AARRR Pirate Metrics](../../term_dictionary/term_aarrr_pirate_metrics.md) — What it is: an adoption/retention metrics framework; relevance: this note's `session.count` and `active_time.total` are the activation/engagement signals an adoption analysis (pirate-metrics style) is built on.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — What it is: the model invoking tools and getting results back; relevance: the code-edit-tool-decision counter in this note records accept/reject outcomes of exactly these tool-use calls.

### 4. `cc_otel_events_reference` (6 term notes)
- [Observability in Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — What it is: agent telemetry instrumentation; relevance: this note is the events half of Claude Code's observable surface — the structured log/event stream every audit and analysis query reads.
- [Session ID](../../term_dictionary/term_sessionid.md) — What it is: a per-session identifier; relevance: `session.id` plus the per-event `event.sequence` are how this note's ~26 event types are grouped and ordered within a session.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — What it is: model tool invocation; relevance: the `tool_result` and `tool_decision` events catalogued here record the lifecycle and accept/reject outcome of each tool-use call, joined by `tool_use_id`.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — What it is: the open protocol for connecting external tools; relevance: this note documents the `mcp_server_connection` event and MCP attribution on tool/API events (server/tool names, transport, scope).
- [Skills](../../term_dictionary/term_skills.md) — What it is: packaged repeatable Claude Code workflows; relevance: the `skill_activated` event and `skill.name` attribution this note catalogs track when and how skills fire across a fleet.
- [Compaction](../../term_dictionary/term_compaction.md) — What it is: summarizing conversation history to reclaim context; relevance: this note documents the `compaction` event (trigger, pre/post tokens, precompute-reuse) emitted when Claude Code compacts.

### 5. `cc_otel_traces` (7 term notes)
- [Trace](../../term_dictionary/term_trace.md) — What it is: an end-to-end record of a request as a tree of timed spans; relevance: this note IS Claude Code's distributed-tracing export — the `claude_code.interaction` root and its child spans form exactly such a trace.
- [Context Propagation](../../term_dictionary/term_context_propagation.md) — What it is: passing trace context across process/service boundaries; relevance: the W3C `traceparent`/`TRACEPARENT`/`TRACESTATE` in-and-out propagation this note details is textbook trace-context propagation through subprocesses and the API.
- [Observability in Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — What it is: agent telemetry instrumentation; relevance: tracing is the third telemetry signal (after metrics/logs) this note adds, giving per-prompt request waterfalls for the agent.
- [X-Ray](../../term_dictionary/term_xray.md) — What it is: AWS distributed-tracing service; relevance: a representative tracing backend that ingests the OTLP spans this note's exporter emits, grounding "view a full request as a single trace".
- [Microservices Architecture](../../term_dictionary/term_microservices_architecture.md) — What it is: a system of small independently-deployed services; relevance: distributed tracing exists to follow a request across such boundaries — the same pattern this note uses to link prompt → API request → tool subprocess.
- [Subagent](../../term_dictionary/term_subagent.md) — What it is: an isolated-context Claude Code worker spawned by the Agent tool; relevance: this note describes how a subagent's API/tool spans nest under the parent's `claude_code.tool` span via `agent_id`/`parent_agent_id`.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — What it is: model tool invocation; relevance: each `claude_code.tool` span in this note's hierarchy wraps one tool-use call, with child spans for permission-wait and execution.

### 6. `cc_otel_audit_and_siem` (7 term notes)
- [AAA (Authentication, Authorization, Accounting)](../../term_dictionary/term_aaa.md) — What it is: the identity-security triad of who-you-are / what-you-may-do / what-you-did; relevance: this note turns Claude Code events into the "accounting"/audit leg — every event carries the identity that tie actions to a user.
- [Delegated Identity](../../term_dictionary/term_delegated_identity.md) — What it is: acting under an end-user's identity rather than a service account; relevance: this note states Claude Code records the developer's own account identity on each event (no separate service account), the delegated-identity audit model.
- [IAM](../../term_dictionary/term_iam.md) — What it is: identity-and-access management; relevance: the `user.email`/`user.account_id`/`organization.id` attributes this note uses for attribution are the IAM identity facets carried on the audit stream.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — What it is: progressive permission escalation in Claude Code; relevance: this note's security-question table maps `permission_mode_changed` and `tool_decision` events — the audit trail of how much trust was granted.
- [Observability in Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — What it is: agent telemetry; relevance: this note repurposes the same OTLP logs exporter as a SIEM feed, the security-monitoring application of agent observability.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — What it is: the external-tool protocol; relevance: this note's "Audit MCP activity" section shows how `OTEL_LOG_TOOL_DETAILS=1` surfaces MCP server/tool names and call arguments for security review.
- [Service Principal](../../term_dictionary/term_service_principal.md) — What it is: a non-human identity used by an application/service; relevance: this note explicitly contrasts Claude Code's developer-identity model against acting as a service principal, the distinction an auditor must understand.

### 7. `cc_otel_analysis_and_privacy` (6 term notes)
- [Observability in Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — What it is: agent telemetry instrumentation; relevance: this note is the "now-use-the-data" layer — usage/cost/alerting analyses and backend selection over the metrics and events the other notes export.
- [Time-Series Database](../../term_dictionary/term_time_series_database.md) — What it is: a metrics store keyed by time; relevance: this note's backend-considerations section recommends time-series stores (Prometheus) for rate/aggregation analyses of the cost and token metrics.
- [PII (Personally Identifiable Information)](../../term_dictionary/term_pii.md) — What it is: data that can identify an individual; relevance: this note's privacy model centers on what the `OTEL_LOG_*` flags expose — `user.email`, prompts, tool arguments — i.e. potential PII the operator must redact.
- [Personal Data](../../term_dictionary/term_personal_data.md) — What it is: any data relating to an identifiable person (GDPR sense); relevance: the opt-in redaction defaults this note documents (prompts/tool detail off by default) are personal-data minimization controls the operator tunes.
- [Langfuse](../../term_dictionary/term_langfuse.md) — What it is: an LLM observability platform; relevance: a representative full-featured backend for the cost/token interpretation and ROI reporting this note describes.
- [Claude Code](../../term_dictionary/term_claude_code.md) — What it is: the agentic coding tool; relevance: this note's ROI/Bedrock-monitoring guidance and privacy guarantees are about Claude Code's own telemetry footprint and how to reason about it.

### 8. `cc_analytics_dashboards` (6 term notes)
- [AARRR Pirate Metrics](../../term_dictionary/term_aarrr_pirate_metrics.md) — What it is: an adoption/activation/retention metrics framework; relevance: this note's dashboard surfaces exactly these — daily active users, sessions, accept rate, leaderboard — the activation/engagement funnel for Claude Code rollout.
- [Observability in Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — What it is: agent telemetry/monitoring; relevance: these hosted dashboards are the no-setup observability path (vs the self-hosted OTel pipeline), surfacing usage/spend metrics for the agent.
- [Langfuse](../../term_dictionary/term_langfuse.md) — What it is: an LLM observability platform tracking token usage and cost; relevance: the API Console dashboard's per-user spend and accepted-lines metrics in this note are the same usage/cost lens such a platform provides.
- [Data Maturity Model](../../term_dictionary/term_data_maturity_model.md) — What it is: stages of an org's analytics capability; relevance: this note's CSV export and "use alongside DORA/sprint velocity" guidance position the dashboard as an input to higher-maturity engineering-metrics practice.
- [Session ID](../../term_dictionary/term_sessionid.md) — What it is: a per-session identifier; relevance: the "sessions" and "daily active users" the dashboards in this note chart are aggregations over sessions, the unit of activity counted.
- [Claude Code](../../term_dictionary/term_claude_code.md) — What it is: the agentic coding tool; relevance: this note documents Claude Code's own hosted analytics product surfaces (Team/Enterprise and API Console dashboards).

### 9. `cc_pr_attribution` (6 term notes)
- [Observability in Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — What it is: agent telemetry/measurement; relevance: PR attribution is the contribution-measurement mechanism behind the dashboards — matching session activity to merged code to quantify the agent's impact.
- [User Forks](../../term_dictionary/term_user_forks.md) — What it is: per-user copies/branches of a repository in a Git workflow; relevance: contextualizes this note's PR-diff matching, which extracts added lines from merged pull requests across branches to attribute authorship.
- [Docs as Code](../../term_dictionary/term_docs_as_code.md) — What it is: managing content through Git PR workflows; relevance: this note's `claude-code-assisted` GitHub label and PR-diff line matching operate on the same PR-based version-control workflow.
- [AARRR Pirate Metrics](../../term_dictionary/term_aarrr_pirate_metrics.md) — What it is: an adoption/retention metrics framework; relevance: this note's "Get the most from analytics" ROI/adoption/power-user guidance turns attributed PRs and lines into the activation/retention signals such a framework tracks.
- [Data Maturity Model](../../term_dictionary/term_data_maturity_model.md) — What it is: stages of analytics capability; relevance: the conservative, normalized, time-windowed attribution algorithm this note describes (and its programmatic CSV/label access) is a structured-measurement practice at the higher maturity stages.
- [Claude Code](../../term_dictionary/term_claude_code.md) — What it is: the agentic coding tool; relevance: this note documents how Claude Code attributes merged-PR lines to its own assistance via session-activity matching.

## Section Coverage Map

```
monitoring-usage.md
├── Quick start ──────────────────────────── → note 1 (cc_monitoring_opentelemetry_setup)
├── Administrator configuration ──────────── → note 1 (managed settings → B14B link-out)
├── Configuration details
│   ├── Common configuration variables ───── → note 2 (cc_otel_configuration_variables)
│   ├── mTLS authentication ──────────────── → note 2 (mTLS canon → B14B link-out)
│   ├── Metrics cardinality control ──────── → note 2
│   ├── Traces (beta) ────────────────────── → note 5 (cc_otel_traces)
│   │   ├── Span hierarchy ───────────────── → note 5
│   │   └── Span attributes ──────────────── → note 5
│   ├── Dynamic headers (+ 3 H4) ─────────── → note 2
│   ├── Multi-team organization support ──── → note 2
│   └── Example configurations ───────────── → note 1
├── Available metrics and events
│   ├── Standard attributes ──────────────── → note 3 (cc_otel_metrics_reference) [shared, defined here, linked from note 4]
│   ├── Metrics + Metric details (8 counters) → note 3
│   └── Events (correlation + ~26 events) ── → note 4 (cc_otel_events_reference)
├── Interpret metrics and events data ────── → note 7 (cc_otel_analysis_and_privacy)
│   ├── Usage/Cost/Alerting/Retry/Event-analysis (5 H3) → note 7
├── Audit security events ────────────────── → note 6 (cc_otel_audit_and_siem)
│   ├── Attribute to users/Audit MCP/Map-questions/Send-to-SIEM (4 H3) → note 6
├── Backend considerations (metrics/events/traces) → note 7
├── Service information ───────────────────── → note 1
├── ROI measurement resources ────────────── → note 7
├── Security and privacy ─────────────────── → note 7
└── Monitor Claude Code on Amazon Bedrock ── → note 7 (→ B14A link-out)
analytics.md
├── (intro: dashboard access table) ──────── → note 8 (cc_analytics_dashboards)
├── Access analytics for Team and Enterprise → note 8
│   ├── Enable contribution metrics ──────── → note 9 (cc_pr_attribution) (GitHub-app setup; ZDR → B16)
│   ├── Review summary metrics ───────────── → note 8
│   ├── Explore the charts (4 H4) ────────── → note 8
│   ├── PR attribution (5 H4) ────────────── → note 9
│   └── Get the most from analytics (4 H4) ─ → note 9
├── Access analytics for API customers ───── → note 8
│   └── View team insights ───────────────── → note 8
└── Related resources ────────────────────── → notes 7/8 (links: monitoring, costs B02A, permissions B05A)
```
No orphaned sections. (`Standard attributes` is defined once in note 3 and referenced by note 4 — single owner, not duplicated.)

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| monitoring-usage (9,858w >2,500, ~70 sections) | notes 1–7 + 8 link-outs | far exceeds the density cap; distinct BB/tasks: setup (procedure) vs config-var reference (concept) vs metrics catalog (concept) vs events catalog (concept) vs traces (concept) vs audit/SIEM (procedure) vs interpret+backends+privacy (argument). env-vars/managed-settings/mTLS/permissions/MCP/cost/data-usage owned by B03A/B14B/B05A/B08A/B02A/B16. |
| monitoring-usage → metrics vs events | note 3 vs note 4 | the two reference catalogs each approach ~650–700w; keeping them in one note would exceed the cap and mix two distinct concept domains (counters vs log events). |
| monitoring-usage → Traces (beta) | note 5 (standalone) | distinct concept (distributed tracing + W3C context propagation) with its own enable path and span-attribute tables; separable from the metrics/events catalogs. |
| analytics (1,590w, 19 H3/H4) | notes 8, 9 | read-the-dashboard surfaces (concept) vs the PR-attribution algorithm + ROI reading guidance (concept); separable concerns, and splitting keeps each note focused even though the page is under the word cap. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_monitoring_opentelemetry_setup | procedure | 550 | 5 | ✅ |
| 2 | cc_otel_configuration_variables | concept | 600 | 2 | ✅ |
| 3 | cc_otel_metrics_reference | concept | 650 | 0 | ✅ |
| 4 | cc_otel_events_reference | concept | 700 | 0 | ✅ |
| 5 | cc_otel_traces | concept | 550 | 1 | ✅ |
| 6 | cc_otel_audit_and_siem | procedure | 550 | 2 | ✅ |
| 7 | cc_otel_analysis_and_privacy | argument | 550 | 0 | ✅ |
| 8 | cc_analytics_dashboards | concept | 600 | 0 | ✅ |
| 9 | cc_pr_attribution | concept | 450 | 0 | ✅ |

No note approaches the caps (≤2,500w / ≤6 code / ≤400 lines). Notes 3 and 4 are the largest (table-heavy
reference catalogs) but stay well under the word cap because attributes are condensed into tables, not prose.
Note 1 carries 5 of the 9 source code blocks (quick-start, managed-settings JSON, example-config bash,
service-info) and remains under the 6-code cap. No over-compression — every H2/H3/H4 maps to a note or an
explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_monitoring_opentelemetry_setup cc_otel_configuration_variables cc_otel_metrics_reference cc_otel_events_reference cc_otel_traces cc_otel_audit_and_siem cc_otel_analysis_and_privacy cc_analytics_dashboards cc_pr_attribution"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] && echo "DENSITY WARNING: $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$CC"
# G5 ghost: verify every internal .md link target exists in the DB
for n in $NOTES; do f="$CC/$n.md"
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/.*\(([^)]+)\)/\1/' | while read l; do
    r=$(cd "$(dirname "$f")" && realpath -q -m "$l"); id=${r#*/the vault/}
    sqlite3 "$(python3 -c 'import sys;sys.path.insert(0,"scripts");from config import DB_PATH_STR;print(DB_PATH_STR)')" \
      "SELECT 1 FROM notes WHERE note_id='$id'" | grep -q 1 || echo "GHOST $n -> $l"
  done; done
```

## Per-Phase Validation Gate (G1–G8) — inherited from master

Single phase (9 notes, all P3). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination (esp. env-var names, defaults, event names) | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3/H4 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 9 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 9 notes receives ≥1 inbound link from a vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound) | confirm in-degree ≥1 per note post-execution; no graph islands | DB in-degree ≥1 query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets
`0_entry_points/entry_claude_code_docs.md`; this sub-plan **contributes its 9 rows** under a
"Monitoring & Analytics" cluster + increments the BB-distribution counts (concept ×6, procedure ×2,
argument ×1). The entry-point back-link is added to each note at finalization (G7/G8).

## Undigested Terms Plan (Step 4e)

b15b creates **no new `term_dictionary` notes** — observability/security vocabulary surfaced by these pages
is covered by an existing substantive term note (link) or is a Claude Code feature term owned by its home
sub-plan (Pattern B; dedup checked across `term_dictionary/` AND `documentation/`):

| Surfaced term | Disposition |
|---|---|
| OpenTelemetry / OTLP / telemetry | link `term_observability_agent_systems` + `term_data_observability` (concept covered; no standalone OTel term note needed — generic vendor protocol, would duplicate observability terms) |
| Distributed tracing / span / traceparent | link `term_trace` + `term_context_propagation` (exist) |
| Metric / time-series / cardinality | link `term_time_series_database` (exists) |
| SIEM / audit / identity attribution | link `term_aaa` + `term_delegated_identity` + `term_iam` (exist) |
| Token usage / cost / spend | link `term_langfuse` (exists) + cost canon → B02A `costs.md` |
| PR attribution / lines of code / leaderboard | concept in notes 8/9 (analytics product feature; no term note) |
| DAU/WAU/MAU / adoption / ROI | link `term_aarrr_pirate_metrics` + `term_data_maturity_model` (exist) |
| Prompt content / tool detail / PII redaction | link `term_pii` + `term_personal_data` (exist); data-usage canon → B16 |
| Permission mode / tool decision / hook / MCP / skill / compaction / subagent / plugin | existing term notes (link) or owned by home sub-plan (B05A/B07A/B08A/B06/B02A/B10A/B09A) — captured there, referenced here as event attributes only |

**Augmentation Step 2d re-scan (2026-06-13):** re-read both pages in full, scanning emphasis/tables/captions
for newly-surfaced terms. The candidate generic terms (OpenTelemetry, OTLP, SIEM, mTLS) are vendor/standard
infrastructure, not Claude Code vocabulary, and are already covered by existing observability/identity term
notes — capturing them would duplicate `term_observability_agent_systems`/`term_trace`/`term_iam` (the exact
P0 over-capture failure the master's dedup policy guards against). **0 new B15B `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B15B authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do these pages' concepts duplicate existing notes?)

## Term-Note Authoring Requirements

**N/A for b15b** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory (esp. exact env-var
  names, default values, and the ~26 event names/attributes, which are error-prone to paraphrase).
- Code blocks verbatim from source. One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8, in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_observability_agent_systems.md` | notes 1, 3, 4 | agent-observability term → CC OTel setup / metrics / events catalogs |
| `term_dictionary/term_trace.md` | note 5 | trace term → CC distributed-tracing (beta) treatment |
| `term_dictionary/term_aaa.md` | note 6 | AAA/accounting term → CC audit-events-as-SIEM-source |
| `term_dictionary/term_langfuse.md` | notes 3, 8 | LLM-observability term → CC token/cost metrics + analytics dashboards |
| `term_dictionary/term_aarrr_pirate_metrics.md` | notes 8, 9 | adoption-metrics term → CC analytics dashboards + PR attribution ROI |
| `term_dictionary/term_claude_code.md` | notes 1, 8 | product term → CC monitoring setup + hosted analytics surfaces |

## Follow-up Recommendations

- After the 9 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 9
  rows for `entry_claude_code_docs.md` (Monitoring & Analytics cluster); `/tessellum-check-broken-links`.
- Verify the env-var names in notes 1/2/5 against the canonical `env-vars.md` digest (B03A) once it lands;
  cross-link rather than duplicate the variable reference.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B15B, 2026-06-13)

- **Source re-read (Step 2)**: both pages re-read in full from `inbox/claude_code_docs/`; measured words
  match the master figures (monitoring-usage 9,858 · analytics 1,590 = 11,448). monitoring-usage is ~70
  sections (9 H2, 60 H3/H4, 9 code blocks) and far over the 2,500-word cap → split into 7 notes; analytics
  (1,590w, 0 code) → 2 notes. No >1.5× under-estimate of the master's per-page figures.
- **Notes**: 9 (concept 6, procedure 2, argument 1) — 2 over the master's 7 estimate, justified by the two
  reference catalogs (metrics, events) and standalone traces each needing their own note to stay under caps.
  All splits documented in Split Decisions.
- **Per-Note Related Notes Mapping (Step 8)**: 6–7 relevancy-selected term notes per note (30 distinct
- **Dedup (Step 2b across term_dictionary AND documentation/)**: no existing `cc_` monitoring/analytics/
  telemetry/trace note (the `claude_code/` folder does not yet exist); the generic infra terms (OpenTelemetry,
  SIEM, mTLS) are already covered by existing observability/identity term notes → linked, not recreated.
- **Step 2d new-term scan**: candidates (OpenTelemetry, OTLP, SIEM, mTLS) are vendor/standard infra, covered
  by existing terms → **0 new B15B term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G5 verification note, G7/G8 discoverability gate rows.
- **28-item checklist**: PASS (term-note items N/A — B15B authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented; reviewed below and set to `ready`.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability (in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B15B contributes 9 rows under a Monitoring & Analytics cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 9 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes) exactly; body uses `## Overview` / source-mirrored H2s / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | Notes 3/4 (650/700w) are the largest; both well under 2,500w (table-condensed). monitoring-usage split into 7; analytics into 2. None borderline. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` measured: monitoring-usage 9,858 = master 9,858-implied (sub-plan total 11,448); analytics 1,590; total 11,448 = master Sub-Plans-Index 11,448. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B15B authors 0 term notes; Undigested Terms Plan routes all observability/security/analytics terms (link existing or home sub-plan); Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented — all 30 referenced terms exist and are linked, not recreated; generic infra terms (OpenTelemetry/SIEM/mTLS) deliberately NOT captured to avoid duplicating `term_observability_agent_systems`/`term_trace`/`term_iam`. |
| CP9 | Discoverability (G7/G8) executed-inlinks plan | ✅ PASS | Inlinks table maps ≥1 inbound link per note from outside `claude_code/` (6 existing term notes → all 9 new notes); verified at finalization by DB in-degree ≥1. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `ready`.
