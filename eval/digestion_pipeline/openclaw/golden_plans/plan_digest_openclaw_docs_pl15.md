---
title: Sub-Plan pl15 — OpenClaw Docs: Plugins (minimax, mistral, moonshot, msteams, nextcloud-talk, nostr, novita)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/minimax", "plugins/reference/mistral", "plugins/reference/moonshot", "plugins/reference/msteams", "plugins/reference/nextcloud-talk", "plugins/reference/nostr", "plugins/reference/novita"]
---

# Sub-Plan pl15: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_` prefix) / format / dedup / 9-GATE / cross-refs / entry-point (`entry_openclaw_docs.md`) decisions are ALL inherited from the master; this file re-derives only what is specific to its 7 assigned `plugins/reference/*` pages from a fresh measured re-read.

## Scope

The 7 plugin-reference manifest pages for built-in OpenClaw plugins: four **model/media provider** plugins
(`minimax`, `mistral`, `moonshot`, `novita`) and three **chat-channel** plugins (`msteams`,
`nextcloud-talk`, `nostr`). Each `plugins/reference/<name>` page is a thin, machine-generated manifest stub
(summary, npm package name, install route, the contract "Surface" it implements, and a Related-docs pointer
to the corresponding `/providers/<name>` or `/channels/<name>` how-to page). **Priority: P3 (Phase C — plugin
reference sprawl).** The plugin reference is a catalog/index layer, not operational depth; the substantive
provider/channel setup content lives in the `providers/*` (pr05/pr06) and `channels/*` (ch04) pages and is
LINKED, not duplicated here. The code-side counterparts `repo_openclaw_extensions`,
`repo_openclaw_extensions_llm_providers`, and `repo_openclaw_channels*` are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **412 measured words total** (avg ~59 words/page). **Planned: 2 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| MiniMax plugin | plugins/reference/minimax | 66 | 0 | 3 | 0 | concept (provider plugin manifest) |
| Mistral plugin | plugins/reference/mistral | 58 | 0 | 3 | 0 | concept (provider plugin manifest) |
| Moonshot plugin | plugins/reference/moonshot | 57 | 0 | 3 | 0 | concept (provider plugin manifest) |
| Microsoft Teams plugin | plugins/reference/msteams | 57 | 0 | 3 | 0 | concept (channel plugin manifest) |
| Nextcloud Talk plugin | plugins/reference/nextcloud-talk | 55 | 0 | 3 | 0 | concept (channel plugin manifest) |
| Nostr plugin | plugins/reference/nostr | 57 | 0 | 3 | 0 | concept (channel plugin manifest) |
| Novita plugin | plugins/reference/novita | 62 | 0 | 3 | 0 | concept (provider plugin manifest) |

Every page shares the identical three-H2 skeleton — `## Distribution` (Package + Install route),
`## Surface` (`providers:`/`channels:` list + implemented `contracts:`), `## Related docs` (one pointer
link) — preceded by a one-sentence H1 summary. No H3, no code fences, no prose body beyond the summary line.

## Content Strategy

- **Prioritize**: the catalog facts that are unique per plugin and not stated elsewhere — npm package name,
  install route (bundled-in-OpenClaw vs npm/ClawHub), the provider/channel identifiers each plugin
  registers, and the typed `contracts` (Surface) each provider plugin satisfies (image/media/music/speech/
  video/web-search/embedding/realtime-transcription). This is the index layer FZ-15 integration work needs
  to answer "which plugin provides X, and how is it shipped".
- **Consolidate (split-in-reverse)**: each page is ~55-66 words and structurally identical — far below the
  one-note density floor. Per master density caps (≤2500w/≤6 code) and BB-atomicity, **2 grouped catalog
  notes** are correct, not 7 near-empty stubs. Group by BB-coherent function: (1) the four provider plugins
  into one provider-plugin catalog note; (2) the three channel plugins into one channel-plugin catalog note.
  Each grouped note stays one building_block (concept) and well under caps. See Split Decisions.
- **Link-out (no duplication)**: each plugin's substantive setup/config how-to lives on its `/providers/<name>`
  or `/channels/<name>` page (owned by pr05/pr06 and ch04) — referenced via the Related-docs pointer, NOT
  reproduced. Provider model families (Mistral, MiniMax, Moonshot/Kimi, Novita) and chat platforms (Teams,
  Nextcloud Talk, Nostr) are documented as catalog entries, NOT promoted to `term_dictionary` notes;
  `term_llm` / `term_third_party_genai_services` / `term_provider_plugin` / `term_chatbot` are LINKED.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_provider_plugins.md` | concept | minimax.md, mistral.md, moonshot.md, novita.md — all H2 (Distribution, Surface, Related docs) | 550 | Catalog of OpenClaw's built-in model/media provider plugins (MiniMax, Mistral, Moonshot, Novita): per-plugin npm package, install route, the `providers:` identifiers each registers, and the typed media `contracts` (image/media-understanding/music/speech/video/web-search/embedding/realtime-transcription) each Surface satisfies, with pointers to the per-provider setup pages. |
| 2 | `oc_plugins_reference_channel_plugins.md` | concept | msteams.md, nextcloud-talk.md, nostr.md — all H2 (Distribution, Surface, Related docs) | 450 | Catalog of OpenClaw's built-in chat-channel plugins (Microsoft Teams, Nextcloud Talk, Nostr): per-plugin npm package, install route (npm; ClawHub), the `channels:` identifier each registers, and what each channel covers (Teams bot conversations, Nextcloud Talk conversations, Nostr NIP-04 encrypted DMs), with pointers to the per-channel setup pages. |

Filename derivation per master rule (`oc_` + full slug, `/` and `-` → `_`): the 7 individual slugs would be
`oc_plugins_reference_minimax.md` … `oc_plugins_reference_nostr.md`; the two consolidated catalog notes use the
descriptive aspect suffixes `_provider_plugins` / `_channel_plugins` under the shared `plugins/reference`
slug stem, since each note aggregates multiple sibling reference pages.

## Section Coverage Map

```
plugins/reference/minimax.md
├── (H1 summary: MiniMax / MiniMax Portal provider) ── → note 1 (oc_plugins_reference_provider_plugins)
├── ## Distribution (@openclaw/minimax-provider; included) → note 1
├── ## Surface (providers: minimax, minimax-portal;
│   contracts: image/media/music/speech/video/web-search) → note 1
└── ## Related docs (/providers/minimax) ────────────── → note 1 (link-out)
plugins/reference/mistral.md
├── (H1 summary: Mistral provider) ─────────────────── → note 1
├── ## Distribution (@openclaw/mistral-provider; included) → note 1
├── ## Surface (providers: mistral; contracts:
│   media-understanding/memory-embedding/realtime-transcription) → note 1
└── ## Related docs (/providers/mistral) ───────────── → note 1
plugins/reference/moonshot.md
├── (H1 summary: Moonshot provider) ────────────────── → note 1
├── ## Distribution (@openclaw/moonshot-provider; included) → note 1
├── ## Surface (providers: moonshot; contracts:
│   media-understanding/web-search) ────────────────── → note 1
└── ## Related docs (/providers/moonshot) ──────────── → note 1
plugins/reference/novita.md
├── (H1 summary: Novita / Novita AI / Novitaai provider) → note 1
├── ## Distribution (@openclaw/novita-provider; included) → note 1
├── ## Surface (providers: novita, novita-ai, novitaai) → note 1
└── ## Related docs (/providers/novita) ────────────── → note 1
plugins/reference/msteams.md
├── (H1 summary: Microsoft Teams bot conversations) ── → note 2 (oc_plugins_reference_channel_plugins)
├── ## Distribution (@openclaw/msteams; npm; ClawHub) ─ → note 2
├── ## Surface (channels: msteams) ─────────────────── → note 2
└── ## Related docs (/channels/msteams) ────────────── → note 2 (link-out)
plugins/reference/nextcloud-talk.md
├── (H1 summary: Nextcloud Talk conversations) ─────── → note 2
├── ## Distribution (@openclaw/nextcloud-talk; npm; ClawHub) → note 2
├── ## Surface (channels: nextcloud-talk) ──────────── → note 2
└── ## Related docs (/channels/nextcloud-talk) ─────── → note 2
plugins/reference/nostr.md
├── (H1 summary: Nostr NIP-04 encrypted DMs) ───────── → note 2
├── ## Distribution (@openclaw/nostr; npm; ClawHub) ── → note 2
├── ## Surface (channels: nostr) ───────────────────── → note 2
└── ## Related docs (/channels/nostr) ──────────────── → note 2
```

No orphaned sections — all 7 pages × 3 H2 + H1 summary mapped. Per-provider/per-channel deep setup
(`/providers/*`, `/channels/*`) is referenced via Related docs (owned by pr05/pr06/ch04), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| 7 separate `plugins/reference/*` stub pages (412w total; 55-66w each; identical 3-H2 manifest skeleton, 0 code) | 2 consolidated catalog notes (`_provider_plugins`, `_channel_plugins`) | Each page is far below the one-note density floor; a 1:1 mapping would create 7 near-empty stubs that violate atomicity-by-substance and overwhelm the index with no added signal. Reverse-split (consolidate) into 2 BB-coherent catalog notes grouped by function — provider plugins vs channel plugins. Each grouped note remains one building_block (concept), ~450-550w, 0 code → comfortably within caps. This is a downward revision from the master's placeholder estimate of 11 notes (the master estimate is a per-sub-plan default of ~1.5×pages; these stub pages do not support it). |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (412 measured words, 0 code fences). New `oc_` notes: **2**. New `term_dictionary` notes: **0**.
- BB distribution: concept ×2 (both catalog/index notes).
- Est. digest words ~1,000 (note 1 ~550, note 2 ~450). 0 source code fences → both notes 0 code blocks
  (small config-pointer tables only; well under the ≤6 cap).
- Revised note count vs master placeholder: **2 (not 11)** — locked here at plan stage; rationale in Split Decisions.
- Cross-refs (LOCKED at xref-augment 2026-06-21): per-note Related Notes meet raised floors **≥8 terms ·
  docs are sibling `oc_*` (planned, this series) and `entry_openclaw_docs` is (planned, master W1). Each link
  carries a per-link relevance statement. See Per-Note Related Notes Mapping.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (source re-read 2026-06-21;
> `entry_openclaw_docs` is **(planned, master W1)** — confirmed absent in DB on 2026-06-21, so it is NOT
> counted toward the existing-doc floor. Render in the executor's `## Related Notes` exactly as:
> `- [Name](relpath.md) — what it is; relevance: why THIS note`.

### oc_plugins_reference_provider_plugins (12t · 12s · 11d · 4r)

- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway product whose built-in provider plugins this note catalogs; relevance: the catalog's parent product, every plugin ships inside OpenClaw.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — a pluggable model-provider backend registered via the extension SDK; relevance: the exact concept each MiniMax/Mistral/Moonshot/Novita manifest entry instantiates.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: all four plugins front LLMs and make those models callable from OpenClaw.
- [term_third_party_genai_services](../../term_dictionary/term_third_party_genai_services.md) — external third-party GenAI provider APIs; relevance: these four plugins integrate exactly such external providers into OpenClaw.
- [term_model_catalog](../../term_dictionary/term_model_catalog.md) — the registry of model/provider identifiers an agent can select; relevance: each plugin contributes its `providers:` identifiers to OpenClaw's model catalog.
- [term_multimodal](../../term_dictionary/term_multimodal.md) — model capabilities spanning image/video/audio beyond text; relevance: the Surface `contracts` (image/video/music/speech/media-understanding) are multimodal surfaces this catalog enumerates.
- [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — TTS speech synthesis; relevance: MiniMax's `speechProviders` contract is a TTS surface listed in this catalog.
- [term_realtime_transcription](../../term_dictionary/term_realtime_transcription.md) — streaming speech-to-text; relevance: Mistral's `realtimeTranscriptionProviders` contract maps directly to this term.
- [term_embedding](../../term_dictionary/term_embedding.md) — vector embeddings for semantic search/memory; relevance: Mistral's `memoryEmbeddingProviders` contract produces embeddings for memory search.
- [term_diffusion_model](../../term_dictionary/term_diffusion_model.md) — diffusion-based generative model; relevance: MiniMax's `imageGenerationProviders`/`videoGenerationProviders` are typically diffusion generators.
- [term_npm](../../term_dictionary/term_npm.md) — Node package manager / registry; relevance: distribution + install route (`@openclaw/*-provider`, "included in OpenClaw") is an npm-package fact in every Distribution H2.
- [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — the SDK plugins use to register surfaces/contracts; relevance: each provider plugin is built against and loaded by this SDK to expose its `contracts`.

- [hermes_model_provider_plugin](../hermes_agent/hermes_model_provider_plugin.md) — Hermes/OpenClaw-family doc on building a model-provider plugin; relevance: the operational counterpart of these MiniMax/Mistral/Moonshot/Novita provider-plugin manifests.
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — taxonomy of plugin surfaces/contracts; relevance: explains the `contracts:` Surface vocabulary (imageGenerationProviders, speechProviders, …) this catalog lists per plugin.
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — catalog of bundled/included plugins; relevance: direct analog — these four are "included in OpenClaw" built-in provider plugins.
- [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-generation provider-plugin doc; relevance: details the `imageGenerationProviders` contract MiniMax satisfies.
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech provider configuration; relevance: details the `speechProviders` contract MiniMax satisfies.
- [hermes_model_catalog_reference](../hermes_agent/hermes_model_catalog_reference.md) — model-catalog reference; relevance: where each plugin's `providers:` identifiers surface for selection.
- [oc_providers_minimax](oc_providers_minimax.md) *(planned, this series — pr05)* — per-provider MiniMax setup how-to; relevance: the `/providers/minimax` Related-docs target this manifest links out to.
- [oc_providers_mistral](oc_providers_mistral.md) *(planned, this series — pr05)* — per-provider Mistral setup how-to; relevance: the `/providers/mistral` Related-docs target this manifest links out to.
- [oc_providers_moonshot](oc_providers_moonshot.md) *(planned, this series — pr05)* — per-provider Moonshot/Kimi setup how-to; relevance: the `/providers/moonshot` Related-docs target this manifest links out to.
- [oc_providers_novita](oc_providers_novita.md) *(planned, this series — pr05)* — per-provider Novita setup how-to; relevance: the `/providers/novita` Related-docs target this manifest links out to.
- [oc_plugins_reference_channel_plugins](oc_plugins_reference_channel_plugins.md) *(planned, this series — pl15 sibling)* — the channel-plugin catalog; relevance: the other half of pl15's plugin-reference catalog (provider vs channel).

- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — code package implementing OpenClaw's LLM/media provider extensions; relevance: the source that implements these exact provider plugins.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework that loads and registers plugins; relevance: the loader/registrar for these provider plugins.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: bundles the "included in OpenClaw" provider plugins this catalog covers.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — the Hermes provider-adapter package; relevance: ecosystem counterpart implementing the same provider-adapter pattern these plugins use.

- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw OpenAI provider implementation; relevance: a worked example of the same provider-plugin shape MiniMax/Mistral/etc. follow.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — OpenClaw Anthropic provider implementation; relevance: another concrete provider-plugin registering a `providers:` identifier.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator provider; relevance: shows multi-model-family registration, like Novita's three `providers:` aliases.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider plugin; relevance: another provider-plugin instance illustrating the Surface contract pattern.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS provider; relevance: concrete `speechProviders` contract implementation matching MiniMax's TTS surface.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT provider; relevance: concrete transcription contract implementation matching Mistral's `realtimeTranscriptionProviders`.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — model-catalog manifest planner; relevance: shows how plugin `providers:` identifiers feed the model catalog this note enumerates.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — agent-side model catalog access; relevance: consumes the provider identifiers these plugins register.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entrypoint declarations; relevance: shows how a provider plugin's surfaces/contracts are declared to the SDK.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry implementation; relevance: the registration mechanism that ingests each plugin's `providers:` list.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-generation dispatch; relevance: routes to the `imageGenerationProviders` contract MiniMax satisfies.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — plugin manifest schema; relevance: defines the Distribution/Surface manifest structure these catalog entries summarize.

### oc_plugins_reference_channel_plugins (11t · 12s · 11d · 4r)

- [term_openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway product whose built-in channel plugins this note catalogs; relevance: the catalog's parent product, every channel plugin runs inside OpenClaw.
- [term_chatbot](../../term_dictionary/term_chatbot.md) — an automated conversational agent on a chat platform; relevance: each channel plugin runs OpenClaw as a chatbot on Teams/Nextcloud Talk/Nostr.
- [term_bot](../../term_dictionary/term_bot.md) — a bot account/identity that sends and receives messages; relevance: the bot-account model these channel plugins use (Teams "bot conversations").
- [term_slack](../../term_dictionary/term_slack.md) — the canonical chat-platform integration; relevance: the closest existing chat-channel term — Teams/Nextcloud Talk/Nostr are analogous message channels.
- [term_encryption](../../term_dictionary/term_encryption.md) — message encryption / confidentiality; relevance: Nostr's NIP-04 encrypted direct messages are an encryption surface this note describes.
- [term_websocket](../../term_dictionary/term_websocket.md) — persistent bidirectional realtime connection; relevance: chat-channel plugins maintain websocket-style realtime gateways to their platforms.
- [term_oauth](../../term_dictionary/term_oauth.md) — delegated-authorization token flow; relevance: Teams/Nextcloud channel plugins authenticate the bot account via OAuth/token flows.
- [term_npm](../../term_dictionary/term_npm.md) — Node package manager / registry; relevance: install route is `npm; ClawHub` with `@openclaw/*` package distribution in every Distribution H2.
- [term_messaging_gateway](../../term_dictionary/term_messaging_gateway.md) — the gateway that bridges chat platforms to the agent; relevance: the subsystem these channel plugins plug into to deliver/receive messages.
- [term_channel_kernel](../../term_dictionary/term_channel_kernel.md) — the core channel-abstraction layer; relevance: the contract each `channels:` plugin implements to register a platform.
- [term_socket_mode](../../term_dictionary/term_socket_mode.md) — outbound-only websocket connection mode for chat bots; relevance: the realtime-connection pattern channel plugins use to avoid inbound webhooks.

- [hermes_messaging_teams_bot](../hermes_agent/hermes_messaging_teams_bot.md) — Microsoft Teams bot messaging setup; relevance: the operational setup behind the `msteams` channel-plugin catalog entry.
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging gateway architecture; relevance: explains the channel/gateway subsystem these `channels:` plugins extend.
- [hermes_adding_platform_adapter_plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — adding a platform/channel adapter as a plugin; relevance: the build-side counterpart of these channel-plugin manifests.
- [hermes_adding_platform_adapter_builtin](../hermes_agent/hermes_adding_platform_adapter_builtin.md) — adding a built-in platform adapter; relevance: details how a channel plugin registers a `channels:` identifier.
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — channel webhook routing + security; relevance: covers the inbound/auth surface Teams/Nextcloud channel plugins rely on.
- [cc_channels_overview](../claude_code/cc_channels_overview.md) — coding-agent channels overview; relevance: cross-ecosystem analog of the chat-channel catalog this note builds.
- [oc_channels_msteams](oc_channels_msteams.md) *(planned, this series — ch04)* — per-channel Microsoft Teams setup how-to; relevance: the `/channels/msteams` Related-docs target this manifest links out to.
- [oc_channels_nextcloud_talk](oc_channels_nextcloud_talk.md) *(planned, this series — ch04)* — per-channel Nextcloud Talk setup how-to; relevance: the `/channels/nextcloud-talk` Related-docs target this manifest links out to.
- [oc_channels_nostr](oc_channels_nostr.md) *(planned, this series — ch04)* — per-channel Nostr setup how-to; relevance: the `/channels/nostr` Related-docs target this manifest links out to.
- [oc_channels_overview](oc_channels_overview.md) *(planned, this series — ch01)* — channels concept/overview; relevance: the section hub that frames these channel plugins.
- [oc_plugins_reference_provider_plugins](oc_plugins_reference_provider_plugins.md) *(planned, this series — pl15 sibling)* — the provider-plugin catalog; relevance: the other half of pl15's plugin-reference catalog (channel vs provider).

- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — code package implementing OpenClaw chat-channel plugins; relevance: the source that implements these exact channel plugins.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — the messaging-channel subsystem (text DMs / group messages); relevance: the subsystem Teams/Nextcloud Talk/Nostr text channels extend.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework that loads and registers plugins; relevance: the loader/registrar for these channel plugins.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the Hermes messaging-gateway package; relevance: ecosystem counterpart implementing the same channel-gateway pattern.

- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the OpenClaw channel-adapter contract; relevance: the interface each `channels:` plugin (msteams/nextcloud-talk/nostr) implements.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket-mode channel connection; relevance: a worked channel-plugin example of the realtime-connection pattern these plugins use.
- [snippet_openclaw_channels_discord_intents](../../code_snippets/snippet_openclaw_channels_discord_intents.md) — Discord channel intents/registration; relevance: another concrete channel-plugin registering a platform `channels:` identifier.
- [snippet_hermes_agent_plugins_platform_teams](../../code_snippets/snippet_hermes_agent_plugins_platform_teams.md) — Teams platform plugin; relevance: implementation of the `msteams` channel-plugin catalog entry.
- [snippet_hermes_agent_plugins_platform_irc](../../code_snippets/snippet_hermes_agent_plugins_platform_irc.md) — IRC platform plugin; relevance: a text-channel plugin parallel to Nextcloud Talk/Nostr conversation channels.
- [snippet_hermes_agent_plugins_platform_line](../../code_snippets/snippet_hermes_agent_plugins_platform_line.md) — LINE platform plugin; relevance: another channel-plugin instance illustrating the `channels:` registration shape.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — abstract base for platform/channel adapters; relevance: the shared base contract all channel plugins specialize.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — the channel directory/registry; relevance: where each plugin's `channels:` identifier is registered and discovered.
- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Matrix platform adapter; relevance: a conversation-channel adapter parallel to Nextcloud Talk.
- [snippet_hermes_agent_gw_platform_signal](../../code_snippets/snippet_hermes_agent_gw_platform_signal.md) — Signal platform adapter; relevance: an encrypted-DM channel adapter parallel to Nostr's NIP-04 encrypted DMs.
- [snippet_hermes_agent_gw_platform_telegram_connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram connection setup; relevance: realtime channel-connection pattern shared by these channel plugins.
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel gateway configuration; relevance: how each registered channel (msteams/nextcloud-talk/nostr) is configured and enabled.

## Undigested Terms Plan

> Per master: OpenClaw vocabulary terms are digested as `oc_` doc/catalog notes by their home sub-plan, NOT
> promoted to `term_dictionary`. The only `term_dictionary` interaction is LINKING existing terms.

| Term (from source) | Disposition |
|---|---|
| MiniMax / MiniMax Portal | Catalog entry in note 1; provider name, NOT a term note. Link `term_llm` / `term_third_party_genai_services`. |
| Mistral | Catalog entry in note 1; provider name, NOT a term note. Link `term_llm` / `term_third_party_genai_services`. |
| Moonshot (Kimi) | Catalog entry in note 1; provider name, NOT a term note. Link `term_llm`. (`term_moonshot`/`term_kimi` absent in DB — intentionally not promoted; a provider name, not cross-cutting vocab.) |
| Novita / Novita AI / Novitaai | Catalog entry in note 1; provider name, NOT a term note. Link `term_third_party_genai_services`. |
| Microsoft Teams | Catalog entry in note 2; chat-platform name, NOT a term note. Link `term_chatbot` / `term_bot`. |
| Nextcloud Talk | Catalog entry in note 2; chat-platform name, NOT a term note. Link `term_chatbot`. |
| Nostr / NIP-04 | Catalog entry in note 2; protocol/platform name, NOT a term note. Link `term_encryption` / `term_chatbot`. |
| provider plugin / channel plugin | Concept digested in the catalog notes themselves; link existing `term_provider_plugin` / `term_plugin_manifest` / `term_plugin_sdk`. |
| Surface / contract (imageGenerationProviders, speechProviders, etc.) | Described inline in note 1 as OpenClaw plugin-contract vocabulary (catalog facts); link `term_multimodal` / `term_text_to_speech` / `term_realtime_transcription` / `term_embedding`. NOT term notes. |
| install route (included in OpenClaw / npm / ClawHub) | Distribution fact in both notes; link `term_npm`. NOT a term note. |

**Expected new `term_dictionary` captures: 0.** No genuinely reusable cross-cutting term lacking an existing
note appears in these stub pages — every concept is either OpenClaw catalog vocabulary (→ `oc_` notes) or
covered by an existing term. If augment's re-scan surfaces one, it would route to
`acronym_glossary_llm.md` (provider/model vocab) or `acronym_glossary_tools.md` (plugin/channel vocab);
none is proposed here.

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes (inherited from master). All
provider/channel/contract vocabulary is digested as `oc_` catalog notes or linked to existing terms.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (2 notes, P3). The 8-gate table below is identical in structure to every OpenClaw
sub-plan; all gates must pass before commit.

| Gate | Check | Tool / Method | Pass criterion |
|------|-------|---------------|----------------|
| G1 | Format | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` | YAML field order/required fields OK; `# OpenClaw — …` H1, `## Overview`, `## Related Notes`, `## References`, bold footer present. |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/plugins/reference/<page>.md` | Every package name / provider-channel id / contract / install route traceable to source; no invented facts. |
| G3 | Density + Coverage | `wc -w` (body), fence count | ≤2500w, ≤6 code, ≤400 lines, one building_block per note; all 7 pages' sections covered (Section Coverage Map). |
| G5 | Ghost-reference detect + redirect | `/tessellum-fix-ghost-references` / DB existence re-check | 0 links to non-existent notes; planned siblings cited only where they will exist. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links` | 0 broken relative paths after incremental reindex. |
| G7 | Discoverability (outbound→inbound) | reciprocal-inlink add | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md`). |
| G8 | In-degree ≥1 (anti-island) | `note_links` query post-reindex | in_degree ≥1 for both notes. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_provider_plugins oc_plugins_reference_channel_plugins"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required H2 sections present
  for s in ${(s:|:)REQ_SECTIONS}; do grep -qF "$s" "$f" || echo "MISSING SECTION in $n: $s"; done
  # G3 density (body only, exclude YAML frontmatter)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url:' "$f" || echo "MISSING source_url: $n"; }
  # sibling-prefix cross-ref sanity (≥1 oc_ sibling or entry link)
  grep -qE "$SIBLING_PREFIX|entry_openclaw_docs" "$f" || echo "NO SIBLING/ENTRY XREF: $n"
done

# YAML frontmatter sweep for the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost-reference / DB existence re-check of EXISTING cited targets
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for id in \
  resources/term_dictionary/term_openclaw.md \
  resources/term_dictionary/term_provider_plugin.md \
  resources/term_dictionary/term_llm.md \
  resources/term_dictionary/term_third_party_genai_services.md \
  resources/term_dictionary/term_chatbot.md \
  resources/term_dictionary/term_encryption.md \
  areas/code_repos/repo_openclaw_extensions_llm_providers.md \
  areas/code_repos/repo_openclaw_channels.md \
  areas/code_repos/repo_openclaw_extensions.md ; do
  [ "$c" = 1 ] || echo "GHOST: $id"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_provider_plugins | concept | 550 | 0 | ✅ (≪2500w / 0 code) |
| 2 | oc_plugins_reference_channel_plugins | concept | 450 | 0 | ✅ (≪2500w / 0 code) |

Neither note approaches any cap. The risk on these stub pages is the OPPOSITE of over-density —
under-substance — addressed by consolidating the 7 thin manifests into 2 BB-coherent catalog notes
(see Split Decisions) rather than 7 fragments. No further split needed.

## Entry Point Decision (inherited from master)

Contributes **2 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step, `building_block:
navigation`) under the **Plugins → Reference** cluster (pl15 = "provider & channel plugin reference
catalog"). Each new note receives its entry-point back-link at finalization, satisfying G7/G8 (≥1 inbound
link from outside `documentation/openclaw/`). No standalone entry point for this sub-plan (the shared
`entry_openclaw_docs.md` indexes all 105 sub-plans). Parent-hub wiring (`entry_gen_ai_dev.md`,

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links to add for G7/G8 (DB-verify at execution):
- `entry_openclaw_docs.md` → **both** notes 1 + 2 (primary discoverability path; guarantees in-degree ≥1).
- `repo_openclaw_extensions_llm_providers.md` → note 1 (provider-plugin catalog ↔ the code that implements it).
- `repo_openclaw_channels.md` → note 2 (channel-plugin catalog ↔ the channels code package).
- `repo_openclaw_extensions.md` → notes 1 + 2 (plugin framework ↔ the plugin reference catalog).
- `term_provider_plugin.md` → note 1; `term_chatbot.md` → note 2 (term ↔ catalog of its OpenClaw instances).

anti-island floor for each note; the repo/term inlinks are reciprocal enrichment added at execution.

## Pacing Rules (inherited from master)

One execution phase; all 8 gates pass before commit. Re-read each source page at execution; reproduce
package names / identifiers / contracts verbatim (no invented facts). One building_block per note. Cap
dynamic-workflow fan-out at ~30 agents/run (trivially satisfied — 2 notes). Reindex incrementally; verify
`note_links` + 0 broken links + in-degree ≥1 before commit. `git pull --rebase --autostash` first; commit +
push the phase together; no Claude co-author trailer.

## Augmentation Report (2026-06-21)

**What was locked.** Re-read all 7 source pages under `inbox/openclaw_docs/plugins/reference/` (minimax,
mistral, moonshot, novita, msteams, nextcloud-talk, nostr) on 2026-06-21 — measured counts confirm the
plan's Source table (each 55-66 words, 0 code fences, identical 3-H2 manifest skeleton; 412w total). The
2-note consolidation (provider plugins / channel plugins) and all grounding facts (npm packages, `providers:`
/`channels:` identifiers, Surface `contracts`, install routes, `/providers/*` & `/channels/*` Related-docs
pointers) verified against source verbatim. The placeholder `## Candidate Cross-References` section was
replaced with a LOCKED `## Per-Note Related Notes Mapping` meeting raised floors (≥8 terms · ≥10 snippets ·
Terms/Docs/Repos/Snippets with a per-link relevance statement. G4 gate criterion + Summary Statistics
cross-ref line updated to the locked floors.


| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met (≥8t/≥10s/≥10d) |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_provider_plugins | 12 | 12 | 11 (6 existing + 5 planned) | 4 | ✅ all |
| oc_plugins_reference_channel_plugins | 11 | 12 | 11 (6 existing + 5 planned) | 4 | ✅ all |

cited toward the doc floor are explicitly **(planned, this series)** (pr05 providers, ch04/ch01 channels,
pl15 sibling) and confirmed-absent in DB; `entry_openclaw_docs` confirmed absent and tagged **(planned,
master W1)** — neither is counted toward the existing-doc floor (each note has 6 existing docs, ≥5 floor met).

**New-term candidates + best-fit glossary.** None. Re-scan of all 7 pages (Step 2d) surfaced no genuinely
cross-cutting, vault-reusable term lacking an existing note. Every concept is either OpenClaw catalog
vocabulary digested in the `oc_*` notes (provider/channel names, Surface contracts, install routes) or
to `acronym_glossary_llm.md` (provider/model vocab) or `acronym_glossary_tools.md` (plugin/channel vocab) —
consistent with the master's Undigested-Terms ownership decision. **Expected new term_dictionary captures: 0**
(unchanged from plan stage; Undigested Terms Plan + Term-Note Authoring Requirements (N/A — 0 new terms)
sections present and unchanged).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step ≥8 terms + raised floors | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; note 1 = 12t/12s/11d/4r, note 2 = 11t/12s/11d/4r; each link is an indexed `[Name](relpath.md) — desc; relevance: …`. Both exceed ≥8 terms · ≥10 snippets · ≥10 docs. |
| CP2 | 9-GATE present (G1-G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present; single execution phase; G1 format, G2 grounding, G3 density+coverage, G4 cross-ref (raised-floor criterion), G5 ghost-detect, G6 broken-link, G7/G8 discoverability/in-degree. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at master W1) | **PASS** | `## Entry Point Decision` inherits master: contributes 2 rows to `entry_openclaw_docs.md` (created master W1 pre-step, `building_block: navigation`) under Plugins → Reference; each note gets entry back-link (G7/G8). DB-confirmed `entry_openclaw_docs.md` absent now → correctly cited (planned, master W1), not as existing. |
| CP4 | Size (≤30 or split) | **PASS** | 2 planned notes (consolidated from 7 stub pages); far ≤30. |
| CP5 | Format derived from existing target-dir notes | **PASS** | Format inherited from master Format Definition, derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) corpora; YAML field order + `## Overview`/`## Related Notes`/`## References` + bold footer; verified against existing `resources/documentation/` notes. |
| CP6 | Density (borderline → split) | **PASS** | `## Density Re-Assessment`: note 1 ~550w/0 code, note 2 ~450w/0 code; both ≪2500w/≤6 code caps. Risk is under-substance, addressed by consolidation; no further split needed. |
| CP7 | Sources measured (not guessed) | **PASS** | All 7 source pages re-read 2026-06-21; measured 55-66w each / 412w total / 0 code fences — matches Source table within ±0%. No under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (10 rows, all dispositioned to catalog-entry or existing-term link, 0 promotions); `## Term-Note Authoring Requirements` present (N/A — 0 new terms, per master ownership rule). Expected new captures: 0. |

**RESULT: 9/9 (incl. CP8f) PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (Related Notes locked at raised floors; 0 new terms) |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21** (9/9 checkpoints PASS) |
| 4. Execute | `/tessellum-execute-digestion-plan` | ⏳ pending |
