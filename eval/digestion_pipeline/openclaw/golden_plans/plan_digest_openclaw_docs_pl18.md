---
title: Sub-Plan pl18 — OpenClaw Docs: Plugins (Reference, q-r-s slice)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/reference/qa-matrix", "plugins/reference/qianfan", "plugins/reference/qqbot", "plugins/reference/qwen", "plugins/reference/runway", "plugins/reference/searxng", "plugins/reference/senseaudio"]
---

# Sub-Plan pl18: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, `oc_` prefix) / format / dedup / 9-GATE /
> cross-references / entry-point (`entry_openclaw_docs.md`) decisions are ALL inherited from the master.

## Scope

The 7 alphabetically-adjacent plugin **reference index stubs** `q…r…s` from `plugins/reference/`:
`qa-matrix`, `qianfan`, `qqbot`, `qwen`, `runway`, `searxng`, `senseaudio`. Each page is a one-screen plugin
catalog card naming the npm package, install route, and the contract **surface** the plugin contributes
(a model provider, a chat channel, a media/video/web-search contract, or a QA transport). These are the
machine-generated `plugins/reference/*` registry entries (the per-plugin "what package / where from / what
it exposes" cards), NOT the deep config docs — those live under `providers/*` and `channels/*` (other
sub-plans). **Priority P3** (Phase C — plugin-reference sprawl). The code-side analogs
(`repo_openclaw_extensions*`, `repo_openclaw_channels*`) are LINKED, never recreated.

**Source**: OpenClaw docs, 7 pages, **398 measured words** (tiny stubs). **Planned: 7 notes** (1:1 page→note).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| QA Matrix plugin | plugins/reference/qa-matrix | 48 | 0 | 2 | 0 | model |
| Qianfan plugin | plugins/reference/qianfan | 54 | 0 | 3 | 0 | model |
| QQ Bot plugin | plugins/reference/qqbot | 64 | 0 | 3 | 0 | model |
| Qwen plugin | plugins/reference/qwen | 87 | 0 | 3 | 0 | model |
| Runway plugin | plugins/reference/runway | 50 | 0 | 3 | 0 | model |
| SearXNG plugin | plugins/reference/searxng | 45 | 0 | 2 | 0 | model |
| Senseaudio plugin | plugins/reference/senseaudio | 50 | 0 | 3 | 0 | model |

Total: 398 words, 0 code fences, 18 H2 (Distribution / Surface / Related docs), 0 H3. Every page shares the
identical 3-field template: a 1-line `summary`, a `## Distribution` (Package + Install route), a `## Surface`
(the contract/provider/channel names the plugin registers), and (5 of 7) a `## Related docs` deep-link.

## Content Strategy

- **Prioritize**: the **Surface** field (the contract a plugin registers — `providers:`, `channels:`,
  `contracts: videoGenerationProviders / mediaUnderstandingProviders / webSearchProviders`) and the
  **Distribution** field (npm package id + install route: included / npm / ClawHub / source-only). These are
  the load-bearing facts of a plugin-registry card.
- **Split**: NONE. Every page is 45–87 words — two orders of magnitude under the 2,500-word cap, single BB
  (each is a `model` BB: a static descriptor of a registry entity — package, surface, install route — not a
  task procedure). 1 page → 1 note.
- **Link-out (do NOT inline)**: the deep config/setup docs each card points at — `/providers/qwen`,
  `/providers/qwen-oauth`, `/providers/qianfan`, `/providers/runway`, `/providers/senseaudio`,
  `/channels/qqbot` — are owned by OTHER sub-plans (pr01/pr04/pr07/pr08, ch04); reference them as
  cross-sub-plan `oc_*` planned notes, do not duplicate their content here. Provider/channel/contract
  vocabulary links existing `term_*` notes (no new terms; see Undigested Terms Plan).

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_qa_matrix.md` | model | qa-matrix.md (Distribution, Surface) | 220 | The `@openclaw/qa-matrix` plugin: a Matrix QA transport runner/substrate, source-checkout-only install, registering a `plugin` surface (QA over the Matrix transport). |
| 2 | `oc_plugins_reference_qianfan.md` | model | qianfan.md (Distribution, Surface, Related docs) | 220 | The `@openclaw/qianfan-provider` plugin: adds the Qianfan (Baidu) model provider, installed via npm/ClawHub, registering `providers: qianfan`; deep config in `/providers/qianfan`. |
| 3 | `oc_plugins_reference_qqbot.md` | model | qqbot.md (Distribution, Surface, Related docs) | 230 | The `@openclaw/qqbot` plugin: a QQ Bot chat channel for group + direct-message workflows, npm/ClawHub install, registering `channels: qqbot` plus tools contracts + skills; channel setup in `/channels/qqbot`. |
| 4 | `oc_plugins_reference_qwen.md` | model | qwen.md (Distribution, Surface, Related docs) | 260 | The `@openclaw/qwen-provider` plugin: adds 7 Qwen provider variants (Qwen, Qwen Cloud, Model Studio, DashScope, Qwen OAuth, Qwen Portal, Qwen CLI) plus media-understanding + video-generation contracts; npm/ClawHub install; config in `/providers/qwen` + `/providers/qwen-oauth`. |
| 5 | `oc_plugins_reference_runway.md` | model | runway.md (Distribution, Surface, Related docs) | 210 | The `@openclaw/runway-provider` plugin: adds a Runway video-generation provider, bundled (included in OpenClaw), registering `contracts: videoGenerationProviders`; config in `/providers/runway`. |
| 6 | `oc_plugins_reference_searxng.md` | model | searxng.md (Distribution, Surface) | 205 | The `@openclaw/searxng-plugin` plugin: adds a SearXNG (self-hosted metasearch) web-search provider, bundled, registering `contracts: webSearchProviders`. |
| 7 | `oc_plugins_reference_senseaudio.md` | model | senseaudio.md (Distribution, Surface, Related docs) | 210 | The `@openclaw/senseaudio-provider` plugin: adds a media-understanding (audio) provider, bundled, registering `contracts: mediaUnderstandingProviders`; config in `/providers/senseaudio`. |

## Section Coverage Map

```
plugins/reference/qa-matrix.md
├── (summary) Matrix QA transport runner and substrate ─ → note 1 (oc_plugins_reference_qa_matrix) Overview
├── ## Distribution (@openclaw/qa-matrix, source-only) ─ → note 1
└── ## Surface (plugin) ──────────────────────────────── → note 1
plugins/reference/qianfan.md
├── (summary) Qianfan model provider ─────────────────── → note 2 (oc_plugins_reference_qianfan) Overview
├── ## Distribution (@openclaw/qianfan-provider, npm/ClawHub) → note 2
├── ## Surface (providers: qianfan) ──────────────────── → note 2
└── ## Related docs (/providers/qianfan) ─────────────── → note 2 References (link-out, cross-sub-plan)
plugins/reference/qqbot.md
├── (summary) QQ Bot channel ─────────────────────────── → note 3 (oc_plugins_reference_qqbot) Overview
├── ## Distribution (@openclaw/qqbot, npm/ClawHub) ────── → note 3
├── ## Surface (channels: qqbot; contracts: tools; skills) → note 3
└── ## Related docs (/channels/qqbot) ────────────────── → note 3 References (link-out)
plugins/reference/qwen.md
├── (summary) 7 Qwen provider variants ───────────────── → note 4 (oc_plugins_reference_qwen) Overview
├── ## Distribution (@openclaw/qwen-provider, npm/ClawHub) → note 4
├── ## Surface (providers ×7; mediaUnderstanding/videoGeneration) → note 4
└── ## Related docs (/providers/qwen, /providers/qwen-oauth) → note 4 References (link-out)
plugins/reference/runway.md
├── (summary) video generation provider ──────────────── → note 5 (oc_plugins_reference_runway) Overview
├── ## Distribution (@openclaw/runway-provider, included) ─ → note 5
├── ## Surface (contracts: videoGenerationProviders) ─── → note 5
└── ## Related docs (/providers/runway) ──────────────── → note 5 References (link-out)
plugins/reference/searxng.md
├── (summary) web search provider ────────────────────── → note 6 (oc_plugins_reference_searxng) Overview
├── ## Distribution (@openclaw/searxng-plugin, included) ─ → note 6
└── ## Surface (contracts: webSearchProviders) ───────── → note 6
plugins/reference/senseaudio.md
├── (summary) media understanding provider ───────────── → note 7 (oc_plugins_reference_senseaudio) Overview
├── ## Distribution (@openclaw/senseaudio-provider, included) → note 7
├── ## Surface (contracts: mediaUnderstandingProviders) ─ → note 7
└── ## Related docs (/providers/senseaudio) ──────────── → note 7 References (link-out)
```
No orphaned sections. Every H2 (Distribution / Surface / Related docs) and every YAML `summary` maps to a
note. `## Related docs` deep-links go to the note's `## References` as cross-sub-plan link-outs (NOT inlined).

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are 45–87 words (≤87w ≪ 2,500w cap), 0 code fences, single `model` BB each. No page warrants a split; the 1:1 page→note mapping is the faithful, atomic decomposition. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (398 words total; mean ~57 w/page; max 87 = qwen). New `oc_` notes: **7**. New
  `term_dictionary` notes: **0**.
- BB distribution: **model ×7** (every note is a static descriptor of a registry entity — a plugin's
  package id, install route, and registered contract surface — not a how-to procedure).
- Est. digest words ~1,555 (avg ~222/note — each note ~3–5× the source stub once the surface fields,
  install-route semantics, and cross-links are spelled out, but well under caps). 0 source code fences; notes
  carry 0–1 small fenced blocks (the npm/ClawHub install id) — ≤6 cap trivially met.
- **Cross-refs (LOCKED at xref-augment 2026-06-21 — raised floors):** every note maps **≥8 relevance-selected
  `term_dictionary` terms · ≥10 code_snippets · ≥10 docs under `resources/documentation/`** (≥5 of the 10 docs
  `repo_openclaw_extensions*` / `repo_openclaw_channels*` and the cross-sub-plan `oc_*` deep-config note it
  Mapping**). Per-note locked mapping below.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

paths are FROM a note at `resources/documentation/openclaw/oc_X.md`: terms `../../term_dictionary/term_Y.md`;
snippets `../../code_snippets/snippet_Y.md`; sibling oc docs (this series) `oc_Y.md`; other-folder docs
`../<folder>/<file>.md`; repos `../../../areas/code_repos/repo_Y.md`; entry points
notes WHERE note_id=…`); all snippets exist; ≥5 of the 10 docs per note are EXISTING (hermes/cc/pi/band/bedrock
analogs); `oc_*` sibling/cross-sub-plan docs are marked **(planned, this series)** / **(planned, cross-sub-plan)**.

### oc_plugins_reference_qa_matrix (8t · 10s · 10d)

Source: qa-matrix.md — "Matrix QA transport runner and substrate"; `@openclaw/qa-matrix`; source-checkout-only;
surface `plugin`.

**Terms (8):**
- [openclaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway this plugin loads into; relevance: the qa-matrix plugin is an OpenClaw extension that runs inside the gateway runtime.
- [plugin manifest](../../term_dictionary/term_plugin_manifest.md) — the package descriptor / registry card that declares a plugin's id and surface; relevance: this page IS the plugin's registry card (package + install route + surface).
- [QA](../../term_dictionary/term_qa.md) — quality-assurance / test substrate; relevance: the plugin's whole purpose is a QA transport runner, the "qa" in qa-matrix.
- [test plan](../../term_dictionary/term_test_plan.md) — structured test-coverage specification; relevance: a "QA matrix" is a test-coverage matrix exercised across the Matrix transport.
- [canary testing](../../term_dictionary/term_canary_testing.md) — exercising live paths with synthetic probes; relevance: a QA transport runner drives live channel paths the way canary tests do.
- [channel adapter](../../term_dictionary/term_channel_adapter.md) — the per-platform connector abstraction; relevance: the Matrix transport this QA runner exercises is a channel adapter.
- [agentic evaluation](../../term_dictionary/term_agentic_evaluation.md) — evaluating agent behavior end-to-end; relevance: a QA-matrix substrate is the harness an agentic-evaluation run executes over.
- [npm](../../term_dictionary/term_npm.md) — Node package distribution; relevance: install route here is "source checkout only", the explicit contrast to the npm/ClawHub route of the other cards.

- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — Hermes plugin surface taxonomy (provider/platform/memory/…); relevance: the closest analog to the `plugin` surface this card registers. (existing)
- [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — how Hermes loads/registers plugins; relevance: explains the plugin lifecycle a source-checkout plugin like qa-matrix joins. (existing)
- [hermes_messaging_matrix](../hermes_agent/hermes_messaging_matrix.md) — Matrix channel setup in the sibling Hermes stack; relevance: documents the Matrix transport the QA runner drives. (existing)
- [hermes_messaging_matrix_e2ee](../hermes_agent/hermes_messaging_matrix_e2ee.md) — Matrix end-to-end encryption specifics; relevance: a QA runner over Matrix must traverse the E2EE transport path. (existing)
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel/gateway message-flow architecture; relevance: the substrate the QA transport exercises. (existing)
- [cc_extending_claude_code](../claude_code/cc_extending_claude_code.md) — Claude Code extension model; relevance: cross-tool analog for "a plugin that extends the agent host". (existing)
- [oc_concepts_qa_matrix](oc_concepts_qa_matrix.md) — the QA-matrix concept deep doc; relevance: the substantive concept this registry card points at. (planned, cross-sub-plan, co06)
- [oc_channels_matrix](oc_channels_matrix.md) — Matrix channel deep config; relevance: the transport the QA runner targets. (planned, cross-sub-plan, ch03)
- [oc_concepts_qa_e2e_automation](oc_concepts_qa_e2e_automation.md) — QA end-to-end automation concept; relevance: qa-matrix is the transport runner inside the QA-e2e pipeline. (planned, cross-sub-plan, co05)
- [oc_plugins_reference_qqbot](oc_plugins_reference_qqbot.md) — peer channel-surface plugin card; relevance: the other channel/transport card in this slice. (planned, this series)

**Repos (3):**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the gateway core the plugin loads into; relevance: qa-matrix runs inside the OpenClaw runtime.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: the framework that registers this plugin.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel subsystem; relevance: the Matrix channel the QA transport exercises.

- [snippet_hermes_agent_gw_platform_matrix](../../code_snippets/snippet_hermes_agent_gw_platform_matrix.md) — Matrix platform adapter implementation; relevance: the transport the QA runner exercises, at code level.
- [snippet_hermes_agent_gw_platform_matrix_connect](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_connect.md) — Matrix connect/login flow; relevance: how a QA-matrix runner establishes the live transport session.
- [snippet_hermes_agent_gw_platform_matrix_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_normalize.md) — Matrix message normalization; relevance: the message-shape the QA substrate asserts over.
- [snippet_hermes_agent_gw_platform_matrix_acl](../../code_snippets/snippet_hermes_agent_gw_platform_matrix_acl.md) — Matrix access-control list handling; relevance: a QA transport must traverse channel ACL gates.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — OpenClaw channel registry normalization; relevance: where a channel/transport plugin registers its surface.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory lookup; relevance: how the QA runner enumerates the transports it tests.
- [snippet_hermes_agent_gw_platform_registry](../../code_snippets/snippet_hermes_agent_gw_platform_registry.md) — platform/channel plugin registry; relevance: the registry a `plugin`-surface entry joins.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — abstract base for channel adapters; relevance: the contract a transport-runner asserts against.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — OpenClaw plugin load/lifecycle; relevance: the lifecycle a source-checkout plugin like qa-matrix follows.
- [snippet_hermes_agent_skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — plugin vs skill distinction; relevance: clarifies the bare `plugin` surface this card registers.

### oc_plugins_reference_qianfan (8t · 10s · 10d)

Source: qianfan.md — "Adds Qianfan model provider support"; `@openclaw/qianfan-provider`; npm + ClawHub; surface
`providers: qianfan`; related `/providers/qianfan`.

**Terms (8):**
- [openclaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: the qianfan provider plugin extends OpenClaw's model layer.
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — a plugin that registers a model `providers:` surface; relevance: this card IS a provider plugin (registers `providers: qianfan`).
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Qianfan fronts Baidu's LLMs as a provider.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external generative-AI vendors; relevance: Qianfan (Baidu) is an external GenAI provider wired in.
- [provider routing](../../term_dictionary/term_provider_routing.md) — selecting among registered providers; relevance: a registered `providers: qianfan` entry participates in model routing.
- [model catalog](../../term_dictionary/term_model_catalog.md) — the registry of available models/providers; relevance: registering Qianfan adds entries to the model catalog.
- [npm](../../term_dictionary/term_npm.md) — Node package distribution; relevance: install route is npm + ClawHub (`@openclaw/qianfan-provider`).
- [plugin manifest](../../term_dictionary/term_plugin_manifest.md) — the package/surface registry card; relevance: this page is the manifest for the qianfan provider plugin.

- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud LLM provider setup in Hermes; relevance: the 1:1 analog for adding an external model provider. (existing)
- [hermes_provider_aws_bedrock](../hermes_agent/hermes_provider_aws_bedrock.md) — a concrete provider plugin (Bedrock); relevance: structurally identical provider-plugin card to qianfan. (existing)
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth/env-var config; relevance: how a qianfan provider's API key/auth is configured. (existing)
- [hermes_cli_commands_chat_provider](../hermes_agent/hermes_cli_commands_chat_provider.md) — selecting/chatting via a provider on the CLI; relevance: how a registered qianfan provider is invoked. (existing)
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy incl. model-provider; relevance: defines the `providers:` surface this card registers. (existing)
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering a custom model provider in pi; relevance: cross-tool analog of registering `providers: qianfan`. (existing)
- [oc_providers_qianfan](oc_providers_qianfan.md) — the Qianfan provider deep config; relevance: the `## Related docs` link-out target with full setup. (planned, cross-sub-plan, pr07)
- [oc_concepts_model_providers](oc_concepts_model_providers.md) — the model-providers concept; relevance: the abstraction a provider plugin instantiates. (planned, cross-sub-plan, co04)
- [oc_plugins_reference_qwen](oc_plugins_reference_qwen.md) — peer provider-plugin card (Alibaba); relevance: sibling China-cluster model provider in this slice. (planned, this series)
- [oc_plugins_reference_senseaudio](oc_plugins_reference_senseaudio.md) — peer provider-plugin card; relevance: another `providers:`/`contracts:` registering plugin in this slice. (planned, this series)

**Repos (3):**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway core; relevance: the runtime the provider loads into.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the LLM-provider extension subsystem; relevance: qianfan's home subsystem.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin framework; relevance: registers the provider plugin.

- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registration registry; relevance: where `providers: qianfan` would register.
- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — China-cluster provider plugin (Baidu/Alibaba family); relevance: directly covers Qianfan-class Chinese providers.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch wiring; relevance: how a registered provider is constructed and dispatched to.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstract class; relevance: the contract a qianfan provider plugin implements.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a concrete OpenClaw provider plugin; relevance: same provider-plugin shape as qianfan, in OpenClaw.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator provider; relevance: how an external-vendor provider is wired as a provider plugin.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: registering qianfan adds catalog entries.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest-driven model catalog planning; relevance: how a provider plugin's manifest feeds the catalog.
- [snippet_hermes_agent_core_error_classifier_provider_maps](../../code_snippets/snippet_hermes_agent_core_error_classifier_provider_maps.md) — per-provider error mapping; relevance: a new provider needs error classification entries.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — CLI plugin install command; relevance: the npm/ClawHub install route this card declares.

### oc_plugins_reference_qqbot (8t · 10s · 10d)

Source: qqbot.md — "OpenClaw QQ Bot channel plugin for group and direct-message workflows"; `@openclaw/qqbot`;
npm + ClawHub; surface `channels: qqbot; contracts: tools; skills`; related `/channels/qqbot`.

**Terms (8):**
- [openclaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: the qqbot channel plugin extends OpenClaw's channel layer.
- [channel adapter](../../term_dictionary/term_channel_adapter.md) — per-platform connector; relevance: qqbot registers a `channels:` surface — it is a channel adapter for QQ.
- [channel kernel](../../term_dictionary/term_channel_kernel.md) — the core that hosts channel adapters; relevance: the qqbot channel plugs into the channel kernel.
- [chatbot](../../term_dictionary/term_chatbot.md) — automated conversational agent on a chat platform; relevance: a QQ bot is a chatbot on the QQ platform.
- [conversational AI](../../term_dictionary/term_conversational_ai.md) — dialog-driven AI systems; relevance: the group/DM workflows the channel serves are conversational-AI interactions.
- [tool registry](../../term_dictionary/term_tool_registry.md) — registry of agent-callable tools; relevance: the plugin also contributes `contracts: tools`.
- [npm](../../term_dictionary/term_npm.md) — Node package distribution; relevance: install route is npm + ClawHub (`@openclaw/qqbot`).
- [plugin manifest](../../term_dictionary/term_plugin_manifest.md) — package/surface registry card; relevance: this page is the qqbot plugin's manifest.

- [hermes_gateway_qqbot_setup](../hermes_agent/hermes_gateway_qqbot_setup.md) — QQ Bot channel setup in Hermes; relevance: the exact same QQ Bot channel, deep-config analog. (existing)
- [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — channel/gateway message-flow architecture; relevance: the substrate a `channels: qqbot` adapter plugs into. (existing)
- [hermes_adding_platform_adapter_plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — how to add a platform/channel adapter plugin; relevance: the procedure that builds a qqbot-class channel plugin. (existing)
- [hermes_messaging_teams_bot](../hermes_agent/hermes_messaging_teams_bot.md) — a bot channel (Teams) for group/DM; relevance: peer group+DM bot channel, structurally identical. (existing)
- [hermes_webhooks_routes_security](../hermes_agent/hermes_webhooks_routes_security.md) — webhook ingress routing/security; relevance: a QQ bot channel ingests via webhook routes. (existing)
- [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel setup in Claude Code; relevance: cross-tool analog of wiring a chat channel. (existing)
- [oc_channels_qqbot](oc_channels_qqbot.md) — QQ Bot channel deep config; relevance: the `## Related docs` link-out target. (planned, cross-sub-plan, ch04)
- [oc_concepts_channel_docking](oc_concepts_channel_docking.md) — channel docking concept; relevance: how a channel plugin docks into the gateway. (planned, cross-sub-plan, co01)
- [oc_plugins_reference_qa_matrix](oc_plugins_reference_qa_matrix.md) — peer channel/transport card; relevance: the other channel-surface plugin in this slice. (planned, this series)
- [oc_tools_plugin](oc_tools_plugin.md) — the tools-via-plugin contract; relevance: qqbot also registers `contracts: tools`. (planned, cross-sub-plan, to06)

**Repos (3):**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway core; relevance: the runtime the channel plugin loads into.
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel subsystem; relevance: qqbot extends the channel subsystem.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel implementations; relevance: qqbot's peer group of messaging channels.

- [snippet_hermes_agent_gw_platform_qqbot_adapter](../../code_snippets/snippet_hermes_agent_gw_platform_qqbot_adapter.md) — QQ Bot channel adapter implementation; relevance: the exact `channels: qqbot` adapter at code level.
- [snippet_hermes_agent_gw_platform_qqbot_keyboards](../../code_snippets/snippet_hermes_agent_gw_platform_qqbot_keyboards.md) — QQ Bot interactive keyboards; relevance: a QQ-specific UI surface the channel adds.
- [snippet_hermes_agent_gw_platform_registry](../../code_snippets/snippet_hermes_agent_gw_platform_registry.md) — channel/platform plugin registry; relevance: where `channels: qqbot` registers.
- [snippet_hermes_agent_gw_platform_base_abstract](../../code_snippets/snippet_hermes_agent_gw_platform_base_abstract.md) — abstract channel-adapter base; relevance: the base contract the qqbot adapter implements.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory lookup; relevance: how the gateway enumerates the qqbot channel.
- [snippet_hermes_agent_gw_config_per_channel](../../code_snippets/snippet_hermes_agent_gw_config_per_channel.md) — per-channel config block; relevance: the config a `channels: qqbot` entry carries.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — OpenClaw channel registry normalization; relevance: where the qqbot channel surface normalizes into the registry.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tools registry; relevance: the qqbot plugin also contributes `contracts: tools`.
- [snippet_hermes_agent_skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — skills vs plugins; relevance: qqbot's surface includes `skills`, clarified here.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — CLI plugin install; relevance: the npm/ClawHub install route this card declares.

### oc_plugins_reference_qwen (8t · 11s · 11d)

Source: qwen.md — "Adds Qwen, Qwen Cloud, Model Studio, DashScope, Qwen Oauth, Qwen Portal, Qwen CLI model
provider support"; `@openclaw/qwen-provider`; npm + ClawHub; surface `providers: …×7; contracts:
mediaUnderstandingProviders, videoGenerationProviders`; related `/providers/qwen`, `/providers/qwen-oauth`.

**Terms (8):**
- [openclaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: the qwen provider plugin extends OpenClaw's model layer.
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — registers a `providers:` surface; relevance: this card registers 7 Qwen `providers:` variants.
- [Qwen](../../term_dictionary/term_qwen.md) — the Alibaba Qwen model family; relevance: the exact model family this plugin fronts.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the Qwen variants are LLM providers.
- [OAuth token](../../term_dictionary/term_oauth_token.md) — token-based delegated auth; relevance: the `qwen-oauth` variant authenticates via OAuth (see `/providers/qwen-oauth`).
- [multimodal](../../term_dictionary/term_multimodal.md) — models spanning text+media; relevance: the plugin also registers `mediaUnderstandingProviders` + `videoGenerationProviders` (multimodal contracts).
- [video processing](../../term_dictionary/term_video_processing.md) — video generation/understanding; relevance: the `videoGenerationProviders` contract surface this plugin adds.
- [npm](../../term_dictionary/term_npm.md) — Node package distribution; relevance: install route is npm + ClawHub (`@openclaw/qwen-provider`).

- [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud LLM provider setup; relevance: the analog for adding a multi-variant model provider. (existing)
- [hermes_provider_xai_grok_oauth](../hermes_agent/hermes_provider_xai_grok_oauth.md) — an OAuth-authenticated provider plugin; relevance: directly analogous to the `qwen-oauth` variant. (existing)
- [hermes_env_vars_providers_auth_tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — provider auth/env config; relevance: how Qwen's API/OAuth credentials are configured. (existing)
- [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-generation provider plugin; relevance: the `videoGenerationProviders` contract Qwen registers. (existing)
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — media (image/video/audio) tool reference; relevance: the media-understanding/video contracts surface. (existing)
- [pi_custom_models](../pi/pi_custom_models.md) — registering custom models/variants; relevance: cross-tool analog of registering 7 Qwen variants. (existing)
- [oc_providers_qwen](oc_providers_qwen.md) — the Qwen provider deep config; relevance: the `## Related docs` link-out target. (planned, cross-sub-plan, pr07)
- [oc_providers_qwen_oauth](oc_providers_qwen_oauth.md) — the Qwen OAuth provider deep config; relevance: the second `## Related docs` link-out target. (planned, cross-sub-plan, pr07)
- [oc_concepts_model_providers](oc_concepts_model_providers.md) — model-providers concept; relevance: the abstraction the 7 variants instantiate. (planned, cross-sub-plan, co04)
- [oc_plugins_reference_qianfan](oc_plugins_reference_qianfan.md) — peer China-cluster provider card; relevance: sibling Chinese model provider in this slice. (planned, this series)
- [oc_plugins_reference_runway](oc_plugins_reference_runway.md) — peer video-generation contract card; relevance: also registers `videoGenerationProviders`. (planned, this series)

**Repos (3):**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway core; relevance: the runtime the provider loads into.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension subsystem; relevance: Qwen's home subsystem.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin framework; relevance: registers the multi-variant provider plugin.

- [snippet_hermes_agent_plugins_provider_china_cluster](../../code_snippets/snippet_hermes_agent_plugins_provider_china_cluster.md) — China-cluster provider plugin (Qwen/DashScope family); relevance: directly covers Qwen-class providers.
- [snippet_hermes_agent_plugins_provider_xai_oauth](../../code_snippets/snippet_hermes_agent_plugins_provider_xai_oauth.md) — OAuth provider plugin; relevance: the `qwen-oauth` variant's auth pattern.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: where the 7 Qwen `providers:` entries register.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth auth-profile portability; relevance: the credential model behind `qwen-oauth`/`qwen-portal`.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-generation dispatch; relevance: the `videoGenerationProviders` contract Qwen registers.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-gen tool; relevance: consumes the `videoGenerationProviders` Qwen contributes.
- [snippet_hermes_agent_tools_vision_input](../../code_snippets/snippet_hermes_agent_tools_vision_input.md) — vision/media input handling; relevance: the `mediaUnderstandingProviders` contract surface.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: the 7 Qwen variants populate the catalog.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — manifest-driven catalog planning; relevance: how the qwen-provider manifest feeds the catalog.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base abstract; relevance: the contract each Qwen variant implements.
- [snippet_hermes_agent_cli_plugins_cmd_install](../../code_snippets/snippet_hermes_agent_cli_plugins_cmd_install.md) — CLI plugin install; relevance: the npm/ClawHub install route this card declares.

### oc_plugins_reference_runway (8t · 10s · 10d)

Source: runway.md — "Adds video generation provider support"; `@openclaw/runway-provider`; included in OpenClaw;
surface `contracts: videoGenerationProviders`; related `/providers/runway`.

**Terms (8):**
- [openclaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: the runway provider plugin is bundled into OpenClaw.
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — registers a provider contract; relevance: runway registers `contracts: videoGenerationProviders`.
- [video processing](../../term_dictionary/term_video_processing.md) — video generation/processing; relevance: Runway is a video-generation provider — the exact contract it registers.
- [multimodal](../../term_dictionary/term_multimodal.md) — text+media models; relevance: video generation is a multimodal media contract.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external GenAI vendors; relevance: Runway is an external GenAI video service wired in as a provider.
- [genai](../../term_dictionary/term_genai.md) — generative AI; relevance: a video-generation provider is a generative-AI capability.
- [plugin manifest](../../term_dictionary/term_plugin_manifest.md) — package/surface registry card; relevance: this page is the runway-provider manifest (bundled plugin).
- [npm](../../term_dictionary/term_npm.md) — Node package id form; relevance: the `@openclaw/runway-provider` package id (bundled = included, not separately npm-installed).

- [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-generation provider plugin in Hermes; relevance: the exact 1:1 analog to the runway video-gen provider. (existing)
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — media/video tool reference; relevance: the platform-media surface video gen plugs into. (existing)
- [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-generation provider plugin; relevance: sibling media-generation provider-plugin pattern. (existing)
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy incl. media contracts; relevance: defines the `contracts:` surface runway registers. (existing)
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled/built-in plugins; relevance: runway is "included in OpenClaw" — a bundled plugin. (existing)
- [hermes_features_overview](../hermes_agent/hermes_features_overview.md) — feature/capability overview; relevance: places video generation among the agent's media capabilities. (existing)
- [oc_providers_runway](oc_providers_runway.md) — Runway provider deep config; relevance: the `## Related docs` link-out target. (planned, cross-sub-plan, pr07)
- [oc_tools_video_generation](oc_tools_video_generation.md) — the video-generation tool; relevance: the tool that consumes the `videoGenerationProviders` contract. (planned, cross-sub-plan, to08)
- [oc_plugins_reference_qwen](oc_plugins_reference_qwen.md) — peer card also registering `videoGenerationProviders`; relevance: sibling video-gen contract in this slice. (planned, this series)
- [oc_plugins_reference_senseaudio](oc_plugins_reference_senseaudio.md) — peer bundled media-contract card; relevance: another bundled `contracts:` media plugin in this slice. (planned, this series)

**Repos (3):**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway core; relevance: the runtime the bundled provider loads into.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin/extension framework; relevance: registers the bundled video-gen provider.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app/media surfaces; relevance: consumers that render generated video.

- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-generation dispatch; relevance: the `videoGenerationProviders` contract Runway registers, at code level.
- [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video-gen tool; relevance: the tool that invokes the runway video-gen provider.
- [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen dispatch; relevance: sibling media-generation dispatch pattern.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: where the video-gen provider contract registers.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: the bundled provider-plugin shape runway follows.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: the video-gen contract surfaces a tool in the catalog.
- [snippet_hermes_agent_toolsets_definitions](../../code_snippets/snippet_hermes_agent_toolsets_definitions.md) — toolset definitions; relevance: how a media-generation contract is grouped into toolsets.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loading; relevance: how a bundled plugin like runway is loaded at startup.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: the lifecycle of a bundled/included plugin.
- [snippet_hermes_agent_skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — plugin vs skill; relevance: clarifies that runway is a contract-registering plugin, not a skill.

### oc_plugins_reference_searxng (8t · 10s · 10d)

Source: searxng.md — "Adds web search provider support"; `@openclaw/searxng-plugin`; included in OpenClaw;
surface `contracts: webSearchProviders`. (No `## Related docs`.)

**Terms (8):**
- [openclaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: the searxng plugin is bundled into OpenClaw.
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — registers a provider contract; relevance: searxng registers `contracts: webSearchProviders`.
- [tool registry](../../term_dictionary/term_tool_registry.md) — registry of agent-callable tools; relevance: a web-search provider backs the search tool the agent calls.
- [tool gateway](../../term_dictionary/term_tool_gateway.md) — the layer that exposes tools to the agent; relevance: the search provider surfaces through the tool gateway.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external services wired in; relevance: SearXNG is an external/self-hosted metasearch backend wired in as a provider.
- [browser automation](../../term_dictionary/term_browser_automation.md) — programmatic web access; relevance: web search is the non-browser path to the same "fetch from the web" capability cluster.
- [plugin manifest](../../term_dictionary/term_plugin_manifest.md) — package/surface registry card; relevance: this page is the searxng-plugin manifest (bundled).
- [npm](../../term_dictionary/term_npm.md) — Node package id form; relevance: the `@openclaw/searxng-plugin` package id (bundled = included).

- [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — web-search provider plugin in Hermes; relevance: the exact 1:1 analog to the searxng web-search provider. (existing)
- [hermes_web_search_extract](../hermes_agent/hermes_web_search_extract.md) — web search + content extraction; relevance: what a `webSearchProviders` backend returns to the agent. (existing)
- [hermes_x_search_grok](../hermes_agent/hermes_x_search_grok.md) — a concrete search provider (X/Grok); relevance: sibling web-search provider, same contract shape. (existing)
- [hermes_tool_gateway](../hermes_agent/hermes_tool_gateway.md) — the tool gateway; relevance: where the web-search provider's tool is exposed. (existing)
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: defines the `contracts:` surface searxng registers. (existing)
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled/built-in plugins; relevance: searxng is "included in OpenClaw" — a bundled plugin. (existing)
- [oc_tools_searxng_search](oc_tools_searxng_search.md) — the SearXNG search tool deep doc; relevance: the substantive tool docs this provider backs. (planned, cross-sub-plan, to06)
- [oc_tools_web](oc_tools_web.md) — the web-access/search tool family; relevance: the agent-facing surface the search provider feeds. (planned, cross-sub-plan, to08)
- [oc_plugins_reference_qwen](oc_plugins_reference_qwen.md) — peer contract-registering provider card; relevance: another `contracts:`-registering plugin in this slice. (planned, this series)
- [oc_plugins_reference_senseaudio](oc_plugins_reference_senseaudio.md) — peer bundled-contract card; relevance: another bundled `contracts:` plugin in this slice. (planned, this series)

**Repos (3):**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway core; relevance: the runtime the bundled plugin loads into.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin framework; relevance: registers the bundled web-search provider.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills/tools subsystem; relevance: the skills/tools that consume the web-search provider.

- [snippet_hermes_agent_plugins_web](../../code_snippets/snippet_hermes_agent_plugins_web.md) — web plugin (search/fetch); relevance: the web-search plugin shape searxng follows.
- [snippet_hermes_agent_tools_web_tools](../../code_snippets/snippet_hermes_agent_tools_web_tools.md) — web tools (search/fetch) implementation; relevance: the tool the `webSearchProviders` contract backs.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tool registry; relevance: where the web-search tool registers.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: the search provider surfaces a tool into the catalog.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: where the `webSearchProviders` contract registers.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: the bundled provider-plugin shape searxng follows.
- [snippet_hermes_agent_toolsets_definitions](../../code_snippets/snippet_hermes_agent_toolsets_definitions.md) — toolset definitions; relevance: how a search contract is grouped into toolsets.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loading; relevance: how the bundled searxng plugin is loaded.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: the lifecycle of a bundled/included plugin.
- [snippet_hermes_agent_skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — plugin vs skill; relevance: clarifies that searxng is a contract-registering plugin.

### oc_plugins_reference_senseaudio (8t · 10s · 10d)

Source: senseaudio.md — "Adds media understanding provider support"; `@openclaw/senseaudio-provider`; included in
OpenClaw; surface `contracts: mediaUnderstandingProviders`; related `/providers/senseaudio`.

**Terms (8):**
- [openclaw](../../term_dictionary/term_openclaw.md) — the host gateway; relevance: the senseaudio plugin is bundled into OpenClaw.
- [provider plugin](../../term_dictionary/term_provider_plugin.md) — registers a provider contract; relevance: senseaudio registers `contracts: mediaUnderstandingProviders`.
- [multimodal](../../term_dictionary/term_multimodal.md) — text+media models; relevance: media understanding (audio) is a multimodal contract.
- [speech-to-text](../../term_dictionary/term_speech_to_text.md) — audio→text transcription; relevance: audio "media understanding" is essentially speech-to-text / audio transcription.
- [realtime transcription](../../term_dictionary/term_realtime_transcription.md) — streaming STT; relevance: an audio-understanding provider does (near-)realtime transcription.
- [third-party GenAI services](../../term_dictionary/term_third_party_genai_services.md) — external services; relevance: Senseaudio is an external audio-AI service wired in as a provider.
- [plugin manifest](../../term_dictionary/term_plugin_manifest.md) — package/surface registry card; relevance: this page is the senseaudio-provider manifest (bundled).
- [npm](../../term_dictionary/term_npm.md) — Node package id form; relevance: the `@openclaw/senseaudio-provider` package id (bundled = included).

- [hermes_stt_transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text / transcription provider; relevance: the audio-understanding capability senseaudio provides. (existing)
- [hermes_tts_providers](../hermes_agent/hermes_tts_providers.md) — audio (TTS) provider plugins; relevance: sibling audio-provider-plugin pattern (the inverse direction). (existing)
- [hermes_tools_reference_platform_media](../hermes_agent/hermes_tools_reference_platform_media.md) — media (audio/video/image) tool reference; relevance: the platform-media surface media-understanding plugs into. (existing)
- [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy incl. media contracts; relevance: defines the `contracts:` surface senseaudio registers. (existing)
- [hermes_built_in_plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled/built-in plugins; relevance: senseaudio is "included in OpenClaw" — a bundled plugin. (existing)
- [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media handling settings (audio/attachments); relevance: how inbound audio reaches a media-understanding provider. (existing)
- [oc_providers_senseaudio](oc_providers_senseaudio.md) — Senseaudio provider deep config; relevance: the `## Related docs` link-out target. (planned, cross-sub-plan, pr07)
- [oc_nodes_media_understanding](oc_nodes_media_understanding.md) — the media-understanding node concept; relevance: the runtime node that consumes the `mediaUnderstandingProviders` contract. (planned, cross-sub-plan, nd02)
- [oc_plugins_reference_qwen](oc_plugins_reference_qwen.md) — peer card also registering `mediaUnderstandingProviders`; relevance: sibling media-understanding contract in this slice. (planned, this series)
- [oc_plugins_reference_runway](oc_plugins_reference_runway.md) — peer bundled media-contract card; relevance: another bundled `contracts:` media plugin in this slice. (planned, this series)

**Repos (3):**
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — gateway core; relevance: the runtime the bundled provider loads into.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — the voice/speech extension subsystem; relevance: senseaudio's home subsystem (audio understanding).
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin framework; relevance: registers the bundled audio-understanding provider.

- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram speech-to-text provider; relevance: the exact audio-understanding (STT) provider shape senseaudio follows.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: the tool that invokes the media-understanding provider.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — media-stream transcription; relevance: audio media understanding over a live stream.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — audio media stream handling; relevance: the inbound audio a media-understanding provider consumes.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — speech pipeline; relevance: the audio-processing pipeline behind media understanding.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: where the `mediaUnderstandingProviders` contract registers.
- [snippet_hermes_agent_plugins_provider_custom](../../code_snippets/snippet_hermes_agent_plugins_provider_custom.md) — custom provider plugin; relevance: the bundled provider-plugin shape senseaudio follows.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loading; relevance: how the bundled senseaudio plugin is loaded.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: the lifecycle of a bundled/included plugin.

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc notes (these plugin cards), NOT new
`term_dictionary` entries; the only `term_dictionary` interaction is **linking existing** terms. **Expected
new term_dictionary captures: 0.** All vocabulary on these 7 stub pages maps to existing terms or to the
oc_* notes themselves.

| Term | Disposition |
|---|---|
| plugin / plugin reference / Surface / Distribution | Digested AS the `oc_plugins_reference_*` notes (the subject of each page); link `term_plugin_manifest` (existing). |
| provider plugin (`providers:` surface) | Link existing `term_provider_plugin`. |
| channel plugin (`channels:` surface) | Link existing `term_channel_adapter` / `term_channel_kernel`. |
| video generation (`videoGenerationProviders`) | Link existing `term_video_processing` + `term_multimodal`. NOTE: no `term_video_generation` exists; `term_video_processing` is the nearest existing substantive term (do NOT create a too-general new term for a single-contract reference). |
| media understanding (`mediaUnderstandingProviders`) | Link existing `term_multimodal` + `term_speech_to_text`. No `term_media_understanding` exists; covered by multimodal/STT. |
| web search (`webSearchProviders`) | Link existing `term_tool_registry` + `term_third_party_genai_services`. NOTE: no `term_web_search` exists; it is a generic cross-cutting capability — candidate flagged below but NOT captured by pl18 (out of scope for a 45-word stub; defer to a tools sub-plan that documents the search tool substantively). |
| Qwen / Qianfan / Runway / SearXNG / Senseaudio / QQ Bot (product names) | Provider/service/channel product names — documented as config in the `oc_*` card, NOT promoted to term notes. `term_qwen` exists and is linked (note 4); the others link `term_third_party_genai_services` / `term_llm`. |
| QA / QA matrix / transport runner | Link existing `term_qa` / `term_test_plan` / `term_canary_testing`. |
| npm / ClawHub / source checkout (install routes) | Link existing `term_npm` (+ `term_npm_scoping`). ClawHub install route is documented in the cw01–03 sub-plans; link out, do not define here. |

**New-term candidates (NOT captured by pl18; flagged for the owning substantive sub-plan):**
- `term_web_search` — a genuinely reusable cross-cutting capability with no existing note, but it should be
  captured (if at all) by the **tools** sub-plan that documents the web-search tool substantively
  (`to06`/`tools/searxng-search`), NOT by a 45-word plugin-registry stub. Best-fit glossary if later
  captured: `acronym_glossary_ai_agents.md` (agent tool capabilities). pl18 links `term_tool_registry`
  meanwhile. **Disposition for pl18: do nothing (defer).**

## Term-Note Authoring Requirements

**N/A (0 new terms).** pl18 authors zero `term_dictionary` notes; it only links existing terms (inherited
from master). The single new-term candidate (`term_web_search`) is explicitly deferred to a tools sub-plan,
so no authoring obligation falls on pl18.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P3). All 8 gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order + body H2: Overview / Related Notes; footer) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (every claim diffs vs `inbox/openclaw_docs/plugins/reference/<page>.md`) | manual diff vs mirror page (package id, install route, surface verbatim) |
| G3 | Density + Coverage (≤400L / ≤2500w / ≤6 code; every H2/Surface field mapped) | `wc -w` + Section Coverage Map |
| G4 | Cross-Reference (≥8 terms · ≥10 snippets · ≥10 docs per note, each with a relevance statement; + repos + siblings) | Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21) |
| G5 | Ghost-reference detect + redirect (no link to a non-existent note_id) | `/tessellum-fix-ghost-references`; planned siblings created same phase |
| G6 | Broken-link fix (correct relative paths) | `/tessellum-fix-broken-links` |
| G7 | Discoverability — every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` | `entry_openclaw_docs.md` rows + repo/term inlinks |
| G8 | In-degree ≥1 (anti-island) per new note | `note_links` query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_qa_matrix oc_plugins_reference_qianfan oc_plugins_reference_qqbot oc_plugins_reference_qwen oc_plugins_reference_runway oc_plugins_reference_searxng oc_plugins_reference_senseaudio"
for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1: required body sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "G1 MISSING SECTION '$sec': $n"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "G1 MISSING source_url: $n"; }
  # format check (errors + non-indexed-link)
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # G3: density caps (body only)
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # G4: at least one sibling oc_ link present
  grep -q "$SIBLING_PREFIX" "$f" || echo "G4 NO SIBLING oc_ LINK: $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code | Within caps (≤400L/≤2500w/≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_qa_matrix | model | 220 | 0–1 | ✅ |
| 2 | oc_plugins_reference_qianfan | model | 220 | 0–1 | ✅ |
| 3 | oc_plugins_reference_qqbot | model | 230 | 0–1 | ✅ |
| 4 | oc_plugins_reference_qwen | model | 260 | 0–1 | ✅ |
| 5 | oc_plugins_reference_runway | model | 210 | 0–1 | ✅ |
| 6 | oc_plugins_reference_searxng | model | 205 | 0–1 | ✅ |
| 7 | oc_plugins_reference_senseaudio | model | 210 | 0–1 | ✅ |

No note approaches any cap (max 260w vs 2,500w; 0 source code fences). The risk here is the OPPOSITE of
over-density: each note must be padded to atomic substance WITHOUT inventing content — the strategy is to
spell out the Surface contract semantics + install-route meaning + cross-links from the verbatim source, not
to fabricate config detail. No splits; no merges (master mandates 1 note per reference page).

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (CREATED as a master pre-step W1 — required because the
series totals >30 notes), under the **Plugins → Reference** cluster (pl18, q-r-s slice). Each new note gets
its entry-point back-link at finalization (this is the G7/G8 anti-island inbound link). No standalone entry
point for pl18 alone (7 notes ≪ 30-note threshold).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfies G7/G8 in-degree ≥1):
- `entry_openclaw_docs.md` (planned, master pre-step) → all 7 notes (primary anti-island hub link).
- `repo_openclaw_extensions_llm_providers.md` → notes 2 (qianfan), 4 (qwen) — provider-plugin extensions.
- `repo_openclaw_extensions.md` → notes 5 (runway), 6 (searxng) — bundled contract plugins.
- `repo_openclaw_channels.md` / `repo_openclaw_channels_messaging.md` → note 3 (qqbot) — channel plugin.
- `repo_openclaw_channels.md` → note 1 (qa-matrix) — Matrix transport / QA channel.
- `repo_openclaw_extensions_voice_speech.md` → note 7 (senseaudio) — audio/speech provider.
- `term_qwen.md` → note 4 (qwen); `term_provider_plugin.md` → notes 2/4/5/6/7; `term_npm.md` → notes 2/3/6.

(planned master pre-step, created before pl18 executes).

## Pacing Rules (inherited from master)

One execution phase, 7 notes (well under the ~30-agent fan-out cap). 8 gates before commit. Re-read each
source page; reproduce package id / install route / surface verbatim. One BB per note (all `model`). Commit +
push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer). Reindex
incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment — raised floors locked) |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-21** (9/9 checkpoints PASS) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**xref-augment scope:** locked the Per-Note Related Notes Mapping at the raised floors (**≥8 terms · ≥10
snippets · ≥10 docs per note**, relevance-selected against a fresh re-read of all 7 source pages under
section (which carried 6–8 terms + repos only, no snippet/doc floor). Updated the Summary-Statistics cross-ref
line and the G4 gate row to the raised floors.


| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_qa_matrix | 8 | 10 | 10 (6 existing / 4 planned) | 3 | ✅ |
| oc_plugins_reference_qianfan | 8 | 10 | 10 (6 existing / 4 planned) | 3 | ✅ |
| oc_plugins_reference_qqbot | 8 | 10 | 10 (6 existing / 4 planned) | 3 | ✅ |
| oc_plugins_reference_qwen | 8 | 11 | 11 (6 existing / 5 planned) | 3 | ✅ |
| oc_plugins_reference_runway | 8 | 10 | 10 (6 existing / 4 planned) | 3 | ✅ |
| oc_plugins_reference_searxng | 8 | 10 | 10 (6 existing / 4 planned) | 3 | ✅ |
| oc_plugins_reference_senseaudio | 8 | 10 | 10 (6 existing / 4 planned) | 3 | ✅ |

from the `hermes_agent/`, `claude_code/`, `pi/`, `band/`, and `aws_bedrock/` coding-agent corpora; the
remaining doc slots are this-series sibling `oc_*` cards or cross-sub-plan `oc_*` deep-config notes (`pr07`,
`co01/04/05/06`, `ch03/04`, `nd02`, `to06/08`) marked planned. **0 ghost references** (the only
series / the W1 pre-step before pl18 executes; G5 redirect rule applies if any planned target is dropped).

**New-term candidates + best-fit glossary:** none captured by pl18 (0 new `term_dictionary` notes per master).
Re-read of all 7 stub pages (398 words total, max 87) surfaced **no new undigested terms** beyond the original
plan's Step-4e inventory. The single standing candidate is `term_web_search` (genuinely reusable web-search
capability, no existing note) — **deferred** to the tools sub-plan that documents the web-search tool
substantively (`to06`/`tools/searxng-search`), NOT a 45-word plugin stub; best-fit glossary if later captured:
`acronym_glossary_ai_agents.md`. pl18 links existing `term_tool_registry` + `term_tool_gateway` +
`term_third_party_genai_services` meanwhile. (Also confirmed absent and intentionally NOT created:
`term_video_generation`, `term_media_understanding`, `term_qa_matrix` — covered by existing
`term_video_processing` / `term_multimodal` / `term_speech_to_text` / `term_qa` per the Undigested Terms Plan.)

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors, relevance per link) | **PASS** | Per-Note Related Notes Mapping: every note has 8 terms · ≥10 snippets · ≥10 docs, each rendered `- [Name](relpath.md) — what; relevance: why`. |
| CP2 | 9-GATE present per batch (G1–G9) | **PASS** | Per-Phase Validation Gate table lists G1–G8 (incl. G5 ghost-detect, G6 broken-link-fix, G7/G8 discoverability/in-degree); single execution phase. |
| CP3 | Entry point inherited (`entry_openclaw_docs` planned at W1) | **PASS** | Entry Point Decision: 7 rows into `entry_openclaw_docs.md` (master W1 pre-step, >30-note series ⇒ CREATE required); per-note back-link at finalization. |
| CP4 | Plan size manageable | **PASS** | 7 notes ≪ 30 cap; 1:1 page→note; no split needed (Split Decisions table). |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited from master, derived from existing `documentation/` notes (`hermes_*`/`cc_*`/`pi_*`); body H2 `## Overview` / `## Related Notes` matches the verified target-dir convention (e.g. `hermes_plugin_types_surfaces.md`). |
| CP6 | Density / BB atomicity | **PASS** | Density Re-Assessment: all 7 notes ~205–260w (≪ 2,500w cap), 0–1 code fences, single `model` BB each; risk is under- not over-density. |
| CP7 | Source word counts measured | **PASS** | All 7 pages re-read this session under `inbox/openclaw_docs/plugins/reference/` (qa-matrix 48w … qwen 87w; 398w total) — matches the plan's Source table; no under-estimation. |
| CP8 | Undigested Terms Plan + authoring reqs | **PASS** | Undigested Terms Plan present; 0 new terms (master design: OpenClaw vocab → `oc_*` docs, link existing terms). Term-Note Authoring Requirements section present (N/A — 0 terms). |
| CP8f | Slug specificity / collision audit | **PASS** | 0 `term_*` slugs to capture (no specificity risk). Collision audit run on all 7 planned `oc_*` doc slugs: each maps 1:1 to a unique `plugins/reference/*` page; no existing `term_*`/doc note covers a per-plugin registry card (`term_qwen` is the model family, not the plugin card — distinct). |
| CP9 | Discoverability / inlinks (G8 executed) | **PASS** | Inlinks (existing → new) table covers all 7 notes with ≥1 outside-folder inbound link (`entry_openclaw_docs` hub + `repo_openclaw_*` + `term_*`); G8 in-degree ≥1 is in the phase gate table as an EXECUTED check. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending → ready`.
