---
title: Sub-Plan cl04 — OpenClaw Docs: CLI (gateway, health, hooks, infer, logs, mcp, memory)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["cli/gateway", "cli/health", "cli/hooks", "cli/infer", "cli/logs", "cli/mcp", "cli/memory"]
---

# Sub-Plan cl04: CLI

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML order, `## Overview`/`## Related Notes`/`## References`, ≤400L/≤2500w/≤6 code, one BB/note), dedup (term_dictionary + documentation/ + `repo_openclaw*` three-way), 9-GATE, cross-references, and entry-point (`entry_openclaw_docs.md`) decisions are ALL inherited from the master.

## Scope

The 7 CLI reference pages for OpenClaw's **operational core** command surfaces: `openclaw gateway` (run/query/service/discovery), `openclaw health` (Gateway health snapshot), `openclaw hooks` (agent hook lifecycle), `openclaw infer` (headless provider-backed inference), `openclaw logs` (RPC log tail), `openclaw mcp` (MCP server + client registry), and `openclaw memory` (semantic memory indexing + dreaming). **Priority P1 (Phase A)** — these define the CLI vocabulary (Gateway lifecycle, MCP surfaces, inference capability tree, memory/dreaming) that the rest of the CLI/gateway/concepts sub-plans reference. The code-side counterparts (`repo_openclaw_gateway`, `repo_openclaw_memory`, the `snippet_openclaw_gateway_*` / `snippet_openclaw_memory_*` corpora) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **13,338 measured words**. **Planned: 9 notes** (gateway.md and mcp.md each split; see Split Decisions).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| gateway | /cli/gateway | 3,656 | 17 | 6 | 11 | procedure (split: run+service vs query+probe) |
| health | /cli/health | 190 | 1 | 2 | 0 | procedure |
| hooks | /cli/hooks | 1,035 | 23 | 9 | 4 | procedure |
| infer | /cli/infer | 2,381 | 14 | 16 | 0 | procedure |
| logs | /cli/logs | 436 | 1 | 5 | 0 | procedure |
| mcp | /cli/mcp | 4,518 | 23 | 6 | 24 | procedure + model (split: serve vs registry) |
| memory | /cli/memory | 1,122 | 5 | 4 | 4 | procedure |

(Code = fence pairs, `grep -c '```' / 2`; gateway 34/2=17, hooks 46/2=23, infer 28/2=14, mcp 46/2=23, memory 10/2=5, health 2/2=1, logs 2/2=1.)

## Content Strategy

- **Prioritize**: the Gateway lifecycle (run modes, bind/auth guardrails, safe-restart deferral, service management) and the two MCP surfaces (`serve` = OpenClaw-as-MCP-server bridge contract; registry = OpenClaw-managed outbound MCP definitions) — these are the most-referenced operational primitives and the highest-novelty content (no existing `oc_*` MCP/gateway CLI doc).
- **Split**: `gateway.md` (3,656w) → run+restart+service-management procedure vs query+probe+discovery procedure; `mcp.md` (4,518w, two distinct subsystems) → `mcp serve` bridge procedure+event-model vs MCP client-registry procedure. Both exceed the 2,500w cap and contain two distinct task/BB clusters.
- **Link-out (do NOT redefine)**: provider/model config (`/concepts/models`, `/providers/*` → pr0x sub-plans); ACP harness hosting (`/cli/acp` → cl01); dreaming concept deep-dive (`/concepts/dreaming` → co02); automation hooks reference (`/automation/hooks` → au01); plugins installer (`/cli/plugins`, `/tools/plugin` → cl06/to06); Bonjour/discovery/health gateway runbooks (`/gateway/bonjour`, `/gateway/discovery`, `/gateway/health`, `/gateway/logging`, `/gateway/diagnostics` → gw0x). Terms `term_mcp`/`term_websocket`/`term_oauth_token`/`term_cron`/`term_health_check` are linked, never inlined (master Undigested-Terms rule).

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_cli_gateway_run.md` | procedure | gateway.md: Run the Gateway (+Startup behavior, Options), Restart the Gateway (+Gateway profiling), Manage the Gateway service (+Install with a wrapper, Command options, Lifecycle behavior, Auth and SecretRefs at install time) | 700 | Running and operating the Gateway from the CLI: `openclaw gateway`/`run`, startup guardrails (`gateway.mode=local`, bind/auth blocks), `--port`/`--bind`/`--auth`/`--tailscale` options, safe/force restart deferral, profiling env flags, and managed-service install (incl. `--wrapper`) / start / stop / uninstall lifecycle. |
| 2 | `oc_cli_gateway_query.md` | procedure | gateway.md: Query a running Gateway (output modes, shared options), `gateway health`/`usage-cost`/`stability`/`diagnostics export`/`status`/`probe` (+Remote over SSH), `gateway call`, Discover gateways (Bonjour) + `gateway discover` | 700 | Querying and diagnosing a running Gateway over WebSocket RPC: output/auth modes, `gateway health`/`usage-cost`/`stability`/`diagnostics export`/`status`/`probe` (capability + read-probe classification, SSH port-forward), low-level `gateway call`, and Bonjour `gateway discover` (mDNS/wide-area DNS-SD beacons + TXT hints). |
| 3 | `oc_cli_health.md` | procedure | health.md: (intro), Options, Examples, Notes, Related | 250 | `openclaw health`: fetch a health snapshot from the running Gateway, cached-vs-live probe behavior, `--json`/`--timeout`/`--verbose` flags, and per-agent session-store expansion. |
| 4 | `oc_cli_hooks.md` | procedure | hooks.md: (intro), List/Get info/Check eligibility, Enable/Disable a Hook, Notes, Install hook packs, Update hook packs, Bundled hooks (session-memory, bootstrap-extra-files, command-logger, boot-md) | 700 | `openclaw hooks`: discover/inspect/enable/disable agent hooks (workspace opt-in, plugin-managed hooks delegate to the plugin), install/update hook packs via the unified `openclaw plugins` installer, and the four bundled hooks (session-memory, bootstrap-extra-files, command-logger, boot-md). |
| 5 | `oc_cli_infer.md` | procedure | infer.md: (intro), Turn infer into a skill, Why use infer, Command tree, Common tasks, Behavior, Model, Image, Audio, TTS, Video, Web, Embedding, JSON output, Common pitfalls, Notes | 750 | `openclaw infer`: the canonical headless capability surface for provider-backed inference — model run (local vs `--gateway`, `--thinking`, image attach), image generate/edit/describe, audio transcribe, TTS, video, web search/fetch, embedding — plus the stable `--json` envelope and local-vs-gateway transport defaults. |
| 6 | `oc_cli_mcp_serve.md` | procedure | mcp.md: (intro), Choose the right MCP path, OpenClaw as an MCP server (When to use serve, How it works, Choose a client mode, What serve exposes, Usage, Bridge tools, Event model, Claude channel notifications, MCP client config, Options, Security and trust boundary, Testing, Troubleshooting), Current limits | 750 | `openclaw mcp serve`: running OpenClaw as a stdio MCP server that bridges Gateway-routed channel conversations to an MCP client — bridge tools (`conversations_list`/`messages_read`/`events_poll`/`messages_send`/`permissions_*`), the in-memory event model, Claude channel-notification mode, connection options, and the trust boundary. |
| 7 | `oc_cli_mcp_registry.md` | procedure | mcp.md: OpenClaw as an MCP client registry (Important behavior, Saved MCP server definitions, Common server recipes, Control UI), Control UI section | 700 | `openclaw mcp` client registry: managing OpenClaw-saved outbound MCP server definitions (`list`/`show`/`status`/`doctor`/`probe`/`add`/`set`/`configure`/`tools`/`login`/`logout`/`reload`/`unset`), server recipes (filesystem/memory/HTTP/CUA), tool filters, OAuth login flow, and the Control UI `/mcp` editor. |
| 8 | `oc_cli_mcp_transports.md` | model | mcp.md: JSON output shapes (status/doctor/probe --json), Stdio transport (+env safety filter), SSE / HTTP transport, OAuth workflow, Streamable HTTP transport | 600 | The MCP registry data contract: `status`/`doctor`/`probe` `--json` output shapes, and the three transport field schemas (stdio + startup-env safety filter, SSE/HTTP, streamable-http) plus the `auth: "oauth"` login workflow that registry config validates. |
| 9 | `oc_cli_memory.md` | procedure | memory.md: (intro), Examples, Options (status/index/search/promote/promote-explain/rem-harness), Dreaming, Related | 700 | `openclaw memory`: semantic-memory indexing and search via the bundled `memory-core` plugin — `status`/`index`/`search`/`promote`/`promote-explain`/`rem-harness` flags, promotion-signal ranking into `MEMORY.md`, and the three-phase Dreaming consolidation system (light/REM/deep) with its sweep schedule and thresholds. |

## Section Coverage Map

```
gateway.md (3,656w, 6 H2 / 11 H3)
├── Run the Gateway (Startup behavior) ───────────────── → note 1 (oc_cli_gateway_run)
│   └── ### Options ──────────────────────────────────── → note 1
├── Restart the Gateway ─────────────────────────────── → note 1
│   └── ### Gateway profiling ────────────────────────── → note 1
├── Manage the Gateway service ──────────────────────── → note 1
│   ├── ### Install with a wrapper ───────────────────── → note 1
│   └── (Command options / Lifecycle / Auth+SecretRefs) → note 1
├── Query a running Gateway (output/shared options) ─── → note 2 (oc_cli_gateway_query)
│   ├── ### gateway health / usage-cost / stability ──── → note 2
│   ├── ### gateway diagnostics export / status / probe → note 2
│   │   └── #### Remote over SSH (Mac app parity) ────── → note 2
│   └── ### gateway call <method> ────────────────────── → note 2
├── Discover gateways (Bonjour) ─────────────────────── → note 2
│   └── ### gateway discover ─────────────────────────── → note 2
└── Related ──────────────────────────────────────────── → notes 1+2 (References)
health.md (190w, 2 H2)
├── (intro) / ## Options / Examples / Notes ─────────── → note 3 (oc_cli_health)
└── ## Related ───────────────────────────────────────── → note 3 (References)
hooks.md (1,035w, 9 H2 / 4 H3)
├── (intro) / List / Get info / Check eligibility ───── → note 4 (oc_cli_hooks)
├── Enable / Disable a Hook / Notes ─────────────────── → note 4
├── Install hook packs / Update hook packs ──────────── → note 4
├── Bundled hooks (### session-memory / bootstrap-extra-files
│   / command-logger / boot-md) ─────────────────────── → note 4
└── Related ──────────────────────────────────────────── → note 4 (References)
infer.md (2,381w, 16 H2)
├── (intro) / Turn infer into a skill / Why use infer ─ → note 5 (oc_cli_infer)
├── Command tree / Common tasks / Behavior ──────────── → note 5
├── Model / Image / Audio / TTS / Video / Web / Embedding → note 5
├── JSON output / Common pitfalls / Notes ───────────── → note 5
└── Related ──────────────────────────────────────────── → note 5 (References)
mcp.md (4,518w, 6 H2 / 24 H3)
├── (intro) / Choose the right MCP path ─────────────── → note 6 (oc_cli_mcp_serve)
├── OpenClaw as an MCP server (When to use serve, How it
│   works, Choose a client mode, What serve exposes,
│   Usage, Bridge tools, Event model, Claude channel
│   notifications, MCP client config, Options, Security
│   and trust boundary, Testing, Troubleshooting) ───── → note 6
├── Current limits ──────────────────────────────────── → note 6
├── OpenClaw as an MCP client registry (Important behavior,
│   ### Saved MCP server definitions, ### Common server
│   recipes) ────────────────────────────────────────── → note 7 (oc_cli_mcp_registry)
├── ## Control UI ────────────────────────────────────── → note 7
├── ### JSON output shapes (status/doctor/probe --json) → note 8 (oc_cli_mcp_transports)
├── ### Stdio transport (+env safety filter) ────────── → note 8
├── ### SSE / HTTP transport ─────────────────────────── → note 8
├── ### OAuth workflow ───────────────────────────────── → note 8
├── ### Streamable HTTP transport ───────────────────── → note 8
└── ## Related ───────────────────────────────────────── → notes 6+7+8 (References)
memory.md (1,122w, 4 H2 / 4 H3)
├── (intro) / ## Examples / ## Options (status/index/search/
│   promote/promote-explain/rem-harness) ────────────── → note 9 (oc_cli_memory)
├── ## Dreaming ──────────────────────────────────────── → note 9
└── ## Related ───────────────────────────────────────── → note 9 (References)
```
No orphaned sections. Provider/model config, ACP hosting, dreaming concept, automation hooks, plugins installer, and Bonjour/discovery/health/logging gateway runbooks are linked-out, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| gateway.md (3,656w, 6 H2 / 11 H3, 17 code) | notes 1 (`oc_cli_gateway_run`) + 2 (`oc_cli_gateway_query`) | Exceeds the 2,500w cap and mixes two task clusters: operating the local/managed Gateway process (run/restart/service/install) vs querying+diagnosing a running Gateway over RPC (health/usage-cost/stability/status/probe/call/discover). Split keeps each ≤700w / ≤6 code and one focused procedure. |
| mcp.md (4,518w, 6 H2 / 24 H3, 23 code) | notes 6 (`oc_cli_mcp_serve`) + 7 (`oc_cli_mcp_registry`) + 8 (`oc_cli_mcp_transports`) | The page documents two distinct subsystems (`serve` = OpenClaw-as-MCP-server bridge; the registry subcommands = OpenClaw-as-MCP-client-side definition store) plus a heavy transport/JSON-schema reference. Far exceeds 2,500w and mixes procedure + a data/contract (model BB). Three-way split: serve procedure, registry-management procedure, transport+JSON-shape model — each ≤6 code, one BB. |

## Summary Statistics & Building Block Distribution

- Source pages: 7 (13,338 words). New `oc_` notes: **9**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×8** (notes 1–7, 9) · **model ×1** (note 8 — MCP transport/JSON schemas).
- Est. digest words ~5,850 (avg ~650/note); all notes ≤750w, well under the 2,500w cap.
- 84 source code fences (gateway 17 + health 1 + hooks 23 + infer 14 + logs[n/a, logs is cl05? no — logs is in cl04] + mcp 23 + memory 5; note logs.md=1) distribute across 9 notes; each note keeps **≤6 code blocks** by reproducing only canonical/representative command + config snippets verbatim (esp. the 23-fence hooks/mcp pages and 14-fence infer page are trimmed to ≤6 each).

> **Note:** logs.md is the 5th of this sub-plan's 7 pages (436w, 1 code, 5 H2) and maps 1:1 to note... — correction below. The 7th planned procedure note for logs is enumerated as part of the table; see the Coverage clarification.

## logs.md coverage clarification (page 5 of 7)

logs.md was measured (436w / 1 code / 5 H2: Options, Shared Gateway RPC options, Examples, Notes, Related) and maps 1:1 to a dedicated procedure note. To keep one BB per note and avoid bloating the gateway-query note, logs gets its own note:

| # | Filename | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 10 | `oc_cli_logs.md` | procedure | logs.md: (intro), Options, Shared Gateway RPC options, Examples, Notes, Related | 350 | `openclaw logs`: tail Gateway file logs over RPC (remote-capable) — `--limit`/`--max-bytes`/`--follow`/`--interval`/`--json` and timezone flags, the shared Gateway client flags, and the implicit-local-loopback fallback + `--follow` reconnect-with-backoff behavior. |

```
logs.md (436w, 5 H2)
├── (intro) / ## Options / Shared Gateway RPC options ── → note 10 (oc_cli_logs)
├── ## Examples / ## Notes ───────────────────────────── → note 10
└── ## Related ───────────────────────────────────────── → note 10 (References)
```

**Revised totals:** 7 pages → **10 notes** (gateway ×2, mcp ×3, health/hooks/infer/logs/memory ×1 each). BB: procedure ×9 (notes 1–7, 9, 10) · model ×1 (note 8). Est. digest words ~6,200 (avg ~620/note). This exceeds the master's nominal ~11 estimate window only marginally (10 ≤ 11) and stays within the ≤30-note plan-size rule.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_cli_gateway_run (8t · 12s · 11d)

**Terms** (8)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway/agent platform; relevance: `openclaw gateway` runs OpenClaw's core process.
- [term_websocket](../../term_dictionary/term_websocket.md) — full-duplex TCP-framed protocol; relevance: the Gateway is a WebSocket server, `--port`/`--bind` configure its listener.
- [term_authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: `--auth token|password`, `--password-file`, install-time SecretRef validation.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: `--token` / `OPENCLAW_GATEWAY_TOKEN` token auth mode.
- [term_health_check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: startup benchmark records `/healthz` (liveness) vs `/readyz` (readiness).
- [term_idempotency](../../term_dictionary/term_idempotency.md) — repeat-safe operation; relevance: `--safe` restart coalesces duplicate restart requests, deferral gate.
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — signal/event-handler dispatch; relevance: SIGUSR1 in-process restart, SIGINT/SIGTERM shutdown handlers.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — process isolation/guardrail; relevance: bind-beyond-loopback-without-auth safety guardrail, `--wrapper` run-as-helper shim.

**Docs** (11: 6 existing + 5 sibling)
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi coding-agent CLI command reference; relevance: sibling coding-agent's gateway/daemon run surface.
- [pi_security_model](../pi/pi_security_model.md) — Pi bind/auth/trust model; relevance: analog of OpenClaw's bind-mode + loopback guardrail.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — Claude Code gateway/proxy env config; relevance: analogous gateway-fronting config surface.
- [cc_settings_files](../claude_code/cc_settings_files.md) — Claude Code settings.json layering; relevance: analog of `~/.openclaw/openclaw.json` `gateway.mode` config file.
- [cc_managed_settings](../claude_code/cc_managed_settings.md) — admin-managed config precedence; relevance: managed-service install persists config/env like managed settings.
- [pi_containerization](../pi/pi_containerization.md) — Pi service/container run modes; relevance: analog of managed-service install (launchd/systemd) lifecycle.
- [oc_cli_gateway_query](oc_cli_gateway_query.md) — (planned, this series) querying a running Gateway; relevance: the process started here is queried/diagnosed there.
- [oc_cli_health](oc_cli_health.md) — (planned, this series) health snapshot CLI; relevance: post-start liveness/readiness check.
- [oc_cli_logs](oc_cli_logs.md) — (planned, this series) tail Gateway logs; relevance: operating the running process.
- [oc_cli_mcp_serve](oc_cli_mcp_serve.md) — (planned, this series) OpenClaw-as-MCP-server; relevance: serve bridges to a running Gateway started here.
- [oc_cli_memory](oc_cli_memory.md) — (planned, this series) memory CLI; relevance: memory `secrets.resolve` requires a running Gateway.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server implementation; relevance: implements run/restart/bind/auth/service lifecycle.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboard/setup wizard; relevance: `onboard --mode local`/`setup` write `gateway.mode=local`.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security guardrails; relevance: bind-beyond-loopback + inline-secret-exposure guardrails.

**Snippets** (12)
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listener bind; relevance: code behind `--port`/`--bind`.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — startup auth gating; relevance: `gateway.mode=local` startup guard + auth-required-before-bind.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — token/password mode resolution; relevance: `--auth`/`--token`/`--password` handling.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — restart/startup orchestration; relevance: `--safe` restart, channel settling at start.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env flags; relevance: `OPENCLAW_GATEWAY_STARTUP_TRACE`/`RESTART_TRACE`/`OPENCLAW_WRAPPER`.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — shutdown sequencing; relevance: SIGINT/SIGTERM stop, active-work drain on `--safe`.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — in-process respawn; relevance: SIGUSR1 in-process restart path.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — macOS launchd plist; relevance: `gateway install` managed-service on macOS.
- [snippet_openclaw_daemon_launchd_restart_handoff](../../code_snippets/snippet_openclaw_daemon_launchd_restart_handoff.md) — supervisor restart handoff; relevance: managed-service restart vs in-process restart.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — Linux systemd unit; relevance: `gateway install` on Linux, `EnvironmentFile` parsing.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup writes config; relevance: `setup` writes `gateway.mode=local`.
- [snippet_hermes_agent_cli_gateway_lifecycle](../../code_snippets/snippet_hermes_agent_cli_gateway_lifecycle.md) — analogous install/start/stop/restart; relevance: sibling agent's managed-service lifecycle.

### oc_cli_gateway_query (9t · 12s · 11d)

**Terms** (9)
- [term_websocket](../../term_dictionary/term_websocket.md) — WS transport; relevance: all query commands use WebSocket RPC.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — JSON-RPC method/params; relevance: `gateway call <method> --params` is the low-level RPC helper.
- [term_health_check](../../term_dictionary/term_health_check.md) — liveness/readiness/probe; relevance: `gateway health`/`status`/`probe` read-probe classification.
- [term_authentication](../../term_dictionary/term_authentication.md) — auth-capability; relevance: probe reports read-only/write/admin capability, SecretRef resolution.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway platform; relevance: querying an OpenClaw Gateway.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — non-mutating reads; relevance: diagnostic probes reuse cached device auth, do not create pairing state.
- [term_sse](../../term_dictionary/term_sse.md) — server push hints; relevance: discovery TXT hints / streamed status differ from one-shot reads (transport contrast).
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — proxy/tunnel fronting; relevance: SSH port-forward `probe --ssh` reaches loopback-bound remote Gateways.

**Docs** (11: 6 existing + 5 sibling)
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — Pi RPC envelope; relevance: analog of OpenClaw WS RPC request/response shape.
- [pi_rpc_commands](../pi/pi_rpc_commands.md) — Pi RPC command catalog; relevance: analog of `gateway call <method>` method surface.
- [pi_rpc_events](../pi/pi_rpc_events.md) — Pi RPC streamed events; relevance: `--expect-final` streamed intermediate events.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — gateway/proxy URL config; relevance: `--url` remote-gateway targeting analog.
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — config diagnostics; relevance: analog of `gateway status --deep` config validation.
- [cc_agent_view_monitor](../claude_code/cc_agent_view_monitor.md) — live agent/service monitor; relevance: analog of probe/status connectivity view.
- [oc_cli_gateway_run](oc_cli_gateway_run.md) — (planned, this series) run/restart/install; relevance: the process being queried.
- [oc_cli_health](oc_cli_health.md) — (planned, this series) health snapshot; relevance: `gateway health` overlaps the standalone `openclaw health`.
- [oc_cli_logs](oc_cli_logs.md) — (planned, this series) RPC log tail; relevance: `gateway call logs.tail` is the same RPC.
- [oc_cli_mcp_registry](oc_cli_mcp_registry.md) — (planned, this series) MCP registry probe; relevance: `mcp probe` mirrors `gateway probe` reachability proof.
- [oc_cli_memory](oc_cli_memory.md) — (planned, this series) memory CLI; relevance: `memory status` needs gateway connectivity like the query commands.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: status/probe/discover/call RPC handlers.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — auth/scope classification; relevance: probe capability (read/write/admin) + scope-limited classification.

**Snippets** (12)
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: shape behind `gateway call --json`.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — RPC errors + version; relevance: `status.runtimeVersion`, `gateway.version`, error exit codes.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC method groups; relevance: `health`/`status`/`config.get`/`system-presence` read-scope RPCs.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth helpers; relevance: probe SecretRef resolution, `--token`/`--password` for `--url`.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method gating; relevance: `gateway call` capability/scope gating.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential resolution; relevance: `--url` requires explicit creds, no config fallback.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connect; relevance: connect-only vs read-probe reachability.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: `ssh_tunnel_failed`/`auth_secretref_unresolved`/`probe_scope_limited` warnings.
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — usage-cost summary; relevance: `gateway usage-cost --days`.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — status/latency cache; relevance: `gateway status`/`stability` recorder output.
- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — mDNS discovery; relevance: `gateway discover` Bonjour `_openclaw-gw._tcp` beacons + TXT hints.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — analogous status/health probe; relevance: sibling agent's gateway status/health command.

### oc_cli_health (8t · 10s · 10d)

**Terms** (8)
- [term_health_check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: the entire command is a health snapshot fetch.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway platform; relevance: snapshot comes from the running OpenClaw Gateway.
- [term_websocket](../../term_dictionary/term_websocket.md) — WS RPC; relevance: snapshot fetched over the Gateway WebSocket RPC.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — machine output; relevance: `--json` machine-readable health payload.
- [term_authentication](../../term_dictionary/term_authentication.md) — gateway connect; relevance: a live probe (`--verbose`) requires connecting to the Gateway.
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — cache-then-refresh; relevance: returns a fresh cached snapshot then refreshes in the background.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — read-only; relevance: a non-mutating diagnostic read.
- [term_context_window](../../term_dictionary/term_context_window.md) — per-agent state; relevance: output expands per-agent session stores when multiple agents configured.

**Docs** (10: 5 existing + 5 sibling)
- [cc_agent_view_monitor](../claude_code/cc_agent_view_monitor.md) — live monitor view; relevance: analog of a quick health/status snapshot.
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — config diagnostics; relevance: analog of a fast health check.
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi CLI command surface; relevance: sibling tool's status/health command.
- [bedrock_monitoring_runtime_metrics](../aws_bedrock/bedrock_monitoring_runtime_metrics.md) — runtime health metrics; relevance: managed-runtime health/metrics analog.
- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — telemetry/health signals; relevance: what a health snapshot's diagnostics may report.
- [oc_cli_gateway_query](oc_cli_gateway_query.md) — (planned, this series) `gateway health`; relevance: `openclaw health` overlaps `gateway health`.
- [oc_cli_gateway_run](oc_cli_gateway_run.md) — (planned, this series) run the Gateway; relevance: the process being health-checked.
- [oc_cli_logs](oc_cli_logs.md) — (planned, this series) log tail; relevance: complementary diagnostic on the same Gateway.
- [oc_cli_mcp_registry](oc_cli_mcp_registry.md) — (planned, this series) `mcp doctor`; relevance: another diagnostic/readiness check.
- [oc_cli_memory](oc_cli_memory.md) — (planned, this series) `memory status`; relevance: subsystem-level health analog.

**Repos** (2)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: health-snapshot RPC + `eventLoop` diagnostic block.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent runtime; relevance: per-agent session-store expansion in `--verbose`.

**Snippets** (10)
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — analogous health snapshot; relevance: sibling agent's health command.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: transport of the health RPC.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: the `health` read-scope RPC method.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — cached status; relevance: cached-then-refresh snapshot behavior.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — `/healthz` `/readyz` endpoints; relevance: HTTP liveness/readiness served alongside the snapshot.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth for live probe; relevance: `--verbose` live probe needs gateway auth.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connect/timeout; relevance: `--timeout` connection timeout.
- [snippet_openclaw_gateway_channels_runtime_snapshot](../../code_snippets/snippet_openclaw_gateway_channels_runtime_snapshot.md) — runtime snapshot; relevance: channels/accounts in the per-agent health view.
- [snippet_openclaw_gateway_session_utils_subagent_liveness](../../code_snippets/snippet_openclaw_gateway_session_utils_subagent_liveness.md) — liveness tracking; relevance: per-agent/subagent liveness in the snapshot.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect errors; relevance: `--timeout`/connect failures surfaced by `openclaw health`.

### oc_cli_hooks (8t · 11s · 10d)

**Terms** (8)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the platform; relevance: `openclaw hooks` manages OpenClaw agent hooks.
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — event handlers; relevance: hooks fire on `command:new`/`command:reset`/`gateway:startup`/`agent:bootstrap` events.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — agent automations; relevance: hooks are agent-loop automations.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — config writes; relevance: enable/disable write `hooks.internal.entries.<name>.enabled` once.
- [term_webhook](../../term_dictionary/term_webhook.md) — event-callback pattern; relevance: hooks are the local event-handler analog of webhooks.
- [term_skills](../../term_dictionary/term_skills.md) — installable packs; relevance: hook packs install via the unified `openclaw plugins` installer.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled automation; relevance: hooks sit beside cron in OpenClaw's automation surface (command-logger audit, boot-md).
- [term_sandbox](../../term_dictionary/term_sandbox.md) — install safety; relevance: hook-pack npm installs run project-local with `--ignore-scripts`.

**Docs** (10: 5 existing + 5 sibling)
- [cc_hooks_overview](../claude_code/cc_hooks_overview.md) — Claude Code hooks model; relevance: directly analogous agent-hook lifecycle.
- [cc_hook_session_lifecycle_events](../claude_code/cc_hook_session_lifecycle_events.md) — session lifecycle hook events; relevance: analog of `command:new`/`command:reset`/`gateway:startup`.
- [cc_hook_configuration_settings](../claude_code/cc_hook_configuration_settings.md) — hook config schema; relevance: analog of `hooks.internal.entries.*` config.
- [cc_sdk_hooks_overview](../claude_code/cc_sdk_hooks_overview.md) — SDK hooks overview; relevance: programmatic hook handler analog.
- [pi_extensions_events_lifecycle](../pi/pi_extensions_events_lifecycle.md) — Pi lifecycle event extensions; relevance: sibling tool's event-driven extension model.
- [oc_cli_memory](oc_cli_memory.md) — (planned, this series) memory CLI; relevance: the `session-memory` bundled hook writes to memory.
- [oc_cli_gateway_run](oc_cli_gateway_run.md) — (planned, this series) run/restart; relevance: restart the Gateway so enabled hooks reload.
- [oc_cli_mcp_serve](oc_cli_mcp_serve.md) — (planned, this series) plugins/installer surface; relevance: hook packs share the `plugins install` installer.
- [oc_cli_health](oc_cli_health.md) — (planned, this series) health snapshot; relevance: confirm hooks loaded after restart.
- [oc_cli_logs](oc_cli_logs.md) — (planned, this series) log tail; relevance: `command-logger` hook writes an audit log.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: loads internal hook handlers at startup.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugins/extensions; relevance: plugin-managed hooks delegate to the owning plugin.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory engine; relevance: `session-memory` hook target.

**Snippets** (11)
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — hook dispatch handler; relevance: how the Gateway invokes hook handlers on events.
- [snippet_openclaw_gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — hook config payload; relevance: `hooks.internal.entries`/`installs`/`load.extraDirs` schema.
- [snippet_openclaw_gateway_session_reset_helpers_hooks](../../code_snippets/snippet_openclaw_gateway_session_reset_helpers_hooks.md) — reset hooks; relevance: `command:reset` fires `session-memory`.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: `/new`/`/reset` events that hooks subscribe to.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: plugin-managed hooks enable/disable with the plugin.
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — startup ordering; relevance: `boot-md` runs `gateway:startup` after channels start.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron/service notifications; relevance: command-logger audit + automation lifecycle adjacency.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — agent bootstrap; relevance: `bootstrap-extra-files` injects files during `agent:bootstrap`.
- [snippet_openclaw_security_skill_scanner](../../code_snippets/snippet_openclaw_security_skill_scanner.md) — install scanning; relevance: hook-pack/plugin install safety (`--ignore-scripts`, integrity hash).
- [snippet_openclaw_memory_root_files](../../code_snippets/snippet_openclaw_memory_root_files.md) — memory file outputs; relevance: `session-memory` writes `memory/YYYY-MM-DD-HHMM.md`.
- [snippet_hermes_agent_gw_hooks](../../code_snippets/snippet_hermes_agent_gw_hooks.md) — analogous gateway hooks; relevance: sibling agent's hook system.

### oc_cli_infer (10t · 12s · 12d)

**Terms** (10)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the platform; relevance: `openclaw infer` is OpenClaw's headless capability surface.
- [term_llm](../../term_dictionary/term_llm.md) — language model; relevance: `model run` provider-backed text inference.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — configured provider; relevance: uses providers/models already configured in OpenClaw.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — model registry; relevance: `model run --model <provider/model>` resolves catalog rows.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — image/audio/video; relevance: image/audio/video describe + `model run --file` image attach.
- [term_chain_of_thought](../../term_dictionary/term_chain_of_thought.md) — reasoning level; relevance: `model run --thinking <level>`.
- [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — TTS; relevance: `tts convert`/`voices`/`set-provider`.
- [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — transcription; relevance: `audio transcribe`.
- [term_embedding](../../term_dictionary/term_embedding.md) — vector embeddings; relevance: `embedding create`.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — external backends; relevance: openai/google/cerebras/groq/mistral/ollama provider backends.

**Docs** (12: 7 existing + 5 sibling)
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi headless CLI; relevance: sibling tool's one-shot inference surface.
- [pi_json_mode](../pi/pi_json_mode.md) — Pi JSON output; relevance: analog of infer's stable `--json` envelope.
- [pi_sdk_run_modes](../pi/pi_sdk_run_modes.md) — Pi one-shot vs session run modes; relevance: infer local lean one-shot vs `--gateway` routing.
- [cc_headless_examples](../claude_code/cc_headless_examples.md) — Claude Code headless examples; relevance: analog of scripted headless inference.
- [cc_amazon_bedrock_model_config](../claude_code/cc_amazon_bedrock_model_config.md) — provider/model config; relevance: `--model provider/model` selection analog.
- [bedrock_invoke_api_text](../aws_bedrock/bedrock_invoke_api_text.md) — text inference API; relevance: analog of `model run` text completion.
- [bedrock_invoke_api_multimodal](../aws_bedrock/bedrock_invoke_api_multimodal.md) — multimodal invoke; relevance: analog of `model run --file` image attach / `image describe`.
- [oc_cli_gateway_query](oc_cli_gateway_query.md) — (planned, this series) `--gateway` routing; relevance: `model run --gateway` exercises Gateway routing.
- [oc_cli_memory](oc_cli_memory.md) — (planned, this series) memory CLI; relevance: `embedding create` powers memory indexing.
- [oc_cli_mcp_serve](oc_cli_mcp_serve.md) — (planned, this series) one-shot retire bundled MCP; relevance: `infer model run` retires bundled MCP runtimes at run end.
- [oc_cli_gateway_run](oc_cli_gateway_run.md) — (planned, this series) run the Gateway; relevance: `--gateway` requires a running Gateway + trusted operator credential.
- [oc_cli_health](oc_cli_health.md) — (planned, this series) provider health; relevance: `infer ... providers --json` is a provider readiness check.

**Repos** (3)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — capability runtime; relevance: shared capability runtime + default-agent resolution.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugins; relevance: provider/model activation behind infer.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway routing; relevance: `--gateway` routed inference path.

**Snippets** (12)
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: `model run --model`/`model list`/`inspect` resolution.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog discovery; relevance: `models list --all` static catalog rows.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest; relevance: provider/model capability flags (image-capable etc).
- [snippet_openclaw_cli_command_catalog](../../code_snippets/snippet_openclaw_cli_command_catalog.md) — CLI command tree; relevance: the `infer` subcommand tree (model/image/audio/tts/video/web/embedding).
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: `openai/<model>` path, `gpt-image`, whisper, moderation hints.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: `anthropic/claude-sonnet` smoke probes.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama; relevance: `ollama/qwen2.5vl` vision, `OLLAMA_API_KEY` placeholder.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — TTS provider; relevance: `tts convert` synthesis backend.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — STT provider; relevance: `audio transcribe` backend.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs; relevance: `embedding create` vector generation.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image validate; relevance: `image generate`/`edit` output handling + MIME detection.
- [snippet_hermes_agent_cli_oneshot](../../code_snippets/snippet_hermes_agent_cli_oneshot.md) — analogous one-shot run; relevance: sibling agent's headless one-shot inference.

### oc_cli_mcp_serve (9t · 12s · 11d)

**Terms** (9)
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: `serve` runs OpenClaw as an MCP server.
- [term_mcp_gateway](../../term_dictionary/term_mcp_gateway.md) — MCP gateway bridge; relevance: serve bridges Gateway channel conversations to an MCP client.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the platform; relevance: OpenClaw acting as the MCP server.
- [term_websocket](../../term_dictionary/term_websocket.md) — WS connect; relevance: the bridge connects to the Gateway over WebSocket.
- [term_claude_code](../../term_dictionary/term_claude_code.md) — MCP client; relevance: Claude Code is a target client + `--claude-channel-mode`.
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — event queue; relevance: in-memory live event queue, `events_poll`/`events_wait`.
- [term_authentication](../../term_dictionary/term_authentication.md) — bridge auth/trust; relevance: token/password bridge auth + trust boundary.
- [term_acp_agent_client_protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — ACP harness hosting; relevance: contrast `serve` (server) with `openclaw acp` (hosting runtime).
- [term_idempotency](../../term_dictionary/term_idempotency.md) — clean teardown; relevance: bridge exits + queue disposed on disconnect; runtimes retired per run.

**Docs** (11: 6 existing + 5 sibling)
- [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — Claude Code MCP overview; relevance: directly analogous MCP integration.
- [cc_mcp_quickstart](../claude_code/cc_mcp_quickstart.md) — MCP server quickstart; relevance: client config (`mcpServers`) analog.
- [cc_sdk_connect_mcp_servers](../claude_code/cc_sdk_connect_mcp_servers.md) — SDK MCP connect; relevance: stdio MCP server spawn analog.
- [pi_extensions_events_agent_tools](../pi/pi_extensions_events_agent_tools.md) — Pi agent-tool events; relevance: analog of bridge tool surface + event model.
- [cc_sdk_mcp_auth_and_errors](../claude_code/cc_sdk_mcp_auth_and_errors.md) — MCP auth/errors; relevance: bridge trust boundary + auth.
- [oc_cli_mcp_registry](oc_cli_mcp_registry.md) — (planned, this series) MCP client registry; relevance: the sibling outbound-server half of `openclaw mcp`.
- [oc_cli_mcp_transports](oc_cli_mcp_transports.md) — (planned, this series) transport schemas; relevance: bridge stdio transport + JSON shapes.
- [oc_cli_gateway_run](oc_cli_gateway_run.md) — (planned, this series) run the Gateway; relevance: serve needs a routed local/remote Gateway.
- [oc_cli_gateway_query](oc_cli_gateway_query.md) — (planned, this series) `--url` targeting; relevance: serve `--url`/`--token-file` remote-gateway connect.
- [oc_cli_infer](oc_cli_infer.md) — (planned, this series) one-shot MCP retire; relevance: one-shot agent entry points retire bundled MCP runtimes.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: session route metadata the bridge exposes.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel backends; relevance: channel-backed conversations the bridge surfaces.

**Snippets** (12)
- [snippet_hermes_agent_mcp_serve_hermes_as_server](../../code_snippets/snippet_hermes_agent_mcp_serve_hermes_as_server.md) — agent-as-MCP-server; relevance: directly analogous `serve` implementation.
- [snippet_hermes_agent_mcp_serve_tool_surface](../../code_snippets/snippet_hermes_agent_mcp_serve_tool_surface.md) — exposed MCP tools; relevance: analog of `conversations_list`/`messages_read`/`events_poll`/`messages_send`/`permissions_*`.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — MCP loopback bridge; relevance: bridge-to-Gateway loopback connect.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: WS RPC the bridge uses to read/send.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation routing; relevance: route metadata (`channel`/recipient/`accountId`/`threadId`) for `conversations_list`.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — send handler; relevance: `messages_send` replies through the stored route.
- [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — approval manager; relevance: `permissions_list_open`/`permissions_respond` exec/plugin approvals.
- [snippet_openclaw_gateway_session_fs_transcript_candidate_scan](../../code_snippets/snippet_openclaw_gateway_session_fs_transcript_candidate_scan.md) — transcript read; relevance: `messages_read` recent transcript history.
- [snippet_hermes_agent_tools_mcp_notifications](../../code_snippets/snippet_hermes_agent_tools_mcp_notifications.md) — MCP notifications; relevance: `notifications/claude/channel` push model.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle; relevance: deleting/resetting a session disposes its MCP clients.

### oc_cli_mcp_registry (9t · 12s · 11d)

**Terms** (9)
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the servers being registered are MCP servers.
- [term_tool_registry](../../term_dictionary/term_tool_registry.md) — tool catalog/filters; relevance: `toolFilter.include`/`exclude`, `tools` subcommand, generated utility tools.
- [term_oauth](../../term_dictionary/term_oauth.md) — OAuth flow; relevance: `login`/`logout`, `auth: "oauth"` HTTP server flow.
- [term_authentication](../../term_dictionary/term_authentication.md) — auth/static checks; relevance: `doctor` static checks for auth/credential problems.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the platform; relevance: OpenClaw-as-MCP-client-registry.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — server scoping; relevance: filesystem/CUA servers scoped via narrow tool filters + OS prompts.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — config-only ops; relevance: `list`/`show`/`status`/`set`/`unset` read/write config without connecting.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: registered MCP tools become callable agent tools.

**Docs** (11: 6 existing + 5 sibling)
- [cc_mcp_server_management](../claude_code/cc_mcp_server_management.md) — MCP server management; relevance: directly analogous add/list/remove/configure server registry.
- [cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md) — managed MCP config; relevance: admin-managed MCP server definitions analog.
- [cc_sdk_connect_mcp_servers](../claude_code/cc_sdk_connect_mcp_servers.md) — SDK MCP servers; relevance: programmatic saved-server consumption.
- [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — MCP OAuth; relevance: `login`/`logout` OAuth credential store analog.
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — Pi custom tools; relevance: registering external tool servers analog.
- [oc_cli_mcp_serve](oc_cli_mcp_serve.md) — (planned, this series) OpenClaw-as-server; relevance: the inbound half of `openclaw mcp`.
- [oc_cli_mcp_transports](oc_cli_mcp_transports.md) — (planned, this series) transport schemas; relevance: stdio/SSE/streamable-http fields the registry stores.
- [oc_cli_gateway_query](oc_cli_gateway_query.md) — (planned, this series) `probe`; relevance: `mcp probe`/`doctor --probe` mirror `gateway probe`.
- [oc_cli_infer](oc_cli_infer.md) — (planned, this series) embedded runtime; relevance: saved servers project into eligible inference/agent runtimes.
- [oc_cli_health](oc_cli_health.md) — (planned, this series) doctor/readiness; relevance: `mcp doctor` is a subsystem readiness check.

**Repos** (3)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: embedded runtime consumes the registry, `tools.deny: ["bundle-mcp"]`.
- [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — toolset registry; relevance: analogous outbound MCP toolset registry.

**Snippets** (12)
- [snippet_hermes_agent_cli_mcp_config](../../code_snippets/snippet_hermes_agent_cli_mcp_config.md) — MCP server config CLI; relevance: directly analogous add/set/configure registry.
- [snippet_hermes_agent_tools_mcp_call](../../code_snippets/snippet_hermes_agent_tools_mcp_call.md) — MCP tool call; relevance: registered tools invoked at agent turn.
- [snippet_hermes_agent_tools_mcp_client](../../code_snippets/snippet_hermes_agent_tools_mcp_client.md) — MCP client; relevance: `probe` opens a live MCP client session.
- [snippet_hermes_agent_tools_mcp_lifecycle](../../code_snippets/snippet_hermes_agent_tools_mcp_lifecycle.md) — MCP lifecycle/reaping; relevance: `reload` disposes cached runtimes, idle TTL reaping.
- [snippet_hermes_agent_tools_mcp_oauth](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth.md) — MCP OAuth; relevance: `login`/`logout` OAuth credential flow.
- [snippet_hermes_agent_tools_mcp_oauth_manager](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth_manager.md) — OAuth credential store; relevance: stored OAuth tokens/verifier state.
- [snippet_hermes_agent_tools_mcp_retry](../../code_snippets/snippet_hermes_agent_tools_mcp_retry.md) — MCP retry/pause; relevance: repeated MCP failures briefly pause that server.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — HTTP MCP bridge; relevance: registry HTTP server connect for `probe`.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway methods; relevance: registry-config RPC + runtime adapter normalization.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: MCP tools surface in `coding`/`messaging` tool profiles.
- [snippet_hermes_agent_skills_mcp_native](../../code_snippets/snippet_hermes_agent_skills_mcp_native.md) — native MCP integration; relevance: server recipes (filesystem/memory/HTTP/CUA) analog.

### oc_cli_mcp_transports (8t · 10s · 10d) — model

**Terms** (8)
- [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the transport contract being modeled.
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — JSON-RPC; relevance: MCP rides JSON-RPC over each transport; `status`/`doctor`/`probe --json` shapes.
- [term_sse](../../term_dictionary/term_sse.md) — Server-Sent Events; relevance: the SSE/HTTP transport field schema.
- [term_oauth](../../term_dictionary/term_oauth.md) — OAuth workflow; relevance: `auth: "oauth"` HTTP-server login flow + token storage.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — stored credential; relevance: stored OAuth tokens/`authStatus` in the status shape.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — HTTP streaming front; relevance: streamable-http fronts remote MCP servers.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — startup-env safety; relevance: stdio env safety filter blocks `NODE_OPTIONS`/`PYTHONSTARTUP`/`LD_PRELOAD`-class keys.
- [term_authentication](../../term_dictionary/term_authentication.md) — mTLS/headers; relevance: `clientCert`/`clientKey` mTLS, static `headers`, `sslVerify`.

**Docs** (10: 6 existing + 4 sibling)
- [cc_mcp_transports](../claude_code/cc_mcp_transports.md) — MCP transport types; relevance: directly analogous stdio/SSE/HTTP transport contract.
- [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — MCP auth; relevance: OAuth + header/TLS auth field schemas.
- [cc_sdk_mcp_auth_and_errors](../claude_code/cc_sdk_mcp_auth_and_errors.md) — MCP auth/errors; relevance: OAuth-not-authorized doctor error analog.
- [pi_rpc_protocol](../pi/pi_rpc_protocol.md) — RPC protocol envelope; relevance: JSON-RPC-over-transport model analog.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — custom server config; relevance: transport/auth config field schema analog.
- [pi_security_model](../pi/pi_security_model.md) — env/secret safety; relevance: analog of the stdio env startup-safety filter + header redaction.
- [oc_cli_mcp_registry](oc_cli_mcp_registry.md) — (planned, this series) registry commands; relevance: the registry that validates/stores these transport fields.
- [oc_cli_mcp_serve](oc_cli_mcp_serve.md) — (planned, this series) stdio serve; relevance: serve uses the stdio transport modeled here.
- [oc_cli_gateway_query](oc_cli_gateway_query.md) — (planned, this series) `--json` shapes; relevance: shared machine-output JSON-shape convention.
- [oc_cli_infer](oc_cli_infer.md) — (planned, this series) `--json` envelope; relevance: parallel stable JSON output contract.

**Repos** (2)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: transport normalization for the embedded runtime (`type:"http"` → `transport`).
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security filters; relevance: stdio env safety filter, sensitive-value redaction.

**Snippets** (10)
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — HTTP MCP transport; relevance: SSE/streamable-http connect path.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: JSON-RPC shape underlying every transport.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — schema groups; relevance: `status`/`doctor`/`probe` JSON-shape grouping analog.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content/env safety; relevance: stdio env safety filter rejecting interpreter-startup keys.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client TLS/mTLS; relevance: `clientCert`/`clientKey`/`sslVerify` fields.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential redaction; relevance: redacted userinfo/`headers` in logs and status.
- [snippet_hermes_agent_tools_mcp_oauth](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth.md) — OAuth workflow; relevance: `auth: "oauth"` login/code/logout steps.
- [snippet_hermes_agent_tools_mcp_oauth_manager](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth_manager.md) — OAuth state; relevance: `authStatus.hasTokens`/`hasCodeVerifier` fields in `status --json`.
- [snippet_hermes_agent_tools_mcp_client](../../code_snippets/snippet_hermes_agent_tools_mcp_client.md) — MCP client transports; relevance: which transport shapes a client supports at execution.
- [snippet_hermes_agent_cli_mcp_config](../../code_snippets/snippet_hermes_agent_cli_mcp_config.md) — MCP config shape; relevance: example config-shape JSON for stdio/HTTP/streamable-http.

### oc_cli_memory (9t · 11s · 11d)

**Terms** (9 — `term_semantic_search` MISSING, replaced by rag/vector_db/embedding)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the platform; relevance: `openclaw memory` semantic-memory CLI.
- [term_rag](../../term_dictionary/term_rag.md) — retrieval-augmented memory; relevance: index + search semantic memory (the standalone semantic-search concept lives here, not in a missing term).
- [term_embedding](../../term_dictionary/term_embedding.md) — vector embeddings; relevance: embedding-provider readiness, `memory index` builds the vector index.
- [term_vector_database](../../term_dictionary/term_vector_database.md) — vector store; relevance: `status --deep` probes local vector-store + semantic-vector-search readiness.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled sweep; relevance: managed dreaming cron `dreaming.frequency = 0 3 * * *`.
- [term_context_engine](../../term_dictionary/term_context_engine.md) — agent context feed; relevance: promoted `MEMORY.md` facts feed agent context.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — bundled plugin; relevance: `memory-core` bundled plugin + embedding provider selection.
- [term_skills](../../term_dictionary/term_skills.md) — plugin slot; relevance: `plugins.slots.memory` selects `memory-core`.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — re-runnable; relevance: `status --fix` repairs stale recall locks; promote re-reads live note before writing.

**Docs** (11: 6 existing + 5 sibling)
- [cc_memory_overview](../claude_code/cc_memory_overview.md) — Claude Code memory; relevance: directly analogous agent-memory model.
- [cc_auto_memory](../claude_code/cc_auto_memory.md) — automatic memory promotion; relevance: analog of dreaming promotion into `MEMORY.md`.
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — memory/context budgeting; relevance: promoted-snippet token bounding (`maxPromotedSnippetTokens`).
- [bedrock_kb_how_it_works](../aws_bedrock/bedrock_kb_how_it_works.md) — KB embed+index+retrieve; relevance: analog of embed/index/semantic-search pipeline.
- [bedrock_kb_overview](../aws_bedrock/bedrock_kb_overview.md) — knowledge base overview; relevance: vector-store-backed retrieval analog.
- [oc_cli_hooks](oc_cli_hooks.md) — (planned, this series) `session-memory` hook; relevance: the hook that seeds short-term memory.
- [oc_cli_infer](oc_cli_infer.md) — (planned, this series) `embedding create`; relevance: embeddings power memory indexing/search.
- [oc_cli_gateway_run](oc_cli_gateway_run.md) — (planned, this series) `secrets.resolve`; relevance: memory needs a running Gateway for SecretRef embedding keys.
- [oc_cli_gateway_query](oc_cli_gateway_query.md) — (planned, this series) gateway version skew; relevance: command needs a gateway supporting `secrets.resolve`.
- [oc_cli_health](oc_cli_health.md) — (planned, this series) `memory status`; relevance: subsystem readiness check overlap.

**Repos** (3)
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory-core engine; relevance: index/search/promote/dreaming implementation.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent runtime; relevance: `--agent` per-agent memory scoping.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: `secrets.resolve` snapshot + dreaming cron management.

**Snippets** (11)
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine; relevance: `index`/`search`/`status` core.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime; relevance: per-agent runtime probing/indexing.
- [snippet_openclaw_memory_dreaming_constants](../../code_snippets/snippet_openclaw_memory_dreaming_constants.md) — dreaming thresholds; relevance: `minScore=0.8`, `minRecallCount=3`, `recencyHalfLifeDays=14`.
- [snippet_openclaw_memory_dreaming_resolvers](../../code_snippets/snippet_openclaw_memory_dreaming_resolvers.md) — dreaming phase resolvers; relevance: light/REM/deep phase execution order.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs; relevance: embedding-provider readiness for `index`.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory events; relevance: recall/promotion signals (`frequency`/`relevance`/`query diversity`).
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — host embeddings; relevance: vector index build behind `memory index --force`.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — agent memory search; relevance: `memory search --query` retrieval path.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — dreaming preview/doctor; relevance: `rem-harness` preview + `Dreaming status: blocked` diagnosis.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — dreaming cron repair; relevance: managed dreaming cron `dreaming.frequency` sweep.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — secrets resolve; relevance: `secrets.resolve` for SecretRef embedding API keys.

### oc_cli_logs (8t · 10s · 10d)

**Terms** (8)
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the platform; relevance: `openclaw logs` tails the OpenClaw Gateway logs.
- [term_websocket](../../term_dictionary/term_websocket.md) — WS RPC; relevance: logs are tailed over the Gateway WebSocket RPC (`logs.tail`).
- [term_json_rpc](../../term_dictionary/term_json_rpc.md) — RPC + JSON; relevance: `logs.tail` RPC, `--json` line-delimited events.
- [term_authentication](../../term_dictionary/term_authentication.md) — explicit creds; relevance: `--url` requires explicit `--token`, no config fallback.
- [term_health_check](../../term_dictionary/term_health_check.md) — diagnostic; relevance: log tail is a primary remote diagnostic.
- [term_event_driven_architecture](../../term_dictionary/term_event_driven_architecture.md) — stream + reconnect; relevance: `--follow` stream, reconnect-with-exponential-backoff.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — safe fallback; relevance: implicit-local-loopback falls back to the file log automatically.
- [term_cron](../../term_dictionary/term_cron.md) — service journal; relevance: on Linux `--follow` reads the user-systemd Gateway journal by PID.

**Docs** (10: 5 existing + 5 sibling)
- [pi_cli_reference](../pi/pi_cli_reference.md) — Pi CLI surface; relevance: sibling tool's logs command.
- [pi_rpc_events](../pi/pi_rpc_events.md) — streamed RPC events; relevance: `--follow` streamed `{"type":"notice"}` records.
- [cc_data_usage_and_telemetry](../claude_code/cc_data_usage_and_telemetry.md) — telemetry/logging; relevance: analogous log/telemetry surface.
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — config/log diagnostics; relevance: tailing logs to debug a running agent.
- [cc_monitoring_opentelemetry_setup](../claude_code/cc_monitoring_opentelemetry_setup.md) — observability setup; relevance: structured-log/observability analog.
- [oc_cli_gateway_query](oc_cli_gateway_query.md) — (planned, this series) `gateway call logs.tail`; relevance: the same RPC the low-level helper exposes.
- [oc_cli_health](oc_cli_health.md) — (planned, this series) health snapshot; relevance: complementary diagnostic on the same Gateway.
- [oc_cli_gateway_run](oc_cli_gateway_run.md) — (planned, this series) run/profiling; relevance: `--cli-backend-logs`/`--ws-log` shape what logs contain.
- [oc_cli_mcp_registry](oc_cli_mcp_registry.md) — (planned, this series) doctor diagnostics; relevance: another remote-diagnostic command.
- [oc_cli_memory](oc_cli_memory.md) — (planned, this series) `status --verbose`; relevance: verbose-log diagnostic pattern.

**Repos** (2)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway server; relevance: `logs.tail` RPC + file-log fallback.

**Snippets** (10)
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC envelope; relevance: `logs.tail` RPC request/response shape.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: the `logs.tail` read-scope method.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential resolution; relevance: `--url` requires explicit `--token`, no fallback.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect errors; relevance: non-recoverable auth/config errors exit immediately.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client reconnect; relevance: `--follow` reconnect-with-backoff (up to 8 retries, 30s cap).
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — WS connect/timeout; relevance: `--timeout`, WebSocket close/drop handling.
- [snippet_openclaw_daemon_systemd_unit_render_parse](../../code_snippets/snippet_openclaw_daemon_systemd_unit_render_parse.md) — systemd unit; relevance: Linux user-systemd journal-by-PID log source.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env/logging; relevance: file-log path + log styling env.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — server config/logging; relevance: configured-file fallback log path resolution.
- [snippet_hermes_agent_cli_logs](../../code_snippets/snippet_hermes_agent_cli_logs.md) — analogous logs command; relevance: sibling agent's `logs` tail/follow.

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| Gateway / Gateway service / bind mode / safe-restart deferral | OpenClaw CLI vocab → digested in oc_cli_gateway_run / oc_cli_gateway_query; link **term_websocket**, **term_openclaw**. No new term note. |
| `openclaw mcp serve` bridge / bridge tools / event queue | OpenClaw vocab → oc_cli_mcp_serve; link **term_mcp**, **term_mcp_gateway**. No new term note. |
| stdio / SSE / streamable-http transport, env safety filter | OpenClaw vocab → oc_cli_mcp_transports; link **term_mcp**, **term_sse**, **term_sandbox**. No new term note. |
| infer capability tree / `model run` / image/audio/tts/video/web/embedding | OpenClaw vocab → oc_cli_infer; link **term_llm**, **term_multimodal**, **term_embedding**, **term_text_to_speech**, **term_speech_to_text**. No new term note. |
| agent hooks / hook packs / bundled hooks (session-memory etc.) | OpenClaw vocab → oc_cli_hooks; link **term_event_driven_architecture**, **term_skills**. No new term note. |
| Dreaming (light/REM/deep) / promotion signals / `MEMORY.md` | OpenClaw vocab → oc_cli_memory (concept deep-dive lives in co02 `/concepts/dreaming`); link **term_rag**, **term_cron**. No new term note. |
| Bonjour / mDNS / wide-area DNS-SD / beacon | OpenClaw vocab → oc_cli_gateway_query (runbook lives in gw0x); link **term_openclaw**, **term_websocket**. No new term note. |
| **semantic search** (memory search) | **Candidate gap**: `term_semantic_search` is MISSING in DB; the memory note links existing **term_rag** + **term_vector_database** + **term_embedding** instead (no inline definition). NOT promoted by cl04 — semantic search is cross-cutting (retrieval/RAG corpus owns it); flag for a future term capture if a doc-page home appears. Best-fit glossary if ever captured: `acronym_glossary_ai_ml.md`. |
| **liveness/readiness probe**, **DNS-SD**, **mDNS**, **systemd/launchd**, **OpenTelemetry/Prometheus**, **SecretRef**, **dreaming** | All MISSING as term notes but each is documented inline as OpenClaw config/CLI behavior in its home `oc_*` note (no standalone term note needed); link the nearest existing term (term_health_check, term_websocket, term_cron, term_openclaw). No new captures. |

**Expected new `term_dictionary` captures: 0** (per master Undigested-Terms design — OpenClaw vocab → `oc_*` doc notes, existing terms linked).

## Term-Note Authoring Requirements

**N/A (0 new terms)** — cl04 authors zero `term_dictionary` notes. Inherited from master. If augment Step 2d surfaces a genuinely cross-cutting, vault-reusable term with no doc-page home AND no existing note (none expected; `term_semantic_search` is owned by the retrieval corpus, not this sub-plan), it would be captured via `/tessellum-capture-term-note` + added to `acronym_glossary_ai_ml.md` per master W5.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (10 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` (YAML field order, `## Overview`/`## Related Notes`/`## References`, bold `**Source**`/`**Last Updated**`/`**Status**` footer) |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/cli/<page>.md`; no invented flags/commands; commands/config reproduced verbatim |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks, one `building_block`; every mapped H2/H3 covered |
| G5 | Ghost-reference | every cited note_id resolves in DB; redirect/drop ghosts (e.g. term_semantic_search) |
| G6 | Broken-link fix | `/tessellum-fix-broken-links`; 0 broken links post-reindex |
| G7 | Discoverability | each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo_openclaw* / term_* inlinks) |
| G8 | In-degree ≥1 | `note_links` query confirms in_degree ≥1 per new note (anti-island) |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_cli_gateway_run oc_cli_gateway_query oc_cli_health oc_cli_hooks oc_cli_infer oc_cli_mcp_serve oc_cli_mcp_registry oc_cli_mcp_transports oc_cli_memory oc_cli_logs"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w ${cb}cb)"
  # sibling-prefix self-reference present (intra-series link)
  grep -q "$SIBLING_PREFIX" "$f" || echo "$n NO SIBLING LINK"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5 ghost-reference + G6 broken links after reindex
bash scripts/update_notes_database.sh
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_cli_gateway_run | procedure | 700 | ≤6 | ✅ (source slice ~1,500w / 9 fences → trimmed) |
| 2 | oc_cli_gateway_query | procedure | 700 | ≤6 | ✅ (source slice ~2,150w / 8 fences → trimmed) |
| 3 | oc_cli_health | procedure | 250 | 1 | ✅ |
| 4 | oc_cli_hooks | procedure | 700 | ≤6 | ✅ (source 1,035w / 23 fences → output/example fences trimmed) |
| 5 | oc_cli_infer | procedure | 750 | ≤6 | ✅ (source 2,381w / 14 fences → representative command blocks only) |
| 6 | oc_cli_mcp_serve | procedure | 750 | ≤6 | ✅ (source slice ~2,400w / ~12 fences → trimmed) |
| 7 | oc_cli_mcp_registry | procedure | 700 | ≤6 | ✅ (recipe/example fences trimmed) |
| 8 | oc_cli_mcp_transports | model | 600 | ≤6 | ✅ (3 JSON shapes + 1 config example kept) |
| 9 | oc_cli_memory | procedure | 700 | ≤5 | ✅ (source 1,122w / 5 fences) |
| 10 | oc_cli_logs | procedure | 350 | 1 | ✅ |

No note approaches the caps. The code-dense pages (gateway 17, hooks 23, infer 14, mcp 23 fences) are split and/or trimmed so each note keeps ≤6 verbatim snippets.

## Entry Point Decision (inherited from master)

Contributes **10 rows** to `entry_openclaw_docs.md` (created as a master pre-step W1) under a "CLI — operational core (cl04)" cluster. Each new note receives its entry-point back-link at finalization (satisfies G7/G8). No new entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; each gives every new note in-degree ≥1 for G7/G8):

- **entry_openclaw_docs.md** → all 10 notes (primary anti-island guarantee).
- **repo_openclaw_gateway.md** → notes 1, 2, 3, 6, 7, 8, 10 (gateway/MCP/health/logs CLI ↔ gateway code).
- **repo_openclaw_memory.md** → notes 4 (session-memory hook), 9 (memory CLI).
- **repo_openclaw_agents.md** → notes 5 (infer capability runtime), 9 (per-agent memory).
- **repo_openclaw_extensions_llm_providers.md** → note 5 (infer providers).
- **term_health_check.md** → notes 2, 3; **term_websocket.md** → notes 1, 2, 10; **term_rag.md** → note 9; **term_cron.md** → notes 4, 9.
- **term_text_to_speech.md** / **term_speech_to_text.md** / **term_embedding.md** → note 5.

## Pacing Rules (inherited from master)

- Single execution phase; all 8 gates pass before commit. Cap dynamic-workflow fan-out at ~30 agents/run (10 notes is well under). Re-read each source page during execution; reproduce commands/config snippets verbatim. One BB per note.
- `git pull --rebase --autostash origin main` first; commit + push the wave together; no Claude co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links before commit.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Follow-up Recommendations

- At augment: lock the per-note Related mapping (raise to the master floor with relevance statements), re-confirm the `term_semantic_search` MISSING decision (link term_rag/term_vector_database), and verify the gateway/mcp split boundaries against a fresh re-read. **DONE 2026-06-21.**
- Cross-link cl05 (`cli/models`, `cli/node`/`nodes`) and gw0x (gateway runbooks: bonjour, discovery, health, logging, diagnostics) once those notes exist; cl01 (`cli/acp`) for the serve-vs-ACP decision.

## Augmentation Report (2026-06-21)



**Per-note counts (terms / snippets / docs[existing+sibling] / repos):**

| Note | Terms | Snippets | Docs (exist+sib) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_cli_gateway_run | 8 | 12 | 11 (6+5) | 3 | ✅ |
| oc_cli_gateway_query | 9 | 12 | 11 (6+5) | 3 | ✅ |
| oc_cli_health | 8 | 10 | 10 (5+5) | 2 | ✅ |
| oc_cli_hooks | 8 | 11 | 10 (5+5) | 3 | ✅ |
| oc_cli_infer | 10 | 12 | 12 (7+5) | 3 | ✅ |
| oc_cli_mcp_serve | 9 | 12 | 11 (6+5) | 3 | ✅ |
| oc_cli_mcp_registry | 9 | 12 | 11 (6+5) | 3 | ✅ |
| oc_cli_mcp_transports | 8 | 10 | 10 (6+4) | 2 | ✅ |
| oc_cli_memory | 9 | 11 | 11 (6+5) | 3 | ✅ |
| oc_cli_logs | 8 | 10 | 10 (5+5) | 2 | ✅ |


**New-term candidate + best-fit glossary.** None promoted. The only candidate gap is **semantic search** (`term_semantic_search`, MISSING) — left uncaptured by cl04 (cross-cutting; owned by the retrieval/RAG corpus, not this CLI sub-plan). Best-fit glossary IF ever captured: `acronym_glossary_ai_ml.md`. Re-confirmed at augment. Expected new `term_dictionary` captures from cl04: **0**.

**Source re-read note (Step 2a measured).** gateway 3,656w · mcp 4,518w · infer 2,381w · memory 1,122w · hooks 1,035w · health 190w · logs 436w — all within ±2% of the plan's Source table (no density estimation failure; splits already correct). No newly-surfaced undigested terms (Step 2d clean — 0 new).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

```
PLAN REVIEW — FINAL SIGN-OFF
Plan: plan_digest_openclaw_docs_cl04.md
Date: 2026-06-21
```

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors | **PASS** | Per-Note Related Notes Mapping: all 10 notes ≥8 terms (min 8, max 10) + ≥10 snippets + ≥10 docs, each link with a relevance statement; bare links absent. |
| CP2 | 9-GATE present (G1–G6,G8) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table present; single phase; G1 format, G2 grounding, G3 density+coverage, G4 cross-ref (raised floors), G5 ghost-reference, G6 broken-link, G7+G8 discoverability/in-degree all present. |
| CP3 | Entry point inherited (entry_openclaw_docs planned W1) | **PASS** | "Entry Point Decision" inherits master: contributes 10 rows to `entry_openclaw_docs.md` (created at master pre-step W1); each note gets entry-point back-link at finalization (G7/G8). No new entry point created by sub-plan. |
| CP4 | Size | **PASS** | 10 notes ≤ 30-note plan-size rule. |
| CP5 | Format derived | **PASS** | Format inherited verbatim from master Format Definition, derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora: `## Overview` / `## Related Notes` / `## References` + bold footer; YAML field order + forbidden-field list match. |
| CP6 | Density | **PASS** | Density Re-Assessment table: every note ≤750w (avg ~620w) / ≤6 code blocks / ≤400 lines; code-dense pages (gateway/hooks/mcp/infer) split and trimmed. No borderline note. |
| CP7 | Sources measured | **PASS** | Re-read all 7 pages 2026-06-21: gateway 3,656 / mcp 4,518 / infer 2,381 / memory 1,122 / hooks 1,035 / health 190 / logs 436 — all within ±2% of plan estimates (ratio 0.98–1.0). No under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | "Undigested Terms Plan" present (all OpenClaw vocab → `oc_*` doc notes, existing terms linked, 0 new captures); "Term-Note Authoring Requirements" present (N/A, 0 new terms, inherited from master). |
| CP8f | Slug/collision | **PASS** | 0 new term slugs (no specificity/rename needed). Collision audit on the 10 planned doc slugs: no `oc_cli_*` note exists yet (`resources/documentation/openclaw/*` empty); planned doc notes do NOT duplicate existing term notes (term_mcp/term_health_check/etc. are LINKED, not recreated — confirmed in mapping). |
| CP9 | Discoverability / inlinks | **PASS** | "Inlinks (existing notes → new notes)" maps every new note to ≥1 outside-folder inbound link (entry_openclaw_docs + repo_openclaw* / term_* inlinks); G8-Discoverability in the phase gate table; inlinks are a gated execution step, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.**
