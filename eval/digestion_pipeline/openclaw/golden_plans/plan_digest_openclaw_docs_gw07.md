---
title: Sub-Plan gw07 — OpenClaw Docs: Gateway (Tools-Invoke HTTP API, Troubleshooting, Trusted-Proxy Auth)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["gateway/tools-invoke-http-api", "gateway/troubleshooting", "gateway/trusted-proxy-auth"]
---

# Sub-Plan gw07: Gateway

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML frontmatter + `## Overview`/source-mirrored H2/H3/`## Related Notes`/`## References` + bold footer), dedup-before-create (term_dictionary AND documentation/ AND `repo_openclaw*`), the 9-GATE, cross-refs, and entry-point wiring (`entry_openclaw_docs.md`) are ALL inherited from the master.

## Scope

The three Gateway operational/security pages that do not fit gw01–gw06: the direct single-tool HTTP invocation endpoint (`/tools/invoke`), the deep gateway/channels/automation/nodes/browser troubleshooting runbook, and trusted-proxy (identity-aware reverse-proxy) authentication. These are the "operate it / secure it / fix it" tail of the Gateway section — high operational relevance for anyone running an OpenClaw gateway. **Priority P1 (Phase A — Gateway).** OpenClaw is the FZ 15 integration target, and these pages define the gateway HTTP surface, its auth boundary, and the symptom→command→fix knowledge an operator needs. The code-side counterparts (`repo_openclaw_gateway`, `repo_openclaw_security`) and the gateway/security code snippets are LINKED, never recreated.

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Tools invoke API | `gateway/tools-invoke-http-api` | 1,072 | 3 | 7 | 0 | procedure (HTTP-endpoint how-to + security boundary) |
| Troubleshooting | `gateway/troubleshooting` | 5,714 | 31 | 21 | 1 | procedure (symptom-based runbook; SPLIT) |
| Trusted proxy auth | `gateway/trusted-proxy-auth` | 2,512 | 10 | 14 | 2 | procedure (reverse-proxy auth setup) |

Total measured: **9,298 words, 44 code blocks** (fences ÷ 2: 6/2, 62/2, 20/2). Troubleshooting (5,714w / 21 H2) far exceeds the 2,500-word cap and is multi-cluster ⇒ SPLIT into 3 notes; the other two pages are single notes. **Planned: 5 notes.**

## Content Strategy

- **Prioritize**: (1) the `/tools/invoke` security boundary (it is a full operator-access surface with a hard deny list — the most security-load-bearing content here), and (2) the trusted-proxy auth model + security checklist (an identity-delegation mode flagged `critical` by `openclaw security audit`). These are the cross-cutting facts other gateway/security notes will link back to.
- **Split**: `troubleshooting.md` (5,714w) into 3 symptom-cluster notes by subsystem — (a) gateway-process/config/update/protocol/memory/probe, (b) auth/connectivity (dashboard Control UI connect, auth detail-code map, device-auth v2, post-upgrade auth drift), and (c) message-flow/runtime (no-replies, channel-connected-but-silent, cron/heartbeat, node-tool, browser-tool). This keeps each note ≤~2,000w / ≤6 code blocks and one coherent task cluster. The 31 source `bash` snippets are reproduced selectively (≤6/note) — command ladders kept verbatim, repetitive per-symptom ladders summarized.
- **Link-out (do NOT redefine)**: gateway auth *modes* themselves live in `gateway/authentication` (gw01) and `gateway/configuration` (gw02) → link, not restate; the `gateway/security` audit detail lives in gw06 → link; channel/node/browser troubleshooting deep-dives have their own pages (channels/troubleshooting, nodes/troubleshooting, tools/browser-linux-troubleshooting) in other sub-plans → link as "see also". Existing vocabulary (`term_oauth`, `term_authentication`, `term_reverse_proxy`, `term_rate_limiting`, `term_tls`, `term_websocket`, `term_function_calling`, `term_cron`) is LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_gateway_tools_invoke_http_api.md` | procedure | `gateway/tools-invoke-http-api`: Authentication, Security boundary, Request body, Policy + routing behavior, Responses, Example, Related | 700 | The Gateway `POST /tools/invoke` HTTP endpoint for invoking a single tool directly: auth paths (shared-secret bearer / trusted-proxy / none), the full-operator-access security boundary, request-body schema, tool-policy filtering, the default hard deny list (exec/spawn/shell/fs_write/…), `gateway.tools` allow/deny overrides, and response codes. |
| 2 | `oc_gateway_troubleshooting_process_config.md` | procedure | `gateway/troubleshooting`: Command ladder, After an update, Split brain installs and newer config guard, Protocol mismatch after rollback, Skill symlink skipped as path escape, Gateway service not running, macOS gateway silently stops, Gateway exits during high memory use, Gateway rejected invalid config, Gateway probe warnings | 1,900 | Gateway process/config troubleshooting runbook: the command ladder, post-update recovery, split-brain/newer-config-guard, protocol-mismatch-after-rollback, skill-symlink-escape, service-not-running, macOS maintenance-sleep crashes, high-memory/OOM stability bundles, invalid-config rejection/repair, and probe warnings — each with exact commands and signatures. |
| 3 | `oc_gateway_troubleshooting_auth_connectivity.md` | procedure | `gateway/troubleshooting`: Anthropic 429 extra usage for long context, Upstream 403 blocked responses, Local OpenAI-compatible backend passes probes but agent runs fail, Dashboard control UI connectivity (+ Auth detail codes quick map, device-auth v2 migration), If you upgraded and something suddenly broke | 1,700 | Auth, model-call, and connectivity troubleshooting: Anthropic long-context 429, upstream-WAF 403, local OpenAI-compatible-backend compat fixes, Control UI / dashboard connect failures with the `error.details.code` auth detail-code map, device-auth v2 handshake, and post-upgrade auth/URL/bind drift. |
| 4 | `oc_gateway_troubleshooting_message_runtime.md` | procedure | `gateway/troubleshooting`: No replies, Channel connected messages not flowing, Cron and heartbeat delivery, Node paired tool fails, Browser tool fails, Related | 1,500 | Message-flow and runtime troubleshooting: no-replies / channel-connected-but-silent (pairing, mention gating, allowlist), cron+heartbeat delivery skip reasons, node-paired-tool failures (permissions/approvals), and browser-tool failures (plugin allow, CDP, existing-session signatures). |
| 5 | `oc_gateway_trusted_proxy_auth.md` | procedure | `gateway/trusted-proxy-auth`: When to use / NOT use, How it works, Control UI pairing behavior, Configuration (+ reference), TLS termination and HSTS, Proxy setup examples (Pomerium/Caddy/nginx/Traefik), Mixed token configuration, Operator scopes header, Security checklist, Security audit, Troubleshooting, Migration from token auth | 1,500 | Delegating Gateway auth to a trusted identity-aware reverse proxy (`gateway.auth.mode="trusted-proxy"`): when to use, the proxy-IP + identity-header trust flow, Control UI device-less scope behavior, config reference, TLS/HSTS placement, Pomerium/Caddy/nginx/Traefik examples, mixed-token rejection, the `x-openclaw-scopes` cap, security checklist/audit, and migration. |

One building_block per note (all five are `procedure`). No note exceeds the 2,500-word / 400-line / 6-code-block caps (see Density Re-Assessment).

## Section Coverage Map

Every source H2/H3 maps to exactly one planned note. No orphans.

```
gateway/tools-invoke-http-api.md (7 H2)
├── (intro: POST /tools/invoke, port, 2MB payload) ── → note 1 (oc_gateway_tools_invoke_http_api)
├── ## Authentication ─────────────────────────────── → note 1
├── ## Security boundary (important) ──────────────── → note 1
├── ## Request body ──────────────────────────────── → note 1
├── ## Policy + routing behavior (hard deny list) ── → note 1
├── ## Responses ─────────────────────────────────── → note 1
├── ## Example ───────────────────────────────────── → note 1
└── ## Related ───────────────────────────────────── → note 1 (References / see-also)

gateway/troubleshooting.md (21 H2 / 1 H3)
├── ## Command ladder ────────────────────────────── → note 2 (process_config)
├── ## After an update ───────────────────────────── → note 2
├── ## Split brain installs and newer config guard ─ → note 2
├── ## Protocol mismatch after rollback ──────────── → note 2
├── ## Skill symlink skipped as path escape ──────── → note 2
├── ## Gateway service not running ────────────────── → note 2
├── ## macOS gateway silently stops responding … ─── → note 2
├── ## Gateway exits during high memory use ───────── → note 2
├── ## Gateway rejected invalid config ───────────── → note 2
├── ## Gateway probe warnings ────────────────────── → note 2
├── ## Anthropic 429 extra usage … long context ──── → note 3 (auth_connectivity)
├── ## Upstream 403 blocked responses ────────────── → note 3
├── ## Local OpenAI-compatible backend … runs fail ─ → note 3
├── ## Dashboard control UI connectivity ─────────── → note 3
│   └── ### Auth detail codes quick map ──────────── → note 3
├── ## If you upgraded and something suddenly broke  → note 3
├── ## No replies ────────────────────────────────── → note 4 (message_runtime)
├── ## Channel connected, messages not flowing ───── → note 4
├── ## Cron and heartbeat delivery ───────────────── → note 4
├── ## Node paired, tool fails ───────────────────── → note 4
├── ## Browser tool fails ────────────────────────── → note 4
└── ## Related ───────────────────────────────────── → note 4 (References / see-also)

gateway/trusted-proxy-auth.md (14 H2 / 2 H3)
├── (intro Warning: security-sensitive) ──────────── → note 5 (trusted_proxy_auth)
├── ## When to use / ## When NOT to use ──────────── → note 5
├── ## How it works ──────────────────────────────── → note 5
├── ## Control UI pairing behavior ───────────────── → note 5
├── ## Configuration ─────────────────────────────── → note 5
│   └── ### Configuration reference (ParamFields) ── → note 5
├── ## TLS termination and HSTS ──────────────────── → note 5
│   └── ### Rollout guidance ──────────────────────── → note 5
├── ## Proxy setup examples (Pomerium/Caddy/nginx/Traefik) → note 5
├── ## Mixed token configuration ─────────────────── → note 5
├── ## Operator scopes header ────────────────────── → note 5
├── ## Security checklist ────────────────────────── → note 5
├── ## Security audit ────────────────────────────── → note 5
├── ## Troubleshooting (trusted_proxy_* codes) ───── → note 5
├── ## Migration from token auth ─────────────────── → note 5
└── ## Related ───────────────────────────────────── → note 5 (References / see-also)
```

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| `gateway/troubleshooting.md` (5,714w, 21 H2 / 1 H3, 31 code blocks) | notes 2 + 3 + 4 | Exceeds the 2,500-word / 6-code-block caps ~2.3×. The runbook is three distinct symptom clusters by subsystem: (2) gateway process/config/update/protocol/memory/probe, (3) auth + model-call + Control UI connectivity, (4) message-flow + cron/heartbeat + node + browser. Splitting keeps each note ≤~2,000w, ≤6 code blocks, and one coherent operator task cluster — and lets sibling notes (e.g. an auth doc) link the precise relevant cluster. |
| `gateway/tools-invoke-http-api.md` (1,072w) | note 1 (no split) | Single coherent endpoint how-to; well under caps. |
| `gateway/trusted-proxy-auth.md` (2,512w, 14 H2) | note 5 (no split) | Marginally over the 2,500-word cap but a single tightly-coupled topic (one auth mode end-to-end: setup → examples → checklist → audit → troubleshooting → migration). Splitting would fragment a single decision flow; trim slightly (compress the 4 near-identical proxy examples to their distinct headers/identity-header lines) to land ≤~1,500 digest words. Borderline per CP6 → kept single because no clean BB or task-cluster boundary exists. |

## Summary Statistics & Building Block Distribution

- Source pages: **3** (9,298 measured words, 44 code blocks).
- New `oc_*` notes: **5** (1 from tools-invoke, 3 from troubleshooting, 1 from trusted-proxy-auth).
- New `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: **procedure ×5** (all five). No concept/model/argument notes (these are operational/security how-to pages; the trusted-proxy security boundary is procedural with strong policy callouts, kept as procedure with prominent security warnings rather than argument).
- Estimated digest words: ~7,300 total (note 1 ~700, note 2 ~1,900, note 3 ~1,700, note 4 ~1,500, note 5 ~1,500); avg ~1,460/note, all ≤2,500.
- Code blocks: 44 source fences distribute across the 5 notes; each note caps at 6 (command ladders + key config snippets reproduced verbatim; repetitive per-symptom ladders and the 4 near-duplicate proxy examples compressed).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_gateway_tools_invoke_http_api (8t · 11s · 10d)

- [function calling](../../term_dictionary/term_function_calling.md) — LLM tool/function invocation; relevance: `/tools/invoke` invokes exactly one named tool with `args`, the unit of function-calling this endpoint exposes over HTTP.
- [authentication](../../term_dictionary/term_authentication.md) — verifying caller identity; relevance: the endpoint uses Gateway auth (token/password/trusted-proxy/none) — the page's whole Authentication + auth-matrix section.
- [OAuth token](../../term_dictionary/term_oauth_token.md) — bearer credential; relevance: shared-secret auth is sent as `Authorization: Bearer <token>` and treated as a full operator credential.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: the trusted-proxy auth path delegates identity to an OAuth/OIDC proxy that injects identity headers.
- [API gateway](../../term_dictionary/term_api_gateway.md) — HTTP entry point fronting backend services; relevance: `/tools/invoke` is one route on the Gateway's HTTP surface (same port, WS+HTTP multiplex).
- [rate limiting](../../term_dictionary/term_rate_limiting.md) — throttling requests; relevance: `gateway.auth.rateLimit` returns `429` + `Retry-After` after too many auth failures on this endpoint.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex protocol over one TCP port; relevance: the endpoint shares the Gateway port via WS+HTTP multiplex (`http://<host>:<port>/tools/invoke`).
- [sandbox](../../term_dictionary/term_sandbox.md) — confinement of dangerous operations; relevance: the hard deny list (`exec`/`spawn`/`shell`/`fs_write`/…) is the RCE/sandbox boundary that blocks mutating tools even when session policy allows them.

- [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — Claude Code MCP server auth; relevance: analogous tool/MCP auth boundary where a bearer credential gates tool access.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — HTTP proxy/gateway config for an agent; relevance: parallel of configuring the gateway HTTP/auth surface this endpoint sits on.
- [cc_sdk_mcp_auth_and_errors](../claude_code/cc_sdk_mcp_auth_and_errors.md) — MCP auth + error handling in the SDK; relevance: the `200/400/401/404/429/500` response shape mirrors the SDK tool-call auth/error contract.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code authentication options; relevance: cross-tool reference for bearer-vs-identity auth choices behind a tool-invoke surface.
- [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — web security boundaries + payload limits; relevance: parallels the 2 MB payload cap + "keep off public internet" security boundary.
- [hermes_api_server_setup_auth](../hermes_agent/hermes_api_server_setup_auth.md) — Hermes API-server auth setup; relevance: sibling coding-agent's HTTP API auth, the closest analog to this Gateway HTTP endpoint's bearer model.
- [hermes_dashboard_rest_api](../hermes_agent/hermes_dashboard_rest_api.md) — Hermes REST API surface; relevance: comparison HTTP-RPC surface for invoking agent operations directly.
- [band_websocket_overview](../band/band_websocket_overview.md) — WebSocket transport overview; relevance: explains the WS+HTTP multiplex transport this endpoint shares with the Gateway port.
- [oc_gateway_trusted_proxy_auth](oc_gateway_trusted_proxy_auth.md) — trusted-proxy auth mode (planned, this series); relevance: one of the three auth paths this endpoint accepts (`gateway.auth.mode="trusted-proxy"`).
- [oc_gateway_troubleshooting_auth_connectivity](oc_gateway_troubleshooting_auth_connectivity.md) — auth/connectivity troubleshooting (planned, this series); relevance: where `401`/`429` failures from this endpoint are diagnosed.

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway HTTP/WS server; relevance: implements the `/tools/invoke` route + auth + response codes.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/policy code; relevance: owns the hard deny list + dangerous-tool policy enforced here.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent + tool-policy code; relevance: the `tools.allow`/`byProvider`/per-agent policy chain that filters tool availability (404 if denied).

- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize-then-dispatch flow; relevance: the auth-check that gates this endpoint before a tool runs.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — token/password/trusted-proxy/none helpers; relevance: implements the exact auth modes in the page's auth matrix.
- [snippet_openclaw_gateway_auth_rate_limit_install_policy](../../code_snippets/snippet_openclaw_gateway_auth_rate_limit_install_policy.md) — auth rate-limit policy install; relevance: the `429`+`Retry-After` lockout this endpoint returns on auth-failure bursts.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — per-method scope gating; relevance: the operator-scope gating that decides owner-vs-narrowed access for invokes.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool allow/deny policy resolution; relevance: the policy chain (`tools.allow`, `byProvider`, per-agent, group) that yields 404 when a tool is not allowed.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tools deny list; relevance: the verbatim hard deny list (`exec`/`spawn`/`shell`/`fs_*`/`cron`/`gateway`/`nodes`…) this page documents.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WS listener; relevance: the WS+HTTP multiplex on one port that serves `/tools/invoke`.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP route dispatch; relevance: how the server routes `POST /tools/invoke` and returns method-not-allowed (`405`) for other verbs.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — misc server method handlers; relevance: the request-parse + `400`/`500` error envelope (`{ ok:false, error:{type,message} }`) returned here.
- [snippet_openclaw_gateway_agent_dispatch_handler](../../code_snippets/snippet_openclaw_gateway_agent_dispatch_handler.md) — agent/session dispatch; relevance: how `sessionKey` (`main`/agent/`global`) routes the invoke into a session.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: explains why denying `write`/`edit`/`apply_patch` does NOT make a reachable `exec` read-only (the page's boundary note).

### oc_gateway_troubleshooting_process_config (8t · 10s · 10d)

- [health check](../../term_dictionary/term_health_check.md) — liveness/readiness probe; relevance: the command ladder + `gateway status --deep`/`doctor`/probe signals (`Runtime: running`, `Connectivity probe: ok`).
- [authentication](../../term_dictionary/term_authentication.md) — caller-identity verification; relevance: `refusing to bind gateway … without auth` — non-loopback bind requires a valid auth path.
- [TLS](../../term_dictionary/term_tls.md) — transport security; relevance: bind/auth guardrails for non-loopback (`lan`/`tailnet`/`custom`) exposure that pair with TLS posture.
- [WebSocket](../../term_dictionary/term_websocket.md) — Gateway client transport; relevance: `Established clients:` / `Gateway clients` in `status --deep`/`doctor --deep` are the WS/TCP clients to clean up on protocol mismatch.
- [sandbox](../../term_dictionary/term_sandbox.md) — containment boundary; relevance: skill-root containment + `symlink-escape` (`allowSymlinkTargets`) is the path-escape sandbox the page troubleshoots.
- [cron](../../term_dictionary/term_cron.md) — scheduled-task subsystem; relevance: cron/heartbeat scheduler health is gated on gateway process state recovered by this runbook.
- [failover](../../term_dictionary/term_failover.md) — recovery to a healthy state; relevance: split-brain / newer-config-guard / protocol-mismatch-after-rollback are version-failover recovery flows.
- [memory dreaming](../../term_dictionary/term_memory_dreaming.md) — OpenClaw background memory consolidation; relevance: `doctor` memory/dreaming preview + high-memory/OOM stability bundles (`diagnostic.memory.pressure.critical`) this note covers.

- [cc_troubleshoot_memory](../claude_code/cc_troubleshoot_memory.md) — agent OOM/memory-pressure diagnosis; relevance: direct analog to the high-memory/OOM stability-bundle section (`V8 heap`, RSS thresholds).
- [cc_performance_and_stability](../claude_code/cc_performance_and_stability.md) — process performance/stability; relevance: parallels the macOS maintenance-sleep crash + respawn-gate stability runbook.
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — config debugging; relevance: analog to `Gateway rejected invalid config` (validate, `.rejected.*`/`.clobbered.*`, repair).
- [cc_install_diagnostics](../claude_code/cc_install_diagnostics.md) — install/version diagnostics; relevance: parallels split-brain installs + `which openclaw`/`--version` PATH cleanup.
- [cc_environment_variables](../claude_code/cc_environment_variables.md) — env-var reference; relevance: documents env overrides like the `OPENCLAW_ALLOW_OLDER_BINARY_DESTRUCTIVE_ACTIONS` / `OPENCLAW_SERVICE_REPAIR_POLICY` escape hatches.
- [cc_settings_reference](../claude_code/cc_settings_reference.md) — settings/config reference; relevance: analog for the `gateway.mode`/`skills.load`/`diagnostics` config keys touched in repair steps.
- [hermes_gateway_internals](../hermes_agent/hermes_gateway_internals.md) — Hermes gateway process internals; relevance: sibling gateway's service/process lifecycle, the closest analog to OpenClaw's service-not-running diagnosis.
- [hermes_cli_commands_ops_maintenance_auth](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md) — ops/maintenance CLI; relevance: parallel restart/doctor/maintenance command surface.
- [oc_gateway_troubleshooting_auth_connectivity](oc_gateway_troubleshooting_auth_connectivity.md) — auth/connectivity troubleshooting (planned, this series); relevance: sibling cluster for the auth-side failures that overlap post-update drift.
- [oc_gateway_troubleshooting_message_runtime](oc_gateway_troubleshooting_message_runtime.md) — message/runtime troubleshooting (planned, this series); relevance: sibling cluster for the message-flow side once the process is healthy.

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway process/service code; relevance: implements service start/stop/restart, config reload, and the version-guard refusals.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/config-validation code; relevance: owns invalid-config rejection (`.rejected.*`) and skill-root escape checks.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skill loader; relevance: the symlink-escape containment + `allowSymlinkTargets` handling.

- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — apply a config reload; relevance: hot-reload apply path that skips invalid edits (the rejected-config section).
- [snippet_openclaw_gateway_config_reload_plan](../../code_snippets/snippet_openclaw_gateway_config_reload_plan.md) — plan a config reload; relevance: the reload-plan stage where invalid external edits are detected and ignored.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — compile-cache + respawn; relevance: the respawn behavior behind post-update restart + KeepAlive/respawn-gate troubleshooting.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — doctor memory/dreaming preview; relevance: the doctor memory-pressure diagnostics behind the OOM/stability-bundle section.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — server config + plugin load; relevance: `plugin load failed: dependency tree corrupted` after-update recovery (`doctor --fix`).
- [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart on startup; relevance: empty-channels-after-update recovery during gateway restart.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — auth checks at startup; relevance: `refusing to bind … without auth` / `gateway.mode` startup-fail-closed guard.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — shutdown/exit handling; relevance: clean-shutdown signal logging vs transient-crash (the macOS `received SIG*` distinction).
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env resolution; relevance: how env flags (older-binary destructive actions, service-repair policy) gate process mutations.
- [snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md) — post-attach runtime setup; relevance: the startup sequence that surfaces probe warnings + capability/connectivity signals.

### oc_gateway_troubleshooting_auth_connectivity (8t · 10s · 11d)

- [authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: the whole `error.details.code` auth detail-code map + device-auth v2 handshake.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated auth protocol; relevance: stale per-agent OAuth auth shadows removed by `doctor --fix`, re-auth after update.
- [OAuth token](../../term_dictionary/term_oauth_token.md) — bearer/device token; relevance: `AUTH_TOKEN_MISMATCH`/`AUTH_DEVICE_TOKEN_MISMATCH` token-drift recovery + cached-token retry.
- [WebSocket](../../term_dictionary/term_websocket.md) — Control UI transport; relevance: Control UI WS connect, `device nonce`/`signature` challenge, and `missing scope` after connect.
- [rate limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: Anthropic `429 … long context` + `too many failed authentication attempts (retry later)` lockout buckets.
- [reverse proxy](../../term_dictionary/term_reverse_proxy.md) — upstream proxy layer; relevance: upstream `403 blocked` from a CDN/WAF/reverse proxy in front of an OpenAI-compatible endpoint.
- [WAF](../../term_dictionary/term_waf.md) — web application firewall; relevance: the upstream-403 section explicitly blames WAF/bot-management/CDN security layers.
- [TLS](../../term_dictionary/term_tls.md) — transport security / secure context; relevance: HTTP-where-device-identity-required → use HTTPS so the browser can generate device identity.

- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — auth + network error reference; relevance: direct analog to the connect/auth + 401/403 connectivity failure catalog.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login/auth troubleshooting; relevance: parallels re-auth/token-drift recovery after upgrade.
- [cc_authentication](../claude_code/cc_authentication.md) — auth options; relevance: cross-reference for the auth modes whose drift this note diagnoses.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network/TLS/access; relevance: secure-context/HTTPS requirement for device identity + access errors.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: upstream-proxy/WAF-403 + OpenAI-compatible backend routing config.
- [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — server/usage-limit (429) errors; relevance: direct analog to the Anthropic `429 long-context` rate-limit section.
- [cc_request_and_quality_errors](../claude_code/cc_request_and_quality_errors.md) — request/quality errors; relevance: parallels the `model_not_found`/empty-turn/`incomplete turn` OpenAI-compatible-backend signatures.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — Hermes dashboard remote auth; relevance: sibling Control-UI/dashboard remote-auth connectivity, the closest analog to OpenClaw dashboard connect failures.
- [oc_gateway_trusted_proxy_auth](oc_gateway_trusted_proxy_auth.md) — trusted-proxy auth (planned, this series); relevance: the device-less Control-UI scope behavior + `missing scope` fix referenced here.
- [oc_gateway_troubleshooting_process_config](oc_gateway_troubleshooting_process_config.md) — process/config troubleshooting (planned, this series); relevance: sibling cluster for the process-side of post-update breakage.
- [oc_gateway_tools_invoke_http_api](oc_gateway_tools_invoke_http_api.md) — tools-invoke HTTP API (planned, this series); relevance: the endpoint whose `401`/`429` auth-failure responses this note explains.

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway connect/auth code; relevance: implements the connect handshake + auth error/detail codes.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — device-auth/scopes code; relevance: device-auth v2, scope mismatch, pairing-required logic.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM provider plugins; relevance: OpenAI-compatible backend `compat.*` flags + Anthropic long-context provider behavior.

- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error/detail codes; relevance: the `AUTH_TOKEN_MISSING`/`MISMATCH`/`SCOPE_MISMATCH`/`PAIRING_REQUIRED` map this note tabulates.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: the device-identity/ticket flow behind dashboard connect + nonce/signature checks.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect via proxy/url; relevance: `gateway connect failed`/wrong-url-target + remote-vs-local targeting after upgrade.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: token/password/trusted-proxy mode resolution behind the bind/auth drift.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — per-agent OAuth profile portability; relevance: the stale per-agent OAuth auth-shadow cleanup (`doctor --fix`) on re-auth 401s.
- [snippet_openclaw_gateway_mcp_http_loopback](../../code_snippets/snippet_openclaw_gateway_mcp_http_loopback.md) — loopback HTTP/MCP path; relevance: direct loopback backend RPC + `gateway-client`/`client.mode:"backend"` scope-baseline note.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — startup auth/bind guard; relevance: `refusing to bind … without auth` + non-loopback bind guardrails after upgrade.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC protocol schema; relevance: the connect/protocol handshake + `connect.rpcOk` diagnostics the probe surfaces.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — security/probe execution; relevance: the probe diagnostics (scopes missing, multiple-gateway warnings) cross-cut with connectivity checks.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env/url resolution; relevance: `gateway.mode=remote` / `gateway.remote.url` targeting that misroutes CLI calls after upgrade.

### oc_gateway_troubleshooting_message_runtime (8t · 10s · 10d)

- [cron](../../term_dictionary/term_cron.md) — scheduled-task subsystem; relevance: `cron status`/`runs` + scheduler-disabled/timer-tick-failed signatures.
- [heartbeat](../../term_dictionary/term_heartbeat.md) — periodic liveness/agent tick; relevance: heartbeat delivery skip reasons (`quiet-hours`, `no-tasks-due`, `dm-blocked`, `empty-heartbeat-file`).
- [access control](../../term_dictionary/term_access_control.md) — who-may-do-what policy; relevance: DM policy / allowlist / group mention gating (`requireMention`, `mentionPatterns`).
- [function calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: node-paired tool failures + `SYSTEM_RUN_DENIED` exec-approval/allowlist on the node tool surface.
- [authentication](../../term_dictionary/term_authentication.md) — identity/permission verification; relevance: channel auth `401/403`, `missing_scope`, `not_in_channel`, `Forbidden` permission signatures.
- [sandbox](../../term_dictionary/term_sandbox.md) — execution confinement; relevance: exec approvals + allowlist gating on node `system.run` (`SYSTEM_RUN_DENIED: allowlist miss`).
- [health check](../../term_dictionary/term_health_check.md) — status probe; relevance: `channels status --probe`, `nodes status`, `browser status` liveness checks open each cluster.
- [dm policy](../../term_dictionary/term_dm_policy.md) — direct-message gating policy; relevance: DM policy (`pairing`/`allowlist`/`open`/`disabled`) is the first thing to check when a channel is connected but silent.

- [cc_chrome_browser_automation](../claude_code/cc_chrome_browser_automation.md) — Chrome browser automation; relevance: direct analog to the browser-tool-fails cluster (CDP, profiles, plugin allow).
- [cc_chrome_setup_and_troubleshooting](../claude_code/cc_chrome_setup_and_troubleshooting.md) — Chrome setup/troubleshooting; relevance: parallels `DevToolsActivePort`/CDP/existing-session browser failures.
- [cc_computer_use](../claude_code/cc_computer_use.md) — computer-use/browser control; relevance: the browser-control surface whose failures this cluster diagnoses.
- [hermes_browser_supervisor](../hermes_agent/hermes_browser_supervisor.md) — Hermes browser supervisor; relevance: sibling agent's browser-process lifecycle, the closest analog to OpenClaw browser-tool start/attach failures.
- [hermes_browser_automation_backends](../hermes_agent/hermes_browser_automation_backends.md) — browser automation backends; relevance: managed-vs-existing-session/CDP backend distinctions mirrored in the signatures.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — provider fallback; relevance: parallels the "configure fallback models so runs continue" guidance touching message delivery.
- [cc_debug_your_configuration](../claude_code/cc_debug_your_configuration.md) — config debugging; relevance: analog for inspecting `channels`/`plugins.allow` config when flow is dead.
- [oc_gateway_troubleshooting_process_config](oc_gateway_troubleshooting_process_config.md) — process/config troubleshooting (planned, this series); relevance: sibling cluster — confirm the gateway process is healthy before chasing message flow.
- [oc_gateway_troubleshooting_auth_connectivity](oc_gateway_troubleshooting_auth_connectivity.md) — auth/connectivity troubleshooting (planned, this series); relevance: sibling cluster — channel `401/403`/`missing_scope` overlaps with auth diagnosis.
- [oc_gateway_tools_invoke_http_api](oc_gateway_tools_invoke_http_api.md) — tools-invoke HTTP API (planned, this series); relevance: node `nodes`/`exec` tool relay shares the tool-policy surface this endpoint also gates.

- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel routing/policy code; relevance: implements DM policy, allowlist, mention gating, and per-channel delivery.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — scheduler + node relay code; relevance: cron/heartbeat scheduler and the node command relay this note troubleshoots.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — per-agent tool policy/approvals; relevance: exec-approval + tool-policy state behind node-tool failures.

- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: `SYSTEM_RUN_DENIED` approval/allowlist gating on node `system.run`.
- [snippet_openclaw_gateway_chat_send_handler](../../code_snippets/snippet_openclaw_gateway_chat_send_handler.md) — chat send handler; relevance: the message-send path behind no-replies / channel-connected-but-silent.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — doctor cron/dream-diary repair; relevance: cron scheduler health + repair behind cron/heartbeat delivery skips.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool allow/deny policy; relevance: node-paired tool availability + per-agent allow/deny that yields tool failures.
- [snippet_openclaw_gateway_channels_runtime_snapshot](../../code_snippets/snippet_openclaw_gateway_channels_runtime_snapshot.md) — channels runtime snapshot; relevance: `channels status --probe` per-account transport/policy state.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem policy; relevance: the exec-approval/allowlist policy gating node `system.run`.
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke (APNs relay); relevance: the node command relay whose `NODE_BACKGROUND_UNAVAILABLE`/`*_PERMISSION_REQUIRED` failures this note maps.
- [snippet_openclaw_gateway_chat_abort_handler](../../code_snippets/snippet_openclaw_gateway_chat_abort_handler.md) — chat abort handling; relevance: turn lifecycle behind silent/no-reply behavior.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — channel socket-mode connect; relevance: a concrete channel-connected-but-not-flowing transport (`missing_scope`/`not_in_channel`) example.
- [snippet_openclaw_gateway_exec_approval_ios_push](../../code_snippets/snippet_openclaw_gateway_exec_approval_ios_push.md) — exec-approval push; relevance: the `SYSTEM_RUN_DENIED: approval required` pending-approval path on node tools.

### oc_gateway_trusted_proxy_auth (9t · 11s · 10d)

- [reverse proxy](../../term_dictionary/term_reverse_proxy.md) — proxy fronting a backend; relevance: the core mechanism — Gateway trusts an identity-aware reverse proxy (Pomerium/Caddy/nginx/Traefik).
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-auth protocol; relevance: the proxy authenticates via OAuth/OIDC/SAML and injects an identity header.
- [OAuth token](../../term_dictionary/term_oauth_token.md) — token credential; relevance: mixed-token rejection (`mixed_trusted_proxy_token`) — token + trusted-proxy can't coexist.
- [authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: auth is delegated to the proxy; Gateway extracts identity from `userHeader`.
- [TLS](../../term_dictionary/term_tls.md) — transport security; relevance: TLS termination point + HSTS placement (proxy-vs-gateway) and rollout guidance.
- [WebSocket](../../term_dictionary/term_websocket.md) — Control UI transport; relevance: WS `1008 unauthorized` errors + `x-openclaw-scopes` cap on the WS upgrade.
- [API gateway](../../term_dictionary/term_api_gateway.md) — HTTP entry surface; relevance: the Gateway HTTP surface sits behind the proxy; browser-origin/`allowedOrigins` still apply.
- [access control](../../term_dictionary/term_access_control.md) — authorization policy; relevance: `allowUsers` allowlist + operator-scope capping become the effective access control in this mode.
- [load balancer](../../term_dictionary/term_load_balancer.md) — traffic distributor; relevance: the `trusted_proxy_untrusted_source` troubleshooting caveat — an LB in front of the proxy changes the source IP.

- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: closest analog — configuring an agent behind an HTTP proxy/gateway.
- [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network/TLS/access; relevance: TLS termination + HSTS + access-origin policy this page details.
- [cc_cloud_network_access](../claude_code/cc_cloud_network_access.md) — cloud/network access; relevance: Kubernetes/container deployment where the proxy is the only path (the page's use-case).
- [cc_authentication](../claude_code/cc_authentication.md) — auth options; relevance: cross-reference for identity-delegation vs token auth trade-offs.
- [cc_web_security_and_limits](../claude_code/cc_web_security_and_limits.md) — web security boundaries; relevance: browser-origin policy + header-stripping security boundary the checklist enforces.
- [hermes_dashboard_auth_remote](../hermes_agent/hermes_dashboard_auth_remote.md) — Hermes dashboard remote auth; relevance: sibling agent's remote/reverse-proxy dashboard auth, the closest analog to this mode.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — Hermes proxy routing; relevance: parallel reverse-proxy/identity-header routing in a sibling coding agent.
- [oc_gateway_tools_invoke_http_api](oc_gateway_tools_invoke_http_api.md) — tools-invoke HTTP API (planned, this series); relevance: trusted-proxy is one of this endpoint's accepted auth paths.
- [oc_gateway_troubleshooting_auth_connectivity](oc_gateway_troubleshooting_auth_connectivity.md) — auth/connectivity troubleshooting (planned, this series); relevance: Control-UI device-less scope + `missing scope` failures cross-link here.
- [oc_gateway_troubleshooting_process_config](oc_gateway_troubleshooting_process_config.md) — process/config troubleshooting (planned, this series); relevance: `refusing to bind … without auth` non-loopback-bind guard interacts with trusted-proxy bind config.

- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — Gateway auth/header code; relevance: implements the trusted-proxy auth path, `trustedProxies` IP check, and header extraction.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security-audit/scope code; relevance: the `openclaw security audit` critical finding + scope-cap/`allowUsers` handling.

- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: the `trusted-proxy` mode branch + `allowLoopback`/`requiredHeaders` resolution.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect via proxy; relevance: the trusted-proxy source-IP + identity-header connect flow.
- [snippet_openclaw_gateway_control_ui_auth_ticket](../../code_snippets/snippet_openclaw_gateway_control_ui_auth_ticket.md) — Control UI auth ticket; relevance: device-less Control-UI WS sessions + scope-clearing behavior in this mode.
- [snippet_openclaw_gateway_connect_error_codes](../../code_snippets/snippet_openclaw_gateway_connect_error_codes.md) — connect error codes; relevance: the `trusted_proxy_*` error codes (untrusted_source, loopback_source, user_missing, user_not_allowed).
- [snippet_openclaw_security_audit_composition](../../code_snippets/snippet_openclaw_security_audit_composition.md) — security-audit composition; relevance: how the audit composes the trusted-proxy critical finding + sub-checks (missing `trustedProxies`/`userHeader`, empty `allowUsers`).
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize-then-dispatch; relevance: the authorize stage that consumes the extracted proxy identity + capped scopes.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — per-method scope gating; relevance: `x-openclaw-scopes` cap-not-grant + plugin-route `operator.write` fallback.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP+WS listener; relevance: the WS upgrade path where `1008 unauthorized` + scope capping occur.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — startup auth/bind guard; relevance: `mixed_trusted_proxy_token` startup rejection + non-loopback-bind guard for this mode.
- [snippet_openclaw_security_fix_remediation](../../code_snippets/snippet_openclaw_security_fix_remediation.md) — security-fix remediation; relevance: remediation guidance behind the security checklist + audit findings.
- [snippet_openclaw_security_audit_probe_execute](../../code_snippets/snippet_openclaw_security_audit_probe_execute.md) — security-audit probe execution; relevance: the audit run (`openclaw security audit`) invoked in the migration + checklist steps.

> Note: terms NOT in the vault that appear in these pages (e.g. a generic `term_zero_trust`, `term_hsts`, `term_oidc`, `term_saml`, `term_systemd`, `term_launchd`, `term_remote_code_execution`) are NOT created (see Undigested Terms Plan) — they are described in prose within the `oc_*` notes and linked to the nearest existing term when one exists (e.g. HSTS → `term_tls`; OIDC/SAML → `term_oauth`/`term_authentication`; RCE → `term_sandbox`; WAF/CDN → `term_waf`/`term_cdn`).

## Undigested Terms Plan

Per master design decision: OpenClaw vocabulary is digested as `oc_*` doc notes (these very notes), NOT new `term_dictionary` entries; the only term_dictionary interaction is LINKING existing terms. Expected **0 new term_dictionary captures**.

| Term (appears on these pages) | Disposition |
|---|---|
| trusted-proxy auth / identity-aware proxy | Digested in `oc_gateway_trusted_proxy_auth` (note 5); link `term_reverse_proxy` + `term_authentication`. No new term. |
| `/tools/invoke` HTTP endpoint | Digested in `oc_gateway_tools_invoke_http_api` (note 1); link `term_api_gateway` + `term_function_calling`. No new term. |
| operator scopes / `x-openclaw-scopes` | Digested in notes 1 + 5; link `term_access_control`. OpenClaw-specific vocabulary → stays in the `oc_*` notes. No new term. |
| device identity / pairing / device-auth v2 | Digested in note 3 (and gw01 `gateway/pairing` elsewhere); link `term_authentication`. OpenClaw-specific → no new term. |
| hard deny list (RCE tools) | Digested in note 1; link `term_sandbox`. No new term. |
| HSTS / `Strict-Transport-Security` | Described in note 5 prose; link existing `term_tls`. No new term. |
| OIDC / SAML / forward-auth | Described in note 5 prose; link existing `term_oauth` / `term_authentication`. No new term. |
| RCE (remote code execution) | Described in note 1 prose; link existing `term_sandbox`. No new term (`term_remote_code_execution`/`term_rce` not in vault; not cross-cutting enough to justify a new capture here). |
| WAF / CDN / bot-management | Described in note 3 prose; link existing `term_waf` + `term_cdn`. No new term. |
| OOM / memory pressure / stability bundle | Described in note 2 prose; OpenClaw-runtime-specific → stays in `oc_*` note. No new term. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing note was found. (If augment surfaces one, capture via `/tessellum-capture-term-note` and add to the agentic/LLM-dev `acronym_glossary_*.md`; expected glossary = none.)

## Term-Note Authoring Requirements

N/A (0 new terms). Inherited from master: any new `term_dictionary` note (none here) must be researched multi-source, follow the term-note format, and be added to its `acronym_glossary_*.md` with the correct indexed link format.

## Per-Phase Validation Gate (G1–G9)

Single execution phase (5 notes). All gates inherited from master; run after the wave.

| Gate | Check | Tool / Command | Pass criterion |
|---|---|---|---|
| G1 | Format + YAML frontmatter | `/tessellum-check-note-format` + `python3 scripts/check_yaml_frontmatter.py --path <note>` | Frontmatter field order/tags (`resource`,`documentation`,`openclaw`,`gateway`,…), required H2 (`## Overview`, `## Related Notes`), bold footer present; YAML valid (quoted year, itemized lists). |
| G2 | Grounding | Diff each note vs its source section(s) in `inbox/openclaw_docs/gateway/<page>.md` | Every claim/command/config key traces to source; no invented flags/codes. |
| G3 | Density + Coverage | line/word/code counts + Section Coverage Map | Each note ≤400 lines / ≤2,500 words / ≤6 code blocks; every source H2/H3 mapped (no orphan). |
| G5 | Ghost-reference detect + redirect | `/tessellum-fix-ghost-references` + DB-verify each cited note_id | 0 ghost references; every EXISTING cited note resolves in `notes`. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` + reindex | 0 broken links after `bash scripts/update_notes_database.sh`. |
| G7 | Discoverability (inbound) | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` rows + W3 code↔docs links). | in_degree ≥1 per new note. |
| G8 | Anti-island | `note_links` query post-reindex | No new note is an island; all 5 linked from `entry_openclaw_docs.md`. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
cd /path/to/vault

# Resolve config-driven paths
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")

# --- Gate sweep (run after the 5 notes are written) ---
GATE_DIR="resources/documentation/openclaw"
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"

NOTES="oc_gateway_tools_invoke_http_api oc_gateway_troubleshooting_process_config oc_gateway_troubleshooting_auth_connectivity oc_gateway_troubleshooting_message_runtime oc_gateway_trusted_proxy_auth"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  echo "=== $f ==="
  # G1: required H2 sections present
  for sec in "## Overview" "## Related Notes" "## References"; do
    grep -qF "$sec" "$f" || echo "  MISSING SECTION: $sec"
  done
  # G1: source_url present in frontmatter
  if [ "$REQUIRE_SOURCE_URL" = "1" ]; then
    grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "  MISSING source_url"
  fi
  # G3: density caps
  lc=$(wc -l < "$f"); wc=$(wc -w < "$f"); cb=$(( $(grep -c '```' "$f") / 2 ))
  [ "$lc" -le 400 ] || echo "  OVER 400 lines ($lc)"
  [ "$wc" -le 2500 ] || echo "  OVER 2500 words ($wc)"
  [ "$cb" -le 6 ] || echo "  OVER 6 code blocks ($cb)"
  # G4: ≥6 term links + ≥1 sibling oc_ link
  tl=$(grep -c 'term_dictionary/term_' "$f"); echo "  term links: $tl (need >=6)"
  sl=$(grep -c "($SIBLING_PREFIX" "$f"); echo "  sibling oc_ links: $sl"
done

# G1 (authoritative YAML check)
for n in ${=NOTES}; do
  python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR/$n.md"
done

# G5: DB-verify every cited EXISTING note_id resolves (sample; expand with augment-locked list)
for id in \
  resources/term_dictionary/term_reverse_proxy.md \
  resources/term_dictionary/term_authentication.md \
  resources/term_dictionary/term_function_calling.md \
  areas/code_repos/repo_openclaw_gateway.md \
  areas/code_repos/repo_openclaw_security.md \
  resources/documentation/claude_code/cc_proxy_and_gateway_config.md ; do
done

# G6/G8: reindex + broken-link + in-degree check (after writing)
bash scripts/update_notes_database.sh
for n in ${=NOTES}; do
  echo "$n in_degree=$deg (need >=1)"
done
```

## Density Re-Assessment

| Note | ~Words | Est. lines | Code blocks | Within caps (≤2500w / ≤400L / ≤6cb)? |
|---|---:|---:|---:|---|
| `oc_gateway_tools_invoke_http_api` | 700 | ~140 | 3 (request-body JSON, deny-override json5, curl example) | Yes |
| `oc_gateway_troubleshooting_process_config` | 1,900 | ~330 | 6 (command ladder + selective per-symptom ladders/config) | Yes (at code-block cap; repetitive ladders compressed) |
| `oc_gateway_troubleshooting_auth_connectivity` | 1,700 | ~300 | 6 (probe commands + compat config + detail-code table) | Yes |
| `oc_gateway_troubleshooting_message_runtime` | 1,500 | ~270 | 5 (channels/cron/node/browser command ladders) | Yes |
| `oc_gateway_trusted_proxy_auth` | 1,500 | ~290 | 6 (config + reference + 1–2 proxy examples + TLS) | Yes (4 near-duplicate proxy examples compressed to fit) |

All five within caps. Notes 2 and 5 are watched at execution: if a note approaches 2,500 words or 7 code blocks, prefer trimming repetitive command ladders / proxy examples over a re-split (clusters are already coherent).

## Entry Point Decision (inherited from master)

`entry_openclaw_docs.md` is CREATED as a master pre-step (W1, >30-note series). This sub-plan contributes **5 rows** to its Gateway-section table:

| Note | Section | One-line |
|---|---|---|
| `oc_gateway_tools_invoke_http_api` | Gateway | `POST /tools/invoke` direct single-tool HTTP endpoint, auth + hard deny list. |
| `oc_gateway_troubleshooting_process_config` | Gateway | Gateway process/config/update/protocol/memory/probe troubleshooting runbook. |
| `oc_gateway_troubleshooting_auth_connectivity` | Gateway | Auth, model-call, and Control UI connectivity troubleshooting + auth detail-code map. |
| `oc_gateway_troubleshooting_message_runtime` | Gateway | Message-flow, cron/heartbeat, node, and browser-tool troubleshooting. |
| `oc_gateway_trusted_proxy_auth` | Gateway | Delegating Gateway auth to a trusted identity-aware reverse proxy. |

No new entry point is created by this sub-plan (the series hub already covers the threshold).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links to satisfy G7/G8 (each new note must RECEIVE ≥1; verify in DB at augment, add at execute):

- **`entry_openclaw_docs.md`** → all 5 notes (primary anti-island guarantee; the 5 rows above).
- **`areas/code_repos/repo_openclaw_gateway.md`** → `oc_gateway_tools_invoke_http_api`, `oc_gateway_troubleshooting_process_config`, `oc_gateway_trusted_proxy_auth` (code→docs cross-link; verified exists).
- **`areas/code_repos/repo_openclaw_security.md`** → `oc_gateway_trusted_proxy_auth`, `oc_gateway_tools_invoke_http_api` (security boundary / deny list; verified exists).
- **`resources/term_dictionary/term_openclaw.md`** → `oc_gateway_trusted_proxy_auth` or the troubleshooting cluster (code↔docs, W3; verified exists).
- **`resources/term_dictionary/term_reverse_proxy.md`** → `oc_gateway_trusted_proxy_auth` (term→doc backlink; verified exists).

## Pacing Rules (inherited from master)

Cap dynamic-workflow fan-out at ~30 agents/run (this sub-plan = 5 notes, single wave — well within cap). Embed manifests in the script. `git pull --rebase --autostash origin main` before committing; commit per sub-plan / per wave; `git push origin main` immediately after each commit; no Claude co-author trailer. Reindex incrementally after the wave (`bash scripts/update_notes_database.sh`); verify `note_links` populated + 0 broken links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` (this file) | 🟢 DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | 🟢 DONE (xref-augment 2026-06-21 — per-note mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | 🟢 DONE — READY (9/9, 2026-06-21) |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

## Augmentation Report (2026-06-21)

**Scope of this pass (xref-augment):** built and LOCKED the per-note Related Notes Mapping at the **raised floors** (≥8 term_dictionary terms · ≥10 code_snippets · ≥10 docs per note, PLUS relevant `repo_openclaw*` + sibling `oc_*`), re-reading all three source pages (`gateway/tools-invoke-http-api`, `gateway/troubleshooting`, `gateway/trusted-proxy-auth`) under `inbox/openclaw_docs/` to relevance-select (not pad) each link. Replaced the prior loose "Candidate Cross-References" section with `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`; updated the Summary Statistics cross-ref line and the G4 gate row to the raised floors.


| Note | Terms | Snippets | Docs (existing / planned-sibling) | Repos | Floors met (≥8t/≥10s/≥10d) |
|---|---:|---:|---|---:|---|
| `oc_gateway_tools_invoke_http_api` | 8 | 11 | 10 (8 / 2) | 3 | ✅ |
| `oc_gateway_troubleshooting_process_config` | 8 | 10 | 10 (8 / 2) | 3 | ✅ |
| `oc_gateway_troubleshooting_auth_connectivity` | 8 | 10 | 11 (8 / 3) | 3 | ✅ |
| `oc_gateway_troubleshooting_message_runtime` | 8 | 10 | 10 (7 / 3) | 3 | ✅ |
| `oc_gateway_trusted_proxy_auth` | 9 | 11 | 10 (7 / 3) | 2 | ✅ |



**New-term candidates:** NONE. The xref re-read surfaced no genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing note. Page vocabulary that is OpenClaw-specific (`trusted-proxy auth`, `/tools/invoke`, operator scopes / `x-openclaw-scopes`, device-auth v2, hard deny list, stability bundle) stays in the `oc_*` notes per the master "OpenClaw vocab = `oc_*` docs, not `term_*`" design decision. Generic vocabulary that appears (HSTS, OIDC, SAML, RCE, WAF, CDN, systemd, launchd, OOM, zero-trust) is described in prose and linked to the nearest EXISTING term where one exists (HSTS → `term_tls`; OIDC/SAML → `term_oauth`/`term_authentication`; RCE → `term_sandbox`; WAF → `term_waf`; CDN → `term_cdn`). **Best-fit glossary if any future capture were needed:** the agentic/LLM-dev `acronym_glossary_*.md` — but expected = none.

**Other 15-section augmentation status (inherited, verified present):** Section Coverage Map ✅ (every source H2/H3 mapped, no orphan), Split Decisions ✅ (troubleshooting → notes 2/3/4 with rationale), Density Re-Assessment ✅ (all ≤2500w/≤400L/≤6cb), Validation Scripts incl. G5 ghost-detect ✅, Per-Phase G1–G8 gate table ✅, Inlinks (existing→new) ✅, Undigested Terms Plan ✅ (0 new terms, with disposition table), Term-Note Authoring Requirements ✅ (N/A — 0 terms — with inherited master mandate), Entry Point Decision ✅ (inherited — `entry_openclaw_docs` CREATED at W1 for the >30-note series; this sub-plan contributes 5 Gateway rows). Documentation-Note Authoring Spec is inherited from the master Format Definition (derived from existing `cc_*`/`pi_*` doc corpora: `## Overview` opener, source-mirrored H2/H3, `## Related Notes` with relevance statements, `## References`, bold `**Source**`/`**Last Updated**`/`**Status**` footer).

**Collision/dedup audit (generalized to ALL planned notes, term_dictionary AND documentation/):** All 5 planned `oc_gateway_*` slugs are NEW (no `resources/documentation/openclaw/` notes exist yet; `entry_openclaw_docs` is the only planned-but-absent doc-side note). None duplicates an existing `term_*` note — the concepts (`/tools/invoke` endpoint, trusted-proxy auth, the three troubleshooting clusters) have no existing substantive term or doc home; existing terms (`term_reverse_proxy`, `term_authentication`, `term_api_gateway`, etc.) are LINKED, not recreated. 0 too-general slugs (all are scoped `oc_gateway_<specific-topic>`); 0 removals.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review of the augmented plan. 9 mandatory checkpoints:

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step ≥8 terms + floors | **PASS** | `## Per-Note Related Notes Mapping (LOCKED …)` present; every note has ≥8 terms, ≥10 snippets, ≥10 docs, each rendered as `- [Name](relpath.md) — what; relevance: why THIS note` (relevance statement on every link). Per-note: 8t/11s/10d, 8t/10s/10d, 8t/10s/11d, 8t/10s/10d, 9t/11s/10d. ≥1 entry-point back-link inherited via `entry_openclaw_docs` (Inlinks + Entry Point Decision). |
| CP2 | 9-GATE present (G1–G6 + G8) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table has G1 format, G2 grounding, G3 density+coverage, G4 cross-ref (raised floors), G5 ghost-detect + DB-verify, G6 broken-link fix, G7 + G8 discoverability/anti-island. Single execution phase → one gate table covers it (M≥N). |
| CP4 | Size | **PASS** | 5 planned notes (≤30); single wave, well within the 30-note plan cap and the ~30-agent fan-out cap. |
| CP5 | Format derived | **PASS** | Format Definition inherited from master, DERIVED from existing `cc_*`/`pi_*` doc corpora (`## Overview` opener — not `## Definition`; source-mirrored H2/H3; `## Related Notes`; `## References`; bold footer; forbidden-field list). Matches the actual target-dir-analog convention, not invented. |
| CP6 | Density | **PASS** | Density Re-Assessment: all 5 ≤2500w / ≤400L / ≤6cb. Troubleshooting (5,714w) split into notes 2/3/4 by symptom cluster; trusted-proxy (2,512w) kept single (one coherent auth mode) with compression plan. No unaddressed borderline note. |
| CP7 | Sources measured | **PASS** | Source table measured 2026-06-20 (1,072 / 5,714 / 2,512 words); re-read this pass confirms the magnitudes — troubleshooting is the dense 21-H2 page (3-way split correct), the other two are single-note. No >1.5× under-estimate. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (0 new terms, with per-vocabulary disposition table); `## Term-Note Authoring Requirements` present (N/A for 0 terms, inherits the multi-source-research + format mandate from master). Plan does not inline-author any term; all term interaction is LINK-existing. |
| CP8f | Slug specificity / collision audit | **PASS** | Collision/dedup audit (Augmentation Report) generalized to ALL 5 planned notes across term_dictionary AND documentation/: all NEW, all specifically scoped (`oc_gateway_<topic>`), 0 duplicates of existing term/doc notes, 0 too-general slugs, 0 removals/renames. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` covers all 5 new notes with ≥1 outside-folder inbound link each (primary: `entry_openclaw_docs` → all 5; plus `repo_openclaw_gateway`/`repo_openclaw_security`/`term_openclaw`/`term_reverse_proxy` code↔docs backlinks). G8 anti-island gate in the phase table; inlinks are a gated EXECUTE phase, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
