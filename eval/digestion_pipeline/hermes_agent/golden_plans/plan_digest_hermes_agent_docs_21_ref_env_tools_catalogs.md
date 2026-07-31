---
title: Hermes Agent Docs Digestion — Sub-Plan 21 — Reference: Env Vars, Tools/Toolsets, Skills Catalogs, MCP-config, Model-catalog, FAQ
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/reference/
pages:
  - reference/environment-variables.md
  - reference/faq.md
  - reference/tools-reference.md
  - reference/toolsets-reference.md
  - reference/mcp-config-reference.md
  - reference/model-catalog.md
  - reference/skills-catalog.md
  - reference/optional-skills-catalog.md
  - reference/automation-blueprints-catalog.mdx
---

# Sub-Plan 21: Reference — Env Vars, Tools/Toolsets, Skills Catalogs, MCP-config, Model-catalog, FAQ

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). This file is the ONLY place SP21's note
> filenames/BBs/coverage are defined.

## Scope

The **reference layer** of the Hermes Agent docs: the complete environment-variable table, the
built-in tools registry + the toolset grouping/activation model, the MCP server-config schema, the
model-catalog manifest, the bundled + optional skills catalogs, the automation-blueprints stub, and
the troubleshooting FAQ. Source = 9 mirrored pages in `inbox/hermes_agent_docs/reference/` (8
substantive + 1 stub merged). **P3 / reference** — these are look-up notes that downstream and
upstream notes link INTO; SP21 itself owns **0 captures** (no new term notes) — every Hermes concept
it touches is owned by a feature sub-plan (link at finalization) or is an existing verified term.
Notes here are `model`/`navigation`/`procedure` BB enumerations that cross-link DOWN to the
`snippet_hermes_agent_tools_*`/`cli_*`/`core_*` implementation layer.

## Content Strategy

- **One BB per note.** The two largest pages (`environment-variables` 9291w; `tools-reference` 3235w,
  79 tools) split by category cluster; `faq` splits by problem domain (see Split Decisions).
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: every
  env var / tool / toolset configures a feature whose concept + how-to is owned by its home SP
  (config SP02, providers SP14/SP09, messaging SP11-13, media/web SP08, skills SP05, MCP/ACP SP09,
  automation SP06, dashboard SP10). SP21 captures the *reference enumeration*, not the feature prose.
- **Collision (augment): `term_model_catalog.md` (active) is the generic concept** — a textbook LIKE
  match; the planned `hermes_model_catalog_reference` is a Hermes-specific manifest-schema reference
  (URL, JSON schema, fetch/override behavior) → LINK the term, do NOT recreate.
- **Collision: `term_prfaq.md` (active) is the Amazon PR/FAQ document format**, unrelated to Hermes'
  troubleshooting FAQ — a LIKE false-positive; the planned `hermes_faq_*` notes are NOT a dup; do NOT
  link the unrelated term.
- `automation-blueprints-catalog.mdx` is a 189-word stub (client-rendered blueprint gallery + one
  "Writing your own" pointer) → **NOT a standalone note; merged** into the bundled-skills catalog note
  (Note 8) as a short blueprint-gallery section + link-out to SP17's `guides/automation-blueprints`
  (recorded in the coverage map).

## Source Pages (Re-measured 2026-06-19, mirror c253b07 — wc)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| reference/environment-variables.md | 9291 | 2 | MIXED model+settings reference | 2 (split) |
| reference/faq.md | 4699* | 44 | procedure (troubleshooting) | 2 (split) |
| reference/tools-reference.md | 3235 | 0 | model (tool registry) | 2 (split) |
| reference/optional-skills-catalog.md | 2911 | 3 | navigation (catalog) | 1 |
| reference/toolsets-reference.md | 1493 | 6 | model (toolset grouping) | 1 |
| reference/skills-catalog.md | 1420 | 0 | navigation (catalog) | 1 |
| reference/mcp-config-reference.md | 1044 | 15 | procedure (config schema) | 1 |
| reference/model-catalog.md | 500 | 5 | model (manifest schema) | 1 |
| reference/automation-blueprints-catalog.mdx | 189 | 0 | — (stub) | 0 (merge → Note 8) |

> *faq.md: master ledger reports 4699w/44code (counts in-code-fence prose). `wc` over the body
> excluding the 44 code fences = ~1142 prose words; the page is heavily command-block driven. Either
> figure confirms the SPLIT-2 decision (44 code blocks > 6 cap → must split). Density re-assessment
> uses the per-note curated-block counts below.

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **11 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_env_vars_providers_auth_tools.md` | model | env-vars §LLM Providers, §Provider Auth (OAuth), §Tool APIs (+Langfuse Observability, +Nous Tool Gateway) | ~1400 | Reference half 1: the provider/auth/tool-API environment variables — `*_API_KEY`/`*_BASE_URL` per inference provider, Anthropic/Nous OAuth knobs, search/FAL/voice tool-API keys, Langfuse observability, Nous Tool Gateway billing vars; all live in `~/.hermes/.env` or via `hermes config set`. |
| 2 | `hermes_env_vars_runtime_messaging_behavior.md` | model | env-vars §Terminal Backend, §SSH Backend, §Container Resources, §Persistent Shell, §Messaging (+Web Dashboard, MS-Graph ×3, Teams summary, LINE, ntfy, Advanced Messaging Tuning), §Agent Behavior, §Interface, §Session Settings, §Context Compression, §Auxiliary Task Overrides, §Fallback Providers, §Provider Routing | ~1500 | Reference half 2: the terminal/SSH/container/persistent-shell backend vars, the messaging-gateway + per-platform vars (dashboard, MS-Graph, LINE, ntfy, tuning), and the agent-behavior/interface/session/context-compression/auxiliary/fallback/routing config-only vars. |
| 3 | `hermes_tools_reference_core.md` | model | tools-reference §file, §code_execution, §cronjob, §delegation, §memory, §session_search, §skills, §terminal, §todo, §clarify, §moa, §vision (+intro Quick Counts, +MCP-tools tip) | ~1300 | Built-in tools registry, group 1 (core agent tools): file (`patch`/`read_file`/`search_files`/`write_file`), `terminal`+`process`, `execute_code`, `cronjob`, `delegate_task`, `memory`, `session_search`, `skill_view`/`skill_manage`/`skills_list`, `todo`, `clarify`, `mixture_of_agents`, `vision_analyze`; plus the ~71-tool quick-count and the `mcp_<server>_` dynamic-tool note. |
| 4 | `hermes_tools_reference_platform_media.md` | model | tools-reference §browser (+CDP-gated), §computer_use, §image_gen, §video/§video_gen, §web, §x_search, §tts, §kanban, §messaging, §homeassistant, §discord/§discord_admin, §spotify, §feishu_doc/§feishu_drive, §hermes-yuanbao | ~1400 | Built-in tools registry, group 2 (platform + media + browser tools): the 10 `browser_*` (+2 CDP-gated) tools, `computer_use`, `image_generate`/`video_generate`/`video_analyze`, `web_search`/`web_extract`, `x_search`, `text_to_speech`, the 9 `kanban_*` tools, `send_message`, Home Assistant, Discord (+admin), Spotify, Feishu doc/drive, Yuanbao — each with its gating credential/platform. |
| 5 | `hermes_toolsets_reference.md` | model | toolsets-reference §How Toolsets Work, §Configuring Toolsets (per-session/per-platform/interactive), §Core Toolsets, §Platform Toolsets, §Dynamic Toolsets (MCP/plugin/custom/wildcards), §Relationship to `hermes tools` | ~1100 | The toolset grouping model: how tools are bundled into named toolsets, the three activation surfaces (CLI `--toolsets`, `config.yaml` per-platform, interactive `hermes tools`), the core vs platform vs dynamic (MCP/plugin/custom) toolset tiers, wildcard matching, and how it relates to `hermes tools`. |
| 6 | `hermes_mcp_config_reference.md` | procedure | mcp-config-reference §Root config shape, §Server keys, §`tools` policy keys, §Filtering semantics (include/exclude/precedence), §Utility-tool policy (resources/prompts/capability-aware), §`enabled: false`, §Empty result behavior, §Example configs (allowlist/blacklist/resource-only/mTLS), §Reloading config, §Tool naming (+sanitization), §OAuth 2.1 authentication | ~1300 | The `mcp_servers` config schema reference: root shape, per-server keys, the `tools` include/exclude allow/deny policy + precedence, utility-tool (resources/prompts) toggles, `enabled: false`, 4 worked example configs (GitHub allowlist, Stripe blacklist, resource-only, mTLS), live config reload, tool-name sanitization, and MCP OAuth 2.1 (PKCE) auth. |
| 7 | `hermes_model_catalog_reference.md` | model | model-catalog §Live manifest URL, §Schema, §Fetch behavior, §Config (+Per-provider override URLs), §Updating the manifest | ~700 | The model-catalog manifest reference: the live manifest URL, the per-model JSON schema (id, context window, modality, pricing), fetch/cache behavior, the `config.yaml` knobs + per-provider override URLs, and how the manifest is regenerated from the in-repo model lists. |
| 8 | `hermes_skills_catalog_bundled.md` | navigation | skills-catalog ALL §category sections (apple…yuanbao); + merged automation-blueprints-catalog §gallery + §Writing your own | ~1100 | Catalog of the bundled skills shipped with Hermes, grouped by category (apple, autonomous-ai-agents, creative, data-science, devops, email, github, media, mlops, note-taking, productivity, research, smart-home, social-media, software-development, yuanbao); plus a short automation-blueprints gallery pointer (link-out to SP17's build guide). |
| 9 | `hermes_optional_skills_catalog.md` | navigation | optional-skills-catalog §intro + ALL §category sections (autonomous-ai-agents, blockchain, communication, creative, devops, dogfood, email, finance, gaming, health, mcp, migration, mlops, productivity, research, security, software-development, web-development), §Contributing Optional Skills | ~1100 | Catalog of optional (install-on-demand) skills, grouped by category, plus how to install them and the Contributing-Optional-Skills pointer; the on-demand counterpart to the bundled catalog. |
| 10 | `hermes_faq_install_provider_terminal.md` | procedure | faq §FAQ (LLM providers, Windows, WSL2 Chrome, Android/Termux, data privacy, offline/local, cost, multi-user, memory-vs-skills, Python project), §Troubleshooting → Installation Issues, → Provider & Model Issues, → Terminal Issues | ~1500 | FAQ half 1: the common questions (providers, OS support, privacy, offline, cost, memory-vs-skills, Python embedding) plus installation, provider/model, and terminal/Docker troubleshooting fixes (PATH reload, Python upgrade, no-sudo cleanup, provider re-setup, model list, context overflow, docker group). |
| 11 | `hermes_faq_messaging_perf_profiles_workflows.md` | procedure | faq §Troubleshooting → Messaging Issues, → Performance Issues, → MCP Issues; §Profiles (5 Qs); §Workflows & Patterns (multi-model, per-chat binding, hiding logs, slash limit, shared threads, export, single-profile move, `hermes backup` vs `profile export`, permission-denied, error-400) | ~1500 | FAQ half 2: messaging-gateway / performance / MCP troubleshooting, the profiles Q&A, and the workflow-pattern recipes (multi-model tasks, per-chat agent binding, hiding logs/reasoning, Telegram slash-command limit, shared thread sessions, exporting/moving profiles, backup-vs-export, permission-denied + error-400 fixes). |

**SP21 totals:** 11 notes · model 5 · navigation 2 · procedure 4 · concept 0 (all concepts are existing
term notes or owned by feature SPs). 8 source pages digested (all substantive), 0 skipped,
automation-blueprints-catalog stub merged into Note 8.

## Summary Statistics & Building Block Distribution

- Notes: 11 · model 5 · navigation 2 · procedure 4 · concept 0 (reference layer — concepts live in term notes / feature SPs).
- Source: 8 digested pages (~24.6K words incl. code) → ~12.9K words of notes (compression via reference-table condensing + feature link-outs).
- BB mix: model 45%, procedure 36%, navigation 18%.

## Section Coverage Map

```
environment-variables.md (9291w)
├── LLM Providers / Provider Auth (OAuth) / Tool APIs (+Langfuse, +Nous Tool Gateway) → Note 1 (provider concepts→SP14/SP09)
├── Terminal Backend / SSH Backend / Container Resources / Persistent Shell ───────── → Note 2 (backend model→SP02 hermes_terminal_backends)
├── Messaging (+Web Dashboard, MS-Graph ×3, Teams summary, LINE, ntfy, Advanced Tuning) → Note 2 (per-platform setup→SP11-13; dashboard→SP10)
└── Agent Behavior / Interface / Session / Context Compression / Auxiliary / Fallback / Provider Routing → Note 2 (compression→SP18; fallback/routing→SP09)
faq.md (4699w / 44 code)
├── FAQ Qs (providers/Windows/WSL2/Android/privacy/offline/cost/multi-user/memory-vs-skills/Python) → Note 10 (feature detail→SP05/SP14/SP17)
├── Troubleshooting → Installation Issues / Provider & Model Issues / Terminal Issues → Note 10 (install→SP01; config→SP02)
├── Troubleshooting → Messaging Issues / Performance Issues / MCP Issues ──────────── → Note 11 (messaging→SP11-13; mcp→SP09)
├── Profiles (5 Qs) ───────────────────────────────────────────────────────────────── → Note 11 (profiles concept→SP04)
└── Workflows & Patterns (10 recipes) / Still Stuck? ─────────────────────────────── → Note 11 (sessions→SP02; cron→SP06)
tools-reference.md (3235w, 0 code)
├── intro Quick Counts + MCP-tools tip ──────────────────────────────────────────── → Note 3 (overview) (mcp→SP09)
├── file / code_execution / cronjob / delegation / memory / session_search / skills / terminal / todo / clarify / moa / vision → Note 3
└── browser (+CDP) / computer_use / image_gen / video(+gen) / web / x_search / tts / kanban / messaging / homeassistant / discord(+admin) / spotify / feishu_doc(+drive) / hermes-yuanbao → Note 4
toolsets-reference.md (1493w) ── ALL sections ───────────────────────────────────── → Note 5 (mcp→SP09; plugins→SP06; hermes tools→SP20)
mcp-config-reference.md (1044w) ── ALL sections ─────────────────────────────────── → Note 6 (mcp feature→SP09; OAuth/PKCE→SP09)
model-catalog.md (500w) ── ALL sections ─────────────────────────────────────────── → Note 7 (configuring-models→SP02; providers→SP14)
skills-catalog.md (1420w) ── ALL category sections ──────────────────────────────── → Note 8 (skills feature→SP05; work-with-skills→SP17)
automation-blueprints-catalog.mdx (189w) ── gallery + Writing your own ──────────── → MERGE into Note 8 (link-out to SP17 guides/automation-blueprints)
optional-skills-catalog.md (2911w) ── intro + ALL category sections + Contributing → Note 9 (skills feature→SP05; mcp skills→SP09)
```

No source H2/H3 orphaned. All 8 substantive pages fully covered; the stub is merged (recorded above);
feature-page detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| environment-variables.md (9291w, 2 code) | Note 1 (providers/auth/tool-API vars) + Note 2 (terminal/messaging/agent-behavior vars) | >2500w (×3.7); two cohesive clusters — "what to authenticate against" (providers/auth/tool keys) vs "how the runtime/gateway behaves" (backends/messaging/behavior/config-only). |
| faq.md (4699w, 44 code) | Note 10 (FAQ Qs + install/provider/terminal troubleshooting) + Note 11 (messaging/perf/mcp + profiles + workflows) | 44 code blocks > 6 cap → must split; two problem domains — first-run setup vs operate/scale (messaging, profiles, workflow recipes). |
| tools-reference.md (3235w, 79 tools) | Note 3 (core agent toolsets) + Note 4 (platform + media + browser toolsets) | >2500w; the registry naturally bisects into local-agent tools (file/terminal/code/memory/skills/delegation/cron) vs platform/media/browser tools (browser/cdp/computer_use/image/video/web/x/tts/kanban/messaging/HA/discord/spotify/feishu/yuanbao). |
| automation-blueprints-catalog.mdx (189w stub) | MERGE → Note 8 | 189w client-rendered gallery; too thin for a standalone note — folded into the bundled-skills catalog as a blueprint-gallery section + link-out to SP17's `guides/automation-blueprints`. |

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| `hermes_model_catalog_reference` | `term_model_catalog.md` (active) | **NOT a dup** — that term is the *generic concept* (catalog of available models); this note is Hermes' concrete manifest-URL + JSON-schema + fetch/override reference (classic LIKE match, master caution list) | CREATE; LINK `term_model_catalog` as a related component term. |
| `hermes_faq_install_provider_terminal`, `hermes_faq_messaging_perf_profiles_workflows` | `term_prfaq.md` (active) | **NOT a dup** — `term_prfaq` is the Amazon *PR/FAQ document format*, unrelated to Hermes troubleshooting (LIKE false-positive) | CREATE; do NOT link the unrelated term. |
| `hermes_env_vars_providers_auth_tools`, `hermes_env_vars_runtime_messaging_behavior` | no term/doc note named `environment_variable*` (DB returns none) | NEW | CREATE; LINK component terms (`term_oauth_token`, `term_authentication`, `term_provider_plugin`, …). |
| `hermes_tools_reference_core`, `hermes_tools_reference_platform_media`, `hermes_toolsets_reference` | no `tool_registry`/`toolset`/`built_in_tool` term or doc note (DB returns none) | NEW | CREATE; LINK `term_function_calling`/`term_guardrails`/component terms. |
| `hermes_mcp_config_reference` | `term_mcp.md`, `term_mcp_gateway.md` (active) | **NOT a dup** — those are the MCP *concept*; this is the `mcp_servers` config-schema reference | CREATE; LINK both terms. |
| `hermes_skills_catalog_bundled`, `hermes_optional_skills_catalog` | `term_skills.md`, `term_skill_manifest.md` (active) | **NOT a dup** — those are the skills *concept/format*; these are the shipped-skill catalogs (navigation enumerations) | CREATE; LINK both terms. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug's keywords;
**0 substantive same-concept duplicates** (the 2 LIKE hits — `term_model_catalog`, `term_prfaq` — are
component-link / false-positive, confirmed by reading the notes). No existing `documentation/hermes_agent/`
note exists yet (DB returns 0) → no doc-doc collisions; intra-series links resolve at finalization (G5/G8).

## Per-Note Related Notes Mapping (FINALIZED — ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **Four-floor standard set 2026-06-19 (master directive, supersedes the prior ≥8 term / ≥8 snippet / ≥5 doc
> floor):** each note's `## Related Notes` carries, ALL relevancy-selected to the note's actual content and each
> rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`:
>   repo digests whose modules implement what the doc note describes),
>   layer the note documents — raised from the prior 8 and promoted from a "bonus" to a COUNTED floor),
> - **≥10 DOC notes** (`../../documentation/`, sibling `hermes_*` in this series [may not-yet-exist; resolve at
>
> terms owned by other SPs (e.g. `term_nous_portal`→SP14, `term_messaging_gateway`→SP11,
> `term_provider_routing`/`term_fallback_provider`/`term_credential_pool`→SP09, `term_tool_gateway`→SP05,
> `term_pkce`→SP09) are ADDITIONAL forward-refs (+fin …), EXCLUDED from the ≥8 term floor.

**Note 1 `hermes_env_vars_providers_auth_tools`** (model)
- Terms (≥8): term_provider_plugin, term_oauth_token, term_authentication, term_llm, term_model_catalog, term_autonomous_coding_agents, term_agent_harness, term_prompt_caching, term_oauth, term_bedrock — relevance: the provider/auth/tool-API vars authenticate against each LLM provider plugin, set OAuth/Bedrock credentials, and toggle response caching the harness reads. (+fin: term_nous_portal, term_tool_gateway, term_provider_routing)
- Code-Repos (≥5): repo_hermes_agent_providers_adapters — the per-provider adapters that read these `*_API_KEY`/`*_BASE_URL` vars; repo_hermes_agent_cli — `hermes config set`/`hermes model`/`hermes auth` write these vars into `~/.hermes/.env`; repo_hermes_agent_agent_core — the credential-pool/auth-resolution core that consumes them at request time; repo_hermes_agent — the top-level package whose `~/.hermes/.env` + `config.yaml` loading anchors all env vars; repo_hermes_agent_tools — the search/FAL/voice tool-API keys (EXA/TAVILY/FAL/ElevenLabs) gating tool registration.
- Snippets (≥10): cli_providers_registry, cli_auth_provider_state, cli_auth_resolve_provider, cli_auth_storage, cli_config_set, cli_config_schema, cli_main_provider_flows, core_credential_sources, core_bedrock_adapter_credentials, core_anthropic_adapter_oauth, core_credential_pool_seeding, providers_init_dispatch — relevance: the provider-registry, auth-state/storage, OAuth-resolution, config-set, credential-source/pool, and Anthropic/Bedrock adapter code that consumes these `*_API_KEY`/`*_BASE_URL`/OAuth env vars.
- Docs (≥10): hermes_env_vars_runtime_messaging_behavior, hermes_model_catalog_reference, hermes_mcp_config_reference, hermes_tools_reference_core, hermes_faq_install_provider_terminal (sibling SP21, resolve at finalization); cc_environment_variables — Claude Code's env-var reference, the closest analogue; cc_authentication — agent auth-key/OAuth model; cc_model_selection — provider/model selection knobs; cc_amazon_bedrock_model_config — Bedrock credential config analogue; cc_prompt_caching_mechanism — response-cache analogue to `HERMES_OPENROUTER_CACHE*`.

**Note 2 `hermes_env_vars_runtime_messaging_behavior`** (model)
- Terms (≥8): term_sandbox_backend, term_docker, term_ssh, term_context_window, term_progressive_summarization, term_failover, term_rate_limiting, term_authentication, term_webhook, term_access_control — relevance: the backend vars select terminal/SSH/container execution; context/compression/fallback/routing vars tune the runtime; messaging vars (webhook listeners, allowlists/access control) authenticate the gateways. (+fin: term_messaging_gateway, term_fallback_provider, term_provider_routing, term_context_compression)
- Code-Repos (≥5): repo_hermes_agent_gateway_messaging — the messaging gateway whose per-platform env vars (Telegram/Discord/Slack/MS-Graph/LINE/ntfy + Advanced Tuning) this half configures; repo_hermes_agent_tools — the terminal/SSH/container/persistent-shell backend the `TERMINAL_*` vars drive; repo_hermes_agent_agent_core — the agent-behavior/context-compression/fallback/routing runtime the `HERMES_*` behavior vars tune; repo_hermes_agent_cli — `hermes config set` persists these to `.env`/`config.yaml`; repo_hermes_agent — the top-level package whose `HERMES_HOME`/config loading scopes the whole runtime.
- Snippets (≥10): cli_config_set, cli_config_schema, core_hermes_home, core_prompt_builder_environment, gw_config_schema, gw_display_config, core_auxiliary_proxy_url, cli_tools_config, gw_config_per_channel, core_conversation_loop_context_overflow, tools_terminal_session, gw_runner_supervisor — relevance: the config-schema, HERMES_HOME resolution, gateway per-channel config/display/supervisor, auxiliary-proxy, terminal-session, and context-overflow code these runtime/messaging/behavior env vars drive.
- Docs (≥10): hermes_env_vars_providers_auth_tools, hermes_tools_reference_core, hermes_mcp_config_reference, hermes_faq_messaging_perf_profiles_workflows, hermes_toolsets_reference (sibling SP21, resolve at finalization); cc_environment_variables — Claude Code env-var reference analogue; cc_settings_reference — the config-knob reference analogue; cc_terminal_configuration — terminal-backend config analogue; cc_proxy_and_gateway_config — gateway/proxy var analogue; cc_reduce_token_usage — context-compression behavior analogue.

**Note 3 `hermes_tools_reference_core`** (model)
- Terms (≥8): term_function_calling, term_guardrails, term_subagent, term_cron, term_skills, term_skill_manifest, term_context_window, term_multi_agent_systems, term_moa, term_session_persistence — relevance: the registry lists the agent's callable tools (function-calling), each schema-guarded; delegation spawns subagents; cronjob/skills/session_search/mixture_of_agents are core agent capabilities. (+fin: term_code_execution_tool, term_delegate_task)
- Code-Repos (≥5): repo_hermes_agent_tools — the package that implements every core tool (file/terminal/code_execution/cronjob/delegation/memory/session_search/skills/todo/clarify/moa/vision) this note enumerates; repo_hermes_agent_agent_core — the agent loop that invokes these tools and assembles the registry; repo_hermes_agent_cron — the cron subsystem behind the `cronjob` tool; repo_hermes_agent_skills — the skills subsystem behind `skill_view`/`skill_manage`/`skills_list`; repo_hermes_agent — the top-level package wiring the core toolset into a session.
- Snippets (≥10): tools_registry, tools_file_tools, tools_terminal_exec, tools_code_exec_sandbox, tools_cronjob_register, tools_delegate_spawn, tools_memory, tools_skills_invoke, tools_clarify, tools_process_register, tools_terminal_bg, tools_skill_manager — relevance: the tool-registry assembly plus the file/terminal(+process/bg)/code-exec/cron/delegation/memory/skills/clarify tool implementations this group documents.
- Docs (≥10): hermes_tools_reference_platform_media, hermes_toolsets_reference, hermes_mcp_config_reference, hermes_env_vars_providers_auth_tools, hermes_optional_skills_catalog (sibling SP21, resolve at finalization); cc_built_in_tools — Claude Code built-in tools registry analogue; cc_tools_catalog — the per-tool catalog analogue; cc_file_tool_behavior — file-tool semantics analogue; cc_execution_tool_behavior — code/terminal execution-tool analogue; cc_subagents_overview — delegation/subagent analogue.

**Note 4 `hermes_tools_reference_platform_media`** (model)
- Terms (≥8): term_function_calling, term_multimodal, term_computer_vision, term_guardrails, term_kanban, term_subagent, term_multi_agent_systems, term_pii, term_webhook, term_access_control — relevance: media tools (image/video/vision/tts) are multimodal; browser/computer_use are vision-capable; kanban tools coordinate multi-agent work; messaging/Discord tools handle user PII + access control; all are schema-guarded callable tools. (+fin: term_browser_automation, term_text_to_speech, term_messaging_gateway)
- Code-Repos (≥5): repo_hermes_agent_tools — the package implementing the browser/computer_use/image/video/web/x_search/tts/kanban/messaging/HA/Discord/Spotify/Feishu/Yuanbao tools this note enumerates; repo_hermes_agent_gateway_messaging — the gateway behind `send_message`, Discord, Feishu, and Yuanbao platform tools; repo_hermes_agent_plugins — the bundled Spotify/video_gen plugins that register their tools; repo_hermes_agent_agent_core — the agent loop that materializes and gates these platform/media tools; repo_hermes_agent — the top-level package wiring platform toolsets into a session.
- Snippets (≥10): tools_browser_navigate, tools_browser_cdp, tools_browser_screenshot, tools_computer_use_tool, tools_image_gen, tools_video_gen, tools_kanban_register, tools_kanban_mutate, tools_send_dispatch, tools_tts_routing, tools_vision_dispatch, tools_web_tools — relevance: the browser/CDP/screenshot, computer-use, image/video-gen, kanban (register+mutate), send-message, tts, vision, and web tool implementations this group documents.
- Docs (≥10): hermes_tools_reference_core, hermes_toolsets_reference, hermes_env_vars_runtime_messaging_behavior, hermes_mcp_config_reference, hermes_skills_catalog_bundled (sibling SP21, resolve at finalization); cc_built_in_tools — Claude Code built-in tools analogue; cc_computer_use — computer-use tool analogue; cc_chrome_browser_automation — browser-automation analogue; cc_computer_use_safety — vision/desktop-control safety analogue; cc_tools_catalog — per-tool catalog analogue.

**Note 5 `hermes_toolsets_reference`** (model)
- Terms (≥8): term_function_calling, term_mcp, term_guardrails, term_skills, term_subagent, term_kanban, term_multimodal, term_agent_harness, term_access_control, term_orchestration — relevance: toolsets are named bundles of callable tools the harness materializes per-session/per-platform; dynamic toolsets pull MCP/plugin tools; the bundle (with capability/workflow gating = access control) orchestrates what the agent can call. (+fin: term_hermes_plugin)
- Code-Repos (≥5): repo_hermes_agent_mcp_toolsets — the package that defines core/composite/platform/dynamic toolsets and the MCP-server `mcp-<server>` toolset generation; repo_hermes_agent_tools — the underlying tools each toolset bundles; repo_hermes_agent_cli — the `hermes tools` curses UI + per-platform persistence; repo_hermes_agent_plugins — plugin-registered toolsets via `ctx.register_tool()`; repo_hermes_agent_agent_core — the session materialization that resolves wildcards and capability/workflow gating.
- Snippets (≥10): toolsets_definitions, toolsets_materialize, toolset_distributions, tools_registry, tools_lazy_deps, cli_tools_config, cli_tools_enable, cli_tools_policy, providers_init_dispatch, mcp_serve_tool_surface, tools_skills_guard, gw_platform_registry — relevance: the toolset definition/materialization/distribution code, the tool registry + lazy-deps gating, the `hermes tools` enable/policy CLI surface, the MCP/plugin tool surface, and the platform-toolset registry this page describes.
- Docs (≥10): hermes_tools_reference_core, hermes_tools_reference_platform_media, hermes_mcp_config_reference, hermes_env_vars_runtime_messaging_behavior, hermes_optional_skills_catalog (sibling SP21, resolve at finalization); cc_built_in_tools — Claude Code tool-group analogue; cc_tools_catalog — tool grouping/catalog analogue; cc_sdk_tool_access_control — tool-availability gating analogue; cc_mcp_server_management — dynamic MCP-toolset analogue; cc_settings_reference — per-platform tool config analogue.

**Note 6 `hermes_mcp_config_reference`** (procedure)
- Terms (≥8): term_mcp, term_mcp_gateway, term_json_rpc, term_tls, term_oauth_token, term_authentication, term_function_calling, term_guardrails, term_oauth, term_access_control — relevance: the schema configures MCP servers (JSON-RPC transports), include/exclude tool policies (guardrails/access control), mTLS (TLS) and OAuth 2.1 auth. (+fin: term_pkce)
- Code-Repos (≥5): repo_hermes_agent_mcp_toolsets — the package implementing the `mcp_servers` config schema, filtering, lifecycle, and `mcp-<server>` toolset generation; repo_hermes_agent_tools — the MCP client/call/OAuth tool code that consumes the schema; repo_hermes_agent_cli — the `hermes mcp` config CLI + `/reload-mcp`; repo_hermes_agent_acp — the ACP surface that also speaks MCP-style tool exposure; repo_hermes_agent_agent_core — the session that registers sanitized `mcp_<server>_<tool>` names and applies the policy.
- Snippets (≥10): tools_mcp_client, tools_mcp_call, tools_mcp_lifecycle, tools_mcp_oauth, tools_mcp_oauth_manager, tools_mcp_notifications, cli_mcp_config, mcp_serve_tool_surface, mcp_serve_hermes_as_server, cli_auth_oauth_callback_server, tools_lazy_deps, toolsets_materialize — relevance: the MCP client/call/lifecycle/OAuth(+callback server)/notification code, the `hermes mcp` config CLI, the serve-as-server surface, and the dynamic MCP-toolset materialization this schema drives.
- Docs (≥10): hermes_tools_reference_core, hermes_toolsets_reference, hermes_env_vars_providers_auth_tools, hermes_optional_skills_catalog, hermes_faq_messaging_perf_profiles_workflows (sibling SP21, resolve at finalization); cc_mcp_overview — MCP concept analogue; cc_mcp_server_management — server-config management analogue; cc_mcp_transports — stdio/HTTP transport analogue; cc_mcp_authentication — MCP OAuth/auth analogue; cc_managed_mcp_configuration — config-schema/policy analogue.

**Note 7 `hermes_model_catalog_reference`** (model)
- Terms (≥8): term_model_catalog, term_provider_plugin, term_llm, term_multimodal, term_context_window, term_authentication, term_caching, term_autonomous_coding_agents, term_failover, term_quantization — relevance: the manifest enumerates models with context-window/modality/pricing per provider; fetch/cache (with offline snapshot fallback = failover) and config override URLs feed model selection across providers. (+fin: term_nous_portal, term_provider_routing)
- Code-Repos (≥5): repo_hermes_agent_cli — the `hermes model`/`/model` picker that fetches the manifest, `hermes_cli/models.py` lists, and `build_model_catalog.py` generator; repo_hermes_agent_providers_adapters — the per-provider model normalization (OpenRouter, Nous Portal) the catalog curates; repo_hermes_agent_agent_core — the model-capability probe/introspection that consumes the schema; repo_hermes_agent — the top-level package whose `config.yaml` `model_catalog:` block holds the URL/TTL/override config; repo_hermes_agent_tui_gateway — the TUI/gateway model picker surface fed by the catalog.
- Snippets (≥10): cli_model_catalog, cli_models_fetch, cli_models_normalize, cli_models_picker, model_tools_capability_probe, model_tools_introspection, cli_model_switch_validate, cli_providers_registry, cli_model_switch_swap, cli_model_switch_entry, providers_init_dispatch, core_error_classifier_provider_maps — relevance: the catalog fetch/normalize/picker code, the model-switch entry/swap/validate path, the capability-probe/introspection that consumes the manifest schema, and the provider-map error classification on fallback.
- Docs (≥10): hermes_env_vars_providers_auth_tools, hermes_tools_reference_core, hermes_mcp_config_reference, hermes_configuring_models_dashboard, hermes_model_aux_provider_config (sibling SP21/SP02/SP14, resolve at finalization); cc_model_selection — model-selection analogue; cc_fallback_models — manifest-unreachable fallback analogue; cc_amazon_bedrock_model_config — per-provider model config analogue; cc_restrict_model_selection — provider/model curation analogue; cc_environment_variables — `HERMES_MODEL`/catalog env knobs analogue.

**Note 8 `hermes_skills_catalog_bundled`** (navigation)
- Terms (≥8): term_skills, term_skill_manifest, term_autonomous_coding_agents, term_agentic_ai, term_subagent, term_function_calling, term_cron, term_prompt_engineering, term_orchestration, term_multi_agent_systems — relevance: each catalog entry is a bundled SKILL.md the agent can invoke; categories span autonomous-agent/devops/mlops/research multi-agent workflows; automation blueprints orchestrate/chain skills via cron. (+fin: term_skills_hub, term_skill_curator)
- Code-Repos (≥5): repo_hermes_agent_skills — the package shipping the bundled SKILL.md catalog (apple…yuanbao) this note enumerates; repo_hermes_agent_cli — the `hermes skills`/skills-hub install + setup commands; repo_hermes_agent_cron — the cron subsystem behind automation-blueprint scheduling; repo_hermes_agent_agent_core — the prompt-builder skills snapshot that surfaces the catalog at session start; repo_hermes_agent_tools — the `skill_view`/`skill_manage`/`skills_list` tools that browse/invoke catalog entries.
- Snippets (≥10): cli_skills_hub, cli_skills_install, cli_setup_skills, tools_skills_hub_registry, tools_skills_hub_install, tools_skills_invoke, tools_skills_validate, core_prompt_builder_skills_snapshot, skills_index_cache, skills_canonical_format, core_skill_commands_discovery, skills_devops_kanban_orchestrator — relevance: the skills-hub registry/install/invoke/validate code, the index cache + canonical SKILL.md format, the command-discovery path, the prompt-builder skills snapshot that surfaces the catalog at session start, and a representative bundled-skill (devops kanban orchestrator).
- Docs (≥10): hermes_optional_skills_catalog, hermes_tools_reference_core, hermes_toolsets_reference, hermes_env_vars_providers_auth_tools, hermes_mcp_config_reference (sibling SP21, resolve at finalization); cc_bundled_skills — Claude Code bundled-skills catalog analogue; cc_skills_overview — skills concept analogue; cc_skill_invocation_and_lifecycle — skill load/invoke analogue; cc_skill_frontmatter_reference — SKILL.md frontmatter (blueprint slot) analogue; cc_create_and_run_workflows — automation-blueprint/workflow analogue.

**Note 9 `hermes_optional_skills_catalog`** (navigation)
- Terms (≥8): term_skills, term_skill_manifest, term_autonomous_coding_agents, term_agentic_ai, term_mcp, term_function_calling, term_guardrails, term_prompt_engineering, term_orchestration, term_access_control — relevance: optional skills install on demand into the same registry; categories include MCP/security/migration/blockchain/finance workflows the agent can pull when needed, gated by the skills guard (access control). (+fin: term_skills_hub, term_skill_curator)
- Code-Repos (≥5): repo_hermes_agent_skills — the package hosting the optional (install-on-demand) skills catalog + optional-skills registry; repo_hermes_agent_cli — the `hermes skills install` on-demand install flow + `HERMES_OPTIONAL_SKILLS` auto-install; repo_hermes_agent_mcp_toolsets — the `mcp` optional-skills category that wires MCP-native skills; repo_hermes_agent_tools — the skills guard/validate/invoke tools driving the install flow; repo_hermes_agent_agent_core — the registry merge that makes installed optional skills available next session.
- Snippets (≥10): cli_skills_hub, cli_skills_install, tools_skills_hub_registry, tools_skills_hub_install, tools_skills_validate, tools_skills_guard, tools_skills_invoke, cli_setup_skills, optional_skills_registry, skills_mcp_native, optional_skills_security_sherlock, optional_skills_migration_openclaw — relevance: the on-demand skills-hub install/registry/guard/validate code plus the optional-skills registry and representative optional skills (mcp-native, security/sherlock, openclaw migration) this catalog enumerates.
- Docs (≥10): hermes_skills_catalog_bundled, hermes_tools_reference_core, hermes_toolsets_reference, hermes_mcp_config_reference, hermes_faq_install_provider_terminal (sibling SP21, resolve at finalization); cc_skills_overview — skills concept analogue; cc_create_a_skill — skill authoring/install analogue; cc_plugin_marketplaces_and_install — on-demand install-from-catalog analogue; cc_host_and_manage_marketplaces — hub/marketplace hosting analogue; cc_large_codebase_skills_and_plugins — pulling skills on demand analogue.

**Note 10 `hermes_faq_install_provider_terminal`** (procedure)
- Terms (≥8): term_autonomous_coding_agents, term_llm, term_provider_plugin, term_model_catalog, term_sandbox_backend, term_docker, term_context_window, term_skills, term_rate_limiting, term_authentication — relevance: the FAQ covers provider/model selection, API-key/auth fixes, 429 rate-limit retries, install fixes, context-window overflow, Docker/terminal backend issues, and the memory-vs-skills distinction. (+fin: term_nous_portal, term_honcho, term_hermes_profile)
- Code-Repos (≥5): repo_hermes_agent_cli — the `hermes` installer/setup/doctor/`hermes model` commands the install + provider answers exercise; repo_hermes_agent_providers_adapters — the provider adapters behind "can't switch providers"/"API key not working"/400-error answers; repo_hermes_agent_tools — the terminal/Docker backend behind the terminal-troubleshooting answers; repo_hermes_agent_agent_core — the context-overflow/`/compress` and memory-vs-skills behavior; repo_hermes_agent — the top-level package + `install.sh`/PATH/Python-version install path.
- Snippets (≥10): cli_setup_installer, cli_setup_verify, cli_setup_wizard, cli_doctor_primitives, cli_doctor_api_connectivity, cli_doctor_auth_dirs, cli_doctor_entry_early_checks, core_error_classifier_provider_maps, cli_main_provider_flows, cli_model_switch_verify, cli_uninstall, core_conversation_loop_context_overflow — relevance: the installer/wizard/doctor(early-checks/api/auth)/provider-flow/error-classifier/uninstall and context-overflow code paths the install + provider + terminal troubleshooting answers exercise.
- Docs (≥10): hermes_faq_messaging_perf_profiles_workflows, hermes_env_vars_providers_auth_tools, hermes_model_catalog_reference, hermes_tools_reference_core, hermes_optional_skills_catalog (sibling SP21, resolve at finalization); cc_install — install analogue; cc_install_failures_reference — install-error fixes analogue; cc_authentication_and_network_errors — provider/API-key error analogue; cc_login_authentication_troubleshooting — auth-troubleshooting analogue; cc_debug_your_configuration — config-debug analogue.

**Note 11 `hermes_faq_messaging_perf_profiles_workflows`** (procedure)
- Terms (≥8): term_autonomous_coding_agents, term_mcp, term_context_window, term_progressive_summarization, term_session_persistence, term_subagent, term_idempotency, term_multi_agent_systems, term_access_control, term_cron — relevance: the FAQ covers messaging-gateway + MCP fixes, performance/context-compression, profile isolation, allowlist/access control, cron-job workflows, shared-thread sessions, and multi-model/per-chat-binding workflow recipes. (+fin: term_messaging_gateway, term_hermes_profile, term_provider_routing)
- Code-Repos (≥5): repo_hermes_agent_gateway_messaging — the gateway behind "bot not responding"/"messages not delivering"/allowlist and shared-thread-session answers; repo_hermes_agent_mcp_toolsets — the MCP subsystem behind the MCP-issue answers; repo_hermes_agent_agent_core — the context-compression/`/compress` and per-chat session-keying behavior; repo_hermes_agent_cli — the `hermes profile`/`hermes backup`/export commands behind the profiles/migration answers; repo_hermes_agent_cron — the cron-job workflow recipes the FAQ recommends.
- Snippets (≥10): gw_config_load, gw_delivery, gw_memory_monitor, gw_status_health, gw_runner_session_key, tools_mcp_client, tools_mcp_lifecycle, core_prompt_builder_subscription_truncate, core_conversation_compression_entry, cli_memory_setup, cli_config_set, gw_runner_cron — relevance: the gateway config/delivery/memory-monitor/status-health/session-key, MCP-client+lifecycle, context-truncation/compression, memory-setup, and cron-runner code the messaging/perf/profile/workflow answers reference.
- Docs (≥10): hermes_faq_install_provider_terminal, hermes_mcp_config_reference, hermes_env_vars_runtime_messaging_behavior, hermes_tools_reference_platform_media, hermes_toolsets_reference (sibling SP21, resolve at finalization); cc_mcp_server_management — MCP-issue/management analogue; cc_reduce_token_usage — performance/context-compression analogue; cc_what_survives_compaction — `/compress` behavior analogue; cc_sessions — session/thread-keying analogue; cc_workflow_recipes — multi-model/per-chat workflow-recipe analogue.

All 11 notes meet ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc. Snippet IDs are under
`resources/documentation/hermes_agent/` (intra-series links land at finalization, verified by G5/G8).
Forward-ref terms (`term_nous_portal`, `term_tool_gateway`, `term_messaging_gateway`,
`term_fallback_provider`, `term_provider_routing`, `term_credential_pool`, `term_pkce`,
`term_context_compression`, `term_skills_hub`, `term_skill_curator`, `term_browser_automation`,
`term_text_to_speech`, `term_code_execution_tool`, `term_delegate_task`, `term_honcho`,
`term_hermes_profile`, `term_hermes_plugin`) are owned by other SPs and EXCLUDED from the ≥8 floor;
they are added at finalization once those SPs capture them.

## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15; re-measured 2026-06-19, mirror c253b07)

Re-read all 8 substantive source pages from `inbox/hermes_agent_docs/reference/`; measured counts match
the Source Pages table (no >50% estimate misses). The 2026-06-19 re-sync re-measured the 4 grown pages
(env-vars 9223→9291w, tools-reference 3210→3235w, mcp-config 1036→1044w, optional-skills 2864→2911w; all
code-block counts unchanged) — every delta is <70 words and below threshold, so all per-note ~estimates
and code budgets stand and no note approaches the ≤2500w/≤6 code/≤400 line caps. Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 env-vars-providers-auth-tools | model | 1400 | ≤6 (mostly tables; 1-2 `.env`/`config set` blocks) | ✓ |
| 2 env-vars-runtime-messaging-behavior | model | 1500 | ≤6 (tables; 1-2 example blocks) | ✓ |
| 3 tools-reference-core | model | 1300 | ≤6 (source has 0 code; curate ≤6 schema/usage snippets if any, else 0) | ✓ |
| 4 tools-reference-platform-media | model | 1400 | ≤6 (source 0 code; 0 expected) | ✓ |
| 5 toolsets-reference | model | 1100 | ≤6 (curate from 6 config blocks) | ✓ |
| 6 mcp-config-reference | procedure | 1300 | ≤6 (curate from 15 example blocks; one canonical per pattern) | ✓ |
| 7 model-catalog-reference | model | 700 | ≤5 (from 5 schema/config blocks) | ✓ |
| 8 skills-catalog-bundled | navigation | 1100 | ≤2 (catalog is prose/tables; 0 source code + blueprint pointer) | ✓ |
| 9 optional-skills-catalog | navigation | 1100 | ≤3 (from 3 install blocks) | ✓ |
| 10 faq-install-provider-terminal | procedure | 1500 | ≤6 (curate from ~22 short command blocks; summarize rest in prose) | ✓ |
| 11 faq-messaging-perf-profiles-workflows | procedure | 1500 | ≤6 (curate from ~22 short command blocks; summarize rest in prose) | ✓ |

No further splits needed — all 11 notes ≤2500w. The code-heavy pages (faq 44 blocks → Notes 10/11;
mcp-config 15 blocks → Note 6; env-vars tables → Notes 1/2) are curated to ≤6 load-bearing blocks per
note, with the rest summarized in prose (kept blocks verbatim). If any note exceeds 350 lines during
writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Reference catalogs (Notes 8/9) use `building_block: navigation`; tool/toolset/env/model registries use
`building_block: model`; FAQ + mcp-config-schema use `building_block: procedure`. Not invented — matches
existing `cc_` notes.

## Undigested Terms Plan (SP21)

**SP21 owns 0 new term captures.** Per the master's corpus-wide ownership sweep, every Hermes-specific
concept SP21 references is owned by another sub-plan (link at finalization) or is an existing verified term.
Augment re-read of all 8 pages surfaced **0 new** undigested terms that SP21 should own — the reference
pages enumerate vars/tools/skills whose concept-term is owned by the feature's home sub-plan (this is the
expected outcome for a pure-reference sub-plan).

| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_nous_portal`, `term_tool_gateway` | LINK only (forward-ref, +fin) | SP14 / SP05 | env-vars + model-catalog reference the portal/gateway billing; concept homes are SP14/SP05. |
| `term_provider_routing`, `term_fallback_provider`, `term_credential_pool` | LINK only (+fin) | SP09 | config-only env vars (`Provider Routing`/`Fallback Providers`); concepts owned by SP09. |
| `term_messaging_gateway` | LINK only (+fin) | SP11 | messaging env vars + FAQ messaging issues; concept owned by SP11. |
| `term_pkce` | LINK only (+fin) | SP09 | mcp-config OAuth 2.1 PKCE; concept owned by SP09. |
| `term_context_compression` | LINK only (+fin) | SP18 | `Context Compression` env vars + FAQ perf; concept owned by SP18. |
| `term_skills_hub`, `term_skill_curator` | LINK only (+fin) | SP05 | skills catalogs reference the multi-source hub/curator; concept homes SP05. |
| `term_browser_automation`, `term_text_to_speech`, `term_code_execution_tool`, `term_delegate_task` | LINK only (+fin) | SP08 / SP06 | tools-reference enumerates these tools; concept homes SP08 (media/web) / SP06 (automation). |
| `term_honcho`, `term_hermes_profile` | LINK only (+fin) | SP05 / SP04 | FAQ memory-vs-skills + profiles answers; concept homes SP05/SP04. |

### Renamed (general → specific)

— (audit performed; SP21 owns 0 new term captures, so no slugs to rename. The specificity heuristic was
applied to the master's forward-ref slugs SP21 links; all are already scope-qualified by their owners,
e.g. `term_messaging_gateway` not `term_gateway`, `term_credential_pool` not `term_pool`,
`term_provider_routing` not `term_routing`.)

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_model_catalog` (would duplicate) | `term_model_catalog.md` (active) | Not captured — link the existing term from the `hermes_model_catalog_reference` doc note (term is the generic concept; doc note is Hermes' manifest reference). |
| `term_built_in_tools` / `term_toolset` (would-be) | none substantive (DB returns 0) | No removal — SP21 was never going to capture these; doc notes (`hermes_tools_reference_*`, `hermes_toolsets_reference`) created instead; link component terms (`term_function_calling`, `term_guardrails`). |
| `term_faq` (would-be) | `term_prfaq.md` (active, UNRELATED — Amazon PR/FAQ format) | Not captured — `term_prfaq` is a LIKE false-positive; do NOT link it from the Hermes FAQ doc notes. |

## Term-Note Authoring Requirements

N/A (inherited) — SP21 owns 0 new term notes. Forward-referenced terms follow the master's
`/tessellum-capture-term-note` spec under their owning sub-plans (SP04/05/06/08/09/11/14/18). The full
diversity, MathJax, fleeting-content guard, glossary template, depth-scaled Related Terms 8/10/12,
backlink expansion, >200-line decomposition) apply to those captures in their home sub-plans, not here.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (env-vars + tools registry, P3-pilot):** Notes 1, 2, 3, 4. Pilot Note 3
  (`hermes_tools_reference_core`) first → reindex → verify format/ghost/in-degree BEFORE the rest.
  GATE G1–G8.
- **Phase 2 (toolsets + mcp-config + model-catalog):** Notes 5, 6, 7. GATE G1–G8.
- **Phase 3 (skills catalogs + FAQ):** Notes 8, 9, 10, 11. GATE G1–G8.

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/reference/<page>` (code
verbatim for kept blocks; tool descriptions verbatim) · G3 density+coverage · G4 cross-refs + entry-point
row · **G5 ghost (Script 4, DB-verify every ref)** · **G6 broken-links
(`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)** · G7 single-BB · **G8 in-degree ≥1 from
outside the folder**.

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
for n in hermes_env_vars_providers_auth_tools hermes_env_vars_runtime_messaging_behavior hermes_tools_reference_core hermes_tools_reference_platform_media hermes_toolsets_reference hermes_mcp_config_reference hermes_model_catalog_reference hermes_skills_catalog_bundled hermes_optional_skills_catalog hermes_faq_install_provider_terminal hermes_faq_messaging_perf_profiles_workflows; do
```

## Entry Point Decision (inherited)

Contributes 11 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under a "Reference: Env Vars, Tools, Catalogs, MCP-config, Model-catalog & FAQ" section.
Parent hub back-link in `entry_research_and_ai_hub.md` is handled at master level. SP21 does NOT create a
separate entry point — the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md`
(matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_providers_adapters.md` | → `hermes_env_vars_providers_auth_tools`, `hermes_model_catalog_reference` | provider adapters ↔ provider env-var + model-catalog reference |
| `repo_hermes_agent.md` | → `hermes_env_vars_runtime_messaging_behavior` | implementation ↔ runtime/behavior env-var reference |
| `repo_hermes_agent_tools.md` | → `hermes_tools_reference_core`, `hermes_tools_reference_platform_media` | tools repo ↔ built-in tools registry |
| `repo_hermes_agent_mcp_toolsets.md` | → `hermes_toolsets_reference`, `hermes_mcp_config_reference` | MCP/toolsets repo ↔ toolset + MCP-config reference |
| `repo_hermes_agent_skills.md` | → `hermes_skills_catalog_bundled`, `hermes_optional_skills_catalog` | skills repo ↔ shipped-skill catalogs |
| `repo_hermes_agent_cli.md` | → `hermes_faq_install_provider_terminal` | CLI repo ↔ install/provider/terminal FAQ |
| `repo_hermes_agent_gateway_messaging.md` | → `hermes_faq_messaging_perf_profiles_workflows` | gateway repo ↔ messaging/perf/profiles FAQ |
| `term_model_catalog.md` | → `hermes_model_catalog_reference` | concept term → Hermes manifest reference |
| `term_prfaq.md` | (NO inlink — unrelated Amazon PR/FAQ format) | confirmed LIKE false-positive; do NOT link |
| `entry_code_snippets_hermes_agent.md` | → `hermes_tools_reference_core`, `hermes_env_vars_providers_auth_tools` | code layer ↔ reference docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 11 notes | navigation hub |

Guarantees every new note in-degree ≥1 from outside the folder (G8). Inlink addition is a gated execution
phase (Phase 3b), not a recommendation.

## Pacing Rules (inherited)

Pilot Note 3 (`hermes_tools_reference_core`) → reindex → verify format/ghost/in-degree BEFORE authoring the
rest. Commit per phase (per-wave commits for multi-agent runs). Re-read the source page before writing each
note — do NOT work from memory. Tool descriptions + code blocks verbatim for kept blocks; curate code-heavy
notes (faq Notes 10/11, mcp-config Note 6) to ≤6 load-bearing blocks, summarize the rest in prose. The
big-table pages (env-vars Notes 1/2, tools Notes 3/4) condense the reference tables but keep variable/tool
NAMES + their one-line descriptions verbatim. If a note exceeds 350 lines during writing, STOP and split.
If multi-agent: agents return note content, master writes serially where there is write-contention; ≤30
agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP21 lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 11 rows to
  the master-created entry point; backfill the `repo_hermes_agent_*` / `term_model_catalog` inlinks (G8);
  run `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- After P1/P2 waves land: cross-link the reference notes (env-vars ↔ SP02 config; tools ↔ SP08 feature
  pages; toolsets ↔ SP20 `hermes tools` commands; mcp-config ↔ SP09 MCP; model-catalog ↔ SP02
  configuring-models + SP14 providers) — bidirectional reference↔feature links once those SPs land.
- Consider one `thought_` note comparing the docs-stated tool/toolset registry vs the code-digestion
  findings in `snippet_hermes_agent_tools_registry` / `toolsets_definitions`.

## Augmentation Report

- Sections added/updated: Collision&Dedup Audit (2 LIKE hits — `term_model_catalog` component-link,
  `term_prfaq` false-positive — confirmed by reading the notes), finalized Per-Note Mapping (≥8 term + ≥5
  Density Re-Assessment (re-read confirmed), G5 ghost + G8 scripts, Inlinks.
- Cross-ref floor set 2026-06-19 to ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note (all counted,
  to ground each relevance clause; added the new code-repo floor (5 `repo_hermes_agent_*` per note), promoted
  `cc_*` analogues). No existing relevant cross-ref dropped (additive level-up).
- Density re-read: counts match measured; **no additional splits** beyond the planned 6 (env-vars→2,
  faq→2, tools→2). All 11 notes ≤2500w; code-heavy faq/mcp-config notes curated to ≤6 blocks.
- Collision audit: **0 removals** — `term_model_catalog` (generic concept) is LINK-not-dup;
  `term_prfaq` (Amazon PR/FAQ) is an unrelated false-positive (no link); no doc note duplicates an
  existing term/doc note; no `documentation/hermes_agent/` note exists yet (0 doc-doc collisions).
- Stub handling: `automation-blueprints-catalog.mdx` (189w) merged into Note 8 (recorded in coverage map);
  not a standalone note.
- Undigested terms surfaced at augment: **0 new** (SP21 owns 0 captures; all concepts owned by other SPs —
  the expected outcome for a pure-reference sub-plan).
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans; stub
merged) ✓ Split Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note
Format Def (derived) ✓ Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓
Undigested Terms Plan ✓ Capture Phase per term (N/A — 0 owned) ✓ best-fit glossary (N/A) ✓ Term-Note Auth
Reqs (N/A-inherited) ✓ invokes capture-term-note (N/A) ✓ Entry-Point Decision ✓ matches size threshold ✓
Slug Specificity (N/A — 0 owned; audit noted) ✓ Slug Collision (2 LIKE hits caught: component-link +
false-positive) ✓ dedup generalized to ALL notes incl doc, searched term_dictionary AND documentation/ ✓
G8 in every phase + inlinks EXECUTED ✓ Doc-Note Authoring Spec derived ✓). Term-capture items are
N/A-pass (SP21 owns 0 captures); dedup/collision items are substantively PASS (audit performed on all 11
doc notes).

## Review Sign-Off

**Reviewed 2026-06-15; independently re-reviewed 2026-06-19 against the FOUR-FLOOR standard — READY FOR EXECUTION (9/9 checkpoints pass).**

> **Re-review 2026-06-19 (four-floor):** Independent CP1-CP9 pass. CP1 measured per-note counts =
> 10 term / 5 code-repo / 12 snippet / 10 doc for all 11 notes (every floor met or exceeded; each link
> 107/107 snippets (`snippet_hermes_agent_*`), 12/12 code-repos (`repo_hermes_agent_*`), 42/42 terms,
> 42/42 `cc_*` docs; 0 missing. 13 sibling `hermes_*` doc IDs correctly not-yet-existing (resolve at
> finalization, G5/G8). CP7 re-measure (mirror c253b07): env-vars 9291/2, tools-reference 3235/0,
> mcp-config 1044/15, model-catalog 500/5, toolsets 1493/6, skills-catalog 1420/0 — match plan;
> faq body-only 1142w/40-code-fences and optional-skills 2848w/3-code differ negligibly from the
> manifest's 4699w-prose/44 and 2911w (measurement-method/sync drift, no cap breach, split decisions
> unaffected). 0 doc-doc collisions (no `documentation/hermes_agent/` note exists yet).

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 3 phases, each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (11 rows under a Reference section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 11 notes ≤30; master holds the corpus-level split. |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | env-vars→2, faq→2 (44 code blocks > cap), tools→2; all notes ≤2500w; code-heavy notes curated ≤6; stub merged into Note 8. |
| CP7 | Source counts measured | PASS | Re-measured 2026-06-19 (mirror c253b07): env-vars 9291, faq 4699 (44 code), tools 3235 (79 tools), optional-skills 2911, toolsets 1493, skills-catalog 1420, mcp-config 1044, model-catalog 500, automation-blueprints 189 — measured == plan. |
| CP8 | Undigested Terms + Authoring Reqs | PASS (N/A) | SP21 owns 0 term captures (all concepts owned by SP04/05/06/08/09/11/14/18); Undigested Terms Plan + Authoring Reqs sections present; multi-source mandate inherited by owners. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit table covers all 11 doc notes (term_dictionary AND documentation/); 2 LIKE hits confirmed (`term_model_catalog` = component-link, `term_prfaq` = unrelated false-positive); Renamed/Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 11 notes from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation. |

**RESULT: 9/9 → READY FOR EXECUTION.**

## Re-Sync Note (2026-06-19)

The local doc mirror was re-downloaded from `NousResearch/hermes-agent` `website/docs/` at main HEAD
`c253b07` (was pinned `95715dc`); byte-identical to upstream main. Independently re-measured every owned
page (body-only word count; code-fence count = `^\s*```` lines ÷ 2). The 4 grown pages:

- reference/environment-variables.md — 9223w/2code -> 9291w/2code
- reference/tools-reference.md — 3210w/0code -> 3235w/0code
- reference/mcp-config-reference.md — 1036w/15code -> 1044w/15code
- reference/optional-skills-catalog.md — 2864w/3code -> 2911w/3code

Spot-re-measured 3 unchanged pages — all stable: toolsets-reference 1493w/6code, skills-catalog
1420w/0code, model-catalog 500w/5code (match the plan). My measurements equal the manifest for all 4
changed pages — no discrepancy.

**Density re-decision: none.** Every delta is small (+68 / +25 / +8 / +47 words; 0 code-block change).
The largest grown page (env-vars) was already split into Notes 1+2 for being ×3.7 over the 2500w cap; the
others stay single-note (tools-reference's split is for the 79-tool registry bisect, not a cap breach;
mcp-config 1044w and optional-skills 2911w remain comfortably within per-note budgets after their
existing split/single-note plan). No planned-note filename, BB type, or code budget changes; **no new
split added**. The cross-ref floor was subsequently raised 2026-06-19 to the four-floor standard (≥8 term +
≥5 code-repo + ≥10 snippet + ≥10 doc per note); no GATE was weakened. **Plan remains READY for execution.**

## Pipeline Status (Per-Sub-Plan)

- Plan: **DONE** · Augment: **DONE** (2026-06-15, 31/31; re-augmented four-floor 2026-06-19) · Review: **DONE** (2026-06-15, 9/9 READY; independently re-reviewed four-floor 2026-06-19, 9/9 READY) · Execute: pending · Re-synced 2026-06-19

**Source**: `inbox/hermes_agent_docs/reference/{environment-variables,faq,tools-reference,toolsets-reference,mcp-config-reference,model-catalog,skills-catalog,optional-skills-catalog,automation-blueprints-catalog}.{md,mdx}`
**Last Updated**: 2026-06-15 (re-measured 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
