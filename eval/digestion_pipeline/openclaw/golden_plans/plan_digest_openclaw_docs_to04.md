---
title: Sub-Plan to04 — OpenClaw Docs: Tools (search providers, goal, image generation, llm-task, lobster)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["tools/gemini-search", "tools/goal", "tools/grok-search", "tools/image-generation", "tools/kimi-search", "tools/llm-task", "tools/lobster"]
---

# Sub-Plan to04: Tools

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, `oc_*` prefix), format (YAML field order + `## Overview`/`## Related Notes`/`## References` body), dedup (three-way across term_dictionary / documentation / `repo_openclaw*`), the 9-GATE (G1–G9), cross-references, undigested-terms ownership, and entry-point wiring are ALL inherited from the master.

## Scope


**Source**: OpenClaw docs, 7 pages, 7,537 measured words. **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| gemini-search | tools/gemini-search | 446 | 1 | 7 | 0 | procedure |
| goal | tools/goal | 1,180 | 7 | 10 | 0 | concept |
| grok-search | tools/grok-search | 576 | 1 | 7 | 0 | procedure |
| image-generation | tools/image-generation | 2,828 | 13 | 9 | 3 | procedure + model (split) |
| kimi-search | tools/kimi-search | 434 | 1 | 5 | 0 | procedure |
| llm-task | tools/llm-task | 449 | 5 | 7 | 1 | procedure |
| lobster | tools/lobster | 1,624 | 17 | 18 | 4 | concept |

Total: 7,537 words, 45 code fences, 63 H2, 8 H3.

## Content Strategy

- **Prioritize**: the cross-provider `image_generate` contract (routing order, parameters, per-provider capabilities — the most-referenced, most-complex tool here) and the Lobster workflow runtime (deterministic pipelines + approval/resume — a distinctive OpenClaw automation primitive that the Automation sub-plan and `llm-task` both reference).
- **Split**: `image-generation.md` (2,828w > 2,500w cap; 13 fences > 6 cap; mixes a tool-usage **procedure** with a per-provider capability/deep-dive **model/reference**) → 2 notes (usage procedure + provider/capability reference). See Split Decisions.
- **One note per page otherwise**: the three search providers (gemini/grok/kimi, 434–576w each) are short, single-BB procedure pages → 1 note each (NOT merged — each is a distinct provider with its own auth/config/credential-precedence and the master maps one note per reference page). `goal` (1,180w) and `lobster` (1,624w) each stay 1 note (under the 2,500w cap), but Lobster's 17 fences exceed the 6-fence cap → reproduce only ~5–6 representative fences (see Density Re-Assessment).
- **Link-out (do NOT redefine)**: the `tools/web` Web Search overview + auto-detection (owned by to08 `tools/web`), `x_search` (to08 `tools/web#x_search`), provider setup pages (`providers/google`, `providers/moonshot`, `providers/xai`, `providers/openai`, `providers/comfy`, `providers/fal`, `providers/minimax`, `providers/vydra` — Providers section pr01–pr09), `tools/thinking`/`tools/subagents`/`tools/slash-commands` (to07), `concepts/session-tool`/`concepts/compaction`/`concepts/models` (co04/co06), `automation/taskflow`/`automation/tasks`/`automation/cron-jobs`/`automation/standing-orders` (au01), `gateway/config-agents` (gw01), `tools/plugin` (to06), `prose`/OpenProse (rt03). Existing terms (`term_llm`, `term_claude`, `term_oauth`, `term_mcp`, etc.) linked, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_tools_gemini_search.md` | procedure | gemini-search.md: Get an API key, Config, How it works, Supported parameters, Model selection, Base URL overrides | 380 | Configuring Gemini as a `web_search` provider: API-key sources + credential precedence (webSearch.apiKey → GEMINI_API_KEY → google.apiKey), Google Search grounding behavior with SSRF-guarded citation resolution, supported params (query/freshness/date range), model selection, base-URL overrides. |
| 2 | `oc_tools_grok_search.md` | procedure | grok-search.md: Onboarding and configure, Sign in or get an API key, Config, How it works, Supported parameters, Base URL overrides | 430 | Configuring Grok (xAI web-grounded responses) as a `web_search` provider: xAI-OAuth-preferred onboarding, API-key fallback, credential alternatives, the related `x_search` follow-up, 60s default timeout, base-URL/Responses-endpoint overrides. |
| 3 | `oc_tools_kimi_search.md` | procedure | kimi-search.md: Get an API key, Config, How it works, Supported parameters | 360 | Configuring Kimi (Moonshot web search) as a `web_search` provider: KIMI/MOONSHOT key sources, .ai vs .cn region/base-URL reuse from chat config, grounding-evidence requirement and the `kimi_web_search_ungrounded` error fallback. |
| 4 | `oc_tools_goal.md` | concept | goal.md: What goals are for, Command reference, Statuses, Token budgets, Model tools, TUI, Channel behavior, Troubleshooting | 620 | The session goal: one durable per-session objective (distinct from tasks/cron/standing orders), `/goal` lifecycle commands + status set, optional token budgets, the get/create/update_goal model tools (operator-only pause/resume/clear), TUI footer states, and channel/session-key behavior. |
| 5 | `oc_tools_image_generation.md` | procedure | image-generation.md: (intro async-task model), Quick start, Common routes, Tool parameters, Configuration (Model selection, Provider selection order, Image editing), Examples | 700 | Using the `image_generate` tool: async background-task model + completion delivery, quick-start auth + default model, common provider/model routes, the full tool-parameter surface (size/aspectRatio/resolution/quality/background/count/openai/fal hints), model-selection + provider-selection-order config, image editing, and CLI/tool examples. |
| 6 | `oc_tools_image_generation_providers.md` | model | image-generation.md: Supported providers, Provider capabilities, Provider deep dives (OpenAI, Microsoft Foundry, OpenRouter, fal Krea 2, MiniMax, xAI) | 650 | The `image_generate` provider/capability reference: the 11 supported providers with default models + auth, the per-provider capability matrix (max count, edit/reference limits, size/aspect/resolution), and provider deep dives (OpenAI gpt-image-2/1.5 + Codex OAuth, Microsoft Foundry MAI, OpenRouter, fal Krea 2, MiniMax dual-auth, xAI grok-imagine). |
| 7 | `oc_tools_llm_task.md` | procedure | llm-task.md: Enable the plugin, Config (optional), Tool parameters, Output, Example: Lobster workflow step (incl. Important limitation), Safety notes | 420 | The optional `llm-task` plugin tool: enabling it (`plugins.entries.llm-task` + `tools.alsoAllow`), optional defaults config (provider/model/allowedModels/maxTokens), tool parameters (prompt/input/schema/thinking/…), JSON-Schema-validated `details.json` output, the embedded-Lobster `openclaw.invoke` limitation, and JSON-only safety notes. |
| 8 | `oc_tools_lobster.md` | concept | lobster.md: Why / Why a DSL, How it works, Pattern (small CLI + JSON pipes + approvals), JSON-only LLM steps, Workflow files (.lobster), Install, Enable the tool, Tool parameters (run/resume/optional inputs), Output envelope, Approvals, OpenProse, Safety, Troubleshooting, Case study | 720 | The Lobster typed workflow runtime: deterministic multi-step tool pipelines with explicit approval gates and resume tokens, the in-process embedded runner, the small-CLI + JSON-pipes + approvals pattern, `.lobster` workflow files, `run`/`resume` tool params + optional inputs, the 3-status output envelope, safety model (local/no-secrets/sandbox-aware/hardened), and OpenProse pairing. |

## Section Coverage Map

```
gemini-search.md
├── (intro: Gemini + Google Search grounding) ─────────── → note 1 (oc_tools_gemini_search)
├── Get an API key ───────────────────────────────────── → note 1
├── Config ───────────────────────────────────────────── → note 1
├── How it works (grounding, SSRF-guarded citations) ──── → note 1
├── Supported parameters (query/freshness/date range) ─── → note 1
├── Model selection ──────────────────────────────────── → note 1
├── Base URL overrides ───────────────────────────────── → note 1
└── Related (web/brave/perplexity) ───────────────────── → note 1 References (link-out to08/pl)
grok-search.md
├── (intro: Grok xAI web-grounded; x_search/code_execution) → note 2 (oc_tools_grok_search)
├── Onboarding and configure ─────────────────────────── → note 2
├── Sign in or get an API key ────────────────────────── → note 2
├── Config ───────────────────────────────────────────── → note 2
├── How it works ─────────────────────────────────────── → note 2
├── Supported parameters (query; 60s timeout) ────────── → note 2
├── Base URL overrides ───────────────────────────────── → note 2
└── Related (web/x_search/gemini) ────────────────────── → note 2 References (link-out)
kimi-search.md
├── (intro: Kimi Moonshot web search) ────────────────── → note 3 (oc_tools_kimi_search)
├── Get an API key (+ region/model prompts) ──────────── → note 3
├── Config (.ai/.cn region reuse) ────────────────────── → note 3
├── How it works (grounding-evidence requirement) ────── → note 3
├── Supported parameters (query) ─────────────────────── → note 3
└── Related (web/moonshot/gemini/grok) ───────────────── → note 3 References (link-out)
goal.md
├── # Goal (intro: durable session objective) ────────── → note 4 (oc_tools_goal)
├── Quick start ──────────────────────────────────────── → note 4
├── What goals are for ───────────────────────────────── → note 4
├── Command reference ────────────────────────────────── → note 4
├── Statuses ─────────────────────────────────────────── → note 4
├── Token budgets ────────────────────────────────────── → note 4
├── Model tools (get/create/update_goal) ─────────────── → note 4
├── TUI ──────────────────────────────────────────────── → note 4
├── Channel behavior ─────────────────────────────────── → note 4
├── Troubleshooting ──────────────────────────────────── → note 4
└── Related (slash-commands/tui/session-tool/…) ──────── → note 4 References (link-out)
image-generation.md
├── (intro: image_generate async task model) ─────────── → note 5 (oc_tools_image_generation)
├── Quick start ──────────────────────────────────────── → note 5
├── Common routes ────────────────────────────────────── → note 5
├── Tool parameters ──────────────────────────────────── → note 5
├── Configuration ▸ Model selection (H3) ─────────────── → note 5
├── Configuration ▸ Provider selection order (H3) ────── → note 5
├── Configuration ▸ Image editing (H3) ───────────────── → note 5
├── Examples ─────────────────────────────────────────── → note 5
├── Supported providers ──────────────────────────────── → note 6 (oc_tools_image_generation_providers)
├── Provider capabilities (matrix) ───────────────────── → note 6
├── Provider deep dives (OpenAI/Foundry/OpenRouter/
│   fal Krea 2/MiniMax/xAI) ──────────────────────────── → note 6
└── Related (providers/config-ref/models) ────────────── → notes 5+6 References (link-out)
llm-task.md
├── (intro: optional JSON-only LLM task tool) ────────── → note 7 (oc_tools_llm_task)
├── Enable the plugin ────────────────────────────────── → note 7
├── Config (optional) ────────────────────────────────── → note 7
├── Tool parameters ──────────────────────────────────── → note 7
├── Output (details.json + schema validation) ────────── → note 7
├── Example: Lobster workflow step ▸ Important limitation (H3) → note 7
├── Safety notes ─────────────────────────────────────── → note 7
└── Related (thinking/subagents/slash-commands) ──────── → note 7 References (link-out)
lobster.md
├── (intro + Hook) ───────────────────────────────────── → note 8 (oc_tools_lobster)
├── Why / Why a DSL instead of plain programs? ───────── → note 8
├── How it works (in-process embedded runner) ────────── → note 8
├── Pattern: small CLI + JSON pipes + approvals ──────── → note 8
├── JSON-only LLM steps (llm-task) ▸ Important limitation (H3) → note 8 (cross-link note 7)
├── Workflow files (.lobster) ────────────────────────── → note 8
├── Install Lobster / Enable the tool ────────────────── → note 8
├── Example: Email triage ────────────────────────────── → note 8
├── Tool parameters ▸ run / resume / Optional inputs (H3) → note 8
├── Output envelope / Approvals ──────────────────────── → note 8
├── OpenProse / Safety / Troubleshooting ─────────────── → note 8
├── Learn more / Case study: community workflows ─────── → note 8 (+ References for external links)
└── Related (automation/tools overview) ──────────────── → note 8 References (link-out)
```
No orphaned sections. Every H2/H3 maps to a note. "Related" lists and external case-study/thread URLs become each note's `## References` (external URLs only) or link-outs to the owning sub-plan (to06/to07/to08, pr01–pr09, au01, co04/co06, gw01, rt03).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| image-generation.md (2,828w, 13 fences, 9 H2 / 3 H3) | note 5 `oc_tools_image_generation` (procedure) + note 6 `oc_tools_image_generation_providers` (model) | Exceeds the 2,500-word AND 6-fence caps, AND mixes two BBs: a *how-to-use-the-tool* procedure (auth, params, config, editing, examples) vs a *per-provider capability/reference* model (the 11-provider support table, the capability matrix, the provider deep-dives). Split per the word-cap, code-cap, and mixed-BB rules; keeps each note single-BB and ≤700w/≤6 fences. |
| (none — all other 6 pages stay 1 note) | — | gemini/grok/kimi (434–576w), goal (1,180w), llm-task (449w), lobster (1,624w) are each under the 2,500-word cap and single-BB; one note per page. Lobster's 17 fences are handled by reproducing only ~5–6 representative fences (Density Re-Assessment), not by splitting (the content is one coherent concept). |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (7,537 words, 45 code fences). New `oc_*` notes: **8**. New `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: **procedure ×5** (notes 1, 2, 3, 5, 7) · **concept ×2** (notes 4, 8) · **model ×1** (note 6).
- Est. digest words ~**4,680** (avg ~585/note); every note ≤720w, ≤6 code fences, single building_block, ≤400 lines.
- Code fences: only verbatim config/CLI/tool-call snippets reproduced, each note kept ≤6 (the fence-heavy `lobster.md` (17) and `image-generation.md` (13) are the binding constraints — Lobster keeps the most-illustrative ~5–6; image-generation's fences distribute across the two split notes ≤6 each).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_tools_gemini_search (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway product; relevance: subject system; Gemini is configured as one of its `web_search` providers.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: Gemini is the LLM that produces the grounded synthesized answer.
- [term_claude](../../term_dictionary/term_claude.md) — Anthropic Claude model family; relevance: the peer LLM provider OpenClaw also routes through the same provider/model config surface.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — externally-hosted GenAI APIs; relevance: Gemini/Google AI Studio is exactly such a third-party GenAI service requiring an API key.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — proxy fronting an upstream service; relevance: `webSearch.baseUrl` routes Gemini web search through an operator proxy / custom endpoint.
- [term_api_gateway](../../term_dictionary/term_api_gateway.md) — API-routing front door; relevance: the Gemini-compatible base-URL normalization (`/v1beta`) and proxy routing is an API-gateway pattern.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — models handling multiple modalities; relevance: Gemini is a multimodal model family; grounding fuses search results with generation.
- [term_ssrf_guard](../../term_dictionary/term_ssrf_guard.md) — server-side-request-forgery defense; relevance: citation redirect resolution uses the SSRF guard path (HEAD + redirect + http/https validation), blocking private targets.
- [term_contextual_grounding](../../term_dictionary/term_contextual_grounding.md) — anchoring generation to retrieved evidence; relevance: Google Search grounding returns AI-synthesized answers backed by live results with citations — the page's core mechanism.
- [term_credential_pool](../../term_dictionary/term_credential_pool.md) — managed pool of provider credentials; relevance: the `webSearch.apiKey → GEMINI_API_KEY → google.apiKey` precedence is a credential-resolution chain.

**Docs**
- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — Hermes web-search provider plugin contract; relevance: the sibling-ecosystem analog of OpenClaw's pluggable `web_search` provider that Gemini implements.
- [hermes_provider_google_gemini](../hermes_agent/hermes_provider_google_gemini.md) — Hermes Google/Gemini provider setup; relevance: the same Google/Gemini auth + base-URL config surface from the Hermes side.
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — Hermes web-search + content extraction; relevance: the grounding/citation-extraction behavior parallel to Gemini's synthesized-answer-with-citations.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — Hermes provider routing + proxies; relevance: the operator-proxy / base-URL override mechanism that `webSearch.baseUrl` implements.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — Hermes provider/auth/tool env vars; relevance: the `GEMINI_API_KEY` / provider env-var precedence equivalent.
- [hermes_tool_gateway](../hermes_agent/hermes_tool_gateway.md) — Hermes tool gateway; relevance: web_search is dispatched through the tool gateway, where Gemini is one provider.
- [hermes_configuring_models_dashboard](../hermes_agent/hermes_configuring_models_dashboard.md) — Hermes model configuration; relevance: model selection (`gemini-2.5-flash` default) parallels OpenClaw `webSearch.model`.
- [cc_environment_variables](../claude_code/cc_environment_variables.md) — Claude Code env var reference; relevance: peer coding-agent convention for provider API-key env vars (`GEMINI_API_KEY`-style).
- [oc_tools_grok_search](oc_tools_grok_search.md) — Grok `web_search` provider (planned, this series); relevance: sibling web-search provider with the same config shape.
- [oc_tools_kimi_search](oc_tools_kimi_search.md) — Kimi `web_search` provider (planned, this series); relevance: sibling web-search provider, region/base-URL reuse analog.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — OpenClaw LLM-provider extensions; relevance: implements the Google/Gemini provider extension that backs Gemini web search.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: dispatches the `web_search` tool call and runs the SSRF-guarded citation resolution.

**Snippets**
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — Hermes web tool implementations; relevance: the concrete `web_search` tool surface Gemini plugs into.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — Hermes web plugin; relevance: provider-plugin pattern for web search (Gemini analog).
- [snippet_hermes_agent_cli_web_config_schema](../../code_snippets/snippet_hermes_agent_cli_web_config_schema.md) — Hermes `web` config schema; relevance: exact analog of `openclaw configure --section web` apiKey/baseUrl/model fields.
- [snippet_hermes_agent_core_credential_pool_entry](../../code_snippets/snippet_hermes_agent_core_credential_pool_entry.md) — credential-pool entry; relevance: models the `apiKey → ENV → provider.apiKey` precedence Gemini uses.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: the multi-source key lookup (webSearch.apiKey / GEMINI_API_KEY / google.apiKey).
- [snippet_hermes_agent_core_gemini_cloudcode_adapter_auth](../../code_snippets/snippet_hermes_agent_core_gemini_cloudcode_adapter_auth.md) — Gemini adapter auth; relevance: Google/Gemini auth flow underlying the provider.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — providers registry; relevance: how a provider (Gemini) is registered/selected.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registry; relevance: the registry that exposes Gemini as a selectable provider.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw OpenAI provider; relevance: peer OpenClaw provider implementation showing the provider-config contract Gemini follows.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — gateway provider fallback context; relevance: provider/base-URL fallback resolution analog to Gemini's baseUrl precedence.

### oc_tools_grok_search (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: subject system; Grok is one of its `web_search` providers.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: Grok (xAI) is the LLM producing web-grounded synthesized answers.
- [term_xai](../../term_dictionary/term_xai.md) — xAI / Grok provider; relevance: Grok web search is powered by xAI web-grounded responses — the page's exact provider.
- [term_oauth](../../term_dictionary/term_oauth.md) — OAuth authorization; relevance: Grok web search prefers an existing xAI OAuth sign-in over an API key.
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth credential token; relevance: the xAI OAuth profile token is reused for web search, `x_search`, and `code_execution`.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — externally-hosted GenAI APIs; relevance: xAI/Grok is a third-party GenAI service.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — upstream-fronting proxy; relevance: `webSearch.baseUrl` routes Grok through an operator proxy / xAI-compatible Responses endpoint.
- [term_pkce](../../term_dictionary/term_pkce.md) — Proof Key for Code Exchange; relevance: the OAuth-preferred flow (`models auth login --method oauth`) is a PKCE-style device/OAuth sign-in.
- [term_auth_profile](../../term_dictionary/term_auth_profile.md) — stored provider auth profile; relevance: Grok reuses the existing xAI OAuth *profile* without prompting for a separate web-search key.
- [term_contextual_grounding](../../term_dictionary/term_contextual_grounding.md) — anchoring generation to evidence; relevance: xAI web-grounded responses synthesize answers with inline citations.

**Docs**
- [hermes_provider_xai_grok_oauth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — Hermes xAI/Grok OAuth provider; relevance: near-exact analog of Grok's xAI-OAuth-preferred onboarding.
- [hermes_x_search_grok](../hermes_agent/hermes_x_search_grok.md) — Hermes X (Twitter) search via Grok; relevance: the `x_search` follow-up tool the page references, on the Hermes side.
- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — web-search provider plugin; relevance: the pluggable `web_search` provider contract Grok implements.
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — web-search + extraction; relevance: grounded-answer + citation behavior parallel.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — provider routing + proxies; relevance: the Responses-endpoint/base-URL override Grok exposes.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env vars; relevance: `XAI_API_KEY` env fallback equivalent.
- [hermes_tool_gateway](../hermes_agent/hermes_tool_gateway.md) — tool gateway; relevance: web_search dispatch surface where Grok is a provider.
- [cc_environment_variables](../claude_code/cc_environment_variables.md) — Claude Code env vars; relevance: peer convention for provider API-key env vars (`XAI_API_KEY`).
- [oc_tools_gemini_search](oc_tools_gemini_search.md) — Gemini `web_search` provider (planned, this series); relevance: sibling provider with the same config/grounding shape.
- [oc_tools_kimi_search](oc_tools_kimi_search.md) — Kimi `web_search` provider (planned, this series); relevance: sibling provider; alternative grounded search.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: implements the xAI/Grok provider backing Grok web search.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agents; relevance: the agent tool catalog exposing `web_search` / `x_search` / `code_execution`.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: dispatches the Grok web-search call and applies the 60s timeout default.

**Snippets**
- [snippet_hermes_agent_plugins_provider_xai_oauth](../../code_snippets/snippet_hermes_agent_plugins_provider_xai_oauth.md) — xAI OAuth provider plugin; relevance: the exact xAI-OAuth-preferred credential flow Grok uses.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web tool implementations; relevance: the `web_search` / `x_search` tool surface.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web plugin; relevance: provider-plugin pattern for web search.
- [snippet_hermes_agent_cli_web_config_schema](../../code_snippets/snippet_hermes_agent_cli_web_config_schema.md) — web config schema; relevance: `configure --section web` apiKey/baseUrl fields Grok shares.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: OAuth-then-API-key credential resolution Grok follows.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: reusing one xAI OAuth profile across web_search/x_search/code_execution.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential ordering; relevance: the OAuth-preferred-then-key precedence Grok documents.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — providers registry; relevance: how the xAI provider is registered/selected.
- [snippet_hermes_agent_core_credential_pool_entry](../../code_snippets/snippet_hermes_agent_core_credential_pool_entry.md) — credential-pool entry; relevance: the multi-source xAI credential model.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw OpenAI provider; relevance: peer provider-config contract (Responses-style endpoint) Grok mirrors.

### oc_tools_kimi_search (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: subject system; Kimi is one of its `web_search` providers.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: Kimi (Moonshot) is the LLM producing the grounded answer.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — externally-hosted GenAI APIs; relevance: Moonshot/Kimi is a third-party GenAI service requiring KIMI/MOONSHOT keys.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — upstream-fronting proxy; relevance: `tools.web.search.kimi.baseUrl` overrides the search base URL / region host.
- [term_api_gateway](../../term_dictionary/term_api_gateway.md) — API-routing front door; relevance: the .ai vs .cn region base-URL routing reused from chat config.
- [term_deepseek](../../term_dictionary/term_deepseek.md) — DeepSeek non-US-host LLM provider; relevance: peer non-US-host provider analog (region/base-URL switching, key host mismatch caveat).
- [term_idempotency](../../term_dictionary/term_idempotency.md) — repeatable-without-side-effect behavior; relevance: the grounding-evidence guard returns a structured `kimi_web_search_ungrounded` error instead of wrapping a non-search reply, so retries are safe.
- [term_contextual_grounding](../../term_dictionary/term_contextual_grounding.md) — anchoring generation to evidence; relevance: Kimi is treated as successful only after Moonshot returns native web-search grounding evidence (citations / `search_results`).
- [term_credential_pool](../../term_dictionary/term_credential_pool.md) — managed provider-credential pool; relevance: `KIMI_API_KEY` / `MOONSHOT_API_KEY` source precedence.
- [term_information_retrieval](../../term_dictionary/term_information_retrieval.md) — retrieving relevant documents; relevance: Moonshot web search is the IR backend feeding Kimi's grounded synthesis.

**Docs**
- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — web-search provider plugin; relevance: the pluggable `web_search` provider contract Kimi implements.
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — web-search + extraction; relevance: grounded-answer + citation behavior, including the grounding-evidence requirement.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — provider routing + proxies; relevance: the region/base-URL override Kimi exposes (.ai vs .cn).
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env vars; relevance: `KIMI_API_KEY` / `MOONSHOT_API_KEY` env precedence equivalent.
- [hermes_tool_gateway](../hermes_agent/hermes_tool_gateway.md) — tool gateway; relevance: web_search dispatch surface where Kimi is a provider.
- [hermes_nous_portal_subscription](../hermes_agent/hermes_nous_portal_subscription.md) — Nous portal subscription/provider routing; relevance: alternate-host / regional provider routing analog (host-mismatch 401 caveat).
- [hermes_configuring_models_dashboard](../hermes_agent/hermes_configuring_models_dashboard.md) — model configuration; relevance: Kimi web-search model selection (`kimi-k2.6` default) and host config reuse.
- [cc_environment_variables](../claude_code/cc_environment_variables.md) — Claude Code env vars; relevance: peer convention for provider API-key env vars.
- [oc_tools_gemini_search](oc_tools_gemini_search.md) — Gemini `web_search` provider (planned, this series); relevance: sibling provider; grounded-search analog.
- [oc_tools_grok_search](oc_tools_grok_search.md) — Grok `web_search` provider (planned, this series); relevance: sibling provider; grounded-search analog.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: implements the Moonshot/Kimi provider backing Kimi web search.

**Snippets**
- [snippet_hermes_agent_plugins_provider_kimi_coding](../../code_snippets/snippet_hermes_agent_plugins_provider_kimi_coding.md) — Kimi (Moonshot) provider plugin def; relevance: the concrete Kimi/Moonshot provider definition with region base-URL.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web tool implementations; relevance: the `web_search` tool surface Kimi plugs into.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web plugin; relevance: provider-plugin pattern for web search.
- [snippet_hermes_agent_cli_web_config_schema](../../code_snippets/snippet_hermes_agent_cli_web_config_schema.md) — web config schema; relevance: `configure --section web` apiKey/baseUrl/model fields Kimi shares.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: KIMI/MOONSHOT multi-source key lookup.
- [snippet_hermes_agent_core_credential_pool_seeding](../../code_snippets/snippet_hermes_agent_core_credential_pool_seeding.md) — credential-pool seeding; relevance: seeding provider keys / host reuse from chat config.
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — China-cluster (.cn host) provider plugin; relevance: the .cn region/base-URL reuse and host-mismatch (401) handling Kimi documents.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — providers registry; relevance: how the Moonshot provider is registered/selected.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registry; relevance: registry exposing Kimi as a selectable provider.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — gateway provider fallback context; relevance: structured-error fallback (the `kimi_web_search_ungrounded` redirect-to-Brave/web_fetch suggestion).

### oc_tools_goal (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: subject system; the goal is OpenClaw session state.
- [term_persistent_goal](../../term_dictionary/term_persistent_goal.md) — durable per-session objective; relevance: this IS the concept the page documents — one durable goal attached to the session.
- [term_agent_steering](../../term_dictionary/term_agent_steering.md) — directing/steering an agent's target; relevance: operator-vs-model goal control (model can't silently move the target).
- [term_steering_files](../../term_dictionary/term_steering_files.md) — durable steering artifacts; relevance: the goal is durable session steering that survives restarts and moves with the session key.
- [term_human_in_the_loop](../../term_dictionary/term_human_in_the_loop.md) — human-gated agent control; relevance: operator-only pause/resume/clear; the model may only complete/block.
- [term_message_queue](../../term_dictionary/term_message_queue.md) — queue of detached/scheduled work; relevance: explicit contrast — a goal is NOT a task queue.
- [term_cron](../../term_dictionary/term_cron.md) — scheduled recurring jobs; relevance: explicit contrast — use cron/tasks/standing orders for detached/repeating work, a goal for one visible objective.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool/function invocation; relevance: `get_goal` / `create_goal` / `update_goal` are model tools exposed to harnesses.
- [term_open_loops](../../term_dictionary/term_open_loops.md) — unfinished tracked objectives; relevance: a goal keeps a concrete outcome visible across many turns (an open loop) until complete/cleared.
- [term_delegate_task](../../term_dictionary/term_delegate_task.md) — handing off managed sub-work; relevance: contrast partner — Task Flow / tasks fan out managed sub-work, distinct from the single durable goal.

**Docs**
- [hermes_persistent_goals](../hermes_agent/hermes_persistent_goals.md) — Hermes `/goal` persistent goals; relevance: near-exact analog — `/goal` lifecycle, statuses, and footer behavior on the Hermes side.
- [hermes_slash_commands_interactive_cli](../hermes_agent/hermes_slash_commands_interactive_cli.md) — Hermes interactive slash commands; relevance: `/goal` is a slash command; the command-surface analog.
- [hermes_cron_scheduling](../hermes_agent/hermes_cron_scheduling.md) — Hermes cron scheduling; relevance: the cron-vs-goal contrast (detached/repeating work vs durable objective).
- [hermes_kanban_multi_agent_board](../hermes_agent/hermes_kanban_multi_agent_board.md) — Hermes kanban task board; relevance: the task-queue contrast (managed fan-out work vs single goal).
- [hermes_agent_loop](../hermes_agent/hermes_agent_loop.md) — Hermes agent loop; relevance: the goal is the target the agent pursues across the multi-turn loop.
- [hermes_env_vars_runtime_messaging_behavior](../hermes_agent/hermes_env_vars_runtime_messaging_behavior.md) — runtime/messaging behavior; relevance: goal state is attached to the session key, not the transport/channel.
- [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — Claude Code scheduled-task model; relevance: the detached/scheduled-work contrast to the in-session goal.
- [cc_scheduling_options_comparison](../claude_code/cc_scheduling_options_comparison.md) — CC scheduling options comparison; relevance: peer framing of goal-vs-task-vs-cron-vs-standing-order choices.
- [oc_tools_lobster](oc_tools_lobster.md) — Lobster workflow runtime (planned, this series); relevance: workflows (multi-step pipelines) vs a single durable objective — the page contrasts them.
- [oc_tools_llm_task](oc_tools_llm_task.md) — llm-task plugin tool (planned, this series); relevance: sibling tool in the same Tools cluster; goal can frame an llm-task workflow's objective.

**Repos**
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — OpenClaw sessions; relevance: the goal is session state keyed by session key, surviving restarts — owned by the sessions module.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agents; relevance: exposes the `get/create/update_goal` model-tool surface to harnesses.

**Snippets**
- [snippet_hermes_agent_cli_goals](../../code_snippets/snippet_hermes_agent_cli_goals.md) — Hermes `goals.py` goal-judge verdict parse; relevance: the concrete goal lifecycle/verdict handling implementation analog.
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — session lifecycle patches; relevance: session state survives restarts / `/new` `/reset` clear it — goal lifecycle plumbing.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — gateway node session; relevance: session-key-attached state the goal rides on.
- [snippet_hermes_agent_gw_session_state](../../code_snippets/snippet_hermes_agent_gw_session_state.md) — gateway session state; relevance: per-session durable state model (where a goal lives).
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — agent tool catalog; relevance: registers the `get/create/update_goal` model tools.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: the registry that surfaces the goal model tools.
- [snippet_hermes_agent_core_conversation_loop_session_persist](../../code_snippets/snippet_hermes_agent_core_conversation_loop_session_persist.md) — session persistence in the loop; relevance: token-usage / session snapshot persistence the token-budget baseline depends on.
- [snippet_hermes_agent_tui_server_slash](../../code_snippets/snippet_hermes_agent_tui_server_slash.md) — TUI server slash-command handling; relevance: `/goal` command parsing + TUI footer states.
- [snippet_hermes_agent_tools_clarify](../../code_snippets/snippet_hermes_agent_tools_clarify.md) — clarify/operator-gate tool; relevance: operator-gated control (model cannot silently pause/resume — parallels clarify's human gate).

### oc_tools_image_generation (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: subject system; `image_generate` is its agent tool.
- [term_diffusion_model](../../term_dictionary/term_diffusion_model.md) — image diffusion model; relevance: the underlying generative model class (FLUX, gpt-image, etc.) `image_generate` drives.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — multi-modality models; relevance: image generation + reference-image editing is a multimodal capability.
- [term_model_failover](../../term_dictionary/term_model_failover.md) — automatic fallback to next model; relevance: `imageGenerationModel.fallbacks` tries the next candidate when a provider fails (verified substitute for missing `term_text_to_image`).
- [term_model_router](../../term_dictionary/term_model_router.md) — routing requests across models/providers; relevance: the provider-selection-order (model param → primary → fallbacks → auto-detect) is model routing.
- [term_oauth](../../term_dictionary/term_oauth.md) — OAuth authorization; relevance: ChatGPT/Codex OAuth routes image requests through the Codex Responses backend.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — externally-hosted GenAI APIs; relevance: OpenAI/Google/fal/etc. image backends are third-party GenAI services.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — repeatable-without-duplication behavior; relevance: the idempotent direct fallback sends only the *missing* images when active wake fails.
- [term_provider_routing](../../term_dictionary/term_provider_routing.md) — routing across providers; relevance: the auth-aware provider selection order and per-call exact-override behavior.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — SSRF / private-network guard; relevance: LAN/LocalAI endpoints stay blocked unless `dangerouslyAllowPrivateNetwork` is opted in.

**Docs**
- [hermes_image_generation](../hermes_agent/hermes_image_generation.md) — Hermes image generation; relevance: near-exact analog of the `image_generate` tool usage + config.
- [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — Hermes image-gen provider plugin; relevance: the pluggable image-provider backend `image_generate` dispatches to.
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tools reference; relevance: image/media tool parameters + async media delivery analog.
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — messaging media settings; relevance: how generated image attachments are delivered through the message tool.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — Hermes fallback providers; relevance: the primary/fallbacks/auto-detect provider chain for image generation.
- [hermes_configuring_models_dashboard](../hermes_agent/hermes_configuring_models_dashboard.md) — model configuration; relevance: `imageGenerationModel.primary/timeoutMs/fallbacks` config surface.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env vars; relevance: `OPENAI_API_KEY` / `GEMINI_API_KEY` / `OPENROUTER_API_KEY` quick-start auth.
- [pi_custom_streaming_api](../pi/pi_custom_streaming_api.md) — Pi custom streaming/async API; relevance: the async background-task + completion-agent-wake delivery model.
- [oc_tools_image_generation_providers](oc_tools_image_generation_providers.md) — image_generate provider/capability reference (planned, this series); relevance: the provider/capability half of the split — providers, matrix, deep dives.
- [oc_tools_gemini_search](oc_tools_gemini_search.md) — Gemini `web_search` provider (planned, this series); relevance: Google/Gemini auth (`GEMINI_API_KEY`/`GOOGLE_API_KEY`) reuse for the Google image route.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: implements the image-generation provider backends.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agents; relevance: the async background-task model + completion-agent wake that delivers generated images.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: records the background task, returns the task id, and applies the SSRF/private-network guard.

**Snippets**
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — Hermes image-gen tool; relevance: the concrete `image_generate` tool implementation (params, model ref, edit mode).
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen plugin dispatch; relevance: provider dispatch + selection-order analog.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision/reference-image dispatch; relevance: reference-image edit-mode (`image`/`images`) handling.
- [snippet_hermes_agent_core_codex_responses_adapter_init](../../code_snippets/snippet_hermes_agent_core_codex_responses_adapter_init.md) — Codex Responses adapter init; relevance: the ChatGPT/Codex OAuth route image requests use.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw OpenAI provider; relevance: the default `openai/gpt-image-2` route + OAuth-vs-API-key resolution.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — gateway fallback context; relevance: the primary→fallbacks→auto-detect provider chain.
- [snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — activate-fallback helper; relevance: failover to the next configured candidate on auth/rate-limit error.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — gateway outbound runner; relevance: delivering the completion reply / generated attachment through the message tool.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registry; relevance: auth-aware provider candidate list (auto-detection).
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: `image_generate` appears only when a provider is available (registry-conditioned tool).

### oc_tools_image_generation_providers (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: subject system; this note is its image-provider reference.
- [term_diffusion_model](../../term_dictionary/term_diffusion_model.md) — image diffusion model; relevance: each provider's default model (FLUX, gpt-image, grok-imagine, Krea) is a diffusion/image model.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — multi-modality models; relevance: the capability matrix covers generate + edit/reference (multimodal).
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — provider/model registry; relevance: the 11-provider support table + `action:"list"` runtime inspection IS a model catalog.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — externally-hosted GenAI APIs; relevance: every listed provider (OpenAI, Foundry, fal, MiniMax, xAI, …) is a third-party GenAI service.
- [term_xai](../../term_dictionary/term_xai.md) — xAI / Grok provider; relevance: the xAI `grok-imagine-image` deep dive (endpoints, aspect ratios, resolutions).
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — per-provider plugin backend; relevance: each provider is a plugin backend with its own auth + capability declaration.
- [term_oauth](../../term_dictionary/term_oauth.md) — OAuth authorization; relevance: Codex/ChatGPT OAuth (OpenAI) and `minimax-portal` OAuth (MiniMax) auth paths.
- [term_model_failover](../../term_dictionary/term_model_failover.md) — fallback across models; relevance: provider capability differences drive the failover/remap (geometry remap to closest supported size/aspect/resolution).
- [term_model_router](../../term_dictionary/term_model_router.md) — cross-provider routing; relevance: provider-prefix model refs (`openai/`, `fal/`, `microsoft-foundry/`) route to the right backend.

**Docs**
- [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — Hermes image-gen provider plugin; relevance: near-exact analog — per-provider image backend, default model, auth, capability declaration.
- [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — Hermes video-gen provider plugin; relevance: sibling media-provider plugin pattern (same capability-declaration shape).
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tools reference; relevance: per-provider media capability/parameter reference analog.
- [hermes_provider_xai_grok_oauth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — xAI/Grok provider; relevance: the xAI grok-imagine provider auth + setup deep dive.
- [hermes_provider_google_gemini](../hermes_agent/hermes_provider_google_gemini.md) — Google/Gemini provider; relevance: the Google image provider (gemini image preview) setup.
- [hermes_configuring_models_dashboard](../hermes_agent/hermes_configuring_models_dashboard.md) — model configuration; relevance: per-provider default models + deployment-name config (e.g. Microsoft Foundry).
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — fallback providers; relevance: provider capability gaps drive the geometry remap / failover behavior.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — Pi custom provider registration; relevance: registering a provider with its model + auth metadata (provider-catalog analog).
- [oc_tools_image_generation](oc_tools_image_generation.md) — image_generate usage (planned, this series); relevance: the usage half of the split — params, config, examples.
- [oc_tools_grok_search](oc_tools_grok_search.md) — Grok `web_search` provider (planned, this series); relevance: xAI credential shared with grok-imagine image generation.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: implements the per-provider image backends + capability declarations.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agents; relevance: `action:"list"`/`action:"status"` runtime provider inspection from the tool surface.

**Snippets**
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen plugin dispatch; relevance: per-provider dispatch + capability lookup.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-gen tool; relevance: provider/model ref parsing + geometry-hint forwarding.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registry; relevance: the registry of image providers + default models (`action:list`).
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw OpenAI provider; relevance: the OpenAI gpt-image-2/1.5 + Codex OAuth deep-dive backend.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator provider; relevance: the OpenRouter image-models deep dive (chat-completions image API).
- [snippet_hermes_agent_plugins_provider_kimi_coding](../../code_snippets/snippet_hermes_agent_plugins_provider_kimi_coding.md) — provider plugin def; relevance: concrete per-provider plugin definition shape (auth + model).
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — China-cluster provider plugin; relevance: alternate-host provider definition (MiniMax dual-auth / regional analog).
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen dispatch; relevance: sibling media-provider dispatch with the same per-provider capability pattern.
- [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision dispatch; relevance: reference-image edit limits per provider (capability matrix).
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — gateway fallback context; relevance: capability-driven geometry remap / closest-supported fallback.

### oc_tools_llm_task (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: subject system; llm-task is its optional plugin tool.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: llm-task runs a single LLM step (provider/model/maxTokens) inside a workflow.
- [term_structured_output](../../term_dictionary/term_structured_output.md) — model output constrained to a structure; relevance: llm-task is JSON-only and returns structured output — the page's core contract.
- [term_json_schema](../../term_dictionary/term_json_schema.md) — JSON Schema validation; relevance: `details.json` is validated against the optional `schema` parameter.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: llm-task is an optional tool the agent calls; `tools.alsoAllow` gates it.
- [term_chain_of_thought](../../term_dictionary/term_chain_of_thought.md) — explicit model reasoning; relevance: the `thinking` parameter accepts standard reasoning presets (`low`/`medium`).
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — per-provider plugin backend; relevance: llm-task selects a `provider`/`model` and respects an `allowedModels` allowlist.
- [term_subagent](../../term_dictionary/term_subagent.md) — delegated sub-agent; relevance: the page's Related links sub-agents as the alternative to a single JSON-only LLM step.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — safe-to-repeat behavior; relevance: JSON-only + no-tools-exposed + put-approvals-before-side-effects keeps an llm-task step safe to re-run.
- [term_agentic_workflow](../../term_dictionary/term_agentic_workflow.md) — multi-step agent workflow; relevance: llm-task is designed as a single LLM step inside workflow engines like Lobster.

**Docs**
- [cc_sdk_structured_output_schemas](../claude_code/cc_sdk_structured_output_schemas.md) — CC SDK type-safe schemas + structured-output errors; relevance: near-exact analog — schema-validated JSON output with error handling.
- [cc_sdk_structured_outputs](../claude_code/cc_sdk_structured_outputs.md) — CC SDK structured outputs; relevance: the structured/JSON output contract llm-task implements.
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — CC effort level + thinking; relevance: the `thinking` reasoning presets (`low`/`medium`) llm-task accepts.
- [hermes_plugin_llm_access](../hermes_agent/hermes_plugin_llm_access.md) — Hermes plugin LLM access; relevance: how a plugin tool gains LLM access (provider/model/auth profile) — the llm-task analog.
- [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — Hermes plugin authoring tutorial; relevance: enabling an optional plugin tool (`plugins.entries` + `tools.alsoAllow`).
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — Hermes built-in/optional plugins; relevance: llm-task is an optional plugin tool toggled on per-config.
- [pi_extensions_custom_tools](../pi/pi_extensions_custom_tools.md) — Pi custom tools extension; relevance: defining a custom/optional tool with typed parameters (peer pattern).
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — Hermes sub-agent delegation; relevance: the Related sub-agents alternative to a single llm-task step.
- [oc_tools_lobster](oc_tools_lobster.md) — Lobster workflow runtime (planned, this series); relevance: the workflow engine that embeds llm-task as a JSON-only LLM step (incl. the `openclaw.invoke` embedded-runner limitation).
- [oc_tools_goal](oc_tools_goal.md) — session goal (planned, this series); relevance: sibling Tools-cluster tool; a goal can frame an llm-task-driven workflow's objective.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions; relevance: the optional plugin-tool framework that hosts llm-task.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agents; relevance: `tools.allow` / `tools.alsoAllow` policy that enables the optional tool.

**Snippets**
- [snippet_hermes_agent_tools_schema_sanitizer](../../code_snippets/snippet_hermes_agent_tools_schema_sanitizer.md) — JSON-schema sanitizer; relevance: validating/normalizing the `schema` used to check `details.json`.
- [snippet_wf_schema_agent_contract](../../code_snippets/snippet_wf_schema_agent_contract.md) — workflow schema agent contract; relevance: schema-validated agent step contract (llm-task step analog).
- [snippet_hermes_agent_core_runtime_helpers_reasoning](../../code_snippets/snippet_hermes_agent_core_runtime_helpers_reasoning.md) — reasoning helper; relevance: applying the `thinking` reasoning preset to the model call.
- [snippet_hermes_agent_core_think_scrubber](../../code_snippets/snippet_hermes_agent_core_think_scrubber.md) — think/reasoning scrubber; relevance: JSON-only output requires stripping reasoning/commentary — the page's "output only JSON" rule.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool allow/alsoAllow policy; relevance: exactly the `tools.alsoAllow: ["llm-task"]` enablement.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: how the optional llm-task tool is registered/exposed.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: optional-tool registration (provider/model defaults).
- [snippet_hermes_agent_core_credential_pool_entry](../../code_snippets/snippet_hermes_agent_core_credential_pool_entry.md) — credential-pool entry; relevance: `defaultAuthProfileId`/provider credential resolution for the step.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw OpenAI provider; relevance: the `defaultProvider:"openai"` / `defaultModel` backend for the LLM step.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registry; relevance: resolving `provider`/`allowedModels` for the llm-task call.

### oc_tools_lobster (10t · 10s · 10d)

**Terms**
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: subject system; Lobster runs in-process as an embedded runner inside the gateway.
- [term_orchestration](../../term_dictionary/term_orchestration.md) — coordinating multi-step execution; relevance: the typed runtime moves orchestration off the LLM into a deterministic engine.
- [term_agentic_workflow](../../term_dictionary/term_agentic_workflow.md) — multi-step agent workflow; relevance: deterministic multi-step tool pipelines are exactly what Lobster runs.
- [term_human_in_the_loop](../../term_dictionary/term_human_in_the_loop.md) — human-gated control; relevance: explicit approval gates halt side-effecting steps until approved.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — safe-to-repeat / resumable; relevance: resume tokens continue a halted workflow without re-running earlier steps.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — sandboxed execution; relevance: Lobster is sandbox-aware and disabled when the tool context is sandboxed.
- [term_structured_output](../../term_dictionary/term_structured_output.md) — structured result; relevance: Lobster returns a JSON output envelope with one of three statuses.
- [term_task_decomposition](../../term_dictionary/term_task_decomposition.md) — breaking work into steps; relevance: small-CLI + JSON-pipes pattern decomposes a workflow into chained typed steps.
- [term_delegate_task](../../term_dictionary/term_delegate_task.md) — handing off managed work; relevance: one Lobster tool call replaces many back-and-forth LLM-orchestrated tool calls.
- [term_agent_orchestration](../../term_dictionary/term_agent_orchestration.md) — orchestrating agent steps; relevance: OpenProse pairs with Lobster — multi-agent prep then a deterministic Lobster pipeline.

**Docs**
- [hermes_kanban_worker_orchestrator](../hermes_agent/hermes_kanban_worker_orchestrator.md) — Hermes worker orchestrator; relevance: deterministic multi-step orchestration with approval/handoff — the closest Hermes analog.
- [cc_create_and_run_workflows](../claude_code/cc_create_and_run_workflows.md) — Claude Code workflows; relevance: authoring + running deterministic multi-step workflows (peer coding-agent analog).
- [hermes_cron_scheduling](../hermes_agent/hermes_cron_scheduling.md) — Hermes cron scheduling; relevance: scheduling Lobster workflows (the page's Automation Related link).
- [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — Hermes plugin authoring; relevance: Lobster is an optional plugin tool (`tools.alsoAllow: ["lobster"]`); plugin-tool authoring.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — built-in/optional plugins; relevance: the embedded Lobster runner ships with the Lobster plugin (not enabled by default).
- [hermes_plugin_llm_access](../hermes_agent/hermes_plugin_llm_access.md) — plugin LLM access; relevance: the JSON-only LLM step (llm-task) Lobster calls for classify/summarize/draft.
- [hermes_agent_loop](../hermes_agent/hermes_agent_loop.md) — Hermes agent loop; relevance: Lobster collapses many LLM-orchestrated loop turns into one deterministic tool call.
- [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — CC exec tool behavior; relevance: timeouts / output caps / sandbox checks enforced by the runtime — Lobster's safety model.
- [oc_tools_llm_task](oc_tools_llm_task.md) — llm-task plugin tool (planned, this series); relevance: the JSON-only LLM step inside Lobster, incl. the embedded-runner `openclaw.invoke` limitation.
- [oc_tools_goal](oc_tools_goal.md) — session goal (planned, this series); relevance: a durable goal can frame a Lobster pipeline's objective; both are in the Tools cluster.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — OpenClaw extensions; relevance: Lobster is an optional plugin tool in the extensions framework.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — OpenClaw gateway; relevance: the in-process embedded runner executes inside the gateway process (no subprocess, no network from the plugin).
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — OpenClaw agents; relevance: tool allowlists (`alsoAllow`) + sub-agent tools (`tools.subagents.tools`) for OpenProse.

**Snippets**
- [snippet_hermes_agent_core_aiagent_orchestrator](../../code_snippets/snippet_hermes_agent_core_aiagent_orchestrator.md) — agent orchestrator; relevance: moving orchestration into a runtime instead of the LLM.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — delegate spawn; relevance: one call fanning out steps (OpenProse sub-agent + Lobster pipeline pairing).
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool allow/alsoAllow policy; relevance: exactly `tools.alsoAllow: ["lobster"]` (and avoid restrictive `tools.allow`).
- [snippet_hermes_agent_core_tool_executor_sequential](../../code_snippets/snippet_hermes_agent_core_tool_executor_sequential.md) — sequential tool executor; relevance: chained step execution with stdin piping (`$step.stdout`/`$step.json`).
- [snippet_hermes_agent_tools_schema_sanitizer](../../code_snippets/snippet_hermes_agent_tools_schema_sanitizer.md) — JSON-schema sanitizer; relevance: the JSON-only-output / valid-JSON-envelope requirement (and the embedded llm-task step's schema).
- [snippet_hermes_agent_cli_kanban_decompose](../../code_snippets/snippet_hermes_agent_cli_kanban_decompose.md) — kanban decompose; relevance: decomposing a goal into ordered approvable steps (workflow-file analog).
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — gateway plugin context; relevance: the in-process plugin execution context the embedded runner uses.


## Undigested Terms Plan

Per master design decision: OpenClaw vocabulary is digested as `oc_*` documentation concept notes by their home sub-plan, NOT as new `term_dictionary` entries; the only `term_dictionary` interaction is **linking existing terms**. **Expected: 0 new `term_dictionary` captures.**

| Term (appears in to04 source) | Disposition |
|---|---|
| Gemini web search / Google Search grounding | → note 1 `oc_tools_gemini_search` (oc doc note); link `term_llm`, `term_multimodal`. NOT a new term. |
| Grok web search / xAI web-grounded responses / `x_search` | → note 2 `oc_tools_grok_search`; link `term_xai`, `term_oauth`. `x_search` is owned by to08 `tools/web` — link-out, NOT a term. |
| Kimi / Moonshot web search / `kimi_web_search_ungrounded` error | → note 3 `oc_tools_kimi_search`; link `term_third_party_genai_services`. NOT a new term. |
| Session goal / token budget / get_goal/create_goal/update_goal | → note 4 `oc_tools_goal`; link `term_agent_steering`, `term_human_in_the_loop`, `term_function_calling`. Goal vocabulary is doc-page-owned, NOT promoted. |
| `image_generate` / image generation / image editing / provider routing | → notes 5+6; link `term_diffusion_model`, `term_multimodal`, `term_model_failover`, `term_model_catalog`. NOT new terms. |
| Provider names (OpenAI, Google, fal, Microsoft Foundry, MiniMax, ComfyUI, DeepInfra, OpenRouter, LiteLLM, xAI, Vydra) | Documented as config in notes 5/6; link `term_llm`/`term_claude`/`term_xai`/`term_third_party_genai_services`. Provider names NOT promoted to term notes (owned by Providers section pr01–pr09). |
| `llm-task` / JSON-only LLM step / JSON Schema validation | → note 7 `oc_tools_llm_task`; link `term_structured_output`, `term_json_schema`. NOT a new term. |
| Lobster / workflow runtime / DSL / resume token / approval gate / `.lobster` files / OpenProse | → note 8 `oc_tools_lobster`; link `term_orchestration`, `term_agentic_workflow`, `term_human_in_the_loop`, `term_idempotency`. Lobster/OpenProse are doc-page-owned product names, NOT term-dictionary entries. |

**New-term candidates:** none. Probed for a reusable cross-cutting term with no doc-page home AND no existing note — none qualifies (`term_workflow_orchestration`, `term_dsl`, `term_web_search`, `term_x_search`, `term_grounding`, `term_token_budget`, `term_text_to_image`, `term_slash_command`, `term_thinking` were all checked: each is either OpenClaw-product vocabulary owned by an `oc_*` doc note or already covered by an existing broader term, e.g. `term_orchestration`/`term_agentic_workflow` cover workflow orchestration; `term_diffusion_model` covers image gen). If augment surfaces a genuine reusable term, it would be captured via `/tessellum-capture-term-note` + added to the agentic/LLM `acronym_glossary_*.md` (best fit: `acronym_glossary_genai_dev.md` / the agentic-coding glossary).

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P2). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format: YAML field order + forbidden-field absence; `# OpenClaw — …` H1, `## Overview`, `## Related Notes`, `## References`, `**Source**`/`**Last Updated**`/`**Status**` footer | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim traceable to `inbox/openclaw_docs/tools/<page>.md` (no invented config keys/params/provider facts) | diff vs mirror page |
| G3 | Density + Coverage: ≤400 lines, ≤2,500 words, ≤6 code fences, one building_block per note; every mapped H2/H3 covered | word/fence count + Section Coverage Map |
| G4 | Cross-Reference: `## Related Notes` ≥6 relevance-selected verified `term_dictionary` terms + sibling `oc_*` + `repo_openclaw*`/other vault notes, each an indexed `[text](path.md)` link with a relevance statement | per Candidate Cross-References (locked at augment) |
| G5 | Ghost-reference detect + redirect: no link to a non-existent note (e.g. NOT `term_text_to_image`/`term_web_search`/`term_x_search`); ghost matches redirected | `/tessellum-fix-ghost-references` |
| G6 | Broken-link fix: relative paths resolve from `resources/documentation/openclaw/` | `/tessellum-fix-broken-links` |
| G7/G8 | Discoverability: every new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/`; in-degree ≥1 (anti-island), satisfied via `entry_openclaw_docs.md` + the inlinks below | `note_links` query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_tools_gemini_search oc_tools_grok_search oc_tools_kimi_search oc_tools_goal oc_tools_image_generation oc_tools_image_generation_providers oc_tools_llm_task oc_tools_lobster"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + broken-link class
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url required (G2 provenance)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # has >=1 sibling oc_* related link (G4 series wiring)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "$n NO SIBLING oc_* LINK"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb fences)"
done

# YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# DB-verify a cross-ref target (note_name is the bare stem; note_id is path-qualified)
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for t in term_openclaw term_diffusion_model term_orchestration term_agentic_workflow term_model_failover \
         term_structured_output term_json_schema term_agent_steering term_human_in_the_loop term_idempotency \
         repo_openclaw_extensions_llm_providers repo_openclaw_gateway repo_openclaw_sessions; do
  echo "$t => $(sqlite3 "$DB" "SELECT IFNULL((SELECT 1 FROM notes WHERE note_name='$t' LIMIT 1),'MISSING')")"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Src fences | Fences in note | Within caps? |
|---|---|---|---:|---:|---:|---|
| 1 | oc_tools_gemini_search | procedure | 380 | 1 | 1 | ✅ |
| 2 | oc_tools_grok_search | procedure | 430 | 1 | 1–2 | ✅ |
| 3 | oc_tools_kimi_search | procedure | 360 | 1 | 1 | ✅ |
| 4 | oc_tools_goal | concept | 620 | 7 | ≤6 (keep `/goal` lifecycle + status + footer examples; trim repeats) | ✅ |
| 5 | oc_tools_image_generation | procedure | 700 | ~7 (of 13) | ≤6 (quick-start config + selection-order + 1–2 examples) | ✅ |
| 6 | oc_tools_image_generation_providers | model | 650 | ~6 (of 13) | ≤6 (capability matrix as table; 1–2 deep-dive config snippets) | ✅ |
| 7 | oc_tools_llm_task | procedure | 420 | 5 | ≤6 (enable + config + 1 Lobster-step example) | ✅ |
| 8 | oc_tools_lobster | concept | 720 | 17 | ≤6 (pattern pipe + workflow file + run/resume + output envelope) | ✅ (fences capped — see Split Decisions; NOT split, representative subset) |

No note exceeds 2,500 words or 400 lines. The two fence-heavy pages (lobster 17, image-generation 13) are the binding code-cap constraints: image-generation SPLIT so each half ≤6; lobster keeps only the ~5–6 most-illustrative fences (the rest are link-outs to the source). Each note holds exactly one building_block.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (created as the master pre-step W1) under the **Tools** section (to01–to08 cluster). Suggested grouping within the row set: a "Web search providers" trio (notes 1–3), "Session goal" (note 4), "Image generation" pair (notes 5–6), "Workflow tools" pair (notes 7–8). Each note receives its `entry_openclaw_docs.md` back-link at finalization (satisfies G7/G8). No separate sub-entry-point (the 8 to04 notes are part of the larger Tools section already indexed by the master hub).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify + add at execution; all targets below verified to exist 2026-06-20):

- `entry_openclaw_docs.md` (master pre-step W1) → **all 8 notes** (primary anti-island guarantee).
- `repo_openclaw_extensions_llm_providers` → notes 1, 2, 3, 5, 6 (the LLM/search/image provider extension code ↔ docs).
- `repo_openclaw_gateway` → notes 1, 5, 8 (web-search dispatch, image async task, in-process Lobster runner).
- `repo_openclaw_sessions` → note 4 (session goal state).
- `repo_openclaw_extensions` → notes 7, 8 (optional plugin tools).
- `repo_openclaw_agents` → notes 2, 4, 5, 7, 8 (tool catalog / model-tool surface / tool policy).
- `term_openclaw` → all 8 (subject term back-link), `term_diffusion_model`/`term_multimodal` → notes 5–6, `term_orchestration`/`term_agentic_workflow` → note 8, `term_structured_output`/`term_json_schema` → note 7, `term_agent_steering`/`term_human_in_the_loop` → note 4.
- `entry_code_snippets_openclaw` → notes 5, 6, 8 (links the image-gen/provider/tool-policy snippets cited above).

## Pacing Rules (inherited from master)

One execution phase (8 notes ≤ fan-out cap). Re-read each source page before drafting; reproduce config/CLI/tool-call snippets verbatim; one building_block per note; keep fences ≤6 (split image-generation, trim lobster). Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit. `git pull --rebase --autostash` first; commit + push the phase as one cycle; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: Per-Note Related Notes Mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21** (9/9 checkpoints PASS) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment pass:** xref-augment — re-read all 7 assigned source pages under `inbox/openclaw_docs/tools/`, then built and LOCKED the **Per-Note Related Notes Mapping** at the raised floors (**≥8 `term_dictionary` terms · ≥10 `code_snippets` · ≥10 docs under `resources/documentation/`** per note, PLUS relevant `repo_openclaw*` + sibling `oc_*`). Replaced the prior "Candidate Cross-References" section; updated the Summary Statistics cross-ref line to the raised standard.


| Note | BB | Terms | Snippets | Docs (≥5 existing) | Repos+entry | Floors met |
|---|---|---:|---:|---:|---:|---|
| oc_tools_gemini_search | procedure | 10 | 10 | 10 (8 existing + 2 oc_) | 2 repos + entry | ✅ |
| oc_tools_grok_search | procedure | 10 | 10 | 10 (8 existing + 2 oc_) | 3 repos + entry | ✅ |
| oc_tools_kimi_search | procedure | 10 | 10 | 10 (8 existing + 2 oc_) | 2 repos + entry | ✅ |
| oc_tools_goal | concept | 10 | 10 | 10 (8 existing + 2 oc_) | 2 repos + entry | ✅ |
| oc_tools_image_generation | procedure | 10 | 10 | 10 (8 existing + 2 oc_) | 3 repos + entry | ✅ |
| oc_tools_image_generation_providers | model | 10 | 10 | 10 (8 existing + 2 oc_) | 3 repos + entry | ✅ |
| oc_tools_llm_task | procedure | 10 | 10 | 10 (8 existing + 2 oc_) | 2 repos + entry | ✅ |
| oc_tools_lobster | concept | 10 | 10 | 10 (8 existing + 2 oc_) | 3 repos + entry | ✅ |



**New-term candidates:** **none.** Per the master design decision, OpenClaw tool vocabulary is digested as `oc_*` doc notes, not new `term_dictionary` entries. The re-read (Step 2d) surfaced no genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an existing note: `term_persistent_goal`, `term_orchestration`, `term_agentic_workflow`, `term_structured_output`, `term_json_schema`, `term_provider_plugin`, `term_model_failover`, `term_model_router`, `term_credential_pool`, `term_ssrf_guard`, `term_contextual_grounding` all already EXIST and were linked. Probed-and-MISSING (`term_text_to_image`, `term_web_search`, `term_x_search`) are OpenClaw/product vocabulary owned by `oc_*`/to08 doc notes (link-out), not promotable terms. Expected 0 new `term_dictionary` captures stands. (If a future pass surfaces a real reusable term, best-fit glossary = `acronym_glossary_genai_dev.md` / the agentic-coding glossary, per the Undigested Terms Plan.)

**Issues / carry-forward:** `entry_openclaw_docs.md` must be CREATED as the master pre-step W1 before execution (it is the sole anti-island inbound-link guarantee for all 8 notes and is cited in every note's mapping; currently MISSING from the DB by design).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only review of the augmented plan. CP7 word counts were re-measured from the actual mirror pages (body-only, excluding YAML frontmatter): gemini 411w, goal 1109w, grok 541w, image-generation 2779w (13 fences → confirms the split), kimi 405w, llm-task 417w, lobster 1589w (17 fences → confirms the fence-cap-not-split decision) — all within ±10% of the plan's Source-table figures, i.e. measured not guessed.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE present per batch | **PASS** | Single-phase G1–G6 + G7/G8 (Discoverability) table present (Per-Phase Validation Gate section); Validation Scripts implement G1/format, G3/density, G5/ghost (note_name DB probe), G6/broken-link, G7/G8 (note_links). |
| CP3 | Entry point inherited (entry_openclaw_docs at W1) | **PASS** | Entry Point Decision contributes 8 rows to `entry_openclaw_docs.md` (master pre-step W1, Tools cluster); each note gets its back-link at finalization (G7/G8). No sub-entry-point needed. |
| CP4 | Size | **PASS** | 8 notes ≤ 30 cap (single phase ≤ fan-out cap). |
| CP5 | Format derived | **PASS** | Inherits the master Format Definition derived from the existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora: YAML field order, `# OpenClaw — …` H1, `## Overview` / `## Related Notes` / `## References`, bold `**Source**`/`**Last Updated**`/`**Status**` footer; same forbidden-field list. Not invented. |
| CP6 | Density | **PASS** | Density Re-Assessment: every note ≤720w / ≤6 fences / ≤400 lines / single BB; image-generation SPLIT (2779w/13 fences > caps → 2 notes ≤6 each); lobster fence-capped (17→~5–6 representative, content is one coherent concept) — no borderline note left unaddressed. |
| CP7 | Sources measured | **PASS** | Re-measured 2026-06-21 (body-only): all 7 pages within ±10% of plan estimates; image-generation 2779w/13 fences and lobster 1589w/17 fences confirm the split + fence-cap decisions. |
| CP8 | Undigested terms + authoring reqs | **PASS** | Undigested Terms Plan present (every row dispositioned to an `oc_*` doc note + linked existing terms; **0 new term captures**); Term-Note Authoring Requirements present (N/A — 0 new terms; master multi-source mandate applies if a term surfaces). |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs to rename (no captures). All-notes dedup/collision audit: 8 planned `oc_*` doc notes checked against `term_dictionary/` AND `resources/documentation/` — none duplicate an existing term or doc (OpenClaw tool vocabulary has no existing `oc_*` doc home; sibling code-side `repo_openclaw*`/`snippet_*`/`hermes_*` notes are LINKED, not duplicated). `term_text_to_image`/`term_web_search`/`term_x_search` probed MISSING → excluded as ghosts; verified substitutes used. |

**RESULT: 9/9 (incl. CP8f) PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`. Pre-execution dependency: create `entry_openclaw_docs.md` (master W1) — it is the anti-island inbound-link source cited in every note's mapping.
