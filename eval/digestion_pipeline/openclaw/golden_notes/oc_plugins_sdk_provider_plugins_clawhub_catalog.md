---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - clawhub
keywords:
  - openclaw provider plugin publish
  - clawhub package publish
  - provider plugin file structure
  - catalog order reference
  - catalog order simple profile paired late
  - provider plugin model catalog
  - provider plugin clawhub
topics:
  - OpenClaw
  - Provider Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/sdk-provider-plugins
access_control_group: ["general"]
---

# OpenClaw — Publishing a Provider Plugin to ClawHub & Catalog-Order Reference

## Overview

This procedure covers the deployment half of the OpenClaw provider-plugin guide: how to publish a provider plugin to ClawHub, the canonical provider-plugin on-disk file structure, and the `catalog.order` reference that controls when a plugin's model catalog merges relative to built-in providers. It mirrors the trailing sections of the `plugins/sdk-provider-plugins` source page (Publish to ClawHub, File structure, Catalog order reference, Next steps). The authoring walkthrough that produces the provider this section publishes — package/manifest, `registerProvider`, dynamic model resolution, runtime hooks, extra capabilities, and tests — is the companion note `oc_plugins_sdk_provider_plugins_walkthrough`.

## Publish to ClawHub

Provider plugins publish the same way as any other external code plugin. Run the dry-run first, then the real publish:

```bash
clawhub package publish your-org/your-plugin --dry-run
clawhub package publish your-org/your-plugin
```

Do not use the legacy skill-only publish alias here; plugin packages should use `clawhub package publish`.

Publishing on ClawHub requires the `openclaw.compat` and `openclaw.build` fields in `package.json` — the source notes that "if you publish the provider on ClawHub, those `openclaw.compat` and `openclaw.build` fields are required in `package.json`." Those fields are set during the package/manifest step of the authoring walkthrough; for a provider they look like `compat: { pluginApi, minGatewayVersion }` and `build: { openclawVersion, pluginSdkVersion }`. *(The exact pin values are shown in the authoring walkthrough note, not duplicated here.)*

## File structure

The canonical on-disk layout for a bundled provider plugin (here the `acme-ai` example) is:

```
<bundled-plugin-root>/acme-ai/
├── package.json              # openclaw.providers metadata
├── openclaw.plugin.json      # Manifest with provider auth metadata
├── index.ts                  # definePluginEntry + registerProvider
└── src/
    ├── provider.test.ts      # Tests
    └── usage.ts              # Usage endpoint (optional)
```

Each file maps to one authoring concern: `package.json` carries the `openclaw.providers` metadata; `openclaw.plugin.json` is the manifest carrying provider auth metadata; `index.ts` holds the `definePluginEntry` + `registerProvider` wiring; and the `src/` directory holds the `provider.test.ts` tests and an optional `usage.ts` usage endpoint.

## Catalog order reference

`catalog.order` controls when your catalog merges relative to built-in providers. The source documents four ordering values, each running in a distinct pass:

| Order     | When          | Use case                                        |
| --------- | ------------- | ----------------------------------------------- |
| `simple`  | First pass    | Plain API-key providers                         |
| `profile` | After simple  | Providers gated on auth profiles                |
| `paired`  | After profile | Synthesize multiple related entries             |
| `late`    | Last pass     | Override existing providers (wins on collision) |

`simple` runs in the first pass and fits plain API-key providers (the value used by the `acme-ai` example's `catalog: { order: "simple", ... }`). `profile` runs after `simple` and is for providers gated on auth profiles. `paired` runs after `profile` and is used to synthesize multiple related entries. `late` runs in the last pass and is the override slot — a `late` catalog wins on collision with an existing provider, which is how an aggregator/proxy plugin can override built-in provider rows.

## Next steps

The source page closes by pointing to the related plugin-SDK references that complete a provider plugin:

- **Channel Plugins** (`/plugins/sdk-channel-plugins`) — if your plugin also provides a channel.
- **SDK Runtime** (`/plugins/sdk-runtime`) — the `api.runtime` helpers (TTS, search, subagent).
- **SDK Overview** (`/plugins/sdk-overview`) — the full subpath import reference.
- **Plugin Internals** (`/plugins/architecture-internals#provider-runtime-hooks`) — provider runtime-hook details and bundled examples.

The page's trailing `## Related` list cites Plugin SDK setup (`/plugins/sdk-setup`), Building plugins (`/plugins/building-plugins`), and Building channel plugins (`/plugins/sdk-channel-plugins`).

**Source**: OpenClaw documentation — `plugins/sdk-provider-plugins` (mirror `inbox/openclaw_docs/plugins/sdk-provider-plugins.md`), sections Publish to ClawHub / File structure / Catalog order reference / Next steps
**Last Updated**: 2026-06-22
**Status**: Active
