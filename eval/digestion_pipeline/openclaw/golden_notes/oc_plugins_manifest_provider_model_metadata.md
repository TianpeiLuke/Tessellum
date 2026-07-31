---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - manifest
keywords:
  - openclaw plugin manifest provider metadata
  - providerAuthChoices modelSupport
  - modelCatalog modelIdNormalization
  - providerEndpoints providerRequest
  - secretProviderIntegrations modelPricing
  - openclaw provider index
  - provider model metadata before runtime
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

# OpenClaw — Plugin Manifest Provider/Model Metadata

## Overview

This note models the **provider and model metadata blocks** of the native `openclaw.plugin.json` manifest — the cheap, declarative fields OpenClaw reads **before any provider runtime loads** so core can resolve, route, price, and onboard a provider plugin without importing its code. It covers the eight metadata blocks the `plugins/manifest` source assigns here — `providerAuthChoices`, `modelSupport`, `modelCatalog`, `modelIdNormalization`, `providerEndpoints`, `providerRequest`, `secretProviderIntegrations`, and `modelPricing` — plus the `modelPricing`-adjacent **OpenClaw Provider Index** fallback contract. All transport, request transforms, token refresh, credential validation, and actual model behavior stay in plugin runtime; these manifest fields are metadata only.

## providerAuthChoices

Each `providerAuthChoices` entry describes one onboarding or auth choice, read before provider runtime loads. Provider setup lists use these manifest choices, descriptor-derived setup choices, and install-catalog metadata without loading provider runtime. Fields:

| Field | Required | Type | What it means |
| --- | --- | --- | --- |
| `provider` | Yes | `string` | Provider id this choice belongs to. |
| `method` | Yes | `string` | Auth method id to dispatch to. |
| `choiceId` | Yes | `string` | Stable auth-choice id used by onboarding and CLI flows. |
| `choiceLabel` | No | `string` | User-facing label. If omitted, OpenClaw falls back to `choiceId`. |
| `choiceHint` | No | `string` | Short helper text for the picker. |
| `assistantPriority` | No | `number` | Lower values sort earlier in assistant-driven interactive pickers. |
| `assistantVisibility` | No | `"visible"` \| `"manual-only"` | Hide the choice from assistant pickers while still allowing manual CLI selection. |
| `deprecatedChoiceIds` | No | `string[]` | Legacy choice ids that should redirect users to this replacement choice. |
| `groupId` / `groupLabel` / `groupHint` | No | `string` | Optional group id, user-facing group label, and group helper text. |
| `optionKey` | No | `string` | Internal option key for simple one-flag auth flows. |
| `cliFlag` / `cliOption` / `cliDescription` | No | `string` | CLI flag name (e.g. `--openrouter-api-key`), full option shape (`--openrouter-api-key <key>`), and CLI help description. |
| `onboardingScopes` | No | `Array<"text-inference" \| "image-generation" \| "music-generation">` | Which onboarding surfaces this choice appears in; defaults to `["text-inference"]`. |

The companion top-level `providerAuthAliases` maps provider ids that should reuse another provider id for auth lookup (e.g. a coding provider sharing the base provider API key and auth profiles), and `channelEnvVars` is cheap channel env metadata OpenClaw inspects without loading plugin code. The deprecated `providerAuthEnvVars` (`Record<string, string[]>`) remains a compatibility env-metadata surface during the deprecation window; new plugins prefer `setup.providers[].envVars`.

## modelSupport

Use `modelSupport` when OpenClaw should infer your provider plugin from shorthand model ids like `gpt-5.5` or `claude-sonnet-4.6` before plugin runtime loads.

```json
{
  "modelSupport": {
    "modelPrefixes": ["gpt-", "o1", "o3", "o4"],
    "modelPatterns": ["^computer-use-preview"]
  }
}
```

Precedence OpenClaw applies: explicit `provider/model` refs use the owning `providers` manifest metadata; `modelPatterns` beat `modelPrefixes`; if one non-bundled plugin and one bundled plugin both match, the non-bundled plugin wins; remaining ambiguity is ignored until the user or config specifies a provider. Fields: `modelPrefixes` (`string[]`, matched with `startsWith` against shorthand model ids) and `modelPatterns` (`string[]`, regex sources matched against shorthand model ids after profile suffix removal). `modelPatterns` entries are compiled through `compileSafeRegex`, which rejects patterns containing nested repetition (for example `(a+)+$`); patterns that fail the safety check are silently skipped, the same as syntactically invalid regex.

## modelCatalog

`modelCatalog` is the manifest-owned source for fixed catalog rows, provider aliases, suppression rules, and discovery mode — the control-plane contract for read-only listing, onboarding, model pickers, aliases, and suppression without loading plugin runtime. Runtime refresh still belongs in provider runtime code, but the manifest tells core when runtime is required.

```json
{
  "providers": ["openai"],
  "modelCatalog": {
    "providers": {
      "openai": {
        "baseUrl": "https://api.openai.com/v1",
        "api": "openai-responses",
        "models": [
          { "id": "gpt-5.4", "name": "GPT-5.4", "input": ["text", "image"],
            "reasoning": true, "contextWindow": 256000, "maxTokens": 128000,
            "cost": { "input": 1.25, "output": 10, "cacheRead": 0.125 },
            "status": "available", "tags": ["default"] }
        ]
      }
    },
    "aliases": { "azure-openai-responses": { "provider": "openai", "api": "azure-openai-responses" } },
    "suppressions": [ { "provider": "azure-openai-responses", "model": "gpt-5.3-codex-spark", "reason": "not available on Azure OpenAI Responses" } ],
    "discovery": { "openai": "static" }
  }
}
```

Top-level fields: `providers` (`Record<string, object>` — catalog rows for owned provider ids; keys should also appear in top-level `providers`), `aliases` (provider aliases that resolve to an owned provider for catalog/suppression planning), `suppressions` (`object[]` — rows from another source this plugin suppresses), `discovery` (`Record<string, "static" \| "refreshable" \| "runtime">` — whether the catalog is read from manifest metadata, refreshed into cache, or requires runtime), and `runtimeAugment` (`boolean` — set `true` only when provider runtime must append catalog rows after manifest/config planning).

Per-provider fields: `baseUrl`, `api` (`ModelApi`), `headers` (`Record<string, string>`), and `models` (`object[]`, required; rows without an `id` are ignored). Model-row fields include `id` (provider-local id without the `provider/` prefix), `name`, per-model `api`/`baseUrl`/`headers` overrides, `input` (`Array<"text" \| "image" \| "document" \| "audio" \| "video">`), `reasoning` (`boolean`), `contextWindow`, `contextTokens` (effective runtime cap when different), `maxTokens`, `cost` (USD per million tokens, optional `tieredPricing`), `compat`, `status` (`"available"` \| `"preview"` \| `"deprecated"` \| `"disabled"`), `statusReason`, `replaces` (`string[]`), `replacedBy` (`string`), and `tags` (`string[]`). Suppression-entry fields: `provider` (must be owned or an owned alias), `model`, `reason`, plus optional guards `when.baseUrlHosts` (`string[]`) and `when.providerConfigApiIn` (`string[]`).

`aliases` participates in provider ownership lookup for model-catalog planning; alias targets must be top-level providers owned by the same plugin, and aliases do not expand unfiltered listings (broad lists emit only the owning canonical provider rows). `suppressions` replaces the old provider-runtime `suppressBuiltInModel` hook — honored only when the provider is owned or declared as a `modelCatalog.aliases` key targeting an owned provider; runtime suppression hooks are no longer called during model resolution. Discovery modes: use `static` only when manifest rows are complete enough to skip registry/runtime discovery, `refreshable` when rows are useful listable seeds/supplements but a refresh/cache can add more (not authoritative alone), and `runtime` when OpenClaw must load provider runtime to know the list. Do not put runtime-only data in `modelCatalog`.

## modelIdNormalization

Use `modelIdNormalization` for cheap provider-owned model-id cleanup that must happen before provider runtime loads, keeping aliases (short model names, provider-local legacy ids, proxy prefix rules) in the owning plugin manifest instead of core model-selection tables.

```json
{
  "providers": ["anthropic", "openrouter"],
  "modelIdNormalization": {
    "providers": {
      "anthropic": { "aliases": { "sonnet-4.6": "claude-sonnet-4-6" } },
      "openrouter": { "prefixWhenBare": "openrouter" }
    }
  }
}
```

Provider fields: `aliases` (`Record<string,string>` — case-insensitive exact model-id aliases; values are returned as written), `stripPrefixes` (`string[]` — prefixes to remove before alias lookup, useful for legacy provider/model duplication), `prefixWhenBare` (`string` — prefix to add when the normalized model id does not already contain `/`), and `prefixWhenBareAfterAliasStartsWith` (`object[]` — conditional bare-id prefix rules after alias lookup, keyed by `modelPrefix` and `prefix`).

## providerEndpoints and providerRequest

`providerEndpoints` (`object[]`) carries endpoint host/baseUrl metadata for routes that generic request policy must classify before provider runtime loads. Core owns the meaning of each `endpointClass`; plugin manifests own the host/base-URL metadata. Endpoint fields: `endpointClass` (`string` — a known core class such as `openrouter`, `moonshot-native`, or `google-vertex`), `hosts` (`string[]` — exact hostnames), `hostSuffixes` (`string[]` — host suffixes; prefix with `.` for domain suffix-only matching), `baseUrls` (`string[]` — exact normalized HTTP(S) base URLs), `googleVertexRegion` (`string` — static region for exact global hosts), and `googleVertexRegionHostSuffix` (`string` — suffix to strip from matching hosts to expose the Vertex region prefix).

`providerRequest` (`object`) is cheap provider-family and request-compatibility metadata used by generic request policy before provider runtime loads; behavior-specific payload rewriting stays in provider runtime hooks or shared provider-family helpers.

```json
{
  "providers": ["vllm"],
  "providerRequest": {
    "providers": { "vllm": { "family": "vllm", "openAICompletions": { "supportsStreamingUsage": true } } }
  }
}
```

Provider fields: `family` (`string` — family label used by generic request-compatibility decisions and diagnostics), `compatibilityFamily` (`"moonshot"` — optional provider-family compatibility bucket for shared request helpers), and `openAICompletions` (`object` — OpenAI-compatible completions request flags, currently `supportsStreamingUsage`).

## secretProviderIntegrations

Use `secretProviderIntegrations` (`Record<string, object>`) when a plugin publishes a reusable SecretRef exec provider preset. OpenClaw reads this metadata before plugin runtime loads, stores plugin ownership in `secrets.providers.<alias>.pluginIntegration`, and leaves actual secret resolution to the SecretRef runtime. Presets are exposed only for bundled plugins and installed plugins discovered from managed plugin install roots (such as git and ClawHub installs).

```json
{
  "secretProviderIntegrations": {
    "secret-store": {
      "providerAlias": "team-secrets",
      "displayName": "Team secrets",
      "source": "exec",
      "command": "${node}",
      "args": ["./bin/resolve-secrets.mjs"]
    }
  }
}
```

The map key is the integration id; if `providerAlias` is omitted, OpenClaw uses the integration id as the SecretRef provider alias (aliases must match the normal SecretRef alias pattern, e.g. `team-secrets` or `onepassword-work`). When an operator selects the preset, OpenClaw writes a `secrets.providers.<alias>` reference with `source: "exec"` and a `pluginIntegration` block recording `pluginId` and `integrationId`. At startup/reload OpenClaw resolves the provider by loading current manifest metadata, checking the owning plugin is installed and active, and materializing the exec command; disabling or removing the plugin revokes the provider for active SecretRefs. Only `source: "exec"` presets are supported, `command` must be `${node}`, and `args[0]` must be a `./` plugin-root-relative resolver script. Node options such as `--require`, `--import`, `--loader`, `--env-file`, `--eval`, and `--print` are not part of the preset contract. OpenClaw derives `trustedDirs` from the plugin root and (for `${node}` presets) the current Node executable directory; manifest-authored `trustedDirs` are ignored. Other exec options (`timeoutMs`, `maxOutputBytes`, `jsonOnly`, `env`, `passEnv`, `allowInsecurePath`) pass through to the normal SecretRef exec provider config.

## modelPricing

Use `modelPricing` (`object`) when a provider needs control-plane pricing behavior before runtime loads; the Gateway pricing cache reads this metadata without importing provider runtime code.

```json
{
  "providers": ["ollama", "openrouter"],
  "modelPricing": {
    "providers": {
      "ollama": { "external": false },
      "openrouter": { "openRouter": { "passthroughProviderModel": true }, "liteLLM": false }
    }
  }
}
```

Provider fields: `external` (`boolean` — set `false` for local/self-hosted providers that should never fetch OpenRouter or LiteLLM pricing), `openRouter` (`false \| object` — OpenRouter pricing lookup mapping; `false` disables it), and `liteLLM` (`false \| object` — LiteLLM lookup mapping; `false` disables it). Source fields inside a mapping: `provider` (`string` — external catalog provider id when it differs from the OpenClaw id, e.g. `z-ai` for a `zai` provider), `passthroughProviderModel` (`boolean` — treat slash-containing model ids as nested provider/model refs, useful for proxy providers such as OpenRouter), and `modelIdTransforms` (`"version-dots"[]` — extra external catalog model-id variants; `version-dots` tries dotted version ids like `claude-opus-4.6`).

### OpenClaw Provider Index

The OpenClaw Provider Index is OpenClaw-owned **preview** metadata for providers whose plugins may not be installed yet; it is **not part of a plugin manifest**. Plugin manifests remain the installed-plugin authority. The Provider Index is the internal fallback contract that future installable-provider and pre-install model picker surfaces consume when a provider plugin is not installed. Catalog authority order: (1) user config, (2) installed plugin manifest `modelCatalog`, (3) model catalog cache from explicit refresh, (4) OpenClaw Provider Index preview rows. The Provider Index must not contain secrets, enabled state, runtime hooks, or live account-specific model data; its preview catalogs use the same `modelCatalog` provider row shape but should stay limited to stable display metadata unless runtime adapter fields (`api`, `baseUrl`, pricing, compatibility flags) are intentionally kept aligned with the installed plugin manifest. Providers with live `/models` discovery should write refreshed rows through the explicit model catalog cache path instead of making normal listing/onboarding call provider APIs. Provider Index entries may also carry installable-plugin metadata (package name, npm install spec, expected integrity, cheap auth-choice labels) mirroring the channel catalog pattern; once the plugin is installed, its manifest wins and the Provider Index entry is ignored for that provider. Legacy top-level capability keys (`speechProviders`, `realtimeTranscriptionProviders`, `realtimeVoiceProviders`, `mediaUnderstandingProviders`, `imageGenerationProviders`, `videoGenerationProviders`, `webFetchProviders`, `webSearchProviders`) are deprecated — use `openclaw doctor --fix` to move them under `contracts`; normal manifest loading no longer treats those top-level fields as capability ownership.

**Source**: OpenClaw documentation — `plugins/manifest` (mirror `inbox/openclaw_docs/plugins/manifest.md`)
**Last Updated**: 2026-06-22
**Status**: Active
