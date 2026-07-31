---
title: Sub-Plan pr06 — OpenClaw Docs: Providers (NVIDIA, Ollama, OpenAI, OpenCode, OpenRouter)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["providers/nvidia", "providers/ollama", "providers/ollama-cloud", "providers/openai", "providers/opencode", "providers/opencode-go", "providers/openrouter"]
---

# Sub-Plan pr06: Providers

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order, `## Overview`/`## Related Notes`/`## References`/bold footer, ≤400L/≤2500w/≤6 code, one BB/note), dedup (three-way across term_dictionary + documentation/ + repo_openclaw*), 9-GATE, cross-refs, and entry-point wiring are ALL inherited from the master.

## Scope

The 7 provider pages for the "open-*" / Ollama / OpenAI provider cluster: NVIDIA's free OpenAI-compatible API (Nemotron 3 Ultra), Ollama (local + cloud + hybrid, vision, embeddings, web search), Ollama Cloud (the dedicated cloud-only provider id), OpenAI (Codex-runtime agent models + direct API key, images/video/voice/Azure), OpenCode (Zen + Go hosted catalogs), OpenCode Go (the Go catalog sibling), and OpenRouter (unified aggregator API + image/video/music/TTS/STT + Fusion router). These document how OpenClaw connects to and configures each LLM/media provider — the provider/model layer the CLI (`cli/models`, `cli/configure`), gateway config, and concepts (`concepts/model-providers`, `concepts/models`) reference. **Priority P2** (Phase B — features/integration). The code-side counterparts `repo_openclaw_extensions_llm_providers` and `repo_openclaw_agents` (model catalog/auth) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 15,177 measured words. **Planned: 11 notes** (2 pages split 3-way; 5 reference pages = 1 note each).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/providers/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| NVIDIA | providers/nvidia | 888 | 6 | 7 | 0 | procedure |
| Ollama | providers/ollama | 5,456 | 57 | 11 | 2 | procedure (split: setup/discovery · vision · advanced/troubleshoot) |
| Ollama Cloud | providers/ollama-cloud | 526 | 4 | 7 | 0 | procedure |
| OpenAI | providers/openai | 5,602 | 39 | 13 | 5 | procedure (split: auth/runtime · media · advanced) |
| OpenCode | providers/opencode | 484 | 9 | 5 | 2 | procedure |
| OpenCode Go | providers/opencode-go | 472 | 6 | 4 | 0 | procedure |
| OpenRouter | providers/openrouter | 1,749 | 17 | 12 | 0 | procedure |

Total: **15,177 words**, ~138 code fences. (Fence counts = grep `^```` lines / 2.)

## Content Strategy

- **Prioritize**: provider auth + model-ref resolution (every run depends on which provider/key/route is selected), and the two large multi-capability pages (Ollama, OpenAI) whose setup, vision/media, and advanced-tuning clusters are independently load-bearing.
- **Split (word-cap + mixed-task-cluster)**: `ollama.md` (5,456w) → 3 notes (setup+discovery procedure · vision/image-understanding procedure · advanced-config+troubleshooting procedure); `openai.md` (5,602w) → 3 notes (auth+Codex-runtime procedure · image/video/voice media procedure · advanced transport/compaction/Azure procedure). Both far exceed the 2,500w cap and bundle distinct task clusters.
- **Link-out, do not duplicate**: provider env vars / config schema → gateway config sub-plans (gw01/gw02); the shared `image_generate` / `video_generate` / `music_generate` / `tts` / web-search tool surfaces → tools sub-plans (to04/to05/to06/to08); failover/model-ref concepts → concepts sub-plans (co04); model names (Kimi, GLM, MiniMax, GPT-5, Nemotron, Sora) are documented as catalog config, NOT promoted to term notes (link `term_llm`, `term_qwen`, `term_deepseek`, `term_nemotron`, `term_claude`, `term_multimodal`). OpenCode Go's catalog is the Go half of the OpenCode page; kept as a small standalone note that points back at the OpenCode note (mirrors the source's parent/child relationship).

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_providers_nvidia.md` | procedure | nvidia.md: all (Getting started, Config example, Featured catalog, Nemotron 3 Ultra, Bundled fallback catalog, Advanced configuration) | 480 | Configuring NVIDIA's free OpenAI-compatible API in OpenClaw: `NVIDIA_API_KEY` onboarding, default Nemotron 3 Ultra, the live featured-model catalog + bundled fallback, and reasoning/timeout advanced params. |
| 2 | `oc_providers_ollama_setup.md` | procedure | ollama.md: intro, Auth rules, Getting started, Cloud models, Model discovery (implicit provider), Configuration | 720 | Setting up Ollama in OpenClaw: native `/api/chat` vs the forbidden `/v1` route, auth rules (local marker vs cloud key), the three modes (cloud+local / cloud-only / local-only), onboarding/manual setup, and implicit auto-discovery from `/api/tags`. |
| 3 | `oc_providers_ollama_vision.md` | procedure | ollama.md: Vision and image description | 430 | Routing image understanding through local/hosted Ollama vision models: marking models image-capable (`input: ["text","image"]`), `infer image describe`, `agents.defaults.imageModel`, and `num_ctx`/timeout caps for constrained hardware. |
| 4 | `oc_providers_ollama_advanced.md` | procedure | ollama.md: Common recipes, Model selection, Quick verification, Ollama Web Search, Advanced configuration, Troubleshooting | 740 | Advanced Ollama operation: common config recipes (LAN host, cloud-only, multi-host, lean local profile), context-window/thinking/embeddings tuning, Ollama Web Search, and troubleshooting (WSL2 crash loop, tool-JSON-as-text, cold-model timeouts). |
| 5 | `oc_providers_ollama_cloud.md` | procedure | ollama-cloud.md: all (Setup, Defaults, When to choose, Models, Live test, Troubleshooting) | 420 | Using the dedicated `ollama-cloud` provider id for cloud-only routing: `OLLAMA_API_KEY` setup against `https://ollama.com`, native `/api/chat` style, live-catalog model discovery, and when to pick it over the local `ollama` provider. |
| 6 | `oc_providers_openai_auth.md` | procedure | openai.md: intro, Quick choice, Naming map, OpenClaw feature coverage, Memory embeddings, Getting started (API key + Codex subscription tabs), Native Codex app-server auth | 760 | Authenticating and routing OpenAI in OpenClaw: the single `openai` provider id over Codex-runtime agent turns vs direct API-key, the provider/runtime/auth naming map, `auth.order.openai`, device-code OAuth, context-window caps, and memory embeddings. |
| 7 | `oc_providers_openai_media.md` | procedure | openai.md: Image generation, Video generation, GPT-5 prompt contribution, Voice and speech (TTS, STT, realtime transcription, realtime voice) | 720 | OpenAI media capabilities in OpenClaw: image generation (`gpt-image-2`, transparent-background path), video (`sora-2`), the GPT-5 prompt-contribution overlay, and voice/speech (TTS voices, batch + realtime STT, Realtime voice billing caveats). |
| 8 | `oc_providers_openai_advanced.md` | procedure | openai.md: Azure OpenAI endpoints, Advanced configuration (Transport, Fast mode, service_tier, server-side compaction, strict-agentic, native vs compatible routes) | 700 | Advanced OpenAI tuning: Azure OpenAI image endpoints (deployment-name rule, api-version, regions), WebSocket/SSE transport, fast-mode/`service_tier` priority, Responses server-side compaction, strict-agentic GPT mode, and native-vs-proxy request shaping. |
| 9 | `oc_providers_opencode.md` | procedure | opencode.md: all (intro, Getting started Zen/Go, Config example, Built-in catalogs, Advanced configuration) | 470 | Using OpenCode's two hosted catalogs (Zen `opencode/*`, Go `opencode-go/*`) in OpenClaw: shared `OPENCODE_API_KEY`, per-catalog onboarding, the runtime provider split, and Gemini/non-Gemini replay behavior. |
| 10 | `oc_providers_opencode_go.md` | procedure | opencode-go.md: all (intro, Built-in catalog, Getting started, Config example, Advanced configuration) | 420 | The OpenCode Go catalog (`opencode-go/*`): the bundled Go model lineup (GLM, Kimi, DeepSeek, MiMo, MiniMax, Qwen), shared-key setup with OpenCode, and the runtime-ref convention that keeps Zen/Go routing distinct. |
| 11 | `oc_providers_openrouter.md` | procedure | openrouter.md: all (Getting started OAuth/API-key, Config example, Model references, Image/Video/Music/TTS/STT generation, Fusion router, Authentication and headers, Advanced configuration) | 800 | Using OpenRouter's unified aggregator API in OpenClaw: PKCE-OAuth vs API-key onboarding, `openrouter/<provider>/<model>` refs, image/video/music/TTS/STT backing, the Fusion parallel-panel router, app-attribution headers, response caching, and provider-routing metadata. |

## Section Coverage Map

```
nvidia.md
├── (intro: OpenAI-compatible API, Nemotron default) ── → note 1 (oc_providers_nvidia)
├── Getting started ─────────────────────────────────── → note 1
├── Config example ──────────────────────────────────── → note 1
├── Featured catalog ────────────────────────────────── → note 1
├── Nemotron 3 Ultra ────────────────────────────────── → note 1
├── Bundled fallback catalog ────────────────────────── → note 1
├── Advanced configuration (auto-enable, catalog/pricing,
│   OpenAI-compatible endpoint, Ultra reasoning params,
│   slow custom provider) ──────────────────────────── → note 1
└── Related ─────────────────────────────────────────── → note 1 (Related Notes / References)
ollama.md
├── (intro: 3 modes, ollama-cloud pointer, /v1 warning) → note 2 (oc_providers_ollama_setup)
├── Auth rules (local/LAN, remote/cloud, custom ids,
│   auth profiles, memory embedding scope) ──────────── → note 2
├── Getting started (onboarding, manual setup) ──────── → note 2
├── Cloud models (cloud+local, cloud-only, local-only) → note 2
├── Model discovery (implicit provider) ─────────────── → note 2
├── Configuration (basic, explicit, custom base URL) ── → note 2
├── Vision and image description ─────────────────────── → note 3 (oc_providers_ollama_vision)
├── Common recipes ──────────────────────────────────── → note 4 (oc_providers_ollama_advanced)
├── Model selection (H3) ────────────────────────────── → note 4
├── Quick verification (H3) ─────────────────────────── → note 4
├── Ollama Web Search ───────────────────────────────── → note 4 (→ to05 ollama-search)
├── Advanced configuration (legacy OpenAI-compat,
│   context windows, thinking, reasoning, costs,
│   memory embeddings, streaming) ──────────────────── → note 4
├── Troubleshooting (WSL2, not detected, no models,
│   connection refused, curl-vs-OpenClaw, tool-JSON,
│   Kimi/GLM garble, cold timeout, large-context) ──── → note 4
└── Related ─────────────────────────────────────────── → notes 2–4 (Related Notes / References)
ollama-cloud.md
├── (intro: ollama-cloud provider id, native /api/chat) → note 5 (oc_providers_ollama_cloud)
├── Setup ───────────────────────────────────────────── → note 5
├── Defaults ────────────────────────────────────────── → note 5
├── When to choose Ollama Cloud ─────────────────────── → note 5
├── Models ──────────────────────────────────────────── → note 5
├── Live test ───────────────────────────────────────── → note 5
├── Troubleshooting ─────────────────────────────────── → note 5
└── Related ─────────────────────────────────────────── → note 5 (Related Notes / References)
openai.md
├── (intro: one provider id, agent vs non-agent) ────── → note 6 (oc_providers_openai_auth)
├── Quick choice ────────────────────────────────────── → note 6
├── Naming map ──────────────────────────────────────── → note 6
├── OpenClaw feature coverage ───────────────────────── → note 6
├── Memory embeddings ───────────────────────────────── → note 6
├── Getting started (API key tab, Codex subscription tab,
│   route summaries, context-window cap, catalog recovery) → note 6
├── Native Codex app-server auth ────────────────────── → note 6
├── Image generation ────────────────────────────────── → note 7 (oc_providers_openai_media)
├── Video generation ────────────────────────────────── → note 7
├── GPT-5 prompt contribution ───────────────────────── → note 7
├── Voice and speech (TTS, STT, realtime transcription,
│   realtime voice) ───────────────────────────────── → note 7
├── Azure OpenAI endpoints (Configuration, API version,
│   deployment names, regions, parameter differences) ─ → note 8 (oc_providers_openai_advanced)
├── Advanced configuration (Transport, Fast mode,
│   service_tier, server-side compaction, strict-agentic,
│   native vs OpenAI-compatible routes) ────────────── → note 8
└── Related ─────────────────────────────────────────── → notes 6–8 (Related Notes / References)
opencode.md
├── (intro: Zen + Go catalogs table) ────────────────── → note 9 (oc_providers_opencode)
├── Getting started (Zen tab, Go tab) ───────────────── → note 9
├── Config example ──────────────────────────────────── → note 9
├── Built-in catalogs (Zen H3, Go H3) ───────────────── → note 9
├── Advanced configuration (key aliases, shared creds,
│   billing, Gemini/non-Gemini replay) ─────────────── → note 9
└── Related ─────────────────────────────────────────── → note 9 (Related Notes / References)
opencode-go.md
├── (intro: Go catalog within OpenCode) ─────────────── → note 10 (oc_providers_opencode_go)
├── Built-in catalog (model table) ──────────────────── → note 10
├── Getting started (interactive, non-interactive) ──── → note 10
├── Config example ──────────────────────────────────── → note 10
├── Advanced configuration (routing, ref convention,
│   shared credentials) ───────────────────────────── → note 10
└── Related ─────────────────────────────────────────── → note 10 (Related Notes / References)
openrouter.md
├── (intro: unified API, OpenAI-compatible) ─────────── → note 11 (oc_providers_openrouter)
├── Getting started (OAuth, API key) ────────────────── → note 11
├── Config example ──────────────────────────────────── → note 11
├── Model references ─────────────────────────────────── → note 11
├── Image generation ────────────────────────────────── → note 11
├── Video generation ────────────────────────────────── → note 11
├── Music generation ────────────────────────────────── → note 11
├── Text-to-speech ──────────────────────────────────── → note 11
├── Speech-to-text (inbound audio) ──────────────────── → note 11
├── Fusion router ───────────────────────────────────── → note 11
├── Authentication and headers ──────────────────────── → note 11
├── Advanced configuration (response caching, Anthropic
│   cache markers, reasoning prefill, thinking injection,
│   DeepSeek V4 replay, OpenAI-only shaping, Gemini routes,
│   provider routing metadata) ─────────────────────── → note 11
└── Related ─────────────────────────────────────────── → note 11 (Related Notes / References)
```
No orphaned sections. Shared media/web-search tool surfaces (image/video/music/tts/web), gateway config schema, and failover/model-ref concepts are LINKED to their home sub-plans (to0x / gw0x / co0x), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| ollama.md (5,456w, 11 H2 / 2 H3, 57 fences) | notes 2 + 3 + 4 | >2× the 2,500w cap and bundles three distinct task clusters: (a) setup/auth/mode-selection/discovery, (b) vision/image-understanding, (c) advanced-tuning + troubleshooting. Each cluster is independently load-bearing and keeps each note ≤740w / ≤6 code. |
| openai.md (5,602w, 13 H2 / 5 H3, 39 fences) | notes 6 + 7 + 8 | >2× the cap; mixes (a) auth + Codex-runtime routing, (b) media generation (image/video/voice), and (c) advanced transport/compaction/Azure tuning. Split per word-cap + distinct-task-cluster rules; keeps each ≤760w / ≤6 code. |

All other pages (nvidia 888w, ollama-cloud 526w, opencode 484w, opencode-go 472w, openrouter 1,749w) are single-BB and ≤2,500w → 1 note each (openrouter is content-dense at 1,749w but a single coherent aggregator procedure; kept as 1 note with selective code reproduction to stay ≤6 fences).

## Summary Statistics & Building Block Distribution

- Source pages: **7** (15,177 words). New `oc_` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×11** (all 11 notes — provider setup/config/auth/media are operational how-tos).
- Est. digest words: ~6,660 (avg ~605/note; range 420–800). ~138 source code fences distribute across the 11 notes; each note kept ≤6 by reproducing only the canonical config snippet(s) per section verbatim and link-pointing repeated variants.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_providers_nvidia (8t · 10s · 10d)
**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model abstraction; relevance: NVIDIA serves open LLMs (Nemotron, Kimi, GLM) through OpenClaw.
- [Nemotron](../../term_dictionary/term_nemotron.md) — NVIDIA's Nemotron reasoning model family; relevance: Nemotron 3 Ultra 550B is the bundled NVIDIA default.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible request/response contract; relevance: NVIDIA exposes the standard `/v1` `openai-completions` endpoint OpenClaw targets.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — explicit reasoning trace; relevance: Ultra's `enable_thinking`/`reasoning_budget` template params control reasoning output.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted model APIs; relevance: NVIDIA's free hosted API is one such third-party provider.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — enumerable provider model list; relevance: the live featured-model catalog + bundled fallback catalog are the two NVIDIA catalogs.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool-call protocol; relevance: NVIDIA agent turns make tool calls over OpenAI-completions.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: Ultra advertises a 1M-token context with 16,384 max output.
**Docs**
- [hermes_run_nemotron_3_ultra_free](../hermes_agent/hermes_run_nemotron_3_ultra_free.md) — Hermes guide to running Nemotron 3 Ultra free via NVIDIA; relevance: the exact same NVIDIA-free-API + Nemotron default in a sibling coding agent.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider catalog; relevance: NVIDIA is a cloud OpenAI-compatible provider in the same class.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — registering a new inference provider; relevance: parallels NVIDIA's `baseUrl`+`api: openai-completions` registration.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider/model routing rules; relevance: NVIDIA model-ref resolution and default selection.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — OpenAI-compatible base-URL gateway config; relevance: NVIDIA uses an OpenAI-compatible base URL just like a gateway endpoint.
- [cc_model_selection](../claude_code/cc_model_selection.md) — choosing/setting the active model; relevance: `openclaw models set nvidia/...` mirrors model-selection config.
- [pi_custom_models](../pi/pi_custom_models.md) — custom OpenAI-compatible model entry; relevance: the slow-custom-provider NVIDIA entry is a custom model definition.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering a custom provider; relevance: NVIDIA custom provider (`custom-integrate-api-nvidia-com`) registration.
- [oc_providers_openrouter](oc_providers_openrouter.md) — OpenRouter aggregator (planned, this series); relevance: the other bundled OpenAI-compatible aggregator provider.
- [oc_providers_opencode](oc_providers_opencode.md) — OpenCode catalogs (planned, this series); relevance: peer hosted-catalog provider with a bundled fallback catalog.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension package; relevance: implements the NVIDIA provider plugin.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent/model-catalog runtime; relevance: model catalog + featured-catalog fetch live here.
**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — openai-completions provider implementation; relevance: NVIDIA reuses the openai-completions provider path.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planning; relevance: builds the bundled fallback catalog NVIDIA falls back to.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — normalize discovered catalog rows; relevance: normalizes NVIDIA's live featured-model feed.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalization; relevance: shapes the featured-models.json into OpenClaw model rows.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent-side model catalog assembly; relevance: surfaces NVIDIA models in setup/model-selection.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing/alias lookup; relevance: NVIDIA models default cost 0 and need alias resolution.
- [snippet_hermes_agent_cli_model_catalog](../../code_snippets/snippet_hermes_agent_cli_model_catalog.md) — Hermes model catalog CLI; relevance: parallel featured-catalog fetch + cache pattern.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: registers OpenAI-compatible providers like NVIDIA.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: bundled fallback catalog feeds failover.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env-var wiring; relevance: `NVIDIA_API_KEY` auto-enables the provider from env.

### oc_providers_ollama_setup (8t · 10s · 10d)
**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Ollama serves local + cloud LLMs to OpenClaw.
- [Qwen](../../term_dictionary/term_qwen.md) — Qwen model family; relevance: `qwen3.5:9b`/`qwen3:32b` are common local Ollama models.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model list; relevance: implicit auto-discovery builds the catalog from `/api/tags`.
- [Authentication](../../term_dictionary/term_authentication.md) — credential resolution; relevance: local `ollama-local` marker vs real `OLLAMA_API_KEY` cloud key.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls; relevance: native `/api/chat` supports tool calling whereas the `/v1` route breaks it.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted model APIs; relevance: Ollama Cloud (`https://ollama.com`) is the hosted third-party surface.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider integration; relevance: the bundled Ollama plugin registers the `ollama` + `ollama-cloud` provider ids.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: `num_ctx`/`contextWindow` budgets are configured per Ollama model.
**Docs**
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — local Ollama provider setup in Hermes; relevance: same native-API-vs-`/v1` and local-host setup model.
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — self-hosted LLM guide; relevance: the local-only Ollama mode is a self-hosted LLM.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: Ollama's cloud + hybrid modes.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider/auth env vars; relevance: `OLLAMA_API_KEY` env-var auth convention.
- [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: `openclaw models set ollama/<model>` config.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — OpenAI-compatible gateway; relevance: the legacy `/v1` Ollama route is the OpenAI-compatible gateway shape (and the trap this note warns against).
- [pi_custom_models](../pi/pi_custom_models.md) — local Ollama/vLLM/LM Studio config; relevance: explicit-config Ollama model definitions.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth resolution; relevance: local-marker vs real-key auth rules.
- [oc_providers_ollama_cloud](oc_providers_ollama_cloud.md) — dedicated cloud provider (planned, this series); relevance: the `ollama-cloud` first-class id this page points to.
- [oc_providers_ollama_advanced](oc_providers_ollama_advanced.md) — advanced Ollama config (planned, this series); relevance: recipes/tuning/troubleshooting continuation.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension package; relevance: implements the Ollama plugin.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent/model-catalog runtime; relevance: model discovery + selection.
**Snippets**
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider implementation; relevance: the native `/api/chat` local provider path.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — normalize discovered models; relevance: `/api/tags` auto-discovery normalization.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalization; relevance: `/api/show` capability detection (vision/tools/thinking).
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: implicit Ollama provider catalog.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — Hermes Ollama-cloud provider plugin; relevance: parallel native Ollama provider registration.
- [snippet_hermes_agent_core_agent_init_memory_ollama](../../code_snippets/snippet_hermes_agent_core_agent_init_memory_ollama.md) — Ollama init in Hermes; relevance: local Ollama host init + auth marker.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: registers Ollama with native API style.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env wiring; relevance: `OLLAMA_API_KEY` env resolution.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential ordering; relevance: `auth-profiles.json` Ollama credential storage.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: local-marker vs bearer-key resolution for Ollama hosts.

### oc_providers_ollama_vision (8t · 10s · 10d)
**Terms**
- [Multimodal](../../term_dictionary/term_multimodal.md) — text+image (multimodal) input; relevance: vision models accept `input: ["text","image"]`.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: vision-capable Ollama LLMs (`qwen2.5vl`) handle image understanding.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider; relevance: the Ollama plugin registers Ollama as an image-capable media-understanding provider.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: cap `num_ctx` so constrained hardware does not crash on full vision context.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation; relevance: the explicit `image` tool the agent can call during a turn.
- [Qwen](../../term_dictionary/term_qwen.md) — Qwen model family; relevance: `qwen2.5vl:7b` is the documented Ollama vision model.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted model APIs; relevance: hosted Ollama vision models route through the same flow.
- [RAG](../../term_dictionary/term_rag.md) — retrieval/media preflight; relevance: inbound image understanding feeds the media-understanding preflight surface.
**Docs**
- [hermes_vision_image_paste](../hermes_agent/hermes_vision_image_paste.md) — vision/image-paste handling; relevance: same image-understanding routing into a model.
- [hermes_image_generation](../hermes_agent/hermes_image_generation.md) — image capabilities; relevance: sibling image media surface (understanding vs generation contrast).
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — local Ollama provider; relevance: marking local Ollama models image-capable.
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tool reference; relevance: `infer image describe` and the image tool surface.
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — self-hosted LLM; relevance: local vision models on constrained hardware.
- [cc_context_window_anatomy](../claude_code/cc_context_window_anatomy.md) — context-window anatomy; relevance: `num_ctx` capping for vision context budget.
- [pi_custom_models](../pi/pi_custom_models.md) — custom model entries; relevance: marking a model `input: ["text","image"]` manually.
- [oc_providers_ollama_setup](oc_providers_ollama_setup.md) — Ollama setup (planned, this series); relevance: prerequisite provider setup/discovery.
- [oc_providers_ollama_advanced](oc_providers_ollama_advanced.md) — advanced Ollama (planned, this series); relevance: timeout/`num_ctx` tuning continuation.
- [oc_providers_openai_media](oc_providers_openai_media.md) — OpenAI media (planned, this series); relevance: the OpenAI image-understanding/generation counterpart.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension package; relevance: implements the image-capable Ollama provider.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway media pipeline; relevance: routes inbound image media to the vision model.
**Snippets**
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — chat media pipeline; relevance: inbound image injection into the prompt.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: preflights image files before sending to Ollama vision.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed image lifecycle; relevance: lifecycle of image records routed to vision.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: the provider that serves vision models.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — capability schema normalization; relevance: detects the `vision` capability from `/api/show`.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image tool; relevance: parallel image tool surface.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen dispatch; relevance: image-capability provider dispatch pattern.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — Hermes Ollama provider; relevance: registering the Ollama media-understanding provider.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — discovery normalization; relevance: discovers image-capable models.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — media stream handling; relevance: shared media-input plumbing for non-text inputs.

### oc_providers_ollama_advanced (9t · 10s · 10d)
**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: advanced tuning of Ollama LLM behavior.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: `num_ctx`, `contextWindow`, `contextTokens` tuning recipes.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning trace; relevance: `/think` thinking-control levels for reasoning models.
- [Embedding](../../term_dictionary/term_embedding.md) — vector embeddings; relevance: memory embeddings via Ollama `/api/embed` (`nomic-embed-text`).
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation / web search; relevance: memory search + Ollama Web Search retrieval (the `web_search` surface owned by tools to05).
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls; relevance: tool schemas + `compat.supportsTools:false` for weak local models.
- [Model Failover](../../term_dictionary/term_model_failover.md) — fallback model ladder; relevance: primary/fallback recipes (`fallbacks: [...]`).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — OpenAI-compat proxy mode; relevance: the legacy `/v1` `openai-completions` proxy mode for Ollama behind a proxy.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model list; relevance: multi-host custom-provider catalogs and selection.
**Docs**
- [hermes_context_compression_caching](../hermes_agent/hermes_context_compression_caching.md) — context compression/caching; relevance: context-window tuning + thinking budgets.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — provider/model fallbacks; relevance: Ollama primary/fallback ladders.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory provider catalog; relevance: Ollama as a memory embedding provider.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — proxy routing; relevance: OpenAI-compat proxy mode + multi-host routing.
- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — web-search provider; relevance: Ollama Web Search as a `web_search` provider.
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — effort/thinking levels; relevance: `/think low|medium|high|max` mapping.
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — reducing token usage; relevance: lowering `contextWindow`/`maxTokens` for slow large-context models.
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — fallback model config; relevance: the fallback recipe pattern.
- [oc_providers_ollama_setup](oc_providers_ollama_setup.md) — Ollama setup (planned, this series); relevance: prerequisite auth/discovery base.
- [oc_providers_ollama_cloud](oc_providers_ollama_cloud.md) — Ollama Cloud (planned, this series); relevance: cloud-only recipe variant.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension package; relevance: implements Ollama tuning/compat behavior.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: Ollama memory-embedding provider lives here.
**Snippets**
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — fallback ladder; relevance: Ollama primary/fallback config.
- [snippet_openclaw_gateway_session_utils_model_fallback](../../code_snippets/snippet_openclaw_gateway_session_utils_model_fallback.md) — session model fallback; relevance: runtime fallback when an Ollama host is unreachable.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — fallback cooldown; relevance: cold-model timeout + degrade behavior.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — memory embedding inputs; relevance: query/document embedding prefixes for `nomic-embed-text`.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — host embeddings; relevance: `/api/embed` batching for Ollama memory embeddings.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search; relevance: selecting Ollama as the `memorySearch` provider.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — schema normalization; relevance: thinking/reasoning capability detection.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: native `/api/chat` vs legacy `/v1` request shaping.
- [snippet_hermes_agent_tools_memory](../../code_snippets/snippet_hermes_agent_tools_memory.md) — memory tool; relevance: memory search over embedded chunks.
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — usage/cost summary; relevance: Ollama costs default to 0 (free/local).

### oc_providers_ollama_cloud (8t · 10s · 10d)
**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: hosted Ollama LLMs served cloud-only.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model list; relevance: live hosted-catalog discovery (`models list --provider ollama-cloud`).
- [Authentication](../../term_dictionary/term_authentication.md) — credential resolution; relevance: a real `OLLAMA_API_KEY` cloud key vs the local `ollama-local` marker.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored API credential; relevance: the cloud API key stored against `https://ollama.com`.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted model APIs; relevance: Ollama Cloud is the hosted third-party surface.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls; relevance: native `/api/chat` style (not `/v1`) preserves tool calling.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider; relevance: `ollama-cloud` is a first-class registered provider id.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — base-URL routing; relevance: cloud-only routing pinned to `https://ollama.com` without local host mixing.
**Docs**
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: cloud-only hosted Ollama routing.
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — local vs cloud Ollama; relevance: when to choose cloud over local provider.
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth env vars; relevance: `OLLAMA_API_KEY` cloud-key convention.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider routing; relevance: keeping `ollama-cloud` routing separate from local `ollama`.
- [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: `openclaw models set ollama-cloud/<model>`.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud-hosted provider config; relevance: configuring a cloud-only hosted provider.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth; relevance: real-key requirement for hosted endpoints.
- [oc_providers_ollama_setup](oc_providers_ollama_setup.md) — Ollama setup (planned, this series); relevance: the local/hybrid provider this page contrasts with.
- [oc_providers_ollama_advanced](oc_providers_ollama_advanced.md) — advanced Ollama (planned, this series); relevance: shared embeddings/web-search caveats.
- [oc_providers_openrouter](oc_providers_openrouter.md) — OpenRouter (planned, this series); relevance: alternative when `/v1` semantics are needed instead.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension package; relevance: implements the `ollama-cloud` provider id.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — model-catalog runtime; relevance: live hosted-catalog discovery + selection.
**Snippets**
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — Ollama provider implementation; relevance: the native `/api/chat` provider repointed at `https://ollama.com`.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — discovery normalization; relevance: live hosted-catalog model ids vs local pull names.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — schema normalization; relevance: hosted model metadata shaping.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: the `ollama-cloud` catalog assembly.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — Hermes Ollama-cloud plugin; relevance: the direct cloud-only provider analog.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env wiring; relevance: `OLLAMA_API_KEY` cloud-key resolution.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential; relevance: cloud-key credential storage.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: real-key (not local-marker) enforcement for cloud.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: registering a separate hosted provider id.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: resolving hosted model ids/aliases.

### oc_providers_openai_auth (10t · 11s · 10d)
**Terms**
- [OAuth](../../term_dictionary/term_oauth.md) — OAuth authorization; relevance: Codex/ChatGPT subscription sign-in via OAuth.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored access/refresh token; relevance: device-code OAuth stores access/refresh tokens in the agent auth store.
- [Authentication](../../term_dictionary/term_authentication.md) — credential resolution; relevance: subscription vs direct API-key auth shapes for one `openai` id.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — named credential profile; relevance: `auth.order.openai`, `openai:*` ordered profiles, multi-login profile ids.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: routing OpenAI GPT-5 agent turns.
- [Claude](../../term_dictionary/term_claude.md) — Claude/Anthropic models; relevance: comparable subscription-vs-key auth model in the sibling provider.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — agent execution harness; relevance: the native Codex app-server harness runs OpenAI agent turns.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: native `contextWindow` 1M vs default runtime `contextTokens` 272K cap.
- [Embedding](../../term_dictionary/term_embedding.md) — vector embeddings; relevance: OpenAI `text-embedding-3-small` memory embeddings.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Claude Code CLI; relevance: sibling coding-agent tool with the same subscription-vs-key auth split.
**Docs**
- [hermes_codex_runtime_setup](../hermes_agent/hermes_codex_runtime_setup.md) — Codex runtime setup; relevance: the native Codex app-server harness setup analog.
- [hermes_codex_runtime_tools](../hermes_agent/hermes_codex_runtime_tools.md) — Codex runtime tools; relevance: Codex app-server thread/tool controls (`/codex ...`).
- [hermes_oauth_over_ssh](../hermes_agent/hermes_oauth_over_ssh.md) — OAuth on headless hosts; relevance: device-code OAuth for callback-hostile setups.
- [hermes_subscription_proxy](../hermes_agent/hermes_subscription_proxy.md) — subscription proxy auth; relevance: subscription-vs-API-key routing.
- [hermes_credential_pools](../hermes_agent/hermes_credential_pools.md) — credential pools/rotation; relevance: rotating to the next ordered `openai:*` profile on usage limits.
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code authentication; relevance: subscription-vs-API-key auth in the sibling tool.
- [cc_login_authentication_troubleshooting](../claude_code/cc_login_authentication_troubleshooting.md) — login auth troubleshooting; relevance: recovering OAuth routing (`doctor --fix`, re-login).
- [cc_agent_sdk_install_and_auth](../claude_code/cc_agent_sdk_install_and_auth.md) — SDK install + auth; relevance: agent-runtime auth selection.
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth resolution order; relevance: subscription-vs-key resolution + `auth.order`.
- [oc_providers_openai_media](oc_providers_openai_media.md) — OpenAI media (planned, this series); relevance: media surfaces gated on Platform credits vs Codex auth.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension package; relevance: implements the OpenAI provider + Codex plugin.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime + auth profiles; relevance: `auth.order.openai` profile ordering + rotation.
**Snippets**
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile ordering + credential; relevance: `auth.order.openai` profile ordering and credential selection.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: storing/migrating Codex OAuth credentials.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profiles; relevance: app-server's existing Codex CLI ChatGPT sign-in fallback.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: subscription/API-key/env auth-mode resolution.
- [snippet_openclaw_gateway_auth_authorize_dispatch](../../code_snippets/snippet_openclaw_gateway_auth_authorize_dispatch.md) — authorize dispatch; relevance: device-code/OAuth authorize flow.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — credential/secret handling; relevance: keeping `CODEX_API_KEY`/`OPENAI_API_KEY` out of spawned children.
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — Hermes Codex provider; relevance: native Codex runtime + auth analog.
- [snippet_hermes_agent_core_anthropic_adapter_oauth](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_oauth.md) — adapter OAuth; relevance: subscription-OAuth-vs-key adapter pattern.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: catalog recovery synthesizing the `gpt-5.5` OAuth row.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — embedding inputs; relevance: OpenAI memory embeddings (`text-embedding-3-small`, asymmetric input types).
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — CLI auth login/logout; relevance: `models auth login --provider openai` analog.

### oc_providers_openai_media (8t · 11s · 11d)
**Terms**
- [Multimodal](../../term_dictionary/term_multimodal.md) — multimodal generation; relevance: image (`gpt-image-2`) and video (`sora-2`) generation + vision.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — TTS synthesis; relevance: `messages.tts` OpenAI voices/models (`gpt-4o-mini-tts`).
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — STT transcription; relevance: batch (`gpt-4o-transcribe`) + realtime STT.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: Realtime API uses `wss://api.openai.com/v1/realtime`.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: GPT-5 family + the GPT-5 prompt-contribution overlay.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider; relevance: the bundled `openai` plugin registers image/video/TTS/STT/realtime.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls; relevance: `image_generate`/`video_generate` tools the agent calls.
- [RAG](../../term_dictionary/term_rag.md) — media preflight pipeline; relevance: inbound audio/STT flows through media-understanding preflight.
**Docs**
- [hermes_image_generation](../hermes_agent/hermes_image_generation.md) — image generation; relevance: OpenAI image-generation surface analog.
- [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-gen provider plugin; relevance: how an image provider registers the `image_generate` tool.
- [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-gen provider plugin; relevance: `sora-2` video-generation registration analog.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — TTS providers; relevance: OpenAI TTS voices/models config.
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — STT transcription; relevance: batch + realtime speech-to-text.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice mode guide; relevance: realtime voice over a WebSocket session.
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tools; relevance: the image/video/audio tool surface.
- [cc_context_cost_by_feature](../claude_code/cc_context_cost_by_feature.md) — per-feature cost; relevance: Realtime voice billed against Platform credits, not subscription.
- [oc_providers_openai_auth](oc_providers_openai_auth.md) — OpenAI auth (planned, this series); relevance: media surfaces require Platform-credit auth distinct from Codex OAuth.
- [oc_providers_ollama_vision](oc_providers_ollama_vision.md) — Ollama vision (planned, this series); relevance: the local image-understanding counterpart.
- [oc_providers_openrouter](oc_providers_openrouter.md) — OpenRouter media (planned, this series); relevance: alternative image/video/music/TTS/STT backing.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension package; relevance: implements the OpenAI media plugin surfaces.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — apps incl. Control UI Talk; relevance: Control UI Talk realtime voice (`talk.realtime.provider: "openai"`).
**Snippets**
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — talk transcription relay; relevance: Control UI Talk realtime transcription relay.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed image lifecycle; relevance: lifecycle of `image_generate` outputs.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: preflight for generated/edited images.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — chat media pipeline; relevance: media output delivered to channels.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — voice-call STT stream; relevance: realtime transcription path for Voice Call.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call audio stream; relevance: G.711 u-law realtime audio plumbing.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-call manager; relevance: realtime voice session management.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-gen tool; relevance: `video_generate` (`sora-2`) tool analog.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: routing TTS to an OpenAI provider.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription; relevance: batch STT transcription analog.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-gen tool; relevance: `image_generate` (`gpt-image-2`) tool analog.

### oc_providers_openai_advanced (9t · 11s · 10d)
**Terms**
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex transport; relevance: WebSocket-first transport (`"auto"`) for `openai/*`.
- [SSE](../../term_dictionary/term_sse.md) — server-sent events; relevance: SSE fallback during WebSocket cool-down.
- [Compaction](../../term_dictionary/term_compaction.md) — context compaction; relevance: Responses server-side compaction (`context_management`, `compact_threshold`).
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — prompt-cache reuse; relevance: native prompt-cache hints + `store: true`.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — proxy routing; relevance: native vs OpenAI-compatible `/v1` proxy request shaping.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: 70%-of-`contextWindow` default compact threshold.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool calls; relevance: strict tool schemas on native routes.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — Responses contract; relevance: server-side compaction is a Responses-API feature.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — endpoint gateway; relevance: Azure OpenAI deployment-scoped endpoints + api-version routing.
**Docs**
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — proxy routing; relevance: native vs proxy request shaping.
- [hermes_provider_azure_foundry_setup](../hermes_agent/hermes_provider_azure_foundry_setup.md) — Azure Foundry provider setup; relevance: Azure OpenAI endpoints, deployment names, regions.
- [hermes_context_compression_caching](../hermes_agent/hermes_context_compression_caching.md) — compression/caching; relevance: server-side compaction + prompt-cache hints.
- [hermes_provider_runtime](../hermes_agent/hermes_provider_runtime.md) — provider runtime; relevance: transport + service-tier runtime behavior.
- [cc_amazon_bedrock_mantle_endpoint](../claude_code/cc_amazon_bedrock_mantle_endpoint.md) — endpoint/base-URL override; relevance: base-URL override for a non-default (Azure) endpoint.
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway config; relevance: native-vs-proxy route distinction.
- [cc_extended_context_1m](../claude_code/cc_extended_context_1m.md) — extended 1M context; relevance: compact-threshold budgeting on large context.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — model override/compat flags; relevance: per-model transport/compat/`service_tier` tuning.
- [oc_providers_openai_auth](oc_providers_openai_auth.md) — OpenAI auth (planned, this series); relevance: prerequisite provider auth/runtime base.
- [oc_providers_openai_media](oc_providers_openai_media.md) — OpenAI media (planned, this series); relevance: Azure image-generation routing shares the base-URL detection.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension package; relevance: implements OpenAI native/proxy request shaping.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway transport/streaming; relevance: WebSocket/SSE transport + Responses streaming.
**Snippets**
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — OpenAI HTTP/SSE stream; relevance: SSE fallback streaming path.
- [snippet_openclaw_gateway_openresponses_session_sse](../../code_snippets/snippet_openclaw_gateway_openresponses_session_sse.md) — OpenResponses session SSE; relevance: Responses-API SSE session handling.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — OpenAI HTTP message build; relevance: native-vs-proxy request body shaping.
- [snippet_openclaw_gateway_openresponses_tools_usage](../../code_snippets/snippet_openclaw_gateway_openresponses_tools_usage.md) — OpenResponses tools/usage; relevance: strict tool schemas + usage-counter normalization.
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction chunk safety; relevance: server-side compaction threshold/chunking.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction identifier handoff; relevance: `store: true` + Responses compaction continuity.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — prompt-cache sections; relevance: prompt-cache hints on system blocks.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: native OpenAI request/transport implementation.
- [snippet_hermes_agent_core_bedrock_adapter_streaming](../../code_snippets/snippet_hermes_agent_core_bedrock_adapter_streaming.md) — adapter streaming; relevance: native-endpoint streaming-transport pattern.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — session model overrides; relevance: per-model `params` (transport/`service_tier`/fast-mode) overrides.

### oc_providers_opencode (8t · 10s · 10d)
**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: OpenCode hosts Claude/GPT/Gemini/Kimi/GLM LLMs.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model list; relevance: the Zen and Go hosted catalogs.
- [Model Router](../../term_dictionary/term_model_router.md) — model-routing proxy; relevance: Zen is a curated multi-model proxy routing to Claude/GPT/Gemini.
- [Claude](../../term_dictionary/term_claude.md) — Claude/Anthropic models; relevance: Zen `opencode/claude-opus-*` refs.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted model APIs; relevance: OpenCode is a hosted aggregator service.
- [Authentication](../../term_dictionary/term_authentication.md) — credential resolution; relevance: shared `OPENCODE_API_KEY` (+ `OPENCODE_ZEN_API_KEY` alias) for both catalogs.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider; relevance: two runtime provider ids (`opencode`, `opencode-go`) from one setup.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — proxy routing; relevance: Zen is a proxy that routes per-model upstream (incl. Gemini replay path).
**Docs**
- [band_adapter_opencode](../band/band_adapter_opencode.md) — OpenCode adapter; relevance: the same OpenCode hosted-catalog provider in a sibling agent.
- [band_adapter_catalog](../band/band_adapter_catalog.md) — adapter/provider catalog; relevance: OpenCode as a cataloged provider adapter.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: OpenCode is a cloud hosted-catalog provider.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider routing; relevance: keeping Zen/Go runtime ids distinct for upstream routing.
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog reference; relevance: built-in catalog rows + example models.
- [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: `config set agents.defaults.model.primary "opencode/..."`.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — OpenAI-compatible gateway; relevance: OpenCode is an OpenAI-compatible multi-model gateway.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud provider config; relevance: configuring a hosted-catalog cloud provider.
- [oc_providers_opencode_go](oc_providers_opencode_go.md) — OpenCode Go (planned, this series); relevance: the child Go catalog sharing the same key.
- [oc_providers_openrouter](oc_providers_openrouter.md) — OpenRouter (planned, this series); relevance: peer multi-model aggregator/router.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension package; relevance: implements the OpenCode Zen/Go providers.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — model-catalog runtime; relevance: Zen/Go catalog assembly + routing.
**Snippets**
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: the Zen/Go bundled catalogs.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — schema normalization; relevance: normalizes the two catalog schemas.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — discovery normalization; relevance: `models list --provider opencode` discovery.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planner; relevance: bundles OpenCode catalog rows.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: Gemini/non-Gemini replay-policy distinction parallels Anthropic-route handling.
- [snippet_hermes_agent_cli_model_catalog](../../code_snippets/snippet_hermes_agent_cli_model_catalog.md) — Hermes model catalog CLI; relevance: hosted catalog fetch/listing.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: registering split runtime provider ids.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential; relevance: one `OPENCODE_API_KEY` stores creds for both providers.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env wiring; relevance: `OPENCODE_API_KEY`/`OPENCODE_ZEN_API_KEY` resolution.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: resolving `opencode/*` and `opencode-go/*` aliases.

### oc_providers_opencode_go (8t · 10s · 10d)
**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the Go catalog's hosted LLM lineup.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model list; relevance: the bundled Go model lineup (GLM/Kimi/DeepSeek/MiMo/MiniMax/Qwen).
- [Qwen](../../term_dictionary/term_qwen.md) — Qwen model family; relevance: `opencode-go/qwen3.5-plus` / `qwen3.6-plus`.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — DeepSeek model family; relevance: `opencode-go/deepseek-v4-pro` / `deepseek-v4-flash`.
- [Authentication](../../term_dictionary/term_authentication.md) — credential resolution; relevance: shared `OPENCODE_API_KEY` with the Zen catalog.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted model APIs; relevance: OpenCode-hosted Go catalog is a third-party surface.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider; relevance: the `opencode-go` runtime provider id.
- [Context Window](../../term_dictionary/term_context_window.md) — token budget; relevance: GLM-5.2 advertises a 1M-token context / 131K output.
**Docs**
- [band_adapter_opencode](../band/band_adapter_opencode.md) — OpenCode adapter; relevance: OpenCode (incl. Go) as a provider adapter.
- [band_adapter_catalog](../band/band_adapter_catalog.md) — provider/adapter catalog; relevance: cataloged Go model rows.
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog reference; relevance: the Go bundled model rows + refs.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider routing; relevance: the runtime-ref convention keeping `opencode-go/...` routing distinct.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: OpenCode Go is a cloud hosted-catalog provider.
- [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: `config set agents.defaults.model.primary "opencode-go/..."`.
- [cc_restrict_model_selection](../claude_code/cc_restrict_model_selection.md) — restricting model selection; relevance: choosing among the Go catalog refs.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud provider config; relevance: configuring the hosted Go catalog provider.
- [oc_providers_opencode](oc_providers_opencode.md) — OpenCode parent (planned, this series); relevance: the parent page sharing onboarding + key.
- [oc_providers_nvidia](oc_providers_nvidia.md) — NVIDIA (planned, this series); relevance: peer with the same GLM/Kimi/MiniMax model families in its catalog.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension package; relevance: implements the `opencode-go` provider.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — model-catalog runtime; relevance: Go catalog rows from the bundled registry.
**Snippets**
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: the bundled Go model registry.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planner; relevance: sources most Go rows from the bundled registry.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — schema normalization; relevance: shapes Go model rows incl. GLM-5.2 context/output.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — discovery normalization; relevance: `models list --provider opencode-go` discovery.
- [snippet_hermes_agent_cli_model_catalog](../../code_snippets/snippet_hermes_agent_cli_model_catalog.md) — Hermes model catalog CLI; relevance: hosted catalog listing for a Go-style provider.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry; relevance: registers `opencode-go` runtime id.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential; relevance: shared `OPENCODE_API_KEY` credential storage.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env wiring; relevance: `OPENCODE_API_KEY` env resolution.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: resolving `opencode-go/*` model aliases.
- [snippet_openclaw_sessions_model_overrides](../../code_snippets/snippet_openclaw_sessions_model_overrides.md) — session model overrides; relevance: per-session Go model ref selection.

### oc_providers_openrouter (10t · 10s · 11d)
**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: OpenRouter aggregates many upstream LLMs behind one endpoint.
- [Model Router](../../term_dictionary/term_model_router.md) — model-routing layer; relevance: unified routing + the Fusion parallel-panel-and-judge router.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — aggregator gateway; relevance: OpenRouter is an aggregator gateway over many upstream providers.
- [OAuth](../../term_dictionary/term_oauth.md) — OAuth authorization; relevance: PKCE-OAuth onboarding that issues an OpenRouter key.
- [PKCE](../../term_dictionary/term_pkce.md) — Proof Key for Code Exchange; relevance: the OpenRouter sign-in is a PKCE login flow.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — prompt/response cache; relevance: opt-in response caching + Anthropic `cache_control` markers.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — DeepSeek model family; relevance: DeepSeek V4 reasoning-replay + `reasoning_effort` on OpenRouter routes.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning trace; relevance: thinking/reasoning injection mapped to OpenRouter proxy reasoning payloads.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multimodal generation; relevance: OpenRouter backs image/video/music generation + TTS/STT.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted model APIs; relevance: OpenRouter is a third-party aggregator service.
**Docs**
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — provider routing; relevance: `openrouter/<provider>/<model>` refs + provider-routing metadata.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — proxy routing; relevance: OpenRouter is an OpenAI-compatible proxy aggregator.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: OpenRouter as a cloud aggregator provider.
- [hermes_context_compression_caching](../hermes_agent/hermes_context_compression_caching.md) — compression/caching; relevance: response caching + Anthropic cache markers.
- [hermes_image_generation](../hermes_agent/hermes_image_generation.md) — image generation; relevance: OpenRouter backing the `image_generate` tool.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — TTS providers; relevance: OpenRouter `/audio/speech` TTS.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — OpenAI-compatible gateway; relevance: OpenRouter is an OpenAI-compatible unified API.
- [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — LiteLLM gateway; relevance: OpenRouter pricing/routing parallels the LiteLLM aggregator.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — model override/compat; relevance: `openRouterRouting` only/order/sort provider-routing object.
- [oc_providers_openai_advanced](oc_providers_openai_advanced.md) — OpenAI advanced (planned, this series); relevance: OpenAI-only request shaping NOT forwarded through OpenRouter's proxy path.
- [oc_providers_nvidia](oc_providers_nvidia.md) — NVIDIA (planned, this series); relevance: peer OpenAI-compatible provider.
**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider extension package; relevance: implements the OpenRouter aggregator provider.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: model-ref resolution + reasoning injection.
**Snippets**
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator provider; relevance: the core OpenRouter provider implementation.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — OpenRouter/LiteLLM pricing; relevance: OpenRouter model pricing resolution.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — Hermes OpenRouter plugin; relevance: parallel OpenRouter provider registration.
- [snippet_openclaw_agents_system_prompt_cache_sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — prompt-cache sections; relevance: Anthropic `cache_control` markers on system blocks.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env wiring; relevance: `OPENROUTER_API_KEY` env resolution + app-attribution headers.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: PKCE-OAuth result stored as the `openrouter:default` API-key profile.
- [snippet_hermes_agent_cli_auth_spotify_pkce](../../code_snippets/snippet_hermes_agent_cli_auth_spotify_pkce.md) — PKCE auth flow; relevance: the PKCE login-flow pattern OpenRouter OAuth uses.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: OpenRouter runs through the OpenAI-compatible proxy path.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed image lifecycle; relevance: OpenRouter `image_generate`/`video_generate`/`music_generate` outputs.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: `openrouter/auto` automatic routing + provider `allow_fallbacks`.

## Undigested Terms Plan

| Term (from source) | Disposition |
|---|---|
| provider / model provider | Link existing `term_provider_plugin` + `term_llm`; OpenClaw provider mechanics digested in the `oc_providers_*` notes themselves. |
| provider id / runtime provider | Digested as config concept in the notes; link `term_provider_plugin`. No new term. |
| (built-in / featured / bundled) catalog | Link existing `term_model_catalog`. No new term. |
| model ref (`provider/model`) | Digested inline as config; link `term_model_catalog` / `term_model_router`. No new term. |
| auto-discovery / implicit provider | Digested inline (Ollama `/api/tags`); link `term_model_catalog`. No new term. |
| auth profile / `auth.order` | Link existing `term_auth_profile` + `term_authentication`. No new term. |
| `OLLAMA_API_KEY` / `OPENAI_API_KEY` / `NVIDIA_API_KEY` / `OPENCODE_API_KEY` / `OPENROUTER_API_KEY` | Provider-specific env vars; documented as config, not promoted. Link `term_authentication` / `term_oauth_token`. No new term. |
| Codex runtime / Codex app-server harness | Link existing `term_agent_harness`; digested inline in `oc_providers_openai_auth`. No new term. |
| vision model / image understanding | Link existing `term_multimodal`. No new term. |
| memory embeddings / embedding provider | Link existing `term_embedding` + `term_rag`. No new term. |
| Ollama Web Search / web_search provider | Digested inline; link `term_rag` (no `term_web_search` note exists — surface owned by tools sub-plan to05). No new term. |
| Fusion router | Digested inline in `oc_providers_openrouter`; link `term_model_router`. No new term. |
| Realtime voice / Realtime API | Digested inline in `oc_providers_openai_media`; link `term_websocket` + `term_speech_to_text` (no `term_realtime_api` note exists). No new term. |
| TTS / STT (text-to-speech / speech-to-text) | Link existing `term_text_to_speech` + `term_speech_to_text`. No new term. |
| service_tier / priority processing / fast mode | Digested inline as OpenAI config; no reusable cross-cutting term. No new term. |
| WebSocket vs SSE transport | Link existing `term_websocket` + `term_sse`. No new term. |
| server-side compaction (Responses) | Link existing `term_compaction`. No new term. |
| prompt caching / cache markers / response cache | Link existing `term_prompt_caching` + `term_kv_cache`. No new term. |
| Azure OpenAI (deployment names, api-version) | Documented as config; link `term_api_gateway`. No new term (no `term_azure_openai` note; not cross-cutting enough to justify one). |
| model names: Kimi, GLM, MiniMax, GPT-5, Nemotron, Sora, Nemotron 3 Ultra, gpt-image-2 | Catalog config, NOT promoted to term notes (per master policy). Link `term_llm` / `term_nemotron` / `term_qwen` / `term_deepseek` / `term_claude` / `term_multimodal`. No new term. |


## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; it only LINKS existing terms (inherited from master Undigested-Terms decision). If augment Step 2d surfaces a genuinely cross-cutting, vault-reusable term with no existing note and no `oc_*` doc home, it would be captured via `/tessellum-capture-term-note` and added to its best-fit `acronym_glossary_*.md` (most likely `acronym_glossary_ai_ml.md` / the agentic-LLM glossary) per master W5 — none expected.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P2). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format: YAML field order + body structure (`## Overview`, `## Related Notes`, `## References`, bold footer) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: each note's claims/config diff against `inbox/openclaw_docs/providers/<page>.md` (verbatim config snippets) | manual diff vs mirror |
| G3 | Density + Coverage: ≤400 lines, ≤2,500 words, ≤6 code blocks, one BB/note; every H2/H3 mapped (Section Coverage Map) | `wc -w` + fence count |
| G4 | Cross-Reference: ≥6 relevancy-selected term links + repo/sibling/other links per note, each with a relevance statement | manual review |
| G5 | Ghost-reference detect + redirect: 0 links to non-existent notes | `/tessellum-fix-ghost-references` + DB existence check |
| G6 | Broken-link fix: 0 broken relative paths | `/tessellum-fix-broken-links` |
| G7 | Discoverability: every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | inlink audit (see Inlinks section) |
| G8 | In-degree ≥1 (anti-island): satisfied via `entry_openclaw_docs.md` rows + repo/term backlinks | `note_links` query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_providers_nvidia oc_providers_ollama_setup oc_providers_ollama_vision oc_providers_ollama_advanced oc_providers_ollama_cloud oc_providers_openai_auth oc_providers_openai_media oc_providers_openai_advanced oc_providers_opencode oc_providers_opencode_go oc_providers_openrouter"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do
    grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"
  done
  # require source_url in frontmatter
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code)"
  # G4 sibling/series link presence
  grep -q "$SIBLING_PREFIX" "$f" || echo "$n NO SIBLING/SERIES LINK"
done

# YAML frontmatter sweep across the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Within caps (≤2500w/≤6 code/≤400L)? |
|---|---|---|---:|---|
| 1 | oc_providers_nvidia | procedure | 480 | ✅ |
| 2 | oc_providers_ollama_setup | procedure | 720 | ✅ |
| 3 | oc_providers_ollama_vision | procedure | 430 | ✅ |
| 4 | oc_providers_ollama_advanced | procedure | 740 | ✅ (reproduce ≤6 canonical recipes/snippets; link the rest) |
| 5 | oc_providers_ollama_cloud | procedure | 420 | ✅ |
| 6 | oc_providers_openai_auth | procedure | 760 | ✅ |
| 7 | oc_providers_openai_media | procedure | 720 | ✅ |
| 8 | oc_providers_openai_advanced | procedure | 700 | ✅ |
| 9 | oc_providers_opencode | procedure | 470 | ✅ |
| 10 | oc_providers_opencode_go | procedure | 420 | ✅ |
| 11 | oc_providers_openrouter | procedure | 800 | ✅ (1,749w source / 17 fences → reproduce ≤6 config snippets selectively) |

No note approaches caps after the 3-way splits of ollama.md and openai.md. Code-heavy sections (ollama advanced 57 fences, openai media/advanced 39 fences, openrouter 17 fences) reproduce only the canonical config/JSON5 snippet per topic and link the redundant variants — each note ≤6 code blocks.

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)

- `entry_openclaw_docs.md` (planned, master pre-step) → **all 11 notes** (primary inbound source).
- `repo_openclaw_extensions_llm_providers` → notes 1, 2, 4, 5, 6, 9, 10, 11 (the LLM-provider extension package that implements these providers).
- `repo_openclaw_agents` → notes 2, 5, 6, 9, 10 (model catalog + auth profiles).
- `repo_openclaw_memory` → note 4 (Ollama memory embeddings).
- `repo_openclaw_apps` → note 7 (Control UI Talk realtime voice).
- `term_openclaw` → notes 6, 11 (anchor provider docs from the OpenClaw term note).
- `term_nemotron` → note 1; `term_qwen` → notes 2, 10; `term_deepseek` → notes 10, 11; `term_multimodal` → notes 3, 7, 11; `term_text_to_speech` / `term_speech_to_text` → note 7; `term_model_router` → notes 9, 11; `term_provider_plugin` → notes 2, 5, 6.

Each new note gets ≥1 reciprocal inbound link (entry point guarantees in-degree ≥1; term/repo backlinks add diversity).

## Pacing Rules (inherited from master)

One execution phase, 11 notes (≤30 fan-out cap; well within wave budget). Re-read each source page before authoring; reproduce config/JSON5 snippets verbatim; one BB per note. Cap dynamic-workflow fan-out at ~30 agents/run. `git pull --rebase --autostash origin main` before committing; commit + push per wave (no Claude co-author trailer). Reindex incrementally; verify `note_links` populated + 0 broken links + in-degree ≥1 before commit. All 8 gates pass before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**What was locked** (per-note counts; all floors met):

| # | Note | Terms | Snippets | Docs | Existing docs | Repos | Floors |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | oc_providers_nvidia | 8 | 10 | 10 | 8 | 2 | ✅ |
| 2 | oc_providers_ollama_setup | 8 | 10 | 10 | 8 | 2 | ✅ |
| 3 | oc_providers_ollama_vision | 8 | 10 | 10 | 7 | 2 | ✅ |
| 4 | oc_providers_ollama_advanced | 9 | 10 | 10 | 8 | 2 | ✅ |
| 5 | oc_providers_ollama_cloud | 8 | 10 | 10 | 7 | 2 | ✅ |
| 6 | oc_providers_openai_auth | 10 | 11 | 10 | 9 | 2 | ✅ |
| 7 | oc_providers_openai_media | 8 | 11 | 11 | 8 | 2 | ✅ |
| 8 | oc_providers_openai_advanced | 9 | 11 | 10 | 8 | 2 | ✅ |
| 9 | oc_providers_opencode | 8 | 10 | 10 | 8 | 2 | ✅ |
| 10 | oc_providers_opencode_go | 8 | 10 | 10 | 8 | 2 | ✅ |
| 11 | oc_providers_openrouter | 10 | 10 | 11 | 9 | 2 | ✅ |




## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | Per-note mapping locked at ≥8 terms · ≥10 snippets · ≥10 docs, each link with a relevance statement; floor-counter over all 11 H3 blocks → ALL FLOORS MET (min terms=8, min snippets=10, min docs=10, min existing-docs=7). |
| CP2 | 9-GATE present per batch | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link, G7/G8 discoverability (inherited from master). |
| CP4 | Plan size | **PASS** | 11 notes ≤30 fan-out cap; single execution phase. |
| CP5 | Format derived from existing notes | **PASS** | YAML field order + `## Overview`/`## Related Notes`/`## References`/bold footer inherited verbatim from master Format Definition, which was derived from the existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora (same source type). |
| CP6 | Density | **PASS** | Density Re-Assessment table: all 11 notes 420–800w, ≤6 code, ≤400L; ollama.md (5,456w) → 3 notes and openai.md (5,602w) → 3 notes split per word-cap + distinct-task-cluster; no note approaches caps. |
| CP7 | Sources measured | **PASS** | Re-read + `wc -w` of all 7 mirror pages = 15,177w, exactly matching the plan's Source table (ratio 1.00); no under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (every row dispositioned to an existing term or inline-config) + `## Term-Note Authoring Requirements` present (N/A — 0 new terms; falls back to `/tessellum-capture-term-note` + `acronym_glossary_ai_ml.md` if any surface). New-term scan re-run at augment → 0. |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs to author (all linked existing). Collision audit generalized to all 11 planned `oc_*` doc notes: each is a provider-config procedure with no duplicate among existing term/doc notes (term_* are concepts, oc_* are provider how-tos); the draft `term_api_key` collision (DB-MISSING) resolved by substituting `term_authentication`+`term_oauth_token`. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks` table maps outside-folder inbound links to all 11 notes (`entry_openclaw_docs` → all 11 primary; `repo_openclaw_extensions_llm_providers`/`repo_openclaw_agents`/`repo_openclaw_memory`/`repo_openclaw_apps` + `term_*` backlinks add diversity); G8 in-degree ≥1 in the phase gate table, executed at finalization. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
