---
title: Sub-Plan gw02 — OpenClaw Docs: Gateway Configuration, Diagnostics, Discovery & Doctor
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["gateway/config-tools", "gateway/configuration", "gateway/configuration-examples", "gateway/configuration-reference", "gateway/diagnostics", "gateway/discovery", "gateway/doctor"]
---

# Sub-Plan gw02: Gateway

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format/YAML, dedup-before-create, the 9-GATE, cross-refs,
> Undigested-Terms ownership, and entry-point (W1 `entry_openclaw_docs.md`) decisions are ALL inherited from the master.

## Scope

The 7 Gateway-configuration / operability pages: the `tools.*` + custom-provider config surface (`config-tools`),
the task-oriented configuration overview (`configuration`), copy-paste configuration examples
(`configuration-examples`), the exhaustive field-level configuration reference (`configuration-reference`), the
shareable diagnostics-bundle workflow (`diagnostics`), node discovery + transports design (`discovery`), and the
`openclaw doctor` repair/migration tool (`doctor`). **Priority P1 (Phase A)** — this is the gateway configuration
vocabulary the CLI, channels, providers, plugins, and tools sub-plans all reference. The code-side counterparts
`repo_openclaw_gateway` and `repo_openclaw` are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 25,543 measured words. **Planned: 11 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| config-tools | gateway/config-tools | 3,803 | 18 | 3 | 17 | procedure (split: tools policy vs custom providers) |
| configuration | gateway/configuration | 3,504 | 7 | 9 | 3 | procedure (split: setup/tasks vs reload/RPC/env) |
| configuration-examples | gateway/configuration-examples | 1,829 | 11 | 5 | 9 | procedure |
| configuration-reference | gateway/configuration-reference | 8,397 | 34 | 34 | 21 | model (split ×3: runtime/agents/tools/models · platform/UI/gateway/discovery · ops/secrets/cron/includes) |
| diagnostics | gateway/diagnostics | 1,171 | 9 | 7 | 0 | procedure |
| discovery | gateway/discovery | 1,062 | 0 | 7 | 4 | concept (discovery/transport design) |
| doctor | gateway/doctor | 5,777 | 4 | 6 | 1 | procedure (split: usage/lint vs migration/check catalog) |

Code blocks = `grep -c '^\`\`\`'` ÷ 2. Words = `wc -w` over the whole file (frontmatter included; trimmed in the note).

## Content Strategy

- **Prioritize**: (1) the `configuration` task-oriented overview + strict-validation/hot-reload behavior (every
  edit depends on it); (2) the `tools.*` policy surface (`config-tools`) — profiles, groups, sandbox tool gating,
  allow/deny — which the tools and channels sub-plans cross-reference; (3) the `doctor` repair/migration tool (the
  recovery path when validation fails). These three define the operational core of Gateway config.
- **Split**: four pages exceed the 2,500-word cap and/or mix building blocks — `config-tools` (3,803w),
  `configuration` (3,504w), `configuration-reference` (8,397w → 3 notes by subsystem cluster), `doctor` (5,777w).
  See Split Decisions.
- **Link-out (don't redefine)**: per-channel config → ch01–ch06; per-provider config → pr01–pr09; per-plugin config
  → pl01–pl25; memory/QMD/dreaming deep knobs → `reference/memory-config` (rf02); secrets `SecretRef` deep surface →
  gw05/gw06 (`gateway/secrets`); CLI `openclaw config`/`openclaw doctor` command syntax → cl02/cl03 (`cli/config`,
  `cli/doctor`); OpenTelemetry/Prometheus exporters → gw04/gw05. These are referenced by section pointer, not copied.
- **One BB per note**: the reference page is a field-map (model BB); discovery is design/concept; the rest are
  configuration procedures. Code fences are reproduced selectively and verbatim, ≤6 per note.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_gateway_config_tools_policy.md` | procedure | config-tools.md: Tools (Tool profiles, Tool groups, MCP/plugin tools in sandbox policy, codeMode, allow/deny, byProvider, toolsBySender, elevated, exec, loopDetection, web, media, agentToAgent, sessions, sessions_spawn, experimental, subagents) | 700 | The `tools.*` policy surface: tool profiles (minimal/coding/messaging/full), tool groups, sandbox tool gating for MCP/plugin tools, and the per-tool config keys (allow/deny, byProvider, elevated, exec, loopDetection, web, media, sessions, subagents). |
| 2 | `oc_gateway_config_custom_providers.md` | procedure | config-tools.md: Custom providers and base URLs (Provider field details, Provider examples) | 500 | Registering custom model providers and overriding base URLs in `models.providers.*`: provider field details and OpenAI-compatible self-hosted endpoint examples. |
| 3 | `oc_gateway_configuration_overview.md` | procedure | configuration.md: Minimal config, Editing config, Strict validation, Common tasks, Full reference (pointer) | 700 | Configuring OpenClaw via the JSON5 `~/.openclaw/openclaw.json`: minimal config, the four edit paths (wizard/CLI/Control-UI/direct), strict schema validation and refuse-to-start behavior, and the common-task accordion of pointers. |
| 4 | `oc_gateway_config_reload_rpc_env.md` | procedure | configuration.md: Config hot reload (Reload modes, hot-apply vs restart, Reload planning), Config RPC (programmatic updates), Environment variables | 600 | Applying config changes at runtime: hot-reload modes, what hot-applies vs needs a restart, reload planning, the programmatic Config RPC, and the gateway environment-variable surface. |
| 5 | `oc_gateway_configuration_examples.md` | procedure | configuration-examples.md: Quick start (absolute minimum, recommended starter), Expanded example, Common patterns (symlinked skill repo, shared baseline, multi-platform, trusted node auto-approval, secure DM, API key + fallback, work bot, local models only), Tips | 650 | Copy-paste schema-accurate config recipes: minimal/recommended starters, a major-options expanded example, and common patterns (shared skill baseline, multi-platform, trusted-node auto-approval, secure DM, provider fallback, restricted work bot, local-models-only). |
| 6 | `oc_gateway_config_reference_runtime.md` | model | configuration-reference.md: Channels, Agent defaults/multi-agent/sessions/messages, Tools and custom providers, Models (Codex harness plugin config, OpenAI-compatible endpoints, multi-instance isolation), MCP, Skills, Plugins, Commitments | 700 | Field-level reference for the agent-runtime config surfaces: channels, agent defaults / multi-agent / sessions / messages, tools + custom providers, models (Codex harness, OpenAI-compatible endpoints, multi-instance isolation), MCP, skills, plugins, and commitments. |
| 7 | `oc_gateway_config_reference_platform.md` | model | configuration-reference.md: Browser, UI, Gateway (gateway.tls, gateway.reload, Gmail integration), Hooks, Canvas plugin host, Discovery (mDNS/Bonjour, wide-area DNS-SD), Environment (env inline, env var substitution) | 650 | Field-level reference for the platform/surface config: browser, UI, gateway (TLS, reload, Gmail), hooks, canvas plugin host, discovery (mDNS/Bonjour + wide-area DNS-SD), and the environment (inline `env`, env-var substitution) surfaces. |
| 8 | `oc_gateway_config_reference_ops.md` | model | configuration-reference.md: Secrets (SecretRef, credential surface, secret providers), Auth storage (auth.cooldowns), Logging, Diagnostics, Update, ACP, CLI, Wizard, Identity, Bridge (legacy), Cron (cron.retry/failureAlert/failureDestination), Media model template variables, Config includes ($include) | 700 | Field-level reference for operations/security config: secrets (`SecretRef`, credential surface, secret providers), auth storage + cooldowns, logging, diagnostics, update, ACP, CLI, wizard, identity, cron (retry/failure-alert/destination), media model template variables, and config includes (`$include`). |
| 9 | `oc_gateway_diagnostics_export.md` | procedure | diagnostics.md: Quick start, Chat command, What the export contains, Privacy model, Stability recorder, Useful options, Disable diagnostics | 600 | Creating shareable Gateway diagnostics bundles: `openclaw gateway diagnostics export`, the `/diagnostics` chat command + exec-approval flow, bundle contents, the redaction/privacy model, the stability recorder, options, and how to disable diagnostics. |
| 10 | `oc_gateway_discovery.md` | concept | discovery.md: Terms, Why both direct and SSH, Discovery inputs (Bonjour/DNS-SD beacon, Tailnet, Manual/SSH), Transport selection, Pairing + auth, Responsibilities by component | 550 | OpenClaw's node-discovery + transport design: direct WS vs SSH fallback, discovery inputs (Bonjour/DNS-SD service beacon, Tailnet/MagicDNS, manual SSH), the client transport-selection policy, gateway-owned pairing/auth, and component responsibilities. |
| 11 | `oc_gateway_doctor.md` | procedure | doctor.md: Quick start (headless/automation modes), Read-only lint mode, What it does (summary), Dreams UI backfill and reset, Detailed behavior and rationale | 750 | The `openclaw doctor` repair + migration tool: quick start, headless/automation + read-only lint modes, `--fix`/`--yes` repairs, the migration/check catalog (config normalization, legacy migrations, state integrity, gateway/service, auth/pairing checks), and the Dreams UI backfill/reset. |

Filenames apply the master rule (`oc_` + slug with `/` and `-` → `_`), with a short aspect suffix for each split note.

## Section Coverage Map

```
config-tools.md
├── Tools (Tool profiles, Tool groups, MCP/plugin tools in sandbox policy,
│   tools.codeMode, tools.allow/deny, tools.byProvider, tools.toolsBySender,
│   tools.elevated, tools.exec, tools.loopDetection, tools.web, tools.media,
│   tools.agentToAgent, tools.sessions, tools.sessions_spawn,
│   tools.experimental, agents.defaults.subagents) ──────────── → note 1 (oc_gateway_config_tools_policy)
├── Custom providers and base URLs (Provider field details, Provider examples) → note 2 (oc_gateway_config_custom_providers)
└── Related ───────────────────────────────────────────────── → References (link-out)
configuration.md
├── Minimal config / Editing config / Strict validation / Common tasks ──── → note 3 (oc_gateway_configuration_overview)
├── Full reference (pointer) ─────────────────────────────────────────── → note 3 (→ notes 6–8)
├── Config hot reload (Reload modes, hot-apply vs restart, Reload planning) → note 4 (oc_gateway_config_reload_rpc_env)
├── Config RPC (programmatic updates) ────────────────────────────────── → note 4
├── Environment variables ────────────────────────────────────────────── → note 4
└── Related ─────────────────────────────────────────────────────────── → References (link-out)
configuration-examples.md
├── Quick start (Absolute minimum, Recommended starter) ──────────────── → note 5 (oc_gateway_configuration_examples)
├── Expanded example (major options) ─────────────────────────────────── → note 5
├── Common patterns (symlinked sibling skill repo, shared skill baseline,
│   multi-platform, trusted node auto-approval, secure DM, API key +
│   MiniMax fallback, work bot, local models only) ───────────────────── → note 5
├── Tips ─────────────────────────────────────────────────────────────── → note 5
└── Related ─────────────────────────────────────────────────────────── → References (link-out)
configuration-reference.md
├── Channels ─────────────────────────────────────────────────────────── → note 6 (oc_gateway_config_reference_runtime)
├── Agent defaults, multi-agent, sessions, and messages ──────────────── → note 6
├── Tools and custom providers ───────────────────────────────────────── → note 6
├── Models (Codex harness plugin config, OpenAI-compatible endpoints,
│   Multi-instance isolation) ────────────────────────────────────────── → note 6
├── MCP / Skills / Plugins / Commitments ─────────────────────────────── → note 6
├── Browser / UI ─────────────────────────────────────────────────────── → note 7 (oc_gateway_config_reference_platform)
├── Gateway (gateway.tls, gateway.reload) ────────────────────────────── → note 7
├── Hooks (Gmail integration) / Canvas plugin host ───────────────────── → note 7
├── Discovery (mDNS Bonjour, Wide-area DNS-SD) ───────────────────────── → note 7
├── Environment (env inline env vars, Env var substitution) ──────────── → note 7
├── Secrets (SecretRef, Supported credential surface, Secret providers) ─ → note 8 (oc_gateway_config_reference_ops)
├── Auth storage (auth.cooldowns) ────────────────────────────────────── → note 8
├── Logging / Diagnostics / Update / ACP / CLI / Wizard / Identity ────── → note 8
├── Bridge (legacy, removed) ─────────────────────────────────────────── → note 8
├── Cron (cron.retry, cron.failureAlert, cron.failureDestination) ─────── → note 8
├── Media model template variables ───────────────────────────────────── → note 8
├── Config includes ($include) ───────────────────────────────────────── → note 8
└── Related ─────────────────────────────────────────────────────────── → References (link-out)
diagnostics.md
├── Quick start / Chat command / What the export contains ───────────── → note 9 (oc_gateway_diagnostics_export)
├── Privacy model / Stability recorder / Useful options / Disable ─────── → note 9
└── Related ─────────────────────────────────────────────────────────── → References (link-out)
discovery.md
├── Terms / Why we keep both direct and SSH ──────────────────────────── → note 10 (oc_gateway_discovery)
├── Discovery inputs (Bonjour/DNS-SD, Tailnet, Manual/SSH) ───────────── → note 10
├── Transport selection / Pairing + auth / Responsibilities ──────────── → note 10
└── Related ─────────────────────────────────────────────────────────── → References (link-out)
doctor.md
├── Quick start (Headless and automation modes) / Read-only lint mode ── → note 11 (oc_gateway_doctor)
├── What it does (summary) ───────────────────────────────────────────── → note 11
├── Dreams UI backfill and reset ─────────────────────────────────────── → note 11
├── Detailed behavior and rationale ──────────────────────────────────── → note 11
└── Related ─────────────────────────────────────────────────────────── → References (link-out)
```
No orphaned sections. Per-channel/provider/plugin/memory/secrets/CLI/exporter deep references are linked out, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| config-tools.md (3,803w, 18 code, 17 H3, mixed) | notes 1 + 2 | exceeds 2,500w; the `tools.*` policy/sandbox surface and the custom-provider/base-URL setup are distinct task clusters; split keeps each ≤700w and ≤6 code blocks (18 fences distribute). |
| configuration.md (3,504w, 9 H2) | notes 3 + 4 | exceeds 2,500w; first-time setup + validation + common tasks (a getting-started procedure) vs runtime reload + Config RPC + env vars (an operate-while-running procedure) are separate task clusters. |
| configuration-reference.md (8,397w, 34 H2, 34 code) | notes 6 + 7 + 8 | far exceeds 2,500w and is a multi-subsystem field-map (model BB); split into runtime (channels/agents/tools/models/MCP/skills/plugins/commitments), platform (browser/UI/gateway/hooks/canvas/discovery/env), and ops/security (secrets/auth/logging/diagnostics/update/ACP/CLI/wizard/identity/cron/media-vars/includes) clusters so each note stays ≤700w and ≤6 code. |
| doctor.md (5,777w, 6 H2) | (none) | kept as 1 note (note 11) at ~750w: it is a single coherent `openclaw doctor` procedure; the "What it does" check/migration catalog is summarized (one BB), not reproduced field-by-field. Watch density at execution — if it overruns, promote a split into usage/lint vs migration-catalog. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (25,543 measured words). New `oc_` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×7 (notes 1–5, 9, 11) · model ×3 (notes 6–8, the reference field-maps) · concept ×1 (note 10, discovery design).
- Est. digest words ~7,100 (avg ~645/note); all ≤750w (well under the 2,500-word cap). 92 source code fences
  distribute across the procedure/model notes; each note kept ≤6 (config snippets reproduced selectively, verbatim).
- Cross-refs (**LOCKED at xref-augment 2026-06-21**): each note maps **≥8 relevance-selected `term_dictionary`
  sibling `oc_*` count toward the 10-doc floor as "(planned, this series)"), PLUS relevant `repo_openclaw*`, each
  Notes Mapping (LOCKED — xref-augment 2026-06-21)** for the locked per-note lists.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

**Standard (per note):** ≥8 `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`,
toward the 10-doc floor. Repos are listed separately as additional discovery anchors. Relative paths are FROM a note
at `resources/documentation/openclaw/oc_X.md`: term `../../term_dictionary/`, snippet `../../code_snippets/`, other
(`SELECT 1 FROM notes WHERE note_id='<id>'`) on 2026-06-21.

### oc_gateway_config_tools_policy (8t · 10s · 10d)

**Terms**
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol server/tool standard; relevance: configured MCP servers are exposed as `bundle-mcp` plugin tools gated by `tools.sandbox.tools`.
- [MCP Gateway](../../term_dictionary/term_mcp_gateway.md) — fronts MCP servers as managed tools; relevance: `mcp.servers` entries surface through the same sandbox tool gate this note documents.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution mode; relevance: `sandbox.mode` all/non-main is the gate that makes `tools.sandbox.tools.alsoAllow` load-bearing.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool-invocation; relevance: `tools.*` allow/deny defines the callable tool surface the model sees.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — registered tool catalog; relevance: tool profiles (minimal/coding/messaging/full) and groups define the registered set this policy filters.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned child agent; relevance: `tools.sessions_spawn` and `agents.defaults.subagents` are config keys covered here.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — agent-to-agent orchestration; relevance: `tools.agentToAgent` enables the agent-to-agent tool this policy governs.
- [Deny-First](../../term_dictionary/term_deny_first.md) — deny-wins authorization default; relevance: `tools.deny` wins over `tools.allow` — the exact deny-first semantics this note states.
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — sandboxed code-run tool; relevance: `group:runtime` (`exec`/`process`/`code_execution`) is the highest-risk tool group gated here.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization policy; relevance: `byProvider`/`toolsBySender`/`elevated` are the per-sender authorization layers documented.

**Docs**
- [Claude Code — Sandbox vs Permissions](../claude_code/cc_sandbox_vs_permissions.md) — how sandbox and permission layers compose; relevance: the same two-layer model (sandbox gate + tool allowlist) OpenClaw applies.
- [Claude Code — Tool-Specific Permission Rules](../claude_code/cc_tool_specific_permission_rules.md) — per-tool allow/deny rule syntax; relevance: direct analog to `tools.allow`/`tools.deny` wildcard/case-insensitive rules.
- [Claude Code — Permission System and Rules](../claude_code/cc_permission_system_and_rules.md) — allow/ask/deny precedence; relevance: parallels OpenClaw's deny-wins precedence over profile/group baselines.
- [Claude Code — Execution Tool Behavior](../claude_code/cc_execution_tool_behavior.md) — bash/exec tool runtime semantics; relevance: documents the `exec`/`code_execution` tool this note's `group:runtime` and `tools.exec` gate.
- [Claude Code — MCP Installation Scopes](../claude_code/cc_mcp_installation_scopes.md) — where MCP servers register; relevance: scope analog to OpenClaw's `bundle-mcp`/server-glob sandbox allowlist entries.
- [Hermes — Tools Runtime](../hermes_agent/hermes_tools_runtime.md) — tool registry + lazy-load runtime; relevance: implementation view of the registered tool set OpenClaw's profiles/groups select from.
- [Hermes — MCP Concept and Config](../hermes_agent/hermes_mcp_concept_config.md) — MCP server config model; relevance: the server-config shape that becomes plugin-owned tools under the sandbox gate.
- [oc_gateway_config_custom_providers](oc_gateway_config_custom_providers.md) — companion half of config-tools.md (planned, this series); relevance: the other tool-adjacent surface (`models.providers.*`) from the same source page.
- [oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md) — Tools-and-custom-providers field reference (planned, this series); relevance: the field-level map of every `tools.*` key summarized here.
- [oc_gateway_configuration_overview](oc_gateway_configuration_overview.md) — parent config overview (planned, this series); relevance: where the `tools.*` block fits in the whole config tree.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: implements the `tools.*` policy + sandbox tool gating.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: applies the tool profile/group/allowlist to the agent's callable set.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills layer; relevance: `skill_workshop` is in the coding profile this note lists.

**Snippets**
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool allow/deny policy resolution; relevance: the exact deny-wins/profile-baseline logic this note documents.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — registered tool catalog assembly; relevance: how profiles/groups expand into the concrete tool set.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — deny-list for dangerous tools; relevance: code-side of `group:fs`/`group:runtime` deny enforcement.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec/filesystem gating; relevance: `tools.exec` + `group:fs` enforcement implementation.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — runtime exec audit; relevance: how elevated/exec tool use is audited under policy.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: the gateway-side command-gating analog to `tools.elevated`.
- [snippet_openclaw_agents_subagent_spawn_acp](../../code_snippets/snippet_openclaw_agents_subagent_spawn_acp.md) — subagent spawn over ACP; relevance: implements `tools.sessions_spawn`/`subagents` config.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry implementation; relevance: registered-tool-set analog OpenClaw profiles/groups select from.
- [snippet_hermes_agent_skills_mcp_native](../../code_snippets/snippet_hermes_agent_skills_mcp_native.md) — native MCP tool exposure; relevance: how MCP servers become callable tools the sandbox gate filters.

### oc_gateway_config_custom_providers (8t · 10s · 10d)

**Terms**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — config-defined model backend; relevance: a custom provider IS a `models.providers.*` provider backend this note registers.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: each custom provider fronts one or more LLMs.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — front-end request forwarder; relevance: a `baseUrl` override commonly points at a reverse-proxied/self-hosted endpoint.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI APIs; relevance: custom providers target external/self-hosted GenAI servers.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider→models registry; relevance: `models.providers.*` declares the provider's model catalog.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — request-routing front door; relevance: OpenAI-compatible gateway endpoints are a primary `baseUrl` target.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool-call formatting; relevance: provider `api` type governs how tool calls are encoded for that backend.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — route requests across providers; relevance: custom providers join the routing/fallback pool.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — backup model backend; relevance: a custom provider is often the fallback target in a primary+fallback chain.
- [Model Failover](../../term_dictionary/term_model_failover.md) — automatic provider switchover; relevance: custom providers participate in failover when a primary is unavailable.

**Docs**
- [Pi — Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering a custom model provider; relevance: closest cross-tool analog to `models.providers.*` registration.
- [Pi — Custom Models](../pi/pi_custom_models.md) — declaring custom model entries; relevance: the model-catalog half of custom-provider setup.
- [Pi — Model Overrides Compat](../pi/pi_model_overrides_compat.md) — OpenAI-compatible model overrides; relevance: parallels OpenClaw's OpenAI-compatible endpoint field details.
- [Hermes — Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — add a new provider backend; relevance: same task as registering a custom provider + base URL.
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin contract; relevance: implementation analog of OpenClaw's provider-plugin backend.
- [Hermes — Provider Routing and Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — base-URL/proxy routing; relevance: the proxy/base-URL override pattern this note documents.
- [Claude Code — LLM Gateway (LiteLLM)](../claude_code/cc_llm_gateway_litellm.md) — OpenAI-compatible gateway in front of models; relevance: canonical OpenAI-compatible `baseUrl` target.
- [Claude Code — Amazon Bedrock Mantle Endpoint](../claude_code/cc_amazon_bedrock_mantle_endpoint.md) — custom Bedrock endpoint override; relevance: a concrete base-URL override example.
- [oc_gateway_config_tools_policy](oc_gateway_config_tools_policy.md) — companion half of config-tools.md (planned, this series); relevance: the tool-policy surface from the same source page.
- [oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md) — Models field reference incl. OpenAI-compatible endpoints (planned, this series); relevance: the field-level map of `models.providers.*`.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: the extension layer custom providers register into.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: resolves provider config + base URLs at request time.

**Snippets**
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: implements exactly the custom-provider registration this note configures.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstraction; relevance: the provider-field contract (api type, baseUrl, models) this note documents.
- [snippet_hermes_agent_core_auxiliary_proxy_url](../../code_snippets/snippet_hermes_agent_core_auxiliary_proxy_url.md) — resolve provider proxy/base URL; relevance: code-side of `baseUrl` override resolution.
- [snippet_hermes_agent_core_anthropic_adapter_endpoints](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_endpoints.md) — adapter endpoint selection; relevance: how a base-URL override re-points an OpenAI/Anthropic-compatible adapter.
- [snippet_hermes_agent_core_auxiliary_headers](../../code_snippets/snippet_hermes_agent_core_auxiliary_headers.md) — provider auth headers; relevance: the header/api-key plumbing a custom provider needs.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: registry that custom providers join — analog to `models.providers.*`.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — plugin provider registry; relevance: plugin-side provider registration model.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: the OpenAI-compatible base case custom providers mimic.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: self-hosted base-URL endpoint example.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator provider; relevance: third-party GenAI gateway base-URL example.

### oc_gateway_configuration_overview (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway product; relevance: the product being configured via `~/.openclaw/openclaw.json`.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema-validation standard; relevance: strict validation / `openclaw config schema` rejects unknown keys.
- [Structured Output](../../term_dictionary/term_structured_output.md) — schema-constrained output; relevance: the JSON5 config is a schema-validated structured document.
- [Agentic Workflow](../../term_dictionary/term_agentic_workflow.md) — agent-driven task flow; relevance: config drives the agent's behavior/channels/tools.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational bot; relevance: `channels.*`/`allowFrom` control who can message the bot.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: automation config (`cron`/`hooks`) is a common-task accordion item.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution; relevance: sandboxing is a top-level config concern in the overview.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization policy; relevance: `allowFrom`/who-can-message is the core access policy set here.

**Docs**
- [Claude Code — Settings Files](../claude_code/cc_settings_files.md) — settings file locations + precedence; relevance: analog to `~/.openclaw/openclaw.json` + the edit-paths model.
- [Claude Code — Settings Reference](../claude_code/cc_settings_reference.md) — full settings field map; relevance: the "full reference" pointer this overview defers to.
- [Claude Code — Debug Your Configuration](../claude_code/cc_debug_your_configuration.md) — diagnosing bad config; relevance: parallels "validation fails → run doctor" recovery path.
- [Claude Code — Server-Managed Settings](../claude_code/cc_server_managed_settings.md) — managed/locked config; relevance: strict-schema/managed-config posture analog.
- [Hermes — Config Files Precedence](../hermes_agent/hermes_config_files_precedence.md) — config layering/precedence; relevance: the edit-paths (wizard/CLI/UI/direct) + precedence model.
- [Pi — Settings Reference](../pi/pi_settings_reference.md) — settings reference; relevance: cross-tool full-reference analog.
- [oc_gateway_config_reload_rpc_env](oc_gateway_config_reload_rpc_env.md) — runtime-edit companion (planned, this series); relevance: the operate-while-running half of configuration.md.
- [oc_gateway_configuration_examples](oc_gateway_configuration_examples.md) — copy-paste recipes (planned, this series); relevance: the worked configs that realize this overview.
- [oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md) — runtime field reference (planned, this series); relevance: the "full reference" the overview points to.
- [oc_gateway_doctor](oc_gateway_doctor.md) — repair/migration tool (planned, this series); relevance: `doctor --fix` repairs configs that fail strict validation.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: loads/validates `~/.openclaw/openclaw.json` and refuses to start on schema failure.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: the config surface + JSON Schema source.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — onboarding/config wizard; relevance: `openclaw onboard`/`configure` interactive edit path.

**Snippets**
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard-driven config write; relevance: the interactive edit path this overview lists.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config assembly; relevance: how the validated config becomes runtime state.
- [snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md) — config validation command; relevance: analog of `openclaw config validate`/strict-schema refusal.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — startup auth/config load; relevance: the refuse-to-start-on-invalid-config behavior.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI command routing; relevance: routes `config get/set/unset` one-liner edit path.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — schema group definitions; relevance: the `config.schema.lookup` schema surface Control UI renders.
- [snippet_hermes_agent_cli_config_migrate](../../code_snippets/snippet_hermes_agent_cli_config_migrate.md) — config migration; relevance: the legacy-config path doctor handles when validation fails.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — wizard import flow; relevance: importing existing config into the validated wizard model.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — apply config changes; relevance: how a direct edit is validated then applied (links to note 4).

### oc_gateway_config_reload_rpc_env (8t · 10s · 10d)

**Terms**
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC-over-JSON protocol; relevance: the Config RPC (`config.get`/`patch`/`apply`) is the programmatic-update surface.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the gateway being reconfigured at runtime.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: the gateway WS carries the Config RPC calls.
- [WebSocket Framing](../../term_dictionary/term_websocket_framing.md) — WS message framing; relevance: the RPC envelope/framing the Config RPC rides on.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema validation; relevance: hot-reload re-validates the edited config against the schema before applying.
- [Rate Limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: control-plane writes are rate-limited to 3/60s + 30s restart cooldown.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — credential token; relevance: env-injected credentials live in the env-var surface this note covers.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: env vars + config feed automation (cron/hooks) hot-applied at reload.

**Docs**
- [Claude Code — Environment Variables](../claude_code/cc_environment_variables.md) — env-var surface; relevance: direct analog to OpenClaw's `.env`/`~/.openclaw/.env`/inline `env` surface.
- [Claude Code — Settings Files](../claude_code/cc_settings_files.md) — config file watching/precedence; relevance: the watched-file + reload model.
- [Claude Code — Debug Your Configuration](../claude_code/cc_debug_your_configuration.md) — diagnosing reload/config issues; relevance: "config reload skipped (invalid)" recovery.
- [Hermes — Config Files Precedence](../hermes_agent/hermes_config_files_precedence.md) — config + env precedence; relevance: how inline `env`/`.env` interact without overriding existing vars.
- [Hermes — Env Vars (Providers/Auth/Tools)](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — env-var catalog; relevance: the credential/env surface injected into config.
- [Pi — SDK Options](../pi/pi_sdk_options.md) — programmatic config options; relevance: cross-tool analog to the Config RPC programmatic-update flow.
- [oc_gateway_configuration_overview](oc_gateway_configuration_overview.md) — parent overview / edit paths (planned, this series); relevance: the first-time-setup half this reload/RPC note complements.
- [oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md) — Environment + includes field reference (planned, this series); relevance: the field-level `env`/`$include` map.
- [oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md) — hot-applies-vs-restart field map (planned, this series); relevance: which `agent`/`models`/`tools` fields hot-apply.
- [oc_gateway_doctor](oc_gateway_doctor.md) — repair tool (planned, this series); relevance: `doctor --fix` recovers when a reload is rejected as invalid.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: the hot-reload file watcher + Config RPC handlers.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: the env-var resolution surface.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session runtime; relevance: what hot-applies vs needs a restart per active session.

**Snippets**
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — reload-and-apply logic; relevance: implements hot-apply vs restart decision this note documents.
- [snippet_openclaw_gateway_rpc_protocol_envelope](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_envelope.md) — RPC request envelope; relevance: the wire shape of `config.get`/`config.patch` calls.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: `config.schema.lookup` path-scoped schema nodes.
- [snippet_openclaw_gateway_rpc_protocol_error_codes_version](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_error_codes_version.md) — RPC error codes/version; relevance: error/version handling for control-plane writes.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — broadcast runtime config; relevance: how an applied config change propagates to runtime.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway RPC methods; relevance: where `config.*`/`update.*` methods are registered.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway WS channel; relevance: the WS transport the Config RPC travels over.
- [snippet_openclaw_acp_server](../../code_snippets/snippet_openclaw_acp_server.md) — ACP/RPC server; relevance: the RPC server pattern serving config methods.
- [snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md) — config re-validation; relevance: reload re-validates against schema before applying.
- [snippet_hermes_agent_cli_config_migrate](../../code_snippets/snippet_hermes_agent_cli_config_migrate.md) — config migration on load; relevance: legacy-config handling at reload time.

### oc_gateway_configuration_examples (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the configs being exemplified target OpenClaw.
- [Skills](../../term_dictionary/term_skills.md) — agent skill bundles; relevance: shared-skill-baseline / symlinked-sibling-skill-repo patterns are example recipes.
- [Skill Manifest](../../term_dictionary/term_skill_manifest.md) — skill declaration; relevance: the symlinked skill repo pattern relies on skill manifests.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: the Anthropic-API-key example pattern.
- [Model Failover](../../term_dictionary/term_model_failover.md) — provider switchover; relevance: the "API key + MiniMax fallback" recipe.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization policy; relevance: work-bot restricted-access + secure-DM example patterns.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — direct-message access rules; relevance: the secure-DM (shared inbox / multi-user DM) recipe.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the local-models-only recipe.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational bot; relevance: the multi-platform bot setup recipe.

**Docs**
- [Claude Code — Settings Reference](../claude_code/cc_settings_reference.md) — full settings map; relevance: the field vocabulary the expanded example uses.
- [Claude Code — Settings Files](../claude_code/cc_settings_files.md) — config layering; relevance: the shared-baseline + override pattern.
- [Hermes — Profile Distribution Model](../hermes_agent/hermes_profile_distribution_model.md) — shareable config profiles; relevance: analog to the shared-skill-baseline + multi-platform recipes.
- [Hermes — Local/Self-Hosted LLM](../hermes_agent/hermes_local_self_hosted_llm.md) — local-models setup; relevance: the local-models-only recipe.
- [Hermes — Secrets (Bitwarden)](../hermes_agent/hermes_secrets_bitwarden.md) — API-key/secret handling in config; relevance: the API-key example + secure secret storage.
- [Pi — Cloud Providers](../pi/pi_cloud_providers.md) — provider/fallback config; relevance: the API-key + fallback recipe.
- [oc_gateway_configuration_overview](oc_gateway_configuration_overview.md) — the page these examples support (planned, this series); relevance: examples realize the overview's edit paths.
- [oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md) — fields used in the expanded example (planned, this series); relevance: the field-level reference for each recipe key.
- [oc_gateway_config_tools_policy](oc_gateway_config_tools_policy.md) — tool-policy in the work-bot recipe (planned, this series); relevance: the restricted-tool patterns the work-bot recipe applies.
- [oc_gateway_config_custom_providers](oc_gateway_config_custom_providers.md) — provider config in the fallback recipe (planned, this series); relevance: the custom-provider/base-URL fields the fallback recipe uses.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: consumes these example configs.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills layer; relevance: skill baseline/override patterns in the examples.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: the config root the examples write.

**Snippets**
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard-generated config; relevance: produces starter configs like the recommended-starter recipe.
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — runtime config assembly; relevance: how an example config becomes runtime state.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest format; relevance: the shared-skill-baseline / symlinked-skill-repo recipe.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider config; relevance: the API-key provider example.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama config; relevance: the local-models-only recipe.
- [snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — fallback activation; relevance: the API-key + fallback recipe behavior.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: the multi-provider/model fields the expanded example sets.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy; relevance: the restricted-tool work-bot recipe.
- [snippet_openclaw_cli_route](../../code_snippets/snippet_openclaw_cli_route.md) — CLI routing; relevance: the `openclaw config set` one-liners that build these examples.

### oc_gateway_config_reference_runtime (9t · 10s · 10d)

**Terms**
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: the `mcp` config block field reference.
- [Skills](../../term_dictionary/term_skills.md) — agent skill bundles; relevance: the `skills` config block.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin declaration contract; relevance: the `plugins` config block + manifest contracts.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — multi-agent orchestration; relevance: agent-defaults / multi-agent config surface.
- [Subagent](../../term_dictionary/term_subagent.md) — spawned child agent; relevance: subagent defaults under agents config.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider→models registry; relevance: the Models config surface (Codex harness, OpenAI-compatible).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model backend; relevance: custom providers inside the Models block.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool-call surface; relevance: the Tools-and-custom-providers field block.
- [Compaction](../../term_dictionary/term_compaction.md) — context compaction; relevance: the sessions/messages config knobs (compaction settings).
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent execution harness; relevance: Codex harness plugin config + multi-instance isolation.

**Docs**
- [Claude Code — Subagent Configuration Reference](../claude_code/cc_subagent_configuration_reference.md) — subagent config fields; relevance: direct analog to agent-defaults/subagent config here.
- [Claude Code — Settings Reference](../claude_code/cc_settings_reference.md) — full settings field map; relevance: the closest field-reference precedent for this model BB.
- [Claude Code — Plugin Components](../claude_code/cc_plugin_components.md) — plugin config surface; relevance: the `plugins` config block + manifest contracts.
- [Claude Code — Work With Subagents](../claude_code/cc_work_with_subagents.md) — multi-agent usage; relevance: the multi-agent config this reference governs.
- [Hermes — MCP Config Reference](../hermes_agent/hermes_mcp_config_reference.md) — MCP config fields; relevance: the `mcp` config block reference.
- [Hermes — Provider Runtime](../hermes_agent/hermes_provider_runtime.md) — model/provider runtime config; relevance: the Models config surface + custom-provider fields.
- [Pi — Custom Models](../pi/pi_custom_models.md) — model declaration fields; relevance: cross-tool analog for the Models block.
- [oc_gateway_config_reference_platform](oc_gateway_config_reference_platform.md) — platform reference cluster (planned, this series); relevance: sibling field-reference cluster from the same source page.
- [oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md) — ops reference cluster (planned, this series); relevance: sibling field-reference cluster.
- [oc_gateway_configuration_overview](oc_gateway_configuration_overview.md) — the overview that points here (planned, this series); relevance: the entry point into this full reference.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: validates these runtime config surfaces.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: agent-defaults/multi-agent/Codex-harness config.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session runtime; relevance: sessions/messages/compaction config.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills layer; relevance: the `skills` config block.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension layer; relevance: the `plugins` config block.

**Snippets**
- [snippet_openclaw_agents_runtime_config](../../code_snippets/snippet_openclaw_agents_runtime_config.md) — agent runtime config; relevance: assembles agent-defaults/sessions/messages from this reference.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: the Models config surface.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: the Tools-and-custom-providers field block.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the `plugins` manifest-contract fields.
- [snippet_hermes_agent_plugins_interfaces_abcs](../../code_snippets/snippet_hermes_agent_plugins_interfaces_abcs.md) — plugin interfaces; relevance: the plugin config contract surface.
- [snippet_hermes_agent_skills_codex](../../code_snippets/snippet_hermes_agent_skills_codex.md) — Codex harness skill; relevance: the Codex harness plugin config in Models.
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — Codex provider plugin; relevance: Codex-harness Models config + multi-instance isolation.
- [snippet_hermes_agent_core_context_engine_abc](../../code_snippets/snippet_hermes_agent_core_context_engine_abc.md) — context engine; relevance: the messages/compaction config knobs.
- [snippet_hermes_agent_honcho_session_query](../../code_snippets/snippet_hermes_agent_honcho_session_query.md) — session query; relevance: the sessions config surface.

### oc_gateway_config_reference_platform (8t · 10s · 10d)

**Terms**
- [TLS](../../term_dictionary/term_tls.md) — transport-layer security; relevance: the `gateway.tls` config field reference.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — certificate fingerprint pinning; relevance: `gatewayTls`/fingerprint fields the discovery beacon advertises.
- [DNS](../../term_dictionary/term_dns.md) — domain name system; relevance: wide-area DNS-SD discovery config.
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — mDNS service discovery; relevance: the `discovery` mDNS/Bonjour config block.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: the `browser` config block.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP callback; relevance: Gmail integration / hooks config.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: gateway WS bind/reload config.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the gateway/UI surface being configured.

**Docs**
- [Claude Code — Network, TLS and Access](../claude_code/cc_network_tls_and_access.md) — TLS/network config; relevance: direct analog to `gateway.tls` + bind config.
- [Claude Code — Proxy and Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — gateway/proxy fields; relevance: the gateway server config surface.
- [Claude Code — Settings Reference](../claude_code/cc_settings_reference.md) — full settings map; relevance: the field-reference precedent for browser/UI fields.
- [Hermes — Web Dashboard Overview](../hermes_agent/hermes_web_dashboard_overview.md) — control UI/dashboard; relevance: the `ui`/Control-UI config block.
- [Hermes — MsGraph Webhook Listener](../hermes_agent/hermes_msgraph_webhook_listener.md) — webhook/hooks integration; relevance: the Gmail integration / hooks config analog.
- [Band — A2A Gateway](../band/band_a2a_gateway.md) — gateway server config; relevance: gateway-server bind/TLS surface analog.
- [oc_gateway_discovery](oc_gateway_discovery.md) — discovery design (planned, this series); relevance: the design these mDNS/DNS-SD fields configure.
- [oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md) — runtime reference cluster (planned, this series); relevance: sibling field-reference cluster.
- [oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md) — ops reference cluster (planned, this series); relevance: sibling field-reference cluster.
- [oc_gateway_config_reload_rpc_env](oc_gateway_config_reload_rpc_env.md) — env-var substitution (planned, this series); relevance: the `env`/substitution surface this platform reference also touches.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: gateway/UI/discovery config validation.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — apps/Control UI; relevance: Control UI / canvas plugin host config.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: the env/discovery config root.

**Snippets**
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning; relevance: implements `gateway.tls` fingerprint pinning.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client TLS identity; relevance: the TLS config the platform reference exposes.
- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — mDNS discovery client; relevance: consumes the `discovery` mDNS/Bonjour config fields.
- [snippet_openclaw_macos_canvas_filewatcher](../../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md) — canvas plugin host; relevance: the Canvas plugin host config block.
- [snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md) — canvas lifecycle; relevance: the canvas host lifecycle the config controls.
- [snippet_openclaw_gateway_hooks_config_payload](../../code_snippets/snippet_openclaw_gateway_hooks_config_payload.md) — hooks config payload; relevance: the Hooks (Gmail integration) config block.
- [snippet_openclaw_gateway_hooks_request_handler](../../code_snippets/snippet_openclaw_gateway_hooks_request_handler.md) — hooks request handler; relevance: how hook/webhook config is dispatched.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser dispatch; relevance: the `browser` config block in action.
- [snippet_openclaw_gateway_server_http_listen_ws](../../code_snippets/snippet_openclaw_gateway_server_http_listen_ws.md) — HTTP/WS listener; relevance: the gateway bind/WS config the platform reference sets.
- [snippet_openclaw_gateway_server_runtime_config_broadcast](../../code_snippets/snippet_openclaw_gateway_server_runtime_config_broadcast.md) — runtime config broadcast; relevance: how gateway/UI config changes propagate.

### oc_gateway_config_reference_ops (8t · 10s · 10d)

**Terms**
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — credential token; relevance: Auth storage / `auth.cooldowns` + the credential surface.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — named credential set; relevance: auth-storage profiles + cooldown/disabled state config.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — pooled credentials; relevance: the supported credential surface secrets feed.
- [Secrets Manager](../../term_dictionary/term_secrets_manager.md) — external secret store; relevance: secret-providers config (`SecretRef` resolution backends).
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: the `cron` config block (retry/failureAlert/failureDestination).
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent client protocol; relevance: the `ACP` config block.
- [JSON-RPC](../../term_dictionary/term_json_rpc.md) — RPC-over-JSON; relevance: the CLI/RPC config surface in ops.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness probe; relevance: the Diagnostics/health config block.

**Docs**
- [Claude Code — Authentication](../claude_code/cc_authentication.md) — auth/credential config; relevance: analog to auth storage + credential surface.
- [Claude Code — OTel Configuration Variables](../claude_code/cc_otel_configuration_variables.md) — logging/telemetry config; relevance: the Logging/Diagnostics config blocks.
- [Claude Code — Data Usage and Telemetry](../claude_code/cc_data_usage_and_telemetry.md) — telemetry/diagnostics posture; relevance: the diagnostics config + privacy surface.
- [Hermes — Credential Pools](../hermes_agent/hermes_credential_pools.md) — credential-pool config; relevance: the credential surface secrets/auth-storage config feeds.
- [Hermes — Secrets (Bitwarden)](../hermes_agent/hermes_secrets_bitwarden.md) — secret-provider backend; relevance: the secret-providers config (`SecretRef`).
- [Hermes — Cron Internals](../hermes_agent/hermes_cron_internals.md) — cron job model; relevance: the `cron` retry/failure config block.
- [oc_gateway_diagnostics_export](oc_gateway_diagnostics_export.md) — diagnostics in action (planned, this series); relevance: the Diagnostics config block this reference exposes.
- [oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md) — runtime reference cluster (planned, this series); relevance: sibling field-reference cluster.
- [oc_gateway_config_reference_platform](oc_gateway_config_reference_platform.md) — platform reference cluster (planned, this series); relevance: sibling field-reference cluster.
- [oc_gateway_doctor](oc_gateway_doctor.md) — repair tool (planned, this series); relevance: doctor migrates the cron/auth-storage fields documented here.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: secrets/auth/logging/cron config validation.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security layer; relevance: `SecretRef` / credential surface / secret providers.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: config includes (`$include`) root + media template variables.

**Snippets**
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential order; relevance: the auth-storage credential surface this reference defines.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: `auth.cooldowns` + OAuth credential config.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credentials/secrets resolution; relevance: `SecretRef` resolution and the credential surface.
- [snippet_hermes_agent_cli_auth_storage](../../code_snippets/snippet_hermes_agent_cli_auth_storage.md) — auth storage; relevance: the auth-storage config block analog.
- [snippet_hermes_agent_cron_run_job_execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md) — cron job execution; relevance: the `cron` retry/failure config in action.
- [snippet_hermes_agent_core_logging_setup](../../code_snippets/snippet_hermes_agent_core_logging_setup.md) — logging setup; relevance: the Logging config block.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — secret-redaction patterns; relevance: the credential/secret redaction the secret surface needs.
- [snippet_hermes_agent_tools_mcp_oauth](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth.md) — MCP OAuth; relevance: OAuth credential surface for tool/MCP auth.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — provider cooldown; relevance: the `auth.cooldowns`/disabled-state semantics.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway RPC methods; relevance: the CLI/ACP/RPC config surface in ops.

### oc_gateway_diagnostics_export (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the Gateway being diagnosed/exported.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness/health probe; relevance: status/health snapshots included in the bundle.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization policy; relevance: the exec-approval gate on `/diagnostics` (never allow-all).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — credential token; relevance: `--token` + credential/token redaction in the privacy model.
- [PII](../../term_dictionary/term_pii.md) — personally identifiable info; relevance: the redaction model strips usernames/hostnames/account ids.
- [Observability of Agent Systems](../../term_dictionary/term_observability_agent_systems.md) — agent monitoring; relevance: the stability recorder + liveness/phase telemetry.
- [Agent Trajectory](../../term_dictionary/term_agent_trajectory.md) — agent run trace; relevance: Codex-harness session/thread breakdown in the report.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-driving coding agents; relevance: the Codex-harness feedback-upload path.

**Docs**
- [Claude Code — OTel Analysis and Privacy](../claude_code/cc_otel_analysis_and_privacy.md) — telemetry privacy/redaction; relevance: direct analog to the diagnostics privacy/redaction model.
- [Claude Code — Data Usage and Telemetry](../claude_code/cc_data_usage_and_telemetry.md) — what's collected/redacted; relevance: the export's keep/omit/redact contract.
- [Claude Code — Monitoring (OpenTelemetry Setup)](../claude_code/cc_monitoring_opentelemetry_setup.md) — operational metrics; relevance: the stability recorder's operational-facts stream.
- [Claude Code — OTel Configuration Variables](../claude_code/cc_otel_configuration_variables.md) — telemetry config; relevance: the `diagnostics.*` enable/snapshot config knobs.
- [Hermes — CLI Commands (Ops/Maintenance/Auth)](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md) — ops/diagnostics CLI; relevance: analog to `openclaw gateway diagnostics export`.
- [Band — Agent API Context Activity](../band/band_agent_api_context_activity.md) — activity/observability surface; relevance: the operational activity captured in the bundle.
- [oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md) — the `diagnostics.*` config block (planned, this series); relevance: where enabled/memoryPressureSnapshot are configured.
- [oc_gateway_doctor](oc_gateway_doctor.md) — companion health/repair tool (planned, this series); relevance: doctor + diagnostics are the paired support tools.
- [oc_gateway_config_reference_platform](oc_gateway_config_reference_platform.md) — logging/gateway config (planned, this series); relevance: the logging surface diagnostics summarizes.
- [oc_gateway_configuration_overview](oc_gateway_configuration_overview.md) — diagnostic-commands-when-invalid path (planned, this series); relevance: diagnostics is one of the few commands that work when config is invalid.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: the diagnostics export + stability recorder.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security layer; relevance: the redaction/privacy model for credentials.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: the logs/state layout (`~/.openclaw/logs/stability/`).

**Snippets**
- [snippet_hermes_agent_gw_memory_monitor](../../code_snippets/snippet_hermes_agent_gw_memory_monitor.md) — memory-pressure monitor; relevance: the memoryPressureSnapshot + memory-readings the bundle records.
- [snippet_hermes_agent_gw_status_snapshot](../../code_snippets/snippet_hermes_agent_gw_status_snapshot.md) — status snapshot; relevance: the sanitized Gateway status in the export.
- [snippet_hermes_agent_gw_status_health](../../code_snippets/snippet_hermes_agent_gw_status_health.md) — health status; relevance: the health snapshot included in the bundle.
- [snippet_hermes_agent_gw_shutdown_forensics](../../code_snippets/snippet_hermes_agent_gw_shutdown_forensics.md) — shutdown forensics; relevance: the persisted stability bundle after a fatal exit/restart.
- [snippet_hermes_agent_core_auxiliary_diagnostics](../../code_snippets/snippet_hermes_agent_core_auxiliary_diagnostics.md) — diagnostics assembly; relevance: how a diagnostics bundle is composed.
- [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — redaction patterns; relevance: the credential/payload redaction the privacy model applies.
- [snippet_hermes_agent_trajectory_redact_export](../../code_snippets/snippet_hermes_agent_trajectory_redact_export.md) — redacted trajectory export; relevance: the Codex session/thread breakdown with redaction.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — shutdown handling; relevance: the shutdown-timeout/restart events the stability recorder captures.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec runtime audit; relevance: the exec-approval gate on the `/diagnostics` command.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway RPC methods; relevance: where `gateway diagnostics`/`gateway stability` methods register.

### oc_gateway_discovery (8t · 10s · 10d)

**Terms**
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — mDNS/DNS-SD service discovery; relevance: the primary discovery input (`_openclaw-gw._tcp` beacon, TXT keys).
- [DNS](../../term_dictionary/term_dns.md) — domain name system; relevance: wide-area DNS-SD + MagicDNS cross-network discovery.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: the Gateway WS endpoint clients discover and connect to.
- [TLS Pinning](../../term_dictionary/term_tls_pinning.md) — fingerprint pinning; relevance: `gatewayTlsSha256` must never override a stored pin (security note).
- [TLS](../../term_dictionary/term_tls.md) — transport-layer security; relevance: secure first-time tailnet/public connect (`wss://`) requirement.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the gateway advertising the discovery beacon.
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: pairing token/keypair auth on the direct transport.
- [Access Control](../../term_dictionary/term_access_control.md) — authorization policy; relevance: gateway-owned pairing scopes/ACLs (not a raw proxy).

**Docs**
- [Claude Code — Remote Control](../claude_code/cc_remote_control.md) — remote-gateway control; relevance: the operator-remote-control problem (mac app controlling a remote gateway).
- [Claude Code — Network, TLS and Access](../claude_code/cc_network_tls_and_access.md) — network/TLS access; relevance: the secure transport-selection + TLS-pinning policy.
- [Hermes — OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md) — SSH-forwarded auth; relevance: the SSH-transport fallback (forwarding loopback gateway port).
- [Band — WebSocket Overview](../band/band_websocket_overview.md) — WS transport design; relevance: the direct-WS transport clients discover.
- [Band — A2A Gateway](../band/band_a2a_gateway.md) — gateway discovery/transport; relevance: gateway-as-discovery-owner design analog.
- [Hermes — Desktop Remote Backend](../hermes_agent/hermes_desktop_remote_backend.md) — desktop→remote-gateway link; relevance: the macOS-app-picks-a-gateway transport-selection flow.
- [oc_gateway_config_reference_platform](oc_gateway_config_reference_platform.md) — Discovery mDNS/DNS-SD config fields (planned, this series); relevance: the config that drives this discovery design.
- [oc_gateway_configuration_overview](oc_gateway_configuration_overview.md) — `gateway.bind` config (planned, this series); relevance: the bind-mode config that controls beacon advertising.
- [oc_gateway_doctor](oc_gateway_doctor.md) — pairing/port diagnostics (planned, this series); relevance: doctor detects pairing trouble + gateway port collisions.
- [oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md) — auth/identity config (planned, this series); relevance: the auth/identity surface pairing relies on.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: advertises beacons, owns pairing/auth, hosts the WS endpoint.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — apps; relevance: the macOS app that picks a gateway / shows pairing prompts.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: the `bonjour` bundled plugin + bind modes.

**Snippets**
- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — mDNS browse client; relevance: the client-side Bonjour/DNS-SD browse + "pick a gateway" flow.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS pairing; relevance: the iOS/Android node pairing + first-time fingerprint trust.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — gateway pairing decisions; relevance: gateway as source of truth for node admission.
- [snippet_openclaw_gateway_call_method_gating](../../code_snippets/snippet_openclaw_gateway_call_method_gating.md) — method scopes/ACLs; relevance: the scopes/ACLs (not a raw proxy) the gateway enforces.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — client connect/SSH proxy; relevance: the SSH-transport fallback connect path.
- [snippet_openclaw_kit_gateway_tls_pinning](../../code_snippets/snippet_openclaw_kit_gateway_tls_pinning.md) — TLS pinning; relevance: pinning the discovered `gatewayTlsSha256` fingerprint.
- [snippet_openclaw_gateway_client_identity_tls](../../code_snippets/snippet_openclaw_gateway_client_identity_tls.md) — client TLS identity; relevance: secure direct-WS transport identity.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session; relevance: the paired Gateway-WS node session after discovery.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway WS channel; relevance: the direct-WS endpoint discovery resolves to.
- [snippet_openclaw_android_gateway_session_ws](../../code_snippets/snippet_openclaw_android_gateway_session_ws.md) — WS session client; relevance: connecting to the discovered/paired Gateway WS.

### oc_gateway_doctor (8t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product; relevance: the product `doctor` repairs/migrates.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema validation; relevance: doctor diagnoses/fixes the validation failures that block startup.
- [Health Check](../../term_dictionary/term_health_check.md) — liveness probe; relevance: the health check + restart prompt doctor runs.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — credential token; relevance: model-auth health — OAuth expiry refresh + cooldown reporting.
- [Cron](../../term_dictionary/term_cron.md) — scheduled jobs; relevance: legacy cron-store migration.
- [Sandbox](../../term_dictionary/term_sandbox.md) — isolated execution; relevance: sandbox image repair when sandboxing is enabled.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin declaration; relevance: legacy plugin-manifest contract-key migration (`*Providers` → `contracts`).
- [Authentication](../../term_dictionary/term_authentication.md) — identity verification; relevance: device-pairing trouble detection + gateway auth checks.

**Docs**
- [Claude Code — Debug Your Configuration](../claude_code/cc_debug_your_configuration.md) — config diagnosis/repair; relevance: the closest analog to doctor's config-normalization/lint pass.
- [Claude Code — Settings Files](../claude_code/cc_settings_files.md) — config files + migrations; relevance: the legacy-config-key migration surface doctor rewrites.
- [Claude Code — Authentication](../claude_code/cc_authentication.md) — auth/credential health; relevance: doctor's model-auth health + OAuth refresh checks.
- [Hermes — CLI Commands (Ops/Maintenance/Auth)](../hermes_agent/hermes_cli_commands_ops_maintenance_auth.md) — ops/doctor-style CLI; relevance: direct analog to `openclaw doctor` repair/lint commands.
- [Hermes — Migrate From OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — config/state migration; relevance: the legacy on-disk state + config migrations doctor performs.
- [Hermes — Cron Internals](../hermes_agent/hermes_cron_internals.md) — cron job model; relevance: the legacy cron-store migration doctor applies.
- [oc_gateway_configuration_overview](oc_gateway_configuration_overview.md) — validation-failure → `doctor --fix` path (planned, this series); relevance: doctor is the recovery path when strict validation fails.
- [oc_gateway_diagnostics_export](oc_gateway_diagnostics_export.md) — companion diagnostics tool (planned, this series); relevance: doctor + diagnostics are the paired support tools.
- [oc_gateway_config_reference_ops](oc_gateway_config_reference_ops.md) — cron/auth-storage fields (planned, this series); relevance: the fields doctor migrates/repairs.
- [oc_gateway_config_reference_runtime](oc_gateway_config_reference_runtime.md) — provider/model runtime fields (planned, this series); relevance: the Codex-route/provider-runtime cleanup doctor performs.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway runtime; relevance: gateway runtime/service/port checks doctor runs.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: config normalization + legacy migrations.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session runtime; relevance: session lock/transcript repair.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security layer; relevance: config-permission chmod 600 + auth health checks.

**Snippets**
- [snippet_hermes_agent_cli_doctor_primitives](../../code_snippets/snippet_hermes_agent_cli_doctor_primitives.md) — doctor check primitives; relevance: the check/repair primitive model doctor uses.
- [snippet_hermes_agent_cli_doctor_entry_early_checks](../../code_snippets/snippet_hermes_agent_cli_doctor_entry_early_checks.md) — doctor early checks; relevance: the quick-start/pre-flight checks.
- [snippet_hermes_agent_cli_doctor_auth_dirs](../../code_snippets/snippet_hermes_agent_cli_doctor_auth_dirs.md) — doctor auth/dir checks; relevance: auth-storage + config-dir permission checks.
- [snippet_hermes_agent_cli_doctor_api_connectivity](../../code_snippets/snippet_hermes_agent_cli_doctor_api_connectivity.md) — doctor connectivity checks; relevance: the model-auth/connectivity health checks.
- [snippet_hermes_agent_cli_doctor_late_sections_summary](../../code_snippets/snippet_hermes_agent_cli_doctor_late_sections_summary.md) — doctor summary output; relevance: the "What it does (summary)" catalog rendering.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — Dreams diary repair/cron; relevance: directly implements the Dreams UI backfill/reset doctor-style RPC.
- [snippet_hermes_agent_cli_config_migrate](../../code_snippets/snippet_hermes_agent_cli_config_migrate.md) — config migration; relevance: the legacy-config-key migrations doctor applies.
- [snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md) — config validation; relevance: the read-only lint mode validating config.
- [snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md) — startup runtime attach; relevance: gateway runtime/service checks (installed-but-not-running).
- [snippet_hermes_agent_gw_session_lifecycle](../../code_snippets/snippet_hermes_agent_gw_session_lifecycle.md) — session lifecycle; relevance: session lock inspection + stale-lock cleanup.

> **DB-verification note (xref-augment 2026-06-21):** every EXISTING `term_*`/`snippet_*`/`repo_*`/`cc_*`/`hermes_*`/
> plan-stage candidate list cited a slug that does not exist as an exact id (`term_secrets_management`, `term_mdns`,
> `term_bonjour`, `term_tailscale`, `term_pairing`, `term_metrics`, `term_telemetry`, `term_observability`), a
> `term_dns`/`term_tls_pinning`, `term_authentication`/`term_access_control`, `term_observability_agent_systems`).
> Sibling `oc_*` ids are this-series planned notes (not yet in the DB) and count toward the 10-doc floor only as

## Undigested Terms Plan

Per master: OpenClaw vocabulary terms are digested as `oc_*` doc concept notes by their home sub-plan, NOT as new
`term_dictionary` entries; the only `term_dictionary` interaction is **linking existing** terms.

| Term (appears in source) | Disposition |
|---|---|
| tool profile / tool group / `tools.profile` | Digested in `oc_gateway_config_tools_policy` (note 1); no term note. Link `term_tool_registry`/`term_function_calling`. |
| sandbox tool policy / `tools.sandbox` | Digested in note 1; link existing `term_sandbox`. |
| `bundle-mcp` / MCP server glob | Digested in note 1; link existing `term_mcp` / `term_mcp_gateway`. |
| custom provider / base-URL override / OpenAI-compatible endpoint | Digested in `oc_gateway_config_custom_providers` (note 2); link `term_provider_plugin`/`term_reverse_proxy`/`term_api_gateway`. |
| JSON5 config / strict schema validation | Digested in notes 3, 6–8; link existing `term_json_schema`. |
| hot reload / reload modes / Config RPC | Digested in `oc_gateway_config_reload_rpc_env` (note 4); link `term_json_rpc`. |
| `SecretRef` / credential surface / secret providers | Digested in `oc_gateway_config_reference_ops` (note 8) + cross-link gw05/gw06 secrets pages; link `term_oauth_token`. (No existing `term_secrets_management`; not promoted here — gw05/gw06 own the deep secrets surface.) |
| diagnostics bundle / stability recorder / privacy model | Digested in `oc_gateway_diagnostics_export` (note 9); link `term_health_check`. |
| Bonjour / mDNS / DNS-SD / Tailnet / MagicDNS / SSH transport | Digested in `oc_gateway_discovery` (note 10); link existing `term_dns`/`term_tls`. (No existing `term_bonjour`/`term_mdns`/`term_tailscale`; documented as discovery-design prose, not promoted — see new-term note below.) |
| `openclaw doctor` / read-only lint / migrations | Digested in `oc_gateway_doctor` (note 11); link `term_json_schema`/`term_health_check`. |
| device pairing / pairing token / scopes/ACLs | Digested in notes 10–11; link `term_authentication`/`term_access_control`. (No existing `term_pairing`; gw04 `gateway/pairing` owns the pairing concept.) |

**New-term candidates (cross-cutting, no doc-page home AND no existing note):** **0 expected.** All vocabulary above
has either a doc-page home (an `oc_*` note in this or a sibling sub-plan) or an existing term to link. The closest
genuinely cross-cutting candidate, **zero-configuration networking / mDNS+DNS-SD service discovery** (no
`term_mdns`/`term_zero_conf`/`term_bonjour` exists), is NOT promoted here: it is owned by gw01 `gateway/bonjour` +
gw03 (`local-model-services`) as a discovery concept, and `oc_gateway_discovery` digests the design directly. If a
later sub-plan finds it genuinely reusable vault-wide, capture via `/tessellum-capture-term-note` as
`term_dns_sd_discovery` (best-fit slug; collision-checked vs existing `term_dns`) and add to
`0_entry_points/acronym_glossary_systems.md` (network/systems vocabulary) — flagged for the master, not done here.

## Term-Note Authoring Requirements

**N/A for gw02 — authors zero `term_dictionary` notes.** (Inherited from master: OpenClaw vocabulary is digested as
`oc_*` doc notes, never as inlined term definitions; existing terms are linked only.) If a future augment promotes

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P1). All gates must PASS before commit.

| Gate | Check | Tool / criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` — YAML field order, H1 `# OpenClaw — …`, `## Overview` + `## Related Notes` present, footer. |
| G2 | Grounding | Diff each note vs `inbox/openclaw_docs/gateway/<page>.md`; no claim absent from source; code fences verbatim. |
| G3 | Density + Coverage | ≤400 lines · ≤2,500 words · ≤6 code blocks · one building_block; every mapped H2/H3 covered (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevance-selected `term_dictionary` terms + repo_openclaw* + sibling `oc_*`, each indexed `[text](path.md)` link with a relevance statement. |
| G6 | Broken-link | `/tessellum-fix-broken-links` — 0 broken relative paths after reindex. |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (anti-island). |
| G8 | In-degree ≥1 | Confirmed via `note_links` after reindex; satisfied via `entry_openclaw_docs.md` rows + repo/term inlinks. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_gateway_config_tools_policy oc_gateway_config_custom_providers oc_gateway_configuration_overview oc_gateway_config_reload_rpc_env oc_gateway_configuration_examples oc_gateway_config_reference_runtime oc_gateway_config_reference_platform oc_gateway_config_reference_ops oc_gateway_diagnostics_export oc_gateway_discovery oc_gateway_doctor"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density (body words excl. frontmatter; code blocks)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code / $lines L)"
  # G4 sibling-prefix cross-ref presence
  grep -q "($SIBLING_PREFIX" "$f" || echo "NO SIBLING $SIBLING_PREFIX XREF in $n"
done

# G1 YAML frontmatter (whole folder)
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost / G6 broken-link / G8 in-degree after reindex
bash scripts/update_notes_database.sh --force
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w / ≤6 code / ≤400L)? |
|---|---|---|---:|---:|---|
| 1 | oc_gateway_config_tools_policy | procedure | 700 | ≤6 | ✅ |
| 2 | oc_gateway_config_custom_providers | procedure | 500 | ≤4 | ✅ |
| 3 | oc_gateway_configuration_overview | procedure | 700 | ≤5 | ✅ |
| 4 | oc_gateway_config_reload_rpc_env | procedure | 600 | ≤4 | ✅ |
| 5 | oc_gateway_configuration_examples | procedure | 650 | ≤6 | ✅ |
| 6 | oc_gateway_config_reference_runtime | model | 700 | ≤6 | ✅ |
| 7 | oc_gateway_config_reference_platform | model | 650 | ≤6 | ✅ |
| 8 | oc_gateway_config_reference_ops | model | 700 | ≤6 | ✅ |
| 9 | oc_gateway_diagnostics_export | procedure | 600 | ≤6 | ✅ |
| 10 | oc_gateway_discovery | concept | 550 | 0 | ✅ |
| 11 | oc_gateway_doctor | procedure | 750 | ≤4 | ✅ (borderline — watch at execution; promote a split if it overruns 2,500w) |

No note approaches the caps. The code-dense reference page (34 fences) is split ×3 and the tools page (18 fences) ×2
so each note stays ≤6 code blocks; only the most-illustrative `json5` snippets are reproduced verbatim.

## Entry Point Decision (inherited from master)

Contributes **11 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step, `building_block: navigation`)
under a "Gateway — Configuration & Operability" cluster (gw02). Each note also gets its entry-point back-link at
finalization (this is the G7/G8 outside-folder inbound link). No new entry point is created by this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution):

- `entry_openclaw_docs.md` → all 11 notes (the primary anti-island inbound link).
- `repo_openclaw_gateway.md` → notes 1, 3, 4, 6, 7, 8, 9, 11 (the code-side gateway counterpart).
- `repo_openclaw_extensions_llm_providers.md` → note 2 (custom-provider config).
- `repo_openclaw_security.md` → notes 8, 9 (secrets/credential-surface + diagnostics redaction).
- `repo_openclaw_sessions.md` → notes 4, 11 (reload-vs-restart per session; session lock/transcript repair).
- `repo_openclaw_apps.md` → notes 7, 10 (Control UI / canvas host; macOS app gateway discovery).
- `term_openclaw.md` → notes 3, 10, 11 (the configured/discovered/repaired product).
- `term_mcp.md` → note 1; `term_dns.md` → notes 7, 10; `term_oauth_token.md` → notes 8, 9, 11.

## Pacing Rules (inherited from master)

One execution phase; all 8 gates PASS before commit. Re-read each source page at execution; config snippets
reproduced verbatim. One BB per note (procedure ×7 · model ×3 · concept ×1). Cap dynamic-workflow fan-out at
~30 agents/run; reindex incrementally; verify `note_links` + 0 broken links before commit; `git pull --rebase
--autostash` first; no Claude co-author trailer; commit + push after the phase.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment: per-note mapping locked at raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**Per-note counts (locked).**

| Note | Terms | Snippets (all existing) | Docs total | Docs existing | Docs planned-sibling | Repos | Floors met |
|---|---:|---:|---:|---:|---:|---:|---|
| oc_gateway_config_tools_policy | 10 | 10 | 10 | 7 | 3 | 3 | ✅ |
| oc_gateway_config_custom_providers | 10 | 10 | 10 | 8 | 2 | 3 | ✅ |
| oc_gateway_configuration_overview | 8 | 10 | 10 | 6 | 4 | 3 | ✅ |
| oc_gateway_config_reload_rpc_env | 8 | 10 | 10 | 6 | 4 | 3 | ✅ |
| oc_gateway_configuration_examples | 9 | 10 | 10 | 6 | 4 | 3 | ✅ |
| oc_gateway_config_reference_runtime | 10 | 10 | 10 | 7 | 3 | 5 | ✅ |
| oc_gateway_config_reference_platform | 8 | 10 | 10 | 6 | 4 | 3 | ✅ |
| oc_gateway_config_reference_ops | 8 | 10 | 10 | 6 | 4 | 3 | ✅ |
| oc_gateway_diagnostics_export | 8 | 10 | 10 | 6 | 4 | 3 | ✅ |
| oc_gateway_discovery | 8 | 10 | 10 | 6 | 4 | 3 | ✅ |
| oc_gateway_doctor | 8 | 10 | 10 | 6 | 4 | 4 | ✅ |




## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table present per batch (G1–G6 + G8) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost, G6 Broken-link, G7/G8 Discoverability+In-degree for the single P1 phase. |
| CP4 | Plan size manageable (≤30 or split) | **PASS** | 11 planned notes ≤ 30; self-contained sub-plan of the 105-sub-plan master. |
| CP5 | Note format aligned + DERIVED from existing notes | **PASS** | Master Format Definition derived from existing `claude_code/cc_*` notes; verified against `cc_sandbox_modes.md` (YAML order tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group; H1 `# OpenClaw — …`; `## Overview`; `## Related Notes`; bold footer). Not invented. |
| CP6 | Borderline density → split promoted | **PASS** | `## Density Re-Assessment`: all ≤750w / ≤6 code / ≤400L. Note 11 (doctor, 750w) flagged borderline with an execution-time split trigger. configuration-reference (8,397w) split ×3, config-tools (3,803w) ×2, configuration (3,504w) ×2 — all source pages >2,500w are split. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured all 7 pages via `wc -w` / `grep -c '^\`\`\`'` on 2026-06-21: **exact match** to the plan's Source table (25,543w total). Ratio 1.00 — no under-estimation. |
| CP8 | Undigested Terms Plan + Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (every row dispositioned to an `oc_*` home + existing term to link); `## Term-Note Authoring Requirements` present, correctly N/A (gw02 authors 0 term notes per master design). |
| CP8f | Slug specificity + all-notes (term AND doc) dedup/collision audit | **PASS** | Doc-note collision audit run: each planned `oc_*` is a NEW slug (none exist in DB) and none duplicates an existing `term_*`/doc — the gateway-config `oc_*` topics have no existing substantive doc note (verified `entry_openclaw_docs`/`oc_*` absent). Term substitutions documented in the Augmentation Report's slug-correction note; no too-general or duplicate term slug is created (0 new terms). |
| CP9 | Discoverability — inbound links executed (G8), no islands | **PASS** | `## Inlinks (existing notes → new notes)` maps an outside-folder inbound link to all 11 notes (`entry_openclaw_docs` → all 11, plus `repo_openclaw_gateway`/`repo_openclaw_extensions_llm_providers`/`repo_openclaw_security`/`repo_openclaw_sessions`/`repo_openclaw_apps`/`term_*` per-note); G8 in-degree ≥1 is in the gate table as an EXECUTED/verified step, not a recommendation. |


## Plan Amendments (by master agent during execution)

| Date | Section | Original | Amended | Rationale |
|---|---|---|---|---|
| 2026-06-23 | Planned Notes | oc_gateway_config_reference_ops (1 model note, secrets/auth/logging/diagnostics/update/acp/cli/cron/media/$include) | SPLIT into oc_gateway_config_reference_ops (secrets/auth/logging/diagnostics) + oc_gateway_config_reference_ops_jobs (update/acp/cli/wizard/identity/bridge/cron+retry/failureAlert/failureDestination/media-template-vars/$include) | Source `configuration-reference.md` is ~8,400w; the ops note ran 2866w > 2500 cap. User directive: split when density too high, no drop/omit. Both halves model BB. gw02 note count +1. |
| 2026-06-23 | Planned Notes | oc_gateway_config_reference_platform (1 model note, browser/ui/gateway/hooks/canvas/discovery/env) | SPLIT into oc_gateway_config_reference_platform (browser/ui/gateway-server +tls +reload) + oc_gateway_config_reference_surfaces (hooks+Gmail/canvas/discovery/env) | Same source page; platform note ran 2714w > 2500 cap. Split, not compressed. Both halves model BB. gw02 note count +1 → 13 total. |
