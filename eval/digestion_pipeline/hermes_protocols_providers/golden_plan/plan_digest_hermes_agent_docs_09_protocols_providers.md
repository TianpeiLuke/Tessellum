---
title: Hermes Agent Docs Digestion — Sub-Plan 09 — Protocols & Provider Integration
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/
pages:
  - user-guide/features/mcp.md
  - user-guide/features/acp.md
  - user-guide/features/api-server.md
  - user-guide/features/provider-routing.md
  - user-guide/features/fallback-providers.md
  - user-guide/features/credential-pools.md
  - user-guide/features/subscription-proxy.md
---

# Sub-Plan 09: Protocols & Provider Integration

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP09's note
> filenames/BBs/coverage/term-captures are defined.

## Scope

The protocol surfaces by which Hermes connects to the outside world plus the provider-resilience
stack: **MCP** (connect TO external tool servers AND run Hermes AS an MCP server), **ACP** (run Hermes
inside ACP editors — VS Code/Zed/JetBrains), the **OpenAI-compatible API server** (serve the agent over
HTTP), the **subscription proxy** (serve raw model inference through a Nous Portal OAuth sub), and the
three-layer provider stack — **provider routing** (OpenRouter sub-provider selection), **fallback
providers** (cross-provider failover), and **credential pools** (same-provider multi-key rotation).
Source = 7 mirrored pages in `inbox/hermes_agent_docs/` (all substantive). **P1 / foundational** —
concepts here (MCP, ACP, fallback/credential-pool/provider-routing) are referenced by SP01 (quickstart
next-layer), SP02 (config provider/credential blocks), SP14 (providers), SP15 (provider guides), and
SP18 (provider-runtime / acp-internals).

## Content Strategy

- **One BB per note.** `mcp.md` mixes a concept/config arc and a filtering/serving arc → split into 2.
  `api-server.md` mixes an endpoint data-model arc and a setup/auth/deployment arc → split into 2. The
  other 5 pages are each one cohesive BB → 1 note each.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the
  provider CATALOG + per-provider auth details (SP14 `integrations/providers`, SP15 provider guides);
  the `auxiliary.*` / `provider_routing:` / `fallback_providers:` / `credential_pool_strategies:`
  CONFIG BLOCKS as they appear in `configuration.md` (SP02 owns the config-file reference — SP09 owns
  the CONCEPT/procedure, SP02 owns the config-key catalog; bidirectional link); OAuth-over-SSH walkthrough
  (SP15 guide); Open WebUI / Matrix proxy setup (SP12/SP11 messaging); cron/delegation provider inheritance
  (SP06 owns cron/delegation, SP09 documents the fallback inheritance only); developer internals
  (`acp-internals`, `provider-runtime`, `tools-runtime` → SP18).
- **Collision (augment): `term_mcp.md` + `term_acp_agent_client_protocol.md` (both active) own the MCP/ACP CONCEPTS** — the
  planned `hermes_mcp_concept_config` / `hermes_acp_editor_integration` are user-facing
  config/integration PROCEDURE+concept notes (a different BB scope: how to USE the protocol in Hermes,
  not what the protocol IS) → LINK both terms, do NOT recreate.
- **Collision (augment): `term_api_gateway.md` (125L active) is the generic microservices API-gateway
  pattern, NOT the Hermes OpenAI-compatible API server** — a master-listed LIKE false-positive
  (`messaging gateway ≠ term_api_gateway`). The planned `hermes_api_server_*` notes are NOT a dup; do
  NOT link the unrelated term.
  technique, NOT Hermes credential pools** — master-listed LIKE false-positive
  (`credential pool ≠ term_credential_stuffing`). The planned `term_credential_pool` + `hermes_credential_pools`
  are NOT dups; do NOT link the unrelated term.

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/features/mcp.md | 3868 | 42 | MIXED concept+procedure | 2 (split) |
| user-guide/features/api-server.md | 2608 | 22 | MIXED model+procedure | 2 (split) |
| user-guide/features/fallback-providers.md | 2582 | 18 | model | 1 |
| user-guide/features/credential-pools.md | 1351 | 12 | concept | 1 |
| user-guide/features/acp.md | 1292 | 14 | procedure | 1 |
| user-guide/features/subscription-proxy.md | 865 | 11 | procedure | 1 |
| user-guide/features/provider-routing.md | 649 | 15 | procedure | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **9 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_mcp_concept_config.md` | concept | mcp §What MCP gives you, §Quick start, §Catalog (one-click install, tool selection at install, trust model, manifest version compat, `${ENV_VAR}` substitution, updating selection/manifest), §Two kinds of MCP servers (stdio/HTTP/OAuth-authenticated incl. PKCE + DCR pitfalls + config auto-reload race), §mTLS / client certificates, §Basic configuration reference (common keys, minimal stdio/HTTP), §Built-in presets | ~1700 | What MCP is in Hermes and how to wire servers: stdio vs remote HTTP vs OAuth 2.1 (PKCE/DCR) MCP servers, the curated one-click catalog + per-tool install checklist + trust model, `${ENV_VAR}` substitution, mTLS client certs, the `mcp_servers` config keys, and `--preset` shortcuts. |
| 2 | `hermes_mcp_filtering_serving.md` | procedure | mcp §How Hermes registers MCP tools (prefix scheme), §MCP utility tools (capability-aware), §Per-server filtering (disable / include / exclude / precedence / utility filtering / full example / filtered-out behavior), §Runtime behavior (discovery, dynamic tool discovery, reloading, toolsets), §Security model, §Example use cases, §Troubleshooting, §Parallel Tool Calls, §MCP Sampling Support, §Running Hermes as an MCP server (when/quick-start/client config/available tools/event system/options/how-it-works/limits) | ~1700 | Operating MCP at runtime: the `mcp_<server>_<tool>` prefix scheme, capability-aware utility wrappers, per-server include/exclude filtering + precedence as a security control, dynamic tool discovery + `/reload-mcp`, parallel tool calls, MCP sampling (server-requested inference), and running `hermes mcp serve` so other agents use Hermes' 10-tool messaging bridge. |
| 3 | `hermes_acp_editor_integration.md` | procedure | acp §What Hermes exposes in ACP mode, §Installation (+browser tools setup), §Launching the ACP server, §Editor setup (VS Code / Zed / JetBrains), §Registry manifest, §Configuration and credentials, §Session behavior, §Working directory behavior, §Approvals (+session-scoped auto-approval 4-tier), §Troubleshooting | ~1200 | Running Hermes as an ACP server inside editors: the curated `hermes-acp` toolset, `.[acp]` install + optional browser bootstrap, `hermes acp` / `uvx` launch, VS Code / Zed registry / JetBrains setup, in-memory ACP session manager, editor-cwd binding, and the 4-tier approval model (allow once/session/always/deny). |
| 4 | `hermes_api_server_endpoints.md` | model | api-server §intro, §Endpoints (chat/completions, responses incl. previous_response_id / named conversations / GET/DELETE, models, capabilities, health, health/detailed), §Runs API (create/poll/events SSE/stop/approval), §Jobs API (CRUD/pause/resume/run), §Sessions API (REST table + fork/chat/stream), §Skills and toolsets discovery, §Long-term memory scoping (`X-Hermes-Session-Key`), §System Prompt Handling | ~1500 | The OpenAI-compatible API surface as a data model: `/v1/chat/completions` + `/v1/responses` (stateful via `previous_response_id` / named conversations), the runs API (SSE progress + stop + approval), jobs CRUD, sessions-over-REST, skills/toolsets discovery, `X-Hermes-Session-Key` memory scoping, and system-prompt layering. |
| 5 | `hermes_api_server_setup_auth.md` | procedure | api-server §Quick Start (enable / start gateway / connect frontend), §Authentication, §Configuration (env vars + config.yaml), §Security Headers, §CORS, §Compatible Frontends, §Multi-User Setup with Profiles, §Limitations, §Proxy Mode | ~1100 | Standing up and securing the API server: `API_SERVER_*` env enablement, bearer-token auth (required on every deploy incl. loopback), CORS allowlisting, security headers, the compatible-frontend matrix, per-profile multi-user isolation on separate ports, limitations, and gateway proxy mode (`GATEWAY_PROXY_URL`). |
| 6 | `hermes_provider_routing.md` | procedure | provider-routing §intro, §Configuration, §Options (sort / only / ignore / order / require_parameters / data_collection), §Practical Examples, §How It Works (extra_body.provider mapping), §Default Behavior, §Provider Routing vs Fallback Models | ~700 | OpenRouter sub-provider routing: the `provider_routing:` config block (sort by price/throughput/latency, only/ignore/order whitelisting, require_parameters, data_collection), how it maps onto OpenRouter's `extra_body.provider`, default behavior, and how it differs from cross-provider fallback. |
| 7 | `hermes_fallback_providers.md` | model | fallback-providers §intro (3 resilience layers), §Primary Model Fallback (config / supported providers / custom endpoint / when triggers / behavior / per-turn / examples / where works), §Auxiliary Task Fallback (tasks / auto-detection chains / configuring / provider options / direct endpoint override), §Auxiliary Capacity-Error Fallback (4-layer ladder / per-task fallback_chain / quota error strings), §Context Compression Fallback, §Delegation Provider Override, §Cron Job Providers, §Summary | ~1700 | The cross-provider resilience model: per-turn primary-model failover on rate-limit/server/auth errors, the supported-provider matrix, independent auxiliary-task provider chains (vision/compression/web-extract/etc.), the capacity-error fallback ladder (primary aux → fallback_chain → main agent → re-raise), compression degrade-to-no-summary, and delegation/cron provider inheritance. |
| 8 | `hermes_credential_pools.md` | concept | credential-pools §intro (vs fallback), §How It Works (rotation decision flow), §Quick Start, §Interactive Management, §CLI Commands, §Rotation Strategies, §Error Recovery (429/402/401/exhausted), §Custom Endpoint Pools, §Auto-Discovery (sources + reference-only secrets), §Delegation & Subagent Sharing, §Thread Safety, §Architecture, §Storage (auth.json shape) | ~1300 | Same-provider multi-key rotation: registering multiple keys/OAuth tokens per provider, the rotation decision flow (429 retry-once / 402 immediate / 401 refresh-then-rotate / exhausted → fallback), the 4 rotation strategies, per-error cooldowns, auto-discovery + reference-only secret storage in `auth.json`, subagent pool sharing, and thread-safe selection. |
| 9 | `hermes_subscription_proxy.md` | procedure | subscription-proxy §intro (vs API server), §Quick Start (portal login / proxy start / point app), §Available providers, §Check status, §Allowed paths, §Configuring OpenViking, §Configuring Karakeep, §Exposing on LAN, §Rate limits, §Architecture, §Future providers | ~750 | The credential-attaching pass-through proxy: `hermes portal` OAuth login + `hermes proxy start` to serve a Nous Portal / xAI subscription as an OpenAI-compatible endpoint, the allowed-path whitelist, OpenViking/Karakeep client config, LAN exposure caveats, tier rate limits, and the minimal no-transformation request flow. |

**SP09 totals:** 9 notes · procedure 5 · model 2 · concept 2.
7 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 9 · procedure 5 · model 2 · concept 2.
- Source: 7 digested pages (~13.2K words) → ~11.7K words of notes (modest compression via link-outs to
  SP14/SP15 provider catalog + SP02 config-key reference).
- BB mix: procedure 56%, model 22%, concept 22%.
- New term captures (SP09 owns): 4 (`term_provider_routing`, `term_fallback_provider`,

## Section Coverage Map

```
mcp.md (3868w)
├── intro / What MCP gives you ──────────────────────────── → Note 1
├── Quick start ────────────────────────────────────────── → Note 1
├── Catalog (install / tool-selection / trust / manifest-version / ${ENV_VAR} subst / updating) → Note 1
├── Two kinds of MCP servers (stdio / HTTP / OAuth-authenticated incl. PKCE+DCR+auto-reload race) → Note 1 (oauth-over-ssh deep→SP15)
├── mTLS / client certificates / Basic configuration reference / Built-in presets → Note 1 (config-key catalog→SP02)
├── How Hermes registers MCP tools / MCP utility tools ──── → Note 2
├── Per-server filtering (disable/include/exclude/precedence/utility/full example/filtered-out) → Note 2
├── Runtime behavior (discovery / dynamic / reloading / toolsets) / Security model → Note 2
├── Example use cases / Troubleshooting / Parallel Tool Calls / MCP Sampling Support → Note 2
└── Running Hermes as an MCP server (all sub-sections) ───── → Note 2 (use-mcp guide→SP17)
acp.md (1292w) ── ALL sections ──────────────────────────── → Note 3 (acp-internals/tools-runtime/provider-runtime→SP18; browser→SP08)
api-server.md (2608w)
├── intro / Endpoints (all) / Runs API / Jobs API / Sessions API / Skills+toolsets discovery / X-Hermes-Session-Key / System Prompt Handling → Note 4 (open-webui→SP12; honcho→SP05)
├── Quick Start / Authentication / Configuration / Security Headers / CORS → Note 5
├── Compatible Frontends / Multi-User Setup with Profiles / Limitations → Note 5 (profiles→SP04; env-vars ref→SP21)
└── Proxy Mode ─────────────────────────────────────────── → Note 5 (Matrix proxy→SP11)
provider-routing.md (649w) ── ALL sections ──────────────── → Note 6 (nous-portal→SP14; fallback→Note 7)
fallback-providers.md (2582w) ── ALL sections ───────────── → Note 7 (provider catalog→SP14; provider guides→SP15; cron→SP06; delegation→SP06; compression internals→SP18)
credential-pools.md (1351w) ── ALL sections ─────────────── → Note 8 (secrets/bitwarden→SP03; delegation→SP06; nous-portal→SP14)
subscription-proxy.md (865w) ── ALL sections ────────────── → Note 9 (nous-portal→SP14; open-webui→SP12; api-server contrast→Note 5)
```

No source H2/H3 orphaned. All 7 pages fully covered; provider-catalog / per-provider-auth / config-key
detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| mcp.md (3868w, 42 code) | Note 1 (concept+config: what MCP is, catalog, server kinds, mTLS, config keys, presets) + Note 2 (procedure: prefix/filtering/runtime/sampling/serving) | >2500w → 2 notes; two arcs — declaring/configuring MCP servers (concept) vs operating/filtering/serving MCP at runtime (procedure). Each cluster curated to ≤6 load-bearing code blocks (42 source blocks → keep canonical YAML per concept). |
| api-server.md (2608w, 22 code) | Note 4 (model: the endpoint surface — chat/responses/runs/jobs/sessions/discovery/headers) + Note 5 (procedure: enable/auth/CORS/multi-user/proxy-mode) | >2500w → 2 notes; the endpoint REST surface is a distinct `model` BB (data shapes, request/response schemas) separated from the setup/security/deployment procedure. |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note / slug | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_mcp_concept_config`, `hermes_mcp_filtering_serving` | `term_mcp.md` (active), `term_mcp_gateway.md` (active) | **NOT a dup** — terms own the MCP *concept*; these are Hermes-specific config/runtime *procedure+concept* notes | CREATE; LINK both terms. |
| `hermes_acp_editor_integration` | `term_acp_agent_client_protocol.md` (active) | **NOT a dup** — term owns the ACP *concept*; this is the Hermes-editor *integration procedure* | CREATE; LINK `term_acp_agent_client_protocol`. |
| `hermes_api_server_endpoints`, `hermes_api_server_setup_auth` | `term_api_gateway.md` (125L active) | **NOT a dup** — that term is the generic microservices *API-gateway pattern* (read 2026-06-15: "single entry point … microservices architecture"), unrelated to the OpenAI-compatible API server (master LIKE false-positive `messaging gateway ≠ term_api_gateway`) | CREATE; do NOT link the unrelated term. |
| `hermes_provider_routing`, `hermes_fallback_providers`, `hermes_subscription_proxy` | no substantive term/doc note covers these procedures; no `hermes_agent/` doc notes exist yet | NEW | CREATE. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
**0 substantive same-concept duplicates** (the MCP/ACP term hits are concept-vs-procedure-scope LINKs;
the api_gateway / credential_stuffing / aws_sdk_credential_chain hits are confirmed-unrelated LIKE
false-positives, read at augmentation). New `hermes_agent/` folder → no doc-doc collisions (SP01 not yet
executed; intra-series links resolve at finalization, verified by G5/G8). Owned-slug pre-flight (Step
4e.2) re-run 2026-06-15: all 4 ABSENT, all 4 confirmed NEW.

## Owned-Term Specificity + Collision Verdicts (per master directive)

| Owned slug | DF | Specificity verdict | Collision verdict | Capture |
|---|---:|---|---|---|
| `term_provider_routing` | 7 | OK — domain-scoped (OpenRouter sub-provider selection); not the bare word "routing" (which the audit shows maps to `term_cap_routing`/`term_cs_contact_routing`, different concepts) | NEW (ABSENT); `term_provider_plugin` is a different concept → LINK | YES (full) |
| `term_fallback_provider` | 8 | OK — singular concept noun; literature's standard term for the failover-target provider | NEW (ABSENT); no `term_*fallback*` exists; `term_failover` is the generic mechanism → LINK | YES (full) |
| `term_pkce` | 12 | OK — canonical acronym (Proof Key for Code Exchange); acronym-first naming per file-naming rule | NEW (ABSENT); `term_oauth_token`/`term_authentication` are broader → LINK | YES (full) |

**`term_mcp` + `term_acp_agent_client_protocol` EXIST (active) → LINK, do NOT capture** (master directive). No specificity
renames needed (all 4 owned slugs already scope-specific). No removals (all 4 ABSENT + concept-distinct).

## Per-Note Related Notes Mapping (FINALIZED — ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **FOUR-FLOOR STANDARD set 2026-06-19 (master directive, supersedes the earlier ≥8 term + ≥5 code-repo +
> ≥10 doc "+bonus snippets" state and the 2026-06-14 ≥8 term + ≥8 snippet + ≥5 doc floor):** each note's
> `## Related Notes` carries — all relevancy-selected to that note's actual content and each rendered as
> `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   2026-06-19** — the `repo_hermes_agent_*` source-code repo notes whose modules implement what THIS doc note
>   documents (all 13 exist active: `repo_hermes_agent`, `_agent_core`, `_cli`, `_gateway_messaging`,
>   `_mcp_toolsets`, `_tools`, `_skills`, `_plugins`, `_providers_adapters`, `_cron`, `_acp`,
>   `_trajectory_research`, `_tui_gateway`).
> - **≥10 SNIPPET notes** (`../../code_snippets/snippet_hermes_agent_*.md`) — **COUNTED FLOOR (promoted
>   2026-06-19** — the implementation-layer Hermes code snippets whose CODE this doc note documents, selected
>   by the planned note's content (517 active `snippet_hermes_agent_*` in the corpus).
> - **≥10 DOCUMENTATION notes** (`../../documentation/`) — a mix of sibling `hermes_*` notes in THIS series
>   (resolve at finalization per G5/G8 — allowed to not-yet-exist; DB count is 0 today) + analogous
>
> are allowed un-verified — they're created later in this series and resolve at finalization (G5/G8); they are
> explicitly tagged `(+fin)`. SP09's own 4 Phase-0 term captures (`term_pkce`, `term_provider_routing`,
> `term_fallback_provider`, `term_credential_pool`) are ABSENT today (captured in Phase 0 BEFORE the digest
> terms are listed as `(+Phase 0)` ADDITIONS (relevant but not relied on for the ≥8 active floor). Other SPs'
> Hermes-specific forward-ref terms (`term_tool_gateway`→SP05, `term_nous_portal`→SP14,
> `term_messaging_gateway`→SP11, `term_skills_hub`→SP05, `term_openrouter`→SP14) are ADDITIONAL forward-refs
> `(+fin)`, NOT counted to the ≥8 floor (they don't exist yet).

**Note 1 `hermes_mcp_concept_config`** (concept)
- Terms (8 active): [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: this page IS the Hermes MCP-client config surface. [term_mcp_gateway](../../term_dictionary/term_mcp_gateway.md) — MCP aggregation/proxy; relevance: the catalog + `mcp_servers` block aggregate many MCP servers behind one agent. [term_oauth_token](../../term_dictionary/term_oauth_token.md) — bearer/refresh token; relevance: remote HTTP servers use `auth: oauth`, tokens cached at `~/.hermes/mcp-tokens/`. [term_oauth](../../term_dictionary/term_oauth.md) — OAuth 2.1 authorization framework; relevance: the §OAuth-authenticated HTTP servers flow (discovery, DCR, token exchange/refresh, step-up). [term_authentication](../../term_dictionary/term_authentication.md) — identity proof; relevance: API key / OAuth / mTLS are the three server auth modes. [term_tls](../../term_dictionary/term_tls.md) — Transport Layer Security; relevance: §mTLS client certs (`client_cert`/`client_key`) feed the TLS handshake. [term_tls_pinning](../../term_dictionary/term_tls_pinning.md) — cert-binding hardening; relevance: same mutual-TLS trust surface as the client-certificate config. [term_agent_harness](../../term_dictionary/term_agent_harness.md) — the agent runtime; relevance: the harness discovers + registers MCP tools at startup. (+ [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md), [term_tool_registry](../../term_dictionary/term_tool_registry.md); +Phase 0: term_pkce — PKCE auth flow used by remote OAuth servers; +fin: term_tool_gateway, term_nous_portal)
- Code-Repos (5): [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP client + toolset registration module; relevance: implements `mcp_servers` parsing, stdio/HTTP/OAuth connect, catalog install. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — credential/auth resolution; relevance: resolves `${ENV_VAR}` substitution, OAuth tokens, and mTLS cert paths for MCP servers. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes mcp` / `hermes mcp install` / `hermes mcp login`; relevance: the catalog picker, install checklist, and OAuth login commands this page documents. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool registry the MCP tools land in; relevance: registered MCP tools join the same registry as native tools. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties the MCP config-load path into agent startup.
- Docs (10): [hermes_mcp_filtering_serving](hermes_mcp_filtering_serving.md) — runtime/filtering counterpart; relevance: same protocol, runtime half (+fin). [hermes_config_files_precedence](hermes_config_files_precedence.md) — `config.yaml` key reference; relevance: SP02 owns the `mcp_servers` key catalog this page links out to (+fin). [hermes_acp_editor_integration](hermes_acp_editor_integration.md) — ACP protocol sibling; relevance: the other editor-facing protocol surface (+fin). [hermes_credential_pools](hermes_credential_pools.md) — credential rotation; relevance: shared OAuth-token/secret resolution (+fin). [hermes_subscription_proxy](hermes_subscription_proxy.md) — OAuth-attaching proxy; relevance: shares the `hermes portal`/auth.json OAuth machinery (+fin). [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — Claude Code MCP overview; relevance: closest analogue agent-tool MCP concept doc. [cc_mcp_transports](../claude_code/cc_mcp_transports.md) — stdio/SSE/HTTP transports; relevance: the same two-kinds-of-servers transport split. [cc_mcp_authentication](../claude_code/cc_mcp_authentication.md) — MCP OAuth auth; relevance: analogous remote-server OAuth flow. [cc_mcp_installation_scopes](../claude_code/cc_mcp_installation_scopes.md) — install scoping; relevance: analogous to the catalog one-click install + scope model. [cc_managed_mcp_configuration](../claude_code/cc_managed_mcp_configuration.md) — managed MCP config; relevance: analogous declarative server-config surface.
- Snippets (≥10): [tools_mcp_client](../../code_snippets/snippet_hermes_agent_tools_mcp_client.md) — MCP client connect; relevance: implements stdio/HTTP connect for `mcp_servers` entries. [tools_mcp_lifecycle](../../code_snippets/snippet_hermes_agent_tools_mcp_lifecycle.md) — connect/discover/register lifecycle; relevance: the startup tool-discovery + registration this page describes. [tools_mcp_oauth](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth.md) — MCP OAuth flow; relevance: the `auth: oauth` discovery/DCR/PKCE/token-exchange path. [tools_mcp_oauth_manager](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth_manager.md) — token cache/refresh; relevance: `~/.hermes/mcp-tokens/<server>.json` 0o600 cache + refresh + step-up. [cli_mcp_config](../../code_snippets/snippet_hermes_agent_cli_mcp_config.md) — `mcp_servers` config parsing; relevance: parses `command`/`args`/`url`/`headers`/`client_cert`/`tools` keys + `${ENV_VAR}` substitution. [providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — credential/env resolution; relevance: resolves `${ENV_VAR}` and stdio `env` passthrough for MCP servers. [core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source order; relevance: where `~/.hermes/.env` API keys / OAuth tokens come from for MCP auth. [tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: registered MCP tools land in the same registry as native tools. [tools_credential_files](../../code_snippets/snippet_hermes_agent_tools_credential_files.md) — cert/key file resolution; relevance: resolves the mTLS `client_cert`/`client_key` PEM-path shapes (single/2-tuple/3-tuple). [gw_config_load](../../code_snippets/snippet_hermes_agent_gw_config_load.md) — config.yaml loader; relevance: loads `~/.hermes/config.yaml` (incl. `mcp_servers`) at startup. [gw_config_schema](../../code_snippets/snippet_hermes_agent_gw_config_schema.md) — config schema; relevance: validates the `mcp_servers` block shape this page's reference table defines.

**Note 2 `hermes_mcp_filtering_serving`** (procedure)
- Terms (8 active): [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: this page operates MCP at runtime (prefix/filter/serve). [term_mcp_gateway](../../term_dictionary/term_mcp_gateway.md) — MCP aggregation; relevance: `hermes mcp serve` makes Hermes itself the gateway bridging 10 messaging tools. [term_tool_registry](../../term_dictionary/term_tool_registry.md) — tool namespace; relevance: the `mcp_<server>_<tool>` prefix scheme + per-server include/exclude shape the registry. [term_subagent](../../term_dictionary/term_subagent.md) — delegated agent; relevance: other MCP clients (incl. agents) consume Hermes' served tools. [term_multi_agent_systems](../../term_dictionary/term_multi_agent_systems.md) — agent-to-agent topology; relevance: `mcp serve` lets Claude Code/Cursor use Hermes' messaging bridge. [term_function_calling](../../term_dictionary/term_function_calling.md) — tool/function invocation; relevance: MCP sampling lets servers request inference incl. tool rounds. [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable session store; relevance: the serve event bridge polls Hermes' session DB. [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: dynamic discovery + `/reload-mcp` re-register tools into the running harness. (+ [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md), [term_webhook](../../term_dictionary/term_webhook.md) — `notifications/tools/list_changed` is a server-push akin to a webhook; +fin: term_messaging_gateway, term_tool_gateway)
- Code-Repos (5): [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP runtime/filter/serve module; relevance: implements prefix registration, include/exclude filtering, dynamic discovery, `mcp serve`. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool registry + toolsets; relevance: the `mcp-<server>` runtime toolset + utility-tool wrappers live here. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — messaging bridge; relevance: the 10 served tools (`conversations_list`, `messages_send`, …) wrap the gateway's `send_message` + session DB. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes mcp serve` / `/reload-mcp`; relevance: the serve entrypoint + reload slash command. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — sampling inference handler; relevance: MCP sampling (`sampling/createMessage`) routes back through the core conversation loop.
- Docs (10): [hermes_mcp_concept_config](hermes_mcp_concept_config.md) — config counterpart; relevance: same protocol, config half (+fin). [hermes_api_server_endpoints](hermes_api_server_endpoints.md) — served-surface analogue; relevance: serving Hermes' tools over a protocol mirrors serving the agent over HTTP (+fin). [hermes_acp_editor_integration](hermes_acp_editor_integration.md) — another served protocol; relevance: ACP also exposes a curated tool surface to external clients (+fin). [hermes_config_files_precedence](hermes_config_files_precedence.md) — `tools.include/exclude` keys; relevance: SP02 owns the filter-config key reference (+fin). [hermes_subscription_proxy](hermes_subscription_proxy.md) — pass-through serving; relevance: another "serve a Hermes capability to outside clients" surface (+fin). [cc_mcp_overview](../claude_code/cc_mcp_overview.md) — MCP overview; relevance: analogous MCP runtime model. [cc_mcp_server_management](../claude_code/cc_mcp_server_management.md) — server lifecycle/reload; relevance: analogous to `/reload-mcp` + discovery. [cc_mcp_tool_search](../claude_code/cc_mcp_tool_search.md) — tool selection/filtering; relevance: analogous tool-namespace control. [cc_built_in_tools](../claude_code/cc_built_in_tools.md) — built-in tool surface; relevance: served MCP tools sit alongside built-ins. [cc_sdk_connect_mcp_servers](../claude_code/cc_sdk_connect_mcp_servers.md) — SDK MCP wiring; relevance: analogous programmatic MCP registration.
- Snippets (≥10): [tools_mcp_notifications](../../code_snippets/snippet_hermes_agent_tools_mcp_notifications.md) — `notifications/tools/list_changed` handler; relevance: the lock-protected dynamic tool re-discovery this page documents. [tools_mcp_call](../../code_snippets/snippet_hermes_agent_tools_mcp_call.md) — prefixed tool invocation; relevance: calls `mcp_<server>_<tool>` and (when enabled) parallel-batch concurrent tool runs. [tools_mcp_retry](../../code_snippets/snippet_hermes_agent_tools_mcp_retry.md) — MCP tool retry; relevance: runtime resilience around MCP tool calls. [tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — registry + prefix scheme; relevance: implements `mcp_<server>_<tool>` namespacing + include/exclude filter application. [toolsets_definitions](../../code_snippets/snippet_hermes_agent_toolsets_definitions.md) — toolset definitions; relevance: the `mcp-<server>` runtime toolset created per contributing server. [toolsets_materialize](../../code_snippets/snippet_hermes_agent_toolsets_materialize.md) — toolset materialization; relevance: materializes the per-server toolset (skips empty/fully-filtered servers). [mcp_serve_hermes_as_server](../../code_snippets/snippet_hermes_agent_mcp_serve_hermes_as_server.md) — `hermes mcp serve`; relevance: runs Hermes AS a stdio MCP server with the event bridge. [mcp_serve_tool_surface](../../code_snippets/snippet_hermes_agent_mcp_serve_tool_surface.md) — the 10 served tools; relevance: `conversations_list`/`messages_send`/`events_poll`/… messaging-bridge surface. [tools_mcp_lifecycle](../../code_snippets/snippet_hermes_agent_tools_mcp_lifecycle.md) — discovery/reload lifecycle; relevance: `/reload-mcp` + utility-tool capability-aware registration. [gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — session DB lifecycle; relevance: the serve event bridge polls Hermes' session store for new messages.

**Note 3 `hermes_acp_editor_integration`** (procedure)
- Terms (8 active): [term_json_rpc](../../term_dictionary/term_json_rpc.md) — JSON-RPC over stdio; relevance: ACP speaks JSON-RPC; Hermes logs to stderr to keep stdout clean. [term_subagent](../../term_dictionary/term_subagent.md) — delegated agent; relevance: the curated `hermes-acp` toolset includes `delegate_task`. [term_human_in_the_loop](../../term_dictionary/term_human_in_the_loop.md) — human approval gate; relevance: dangerous terminal commands route back as editor approval prompts. [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: ACP `list/load/resume/fork` reuse Hermes' normal persistence paths. [term_sandbox_backend](../../term_dictionary/term_sandbox_backend.md) — execution sandbox; relevance: file/terminal/execute_code tools run relative to the editor cwd. [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: the underlying `AIAgent` powers each ACP session. [term_function_calling](../../term_dictionary/term_function_calling.md) — tool/function invocation; relevance: ACP renders tool activity (file diffs, terminal) as the agent's tool calls. [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — editor-native coding agent; relevance: ACP makes Hermes behave like an editor-native coding agent. (+ [term_acp_agent_client_protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — the ACP concept term (active); relevance: this note is the Hermes-editor ACP *integration procedure* that LINKs the existing concept term, [term_tool_registry](../../term_dictionary/term_tool_registry.md) — the curated toolset is a filtered registry view, [term_mcp](../../term_dictionary/term_mcp.md) — the sibling stdio editor/agent protocol; +fin: term_tool_gateway)
- Code-Repos (5): [repo_hermes_agent_acp](../../../areas/code_repos/repo_hermes_agent_acp.md) — the ACP adapter module; relevance: implements `hermes acp`/`hermes-acp`/`acp_adapter`, in-memory session manager, approval bridge, registry manifest. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `hermes-acp` toolset; relevance: the curated file/terminal/web/memory/skills toolset exposed in ACP mode. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes acp --setup/--check/--setup-browser`; relevance: the launch + browser-bootstrap commands. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `AIAgent` + approval semantics; relevance: ACP options map onto Hermes' internal allow-once/session/always approval cache. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider resolution; relevance: ACP inherits the normal runtime provider/credential resolver.
- Docs (10): [hermes_mcp_filtering_serving](hermes_mcp_filtering_serving.md) — served-tool sibling; relevance: ACP and MCP-serve both expose curated tool surfaces (+fin). [hermes_mcp_concept_config](hermes_mcp_concept_config.md) — MCP config; relevance: ACP and MCP are the two external-protocol surfaces (+fin). [hermes_api_server_endpoints](hermes_api_server_endpoints.md) — HTTP agent surface; relevance: third way to drive the agent from outside (+fin). [hermes_config_files_precedence](hermes_config_files_precedence.md) — `~/.hermes/config.yaml`; relevance: ACP reuses the same config/env/skills/state.db (+fin). [hermes_fallback_providers](hermes_fallback_providers.md) — provider resilience; relevance: ACP inherits the configured fallback chain (+fin). [cc_vs_code_extension](../claude_code/cc_vs_code_extension.md) — VS Code agent integration; relevance: direct analogue to the VS Code ACP setup. [cc_jetbrains_plugin](../claude_code/cc_jetbrains_plugin.md) — JetBrains plugin; relevance: direct analogue to the JetBrains ACP path. [cc_vs_code_ide_mcp_server](../claude_code/cc_vs_code_ide_mcp_server.md) — IDE-as-server; relevance: editor↔agent over a local protocol, like ACP-over-stdio. [cc_sdk_tool_approval_handling](../claude_code/cc_sdk_tool_approval_handling.md) — approval handling; relevance: analogous to the 4-tier ACP approval model. [cc_permission_modes_overview](../claude_code/cc_permission_modes_overview.md) — permission modes; relevance: allow-once/session/always parallels CC permission scopes.
- Snippets (≥10): [acp_entry](../../code_snippets/snippet_hermes_agent_acp_entry.md) — `hermes acp` entrypoint; relevance: the launch command + stderr-only logging this page documents. [acp_server_init](../../code_snippets/snippet_hermes_agent_acp_server_init.md) — ACP server init; relevance: boots the JSON-RPC-over-stdio ACP server. [acp_server_session_methods](../../code_snippets/snippet_hermes_agent_acp_server_session_methods.md) — session list/load/resume/fork; relevance: the ACP session methods reusing Hermes persistence. [acp_server_prompt](../../code_snippets/snippet_hermes_agent_acp_server_prompt.md) — prompt/turn handling; relevance: drives each `AIAgent` turn inside an ACP session. [acp_session](../../code_snippets/snippet_hermes_agent_acp_session.md) — in-memory session manager; relevance: the editor-cwd-bound in-memory ACP session state. [acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — `hermes-acp` toolset; relevance: registers the curated file/terminal/web/memory/skills toolset. [acp_tools_permission](../../code_snippets/snippet_hermes_agent_acp_tools_permission.md) — approval bridge; relevance: maps the 4-tier allow-once/session/always/deny model to editor prompts. [acp_registry_manifest](../../code_snippets/snippet_hermes_agent_acp_registry_manifest.md) — registry manifest; relevance: the editor registry-manifest (VS Code/Zed/JetBrains) this page configures. [acp_auth](../../code_snippets/snippet_hermes_agent_acp_auth.md) — ACP credential resolution; relevance: ACP inherits the normal provider/credential resolver (§Configuration and credentials). [acp_server_module_helpers](../../code_snippets/snippet_hermes_agent_acp_server_module_helpers.md) — ACP server helpers; relevance: working-directory binding + browser-tools bootstrap helpers (`--setup-browser`).

**Note 4 `hermes_api_server_endpoints`** (model)
- Terms (8 active): [term_rest](../../term_dictionary/term_rest.md) — REST/HTTP resource model; relevance: the whole surface is a REST data model (chat/responses/runs/jobs/sessions). [term_sse](../../term_dictionary/term_sse.md) — Server-Sent Events; relevance: streaming responses + runs `/events` + `/chat/stream` emit SSE event types. [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: `/v1/responses` stores chains via `previous_response_id`; sessions API persists over REST. [term_multimodal](../../term_dictionary/term_multimodal.md) — multi-input model; relevance: inline `image_url`/`input_image` parts on chat/responses/sessions payloads. [term_computer_vision](../../term_dictionary/term_computer_vision.md) — image understanding; relevance: the multimodal image path feeds vision analysis. [term_idempotency](../../term_dictionary/term_idempotency.md) — request dedup; relevance: `Idempotency-Key` cached 5 min for dedup. [term_caching](../../term_dictionary/term_caching.md) — response cache; relevance: stored responses use LRU eviction (max 100). [term_lru_cache](../../term_dictionary/term_lru_cache.md) — least-recently-used eviction; relevance: the exact eviction policy for stored responses. (+ [term_subagent](../../term_dictionary/term_subagent.md), [term_webhook](../../term_dictionary/term_webhook.md) — run events are push-style; +Phase 0: term_pkce; +fin: term_nous_portal, term_tool_gateway)
- Code-Repos (5): [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the gateway that hosts the API server; relevance: `hermes gateway` exposes the OpenAI-compatible routes, runs/jobs/sessions APIs. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `AIAgent` + conversation loop; relevance: each endpoint dispatches into the core agent turn (incl. `gateway_session_key`). [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — skills/toolsets discovery; relevance: `/v1/skills` + `/v1/toolsets` enumerate the registry. [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — jobs CRUD backing; relevance: `/api/jobs/*` mirrors `hermes cron` shape. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties the API-server routing into the agent runtime.
- Docs (10): [hermes_api_server_setup_auth](hermes_api_server_setup_auth.md) — setup/auth counterpart; relevance: same server, deployment half (+fin). [hermes_mcp_filtering_serving](hermes_mcp_filtering_serving.md) — `/v1/toolsets` source; relevance: the served toolsets are the MCP/runtime toolsets (+fin). [hermes_subscription_proxy](hermes_subscription_proxy.md) — contrasting server; relevance: agent-backend vs raw-model passthrough (+fin). [hermes_session_search_storage](hermes_session_search_storage.md) — session storage; relevance: sessions API reads/writes the session store (+fin). [hermes_sessions_lifecycle_resume](hermes_sessions_lifecycle_resume.md) — fork/resume semantics; relevance: `/api/sessions/{id}/fork` matches CLI `/branch` (+fin). [cc_headless_mode](../claude_code/cc_headless_mode.md) — programmatic agent surface; relevance: analogous "drive the agent over an API" model. [cc_sdk_session_management_api](../claude_code/cc_sdk_session_management_api.md) — session REST/API; relevance: analogous sessions-over-API surface. [cc_sdk_streaming_output](../claude_code/cc_sdk_streaming_output.md) — streaming output; relevance: analogous SSE token/tool-progress streaming. [cc_sdk_stream_text_and_tool_calls](../claude_code/cc_sdk_stream_text_and_tool_calls.md) — streamed tool calls; relevance: matches `function_call`/`function_call_output` stream items. [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — hosting agent sessions; relevance: analogous to runs API for detached progress.
- Snippets (≥10): [gw_platform_api_server_routes](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_routes.md) — route table; relevance: the `/v1/chat/completions` + `/v1/responses` + runs/jobs/sessions/skills/toolsets endpoint surface. [gw_platform_api_server_connect](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_connect.md) — API-server connect/boot; relevance: stands up the OpenAI-compatible server inside the gateway. [gw_run_helpers](../../code_snippets/snippet_hermes_agent_gw_run_helpers.md) — runs API helpers; relevance: create/poll/SSE-events/stop/approval for the runs API. [gw_runner_session_key](../../code_snippets/snippet_hermes_agent_gw_runner_session_key.md) — session-key derivation; relevance: `X-Hermes-Session-Key` long-term-memory scoping. [gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — session lifecycle; relevance: the sessions-over-REST table + fork/chat/stream persistence. [gw_stream_consumer](../../code_snippets/snippet_hermes_agent_gw_stream_consumer.md) — SSE stream consumer; relevance: streaming responses + runs `/events` + `/chat/stream` event emission. [gw_stream_backpressure](../../code_snippets/snippet_hermes_agent_gw_stream_backpressure.md) — stream backpressure; relevance: SSE flow control for long-running streamed turns. [core_conversation_loop_api_dispatch](../../code_snippets/snippet_hermes_agent_core_conversation_loop_api_dispatch.md) — API→agent dispatch; relevance: each endpoint dispatches into the core agent turn (incl. `gateway_session_key`). [gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — session state store; relevance: backs the sessions API + `previous_response_id`/named-conversation chains. [gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — health endpoints; relevance: `/health` + `/health/detailed` + capabilities reporting.

**Note 5 `hermes_api_server_setup_auth`** (procedure)
- Terms (8 active): [term_authentication](../../term_dictionary/term_authentication.md) — identity proof; relevance: bearer-token auth required on every deploy incl. loopback. [term_oauth_token](../../term_dictionary/term_oauth_token.md) — bearer token; relevance: `API_SERVER_KEY` is the bearer presented in `Authorization`. [term_rest](../../term_dictionary/term_rest.md) — HTTP surface; relevance: setup stands up the REST endpoints behind one auth. [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — forwarding proxy; relevance: proxy mode (`GATEWAY_PROXY_URL`) forwards to another gateway. [term_proxy_pattern](../../term_dictionary/term_proxy_pattern.md) — proxy design pattern; relevance: the split-deployment relay (Docker Matrix → host agent). [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable sessions; relevance: per-profile isolation gives each user a separate session/memory store. [term_idempotency](../../term_dictionary/term_idempotency.md) — request dedup; relevance: `Idempotency-Key` is an allowed CORS request header. [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent runtime; relevance: the API server gives full toolset access incl. terminal — the security warning. (+ [term_oauth](../../term_dictionary/term_oauth.md), [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md); +fin: term_nous_portal, term_tool_gateway)
- Code-Repos (5): [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway hosting the API server; relevance: `hermes gateway` boots the API server, applies auth middleware + security headers + CORS. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes profile create` / `hermes -p <profile> gateway`; relevance: per-profile multi-user setup on separate ports. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider boot; relevance: the API server needs a configured provider before it is useful. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — agent turn dispatch; relevance: authenticated requests dispatch into the core agent. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties env-var enablement (`API_SERVER_*`) into startup.
- Docs (10): [hermes_api_server_endpoints](hermes_api_server_endpoints.md) — endpoint surface; relevance: same server, data-model half (+fin). [hermes_subscription_proxy](hermes_subscription_proxy.md) — contrasting proxy; relevance: the page explicitly contrasts API server vs proxy auth (+fin). [hermes_mcp_concept_config](hermes_mcp_concept_config.md) — config surface; relevance: shares the `~/.hermes/.env` + config model (+fin). [hermes_config_files_precedence](hermes_config_files_precedence.md) — env-var/config reference; relevance: SP02/SP21 own the `API_SERVER_*` env catalog this links out to (+fin). [hermes_credential_pools](hermes_credential_pools.md) — provider credentials; relevance: per-profile providers feed credential pools (+fin). [cc_authentication](../claude_code/cc_authentication.md) — agent auth; relevance: analogous bearer/token auth setup. [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network/TLS controls; relevance: analogous CORS/security-header hardening. [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: direct analogue to gateway proxy mode. [cc_sdk_hosting_provisioning_and_scaling](../claude_code/cc_sdk_hosting_provisioning_and_scaling.md) — hosting/scaling; relevance: analogous multi-user deployment topology. [cc_sdk_secure_deployment_principles](../claude_code/cc_sdk_secure_deployment_principles.md) — secure deploy; relevance: analogous "auth required on every deploy" guidance.
- Snippets (≥10): [gw_platform_api_server_middleware](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_middleware.md) — auth/CORS/security-header middleware; relevance: the bearer-token auth + CORS allowlist + security headers this page configures. [gw_platform_api_server_connect](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_connect.md) — server boot; relevance: `API_SERVER_*` env enablement + gateway boot. [gw_platform_api_server_routes](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_routes.md) — protected routes; relevance: the REST routes that sit behind the single bearer auth. [gw_runner_provider_boot](../../code_snippets/snippet_hermes_agent_gw_runner_provider_boot.md) — provider boot; relevance: a configured provider is required before the API server is useful. [gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — per-profile sessions; relevance: per-profile multi-user isolation gives each user a separate session store. [gw_run_helpers](../../code_snippets/snippet_hermes_agent_gw_run_helpers.md) — run dispatch; relevance: authenticated requests dispatch into runs. [gw_runner_acl](../../code_snippets/snippet_hermes_agent_gw_runner_acl.md) — access control; relevance: the full-toolset-access security warning + per-profile ACL. [gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — outbound proxy forward; relevance: gateway proxy mode (`GATEWAY_PROXY_URL`) forwards to another gateway. [gw_start_gateway_main](../../code_snippets/snippet_hermes_agent_gw_start_gateway_main.md) — `hermes gateway` main; relevance: the gateway entrypoint that starts the API server on a chosen port. [gw_runner_init](../../code_snippets/snippet_hermes_agent_gw_runner_init.md) — runner init; relevance: per-profile runner init on separate ports for multi-user setup.

**Note 6 `hermes_provider_routing`** (procedure)
- Terms (8 active): [term_model_router](../../term_dictionary/term_model_router.md) — routes requests across models/providers; relevance: provider routing is exactly OpenRouter sub-provider selection. [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider adapter pattern; relevance: routing config flows through the provider adapter to `extra_body.provider`. [term_load_balancer](../../term_dictionary/term_load_balancer.md) — distributes load by policy; relevance: `sort: price/throughput/latency` ranks sub-providers like a policy-driven balancer. [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: routing picks which provider serves the LLM request. [term_model_catalog](../../term_dictionary/term_model_catalog.md) — model/provider inventory; relevance: `only`/`ignore`/`order` whitelist against the OpenRouter provider catalog. [term_failover](../../term_dictionary/term_failover.md) — switch on failure; relevance: §Provider Routing vs Fallback contrasts sub-provider routing with cross-provider failover. [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — throttle handling; relevance: throughput/latency sort and `order` fallbacks mitigate provider rate caps. [term_haproxy](../../term_dictionary/term_haproxy.md) — load-balancer exemplar; relevance: concrete analogue of priority-order + health-aware routing. (+ [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md); +Phase 0: term_provider_routing — the OpenRouter sub-provider-selection concept this note documents; +fin: term_nous_portal, term_openrouter)
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider registry/dispatch; relevance: implements mapping `provider_routing.*` → `extra_body.provider` on every OpenRouter call. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `AIAgent` construction; relevance: routing params (`providers_allowed`/`providers_order`/`provider_sort`) are passed when creating the agent. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — config load; relevance: `~/.hermes/config.yaml` `provider_routing:` loaded at CLI/gateway startup. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway-mode load; relevance: same routing config applied when the gateway starts. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties routing into the provider boot path.
- Docs (10): [hermes_fallback_providers](hermes_fallback_providers.md) — cross-provider failover; relevance: the explicit "routing vs fallback" contrast (+fin). [hermes_credential_pools](hermes_credential_pools.md) — same-provider rotation; relevance: third resilience layer below routing/fallback (+fin). [hermes_config_files_precedence](hermes_config_files_precedence.md) — config keys; relevance: SP02 owns the `provider_routing:` key catalog (+fin). [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) — model/provider config; relevance: routing sits in the same provider-config arc (+fin). [hermes_subscription_proxy](hermes_subscription_proxy.md) — Portal routing note; relevance: Portal traffic still respects per-model routing (+fin). [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: analogous "pick which model/provider" control. [cc_restrict_model_selection](../claude_code/cc_restrict_model_selection.md) — model allowlist; relevance: analogous to `only`/`ignore` whitelisting. [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — LLM gateway routing; relevance: analogous provider-routing layer. [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — LiteLLM multi-provider; relevance: direct analogue of multi-provider routing config. [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — gateway config; relevance: analogous provider-routing-through-a-gateway setup.
- Snippets (≥10): [cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: where `provider_routing:` config is read and attached to provider construction. [providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: dispatches to the OpenRouter adapter carrying routing params. [providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base interface; relevance: the adapter contract that maps routing → request body. [core_anthropic_adapter_client](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_client.md) — adapter client construction; relevance: pattern for passing provider-selection params at client build. [gw_runner_provider_boot](../../code_snippets/snippet_hermes_agent_gw_runner_provider_boot.md) — gateway provider boot; relevance: same routing config applied when the gateway starts. [core_runtime_helpers_switch_client](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_switch_client.md) — client switch; relevance: rebuilds the client with routing options on provider change. [cli_main_provider_flows](../../code_snippets/snippet_hermes_agent_cli_main_provider_flows.md) — CLI provider flows; relevance: `~/.hermes/config.yaml` provider/routing load at CLI startup. [core_auxiliary_proxy_url](../../code_snippets/snippet_hermes_agent_core_auxiliary_proxy_url.md) — proxy/base-url resolution; relevance: provider base-URL/endpoint resolution underneath routing. [plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter provider plugin; relevance: implements the `extra_body.provider` mapping (`sort`/`only`/`ignore`/`order`/`require_parameters`/`data_collection`). [plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: registers OpenRouter + the other adapters routing selects among.

**Note 7 `hermes_fallback_providers`** (model)
- Terms (8 active): [term_model_failover](../../term_dictionary/term_model_failover.md) — switch model/provider on failure; relevance: primary-model fallback is exactly cross-provider model failover. [term_failover](../../term_dictionary/term_failover.md) — failure switchover; relevance: the page's whole resilience model. [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider adapter; relevance: the 40-row supported-provider matrix maps to adapters. [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — 429 handling; relevance: fallback triggers on rate limits after retries; capacity errors bypass the explicit-provider gate. [term_circuit_breaker](../../term_dictionary/term_circuit_breaker.md) — trip-and-switch; relevance: per-turn at-most-once fallback prevents cascading failover loops. [term_exponential_backoff](../../term_dictionary/term_exponential_backoff.md) — retry spacing; relevance: fallback activates "after exhausting retry attempts." [term_multimodal](../../term_dictionary/term_multimodal.md) — vision/aux tasks; relevance: auxiliary vision chain has its own provider resolution. [term_progressive_summarization](../../term_dictionary/term_progressive_summarization.md) — context compression; relevance: compression aux degrades to no-summary if all layers fail. (+ [term_llm](../../term_dictionary/term_llm.md), [term_model_router](../../term_dictionary/term_model_router.md); +Phase 0: term_fallback_provider, term_credential_pool, term_provider_routing; +fin: term_nous_portal, term_openrouter)
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider/error resolution; relevance: implements credential resolution, client rebuild, supported-provider matrix, capacity-error classification. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `run_agent.py` error recovery + in-place client swap; relevance: per-turn fallback activation, retry-counter reset, conversation preservation. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes fallback` manager + `fallback_providers:` config; relevance: the interactive picker + YAML persistence/migration. [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — cron provider inheritance; relevance: cron agents inherit the configured fallback chain. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — auxiliary-task tools; relevance: vision/web-extract/compression aux tasks have independent provider chains.
- Docs (10): [hermes_credential_pools](hermes_credential_pools.md) — same-provider rotation tried first; relevance: layer 1 of the 3-layer resilience stack (+fin). [hermes_provider_routing](hermes_provider_routing.md) — sub-provider routing; relevance: the explicit routing-vs-fallback contrast (+fin). [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) — aux/compression config; relevance: SP02 owns the `auxiliary.*` / `fallback_providers:` key catalog (+fin). [hermes_config_files_precedence](hermes_config_files_precedence.md) — config keys; relevance: where `fallback_providers:` lives (+fin). [hermes_subscription_proxy](hermes_subscription_proxy.md) — Portal as fallback target; relevance: `nous` is a supported fallback provider (+fin). [hermes_cron_scheduled_tasks](hermes_cron_scheduled_tasks.md) — cron provider override; relevance: SP06 owns cron; this page documents the inheritance only (+fin). [cc_fallback_models](../claude_code/cc_fallback_models.md) — fallback models; relevance: direct analogue of primary-model fallback. [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — 429/5xx/quota errors; relevance: analogous error taxonomy that triggers fallback. [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: fallback chain is an ordered model/provider selection. [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — gateway failover; relevance: analogous cross-provider routing/failover layer.
- Snippets (≥10): [core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — fallback activation; relevance: per-turn primary-model failover after retries exhausted. [core_error_classifier_taxonomy](../../code_snippets/snippet_hermes_agent_core_error_classifier_taxonomy.md) — error taxonomy; relevance: classifies rate-limit/server/auth/capacity errors that trigger fallback. [core_error_classifier_provider_maps](../../code_snippets/snippet_hermes_agent_core_error_classifier_provider_maps.md) — provider error maps; relevance: the supported-provider matrix + capacity-error string maps. [core_error_classifier_backoff](../../code_snippets/snippet_hermes_agent_core_error_classifier_backoff.md) — backoff policy; relevance: fallback activates "after exhausting retry attempts." [core_conversation_loop_retry_handler](../../code_snippets/snippet_hermes_agent_core_conversation_loop_retry_handler.md) — retry handler; relevance: per-turn at-most-once fallback + retry-counter reset preventing cascading loops. [core_runtime_helpers_switch_client](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_switch_client.md) — in-place client swap; relevance: rebuilds the provider client mid-turn while preserving the conversation. [core_auxiliary_auth_resolution](../../code_snippets/snippet_hermes_agent_core_auxiliary_auth_resolution.md) — auxiliary auth resolution; relevance: independent auxiliary-task (vision/compression/web-extract) provider chains. [core_auxiliary_diagnostics](../../code_snippets/snippet_hermes_agent_core_auxiliary_diagnostics.md) — auxiliary diagnostics; relevance: capacity-error fallback ladder diagnostics (primary aux → fallback_chain → main → re-raise). [core_conversation_loop_rate_limit_recovery](../../code_snippets/snippet_hermes_agent_core_conversation_loop_rate_limit_recovery.md) — 429 recovery; relevance: the rate-limit recovery path that hands off to fallback. [gw_runner_cron](../../code_snippets/snippet_hermes_agent_gw_runner_cron.md) — cron provider inheritance; relevance: cron agents inherit the configured fallback chain (§Cron Job Providers).

**Note 8 `hermes_credential_pools`** (concept)
- Terms (8 active): [term_round_robin](../../term_dictionary/term_round_robin.md) — cyclic selection; relevance: one of the 4 rotation strategies (`fill_first`/`round_robin`/`least_used`/`random`). [term_failover](../../term_dictionary/term_failover.md) — switch on exhaustion; relevance: when all pool keys exhaust, fall through to `fallback_model`. [term_model_failover](../../term_dictionary/term_model_failover.md) — provider switchover; relevance: pools are the same-provider layer tried before cross-provider model failover. [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — 429/402 handling; relevance: rotation decision flow keys off 429 retry-once / 402 immediate / 401 refresh. [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: pools rotate API keys AND OAuth tokens; 401 triggers token refresh. [term_authentication](../../term_dictionary/term_authentication.md) — credential auth; relevance: auto-discovery seeds pools from env/OAuth/Claude-Code/PKCE sources. [term_subagent](../../term_dictionary/term_subagent.md) — delegated agent; relevance: parent's pool is shared with `delegate_task` subagents (per-task leasing). [term_thread_binding_policy](../../term_dictionary/term_thread_binding_policy.md) — concurrency control; relevance: a threading lock guards all pool mutations for concurrent sessions. (+ [term_provisioned_concurrency](../../term_dictionary/term_provisioned_concurrency.md), [term_aws_sdk_credential_chain](../../term_dictionary/term_aws_sdk_credential_chain.md) — analogous ordered credential lookup; +Phase 0: term_credential_pool, term_fallback_provider, term_provider_routing; +fin: term_nous_portal)
- Code-Repos (5): [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — `agent/credential_pool.py` + `runtime_provider.py`; relevance: the pool manager (storage, selection, rotation, cooldowns) + pool-aware resolution. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes auth` commands; relevance: `auth_commands.py` add/list/remove/reset + interactive wizard + strategy selection. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `run_agent.py` error recovery; relevance: 429/402/401 → pool rotation → fallback handoff. [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — subagent/delegation sharing; relevance: spawned children inherit the parent pool for rate-limit resilience. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties auto-discovery seeding into startup, `auth.json` storage.
- Docs (10): [hermes_fallback_providers](hermes_fallback_providers.md) — cross-provider layer; relevance: pools are tried first, then fallback (+fin). [hermes_provider_routing](hermes_provider_routing.md) — sub-provider routing; relevance: third layer of the resilience stack (+fin). [hermes_subscription_proxy](hermes_subscription_proxy.md) — Portal OAuth; relevance: Portal OAuth seeds pools; proxy shares `auth.json` (+fin). [hermes_config_files_precedence](hermes_config_files_precedence.md) — `credential_pool_strategies:` keys; relevance: strategies stored in config.yaml not auth.json (+fin). [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — secret storage; relevance: SP03 owns Bitwarden/Vault/keyring reference-only secret storage (+fin). [cc_authentication](../claude_code/cc_authentication.md) — auth/credentials; relevance: analogous credential management. [cc_sdk_credential_and_filesystem_controls](../claude_code/cc_sdk_credential_and_filesystem_controls.md) — credential controls; relevance: analogous credential-source resolution + reference-only secrets. [cc_server_and_usage_limit_errors](../claude_code/cc_server_and_usage_limit_errors.md) — 429/quota errors; relevance: the error taxonomy that drives rotation. [cc_amazon_bedrock_model_config](../claude_code/cc_amazon_bedrock_model_config.md) — multi-credential provider; relevance: analogous multi-key provider configuration. [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — auth refresh issues; relevance: analogous 401 refresh-then-rotate handling.
- Snippets (≥10): [core_credential_pool_dataclass](../../code_snippets/snippet_hermes_agent_core_credential_pool_dataclass.md) — pool dataclass; relevance: the per-provider pool model (keys/OAuth tokens, strategy, cooldowns). [core_credential_pool_entry](../../code_snippets/snippet_hermes_agent_core_credential_pool_entry.md) — pool entry; relevance: per-key entry state (429/402/401 cooldown + exhausted flags). [core_credential_pool_selection](../../code_snippets/snippet_hermes_agent_core_credential_pool_selection.md) — rotation decision flow; relevance: the 4 strategies (`fill_first`/`round_robin`/`least_used`/`random`) + thread-safe selection. [core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — auto-discovery seeding; relevance: seeds pools from env/OAuth/Claude-Code/PKCE sources + reference-only secrets. [core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source order; relevance: the discovery sources feeding the pool. [cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — `hermes auth` add/remove; relevance: the interactive add/list/remove/reset wizard. [cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — `auth.json` storage; relevance: reference-only secret storage shape this page documents. [core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — pool→fallback handoff; relevance: when all pool keys exhaust, fall through to `fallback_model`. [cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider resolution; relevance: resolves which provider's pool a request uses (incl. custom-endpoint pools). [cli_auth_provider_state](../../code_snippets/snippet_hermes_agent_cli_auth_provider_state.md) — provider auth state; relevance: 401 refresh-then-rotate token state for OAuth-token pool entries.

**Note 9 `hermes_subscription_proxy`** (procedure)
- Terms (8 active): [term_oauth_token](../../term_dictionary/term_oauth_token.md) — refreshing bearer; relevance: the proxy attaches a refreshing Portal OAuth bearer to every upstream request. [term_oauth](../../term_dictionary/term_oauth.md) — OAuth flow; relevance: `hermes portal` runs the Nous Portal OAuth login. [term_authentication](../../term_dictionary/term_authentication.md) — credential attach; relevance: the proxy ignores the client bearer and attaches the real credential. [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — forwarding server; relevance: the proxy is a credential-attaching pass-through forwarder. [term_proxy_pattern](../../term_dictionary/term_proxy_pattern.md) — proxy design pattern; relevance: minimal no-transformation forward of `POST /v1/chat/completions`. [term_rest](../../term_dictionary/term_rest.md) — OpenAI-compatible HTTP; relevance: only an allowed-path whitelist (`/v1/chat/completions`, `/v1/embeddings`, …) is forwarded. [term_embedding](../../term_dictionary/term_embedding.md) — embeddings endpoint; relevance: `/v1/embeddings` is an allowed forwarded path (OpenViking embedding model). [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — tier limits; relevance: the Portal tier's RPM/TPM limits apply across the whole single-bearer proxy. (+ [term_llm](../../term_dictionary/term_llm.md), [term_cross_region_proxy](../../term_dictionary/term_cross_region_proxy.md) — analogous forwarding-proxy topology; +Phase 0: term_pkce; +fin: term_nous_portal)
- Code-Repos (5): [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `hermes proxy start/status/providers` + `hermes portal`; relevance: implements `hermes_cli/proxy/` server + `UpstreamAdapter` registry + OAuth login. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — upstream credential mint/refresh; relevance: resolves + refreshes the Portal/xAI bearer the proxy attaches. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — HTTP serving + SSE forward; relevance: the verbatim request forward + unchanged SSE streaming path. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — runtime helpers; relevance: shares the client-switch/credential-resolution runtime used per request. [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — implementation root; relevance: ties `auth.json` refresh-token storage into the proxy.
- Docs (10): [hermes_api_server_setup_auth](hermes_api_server_setup_auth.md) — contrasting server; relevance: the page explicitly contrasts proxy vs API-server auth/use-case (+fin). [hermes_api_server_endpoints](hermes_api_server_endpoints.md) — agent-backend surface; relevance: agent-as-backend vs raw-model passthrough (+fin). [hermes_fallback_providers](hermes_fallback_providers.md) — provider resilience; relevance: `nous`/`xai` are also fallback providers (+fin). [hermes_credential_pools](hermes_credential_pools.md) — OAuth storage; relevance: shares the `~/.hermes/auth.json` OAuth/refresh-token store (+fin). [hermes_config_files_precedence](hermes_config_files_precedence.md) — config/auth files; relevance: where Portal logins live (+fin). [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: direct analogue of a credential-attaching upstream proxy. [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — LLM gateway; relevance: analogous "front a subscription/endpoint for many clients." [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — LiteLLM proxy; relevance: analogous OpenAI-compatible passthrough proxy. [cc_authentication](../claude_code/cc_authentication.md) — auth; relevance: analogous OAuth-login + credential attach. [cc_network_tls_and_access](../claude_code/cc_network_tls_and_access.md) — network access; relevance: analogous LAN-exposure / no-auth-of-its-own caveat.
- Snippets (≥10): [cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — OAuth callback server; relevance: the `hermes portal` loopback OAuth login callback. [cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — login/logout; relevance: Portal OAuth login + credential persistence. [cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — `auth.json` store; relevance: the `~/.hermes/auth.json` refresh-token store the proxy reads. [cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider resolve; relevance: resolves the Portal/xAI upstream the proxy forwards to. [cli_auth_provider_state](../../code_snippets/snippet_hermes_agent_cli_auth_provider_state.md) — provider auth state; relevance: tracks the refreshing bearer state attached per request. [core_anthropic_adapter_oauth](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_oauth.md) — adapter OAuth refresh; relevance: mints/refreshes the OAuth bearer the proxy attaches. [core_runtime_helpers_switch_client](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_switch_client.md) — client/credential resolution; relevance: shared credential-resolution runtime used per proxied request. [gw_platform_api_server_connect](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_connect.md) — HTTP serving/forward; relevance: the verbatim request forward + unchanged SSE streaming path. [core_auxiliary_proxy_url](../../code_snippets/snippet_hermes_agent_core_auxiliary_proxy_url.md) — upstream URL resolution; relevance: resolves the allowed-path upstream base URL (`/v1/chat/completions`, `/v1/embeddings`, …). [gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — outbound forwarding; relevance: the minimal no-transformation pass-through forward to the upstream subscription.

`term_fallback_provider`, `term_credential_pool`) are ADDITIONS `(+Phase 0)`, captured before the digest notes
and NOT relied on for the active floor. Sibling `hermes_*` doc links (`hermes_config_files_precedence`,
`hermes_model_aux_provider_config`, `hermes_session_search_storage`, `hermes_sessions_lifecycle_resume`,
`hermes_security_skill_memory_settings`, `hermes_cron_scheduled_tasks`, and the in-SP09 siblings) are
intra-series forward-refs `(+fin)` that resolve in `resources/documentation/hermes_agent/` at finalization
active 2026-06-19) and as of 2026-06-19 are a **COUNTED floor (≥10 per note)**, promoted from the prior bonus
group.
**Placeholder/inactive slugs caught at finalization and kept out of the counted lists:**
`term_mutual_tls`, `term_concurrency`, `term_tool_use`, `term_retry`, `term_thread_safety`,
`term_data_privacy` (all DB-ABSENT 2026-06-19; substituted with active equivalents — `term_tls`/`term_tls_pinning`,
`term_thread_binding_policy`/`term_provisioned_concurrency`, `term_function_calling`/`term_tool_registry`,
`term_exponential_backoff`); `gw_session_key` (snippet ABSENT → `gw_runner_session_key`). Each note's list uses

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15; re-measured 2026-06-19 mirror c253b07)

Re-read all 7 source pages from `inbox/hermes_agent_docs/`; measured counts match the Source Pages
table (no >50% estimate misses). 2026-06-19 re-measure: mcp.md 3818→3868w / 43→42 code, fallback-providers.md
2470→2582w / 17→18 code; both projected notes (1 and 7) remain heavily link-out-compressed and well under
the ≤2500w / ≤6 code / ≤400 line caps — **no split triggered** by the growth (see Note 7 below). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 mcp-concept-config | concept | 1700 | ≤6 (curate from 42 short blocks; one canonical YAML per server kind/feature; tables in prose) | ✓ |
| 2 mcp-filtering-serving | procedure | 1700 | ≤6 (from filtering/sampling/serve blocks) | ✓ |
| 3 acp-editor-integration | procedure | 1200 | ≤6 (from 14; one canonical per editor) | ✓ |
| 4 api-server-endpoints | model | 1500 | ≤6 (from 22; one canonical request/response per endpoint family) | ✓ |
| 5 api-server-setup-auth | procedure | 1100 | ≤6 | ✓ |
| 6 provider-routing | procedure | 700 | ≤6 (curate from 15 short YAML; keep the option-canonical + mapping block) | ✓ |
| 7 fallback-providers | model | 1700 | ≤6 (curate from 18; keep config-shape + chain + summary; provider matrix in prose table) | ✓ |
| 8 credential-pools | concept | 1300 | ≤6 (from 12; keep decision-flow + strategies + auth.json shape) | ✓ |
| 9 subscription-proxy | procedure | 750 | ≤6 (from 11; keep portal/start/point-app + arch) | ✓ |

No further splits needed — all 9 notes are ≤2500w. mcp.md→2 and api-server.md→2 are the only splits.
Code-heavy pages (mcp 42, provider-routing 15) are curated to ≤6 load-bearing blocks per note, the rest
summarized in prose (kept blocks verbatim). The large fallback supported-provider matrix (~46 rows) is
kept as a prose markdown TABLE (not a code block) so it doesn't count against the ≤6 code cap. If any
note exceeds 350 lines during writing, STOP and split.

**fallback-providers.md 2470→2582w (crossed the 2500w raw-page threshold) — re-decision: NO SPLIT.**
The 2500w cap is per *planned note*, not per source page. The whole page is owned by a single note
(Note 7, model BB) projected at ~1700w — the +112w of growth (mostly added supported-provider matrix
rows + a couple of auxiliary-task clarifications) lands inside the parts the plan already PROSE-COMPRESSES
and LINK-ROUTES (the ~46-row provider matrix → SP14 catalog prose table; provider guides → SP15;
cron/delegation → SP06; compression internals → SP18; 18 code blocks curated to ≤6). The projected note
stays well under ≤2500w / ≤6 code / ≤400 lines after the growth → the existing single Note 7 still fits,
no split warranted. (mcp.md 3818→3868w stays >2500 and was already split into Notes 1+2 — unchanged.)

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it
IS, NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc** —
four-floor standard set 2026-06-19, all counted) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP09)

`term_mcp` + `term_acp_agent_client_protocol` EXIST (active) → LINK, do NOT capture. Each is captured in **Phase 0 via
`/tessellum-capture-term-note <term>` (NOT inline)** BEFORE the digest notes are written, so Related-Notes
Related Terms 8/10/12, glossary template, backlink expansion) are MANDATORY for all 4.

| Term slug | Concept | DF | Capture Phase | Stub or Full | Best-fit glossary | Source page |
|---|---|---:|---|---|---|---|
| `term_pkce` | OAuth 2.1 Proof Key for Code Exchange auth flow | 12 | Phase 0 | full | `acronym_glossary_security.md` | mcp.md §OAuth-authenticated HTTP servers |
| `term_provider_routing` | OpenRouter underlying-provider selection (sort/only/ignore/order) | 7 | Phase 0 | full | `acronym_glossary_llm.md` | provider-routing.md |
| `term_fallback_provider` | primary/aux cross-provider failover chain | 8 | Phase 0 | full | `acronym_glossary_llm.md` | fallback-providers.md |
| `term_credential_pool` | multi-key/OAuth-token rotation per provider (≠ credential_stuffing) | 6 | Phase 0 | full | `acronym_glossary_systems.md` | credential-pools.md |

| Existing term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_mcp`, `term_mcp_gateway`, `term_acp_agent_client_protocol` | LINK (do NOT recreate) | — | own the MCP/ACP concept; SP09 doc notes are USE-procedure scope. |
| `term_tool_gateway`, `term_skills_hub` | LINK only (forward-ref, +fin) | SP05 | referenced in MCP/ACP/api-server; concept home is SP05. |
| `term_nous_portal`, `term_openrouter` | LINK only (+fin) | SP14 | provider/portal billing concepts; captured by SP14. |
| `term_messaging_gateway` | LINK only (+fin) | SP11 | `mcp serve` messaging bridge; concept owned by SP11. |

### Renamed (general → specific)

— (specificity audit performed on all 4 owned slugs; **0 renames** — each is already scope-qualified:
`term_pkce` is the canonical acronym; `term_provider_routing` carries the `provider_` qualifier
(distinguishes it from bare `routing` → `term_cap_routing`/`term_cs_contact_routing`); `term_fallback_provider`
and `term_credential_pool` are scope-qualified compounds. See Owned-Term Specificity table above.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, lines, status) | Action |
|---|---|---|
| `term_mcp` (would duplicate) | `resources/term_dictionary/term_mcp.md` (active) | Not captured — LINK the existing term from the MCP doc notes. |
| `term_acp_agent_client_protocol` (would duplicate) | `resources/term_dictionary/term_acp_agent_client_protocol.md` (active) | Not captured — LINK the existing term from the ACP doc note. |
| `term_api_server` (would-be) | `term_api_gateway.md` (125L, active) is the UNRELATED generic gateway pattern | **No removal** — SP09 was never going to capture an api-server term; doc notes `hermes_api_server_*` created instead; `term_api_gateway` NOT linked. |

## Term-Note Authoring Requirements (Per Undigested Term — Inherited from `/tessellum-capture-term-note` canonical)

Every one of SP09's 4 owned terms MUST be authored via **`/tessellum-capture-term-note <term>`** (Phase 0,
ENRICHER_INPUTS non-interactive or interactive), NOT inline-authored within a digest note. The capture
skill enforces the requirements below; this plan invokes them.

### YAML Frontmatter (required fields)

```yaml
---
tags:
  - resource
  - terminology
  - <domain_tag_1>          # e.g. security (pkce), llm_infrastructure (provider_routing/fallback), systems (credential_pool)
  - <domain_tag_2>
keywords:
  - <ACRONYM or canonical name>
  - <full name>
  - <variant spellings>
topics:
  - <topic_1>
  - <topic_2>
language: markdown
date of note: 2026-06-15
status: active
building_block: concept       # MUST be concept for term notes
access_control_group: ["general"]
related_wiki: null            # external open-source docs; no Amazon wiki
---
```

### Required H1 + H2 sections (in order)

| Section | Required | Content |
|---|---|---|
| `# <ACRONYM> - <Full Name>` H1 | Yes | e.g. `# PKCE - Proof Key for Code Exchange` |
| `## Definition` | Yes | 1-2 paragraphs: what it is, what problem it solves, who uses it |
| `## Context` | Yes | Which systems/workflows use it (Hermes provider stack + the broader OAuth/LLM-infra ecosystem) |
| `## Key Characteristics` | Yes | Bullet list of distinctive properties + technical approach |
| `## Performance / Metrics` | Optional | Only if metrics found; omit otherwise |
| `## Related Terms` | Yes | **depth-scaled minimum vault term-note links** (8/10/12 by note depth) — INDEXED markdown link format `**[Term Name](term_X.md)** — one-line description`; ≥3 in-domain + ≥3 cross-domain |
| `## References` | Yes | EXTERNAL URLs ONLY (Hermes docs page, OAuth 2.1 RFC 7636 for PKCE, OpenRouter docs, Wikipedia); NO `term_*.md` links here |


The source doc that triggered the capture is ONE viewpoint. Every capture MUST research across multiple
sources (the digest page alone is single-source trapped scope → FAIL):

1. **External authoritative** (≥2 of): the official spec/RFC (PKCE → RFC 7636 / OAuth 2.1; provider_routing → OpenRouter routing docs; fallback/credential_pool → vendor resilience docs + Wikipedia "failover"/"high availability"), the canonical open-source documentation, Wikipedia.
2. **Vault cross-reference**: `/tessellum-search-notes <term>` AND DB query for in-domain + cross-domain related term notes (capture-term-note Steps 3d + 3e).

### Cross-Domain Diversity for Related Terms (8/10/12 minimum)

Per capture-term-note Step 3e, Related Terms MUST mix in-domain + cross-domain. Suggested anchors per owned term:
- `term_pkce`: in-domain `term_oauth_token`, `term_authentication`; cross-domain `term_mcp`, `term_acp_agent_client_protocol`, `term_credential_pool`, `term_provider_plugin`, `term_tls`, `term_session_persistence`.
- `term_provider_routing`: in-domain `term_provider_plugin`, `term_load_balancer`, `term_failover`; cross-domain `term_fallback_provider`, `term_llm`, `term_model_catalog`, `term_rate_limiting`, `term_round_robin`.
- `term_fallback_provider`: in-domain `term_failover`, `term_circuit_breaker`, `term_exponential_backoff`, `term_rate_limiting`; cross-domain `term_credential_pool`, `term_provider_routing`, `term_provider_plugin`, `term_progressive_summarization`.
- `term_credential_pool`: in-domain `term_round_robin`, `term_oauth_token`, `term_rate_limiting`, `term_failover`; cross-domain `term_fallback_provider`, `term_provider_routing`, `term_subagent`, `term_authentication`. **Do NOT relate to `term_credential_stuffing` (unrelated).**

### Math Notation, Fleeting-Content Guard, Glossary Entry, File Naming, Depth-Scaled Minimums, Backlink Expansion, Section Ordering, >200-Line Decomposition

All per the augment canonical Step 10.5d (inherited verbatim): MathJax for any formula; strip person
aliases / bare ETAs / dollar amounts; glossary entry = exact `**Full Name** / **Description** (4-5 sentences
max, no metrics, bold the key fact) / **Documentation** / **Wiki** / **Related**` template; file naming uses
the canonical acronym (`term_pkce`, not `term_proof_key_for_code_exchange`); depth tier sets Related-Terms
minimum (these are simple-to-moderate concepts → target 8-10); add 1-2 inbound backlinks (`grep -rl` plain
mentions) + 5-10 cross-domain term-note inlinks; Related Terms before References, footer last; if a note
exceeds 200 lines, decompose (procedure→`sop_*`, model/argument→`thought_*`). Acceptance fails on
single-source scope, <minimum Related Terms, no cross-domain diversity, no inlink expansion,
`term_*.md` in References, external URL in Related Terms, forbidden YAML field, `building_block`≠concept,
plain-text math, or overwriting a substantive existing note.

## Execution Phases (per-phase 8-GATE)

- **Phase 0 (owned term captures — runs FIRST):** `/tessellum-capture-term-note term_pkce`,
  `/tessellum-capture-term-note term_provider_routing`, `/tessellum-capture-term-note term_fallback_provider`,
  + backlink expansion. Reindex after the batch. GATE G1, G5 (the 4 new terms now exist for the digest
  notes' Related Notes), G6, G8.
- **Phase 1 (protocols, P1-hub pilot):** Notes 1, 2, 3. Pilot Note 1 (`hermes_mcp_concept_config`) first
  → reindex → verify format/ghost/in-degree BEFORE the rest. GATE G1–G8.
- **Phase 2 (API surface + proxy):** Notes 4, 5, 9. GATE G1–G8.
- **Phase 3 (provider resilience stack):** Notes 6, 7, 8. GATE G1–G8.
- **Phase 3b (inlinks):** add the inbound links from the table below (EXECUTED, gated — G8).

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim
for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify
every ref)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB ·
**G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}*.md; do python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}*.md; do grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder
for n in hermes_mcp_concept_config hermes_mcp_filtering_serving hermes_acp_editor_integration hermes_api_server_endpoints hermes_api_server_setup_auth hermes_provider_routing hermes_fallback_providers hermes_credential_pools hermes_subscription_proxy; do
# Owned-term existence (after Phase 0)
for t in term_pkce term_provider_routing term_fallback_provider term_credential_pool; do
```

## Entry Point Decision (inherited)

Contributes 9 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Protocols & Provider Integration" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP09 does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_mcp_toolsets.md` | → `hermes_mcp_concept_config`, `hermes_mcp_filtering_serving` | MCP toolset repo ↔ MCP usage docs |
| `repo_hermes_agent_acp.md` | → `hermes_acp_editor_integration` | ACP repo ↔ ACP editor-integration doc |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_api_server_endpoints`, `hermes_api_server_setup_auth` | gateway repo (hosts the API server) ↔ API-server docs |
| `repo_hermes_agent_providers_adapters.md` | → `hermes_provider_routing`, `hermes_fallback_providers`, `hermes_credential_pools`, `hermes_subscription_proxy` | provider/adapter repo ↔ provider-stack docs |
| `repo_hermes_agent.md` | → `hermes_mcp_concept_config`, `hermes_fallback_providers` | implementation root ↔ key protocol/provider usage |
| `term_mcp.md` | → `hermes_mcp_concept_config`, `hermes_mcp_filtering_serving` | concept term → Hermes MCP usage docs |
| `term_acp_agent_client_protocol.md` | → `hermes_acp_editor_integration` | concept term → Hermes ACP integration doc |
| `term_failover.md` | → `hermes_fallback_providers` | failover concept → cross-provider fallback doc |
| `term_round_robin.md` | → `hermes_credential_pools` | rotation strategy concept → credential-pool doc |
| `term_oauth_token.md` | → `hermes_subscription_proxy`, `hermes_provider_routing` | OAuth concept → proxy/routing usage |
| `term_api_gateway.md` | (NO inlink — unrelated generic gateway pattern) | confirmed false-positive; do NOT link |
| `entry_code_snippets_hermes_agent.md` | → `hermes_mcp_concept_config`, `hermes_credential_pools` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 9 notes | navigation hub |

Plus the 4 Phase-0 term captures each get inbound `## Related Terms` links from existing in/cross-domain
term notes (capture-term-note Step 6e backlink expansion, 5-10 inlinks each). Guarantees every new note
(9 docs + 4 terms) ends with in-degree ≥1 from outside the folder (G8). Inlink addition is a gated
execution phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Run **Phase 0 (4 term captures) FIRST** so the digest notes' Related Notes resolve. Pilot Note 1
(`hermes_mcp_concept_config`) → reindex → verify format/ghost/in-degree BEFORE authoring the rest.
Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each note —
do NOT work from memory. Code blocks verbatim for kept blocks; curate code-heavy notes (mcp 42,
provider-routing 15) to ≤6 load-bearing blocks, summarize the rest in prose; keep the fallback
supported-provider matrix as a prose table (not a code block). If a note exceeds 350 lines during writing,
STOP and split. If multi-agent: agents return note content, master writes serially where there is
write-contention; ≤30 agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP09 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 9 rows to
  the master-created entry point; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8); run
  `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After P1 wave: cross-link the SP02 config-key reference (`hermes_model_aux_provider_config`,
  `hermes_config_files_precedence`) bidirectionally with Notes 6/7/8 (config block ↔ concept/procedure).
- Cross-link Note 9 (subscription proxy) ↔ SP14 `term_nous_portal` once captured.
- Consider one `thought_` note comparing the docs-stated provider-resilience design (pool → fallback →
  auxiliary ladder) vs the code-digestion findings in `snippet_hermes_agent_core_credential_pool_*` /
  `core_chat_helpers_activate_fallback`.

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (3 LIKE false-positives confirmed by reading the notes:
  AWS lookup; MCP/ACP term hits = concept-vs-procedure LINKs), Owned-Term Specificity+Collision verdicts,
  active), Doc-Note Authoring Spec (derived from `cc_*.md`), Term-Note Authoring Requirements (4 owned, multi-source mandate),
  Density Re-Assessment (re-read confirmed), Phase 0 term-capture phase, G5 ghost + G8 scripts, Inlinks.
- Density re-read: counts match measured (mcp 3868, api-server 2608, fallback 2582, credential-pools 1351,
  acp 1292, subscription-proxy 865, provider-routing 649; re-measured 2026-06-19 mirror c253b07); **2 splits**
  (mcp→2, api-server→2). All 9 notes ≤2500w; code-heavy notes curated to ≤6 blocks. fallback 2470→2582
  crossed the 2500w *page* threshold but its single owning Note 7 stays ~1700w (link-out-compressed) → no split.
- Collision audit: **0 removals** of would-be captures — all 4 owned slugs ABSENT + concept-distinct;
  `term_mcp`/`term_acp_agent_client_protocol` LINK-not-recreate; 3 LIKE hits confirmed unrelated.
- Term placeholder catch: **6 non-existent term slugs + 1 absent snippet caught at finalization**
  (`term_mutual_tls`, `term_concurrency`, `term_tool_use`, `term_retry`, `term_thread_safety`,
- Undigested terms surfaced at augment: **0 new** beyond the master inventory (the 4 owned slugs were
  already in the master sweep; re-read confirmed no additional captures needed).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.
- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  code-repo / ≥10 doc "+bonus snippets" state and the 2026-06-14 ≥8 term / ≥8 snippet / ≥5 doc floor. Each of
  the 9 planned notes' Per-Note Mapping carries a Code-Repos (≥5) line (from the 13 `repo_hermes_agent_*`
  2026-06-19), and Docs (≥10) (sibling `hermes_*` (+fin) + analogous `claude_code/cc_*` agent-tool docs,
  owned terms are `(+Phase 0)` additions, not relied on for the active floor. Repos cited across SP09:
  `repo_hermes_agent`, `_agent_core`, `_cli`, `_gateway_messaging`, `_mcp_toolsets`, `_tools`, `_acp`,
  `_providers_adapters`, `_cron`.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (≥8 term/≥5 code-repo/≥10 snippet/≥10 doc;
Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan ✓ Capture
Phase per term (Phase 0, all 4) ✓ best-fit glossary (all 4 verified glossary targets) ✓ Term-Note Auth Reqs ✓
invokes capture-term-note (all 4) ✓ Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (4 owned,
0 renames, justified) ✓ Slug Collision (3 LIKE false-positives + 6 placeholders + 1 snippet caught) ✓ dedup
generalized to ALL notes incl doc, searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks
EXECUTED (Phase 3b) ✓ Doc-Note Authoring Spec derived ✓).

## Review Sign-Off

**Re-reviewed 2026-06-19 (four-floor standard) — READY FOR EXECUTION (9/9 checkpoints pass).**
Independent /tessellum-review-digestion-plan re-run against the FOUR-FLOOR standard (≥8 term / ≥5 code-repo /
terms (the `(+ Phase 0)`/`(+fin)` additions correctly excluded from the count), 5 code-repos, ≥10 snippets
(Note 1 = 11), and 10 docs, every counted link with a `relevance:` clause. **Anti-fabrication: ALL cited IDs
distinct `cc_*` doc IDs active; the 4 Phase-0 owned terms correctly ABSENT (additions, not counted); 0 fabricated
IDs.** Doc targets: 15 sibling `hermes_*` (+fin, resolve at finalization per G5/G8), 0 non-hermes/non-cc ghost
targets. CP7 source counts independently re-measured from `inbox/hermes_agent_docs/` (mcp 3868w/42, api-server
2608w/22, fallback 2582w/18, credential-pools 1351w/12, acp 1292w/14, subscription-proxy 865w/11,
provider-routing 649w/15) — exact match to the Source Pages table. Four-floor wording consistent across the
mapping preamble, "All 9 notes meet" assertion, Authoring Spec minimum, Augmentation Report, 31-item checklist,
and CP1 sign-off. No factual fixes required.

| CP | Check | Result | Evidence (2026-06-19 four-floor re-review) |
|----|-------|--------|--------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Phase 0 + 3 digest phases + Phase 3b, each G1–G8 incl G5-ghost (Script 4 DB-verify) + G6-broken + G8 in-degree ≥1 from outside the folder. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (9 rows, Protocols & Provider Integration section); matches >30-note threshold. |
| CP4 | Plan size manageable | PASS | 9 doc notes + 4 term captures ≤30. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md`; four-floor minimum embedded (line 317). |
| CP6 | Borderline density → split | PASS | mcp→2, api-server→2; all 9 notes ≤2500w/≤6 code/≤400 lines; fallback 2582w page but Note 7 ~1700w → no split. |
| CP7 | Source counts measured | PASS | Re-measured 2026-06-19 from inbox — exact match to Source Pages table on all 7 pages. |
| CP8 | Undigested Terms + Authoring Reqs | PASS | 4 owned captures ABSENT-verified → Phase 0; multi-source mandate in MUST-language; `term_mcp`/`term_acp_agent_client_protocol` LINK-not-recreate. |
| CP8f | Slug specificity + all-notes collision audit | PASS | 4 owned, 0 renames justified; 3 LIKE false-positives confirmed; 6 placeholder terms + 1 absent snippet caught + replaced with active IDs (verified 0 non-active in counted lists). |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 9 doc notes + 4 term captures from outside the folder; gated Phase 3b. |

**RESULT: 9/9 → READY FOR EXECUTION (four-floor re-review 2026-06-19).**

---

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | Phase 0 + 3 digest phases + Phase 3b, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (9 rows under a Protocols & Provider Integration section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 9 doc notes + 4 term captures ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | mcp→2, api-server→2; all notes ≤2500w; code-heavy notes curated ≤6; fallback matrix kept as prose table; borderline notes (1/2/7 at ~1700w) are cohesive single-BB clusters, KEEP justified. |
| CP7 | Source counts measured | PASS | Re-measured 2026-06-19 (mirror c253b07): mcp 3868, api-server 2608, fallback 2582, credential-pools 1351, acp 1292, subscription-proxy 865, provider-routing 649 — measured == master ledger; fallback crossed 2500w page cap but single owning Note 7 stays ~1700w (no split). |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP09 owns 4 term captures (all ABSENT-verified → CAPTURE Phase 0); Undigested Terms Plan + Term-Note Authoring Requirements present; multi-source mandate in MUST-language; `term_mcp`/`term_acp_agent_client_protocol` LINK-not-recreate. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Owned-Term Specificity+Collision table (4 owned, 0 renames justified); Collision & Dedup Audit covers all 9 doc notes + 4 terms (term_dictionary AND documentation/); 3 LIKE false-positives confirmed by READING the notes (api_gateway/credential_stuffing/aws_sdk_credential_chain); 6 placeholder terms + 1 absent snippet caught + replaced; Renamed/Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 9 doc notes + 4 term captures from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.**

## Re-Sync Note (2026-06-19)

Re-downloaded `inbox/hermes_agent_docs/` from upstream main HEAD (mirror_commit c253b07, was 95715dc);
independently re-measured all SP09-owned pages with the ledger convention (BODY words after stripping YAML
frontmatter; code blocks = ``` lines / 2). My measurements matched the manifest exactly. Changed pages:

- user-guide/features/mcp.md — 3818w/43code -> 3868w/42code
- user-guide/features/fallback-providers.md — 2470w/17code -> 2582w/18code

Spot-re-measured 3 unchanged pages — all stable: api-server.md 2608w/22, credential-pools.md 1351w/12,
provider-routing.md 649w/15.

**Density re-decision evaluated:** fallback-providers.md crossed the 2500w *page* threshold (2470→2582).
The 2500w cap applies per planned NOTE, not per source page. The page is owned by a single note (Note 7
`hermes_fallback_providers`, model BB) projected at ~1700w — the +112w growth (extra supported-provider
matrix rows + minor auxiliary-task clarifications) falls inside content the plan already prose-compresses
and link-routes (provider matrix → SP14 catalog table; provider guides → SP15; cron/delegation → SP06;
compression internals → SP18; 18 code blocks curated to ≤6). Projected Note 7 stays well under
≤2500w / ≤6 code / ≤400 lines → **NO SPLIT**. mcp.md (3868w) remains >2500 and was already split into
Notes 1+2 (unchanged). No new splits, no new notes — note count stays **9**; entry-point still contributes
**9 rows**.

Cross-ref floor was ≥8 term + ≥8 snippet + ≥5 doc per planned note at this 2026-06-19 re-sync; it was
subsequently **RAISED later on 2026-06-19** (master directive) to the FOUR-FLOOR standard
≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note (snippets promoted from a bonus group to a counted
≥10 floor) — see the Per-Note Related Notes Mapping and Augmentation Report. No planned-note filename, BB type,
or gate altered. Plan remains **READY** for execution.

## Pipeline Status (Per-Sub-Plan)


**Source**: `inbox/hermes_agent_docs/user-guide/features/{mcp,acp,api-server,provider-routing,fallback-providers,credential-pools,subscription-proxy}.md`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
