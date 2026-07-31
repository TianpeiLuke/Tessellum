---
title: Sub-Plan pr08 — OpenClaw Docs: Providers (SGLang, StepFun, Synthetic, Tencent, Together, Venice, Vercel AI Gateway)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["providers/sglang", "providers/stepfun", "providers/synthetic", "providers/tencent", "providers/together", "providers/venice", "providers/vercel-ai-gateway"]
---

# Sub-Plan pr08: Providers

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format, dedup-before-create, 9-GATE validation, undigested-terms
> policy, cross-references, and entry-point wiring (`entry_openclaw_docs.md`) are inherited from the master and are not re-derived here.

## Scope

The 7 provider reference pages covering the tail end of the alphabetized provider list: **SGLang** (self-hosted OpenAI-compatible
server), **StepFun** (dual standard / Step-Plan endpoints, China vs Global regions), **Synthetic** (Anthropic-Messages-compatible
proxy fronting open-weight HuggingFace models), **Tencent Cloud TokenHub** (Hy3 preview, tiered pricing), **Together AI**
(open-source model aggregator + video generation), **Venice AI** (privacy-focused inference, private vs anonymized modes),
and **Vercel AI Gateway** (unified multi-upstream gateway). Each page is a "how do I connect provider X to OpenClaw" reference:
provider id, auth env var / onboarding `--auth-choice`, base URL, built-in model catalog, and config example. **Priority P2**
(Phase B — features/integration). The code-side counterparts (`repo_openclaw_extensions_llm_providers`, the
`snippet_openclaw_provider_*` family) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 5,232 measured words. **Planned: 7 notes (1 per page; no splits).**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| SGLang | providers/sglang | 579 | 1 | 5 | 0 | procedure |
| StepFun | providers/stepfun | 750 | 1 | 6 | 0 | procedure |
| Synthetic | providers/synthetic | 644 | 1 | 4 | 0 | procedure |
| Tencent Cloud (TokenHub) | providers/tencent | 612 | 4 | 6 | 0 | procedure |
| Together AI | providers/together | 508 | 2 | 4 | 1 | procedure |
| Venice AI | providers/venice | 1,670 | 3 | 14 | 1 | procedure |
| Vercel AI gateway | providers/vercel-ai-gateway | 469 | 1 | 5 | 0 | procedure |

Notes on the measurement: `Code` = ` ``` ` fences / 2 (some pages embed `<CodeGroup>` / `<Steps>` MDX wrappers around
inner ` ```bash`/` ```json5 ` fences; tencent's 4 and venice's 3 fence-pairs are counted from the raw `grep -c '^```'`/2).
`H2` counts `## ` headings (including the trailing `## Related` card section, which is digested into `## References`, not body).
No page exceeds the 2,500-word density cap; venice (1,670w) is the largest and stays comfortably within caps.

## Content Strategy

- **Prioritize**: the auth + onboarding path for each provider (env var, `--auth-choice`, base URL) and the built-in model
  catalog (model refs, context window, reasoning/vision capability) — these are what a user needs to actually configure a run.
  For Venice, the **private-vs-anonymized privacy model** is the load-bearing distinction and is prioritized over the long
  41-model catalog (catalog summarized to representative rows, not reproduced verbatim).
- **Split**: **None.** All 7 pages are single-BB (procedure) provider-setup references and each is well under the 2,500-word /
  6-code-block caps. One page = one `oc_*` note. (See Split Decisions.)
- **Link-out** (do NOT duplicate): the shared model-selection / provider-rules / failover overview (`concepts/model-providers`,
  `concepts/models`) → linked, not redigested (owned by co04). The full config schema (`gateway/configuration-reference`,
  `gateway/configuration`) → linked (owned by gw02). Together's video-generation tool (`tools/video-generation`) → linked
  (owned by to08). Daemon env-var availability (`~/.openclaw/.env`, `env.shellEnv`) is summarized in-note (it recurs on
  tencent/together/venice/vercel) and cross-referenced rather than promoted to a new note. Provider/model vocabulary
  (model ref, anonymized inference, tiered pricing, model discovery) is captured in these `oc_*` notes, not as `term_dictionary`
  entries; existing terms (`term_llm`, `term_claude`, `term_function_calling`, `term_openai_responses_api`, etc.) are linked.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_providers_sglang.md` | procedure | sglang.md: property table, Getting started, Model discovery (implicit provider), Explicit configuration, Advanced configuration (proxy-style behavior, troubleshooting) | 480 | Connecting OpenClaw to a self-hosted SGLang server via the `openai-completions` family: `SGLANG_API_KEY` opt-in, `--auth-choice sglang`, implicit model auto-discovery from `/v1/models` vs explicit `models.providers.sglang` config, and proxy-style request shaping. |
| 2 | `oc_providers_stepfun.md` | procedure | stepfun.md: install plugin, region/endpoint overview, built-in catalog, Getting started (Standard / Step Plan tabs), Advanced configuration | 540 | Setting up the StepFun provider plugin's two surfaces (`stepfun` standard vs `stepfun-plan` Step-Plan), China (`.com`) vs Global (`.ai`) endpoints, `STEPFUN_API_KEY`, the step-3.5-flash catalog, and region-matched dual-profile onboarding. |
| 3 | `oc_providers_synthetic.md` | procedure | synthetic.md: property table, Getting started, Config example, Built-in catalog (21 models), model allowlist / base-URL override | 500 | Using Synthetic's Anthropic-Messages-compatible proxy (`synthetic` provider, `SYNTHETIC_API_KEY`, `api.synthetic.new/anthropic` with auto-`/v1`): onboarding, the `hf:`-prefixed open-weight model catalog, model allowlist, and base-URL override. |
| 4 | `oc_providers_tencent.md` | procedure | tencent.md: property table, Quick start, Non-interactive setup, Built-in catalog (Hy3 preview), Tiered pricing, Advanced configuration (endpoint override, daemon env availability) | 500 | Configuring Tencent Cloud TokenHub (`tencent-tokenhub` provider, `TOKENHUB_API_KEY`, `--auth-choice tokenhub-api-key`) for the Hy3-preview MoE model: quick/non-interactive onboarding, tiered cost metadata, China vs intl endpoint override, and daemon env availability. |
| 5 | `oc_providers_together.md` | procedure | together.md: property table, Getting started + Non-interactive example, Built-in catalog, Video generation, env/troubleshooting accordions | 460 | Connecting Together AI (`together` provider, `TOGETHER_API_KEY`, OpenAI-compatible) for open-source models (Llama/Kimi/DeepSeek/Qwen/GLM) plus the bundled `video_generate` Wan2.2 video model, with onboarding and daemon env notes. |
| 6 | `oc_providers_venice.md` | procedure | venice.md: Why Venice, Privacy modes, Features, Getting started, Model selection, DeepSeek V4 replay, Built-in catalog (41), Model discovery, Streaming/tool support, Pricing, Usage examples, Troubleshooting, Advanced configuration | 720 | Setting up Venice AI privacy-focused inference: the private-vs-anonymized mode distinction, `VENICE_API_KEY` (`vapi_`) onboarding, recommended-model selection, the DeepSeek-V4 `reasoning_content` replay fix, manifest-backed model discovery, and OpenAI-compatible config. |
| 7 | `oc_providers_vercel_ai_gateway.md` | procedure | vercel-ai-gateway.md: property table, Getting started, Non-interactive example, Model ID shorthand, Advanced configuration (daemon env, provider routing, thinking levels) | 440 | Using the Vercel AI Gateway (`vercel-ai-gateway` provider, `AI_GATEWAY_API_KEY`, Anthropic-Messages-compatible) as a unified multi-upstream gateway: `/v1/models` auto-discovery, model-ID shorthand normalization, per-upstream routing by ref prefix, and prefix-aware thinking levels. |

## Section Coverage Map

```
sglang.md
├── (intro property table: id/plugin/auth/api/baseUrl/model/streaming/pricing) → note 1 (oc_providers_sglang)
├── Getting started (start SGLang, set key, onboard/manual model) ──────────── → note 1
├── Model discovery (implicit provider) ───────────────────────────────────── → note 1
├── Explicit configuration (manual models) ────────────────────────────────── → note 1
├── Advanced configuration (proxy-style behavior, troubleshooting) ─────────── → note 1
└── Related (model-providers, configuration-reference) ─────────────────────── → note 1 ## References + link-out
stepfun.md
├── (intro: stepfun vs stepfun-plan, China/global warning) ─────────────────── → note 2 (oc_providers_stepfun)
├── Install plugin ────────────────────────────────────────────────────────── → note 2
├── Region and endpoint overview ──────────────────────────────────────────── → note 2
├── Built-in catalog (standard + step-plan) ───────────────────────────────── → note 2
├── Getting started (Standard / Step Plan tabs, Model refs H3s) ────────────── → note 2
├── Advanced configuration (full config standard/step-plan, notes) ─────────── → note 2
└── Related ────────────────────────────────────────────────────────────────── → note 2 ## References + link-out
synthetic.md
├── (intro property table + Anthropic-Messages note) ──────────────────────── → note 3 (oc_providers_synthetic)
├── Getting started (key, onboard, default model, /v1 warning) ─────────────── → note 3
├── Config example ────────────────────────────────────────────────────────── → note 3
├── Built-in catalog (21 hf: models) + allowlist / base-URL override ───────── → note 3
└── Related ────────────────────────────────────────────────────────────────── → note 3 ## References + link-out
tencent.md
├── (intro property table) ────────────────────────────────────────────────── → note 4 (oc_providers_tencent)
├── Quick start (create key, onboard CodeGroup, verify) ────────────────────── → note 4
├── Non-interactive setup ─────────────────────────────────────────────────── → note 4
├── Built-in catalog (hy3-preview) + Hy3/HY-3D disambiguation tip ──────────── → note 4
├── Tiered pricing ────────────────────────────────────────────────────────── → note 4
├── Advanced configuration (endpoint override, daemon env availability) ────── → note 4
└── Related ────────────────────────────────────────────────────────────────── → note 4 ## References + link-out
together.md
├── (intro property table) ────────────────────────────────────────────────── → note 5 (oc_providers_together)
├── Getting started (key, onboard, default model) ─────────────────────────── → note 5
│   └── Non-interactive example (H3) ───────────────────────────────────────── → note 5
├── Built-in catalog ──────────────────────────────────────────────────────── → note 5
├── Video generation (video_generate tool, Wan2.2, params) ─────────────────── → note 5 (+ link-out to08)
├── env / troubleshooting accordions ──────────────────────────────────────── → note 5
└── Related (model-providers, video-generation, configuration-reference) ───── → note 5 ## References + link-out
venice.md
├── (intro: privacy-focused inference) ────────────────────────────────────── → note 6 (oc_providers_venice)
├── Why Venice in OpenClaw ─────────────────────────────────────────────────── → note 6
├── Privacy modes (private vs anonymized table + warning) ──────────────────── → note 6
├── Features ───────────────────────────────────────────────────────────────── → note 6
├── Getting started (key, configure tabs, verify) ─────────────────────────── → note 6
├── Model selection (defaults, change, use-case table) ─────────────────────── → note 6
├── DeepSeek V4 replay behavior ───────────────────────────────────────────── → note 6
├── Built-in catalog (41: 26 private + 12 anonymized) ──────────────────────── → note 6 (summarized)
├── Model discovery ───────────────────────────────────────────────────────── → note 6
├── Streaming and tool support ────────────────────────────────────────────── → note 6
├── Pricing + (Venice anonymized vs direct API H3) ─────────────────────────── → note 6
├── Usage examples ────────────────────────────────────────────────────────── → note 6
├── Troubleshooting ───────────────────────────────────────────────────────── → note 6
├── Advanced configuration (config file example) ──────────────────────────── → note 6
└── Related ────────────────────────────────────────────────────────────────── → note 6 ## References + link-out
vercel-ai-gateway.md
├── (intro property table + auto-discovery tip) ───────────────────────────── → note 7 (oc_providers_vercel_ai_gateway)
├── Getting started (set key, default model, verify) ──────────────────────── → note 7
├── Non-interactive example ───────────────────────────────────────────────── → note 7
├── Model ID shorthand (normalization table) ──────────────────────────────── → note 7
├── Advanced configuration (daemon env, provider routing, thinking levels) ─── → note 7
└── Related (model-providers, troubleshooting) ─────────────────────────────── → note 7 ## References + link-out
```
No orphaned sections. `concepts/model-providers` + `concepts/models` (co04), `gateway/configuration*` (gw02), and
`tools/video-generation` (to08) are link-outs, not duplicated here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are single-BB (procedure) provider-setup references; each is ≤1,670 words and ≤6 code blocks, well within caps. The largest (venice, 1,670w / 14 H2) stays one cohesive provider-setup note — its sections (privacy modes, catalog, discovery, pricing, troubleshooting) all serve one task (configure Venice) and do not cross a BB boundary, so no split is warranted. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (5,232 measured words). New `oc_*` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×7** (every provider page is a setup/configuration how-to). No concept/model/argument notes.
- Est. digest words: ~3,640 (avg ~520/note); each note ≤720 words, ≤6 code blocks (config snippets reproduced selectively,
  verbatim). 14 source code fence-pairs distribute across the 7 notes; venice's 41-model catalog is summarized to
  representative rows (private vs anonymized) rather than reproduced in full to stay within the line cap.
- Cross-refs (LOCKED at xref-augment 2026-06-21): every note maps **≥8 relevancy-selected `term_dictionary` terms ·
  **Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)** below for the locked per-note mapping the executor
  copies verbatim.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

the master's ≥6-terms baseline for this xref-augment pass.) All snippets and all cited EXISTING terms/docs/repos were
exist yet → cited as **(planned, this series)** toward the 10-doc floor; **≥5 of the 10 docs per note are EXISTING
doc → `../<folder>/`; sibling oc_ → same dir; repo → `../../../areas/code_repos/`; snippet → `../../code_snippets/`).
Rendered in each note's `## Related Notes` as: `- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`.

`term_local_inference`, `term_inference_endpoint`, `term_data_privacy`, `term_video_generation`, `term_reasoning_model`,
`term_uncensored_model`, `term_open_weight_model`, `term_privacy`, `term_anonymization`, `term_proxy`, `term_streaming`,
`term_tool_use`, `term_kimi`, `term_moonshot`, `term_qwen3`, `term_glm`, `term_minimax`, `term_openai`, `term_openrouter`,
`term_tiered_pricing`, `term_model_ref`, `term_model_alias`, `term_environment_variable`, `term_daemon`,
`term_generative_ai`, `entry_openclaw_docs` (planned W1 — back-link added at finalization, not cited as existing).

### oc_providers_sglang (9t · 11s · 11d)

**Terms** (9, all `../../term_dictionary/`):
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: SGLang serves open-weight LLMs over an OpenAI-compatible API.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: this note configures OpenClaw to talk to SGLang.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider integration; relevance: `sglang` is a bundled plugin (`enabledByDefault: true`).
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — proxy fronting an upstream API; relevance: SGLang is treated as a proxy-style `/v1` backend, not native OpenAI (no OpenAI-only request shaping).
- [term_openai_responses_api](../../term_dictionary/term_openai_responses_api.md) — OpenAI HTTP API family; relevance: the connection uses the `openai-completions` API family.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — set of available models; relevance: auto-discovery converts `GET /v1/models` into catalog entries.
- [term_context_window](../../term_dictionary/term_context_window.md) — max input tokens; relevance: explicit config pins `contextWindow`/`maxTokens` per model.
- [term_sandbox](../../term_dictionary/term_sandbox.md) — isolated local execution; relevance: SGLang runs as a self-hosted local server (`127.0.0.1:30000`).
- [term_vllm](../../term_dictionary/term_vllm.md) — high-throughput LLM serving engine; relevance: SGLang is a sibling self-hosted OpenAI-compatible serving stack to vLLM.

**Docs** (11; 7 existing + 4 planned siblings):
- [pi_custom_models](../pi/pi_custom_models.md) — Pi local Ollama/vLLM/LM-Studio model config; relevance: closest precedent for a self-hosted OpenAI-compatible `models.providers.*` block.
- [pi_provider_auth](../pi/pi_provider_auth.md) — Pi provider auth/API-key wiring; relevance: SGLang's `SGLANG_API_KEY` opt-in mirrors Pi's per-provider auth.
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — Hermes self-hosted LLM setup; relevance: direct analog of pointing the agent at a local inference server.
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — Hermes local Ollama provider; relevance: same localhost base-URL + dummy-key pattern as SGLang.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — adding a new inference provider in Hermes; relevance: explains the OpenAI-compatible provider contract SGLang plugs into.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — pointing Claude Code at a custom base URL; relevance: same custom-`baseUrl` redirection SGLang uses.
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — Hermes model-catalog schema; relevance: documents the `/models` discovery → catalog conversion SGLang relies on.
- [oc_providers_synthetic](oc_providers_synthetic.md) — (planned, this series) Synthetic proxy provider; relevance: sibling OpenAI/Anthropic-compatible provider with base-URL override.
- [oc_providers_together](oc_providers_together.md) — (planned, this series) Together aggregator; relevance: sibling OpenAI-compatible provider with a bundled catalog.
- [oc_providers_venice](oc_providers_venice.md) — (planned, this series) Venice proxy; relevance: sibling provider using `/v1/models` discovery.
- [oc_providers_vercel_ai_gateway](oc_providers_vercel_ai_gateway.md) — (planned, this series) Vercel gateway; relevance: sibling provider with `/v1/models` auto-discovery.

**Repos** (3, `../../../areas/code_repos/`):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled provider plugin layer; relevance: implements the `sglang`/OpenAI-compatible backends this note configures.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime consuming the catalog; relevance: resolves discovered SGLang models for the agent.

**Snippets** (11, `../../code_snippets/`, all existing):
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — localhost base-URL + ignored apiKey + model list; relevance: exactly SGLang's local pattern.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider definition; relevance: the API family SGLang connects through.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — runtime model catalog; relevance: what `/v1/models` discovery populates.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — normalizes discovered model IDs; relevance: converts SGLang's `/models` IDs into entries.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — model schema normalization; relevance: shapes the `contextWindow`/`maxTokens` fields SGLang pins.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env resolution; relevance: how `SGLANG_API_KEY` reaches the provider.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — builds OpenAI HTTP request payloads; relevance: the request shaping SGLang's proxy-style path uses.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenAI-compatible aggregator provider; relevance: sibling OpenAI-compatible provider implementation.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom OpenAI-compatible provider plugin; relevance: SGLang is a custom-endpoint OpenAI-compatible provider.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — Ollama provider plugin; relevance: parallel self-hosted/local provider plugin.
- [snippet_hermes_agent_cli_models_fetch](../../code_snippets/snippet_hermes_agent_cli_models_fetch.md) — fetches a provider's `/models`; relevance: the discovery call analog to SGLang's `/v1/models`.

### oc_providers_stepfun (9t · 11s · 11d)

**Terms** (9):
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: StepFun serves step-3.5-flash LLMs.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: this note configures OpenClaw for StepFun.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: `@openclaw/stepfun-provider` is an official external plugin exposing two provider ids.
- [term_openai_responses_api](../../term_dictionary/term_openai_responses_api.md) — OpenAI HTTP API; relevance: both surfaces use the `openai-completions` API.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — model set; relevance: standard vs step-plan catalogs.
- [term_context_window](../../term_dictionary/term_context_window.md) — context length; relevance: 262,144-token step-3.5-flash context.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — proxy backend; relevance: China `.com` vs Global `.ai` endpoint surfaces front the same models.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI; relevance: StepFun is an external hosted provider.
- [term_data_residency](../../term_dictionary/term_data_residency.md) — regional data handling; relevance: China-key/`.com` vs intl-key/`.ai` region selection.

**Docs** (11; 7 existing + 4 planned siblings):
- [pi_custom_models](../pi/pi_custom_models.md) — provider-with-models config; relevance: StepFun's `models.providers.stepfun` block reuses this schema.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — separate-endpoint / merge-mode config; relevance: StepFun uses `models.mode: merge` and two endpoints.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — Hermes cloud provider setup; relevance: hosted-provider config analog for StepFun.
- [hermes_configuring_models_dashboard](../hermes_agent/hermes_configuring_models_dashboard.md) — configuring models/providers; relevance: the `models list`/`models set` workflow StepFun documents.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: `STEPFUN_API_KEY` placement.
- [cc_model_selection](../claude_code/cc_model_selection.md) — choosing/switching models; relevance: the `models set <provider/model>` analog for stepfun vs stepfun-plan.
- [cc_amazon_bedrock_mantle_endpoint](../claude_code/cc_amazon_bedrock_mantle_endpoint.md) — region/endpoint override; relevance: precedent for region-matched endpoint selection.
- [oc_providers_tencent](oc_providers_tencent.md) — (planned, this series) Tencent provider; relevance: sibling China-region provider with endpoint override.
- [oc_providers_synthetic](oc_providers_synthetic.md) — (planned, this series) Synthetic provider; relevance: sibling external-package provider with merge-mode catalog.
- [oc_providers_venice](oc_providers_venice.md) — (planned, this series) Venice provider; relevance: sibling `models.mode: merge` provider config.
- [oc_providers_vercel_ai_gateway](oc_providers_vercel_ai_gateway.md) — (planned, this series) Vercel gateway; relevance: sibling multi-endpoint routing by ref prefix.

**Repos** (3):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension layer; relevance: hosts external provider packages like `@openclaw/stepfun-provider`.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — gateway app lifecycle; relevance: `openclaw gateway restart` after plugin install.

**Snippets** (11, all existing):
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider/model definition; relevance: StepFun's two surfaces use this API.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — runtime model catalog; relevance: holds the standard + step-plan catalogs.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin install/load lifecycle; relevance: installing `@openclaw/stepfun-provider` before setup.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — external plugin package contract; relevance: the official-package contract StepFun's plugin satisfies.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — applies a config reload; relevance: gateway restart picks up the new provider.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — per-session model override; relevance: switching between `stepfun/...` and `stepfun-plan/...` refs.
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — China-region provider cluster plugin; relevance: direct analog of China vs global endpoint selection.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: registering two provider ids from one package.
- [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — model-switch CLI entry; relevance: the `models set` switch between StepFun surfaces.
- [snippet_hermes_agent_cli_models_normalize](../../code_snippets/snippet_hermes_agent_cli_models_normalize.md) — normalizes model refs; relevance: distinguishes `stepfun/` vs `stepfun-plan/` prefixes.

### oc_providers_synthetic (10t · 11s · 11d)

**Terms** (10):
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: Synthetic fronts open-weight HF LLMs.
- [term_claude](../../term_dictionary/term_claude.md) — Anthropic Claude model family; relevance: Synthetic uses the Anthropic Messages API surface.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: this note configures the `synthetic` provider in OpenClaw.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: registered as the `synthetic` provider.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — proxy backend; relevance: Synthetic is an Anthropic-compatible proxy fronting HF models; OpenClaw auto-appends `/v1`.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — model set; relevance: the 21-model `hf:`-prefixed catalog.
- [term_context_window](../../term_dictionary/term_context_window.md) — context length; relevance: per-model windows up to 524k (Llama-4-Maverick).
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI; relevance: Synthetic is an external proxy provider.
- [term_deepseek](../../term_dictionary/term_deepseek.md) — DeepSeek model family; relevance: many `hf:deepseek-ai/*` models in the catalog.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — text+image input; relevance: Kimi-K2.5 / Qwen3-VL accept `text + image`.

**Docs** (11; 7 existing + 4 planned siblings):
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Anthropic-compatible / proxy provider config; relevance: precedent for an Anthropic-Messages proxy provider.
- [pi_custom_models](../pi/pi_custom_models.md) — model-allowlist + base-URL-override schema; relevance: Synthetic's allowlist + base-URL override.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider setup; relevance: hosted Anthropic-compatible provider config analog.
- [hermes_model_aux_provider_config](../hermes_agent/hermes_model_aux_provider_config.md) — provider/model config schema; relevance: the `api: anthropic-messages` provider block.
- [cc_restrict_model_selection](../claude_code/cc_restrict_model_selection.md) — restricting allowed models; relevance: Synthetic's `agents.defaults.models` allowlist concept.
- [cc_authentication](../claude_code/cc_authentication.md) — API-key/auth config; relevance: `SYNTHETIC_API_KEY` onboarding.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: `SYNTHETIC_API_KEY` placement.
- [oc_providers_venice](oc_providers_venice.md) — (planned, this series) Venice proxy; relevance: sibling proxy fronting open + proprietary models.
- [oc_providers_together](oc_providers_together.md) — (planned, this series) Together aggregator; relevance: sibling open-weight aggregator catalog.
- [oc_providers_sglang](oc_providers_sglang.md) — (planned, this series) SGLang; relevance: sibling base-URL-override OpenAI/Anthropic-compatible provider.
- [oc_providers_vercel_ai_gateway](oc_providers_vercel_ai_gateway.md) — (planned, this series) Vercel gateway; relevance: sibling Anthropic-Messages-compatible provider with `/v1` handling.

**Repos** (3):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension layer; relevance: implements the `synthetic` Anthropic-Messages provider.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: resolves the model allowlist against the catalog.

**Snippets** (11, all existing):
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic-Messages provider definition; relevance: exactly Synthetic's `api: anthropic-messages` shape.
- [snippet_hermes_agent_plugins_provider_anthropic](../../code_snippets/snippet_hermes_agent_plugins_provider_anthropic.md) — adaptive-thinking / base-URL Anthropic provider plugin; relevance: Synthetic's base-URL + Anthropic-client `/v1` append.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — runtime model catalog; relevance: holds the 21 `hf:` models.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — model schema normalization; relevance: shapes per-model `contextWindow`/`reasoning`/`input` fields.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool/model availability gating; relevance: allowlist hides non-listed models from the agent.
- [snippet_hermes_agent_core_anthropic_adapter_oauth](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_oauth.md) — Anthropic adapter; relevance: the Anthropic-Messages client path Synthetic rides on.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: BYOK API-key auth for the proxy.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: Synthetic is a custom Anthropic-compatible endpoint.
- [snippet_hermes_agent_plugins_provider_kimi_coding](../../code_snippets/snippet_hermes_agent_plugins_provider_kimi_coding.md) — Kimi coding provider; relevance: Synthetic catalog includes Kimi-K2 models.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential ordering; relevance: how `SYNTHETIC_API_KEY` resolves into the provider.

### oc_providers_tencent (10t · 11s · 11d)

**Terms** (10):
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: Hy3 preview is an LLM served via TokenHub.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: this note configures the `tencent-tokenhub` provider.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: bundled `tencent-tokenhub` plugin (`enabledByDefault: true`).
- [term_openai_responses_api](../../term_dictionary/term_openai_responses_api.md) — OpenAI HTTP API; relevance: TokenHub uses the `openai-completions` API.
- [term_moe](../../term_dictionary/term_moe.md) — mixture-of-experts architecture; relevance: Hy3 preview is Tencent Hunyuan's large MoE model.
- [term_mixture_of_experts](../../term_dictionary/term_mixture_of_experts.md) — sparse expert routing; relevance: the architecture behind Hy3 preview.
- [term_chain_of_thought](../../term_dictionary/term_chain_of_thought.md) — explicit reasoning steps; relevance: reasoning-enabled model supporting `reasoning_effort`.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool-calling protocol; relevance: standard chat-completions tool calling supported.
- [term_context_window](../../term_dictionary/term_context_window.md) — context length; relevance: 256k context.
- [term_data_residency](../../term_dictionary/term_data_residency.md) — regional data handling; relevance: China vs international (`tokenhub-intl`) endpoint override.

**Docs** (11; 7 existing + 4 planned siblings):
- [pi_custom_models](../pi/pi_custom_models.md) — per-model cost/context config; relevance: the override-pricing / context analog.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider setup; relevance: hosted OpenAI-compatible provider config analog.
- [cc_model_selection](../claude_code/cc_model_selection.md) — choosing/switching models; relevance: the `models list --provider tencent-tokenhub` picker.
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — env-var availability for managed processes; relevance: `TOKENHUB_API_KEY` must reach launchd/systemd/Docker.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: daemon env availability for `TOKENHUB_API_KEY`.
- [cc_amazon_bedrock_mantle_endpoint](../claude_code/cc_amazon_bedrock_mantle_endpoint.md) — endpoint override; relevance: precedent for a region-specific endpoint override.
- [bedrock_cross_region_overview](../aws_bedrock/bedrock_cross_region_overview.md) — cross-region inference routing; relevance: China-vs-intl region selection analog.
- [oc_providers_stepfun](oc_providers_stepfun.md) — (planned, this series) StepFun; relevance: sibling China-region provider with `.com`/`.ai` endpoints.
- [oc_providers_vercel_ai_gateway](oc_providers_vercel_ai_gateway.md) — (planned, this series) Vercel gateway; relevance: sibling endpoint-override + daemon-env pattern.
- [oc_providers_venice](oc_providers_venice.md) — (planned, this series) Venice; relevance: sibling provider with tiered/credit pricing metadata.
- [oc_providers_together](oc_providers_together.md) — (planned, this series) Together; relevance: sibling daemon-env-availability note.

**Repos** (3):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension layer; relevance: implements the bundled `tencent-tokenhub` provider.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway daemon; relevance: daemon env availability via `~/.openclaw/.env` / `env.shellEnv`.

**Snippets** (11, all existing):
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider definition; relevance: TokenHub's API family.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — catalog with cost metadata; relevance: holds the `hy3-preview` entry + tiered cost.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing/alias lookup; relevance: the tiered cost-metadata resolution.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — pricing from upstream tables; relevance: how tiered per-window rates populate cost estimates.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd env for the daemon; relevance: making `TOKENHUB_API_KEY` visible to systemd.
- [snippet_openclaw_daemon_launchd_plist_render](../../code_snippets/snippet_openclaw_daemon_launchd_plist_render.md) — launchd plist rendering; relevance: env availability for a launchd-managed gateway.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env resolution; relevance: env-file vs shell-env precedence for the key.
- [snippet_openclaw_gateway_config_reload_apply](../../code_snippets/snippet_openclaw_gateway_config_reload_apply.md) — applies `config set` changes; relevance: the `config set ...baseUrl` endpoint override.
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — China-region provider cluster; relevance: direct analog of China vs intl TokenHub endpoints.
- [snippet_hermes_agent_cli_model_catalog](../../code_snippets/snippet_hermes_agent_cli_model_catalog.md) — CLI model catalog; relevance: `models list --provider` output for tencent-tokenhub.

### oc_providers_together (10t · 11s · 11d)

**Terms** (10):
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: Together serves open-source LLMs.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: this note configures the `together` provider.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: bundled `together` plugin that also registers a video model.
- [term_openai_responses_api](../../term_dictionary/term_openai_responses_api.md) — OpenAI HTTP API; relevance: Together is OpenAI-compatible.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — model set; relevance: bundled Llama/Kimi/DeepSeek/Qwen/GLM catalog.
- [term_context_window](../../term_dictionary/term_context_window.md) — context length; relevance: per-model contexts up to 512k (DeepSeek-V4-Pro).
- [term_diffusion_model](../../term_dictionary/term_diffusion_model.md) — generative diffusion model; relevance: the Wan2.2 text-to-video model.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI; relevance: Together is an open-source model aggregator service.
- [term_deepseek](../../term_dictionary/term_deepseek.md) — DeepSeek family; relevance: DeepSeek-V4-Pro in the bundled catalog.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — multi-input/output; relevance: Kimi-K2.6 text+image plus text-to-video.

**Docs** (11; 6 existing + 5 planned siblings):
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — gateway/aggregator provider config; relevance: hosted-aggregator provider precedent.
- [cc_model_selection](../claude_code/cc_model_selection.md) — choosing/switching models; relevance: model refs `together/<model-id>`.
- [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-generation provider plugin; relevance: Together's bundled `video_generate` Wan2.2 registration.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: daemon availability of `TOGETHER_API_KEY`.
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — env-var availability; relevance: key visible to the daemon-managed gateway.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider setup; relevance: OpenAI-compatible hosted-provider config analog.
- [oc_providers_synthetic](oc_providers_synthetic.md) — (planned, this series) Synthetic; relevance: sibling open-weight aggregator.
- [oc_providers_venice](oc_providers_venice.md) — (planned, this series) Venice; relevance: sibling multi-model proxy with vision/coding models.
- [oc_providers_vercel_ai_gateway](oc_providers_vercel_ai_gateway.md) — (planned, this series) Vercel gateway; relevance: sibling aggregator/gateway with one key for many upstreams.
- [oc_providers_sglang](oc_providers_sglang.md) — (planned, this series) SGLang; relevance: sibling OpenAI-compatible provider.
- [oc_providers_tencent](oc_providers_tencent.md) — (planned, this series) Tencent; relevance: sibling daemon-env-availability note.

**Repos** (3):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider + media-tool extensions; relevance: implements the `together` provider and its video tool.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: resolves the `video_generate` tool model and chat catalog.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway daemon; relevance: daemon env availability for `TOGETHER_API_KEY`.

**Snippets** (11, all existing):
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator fanning to many upstreams; relevance: closest analog to Together's open-model aggregation.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider definition; relevance: Together's API family.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog incl. media models; relevance: holds the chat catalog + video model.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media output pipeline; relevance: handling generated video output.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — managed media validation; relevance: media-asset handling for the video tool.
- [snippet_openclaw_daemon_systemd_linger_env](../../code_snippets/snippet_openclaw_daemon_systemd_linger_env.md) — systemd env for the daemon; relevance: making `TOGETHER_API_KEY` visible to systemd.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: `~/.openclaw/.env` vs shell-env key resolution.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: registers the shared `video_generate` tool.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: registering a provider + its bundled tool.
- [snippet_hermes_agent_cli_models_fetch](../../code_snippets/snippet_hermes_agent_cli_models_fetch.md) — fetch provider models; relevance: `models list --provider together` verification.

### oc_providers_venice (13t · 12s · 11d)

**Terms** (13):
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: Venice serves private + anonymized LLMs.
- [term_claude](../../term_dictionary/term_claude.md) — Anthropic Claude family; relevance: Claude Opus/Sonnet available anonymized via Venice's proxy.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: this note configures the `venice` provider.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: the `venice` provider with a manifest-backed seed catalog.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — proxy backend; relevance: anonymized models are proxied through Venice over OpenAI-compatible `/v1`.
- [term_data_minimization](../../term_dictionary/term_data_minimization.md) — strip non-essential data; relevance: Venice strips metadata before forwarding anonymized requests.
- [term_pii](../../term_dictionary/term_pii.md) — personally identifiable information; relevance: privacy/anonymization is the page's core value prop.
- [term_anonymized_data](../../term_dictionary/term_anonymized_data.md) — data with identifiers removed; relevance: the "anonymized" privacy mode forwards de-identified requests.
- [term_data_residency](../../term_dictionary/term_data_residency.md) — data-handling location/mode; relevance: private (ephemeral) vs anonymized (proxied) data modes.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool-calling; relevance: function calling supported on select models.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — text+image; relevance: vision-capable models in the catalog.
- [term_deepseek](../../term_dictionary/term_deepseek.md) — DeepSeek family; relevance: the DeepSeek-V4 `reasoning_content` replay-fix behavior.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — model set; relevance: the 41-model private/anonymized catalog + manifest discovery.

**Docs** (11; 6 existing + 5 planned siblings):
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — proxy/gateway provider config; relevance: precedent for a proxy provider.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — provider-specific compat/replay quirks; relevance: the DeepSeek-V4 `reasoning_content` replay fix.
- [cc_model_selection](../claude_code/cc_model_selection.md) — model refs and picker; relevance: `models set venice/...` model selection.
- [cc_extended_context_1m](../claude_code/cc_extended_context_1m.md) — 1M-token context; relevance: anonymized Claude/GPT/Gemini models expose 1M context.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider setup; relevance: hosted-proxy provider config analog.
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model-catalog schema; relevance: the manifest-backed seed catalog + runtime refresh.
- [oc_providers_synthetic](oc_providers_synthetic.md) — (planned, this series) Synthetic; relevance: sibling proxy fronting open-weight models.
- [oc_providers_vercel_ai_gateway](oc_providers_vercel_ai_gateway.md) — (planned, this series) Vercel gateway; relevance: sibling unified multi-upstream proxy.
- [oc_providers_together](oc_providers_together.md) — (planned, this series) Together; relevance: sibling multi-model OpenAI-compatible provider.
- [oc_providers_sglang](oc_providers_sglang.md) — (planned, this series) SGLang; relevance: sibling `/v1/models` discovery + manifest fallback.
- [oc_providers_tencent](oc_providers_tencent.md) — (planned, this series) Tencent; relevance: sibling reasoning-model + pricing-metadata note.

**Repos** (3):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension + manifest catalog; relevance: implements the `venice` provider and its seed manifest.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: resolves model refs / allowlist against the catalog.

**Snippets** (12, all existing):
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider definition; relevance: Venice's OpenAI-compatible `/v1` config block.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: BYOK / proxied-key auth modes for private vs anonymized.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest-backed catalog planner; relevance: Venice's manifest-backed seed catalog.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — normalizes discovered models; relevance: runtime refresh from the Venice `/models` endpoint.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — runtime model catalog; relevance: holds the 41 private/anonymized entries.
- [snippet_openclaw_agents_context_anthropic_prefix](../../code_snippets/snippet_openclaw_agents_context_anthropic_prefix.md) — assistant-message prefix handling; relevance: the DeepSeek-V4 `reasoning_content` replay-placeholder fill.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — reasoning/thinking modes; relevance: Venice rejects DeepSeek's native top-level `thinking` control.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — sanitizes request payloads; relevance: metadata stripping before anonymized forwarding.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — per-call credential/secret handling; relevance: `vapi_` API-key handling for private vs anonymized.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: Venice is a custom OpenAI-compatible endpoint.
- [snippet_hermes_agent_core_error_classifier_provider_maps](../../code_snippets/snippet_hermes_agent_core_error_classifier_provider_maps.md) — provider error mapping; relevance: handling Venice's rejection of native `thinking` control.

### oc_providers_vercel_ai_gateway (10t · 11s · 11d)

**Terms** (10):
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: the gateway fronts hundreds of upstream LLMs.
- [term_claude](../../term_dictionary/term_claude.md) — Anthropic Claude family; relevance: Claude routes via `vercel-ai-gateway/anthropic/...`.
- [term_openclaw](../../term_dictionary/term_openclaw.md) — the gateway; relevance: this note configures the `vercel-ai-gateway` provider.
- [term_api_gateway](../../term_dictionary/term_api_gateway.md) — unified API front door; relevance: Vercel AI Gateway is a unified gateway to upstream providers.
- [term_model_router](../../term_dictionary/term_model_router.md) — route requests by model; relevance: per-upstream routing by model-ref prefix with one shared key.
- [term_reverse_proxy](../../term_dictionary/term_reverse_proxy.md) — proxy backend; relevance: the gateway fronts many upstream APIs.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider integration; relevance: the `vercel-ai-gateway` provider.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — model set; relevance: auto-discovered `/v1/models` catalog.
- [term_chain_of_thought](../../term_dictionary/term_chain_of_thought.md) — explicit reasoning; relevance: prefix-aware `/think` thinking levels per upstream contract.
- [term_openai_responses_api](../../term_dictionary/term_openai_responses_api.md) — OpenAI HTTP API; relevance: OpenAI/Codex refs expose `/think xhigh` (Anthropic-Messages-compatible + OpenAI upstreams).

**Docs** (11; 6 existing + 5 planned siblings):
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Cloudflare/Vercel AI Gateway config; relevance: gateway-provider config precedent.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — routing-preference / gateway routing compat; relevance: `vercelGatewayRouting`-style per-upstream routing.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — LLM gateway base-URL routing; relevance: same unified-gateway base-URL pattern.
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — per-route provider selection; relevance: routing across upstreams under one gateway.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider setup; relevance: hosted unified-gateway config analog.
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — env-var availability; relevance: `AI_GATEWAY_API_KEY` must reach the daemon.
- [oc_providers_together](oc_providers_together.md) — (planned, this series) Together; relevance: sibling aggregator/gateway.
- [oc_providers_venice](oc_providers_venice.md) — (planned, this series) Venice; relevance: sibling proxy with per-prefix behavior + `/v1/models` discovery.
- [oc_providers_synthetic](oc_providers_synthetic.md) — (planned, this series) Synthetic; relevance: sibling Anthropic-Messages-compatible provider.
- [oc_providers_sglang](oc_providers_sglang.md) — (planned, this series) SGLang; relevance: sibling `/v1/models` auto-discovery provider.
- [oc_providers_tencent](oc_providers_tencent.md) — (planned, this series) Tencent; relevance: sibling daemon-env-availability note.

**Repos** (3):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider/gateway extension layer; relevance: implements the `vercel-ai-gateway` provider.

**Snippets** (11, all existing):
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — gateway fanning out to many upstreams; relevance: closest analog to a unified multi-upstream gateway.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: single-key unified-billing / BYOK auth modes.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — normalizes discovered models; relevance: the `/v1/models` auto-discovery the gateway uses.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — model schema normalization; relevance: shorthand-to-canonical model-ref normalization.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider definition; relevance: OpenAI/Codex upstream refs through the gateway.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic-Messages provider definition; relevance: the gateway is Anthropic-Messages-compatible; Claude upstreams.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — reasoning/thinking modes; relevance: prefix-aware `/think` levels per upstream contract.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: `AI_GATEWAY_API_KEY` daemon availability.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter gateway provider; relevance: sibling single-key multi-upstream gateway plugin.
- [snippet_hermes_agent_cli_models_normalize](../../code_snippets/snippet_hermes_agent_cli_models_normalize.md) — normalizes model refs; relevance: shorthand `opus-4.6` → canonical `anthropic/claude-opus-4-6`.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: dispatches a request to the resolved upstream provider, the gateway-routing analog.

## Undigested Terms Plan

Per master: OpenClaw provider/model vocabulary is digested INTO these `oc_*` doc notes (not promoted to `term_dictionary`);
the only `term_dictionary` interaction is LINKING existing terms. Expected new term captures: **0**.

| Term (as it appears in source) | Disposition |
|---|---|
| SGLang / StepFun / Synthetic / Tencent TokenHub / Together AI / Venice AI / Vercel AI Gateway (provider names) | Documented as provider config inside the respective `oc_providers_*` note; NOT promoted to term notes (provider names are not reusable cross-cutting concepts). Link `term_llm` / `term_third_party_genai_services`. |
| `openai-completions` / `anthropic-messages` (API families) | Documented in-note; link existing `term_openai_responses_api` / `term_claude`. No new term. |
| model discovery / implicit provider / `/v1/models` auto-discovery | Captured in `oc_providers_sglang` / `oc_providers_venice` / `oc_providers_vercel_ai_gateway`; link `term_model_catalog`. No new term. |
| private vs anonymized inference (Venice privacy modes) | Captured in `oc_providers_venice`; link existing `term_data_minimization` / `term_pii` / `term_data_residency`. No new term. |
| Hy3 preview / MoE reasoning model | Captured in `oc_providers_tencent`; link `term_moe` / `term_mixture_of_experts` / `term_chain_of_thought`. No new term. |
| tiered pricing / cost metadata | Captured in `oc_providers_tencent`; no existing `term_tiered_pricing` (MISSING) — described in-note, not promoted (single-page, not cross-cutting). |
| video generation (`video_generate`, Wan2.2) | Captured (briefly) in `oc_providers_together`; primary owner is `tools/video-generation` (to08). Link `term_diffusion_model`; existing `term_video_generation` is MISSING — not promoted here (deferred to to08's scope). |
| DeepSeek V4 `reasoning_content` replay | Captured in `oc_providers_venice`; link `term_deepseek` / `term_chain_of_thought`. No new term. |
| model ref / model-ID shorthand / normalization | Captured in `oc_providers_vercel_ai_gateway`; `term_model_ref` / `term_model_alias` are MISSING — described in-note, not promoted (provider-config detail). |
| daemon env-var availability (`~/.openclaw/.env`, `env.shellEnv`) | Summarized in-note (recurs on tencent/together/venice/vercel); `term_environment_variable` / `term_daemon` MISSING — link `cc_configure_your_environment`. Not promoted (operational detail, gw-owned). |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term with no existing note and no doc-page home
surfaced in these 7 pages. (If augment's Step-2d re-scan disagrees, the single highest-value candidate would be a generic
"model ref" or "model discovery" concept — but both are OpenClaw-config-specific and belong in the `oc_*` doc notes, and a
generic glossary slug would collide with the broader model-catalog vocabulary already covered by `term_model_catalog`.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; it only LINKS existing terms (inherited from
master). If augment proposes a new term, the master's W5 applies: capture via `/tessellum-capture-term-note` (multi-source
research) + add to the appropriate `acronym_glossary_*.md` (the agentic/LLM glossary).

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P2). All gates must PASS before commit.

| Gate | Check | Tool / Method | Pass criterion |
|---|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` | YAML field order/forbidden-fields OK; `# OpenClaw — …` H1; `## Overview` + `## Related Notes` + `## References` present; bold footer. |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/providers/<page>.md` | No invented provider ids/env vars/base URLs/model refs; config snippets reproduced verbatim from source. |
| G3 | Density + Coverage | word/code/line count; Section Coverage Map | ≤2,500 words, ≤6 code blocks, ≤400 lines, one BB; every source H2/H3 mapped to a note. |
| G4 | Cross-Reference | count Related Notes links | ≥6 relevancy-selected `term_dictionary` terms + sibling `oc_*` + `repo_openclaw*` + other vault notes, each with a relevance statement. |
| G5 | Ghost-reference detect + redirect | `/tessellum-fix-ghost-references` + DB existence | 0 links to non-existent notes; MISSING candidates dropped (already pruned in Candidate Cross-References). |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` | 0 broken relative paths after reindex. |
| G7 | Discoverability (outbound) | note has outbound links | each note links ≥6 terms + siblings + repos. |
| G8 | Discoverability (inbound, in-degree ≥1) | `note_links` query | each new note RECEIVES ≥1 inbound link from OUTSIDE `documentation/openclaw/` (via `entry_openclaw_docs.md` + the inlinks below). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_providers_sglang oc_providers_stepfun oc_providers_synthetic oc_providers_tencent oc_providers_together oc_providers_venice oc_providers_vercel_ai_gateway"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections
  for s in "## Overview" "## Related Notes"; do
    grep -qF "$s" "$f" || echo "MISSING SECTION [$s]: $n"
  done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url: $n"; }
  # at least one sibling oc_ cross-link
  grep -q "($SIBLING_PREFIX" "$f" || grep -q "]($SIBLING_PREFIX" "$f" || echo "NO SIBLING oc_ LINK: $n"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w, $cb cb, $lines L)"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G8 in-degree (after reindex): each note must have ≥1 inbound link from outside the folder
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  [ "${deg:-0}" -ge 1 ] || echo "G8 FAIL (no outside inbound): $n"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_providers_sglang | procedure | 480 | 2 | ✅ |
| 2 | oc_providers_stepfun | procedure | 540 | 3 | ✅ |
| 3 | oc_providers_synthetic | procedure | 500 | 2 | ✅ |
| 4 | oc_providers_tencent | procedure | 500 | 3 | ✅ |
| 5 | oc_providers_together | procedure | 460 | 2 | ✅ |
| 6 | oc_providers_venice | procedure | 720 | 3 | ✅ |
| 7 | oc_providers_vercel_ai_gateway | procedure | 440 | 1 | ✅ |

No note approaches the caps (≤2,500w / ≤6 code / ≤400 lines). venice (720w) is the largest; its 41-model catalog is
summarized (private vs anonymized representative rows) rather than reproduced in full to keep the note focused and within line
budget. Config JSON5 snippets are reproduced verbatim, one per note (sglang/stepfun/synthetic/venice show a full
`models.providers.*` block; tencent/together/vercel use shorter `config set` / model-default snippets).

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as master pre-step W1) under the **Providers** section/cluster:
`oc_providers_sglang`, `oc_providers_stepfun`, `oc_providers_synthetic`, `oc_providers_tencent`, `oc_providers_together`,
`oc_providers_venice`, `oc_providers_vercel_ai_gateway`. Each note receives its entry-point back-link at finalization
(this satisfies G8 in-degree ≥1 from outside the folder). Per master W2/W3, the docs hub also links from

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; all sources below confirmed present except
`entry_openclaw_docs` which is created in master pre-step W1):

- `entry_openclaw_docs.md` (planned, W1) → all 7 notes (primary G7/G8 satisfier).
- `repo_openclaw_extensions_llm_providers.md` → all 7 (it implements the provider/extension layer these pages configure).
- `repo_openclaw.md` → notes 1, 4 (bundled providers `sglang` / `tencent-tokenhub`).
- `term_llm.md` → all 7 (every provider fronts an LLM).
- `term_claude.md` → notes 3, 6, 7 (Synthetic Anthropic-Messages; Venice/Vercel route Claude).
- `term_data_minimization.md` / `term_pii.md` → note 6 (Venice privacy/anonymization).
- `term_moe.md` / `term_mixture_of_experts.md` → note 4 (Hy3 preview MoE).
- `term_api_gateway.md` / `term_model_router.md` → note 7 (Vercel AI Gateway).
- `term_diffusion_model.md` → note 5 (Together Wan2.2 video model).
- Sibling `pi_cloud_providers.md` / `pi_custom_models.md` → reciprocal cross-links to the closest provider-config precedents.

## Pacing Rules (inherited from master)

One execution phase, 7 notes (≤30 fan-out cap). 8 gates must PASS before commit. Re-read each source page before writing;
reproduce config snippets verbatim; one BB (procedure) per note. `git pull --rebase --autostash` first; commit+push after the
phase; no Claude co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links + G8 in-degree ≥1 before commit.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment: per-note Related mapping LOCKED at raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CPs PASS)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this pass:** xref-augment — built and LOCKED the per-note Related Notes mapping at raised floors
`## Candidate Cross-References` section with `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`. All 7
false-positives; no padding). Measured words confirmed identical to the Source table (sglang 579 · stepfun 750 ·
synthetic 644 · tencent 612 · together 508 · venice 1670 · vercel-ai-gateway 469).


| Note | Terms | Snippets | Docs (existing + planned-sibling) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_providers_sglang | 9 | 11 | 11 (7 + 4) | 3 | ✅ |
| oc_providers_stepfun | 9 | 11 | 11 (7 + 4) | 3 | ✅ |
| oc_providers_synthetic | 10 | 11 | 11 (7 + 4) | 3 | ✅ |
| oc_providers_tencent | 10 | 11 | 11 (7 + 4) | 3 | ✅ |
| oc_providers_together | 10 | 11 | 11 (6 + 5) | 3 | ✅ |
| oc_providers_venice | 13 | 12 | 11 (6 + 5) | 3 | ✅ |
| oc_providers_vercel_ai_gateway | 10 | 11 | 11 (6 + 5) | 3 | ✅ |

**DB-verification (deterministic G5):** every cited EXISTING term/doc/repo/snippet `note_id` was confirmed present via
provider snippets). Docs floor uses the rich `pi_*` / `claude_code/cc_*` / `hermes_agent/hermes_*` / `aws_bedrock/bedrock_*`
coding-agent corpora; each note carries ≥5 EXISTING docs (6-7 here) toward the 10-doc floor, the remainder being planned
siblings in this series.

(provider init/dispatch — the gateway-routing analog). No other ghosts.

no vault term note exists), plus the plan-stage drop list (`term_video_generation`, `term_uncensored_model`,
`term_open_weight_model`, `term_self_hosting`, `term_local_inference`, `term_privacy`, `term_anonymization`, `term_proxy`,
`term_kimi`, `term_glm`, `term_minimax`, `term_tiered_pricing`, `term_model_ref`, etc.). `entry_openclaw_docs` remains
planned (master W1) — back-link added at finalization, not cited as existing.

**New-term candidates:** **none.** The Step-2d re-scan of all 7 re-read pages surfaced no genuinely cross-cutting,
vault-reusable term that (a) has no existing vault note AND (b) has no `oc_*` doc-page home. Two near-candidates and their
best-fit glossary disposition:
- *model discovery / `/v1/models` auto-discovery* — best-fit glossary would be the agentic/LLM glossary
  (`0_entry_points/acronym_glossary_*` agentic/LLM), but it is OpenClaw-config-specific and is digested INTO
  `oc_providers_sglang` / `oc_providers_venice` / `oc_providers_vercel_ai_gateway`; existing `term_model_catalog` already
  covers the reusable concept. NOT promoted.
- *anonymized inference (Venice privacy mode)* — best-fit glossary would be the privacy/data glossary, but existing
  `term_anonymized_data` + `term_data_minimization` + `term_pii` + `term_data_residency` already cover it; the OpenClaw-specific
  "private vs anonymized mode" detail is digested into `oc_providers_venice`. NOT promoted.

This is consistent with the master's design decision (OpenClaw vocabulary is digested into `oc_*` doc notes, not promoted to
`term_dictionary`). Expected new term captures remain **0**.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review run after the xref-augment pass. CP7 source words were re-measured (not from memory).

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step exists — ≥8 terms + floors (≥10 snippets, ≥10 docs) per note, each link with a relevance statement | **PASS** | `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)` present; floor audit per note 9-13 terms / 11-12 snippets / 11 docs; every link rendered `- [Name](relpath.md) — what; relevance: why`. Floors exceed the ≥8/≥10/≥10 standard for all 7. |
| CP2 | 9-GATE present per batch (G1-G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Ref, G5 Ghost-detect+redirect, G6 Broken-link fix, G7 outbound discoverability, G8 inbound in-degree ≥1; `## Validation Scripts` implements format/density/source_url/sibling-link/G8-indegree checks. |
| CP4 | Plan size | **PASS** | 7 notes ≤ 30 fan-out cap; single execution phase; no split needed. |
| CP5 | Note format derived (not invented) | **PASS** | Master Format Definition derived from `pi_*`/`cc_*` corpora; spot-checked `pi_cloud_providers.md` — YAML field order (`tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group`) + `# Pi — <Title>` → `## Overview` → `## Related Notes` → `## References` match the plan's spec exactly. |
| CP6 | Density | **PASS** | `## Density Re-Assessment`: every note ≤720 words / ≤3 code blocks / well under ≤2500w·≤6cb·≤400L caps; venice (720w, largest) catalog summarized to representative rows. No borderline note. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-measured all 7 pages with `wc -w`: 579/750/644/612/508/1670/469 — identical to the plan's Source table (ratio ≈1.00). No under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present, 0 new terms (all rows dispositioned to in-note capture + existing-term links, each with rationale); `## Term-Note Authoring Requirements` present as N/A-with-fallback (0 new terms; master W5 applies if augment proposes one). New-term scan this pass surfaced none. |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new `term_dictionary` slugs created → no specificity/collision risk. All planned `oc_*` doc slugs checked against `term_dictionary/` + `documentation/`: no `oc_providers_*` slug duplicates an existing term or doc note (sibling oc_ docs DB-confirmed absent; the broader provider/model vocabulary is owned by existing `term_*` notes, which are LINKED not duplicated). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound source (`entry_openclaw_docs`, `repo_openclaw_extensions_llm_providers` → all 7; plus per-note term/repo/sibling-doc inlinks); G8 in-degree ≥1 gated in the gate table + Validation Scripts (DB in-degree check). Inlinks are an EXECUTED phase at finalization, not merely recommended. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
