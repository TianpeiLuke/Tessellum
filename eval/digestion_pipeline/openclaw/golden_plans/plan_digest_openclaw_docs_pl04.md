---
title: Sub-Plan pl04 — OpenClaw Docs: Plugins (manifest, memory plugins, presentation, oc-path, inventory, permissions)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["plugins/manifest", "plugins/memory-lancedb", "plugins/memory-wiki", "plugins/message-presentation", "plugins/oc-path", "plugins/plugin-inventory", "plugins/plugin-permission-requests"]
---

# Sub-Plan pl04: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, prefix `oc_`), format (YAML field order + body H2 structure +
> ≤400L/≤2500w/≤6-code caps), dedup (3-way across term_dictionary / documentation / `repo_openclaw*`),
> undigested-terms policy (OpenClaw vocab → `oc_` doc notes, link existing terms), 9-GATE validation,
> cross-refs, and entry-point (`entry_openclaw_docs.md`, W1) are ALL inherited from the master.

## Scope

The 7 mid-alphabet plugin-system pages: the native plugin **manifest** schema (`openclaw.plugin.json`), the
two bundled memory plugins (**memory-lancedb** vector store, **memory-wiki** compiled knowledge vault), the
shared **message-presentation** outbound-UI contract, the opt-in **oc-path** (`oc://` workspace addressing)
plugin, the generated **plugin-inventory** (core/external/source-only catalog), and **plugin-permission-requests**
(the `plugin.approval.*` runtime gate). Priority **P3** (Phase C — plugin reference sprawl), but the manifest and
permission pages are conceptually load-bearing (every plugin ships a manifest; approval is a security gate).
Code-side counterparts (`repo_openclaw_extensions`, `repo_openclaw_memory`, `repo_openclaw_security`) are LINKED,
not recreated.

**Source**: OpenClaw docs, 7 pages, **19,525 measured words**. **Planned: 11 notes** (manifest splits 5-way).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| manifest | plugins/manifest | 9,680 | 23 | 31 | 4 | model (schema/field reference) — SPLITS 5-way |
| memory-lancedb | plugins/memory-lancedb | 1,333 | 16 | 11 | 3 | procedure (install/config/embeddings) |
| memory-wiki | plugins/memory-wiki | 2,148 | 6 | 20 | 3 | concept (vault/claims/compile model) |
| message-presentation | plugins/message-presentation | 1,967 | 12 | 10 | 0 | model (render contract/types) |
| oc-path | plugins/oc-path | 1,026 | 4 | 7 | 0 | procedure (enable + `oc://` scheme) |
| plugin-inventory | plugins/plugin-inventory | 2,286 | 2 | 4 | 0 | model (generated catalog/reference) |
| plugin-permission-requests | plugins/plugin-permission-requests | 1,085 | 3 | 6 | 0 | procedure (request approval flow) |

(H2/H3 counts via `grep -nE '^#{2,3} '`; manifest has one stray `# …` shell-comment heading inside oc-path
is unrelated. manifest H3 = 4 nested `setup`/`channelConfigs` subsections + `package.json`/`OpenClaw Provider Index`.)

## Content Strategy

- **Prioritize**: the manifest **top-level field reference** (the contract every plugin ships) and the
  **permission-request** approval flow (a security gate analogous to `repo_openclaw_security`). These are the
  most-referenced pages by the rest of the plugin corpus.
- **Split**: `manifest.md` (9,680w / 23 code / 31 H2) far exceeds the 2,500w + single-BB caps and mixes an
  overview procedure with many independent declarative reference clusters → 5 notes grouped by metadata domain
  (overview+top-level fields · provider/model metadata · generation/media/tool metadata · channel/UI/contracts ·
  discovery/validation/package.json). Each stays ≤2,500w and ≤6 code blocks.
- **Keep 1 note each**: memory-lancedb (1,333w), memory-wiki (2,148w, under cap, single concept BB), 
  message-presentation (1,967w), oc-path (1,026w), plugin-inventory (2,286w, single reference-catalog BB),
  plugin-permission-requests (1,085w).
- **Link-out, do not redefine**: vector-store / embedding / RAG / knowledge-graph concepts → link
  `term_vector_database` / `term_embedding` / `term_rag` / `term_knowledge_graph`; the plugin SDK / capability
  model → link `term_plugin_sdk` / `term_plugin_manifest` / `term_capability_negotiation` and `repo_openclaw_extensions`;
  exec/sandbox approvals beyond plugin scope → link `term_sandbox` + (planned) gateway sub-plan notes.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page / section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_manifest_overview.md` | concept | manifest.md: intro, What this file does, Minimal example, Rich example, Top-level field reference | 700 | The `openclaw.plugin.json` native manifest: what it does (cheap pre-load metadata, validate config without executing code), minimal/rich examples, and the full top-level field table. |
| 2 | `oc_plugins_manifest_provider_model_metadata.md` | model | manifest.md: providerAuthChoices, modelSupport, modelCatalog, modelIdNormalization, providerEndpoints, providerRequest, secretProviderIntegrations, modelPricing (+ OpenClaw Provider Index) | 700 | Manifest provider/model metadata blocks read before provider runtime loads: auth choices, model support/catalog/id-normalization, provider endpoints/request policy, secret-provider presets, and model pricing. |
| 3 | `oc_plugins_manifest_generation_tool_metadata.md` | model | manifest.md: Generation provider metadata reference, Tool metadata reference, mediaUnderstandingProviderMetadata, contracts reference | 600 | Manifest generation/media/tool metadata: static auth signals for image/video/music/media-understanding providers, plugin-owned tool availability metadata, and the `contracts` capability-ownership snapshot. |
| 4 | `oc_plugins_manifest_channel_ui_setup.md` | model | manifest.md: commandAliases, activation, qaRunners, setup (+ setup.providers / setup fields), uiHints, channelConfigs (+ Replacing another channel plugin) | 650 | Manifest control-plane metadata: command aliases, activation planner hints, QA runners, setup/onboarding descriptors, UI hints, and channel-config (including channel-plugin replacement). |
| 5 | `oc_plugins_manifest_discovery_validation.md` | procedure | manifest.md: Manifest versus package.json (+ package.json fields that affect discovery), Discovery precedence (duplicate plugin ids), JSON Schema requirements, Validation behavior, Notes | 600 | How OpenClaw discovers and validates manifests: manifest-vs-package.json split, discovery precedence for duplicate ids, JSON Schema requirements, and validation behavior/error handling. |
| 6 | `oc_plugins_memory_lancedb.md` | procedure | memory-lancedb.md: Installation, Quick start, Provider-backed/Ollama/OpenAI-compatible embeddings, Recall and capture limits, Commands, Storage, Runtime dependencies, Troubleshooting | 650 | The bundled `memory-lancedb` vector-store memory plugin: install, configure embedding providers (provider-backed / Ollama / OpenAI-compatible), recall/capture limits, commands, on-disk storage, and troubleshooting. |
| 7 | `oc_plugins_memory_wiki.md` | concept | memory-wiki.md: What it adds, How it fits with memory, Hybrid pattern, Vault modes, Vault layout, OKF imports, Claims/evidence, Entity metadata, Compile pipeline, Dashboards, Search, Agent tools, Prompt behavior, Configuration, CLI, Obsidian, Workflow | 700 | The bundled `memory-wiki` compiled-knowledge-vault plugin: vault modes (isolated/bridge/unsafe-local), structured claims + provenance, the compile pipeline, dashboards, `wiki_search`/`wiki_get` tools, Obsidian support, and the recommended hybrid memory pattern. |
| 8 | `oc_plugins_message_presentation.md` | model | message-presentation.md: Contract, Producer examples, Renderer contract, Core render flow, Degradation rules, Provider mapping, Presentation vs InteractiveReply, Delivery pin, Plugin author checklist | 650 | OpenClaw's shared rich-outbound-UI contract: the presentation block types (sections/buttons/selects/cards), producer + renderer contracts, core render flow, degradation rules, per-provider mapping, and the delivery-pin/author checklist. |
| 9 | `oc_plugins_oc_path.md` | procedure | oc-path.md: Why enable it, Where it runs, Enable, Dependencies, What it provides, Relationship to other plugins, Safety | 500 | The opt-in `oc-path` plugin and the `oc://` workspace-file addressing scheme: why/where it runs, how to enable it, dependencies, the four supported file kinds, relationship to other plugins, and safety guarantees. |
| 10 | `oc_plugins_plugin_inventory.md` | model | plugin-inventory.md: Definitions, Install a plugin, Core npm package, Official external packages, Source checkout only | 600 | The generated OpenClaw plugin inventory: definitions of core-npm vs official-external vs source-only distribution, how to install a plugin, and the canonical three-tier plugin catalog. |
| 11 | `oc_plugins_plugin_permission_requests.md` | procedure | plugin-permission-requests.md: Choose the right gate, Request approval before a tool call, Decision behavior, Route approval prompts, Codex native permissions, Troubleshooting | 600 | Plugin permission requests via the Gateway `plugin.approval.*` flow: choosing the right gate (optional tools vs plugin approvals vs exec approvals vs Codex/MCP), requesting approval before a tool call, decision behavior, prompt routing, and troubleshooting. |

## Section Coverage Map

```
manifest.md (9,680w, 31 H2)
├── (intro) native manifest vs compatible bundles ──────────── → note 1 (manifest_overview)
├── What this file does ────────────────────────────────────── → note 1
├── Minimal example / Rich example ─────────────────────────── → note 1
├── Top-level field reference ──────────────────────────────── → note 1
├── providerAuthChoices reference ──────────────────────────── → note 2 (provider_model_metadata)
├── modelSupport reference ─────────────────────────────────── → note 2
├── modelCatalog reference ─────────────────────────────────── → note 2
├── modelIdNormalization reference ─────────────────────────── → note 2
├── providerEndpoints reference ────────────────────────────── → note 2
├── providerRequest reference ──────────────────────────────── → note 2
├── secretProviderIntegrations reference ───────────────────── → note 2
├── modelPricing reference (+ OpenClaw Provider Index H3) ───── → note 2
├── Generation provider metadata reference ─────────────────── → note 3 (generation_tool_metadata)
├── Tool metadata reference ────────────────────────────────── → note 3
├── mediaUnderstandingProviderMetadata reference ───────────── → note 3
├── contracts reference ────────────────────────────────────── → note 3
├── commandAliases reference ───────────────────────────────── → note 4 (channel_ui_setup)
├── activation reference ───────────────────────────────────── → note 4
├── qaRunners reference ────────────────────────────────────── → note 4
├── setup reference (+ setup.providers H3, setup fields H3) ── → note 4
├── uiHints reference ──────────────────────────────────────── → note 4
├── channelConfigs reference (+ Replacing another channel H3) → note 4
├── Manifest versus package.json (+ package.json fields H3) ── → note 5 (discovery_validation)
├── Discovery precedence (duplicate plugin ids) ────────────── → note 5
├── JSON Schema requirements ───────────────────────────────── → note 5
├── Validation behavior ────────────────────────────────────── → note 5
├── Notes ──────────────────────────────────────────────────── → note 5
└── Related (source link list) ─────────────────────────────── → note 1 ## Related Notes (links, not body)
memory-lancedb.md (1,333w, 11 H2)
├── Installation / Quick start ─────────────────────────────── → note 6 (memory_lancedb)
├── Provider-backed / Ollama / OpenAI-compatible embeddings ── → note 6
├── Recall and capture limits / Commands / Storage ─────────── → note 6
├── Runtime dependencies / Troubleshooting (3 H3) ──────────── → note 6
└── Related ────────────────────────────────────────────────── → note 6 ## Related Notes
memory-wiki.md (2,148w, 20 H2)
├── What it adds / How it fits with memory / Hybrid pattern ── → note 7 (memory_wiki)
├── Vault modes (isolated/bridge/unsafe-local H3) / layout ─── → note 7
├── OKF imports / Claims+evidence / Entity metadata ────────── → note 7
├── Compile pipeline / Dashboards / Search / Agent tools ───── → note 7
├── Prompt behavior / Configuration (+ QMD+bridge H3) / CLI ── → note 7
├── Obsidian support / Recommended workflow ────────────────── → note 7
└── Related docs ───────────────────────────────────────────── → note 7 ## Related Notes
message-presentation.md (1,967w, 10 H2)
├── Contract / Producer examples / Renderer contract ───────── → note 8 (message_presentation)
├── Core render flow / Degradation rules / Provider mapping ── → note 8
├── Presentation vs InteractiveReply / Delivery pin ────────── → note 8
├── Plugin author checklist ────────────────────────────────── → note 8
└── Related docs ───────────────────────────────────────────── → note 8 ## Related Notes
oc-path.md (1,026w, 7 H2)
├── Why enable it (+ 3 shell-comment example headings) ─────── → note 9 (oc_path)
├── Where it runs / Enable / Dependencies ──────────────────── → note 9
├── What it provides / Relationship to other plugins / Safety → note 9
└── Related ────────────────────────────────────────────────── → note 9 ## Related Notes
plugin-inventory.md (2,286w, 4 H2)
├── Definitions / Install a plugin ─────────────────────────── → note 10 (plugin_inventory)
├── Core npm package (72 plugins) ──────────────────────────── → note 10
├── Official external packages ─────────────────────────────── → note 10
└── Source checkout only ───────────────────────────────────── → note 10
plugin-permission-requests.md (1,085w, 6 H2)
├── Choose the right gate ──────────────────────────────────── → note 11 (permission_requests)
├── Request approval before a tool call / Decision behavior ── → note 11
├── Route approval prompts / Codex native permissions ──────── → note 11
├── Troubleshooting ────────────────────────────────────────── → note 11
└── Related ────────────────────────────────────────────────── → note 11 ## Related Notes
```
No orphaned sections. Every source H2/H3 maps to exactly one planned note. (The "## Related" / "## Related docs"
H2 in each source page is a link list, not body content — it feeds the new note's `## Related Notes` section, not
a separate note.)

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| manifest.md (9,680w, 23 code, 31 H2 / 4 H3, mixed BB) | notes 1–5 | ~3.9× the 2,500w cap and far over the 6-code cap; mixes an overview procedure/concept with 25+ independent declarative reference clusters. Split by metadata domain: (1) overview + top-level field table; (2) provider/model metadata; (3) generation/media/tool/contracts metadata; (4) channel/UI/activation/setup/QA metadata; (5) discovery + validation + package.json. Each resulting note ≤700w, ≤6 code, single BB. |
| memory-wiki.md (2,148w, 20 H2) | note 7 (no split) | Under the 2,500w cap; the 20 H2s are all facets of one coherent concept (the compiled-vault model). Code-light (6 fences). Kept atomic as one concept note. |
| plugin-inventory.md (2,286w, 4 H2) | note 10 (no split) | Under 2,500w; the bulk is a flat generated catalog (one reference-model BB). The three tiers are one taxonomy, not separable task clusters. Kept as one note. |
| memory-lancedb / message-presentation / oc-path / plugin-permission-requests | notes 6 / 8 / 9 / 11 (no split) | Each ≤2,148w and single-BB. No split. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (19,525 measured words). New `oc_` notes: **11**. New `term_dictionary` notes: **0**.
- BB distribution: **model ×5** (notes 2, 3, 4, 8, 10 — declarative metadata/contract/catalog tables) ·
  **concept ×2** (notes 1, 7) · **procedure ×4** (notes 5, 6, 9, 11). One building_block per note (note 4 =
  model: manifest channel/UI/activation/setup are declarative metadata, not a step-by-step task).
- Est. digest words ~6,950 (avg ~630/note); within the master's "≤2,500w/note" cap with wide margin.
- Source code fences (66 total) distribute across the 11 notes; manifest's 23 fences split so each manifest
  note reproduces ≤6 representative JSON snippets verbatim (omitting redundant field-by-field examples).
- **Cross-refs (LOCKED at xref-augment 2026-06-21):** every note's `## Per-Note Related Notes Mapping`
  carries **≥8 `term_dictionary` terms · ≥10 code_snippets · ≥10 docs** (≥5 of the 10 docs EXISTING
  are the 11 this-series `oc_*` siblings + `entry_openclaw_docs.md` (master W1). Per-note counts: 10–12 terms,
  11–12 snippets, 10–11 docs each.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> paths are FROM a note at `resources/documentation/openclaw/oc_X.md`: term `../../term_dictionary/…`,
> snippet `../../code_snippets/…`, sibling `oc_*` (this series, planned) `oc_Y.md`, other doc `../<folder>/…`,
> repo `../../../areas/code_repos/…`, entry `../../../0_entry_points/…`. Sibling `oc_*` and `entry_openclaw_docs.md`
> are **(planned, this series / master W1)** and count toward the 10-doc floor; ≥5 of the 10 docs per note are

### oc_plugins_manifest_overview (11t · 11s · 11d)

**Terms** — [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — the `openclaw.plugin.json` metadata contract; relevance: this note IS the top-level manifest overview. · [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — the public plugin SDK; relevance: the manifest is the SDK's pre-load declaration surface. · [term_json_schema](../../term_dictionary/term_json_schema.md) — JSON Schema validation; relevance: `configSchema` validates config without executing code. · [term_capability_negotiation](../../term_dictionary/term_capability_negotiation.md) — capability declaration/handshake; relevance: the manifest declares static capability ownership (`contracts`). · [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider-type plugin; relevance: the rich example manifest is a provider (`openrouter`). · [term_configuration_model](../../term_dictionary/term_configuration_model.md) — config field model; relevance: top-level field reference is the manifest's config model. · [term_openclaw](../../term_dictionary/term_openclaw.md) — the OpenClaw gateway; relevance: native vs compatible-bundle manifests are OpenClaw-host concepts. · [term_skill_manifest](../../term_dictionary/term_skill_manifest.md) — skill declaration manifest; relevance: manifest declares skill roots alongside plugin metadata. · [term_acp_agent_client_protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — agent-client protocol; relevance: compatible Codex/Claude/Cursor bundle manifests are ACP-adjacent harness layouts. · [term_function_calling](../../term_dictionary/term_function_calling.md) — model tool/function invocation; relevance: manifest declares plugin-owned tool availability. · [term_npm](../../term_dictionary/term_npm.md) — npm packaging; relevance: manifest is distinguished from `package.json`/npm install metadata.

**Docs** — [cc_plugin_manifest_schema](../claude_code/cc_plugin_manifest_schema.md) — Claude Code's `plugin.json` schema; relevance: direct cross-tool analogue of the OpenClaw manifest. · [cc_plugins_overview](../claude_code/cc_plugins_overview.md) — Claude Code plugin model overview; relevance: same "manifest + components" mental model. · [cc_sdk_plugin_structure](../claude_code/cc_sdk_plugin_structure.md) — Claude SDK plugin layout; relevance: plugin-root file layout parallel. · [hermes_build_plugin_tutorial](../hermes_agent/hermes_build_plugin_tutorial.md) — Hermes plugin authoring walkthrough; relevance: end-to-end manifest authoring sibling. · [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — Hermes plugin system; relevance: manifest-driven discovery/validation in a sibling harness. · [hermes_plugin_types_surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin type/surface taxonomy; relevance: the manifest declares which surfaces a plugin owns. · [pi/pi_extensions_overview](../pi/pi_extensions_overview.md) — Pi extension model; relevance: third coding-agent extension-manifest analogue. · [oc_plugins_manifest_provider_model_metadata](oc_plugins_manifest_provider_model_metadata.md) — provider/model manifest blocks (planned, this series); relevance: detail of the fields this overview introduces. · [oc_plugins_manifest_discovery_validation](oc_plugins_manifest_discovery_validation.md) — manifest discovery/validation (planned, this series); relevance: how the host reads this manifest. · [oc_plugins_plugin_inventory](oc_plugins_plugin_inventory.md) — plugin inventory/distribution (planned, this series); relevance: every inventoried plugin ships this manifest. · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link / anti-island.

**Repos** — [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin/extension framework repo; relevance: implements the manifest loader. · [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the OpenClaw monorepo; relevance: host that reads `openclaw.plugin.json`. · [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: manifest declares skill roots.


### oc_plugins_manifest_provider_model_metadata (11t · 11s · 11d)

**Terms** — [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider-type plugin; relevance: these blocks describe a provider plugin's metadata. · [term_model_catalog](../../term_dictionary/term_model_catalog.md) — model catalog; relevance: `modelCatalog`/`modelSupport` are the manifest's catalog declarations. · [term_provider_routing](../../term_dictionary/term_provider_routing.md) — provider routing; relevance: `providerEndpoints`/`providerRequest` shape routing. · [term_fallback_provider](../../term_dictionary/term_fallback_provider.md) — fallback provider; relevance: provider/model metadata feeds failover ladders. · [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: this metadata is about LLM provider plugins. · [term_authentication](../../term_dictionary/term_authentication.md) — auth; relevance: `providerAuthChoices`/`secretProviderIntegrations`. · [term_oauth](../../term_dictionary/term_oauth.md) — OAuth flow; relevance: provider auth choices include OAuth methods. · [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — manifest contract; relevance: these are manifest field blocks. · [term_bedrock](../../term_dictionary/term_bedrock.md) — Amazon Bedrock; relevance: bedrock-class providers use provider endpoint/request metadata. · [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth token; relevance: secret-provider presets store provider OAuth tokens. · [term_configuration_model](../../term_dictionary/term_configuration_model.md) — config model; relevance: `modelPricing`/`modelIdNormalization` are config-time declarations.

**Docs** — [hermes_provider_routing](../hermes_agent/hermes_provider_routing.md) — Hermes provider routing; relevance: routing analogue of `providerRequest`. · [hermes_provider_routing_proxies](../hermes_agent/hermes_provider_routing_proxies.md) — routing via proxies; relevance: `providerEndpoints` host-suffix routing parallel. · [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: catalog of provider plugins this metadata describes. · [hermes_provider_aws_bedrock](../hermes_agent/hermes_provider_aws_bedrock.md) — Bedrock provider; relevance: concrete provider-metadata example. · [cc_llm_gateway](../claude_code/cc_llm_gateway.md) — Claude Code LLM gateway; relevance: model-catalog/provider-endpoint cross-tool parallel. · [cc_llm_gateway_litellm](../claude_code/cc_llm_gateway_litellm.md) — LiteLLM gateway; relevance: provider id normalization/routing analogue. · [pi/pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — Pi custom provider registration; relevance: declaring a provider's model support cross-tool. · [pi/pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi cloud providers; relevance: provider catalog analogue. · [oc_plugins_manifest_overview](oc_plugins_manifest_overview.md) — manifest overview (planned, this series); relevance: parent overview of these blocks. · [oc_plugins_manifest_generation_tool_metadata](oc_plugins_manifest_generation_tool_metadata.md) — generation/tool metadata (planned, this series); relevance: sibling manifest-metadata cluster. · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link.

**Repos** — [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM provider plugins repo; relevance: implements the provider plugins this metadata declares. · [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: hosts provider plugin metadata loading. · [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: provider runtime that reads this metadata.

**Snippets** — [snippet_openclaw_provider_openrouter_aggregator](../../code_snippets/snippet_openclaw_provider_openrouter_aggregator.md) — OpenRouter aggregator provider; relevance: the page's rich example is `openrouter`. · [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — Anthropic provider; relevance: provider plugin with auth-choice/model metadata. · [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenAI provider; relevance: model-catalog/endpoint declaration example. · [snippet_openclaw_provider_ollama_local](../../code_snippets/snippet_openclaw_provider_ollama_local.md) — local Ollama provider; relevance: provider-endpoint/base-url metadata. · [snippet_openclaw_agents_model_catalog](../../code_snippets/snippet_openclaw_agents_model_catalog.md) — runtime model catalog; relevance: consumes manifest `modelCatalog`/`modelSupport`. · [snippet_openclaw_gateway_model_pricing_alias_lookup](../../code_snippets/snippet_openclaw_gateway_model_pricing_alias_lookup.md) — model pricing/alias lookup; relevance: consumes `modelPricing`/`modelIdNormalization`. · [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — provider fallback context; relevance: provider metadata feeds fallback. · [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — Hermes provider registry; relevance: provider-metadata registry parallel. · [snippet_hermes_agent_cli_auth_resolve_provider](../../code_snippets/snippet_hermes_agent_cli_auth_resolve_provider.md) — provider auth resolution; relevance: `providerAuthChoices` resolution analogue. · [snippet_hermes_agent_cli_providers_registry](../../code_snippets/snippet_hermes_agent_cli_providers_registry.md) — providers registry; relevance: model-support declaration parallel. · [snippet_hermes_agent_providers_base_abc](../../code_snippets/snippet_hermes_agent_providers_base_abc.md) — provider base contract; relevance: the shape provider metadata feeds.

### oc_plugins_manifest_generation_tool_metadata (10t · 11s · 11d)

**Terms** — [term_tool_descriptor](../../term_dictionary/term_tool_descriptor.md) — tool descriptor; relevance: `Tool metadata reference` declares plugin-owned tool availability. · [term_tool_registry](../../term_dictionary/term_tool_registry.md) — tool registry; relevance: tool metadata feeds the registry. · [term_capability_negotiation](../../term_dictionary/term_capability_negotiation.md) — capability ownership; relevance: `contracts` is a static capability-ownership snapshot. · [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin; relevance: generation/media-understanding provider metadata. · [term_function_calling](../../term_dictionary/term_function_calling.md) — function/tool calling; relevance: tool metadata governs what the model can call. · [term_authentication](../../term_dictionary/term_authentication.md) — auth; relevance: static auth signals for image/video/music providers. · [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — manifest contract; relevance: these are manifest blocks. · [term_multimodal](../../term_dictionary/term_multimodal.md) — multimodal I/O; relevance: generation/media-understanding metadata is multimodal. · [term_text_to_speech](../../term_dictionary/term_text_to_speech.md) — TTS; relevance: music/speech generation provider metadata. · [term_speech_to_text](../../term_dictionary/term_speech_to_text.md) — STT; relevance: media-understanding provider metadata covers audio.

**Docs** — [hermes_image_gen_provider_plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-gen provider plugin; relevance: concrete generation-provider metadata analogue. · [hermes_video_gen_provider_plugin](../hermes_agent/hermes_video_gen_provider_plugin.md) — video-gen provider plugin; relevance: video-generation provider-metadata example paralleling the image-gen block this note documents. · [hermes_tools_reference_core](../hermes_agent/hermes_tools_reference_core.md) — core tools reference; relevance: tool-availability declaration parallel. · [hermes_web_search_provider_plugin](../hermes_agent/hermes_web_search_provider_plugin.md) — web-search provider plugin; relevance: provider-tool metadata example. · [hermes_adding_built_in_tool](../hermes_agent/hermes_adding_built_in_tool.md) — adding a built-in tool; relevance: how plugin-owned tools are declared/registered. · [cc_plugin_components](../claude_code/cc_plugin_components.md) — Claude Code plugin components; relevance: tool/skill component declaration parallel. · [pi/pi_extensions_api_methods](../pi/pi_extensions_api_methods.md) — Pi extension API methods; relevance: extension-declared tool surface analogue. · [pi/pi_sdk_options](../pi/pi_sdk_options.md) — Pi SDK options; relevance: declarative capability options parallel. · [oc_plugins_manifest_provider_model_metadata](oc_plugins_manifest_provider_model_metadata.md) — provider/model metadata (planned, this series); relevance: sibling manifest cluster. · [oc_plugins_manifest_overview](oc_plugins_manifest_overview.md) — manifest overview (planned, this series); relevance: parent overview. · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link.

**Repos** — [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: hosts tool/generation provider plugins. · [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — voice/speech extensions; relevance: implements media/speech generation providers. · [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: runtime consuming tool/contract metadata.

**Snippets** — [snippet_hermes_agent_model_tools_introspection](../../code_snippets/snippet_hermes_agent_model_tools_introspection.md) — tool introspection; relevance: tool-availability metadata analogue. · [snippet_hermes_agent_toolsets_definitions](../../code_snippets/snippet_hermes_agent_toolsets_definitions.md) — toolset definitions; relevance: declarative tool metadata parallel. · [snippet_hermes_agent_acp_tools_register](../../code_snippets/snippet_hermes_agent_acp_tools_register.md) — tool registration; relevance: how declared tools enter the registry. · [snippet_hermes_agent_cli_tools_config](../../code_snippets/snippet_hermes_agent_cli_tools_config.md) — tool config; relevance: tool availability configuration. · [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image generation tool; relevance: generation-provider metadata example. · [snippet_hermes_agent_tools_video_gen](../../code_snippets/snippet_hermes_agent_tools_video_gen.md) — video generation tool; relevance: generation-provider metadata example. · [snippet_hermes_agent_plugins_image_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_image_gen_dispatch.md) — image-gen dispatch; relevance: generation provider routed from metadata. · [snippet_hermes_agent_plugins_video_gen_dispatch](../../code_snippets/snippet_hermes_agent_plugins_video_gen_dispatch.md) — video-gen dispatch; relevance: generation provider metadata in action. · [snippet_hermes_agent_tools_vision_dispatch](../../code_snippets/snippet_hermes_agent_tools_vision_dispatch.md) — vision dispatch; relevance: media-understanding provider metadata. · [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — Deepgram STT; relevance: media-understanding/speech provider example. · [snippet_openclaw_voice_call_media_stream_audio](../../code_snippets/snippet_openclaw_voice_call_media_stream_audio.md) — media stream audio; relevance: media generation/understanding provider surface.

### oc_plugins_manifest_channel_ui_setup (10t · 11s · 11d)

**Terms** — [term_channel_adapter](../../term_dictionary/term_channel_adapter.md) — channel adapter; relevance: `channelConfigs`/channel-plugin replacement is channel-adapter metadata. · [term_configuration_model](../../term_dictionary/term_configuration_model.md) — config model; relevance: `setup`/`uiHints`/`commandAliases` are config-time descriptors. · [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — manifest contract; relevance: these are manifest control-plane blocks. · [term_capability_negotiation](../../term_dictionary/term_capability_negotiation.md) — capability declaration; relevance: `activation` declares control-plane surface ownership. · [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin; relevance: `setup.providers` onboarding descriptors. · [term_skill_manifest](../../term_dictionary/term_skill_manifest.md) — skill manifest; relevance: `commandAliases` overlap native command/skill defaults. · [term_tool_registry](../../term_dictionary/term_tool_registry.md) — tool registry; relevance: `qaRunners` register QA-host inspectable surfaces. · [term_command_pattern](../../term_dictionary/term_command_pattern.md) — command pattern; relevance: `commandAliases` map names to CLI/native commands. · [term_authentication](../../term_dictionary/term_authentication.md) — auth; relevance: `setup` onboarding declares provider env vars / auth choices. · [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw host; relevance: activation planner/QA host are OpenClaw control-plane surfaces.

**Docs** — [hermes_adding_platform_adapter_plugin](../hermes_agent/hermes_adding_platform_adapter_plugin.md) — adding a channel adapter; relevance: `channelConfigs`/replacement metadata analogue. · [cc_channels_setup](../claude_code/cc_channels_setup.md) — Claude Code channel setup; relevance: channel onboarding/setup parallel. · [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Slack messaging setup; relevance: concrete channel-config example. · [hermes_gateway_feishu_setup](../hermes_agent/hermes_gateway_feishu_setup.md) — Feishu setup; relevance: channel onboarding descriptors. · [hermes_telegram_setup](../hermes_agent/hermes_telegram_setup.md) — Telegram setup; relevance: channel-config/setup metadata example. · [hermes_gateway_operations](../hermes_agent/hermes_gateway_operations.md) — gateway operations; relevance: activation/restart picks up manifest snapshot. · [pi/pi_sdk_options](../pi/pi_sdk_options.md) — Pi SDK options; relevance: declarative UI/setup options parallel. · [cc_statusline_setup](../claude_code/cc_statusline_setup.md) — statusline/UI setup; relevance: `uiHints` config-UI analogue. · [oc_plugins_manifest_overview](oc_plugins_manifest_overview.md) — manifest overview (planned, this series); relevance: parent overview. · [oc_plugins_manifest_discovery_validation](oc_plugins_manifest_discovery_validation.md) — discovery/validation (planned, this series); relevance: how channel/setup metadata is validated. · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link.

**Repos** — [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels framework; relevance: consumes `channelConfigs` metadata. · [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: channel-plugin replacement targets these. · [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: hosts activation/setup metadata loading.

**Snippets** — [snippet_openclaw_wizard_setup_config](../../code_snippets/snippet_openclaw_wizard_setup_config.md) — wizard setup config; relevance: `setup`/`setup.providers` onboarding descriptors. · [snippet_openclaw_wizard_clack_prompter](../../code_snippets/snippet_openclaw_wizard_clack_prompter.md) — onboarding prompter; relevance: `uiHints`/setup drive onboarding prompts. · [snippet_openclaw_channels_adapter_contract](../../code_snippets/snippet_openclaw_channels_adapter_contract.md) — channel adapter contract; relevance: `channelConfigs` feeds the adapter contract. · [snippet_openclaw_gateway_channels_restart_startup](../../code_snippets/snippet_openclaw_gateway_channels_restart_startup.md) — channel restart/startup; relevance: activation/restart picks up channel metadata. · [snippet_hermes_agent_cli_config_schema](../../code_snippets/snippet_hermes_agent_cli_config_schema.md) — CLI config schema; relevance: config-time validation of setup/UI metadata. · [snippet_hermes_agent_cli_profiles_schema](../../code_snippets/snippet_hermes_agent_cli_profiles_schema.md) — profiles schema; relevance: setup-provider profile metadata parallel. · [snippet_hermes_agent_gw_platform_slack](../../code_snippets/snippet_hermes_agent_gw_platform_slack.md) — Slack platform; relevance: channel-config example. · [snippet_hermes_agent_gw_platform_discord_normalize](../../code_snippets/snippet_hermes_agent_gw_platform_discord_normalize.md) — Discord normalize; relevance: channel-plugin behavior gated by channel metadata. · [snippet_hermes_agent_cli_kanban_commands](../../code_snippets/snippet_hermes_agent_cli_kanban_commands.md) — CLI command wiring; relevance: `commandAliases` registration analogue. · [snippet_hermes_agent_cli_main_entry_point](../../code_snippets/snippet_hermes_agent_cli_main_entry_point.md) — CLI entry/command routing; relevance: command-alias resolution parallel. · [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — plugin lifecycle; relevance: activation hooks fire during plugin load.

### oc_plugins_manifest_discovery_validation (10t · 11s · 11d)

**Terms** — [term_json_schema](../../term_dictionary/term_json_schema.md) — JSON Schema; relevance: every plugin must ship a JSON Schema validated at config read/write. · [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — manifest contract; relevance: manifest-vs-`package.json` split is the note's core. · [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin SDK; relevance: `openclaw.compat.pluginApi` floor and entrypoints are SDK contracts. · [term_configuration_model](../../term_dictionary/term_configuration_model.md) — config model; relevance: strict schema rejects unknown config keys. · [term_capability_negotiation](../../term_dictionary/term_capability_negotiation.md) — capability/kind selection; relevance: exclusive plugin kinds via `plugins.slots.*`. · [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin; relevance: discovery precedence governs duplicate provider ids. · [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw host; relevance: discovery roots and host-version floor are host concepts. · [term_npm](../../term_dictionary/term_npm.md) — npm packaging; relevance: `package.json#openclaw.install` npm/integrity metadata (semver floors `minHostVersion`/`compat.pluginApi`). · [term_skill_manifest](../../term_dictionary/term_skill_manifest.md) — skill manifest; relevance: skill-root declarations are discovered/validated alongside the plugin manifest. · [term_command_pattern](../../term_dictionary/term_command_pattern.md) — command pattern; relevance: discovery/Doctor diagnostics surface duplicate-id overrides.

**Docs** — [cc_plugin_dependencies](../claude_code/cc_plugin_dependencies.md) — Claude Code plugin dependency resolution; relevance: discovery/precedence + dependency parallel. · [cc_plugin_caching_and_troubleshooting](../claude_code/cc_plugin_caching_and_troubleshooting.md) — plugin caching/troubleshooting; relevance: discovery/validation failure diagnostics analogue. · [cc_marketplace_json_schema](../claude_code/cc_marketplace_json_schema.md) — marketplace JSON schema; relevance: schema-validation-of-manifest parallel. · [cc_plugin_user_config_and_env](../claude_code/cc_plugin_user_config_and_env.md) — plugin user config/env; relevance: strict config-key validation analogue. · [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — Hermes plugin system; relevance: discovery + validation in a sibling harness. · [hermes_plugin_extensions_hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — Hermes plugin hooks; relevance: entrypoint/extension declaration parallel. · [pi/pi_packages](../pi/pi_packages.md) — Pi package/distribution; relevance: package-vs-manifest split analogue. · [oc_plugins_manifest_overview](oc_plugins_manifest_overview.md) — manifest overview (planned, this series); relevance: parent overview. · [oc_plugins_plugin_inventory](oc_plugins_plugin_inventory.md) — plugin inventory (planned, this series); relevance: discovery feeds the inventory + install hints. · [oc_plugins_manifest_channel_ui_setup](oc_plugins_manifest_channel_ui_setup.md) — channel/UI setup (planned, this series); relevance: `package.json#openclaw.channel` discovery fields. · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link.

**Repos** — [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: implements manifest discovery + schema validation. · [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: Doctor/startup discovery diagnostics live here. · [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — skills subsystem; relevance: skill-root discovery parallels plugin discovery.


### oc_plugins_memory_lancedb (12t · 12s · 11d)

**Terms** — [term_vector_database](../../term_dictionary/term_vector_database.md) — vector DB; relevance: LanceDB is the plugin's vector store. · [term_embedding](../../term_dictionary/term_embedding.md) — embeddings; relevance: recall uses configurable embedding providers. · [term_dense_retrieval](../../term_dictionary/term_dense_retrieval.md) — dense retrieval; relevance: vector recall is dense retrieval. · [term_rag](../../term_dictionary/term_rag.md) — retrieval-augmented generation; relevance: auto-recall injects memory pre-turn. · [term_recall](../../term_dictionary/term_recall.md) — recall; relevance: `recallMaxChars`/`memory_recall` govern recall. · [term_information_retrieval](../../term_dictionary/term_information_retrieval.md) — IR; relevance: `ltm search`/query are IR over the table. · [term_storage_engine](../../term_dictionary/term_storage_engine.md) — storage engine; relevance: `dbPath`/`storageOptions` (incl. S3) configure storage. · [term_columnar_storage](../../term_dictionary/term_columnar_storage.md) — columnar storage; relevance: LanceDB is a columnar vector store. · [term_matryoshka_embeddings](../../term_dictionary/term_matryoshka_embeddings.md) — Matryoshka embeddings; relevance: `dimensions` truncation for non-standard models. · [term_agentic_memory](../../term_dictionary/term_agentic_memory.md) — agentic memory; relevance: auto-capture/recall is agent long-term memory. · [term_qmd](../../term_dictionary/term_qmd.md) — QMD memory backend; relevance: contrasted/companion active-memory backend (one owns the slot). · [term_failover](../../term_dictionary/term_failover.md) — failover; relevance: missing-dependency/unsupported-platform fallback to the default memory backend.

**Docs** — [hermes_memory_provider_plugin](../hermes_agent/hermes_memory_provider_plugin.md) — Hermes memory provider plugin; relevance: direct analogue of a pluggable vector-memory backend. · [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory provider catalog; relevance: catalog of memory backends incl. vector stores. · [cc_memory_overview](../claude_code/cc_memory_overview.md) — Claude Code memory overview; relevance: agent long-term memory model parallel. · [cc_auto_memory](../claude_code/cc_auto_memory.md) — auto memory; relevance: auto-recall/auto-capture analogue. · [band/band_agent_api_memories](../band/band_agent_api_memories.md) — Band agent memory API; relevance: memory store/recall API parallel. · [hermes_inference_providers_cloud](../hermes_agent/hermes_inference_providers_cloud.md) — cloud inference providers; relevance: embedding providers (OpenAI/Ollama/Copilot) overlap. · [pi/pi_cloud_providers](../pi/pi_cloud_providers.md) — Pi cloud providers; relevance: OpenAI-compatible embedding endpoint config parallel. · [oc_plugins_memory_wiki](oc_plugins_memory_wiki.md) — memory-wiki plugin (planned, this series); relevance: companion memory plugin in the recommended hybrid pattern. · [oc_plugins_manifest_provider_model_metadata](oc_plugins_manifest_provider_model_metadata.md) — provider/model metadata (planned, this series); relevance: embedding provider adapters declared via manifest. · [oc_plugins_plugin_inventory](oc_plugins_plugin_inventory.md) — plugin inventory (planned, this series); relevance: memory-lancedb is an official external package. · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link.

**Repos** — [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: implements the LanceDB memory plugin + embedding adapters. · [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: external memory plugin packaging. · [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: `ltm` CLI namespace + memory slot live here.


### oc_plugins_memory_wiki (12t · 12s · 11d)

**Terms** — [term_knowledge_graph](../../term_dictionary/term_knowledge_graph.md) — knowledge graph; relevance: relationship edges + entity pages form a graph. · [term_knowledge_base](../../term_dictionary/term_knowledge_base.md) — knowledge base; relevance: the compiled vault is a maintained KB. · [term_agentic_memory](../../term_dictionary/term_agentic_memory.md) — agentic memory; relevance: wiki is a durable-memory layer beside active memory. · [term_episodic_memory](../../term_dictionary/term_episodic_memory.md) — episodic memory; relevance: contrasts wiki's semantic/compiled layer vs episodic recall. · [term_graphrag](../../term_dictionary/term_graphrag.md) — GraphRAG; relevance: structured claims + relationships enable graph-aware retrieval. · [term_hipporag](../../term_dictionary/term_hipporag.md) — HippoRAG; relevance: provenance-aware retrieval analogue. · [term_temporal_knowledge_graph](../../term_dictionary/term_temporal_knowledge_graph.md) — temporal KG; relevance: `lastRefreshedAt`/stale-page tracking is temporal. · [term_markdown](../../term_dictionary/term_markdown.md) — Markdown; relevance: vault pages are Markdown with frontmatter blocks. · [term_xwiki](../../term_dictionary/term_xwiki.md) — XWiki; relevance: structured-wiki/knowledge-vault analogue. · [term_memory_dreaming](../../term_dictionary/term_memory_dreaming.md) — memory dreaming; relevance: dreaming stays with active memory, not the wiki layer. · [term_honcho](../../term_dictionary/term_honcho.md) — Honcho memory; relevance: an active-memory backend the wiki bridges from. · [term_zettelkasten](../../term_dictionary/term_zettelkasten.md) — Zettelkasten; relevance: deterministic linked-page knowledge-vault model.

**Docs** — [hermes_optional_skills_catalog](../hermes_agent/hermes_optional_skills_catalog.md) — optional skills catalog (incl. Obsidian); relevance: Obsidian render-mode integration parallel. · [hermes_memory_providers_honcho](../hermes_agent/hermes_memory_providers_honcho.md) — Honcho memory provider; relevance: active-memory backend the wiki bridges. · [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory provider catalog; relevance: where a compiled-knowledge layer fits among backends. · [cc_memory_overview](../claude_code/cc_memory_overview.md) — Claude Code memory overview; relevance: durable vs active memory split parallel. · [band/band_agent_api_memories](../band/band_agent_api_memories.md) — Band memory API; relevance: structured memory/claims API analogue. · [band/band_overview](../band/band_overview.md) — Band overview; relevance: agent knowledge/memory product context. · [hermes_work_with_skills_guide](../hermes_agent/hermes_work_with_skills_guide.md) — skills guide; relevance: `wiki_*` agent tools register like skills. · [oc_plugins_memory_lancedb](oc_plugins_memory_lancedb.md) — memory-lancedb (planned, this series); relevance: the active-memory backend in the hybrid pattern. · [oc_plugins_oc_path](oc_plugins_oc_path.md) — oc-path (planned, this series); relevance: byte-fidelity file edits over the same Markdown vault substrate. · [oc_plugins_plugin_inventory](oc_plugins_plugin_inventory.md) — plugin inventory (planned, this series); relevance: memory-wiki is a bundled core plugin. · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link.

**Repos** — [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory subsystem; relevance: implements memory-wiki compile/search/bridge. · [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: bundled plugin packaging. · [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: `openclaw wiki` CLI surface lives here.


### oc_plugins_message_presentation (10t · 12s · 11d)

**Terms** — [term_channel_adapter](../../term_dictionary/term_channel_adapter.md) — channel adapter; relevance: channel plugins declare `presentationCapabilities` on their outbound adapter. · [term_capability_negotiation](../../term_dictionary/term_capability_negotiation.md) — capability negotiation; relevance: core adapts presentation to advertised renderer limits. · [term_markdown](../../term_dictionary/term_markdown.md) — Markdown; relevance: `markdownDialect` (slack-mrkdwn/discord-markdown) per channel. · [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider/channel plugin; relevance: per-provider native render targets (Slack/Discord/Teams/Feishu). · [term_tool_descriptor](../../term_dictionary/term_tool_descriptor.md) — tool descriptor; relevance: `describeMessageTool` declares presentation support. · [term_configuration_model](../../term_dictionary/term_configuration_model.md) — config/contract model; relevance: the typed `MessagePresentation`/`limits` contract. · [term_webhook](../../term_dictionary/term_webhook.md) — webhook/interaction; relevance: button/select `callback` actions travel the channel interaction path. · [term_function_calling](../../term_dictionary/term_function_calling.md) — command invocation; relevance: `action.type:"command"` runs a native slash command. · [term_command_pattern](../../term_dictionary/term_command_pattern.md) — command pattern; relevance: button actions map to commands/callbacks. · [term_idempotency](../../term_dictionary/term_idempotency.md) — idempotency; relevance: `reusable` buttons for repeatable/idempotent actions.

**Docs** — [hermes_messaging_slack](../hermes_agent/hermes_messaging_slack.md) — Slack messaging; relevance: Block Kit native render target. · [hermes_gateway_feishu_features](../hermes_agent/hermes_gateway_feishu_features.md) — Feishu interactive cards; relevance: Feishu card render target. · [hermes_discord_advanced](../hermes_agent/hermes_discord_advanced.md) — Discord advanced; relevance: components/container render target. · [hermes_messaging_media_settings](../hermes_agent/hermes_messaging_media_settings.md) — media settings; relevance: per-channel rendering/limits. · [hermes_messaging_gateway_architecture](../hermes_agent/hermes_messaging_gateway_architecture.md) — messaging gateway architecture; relevance: core-render-flow + delivery path analogue. · [hermes_deliverable_mode](../hermes_agent/hermes_deliverable_mode.md) — deliverable/rich output; relevance: rich outbound UI contract parallel. · [cc_channels_setup](../claude_code/cc_channels_setup.md) — channel setup; relevance: channel render-capability declaration parallel. · [oc_plugins_plugin_inventory](oc_plugins_plugin_inventory.md) — plugin inventory (planned, this series); relevance: channel renderers are inventoried plugins. · [oc_plugins_manifest_channel_ui_setup](oc_plugins_manifest_channel_ui_setup.md) — channel/UI manifest (planned, this series); relevance: channel plugins declared via manifest render this. · [oc_plugins_plugin_permission_requests](oc_plugins_plugin_permission_requests.md) — permission requests (planned, this series); relevance: approval prompts are built as presentation blocks. · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link.

**Repos** — [repo_openclaw_channels_messaging](../../../areas/code_repos/repo_openclaw_channels_messaging.md) — messaging channels; relevance: implements per-provider presentation renderers. · [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels framework; relevance: outbound-adapter `presentationCapabilities`. · [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: presentation SDK helpers from `plugin-sdk/interactive-runtime`.


### oc_plugins_oc_path (10t · 11s · 11d)

**Terms** — [term_markdown](../../term_dictionary/term_markdown.md) — Markdown; relevance: `oc://` addresses markdown frontmatter/sections/items/fields. · [term_json_schema](../../term_dictionary/term_json_schema.md) — JSON Schema/JSON; relevance: jsonc/json5 leaf addressing + the plugin's own manifest. · [term_configuration_model](../../term_dictionary/term_configuration_model.md) — config model; relevance: example resolves/sets `config.jsonc/plugins/github/enabled`. · [term_sandbox](../../term_dictionary/term_sandbox.md) — sandbox/isolation; relevance: in-process, no network sockets, pure file transform. · [term_threat_model](../../term_dictionary/term_threat_model.md) — threat model/safety; relevance: redaction-sentinel guard refuses `__OPENCLAW_REDACTED__` writes (`OC_EMIT_SENTINEL`). · [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin SDK; relevance: substrate verbs are private; consumers use the CLI or build a plugin against the SDK. · [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw host; relevance: opt-in bundled plugin under `extensions/oc-path/`. · [term_command_pattern](../../term_dictionary/term_command_pattern.md) — command pattern; relevance: `resolve`/`find`/`set`/`validate`/`emit` subcommands via commander. · [term_idempotency](../../term_dictionary/term_idempotency.md) — idempotency; relevance: byte-fidelity round-trips + dry-run before apply. · [term_access_control](../../term_dictionary/term_access_control.md) — access control; relevance: narrow addressing/byte-preserving layer, not owner of higher-level semantics.

**Docs** — [cc_dot_claude_directory](../claude_code/cc_dot_claude_directory.md) — `.claude` directory/config files; relevance: addressing workspace config files analogue. · [cc_plugin_user_config_and_env](../claude_code/cc_plugin_user_config_and_env.md) — plugin user config/env; relevance: addressing single config leaves parallel. · [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin components; relevance: CLI-command-only plugin surface analogue. · [hermes_event_hooks](../hermes_agent/hermes_event_hooks.md) — event hooks; relevance: hooks/agents treat oc-path as deterministic substrate. · [hermes_lsp_diagnostics](../hermes_agent/hermes_lsp_diagnostics.md) — LSP diagnostics; relevance: editor-integration single-node addressing parallel. · [pi/pi_extensions_overview](../pi/pi_extensions_overview.md) — Pi extensions; relevance: opt-in CLI-extension plugin model. · [pi/pi_packages](../pi/pi_packages.md) — Pi packages/CLI; relevance: CLI-surface plugin distribution analogue. · [oc_plugins_plugin_inventory](oc_plugins_plugin_inventory.md) — plugin inventory (planned, this series); relevance: oc-path is a bundled core plugin entry. · [oc_plugins_memory_wiki](oc_plugins_memory_wiki.md) — memory-wiki (planned, this series); relevance: same Markdown-vault substrate, different ownership (memory writes go through memory plugins). · [oc_plugins_manifest_overview](oc_plugins_manifest_overview.md) — manifest overview (planned, this series); relevance: shows oc-path's own `openclaw.plugin.json` (activation onCommands). · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link.

**Repos** — [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: `extensions/oc-path/` lives here. · [repo_openclaw_cli_wizard](../../../areas/code_repos/repo_openclaw_cli_wizard.md) — CLI/wizard; relevance: `openclaw path` CLI registration. · [repo_openclaw_apps](../../../areas/code_repos/repo_openclaw_apps.md) — apps/editor integrations; relevance: editor extensions map `oc://` to nodes.


### oc_plugins_plugin_inventory (10t · 11s · 11d)

**Terms** — [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — manifest; relevance: inventory is generated from `openclaw.plugin.json`/`package.json`. · [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin SDK; relevance: every inventoried plugin is built against the SDK. · [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider plugin; relevance: many inventory entries are provider plugins. · [term_channel_adapter](../../term_dictionary/term_channel_adapter.md) — channel adapter; relevance: channel plugins are a major inventory category. · [term_skill_manifest](../../term_dictionary/term_skill_manifest.md) — skill manifest; relevance: skill plugins appear in the catalog. · [term_capability_negotiation](../../term_dictionary/term_capability_negotiation.md) — capability ownership; relevance: each entry describes what capability the plugin adds. · [term_openclaw](../../term_dictionary/term_openclaw.md) — OpenClaw host; relevance: core-npm vs external-vs-source distribution is host-relative. · [term_npm](../../term_dictionary/term_npm.md) — npm; relevance: core-npm-package vs official-external-npm distribution tiers. · [term_function_calling](../../term_dictionary/term_function_calling.md) — tool plugins; relevance: tool plugins are an inventory category. · [term_vector_database](../../term_dictionary/term_vector_database.md) — vector DB; relevance: memory-lancedb/memory-wiki are inventoried memory plugins.

**Docs** — [cc_plugin_marketplaces_and_install](../claude_code/cc_plugin_marketplaces_and_install.md) — Claude Code marketplaces/install; relevance: distribution-tier + install analogue. · [cc_plugin_sources](../claude_code/cc_plugin_sources.md) — plugin sources; relevance: bundled vs external vs local source parallel. · [cc_plugin_cli_commands](../claude_code/cc_plugin_cli_commands.md) — plugin CLI commands; relevance: `openclaw plugins install/inspect` flow. · [cc_host_and_manage_marketplaces](../claude_code/cc_host_and_manage_marketplaces.md) — host/manage marketplaces; relevance: ClawHub/npm distribution analogue. · [pi/pi_packages](../pi/pi_packages.md) — Pi packages; relevance: package distribution/install parallel. · [hermes_optional_skills_catalog](../hermes_agent/hermes_optional_skills_catalog.md) — optional skills catalog; relevance: generated catalog-of-installables analogue. · [hermes_plugins_system](../hermes_agent/hermes_plugins_system.md) — Hermes plugin system; relevance: bundled-vs-installable plugin model. · [oc_plugins_manifest_overview](oc_plugins_manifest_overview.md) — manifest overview (planned, this series); relevance: inventory generated from manifests. · [oc_plugins_oc_path](oc_plugins_oc_path.md) — oc-path (planned, this series); relevance: a bundled core-npm plugin entry. · [oc_plugins_memory_lancedb](oc_plugins_memory_lancedb.md) — memory-lancedb (planned, this series); relevance: an official-external package entry. · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link.

**Repos** — [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: `extensions/*` is the inventory source. · [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — monorepo; relevance: core npm package `files` exclusions decide distribution tier. · [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — LLM providers; relevance: provider plugins dominate the inventory. · [repo_openclaw_channels](../../../areas/code_repos/repo_openclaw_channels.md) — channels; relevance: channel plugins are a major inventory category.


### oc_plugins_plugin_permission_requests (10t · 11s · 11d)

**Terms** — [term_sandbox](../../term_dictionary/term_sandbox.md) — sandbox; relevance: exec approvals/host exec policy are a sibling gate. · [term_iframe_sandbox](../../term_dictionary/term_iframe_sandbox.md) — iframe sandbox; relevance: per-action approval as an isolation/consent boundary analogue. · [term_posix_permissions](../../term_dictionary/term_posix_permissions.md) — POSIX permissions; relevance: allow/deny decision model parallel. · [term_gateway_hooks](../../term_dictionary/term_gateway_hooks.md) — gateway hooks; relevance: prompts start in a `before_tool_call` hook. · [term_tool_registry](../../term_dictionary/term_tool_registry.md) — tool registry; relevance: optional-tools gate controls tool exposure via `tools.allow`. · [term_capability_negotiation](../../term_dictionary/term_capability_negotiation.md) — capability negotiation; relevance: choosing the right gate per decision point. · [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin SDK; relevance: `definePluginEntry`/`api.on("before_tool_call")` SDK surface. · [term_mcp](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: MCP approval elicitations bridge through plugin approvals. · [term_function_calling](../../term_dictionary/term_function_calling.md) — tool call; relevance: approval gates a model-selected tool call. · [term_threat_model](../../term_dictionary/term_threat_model.md) — threat model; relevance: severity/`allow-once` choices encode risk of the action.

**Docs** — [cc_sdk_tool_approval_handling](../claude_code/cc_sdk_tool_approval_handling.md) — SDK tool approval handling; relevance: direct per-tool-call approval analogue. · [cc_sdk_permissions_evaluation](../claude_code/cc_sdk_permissions_evaluation.md) — permissions evaluation; relevance: allow/deny decision evaluation parallel. · [cc_permission_system_and_rules](../claude_code/cc_permission_system_and_rules.md) — permission system/rules; relevance: gate-selection + allowlist model. · [cc_channel_permission_relay](../claude_code/cc_channel_permission_relay.md) — channel permission relay; relevance: routing approval prompts to chat targets. · [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permissions; relevance: distinguishes exec/sandbox gate from plugin-approval gate. · [hermes_security_command_approval](../hermes_agent/hermes_security_command_approval.md) — command approval; relevance: exec-approval sibling gate. · [pi/pi_security_model](../pi/pi_security_model.md) — Pi security model; relevance: approval/permission gating analogue. · [oc_plugins_message_presentation](oc_plugins_message_presentation.md) — message presentation (planned, this series); relevance: approval prompts render as presentation blocks/buttons. · [oc_plugins_manifest_channel_ui_setup](oc_plugins_manifest_channel_ui_setup.md) — channel/UI manifest (planned, this series); relevance: `tools.allow` optional-tools discovery gate context. · [oc_plugins_manifest_overview](oc_plugins_manifest_overview.md) — manifest overview (planned, this series); relevance: plugins declaring approval hooks ship a manifest. · [entry_openclaw_docs](../../../0_entry_points/entry_openclaw_docs.md) — OpenClaw docs hub (planned, master W1); relevance: navigation back-link.

**Repos** — [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security subsystem; relevance: implements exec/plugin approval policy. · [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: `plugin.approval.*` flow + pending-approval delivery. · [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extension framework; relevance: `before_tool_call.requireApproval` hook SDK.

**Snippets** — [snippet_openclaw_acp_permission_relay](../../code_snippets/snippet_openclaw_acp_permission_relay.md) — ACP permission relay; relevance: routes native/MCP approval through plugin approvals. · [snippet_openclaw_gateway_exec_approval_manager](../../code_snippets/snippet_openclaw_gateway_exec_approval_manager.md) — exec approval manager; relevance: sibling exec-approval gate (`approvals.exec` vs `approvals.plugin`). · [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — agent tool policy; relevance: optional-tools/`tools.allow` discovery gate. · [snippet_openclaw_gateway_node_command_policy](../../code_snippets/snippet_openclaw_gateway_node_command_policy.md) — node command policy; relevance: host exec policy/allowlist. · [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — exec audit runtime; relevance: durable exec allowlist auditing. · [snippet_hermes_agent_acp_tools_permission](../../code_snippets/snippet_hermes_agent_acp_tools_permission.md) — tool permission; relevance: per-call approval decision model. · [snippet_hermes_agent_tools_approval_ui](../../code_snippets/snippet_hermes_agent_tools_approval_ui.md) — approval UI; relevance: allow-once/allow-always/deny buttons. · [snippet_hermes_agent_tools_approval_policy](../../code_snippets/snippet_hermes_agent_tools_approval_policy.md) — approval policy; relevance: `allowedDecisions`/timeout behavior. · [snippet_hermes_agent_core_shell_hooks_allowlist](../../code_snippets/snippet_hermes_agent_core_shell_hooks_allowlist.md) — shell hook allowlist; relevance: exec allowlist sibling gate. · [snippet_hermes_agent_gw_hooks](../../code_snippets/snippet_hermes_agent_gw_hooks.md) — gateway hooks; relevance: `before_tool_call` hook registration. · [snippet_hermes_agent_skills_mcp_native](../../code_snippets/snippet_hermes_agent_skills_mcp_native.md) — native MCP; relevance: MCP tool approval elicitation routing.

## Undigested Terms Plan

| Term | Disposition |
|---|---|
| plugin manifest / `openclaw.plugin.json` | Documented as `oc_plugins_manifest_*` doc notes; link existing `term_plugin_manifest`. No new term. |
| configSchema / JSON Schema requirements | Subject of note 5; link existing `term_json_schema`. No new term. |
| modelCatalog / modelSupport / providerEndpoints / providerRequest / modelPricing / modelIdNormalization | Manifest config fields → note 2 body; link `term_model_catalog` / `term_provider_plugin` / `term_provider_routing`. No new term. |
| contracts / capability ownership snapshot | note 3 body; link `term_capability_negotiation` / `term_tool_registry`. No new term. |
| activation / qaRunners / setup / uiHints / channelConfigs / commandAliases | Manifest control-plane fields → note 4 body; link `term_channel_adapter` / `term_configuration_model`. No new term. |
| memory-lancedb / LanceDB vector store | note 6 body; link existing `term_vector_database` / `term_columnar_storage` / `term_storage_engine`. No new term. |
| embeddings (provider-backed / Ollama / OpenAI-compatible) | note 6 body; link existing `term_embedding` / `term_matryoshka_embeddings`. No new term. |
| memory-wiki / compiled knowledge vault / vault modes / structured claims / OKF | note 7 body; link `term_knowledge_graph` / `term_knowledge_base` / `term_agentic_memory` / `term_honcho`. No new term. |
| `oc://` workspace-file addressing scheme | note 9 body (OpenClaw-specific addressing); link `term_configuration_model` / `term_markdown`. No new term. |
| message presentation / presentation blocks / renderer contract / degradation | note 8 body; link `term_channel_adapter` / `term_capability_negotiation`. No new term. |
| plugin permission requests / `plugin.approval.*` / exec approvals / Codex/MCP approvals | note 11 body; link `term_sandbox` / `term_gateway_hooks` / `term_mcp`. No new term. |
| Core npm / Official external / Source checkout (plugin distribution tiers) | note 10 taxonomy; link `term_plugin_sdk` / `term_plugin_manifest`. No new term. |

**New `term_dictionary` captures: 0.** All vocabulary is either OpenClaw-product-specific (digested into the
`oc_` doc notes) or already covered by an existing substantive term note (linked, not duplicated). No genuinely
cross-cutting, vault-reusable term with no existing note and no doc-page home appeared in these 7 pages. Augment
Step 2d re-scans to confirm.

## Term-Note Authoring Requirements

**N/A (0 new terms).** Inherited from master: if augment's re-scan surfaces a genuinely reusable cross-cutting
it to the best-fit `acronym_glossary_*.md` (the agentic/LLM glossary). No term definition is ever inlined in an
`oc_*` digest note.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (11 notes, P3). All gates must pass before commit.

| Gate | Name | Check |
|---|---|---|
| G1 | Format | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` on each new note (YAML field order; `## Overview` + `## Related Notes` present; footer). |
| G2 | Grounding | Diff each note against its `inbox/openclaw_docs/plugins/<page>.md` source section; no invented fields/claims. |
| G3 | Density + Coverage | ≤400 lines / ≤2,500 words / ≤6 code blocks per note; every mapped section covered. |
| G4 | Cross-Reference | ≥6 relevancy-selected `term_dictionary` links + repo/sibling/other links, each with a relevance statement, all indexed `[text](path.md)`. |
| G6 | Broken-link | `/tessellum-fix-broken-links`; 0 broken relative paths after reindex. |
| G7/G8 | Discoverability | Every new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (in-degree ≥1, anti-island) — satisfied via `entry_openclaw_docs.md` + repo/term inlinks. |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_manifest_overview oc_plugins_manifest_provider_model_metadata oc_plugins_manifest_generation_tool_metadata oc_plugins_manifest_channel_ui_setup oc_plugins_manifest_discovery_validation oc_plugins_memory_lancedb oc_plugins_memory_wiki oc_plugins_message_presentation oc_plugins_oc_path oc_plugins_plugin_inventory oc_plugins_plugin_permission_requests"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required H2 sections
  for sec in "## Overview" "## Related Notes"; do
    grep -qF "$sec" "$f" || echo "MISSING SECTION ($sec): $n"
  done
  # source_url required
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -qE '^source_url: https://docs\.openclaw\.ai/' "$f" || echo "MISSING source_url: $n"; }
  # G3 density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 )); lines=$(wc -l < "$f")
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] || [ "$lines" -gt 400 ]; } && echo "DENSITY WARNING: $n (w=$words cb=$cb L=$lines)"
  # sibling-prefix cross-ref present (G4)
  grep -qE "\($SIBLING_PREFIX[a-z_]+\.md\)" "$f" || echo "NO SIBLING $SIBLING_PREFIX XREF: $n"
done

python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"
# After reindex: G5 ghost + G6 broken-link sweep
bash scripts/update_notes_database.sh --force
# /tessellum-fix-ghost-references and /tessellum-fix-broken-links per master
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_manifest_overview | concept | 700 | 3 | ✅ |
| 2 | oc_plugins_manifest_provider_model_metadata | model | 700 | 5 | ✅ |
| 3 | oc_plugins_manifest_generation_tool_metadata | model | 600 | 4 | ✅ |
| 4 | oc_plugins_manifest_channel_ui_setup | model | 650 | 5 | ✅ |
| 5 | oc_plugins_manifest_discovery_validation | procedure | 600 | 3 | ✅ |
| 6 | oc_plugins_memory_lancedb | procedure | 650 | 6 | ✅ |
| 7 | oc_plugins_memory_wiki | concept | 700 | 5 | ✅ |
| 8 | oc_plugins_message_presentation | model | 650 | 6 | ✅ |
| 9 | oc_plugins_oc_path | procedure | 500 | 4 | ✅ |
| 10 | oc_plugins_plugin_inventory | model | 600 | 2 | ✅ |
| 11 | oc_plugins_plugin_permission_requests | procedure | 600 | 3 | ✅ |

No note approaches caps. The 9,680w/23-code `manifest.md` is split 5-way so each manifest note reproduces ≤6
representative JSON snippets verbatim; memory-lancedb (16 source fences) and message-presentation (12 source
fences) are each held to ≤6 by reproducing only the canonical config/contract examples.

## Entry Point Decision (inherited from master)

Contributes **11 rows** to `entry_openclaw_docs.md` (CREATED as master pre-step W1; >30-note total ⇒ required)
under the **Plugins** section (pl04 cluster). Each new note receives its back-link from `entry_openclaw_docs.md`
at finalization (satisfies G7/G8 in-degree ≥1). No separate entry point for this sub-plan.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links for G7/G8 (DB-verify at execution; all sources confirmed present):

- `entry_openclaw_docs.md` (planned W1) → **all 11 notes** (primary anti-island guarantee).
- `repo_openclaw_extensions` → notes 1, 2, 3, 4, 5, 10 (manifest + inventory are the extension/plugin framework docs).
- `repo_openclaw_memory` → notes 6, 7 (both memory plugins).
- `repo_openclaw_extensions_llm_providers` → note 2 (provider/model manifest metadata).
- `repo_openclaw_channels_messaging` → note 8 (message presentation render contract).
- `repo_openclaw_security` → note 11 (permission-request approval gate).
- `repo_openclaw_apps` / `repo_openclaw_cli_wizard` → note 9 (`oc-path` CLI).
- `term_plugin_manifest` → notes 1, 5, 10; `term_vector_database` → note 6; `term_knowledge_graph` → note 7;
  `term_sandbox` → note 11; `term_channel_adapter` → notes 4, 8.

## Pacing Rules (inherited from master)

One execution phase, 11 notes. Cap dynamic-workflow fan-out at ~30 agents/run; embed the per-note contract
manifest in the dispatch script. Re-read each source page before authoring; reproduce config/JSON snippets
verbatim. One BB per note. Reindex incrementally; verify `note_links` populated + 0 broken links + in-degree ≥1
before commit. `git pull --rebase --autostash` first; commit + push per wave; no Claude co-author trailer.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**What was locked.** Replaced the PLAN-stage `## Candidate Cross-References` with a LOCKED
`## Per-Note Related Notes Mapping` at the raised xref floors (**≥8 terms · ≥10 snippets · ≥10 docs per
note**, relevance-selected from a fresh re-read of all 7 source pages under `inbox/openclaw_docs/plugins/`,
with vault-root-correct relative paths (term `../../term_dictionary/`, snippet `../../code_snippets/`,
sibling `oc_Y.md`, cross-folder doc `../<folder>/`, repo `../../../areas/code_repos/`, entry
`../../../0_entry_points/`). Summary-statistics cross-ref line updated to the locked standard.

this-series `oc_*` siblings + `entry_openclaw_docs.md` (master W1, expected `(planned)`). Programmatic floor
check passed for ALL 11 notes (every note ≥8 terms, ≥10 snippets, ≥10 docs with ≥5 existing). All snippets

**Per-note counts (terms / snippets / docs[existing] / repos):**

| # | Note | terms | snippets | docs (existing) | repos | floors |
|---|---|---:|---:|---:|---:|---|
| 1 | oc_plugins_manifest_overview | 11 | 11 | 11 (7) | 3 | ✅ |
| 2 | oc_plugins_manifest_provider_model_metadata | 11 | 11 | 11 (8) | 3 | ✅ |
| 3 | oc_plugins_manifest_generation_tool_metadata | 10 | 11 | 10 (7) | 3 | ✅ |
| 4 | oc_plugins_manifest_channel_ui_setup | 10 | 11 | 11 (8) | 3 | ✅ |
| 5 | oc_plugins_manifest_discovery_validation | 10 | 11 | 11 (7) | 3 | ✅ |
| 6 | oc_plugins_memory_lancedb | 12 | 12 | 11 (7) | 3 | ✅ |
| 7 | oc_plugins_memory_wiki | 12 | 12 | 11 (7) | 3 | ✅ |
| 8 | oc_plugins_message_presentation | 10 | 12 | 11 (7) | 3 | ✅ |
| 9 | oc_plugins_oc_path | 10 | 11 | 11 (7) | 3 | ✅ |
| 10 | oc_plugins_plugin_inventory | 10 | 11 | 11 (7) | 4 | ✅ |
| 11 | oc_plugins_plugin_permission_requests | 10 | 11 | 11 (7) | 3 | ✅ |

**Two ghost links caught + corrected during augment** (would have failed G5 at execution): `term_redaction`
(MISSING in DB) → re-pointed to `term_threat_model` (verified) on note 9; `term_semantic_versioning`
(MISSING in DB) → replaced with `term_skill_manifest` (verified) on note 5. No other ghosts.

**New-term scan (Step 2d, re-read).** **0 new `term_dictionary` captures** — confirmed, consistent with the
plan's existing Undigested Terms Plan and the master design decision (OpenClaw vocab → `oc_` doc notes; link
existing terms). One **new-term candidate** surfaced and was considered: **OKF (Open Knowledge Format)** — a
portable concept-exchange bundle format imported by `memory-wiki`. It has NO existing term note (BM25 across
`terminology` returned only false-positives: `term_onnx`, `term_skills`, `term_auth_profile`). Disposition:
**keep as note-7 body content, no capture** — within these 7 pages OKF appears only as a single memory-wiki
import feature (not cross-cutting across the sub-plan), so per the master's conservative OpenClaw-vocab policy
it is digested into the `oc_plugins_memory_wiki` note body rather than captured as a standalone term. If a
later sub-plan (e.g. a data-catalog/wiki page) references OKF independently, re-evaluate for a
`term_open_knowledge_format` capture via `/tessellum-capture-term-note` (best-fit glossary: the agentic/LLM
glossary). The "structured claims/evidence/provenance" wiki vocabulary is OpenClaw-product-specific (digested
excluded.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors per note) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED)` present; programmatic count: all 11 notes ≥8 terms (10–12), ≥10 snippets (11–12), ≥10 docs (10–11, ≥5 existing). Every link has a `; relevance:` statement (not a bare link). |
| CP2 | 9-GATE present per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table present with G1 Format, G2 Grounding, G3 Density+Coverage, G4 Cross-Reference, G5 Ghost, G6 Broken-link, G7/G8 Discoverability; single execution phase. |
| CP3 | Entry point inherited (entry_openclaw_docs planned at W1) | **PASS** | `## Entry Point Decision` inherits master: 11 rows to `entry_openclaw_docs.md` (CREATED master pre-step W1; >30-note total ⇒ required); each note gets its back-link at finalization. DB-confirmed `entry_openclaw_docs.md` not yet present (correctly planned). |
| CP4 | Size (≤30 or split) | **PASS** | 11 planned notes ≤ 30. Self-contained sub-plan of a master+sub-plan split. |
| CP5 | Format derived (not invented) | **PASS** | YAML field order + `## Overview`/`## Related Notes` + `**Source**`/`**Last Updated**`/`**Status**` footer inherited from master's Format Definition, itself derived from the existing `claude_code/` + `pi/` doc corpora (same source type). |
| CP6 | Density (≤400L / ≤2500w / ≤6 code per note) | **PASS** | `## Density Re-Assessment` table: all 11 notes ≤700w / ≤6 code; manifest split 5-way (9,643w measured → 5 notes). No borderline note. |
| CP7 | Sources measured (not guessed) | **PASS** | Re-measured 2026-06-21: manifest 9,643w / memory-lancedb 1,285w / memory-wiki 2,103w / message-presentation 1,913w / oc-path 958w / plugin-inventory 2,229w / plugin-permission-requests 1,025w. All within ±5% of plan estimates (manifest H2 count 31 confirmed via grep). |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` (0 new terms) + `## Term-Note Authoring Requirements` (N/A, inherited from master, multi-source mandate stated) present; Step 2d re-scan confirmed 0 captures (OKF candidate documented, kept in note 7 body). |
| CP8f | Slug specificity / collision audit (all notes) | **PASS** | 0 new term slugs (nothing to rename). Doc-note collision audit: 11 `oc_plugins_*` slugs searched against `term_dictionary/` + `documentation/` — no `oc_*` planned note duplicates an existing term or doc (OpenClaw product docs; code side is `repo_openclaw*`, correctly LINKED not recreated). |
| CP9 | Discoverability / inlinks (G8, in-degree ≥1) | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound source (`entry_openclaw_docs.md` → all 11, plus repo/term inlinks); G7/G8 in the gate table; executed-and-verified at finalization. |

**RESULT: 9/9 (CP1–CP9 incl. CP8f) PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
