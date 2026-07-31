---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - load_pipeline
keywords:
  - openclaw plugin load pipeline
  - plugin registry model
  - manifest-first control plane
  - native loader jiti fallback
  - register api activate alias
  - plugin cache boundary
  - activation planner plugin metadata snapshot
  - path safety gates
topics:
  - OpenClaw
  - Plugin Architecture Internals
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/architecture-internals
access_control_group: ["general"]
---

# OpenClaw — Plugin Load Pipeline and Registry Model

## Overview

This note explains the OpenClaw **plugin load pipeline** and the **central plugin registry** it feeds — the internal mechanics by which a manifest on disk becomes a live, one-way registration core can read. It mirrors the `## Load pipeline` (including `### Manifest-first behavior` and `### Plugin cache boundary`) and `## Registry model` sections of the `plugins/architecture-internals` source page. The conceptual model here is the mental map for debugging plugin load order and registry state: how startup discovers candidates, reads manifests, rejects unsafe entries, decides enablement, loads native modules (native loader vs the emergency Jiti fallback), calls `register(api)`, and exposes the resulting registry. Runtime hooks/helpers (`## Conversation binding callbacks` onward) and the gateway/SDK reference tables are documented in the sibling notes and are out of scope here.

## Load pipeline

At startup OpenClaw runs roughly an eight-step sequence to turn discoverable plugin roots into a populated registry:

1. discover candidate plugin roots
2. read native or compatible bundle manifests and package metadata
3. reject unsafe candidates
4. normalize plugin config (`plugins.enabled`, `allow`, `deny`, `entries`, `slots`, `load.paths`)
5. decide enablement for each candidate
6. load enabled native modules: built bundled modules use a native loader; third-party local source TypeScript uses the emergency Jiti fallback
7. call native `register(api)` hooks and collect registrations into the plugin registry
8. expose the registry to commands/runtime surfaces

The entry hook is `register` — but `activate` is a **legacy alias for `register`**: the loader resolves whichever is present (`def.register ?? def.activate`) and calls it at the same point. All bundled plugins use `register`, and `register` is preferred for new plugins.

The **safety gates happen before runtime execution** (between discovery and load). Candidates are blocked when the entry escapes the plugin root, the path is world-writable, or path ownership looks suspicious for non-bundled plugins. Blocked candidates remain tied to their plugin id for diagnostics: if config still references that id, validation reports the plugin as present but blocked and points back to the path-safety warning instead of treating the config entry as stale.

### Manifest-first behavior

The **manifest is the control-plane source of truth.** OpenClaw uses it to identify the plugin, discover declared channels/skills/config schema or bundle capabilities, validate `plugins.entries.<id>.config`, augment Control UI labels/placeholders, show install/catalog metadata, and preserve cheap activation and setup descriptors **without loading plugin runtime**. For native plugins the runtime module is the **data-plane** part — it registers actual behavior such as hooks, tools, commands, or provider flows. Optional manifest `activation` and `setup` blocks stay on the control plane: they are metadata-only descriptors for activation planning and setup discovery and do not replace runtime registration, `register(...)`, or `setupEntry`.

The first live activation consumers use manifest command, channel, and provider hints to **narrow plugin loading** before broader registry materialization: CLI loading narrows to plugins that own the requested primary command; channel setup/plugin resolution narrows to plugins that own the requested channel id; explicit provider setup/runtime resolution narrows to plugins that own the requested provider id; and Gateway startup planning uses `activation.onStartup` for explicit startup imports and startup opt-outs, while plugins without startup metadata load only through narrower activation triggers. Request-time runtime preloads that ask for the broad `all` scope still derive an explicit effective plugin id set from config, startup planning, configured channels, slots, and auto-enable rules; if that derived set is empty, OpenClaw loads an **empty runtime registry instead of widening to every discoverable plugin**.

The **activation planner** exposes both an ids-only API for existing callers and a plan API for new diagnostics. Plan entries report why a plugin was selected, separating explicit `activation.*` planner hints from manifest ownership fallback such as `providers`, `channels`, `commandAliases`, `setup.providers`, `contracts.tools`, and hooks. That reason split is the compatibility boundary: existing plugin metadata keeps working, while new code can detect broad hints or fallback behavior without changing runtime loading semantics.

Setup discovery prefers descriptor-owned ids such as `setup.providers` and `setup.cliBackends` to narrow candidate plugins before falling back to `setup-api` for plugins that still need setup-time runtime hooks. Provider setup lists use manifest `providerAuthChoices`, descriptor-derived setup choices, and install-catalog metadata without loading provider runtime. Explicit `setup.requiresRuntime: false` is a descriptor-only cutoff; omitted `requiresRuntime` keeps the legacy setup-api fallback for compatibility. If more than one discovered plugin claims the same normalized setup provider or CLI backend id, setup lookup refuses the ambiguous owner instead of relying on discovery order. When setup runtime does execute, registry diagnostics report drift between `setup.providers` / `setup.cliBackends` and the providers or CLI backends registered by setup-api without blocking legacy plugins.

### Plugin cache boundary

OpenClaw does **not** cache plugin discovery results or direct manifest registry data behind wall-clock windows: installs, manifest edits, and load-path changes must become visible on the next explicit metadata read or snapshot rebuild. The manifest file parser may keep a bounded file-signature cache keyed by the opened manifest path, inode, size, and timestamps; that cache only avoids re-parsing unchanged bytes and **must not** cache discovery, registry, owner, or policy answers.

The safe metadata fast path is **explicit object ownership, not a hidden cache.** Gateway startup hot paths should pass the current `PluginMetadataSnapshot`, the derived `PluginLookUpTable`, or an explicit manifest registry through the call chain. Config validation, startup auto-enable, plugin bootstrap, and provider selection can reuse those objects while they represent the current config and plugin inventory. Setup lookup still reconstructs manifest metadata on demand unless the specific setup path receives an explicit manifest registry; that stays a cold-path fallback rather than a hidden lookup cache. When the input changes, OpenClaw rebuilds and replaces the snapshot instead of mutating it or keeping historical copies. Views over the active plugin registry and bundled channel bootstrap helpers should be recomputed from the current registry/root; short-lived maps are fine inside one call to dedupe work or guard reentry but must not become process metadata caches.

For plugin loading the **persistent cache layer is runtime loading**. It may reuse loader state when code or installed artifacts are actually loaded, such as:

- `PluginLoaderCacheState` and compatible active runtime registries
- jiti/module caches and public-surface loader caches used to avoid importing the same runtime surface repeatedly
- filesystem caches for installed plugin artifacts
- short-lived per-call maps for path normalization or duplicate resolution

Those caches are data-plane implementation details and must **not** answer control-plane questions such as "which plugin owns this provider?" unless the caller deliberately asked for runtime loading. OpenClaw explicitly forbids persistent or wall-clock caches for: discovery results; direct manifest registries; manifest registries reconstructed from the installed plugin index; provider owner lookup, model suppression, provider policy, or public-artifact metadata; and any other manifest-derived answer where a changed manifest, installed index, or load path should be visible on the next metadata read. Callers that rebuild manifest metadata from the persisted installed plugin index reconstruct that registry on demand — the installed index is durable source-plane state, not a hidden in-process metadata cache.

## Registry model

Loaded plugins do **not** directly mutate random core globals; they register into a **central plugin registry**. The registry tracks:

- plugin records (identity, source, origin, status, diagnostics)
- tools
- legacy hooks and typed hooks
- channels
- providers
- gateway RPC handlers
- HTTP routes
- CLI registrars
- background services
- plugin-owned commands

Core features then read from that registry instead of talking to plugin modules directly. This keeps loading **one-way**: plugin module → registry registration, and core runtime → registry consumption. That separation matters for maintainability — most core surfaces need only one integration point ("read the registry"), not a special-case for every plugin module.

**Source**: OpenClaw documentation — `plugins/architecture-internals` (mirror `inbox/openclaw_docs/plugins/architecture-internals.md`), sections `## Load pipeline` (+ Manifest-first behavior, Plugin cache boundary) and `## Registry model`
**Last Updated**: 2026-06-22
**Status**: Active
