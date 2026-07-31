---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - runtime_hooks
keywords:
  - openclaw plugin runtime hooks
  - provider runtime hooks hook order
  - before_model_resolve before_prompt_build
  - api.runtime tts mediaUnderstanding subagent
  - api.runtime.imageGeneration generate
  - onConversationBindingResolved
  - adding a new capability checklist
  - registerSpeechProvider registerMediaUnderstandingProvider
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

# OpenClaw — Plugin Runtime Hooks, Helpers, and Adding a Capability

## Overview

This note covers the plugin **runtime extension surface** documented in the back half of the `plugins/architecture-internals` source page: the conversation-binding callback, the three-layer provider model with its ordered 40+ provider runtime hooks, the `api.runtime.*` helper accessors (TTS, speech, media-understanding, subagent, web-search, image-generation), and the internal "add a new capability" sequence plus checklist and template. These are the hooks and helpers a native plugin uses at runtime — after the load pipeline calls `register(api)` and collects its registrations (the prerequisite registry is covered by `oc_plugins_architecture_internals_load_registry`). The reference tables (gateway HTTP routes, SDK import paths, message-tool schemas, catalogs) live in the sibling reference note.

## Conversation Binding Callbacks

A plugin that binds a conversation can react to a resolved approval by registering `api.onConversationBindingResolved(...)`. The callback fires **after a bind request is approved or denied**, after core approval handling finishes. Payload fields:

- `status`: `"approved"` or `"denied"`.
- `decision`: `"allow-once"`, `"allow-always"`, or `"deny"`.
- `binding`: the resolved binding, present for approved requests.
- `request`: original request summary, detach hint, sender id, conversation metadata.

This callback is **notification-only** — it does not change who is allowed to bind a conversation. A plugin uses the `approved` branch to read `event.binding?.conversationId`, and the denied branch to clear local pending state via `event.request.conversation.conversationId`.

## Provider Runtime Hooks

Provider plugins have **three layers**. (1) **Manifest metadata** for cheap pre-runtime lookup: `setup.providers[].envVars`, deprecated `providerAuthEnvVars`, `providerAuthAliases`, `providerAuthChoices`, and `channelEnvVars`. (2) **Config-time hooks**: `catalog` (legacy alias `discovery`) plus `applyConfigDefaults`. (3) **Runtime hooks**: 40+ optional hooks covering auth, model resolution, stream wrapping, thinking levels, replay policy, and usage endpoints. OpenClaw still owns the generic agent loop, failover, transcript handling, and tool policy — these hooks are the extension surface for provider-specific behavior without a custom inference transport. Compatibility-only fields OpenClaw no longer calls (`ProviderPlugin.capabilities`, `suppressBuiltInModel`) are intentionally not in the hook order.

The manifest layer lets generic auth/status/model-picker paths see provider facts without loading plugin runtime: `setup.providers[].envVars` for env-based credentials; `providerAuthAliases` to reuse another provider id's env vars/auth profiles/onboarding choice; `providerAuthChoices` to give onboarding CLI surfaces the choice id, group labels, and one-flag auth wiring; and `channelEnvVars` for env-driven channel auth. Provider runtime `envVars` is kept only for operator-facing hints (onboarding labels, OAuth client-id/secret setup vars).

### Hook Order and Usage

For model/provider plugins, OpenClaw calls hooks in this rough order; the "What it does" column is the quick decision guide. The hook names are verbatim from source.

| #  | Hook | What it does |
| --- | --- | --- |
| 1 | `catalog` | Publish provider config into `models.providers` at `models.json` generation |
| 2 | `applyConfigDefaults` | Apply provider-owned global config defaults at materialization |
| 3 | `normalizeModelId` | Normalize legacy/preview model-id aliases before lookup |
| 4 | `normalizeTransport` | Normalize provider-family `api`/`baseUrl` before model assembly |
| 5 | `normalizeConfig` | Normalize `models.providers.<id>` before resolution |
| 6 | `applyNativeStreamingUsageCompat` | Native streaming-usage compat rewrites for config providers |
| 7 | `resolveConfigApiKey` | Resolve env-marker auth before runtime auth loading |
| 8 | `resolveSyntheticAuth` | Surface local/config-backed auth without persisting plaintext |
| 9 | `resolveExternalAuthProfiles` | Overlay external auth profiles (default `persistence: runtime-only`) |
| 10 | `shouldDeferSyntheticProfileAuth` | Defer synthetic placeholders behind env/config auth |
| 11 | `resolveDynamicModel` | Sync fallback for model ids not yet in the registry |
| 12 | `prepareDynamicModel` | Async warm-up, then `resolveDynamicModel` reruns |
| 13 | `normalizeResolvedModel` | Final rewrite before the runner uses the resolved model |
| 14 | `normalizeToolSchemas` | Normalize tool schemas before the runner sees them |
| 15 | `inspectToolSchemas` | Surface schema diagnostics after normalization |
| 16 | `resolveReasoningOutputMode` | Select native vs tagged reasoning-output contract |
| 17 | `prepareExtraParams` | Request-param normalization before stream wrappers |
| 18 | `createStreamFn` | Fully replace the stream path with a custom transport |
| 20 | `wrapStreamFn` | Stream wrapper after generic wrappers apply |
| 21 | `resolveTransportTurnState` | Attach native per-turn transport headers/metadata |
| 22 | `resolveWebSocketSessionPolicy` | Attach native WS headers / session cool-down policy |
| 23 | `formatApiKey` | Stored profile becomes the runtime `apiKey` string |
| 24 | `refreshOAuth` | OAuth refresh override for custom endpoints/failure policy |
| 25 | `buildAuthDoctorHint` | Repair hint when OAuth refresh fails |
| 26 | `matchesContextOverflowError` | Provider-owned context-overflow matcher |
| 27 | `classifyFailoverReason` | Provider-owned failover reason classification |
| 28 | `isCacheTtlEligible` | Prompt-cache TTL policy for proxy/backhaul providers |
| 29 | `buildMissingAuthMessage` | Replace the generic missing-auth recovery message |
| 30 | `augmentModelCatalog` | Synthetic/final catalog rows appended after discovery |
| 31 | `resolveThinkingProfile` | Model-specific `/think` level set, labels, default |
| 32 | `isBinaryThinking` | On/off reasoning toggle compatibility hook |
| 33 | `supportsXHighThinking` | `xhigh` reasoning support compatibility hook |
| 34 | `resolveDefaultThinkingLevel` | Default `/think` level compatibility hook |
| 35 | `isModernModelRef` | Modern-model matcher for live/smoke selection |
| 36 | `prepareRuntimeAuth` | Exchange a credential into the runtime token just before inference |
| 37 | `resolveUsageAuth` | Resolve usage/billing credentials for `/usage` surfaces |
| 38 | `fetchUsageSnapshot` | Fetch/normalize provider usage-quota snapshots after auth |
| 39 | `createEmbeddingProvider` | Build a provider-owned embedding adapter for memory/search |
| 40 | `buildReplayPolicy` | Return a replay policy controlling transcript handling |
| 41 | `sanitizeReplayHistory` | Rewrite replay history after generic cleanup |
| 42 | `validateReplayTurns` | Final replay-turn validation/reshaping before the runner |
| 43 | `onModelSelected` | Run provider-owned post-selection side effects |

Note there is no `#19` in the source order. `normalizeModelId`, `normalizeTransport`, and `normalizeConfig` first check the matched provider plugin, then fall through other hook-capable provider plugins until one actually changes the model id or transport/config (the bundled Google config normalizer still backstops supported Google-family entries). A fully custom wire protocol is a different class of extension; these hooks run on OpenClaw's normal inference loop. `resolveUsageAuth` decides whether OpenClaw calls `fetchUsageSnapshot` or falls back to generic credential resolution: return `{ token, accountId? }` for a usage credential, `{ handled: true }` to suppress generic API-key/OAuth fallback, and `null`/`undefined` when usage auth was not handled.

### Provider Example

A provider plugin registers via `api.registerProvider(...)`, combining catalog, dynamic-model resolution, runtime-auth exchange, and usage hooks:

```ts
api.registerProvider({
  id: "example-proxy",
  label: "Example Proxy",
  auth: [],
  catalog: {
    order: "simple",
    run: async (ctx) => {
      const apiKey = ctx.resolveProviderApiKey("example-proxy").apiKey;
      if (!apiKey) {
        return null;
      }
      return {
        provider: {
          baseUrl: "https://proxy.example.com/v1",
          apiKey,
          api: "openai-completions",
          models: [{ id: "auto", name: "Auto" }],
        },
      };
    },
  },
  resolveDynamicModel: (ctx) => ({ id: ctx.modelId, name: ctx.modelId, provider: "example-proxy", api: "openai-completions", baseUrl: "https://proxy.example.com/v1", reasoning: false, input: ["text"], cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }, contextWindow: 128000, maxTokens: 8192 }),
  prepareRuntimeAuth: async (ctx) => {
    const exchanged = await exchangeToken(ctx.apiKey);
    return { apiKey: exchanged.token, baseUrl: exchanged.baseUrl, expiresAt: exchanged.expiresAt };
  },
  resolveUsageAuth: async (ctx) => {
    const auth = await ctx.resolveOAuthToken();
    return auth ? { token: auth.token } : null;
  },
  fetchUsageSnapshot: async (ctx) => {
    return await fetchExampleProxyUsage(ctx.token, ctx.timeoutMs, ctx.fetchFn);
  },
});
```

### Built-in Examples

Bundled provider plugins combine the hooks per vendor; the authoritative set lives under `extensions/`. The source groups them as: **pass-through catalog providers** (OpenRouter, Kilocode, Z.AI, xAI register `catalog` plus `resolveDynamicModel`/`prepareDynamicModel`); **OAuth and usage-endpoint providers** (GitHub Copilot, Gemini CLI, ChatGPT Codex, MiniMax, Xiaomi, z.ai pair `prepareRuntimeAuth`/`formatApiKey` with `resolveUsageAuth` + `fetchUsageSnapshot`); **replay/transcript cleanup families** (`google-gemini`, `passthrough-gemini`, `anthropic-by-model`, `hybrid-anthropic-openai` opt into transcript policy via `buildReplayPolicy`); **catalog-only providers** (`byteplus`, `cloudflare-ai-gateway`, `huggingface`, `kimi-coding`, `nvidia`, `qianfan`, `synthetic`, `together`, `venice`, `vercel-ai-gateway`, `volcengine` register just `catalog`); and **Anthropic-specific stream helpers** (`/fast` / `serviceTier`, `context1m`, beta headers live in the Anthropic plugin's public `api.ts`/`contract-api.ts` seam — `wrapAnthropicProviderStream`, `resolveAnthropicBetas`, `resolveAnthropicFastMode`, `resolveAnthropicServiceTier` — not the generic SDK).

### `api.runtime.imageGeneration`

Image generation is reached through `api.runtime.imageGeneration`. `generate(...)` generates an image using the configured image-generation provider chain; `listProviders(...)` lists available image-generation providers and their capabilities.

```ts
const result = await api.runtime.imageGeneration.generate({
  config: api.config,
  args: { prompt: "A friendly lobster mascot", size: "1024x1024" },
});

const providers = api.runtime.imageGeneration.listProviders({
  config: api.config,
});
```

## Runtime Helpers

Plugins access core helpers via `api.runtime`. **TTS** (`api.runtime.tts`): `textToSpeech` returns the core TTS payload (PCM buffer + sample rate; plugins must resample/encode) using core `messages.tts` config; `textToSpeechTelephony` is the telephony variant (OpenAI and ElevenLabs support telephony, Microsoft does not); `listVoices` is optional per provider with richer metadata (locale, gender, personality tags). Plugins register synthesis backends via `api.registerSpeechProvider(...)` — TTS policy/fallback/reply delivery stay in core; legacy Microsoft `edge` input normalizes to the `microsoft` id. The preferred ownership model is company-oriented: one vendor plugin can own text, speech, image, and future media providers.

For image/audio/video understanding, plugins register one typed provider via `api.registerMediaUnderstandingProvider(...)` (`capabilities: ["image","audio","video"]` with `describeImage`/`transcribeAudio`/`describeVideo`) rather than a generic key/value bag — core keeps orchestration/fallback/config/channel wiring; expansion stays typed. Video generation follows the same pattern: core owns the contract and runtime helper, vendor plugins register `api.registerVideoGenerationProvider(...)`, and feature/channel plugins consume `api.runtime.videoGeneration.*`. The media-understanding runtime helpers are the preferred shared surface:

```ts
const image = await api.runtime.mediaUnderstanding.describeImageFile({ filePath: "/tmp/inbound-photo.jpg", cfg: api.config, agentDir: "/tmp/agent" });
const video = await api.runtime.mediaUnderstanding.describeVideoFile({ filePath: "/tmp/inbound-video.mp4", cfg: api.config });
const { text } = await api.runtime.mediaUnderstanding.transcribeAudioFile({ filePath: "/tmp/inbound-audio.ogg", cfg: api.config, mime: "audio/ogg" });

const extraction = await api.runtime.mediaUnderstanding.extractStructuredWithModel({
  provider: "codex",
  model: "gpt-5.5",
  input: [{ type: "image", buffer: receiptImageBuffer, fileName: "receipt.png", mime: "image/png" }, { type: "text", text: "Use the printed fields as the source of truth." }],
  instructions: "Return entities and searchable tags.",
  schemaName: "example.evidence",
  jsonSchema: { type: "object", properties: { entities: { type: "array", items: { type: "string" } }, tags: { type: "array", items: { type: "string" } } } },
  cfg: api.config,
});
```

`extractStructuredWithModel(...)` is the plugin-facing seam for bounded provider-owned image-first extraction (include ≥1 image input; text is supplemental); it uses core audio config (`tools.media.audio`) and provider fallback order, returns `{ text: undefined }` when no output is produced, and `api.runtime.stt.transcribeAudioFile(...)` remains a compatibility alias.

Plugins launch background subagent runs through `api.runtime.subagent.run({ sessionKey, message, provider?, model?, deliver? })`: `provider`/`model` are optional per-run overrides (not persistent) honored only for trusted callers; for plugin-owned fallback runs operators opt in with `plugins.entries.<id>.subagent.allowModelOverride: true`, restrict to `plugins.entries.<id>.subagent.allowedModels` canonical `provider/model` targets (or `"*"`), and untrusted runs still work but override requests are rejected. Plugin-created subagent sessions are tagged with the creating plugin id; fallback `api.runtime.subagent.deleteSession(...)` deletes only those owned sessions, while arbitrary deletion needs an admin-scoped Gateway request. For web search, `api.runtime.webSearch.listProviders({ config })` and `api.runtime.webSearch.search({ config, args })` are the preferred shared surface; plugins register vendor transports via `api.registerWebSearchProvider(...)` while core keeps provider selection and credential resolution.

## Adding a New Capability

When a plugin needs behavior that does not fit the current API, do not reach in privately — add the missing capability. The recommended sequence is: (1) **define the core contract** (policy, fallback, config merge, lifecycle, channel semantics, runtime helper shape); (2) **add typed plugin registration/runtime surfaces** — extend `OpenClawPluginApi` and/or `api.runtime` with the smallest useful typed surface; (3) **wire core + channel/feature consumers** through core, not by importing a vendor implementation; (4) **register vendor implementations** against the capability; (5) **add contract coverage** so ownership stays explicit. The source points to the Capability Cookbook (`/tools/capability-cookbook`) for a file checklist and worked example.

### Capability Checklist

A new capability should usually touch these surfaces together; a missing surface usually signals an incompletely integrated capability:

- core contract types in `src/<capability>/types.ts`
- core runner/runtime helper in `src/<capability>/runtime.ts`
- plugin API registration surface in `src/plugins/types.ts`
- plugin registry wiring in `src/plugins/registry.ts`
- plugin runtime exposure in `src/plugins/runtime/*` (when feature/channel plugins consume it)
- capture/test helpers in `src/test-utils/plugin-registration.ts`
- ownership/contract assertions in `src/plugins/contracts/registry.ts`
- operator/plugin docs in `docs/`

### Capability Template

The minimal pattern wires a core contract type, a typed plugin registration, a shared runtime helper, and a contract test:

```ts
// core contract
export type VideoGenerationProviderPlugin = {
  id: string;
  label: string;
  generateVideo: (req: VideoGenerationRequest) => Promise<VideoGenerationResult>;
};

// plugin API
api.registerVideoGenerationProvider({
  id: "openai",
  label: "OpenAI",
  async generateVideo(req) {
    return await generateOpenAiVideo(req);
  },
});

// shared runtime helper for feature/channel plugins
const clip = await api.runtime.videoGeneration.generate({ prompt: "Show the robot walking through the lab.", cfg });

// contract test
expect(findVideoGenerationProviderIdsForPlugin("openai")).toEqual(["openai"]);
```

The rule stays simple: core owns the capability contract + orchestration, vendor plugins own implementations, feature/channel plugins consume runtime helpers, and contract tests keep ownership explicit.

**Source**: OpenClaw documentation — `plugins/architecture-internals` (mirror `inbox/openclaw_docs/plugins/architecture-internals.md`)
**Last Updated**: 2026-06-22
**Status**: Active
