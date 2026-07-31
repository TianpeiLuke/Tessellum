---
title: Sub-Plan pr05 — OpenClaw Docs: Providers (LiteLLM, LM Studio, MiniMax, Mistral, Models, Moonshot, Novita)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["providers/litellm", "providers/lmstudio", "providers/minimax", "providers/mistral", "providers/models", "providers/moonshot", "providers/novita"]
---

# Sub-Plan pr05: Providers

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_*`), format, dedup-before-create, the 9-GATE table,
> cross-reference policy, undigested-terms ownership (OpenClaw vocab → `oc_*` notes, never new term notes), and
> entry-point wiring are ALL inherited from the master; this file re-measures its 7 pages and locks the
> per-page → note coverage. Candidate cross-references are listed here; the exact locked per-note mapping is
> set later at `/tessellum-augment-digestion-plan`.

## Scope

The 7 provider pages for OpenAI-compatible gateways and aggregators (LiteLLM), local/self-hosted inference
(LM Studio), the multimodal MiniMax provider family (chat + image/TTS/music/video/search), Mistral (chat +
Voxtral STT + embeddings), the provider quickstart/index (`models`), Moonshot AI (Kimi K2 vs Kimi Coding),
and Novita (hosted OpenAI-compatible aggregator). **P2 (Phase B)** — the model-connectivity layer that the
gateway, CLI `models`/`infer`, and concepts/model-providers pages reference. Each page is a per-provider
setup/config reference; the code-side counterparts (`repo_openclaw_extensions_llm_providers`,
`repo_openclaw_agents`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **7,182 measured words**. **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| LiteLLM | providers/litellm | 646 | 3 | 4 | 3 | procedure |
| LM Studio | providers/lmstudio | 932 | 13 | 5 | 7 | procedure |
| MiniMax | providers/minimax | 2,273 | 3 | 8 | 6 | procedure + model (mixed-BB split: chat-setup vs media/search capabilities) |
| Mistral | providers/mistral | 988 | 4 | 6 | 0 | procedure |
| Model provider quickstart | providers/models | 270 | 1 | 4 | 0 | procedure |
| Moonshot AI | providers/moonshot | 1,650 | 1 | 5 | 0 | procedure |
| NovitaAI | providers/novita | 423 | 3 | 6 | 0 | procedure |

(Code = ``` fence pairs, i.e. raw fence lines / 2. LM Studio has 13 fenced blocks in source; only ≤6 verbatim
config snippets are reproduced per the density cap — see Content Strategy + Density Re-Assessment.)

## Content Strategy

- **Prioritize**: the provider config blocks every run depends on — `models.providers.<id>` (baseUrl / apiKey /
  api / models[]), onboarding `--auth-choice` flags, and the model-ref convention (`provider/model`). These are
  the load-bearing, copy-paste config the user needs.
- **Split**: `minimax.md` (2,273w, 8 H2 / 6 H3) is **mixed-BB** — a chat-provider setup procedure (catalog,
  OAuth vs API-key auth, configure wizard, thinking defaults, fallback) PLUS a multimodal capabilities model
  (image generation, TTS, music, video, image understanding, web search, each with its own config + the shared
  media-tool pointer). Split into note 3 (chat setup, procedure) + note 4 (media & search capabilities, model).
- **Selective code reproduction (LM Studio)**: 13 source fences exceed the ≤6 cap; reproduce the canonical
  Explicit/JIT/LAN config snippets + the auth-token export verbatim and summarize the rest in prose (≤6 blocks).
- **Skip / link-out**: shared media-tool semantics → `/tools/image-generation`, `/tools/music-generation`,
  `/tools/video-generation`, `/tools/minimax-search`, `/tools/web` (Tools section, to0x sub-plans); local model
  lifecycle → `/gateway/local-models` (gw03); the provider-rules concept page `/concepts/model-providers`,
  `/concepts/models`, `/concepts/model-failover` (co04) are LINKED, not redefined. Provider company names
  (Mistral, Moonshot, MiniMax, Novita) are documented as config, NOT promoted to `term_dictionary` notes —
  link existing `term_llm` / `term_third_party_genai_services` / `term_provider_plugin`.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_providers_litellm.md` | procedure | litellm.md: Quick start (onboarding + manual), Configuration (env vars, config file), Advanced configuration (image generation, virtual keys, model routing, viewing usage, proxy-behavior notes) | 480 | Route OpenClaw through a LiteLLM proxy for unified 100+-provider access, cost tracking, and routing: onboarding vs manual setup, `models.providers.litellm` config, image-generation backing, virtual keys, and the OpenAI-compat proxy-behavior caveats. |
| 2 | `oc_providers_lmstudio.md` | procedure | lmstudio.md: Quick start, Non-interactive onboarding, Configuration (streaming-usage compat, thinking compat, explicit config), Troubleshooting (not-detected, 401, JIT loading, LAN/tailnet host) | 560 | Run OpenClaw against local open-weight models via LM Studio (`lms`/`llmster`): install + server start, interactive/non-interactive onboarding, model-ref format, streaming-usage + reasoning-effort normalization, JIT/preload, LAN/tailnet host trust, and 401/not-detected troubleshooting. |
| 3 | `oc_providers_minimax_setup.md` | procedure | minimax.md: provider split table, Built-in catalog, Getting started (OAuth Coding Plan + API key, intl/CN), Configure via `openclaw configure`, Advanced configuration (options, thinking defaults, fast mode, fallback, coding-plan usage), Notes, Troubleshooting | 620 | Configure MiniMax chat models (default M3) in OpenClaw: `minimax` (API key) vs `minimax-portal` (OAuth) provider split, model catalog, intl/CN onboarding, the `configure` wizard, M2.x thinking-disable default + M3 exemption, fast mode, fallback, and the "Unknown model" fix. |
| 4 | `oc_providers_minimax_media.md` | model | minimax.md: Capabilities (Image generation, Text-to-speech, Music generation, Video generation, Image understanding, Web search) | 560 | The MiniMax multimodal capability surface bundled with the provider: `image_generate` (image-01, aspect ratios), TTS (T2A v2, voices, transcode), `music_generate` (music-2.6), `video_generate` (Hailuo), `MiniMax-VL-01` image understanding, and Token-Plan `web_search` — config paths, defaults, and auth resolution per capability. |
| 5 | `oc_providers_mistral.md` | procedure | mistral.md: provider property table, Getting started, Built-in LLM catalog, Audio transcription (Voxtral), Voice Call streaming STT, Advanced configuration (adjustable reasoning, memory embeddings, auth + base URL) | 560 | Use Mistral with OpenClaw — the bundled plugin's four contracts (chat, Voxtral batch transcription, Voxtral Realtime STT for Voice Call, `mistral-embed` memory embeddings): API-key onboarding, the LLM catalog, adjustable-reasoning → `reasoning_effort` mapping, the temperature-0 caveat, and base-URL config. |
| 6 | `oc_providers_models.md` | procedure | models.md: Quick start (two steps), Supported providers (starter set), Additional provider variants, Related | 320 | The model-provider quickstart/index for OpenClaw: the two-step authenticate-then-set-`provider/model` flow, the starter-set provider catalog (links to per-provider pages), and the additional provider variants (`anthropic-vertex`, `copilot-proxy`, `google-gemini-cli`). |
| 7 | `oc_providers_moonshot.md` | procedure | moonshot.md: Built-in model catalog, Getting started (Moonshot API intl/CN, Kimi Coding), Kimi web search, Advanced configuration (native thinking mode, tool-call-id sanitization, streaming-usage compat, endpoint/model-ref reference) | 620 | Configure Moonshot AI in OpenClaw: the Kimi K2 catalog + pricing, the separate `moonshot/` (Open Platform, intl/CN) vs `kimi/` (Kimi Coding) providers and keys, K2.7-Code always-on native thinking, the `/think`→thinking-type map, tool-call-id sanitization, and Kimi `web_search`. |
| 8 | `oc_providers_novita.md` | procedure | novita.md: Setup, Defaults, When to choose Novita, Models, Troubleshooting | 340 | Use NovitaAI's OpenAI-compatible hosted API as a bundled OpenClaw provider (`novita`, aliases `novita-ai`/`novitaai`): API-key setup, default `novita/deepseek/deepseek-v3-0324`, the seeded multi-vendor route catalog (DeepSeek/Kimi/MiniMax/GLM/Qwen), when-to-choose guidance, and 401/unknown-model troubleshooting. |

## Section Coverage Map

```
litellm.md
├── (intro: why LiteLLM + OpenClaw) ───────────────── → note 1 (oc_providers_litellm)
├── Quick start (Onboarding / Manual setup) ───────── → note 1
├── Configuration (Env variables, Config file) ────── → note 1
└── Advanced configuration (Image generation,
    Virtual keys, Model routing, Viewing usage,
    Proxy behavior notes) ──────────────────────────── → note 1
lmstudio.md
├── (intro: LM Studio / llama.cpp / MLX) ──────────── → note 2 (oc_providers_lmstudio)
├── Quick start (install/server/auth/onboard/model) ─ → note 2
├── Non-interactive onboarding ────────────────────── → note 2
├── Configuration (Streaming usage compat, Thinking
│   compat, Explicit configuration) ───────────────── → note 2
└── Troubleshooting (Not detected, 401, JIT loading,
    LAN/tailnet host) ──────────────────────────────── → note 2
minimax.md
├── (intro: defaults + bundled caps + provider split) → note 3 (oc_providers_minimax_setup)
├── Built-in catalog ──────────────────────────────── → note 3
├── Getting started (OAuth Coding Plan, API key) ──── → note 3
├── Configure via `openclaw configure` ────────────── → note 3
├── Capabilities ─ Image generation ───────────────── → note 4 (oc_providers_minimax_media)
├── Capabilities ─ Text-to-speech ─────────────────── → note 4
├── Capabilities ─ Music generation ───────────────── → note 4
├── Capabilities ─ Video generation ───────────────── → note 4
├── Capabilities ─ Image understanding ────────────── → note 4
├── Capabilities ─ Web search ─────────────────────── → note 4
├── Advanced configuration (options, thinking, fast
│   mode, fallback, coding-plan usage) ────────────── → note 3
├── Notes ─────────────────────────────────────────── → note 3
└── Troubleshooting ("Unknown model") ─────────────── → note 3
mistral.md
├── (intro: 4 contracts + property table) ─────────── → note 5 (oc_providers_mistral)
├── Getting started ───────────────────────────────── → note 5
├── Built-in LLM catalog ──────────────────────────── → note 5
├── Audio transcription (Voxtral) ─────────────────── → note 5
├── Voice Call streaming STT ──────────────────────── → note 5
└── Advanced configuration (Adjustable reasoning,
    Memory embeddings, Auth and base URL) ──────────── → note 5
models.md
├── Quick start (two steps) ───────────────────────── → note 6 (oc_providers_models)
├── Supported providers (starter set) ─────────────── → note 6
└── Additional provider variants ──────────────────── → note 6
moonshot.md
├── (intro: Kimi API + warning separate providers) ── → note 7 (oc_providers_moonshot)
├── Built-in model catalog ────────────────────────── → note 7
├── Getting started (Moonshot API, Kimi Coding) ───── → note 7
├── Kimi web search ───────────────────────────────── → note 7
└── Advanced configuration (Native thinking mode,
    Tool-call-id sanitization, Streaming-usage compat,
    Endpoint/model-ref reference) ──────────────────── → note 7
novita.md
├── (intro: hosted OpenAI-compatible aggregator) ──── → note 8 (oc_providers_novita)
├── Setup ─────────────────────────────────────────── → note 8
├── Defaults ──────────────────────────────────────── → note 8
├── When to choose Novita ─────────────────────────── → note 8
├── Models ────────────────────────────────────────── → note 8
└── Troubleshooting ───────────────────────────────── → note 8
```
No orphaned sections. Shared media-tool semantics (`/tools/*`), local-model lifecycle (`/gateway/local-models`),
and the provider-rules concept pages (`/concepts/model-providers`, `/concepts/models`,
`/concepts/model-failover`) are linked-out, not duplicated (owned by Tools / Gateway / Concepts sub-plans).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| minimax.md (2,273w, 8 H2 / 6 H3, mixed BB) | note 3 (`oc_providers_minimax_setup`, procedure) + note 4 (`oc_providers_minimax_media`, model) | The page mixes a chat-provider **setup procedure** (catalog, OAuth/API-key auth, configure wizard, thinking defaults, fallback, troubleshooting) with a multimodal **capabilities model** (image/TTS/music/video/image-understanding/web-search, each its own config + a shared media-tool pointer). One BB per note ⇒ split; each half stays ≤620w / ≤6 code. |

All other pages: 1 note each (each ≤2,500w, single procedure BB). LM Studio is code-dense (13 fences) but a
single procedure — kept as one note with selective ≤6 verbatim snippets, not split.

## Summary Statistics & Building Block Distribution

- Source pages: **7** (7,182 measured words). New `oc_*` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×7** (notes 1, 2, 3, 5, 6, 7, 8) · **model ×1** (note 4, MiniMax media capabilities).
- Est. digest words ~**4,060** (avg ~510/note; range 320–620). 28 source fence-pairs distribute across notes;
  each note kept ≤6 code blocks (LM Studio + MiniMax reproduce canonical config selectively).
- Cross-refs: **LOCKED at xref-augment 2026-06-21** — see `## Per-Note Related Notes Mapping`. Each of the 8
  notes meets the raised floors **≥8 `term_dictionary` terms · ≥10 code_snippets · ≥10 docs** (≥5 of the 10

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> Paths are RELATIVE from a note at `resources/documentation/openclaw/oc_X.md`: term →
> `../../term_dictionary/term_Y.md`; sibling `oc_*` (this series, not yet created) → `oc_Y.md`; other doc →
> `../<folder>/<file>.md`; repo → `../../../areas/code_repos/repo_Y.md`; snippet →
> (`term_ollama`, `term_mistral`, `term_moonshot`, `term_minimax`, `term_llm_gateway`, `term_kimi`,
> `term_glm`, `term_voxtral`, `term_gguf`, `term_tts`, `term_image_generation`, `term_web_search`,
> `term_reasoning_effort`, `term_semantic_search`) are deliberately NOT cited.

### oc_providers_litellm (8t · 11s · 11d)

**Terms** (8)
- [LLM](../../term_dictionary/term_llm.md) — large language model served behind a provider API; relevance: LiteLLM fronts 100+ LLM backends OpenClaw can route to.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — externally hosted generative-AI APIs; relevance: LiteLLM is the unified gateway over 100+ third-party services.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — server that forwards client requests to upstream backends; relevance: LiteLLM runs as a reverse proxy in front of model vendors on `localhost:4000`.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — single entry point that fronts/routes backend APIs; relevance: LiteLLM is the OpenAI-compatible gateway OpenClaw points `models.providers.litellm.baseUrl` at.
- [Model Router](../../term_dictionary/term_model_router.md) — component that maps a model name to a chosen backend; relevance: LiteLLM `model_list` routing keeps OpenClaw requesting one model ref while it picks the backend.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routing requests across multiple model providers; relevance: LiteLLM provides provider-side routing/failover beneath one OpenClaw provider entry.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — reuse of cached prompt prefixes to cut cost/latency; relevance: the proxy-behavior notes warn no prompt-cache hints pass through LiteLLM's OpenAI-compat path.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: the worked config routes `litellm/claude-opus-4-6` and `model: claude-opus-4-6` through the proxy.

**Docs** (11; 5 existing)
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — Claude Code routing through an LLM gateway; relevance: same gateway-fronting pattern OpenClaw uses for LiteLLM. (existing)
- [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — Claude Code's LiteLLM gateway config; relevance: direct cross-tool precedent for the exact LiteLLM proxy setup. (existing)
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — proxy/gateway base-URL + key injection; relevance: mirrors the `baseUrl`/`apiKey` config block. (existing)
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider config in Hermes; relevance: peer coding-agent's provider-via-gateway config. (existing)
- [hermes_model_aux_provider_config](../hermes_agent/hermes_model_aux_provider_config.md) — aux/secondary provider config for models; relevance: aligns with LiteLLM virtual-key + cost-tracking config. (existing)
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi's cloud provider catalog/config; relevance: gateway/base-URL config parallel. (existing)
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — per-model compat overrides; relevance: explains compat flags LiteLLM's OpenAI-compat proxy does/doesn't pass. (existing)
- [oc_providers_models](oc_providers_models.md) — provider quickstart/index; relevance: index page that links LiteLLM as one provider path. (planned, this series)
- [oc_providers_novita](oc_providers_novita.md) — hosted aggregator provider; relevance: peer aggregator/gateway alternative to a self-run LiteLLM. (planned, this series)
- [oc_providers_minimax_setup](oc_providers_minimax_setup.md) — OpenAI/Anthropic-compat provider config; relevance: sibling `models.providers.<id>` config exemplar. (planned, this series)
- [oc_providers_lmstudio](oc_providers_lmstudio.md) — local OpenAI-compat provider; relevance: contrasts a local proxy vs a LiteLLM gateway proxy. (planned, this series)

**Repos** (2)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension impls; relevance: where the OpenAI-compatible gateway/aggregator provider is implemented.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime, provider/auth resolution; relevance: resolves the `litellm/` model ref + API key at runtime.

**Snippets** (11)
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider def; relevance: the gateway/aggregator fan-out shape LiteLLM fills.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider def; relevance: LiteLLM uses `api: "openai-completions"`.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — OpenRouter/LiteLLM pricing lookup; relevance: implements the cost-tracking LiteLLM enables.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model alias→pricing resolution; relevance: maps `litellm/...` aliases to cost rows.
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — daily usage/cost rollup; relevance: the spend logs LiteLLM's dashboard surfaces.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/latency/cache status; relevance: the cache-hint gap noted in proxy-behavior notes.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog assembly; relevance: where `models[]` entries for litellm are materialized.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — proxy client connect; relevance: connecting to the LiteLLM proxy host.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution order; relevance: resolves `LITELLM_API_KEY` / virtual keys.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — Hermes aggregator provider plugin; relevance: cross-tool gateway/aggregator provider impl.

### oc_providers_lmstudio (9t · 11s · 11d)

**Terms** (9)
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: LM Studio runs open-weight LLMs locally for OpenClaw.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled plugin registering a model provider; relevance: `models.providers.lmstudio` is a bundled local OpenAI-compat provider plugin.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external/self-hosted GenAI endpoints; relevance: LM Studio exposes an OpenAI-compatible local endpoint.
- [vLLM](../../term_dictionary/term_vllm.md) — high-throughput local inference server; relevance: explicitly listed as a peer OpenAI-compat local backend with the same streaming-usage behavior.
- [Quantization](../../term_dictionary/term_quantization.md) — reduced-precision weights (GGUF) for local inference; relevance: LM Studio runs llama.cpp GGUF / MLX quantized weights.
- [Context Window](../../term_dictionary/term_context_window.md) — max tokens a model accepts; relevance: setup applies a preferred load context length across discovered models.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — model reasoning traces; relevance: OpenClaw normalizes LM Studio's binary reasoning discovery into `reasoning_effort` levels.
- [SSE](../../term_dictionary/term_sse.md) — server-sent-event streaming; relevance: streaming-usage compat recovers token counts from llama.cpp `timings` when usage is missing.
- [Authentication](../../term_dictionary/term_authentication.md) — credential checks / API tokens; relevance: `LM_API_TOKEN` and the 401 troubleshooting path.

**Docs** (11; 6 existing)
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — local/self-hosted LLM setup in Hermes; relevance: direct cross-tool precedent for LM-Studio-style local serving. (existing)
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — adding an inference provider; relevance: same provider-registration flow for a local backend. (existing)
- [pi_custom_models](../pi/pi_custom_models.md) — local Ollama/vLLM/LM-Studio models.json; relevance: documents the same local-model provider config. (existing)
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering a custom provider; relevance: registering `lmstudio` as a custom OpenAI-compat provider. (existing)
- [cc_model_selection](../claude_code/cc_model_selection.md) — choosing/configuring models; relevance: model-ref selection (`lmstudio/author/model`). (existing)
- [cc_configure_your_environment](../claude_code/cc_configure_your_environment.md) — env-var key injection; relevance: `LM_API_TOKEN` export pattern. (existing)
- [oc_providers_models](oc_providers_models.md) — provider index; relevance: lists LM Studio as a local provider option. (planned, this series)
- [oc_providers_litellm](oc_providers_litellm.md) — local-proxy OpenAI-compat path; relevance: contrasts gateway proxy vs local server. (planned, this series)
- [oc_providers_novita](oc_providers_novita.md) — hosted alternative; relevance: hosted-vs-local trade-off the LM Studio page implies. (planned, this series)
- [oc_providers_minimax_setup](oc_providers_minimax_setup.md) — provider config sibling; relevance: another `models.providers.<id>` config exemplar. (planned, this series)
- [oc_providers_mistral](oc_providers_mistral.md) — OpenAI-compat provider sibling; relevance: same `api: "openai-completions"` shape. (planned, this series)

**Repos** (2)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: where the local OpenAI-compat provider + private-network trust is implemented.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime/model resolution; relevance: resolves the `lmstudio/` model ref + preload step.

**Snippets** (11)
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — localhost base-url + ignored apiKey; relevance: near-identical shape to LM Studio's explicit local config.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — local/custom provider plugin; relevance: cross-tool local provider plugin impl.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider def; relevance: LM Studio uses `api: "openai-completions"`.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — normalize discovered model metadata; relevance: normalizes LM Studio `/api/v1/models` discovery + reasoning options.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — model schema normalization; relevance: maps binary `off/on` reasoning to `reasoning_effort` levels.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — MLX (Apple Silicon) inference; relevance: LM Studio runs MLX models on Apple Silicon.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage from streaming metadata; relevance: token-count recovery from llama.cpp `timings`.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — runtime env-var handling; relevance: `LM_API_TOKEN` injection.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: stores discovered LM Studio models into config.
- [snippet_openclaw_gateway_client_connect_proxy](../../code_snippets/snippet_openclaw_gateway_client_connect_proxy.md) — proxy/private-network connect; relevance: LAN/tailnet host + allowPrivateNetwork trust.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: peer impl of a custom local provider entry.

### oc_providers_minimax_setup (9t · 10s · 11d)

**Terms** (9)
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: MiniMax M3/M2.7 are the chat LLMs this note configures.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted GenAI vendor; relevance: MiniMax is a hosted third-party provider (intl/CN endpoints).
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider plugin; relevance: `minimax` / `minimax-portal` are bundled provider plugins.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization flow; relevance: the Coding-Plan OAuth path uses `minimax-portal`.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer token from OAuth; relevance: `MINIMAX_OAUTH_TOKEN` / stored OAuth profile auth resolution.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning/thinking blocks; relevance: M2.x thinking-disable default vs M3 native Anthropic thinking blocks.
- [Model Failover](../../term_dictionary/term_model_failover.md) — automatic fallback to a backup model; relevance: the fallback example fails primary over to `minimax/MiniMax-M2.7`.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — cached-prefix cost fields; relevance: the model `cost` block carries `cacheRead`/`cacheWrite` rates.
- [Authentication](../../term_dictionary/term_authentication.md) — credential resolution; relevance: API-key vs OAuth auth profile selection (`MINIMAX_API_KEY`).

**Docs** (11; 6 existing)
- [pi_custom_models](../pi/pi_custom_models.md) — Anthropic-messages / OpenAI-completions provider config; relevance: same `api:`/`baseUrl` provider config shape. (existing)
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — thinking + cache compat flags; relevance: the M2.x thinking-disable compat behavior. (existing)
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth/credential resolution; relevance: API-key vs OAuth profile precedence. (existing)
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — thinking/effort levels; relevance: the thinking-default behavior MiniMax exempts M3 from. (existing)
- [hermes_configuring_models_dashboard](../hermes_agent/hermes_configuring_models_dashboard.md) — configuring models; relevance: the `openclaw configure` wizard equivalent. (existing)
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider setup; relevance: hosted intl/CN provider onboarding parallel. (existing)
- [oc_providers_minimax_media](oc_providers_minimax_media.md) — the media/search half of this provider; relevance: shared auth/key; split sibling. (planned, this series)
- [oc_providers_models](oc_providers_models.md) — provider index; relevance: lists MiniMax setup path. (planned, this series)
- [oc_providers_moonshot](oc_providers_moonshot.md) — another intl/CN dual-endpoint provider; relevance: parallel intl/CN + dual-provider-id split. (planned, this series)
- [oc_providers_litellm](oc_providers_litellm.md) — provider config sibling; relevance: another `models.providers.<id>` exemplar. (planned, this series)
- [oc_providers_mistral](oc_providers_mistral.md) — reasoning-effort provider sibling; relevance: parallel thinking/reasoning-effort mapping. (planned, this series)

**Repos** (2)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugin impls; relevance: the MiniMax provider plugin lives here.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — auth profiles / model catalog; relevance: stores MiniMax auth profiles + thinking-default injection.

**Snippets** (10)
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — `anthropic-messages` provider def; relevance: MiniMax uses `api: "anthropic-messages"`.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider def; relevance: the optional OpenAI-compatible MiniMax payload path.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: `minimax-portal` Coding-Plan OAuth profile handling.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution order; relevance: OAuth-then-env-key MiniMax auth precedence.
- [snippet_openclaw_agents_context_anthropic_prefix](../../code_snippets/snippet_openclaw_agents_context_anthropic_prefix.md) — Anthropic prefix/thinking handling; relevance: the M2.x `thinking: { type: "disabled" }` injection.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — fallback ladder; relevance: the primary→MiniMax-M2.7 fallback chain.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: materializes M3 + both M2.7 entries.
- [snippet_openclaw_gateway_usage_cost_summary_daily](../../code_snippets/snippet_openclaw_gateway_usage_cost_summary_daily.md) — usage/cost rollup; relevance: Coding-Plan `% left` usage normalization.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing alias lookup; relevance: the per-model `cost` cacheRead/Write fields.
- [snippet_hermes_agent_plugins_provider_anthropic](../../code_snippets/snippet_hermes_agent_plugins_provider_anthropic.md) — Hermes anthropic-messages provider; relevance: cross-tool Anthropic-compat provider impl.

### oc_providers_minimax_media (10t · 11s · 11d)

**Terms** (10)
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative image model; relevance: `image-01` text-to-image / image-to-image generation.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: MiniMax T2A v2 registers as the `messages.tts` speech provider.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcription; relevance: the paired media/audio pipeline (transcode + voice-note targets).
- [Multimodal](../../term_dictionary/term_multimodal.md) — combined text/image/audio modalities; relevance: the bundled image/TTS/music/video/understanding/search capability surface.
- [VLM](../../term_dictionary/term_vlm.md) — vision-language model; relevance: `MiniMax-VL-01` image-understanding model.
- [Video Processing](../../term_dictionary/term_video_processing.md) — video generation/handling; relevance: `MiniMax-Hailuo-2.3` text-to-video / image-reference flows.
- [LLM](../../term_dictionary/term_llm.md) — chat-capable model; relevance: M3 advertises image input alongside the media providers.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted GenAI vendor; relevance: the MiniMax Token-Plan media + `web_search` APIs.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — capability-registering plugin; relevance: the MiniMax plugin registers `image_generate`/`music_generate`/`video_generate`/`web_search`.
- [Voice Call](../../term_dictionary/term_voice_call.md) — voice-note/voice-channel delivery; relevance: Feishu/Telegram voice-note Opus transcode targets for TTS output.

**Docs** (11; 6 existing)
- [hermes_image_generation](../hermes_agent/hermes_image_generation.md) — image-gen tool/provider; relevance: the shared `image_generate` tool MiniMax backs. (existing)
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — TTS provider catalog; relevance: peer of MiniMax T2A v2 as a TTS provider. (existing)
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — platform media tools; relevance: the media-tool semantics MiniMax capabilities plug into. (existing)
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media/transcode settings; relevance: the MP3→Opus voice-note transcode behavior. (existing)
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — multimodal cloud provider config; relevance: registering a multimodal provider. (existing)
- [cc_model_selection](../claude_code/cc_model_selection.md) — model/provider selection; relevance: selecting the image/music/video default models. (existing)
- [oc_providers_minimax_setup](oc_providers_minimax_setup.md) — the chat-setup half; relevance: shared MiniMax auth/key; split sibling. (planned, this series)
- [oc_providers_mistral](oc_providers_mistral.md) — other audio/STT provider; relevance: parallel media-understanding (Voxtral) provider. (planned, this series)
- [oc_providers_moonshot](oc_providers_moonshot.md) — other web-search provider; relevance: parallel `web_search` capability (Kimi search). (planned, this series)
- [oc_providers_models](oc_providers_models.md) — provider index; relevance: indexes MiniMax among media-capable providers. (planned, this series)
- [oc_providers_litellm](oc_providers_litellm.md) — image-gen-capable gateway; relevance: LiteLLM can also back `image_generate`, a cross-provider contrast. (planned, this series)

**Repos** (3)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — media + search capability registration; relevance: where the MiniMax media/search providers are implemented.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel media delivery; relevance: Feishu/Telegram voice-note delivery of transcoded audio.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extensions; relevance: the TTS speech-provider integration surface.

**Snippets** (11)
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — media model registration; relevance: registers `image-01`/`music-2.6`/Hailuo/VL-01 in the catalog.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image lifecycle; relevance: lifecycle of generated `image-01` outputs.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — image resize/validate; relevance: aspect-ratio / output-image handling.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen dispatch; relevance: cross-tool `image_generate` provider dispatch.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-gen tool; relevance: shared image-generation tool surface.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — TTS synthesis path; relevance: the speech-synthesis pipeline T2A v2 plugs into.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: TTS provider/voice routing parallel to T2A config.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — transcript media pipeline; relevance: the audio attachment / transcode pipeline.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: media-understanding/STT routing alongside generation.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — peer TTS provider impl; relevance: structural parallel to the MiniMax T2A speech provider.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call audio stream; relevance: the voice-note audio delivery targets (Feishu/Telegram).

### oc_providers_mistral (9t · 10s · 11d)

**Terms** (9)
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Mistral's chat catalog (Large/Medium/Small/Pixtral/Codestral/Devstral/Magistral).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted GenAI vendor; relevance: Mistral is a hosted OpenAI-compatible provider.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled multi-contract plugin; relevance: the bundled Mistral plugin registers four contracts.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcription; relevance: Voxtral batch transcription + Voxtral Realtime STT.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming STT; relevance: `voxtral-mini-transcribe-realtime-2602` streams transcripts for Voice Call.
- [Voice Call](../../term_dictionary/term_voice_call.md) — phone/voice channel; relevance: Voxtral Realtime is the Voice Call streaming STT provider (Twilio `pcm_mulaw` @ 8 kHz).
- [Multimodal](../../term_dictionary/term_multimodal.md) — text+image input; relevance: most catalog models accept text+image input.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — adjustable reasoning; relevance: thinking level maps to Mistral `reasoning_effort` (`none`/`high`).
- [Embedding](../../term_dictionary/term_embedding.md) — vector embeddings for retrieval/memory; relevance: `mistral-embed` serves memory embeddings via `/v1/embeddings`.

**Docs** (11; 6 existing)
- [cc_model_selection](../claude_code/cc_model_selection.md) — model selection/config; relevance: choosing among the Mistral catalog refs. (existing)
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — effort/thinking levels; relevance: the thinking→`reasoning_effort` mapping. (existing)
- [pi_custom_models](../pi/pi_custom_models.md) — OpenAI-compatible provider config; relevance: Mistral uses `api: "openai-completions"`, `baseUrl: https://api.mistral.ai/v1`. (existing)
- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — STT/transcription setup; relevance: the Voxtral batch + realtime transcription contracts. (existing)
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory/embedding providers; relevance: `mistral-embed` as a memory-search embedding provider. (existing)
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice mode / streaming STT; relevance: realtime STT for voice interaction. (existing)
- [oc_providers_models](oc_providers_models.md) — provider index; relevance: lists Mistral among providers. (planned, this series)
- [oc_providers_minimax_media](oc_providers_minimax_media.md) — other audio/STT + media provider; relevance: parallel media-understanding/STT capability provider. (planned, this series)
- [oc_providers_litellm](oc_providers_litellm.md) — other `openai-completions` provider; relevance: same OpenAI-compat chat shape. (planned, this series)
- [oc_providers_moonshot](oc_providers_moonshot.md) — other reasoning/thinking provider; relevance: parallel reasoning-effort handling. (planned, this series)
- [oc_providers_lmstudio](oc_providers_lmstudio.md) — OpenAI-compat provider sibling; relevance: same `api: "openai-completions"` config shape. (planned, this series)

**Repos** (2)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled Mistral plugin's four contracts; relevance: chat/Voxtral/realtime-STT/embedding registration.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: `mistral-embed` memory-search embeddings integration.

**Snippets** (10)
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider def; relevance: Mistral's chat API shape.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: the bundled Mistral catalog rows.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search; relevance: `memorySearch: { provider: "mistral" }` embeddings.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — voice-call stream transcription; relevance: Voxtral Realtime streaming STT for Voice Call.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call audio stream; relevance: `pcm_mulaw` @ 8 kHz Twilio media frames.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — peer STT provider impl; relevance: structural parallel to the Voxtral STT contract.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: batch media-understanding transcription path.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tooling; relevance: realtime STT wired into voice interaction.
- [snippet_openclaw_agents_context_anthropic_prefix](../../code_snippets/snippet_openclaw_agents_context_anthropic_prefix.md) — thinking/effort handling; relevance: the thinking→`reasoning_effort` translation.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-call manager; relevance: wires the streaming STT provider into Voice Call.

### oc_providers_models (8t · 10s · 11d)

**Terms** (8)
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the page is the LLM-provider quickstart/index.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted GenAI vendors; relevance: the supported-providers starter set is third-party services.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider plugin; relevance: each listed provider is a bundled/installable provider plugin.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: the supported-providers index is the provider/model catalog entry point.
- [Model Failover](../../term_dictionary/term_model_failover.md) — backup-model routing; relevance: the page links `/concepts/model-failover`.
- [Model Router](../../term_dictionary/term_model_router.md) — model-ref→backend mapping; relevance: the `provider/model` ref convention this page teaches.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: the worked example sets `anthropic/claude-opus-4-6`.
- [Authentication](../../term_dictionary/term_authentication.md) — provider auth step; relevance: step 1 is "authenticate with the provider (via `openclaw onboard`)".

**Docs** (11; 6 existing)
- [cc_model_selection](../claude_code/cc_model_selection.md) — choosing/configuring models; relevance: the same authenticate-then-pick-model flow. (existing)
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — provider catalog/config; relevance: the supported-providers catalog parallel. (existing)
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: peer coding-agent's provider index. (existing)
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — adding a provider; relevance: the per-provider onboarding the index links out to. (existing)
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog reference; relevance: the catalog of providers/models this index fronts. (existing)
- [cc_google_vertex_ai](../claude_code/cc_google_vertex_ai.md) — Google Vertex provider; relevance: parallels the `anthropic-vertex` / `google-gemini-cli` additional variants. (existing)
- [oc_providers_litellm](oc_providers_litellm.md) — per-provider page; relevance: index links the LiteLLM gateway path. (planned, this series)
- [oc_providers_lmstudio](oc_providers_lmstudio.md) — per-provider page; relevance: index links the local LM Studio path. (planned, this series)
- [oc_providers_minimax_setup](oc_providers_minimax_setup.md) — per-provider page; relevance: index links MiniMax setup. (planned, this series)
- [oc_providers_moonshot](oc_providers_moonshot.md) — per-provider page; relevance: index links Moonshot/Kimi. (planned, this series)
- [oc_providers_novita](oc_providers_novita.md) — per-provider page; relevance: index links the Novita aggregator. (planned, this series)

**Repos** (2)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider registry; relevance: the bundled provider catalog the index enumerates.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — provider/model resolution; relevance: resolves the `provider/model` default the page sets.

**Snippets** (10)
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog assembly; relevance: builds the supported-providers catalog.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider def; relevance: one starter-set provider variant.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — anthropic-messages provider def; relevance: the `anthropic/claude-opus-4-6` worked example.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` provider def; relevance: the OpenAI starter-set provider.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local provider def; relevance: a local provider variant in the catalog.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planning; relevance: plans the provider/model manifest the index reflects.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution; relevance: the authenticate step (step 1) of the quickstart.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — provider registry CLI; relevance: cross-tool provider-index impl.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider plugin registry; relevance: how providers register into the catalog.

### oc_providers_moonshot (9t · 10s · 11d)

**Terms** (9)
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Moonshot's Kimi K2 chat models.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted GenAI vendor + search API; relevance: Moonshot Open Platform + Kimi `web_search`.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider plugin; relevance: separate `moonshot/` and `kimi/` provider plugins.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — native thinking mode; relevance: K2.7-Code always-on native thinking + `/think`→thinking-type map.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool-call protocol; relevance: tool-call-id sanitization + `tool_choice` constraint.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — cache-read pricing; relevance: the cache-read pricing fields in the K2 catalog.
- [Authentication](../../term_dictionary/term_authentication.md) — credential keys; relevance: `MOONSHOT_API_KEY` vs `KIMI_API_KEY` for the two providers.
- [SSE](../../term_dictionary/term_sse.md) — streaming-usage compat; relevance: streaming-usage compatibility handling.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — token-based auth; relevance: Kimi Coding auth/token flow distinct from the API key.

**Docs** (11; 6 existing)
- [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: choosing between Kimi K2 catalog refs. (existing)
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — effort/thinking levels; relevance: the `/think`→thinking-type mapping. (existing)
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — compat flags for OpenAI-compat endpoints; relevance: streaming-usage / tool-call-id compat. (existing)
- [pi_provider_auth](../pi/pi_provider_auth.md) — provider auth resolution; relevance: the `MOONSHOT_API_KEY` vs `KIMI_API_KEY` selection. (existing)
- [hermes_x_search_grok](../hermes_agent/hermes_x_search_grok.md) — provider-bundled web search; relevance: parallel to Kimi `web_search`. (existing)
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider setup; relevance: intl/CN hosted-provider onboarding parallel. (existing)
- [oc_providers_models](oc_providers_models.md) — provider index; relevance: lists Moonshot/Kimi. (planned, this series)
- [oc_providers_minimax_setup](oc_providers_minimax_setup.md) — other intl/CN dual-endpoint provider; relevance: parallel intl/CN + dual-provider-id split. (planned, this series)
- [oc_providers_litellm](oc_providers_litellm.md) — other `openai-completions` provider; relevance: same OpenAI-compat chat shape. (planned, this series)
- [oc_providers_minimax_media](oc_providers_minimax_media.md) — other web-search provider; relevance: parallel bundled `web_search` capability. (planned, this series)
- [oc_providers_mistral](oc_providers_mistral.md) — other reasoning provider; relevance: parallel native-reasoning handling. (planned, this series)

**Repos** (2)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugin impls; relevance: the `moonshot`/`kimi` provider plugins + web_search.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — auth/model resolution; relevance: resolves the two key envs + native-thinking handling.

**Snippets** (10)
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` def; relevance: Moonshot's OpenAI-compatible endpoint.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: the Kimi K2 catalog rows.
- [snippet_hermes_agent_plugins_provider_kimi_coding](../../code_snippets/snippet_hermes_agent_plugins_provider_kimi_coding.md) — Kimi Coding provider plugin; relevance: cross-tool `kimi/` Kimi-Coding provider impl.
- [snippet_openclaw_agents_context_anthropic_prefix](../../code_snippets/snippet_openclaw_agents_context_anthropic_prefix.md) — thinking/reasoning handling; relevance: K2.7-Code always-on native thinking + `/think` map.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool-call policy; relevance: tool-call-id sanitization + `tool_choice` constraint.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing alias lookup; relevance: K2 cache-read pricing fields.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/cache status; relevance: streaming-usage compat behavior.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution order; relevance: `MOONSHOT_API_KEY` vs `KIMI_API_KEY` precedence.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — aggregator/provider plugin pattern; relevance: structural parallel for a multi-capability bundled provider.
- [snippet_hermes_agent_cli_auth_provider_state](../../code_snippets/snippet_hermes_agent_cli_auth_provider_state.md) — provider auth state; relevance: dual-key provider auth state tracking.

### oc_providers_novita (8t · 10s · 11d)

**Terms** (8)
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Novita hosts open-weight LLM routes for agent turns.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — hosted aggregator API; relevance: Novita is a hosted OpenAI-compatible aggregator over many vendors.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider plugin; relevance: `novita` (aliases `novita-ai`/`novitaai`) is a bundled provider plugin.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — seeded route catalog; relevance: the seeded multi-vendor route catalog (DeepSeek/Kimi/MiniMax/GLM/Qwen).
- [DeepSeek](../../term_dictionary/term_deepseek.md) — DeepSeek model family; relevance: default model `novita/deepseek/deepseek-v3-0324` + R1 route.
- [Qwen](../../term_dictionary/term_qwen.md) — Qwen model family; relevance: `novita/qwen/qwen3-235b-a22b-fp8` route.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — a provider used as a backup path; relevance: "when to choose Novita" positions it as another hosted fallback path.
- [Authentication](../../term_dictionary/term_authentication.md) — API-key auth; relevance: `NOVITA_API_KEY` setup + 401/403 troubleshooting.

**Docs** (11; 6 existing)
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — cloud provider catalog/config; relevance: hosted aggregator provider config parallel. (existing)
- [cc_model_selection](../claude_code/cc_model_selection.md) — model selection; relevance: picking exact `novita/<route-id>` refs. (existing)
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: peer hosted-aggregator setup. (existing)
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — fallback provider config; relevance: setting Novita as a fallback provider path. (existing)
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — adding a provider; relevance: the bundled-provider onboarding flow. (existing)
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider env vars/auth; relevance: `NOVITA_API_KEY` env-var auth. (existing)
- [oc_providers_models](oc_providers_models.md) — provider index; relevance: lists Novita among providers. (planned, this series)
- [oc_providers_litellm](oc_providers_litellm.md) — other aggregator/gateway; relevance: LiteLLM is the self-run aggregator contrast to hosted Novita. (planned, this series)
- [oc_providers_lmstudio](oc_providers_lmstudio.md) — local alternative; relevance: Novita is explicitly contrasted against running local LM Studio/Ollama/vLLM. (planned, this series)
- [oc_providers_minimax_setup](oc_providers_minimax_setup.md) — vendor whose routes Novita resells; relevance: MiniMax routes appear in the Novita catalog. (planned, this series)
- [oc_providers_moonshot](oc_providers_moonshot.md) — vendor whose routes Novita resells; relevance: Kimi/Moonshot routes appear in the Novita catalog. (planned, this series)

**Repos** (2)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider plugin impls; relevance: the bundled Novita provider + alias/route normalization.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — provider/model resolution; relevance: resolves `novita/<route-id>` refs + the default model.

**Snippets** (10)
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — peer hosted aggregator def; relevance: the same OpenAI-compat aggregator provider shape.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — `openai-completions` def; relevance: Novita uses the OpenAI-compatible endpoint.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: seeds the Novita multi-vendor route catalog.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — fallback ladder; relevance: Novita as a fallback provider path.
- [snippet_openclaw_agents_model_fallback_cooldown](../../code_snippets/snippet_openclaw_agents_model_fallback_cooldown.md) — fallback cooldown; relevance: tolerating provider-specific variance / slow routes.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error handling; relevance: 401/403/unknown-model error → reroute.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — aggregator pricing lookup; relevance: per-route cost for an aggregator's routes.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution; relevance: `NOVITA_API_KEY` auth profile.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model-ref normalization; relevance: `novita/<route-id>` normalization from `models list`.

## Undigested Terms Plan

pr05 creates **0 new `term_dictionary` notes** (per master: OpenClaw provider vocabulary → `oc_*` doc notes;
only EXISTING terms are linked).

| Term (as it appears in source) | Disposition |
|---|---|
| LiteLLM, LM Studio, MiniMax, Mistral, Moonshot/Kimi, NovitaAI (provider/company names) | Documented as config in their `oc_providers_*` notes; NOT promoted to term notes. Link `term_llm` / `term_third_party_genai_services` / `term_provider_plugin`. |
| LLM gateway / proxy / model routing / virtual keys (LiteLLM) | Captured in `oc_providers_litellm`; link `term_reverse_proxy`, `term_api_gateway`, `term_model_router`. (`term_llm_gateway` checked — MISSING; do not invent, link `term_api_gateway`.) |
| Local inference / GGUF / MLX / JIT model loading / Apple Silicon (LM Studio) | Captured in `oc_providers_lmstudio`; link `term_quantization`, `term_vllm`, `term_context_window`. (`term_gguf`/`term_local_inference`/`term_apple_silicon` checked — MISSING; not invented.) |
| OpenAI-compatible API / Anthropic-messages API / `openai-completions` / `anthropic-messages` | Documented as config (`api:` field) in each provider note; link `term_openai_responses_api`, `term_converse_api`, `term_function_calling`. (`term_openai_compatible_api`/`term_anthropic_messages_api` checked — MISSING; not invented.) |
| Reasoning / thinking levels / `reasoning_effort` (Mistral, MiniMax, Moonshot) | Captured in the per-provider notes; link `term_chain_of_thought`. (`term_reasoning_effort`/`term_reasoning_model` checked — MISSING; not invented.) |
| Image / TTS / music / video generation, image understanding, web search (MiniMax media) | Captured in `oc_providers_minimax_media`; link `term_diffusion_model`, `term_text_to_speech`, `term_speech_to_text`, `term_multimodal`, `term_voice_call`. Shared tool semantics link-out to `/tools/*` (Tools sub-plans). (`term_tts`/`term_image_generation`/`term_web_search` checked — MISSING; not invented.) |
| Voxtral (batch + realtime STT), `mistral-embed` embeddings | Captured in `oc_providers_mistral`; link `term_speech_to_text`, `term_voice_call`. (`term_voxtral`/`term_embeddings` checked — MISSING; not invented.) |
| Model ref convention (`provider/model`), provider id / aliases, `--auth-choice`, model failover/fallback | Documented as config across the notes; link `term_model_catalog`, `term_model_failover`. |
| Cost tracking / token usage / cache-read–write pricing | Documented inline as config fields; link `term_prompt_caching`, `term_kv_cache`. (`term_cost_tracking`/`term_token_usage` checked — MISSING; not invented.) |

**New-term candidates:** none. No genuinely cross-cutting, vault-reusable term lacks an existing note AND a
doc-page home — all source vocabulary is either provider config (digested in `oc_*`) or covered by an existing
linked term. Augment Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** pr05 authors zero `term_dictionary` notes; it only links existing terms. The master's
new-term capture requirement (`/tessellum-capture-term-note` + acronym glossary) does not apply here. Inherited
from master.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P2). All gates must PASS before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format (`/tessellum-check-note-format` + `check_yaml_frontmatter.py`) | Fixed YAML field order, `## Overview` + source-mirrored body + `## Related Notes` + `## References` + bold footer; no forbidden YAML fields. |
| G2 | Grounding (diff vs `inbox/openclaw_docs/providers/<page>.md`) | Every config block / model id / env var / `--auth-choice` flag traces to source; no invented values. |
| G3 | Density + Coverage | ≤400 lines, ≤2,500 words, ≤6 code blocks, one building_block per note; every mapped H2/H3 present. |
| G4 | Cross-Reference | ≥6 relevancy-selected term links + repo/sibling/doc/snippet links per note, each with a relevance statement. |
| G6 | Broken-link fix (`/tessellum-fix-broken-links`) | 0 broken relative paths after reindex. |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md`). |
| G8 | In-degree ≥1 | `note_links`/`in_degree` confirms each new note has ≥1 inbound edge. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_providers_litellm oc_providers_lmstudio oc_providers_minimax_setup oc_providers_minimax_media oc_providers_mistral oc_providers_models oc_providers_moonshot oc_providers_novita"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n: format OK"
  # required H2 sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n: MISSING SECTION $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n: MISSING source_url"; }
  # at least one sibling oc_ Related link
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "$n: NO sibling $SIBLING_PREFIX link"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5 ghost / G6 broken handled via /tessellum-fix-ghost-references + /tessellum-fix-broken-links after reindex.
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code blocks | Within caps (≤400L / ≤2500w / ≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_providers_litellm | procedure | 480 | ≤6 | ✅ |
| 2 | oc_providers_lmstudio | procedure | 560 | ≤6 (selective from 13 source fences) | ✅ |
| 3 | oc_providers_minimax_setup | procedure | 620 | ≤6 | ✅ |
| 4 | oc_providers_minimax_media | model | 560 | ≤4 | ✅ |
| 5 | oc_providers_mistral | procedure | 560 | ≤6 | ✅ |
| 6 | oc_providers_models | procedure | 320 | ≤2 | ✅ |
| 7 | oc_providers_moonshot | procedure | 620 | ≤6 (selective from large config) | ✅ |
| 8 | oc_providers_novita | procedure | 340 | ≤3 | ✅ |

No note approaches caps. The two code-/config-dense pages — `lmstudio.md` (13 fences) and `minimax.md`
(reproduces only canonical config) — reproduce canonical snippets selectively to stay ≤6; the mixed-BB
`minimax.md` split keeps each half single-BB and ≤620w.

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (the navigation hub CREATED as the master W1 pre-step,
>30 master total) under the **Providers** section / pr05 sub-plan cluster. Each note receives its
entry-point back-link at finalization (satisfies G7/G8). No standalone entry point for this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all targets below confirmed present):
- `entry_openclaw_docs.md` (W1 hub) → all 8 notes (primary discoverability path).
- `repo_openclaw_extensions_llm_providers.md` → notes 1, 2, 3, 4, 5, 6, 7, 8 (code↔docs cross-link; the
  provider-plugin implementation each note documents).
- `repo_openclaw_agents.md` → notes 3, 5, 6, 7, 8 (auth profiles / model catalog).
- `term_llm.md` → notes 1, 6 (provider-quickstart / gateway entry points).
- `term_third_party_genai_services.md` → notes 1, 8 (aggregator/gateway provider catalog).
- `term_provider_plugin.md` → notes 2, 3, 5 (bundled provider plugins).
- `term_speech_to_text.md` / `term_voice_call.md` → notes 4, 5 (MiniMax media + Mistral Voxtral STT).
- `term_deepseek.md` / `term_qwen.md` → note 8 (Novita route catalog).
- `term_model_failover.md` → note 6 (failover pointer).

## Pacing Rules (inherited from master)

One execution phase; all 8 gates pass before commit. Re-read each source page; reproduce config snippets
verbatim and selectively (≤6/note). One BB per note (the minimax split enforces this). Cap dynamic-workflow
fan-out at ~30 agents/run; reindex incrementally; verify `note_links` + 0 broken links before commit;
`git pull --rebase --autostash` first; no Claude co-author trailer; commit + push in the same turn.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**What was locked.** The `## Candidate Cross-References` section was replaced by `## Per-Note Related Notes
Mapping (LOCKED — xref-augment 2026-06-21)` at the RAISED floors: **≥8 `term_dictionary` terms · ≥10
renders as `- [Name](relpath.md) — what it is; relevance: why THIS note`, grouped **Terms / Docs / Repos /
Snippets**. All 7 source pages were re-read from `inbox/openclaw_docs/providers/` before selection. Per-note
counts verified programmatically against H3 headers (exact match) and all snippet/doc/term targets verified in
the unified DB (110 distinct existing targets OK; the only absent targets are the 8 planned `oc_*` siblings,

**Per-note counts (terms · snippets · docs · repos):**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors |
|---|---:|---:|---|---:|---|
| oc_providers_litellm | 8 | 11 | 11 (7/4) | 2 | ✅ |
| oc_providers_lmstudio | 9 | 11 | 11 (6/5) | 2 | ✅ |
| oc_providers_minimax_setup | 9 | 10 | 11 (6/5) | 2 | ✅ |
| oc_providers_minimax_media | 10 | 11 | 11 (6/5) | 3 | ✅ |
| oc_providers_mistral | 9 | 10 | 11 (6/5) | 2 | ✅ |
| oc_providers_models | 8 | 10 | 11 (6/5) | 2 | ✅ |
| oc_providers_moonshot | 9 | 10 | 11 (6/5) | 2 | ✅ |
| oc_providers_novita | 8 | 10 | 11 (6/5) | 2 | ✅ |

**New-term candidates + best-fit glossary.** **None.** Step 2d re-scan of all 7 re-read pages surfaced no
genuinely cross-cutting, vault-reusable term lacking both an existing note AND a doc-page home. All provider
vocabulary is either (a) provider config digested in the `oc_*` notes, or (b) covered by an existing linked
term. Terms checked-and-MISSING (`term_ollama`, `term_mistral`, `term_moonshot`, `term_minimax`,
`term_llm_gateway`, `term_kimi`, `term_glm`, `term_voxtral`, `term_gguf`, `term_tts`, `term_image_generation`,
`term_web_search`, `term_reasoning_effort`, `term_semantic_search`) are per master policy NOT invented —
substitutes linked instead (e.g. `term_api_gateway`/`term_reverse_proxy` for LLM-gateway, `term_chain_of_thought`
for reasoning-effort, `term_diffusion_model`/`term_vlm`/`term_video_processing` for the media capabilities,
`term_realtime_transcription`/`term_speech_to_text` for Voxtral). pr05 still authors **0 new `term_dictionary`
notes** (consistent with master). Best-fit glossary: N/A (no new terms).

**Newly-discovered relevant existing terms (added beyond the draft's ≥6 set to hit ≥8):**
`term_provider_routing`, `term_fallback_provider`, `term_realtime_transcription`, `term_embedding`,

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors (≥10 snippets, ≥10 docs) | **PASS** | All 8 notes: ≥8 terms / ≥10 snippets / ≥10 docs; each link carries a `relevance:` statement; per-note counts match H3 headers exactly (verified programmatically). |
| CP2 | 9-GATE present per batch (G1-G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with all of G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost, G6 broken-link, G7 discoverability, G8 in-degree. |
| CP4 | Size (≤30 or split) | **PASS** | 8 notes (single execution phase), well under 30; part of the 105-sub-plan master split. |
| CP5 | Format derived from existing target-dir notes | **PASS** | YAML field order + `## Overview` / source-mirrored body / `## Related Notes` / `## References` / bold footer derived from existing `cc_*` / `pi_*` doc corpora (master Format Definition); `building_block` ∈ {procedure ×7, model ×1}. |
| CP6 | Density (borderline → split promoted) | **PASS** | Density Re-Assessment: all 8 notes ≤620w / ≤6 code / ≤400L; mixed-BB `minimax.md` already split into setup (procedure) + media (model). No borderline note unaddressed. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-measured all 7 pages: litellm 607w (est 646, 0.94×), lmstudio 897 (932, 0.96×), minimax 2249 (2273, 0.99×), mistral 946 (988, 0.96×), models 236 (270, 0.87×), moonshot 1602 (1650, 0.97×), novita 392 (423, 0.93×). All within 0.87–0.99× (±30%). |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (0 new terms; all dispositions = link existing); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, master requirement does not apply). New-term scan (Step 2d) re-run: none. |
| CP8f | Slug specificity + collision audit (all notes, term AND doc) | **PASS** | Collision audit over all 8 planned `oc_*` slugs: 0 exact matches in DB; synonym scan (litellm/minimax/etc.) found only different-tool notes (`cc_llm_gateway_litellm`, `hermes_provider_minimax_oauth`) which the plan LINKS, not recreates. No too-general slugs (all are `oc_providers_<vendor>[_<facet>]`). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing → new)` covers all 8 notes with ≥1 outside-folder inbound link (entry_openclaw_docs hub + repo_openclaw_extensions_llm_providers → all 8); G8-Discoverability + G8 in-degree in the gate table as an executed phase. |

**RESULT: 10/10 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
