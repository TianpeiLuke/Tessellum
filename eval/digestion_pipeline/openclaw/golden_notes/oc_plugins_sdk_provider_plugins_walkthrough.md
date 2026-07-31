---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - providers
keywords:
  - openclaw provider plugin walkthrough
  - registerProvider catalog auth
  - resolveDynamicModel prepareDynamicModel
  - provider runtime hooks order
  - buildProviderReplayFamilyHooks stream family
  - defineSingleProviderPluginEntry
  - registerModelCatalogProvider live catalog
  - provider extra capabilities tts stt embeddings
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

# OpenClaw — Building a Provider Plugin (Walkthrough)

## Overview

This note is the step-by-step procedure for authoring an OpenClaw **provider plugin** — a plugin that adds a model provider (LLM) to OpenClaw's normal inference loop with a model catalog, API-key auth, and dynamic model resolution. It mirrors the `## Walkthrough` `<Steps>` of the `plugins/sdk-provider-plugins` source page: Step 1 package & manifest, Step 2 register the provider (catalog, live discovery, single-provider helper), Step 3 dynamic model resolution, Step 4 runtime hooks (replay/stream/tool families, auth/usage hooks, the full hook order), Step 5 extra capabilities (speech, transcription, voice, media, embeddings, image/video, web fetch/search), and Step 6 testing. The page warns that if a model must run through a native agent daemon owning threads, compaction, or tool events, pair the provider with an agent harness instead of putting daemon protocol in core. The companion ClawHub-publish + catalog-order + file-structure reference lives in `oc_plugins_sdk_provider_plugins_clawhub_catalog`.

## Step 1: Package and Manifest

The plugin declares two files. `package.json` carries the `openclaw` field with `"extensions": ["./index.ts"]`, `"providers": ["acme-ai"]`, and (required to publish on ClawHub) `compat` (`pluginApi`, `minGatewayVersion`) and `build` (`openclawVersion`, `pluginSdkVersion`). The companion `openclaw.plugin.json` manifest declares `id`, `name`, `description`, `providers`, optional `modelSupport.modelPrefixes`, a `setup.providers[]` block of `envVars`, `providerAuthAliases`, `providerAuthChoices`, and `configSchema`.

```json openclaw.plugin.json
{
  "id": "acme-ai",
  "name": "Acme AI",
  "description": "Acme AI model provider",
  "providers": ["acme-ai"],
  "modelSupport": { "modelPrefixes": ["acme-"] },
  "setup": {
    "providers": [{ "id": "acme-ai", "envVars": ["ACME_AI_API_KEY"] }]
  },
  "providerAuthAliases": { "acme-ai-coding": "acme-ai" },
  "providerAuthChoices": [
    {
      "provider": "acme-ai", "method": "api-key",
      "choiceId": "acme-ai-api-key", "choiceLabel": "Acme AI API key",
      "groupId": "acme-ai", "groupLabel": "Acme AI",
      "cliFlag": "--acme-ai-api-key",
      "cliOption": "--acme-ai-api-key <key>",
      "cliDescription": "Acme AI API key"
    }
  ],
  "configSchema": { "type": "object", "additionalProperties": false }
}
```

Per the source: `setup.providers[].envVars` lets OpenClaw detect credentials **without loading your plugin runtime**; add `providerAuthAliases` when a provider variant should reuse another provider id's auth; `modelSupport` is optional and lets OpenClaw auto-load the provider from shorthand model ids before runtime hooks exist.

## Step 2: Register the Provider

A minimal text provider needs an `id`, `label`, `auth`, and `catalog` — the provider-owned runtime/config hook that can call live vendor APIs and returns `models.providers` entries. The entry is wrapped with `definePluginEntry` and authenticated via `createProviderApiKeyAuthMethod` (`openclaw/plugin-sdk/provider-auth`); inside `register(api)` you call `api.registerProvider(...)`.

```typescript index.ts
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { createProviderApiKeyAuthMethod } from "openclaw/plugin-sdk/provider-auth";

export default definePluginEntry({
  id: "acme-ai", name: "Acme AI", description: "Acme AI model provider",
  register(api) {
    api.registerProvider({
      id: "acme-ai", label: "Acme AI", docsPath: "/providers/acme-ai",
      envVars: ["ACME_AI_API_KEY"],
      auth: [createProviderApiKeyAuthMethod({
        providerId: "acme-ai", methodId: "api-key", label: "Acme AI API key",
        optionKey: "acmeAiApiKey", flagName: "--acme-ai-api-key",
        envVar: "ACME_AI_API_KEY", defaultModel: "acme-ai/acme-large",
      })],
      catalog: {
        order: "simple",
        run: async (ctx) => {
          const apiKey = ctx.resolveProviderApiKey("acme-ai").apiKey;
          if (!apiKey) return null;
          return { provider: {
            baseUrl: "https://api.acme-ai.com/v1", apiKey, api: "openai-completions",
            models: [{ id: "acme-large", name: "Acme Large", reasoning: true,
              input: ["text", "image"],
              cost: { input: 3, output: 15, cacheRead: 0.3, cacheWrite: 3.75 },
              contextWindow: 200000, maxTokens: 32768 }],
          } };
        },
      },
    });
    api.registerModelCatalogProvider({
      provider: "acme-ai", kinds: ["text"],
      liveCatalog: async (ctx) => {
        const apiKey = ctx.resolveProviderApiKey("acme-ai").apiKey;
        if (!apiKey) return null;
        return [{ kind: "text", provider: "acme-ai", model: "acme-large",
          label: "Acme Large", source: "live" }];
      },
    });
  },
});
```

`registerModelCatalogProvider` is the newer control-plane catalog surface for list/help/picker UI — use it for `text`, `image-generation`, `video-generation`, and `music-generation` rows; keep vendor endpoint calls + response mapping in the plugin while OpenClaw owns the shared row shape, source labels, and help rendering. Users can then `openclaw onboard --acme-ai-api-key <key>` and select `acme-ai/acme-large`.

### Live model discovery

If your provider exposes a `/models`-style API, keep the provider-specific endpoint and row projection in your plugin and use `openclaw/plugin-sdk/provider-catalog-live-runtime` for the shared fetch lifecycle (guarded HTTP fetches, provider-auth headers, structured HTTP errors, TTL caching, static fallback). Use `buildLiveModelProviderConfig` when the live API only tells you which provider-owned static rows are available (passing `providerId`, `endpoint`, `providerConfig`, `models`, `apiKey`, `discoveryApiKey`, `fetchGuard`, `ttlMs`, `auditContext`), paired with a `staticCatalog` block. Use `getCachedLiveProviderModelRows` when the API returns richer metadata the plugin must project itself, catching `LiveModelCatalogHttpError` to fall back to static models. Rules: `run` stays auth-gated and returns `null` when no usable credential exists; keep an offline `staticRun`/static fallback so setup/docs/tests/picker surfaces never need live network; use a TTL appropriate for model-list freshness; avoid request-time filesystem polling; and pass a provider-specific `readRows` / `readModelId` only when the upstream response is not an OpenAI-compatible `{ data: [{ id, object }] }` shape.

### Text transforms and the single-provider helper

If the upstream provider uses different control tokens than OpenClaw, add a small bidirectional `api.registerTextTransforms({ input, output })` instead of replacing the stream path: `input` rewrites the final system prompt + text message content before transport; `output` rewrites assistant text deltas + final text before OpenClaw parses its control markers or delivers to a channel.

For bundled providers that register one text provider with API-key auth plus a single catalog-backed runtime, prefer the narrower `defineSingleProviderPluginEntry(...)` helper (from `openclaw/plugin-sdk/provider-entry`). Its `catalog` exposes `buildProvider` (live catalog path used when OpenClaw can resolve real provider auth; may do provider-specific discovery) and `buildStaticProvider` (offline rows safe to show before auth — must not require credentials or make network requests). The page notes `models list --all` currently executes static catalogs only for bundled provider plugins, with empty config, empty env, and no agent/workspace paths. For onboarding that also patches `models.providers.*`, aliases, and the agent default model, use preset helpers from `openclaw/plugin-sdk/provider-onboard` (narrowest: `createDefaultModelPresetAppliers(...)`, `createDefaultModelsPresetAppliers(...)`, `createModelCatalogPresetAppliers(...)`). When a native endpoint supports streamed usage blocks on the normal `openai-completions` transport, prefer shared helpers in `openclaw/plugin-sdk/provider-catalog-shared` (`supportsNativeStreamingUsageCompat(...)`, `applyProviderNativeStreamingUsageCompat(...)`) over hardcoding provider-id checks.

## Step 3: Add Dynamic Model Resolution

If your provider accepts arbitrary model IDs (like a proxy or router), add `resolveDynamicModel` to the `registerProvider` call. It receives a `ctx` (with `ctx.modelId`) and returns a model definition (`id`, `name`, `provider`, `api`, `baseUrl`, `reasoning`, `input`, `cost`, `contextWindow`, `maxTokens`).

```typescript
api.registerProvider({
  // ... id, label, auth, catalog from Step 2
  resolveDynamicModel: (ctx) => ({
    id: ctx.modelId, name: ctx.modelId, provider: "acme-ai",
    api: "openai-completions", baseUrl: "https://api.acme-ai.com/v1",
    reasoning: false, input: ["text"],
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
    contextWindow: 128000, maxTokens: 8192,
  }),
});
```

If resolving requires a network call, use `prepareDynamicModel` for async warm-up — `resolveDynamicModel` runs again after it completes.

## Step 4: Add Runtime Hooks (as needed)

Most providers only need `catalog` + `resolveDynamicModel`; add hooks incrementally. Shared helper builders cover the common replay/tool-compat families, so plugins usually do not hand-wire each hook. Compose `buildProviderReplayFamilyHooks({ family })`, `buildProviderStreamFamilyHooks(...)`, and `buildProviderToolCompatFamilyHooks(...)` (from `provider-model-shared`, `provider-stream`, `provider-tools` under `openclaw/plugin-sdk/`), then spread into `registerProvider`.

```typescript
import { buildProviderReplayFamilyHooks } from "openclaw/plugin-sdk/provider-model-shared";
import { buildProviderStreamFamilyHooks } from "openclaw/plugin-sdk/provider-stream";
import { buildProviderToolCompatFamilyHooks } from "openclaw/plugin-sdk/provider-tools";

const GOOGLE_FAMILY_HOOKS = {
  ...buildProviderReplayFamilyHooks({ family: "google-gemini" }),
  ...buildProviderStreamFamilyHooks("google-thinking"),
  ...buildProviderToolCompatFamilyHooks("gemini"),
};
api.registerProvider({ id: "acme-gemini-compatible", /* ... */ ...GOOGLE_FAMILY_HOOKS });
```

**Available replay families today** (family → bundled examples): `openai-compatible` (OpenAI-style replay incl. tool-call-id sanitation, assistant-first ordering, generic Gemini-turn validation → `moonshot`, `ollama`, `xai`, `zai`); `anthropic-by-model` (Claude-aware replay chosen by `modelId` → `amazon-bedrock`, `anthropic-vertex`); `google-gemini` (native Gemini replay + bootstrap sanitation, with direct `google` overriding `resolveReasoningOutputMode` to `native` → `google`, `google-gemini-cli`); `passthrough-gemini` (Gemini thought-signature sanitation for proxy transports → `openrouter`, `kilocode`, `opencode`, `opencode-go`); `hybrid-anthropic-openai` (mixed Anthropic + OpenAI surfaces in one plugin → `minimax`).

**Available stream families today:** `google-thinking`, `kilocode-thinking`, `moonshot-thinking`, `minimax-fast-mode`, `openai-responses-defaults` (native OpenAI/Codex Responses wrappers: attribution headers, `/fast`/`serviceTier`, text verbosity, native Codex web search, reasoning-compat shaping, Responses context management → `openai`), `openrouter-thinking`, `tool-stream-default-on` (default-on `tool_stream`, e.g. Z.AI). Each builder is composed from lower-level public helpers in the same packages (`provider-model-shared`, `provider-stream`, `provider-stream-shared`, `provider-tools`) you can reach for off the common pattern. Some stream helpers stay provider-local on purpose — `@openclaw/anthropic-provider` keeps `wrapAnthropicProviderStream`, `resolveAnthropicBetas`, `resolveAnthropicFastMode`, `resolveAnthropicServiceTier` in its own seam because they encode Claude OAuth beta handling and `context1m` gating; the xAI plugin keeps native xAI Responses shaping in its own `wrapStreamFn`. The same package-root pattern backs `@openclaw/openai-provider` and `@openclaw/openrouter-provider`.

Specialized hooks (per source tabs): `prepareRuntimeAuth` for a token exchange before each inference call (returns `{ apiKey, baseUrl, expiresAt }`); `wrapStreamFn` for custom headers/body derived from `ctx.streamFn`; `resolveTransportTurnState` / `resolveWebSocketSessionPolicy` for native per-turn/WS headers and metadata; `resolveUsageAuth` + `fetchUsageSnapshot` for usage/billing. `resolveUsageAuth` has three outcomes: `{ token, accountId? }` when a usage credential exists; `{ handled: true }` only when the provider definitively handled usage auth but has no usable token (OpenClaw skips generic fallback); `null`/`undefined` when not handled (OpenClaw continues with generic API-key/OAuth fallback).

**Full provider-hook order.** OpenClaw calls hooks in this order (most providers use 2–3; compatibility-only fields OpenClaw no longer calls — `ProviderPlugin.capabilities`, `suppressBuiltInModel` — are excluded): 1 `catalog`, 2 `applyConfigDefaults`, 3 `normalizeModelId`, 4 `normalizeTransport`, 5 `normalizeConfig`, 6 `applyNativeStreamingUsageCompat`, 7 `resolveConfigApiKey`, 8 `resolveSyntheticAuth`, 9 `shouldDeferSyntheticProfileAuth`, 10 `resolveDynamicModel`, 11 `prepareDynamicModel`, 12 `normalizeResolvedModel`, 13 `normalizeToolSchemas`, 14 `inspectToolSchemas`, 15 `resolveReasoningOutputMode`, 16 `prepareExtraParams`, 17 `createStreamFn`, 19 `wrapStreamFn`, 20 `resolveTransportTurnState`, 21 `resolveWebSocketSessionPolicy`, 22 `formatApiKey`, 23 `refreshOAuth`, 24 `buildAuthDoctorHint`, 25 `matchesContextOverflowError`, 26 `classifyFailoverReason`, 27 `isCacheTtlEligible`, 28 `buildMissingAuthMessage`, 29 `augmentModelCatalog`, 30 `resolveThinkingProfile`, 31 `isBinaryThinking`, 32 `supportsXHighThinking`, 33 `resolveDefaultThinkingLevel`, 34 `isModernModelRef`, 35 `prepareRuntimeAuth`, 36 `resolveUsageAuth`, 37 `fetchUsageSnapshot`, 38 `createEmbeddingProvider`, 39 `buildReplayPolicy`, 40 `sanitizeReplayHistory`, 41 `validateReplayTurns`, 42 `onModelSelected` (the source table skips 18). Runtime fallback notes: `normalizeConfig` checks the matched provider first, then other hook-capable plugins until one changes the config, else the bundled Google normalizer applies; Amazon Bedrock keeps AWS env-marker resolution in its `resolveConfigApiKey` but runtime auth uses the AWS SDK default chain with `auth: "aws-sdk"`; `resolveThinkingProfile(ctx)` receives `provider`, `modelId`, optional merged `reasoning` hint and model `compat` facts (use `compat` only to select the thinking UI/profile); `resolveSystemPromptContribution` lets a provider inject cache-aware system-prompt guidance (preferred over `before_prompt_build` when scoped to one provider/model family).

## Step 5: Add Extra Capabilities (optional)

A provider plugin can register embeddings, speech, realtime transcription, realtime voice, media understanding, image/video generation, web fetch, and web search alongside text inference — OpenClaw classifies this as a **hybrid-capability** plugin (the recommended one-plugin-per-vendor pattern). Register each inside `register(api)` alongside `api.registerProvider(...)`, picking only what you need.

```typescript
api.registerSpeechProvider({ id, label, defaultTimeoutMs, isConfigured, synthesize });
api.registerRealtimeTranscriptionProvider({ id, isConfigured, createSession });
api.registerRealtimeVoiceProvider({ id, label, capabilities, isConfigured, createBridge });
api.registerMediaUnderstandingProvider({ id, capabilities, describeImage, transcribeAudio });
api.registerEmbeddingProvider({ id, defaultModel, transport, authProviderId, create });
api.registerImageGenerationProvider({ id, label, generate });
api.registerVideoGenerationProvider({ id, label, capabilities, generateVideo });
api.registerWebFetchProvider({ id, label, createTool });
api.registerWebSearchProvider({ id, label, search });
```

Per-capability rules: use `assertOkOrThrowProviderError(...)` (`openclaw/plugin-sdk/provider-http`) for provider HTTP failures so plugins share capped error-body reads, JSON error parsing, and request-id suffixes. Prefer `createRealtimeTranscriptionWebSocketSession(...)` for streaming STT (handles proxy capture, reconnect backoff, close flushing, ready handshakes, audio queueing, close-event diagnostics — your plugin only maps upstream events); batch STT POSTing multipart audio uses `buildAudioTranscriptionFormData(...)`. Realtime voice must declare `capabilities` so `talk.catalog` exposes valid modes/transports/audio formats/feature flags, and implement `handleBargeIn` when a transport detects human interruption. Media-understanding providers needing no credentials can expose `resolveAuth` returning `kind: "none"`; new media providers prefer `req.auth` over `req.apiKey`. Embedding providers must declare the same id in `contracts.embeddingProviders` (the general embedding contract incl. memory search; `registerMemoryEmbeddingProvider(...)` is deprecated compatibility). Video capabilities use a **mode-aware** shape (`generate`, `imageToVideo`, `videoToVideo`) because flat aggregate fields cannot advertise transform-mode support or disabled modes cleanly; music generation follows the same pattern with `generate`/`edit` blocks.

## Step 6: Test

Export the provider config object and exercise it directly with vitest — asserting `resolveDynamicModel` returns the requested `id`/`provider`, `catalog.run` returns models when a key is available, and `null` when not.

```typescript src/provider.test.ts
import { describe, it, expect } from "vitest";
import { acmeProvider } from "./provider.js";

describe("acme-ai provider", () => {
  it("resolves dynamic models", () => {
    const model = acmeProvider.resolveDynamicModel!({ modelId: "acme-beta-v3" } as any);
    expect(model.id).toBe("acme-beta-v3");
    expect(model.provider).toBe("acme-ai");
  });
  it("returns catalog when key is available", async () => {
    const result = await acmeProvider.catalog!.run({
      resolveProviderApiKey: () => ({ apiKey: "test-key" }) } as any);
    expect(result?.provider?.models).toHaveLength(2);
  });
  it("returns null catalog when no key", async () => {
    const result = await acmeProvider.catalog!.run({
      resolveProviderApiKey: () => ({ apiKey: undefined }) } as any);
    expect(result).toBeNull();
  });
});
```

**Source**: OpenClaw documentation — `plugins/sdk-provider-plugins` (mirror `inbox/openclaw_docs/plugins/sdk-provider-plugins.md`), `## Walkthrough` Steps 1–6
**Last Updated**: 2026-06-22
**Status**: Active
