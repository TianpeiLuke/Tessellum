---
title: Sub-Plan gw04 — OpenClaw Docs: Gateway (multi-gateway, HTTP APIs, OpenShell, OpenTelemetry, scopes, pairing)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - gateway/multiple-gateways
  - gateway/openai-http-api
  - gateway/openresponses-http-api
  - gateway/openshell
  - gateway/opentelemetry
  - gateway/operator-scopes
  - gateway/pairing
---

# Sub-Plan gw04: Gateway

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_<topic>_*` prefix), format/YAML, dedup-before-create
> (term_dictionary + documentation/ + repo_openclaw*), 9-GATE, cross-references, and entry-point wiring are ALL
> inherited from the master and are not re-derived here.

## Scope

The seven `gateway/*` pages covering Gateway operational surfaces beyond core config/auth: running **multiple
isolated Gateways** on one host (profiles/ports), the two OpenAI-compatible **HTTP API endpoints**
(`/v1/chat/completions` and `/v1/responses`), the **OpenShell** managed-sandbox backend, **OpenTelemetry** export
(setup + the full metric/span/event catalog), the **operator-scope** authorization model, and **Gateway-owned
node pairing**. Priority **P1 (Phase A)** — these define the Gateway's external integration contracts (HTTP/OTLP),
its authorization vocabulary (operator scopes), and its pairing/identity boundary, which the channels, tools, CLI,
and platforms corpora reference. The code-side counterparts `repo_openclaw_gateway` / `repo_openclaw_security` /
`repo_openclaw_sessions` are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 10,377 measured words. **Planned: 8 notes** (opentelemetry.md splits into 2).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| multiple-gateways | gateway/multiple-gateways | 866 | 6 | 11 | 0 | procedure |
| openai-http-api | gateway/openai-http-api | 2,188 | 9 | 14 | 5 | procedure (HTTP-endpoint contract) |
| openresponses-http-api | gateway/openresponses-http-api | 1,489 | 7 | 13 | 3 | procedure (HTTP-endpoint contract) |
| openshell | gateway/openshell | 1,242 | 8 | 11 | 7 | procedure |
| opentelemetry | gateway/opentelemetry | 2,570 | 8 | 10 | 10 | mixed (split: setup procedure vs metric/span/event model) |
| operator-scopes | gateway/operator-scopes | 734 | 0 | 6 | 0 | concept (authorization model) |
| pairing | gateway/pairing | 1,288 | 2 | 13 | 0 | procedure |

(Code = raw ``` fence count ÷ 2. Word counts measured via `wc -w` on the mirror, frontmatter included; body-only
counts are marginally lower, so the 2,500-word density cap is assessed on body words at execution.)

## Content Strategy

- **Prioritize**: the HTTP-API auth/security boundary + agent-first model contract (both HTTP endpoints share it —
  every external integration depends on it), the operator-scope levels + approval-time-check model (the
  authorization vocabulary the whole Gateway control plane uses), and the OpenTelemetry signal catalog (exact
  metric/span/attribute names operators need to build dashboards).
- **Split**: `opentelemetry.md` (2,570w, mixed BB) → a setup/config **procedure** note (how to enable, configure,
  sample, privacy-control, disable) + a metric/span/event-catalog **model** note (the exact exported telemetry
  shapes). The split is forced by the word cap AND the BB boundary (setup how-to vs reference data model).
- **Keep 1 note each**: multiple-gateways (single isolation procedure), openai-http-api and
  openresponses-http-api (one endpoint contract each — kept separate because they are sibling reference pages with
  distinct request shapes; openresponses adds item-based input + image/file handling), openshell (one
  backend-setup procedure), operator-scopes (one authorization model), pairing (one node-pairing procedure).
- **Link-out, do not redefine**: `gateway/configuration-reference` / `gateway/security` / `gateway/sandboxing` /
  `gateway/trusted-proxy-auth` / `gateway/protocol` (other gw sub-plans gw02/gw05/gw06/gw07) are cross-linked, not
  duplicated; `gateway/logging` + top-level `logging` (gw03/rt02) referenced from the OTel notes; provider
  `providers/openai` linked from the HTTP-API notes; `term_mcp`/`term_llm`/`term_oauth_token`/`term_sandbox`/
  `term_sse` linked, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_gateway_multiple_gateways.md` | procedure | multiple-gateways.md (all 10 content H2: Best recommended setup, Rescue-Bot Quickstart, Why this works, What `--profile rescue onboard` Changes, General multi-gateway setup, Isolation checklist, Port mapping, Browser/CDP notes, Manual env example, Quick checks) | 600 | Running multiple isolated OpenClaw Gateways on one host: the rescue-bot quickstart, per-profile config/state/workspace/port isolation, the derived browser/canvas/CDP port mapping, and the `gateway status --deep`/`probe` checks. |
| 2 | `oc_gateway_openai_http_api.md` | procedure | openai-http-api.md (Auth, Security boundary, When to use, Agent-first model contract, Enabling/Disabling, Session behavior, Why this surface matters, Model list and agent routing, Streaming SSE, Chat tool contract + 5 H3, Open WebUI quick setup, Examples) | 750 | Exposing the Gateway's OpenAI-compatible `/v1/chat/completions` (plus `/v1/models`, `/v1/embeddings`) endpoint: enabling it, the full-operator-access security boundary, the agent-target `model` contract (`openclaw/<agentId>`, `x-openclaw-model`), SSE streaming, the function-tool subset, and Open WebUI setup. |
| 3 | `oc_gateway_openresponses_http_api.md` | procedure | openresponses-http-api.md (Auth/security/routing, Session behavior, Request shape, Items (input) + 3 H3, Tools, Images, Files, File+image limits, Streaming SSE, Usage, Errors, Examples) | 700 | Exposing the Gateway's OpenResponses-compatible `/v1/responses` endpoint: item-based `input`, client function-tools, `input_image`/`input_file` handling (MIME/size limits, untrusted-content wrapping, PDF extraction), the `response.*` SSE event sequence, usage normalization, and config limits. |
| 4 | `oc_gateway_openshell.md` | procedure | openshell.md (Prerequisites, Quick start, Workspace modes + 3 H3 mirror/remote/choosing, Configuration reference, Examples + 3 H3, Lifecycle management + When to recreate, Security hardening, Current limitations, How it works) | 650 | Using OpenShell as a managed remote-sandbox backend instead of local Docker: installing the plugin, choosing `mirror` vs `remote` workspace mode, the `plugins.entries.openshell.config` reference, sandbox lifecycle/recreate, and the SSH-bridge security hardening. |
| 5 | `oc_gateway_opentelemetry_setup.md` | procedure | opentelemetry.md: How it fits together, Quick start, Signals exported, Configuration reference + Environment variables H3, Privacy and content capture, Sampling and flushing, Without an exporter, Disable | 650 | Enabling OpenClaw's `diagnostics-otel` OTLP/HTTP export: install/enable, the `diagnostics.otel` config + env-var overrides, traces/metrics/logs toggles, the privacy/content-capture controls, sampling/flush tuning, running diagnostics without an exporter, and disabling. |
| 6 | `oc_gateway_opentelemetry_signals.md` | model | opentelemetry.md: Exported metrics (Model usage, Message flow, Talk, Queues and sessions, Session liveness telemetry, Harness lifecycle, Tool execution, Exec, Diagnostics internals), Exported spans, Diagnostic event catalog | 700 | The exact OpenClaw telemetry catalog: every exported metric (name/type/attributes) across model-usage, message-flow, Talk, queue/session, harness, tool, and exec families, the span set with their attributes, the session-liveness state model, and the underlying diagnostic event catalog. |
| 7 | `oc_gateway_operator_scopes.md` | concept | operator-scopes.md (Roles, Scope levels, Method scope is only the first gate, Device pairing approvals, Node pairing approvals, Shared-secret auth) | 550 | The Gateway operator-authorization model: the `operator`/`node` roles, the six `operator.*` scope levels, the two-stage gate (method scope then approval-time checks), how device/node pairing approvals derive required scopes, and shared-secret-auth full-operator restoration. |
| 8 | `oc_gateway_pairing.md` | procedure | pairing.md (Concepts, How pairing works, CLI workflow, API surface, Node command gating, Node event trust boundaries, Auto-approval macOS, Trusted-CIDR auto-approval, Metadata-upgrade auto-approval, QR pairing helpers, Locality and forwarded headers, Storage, Transport behavior) | 700 | Gateway-owned node pairing: the pending/paired/token lifecycle, the `openclaw nodes` CLI + `node.pair.*` protocol methods/events, the 2026.3.31+ node-command-gating and trust-boundary changes, the auto-approval paths (silent, trusted-CIDR, metadata-upgrade), forwarded-header locality rules, and private storage. |

## Section Coverage Map

```
multiple-gateways.md
├── Best recommended setup ───────────────────── → note 1 (oc_gateway_multiple_gateways)
├── Rescue-Bot Quickstart ────────────────────── → note 1
├── Why this works ───────────────────────────── → note 1
├── What `--profile rescue onboard` Changes ───── → note 1
├── General multi-gateway setup ──────────────── → note 1
├── Isolation checklist ──────────────────────── → note 1
├── Port mapping (derived) ───────────────────── → note 1
├── Browser/CDP notes (common footgun) ───────── → note 1
├── Manual env example ───────────────────────── → note 1
├── Quick checks ─────────────────────────────── → note 1
└── Related (link-out) ───────────────────────── → note 1 References
openai-http-api.md
├── (preamble: /v1 endpoints served) ─────────── → note 2 (oc_gateway_openai_http_api) Overview
├── Authentication ───────────────────────────── → note 2
├── Security boundary (important) + Auth matrix ─ → note 2
├── When to use this endpoint ────────────────── → note 2
├── Agent-first model contract ───────────────── → note 2
├── Enabling / Disabling the endpoint ────────── → note 2
├── Session behavior ─────────────────────────── → note 2
├── Why this surface matters ─────────────────── → note 2
├── Model list and agent routing (Accordions) ── → note 2
├── Streaming (SSE) ──────────────────────────── → note 2
├── Chat tool contract (Supported/Unsupported,
│   Non-streaming/Streaming shapes, Follow-up) ─ → note 2
├── Open WebUI quick setup ───────────────────── → note 2
├── Examples ─────────────────────────────────── → note 2
└── Related (link-out) ───────────────────────── → note 2 References
openresponses-http-api.md
├── (preamble: /v1/responses) ────────────────── → note 3 (oc_gateway_openresponses_http_api) Overview
├── Authentication, security, and routing ────── → note 3 (defers shared bits to note 2)
├── Session behavior ─────────────────────────── → note 3
├── Request shape (supported) ────────────────── → note 3
├── Items (input): message / function_call_output
│   / reasoning & item_reference ─────────────── → note 3
├── Tools (client-side function tools) ───────── → note 3
├── Images (`input_image`) ───────────────────── → note 3
├── Files (`input_file`) ─────────────────────── → note 3
├── File + image limits (config) ─────────────── → note 3
├── Streaming (SSE) ──────────────────────────── → note 3
├── Usage / Errors / Examples ────────────────── → note 3
└── Related (link-out) ───────────────────────── → note 3 References
openshell.md
├── (preamble: managed sandbox backend) ──────── → note 4 (oc_gateway_openshell) Overview
├── Prerequisites ────────────────────────────── → note 4
├── Quick start ──────────────────────────────── → note 4
├── Workspace modes: mirror / remote / choosing ─ → note 4
├── Configuration reference ──────────────────── → note 4
├── Examples: minimal / mirror+GPU / per-agent ── → note 4
├── Lifecycle management / When to recreate ──── → note 4
├── Security hardening ───────────────────────── → note 4
├── Current limitations ──────────────────────── → note 4
├── How it works ─────────────────────────────── → note 4
└── Related (link-out) ───────────────────────── → note 4 References
opentelemetry.md
├── (preamble: diagnostics-otel, OTLP/HTTP) ──── → note 5 (oc_gateway_opentelemetry_setup) Overview
├── How it fits together ─────────────────────── → note 5
├── Quick start ──────────────────────────────── → note 5
├── Signals exported (Metrics/Traces/Logs table) → note 5
├── Configuration reference + Environment vars ── → note 5
├── Privacy and content capture ──────────────── → note 5
├── Sampling and flushing ────────────────────── → note 5
├── Without an exporter ──────────────────────── → note 5
├── Disable ──────────────────────────────────── → note 5
├── Exported metrics (Model usage, Message flow,
│   Talk, Queues and sessions, Session liveness
│   telemetry, Harness lifecycle, Tool execution,
│   Exec, Diagnostics internals) ─────────────── → note 6 (oc_gateway_opentelemetry_signals)
├── Exported spans ───────────────────────────── → note 6
├── Diagnostic event catalog ─────────────────── → note 6
└── Related (link-out) ───────────────────────── → notes 5 & 6 References
operator-scopes.md
├── (preamble: scopes = control-plane guardrail) → note 7 (oc_gateway_operator_scopes) Overview
├── Roles ────────────────────────────────────── → note 7
├── Scope levels (table) ─────────────────────── → note 7
├── Method scope is only the first gate ──────── → note 7
├── Device pairing approvals ─────────────────── → note 7
├── Node pairing approvals ───────────────────── → note 7
└── Shared-secret auth ───────────────────────── → note 7
pairing.md
├── (preamble: Gateway-owned pairing) ────────── → note 8 (oc_gateway_pairing) Overview
├── Concepts ─────────────────────────────────── → note 8
├── How pairing works ────────────────────────── → note 8
├── CLI workflow (headless friendly) ─────────── → note 8
├── API surface (gateway protocol) + Warning ─── → note 8
├── Node command gating (2026.3.31+) ─────────── → note 8
├── Node event trust boundaries (2026.3.31+) ─── → note 8
├── Auto-approval (macOS app) ────────────────── → note 8
├── Trusted-CIDR device auto-approval ────────── → note 8
├── Metadata-upgrade auto-approval ───────────── → note 8
├── QR pairing helpers ───────────────────────── → note 8
├── Locality and forwarded headers ───────────── → note 8
├── Storage (local, private) ─────────────────── → note 8
├── Transport behavior ───────────────────────── → note 8
└── Related (link-out) ───────────────────────── → note 8 References
```
No orphaned sections. Cross-cutting topics (configuration-reference, security, sandboxing, trusted-proxy-auth,
protocol, logging, providers/openai) are linked to their owning sub-plans, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| opentelemetry.md (2,570w, 10 H2 / 10 H3, mixed BB) | notes 5 (`oc_gateway_opentelemetry_setup`, procedure) + 6 (`oc_gateway_opentelemetry_signals`, model) | Exceeds the 2,500-word cap AND mixes two building blocks: an enable/configure/tune **procedure** (Quick start, Configuration reference, Privacy, Sampling, Disable) and a **reference data model** (Exported metrics/spans + Diagnostic event catalog — ~50 metric names with attribute lists, ~17 span shapes). Split per word-cap + mixed-BB rules; each half stays ≤700w and ≤6 code blocks. |
| openai-http-api.md (2,188w) | note 2 (single) | Under the 2,500-word cap and a single building block (one HTTP-endpoint contract: auth + model contract + tool contract). Kept whole; the 9 code fences reproduce selectively to stay ≤6. Not split — would fragment one endpoint's contract. |

All other pages are 1 note each (each ≤2,188w, single BB).

## Summary Statistics & Building Block Distribution

- Source pages: **7** (10,377 measured words). New `oc_` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×5** (notes 1, 2, 3, 4, 8) · **model ×1** (note 6) · **concept ×1** (note 7) ·
  the OTel pair contributes 1 procedure (note 5) + 1 model (note 6).
  Totals: procedure 6, model 1, concept 1.
- Est. digest words ~5,300 (avg ~660/note). The 40 source code fences distribute across the procedure/model
  notes; each note kept ≤6 (config snippets reproduced selectively, verbatim — e.g. the OTel config-reference
  block is reproduced once in note 5, the responses limits block once in note 3).
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** per-note mapping in
  [## Per-Note Related Notes Mapping (LOCKED)](#per-note-related-notes-mapping-locked--xref-augment-2026-06-21)
  meets the raised floors — **≥8 terms · ≥10 snippets · ≥10 docs per note** (PLUS 3 `repo_openclaw*` each + sibling

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

(PLUS relevant `repo_openclaw*` + sibling `oc_*`. Sibling `oc_*` docs in this series do not exist yet → cited as
snippets, repos, and the EXISTING docs were confirmed present in the unified DB via `sqlite3` on 2026-06-21.
Relative paths are written FROM `resources/documentation/openclaw/oc_*.md`: term →
`../../term_dictionary/term_Y.md`; sibling oc_ → `oc_Y.md`; other doc → `../<folder>/<file>.md`; repo →
`../../../areas/code_repos/repo_Y.md`; snippet → `../../code_snippets/snippet_Y.md`; analysis →
`../../analysis_thoughts/<file>.md`.)

### oc_gateway_multiple_gateways (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted gateway connecting chat platforms to coding agents; relevance: this note runs more than one OpenClaw Gateway on one host.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — managed store for credentials/state; relevance: each profile needs an isolated `OPENCLAW_STATE_DIR` holding per-instance creds/sessions.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session/state across restarts; relevance: per-profile state dirs keep each Gateway's sessions independent.
- [Cron](../../term_dictionary/term_cron.md) — scheduled/managed background jobs; relevance: each profile installs its own managed service (`gateway install`) under a distinct service name.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting/forwarding network layer; relevance: `gateway probe` treats one Gateway reachable through SSH tunnel/proxy URL as one identity, not many.
- [Proxy Pattern](../../term_dictionary/term_proxy_pattern.md) — indirection/transport façade; relevance: distinguishes "one gateway, multiple transports" from genuinely separate isolated instances.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional transport; relevance: each Gateway serves its WS+HTTP multiplex on a unique base port.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: derived browser/canvas/CDP ports per instance avoid sandbox/browser-control collisions.

**Docs**
- [oc_gateway_pairing](oc_gateway_pairing.md) — Gateway-owned node pairing (planned, this series); relevance: remote-mode nodes must pair against the correct isolated Gateway instance.
- [oc_gateway_openshell](oc_gateway_openshell.md) — managed sandbox backend (planned, this series); relevance: each isolated instance scopes its own sandbox lifecycle.
- [oc_gateway_operator_scopes](oc_gateway_operator_scopes.md) — operator authorization model (planned, this series); relevance: separate Gateways under separate OS users is the recommended hard trust boundary vs scopes.
- [hermes_profile_gateways_services](../hermes_agent/hermes_profile_gateways_services.md) — multi-profile gateways + services in the sibling tool; relevance: direct analog of OpenClaw per-profile gateway/service isolation.
- [hermes_profiles_multi_agent](../hermes_agent/hermes_profiles_multi_agent.md) — multiple agent profiles on one host; relevance: same named-profile isolation pattern OpenClaw uses for multi-gateway.
- [hermes_faq_messaging_perf_profiles_workflows](../hermes_agent/hermes_faq_messaging_perf_profiles_workflows.md) — profile/perf operational FAQ; relevance: parallels OpenClaw's "when to run multiple instances" guidance.
- [hermes_docker_volumes_supervision](../hermes_agent/hermes_docker_volumes_supervision.md) — per-instance volumes + process supervision; relevance: analog to per-profile state-dir/workspace isolation.
- [cc_sdk_isolation_technologies](../claude_code/cc_sdk_isolation_technologies.md) — isolation technologies for agent runtimes; relevance: conceptual backing for instance-level isolation vs in-process scopes.
- [cc_sdk_hosting_provisioning_and_scaling](../claude_code/cc_sdk_hosting_provisioning_and_scaling.md) — hosting/provisioning multiple runtimes; relevance: parallels running several long-lived Gateways for different roles/tenants.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network access/ports/TLS; relevance: backing concept for the derived-port mapping and loopback-only browser-control port.
- [pi_containerization](../pi/pi_containerization.md) — containerized isolated runtimes; relevance: another isolated-instance pattern paralleling separate Gateways.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway install/port/profile lifecycle; relevance: implements `gateway install`, `--port`, profile state, and probe.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — `onboard`/`setup` flows; relevance: `--profile rescue onboard` writes a separate profile via this code.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — managed-service install; relevance: implements the per-profile managed launchd/systemd/schtasks service.

**Snippets**
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — per-profile gateway compile-cache + respawn; relevance: each profile runs an independent gateway process.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — probe/transport identity over proxy; relevance: `probe` "multiple reachable gateway identities" logic.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: `OPENCLAW_CONFIG_PATH`/`OPENCLAW_STATE_DIR`/`OPENCLAW_GATEWAY_PORT` per instance.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WS listen on the gateway port; relevance: the base port each instance binds uniquely.
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — config reload planning; relevance: per-profile config file drives each instance.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: applies per-instance config without cross-instance races.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist render; relevance: per-profile macOS managed service name/port.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render/parse; relevance: per-profile Linux managed service.
- [snippet_openclaw_daemon_schtasks_argv_render](../../code_snippets/snippet_openclaw_daemon_schtasks_argv_render.md) — schtasks argv render; relevance: per-profile Windows managed service.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervision; relevance: keeps each isolated gateway process alive.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — service/cron notifications; relevance: stale-service detection backing `gateway status --deep`.

### oc_gateway_openai_http_api (9t · 11s · 12d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: exposes the OpenAI-compatible `/v1/chat/completions` surface.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: requests run as a Gateway agent turn backed by an LLM provider.
- [SSE](../../term_dictionary/term_sse.md) — Server-Sent Events streaming; relevance: `stream: true` yields `text/event-stream` chunks ending in `data: [DONE]`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-emitted structured tool calls; relevance: the chat tool contract (`tools`/`tool_choice`/`tool_calls`).
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — the newer agent-native endpoint; relevance: `/v1/responses` is served alongside chat-completions and shares the agent-target model contract.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the four `gateway.auth.mode` paths (token/password/trusted-proxy/none).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: `Authorization: Bearer <token>` is the shared-secret operator credential here.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: `gateway.auth.rateLimit` returns `429` with `Retry-After` on auth-failure storms.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model providers; relevance: `x-openclaw-model` overrides the backend provider/model for the selected agent.

**Docs**
- [oc_gateway_openresponses_http_api](oc_gateway_openresponses_http_api.md) — `/v1/responses` endpoint (planned, this series); relevance: sibling endpoint that defers auth/security/model-contract to this note.
- [oc_gateway_operator_scopes](oc_gateway_operator_scopes.md) — operator scope model (planned, this series); relevance: this endpoint restores the full default operator scope set for shared-secret bearer auth.
- [hermes_api_server_endpoints](../hermes_agent/hermes_api_server_endpoints.md) — sibling tool's HTTP API endpoints; relevance: direct analog of exposing an OpenAI-style HTTP surface from a gateway.
- [hermes_api_server_setup_auth](../hermes_agent/hermes_api_server_setup_auth.md) — API server setup + auth; relevance: parallels enabling the endpoint + bearer/identity auth modes.
- [hermes_open_webui_integration](../hermes_agent/hermes_open_webui_integration.md) — Open WebUI connection guide; relevance: same Open WebUI base-URL/token/model setup OpenClaw documents.
- [hermes_programmatic_integration](../hermes_agent/hermes_programmatic_integration.md) — programmatic gateway integration; relevance: analog to using the endpoint as another operator/client surface.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — OpenAI-compatible LLM-gateway config; relevance: closest sibling-tool doc for routing through an OpenAI-compatible endpoint.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway endpoint config; relevance: endpoint-enable + base-URL patterns analogous to OpenClaw's.
- [cc_sdk_stream_text_and_tool_calls](../claude_code/cc_sdk_stream_text_and_tool_calls.md) — streamed text + tool-call deltas; relevance: backs the streaming tool-call SSE chunk shape.
- [cc_authentication](../claude_code/cc_authentication.md) — auth modes for an agent tool; relevance: parallels token/password/identity-bearing auth selection.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering provider/model targets; relevance: analog for the agent-target `model` and backend-model override.
- [band_rest_api_introduction](../band/band_rest_api_introduction.md) — REST API surface for a coding-agent platform; relevance: another agent-platform HTTP contract paralleling these endpoints.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — HTTP+WS multiplex + agent-run codepath; relevance: serves `/v1/*` and runs them as `openclaw agent`.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent-target routing; relevance: `openclaw/<agentId>` selects the agent target.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM provider backends; relevance: `x-openclaw-model` resolves to a provider/model here.

**Snippets**
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — build the chat-completions request into an agent turn; relevance: core request-translation codepath.
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — SSE streaming of chat completions; relevance: the `data: <json>` / `[DONE]` stream shape.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode resolution helpers; relevance: token/password/trusted-proxy/none selection.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WS listener; relevance: the same-port multiplex serving `/v1/*`.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — auth rate-limit policy install; relevance: `429`/`Retry-After` on auth failures.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize + dispatch; relevance: full-operator-scope restoration for shared-secret bearer.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — chat send handler; relevance: the agent-run codepath the endpoint reuses.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — buffered streaming deltas; relevance: incremental assistant/tool-call delta emission.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — agent dispatch; relevance: routes `model: openclaw/<agentId>` to the right agent.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider backend; relevance: backend resolution for `x-openclaw-model: openai/...`.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model/agent catalog; relevance: `/v1/models` returns OpenClaw agent targets, not raw provider models.

### oc_gateway_openresponses_http_api (8t · 11s · 12d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: exposes the OpenResponses `/v1/responses` endpoint.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — item-based agent-native API; relevance: this endpoint implements the OpenResponses request/event shape.
- [SSE](../../term_dictionary/term_sse.md) — Server-Sent Events; relevance: the `response.*` event sequence streams over `text/event-stream`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — structured tool calls; relevance: client function-tools + `function_call`/`function_call_output` turn loop.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: requests run as a Gateway agent turn backed by an LLM.
- [Prompt Injection](../../term_dictionary/term_prompt_injection.md) — untrusted-content instruction-hijack risk; relevance: decoded file text is wrapped as untrusted external content with boundary markers.
- [Session Data](../../term_dictionary/term_session_data.md) — per-conversation session state; relevance: stateless-per-request by default, `user`/`previous_response_id` derive a stable session.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the same Gateway auth matrix as chat-completions governs this endpoint.

**Docs**
- [oc_gateway_openai_http_api](oc_gateway_openai_http_api.md) — `/v1/chat/completions` (planned, this series); relevance: shares auth/security/agent-target-model contract, deferred from this note.
- [oc_gateway_opentelemetry_signals](oc_gateway_opentelemetry_signals.md) — telemetry catalog (planned, this series); relevance: `usage` normalization feeds the token/cost metrics.
- [pi_custom_streaming_api](../pi/pi_custom_streaming_api.md) — item-based streaming-event API; relevance: closest analog of the OpenResponses incremental event contract.
- [hermes_api_server_endpoints](../hermes_agent/hermes_api_server_endpoints.md) — sibling tool's HTTP API endpoints; relevance: parallels a second item-based HTTP surface on the same server.
- [hermes_context_references](../hermes_agent/hermes_context_references.md) — attaching files/references into context; relevance: analog of `input_file`/`input_image` content injection.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media/file size + MIME handling; relevance: parallels image/file MIME allowlists and size caps.
- [cc_prompt_injection_defenses](../claude_code/cc_prompt_injection_defenses.md) — untrusted-content defenses; relevance: backs the untrusted-external-content wrapping of decoded file bytes.
- [cc_sdk_cost_and_usage_tracking](../claude_code/cc_sdk_cost_and_usage_tracking.md) — usage/token accounting; relevance: the `usage` normalization (`input_tokens`/`prompt_tokens` aliases).
- [cc_sdk_streaming_output](../claude_code/cc_sdk_streaming_output.md) — streaming output events; relevance: analog of the `response.output_text.delta`/`done` event flow.
- [cc_request_and_quality_errors](../claude_code/cc_request_and_quality_errors.md) — request-error taxonomy; relevance: backs the `400`/`401`/`405`/`502` + `invalid_request_error` cases.
- [band_agent_api_context_activity](../band/band_agent_api_context_activity.md) — agent context/activity API; relevance: another item/context-based agent request model.
- [pi_security_model](../pi/pi_security_model.md) — security model for an agent tool; relevance: backs URL-fetch guards (DNS/private-IP/redirect caps) and allowlists.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — responses endpoint + agent run; relevance: serves `/v1/responses` on the multiplex.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent-target routing; relevance: `model: openclaw/<agentId>` selection.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider backends; relevance: `x-openclaw-model` backend override resolution.

**Snippets**
- [snippet_openclaw_gateway_openresponses_session_sse](../../code_snippets/snippet_openclaw_gateway_openresponses_session_sse.md) — responses session + SSE event sequence; relevance: emits the `response.*` event stream.
- [snippet_openclaw_gateway_openresponses_tools_usage](../../code_snippets/snippet_openclaw_gateway_openresponses_tools_usage.md) — responses tools + usage; relevance: client function-tools + usage normalization.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitize/wrap; relevance: untrusted-content wrapping of `input_file`/`input_image`.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content boundary markers; relevance: the `<<<EXTERNAL_UNTRUSTED_CONTENT>>>` wrapping path.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: image MIME validation + size limits + HEIC normalization.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media pipeline; relevance: decoding/extracting file/image parts for the prompt.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — message-build codepath; relevance: shared request-to-agent-turn translation with chat-completions.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: shared auth matrix with chat-completions.
- [snippet_openclaw_sessions_session_key_utils](../../code_snippets/snippet_openclaw_sessions_session_key_utils.md) — session-key derivation; relevance: `user`/`previous_response_id` → stable session key.
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session-id resolution; relevance: stateless-per-request vs reused-session routing.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency/cache status; relevance: the normalized usage counters reported back.

### oc_gateway_openshell (8t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: OpenShell is OpenClaw's managed remote-sandbox backend.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: OpenShell provisions remote sandboxes instead of local Docker.
- [SSH](../../term_dictionary/term_ssh.md) — secure shell transport; relevance: OpenShell uses the core SSH transport + remote filesystem bridge.
- [Docker](../../term_dictionary/term_docker.md) — local container runtime; relevance: OpenShell is the managed alternative to the local Docker backend.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multiple agents on one host; relevance: per-agent sandbox `scope: agent` and per-agent OpenShell config.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session/state; relevance: `scope: session` ties a sandbox to a session lifecycle.
- [OpenShell](../../term_dictionary/term_openshell.md) — OpenClaw's managed sandbox-backend concept; relevance: existing substantive term note for OpenShell — this procedure note LINKS it (do not duplicate the concept).
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — credential/provider attachment; relevance: `providers`/`policy` attach provider creds at sandbox create.

**Docs**
- [oc_gateway_multiple_gateways](oc_gateway_multiple_gateways.md) — multi-instance isolation (planned, this series); relevance: each isolated Gateway scopes its own OpenShell sandboxes.
- [oc_gateway_operator_scopes](oc_gateway_operator_scopes.md) — operator authorization (planned, this series); relevance: exec/tool routing through the sandbox is gated by operator scopes.
- [pi_containerization](../pi/pi_containerization.md) — containerized agent runtimes; relevance: closest analog of a managed container/sandbox backend.
- [cc_sandbox_runtime_and_containers](../claude_code/cc_sandbox_runtime_and_containers.md) — sandbox runtime + containers; relevance: parallels the managed-backend container model.
- [cc_sandbox_filesystem_network_isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — FS/network isolation; relevance: backs the remote-FS-bridge isolation OpenShell relies on.
- [cc_sdk_isolation_technologies](../claude_code/cc_sdk_isolation_technologies.md) — isolation technologies; relevance: conceptual backing for delegating sandbox lifecycle to a remote.
- [cc_sdk_credential_and_filesystem_controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential/FS controls; relevance: parallels workspace-fd pinning + sandbox-identity rechecks.
- [cc_sandbox_limitations_and_troubleshooting](../claude_code/cc_sandbox_limitations_and_troubleshooting.md) — sandbox limitations; relevance: analog of OpenShell's current limitations (no sandbox browser, no docker binds).
- [hermes_terminal_backends](../hermes_agent/hermes_terminal_backends.md) — remote terminal/exec backends; relevance: SSH-based remote command-execution backend analog.
- [hermes_security_isolation_credentials](../hermes_agent/hermes_security_isolation_credentials.md) — isolation + credentials; relevance: parallels the SSH-bridge security hardening.
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — deploying coding agents; relevance: another remote/managed deployment model for agent execution.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — sandbox routing; relevance: routes tool execution through the configured sandbox backend.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent sandbox config; relevance: `agents.defaults.sandbox` + per-agent `list[]` overrides.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension loading; relevance: the `@openclaw/openshell-sandbox` plugin loads as an extension.

**Snippets**
- [snippet_openclaw_security_openshell_backend](../../code_snippets/snippet_openclaw_security_openshell_backend.md) — OpenShell backend; relevance: the managed-sandbox backend implementation.
- [snippet_openclaw_security_openshell_cli](../../code_snippets/snippet_openclaw_security_openshell_cli.md) — `openshell` CLI invocation; relevance: `sandbox create/get/delete`, `ssh-config` lifecycle calls.
- [snippet_openclaw_security_openshell_fs_bridge](../../code_snippets/snippet_openclaw_security_openshell_fs_bridge.md) — remote FS bridge; relevance: read/write/edit/apply_patch through the sandbox bridge.
- [snippet_openclaw_security_openshell_mirror](../../code_snippets/snippet_openclaw_security_openshell_mirror.md) — mirror-mode sync; relevance: pre/post-exec local↔remote sync behavior.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — session FS index read; relevance: file/media reads through the sandbox bridge.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: workspace-root fd pinning + identity recheck hardening.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestration; relevance: routing `exec` through the remote sandbox.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval manager; relevance: approval gating still applies to sandboxed exec.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tool deny; relevance: tool policy applies on the OpenShell backend.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: enabling/disabling the openshell plugin.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback MCP/HTTP bridge; relevance: loopback bridging used by sandbox tool routing.

### oc_gateway_opentelemetry_setup (8t · 10s · 12d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: this note enables OpenClaw's `diagnostics-otel` OTLP export.
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — observability of agentic runtimes; relevance: OTel export makes agent runs/model calls observable.
- [Model Monitoring](../../term_dictionary/term_model_monitoring.md) — monitoring model usage/health; relevance: traces/metrics for model usage and failover.
- [Data Observability](../../term_dictionary/term_data_observability.md) — observability of data flows; relevance: message-flow/queue/session signals across the pipeline.
- [Observer Pattern](../../term_dictionary/term_observer_pattern.md) — event-subscription design; relevance: the plugin subscribes to in-process diagnostic events and exports them.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — secret/content handling; relevance: content-capture is off by default; collector headers/tokens are sensitive.
- [PII](../../term_dictionary/term_pii.md) — personally identifiable info; relevance: privacy controls keep prompt/response text out of spans unless explicitly opted in.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — cached-prompt token reuse; relevance: cache token signals are part of the cost telemetry this enables.

**Docs**
- [oc_gateway_opentelemetry_signals](oc_gateway_opentelemetry_signals.md) — the exported metric/span/event catalog (planned, this series); relevance: this note configures the export of that catalog.
- [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — sibling-tool OTel setup; relevance: closest analog of enabling OTLP export for an agent tool.
- [cc_sdk_observability_opentelemetry](../claude_code/cc_sdk_observability_opentelemetry.md) — SDK OTel observability; relevance: parallels wiring traces/metrics/logs from an agent SDK.
- [cc_otel_configuration_variables](../claude_code/cc_otel_configuration_variables.md) — OTel config/env variables; relevance: analog of `OTEL_EXPORTER_OTLP_*`/`OTEL_SERVICE_NAME` overrides.
- [cc_otel_analysis_and_privacy](../claude_code/cc_otel_analysis_and_privacy.md) — OTel analysis + privacy; relevance: parallels the privacy/content-capture opt-in controls.
- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — telemetry + content/privacy; relevance: analog of withholding raw content unless capture is enabled.
- [cc_environment_variables](../claude_code/cc_environment_variables.md) — env-var configuration; relevance: backs env-override precedence (signal-specific config > env > shared).
- [cloudwatch_otel_overview](../aws_cloudwatch/cloudwatch_otel_overview.md) — OTLP ingestion into a collector backend; relevance: a concrete OTLP backend the export targets.
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway operations/diagnostics; relevance: analog of operating gateway observability.
- [pi_security_model](../pi/pi_security_model.md) — security/privacy model; relevance: backs the content-capture-off-by-default privacy stance.
- [cc_otel_audit_and_siem](../claude_code/cc_otel_audit_and_siem.md) — OTel audit/SIEM export; relevance: parallels exporting logs/spans to a downstream collector.
- [cloudwatch_logs_data_protection](../aws_cloudwatch/cloudwatch_logs_data_protection.md) — log data protection/redaction; relevance: analog of log-body redaction + sanitized attributes.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — diagnostics surface; relevance: emits the in-process diagnostic events the plugin exports.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — content-capture redaction; relevance: bounded/redacted attribute handling for spans.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin loading; relevance: the `diagnostics-otel` plugin loads as an extension.

**Snippets**
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency/cache status; relevance: the model-usage signals OTel exports.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — gateway lifecycle/respawn; relevance: the gateway process that hosts the diagnostics surface.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — content boundary/redaction; relevance: backs content-capture privacy controls.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: `OTEL_*` env overrides + `OPENCLAW_OTEL_PRELOADED`.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — config reload apply; relevance: applying `diagnostics.otel.*` config.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin enable/disable lifecycle; relevance: `plugins enable/disable diagnostics-otel`.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — server config + plugins wiring; relevance: `plugins.allow`/`entries` gating for the exporter.
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — daily usage/cost summary; relevance: the cost counters whose export this enables.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — streamed delta/heartbeat; relevance: time-to-first-byte / streaming signals.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets handling; relevance: collector header tokens treated as secrets.

**Note** (term floor): `term_caching`/`term_pii` substitute for the unresolved `term_usage_tracking` cited at plan
time; `term_distributed_tracing`/`term_observability` do NOT exist in the DB (master decision keeps OpenTelemetry as
OpenClaw/tool vocabulary inside the note, covered by the existing observability terms above).

### oc_gateway_opentelemetry_signals (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: this note is OpenClaw's exact exported-telemetry catalog.
- [Observability for Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — agentic-runtime observability; relevance: the metric/span families cover model/message/queue/session/exec.
- [Model Monitoring](../../term_dictionary/term_model_monitoring.md) — model usage/health monitoring; relevance: model-usage metrics (tokens, cost, duration, TTFB).
- [KV Cache](../../term_dictionary/term_kv_cache.md) — cached key/value reuse; relevance: `cache_read`/`cache_write` token attributes on `openclaw.model.usage`.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — cached-prompt reuse; relevance: cache token counters distinguish cached input from billed total.
- [Model Failover](../../term_dictionary/term_model_failover.md) — provider/model fallback; relevance: the `openclaw.model.failover` counter with to-provider/to-model/reason attrs.
- [Context Window](../../term_dictionary/term_context_window.md) — model context budget; relevance: `openclaw.context.tokens` histogram + `context.assembled` span.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session state; relevance: session-state/liveness metrics + the long_running/stalled/stuck model.
- [Data Governance](../../term_dictionary/term_data_governance.md) — bounded/redacted attribute policy; relevance: spans carry only bounded identifiers + hash-only request ids, never content.

**Docs**
- [oc_gateway_opentelemetry_setup](oc_gateway_opentelemetry_setup.md) — enable/configure the export (planned, this series); relevance: that note enables and scopes the signals catalogued here.
- [cc_otel_metrics_reference](../claude_code/cc_otel_metrics_reference.md) — exported-metrics reference; relevance: closest analog — a named metric/attribute catalog.
- [cc_otel_traces](../claude_code/cc_otel_traces.md) — exported spans/traces; relevance: analog of the exported span set with attributes.
- [cc_otel_events_reference](../claude_code/cc_otel_events_reference.md) — telemetry event reference; relevance: analog of the diagnostic event catalog backing metrics/spans.
- [cc_otel_analysis_and_privacy](../claude_code/cc_otel_analysis_and_privacy.md) — analysis + privacy of telemetry; relevance: bounded/low-cardinality attributes + privacy stance.
- [cc_sdk_cost_and_usage_tracking](../claude_code/cc_sdk_cost_and_usage_tracking.md) — token/cost accounting; relevance: analog of the token/cost metric families.
- [cloudwatch_custom_metrics](../aws_cloudwatch/cloudwatch_custom_metrics.md) — custom metric counters/histograms; relevance: backs the counter-vs-histogram metric typing.
- [cloudwatch_dashboards_overview](../aws_cloudwatch/cloudwatch_dashboards_overview.md) — building dashboards from metrics; relevance: operators use these exact names/attrs to build dashboards.
- [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — server/usage error categories; relevance: backs `errorCategory`/`failureKind` span+metric attributes.
- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — telemetry content/privacy; relevance: analog of bounded-attribute, content-withheld defaults.
- [cloudwatch_metrics_overview](../aws_cloudwatch/cloudwatch_metrics_overview.md) — metrics model overview; relevance: counter/histogram/attribute model parallel.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — emits the diagnostic events; relevance: source of model/message/queue/exec signals.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session-liveness state machine; relevance: backs long_running/stalled/stuck classification + recovery events.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — bounded/hashed attribute redaction; relevance: hash-only request ids + sanitized attributes.

**Snippets**
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — usage/cost summary; relevance: the cost/token counter family.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency/cache status; relevance: run-duration/TTFB/cache-status metrics.
- [snippet_openclaw_gateway_session_utils_subagent_liveness](../../code_snippets/snippet_openclaw_gateway_session_utils_subagent_liveness.md) — subagent liveness; relevance: the session-liveness state model + stuck/stalled detection.
- [snippet_openclaw_gateway_session_utils_model_fallback](../../code_snippets/snippet_openclaw_gateway_session_utils_model_fallback.md) — model fallback; relevance: `openclaw.model.failover` metric source.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error classification; relevance: failover reason/errorCategory attributes.
- [snippet_openclaw_gateway_session_reset_mutation_perform](../../code_snippets/snippet_openclaw_gateway_session_reset_mutation_perform.md) — session recovery mutation; relevance: `session.recovery.requested/completed` events (aborted/released).
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — content redaction; relevance: spans withhold prompt/response/tool content.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — payload size validation; relevance: backs `openclaw.payload.large`/`large_bytes`.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestration; relevance: `openclaw.exec.duration_ms` + exec span attributes.
- [snippet_openclaw_agents_tool_loop_detectors_circuit](../../code_snippets/snippet_openclaw_agents_tool_loop_detectors_circuit.md) — tool-loop circuit detection; relevance: `openclaw.tool.loop.iterations`/`duration_ms`.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method gating / blocked tools; relevance: `openclaw.tool.execution.blocked` (deniedReason).

### oc_gateway_operator_scopes (8t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: scopes are OpenClaw's control-plane authorization vocabulary.
- [Access Control](../../term_dictionary/term_access_control.md) — who-can-do-what enforcement; relevance: the six `operator.*` scope levels define control-plane permissions.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: scopes apply after a client authenticates with a role.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer/device token; relevance: device-token scopes + self-scoped management.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent client transport; relevance: clients connect over WS with `operator` or `node` role.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC method calls; relevance: each Gateway RPC has a least-privilege method scope.
- [Threat Model](../../term_dictionary/term_threat_model.md) — adversary/boundary analysis; relevance: scopes are a single-operator-domain guardrail, NOT hostile multi-tenant isolation.
- [Session Data](../../term_dictionary/term_session_data.md) — per-session state/role; relevance: operator vs node session roles + shared-secret session scope restoration.

**Docs**
- [oc_gateway_pairing](oc_gateway_pairing.md) — node/device pairing (planned, this series); relevance: `node.pair.approve` derives extra approval scopes from the pending command list.
- [oc_gateway_openai_http_api](oc_gateway_openai_http_api.md) — HTTP API endpoints (planned, this series); relevance: shared-secret HTTP surfaces restore the full default operator scope set.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — security architecture; relevance: analog of a layered control-plane authorization model.
- [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — permission rules; relevance: parallels least-privilege method gating + approval-time checks.
- [cc_managed_permission_settings_and_precedence](../claude_code/cc_managed_permission_settings_and_precedence.md) — managed permission precedence; relevance: analog of scope precedence + admin-satisfies-all.
- [cc_sdk_tool_access_control](../claude_code/cc_sdk_tool_access_control.md) — tool access control; relevance: parallels method-scope-as-first-gate then handler checks.
- [cc_mcp_installation_scopes](../claude_code/cc_mcp_installation_scopes.md) — scope tiers for capabilities; relevance: analog of scope-level taxonomy.
- [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure deployment principles; relevance: "use separate processes/users for real trust separation" matches the note's guidance.
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — command approval gating; relevance: analog of approval-time scope derivation for risky commands.
- [pi_security_model](../pi/pi_security_model.md) — security model; relevance: parallels role/scope guardrails for an agent tool.

**Repos**
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — scope enforcement; relevance: implements the scope/approval-time checks.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — per-method least-privilege scope; relevance: maps each RPC to its method scope.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — operator/node session roles; relevance: role assignment + self-scoped device-token sessions.

**Snippets**
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — per-method scope gating; relevance: method scope decides whether a request reaches the handler.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize + dispatch; relevance: scope check then handler approval-time checks.
- [snippet_openclaw_agents_scope](../../code_snippets/snippet_openclaw_agents_scope.md) — agent scope model; relevance: scope vocabulary applied to agent actions.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: shared-secret vs identity-bearing scope handling.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets in calls; relevance: `operator.talk.secrets` reading Talk config with secrets.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval manager; relevance: `operator.approvals` exec/plugin approval APIs.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: command-derived approval scopes for node pairing.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: operator-role control-plane client auth.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client identity/TLS; relevance: identity-bearing modes honoring declared scopes.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send/role policy; relevance: write-scoped vs admin-scoped command-level gating (`/config set`).
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec-runtime audit; relevance: high-risk approvals require `operator.admin`.

### oc_gateway_pairing (10t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted coding-agent gateway; relevance: the Gateway is the source of truth for node pairing.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: pairing establishes node identity and issues an auth token.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — issued/rotated token; relevance: approval mints a fresh token; tokens rotate on re-pair.
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent transport; relevance: nodes request pairing over the Gateway WS endpoint.
- [Access Control](../../term_dictionary/term_access_control.md) — permission enforcement; relevance: node command gating (2026.3.31+) blocks commands until pairing is approved.
- [Threat Model](../../term_dictionary/term_threat_model.md) — trust-boundary analysis; relevance: node-event trust boundaries restrict node-originated runs to a reduced surface.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC methods/events; relevance: the `node.pair.*` methods + `node.pair.requested/resolved` events.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — fronting proxy/forwarded headers; relevance: forwarded-header evidence disqualifies a loopback locality claim.
- [Idempotency](../../term_dictionary/term_idempotency.md) — repeat-safe operations; relevance: `node.pair.request` is idempotent per node (same pending request).
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — OpenClaw DM/device pairing concept; relevance: existing substantive term note for pairing — this Gateway-owned node-pairing procedure LINKS it (do not duplicate the concept).

**Docs**
- [oc_gateway_operator_scopes](oc_gateway_operator_scopes.md) — operator scope model (planned, this series); relevance: pairing approvals derive `operator.pairing`/`write`/`admin` from the command list.
- [oc_gateway_multiple_gateways](oc_gateway_multiple_gateways.md) — multi-instance isolation (planned, this series); relevance: remote-mode pairing happens against the correct Gateway's store.
- [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — command-approval gating; relevance: analog of approval-gated command exposure for remote actors.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — gateway internals; relevance: parallels gateway-owned membership/transport behavior.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — remote auth/approval UI; relevance: analog of approve/reject frontends over a remote gateway.
- [cc_channel_permission_relay](../claude_code/cc_channel_permission_relay.md) — permission relay to a client; relevance: parallels relaying approval decisions to remote nodes.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — security architecture; relevance: trust/identity boundary framing for paired vs unpaired actors.
- [cc_authentication](../claude_code/cc_authentication.md) — token/identity auth; relevance: analog of issued-token + rotation-on-re-pair.
- [band_websocket_overview](../band/band_websocket_overview.md) — WS channels for agents; relevance: another WS pairing/connect-and-trust model.
- [band_contacts_and_discovery](../band/band_contacts_and_discovery.md) — contact/peer discovery + approval; relevance: analog of pending-vs-paired membership management.
- [pi_security_model](../pi/pi_security_model.md) — security model; relevance: trust-boundary backing for node-event hardening.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — pairing store + protocol; relevance: stores pending/paired nodes and serves `node.pair.*`.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — trust boundaries; relevance: node-command gating + node-event trust-boundary hardening.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — device/node session lifecycle; relevance: invalidating node-role sessions on remove.

**Snippets**
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — gateway node-pairing store/methods; relevance: the pending/paired lifecycle + token issuance.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS gateway pairing; relevance: a concrete remote-node pairing client flow.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing allowlist; relevance: trusted-CIDR/allowlist-style auto-approval parallel.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — connect over proxy; relevance: forwarded-header locality disqualification logic.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: `gateway.nodes.allowCommands`/`denyCommands` after pairing.
- [snippet_openclaw_gateway_node_events_presence_apns](../../code_snippets/snippet_openclaw_gateway_node_events_presence_apns.md) — node presence events; relevance: `node.presence.alive` accepted only from paired node sessions.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: declared commands become available after pairing approval.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session (kit); relevance: WS node-role session establishment + token use.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning (kit); relevance: secure transport for remote-node pairing.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — Android WS session; relevance: another remote-node pairing/connect client.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method gating; relevance: `node.pair.*` method-scope reachability.

**Analysis (additional)**

## Undigested Terms Plan

| Term | Disposition |
|------|-------------|
| operator scope / `operator.read`/`write`/`admin`/`pairing`/`approvals`/`talk.secrets` | OpenClaw control-plane vocabulary → documented IN `oc_gateway_operator_scopes` (note 7); not a `term_dictionary` capture. Link `term_access_control`, `term_authentication`. |
| OpenAI-compatible HTTP endpoint / `/v1/chat/completions` / `/v1/responses` / `/v1/models` / `/v1/embeddings` | OpenClaw endpoint surfaces → documented IN notes 2/3; link `term_openai_responses_api`, `term_llm`, `term_embedding`. |
| agent-first model contract / `openclaw/<agentId>` / `x-openclaw-model` | OpenClaw routing vocabulary → documented IN note 2; link `term_llm`, `term_model_router`. |
| OpenShell / mirror vs remote workspace mode / managed sandbox backend | OpenClaw product vocabulary → documented IN note 4; link `term_sandbox`, `term_ssh`, `term_docker`. |
| diagnostics-otel / OTLP/HTTP / signals (metrics/traces/logs) / content capture | OpenClaw + OTel vocabulary → documented IN notes 5/6; link existing `term_observability_agent_systems`, `term_model_monitoring`, `term_data_observability`. **No new `term_opentelemetry`/`term_observability`/`term_distributed_tracing` capture** — existing observability terms cover it (master decision: OpenClaw/tool vocab → oc_ doc notes, not term_dictionary). |
| Gateway-owned node pairing / `node.pair.*` / pending vs paired / token rotation | OpenClaw vocabulary → documented IN note 8; link `term_oauth_token`, `term_authentication`, `term_json_rpc`. |
| multiple gateways / profiles / derived ports / isolation | OpenClaw operational vocabulary → documented IN note 1; link `term_openclaw`, `term_secrets_manager`. |

**Expected new `term_dictionary` captures: 0.** All vocabulary is either OpenClaw product/endpoint terminology
(home = the `oc_*` doc note) or covered by an existing substantive term note (linked, not duplicated). Augment
Step 2d re-runs the new-term scan; the only borderline cross-cutting candidate, generic "OpenTelemetry", is
intentionally NOT promoted because `term_observability_agent_systems` + `term_model_monitoring` +
`term_data_observability` already cover the reusable concept (and `cc_monitoring_opentelemetry_setup` is the
existing OTel doc anchor). If augment finds a genuinely reusable, non-OpenClaw-specific term with no existing
note, it would be captured via `/tessellum-capture-term-note` and added to `acronym_glossary_a_g.md` (for OTLP) —
but none is expected.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; it only LINKS existing terms.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|------|-------|---------------|
| G1 | Format: YAML field order + forbidden fields; H1/`## Overview`/`## Related Notes`/`## References`/footer; itemized keywords/topics; quoted years | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim traces to `inbox/openclaw_docs/gateway/<page>.md` (no hallucinated config keys/metric names/scope names); config/metric snippets verbatim | diff vs mirror source |
| G3 | Density + Coverage: ≤400 lines, ≤2,500 words, ≤6 code blocks, one building_block per note; every mapped H2/H3 covered | `wc` + section-coverage-map audit |
| G4 | Cross-Reference: ≥6 relevance-selected term links + repo/sibling/other-vault links per note, each with a relevance statement; indexed `[text](path.md)` link format | manual + `note_links` query |
| G5 | Ghost-reference: every cited note_id resolves in DB; ghost targets redirected/dropped | `sqlite3` existence sweep |
| G6 | Broken-link fix: 0 broken relative paths after reindex | `/tessellum-fix-broken-links` |
| G7 | Discoverability: every new note links out to ≥1 existing note (out-degree ≥1) | `note_links` query |
| G8 | In-degree ≥1: every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (anti-island), satisfied via `entry_openclaw_docs.md` + repo/term inlinks | `note_links` query + `in_degree` |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
cd /path/to/vault
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_gateway_multiple_gateways oc_gateway_openai_http_api oc_gateway_openresponses_http_api oc_gateway_openshell oc_gateway_opentelemetry_setup oc_gateway_opentelemetry_signals oc_gateway_operator_scopes oc_gateway_pairing"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density (body words, fences/2)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (words=$words code=$cb lines=$lines)"
  # G4 sibling-prefix cross-ref presence (≥1 oc_ sibling link)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "$n NO SIBLING ($SIBLING_PREFIX) LINK"
done

# YAML frontmatter sweep over the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference sweep: every linked note_id must resolve in DB
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
# (executed by /tessellum-fix-ghost-references; manual spot-check example:)
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code (≤6) | Within caps? |
|---|---|---|---:|---|---|
| 1 | oc_gateway_multiple_gateways | procedure | 600 | 4 (rescue quickstart, general setup, env example, quick checks) | ✅ |
| 2 | oc_gateway_openai_http_api | procedure | 750 | 5 (enable, smoke curl, stable-session, streaming, list-models — drop 4 of 9 source fences) | ✅ |
| 3 | oc_gateway_openresponses_http_api | procedure | 700 | 5 (function_call_output, input_image, limits config, streaming example) | ✅ |
| 4 | oc_gateway_openshell | procedure | 650 | 5 (quick-start config, minimal remote, mirror+GPU or per-agent, lifecycle) | ✅ |
| 5 | oc_gateway_opentelemetry_setup | procedure | 650 | 5 (install, quick-start config, full config-reference, without-exporter, disable) | ✅ |
| 6 | oc_gateway_opentelemetry_signals | model | 700 | 1–2 (metric/span lists reproduced as prose tables, not fences) | ✅ |
| 7 | oc_gateway_operator_scopes | concept | 550 | 0 (scope tables as markdown tables) | ✅ |
| 8 | oc_gateway_pairing | procedure | 700 | 3 (CLI workflow, autoApproveCidrs config, storage paths) | ✅ |

No note approaches the 2,500-word / 400-line caps. The two code-heavy source pages (openai-http-api 9 fences,
opentelemetry 8 fences) are kept ≤6 by selective verbatim reproduction; the metric/span catalog (note 6) is
rendered as markdown tables rather than code fences. opentelemetry.md split (2,570w → notes 5+6) keeps each half
comfortably under cap.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `0_entry_points/entry_openclaw_docs.md` (created as the master W1 pre-step;
`building_block: navigation`) under the **Gateway** section, sub-plan **gw04** cluster. Each new note receives its
entry-point back-link at finalization (this is the primary G8 inbound-link source). No new entry point is created
`repo_openclaw`) is a master-level concern, not repeated per sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links to satisfy G7/G8 (DB-verify + add at execution):

- `entry_openclaw_docs.md` → all 8 notes (primary anti-island source; created as master pre-step).
- `repo_openclaw_gateway` → notes 1, 2, 3, 5, 6, 7, 8 (gateway HTTP/OTel/pairing/scope surfaces).
- `repo_openclaw_security` → notes 7, 8, 5 (scopes, pairing trust boundaries, content-capture redaction).
- `repo_openclaw_sessions` → notes 6, 7, 8 (session-liveness telemetry, operator/node session roles, pairing lifecycle).
- `repo_openclaw_agents` → notes 2, 3, 4 (agent-target routing, per-agent sandbox).
- `repo_openclaw_extensions` / `repo_openclaw_extensions_llm_providers` → notes 4, 5 (openshell + diagnostics-otel plugins), note 2 (`x-openclaw-model` backend override).
- `term_openclaw` → notes 1, 7 (gateway product + authorization model); `term_sandbox` → note 4; `term_oauth_token` → notes 7, 8; `term_observability_agent_systems` → notes 5, 6; `term_openai_responses_api` → notes 2, 3.

## Pacing Rules (inherited from master)

Single phase, 8 notes — within the ≤7-ideal / fan-out cap envelope (≤30 agents/run). Re-read each source page
before authoring; reproduce config/metric snippets verbatim; one building_block per note. `git pull --rebase
--autostash` first; commit + push the phase as one indivisible cycle; no Claude co-author trailer. Reindex
incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref mapping LOCKED at raised floors; see Augmentation Report) |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21** — 9/9 checkpoints PASS (see Review Sign-Off) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope.** xref-augment pass: re-read all 7 source pages under `inbox/openclaw_docs/gateway/` (measured word
counts confirm the plan's Source table exactly — multiple-gateways 866, openai-http-api 2,188,
openresponses-http-api 1,489, openshell 1,242, opentelemetry 2,570, operator-scopes 734, pairing 1,288). Replaced
the plan-stage `## Candidate Cross-References` with a LOCKED `## Per-Note Related Notes Mapping` meeting the raised
floors **≥8 terms · ≥10 snippets · ≥10 docs per note** (PLUS 3 `repo_openclaw*` each + sibling `oc_*`).

**What was locked (per-note counts — terms / snippets / docs / repos; all floors met):**

| Note | BB | Terms | Snippets | Docs (existing / planned) | Repos | Floors |
|---|---|---:|---:|---|---:|---|
| oc_gateway_multiple_gateways | procedure | 8 | 11 | 11 (8 / 3) | 3 | PASS |
| oc_gateway_openai_http_api | procedure | 9 | 11 | 12 (10 / 2) | 3 | PASS |
| oc_gateway_openresponses_http_api | procedure | 8 | 11 | 12 (10 / 2) | 3 | PASS |
| oc_gateway_openshell | procedure | 8 | 11 | 11 (9 / 2) | 3 | PASS |
| oc_gateway_opentelemetry_setup | procedure | 8 | 10 | 12 (11 / 1) | 3 | PASS |
| oc_gateway_opentelemetry_signals | model | 9 | 11 | 11 (10 / 1) | 3 | PASS |
| oc_gateway_operator_scopes | concept | 8 | 11 | 10 (8 / 2) | 3 | PASS |
| oc_gateway_pairing | procedure | 10 | 11 | 11 (9 / 2) | 3 | PASS |

**DB-verification.** Every cited EXISTING note_id was confirmed present in the unified DB
snippet corpus, 253 notes). The doc neighbors draw on the existing `claude_code/cc_*` (incl. the dedicated
`cc_otel_*` cluster), `hermes_agent/hermes_*` (gateway/API/security analogs), `pi/pi_*`, `band/band_*`, and
`aws_cloudwatch/cloudwatch_*` (OTLP/metrics/dashboards) corpora.

- `term_embeddings` → does not exist → use `term_embedding` (verified). Both HTTP-API notes link via `term_llm` +
  endpoint vocabulary; `term_embedding` is available if needed at execution.
- `term_gpu` → does not exist → dropped; OpenShell GPU is documented IN note 4 (vocab) and linked via `term_sandbox`.
- `term_session` → does not exist → use `term_session_persistence` / `term_session_data` (both verified).
- `term_usage_tracking` → does not exist → substituted with `term_caching` (cache token signals) + `term_pii`
  (content-capture privacy) on note 5; cost signals on note 6 link `term_kv_cache` / `term_prompt_caching`.
- `cc_sandbox`-class → resolved to concrete verified docs `cc_sandbox_runtime_and_containers`,
  `cc_sandbox_filesystem_network_isolation`, `cc_sandbox_limitations_and_troubleshooting`,
  `cc_sdk_credential_and_filesystem_controls`.

**CP8f collision audit (generalized to ALL planned notes — term AND doc).** None of the 8 planned `oc_*` slugs
collide with any existing note (all `NONE`). The audit surfaced two EXISTING substantive **concept** term notes
adjacent to two planned **procedure** doc notes: `term_openshell.md` (active, ~9.8 KB, `building_block: concept`)
and `term_dm_pairing.md` (active, ~6.7 KB, `building_block: concept`). These are NOT duplicates (different BB — the
planned notes are operational how-tos, not concept definitions), so per the CP8f "link, don't duplicate" rule they
were **added as LINKS**: `term_openshell` → note 4, `term_dm_pairing` → note 8 (each marked "do not duplicate the
concept"). No planned doc note duplicates an existing term note's concept.

**New-term candidates (Step 2d re-scan): NONE.** Expected new `term_dictionary` captures remain **0**. All
vocabulary is either OpenClaw product/endpoint terminology (home = the owning `oc_*` doc note) or already covered by
an existing substantive term note (linked, not duplicated). The re-read surfaced no genuinely cross-cutting,
vault-reusable term lacking both a doc-page home and an existing note. The lone borderline candidate — generic
"OpenTelemetry" / "distributed tracing" — is intentionally NOT promoted: `term_observability_agent_systems` +
`term_model_monitoring` + `term_data_observability` + `term_observer_pattern` already cover the reusable concept,
and `cc_monitoring_opentelemetry_setup` / `cc_otel_*` are the existing doc anchors (master decision: OpenClaw/tool
vocab → `oc_` doc notes, not `term_dictionary`). Best-fit glossary if ever promoted: `acronym_glossary_a_g.md`
(for OTLP) — not expected.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step ≥8 terms + floors | **PASS** | LOCKED Per-Note mapping: every note ≥8 terms (8–10), ≥10 snippets (10–11), ≥10 docs (10–12); each link carries a one-line what-it-is + a relevance statement (`- [Name](path.md) — …; relevance: …`). Raised-floor standard stated in the section header. |
| CP2 | 9-GATE present per batch (G1-G6 + G8) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with all 8 gates incl. G5-Ghost + G6-Broken + G7/G8 discoverability; single execution phase. |
| CP3 | Entry point inherited (`entry_openclaw_docs` planned at W1) | **PASS** | `## Entry Point Decision (inherited from master)`: contributes 8 rows to `0_entry_points/entry_openclaw_docs.md` (master W1 pre-step, `building_block: navigation`); not yet created (confirmed absent in DB) — correctly inherited, not re-derived per sub-plan. >30-note master ⇒ CREATE required; matches threshold. |
| CP4 | Size | **PASS** | 8 planned notes ≤ 30; single phase within fan-out cap (≤30 agents/run). |
| CP5 | Format derived (not invented) | **PASS** | Format inherited verbatim from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` corpora (same source type); body `# … → ## Overview → mirrored H2/H3 → ## Related Notes → ## References → footer`; forbidden-field list present; matches existing target-dir convention. |
| CP6 | Density / borderline splits | **PASS** | `## Density Re-Assessment` table: all 8 notes 550–750w, ≤6 code blocks; opentelemetry.md (2,570w, mixed BB) correctly split into setup (procedure) + signals (model); no borderline note unaddressed. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-read all 7 pages via the `inbox/openclaw_docs/gateway/` mirror; `wc -w` matches the plan's Source table exactly (866 / 2,188 / 1,489 / 1,242 / 2,570 / 734 / 1,288). |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | `## Undigested Terms Plan` present (all rows have a disposition — documented-in-`oc_`-note or link-existing); `## Term-Note Authoring Requirements` present as "N/A (0 new terms)" with master multi-source mandate inherited (applies only if a new term is later proposed). Expected new captures: 0. |
| CP8f | Slug specificity / collision audit | **PASS** | CP8f run for ALL planned notes (not only term slugs) across term_dictionary AND documentation/: 0 slug collisions for the 8 `oc_*` slugs; 2 adjacent substantive term concepts (`term_openshell`, `term_dm_pairing`) caught and added as LINKS (different BB, not duplicates). No too-general slug; OpenTelemetry NOT over-promoted. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound link (`entry_openclaw_docs` → all 8; plus `repo_openclaw_*` + `term_*` + FZ-15 analysis inlinks); G8-Discoverability is in the phase gate table as a gated execution step. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.**
</content>
</invoke>
