---
title: Sub-Plan pl24 — OpenClaw Docs: Plugins (SDK Channel, Entrypoints, Migration, Overview, Provider, Runtime, Setup)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/sdk-channel-plugins", "plugins/sdk-entrypoints", "plugins/sdk-migration", "plugins/sdk-overview", "plugins/sdk-provider-plugins", "plugins/sdk-runtime", "plugins/sdk-setup"]
---


# Sub-Plan pl24: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared

## Scope

The 7 **plugin SDK** pages — the typed contract between OpenClaw plugins and core. Together they cover: the SDK overview (import map + registration API), the four `define*PluginEntry` entrypoint helpers, the channel-plugin and provider-plugin authoring walkthroughs, the `api.runtime` injected-helper reference, plugin packaging/setup/config-schema (`package.json` `openclaw` field, `openclaw.plugin.json` manifest, `setup-entry.ts`, config schemas, setup wizards), and the legacy-surface → narrow-subpath migration guide. **Priority: P3 (Phase C — plugin reference sprawl).** These pages depend on (and should LINK, not redefine) the existing CODE-side `repo_openclaw*` notes, `term_plugin_sdk`, `term_plugin_manifest`, and `term_provider_plugin`. This is the SDK-authoring core of the plugins section (`plugins/sdk-*`), distinct from the per-plugin `plugins/reference/*` pages in pl05–pl23.

**Source**: OpenClaw docs, 7 pages, 25,429 measured words. **Planned: 13 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| sdk-channel-plugins | plugins/sdk-channel-plugins | 4,025 | 10 | 8 | 0 | procedure (split: concepts vs walkthrough) |
| sdk-entrypoints | plugins/sdk-entrypoints | 1,732 | 7 | 6 | 0 | model (reference) |
| sdk-migration | plugins/sdk-migration | 6,522 | 16 | 11 | 0 | procedure (split: migration vs import-path reference) |
| sdk-overview | plugins/sdk-overview | 3,176 | 6 | 2 | 18 | model (split: imports vs registration API) |
| sdk-provider-plugins | plugins/sdk-provider-plugins | 4,315 | 24 | 6 | 0 | procedure (split: walkthrough vs ClawHub/catalog) |
| sdk-runtime | plugins/sdk-runtime | 3,027 | 27 | 6 | 0 | model (split: config/utilities vs namespaces) |
| sdk-setup | plugins/sdk-setup | 2,632 | 20 | 5 | 9 | procedure (split: packaging vs config schema/wizards) |

Totals: **25,429 words · 110 code fences · 7 pages.** Six of seven pages exceed the 2,500-word cap and split; only `sdk-entrypoints` (1,732w) stays one note.

## Content Strategy

- **Prioritize:** (1) the SDK overview registration API (`OpenClawPluginApi` methods — every plugin type uses it) and import convention; (2) the `define*PluginEntry` entrypoints (the canonical wiring shape); (3) the channel/provider authoring walkthroughs (the two most common plugin types, with the most code); (4) the `api.runtime` namespace reference (the helper surface every plugin reaches for). These are the load-bearing reference pages other plugin pages link into.
- **Split** (word-cap >2500 and/or mixed BB): each of the 6 oversized pages → 2 notes along a natural concept/reference vs procedure boundary (see Split Decisions). Keeps each note ≤6 code blocks and one building_block.
- **Link-out (do NOT redefine):** plugin-architecture/lifecycle, building-plugins how-to, manifest deep-dive, hooks, ClawHub publishing, and the per-plugin reference pages are owned by other Plugins sub-plans (pl01–pl23, pl25) and ClawHub (cw01–03) — cite as sibling `oc_*` (planned) or external URL, do not duplicate. Term definitions (`term_plugin_sdk`, `term_plugin_manifest`, `term_provider_plugin`, `term_oauth`, `term_websocket`, `term_function_calling`, `term_subagent`, `term_text_to_speech`, `term_speech_to_text`) are LINKED, never inlined.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_sdk_overview_imports.md` | model | sdk-overview.md: Import convention, Subpath reference, Internal module convention | 600 | OpenClaw plugin-SDK import model: always import from a narrow `openclaw/plugin-sdk/<subpath>`, the grouped subpath catalog, deprecated branded/compat facades to avoid, and the internal module convention. |
| 2 | `oc_plugins_sdk_overview_registration_api.md` | model | sdk-overview.md: Registration API (Capability, Tools/commands, Infrastructure, Host hooks, Gateway discovery, CLI registration/backend, Exclusive slots, Deprecated memory adapters, Events/lifecycle, Hook decision semantics, API object fields) | 700 | The `OpenClawPluginApi` `register(api)` surface: every registration method (capabilities, tools/commands, infrastructure, host hooks, gateway discovery, CLI metadata/backend, exclusive slots, events/lifecycle), hook-decision semantics, and the `api` object fields. |
| 3 | `oc_plugins_sdk_entrypoints.md` | model | sdk-entrypoints.md: defineToolPlugin, definePluginEntry, defineChannelPluginEntry, defineSetupPluginEntry, Registration mode, Plugin shapes | 650 | The four `define*PluginEntry` helpers that wrap a plugin's exported entry: tool, generic, channel, and setup entrypoints; registration mode (eager vs deferred); and the canonical plugin object shapes. |
| 4 | `oc_plugins_sdk_channel_plugins_concepts.md` | concept | sdk-channel-plugins.md: How channel plugins work, Approvals and channel capabilities, Inbound mention policy | 650 | How OpenClaw channel plugins work — the inbound/outbound dispatch model, approval flow and declared channel capabilities, and the inbound mention/bot-loop policy a channel must implement. |
| 5 | `oc_plugins_sdk_channel_plugins_walkthrough.md` | procedure | sdk-channel-plugins.md: Walkthrough (Package & manifest, Build channel object, Wire entry point, Add setup entry, Handle inbound, Test), File structure, Advanced topics, Next steps | 700 | Step-by-step channel-plugin authoring: package/manifest, build the channel plugin object, wire the entry point, add a setup entry, handle inbound messages, test; plus file structure and advanced topics. |
| 6 | `oc_plugins_sdk_provider_plugins_walkthrough.md` | procedure | sdk-provider-plugins.md: Walkthrough (Package & manifest, Register provider, Dynamic model resolution, Runtime hooks, Extra capabilities, Test) | 750 | Step-by-step provider-plugin authoring: package/manifest, register the provider, dynamic model resolution, runtime hooks, optional extra capabilities, and testing the provider. |
| 7 | `oc_plugins_sdk_provider_plugins_clawhub_catalog.md` | procedure | sdk-provider-plugins.md: Publish to ClawHub, File structure, Catalog order reference, Next steps | 450 | Publishing a provider plugin to ClawHub and the catalog-order reference: file structure, required publish metadata, and how providers are ordered in the model catalog. |
| 8 | `oc_plugins_sdk_runtime_config_utilities.md` | procedure | sdk-runtime.md: Config loading and writes, Reusable runtime utilities, Storing runtime references, Other top-level api fields | 650 | Using `api.runtime` config + shared utilities: config-snapshot reads, `mutateConfigFile`/`replaceConfigFile` with `afterWrite` policy, the shared `botLoopProtection` guard, storing runtime references, and other top-level `api` fields. |
| 9 | `oc_plugins_sdk_runtime_namespaces.md` | model | sdk-runtime.md: Runtime namespaces (agent, agent.defaults, llm, subagent, nodes, tasks.managedFlows, tts, mediaUnderstanding, imageGeneration, webSearch, media, config, system, events, logging, modelAuth, state, tools, channel) | 700 | Reference for the `api.runtime` namespaces injected into every plugin: agent/session, llm, subagent, nodes, managed-flow tasks, tts/stt, image-gen, web-search, media, system, events, logging, model-auth, state, tools, and channel helpers. |
| 10 | `oc_plugins_sdk_setup_packaging.md` | procedure | sdk-setup.md: Package metadata (openclaw fields, openclaw.channel, openclaw.install, Deferred full load), Plugin manifest, ClawHub publishing, Setup entry (narrow helper imports, channel-owned single-account promotion) | 650 | Packaging an OpenClaw plugin: the `package.json` `openclaw` field (extensions, channel, install, deferred load), the `openclaw.plugin.json` manifest, ClawHub publishing metadata, and the `setup-entry.ts` setup entry. |
| 11 | `oc_plugins_sdk_setup_config_schema_wizards.md` | procedure | sdk-setup.md: Config schema (Building channel config schemas), Setup wizards, Publishing and installing | 550 | Defining plugin config schemas and setup wizards: `buildChannelConfigSchema`, channel-config-schema primitives, the setup-wizard flow, and publishing/installing the plugin. |
| 12 | `oc_plugins_sdk_migration.md` | procedure | sdk-migration.md: What is changing, Why this changed, Talk/realtime-voice migration plan, Compatibility policy, How to migrate, Active deprecations, Removal timeline, Suppressing warnings | 700 | Migrating plugins off the deprecated broad SDK surfaces (`plugin-sdk/compat`, `infra-runtime`, `config-runtime`, `extension-api`) to narrow subpaths: what changed and why, the compatibility policy, the step-by-step migration, active deprecations, and removal timeline. |
| 13 | `oc_plugins_sdk_migration_import_paths.md` | model | sdk-migration.md: Import path reference | 550 | The legacy → modern import-path reference table for plugin-SDK migration: each deprecated broad import mapped to its narrow `openclaw/plugin-sdk/<subpath>` replacement(s). |

## Section Coverage Map

```
sdk-overview.md
├── Import convention ────────────────────────────────── → note 1 (oc_plugins_sdk_overview_imports)
├── Subpath reference ────────────────────────────────── → note 1
├── Internal module convention ───────────────────────── → note 1
├── Registration API ─────────────────────────────────── → note 2 (oc_plugins_sdk_overview_registration_api)
│   ├── Capability registration ──────────────────────── → note 2
│   ├── Tools and commands ───────────────────────────── → note 2
│   ├── Infrastructure ───────────────────────────────── → note 2
│   ├── Host hooks for workflow plugins ──────────────── → note 2
│   ├── Gateway discovery registration ───────────────── → note 2
│   ├── CLI registration metadata / CLI backend ──────── → note 2
│   ├── Exclusive slots / Deprecated memory adapters ─── → note 2
│   ├── Events and lifecycle / Hook decision semantics ─ → note 2
│   └── API object fields ────────────────────────────── → note 2
sdk-entrypoints.md
├── defineToolPlugin ─────────────────────────────────── → note 3 (oc_plugins_sdk_entrypoints)
├── definePluginEntry ────────────────────────────────── → note 3
├── defineChannelPluginEntry ─────────────────────────── → note 3
├── defineSetupPluginEntry ───────────────────────────── → note 3
├── Registration mode ────────────────────────────────── → note 3
└── Plugin shapes ────────────────────────────────────── → note 3
sdk-channel-plugins.md
├── How channel plugins work ─────────────────────────── → note 4 (oc_plugins_sdk_channel_plugins_concepts)
├── Approvals and channel capabilities ───────────────── → note 4
├── Inbound mention policy ───────────────────────────── → note 4
├── Walkthrough (6 steps) ────────────────────────────── → note 5 (oc_plugins_sdk_channel_plugins_walkthrough)
├── File structure / Advanced topics / Next steps ────── → note 5
sdk-provider-plugins.md
├── Walkthrough (6 steps) ────────────────────────────── → note 6 (oc_plugins_sdk_provider_plugins_walkthrough)
├── Publish to ClawHub ───────────────────────────────── → note 7 (oc_plugins_sdk_provider_plugins_clawhub_catalog)
├── File structure ───────────────────────────────────── → note 7
├── Catalog order reference / Next steps ─────────────── → note 7
sdk-runtime.md
├── Config loading and writes ────────────────────────── → note 8 (oc_plugins_sdk_runtime_config_utilities)
├── Reusable runtime utilities ───────────────────────── → note 8
├── Storing runtime references ───────────────────────── → note 8
├── Other top-level api fields ───────────────────────── → note 8
├── Runtime namespaces (19 accordions) ───────────────── → note 9 (oc_plugins_sdk_runtime_namespaces)
sdk-setup.md
├── Package metadata (openclaw fields, channel, install, deferred load) → note 10 (oc_plugins_sdk_setup_packaging)
├── Plugin manifest ──────────────────────────────────── → note 10
├── ClawHub publishing ───────────────────────────────── → note 10
├── Setup entry (narrow imports, single-account promotion) → note 10
├── Config schema (Building channel config schemas) ──── → note 11 (oc_plugins_sdk_setup_config_schema_wizards)
├── Setup wizards ────────────────────────────────────── → note 11
├── Publishing and installing ────────────────────────── → note 11
sdk-migration.md
├── What is changing / Why this changed ──────────────── → note 12 (oc_plugins_sdk_migration)
├── Talk and realtime voice migration plan ───────────── → note 12
├── Compatibility policy / How to migrate ────────────── → note 12
├── Active deprecations / Removal timeline ───────────── → note 12
├── Suppressing the warnings temporarily ─────────────── → note 12
└── Import path reference ────────────────────────────── → note 13 (oc_plugins_sdk_migration_import_paths)
```

No orphaned sections. Each page's trailing `## Related` (link list, every page) is consumed as candidate cross-refs, not a digested section. Architecture/lifecycle/building-plugins/hooks/manifest/ClawHub-detail content referenced inline is link-out to sibling sub-plans (pl01–pl23, pl25, cw01–03), not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| sdk-channel-plugins.md (4,025w, 8 H2) | notes 4 + 5 | Exceeds 2,500w; mixes a conceptual model (how channel plugins work / approvals / inbound policy → concept BB) with a 6-step authoring walkthrough (procedure BB). Split per word-cap + mixed-BB rules. |
| sdk-provider-plugins.md (4,315w, 24 code, 6 H2) | notes 6 + 7 | Exceeds 2,500w and 6-code cap (24 fences). Split the 6-step authoring walkthrough (procedure) from the ClawHub-publish + catalog-order reference (deployment procedure), keeping each ≤6 code. |
| sdk-runtime.md (3,027w, 27 code, 6 H2) | notes 8 + 9 | Exceeds 2,500w and far exceeds the 6-code cap (27 fences). Split config/utilities usage (procedure) from the 19-namespace `api.runtime` reference (model BB), distributing the code so each note stays ≤6. |
| sdk-setup.md (2,632w, 20 code, 8 H2/H3) | notes 10 + 11 | Exceeds 2,500w and 6-code cap (20 fences). Split packaging/manifest/setup-entry (procedure) from config-schema-building + setup-wizards + install (procedure) — two distinct task clusters. |
| sdk-overview.md (3,176w, 2 H2 / 18 H3) | notes 1 + 2 | Exceeds 2,500w; mixes the import/subpath model (note 1) with the large `OpenClawPluginApi` registration-API reference (note 2, 18 H3 sub-methods) — both model BB but distinct lookup targets, split for atomicity. |
| sdk-migration.md (6,522w, 16 code, 11 H2) | notes 12 + 13 | Largest page (>2.5× cap). Split the migration narrative + policy + deprecation timeline (procedure) from the standalone Import path reference table (model/lookup BB). |
| sdk-entrypoints.md (1,732w, 7 code) | (none — 1 note) | Under 2,500w; single coherent reference of the four `define*PluginEntry` helpers + registration mode + plugin shapes. Stays one note (note 3); 7 fences trimmed to ≤6 by reproducing only the canonical signature per helper. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (25,429 words, 110 code fences). New `oc_` notes: **13** (planned-notes rows #1–#13, one per row). New `term_dictionary` notes: **0**.
- BB distribution: **procedure ×7** (notes 5, 6, 7, 8, 10, 11, 12) · **model ×5** (notes 1, 2, 3, 9, 13) · **concept ×1** (note 4) = 13 notes.
- Est. digest words ~8,250 (avg ~635/note) — strong compression of 25,429 source words (~32%), appropriate for reference/walkthrough pages with heavy code that is reproduced selectively.
- 110 source code fences distribute across the 13 notes; each note kept ≤6 (config/signature snippets reproduced verbatim and selectively; the 24/27/20-fence pages drove their splits).
- **Note count vs master estimate:** master estimated 11; locked here at **13**. The +2 comes from the heavier-than-typical SDK code density (sdk-provider-plugins 24, sdk-runtime 27, sdk-setup 20 fences) forcing reference/procedure splits to keep each note ≤6 code blocks and one BB.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

>
> **Relative paths** from a note at `resources/documentation/openclaw/oc_X.md`: term → `../../term_dictionary/term_Y.md` · snippet → `../../code_snippets/snippet_Y.md` · repo → `../../../areas/code_repos/repo_Y.md` · sibling oc_ → `oc_Y.md` · other doc → `../<folder>/<file>.md` (`../pi/`, `../hermes_agent/`, `../claude_code/`, `../band/`, `../aws_bedrock_agentcore/`) · analysis → `../../analysis_thoughts/argument_Y.md` · entry → `../../../0_entry_points/entry_Y.md`.

### oc_plugins_sdk_overview_imports (10t · 11s · 11d)

**Terms**
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — OpenClaw's typed plugin↔core contract; relevance: this note IS the import-convention reference for the `openclaw/plugin-sdk/<subpath>` surface.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed language of the SDK; relevance: every subpath is a typed TS module imported via `import { … } from "openclaw/plugin-sdk/<subpath>"`.
- [Deprecation](../../term_dictionary/term_deprecation.md) — managed API sunset policy; relevance: the page enumerates deprecated branded/compat facade subpaths (`plugin-sdk/discord`, `…/slack`) to avoid.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: channel config is published through `openclaw.plugin.json#channelConfigs`, referenced by the import guidance.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool-call mechanism; relevance: the `plugin-sdk/core` umbrella exposes tool/capability surfaces backing function calling.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — host tool/command store; relevance: tool/capability subpaths register into the host tool registry.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the plugin contract this note maps belongs to OpenClaw.
- [Discriminated Union](../../term_dictionary/term_discriminated_union.md) — typed variant modeling; relevance: SDK subpath exports are typed module surfaces grouped by area, the TS discriminated-union pattern.
- [Hermes Plugin](../../term_dictionary/term_hermes_plugin.md) — Hermes's analogous plugin system; relevance: cross-ecosystem parallel of a narrow-import plugin SDK surface.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: an alternative plugin/extension surface the SDK import map sits alongside.

**Docs**
- [pi: Extensions Overview](../pi/pi_extensions_overview.md) — Pi's extension SDK surface; relevance: closest cross-tool parallel to OpenClaw's plugin-SDK import map.
- [pi: SDK Options](../pi/pi_sdk_options.md) — Pi SDK import/config options; relevance: parallels the subpath-import convention this note documents.
- [pi: Packages](../pi/pi_packages.md) — Pi package/module layout; relevance: parallels OpenClaw's narrow-subpath package-exports model.
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — Hermes plugin import surfaces; relevance: same "what to import per plugin type" reference shape.
- [Hermes: Plugins System](../hermes_agent/hermes_plugins_system.md) — Hermes plugin system overview; relevance: cross-ecosystem analog of the SDK import contract.
- [Claude Code: Plugins Overview](../claude_code/cc_plugins_overview.md) — Claude Code plugin model; relevance: parallel coding-agent plugin import/registration overview.
- [Claude Code: Plugin Components](../claude_code/cc_plugin_components.md) — CC plugin building blocks; relevance: parallels the subpath grouping (entry, channel, provider, runtime).
- [Band: SDK Architecture](../band/band_sdk_architecture.md) — Band adapter SDK structure; relevance: cross-tool analog of an import-organized plugin SDK.
- [oc_plugins_sdk_subpaths](oc_plugins_sdk_subpaths.md) (planned, pl25) — the full subpath catalog; relevance: this note's import convention points to that grouped catalog.
- [oc_plugins_sdk_overview_registration_api](oc_plugins_sdk_overview_registration_api.md) (planned, this series, note 2) — the registration API; relevance: the other half of the SDK overview page.
- [oc_plugins_sdk_migration_import_paths](oc_plugins_sdk_migration_import_paths.md) (planned, this series, note 13) — legacy→narrow import map; relevance: operationalizes the import convention this note defines.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions/plugin framework; relevance: consumes these SDK subpaths.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: owns `src/plugin-sdk/` and the generated export map.

**Snippets**
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin-SDK entry usage; relevance: concrete narrow-subpath import in practice.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package/openclaw-field contract; relevance: the `package.json`/`openclaw.plugin.json` surface the imports tie to.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin load/register lifecycle; relevance: shows the SDK surfaces an imported entry reaches.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — narrow setup-helper imports; relevance: exemplifies the narrow-subpath import discipline.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — import migration helper; relevance: enforces moving off deprecated broad/branded import paths.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — Hermes plugin SDK layout; relevance: cross-ecosystem analog of import-grouped SDK modules.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — Hermes manifest schema; relevance: the manifest the import map cross-references for channel config.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest format; relevance: a sibling manifest-driven surface in the same SDK.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor contract; relevance: a typed SDK contract reached via narrow imports.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: how imported plugin entries are loaded at runtime.

### oc_plugins_sdk_overview_registration_api (10t · 12s · 11d)

**Terms**
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — typed plugin↔core contract; relevance: `OpenClawPluginApi.register(api)` is the SDK's central registration surface this note documents.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — host tool/command store; relevance: `api.registerTool`/`registerCommand` populate the host tool/command registry.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool-call mechanism; relevance: registered tools/commands are the function-calling capabilities exposed to the agent.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model-provider plugin; relevance: capability registration includes `registerProvider`/embedding/speech/media providers.
- [Cron](../../term_dictionary/term_cron.md) — scheduled-job runtime; relevance: `scheduleSessionTurn`/`registerSessionSchedulerJob` host hooks are Cron-backed.
- [WebSocket](../../term_dictionary/term_websocket.md) — duplex transport; relevance: gateway discovery + events/lifecycle registration tie into the gateway transport.
- [Gateway Hooks](../../term_dictionary/term_gateway_hooks.md) — host lifecycle hooks; relevance: `registerHook`/`api.on` register typed lifecycle/host hooks documented here.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — tool metadata schema; relevance: `registerToolMetadata`/CLI descriptors register tool/command catalog metadata.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the registration API is OpenClaw's plugin entry surface.
- [Sandbox](../../term_dictionary/term_sandbox.md) — policy/trust boundary; relevance: trusted tool policy + reserved `operator.admin` namespaces gate plugin authority.

**Docs**
- [pi: Extensions API Methods](../pi/pi_extensions_api_methods.md) — Pi extension `register*` methods; relevance: closest parallel to OpenClaw's `OpenClawPluginApi` method reference.
- [pi: Extensions Overview](../pi/pi_extensions_overview.md) — Pi extension surface; relevance: cross-tool analog of the registration-API model.
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — Hermes plugin registration surfaces; relevance: parallels the capability/tool/hook registration table.
- [Hermes: Plugin Extensions & Hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — Hermes hook registration; relevance: parallels `registerHook`/host-hook decision semantics.
- [Hermes: Event Hooks](../hermes_agent/hermes_event_hooks.md) — Hermes event hook contract; relevance: parallels the events/lifecycle + hook-decision-semantics sections.
- [Hermes: Adding a Built-in Tool](../hermes_agent/hermes_adding_built_in_tool.md) — Hermes tool registration; relevance: parallels `registerTool`/`registerCommand`.
- [Claude Code: Plugin Components](../claude_code/cc_plugin_components.md) — CC plugin registration units; relevance: parallel registration-surface taxonomy.
- [Claude Code: OTEL Events Reference](../claude_code/cc_otel_events_reference.md) — CC lifecycle event names; relevance: parallels the events/lifecycle hook catalog.
- [oc_plugins_sdk_overview_imports](oc_plugins_sdk_overview_imports.md) (planned, this series, note 1) — import convention; relevance: the other half of the SDK overview page.
- [oc_plugins_sdk_entrypoints](oc_plugins_sdk_entrypoints.md) (planned, this series, note 3) — `define*PluginEntry` wrappers; relevance: invoke `register(api)` with this `api` surface.
- [oc_plugins_sdk_runtime_namespaces](oc_plugins_sdk_runtime_namespaces.md) (planned, this series, note 9) — `api.runtime` namespaces; relevance: the runtime half of the same `api` object.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions framework; relevance: implements the registration-API surface.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: registers tool/command capabilities via this API.

**Snippets**
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — register/lifecycle hooks; relevance: the lifecycle this API drives.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin entry/register usage; relevance: literal `register(api)` body.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor contract; relevance: the descriptor metadata `registerToolMetadata`/CLI descriptors emit.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skill/tool registration; relevance: a concrete capability-registration consumer.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — gateway HTTP route plumbing; relevance: backs `registerHttpRoute`/`registerGatewayMethod`.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway RPC method registration; relevance: backs `registerGatewayMethod` + reserved-namespace coercion.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: the typed RPC surface registered methods join.
- [snippet_openclaw_context_engine_registry_factories](../../code_snippets/snippet_openclaw_context_engine_registry_factories.md) — context-engine registry; relevance: backs the exclusive-slot `registerContextEngine`.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime/registration; relevance: backs `registerMemoryCapability` exclusive memory slots.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider register/unregister; relevance: cross-ecosystem analog of `registerProvider`.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK register surface; relevance: parallel registration-API layout.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth modes; relevance: the `operator.admin` scope policy reserved namespaces enforce.

### oc_plugins_sdk_entrypoints (10t · 11s · 11d)

**Terms**
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — typed plugin↔core contract; relevance: the four `define*PluginEntry` helpers are core SDK exports.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model-provider plugin; relevance: `definePluginEntry`/`defineSingleProviderPluginEntry` wrap provider plugins.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool-call mechanism; relevance: `defineToolPlugin` defines a tool (function-calling) plugin entry.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed language; relevance: entrypoints are typed factory functions returning plugin objects.
- `TypeBox` (new-term CANDIDATE, NOT yet in vault — rendered as plain code, NOT a link, so it is not a G5 ghost) — TS runtime schema lib; relevance: `defineToolPlugin` infers config/tool param types from TypeBox schemas. See Augmentation Report new-term candidates.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: registration mode + plugin shapes correspond to manifest-declared entries.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: entry helpers are OpenClaw plugin exports.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — host tool store; relevance: `defineToolPlugin` writes `contracts.tools` into the manifest/registry.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — channel plugin surface; relevance: `defineChannelPluginEntry` wires the `ChannelPlugin` adapter.
- [Discriminated Union](../../term_dictionary/term_discriminated_union.md) — typed variant modeling; relevance: registration mode + plugin shapes are modeled as typed variants.
- [Hermes Plugin](../../term_dictionary/term_hermes_plugin.md) — Hermes plugin system; relevance: cross-ecosystem analog of entry/registration helpers.

**Docs**
- [pi: SDK Options](../pi/pi_sdk_options.md) — Pi SDK entry/config options; relevance: parallels the `define*Entry` option/field reference.
- [pi: Custom Provider Registration](../pi/pi_custom_provider_registration.md) — Pi provider entry; relevance: parallels `definePluginEntry`/`defineSingleProviderPluginEntry` for providers.
- [pi: Extensions API Methods](../pi/pi_extensions_api_methods.md) — Pi extension register API; relevance: the `register(api)` the entry wraps.
- [Hermes: Build a Plugin Tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — Hermes plugin entry walkthrough; relevance: parallel "every plugin exports an entry" model.
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — Hermes entry surfaces; relevance: parallels the tool/provider/channel/setup entry split.
- [Claude Code: Plugin Components](../claude_code/cc_plugin_components.md) — CC plugin entry units; relevance: parallel plugin-entry taxonomy.
- [Claude Code: Plugin Quickstart](../claude_code/cc_plugin_quickstart.md) — CC plugin entry quickstart; relevance: parallel default-entry-object pattern.
- [Band: Creating Adapters (Implementation)](../band/band_creating_adapters_implementation.md) — Band adapter entry impl; relevance: cross-tool analog of a plugin entry factory.
- [oc_plugins_sdk_overview_registration_api](oc_plugins_sdk_overview_registration_api.md) (planned, this series, note 2) — the `api` object; relevance: the `register` receives this `api`.
- [oc_plugins_sdk_channel_plugins_walkthrough](oc_plugins_sdk_channel_plugins_walkthrough.md) (planned, this series, note 5) — channel walkthrough; relevance: uses `defineChannelPluginEntry` in context.
- [oc_plugins_sdk_setup_packaging](oc_plugins_sdk_setup_packaging.md) (planned, this series, note 10) — packaging/setup-entry; relevance: `package.json` `extensions`/`setupEntry` point at these entries.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions framework; relevance: hosts the entrypoint/registration framework.
- [repo_hermes_agent_plugins](../../../areas/code_repos/repo_hermes_agent_plugins.md) — Hermes plugin pkg; relevance: cross-ecosystem entry/registration parallel.

**Snippets**
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin-SDK entry definition; relevance: the literal runtime form of these `define*` helpers.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — `package.json` openclaw fields; relevance: `extensions`/`runtimeExtensions`/`setupEntry` the entries are referenced from.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — load/register lifecycle; relevance: registration mode (full/discovery/setup) the entry gates on.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — tool descriptor; relevance: the static metadata `defineToolPlugin` emits.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the `ChannelPlugin` shape `defineChannelPluginEntry` wraps.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: how built `runtimeExtensions`/`runtimeSetupEntry` are loaded.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider entry registration; relevance: cross-ecosystem analog of provider entry helpers.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK entry layout; relevance: parallel entry/registration architecture.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest format; relevance: sibling manifest-declared entry surface.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — setup-entry imports; relevance: the narrow setup-helper families `defineSetupPluginEntry` pairs with.

### oc_plugins_sdk_channel_plugins_concepts (9t · 11s · 12d)

**Terms**
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — channel plugin surface; relevance: the note IS the conceptual model of the `ChannelPlugin` adapter (config/security/pairing/outbound/threading).
- [Channel Kernel](../../term_dictionary/term_channel_kernel.md) — core channel dispatch; relevance: core owns the shared `message` tool, session-key shape, and dispatch the concept describes.
- [WebSocket](../../term_dictionary/term_websocket.md) — duplex transport; relevance: channel inbound/outbound dispatch runs over channel transports (often websocket/long-poll).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: channel plugins are OpenClaw's chat-platform connectors.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — direct-message allowlist policy; relevance: the security/pairing layer is the plugin-owned DM policy + allowlist.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool-call mechanism; relevance: channel capabilities declare which tool/approval actions are exposed.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/identity gate; relevance: inbound mention policy + bot-loop protection gate untrusted senders.
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — agent-client protocol; relevance: channel dispatch feeds the agent-client run path.
- [Sandbox](../../term_dictionary/term_sandbox.md) — policy/trust boundary; relevance: approvals/capabilities gate what a channel-driven agent may do.

**Docs**
- [Claude Code: Build a Channel](../claude_code/cc_build_a_channel.md) — CC channel authoring concept; relevance: closest parallel of the channel-plugin adapter model.
- [Claude Code: Channels Overview](../claude_code/cc_channels_overview.md) — CC channel model; relevance: parallels how channels map to a shared message surface.
- [Claude Code: Channel Reply Tool](../claude_code/cc_channel_reply_tool.md) — CC shared reply tool; relevance: parallels "core owns the shared message tool".
- [Claude Code: Channel Permission Relay](../claude_code/cc_channel_permission_relay.md) — CC channel approval relay; relevance: parallels approvals + channel capabilities.
- [Hermes: Adding a Platform Adapter Plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — Hermes channel adapter concept; relevance: cross-ecosystem analog of the channel adapter surface.
- [Hermes: Messaging — Slack](../hermes_agent/hermes_messaging_slack.md) — Hermes channel example; relevance: concrete inbound/outbound + mention model parallel.
- [Band: WebSocket Agent Channels](../band/band_websocket_agent_channels.md) — Band channel transport; relevance: parallels channel inbound/outbound transport dispatch.
- [oc_plugins_sdk_channel_plugins_walkthrough](oc_plugins_sdk_channel_plugins_walkthrough.md) (planned, this series, note 5) — channel authoring; relevance: the procedure realizing this concept.
- [oc_plugins_sdk_runtime_namespaces](oc_plugins_sdk_runtime_namespaces.md) (planned, this series, note 9) — `api.runtime.channel`; relevance: the runtime mention/media helpers a channel reaches.
- [oc_plugins_sdk_entrypoints](oc_plugins_sdk_entrypoints.md) (planned, this series, note 3) — `defineChannelPluginEntry`; relevance: the entry that wires this channel concept.
- [oc_channels_bot_loop_protection](oc_channels_bot_loop_protection.md) (planned, ch01) — bot-loop policy; relevance: the inbound-mention bot-loop guard this concept references.
- [oc_channels_access_groups](oc_channels_access_groups.md) (planned, ch01) — channel access groups; relevance: the DM/approval allowlist policy the concept gates on.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel framework; relevance: implements this channel-plugin model.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging-channel impl; relevance: inbound/outbound + approval implementation of the concept.
- [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — Hermes messaging gateway; relevance: cross-ecosystem channel-dispatch parallel.

**Snippets**
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the `ChannelPlugin` surface this concept defines.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel kernel dispatch; relevance: the core-owned dispatch the concept contrasts with plugin-owned work.
- [snippet_openclaw_channels_registry_normalize](../../code_snippets/snippet_openclaw_channels_registry_normalize.md) — channel registry normalize; relevance: how channels register into core.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — conversation/session-key mapping; relevance: the session-grammar layer the concept names.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket-mode inbound; relevance: a concrete inbound-transport example.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — channel DM security audit; relevance: the DM-policy/allowlist security layer.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source trust audit; relevance: the inbound-trust boundary the concept enforces.
- [snippet_openclaw_sessions_session_chat_type](../../code_snippets/snippet_openclaw_sessions_session_chat_type.md) — session chat-type resolution; relevance: the base-chat/thread session grammar.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Hermes Slack platform; relevance: parallel channel inbound/outbound concept.
- [snippet_hermes_agent_gw_runner_outbound](../../code_snippets/snippet_hermes_agent_gw_runner_outbound.md) — Hermes outbound runner; relevance: parallels the channel outbound dispatch the concept describes.

### oc_plugins_sdk_channel_plugins_walkthrough (9t · 12s · 11d)

**Terms**
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — typed plugin↔core contract; relevance: the walkthrough uses `openclaw/plugin-sdk/channel-core` helpers throughout.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: Step 1 builds the `package.json` `openclaw.channel` + `openclaw.plugin.json` manifest.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — channel plugin surface; relevance: Step 2 builds the `ChannelPlugin` object via `createChatChannelPlugin`.
- [WebSocket](../../term_dictionary/term_websocket.md) — duplex transport; relevance: the inbound-handler step processes channel transport/webhook events.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/identity gate; relevance: the setup-entry step wires channel credentials/auth + pairing.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the walkthrough targets OpenClaw channel plugins.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — direct-message allowlist; relevance: Step 2's `security.dm` resolver sets the DM policy/allowlist.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin; relevance: the channel-plugin object mirrors the provider-plugin authoring shape.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed language; relevance: every walkthrough file (`channel.ts`, `index.ts`, `setup-entry.ts`) is typed TS.

**Docs**
- [Claude Code: Build a Channel](../claude_code/cc_build_a_channel.md) — CC channel build walkthrough; relevance: closest parallel step-by-step channel authoring guide.
- [Hermes: Adding a Platform Adapter Plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — Hermes channel authoring; relevance: parallel package→adapter→entry→inbound flow.
- [Hermes: Messaging — Teams Bot](../hermes_agent/hermes_messaging_teams_bot.md) — Teams channel example; relevance: the bundled Teams pattern the walkthrough's inbound step cites.
- [Hermes: Messaging — Line](../hermes_agent/hermes_messaging_line.md) — Line channel example; relevance: parallel webhook-inbound channel build.
- [Hermes: Build a Plugin Tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — Hermes plugin build; relevance: parallel package/manifest/entry scaffolding.
- [Band: Creating Adapters (Patterns)](../band/band_creating_adapters_patterns.md) — Band adapter patterns; relevance: cross-tool analog of channel-adapter authoring.
- [Band: Adapter Setup](../band/band_adapter_setup.md) — Band adapter setup; relevance: parallels the setup-entry/wizard step.
- [oc_plugins_sdk_channel_plugins_concepts](oc_plugins_sdk_channel_plugins_concepts.md) (planned, this series, note 4) — channel model; relevance: the concept this walkthrough realizes.
- [oc_plugins_sdk_setup_packaging](oc_plugins_sdk_setup_packaging.md) (planned, this series, note 10) — packaging/setup-entry; relevance: the deep reference Step 1/4 link to.
- [oc_plugins_sdk_testing](oc_plugins_sdk_testing.md) (planned, pl25) — channel test helpers; relevance: Step 6 (Test) links to the SDK testing reference.
- [oc_plugins_sdk_entrypoints](oc_plugins_sdk_entrypoints.md) (planned, this series, note 3) — `defineChannelPluginEntry`; relevance: the entry helper Step 3 wires.

**Repos**
- [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channel framework; relevance: the framework the walkthrough targets.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — setup wizard/CLI; relevance: the setup-entry/wizard Step 4 adds.
- [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: the bundled channel families the walkthrough mirrors.

**Snippets**
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package/manifest contract; relevance: the Step 1 `package.json`/`openclaw.plugin.json` output.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the `ChannelPlugin` object Step 2 builds.
- [snippet_openclaw_channels_slack_socket_mode](../../code_snippets/snippet_openclaw_channels_slack_socket_mode.md) — Slack socket-mode inbound; relevance: a real inbound-handler pattern for Step 5.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel dispatch; relevance: where inbound messages are dispatched after the handler.
- [snippet_openclaw_channels_conversation_resolution](../../code_snippets/snippet_openclaw_channels_conversation_resolution.md) — session/conversation mapping; relevance: the session-grammar wiring of Step 2/5.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — entry definition; relevance: the `index.ts` entry Step 3 wires.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup config wiring; relevance: the setup-entry Step 4 config plumbing.
- [snippet_openclaw_security_audit_channel_dm](../../code_snippets/snippet_openclaw_security_audit_channel_dm.md) — DM security audit; relevance: the `security.dm` policy Step 2 sets.
- [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Hermes Slack inbound/outbound; relevance: cross-ecosystem channel build parallel.
- [snippet_hermes_agent_gw_platform_discord_connect](../../code_snippets/snippet_hermes_agent_gw_platform_discord_connect.md) — Hermes Discord connect; relevance: parallel channel transport/inbound wiring.
- [snippet_hermes_agent_plugins_platform_teams](../../code_snippets/snippet_hermes_agent_plugins_platform_teams.md) — Hermes Teams platform; relevance: the bundled-Teams inbound pattern the walkthrough names.

### oc_plugins_sdk_provider_plugins_walkthrough (9t · 12s · 12d)

**Terms**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model-provider plugin; relevance: the note IS the provider-plugin authoring procedure.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — typed plugin↔core contract; relevance: uses `openclaw/plugin-sdk/provider*` registration helpers.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: a provider plugin fronts an LLM the agent calls.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider/model registry; relevance: Step 2 `catalog`/`registerModelCatalogProvider` populates the model catalog.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool-call mechanism; relevance: provider streaming must support tool-call (function-calling) blocks.
- [Converse API](../../term_dictionary/term_converse_api.md) — Bedrock converse-stream API; relevance: Bedrock-style providers register a converse-stream `api` type.
- [OpenAI Responses API](../../term_dictionary/term_openai_responses_api.md) — OpenAI Responses transport; relevance: `openai-responses-defaults` stream family wraps the Responses transport.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — KV/prompt cache; relevance: provider `isCacheTtlEligible`/cost `cacheRead`/`cacheWrite` hooks gate prompt caching.
- [Model Failover](../../term_dictionary/term_model_failover.md) — provider fallback; relevance: provider `classifyFailoverReason`/`matchesContextOverflowError` hooks drive failover.

**Docs**
- [pi: Custom Provider Registration](../pi/pi_custom_provider_registration.md) — Pi provider authoring; relevance: closest parallel provider-plugin walkthrough.
- [pi: Custom Streaming API](../pi/pi_custom_streaming_api.md) — Pi custom stream transport; relevance: parallels `createStreamFn`/`wrapStreamFn` runtime hooks.
- [pi: Custom Models](../pi/pi_custom_models.md) — Pi dynamic model defs; relevance: parallels `resolveDynamicModel`/dynamic model resolution.
- [pi: Cloud Providers](../pi/pi_cloud_providers.md) — Pi cloud provider config; relevance: parallel provider catalog/auth model.
- [Hermes: Adding an Inference Provider](../hermes_agent/hermes_adding_inference_provider.md) — Hermes provider authoring; relevance: parallel package→register→catalog→hooks flow.
- [Hermes: Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — Hermes model-provider plugin; relevance: the closest sibling provider-plugin authoring doc.
- [Hermes: Provider Runtime](../hermes_agent/hermes_provider_runtime.md) — Hermes provider runtime hooks; relevance: parallels the runtime-hook order (Step 4).
- [Hermes: Provider — AWS Bedrock](../hermes_agent/hermes_provider_aws_bedrock.md) — Bedrock provider example; relevance: the converse-API/`anthropic-by-model` replay family example.
- [oc_plugins_sdk_provider_plugins_clawhub_catalog](oc_plugins_sdk_provider_plugins_clawhub_catalog.md) (planned, this series, note 7) — publish/catalog-order; relevance: the publish + catalog-order half of the provider page.
- [oc_plugins_sdk_runtime_namespaces](oc_plugins_sdk_runtime_namespaces.md) (planned, this series, note 9) — `api.runtime.llm`; relevance: runtime helpers used in Step 4 hooks.
- [oc_providers_models](oc_providers_models.md) (planned, pr05) — provider/model catalog reference; relevance: the user-facing model catalog this walkthrough feeds.
- [oc_plugins_sdk_entrypoints](oc_plugins_sdk_entrypoints.md) (planned, this series, note 3) — `definePluginEntry`/`defineSingleProviderPluginEntry`; relevance: the entry Step 2 uses.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: the providers this walkthrough produces.
- [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — Hermes provider adapters; relevance: cross-ecosystem provider authoring parallel.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions framework; relevance: hosts the provider registration surface.

**Snippets**
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI-compatible provider; relevance: a concrete provider plugin matching Step 2.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider seam; relevance: the Claude beta-header/`service_tier` provider-local barrel example.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: `openai-compatible` replay family + static-catalog example.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator; relevance: dynamic-model proxy + `passthrough-gemini`/`openrouter-thinking` family example.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: where Step 2 catalog rows land.
- [snippet_openclaw_agents_btw_streamSimple_sanitize](../../code_snippets/snippet_openclaw_agents_btw_streamSimple_sanitize.md) — stream-simple sanitize; relevance: the shared stream/replay sanitation provider hooks plug into.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider register lifecycle; relevance: the register/unregister of Step 2.
- [snippet_hermes_agent_plugins_provider_bedrock](../../code_snippets/snippet_hermes_agent_plugins_provider_bedrock.md) — Bedrock provider plugin; relevance: the converse-stream provider example.
- [snippet_hermes_agent_plugins_provider_codex](../../code_snippets/snippet_hermes_agent_plugins_provider_codex.md) — Codex provider; relevance: the OpenAI/Codex Responses stream-family example.
- [snippet_hermes_agent_plugins_provider_openrouter](../../code_snippets/snippet_hermes_agent_plugins_provider_openrouter.md) — OpenRouter provider; relevance: proxy/aggregator dynamic-model parallel.
- [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base contract; relevance: cross-ecosystem provider hook surface parallel.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen provider dispatch; relevance: the extra-capability (image/video/music) registration of Step 5.

### oc_plugins_sdk_provider_plugins_clawhub_catalog (8t · 10s · 11d)

**Terms**
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model-provider plugin; relevance: publishing/cataloging the provider plugin authored in note 6.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider/model registry; relevance: the `catalog.order` reference governs how providers/models sort in the catalog.
- [Model Router](../../term_dictionary/term_model_router.md) — provider/model selection; relevance: catalog order affects provider/model selection routing.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`/package fields; relevance: ClawHub publish requires the `compat`/`build` manifest fields.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: ClawHub is OpenClaw's plugin registry.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model vendors; relevance: published providers connect third-party GenAI endpoints.
- [Provider Routing](../../term_dictionary/term_provider_routing.md) — request routing across providers; relevance: catalog order + `late`/`simple` passes shape provider routing/override.
- [Fallback Provider](../../term_dictionary/term_fallback_provider.md) — backup model provider; relevance: catalog-order `late` overrides and offline static catalogs back fallback behavior.

**Docs**
- [Hermes: Plugins Management](../hermes_agent/hermes_plugins_management.md) — Hermes plugin publish/install; relevance: parallels the publish/install lifecycle of a provider plugin.
- [Hermes: Inference Providers (Cloud)](../hermes_agent/hermes_inference_providers_cloud.md) — Hermes cloud provider catalog; relevance: parallels the published-provider model catalog.
- [Hermes: Provider Routing & Proxies](../hermes_agent/hermes_provider_routing_proxies.md) — Hermes provider routing; relevance: parallels how catalog order affects selection/routing.
- [Claude Code: Marketplace JSON Schema](../claude_code/cc_marketplace_json_schema.md) — CC plugin marketplace schema; relevance: parallel publish-metadata/marketplace contract.
- [Claude Code: Plugins Overview](../claude_code/cc_plugins_overview.md) — CC plugin publish model; relevance: parallel plugin-distribution overview.
- [pi: Cloud Providers](../pi/pi_cloud_providers.md) — Pi cloud provider listing; relevance: parallel provider-catalog ordering reference.
- [oc_plugins_sdk_provider_plugins_walkthrough](oc_plugins_sdk_provider_plugins_walkthrough.md) (planned, this series, note 6) — provider authoring; relevance: the provider this section publishes.
- [oc_plugins_sdk_setup_packaging](oc_plugins_sdk_setup_packaging.md) (planned, this series, note 10) — packaging metadata; relevance: the `compat`/`build` package fields required to publish.
- [oc_clawhub_publishing](oc_clawhub_publishing.md) (planned, cw02) — full ClawHub publish flow; relevance: the deep publish flow this section summarizes.
- [oc_clawhub_quickstart](oc_clawhub_quickstart.md) (planned, cw02) — ClawHub quickstart; relevance: the `clawhub package publish` entry point this cites.
- [oc_providers_models](oc_providers_models.md) (planned, pr05) — model catalog reference; relevance: the catalog the order reference shapes.

**Repos**
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM-provider extensions; relevance: source of the providers being published.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — apps/ClawHub surfaces; relevance: backs the ClawHub publish/catalog surfaces.

**Snippets**
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog assembly; relevance: the runtime catalog the `catalog.order` reference shapes.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — aggregator catalog; relevance: a `late`/override-order provider example.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider catalog; relevance: a `simple`-order plain-API-key provider example.
- [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local provider catalog; relevance: an offline static-catalog publish example.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package/openclaw fields; relevance: the `compat`/`build`/`install` metadata required to publish.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: how published providers register/order at load.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — manifest schema; relevance: the publish-metadata manifest parallel.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: a bundled provider whose static catalog feeds the order reference.
- [snippet_hermes_agent_plugins_provider_nous](../../code_snippets/snippet_hermes_agent_plugins_provider_nous.md) — Nous subscription provider; relevance: parallel published-provider catalog/auth example.

### oc_plugins_sdk_runtime_config_utilities (9t · 11s · 11d)

**Terms**
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — typed plugin↔core contract; relevance: `api.runtime.config` + utilities are SDK-injected helpers.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider/channel plugins; relevance: provider/channel callbacks must use the active runtime config snapshot, not a file snapshot.
- [Cron](../../term_dictionary/term_cron.md) — scheduled/restart runtime; relevance: `afterWrite: { mode: "restart" }` policy governs gateway reload after config writes.
- [Sandbox](../../term_dictionary/term_sandbox.md) — policy/trust boundary; relevance: `selectApplicableRuntimeConfig` resolves credentials under the runtime/policy boundary.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/identity gate; relevance: bot-loop protection guards untrusted inbound senders.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the runtime-config helpers are OpenClaw's injected plugin surface.
- [Deprecation](../../term_dictionary/term_deprecation.md) — managed API sunset; relevance: `loadConfig()`/`writeConfigFile()` are deprecated compat helpers under `runtime-config-load-write`.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — shared credential store; relevance: `selectApplicableRuntimeConfig` resolves SecretRef-backed credentials for the runtime view.
- [Messaging Gateway](../../term_dictionary/term_messaging_gateway.md) — gateway transport hub; relevance: the gateway owns when a config-write restart/reload actually happens.

**Docs**
- [Hermes: Provider Runtime](../hermes_agent/hermes_provider_runtime.md) — Hermes runtime config helpers; relevance: parallels using the active runtime config snapshot on hot paths.
- [Hermes: Tools Runtime](../hermes_agent/hermes_tools_runtime.md) — Hermes tool runtime context; relevance: parallels `ctx.getRuntimeConfig()` inside long-lived tools.
- [Hermes: Gateway Internals](../hermes_agent/hermes_gateway_internals.md) — Hermes gateway reload; relevance: parallels the gateway-owned reload/restart after config writes.
- [pi: Extensions API Methods](../pi/pi_extensions_api_methods.md) — Pi runtime/config injection; relevance: parallel injected-runtime config access.
- [pi: Model Overrides & Compat](../pi/pi_model_overrides_compat.md) — Pi config-override snapshot; relevance: parallels config-snapshot reads + override gating.
- [Claude Code: Hook Configuration Settings](../claude_code/cc_hook_configuration_settings.md) — CC config write/reload; relevance: parallel config-mutation + reload contract.
- [oc_plugins_sdk_runtime_namespaces](oc_plugins_sdk_runtime_namespaces.md) (planned, this series, note 9) — `api.runtime` namespaces; relevance: the namespaces reached through the same `api.runtime`.
- [oc_plugins_sdk_migration](oc_plugins_sdk_migration.md) (planned, this series, note 12) — config load/write migration; relevance: Step 1 of migration is exactly these config helpers.
- [oc_gateway_configuration](oc_gateway_configuration.md) (planned, gw02) — gateway config model; relevance: the config file these helpers mutate.
- [oc_concepts_session_pruning](oc_concepts_session_pruning.md) (planned, co06) — session/runtime lifecycle; relevance: the runtime snapshot/revision these helpers advance.
- [oc_plugins_sdk_overview_registration_api](oc_plugins_sdk_overview_registration_api.md) (planned, this series, note 2) — `api` object fields; relevance: `api.config`/`api.runtime` fields this note uses.

**Repos**
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: owns config reload/restart after `mutateConfigFile`.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — sessions/runtime store; relevance: the runtime snapshot + cache-key the writes advance.

**Snippets**
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway-side plugin config load; relevance: mirrors the config-snapshot contract.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin/config load; relevance: the runtime config load path these helpers read from.
- [snippet_openclaw_gateway_server_startup_post_attach_runtime](../../code_snippets/snippet_openclaw_gateway_server_startup_post_attach_runtime.md) — post-attach runtime; relevance: how the gateway applies a config-write reload/restart.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — plugin fallback context; relevance: the runtime-config context provided to plugin callbacks.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — config write/setup; relevance: a concrete config-mutation path.
- [snippet_openclaw_channels_kernel_dispatch](../../code_snippets/snippet_openclaw_channels_kernel_dispatch.md) — channel dispatch + bot-loop; relevance: where `botLoopProtection` facts are applied before dispatch.
- [snippet_openclaw_security_audit_channel_source](../../code_snippets/snippet_openclaw_security_audit_channel_source.md) — channel source trust; relevance: the bot-pair/untrusted-sender guard the utility enforces.
- [snippet_openclaw_gateway_auth_modes_helpers](../../code_snippets/snippet_openclaw_gateway_auth_modes_helpers.md) — gateway auth modes; relevance: the credential/runtime-config boundary `selectApplicableRuntimeConfig` respects.
- [snippet_hermes_agent_cli_config_loading](../../code_snippets/snippet_hermes_agent_cli_config_loading.md) — CLI config loading; relevance: cross-ecosystem load-once-at-boundary parallel.
- [snippet_hermes_agent_cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — tool config resolution; relevance: parallel passed-config-on-hot-paths pattern.
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import; relevance: the narrow `config-mutation`/`runtime-config-snapshot` subpaths this note recommends.

### oc_plugins_sdk_runtime_namespaces (10t · 12s · 12d)

**Terms**
- [Subagent](../../term_dictionary/term_subagent.md) — embedded background agent; relevance: `api.runtime.subagent` runs/manages subagent sessions.
- [Text-to-Speech](../../term_dictionary/term_text_to_speech.md) — TTS synthesis; relevance: `api.runtime.tts` is the TTS helper namespace.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — STT transcription; relevance: `api.runtime.mediaUnderstanding`/`stt` cover transcription.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: `api.runtime.llm.complete` is the injected host-owned LLM call.
- [Voice Call](../../term_dictionary/term_voice_call.md) — telephony/realtime voice; relevance: nodes/talk + media namespaces back voice-call plugins.
- [Function Calling](../../term_dictionary/term_function_calling.md) — agent tool-call mechanism; relevance: `api.runtime.tools` exposes tool factories/registration.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — provider/model registry; relevance: `api.runtime.modelAuth`/llm resolve models from the catalog.
- [Multimodal](../../term_dictionary/term_multimodal.md) — image/audio/video understanding; relevance: `api.runtime.mediaUnderstanding`/`imageGeneration` are multimodal helpers.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming STT; relevance: the media/voice namespaces expose realtime transcription helpers.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — embedded agent executor; relevance: `api.runtime.agent.runEmbeddedAgent` uses the same harness selection as channel replies.

**Docs**
- [Hermes: Tools Runtime](../hermes_agent/hermes_tools_runtime.md) — Hermes runtime helper surface; relevance: closest parallel to the injected `api.runtime` namespaces.
- [Hermes: STT Transcription](../hermes_agent/hermes_stt_transcription.md) — Hermes STT runtime; relevance: parallels `api.runtime.mediaUnderstanding`/`stt`.
- [Hermes: TTS Providers](../hermes_agent/hermes_tts_providers.md) — Hermes TTS; relevance: parallels `api.runtime.tts`.
- [Hermes: Image Generation](../hermes_agent/hermes_image_generation.md) — Hermes image gen; relevance: parallels `api.runtime.imageGeneration`.
- [Hermes: Tools Reference — Platform Media](../hermes_agent/hermes_tools_reference_platform_media.md) — Hermes media helpers; relevance: parallels `api.runtime.media`/`channel.media`.
- [pi: Extensions API Methods](../pi/pi_extensions_api_methods.md) — Pi injected runtime helpers; relevance: parallel injected-helper namespace model.
- [Claude Code: Subagent Configuration Reference](../claude_code/cc_subagent_configuration_reference.md) — CC subagent runtime; relevance: parallels `api.runtime.subagent`.
- [oc_plugins_sdk_runtime_config_utilities](oc_plugins_sdk_runtime_config_utilities.md) (planned, this series, note 8) — config/utility half; relevance: the config + utility half of the same `api.runtime`.
- [oc_plugins_sdk_provider_plugins_walkthrough](oc_plugins_sdk_provider_plugins_walkthrough.md) (planned, this series, note 6) — provider hooks; relevance: providers reach `api.runtime.llm`/`modelAuth` in runtime hooks.
- [oc_nodes_talk](oc_nodes_talk.md) (planned, nd02) — Talk/voice nodes; relevance: `api.runtime.nodes`/talk back the voice-call namespaces.
- [oc_tools_subagents](oc_tools_subagents.md) (planned, to07) — subagent tool; relevance: the user-facing subagent surface `api.runtime.subagent` mirrors.
- [oc_plugins_sdk_overview_registration_api](oc_plugins_sdk_overview_registration_api.md) (planned, this series, note 2) — `api` object; relevance: `api.runtime` is one field on the registration `api` object.

**Repos**
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extensions; relevance: implements the tts/stt/media namespace helpers.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: backs `api.runtime.agent` identity/session/embedded-run helpers.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — voice/phone channels; relevance: backs the nodes/talk voice-call namespaces.

**Snippets**
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — ElevenLabs TTS; relevance: backs `api.runtime.tts.textToSpeech`/`listVoices`.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT; relevance: backs `api.runtime.mediaUnderstanding.transcribeAudioFile`.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS; relevance: a local TTS provider under the tts namespace.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call audio stream; relevance: backs the nodes/talk/media voice namespaces.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — voice-call transcription; relevance: realtime-transcription helper under the media namespace.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine; relevance: backs `api.runtime.tools` memory tool factories + state store.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime; relevance: the SQLite-backed keyed `api.runtime.state` store parallel.
- [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — model catalog; relevance: `api.runtime.modelAuth`/llm resolve models from it.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS routing; relevance: cross-ecosystem `runtime.tts` routing parallel.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription helper; relevance: cross-ecosystem `runtime.stt` parallel.
- [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen dispatch; relevance: parallel media-generation runtime namespace.
- [snippet_openclaw_gateway_server_methods_misc](../../code_snippets/snippet_openclaw_gateway_server_methods_misc.md) — gateway RPC methods; relevance: how `api.runtime.nodes.invoke` routes over Gateway RPC from CLI.

### oc_plugins_sdk_setup_packaging (9t · 11s · 11d)

**Terms**
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: the note documents the `package.json` `openclaw` field + `openclaw.plugin.json` manifest.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — typed plugin↔core contract; relevance: the setup-entry imports narrow plugin-SDK setup helpers.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin; relevance: packaging covers provider (and channel) plugin baselines incl. `compat`/`build`.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the `openclaw` package field is OpenClaw's plugin metadata surface.
- [Deprecation](../../term_dictionary/term_deprecation.md) — managed API sunset; relevance: `compat.pluginApi`/`minGatewayVersion` version gating + legacy `showInSetup` aliases.
- [Third-Party GenAI Services](../../term_dictionary/term_third_party_genai_services.md) — external model/connectors; relevance: channel/provider plugins package third-party connectors.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — channel plugin surface; relevance: `openclaw.channel` metadata describes the channel package for setup/picker surfaces.
- [Cron](../../term_dictionary/term_cron.md) — restart/reload runtime; relevance: deferred full load + install flows tie into gateway listen/restart timing.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/identity gate; relevance: `expectedIntegrity`/`minHostVersion` enforce trusted-install integrity gates.

**Docs**
- [Hermes: Plugins Management](../hermes_agent/hermes_plugins_management.md) — Hermes plugin packaging/install; relevance: closest parallel of plugin packaging metadata.
- [Hermes: Build a Plugin Tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — Hermes plugin scaffold; relevance: parallels `package.json`/manifest packaging.
- [Hermes: Env Vars — Providers, Auth, Tools](../hermes_agent/hermes_env_vars_providers_auth_tools.md) — Hermes env-var manifest; relevance: parallels `setup.providers[].envVars`/`channelEnvVars`.
- [Claude Code: Plugin Manifest Schema](../claude_code/cc_plugin_manifest_schema.md) — CC plugin manifest; relevance: closest parallel to `openclaw.plugin.json` packaging.
- [Claude Code: Marketplace JSON Schema](../claude_code/cc_marketplace_json_schema.md) — CC marketplace/install metadata; relevance: parallels `openclaw.install`/ClawHub metadata.
- [pi: Packages](../pi/pi_packages.md) — Pi package metadata; relevance: parallel package-metadata model.
- [pi: Development](../pi/pi_development.md) — Pi local dev/install; relevance: parallels local/dev install paths + deferred load.
- [oc_plugins_sdk_setup_config_schema_wizards](oc_plugins_sdk_setup_config_schema_wizards.md) (planned, this series, note 11) — config-schema/wizard half; relevance: the second half of the setup page.
- [oc_plugins_manifest](oc_plugins_manifest.md) (planned, pl04) — full manifest schema; relevance: the deep manifest reference this note links to.
- [oc_clawhub_publishing](oc_clawhub_publishing.md) (planned, cw02) — ClawHub publish; relevance: the publish flow the packaging metadata feeds.
- [oc_plugins_sdk_entrypoints](oc_plugins_sdk_entrypoints.md) (planned, this series, note 3) — entry points; relevance: `extensions`/`setupEntry` package fields point at these entries.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions framework; relevance: loads extensions from `openclaw.extensions` entry points.
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/wizard; relevance: the setup-entry/single-account promotion + install flow.
- [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — apps/ClawHub; relevance: backs the install/onboarding surfaces packaging metadata drives.

**Snippets**
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package/openclaw fields; relevance: the package-contract this note specifies.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — plugin entry; relevance: the `extensions`/`setupEntry` entries packaging points at.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — load lifecycle; relevance: deferred-full-load + setup-entry loading windows.
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup config; relevance: the setup-entry config plumbing.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — narrow setup imports; relevance: the narrow setup-helper imports the setup-entry uses.
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — wizard prompter; relevance: the onboarding install-on-demand prompts packaging enables.
- [snippet_openclaw_gateway_server_plugins_runtime_load](../../code_snippets/snippet_openclaw_gateway_server_plugins_runtime_load.md) — runtime plugin load; relevance: how packaged `runtimeExtensions` are discovered/loaded.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — manifest schema; relevance: parallel manifest packaging contract.
- [snippet_hermes_agent_cli_setup_installer](../../code_snippets/snippet_hermes_agent_cli_setup_installer.md) — plugin installer; relevance: cross-ecosystem npm/ClawHub install parallel.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest; relevance: a sibling manifest packaging surface.

### oc_plugins_sdk_setup_config_schema_wizards (9t · 10s · 11d)

**Terms**
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema validation language; relevance: `buildChannelConfigSchema` produces the channel-config JSON Schema.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — typed plugin↔core contract; relevance: config-schema primitives + builder live on plugin-SDK subpaths.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: schemas are published via `openclaw.plugin.json#channelConfigs`.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/identity gate; relevance: setup wizards collect credentials/secrets (tokens, env vars).
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: `openclaw onboard` is the wizard host.
- [Cron](../../term_dictionary/term_cron.md) — restart/reload runtime; relevance: install/finalize ties into gateway reload after config writes.
- [DM Policy](../../term_dictionary/term_dm_policy.md) — direct-message allowlist; relevance: the `ChannelSetupWizard` collects `dmPolicy`/`allowFrom`.
- `TypeBox` (new-term CANDIDATE, NOT yet in vault — rendered as plain code, NOT a link, so it is not a G5 ghost) — TS runtime schema lib; relevance: `buildJsonChannelConfigSchema` accepts a TypeBox schema. See Augmentation Report new-term candidates.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed language; relevance: schema builders + wizard objects are typed TS.
- [Credential Pool](../../term_dictionary/term_credential_pool.md) — shared credential store; relevance: wizard credentials resolve into SecretRef-backed config.

**Docs**
- [Hermes: Build a Plugin Tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — Hermes config-schema/wizard; relevance: parallels config-schema + setup-wizard authoring.
- [Hermes: Plugins Management](../hermes_agent/hermes_plugins_management.md) — Hermes plugin config/install; relevance: parallels publish/install + config validation.
- [pi: SDK Options](../pi/pi_sdk_options.md) — Pi config-schema options; relevance: parallel plugin config-schema definition.
- [pi: Provider Auth](../pi/pi_provider_auth.md) — Pi auth/setup flow; relevance: parallels the credential-collecting setup wizard.
- [Claude Code: Plugin Manifest Schema](../claude_code/cc_plugin_manifest_schema.md) — CC config schema; relevance: parallel manifest config-schema contract.
- [Claude Code: Plugin Quickstart](../claude_code/cc_plugin_quickstart.md) — CC setup quickstart; relevance: parallel setup/config flow.
- [oc_plugins_sdk_setup_packaging](oc_plugins_sdk_setup_packaging.md) (planned, this series, note 10) — packaging half; relevance: the packaging half this continues.
- [oc_plugins_manifest](oc_plugins_manifest.md) (planned, pl04) — full manifest schema; relevance: where `channelConfigs` schemas are published.
- [oc_gateway_secrets](oc_gateway_secrets.md) (planned, gw05) — secrets/SecretRef; relevance: where wizard-collected credentials are stored.
- [oc_start_wizard](oc_start_wizard.md) (planned, st02) — onboarding wizard; relevance: `openclaw onboard` the setup wizard plugs into.
- [oc_plugins_sdk_channel_plugins_walkthrough](oc_plugins_sdk_channel_plugins_walkthrough.md) (planned, this series, note 5) — channel build; relevance: the channel whose config schema/wizard this defines.

**Repos**
- [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/setup wizard; relevance: implements the setup-wizard flow + `createSetupTranslator`.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions framework; relevance: installs/loads the configured plugin.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security/secrets; relevance: the credential/SecretRef handling wizards collect into.

**Snippets**
- [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — setup config/schema; relevance: the config-schema-driven setup config plumbing.
- [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — wizard prompter; relevance: the interactive setup-wizard credential prompts.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — narrow setup imports; relevance: the narrow `setup-runtime`/`setup-tools` helper imports.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway plugin config; relevance: gateway-side plugin config-schema validation.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the `ChannelPlugin` the `ChannelSetupWizard` belongs to.
- [snippet_openclaw_skills_manifest_format](../../code_snippets/snippet_openclaw_skills_manifest_format.md) — skill manifest/schema; relevance: a sibling schema-published surface.
- [snippet_hermes_agent_cli_setup_wizard](../../code_snippets/snippet_hermes_agent_cli_setup_wizard.md) — Hermes setup wizard; relevance: cross-ecosystem setup-wizard parallel.
- [snippet_hermes_agent_cli_config_validate](../../code_snippets/snippet_hermes_agent_cli_config_validate.md) — config validation; relevance: parallel JSON-Schema config validation.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — manifest schema; relevance: parallel config-schema-in-manifest contract.

### oc_plugins_sdk_migration (9t · 11s · 12d)

**Terms**
- [Deprecation](../../term_dictionary/term_deprecation.md) — managed API sunset; relevance: the note IS the deprecation/migration policy for broad SDK surfaces.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — typed plugin↔core contract; relevance: migrating from broad to narrow `openclaw/plugin-sdk/<subpath>` imports.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model-provider plugin; relevance: provider convenience seams + discovery types are among the removed/migrated surfaces.
- [Voice Call](../../term_dictionary/term_voice_call.md) — realtime/telephony voice; relevance: the Talk/realtime-voice migration plan is a dedicated section.
- [Speech-to-Text](../../term_dictionary/term_speech_to_text.md) — STT transcription; relevance: realtime voice migration covers STT/TTS provider seams + `talk.session.*` STT.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the migration hardens OpenClaw's plugin contract.
- [Gateway Hooks](../../term_dictionary/term_gateway_hooks.md) — host lifecycle hooks; relevance: `deactivate`→`gateway_stop`, `subagent_spawning`→core binding hook migrations.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — host tool/command store; relevance: `command-auth`→`command-status` help builders + tool-result middleware migration.
- [Authentication](../../term_dictionary/term_authentication.md) — credential/identity gate; relevance: `providerAuthEnvVars`→`setup.providers[].envVars` + external-auth-provider manifest migration.

**Docs**
- [Claude Code: SDK Hooks Troubleshooting](../claude_code/cc_sdk_hooks_troubleshooting.md) — CC hook/SDK migration issues; relevance: parallels migrating off deprecated hook/SDK surfaces.
- [Claude Code: Plugins Overview](../claude_code/cc_plugins_overview.md) — CC plugin model evolution; relevance: parallel plugin-architecture modernization.
- [Hermes: Plugins Management](../hermes_agent/hermes_plugins_management.md) — Hermes plugin lifecycle; relevance: parallels deprecation/compatibility-window management.
- [Hermes: Provider Runtime](../hermes_agent/hermes_provider_runtime.md) — Hermes provider hook migration; relevance: parallels provider discovery→catalog type + thinking-hook migration.
- [Hermes: Event Hooks](../hermes_agent/hermes_event_hooks.md) — Hermes hook rename contract; relevance: parallels `deactivate`→`gateway_stop` hook-rename migrations.
- [pi: Extensions Events & Lifecycle](../pi/pi_extensions_events_lifecycle.md) — Pi lifecycle hooks; relevance: parallels lifecycle-hook deprecation/migration.
- [pi: Compaction Extensions](../pi/pi_compaction_extensions.md) — Pi replay/compaction migration; relevance: parallels the replay-policy/compaction provider-hook migration.
- [oc_plugins_sdk_migration_import_paths](oc_plugins_sdk_migration_import_paths.md) (planned, this series, note 13) — import-path table; relevance: the legacy→modern mapping this narrative references.
- [oc_plugins_sdk_overview_imports](oc_plugins_sdk_overview_imports.md) (planned, this series, note 1) — import convention; relevance: the narrow-import target state migration moves toward.
- [oc_plugins_sdk_runtime_config_utilities](oc_plugins_sdk_runtime_config_utilities.md) (planned, this series, note 8) — config helpers; relevance: Step 1 migrates these `loadConfig`/`writeConfigFile` helpers.
- [oc_plugins_compatibility](oc_plugins_compatibility.md) (planned, pl02) — plugin compat policy; relevance: the compatibility-window policy this migration follows.
- [oc_refactor_acp](oc_refactor_acp.md) (planned, rx01) — ACP refactor; relevance: parallel breaking-clean migration in the same ecosystem.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions framework; relevance: plugins that must migrate off `extension-api`/`infra-runtime`/`compat`.
- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extensions; relevance: affected by the Talk/realtime-voice migration plan.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: owns the new `talk.session.*`/`talk.client.*` RPC and `gateway_stop` hook.

**Snippets**
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — import migration; relevance: the broad→narrow import rewrite this guide prescribes.
- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle hooks; relevance: the `deactivate`→`gateway_stop` lifecycle-hook migration.
- [snippet_openclaw_gateway_server_impl_config_plugins](../../code_snippets/snippet_openclaw_gateway_server_impl_config_plugins.md) — gateway config plugins; relevance: the config-runtime load/write migration target.
- [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — voice-call audio; relevance: surfaces moving onto the shared Talk session controller.
- [snippet_openclaw_voice_call_media_stream_transcription](../../code_snippets/snippet_openclaw_voice_call_media_stream_transcription.md) — voice-call transcription; relevance: the `talk.transcription.*`→`talk.session.*` migration.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider seam; relevance: the provider-local barrel pattern replacing branded SDK seams.
- [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter provider; relevance: provider discovery→catalog type migration example.
- [snippet_openclaw_gateway_rpc_protocol_schema_groups](../../code_snippets/snippet_openclaw_gateway_rpc_protocol_schema_groups.md) — RPC schema groups; relevance: the new unified `talk.session.*` RPC vocabulary.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — entry/import usage; relevance: the modern entry/import shape migration targets.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: parallel provider-hook (discovery→catalog) migration surface.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime; relevance: `registerMemoryEmbeddingProvider`→`registerEmbeddingProvider` migration.

### oc_plugins_sdk_migration_import_paths (9t · 10s · 11d)

**Terms**
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — typed plugin↔core contract; relevance: the table maps every legacy import to its narrow plugin-SDK subpath.
- [Deprecation](../../term_dictionary/term_deprecation.md) — managed API sunset; relevance: each row is a deprecated → replacement import mapping.
- [TypeScript](../../term_dictionary/term_typescript.md) — typed language; relevance: entries are TS module import specifiers.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — model-provider plugin; relevance: provider/channel seam imports are mapped to generic subpaths.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — `openclaw.plugin.json`; relevance: config-runtime imports map to manifest-published config subpaths.
- [OpenClaw](../../term_dictionary/term_openclaw.md) — the product; relevance: the subpaths are OpenClaw's `openclaw/plugin-sdk/*` export map.
- [Channel Adapter](../../term_dictionary/term_channel_adapter.md) — channel plugin surface; relevance: many rows map channel route/inbound/outbound/approval seams to narrow channel subpaths.
- [JSON Schema](../../term_dictionary/term_json_schema.md) — schema validation; relevance: `channel-config-schema*` subpath rows map config-schema builders.
- [Tool Registry](../../term_dictionary/term_tool_registry.md) — host tool/command store; relevance: `command-auth`/`command-status` import rows cover tool/command surfaces.

**Docs**
- [oc_plugins_sdk_migration](oc_plugins_sdk_migration.md) (planned, this series, note 12) — migration narrative; relevance: the narrative this table belongs to.
- [oc_plugins_sdk_overview_imports](oc_plugins_sdk_overview_imports.md) (planned, this series, note 1) — import convention; relevance: the convention the table operationalizes row-by-row.
- [oc_plugins_sdk_subpaths](oc_plugins_sdk_subpaths.md) (planned, pl25) — full subpath catalog; relevance: the canonical destination subpaths each row maps to.
- [Hermes: Plugins System](../hermes_agent/hermes_plugins_system.md) — Hermes plugin import surfaces; relevance: parallel narrow-import organization reference.
- [Hermes: Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — Hermes import surfaces; relevance: parallel per-type import mapping.
- [pi: Packages](../pi/pi_packages.md) — Pi package/import layout; relevance: parallel import-path organization model.
- [pi: Extensions API Methods](../pi/pi_extensions_api_methods.md) — Pi import→method mapping; relevance: parallel import-to-API reference.
- [Claude Code: Plugin Components](../claude_code/cc_plugin_components.md) — CC import/component map; relevance: parallel component-to-import reference.
- [Band: SDK Reference — Adapters](../band/band_sdk_reference_adapters.md) — Band adapter import reference; relevance: cross-tool analog of an SDK import reference table.
- [Band: SDK Overview](../band/band_sdk_overview.md) — Band SDK surface; relevance: parallel SDK import-surface catalog.
- [oc_plugins_sdk_runtime_config_utilities](oc_plugins_sdk_runtime_config_utilities.md) (planned, this series, note 8) — config subpaths; relevance: the `config-contracts`/`config-mutation` rows this table lists.

**Repos**
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions framework; relevance: consumers of the mapped import paths.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — OpenClaw monorepo; relevance: owns the `src/plugin-sdk/` source the table maps to.

**Snippets**
- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — migration import rewrite; relevance: the legacy→narrow import rewrite this table drives.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — entry/import usage; relevance: uses the modern narrow import paths.
- [snippet_openclaw_wizard_setup_imports](../../code_snippets/snippet_openclaw_wizard_setup_imports.md) — narrow setup imports; relevance: the `setup-runtime`/`setup-tools` import rows in practice.
- [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: the `channel-core`/`channel-outbound` import rows' target surface.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider seam; relevance: the provider-local-barrel rows replacing branded imports.
- [snippet_openclaw_gateway_server_http_plugin_routing](../../code_snippets/snippet_openclaw_gateway_server_http_plugin_routing.md) — gateway routing; relevance: the `gateway-runtime` import rows' target surface.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime; relevance: the `memory-host-*` import rows' target surface.
- [snippet_openclaw_plugin_package_contract](../../code_snippets/snippet_openclaw_plugin_package_contract.md) — package/openclaw fields; relevance: the package-export subset the table is generated from.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK layout; relevance: parallel narrow-import SDK structure.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: the `provider-*` import rows' target surface.

## Undigested Terms Plan

> Per master: OpenClaw vocabulary terms are subjects of doc pages → digested as `oc_*` doc notes, NOT new `term_dictionary` entries. The only `term_dictionary` interaction is LINKING existing terms. Expect **0 new term_dictionary captures**.

| Term (appears in pl24 source) | Disposition |
|---|---|
| plugin SDK / `OpenClawPluginApi` / `register(api)` | Documented in `oc_plugins_sdk_overview_*` notes; LINK existing `term_plugin_sdk`. |
| `define*PluginEntry` (tool/plugin/channel/setup entry) | Documented in `oc_plugins_sdk_entrypoints` (note 3); not a term. |
| channel plugin / inbound mention policy / bot-loop protection | Documented in `oc_plugins_sdk_channel_plugins_*`; LINK `term_websocket`, `term_authentication`. |
| provider plugin / dynamic model resolution / catalog order | Documented in `oc_plugins_sdk_provider_plugins_*`; LINK `term_provider_plugin`, `term_model_catalog`, `term_model_router`. |
| `api.runtime` namespaces (agent/llm/subagent/tts/stt/nodes/tasks/media/…) | Documented in `oc_plugins_sdk_runtime_namespaces`; LINK `term_subagent`, `term_text_to_speech`, `term_speech_to_text`, `term_llm`, `term_voice_call`. |
| `openclaw.plugin.json` manifest / `package.json` `openclaw` field | Documented in `oc_plugins_sdk_setup_packaging`; LINK existing `term_plugin_manifest`. |
| `buildChannelConfigSchema` / config schema / setup wizard | Documented in `oc_plugins_sdk_setup_config_schema_wizards`; LINK `term_json_schema`. |
| broad-surface deprecation / migration / import-path map | Documented in `oc_plugins_sdk_migration*`; LINK existing `term_deprecation`. |
| `afterWrite` config write policy / `mutateConfigFile` | Documented in `oc_plugins_sdk_runtime_config_utilities`; config-write mechanism, not a reusable term. |

**New `term_dictionary` candidates: NONE.** No genuinely cross-cutting, vault-reusable term lacks an existing note or a doc-page home. All vocabulary is either OpenClaw-specific config/API (→ `oc_*` docs) or already a term (`term_plugin_sdk`, `term_plugin_manifest`, `term_provider_plugin`, `term_oauth`, `term_websocket`, `term_function_calling`, `term_subagent`, `term_text_to_speech`, `term_speech_to_text`, `term_voice_call`, `term_model_catalog`, `term_model_router`, `term_json_schema`, `term_deprecation`, `term_typescript`). Augment re-runs the Step 2d scan to confirm.

## Term-Note Authoring Requirements


## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (13 notes, P3). All gates must PASS before commit.

| Gate | Check | Tool / Method | Pass criterion |
|---|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` | YAML field order/forbidden-fields OK; `## Overview` + `## Related Notes` present; bold footer present. |
| G2 | Grounding | diff each note vs `inbox/openclaw_docs/plugins/<page>.md` | No hallucinated API/method/field; code snippets verbatim. |
| G3 | Density + Coverage | line/word/code caps + Section Coverage Map | ≤400 lines, ≤2,500 words, ≤6 code blocks; every mapped H2/H3 covered; one BB/note. |
| G4 | Cross-Reference | `## Related Notes` count | ≥6 relevancy-selected term links + repo/sibling/other, each with relevance statement. |
| G5 | Ghost-reference | ghost-note scan / DB existence | 0 links to non-existent notes (planned `oc_*`/`entry_openclaw_docs` resolve post-execution). |
| G6 | Broken-link | `/tessellum-fix-broken-links` + reindex | 0 broken relative paths. |
| G7 | Discoverability (inbound) | `note_links` query | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/`. |
| G8 | In-degree ≥1 / anti-island | `in_degree` column post-reindex | Each new note `in_degree ≥1` (satisfied via `entry_openclaw_docs.md`). |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note | Backs the standing no-mid-paragraph-break rule; catches subagent hard-wrap habit |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_sdk_overview_imports oc_plugins_sdk_overview_registration_api oc_plugins_sdk_entrypoints oc_plugins_sdk_channel_plugins_concepts oc_plugins_sdk_channel_plugins_walkthrough oc_plugins_sdk_provider_plugins_walkthrough oc_plugins_sdk_provider_plugins_clawhub_catalog oc_plugins_sdk_runtime_config_utilities oc_plugins_sdk_runtime_namespaces oc_plugins_sdk_setup_packaging oc_plugins_sdk_setup_config_schema_wizards oc_plugins_sdk_migration oc_plugins_sdk_migration_import_paths"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + required sections
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  for s in ${(s:|:)REQ_SECTIONS}; do grep -qF "$s" "$f" || echo "$n MISSING SECTION: $s"; done
  # require source_url
  [ "$REQUIRE_SOURCE_URL" = "1" ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "$n MISSING source_url"; }
  # require ≥1 sibling oc_ cross-link in Related Notes
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "$n NO SIBLING $SIBLING_PREFIX LINK"
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
done

# G1 YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
```

## Density Re-Assessment

| # | Note | BB | ~Words | Code (≤6) | Within caps? |
|---|---|---|---:|---|---|
| 1 | oc_plugins_sdk_overview_imports | model | 600 | ≤4 | ✅ |
| 2 | oc_plugins_sdk_overview_registration_api | model | 700 | ≤4 | ✅ |
| 3 | oc_plugins_sdk_entrypoints | model | 650 | ≤6 (7 src fences trimmed) | ✅ |
| 4 | oc_plugins_sdk_channel_plugins_concepts | concept | 650 | ≤4 | ✅ |
| 5 | oc_plugins_sdk_channel_plugins_walkthrough | procedure | 700 | ≤6 | ✅ |
| 6 | oc_plugins_sdk_provider_plugins_walkthrough | procedure | 750 | ≤6 (from 24-fence page) | ✅ |
| 7 | oc_plugins_sdk_provider_plugins_clawhub_catalog | procedure | 450 | ≤4 | ✅ |
| 8 | oc_plugins_sdk_runtime_config_utilities | procedure | 650 | ≤6 (from 27-fence page) | ✅ |
| 9 | oc_plugins_sdk_runtime_namespaces | model | 700 | ≤6 (selective namespace examples) | ✅ |
| 10 | oc_plugins_sdk_setup_packaging | procedure | 650 | ≤6 (from 20-fence page) | ✅ |
| 11 | oc_plugins_sdk_setup_config_schema_wizards | procedure | 550 | ≤6 | ✅ |
| 12 | oc_plugins_sdk_migration | procedure | 700 | ≤6 (from 16-fence page) | ✅ |
| 13 | oc_plugins_sdk_migration_import_paths | model | 550 | ≤2 (table-dominant) | ✅ |

No note approaches caps after splitting. The three code-densest pages (sdk-provider-plugins 24, sdk-runtime 27, sdk-setup 20 fences) each split so every note stays ≤6 code blocks; `sdk-entrypoints` (7 fences, one note) reproduces only the canonical signature per `define*` helper to land ≤6.

## Entry Point Decision (inherited from master)

Contributes **13 rows** to `entry_openclaw_docs.md` (CREATED as master pre-step W1, `building_block: navigation`) under a **Plugins → SDK (pl24)** cluster. Each new note receives its entry-point back-link at finalization (satisfies G7/G8: ≥1 outside-folder inbound link + `in_degree ≥1`). No separate child entry point — the master `entry_openclaw_docs.md` is the single hub for all 105 sub-plans.

## Inlinks (existing notes → new notes)


- `entry_openclaw_docs.md` (planned, master W1) → **all 13 notes** (primary in-degree source).
- `repo_openclaw_extensions` → notes 1, 2, 3, 10, 11, 12, 13 (extensions framework consuming the SDK).
- `repo_openclaw_extensions_llm_providers` → notes 6, 7 (provider-plugin authoring).
- `repo_openclaw_channels` / `repo_openclaw_channels_messaging` → notes 4, 5 (channel-plugin authoring).
- `repo_openclaw_extensions_voice_speech` → notes 9, 12 (runtime tts/stt namespaces; voice migration).
- `repo_openclaw_gateway` → note 8 (gateway-owned config reload).
- `repo_openclaw_cli_wizard` → notes 5, 10, 11 (setup-entry/wizard).
- `term_plugin_sdk` → notes 1, 2, 3, 13 (SDK term ↔ SDK docs).
- `term_plugin_manifest` → notes 10, 11 (manifest term ↔ packaging/schema docs).
- `term_provider_plugin` → notes 6, 7 (provider term ↔ provider docs).
- `term_deprecation` → notes 12, 13 (deprecation term ↔ migration docs).

## Pacing Rules (inherited from master)

One execution phase. Cap dynamic-workflow fan-out at ~30 agents/run; embed the per-note manifest in the script; re-read each source page (config/signature snippets verbatim); one BB per note. Run all 8 gates before commit; reindex incrementally; verify `note_links` + 0 broken links + `in_degree ≥1`. `git pull --rebase --autostash origin main` first; commit + push per wave; **no Claude co-author trailer.**

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending (status: ready) |

## Augmentation Report (2026-06-21)



**Per-note locked counts (terms · snippets · docs · repos; all floors met):**

| # | Note | Terms | Snippets | Docs | Repos | Existing docs | Floors |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | oc_plugins_sdk_overview_imports | 10 | 11 | 11 | 2 | 8 | ✅ |
| 2 | oc_plugins_sdk_overview_registration_api | 10 | 12 | 11 | 2 | 8 | ✅ |
| 3 | oc_plugins_sdk_entrypoints | 10 | 11 | 11 | 2 | 8 | ✅ |
| 4 | oc_plugins_sdk_channel_plugins_concepts | 9 | 11 | 12 | 3 | 7 | ✅ |
| 5 | oc_plugins_sdk_channel_plugins_walkthrough | 9 | 12 | 11 | 3 | 7 | ✅ |
| 6 | oc_plugins_sdk_provider_plugins_walkthrough | 9 | 12 | 12 | 3 | 8 | ✅ |
| 7 | oc_plugins_sdk_provider_plugins_clawhub_catalog | 8 | 10 | 11 | 2 | 6 | ✅ |
| 8 | oc_plugins_sdk_runtime_config_utilities | 9 | 11 | 11 | 2 | 6 | ✅ |
| 9 | oc_plugins_sdk_runtime_namespaces | 10 | 12 | 12 | 3 | 7 | ✅ |
| 10 | oc_plugins_sdk_setup_packaging | 9 | 11 | 11 | 3 | 7 | ✅ |
| 11 | oc_plugins_sdk_setup_config_schema_wizards | 9 | 10 | 11 | 3 | 6 | ✅ |
| 12 | oc_plugins_sdk_migration | 9 | 11 | 12 | 3 | 7 | ✅ |
| 13 | oc_plugins_sdk_migration_import_paths | 9 | 10 | 11 | 2 | 7 | ✅ |


**Density re-confirmation (re-read).** Measured words match the Source table exactly: channel-plugins 4,025 · entrypoints 1,732 · migration 6,522 · overview 3,176 · provider-plugins 4,315 · runtime 3,027 · setup 2,632 (= 25,429 total). Code fences confirmed at 10 / 7 / 16 / 6 / 24 / 27 / 20 = 110 (indented accordion fences included). The 24/27/20-fence pages justify the provider/runtime/setup splits; no planned note approaches the ≤6-code / ≤2,500-word caps.

**New-term candidate.** `TypeBox` (TS runtime JSON-schema library; backs `defineToolPlugin` config/param inference + `buildJsonChannelConfigSchema`) — appears in `sdk-entrypoints` and `sdk-setup`. **Best-fit disposition: NOT a new `term_dictionary` capture.** Per the master ownership policy (OpenClaw vocabulary terms are digested as `oc_*` doc pages, not term_dictionary entries), TypeBox has a doc-page home: `concepts/typebox` is assigned to sub-plan **co07** → `oc_concepts_typebox.md`. pl24 renders `TypeBox` as plain inline code (not a link) until co07 lands; the two notes that reference it then cross-link `oc_concepts_typebox` at execution. Best-fit glossary if ever captured standalone: the agentic/LLM glossary. **Net new `term_dictionary` captures for pl24: 0.**

**Augmentation fix applied.** Corrected the H3 header count for `oc_plugins_sdk_entrypoints` from `10s` to `11s` (the Snippets group lists 11 items; the header undercounted by one). No content was added or removed — header now matches the listed items.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)


| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table per batch (G1–G6, G7/G8 discoverability) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present for the single execution phase; includes G5-ghost + G6-broken + G7/G8 inbound-link/in-degree; validation scripts present. |
| CP3 | Entry-point update specified (inherited; entry_openclaw_docs at master W1) | **PASS** | `## Entry Point Decision` contributes 13 rows to the master `entry_openclaw_docs.md` (CREATED at W1, `building_block: navigation`); no separate child entry point (correct — master is the single hub for 105 sub-plans). |
| CP4 | Plan size (≤30 or split) | **PASS** | 13 notes, single phase — well under 30. |
| CP5 | Note format derived (not invented) | **PASS** | Format inherited verbatim from master Format Definition, which is derived from existing `claude_code/cc_*` + `pi/pi_*` doc corpora (`## Overview` → body → `## Related Notes` → `## References` → bold footer; fixed YAML field order; forbidden-field list). |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment table shows all 13 notes ≤6 code / ~450–750 words; the 3 code-densest pages (24/27/20 fences) already split into 2 notes each per Split Decisions. No borderline note left unsplit. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-measured: 4,025 / 1,732 / 6,522 / 3,176 / 4,315 / 3,027 / 2,632 — exact match to Source table (ratio 1.00). Code fences 10/7/16/6/24/27/20 confirmed. |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements | **PASS** | `## Undigested Terms Plan` present (9-row disposition table, all OpenClaw vocab routed to `oc_*` doc notes or existing terms); `## Term-Note Authoring Requirements` present as N/A (0 new terms), with the inherited capture mandate stated. |
| CP8f | Slug/collision + all-notes dedup audit | **PASS** | 0 new `term_dictionary` slugs → no specificity/collision rename needed; `TypeBox` checked — absent from vault as a term, owned by co07 as a doc page (`concepts/typebox`), so not a dup. No planned `oc_*` doc note duplicates an existing term note (dedup-before-create inherited from master). |

**RESULT: 9/9 CP pass → READY FOR EXECUTION.** Status advanced `pending → ready`.
