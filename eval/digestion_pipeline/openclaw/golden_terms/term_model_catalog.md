---
tags:
  - resource
  - terminology
  - openclaw
  - model-catalog
  - llm-infrastructure
  - model-registry
keywords:
  - Model Catalog
  - model registry
  - manifest-planner
  - persisted-models.json
  - PI SDK ModelRegistry
  - cross-plugin model catalog
  - provider-model dedupe
topics:
  - LLM infrastructure
  - Model catalog
  - OpenClaw architecture
language: markdown
date of note: 2026-05-10
status: active
building_block: concept
related_wiki: https://github.com/openclaw/openclaw/blob/main/src/agents/model-catalog.ts
access_control_group: ["general"]
---

# Model Catalog

## Definition

A **model catalog** is an in-process registry of (provider, model-id) entries — each carrying metadata such as context-window size, input-modality flags, reasoning capability, and provider-specific compatibility overrides — that an LLM-agent runtime consults when it has to bind a user-specified model id to an actual inference endpoint. Industry treatment distinguishes three closely related artefacts: a **model garden** is a curated *discovery* surface (e.g., Vertex AI Model Garden's ~200 enterprise-ready foundation models for browsing and selection); a **model registry** is a *lifecycle* repository for trained models, their versions, and deployment metadata (MLflow, Vertex AI Model Registry, JFrog); and a **model catalog** is the *runtime lookup* table that an SDK, gateway, or proxy uses to resolve a name to invocation parameters (LiteLLM's 2,600+ models across 140+ providers, llmware's `ModelCatalog` class, OpenRouter's `/models` endpoint).

OpenClaw's **`loadModelCatalog`** (`src/agents/model-catalog.ts`) is the runtime-lookup flavour. It assembles entries from three sources in priority order: the PI SDK `ModelRegistry` reading on-disk `models.json` populated by built-in provider plugins, the manifest-planner rows derived from plugin metadata snapshots eligible for the control plane, and `buildConfiguredModelCatalog` materializing user-configured providers from `OpenClawConfig`. The resulting list is deduped on `(normalizedProvider, lowercaseId)`, sorted, and memoised in a module-level promise — with a separate side-effect-free read-only branch so the gateway's `models.list` RPC never blocks on plugin I/O.

## Context

Model catalogs sit between the human-facing model name (`claude-opus-4`, `gpt-4o`) and the wire-level provider call. LiteLLM's catalog is consulted at proxy startup to expose `/v1/models` and to look up per-token pricing and capability flags before each request. OpenRouter publishes its catalog as a public JSON endpoint that aggregator clients poll for context-window and pricing. Vertex AI Model Garden plays the discovery role, after which selected models are registered into Vertex AI Model Registry for managed-lifecycle tracking. Anthropic's models endpoint plays a similar runtime role for its own SDKs.

In OpenClaw, the catalog is the substrate that the **Subagent** spawn machinery, the model-failover ladder, the context-window guard, and the vision/document capability probes (`modelSupportsVision`, `modelSupportsDocument`) all consult. Every agent turn that has to pick or validate a model — context-window check before append, failover decision after a 429, ACP-translator capability negotiation — looks the candidate up in the catalog rather than hard-coding provider capabilities. Plugins extend the catalog by emitting manifest rows; users override it via `OpenClawConfig.providers[].models`; and the runtime cross-checks both against what the PI SDK can actually discover on disk.

## Key Characteristics

- **Three-source assembler**: priority-ordered merge of (1) PI SDK `ModelRegistry` over `models.json`, (2) manifest-planner rows from eligible plugin metadata snapshots, (3) `OpenClawConfig`-derived configured providers
- **Three-tier context-window fallback**: per-entry `contextWindow` → provider-level `contextWindow` → `PI_CUSTOM_MODEL_DEFAULT_CONTEXT_WINDOW` (128_000)
- **Composite `(provider, id)` dedupe key**: `catalogEntryDedupeKey` normalises both halves before comparison; downstream consumers see at most one entry per logical model
- **Capability probes**: `modelSupportsVision` / `modelSupportsDocument` are pure functions over a catalog entry's `input: ModelInputType[]` array (`"text" | "image" | "audio" | "video" | "document"`) — agents call these instead of maintaining per-provider tables
- **Non-poisoning cache for live discovery**: a transient `import()` failure (e.g., during `pnpm install`) is caught so the module-level promise is never resolved to a rejection; the next call retries
- **Normalized schemas**: provider/model/alias/discovery/suppression sub-records are validated by `src/model-catalog/normalize.ts` before any merge; unknown values silently coerce to `undefined` so optional fields stay absent rather than null
- **Merge-key conflict detection**: when two plugins emit the same `(provider, id)` row, both are *dropped* (not first-wins) and recorded in `ManifestModelCatalogConflict` so the caller can surface the collision
- **Read-only branch**: gateway `models.list` calls take a side-effect-free path that parses `models.json` directly, bypassing PI SDK and provider-plugin augmentation, so the RPC cannot block on plugin I/O

## Related Terms


### Related Code Snippets

- **[snippet_openclaw_agents_model_catalog](../code_snippets/snippet_openclaw_agents_model_catalog.md)**: three-source catalog assembler with plugin discovery and capability probes
- **[snippet_openclaw_model_catalog_normalize_schemas](../code_snippets/snippet_openclaw_model_catalog_normalize_schemas.md)**: provider/model/alias schema normalizer toolkit (L1-L260)
- **[snippet_openclaw_model_catalog_normalize_discovery](../code_snippets/snippet_openclaw_model_catalog_normalize_discovery.md)**: discovery + suppression + denormalization assembler (L260-L511)
- **[snippet_openclaw_model_catalog_manifest_planner](../code_snippets/snippet_openclaw_model_catalog_manifest_planner.md)**: per-plugin entry assembler with merge-key conflict detection
- **[Provider Routing](../term_dictionary/term_provider_routing.md)**: OpenRouter sub-provider selection whose `only`/`ignore`/`order` lists whitelist against the aggregated provider/model catalog
- **[OpenClaw — Model Provider Directory](../documentation/openclaw/oc_provider_directory.md)** — This note is the conceptual index of the OpenClaw **provider directory**: the catalog of LLM, transcription, and media-generation model backends OpenClaw can…

## References

- [OpenClaw — src/agents/model-catalog.ts](https://github.com/openclaw/openclaw/blob/main/src/agents/model-catalog.ts) — primary source (Class 2: upstream org docs)
- [LiteLLM Providers & Models catalog](https://models.litellm.ai/) — 2,600+ models across 140+ providers, the canonical industry exemplar (Class 2)
- [LiteLLM Model Discovery docs](https://docs.litellm.ai/docs/proxy/model_discovery) — how a proxy exposes its catalog over `/v1/models` (Class 2)
- [Vertex AI Model Registry — Introduction](https://cloud.google.com/vertex-ai/docs/model-registry/introduction) — contrasting *registry* concept (Class 2)
- [Vertex AI — Wikipedia](https://en.wikipedia.org/wiki/Vertex_AI) — Model Garden vs Model Registry framing (Class 1: Wikipedia)
- [llmware ModelCatalog](https://llmware-ai.github.io/llmware/components/model_catalog) — sibling open-source `ModelCatalog` design (Class 2)
- [OpenRouter — Models](https://openrouter.ai/docs/overview/models) — aggregator catalog endpoint (Class 2)
