---
title: Sub-Plan pl06 — OpenClaw Docs: Plugins (Reference, anthropic-vertex → byteplus)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/anthropic-vertex", "plugins/reference/arcee", "plugins/reference/azure-speech", "plugins/reference/bonjour", "plugins/reference/brave", "plugins/reference/browser", "plugins/reference/byteplus"]
---


# Sub-Plan pl06: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order + body), dedup (3-way across term_dictionary / documentation / repo_openclaw*), the 9-GATE per phase, cross-references, undigested-terms ownership, and the entry-point decision are ALL inherited from the master.
> Scope here: the 7 plugin **reference** pages `anthropic-vertex` through `byteplus`. All are short stub reference cards; this sub-plan plans **7 notes (1 per page, no splits)**.

## Scope

The 7 plugin-reference stub pages covering the slice of OpenClaw's ClawHub/built-in plugin catalog from `anthropic-vertex` to `byteplus` (alphabetical). Each page is a short "plugin reference card" stating the plugin's purpose, npm/ClawHub distribution package, install route, the runtime *surface* it contributes (a provider name, a `contracts:` capability, or a plain `plugin`), and (most) a pointer to the corresponding provider/tool doc. The seven span four sub-domains: **LLM model providers** (`anthropic-vertex`, `arcee`, `byteplus`), **speech/TTS** (`azure-speech`), **web search** (`brave`), **browser tooling** (`browser`), and **gateway discovery** (`bonjour`). Priority **P3** (Phase C — plugin reference sprawl); these are 1-per-plugin catalog cards, not core architecture, so they are digested last. The code-side counterparts (`repo_openclaw_extensions`, `repo_openclaw_extensions_llm_providers`, `repo_openclaw_extensions_voice_speech`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **433 measured words** (sum of body, excluding YAML), **0 code fences**. **Planned: 7 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| anthropic-vertex | /plugins/reference/anthropic-vertex | 109 | 0 | 3 | 0 | concept |
| arcee | /plugins/reference/arcee | 54 | 0 | 3 | 0 | concept |
| azure-speech | /plugins/reference/azure-speech | 64 | 0 | 3 | 0 | concept |
| bonjour | /plugins/reference/bonjour | 48 | 0 | 2 | 0 | concept |
| brave | /plugins/reference/brave | 55 | 0 | 3 | 0 | concept |
| browser | /plugins/reference/browser | 47 | 0 | 3 | 0 | concept |
| byteplus | /plugins/reference/byteplus | 56 | 0 | 2 | 0 | concept |

> H2 set is uniform: every page has `## Distribution` + `## Surface`; five also have `## Related docs` (arcee, azure-speech, brave, browser) or an inline `## Claude Fable 5` manual section (anthropic-vertex). bonjour and byteplus have only Distribution + Surface. No H3 anywhere; 0 code fences anywhere.

## Content Strategy

- **Prioritize**: faithfully capturing each plugin's identity tuple — purpose, **package name** + **install route** (npm / ClawHub / "included in OpenClaw"), and the **surface** it registers (`providers:` name(s), `contracts:` capability, or plain `plugin`). These three facts are the load-bearing content of a plugin reference card and the only durable data on the page.
- **Do NOT split**: every page is far below the 2,500-word cap (max 109w) and single-BB (concept). Each page → exactly one note. No mixed-BB or oversize page in this batch.
- **Special content**: `anthropic-vertex` carries a manual `## Claude Fable 5` block (thinking/effort behavior of `claude-fable-5` on Vertex) — preserved verbatim as a body subsection of its note. `byteplus` registers TWO provider names (`byteplus`, `byteplus-plan`) plus a `videoGenerationProviders` contract — both captured.
- **Link-out, do NOT redefine**: provider/tool concepts live in their own docs (`/providers/arcee`, `/providers/azure-speech`, `/tools/brave-search`, `/tools/browser`) — these are PROVIDERS / TOOLS sub-plan pages (pr*/to*), so each `oc_*` note links out to its sibling doc (planned, other series) rather than duplicating provider/tool detail. Terms `term_llm` / `term_claude` / `term_text_to_speech` / `term_internal_search` / `term_browser_automation` / `term_bonjour_discovery` are LINKED, never inlined.
- **Dedup-before-create (REQUIRED, master policy)**: each of the 7 `oc_plugins_reference_*` filenames is novel (no `resources/documentation/openclaw/` notes exist yet, DB-confirmed 0 rows) and is NOT a duplicate of any `term_dictionary` or `repo_openclaw*` note — those are linked. Outcome per candidate = create.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_anthropic_vertex.md` | concept | anthropic-vertex.md: Distribution, Surface, Claude Fable 5 | 220 | The `@openclaw/anthropic-vertex-provider` plugin: registers the `anthropic-vertex` provider for Claude models on Google Vertex AI; npm/ClawHub install; documents `claude-fable-5` adaptive-thinking/effort behavior on Vertex. |
| 2 | `oc_plugins_reference_arcee.md` | concept | arcee.md: Distribution, Surface, Related docs | 170 | The `@openclaw/arcee-provider` plugin: adds the `arcee` model provider to OpenClaw; npm/ClawHub (`clawhub:@openclaw/arcee-provider`); points to the `/providers/arcee` provider doc. |
| 3 | `oc_plugins_reference_azure_speech.md` | concept | azure-speech.md: Distribution, Surface, Related docs | 180 | The `@openclaw/azure-speech` plugin (included in OpenClaw): contributes a `speechProviders` contract for Azure AI Speech TTS — MP3, native Ogg/Opus voice notes, PCM telephony; links the `/providers/azure-speech` doc. |
| 4 | `oc_plugins_reference_bonjour.md` | concept | bonjour.md: Distribution, Surface | 170 | The `@openclaw/bonjour` plugin (included in OpenClaw): advertises the local OpenClaw gateway over Bonjour/mDNS so clients can auto-discover it on the LAN; registers as a plain `plugin` surface. |
| 5 | `oc_plugins_reference_brave.md` | concept | brave.md: Distribution, Surface, Related docs | 175 | The `@openclaw/brave-plugin` plugin: contributes a `webSearchProviders` contract backing Brave Search for agent web search; npm/ClawHub; links the `/tools/brave-search` tool doc. |
| 6 | `oc_plugins_reference_browser.md` | concept | browser.md: Distribution, Surface, Related docs | 175 | The `@openclaw/browser-plugin` plugin (included in OpenClaw): contributes agent-callable `tools` plus `skills` for browser control; links the `/tools/browser` tool doc. |
| 7 | `oc_plugins_reference_byteplus.md` | concept | byteplus.md: Distribution, Surface | 185 | The `@openclaw/byteplus-provider` plugin (included in OpenClaw): registers two model providers (`byteplus`, `byteplus-plan`) plus a `videoGenerationProviders` contract for BytePlus / BytePlus Plan. |

> Each note's filename = `oc_` + the full slug with `/` and `-` replaced by `_` (`plugins/reference/anthropic-vertex` → `oc_plugins_reference_anthropic_vertex.md`). No aspect suffix needed (no splits). One BB (`concept`) per note.

## Section Coverage Map

```
plugins/reference/anthropic-vertex.md
├── ## Distribution (package, install route) ──── → note 1 (oc_plugins_reference_anthropic_vertex)
├── ## Surface (providers: anthropic-vertex) ──── → note 1
└── ## Claude Fable 5 (manual block) ──────────── → note 1
plugins/reference/arcee.md
├── ## Distribution ───────────────────────────── → note 2 (oc_plugins_reference_arcee)
├── ## Surface (providers: arcee) ─────────────── → note 2
└── ## Related docs (/providers/arcee) ────────── → note 2 (link-out)
plugins/reference/azure-speech.md
├── ## Distribution ───────────────────────────── → note 3 (oc_plugins_reference_azure_speech)
├── ## Surface (contracts: speechProviders) ───── → note 3
└── ## Related docs (/providers/azure-speech) ─── → note 3 (link-out)
plugins/reference/bonjour.md
├── ## Distribution ───────────────────────────── → note 4 (oc_plugins_reference_bonjour)
└── ## Surface (plugin) ───────────────────────── → note 4
plugins/reference/brave.md
├── ## Distribution ───────────────────────────── → note 5 (oc_plugins_reference_brave)
├── ## Surface (contracts: webSearchProviders) ── → note 5
└── ## Related docs (/tools/brave-search) ─────── → note 5 (link-out)
plugins/reference/browser.md
├── ## Distribution ───────────────────────────── → note 6 (oc_plugins_reference_browser)
├── ## Surface (contracts: tools; skills) ─────── → note 6
└── ## Related docs (/tools/browser) ──────────── → note 6 (link-out)
plugins/reference/byteplus.md
├── ## Distribution ───────────────────────────── → note 7 (oc_plugins_reference_byteplus)
└── ## Surface (providers: byteplus, byteplus-plan; contracts: videoGenerationProviders) → note 7
```
No orphaned sections. Every H2 (Distribution / Surface / Related docs / Claude Fable 5) maps to its single page note. `Related docs` pointers are reproduced as link-outs to the provider/tool sibling docs (pr*/to* series, planned).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | (none) | All 7 pages ≤109 words and single-BB (concept); each = 1 note. No page approaches the 2,500-word / 6-code-block caps or mixes building blocks. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (433 words total; 0 code fences). New `oc_` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: **concept ×7** (all are descriptive plugin-identity reference cards — what the plugin is, where it comes from, what surface it registers; no procedure/steps, no model/schema, no argument).
- Est. digest words ~**1,275** (avg ~182/note). Each note is well under caps; the digest is *larger* than the source per note because the `## Overview` + relevance-stated `## Related Notes` cross-ref section add framing the bare stub lacks — this is expected for stub-card digestion (faithful capture + vault wiring), not over-compression risk.
- Sub-domains: providers ×3 (anthropic-vertex, arcee, byteplus) · speech ×1 (azure-speech) · search ×1 (brave) · browser ×1 (browser) · discovery ×1 (bonjour).

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


### oc_plugins_reference_anthropic_vertex (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway/agent product this plugin extends; relevance: the plugin registers a provider into OpenClaw's runtime.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family, including `claude-fable-5`; relevance: this plugin serves Claude models specifically, on Vertex.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the plugin fronts a Claude LLM behind the `anthropic-vertex` provider name.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — the plugin class that registers a model provider; relevance: this note IS a provider-plugin reference card.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — externally hosted generative-AI APIs; relevance: Vertex AI is the external GenAI host the plugin targets.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — step-by-step model reasoning; relevance: documents Fable 5's adaptive-thinking and `/think` effort behavior on Vertex.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the declarative plugin descriptor; relevance: the provider plugin declares its surface via a manifest.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the SDK provider plugins are built on; relevance: an anthropic-vertex provider plugin is authored against the plugin SDK.
- [Foundation Model](../../term_dictionary/term_foundation_model.md) — large pretrained base model served by a provider; relevance: Claude on Vertex is the foundation model this plugin exposes.

**Docs**
- [Claude Code: Google Vertex AI](../claude_code/cc_google_vertex_ai.md) — configuring Claude Code against Vertex-hosted Claude; relevance: closest existing analog — same model family on the same cloud host.
- [Claude Code: Claude Platform on AWS Setup](../claude_code/cc_claude_platform_on_aws_setup.md) — Bedrock/cloud setup for Claude; relevance: parallel cloud-host provider config for the same models.
- [Claude Code: LLM Gateway (LiteLLM)](../claude_code/cc_llm_gateway_litellm.md) — fronting providers behind a gateway; relevance: an anthropic-vertex provider is one such fronted backend.
- [Claude Code: Model Selection](../claude_code/cc_model_selection.md) — choosing/restricting which model serves; relevance: `anthropic-vertex/claude-fable-5` is a selectable model id.
- [Hermes: Cloud Inference Providers](../hermes_agent/hermes_inference_providers_cloud.md) — cloud LLM provider configuration in the sibling agent; relevance: same provider-plugin pattern for Vertex/cloud Claude.
- [Hermes: Anthropic Provider Plugin](../hermes_agent/hermes_provider_aws_bedrock.md) — Bedrock-hosted Anthropic provider; relevance: cross-host counterpart of the Vertex provider.
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — how a new model provider plugin is added; relevance: explains the registration this card summarizes.
- [Pi: Cloud Providers](../pi/pi_cloud_providers.md) — cloud model providers in the Pi agent; relevance: parallel provider catalog including Vertex/Anthropic.
- [Band: Claude SDK Adapter](../band/band_adapter_claude_sdk.md) — adapting Claude SDK into a coding-agent runtime; relevance: cross-ecosystem view of serving Claude models.
- [oc_plugins_reference_arcee](oc_plugins_reference_arcee.md) (planned, this series) — sibling model-provider plugin card; relevance: same provider-plugin shape, different vendor.
- [oc_plugins_reference_byteplus](oc_plugins_reference_byteplus.md) (planned, this series) — sibling model-provider plugin card; relevance: same provider-plugin shape, includes a contract surface too.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — where LLM provider plugins live in code; relevance: code home of the anthropic-vertex provider.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the OpenClaw extension framework; relevance: the framework this plugin plugs into.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: top-level product the plugin extends.

**Snippets**
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — OpenClaw's Anthropic provider implementation; relevance: the code realizing an Anthropic-family provider.
- [snippet_hermes_agent_plugins_provider_anthropic](../../code_snippets/snippet_hermes_agent_plugins_provider_anthropic.md) — sibling Anthropic provider plugin; relevance: the cross-agent provider-plugin pattern.
- [snippet_hermes_agent_plugins_provider_bedrock](../../code_snippets/snippet_hermes_agent_plugins_provider_bedrock.md) — Bedrock-hosted Claude provider; relevance: the cloud-host provider counterpart.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-name registry; relevance: how `anthropic-vertex` gets registered as a provider name.
- [snippet_hermes_agent_core_anthropic_adapter_client](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_client.md) — Anthropic API client adapter; relevance: the client wiring behind a Claude provider.
- [snippet_hermes_agent_core_anthropic_adapter_endpoints](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_endpoints.md) — Anthropic endpoint resolution; relevance: how Vertex vs direct endpoints are selected.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK shape this provider plugin is built on.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — OpenClaw plugin SDK entrypoints; relevance: how a provider plugin declares its entry.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — CLI provider registry listing; relevance: how the new provider surfaces to users.
- [snippet_hermes_agent_cli_model_switch_entry](../../code_snippets/snippet_hermes_agent_cli_model_switch_entry.md) — switching the active model; relevance: selecting `anthropic-vertex/claude-fable-5` at runtime.

### oc_plugins_reference_arcee (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product this plugin extends; relevance: the plugin adds an Arcee provider to OpenClaw.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Arcee is an LLM model provider.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model-provider plugin class; relevance: this note is an Arcee provider-plugin card.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external generative-AI APIs; relevance: Arcee is a third-party model service.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the plugin descriptor; relevance: the provider declares its `providers: arcee` surface via manifest.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the SDK providers are built on; relevance: the Arcee provider is authored against the plugin SDK.
- [npm](../../term_dictionary/term_npm.md) — the Node package registry/CLI; relevance: the documented install route (`@openclaw/arcee-provider`) is npm.
- [LLM Foundation Model](../../term_dictionary/term_foundation_model.md) — pretrained base model exposed by a provider; relevance: Arcee serves foundation models behind this provider.
- [Model Router](../../term_dictionary/term_model_router.md) — routes requests across model providers; relevance: registering `arcee` makes it a routable provider target.

**Docs**
- [Hermes: Cloud Inference Providers](../hermes_agent/hermes_inference_providers_cloud.md) — cloud LLM providers in the sibling agent; relevance: parallel catalog where an Arcee-like provider is configured.
- [Hermes: Provider Runtime](../hermes_agent/hermes_provider_runtime.md) — how a provider is loaded at runtime; relevance: how the `arcee` provider becomes active.
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — adding a new model provider; relevance: the registration step this card summarizes.
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — model-provider plugin reference; relevance: the exact plugin type Arcee is.
- [Pi: Custom Provider Registration](../pi/pi_custom_provider_registration.md) — registering a custom model provider; relevance: cross-ecosystem analog of adding `arcee`.
- [Pi: Cloud Providers](../pi/pi_cloud_providers.md) — Pi's cloud provider catalog; relevance: parallel provider listing.
- [Claude Code: Model Selection](../claude_code/cc_model_selection.md) — selecting which model serves; relevance: an `arcee/*` model becomes selectable once registered.
- [Band: SDK Reference — Adapters](../band/band_sdk_reference_adapters.md) — provider/model adapters in Band; relevance: cross-ecosystem provider-adapter pattern.
- [oc_plugins_reference_anthropic_vertex](oc_plugins_reference_anthropic_vertex.md) (planned, this series) — sibling provider plugin; relevance: same provider-plugin shape.
- [oc_plugins_reference_byteplus](oc_plugins_reference_byteplus.md) (planned, this series) — sibling provider plugin; relevance: another model-provider card in the same alphabetical slice.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — code home of LLM provider plugins; relevance: where the Arcee provider lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework; relevance: the framework the Arcee plugin plugs into.

**Snippets**
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — a custom model provider plugin; relevance: the generic pattern Arcee follows.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-name registry; relevance: how `arcee` is registered as a provider name.
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — a multi-vendor provider cluster; relevance: shows how additional vendors like Arcee slot in.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregator; relevance: aggregating providers including ones like Arcee.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — an OpenClaw model provider impl; relevance: the provider-impl template Arcee mirrors.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK the Arcee provider is built on.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoints; relevance: how the Arcee provider declares its entry.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — CLI provider registry; relevance: how Arcee surfaces in the provider list.
- [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — resolving provider auth/credentials; relevance: Arcee's API-key resolution at use time.
- [snippet_hermes_agent_cli_models_normalize](../../code_snippets/snippet_hermes_agent_cli_models_normalize.md) — normalizing model ids across providers; relevance: how `arcee/*` model ids are normalized.

### oc_plugins_reference_azure_speech (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product this plugin extends; relevance: the plugin contributes a speech capability to OpenClaw.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — converting text to spoken audio; relevance: Azure AI Speech TTS is the plugin's core function.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — converting audio to text; relevance: the sibling speech capability in the same speech-provider surface.
- [Voice Call](../../term_dictionary/term_voice_call.md) — telephony voice sessions; relevance: PCM telephony is a documented Azure Speech output target.
- [Voice Bot](../../term_dictionary/term_voice_bot.md) — a voice-driven conversational agent; relevance: the consumer of TTS voice notes / telephony audio.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin that registers a provider/contract; relevance: this plugin registers a `speechProviders` contract.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the plugin descriptor; relevance: the plugin declares its `contracts: speechProviders` surface via manifest.
- [Multimodal](../../term_dictionary/term_multimodal.md) — handling audio/text/other modalities; relevance: TTS adds an audio output modality to the agent.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the SDK contract plugins are built on; relevance: the azure-speech plugin is authored against the plugin SDK.

**Docs**
- [Hermes: TTS Providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech provider catalog; relevance: the exact analog — TTS provider plugins incl. Azure.
- [Hermes: Voice Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — driving voice mode from the CLI; relevance: how TTS output is invoked by a user.
- [Hermes: Use Voice Mode Guide](../hermes_agent/hermes_use_voice_mode_guide.md) — using voice end-to-end; relevance: consumer-side flow that Azure TTS feeds.
- [Hermes: STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text transcription; relevance: the paired speech capability on the same surface.
- [Hermes: Voice Gateway (Discord VC)](../hermes_agent/hermes_voice_gateway_discord_vc.md) — voice over a channel; relevance: a downstream consumer of TTS audio.
- [Claude Code: Voice Dictation](../claude_code/cc_voice_dictation.md) — speech input in Claude Code; relevance: cross-ecosystem speech-capability reference.
- [Hermes: Platform Media Tools Reference](../hermes_agent/hermes_tools_reference_platform_media.md) — media (audio/image/video) tool surfaces; relevance: TTS produces media outputs (MP3/Ogg/Opus).
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the `contracts:` surface azure-speech uses.
- [oc_plugins_reference_brave](oc_plugins_reference_brave.md) (planned, this series) — sibling contract-surface plugin; relevance: same `contracts:` plugin shape, different capability.
- [oc_plugins_reference_browser](oc_plugins_reference_browser.md) (planned, this series) — sibling contract-surface plugin; relevance: same `contracts:` plugin shape.
- [oc_plugins_reference_byteplus](oc_plugins_reference_byteplus.md) (planned, this series) — also registers a media-generation contract; relevance: another media-producing contract plugin.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — code home of speech provider plugins; relevance: where azure-speech lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework; relevance: the framework azure-speech plugs into.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — telephony channel; relevance: the PCM-telephony consumer of Azure TTS.

**Snippets**
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — an OpenClaw TTS provider impl; relevance: the speech-provider template azure-speech mirrors.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — a local TTS provider; relevance: another `speechProviders` implementation.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — an STT provider; relevance: the paired speech-to-text contract surface.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline wiring; relevance: how a speech provider feeds the audio pipeline.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call audio stream; relevance: PCM telephony audio path Azure TTS targets.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — call transcription stream; relevance: the STT side of the same telephony stream.
- [snippet_openclaw_voice_call_manager](../../code_snippets/snippet_openclaw_voice_call_manager.md) — voice-call orchestration; relevance: the manager that drives TTS playback in calls.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — routing TTS requests to providers; relevance: how an azure-speech provider gets selected.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: paired speech capability invocation.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice mode tool entry; relevance: the consumer that triggers TTS.

### oc_plugins_reference_bonjour (9t · 10s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway product this plugin extends; relevance: bonjour advertises the OpenClaw gateway.
- [Bonjour Discovery](../../term_dictionary/term_bonjour_discovery.md) — Bonjour/mDNS zero-config LAN service discovery; relevance: the exact mechanism this plugin implements.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — the plugin class; relevance: bonjour registers as a plain `plugin` surface (the simplest plugin form).
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the plugin descriptor; relevance: the plugin declares its `plugin` surface via manifest.
- [WebSocket](../../term_dictionary/term_websocket.md) — the gateway's persistent client transport; relevance: clients that discover the gateway connect over it.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the SDK plugins are built on; relevance: the bonjour plugin is authored against the plugin SDK.
- [DNS](../../term_dictionary/term_dns.md) — the name-resolution protocol mDNS extends; relevance: mDNS is multicast DNS, the basis of Bonjour discovery.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — the gateway pattern OpenClaw implements; relevance: the gateway being advertised on the LAN.

**Docs**
- [Claude Code: Remote Control](../claude_code/cc_remote_control.md) — connecting a client to a remote backend; relevance: discovery is the prelude to remote connection.
- [Hermes: Gateway PID/Discovery](../hermes_agent/hermes_desktop_remote_backend.md) — locating the local backend; relevance: parallel local-gateway discovery flow.
- [Hermes: Dashboard Auth (Remote)](../hermes_agent/hermes_dashboard_auth_remote.md) — authenticating to a discovered gateway; relevance: the auth step after discovery.
- [Band: A2A Gateway](../band/band_a2a_gateway.md) — agent-to-agent gateway; relevance: cross-ecosystem gateway-advertisement analog.
- [Band: A2A Overview](../band/band_a2a_overview.md) — agent-to-agent connectivity model; relevance: how agents/clients find each other.
- [Hermes: OAuth over SSH](../hermes_agent/hermes_oauth_over_ssh.md) — alternative remote-connect transport; relevance: contrast to LAN auto-discovery for reaching the gateway.
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the bare `plugin` surface bonjour uses.
- [oc_plugins_reference_browser](oc_plugins_reference_browser.md) (planned, this series) — sibling plugin card; relevance: same plugin-reference shape.
- [/gateway/bonjour](oc_gateway_bonjour.md) (planned, gw* series) — the gateway-side Bonjour doc; relevance: the gateway config this plugin's advertisement targets.
- [/gateway/discovery](oc_gateway_discovery.md) (planned, gw* series) — gateway discovery doc; relevance: the broader discovery feature bonjour participates in.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway server; relevance: the gateway being advertised over Bonjour.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework; relevance: the framework the bonjour plugin plugs into.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: the product whose gateway is advertised.

**Snippets**
- [snippet_openclaw_android_gateway_session_mdns](../../code_snippets/snippet_openclaw_android_gateway_session_mdns.md) — Android client mDNS gateway discovery; relevance: the client side of Bonjour/mDNS advertisement.
- [snippet_openclaw_ios_gateway_pairing](../../code_snippets/snippet_openclaw_ios_gateway_pairing.md) — iOS gateway pairing after discovery; relevance: the pairing step following auto-discovery.
- [snippet_hermes_agent_cli_gateway_pid_discovery](../../code_snippets/snippet_hermes_agent_cli_gateway_pid_discovery.md) — locating the local gateway; relevance: parallel local-gateway discovery mechanism.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway server methods; relevance: the server endpoints clients reach post-discovery.
- [snippet_openclaw_gateway_server_impl_auth_startup](../../code_snippets/snippet_openclaw_gateway_server_impl_auth_startup.md) — gateway startup/auth; relevance: when the advertisement is published at server start.
- [snippet_openclaw_gateway_server_impl_shutdown](../../code_snippets/snippet_openclaw_gateway_server_impl_shutdown.md) — gateway shutdown; relevance: when the Bonjour advertisement is withdrawn.
- [snippet_hermes_agent_gw_platform_api_server_routes](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_routes.md) — gateway HTTP routes; relevance: the surfaces a discovered client connects to.
- [snippet_hermes_agent_gw_platform_api_server_connect](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_connect.md) — client connect handshake; relevance: the connect that follows discovery.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle hooks; relevance: a plain `plugin` like bonjour runs on lifecycle start/stop.
- [snippet_hermes_agent_gw_config_schema](../../code_snippets/snippet_hermes_agent_gw_config_schema.md) — gateway config schema; relevance: where discovery/advertisement settings are configured.

### oc_plugins_reference_brave (9t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product this plugin extends; relevance: brave adds a web-search capability to OpenClaw.
- [Internal Search](../../term_dictionary/term_internal_search.md) — keyword/full-text search capability; relevance: closest vault term for the web-search function brave provides.
- [Hybrid Search](../../term_dictionary/term_hybrid_search.md) — combined lexical+semantic retrieval; relevance: search-retrieval concept the web-search tool serves.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin that registers a contract/provider; relevance: brave registers a `webSearchProviders` contract.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the plugin descriptor; relevance: declares the `contracts: webSearchProviders` surface.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent-invokable tool calls; relevance: web search is exposed as an agent-callable tool/contract.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — registry of agent tools; relevance: the contract registry the brave provider populates.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — retrieving relevant documents for a query; relevance: web search is an IR task.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: web search supplies the external retrieval RAG consumes.

**Docs**
- [Hermes: Web Search & Extract](../hermes_agent/hermes_web_search_extract.md) — web-search tool config in the sibling agent; relevance: the exact analog of the brave web-search contract.
- [Hermes: Tool Gateway](../hermes_agent/hermes_tool_gateway.md) — how tools are exposed to the agent; relevance: how a web-search tool is surfaced.
- [Hermes: Core Tools Reference](../hermes_agent/hermes_tools_reference_core.md) — built-in tool catalog; relevance: web search is one such agent tool.
- [Hermes: Adding a Built-in Tool](../hermes_agent/hermes_adding_built_in_tool.md) — how a tool/contract is added; relevance: the registration brave performs.
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the `contracts:` surface brave uses.
- [Hermes: X Search (Grok)](../hermes_agent/hermes_x_search_grok.md) — another web-search provider; relevance: a sibling `webSearchProviders` backend.
- [Pi: Custom Tools Extension](../pi/pi_extensions_custom_tools.md) — registering custom agent tools; relevance: cross-ecosystem tool/contract registration.
- [oc_plugins_reference_browser](oc_plugins_reference_browser.md) (planned, this series) — sibling tool/contract plugin; relevance: same `contracts:` plugin shape, browser tooling.
- [oc_plugins_reference_azure_speech](oc_plugins_reference_azure_speech.md) (planned, this series) — sibling contract plugin; relevance: same `contracts:` surface pattern.
- [/tools/brave-search](oc_tools_brave_search.md) (planned, to* series) — the brave-search tool doc; relevance: the tool this provider backs.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework; relevance: the framework the brave plugin plugs into.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the agent runtime; relevance: invokes the web-search tool brave contributes.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: the product the plugin extends.

**Snippets**
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web-search/fetch tool impl; relevance: the code realizing a web-search tool like brave.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web plugin surface; relevance: a web-capability plugin parallel to brave.
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — registering tools into the agent; relevance: how the web-search contract gets registered.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider/contract registry; relevance: how `webSearchProviders` gets populated.
- [snippet_slipbot_bm25_tool](../../code_snippets/snippet_slipbot_bm25_tool.md) — a BM25 search tool; relevance: lexical-search counterpart to web search.
- [snippet_slipbot_query_expander](../../code_snippets/snippet_slipbot_query_expander.md) — query expansion before search; relevance: search query preprocessing the tool may use.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK brave's contract plugin is built on.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package + contract declaration; relevance: how a `contracts:` surface is declared.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor contract; relevance: the contract shape a web-search tool exposes.

### oc_plugins_reference_browser (9t · 11s · 10d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product this plugin extends; relevance: browser adds agent-callable browser tools/skills to OpenClaw.
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic browser control; relevance: the plugin's core function.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent-invokable tool calls; relevance: browser contributes agent-callable `tools`.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — registry of agent tools; relevance: the plugin registers into the `tools` contract.
- [Skills](../../term_dictionary/term_skills.md) — packaged agent capabilities; relevance: the plugin also contributes `skills`.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — plugin that registers a contract/surface; relevance: browser registers `tools` + `skills` surfaces.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the plugin descriptor; relevance: declares the `contracts: tools; skills` surface.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agents that drive tools; relevance: the agent that invokes the browser tools/skills.
- [Multimodal](../../term_dictionary/term_multimodal.md) — handling visual/page content; relevance: browser tooling yields screenshots/DOM the agent reads.

**Docs**
- [Claude Code: Chrome Browser Automation](../claude_code/cc_chrome_browser_automation.md) — driving a browser from a coding agent; relevance: the exact analog of the browser plugin.
- [Hermes: Browser Automation Setup](../hermes_agent/hermes_browser_automation_setup.md) — setting up agent browser control; relevance: configuring the browser tool/skill surface.
- [Hermes: Core Tools Reference](../hermes_agent/hermes_tools_reference_core.md) — built-in agent tools; relevance: browser tools are among them.
- [Hermes: Creating Skill Format](../hermes_agent/hermes_creating_skill_format.md) — authoring agent skills; relevance: the `skills` surface this plugin contributes to.
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: explains the `tools`/`skills` surfaces browser uses.
- [Claude Code: SDK Skills](../claude_code/cc_sdk_skills.md) — defining skills via SDK; relevance: cross-ecosystem skills surface analog.
- [Pi: Custom Tools Extension](../pi/pi_extensions_custom_tools.md) — registering custom tools; relevance: cross-ecosystem tool registration like browser's.
- [oc_plugins_reference_brave](oc_plugins_reference_brave.md) (planned, this series) — sibling tool/contract plugin; relevance: same `contracts:` plugin shape, web search.
- [oc_plugins_reference_azure_speech](oc_plugins_reference_azure_speech.md) (planned, this series) — sibling contract plugin; relevance: same `contracts:` surface pattern.
- [/tools/browser](oc_tools_browser.md) (planned, to* series) — the browser tool doc; relevance: the tool this plugin contributes.

**Repos**
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the agent runtime; relevance: invokes the browser tools/skills.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — the skills subsystem; relevance: the `skills` surface this plugin contributes to.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework; relevance: the framework the browser plugin plugs into.

**Snippets**
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — browser navigation tool; relevance: a core browser tool the plugin exposes.
- [snippet_hermes_agent_tools_browser_dom](../../code_snippets/snippet_hermes_agent_tools_browser_dom.md) — DOM inspection tool; relevance: another browser tool surface.
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — browser session management; relevance: session state behind the browser tools.
- [snippet_hermes_agent_tools_browser_cdp](../../code_snippets/snippet_hermes_agent_tools_browser_cdp.md) — Chrome DevTools Protocol control; relevance: the control transport browser tooling uses.
- [snippet_hermes_agent_tools_browser_screenshot](../../code_snippets/snippet_hermes_agent_tools_browser_screenshot.md) — screenshot capture; relevance: a multimodal browser tool output.
- [snippet_hermes_agent_tools_browser_supervisor_lifecycle](../../code_snippets/snippet_hermes_agent_tools_browser_supervisor_lifecycle.md) — browser process lifecycle; relevance: managing the browser the plugin drives.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — dispatching browser tool calls; relevance: how browser tool calls are routed from the plugin.
- [snippet_hermes_agent_tools_skills_invoke](../../code_snippets/snippet_hermes_agent_tools_skills_invoke.md) — invoking a skill; relevance: the `skills` surface this plugin also contributes.
- [snippet_hermes_agent_skills_canonical_format](../../code_snippets/snippet_hermes_agent_skills_canonical_format.md) — skill definition format; relevance: the shape of the skills browser registers.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor contract; relevance: the `tools` contract browser populates.
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — registering tools into the agent; relevance: how browser's tools get registered.

### oc_plugins_reference_byteplus (9t · 11s · 11d)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product this plugin extends; relevance: byteplus adds model + media-gen providers to OpenClaw.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: BytePlus / BytePlus Plan are LLM model providers.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model-provider plugin class; relevance: this note registers two providers (`byteplus`, `byteplus-plan`).
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external generative-AI APIs; relevance: BytePlus is a third-party GenAI service.
- [Video Processing](../../term_dictionary/term_video_processing.md) — generating/handling video; relevance: the `videoGenerationProviders` contract this plugin also registers.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the plugin descriptor; relevance: declares the providers + `videoGenerationProviders` contract surfaces.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the SDK provider/contract plugins are built on; relevance: byteplus is authored against the plugin SDK.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multiple output modalities; relevance: byteplus spans text (LLM) and video generation.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — generative model class behind media gen; relevance: the model family video generation typically uses.

**Docs**
- [Hermes: Video-Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — a video-generation provider plugin; relevance: the exact analog of byteplus's `videoGenerationProviders` contract.
- [Hermes: Image-Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — an image-generation provider plugin; relevance: sibling media-generation provider pattern.
- [Hermes: Image Generation](../hermes_agent/hermes_image_generation.md) — image-gen tool/feature; relevance: the media-gen capability family byteplus's contract joins.
- [Hermes: Cloud Inference Providers](../hermes_agent/hermes_inference_providers_cloud.md) — cloud LLM providers; relevance: byteplus's two model providers are configured the same way.
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — model-provider plugin reference; relevance: the plugin type for `byteplus` / `byteplus-plan`.
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — registering a model provider; relevance: the registration this card summarizes.
- [Hermes: Platform Media Tools Reference](../hermes_agent/hermes_tools_reference_platform_media.md) — media (image/video) tool surfaces; relevance: where generated video is delivered.
- [Pi: Cloud Providers](../pi/pi_cloud_providers.md) — cloud provider catalog; relevance: parallel multi-provider listing.
- [oc_plugins_reference_anthropic_vertex](oc_plugins_reference_anthropic_vertex.md) (planned, this series) — sibling model-provider plugin; relevance: same provider-plugin shape.
- [oc_plugins_reference_arcee](oc_plugins_reference_arcee.md) (planned, this series) — sibling model-provider plugin; relevance: same provider-plugin shape.
- [oc_plugins_reference_azure_speech](oc_plugins_reference_azure_speech.md) (planned, this series) — also registers a media contract; relevance: another media-producing contract plugin.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — code home of LLM provider plugins; relevance: where the byteplus providers live.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework; relevance: the framework byteplus plugs into.

**Snippets**
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen provider dispatch; relevance: the code path for the `videoGenerationProviders` contract.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-generation tool; relevance: how generated video is requested by the agent.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen provider dispatch; relevance: sibling media-gen provider dispatch pattern.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-generation tool; relevance: the adjacent media-gen capability.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-name registry; relevance: how `byteplus` and `byteplus-plan` register.
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — China-region provider cluster; relevance: BytePlus (ByteDance) fits this regional provider group.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — provider aggregator; relevance: aggregating multi-vendor model providers like byteplus.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: the SDK byteplus's plugin is built on.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package + contract declaration; relevance: how a plugin declares both providers and a contract.
- [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — CLI provider registry; relevance: how byteplus's two providers surface to users.
- [snippet_hermes_agent_toolsets_definitions](../../code_snippets/snippet_hermes_agent_toolsets_definitions.md) — toolset/contract definitions; relevance: how the media-gen contract is defined as a toolset.


## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc notes by its home sub-plan, NOT promoted to `term_dictionary`; the only `term_dictionary` interaction is LINKING existing terms. Provider/plugin/contract proper names are documented as configuration data, not promoted to terms.

| Term (appears in source) | Disposition |
|---|---|
| anthropic-vertex / arcee / byteplus (provider names) | Config data captured in their `oc_*` notes; link `term_llm` / `term_claude` / `term_third_party_genai_services`. Not promoted. |
| Claude Fable 5 / `claude-fable-5` | Model name captured in note 1 body (thinking/effort behavior); link `term_claude` + `term_chain_of_thought`. Not promoted. |
| Google Vertex AI | Cloud host captured as config in note 1; link `term_third_party_genai_services` (no existing `term_vertex_ai` — DB-confirmed MISSING — and a cloud-host name is not vault-reusable cross-cutting vocab). Not promoted. |
| speechProviders / webSearchProviders / videoGenerationProviders / tools / skills (contract names) | OpenClaw plugin-contract identifiers; captured verbatim as the Surface data in their `oc_*` notes; link `term_text_to_speech` / `term_internal_search` / `term_video_processing` / `term_function_calling` / `term_tool_registry`. Not promoted (product-specific contract names). |
| ClawHub | OpenClaw plugin registry; documented as install-route config; no existing `term_clawhub` (DB-confirmed MISSING) but ClawHub has its own doc sub-plans (cw01–03) — it is digested there as `oc_clawhub_*`, NOT as a new term here. Link/defer to cw* series. |
| Azure AI Speech / Brave Search / BytePlus (vendor/service names) | Third-party service names; captured as config; link existing capability terms. Not promoted. |

**New `term_dictionary` captures from pl06: 0** (expected per master). No genuinely cross-cutting, vault-reusable term lacks both a doc-page home AND an existing note. Augment Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms)** — pl06 authors zero `term_dictionary` notes (inherited from master; provider/contract/vendor names link existing terms or are captured as `oc_*` config data). If augment's Step 2d re-scan surfaces a genuinely cross-cutting reusable term with no doc-page home and no existing note, capture it via `/tessellum-capture-term-note` and add it to the best-fit glossary (`acronym_glossary_developer.md` for plugin/SDK vocab, `acronym_glossary_llm.md` for model/provider vocab) — not expected here.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single phase (7 notes, P3). Gate table identical to the master's 9-GATE; all must pass before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean for all 7 notes (YAML field order, `## Overview` + `## Related Notes`, footer). |
| G2 | Grounding | Each note's facts (package, install route, surface, Fable-5 behavior) diff-match `inbox/openclaw_docs/plugins/reference/<page>.md`; no invented capability. |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2500 words / ≤6 code blocks; one BB (concept); every source H2 covered (Section Coverage Map). |
| G4 | Cross-Reference | ≥6 relevance-selected term links + repo/sibling/entry links per note, each with a relevance statement. |
| G6 | Broken-link | `/tessellum-fix-broken-links` → 0 broken links after reindex. |
| G7 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` + repo/term inlinks). |
| G8 | In-degree ≥1 | `note_links` confirms in-degree ≥1 per new note (anti-island). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_anthropic_vertex oc_plugins_reference_arcee oc_plugins_reference_azure_speech oc_plugins_reference_bonjour oc_plugins_reference_brave oc_plugins_reference_browser oc_plugins_reference_byteplus"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required H2 sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION '$sec' in $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # has ≥1 sibling oc_ link (discoverability within series)
  grep -q "($SIBLING_PREFIX" "$f" || echo "NO sibling $SIBLING_PREFIX link in $n"
  # density caps
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code / $lines L)"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# G5/G6 after reindex:
bash scripts/update_notes_database.sh
# (then /tessellum-fix-ghost-references and /tessellum-fix-broken-links per master)
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_anthropic_vertex | concept | 220 | 0 | ✅ |
| 2 | oc_plugins_reference_arcee | concept | 170 | 0 | ✅ |
| 3 | oc_plugins_reference_azure_speech | concept | 180 | 0 | ✅ |
| 4 | oc_plugins_reference_bonjour | concept | 170 | 0 | ✅ |
| 5 | oc_plugins_reference_brave | concept | 175 | 0 | ✅ |
| 6 | oc_plugins_reference_browser | concept | 175 | 0 | ✅ |
| 7 | oc_plugins_reference_byteplus | concept | 185 | 0 | ✅ |

No note approaches any cap (max 220w vs 2,500; 0 code vs 6; all ≤400 lines). These are intentionally small reference cards; no over-compression (every source fact is captured) and no over-expansion (no invented content — the digest-over-source delta is only `## Overview` framing + relevance-stated `## Related Notes` wiring).

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (W1, created as a master pre-step) under the **Plugins → Reference** cluster (pl06 segment, anthropic-vertex → byteplus). Each note receives its entry-point back-link at finalization; this back-link is one mechanism satisfying G7/G8 (≥1 outside-folder inbound link). No new entry point is created by this sub-plan (master owns W1).

## Inlinks (existing notes → new notes)


- `entry_openclaw_docs.md` (planned, pre-step) → all 7 notes (primary discoverability).
- `repo_openclaw_extensions.md` → all 7 (each note documents a plugin in the extensions framework).
- `repo_openclaw_extensions_llm_providers.md` → notes 1, 2, 7 (anthropic-vertex, arcee, byteplus provider plugins).
- `repo_openclaw_extensions_voice_speech.md` → note 3 (azure-speech).
- `repo_openclaw_gateway.md` → note 4 (bonjour advertises the gateway).
- `repo_openclaw_agents.md` → notes 5, 6 (search + browser tools invoked by the agent runtime).
- `term_openclaw.md` → all 7 (product ↔ plugin reference).
- `term_provider_plugin.md` → notes 1, 2, 7; `term_text_to_speech.md` → note 3; `term_bonjour_discovery.md` → note 4; `term_internal_search.md` → note 5; `term_browser_automation.md` → note 6; `term_video_processing.md` → note 7.

## Pacing Rules (inherited from master)

One execution phase, 7 notes; 8 gates before commit. Re-read each source page; reproduce the package / install-route / surface facts verbatim (no fences to copy — all pages are fence-free). One BB (concept) per note. Cap dynamic-workflow fan-out ≤30 agents/run (7 notes here, well within). `git pull --rebase --autostash` before committing; no Claude co-author trailer. Incremental reindex; verify `note_links` + 0 broken links + in-degree ≥1 before commit+push.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment; floors raised + locked) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)


**What was locked (per-note counts):**

| Note | Terms | Snippets | Docs | Repos | Floors met (≥8t · ≥10s · ≥10d) |
|---|---:|---:|---:|---:|---|
| oc_plugins_reference_anthropic_vertex | 9 | 11 | 11 | 3 | YES |
| oc_plugins_reference_arcee | 9 | 10 | 10 | 3 | YES |
| oc_plugins_reference_azure_speech | 9 | 11 | 11 | 3 | YES |
| oc_plugins_reference_bonjour | 9 | 10 | 10 | 3 | YES |
| oc_plugins_reference_brave | 9 | 11 | 10 | 3 | YES |
| oc_plugins_reference_browser | 9 | 11 | 10 | 3 | YES |
| oc_plugins_reference_byteplus | 9 | 11 | 11 | 3 | YES |

**Verification (this session):**

**Density re-measure (CP7 input):** strict body-word count (excl. YAML frontmatter, plan's `sed -n '/^---$/,/^---$/!p'` method) = anthropic-vertex 79 · arcee 30 · azure-speech 35 · bonjour 24 · brave 30 · browser 27 · byteplus 30 → **total 255 body words** (plan stated 433; the plan over-counted, not under-counted — this only relaxes, never tightens, the split decision). Max page is 79 words vs the 2,500-word cap; 0 code fences anywhere. No re-split needed; the no-split decision stands.

**New-term candidates:** **0.** Step 2d re-scan of all 7 pages surfaced no genuinely cross-cutting, vault-reusable term lacking BOTH a doc-page home AND an existing note. Provider/contract/vendor proper names (`anthropic-vertex`, `arcee`, `byteplus`, `byteplus-plan`, `claude-fable-5`, `speechProviders`, `webSearchProviders`, `videoGenerationProviders`, `tools`, `skills`, `Google Vertex AI`, `Azure AI Speech`, `Brave Search`, `ClawHub`) remain captured as config data in their `oc_*` notes and link existing terms — consistent with the master's OpenClaw-vocabulary-as-doc-notes policy. Best-fit glossary, if a future term were ever needed: `acronym_glossary_developer.md` (plugin/SDK vocab) or `acronym_glossary_llm.md` (model/provider vocab). Not exercised by pl06.

**Dedup (CP8f):** `resources/documentation/openclaw/` currently holds 0 notes (DB-confirmed); all 7 planned `oc_plugins_reference_*` slugs are novel and do not duplicate any existing `term_dictionary`, `documentation/`, or `repo_openclaw*` note (those are LINKED, not recreated). No too-general term slugs (pl06 creates 0 terms). No collisions.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step ≥8 terms + floors | **PASS** | Per-Note Related Notes Mapping (LOCKED) present; every note has 9 terms (≥8), 10-11 snippets (≥10), 10-11 docs (≥10), 3 repos; each link has a `relevance:` statement. Bare-link/no-relevance = 0. |
| CP2 | 9-GATE present per phase (G1-G6, G8) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present for the single phase; G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Ref, G5 Ghost, G6 Broken-link, G7/G8 Discoverability all listed with pass criteria; `/tessellum-fix-ghost-references` + `/tessellum-fix-broken-links` referenced in Validation Scripts. |
| CP4 | Size | **PASS** | 7 planned notes, single phase — well under the ≤30 cap; no split strategy required. |
| CP5 | Format derived (not invented) | **PASS** | Inherits master Format Definition derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` opener, `## Related Notes` reference section, bold `**Source**`/`**Last Updated**`/`**Status**` footer, fixed YAML field order, forbidden-field list). Validation script greps `## Overview` + `## Related Notes`. |
| CP6 | Density (borderline → split) | **PASS** | Max body 79 words / 0 code fences / est ≤400 lines per note; no borderline note. Density Re-Assessment + re-measure (255 total body words) confirm no over-density and no need to promote any split. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-read + re-measured all 7 pages this session (79/30/35/24/30/27/30 body words; 255 total). No page exceeds 1.5× its estimate (plan over-counted at 433; ratio <1 everywhere) — zero under-estimation; all far below the 2,500-word cap. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (7-row disposition table, all "Not promoted / link existing"); New term captures = 0 (expected per master); `## Term-Note Authoring Requirements` present as N/A-with-fallback (0 new terms; capture path + best-fit glossary specified if a re-scan ever surfaces one). Step 2d re-scan this session: 0 new terms. |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound source (entry_openclaw_docs + repo_openclaw* + term inlinks); G7/G8 in the gate table require DB in-degree ≥1 per new note (anti-island), verified at execution. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending` → `ready`.
