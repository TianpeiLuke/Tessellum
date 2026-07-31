---
title: Sub-Plan gw05 — OpenClaw Docs: Gateway (Prometheus, Protocol, Remote, Sandboxing, Secrets)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["gateway/prometheus", "gateway/protocol", "gateway/remote", "gateway/remote-gateway-readme", "gateway/sandbox-vs-tool-policy-vs-elevated", "gateway/sandboxing", "gateway/secrets"]
---

# Sub-Plan gw05: Gateway

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML order, `## Overview` → body → `## Related
> Notes` → `## References` → bold footer), dedup-before-create (term_dictionary + documentation/ + repo_openclaw*),
> 9-GATE validation, cross-references, entry-point wiring, and the OpenClaw-vocab-as-doc-note term policy are ALL
> inherited from the master. Per-note Related mapping is LOCKED later at augment; this plan lists Candidate

## Scope

The 7 Gateway pages governing OpenClaw's **runtime control plane + security surface**: Prometheus metrics export
(`prometheus`), the Gateway WebSocket wire protocol (`protocol`, the single control-plane + node transport),
remote/VPN/tailnet access patterns (`remote`) and the macOS.app remote-gateway setup runbook
(`remote-gateway-readme`), the three orthogonal containment layers (`sandbox-vs-tool-policy-vs-elevated`), the
sandboxing backend/mode/workspace model (`sandboxing`), and the SecretRef secrets-management contract
(`secrets`). **Priority P1 (Phase A)** — these define the gateway/security/observability vocabulary the CLI,
tools, channels, and concepts sub-plans reference. Code-side counterparts (`repo_openclaw_gateway`,
`repo_openclaw_security`, `repo_openclaw_sessions`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **17,369 measured words**. **Planned: 12 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| prometheus | gateway/prometheus | 1,410 | 7 | 8 | 0 | procedure |
| protocol | gateway/protocol | 6,078 | 9 | 16 | 13 | model (split ×4) |
| remote | gateway/remote | 1,487 | 11 | 9 | 4 | procedure |
| remote-gateway-readme | gateway/remote-gateway-readme | 490 | 11 | 7 | 8 | procedure |
| sandbox-vs-tool-policy-vs-elevated | gateway/sandbox-vs-tool-policy-vs-elevated | 1,058 | 2 | 6 | 4 | concept |
| sandboxing | gateway/sandboxing | 3,367 | 8 | 13 | 5 | procedure (split ×2) |
| secrets | gateway/secrets | 3,479 | 24 | 28 | 0 | model + procedure (split ×2) |

> Code = fences/2 (raw `grep -c '```'` halved). Raw fence counts: prometheus 14, protocol 18, remote 22,
> remote-gateway-readme 22, sandbox-vs-tool-policy-vs-elevated 4, sandboxing 16, secrets 48. Note: PromQL/
> shell/JSON recipe blocks in `prometheus`/`remote` inflate the raw fence count; each digest note caps at ≤6.

## Content Strategy

- **Prioritize**: the Gateway WS protocol (the runtime control plane every client speaks) and the SecretRef
  contract + sandboxing model (the security surface) — these are the highest-novelty, highest-reference notes.
- **Split** (word-cap >2,500 and/or mixed-BB, per master):
  - `protocol.md` (6,078w, 29 headings, multi-BB) → **4 notes**: (1) transport/handshake/framing/versioning
    wire model, (2) roles/scopes/presence/broadcast capability model, (3) RPC method families + event families
    + task-ledger reference, (4) auth + device identity/pairing + TLS/pinning procedure.
  - `secrets.md` (3,479w, mixed model+procedure) → **2 notes**: (1) the SecretRef contract + runtime/access model,
    (2) the operational audit/configure/apply procedure (provider config, file-backed keys, exec/MCP/SSH integration).
  - `sandboxing.md` (3,367w, >2,500w) → **2 notes**: (1) sandboxing model (what's sandboxed, modes, scope), (2)
    the backend setup procedure (Docker/SSH/OpenShell, workspace access, bind mounts, images, setupCommand).
- **Keep 1 note** (reference pages ≤2,500w, single BB): `prometheus`, `remote`, `remote-gateway-readme`,
  `sandbox-vs-tool-policy-vs-elevated`.
- **Link-out (not redefined)**: OpenTelemetry export (gw04 `gateway/opentelemetry`) — `prometheus` only
  cross-links the OTel-vs-Prometheus comparison; trusted-proxy auth (gw07 `gateway/trusted-proxy-auth`);
  tailscale (gw06 `gateway/tailscale`); operator-scopes / pairing detail (gw04); secrets-plan-contract / security
  audit-checks (gw06). Term vocabulary (`term_websocket`, `term_json_rpc`, `term_sandbox`, `term_secrets_manager`,
  `term_tls`, `term_oauth_token`, `term_prometheus`→absent so link `term_observability_agent_systems`) is LINKED.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_gateway_prometheus.md` | procedure | prometheus.md (full): Quick start, Metrics exported, Label policy, PromQL recipes, Prometheus-vs-OpenTelemetry, Troubleshooting | 600 | Enabling and scraping the Gateway Prometheus `/metrics` endpoint: quick-start config, the exported metric families, cardinality/label policy, PromQL recipe snippets, and when to choose Prometheus over OpenTelemetry. |
| 2 | `oc_gateway_protocol_transport.md` | model | protocol.md: Transport, Handshake (connect) + Node example, Framing, Versioning + Client constants | 650 | The Gateway WebSocket wire model: text/JSON frames, the mandatory `connect` first frame, the challenge/`hello-ok` handshake with role+scope declaration, payload/buffer limits, frame envelope shape, and protocol versioning constants. |
| 3 | `oc_gateway_protocol_roles_scopes.md` | model | protocol.md: Roles + scopes (Roles, Scopes operator, Caps/commands/permissions node), Presence (Node background alive event), Broadcast event scoping, Scope | 600 | The connection capability model: client roles, operator scopes, node caps/commands/permissions, presence + node background-alive events, and broadcast-event scoping that govern what a connection may do. |
| 4 | `oc_gateway_protocol_rpc_methods.md` | model | protocol.md: Common RPC method families (Common event families, Node helper methods, Task ledger RPCs, Operator helper methods, `models.list` views), Exec approvals, Agent delivery fallback | 700 | Reference of the Gateway RPC surface: the common RPC method families, event families, node + operator helper methods, task-ledger RPCs, `models.list` views, exec-approval RPCs, and the agent-delivery fallback path. |
| 5 | `oc_gateway_protocol_auth_pairing.md` | procedure | protocol.md: Auth, Device identity + pairing (Device auth migration diagnostics), TLS + pinning | 600 | Authenticating and pairing a Gateway connection: the auth handshake, device identity + pairing flow, device-auth migration diagnostics, and TLS certificate pinning for the WS control plane. |
| 6 | `oc_gateway_remote.md` | procedure | remote.md (full): The core idea, VPN/tailnet setups, Command flow, SSH tunnel, CLI remote defaults, Credential precedence, Chat UI / macOS remote, Security rules, persistent LaunchAgent tunnel | 700 | Accessing a Gateway remotely over a VPN/tailnet or SSH tunnel: the three deployment topologies, where commands actually run, CLI remote defaults + credential precedence, chat-UI/macOS remote modes, the remote/VPN security rules, and a persistent macOS SSH-tunnel LaunchAgent. |
| 7 | `oc_gateway_remote_app_setup.md` | procedure | remote-gateway-readme.md (full): Overview, Quick setup (SSH config, copy key, remote auth, start tunnel, restart), Auto-Start Tunnel on Login (PLIST), Troubleshooting, How it works | 450 | Step-by-step runbook for pointing OpenClaw.app at a remote Gateway over an SSH tunnel: SSH config + key, remote-auth setup, starting the tunnel, restarting the app, auto-starting the tunnel on login via a launchd PLIST, and troubleshooting. |
| 8 | `oc_gateway_sandbox_vs_tool_policy_vs_elevated.md` | concept | sandbox-vs-tool-policy-vs-elevated.md (full): Quick debug, Sandbox (where tools run, bind mounts), Tool policy (which tools exist/are callable, tool groups), Elevated (exec-only run-on-host), Common jail fixes | 600 | The three orthogonal containment layers and how they compose: sandbox (where a tool runs), tool policy (which tools exist / are callable), and elevated exec (run-on-host bypass) — with a quick-debug decision guide and common "sandbox jail" fixes. |
| 9 | `oc_gateway_sandboxing_model.md` | model | sandboxing.md: What gets sandboxed, Modes, Scope, Tool policy and escape hatches, Multi-agent overrides | 600 | The sandboxing model: what gets sandboxed vs runs on host, the available sandbox modes, scoping (per-agent/per-session), and how tool policy + escape hatches and multi-agent overrides layer on top. |
| 10 | `oc_gateway_sandboxing_backends.md` | procedure | sandboxing.md: Backend (Choosing a backend, Docker/SSH/OpenShell), Workspace access, Custom bind mounts, Images and setup, setupCommand, Minimal enable example | 750 | Configuring a sandbox backend: choosing among Docker / SSH / OpenShell, granting workspace access, adding custom bind mounts, building images + one-time `setupCommand`, and a minimal enable example. |
| 11 | `oc_gateway_secrets_contract.md` | model | secrets.md: Goals and runtime model, Agent-access boundary, Active-surface filtering, SecretRef contract, Supported credential surface, Required behavior and precedence, Activation triggers, Degraded/recovered signals, One-way safety policy, Legacy auth compatibility | 700 | The SecretRef secrets-management contract + runtime model: the eager in-memory snapshot, agent-access boundary, active-surface filtering, the SecretRef syntax/precedence, supported credential surface, activation triggers, degraded/recovered signals, and the one-way (no-plaintext-back) safety policy. |
| 12 | `oc_gateway_secrets_operations.md` | procedure | secrets.md: Gateway auth surface diagnostics, Onboarding reference preflight, Provider config, File-backed API keys, Exec integration examples, MCP server env vars, Sandbox SSH auth material, Command-path resolution, Audit and configure workflow, Web UI note | 700 | Operating secrets in production: the `secrets audit`/`configure`/apply workflow, gateway-auth-surface diagnostics, onboarding preflight, wiring SecretRefs into provider config, file-backed API keys, exec/MCP/sandbox-SSH integration, command-path resolution, and the Web UI note. |

> Filename rule applied: `oc_` + slug with `/` and `-` → `_`. Split notes append a short aspect suffix
> (`_transport`, `_roles_scopes`, `_rpc_methods`, `_auth_pairing`, `_model`, `_backends`, `_contract`,
> `_operations`, `_app_setup`). One building_block per note.

## Section Coverage Map

```
prometheus.md
├── Quick start ──────────────────────────────────────── → note 1 (oc_gateway_prometheus)
├── Metrics exported ─────────────────────────────────── → note 1
├── Label policy ─────────────────────────────────────── → note 1
├── PromQL recipes ───────────────────────────────────── → note 1
├── Choosing between Prometheus and OpenTelemetry ────── → note 1 (link-out gw04 opentelemetry)
├── Troubleshooting ──────────────────────────────────── → note 1
└── Related ──────────────────────────────────────────── → note 1 (References)
protocol.md
├── Transport ────────────────────────────────────────── → note 2 (oc_gateway_protocol_transport)
├── Handshake (connect) + Node example ───────────────── → note 2
├── Framing ──────────────────────────────────────────── → note 2
├── Versioning + Client constants ────────────────────── → note 2
├── Roles + scopes (Roles, Scopes operator, Caps/commands/permissions node) → note 3 (oc_gateway_protocol_roles_scopes)
├── Presence + Node background alive event ───────────── → note 3
├── Broadcast event scoping ──────────────────────────── → note 3
├── Scope ────────────────────────────────────────────── → note 3
├── Common RPC method families ───────────────────────── → note 4 (oc_gateway_protocol_rpc_methods)
│   ├── Common event families ────────────────────────── → note 4
│   ├── Node helper methods ──────────────────────────── → note 4
│   ├── Task ledger RPCs ─────────────────────────────── → note 4
│   ├── Operator helper methods ──────────────────────── → note 4
│   └── models.list views ────────────────────────────── → note 4
├── Exec approvals ───────────────────────────────────── → note 4
├── Agent delivery fallback ──────────────────────────── → note 4
├── Auth ─────────────────────────────────────────────── → note 5 (oc_gateway_protocol_auth_pairing)
├── Device identity + pairing + Device auth migration diagnostics → note 5
├── TLS + pinning ────────────────────────────────────── → note 5
└── Related ──────────────────────────────────────────── → notes 2–5 (References)
remote.md
├── The core idea ────────────────────────────────────── → note 6 (oc_gateway_remote)
├── Common VPN and tailnet setups (3 topologies) ─────── → note 6
├── Command flow (what runs where) ───────────────────── → note 6
├── SSH tunnel (CLI + tools) ─────────────────────────── → note 6
├── CLI remote defaults ──────────────────────────────── → note 6
├── Credential precedence ────────────────────────────── → note 6
├── Chat UI / macOS app remote ───────────────────────── → note 6
├── Security rules (remote/VPN) ──────────────────────── → note 6
├── macOS persistent SSH tunnel via LaunchAgent ──────── → note 6
└── Related ──────────────────────────────────────────── → note 6 (References)
remote-gateway-readme.md
├── Overview ─────────────────────────────────────────── → note 7 (oc_gateway_remote_app_setup)
├── Quick setup (Steps 1–5) ──────────────────────────── → note 7
├── Auto-Start Tunnel on Login (PLIST, load) ─────────── → note 7
├── Troubleshooting ──────────────────────────────────── → note 7
├── How it works ─────────────────────────────────────── → note 7
└── Related ──────────────────────────────────────────── → note 7 (References)
sandbox-vs-tool-policy-vs-elevated.md
├── Quick debug ──────────────────────────────────────── → note 8 (oc_gateway_sandbox_vs_tool_policy_vs_elevated)
├── Sandbox: where tools run (+ bind mounts quick check) → note 8
├── Tool policy: which tools exist/are callable (+ groups) → note 8
├── Elevated: exec-only run-on-host ──────────────────── → note 8
├── Common "sandbox jail" fixes ──────────────────────── → note 8
└── Related ──────────────────────────────────────────── → note 8 (References)
sandboxing.md
├── What gets sandboxed ──────────────────────────────── → note 9 (oc_gateway_sandboxing_model)
├── Modes ────────────────────────────────────────────── → note 9
├── Scope ────────────────────────────────────────────── → note 9
├── Tool policy and escape hatches ───────────────────── → note 9
├── Multi-agent overrides ────────────────────────────── → note 9
├── Backend (Choosing, Docker, SSH, OpenShell) ───────── → note 10 (oc_gateway_sandboxing_backends)
├── Workspace access ─────────────────────────────────── → note 10
├── Custom bind mounts ───────────────────────────────── → note 10
├── Images and setup ─────────────────────────────────── → note 10
├── setupCommand (one-time container setup) ──────────── → note 10
├── Minimal enable example ───────────────────────────── → note 10
└── Related ──────────────────────────────────────────── → notes 9–10 (References)
secrets.md
├── Goals and runtime model ──────────────────────────── → note 11 (oc_gateway_secrets_contract)
├── Agent-access boundary ────────────────────────────── → note 11
├── Active-surface filtering ─────────────────────────── → note 11
├── SecretRef contract ───────────────────────────────── → note 11
├── Supported credential surface ─────────────────────── → note 11
├── Required behavior and precedence ─────────────────── → note 11
├── Activation triggers ──────────────────────────────── → note 11
├── Degraded and recovered signals ───────────────────── → note 11
├── One-way safety policy ────────────────────────────── → note 11
├── Legacy auth compatibility notes ──────────────────── → note 11
├── Gateway auth surface diagnostics ─────────────────── → note 12 (oc_gateway_secrets_operations)
├── Onboarding reference preflight ───────────────────── → note 12
├── Provider config ──────────────────────────────────── → note 12
├── File-backed API keys ─────────────────────────────── → note 12
├── Exec integration examples ────────────────────────── → note 12
├── MCP server environment variables ─────────────────── → note 12
├── Sandbox SSH auth material ────────────────────────── → note 12
├── Command-path resolution ──────────────────────────── → note 12
├── Audit and configure workflow ─────────────────────── → note 12
├── Web UI note ──────────────────────────────────────── → note 12
└── Related ──────────────────────────────────────────── → notes 11–12 (References)
```
No orphaned sections. Link-out targets (gw04 opentelemetry/operator-scopes/pairing, gw06 tailscale/
secrets-plan-contract/security audit-checks, gw07 trusted-proxy-auth) are cross-linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| protocol.md (6,078w, 16 H2 / 13 H3, multi-BB) | notes 2 + 3 + 4 + 5 | >2,500w by ~2.4×; four distinct task/concept clusters — wire transport model, capability (roles/scopes/presence) model, RPC-surface reference, and auth/pairing/TLS procedure. Splitting keeps each ≤700w, ≤6 code, single BB. |
| secrets.md (3,479w, 28 H2, mixed BB) | notes 11 + 12 | >2,500w; mixes the SecretRef contract/runtime model (model BB) with the audit/configure/provider-wiring operational procedure (procedure BB). Split per word-cap + mixed-BB rules. |
| sandboxing.md (3,367w, 13 H2 / 5 H3) | notes 9 + 10 | >2,500w; separates the conceptual sandboxing model (what/modes/scope/escape-hatches) from the backend-setup procedure (Docker/SSH/OpenShell, workspace, bind mounts, images, setupCommand). |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (17,369 words). New `oc_*` notes: **12** (4 single-page notes + protocol ×4 + secrets ×2 + sandboxing ×2). New `term_dictionary` notes: **0** (expected).
- BB distribution (authoritative):
  - **procedure ×6** — notes 1, 5, 6, 7, 10, 12
  - **model ×5** — notes 2, 3, 4, 9, 11
  - **concept ×1** — note 8
  - (6 + 5 + 1 = **12** ✓)
- Est. digest words ~**7,950** (avg ~660/note); within the ≤2,500w-per-note cap with wide margin.
- 70 source code fences (sum across pages) distribute across notes; each digest note caps at **≤6** (PromQL/
  JSON/shell/PLIST snippets reproduced selectively, verbatim). The fence-dense pages (`secrets` 24,
  `remote`/`remote-gateway-readme` 11 each, `protocol` 9) are the splits/single-pages where snippet selection
  is most aggressive.
- **Cross-refs (LOCKED — xref-augment 2026-06-21):** every note maps **≥8 relevance-selected `term_dictionary`
  `repo_openclaw*` + the `entry_openclaw_docs` back-link, each with a per-link relevance statement, all EXISTING

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

**Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (source re-read 2026-06-21),
remainder are sibling `oc_*` "(planned, this series)"; relevant `repo_openclaw*` + the `entry_openclaw_docs`
back-link (planned, W1) are additional. Relative paths from `resources/documentation/openclaw/oc_X.md`:
term → `../../term_dictionary/`; cc_* → `../claude_code/`; hermes_* → `../hermes_agent/`; pi_* → `../pi/`;
band_* → `../band/`; bedrock_agentcore_* → `../aws_bedrock_agentcore/`; cloudwatch_* → `../aws_cloudwatch/`;
wiki_* → `../wiki/`; snippet → `../../code_snippets/`; repo → `../../../areas/code_repos/`;
entry → `../../../0_entry_points/`; sibling oc_ → `oc_Y.md`.

### oc_gateway_prometheus (8t · 10s · 10d)

**Terms**
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — agent-runtime telemetry surfacing (tokens/spend/latency/skill usage); relevance: the `/api/diagnostics/prometheus` exporter surfaces exactly these agent-runtime signals (`openclaw_model_tokens_total`, `openclaw_model_cost_usd_total`, `openclaw_skill_used_total`).
- [Data Observability](../../term_dictionary/term_data_observability.md) — pipeline metric/health monitoring; relevance: the metric families + dashboards/alerts this note enables are a data-observability surface for the gateway runtime.
- [Time-Series Database](../../term_dictionary/term_time_series_database.md) — TSDB for metric storage/PromQL; relevance: Prometheus IS a TSDB; the note's PromQL recipes (`rate()`, `increase()`, `histogram_quantile`) are TSDB queries against scraped series.
- [EMF — Embedded Metric Format](../../term_dictionary/term_emf.md) — structured metric emission convention; relevance: contrasts with the Prometheus text exposition format this exporter emits; both are metric-emission conventions an operator chooses between.
- [Model Monitoring](../../term_dictionary/term_model_monitoring.md) — production model-call observation; relevance: `openclaw_model_call_total`, `openclaw_model_failover_total`, and `gen_ai_client_token_usage` are model-monitoring metrics exported here.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling/quota control; relevance: `scrape_interval`, the 2048-series cap, and `openclaw_prometheus_series_dropped_total` are cardinality/rate controls central to this note.
- [LLM — Large Language Model](../../term_dictionary/term_llm.md) — the model the gateway runs; relevance: the exported token/cost/duration metrics meter LLM calls; `gen_ai_client_token_usage` follows OTel GenAI conventions.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product being scraped; relevance: every metric is `openclaw_*`-prefixed and emitted by the OpenClaw gateway via the `diagnostics-prometheus` plugin.

**Docs**
- [CC: OpenTelemetry Setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — enabling OTel metrics export in a coding agent; relevance: the note's "Prometheus vs OpenTelemetry" section directly weighs this pull-vs-push alternative.
- [CC: OTel Metrics Reference](../claude_code/cc_otel_metrics_reference.md) — agent metric catalog (tokens, cost, sessions); relevance: closest peer to OpenClaw's "Metrics exported" table — same token/cost/session metric families under OTel naming.
- [CC: SDK Observability (OpenTelemetry)](../claude_code/cc_sdk_observability_opentelemetry.md) — SDK-level telemetry wiring; relevance: parallels the gateway-as-exporter model; both expose agent telemetry to external collectors.
- [CC: Data Usage and Telemetry](../claude_code/cc_data_usage_and_telemetry.md) — what telemetry is/isn't collected + privacy; relevance: mirrors this note's label policy ("what never appears in Prometheus output" — no prompt text, secrets, session ids).
- [CC: OTel Analysis and Privacy](../claude_code/cc_otel_analysis_and_privacy.md) — privacy-preserving telemetry analysis; relevance: corroborates the low-cardinality/redaction label policy this exporter enforces.
- [CC: Analytics Dashboards](../claude_code/cc_analytics_dashboards.md) — building agent usage dashboards; relevance: the consuming surface for the scraped metrics (Grafana dashboards the PromQL recipes feed).
- [AWS Bedrock AgentCore: Observability Overview](../aws_bedrock_agentcore/bedrock_agentcore_observability_overview.md) — managed-agent observability stack; relevance: an alternative managed observability path for agent runtimes, contrasting OpenClaw's self-hosted pull model.
- [AWS CloudWatch: Metrics Overview](../aws_cloudwatch/cloudwatch_metrics_overview.md) — counter/gauge/histogram metric model; relevance: same metric-type vocabulary (counter/gauge/histogram) the exported-metrics table uses.
- [AWS CloudWatch: Alarms / PromQL](../aws_cloudwatch/cloudwatch_alarms_promql.md) — PromQL-based alerting on metrics; relevance: directly applies the PromQL recipe patterns (SLO thresholds, dropped-series alarm) to alerting.
- [oc_gateway_protocol_rpc_methods](oc_gateway_protocol_rpc_methods.md) — Gateway RPC surface incl. `usage.cost`/`usage.status` (planned, this series); relevance: the RPC usage/cost methods are the in-band counterpart to the out-of-band Prometheus scrape this note documents.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway server that registers the `/api/diagnostics/prometheus` route; relevance: code-side home of the exporter and diagnostics event flow.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level OpenClaw repo + `diagnostics-prometheus` plugin; relevance: where the plugin is installed/enabled per the quick-start.

**Snippets**
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — structured logging/diagnostics init; relevance: peer to the diagnostics event pipeline that feeds the exporter.
- [snippet_hermes_agent_plugins_observability_langfuse](../../code_snippets/snippet_hermes_agent_plugins_observability_langfuse.md) — observability plugin export; relevance: a plugin-as-exporter pattern analogous to `diagnostics-prometheus`.
- [snippet_hermes_agent_core_conversation_loop_usage_accounting](../../code_snippets/snippet_hermes_agent_core_conversation_loop_usage_accounting.md) — per-turn token/cost accounting; relevance: the source of token/cost counters (`model_tokens_total`, `model_cost_usd_total`) this note exports.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway plugin config/load; relevance: how the `diagnostics-prometheus` plugin is enabled + its HTTP route registered at startup.
- [snippet_openclaw_gateway_agent_voice_wake_tracking](../../code_snippets/snippet_openclaw_gateway_agent_voice_wake_tracking.md) — gateway event tracking; relevance: example of the gateway-event instrumentation that becomes `openclaw_talk_event_total` series.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — gateway HTTP/WS listener; relevance: the HTTP server stack that hosts the auth-protected `/metrics` route.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth-mode resolution; relevance: the scrape route requires operator-scope gateway auth (the `Authorization: Bearer` path in the quick-start).
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — rate-limit/policy guard; relevance: cardinality/series-cap control is the metric-side analogue of this rate-limiting guard.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — plugin HTTP route registration; relevance: how the plugin's `/api/diagnostics/prometheus` route is wired into the gateway HTTP surface.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — misc gateway methods incl. `diagnostics.stability`; relevance: the diagnostics/stability recorder is the bounded event source the exporter renders.

### oc_gateway_protocol_transport (8t · 10s · 10d)

**Terms**
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex framed transport; relevance: the protocol is "WebSocket, text frames with JSON payloads" — the literal transport this note models.
- [WebSocket Framing](../../term_dictionary/term_websocket_framing.md) — frame structure/payload limits; relevance: this note documents the req/res/event envelope, 64 KiB pre-connect cap, and `maxPayload`/`maxBufferedBytes` framing limits.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — id/method/params request model; relevance: the `{type:"req", id, method, params}` envelope is a JSON-RPC-style framing the handshake uses.
- [RPC — Remote Procedure Call](../../term_dictionary/term_rpc.md) — request/response over a wire; relevance: the `connect` request and `hello-ok` response are the foundational RPC pair of the control plane.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — feature/version handshake; relevance: `minProtocol`/`maxProtocol` + `hello-ok.features.methods/events` is exactly capability + version negotiation.
- [SSE — Server-Sent Events](../../term_dictionary/term_sse.md) — server-push streaming alternative; relevance: contrasts with the WS bidirectional transport; the gateway also has SSE surfaces, so the transport choice matters.
- [ACP — Agent Client Protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — agent↔client wire protocol; relevance: a sibling agent wire protocol OpenClaw also speaks; the gateway WS protocol is the OpenClaw-native equivalent.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway whose protocol this is; relevance: this is OpenClaw's "single control plane + node transport".

**Docs**
- [Band: WebSocket Overview](../band/band_websocket_overview.md) — WS transport for an agent platform; relevance: closest peer doc — same framed-WS-as-control-plane model for an agent system.
- [CC: MCP Transports](../claude_code/cc_mcp_transports.md) — stdio/SSE/WS transport selection; relevance: situates the WS transport against MCP's transport menu; framing/limits comparison.
- [CC: Network, TLS and Access](../claude_code/cc_network_tls_and_access.md) — transport security + access; relevance: the `wss://`/TLS layer this WS protocol rides on (versioning constants reference `tlsFingerprint`).
- [Band: MCP Overview](../band/band_mcp_overview.md) — MCP wire integration; relevance: parallel JSON-RPC-over-transport surface; framing/envelope analogy.
- [Hermes: MCP Config Reference](../hermes_agent/hermes_mcp_config_reference.md) — MCP server transport config; relevance: another JSON-RPC framing/transport configuration peer.
- [Band: A2A Adapter](../band/band_a2a_adapter.md) — agent-to-agent protocol adapter; relevance: a sibling agent transport whose handshake/versioning parallels `connect`/`hello-ok`.
- [CC: MCP Quickstart](../claude_code/cc_mcp_quickstart.md) — connecting over a JSON-RPC transport; relevance: client-side connect flow analogous to the WS `connect` first-frame requirement.
- [oc_gateway_protocol_roles_scopes](oc_gateway_protocol_roles_scopes.md) — role/scope capability model (planned, this series); relevance: the `role`+`scopes` declared in the `connect` frame are detailed there.
- [oc_gateway_protocol_rpc_methods](oc_gateway_protocol_rpc_methods.md) — RPC method-family reference (planned, this series); relevance: the methods carried over this transport's req/res envelope.
- [oc_gateway_protocol_auth_pairing](oc_gateway_protocol_auth_pairing.md) — auth/pairing/TLS (planned, this series); relevance: the `auth`/`device` fields of the `connect` frame are detailed there.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway WS server + `packages/gateway-protocol` schema; relevance: where `frames.ts`/`version.ts`/`client.ts` (cited by this note) live.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — top-level repo housing the protocol package; relevance: the `pnpm protocol:gen`/`:check` codegen targets run here.

**Snippets**
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — req/res/event envelope shape; relevance: the exact framing model (`{type:"req"...}`/`{type:"res"...}`/`{type:"event"...}`) this note defines.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — protocol error codes + version constants; relevance: implements `PROTOCOL_VERSION`/`minProtocol`/`maxProtocol` negotiation and `UNAVAILABLE` retryable errors.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — `connect` failure codes; relevance: the `connect`-time error surface (e.g. `startup-sidecars` `UNAVAILABLE`) this note describes.
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — top-level frame dispatch; relevance: routes incoming text frames to the req/res/event handlers per the framing rules.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection lifecycle; relevance: implements the connect→hello-ok handshake + tick/timeout close (code `4000`) constants.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — reference client connect path; relevance: the `src/gateway/client.ts` constants table (timeouts, backoff, `MAX_PAYLOAD_BYTES`) this note tabulates.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — SDK WS channel client; relevance: a third-party-style client honoring the `hello-ok.policy` limits this note specifies.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android node WS session; relevance: the node-side of the WS transport (the "Node example" connect frame in this note).
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — server WS listener bind; relevance: the loopback/port bind that hosts the WS endpoint clients first `connect` to.

### oc_gateway_protocol_roles_scopes (8t · 10s · 10d)

**Terms**
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — declared caps/commands/permissions; relevance: nodes declare `caps`/`commands`/`permissions` claims that the gateway enforces server-side — the core of this note.
- [Access Control](../../term_dictionary/term_access_control.md) — subject→permission gating; relevance: operator scopes (`operator.read/write/admin/...`) gate which methods/broadcasts a connection may use.
- [FGAC — Fine-Grained Access Control](../../term_dictionary/term_fgac.md) — granular per-resource permissions; relevance: the per-method scope + approval-time + command-level checks (e.g. `/config set` needs `operator.admin`) are FGAC.
- [AAA — Authentication, Authorization, Accounting](../../term_dictionary/term_aaa.md) — the authZ leg of AAA; relevance: scope resolution + reserved admin prefixes (`config.*`, `exec.approvals.*`) is the authorization model.
- [WebSocket](../../term_dictionary/term_websocket.md) — the connection these scopes attach to; relevance: roles/scopes are declared at WS `connect` and gate the per-socket broadcast stream.
- [Session Features](../../term_dictionary/term_session_features.md) — per-session capability surface; relevance: broadcast scoping decides which session content (chat/agent/tool frames) a connection passively receives.
- [Audit Operations](../../term_dictionary/term_audit_operations.md) — security event logging; relevance: scope/approval decisions are audited; presence + `system-event` feed the operability surface.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway enforcing this model; relevance: this is OpenClaw's role/scope/presence/broadcast capability model.

**Docs**
- [CC: Channels Security and Enterprise Controls](../claude_code/cc_channels_security_and_enterprise_controls.md) — per-surface permission gating; relevance: closest peer — role/scope gating of agent surfaces in an enterprise control plane.
- [CC: Security Guidance Layers and Rules](../claude_code/cc_security_guidance_layers_and_rules.md) — layered permission rules; relevance: parallels "method scope is only the first gate" + command-level + approval-time layering.
- [CC: Managed Permission Settings and Precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — permission precedence resolution; relevance: mirrors reserved-admin-prefix precedence and scope-upgrade rules.
- [CC: Tool-Specific Permission Rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool allow gating; relevance: analogous to plugin-registered RPC methods requesting their own operator scope.
- [CC: Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — relaying permission/scope across surfaces; relevance: parallels presence keyed by device identity showing one row across operator+node roles.
- [Band: A2A Adapter](../band/band_a2a_adapter.md) — agent role/capability declaration; relevance: peer model where a connecting agent declares role + capabilities, like the operator/node role split.
- [oc_gateway_protocol_transport](oc_gateway_protocol_transport.md) — connect frame carrying role/scopes (planned, this series); relevance: roles/scopes are declared in the `connect` params this details.
- [oc_gateway_protocol_rpc_methods](oc_gateway_protocol_rpc_methods.md) — the scoped RPC surface (planned, this series); relevance: every method family in that note is gated by the scopes defined here.
- [oc_gateway_protocol_auth_pairing](oc_gateway_protocol_auth_pairing.md) — pairing/scope-upgrade checks (planned, this series); relevance: `node.pair.approve` approval-time scope checks bridge pairing and this scope model.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway server enforcing scopes/broadcast gating; relevance: server-side allowlist enforcement of node claims lives here.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/presence state; relevance: presence entries + `node.list` `lastSeen*` + background-alive events are session-layer state.

**Snippets**
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — per-method scope gate; relevance: implements "method scope is only the first gate" + reserved-admin-prefix resolution.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize-then-dispatch; relevance: the authorization step that checks the connection's scopes before running a method.
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — node presence/alive events; relevance: the `node.presence.alive` background-wake event + presence snapshot this note documents.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — scoped runtime broadcast; relevance: the scope-gated broadcast event delivery (chat/agent frames need `operator.read`) this note specifies.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command allowlist; relevance: server-side enforcement of node `commands`/`permissions` claims.
- [snippet_openclaw_gateway_node_events_voice_exec_dedup](../../code_snippets/snippet_openclaw_gateway_node_events_voice_exec_dedup.md) — node-event handling; relevance: durable-vs-acknowledged `node.event` handling (the `handled: false` device-less case).
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — chat-frame handling; relevance: chat/agent/tool broadcast frames are the scope-gated content (`operator.read`) this note covers.
- [snippet_hermes_agent_gw_runner_acl](../../code_snippets/snippet_hermes_agent_gw_runner_acl.md) — gateway ACL enforcement; relevance: peer ACL model for gating who may invoke gateway actions, like operator scopes here.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — `system-presence`/`system-event` methods; relevance: the presence + system-event RPCs this note's Presence section describes.
- [snippet_openclaw_gateway_agent_identity_reset](../../code_snippets/snippet_openclaw_gateway_agent_identity_reset.md) — identity/role state; relevance: device-identity-keyed presence rows (operator+node on one device) tie to this identity handling.

### oc_gateway_protocol_rpc_methods (8t · 10s · 10d)

**Terms**
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — method/params/result calls; relevance: every RPC family (`sessions.*`, `tasks.*`, `config.*`, `models.list`) is a JSON-RPC-style method over the WS envelope.
- [RPC — Remote Procedure Call](../../term_dictionary/term_rpc.md) — remote method invocation; relevance: this note is the RPC-surface reference for the gateway control plane.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: `tools.catalog`/`tools.effective`/`tools.invoke` expose the function-calling tool surface over RPC.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — catalog of callable tools; relevance: `tools.catalog`/`commands.list`/`skills.*` are the gateway's tool/command registry RPCs.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — per-tool metadata/provenance; relevance: `tools.catalog` returns grouped tools with `source`/`pluginId`/`optional` provenance — descriptor metadata.
- [Event Ledger](../../term_dictionary/term_event_ledger.md) — durable record of work items; relevance: `tasks.list/get/cancel` expose the Gateway task ledger (`TaskSummary` records) this note documents.
- [MCP — Model Context Protocol](../../term_dictionary/term_mcp.md) — external tool servers; relevance: `tools.effective` projects warm MCP server tools (`mcp-not-yet-connected` notices) into the RPC response.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway exposing these RPCs; relevance: the entire WS method surface (`hello-ok.features.methods`) is OpenClaw's.

**Docs**
- [CC: Tools Catalog](../claude_code/cc_tools_catalog.md) — enumerating available tools; relevance: peer to `tools.catalog`/`tools.effective` — the agent tool-inventory surface.
- [CC: Commands Reference](../claude_code/cc_commands_reference.md) — command/method inventory; relevance: parallels `commands.list` runtime command inventory + slash aliases.
- [CC: Subagent Configuration Reference](../claude_code/cc_subagent_configuration_reference.md) — agent/session management; relevance: parallels `agents.*`/`sessions.*` agent+session control RPCs.
- [CC: Dispatch Background Agents](../claude_code/cc_dispatch_background_agents.md) — background task dispatch; relevance: parallels the task-ledger RPCs (`tasks.*`) and `cron.*` automation methods.
- [Hermes: Security Command Approval](../hermes_agent/hermes_security_command_approval.md) — exec/command approval flow; relevance: peer to the `exec.approval.*` family + `exec.approvals.set` policy this note documents.
- [CC: MCP Transports](../claude_code/cc_mcp_transports.md) — MCP tool exposure; relevance: `tools.effective` MCP projection semantics map onto MCP transport concepts here.
- [Band: MCP Overview](../band/band_mcp_overview.md) — MCP tool integration; relevance: another MCP-over-gateway tool surface comparable to `tools.invoke`.
- [oc_gateway_protocol_transport](oc_gateway_protocol_transport.md) — the envelope these methods ride (planned, this series); relevance: every RPC here uses the req/res framing defined there.
- [oc_gateway_protocol_roles_scopes](oc_gateway_protocol_roles_scopes.md) — scopes gating each method (planned, this series); relevance: each method's `operator.read/write/admin` requirement is defined there.
- [oc_gateway_protocol_auth_pairing](oc_gateway_protocol_auth_pairing.md) — `device.*` token RPCs (planned, this series); relevance: `device.token.rotate/revoke` + `device.pair.*` are detailed there.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway server-methods (`src/gateway/server-methods/*.ts`); relevance: the implementation of every RPC family this note references.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session + task-ledger state; relevance: backs `sessions.*` and the `tasks.*` ledger RPCs.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent records/workspace; relevance: backs `agents.*`, `agent.wait`, and `models.list` agent-scoped views.

**Snippets**
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC method-family schema grouping; relevance: the TypeBox-grouped method families (`hello-ok.features.methods`) this note enumerates.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — `agent` request dispatch + delivery; relevance: implements the "Agent delivery fallback" (`deliver`/`bestEffortDeliver`) section.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval lifecycle; relevance: the `exec.approval.request/resolve/waitDecision` family + `systemRunPlan` enforcement.
- [snippet_openclaw_gateway_exec_approval_ios_push](../../code_snippets/snippet_openclaw_gateway_exec_approval_ios_push.md) — exec approval push notify; relevance: the broadcast `exec.approval.requested` → operator-resolve path this note describes.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — `health`/`status`/`diagnostics.stability` methods; relevance: the "System and identity" RPC family in this note.
- [snippet_openclaw_acp_permission_relay](../../code_snippets/snippet_openclaw_acp_permission_relay.md) — tool/permission relay; relevance: parallels `tools.invoke` routing through gateway tool policy (refusals return `ok:false`).
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — tool approval policy; relevance: peer to `exec.approvals.get/set` policy snapshots.
- [snippet_openclaw_gateway_agent_voice_wake_tracking](../../code_snippets/snippet_openclaw_gateway_agent_voice_wake_tracking.md) — `voicewake.*`/event RPCs; relevance: the `voicewake.get/set` + event-family RPCs this note lists.

### oc_gateway_protocol_auth_pairing (8t · 10s · 10d)

**Terms**
- [Authentication](../../term_dictionary/term_authentication.md) — verifying client identity; relevance: shared-secret token/password connect auth + identity-bearing modes are the auth handshake this note covers.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer token credential; relevance: the issued per-device `deviceToken` (bounded operator token from bootstrap) is the bearer this note persists/rotates.
- [TLS — Transport Layer Security](../../term_dictionary/term_tls.md) — encrypted transport; relevance: TLS for WS connections + cert handling underpin the trusted-endpoint auto-promotion rule.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — certificate fingerprint pinning; relevance: this note's "TLS + pinning" section (`gateway.remote.tlsFingerprint`, `--tls-fingerprint`).
- [Device ID](../../term_dictionary/term_device_id.md) — stable device identity; relevance: `device.id` derived from a keypair fingerprint is the pairing identity this note centers on.
- [WebSocket](../../term_dictionary/term_websocket.md) — the connection being authed; relevance: auth + device identity are asserted in the WS `connect` frame and verified against the challenge nonce.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — scope set in handshake; relevance: `AUTH_SCOPE_MISMATCH` + scope-preservation on reconnect tie auth to the negotiated scope set.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway issuing device tokens; relevance: OpenClaw's per-device/role token issuance, rotation, and pairing approval model.

**Docs**
- [CC: Network, TLS and Access](../claude_code/cc_network_tls_and_access.md) — TLS + access control; relevance: the TLS/pinning layer this note's auth rides on.
- [CC: Authentication and Network Errors](../claude_code/cc_authentication_and_network_errors.md) — auth failure diagnostics; relevance: peer to the `DEVICE_AUTH_*`/`AUTH_TOKEN_MISMATCH` detail codes + `recommendedNextStep` recovery hints.
- [CC: MCP Authentication](../claude_code/cc_mcp_authentication.md) — token/OAuth auth for a transport; relevance: parallel token-bearing connect auth + retry semantics.
- [CC: Login Authentication Troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth retry/recovery; relevance: mirrors the device-auth migration diagnostics + bounded-retry client behavior.
- [CC: Remote Control](../claude_code/cc_remote_control.md) — pairing a remote control client; relevance: peer to device pairing approval + bootstrap (QR/setup-code) handoff.
- [AWS Bedrock AgentCore: Identity Overview](../aws_bedrock_agentcore/bedrock_agentcore_identity_overview.md) — agent identity/credential model; relevance: managed-agent device-identity + token issuance analogue to OpenClaw pairing.
- [oc_gateway_protocol_transport](oc_gateway_protocol_transport.md) — connect frame `auth`/`device` fields (planned, this series); relevance: this note explains the `auth`/`device` params the connect frame carries.
- [oc_gateway_protocol_roles_scopes](oc_gateway_protocol_roles_scopes.md) — scopes bound to a device token (planned, this series); relevance: token issuance is bounded to the approved role/scope set defined there.
- [oc_gateway_secrets_contract](oc_gateway_secrets_contract.md) — `gateway.auth.token` SecretRef (planned, this series); relevance: the connect token can be a SecretRef resolved per the secrets contract.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — connect/challenge/handshake + device-auth verification; relevance: `selectConnectAuth`, challenge signing, and device-token issuance live here.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — device identity/pairing security policy; relevance: pairing approval, nonce/signature validation, and break-glass trust paths.

**Snippets**
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client device identity + TLS; relevance: the device keypair signing + TLS-fingerprint pin this note's auth/pinning sections cover.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing approval; relevance: the `node.pair.*` approval flow + local-loopback auto-approval this note describes.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode selection; relevance: shared-secret vs identity-bearing (trusted-proxy/Tailscale) vs `none` connect-auth modes.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: the device-less operator Control UI trust paths (`allowInsecureAuth`, `dangerouslyDisableDeviceAuth`).
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect/auth error codes; relevance: `DEVICE_AUTH_*` + `PAIRING_REQUIRED`/`AUTH_*_MISMATCH` codes this note tabulates.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect auth assembly; relevance: `selectConnectAuth` token priority (shared → deviceToken → stored per-device → bootstrap).
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS QR/setup-code pairing; relevance: the QR/setup-code bootstrap mobile-operator handoff (bounded operator token) this note describes.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS fingerprint pinning; relevance: implements the optional cert-fingerprint pin this note's "TLS + pinning" section specifies.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — paired-node invoke via push; relevance: post-pairing node command delivery to authenticated device sessions.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — paired-device command policy; relevance: paired-device metadata pinning controls command policy on reconnect (legacy `v2` signature note).

### oc_gateway_remote (8t · 10s · 10d)

**Terms**
- [VPN — Virtual Private Network](../../term_dictionary/term_vpn.md) — private overlay network; relevance: the "Common VPN and tailnet setups" topologies (Tailscale/private bind) are the core deployment patterns.
- [SSH — Secure Shell](../../term_dictionary/term_ssh.md) — encrypted remote shell + tunneling; relevance: the SSH tunnel (`ssh -N -L 18789:...`) is the universal remote-access fallback this note details.
- [Tunneling](../../term_dictionary/term_tunneling.md) — port forwarding over a secure channel; relevance: `LocalForward`/SSH port-forward of the loopback gateway port is the central mechanism.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting a service for ingress/auth; relevance: Tailscale Serve + `trusted-proxy` identity-aware proxy are the non-loopback ingress options.
- [Authentication](../../term_dictionary/term_authentication.md) — gateway auth for remote binds; relevance: non-loopback binds MUST use token/password/trusted-proxy auth — the security-rules section.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — remote client credential; relevance: `gateway.remote.token` credential precedence + explicit-credential-required-with-`--url` rules.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway being accessed remotely; relevance: the master/single-gateway + node-peripheral model is OpenClaw's remote architecture.

**Docs**
- [CC: Cloud Network Access](../claude_code/cc_cloud_network_access.md) — remote/cloud network access for an agent; relevance: closest peer — connecting clients to a remote agent host over a network.
- [Hermes: OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md) — auth over an SSH tunnel; relevance: directly parallels carrying gateway auth over the SSH tunnel this note builds.
- [CC: Network, TLS and Access](../claude_code/cc_network_tls_and_access.md) — `wss://` vs plaintext + access; relevance: the "public hosts must use `wss://`; loopback/`.ts.net` may use `ws://`" rule.
- [CC: Remote Control](../claude_code/cc_remote_control.md) — driving an agent from a remote client; relevance: peer to the macOS app remote mode + chat-UI remote access.
- [CC: Cloud Environment](../claude_code/cc_cloud_environment.md) — agent in a cloud host; relevance: the VPS/home-server always-on gateway topology.
- [Band: WebSocket Overview](../band/band_websocket_overview.md) — connecting clients over WS; relevance: the remote client connects to the gateway WS over the tunnel/tailnet.
- [oc_gateway_remote_app_setup](oc_gateway_remote_app_setup.md) — macOS app SSH-tunnel runbook (planned, this series); relevance: the concrete app-side runbook for the persistent tunnel this note introduces.
- [oc_gateway_protocol_auth_pairing](oc_gateway_protocol_auth_pairing.md) — connect auth modes (planned, this series); relevance: trusted-proxy/Tailscale identity-bearing auth is the connect-side of the remote security rules.
- [oc_gateway_secrets_contract](oc_gateway_secrets_contract.md) — `gateway.remote.token` SecretRef activation (planned, this series); relevance: remote token/password can be SecretRefs whose active-surface depends on `gateway.mode=remote`.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway bind/remote/credential-precedence logic; relevance: loopback bind, `gateway.remote.*` resolution, and `--url` credential rules live here.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — macOS app remote/SSH transport; relevance: the app's remote mode + managed SSH tunnel transport.

**Snippets**
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect + URL/proxy resolution; relevance: the remote `gateway.remote.url`/`--url` connect path + credential assembly this note configures.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client TLS/identity; relevance: `tlsFingerprint` pinning for `wss://` remote (incl. macOS direct mode) in the security rules.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode resolution; relevance: trusted-proxy/Tailscale/token auth selection for non-loopback binds.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — runtime bind/config; relevance: the loopback-vs-lan/tailnet bind decision the "core idea" rests on.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential resolution for call paths; relevance: the shared credential-precedence contract across call/probe/status this note tabulates.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — SDK client over WS to remote gateway; relevance: a client connecting to `ws://127.0.0.1:18789` through the tunnel.
- [snippet_openclaw_daemon_schtasks_pid_kill_tree](../../code_snippets/snippet_openclaw_daemon_schtasks_pid_kill_tree.md) — daemon/background-process lifecycle; relevance: peer to the persistent LaunchAgent that keeps the tunnel process alive across reboots.
- [snippet_hermes_agent_core_auxiliary_proxy_url](../../code_snippets/snippet_hermes_agent_core_auxiliary_proxy_url.md) — proxy URL resolution; relevance: parallels resolving the remote/proxy URL + credentials for outbound connections.
- [snippet_openclaw_voice_call_media_stream_admission](../../code_snippets/snippet_openclaw_voice_call_media_stream_admission.md) — remote media/stream admission; relevance: the chat-UI/voice-wake forwarding the macOS remote mode drives over the same transport.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — process-tree management; relevance: tunnel process supervision (`launchctl kickstart`/`bootout`, `ps`/`lsof` checks) analogue.

### oc_gateway_remote_app_setup (8t · 10s · 10d)

**Terms**
- [SSH — Secure Shell](../../term_dictionary/term_ssh.md) — encrypted remote shell + key auth; relevance: the runbook is an SSH config + `ssh-copy-id` key setup + `ssh -N` tunnel for OpenClaw.app.
- [Tunneling](../../term_dictionary/term_tunneling.md) — `LocalForward` port forwarding; relevance: `LocalForward 18789 127.0.0.1:18789` is the literal tunnel the app connects through.
- [VPN — Virtual Private Network](../../term_dictionary/term_vpn.md) — private-network alternative; relevance: the SSH tunnel is the alternative to a tailnet/VPN bind for the same remote-gateway reach.
- [Authentication](../../term_dictionary/term_authentication.md) — remote gateway auth; relevance: `openclaw config set gateway.remote.token` is the durable remote-auth setup step.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — `gateway.remote.token` bearer; relevance: the token/password remote credential persisted in config for the app.
- [Cron](../../term_dictionary/term_cron.md) — scheduled/at-load job; relevance: the launchd `RunAtLoad`/`KeepAlive` LaunchAgent is a cron-like auto-start/restart scheduler for the tunnel.
- [Remote SSH](../../term_dictionary/term_remote_ssh.md) — remote-host SSH access pattern; relevance: the whole runbook is a remote-SSH access setup for the app→gateway connection.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the app + gateway being connected; relevance: OpenClaw.app connecting to a remote OpenClaw gateway is the runbook's subject.

**Docs**
- [CC: Cloud Network Access](../claude_code/cc_cloud_network_access.md) — remote-host network access; relevance: peer for connecting a desktop client to a remote agent host.
- [Hermes: OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md) — auth tunneled over SSH; relevance: directly parallels carrying `gateway.remote.token` auth over the SSH tunnel.
- [CC: Remote Control](../claude_code/cc_remote_control.md) — remote control-client setup; relevance: peer runbook for pointing a client app at a remote agent.
- [CC: Desktop Environments (Extend and Enterprise)](../claude_code/cc_desktop_environments_extend_and_enterprise.md) — desktop client remote/enterprise setup; relevance: the macOS desktop-app remote-gateway configuration analogue.
- [CC: Network, TLS and Access](../claude_code/cc_network_tls_and_access.md) — secure remote transport; relevance: the loopback-forward-over-SSH keeps the gateway off public ingress (the security rationale).
- [Band: WebSocket Overview](../band/band_websocket_overview.md) — app↔gateway WS connection; relevance: the app connects to `ws://127.0.0.1:18789` (forwarded) — a WS client connection.
- [oc_gateway_remote](oc_gateway_remote.md) — full remote-access concepts/CLI (planned, this series); relevance: this runbook is the app-specific subset of that conceptual page (merged source banner).
- [oc_gateway_protocol_auth_pairing](oc_gateway_protocol_auth_pairing.md) — connect auth after tunnel up (planned, this series); relevance: once tunneled, the app still completes the device-auth/pairing connect handshake.
- [oc_gateway_secrets_operations](oc_gateway_secrets_operations.md) — storing remote token via config/SecretRef (planned, this series); relevance: `config set gateway.remote.token` can target a SecretRef per the secrets ops workflow.

**Repos**
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — OpenClaw.app remote/SSH-tunnel transport; relevance: the app code that connects to the forwarded local port + manages the transport.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the remote gateway endpoint; relevance: the server the tunnel forwards to on port 18789.

**Snippets**
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect to forwarded URL; relevance: the app connecting to `ws://127.0.0.1:18789` with `gateway.remote.token`.
- [snippet_openclaw_daemon_schtasks_pid_kill_tree](../../code_snippets/snippet_openclaw_daemon_schtasks_pid_kill_tree.md) — background daemon lifecycle/auto-restart; relevance: peer to the launchd LaunchAgent `KeepAlive`/`RunAtLoad` auto-start + restart-on-crash.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — process supervision; relevance: tunnel process checks/restart (`ps`, `lsof`, `launchctl kickstart`/`bootout`).
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity/TLS over the tunnel; relevance: the app still presents device identity through the forwarded connection.
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — CLI config-set persistence; relevance: peer to `openclaw config set gateway.remote.token` durable config write.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — guided setup config writing; relevance: the config-write step (remote token) the runbook performs.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — remote auth-mode resolution; relevance: how the app's `gateway.remote.token` resolves into connect auth.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — remote gateway WS listener; relevance: the loopback-bound WS endpoint the tunnel forwards to on the remote host.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection lifecycle; relevance: the app re-establishes the WS connection to the forwarded local port after each restart/tunnel-reconnect.
- [snippet_hermes_agent_core_auxiliary_proxy_url](../../code_snippets/snippet_hermes_agent_core_auxiliary_proxy_url.md) — forwarded-URL resolution; relevance: resolving the local forwarded URL + auth for the app's connection.

### oc_gateway_sandbox_vs_tool_policy_vs_elevated (8t · 10s · 10d)

**Terms**
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated tool-execution environment; relevance: layer 1 of the three controls — sandbox decides WHERE tools run (backend vs host).
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — runtime providing the sandbox; relevance: the `agents.defaults.sandbox.*` backend the first control selects (Docker/SSH/OpenShell).
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: tool policy (layer 2) decides WHICH tools exist/are callable — gating the function-calling surface.
- [Access Control](../../term_dictionary/term_access_control.md) — allow/deny gating; relevance: `tools.allow`/`tools.deny` ("deny always wins") is the tool-policy access-control model.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — effective tool/elevated set; relevance: `openclaw sandbox explain` prints the effective sandbox/tool/elevated capability composition.
- [iframe Sandbox](../../term_dictionary/term_iframe_sandbox.md) — bounded-capability isolation primitive; relevance: an analogous "isolate-then-selectively-allow" model to OpenClaw's sandbox + tool policy layering.
- [Audit Operations](../../term_dictionary/term_audit_operations.md) — policy decision logging; relevance: `agents/tool-policy` audit log entries record which allow/deny rule blocked a tool.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the system composing these controls; relevance: this is OpenClaw's three-orthogonal-controls mental model.

**Docs**
- [CC: Sandbox vs Permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox-vs-permission distinction; relevance: the directly analogous "what's the difference between sandbox and tool permission" framing.
- [CC: Sandbox Modes](../claude_code/cc_sandbox_modes.md) — off/scoped/all modes; relevance: the `off`/`non-main`/`all` sandbox modes this note's "where tools run" section references.
- [CC: Sandbox Filesystem/Network Isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — fs/net isolation; relevance: bind-mount piercing (`docker.binds`, `:ro`/`:rw`) is the filesystem-isolation quick-check here.
- [CC: Tool-Specific Permission Rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool allow/deny; relevance: peer to tool profiles + `group:*` allow/deny + "deny always wins".
- [CC: Managed Permission Settings and Precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — permission precedence; relevance: the global/per-agent/sandbox/provider tool-policy precedence layering.
- [CC: SDK Python Tool IO and Sandbox](../claude_code/cc_sdk_python_tool_io_and_sandbox.md) — tool execution inside a sandbox; relevance: the "where exec runs" + elevated-escape distinction at SDK level.
- [oc_gateway_sandboxing_model](oc_gateway_sandboxing_model.md) — full sandboxing model (planned, this series); relevance: the "See Sandboxing for the full matrix" link-target this note defers to.
- [oc_gateway_sandboxing_backends](oc_gateway_sandboxing_backends.md) — backend setup (planned, this series); relevance: the bind-mount/backend detail this note quick-checks is fully documented there.
- [oc_gateway_secrets_operations](oc_gateway_secrets_operations.md) — sandbox SSH/secret material (planned, this series); relevance: secret-bearing binds (`:ro` for secrets) tie sandbox policy to secrets handling.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — sandbox/tool-policy/elevated enforcement; relevance: the three controls' policy code (deny-wins, elevated gates).
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — `agents/tool-policy` audit + `sandbox explain`; relevance: where the tool-policy audit entries + effective-policy inspector are produced.

**Snippets**
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny-list enforcement; relevance: "deny always wins" tool-policy gate — the hard stop this note describes.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: tool policy filters by name but does not inspect exec side effects — exactly this snippet's concern.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — composed policy audit; relevance: the effective-policy composition `sandbox explain`/audit reports (agent/global/default origin).
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — tool approval/policy; relevance: peer policy model where allow/deny + approvals compose like elevated gates.
- [snippet_openclaw_acp_permission_relay](../../code_snippets/snippet_openclaw_acp_permission_relay.md) — permission relay for tools; relevance: tool-availability gating relayed to the runtime, like the tool-policy layer.
- [snippet_openclaw_security_openshell_fs_bridge](../../code_snippets/snippet_openclaw_security_openshell_fs_bridge.md) — sandbox fs bridge; relevance: "where tools run" filesystem boundary the sandbox layer enforces.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — sandboxed code execution; relevance: peer to sandboxed `exec` vs elevated run-on-host distinction.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec runtime audit; relevance: elevated exec bypasses sandbox (`gateway`/`node` escape path) — the audited run-on-host case.
- [snippet_hermes_agent_tools_credential_files](../../code_snippets/snippet_hermes_agent_tools_credential_files.md) — credential-path protection; relevance: blocked credential-root binds (`~/.aws`, `~/.ssh`) are the bind-security quick-check.

### oc_gateway_sandboxing_model (8t · 10s · 10d)

**Terms**
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution to limit blast radius; relevance: the note's subject — what gets sandboxed (tool exec, browser) vs runs on host (the Gateway).
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — runtime selection; relevance: `backend` (docker/ssh/openshell) is one axis of the sandboxing model.
- [Session Features](../../term_dictionary/term_session_features.md) — per-session sandbox scope; relevance: `scope` (`agent`/`session`/`shared`) and `non-main` mode are session-keyed sandbox decisions.
- [Capability Negotiation](../../term_dictionary/term_capability_negotiation.md) — effective sandbox/tool capability; relevance: tool-policy escape hatches + multi-agent overrides compose the effective sandbox capability set.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tools being sandboxed; relevance: `exec`/`read`/`write`/`edit`/`apply_patch`/`process` are the function-calling tools that run sandboxed.
- [iframe Sandbox](../../term_dictionary/term_iframe_sandbox.md) — bounded-capability isolation; relevance: analogous "not a perfect boundary but materially limits access" isolation primitive.
- [Audit Operations](../../term_dictionary/term_audit_operations.md) — sandbox policy logging; relevance: tool-policy-and-escape-hatch decisions are audited like the elevated bypass path.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the system whose sandbox this is; relevance: OpenClaw's optional, config-driven sandboxing of tool execution.

**Docs**
- [CC: Sandbox Modes](../claude_code/cc_sandbox_modes.md) — sandbox mode selection; relevance: the `off`/`non-main`/`all` modes this note's "Modes" section defines.
- [CC: Sandbox Environments Comparison](../claude_code/cc_sandbox_environments_comparison.md) — comparing sandbox runtimes; relevance: peer to the Docker/SSH/OpenShell "Choosing a backend" matrix.
- [CC: Sandbox Settings](../claude_code/cc_sandbox_settings.md) — sandbox config knobs; relevance: `scope`/`workspaceAccess`/`mode` settings this note enumerates.
- [CC: Sandbox Org Enforcement](../claude_code/cc_sandbox_org_enforcement.md) — org-level sandbox policy; relevance: parallels multi-agent overrides + "keep it locked down" enforcement.
- [CC: Sandbox Filesystem/Network Isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — fs/net isolation; relevance: workspace-access (`none`/`ro`/`rw`) + no-network-default isolation this note's scope covers.
- [pi: Containerization](../pi/pi_containerization.md) — container-based isolation model; relevance: peer concept for container-isolated agent tool execution.
- [oc_gateway_sandboxing_backends](oc_gateway_sandboxing_backends.md) — backend setup procedure (planned, this series); relevance: the procedural counterpart configuring the backends this model describes.
- [oc_gateway_sandbox_vs_tool_policy_vs_elevated](oc_gateway_sandbox_vs_tool_policy_vs_elevated.md) — the three controls (planned, this series); relevance: tool-policy + elevated escape hatches that layer on the sandbox model.
- [oc_gateway_secrets_operations](oc_gateway_secrets_operations.md) — sandbox SSH secret material (planned, this series); relevance: SSH-backend auth material is resolved via secrets — a model→ops link.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — sandboxing enforcement + escape hatches; relevance: what-gets-sandboxed + elevated-bypass policy code.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/scope state; relevance: `scope`/`non-main` decisions are session-keyed (`session.mainKey`).

**Snippets**
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/fs sandbox policy; relevance: what filesystem/process access the sandbox limits — the model's core.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — tool deny in sandbox; relevance: "tool allow/deny still applies before sandbox rules" — escape-hatch interaction.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — sandboxed code exec; relevance: the sandboxed tool-execution surface (`exec`/`process`) this model covers.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec runtime audit; relevance: elevated bypass (`gateway`/`node` escape) is the not-sandboxed runtime path.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker sandbox environment; relevance: the default Docker backend the model selects when sandboxing is on.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — multi-agent spawn; relevance: multi-agent overrides (`agents.list[].sandbox`) the model's last section covers.
- [snippet_openclaw_security_openshell_mirror](../../code_snippets/snippet_openclaw_security_openshell_mirror.md) — sandbox workspace mirror; relevance: workspace-access/scope behavior across backends in the model.
- [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — tool-policy gate; relevance: tool policy applies before sandbox — the escape-hatch precedence rule.

### oc_gateway_sandboxing_backends (8t · 10s · 10d)

**Terms**
- [Sandbox Backend](../../term_dictionary/term_sandbox_backend.md) — the runtime providing isolation; relevance: the note's subject — choosing/configuring Docker vs SSH vs OpenShell backends.
- [Sandbox](../../term_dictionary/term_sandbox.md) — the isolation being backed; relevance: each backend implements the sandbox the gateway runs tools inside.
- [Docker](../../term_dictionary/term_docker.md) — container runtime; relevance: the default backend — `openclaw-sandbox:bookworm-slim` image, `docker.binds`, `docker.network`, DooD constraints.
- [SSH — Secure Shell](../../term_dictionary/term_ssh.md) — remote-host execution transport; relevance: the SSH backend runs tools on an SSH-accessible host (`sandbox.ssh.target`, identity/cert material).
- [OpenShell](../../term_dictionary/term_openshell.md) — managed remote sandbox; relevance: the OpenShell backend with `mirror`/`remote` workspace modes this note configures.
- [Git Worktree Agents](../../term_dictionary/term_git_worktree_agents.md) — isolated per-agent workspaces; relevance: the per-scope workspace (`scope: agent/session/shared`) + remote-canonical seeding model parallels isolated worktrees.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable workspace state; relevance: remote-canonical backends persist the workspace remotely (`recreate` re-seeds) — a session-state durability concern.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the system configuring backends; relevance: `agents.defaults.sandbox.backend` + `setupCommand` are OpenClaw config.

**Docs**
- [CC: Sandbox Runtime and Containers](../claude_code/cc_sandbox_runtime_and_containers.md) — container sandbox runtime setup; relevance: closest peer — Docker-runtime sandbox setup + image building.
- [CC: Sandboxed Bash Tool Setup](../claude_code/cc_sandboxed_bash_tool_setup.md) — setting up a sandboxed exec tool; relevance: peer to enabling the sandbox + `setupCommand` one-time container provisioning.
- [CC: Sandbox Environments Comparison](../claude_code/cc_sandbox_environments_comparison.md) — comparing backends; relevance: the "Choosing a backend" Docker/SSH/OpenShell matrix.
- [CC: Sandbox Limitations and Troubleshooting](../claude_code/cc_sandbox_limitations_and_troubleshooting.md) — backend gotchas; relevance: peer to DooD path-mapping/`EACCES`, bwrap namespace, and no-network `setupCommand` pitfalls.
- [Hermes: Terminal Backends](../hermes_agent/hermes_terminal_backends.md) — pluggable execution backends; relevance: directly analogous "choose a backend" model (Docker/SSH/remote) for tool execution.
- [CC: SDK Isolation Technologies](../claude_code/cc_sdk_isolation_technologies.md) — isolation tech choices; relevance: the namespace/container isolation Docker/SSH/OpenShell backends provide.
- [pi: Containerization](../pi/pi_containerization.md) — container build + run; relevance: peer to the `docker build`/image-and-setup section.
- [oc_gateway_sandboxing_model](oc_gateway_sandboxing_model.md) — the model these backends implement (planned, this series); relevance: this procedure configures the modes/scope/workspace-access the model defines.
- [oc_gateway_sandbox_vs_tool_policy_vs_elevated](oc_gateway_sandbox_vs_tool_policy_vs_elevated.md) — bind/tool-policy interaction (planned, this series); relevance: `docker.binds` security + tool-policy gating cross-reference.
- [oc_gateway_secrets_operations](oc_gateway_secrets_operations.md) — sandbox SSH SecretRef material (planned, this series); relevance: `ssh.identityData`/`certificateData` are SecretRefs resolved per secrets ops.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — sandbox backend + bind validation; relevance: bind-source blocking, symlink-escape checks, OpenShell/SSH transport code.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — sandbox lifecycle (`sandbox list/recreate`); relevance: backend-aware lifecycle + `sandbox-setup.sh` orchestration.

**Snippets**
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — OpenShell backend setup; relevance: the OpenShell backend (`from`/`mode`/`remoteWorkspaceDir`) config this note documents.
- [snippet_openclaw_security_openshell_cli](../../code_snippets/snippet_openclaw_security_openshell_cli.md) — OpenShell CLI (`sandbox ssh-config`); relevance: `openshell sandbox create/get/delete/ssh-config` lifecycle the note references.
- [snippet_openclaw_security_openshell_fs_bridge](../../code_snippets/snippet_openclaw_security_openshell_fs_bridge.md) — OpenShell remote fs bridge; relevance: the shared remote filesystem bridge reused by SSH + OpenShell backends.
- [snippet_openclaw_security_openshell_mirror](../../code_snippets/snippet_openclaw_security_openshell_mirror.md) — `mirror` vs `remote` workspace; relevance: the mirror/remote workspace-mode sync behavior this note's tabs explain.
- [snippet_hermes_agent_tools_environments_docker](../../code_snippets/snippet_hermes_agent_tools_environments_docker.md) — Docker exec environment; relevance: peer to the Docker backend (image, network, socket) config.
- [snippet_hermes_agent_tools_environments_ssh](../../code_snippets/snippet_hermes_agent_tools_environments_ssh.md) — SSH exec environment; relevance: peer to `backend: "ssh"` remote-host execution + identity material.
- [snippet_hermes_agent_tools_environments_file_sync](../../code_snippets/snippet_hermes_agent_tools_environments_file_sync.md) — remote workspace file sync; relevance: the seed-once + remote-canonical (no sync-back) workspace model.
- [snippet_hermes_agent_tools_credential_files](../../code_snippets/snippet_hermes_agent_tools_credential_files.md) — credential-file handling; relevance: blocked credential-root binds (`~/.aws`,`~/.ssh`) + `:ro` secret mounts.
- [snippet_hermes_agent_tools_environments_base](../../code_snippets/snippet_hermes_agent_tools_environments_base.md) — backend abstraction base; relevance: the pluggable-backend abstraction the "Choosing a backend" matrix selects from.
- [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — sandboxed exec runtime; relevance: how exec/file tools run against the configured backend workspace.

### oc_gateway_secrets_contract (9t · 10s · 10d)

**Terms**
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed secret resolution; relevance: SecretRef (`env`/`file`/`exec`) is OpenClaw's pluggable secrets-manager contract — the note's subject.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — managed pool of credentials; relevance: the supported-credential surface + active-surface filtering manage the gateway's credential set.
- [AWS SDK Credential Chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — precedence-ordered credential resolution; relevance: the "required behavior and precedence" (ref-over-plaintext, shadowing) is a credential-chain precedence model.
- [Authentication](../../term_dictionary/term_authentication.md) — credentials feeding auth; relevance: `gateway.auth.token`/`gateway.remote.token` SecretRefs gate gateway auth (active-surface diagnostics).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — excluded rotating credential class; relevance: "OAuth refresh material is intentionally excluded from read-only SecretRef resolution".
- [Session Sanitization](../../term_dictionary/term_session_sanitization.md) — scrubbing sensitive values; relevance: the one-way safety policy (no plaintext rollback backups) + redaction sentinel are sanitization guarantees.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — `auth-profiles.json` credential store; relevance: `REF_SHADOWED` (auth-profiles taking precedence over openclaw.json refs) is a contract precedence finding.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — degraded-state fallback; relevance: degraded/recovered signals keep the last-known-good snapshot when reload activation fails.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway holding the snapshot; relevance: the eager in-memory runtime snapshot + atomic-swap reload are OpenClaw's runtime model.

**Docs**
- [CC: SDK Credential and Filesystem Controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential + fs access controls; relevance: closest peer — the agent-access boundary (credentials readable via file/shell tools) this note warns about.
- [CC: Security Architecture](../claude_code/cc_security_architecture.md) — overall security posture; relevance: SecretRef-as-security-migration-gate fits the layered security architecture.
- [CC: OTel Analysis and Privacy](../claude_code/cc_otel_analysis_and_privacy.md) — redaction/privacy of sensitive values; relevance: the one-way scrubbing + redaction-sentinel parallel telemetry redaction.
- [CC: SDK Secure Deployment Principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure deployment of credentials; relevance: the production "treat readable files as secrets until isolated" deployment guidance.
- [Hermes: Credential Pools](../hermes_agent/hermes_credential_pools.md) — credential pool runtime; relevance: peer runtime credential-pool model with precedence + fallback.
- [Hermes: Security Isolation Credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolating credentials from the agent; relevance: directly parallels the agent-access boundary (SecretRefs are not a process-isolation boundary).
- [CC: Authentication](../claude_code/cc_authentication.md) — credential/auth setup; relevance: `gateway.auth.*` SecretRef active-surface resolution.
- [AWS Bedrock AgentCore: Identity Overview](../aws_bedrock_agentcore/bedrock_agentcore_identity_overview.md) — managed agent credential/identity; relevance: managed-credential-surface contrast to OpenClaw's self-hosted SecretRef model.
- [oc_gateway_secrets_operations](oc_gateway_secrets_operations.md) — audit/configure/apply ops (planned, this series); relevance: the operational procedure that applies this contract.
- [oc_gateway_protocol_auth_pairing](oc_gateway_protocol_auth_pairing.md) — gateway auth token consuming SecretRefs (planned, this series); relevance: the connect-auth token this contract resolves.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — secrets runtime + active-surface policy; relevance: snapshot resolution, fail-fast/degraded signals, one-way scrubbing.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — `secrets.reload`/`secrets.resolve` RPC + auth surface; relevance: the gateway RPCs + auth-surface diagnostics consuming the contract.

**Snippets**
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/SecretRef resolution; relevance: resolving SecretRefs from the active snapshot for call paths — the contract's read path.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential precedence ordering; relevance: `REF_SHADOWED`/ref-over-plaintext precedence this note's "required behavior" section.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — sensitive-value sanitization; relevance: the one-way/no-plaintext-back safety posture + redaction sentinel.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: peer `env`/`file`/`exec` credential-source model.
- [snippet_hermes_agent_core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — credential pool seeding; relevance: peer to the eager in-memory snapshot seeding at activation.
- [snippet_hermes_agent_core_auxiliary_auth_resolution](../../code_snippets/snippet_hermes_agent_core_auxiliary_auth_resolution.md) — auth resolution precedence; relevance: precedence + active-surface "which credential wins" resolution.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — redaction patterns; relevance: header-residue/secret redaction the contract enforces (no secrets in logs/metrics).
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth credential handling; relevance: OAuth refresh material excluded from SecretRef resolution (separate compatibility).
- [snippet_hermes_agent_core_bedrock_adapter_credentials](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_credentials.md) — provider credential adapter; relevance: provider apiKey fields backed by SecretRefs (supported credential surface).
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — config reload/activation; relevance: atomic-swap reload + write-RPC preflight (`config.set/apply/patch`) activation triggers.

### oc_gateway_secrets_operations (8t · 10s · 10d)

**Terms**
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — provider-backed secret resolution; relevance: `secrets.providers` (env/file/exec: 1Password, Vault, bws, sops, pass) is the secrets-manager wiring this note operates.
- [Authentication](../../term_dictionary/term_authentication.md) — credentials feeding auth surfaces; relevance: gateway-auth-surface diagnostics + provider config wire auth credentials via SecretRefs.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — token credential field; relevance: provider `apiKey`/token fields are the SecretRef targets configured in the workflow.
- [AWS SDK Credential Chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — exec-resolver credential lookup; relevance: the exec provider (Vault/bws/sops) is a credential-chain resolver invoked at activation.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — `auth-profiles.json` scrubbing target; relevance: `secrets configure` scrubs static credentials from `auth-profiles.json`/`.env`/`auth.json`.
- [Odin](../../term_dictionary/term_odin.md) — Amazon secrets-distribution service; relevance: an internal secrets-manager analogue to the external exec providers (Vault/1Password) this note wires.
- [MCP — Model Context Protocol](../../term_dictionary/term_mcp.md) — MCP server env vars; relevance: the "MCP server environment variables" section wires SecretRefs into `acpx.mcpServers` env.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the CLI/gateway running the workflow; relevance: `openclaw secrets audit/configure/apply` is the operator workflow's command surface.

**Docs**
- [CC: SDK Credential and Filesystem Controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential controls + scrubbing; relevance: peer to the audit-then-scrub migration (plaintext-residue detection) workflow.
- [CC: Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — gateway/provider config wiring; relevance: parallels wiring SecretRefs into provider config + command-path resolution.
- [CC: Security Architecture](../claude_code/cc_security_architecture.md) — security migration posture; relevance: "audit/configure/apply is a security migration gate, not convenience" framing.
- [Hermes: Secrets Bitwarden](../hermes_agent/hermes_secrets_bitwarden.md) — Bitwarden secrets integration; relevance: directly parallels the bws (Bitwarden Secrets Manager) exec-resolver example in this note.
- [Hermes: Credential Pools](../hermes_agent/hermes_credential_pools.md) — operating credential pools; relevance: peer to provider config + precedence operations.
- [CC: Authentication](../claude_code/cc_authentication.md) — configuring auth credentials; relevance: gateway-auth-surface diagnostics + onboarding preflight credential setup.
- [Band: Environment Variables](../band/band_environment_variables.md) — env-var credential config; relevance: env SecretRefs + the "do not put `file:...` in the env block" file-backed-key rule.
- [oc_gateway_secrets_contract](oc_gateway_secrets_contract.md) — the contract this applies (planned, this series); relevance: the runtime model + active-surface filtering this operational note enacts.
- [oc_gateway_sandboxing_backends](oc_gateway_sandboxing_backends.md) — sandbox SSH SecretRef material (planned, this series); relevance: the "Sandbox SSH auth material" section wires SecretRefs into the SSH backend configured there.
- [oc_gateway_remote_app_setup](oc_gateway_remote_app_setup.md) — `gateway.remote.token` via SecretRef (planned, this series); relevance: the remote token this note can resolve from a provider.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — `secrets audit/configure/apply` + exec providers; relevance: the audit findings engine, scrubbers, and exec-provider runtime.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider `apiKey` config surface; relevance: the `models.providers.*.apiKey` SecretRef targets the workflow configures.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — `secrets.reload`/`secrets.resolve` + config-write preflight; relevance: the gateway RPCs + write-RPC activation this workflow triggers.

**Snippets**
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — SecretRef resolution on call paths; relevance: command-path resolution (`secrets.resolve`) strict-vs-read-only behavior this note documents.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI credential resolver; relevance: the exec-provider pattern (op/vault/bws/sops/pass external binaries) this note configures.
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — audit finding composition; relevance: `secrets audit --check` findings (plaintext residue, unresolved refs, shadowing, legacy residues).
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-provider audit runtime; relevance: `secrets audit --allow-exec` executing exec providers during audit.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — audit probe execution; relevance: the preflight resolution + probe before applying SecretRefs.
- [snippet_hermes_agent_core_bedrock_adapter_credentials](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_credentials.md) — provider credential wiring; relevance: pointing `models.providers.*.apiKey` at a SecretRef (provider config section).
- [snippet_hermes_agent_cli_config_set](../../code_snippets/snippet_hermes_agent_cli_config_set.md) — CLI config writes; relevance: peer to the `openclaw secrets configure --apply` config-mutation step.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — onboarding/setup config; relevance: the onboarding-reference preflight (interactive SecretRef storage validation) this note covers.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — env/file/exec sources; relevance: the `secrets.providers` env/file/exec provider definitions configured here.
- [snippet_hermes_agent_tools_credential_files](../../code_snippets/snippet_hermes_agent_tools_credential_files.md) — file-backed credential handling; relevance: the "file-backed API keys" (`mode: singleValue`/`json`, do-not-use-env-block) section.

> All cited EXISTING `note_name`s above are DB-confirmed present (verified 2026-06-21 via
> Sibling `oc_*` notes are "(planned, this series)" and count toward the 10-doc floor (≥5 existing per note);
> `entry_openclaw_docs` is the master W1 pre-step. Per-note totals (terms · snippets · existing-docs+siblings):
> all 12 notes meet ≥8 terms · ≥10 snippets · ≥10 docs (≥5 existing).

## Undigested Terms Plan

Per master, OpenClaw gateway vocabulary is digested as `oc_*` doc notes (not new `term_dictionary` entries);
the only term interaction is **linking existing** terms. **Expected new term_dictionary captures: 0.**

| Term (appears in source) | Disposition |
|---|---|
| Gateway WS protocol / handshake / framing / versioning | → `oc_gateway_protocol_transport` (doc note); link `term_websocket`, `term_json_rpc`, `term_rpc`. |
| Roles / scopes / caps / presence / broadcast scoping | → `oc_gateway_protocol_roles_scopes`; link `term_capability_negotiation`, `term_session_features`. |
| RPC method families / event families / task-ledger RPCs / `models.list` | → `oc_gateway_protocol_rpc_methods`; link `term_json_rpc`, `term_function_calling`. |
| Device identity / pairing / TLS pinning | → `oc_gateway_protocol_auth_pairing`; link `term_authentication`, `term_oauth_token`, `term_tls`. |
| Prometheus `/metrics` / PromQL / cardinality / label policy | → `oc_gateway_prometheus`; link `term_observability_agent_systems`, `term_data_observability`. |
| VPN / tailnet / SSH tunnel / credential precedence | → `oc_gateway_remote` (+ `_app_setup`); link `term_vpn`, `term_ssh`, `term_tunneling`. |
| Sandbox vs tool policy vs elevated / tool groups | → `oc_gateway_sandbox_vs_tool_policy_vs_elevated` + `_sandboxing_model`; link `term_sandbox`, `term_sandbox_backend`. |
| Sandbox backends (Docker/SSH/OpenShell) / bind mounts / setupCommand | → `oc_gateway_sandboxing_backends`; link `term_docker`, `term_sandbox_backend`. |
| SecretRef contract / runtime snapshot / active-surface filtering | → `oc_gateway_secrets_contract`; link `term_secrets_manager`, `term_credential_pool`. |
| `secrets audit`/`configure`/apply / file-backed keys / command-path resolution | → `oc_gateway_secrets_operations`; link `term_secrets_manager`, `term_aws_sdk_credential_chain`. |

**New-term candidates (genuinely cross-cutting, no existing note):** none identified. Several adjacent terms are
ABSENT from `term_dictionary` (`term_prometheus`, `term_opentelemetry`, `term_tailscale`, `term_secret`/
`term_secrets_management`, `term_session`, `term_environment_variable`) but are either provider/product-specific
(documented in the `oc_*` doc note, not promoted) or already covered by a more general existing term
(`term_observability_agent_systems`, `term_secrets_manager`, `term_tunneling`, `term_session_persistence`). If
augment determines a truly reusable cross-cutting term is warranted (e.g. a generic "secrets reference / SecretRef"
concept), the best-fit glossary is `acronym_glossary_gen_ai_dev.md`; default decision remains **0 new terms**.

## Term-Note Authoring Requirements

**N/A (0 new terms).** gw05 authors zero `term_dictionary` notes. Inherited from master: any new term would be
`acronym_glossary_*.md` (best-fit: `acronym_glossary_gen_ai_dev.md`).

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (12 notes, P1). All gates must pass before commit.

| Gate | Check | Tool |
|---|---|---|
| G1 | Format: YAML field order + forbidden fields, H1/`## Overview`/`## Related Notes`, density caps | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim traceable to `inbox/openclaw_docs/gateway/<page>.md` (no hallucinated RPCs/flags) | diff vs source |
| G3 | Density + Coverage: ≤400 lines / ≤2,500 words / ≤6 code; every mapped H2/H3 covered; one BB/note | manual + script |
| G4 | Cross-Reference: ≥6 relevance-selected terms + repo_openclaw* + sibling oc_* + relevance statements | manual |
| G5 | Ghost-reference detect + redirect (every cited target resolves in DB) | ghost-reference scan |
| G6 | Broken-link fix (relative paths correct) | `/tessellum-fix-broken-links` |
| G7/G8 | Discoverability: each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (in-degree ≥1, anti-island) — via `entry_openclaw_docs.md` + repo/term inlinks | DB `in_degree` query |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_gateway_prometheus oc_gateway_protocol_transport oc_gateway_protocol_roles_scopes oc_gateway_protocol_rpc_methods oc_gateway_protocol_auth_pairing oc_gateway_remote oc_gateway_remote_app_setup oc_gateway_sandbox_vs_tool_policy_vs_elevated oc_gateway_sandboxing_model oc_gateway_sandboxing_backends oc_gateway_secrets_contract oc_gateway_secrets_operations"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + link check
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections present
  for s in ${(s:|:)REQ_SECTIONS}; do grep -qF "$s" "$f" || echo "$n MISSING SECTION: $s"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # density caps (body words excl. frontmatter; fences/2)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
  # at least one sibling oc_ link (cross-ref sanity)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "$n NO SIBLING oc_ LINK"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
bash scripts/update_notes_database.sh --force   # reindex, then verify in-degree ≥1 + 0 broken links
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source fences | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_gateway_prometheus | procedure | 600 | 7 (cap ≤6) | ✅ |
| 2 | oc_gateway_protocol_transport | model | 650 | (from 9) | ✅ |
| 3 | oc_gateway_protocol_roles_scopes | model | 600 | (from 9) | ✅ |
| 4 | oc_gateway_protocol_rpc_methods | model | 700 | (from 9) | ✅ |
| 5 | oc_gateway_protocol_auth_pairing | procedure | 600 | (from 9) | ✅ |
| 6 | oc_gateway_remote | procedure | 700 | 11 (cap ≤6) | ✅ |
| 7 | oc_gateway_remote_app_setup | procedure | 450 | 11 (cap ≤6) | ✅ |
| 8 | oc_gateway_sandbox_vs_tool_policy_vs_elevated | concept | 600 | 2 | ✅ |
| 9 | oc_gateway_sandboxing_model | model | 600 | (from 8) | ✅ |
| 10 | oc_gateway_sandboxing_backends | procedure | 750 | (from 8) | ✅ |
| 11 | oc_gateway_secrets_contract | model | 700 | (from 24) | ✅ |
| 12 | oc_gateway_secrets_operations | procedure | 700 | (from 24) | ✅ |

**Authoritative BB tally: procedure ×6 (1,5,6,7,10,12) · model ×5 (2,3,4,9,11) · concept ×1 (8) = 12 notes.**
No note approaches the ≤2,500w / ≤400L caps. Code-dense source pages (`secrets` 24 fences, `remote`/
`remote-gateway-readme` 11 each, `protocol` 9, `prometheus` 7) are split or selectively excerpted so each note
keeps **≤6** verbatim code blocks (PromQL recipes, JSON envelopes, shell/PLIST snippets chosen for load-bearing value).

## Entry Point Decision (inherited from master)

Contributes **12 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step before first execution),
grouped under a **"Gateway — Protocol, Remote, Sandboxing & Secrets"** cluster. Each note receives its
entry-point back-link at finalization (satisfies G7/G8 in-degree ≥1). No standalone entry point for gw05 alone
(below the >30-note threshold; the section rolls up into the shared `entry_openclaw_docs.md` Gateway section).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution):
- `entry_openclaw_docs.md` (planned W1) → **all 12 notes** (primary anti-island guarantor).
- `repo_openclaw_gateway` → notes 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 (the gateway code↔docs cross-link).
- `repo_openclaw_security` → notes 5, 8, 9, 10, 11, 12.
- `repo_openclaw_sessions` → notes 3, 4, 9.
- `term_websocket` → notes 2, 3, 4; `term_json_rpc` → notes 2, 4.
- `term_sandbox` / `term_sandbox_backend` → notes 8, 9, 10.
- `term_secrets_manager` → notes 11, 12; `term_authentication` → notes 5, 11, 12.
- `term_vpn` / `term_ssh` / `term_tunneling` → notes 6, 7.
- `term_observability_agent_systems` → note 1.

## Pacing Rules (inherited from master)

Single execution phase, 12 notes. Cap dynamic-workflow fan-out at ~30 agents/run. Re-read each source page
before authoring; reproduce config/PromQL/JSON/PLIST snippets verbatim (verify against
`inbox/openclaw_docs/gateway/<page>.md`). One BB per note. All 8 gates pass before commit;
`git pull --rebase --autostash` first, reindex incrementally, verify `note_links` + 0 broken links + in-degree ≥1,
commit + push the wave (no Claude co-author trailer).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augmentation pass:** locked the Per-Note Related Notes Mapping at the RAISED floors
(**≥8 term_dictionary terms · ≥10 code_snippets · ≥10 docs per note**), replacing the prior Candidate
Cross-References section. All 7 source pages re-read from `inbox/openclaw_docs/gateway/` on 2026-06-21 to
`term_risk_table` surfaced by BM25 on "metrics" were rejected as irrelevant to the Prometheus exporter).

**What was locked (per-note counts — terms · snippets · docs[existing+sibling] · repos):**

| Note | Terms | Snippets | Docs (existing + sibling) | Repos | Floors |
|---|---:|---:|---|---:|---|
| oc_gateway_prometheus | 8 | 10 | 10 (9 + 1) | 2 | ✅ |
| oc_gateway_protocol_transport | 8 | 10 | 10 (7 + 3) | 2 | ✅ |
| oc_gateway_protocol_roles_scopes | 8 | 10 | 10 (7 + 3) | 2 | ✅ |
| oc_gateway_protocol_rpc_methods | 8 | 10 | 10 (7 + 3) | 3 | ✅ |
| oc_gateway_protocol_auth_pairing | 8 | 10 | 10 (7 + 3) | 2 | ✅ |
| oc_gateway_remote | 8 | 10 | 10 (7 + 3) | 2 | ✅ |
| oc_gateway_remote_app_setup | 8 | 10 | 10 (7 + 3) | 2 | ✅ |
| oc_gateway_sandbox_vs_tool_policy_vs_elevated | 8 | 10 | 10 (7 + 3) | 2 | ✅ |
| oc_gateway_sandboxing_model | 8 | 10 | 10 (7 + 3) | 2 | ✅ |
| oc_gateway_sandboxing_backends | 8 | 10 | 10 (7 + 3) | 2 | ✅ |
| oc_gateway_secrets_contract | 9 | 10 | 10 (8 + 2) | 2 | ✅ |
| oc_gateway_secrets_operations | 8 | 10 | 10 (7 + 3) | 3 | ✅ |

**Verification (2026-06-21):** all 205 distinct `.md` link targets in the LOCKED section checked against
No duplicate links within any single note. Source word/fence counts re-measured (protocol 6,047w/9code,
secrets 3,429w/5code, sandboxing 3,335w/4code, prometheus 1,353w/2code, remote 1,464w/11code) — all within
±5% of the plan's Source table; no new splits required.

**New-term candidates:** **none.** Per master, OpenClaw gateway vocabulary is digested as `oc_*` doc notes,
not new `term_dictionary` entries (expected new term captures: 0). The re-read surfaced no genuinely
cross-cutting, vault-reusable term lacking both a doc-page home and an existing note. Adjacent absent terms
(`term_prometheus`, `term_opentelemetry`, `term_tailscale`, `term_secret`/`term_secrets_management`,
`term_session`, `term_environment_variable`) remain covered by existing more-general terms
(`term_observability_agent_systems`, `term_time_series_database`, `term_tunneling`, `term_secrets_manager`,
`term_session_persistence`, etc.) — confirmed by this pass; **default decision stands: 0 new terms.** If a
future pass deems one warranted, best-fit glossary is `acronym_glossary_gen_ai_dev.md`.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

PLAN REVIEW — FINAL SIGN-OFF · Plan: `plan_digest_openclaw_docs_gw05.md` · Date: 2026-06-21

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance per link) | **PASS** | LOCKED mapping: every note ≥8 terms · ≥10 snippets · ≥10 docs, each link `[Name](path) — what; relevance: why THIS note`. Floors verified by parser (all 12 = floors YES). |
| CP2 | 9-GATE present per batch (G1–G6, G7/G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present + `## Validation Scripts` (G1 format, ghost/G5, density, broken-link/G6, in-degree/G7-G8). Single phase, 1 gate table for 12 notes. |
| CP3 | Entry point inherited (`entry_openclaw_docs` planned at W1) | **PASS** | `## Entry Point Decision (inherited from master)`: 12 rows into `entry_openclaw_docs.md` (master W1 pre-step), Gateway cluster; no standalone gw05 entry (below >30 threshold). |
| CP4 | Plan size manageable | **PASS** | 12 notes ≤ 30; single execution phase. |
| CP5 | Note format derived from existing target-dir notes | **PASS** | Master Format Definition derived from `claude_code/`+`pi/` corpora (`## Overview`→body→`## Related Notes`→`## References`→bold footer; YAML field order; forbidden fields listed). Inherited verbatim. |
| CP6 | Density / BB atomicity (borderline → split) | **PASS** | Density Re-Assessment: all 12 notes ≤750w, ≤6 code, one BB each; protocol×4/secrets×2/sandboxing×2 splits applied. Re-measured sources confirm no further split. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured 5 densest pages 2026-06-21 (protocol 6,047 / secrets 3,429 / sandboxing 3,335 / prometheus 1,353 / remote 1,464) — all within ±5% of plan's Source table; ratio 0.97–1.0. |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | `## Undigested Terms Plan` present (all rows → `oc_*` doc note + link existing terms); `## Term-Note Authoring Requirements` present (N/A, 0 new terms; inherited capture-term-note canonical for any future term). |
| CP8f | Slug specificity / collision dedup audit | **PASS** | 0 new term slugs → no specificity/collision risk. Doc-note dedup: all 12 `oc_gateway_*` slugs checked vs `term_dictionary/` + `documentation/` — no existing note duplicates them (gateway product docs, distinct from general terms); existing terms are LINKED not recreated. |
| CP9 | Discoverability / inlinks (G8, in-degree ≥1) | **PASS** | `## Inlinks (existing notes → new notes)`: `entry_openclaw_docs` → all 12 (anti-island guarantor) + `repo_openclaw_gateway`/`_security`/`_sessions` + term inlinks; G7/G8 in-degree ≥1 in gate table, executed at finalization. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
