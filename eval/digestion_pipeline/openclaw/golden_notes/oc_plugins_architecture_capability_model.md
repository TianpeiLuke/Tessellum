---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - capability_model
keywords:
  - openclaw plugin capability model
  - native plugin capability types
  - registerProvider registerSpeechProvider
  - plugin shapes plain hybrid hook-only non-capability
  - legacy hook-only plugin before_agent_start
  - plugin compatibility signals doctor inspect
  - plugin architecture four layers
  - plugin metadata snapshot lookup table
topics:
  - OpenClaw
  - Plugin Capability Model
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/architecture
access_control_group: ["general"]
---

# OpenClaw — Plugin Capability Model and Architecture Overview

## Overview

This note captures the **public native-plugin capability model** of the OpenClaw plugin system and the high-level four-layer architecture overview, mirroring the first half of the `plugins/architecture` source page. It covers the capability-type table (the registration method each capability uses and example plugins), the external-compatibility stance for adopting capability registration, the four plugin **shapes** OpenClaw classifies every loaded plugin into, the legacy hook-only path, the `openclaw doctor` / `plugins inspect` compatibility signals, and the four-layer architecture overview (discovery → enablement → runtime loading → surface consumption) plus the metadata snapshot and activation-planning control plane. The capability **ownership** model, contracts/enforcement, the execution model, and the export boundary are the subject of the sibling note `oc_plugins_architecture_ownership_contracts` and are not repeated here.

## Public capability model

Capabilities are the public **native plugin** model inside OpenClaw. Every native OpenClaw plugin registers against one or more capability types via a typed `api.register*` method. The capability table from the source page (capability, registration method, and example plugins) is:

| Capability | Registration method | Example plugins |
| --- | --- | --- |
| Text inference | `api.registerProvider(...)` | `openai`, `anthropic` |
| CLI inference backend | `api.registerCliBackend(...)` | `openai`, `anthropic` |
| Embeddings | `api.registerEmbeddingProvider(...)` | Provider-owned vector plugins |
| Speech | `api.registerSpeechProvider(...)` | `elevenlabs`, `microsoft` |
| Realtime transcription | `api.registerRealtimeTranscriptionProvider(...)` | `openai` |
| Realtime voice | `api.registerRealtimeVoiceProvider(...)` | `openai` |
| Media understanding | `api.registerMediaUnderstandingProvider(...)` | `openai`, `google` |
| Transcripts source | `api.registerTranscriptSourceProvider(...)` | `discord` |
| Image generation | `api.registerImageGenerationProvider(...)` | `openai`, `google`, `fal`, `minimax` |
| Music generation | `api.registerMusicGenerationProvider(...)` | `google`, `minimax` |
| Video generation | `api.registerVideoGenerationProvider(...)` | `qwen` |
| Web fetch | `api.registerWebFetchProvider(...)` | `firecrawl` |
| Web search | `api.registerWebSearchProvider(...)` | `google` |
| Channel / messaging | `api.registerChannel(...)` | `msteams`, `matrix` |
| Gateway discovery | `api.registerGatewayDiscoveryService(...)` | `bonjour` |

A plugin that registers **zero capabilities** but provides hooks, tools, discovery services, or background services is a **legacy hook-only** plugin, and that pattern is still fully supported.

### External compatibility stance

The capability model is landed in core and used by bundled/native plugins today, but external plugin compatibility still needs a tighter bar than "it is exported, therefore it is frozen." The source page gives three situation-specific guidances:

| Plugin situation | Guidance |
| --- | --- |
| Existing external plugins | Keep hook-based integrations working; this is the compatibility baseline. |
| New bundled/native plugins | Prefer explicit capability registration over vendor-specific reach-ins or new hook-only designs. |
| External plugins adopting capability registration | Allowed, but treat capability-specific helper surfaces as evolving unless docs mark them stable. |

Capability registration is the intended direction; legacy hooks remain the safest no-breakage path for external plugins during the transition. Exported helper subpaths are not all equal — the doc says to prefer narrow documented contracts over incidental helper exports.

### Plugin shapes

OpenClaw classifies every loaded plugin into a **shape** based on its actual registration behavior (not just static metadata). The four shapes are:

- **plain-capability** — registers exactly one capability type (for example a provider-only plugin like `mistral`).
- **hybrid-capability** — registers multiple capability types (for example `openai` owns text inference, speech, media understanding, and image generation).
- **hook-only** — registers only hooks (typed or custom), with no capabilities, tools, commands, or services.
- **non-capability** — registers tools, commands, services, or routes but no capabilities.

Run `openclaw plugins inspect <id>` to see a plugin's shape and capability breakdown.

### Legacy hooks

The `before_agent_start` hook remains supported as a compatibility path for hook-only plugins, because legacy real-world plugins still depend on it. The documented direction is: keep it working, document it as legacy, prefer `before_model_resolve` for model/provider override work, prefer `before_prompt_build` for prompt mutation work, and remove it only after real usage drops and fixture coverage proves migration safety.

### Compatibility signals

When you run `openclaw doctor` or `openclaw plugins inspect <id>`, you may see one of these labels:

| Signal | Meaning |
| --- | --- |
| **config valid** | Config parses fine and plugins resolve |
| **compatibility advisory** | Plugin uses a supported-but-older pattern (e.g. `hook-only`) |
| **legacy warning** | Plugin uses `before_agent_start`, which is deprecated |
| **hard error** | Config is invalid or plugin failed to load |

Neither `hook-only` nor `before_agent_start` breaks a plugin today: `hook-only` is advisory, and `before_agent_start` only triggers a warning. These signals also appear in `openclaw status --all` and `openclaw plugins doctor`.

## Architecture overview

OpenClaw's plugin system has **four layers**, run as a startup sequence:

1. **Manifest + discovery** — OpenClaw finds candidate plugins from configured paths, workspace roots, global plugin roots, and bundled plugins. Discovery reads native `openclaw.plugin.json` manifests plus supported bundle manifests first.
2. **Enablement + validation** — core decides whether a discovered plugin is enabled, disabled, blocked, or selected for an exclusive slot such as memory.
3. **Runtime loading** — native OpenClaw plugins are loaded in-process and register capabilities into a central registry. Packaged JavaScript loads through native `require`; third-party local source TypeScript is the emergency Jiti fallback. Compatible bundles are normalized into registry records without importing runtime code.
4. **Surface consumption** — the rest of OpenClaw reads the registry to expose tools, channels, provider setup, hooks, HTTP routes, CLI commands, and services.

For plugin CLI specifically, root command discovery is split into two phases: parse-time metadata comes from `registerCli(..., { descriptors: [...] })`, and the real plugin CLI module can stay lazy and register on first invocation. That keeps plugin-owned CLI code inside the plugin while still letting OpenClaw reserve root command names before parsing.

The source page draws an important design boundary across these layers: manifest/config validation should work from **manifest/schema metadata** without executing plugin code; native capability discovery may load trusted plugin entry code to build a non-activating registry snapshot; and native runtime behavior comes from the plugin module's `register(api)` path with `api.registrationMode === "full"`. That split lets OpenClaw validate config, explain missing/disabled plugins, and build UI/schema hints before the full runtime is active.

### Plugin metadata snapshot and lookup table

Gateway startup builds one `PluginMetadataSnapshot` for the current config snapshot. The snapshot is **metadata-only**: it stores the installed plugin index, manifest registry, manifest diagnostics, owner maps, a plugin id normalizer, and manifest records — it does not hold loaded plugin modules, provider SDKs, package contents, or runtime exports. Plugin-aware config validation, startup auto-enable, and Gateway plugin bootstrap consume that snapshot instead of rebuilding manifest/index metadata independently. `PluginLookUpTable` is derived from the same snapshot and adds the startup plugin plan for the current runtime config.

After startup, Gateway keeps the current metadata snapshot as a replaceable runtime product so repeated runtime provider discovery can borrow it instead of reconstructing the installed index and manifest registry for each provider-catalog pass. The snapshot is cleared or replaced on Gateway shutdown, config/plugin inventory changes, and installed index writes; callers fall back to the cold manifest/index path when no compatible current snapshot exists. Compatibility checks must include plugin discovery roots such as `plugins.load.paths` and the default agent workspace, because workspace plugins are part of the metadata scope.

The snapshot and lookup table keep repeated startup decisions on the fast path: channel ownership, deferred channel startup, startup plugin ids, provider and CLI backend ownership, setup provider / command alias / model catalog provider / manifest contract ownership, plugin config schema and channel config schema validation, and startup auto-enable decisions. The safety boundary is **snapshot replacement, not mutation** — rebuild the snapshot when config, plugin inventory, install records, or persisted index policy changes; do not treat it as a broad mutable global registry, and do not keep unbounded historical snapshots. Runtime plugin loading remains separate from metadata snapshots so stale runtime state cannot be hidden behind a metadata cache. The detailed cache rule (manifest and discovery metadata are fresh unless a caller holds an explicit snapshot/lookup table/manifest registry; only runtime loader, module, and dependency-artifact caches persist) is documented under the plugin cache boundary in the internals page.

### Activation planning

Activation planning is part of the **control plane**: callers can ask which plugins are relevant to a concrete command, provider, channel, route, agent harness, or capability before loading broader runtime registries. The planner keeps current manifest behavior compatible: `activation.*` fields are explicit planner hints; `providers`, `channels`, `commandAliases`, `setup.providers`, `contracts.tools`, and hooks remain manifest ownership fallback; the ids-only planner API stays available for existing callers; and the plan API reports reason labels so diagnostics can distinguish explicit hints from ownership fallback. Per the source warning, `activation` is **not** a lifecycle hook or a replacement for `register(...)` — it is metadata used to narrow loading, and ownership fields are preferred when they already describe the relationship. (The shared `message` tool boundary, channel discovery seams, and the rest of the startup sequence are documented in the internals notes; see `oc_plugins_architecture_internals_load_registry`.)

**Source**: OpenClaw documentation — `plugins/architecture` (mirror `inbox/openclaw_docs/plugins/architecture.md`)
**Last Updated**: 2026-06-22
**Status**: Active
