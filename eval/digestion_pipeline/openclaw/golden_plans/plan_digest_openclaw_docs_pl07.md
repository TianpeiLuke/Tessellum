---
title: Sub-Plan pl07 — OpenClaw Docs: Plugins (canvas, cerebras, chutes, clickclack, cloudflare-ai-gateway, codex, codex-supervisor)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - plugins/reference/canvas
  - plugins/reference/cerebras
  - plugins/reference/chutes
  - plugins/reference/clickclack
  - plugins/reference/cloudflare-ai-gateway
  - plugins/reference/codex
  - plugins/reference/codex-supervisor
---

# Sub-Plan pl07: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`) / format / dedup (term_dictionary + documentation/ + `repo_openclaw*`) / 9-GATE / cross-refs / entry-point (`entry_openclaw_docs.md`) decisions are ALL inherited from the master; this file holds only the per-note plan for its 7 assigned `plugins/reference/*` pages.

## Scope

The first 7 alphabetical `plugins/reference/*` stub pages of the Plugins section: the one-page-per-plugin
reference cards for **canvas** (experimental UI surface), **cerebras / chutes / cloudflare-ai-gateway** (model-provider
plugins), **clickclack** (a chat-channel plugin), **codex** (a Codex app-server harness + GPT-catalog provider plugin),
and **codex-supervisor** (supervise Codex app-server sessions). Each card states the plugin summary, its npm/ClawHub
**Distribution** package, the contract **Surface** it implements (`providers` / `channels` / `contracts` such as `tools`),
and a **Related docs** pointer to the deeper provider/channel/harness page. **Priority P3 (Phase C — plugin reference
sprawl).** The code-side counterparts (`repo_openclaw_extensions_llm_providers`, `repo_openclaw_channels`,
`repo_openclaw_apps`, the codex provider snippets) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **454 measured words** (all stub cards). **Planned: 7 notes (1 per page).**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| canvas | /plugins/reference/canvas | 55 | 0 | 2 | 0 | procedure |
| cerebras | /plugins/reference/cerebras | 54 | 0 | 3 | 0 | procedure |
| chutes | /plugins/reference/chutes | 54 | 0 | 3 | 0 | procedure |
| clickclack | /plugins/reference/clickclack | 62 | 0 | 3 | 0 | procedure |
| cloudflare-ai-gateway | /plugins/reference/cloudflare-ai-gateway | 62 | 0 | 3 | 0 | procedure |
| codex | /plugins/reference/codex | 69 | 0 | 3 | 0 | procedure |
| codex-supervisor | /plugins/reference/codex-supervisor | 98 | 0 | 3 | 0 | procedure |

H2 set per page (measured): all carry `## Distribution` + `## Surface`; all except `canvas` add `## Related docs`;
`codex-supervisor` additionally has `## Session Listing` (a 1-paragraph runtime note about `codex_sessions_list`,
`include_stored`, the 200/1000 stored-session cap). No page has any H3 or any code fence (`Code` = 0 throughout).

## Content Strategy

- **Prioritize**: faithfully digest the load-bearing facts of each card — the **npm package name**, the **install
  route** (npm + ClawHub `clawhub:` slug, or "included in OpenClaw"), the **contract surface** (which provider/channel/
  contract it registers), and the codex-supervisor `## Session Listing` operational detail (it is the only non-boilerplate
  prose). These cards are how an operator discovers/audits which plugin owns a capability.
- **Do NOT split**: every page is a 54–98-word stub far under the 2,500-word / 400-line / 6-code caps and is
  single-BB (procedure = install/configure/audit one plugin). One note per page (master "most reference pages = 1 note").
- **Do NOT over-expand**: these are intentionally thin. Each `oc_*` note's `## Overview` + body mirrors the card 1:1;
  the substance (provider config, channel setup, harness internals) lives in the deeper pages the card points to and is
  reached via `## Related Notes`. Do not invent configuration steps the source does not contain.
- **Link-out (do not duplicate)**: the `Related docs` targets — `/providers/cerebras` (→ `pr01`), `/providers/chutes`
  + `/providers/cloudflare-ai-gateway` (→ `pr02`), `/channels/clickclack` (→ `ch01`), `/plugins/codex-harness`
  (→ `pl02`) — are other sub-plans' notes; cite as "(planned, OpenClaw docs)" in cross-refs, do not inline.
- **Dedup-before-create**: ran the three-way check (bm25 + dense + filename grep) across `term_dictionary/`,
  `resources/documentation/`, and `areas/code_repos/repo_openclaw*`. No existing `oc_*` doc note for any of these 7
  plugins (the `openclaw/` doc folder does not yet exist); the related provider/channel/codex content lives on the CODE
  side (`repo_openclaw_extensions_llm_providers`, `repo_openclaw_channels`, `repo_openclaw_apps`, codex snippets) and is
  LINKED, not recreated. Outcome for all 7 candidates: **(1) no note → create.**

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_canvas.md` | procedure | canvas.md: Distribution, Surface | 230 | The Canvas plugin reference: an experimental Canvas-control / A2UI rendering surface for paired nodes, packaged as `@openclaw/canvas-plugin`, included in OpenClaw, registering the `tools` contract surface. |
| 2 | `oc_plugins_reference_cerebras.md` | procedure | cerebras.md: Distribution, Surface, Related docs | 230 | The Cerebras provider plugin reference: adds the `cerebras` model provider, packaged as `@openclaw/cerebras-provider`, installed via npm or ClawHub (`clawhub:@openclaw/cerebras-provider`); points to the Cerebras provider config page. |
| 3 | `oc_plugins_reference_chutes.md` | procedure | chutes.md: Distribution, Surface, Related docs | 230 | The Chutes provider plugin reference: adds the `chutes` model provider, packaged as `@openclaw/chutes-provider`, installed via npm or ClawHub (`clawhub:@openclaw/chutes-provider`); points to the Chutes provider config page. |
| 4 | `oc_plugins_reference_clickclack.md` | procedure | clickclack.md: Distribution, Surface, Related docs | 230 | The Clickclack channel plugin reference: adds the `clickclack` channel surface for sending/receiving OpenClaw messages, packaged as `@openclaw/clickclack`, included in OpenClaw; points to the Clickclack channel config page. |
| 5 | `oc_plugins_reference_cloudflare_ai_gateway.md` | procedure | cloudflare-ai-gateway.md: Distribution, Surface, Related docs | 230 | The Cloudflare AI Gateway provider plugin reference: adds the `cloudflare-ai-gateway` model provider, packaged as `@openclaw/cloudflare-ai-gateway-provider`, installed via npm or ClawHub; points to the Cloudflare AI Gateway provider config page. |
| 6 | `oc_plugins_reference_codex.md` | procedure | codex.md: Distribution, Surface, Related docs | 240 | The Codex plugin reference: an OpenClaw Codex app-server harness + model-provider plugin with a Codex-managed GPT catalog, packaged as `@openclaw/codex`, installed via npm/ClawHub; registers the `codex` provider plus `mediaUnderstandingProviders`, `migrationProviders`, `webSearchProviders` contracts; points to the codex-harness page. |
| 7 | `oc_plugins_reference_codex_supervisor.md` | procedure | codex-supervisor.md: Distribution, Surface, Session Listing | 290 | The Codex Supervisor plugin reference: supervises Codex app-server sessions from OpenClaw, packaged as `@openclaw/codex-supervisor`, included in OpenClaw, registering the `tools` contract; documents `codex_sessions_list` (loaded-only by default; `include_stored` for stored history via Codex's state-DB listing path; stored cap 200, raisable to 1000 via `max_stored_sessions`). |

Filename derivation (master rule): `oc_` + full slug with `/` and `-` → `_`. E.g. `plugins/reference/cloudflare-ai-gateway`
→ `oc_plugins_reference_cloudflare_ai_gateway.md`; `plugins/reference/codex-supervisor` → `oc_plugins_reference_codex_supervisor.md`.
No split-aspect suffixes (no page splits — see Split Decisions).

## Section Coverage Map

```
canvas.md
├── (intro summary) ──────────────────── → note 1 (oc_plugins_reference_canvas) ## Overview
├── ## Distribution (pkg, install route) → note 1
└── ## Surface (contracts: tools) ────── → note 1
cerebras.md
├── (intro summary) ──────────────────── → note 2 (oc_plugins_reference_cerebras) ## Overview
├── ## Distribution ──────────────────── → note 2
├── ## Surface (providers: cerebras) ─── → note 2
└── ## Related docs (/providers/cerebras) → note 2 ## Related Notes (link-out → pr01)
chutes.md
├── (intro summary) ──────────────────── → note 3 (oc_plugins_reference_chutes) ## Overview
├── ## Distribution ──────────────────── → note 3
├── ## Surface (providers: chutes) ───── → note 3
└── ## Related docs (/providers/chutes) ─ → note 3 ## Related Notes (link-out → pr02)
clickclack.md
├── (intro summary) ──────────────────── → note 4 (oc_plugins_reference_clickclack) ## Overview
├── ## Distribution ──────────────────── → note 4
├── ## Surface (channels: clickclack) ── → note 4
└── ## Related docs (/channels/clickclack) → note 4 ## Related Notes (link-out → ch01)
cloudflare-ai-gateway.md
├── (intro summary) ──────────────────── → note 5 (oc_plugins_reference_cloudflare_ai_gateway) ## Overview
├── ## Distribution ──────────────────── → note 5
├── ## Surface (providers: cloudflare-ai-gateway) → note 5
└── ## Related docs (/providers/cloudflare-ai-gateway) → note 5 ## Related Notes (link-out → pr02)
codex.md
├── (intro summary) ──────────────────── → note 6 (oc_plugins_reference_codex) ## Overview
├── ## Distribution ──────────────────── → note 6
├── ## Surface (providers: codex; contracts: media/migration/webSearch) → note 6
└── ## Related docs (/plugins/codex-harness) → note 6 ## Related Notes (link-out → pl02)
codex-supervisor.md
├── (intro summary) ──────────────────── → note 7 (oc_plugins_reference_codex_supervisor) ## Overview
├── ## Distribution ──────────────────── → note 7
├── ## Surface (contracts: tools) ────── → note 7
└── ## Session Listing (codex_sessions_list, include_stored, 200/1000 cap) → note 7 (dedicated H2)
```
No orphaned sections. Every H2 (and the intro summary) of every page maps to its single note. The `Related docs`
pointers are realized as link-out entries in each note's `## Related Notes` (to other OpenClaw doc sub-plans), not as
inlined content.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are 54–98-word single-BB stub cards, far below the 2,500-word / 400-line / 6-code split thresholds and not mixed-BB. One note per page per the master "most reference pages = 1 note" rule. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (454 measured words total; range 54–98 each). New `oc_*` notes: **7** (1 per page). New
  `term_dictionary` notes: **0** (see Undigested Terms Plan).
- BB distribution: **procedure ×7** (each note = install / configure / audit one plugin). No concept/model/argument notes.
- Code fences in source: **0** across all 7 pages; each note may include ≤1 short fenced block to show the npm/ClawHub
  install command verbatim (well under the ≤6 cap).
- Est. digest words: **~1,680** (avg ~240/note) — these are deliberately thin reference notes; the depth lives in the
  linked provider/channel/harness sub-plans.
- Cross-refs (LOCKED at xref-augment 2026-06-21 — raised floors): every note maps **≥8 relevance-selected
  `band_*`; remainder sibling `oc_*` "planned, this series") PLUS relevant `repo_openclaw*`. All EXISTING `term_*`/`repo_*`/
  **## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)** below.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

**Standard:** `>=8 terms · >=10 snippets · >=10 docs per note`, relevance-selected (re-read source; no padding),
(`cc_*`/`hermes_*`/`band_*`). Rendered in the note's `## Related Notes` as
`- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`. Relative paths from
`resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/…`; cc → `../claude_code/…`;
hermes → `../hermes_agent/…`; band → `../band/…`; repo → `../../../areas/code_repos/…`; snippet → `../../code_snippets/…`;
sibling oc → `oc_….md`; entry → `../../../0_entry_points/entry_openclaw_docs.md`.

The not-existing proper-noun terms the plan deliberately does NOT cite (DB-confirmed GHOST, depth reached via link-out
sibling `oc_*`): `term_cerebras`, `term_chutes`, `term_cloudflare`, `term_codex`, `term_openai_codex`, `term_channel`,
`term_clickclack`, `term_supervisor`, `term_canvas`, `term_plugin`, `term_model_provider`.

### oc_plugins_reference_canvas (8t · 12s · 11d)

**Terms** (8, existing):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway this is a plugin for; relevance: the canvas plugin is an OpenClaw extension.
- [A2UI](../../term_dictionary/term_a2ui.md) — agent-to-UI rendering protocol; relevance: the card names "A2UI rendering surfaces" as canvas's core capability.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the per-plugin declaration of package + surface; relevance: `@openclaw/canvas-plugin` ships a manifest declaring its `tools` surface.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the OpenClaw extension SDK plugins build on; relevance: canvas is authored against the plugin SDK.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — the runtime registry contracts/tools register into; relevance: canvas registers the `tools` contract surface.
- [WebSocket](../../term_dictionary/term_websocket.md) — the gateway's bidirectional transport; relevance: paired-node canvas surfaces stream control/render over the gateway WS.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool-invocation mechanism; relevance: the `tools` contract canvas registers is invoked via function calling.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agents OpenClaw fronts; relevance: canvas is an experimental UI surface for those paired agent nodes.

**Docs** (11; 8 existing + 3 planned):
- [Claude Code: Channels Overview](../claude_code/cc_channels_overview.md) — surfaces/channels model for a coding agent; relevance: closest precedent for a plugin-registered runtime surface. (existing)
- [Claude Code: Build a Channel](../claude_code/cc_build_a_channel.md) — authoring a runtime surface plugin; relevance: parallel to authoring the canvas surface. (existing)
- [Claude Code: Computer Use](../claude_code/cc_computer_use.md) — agent UI/screen-control surface; relevance: canvas control is OpenClaw's analog of a visual control surface. (existing)
- [Claude Code: Computer Use Safety](../claude_code/cc_computer_use_safety.md) — guardrails for a control surface; relevance: experimental canvas control raises the same safety considerations. (existing)
- [Claude Code: Plugins Overview](../claude_code/cc_plugins_overview.md) — what a plugin is and how it extends the agent; relevance: frames canvas as a bundled plugin. (existing)
- [Claude Code: Plugin Components](../claude_code/cc_plugin_components.md) — the component surfaces a plugin can ship; relevance: canvas ships a `tools` component. (existing)
- [Hermes: Built-in Plugins](../hermes_agent/hermes_built_in_plugins.md) — bundled (included) plugins in a sibling harness; relevance: canvas is "included in OpenClaw" — a built-in plugin. (existing)
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — the surface taxonomy plugins register; relevance: maps the `tools`/UI surface canvas uses. (existing)
- [oc_plugins_reference_codex_supervisor](oc_plugins_reference_codex_supervisor.md) — sibling reference card also registering `contracts: tools`; relevance: same surface shape. (planned, this series)
- [oc_refactor_canvas](oc_refactor_canvas.md) — the canvas refactor design page (`rx01`); relevance: deeper canvas-surface architecture this card points toward. (planned, this series)
- [oc_plugins_reference](oc_plugins_reference.md) — the plugin-reference index (`pl05`); relevance: the cluster hub this card belongs to. (planned, this series)

**Repos** (3, existing):
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — OpenClaw app/UI surface code; relevance: hosts canvas/A2UI rendering surfaces. (existing)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: loads `@openclaw/canvas-plugin`. (existing)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the gateway hosting node pairing + transport; relevance: carries the paired-node canvas WS transport. (existing)

**Snippets** (12, existing):
- [snippet_openclaw_macos_canvas_lifecycle](../../code_snippets/snippet_openclaw_macos_canvas_lifecycle.md) — macOS canvas surface lifecycle impl; relevance: the runtime behind the canvas control surface.
- [snippet_openclaw_macos_canvas_filewatcher](../../code_snippets/snippet_openclaw_macos_canvas_filewatcher.md) — canvas file-watch/render trigger; relevance: how canvas re-renders A2UI on change.
- [snippet_openclaw_kit_gateway_channel_ws](../../code_snippets/snippet_openclaw_kit_gateway_channel_ws.md) — gateway WS channel a paired node uses; relevance: the transport canvas surfaces render over.
- [snippet_openclaw_kit_gateway_node_session](../../code_snippets/snippet_openclaw_kit_gateway_node_session.md) — node session binding over the gateway; relevance: canvas is a per-paired-node surface bound to a node session.
- [snippet_openclaw_gateway_ws_connection](../../code_snippets/snippet_openclaw_gateway_ws_connection.md) — gateway WS connection handling; relevance: underpins the canvas paired-node stream.
- [snippet_openclaw_gateway_nodes_pairing](../../code_snippets/snippet_openclaw_gateway_nodes_pairing.md) — node pairing flow; relevance: canvas surfaces target "paired nodes".
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load lifecycle; relevance: how the canvas plugin is loaded.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package + surface contract; relevance: declares canvas's `tools` surface.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: canvas's entry registration.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway plugin config resolution; relevance: how a bundled plugin like canvas is enabled.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin loader; relevance: loads canvas at gateway startup.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — the runtime tool catalog; relevance: where canvas's `tools` contract surfaces land.

### oc_plugins_reference_cerebras (9t · 12s · 12d)

**Terms** (9, existing):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: cerebras is an OpenClaw provider plugin.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin that registers a model provider; relevance: cerebras registers the `cerebras` provider surface.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: cerebras serves LLM inference to OpenClaw.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the discovered set of available models; relevance: the cerebras provider feeds models into the catalog.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted model APIs; relevance: Cerebras is a third-party inference service.
- [npm](../../term_dictionary/term_npm.md) — the JS package registry/installer; relevance: install route is `npm` (plus ClawHub).
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + surface declaration; relevance: `@openclaw/cerebras-provider` ships one declaring `providers: cerebras`.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the extension SDK; relevance: the provider plugin is built on it.
- [Model Router](../../term_dictionary/term_model_router.md) — routes calls across providers; relevance: cerebras becomes a routable provider once registered.

**Docs** (12; 7 existing + 5 planned):
- [Claude Code: Model Selection](../claude_code/cc_model_selection.md) — picking a provider's model; relevance: cerebras adds selectable cerebras models. (existing)
- [Claude Code: Fallback Models](../claude_code/cc_fallback_models.md) — provider/model failover; relevance: cerebras participates in the fallback ladder. (existing)
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — how a provider plugin is added in a sibling harness; relevance: exact analog of registering cerebras. (existing)
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin authoring spec; relevance: the shape `@openclaw/cerebras-provider` follows. (existing)
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — catalog of cloud providers; relevance: Cerebras is a cloud inference provider. (existing)
- [Hermes: Provider Routing](../hermes_agent/hermes_provider_routing.md) — routing across providers; relevance: how a registered cerebras provider is routed to. (existing)
- [Hermes: Model Catalog Reference](../hermes_agent/hermes_model_catalog_reference.md) — model catalog schema; relevance: where cerebras models are surfaced. (existing)
- [oc_providers_cerebras](oc_providers_cerebras.md) — the deeper Cerebras provider config page (`pr01`, the card's `Related docs` target); relevance: where the provider's full configuration lives. (planned, this series)
- [oc_plugins_reference_chutes](oc_plugins_reference_chutes.md) — sibling provider-plugin card (`pl07`); relevance: identical provider-plugin shape. (planned, this series)
- [oc_plugins_reference_cloudflare_ai_gateway](oc_plugins_reference_cloudflare_ai_gateway.md) — sibling provider-plugin card; relevance: same surface. (planned, this series)
- [oc_plugins_reference_codex](oc_plugins_reference_codex.md) — sibling provider-plugin card; relevance: same `providers:` surface (plus contracts). (planned, this series)
- [oc_providers_models](oc_providers_models.md) — the provider/models overview (`pr05`); relevance: cross-provider model concepts. (planned, this series)

**Repos** (3, existing):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the LLM-provider extension framework; relevance: registers the `cerebras` provider. (existing)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — the agent/model-catalog runtime; relevance: consumes the provider's models. (existing)

**Snippets** (12, existing):
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider definition; relevance: the provider-definition pattern Cerebras follows.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — another provider definition; relevance: shows the provider contract cerebras implements.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — the runtime model catalog; relevance: where cerebras models register.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery/normalization; relevance: how cerebras models are discovered + normalized.
- [snippet_openclaw_model_catalog_manifest_planner](../../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md) — catalog manifest planning; relevance: planning cerebras model entries.
- [snippet_openclaw_agents_model_fallback_ladder](../../code_snippets/snippet_openclaw_agents_model_fallback_ladder.md) — provider/model fallback ladder; relevance: cerebras as a ladder rung.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registry; relevance: how a provider plugin like cerebras registers.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — a concrete provider plugin; relevance: parallel hosted-provider plugin.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load lifecycle; relevance: how the cerebras plugin loads.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package + surface contract; relevance: declares `providers: cerebras`.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: cerebras's registration entry.

### oc_plugins_reference_chutes (9t · 12s · 12d)

**Terms** (9, existing):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: chutes is an OpenClaw provider plugin.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — registers a model provider; relevance: chutes registers the `chutes` provider.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: chutes serves LLM inference.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — discovered model set; relevance: chutes feeds the catalog.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted model APIs; relevance: Chutes is a third-party inference service.
- [npm](../../term_dictionary/term_npm.md) — JS package registry/installer; relevance: install route is `npm` + ClawHub.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the extension SDK; relevance: the provider plugin is built on it.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + surface declaration; relevance: `@openclaw/chutes-provider` declares `providers: chutes`.
- [Model Router](../../term_dictionary/term_model_router.md) — routes across providers; relevance: chutes becomes routable once registered.

**Docs** (12; 7 existing + 5 planned):
- [Claude Code: Model Selection](../claude_code/cc_model_selection.md) — picking a provider's model; relevance: chutes adds selectable models. (existing)
- [Claude Code: Fallback Models](../claude_code/cc_fallback_models.md) — model failover; relevance: chutes participates in fallback. (existing)
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — adding a provider plugin; relevance: analog of registering chutes. (existing)
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin authoring spec; relevance: the shape chutes follows. (existing)
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — cloud provider catalog; relevance: Chutes is a hosted/aggregator inference service. (existing)
- [Hermes: Provider Routing](../hermes_agent/hermes_provider_routing.md) — routing across providers; relevance: how a chutes provider is routed to. (existing)
- [Hermes: Fallback Providers](../hermes_agent/hermes_fallback_providers.md) — provider-level failover; relevance: chutes as a fallback provider. (existing)
- [oc_providers_chutes](oc_providers_chutes.md) — the deeper Chutes provider config page (`pr02`, the card's `Related docs` target); relevance: where the full provider config lives. (planned, this series)
- [oc_plugins_reference_cerebras](oc_plugins_reference_cerebras.md) — sibling provider-plugin card; relevance: identical shape. (planned, this series)
- [oc_plugins_reference_cloudflare_ai_gateway](oc_plugins_reference_cloudflare_ai_gateway.md) — sibling provider-plugin card; relevance: same surface. (planned, this series)
- [oc_providers_models](oc_providers_models.md) — provider/models overview (`pr05`); relevance: cross-provider model concepts. (planned, this series)
- [oc_plugins_reference](oc_plugins_reference.md) — plugin-reference index (`pl05`); relevance: the cluster hub. (planned, this series)

**Repos** (3, existing):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension framework; relevance: registers the `chutes` provider. (existing)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent/model-catalog runtime; relevance: consumes chutes models. (existing)

**Snippets** (12, existing):
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider definition; relevance: pattern chutes follows.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator/hosted-provider pattern; relevance: Chutes is an aggregated hosted-inference service.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — another provider definition; relevance: shows the provider contract chutes implements.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — runtime model catalog; relevance: where chutes models register.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery/normalization; relevance: how chutes models are discovered.
- [snippet_openclaw_model_catalog_normalize_schemas](../../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md) — model-schema normalization; relevance: normalizing chutes model schemas.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registry; relevance: how chutes registers.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — concrete aggregator provider plugin; relevance: parallel hosted/aggregator plugin.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load lifecycle; relevance: how the chutes plugin loads.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package + surface contract; relevance: declares `providers: chutes`.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: chutes's registration entry.

### oc_plugins_reference_clickclack (8t · 11s · 11d)

**Terms** (8, existing):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: clickclack is an OpenClaw channel plugin.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — the contract that maps a chat platform to OpenClaw; relevance: clickclack registers a `channels:` adapter surface.
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — the dispatch kernel channels bind to; relevance: the clickclack adapter dispatches through the channel kernel.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + surface declaration; relevance: `@openclaw/clickclack` declares `channels: clickclack`.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the extension SDK; relevance: the channel plugin is built on it.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — the runtime contract registry; relevance: the channel surface registers into the same plugin contract registry.
- [WebSocket](../../term_dictionary/term_websocket.md) — bidirectional transport; relevance: a chat-channel surface streams send/receive over the gateway transport.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external platform integrations; relevance: clickclack docks an external chat platform into OpenClaw.

**Docs** (11; 7 existing + 4 planned):
- [Claude Code: Channels Overview](../claude_code/cc_channels_overview.md) — the channel/surface model; relevance: clickclack is a channel surface. (existing)
- [Claude Code: Channels Setup](../claude_code/cc_channels_setup.md) — configuring a channel; relevance: install/configure parallel for clickclack. (existing)
- [Claude Code: Build a Channel](../claude_code/cc_build_a_channel.md) — authoring a channel plugin; relevance: clickclack is exactly such a channel plugin. (existing)
- [Claude Code: Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — sending replies through a channel; relevance: clickclack sends/receives OpenClaw messages. (existing)
- [Claude Code: Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — relaying permissions over a channel; relevance: channel-plugin permission behavior. (existing)
- [Hermes: Adding a Platform Adapter (Plugin)](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — adding a chat-platform adapter as a plugin; relevance: exact analog of clickclack. (existing)
- [Hermes: Messaging Gateway Architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — how messaging channels plug into the gateway; relevance: where the clickclack channel binds. (existing)
- [oc_channels_clickclack](oc_channels_clickclack.md) — the deeper Clickclack channel config page (`ch01`, the card's `Related docs` target); relevance: full channel configuration. (planned, this series)
- [oc_channels_channel_routing](oc_channels_channel_routing.md) — channel routing concepts (`ch01`); relevance: how clickclack messages route. (planned, this series)
- [oc_plugins_reference](oc_plugins_reference.md) — plugin-reference index (`pl05`); relevance: the cluster hub. (planned, this series)
- [oc_concepts_channel_docking](oc_concepts_channel_docking.md) — the channel-docking concept (`co01`); relevance: the model clickclack realizes. (planned, this series)

**Repos** (3, existing):
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — the channel framework; relevance: registers + loads `clickclack`. (existing)
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel adapters; relevance: clickclack is a messaging channel. (existing)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: loads the bundled clickclack plugin. (existing)

**Snippets** (11, existing):
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — the channel adapter contract; relevance: the interface clickclack implements.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalization; relevance: how clickclack registers as a channel.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: routes clickclack messages.
- [snippet_openclaw_channels_binding_routing](../../code_snippets/snippet_openclaw_channels_binding_routing.md) — channel binding/routing; relevance: binds clickclack conversations to agents.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation resolution; relevance: resolves clickclack threads.
- [snippet_openclaw_channels_match_resolver](../../code_snippets/snippet_openclaw_channels_match_resolver.md) — channel match resolver; relevance: matches inbound clickclack messages.
- [snippet_openclaw_channels_status_reactions](../../code_snippets/snippet_openclaw_channels_status_reactions.md) — status/reaction handling; relevance: channel-plugin send-side behavior.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — plugin package + surface contract; relevance: declares `channels: clickclack`.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load lifecycle; relevance: how clickclack loads.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: clickclack's registration entry.
- [snippet_hermes_agent_gw_channel_directory](../../code_snippets/snippet_hermes_agent_gw_channel_directory.md) — channel directory in a sibling gateway; relevance: where a channel plugin like clickclack registers.

### oc_plugins_reference_cloudflare_ai_gateway (9t · 12s · 12d)

**Terms** (9, existing):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: this is an OpenClaw provider plugin.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — registers a model provider; relevance: registers the `cloudflare-ai-gateway` provider.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: routes LLM calls through Cloudflare AI Gateway.
- [API Gateway](../../term_dictionary/term_api_gateway.md) — a gateway fronting upstream APIs; relevance: Cloudflare AI Gateway is an AI gateway fronting upstream model APIs.
- [Reverse Proxy](../../term_dictionary/term_reverse_proxy.md) — proxies requests to upstreams; relevance: the AI gateway reverse-proxies model calls.
- [Model Router](../../term_dictionary/term_model_router.md) — routes calls across providers/models; relevance: the gateway routes to upstream providers.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external hosted model APIs; relevance: the gateway fronts third-party model APIs.
- [npm](../../term_dictionary/term_npm.md) — JS package registry/installer; relevance: install route is `npm` + ClawHub.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the discovered model set; relevance: gateway-routed models feed the catalog.

**Docs** (12; 7 existing + 5 planned):
- [Claude Code: LLM Gateway](../claude_code/cc_llm_gateway.md) — routing model calls through a gateway base URL; relevance: exactly what the cloudflare-ai-gateway provider does. (existing)
- [Claude Code: LLM Gateway (LiteLLM)](../claude_code/cc_llm_gateway_litellm.md) — a concrete gateway proxy; relevance: another model-gateway analog. (existing)
- [Claude Code: Proxy & Gateway Config](../claude_code/cc_proxy_and_gateway_config.md) — configuring a gateway/proxy; relevance: how to point the agent at the AI gateway base URL. (existing)
- [Claude Code: Model Selection](../claude_code/cc_model_selection.md) — selecting a model; relevance: gateway-fronted models are selectable. (existing)
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — adding a provider plugin; relevance: analog of registering the gateway provider. (existing)
- [Hermes: Provider Routing & Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — routing through proxies/gateways; relevance: the gateway-proxy routing model. (existing)
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin authoring; relevance: the shape this plugin follows. (existing)
- [oc_providers_cloudflare_ai_gateway](oc_providers_cloudflare_ai_gateway.md) — the deeper provider config page (`pr02`, the card's `Related docs` target); relevance: full gateway-provider config. (planned, this series)
- [oc_plugins_reference_cerebras](oc_plugins_reference_cerebras.md) — sibling provider-plugin card; relevance: same shape. (planned, this series)
- [oc_plugins_reference_chutes](oc_plugins_reference_chutes.md) — sibling provider-plugin card; relevance: same shape. (planned, this series)
- [oc_gateway_local_model_services](oc_gateway_local_model_services.md) — gateway/model-service routing concept (`gw03`); relevance: gateway-fronted model serving. (planned, this series)
- [oc_providers_models](oc_providers_models.md) — provider/models overview (`pr05`); relevance: cross-provider model concepts. (planned, this series)

**Repos** (3, existing):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension framework; relevance: registers the gateway provider. (existing)
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — the OpenClaw gateway; relevance: hosts model routing/auth toward the AI gateway. (existing)

**Snippets** (12, existing):
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — gateway/aggregator-routing provider; relevance: Cloudflare AI Gateway is a routing/aggregation front.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — BYOK / gateway auth modes; relevance: auth to the upstream AI gateway.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider definition; relevance: the gateway exposes an OpenAI-compatible surface.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — runtime model catalog; relevance: where gateway-routed models register.
- [snippet_openclaw_gateway_model_pricing_openrouter_litellm](../../code_snippets/snippet_openclaw_gateway_model_pricing_openrouter_litellm.md) — gateway model-pricing resolution; relevance: pricing for gateway-routed models.
- [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model alias/pricing lookup; relevance: alias resolution for gateway-fronted models.
- [snippet_openclaw_model_catalog_normalize_discovery](../../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md) — model discovery/normalization; relevance: discovering models behind the gateway.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package + surface contract; relevance: declares `providers: cloudflare-ai-gateway`.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load lifecycle; relevance: how the plugin loads.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin SDK entry points; relevance: the plugin's registration entry.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider-plugin registry; relevance: how the gateway provider registers.

### oc_plugins_reference_codex (9t · 12s · 12d)

**Terms** (9, existing):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: codex is an OpenClaw harness + provider plugin.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — registers a model provider; relevance: codex registers the `codex` provider.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — discovered model set; relevance: codex ships a Codex-managed GPT catalog.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: codex serves GPT models.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime hosting a coding agent; relevance: codex is a Codex app-server harness.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: codex registers `webSearchProviders`/`mediaUnderstandingProviders` contracts invoked via tools.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI's response/event API; relevance: Codex uses the Responses API surface.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + surface declaration; relevance: `@openclaw/codex` declares its provider + contract surfaces.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agents OpenClaw fronts; relevance: Codex is an autonomous coding agent harnessed here.

**Docs** (12; 8 existing + 4 planned):
- [Hermes: Codex Runtime Setup](../hermes_agent/hermes_codex_runtime_setup.md) — setting up a Codex app-server runtime; relevance: the harness this card is the OpenClaw analog of. (existing)
- [Hermes: Codex Runtime Tools](../hermes_agent/hermes_codex_runtime_tools.md) — Codex runtime tool surface; relevance: the contract/tool surfaces codex exposes. (existing)
- [Band: Codex Adapter](../band/band_adapter_codex.md) — a Codex coding-agent adapter; relevance: parallel Codex integration in a sibling platform. (existing)
- [Band: Coding Agents Deployment](../band/band_coding_agents_deployment.md) — deploying coding agents; relevance: deploying the Codex harness. (existing)
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — provider-plugin authoring; relevance: the `providers:` half of the codex card. (existing)
- [Hermes: Web Search Provider Plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — a webSearchProviders contract plugin; relevance: codex also registers `webSearchProviders`. (existing)
- [Claude Code: Model Selection](../claude_code/cc_model_selection.md) — selecting a model; relevance: Codex-managed GPT catalog models become selectable. (existing)
- [Claude Code: Computer Use](../claude_code/cc_computer_use.md) — agent computer-use surface; relevance: codex harness includes computer-use (per `plugins/codex-computer-use`). (existing)
- [oc_plugins_codex_harness](oc_plugins_codex_harness.md) — the deeper Codex harness page (`pl02`, the card's `Related docs` target); relevance: full harness internals. (planned, this series)
- [oc_plugins_reference_codex_supervisor](oc_plugins_reference_codex_supervisor.md) — sibling card supervising Codex sessions; relevance: supervises the harness this card defines. (planned, this series)
- [oc_plugins_codex_computer_use](oc_plugins_codex_computer_use.md) — Codex computer-use plugin (`pl02`); relevance: a contract surface of the codex harness. (planned, this series)
- [oc_providers_models](oc_providers_models.md) — provider/models overview (`pr05`); relevance: how the GPT catalog fits the model layer. (planned, this series)

**Repos** (3, existing):
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extension framework; relevance: registers the `codex` provider. (existing)
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — app-server host; relevance: hosts the Codex app-server harness. (existing)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent/model-catalog runtime; relevance: consumes the Codex GPT catalog. (existing)

**Snippets** (12, existing):
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — a Codex provider plugin; relevance: the provider half codex implements.
- [snippet_hermes_agent_core_codex_runtime](../../code_snippets/snippet_hermes_agent_core_codex_runtime.md) — Codex app-server runtime; relevance: the harness runtime codex wraps.
- [snippet_hermes_agent_core_codex_responses_adapter_init](../../code_snippets/snippet_hermes_agent_core_codex_responses_adapter_init.md) — Responses-API adapter init; relevance: codex uses the OpenAI Responses API surface.
- [snippet_hermes_agent_core_codex_responses_adapter_request](../../code_snippets/snippet_hermes_agent_core_codex_responses_adapter_request.md) — Responses-API request building; relevance: how codex issues Responses-API calls.
- [snippet_hermes_agent_core_codex_responses_adapter_extract](../../code_snippets/snippet_hermes_agent_core_codex_responses_adapter_extract.md) — Responses-API result extraction; relevance: parsing Codex/GPT responses.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider; relevance: the GPT-provider definition pattern codex follows.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — runtime model catalog; relevance: where the Codex GPT catalog registers.
- [snippet_openclaw_gateway_openresponses_session_sse](../../code_snippets/snippet_openclaw_gateway_openresponses_session_sse.md) — OpenResponses SSE session; relevance: codex's Responses-style streaming.
- [snippet_openclaw_gateway_openresponses_tools_usage](../../code_snippets/snippet_openclaw_gateway_openresponses_tools_usage.md) — OpenResponses tool usage; relevance: codex's contract/tool surfaces over Responses.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package + surface contract; relevance: declares `providers: codex` + the three contracts.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load lifecycle; relevance: how the codex plugin loads.
- [snippet_hermes_agent_skills_codex](../../code_snippets/snippet_hermes_agent_skills_codex.md) — Codex skills wiring; relevance: how Codex capabilities are surfaced as tools.

### oc_plugins_reference_codex_supervisor (9t · 12s · 12d)

**Terms** (9, existing):
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the gateway this plugin extends; relevance: codex-supervisor is an OpenClaw plugin.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime hosting a coding agent; relevance: it supervises the Codex app-server harness.
- [Session Persistence](../../term_dictionary/term_session_persistence.md) — durable session storage; relevance: `## Session Listing` reads stored history via Codex's state DB.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — the runtime contract registry; relevance: registers the `tools` contract; `codex_sessions_list` is a registered tool.
- [Function Calling](../../term_dictionary/term_function_calling.md) — model tool invocation; relevance: `codex_sessions_list`/`include_stored`/`max_stored_sessions` are invoked as a tool call.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — package + surface declaration; relevance: `@openclaw/codex-supervisor` declares `contracts: tools`.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the extension SDK; relevance: the supervisor plugin is built on it.
- [Process Supervisor](../../term_dictionary/term_autonomous_coding_agents.md) — autonomous coding agents; relevance: it supervises Codex agent sessions (process-level oversight).
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: the supervised Codex sessions run GPT models.

**Docs** (12; 8 existing + 4 planned):
- [Hermes: Codex Runtime Setup](../hermes_agent/hermes_codex_runtime_setup.md) — Codex app-server runtime; relevance: the harness this card supervises. (existing)
- [Hermes: Codex Runtime Tools](../hermes_agent/hermes_codex_runtime_tools.md) — Codex runtime tool surface; relevance: the tool surface (incl. session listing) it exposes. (existing)
- [Hermes: Sessions Lifecycle & Resume](../hermes_agent/hermes_sessions_lifecycle_resume.md) — session lifecycle/resume; relevance: loaded-vs-stored session distinction mirrored by `include_stored`. (existing)
- [Hermes: Session Storage](../hermes_agent/hermes_session_storage.md) — how sessions are stored; relevance: the stored-history state DB `codex_sessions_list` reads. (existing)
- [Hermes: Session Search & Storage](../hermes_agent/hermes_session_search_storage.md) — searching/listing stored sessions; relevance: the listing path codex-supervisor wraps. (existing)
- [Claude Code: Sessions](../claude_code/cc_sessions.md) — session model for a coding agent; relevance: loaded/stored session concepts. (existing)
- [Claude Code: Background Session Hosting](../claude_code/cc_background_session_hosting.md) — supervising background sessions; relevance: codex-supervisor supervises app-server sessions. (existing)
- [Band: Codex Adapter](../band/band_adapter_codex.md) — a Codex coding-agent adapter; relevance: the Codex sessions being supervised. (existing)
- [oc_plugins_reference_codex](oc_plugins_reference_codex.md) — sibling card defining the Codex harness/provider; relevance: the harness this card supervises. (planned, this series)
- [oc_plugins_codex_harness](oc_plugins_codex_harness.md) — the Codex harness page (`pl02`); relevance: harness internals the supervisor manages. (planned, this series)
- [oc_concepts_session](oc_concepts_session.md) — the session concept page (`co06`); relevance: loaded-vs-stored session model. (planned, this series)
- [oc_plugins_reference_canvas](oc_plugins_reference_canvas.md) — sibling reference card also registering `contracts: tools`; relevance: same surface shape. (planned, this series)

**Repos** (3, existing):
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — Codex app-server host; relevance: the app-server whose sessions are supervised. (existing)
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store/listing; relevance: the stored-session listing path `codex_sessions_list` uses. (existing)
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the extension/plugin framework; relevance: loads the bundled supervisor plugin. (existing)

**Snippets** (12, existing):
- [snippet_openclaw_gateway_sessions_read_methods](../../code_snippets/snippet_openclaw_gateway_sessions_read_methods.md) — session read/list methods; relevance: the listing path mirrored by `codex_sessions_list`.
- [snippet_openclaw_gateway_session_fs_index_read](../../code_snippets/snippet_openclaw_gateway_session_fs_index_read.md) — stored-session index read; relevance: stored-history read behind `include_stored`.
- [snippet_openclaw_gateway_session_fs_title_cache_archive](../../code_snippets/snippet_openclaw_gateway_session_fs_title_cache_archive.md) — stored/archived session cache; relevance: the stored-session cap behavior (200/1000).
- [snippet_openclaw_sessions_session_id_resolution](../../code_snippets/snippet_openclaw_sessions_session_id_resolution.md) — session id resolution; relevance: resolving listed Codex session ids.
- [snippet_openclaw_sessions_lifecycle_events](../../code_snippets/snippet_openclaw_sessions_lifecycle_events.md) — session lifecycle events; relevance: loaded-vs-stored session lifecycle.
- [snippet_openclaw_gateway_sessions_lifecycle_patches](../../code_snippets/snippet_openclaw_gateway_sessions_lifecycle_patches.md) — session lifecycle patching; relevance: how supervised sessions transition state.
- [snippet_openclaw_process_supervisor](../../code_snippets/snippet_openclaw_process_supervisor.md) — process supervision; relevance: supervising the Codex app-server process.
- [snippet_openclaw_process_kill_tree](../../code_snippets/snippet_openclaw_process_kill_tree.md) — process tree teardown; relevance: tearing down supervised Codex sessions.
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — the Codex provider plugin; relevance: the harness/provider being supervised.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load lifecycle; relevance: how the supervisor plugin loads.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package + surface contract; relevance: declares `contracts: tools`.
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — the runtime tool catalog; relevance: where `codex_sessions_list` registers as a tool.

>=5 EXISTING docs are present per note. Proper-noun terms confirmed GHOST (`term_cerebras`, `term_chutes`,
`term_cloudflare`, `term_codex`, `term_openai_codex`, `term_channel`, `term_clickclack`, `term_supervisor`,
`term_canvas`) are deliberately NOT cited — their depth is reached via the link-out sibling `oc_*` provider/channel/harness notes.

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_*` doc notes by its home sub-plan, NOT as new `term_dictionary`
entries; the only `term_dictionary` interaction is **linking existing** terms. Expected **0 new term_dictionary captures**.

| Term (appears in source) | Disposition |
|---|---|
| provider plugin / model provider | Link existing `term_provider_plugin`, `term_llm`, `term_model_catalog`, `term_third_party_genai_services`. |
| Cerebras / Chutes (provider names) | Proper-noun provider names — NOT promoted to terms (master rule; no `term_cerebras`/`term_chutes` in DB). Digested inside their `oc_*` notes; depth in the planned `pr01`/`pr02` provider notes (link-out). |
| Cloudflare AI Gateway | Gateway product name — link existing `term_api_gateway` / `term_reverse_proxy` / `term_model_router`; not a new term. |
| Codex / GPT catalog / app-server harness | Link existing `term_agent_harness`, `term_model_catalog`, `term_openai_responses_api`; "Codex"/"GPT" proper nouns not promoted (no `term_codex` in DB). Depth in `pl02` codex-harness (link-out). |
| Clickclack (channel name) | Channel proper noun — NOT a new term; link existing `term_channel_adapter` / `term_channel_kernel`; depth in `ch01` (link-out). |
| A2UI / Canvas surface | Link existing `term_a2ui`; "Canvas" surface proper noun not promoted. |
| ClawHub / npm install route | Link existing `term_npm`; "ClawHub" is documented by its own `cw01`–`cw03` sub-plans (link-out), not a new term. |
| contracts: tools / mediaUnderstandingProviders / migrationProviders / webSearchProviders | Contract-surface identifiers — link existing `term_tool_registry` / `term_function_calling`; not new terms. |
| codex_sessions_list / include_stored / max_stored_sessions | Tool name + params specific to codex-supervisor — documented in note 7 body verbatim; not reusable cross-cutting terms. |

**New-term candidates: NONE.** No genuinely reusable, cross-cutting term lacks both a doc-page home and an existing note.
(If augment's re-run of the Step 2d scan surfaces one, capture it via `/tessellum-capture-term-note` + add to the best-fit
glossary — most likely `acronym_glossary_agentic_ai.md` or `acronym_glossary_llm.md`.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** Inherited from master: no term definition is ever inlined in an `oc_*` note; existing terms are
glossary entry, no inlining in the doc note).

## Per-Phase Validation Gate (G1–G9)

Single execution phase (7 notes). 9-GATE inherited verbatim from the master.

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` clean for all 7 notes (fixed YAML field order; no forbidden fields; `## Overview` + `## Related Notes` + `## References` + bold footer present). |
| G2 | Grounding | Each note diffs faithfully against `inbox/openclaw_docs/plugins/reference/<page>.md` — package name, install route, surface, and (note 7) the Session Listing facts reproduced exactly; nothing invented. |
| G3 | Density + Coverage | Each note ≤400 lines / ≤2,500 words / ≤6 code blocks (all ~240w stubs); every source H2/intro mapped (Section Coverage Map); one `building_block: procedure` per note. |
| G4 | Cross-Reference | Each note's `## Related Notes` meets the LOCKED raised floors: **≥8 `term_dictionary` terms · ≥10 code_snippets · ≥10 docs** (≥5 EXISTING `cc_*`/`hermes_*`/`band_*`) + relevant `repo_openclaw*`, each an indexed `[text](path.md)` link with a relevance statement (verbatim from **## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)**). |
| G5 | Ghost-reference detect + redirect | No links to non-existent notes; the not-existing terms list (`term_cerebras`, …) is excluded; planned siblings flagged. |
| G6 | Broken-link fix | `/tessellum-fix-broken-links`; 0 broken links after incremental reindex; relative paths correct from `resources/documentation/openclaw/`. |
| G7 | Discoverability (inbound) | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (via `entry_openclaw_docs.md` rows + the inlinks below). |
| G8 | In-degree ≥1 / anti-island | DB `in_degree ≥ 1` for each of the 7 notes after reindex (`note_links` verified). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
# Resolve paths from config (single source of truth)
cd /path/to/vault
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")

# --- G2 grounding: confirm measured source word counts (re-measure at execution) ---
for f in canvas cerebras chutes clickclack cloudflare-ai-gateway codex codex-supervisor; do
  echo "$f: $(wc -w < inbox/openclaw_docs/plugins/reference/$f.md) words, \
$(($(grep -c '```' inbox/openclaw_docs/plugins/reference/$f.md)/2)) code fences"
done

# --- G1/G3/G4/G7 gate sweep over the new notes ---
GATE_DIR=resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
for f in $GATE_DIR/oc_plugins_reference_canvas.md \
         $GATE_DIR/oc_plugins_reference_cerebras.md \
         $GATE_DIR/oc_plugins_reference_chutes.md \
         $GATE_DIR/oc_plugins_reference_clickclack.md \
         $GATE_DIR/oc_plugins_reference_cloudflare_ai_gateway.md \
         $GATE_DIR/oc_plugins_reference_codex.md \
         $GATE_DIR/oc_plugins_reference_codex_supervisor.md ; do
  echo "=== $f ==="
  grep -Eq "$REQ_SECTIONS" "$f" && echo "  required sections: OK" || echo "  MISSING required section"
  if [ "$REQUIRE_SOURCE_URL" = "1" ]; then
    grep -q '^source_url: https://docs.openclaw.ai/' "$f" && echo "  source_url: OK" || echo "  source_url MISSING"
  fi
  echo "  sibling links ($SIBLING_PREFIX): $(grep -oE "$SIBLING_PREFIX[a-z0-9_]+\.md" "$f" | sort -u | wc -l)"
done

# --- G1 YAML frontmatter validation ---
for f in $GATE_DIR/oc_plugins_reference_*.md; do
  python3 scripts/check_yaml_frontmatter.py --path "$f"
done

# --- G1 note format ---  (via skill at execution: /tessellum-check-note-format)
for nm in term_openclaw term_a2ui term_plugin_manifest term_plugin_sdk term_tool_registry \
          term_provider_plugin term_model_catalog term_third_party_genai_services term_npm \
          term_channel_adapter term_channel_kernel term_api_gateway term_reverse_proxy term_model_router \
          term_agent_harness term_openai_responses_api term_function_calling term_session_persistence \
          term_llm term_websocket \
          repo_openclaw_extensions repo_openclaw_extensions_llm_providers repo_openclaw_channels \
          repo_openclaw_channels_messaging repo_openclaw_apps repo_openclaw_agents repo_openclaw_gateway \
          snippet_openclaw_plugin_lifecycle snippet_openclaw_plugin_package_contract \
          snippet_openclaw_plugin_sdk_entries snippet_openclaw_provider_openai \
          snippet_openclaw_provider_openrouter_aggregator snippet_openclaw_agents_model_catalog \
          snippet_openclaw_channels_adapter_contract snippet_openclaw_channels_kernel_dispatch \
          snippet_openclaw_gateway_sessions_read_methods snippet_openclaw_macos_canvas_lifecycle \
          snippet_hermes_agent_plugins_provider_codex cc_channels_overview cc_llm_gateway \
          hermes_codex_runtime_setup ; do
  printf '%-50s %s\n' "$nm" "${r:-GHOST}"
done

# --- G6 broken links + G8 in-degree (after incremental reindex) ---
bash scripts/update_notes_database.sh   # incremental; --force only if needed
for nm in oc_plugins_reference_canvas oc_plugins_reference_cerebras oc_plugins_reference_chutes \
          oc_plugins_reference_clickclack oc_plugins_reference_cloudflare_ai_gateway \
          oc_plugins_reference_codex oc_plugins_reference_codex_supervisor ; do
  printf '%-45s in_degree=%s\n' "$nm" "$(sqlite3 "$DB" "SELECT in_degree FROM notes WHERE note_name='$nm';")"
done
```

## Density Re-Assessment

| Note | Est. words | Est. code blocks | Caps (≤2500w / ≤400L / ≤6 code) | Near cap? |
|------|-----------:|-----------------:|---------------------------------|-----------|
| oc_plugins_reference_canvas | 230 | 0–1 | within | No (far below) |
| oc_plugins_reference_cerebras | 230 | 0–1 | within | No |
| oc_plugins_reference_chutes | 230 | 0–1 | within | No |
| oc_plugins_reference_clickclack | 230 | 0–1 | within | No |
| oc_plugins_reference_cloudflare_ai_gateway | 230 | 0–1 | within | No |
| oc_plugins_reference_codex | 240 | 0–1 | within | No |
| oc_plugins_reference_codex_supervisor | 290 | 0–1 | within | No |

All notes are well under every cap (no note approaches 2,500 words). No borderline densities → no split promotion needed.
Risk is the opposite (over-thin stubs); mitigated by the ≥6-term + repo/snippet cross-reference floor giving each note
real graph connectivity rather than padding the body.

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (created as the master pre-step W1; `building_block: navigation`),
under the Plugins → Reference cluster (sub-plan `pl07`), one row per note (canvas / cerebras / chutes / clickclack /
cloudflare-ai-gateway / codex / codex-supervisor). Each note receives the entry-point back-link at finalization
(satisfies G7/G8). No separate entry point for this sub-plan (master hub aggregates all Plugins sub-plans).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify + add at execution; satisfies G7/G8 — each new note in-degree ≥1):

- `entry_openclaw_docs.md` (planned, master pre-step W1) → all 7 notes (primary inbound; Plugins/Reference cluster rows).
- `repo_openclaw_extensions_llm_providers.md` → notes 2 (cerebras), 3 (chutes), 5 (cloudflare-ai-gateway), 6 (codex).
- `repo_openclaw_channels.md` → note 4 (clickclack).
- `repo_openclaw_apps.md` → notes 1 (canvas), 6 (codex), 7 (codex-supervisor).
- `repo_openclaw_sessions.md` → note 7 (codex-supervisor).
- `term_a2ui.md` → note 1 (canvas).
- `term_provider_plugin.md` → notes 2, 3, 5, 6.
- `repo_openclaw_extensions.md` → notes 1, 4, 7.

These reciprocate the `## Related Notes` outbound links, ensuring no orphan/island note.

## Pacing Rules (inherited from master)

One execution phase; 8 gates (G1–G9) before commit. Re-read each source page at execution; reproduce package name /
install route / surface / Session-Listing facts verbatim. One `building_block: procedure` per note. Incremental reindex
after the wave; verify `note_links` + 0 broken links + in-degree ≥1 before commit. `git pull --rebase --autostash`
first; commit+push the wave together; no Claude co-author trailer. Fan-out cap ~30 agents/run (this sub-plan is 7 notes,
well within a single wave).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21 (xref-augment, raised floors)** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**What was locked.** The prior "## Candidate Cross-References" section was replaced by **## Per-Note Related Notes
Snippets) mapping at the **raised floors**: `≥8 terms · ≥10 snippets · ≥10 docs per note`, with `≥5 of the 10 docs`
confirmed all 7 notes meet every floor.

**Per-note counts (terms / snippets / docs (existing+oc) / repos — all floors met):**

| Note | Terms | Snippets | Docs (existing/oc) | Repos | Floors met |
|------|------:|---------:|-------------------:|------:|:----------:|
| oc_plugins_reference_canvas | 8 | 12 | 11 (8/3) | 3 | ✅ |
| oc_plugins_reference_cerebras | 9 | 12 | 12 (7/5) | 3 | ✅ |
| oc_plugins_reference_chutes | 9 | 12 | 12 (7/5) | 3 | ✅ |
| oc_plugins_reference_clickclack | 8 | 11 | 11 (7/4) | 3 | ✅ |
| oc_plugins_reference_cloudflare_ai_gateway | 9 | 12 | 12 (7/5) | 3 | ✅ |
| oc_plugins_reference_codex | 9 | 12 | 12 (8/4) | 3 | ✅ |
| oc_plugins_reference_codex_supervisor | 9 | 12 | 12 (8/4) | 3 | ✅ |

**Corpora used.** Terms: the 20-odd OpenClaw/agent-runtime `term_dictionary` notes (provider/channel proper-noun terms
intentionally NOT cited — DB-confirmed GHOST). Snippets: the rich `snippet_openclaw_*` (plugin/provider/channel/session/
EXISTING `claude_code/cc_*` (plugins, model-selection, channels, gateway, sessions, computer-use), `hermes_agent/hermes_*`
(provider/plugin/codex/session), and `band/band_*` (codex adapter, coding-agents, ACP) corpora, supplemented by sibling
`oc_*` (planned, this series) toward the 10-doc floor.

**New-term candidates: NONE.** Re-read of all 7 pages surfaced no genuinely reusable, cross-cutting term lacking both a
doc-page home and an existing vault note. Per master design (mirrors `claude_code`/`pi`), OpenClaw vocabulary is digested
as `oc_*` doc notes, not new `term_dictionary` entries; only EXISTING terms are linked. Proper nouns (Cerebras, Chutes,
Cloudflare, Codex, Clickclack, Canvas, GPT, ClawHub) are not promoted. Best-fit glossary if a future term were ever
needed: `acronym_glossary_agentic_ai.md` or `acronym_glossary_llm.md` (master W5).

**Sections unchanged (already complete + correct from plan-digestion):** Section Coverage Map (every H2/intro mapped,
no orphans), Split Decisions (no splits — all 7 pages are 54–98w single-BB stubs), Density Re-Assessment (all far below
caps), Undigested Terms Plan, Term-Note Authoring Requirements (N/A, 0 new terms), Per-Phase 9-GATE table, Validation
Scripts, Entry Point Decision (inherited — UPDATE `entry_openclaw_docs.md`, created master pre-step W1), Inlinks, Pacing.
Re-measured source word counts confirm the plan's 454-word total (CP7 below).

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|----|------------|:------:|----------|
| CP2 | 9-GATE present per batch | **PASS** | "## Per-Phase Validation Gate (G1–G9)" present for the single execution phase: G1 Format, G2 Grounding, G3 Density+Coverage, G4 CrossRef (raised floors), G5 Ghost, G6 Broken-link, G7 Discoverability, G8 in-degree≥1 — inherited verbatim from master. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | "## Entry Point Decision (inherited from master)": contributes 7 rows to `entry_openclaw_docs.md` (created master pre-step W1, `building_block: navigation`), Plugins→Reference cluster (`pl07`), one row per note; size threshold satisfied (master >30-note series ⇒ CREATE dedicated hub already decided). |
| CP4 | Size | **PASS** | 7 planned notes (well ≤30); single execution phase; no split needed. |
| CP5 | Format derived from existing target-dir notes | **PASS** | Format inherited from master "## Format Definition (Shared)", derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (verified: those dirs use `## Overview` + `## Related Notes` + bold `**Source**`/`**Last Updated**`/`**Status**` footer + fixed YAML field order with `source_url`, forbidden-field list). Not invented. |
| CP6 | Density | **PASS** | Density Re-Assessment: all 7 notes ~230–290 est. words, 0–1 code blocks, far below 2,500w/400L/6-code caps; no borderline → no split promotion. Risk is over-thin, mitigated by the raised cross-ref floors giving real graph connectivity. |
| CP7 | Sources measured | **PASS** | Re-measured `wc -w` of all 7 mirror pages: canvas 55, cerebras 54, chutes 54, clickclack 62, cloudflare-ai-gateway 62, codex 69, codex-supervisor 98 → matches the plan's per-page table and 454-word total exactly; 0 code fences confirmed. No under-estimation. |
| CP8 | Undigested terms + authoring reqs | **PASS** | "## Undigested Terms Plan" present (every source term → disposition: link-existing or proper-noun-not-promoted); "## Term-Note Authoring Requirements" present (N/A, 0 new terms, master authoring reqs apply if one ever surfaces). Must-language inherited from master. |
| CP8f | Slug / collision audit | **PASS** | All 7 planned slugs derive deterministically from page slugs (master rule `oc_` + slug with `/`,`-`→`_`); collision audit (term_dictionary AND documentation/) found no existing `oc_*` doc nor substantive term duplicating these 7 plugin cards. Proper-noun terms (`term_cerebras`…`term_canvas`) DB-confirmed GHOST → correctly NOT cited; no doc-note duplicates an existing term note. |
| CP9 | Discoverability / inlinks | **PASS** | "## Inlinks (existing notes → new notes)": every new note has ≥1 planned outside-folder inbound link (`entry_openclaw_docs` → all 7; `repo_openclaw_extensions_llm_providers` → 2/3/5/6; `repo_openclaw_channels` → 4; `repo_openclaw_apps` → 1/6/7; `repo_openclaw_sessions` → 7; `term_a2ui` → 1; etc.); G7/G8 in the gate table mark inlink-addition as an executed, gated step (in-degree≥1 verified at reindex). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
