---
title: "Sub-Plan pl11 — OpenClaw Docs: Plugins (reference — github-copilot, gmi, google, google-meet, googlechat, gradium, groq)"
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - plugins/reference/github-copilot
  - plugins/reference/gmi
  - plugins/reference/google
  - plugins/reference/google-meet
  - plugins/reference/googlechat
  - plugins/reference/gradium
  - plugins/reference/groq
---

# Sub-Plan pl11: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format, dedup-before-create, 9-GATE validation, undigested-terms ownership, cross-refs, and entry-point wiring are ALL inherited from the master.
> The 7 assigned pages are micro-stub plugin-inventory cards (`## Distribution` / `## Surface` / `## Related docs`, 48–75 words, 0 code each); per the atomicity + density rules they consolidate by contract/BB cluster into 4 `oc_` procedure notes, not 1-per-page.

## Scope

The 7 alphabetically-contiguous `plugins/reference/*` inventory cards for the `g*` plugins: model/inference providers (`github-copilot`, `gmi`, `google`, `groq`), a text-to-speech provider (`gradium`), a chat channel (`googlechat`), and a meeting-participant tool (`google-meet`). Each card states only the npm package name, install route (included-in-OpenClaw vs npm/ClawHub), the capability surface it registers (`providers:` / `channels:` / `contracts:`), and a pointer to the corresponding `providers/*`, `channels/*`, or `plugins/*` deep-dive page (out of this sub-plan's scope — owned by `pr03`/`pr04`, `ch02`, `pl03`).

Priority **P3** (Phase C — plugin-reference sprawl). These cards are thin "what package provides what capability" inventory entries; their value is the npm-package ↔ capability-surface ↔ deep-dive-page mapping, not conceptual depth. The substantive OpenClaw code-side notes (`repo_openclaw_extensions`, `repo_openclaw_extensions_llm_providers`, `repo_openclaw_extensions_voice_speech`, `repo_openclaw_channels*`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, 419 measured words. **Planned: 4 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| GitHub Copilot plugin | plugins/reference/github-copilot | 60 | 0 | 3 | 0 | procedure |
| Gmi plugin | plugins/reference/gmi | 52 | 0 | 3 | 0 | procedure |
| Google plugin | plugins/reference/google | 75 | 0 | 3 | 0 | procedure |
| Google Meet plugin | plugins/reference/google-meet | 67 | 0 | 3 | 0 | procedure |
| Google Chat plugin | plugins/reference/googlechat | 61 | 0 | 3 | 0 | procedure |
| Gradium plugin | plugins/reference/gradium | 48 | 0 | 3 | 0 | procedure |
| Groq plugin | plugins/reference/groq | 56 | 0 | 3 | 0 | procedure |

Totals: 419 words, 0 code fences, 21 H2 (3 identical per page: `## Distribution`, `## Surface`, `## Related docs`), 0 H3. All BBs are procedure (install/enable/configure a plugin to register a capability surface).

## Content Strategy

- **Prioritize**: the npm-package → capability-surface → deep-dive-page mapping (the only durable content), and the install-route distinction (included-in-OpenClaw vs `npm` vs `clawhub:@openclaw/...`). These are what a user/operator actually needs from a plugin-inventory card.
- **Consolidate (not split)**: each page is a 48–75-word micro-stub — far below the 1-note atomic floor on its own. Grouping by capability contract keeps each note a focused, single-BB "how to enable this class of g* plugin" procedure while staying well under all density caps (4 notes × ≤300w). One note per page would create 7 near-empty notes that fail the substantive-content bar and bloat the graph.
- **Link-out (owned elsewhere)**: each card's `## Related docs` pointer (`/providers/github-copilot`, `/providers/gmi`, `/providers/google`, `/providers/groq`, `/providers/gradium`, `/channels/googlechat`, `/plugins/google-meet`) is the deep-dive page for that integration — owned by other sub-plans (`pr03`, `pr04`, `ch02`, `pl03`). This sub-plan links those as `## References` / sibling pointers and does NOT duplicate their config detail. Provider/channel/speech vocabulary links existing `term_*` notes; nothing is redefined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_g_model_providers.md` | procedure | github-copilot.md, gmi.md, google.md, groq.md (all 3 H2 each) | 280 | The four `g*` model/inference provider plugins: GitHub Copilot (`@openclaw/github-copilot-provider`, built-in), GMI Cloud (`@openclaw/gmi-provider`, npm/ClawHub), Google (`@openclaw/google-plugin`, built-in; Gemini CLI + Vertex + 7 media contracts), and Groq (`@openclaw/groq-provider`, npm/ClawHub). Per-plugin package, install route, registered `providers:` ids, and extra `contracts:` (embedding/media/speech/image/video/music/web-search). |
| 2 | `oc_plugins_reference_gradium_speech_provider.md` | procedure | gradium.md (all 3 H2) | 180 | The Gradium text-to-speech provider plugin (`@openclaw/gradium-speech`, npm/ClawHub: `clawhub:@openclaw/gradium-speech`), registering the `speechProviders` contract; install route and capability surface. |
| 3 | `oc_plugins_reference_googlechat_channel.md` | procedure | googlechat.md (all 3 H2) | 190 | The Google Chat channel plugin (`@openclaw/googlechat`, npm/ClawHub) for spaces and direct messages, registering the `channels: googlechat` surface; install route and pointer to the channel deep-dive. |
| 4 | `oc_plugins_reference_google_meet_tool.md` | procedure | google-meet.md (all 3 H2) | 190 | The Google Meet participant plugin (`@openclaw/google-meet`, npm/ClawHub) for joining calls via Chrome or Twilio transports, registering the `tools` contract; install route and pointer to the plugin deep-dive. |

Filename convention: `oc_` + full slug with `/` and `-` → `_`. Note 1 is a consolidation of the four model-provider `g*` cards (single contract class) and so takes a descriptive grouped slug (`oc_plugins_reference_g_model_providers`) rather than any one page slug; notes 2–4 keep their single-page slug (`gradium` → `gradium_speech_provider`, `googlechat` → `googlechat_channel`, `google-meet` → `google_meet_tool`) with a short aspect suffix marking the capability class. See Split Decisions.

## Section Coverage Map

```
plugins/reference/github-copilot.md
├── Distribution (pkg @openclaw/github-copilot-provider, included in OpenClaw) → note 1
├── Surface (providers: github-copilot; contracts: memoryEmbeddingProviders) → note 1
└── Related docs (/providers/github-copilot) ─────────────────────────────── → note 1 (References pointer)
plugins/reference/gmi.md
├── Distribution (pkg @openclaw/gmi-provider, npm / ClawHub) ──────────────── → note 1
├── Surface (providers: gmi, gmi-cloud, gmicloud) ────────────────────────── → note 1
└── Related docs (/providers/gmi) ───────────────────────────────────────── → note 1 (References pointer)
plugins/reference/google.md
├── Distribution (pkg @openclaw/google-plugin, included in OpenClaw) ──────── → note 1
├── Surface (providers: google/google-gemini-cli/google-vertex; 7 contracts) → note 1
└── Related docs (/providers/google) ────────────────────────────────────── → note 1 (References pointer)
plugins/reference/groq.md
├── Distribution (pkg @openclaw/groq-provider, npm / ClawHub) ─────────────── → note 1
├── Surface (providers: groq; contracts: mediaUnderstandingProviders) ─────── → note 1
└── Related docs (/providers/groq) ──────────────────────────────────────── → note 1 (References pointer)
plugins/reference/gradium.md
├── Distribution (pkg @openclaw/gradium-speech, npm / ClawHub) ────────────── → note 2
├── Surface (contracts: speechProviders) ────────────────────────────────── → note 2
└── Related docs (/providers/gradium) ───────────────────────────────────── → note 2 (References pointer)
plugins/reference/googlechat.md
├── Distribution (pkg @openclaw/googlechat, npm / ClawHub) ────────────────── → note 3
├── Surface (channels: googlechat) ──────────────────────────────────────── → note 3
└── Related docs (/channels/googlechat) ─────────────────────────────────── → note 3 (References pointer)
plugins/reference/google-meet.md
├── Distribution (pkg @openclaw/google-meet, npm / ClawHub) ───────────────── → note 4
├── Surface (contracts: tools) ──────────────────────────────────────────── → note 4
└── Related docs (/plugins/google-meet) ─────────────────────────────────── → note 4 (References pointer)
```

No orphaned sections: every H2 of every page maps to a planned note. Each card's `## Related docs` pointer is preserved as a `## References` external link (the deep-dive page is owned by `pr03`/`pr04`/`ch02`/`pl03`, not duplicated here).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| github-copilot.md + gmi.md + google.md + groq.md (60+52+75+56 = 243w combined) | **CONSOLIDATED into note 1** | Four micro-stubs of the same BB (procedure) and same capability class (`providers:` model/inference) — each below the atomic floor alone; one focused "g* model-provider plugins" note (~280w) is the correct atomic unit and stays far under all caps. NOT a split — a consolidation. |
| gradium.md (48w) | note 2 (standalone) | Distinct capability class (`speechProviders` / TTS); kept its own note so the speech-provider contract is discoverable on its own, even though tiny. |
| googlechat.md (61w) | note 3 (standalone) | Distinct BB-relevant capability class (`channels:`); a channel plugin is a different integration shape than a model provider; kept standalone. |
| google-meet.md (67w) | note 4 (standalone) | Distinct capability class (`contracts: tools` — a meeting-participant tool via Chrome/Twilio); kept standalone. |

No page exceeds 2,500 words or mixes BBs, so no word-cap or mixed-BB *split* is needed. The only structural decision is the inverse — consolidating four same-class micro-stubs (note 1).

## Summary Statistics & Building Block Distribution

- Source pages: 7 (419 words total). New `oc_` notes: **4**. New `term_dictionary` notes: **0**.
- BB distribution: procedure ×4 (notes 1–4). No concept/model/argument notes (these are install/enable cards).
- Est. digest words ~840 (avg ~210/note); max note ~280w. 0 source code fences → 0 code blocks in any note (well under the ≤6 cap; package names/contract ids rendered inline as `code`).
- Density: every note ≤300 words, ≤400 lines, 0 code blocks, single BB — no note approaches any cap.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`: terms `../../term_dictionary/term_Y.md`; sibling oc docs `oc_Y.md`; other docs `../<folder>/<file>.md`; repos `../../../areas/code_repos/repo_Y.md`; snippets `../../code_snippets/snippet_Y.md`.

### oc_plugins_reference_g_model_providers (12t · 14s · 14d)

The four `g*` model/inference provider plugins (GitHub Copilot, GMI Cloud, Google/Gemini-CLI/Vertex, Groq) — npm package, install route, registered `providers:` ids, and extra `contracts:` (embedding / media-understanding / image / video / music / speech / web-search). Sourced from github-copilot.md, gmi.md, google.md, groq.md.

**Terms** (12)
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — plugin that registers a model/inference provider with the agent host; relevance: the exact BB of all four cards — each registers `providers:` ids via a provider plugin.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the model class Copilot/GMI/Google/Groq all serve.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI inference vendors; relevance: GMI Cloud, Groq, and Google are exactly such external services wired in via plugin.
- [model catalog](../../term_dictionary/term_model_catalog.md) — registry of available models per provider; relevance: each provider plugin contributes its models to the host's catalog.
- [model router](../../term_dictionary/term_model_router.md) — selects which provider/model serves a request; relevance: registering multiple `g*` providers gives the router more routing targets.
- [provider routing](../../term_dictionary/term_provider_routing.md) — routing requests across registered providers; relevance: the four plugins expand the routable provider set.
- [model failover](../../term_dictionary/term_model_failover.md) — fall back to an alternate provider on error; relevance: multiple registered `g*` providers enable failover chains.
- [function calling](../../term_dictionary/term_function_calling.md) — model invoking declared tools; relevance: the inference providers these plugins register expose tool/function-calling surfaces.
- [embedding](../../term_dictionary/term_embedding.md) — vector representation for retrieval; relevance: Copilot + Google register the `memoryEmbeddingProviders` contract.
- [structured output](../../term_dictionary/term_structured_output.md) — schema-constrained model responses; relevance: a capability the registered model providers expose to the agent.
- [npm](../../term_dictionary/term_npm.md) — Node package manager / registry; relevance: GMI and Groq install via npm / ClawHub (Copilot + Google are built-in).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway these plugins extend; relevance: the product whose provider surface these cards register against.

**Docs** (14: 9 existing + 5 planned-this-series)
- [Hermes: cloud inference providers](../hermes_agent/hermes_inference_providers_cloud.md) — the cloud-provider catalog in the Hermes corpus; relevance: closest analog — same "list of hosted model providers" surface as these four cards.
- [Hermes: adding an inference provider](../hermes_agent/hermes_adding_inference_provider.md) — how to register a new provider; relevance: the procedure these install cards are the inventory entries for.
- [Hermes: model provider plugin](../hermes_agent/hermes_model_provider_plugin.md) — the provider-plugin shape in Hermes; relevance: structural twin of the `g*` provider plugins.
- [Hermes: provider routing & proxies](../hermes_agent/hermes_provider_routing_proxies.md) — routing/proxying across providers; relevance: explains how the registered `g*` providers are selected at runtime.
- [Hermes: Google Gemini provider](../hermes_agent/hermes_provider_google_gemini.md) — the Gemini provider in Hermes; relevance: direct analog of the google.md card (Gemini CLI + Vertex).
- [Hermes: AWS Bedrock provider](../hermes_agent/hermes_provider_aws_bedrock.md) — a hosted model provider plugin; relevance: another provider-card analog in the sibling corpus.
- [pi: cloud providers](../pi/pi_cloud_providers.md) — pi's hosted-provider list; relevance: same provider-inventory pattern in the pi docs.
- [pi: provider auth](../pi/pi_provider_auth.md) — credentials for hosted providers; relevance: the auth step a user does after installing one of these `g*` provider plugins.
- [Claude Code: LLM gateway](../claude_code/cc_llm_gateway.md) — routing LLM traffic through a gateway; relevance: gateway-side framing of the provider surface these plugins register.
- [OpenClaw plugins reference index (planned, this series)](oc_plugins_reference_index.md) — the reference landing page; relevance: parent inventory page these cards sit under.
- [OpenClaw providers add-provider (planned, this series)](oc_providers_add_provider.md) — the provider deep-dive owned by pr03/pr04; relevance: the `## Related docs` target each `g*` card points to.
- [oc_plugins_reference_gradium_speech_provider (planned, this series)](oc_plugins_reference_gradium_speech_provider.md) — sibling provider-plugin card (speech class); relevance: contrast — a non-model provider plugin in this same sub-plan.
- [oc_plugins_reference_googlechat_channel (planned, this series)](oc_plugins_reference_googlechat_channel.md) — sibling channel-plugin card; relevance: contrasts the `providers:` surface with a `channels:` surface.
- [oc_plugins_reference_google_meet_tool (planned, this series)](oc_plugins_reference_google_meet_tool.md) — sibling tool-plugin card; relevance: contrasts `providers:` with a `contracts: tools` surface.

**Repos** (4)
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the LLM-provider extension package family; relevance: where the `@openclaw/*-provider` packages in these cards actually live.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: loads and resolves these provider plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the host gateway repo; relevance: the product these plugins extend.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — Hermes provider adapters; relevance: code-side analog of the provider plugins these cards describe.

**Snippets** (14)
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw OpenAI provider impl; relevance: the canonical provider-plugin code shape these `g*` cards mirror.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — OpenClaw Anthropic provider impl; relevance: a built-in provider plugin (like Copilot/Google) in code.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider impl; relevance: shows a provider plugin registering multiple `providers:` ids (cf. GMI's gmi/gmi-cloud/gmicloud).
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local provider impl; relevance: contrast — a non-cloud provider plugin of the same shape.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: where the models a `g*` provider registers land.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planner; relevance: plans the catalog these provider plugins contribute to.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: the entrypoint mechanism a `@openclaw/*-provider` package uses to register its surface.
- [snippet_openclaw_agents_context_anthropic_prefix](../../code_snippets/snippet_openclaw_agents_context_anthropic_prefix.md) — provider-specific context prefixing; relevance: provider-plugin-level request shaping.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: how registered `providers:` ids are tracked (the surface each card declares).
- [snippet_hermes_agent_plugins_provider_copilot](../../code_snippets/snippet_hermes_agent_plugins_provider_copilot.md) — Copilot provider plugin impl; relevance: exact code analog of the github-copilot.md card.
- [snippet_hermes_agent_core_gemini_native_adapter_request](../../code_snippets/snippet_hermes_agent_core_gemini_native_adapter_request.md) — Gemini native adapter; relevance: code analog of the google.md card (Gemini provider request path).
- [snippet_hermes_agent_core_gemini_native_adapter_init](../../code_snippets/snippet_hermes_agent_core_gemini_native_adapter_init.md) — Gemini adapter init; relevance: provider-plugin init path for the Google card.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base class; relevance: the abstract contract every model-provider plugin implements.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — CLI provider registry; relevance: how installed provider plugins are enumerated/selected.

### oc_plugins_reference_gradium_speech_provider (10t · 12s · 12d)

The Gradium text-to-speech provider plugin (`@openclaw/gradium-speech`, npm / `clawhub:@openclaw/gradium-speech`) registering the `speechProviders` contract; install route + capability surface. Sourced from gradium.md.

**Terms** (10)
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a provider with the host; relevance: Gradium is a provider plugin (speech class).
- [text to speech](../../term_dictionary/term_text_to_speech.md) — synthesizing audio from text; relevance: the exact capability Gradium adds (the card summary). (`term_tts`/`term_speech_synthesis` confirmed MISSING — `term_text_to_speech` is the verified TTS term.)
- [speech to text](../../term_dictionary/term_speech_to_text.md) — transcribing audio to text; relevance: sibling speech contract for contrast with `speechProviders`.
- [realtime transcription](../../term_dictionary/term_realtime_transcription.md) — streaming STT; relevance: adjacent speech-pipeline contract a TTS provider often pairs with.
- [voice mode](../../term_dictionary/term_voice_mode.md) — agent voice-interaction mode; relevance: the user-facing feature a `speechProviders` plugin powers.
- [multimodal](../../term_dictionary/term_multimodal.md) — handling audio/text/image jointly; relevance: speech providers extend the agent into the audio modality.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI vendors; relevance: Gradium is an external TTS vendor wired in via plugin.
- [tool gateway](../../term_dictionary/term_tool_gateway.md) — gateway exposing capabilities to the agent; relevance: the `speechProviders` contract is surfaced through the host gateway.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: Gradium installs via npm / ClawHub.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: the product Gradium registers its speech surface against.

**Docs** (12: 7 existing + 5 planned-this-series)
- [Hermes: TTS providers](../hermes_agent/hermes_tts_providers.md) — the TTS-provider catalog in Hermes; relevance: closest analog — same speech-provider surface Gradium registers.
- [Hermes: STT transcription](../hermes_agent/hermes_stt_transcription.md) — the STT side of the speech pipeline; relevance: sibling speech contract contrast.
- [Hermes: voice mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — enabling voice mode from CLI; relevance: the feature a `speechProviders` plugin enables.
- [Hermes: image-gen provider plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — a contract-registering media provider plugin; relevance: structural twin — a provider plugin that registers a single media contract (like `speechProviders`).
- [Hermes: video-gen provider plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — another single-contract media provider plugin; relevance: same plugin-shape analog as Gradium.
- [pi: custom provider registration](../pi/pi_custom_provider_registration.md) — registering a custom provider; relevance: the registration mechanism Gradium uses.
- [Claude Code: voice dictation](../claude_code/cc_voice_dictation.md) — voice-to-text in Claude Code; relevance: speech-capability analog in the cc corpus.
- [OpenClaw providers gradium deep-dive (planned, this series)](oc_providers_gradium.md) — the provider deep-dive owned by pr04; relevance: the `## Related docs` target this card points to.
- [OpenClaw plugins reference index (planned, this series)](oc_plugins_reference_index.md) — reference landing page; relevance: parent inventory page.
- [oc_plugins_reference_g_model_providers (planned, this series)](oc_plugins_reference_g_model_providers.md) — sibling provider-plugin card (model class); relevance: contrast — model `providers:` vs speech `contracts:`.
- [oc_plugins_reference_google_meet_tool (planned, this series)](oc_plugins_reference_google_meet_tool.md) — sibling tool-plugin card; relevance: voice/meeting adjacency.
- [oc_plugins_reference_googlechat_channel (planned, this series)](oc_plugins_reference_googlechat_channel.md) — sibling channel-plugin card; relevance: another single-surface plugin contrast.

**Repos** (3)
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — the voice/speech extension package family; relevance: where `@openclaw/gradium-speech` actually lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: loads the Gradium plugin.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — host gateway repo; relevance: the product Gradium extends.

**Snippets** (12)
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS provider impl; relevance: exact code analog — a `speechProviders` TTS plugin like Gradium.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS impl; relevance: contrast — a local `speechProviders` plugin of the same shape.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT impl; relevance: the STT-provider counterpart to the TTS contract Gradium registers.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline assembly; relevance: where a registered `speechProviders` plugin plugs in.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: how `@openclaw/gradium-speech` registers its surface.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — audio media-stream handling; relevance: downstream consumer of synthesized speech.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — transcription stream; relevance: the STT side that pairs with Gradium TTS in a voice loop.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing across providers; relevance: how a registered speech provider is selected.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: sibling speech-tool wiring.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: the feature a `speechProviders` plugin powers.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: how Gradium's registered speech provider is tracked.

### oc_plugins_reference_googlechat_channel (10t · 11s · 11d)

The Google Chat channel plugin (`@openclaw/googlechat`, npm / ClawHub) for spaces and direct messages, registering `channels: googlechat`; install route + deep-dive pointer. Sourced from googlechat.md.

**Terms** (10)
- [chatbot](../../term_dictionary/term_chatbot.md) — automated conversational agent in a chat platform; relevance: what a Google Chat channel plugin makes the agent behave as.
- [conversational AI](../../term_dictionary/term_conversational_ai.md) — multi-turn dialogue systems; relevance: the interaction model a chat channel enables.
- [Slack](../../term_dictionary/term_slack.md) — a chat platform integration; relevance: sibling chat-channel analog (same `channels:` surface, different platform).
- [channel adapter](../../term_dictionary/term_channel_adapter.md) — translates platform events to the agent's channel model; relevance: the component a `channels: googlechat` plugin supplies.
- [messaging gateway](../../term_dictionary/term_messaging_gateway.md) — gateway routing chat-platform traffic; relevance: where the googlechat channel attaches.
- [webhook](../../term_dictionary/term_webhook.md) — HTTP callback for inbound events; relevance: Google Chat delivers events to the channel via webhook/HTTP ingress.
- [block kit](../../term_dictionary/term_block_kit.md) — structured chat message UI blocks; relevance: rich-message rendering a chat channel adapter handles.
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a surface with the host; relevance: the registration shape (here a `channels:` surface, not `providers:`).
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: googlechat installs via npm / ClawHub.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: the product this channel plugin registers against.

**Docs** (11: 6 existing + 5 planned-this-series)
- [Hermes: Google Chat messaging](../hermes_agent/hermes_messaging_google_chat.md) — the exact Google Chat integration in the Hermes corpus; relevance: closest analog — same platform, same channel surface.
- [Hermes: messaging gateway architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — how chat channels attach to the gateway; relevance: the architecture a `channels: googlechat` plugin slots into.
- [Hermes: adding a platform adapter plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — building a channel/platform plugin; relevance: the procedure this install card is the inventory entry for.
- [Hermes: Slack messaging](../hermes_agent/hermes_messaging_slack.md) — Slack channel integration; relevance: sibling channel-plugin analog.
- [Claude Code: channels setup](../claude_code/cc_channels_setup.md) — setting up chat channels; relevance: channel-install analog in the cc corpus.
- [Claude Code: Slack setup & routing](../claude_code/cc_slack_setup_and_routing.md) — Slack channel config + routing; relevance: sibling chat-channel setup pattern.
- [OpenClaw channels googlechat deep-dive (planned, this series)](oc_channels_googlechat.md) — the channel deep-dive owned by ch02; relevance: the `## Related docs` target this card points to.
- [OpenClaw plugins reference index (planned, this series)](oc_plugins_reference_index.md) — reference landing page; relevance: parent inventory page.
- [oc_plugins_reference_g_model_providers (planned, this series)](oc_plugins_reference_g_model_providers.md) — sibling plugin card (model class); relevance: contrast — `channels:` vs `providers:` surface.
- [oc_plugins_reference_google_meet_tool (planned, this series)](oc_plugins_reference_google_meet_tool.md) — sibling tool-plugin card; relevance: other Google integration in this sub-plan.
- [oc_plugins_reference_gradium_speech_provider (planned, this series)](oc_plugins_reference_gradium_speech_provider.md) — sibling provider-plugin card; relevance: single-surface plugin contrast.

**Repos** (3)
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — the messaging-channel package family; relevance: where `@openclaw/googlechat` actually lives.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel framework; relevance: loads/normalizes the googlechat channel.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — host gateway repo; relevance: the product this channel plugin extends.

**Snippets** (11)
- [snippet_hermes_agent_plugins_platform_google_chat](../../code_snippets/snippet_hermes_agent_plugins_platform_google_chat.md) — Google Chat platform plugin impl; relevance: exact code analog of the googlechat.md card.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: how a registered `channels: googlechat` surface is normalized.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket-mode channel impl; relevance: sibling channel-plugin code shape.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord channel intents; relevance: another channel-plugin analog.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — chat session typing; relevance: how spaces vs direct-message sessions (the googlechat card's scope) are typed.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel-source security audit; relevance: validating inbound events from a registered channel.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — gateway channel directory; relevance: how installed channel plugins are enumerated.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Slack gateway platform impl; relevance: sibling channel-platform code.
- [snippet_hermes_agent_gw_platform_mattermost](../../code_snippets/snippet_hermes_agent_gw_platform_mattermost.md) — Mattermost gateway platform impl; relevance: another spaces/DM-style chat channel analog.
- [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — outbound message delivery; relevance: the send path a chat channel plugin uses.
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel config; relevance: how a `channels: googlechat` plugin is configured.

### oc_plugins_reference_google_meet_tool (12t · 12s · 11d)

The Google Meet participant plugin (`@openclaw/google-meet`, npm / ClawHub) for joining calls via Chrome or Twilio transports, registering `contracts: tools`; install route + deep-dive pointer. Sourced from google-meet.md.

**Terms** (12)
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — plugin registering a surface with the host; relevance: the registration shape (here a `contracts: tools` surface).
- [function calling](../../term_dictionary/term_function_calling.md) — model invoking declared tools; relevance: the `tools` contract this plugin registers is consumed via function calling.
- [tool registry](../../term_dictionary/term_tool_registry.md) — registry of agent-callable tools; relevance: where the Google Meet tool lands once the plugin registers `contracts: tools`.
- [tool descriptor](../../term_dictionary/term_tool_descriptor.md) — schema describing a callable tool; relevance: the descriptor the plugin contributes for the meeting tool.
- [browser automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: the Chrome transport joins the call via browser automation.
- [CDP](../../term_dictionary/term_cdp.md) — Chrome DevTools Protocol; relevance: the protocol the Chrome transport drives to join a Meet call.
- [webhook](../../term_dictionary/term_webhook.md) — HTTP callback; relevance: the Twilio transport uses webhook callbacks for call media/events.
- [voice call](../../term_dictionary/term_voice_call.md) — telephony/voice call handling; relevance: the Twilio transport joins via a voice-call path.
- [VoIP](../../term_dictionary/term_voip.md) — voice over IP; relevance: the call-media layer the Twilio transport rides.
- [multimodal](../../term_dictionary/term_multimodal.md) — joint audio/text/video; relevance: a meeting participant ingests live audio/video.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: google-meet installs via npm / ClawHub.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: the product this tool plugin registers against.

**Docs** (11: 6 existing + 5 planned-this-series)
- [Hermes: Teams meetings pipeline (built-in plugins)](../hermes_agent/hermes_built_in_plugins.md) — built-in plugin inventory incl. meeting/participant tools; relevance: closest analog — meeting-participant plugin in the Hermes corpus.
- [Claude Code: Chrome browser automation](../claude_code/cc_chrome_browser_automation.md) — driving Chrome programmatically; relevance: the exact mechanism of the Chrome transport for joining a Meet call.
- [Claude Code: Chrome setup & troubleshooting](../claude_code/cc_chrome_setup_and_troubleshooting.md) — Chrome automation setup; relevance: the setup a user does to enable the Chrome transport.
- [Hermes: browser automation setup](../hermes_agent/hermes_browser_automation_setup.md) — configuring browser automation; relevance: Chrome-transport setup analog.
- [Hermes: browser automation backends](../hermes_agent/hermes_browser_automation_backends.md) — browser backend options; relevance: the Chrome backend the Meet tool drives.
- [Hermes: tools reference — platform media](../hermes_agent/hermes_tools_reference_platform_media.md) — media-handling tools; relevance: the media surface a meeting-participant tool uses.
- [OpenClaw plugins google-meet deep-dive (planned, this series)](oc_plugins_google_meet.md) — the plugin deep-dive owned by pl03; relevance: the `## Related docs` target this card points to.
- [OpenClaw plugins reference index (planned, this series)](oc_plugins_reference_index.md) — reference landing page; relevance: parent inventory page.
- [oc_plugins_reference_googlechat_channel (planned, this series)](oc_plugins_reference_googlechat_channel.md) — sibling Google integration; relevance: contrast — `channels:` vs `contracts: tools` surface.
- [oc_plugins_reference_gradium_speech_provider (planned, this series)](oc_plugins_reference_gradium_speech_provider.md) — sibling provider-plugin card; relevance: voice/speech adjacency for the call-media path.
- [oc_plugins_reference_g_model_providers (planned, this series)](oc_plugins_reference_g_model_providers.md) — sibling plugin card; relevance: contrast — `providers:` vs `contracts: tools` surface.

**Repos** (3)
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/call transport package family; relevance: the Twilio voice-call transport adjacency.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: loads the google-meet tool plugin.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — host gateway repo; relevance: the product this tool plugin extends.

**Snippets** (12)
- [snippet_hermes_agent_plugins_google_meet](../../code_snippets/snippet_hermes_agent_plugins_google_meet.md) — Google Meet plugin impl; relevance: exact code analog of the google-meet.md card.
- [snippet_hermes_agent_plugins_teams_pipeline](../../code_snippets/snippet_hermes_agent_plugins_teams_pipeline.md) — Teams meeting pipeline impl; relevance: sibling meeting-participant plugin in code.
- [snippet_hermes_agent_tools_browser_cdp](../../code_snippets/snippet_hermes_agent_tools_browser_cdp.md) — CDP browser driver; relevance: the Chrome-transport mechanism for joining a call.
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — browser navigation; relevance: navigating to the Meet URL via the Chrome transport.
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — browser session management; relevance: the session a Chrome-transport meeting tool holds.
- [snippet_hermes_agent_tools_browser_supervisor_lifecycle](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_lifecycle.md) — browser supervisor lifecycle; relevance: managing the Chrome instance the Meet tool drives.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser tool dispatch; relevance: dispatching browser actions a `contracts: tools` plugin registers.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice call manager; relevance: the Twilio voice-call transport path.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — call media transcription; relevance: transcribing meeting audio the participant ingests.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — call audio stream; relevance: the audio media a Twilio-transport meeting tool handles.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — Twilio webhook signature verify; relevance: securing the Twilio transport's webhook callbacks.
- [snippet_hermes_agent_gw_platform_sms](../../code_snippets/snippet_hermes_agent_gw_platform_sms.md) — SMS/Twilio platform impl; relevance: the Twilio integration shape the Twilio transport reuses.

## Undigested Terms Plan (Step 4e)

Per master, OpenClaw vocabulary is digested as `oc_` doc notes (these install cards), NOT new `term_dictionary` entries; existing terms are linked. **Expected 0 new `term_dictionary` captures** for pl11.

| Term | Disposition |
|---|---|
| GitHub Copilot (provider) | Documented as config in note 1; link existing `term_provider_plugin` / `term_llm` / `term_third_party_genai_services`. Provider name not promoted (no `term_github_copilot`, confirmed MISSING — names-as-config rule). |
| GMI / GMI Cloud (provider) | Config in note 1; link `term_provider_plugin` / `term_third_party_genai_services`. Not promoted. |
| Google / Gemini CLI / Vertex (providers) | Config in note 1; link `term_llm` / `term_provider_plugin`. Names not promoted (`term_gemini`/`term_vertex_ai` confirmed MISSING). |
| Groq (provider) | Config in note 1; link `term_provider_plugin` / `term_third_party_genai_services`. Not promoted. |
| Gradium (TTS provider) | Config in note 2; link existing `term_text_to_speech` / `term_provider_plugin`. Not promoted. |
| Google Chat (channel) | Config in note 3; link `term_chatbot` / `term_bot`. Not promoted (`term_chat_platform` MISSING). |
| Google Meet (tool/participant) | Config in note 4; link `term_function_calling` / `term_provider_plugin`. Not promoted (`term_video_conferencing` MISSING). |
| `speechProviders` / `memoryEmbeddingProviders` / `mediaUnderstandingProviders` / `tools` etc. (contracts) | OpenClaw capability-contract vocabulary → described in the `oc_` notes (and ultimately the `plugins/architecture`/`plugins/manifest` deep-dives owned by pl01/pl04); link `term_provider_plugin` / `term_embedding` / `term_function_calling`. Not new terms. |

**New-term candidates: none.** No genuinely cross-cutting, vault-reusable term lacking a home appears in these 7 cards — all are provider/channel/tool *names* (documented as config) or OpenClaw-internal contract ids (documented in the `oc_` notes). If augment's re-scan surfaces one, it would be captured via `/tessellum-capture-term-note` + added to `acronym_glossary_agentic_ai.md` (best-fit for agent/plugin vocabulary); not anticipated.

## Term-Note Authoring Requirements

**N/A (0 new terms).** pl11 authors zero `term_dictionary` notes (inherited from master). If augment proposes a new term, the master's multi-source-research + glossary-update requirement applies.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (4 notes, P3). All gates must PASS before commit.

| Gate | Check | Tooling | Pass criterion |
|---|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` | YAML field order/values valid; `# OpenClaw — …` H1; `## Overview` + `## Related Notes` present; bold footer. 0 ERROR/LINK-003. |
| G2 | Grounding | diff vs `inbox/openclaw_docs/plugins/reference/<page>.md` | Every package name, install route, and capability-surface id traces to source; no invented config. |
| G3 | Density + Coverage | `wc -w` / fence count | Each note ≤2500w / ≤6 code / ≤400L (all expected ≤300w, 0 code); all 21 H2 covered (Section Coverage Map). |
| G4 | Cross-Reference | link audit | ≥6 relevance-selected term links + repo/sibling/analog links per note, each with a relevance statement. |
| G6 | Broken-link | `/tessellum-fix-broken-links` | 0 broken relative paths after reindex. |
| G7/G8 | Discoverability / in-degree ≥1 | `note_links` query | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + candidate inlinks below); in-degree ≥1, no island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_g_model_providers oc_plugins_reference_gradium_speech_provider oc_plugins_reference_googlechat_channel oc_plugins_reference_google_meet_tool"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for s in "## Overview" "## Related Notes"; do
    grep -qF "$s" "$f" || echo "MISSING SECTION [$s] in $n"
  done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # density (frontmatter-stripped body word count + fence pairs)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w, $cb code)"
  # sibling/discoverability: ≥1 oc_ sibling link
  grep -q "($SIBLING_PREFIX" "$f" || echo "NO SIBLING ($SIBLING_PREFIX) link in $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# post-write: incremental reindex + in-degree (G7/G8)
bash scripts/update_notes_database.sh
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  [ "${indeg:-0}" -ge 1 ] && echo "$n in-degree(outside-folder)=$indeg OK" || echo "G8 FAIL: $n has no outside-folder inbound link"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_g_model_providers | procedure | 280 | 0 | ✅ |
| 2 | oc_plugins_reference_gradium_speech_provider | procedure | 180 | 0 | ✅ |
| 3 | oc_plugins_reference_googlechat_channel | procedure | 190 | 0 | ✅ |
| 4 | oc_plugins_reference_google_meet_tool | procedure | 190 | 0 | ✅ |

No note approaches any cap (≤2500w / ≤6 code / ≤400L). Source has 0 code fences, so notes render package names and contract ids inline; the only borderline concern is the *opposite* (under-thin), addressed by consolidating the four model-provider stubs into note 1 and by enriching each note with Overview context + the cross-reference web.

## Entry Point Decision (inherited from master)

Contributes **4 rows** to `entry_openclaw_docs.md` (created as a master pre-step, W1) under the **Plugins → Reference (g\*)** cluster — one row per note (note 1 covers 4 source pages; notes 2–4 one each). Each note receives its entry-point back-link at finalization (satisfies G7/G8 in-degree). No new entry point is created by this sub-plan; it is a contributor to the master's `entry_openclaw_docs.md`.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfy G7/G8):

- `entry_openclaw_docs.md` → notes 1, 2, 3, 4 (primary discoverability source — guaranteed ≥1 inbound each).
- `repo_openclaw_extensions_llm_providers.md` → note 1 (the package family these provider plugins ship in).
- `repo_openclaw_extensions_voice_speech.md` → note 2 (the speech-provider package family).
- `repo_openclaw_channels_messaging.md` → note 3 (the channel package family).
- `repo_openclaw_channels_voice_phone.md` → note 4 (the voice/call transport family — Twilio adjacency).
- `term_provider_plugin.md` → notes 1, 2 (canonical provider-plugin term; reciprocal back-link).
- `term_text_to_speech.md` → note 2; `term_chatbot.md` → note 3; `term_function_calling.md` → note 4 (reciprocal back-links).
- `term_openclaw.md` → notes 1–4 (host term, reciprocal).

## Pacing Rules (inherited from master)

Single phase, 4 notes — well under the ~30-agent fan-out cap. Re-read each of the 7 source cards; reproduce package names / install routes / capability-surface ids verbatim (inline `code`, 0 fenced blocks). One BB per note (all procedure). `git pull --rebase --autostash origin main` before commit; commit+push the phase as one cycle; no Claude co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links + G8 in-degree ≥1 before commit.

## Augmentation Report (2026-06-21)


**Per-note locked counts.**

| Note | Terms | Snippets | Docs (existing+planned) | Repos | Floors met (≥8t/≥10s/≥10d, ≥5 existing docs) |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_g_model_providers | 12 | 14 | 14 (9+5) | 4 | ✅ |
| oc_plugins_reference_gradium_speech_provider | 10 | 12 | 12 (7+5) | 3 | ✅ |
| oc_plugins_reference_googlechat_channel | 10 | 11 | 11 (6+5) | 3 | ✅ |
| oc_plugins_reference_google_meet_tool | 12 | 12 | 11 (6+5) | 3 | ✅ |


**New-term candidates: none.** The re-read surfaced no cross-cutting, vault-reusable term lacking a home. All `g*` entries are provider/channel/tool *names* (documented as config per the names-as-config rule) or OpenClaw capability-contract ids (`speechProviders`, `memoryEmbeddingProviders`, `mediaUnderstandingProviders`, `tools`, `imageGenerationProviders`, `videoGenerationProviders`, `musicGenerationProviders`, `realtimeVoiceProviders`, `webSearchProviders`) documented in the `oc_` notes. CONFIRMED-MISSING and correctly excluded (not ghosts): `term_groq`, `term_github_copilot`, `term_gemini`, `term_vertex_ai`, `term_tts`, `term_speech_synthesis`, `term_chat_platform`, `term_discord`, `term_telegram`, `term_video_conferencing`, `term_twilio`, `term_chrome`, `term_realtime_voice`, `term_google_meet`. If a future re-scan promotes one, best-fit glossary = `acronym_glossary_agentic_ai.md` (agent/plugin vocabulary), captured via `/tessellum-capture-term-note` + W5.

**Unchanged (already adequate from plan-digestion):** Section Coverage Map (all 21 H2 mapped, 0 orphans), Split Decisions (note 1 = consolidation of 4 same-class micro-stubs), Density Re-Assessment (all ≤300w, 0 code, no caps approached), Undigested Terms Plan (0 new terms), Per-Phase G1–G8 gates, Validation Scripts, Inlinks (G7/G8), Entry Point Decision (contributor to master W1 `entry_openclaw_docs.md`).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + raised floors, relevance + descriptions) | **PASS** | LOCKED Per-Note Related Notes Mapping: each note ≥8 terms (10–12), ≥10 snippets (11–14), ≥10 docs (11–14, ≥5 existing) + repos; every link carries `— what it is; relevance: …`. Counts re-verified from file by script. |
| CP2 | 9-GATE present per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present for the single execution phase; G5 ghost + G6 broken-link + G7/G8 discoverability all present; `## Validation Scripts` implements format/density/sibling/in-degree checks. |
| CP3 | Entry point inherited (`entry_openclaw_docs` planned at master W1) | **PASS** | `## Entry Point Decision` — 4 rows into master's `entry_openclaw_docs.md` (W1 pre-step; DB confirms it is not yet created → correctly a pre-execution dependency, not a per-sub-plan CREATE). |
| CP4 | Size (≤30 or split) | **PASS** | 4 planned notes, single phase, well under 30 and under the ~30-agent fan-out cap. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited verbatim from master Format Definition, itself derived from existing `claude_code/` + `pi/` doc corpora (`## Overview` / `## Related Notes` / bold footer; fixed YAML field order; forbidden-field list). |
| CP6 | Density / BB atomicity | **PASS** | All 4 notes ≤300w, 0 code blocks, single `procedure` BB; only structural decision is the inverse (consolidating 4 under-thin model-provider stubs into note 1). No borderline note. |
| CP7 | Source word counts measured | **PASS** | All 7 pages re-read 2026-06-21: 60/52/75/67/61/48/56 = 419w; matches plan Source table exactly (ratio 1.00). |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | `## Undigested Terms Plan` present (all rows dispositioned, 0 new captures); `## Term-Note Authoring Requirements` present (N/A — 0 new terms; master multi-source mandate applies if any surface). |
| CP8f | Slug specificity + collision audit (term AND doc) | **PASS** | All 4 `oc_` slugs DB-checked: 0 existing-note collisions; no planned slug duplicates an existing `term_*` (g_model_providers/gradium/googlechat/google_meet term-matches all empty). Note-1 grouped slug justified in Split Decisions. |
| CP9 | Discoverability / inlinks executed (G8) | **PASS** | `## Inlinks` maps ≥1 outside-folder inbound link to every note (`entry_openclaw_docs` → all 4, plus repo/term reciprocals); G8 in-degree check scripted in `## Validation Scripts` (fails if any note has 0 outside-folder inbound link). |

**RESULT: 9/9 (+ CP8f) PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** (9/9 + CP8f PASS → READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |
