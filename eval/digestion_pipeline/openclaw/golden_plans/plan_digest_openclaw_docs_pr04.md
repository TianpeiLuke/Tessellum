---
title: Sub-Plan pr04 — OpenClaw Docs: Providers (Google, Gradium, Groq, Hugging Face, Inferrs, Inworld, Kilo Gateway)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["providers/google", "providers/gradium", "providers/groq", "providers/huggingface", "providers/inferrs", "providers/inworld", "providers/kilocode"]
---


# Sub-Plan pr04: Providers

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order + body H2 + density caps), dedup (three-way vs term_dictionary / documentation / `repo_openclaw*`), undigested-terms policy (OpenClaw vocab → `oc_` doc notes, link existing terms), 9-GATE validation, cross-references, and entry-point wiring are ALL inherited from the master.
> This sub-plan covers 7 provider integration pages → **8 planned `oc_provider_*` notes** (google splits into chat-vs-media). Per-note Related-Notes mapping is LOCKED (xref-augment 2026-06-21) at raised floors (≥8 terms · ≥10 snippets · ≥10 docs) in "## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)".

## Scope

The 7 provider pages assigned to pr04: **Google (Gemini)**, **Gradium**, **Groq**, **Hugging Face (inference)**, **Inferrs**, **Inworld**, and **Kilo Gateway (kilocode)**. They cover three sub-families of OpenClaw provider integrations:

- **First-class multi-capability LLM provider** — Google/Gemini (chat + image/video/music generation + TTS + realtime voice + Grounding web search).
- **OpenAI-compatible chat / inference providers** — Groq (LPU fast inference + Whisper transcription), Hugging Face Inference router, Inferrs (self-hosted local OpenAI-compatible server), Kilo Gateway (unified multi-model gateway).
- **Speech (text-to-speech) providers** — Gradium, Inworld.

Priority **P2** (Phase B — features/integration). These pages are *per-provider configuration procedures*: how to install the plugin, supply credentials (API key / OAuth / env var), choose default models, and tune provider-specific options. They reference the shared provider/model layer (`concepts/model-providers`, `concepts/models`) and shared media/TTS tools defined elsewhere. The code-side counterparts (`repo_openclaw_extensions_llm_providers`, `repo_openclaw_extensions_voice_speech`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **5,365 measured words**. **Planned: 8 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Google (Gemini) | providers/google | 1,851 | 7 | 10 | 0 | procedure (split: chat/auth/search vs media/voice) |
| Gradium | providers/gradium | 510 | 3 | 7 | 1 | procedure |
| Groq | providers/groq | 818 | 3 | 6 | 1 | procedure |
| Hugging Face (inference) | providers/huggingface | 1,077 | 1 | 4 | 1 | procedure |
| Inferrs | providers/inferrs | 940 | 2 | 6 | 0 | procedure |
| Inworld | providers/inworld | 557 | 1 | 5 | 0 | procedure |
| Kilo Gateway | providers/kilocode | 612 | 2 | 6 | 0 | procedure |

Totals: 5,365 words · 19 code fences · 44 H2 · 4 H3.

## Content Strategy

- **Prioritize**: provider auth + model selection (every run depends on the credential env var, the `provider/model` ref form, and the default-model config) and the OpenAI-compatible-path quirks (Groq `reasoning_effort` mapping, Inferrs `requiresStringContent`/`supportsTools` compat flags, Kilo proxy-reasoning behavior) — these are the operationally load-bearing parts.
- **Split**: `google.md` (1,851w, 10 H2) mixes two distinct task clusters — (a) Gemini chat auth (API key + Gemini-CLI OAuth), thinking-level mapping, Grounding web search, and advanced config; (b) the bundled Google media + voice providers (image, video, music generation, batch TTS, realtime voice over the Live API). Split into 2 notes (chat/auth/search vs media/voice) so each is single-focus and stays well under caps. All other pages → 1 note each (all ≤1,100w).
- **Link-out (not duplicated)**: shared provider/model selection + failover → `concepts/model-providers`, `concepts/models` (co04, planned) and existing `term_model_failover`/`cc_model_selection`; shared media tools (`tools/image-generation`, `tools/video-generation`, `tools/music-generation`, `tools/tts`, `tools/thinking`, `tools/gemini-search`) → Tools sub-plans (to0x, planned); local model services (`gateway/local-model-services`, `gateway/local-models`) → Gateway sub-plans (gw0x, planned); model names (Llama, Qwen, DeepSeek, Gemma, GPT-OSS, Kimi, GLM) are documented as catalog rows / config refs, NOT promoted to new term notes — link existing `term_llm`/`term_claude`/`term_deepseek`/`term_qwen` where relevant.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_provider_google_chat.md` | procedure | google.md: front matter, Getting started (API key Tab + Gemini CLI OAuth Tab), Capabilities table, Web search, Advanced configuration (Direct Gemini cache reuse, Gemini CLI usage notes, Environment/daemon) | 650 | Configuring the Google Gemini chat provider: API-key vs Gemini-CLI OAuth auth, `GEMINI_API_KEY`/`GOOGLE_API_KEY` env vars, default `google/*` model ref, thinking-level mapping for Gemini 3/3.1/Gemma 4, Gemini Grounding web search, and advanced cache/daemon config. |
| 2 | `oc_provider_google_media_voice.md` | procedure | google.md: Image generation, Video generation, Music generation, Text-to-speech, Realtime voice | 650 | The bundled Google media + voice providers: image generation (Gemini 3.1 Flash Image), video generation (Veo 3.1), music generation (Lyria 3), batch Gemini TTS (voices, audio tags), and realtime voice over the Gemini Live API (VAD/turn/session settings for Voice Call and Meet). |
| 3 | `oc_provider_gradium.md` | procedure | gradium.md: front matter, Install plugin, Setup, Config, Voices (+ Per-message voice override), Output, Auto-select order | 450 | Configuring the Gradium text-to-speech provider: install `@openclaw/gradium-speech`, `GRADIUM_API_KEY` auth, `messages.tts.providers.gradium` config, voice catalog + per-message `/voice:` override directives, surface-driven output formats (WAV/Opus/u-law), and auto-select priority 30. |
| 4 | `oc_provider_groq.md` | procedure | groq.md: front matter, Install plugin, Getting started (+ Config file example), Built-in catalog, Reasoning models, Audio transcription, advanced (daemon env, custom model ids) | 550 | Configuring the Groq provider: install `@openclaw/groq-provider`, `GROQ_API_KEY` auth, OpenAI-compatible chat with the LPU catalog (Llama/Qwen/GPT-OSS/Compound), `/think`→`reasoning_effort` mapping, and the Whisper audio-transcription media provider on `tools.media.audio`. |
| 5 | `oc_provider_huggingface.md` | procedure | huggingface.md: front matter, Getting started (+ Non-interactive setup), Model IDs, Advanced configuration (model discovery, names/aliases/policy suffixes, daemon env, fallback config examples) | 600 | Configuring the Hugging Face Inference Providers router: fine-grained `HF_TOKEN`/`HUGGINGFACE_HUB_TOKEN` auth, OpenAI-compatible router endpoint, `huggingface/<org>/<model>` Hub-style refs, `:fastest`/`:cheapest` policy suffixes, dynamic model discovery via GET /v1/models, and alias/fallback config. |
| 6 | `oc_provider_inferrs.md` | procedure | inferrs.md: front matter, Getting started, Full config example, On-demand startup, Advanced configuration (requiresStringContent, Gemma tool-schema, smoke test, proxy-style), Troubleshooting | 600 | Running OpenClaw against a self-hosted Inferrs OpenAI-compatible local server: custom `models.providers.inferrs` entry (no bundled plugin), `localService` on-demand startup, the `requiresStringContent`/`supportsTools` compat flags, proxy-style request shaping, and troubleshooting local backends. |
| 7 | `oc_provider_inworld.md` | procedure | inworld.md: front matter, Install plugin, Getting started, Configuration options, Notes (Authentication, Models, Audio outputs, Custom endpoints) | 450 | Configuring the Inworld streaming text-to-speech provider: install `@openclaw/inworld-speech`, `INWORLD_API_KEY` HTTP-Basic (Base64 dashboard credential) auth, `messages.tts.providers.inworld` config (voice/model/temperature), and surface-driven MP3/OGG_OPUS/PCM output. |
| 8 | `oc_provider_kilocode.md` | procedure | kilocode.md: front matter, Install plugin, Getting started, Default model, Built-in catalog, Config example, advanced (Transport/compat, Stream wrapper/reasoning, Troubleshooting) | 500 | Configuring the Kilo Gateway (`kilocode`) unified-API provider: install `@openclaw/kilocode-provider`, `KILOCODE_API_KEY` auth, the `kilocode/kilo/auto` smart-routing default, dynamic model discovery + static fallback catalog, OpenRouter-compatible proxy transport, and proxy-reasoning caveats. |

Filename rule applied: `oc_` + slug with `/`→`_` and `-`→`_`; google split appends a `_chat` / `_media_voice` aspect suffix. (`providers/google` → base `oc_provider_google`; split → `oc_provider_google_chat`, `oc_provider_google_media_voice`. The other slugs are 1-note: `providers/groq` → `oc_provider_groq`, etc.)

## Section Coverage Map

```
google.md (1,851w, 10 H2)
├── (front matter: provider id / auth / API / runtime option) → note 1 (oc_provider_google_chat)
├── ## Getting started (Tab: API key; Tab: Gemini CLI OAuth) ──── → note 1
├── ## Capabilities (capability matrix) ───────────────────────── → note 1 (overview anchor; media rows cross-ref note 2)
├── ## Web search (Gemini Grounding, webSearch config, /think) ── → note 1
├── ## Image generation ──────────────────────────────────────── → note 2 (oc_provider_google_media_voice)
├── ## Video generation ──────────────────────────────────────── → note 2
├── ## Music generation ──────────────────────────────────────── → note 2
├── ## Text-to-speech (batch Gemini TTS, voices, audio tags) ──── → note 2
├── ## Realtime voice (Gemini Live API, VAD/turn/session table) ─ → note 2
├── ## Advanced configuration (cache reuse, Gemini CLI notes, env) → note 1
└── ## Related (cards → link-out: model-providers, media tools) ── → notes 1+2 References
gradium.md (510w, 7 H2 / 1 H3)
├── (front matter property table: id/auth/baseUrl/voice) ──────── → note 3 (oc_provider_gradium)
├── ## Install plugin / ## Setup / ## Config ─────────────────── → note 3
├── ## Voices / ### Per-message voice override ───────────────── → note 3
├── ## Output / ## Auto-select order ─────────────────────────── → note 3
└── ## Related (link-out: tts, media-overview) ───────────────── → note 3 References
groq.md (818w, 6 H2 / 1 H3)
├── (front matter property table) ────────────────────────────── → note 4 (oc_provider_groq)
├── ## Install plugin / ## Getting started (+ ### Config file example) → note 4
├── ## Built-in catalog (model table) ────────────────────────── → note 4
├── ## Reasoning models (/think → reasoning_effort) ──────────── → note 4
├── ## Audio transcription (Whisper media provider) ──────────── → note 4
└── ## Related (link-out: model-providers, thinking, config-ref) → note 4 References
huggingface.md (1,077w, 4 H2 / 1 H3)
├── (front matter: provider/auth/api/billing) ────────────────── → note 5 (oc_provider_huggingface)
├── ## Getting started (+ ### Non-interactive setup) ─────────── → note 5
├── ## Model IDs (Hub-style refs, :fastest/:cheapest) ────────── → note 5
├── ## Advanced configuration (discovery, names/aliases/suffixes, daemon, fallback examples) → note 5
└── ## Related (link-out: model-providers, models, config) ───── → note 5 References
inferrs.md (940w, 6 H2)
├── (front matter property table + Note: custom backend) ─────── → note 6 (oc_provider_inferrs)
├── ## Getting started / ## Full config example ──────────────── → note 6
├── ## On-demand startup (localService) ──────────────────────── → note 6
├── ## Advanced configuration (requiresStringContent, Gemma, smoke test, proxy-style) → note 6
├── ## Troubleshooting ───────────────────────────────────────── → note 6
└── ## Related (link-out: local-models, local-model-services, gw troubleshooting) → note 6 References
inworld.md (557w, 5 H2)
├── (front matter property table) ────────────────────────────── → note 7 (oc_provider_inworld)
├── ## Install plugin / ## Getting started ───────────────────── → note 7
├── ## Configuration options ─────────────────────────────────── → note 7
├── ## Notes (Authentication, Models, Audio outputs, Custom endpoints) → note 7
└── ## Related (link-out: tts, config, providers, troubleshooting) → note 7 References
kilocode.md (612w, 6 H2)
├── (front matter property table) ────────────────────────────── → note 8 (oc_provider_kilocode)
├── ## Install plugin / ## Getting started ───────────────────── → note 8
├── ## Default model (kilocode/kilo/auto) ────────────────────── → note 8
├── ## Built-in catalog (dynamic discovery + static fallback) ── → note 8
├── ## Config example ────────────────────────────────────────── → note 8
├── (advanced: Transport/compat, Stream wrapper/reasoning, Troubleshooting) → note 8
└── ## Related (link-out: model-providers, config-ref) ───────── → note 8 References
```
No orphaned sections. Shared model/media/tts tool pages and local-model-service pages are linked, not duplicated (owned by co0x / to0x / gw0x sub-plans).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| google.md (1,851w, 10 H2, 7 code) | notes 1 + 2 | Mixed concern: chat-provider auth/model/thinking/Grounding-search/advanced (note 1) vs the bundled Google media + voice providers — image/video/music generation, batch TTS, realtime Live-API voice (note 2). Two distinct task clusters and capability families; splitting keeps each single-focus, ≤650w, and ≤6 code fences (the page has 7 fences total — splitting also resolves the code-cap pressure). Both remain `procedure` BB. |
| gradium.md (510w) | note 3 (no split) | Single TTS-provider config procedure, well under caps. |
| groq.md (818w) | note 4 (no split) | Single chat+transcription provider config procedure; the Whisper media provider is a sub-section of the same Groq integration, not a separate BB. |
| huggingface.md (1,077w) | note 5 (no split) | Single inference-router config procedure; the 5 config examples are variations of one task. |
| inferrs.md (940w) | note 6 (no split) | Single local-OpenAI-compatible-server config procedure (config + on-demand + compat + troubleshooting are one task cluster). |
| inworld.md (557w) | note 7 (no split) | Single streaming-TTS-provider config procedure. |
| kilocode.md (612w) | note 8 (no split) | Single unified-gateway provider config procedure. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (5,365 measured words, 19 code fences). New `oc_` notes: **8**. New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×8** (every note is a per-provider configuration procedure). No concept/model/argument notes in this sub-plan.
- Est. digest words ≈ 4,450 (avg ≈ 556/note); all notes ≤650w (well under the 2,500w cap). 19 source fences distribute across the 8 notes; each note kept ≤6 fences (config snippets reproduced selectively, verbatim — google's 7 fences split 4/3 across notes 1/2).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

>
> Relative paths from `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/term_Y.md`; sibling oc_ → `oc_Y.md`; cc_ → `../claude_code/cc_Y.md`; pi_ → `../pi/pi_Y.md`; hermes_ → `../hermes_agent/hermes_Y.md`; band_ → `../band/band_Y.md`; bedrock_ → `../aws_bedrock/bedrock_Y.md`; repo → `../../../areas/code_repos/repo_Y.md`; snippet → `../../code_snippets/snippet_Y.md`.

### oc_provider_google_chat (10t · 12s · 11d)

**Terms** (10):
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the Gemini 3/3.1 Pro and Gemma 4 chat models this provider authenticates and serves.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential verification; relevance: the API-key vs Gemini-CLI auth choice (`GEMINI_API_KEY`/`GOOGLE_API_KEY`) is the core of "Getting started".
- [OAuth](../../term_dictionary/term_oauth.md) — delegated authorization protocol; relevance: the Gemini CLI tab reuses an existing Gemini CLI login via OAuth instead of a separate API key.
- [PKCE](../../term_dictionary/term_pkce.md) — Proof Key for Code Exchange OAuth flow; relevance: the doc states the `google-gemini-cli` provider uses PKCE OAuth for the local Gemini CLI login.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — issued access/refresh credential; relevance: `OPENCLAW_GEMINI_OAUTH_CLIENT_ID`/`_SECRET` (or `GEMINI_CLI_*`) drive the OAuth token exchange and refresh.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — intermediate reasoning trace; relevance: the `thinkingLevel`/`thinkingBudget` mapping for Gemini 3/3.1/Gemma 4 and `/think adaptive` control reasoning visibility.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external generative-AI APIs; relevance: Google AI Studio / Gemini API is the external GenAI service this provider integrates.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — reuse of cached prompt context; relevance: "Direct Gemini cache reuse" passes `cachedContent` and normalizes hits into OpenClaw `cacheRead`.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: `openclaw models list --provider google` and the Capabilities matrix enumerate the provider's model catalog.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: Gemini chat supports tool calls, the contract OpenClaw keeps for agent runs.

**Docs** (11):
- [cc_google_vertex_ai](../claude_code/cc_google_vertex_ai.md) — Claude Code Google Vertex AI provider setup; relevance: closest analog of Google-provider auth + region/project config (`GOOGLE_CLOUD_PROJECT`).
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — Claude Code effort/thinking levels; relevance: direct analog of the Gemini `thinkingLevel`/`/think` reasoning mapping.
- [cc_model_selection](../claude_code/cc_model_selection.md) — Claude Code model selection; relevance: the `provider/model` ref form and default-model config this page sets (`google/gemini-3.1-pro-preview`).
- [cc_prompt_caching_mechanism](../claude_code/cc_prompt_caching_mechanism.md) — Claude Code prompt-caching mechanism; relevance: direct analog of the "Direct Gemini cache reuse" (`cachedContent` → `cacheRead`) advanced config.
- [hermes_provider_google_gemini](../hermes_agent/hermes_provider_google_gemini.md) — Hermes Google Gemini provider; relevance: sibling-ecosystem Gemini provider config (auth, model refs) — the closest cross-corpus analog.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — Hermes add-inference-provider how-to; relevance: the general provider-registration procedure that the Google plugin instantiates.
- [pi_provider_auth](../pi/pi_provider_auth.md) — pi provider auth (subscription vs key); relevance: the subscription/CLI-OAuth-vs-API-key auth choice mirrors Gemini CLI OAuth vs API key.
- [pi_cloud_providers](../pi/pi_cloud_providers.md) — pi cloud-provider config; relevance: Google/Vertex/ADC cloud-credential analog for the gateway-host env setup.
- [oc_provider_google_media_voice](oc_provider_google_media_voice.md) — the bundled Google media/voice half (planned, this series); relevance: same `google` plugin; Capabilities matrix media rows cross-ref this note.
- [oc_concepts_model_providers](oc_concepts_model_providers.md) — shared provider/model-ref/failover layer (planned, co04); relevance: the model-selection layer the Google provider plugs into.
- [oc_tools_gemini_search](oc_tools_gemini_search.md) — Gemini Grounding web-search tool (planned, to0x); relevance: the Web search section configures `webSearch` and defers tool behavior to this tool page.


**Snippets** (12):
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog assembly; relevance: how `models list --provider google` resolves the catalog.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — discovery normalization; relevance: normalizes `google/gemini-3.1-pro` alias to canonical ids.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalization; relevance: model-entry schema for Gemini catalog rows.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider entry; relevance: provider-entry pattern (apiKey/baseUrl/models) the Google provider follows.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential precedence resolution; relevance: the `apiKey` → `GEMINI_API_KEY` → `GOOGLE_API_KEY` fallback order.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile portability; relevance: reusing the Gemini CLI OAuth login as a portable auth profile.
- [snippet_openclaw_agents_auth_profiles_external_cli](../../code_snippets/snippet_openclaw_agents_auth_profiles_external_cli.md) — external-CLI auth profile; relevance: the `google-gemini-cli` runtime reuses the local `gemini` CLI credential.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env loading; relevance: the daemon `GEMINI_API_KEY` availability (`~/.openclaw/.env`/`env.shellEnv`) callout.
- [snippet_openclaw_gateway_usage_latency_cache_status](../../code_snippets/snippet_openclaw_gateway_usage_latency_cache_status.md) — usage/cache-status accounting; relevance: Gemini `cachedContentTokenCount` → `cacheRead` normalization.
- [snippet_hermes_agent_core_gemini_cloudcode_adapter_auth](../../code_snippets/snippet_hermes_agent_core_gemini_cloudcode_adapter_auth.md) — Hermes Gemini Cloud Code adapter auth; relevance: direct cross-corpus analog of Gemini-CLI-OAuth credential handling.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: resolving the active provider's credential/auth-choice analog.
- [snippet_hermes_agent_cli_models_fetch](../../code_snippets/snippet_hermes_agent_cli_models_fetch.md) — model-list fetch; relevance: the `models list` catalog-fetch analog.

### oc_provider_google_media_voice (10t · 12s · 11d)

**Terms** (10):
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis from text; relevance: the batch Gemini TTS path (`gemini-3.1-flash-tts-preview`, voices, audio tags) is a core section.
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex socket protocol; relevance: the Gemini Live API uses bidirectional audio + function calling over a WebSocket.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multiple input/output modalities; relevance: image/video/music generation + image/audio/video understanding span text, image, audio, and video.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative denoising model; relevance: the image (Gemini Flash Image) and video (Veo) generation models are diffusion-class media generators.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: OpenClaw keeps tool calls on the shared realtime-voice contract over the Live API.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the Gemini generation models backing image/video/music/TTS/realtime.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external generative-AI APIs; relevance: the Google media + Live APIs are external GenAI services.
- [Model Failover](../../term_dictionary/term_model_failover.md) — fallback across providers; relevance: shared media-tool provider selection + failover (deferred to the Tools pages) governs which provider serves each media tool.
- [SSE](../../term_dictionary/term_sse.md) — server-sent events streaming; relevance: streaming media/audio delivery and session-backed status flow for detached music runs.
- [TTS](../../term_dictionary/term_speech_to_text.md) — speech-to-text transcription; relevance: the Capabilities matrix lists audio transcription / Live API transcription as a Google capability alongside TTS.

**Docs** (11):
- [cc_google_vertex_ai](../claude_code/cc_google_vertex_ai.md) — Claude Code Google Vertex AI setup; relevance: Google-provider config + project/region analog for the media/voice providers.
- [cc_model_selection](../claude_code/cc_model_selection.md) — Claude Code model selection; relevance: the `imageGenerationModel`/`videoGenerationModel`/`musicGenerationModel` default-ref selection pattern.
- [hermes_provider_google_gemini](../hermes_agent/hermes_provider_google_gemini.md) — Hermes Gemini provider; relevance: sibling-ecosystem Gemini config including media/voice capabilities.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — Hermes TTS providers; relevance: cross-corpus TTS-provider config analog for the Gemini TTS path.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — Hermes voice-mode guide; relevance: realtime/voice-mode setup analog for the Gemini Live API realtime voice.
- [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — Hermes image-gen provider plugin; relevance: direct analog of the bundled Google image-generation provider.
- [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — Hermes video-gen provider plugin; relevance: direct analog of the Veo video-generation provider registration.
- [oc_provider_google_chat](oc_provider_google_chat.md) — the chat/auth/search half (planned, this series); relevance: same `google` plugin; shares auth + the Capabilities matrix anchor.
- [oc_tools_image_generation](oc_tools_image_generation.md) — shared image-generation tool (planned, to0x); relevance: the page defers shared image-tool params/failover to this tool.
- [oc_tools_video_generation](oc_tools_video_generation.md) — shared video-generation tool (planned, to0x); relevance: shared video-tool params/failover home.
- [oc_tools_tts](oc_tools_tts.md) — shared TTS tool (planned, to0x); relevance: shared TTS provider-selection home for the Gemini TTS path.

**Repos** (4): [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech/voice extensions; relevance: home of the Google TTS + realtime voice providers. · [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — Voice Call/telephony bridge; relevance: consumes the Gemini Live realtime voice + PCM TTS for telephony/Meet. · [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: where the Google image/video/music providers register. · [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway runtime; relevance: hosts the shared media-tool task/status flow.

**Snippets** (12):
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — Voice Call runtime; relevance: the realtime-voice runtime consuming the Gemini Live provider.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call media-stream audio; relevance: PCM Live API audio bridging for telephony/Meet.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — media-stream transcription; relevance: Gemini Live transcription on the realtime contract.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-call session manager; relevance: VAD/turn/session settings (`activityHandling`, `sessionResumption`) management.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — Talk transcription relay; relevance: the generic Gateway relay transport for backend-only realtime voice (Control UI Talk).
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — managed-image resize/validate; relevance: image-generation output geometry (`size`/`aspectRatio`/`resolution`) handling.
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — managed-image record lifecycle; relevance: lifecycle of generated image/media artifacts.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS provider; relevance: analog speech-provider implementation (WAV/Opus output) for the Gemini TTS path.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — MLX local TTS; relevance: another TTS-provider analog feeding the reply-audio pipeline.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the reply-audio pipeline (WAV→Opus transcode with ffmpeg) Gemini TTS feeds.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: cross-corpus TTS provider-selection analog.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: realtime voice-mode analog for the Live API bridge.

### oc_provider_gradium (8t · 10s · 10d)

**Terms** (8):
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis from text; relevance: Gradium IS a TTS provider — the note's entire subject.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider integration; relevance: `@openclaw/gradium-speech` is the official installable plugin.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: `GRADIUM_API_KEY` / config `apiKey` with documented precedence.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external generative-AI APIs; relevance: Gradium (`api.gradium.ai`) is an external TTS service.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — request-forwarding intermediary; relevance: the `baseUrl` override targets an operator proxy / compatible origin.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the reply text Gradium synthesizes originates from an LLM run.
- [SSE](../../term_dictionary/term_sse.md) — server-sent streaming; relevance: TTS audio is rendered/streamed into WAV/Opus/u-law reply-audio buffers.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcription; relevance: contrast/companion modality on the same voice surfaces Gradium output targets (telephony/voice-note).

**Docs** (10):
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code authentication; relevance: env-var/secret-ref credential model analog for `GRADIUM_API_KEY`.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — Hermes TTS providers; relevance: direct cross-corpus analog — TTS-provider catalog + config.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — Hermes voice-mode guide; relevance: voice-output setup analog where a TTS provider is selected.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — Hermes voice-mode CLI; relevance: CLI voice-output config analog (provider/voice selection).
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — Hermes add-provider how-to; relevance: the install-plugin + restart-gateway procedure analog.
- [pi_provider_auth](../pi/pi_provider_auth.md) — pi provider auth; relevance: API-key credential model analog for a third-party provider.
- [oc_provider_inworld](oc_provider_inworld.md) — sibling streaming-TTS provider (planned, this series); relevance: the other streaming-TTS provider in pr04 — same `messages.tts` config shape, reciprocal sibling.
- [oc_tools_tts](oc_tools_tts.md) — shared TTS tool (planned, to0x); relevance: the auto-select-order (Gradium = 30) + provider-pinning logic lives here.
- [oc_tools_media_overview](oc_tools_media_overview.md) — media overview (planned, to0x); relevance: where TTS sits among OpenClaw media tools.
- [oc_concepts_model_providers](oc_concepts_model_providers.md) — provider/model layer (planned, co04); relevance: the shared provider-selection framework Gradium registers into.

**Repos** (4): [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech-provider extensions; relevance: home of the Gradium speech plugin. · [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — telephony/voice surfaces; relevance: consumes Gradium's WAV/Opus/u-law output. · [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework; relevance: the plugin-install framework Gradium ships through. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — Hermes provider adapters; relevance: analog speech-provider adapter implementation.

**Snippets** (10):
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS provider; relevance: nearly identical speech-provider shape (API key, voice id, surface-driven output) to Gradium.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — MLX TTS; relevance: another speech-provider implementation feeding the reply-audio pipeline.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the surface-driven output-format selection (WAV/Opus/u-law) Gradium relies on.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: telephony surface consuming u-law 8 kHz TTS output.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — media-stream audio; relevance: how synthesized audio is admitted into the telephony bridge.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential precedence; relevance: resolved `apiKey` first, then `GRADIUM_API_KEY` env fallback.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — call credentials/secrets; relevance: `${ENV}`/secret-ref resolution for the Gradium apiKey.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: making `GRADIUM_API_KEY` visible to the gateway daemon.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: provider auto-select/routing analog (Gradium order 30).
- [snippet_hermes_agent_cli_voice](../../code_snippets/snippet_hermes_agent_cli_voice.md) — CLI voice config; relevance: per-message voice-override directive analog (`/voice:` tokens).

### oc_provider_groq (10t · 12s · 11d)

**Terms** (10):
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Groq serves open-weight chat models (Llama, Qwen, GPT-OSS, Kimi, Compound).
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible API surface; relevance: Groq's `openai-completions` API is the OpenAI-compatible path OpenClaw drives.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — intermediate reasoning; relevance: the `/think` → `reasoning_effort` mapping (none/default/low/medium/high) per Groq reasoning model.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio transcription; relevance: Groq's Whisper (`whisper-large-v3-turbo`) audio media-understanding provider on `tools.media.audio`.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI APIs; relevance: Groq is an external inference provider (LPU hardware).
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — model registry; relevance: the manifest-backed Groq catalog + `openclaw models list --provider groq`.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: `GROQ_API_KEY` auth (env / config / daemon availability).
- [Qwen](../../term_dictionary/term_qwen.md) — Alibaba open-weight model family; relevance: `groq/qwen/qwen3-32b` is a catalog reasoning model.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — open-weight reasoning model family; relevance: DeepSeek R1 Distill uses Groq's native reasoning surface (visibility via `/think`).
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: tool calls on the OpenAI-compatible chat models for agent runs.

**Docs** (11):
- [cc_effort_level_and_thinking](../claude_code/cc_effort_level_and_thinking.md) — Claude Code effort/thinking; relevance: direct analog of `/think` levels → provider effort mapping.
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — Claude Code LLM gateway; relevance: OpenAI-compatible base-URL provider config analog (`https://api.groq.com/openai/v1`).
- [cc_model_selection](../claude_code/cc_model_selection.md) — Claude Code model selection; relevance: the default-model + `provider/model` ref pattern (`groq/llama-3.3-70b-versatile`).
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — Hermes add-inference-provider; relevance: install-plugin + auth + default-model procedure analog.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — Hermes cloud inference providers; relevance: cross-corpus catalog of OpenAI-compatible cloud inference providers like Groq.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — Hermes media providers; relevance: media-provider (audio) registration analog for the Whisper transcription provider.
- [pi_custom_models](../pi/pi_custom_models.md) — pi custom models; relevance: custom OpenAI-completions model-entry config analog (custom Groq model ids).
- [oc_provider_huggingface](oc_provider_huggingface.md) — sibling OpenAI-compatible router (planned, this series); relevance: same `openai-completions` path + open-weight catalog cluster.
- [oc_tools_thinking](oc_tools_thinking.md) — shared thinking tool (planned, to0x); relevance: the `/think` levels page Groq defers `reasoning_effort` translation to.
- [oc_tools_media_overview](oc_tools_media_overview.md) — media overview (planned, to0x); relevance: where `tools.media.audio` transcription sits.
- [oc_concepts_model_providers](oc_concepts_model_providers.md) — provider/model layer (planned, co04); relevance: the shared provider-selection layer Groq plugs into.


**Snippets** (12):
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider entry; relevance: the `openai-completions` provider-entry pattern Groq uses verbatim.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog assembly; relevance: the manifest-backed catalog `models list --provider groq` reads.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest planner; relevance: the static manifest-backed Groq catalog rows.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalization; relevance: uncatalogued Groq ids fall through to the OpenAI-compatible template.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT provider; relevance: audio media-understanding analog for Groq's Whisper transcription provider.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — OpenAI HTTP message build; relevance: building the OpenAI-compatible chat request Groq receives.
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — OpenAI HTTP SSE stream; relevance: streaming the OpenAI-compatible completion response from Groq's fast LPU endpoint.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: the daemon `GROQ_API_KEY` availability callout.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: provider-registration analog for the Groq plugin.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter provider; relevance: another OpenAI-compatible multi-model provider config analog.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: cross-corpus audio-transcription provider analog for Whisper.
- [snippet_hermes_agent_model_tools_capability_probe](../../code_snippets/snippet_hermes_agent_model_tools_capability_probe.md) — model capability probe; relevance: reasoning vs non-reasoning capability detection driving `reasoning_effort`.

### oc_provider_huggingface (10t · 11s · 11d)

**Terms** (10):
- [Hugging Face](../../term_dictionary/term_huggingface.md) — ML model hub + inference platform; relevance: the provider itself — HF Inference Providers router.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the many routed chat models (DeepSeek, Llama, Qwen, GLM, Kimi, GPT-OSS).
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible API; relevance: HF uses the OpenAI-compatible `router.huggingface.co/v1` chat-completions endpoint.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — single-entry request router; relevance: a single HF token routes to many upstream inference providers behind one router API.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI APIs; relevance: HF Inference Providers is an aggregator of external inference services.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — model registry; relevance: GET `/v1/models` discovery merged with the built-in catalog.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: fine-grained `HF_TOKEN`/`HUGGINGFACE_HUB_TOKEN` with the "Make calls to Inference Providers" permission.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — open-weight model family; relevance: `huggingface/deepseek-ai/DeepSeek-R1` is the default model.
- [Qwen](../../term_dictionary/term_qwen.md) — Alibaba open-weight family; relevance: Qwen3/Qwen2.5 are listed + used in fallback config examples.
- [Model Failover](../../term_dictionary/term_model_failover.md) — fallback across models; relevance: the alias/fallback config examples (`fallbacks: [...]`) and `:fastest`/`:cheapest` policy suffixes.

**Docs** (11):
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — Claude Code LLM gateway; relevance: router/gateway base-URL provider config analog (single token fanning out).
- [cc_model_selection](../claude_code/cc_model_selection.md) — Claude Code model selection; relevance: Hub-style `huggingface/<org>/<model>` ref + alias selection.
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — Claude Code fallback models; relevance: direct analog of the primary/fallbacks config examples.
- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — Hermes cloud inference providers; relevance: cross-corpus aggregator/router inference-provider config analog.
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — Hermes add-inference-provider; relevance: the onboarding + token + default-model procedure analog.
- [hermes_fallback_providers](../hermes_agent/hermes_fallback_providers.md) — Hermes fallback providers; relevance: the fallback/alias config analog for the HF examples.
- [pi_custom_models](../pi/pi_custom_models.md) — pi custom models; relevance: custom model-entry + alias config analog.
- [pi_provider_auth](../pi/pi_provider_auth.md) — pi provider auth; relevance: fine-grained token auth model analog.
- [oc_provider_groq](oc_provider_groq.md) — sibling OpenAI-compatible provider (planned, this series); relevance: same `openai-completions` path + open-weight catalog.
- [oc_provider_kilocode](oc_provider_kilocode.md) — sibling unified-gateway provider (planned, this series); relevance: another single-key multi-model router.
- [oc_concepts_models](oc_concepts_models.md) — model selection/refs concept (planned, co04); relevance: model-ref + policy-suffix selection layer.


**Snippets** (11):
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider entry; relevance: the OpenAI-compatible provider-entry pattern HF follows.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: single-key multi-upstream router pattern = HF Inference Providers.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — discovery normalization; relevance: GET `/v1/models` discovery → normalized catalog (`object: list`, `data: [...]`).
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest planner; relevance: merging discovered models ahead of the built-in catalog (metadata/cost/context).
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalization; relevance: name hydration from `name`/`title`/`display_name` or id-derived.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: the `primary` + `fallbacks` ladder in the HF config examples.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing/alias lookup; relevance: per-model `alias` overrides + `:cheapest`/`:fastest` policy variants.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential precedence; relevance: `HUGGINGFACE_HUB_TOKEN` precedence over `HF_TOKEN`.
- [snippet_hermes_agent_cli_models_fetch](../../code_snippets/snippet_hermes_agent_cli_models_fetch.md) — model-list fetch; relevance: the Inference-API model-list fetch populating the onboarding dropdown.
- [snippet_hermes_agent_cli_models_normalize](../../code_snippets/snippet_hermes_agent_cli_models_normalize.md) — model-list normalization; relevance: normalizing the discovered HF model list.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: provider-registration analog for the HF plugin.

### oc_provider_inferrs (10t · 11s · 11d)

**Terms** (10):
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the locally-served model (e.g. `google/gemma-4-E2B-it`) on the inferrs server.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible API; relevance: inferrs serves the generic `openai-completions` `/v1` path OpenClaw drives.
- [vLLM](../../term_dictionary/term_vllm.md) — high-throughput local inference server; relevance: the doc points to vLLM/SGLang as bundled-plugin alternatives in the same local-OpenAI-compatible class.
- [Quantization](../../term_dictionary/term_quantization.md) — model weight compression; relevance: local model serving (Gemma 4 on metal) is a quantization/local-serving context.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider integration; relevance: load-bearing contrast — inferrs is NOT a bundled plugin; you configure a custom `models.providers.inferrs` entry instead.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI backend; relevance: inferrs is a self-hosted external inference backend.
- [Context Window](../../term_dictionary/term_context_window.md) — max token span; relevance: the `contextWindow: 131072` model field in the custom entry.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-invoked tool calls; relevance: `compat.supportsTools: false` disables OpenClaw's tool schema surface for strict local backends.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — request-forwarding intermediary; relevance: inferrs is treated as a proxy-style `/v1` backend (no native OpenAI request shaping / attribution headers).
- [SSE](../../term_dictionary/term_sse.md) — server-sent streaming; relevance: the OpenAI-compatible `/v1/chat/completions` streaming path against the local server.

**Docs** (11):
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — Claude Code LLM gateway; relevance: custom base-URL provider config analog (`http://127.0.0.1:8080/v1`).
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — Claude Code proxy/gateway config; relevance: the proxy-style backend treatment analog.
- [cc_configure_advisor_model](../claude_code/cc_configure_advisor_model.md) — Claude Code advisor-model config; relevance: pointing a model ref at a custom provider entry analog.
- [hermes_local_self_hosted_llm](../hermes_agent/hermes_local_self_hosted_llm.md) — Hermes local self-hosted LLM; relevance: direct cross-corpus analog — self-hosted OpenAI-compatible local server config.
- [hermes_provider_local_llm_mac](../hermes_agent/hermes_provider_local_llm_mac.md) — Hermes local LLM on Mac; relevance: local metal-device serving analog (Gemma on `--device metal`).
- [hermes_provider_ollama_local](../hermes_agent/hermes_provider_ollama_local.md) — Hermes local Ollama provider; relevance: localhost OpenAI-compatible local-backend config analog.
- [pi_custom_models](../pi/pi_custom_models.md) — pi custom models; relevance: the `models.providers` custom-entry schema analog — the closest doc to the inferrs custom entry.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — pi model overrides/compat; relevance: the compat-flag analog (`requiresStringContent`/`supportsTools`).
- [oc_gateway_local_model_services](oc_gateway_local_model_services.md) — local-model-services (planned, gw0x); relevance: the `localService` on-demand-startup field reference this page defers to.
- [oc_gateway_local_models](oc_gateway_local_models.md) — local models (planned, gw0x); relevance: running OpenClaw against local model servers.
- [oc_provider_huggingface](oc_provider_huggingface.md) — sibling OpenAI-compatible provider (planned, this series); relevance: same `openai-completions` path, different (cloud vs local) backend.


**Snippets** (11):
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — Ollama local provider; relevance: localhost baseUrl + ignored apiKey + explicit model list = exactly the inferrs custom-entry pattern.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider entry; relevance: the `openai-completions` provider-entry schema inferrs reuses.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — catalog schema normalization; relevance: the model-entry fields (`id`/`name`/`reasoning`/`cost`/`contextWindow`/`maxTokens`/`compat`).
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog assembly; relevance: how the custom inferrs model entry enters the catalog.
- [snippet_openclaw_gateway_openai_http_message_build](../../code_snippets/snippet_openclaw_gateway_openai_http_message_build.md) — OpenAI HTTP message build; relevance: `requiresStringContent` flattens content-part arrays into plain strings before sending.
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — OpenAI HTTP SSE stream; relevance: the OpenAI-compatible `/v1/chat/completions` request/stream against inferrs.
- [snippet_openclaw_gateway_compile_cache_respawn](../../code_snippets/snippet_openclaw_gateway_compile_cache_respawn.md) — process respawn; relevance: the `localService` on-demand process startup (`command`/`args`/`healthUrl`/`readyTimeoutMs`).
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: launching the local inferrs process from the gateway host.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider; relevance: direct analog of a custom (non-bundled) provider entry.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — local/cloud provider plugin; relevance: configuring a self-hosted/OpenAI-compatible backend provider entry (cross-corpus analog).
- [snippet_hermes_agent_model_tools_capability_probe](../../code_snippets/snippet_hermes_agent_model_tools_capability_probe.md) — capability probe; relevance: the smoke-test / capability checks for whether the local model survives full agent turns.

### oc_provider_inworld (9t · 11s · 10d)

**Terms** (9):
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis from text; relevance: Inworld IS a streaming TTS provider — the note's subject.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider integration; relevance: `@openclaw/inworld-speech` is the official installable plugin.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: `INWORLD_API_KEY` HTTP-Basic Base64 credential with the load-bearing "do not re-encode" callout.
- [SSE](../../term_dictionary/term_sse.md) — server-sent streaming; relevance: OpenClaw posts to Inworld's streaming TTS endpoint and concatenates returned base64 audio chunks.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI APIs; relevance: Inworld (`api.inworld.ai`) is an external TTS service.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — request-forwarding intermediary; relevance: the `baseUrl` custom-endpoint override (trailing slashes stripped).
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the reply text Inworld synthesizes originates from an LLM run.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcription; relevance: companion/contrast voice modality on the same telephony/voice-note surfaces Inworld outputs to.
- [Authentication Token](../../term_dictionary/term_oauth_token.md) — issued credential; relevance: the Base64 dashboard credential is sent verbatim as the HTTP-Basic token (not a bearer/OAuth token — explicit contrast).

**Docs** (10):
- [cc_authentication](../claude_code/cc_authentication.md) — Claude Code authentication; relevance: credential/secret-handling analog for the Base64 HTTP-Basic credential.
- [cc_authentication_and_network_errors](../claude_code/cc_authentication_and_network_errors.md) — Claude Code auth/network errors; relevance: debugging the "do not re-encode / not a bearer token" auth-failure class.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — Hermes TTS providers; relevance: direct cross-corpus analog — streaming TTS-provider config + model/voice options.
- [hermes_use_voice_mode_guide](../hermes_agent/hermes_use_voice_mode_guide.md) — Hermes voice-mode guide; relevance: voice-output setup analog where a streaming TTS provider is selected.
- [hermes_voice_mode_cli](../hermes_agent/hermes_voice_mode_cli.md) — Hermes voice-mode CLI; relevance: voice/model config analog (`speakerVoiceId`/`modelId`/`temperature`).
- [hermes_adding_inference_provider](../hermes_agent/hermes_adding_inference_provider.md) — Hermes add-provider; relevance: install-plugin + restart-gateway + key procedure analog.
- [oc_provider_gradium](oc_provider_gradium.md) — sibling streaming-TTS provider (planned, this series); relevance: the other pr04 streaming-TTS provider — same `messages.tts` config shape, reciprocal sibling.
- [oc_tools_tts](oc_tools_tts.md) — shared TTS tool (planned, to0x); relevance: the same Inworld auth callout is mirrored at `/tools/tts#inworld-primary`.
- [oc_tools_media_overview](oc_tools_media_overview.md) — media overview (planned, to0x); relevance: where streaming TTS sits among OpenClaw media tools.
- [oc_concepts_model_providers](oc_concepts_model_providers.md) — provider/model layer (planned, co04); relevance: the provider-selection framework Inworld registers into.

**Repos** (4): [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — speech-provider extensions; relevance: home of the Inworld speech plugin (`speechProviders` contract). · [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — telephony/voice surfaces; relevance: consumes Inworld's MP3/OGG_OPUS/PCM 22050 Hz output. · [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework; relevance: the plugin-install framework Inworld ships through. · [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — Hermes provider adapters; relevance: analog streaming-speech adapter.

**Snippets** (11):
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS provider; relevance: nearly identical streaming-TTS provider shape (key, voice, model, surface output) to Inworld.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — MLX TTS; relevance: another speech-provider feeding the reply-audio pipeline.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the standard reply-audio pipeline Inworld hands its concatenated buffer to.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — media-stream audio; relevance: PCM 22050 Hz telephony output fed to the bridge.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — media-stream transcription; relevance: companion telephony media-stream path on the same Voice Call surface.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: telephony surface consuming Inworld PCM output.
- [snippet_openclaw_gateway_call_credentials_secrets](../../code_snippets/snippet_openclaw_gateway_call_credentials_secrets.md) — call credentials/secrets; relevance: resolving the Base64 dashboard credential / `INWORLD_API_KEY` fallback.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential precedence; relevance: `apiKey` config → `INWORLD_API_KEY` env fallback.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: making `INWORLD_API_KEY` visible to the gateway.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: provider routing/auto-select analog among configured TTS providers.
- [snippet_hermes_agent_cli_voice](../../code_snippets/snippet_hermes_agent_cli_voice.md) — CLI voice config; relevance: voice/model selection analog.

### oc_provider_kilocode (10t · 11s · 11d)

**Terms** (10):
- [API Gateway](../../term_dictionary/term_api_gateway.md) — single-entry request router; relevance: Kilo Gateway IS a unified API routing many models behind one endpoint/key.
- [Model Router](../../term_dictionary/term_model_router.md) — selects model per request; relevance: `kilocode/kilo/auto` is a provider-owned smart-routing model.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the many routed upstream models (Anthropic, OpenAI, Google via Kilo).
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible API; relevance: Kilo is OpenAI-compatible (OpenAI SDKs work by switching base URL).
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — request-forwarding intermediary; relevance: documented as OpenRouter-compatible proxy-style transport (Bearer token under the hood).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI APIs; relevance: Kilo Gateway is an external aggregator service.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — model registry; relevance: dynamic discovery via GET `/models` merged ahead of a static fallback catalog.
- [Authentication](../../term_dictionary/term_authentication.md) — credential verification; relevance: `KILOCODE_API_KEY` auth (onboarding / env / daemon).
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — intermediate reasoning; relevance: proxy-reasoning normalization + the `kilocode/kilo/auto` "skips reasoning injection" caveat.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic model family; relevance: `kilocode/anthropic/claude-sonnet-4` is a catalog ref + the recommended concrete-ref for reasoning support.

**Docs** (11):
- [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — Claude Code LLM gateway; relevance: LLM-gateway base-URL provider config analog (single key, many models).
- [cc_proxy_and_gateway_config](../claude_code/cc_proxy_and_gateway_config.md) — Claude Code proxy/gateway config; relevance: the proxy-style OpenAI-compatible transport analog.
- [cc_fallback_models](../claude_code/cc_fallback_models.md) — Claude Code fallback models; relevance: dynamic-discovery + static-fallback-catalog behavior analog.
- [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — Claude Code LiteLLM gateway; relevance: OpenRouter/LiteLLM-style proxy gateway analog Kilo is documented against.
- [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — Hermes provider routing; relevance: cross-corpus smart-routing-across-models analog for `kilo/auto`.
- [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — Hermes routing proxies; relevance: proxy-based routing/aggregator transport analog.
- [pi_model_overrides_compat](../pi/pi_model_overrides_compat.md) — pi model overrides/compat; relevance: OpenRouter/aggregator routing-preference + reasoning-compat analog.
- [oc_provider_huggingface](oc_provider_huggingface.md) — sibling unified-router provider (planned, this series); relevance: another single-key multi-model router.
- [oc_provider_groq](oc_provider_groq.md) — sibling OpenAI-compatible provider (planned, this series); relevance: same `openai-completions` provider cluster.
- [oc_concepts_model_providers](oc_concepts_model_providers.md) — provider/model layer (planned, co04); relevance: the provider/failover layer Kilo plugs into.
- [oc_tools_thinking](oc_tools_thinking.md) — shared thinking tool (planned, to0x); relevance: the reasoning/`/think` controls the proxy-reasoning caveat references.


**Snippets** (11):
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: only/order/price aggregator routing = the Kilo unified-gateway / OpenRouter-compatible pattern.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — OpenRouter/LiteLLM pricing; relevance: the OpenRouter-compatible proxy pricing/transport layer.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider entry; relevance: the OpenAI-compatible provider-entry pattern Kilo uses.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — discovery normalization; relevance: GET `api.kilo.ai/.../models` discovery → normalized catalog.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest planner; relevance: merging discovered models ahead of the static fallback catalog (`kilocode/kilo/auto`).
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model-catalog assembly; relevance: how `/models kilocode` resolves the account's available models.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: static fallback to `kilocode/kilo/auto` when discovery fails at startup.
- [snippet_openclaw_gateway_openai_http_sse_stream](../../code_snippets/snippet_openclaw_gateway_openai_http_sse_stream.md) — OpenAI HTTP SSE stream; relevance: Kilo's shared stream wrapper normalizing proxy reasoning payloads on the OpenAI-compatible stream.
- [snippet_openclaw_gateway_runtime_env](../../code_snippets/snippet_openclaw_gateway_runtime_env.md) — gateway runtime env; relevance: the daemon `KILOCODE_API_KEY` availability callout.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter provider; relevance: direct cross-corpus analog of an OpenRouter-compatible aggregator provider.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: provider-registration analog for the kilocode plugin.

## Undigested Terms Plan

Per the master's corpus-wide decision: OpenClaw provider vocabulary is documented as `oc_` doc notes (these 8), NOT promoted to new `term_dictionary` entries; the only `term_dictionary` interaction is **linking existing** terms.

| Term (appears in source) | Disposition |
|---|---|
| Google / Gemini, Gemini CLI, Gemini Live API, Veo, Lyria, Gemma | Documented in `oc_provider_google_chat` / `oc_provider_google_media_voice`; link existing `term_llm`. `term_gemini`/`term_gemma` confirmed MISSING — NOT promoted (provider/model names, not cross-cutting reusable concepts). |
| Gradium, Inworld (TTS providers) | Documented in their `oc_provider_*` notes; link existing `term_text_to_speech`. |
| Groq, LPU, Whisper transcription | Documented in `oc_provider_groq`; link `term_llm` / `term_openai_responses_api`. `term_whisper`/`term_lpu` confirmed MISSING — NOT promoted (vendor/hardware names). |
| Hugging Face Inference Providers, Hub-style refs, `:fastest`/`:cheapest` | Documented in `oc_provider_huggingface`; link existing `term_huggingface` (EXISTS) + `term_api_gateway`. |
| Inferrs, `requiresStringContent`, `supportsTools`, `localService` | Documented in `oc_provider_inferrs`; link existing `term_vllm` / `term_openai_responses_api`. |
| Kilo Gateway, `kilocode/kilo/auto`, smart routing, OpenRouter-compatible | Documented in `oc_provider_kilocode`; link existing `term_api_gateway` / `term_model_router`. `term_kilocode` confirmed MISSING — NOT promoted (product name). |
| OpenAI-compatible (`openai-completions`), `reasoning_effort`, `thinkingLevel`/`thinkingBudget` | Config vocabulary; documented inline in the relevant notes; link existing `term_openai_responses_api` / `term_chain_of_thought`. |
| API key / OAuth / env var / HTTP Basic credential | Link existing `term_authentication` / `term_oauth` / `term_oauth_token`. |

**New `term_dictionary` captures from pr04: 0 (expected).** No genuinely cross-cutting, vault-reusable term with no existing note and no doc-page home appears in these 7 provider pages — all new vocabulary is provider/product/model/config-flag names owned by their `oc_provider_*` doc notes. Augment Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** pr04 authors zero `term_dictionary` notes (inherited from master). If augment's Step 2d re-scan surfaces a genuinely reusable cross-cutting term with no existing note and no doc-page home (not expected), it would be captured via `/tessellum-capture-term-note` and added to its best-fit `acronym_glossary_*.md` (the agentic/LLM glossary, e.g. `acronym_glossary_ai.md`) per master W5 — but no such term is anticipated.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (8 notes, P2). Gate table identical to the master's 9-GATE; all must pass before commit.

| Gate | Check | Tool / Method | Pass criterion |
|---|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` | YAML field order + body H2 (`## Overview` … `## Related Notes` … `## References`) + footer; 0 ERROR/LINK-003 |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/providers/<page>.md` | No hallucinated config keys/env vars/model refs; every claim traceable to source |
| G3 | Density + Coverage | `wc -w` (body) + `grep -c '^\`\`\`'`/2 | Each note ≤2,500w, ≤6 code fences, ≤400 lines, single `building_block`; every source H2/H3 mapped |
| G4 | Cross-Reference | per-note `## Related Notes` | ≥8 term links + ≥10 snippets + ≥10 docs (≥5 existing) + repos/siblings per the LOCKED mapping, each with a relevance statement |
| G5 | Ghost-reference | detect + redirect | 0 links to non-existent notes (planned `oc_*` siblings + co04/to0x/gw0x noted) |
| G6 | Broken-link | `/tessellum-fix-broken-links` | 0 broken links after incremental reindex |
| G7 | Discoverability | inbound link from outside `documentation/openclaw/` | Each note RECEIVES ≥1 inbound link (via `entry_openclaw_docs.md` + repo/term inlinks) |
| G8 | In-degree ≥1 | `note_links` query | Anti-island: in_degree ≥1 for every new note |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
# Run from repo root.
OC=the vault/resources/documentation/openclaw
GATE_DIR=resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_provider_google_chat oc_provider_google_media_voice oc_provider_gradium oc_provider_groq oc_provider_huggingface oc_provider_inferrs oc_provider_inworld oc_provider_kilocode"

for n in ${=NOTES}; do
  f="$OC/$n.md"
  # G1 format + broken-link class
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  for sec in "## Overview" "## Related Notes"; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION ($sec): $n"
  done
  # source_url present in frontmatter
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"; }
  # at least one sibling/cross-link with the oc_ prefix in Related Notes
  grep -qE "\(${SIBLING_PREFIX}[a-z0-9_]+\.md\)" "$f" || echo "NO SIBLING ${SIBLING_PREFIX}* LINK: $n"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
done

# YAML frontmatter sweep over the whole openclaw folder
python3 scripts/check_yaml_frontmatter.py --path "$OC"
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_provider_google_chat | procedure | 650 | 4 | ✅ |
| 2 | oc_provider_google_media_voice | procedure | 650 | 3 | ✅ |
| 3 | oc_provider_gradium | procedure | 450 | 3 | ✅ |
| 4 | oc_provider_groq | procedure | 550 | 3 | ✅ |
| 5 | oc_provider_huggingface | procedure | 600 | 2 | ✅ |
| 6 | oc_provider_inferrs | procedure | 600 | 3 | ✅ |
| 7 | oc_provider_inworld | procedure | 450 | 1 | ✅ |
| 8 | oc_provider_kilocode | procedure | 500 | 2 | ✅ |

No note approaches caps (≤650w vs 2,500w; ≤4 fences vs 6). The only multi-fence source (`google.md`, 7 fences) is split so notes 1/2 stay ≤4 each. Hugging Face's 5 advanced config examples are reproduced selectively (representative subset, ≤2 fences kept verbatim).

## Entry Point Decision (inherited from master)

Contributes **8 rows** to `entry_openclaw_docs.md` (created as a master pre-step, W1) under the **Providers** section (pr04 cluster). Each note receives its entry-point back-link at finalization (the primary G7/G8 inbound-link source). No per-sub-plan entry point is created (master = 105 sub-plans / ~1,053 notes ⇒ single shared `entry_openclaw_docs.md`).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution):
- `entry_openclaw_docs.md` (master pre-step) → all 8 notes (primary anti-island source).
- `repo_openclaw_extensions_llm_providers` → notes 1, 4, 5, 6, 8 (chat/inference provider extensions).
- `repo_openclaw_extensions_voice_speech` → notes 2, 3, 7 (Google media/voice, Gradium, Inworld speech providers).
- `repo_openclaw_channels_voice_phone` → notes 2, 7 (realtime voice / telephony TTS consumers).
- `term_huggingface` → note 5; `term_text_to_speech` → notes 2, 3, 7; `term_api_gateway` → notes 5, 8; `term_model_router` → note 8; `term_openai_responses_api` → notes 4, 5, 6, 8; `term_llm` → all 8.
- Sibling intra-series reciprocal inlinks: `oc_provider_google_chat` ↔ `oc_provider_google_media_voice`; `oc_provider_gradium` ↔ `oc_provider_inworld`; `oc_provider_groq` ↔ `oc_provider_huggingface` ↔ `oc_provider_kilocode` (OpenAI-compatible / gateway cluster).

## Pacing Rules (inherited from master)

Single execution phase, 8 notes (well under the ~30-agent fan-out cap). Re-read each source page; reproduce config snippets verbatim and selectively (≤6 fences/note). One `building_block` (procedure) per note. Run all 8 gates before commit. `git pull --rebase --autostash origin main` first; no Claude co-author trailer; reindex incrementally and verify `note_links` + 0 broken links before `git commit` + `git push origin main` (one indivisible cycle).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)



**Per-note locked counts (terms · snippets · docs [existing/planned] · repos):**

| Note | Terms | Snippets | Docs (exist/planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_provider_google_chat | 10 | 12 | 11 (8/3) | 4 | ✅ |
| oc_provider_google_media_voice | 10 | 12 | 11 (7/4) | 4 | ✅ |
| oc_provider_gradium | 8 | 10 | 10 (6/4) | 4 | ✅ |
| oc_provider_groq | 10 | 12 | 11 (7/4) | 4 | ✅ |
| oc_provider_huggingface | 10 | 11 | 11 (8/3) | 4 | ✅ |
| oc_provider_inferrs | 10 | 11 | 11 (8/3) | 4 | ✅ |
| oc_provider_inworld | 9 | 11 | 10 (6/4) | 4 | ✅ |
| oc_provider_kilocode | 10 | 11 | 11 (7/4) | 4 | ✅ |

**New-term candidates:** none. The Step-2d re-scan of all 7 pages surfaced no genuinely cross-cutting, vault-reusable term lacking both an existing note and a doc-page home — all new vocabulary is provider/product/model/config-flag names (Gemini, Veo, Lyria, Gemma, Gradium, Inworld, Groq, LPU, Whisper, Hugging Face Inference Providers, Inferrs, `requiresStringContent`/`supportsTools`/`localService`, Kilo Gateway, `kilocode/kilo/auto`, OpenAI-compatible / `reasoning_effort` / `thinkingLevel`) owned by their `oc_provider_*` doc notes. `term_dictionary` interaction is link-only. The previously-MISSING terms (`term_gemini`, `term_whisper`, `term_tts`, `term_kilocode`, `term_llama`, `term_gemma`, `term_grok`, `term_lpu`, `term_grounding`, `term_byok`, `term_local_model`) remain correctly NOT promoted. Best-fit glossary IF any future term were promoted: `acronym_glossary_ai.md` (agentic/LLM glossary) per master W5 — but **0 expected and 0 found**.

**Augment-discovered relevance upgrades (vs prior candidate pool):** added strongly-relevant existing terms not in the original pool — `term_pkce` (Gemini CLI PKCE OAuth), `term_speech_to_text` (Groq Whisper / TTS-companion modality), `term_multimodal` + `term_diffusion_model` (Google media/voice generation), `term_mcp`/`term_acp_agent_client_protocol` available but not over-cited. Added the rich `hermes_agent/hermes_*` provider-doc corpus (`hermes_provider_google_gemini`, `hermes_adding_inference_provider`, `hermes_inference_providers_cloud`, `hermes_local_self_hosted_llm`, `hermes_tts_providers`, `hermes_use_voice_mode_guide`, `hermes_provider_routing*`, `hermes_fallback_providers`) and `cc_prompt_caching_mechanism` to meet the 10-doc floor with ≥5 existing docs per note.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table present (G1–G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` has all 8 rows (G1 format, G2 grounding, G3 density+coverage, G4 cross-ref updated to the raised floor, G5 ghost, G6 broken-link, G7 discoverability, G8 in-degree). |
| CP3 | Entry point inherited (`entry_openclaw_docs` planned at W1) | **PASS** | `## Entry Point Decision` + `## Inlinks` cite `entry_openclaw_docs.md` (master pre-step W1) as the primary anti-island source contributing 8 rows; size-decision inherited from master (>30-note corpus ⇒ dedicated entry point CREATED at master level). |
| CP4 | Plan size (≤30 or split) | **PASS** | 8 planned notes — well under 30; single execution phase. |
| CP5 | Note format derived (not invented) | **PASS** | Master Format Definition matches existing `claude_code/cc_google_vertex_ai.md` exactly (YAML field order `tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group`; `## Overview` opener; source-mirrored H2; `## Related Notes`). openclaw/ folder empty ⇒ derived from the sibling `cc_*`/`pi_*` doc corpora per master. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: all 8 notes ≤650w / ≤4 fences (caps 2,500w / 6 fences); google's 1,810w + 7 fences resolved by the planned chat vs media-voice split; no remaining borderline note. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured all 7 pages 2026-06-21 (body, frontmatter-stripped): google 1,810 / gradium 482 / groq 774 / huggingface 1,039 / inferrs 896 / inworld 525 / kilocode 573 — all within ±10% of the plan's Source table; no >1.5× under-estimate. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements + authoring reqs | **PASS** | `## Undigested Terms Plan` present (8 disposition rows, all link-existing); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, inherited capture-term-note canonical referenced for the not-expected case). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks` maps ≥1 outside-folder inbound link to every new note (`entry_openclaw_docs` → all 8; `repo_openclaw_extensions_llm_providers` → 1/4/5/6/8; `repo_openclaw_extensions_voice_speech` → 2/3/7; term inlinks; intra-series reciprocal sibling inlinks); G7+G8 are in the gate table as gated execution phases. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
