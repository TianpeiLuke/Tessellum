---
title: Sub-Plan pl22 — OpenClaw Docs: Plugins (Reference vydra → xiaomi)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/vydra", "plugins/reference/web-readability", "plugins/reference/webhooks", "plugins/reference/whatsapp", "plugins/reference/workboard", "plugins/reference/xai", "plugins/reference/xiaomi"]
---

# Sub-Plan pl22: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_*` prefix), format, dedup, 9-GATE, cross-refs, and entry-point wiring are inherited verbatim from the master; this file locks the per-page measurements, planned notes, coverage map, and candidate cross-references for the 7 assigned plugin-reference pages.

## Scope

The 7 plugin-reference pages `plugins/reference/vydra` through `plugins/reference/xiaomi` (alphabetical tail of the plugin reference index). Each is a one-screen plugin "data sheet": a one-line summary, a Distribution block (npm package + install route), a Surface block (the providers/channels/contracts the plugin registers), and a Related docs pointer. Three are **model-provider plugins** (vydra, xai, xiaomi — media/speech/image/video/web-search providers), one is a **channel plugin** (whatsapp), one is a **content-extractor plugin** (web-readability), one is an **automation plugin** (webhooks → TaskFlows), and one is a **dashboard/tool plugin** (workboard). Priority **P3 (Phase C)** — plugin-reference sprawl, digested after the conceptual/operational core. The code-side `repo_openclaw_extensions*` / `repo_openclaw_channels*` notes are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **409 measured words total** (all stubs, 54–63 words each, 0 code fences). **Planned: 7 notes (1 per page; no splits).**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| vydra | /plugins/reference/vydra | 58 | 0 | 3 | 0 | concept (provider plugin data sheet) |
| web-readability | /plugins/reference/web-readability | 57 | 0 | 2 | 0 | concept (content-extractor plugin) |
| webhooks | /plugins/reference/webhooks | 59 | 0 | 3 | 0 | concept (automation plugin) |
| whatsapp | /plugins/reference/whatsapp | 56 | 0 | 3 | 0 | concept (channel plugin) |
| workboard | /plugins/reference/workboard | 54 | 0 | 3 | 0 | concept (dashboard/tool plugin) |
| xai | /plugins/reference/xai | 62 | 0 | 3 | 0 | concept (provider plugin) |
| xiaomi | /plugins/reference/xiaomi | 63 | 0 | 3 | 0 | concept (provider plugin) |

H2 set per page: `## Distribution`, `## Surface`, and (all except web-readability) `## Related docs`. No H3 on any page. No code fences. The page frontmatter exposes `summary` and `read_when` (an install/configure/audit cue) — both folded into each note's Overview, not copied as YAML.

## Content Strategy

- **Prioritize**: the Distribution (package id + install route) and Surface (registered providers/channels/contracts) facts — these are the load-bearing, queryable content of a plugin reference. Fold the `summary` + `read_when` frontmatter into a 1–2 sentence Overview.
- **Split**: none. Every page is a 54–63-word stub far below the 2,500-word / 6-code-block caps; one BB (concept) each. Splitting a 60-word page would violate atomicity in the other direction.
- **No merge**: do NOT consolidate the 7 stubs into one "misc plugins" note — each plugin is a distinct, independently-addressable reference object (distinct npm package, distinct Surface), and the master assigns 1 note per plugin page across pl05–pl23. Keep 1:1.
- **Link-out, do not redefine**: the model-provider plugins (vydra/xai/xiaomi) point at their `/providers/*` doc (digested under pr09); whatsapp points at `/channels/whatsapp` (ch06); webhooks/workboard point at their full `/plugins/*` how-to page (pl25). Reference these as siblings/planned, never duplicate the provider/channel/how-to content here. Each note links the existing `term_openclaw`, `term_provider_plugin`/`term_plugin_manifest`/`term_plugin_sdk`, and the relevant `repo_openclaw_extensions*` / `repo_openclaw_channels*` code note.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_vydra.md` | concept | vydra.md: Distribution, Surface, Related docs | 220 | The Vydra model-provider plugin (`@openclaw/vydra-provider`, bundled): adds Vydra image-generation, speech, and video-generation provider support to OpenClaw via the `imageGenerationProviders`/`speechProviders`/`videoGenerationProviders` contracts. |
| 2 | `oc_plugins_reference_web_readability.md` | concept | web-readability.md: Distribution, Surface | 200 | The Web Readability plugin (`@openclaw/web-readability-plugin`, bundled): extracts readable article content from local HTML web-fetch responses via the `webContentExtractors` contract. |
| 3 | `oc_plugins_reference_webhooks.md` | concept | webhooks.md: Distribution, Surface, Related docs | 220 | The Webhooks plugin (`@openclaw/webhooks`, bundled): exposes authenticated inbound webhooks that bind external automation to OpenClaw TaskFlows; registers as a plugin surface. |
| 4 | `oc_plugins_reference_whatsapp.md` | concept | whatsapp.md: Distribution, Surface, Related docs | 220 | The WhatsApp channel plugin (`@openclaw/whatsapp`, ClawHub `clawhub:@openclaw/whatsapp` or npm): adds the `whatsapp` channel for WhatsApp Web chats. |
| 5 | `oc_plugins_reference_workboard.md` | concept | workboard.md: Distribution, Surface, Related docs | 200 | The Workboard plugin (`@openclaw/workboard`, bundled): a dashboard workboard for agent-owned issues and sessions; registers via the `tools` contract. |
| 6 | `oc_plugins_reference_xai.md` | concept | xai.md: Distribution, Surface, Related docs | 240 | The xAI model-provider plugin (`@openclaw/xai-plugin`, bundled): adds xAI (Grok) provider support across image-generation, media-understanding, realtime-transcription, speech, tools, video-generation, and web-search contracts. |
| 7 | `oc_plugins_reference_xiaomi.md` | concept | xiaomi.md: Distribution, Surface, Related docs | 220 | The Xiaomi model-provider plugin (`@openclaw/xiaomi-provider`, bundled): adds the `xiaomi` and `xiaomi-token-plan` providers (speech-provider contract) to OpenClaw. |

Filename rule applied: `oc_` + full slug with `/` and `-` → `_` (e.g. `plugins/reference/web-readability` → `oc_plugins_reference_web_readability.md`).

## Section Coverage Map

Every source page and every H2 maps to exactly one planned note; no orphans. (No H3 anywhere; no code fences.)

```
plugins/reference/vydra.md
├── (lead summary line) ─────────────── → note 1 (oc_plugins_reference_vydra) Overview
├── ## Distribution ─────────────────── → note 1 (package + install route)
├── ## Surface ──────────────────────── → note 1 (providers: vydra; contracts: image/speech/video)
└── ## Related docs (→ /providers/vydra) → note 1 References (link-out, pr09 sibling)
plugins/reference/web-readability.md
├── (lead summary line) ─────────────── → note 2 (oc_plugins_reference_web_readability) Overview
├── ## Distribution ─────────────────── → note 2
└── ## Surface ──────────────────────── → note 2 (contracts: webContentExtractors)
plugins/reference/webhooks.md
├── (lead summary line) ─────────────── → note 3 (oc_plugins_reference_webhooks) Overview
├── ## Distribution ─────────────────── → note 3
├── ## Surface ──────────────────────── → note 3 (plugin)
└── ## Related docs (→ /plugins/webhooks) → note 3 References (link-out, pl25 sibling)
plugins/reference/whatsapp.md
├── (lead summary line) ─────────────── → note 4 (oc_plugins_reference_whatsapp) Overview
├── ## Distribution ─────────────────── → note 4 (ClawHub + npm route)
├── ## Surface ──────────────────────── → note 4 (channels: whatsapp)
└── ## Related docs (→ /channels/whatsapp) → note 4 References (link-out, ch06 sibling)
plugins/reference/workboard.md
├── (lead summary line) ─────────────── → note 5 (oc_plugins_reference_workboard) Overview
├── ## Distribution ─────────────────── → note 5
├── ## Surface ──────────────────────── → note 5 (contracts: tools)
└── ## Related docs (→ /plugins/workboard) → note 5 References (link-out, pl25 sibling)
plugins/reference/xai.md
├── (lead summary line) ─────────────── → note 6 (oc_plugins_reference_xai) Overview
├── ## Distribution ─────────────────── → note 6
├── ## Surface ──────────────────────── → note 6 (providers: xai; 7 contracts)
└── ## Related docs (→ /providers/xai) ── → note 6 References (link-out, pr09 sibling)
plugins/reference/xiaomi.md
├── (lead summary line) ─────────────── → note 7 (oc_plugins_reference_xiaomi) Overview
├── ## Distribution ─────────────────── → note 7
├── ## Surface ──────────────────────── → note 7 (providers: xiaomi, xiaomi-token-plan; speech)
└── ## Related docs (→ /providers/xiaomi) → note 7 References (link-out, pr09 sibling)
```

No orphaned sections. `/providers/*`, `/channels/whatsapp`, and `/plugins/{webhooks,workboard}` targets are linked (siblings in pr09 / ch06 / pl25), not duplicated here.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are 54–63-word, 0-code stubs with one BB (concept) each — far below the 2,500-word / 6-code-block caps. No page qualifies for a split; merging is also rejected (each plugin is a distinct addressable reference object). 1 page → 1 note. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (409 words total; mean ~58 w/page). New `oc_*` notes: **7**. New `term_dictionary` notes: **0**.
- BB distribution: concept ×7 (all are plugin reference data sheets — what the plugin is, its package, and what surface it registers; no procedure/model/argument).
- Est. digest words: ~1,520 (avg ~217/note). Each note 200–240 words — well under the 2,500-word cap. 0 source code fences → 0 code blocks per note (each ≤6 cap trivially satisfied).
- Sub-page typing: notes 1, 6, 7 = model-provider plugins; note 4 = channel plugin; notes 2, 5 = contract/tool plugins; note 3 = automation plugin.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


Relative paths are FROM a note at `resources/documentation/openclaw/oc_X.md`: terms `../../term_dictionary/term_Y.md`; sibling oc docs `oc_Y.md`; cross-folder docs `../<folder>/<file>.md`; snippets `../../code_snippets/snippet_Y.md`; repos `../../../areas/code_repos/repo_Y.md`; entry points `../../../0_entry_points/entry_Y.md`.

### oc_plugins_reference_vydra (8t · 12s · 11d)

Source: vydra.md — `@openclaw/vydra-provider` (bundled); providers: vydra; contracts: imageGenerationProviders, speechProviders, videoGenerationProviders.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway/product this plugin extends; relevance: every oc_* note links the parent product the plugin plugs into.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model-provider backend pattern; relevance: Vydra IS a provider plugin — the exact concept it instantiates.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — a plugin's package + contracts declaration; relevance: Vydra's Distribution + Surface blocks ARE its manifest.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external generative-AI backends integrated into a platform; relevance: Vydra is an external GenAI media/speech provider.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthetic voice generation; relevance: Vydra's `speechProviders` contract supplies TTS voices.
- [Video Processing](../../term_dictionary/term_video_processing.md) — video media generation/handling (closest existing term; no `term_video_generation`); relevance: maps to Vydra's `videoGenerationProviders` contract.
- [Multimodal](../../term_dictionary/term_multimodal.md) — models spanning image/audio/video; relevance: Vydra's image+speech+video surface is multimodal media generation.
- [Diffusion Model](../../term_dictionary/term_diffusion_model.md) — the generative architecture behind image/video synthesis; relevance: Vydra's `imageGenerationProviders`/`videoGenerationProviders` are diffusion-class backends.
- [GenAI](../../term_dictionary/term_genai.md) — generative AI umbrella; relevance: Vydra is a generative media provider plugged into the agent stack.
- [LLM](../../term_dictionary/term_llm.md) — the model layer fronted by providers; relevance: the provider sits behind OpenClaw's model/provider layer.

**Docs**
- [Hermes Image-Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — sibling-stack image-generation provider plugin doc; relevance: directly mirrors Vydra's `imageGenerationProviders` surface in the Hermes fork.
- [Hermes Video-Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — sibling video-generation provider plugin; relevance: same `videoGenerationProviders` contract Vydra registers.
- [Hermes TTS Providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech provider catalog; relevance: explains the `speechProviders` surface Vydra contributes to.
- [Hermes Model-Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — the model-provider plugin contract in the sibling stack; relevance: the generic shape of a provider plugin like Vydra.
- [Hermes Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference-provider catalog; relevance: situates a third-party media provider among cloud providers.
- [PI Custom Provider Registration](../pi/pi_custom_provider_registration.md) — how a provider is registered in a related coding-agent; relevance: cross-product analogue of how Vydra registers its providers.
- [oc_plugins_reference_xai](oc_plugins_reference_xai.md) (planned, this series) — sibling media-capable provider plugin; relevance: broadest provider surface in this sub-plan, same provider-plugin family.
- [oc_plugins_reference_xiaomi](oc_plugins_reference_xiaomi.md) (planned, this series) — sibling speech-provider plugin; relevance: another `speechProviders` provider plugin.
- [oc_providers_vydra](oc_providers_vydra.md) (planned, this series — pr09) — the full Vydra provider doc this reference points at via Related docs; relevance: the Related-docs link-out target.
- [oc_plugins_sdk_provider_plugins](oc_plugins_sdk_provider_plugins.md) (planned, this series — pl24) — how provider plugins are built via the SDK; relevance: the authoring counterpart of this reference data sheet.
- [oc_plugins_reference_index](oc_plugins_reference_index.md) (planned, this series — pl05) — the plugin reference index this page is a leaf of; relevance: parent reference index.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the code package registering model-provider plugins; relevance: where Vydra's provider registration lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: hosts provider plugins like Vydra.

**Snippets**
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — a provider plugin that aggregates upstream providers; relevance: concrete provider-plugin registration pattern Vydra follows.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — the OpenAI provider plugin impl; relevance: canonical model-provider plugin shape.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — the Anthropic provider plugin; relevance: another provider-plugin registration example.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — a `speechProviders` TTS provider impl; relevance: the exact speech-contract Vydra registers.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — a local TTS provider; relevance: another speech-provider contract implementation.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-generation tool wiring; relevance: consumer side of Vydra's `imageGenerationProviders`.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen provider dispatch; relevance: how an image-gen provider plugin is dispatched.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-generation tool wiring; relevance: consumer side of Vydra's `videoGenerationProviders`.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen provider dispatch; relevance: dispatch path for a video-gen provider like Vydra.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — the provider registry; relevance: where a provider plugin like Vydra is registered.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: provider-plugin initialization path.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the SDK entry shape a bundled provider plugin exposes.

### oc_plugins_reference_web_readability (8t · 11s · 11d)

Source: web-readability.md — `@openclaw/web-readability-plugin` (bundled); contracts: webContentExtractors. (No `## Related docs`.)

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — parent product; relevance: the gateway this content-extractor plugin extends.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable-backend pattern; relevance: web-readability registers into the `webContentExtractors` contract, the same provider-plugin model.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + contracts declaration; relevance: Distribution + Surface form this plugin's manifest.
- [NPM](../../term_dictionary/term_npm.md) — the Node package registry; relevance: distributed as `@openclaw/web-readability-plugin`, an npm package.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool/contract invocation by the agent; relevance: content extraction is invoked as a contract during the web-fetch tool flow.
- [LLM](../../term_dictionary/term_llm.md) — the agent's model; relevance: extracted readable article text feeds the model's context (the point of the plugin).
- [Browser Automation](../../term_dictionary/term_browser_automation.md) — programmatic page fetch/render; relevance: the plugin processes HTML from local web-fetch/browser responses.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — contract/hook binding pattern; relevance: closest existing term for the contract surface a content-extractor binds into.
- [Tool Gateway](../../term_dictionary/term_tool_gateway.md) — the tool-routing layer; relevance: the web-fetch tool that invokes the extractor routes through the tool gateway.
- [Multimodal](../../term_dictionary/term_multimodal.md) — handling diverse content types; relevance: extracted article content is one of the content types the agent ingests alongside media.

**Docs**
- [Hermes Web Search + Extract](../hermes_agent/hermes_web_search_extract.md) — web search and content extraction in the sibling stack; relevance: directly parallels web-readability's article-extraction purpose.
- [Hermes Web-Search Provider Plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — a contract-provider plugin for web content; relevance: same provider-plugin-into-contract shape as this extractor.
- [Hermes Tools Reference: Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — media/content tool reference; relevance: documents the web/media tools that feed extractors.
- [CC Chrome Browser Automation](../claude_code/cc_chrome_browser_automation.md) — browser/page-fetch automation; relevance: the local-HTML source web-readability extracts from.
- [CC Built-in Tools](../claude_code/cc_built_in_tools.md) — built-in tool catalog (web-fetch); relevance: the web-fetch tool whose responses the extractor processes.
- [CC Web Quickstart](../claude_code/cc_web_quickstart.md) — web tooling quickstart; relevance: cross-product analogue of fetching+reading web content.
- [Hermes Tool Gateway](../hermes_agent/hermes_tool_gateway.md) — the tool routing/gateway layer; relevance: where the web-fetch + extractor contract is dispatched.
- [oc_tools_web_fetch](oc_tools_web_fetch.md) (planned, this series — to08) — the web-fetch tool doc; relevance: the tool whose HTML responses this extractor reads.
- [oc_plugins_tool_plugins](oc_plugins_tool_plugins.md) (planned, this series — pl25) — how contract/tool plugins are authored; relevance: the authoring counterpart of this contract-plugin reference.
- [oc_plugins_sdk_overview](oc_plugins_sdk_overview.md) (planned, this series — pl24) — the plugin SDK overview; relevance: how a `webContentExtractors` contract plugin is built.
- [oc_plugins_reference_index](oc_plugins_reference_index.md) (planned, this series — pl05) — the plugin reference index; relevance: parent reference index this leaf belongs to.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework; relevance: registers contract plugins like this content extractor.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — web/control-UI surfaces; relevance: surfaces that fetch web content the extractor reads.

**Snippets**
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web tool implementations; relevance: the web-fetch tool whose output feeds the extractor.
- [snippet_hermes_agent_tools_browser_navigate](../../code_snippets/snippet_hermes_agent_tools_browser_navigate.md) — browser navigation tool; relevance: source of local HTML the extractor parses.
- [snippet_hermes_agent_tools_browser_session](../../code_snippets/snippet_hermes_agent_tools_browser_session.md) — browser session management; relevance: the session that produces HTML responses for extraction.
- [snippet_hermes_agent_plugins_browser_dispatch](../../code_snippets/snippet_hermes_agent_plugins_browser_dispatch.md) — browser plugin dispatch; relevance: the dispatch path a content-extractor contract participates in.
- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — a web plugin impl; relevance: concrete web/content plugin registration pattern.
- [snippet_brp_agent_tools_crawl](../../code_snippets/snippet_brp_agent_tools_crawl.md) — a crawl/fetch tool; relevance: fetching the page content the extractor then makes readable.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — handling untrusted external content; relevance: the security wrapper around web content the extractor processes.
- [snippet_hermes_agent_optional_skills_web_dev_page_agent](../../code_snippets/snippet_hermes_agent_optional_skills_web_dev_page_agent.md) — a page-reading agent skill; relevance: consumer of extracted readable page content.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — the agent tool catalog; relevance: where the web-fetch tool + extractor contract are listed.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package + contract wiring; relevance: how a contract plugin like webContentExtractors is declared.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the SDK entry shape this bundled plugin exposes.

### oc_plugins_reference_webhooks (8t · 11s · 11d)

Source: webhooks.md — `@openclaw/webhooks` (bundled); Surface: plugin; Related docs → /plugins/webhooks.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — parent product; relevance: the gateway this plugin adds inbound webhooks to.
- [Webhook](../../term_dictionary/term_webhook.md) — authenticated inbound HTTP callbacks; relevance: the plugin's entire purpose IS webhooks.
- [Automation](../../term_dictionary/term_automation.md) — programmatic triggering of workflows; relevance: webhooks bind external automation to OpenClaw TaskFlows.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable runtime surface; relevance: webhooks register as a plugin surface in the runtime.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + Surface declaration; relevance: Distribution + Surface form the plugin's manifest.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — inbound HTTP endpoint front; relevance: webhook endpoints are authenticated inbound HTTP fronting TaskFlows.
- [Cron](../../term_dictionary/term_cron.md) — scheduled-trigger automation; relevance: webhooks are the event-triggered sibling of cron-scheduled automation (both feed TaskFlows).
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — inbound-event trigger model; relevance: webhooks are the canonical inbound-event mechanism.
- [Agent Lifecycle Event](../../term_dictionary/term_agent_lifecycle_event.md) — events that drive agent runs; relevance: a webhook is an external event that kicks off an agent TaskFlow.
- [Silence Token](../../term_dictionary/term_silence_token.md) — gateway inbound-event suppression control; relevance: an inbound-routing control on the same event surface webhooks feed.

**Docs**
- [Hermes Webhooks Routing + Delivery](../hermes_agent/hermes_webhooks_routing_delivery.md) — inbound webhook routing/delivery in the sibling stack; relevance: directly parallels the webhooks plugin's inbound-HTTP-to-TaskFlow binding.
- [Hermes Automation Blueprints: Event](../hermes_agent/hermes_automation_blueprints_event.md) — event-triggered automation blueprints; relevance: the automation surface webhooks trigger.
- [Hermes Automation Blueprints: Scheduled](../hermes_agent/hermes_automation_blueprints_scheduled.md) — scheduled automation blueprints; relevance: the cron sibling of webhook-triggered automation.
- [Hermes Guide: GitHub PR Review Webhook](../hermes_agent/hermes_guide_github_pr_review_webhook.md) — a concrete inbound-webhook integration; relevance: worked example of binding external automation via webhook.
- [Hermes Cron Internals](../hermes_agent/hermes_cron_internals.md) — scheduled-trigger internals; relevance: the cron-trigger counterpart to webhook event-triggers.
- [CC Routine Triggers](../claude_code/cc_routine_triggers.md) — schedule/event triggers in a related agent; relevance: cross-product analogue of webhook/cron automation triggers.
- [Hermes Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — gateway request handling; relevance: where inbound webhook HTTP is received/authenticated.
- [oc_plugins_webhooks](oc_plugins_webhooks.md) (planned, this series — pl25) — the full webhooks how-to this reference points at via Related docs; relevance: the Related-docs link-out target.
- [oc_automation_taskflow](oc_automation_taskflow.md) (planned, this series — au01) — the TaskFlow automation doc; relevance: what webhooks bind to.
- [oc_automation_hooks](oc_automation_hooks.md) (planned, this series — au01) — automation hooks; relevance: the broader event-hook automation surface webhooks belong to.
- [oc_plugins_reference_index](oc_plugins_reference_index.md) (planned, this series — pl05) — the plugin reference index; relevance: parent reference index this leaf belongs to.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework; relevance: hosts plugin surfaces like webhooks.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway exposing/authenticating inbound HTTP; relevance: where webhook endpoints land.

**Snippets**
- [snippet_hermes_agent_gw_platform_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_webhook.md) — inbound webhook gateway adapter; relevance: the direct code-level analogue of the webhooks plugin.
- [snippet_hermes_agent_gw_platform_msgraph_webhook](../../code_snippets/snippet_hermes_agent_gw_platform_msgraph_webhook.md) — an MS Graph webhook receiver; relevance: concrete authenticated inbound-webhook handler.
- [snippet_hermes_agent_skills_devops_webhook](../../code_snippets/snippet_hermes_agent_skills_devops_webhook.md) — a webhook-driven devops skill; relevance: external automation bound to an agent via webhook.
- [snippet_hermes_agent_gw_platform_wecom_callback](../../code_snippets/snippet_hermes_agent_gw_platform_wecom_callback.md) — an inbound callback handler; relevance: authenticated inbound-HTTP callback pattern like webhooks.
- [snippet_openclaw_voice_call_webhook_signature_verify](../../code_snippets/snippet_openclaw_voice_call_webhook_signature_verify.md) — webhook signature verification; relevance: the authentication step that makes webhooks "authenticated inbound".
- [snippet_openclaw_voice_call_webhook_replay_cache](../../code_snippets/snippet_openclaw_voice_call_webhook_replay_cache.md) — webhook replay protection; relevance: inbound-webhook security hardening.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — HTTP plugin route registration; relevance: how a plugin (like webhooks) exposes inbound HTTP routes.
- [snippet_hermes_agent_gw_platform_api_server_routes](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_routes.md) — gateway API server routes; relevance: where inbound webhook routes are registered.
- [snippet_hermes_agent_gw_platform_api_server_middleware](../../code_snippets/snippet_hermes_agent_gw_platform_api_server_middleware.md) — API server auth middleware; relevance: the auth layer fronting inbound webhook endpoints.
- [snippet_hermes_agent_gw_hooks](../../code_snippets/snippet_hermes_agent_gw_hooks.md) — gateway hook registration; relevance: the hook/event surface webhooks plug into.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the SDK entry shape this bundled plugin exposes.

### oc_plugins_reference_whatsapp (8t · 11s · 11d)

Source: whatsapp.md — `@openclaw/whatsapp` (ClawHub `clawhub:@openclaw/whatsapp` or npm); channels: whatsapp; Related docs → /channels/whatsapp.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — parent product; relevance: the gateway this WhatsApp channel plugin extends.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable-backend registration model; relevance: channel plugins follow the same plugin-registration model (the `channels` Surface entry).
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + Surface declaration; relevance: Distribution (ClawHub + npm) + Surface form the manifest.
- [NPM](../../term_dictionary/term_npm.md) — Node package registry; relevance: one of the two install routes is npm (the other is ClawHub).
- [WebSocket](../../term_dictionary/term_websocket.md) — persistent bidirectional connection; relevance: the WhatsApp Web channel maintains a persistent socket for inbound/outbound messages.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — the multi-platform chat gateway layer; relevance: WhatsApp is one channel registered into the messaging gateway.
- [Event-Driven Architecture](../../term_dictionary/term_event_driven_architecture.md) — message-as-event routing; relevance: inbound WhatsApp messages are events routed by the channel layer.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — the core channel-routing engine; relevance: the kernel that the WhatsApp channel plugin registers into.
- [Slack](../../term_dictionary/term_slack.md) — a sibling chat channel; relevance: same channel-plugin shape as WhatsApp, a peer messaging channel.

**Docs**
- [Hermes Messaging: WhatsApp (Baileys)](../hermes_agent/hermes_messaging_whatsapp_baileys.md) — the WhatsApp Web channel via Baileys in the sibling stack; relevance: the exact `whatsapp` channel this plugin adds (WhatsApp Web).
- [Hermes Messaging: WhatsApp Cloud Model](../hermes_agent/hermes_messaging_whatsapp_cloud_model.md) — the alternative WhatsApp Cloud API channel; relevance: the other WhatsApp integration model, contrasts with this Web-chat plugin.
- [Hermes Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — multi-channel gateway architecture; relevance: where the WhatsApp channel plugin registers.
- [Hermes Messaging: Slack](../hermes_agent/hermes_messaging_slack.md) — a sibling channel integration; relevance: peer channel-plugin pattern WhatsApp follows.
- [Hermes Adding Platform-Adapter Plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — how a channel/platform adapter plugin is added; relevance: the authoring shape of a channel plugin like WhatsApp.
- [CC Channels Setup](../claude_code/cc_channels_setup.md) — channel configuration in a related agent; relevance: cross-product analogue of registering a chat channel.
- [Band WebSocket Agent Channels](../band/band_websocket_agent_channels.md) — websocket-based agent channels; relevance: the persistent-socket channel pattern the WhatsApp Web channel uses.
- [oc_channels_whatsapp](oc_channels_whatsapp.md) (planned, this series — ch06) — the full WhatsApp channel doc this reference points at via Related docs; relevance: the Related-docs link-out target.
- [oc_plugins_sdk_channel_plugins](oc_plugins_sdk_channel_plugins.md) (planned, this series — pl24) — how channel plugins are built via the SDK; relevance: the authoring counterpart of this channel-plugin reference.
- [oc_concepts_channel_docking](oc_concepts_channel_docking.md) (planned, this series — co01) — the channel-docking concept; relevance: the conceptual model for how a channel plugin docks into the gateway.
- [oc_plugins_reference_index](oc_plugins_reference_index.md) (planned, this series — pl05) — the plugin reference index; relevance: parent reference index this leaf belongs to.

**Repos**
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — the messaging-channel code package; relevance: implements chat channels like WhatsApp.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel framework; relevance: registers channel plugins like WhatsApp.

**Snippets**
- [snippet_hermes_agent_gw_platform_whatsapp](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp.md) — the WhatsApp platform adapter; relevance: the direct code-level analogue of this WhatsApp channel plugin.
- [snippet_hermes_agent_gw_platform_whatsapp_connect](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_connect.md) — WhatsApp Web connection setup; relevance: how the persistent WhatsApp Web channel connects.
- [snippet_hermes_agent_gw_platform_whatsapp_dispatch](../../code_snippets/snippet_hermes_agent_gw_platform_whatsapp_dispatch.md) — WhatsApp message dispatch; relevance: inbound/outbound message routing for the WhatsApp channel.
- [snippet_hermes_agent_gw_whatsapp_identity](../../code_snippets/snippet_hermes_agent_gw_whatsapp_identity.md) — WhatsApp identity/pairing; relevance: the pairing/identity step the WhatsApp channel plugin performs.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — a socket-mode channel connection; relevance: the persistent-socket channel pattern WhatsApp Web uses.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — channel conversation resolution; relevance: how the channel layer maps inbound WhatsApp chats to sessions.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: where the `whatsapp` channel id is registered/normalized.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — chat-type session typing; relevance: how a WhatsApp chat becomes a typed session.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — gateway node session wiring; relevance: the session a channel plugin's inbound message lands in.
- [snippet_slipbot_socket_mode_connection](../../code_snippets/snippet_slipbot_socket_mode_connection.md) — a socket-mode connection impl; relevance: persistent-connection channel pattern analogous to WhatsApp Web.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the SDK entry shape this channel plugin exposes.

### oc_plugins_reference_workboard (8t · 11s · 11d)

Source: workboard.md — `@openclaw/workboard` (bundled); contracts: tools; Related docs → /plugins/workboard.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — parent product; relevance: the gateway this dashboard/tool plugin extends.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable-backend pattern; relevance: workboard registers via the `tools` contract, the same plugin model.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + Surface declaration; relevance: Distribution + Surface form the manifest.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — the catalog of agent-callable tools; relevance: workboard registers into the `tools` contract, i.e. the tool registry.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool invocation; relevance: workboard exposes tool(s) the agent invokes to manage its issues/sessions.
- [Automation](../../term_dictionary/term_automation.md) — ops/workflow automation; relevance: a dashboard for agent-owned issues/sessions is an automation/ops surface.
- [Kanban](../../term_dictionary/term_kanban.md) — board-based work tracking; relevance: a workboard is a kanban-style board for agent-owned issues.
- [Kanban Multi-Agent](../../term_dictionary/term_kanban_multi_agent.md) — multi-agent board coordination; relevance: workboard tracks issues/sessions across agent-owned work.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — the schema describing a registered tool; relevance: workboard's `tools` contract entries are tool descriptors.
- [LLM](../../term_dictionary/term_llm.md) — the agent driving the tools; relevance: the agent (LLM) calls workboard tools to manage its own issues/sessions.

**Docs**
- [Hermes Kanban Dashboard CLI](../hermes_agent/hermes_kanban_dashboard_cli.md) — the kanban/workboard dashboard in the sibling stack; relevance: directly parallels workboard's dashboard-for-agent-issues purpose.
- [Hermes Kanban Multi-Agent Board](../hermes_agent/hermes_kanban_multi_agent_board.md) — multi-agent issue board; relevance: the agent-owned-issues board model workboard implements.
- [Hermes Kanban Worker Lanes](../hermes_agent/hermes_kanban_worker_lanes.md) — worker/session lanes on the board; relevance: the agent-session tracking workboard provides.
- [Hermes Kanban Tutorial Walkthrough](../hermes_agent/hermes_kanban_tutorial_walkthrough.md) — a board walkthrough; relevance: worked example of an agent-issue dashboard like workboard.
- [Hermes Dashboard Plugins](../hermes_agent/hermes_dashboard_plugins.md) — dashboard plugin surface; relevance: the dashboard-plugin model workboard registers into.
- [Hermes Dashboard Extension API](../hermes_agent/hermes_dashboard_extension_api.md) — the dashboard extension API; relevance: how a dashboard/tool plugin like workboard extends the UI.
- [Hermes Tools Reference: Core](../hermes_agent/hermes_tools_reference_core.md) — core tool catalog; relevance: the `tools` contract workboard registers into.
- [oc_plugins_workboard](oc_plugins_workboard.md) (planned, this series — pl25) — the full workboard how-to this reference points at via Related docs; relevance: the Related-docs link-out target.
- [oc_plugins_tool_plugins](oc_plugins_tool_plugins.md) (planned, this series — pl25) — how tool plugins are authored; relevance: the authoring counterpart of this `tools`-contract reference.
- [oc_web_dashboard](oc_web_dashboard.md) (planned, this series — wb01) — the web dashboard doc; relevance: the dashboard surface that renders the workboard.
- [oc_plugins_reference_index](oc_plugins_reference_index.md) (planned, this series — pl05) — the plugin reference index; relevance: parent reference index this leaf belongs to.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension framework; relevance: hosts tool plugins like workboard.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — the dashboard/web surfaces; relevance: where the workboard dashboard is rendered.

**Snippets**
- [snippet_hermes_agent_plugins_kanban](../../code_snippets/snippet_hermes_agent_plugins_kanban.md) — the kanban/workboard plugin impl; relevance: the direct code-level analogue of the workboard plugin.
- [snippet_hermes_agent_plugins_example_dashboard](../../code_snippets/snippet_hermes_agent_plugins_example_dashboard.md) — an example dashboard plugin; relevance: the dashboard-plugin pattern workboard follows.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — the tool-descriptor contract; relevance: how workboard's `tools` contract entries are described.
- [snippet_hermes_agent_plugins_hermes_achievements](../../code_snippets/snippet_hermes_agent_plugins_hermes_achievements.md) — a tool/dashboard plugin example; relevance: another `tools`-contract plugin registration pattern.
- [snippet_hermes_agent_plugins_spotify](../../code_snippets/snippet_hermes_agent_plugins_spotify.md) — a tool plugin registering tools; relevance: concrete `tools`-contract plugin shape.
- [snippet_hermes_agent_plugins_disk_cleanup](../../code_snippets/snippet_hermes_agent_plugins_disk_cleanup.md) — a tool plugin; relevance: tool-contract plugin registration example.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — the agent tool catalog; relevance: where workboard's tools land for the agent to call.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway server methods; relevance: the server-side methods a dashboard/tool plugin exposes.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — agent task/issue planner; relevance: the issue/session planning workboard surfaces.
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — tool registration; relevance: how a tool plugin like workboard registers its tools.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the SDK entry shape this bundled plugin exposes.

### oc_plugins_reference_xai (9t · 12s · 12d)

Source: xai.md — `@openclaw/xai-plugin` (bundled); providers: xai; contracts: imageGenerationProviders, mediaUnderstandingProviders, realtimeTranscriptionProviders, speechProviders, tools, videoGenerationProviders, webSearchProviders.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — parent product; relevance: the gateway this xAI provider plugin extends.
- [xAI](../../term_dictionary/term_xai.md) — the xAI / Grok model provider; relevance: the exact subject — the provider this plugin adds.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model-provider backend; relevance: xAI is a provider plugin with the broadest contract surface in this sub-plan.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + contracts declaration; relevance: the Surface declares 7 contracts — a large manifest.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external generative-AI backends; relevance: xAI is an external third-party GenAI provider.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming speech-to-text; relevance: the `realtimeTranscriptionProviders` contract maps directly to this term.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthetic voice; relevance: the `speechProviders` contract (TTS/voice) xAI registers.
- [Video Processing](../../term_dictionary/term_video_processing.md) — video generation/handling (closest existing term); relevance: maps to xAI's `videoGenerationProviders` contract.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multi-content-type models; relevance: image + media-understanding + speech + video + web-search = a multimodal surface.
- [GenAI](../../term_dictionary/term_genai.md) — generative AI umbrella; relevance: xAI is a generative provider plugged into the agent stack.
- [LLM](../../term_dictionary/term_llm.md) — the model layer; relevance: Grok is the LLM fronted through OpenClaw's provider layer.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — the agent tool catalog; relevance: xAI also registers the `tools` contract (one of its 7 surfaces).

**Docs**
- [Hermes Provider xAI/Grok OAuth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — the xAI/Grok provider integration (OAuth) in the sibling stack; relevance: the exact xAI provider this plugin adds.
- [Hermes X Search (Grok)](../hermes_agent/hermes_x_search_grok.md) — Grok-backed web/X search; relevance: maps to xAI's `webSearchProviders` contract.
- [Hermes Model-Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — the model-provider plugin shape; relevance: the generic provider-plugin model xAI instantiates.
- [Hermes Image-Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-generation provider; relevance: xAI's `imageGenerationProviders` contract.
- [Hermes Video-Gen Provider Plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-generation provider; relevance: xAI's `videoGenerationProviders` contract.
- [Hermes TTS Providers](../hermes_agent/hermes_tts_providers.md) — text-to-speech providers; relevance: xAI's `speechProviders` contract.
- [Hermes STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text/transcription; relevance: xAI's `realtimeTranscriptionProviders` contract.
- [Hermes Web-Search Provider Plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — web-search provider plugin; relevance: xAI's `webSearchProviders` contract.
- [oc_providers_xai](oc_providers_xai.md) (planned, this series — pr09) — the full xAI provider doc this reference points at via Related docs; relevance: the Related-docs link-out target.
- [oc_plugins_sdk_provider_plugins](oc_plugins_sdk_provider_plugins.md) (planned, this series — pl24) — how provider plugins are built; relevance: the authoring counterpart of this reference data sheet.
- [oc_tools_grok_search](oc_tools_grok_search.md) (planned, this series — to04) — the Grok web-search tool; relevance: the tool surface xAI's webSearchProviders backs.
- [oc_plugins_reference_index](oc_plugins_reference_index.md) (planned, this series — pl05) — the plugin reference index; relevance: parent reference index this leaf belongs to.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the model-provider code package; relevance: where xAI's provider registration lives.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: hosts provider plugins like xAI.

**Snippets**
- [snippet_hermes_agent_plugins_provider_xai_oauth](../../code_snippets/snippet_hermes_agent_plugins_provider_xai_oauth.md) — the xAI provider OAuth plugin; relevance: the direct code-level analogue of this xAI provider plugin.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — the provider registry; relevance: where the xAI provider plugin is registered.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: provider-plugin initialization path xAI follows.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — a multi-contract provider plugin; relevance: a broad-surface provider plugin like xAI's 7 contracts.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen provider dispatch; relevance: xAI's `imageGenerationProviders` contract dispatch.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen provider dispatch; relevance: xAI's `videoGenerationProviders` contract dispatch.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — a speech-provider TTS impl; relevance: xAI's `speechProviders` contract.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — realtime transcription stream; relevance: xAI's `realtimeTranscriptionProviders` contract.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool wiring; relevance: consumer of xAI's realtime-transcription surface.
- [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — tool registration; relevance: xAI's `tools` contract registration.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — the model catalog; relevance: where xAI/Grok models surface for selection.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the SDK entry shape this provider plugin exposes.

### oc_plugins_reference_xiaomi (8t · 11s · 11d)

Source: xiaomi.md — `@openclaw/xiaomi-provider` (bundled); providers: xiaomi, xiaomi-token-plan; contracts: speechProviders.

**Terms**
- [OpenClaw](../../term_dictionary/term_openclaw.md) — parent product; relevance: the gateway this Xiaomi speech-provider plugin extends.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model-provider backend; relevance: Xiaomi is a provider plugin (two provider ids: `xiaomi`, `xiaomi-token-plan`).
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + Surface declaration; relevance: Distribution + Surface form the manifest.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external generative-AI backends; relevance: Xiaomi is an external third-party GenAI provider.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthetic voice; relevance: the `speechProviders` contract is the plugin's sole surface (TTS/speech).
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — ASR/transcription; relevance: the speech-provider family the `speechProviders` contract spans.
- [Multimodal](../../term_dictionary/term_multimodal.md) — multi-content-type stack; relevance: a speech provider participating in OpenClaw's multimodal media stack.
- [GenAI](../../term_dictionary/term_genai.md) — generative AI umbrella; relevance: Xiaomi is a generative speech provider plugged into the agent stack.
- [LLM](../../term_dictionary/term_llm.md) — the model layer; relevance: fronts a model via the provider layer; `xiaomi-token-plan` is a billing/plan variant.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the catalog of available models/providers; relevance: where Xiaomi's two provider ids surface for selection.

**Docs**
- [Hermes TTS Providers](../hermes_agent/hermes_tts_providers.md) — the text-to-speech provider catalog; relevance: the exact `speechProviders` surface Xiaomi contributes to.
- [Hermes STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text/transcription; relevance: the broader speech-provider family Xiaomi belongs to.
- [Hermes Model-Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — the model-provider plugin shape; relevance: the generic provider-plugin model Xiaomi instantiates.
- [Hermes Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference-provider catalog; relevance: situates Xiaomi among cloud providers.
- [Hermes Env Vars: Providers/Auth/Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider credential/config env vars; relevance: how a provider plugin like Xiaomi (incl. `xiaomi-token-plan`) is configured.
- [PI Custom Provider Registration](../pi/pi_custom_provider_registration.md) — provider registration in a related agent; relevance: cross-product analogue of how Xiaomi registers its providers.
- [Hermes Voice-Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — voice/speech mode usage; relevance: the consumer of Xiaomi's speech-provider surface.
- [oc_providers_xiaomi](oc_providers_xiaomi.md) (planned, this series — pr09) — the full Xiaomi provider doc this reference points at via Related docs; relevance: the Related-docs link-out target.
- [oc_plugins_sdk_provider_plugins](oc_plugins_sdk_provider_plugins.md) (planned, this series — pl24) — how provider plugins are built; relevance: the authoring counterpart of this reference data sheet.
- [oc_nodes_talk](oc_nodes_talk.md) (planned, this series — nd02) — the talk/voice node; relevance: a speech surface that consumes a `speechProviders` provider like Xiaomi.
- [oc_plugins_reference_index](oc_plugins_reference_index.md) (planned, this series — pl05) — the plugin reference index; relevance: parent reference index this leaf belongs to.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the model-provider code package; relevance: where Xiaomi's provider registration lives.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — the voice/speech extension code; relevance: the `speechProviders` contract implementation home.

**Snippets**
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — a `speechProviders` TTS provider impl; relevance: the exact speech-contract Xiaomi registers.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — a local TTS provider; relevance: another speech-provider contract implementation.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — a speech-to-text provider; relevance: the STT side of the speech-provider family.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing; relevance: how a speech provider like Xiaomi is selected/routed.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool wiring; relevance: the consumer of Xiaomi's speech-provider surface.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — a speech pipeline; relevance: the speech-processing path a speechProviders plugin feeds.
- [snippet_openclaw_gateway_talk_transcription_relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — transcription relay; relevance: the speech/transcription surface adjacent to Xiaomi's contract.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — the provider registry; relevance: where the Xiaomi provider plugin is registered.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: provider-plugin initialization path Xiaomi follows.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — the model catalog; relevance: where Xiaomi's two provider ids surface for selection.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the SDK entry shape this provider plugin exposes.


## Undigested Terms Plan

Per master, OpenClaw vocabulary surfaced by these pages is digested as `oc_*` doc notes (these 7) or linked to existing terms — **0 new `term_dictionary` captures**.

| Term (surfaced in pages) | Disposition |
|---|---|
| Vydra / xAI (Grok) / Xiaomi (providers) | Documented as `oc_plugins_reference_{vydra,xai,xiaomi}` concept notes (this sub-plan); link `term_xai` (exists), `term_provider_plugin`, `term_third_party_genai_services`, `term_llm`. NOT promoted to provider-name term notes (master policy: provider names are config/reference, not terms). Provider concept lives in pr09 `/providers/*` docs. |
| webhooks / TaskFlow / workboard / web-readability | Documented as the respective `oc_plugins_reference_*` notes; link existing `term_webhook`, `term_automation`, `term_tool_registry`, `term_event_driven_architecture`. TaskFlow → linked as OpenClaw automation vocab in the webhooks note body (owner: au01 `automation/taskflow` doc), not captured here. NO new `term_taskflow`. |
| OpenClaw plugin contracts (imageGenerationProviders, speechProviders, videoGenerationProviders, mediaUnderstandingProviders, realtimeTranscriptionProviders, webSearchProviders, webContentExtractors, tools, channels) | Plugin-surface vocabulary; documented inline in each note's Surface section as OpenClaw config terms; link `term_provider_plugin`/`term_tool_registry`/`term_realtime_transcription`/`term_text_to_speech`/`term_multimodal`. NOT new term notes (OpenClaw-specific contract identifiers, not reusable cross-cutting terms). |
| ClawHub / npm install routes | OpenClaw distribution vocab; link `term_npm` (exists); ClawHub is its own section (cw01–03), not a term here. NO new captures. |

**New-term candidates:** **0.** No genuinely reusable cross-cutting term lacking an existing note appears (provider/brand names and OpenClaw contract identifiers are excluded by master policy; `term_xai`, `term_webhook`, `term_text_to_speech`, `term_realtime_transcription`, `term_multimodal`, `term_provider_plugin`, `term_tool_registry`, `term_npm` all already exist). If augment's Step 2d re-scan surfaces one, the best-fit glossary is `0_entry_points/acronym_glossary_llm.md` (verified present).

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes (inherited from master). Existing terms are linked only.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P3). All gates must pass before commit.

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean: YAML field order, itemized keywords/topics lists, `## Overview` + `## Related Notes` present, bold `**Source**`/`**Last Updated**`/`**Status**` footer. |
| G2 | Grounding | Every Distribution package id, install route, and Surface contract/provider/channel string traces verbatim to `inbox/openclaw_docs/plugins/reference/<page>.md`; no invented contracts. |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2500 words / ≤6 code blocks (all ~200–240w, 0 code); every source H2 mapped (coverage map). |
| G5 | Ghost-reference | No link to a non-existent note; absent candidates (term_grok/term_whatsapp/term_video_generation/term_web_search/etc.) excluded; detect + redirect any ghost. |
| G6 | Broken-link | `/tessellum-fix-broken-links` clean (correct relative paths from `resources/documentation/openclaw/`). |
| G7/G8 | Discoverability | Each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md`); in-degree ≥1, anti-island. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_vydra oc_plugins_reference_web_readability oc_plugins_reference_webhooks oc_plugins_reference_whatsapp oc_plugins_reference_workboard oc_plugins_reference_xai oc_plugins_reference_xiaomi"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + LINK errors
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  echo "$REQ_SECTIONS" | tr '|' '\n' | while read -r sec; do
    grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"
  done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # density (exclude frontmatter)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # sibling-prefix cross-ref present
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "$n NO SIBLING ($SIBLING_PREFIX) link"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_vydra | concept | 220 | 0 | ✅ |
| 2 | oc_plugins_reference_web_readability | concept | 200 | 0 | ✅ |
| 3 | oc_plugins_reference_webhooks | concept | 220 | 0 | ✅ |
| 4 | oc_plugins_reference_whatsapp | concept | 220 | 0 | ✅ |
| 5 | oc_plugins_reference_workboard | concept | 200 | 0 | ✅ |
| 6 | oc_plugins_reference_xai | concept | 240 | 0 | ✅ |
| 7 | oc_plugins_reference_xiaomi | concept | 220 | 0 | ✅ |

No note approaches any cap (max ~240w vs 2,500w cap; 0 code blocks vs 6 cap). These are deliberately short stub-derived reference notes; the Overview + Distribution + Surface + Related-docs content is the full faithful digest of a 54–63-word source page (no over-compression risk; over-expansion avoided by not inventing provider/channel detail that belongs to pr09/ch06/pl25).

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `0_entry_points/entry_openclaw_docs.md` (CREATED as a master pre-step, W1) under the **Plugins → Reference** cluster (sub-plan pl22). Each note gets its entry-point back-link at finalization (this is the G7/G8 inbound-link source). No standalone entry point for this sub-plan (master's series hub covers all 105 sub-plans).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; the entry point is the primary guaranteed inbound):

- `entry_openclaw_docs.md` (planned, W1) → all 7 notes (primary, guaranteed in-degree ≥1).
- `term_openclaw.md` → notes 1–7 (optional "documented plugins" cross-link, per W3 code↔docs wiring).
- `term_xai.md` → note 6 (`oc_plugins_reference_xai`) — the provider-name term linking its plugin reference.
- `repo_openclaw_extensions_llm_providers.md` → notes 1, 6, 7 (the three model-provider plugins it registers).
- `repo_openclaw_channels_messaging.md` → note 4 (`oc_plugins_reference_whatsapp`).
- `repo_openclaw_extensions.md` → notes 2, 3, 5 (contract/automation/tool plugins).
- `repo_openclaw_gateway.md` → note 3 (`oc_plugins_reference_webhooks`, inbound HTTP surface).
- `term_webhook.md` → note 3; `term_tool_registry.md` → note 5; `term_realtime_transcription.md` → note 6.

## Pacing Rules (inherited from master)

Single phase, 7 notes (well under the ~30-agent fan-out cap; could run as one wave). 8 gates before commit. Re-read each source page; Distribution/Surface strings reproduced verbatim. One BB (concept) per note. `git pull --rebase --autostash` before committing; no Claude co-author trailer; commit + push the wave together; incremental reindex; verify `note_links` + 0 broken links before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note related mapping locked at raised floors ≥8t/≥10s/≥10d) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21** — 9/9 PASS → READY |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope locked.** Re-read all 7 source pages under `inbox/openclaw_docs/plugins/reference/` (vydra 58w, web-readability 57w, webhooks 59w, whatsapp 56w, workboard 54w, xai 62w, xiaomi 63w — 409w total, 0 code fences). Measurements match the plan's Source table exactly (no >50% density miss). All 7 are 54–63-word, 0-code, single-BB (concept) stubs → no splits, no merges (each plugin is a distinct addressable reference object).


**Per-note counts (terms / snippets / docs):**

| Note | Terms | Snippets | Docs (existing+planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_vydra | 8 (10 listed) | 12 | 11 (8 existing + 3 planned) | 2 | ✅ |
| oc_plugins_reference_web_readability | 8 (10 listed) | 11 | 11 (7 existing + 4 planned) | 2 | ✅ |
| oc_plugins_reference_webhooks | 8 (10 listed) | 11 | 11 (7 existing + 4 planned) | 2 | ✅ |
| oc_plugins_reference_whatsapp | 8 (10 listed) | 11 | 11 (7 existing + 4 planned) | 2 | ✅ |
| oc_plugins_reference_workboard | 8 (10 listed) | 11 | 11 (7 existing + 4 planned) | 2 | ✅ |
| oc_plugins_reference_xai | 9 (12 listed) | 12 | 12 (8 existing + 4 planned) | 2 | ✅ |
| oc_plugins_reference_xiaomi | 8 (10 listed) | 11 | 11 (7 existing + 4 planned) | 2 | ✅ |

(Each note's term list carries ≥10 relevance-selected entries — comfortably above the ≥8 floor — so the executor can drop any that read as marginal and still clear the floor. "Terms" column shows the floor-satisfying minimum / full listed count.)




## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; every note ≥8 terms (10–12 listed), ≥10 snippets, ≥10 docs, each rendered `- [Name](relpath.md) — what; relevance: why THIS note`. Floors: 8t/12s/11d · 8t/11s/11d · 8t/11s/11d · 8t/11s/11d · 8t/11s/11d · 9t/12s/12d · 8t/11s/11d. |
| CP2 | 9-GATE present (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost, G6 broken-link, G7/G8 discoverability. Single execution phase, all gates before commit. |
| CP4 | Size (≤30 or split) | **PASS** | 7 planned notes, single phase — well under the 30-note cap and ~30-agent fan-out cap. |
| CP5 | Format derived (not invented) | **PASS** | Format Definition inherited verbatim from master, derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora (same source type); `## Overview` + `## Related Notes` + bold `**Source**`/`**Last Updated**`/`**Status**` footer; forbidden-field list present. Target dir `resources/documentation/openclaw/` exists; scan-map `openclaw → dev_tool_docs` (W4 DONE). |
| CP6 | Density (borderline → split) | **PASS** | Density Re-Assessment: all 7 notes 200–240w / 0 code — max ~10% of the 2,500w cap, 0% of the 6-code cap. No borderline cases; splitting a 60-word source page would violate atomicity in the other direction. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-read all 7 `inbox/openclaw_docs/plugins/reference/*.md` this session: vydra 58 / web-readability 57 / webhooks 59 / whatsapp 56 / workboard 54 / xai 62 / xiaomi 63 (= 409w). Matches plan Source table exactly (ratio 1.0, within 0.7–1.3). Distribution/Surface strings verified verbatim. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (0 new captures — all OpenClaw vocab linked to existing terms or documented as these `oc_*` notes, per master Pattern); `## Term-Note Authoring Requirements` present (N/A — 0 new terms; existing terms linked only). New-term candidates: 0 (Step 2d re-scan). |
| CP9 | Discoverability / inlinks (G8) | **PASS** | `## Inlinks (existing → new notes)` table maps ≥1 outside-folder inbound link per note (primary: `entry_openclaw_docs.md` → all 7, guaranteed in-degree ≥1; plus `term_openclaw`, `term_xai`→note6, `repo_openclaw_*`→relevant notes). G7/G8 in the gate table; inlinks are a gated execution step, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
