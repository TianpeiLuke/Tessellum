---
title: Sub-Plan pl14 — OpenClaw Docs: Plugins Reference (memory, Microsoft, migration)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages:
  - plugins/reference/memory-core
  - plugins/reference/memory-lancedb
  - plugins/reference/memory-wiki
  - plugins/reference/microsoft
  - plugins/reference/microsoft-foundry
  - plugins/reference/migrate-claude
  - plugins/reference/migrate-hermes
---

# Sub-Plan pl14: Plugins

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md).
> Shared routing (`resources/documentation/openclaw/`, prefix `oc_`), format/YAML, dedup-before-create,
> 9-GATE, cross-refs, undigested-terms policy, and entry-point wiring are ALL inherited from the master.

## Scope

The 7 `plugins/reference/*` pages covering OpenClaw's **memory** plugins (`memory-core`, `memory-lancedb`,
`memory-wiki`), the **Microsoft** provider plugins (`microsoft` text-to-speech, `microsoft-foundry` model +
image-generation provider), and the **migration** plugins (`migrate-claude`, `migrate-hermes`). These are
the plugin-reference cards — one card per `@openclaw/*` package describing its distribution, install route,
and contract surface; `microsoft-foundry` is the lone substantive card with full config/requirements/
troubleshooting. **Priority P3 (Phase C — plugin reference sprawl).** The code-side counterparts
(`repo_openclaw_memory`, `repo_openclaw_extensions_llm_providers`, `repo_openclaw_extensions_voice_speech`,
`repo_openclaw_extensions`) are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **864 measured words**. **Planned: 5 notes.**

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| Memory Core plugin | plugins/reference/memory-core | 43 | 0 | 2 | 0 | model (plugin reference card) |
| Memory Lancedb plugin | plugins/reference/memory-lancedb | 63 | 0 | 3 | 0 | model (plugin reference card) |
| Memory Wiki plugin | plugins/reference/memory-wiki | 61 | 0 | 3 | 0 | model (plugin reference card) |
| Microsoft plugin | plugins/reference/microsoft | 43 | 0 | 2 | 0 | model (plugin reference card) |
| Microsoft Foundry plugin | plugins/reference/microsoft-foundry | 530 | 1 | 6 | 0 | procedure (provider config) |
| Migrate Claude plugin | plugins/reference/migrate-claude | 67 | 0 | 2 | 0 | model (plugin reference card) |
| Migrate Hermes plugin | plugins/reference/migrate-hermes | 57 | 0 | 2 | 0 | model (plugin reference card) |

Measurement method: `wc -w` on the verbatim mirror file (frontmatter included); code = `grep -c '```' / 2`;
H2 = `^## `, H3 = `^### `. The reference cards share a fixed `## Distribution` / `## Surface` (+ optional
`## Related docs`) skeleton; only `microsoft-foundry` carries a manual-content block (Requirements / Chat
models / MAI image generation / Troubleshooting) inside the `openclaw-plugin-reference:manual-*` markers.

## Content Strategy

- **Prioritize**: the only substantive page, `microsoft-foundry` (530w, full config + auth + image-gen +
  troubleshooting), gets a dedicated procedure note. It is the one page where a reader needs digested,
  cross-referenced operational content.
- **Group thin stubs by theme (density-driven consolidation)**: the other 6 pages are 43–67-word
  reference-card stubs (package name + install route + contract surface). Each alone is far below the floor
  for a useful atomic note, so they are consolidated into **one note per coherent plugin family**:
  - the 3 **memory** plugins → one `oc_plugins_reference_memory.md` (memory-core tools, memory-lancedb
    vector recall, memory-wiki Obsidian vault) — a single "memory plugin family" reference;
  - the 2 **migration** plugins → one `oc_plugins_reference_migration.md` (migrate-claude, migrate-hermes);
  - the lone **microsoft** TTS plugin (43w) → grouped with the Microsoft provider theme but kept distinct
    from the Foundry config note: it joins a small `oc_plugins_reference_microsoft_speech.md` card.
  This honors the master's "most reference pages = 1 note" intent while refusing to mint 43-word notes that
  would fail G3 density/usefulness. Net: 5 notes for 7 pages (1 split-up of microsoft-foundry NOT needed;
  3 consolidations applied). See Split / Consolidation Decisions.
- **Link-out (do NOT redefine)**: LanceDB internals & vector search → `term_vector_database`,
  `term_vector_search`-adjacent terms, `repo_openclaw_memory`; Foundry model/API mechanics →
  `term_provider_plugin`, `term_model_catalog`, `term_function_calling`, `term_chain_of_thought`,
  `term_oauth`/`term_authentication`, `term_bedrock`/`term_claude` for the Anthropic-on-Foundry note;
  the long-form `/plugins/memory-lancedb` and `/plugins/memory-wiki` guide pages are pl04's territory
  (this sub-plan covers only the `plugins/reference/*` cards) — linked, not duplicated.

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_plugins_reference_memory.md` | model | memory-core.md (Distribution, Surface); memory-lancedb.md (Distribution, Surface, Related docs); memory-wiki.md (Distribution, Surface, Related docs) | 500 | Reference card for OpenClaw's three memory plugins — memory-core (`@openclaw/memory-core`, agent-callable tools, bundled), memory-lancedb (`@openclaw/memory-lancedb`, LanceDB-backed long-term memory with auto-recall/auto-capture/vector search, npm + ClawHub), and memory-wiki (`@openclaw/memory-wiki`, persistent wiki compiler + Obsidian-friendly vault, tools + skills, bundled). Distribution, install route, and contract surface per plugin. |
| 2 | `oc_plugins_reference_microsoft_foundry.md` | procedure | microsoft-foundry.md (Distribution, Surface, Requirements, Chat models, MAI image generation, Troubleshooting) | 650 | Configuring the Microsoft Foundry provider plugin (`@openclaw/microsoft-foundry`): Azure/Foundry resource + API-key or Entra ID (`az login`) auth, chat deployments via `microsoft-foundry/<deployment>` on the `/openai/v1` endpoint (GPT/o*/DeepSeek-V4 → openai-responses; MAI-DS-R1 → openai-completions, reasoning-capable), Claude-on-Foundry as a custom `anthropic-messages` provider with `params.canonicalModelId`, MAI image generation (model refs, generations/edits endpoints, size/pixel constraints), and troubleshooting. |
| 3 | `oc_plugins_reference_microsoft_speech.md` | model | microsoft.md (Distribution, Surface) | 350 | Reference card for the Microsoft (Azure) text-to-speech plugin (`@openclaw/microsoft-speech`): adds TTS provider support via the `speechProviders` contract, bundled with OpenClaw. Distinct from the Microsoft Foundry model/image provider; complements OpenClaw's voice/speech extension layer. |
| 4 | `oc_plugins_reference_migration.md` | model | migrate-claude.md (Distribution, Surface); migrate-hermes.md (Distribution, Surface) | 450 | Reference card for OpenClaw's migration plugins — migrate-claude (`@openclaw/migrate-claude`, imports Claude Code + Claude Desktop instructions, MCP servers, skills, and safe configuration) and migrate-hermes (`@openclaw/migrate-hermes`, imports Hermes configuration, memories, skills, and supported credentials), both bundled and exposing the `migrationProviders` contract. |
| 5 | `oc_plugins_reference_overview.md` | concept | ALL 7 pages: the shared `## Distribution` / `## Surface` reference-card schema and the contract-surface vocabulary (tools, skills, speechProviders, providers, imageGenerationProviders, migrationProviders); cross-cutting view of the pl14 plugin families | 450 | Cross-cutting concept note explaining the OpenClaw plugin-reference card model that ties pl14's pages together: every plugin is an `@openclaw/<name>` package with a distribution + install route and a declared contract surface; enumerates the contract-surface types appearing across the memory, Microsoft, and migration families and how they map to OpenClaw's plugin/extension architecture. |

## Section Coverage Map

```
memory-core.md
├── (frontmatter summary "Adds agent-callable tools.") ─── → note 1 (oc_plugins_reference_memory) + note 5 (schema)
├── ## Distribution (@openclaw/memory-core, included) ──── → note 1
└── ## Surface (contracts: tools) ──────────────────────── → note 1 (+ note 5 contract vocab)
memory-lancedb.md
├── (summary: LanceDB long-term memory, auto-recall/-capture, vector search) → note 1
├── ## Distribution (@openclaw/memory-lancedb, npm; ClawHub) → note 1
├── ## Surface (contracts: tools) ──────────────────────── → note 1
└── ## Related docs ([memory-lancedb](/plugins/memory-lancedb)) → note 1 (References; pl04 long-form linked)
memory-wiki.md
├── (summary: persistent wiki compiler + Obsidian vault) ─ → note 1
├── ## Distribution (@openclaw/memory-wiki, included) ──── → note 1
├── ## Surface (contracts: tools; skills) ──────────────── → note 1
└── ## Related docs ([memory-wiki](/plugins/memory-wiki)) ─ → note 1 (References; pl04 long-form linked)
microsoft.md
├── (summary: text-to-speech provider support) ─────────── → note 3 (oc_plugins_reference_microsoft_speech)
├── ## Distribution (@openclaw/microsoft-speech, included) → note 3
└── ## Surface (contracts: speechProviders) ────────────── → note 3 (+ note 5 contract vocab)
microsoft-foundry.md
├── (summary: Microsoft Foundry model provider) ────────── → note 2 (oc_plugins_reference_microsoft_foundry)
├── ## Distribution (@openclaw/microsoft-foundry, included) → note 2
├── ## Surface (providers: microsoft-foundry; contracts: imageGenerationProviders) → note 2 (+ note 5)
├── ## Requirements (Azure/Foundry resource, API-key/Entra ID auth) → note 2
├── ## Chat models (model ref, /openai/v1, responses vs completions, Claude/Anthropic, MAI-DS-R1) → note 2
├── ## MAI image generation (model refs, endpoints, constraints, json5 config) → note 2
└── ## Troubleshooting (az not found, endpoint missing, MAI-only) → note 2
migrate-claude.md
├── (summary: imports Claude Code/Desktop instr, MCP, skills, config) → note 4 (oc_plugins_reference_migration)
├── ## Distribution (@openclaw/migrate-claude, included) ─ → note 4
└── ## Surface (contracts: migrationProviders) ─────────── → note 4 (+ note 5 contract vocab)
migrate-hermes.md
├── (summary: imports Hermes config, memories, skills, credentials) → note 4
├── ## Distribution (@openclaw/migrate-hermes, included) ─ → note 4
└── ## Surface (contracts: migrationProviders) ─────────── → note 4 (+ note 5 contract vocab)
```

No orphaned sections. The shared `## Distribution` / `## Surface` schema is digested per-note AND abstracted
once in note 5 (the overview/schema concept). `## Related docs` long-form targets (`/plugins/memory-lancedb`,
`/plugins/memory-wiki`) belong to pl04 — referenced as external/sibling links, not duplicated here.

## Split / Consolidation Decisions

| Original | Resolution | Rationale |
|---|---|---|
| memory-core.md (43w) + memory-lancedb.md (63w) + memory-wiki.md (61w) | CONSOLIDATE → note 1 `oc_plugins_reference_memory` | Three 43–63-word reference-card stubs of one plugin family (memory). Individually below any useful-note floor (would fail G3 density/usefulness); together they form a coherent "memory plugin family" card under the master's "most reference pages = 1 note" intent. Same BB (model / reference card). |
| migrate-claude.md (67w) + migrate-hermes.md (57w) | CONSOLIDATE → note 4 `oc_plugins_reference_migration` | Two stub cards sharing the `migrationProviders` contract and the same task (import config/skills/credentials from another agent). Same BB; consolidated for usefulness. |
| microsoft.md (43w) | KEEP as note 3 (its own small card) | TTS `speechProviders` plugin — a different contract surface and capability family from the Foundry model/image provider; merging into note 2 (procedure) would mix BB (model card vs config procedure). Kept distinct; padded with cross-refs to the speech/voice extension layer to clear the usefulness floor. |
| microsoft-foundry.md (530w, 6 H2, 1 code) | KEEP as note 2 (no split) | Substantive single-BB procedure (provider config). Under the 2,500w / 6-code caps; one config concern. No split needed. |
| (cross-cutting schema across all 7 pages) | NEW synthesis → note 5 `oc_plugins_reference_overview` | The 7 pages share the plugin-reference card schema (Distribution/Surface/contract types). A concept note abstracts this once so the family cards (notes 1/3/4) need not each re-explain the schema, and gives the consolidated stubs a discoverable conceptual hub. |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (864 words total). New `oc_` notes: **5**. New `term_dictionary` notes: **0**.
- BB distribution: **model ×3** (notes 1, 3, 4 — reference cards) · **procedure ×1** (note 2 — Foundry
  config) · **concept ×1** (note 5 — card-schema overview). One BB per note.
- Est. digest words ~2,350 (avg ~470/note); range 350–650. All well within the ≤2,500w / ≤400-line caps.
  Only one source code fence (the Foundry json5 image-config block) → reproduced verbatim in note 2 (≤6).
- Notes vs master estimate: master's ~11-note estimate assumed ~1.5 notes/page; the **measured** content is
  6 stub cards (≈55w avg) + 1 substantive page, so density-driven consolidation lands at **5 notes** — this
  is the faithful count and is recorded here for the augment/review reconciliation (CP7).
- **Cross-refs (LOCKED at xref-augment 2026-06-21 — raised floors):** each note maps **≥8 relevance-selected
  relevant `repo_openclaw*` and sibling `oc_*`, each with a per-link relevance statement. ALL cited EXISTING

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> '%/<stem>.md'"` at augment (2026-06-21). Sibling `oc_*` notes in this series do not exist yet → marked
> **(planned, this series)** and counted toward the ≥10-doc floor, but **≥5 of the 10 docs per note are
> Relative paths FROM a note at `resources/documentation/openclaw/oc_X.md`: terms
> `../../term_dictionary/term_Y.md`; other-folder docs `../<folder>/<file>.md` (e.g. `../hermes_agent/…`,
> `../claude_code/…`, `../pi/…`, `../band/…`); sibling oc `oc_Y.md`; repos
> `../../../areas/code_repos/repo_Y.md`; snippets `../../code_snippets/snippet_Y.md`; entry points
> `../../../0_entry_points/entry_Y.md`. Each link carries a relevance statement; bare links are incomplete.

### oc_plugins_reference_memory (10t · 11s · 11d · 4r)

- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted gateway connecting chat platforms to coding agents; relevance: these are `@openclaw/memory-*` first-party plugins.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — agent-managed persistent memory across sessions; relevance: the umbrella capability all three memory plugins provide.
- [Episodic Memory](../../term_dictionary/term_episodic_memory.md) — event/interaction-scoped recall; relevance: memory-lancedb's auto-capture stores per-interaction episodes for later recall.
- [Memory Dreaming](../../term_dictionary/term_memory_dreaming.md) — background consolidation/replay of stored memories; relevance: the consolidation analog to memory-lancedb's auto-capture/auto-recall loop.
- [Vector Database](../../term_dictionary/term_vector_database.md) — store/index of embeddings for similarity lookup; relevance: LanceDB IS the vector DB backing memory-lancedb (link, do not create `term_lancedb`).
- [Embedding](../../term_dictionary/term_embedding.md) — dense vector representation of text; relevance: memory-lancedb embeds captured content to enable vector search.
- [Information Retrieval](../../term_dictionary/term_information_retrieval.md) — finding relevant items from a corpus; relevance: auto-recall is an IR query over the memory store.
- [Knowledge Base](../../term_dictionary/term_knowledge_base.md) — curated, queryable store of facts; relevance: memory-wiki compiles a persistent knowledge vault.
- [Zettelkasten](../../term_dictionary/term_zettelkasten.md) — linked atomic-note knowledge method; relevance: memory-wiki's Obsidian-friendly vault is a zettelkasten-style store (link, do not create `term_obsidian`).
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM invoking declared tools; relevance: memory-core/-wiki expose agent-callable `tools` (and memory-wiki `skills`) as their contract surface.

- [Hermes Memory Provider Catalog](../hermes_agent/hermes_memory_provider_catalog.md) — catalog of pluggable memory backends in the sibling Hermes agent; relevance: direct analog of OpenClaw's memory-plugin family (multiple memory providers behind one contract).
- [Hermes Memory Provider Plugin](../hermes_agent/hermes_memory_provider_plugin.md) — how a memory backend plugs into Hermes; relevance: documents the same memory-provider plugin pattern memory-lancedb/-core implement.
- [Hermes Memory Providers — Honcho](../hermes_agent/hermes_memory_providers_honcho.md) — a concrete external memory backend (Honcho); relevance: a peer to LanceDB as a long-term memory provider behind the same contract.
- [Hermes Context Engine Plugin](../hermes_agent/hermes_context_engine_plugin.md) — context assembly/recall plugin; relevance: auto-recall feeding agent context is the same context-engineering role.
- [Hermes Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — the plugin contract-surface taxonomy; relevance: explains the `tools`/`skills` surface vocabulary these memory cards declare.
- [Claude Code — Plugin Components](../claude_code/cc_plugin_components.md) — the component model of a coding-agent plugin; relevance: cross-tool view of how a bundled plugin (like memory-core) exposes tools.
- [oc_plugins_reference_overview](oc_plugins_reference_overview.md) — (planned, this series) the card-schema concept hub; relevance: the conceptual parent of this family card.
- [oc_plugins_reference_microsoft_foundry](oc_plugins_reference_microsoft_foundry.md) — (planned, this series) sibling plugin card; relevance: another `@openclaw/*` reference card in pl14.
- [oc_plugins_reference_microsoft_speech](oc_plugins_reference_microsoft_speech.md) — (planned, this series) sibling plugin card; relevance: peer family card sharing the Distribution/Surface schema.
- [oc_plugins_reference_migration](oc_plugins_reference_migration.md) — (planned, this series) migration family card; relevance: migrate-hermes imports memories — a consumer of this memory subsystem.

- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — the code-side memory subsystem; relevance: implements memory-core/-lancedb/-wiki documented here.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — the skills subsystem; relevance: memory-wiki contributes `skills` to its surface.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin/extension host; relevance: where these memory plugins register.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the umbrella repo; relevance: ships memory-core/-wiki bundled.

- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — the memory engine core; relevance: the engine behind memory-core's tools.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime wiring; relevance: how the memory plugin runs at request time.
- [snippet_openclaw_memory_host_embeddings](../../code_snippets/snippet_openclaw_memory_host_embeddings.md) — embedding host for memory; relevance: the embedding step of memory-lancedb's vector search.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — what gets embedded; relevance: input shaping for auto-capture vectors.
- [snippet_openclaw_memory_host_memory_schema](../../code_snippets/snippet_openclaw_memory_host_memory_schema.md) — the memory record schema; relevance: the LanceDB-backed store structure.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — agent-side memory search; relevance: the auto-recall query path.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory event hooks; relevance: triggers for auto-capture/auto-recall.
- [snippet_openclaw_memory_host_qmd_process](../../code_snippets/snippet_openclaw_memory_host_qmd_process.md) — wiki/markdown processing in memory host; relevance: memory-wiki's persistent wiki compiler.
- [snippet_hermes_agent_tools_memory](../../code_snippets/snippet_hermes_agent_tools_memory.md) — Hermes memory tool surface; relevance: the agent-callable `tools` pattern memory-core exposes.

### oc_plugins_reference_microsoft_foundry (10t · 11s · 11d · 4r)

- [OpenClaw](../../term_dictionary/term_openclaw.md) — the self-hosted coding-agent gateway; relevance: Foundry is a first-party `@openclaw/microsoft-foundry` provider plugin.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin adding a model/inference provider; relevance: Foundry IS a model + image-generation provider plugin.
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — the set of selectable models/deployments; relevance: onboarding discovers Foundry deployments and writes the model ref `microsoft-foundry/<deployment>`.
- [LLM](../../term_dictionary/term_llm.md) — large language model; relevance: Foundry serves GPT/o*/DeepSeek-V4/MAI-DS-R1 chat models.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: Claude-on-Foundry uses the `anthropic-messages` shape with `params.canonicalModelId`.
- [Function Calling](../../term_dictionary/term_function_calling.md) — tool invocation via the model API; relevance: the openai-responses API path supports tool calls Foundry chat deployments use.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — explicit reasoning traces; relevance: MAI-DS-R1 is reasoning-capable through reasoning content (not `reasoning_effort`).
- [Context Window](../../term_dictionary/term_context_window.md) — the model's token budget; relevance: MAI-DS-R1 carries 163,840-token context/output metadata.
- [OAuth](../../term_dictionary/term_oauth.md) — delegated token-based auth; relevance: Entra ID auth via `az login` + `az account get-access-token` token refresh.
- [Authentication](../../term_dictionary/term_authentication.md) — verifying identity for access; relevance: Foundry supports API-key (`AZURE_OPENAI_API_KEY`) or Entra ID auth.

- [Claude Code — Microsoft Foundry](../claude_code/cc_microsoft_foundry.md) — Claude Code's own Microsoft Foundry provider doc; relevance: the closest cross-tool peer — same Azure/Foundry provider, deployment refs, and auth.
- [Hermes Provider — Azure Foundry Setup](../hermes_agent/hermes_provider_azure_foundry_setup.md) — setting up the Azure AI Foundry provider in Hermes; relevance: same resource/deployment/API-key onboarding as this note.
- [Hermes Provider — Azure Foundry Entra ID](../hermes_agent/hermes_provider_azure_foundry_entra_id.md) — Entra ID auth for Azure Foundry in Hermes; relevance: direct analog of the `az login` token-refresh requirement.
- [Hermes Model Provider Plugin](../hermes_agent/hermes_model_provider_plugin.md) — how a model provider plugs in; relevance: documents the model-provider plugin pattern Foundry implements.
- [Hermes Image Gen Provider Plugin](../hermes_agent/hermes_image_gen_provider_plugin.md) — image-generation provider plugin contract; relevance: Foundry also registers `imageGenerationProviders` for MAI image models.
- [Hermes Provider — AWS Bedrock](../hermes_agent/hermes_provider_aws_bedrock.md) — a peer cloud model provider; relevance: contrast — another cloud-managed provider with its own auth/deployment model.
- [Hermes Fallback Providers](../hermes_agent/hermes_fallback_providers.md) — provider failover; relevance: Foundry slots into multi-provider routing/failover.
- [pi_custom_provider_registration](../pi/pi_custom_provider_registration.md) — registering a custom model provider; relevance: cross-tool framing of the custom `anthropic-messages` provider Claude-on-Foundry needs.
- [oc_plugins_reference_microsoft_speech](oc_plugins_reference_microsoft_speech.md) — (planned, this series) the other Microsoft plugin; relevance: sibling Microsoft-vendor card (TTS vs model/image).
- [oc_plugins_reference_overview](oc_plugins_reference_overview.md) — (planned, this series) card-schema hub; relevance: the conceptual parent of this card.
- [oc_plugins_reference_memory](oc_plugins_reference_memory.md) — (planned, this series) sibling family card; relevance: peer `@openclaw/*` reference card in pl14.

- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the LLM-provider extension layer; relevance: where the Foundry model provider plugs in.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin/extension host; relevance: registers the Foundry provider + imageGenerationProviders contract.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — Hermes agent core (cloud adapters + reasoning normalization); relevance: implements the Azure/Anthropic adapter + reasoning-content handling analog.

- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — OpenClaw's Anthropic provider; relevance: the `anthropic-messages` provider Claude-on-Foundry is configured as.
- [snippet_openclaw_provider_openai](../../code_snippets/snippet_openclaw_provider_openai.md) — OpenClaw's OpenAI-compatible provider; relevance: the `/openai/v1` openai-responses/-completions shape Foundry chat uses.
- [snippet_hermes_agent_cli_azure_detect](../../code_snippets/snippet_hermes_agent_cli_azure_detect.md) — Azure CLI detection during onboarding; relevance: the `az login`/`az account get-access-token` discovery path.
- [snippet_hermes_agent_core_anthropic_adapter_client](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_client.md) — Anthropic Messages adapter client; relevance: the wire contract for Claude deployments on Foundry.
- [snippet_hermes_agent_core_anthropic_adapter_endpoints](../../code_snippets/snippet_hermes_agent_core_anthropic_adapter_endpoints.md) — Anthropic adapter endpoint mapping; relevance: maps the `anthropic-messages` shape vs OpenAI shape distinction.
- [snippet_hermes_agent_core_codex_responses_adapter_request](../../code_snippets/snippet_hermes_agent_core_codex_responses_adapter_request.md) — openai-responses request adapter; relevance: the responses-vs-completions API selection Foundry applies per model family.
- [snippet_hermes_agent_core_agent_init_api_mode_resolution](../../code_snippets/snippet_hermes_agent_core_agent_init_api_mode_resolution.md) — resolves which API mode a model uses; relevance: GPT/o* → responses, MAI-DS-R1 → completions resolution logic.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: API-key vs Entra-ID token sourcing.
- [snippet_hermes_agent_tools_image_gen](../../code_snippets/snippet_hermes_agent_tools_image_gen.md) — image-generation tool; relevance: the `image_generate` capability MAI image models back.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registration registry; relevance: how a provider like Foundry is registered.
- [snippet_hermes_agent_core_error_classifier_provider_maps](../../code_snippets/snippet_hermes_agent_core_error_classifier_provider_maps.md) — per-provider error mapping; relevance: the troubleshooting surface (endpoint-missing / az-not-found / MAI-only) classification analog.

### oc_plugins_reference_microsoft_speech (9t · 10s · 11d · 4r)

- [OpenClaw](../../term_dictionary/term_openclaw.md) — the coding-agent gateway; relevance: the `@openclaw/microsoft-speech` plugin is first-party and bundled.
- [Text to Speech](../../term_dictionary/term_text_to_speech.md) — synthesizing audio from text; relevance: the plugin's sole capability — adds TTS provider support.
- [Speech to Text](../../term_dictionary/term_speech_to_text.md) — transcribing audio to text; relevance: the paired STT capability in the same Azure-speech family.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin adding a provider; relevance: it registers a TTS provider via the `speechProviders` contract.
- [Voice Mode](../../term_dictionary/term_voice_mode.md) — agent voice interaction mode; relevance: TTS is a building block of voice-mode output.
- [Voice Call](../../term_dictionary/term_voice_call.md) — phone/voice-channel agent calls; relevance: voice channels consume the TTS provider this plugin adds.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — streaming STT; relevance: the broader Azure-speech realtime audio context this plugin sits beside.
- [Multimodal](../../term_dictionary/term_multimodal.md) — handling multiple modalities; relevance: speech is the audio modality added to the agent's I/O.
- [Function Calling](../../term_dictionary/term_function_calling.md) — declared-capability invocation; relevance: `speechProviders` is one of the plugin contract surfaces alongside tools.

- [Hermes TTS Providers](../hermes_agent/hermes_tts_providers.md) — TTS provider catalog/config in Hermes; relevance: direct analog — the same `speechProviders`/TTS provider concept.
- [Hermes STT Transcription](../hermes_agent/hermes_stt_transcription.md) — speech-to-text in Hermes; relevance: the paired STT side of the speech provider family.
- [Hermes Voice Mode CLI](../hermes_agent/hermes_voice_mode_cli.md) — driving voice mode from the CLI; relevance: TTS output is consumed by voice mode.
- [Hermes Use Voice Mode Guide](../hermes_agent/hermes_use_voice_mode_guide.md) — end-user voice-mode walkthrough; relevance: shows where a TTS provider plugs into the voice experience.
- [Hermes Voice Gateway — Discord VC](../hermes_agent/hermes_voice_gateway_discord_vc.md) — voice gateway into a Discord voice channel; relevance: a concrete voice channel consuming a TTS provider.
- [Hermes Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — plugin surface taxonomy; relevance: defines the provider-surface vocabulary `speechProviders` belongs to.
- [Claude Code — Voice Dictation](../claude_code/cc_voice_dictation.md) — voice input in Claude Code; relevance: cross-tool framing of speech I/O in a coding agent.
- [pi_extensions_overview](../pi/pi_extensions_overview.md) — pi-agent extension model; relevance: cross-tool view of a bundled provider extension.
- [oc_plugins_reference_microsoft_foundry](oc_plugins_reference_microsoft_foundry.md) — (planned, this series) the other Microsoft plugin; relevance: same vendor (Microsoft/Azure), different contract (model/image vs speech).
- [oc_plugins_reference_overview](oc_plugins_reference_overview.md) — (planned, this series) card-schema hub; relevance: conceptual parent of this card.
- [oc_plugins_reference_memory](oc_plugins_reference_memory.md) — (planned, this series) sibling family card; relevance: peer `@openclaw/*` reference card in pl14.

- [repo_openclaw_extensions_voice_speech](../../../areas/code_repos/repo_openclaw_extensions_voice_speech.md) — the voice/speech extension layer; relevance: the home subsystem this TTS plugin belongs to.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin/extension host; relevance: registers the `speechProviders` contribution.
- [repo_openclaw_channels_voice_phone](../../../areas/code_repos/repo_openclaw_channels_voice_phone.md) — the voice/phone channel; relevance: a downstream consumer of the TTS provider.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the umbrella repo; relevance: ships microsoft-speech bundled.

- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — a concrete OpenClaw TTS provider (ElevenLabs); relevance: the peer `speechProviders` implementation pattern microsoft-speech follows.
- [snippet_openclaw_mlx_tts](../../code_snippets/snippet_openclaw_mlx_tts.md) — local MLX TTS provider; relevance: another TTS provider variant in the same speech layer.
- [snippet_openclaw_swabble_speech_pipeline](../../code_snippets/snippet_openclaw_swabble_speech_pipeline.md) — the speech pipeline; relevance: how a TTS provider's output flows through the speech pipeline.
- [snippet_openclaw_speech_deepgram_stt](../../code_snippets/snippet_openclaw_speech_deepgram_stt.md) — a STT provider (Deepgram); relevance: the paired STT side of the speech-provider family.
- [snippet_hermes_agent_tools_tts_routing](../../code_snippets/snippet_hermes_agent_tools_tts_routing.md) — TTS provider routing; relevance: how a registered TTS provider is selected at runtime.
- [snippet_hermes_agent_tools_transcription](../../code_snippets/snippet_hermes_agent_tools_transcription.md) — transcription tool; relevance: the STT counterpart in the sibling agent.
- [snippet_hermes_agent_tools_voice_mode](../../code_snippets/snippet_hermes_agent_tools_voice_mode.md) — voice-mode tool; relevance: the voice loop that consumes TTS output.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registration; relevance: how a speech provider is registered.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a provider-registration example; relevance: the generic provider-plugin registration shape `speechProviders` reuses.

### oc_plugins_reference_migration (10t · 11s · 11d · 5r)

- [OpenClaw](../../term_dictionary/term_openclaw.md) — the coding-agent gateway; relevance: migrate-claude/-hermes are first-party `@openclaw/migrate-*` plugins.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Anthropic's terminal coding agent; relevance: migrate-claude imports Claude Code instructions, MCP servers, and skills.
- [Claude](../../term_dictionary/term_claude.md) — Anthropic's model family; relevance: the Claude Code + Claude Desktop source environments migrate-claude reads.
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol server config; relevance: migrate-claude imports MCP servers into OpenClaw.
- [Skills](../../term_dictionary/term_skills.md) — packaged agent capabilities; relevance: both plugins import skills from the source agent.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the runtime wrapping a coding agent; relevance: migration moves config between agent harnesses (Claude Code / Hermes → OpenClaw).
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the agent class being migrated between; relevance: migration plugins move setups across coding agents.
- [OAuth Token](../../term_dictionary/term_oauth_token.md) — stored access credential; relevance: migrate-hermes imports supported credentials (tokens) safely.
- [Authentication](../../term_dictionary/term_authentication.md) — identity/credential handling; relevance: the "safe configuration" / "supported credentials" import surface.

- [Hermes Migrate from OpenClaw](../hermes_agent/hermes_migrate_from_openclaw.md) — the reverse migration (Hermes importing OpenClaw); relevance: the exact inverse of migrate-hermes — same config/memory/skill/credential surface.
- [Hermes MCP Config Reference](../hermes_agent/hermes_mcp_config_reference.md) — MCP server configuration format; relevance: the MCP-server config migrate-claude imports.
- [Hermes Work with Skills Guide](../hermes_agent/hermes_work_with_skills_guide.md) — authoring/using skills; relevance: the skills both migration plugins import.
- [Claude Code — .claude Directory](../claude_code/cc_dot_claude_directory.md) — the Claude Code config/instructions directory; relevance: the source layout migrate-claude reads (instructions, MCP, skills).
- [Claude Code — Configure Your Environment](../claude_code/cc_configure_your_environment.md) — Claude Code configuration; relevance: the "instructions + safe configuration" migrate-claude imports.
- [Claude Code — Plugins Overview](../claude_code/cc_plugins_overview.md) — Claude Code plugin/extension model; relevance: cross-tool framing of what gets migrated.
- [pi_provider_auth](../pi/pi_provider_auth.md) — credential/auth handling for providers; relevance: cross-tool framing of importing supported credentials safely.
- [oc_plugins_reference_overview](oc_plugins_reference_overview.md) — (planned, this series) card-schema hub; relevance: the conceptual parent of this card; defines `migrationProviders`.
- [oc_plugins_reference_memory](oc_plugins_reference_memory.md) — (planned, this series) memory family card; relevance: migrate-hermes imports memories — a consumer of the memory subsystem.
- [oc_plugins_reference_microsoft_foundry](oc_plugins_reference_microsoft_foundry.md) — (planned, this series) sibling card; relevance: peer `@openclaw/*` reference card in pl14.
- [oc_plugins_reference_microsoft_speech](oc_plugins_reference_microsoft_speech.md) — (planned, this series) sibling card; relevance: peer family card sharing the Distribution/Surface schema.

- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin/extension host; relevance: migration plugins register the `migrationProviders` contract here.
- [repo_openclaw_skills](../../../areas/code_repos/repo_openclaw_skills.md) — the skills subsystem; relevance: skills are an import target.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — the sessions subsystem; relevance: imported config/memories seed agent sessions.
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — Hermes agent core; relevance: the Hermes side migrate-hermes reads config/memories/credentials from.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the umbrella repo; relevance: ships migrate-claude/-hermes bundled.

- [snippet_openclaw_wizard_migration_import](../../code_snippets/snippet_openclaw_wizard_migration_import.md) — the onboarding-wizard migration import path; relevance: the exact import flow migrate-claude/-hermes drive.
- [snippet_hermes_agent_cli_codex_migrate](../../code_snippets/snippet_hermes_agent_cli_codex_migrate.md) — a CLI migration command; relevance: a peer migration importer in the sibling agent.
- [snippet_hermes_agent_skills_vs_plugins](../../code_snippets/snippet_hermes_agent_skills_vs_plugins.md) — skills-vs-plugins distinction; relevance: clarifies the skills both migration plugins import.
- [snippet_hermes_agent_cli_mcp_config](../../code_snippets/snippet_hermes_agent_cli_mcp_config.md) — MCP config handling; relevance: the MCP-server config migrate-claude imports.
- [snippet_hermes_agent_tools_mcp_oauth_manager](../../code_snippets/snippet_hermes_agent_tools_mcp_oauth_manager.md) — MCP OAuth credential manager; relevance: how imported MCP credentials are handled safely.
- [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential source resolution; relevance: the "supported credentials" migrate-hermes imports.
- [snippet_hermes_agent_cli_auth_login_logout](../../code_snippets/snippet_hermes_agent_cli_auth_login_logout.md) — auth login/logout; relevance: re-establishing imported credentials post-migration.
- [snippet_openclaw_agents_auth_profiles_oauth_portability](../../code_snippets/snippet_openclaw_agents_auth_profiles_oauth_portability.md) — OAuth credential portability across profiles; relevance: the "safe configuration"/portable-credential migration surface.
- [snippet_hermes_agent_acp_auth](../../code_snippets/snippet_hermes_agent_acp_auth.md) — ACP auth; relevance: cross-agent auth handoff analog during migration.
- [snippet_hermes_agent_tools_memory](../../code_snippets/snippet_hermes_agent_tools_memory.md) — memory tool surface; relevance: migrate-hermes imports memories.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — the tool/capability registry; relevance: where imported tools/skills land.

### oc_plugins_reference_overview (10t · 10s · 12d · 3r)

- [OpenClaw](../../term_dictionary/term_openclaw.md) — the coding-agent gateway; relevance: every card describes an `@openclaw/<name>` package.
- [Plugin SDK](../../term_dictionary/term_plugin_sdk.md) — the SDK for authoring OpenClaw plugins; relevance: the package + install-route half of the card schema.
- [Plugin Manifest](../../term_dictionary/term_plugin_manifest.md) — the plugin's declared metadata/contract; relevance: the declared contract surface half of the card schema.
- [Provider Plugin](../../term_dictionary/term_provider_plugin.md) — a plugin adding a provider; relevance: one of the enumerated card types (`providers`).
- [Function Calling](../../term_dictionary/term_function_calling.md) — LLM tool invocation; relevance: the `tools` contract surface across cards.
- [Skills](../../term_dictionary/term_skills.md) — packaged agent capabilities; relevance: the `skills` contract surface (memory-wiki, migrations).
- [Text to Speech](../../term_dictionary/term_text_to_speech.md) — speech synthesis capability; relevance: the `speechProviders` contract surface (microsoft-speech).
- [Model Catalog](../../term_dictionary/term_model_catalog.md) — selectable models/deployments; relevance: the `providers` / `imageGenerationProviders` surfaces (Foundry).
- [MCP](../../term_dictionary/term_mcp.md) — Model Context Protocol; relevance: a primary way plugin capabilities reach the agent.
- [ACP — Agent Client Protocol](../../term_dictionary/term_acp_agent_client_protocol.md) — the agent-client transport; relevance: how plugin-provided capabilities are surfaced to clients.

- [Hermes Plugin Types & Surfaces](../hermes_agent/hermes_plugin_types_surfaces.md) — the plugin contract-surface taxonomy; relevance: the closest existing analog of this overview's contract-surface enumeration.
- [Hermes Plugins System](../hermes_agent/hermes_plugins_system.md) — the plugin system overview; relevance: cross-ecosystem framing of package + contract-surface model.
- [Hermes Built-in Plugins](../hermes_agent/hermes_built_in_plugins.md) — the bundled-plugin set; relevance: explains the "included in OpenClaw" distribution most pl14 cards declare.
- [Claude Code — Plugin Components](../claude_code/cc_plugin_components.md) — coding-agent plugin component model; relevance: cross-tool view of how a plugin declares its capabilities.
- [Claude Code — Plugins Overview](../claude_code/cc_plugins_overview.md) — Claude Code plugin/extension overview; relevance: a sibling-tool plugin-schema reference.
- [pi_extensions_overview](../pi/pi_extensions_overview.md) — pi-agent extension model; relevance: a third coding-agent's plugin/extension framing for triangulation.
- [band_sdk_reference_adapters](../band/band_sdk_reference_adapters.md) — adapter SDK reference; relevance: the adapter/extension-surface pattern that mirrors contract surfaces.
- [oc_plugins_reference_memory](oc_plugins_reference_memory.md) — (planned, this series) memory family card; relevance: a child card this overview abstracts.
- [oc_plugins_reference_microsoft_foundry](oc_plugins_reference_microsoft_foundry.md) — (planned, this series) Foundry card; relevance: a child card (`providers`/`imageGenerationProviders`).
- [oc_plugins_reference_microsoft_speech](oc_plugins_reference_microsoft_speech.md) — (planned, this series) speech card; relevance: a child card (`speechProviders`).
- [oc_plugins_reference_migration](oc_plugins_reference_migration.md) — (planned, this series) migration card; relevance: a child card (`migrationProviders`).

- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — the plugin/extension framework; relevance: implements the contract-surface registration this schema describes.
- [repo_openclaw](../../../areas/code_repos/repo_openclaw.md) — the umbrella repo; relevance: bundles the plugins these cards document.
- [repo_openclaw_extensions_llm_providers](../../../areas/code_repos/repo_openclaw_extensions_llm_providers.md) — the provider extension layer; relevance: a concrete contract-surface family (`providers`).

- [snippet_openclaw_plugin_lifecycle](../../code_snippets/snippet_openclaw_plugin_lifecycle.md) — the plugin load/lifecycle; relevance: how a card's package + install route becomes a running plugin.
- [snippet_openclaw_plugin_sdk_entries](../../code_snippets/snippet_openclaw_plugin_sdk_entries.md) — the plugin SDK entry points; relevance: the package + entry-surface half of the schema.
- [snippet_openclaw_skills_tool_descriptor_contract](../../code_snippets/snippet_openclaw_skills_tool_descriptor_contract.md) — the tool/skill descriptor contract; relevance: the `tools`/`skills` contract surfaces.
- [snippet_hermes_agent_plugins_manifest_schema](../../code_snippets/snippet_hermes_agent_plugins_manifest_schema.md) — the plugin manifest schema; relevance: the declared-contract half of the card schema.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: cross-ecosystem framing of plugin surfaces.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registration; relevance: the `providers`/`imageGenerationProviders` surface registration.
- [snippet_openclaw_memory_runtime_re_exports](../../code_snippets/snippet_openclaw_memory_runtime_re_exports.md) — re-exports as a plugin's public surface; relevance: how a plugin exposes its contract entries.
- [snippet_openclaw_speech_elevenlabs_tts](../../code_snippets/snippet_openclaw_speech_elevenlabs_tts.md) — a `speechProviders` implementation; relevance: a concrete instance of an enumerated contract surface.
- [snippet_openclaw_provider_anthropic](../../code_snippets/snippet_openclaw_provider_anthropic.md) — a `providers` implementation; relevance: a concrete instance of the providers contract surface.
- [snippet_hermes_agent_providers_init_dispatch](../../code_snippets/snippet_hermes_agent_providers_init_dispatch.md) — provider init/dispatch; relevance: how registered contract surfaces are dispatched at runtime.

`term_vector_search`, `term_obsidian`, `term_long_term_memory`, `term_semantic_search`, `term_azure_openai`,
`term_amazon_bedrock`, `term_image_generation`, `term_reasoning_model`, `term_speech_synthesis`, `term_tts`,
`term_voice`, `term_lancedb`, `term_azure`, `term_entra_id`, `term_azure_ai_foundry`, `term_migration`,
`term_wiki`. (`entry_openclaw_docs` is created as master pre-step W1 — cited as planned until built.)

## Undigested Terms Plan

Per master: OpenClaw vocabulary is digested as `oc_` doc concept/reference notes (their home is the plugin
page), NOT as new `term_dictionary` entries; the only `term_dictionary` interaction is **linking existing**
terms. **pl14 expects 0 new `term_dictionary` captures.**

| Term (appears in source) | Disposition |
|---|---|
| memory-core / memory-lancedb / memory-wiki (plugin names) | → note 1 (`oc_plugins_reference_memory`); plugin names documented as reference cards, not promoted to term notes. |
| LanceDB | Link existing `term_vector_database` (LanceDB is a vector DB); do NOT create `term_lancedb` (single-product, doc-page-owned). |
| auto-recall / auto-capture / vector search | Link `term_vector_database`, `term_dense_retrieval`, `term_information_retrieval`, `term_agentic_memory`; concepts owned by the memory note + existing terms. |
| Obsidian / wiki compiler / knowledge vault | Link existing `term_knowledge_base`, `term_zettelkasten`; `term_obsidian` MISSING but Obsidian is a single product — describe in-note, link `term_knowledge_base` (no new term). |
| microsoft / microsoft-foundry / microsoft-speech (plugin/provider names) | → notes 2/3; provider names documented as config, link `term_provider_plugin` / `term_llm` / `term_text_to_speech`. |
| Microsoft Foundry / Azure AI Foundry / Entra ID / `az login` | Documented in-note (note 2) as provider config; link `term_oauth`/`term_authentication`. Single-vendor product names — not promoted to terms. |
| openai-responses / openai-completions / anthropic-messages (API shapes) | Link `term_provider_plugin`, `term_function_calling`, `term_claude`; API-shape names documented in-note (note 2). |
| MAI-DS-R1 / MAI-Image-2.5 / canonicalModelId | Documented in-note (note 2) as model config; link `term_model_catalog`, `term_chain_of_thought`. |
| contract surfaces: tools / skills / speechProviders / providers / imageGenerationProviders / migrationProviders | → note 5 (`oc_plugins_reference_overview`); the contract-surface vocabulary is digested as the schema concept; link `term_plugin_sdk`, `term_plugin_manifest`, `term_function_calling`, `term_skills`, `term_text_to_speech`. |

**New-term candidates:** none. No genuinely cross-cutting, vault-reusable term without an existing note OR a
doc-page home appears in these 7 pages. (Augment Step 2d re-scans to confirm.)

## Term-Note Authoring Requirements

**N/A (0 new terms).** pl14 authors zero `term_dictionary` notes (inherited from master: OpenClaw vocab →
`oc_` doc notes; existing terms linked only). If augment Step 2d surfaces a genuine cross-cutting reusable
term with no existing note and no doc-page home, capture it via `/tessellum-capture-term-note` + add to the
best-fit `acronym_glossary_*.md` (the agentic/LLM glossary) per master W5 — not expected here.

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (5 notes, P3). All gates must PASS before commit.

| Gate | Check | Tool / Method |
|---|---|---|
| G1 | Format (YAML field order + forbidden fields; H1/`## Overview`/`## Related Notes`/`## References`/footer) | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding (every claim traceable to the source page; no invented config) | diff each note vs `inbox/openclaw_docs/plugins/reference/<page>.md` |
| G3 | Density + Coverage (≤400 lines / ≤2,500 words / ≤6 code; one BB; every mapped section present) | word/line/code count + Section Coverage Map |
| G4 | Cross-Reference (≥6 relevance-selected term links + repos/siblings, each with a relevance statement) | inspect `## Related Notes`; count + relevance per link |
| G5 | Ghost-reference detect + redirect (no link to a non-existent note) | `/tessellum-fix-ghost-references`; DB existence per target |
| G6 | Broken-link fix (correct relative paths) | `/tessellum-fix-broken-links` |
| G7 | Discoverability (≥1 inbound link from OUTSIDE `documentation/openclaw/`) | `entry_openclaw_docs.md` rows + repo/term inlinks |
| G8 | In-degree ≥1 per new note (anti-island) | `note_links` query post-reindex |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_plugins_reference_memory oc_plugins_reference_microsoft_foundry oc_plugins_reference_microsoft_speech oc_plugins_reference_migration oc_plugins_reference_overview"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n format OK"
  # required sections
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # density
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
done

# YAML frontmatter sweep
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost / G8 in-degree (post-reindex)
for n in ${=NOTES}; do
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | ~Code | Within caps (≤2500w / ≤400L / ≤6 code)? |
|---|---|---|---:|---:|---|
| 1 | oc_plugins_reference_memory | model | 500 | 0 | ✅ |
| 2 | oc_plugins_reference_microsoft_foundry | procedure | 650 | 1 | ✅ |
| 3 | oc_plugins_reference_microsoft_speech | model | 350 | 0 | ✅ |
| 4 | oc_plugins_reference_migration | model | 450 | 0 | ✅ |
| 5 | oc_plugins_reference_overview | concept | 450 | 0 | ✅ |

No note approaches caps. The single source code fence (Foundry json5 image-config) lands in note 2 only.
Notes 1/3/4/5 are well above the usefulness floor only because of consolidation + cross-reference context —
the raw source stubs (43–67w) are intentionally NOT minted as standalone notes (see Consolidation Decisions).

## Entry Point Decision (inherited from master)

Contributes **5 rows** to `entry_openclaw_docs.md` (created as the master W1 pre-step before any sub-plan
executes) under the **Plugins → Reference (pl14)** cluster — one row per note (memory family, Microsoft
Foundry, Microsoft speech, migration family, reference-card overview). Each note also receives its
entry-point back-link at finalization (satisfies G7/G8). No standalone entry point for this sub-plan
(< master's per-sub-plan threshold; rolls into the shared `entry_openclaw_docs.md`).

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; G7/G8):

|---|---|
| oc_plugins_reference_memory | `entry_openclaw_docs` (planned, W1) · `repo_openclaw_memory` · `term_agentic_memory` · `term_vector_database` |
| oc_plugins_reference_microsoft_foundry | `entry_openclaw_docs` (planned) · `repo_openclaw_extensions_llm_providers` · `term_provider_plugin` · `term_claude` |
| oc_plugins_reference_microsoft_speech | `entry_openclaw_docs` (planned) · `repo_openclaw_extensions_voice_speech` · `term_text_to_speech` |
| oc_plugins_reference_migration | `entry_openclaw_docs` (planned) · `repo_openclaw_extensions` · `term_claude_code` · `entry_claude_code_docs` |
| oc_plugins_reference_overview | `entry_openclaw_docs` (planned) · `repo_openclaw_extensions` · `term_plugin_sdk` · all 4 sibling oc cards (reciprocal) |

Every new note gets ≥1 inbound from outside `documentation/openclaw/` (`entry_openclaw_docs` guarantees
the floor; repo/term inlinks add depth). Reciprocal sibling links among the 5 notes provide intra-series
in-degree.

## Pacing Rules (inherited from master)

One execution phase, 5 notes. Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest in the
script. Re-read each source page before authoring; reproduce the one config snippet (Foundry json5)
verbatim. One BB per note. `git pull --rebase --autostash` first; commit + push after the phase; no Claude
co-author trailer. Reindex incrementally; verify `note_links` + 0 broken links + in-degree ≥1 before commit.

## Pipeline Status

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref-augment: per-note mapping LOCKED at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9 CP pass)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Skill**: `/tessellum-augment-digestion-plan` (xref-augment pass — per-note Related Notes mapping at raised
floors). Re-read all 7 source pages from `inbox/openclaw_docs/plugins/reference/` before selecting links;
`term_stylometry`, `term_ssrf_guard` surfaced by BM25 but irrelevant to plugin reference cards).

**What was LOCKED**: the prior `## Candidate Cross-References` section was replaced with
`## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)`. Standard applied:

**Per-note locked counts** (deterministically re-counted from the file):

| Note | Terms | Snippets | Docs (existing/planned) | Repos | Floors met |
|---|---:|---:|---|---:|---|
| oc_plugins_reference_memory | 10 | 11 | 11 (7/4) | 4 | ✅ |
| oc_plugins_reference_microsoft_foundry | 10 | 11 | 11 (8/3) | 4 | ✅ |
| oc_plugins_reference_microsoft_speech | 9 | 10 | 11 (8/3) | 4 | ✅ |
| oc_plugins_reference_migration | 10 | 11 | 11 (7/4) | 5 | ✅ |
| oc_plugins_reference_overview | 10 | 10 | 12 (8/4) | 3 | ✅ |


**Corpora leveraged**: the rich coding-agent doc corpora made the ≥10-doc floor easy with ≥5 existing each —
`hermes_agent/hermes_*` (memory-provider catalog/plugin/honcho, context-engine, plugin-types-surfaces,
azure-foundry-setup + entra-id, model/image-gen/tts/stt provider plugins, migrate-from-openclaw, mcp-config,
work-with-skills), `claude_code/cc_*` (cc_microsoft_foundry — the exact cross-tool Foundry peer —
cc_plugin_components, cc_plugins_overview, cc_sdk_plugins, cc_dot_claude_directory, cc_voice_dictation),
`pi/pi_*` (extensions-overview, custom-provider-registration, provider-auth), `band/band_*`
(sdk_reference_adapters). Snippets drew on the openclaw memory/provider/speech/plugin and

**New-term candidates**: **none.** Re-scan (augment Step 2d) of all 7 pages confirms every OpenClaw-specific
token (memory-core/-lancedb/-wiki, microsoft-foundry/-speech, migrate-claude/-hermes, MAI-DS-R1,
MAI-Image-2.5, `canonicalModelId`, openai-responses/-completions, anthropic-messages, speechProviders /
imageGenerationProviders / migrationProviders, Entra ID, `az login`) is either (a) a single-vendor/product
name owned by its `oc_*` doc page, or (b) covered by an existing linked term. **Best-fit glossary** had a
candidate been found: `0_entry_points/acronym_glossary_gen_ai_dev.md` (the agentic/LLM glossary, per master
W5). pl14 authors **0 new `term_dictionary` notes** (matches the master Undigested-Terms ownership decision).

**Issues**: none blocking. (Note: `term_image_generation`, `term_vector_search`, `term_obsidian`,
`term_speech_synthesis`, `term_voice`, `term_lancedb`, `term_azure_ai_foundry`, `term_entra_id` are confirmed
absent from the DB and were intentionally NOT cited — substituted with existing equivalents
`term_generative_model`/`term_diffusion_model`, `term_information_retrieval`/`term_similarity_search`,
`term_knowledge_base`/`term_zettelkasten`, `term_text_to_speech`, `term_vector_database`, `term_model_catalog`,
`term_oauth`/`term_authentication` respectively.)

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only 9-checkpoint review run after the xref-augment lock.

| CP | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 9-GATE table present per execution phase (G1–G8 incl. G5 ghost, G6 broken, G7/G8 discoverability) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 format, G2 grounding, G3 density+coverage, G4 cross-ref, G5 ghost-detect+redirect, G6 broken-link-fix, G7 discoverability, G8 in-degree≥1. Single phase (5 notes). |
| CP3 | Entry point update specified + inherited | **PASS** | `## Entry Point Decision` contributes 5 rows to `entry_openclaw_docs.md` (master W1 pre-step) under Plugins→Reference (pl14); each note gets its entry-point back-link at finalization (G7/G8). No standalone entry point (below per-sub-plan threshold). |
| CP4 | Plan size manageable (≤30 or split) | **PASS** | 5 planned notes (well under 30); density-driven consolidation 7 pages → 5 notes documented in Split/Consolidation Decisions. |
| CP5 | Note format aligned + DERIVED from existing target-dir notes | **PASS** | Format inherited verbatim from master Format Definition, derived from existing `claude_code/cc_*` + `pi/pi_*` corpora (same source type); YAML field order + `## Overview`/`## Related Notes`/`## References`/footer + forbidden-field list match. Target dir convention confirmed against existing `hermes_*`/`cc_*`/`pi_*`/`band_*` notes used as cross-refs. |
| CP6 | Borderline density → split promoted | **PASS** | Density Re-Assessment: all 5 notes 350–650w / 0–1 code, far below ≤2,500w/≤400L/≤6-code caps; no borderline note. Foundry (650w, 1 code) is single-BB procedure, no split warranted. |
| CP7 | Source word counts measured (not guessed) | **PASS** | Re-read all 7 mirror pages 2026-06-21; measured matches plan Source table (memory-core 43w, memory-lancedb 63w, memory-wiki 61w, microsoft 43w, microsoft-foundry 530w/6 H2/1 code, migrate-claude 67w, migrate-hermes 57w). microsoft-foundry verbatim json5 image-config block confirmed (must-preserve, note 2). |
| CP8 | Undigested Terms Plan + Term-Note Authoring Requirements + dedup/collision audit | **PASS** | `## Undigested Terms Plan` present with per-token disposition (all → `oc_*` doc pages or link existing); New-term candidates: none; `## Term-Note Authoring Requirements` present as N/A (0 new terms) with master W5 fallback path named. |
| CP8f | Term-slug specificity + all-notes (term AND doc) collision audit | **PASS** | 0 new term slugs ⇒ no specificity renames needed. Doc-note collision audit: 5 planned `oc_plugins_reference_*` slugs searched against `documentation/` + `term_dictionary/`; none duplicate an existing note (the OpenClaw plugin-reference cards are new; vector/memory/TTS/migration concepts are LINKED to existing terms, not recreated — per master Dedup Policy). |
| CP9 | Discoverability — inbound links executed (G8), no graph islands | **PASS** | `## Inlinks (existing → new notes)` maps every new note to ≥1 outside-folder inbound source (`entry_openclaw_docs` floor + repo/term/`entry_claude_code_docs` depth); G8 in-degree≥1 in the gate table; reciprocal sibling links among the 5 notes add intra-series in-degree. |

**RESULT: 9/9 checkpoints PASS → READY FOR EXECUTION.** Plan status advanced `pending → ready`.
