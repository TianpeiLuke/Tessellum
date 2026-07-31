---
title: Sub-Plan pr09 — OpenClaw Docs: Providers (vLLM, Volcengine, Vydra, xAI, Xiaomi, Z.AI)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["providers/vllm", "providers/volcengine", "providers/vydra", "providers/xai", "providers/xiaomi", "providers/zai"]
---

# Sub-Plan pr09: Providers

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format/YAML, dedup-before-create (term_dictionary + documentation/ + repo_openclaw*), 9-GATE validation, cross-references, and entry-point wiring (`entry_openclaw_docs.md`) are ALL inherited from the master.

## Scope

The final 6 provider integration pages of the OpenClaw docs (the `v*`–`z*` tail): **vLLM** (local OpenAI-compatible server), **Volcengine/Doubao** (Volcano Engine general + coding endpoints + Seed Speech TTS), **Vydra** (image/video/speech media generation), **xAI/Grok** (Grok models via OAuth + full media/search/code-execution surface), **Xiaomi MiMo** (pay-as-you-go + Token Plan + TTS), and **Z.AI/GLM** (GLM model family via API key). All are bundled provider plugins that register a model provider (and, for several, additional speech/image/video contracts) through OpenClaw's shared provider/tool surfaces. **Priority P2 (Phase B — features/integration):** these depend on the conceptual core (`concepts/model-providers`, `gateway/authentication`, `gateway/configuration`) that Phase A digests, and on the existing code-side `repo_openclaw_extensions_llm_providers` / `repo_openclaw_extensions_voice_speech` notes which are LINKED, not recreated.

**Source**: OpenClaw docs, 6 pages, 6,481 measured words. **Planned: 7 notes** (xai.md splits 2-way; all others 1 note each).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| vLLM | providers/vllm | 1,428 | 17 | 6 | 0 | procedure |
| Volcengine (Doubao) | providers/volcengine | 832 | 7 | 6 | 0 | procedure |
| Vydra | providers/vydra | 577 | 7 | 3 | 0 | procedure |
| xAI | providers/xai | 2,562 | 17 | 7 | 2 | procedure + model (SPLIT) |
| Xiaomi MiMo | providers/xiaomi | 1,205 | 8 | 7 | 0 | procedure |
| Z.AI | providers/zai | 877 | 8 | 6 | 0 | procedure |

(Code = ``` fence pairs = raw fence count / 2. The `## Related` H2 on every page is a CardGroup of doc cross-links, not body content — it maps to the digest note's `## Related Notes`, not a body section.)

## Content Strategy

- **Prioritize**: the provider-setup task path that every run depends on — auth env var / onboarding choice, provider id(s), base URL, default model ref, and `openclaw models list --provider <id>` verification — plus the bundled built-in model catalog for each provider. For xAI, prioritize the OAuth-vs-API-key-vs-device-code setup decision (the recommended path) and the feature-coverage matrix that tells a reader which xAI capabilities OpenClaw actually exposes.
- **Split**: only `xai.md` (2,562w > 2,500w cap, mixed BB). Note 4 (`oc_providers_xai_setup`, procedure) covers the setup paths, OAuth troubleshooting, and built-in chat-model catalog; note 5 (`oc_providers_xai_features`, model) covers the feature-coverage matrix, fast-mode/legacy-alias mappings, and the per-capability media/search/code-execution config (web_search, x_search, code_execution, image/video, TTS, batch + streaming STT). All other pages are single-BB procedures well under caps → 1 note each.
- **Link-out (do NOT duplicate)**: shared media tool semantics (`tools/image-generation`, `tools/video-generation`) → link to those pages' future notes / the existing OpenClaw media snippets; shared model-selection/failover (`concepts/model-providers`) → Phase A note (linked, not redefined); gateway auth + config schema (`gateway/authentication`, `gateway/configuration`, `gateway/configuration-reference`) → Phase A notes; provider/model vocabulary (`term_llm`, `term_claude`, `term_qwen`, `term_deepseek`, `term_text_to_speech`, `term_voice_call`, `term_vllm`, `term_provider_plugin`) → link existing terms, never inline a definition.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_providers_vllm.md` | procedure | vllm.md: header table, Getting started, Model discovery (implicit provider), Explicit configuration (manual models), Advanced configuration (proxy-style, Qwen/Nemotron thinking controls, Qwen tool-calls, custom base URL), Troubleshooting | 650 | Running OpenClaw against a local/LAN vLLM server via the `openai-completions` API: `VLLM_API_KEY` auth, implicit model discovery vs explicit manual model config, proxy-style request shaping, Qwen/Nemotron thinking-format controls, tool-call workarounds, and timeout/reachability troubleshooting. |
| 2 | `oc_providers_volcengine.md` | procedure | volcengine.md: header table, Getting started, Providers and endpoints, Built-in catalog (general + coding tabs), Text-to-speech, Advanced configuration | 600 | Configuring the Volcengine (Doubao) provider: a single `VOLCANO_ENGINE_API_KEY` registers both the general `volcengine` and coding `volcengine-plan` endpoints; built-in Doubao/Kimi/GLM/DeepSeek catalog; BytePlus Seed Speech TTS setup (resource id, voice, legacy AppID/token); daemon env-var handling. |
| 3 | `oc_providers_vydra.md` | procedure | vydra.md: header table + www-host warning, Setup, Capabilities (image, video, video live tests, speech) | 500 | Enabling the bundled Vydra media plugin: one `VYDRA_API_KEY` powers image (`vydra/grok-imagine`), video (`vydra/veo3`, `vydra/kling`), and ElevenLabs-backed speech; the `www` base-URL Authorization-drop caveat; per-capability default models, remote-URL constraints, and live-test flags. |
| 4 | `oc_providers_xai_setup.md` | procedure | xai.md: intro + OAuth notes, Choose your setup path (new/existing install, API-key, pick a model), OAuth troubleshooting, Built-in catalog | 650 | Setting up xAI/Grok in OpenClaw: the recommended Grok OAuth path (browser + device-code) vs API-key, new-vs-existing-install flows, `openclaw models auth login` / `models set`, OAuth-callback/device-code troubleshooting, and the bundled Grok chat-model catalog with forward-resolved legacy slugs. |
| 5 | `oc_providers_xai_features.md` | model | xai.md: OpenClaw feature coverage (capability matrix + Fast-mode mappings + Legacy compatibility aliases H3s), Features (web search, video, image, TTS, STT, streaming STT, x_search config, code_execution config, known limits, advanced notes), Live testing | 750 | The xAI capability surface OpenClaw exposes: the capability-to-surface coverage matrix (chat/Responses, web_search, x_search, code_execution, image/video, batch+streaming STT, batch TTS; what is NOT exposed), fast-mode + legacy-alias model remapping tables, and per-capability config schemas (voices, formats, endpoints, WebSocket STT defaults). |
| 6 | `oc_providers_xiaomi.md` | procedure | xiaomi.md: header table, Getting started, Pay-as-you-go catalog, Token Plan catalog, Text-to-speech, Config example (PAYG + Token Plan), advanced accordions (auto-injection, model details, troubleshooting) | 650 | Configuring Xiaomi MiMo: two text presets (`xiaomi` pay-as-you-go `sk-...` keys, `xiaomi-token-plan` `tp-...` keys with cn/sgp/ams regional base URLs), the MiMo V2/V2.5 model catalogs, chat-completions-based TTS (`mimo-v2.5-tts`, voicedesign), key-shape validation, and daemon env-var handling. |
| 7 | `oc_providers_zai.md` | procedure | zai.md: header table, GLM models, Getting started (auto-detect vs explicit regional), Config example, Built-in catalog, Advanced configuration (forward-resolve, tool-call streaming, thinking/preserved thinking, image understanding, auth details) | 600 | Using Z.AI / GLM models: `ZAI_API_KEY` Bearer auth with endpoint auto-detection vs explicit Coding-Plan/general regional onboarding choices, the bundled GLM-5.x/4.x catalog, `/think` level mapping, preserved-thinking opt-in, GLM-5 forward-resolution, and image understanding (`glm-4.6v`). |

## Section Coverage Map

Every source H2/H3 maps to a planned note; the `## Related` CardGroup on each page becomes that note's `## Related Notes` / `## References` (external console URLs), not a body section.

```
vllm.md
├── (intro + header property table) ───────────────────── → note 1 (oc_providers_vllm)
├── ## Getting started ────────────────────────────────── → note 1
├── ## Model discovery (implicit provider) ─────────────── → note 1
├── ## Explicit configuration (manual models) ──────────── → note 1
├── ## Advanced configuration (proxy-style, Qwen thinking,
│   Nemotron thinking, Qwen tool-calls, custom base URL) ─ → note 1
├── ## Troubleshooting (slow/timeout, not reachable,
│   auth errors, no models, tools-as-text) ─────────────── → note 1
└── ## Related (CardGroup) ─────────────────────────────── → note 1 Related Notes / References

volcengine.md
├── (intro + header detail table) ─────────────────────── → note 2 (oc_providers_volcengine)
├── ## Getting started (+ non-interactive Tip) ─────────── → note 2
├── ## Providers and endpoints ─────────────────────────── → note 2
├── ## Built-in catalog (general + coding Tabs) ────────── → note 2
├── ## Text-to-speech (Seed Speech, legacy AppID/token) ── → note 2
├── ## Advanced configuration (default model, picker
│   fallback, daemon env vars) ─────────────────────────── → note 2
└── ## Related (CardGroup) ─────────────────────────────── → note 2 Related Notes

vydra.md
├── (intro + header table + www-host Warning) ─────────── → note 3 (oc_providers_vydra)
├── ## Setup ──────────────────────────────────────────── → note 3
├── ## Capabilities (image, video, video live tests,
│   speech accordions) ─────────────────────────────────── → note 3
└── ## Related (CardGroup) ─────────────────────────────── → note 3 Related Notes

xai.md
├── (intro + OAuth notes) ─────────────────────────────── → note 4 (oc_providers_xai_setup)
├── ## Choose your setup path (new/existing/API-key/pick) → note 4
├── ## OAuth troubleshooting ───────────────────────────── → note 4
├── ## Built-in catalog ────────────────────────────────── → note 4
├── ## OpenClaw feature coverage (capability matrix) ───── → note 5 (oc_providers_xai_features)
│   ├── ### Fast-mode mappings ──────────────────────────── → note 5
│   └── ### Legacy compatibility aliases ────────────────── → note 5
├── ## Features (web search, video, image, TTS, STT,
│   streaming STT, x_search cfg, code_execution cfg,
│   known limits, advanced notes) ──────────────────────── → note 5
├── ## Live testing ────────────────────────────────────── → note 5
└── ## Related (CardGroup) ─────────────────────────────── → notes 4 + 5 Related Notes

xiaomi.md
├── (intro + header property table) ───────────────────── → note 6 (oc_providers_xiaomi)
├── ## Getting started ────────────────────────────────── → note 6
├── ## Pay-as-you-go catalog ───────────────────────────── → note 6
├── ## Token Plan catalog ──────────────────────────────── → note 6
├── ## Text-to-speech ──────────────────────────────────── → note 6
├── ## Config example (PAYG + Token Plan + accordions:
│   auto-injection, model details, troubleshooting) ────── → note 6
└── ## Related (CardGroup) ─────────────────────────────── → note 6 Related Notes

zai.md
├── (intro + header property table) ───────────────────── → note 7 (oc_providers_zai)
├── ## GLM models ─────────────────────────────────────── → note 7
├── ## Getting started (auto-detect + explicit regional) ─ → note 7
├── ## Config example ──────────────────────────────────── → note 7
├── ## Built-in catalog ────────────────────────────────── → note 7
├── ## Advanced configuration (forward-resolve, tool-call
│   streaming, thinking/preserved thinking, image
│   understanding, auth details) ───────────────────────── → note 7
└── ## Related (CardGroup) ─────────────────────────────── → note 7 Related Notes
```

No orphaned sections. Shared media-tool semantics (`tools/image-generation`, `tools/video-generation`), `concepts/model-providers`, and `gateway/*` config pages are linked (their own sub-plans own them), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| xai.md (2,562w, 7 H2 / 2 H3, 17 code fences, mixed BB) | notes 4 (`oc_providers_xai_setup`, procedure) + 5 (`oc_providers_xai_features`, model) | Exceeds the 2,500-word cap AND mixes a setup/auth **procedure** (OAuth/API-key/device-code paths, troubleshooting, chat-model catalog) with a **model**-BB capability reference (feature-coverage matrix, fast-mode/legacy-alias mapping tables, per-capability media/search/code-execution config schemas). Split per word-cap + one-BB-per-note rules; each half lands ≤750w and ≤6 code fences. |

All other pages: **(no split)** — each is a single-BB procedure (vllm 1,428w / volcengine 832w / vydra 577w / xiaomi 1,205w / zai 877w), all under 2,500w. vllm.md has 17 fences but most are short config/CLI snippets clustered in accordions; the digest reproduces ≤6 representative fences (getting-started, explicit config, one thinking-control, one tool-call workaround, troubleshooting) and prose-summarizes the rest to stay ≤6 per note.

## Summary Statistics & Building Block Distribution

- **Source pages:** 6 (6,481 measured words). **New `oc_` notes: 7.** **New `term_dictionary` notes: 0.**
- **BB distribution:** procedure ×6 (notes 1, 2, 3, 4, 6, 7) · model ×1 (note 5, the xAI feature/capability reference).
- **Est. digest words:** ~4,400 (avg ~630/note); each note ≤750w, well under the 2,500w cap.
- **Code fences:** 64 source fence-pairs across the 6 pages distribute across the 7 notes; each note reproduces ≤6 representative config/CLI snippets verbatim and prose-summarizes the rest (vllm and xai are the fence-heavy pages; the xai split + selective reproduction keeps each half ≤6).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)



### oc_providers_vllm (10t · 10s · 10d)

**Terms**
- [vLLM](../../term_dictionary/term_vllm.md) — high-throughput open-source LLM inference server with an OpenAI-compatible API; relevance: THE provider this note configures (`vllm` provider id, `http://127.0.0.1:8000/v1`).
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: vLLM serves open-source/custom LLMs that OpenClaw drives as the agent model.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled plugin that registers a model provider on OpenClaw's shared contract; relevance: `vllm` is exactly such a bundled local-OpenAI provider plugin.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI's request/response API shape; relevance: vLLM connects via the `openai-completions` OpenAI-compatible API — the closest existing OpenAI-API term.
- [Qwen](../../term_dictionary/term_qwen.md) — Alibaba's open model family; relevance: the note's `compat.thinkingFormat: "qwen-chat-template"` and Qwen tool-call workarounds target Qwen models served through vLLM.
- [Nemotron](../../term_dictionary/term_nemotron.md) — NVIDIA's open reasoning model family; relevance: the Nemotron-3 thinking-controls accordion (`enable_thinking`/`force_nonempty_content` chat-template kwargs) is one of the note's two thinking-control sections.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning-trace prompting; relevance: the Qwen/Nemotron `enable_thinking` and `/think off/on` profile controls toggle visible reasoning.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-emitted structured tool calls; relevance: the "Qwen tool calls appear as text" troubleshooting (`tool_choice: "required"`, parser/template) is a function-calling compat workaround.
- [Context Window](../../term_dictionary/term_context_window.md) — max input+output tokens; relevance: explicit config pins `contextWindow`/`maxTokens` per manual model row.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — request-forwarding intermediary; relevance: vLLM is treated as a proxy-style OpenAI-compatible `/v1` backend (no native OpenAI request shaping / attribution headers).

**Docs**
- [Hermes: Local / Self-Hosted LLM](../hermes_agent/hermes_local_self_hosted_llm.md) — running Hermes against a local/self-hosted LLM endpoint; relevance: direct existing analog of vLLM-as-local-provider, same loopback/LAN topology.
- [Hermes: Provider Ollama Local](../hermes_agent/hermes_provider_ollama_local.md) — local Ollama OpenAI-compatible provider setup; relevance: sibling local-OpenAI-compatible provider pattern (env key + base URL + model id).
- [Hermes: Provider Local LLM (Mac)](../hermes_agent/hermes_provider_local_llm_mac.md) — local-LLM provider config on macOS; relevance: same local-server-as-provider workflow vLLM uses.
- [Hermes: Docker Tools / Local Inference](../hermes_agent/hermes_docker_tools_local_inference.md) — running a local inference server in Docker; relevance: a common vLLM deployment (host/port/timeout matches the note's custom-base-URL/timeout accordions).
- [Pi: Custom Models](../pi/pi_custom_models.md) — declaring local/custom models in `models.json`; relevance: directly parallels vLLM's explicit manual-model config (id/name/contextWindow/maxTokens).
- [Pi: Model Overrides / Compat](../pi/pi_model_overrides_compat.md) — per-model compat-flag overrides; relevance: analog of vLLM's `compat.thinkingFormat` and `params.extra_body` per-model overrides.
- [CC: Model Selection](../claude_code/cc_model_selection.md) — choosing models/providers + failover; relevance: vLLM `vllm/*` model refs participate in the same selection/failover surface.
- [CC: Environment Variables](../claude_code/cc_environment_variables.md) — env-var-driven provider auth; relevance: parallels the note's `VLLM_API_KEY` opt-in auth signal.
- [oc_providers_xiaomi](oc_providers_xiaomi.md) — sibling OpenAI-compatible provider (this series, planned); relevance: same `openai-completions` API + explicit `baseUrl`/`apiKey`/model-list config pattern.
- [oc_providers_zai](oc_providers_zai.md) — sibling provider with thinking controls (this series, planned); relevance: same `/think` reasoning-control + manifest-catalog mechanics.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — code home of bundled model providers; relevance: implements the `vllm` provider this note documents.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-extension framework; relevance: registers the vLLM plugin on the shared provider contract.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — Hermes provider adapters; relevance: parallel OpenAI-compatible adapter implementation.

**Snippets**
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — localhost OpenAI-compatible provider config; relevance: closest code analog of vLLM's loopback `baseUrl`+`apiKey` setup.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider config; relevance: the `openai-completions` API shape vLLM reuses.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider with custom base URL; relevance: same custom-`baseUrl`/proxy-style provider mechanics.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — generic custom provider registration; relevance: parallels vLLM's explicit `models.providers.vllm` block.
- [snippet_hermes_agent_plugins_provider_ollama_cloud](../../code_snippets/snippet_hermes_agent_plugins_provider_ollama_cloud.md) — Ollama-family provider plugin; relevance: another local-OpenAI-compatible provider analog.
- [snippet_hermes_agent_core_chat_helpers_build_kwargs](../../code_snippets/snippet_hermes_agent_core_chat_helpers_build_kwargs.md) — per-model thinking/tool kwargs assembly; relevance: exactly the `chat_template_kwargs`/`extra_body` mapping vLLM thinking-controls use.
- [snippet_hermes_agent_core_lmstudio_reasoning](../../code_snippets/snippet_hermes_agent_core_lmstudio_reasoning.md) — reasoning-control on a local provider; relevance: analog of vLLM Qwen/Nemotron `enable_thinking` handling.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — `/models` discovery normalization; relevance: implements vLLM implicit model discovery (`GET /v1/models` → entries).
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest-vs-runtime catalog planning; relevance: governs the `"vllm/*": {}` wildcard catalog inclusion.
- [snippet_openclaw_gateway_session_utils_model_fallback](../../code_snippets/snippet_openclaw_gateway_session_utils_model_fallback.md) — model fallback at session level; relevance: how a misconfigured/unreachable vLLM model fails over (the troubleshooting section's concern).

**Entry**

### oc_providers_volcengine (10t · 10s · 10d)

**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Volcengine serves Doubao/third-party LLMs to the agent.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider plugin; relevance: a single bundled plugin registers BOTH `volcengine` and `volcengine-plan` provider ids from one key.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible API shape; relevance: the Doubao model endpoints are OpenAI-compatible.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesizing speech from text; relevance: the same plugin registers BytePlus Seed Speech TTS (`messages.tts.provider: "volcengine"`).
- [Voice Call](../../term_dictionary/term_voice_call.md) — voice/telephony channel; relevance: for voice-note targets OpenClaw requests provider-native `ogg_opus` from Seed Speech.
- [DeepSeek](../../term_dictionary/term_deepseek.md) — DeepSeek model family; relevance: `volcengine/deepseek-v3-2-251201` is in the general catalog.
- [MoE](../../term_dictionary/term_moe.md) — mixture-of-experts architecture; relevance: the catalog's Kimi K2.5 / DeepSeek V3.2 / GLM 4.7 are MoE-class models (the candidate-stage `term_kimi` gap is covered by these existing model terms).
- [Context Window](../../term_dictionary/term_context_window.md) — max tokens; relevance: the catalog tables list per-model 128K–256K context sizes.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/auth mechanics; relevance: model key (`VOLCANO_ENGINE_API_KEY`) is deliberately separate from the TTS key (`VOLCENGINE_TTS_API_KEY`).
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — stored credential profile; relevance: onboarding (`--auth-choice volcengine-api-key`) writes the auth profile that registers both providers.

**Docs**
- [Hermes: TTS Providers](../hermes_agent/hermes_tts_providers.md) — configuring TTS provider backends; relevance: direct analog of the Seed Speech TTS provider registration + voice/format selection.
- [Hermes: Model Aux Provider Config](../hermes_agent/hermes_model_aux_provider_config.md) — auxiliary provider config (model + speech); relevance: parallels Volcengine registering a model provider plus an aux TTS provider from one plugin.
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider setup; relevance: same cloud-hosted OpenAI-compatible provider onboarding.
- [Hermes: Provider Routing / Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — routing among general/coding endpoints; relevance: mirrors the `volcengine` (general) vs `volcengine-plan` (coding) endpoint split.
- [Hermes: Env Vars (Providers/Auth/Tools)](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — env-var inventory for provider auth; relevance: the daemon-env-var accordion (`VOLCANO_ENGINE_API_KEY`, `VOLCENGINE_TTS_*`) is the same concern.
- [CC: Model Selection](../claude_code/cc_model_selection.md) — model/provider selection + failover; relevance: the model-picker fallback behavior for `volcengine/*`+`volcengine-plan/*` rows.
- [CC: Environment Variables](../claude_code/cc_environment_variables.md) — env-var auth; relevance: parallels separate model vs TTS env keys.
- [oc_providers_xiaomi](oc_providers_xiaomi.md) — sibling provider with separate TTS (this series, planned); relevance: same "one plugin registers a text provider + a speech provider" shape.
- [oc_providers_vydra](oc_providers_vydra.md) — sibling media/TTS provider (this series, planned); relevance: shared media-key + speech-route mechanics.
- [oc_providers_zai](oc_providers_zai.md) — GLM sibling provider (this series, planned); relevance: GLM 4.7 appears in both catalogs; same Bearer/OpenAI-compatible onboarding.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled model providers; relevance: implements the `volcengine`/`volcengine-plan` model providers.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension code; relevance: implements the Seed Speech TTS provider the same plugin registers.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-extension framework; relevance: registers the Volcengine plugin.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — Hermes provider adapters; relevance: parallel OpenAI-compatible provider adapter.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider config; relevance: the Doubao endpoint shape Volcengine reuses.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — bundled TTS provider registration; relevance: direct analog of the Seed Speech TTS provider block (`messages.tts.providers`).
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech-provider pipeline; relevance: parallels Seed Speech voice/format/`ogg_opus` selection.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — another bundled TTS provider; relevance: sibling TTS-provider registration pattern.
- [snippet_hermes_agent_plugins_provider_kimi_coding](../../code_snippets/snippet_hermes_agent_plugins_provider_kimi_coding.md) — coding-endpoint provider plugin; relevance: direct analog of the `volcengine-plan` coding endpoint (and Kimi K2 coding rows).
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing logic; relevance: how OpenClaw picks `volcengine`/`bytedance`/`doubao` speech aliases.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — manifest catalog normalization; relevance: the built-in general+coding catalog tables come from the manifest.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing/alias resolution; relevance: resolves the catalog model refs and the `bytedance`/`doubao` provider aliases.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution order; relevance: how the single API key resolves to both registered providers.
- [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — CLI model-switch entry; relevance: analog of `openclaw models set`/default-model selection after onboarding.

**Entry**

### oc_providers_vydra (10t · 10s · 10d)

**Terms**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled plugin registering contracts; relevance: one bundled `vydra` plugin (`enabledByDefault: true`) registers three contracts (image/video/speech).
- [Multimodal](../../term_dictionary/term_multimodal.md) — across image/video/audio modalities; relevance: Vydra is purely a media plugin (image `grok-imagine`, video `veo3`/`kling`, speech) — covers the candidate-stage `term_image_generation` gap.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: Vydra's ElevenLabs-backed `speechProviders` route (default `elevenlabs/tts`, voice `21m00...`).
- [Voice Call](../../term_dictionary/term_voice_call.md) — voice delivery channel; relevance: the speech route feeds voice-note/voice-call delivery.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/auth; relevance: one `VYDRA_API_KEY` powers all three capabilities.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — host redirect/forwarding; relevance: the `www` vs apex `Authorization`-drop cross-host redirect caveat is the headline warning.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the underlying `grok-imagine`/`veo3` generation models are LLM-family media models.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of provider models; relevance: per-capability default models (`vydra/grok-imagine`, `vydra/veo3`, `vydra/kling`) are catalog entries.
- [Model Router](../../term_dictionary/term_model_router.md) — selects model per request; relevance: setting `imageGenerationModel`/`videoGenerationModel.primary` routes media requests to Vydra.
- [Failover](../../term_dictionary/term_failover.md) — fallback on provider failure; relevance: the linked shared image/video tools handle provider selection + failover around Vydra.

**Docs**
- [Hermes: Image Generation](../hermes_agent/hermes_image_generation.md) — image-generation tool/provider; relevance: direct analog of Vydra's `image_generate` registration + remote-URL constraints.
- [Hermes: Video Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-generation provider plugin; relevance: exact analog of Vydra's `videoGenerationProviders` (text-to-video + image-to-video).
- [Hermes: TTS Providers](../hermes_agent/hermes_tts_providers.md) — TTS provider config; relevance: Vydra's ElevenLabs-backed speech provider block matches this shape.
- [Hermes: Tools Reference (Platform Media)](../hermes_agent/hermes_tools_reference_platform_media.md) — shared media tool parameters; relevance: the note link-outs to shared image/video tools for parameters/failover.
- [Hermes: Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media delivery to channels; relevance: how generated MP3/image/video is delivered through channel attachments.
- [CC: Model Selection](../claude_code/cc_model_selection.md) — provider/model selection + failover; relevance: per-capability default-provider selection around Vydra.
- [CC: Voice Dictation](../claude_code/cc_voice_dictation.md) — voice/speech feature in a coding agent; relevance: closest CC analog to the speech-synthesis route.
- [oc_providers_xai_features](oc_providers_xai_features.md) — sibling image/video/TTS surface (this series, planned); relevance: xAI exposes the SAME shared `image_generate`/`video_generate`/`tts` contracts Vydra registers.
- [oc_providers_volcengine](oc_providers_volcengine.md) — sibling provider TTS (this series, planned); relevance: shared media-key + speech-route mechanics.
- [oc_providers_xiaomi](oc_providers_xiaomi.md) — sibling TTS provider (this series, planned); relevance: another bundled speech-provider registration analog.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-plugin framework with `enabledByDefault`; relevance: Vydra is bundled and enabled by default.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension code; relevance: implements Vydra's `speechProviders` contract.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled providers; relevance: image/video generation providers live in the same extension layer.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel delivery layer; relevance: generated media (MP3/image/video) is delivered to channels.

**Snippets**
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS provider; relevance: EXACTLY Vydra's speech backing (`elevenlabs/tts`, voice `21m00Tcm4TlvDq8ikWAM`).
- [snippet_openclaw_gateway_managed_image_record_lifecycle](../../code_snippets/snippet_openclaw_gateway_managed_image_record_lifecycle.md) — generated-image storage/lifecycle; relevance: how Vydra's text-to-image output is stored/recorded.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — generated-image validation; relevance: validates Vydra image outputs before delivery.
- [snippet_openclaw_gateway_chat_transcript_media_pipeline](../../code_snippets/snippet_openclaw_gateway_chat_transcript_media_pipeline.md) — media attachment pipeline; relevance: the delivery path for Vydra image/video/audio.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — bundled TTS provider; relevance: sibling speech-provider registration analog.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-generation dispatch; relevance: parallels Vydra `image_generate` provider dispatch.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-generation dispatch; relevance: parallels Vydra `veo3`/`kling` video dispatch + remote-URL handling.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-gen tool surface; relevance: the shared `image_generate` tool Vydra plugs into.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-gen tool surface; relevance: the shared `video_generate` tool Vydra plugs into.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitize/validate; relevance: generated media is sanitized before channel delivery.

**Entry**

### oc_providers_xai_setup (10t · 10s · 10d)

**Terms**
- [OAuth](../../term_dictionary/term_oauth.md) — delegated-authorization protocol; relevance: the recommended Grok setup path is Grok OAuth (browser + device-code).
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — bearer token from an OAuth flow; relevance: xAI decides which accounts can receive OAuth API tokens (eligibility note).
- [PKCE](../../term_dictionary/term_pkce.md) — proof-key-for-code-exchange OAuth extension; relevance: the browser/`127.0.0.1:56121`-callback + device-code flows are PKCE-style OAuth.
- [Authentication](../../term_dictionary/term_authentication.md) — credential mechanics; relevance: the note's core decision is OAuth vs API-key vs device-code auth.
- [Auth Profile](../../term_dictionary/term_auth_profile.md) — stored credential profile; relevance: `openclaw models auth list --provider xai` inspects saved xAI auth profiles.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider plugin; relevance: `xai` is a bundled Grok provider plugin.
- [xAI](../../term_dictionary/term_xai.md) — Elon Musk's AI lab / Grok maker; relevance: THIS provider — the note configures xAI/Grok in OpenClaw.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Grok chat models are the LLMs this provider serves.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: the subscription-vs-API-key auth model parallels Claude Max/subscription auth (cross-provider analog).
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model registry; relevance: the built-in Grok chat catalog (Grok 4.3, Grok Build 0.1, 4.20 beta) with forward-resolved legacy slugs.

**Docs**
- [Hermes: Provider xAI Grok OAuth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — Hermes xAI/Grok OAuth setup; relevance: the closest existing analog — same Grok OAuth/device-code/API-key paths.
- [Pi: Provider Auth](../pi/pi_provider_auth.md) — subscription-login vs API-key resolution; relevance: direct analog of the OAuth-vs-key resolution this note documents.
- [CC: Authentication and Network Errors](../claude_code/cc_authentication_and_network_errors.md) — auth + callback/network failure handling; relevance: parallels the OAuth-callback (`127.0.0.1:56121` unreachable) troubleshooting.
- [Hermes: Provider Minimax OAuth](../hermes_agent/hermes_provider_minimax_oauth.md) — another provider's OAuth onboarding; relevance: sibling OAuth-provider setup flow.
- [Hermes: Setup with Nous Portal](../hermes_agent/hermes_setup_with_nous_portal.md) — subscription-backed provider login; relevance: subscription-eligibility auth analog (SuperGrok/X Premium gating).
- [Hermes: Nous Portal Subscription](../hermes_agent/hermes_nous_portal_subscription.md) — subscription credential model; relevance: parallels OAuth-token eligibility tied to a subscription.
- [Hermes: Credential Pools](../hermes_agent/hermes_credential_pools.md) — credential storage/resolution; relevance: how the OAuth/key credential is stored and reused (incl. webSearch fallback key).
- [CC: Model Selection](../claude_code/cc_model_selection.md) — making a model the default; relevance: `openclaw models set xai/grok-4.3` after sign-in.
- [oc_providers_xai_features](oc_providers_xai_features.md) — the feature half of this provider (this series, planned); relevance: the same credential powers the media/search/code-exec surface documented there.
- [oc_providers_zai](oc_providers_zai.md) — sibling provider (this series, planned); relevance: another bundled provider with regional/auto-detect onboarding choices.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled model providers; relevance: implements the bundled `xai` model provider.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-extension framework; relevance: registers the xAI plugin and its shared OAuth client.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — Hermes CLI; relevance: analogous `models auth login`/device-code OAuth CLI flow.
- [repo_pi_agent_harness_ai](../../../areas/code_repos/repo_pi_agent_harness_ai.md) — Pi agent harness; relevance: subscription-vs-key auth resolution analog.

**Snippets**
- [snippet_hermes_agent_plugins_provider_xai_oauth](../../code_snippets/snippet_hermes_agent_plugins_provider_xai_oauth.md) — xAI OAuth provider wiring; relevance: DIRECT analog — the xAI OAuth provider implementation.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — auth login/logout CLI flow; relevance: parallels `openclaw models auth login/list --provider xai`.
- [snippet_hermes_agent_cli_auth_qwen_oauth](../../code_snippets/snippet_hermes_agent_cli_auth_qwen_oauth.md) — device-code OAuth flow; relevance: the same device-code (URL + short code, remote-poll) pattern xAI uses.
- [snippet_hermes_agent_cli_auth_oauth_callback_server](../../code_snippets/snippet_hermes_agent_cli_auth_oauth_callback_server.md) — localhost OAuth callback server; relevance: exactly the `127.0.0.1:56121` browser-callback path (and why device-code is the fallback).
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential-resolution order; relevance: OAuth → `XAI_API_KEY` → plugin webSearch key fallback chain.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth profile storage/portability; relevance: how saved xAI OAuth profiles persist across the gateway.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — auth-mode helpers; relevance: distinguishing OAuth vs API-key vs device-code modes.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source precedence; relevance: parallels the env-var/config/OAuth credential sources for xAI.
- [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — CLI model-switch; relevance: `openclaw models set xai/grok-4.3` to make Grok the default.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — manifest catalog normalization; relevance: the built-in Grok catalog + legacy/fast-mode slug forward-resolution.

**Entry**

### oc_providers_xai_features (10t · 10s · 10d)

**Terms**
- [Function Calling](../../term_dictionary/term_function_calling.md) — model-emitted tool calls; relevance: `web_search`/`x_search`/`code_execution` are exposed as OpenClaw tools; native xAI requests default `tool_stream: true`.
- [Multimodal](../../term_dictionary/term_multimodal.md) — image/video/audio modalities; relevance: `image_generate` and `video_generate` (covers the candidate-stage `term_image_generation` gap) plus STT/TTS audio.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: batch `/v1/tts` (voices `eve/ara/...`, formats `mp3/wav/pcm/mulaw/alaw`).
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — audio transcription; relevance: batch STT (`grok-stt`, REST `/v1/stt`) via media-understanding.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — live streaming STT; relevance: realtime transcription provider for live voice-call audio.
- [Voice Call](../../term_dictionary/term_voice_call.md) — telephony/voice channel; relevance: streaming STT integrates with Voice Call's Twilio µ-law media stream (`streaming.provider: "xai"`).
- [WebSocket](../../term_dictionary/term_websocket.md) — full-duplex socket protocol; relevance: xAI streaming STT runs over `wss://api.x.ai/v1/stt`.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — Responses API shape; relevance: xAI uses the Responses API as the bundled transport for model/search/code-execution.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning traces; relevance: reasoning vs non-reasoning Grok 4.20 variants + reasoning payload-key stripping.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model registry; relevance: the capability matrix + fast-mode/legacy-alias remap tables map ids onto OpenClaw surfaces.

**Docs**
- [Hermes: x_search (Grok)](../hermes_agent/hermes_x_search_grok.md) — Grok-backed X search tool; relevance: direct analog of the `x_search` tool config (model, baseUrl, citations).
- [Hermes: STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text transcription; relevance: parallels xAI batch + streaming STT registration.
- [Hermes: Image Generation](../hermes_agent/hermes_image_generation.md) — image-gen tool/provider; relevance: parallels `image_generate` (aspect ratios, resolutions, `b64_json`).
- [Hermes: Video Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-gen provider; relevance: parallels `video_generate` (`grok-imagine-video`, modes, durations).
- [Hermes: TTS Providers](../hermes_agent/hermes_tts_providers.md) — TTS provider config; relevance: parallels batch `/v1/tts` voice/format config.
- [Hermes: Voice Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — realtime voice mode; relevance: closest analog to streaming-STT realtime voice-call transcription.
- [Hermes: Tools Reference (Platform Media)](../hermes_agent/hermes_tools_reference_platform_media.md) — shared media tool parameters; relevance: the shared cross-provider image/video controls xAI forwards.
- [CC: Model Selection](../claude_code/cc_model_selection.md) — provider/model selection + failover; relevance: selecting xAI model + media-provider surfaces.
- [oc_providers_xai_setup](oc_providers_xai_setup.md) — the auth/setup half (this series, planned); relevance: same credential powers every capability documented here.
- [oc_providers_vydra](oc_providers_vydra.md) — sibling image/video/TTS provider (this series, planned); relevance: registers the SAME shared `image_generate`/`video_generate`/`tts` contracts.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled providers; relevance: xAI model + `x_search`/`code_execution` tool registration.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension; relevance: implements the TTS/STT contracts xAI registers.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — Voice Call/phone channel; relevance: the consumer of xAI realtime streaming STT (Twilio µ-law frames).
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-extension framework; relevance: registers the xAI plugin and its tools.

**Snippets**
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — realtime streaming STT path; relevance: EXACTLY the xAI WebSocket-STT target (forwards G.711 µ-law frames).
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call media-stream audio; relevance: the µ-law/8000Hz audio frames xAI streaming STT consumes.
- [snippet_openclaw_voice_call_runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: hosts the `streaming.provider: "xai"` transcription path.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — streaming STT provider (Deepgram); relevance: sibling streaming-STT provider analog (same `streaming.providers` shape).
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool surface; relevance: parallels xAI batch STT via `tools.media.audio`.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing; relevance: parallels selecting `xai` as the `messages.tts.provider`.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen dispatch; relevance: parallels xAI `image_generate` (`b64_json`, data-URL refs).
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen dispatch; relevance: parallels xAI `video_generate` (remote-URL edit/extend).
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — generated-image validation; relevance: handles xAI `b64_json` image output before channel delivery.

**Entry**

### oc_providers_xiaomi (10t · 10s · 10d)

**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: MiMo V2/V2.5 are the LLMs this provider serves.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider plugin; relevance: one bundled `xiaomi` plugin registers two text presets (`xiaomi` PAYG + `xiaomi-token-plan`) plus a speech provider.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible API; relevance: both presets use `api: "openai-completions"`.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis; relevance: the `xiaomi` speech provider uses a chat-completions TTS contract (`mimo-v2.5-tts`, voicedesign).
- [Voice Call](../../term_dictionary/term_voice_call.md) — voice-note delivery; relevance: Xiaomi TTS output is transcoded to 48kHz Opus for voice-note targets (Feishu/Telegram).
- [Multimodal](../../term_dictionary/term_multimodal.md) — text+image input; relevance: `mimo-v2-omni`/`mimo-v2.5` accept text+image.
- [Context Window](../../term_dictionary/term_context_window.md) — max tokens; relevance: the catalogs list 262K–1,048,576-token context tiers.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning traces; relevance: the reasoning-enabled rows (`mimo-v2-pro`, `mimo-v2.5*`) — covers the candidate-stage `term_reasoning_model` gap.
- [Authentication](../../term_dictionary/term_authentication.md) — credential mechanics; relevance: `sk-` vs `tp-` key-shape validation warns on wrong-path key entry.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model registry; relevance: the PAYG + Token Plan catalog tables come from the bundled manifest.

**Docs**
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider setup; relevance: same cloud OpenAI-compatible provider onboarding.
- [Hermes: Provider Routing / Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — routing among regional endpoints; relevance: mirrors the cn/sgp/ams Token Plan regional base URLs.
- [Hermes: TTS Providers](../hermes_agent/hermes_tts_providers.md) — TTS provider config; relevance: the Xiaomi speech-provider block (`messages.tts.providers.xiaomi`).
- [Hermes: Model Aux Provider Config](../hermes_agent/hermes_model_aux_provider_config.md) — model + aux speech provider; relevance: parallels Xiaomi registering a text provider plus a TTS provider.
- [Hermes: Env Vars (Providers/Auth/Tools)](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider env-var inventory; relevance: the daemon-env-var troubleshooting (`XIAOMI_API_KEY`, `XIAOMI_TOKEN_PLAN_API_KEY`).
- [CC: Model Selection](../claude_code/cc_model_selection.md) — model/provider selection; relevance: choosing `xiaomi/mimo-v2-flash` vs `xiaomi-token-plan/mimo-v2.5-pro` defaults.
- [Pi: Model Overrides / Compat](../pi/pi_model_overrides_compat.md) — per-model compat; relevance: the note notes pricing/compat come from the manifest (config omits `cost`/`compat`).
- [oc_providers_zai](oc_providers_zai.md) — sibling GLM provider with regional endpoints (this series, planned); relevance: same regional-base-URL onboarding-choice pattern.
- [oc_providers_volcengine](oc_providers_volcengine.md) — sibling provider with separate TTS (this series, planned); relevance: same "text provider + speech provider in one plugin" shape.
- [oc_providers_vllm](oc_providers_vllm.md) — sibling OpenAI-compatible provider (this series, planned); relevance: identical `openai-completions` explicit-config block (id/contextWindow/maxTokens).

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled providers; relevance: implements the `xiaomi`/`xiaomi-token-plan` model providers.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension; relevance: implements the Xiaomi speech (TTS) provider.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-extension framework; relevance: the plugin is bundled `enabledByDefault: true`.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — Hermes provider adapters; relevance: parallel OpenAI-compatible provider adapter.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider config; relevance: Xiaomi's EXACT explicit-config pattern (`baseUrl`/`api`/`apiKey`/`models[]`).
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local OpenAI-compatible provider; relevance: sibling `openai-completions` provider block.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — bundled TTS provider registration; relevance: analog of the `messages.tts.providers.xiaomi` block.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech-provider pipeline; relevance: parallels the chat-completions TTS contract + Opus transcode.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — manifest catalog normalization; relevance: the PAYG/Token Plan catalogs + manifest-backed pricing/compat.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest-vs-runtime catalog; relevance: auto-injection of the `xiaomi` provider when the key/profile exists.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: resolves Token Plan tiered cache-read pricing + `mimo` alias.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing; relevance: selecting `xiaomi`/`mimo` as the speech provider.
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — credential resolution order; relevance: `XIAOMI_API_KEY`/`XIAOMI_TOKEN_PLAN_API_KEY` env vs auth-profile resolution.
- [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — CLI model-switch; relevance: setting the default model after onboarding.

**Entry**

### oc_providers_zai (10t · 10s · 10d)

**Terms**
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: GLM-5.x/4.x are the LLMs this provider serves.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — bundled provider plugin; relevance: `zai` is a bundled GLM provider plugin with a manifest catalog.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — reasoning traces; relevance: `/think off/low/high/max` levels + preserved-thinking opt-in (covers the candidate-stage `term_thinking_budget` gap).
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool calls; relevance: `tool_stream` tool-call streaming is enabled by default for Z.AI.
- [Multimodal](../../term_dictionary/term_multimodal.md) — text+image; relevance: image understanding via `glm-4.6v`.
- [Authentication](../../term_dictionary/term_authentication.md) — credential mechanics; relevance: Bearer auth with `ZAI_API_KEY` + legacy `Z_AI_API_KEY` alias copy-at-startup.
- [Context Window](../../term_dictionary/term_context_window.md) — max tokens; relevance: GLM-5.2 advertises a 1M-token context.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI-compatible API; relevance: preserved thinking replays `reasoning_content` on the same OpenAI-compatible transcript.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — caching repeated prompt prefixes; relevance: preserved thinking increases prompt tokens by replaying historical `reasoning_content` (a caching/cost concern).
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider model registry; relevance: the manifest-backed GLM catalog + GLM-5 forward-resolution from the `glm-4.7` template.

**Docs**
- [CC: Effort Level and Thinking](../claude_code/cc_effort_level_and_thinking.md) — mapping thinking levels to effort; relevance: direct analog of `/think low/high → high effort`, `max → max effort`.
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference provider setup; relevance: same cloud Bearer-auth provider onboarding.
- [Hermes: Provider Routing / Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — endpoint routing; relevance: mirrors auto-detect vs explicit Coding-Plan/general/cn/global endpoint selection.
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — model provider plugin structure; relevance: parallels the bundled `zai` provider + manifest catalog.
- [Hermes: Model Aux Provider Config](../hermes_agent/hermes_model_aux_provider_config.md) — provider config; relevance: parallels the explicit `models.providers.zai.baseUrl` config block.
- [CC: Model Selection](../claude_code/cc_model_selection.md) — model/provider selection; relevance: choosing `zai/glm-5.2` (Coding Plan) vs `zai/glm-5.1` (general) defaults.
- [Pi: Model Overrides / Compat](../pi/pi_model_overrides_compat.md) — per-model compat overrides; relevance: analog of the per-model `params.tool_stream`/`preserveThinking`/`extra_body.thinking` overrides.
- [oc_providers_xiaomi](oc_providers_xiaomi.md) — sibling provider with regional endpoints + reasoning (this series, planned); relevance: same regional onboarding-choice + reasoning-control pattern.
- [oc_providers_vllm](oc_providers_vllm.md) — sibling OpenAI-compatible provider with thinking controls (this series, planned); relevance: same `enable_thinking`/`/think` reasoning-control mechanics.
- [oc_providers_volcengine](oc_providers_volcengine.md) — sibling provider (this series, planned); relevance: GLM 4.7 appears in both; same Bearer/OpenAI-compatible onboarding.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — bundled providers; relevance: implements the bundled `zai`/GLM provider.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — bundled-extension framework; relevance: registers the Z.AI plugin + manifest catalog.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — Hermes provider adapters; relevance: parallel OpenAI-compatible/Bearer provider adapter.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider config; relevance: the explicit `models.providers.zai.baseUrl` config shape.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — provider with thinking/cache behavior; relevance: analog of the preserved-thinking / `reasoning_content` replay behavior.
- [snippet_hermes_agent_core_chat_helpers_build_kwargs](../../code_snippets/snippet_hermes_agent_core_chat_helpers_build_kwargs.md) — per-model thinking/reasoning kwargs; relevance: exactly the `thinking: {type, clear_thinking}` payload mapping for `/think`.
- [snippet_hermes_agent_core_lmstudio_reasoning](../../code_snippets/snippet_hermes_agent_core_lmstudio_reasoning.md) — reasoning-control on a provider; relevance: analog of GLM thinking-disabled vs enabled handling.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — manifest catalog normalization; relevance: the manifest-backed GLM catalog rows.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — catalog discovery/forward-resolve; relevance: GLM-5 forward-resolution from the `glm-4.7` template for unknown ids.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest catalog planning; relevance: read-only `openclaw models list --all --provider zai` without runtime load.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — pricing/alias lookup; relevance: resolves `zai/<model>` refs + endpoint auto-detect fallback (glm-5.1/glm-4.7).
- [snippet_hermes_agent_plugins_provider_kimi_coding](../../code_snippets/snippet_hermes_agent_plugins_provider_kimi_coding.md) — coding-plan provider plugin; relevance: analog of the Z.AI Coding-Plan endpoint onboarding.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source precedence; relevance: `ZAI_API_KEY` vs legacy `Z_AI_API_KEY` resolution at startup.

**Entry**

## Undigested Terms Plan

Per master: OpenClaw provider/media vocabulary is digested as `oc_*` doc notes (these 7), NOT promoted to `term_dictionary`. Existing terms are LINKED. **Expected 0 new `term_dictionary` captures.**

| Term (in source) | Disposition |
|---|---|
| vLLM | `oc_providers_vllm` documents it; link existing `term_vllm` |
| `openai-completions` / OpenAI-compatible API | Config concept inside the notes; link `term_openai_responses_api` (closest existing OpenAI-API term); not a new term |
| Volcengine / Doubao / ModelArk | Provider/model names → documented as config in `oc_providers_volcengine`; not promoted (link `term_llm`) |
| BytePlus Seed Speech / TTS | Media-config concept → `oc_providers_volcengine` / `oc_providers_xiaomi` / `oc_providers_vydra`; link `term_text_to_speech` |
| Vydra / grok-imagine / veo3 / kling | Provider/model names → config in `oc_providers_vydra`; not promoted (link `term_multimodal`) |
| xAI / Grok / Grok Build | Provider/model names → config in `oc_providers_xai_setup`; not promoted (link `term_llm`) |
| Grok OAuth / device-code | Auth procedure → `oc_providers_xai_setup`; link existing `term_oauth` / `term_oauth_token` / `term_pkce` |
| x_search / web_search / code_execution | xAI tool surfaces → `oc_providers_xai_features`; link `term_function_calling`; not promoted |
| Fast-mode / legacy aliases | Model-remap reference → `oc_providers_xai_features`; not a term |
| Xiaomi MiMo / Token Plan | Provider/model + plan names → config in `oc_providers_xiaomi`; not promoted (link `term_llm`) |
| Z.AI / GLM | Provider/model-family names → config in `oc_providers_zai`; not promoted (link `term_llm`) |
| Preserved thinking / `/think` levels | Reasoning-control config → `oc_providers_zai` / `oc_providers_vllm`; link `term_chain_of_thought` |
| Qwen / Nemotron thinking-format | Provider-compat config → `oc_providers_vllm`; link existing `term_qwen` / `term_chain_of_thought` |

**New-term candidates:** none. No genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an existing note. Augment Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; it only LINKS existing terms (inherited from master). If augment Step 2d surfaces a genuinely reusable cross-cutting term with no existing note, it is captured via `/tessellum-capture-term-note` and added to the best-fit `acronym_glossary_*.md` (most likely `acronym_glossary_*` for agentic/LLM dev) per master W5 — not expected here.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P2). All gates must pass before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format: YAML field order + forbidden fields, H1/`## Overview`/`## Related Notes`/`## References` + bold footer | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: digest claims diff against `inbox/openclaw_docs/providers/<page>.md` (no invention; config snippets verbatim) | manual diff vs mirror |
| G3 | Density + Coverage: ≤400 lines / ≤2500 words / ≤6 code blocks per note; every source H2/H3 covered (section map) | `wc`/`grep` + section map |
| G4 | Cross-Reference: ≥6 relevance-selected term links + repos + sibling `oc_*` + docs/snippets, each with a relevance statement | `## Related Notes` review |
| G5 | Ghost-reference detect + redirect: every cited note_id resolves in DB | `/tessellum-fix-ghost-references` |
| G6 | Broken-link fix: 0 broken relative links after reindex | `/tessellum-fix-broken-links` |
| G7 | Discoverability: every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | inlink check (via `entry_openclaw_docs.md` + term/repo backlinks) |
| G8 | In-degree ≥1 (anti-island): `note_links` confirms in_degree ≥1 per new note | `note_links` DB query |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_providers_vllm oc_providers_volcengine oc_providers_vydra oc_providers_xai_setup oc_providers_xai_features oc_providers_xiaomi oc_providers_zai"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + link sanity
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  for s in "## Overview" "## Related Notes"; do
    grep -qF "$s" "$f" || echo "MISSING SECTION '$s' in $n"
  done
  # source_url required (G2 grounding provenance)
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url in $n"; }
  # at least one sibling oc_ cross-link (G4)
  grep -qE "\($SIBLING_PREFIX" "$f" || echo "NO sibling $SIBLING_PREFIX link in $n"
  # G3 density (strip YAML, count words + fence pairs)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w)
  cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n (${words}w / ${cb} code)"
done

# G1 YAML frontmatter sweep across the whole openclaw folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5/G6 after incremental reindex
bash scripts/update_notes_database.sh
# then: /tessellum-fix-ghost-references  and  /tessellum-fix-broken-links
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source words | Code (≤6) | Within caps? |
|---|---|---|---:|---:|---|---|
| 1 | oc_providers_vllm | procedure | 650 | 1,428 | reproduce ≤6 of 17 | ✅ |
| 2 | oc_providers_volcengine | procedure | 600 | 832 | ≤6 of 7 | ✅ |
| 3 | oc_providers_vydra | procedure | 500 | 577 | ≤6 of 7 | ✅ |
| 4 | oc_providers_xai_setup | procedure | 650 | ~1,250 (of 2,562) | ≤6 of 17 | ✅ |
| 5 | oc_providers_xai_features | model | 750 | ~1,312 (of 2,562) | ≤6 of 17 | ✅ |
| 6 | oc_providers_xiaomi | procedure | 650 | 1,205 | ≤6 of 8 | ✅ |
| 7 | oc_providers_zai | procedure | 600 | 877 | ≤6 of 8 | ✅ |

No note approaches the 2,500w / 400-line caps. The two fence-heavy pages (vllm 17, xai 17) stay ≤6 code blocks per note via the xai split + selective verbatim reproduction (getting-started / explicit config / one thinking-control / one tool-call / troubleshooting) with prose-summary of the remainder.

## Entry Point Decision (inherited from master)


## Inlinks (existing notes → new notes)


- `entry_openclaw_docs.md` (planned, master pre-step) → all 7 notes (the primary anti-island inbound for each).
- `repo_openclaw_extensions_llm_providers.md` → notes 1, 2, 4, 5, 6, 7 (it is the code-side home of every bundled model provider here).
- `repo_openclaw_extensions_voice_speech.md` → notes 2, 3, 5, 6 (the TTS/STT-registering providers).
- `repo_openclaw_extensions.md` → note 3 (bundled-plugin framework; Vydra is `enabledByDefault`).
- `term_vllm.md` → note 1.
- `term_voice_call.md` / `term_text_to_speech.md` → notes 3, 5 (Vydra/xAI media + voice).
- `term_qwen.md` → note 1 (Qwen thinking-format + tool-call sections).
- `term_deepseek.md` → note 2 (DeepSeek V3.2 in Volcengine catalog).

## Pacing Rules (inherited from master)

Single execution phase, 7 notes — one wave (well under the ~30-agent fan-out cap). Re-read each source page before authoring; reproduce config/CLI snippets verbatim; one building_block per note (xai split enforces this). `git pull --rebase --autostash origin main` first; commit + push per wave; **no Claude co-author trailer**. Reindex incrementally per wave; verify `note_links` populated + 0 broken links before commit. All 8 gates pass before commit.

## Augmentation Report (2026-06-21)


**Per-note counts (all floors met):**

| Note | Terms | Snippets | Docs | Repos | Entry | Floors |
|---|---:|---:|---:|---:|---:|---|
| oc_providers_vllm | 10 | 10 | 10 (8 existing + 2 planned sibling) | 4 | 1 | ✅ |
| oc_providers_volcengine | 10 | 10 | 10 (7 existing + 3 planned sibling) | 4 | 1 | ✅ |
| oc_providers_vydra | 10 | 10 | 10 (7 existing + 3 planned sibling) | 4 | 1 | ✅ |
| oc_providers_xai_setup | 10 | 10 | 10 (8 existing + 2 planned sibling) | 4 | 1 | ✅ |
| oc_providers_xai_features | 10 | 10 | 10 (8 existing + 2 planned sibling) | 4 | 1 | ✅ |
| oc_providers_xiaomi | 10 | 10 | 10 (7 existing + 3 planned sibling) | 4 | 1 | ✅ |
| oc_providers_zai | 10 | 10 | 10 (7 existing + 3 planned sibling) | 4 | 1 | ✅ |




**New-term candidates:** **NONE.** Step 2d re-scan of all 6 re-read pages confirms every provider/model/media/auth term either (a) is digested as an `oc_*` doc note (these 7), or (b) has an existing `term_dictionary` note to LINK. No genuinely cross-cutting, vault-reusable term lacks both a doc-page home AND an existing note. Expected 0 new `term_dictionary` captures (consistent with master design + Undigested Terms Plan). The Undigested Terms Plan + Term-Note Authoring Requirements (N/A — 0 new terms) sections are unchanged and remain valid.

**Source re-measure (Density Re-Assessment confirmed):** vllm 1,394w · volcengine 786w · vydra 547w · xai 2,532w · xiaomi 1,170w · zai 849w (all within 0.94–0.99× of plan estimates). xai @ 2,532w confirms it exceeds the 2,500w cap → the 2-way `oc_providers_xai_setup` (procedure) + `oc_providers_xai_features` (model) split is justified. H2/H3 counts match the Source table exactly. No further splits needed.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + ≥10 snippets + ≥10 docs floors, each link with relevance statement) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; all 7 notes = 10t/10s/10d; every link rendered as `[Name](relpath.md) — what; relevance: why` (programmatic count + format verified). |
| CP2 | 9-GATE table per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with all 8 gates; G5 ghost (`/tessellum-fix-ghost-references`) + G6 broken-link (`/tessellum-fix-broken-links`) + G7/G8 discoverability/in-degree all listed; validation script implements them. |
| CP4 | Plan size manageable | **PASS** | 7 planned notes, well ≤30; single execution wave (under ~30-agent fan-out cap). |
| CP5 | Note format aligned + DERIVED from existing target-dir notes | **PASS** | Format inherited verbatim from master (derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora): YAML field order `tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group`; body `# OpenClaw — Title` → `## Overview` → mirrored H2/H3 → `## Related Notes` → `## References` → bold footer; forbidden-field list present. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment table: all notes 500–750w, ≤6 code fences, no note near 2,500w/400-line caps; xai split already promotes the only >2,500w / mixed-BB page (procedure + model). No further borderline cases. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 6 pages re-read + measured this session: vllm 1,394 / volcengine 786 / vydra 547 / xai 2,532 / xiaomi 1,170 / zai 849 — all 0.94–0.99× of plan estimates (within ±30%); H2/H3 counts match Source table. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements present | **PASS** | `## Undigested Terms Plan` present (every source term routed to an `oc_*` home or existing-term link; 0 promotions); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, with the conditional capture path stated); must-language used. |
| CP8f | Term-slug specificity + all-notes (term AND doc) dedup/collision audit | **PASS** | Undigested Terms Plan disposition table = collision audit (every provider/model/media term mapped to a doc-note home or an EXISTING term to link, none recreated); specificity audit needs no renames (0 new term slugs); doc-note dedup confirmed — the 7 `oc_providers_*` slugs do not duplicate any existing `term_*`/doc note (master dedup policy + DB sweep). New-term candidates: none. |
| CP9 | Discoverability — inbound links executed (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound (`entry_openclaw_docs` → all 7; `repo_openclaw_extensions_llm_providers` → 6; `repo_openclaw_extensions_voice_speech` → 4; term backlinks); G8-Discoverability + in-degree ≥1 is gate G8 in the phase table (executed phase, not "recommended"). |


## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — 10/10 CP PASS → READY |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (READY) |
