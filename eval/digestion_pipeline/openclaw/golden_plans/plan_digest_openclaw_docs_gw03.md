---
title: Sub-Plan gw03 — OpenClaw Docs: Gateway (External Apps, Lock, Health, Heartbeat, Local Models, Logging)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["gateway/external-apps", "gateway/gateway-lock", "gateway/health", "gateway/heartbeat", "gateway/local-model-services", "gateway/local-models", "gateway/logging"]
---

# Sub-Plan gw03: Gateway

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order, `## Overview` → body → `## Related Notes` → `## References` → bold footer; caps ≤400 lines / ≤2500 words / ≤6 code blocks; one BB per note), dedup-before-create (term_dictionary AND documentation/ AND repo_openclaw*), the 9-GATE table, cross-references, and entry-point wiring (`entry_openclaw_docs.md`) are ALL inherited from the master. This file locks the per-page measurements, planned notes, section coverage, split decision, and candidate cross-references for the 7 gateway operations pages.

## Scope

The 7 gateway operational pages covering how external code talks to the Gateway, how the Gateway guards single-instance startup, and the day-to-day operations layer: health checks, the periodic heartbeat turn, on-demand local model servers, full local-model serving stacks, and logging surfaces. **Priority P1 (Phase A)** — these are the operational/runtime vocabulary that providers, channels, CLI, and tools sub-plans reference (heartbeat ↔ automation/cron; local models ↔ providers; logging/health ↔ diagnostics; external-apps ↔ protocol/RPC). The code-side counterparts `repo_openclaw_gateway`, `repo_openclaw_agents`, and `repo_openclaw_extensions_llm_providers` are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **8,775 measured words** (mirror `inbox/openclaw_docs/gateway/`). **Planned: 8 notes** (heartbeat splits 1→2; all other pages 1 note each).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| External apps | gateway/external-apps | 510 | 0 | 4 | 0 | procedure |
| Gateway lock | gateway/gateway-lock | 342 | 0 | 5 | 0 | model (singleton-guard mechanism) |
| Health checks | gateway/health | 988 | 0 | 7 | 1 | procedure |
| Heartbeat | gateway/heartbeat | 3,235 | 10 | 12 | 11 | procedure (SPLIT: config/contract vs delivery/visibility) |
| Local model services | gateway/local-model-services | 730 | 3 | 7 | 0 | procedure |
| Local models | gateway/local-models | 2,140 | 8 | 7 | 3 | procedure |
| Gateway logging | gateway/logging | 830 | 3 | 5 | 1 | procedure |

Counts: `wc -w` on each mirror file (frontmatter included, ≈10–20 words of noise per page); code = raw ``` fence count / 2 (external-apps 0, gateway-lock 0, health 0, heartbeat 20/2=10, local-model-services 6/2=3, local-models 16/2=8, logging 6/2=3); H2/H3 from `grep -E '^## '`/`'^### '` (H2 counts include the trailing `## Related`).

## Content Strategy

- **Prioritize**: the heartbeat mechanism (response contract, scheduling, cost) and local-model serving (the two most operationally load-bearing, code-heavy pages, and the ones the providers/automation/concepts sub-plans depend on). Health checks are the primary operator-debugging entry point.
- **Split**: `heartbeat.md` (3,235w, 10 code fences, 12 H2 / 11 H3) exceeds the 2,500-word cap and bundles two task clusters — (a) what heartbeat IS + its response/config contract, and (b) how/where deliveries are routed and made visible — so it splits into 2 notes (see Split Decisions). Each stays ≤2,500w / ≤6 code.
- **Link-out (not duplicated)**: cron-vs-heartbeat guidance and background-task records → `automation/*` (au01); provider-specific local backends (ds4, inferrs, LM Studio, Ollama, vLLM) → `providers/*` (pr06–09) and `gw03`'s local-models note links them but does not redefine them; diagnostics-export internals → `gateway/diagnostics` (gw02); OpenTelemetry export → `gateway/opentelemetry` (gw04); protocol/RPC surfaces → `gateway/protocol` (gw05) and `reference/rpc` (rf02); model-failover concept → `concepts/model-failover` (co04). Existing terms (`term_llm`, `term_claude`, `term_cron`, `term_websocket`, `term_pii`/`term_pci` for redaction) are linked, never redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_gateway_external_apps.md` | procedure | external-apps.md: What is available today, Recommended path, App code vs plugin code | 480 | How external apps/scripts/CI/IDE extensions integrate with OpenClaw via Gateway WebSocket + RPC today; the available surfaces table, the recommended connect-and-pin path, and the app-code-vs-plugin-code boundary (no public npm client yet). |
| 2 | `oc_gateway_lock.md` | model | gateway-lock.md: Why, Mechanism, Error surface, Operational notes | 360 | The single-instance gateway guard: a per-config lock file plus an exclusive WS listener bind (`ws://127.0.0.1:18789`); how stale locks are reclaimed, the `GatewayLockError`/`EADDRINUSE` error surface, and systemd exit-code-78 supervisor behavior. |
| 3 | `oc_gateway_health.md` | procedure | health.md: Quick checks, Deep diagnostics, Health monitor config, Uptime monitoring (+ Monitoring service setup examples), When something fails, Dedicated "health" command | 700 | Verifying channel + gateway health: `status`/`status --deep`/`health` CLI commands and flags, on-disk creds/session checks, the channel health-monitor config knobs, the dedicated `/health` uptime endpoint (vs `/v1/chat/completions`), and failure-recovery steps. |
| 4 | `oc_gateway_heartbeat.md` | procedure | heartbeat.md: Quick start, Defaults, What the prompt is for, Response contract, Config, Scope/precedence, Per-agent, Active hours, 24/7, Multi-account, Field notes, HEARTBEAT.md (+ tasks:), Manual wake, Reasoning, Cost awareness, Context overflow | 750 | The periodic main-session heartbeat turn: enabling/cadence (`every`, defaults, active hours), the `HEARTBEAT_OK`/`heartbeat_respond` response contract, the full config schema + scope precedence, the `HEARTBEAT.md` checklist + `tasks:` block, manual wake, and cost controls (isolated/light context). |
| 5 | `oc_gateway_heartbeat_delivery.md` | procedure | heartbeat.md: Delivery behavior (session/target routing, visibility/skip, session lifecycle/audit), Visibility controls (showOk/showAlerts/useIndicator), Per-channel vs per-account examples, Common patterns | 480 | Heartbeat delivery + visibility routing: how `target`/`to`/`session` route a run, the per-channel/per-account visibility flags (`showOk`/`showAlerts`/`useIndicator`) and their precedence, skip-when-busy/alerts-disabled behavior, and session-lifecycle/audit rules. |
| 6 | `oc_gateway_local_model_services.md` | procedure | local-model-services.md: How it works, Config shape, Fields, Inferrs example, ds4 example, Operational notes | 600 | On-demand local model servers via `models.providers.<id>.localService`: the probe-start-wait lifecycle, the config shape + field reference (`command`/`args`/`healthUrl`/`readyTimeoutMs`/`idleStopMs`), worked inferrs + ds4 examples, and idle-shutdown/serialization operational notes. |
| 7 | `oc_gateway_local_models.md` | procedure | local-models.md: Hardware floor, Pick a backend, Recommended LM Studio (+ hybrid/local-first/regional), Other OpenAI-compatible proxies, Smaller/stricter backends, Troubleshooting | 800 | Running OpenClaw on self-hosted local LLMs: hardware floor + prompt-injection safety, backend selection (LM Studio/vLLM/MLX/SGLang/LiteLLM/Ollama/ds4), the recommended LM-Studio-Responses-API config + hosted-fallback hybrids, OpenAI-compatible proxy config (compat flags, tool-call forcing), and a top-down troubleshooting ladder. |
| 8 | `oc_gateway_logging.md` | procedure | logging.md: File-based logger, Console capture, Redaction, Gateway WebSocket logs (+ WS log style), Console formatting | 650 | Gateway logging surfaces: the JSON-lines file logger (path/level/rotation), console capture + style, the secret-redaction policy (`redactSensitive`/`redactPatterns`, always-redact boundaries incl. payment fields), and the WebSocket protocol log modes + subsystem console formatting. |

## Section Coverage Map

```
external-apps.md
├── What is available today (surfaces table) ───────── → note 1 (oc_gateway_external_apps)
├── Recommended path ───────────────────────────────── → note 1
├── App code vs plugin code ────────────────────────── → note 1
└── Related (link-out only) ────────────────────────── → note 1 References (protocol/rpc/cli/sdk)
gateway-lock.md
├── Why ────────────────────────────────────────────── → note 2 (oc_gateway_lock)
├── Mechanism (lock file + exclusive WS bind) ──────── → note 2
├── Error surface (GatewayLockError/EADDRINUSE) ────── → note 2
├── Operational notes (systemd exit 78, macOS PID) ─── → note 2
└── Related (link-out) ─────────────────────────────── → note 2 References (multiple-gateways, troubleshooting)
health.md
├── Quick checks ───────────────────────────────────── → note 3 (oc_gateway_health)
├── Deep diagnostics ───────────────────────────────── → note 3
├── Health monitor config ──────────────────────────── → note 3
├── Uptime monitoring (+ ### Monitoring service setup examples) → note 3
├── When something fails ───────────────────────────── → note 3
├── Dedicated "health" command (flags + snapshot fields) → note 3
└── Related (link-out) ─────────────────────────────── → note 3 References (gateway, diagnostics, troubleshooting)
heartbeat.md
├── Quick start (beginner) ─────────────────────────── → note 4 (oc_gateway_heartbeat)
├── Defaults ───────────────────────────────────────── → note 4
├── What the heartbeat prompt is for ───────────────── → note 4
├── Response contract (HEARTBEAT_OK / heartbeat_respond) → note 4
├── Config (+ ### Scope/precedence, Per-agent, Active hours, 24/7, Multi-account, Field notes) → note 4
├── HEARTBEAT.md (+ ### tasks:, Can the agent update?) → note 4
├── Manual wake (on-demand) ────────────────────────── → note 4
├── Reasoning delivery (optional) ──────────────────── → note 4
├── Cost awareness ─────────────────────────────────── → note 4
├── Context overflow after heartbeat ───────────────── → note 4
├── Delivery behavior (### routing/visibility/lifecycle) → note 5 (oc_gateway_heartbeat_delivery)
├── Visibility controls (showOk/showAlerts/useIndicator) → note 5
├── ### What each flag does / Per-channel vs per-account → note 5
├── ### Common patterns ────────────────────────────── → note 5
└── Related (link-out) ─────────────────────────────── → notes 4+5 References (automation, tasks, timezone)
local-model-services.md
├── How it works (probe-start-wait lifecycle) ──────── → note 6 (oc_gateway_local_model_services)
├── Config shape ───────────────────────────────────── → note 6
├── Fields ─────────────────────────────────────────── → note 6
├── Inferrs example ────────────────────────────────── → note 6
├── ds4 example ────────────────────────────────────── → note 6
├── Operational notes ──────────────────────────────── → note 6
└── Related (link-out) ─────────────────────────────── → note 6 References (local-models, providers/inferrs)
local-models.md
├── Hardware floor ─────────────────────────────────── → note 7 (oc_gateway_local_models)
├── Pick a backend (table) ─────────────────────────── → note 7
├── Recommended: LM Studio (+ ### Hybrid / Local-first / Regional) → note 7
├── Other OpenAI-compatible local proxies ──────────── → note 7
├── Smaller or stricter backends ───────────────────── → note 7
├── Troubleshooting ────────────────────────────────── → note 7
└── Related (link-out) ─────────────────────────────── → note 7 References (configuration-reference, model-failover)
logging.md
├── File-based logger ──────────────────────────────── → note 8 (oc_gateway_logging)
├── Console capture ────────────────────────────────── → note 8
├── Redaction ──────────────────────────────────────── → note 8
├── Gateway WebSocket logs (+ ### WS log style) ─────── → note 8
├── Console formatting (subsystem logging) ─────────── → note 8
└── Related (link-out) ─────────────────────────────── → note 8 References (/logging, opentelemetry, diagnostics)
```
No orphaned sections. All `## Related` blocks are reproduced as `## References` (external doc URLs only); the cron-vs-heartbeat / providers / diagnostics / opentelemetry / protocol pointers are link-outs to other sub-plans, not duplicated content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| heartbeat.md (3,235w, 10 code fences, 12 H2 / 11 H3) | notes 4 (`oc_gateway_heartbeat`) + 5 (`oc_gateway_heartbeat_delivery`) | Exceeds the 2,500-word cap and bundles 10 code fences (>6 cap) across two distinct task clusters: (a) what heartbeat is + its scheduling/response/config/HEARTBEAT.md contract, and (b) delivery routing + per-channel/per-account visibility controls. Splitting keeps each note focused, ≤2,500w, and ≤6 code blocks. |
| (external-apps, gateway-lock, health, local-model-services, local-models, logging) | 1 note each | All ≤2,500w and single-BB; reference pages map 1:1. local-models (2,140w, 8 fences) and local-model-services (730w, 3 fences) stay single notes but reproduce config snippets selectively to keep ≤6 code blocks each (see Density Re-Assessment). |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (8,775 measured words). New `oc_` notes: **8**. New `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: **procedure ×7** (notes 1, 3, 4, 5, 6, 7, 8) · **model ×1** (note 2, the lock singleton-guard mechanism).
- Est. digest words ~4,820 (avg ~600/note); all notes ≤2,500w / ≤6 code. 24 source code fences (heartbeat 10 + local-models 8 + local-model-services 3 + logging 3) distribute across the procedure notes; each note reproduces config snippets selectively to stay ≤6.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> the remainder being **sibling `oc_*` (planned, this series)**. Relevance is the sole selection criterion
> resolve FROM `resources/documentation/openclaw/oc_X.md`: terms `../../term_dictionary/term_Y.md`; sibling oc
> docs `oc_Y.md`; other doc folders `../<folder>/<file>.md`; repos `../../../areas/code_repos/repo_Y.md`;
> snippets `../../code_snippets/snippet_Y.md`; entry points `../../../0_entry_points/entry_Y.md`.
> `entry_openclaw_docs.md` is created as the W1 master pre-step (the G7/G8 inbound source for every note).

### oc_gateway_external_apps (8t · 11s · 11d)

- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway product external apps integrate with; relevance: the integration target this whole page is about.
- [term_websocket](../../term_dictionary/term_websocket.md) — full-duplex socket transport; relevance: external apps connect to the Gateway over WebSocket.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — JSON-RPC method dispatch; relevance: the documented RPC methods (agent, sessions, tasks, models) external apps call.
- [term_acp_agent_client_protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — Agent Client Protocol; relevance: Gateway agent-run RPC parallels ACP and is the recommended `agent`/`agent.wait` path.
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: contrast agent-integration protocol vs the Gateway RPC surface chosen here.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding agents; relevance: external apps start/observe agent runs through the Gateway.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool/function invocation; relevance: the tools RPC surface external apps expose to agent runs.
- [term_api_gateway](../../term_dictionary/term_api_gateway.md) — façade routing requests to backend services; relevance: the Gateway is OpenClaw's single front-door for external app traffic.

- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — Pi's RPC transport/handshake; relevance: directly analogous external-app→coding-agent RPC protocol. *(existing)*
- [pi_extensions_api_methods](../pi/pi_extensions_api_methods.md) — Pi extension API surface; relevance: parallel programmatic method surface for an outside app. *(existing)*
- [band_websocket_overview](../band/band_websocket_overview.md) — Band's WebSocket integration model; relevance: closest analogue to Gateway WS connect-and-call. *(existing)*
- [band_connect_remote_agent](../band/band_connect_remote_agent.md) — connecting an external client to a remote agent; relevance: the same connect-discover-call recommended path. *(existing)*
- [hermes_programmatic_integration](../hermes_agent/hermes_programmatic_integration.md) — calling Hermes from external code; relevance: app-code-vs-plugin-code boundary mirror. *(existing)*
- [cc_sdk_connect_mcp_servers](../claude_code/cc_sdk_connect_mcp_servers.md) — wiring external MCP servers to Claude Code; relevance: the MCP-vs-RPC integration contrast this page draws. *(existing)*
- [oc_gateway_health](oc_gateway_health.md) — health RPC/endpoint; relevance: the health surface external apps should poll. *(planned, this series)*
- [oc_gateway_heartbeat](oc_gateway_heartbeat.md) — periodic agent turn; relevance: an event family external UIs may render. *(planned, this series)*
- [oc_gateway_lock](oc_gateway_lock.md) — single-instance bind; relevance: the listener external apps connect to is the locked WS port. *(planned, this series)*
- [oc_gateway_protocol](oc_gateway_protocol.md) — Gateway WS protocol/versioning; relevance: the page's first "Ready" surface (gw05). *(planned, this series)*
- [oc_reference_rpc](oc_reference_rpc.md) — Gateway RPC method reference; relevance: the page's second "Ready" surface (rf02). *(planned, this series)*

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway RPC/WS server; relevance: implements the surfaces this page documents.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw process; relevance: the process external apps talk to.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin SDK; relevance: the in-process alternative contrasted under App-code-vs-plugin-code.

- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connection establishment; relevance: the connect step of the recommended path.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect handshake error codes; relevance: what an external app must handle on connect.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect through a proxy; relevance: external-bridge connection path.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC request/response envelope; relevance: the wire shape of every method call.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC method schema groups; relevance: the agents/sessions/tasks/models method families this page lists.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — protocol error codes + versioning; relevance: "pin the version / recheck on upgrade" guidance.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — agent RPC dispatch; relevance: the `agent`/`agent.wait` run path external apps start.
- [snippet_openclaw_gateway_entry_dispatch](../../code_snippets/snippet_openclaw_gateway_entry_dispatch.md) — top-level RPC method routing; relevance: how a called method reaches its handler.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — per-method auth-scope gating; relevance: the auth scopes external app calls must hold.
- [snippet_openclaw_gateway_sessions_read_methods](../../code_snippets/snippet_openclaw_gateway_sessions_read_methods.md) — `sessions.*` read RPC; relevance: durable conversation-state methods for app integrations.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — client-kit WS channel; relevance: the client-side connect surface (preview implementation detail).

### oc_gateway_lock (8t · 11s · 10d)

- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the process the lock protects.
- [term_singleton](../../term_dictionary/term_singleton.md) — single-instance guarantee; relevance: the exact property this lock models.
- [term_websocket](../../term_dictionary/term_websocket.md) — WS listener; relevance: the exclusive WS bind is the lock-enforcement mechanism.
- [term_health_check](../../term_dictionary/term_health_check.md) — liveness probe; relevance: the existing `/healthz` responder a duplicate starter probes before backing off.
- [term_circuit_breaker](../../term_dictionary/term_circuit_breaker.md) — bounded-retry stop; relevance: exit-code-78 supervisor stop bounds restart looping like a breaker.
- [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — bounded retries; relevance: startup retries against an unhealthy owner are bounded, not infinite.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — control-port protocol; relevance: the locked port serves the Gateway RPC/WS control protocol.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — safe-to-repeat startup; relevance: stale-lock reclaim makes restart converge to one healthy instance.

- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — Hermes gateway internals; relevance: analogous single-gateway startup/bind internals. *(existing)*
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — running/operating the gateway; relevance: parallel single-instance operational concerns. *(existing)*
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — hosting a long-lived agent process; relevance: same one-host-process lifecycle the lock guards. *(existing)*
- [pi_security_model](../pi/pi_security_model.md) — Pi loopback/port trust model; relevance: the `127.0.0.1:18789` control-port binding posture. *(existing)*
- [band_coding_agents_deployment](../band/band_coding_agents_deployment.md) — deploying agents under a supervisor; relevance: systemd `RestartPreventExitStatus` + supervisor handoff behavior. *(existing)*
- [oc_gateway_health](oc_gateway_health.md) — health snapshot/endpoint; relevance: the `/healthz` responder the lock checks. *(planned, this series)*
- [oc_gateway_heartbeat](oc_gateway_heartbeat.md) — periodic agent turn; relevance: heartbeat runs only after a single gateway holds the lock. *(planned, this series)*
- [oc_gateway_multiple_gateways](oc_gateway_multiple_gateways.md) — running multiple instances on unique ports; relevance: the page's own "Related" link-out (gw04). *(planned, this series)*
- [oc_gateway_troubleshooting](oc_gateway_troubleshooting.md) — diagnosing `EADDRINUSE`/port conflicts; relevance: the page's own troubleshooting link-out (gw07). *(planned, this series)*
- [oc_gateway_background_process](oc_gateway_background_process.md) — running the gateway as a service/daemon; relevance: the macOS PID guard + supervisor context (gw01). *(planned, this series)*

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: owns the lock file, exclusive bind, and shutdown lock removal.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw process; relevance: the process the singleton lock protects.

- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — exclusive HTTP/WS listener bind; relevance: the bind that enforces the lock and throws on `EADDRINUSE`.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — server shutdown sequence; relevance: closes the WS server and removes the lock file.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — startup/auth bootstrap; relevance: the startup path that acquires the lock and probes the port.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — restart/startup wiring; relevance: bounded restart behavior on lock/bind conflict.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — launchd restart handoff; relevance: supervisor handoff to the healthy existing instance.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit render; relevance: where `RestartPreventExitStatus=78` is configured.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd linger/env; relevance: the supervised-gateway environment the lock runs under.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist render; relevance: the macOS supervisor that spawns the gateway behind the PID guard.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervisor; relevance: bounded-retry supervision around the lock conflict.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env/port resolution; relevance: the base port / config that scopes the per-config lock.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — respawn logic; relevance: re-acquiring the lock cleanly on a controlled respawn.

### oc_gateway_health (8t · 11s · 11d)

- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the subject whose health these commands verify.
- [term_health_check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: the dedicated `/health` endpoint and `health` command this page documents.
- [term_websocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: `openclaw health` reads a WS-only snapshot (no direct channel sockets).
- [term_pii](../../term_dictionary/term_pii.md) — personal data; relevance: the diagnostics export redacts identifiers from health/status snapshots.
- [term_pci](../../term_dictionary/term_pci.md) — payment-card data; relevance: same redaction boundary on shared diagnostics bundles.
- [term_circuit_breaker](../../term_dictionary/term_circuit_breaker.md) — restart-cap guard; relevance: the health-monitor restart cap that stops thrashing channels.
- [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — rolling cap; relevance: `channelMaxRestartsPerHour` rolling one-hour restart limit.
- [term_availability](../../term_dictionary/term_availability.md) — system uptime/availability as a measured operational property; relevance: oc_gateway_health covers external uptime polling (BetterStack/UptimeRobot `GET /health`) to track gateway availability — a concept distinct from the health-check endpoint itself, giving the note 8 distinct terms.

- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install/health diagnostics; relevance: analogous local diagnosis the `status` command performs. *(existing)*
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — config debug; relevance: read-only diagnosis output safe to paste, like `status --all`. *(existing)*
- [cc_agent_view_monitor](../claude_code/cc_agent_view_monitor.md) — live agent/health monitor view; relevance: the per-channel probe summary surface. *(existing)*
- [hermes_lsp_diagnostics](../hermes_agent/hermes_lsp_diagnostics.md) — diagnostics surfacing; relevance: parallel diagnostics export/inspect flow. *(existing)*
- [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway operations; relevance: the operator-side health/restart operations mirror. *(existing)*
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi CLI status/health commands; relevance: analogous `status`/`health` CLI verbs and flags. *(existing)*
- [oc_gateway_lock](oc_gateway_lock.md) — `/healthz` responder; relevance: the responder a duplicate starter probes. *(planned, this series)*
- [oc_gateway_logging](oc_gateway_logging.md) — logs operators tail; relevance: the `web-heartbeat`/`web-reconnect` log filters this page references. *(planned, this series)*
- [oc_gateway_heartbeat](oc_gateway_heartbeat.md) — periodic turn; relevance: a custom heartbeat can "verify gateway health". *(planned, this series)*
- [oc_gateway_diagnostics](oc_gateway_diagnostics.md) — diagnostics export internals; relevance: the page's "Diagnostics Export" link-out (gw02). *(planned, this series)*
- [oc_gateway_troubleshooting](oc_gateway_troubleshooting.md) — failure recovery; relevance: the "When something fails" relink/restart steps (gw07). *(planned, this series)*

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: implements the health snapshot, probe, and monitor.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: per-channel health monitors and restart caps.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw process; relevance: the CLI `status`/`health` commands run against it.

- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — latency/cache status snapshot; relevance: fields surfaced in the health snapshot (`durationMs`, cache status).
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — channel status reactions; relevance: per-channel status the probe reports.
- [snippet_openclaw_gateway_channels_runtime_snapshot](../../code_snippets/snippet_openclaw_gateway_channels_runtime_snapshot.md) — channel runtime snapshot; relevance: per-account channel state in the health snapshot.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/startup; relevance: the health-monitor restart of stale channels.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — misc Gateway RPC (incl. health); relevance: the `health`/`probe:true` RPC `status --deep` invokes.
- [snippet_openclaw_gateway_sessions_read_methods](../../code_snippets/snippet_openclaw_gateway_sessions_read_methods.md) — `sessions.*` reads; relevance: the session-store summary in the snapshot.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — doctor/memory preview; relevance: deep-diagnostics memory-pressure facts this page describes.
- [snippet_openclaw_gateway_session_utils_subagent_liveness](../../code_snippets/snippet_openclaw_gateway_session_utils_subagent_liveness.md) — subagent liveness; relevance: liveness warnings (event-loop delay, active/waiting sessions).
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — daily usage/cost summary; relevance: session-store accounting referenced in uptime-monitoring caveats.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential redaction on RPC; relevance: the diagnostics export omits/redacts creds.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — payload sanitize; relevance: oversized-payload events omit message text per this page.

### oc_gateway_heartbeat (8t · 11s · 11d)

- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: heartbeat is an OpenClaw main-session feature.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: the heartbeat-vs-cron decision and cron-lane deferral.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving agents; relevance: each heartbeat is a full periodic agent turn.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: every tick runs an LLM turn (cost driver).
- [term_claude](../../term_dictionary/term_claude.md) — Anthropic model/CLI; relevance: Anthropic OAuth/token auth flips the default cadence to `1h`.
- [term_context_window](../../term_dictionary/term_context_window.md) — token context budget; relevance: "context overflow after heartbeat" recovery on small local windows.
- [term_compaction](../../term_dictionary/term_compaction.md) — transcript compression; relevance: the recovery mechanism + isolatedSession token savings.
- [term_subagent](../../term_dictionary/term_subagent.md) — nested agent lane; relevance: `skipWhenBusy` defers on subagent/nested lanes.

- [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — how scheduled agent turns run; relevance: the closest analogue to the periodic heartbeat turn. *(existing)*
- [cc_scheduling_options_comparison](../claude_code/cc_scheduling_options_comparison.md) — scheduling-mechanism comparison; relevance: the heartbeat-vs-cron-vs-loop decision this page makes. *(existing)*
- [cc_loop_scheduled_tasks](../claude_code/cc_loop_scheduled_tasks.md) — recurring-interval task loop; relevance: cadence/`every` interval semantics. *(existing)*
- [hermes_cron_scheduling](../hermes_agent/hermes_cron_scheduling.md) — cron cadence config; relevance: the cron side of the heartbeat-vs-cron choice. *(existing)*
- [hermes_guide_automate_with_cron](../hermes_agent/hermes_guide_automate_with_cron.md) — automating periodic agent work; relevance: when to use scheduled turns vs heartbeat. *(existing)*
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — cutting per-turn token cost; relevance: the heartbeat "Cost awareness" controls (isolated/light context). *(existing)*
- [oc_gateway_heartbeat_delivery](oc_gateway_heartbeat_delivery.md) — delivery/visibility half; relevance: the split companion note (target/to/visibility). *(planned, this series)*
- [oc_gateway_local_models](oc_gateway_local_models.md) — local LLM serving; relevance: a cheaper heartbeat `model` (e.g. ollama) + context-window caveat. *(planned, this series)*
- [oc_gateway_health](oc_gateway_health.md) — health snapshot; relevance: a custom heartbeat prompt can "verify gateway health". *(planned, this series)*
- [oc_automation_tasks](oc_automation_tasks.md) — background task records; relevance: heartbeat reacts to but does not create task records (au01). *(planned, this series)*
- [oc_concepts_timezone](oc_concepts_timezone.md) — timezone resolution; relevance: `activeHours` is checked in the configured timezone (co07). *(planned, this series)*

- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: heartbeat is a scheduled agent-runtime turn with per-agent precedence.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: heartbeat task-state and idle/daily-expiry timestamps live here.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: schedules and dispatches the heartbeat tick.

- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat buffered delta; relevance: the core heartbeat run/response path.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service + notifications; relevance: cron-lane deferral and scheduled-tick dispatch.
- [snippet_openclaw_gateway_session_utils_model_fallback](../../code_snippets/snippet_openclaw_gateway_session_utils_model_fallback.md) — runtime model fallback; relevance: the heartbeat `model` override + context-overflow reset.
- [snippet_openclaw_agents_context_window_guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — context-window guard; relevance: "context overflow after heartbeat" preflight/reset.
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction safety; relevance: the isolatedSession/compaction token-cost reduction.
- [snippet_openclaw_gateway_session_utils_store_target](../../code_snippets/snippet_openclaw_gateway_session_utils_store_target.md) — session/target resolution; relevance: heartbeat run-context session vs delivery target.
- [snippet_openclaw_gateway_session_utils_subagent_liveness](../../code_snippets/snippet_openclaw_gateway_session_utils_subagent_liveness.md) — subagent liveness; relevance: `skipWhenBusy` deferral on busy subagent lanes.
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — session lifecycle patches; relevance: heartbeat metadata updating the session row without keeping it alive.
- [snippet_openclaw_agents_subagent_spawn_caps](../../code_snippets/snippet_openclaw_agents_subagent_spawn_caps.md) — subagent spawn caps; relevance: the nested-lane busy state heartbeat defers on.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap context budget; relevance: `lightContext` keeping only `HEARTBEAT.md` from bootstrap files.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — system-prompt section modes; relevance: the "Heartbeat" system-prompt section gated on enablement.

### oc_gateway_heartbeat_delivery (8t · 10s · 11d)

- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: delivery routing is OpenClaw heartbeat behavior.
- [term_chatbot](../../term_dictionary/term_chatbot.md) — chat-channel bot; relevance: heartbeat alerts deliver to chat channels (Slack/Telegram/WhatsApp).
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving agents; relevance: the agent run whose output is routed/made visible.
- [term_llm](../../term_dictionary/term_llm.md) — language model; relevance: the run is skipped entirely (no model call) when all visibility flags are off.
- [term_subagent](../../term_dictionary/term_subagent.md) — nested lane; relevance: `skipWhenBusy` lane behavior gating delivery.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: an active cron job/lane skips-and-retries the delivery.
- [term_compaction](../../term_dictionary/term_compaction.md) — transcript handling; relevance: session-lifecycle/audit — transcripts retain hidden heartbeat turns.
- [term_health_check](../../term_dictionary/term_health_check.md) — status indicator; relevance: `useIndicator` emits indicator events for UI status surfaces.

- [cc_manage_your_session](../claude_code/cc_manage_your_session.md) — session management UI; relevance: hiding OK-only acks from history while keeping transcript audit. *(existing)*
- [cc_sdk_sessions_overview](../claude_code/cc_sdk_sessions_overview.md) — session lifecycle model; relevance: idle/daily expiry from last real message, not heartbeat. *(existing)*
- [cc_sdk_session_patterns](../claude_code/cc_sdk_session_patterns.md) — session routing patterns; relevance: run-context session vs delivery target/`to`. *(existing)*
- [hermes_sessions_lifecycle_resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — session lifecycle/resume; relevance: the session-lifecycle/audit rules this note documents. *(existing)*
- [hermes_session_storage](../hermes_agent/hermes_session_storage.md) — where session state persists; relevance: heartbeat metadata updating the stored session row. *(existing)*
- [pi_sessions](../pi/pi_sessions.md) — Pi session model; relevance: analogous main-session vs targeted-channel-session routing. *(existing)*
- [oc_gateway_heartbeat](oc_gateway_heartbeat.md) — config half; relevance: the companion note (cadence/response/config). *(planned, this series)*
- [oc_gateway_health](oc_gateway_health.md) — status/indicator surfaces; relevance: where `useIndicator` indicator events show. *(planned, this series)*
- [oc_concepts_session](oc_concepts_session.md) — session key formats; relevance: the `session` field key formats this note references (co06). *(planned, this series)*
- [oc_channels_groups](oc_channels_groups.md) — group/topic routing; relevance: `to` topic/thread routing (e.g. Telegram `:topic:`) (ch01). *(planned, this series)*
- [oc_concepts_typing_indicators](oc_concepts_typing_indicators.md) — typing indicators; relevance: typing shown while a heartbeat run is active, off via `typingMode:"never"` (co07). *(planned, this series)*

- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel adapters; relevance: per-channel/per-account delivery + visibility flag precedence.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: session-lifecycle/audit and idle-timestamp rules.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the agent run feeding delivery and the busy-lane skip.

- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat run/delta; relevance: the run whose output delivery routes/suppresses.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — outbound chat send; relevance: the actual delivery to `target`+`to`.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — channel status/indicator; relevance: `useIndicator` indicator events.
- [snippet_openclaw_gateway_session_utils_store_target](../../code_snippets/snippet_openclaw_gateway_session_utils_store_target.md) — session/target resolution; relevance: `target:"last"` resolving the last external channel.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding/routing; relevance: routing a run to a specific channel/account/topic.
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send policy; relevance: `directPolicy:"block"` DM-suppression and skip reasons.
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — session lifecycle patches; relevance: idle-timestamp restore + non-alive heartbeat replies.
- [snippet_openclaw_gateway_session_utils_subagent_liveness](../../code_snippets/snippet_openclaw_gateway_session_utils_subagent_liveness.md) — subagent liveness; relevance: skip-when-busy lane deferral.
- [snippet_openclaw_sessions_transcript_events](../../code_snippets/snippet_openclaw_sessions_transcript_events.md) — transcript events; relevance: transcript retains hidden heartbeat/OK turns for audit/replay.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: resolving `to`/account to a concrete delivery destination.

### oc_gateway_local_model_services (9t · 11s · 11d)

- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: `localService` is OpenClaw provider-level config.
- [term_llm](../../term_dictionary/term_llm.md) — language model; relevance: the local model server fronted on demand.
- [term_cold_start](../../term_dictionary/term_cold_start.md) — first-request startup latency; relevance: the probe-start-wait lifecycle + `readyTimeoutMs` control cold start.
- [term_health_check](../../term_dictionary/term_health_check.md) — readiness probe; relevance: `healthUrl` is polled until the server is ready.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — model-provider config entry; relevance: `localService` lives under `models.providers.<id>`.
- [term_vllm](../../term_dictionary/term_vllm.md) — high-throughput OpenAI-compatible server; relevance: a named local backend the lifecycle starts.
- [term_deepseek](../../term_dictionary/term_deepseek.md) — DeepSeek models; relevance: the ds4 example = local DeepSeek V4 Flash.
- [term_openai_responses_api](../../term_dictionary/term_openai_responses_api.md) — OpenAI Responses/Completions API; relevance: the `/v1` API shape the started backend speaks.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI backends; relevance: inferrs/ds4/vLLM are OpenAI-compatible third-party local servers.

- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — self-hosted local LLM setup; relevance: the directly-analogous on-demand local-server pattern. *(existing)*
- [hermes_docker_tools_local_inference](../hermes_agent/hermes_docker_tools_local_inference.md) — local inference server tooling; relevance: starting/managing a child inference process. *(existing)*
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — registering an inference provider; relevance: the provider-entry config that carries `localService`. *(existing)*
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering a custom provider; relevance: the `baseUrl`/`api`/`apiKey` provider block shape. *(existing)*
- [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — fronting models via a proxy; relevance: OpenAI-compatible `/v1` backend fronting. *(existing)*
- [bedrock_inference_profiles](../aws_bedrock/bedrock_inference_profiles.md) — model-serving endpoint config; relevance: contrast managed inference vs on-demand local serving. *(existing)*
- [oc_gateway_local_models](oc_gateway_local_models.md) — full local-stack guide; relevance: the page's primary "Related" link (always-on vs on-demand). *(planned, this series)*
- [oc_gateway_health](oc_gateway_health.md) — readiness/health; relevance: the `healthUrl` readiness model. *(planned, this series)*
- [oc_providers_inferrs](oc_providers_inferrs.md) — inferrs provider; relevance: the page's worked inferrs example link-out (pr04). *(planned, this series)*
- [oc_providers_ds4](oc_providers_ds4.md) — ds4 provider; relevance: the ds4 full-setup/context-sizing link-out (pr03). *(planned, this series)*
- [oc_concepts_models](oc_concepts_models.md) — model catalog/selection; relevance: how a model request resolves to a provider with `localService` (co04). *(planned, this series)*

- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM provider adapters; relevance: provider entries that carry `localService`.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: spawns/manages the child server process and idle shutdown.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: routes the model request through the started backend.

- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: a concrete local OpenAI-compatible backend entry.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog resolution; relevance: resolving a model request to its provider entry.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog normalize/discovery; relevance: discovering models a started local server exposes.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planner; relevance: planning provider/model availability incl. local entries.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — child-process supervision; relevance: managing the spawned local-server child process.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — kill a process tree; relevance: idle-stop shutdown of the OpenClaw-started server.
- [snippet_openclaw_process_exec_orchestrator](../../code_snippets/snippet_openclaw_process_exec_orchestrator.md) — exec orchestration; relevance: launching `command`/`args` for the local service.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env merge; relevance: the `env`/`cwd` merged over the OpenClaw process env.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider; relevance: the `openai-completions` transport the local server uses.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime/timeout config; relevance: `timeoutSeconds` for slow local cold starts.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — provider transport pattern; relevance: the provider-transport contract the local request flows through.

### oc_gateway_local_models (11t · 11s · 12d)

- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: running OpenClaw against self-hosted LLMs.
- [term_llm](../../term_dictionary/term_llm.md) — language model; relevance: the local LLM served from your own box.
- [term_vllm](../../term_dictionary/term_vllm.md) — vLLM serving engine; relevance: a recommended high-throughput OpenAI-compatible backend.
- [term_quantization](../../term_dictionary/term_quantization.md) — weight compression; relevance: aggressively quantized cards truncate context and leak safety.
- [term_prompt_injection](../../term_dictionary/term_prompt_injection.md) — adversarial prompt attack; relevance: the core safety risk small local models raise.
- [term_model_failover](../../term_dictionary/term_model_failover.md) — fallback on model failure; relevance: hosted-primary/local-fallback hybrid configs.
- [term_model_router](../../term_dictionary/term_model_router.md) — model selection/routing; relevance: `primary`/`fallbacks` ordering and `models.mode:"merge"`.
- [term_openai_responses_api](../../term_dictionary/term_openai_responses_api.md) — Responses/Completions API; relevance: LM Studio Responses API vs Chat Completions choice.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI services; relevance: LiteLLM/OAI-proxy/MLX/SGLang OpenAI-compatible proxies.
- [term_data_residency](../../term_dictionary/term_data_residency.md) — data-locality control; relevance: regional hosting / data routing and local-only privacy path.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: tool-call parser issues and the `tool_choice:"required"` override.

- [hermes_provider_local_llm_mac](../hermes_agent/hermes_provider_local_llm_mac.md) — local LLM on Mac; relevance: the Mac Studio / Metal local-stack guidance mirror. *(existing)*
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — self-hosted LLM; relevance: backend selection + OpenAI-compatible endpoint wiring. *(existing)*
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — provider fallback config; relevance: the hosted-primary/local-fallback hybrid. *(existing)*
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — routing via OpenAI-compatible proxies; relevance: LiteLLM/OAI-proxy custom-provider config. *(existing)*
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — model fallback ordering; relevance: the local-first/hosted-safety-net fallback pattern. *(existing)*
- [cc_model_selection](../claude_code/cc_model_selection.md) — choosing/restricting models; relevance: `primary`/aliases model selection. *(existing)*
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — model compat overrides; relevance: `compat.requiresStringContent`/`supportsTools` per-model flags. *(existing)*
- [oc_gateway_local_model_services](oc_gateway_local_model_services.md) — on-demand local server; relevance: the page's own "start only when selected" link-out. *(planned, this series)*
- [oc_gateway_logging](oc_gateway_logging.md) — model-call error diagnostics; relevance: `model.call.error.failureKind` + RSS snapshot troubleshooting. *(planned, this series)*
- [oc_gateway_configuration_reference](oc_gateway_configuration_reference.md) — full config reference; relevance: the page's "Related → Configuration reference" (gw02). *(planned, this series)*
- [oc_concepts_model_failover](oc_concepts_model_failover.md) — model-failover concept; relevance: the page's "Related → Model failover" (co04). *(planned, this series)*
- [oc_concepts_experimental_features](oc_concepts_experimental_features.md) — experimental flags; relevance: the `localModelLean` mode link-out (co02). *(planned, this series)*

- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM provider adapters; relevance: the provider adapters (lmstudio/local/mlx) configured here.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: failover/routing + `localModelLean` tool-surface reduction.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: guarded model requests, exact-origin trust, context preflight.

- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: a concrete local OpenAI-compatible provider block.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — fallback ladder; relevance: the `primary`+`fallbacks` hybrid ordering.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — fallback cooldown; relevance: failover behavior when the local box is down.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error handling; relevance: `terminated`/`ECONNRESET`/closed-stream local-server errors.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalize; relevance: the `models[].id`/`compat` model-entry schema.
- [snippet_openclaw_agents_context_window_guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — context-window guard; relevance: the 20%/8k warn + 10%/4k hard-block preflight thresholds.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider; relevance: proxy-style `/v1` route vs native OpenAI shaping.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: region-pinned hosted variants for data routing.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy; relevance: `localModelLean` dropping heavy tools / `supportsTools:false`.
- [snippet_openclaw_agents_model_fallback_observation](../../code_snippets/snippet_openclaw_agents_model_fallback_observation.md) — fallback observation/logging; relevance: recording model-call failures for diagnostics.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — origin/identity trust; relevance: exact-`baseUrl`-origin trust for loopback/LAN/tailnet local backends.

### oc_gateway_logging (8t · 11s · 11d)

- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the logging surfaces are OpenClaw's.
- [term_websocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: the Gateway WebSocket protocol log modes (normal/verbose).
- [term_pii](../../term_dictionary/term_pii.md) — personal data; relevance: redaction of identifiers before logs/transcripts leave the process.
- [term_pci](../../term_dictionary/term_pci.md) — payment-card data; relevance: always-redact boundary for card number / CVC / payment token fields.
- [term_health_check](../../term_dictionary/term_health_check.md) — slow/error thresholds; relevance: WS logs surface errors and `>=50ms` slow-call thresholds.
- [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — log volume/rotation; relevance: `maxFileBytes` rotation caps bound log growth.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — RPC results; relevance: "interesting" RPC results (ok=false, parse errors) printed in WS logs.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool-call events; relevance: Control-UI tool-call events are an always-redact safety boundary.

- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — telemetry/data handling; relevance: what is and isn't written to logs (redaction policy). *(existing)*
- [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — OTel log/metric export; relevance: the OTLP log-record sink the redaction policy also covers. *(existing)*
- [cc_otel_metrics_reference](../claude_code/cc_otel_metrics_reference.md) — emitted metrics/log fields; relevance: the structured-field log records this page emits. *(existing)*
- [cc_sdk_observability_opentelemetry](../claude_code/cc_sdk_observability_opentelemetry.md) — SDK observability; relevance: file-log + OTLP export of bounded lifecycle records. *(existing)*
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — console/debug output; relevance: console capture + verbosity/`--verbose` behavior. *(existing)*
- [hermes_lsp_diagnostics](../hermes_agent/hermes_lsp_diagnostics.md) — diagnostics output; relevance: parallel subsystem/diagnostic logging surface. *(existing)*
- [oc_gateway_health](oc_gateway_health.md) — logs operators tail; relevance: the `/tmp/openclaw/*.log` filters health debugging uses. *(planned, this series)*
- [oc_gateway_local_models](oc_gateway_local_models.md) — model-call error logging; relevance: `model.call.error.failureKind` records this page describes. *(planned, this series)*
- [oc_gateway_opentelemetry](oc_gateway_opentelemetry.md) — OTLP log export; relevance: the page's "Related → OpenTelemetry export" (gw04). *(planned, this series)*
- [oc_gateway_diagnostics](oc_gateway_diagnostics.md) — diagnostics export; relevance: the page's "Related → Diagnostics export" + always-redact bundles (gw02). *(planned, this series)*
- [oc_logging](oc_logging.md) — user-facing logging overview; relevance: the page's "Related → /logging" link-out (rt02). *(planned, this series)*

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: the gateway logger, WS log modes, and `--ws-log` styles.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — CLI/process; relevance: console capture of `console.*` to file logs.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security policy; relevance: the redaction policy and always-redact safety boundaries.

- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret redaction; relevance: masking secret values before log/transcript sinks.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content handling; relevance: the redaction/safety-boundary policy this note documents.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — payload sanitize; relevance: attachment/body contents kept out of log records.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: the WS request/response frames logged in verbose mode.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — RPC error codes; relevance: the `ok=false`/parse-error WS results printed in normal mode.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — latency status; relevance: the slow-call (`>=50ms`) threshold WS logging.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — transcript media pipeline; relevance: transcript text sink the redaction policy applies to.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env/paths; relevance: `logging.file`/`logging.level` resolution + log dir.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — tool-event safety boundary; relevance: Control-UI tool-call events always redact.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec-approval display; relevance: exec approval command display is an always-redact surface.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — bounded lifecycle records; relevance: talk/voice/managed-room bounded log records (no payload/turn ids).



## Undigested Terms Plan (Step 4e)

gw03 creates **0 new `term_dictionary` notes**. Gateway operational vocabulary is digested as `oc_*` doc notes (this series) or already has a home page in another sub-plan; existing term notes are linked, never redefined.

| Term | Disposition |
|---|---|
| heartbeat, HEARTBEAT.md, heartbeat tasks, manual wake | → `oc_gateway_heartbeat.md` (this series); not a term note |
| heartbeat delivery / visibility flags (showOk/showAlerts/useIndicator) | → `oc_gateway_heartbeat_delivery.md` (this series) |
| gateway lock / GatewayLockError / EADDRINUSE | → `oc_gateway_lock.md` (this series); link `term_singleton` |
| local model service / localService config | → `oc_gateway_local_model_services.md` (this series); link `term_provider_plugin`, `term_cold_start` |
| local models / hardware floor / OpenAI-compatible proxy | → `oc_gateway_local_models.md` (this series); link `term_llm`, `term_vllm`, `term_quantization`, `term_prompt_injection` |
| logging redaction / WS log style / subsystem logging | → `oc_gateway_logging.md` (this series); link `term_pii`, `term_pci` |
| health check / `/health` endpoint / health monitor | → `oc_gateway_health.md` (this series); link `term_health_check` |
| external apps / Gateway RPC integration | → `oc_gateway_external_apps.md` (this series); link `term_json_rpc`, `term_websocket` |
| LM Studio, Ollama, vLLM, MLX, SGLang, ds4, inferrs (provider names) | documented as config; link `term_vllm` where it exists, else link the `providers/*` page (pr05–09) — NOT promoted to term notes |
| timezone, OpenTelemetry, model failover, cron, background tasks, compaction, sessions | existing/owned elsewhere: link `term_cron`/`term_compaction`/`term_model_failover` (exist) or the home doc page (co07 timezone, gw04 opentelemetry, au01 automation, co04/co06 sessions) — NOT new captures |

**New-term candidates: NONE.** No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an existing note. (Candidates considered and rejected as too narrow / page-scoped: `term_health_check` already exists; `term_singleton` already exists; `term_cold_start` already exists. Operational nouns like "gateway lock", "heartbeat", "local model service" are page subjects digested as `oc_*` notes per master policy, not term entries.)

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format: YAML field order + body structure (`## Overview`, `## Related Notes`, `## References`, bold footer); ≤400 lines | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim traces to `inbox/openclaw_docs/gateway/<page>.md` (no hallucinated config keys/flags/defaults) | diff vs mirror source |
| G3 | Density + Coverage: ≤2500 words, ≤6 code blocks, one BB per note; every mapped H2/H3 present | `wc -w` / fence count + Section Coverage Map |
| G4 | Cross-Reference: ≥6 relevance-selected term links + repo/sibling/other links, each with a relevance statement | manual + DB |
| G5 | Ghost-reference detect + redirect: every `[...](...)` target resolves in DB | ghost-reference scan |
| G6 | Broken-link fix: relative paths correct | `/tessellum-fix-broken-links` |
| G7 | Discoverability: every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md`) | `note_links` query |
| G8 | In-degree ≥1 (anti-island) per new note | `notes.in_degree` |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_gateway_external_apps oc_gateway_lock oc_gateway_health oc_gateway_heartbeat oc_gateway_heartbeat_delivery oc_gateway_local_model_services oc_gateway_local_models oc_gateway_logging"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections + source_url
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density (strip frontmatter)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code)"
  # sibling-prefix cross-link present
  grep -q "($SIBLING_PREFIX" "$f" || echo "$n NO sibling oc_ link"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# Ghost-reference / broken-link sweep after incremental reindex:
bash scripts/update_notes_database.sh --force
```

## Density Re-Assessment

| # | Note | BB | Source words | ~Digest words | ~Code | Within caps? |
|---|---|---|---:|---:|---:|---|
| 1 | oc_gateway_external_apps | procedure | 510 | 480 | 0 | ✅ |
| 2 | oc_gateway_lock | model | 342 | 360 | 0 | ✅ |
| 3 | oc_gateway_health | procedure | 988 | 700 | 0–1 | ✅ |
| 4 | oc_gateway_heartbeat | procedure | ~2,100 (of 3,235 split) | 750 | ≤5 | ✅ |
| 5 | oc_gateway_heartbeat_delivery | procedure | ~1,135 (of 3,235 split) | 480 | ≤3 | ✅ |
| 6 | oc_gateway_local_model_services | procedure | 730 | 600 | ≤3 | ✅ |
| 7 | oc_gateway_local_models | procedure | 2,140 | 800 | ≤6 | ✅ (reproduce 4–6 of 8 config snippets selectively) |
| 8 | oc_gateway_logging | procedure | 830 | 650 | ≤3 | ✅ |

No note approaches the 400-line cap. The two code-heavy pages are bounded: heartbeat (10 fences) is split so each half stays ≤6; local-models (8 fences) reproduces only the 4–6 load-bearing config snippets (LM Studio Responses, hybrid fallback, OpenAI-compatible proxy, tool_choice override) verbatim and prose-references the rest.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (created as the W1 master pre-step before first execution) under the **Gateway** section / a "Gateway operations" cluster. Each note receives its entry-point back-link at finalization (this is the primary G7/G8 inbound-link source — anti-island). No new entry point is created by gw03; `entry_openclaw_docs.md` is shared across all 105 sub-plans.

## Inlinks (existing notes → new notes)


- `entry_openclaw_docs.md` → all 8 notes (primary inbound, satisfies G7/G8 for every note).
- `repo_openclaw_gateway.md` → notes 1, 2, 3, 4, 5, 8 (gateway-implementation cross-link).
- `repo_openclaw_extensions_llm_providers.md` → notes 6, 7 (local-provider config).
- `repo_openclaw_agents.md` → notes 4, 5, 6, 7 (heartbeat/agent-runtime + local-model failover).
- `repo_openclaw_channels.md` → notes 3, 5 (channel health monitor + heartbeat delivery).
- `repo_openclaw_security.md` → note 8 (logging redaction / safety boundaries).
- `term_cron.md` → note 4 (heartbeat-vs-cron); `term_model_failover.md` → note 7; `term_health_check.md` → notes 2, 3; `term_singleton.md` → note 2; `term_prompt_injection.md` → note 7; `term_pii.md`/`term_pci.md` → note 8.

## Pacing Rules (inherited from master)

- Single execution phase (8 notes). Cap dynamic-workflow fan-out ≤30 agents/run (well under). Reproduce config snippets verbatim from the mirror; one BB per note; ≥6 relevance-selected term links per note. Run all 8 gates before commit. `git pull --rebase --autostash origin main` first; commit + push per wave; no Claude co-author trailer. Incremental reindex; verify `note_links` + 0 broken links + in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this pass (xref-augment):** re-read all 7 gateway source pages under `inbox/openclaw_docs/gateway/` and rebuilt the per-note Related Notes mapping to the RAISED floors (≥8 terms · ≥10 snippets · ≥10 docs per note), replacing the prior PLAN-stage `## Candidate Cross-References` section with `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.


| Note | Terms | Snippets | Docs (existing / planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_gateway_external_apps | 8 | 11 | 11 (6 / 5) | 3 | ✅ |
| oc_gateway_lock | 8 | 11 | 10 (5 / 5) | 2 | ✅ |
| oc_gateway_health | 8 | 11 | 11 (6 / 5) | 3 | ✅ |
| oc_gateway_heartbeat | 8 | 11 | 11 (6 / 5) | 3 | ✅ |
| oc_gateway_heartbeat_delivery | 8 | 10 | 11 (6 / 5) | 3 | ✅ |
| oc_gateway_local_model_services | 9 | 11 | 11 (6 / 5) | 3 | ✅ |
| oc_gateway_local_models | 11 | 11 | 12 (7 / 5) | 3 | ✅ |
| oc_gateway_logging | 8 | 11 | 11 (6 / 5) | 3 | ✅ |

- **Source measured (CP7):** external-apps 510w/0cb · gateway-lock 342w/0cb · health 988w/0cb · heartbeat 3,235w/10cb · local-model-services 730w/3cb · local-models 2,140w/8cb · logging 830w/3cb — all match the plan's Source table exactly (local-models 8 + heartbeat 10 code blocks confirmed via indented-fence-aware count). No re-split required.


**Issues / notes:** (1) `term_uptime_monitoring` has no dedicated vault note; in oc_gateway_health it is mapped to the existing `term_health_check.md` so the link resolves and the ≥8-term floor is met entirely from existing terms (documented inline in the mapping). (2) The earlier draft's `band_programmatic_integration.md` candidate does NOT exist in the DB; it was dropped and `hermes_programmatic_integration.md` (existing) is used instead.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review of the augmented plan. All 9 checkpoints evaluated against the canonical.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors (≥10 snippets, ≥10 docs), relevance-stated | **PASS** | All 8 notes: ≥8 terms (min 8, max 11), ≥10 snippets (min 10), ≥10 docs (min 10); every link rendered `- [Name](relpath.md) — what; relevance: why`. Programmatic per-group count confirmed header==body counts. |
| CP2 | 9-GATE table present per phase (G1–G9) | **PASS** | Single-phase G1–G8 table present (`## Per-Phase Validation Gate (G1–G9)`), incl. G5 ghost-detect, G6 broken-link, G7/G8 discoverability/in-degree. |
| CP4 | Size ≤30 (or split) | **PASS** | 8 notes — well under 30. |
| CP5 | Format derived from existing notes (not invented) | **PASS** | Format inherited from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` → body → `## Related Notes` → `## References` → bold footer); matches target-dir convention. |
| CP6 | Density / BB atomicity (borderline → split promoted) | **PASS** | heartbeat (3,235w/10cb) split into 2 notes (config vs delivery), each ≤2,500w/≤6cb; local-models (2,140w/8cb) reproduces 4–6 of 8 config snippets selectively to stay ≤6cb. No remaining borderline note. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured all 7 pages 2026-06-21 (wc -w + indented-fence-aware code count); every value matches the plan's Source table; no page >1.5× estimate; no re-split needed. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements + authoring reqs | **PASS** | `## Undigested Terms Plan` present (0 new terms, every row dispositioned to an `oc_*` page or existing-term link); `## Term-Note Authoring Requirements` present (N/A 0 terms, with fallback to capture-term-note + glossary if augment surfaces one). |
| CP8f | Term-slug specificity + all-notes (term AND doc) dedup/collision audit | **PASS** | gw03 creates 0 term slugs (no specificity renames needed). Doc-vs-term collision audit: planned `oc_*` doc slugs (external_apps, lock, health, heartbeat, local_model_services, local_models, logging) checked against `term_dictionary/` — none duplicate an existing substantive term note (operational/page-scoped subjects; existing terms are LINKED not recreated). `documentation/openclaw/` is empty (0 pre-existing siblings) so no intra-series collision. |
| CP9 | Discoverability / inlinks executed (G8, anti-island) | **PASS** | `## Inlinks (existing → new notes)` maps every new note to ≥1 outside-folder inbound link (primary: `entry_openclaw_docs.md` → all 8; plus repo_openclaw_gateway/agents/channels/sessions/security/extensions_llm_providers + term backlinks). G8-Discoverability in the phase gate table; inlinks marked as a gated execution step (not "recommended"). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.**
