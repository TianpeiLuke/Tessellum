---
title: Sub-Plan pl12 — OpenClaw Docs: Plugins (reference, huggingface→line)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/huggingface", "plugins/reference/imessage", "plugins/reference/inworld", "plugins/reference/irc", "plugins/reference/kilocode", "plugins/reference/kimi", "plugins/reference/line"]
---

# Sub-Plan pl12: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format/YAML, dedup (term + doc + `repo_openclaw*`),
> 9-GATE validation, cross-references, undigested-terms ownership, and entry-point wiring are ALL inherited from the master.

## Scope

The 7 alphabetically-contiguous **plugin reference cards** (`plugins/reference/huggingface` → `…/line`) of the
OpenClaw plugin-reference catalog. Each page is a uniform, machine-generated plugin index card describing one
shippable OpenClaw plugin: its `summary`, **Distribution** (npm package name + install route — bundled vs
npm/ClawHub), the **Surface** it contributes (a model `provider`, a `channel`, or a `speechProviders` contract),
and a **Related docs** pointer to the deeper provider/channel page. The 7 cards split into three plugin families:
**model-provider plugins** (huggingface, kilocode, kimi), **chat-channel plugins** (imessage, irc, line), and one
**speech (TTS) provider plugin** (inworld). Priority **P3** (Phase C — plugin reference sprawl); these cards are
the thin catalog layer above the much richer `providers/*` and `channels/*` pages digested in other sub-plans, and
above the existing code-side `repo_openclaw_extensions*` / `repo_openclaw_channels*` notes.

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Hugging Face plugin | `plugins/reference/huggingface` | 58 | 0 | 3 | 0 | procedure |
| iMessage plugin | `plugins/reference/imessage` | 62 | 0 | 3 | 0 | procedure |
| Inworld plugin | `plugins/reference/inworld` | 54 | 0 | 3 | 0 | procedure |
| IRC plugin | `plugins/reference/irc` | 62 | 0 | 3 | 0 | procedure |
| Kilocode plugin | `plugins/reference/kilocode` | 54 | 0 | 3 | 0 | procedure |
| Kimi plugin | `plugins/reference/kimi` | 59 | 0 | 3 | 0 | procedure |
| LINE plugin | `plugins/reference/line` | 57 | 0 | 3 | 0 | procedure |

**Total measured: 406 words, 0 code fences across 7 pages.** Every page shares the identical 3-H2 skeleton
(`## Distribution` / `## Surface` / `## Related docs`), 0 H3, no code blocks. These are catalog stubs, not
tutorials — far below every density cap.

## Content Strategy

- **Prioritize**: faithfully capturing the load-bearing catalog facts of each card — the **npm package name**,
  the **install route** (bundled "included in OpenClaw" vs `npm` + ClawHub), and the exact **surface key**
  (`providers: X`, `channels: X`, or `contracts: speechProviders`). These four fields are the entire value of a
  reference card and must be reproduced verbatim.
- **No splits**: each page is one BB (a procedure: how to install/identify one plugin), ≤62 words, 0 code — one
  note per page. None approaches the 2,500-word / 6-code-block / 400-line caps.
- **No merges**: although the 7 cards are near-identical in shape, they document distinct shippable plugins with
  distinct package names and surfaces; merging would lose per-plugin lookup atomicity (the catalog's whole point).
  Kept atomic, one note per plugin, exactly as the source catalog is one page per plugin.
- **Link-out, do NOT duplicate**: each card's deeper content lives on its `Related docs` target (`/providers/huggingface`,
  `/channels/imessage`, etc.) — those are owned by other sub-plans (`pr04`, `ch02`, `ch03`, `pr04`). This note
  links those as siblings/external pointers and does not re-explain provider auth or channel setup. The code-side
  implementations (`repo_openclaw_extensions_llm_providers`, `repo_openclaw_channels*`,
  `repo_openclaw_extensions_voice_speech`) are LINKED per the dedup policy, never re-documented.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_huggingface.md` | procedure | `plugins/reference/huggingface` (Distribution, Surface, Related docs) | 230 | The `@openclaw/huggingface-provider` plugin: adds the Hugging Face model-provider surface (`providers: huggingface`), bundled in OpenClaw; how to identify/audit it and where the deeper provider config lives. |
| 2 | `oc_plugins_reference_imessage.md` | procedure | `plugins/reference/imessage` (Distribution, Surface, Related docs) | 230 | The `@openclaw/imessage` plugin: adds the iMessage chat channel surface (`channels: imessage`) for sending/receiving OpenClaw messages, bundled in OpenClaw; identification + pointer to channel setup. |
| 3 | `oc_plugins_reference_inworld.md` | procedure | `plugins/reference/inworld` (Distribution, Surface, Related docs) | 230 | The `@openclaw/inworld-speech` plugin: Inworld streaming text-to-speech (MP3 / OGG_OPUS / PCM telephony) registered via the `speechProviders` contract; npm + ClawHub install route. |
| 4 | `oc_plugins_reference_irc.md` | procedure | `plugins/reference/irc` (Distribution, Surface, Related docs) | 230 | The `@openclaw/irc` plugin: adds the IRC chat channel surface (`channels: irc`) for sending/receiving OpenClaw messages, bundled in OpenClaw; identification + pointer to channel setup. |
| 5 | `oc_plugins_reference_kilocode.md` | procedure | `plugins/reference/kilocode` (Distribution, Surface, Related docs) | 230 | The `@openclaw/kilocode-provider` plugin: adds the Kilocode model-provider surface (`providers: kilocode`); npm + ClawHub install route; pointer to deeper provider config. |
| 6 | `oc_plugins_reference_kimi.md` | procedure | `plugins/reference/kimi` (Distribution, Surface, Related docs) | 240 | The `@openclaw/kimi-provider` plugin: adds the Kimi + Kimi-Coding model-provider surfaces (`providers: kimi, kimi-coding`); npm + ClawHub; note its Related-docs pointer routes to `/providers/moonshot`. |
| 7 | `oc_plugins_reference_line.md` | procedure | `plugins/reference/line` (Distribution, Surface, Related docs) | 230 | The `@openclaw/line` plugin: OpenClaw LINE channel for LINE Bot API chats (`channels: line`); npm + ClawHub install route; pointer to channel setup. |

**Locked count: 7 notes** (1 per source page). Master estimated 11 for a typical 7-page sub-plan; these are
uniform single-section catalog stubs (≤62 words, 0 code), so each maps to exactly one atomic note — no splits.

## Section Coverage Map

Every source page exposes the identical three H2 sections and one H1 summary line, all of which map into the
single note for that page. No H3 exist on any page. No orphaned sections.

```
plugins/reference/huggingface.md
├── (H1 summary) "Adds Hugging Face model provider support" → note 1 Overview
├── ## Distribution (pkg @openclaw/huggingface-provider; included) → note 1 (Distribution)
├── ## Surface (providers: huggingface) ───────────────────────── → note 1 (Surface)
└── ## Related docs (/providers/huggingface) ─────────────────── → note 1 (Related Notes + References)
plugins/reference/imessage.md
├── (H1 summary) iMessage channel surface ────────────────────── → note 2 Overview
├── ## Distribution (@openclaw/imessage; included) ───────────── → note 2
├── ## Surface (channels: imessage) ──────────────────────────── → note 2
└── ## Related docs (/channels/imessage) ─────────────────────── → note 2
plugins/reference/inworld.md
├── (H1 summary) Inworld streaming TTS (MP3/OGG_OPUS/PCM) ─────── → note 3 Overview
├── ## Distribution (@openclaw/inworld-speech; npm + ClawHub) ── → note 3
├── ## Surface (contracts: speechProviders) ──────────────────── → note 3
└── ## Related docs (/providers/inworld) ─────────────────────── → note 3
plugins/reference/irc.md
├── (H1 summary) IRC channel surface ─────────────────────────── → note 4 Overview
├── ## Distribution (@openclaw/irc; included) ────────────────── → note 4
├── ## Surface (channels: irc) ───────────────────────────────── → note 4
└── ## Related docs (/channels/irc) ──────────────────────────── → note 4
plugins/reference/kilocode.md
├── (H1 summary) Kilocode model provider ─────────────────────── → note 5 Overview
├── ## Distribution (@openclaw/kilocode-provider; npm + ClawHub) → note 5
├── ## Surface (providers: kilocode) ─────────────────────────── → note 5
└── ## Related docs (/providers/kilocode) ────────────────────── → note 5
plugins/reference/kimi.md
├── (H1 summary) Kimi, Kimi Coding model provider ────────────── → note 6 Overview
├── ## Distribution (@openclaw/kimi-provider; npm + ClawHub) ─── → note 6
├── ## Surface (providers: kimi, kimi-coding) ────────────────── → note 6
└── ## Related docs (/providers/moonshot) ────────────────────── → note 6 (note: target slug = moonshot)
plugins/reference/line.md
├── (H1 summary) LINE Bot API channel ───────────────────────── → note 7 Overview
├── ## Distribution (@openclaw/line; npm + ClawHub) ──────────── → note 7
├── ## Surface (channels: line) ──────────────────────────────── → note 7
└── ## Related docs (/channels/line) ─────────────────────────── → note 7
```

No orphaned sections; deeper provider/channel pages (link targets) are owned by `pr04`/`ch02`/`ch03` and are
linked-out, not duplicated here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are ≤62 words, single-BB (procedure), 0 code — far below every density cap. One note per page; no page splits and no merges. |

## Summary Statistics & Building Block Distribution

- **Source pages:** 7 (406 measured words, 0 code fences).
- **Planned new `oc_` notes:** 7. **New `term_dictionary` notes:** 0 (expected; see Undigested Terms Plan).
- **BB distribution:** procedure ×7 (every card is "how to identify/install one plugin"). 0 concept / model / argument.
- **Estimated digest output:** ~1,620 words (avg ~232/note) — each digest note is intentionally larger than its
  ~58-word source because the required Overview + Related Notes (≥6 relevance-selected terms + siblings + repos)
  + References scaffold adds value beyond the bare catalog card; all stay well under the 2,500-word cap.
- **Plugin families:** model-provider plugins ×3 (huggingface, kilocode, kimi) · chat-channel plugins ×3
  (imessage, irc, line) · speech/TTS provider plugin ×1 (inworld).
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** every note maps **≥8 relevance-selected `term_dictionary`
  terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** + relevant `repo_openclaw*` + sibling
  toward the 10-doc floor as "(planned, this series)". See the locked per-note mapping below.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

`oc_*` docs of this series count toward the 10-doc floor as "(planned, this series)". Paths are relative FROM
`resources/documentation/openclaw/oc_*.md`. Terms NOT in the DB (`term_kimi`, `term_moonshot`, `term_kilocode`,
`term_inworld`, `term_irc`, `term_imessage`, `term_line`, `term_tts`) are intentionally NOT cited — the deeper
provider/channel terms are owned by `pr04`/`pr05`/`ch02`/`ch03`.

### oc_plugins_reference_huggingface (9t · 10s · 11d)

**Terms**
- [Hugging Face](../../term_dictionary/term_huggingface.md) — the HF model hub / inference platform; relevance: this plugin fronts exactly that hub as an OpenClaw provider surface.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model-provider backend; relevance: `providers: huggingface` IS the surface this card contributes.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the HF provider serves LLM inference into OpenClaw's agent loop.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI providers; relevance: HF is an external GenAI service the gateway brokers.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the registry of selectable models; relevance: the plugin contributes HF models to OpenClaw's catalog.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routes a request to the right provider; relevance: enabling this plugin makes HF a routable target.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — secondary provider on failure; relevance: HF can serve as a fallback/primary in the provider chain.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: the plugin ships as the `@openclaw/huggingface-provider` npm package (bundled).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the host gateway product; relevance: the plugin's host runtime.

**Docs**
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — how a provider plugin is authored/registered; relevance: the cross-product analog of OpenClaw's `providers:` surface.
- [Hermes — Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — step-by-step add a model provider; relevance: the deeper how-to for what this card catalogs.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — enumerates provider/channel/speech surfaces; relevance: defines the `providers:` surface this card declares.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin discovery/loading model; relevance: explains how a bundled provider plugin is installed.
- [Hermes — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — model-catalog schema; relevance: where HF models surface once the plugin is active.
- [Hermes — Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: HF as a cloud inference provider.
- [Pi — Custom Models](../pi/pi_custom_models.md) — registering custom model providers; relevance: cross-product analog of HF provider config.
- [Pi — Cloud Providers](../pi/pi_cloud_providers.md) — cloud provider setup; relevance: deeper analog of an external model provider.
- [Pi — Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering a provider backend; relevance: the registration step abstracted by this catalog card.
- [oc_plugins_reference_kilocode](oc_plugins_reference_kilocode.md) — peer model-provider plugin card (planned, this series); relevance: sibling provider-family card.
- [oc_plugins_reference_kimi](oc_plugins_reference_kimi.md) — peer model-provider plugin card (planned, this series); relevance: sibling provider-family card.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — code-side LLM-provider plugin impl; relevance: implements the surface this card documents.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: hosts provider plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root repo; relevance: the host product.

**Snippets**
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry wiring; relevance: how a provider plugin like HF registers its surface.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin skeleton; relevance: the shape of an HF-style provider plugin.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstract class; relevance: the contract an HF provider implements.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init dispatch; relevance: how the provider is instantiated at load.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a concrete OpenClaw provider impl; relevance: structural peer of the HF provider plugin.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider impl; relevance: peer model-provider plugin pattern.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider; relevance: how a provider exposes many models (as HF does).
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the manifest that declares the `providers:` surface.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: how a bundled provider plugin declares entrypoints.
- [snippet_hermes_agent_plugins_provider_bedrock](../../code_snippets/snippet_hermes_agent_plugins_provider_bedrock.md) — Bedrock provider plugin; relevance: peer hosted-model provider plugin impl.

### oc_plugins_reference_imessage (8t · 10s · 11d)

**Terms**
- [Chatbot](../../term_dictionary/term_chatbot.md) — automated conversational agent; relevance: OpenClaw runs as a chatbot over the iMessage channel.
- [Bot](../../term_dictionary/term_bot.md) — automated messaging actor; relevance: the iMessage plugin presents an OpenClaw bot.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP inbound callback; relevance: channel inbound delivery mechanism for messages.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — adapts a platform to the gateway's channel contract; relevance: the iMessage plugin IS a channel adapter.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway brokering chat platforms; relevance: iMessage is one channel docked to it.
- [DM Pairing](../../term_dictionary/term_dm_pairing.md) — pairing a user DM to an agent session; relevance: how an iMessage DM binds to OpenClaw.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway product; relevance: the plugin's host runtime.

**Docs**
- [Hermes — Adding a Platform Adapter Plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — how to add a chat-channel adapter; relevance: the deeper how-to for what this card catalogs.
- [Hermes — Messaging via BlueBubbles (iMessage)](../hermes_agent/hermes_messaging_bluebubbles_imessage.md) — iMessage-over-BlueBubbles setup; relevance: the concrete iMessage channel config.
- [Hermes — Photon iMessage](../hermes_agent/hermes_photon_imessage.md) — alternate iMessage bridge; relevance: another iMessage delivery path for the channel.
- [Hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel/gateway architecture; relevance: where the iMessage channel plugs in.
- [Hermes — Webhooks Routes & Security](../hermes_agent/hermes_webhooks_routes_security.md) — inbound webhook routing; relevance: channel inbound message delivery.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface enumeration; relevance: defines the `channels:` surface this card declares.
- [Claude Code — Channels Setup](../claude_code/cc_channels_setup.md) — channel setup how-to; relevance: cross-product analog of channel install/config.
- [Claude Code — Channels Overview](../claude_code/cc_channels_overview.md) — channel model overview; relevance: conceptual analog of a chat-channel surface.
- [Band — Integration Methods](../band/band_integration_methods.md) — agent channel integration patterns; relevance: cross-product channel-integration analog.
- [oc_plugins_reference_irc](oc_plugins_reference_irc.md) — peer chat-channel plugin card (planned, this series); relevance: sibling channel-family card.
- [oc_plugins_reference_line](oc_plugins_reference_line.md) — peer chat-channel plugin card (planned, this series); relevance: sibling channel-family card.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel subsystem; relevance: hosts channel plugins.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — text-messaging channel impl; relevance: iMessage's code-side home.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root repo; relevance: the host product.

**Snippets**
- [snippet_hermes_agent_skills_apple_imessage](../../code_snippets/snippet_hermes_agent_skills_apple_imessage.md) — Apple iMessage integration; relevance: direct code-side analog of this iMessage channel plugin.
- [snippet_hermes_agent_gw_platform_bluebubbles](../../code_snippets/snippet_hermes_agent_gw_platform_bluebubbles.md) — BlueBubbles iMessage bridge; relevance: the concrete iMessage delivery implementation.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the contract this iMessage plugin satisfies.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: how an inbound iMessage maps to a session.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory registry; relevance: how a channel plugin is registered/discovered.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — base platform normalization; relevance: normalizing inbound iMessage events.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — outbound send dispatch; relevance: sending OpenClaw messages out over the channel.
- [snippet_hermes_agent_tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — outbound message formatting; relevance: formatting messages for the iMessage surface.
- [snippet_hermes_agent_gw_config_schema](../../code_snippets/snippet_hermes_agent_gw_config_schema.md) — gateway/channel config schema; relevance: the config block an iMessage channel uses.
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — webhook listener pattern; relevance: inbound webhook channel delivery analog.

### oc_plugins_reference_inworld (9t · 11s · 11d)

**Terms**
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesizes speech audio from text; relevance: Inworld is a streaming TTS engine — the core surface this plugin adds.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcribes audio to text; relevance: companion speech modality in the same voice stack.
- [Voice Call](../../term_dictionary/term_voice_call.md) — agent participates in a phone/voice call; relevance: PCM telephony is Inworld's output target.
- [VoIP](../../term_dictionary/term_voip.md) — voice over IP transport; relevance: carries the PCM telephony stream Inworld produces.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — agent voice interaction mode; relevance: TTS output is what voice mode plays back.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — live streaming transcription; relevance: the streaming counterpart in the voice pipeline.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable provider backend; relevance: Inworld registers via the `speechProviders` contract as a provider plugin.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multiple input/output modalities; relevance: speech audio is the modality this plugin adds.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway product; relevance: the plugin's host runtime.

**Docs**
- [Hermes — TTS Providers](../hermes_agent/hermes_tts_providers.md) — TTS provider catalog/config; relevance: Inworld is one such streaming TTS provider.
- [Hermes — STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text setup; relevance: companion modality in the voice stack.
- [Hermes — Voice Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — voice mode controls; relevance: consumes TTS output from a provider like Inworld.
- [Hermes — Use Voice Mode Guide](../hermes_agent/hermes_use_voice_mode_guide.md) — end-to-end voice usage; relevance: where a TTS provider plugs in.
- [Hermes — Voice Gateway (Discord VC)](../hermes_agent/hermes_voice_gateway_discord_vc.md) — voice gateway path; relevance: a consumer of TTS audio streams.
- [Hermes — Messaging Media Settings](../hermes_agent/hermes_messaging_media_settings.md) — media/audio settings; relevance: the audio formats (MP3/OGG/PCM) TTS produces.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface enumeration; relevance: defines the speech-provider (`contracts:`) surface this card declares.
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin authoring; relevance: the provider-plugin pattern a speech provider follows.
- [Claude Code — Voice Dictation](../claude_code/cc_voice_dictation.md) — voice dictation feature; relevance: cross-product speech-modality analog.
- [oc_plugins_reference_huggingface](oc_plugins_reference_huggingface.md) — peer provider-family plugin card (planned, this series); relevance: sibling provider-plugin card.
- [oc_plugins_reference_kimi](oc_plugins_reference_kimi.md) — peer provider plugin card (planned, this series); relevance: sibling provider-family card.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extension impl; relevance: the `speechProviders` contract's code-side home.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — telephony channel impl; relevance: consumes the PCM TTS stream.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root repo; relevance: the host product.

**Snippets**
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS impl; relevance: peer TTS provider implementation pattern.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs streaming TTS; relevance: directly peer streaming-TTS provider plugin (Inworld's closest analog).
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the pipeline a TTS provider feeds.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT; relevance: companion speech-modality provider in the same contract family.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing; relevance: how a TTS provider like Inworld is selected/routed.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice mode tool; relevance: the consumer of TTS audio.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: companion modality in the voice stack.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — media-stream audio handling; relevance: the PCM telephony stream Inworld targets.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — media-stream transcription; relevance: voice-call audio pipeline Inworld feeds into.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — talk transcription relay; relevance: voice gateway audio relay path for TTS/STT.

### oc_plugins_reference_irc (8t · 10s · 11d)

**Terms**
- [Chatbot](../../term_dictionary/term_chatbot.md) — automated conversational agent; relevance: OpenClaw runs as a chatbot over IRC.
- [Bot](../../term_dictionary/term_bot.md) — automated messaging actor; relevance: the IRC plugin presents an OpenClaw bot.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP inbound callback; relevance: inbound message delivery mechanism for the channel.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — platform-to-gateway adapter; relevance: the IRC plugin IS a channel adapter.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — core channel routing kernel; relevance: where the IRC channel docks into the gateway.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway brokering chat platforms; relevance: IRC is one channel docked to it.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway product; relevance: the plugin's host runtime.

**Docs**
- [Hermes — Adding a Platform Adapter Plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — add a chat-channel adapter; relevance: the deeper how-to for what this card catalogs.
- [Hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel/gateway architecture; relevance: where the IRC channel plugs in.
- [Hermes — Messaging Simplex](../hermes_agent/hermes_messaging_simplex.md) — a lightweight text channel setup; relevance: structural analog of an IRC-style text channel.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface enumeration; relevance: defines the `channels:` surface this card declares.
- [Hermes — Webhooks Routing & Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — inbound/outbound routing; relevance: channel message routing analog.
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin discovery/loading; relevance: how a bundled channel plugin installs.
- [Claude Code — Channels Setup](../claude_code/cc_channels_setup.md) — channel setup how-to; relevance: cross-product analog of channel install/config.
- [Claude Code — Channels Overview](../claude_code/cc_channels_overview.md) — channel model overview; relevance: conceptual analog of a chat-channel surface.
- [Band — Websocket Agent Channels](../band/band_websocket_agent_channels.md) — websocket agent channels; relevance: cross-product persistent-connection channel analog (IRC keeps a socket).
- [oc_plugins_reference_imessage](oc_plugins_reference_imessage.md) — peer chat-channel plugin card (planned, this series); relevance: sibling channel-family card.
- [oc_plugins_reference_line](oc_plugins_reference_line.md) — peer chat-channel plugin card (planned, this series); relevance: sibling channel-family card.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel subsystem; relevance: hosts channel plugins.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — text-messaging channel impl; relevance: IRC's code-side home.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root repo; relevance: the host product.

**Snippets**
- [snippet_hermes_agent_plugins_platform_irc](../../code_snippets/snippet_hermes_agent_plugins_platform_irc.md) — IRC platform plugin impl; relevance: direct code-side analog of this IRC channel plugin.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the contract this IRC plugin satisfies.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: mapping inbound IRC messages to sessions.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory registry; relevance: how the IRC channel plugin is registered/discovered.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — base platform normalization; relevance: normalizing inbound IRC events.
- [snippet_hermes_agent_plugins_platform_simplex](../../code_snippets/snippet_hermes_agent_plugins_platform_simplex.md) — simplex text channel plugin; relevance: peer lightweight text-channel plugin pattern.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — outbound send dispatch; relevance: sending OpenClaw messages over IRC.
- [snippet_hermes_agent_tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — outbound message formatting; relevance: formatting messages for the IRC surface.
- [snippet_hermes_agent_gw_config_schema](../../code_snippets/snippet_hermes_agent_gw_config_schema.md) — gateway/channel config schema; relevance: the config block an IRC channel uses.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — generic webhook platform; relevance: inbound channel delivery analog.

### oc_plugins_reference_kilocode (9t · 10s · 11d)

**Terms**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model-provider backend; relevance: `providers: kilocode` IS the surface this card contributes.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Kilocode fronts LLM inference.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI providers; relevance: Kilocode is an external GenAI service.
- [Code Generation](../../term_dictionary/term_code_generation.md) — model-driven code synthesis; relevance: Kilocode is a coding-focused model provider.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of selectable models; relevance: the plugin contributes Kilocode models to the catalog.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routes requests to a provider; relevance: enabling this plugin makes Kilocode a routable target.
- [Model Router](../../term_dictionary/term_model_router.md) — selects a model/provider per request; relevance: Kilocode becomes a routable model behind the router.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: the plugin ships as `@openclaw/kilocode-provider` (npm + ClawHub).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway product; relevance: the plugin's host runtime.

**Docs**
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin authoring/registration; relevance: the pattern this Kilocode card catalogs.
- [Hermes — Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — add a model provider step-by-step; relevance: deeper how-to for a Kilocode-style provider.
- [Hermes — Provider Routing](../hermes_agent/hermes_provider_routing.md) — provider routing config; relevance: routing requests to Kilocode.
- [Hermes — Provider Routing Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — routing through proxies; relevance: provider-routing path for a code provider.
- [Hermes — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — model-catalog schema; relevance: where Kilocode models surface.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface enumeration; relevance: defines the `providers:` surface this card declares.
- [Hermes — Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: Kilocode as a cloud inference provider.
- [Pi — Custom Models](../pi/pi_custom_models.md) — custom model-provider config; relevance: cross-product analog of Kilocode provider config.
- [Pi — Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering a provider backend; relevance: the registration step abstracted by this card.
- [oc_plugins_reference_huggingface](oc_plugins_reference_huggingface.md) — peer model-provider plugin card (planned, this series); relevance: sibling provider-family card.
- [oc_plugins_reference_kimi](oc_plugins_reference_kimi.md) — peer model-provider plugin card (planned, this series); relevance: sibling provider-family card.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — code-side LLM-provider plugin impl; relevance: implements the surface this card documents.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: hosts provider plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root repo; relevance: the host product.

**Snippets**
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry wiring; relevance: how the Kilocode provider registers its surface.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin skeleton; relevance: the shape of a Kilocode-style provider plugin.
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — Codex (coding) provider plugin; relevance: peer coding-focused model-provider plugin.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstract class; relevance: the contract Kilocode implements.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init dispatch; relevance: how the provider is instantiated at load.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider; relevance: peer provider-plugin model exposure pattern.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the manifest that declares the `providers:` surface.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: how an npm/ClawHub provider plugin declares entrypoints.
- [snippet_hermes_agent_plugins_namespace_init](../../code_snippets/snippet_hermes_agent_plugins_namespace_init.md) — plugin namespace init; relevance: namespaced provider plugin loading.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK a provider plugin builds on.

### oc_plugins_reference_kimi (9t · 11s · 11d)

**Terms**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model-provider backend; relevance: the dual `providers: kimi, kimi-coding` surface this card contributes.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Kimi serves LLM inference.
- [Code Generation](../../term_dictionary/term_code_generation.md) — model-driven code synthesis; relevance: the `kimi-coding` variant targets coding.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted GenAI providers; relevance: Kimi/Moonshot is an external provider.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of selectable models; relevance: the plugin contributes the Kimi model family to the catalog.
- [Qwen](../../term_dictionary/term_qwen.md) — peer Chinese-lab LLM family; relevance: closest peer provider for relevance context (same provider neighborhood).
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routes requests to a provider; relevance: enabling this plugin makes Kimi routable.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: ships as `@openclaw/kimi-provider` (npm + ClawHub).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway product; relevance: the plugin's host runtime.

**Docs**
- [Hermes — Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin authoring; relevance: the pattern this Kimi card catalogs.
- [Hermes — Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — add a model provider step-by-step; relevance: deeper how-to for a Kimi-style provider.
- [Hermes — Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: Kimi/Moonshot as a cloud inference provider.
- [Hermes — Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — model-catalog schema; relevance: where the Kimi family surfaces.
- [Hermes — Provider Routing](../hermes_agent/hermes_provider_routing.md) — provider routing config; relevance: routing requests to Kimi vs kimi-coding.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface enumeration; relevance: defines the `providers:` surface this card declares (dual-surface case).
- [Hermes — Plugins System](../hermes_agent/hermes_plugins_system.md) — plugin discovery/loading; relevance: how an npm/ClawHub provider plugin installs.
- [Pi — Cloud Providers](../pi/pi_cloud_providers.md) — cloud provider setup; relevance: cross-product analog of an external model provider.
- [Pi — Custom Models](../pi/pi_custom_models.md) — custom model-provider config; relevance: deeper analog of Kimi provider/model config.
- [oc_plugins_reference_huggingface](oc_plugins_reference_huggingface.md) — peer model-provider plugin card (planned, this series); relevance: sibling provider-family card.
- [oc_plugins_reference_kilocode](oc_plugins_reference_kilocode.md) — peer model-provider plugin card (planned, this series); relevance: sibling provider-family card (also coding-focused).

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — code-side LLM-provider plugin impl; relevance: implements the surface this card documents.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: hosts provider plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root repo; relevance: the host product.

**Snippets**
- [snippet_hermes_agent_plugins_provider_kimi_coding](../../code_snippets/snippet_hermes_agent_plugins_provider_kimi_coding.md) — Kimi-coding provider plugin impl; relevance: direct code-side analog of the `kimi-coding` surface.
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — China-cluster provider group; relevance: the provider neighborhood Kimi/Moonshot belongs to.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry wiring; relevance: how the Kimi provider registers its dual surface.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin skeleton; relevance: the shape of a Kimi-style provider plugin.
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — Codex coding provider; relevance: peer coding-focused provider (mirrors `kimi-coding`).
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstract class; relevance: the contract Kimi implements.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init dispatch; relevance: how the provider is instantiated at load.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: the manifest declaring the dual `providers:` surface.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: how an npm/ClawHub provider plugin declares entrypoints.
- [snippet_hermes_agent_plugins_namespace_init](../../code_snippets/snippet_hermes_agent_plugins_namespace_init.md) — plugin namespace init; relevance: namespaced provider plugin loading.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter multi-model provider; relevance: peer multi-surface provider plugin pattern.

### oc_plugins_reference_line (8t · 10s · 11d)

**Terms**
- [Chatbot](../../term_dictionary/term_chatbot.md) — automated conversational agent; relevance: OpenClaw runs as a LINE Bot persona.
- [Bot](../../term_dictionary/term_bot.md) — automated messaging actor; relevance: the LINE plugin presents the OpenClaw bot.
- [Webhook](../../term_dictionary/term_webhook.md) — HTTP inbound callback; relevance: the LINE Bot API delivers messages via webhook.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — platform-to-gateway adapter; relevance: the LINE plugin IS a channel adapter.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway brokering chat platforms; relevance: LINE is one channel docked to it.
- [OAuth](../../term_dictionary/term_oauth.md) — token-based authorization; relevance: LINE Bot channel access token / auth.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway product; relevance: the plugin's host runtime.

**Docs**
- [Hermes — Messaging LINE](../hermes_agent/hermes_messaging_line.md) — LINE channel setup; relevance: the concrete deeper config for the LINE channel this card catalogs.
- [Hermes — Adding a Platform Adapter Plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — add a chat-channel adapter; relevance: the how-to for a LINE-style channel plugin.
- [Hermes — Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel/gateway architecture; relevance: where the LINE channel plugs in.
- [Hermes — Webhooks Routes & Security](../hermes_agent/hermes_webhooks_routes_security.md) — inbound webhook routing; relevance: LINE Bot API webhook delivery.
- [Hermes — Webhooks Routing & Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — inbound/outbound routing; relevance: routing LINE messages in and out.
- [Hermes — Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — surface enumeration; relevance: defines the `channels:` surface this card declares.
- [Claude Code — Channels Setup](../claude_code/cc_channels_setup.md) — channel setup how-to; relevance: cross-product analog of channel install/config.
- [Claude Code — Channels Overview](../claude_code/cc_channels_overview.md) — channel model overview; relevance: conceptual analog of a chat-channel surface.
- [Band — Integration Methods](../band/band_integration_methods.md) — agent channel integration patterns; relevance: cross-product channel-integration analog.
- [oc_plugins_reference_imessage](oc_plugins_reference_imessage.md) — peer chat-channel plugin card (planned, this series); relevance: sibling channel-family card.
- [oc_plugins_reference_irc](oc_plugins_reference_irc.md) — peer chat-channel plugin card (planned, this series); relevance: sibling channel-family card.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel subsystem; relevance: hosts channel plugins.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — text-messaging channel impl; relevance: LINE's code-side home.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw root repo; relevance: the host product.

**Snippets**
- [snippet_hermes_agent_plugins_platform_line](../../code_snippets/snippet_hermes_agent_plugins_platform_line.md) — LINE platform plugin impl; relevance: direct code-side analog of this LINE channel plugin.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the contract this LINE plugin satisfies.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: mapping inbound LINE messages to sessions.
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — generic webhook platform; relevance: the LINE Bot API webhook inbound pattern.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory registry; relevance: how the LINE channel plugin is registered/discovered.
- [snippet_hermes_agent_gw_platform_base_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_base_normalize.md) — base platform normalization; relevance: normalizing inbound LINE events.
- [snippet_hermes_agent_tools_send_dispatch](../../code_snippets/snippet_hermes_agent_tools_send_dispatch.md) — outbound send dispatch; relevance: sending OpenClaw messages over LINE.
- [snippet_hermes_agent_tools_send_format](../../code_snippets/snippet_hermes_agent_tools_send_format.md) — outbound message formatting; relevance: formatting messages for the LINE surface.
- [snippet_hermes_agent_gw_config_schema](../../code_snippets/snippet_hermes_agent_gw_config_schema.md) — gateway/channel config schema; relevance: the config block a LINE channel uses.
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — webhook listener pattern; relevance: inbound webhook channel delivery analog for LINE Bot API.

## Undigested Terms Plan

Per the master's corpus-wide policy: OpenClaw vocabulary on these pages is captured as the `oc_*` doc notes
themselves (the plugin cards ARE the catalog entries), and the only `term_dictionary` interaction is **linking
existing** terms. No term definition is inlined in an `oc_*` note.

| Term (appears on these pages) | Disposition |
|---|---|
| iMessage / IRC / LINE (chat channels) | Documented as the `oc_plugins_reference_{imessage,irc,line}` channel cards; link existing `term_chatbot`/`term_bot`/`term_webhook`. No `term_imessage`/`term_irc`/`term_line` exist and none warranted (channel-specific, single-doc subjects — owned by `ch02`/`ch03` provider/channel pages). |
| Inworld / streaming TTS / MP3 / OGG_OPUS / PCM telephony | Documented as `oc_plugins_reference_inworld`; link existing `term_text_to_speech` / `term_voice_call` / `term_voip`. No new TTS-engine term. |
| Kilocode / Kimi / Kimi Coding / Moonshot | Documented as their `oc_plugins_reference_*` provider cards; link existing `term_provider_plugin` / `term_llm` / `term_third_party_genai_services` / `term_code_generation`. No `term_kilocode`/`term_kimi`/`term_moonshot` (provider-specific, single-doc subjects — owned by `pr04`/`pr05`). |
| provider / channel / speechProviders contract / surface | OpenClaw architecture vocabulary — link existing `term_provider_plugin`; the contract/surface concepts are owned by the `plugins/architecture*` and `concepts/*` sub-plans, not redefined here. |
| npm / ClawHub / install route / package | Distribution vocabulary — link existing `term_npm`; ClawHub is owned by the `clawhub/*` sub-plans (`cw01–03`). No new term. |

**New-term candidates: 0.** No genuinely cross-cutting, vault-reusable term lacking both a doc-page home and an
existing note appears on these 7 stub cards. If augment's re-run of Step 2d surfaces one, it would be captured via
`/tessellum-capture-term-note` and added to the best-fit `acronym_glossary_gen_ai*.md` — not expected.

## Term-Note Authoring Requirements

**N/A (0 new terms).** No `term_dictionary` capture is planned for this sub-plan; all term interaction is linking
glossary-update requirement would apply per `/tessellum-capture-term-note`.)

## Per-Phase Validation Gate (G1–G9)

Single execution phase (all 7 notes). Inherited from master; run after the wave's notes are written and reindexed.

| Gate | Check | Tool / Method | Pass criterion |
|---|---|---|---|
| G1 | Format + YAML | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` | All 7 notes: required H2 (`## Overview`, `## Related Notes`), fixed-order YAML, no forbidden fields, quoted year tags, itemized keywords/topics. |
| G2 | Grounding | Diff each note vs its `inbox/openclaw_docs/plugins/reference/<page>.md` | Package name, install route, surface key, related-docs target reproduced verbatim; no invented config/flags. |
| G3 | Density + Coverage | Word/code/line caps + Section Coverage Map | Each note ≤2,500w / ≤6 code / ≤400 lines (trivially met); all 3 H2 of each source page covered; 0 orphans. |
| G4 | Cross-Reference | `## Related Notes` floor | Each note ≥6 relevance-selected term links + relevant `repo_openclaw*` + sibling `oc_*`, each an indexed `[text](path.md)` link with a relevance statement. |
| G5 | Ghost-reference detect + redirect | `/tessellum-fix-ghost-references` + DB existence check | 0 links to non-existent notes; sibling `oc_*` links resolve once the wave's 7 notes exist. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` + DB rebuild | 0 broken relative paths in `note_links`. |
| G7/G8 | Discoverability / anti-island | `note_links` in-degree query | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` rows; see Inlinks); in-degree ≥1. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
cd /path/to/vault

# Resolve config-driven paths
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")

# --- Gate sweep over this sub-plan's target folder ---
GATE_DIR="resources/documentation/openclaw"
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"

# G1 format (structural)
python3 scripts/check_note_format.py --path "$GATE_DIR"
# G1 YAML frontmatter (per sub-plan notes)
for f in oc_plugins_reference_huggingface oc_plugins_reference_imessage oc_plugins_reference_inworld \
         oc_plugins_reference_irc oc_plugins_reference_kilocode oc_plugins_reference_kimi \
         oc_plugins_reference_line ; do
  python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR/$f.md"
done

# G1 required sections + source_url presence (REQ_SECTIONS / REQUIRE_SOURCE_URL)
for f in "$GATE_DIR"/oc_plugins_reference_*.md ; do
  for sec in ${(s:|:)REQ_SECTIONS} ; do
    grep -q "^$sec" "$f" || echo "MISSING SECTION [$sec] in $f"
  done
  if [ "$REQUIRE_SOURCE_URL" = "1" ]; then
    grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $f"
  fi
done

# G5 ghost-reference + sibling-prefix resolution (SIBLING_PREFIX)
grep -rohE '\]\(([^)]+\.md)\)' "$GATE_DIR"/oc_plugins_reference_*.md | sed -E 's/.*\(([^)]+)\)/\1/' | sort -u | \
while read p; do
  base=$(basename "$p")
  if [ "$cnt" = "0" ]; then
    case "$base" in ${SIBLING_PREFIX}*) echo "SIBLING (expected, this wave): $base" ;; *) echo "GHOST: $base" ;; esac
  fi
done

# G6 broken links + reindex
bash scripts/update_notes_database.sh --force
sqlite3 "$DB" "SELECT COUNT(*) AS broken FROM broken_links;"

# G7/G8 in-degree (anti-island) for the 7 new notes
for f in oc_plugins_reference_huggingface oc_plugins_reference_imessage oc_plugins_reference_inworld \
         oc_plugins_reference_irc oc_plugins_reference_kilocode oc_plugins_reference_kimi \
         oc_plugins_reference_line ; do
  echo -n "$f in_degree="
done
```

## Density Re-Assessment

| Note | Source words | Est. note words | Code blocks | Lines (est.) | Within caps? |
|---|---:|---:|---:|---:|---|
| oc_plugins_reference_huggingface | 58 | ~230 | 0 | ~55 | yes (≤2500w/6c/400L) |
| oc_plugins_reference_imessage | 62 | ~230 | 0 | ~55 | yes |
| oc_plugins_reference_inworld | 54 | ~230 | 0 | ~55 | yes |
| oc_plugins_reference_irc | 62 | ~230 | 0 | ~55 | yes |
| oc_plugins_reference_kilocode | 54 | ~230 | 0 | ~55 | yes |
| oc_plugins_reference_kimi | 59 | ~240 | 0 | ~57 | yes |
| oc_plugins_reference_line | 57 | ~230 | 0 | ~55 | yes |

All notes are far under every density cap; no borderline cases, no split promotions. The (deliberate) expansion
from ~58 source words to ~230 is the required Overview + Related Notes (≥6 relevance terms) + References scaffold,
not source padding — each note remains one atomic procedure.

## Entry Point Decision (inherited from master)

No new entry point is created by this sub-plan. Per master **W1**, the series hub
`0_entry_points/entry_openclaw_docs.md` is created as a pre-step before the first sub-plan executes. This sub-plan
**contributes its 7 rows** to that hub under the Plugins section / pl12 table:

| Note | Family | Surface | Package | Row blurb |
|---|---|---|---|---|
| oc_plugins_reference_huggingface | provider | `providers: huggingface` | `@openclaw/huggingface-provider` | Hugging Face model-provider plugin (bundled). |
| oc_plugins_reference_imessage | channel | `channels: imessage` | `@openclaw/imessage` | iMessage chat-channel plugin (bundled). |
| oc_plugins_reference_inworld | speech | `contracts: speechProviders` | `@openclaw/inworld-speech` | Inworld streaming TTS plugin (npm/ClawHub). |
| oc_plugins_reference_irc | channel | `channels: irc` | `@openclaw/irc` | IRC chat-channel plugin (bundled). |
| oc_plugins_reference_kilocode | provider | `providers: kilocode` | `@openclaw/kilocode-provider` | Kilocode model-provider plugin (npm/ClawHub). |
| oc_plugins_reference_kimi | provider | `providers: kimi, kimi-coding` | `@openclaw/kimi-provider` | Kimi + Kimi-Coding model-provider plugin (npm/ClawHub). |
| oc_plugins_reference_line | channel | `channels: line` | `@openclaw/line` | LINE (LINE Bot API) chat-channel plugin (npm/ClawHub). |

The hub provides the required outside-folder inbound link to satisfy G7/G8 for all 7 notes.

## Inlinks (existing notes → new notes)

existing unless marked (planned).

| Source note (existing unless noted) | → New note(s) | Rationale |
|---|---|---|
| `entry_openclaw_docs.md` (planned, W1 pre-step) | all 7 | series hub rows (primary discoverability link for each note). |
| `areas/code_repos/repo_openclaw_extensions_llm_providers.md` | huggingface, kilocode, kimi | code-side LLM-provider plugin impl → doc cards for those provider plugins. |
| `areas/code_repos/repo_openclaw_channels_messaging.md` | imessage, irc, line | text-channel impl → doc cards for those channel plugins. |
| `areas/code_repos/repo_openclaw_extensions_voice_speech.md` | inworld | voice/speech extension impl → the TTS provider-plugin card. |
| `resources/term_dictionary/term_huggingface.md` | huggingface | term → its OpenClaw provider-plugin doc. |
| `resources/term_dictionary/term_provider_plugin.md` | huggingface, kilocode, kimi, inworld | term → concrete provider/speech plugin examples. |
| `resources/term_dictionary/term_text_to_speech.md` | inworld | term → a concrete TTS provider plugin. |

These inlinks are added during execution (the skill adds reciprocal/source-side links); `entry_openclaw_docs`
rows are the guaranteed anti-island link.

## Pacing Rules (inherited from master)

Cap dynamic-workflow fan-out at ~30 agents/run (this sub-plan's 7 notes fit one small wave); embed manifests in
the script; `git pull --rebase --autostash origin main` before committing; commit per sub-plan / per wave with NO
Claude co-author trailer; reindex incrementally per wave and verify `note_links` + 0 broken links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan (this sub-plan) | `/tessellum-plan-digestion` | 🟢 DONE (authored 2026-06-20, sources measured) |
| 2. Augment | `/tessellum-augment-digestion-plan` | 🟢 DONE (xref-augment 2026-06-21 — per-note mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | 🟢 DONE (2026-06-21 — 9/9 PASS, READY) |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending (status: ready) |

## Augmentation Report (2026-06-21)

**Scope:** xref-augment of the 7 planned `oc_plugins_reference_*` notes — re-read all 7 source pages under
`inbox/openclaw_docs/plugins/reference/` (huggingface, imessage, inworld, irc, kilocode, kimi, line; 406 measured
floors (≥8 terms · ≥10 snippets · ≥10 docs per note)** and replaced the prior "Candidate Cross-References"
section. Density unchanged (all 7 pages ≤62 words, 0 code; no splits/merges).

toward the 10-doc floor):

| Note | Terms | Snippets | Docs (existing + planned-sibling) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_huggingface | 9 | 10 | 11 (9 existing + 2 sibling) | 3 | yes |
| oc_plugins_reference_imessage | 8 | 10 | 11 (9 existing + 2 sibling) | 3 | yes |
| oc_plugins_reference_inworld | 9 | 11 | 11 (9 existing + 2 sibling) | 3 | yes |
| oc_plugins_reference_irc | 8 | 10 | 11 (9 existing + 2 sibling) | 3 | yes |
| oc_plugins_reference_kilocode | 9 | 10 | 11 (9 existing + 2 sibling) | 3 | yes |
| oc_plugins_reference_kimi | 9 | 11 | 11 (9 existing + 2 sibling) | 3 | yes |
| oc_plugins_reference_line | 8 | 10 | 11 (9 existing + 2 sibling) | 3 | yes |

**Corpus discovery vs original draft.** The original draft (≥6-term floor) understated the available vault
coverage. The re-search surfaced a rich parallel coding-agent corpus that the raised floors now exploit:
- **Terms** newly added beyond the original 6-7: `term_provider_routing`, `term_fallback_provider`,
  `term_model_router`, `term_channel_adapter`, `term_channel_kernel`, `term_messaging_gateway`,
  `term_dm_pairing`, `term_voice_mode`, `term_realtime_transcription`, `term_multimodal`, `term_qwen`. All
  `term_inworld`, `term_irc`, `term_imessage`, `term_line`, `term_tts`) remain ABSENT from the DB and are
  correctly NOT cited (owned by `pr04`/`pr05`/`ch02`/`ch03`).
- **Snippets** (all existing): the `snippet_hermes_agent_plugins_provider_*` + `snippet_openclaw_provider_*`
  corpus for provider cards; `snippet_hermes_agent_plugins_platform_{irc,line}` + `snippet_*_apple_imessage` +
  `snippet_*_bluebubbles` + `snippet_openclaw_channels_*` for channel cards; `snippet_openclaw_speech_*` +
  `snippet_openclaw_voice_call_*` + `snippet_hermes_agent_tools_{tts_routing,transcription,voice_mode}` for the
  inworld TTS card. Direct hits: `snippet_hermes_agent_plugins_provider_kimi_coding` (kimi),
  `snippet_hermes_agent_plugins_platform_irc` (irc), `snippet_hermes_agent_plugins_platform_line` (line),
  `snippet_hermes_agent_skills_apple_imessage` (imessage).
- **Docs** (≥5 existing/note): the `hermes_agent/hermes_{model_provider_plugin,provider_routing,
  fallback_providers,adding_inference_provider,model_catalog_reference,plugin_types_surfaces,plugins_system,
  inference_providers_cloud}` provider set; `hermes_{adding_platform_adapter_plugin,messaging_*,
  messaging_gateway_architecture,webhooks_*}` channel set; `hermes_{tts_providers,stt_transcription,
  voice_mode_cli,use_voice_mode_guide,voice_gateway_discord_vc,messaging_media_settings}` voice set; plus
  `pi_{custom_models,cloud_providers,custom_provider_registration}`, `claude_code/cc_channels_*`,
  `cc_voice_dictation`, and `band_{integration_methods,websocket_agent_channels}`.

**New-term candidates: 0.** No genuinely cross-cutting, vault-reusable term lacking both a doc-page home (the
deeper `providers/*` `channels/*` pages owned by other sub-plans) AND an existing note appears on these 7 stub
cards. The Step 2d re-read confirmed the original Undigested Terms Plan: OpenClaw provider/channel vocabulary is
captured as the `oc_*` doc notes themselves; the only `term_dictionary` interaction is linking existing

**Issues:** none blocking. One inherited dependency — `entry_openclaw_docs.md` (master W1 pre-step) does not yet
exist; it is correctly cited as "(planned, W1)" and is the guaranteed anti-island inbound link (G7/G8). Sibling
`oc_*` docs of this series also do not yet exist; they are correctly marked "(planned, this series)" and resolve
once the wave's 7 notes are written (G5 expects these as same-wave siblings, not ghosts).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes ≥8 terms + floors (≥10 snippets, ≥10 docs), relevance-selected, with relevance statements | **PASS** | Per-Note Related Notes Mapping locks 8-9 terms · 10-11 snippets · 11 docs · 3 repos per note; every link carries a `relevance:` clause; min term count 8 (imessage/irc/line) meets the ≥8 floor. |
| CP2 | 9-GATE present per execution phase (G1-G6, G7/G8) | **PASS** | "Per-Phase Validation Gate (G1–G9)" table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost, G6 broken-link, G7/G8 discoverability; consolidated via `/tessellum-validate-note-gates`. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | "Entry Point Decision (inherited from master)" — no new entry point; 7 rows contributed to `entry_openclaw_docs.md` (master W1 pre-step); parent hub identified. |
| CP4 | Plan size manageable | **PASS** | 7 notes (1 per source page) ≤30 cap; single small wave; fits the ~30-agent fan-out cap. |
| CP5 | Note format derived from existing target-dir notes (not invented) | **PASS** | Format inherited from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` / `## Related Notes`, fixed YAML field order, forbidden-field list). |
| CP6 | Density borderline → split promoted | **PASS** | Density Re-Assessment: all 7 notes ~230-240 est. words, 0 code, ~55 lines — far under 2,500w/6c/400L caps; no borderline; no split promotions. |
| CP7 | Source word counts measured (not guessed) | **PASS** | All 7 source pages re-read 2026-06-21 from `inbox/openclaw_docs/plugins/reference/`; measured 54-62 words each (406 total), 0 code — matches plan's Source table exactly (ratio ≈1.0). |
| CP8 | Undigested terms plan + authoring requirements | **PASS** | "Undigested Terms Plan" present with per-row disposition (link-existing); "Term-Note Authoring Requirements" present (N/A — 0 new terms, multi-source mandate stated for the contingency). |
| CP8f | Slug specificity / collision audit (all notes, term + doc) | **PASS** | Provider/channel-specific term slugs (kimi/moonshot/kilocode/inworld/irc/imessage/line/tts) DB-checked ABSENT and excluded (owned by pr/ch sub-plans); 7 planned `oc_*` doc slugs collision-checked vs existing — no duplicate of an existing term or doc note; 0 new term slugs to audit. |
| CP9 | Discoverability / inlinks (G8, no graph islands) | **PASS** | "Inlinks (existing notes → new notes)" table gives every new note ≥1 outside-folder inbound link (entry_openclaw_docs rows guaranteed + repo/term reciprocal links); G7/G8 in the gate table as an EXECUTED phase. |

**RESULT: 9/9 (incl. CP8f) PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
