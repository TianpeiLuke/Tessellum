---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - sdk
keywords:
  - openclaw plugin sdk imports
  - plugin-sdk narrow subpath import
  - openclaw/plugin-sdk/plugin-entry
  - channel-core core import convention
  - deprecated branded compat facades
  - channelConfigs channel-config-schema
  - plugin-sdk-entrypoints.json export map
  - internal module barrel api.ts runtime-api.ts
topics:
  - OpenClaw
  - Plugin SDK
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/sdk-overview
access_control_group: ["general"]
---

# OpenClaw — Plugin SDK Import Convention and Subpath Model

## Overview

This note models the **import side** of the OpenClaw plugin SDK — the typed contract between plugins and core — as described by the `plugins/sdk-overview` page's "Import convention", "Subpath reference", and "Internal module convention" sections. The plugin SDK is exposed as a set of narrow `openclaw/plugin-sdk/<subpath>` modules; a plugin author always imports from a specific subpath, never a broad umbrella, to keep startup fast and avoid circular dependencies. This note covers which subpath to import for which purpose, the channel-config subpath family, the deprecated branded/compat facades to avoid, how the generated export map is produced and audited, and the local-barrel convention for a plugin's own internal imports. The `register(api)` registration API and the `OpenClawPluginApi` method/field reference (the other half of the same source page) are modeled by the sibling note **[oc_plugins_sdk_overview_registration_api](oc_plugins_sdk_overview_registration_api.md)**.

## Import Convention

Always import from a specific subpath — each subpath is a small, self-contained module, which keeps startup fast and prevents circular-dependency issues. The canonical form is `import { … } from "openclaw/plugin-sdk/<subpath>"`. The source page gives the two entry-helper examples:

```typescript
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { defineChannelPluginEntry } from "openclaw/plugin-sdk/channel-core";
```

For channel-specific entry/build helpers, prefer `openclaw/plugin-sdk/channel-core`; keep `openclaw/plugin-sdk/core` for the broader umbrella surface and shared helpers such as `buildChannelConfigSchema`.

### Channel config subpaths

For channel config, publish the channel-owned JSON Schema through `openclaw.plugin.json#channelConfigs`. The `plugin-sdk/channel-config-schema` subpath is for shared schema primitives and the generic builder. OpenClaw's bundled plugins use `plugin-sdk/bundled-channel-config-schema` for retained bundled-channel schemas. Deprecated compatibility exports remain on `plugin-sdk/channel-config-schema-legacy`; per the source, neither bundled schema subpath is a pattern for new plugins.

### Deprecated branded/compat facades to avoid

The source page's Warning is explicit: do not import provider- or channel-branded convenience seams — for example `openclaw/plugin-sdk/slack`, `.../discord`, `.../signal`, `.../whatsapp`. Bundled plugins compose generic SDK subpaths inside their own `api.ts` / `runtime-api.ts` barrels; core consumers should either use those plugin-local barrels or add a narrow generic SDK contract when a need is truly cross-channel. A small set of bundled-plugin helper seams still appear in the generated export map when they have tracked owner usage; they exist for bundled-plugin maintenance only and are not recommended import paths for new third-party plugins. Specifically, `openclaw/plugin-sdk/discord` and `openclaw/plugin-sdk/telegram-account` are kept as deprecated compatibility facades for tracked owner usage — do not copy those import paths into new plugins; use injected runtime helpers and generic channel SDK subpaths instead.

## Subpath Reference

The plugin SDK is exposed as a set of narrow subpaths grouped by area: **plugin entry, channel, provider, auth, runtime, capability, memory, and reserved bundled-plugin helpers**. For the full catalog — grouped and linked — the source page points to **[Plugin SDK subpaths](https://docs.openclaw.ai/plugins/sdk-subpaths)** (digested as the planned sibling **[oc_plugins_sdk_subpaths](oc_plugins_sdk_subpaths_core.md)**), which holds the complete grouped catalog this convention references.

### How the export map is generated and audited

The compiler entrypoint inventory lives in `scripts/lib/plugin-sdk-entrypoints.json`. Package exports are generated from the public subset **after subtracting** repo-local test/internal subpaths listed in `scripts/lib/plugin-sdk-private-local-only-subpaths.json`. Run `pnpm plugin-sdk:surface` to audit the public export count. Deprecated public subpaths that are old enough and unused by bundled extension production code are tracked in `scripts/lib/plugin-sdk-deprecated-public-subpaths.json`; broad deprecated re-export barrels are tracked in `scripts/lib/plugin-sdk-deprecated-barrel-subpaths.json`.

## Internal Module Convention

Within a plugin, use local barrel files for internal imports. The source page gives the canonical file layout:

```
my-plugin/
  api.ts            # Public exports for external consumers
  runtime-api.ts    # Internal-only runtime exports
  index.ts          # Plugin entry point
  setup-entry.ts    # Lightweight setup-only entry (optional)
```

The source Warning is strict: **never** import your own plugin through `openclaw/plugin-sdk/<your-plugin>` from production code — route internal imports through `./api.ts` or `./runtime-api.ts`. The SDK path is the external contract only.

### Bundled-facade runtime-config behavior

Facade-loaded bundled-plugin public surfaces (`api.ts`, `runtime-api.ts`, `index.ts`, `setup-entry.ts`, and similar public entry files) prefer the active runtime config snapshot when OpenClaw is already running; if no runtime snapshot exists yet, they fall back to the resolved config file on disk. Packaged bundled-plugin facades should be loaded through OpenClaw's plugin facade loaders — direct imports from `dist/extensions/...` bypass the manifest and runtime sidecar checks that packaged installs use for plugin-owned code.

### Provider plugin-local contract barrels

Provider plugins can expose a narrow plugin-local contract barrel when a helper is intentionally provider-specific and does not belong in a generic SDK subpath yet. The source lists three bundled examples:

- **Anthropic** — a public `api.ts` / `contract-api.ts` seam for Claude beta-header and `service_tier` stream helpers.
- **`@openclaw/openai-provider`** — `api.ts` exports provider builders, default-model helpers, and realtime provider builders.
- **`@openclaw/openrouter-provider`** — `api.ts` exports the provider builder plus onboarding/config helpers.

Extension production code should likewise avoid `openclaw/plugin-sdk/<other-plugin>` imports. If a helper is truly shared, promote it to a neutral SDK subpath such as `openclaw/plugin-sdk/speech`, `.../provider-model-shared`, or another capability-oriented surface instead of coupling two plugins together.

**Source**: OpenClaw documentation — `plugins/sdk-overview` (mirror `inbox/openclaw_docs/plugins/sdk-overview.md`), sections "Import convention", "Subpath reference", "Internal module convention"
**Last Updated**: 2026-06-22
**Status**: Active
