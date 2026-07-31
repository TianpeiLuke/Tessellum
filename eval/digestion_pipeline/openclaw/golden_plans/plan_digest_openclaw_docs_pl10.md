---
title: Sub-Plan pl10 — OpenClaw Docs: Plugins (reference/elevenlabs … fireworks)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/elevenlabs", "plugins/reference/exa", "plugins/reference/fal", "plugins/reference/feishu", "plugins/reference/file-transfer", "plugins/reference/firecrawl", "plugins/reference/fireworks"]
---

# Sub-Plan pl10: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_` prefix), format (YAML + `## Overview` … `## Related Notes` …
> `## References` + bold footer), dedup (3-way across term_dictionary / documentation / repo_openclaw*), 9-GATE
> validation, cross-references, and entry-point wiring are ALL inherited from the master. This file is the plan
> stage; the locked per-note Related mapping is produced later at `/tessellum-augment-digestion-plan`.

## Scope

The seven `plugins/reference/<plugin>.md` pages from `elevenlabs` through `fireworks` (alphabetical slice of the
plugin-reference catalog). Each page is a short **plugin manifest card**: a one-line summary, a `read_when`
trigger, a **Distribution** block (npm package name + install route — bundled in OpenClaw vs npm/ClawHub), a
**Surface** block (the OpenClaw contracts/providers/channels/skills the plugin contributes), and a **Related docs**
pointer to the matching `/providers/*`, `/tools/*`, or `/channels/*` user page. The seven plugins span four
capability families: speech/media (`elevenlabs`), web search/fetch (`exa`, `firecrawl`), model providers
(`fal`, `fireworks`), a chat channel (`feishu`), and a node file-transfer tool (`file-transfer`).

**Priority P3 (Phase C — plugin reference sprawl).** These are leaf reference cards consumed by the providers,
tools, and channels series; they carry no architecture vocabulary, so they depend on (and link to) the P1/P2
notes rather than the reverse. The code-side `repo_openclaw_extensions*` notes are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 459 measured words (sum). **Planned: 7 notes** (1 per page; no splits — every page is a sub-200-word stub).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Elevenlabs plugin | plugins/reference/elevenlabs | 70 | 0 | 3 | 0 | model |
| Exa plugin | plugins/reference/exa | 50 | 0 | 3 | 0 | model |
| fal plugin | plugins/reference/fal | 58 | 0 | 3 | 0 | model |
| Feishu plugin | plugins/reference/feishu | 68 | 0 | 3 | 0 | model |
| File Transfer plugin | plugins/reference/file-transfer | 91 | 0 | 2 | 0 | model |
| Firecrawl plugin | plugins/reference/firecrawl | 68 | 0 | 3 | 0 | model |
| Fireworks plugin | plugins/reference/fireworks | 54 | 0 | 3 | 0 | model |

- H2 set per page: `## Distribution`, `## Surface`, `## Related docs` (file-transfer omits `## Related docs` → 2 H2s).
- No code fences on any page. No H3s. Each page also carries front-matter (`summary`, `read_when`, `title`).
- **BB = model**: each card is a structured descriptor of a plugin artifact (its package identity + the typed
  contracts/providers/channels it registers) — a reference/record schema, not a how-to procedure or an argument.

## Content Strategy

- **Prioritize**: capturing each plugin's **identity triple** faithfully — package name, install route, and the
  exact Surface declaration (contracts/providers/channels/skills strings, verbatim) — because that triple is the
  load-bearing, machine-meaningful content; everything else is a one-line gloss.
- **Split**: none. Every page is 50–91 words, far under the 2,500-word / mixed-BB split thresholds. 1 page → 1 note.
- **Link-out (do NOT duplicate)**: each card's `Related docs` target is a *different* series' page — the provider
  reference (`/providers/elevenlabs`, `/providers/fal`, `/providers/fireworks`), tool reference
  (`/tools/exa-search`, `/tools/firecrawl`), or channel reference (`/channels/feishu`). Those are owned by the
  `pr*`, `to*`, and `ch*` sub-plans; this sub-plan links to them as planned siblings, never re-digests them.
  Contract/provider concepts (TTS/STT, web search, image/music/video generation, model provider, chat channel)
  are linked to existing `term_dictionary` notes — never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_elevenlabs.md` | model | elevenlabs.md: summary, Distribution, Surface, Related docs | 280 | The `@openclaw/elevenlabs-speech` plugin (bundled in OpenClaw): contributes the `mediaUnderstandingProviders`, `realtimeTranscriptionProviders`, and `speechProviders` contracts (media understanding + realtime transcription + text-to-speech). |
| 2 | `oc_plugins_reference_exa.md` | model | exa.md: summary, Distribution, Surface, Related docs | 250 | The `@openclaw/exa-plugin` (npm / ClawHub `clawhub:@openclaw/exa-plugin`): contributes the `webSearchProviders` contract, adding Exa web-search provider support; pairs with the `/tools/exa-search` tool. |
| 3 | `oc_plugins_reference_fal.md` | model | fal.md: summary, Distribution, Surface, Related docs | 270 | The `@openclaw/fal-provider` plugin (bundled): registers the `fal` provider and the `imageGenerationProviders`, `musicGenerationProviders`, and `videoGenerationProviders` contracts for fal media-generation models. |
| 4 | `oc_plugins_reference_feishu.md` | model | feishu.md: summary, Distribution, Surface, Related docs | 270 | The community-maintained (@m1heng) `@openclaw/feishu` plugin (npm / ClawHub): adds the `feishu` channel plus `tools` and `skills` contracts for Feishu/Lark chats and workplace tooling. |
| 5 | `oc_plugins_reference_file_transfer.md` | model | file-transfer.md: summary, Distribution, Surface | 290 | The `@openclaw/file-transfer` plugin (bundled): contributes `tools` for fetch/list/write files on paired nodes via dedicated node commands, using base64 over `node.invoke` to bypass bash stdout truncation (binaries up to 16 MB). |
| 6 | `oc_plugins_reference_firecrawl.md` | model | firecrawl.md: summary, Distribution, Surface, Related docs | 280 | The `@openclaw/firecrawl-plugin` (npm / ClawHub `clawhub:@openclaw/firecrawl-plugin`): contributes `tools`, `webFetchProviders`, and `webSearchProviders` contracts for Firecrawl web crawl/fetch/search; pairs with `/tools/firecrawl`. |
| 7 | `oc_plugins_reference_fireworks.md` | model | fireworks.md: summary, Distribution, Surface, Related docs | 250 | The `@openclaw/fireworks-provider` plugin (bundled): registers the `fireworks` provider, adding Fireworks AI model-provider support; pairs with `/providers/fireworks`. |

Filename rule applied: `oc_` + full slug with `/` and `-` → `_` (e.g. `plugins/reference/file-transfer` →
`oc_plugins_reference_file_transfer.md`). No aspect suffixes needed (no splits).

## Section Coverage Map

Every H2/H3 of every source page maps to exactly one planned note. No orphans.

```
plugins/reference/elevenlabs.md
├── (front-matter summary + read_when) ──── → note 1 (oc_plugins_reference_elevenlabs) Overview
├── ## Distribution (package, install route) → note 1
├── ## Surface (contracts: media/realtime/speech) → note 1
└── ## Related docs (/providers/elevenlabs) ─ → note 1 References + Related Notes (planned sibling)
plugins/reference/exa.md
├── summary + read_when ──────────────────── → note 2 (oc_plugins_reference_exa) Overview
├── ## Distribution ──────────────────────── → note 2
├── ## Surface (contracts: webSearchProviders) → note 2
└── ## Related docs (/tools/exa-search) ───── → note 2 References + Related Notes (planned sibling)
plugins/reference/fal.md
├── summary + read_when ──────────────────── → note 3 (oc_plugins_reference_fal) Overview
├── ## Distribution ──────────────────────── → note 3
├── ## Surface (providers: fal; contracts: image/music/video) → note 3
└── ## Related docs (/providers/fal) ──────── → note 3 References + Related Notes (planned sibling)
plugins/reference/feishu.md
├── summary + read_when (community @m1heng) ─ → note 4 (oc_plugins_reference_feishu) Overview
├── ## Distribution ──────────────────────── → note 4
├── ## Surface (channels: feishu; contracts: tools; skills) → note 4
└── ## Related docs (/channels/feishu) ────── → note 4 References + Related Notes (planned sibling)
plugins/reference/file-transfer.md
├── summary + read_when (base64/16 MB) ────── → note 5 (oc_plugins_reference_file_transfer) Overview
├── ## Distribution ──────────────────────── → note 5
└── ## Surface (contracts: tools) ─────────── → note 5
plugins/reference/firecrawl.md
├── summary + read_when ──────────────────── → note 6 (oc_plugins_reference_firecrawl) Overview
├── ## Distribution ──────────────────────── → note 6
├── ## Surface (contracts: tools/webFetch/webSearch) → note 6
└── ## Related docs (/tools/firecrawl) ────── → note 6 References + Related Notes (planned sibling)
plugins/reference/fireworks.md
├── summary + read_when ──────────────────── → note 7 (oc_plugins_reference_fireworks) Overview
├── ## Distribution ──────────────────────── → note 7
├── ## Surface (providers: fireworks) ─────── → note 7
└── ## Related docs (/providers/fireworks) ── → note 7 References + Related Notes (planned sibling)
```

No orphaned sections. `Related docs` targets (`/providers/*`, `/tools/*`, `/channels/*`) are owned by the
`pr*`/`to*`/`ch*` sub-plans and linked, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are 50–91 words with a single building_block (model/reference card); each is well under the 2,500-word and mixed-BB split thresholds. 1 page → 1 note. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (459 words total; 50–91 words each). New `oc_` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: model ×7 (every note is a plugin-manifest reference card).
- Code fences in source: **0**. Each digest note may reproduce the verbatim Surface contract string and the
  `clawhub:`/npm install token in a single inline-formatted or 1-fence block — well within the ≤6-fence cap.
- Estimated digest words: ~1,890 (avg ~270/note). Each note is intentionally slim (the source is a stub); the
  Overview + a Distribution + a Surface H2 + Related Notes + References footer is the entire note.
- **Cross-refs (LOCKED at xref-augment 2026-06-21 — raised floors):** each note maps **≥8 relevance-selected
  `hermes_*`/`cc_*`/`pi_*`/`band_*`/`bedrock_*` analogs; remainder are planned sibling `oc_*`) PLUS 3–4
  `repo_openclaw*` repos, each with a per-link relevance statement. Final per-note counts: 10–11 terms /
  planned `oc_*` siblings are backticked, not linked. See `## Per-Note Related Notes Mapping (LOCKED …)`.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

`hermes_agent/` / `claude_code/` / `pi/` / `band/` / `aws_bedrock/` coding-agent corpora with planned sibling
`oc_*` docs (this series, marked `(planned, this series)`). Relative paths are FROM a note at
`resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/term_Y.md`; sibling oc_ doc →
`oc_Y.md`; other doc → `../<folder>/<file>.md`; repo → `../../../areas/code_repos/repo_Y.md`; snippet →
`../../code_snippets/snippet_Y.md`. Each link rendered as `- [Name](relpath.md) — what it is; relevance: why THIS note`.

### oc_plugins_reference_elevenlabs (10t · 11s · 11d)

**Terms**
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesizing speech audio from text; relevance: the plugin's `speechProviders` contract IS a TTS provider (ElevenLabs voices).
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcribing audio to text; relevance: the `realtimeTranscriptionProviders` contract is the streaming STT side of the plugin.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — low-latency streaming ASR; relevance: exact named contract the plugin registers (`realtimeTranscriptionProviders`).
- [Multimodal](../../term_dictionary/term_multimodal.md) — models spanning text/audio/image; relevance: the `mediaUnderstandingProviders` contract is the closest existing concept for media understanding.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — turn-based spoken agent interaction; relevance: TTS + realtime transcription are the building blocks voice mode consumes.
- [Voice Call](../../term_dictionary/term_voice_call.md) — full-duplex telephony agent sessions; relevance: ElevenLabs speech feeds the voice-call media pipeline.
- [Voice Bot](../../term_dictionary/term_voice_bot.md) — agent reachable over a voice channel; relevance: speech synthesis/transcription are the I/O surface of a voice bot.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendors; relevance: ElevenLabs is exactly such a third-party speech/media vendor.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted multi-channel agent gateway; relevance: this plugin is bundled in OpenClaw and extends it.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + surface declaration of a plugin; relevance: this reference card IS the elevenlabs plugin's manifest.

**Docs**
- [Hermes TTS Providers](../hermes_agent/hermes_tts_providers.md) — how a sibling agent registers TTS provider plugins; relevance: direct analog to the `speechProviders` contract.
- [Hermes Use Voice Mode (Guide)](../hermes_agent/hermes_use_voice_mode_guide.md) — operating voice mode end to end; relevance: shows the consumer of TTS+STT this plugin supplies.
- [Hermes Voice Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — CLI surface for voice mode; relevance: equivalent provider-config story for speech.
- [Hermes Voice Gateway (Discord VC)](../hermes_agent/hermes_voice_gateway_discord_vc.md) — voice over a chat channel; relevance: parallel media/speech routing pattern.
- [Hermes Tools Reference — Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — media (audio/image) tooling; relevance: covers media understanding analog to `mediaUnderstandingProviders`.
- [Hermes Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media handling config; relevance: shows how media/audio attachments flow to providers.
- [CC Voice Dictation](../claude_code/cc_voice_dictation.md) — speech-to-text input in a coding agent; relevance: cross-tool STT/transcription analog.
- [Hermes Built-in Plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled-plugin catalog; relevance: ElevenLabs ships "included in OpenClaw" (bundled) — same distribution model.
- [Hermes Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin contract/surface taxonomy; relevance: explains the contracts a speech plugin declares.
- `oc_providers_elevenlabs.md` (planned, pr* series) — the `/providers/elevenlabs` user page; relevance: the plugin card's Related-docs target.
- `oc_plugins_reference_fal.md` (planned, this series) — fellow bundled media plugin; relevance: sibling media-capability plugin card.

- [oc_plugins_reference_exa](oc_plugins_reference_exa.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — the voice/speech extension subsystem; relevance: home of the speech/transcription provider implementations.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo that bundles this plugin; relevance: "included in OpenClaw" install route.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: registers the plugin's contracts.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channel; relevance: a downstream consumer of TTS/STT speech.

**Snippets**
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — the actual ElevenLabs TTS implementation; relevance: direct code behind `speechProviders`.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS provider; relevance: peer speech-provider implementation pattern.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram realtime STT; relevance: the realtime-transcription-provider analog.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline wiring; relevance: how speech providers slot into the runtime.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — live transcription in a call; relevance: consumer of the realtime-transcription contract.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — audio stream handling; relevance: audio I/O around speech providers.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: routes transcription output through the gateway.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin registration entry points; relevance: how the plugin exposes its Surface.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/enable/disable; relevance: Distribution → runtime activation.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package-level plugin contract; relevance: the contract this manifest card describes.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loader; relevance: how the bundled package is loaded.

### oc_plugins_reference_exa (10t · 10s · 11d)

**Terms**
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — finding relevant documents for a query; relevance: the `webSearchProviders` contract is web-scale IR.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: Exa web search is a retrieval source for RAG.
- [Deep Research Agent](../../term_dictionary/term_deep_research_agent.md) — multi-step web research agents; relevance: Exa search is a core tool for research agents.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking typed tools; relevance: web search is exposed to the agent as a callable tool.
- [Tool Gateway](../../term_dictionary/term_tool_gateway.md) — gateway that brokers agent tools; relevance: the search provider is served through the tool gateway.
- [ReAct](../../term_dictionary/term_react.md) — reason-and-act tool loop; relevance: web-search-then-reason is the canonical ReAct pattern.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent surface; relevance: the consumer issuing search queries.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendors; relevance: Exa is exactly such a third-party search vendor.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: this plugin extends OpenClaw via npm/ClawHub.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin package + surface declaration; relevance: this card IS the exa plugin manifest.

**Docs**
- [Hermes Web Search Provider Plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — building a web-search provider plugin; relevance: direct analog to the `webSearchProviders` contract.
- [Hermes Web Search & Extract](../hermes_agent/hermes_web_search_extract.md) — searching + extracting web content; relevance: the capability Exa contributes.
- [Hermes Tool Search](../hermes_agent/hermes_tool_search.md) — search tools as agent tools; relevance: how a search provider surfaces as a tool.
- [Hermes X Search (Grok)](../hermes_agent/hermes_x_search_grok.md) — another search-provider integration; relevance: peer external-search provider pattern.
- [CC Web Overview](../claude_code/cc_web_overview.md) — web capability in a coding agent; relevance: cross-tool web-search/fetch analog.
- [CC MCP Tool Search](../claude_code/cc_mcp_tool_search.md) — discovering tools via search; relevance: search-as-tool plumbing analog.
- [Hermes Built-in Plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled-vs-installed plugin catalog; relevance: Exa is npm/ClawHub-installed, contrasting bundled plugins.
- [Hermes Plugins Management](../hermes_agent/hermes_plugins_management.md) — installing/managing plugins; relevance: the npm/ClawHub install route Exa uses.
- [Hermes Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin contract taxonomy; relevance: classifies the `webSearchProviders` surface.
- `oc_tools_exa_search.md` (planned, to* series) — the `/tools/exa-search` user page; relevance: the plugin card's Related-docs target.
- `oc_plugins_reference_firecrawl.md` (planned, this series) — fellow web search/fetch plugin; relevance: sibling web-capability plugin card.

- [oc_plugins_reference_elevenlabs](oc_plugins_reference_elevenlabs.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: registers the `webSearchProviders` contract.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo/loader; relevance: loads the installed Exa plugin.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app/install routing; relevance: handles npm/ClawHub install enablement.

**Snippets**
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin registration entry points; relevance: how Exa exposes its Surface.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loader; relevance: how an npm-installed plugin is loaded.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — config-driven plugin enablement; relevance: install-route effect on enablement.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/enable/disable; relevance: lifecycle of an installed search plugin.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package-level plugin contract; relevance: the contract this card describes.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — agent tool catalog; relevance: where a search tool is registered for the agent.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool gating policy; relevance: gating which agents may use web search.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — handling untrusted external content; relevance: web-search results are external/untrusted content.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP routing to plugins; relevance: routes search-provider HTTP calls.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — plugin fallback context; relevance: failover behavior for provider plugins.

### oc_plugins_reference_fal (11t · 11s · 11d)

**Terms**
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative model for images/video; relevance: fal's image/video generation runs on diffusion backbones.
- [Stable Diffusion](../../term_dictionary/term_stable_diffusion.md) — flagship open diffusion model; relevance: representative model class served by fal.
- [Multimodal](../../term_dictionary/term_multimodal.md) — models spanning modalities; relevance: fal spans image/music/video generation.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a model provider; relevance: the fal plugin registers the `fal` provider.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: fal's models populate the catalog via the provider.
- [Foundation Model](../../term_dictionary/term_foundation_model.md) — large pretrained generative model; relevance: fal serves foundation media-generation models.
- [GenAI](../../term_dictionary/term_genai.md) — generative AI; relevance: image/music/video generation is generative AI.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendors; relevance: fal is exactly such a hosted media-generation vendor.
- [Amazon Nova](../../term_dictionary/term_amazon_nova.md) — multimodal generation model family; relevance: peer multimodal-generation model for contrast.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: this plugin is bundled in OpenClaw.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin package + surface declaration; relevance: this card IS the fal plugin manifest.

**Docs**
- [Hermes Image Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — building an image-generation provider plugin; relevance: direct analog to `imageGenerationProviders`.
- [Hermes Video Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-generation provider plugin; relevance: direct analog to `videoGenerationProviders`.
- [Hermes Image Generation](../hermes_agent/hermes_image_generation.md) — using image generation; relevance: the capability fal contributes.
- [Hermes Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — registering a model provider plugin; relevance: fal registers the `fal` provider.
- [Hermes Adding Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — how to add a provider; relevance: bundled-provider registration analog.
- [PI Cloud Providers](../pi/pi_cloud_providers.md) — configuring cloud model providers; relevance: provider-config story for a media provider.
- [PI Custom Models](../pi/pi_custom_models.md) — registering custom models; relevance: how fal's models become selectable.
- [Bedrock Invoke API — Multimodal](../aws_bedrock/bedrock_invoke_api_multimodal.md) — invoking multimodal generation; relevance: cross-platform media-generation invocation analog.
- [Bedrock Invoke API — Images](../aws_bedrock/bedrock_invoke_api_images.md) — image-generation invocation; relevance: image-gen request/response analog.
- `oc_providers_fal.md` (planned, pr* series) — the `/providers/fal` user page; relevance: the plugin card's Related-docs target.
- `oc_plugins_reference_fireworks.md` (planned, this series) — fellow bundled provider plugin; relevance: sibling provider plugin card.

- [oc_plugins_reference_elevenlabs](oc_plugins_reference_elevenlabs.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider-extension subsystem; relevance: home of provider-plugin implementations like fal.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo that bundles fal; relevance: "included in OpenClaw" install route.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: registers the generation contracts.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — provider registration (OpenAI); relevance: the provider-registration pattern fal follows.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — provider registration (Anthropic); relevance: peer provider-registration pattern.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local provider registration; relevance: another provider-plugin shape.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery/normalization; relevance: how fal's models enter the catalog.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planning; relevance: declaring fal's generation models.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent model catalog; relevance: where generation models become selectable.
- [snippet_openclaw_gateway_managed_image_resize_validate](../../code_snippets/snippet_openclaw_gateway_managed_image_resize_validate.md) — managed image handling; relevance: processing generated image output.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin registration entry points; relevance: how fal exposes its provider + contracts.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/enable/disable; relevance: bundled provider activation.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package-level plugin contract; relevance: the contract this card describes.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loader; relevance: loads the bundled fal provider.

### oc_plugins_reference_feishu (11t · 11s · 11d)

**Terms**
- [Slack](../../term_dictionary/term_slack.md) — enterprise chat platform; relevance: peer enterprise-chat channel to Feishu/Lark.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway bridging chat platforms; relevance: Feishu is one such bridged messaging platform.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — core channel dispatch engine; relevance: the Feishu `channels` contract plugs into the channel kernel.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — pairing direct-message conversations; relevance: Feishu chats use DM pairing for binding.
- [Thread Binding Policy](../../term_dictionary/term_thread_binding_policy.md) — binding agents to threads; relevance: governs how Feishu threads map to sessions.
- [Conversational AI](../../term_dictionary/term_conversational_ai.md) — dialog-based AI; relevance: the agent surface exposed over Feishu chats.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent in a channel; relevance: what the Feishu channel exposes.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking typed tools; relevance: the plugin's `tools` contract is agent-callable tools.
- [Skills](../../term_dictionary/term_skills.md) — packaged agent capabilities; relevance: the plugin's `skills` contract contributes workplace skills.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: this community plugin extends OpenClaw.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin package + surface declaration; relevance: this card IS the feishu plugin manifest.

**Docs**
- [Hermes Messaging Slack](../hermes_agent/hermes_messaging_slack.md) — wiring a chat platform channel; relevance: direct enterprise-chat channel analog to Feishu.
- [Hermes Messaging Slack Config](../hermes_agent/hermes_messaging_slack_config.md) — channel configuration; relevance: the config story a Feishu channel mirrors.
- [Hermes Messaging Google Chat](../hermes_agent/hermes_messaging_google_chat.md) — another enterprise chat channel; relevance: peer workplace-chat integration.
- [Hermes Adding Platform Adapter Plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — building a channel/platform adapter plugin; relevance: how a community channel plugin like Feishu is authored.
- [Hermes Google Workspace Skill](../hermes_agent/hermes_google_workspace_skill.md) — workplace-tooling skill; relevance: analog to Feishu's `skills` workplace-tools contract.
- [CC Channels Overview](../claude_code/cc_channels_overview.md) — channel concept overview; relevance: defines the channel surface Feishu satisfies.
- [CC Build a Channel](../claude_code/cc_build_a_channel.md) — authoring a channel; relevance: cross-tool channel-plugin authoring analog.
- [CC Channels Setup](../claude_code/cc_channels_setup.md) — connecting channels; relevance: install/connect story for a chat channel.
- [Hermes Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin contract taxonomy; relevance: classifies the `channels`/`tools`/`skills` surfaces.
- `oc_channels_feishu.md` (planned, ch* series) — the `/channels/feishu` user page; relevance: the plugin card's Related-docs target.
- `oc_plugins_reference_exa.md` (planned, this series) — fellow community/installed plugin; relevance: sibling npm/ClawHub plugin card.

- [oc_plugins_reference_elevenlabs](oc_plugins_reference_elevenlabs.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel subsystem; relevance: home of the channel-adapter framework Feishu plugs into.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel implementations; relevance: where a Feishu/Lark adapter lives.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: hosts the `skills` contract Feishu contributes.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo/loader; relevance: loads the installed Feishu plugin.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the channel adapter contract; relevance: the contract a Feishu channel satisfies.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: registering the `feishu` channel.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — binding + routing messages; relevance: routes Feishu messages to sessions.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: dispatch path for Feishu events.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — resolving conversations; relevance: maps Feishu chats to conversations.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match/route resolver; relevance: matching inbound Feishu messages.
- [snippet_openclaw_channels_dm_pairing_allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing allowlist; relevance: pairing/allowlisting Feishu DMs.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest format; relevance: the `skills` contract Feishu declares.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor contract; relevance: the `tools` contract Feishu declares.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin registration entry points; relevance: how Feishu exposes its Surface.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package-level plugin contract; relevance: the contract this card describes.

### oc_plugins_reference_file_transfer (10t · 11s · 10d)

**Terms**
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking typed tools; relevance: the plugin's `tools` contract is agent-callable file ops.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — registry of available tools; relevance: fetch/list/write register as tools.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — typed tool declaration; relevance: each file-op tool is declared via a descriptor.
- [Sandbox](../../term_dictionary/term_sandbox.md) — confined execution boundary; relevance: file ops run within the node execution boundary.
- [Code Execution Tool](../../term_dictionary/term_code_execution_tool.md) — tool that runs commands; relevance: file transfer runs via dedicated node commands.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional socket transport; relevance: `node.invoke` runs over the websocket node transport.
- [Base64](../../term_dictionary/term_base64.md) — binary-to-text encoding; relevance: binaries are sent base64-encoded to bypass stdout truncation.
- [Remote SSH](../../term_dictionary/term_remote_ssh.md) — remote command/file execution; relevance: conceptual analog to paired-node remote file ops.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: this plugin is bundled in OpenClaw.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin package + surface declaration; relevance: this card IS the file-transfer plugin manifest.

**Docs**
- [Hermes Tools Reference — Core](../hermes_agent/hermes_tools_reference_core.md) — core agent tools; relevance: the `tools` family file-transfer extends.
- [Hermes Adding Built-in Tool](../hermes_agent/hermes_adding_built_in_tool.md) — authoring a built-in tool; relevance: how fetch/list/write tools are added.
- [Hermes Tool Gateway](../hermes_agent/hermes_tool_gateway.md) — gateway brokering tools; relevance: file-op tools are served via the tool gateway.
- [CC File Tool Behavior](../claude_code/cc_file_tool_behavior.md) — file-read/write tool semantics; relevance: direct analog to fetch/list/write file ops.
- [CC Sandbox Filesystem & Network Isolation](../claude_code/cc_sandbox_filesystem_network_isolation.md) — fs/network isolation; relevance: the execution boundary node file ops respect.
- [CC Built-in Tools](../claude_code/cc_built_in_tools.md) — built-in tool catalog; relevance: where file tools register.
- [PI Extensions — Custom Tools](../pi/pi_extensions_custom_tools.md) — adding custom tools via extension; relevance: extension-based tool registration analog.
- [Band WebSocket Overview](../band/band_websocket_overview.md) — websocket transport protocol; relevance: analog to the `node.invoke` websocket transport.
- [Band MCP Tools Reference](../band/band_mcp_tools_reference.md) — tool reference over a protocol; relevance: typed-tool contract analog.
- `oc_tools_file_transfer.md` (planned, to* series) — the file-transfer tool user page; relevance: the consumer-facing tool docs (no Related-docs link on the card; nearest sibling).

- [oc_plugins_reference_elevenlabs](oc_plugins_reference_elevenlabs.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway runtime; relevance: hosts `node.invoke` / paired-node transport.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo that bundles this plugin; relevance: "included in OpenClaw" install route.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: registers the `tools` contract.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app/install routing; relevance: bundled-plugin enablement.

**Snippets**
- [snippet_openclaw_gateway_nodes_command_apns_invoke](../../code_snippets/snippet_openclaw_gateway_nodes_command_apns_invoke.md) — node command invoke; relevance: the `node.invoke` command path file transfer uses.
- [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: gating which node commands (file ops) may run.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing; relevance: file ops target paired nodes.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session kit; relevance: the node session the transfer runs over.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — node websocket transport; relevance: the websocket carrying base64 `node.invoke`.
- [snippet_openclaw_android_invoke_dispatcher](../../code_snippets/snippet_openclaw_android_invoke_dispatcher.md) — invoke dispatcher on a node; relevance: dispatching file-op commands on a node.
- [snippet_openclaw_gateway_chat_attachments_sanitize](../../code_snippets/snippet_openclaw_gateway_chat_attachments_sanitize.md) — attachment sanitization; relevance: handling binary file payloads safely.
- [snippet_openclaw_security_exec_filesystem_policy](../../code_snippets/snippet_openclaw_security_exec_filesystem_policy.md) — exec filesystem policy; relevance: the fs boundary file ops obey.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin registration entry points; relevance: how the plugin exposes its `tools` Surface.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package-level plugin contract; relevance: the contract this card describes.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loader; relevance: loads the bundled file-transfer plugin.

### oc_plugins_reference_firecrawl (10t · 10s · 11d)

**Terms**
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — finding relevant documents/content; relevance: Firecrawl's `webSearchProviders` is web-scale IR.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: Firecrawl crawl/fetch supplies retrieval content for RAG.
- [Deep Research Agent](../../term_dictionary/term_deep_research_agent.md) — multi-step web research agents; relevance: crawl/fetch/search are core research-agent tools.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic web navigation/extraction; relevance: web crawl/fetch is automated content extraction.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking typed tools; relevance: the plugin's `tools` contract exposes crawl/fetch as tools.
- [Tool Gateway](../../term_dictionary/term_tool_gateway.md) — gateway brokering agent tools; relevance: Firecrawl tools served via the tool gateway.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational agent surface; relevance: the consumer issuing fetch/search.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendors; relevance: Firecrawl is exactly such a third-party crawl/search vendor.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: this plugin extends OpenClaw via npm/ClawHub.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin package + surface declaration; relevance: this card IS the firecrawl plugin manifest.

**Docs**
- [Hermes Web Search Provider Plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — building a web-search provider plugin; relevance: direct analog to `webSearchProviders`.
- [Hermes Web Search & Extract](../hermes_agent/hermes_web_search_extract.md) — search + extract web content; relevance: exact crawl/fetch/extract capability Firecrawl contributes.
- [Hermes Tool Search](../hermes_agent/hermes_tool_search.md) — search tools as agent tools; relevance: how Firecrawl's `tools` surface as agent tools.
- [Hermes Open WebUI Integration](../hermes_agent/hermes_open_webui_integration.md) — web content integration; relevance: web-fetch consumption analog (`webFetchProviders`).
- [CC Web Overview](../claude_code/cc_web_overview.md) — web capability in a coding agent; relevance: cross-tool web crawl/fetch/search analog.
- [CC MCP Tool Search](../claude_code/cc_mcp_tool_search.md) — discovering tools via search; relevance: search-as-tool plumbing analog.
- [Hermes Built-in Plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled-vs-installed catalog; relevance: Firecrawl is npm/ClawHub-installed.
- [Hermes Plugins Management](../hermes_agent/hermes_plugins_management.md) — installing/managing plugins; relevance: the npm/ClawHub install route Firecrawl uses.
- [Hermes Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin contract taxonomy; relevance: classifies the `tools`/`webFetch`/`webSearch` surfaces.
- `oc_tools_firecrawl.md` (planned, to* series) — the `/tools/firecrawl` user page; relevance: the plugin card's Related-docs target.
- `oc_plugins_reference_exa.md` (planned, this series) — fellow web search/fetch plugin; relevance: sibling web-capability plugin card.

- [oc_plugins_reference_elevenlabs](oc_plugins_reference_elevenlabs.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: registers the `tools`/`webFetch`/`webSearch` contracts.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo/loader; relevance: loads the installed Firecrawl plugin.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app/install routing; relevance: npm/ClawHub install enablement.

**Snippets**
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin registration entry points; relevance: how Firecrawl exposes its three contracts.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loader; relevance: how the npm-installed plugin is loaded.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — config-driven plugin enablement; relevance: install-route effect on enablement.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/enable/disable; relevance: lifecycle of an installed crawl plugin.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package-level plugin contract; relevance: the contract this card describes.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — agent tool catalog; relevance: where Firecrawl tools register.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool gating policy; relevance: gating which agents may crawl/fetch.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — handling untrusted external content; relevance: crawled web content is external/untrusted.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP routing to plugins; relevance: routes Firecrawl HTTP fetch/search calls.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — plugin fallback context; relevance: failover behavior for fetch/search providers.

### oc_plugins_reference_fireworks (11t · 10s · 11d)

**Terms**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a model provider; relevance: the Fireworks plugin registers the `fireworks` provider.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Fireworks serves LLM inference.
- [Foundation Model](../../term_dictionary/term_foundation_model.md) — large pretrained model; relevance: Fireworks hosts foundation models.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: Fireworks models populate the catalog via the provider.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routing requests across providers; relevance: Fireworks is one routable model provider.
- [Failover](../../term_dictionary/term_failover.md) — falling back across providers; relevance: Fireworks participates in the provider fallback ladder.
- [GenAI](../../term_dictionary/term_genai.md) — generative AI; relevance: Fireworks AI is a generative-model provider.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted AI vendors; relevance: Fireworks AI is exactly such a hosted model provider.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model invoking typed tools; relevance: a capability of the LLMs Fireworks serves.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — self-hosted agent gateway; relevance: this plugin is bundled in OpenClaw.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — plugin package + surface declaration; relevance: this card IS the fireworks plugin manifest.

**Docs**
- [Hermes Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — registering a model provider plugin; relevance: direct analog to registering the `fireworks` provider.
- [Hermes Adding Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — adding an inference provider; relevance: how a bundled model provider is added.
- [Hermes Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: Fireworks is a cloud inference provider.
- [Hermes Provider Routing](../hermes_agent/hermes_provider_routing.md) — routing across providers; relevance: how Fireworks slots into routing.
- [Hermes Fallback Providers](../hermes_agent/hermes_fallback_providers.md) — provider fallback ladders; relevance: Fireworks in the failover chain.
- [Hermes Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog reference; relevance: how Fireworks models become selectable.
- [PI Cloud Providers](../pi/pi_cloud_providers.md) — configuring cloud model providers; relevance: provider-config story for Fireworks.
- [PI Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering a provider; relevance: provider-registration analog.
- [PI Custom Models](../pi/pi_custom_models.md) — registering custom models; relevance: exposing Fireworks models.
- `oc_providers_fireworks.md` (planned, pr* series) — the `/providers/fireworks` user page; relevance: the plugin card's Related-docs target.
- `oc_plugins_reference_fal.md` (planned, this series) — fellow bundled provider plugin; relevance: sibling provider plugin card.

- [oc_plugins_reference_elevenlabs](oc_plugins_reference_elevenlabs.md) — sibling plugins page (planned, this series); relevance: same plugins cluster — cross-referenced companion surface in this sub-plan.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — provider-extension subsystem; relevance: home of model-provider plugins like Fireworks.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the monorepo that bundles Fireworks; relevance: "included in OpenClaw" install route.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extension framework; relevance: registers the `fireworks` provider.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — provider registration (OpenAI); relevance: the provider-registration pattern Fireworks follows.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — provider registration (Anthropic); relevance: peer provider-registration pattern.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider registration; relevance: multi-model provider registration analog.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local provider registration; relevance: another provider-plugin shape.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent model catalog; relevance: where Fireworks models become selectable.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery/normalization; relevance: how Fireworks models enter the catalog.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — model pricing lookup; relevance: pricing metadata for provider models.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — model fallback ladder; relevance: Fireworks position in the failover ladder.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin registration entry points; relevance: how Fireworks exposes its provider.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loader; relevance: loads the bundled Fireworks provider.

## Undigested Terms Plan

Per master: OpenClaw vocabulary surfaced by these pages is digested as `oc_*` doc notes (already covered by the
7 planned notes) or LINKED to existing `term_dictionary` notes; **0 new `term_dictionary` captures expected**.

| Term (as it appears on the pages) | Disposition |
|---|---|
| ElevenLabs / Exa / fal / Feishu (Lark) / Firecrawl / Fireworks | Vendor/product names → digested in their `oc_plugins_reference_*` notes; no term_dictionary entry (named product, not a reusable cross-cutting concept). |
| Text-to-speech (speechProviders) | Link existing `term_text_to_speech` ✅. |
| Realtime transcription (realtimeTranscriptionProviders) | Link existing `term_realtime_transcription` ✅ (and `term_speech_to_text` ✅). |
| Media understanding (mediaUnderstandingProviders) | Link existing `term_multimodal` ✅ (closest existing concept). No new term — narrow contract name. |
| Web search (webSearchProviders) | Link existing `term_information_retrieval` ✅ / `term_rag` ✅. (`term_web_search` does not exist; not capturing — adequately covered.) |
| Web fetch (webFetchProviders) | Link existing `term_information_retrieval` ✅. (`term_web_fetch` does not exist; not a reusable standalone concept here.) |
| Image / music / video generation (image/music/videoGenerationProviders) | Link existing `term_diffusion_model` ✅ / `term_multimodal` ✅. (No `term_image_generation` etc.; not capturing — contract names, adequately glossed in-note.) |
| Provider / contract / surface (OpenClaw plugin model) | Link existing `term_provider_plugin` ✅, `term_plugin_manifest` ✅, `term_plugin_sdk` ✅. |
| Channel (feishu) / tools / skills (contracts) | Link existing `term_function_calling` ✅ (tools), `term_chatbot` ✅ (channel); `oc_channels_*` (planned) for the channel itself. |
| node.invoke / paired nodes / base64 / 16 MB transfer | OpenClaw runtime mechanics → glossed in `oc_plugins_reference_file_transfer`; link `term_websocket` ✅ + `repo_openclaw_gateway`. No new term. |
| npm / ClawHub / bundled-in-OpenClaw (install routes) | Distribution mechanics → in-note; link `term_npm` ✅; ClawHub itself owned by the `cw*` sub-plans (`oc_clawhub_*`, planned). |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable concept lacks an existing note here;
the candidate gaps (web_search / image_generation / media_understanding) are narrow contract labels best handled
by linking the nearest existing term and glossing in-note, per master's "near-0 new terms" expectation.

## Term-Note Authoring Requirements

N/A (0 new terms). No `/tessellum-capture-term-note` invocation and no `acronym_glossary_*.md` edit for this sub-plan.

## Per-Phase Validation Gate (G1–G9)

Single execution phase (all 7 notes). Inherited from master; run after authoring, before commit.

| Gate | Check | Tool / Method | Pass criterion |
|---|---|---|---|
| G1 | Format + YAML | `/tessellum-check-note-format` + `python3 scripts/check_yaml_frontmatter.py --path <note>` | All 7 notes: required YAML (tags lead `resource`,`documentation`,`openclaw`; itemized keywords/topics; `building_block: model`; `source_url`; quoted years if any); `# OpenClaw — …` H1; `## Overview` + `## Related Notes` present; bold `**Source**`/`**Last Updated**`/`**Status**` footer. 0 errors. |
| G2 | Grounding | Diff each note's facts vs `inbox/openclaw_docs/plugins/reference/<page>.md` | Package name, install route, and Surface contract/provider/channel strings reproduced verbatim; no invented capabilities. |
| G3 | Density + coverage | Word/line/fence count vs caps; section coverage map | Each note ≤400 lines / ≤2500 words / ≤6 fences; every source H2/H3 mapped (no orphan, no over-compression of the 3 H2s). |
| G4 | Cross-reference | Count + relevance of `## Related Notes` links | Each note ≥6 relevance-selected term links + ≥1 `repo_openclaw*` + ≥1 sibling `oc_*` + relevant snippet/doc; each link has a relevance statement; indexed `[text](path.md)` format. |
| G5 | Ghost-reference | `/tessellum-fix-ghost-references` + DB-verify every cited EXISTING `note_id` | 0 ghost references; all non-`(planned)` targets exist in DB. |
| G6 | Broken-link | `/tessellum-fix-broken-links` after incremental reindex | 0 broken links from the 7 new notes. |
| G7/G8 | Discoverability (anti-island) | Query `note_links` for inbound edges from outside `documentation/openclaw/` | Each new note in-degree ≥1 via `entry_openclaw_docs.md` (+ any `repo_openclaw*`/`term_*` inlinks added per the Inlinks section). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
cd /path/to/vault

# Resolve config-driven paths
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")

# --- Gate sweep over this sub-plan's output folder ---
GATE_DIR="resources/documentation/openclaw"
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"

NOTES="oc_plugins_reference_elevenlabs oc_plugins_reference_exa oc_plugins_reference_fal \
oc_plugins_reference_feishu oc_plugins_reference_file_transfer oc_plugins_reference_firecrawl \
oc_plugins_reference_fireworks"

# G1: format + YAML frontmatter per note
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  python3 scripts/check_yaml_frontmatter.py --path "$f"
  # required H2 sections present
  for s in ${(s:|:)REQ_SECTIONS}; do grep -q "^$s" "$f" || echo "MISSING SECTION [$s] in $f"; done
  # source_url required
  if [ "$REQUIRE_SOURCE_URL" = "1" ]; then grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $f"; done
done

# G3: density caps (lines ≤400, words ≤2500, fences ≤6)
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  awk -v F="$f" 'END{ if(NR>400) print "LINES>"NR" "F }' "$f"
  w=$(wc -w < "$GATE_DIR/$n.md"); [ "$w" -gt 2500 ] && echo "WORDS>$w $n"
  fences=$(( $(grep -c '```' "$GATE_DIR/$n.md") / 2 )); [ "$fences" -gt 6 ] && echo "FENCES>$fences $n"
done

# G4: sibling oc_ link present in each note's Related Notes
for n in ${=NOTES}; do grep -q "($SIBLING_PREFIX" "$GATE_DIR/$n.md" || echo "NO sibling $SIBLING_PREFIX link in $n"; done

# G5: ghost-reference — every cited target resolves in DB (run after reindex)
#   (handled by /tessellum-fix-ghost-references; manual spot-check:)

# Reindex + broken-link gate
bash scripts/update_notes_database.sh
# G6: /tessellum-fix-broken-links   G7/G8: verify in-degree
for n in ${=NOTES}; do
done
```

## Density Re-Assessment

| Note | Source words | Est. note words | Lines | Fences | Within caps (≤400L/≤2500w/≤6f)? |
|---|---:|---:|---:|---:|---|
| oc_plugins_reference_elevenlabs | 70 | 280 | ~70 | 0–1 | ✅ |
| oc_plugins_reference_exa | 50 | 250 | ~65 | 0–1 | ✅ |
| oc_plugins_reference_fal | 58 | 270 | ~68 | 0–1 | ✅ |
| oc_plugins_reference_feishu | 68 | 270 | ~68 | 0–1 | ✅ |
| oc_plugins_reference_file_transfer | 91 | 290 | ~72 | 0–1 | ✅ |
| oc_plugins_reference_firecrawl | 68 | 280 | ~70 | 0–1 | ✅ |
| oc_plugins_reference_fireworks | 54 | 250 | ~65 | 0–1 | ✅ |

All notes far below every cap. The risk here is the *opposite* of over-compression: do NOT pad a 50-word stub
into a 2,500-word essay. Keep notes lean — Overview + Distribution + Surface + Related Notes + References — and
push depth into the linked term/provider/tool/channel notes rather than inventing content not on the page (G2).

## Entry Point Decision (inherited from master)

`entry_openclaw_docs.md` is created as a master pre-step (W1). This sub-plan **contributes 7 rows** to its
Plugins / sub-plan tables (one per planned note), and the hub provides the required inbound link satisfying
G7/G8 for each note. No new entry point is created by this sub-plan (the series hub already exists). After
execution, append the 7 `oc_plugins_reference_*` rows to the Plugins section of `entry_openclaw_docs.md` and
mark the `pl10` sub-plan row complete.

## Inlinks (existing notes → new notes)

Candidate inbound links from OUTSIDE `documentation/openclaw/` for G7/G8 (each new note must RECEIVE ≥1):

- `0_entry_points/entry_openclaw_docs.md` ✅ (planned master pre-step) → all 7 notes (primary anti-island link).
- `areas/code_repos/repo_openclaw_extensions_voice_speech.md` ✅ → `oc_plugins_reference_elevenlabs` (speech plugin ↔ voice/speech extension).
- `areas/code_repos/repo_openclaw_extensions_llm_providers.md` ✅ → `oc_plugins_reference_fal`, `oc_plugins_reference_fireworks` (provider plugins ↔ LLM-provider extensions).
- `areas/code_repos/repo_openclaw_channels_messaging.md` ✅ / `repo_openclaw_channels.md` ✅ → `oc_plugins_reference_feishu` (channel plugin ↔ messaging channels).
- `areas/code_repos/repo_openclaw_gateway.md` ✅ → `oc_plugins_reference_file_transfer` (node.invoke transport ↔ gateway).
- `areas/code_repos/repo_openclaw_extensions.md` ✅ → `oc_plugins_reference_exa`, `oc_plugins_reference_firecrawl` (and all, as the plugin framework).
- `resources/term_dictionary/term_text_to_speech.md` ✅ → `oc_plugins_reference_elevenlabs`; `resources/term_dictionary/term_provider_plugin.md` ✅ → `oc_plugins_reference_fal`/`_fireworks`; `resources/term_dictionary/term_information_retrieval.md` ✅ → `oc_plugins_reference_exa`/`_firecrawl` (term ↔ usage, optional reciprocal backlinks added via `/tessellum-add-inlinks` at execute).

execute via `/tessellum-add-inlinks`); the entry-point link alone satisfies the G7/G8 floor.

## Pacing Rules (inherited from master)

- Cap dynamic-workflow fan-out at ~30 agents/run; embed the per-note manifest in the execution script.
- `git pull --rebase --autostash origin main` before committing; commit per wave; **no Claude co-author trailer**;
  `git push origin main` in the same turn as each commit.
- Reindex incrementally per wave (`bash scripts/update_notes_database.sh`); verify `note_links` populated +
  0 broken links before commit. Pilot 1 note (e.g. `oc_plugins_reference_elevenlabs`), reindex, verify links
  indexed, then fan out the remaining 6 (well under the fan-out cap).

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan (this sub-plan) | `/tessellum-plan-digestion` | 🟢 DONE (this file) |
| 2. Augment | `/tessellum-augment-digestion-plan` | 🟢 DONE (xref-augment 2026-06-21 — see Augmentation Report) |
| 3. Review | `/tessellum-review-digestion-plan` | 🟢 DONE — READY (9/9, see Review Sign-Off) |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |

## Augmentation Report (2026-06-21)

**Scope of this pass (xref-augment):** locked the Per-Note Related Notes Mapping at the **raised floors
(≥8 terms · ≥10 snippets · ≥10 docs per note)**, replacing the draft "Candidate Cross-References" candidate
sets. All 7 source pages under `inbox/openclaw_docs/plugins/reference/` were re-read (elevenlabs 70w, exa 50w,
fal 58w, feishu 68w, file-transfer 91w, firecrawl 68w, fireworks 54w — measured counts confirm the plan's
`hermes_agent/`, `claude_code/`, `pi/`, `band/`, and `aws_bedrock/` + 1–2 planned sibling `oc_*` docs
(this series; backticked, not linked).

**Per-note locked counts (terms / snippets / docs / repos):**

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met |
|---|---:|---:|---:|---:|---|
| oc_plugins_reference_elevenlabs | 10 | 11 | 11 (9/2) | 4 | ✅ |
| oc_plugins_reference_exa | 10 | 10 | 11 (9/2) | 3 | ✅ |
| oc_plugins_reference_fal | 11 | 11 | 11 (9/2) | 3 | ✅ |
| oc_plugins_reference_feishu | 11 | 11 | 11 (9/2) | 4 | ✅ |
| oc_plugins_reference_file_transfer | 10 | 11 | 10 (9/1) | 4 | ✅ |
| oc_plugins_reference_firecrawl | 10 | 10 | 11 (9/2) | 3 | ✅ |
| oc_plugins_reference_fireworks | 11 | 10 | 11 (9/2) | 3 | ✅ |

**New-term candidates:** **none.** The xref-augment surfaced no genuinely cross-cutting, vault-reusable
concept lacking an existing note. The plugin themes (TTS/STT/realtime transcription, web search/fetch,
image/music/video generation, enterprise chat channel, node file transfer, model provider) all map cleanly
`term_realtime_transcription`, `term_information_retrieval`, `term_rag`, `term_diffusion_model`,
`term_provider_plugin`, `term_messaging_gateway`, `term_channel_kernel`, `term_tool_descriptor`, etc.).
This confirms the master's "near-0 new terms" expectation and the draft's Undigested Terms Plan
("New-term candidates: none"). Narrow contract labels (`mediaUnderstandingProviders`, `webFetchProviders`,
`musicGenerationProviders`) remain best handled by linking the nearest existing term + glossing in-note —
NOT captured as `term_dictionary` entries (named contract strings, not reusable concepts). Best-fit glossary
for any future capture would be `0_entry_points/acronym_glossary_gen_ai.md` (the agentic/LLM glossary), but
no capture is required for this sub-plan.

**Issues found / fixed:** the draft's Candidate Cross-References met only the master's old ≥6-term floor with
2–4 snippets and 1 doc per note (far short of the raised ≥10/≥10 floors). The xref-augment expanded every
note to ≥10 snippets and ≥10 docs from the verified corpora, added a per-link relevance statement to each,
and rendered all existing targets as proper indexed `[text](relpath.md)` links with correct relative paths
from `resources/documentation/openclaw/`. No other issues.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE present (G1–G6, G7/G8, G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table covers G1 Format/YAML, G2 Grounding, G3 Density+Coverage, G4 Cross-reference, G5 Ghost-reference, G6 Broken-link, G7/G8 Discoverability (in-degree ≥1). |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` inherits `entry_openclaw_docs.md` (master W1 pre-step, >30-note series ⇒ CREATE); this sub-plan contributes 7 Plugins rows; DB confirms the hub is not-yet-created (planned), correct per W1. |
| CP4 | Size | **PASS** | 7 planned notes (≤30); single execution phase; no split strategy needed. |
| CP5 | Format derived | **PASS** | Format inherited verbatim from master's Format Definition, which is derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora: `# OpenClaw — …` H1, `## Overview` opener, source-mirrored H2s, `## Related Notes`, `## References`, bold footer; forbidden-field list present. |
| CP6 | Density | **PASS** | Density Re-Assessment: all 7 notes 250–290 est. words / ~65–72 lines / 0–1 fences — far below ≤2500w/≤400L/≤6f. Opposite risk (over-padding a stub) flagged with a do-not-pad instruction. |
| CP7 | Sources measured | **PASS** | All 7 source pages re-read at xref-augment; measured words (70/50/58/68/91/68/54) match the plan's Source table exactly (459w sum). |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present with disposition per surfaced term (all → link existing or in-note gloss); New-term candidates: none. `## Term-Note Authoring Requirements` = N/A (0 new terms) — correct; no `/tessellum-capture-term-note` obligation. |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new term slugs planned ⇒ no specificity/collision risk. All-notes dedup: the 7 planned `oc_plugins_reference_*` doc notes are plugin-manifest cards (model BB) with no existing `term_*`/doc duplicate — each plugin links to (does not recreate) its `term_*` concepts and `repo_openclaw_extensions*` code notes. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
