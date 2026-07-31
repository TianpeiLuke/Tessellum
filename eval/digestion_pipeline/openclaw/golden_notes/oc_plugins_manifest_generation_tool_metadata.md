---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - manifest
keywords:
  - openclaw plugin manifest generation metadata
  - generation provider metadata reference
  - toolMetadata configSignals authSignals
  - contracts capability ownership snapshot
  - mediaUnderstandingProviderMetadata
  - static auth signals image video music
  - imageGenerationProviderMetadata referenceAudioInputs
  - contracts.tools registerTool ownership
topics:
  - OpenClaw
  - Plugin Manifest
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/manifest
access_control_group: ["general"]
---

# OpenClaw — Manifest Generation, Tool & Contracts Metadata

## Overview

This note models the generation/media/tool metadata blocks of the OpenClaw native plugin manifest (`openclaw.plugin.json`), mirroring the `Generation provider metadata reference`, `Tool metadata reference`, `contracts reference`, and `mediaUnderstandingProviderMetadata reference` sections of the `plugins/manifest` source page. These blocks are all *static, declarative* metadata that OpenClaw reads **before the provider/plugin runtime loads**, so core tools and tool discovery can decide whether a generation provider, media-understanding provider, or plugin-owned tool is available without importing every provider plugin. Transport, request transforms, token refresh, credential validation, and actual generation behavior stay in the plugin runtime — these manifest fields carry only cheap availability evidence and capability-ownership claims.

## Generation provider metadata reference

The generation provider metadata fields describe static auth signals for providers declared in the matching `contracts.*GenerationProviders` list. OpenClaw reads these fields before provider runtime loads so core tools can decide whether a generation provider is available without importing every provider plugin. These fields are for cheap, declarative facts only — transport, request transforms, token refresh, credential validation, and actual generation behavior stay in the plugin runtime. The metadata key (e.g. `imageGenerationProviderMetadata`) is keyed by provider id, and each provider id used must also appear in the matching `contracts` ownership list.

```json
{
  "contracts": {
    "imageGenerationProviders": ["example-image"]
  },
  "imageGenerationProviderMetadata": {
    "example-image": {
      "aliases": ["example-image-oauth"],
      "authProviders": ["example-image"],
      "configSignals": [
        {
          "rootPath": "plugins.entries.example-image.config",
          "overlayPath": "image",
          "mode": {
            "path": "mode",
            "default": "local",
            "allowed": ["local"]
          },
          "requiredAny": ["workflow", "workflowPath"],
          "required": ["promptNodeId"]
        }
      ],
      "authSignals": [
        { "provider": "example-image" },
        {
          "provider": "example-image-oauth",
          "providerBaseUrl": {
            "provider": "example-image",
            "defaultBaseUrl": "https://api.example.com/v1",
            "allowedBaseUrls": ["https://api.example.com/v1"]
          }
        }
      ]
    }
  }
}
```

Each metadata entry supports these fields (all optional):

| Field | Type | What it means |
| --- | --- | --- |
| `aliases` | `string[]` | Additional provider ids that should count as static auth aliases for the generation provider. |
| `authProviders` | `string[]` | Provider ids whose configured auth profiles should count as auth for this generation provider. |
| `configSignals` | `object[]` | Cheap config-only availability signals for local or self-hosted providers that can be configured without auth profiles or env vars. |
| `authSignals` | `object[]` | Explicit auth signals. When present, these replace the default signal set from the provider id, `aliases`, and `authProviders`. |
| `referenceAudioInputs` | `boolean` | Video-generation only. Set to `true` when the provider accepts reference audio assets; otherwise `video_generate` hides audio reference parameters. |

Each `configSignals` entry supports: `rootPath` (required `string`) — dot path to the plugin-owned config object to inspect, e.g. `plugins.entries.example.config`; `overlayPath` (`string`) — dot path inside the root config whose object should overlay the root object before evaluating, used for capability-specific config such as `image`, `video`, or `music`; `overlayMapPath` (`string`) — dot path whose object *values* should each overlay the root object, used for named account maps such as `accounts` where any configured account should qualify; `required` (`string[]`) — dot paths inside the effective config that must have configured values (strings non-empty; objects/arrays not empty); `requiredAny` (`string[]`) — dot paths where at least one must have a configured value; and `mode` (`object`) — an optional string mode guard inside the effective config, used when config-only availability applies only to one mode.

Each `mode` guard supports: `path` (`string`, defaults to `mode`) — dot path inside the effective config; `default` (`string`) — mode value to use when the config omits the path; `allowed` (`string[]`) — if present, the signal passes only when the effective mode is one of these values; and `disallowed` (`string[]`) — if present, the signal fails when the effective mode is one of these values.

Each `authSignals` entry supports: `provider` (required `string`) — provider id to check in configured auth profiles; and `providerBaseUrl` (`object`) — an optional guard that makes the signal count only when the referenced configured provider uses an allowed base URL, used when an auth alias is valid only for certain APIs. Each `providerBaseUrl` guard supports: `provider` (required `string`) — provider config id whose `baseUrl` should be checked; `defaultBaseUrl` (`string`) — base URL to assume when the provider config omits `baseUrl`; and `allowedBaseUrls` (required `string[]`) — allowed base URLs for this auth signal (the signal is ignored when the configured or default base URL does not match one of these normalized values).

## Tool metadata reference

`toolMetadata` uses the same `configSignals` and `authSignals` shapes as generation provider metadata, keyed by tool name. `contracts.tools` declares ownership; `toolMetadata` declares cheap availability evidence so OpenClaw can avoid importing a plugin runtime just to have its tool factory return `null`.

```json
{
  "setup": {
    "providers": [
      { "id": "example", "envVars": ["EXAMPLE_API_KEY"] }
    ]
  },
  "contracts": {
    "tools": ["example_search"]
  },
  "toolMetadata": {
    "example_search": {
      "authSignals": [
        { "provider": "example" }
      ],
      "configSignals": [
        {
          "rootPath": "plugins.entries.example.config",
          "overlayPath": "search",
          "required": ["apiKey"]
        }
      ]
    }
  }
}
```

If a tool has no `toolMetadata`, OpenClaw preserves the existing behavior and loads the owning plugin when the tool contract matches policy. For hot-path tools whose factory depends on auth/config, plugin authors should declare `toolMetadata` instead of making core import runtime to ask.

## contracts reference

Use `contracts` only for static capability ownership metadata that OpenClaw can read without importing the plugin runtime. Each list is optional; the example below shows the full set of recognized ownership lists, and tool discovery uses these lists to load only the plugin runtimes that can own a requested capability or tool.

```json
{
  "contracts": {
    "agentToolResultMiddleware": ["openclaw", "codex"],
    "trustedToolPolicies": ["workflow-budget"],
    "externalAuthProviders": ["acme-ai"],
    "embeddingProviders": ["openai-compatible"],
    "speechProviders": ["openai"],
    "realtimeTranscriptionProviders": ["openai"],
    "realtimeVoiceProviders": ["openai"],
    "memoryEmbeddingProviders": ["local"],
    "mediaUnderstandingProviders": ["openai"],
    "imageGenerationProviders": ["openai"],
    "videoGenerationProviders": ["qwen"],
    "webFetchProviders": ["firecrawl"],
    "webSearchProviders": ["gemini"],
    "migrationProviders": ["hermes"],
    "gatewayMethodDispatch": ["authenticated-request"],
    "tools": ["firecrawl_search", "firecrawl_scrape"]
  }
}
```

The recognized contract lists, each a `string[]`, are:

| Field | What it means |
| --- | --- |
| `embeddedExtensionFactories` | Codex app-server extension factory ids, currently `codex-app-server`. |
| `agentToolResultMiddleware` | Runtime ids this plugin may register tool-result middleware for. |
| `trustedToolPolicies` | Plugin-local trusted pre-tool policy ids an installed plugin may register. Bundled plugins may register policies without this field. |
| `externalAuthProviders` | Provider ids whose external auth profile hook this plugin owns. |
| `embeddingProviders` | General embedding provider ids this plugin owns for reusable vector embedding use, including memory. |
| `speechProviders` | Speech provider ids this plugin owns. |
| `realtimeTranscriptionProviders` | Realtime-transcription provider ids this plugin owns. |
| `realtimeVoiceProviders` | Realtime-voice provider ids this plugin owns. |
| `memoryEmbeddingProviders` | Deprecated memory-specific embedding provider ids this plugin owns. |
| `mediaUnderstandingProviders` | Media-understanding provider ids this plugin owns. |
| `transcriptSourceProviders` | Transcript source provider ids this plugin owns. |
| `imageGenerationProviders` | Image-generation provider ids this plugin owns. |
| `videoGenerationProviders` | Video-generation provider ids this plugin owns. |
| `webFetchProviders` | Web-fetch provider ids this plugin owns. |
| `webSearchProviders` | Web-search provider ids this plugin owns. |
| `migrationProviders` | Import provider ids this plugin owns for `openclaw migrate`. |
| `gatewayMethodDispatch` | Reserved entitlement for authenticated plugin HTTP routes that dispatch Gateway methods in-process. |
| `tools` | Agent tool names this plugin owns. |

Several lists carry registration/enforcement rules. `contracts.embeddedExtensionFactories` is retained for bundled Codex app-server-only extension factories; bundled tool-result transforms should instead declare `contracts.agentToolResultMiddleware` and register with `api.registerAgentToolResultMiddleware(...)`, and installed plugins may use the same middleware seam only when explicitly enabled and only for runtimes they declare. Installed plugins needing the host-trusted pre-tool policy tier must declare each registered local id in `contracts.trustedToolPolicies` and be explicitly enabled — bundled plugins keep the existing trusted-policy path, but installed plugins with undeclared policy ids are rejected before registration; policy ids are scoped to the registering plugin (two plugins may both declare and register `workflow-budget`, but a single plugin may not register the same local id twice). Runtime `api.registerTool(...)` registrations must match `contracts.tools`. Provider plugins implementing `resolveExternalAuthProfiles` must declare `contracts.externalAuthProviders` or the external-auth hook is ignored. General embedding providers should declare `contracts.embeddingProviders` for each adapter registered with `api.registerEmbeddingProvider(...)` for reusable vector generation (including memory search); `contracts.memoryEmbeddingProviders` is deprecated memory-specific compatibility that remains only while existing providers migrate to the generic seam. `contracts.gatewayMethodDispatch` currently accepts `"authenticated-request"` and is an API hygiene gate for native plugin HTTP routes that intentionally dispatch Gateway control-plane methods in-process (not a sandbox against malicious native plugins) — use it only for tightly reviewed bundled/operator surfaces that already require Gateway HTTP auth.

## mediaUnderstandingProviderMetadata reference

Use `mediaUnderstandingProviderMetadata` when a media-understanding provider has default models, auto-auth fallback priority, or native document support that generic core helpers need before runtime loads. Keys must also be declared in `contracts.mediaUnderstandingProviders`.

```json
{
  "contracts": {
    "mediaUnderstandingProviders": ["example"]
  },
  "mediaUnderstandingProviderMetadata": {
    "example": {
      "capabilities": ["image", "audio"],
      "defaultModels": {
        "image": "example-vision-latest",
        "audio": "example-transcribe-latest"
      },
      "autoPriority": {
        "image": 40
      },
      "nativeDocumentInputs": ["pdf"]
    }
  }
}
```

Each provider entry can include: `capabilities` (`("image" | "audio" | "video")[]`) — media capabilities exposed by this provider; `defaultModels` (`Record<string, string>`) — capability-to-model defaults used when config does not specify a model; `autoPriority` (`Record<string, number>`) — lower numbers sort earlier for automatic credential-based provider fallback; and `nativeDocumentInputs` (`"pdf"[]`) — native document inputs supported by the provider.

**Source**: OpenClaw documentation — `plugins/manifest` (mirror `inbox/openclaw_docs/plugins/manifest.md`), sections "Generation provider metadata reference", "Tool metadata reference", "contracts reference", "mediaUnderstandingProviderMetadata reference"
**Last Updated**: 2026-06-22
**Status**: Active
