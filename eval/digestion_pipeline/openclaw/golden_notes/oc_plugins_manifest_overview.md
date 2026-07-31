---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - manifest
keywords:
  - openclaw plugin manifest
  - openclaw.plugin.json
  - configschema config validation
  - native manifest vs compatible bundle
  - top-level field reference
  - plugins.entries.id
  - cheap pre-load metadata
topics:
  - OpenClaw
  - Plugin Manifest
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/manifest
access_control_group: ["general"]
---

# OpenClaw — Plugin Manifest Overview (`openclaw.plugin.json`)

## Overview

This note covers the OpenClaw **native plugin manifest** as introduced on the `plugins/manifest` source page: what the `openclaw.plugin.json` file is, why every native plugin must ship one, the boundary between native manifests and compatible (Codex/Claude/Cursor) bundle layouts, and the full top-level field reference. The manifest is the cheap, declarative metadata OpenClaw reads **before it loads any plugin code** — so its purpose is to let the host validate configuration and discover capability ownership without booting plugin runtime. It mirrors the source page's intro, "What this file does", the minimal/rich JSON examples, and the "Top-level field reference" table. The deeper per-block field references (provider/model, generation/tool, channel/UI/setup, discovery/validation) are documented in the sibling `oc_plugins_manifest_*` notes.

## Native manifest versus compatible bundles

This contract is for the **native OpenClaw plugin manifest** only. Every native OpenClaw plugin **must** ship an `openclaw.plugin.json` file in the **plugin root**; OpenClaw uses this manifest to validate configuration **without executing plugin code**, and a missing or invalid manifest is treated as a plugin error that blocks config validation. Compatible bundle layouts use different manifest files and are auto-detected but **not** validated against the `openclaw.plugin.json` schema: a Codex bundle uses `.codex-plugin/plugin.json`, a Claude bundle uses `.claude-plugin/plugin.json` (or the default Claude component layout with no manifest), and a Cursor bundle uses `.cursor-plugin/plugin.json`. For compatible bundles, OpenClaw currently reads bundle metadata plus declared skill roots, Claude command roots, Claude bundle `settings.json` defaults, Claude bundle LSP defaults, and supported hook packs when the layout matches OpenClaw runtime expectations. Compatible bundle layouts are documented separately under Plugin bundles (`/plugins/bundles`), and the native capability model under the Capability model page (`/plugins/architecture#public-capability-model`).

## What the manifest is for

`openclaw.plugin.json` is the metadata OpenClaw reads **before it loads your plugin code**, so everything declared in it must be cheap enough to inspect without booting the plugin runtime. The source page enumerates what the manifest is **used for**:

- plugin identity, config validation, and config UI hints
- auth, onboarding, and setup metadata (alias, auto-enable, provider env vars, auth choices)
- activation hints for control-plane surfaces
- shorthand model-family ownership
- static capability-ownership snapshots (`contracts`)
- QA runner metadata the shared `openclaw qa` host can inspect
- channel-specific config metadata merged into catalog and validation surfaces

It is explicitly **not** for registering runtime behavior, declaring code entrypoints, or npm install metadata — those belong in your plugin code and `package.json` (the manifest-vs-`package.json` split is detailed in the discovery/validation sibling note). This "declarative metadata read before code" design is the core concept: the host can answer "what does this plugin own and is its config valid?" without the cost or risk of importing plugin runtime.

## Minimal example

The smallest valid manifest declares only the required `id` and `configSchema`. A plugin with no config still ships an empty-object schema with `additionalProperties: false`:

```json
{
  "id": "voice-call",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

## Rich example

A fully populated manifest — here a provider plugin (`openrouter`) — layers provider/model, auth, setup, and UI-hint metadata on top of the required fields. This single document is what the host reads to classify the provider's endpoints, model-id normalization, auth choices, and config UI before any provider runtime is imported:

```json
{
  "id": "openrouter",
  "name": "OpenRouter",
  "description": "OpenRouter provider plugin",
  "version": "1.0.0",
  "providers": ["openrouter"],
  "modelSupport": {
    "modelPrefixes": ["router-"]
  },
  "modelIdNormalization": {
    "providers": {
      "openrouter": {
        "prefixWhenBare": "openrouter"
      }
    }
  },
  "providerEndpoints": [
    {
      "endpointClass": "openrouter",
      "hostSuffixes": ["openrouter.ai"]
    }
  ],
  "providerRequest": {
    "providers": {
      "openrouter": {
        "family": "openrouter"
      }
    }
  },
  "cliBackends": ["openrouter-cli"],
  "syntheticAuthRefs": ["openrouter-cli"],
  "setup": {
    "providers": [
      {
        "id": "openrouter",
        "envVars": ["OPENROUTER_API_KEY"]
      }
    ]
  },
  "providerAuthAliases": {
    "openrouter-coding": "openrouter"
  },
  "channelEnvVars": {
    "openrouter-chatops": ["OPENROUTER_CHATOPS_TOKEN"]
  },
  "providerAuthChoices": [
    {
      "provider": "openrouter",
      "method": "api-key",
      "choiceId": "openrouter-api-key",
      "choiceLabel": "OpenRouter API key",
      "groupId": "openrouter",
      "groupLabel": "OpenRouter",
      "optionKey": "openrouterApiKey",
      "cliFlag": "--openrouter-api-key",
      "cliOption": "--openrouter-api-key <key>",
      "cliDescription": "OpenRouter API key",
      "onboardingScopes": ["text-inference"]
    }
  ],
  "uiHints": {
    "apiKey": {
      "label": "API key",
      "placeholder": "sk-or-v1-...",
      "sensitive": true
    }
  },
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": {
        "type": "string"
      }
    }
  }
}
```

## Top-level field reference

Only `id` and `configSchema` are **Required**; every other field is optional metadata. The detailed field references for each cluster (provider/model, generation/tool/contracts, channel/UI/setup, discovery/validation) live in the sibling notes — the table below is the full top-level inventory verbatim from the source.

| Field | Required | Type | What it means |
| --- | --- | --- | --- |
| `id` | Yes | `string` | Canonical plugin id. This is the id used in `plugins.entries.<id>`. |
| `configSchema` | Yes | `object` | Inline JSON Schema for this plugin's config. |
| `requiresPlugins` | No | `string[]` | Plugin ids that must also be installed for this plugin to have an effect. Discovery keeps the plugin loadable but warns when any required plugin is missing. |
| `enabledByDefault` | No | `true` | Marks a bundled plugin as enabled by default. Omit it, or set any non-`true` value, to leave the plugin disabled by default. |
| `enabledByDefaultOnPlatforms` | No | `string[]` | Marks a bundled plugin as enabled by default only on the listed Node.js platforms, for example `["darwin"]`. Explicit config still wins. |
| `legacyPluginIds` | No | `string[]` | Legacy ids that normalize to this canonical plugin id. |
| `autoEnableWhenConfiguredProviders` | No | `string[]` | Provider ids that should auto-enable this plugin when auth, config, or model refs mention them. |
| `kind` | No | `"memory"` \| `"context-engine"` | Declares an exclusive plugin kind used by `plugins.slots.*`. |
| `channels` | No | `string[]` | Channel ids owned by this plugin. Used for discovery and config validation. |
| `providers` | No | `string[]` | Provider ids owned by this plugin. |
| `providerCatalogEntry` | No | `string` | Lightweight provider-catalog module path, relative to the plugin root, for manifest-scoped provider catalog metadata that can be loaded without activating the full plugin runtime. |
| `modelSupport` | No | `object` | Manifest-owned shorthand model-family metadata used to auto-load the plugin before runtime. |
| `modelCatalog` | No | `object` | Declarative model catalog metadata for providers owned by this plugin. This is the control-plane contract for future read-only listing, onboarding, model pickers, aliases, and suppression without loading plugin runtime. |
| `modelPricing` | No | `object` | Provider-owned external pricing lookup policy. Use it to opt local/self-hosted providers out of remote pricing catalogs or map provider refs to OpenRouter/LiteLLM catalog ids without hardcoding provider ids in core. |
| `modelIdNormalization` | No | `object` | Provider-owned model-id alias/prefix cleanup that must run before provider runtime loads. |
| `providerEndpoints` | No | `object[]` | Manifest-owned endpoint host/baseUrl metadata for provider routes that core must classify before provider runtime loads. |
| `providerRequest` | No | `object` | Cheap provider-family and request-compatibility metadata used by generic request policy before provider runtime loads. |
| `secretProviderIntegrations` | No | `Record<string, object>` | Declarative SecretRef exec provider presets that setup or install surfaces can offer without hardcoding provider-specific integrations in core. |
| `cliBackends` | No | `string[]` | CLI inference backend ids owned by this plugin. Used for startup auto-activation from explicit config refs. |
| `syntheticAuthRefs` | No | `string[]` | Provider or CLI backend refs whose plugin-owned synthetic auth hook should be probed during cold model discovery before runtime loads. |
| `nonSecretAuthMarkers` | No | `string[]` | Bundled-plugin-owned placeholder API key values that represent non-secret local, OAuth, or ambient credential state. |
| `commandAliases` | No | `object[]` | Command names owned by this plugin that should produce plugin-aware config and CLI diagnostics before runtime loads. |
| `providerAuthEnvVars` | No | `Record<string, string[]>` | Deprecated compatibility env metadata for provider auth/status lookup. Prefer `setup.providers[].envVars` for new plugins; OpenClaw still reads this during the deprecation window. |
| `providerAuthAliases` | No | `Record<string, string>` | Provider ids that should reuse another provider id for auth lookup, for example a coding provider that shares the base provider API key and auth profiles. |
| `channelEnvVars` | No | `Record<string, string[]>` | Cheap channel env metadata that OpenClaw can inspect without loading plugin code. Use this for env-driven channel setup or auth surfaces that generic startup/config helpers should see. |
| `providerAuthChoices` | No | `object[]` | Cheap auth-choice metadata for onboarding pickers, preferred-provider resolution, and simple CLI flag wiring. |
| `activation` | No | `object` | Cheap activation planner metadata for startup, provider, command, channel, route, and capability-triggered loading. Metadata only; plugin runtime still owns actual behavior. |
| `setup` | No | `object` | Cheap setup/onboarding descriptors that discovery and setup surfaces can inspect without loading plugin runtime. |
| `qaRunners` | No | `object[]` | Cheap QA runner descriptors used by the shared `openclaw qa` host before plugin runtime loads. |
| `contracts` | No | `object` | Static capability ownership snapshot for external auth hooks, embeddings, speech, realtime transcription, realtime voice, media-understanding, image-generation, music-generation, video-generation, web-fetch, web search, and tool ownership. |
| `mediaUnderstandingProviderMetadata` | No | `Record<string, object>` | Cheap media-understanding defaults for provider ids declared in `contracts.mediaUnderstandingProviders`. |
| `imageGenerationProviderMetadata` | No | `Record<string, object>` | Cheap image-generation auth metadata for provider ids declared in `contracts.imageGenerationProviders`, including provider-owned auth aliases and base-url guards. |
| `videoGenerationProviderMetadata` | No | `Record<string, object>` | Cheap video-generation auth metadata for provider ids declared in `contracts.videoGenerationProviders`, including provider-owned auth aliases and base-url guards. |
| `musicGenerationProviderMetadata` | No | `Record<string, object>` | Cheap music-generation auth metadata for provider ids declared in `contracts.musicGenerationProviders`, including provider-owned auth aliases and base-url guards. |
| `toolMetadata` | No | `Record<string, object>` | Cheap availability metadata for plugin-owned tools declared in `contracts.tools`. Use it when a tool should not load runtime unless config, env, or auth evidence exists. |
| `channelConfigs` | No | `Record<string, object>` | Manifest-owned channel config metadata merged into discovery and validation surfaces before runtime loads. |
| `skills` | No | `string[]` | Skill directories to load, relative to the plugin root. |
| `name` | No | `string` | Human-readable plugin name. |
| `description` | No | `string` | Short summary shown in plugin surfaces. |
| `version` | No | `string` | Informational plugin version. |
| `uiHints` | No | `Record<string, object>` | UI labels, placeholders, and sensitivity hints for config fields. |

**Source**: OpenClaw documentation — `plugins/manifest` (mirror `inbox/openclaw_docs/plugins/manifest.md`), intro + What this file does + Minimal/Rich example + Top-level field reference
**Last Updated**: 2026-06-22
**Status**: Active
