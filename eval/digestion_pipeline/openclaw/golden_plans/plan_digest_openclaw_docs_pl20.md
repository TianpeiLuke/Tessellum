---
title: Sub-Plan pl20 — OpenClaw Docs: Plugins (Reference T-batch — tavily, telegram, tencent, tlon, together, tokenjuice, tts-local-cli)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/tavily", "plugins/reference/telegram", "plugins/reference/tencent", "plugins/reference/tlon", "plugins/reference/together", "plugins/reference/tokenjuice", "plugins/reference/tts-local-cli"]
---

# Sub-Plan pl20: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing / format / dedup / 9-GATE / cross-references / undigested-terms / entry-point decisions are inherited
> verbatim from the master and not re-derived here; this file locks only what is specific to its 7 assigned plugin-reference pages.

## Scope

The 7 ClawHub **plugin-reference** stub pages whose slugs begin with `t`: `tavily` (web-search tool/provider
plugin), `telegram` (Telegram channel plugin), `tencent` (Tencent TokenHub model-provider plugin), `tlon`
(Tlon/Urbit channel plugin), `together` (Together model + video-generation provider plugin), `tokenjuice`
(tool-result compaction middleware plugin), and `tts-local-cli` (text-to-speech provider plugin). Each page is
a uniform plugin-catalog card with three fixed facets — **Distribution** (npm package + install route),
**Surface** (the OpenClaw contracts/channels/providers/skills the plugin contributes), and **Related docs**
(pointer to the deep feature page). Priority **P3** (Phase C — plugin-reference sprawl): these are 1-per-plugin
inventory cards, lowest-priority, authored after the conceptual/operational core. The code-side counterparts
(`repo_openclaw_extensions`, `repo_openclaw_extensions_llm_providers`, `repo_openclaw_extensions_voice_speech`,
`repo_openclaw_channels*`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **391 measured words** (47–62 words each — all minimal stub cards). **Planned: 7 notes** (1 note per plugin page; no splits — far below all caps).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| tavily | plugins/reference/tavily | 58 | 0 | 3 | 0 | concept (plugin reference card) |
| telegram | plugins/reference/telegram | 62 | 0 | 3 | 0 | concept (plugin reference card) |
| tencent | plugins/reference/tencent | 56 | 0 | 3 | 0 | concept (plugin reference card) |
| tlon | plugins/reference/tlon | 54 | 0 | 3 | 0 | concept (plugin reference card) |
| together | plugins/reference/together | 56 | 0 | 3 | 0 | concept (plugin reference card) |
| tokenjuice | plugins/reference/tokenjuice | 58 | 0 | 3 | 0 | concept (plugin reference card) |
| tts-local-cli | plugins/reference/tts-local-cli | 47 | 0 | 2 | 0 | concept (plugin reference card) |

Totals: 391 words, 0 code fences, 20 H2, 0 H3 across the 7 pages. All pages share the same template: a one-line
summary, `## Distribution` (Package / Install route), `## Surface` (contracts/channels/providers/skills), and
`## Related docs` (a single `/tools/*`, `/channels/*`, or `/providers/*` pointer). `tts-local-cli` omits
`## Related docs` (2 H2 instead of 3).

## Content Strategy

- **Prioritize**: faithfully capturing each plugin's three load-bearing facts — npm package id, install route
  (included-in-OpenClaw vs npm/ClawHub), and the SDK **Surface** it contributes (which OpenClaw contract,
  channel, provider, or skill it registers). These three facts are the entire informational payload of a
  reference card and are the reason these notes exist in the inventory.
- **Do NOT split**: every page is 47–62 words (≤62), 0 code fences, ≤3 H2 — orders of magnitude under the
  density caps (≤2500w / ≤6 code / ≤400 lines). One BB (`concept`) per page. Master allows splits only for
  pages >2500w or mixed-BB; none qualify. 1 note per page.
- **Do NOT pad / fabricate**: these are intentionally terse catalog cards. Each `oc_*` note's Overview restates
  the summary + the deep-feature it fronts; the body mirrors the three source H2 facets verbatim; depth is
  deferred to the linked deep page (e.g. `/tools/tavily`, `/channels/telegram`, `/providers/tencent`), which
  belongs to a different section/sub-plan (Tools / Channels / Providers) — captured there, not here.
- **Link-out (do not redefine)**: the "Related docs" pointer targets a deep page in another section. Those deep
  pages are owned by `to0*` (Tools: tavily, tokenjuice), `ch0*` (Channels: telegram, tlon), `pr0*` (Providers:
  tencent, together). Link the eventual sibling `oc_*` deep note as "(planned, other sub-plan)" and link the
  existing code-side repo/term notes — do not inline tool/channel/provider behavior here.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_tavily.md` | concept | tavily.md: summary, Distribution, Surface, Related docs | 230 | The OpenClaw Tavily plugin reference card: ships in OpenClaw as `@openclaw/tavily-plugin`, contributes `tools` + `webSearchProviders` contracts plus skills, fronting the Tavily web-search integration documented at `/tools/tavily`. |
| 2 | `oc_plugins_reference_telegram.md` | concept | telegram.md: summary, Distribution, Surface, Related docs | 230 | The OpenClaw Telegram plugin reference card: ships in OpenClaw as `@openclaw/telegram`, contributes the `telegram` channel surface for sending/receiving messages, fronting the channel feature documented at `/channels/telegram`. |
| 3 | `oc_plugins_reference_tencent.md` | concept | tencent.md: summary, Distribution, Surface, Related docs | 230 | The OpenClaw Tencent plugin reference card: ships in OpenClaw as `@openclaw/tencent-provider`, contributes the `tencent-tokenhub` model provider, fronting the provider config documented at `/providers/tencent`. |
| 4 | `oc_plugins_reference_tlon.md` | concept | tlon.md: summary, Distribution, Surface, Related docs | 230 | The OpenClaw Tlon plugin reference card: installs via npm/ClawHub as `@openclaw/tlon`, contributes the `tlon` (Urbit) channel surface plus skills, fronting the channel feature documented at `/channels/tlon`. |
| 5 | `oc_plugins_reference_together.md` | concept | together.md: summary, Distribution, Surface, Related docs | 230 | The OpenClaw Together plugin reference card: ships in OpenClaw as `@openclaw/together-provider`, contributes the `together` model provider plus the `videoGenerationProviders` contract, fronting the provider config documented at `/providers/together`. |
| 6 | `oc_plugins_reference_tokenjuice.md` | concept | tokenjuice.md: summary, Distribution, Surface, Related docs | 230 | The OpenClaw Tokenjuice plugin reference card: installs via npm/ClawHub (`clawhub:@openclaw/tokenjuice`), contributes the `agentToolResultMiddleware` contract to compact exec/bash tool results, fronting the tool documented at `/tools/tokenjuice`. |
| 7 | `oc_plugins_reference_tts_local_cli.md` | concept | tts-local-cli.md: summary, Distribution, Surface | 220 | The OpenClaw TTS Local CLI plugin reference card: ships in OpenClaw as `@openclaw/tts-local-cli`, contributes the `speechProviders` contract to add local text-to-speech output (no Related-docs pointer on the source card). |

Filename rule applied (master): `oc_` + full slug with `/` and `-` → `_`. `plugins/reference/tavily` →
`oc_plugins_reference_tavily.md`; `plugins/reference/tts-local-cli` → `oc_plugins_reference_tts_local_cli.md`.

## Section Coverage Map

```
plugins/reference/tavily.md
├── (summary + intro line) ──────── → note 1 (oc_plugins_reference_tavily) Overview
├── ## Distribution ─────────────── → note 1 (Distribution section)
├── ## Surface ──────────────────── → note 1 (Surface section: tools, webSearchProviders; skills)
└── ## Related docs ─────────────── → note 1 (Related Notes / References: → /tools/tavily)
plugins/reference/telegram.md
├── (summary + intro line) ──────── → note 2 (oc_plugins_reference_telegram) Overview
├── ## Distribution ─────────────── → note 2
├── ## Surface ──────────────────── → note 2 (channels: telegram)
└── ## Related docs ─────────────── → note 2 (→ /channels/telegram)
plugins/reference/tencent.md
├── (summary + intro line) ──────── → note 3 (oc_plugins_reference_tencent) Overview
├── ## Distribution ─────────────── → note 3
├── ## Surface ──────────────────── → note 3 (providers: tencent-tokenhub)
└── ## Related docs ─────────────── → note 3 (→ /providers/tencent)
plugins/reference/tlon.md
├── (summary + intro line) ──────── → note 4 (oc_plugins_reference_tlon) Overview
├── ## Distribution ─────────────── → note 4 (npm; ClawHub)
├── ## Surface ──────────────────── → note 4 (channels: tlon; skills)
└── ## Related docs ─────────────── → note 4 (→ /channels/tlon)
plugins/reference/together.md
├── (summary + intro line) ──────── → note 5 (oc_plugins_reference_together) Overview
├── ## Distribution ─────────────── → note 5
├── ## Surface ──────────────────── → note 5 (providers: together; contracts: videoGenerationProviders)
└── ## Related docs ─────────────── → note 5 (→ /providers/together)
plugins/reference/tokenjuice.md
├── (summary + intro line) ──────── → note 6 (oc_plugins_reference_tokenjuice) Overview
├── ## Distribution ─────────────── → note 6 (npm; ClawHub: clawhub:@openclaw/tokenjuice)
├── ## Surface ──────────────────── → note 6 (contracts: agentToolResultMiddleware)
└── ## Related docs ─────────────── → note 6 (→ /tools/tokenjuice)
plugins/reference/tts-local-cli.md
├── (summary + intro line) ──────── → note 7 (oc_plugins_reference_tts_local_cli) Overview
├── ## Distribution ─────────────── → note 7 (included in OpenClaw)
└── ## Surface ──────────────────── → note 7 (contracts: speechProviders)
```

No orphaned sections; every H2 of every page maps to exactly one note. The single `Related docs` pointer per
page maps to the note's `## Related Notes`/`## References` (link-out to the deep page's owning sub-plan).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are 47–62 words, 0 code fences, ≤3 H2, single `concept` BB — far below every density cap. 1 note per page; no merges, no splits. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (391 words total; range 47–62 words/page). New `oc_` notes: **7**. New `term_dictionary`
  notes: **0** (see Undigested Terms Plan).
- BB distribution: `concept` ×7 (every page is a static plugin-reference catalog card — capability declaration,
  not a how-to procedure). No procedure / model / argument notes in this batch.
- Est. digest words: ~1,600 total (~230/note). 0 source code fences ⇒ each note ≤6 code blocks trivially; each
  note ≪2500w / ≪400 lines. Notes are slightly longer than the source cards because the Overview + Related
  Notes (≥6 relevance-selected links) add the vault-connectivity layer the bare card lacks.
- **Cross-refs (raised floors, LOCKED at xref-augment 2026-06-21):** each note maps **≥8 relevance-selected
  mapping in `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`. Per-note totals: tavily
  9t·13s·12d; telegram 9t·13s·12d; tencent/tlon/together/tokenjuice/tts_local_cli 9t·12s·12d each.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)


FROM notes WHERE note_id='…'`). Each note meets ALL three raised floors: **≥8 `term_dictionary` terms**,
"(planned, …)") — PLUS relevant `repo_openclaw*` and entry points as additional connectivity. RELEVANCE is the
Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`: terms `../../term_dictionary/term_Y.md`;
snippets `../../code_snippets/snippet_Y.md`; sibling oc docs `oc_Y.md`; other-folder docs `../<folder>/<file>.md`
(e.g. `../claude_code/cc_Y.md`, `../hermes_agent/hermes_Y.md`, `../pi/pi_Y.md`, `../band/band_Y.md`); repos
`../../../areas/code_repos/repo_Y.md`; entry points `../../../0_entry_points/entry_Y.md`.

### oc_plugins_reference_tavily (9t · 13s · 12d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway hosting this plugin; relevance: this note IS an OpenClaw plugin-reference card.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the manifest declaring a plugin's package + surface; relevance: the card's Distribution facet is a manifest entry.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the contract API plugins register against; relevance: Tavily contributes `tools` + `webSearchProviders` SDK contracts.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent-callable tool invocation; relevance: a `tools` contract exposes Tavily as an agent-callable function.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — where tools register for the agent; relevance: the plugin inserts the Tavily search tool into the registry.
- [RAG](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: web search grounds the agent like retrieval augmentation.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — querying a corpus for relevant docs; relevance: web search is live-web information retrieval.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol tool surface; relevance: a tool/search surface analog to MCP-served tools.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI APIs; relevance: Tavily is an external web-search API.

**Docs** (12)
- [Hermes web-search provider plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — Hermes' analogous web-search provider plugin; relevance: direct sibling-ecosystem implementation of the same `webSearchProviders` surface.
- [Hermes web search + extract](../hermes_agent/hermes_web_search_extract.md) — web search/extract tool behavior; relevance: shows what a web-search tool returns to the agent.
- [Hermes tool search](../hermes_agent/hermes_tool_search.md) — agent tool-search/discovery; relevance: the registry surface Tavily's tool joins.
- [Hermes tool gateway](../hermes_agent/hermes_tool_gateway.md) — gateway tool routing; relevance: how a registered tool is exposed/invoked.
- [Hermes x/grok search](../hermes_agent/hermes_x_search_grok.md) — another external search provider; relevance: parallel external-search integration pattern.
- [cc built-in tools](../claude_code/cc_built_in_tools.md) — Claude Code built-in tool set incl. web search; relevance: peer coding-agent's web-search tool framing.
- [cc tools catalog](../claude_code/cc_tools_catalog.md) — full tool catalog; relevance: how a search tool sits among agent tools.
- [cc MCP tool search](../claude_code/cc_mcp_tool_search.md) — tool-search over MCP servers; relevance: tool-surface discovery analog.
- [cc web overview](../claude_code/cc_web_overview.md) — agent web access; relevance: the web-access capability Tavily supplies.
- [oc_tools_tavily](oc_tools_tavily.md) — deep Tavily tool page (planned, sub-plan to07); relevance: the feature page this reference card fronts.
- [oc_plugins_reference_tokenjuice](oc_plugins_reference_tokenjuice.md) — sibling tool-contributing plugin (planned, this batch); relevance: same `tools` contract family.
- [oc_tools_tokenjuice](oc_tools_tokenjuice.md) — deep Tokenjuice tool page (planned, sub-plan to08); relevance: related tool-surface deep page.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin/extension framework hosting this plugin.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo.
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — analogous web-search/tool plugin layer.
- entry_openclaw_docs (planned, master W1) — docs hub back-link.

**Snippets** (13)
- [openclaw plugin lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/activate lifecycle; relevance: how this plugin is loaded.
- [openclaw plugin package contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — npm-package plugin contract; relevance: the Distribution facet's package shape.
- [openclaw plugin SDK entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK contract entry points; relevance: the `tools`/`webSearchProviders` contracts it registers.
- [openclaw agents tool catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog assembly; relevance: where the Tavily tool lands.
- [openclaw agents tool policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool enable/deny policy; relevance: gating the search tool.
- [openclaw skills tool descriptor contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor schema; relevance: descriptor for the contributed tool.
- [openclaw agents memory search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — agent search over memory; relevance: search-surface implementation analog.
- [hermes web tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web-search tool implementation; relevance: concrete web-search tool code.
- [hermes tools registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: registering a tool plugin.
- [hermes mcp serve tool surface](../../code_snippets/snippet_hermes_agent_mcp_serve_tool_surface.md) — serving tools over MCP; relevance: tool-surface exposure analog.
- [openclaw gateway server plugins runtime load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loading; relevance: how the gateway loads this plugin.
- [openclaw gateway server impl config plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — plugin config wiring; relevance: configuring the plugin.
- [openclaw gateway server http plugin routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — plugin HTTP routing; relevance: plugin route registration.

### oc_plugins_reference_telegram (9t · 13s · 12d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: this is an OpenClaw channel-plugin card.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package/surface manifest; relevance: Distribution facet.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin contract API; relevance: Telegram contributes a `channels` SDK surface.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — adapter bridging a chat platform to the harness; relevance: the Telegram plugin IS a channel adapter.
- [Bot](../../term_dictionary/term_bot.md) — automated chat actor; relevance: the Telegram surface is a bot integration.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational bot; relevance: Telegram delivers conversational messages to the agent.
- [WebSocket](../../term_dictionary/term_websocket.md) — duplex transport; relevance: channel transport analog for send/receive.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime the channel feeds; relevance: the channel pipes messages into the harness.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway routing chat messages; relevance: the subsystem the channel plugs into.

**Docs** (12)
- [Hermes messaging — Slack](../hermes_agent/hermes_messaging_slack.md) — analogous chat-channel adapter; relevance: same channel-adapter pattern in the sibling ecosystem.
- [Hermes Telegram setup](../hermes_agent/hermes_telegram_setup.md) — Telegram channel setup; relevance: the very platform this plugin adds.
- [Hermes Telegram advanced](../hermes_agent/hermes_telegram_advanced.md) — advanced Telegram config; relevance: deeper Telegram channel behavior.
- [Hermes team Telegram assistant guide](../hermes_agent/hermes_guide_team_telegram_assistant.md) — end-to-end Telegram assistant; relevance: real Telegram-channel usage.
- [Hermes adding platform adapter plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — building a channel plugin; relevance: how a channel plugin like this is authored.
- [Hermes messaging — Slack config](../hermes_agent/hermes_messaging_slack_config.md) — channel config reference; relevance: channel-plugin config shape.
- [Hermes WhatsApp cloud model](../hermes_agent/hermes_messaging_whatsapp_cloud_model.md) — another messaging channel; relevance: parallel platform-channel integration.
- [band websocket agent channels](../band/band_websocket_agent_channels.md) — agent chat channels over websocket; relevance: channel-transport model analog.
- [cc channel reply tool](../claude_code/cc_channel_reply_tool.md) — replying on a channel; relevance: channel send-side analog.
- [oc_channels_telegram](oc_channels_telegram.md) — deep Telegram channel page (planned, sub-plan ch05); relevance: the feature page this card fronts.
- [oc_plugins_reference_tlon](oc_plugins_reference_tlon.md) — sibling channel plugin (planned, this batch); relevance: same `channels` contract family.
- [oc_channels_tlon](oc_channels_tlon.md) — deep Tlon channel page (planned, sub-plan ch05); relevance: related channel deep page.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel subsystem this plugin extends.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — the messaging-channel layer.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo.
- entry_openclaw_docs (planned, master W1) — docs hub back-link.

**Snippets** (13)
- [openclaw channels telegram dispatcher](../../code_snippets/snippet_openclaw_channels_telegram_dispatcher.md) — Telegram message dispatch; relevance: concrete Telegram-channel code this plugin provides.
- [openclaw channels telegram transport](../../code_snippets/snippet_openclaw_channels_telegram_transport.md) — Telegram transport layer; relevance: the send/receive transport.
- [openclaw channels adapter contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter interface; relevance: the `channels` contract Telegram implements.
- [openclaw channels kernel dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel routing; relevance: routing inbound Telegram messages.
- [openclaw channels registry normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry; relevance: registering the Telegram channel.
- [openclaw channels binding routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding/routing; relevance: binding Telegram conversations to sessions.
- [openclaw channels conversation resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — resolving a conversation; relevance: mapping Telegram chats to agent threads.
- [hermes gw platform telegram connect](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_connect.md) — Telegram connect; relevance: analog Telegram connection code.
- [hermes gw platform telegram normalize](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_normalize.md) — Telegram message normalize; relevance: normalizing inbound Telegram payloads.
- [hermes gw platform telegram media](../../code_snippets/snippet_hermes_agent_gw_platform_telegram_media.md) — Telegram media handling; relevance: media on the Telegram channel.
- [hermes gw channel directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory; relevance: registry of channels.
- [openclaw plugin lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: how the plugin loads.
- [openclaw gateway server plugins runtime load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: gateway loading the channel plugin.

### oc_plugins_reference_tencent (9t · 12s · 12d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: this is an OpenClaw provider-plugin card.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package/surface manifest; relevance: Distribution facet.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin contract API; relevance: Tencent contributes a `providers` surface.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model backend; relevance: the plugin registers the `tencent-tokenhub` provider.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: TokenHub fronts LLMs.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — registry of available models; relevance: the provider contributes models to the catalog.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI APIs; relevance: Tencent is an external GenAI provider.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — routing requests across providers; relevance: where the Tencent provider participates.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool-call capability of a model; relevance: a provider's models must support tool calls for the harness.

**Docs** (12)
- [Hermes model provider plugin](../hermes_agent/hermes_model_provider_plugin.md) — analogous model-provider plugin; relevance: same `providers` surface in the sibling ecosystem.
- [Hermes adding inference provider](../hermes_agent/hermes_adding_inference_provider.md) — authoring a provider plugin; relevance: how a provider plugin like Tencent is built.
- [Hermes inference providers (cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: Tencent is a cloud provider.
- [Hermes model catalog reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog; relevance: catalog the provider feeds.
- [Hermes provider routing](../hermes_agent/hermes_provider_routing.md) — provider routing; relevance: routing across providers incl. Tencent.
- [Hermes provider — AWS Bedrock](../hermes_agent/hermes_provider_aws_bedrock.md) — a concrete provider; relevance: peer cloud-provider integration shape.
- [pi cloud providers](../pi/pi_cloud_providers.md) — cloud-provider setup; relevance: external-provider configuration analog.
- [pi custom provider registration](../pi/pi_custom_provider_registration.md) — registering a custom provider; relevance: how a provider plugin registers.
- [cc managed MCP configuration](../claude_code/cc_managed_mcp_configuration.md) — managed model/tool config; relevance: provider-config governance analog.
- [oc_providers_tencent](oc_providers_tencent.md) — deep Tencent provider page (planned, sub-plan pr08); relevance: the feature page this card fronts.
- [oc_plugins_reference_together](oc_plugins_reference_together.md) — sibling provider plugin (planned, this batch); relevance: same `providers` contract family.
- [oc_providers_together](oc_providers_together.md) — deep Together provider page (planned, sub-plan pr08); relevance: related provider deep page.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the LLM-provider extension layer.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider-adapter analog.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo.
- entry_openclaw_docs (planned, master W1) — docs hub back-link.

**Snippets** (12)
- [openclaw provider anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a model provider impl; relevance: peer `providers` contract implementation.
- [openclaw provider openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider impl; relevance: peer provider implementation.
- [openclaw provider openrouter aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider; relevance: multi-model provider pattern like TokenHub.
- [openclaw agents model catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: where Tencent models land.
- [openclaw model catalog normalize discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery/normalize; relevance: normalizing provider model lists.
- [openclaw model catalog manifest planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planning; relevance: provider model manifest.
- [openclaw gateway model pricing alias lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing/alias; relevance: provider model pricing.
- [hermes plugins provider registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: registering a provider plugin.
- [hermes plugins provider china cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — China-region providers; relevance: Tencent is a China-region GenAI provider.
- [hermes providers base abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base interface; relevance: the contract a provider plugin implements.
- [openclaw plugin sdk entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK contract entries; relevance: the `providers` contract registration.

### oc_plugins_reference_tlon (9t · 12s · 12d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: this is an OpenClaw channel-plugin card.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package/surface manifest; relevance: Distribution facet (npm; ClawHub).
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin contract API; relevance: Tlon contributes a `channels` surface + skills.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — chat-platform-to-harness bridge; relevance: the Tlon plugin IS a channel adapter for Urbit.
- [Bot](../../term_dictionary/term_bot.md) — automated chat actor; relevance: the Tlon surface is a chat-bot integration.
- [Chatbot](../../term_dictionary/term_chatbot.md) — conversational bot; relevance: Tlon/Urbit chat workflows feed the agent.
- [WebSocket](../../term_dictionary/term_websocket.md) — duplex transport; relevance: channel transport analog.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime the channel feeds; relevance: the channel pipes Urbit messages to the harness.
- [npm](../../term_dictionary/term_npm.md) — Node package registry; relevance: Tlon's install route is npm/ClawHub (not bundled), unlike most cards.

**Docs** (12)
- [Hermes adding platform adapter plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — building a channel plugin; relevance: how a channel plugin like Tlon is authored.
- [Hermes messaging — Slack](../hermes_agent/hermes_messaging_slack.md) — channel adapter; relevance: channel-adapter pattern analog.
- [Hermes messaging — Slack config](../hermes_agent/hermes_messaging_slack_config.md) — channel config; relevance: channel-plugin config shape.
- [Hermes Telegram setup](../hermes_agent/hermes_telegram_setup.md) — another channel setup; relevance: parallel channel-plugin install/config.
- [Hermes plugins management](../hermes_agent/hermes_plugins_management.md) — installing/removing plugins; relevance: Tlon installs via npm/ClawHub, not bundled.
- [Hermes WhatsApp cloud model](../hermes_agent/hermes_messaging_whatsapp_cloud_model.md) — messaging channel; relevance: parallel platform-channel integration.
- [band websocket agent channels](../band/band_websocket_agent_channels.md) — agent channels over websocket; relevance: channel-transport model analog.
- [cc channel reply tool](../claude_code/cc_channel_reply_tool.md) — channel send-side; relevance: replying on a channel analog.
- [pi skills](../pi/pi_skills.md) — skill contribution; relevance: Tlon also contributes skills (the card's `skills` surface).
- [oc_channels_tlon](oc_channels_tlon.md) — deep Tlon channel page (planned, sub-plan ch05); relevance: the feature page this card fronts.
- [oc_plugins_reference_telegram](oc_plugins_reference_telegram.md) — sibling channel plugin (planned, this batch); relevance: same `channels` contract family.
- [oc_channels_telegram](oc_channels_telegram.md) — deep Telegram channel page (planned, sub-plan ch05); relevance: related channel deep page.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel subsystem this plugin extends.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — the messaging-channel layer.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — the skills layer (Tlon also contributes skills).
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo.
- entry_openclaw_docs (planned, master W1) — docs hub back-link.

**Snippets** (12)
- [openclaw channels adapter contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter interface; relevance: the `channels` contract Tlon implements.
- [openclaw channels kernel dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel routing; relevance: routing inbound Tlon messages.
- [openclaw channels registry normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry; relevance: registering the Tlon channel.
- [openclaw channels binding routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding/routing; relevance: binding Tlon conversations.
- [openclaw channels conversation resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: mapping Urbit chats to agent threads.
- [openclaw channels match resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — match resolution; relevance: resolving channel routes.
- [openclaw channels thread bindings policy](../../code_snippets/snippet_openclaw_channels_thread_bindings_policy.md) — thread binding policy; relevance: per-thread channel policy.
- [openclaw channels dm pairing allowlist](../../code_snippets/snippet_openclaw_channels_dm_pairing_allowlist.md) — DM pairing allowlist; relevance: access control on a chat channel.
- [hermes gw channel directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory; relevance: registry of channels.
- [openclaw skills planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skills planning; relevance: the `skills` surface Tlon also contributes.
- [openclaw plugin package contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — npm-package plugin contract; relevance: Tlon installs via npm/ClawHub.
- [openclaw gateway server plugins runtime load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: gateway loading the channel plugin.

### oc_plugins_reference_together (9t · 12s · 12d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: this is an OpenClaw provider-plugin card.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package/surface manifest; relevance: Distribution facet.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin contract API; relevance: Together contributes `providers` + `videoGenerationProviders` surfaces.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable model backend; relevance: the plugin registers the `together` provider.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Together fronts open-weight LLMs.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — model registry; relevance: the provider contributes models.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external AI APIs; relevance: Together is an external GenAI provider.
- [Model Router](../../term_dictionary/term_model_router.md) — routes to a chosen model; relevance: a provider's models become routing targets.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool-call capability; relevance: provider models must support tool calls.

**Docs** (12)
- [Hermes model provider plugin](../hermes_agent/hermes_model_provider_plugin.md) — analogous model-provider plugin; relevance: same `providers` surface in the sibling ecosystem.
- [Hermes video-gen provider plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — a video-generation provider plugin; relevance: Together also contributes `videoGenerationProviders`.
- [Hermes image-gen provider plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — a media-generation provider plugin; relevance: peer media-generation provider surface.
- [Hermes inference providers (cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: Together is a cloud provider.
- [Hermes adding inference provider](../hermes_agent/hermes_adding_inference_provider.md) — authoring a provider plugin; relevance: how the Together plugin is built.
- [Hermes model catalog reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog; relevance: catalog the provider feeds.
- [pi cloud providers](../pi/pi_cloud_providers.md) — cloud-provider setup; relevance: external-provider configuration analog.
- [pi custom models](../pi/pi_custom_models.md) — registering custom models; relevance: Together's open-weight models.
- [oc_providers_together](oc_providers_together.md) — deep Together provider page (planned, sub-plan pr08); relevance: the feature page this card fronts.
- [oc_plugins_reference_tencent](oc_plugins_reference_tencent.md) — sibling provider plugin (planned, this batch); relevance: same `providers` contract family.
- [oc_providers_tencent](oc_providers_tencent.md) — deep Tencent provider page (planned, sub-plan pr08); relevance: related provider deep page.
- [oc_tools_video_generation](oc_tools_video_generation.md) — deep video-generation tool page (planned, sub-plan to08); relevance: the `videoGenerationProviders` contract's consuming feature.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the LLM-provider extension layer.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider-adapter analog.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo.
- entry_openclaw_docs (planned, master W1) — docs hub back-link.

**Snippets** (12)
- [openclaw provider anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — model provider impl; relevance: peer `providers` contract implementation.
- [openclaw provider openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider impl; relevance: peer provider implementation.
- [openclaw provider ollama local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — open-weight model provider; relevance: Together also serves open-weight models.
- [openclaw provider openrouter aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider; relevance: multi-model provider pattern.
- [openclaw agents model catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: where Together models land.
- [openclaw model catalog normalize discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery; relevance: normalizing provider model lists.
- [hermes plugins provider registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: registering a provider plugin.
- [hermes providers base abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base interface; relevance: the contract a provider plugin implements.
- [hermes plugins video gen dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen dispatch; relevance: the `videoGenerationProviders` contract Together adds.
- [hermes tools video gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-gen tool; relevance: video-generation consumer of the provider.
- [openclaw plugin sdk entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK contract entries; relevance: the dual contracts Together registers.

### oc_plugins_reference_tokenjuice (9t · 12s · 12d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: this is an OpenClaw tool/middleware-plugin card.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package/surface manifest; relevance: Distribution facet (npm; ClawHub).
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin contract API; relevance: Tokenjuice contributes the `agentToolResultMiddleware` contract.
- [Compaction](../../term_dictionary/term_compaction.md) — shrinking conversation/tool content; relevance: Tokenjuice compacts exec/bash tool results.
- [Context Compression](../../term_dictionary/term_context_compression.md) — reducing tokens in context; relevance: the middleware's core function.
- [Context Window](../../term_dictionary/term_context_window.md) — the token budget; relevance: the budget Tokenjuice protects.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — token-economy via cache reuse; relevance: sibling token-economy technique.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation producing results; relevance: it middlewares exec/bash tool-call results.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime that runs tool middleware; relevance: the harness applies the middleware to results.

**Docs** (12)
- [Hermes context compression + caching](../hermes_agent/hermes_context_compression_caching.md) — context compression/caching; relevance: directly the technique Tokenjuice applies.
- [Hermes runtime context settings](../hermes_agent/hermes_runtime_context_settings.md) — context budget settings; relevance: configuring the context the middleware trims.
- [Hermes context references](../hermes_agent/hermes_context_references.md) — context reference handling; relevance: managing what stays in context.
- [Hermes tools reference (core)](../hermes_agent/hermes_tools_reference_core.md) — core tool behavior; relevance: the exec/bash tool results being compacted.
- [Hermes plugin hook reference](../hermes_agent/hermes_plugin_hook_reference.md) — plugin hooks/middleware; relevance: middleware-plugin extension surface.
- [Hermes plugin extensions + hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — extension hooks; relevance: how a middleware plugin hooks the result pipeline.
- [cc tools catalog](../claude_code/cc_tools_catalog.md) — tool catalog; relevance: the tool results being middlewared.
- [pi extensions custom tools](../pi/pi_extensions_custom_tools.md) — custom tool extension; relevance: tool-extension authoring analog.
- [pi extensions context](../pi/pi_extensions_context.md) — context extensions; relevance: context-shaping extension analog.
- [oc_tools_tokenjuice](oc_tools_tokenjuice.md) — deep Tokenjuice tool page (planned, sub-plan to08); relevance: the feature page this card fronts.
- [oc_plugins_reference_tavily](oc_plugins_reference_tavily.md) — sibling tool-contributing plugin (planned, this batch); relevance: same tool/contract family.
- [oc_concepts_compaction](oc_concepts_compaction.md) — deep compaction concept page (planned, sub-plan co02); relevance: the underlying concept Tokenjuice implements.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework hosting the middleware.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session/context state the middleware trims.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo.
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — tool-result handling analog.
- entry_openclaw_docs (planned, master W1) — docs hub back-link.

**Snippets** (12)
- [openclaw agents compaction chunk safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — compaction chunk safety; relevance: core compaction logic like Tokenjuice's.
- [openclaw agents compaction identifier handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — compaction identifier handoff; relevance: preserving identifiers across compaction.
- [openclaw gateway sessions compact reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — session compaction/reset; relevance: compacting session context.
- [openclaw agents context window guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — context-window guard; relevance: the budget protection Tokenjuice serves.
- [openclaw agents context lookup](../../code_snippets/snippet_openclaw_agents_context_lookup.md) — context lookup; relevance: reading what's in context before trimming.
- [openclaw agents system prompt cache sections](../../code_snippets/snippet_openclaw_agents_system_prompt_cache_sections.md) — prompt cache sections; relevance: sibling token-economy mechanism.
- [hermes core tool result classification](../../code_snippets/snippet_hermes_agent_core_tool_result_classification.md) — tool-result classification; relevance: classifying results before compacting.
- [hermes core tool dispatch helpers](../../code_snippets/snippet_hermes_agent_core_tool_dispatch_helpers.md) — tool dispatch helpers; relevance: the tool-result pipeline the middleware wraps.
- [openclaw agents tool catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: exec/bash tools whose results are compacted.
- [openclaw agents tool policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy; relevance: policy over tool execution.
- [openclaw plugin lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: how the middleware plugin loads.
- [openclaw plugin package contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — npm-package plugin contract; relevance: Tokenjuice installs via npm/ClawHub.

### oc_plugins_reference_tts_local_cli (9t · 12s · 12d)

**Terms** (9)
- [OpenClaw](../../term_dictionary/term_openclaw.md) — host gateway; relevance: this is an OpenClaw speech-provider-plugin card.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package/surface manifest; relevance: Distribution facet.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — plugin contract API; relevance: the plugin contributes the `speechProviders` surface.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — synthesizing speech from text; relevance: the exact capability the plugin adds.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — transcribing speech; relevance: complementary voice modality on the speech pipeline.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — pluggable backend; relevance: a `speechProviders` contract = a pluggable speech backend.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — agent voice interaction; relevance: TTS output is the voice-mode response channel.
- [Voice Call](../../term_dictionary/term_voice_call.md) — phone/voice channel; relevance: a voice channel consuming local TTS.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — runtime that emits speech; relevance: the harness routes responses to the speech provider.

**Docs** (12)
- [Hermes TTS providers](../hermes_agent/hermes_tts_providers.md) — TTS provider catalog; relevance: directly the `speechProviders` surface this plugin adds.
- [Hermes use voice-mode guide](../hermes_agent/hermes_use_voice_mode_guide.md) — voice-mode usage; relevance: voice mode consumes local TTS output.
- [Hermes voice-mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — voice-mode CLI; relevance: configuring/using voice with TTS.
- [Hermes voice gateway (Discord VC)](../hermes_agent/hermes_voice_gateway_discord_vc.md) — a voice channel; relevance: a voice consumer of TTS.
- [Hermes model provider plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin authoring; relevance: the provider-plugin pattern (speech is a provider kind).
- [Hermes adding inference provider](../hermes_agent/hermes_adding_inference_provider.md) — authoring a provider plugin; relevance: how a speech provider plugin is built.
- [pi cloud providers](../pi/pi_cloud_providers.md) — provider setup; relevance: provider-configuration analog (local vs cloud TTS).
- [cc tools catalog](../claude_code/cc_tools_catalog.md) — tool catalog; relevance: where output-modality tools sit.
- [oc_tools_tts](oc_tools_tts.md) — deep TTS tool page (planned, sub-plan to08); relevance: the feature page this card fronts.
- [oc_plugins_reference_tencent](oc_plugins_reference_tencent.md) — sibling provider plugin (planned, this batch); relevance: same provider-contract family.
- [oc_nodes_talk](oc_nodes_talk.md) — deep voice/talk node page (planned, sub-plan nd02); relevance: a node that emits speech via the provider.
- [oc_concepts_streaming](oc_concepts_streaming.md) — deep streaming concept page (planned, sub-plan co07); relevance: speech output is streamed.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — the voice/speech extension layer.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin framework.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice channel consumer of TTS.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo.
- entry_openclaw_docs (planned, master W1) — docs hub back-link.

**Snippets** (12)
- [openclaw speech elevenlabs tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — an ElevenLabs TTS provider; relevance: peer `speechProviders` implementation.
- [openclaw mlx tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX text-to-speech; relevance: directly a LOCAL TTS provider like tts-local-cli.
- [openclaw speech deepgram stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — a Deepgram STT provider; relevance: complementary speech-to-text modality.
- [openclaw swabble speech pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the pipeline TTS output flows through.
- [openclaw gateway talk transcription relay](../../code_snippets/snippet_openclaw_gateway_talk_transcription_relay.md) — talk/transcription relay; relevance: routing speech between agent and channel.
- [openclaw voice call media stream transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — voice-call media/transcription; relevance: a voice consumer of speech providers.
- [openclaw voice call runtime](../../code_snippets/snippet_openclaw_voice_call_runtime.md) — voice-call runtime; relevance: voice channel emitting TTS.
- [hermes tools tts routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: routing text to a TTS provider.
- [hermes tools transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: complementary speech modality.
- [hermes tools voice mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: voice mode consuming TTS.
- [openclaw plugin sdk entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — SDK contract entries; relevance: the `speechProviders` contract registration.
- [openclaw plugin lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: how the speech plugin loads.

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| plugin / extension (OpenClaw plugin system) | OpenClaw vocab → captured as the `oc_plugins_reference_*` doc notes themselves (this batch + the rest of pl01–25); link existing `term_plugin_manifest` ✓ + `term_plugin_sdk` ✓. No new term note. |
| tavily / Tavily web search | Product/provider name documented as the plugin reference card (note 1) + deep page `/tools/tavily` (to07). Not a reusable cross-cutting term → link `term_rag` ✓ / `term_information_retrieval` ✓ / `term_function_calling` ✓. No new term note. |
| webSearchProviders / web search provider (contract) | OpenClaw SDK contract name → described inline in note 1's Surface section; link `term_information_retrieval` ✓ / `term_rag` ✓. No new term note. |
| telegram / Telegram channel | Platform name → note 2 + deep page `/channels/telegram` (ch05). Link `term_bot` ✓ / `term_chatbot` ✓. No new term note. |
| tencent / TokenHub | Provider name → note 3 + deep page `/providers/tencent` (pr08). Link `term_llm` ✓ / `term_third_party_genai_services` ✓ / `term_provider_plugin` ✓. No new term note. |
| tlon / Urbit | Platform name → note 4 + deep page `/channels/tlon` (ch05). Link `term_bot` ✓ / `term_chatbot` ✓. No new term note. |
| together / Together AI | Provider name → note 5 + deep page `/providers/together` (pr08). Link `term_llm` ✓ / `term_provider_plugin` ✓. No new term note. |
| videoGenerationProviders (contract) | OpenClaw SDK contract name → inline in note 5's Surface section; no existing/dedicated term, but a single appearance of a contract name is not a reusable cross-cutting term → describe inline, no capture. |
| tokenjuice / agentToolResultMiddleware | Plugin/contract name → note 6 + deep page `/tools/tokenjuice` (to08). Link existing `term_compaction` ✓ / `term_context_compression` ✓. No new term note. |
| tts-local-cli / speechProviders | Plugin/contract name → note 7 + deep page `/tools/tts` (to08). Link existing `term_text_to_speech` ✓. No new term note. |

**Outcome: 0 new `term_dictionary` captures.** Every facet maps either to an `oc_*` doc note (this batch or a
subjects of dedicated doc pages and are digested as `oc_*` documentation concept notes, never as new
`term_dictionary` entries; the only `term_dictionary` interaction is linking existing terms. No genuinely
cross-cutting, vault-reusable term with no existing home appears in this batch. Augment re-runs the Step 2d scan.

## Term-Note Authoring Requirements

**N/A (0 new terms)** — this sub-plan authors zero `term_dictionary` notes; it only links existing,
Step 2d re-scan surfaces a genuinely reusable cross-cutting term with no existing note, capture it via
`/tessellum-capture-term-note` and add it to the best-fit `acronym_glossary_*.md` per master W5 — not expected.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P3). Gate table inherited verbatim from the master:

| Gate | Check | Tool / Method | Pass condition |
|------|-------|---------------|----------------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` | YAML field order + forbidden-field check pass; `# OpenClaw — …` H1, `## Overview`, `## Related Notes`, `## References`, bold `**Source**`/`**Last Updated**`/`**Status**` footer present. |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/plugins/reference/<page>.md` | Package id, install route, and Surface contracts/channels/providers reproduced exactly; no fabricated facts beyond the source card. |
| G3 | Density + Coverage | `wc -w` + fence count; section coverage map | Each note ≤2500w / ≤6 code / ≤400 lines (trivially met, ~230w); every source H2 covered. |
| G4 | Cross-Reference | count Related Notes links + relevance statements | ≥6 relevance-selected term links + relevant repos/siblings per note, each with a relevance statement. |
| G5 | Ghost-reference | `/tessellum-fix-ghost-references` + DB existence check | 0 links to non-existent notes (sibling `oc_*` planned-but-absent links deferred/redirected per master). |
| G6 | Broken-link | `/tessellum-fix-broken-links` + reindex | 0 broken relative paths after incremental reindex. |
| G7 | Discoverability | `entry_openclaw_docs.md` rows + reciprocal inlinks | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/`. |
| G8 | In-degree ≥1 | `note_links` query post-reindex | Each new note's `in_degree ≥ 1` (anti-island), satisfied via `entry_openclaw_docs.md`. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

All 8 gates must pass before commit.

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_tavily oc_plugins_reference_telegram oc_plugins_reference_tencent oc_plugins_reference_tlon oc_plugins_reference_together oc_plugins_reference_tokenjuice oc_plugins_reference_tts_local_cli"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "MISSING SECTION in $n: $sec"; done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "MISSING source_url in $n"; }
  # G3 density (body words, excluding frontmatter; code fences/2)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # G4 sibling/cross-ref presence sanity
  grep -q "$SIBLING_PREFIX" "$f" || echo "NO SIBLING/oc_ XREF in $n"
done

# G1 YAML frontmatter (whole folder)
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5/G6/G8 after incremental reindex
bash scripts/update_notes_database.sh
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
for n in ${=NOTES}; do
  [ "${indeg:-0}" -ge 1 ] || echo "G8 FAIL: $n in_degree=${indeg:-0}"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_tavily | concept | 230 | 0 | ✅ (≪2500w / ≪6 code) |
| 2 | oc_plugins_reference_telegram | concept | 230 | 0 | ✅ |
| 3 | oc_plugins_reference_tencent | concept | 230 | 0 | ✅ |
| 4 | oc_plugins_reference_tlon | concept | 230 | 0 | ✅ |
| 5 | oc_plugins_reference_together | concept | 230 | 0 | ✅ |
| 6 | oc_plugins_reference_tokenjuice | concept | 230 | 0 | ✅ |
| 7 | oc_plugins_reference_tts_local_cli | concept | 220 | 0 | ✅ |

No note approaches any cap (largest is ~230w vs 2500w cap; 0 code fences vs 6 cap). Source cards are 47–62w;
digest notes are larger only because of the Overview framing + ≥6-link Related Notes connectivity layer. No
split or merge warranted.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `0_entry_points/entry_openclaw_docs.md` (master W1 pre-step; >30 master total ⇒ a
dedicated docs hub is required and created before the first sub-plan executes), under the **Plugins → Reference**
cluster. Each new note receives its `entry_openclaw_docs.md` back-link at finalization (this is the primary G7/G8
inbound-link source). No standalone entry point is created for this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all sources confirmed to exist):
- `entry_openclaw_docs.md` (planned, master W1) → **all 7 notes** (primary anti-island source).
- `repo_openclaw_extensions` ✓ → notes 1, 2, 3, 4, 5, 6, 7 (the plugin/extension framework hosting these plugins).
- `repo_openclaw_extensions_llm_providers` ✓ → notes 3, 5 (provider plugins).
- `repo_openclaw_extensions_voice_speech` ✓ → note 7 (speech provider plugin).
- `repo_openclaw_channels` ✓ / `repo_openclaw_channels_messaging` ✓ → notes 2, 4 (channel plugins).
- `repo_hermes_agent_tools` ✓ → notes 1, 6 (tool-contributing plugins).
- `term_text_to_speech` ✓ → note 7; `term_compaction` ✓ → note 6; `term_provider_plugin` ✓ → notes 3, 5;
  `term_function_calling` ✓ → note 1.

## Pacing Rules (inherited from master)

One execution phase, 7 notes. Cap dynamic-workflow fan-out at ~30 agents/run (this batch is well under). Re-read
each source card before authoring; reproduce package id / install route / Surface contracts verbatim. One BB
(`concept`) per note. Reindex incrementally after the wave; verify `note_links` + 0 broken links + in-degree ≥1
before commit. `git pull --rebase --autostash origin main` first; commit + push per wave; **no Claude co-author
trailer**.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment at raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment:** per-note Related Notes mapping locked at RAISED FLOORS (≥8 terms · ≥10 snippets ·
Cross-References` candidate pools with `## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`.
All 7 source cards were re-read from `inbox/openclaw_docs/plugins/reference/` on 2026-06-21 to keep selection

**What was locked (per-note counts — all verified by an independent parse of the file + DB existence check):**

| Note | Terms | Snippets | Docs | Existing docs | Repos+entry | Floors met |
|---|---:|---:|---:|---:|---:|---|
| oc_plugins_reference_tavily | 9 | 13 | 12 | 9 | 6 | ✅ |
| oc_plugins_reference_telegram | 9 | 13 | 12 | 9 | 7 | ✅ |
| oc_plugins_reference_tencent | 9 | 12 | 12 | 9 | 7 | ✅ |
| oc_plugins_reference_tlon | 9 | 12 | 12 | 9 | 7 | ✅ |
| oc_plugins_reference_together | 9 | 12 | 12 | 8 | 7 | ✅ |
| oc_plugins_reference_tokenjuice | 9 | 12 | 12 | 9 | 6 | ✅ |
| oc_plugins_reference_tts_local_cli | 9 | 12 | 12 | 8 | 6 | ✅ |

**Verification performed (2026-06-21):**
  verification was `snippet_openclaw_memory_search` — not present; replaced by the existing
  `snippet_openclaw_agents_memory_search`).
- ALL cited `resources/documentation/` existing docs exist (the only candidate dropped was
  `cc_web_search_tool` — not present; the web/search facet is covered by `hermes_web_search_*`, `cc_web_overview`,
  `cc_built_in_tools`, `cc_mcp_tool_search`).
- Planned sibling `oc_*` deep pages (e.g. `oc_tools_tavily`, `oc_channels_telegram`, `oc_providers_tencent`,
  `oc_concepts_compaction`, `oc_tools_tts`) confirmed ABSENT from the DB → correctly marked "(planned, …)" and
  existing docs, well above the 5-existing minimum).
- Source re-read (CP7): body-only word counts 24–34/page (47–62 incl. YAML summary frontmatter); 216–391 total —
  all tiny stub cards, far below every density cap (no under-estimation; the plan's figure is conservative-high).

**New-term candidates / glossary best-fit:** **NONE.** The Undigested Terms Plan's outcome (0 new
`term_dictionary` captures) is re-confirmed at this augment — every facet (web-search, channel, provider,
middleware/compaction, TTS) maps either to an `oc_*` doc note (this batch or a deep-page sub-plan) or to an
doc pages, not new glossary entries; the only `term_dictionary` interaction is linking existing terms. The
Step 2d re-scan surfaced no genuinely cross-cutting vault-reusable term lacking an existing home (the
agentic/LLM glossary already supplies `term_channel_adapter`, `term_messaging_gateway`, `term_provider_routing`,
`term_model_router`, `term_voice_mode`, `term_voice_call`, etc., all newly wired into the per-note lists). No
glossary file therefore requires editing for this sub-plan (W5 obligation = 0).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + ≥10 snippets + ≥10 docs floors, each with relevance statement) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; parse confirms every note 9t/12–13s/12d with existing_docs ≥8; every link carries `— <what>; relevance: <why>`. Floors exceeded for all 7. |
| CP2 | 9-GATE present per batch (G1–G6 + G7/G8 discoverability) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost, G6 Broken-link, G7 Discoverability, G8 in-degree≥1; single P3 phase; G1+G5+G6 runnable via `/tessellum-validate-note-gates` at batch close. |
| CP4 | Size | **PASS** | 7 planned notes (≪30 cap); single execution phase; no split needed (all cards 24–62 words). |
| CP5 | Format derived (not invented) | **PASS** | Format Definition inherited verbatim from master, which was derived from the existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora (`## Overview` / `## Related Notes` / `## References` / bold `**Source**`/`**Last Updated**`/`**Status**` footer; YAML field order tags→keywords→topics→language→date of note→status→building_block→source_url→access_control_group). |
| CP6 | Density / BB atomicity | **PASS** | One `concept` BB per note; ~220–230 digest words each (vs 2500w cap); 0 code fences (vs 6 cap); no borderline note → no proactive split. |
| CP7 | Sources measured | **PASS** | 7 source cards re-read 2026-06-21: body words 24–34/page, 47–62 incl. YAML; total 216–391 — measured, conservative-high, no >1.5× under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (outcome: 0 new captures, every row dispositioned to existing term/repo OR an `oc_*` doc note); `## Term-Note Authoring Requirements` present (N/A — 0 new terms; multi-source mandate cited if Step 2d re-scan ever surfaces one). |
| CP8f | Slug specificity / collision audit | **PASS** | 0 new `term_*` slugs ⇒ no specificity rename needed; collision audit generalized to all 7 planned `oc_*` doc notes — each fronts a distinct plugin-reference card with no existing `term_*` or `documentation/` duplicate (deep pages are owned by to07/to08/ch05/pr08/co02/co07/nd02 sub-plans, linked not recreated). |
| CP9 | Discoverability / inlinks (G8 executed, no graph islands) | **PASS** | `## Inlinks (existing notes → new notes)` maps ≥1 outside-folder inbound link to ALL 7 notes (`entry_openclaw_docs` primary; `repo_openclaw_extensions` → all 7; facet repos/terms → relevant notes); G8 in-degree≥1 check in the gate table + Validation Scripts. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
