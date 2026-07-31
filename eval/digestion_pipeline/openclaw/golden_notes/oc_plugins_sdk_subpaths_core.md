---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - plugin_sdk
keywords:
  - openclaw plugin sdk subpaths
  - plugin-sdk plugin-entry core
  - definePluginEntry defineSingleProviderPluginEntry
  - channel subpaths accordion
  - provider subpaths accordion
  - deprecated compatibility subpaths
  - reserved bundled plugin helper subpaths
  - plugin-sdk surface boundary report
topics:
  - OpenClaw
  - Plugin SDK Subpaths
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/sdk-subpaths
access_control_group: ["general"]
---

# OpenClaw — Plugin SDK Subpath Catalog (Core: Entry, Channel, Provider)

## Overview

This note models part 1 of the OpenClaw **plugin SDK subpath catalog**: the narrow public imports under `openclaw/plugin-sdk/` that a plugin author selects by purpose. It covers the page's intro (the public-subset model and the surface-audit commands), the `## Plugin entry` subpaths, the `### Deprecated compatibility and test helpers` and `### Reserved bundled plugin helper subpaths` notes, and the full **Channel subpaths** and **Provider subpaths** accordions — mirroring the `plugins/sdk-subpaths` source page. Part 2 (auth/security, runtime/storage, capability/testing, memory, reserved-helper subpaths, and the cross-provider usage-snapshot contract) lives in `oc_plugins_sdk_subpaths_runtime`.

## The Public Subpath Model

The plugin SDK is exposed as a set of narrow public subpaths under `openclaw/plugin-sdk/`. The generated compiler entrypoint inventory lives in `scripts/lib/plugin-sdk-entrypoints.json`; **package exports are the public subset after subtracting repo-local test/internal subpaths** listed in `scripts/lib/plugin-sdk-private-local-only-subpaths.json`. Maintainers audit the public export count with `pnpm plugin-sdk:surface` and audit active reserved helper subpaths with `pnpm plugins:boundary-report:summary`; unused reserved helper exports fail the CI report instead of staying in the public SDK as dormant compatibility debt. The authoring guide is the Plugin SDK overview (`/plugins/sdk-overview`); this page is the by-purpose import lookup that guide refers to.

## Plugin entry

The `## Plugin entry` family is the small set of top-level entry/config subpaths a plugin uses to declare itself:

| Subpath | Key exports |
| --- | --- |
| `plugin-sdk/plugin-entry` | `definePluginEntry` |
| `plugin-sdk/core` | `defineChannelPluginEntry`, `createChatChannelPlugin`, `createChannelPluginBase`, `defineSetupPluginEntry`, `buildChannelConfigSchema`, `buildJsonChannelConfigSchema` |
| `plugin-sdk/config-schema` | `OpenClawSchema` |
| `plugin-sdk/provider-entry` | `defineSingleProviderPluginEntry` |
| `plugin-sdk/migration` | Migration provider item helpers such as `createMigrationItem`, reason constants, item status markers, redaction helpers, and `summarizeMigrationItems` |
| `plugin-sdk/migration-runtime` | Runtime migration helpers such as `copyMigrationFileItem`, `withCachedMigrationConfigRuntime`, and `writeMigrationReport` |
| `plugin-sdk/health` | Doctor health-check registration, detection, repair, selection, severity, and finding types for bundled health consumers |

### Deprecated compatibility and test helpers

Deprecated subpaths stay exported for older plugins, but new code should use the focused SDK subpaths. The maintained deprecation list is `scripts/lib/plugin-sdk-deprecated-public-subpaths.json`, and **CI rejects bundled production imports from it**. Broad barrels such as `compat`, `config-types`, `infra-runtime`, `text-runtime`, and `zod` are compatibility only — import `zod` directly from `zod`. OpenClaw's Vitest-backed test-helper subpaths are **repo-local only and are no longer package exports**: `agent-runtime-test-contracts`, `channel-contract-testing`, `channel-target-testing`, `channel-test-helpers`, `plugin-test-api`, `plugin-test-contracts`, `plugin-test-runtime`, `provider-http-test-mocks`, `provider-test-contracts`, `test-env`, `test-fixtures`, `test-node-mocks`, and `testing`.

### Reserved bundled plugin helper subpaths

These subpaths are **plugin-owned compatibility surfaces for their owning bundled plugin, not general SDK APIs**: `plugin-sdk/codex-mcp-projection` and `plugin-sdk/codex-native-task-runtime`. Cross-owner extension imports are blocked by package contract guardrails. (The fuller owner/purpose table for these reserved bundled-helper subpaths is catalogued in part 2, `oc_plugins_sdk_subpaths_runtime`.)

## Channel subpaths

The **Channel subpaths** accordion is the channel-adapter public surface. The maintained import seams for new channel plugins are `plugin-sdk/channel-inbound` (receive paths) and `plugin-sdk/channel-outbound` (delivery), with many older facades kept as **deprecated compatibility** only. Selected entries (verbatim from source):

| Subpath | Key exports |
| --- | --- |
| `plugin-sdk/channel-core` | `defineChannelPluginEntry`, `defineSetupPluginEntry`, `createChatChannelPlugin`, `createChannelPluginBase` |
| `plugin-sdk/config-schema` | Root `openclaw.json` Zod schema export (`OpenClawSchema`) |
| `plugin-sdk/json-schema-runtime` | Cached JSON Schema validation helper for plugin-owned schemas |
| `plugin-sdk/channel-setup` | `createOptionalChannelSetupSurface`, `createOptionalChannelSetupAdapter`, `createOptionalChannelSetupWizard`, plus `DEFAULT_ACCOUNT_ID`, `createTopLevelChannelDmPolicy`, `setSetupChannelEnabled`, `splitSetupEntries` |
| `plugin-sdk/channel-config-helpers` | `createHybridChannelConfigAdapter`, `resolveChannelDmAccess`, `resolveChannelDmAllowFrom`, `resolveChannelDmPolicy`, `normalizeChannelDmPolicy`, `normalizeLegacyDmAliases` |
| `plugin-sdk/chat-channel-ids` | `BUNDLED_CHAT_CHANNEL_IDS`, `BUNDLED_CHAT_CHANNEL_ENVELOPE_PREFIXES`, `ChatChannelId` — canonical bundled/official chat channel ids plus formatter labels/aliases |
| `plugin-sdk/channel-ingress-runtime` | Experimental high-level channel ingress runtime resolver and route fact builders for migrated channel receive paths (prefer over assembling allowlists/projections per plugin) |
| `plugin-sdk/channel-outbound` | Message lifecycle contracts plus reply pipeline options, receipts, live preview/streaming, lifecycle helpers, outbound identity, payload planning, durable sends, and message-send context helpers |
| `plugin-sdk/channel-inbound` | Shared inbound helpers for event classification, context building, formatting, roots, debounce, mention matching, mention-policy, and inbound logging |
| `plugin-sdk/channel-pairing` | `createChannelPairingController` |
| `plugin-sdk/conversation-runtime` | Conversation/thread binding, pairing, and configured-binding helpers |
| `plugin-sdk/channel-route` | Shared route normalization, parser-driven target resolution, thread-id stringification, dedupe/compact route keys, parsed-target types, and route/target comparison helpers |
| `plugin-sdk/channel-targets` | Target parsing helpers; route comparison callers should use `plugin-sdk/channel-route` |
| `plugin-sdk/channel-secret-runtime` | Narrow secret-contract helpers such as `collectSimpleChannelFieldAssignments`, `getChannelSurface`, `pushAssignment`, and secret target types |
| `plugin-sdk/channel-plugin-common` | Shared channel plugin prelude exports |
| `plugin-sdk/interactive-runtime` | Semantic message presentation, delivery, and legacy interactive reply helpers (see Message Presentation) |

Owner-specific deprecated facades (`plugin-sdk/discord`, `plugin-sdk/telegram-account`, `plugin-sdk/zalouser`) stay exported for tracked published packages — e.g. `plugin-sdk/zalouser` is the deprecated Zalo Personal facade for published Lark/Zalo packages that still import sender command authorization, and new plugins should use `plugin-sdk/command-auth` instead. The source enumerates many other deprecated compatibility facades (`channel-reply-pipeline`, `channel-lifecycle`, `channel-message`/`channel-message-runtime`, `inbound-reply-dispatch`, `outbound-send-deps`, `outbound-runtime`, `channel-streaming`, `channel-envelope`/`channel-inbound-roots`/`channel-location`/`channel-logging`, `direct-dm`/`direct-dm-access`, `channel-pairing-paths`, `channel-reply-options-runtime`, `messaging-targets`) that all resolve to `channel-inbound`/`channel-outbound`/`channel-pairing`/`channel-targets`. **Removal plan** (verbatim): keep deprecated channel helper families through the external-plugin migration window, keep repo/bundled plugins on `channel-inbound` and `channel-outbound`, then remove the compatibility subpaths in the next major SDK cleanup — covering the old channel message/runtime, channel streaming, direct-DM access, inbound helper splinter, reply-options, and pairing-path families.

## Provider subpaths

The **Provider subpaths** accordion is the model/speech/media provider-plugin public surface. The entry point is `plugin-sdk/provider-entry` (`defineSingleProviderPluginEntry`); auth, catalog, HTTP, stream, and capability families branch from there. Selected entries (verbatim from source):

| Subpath | Key exports |
| --- | --- |
| `plugin-sdk/provider-entry` | `defineSingleProviderPluginEntry` |
| `plugin-sdk/provider-auth` | `createProviderApiKeyAuthMethod`, `ensureApiKeyFromOptionEnvOrPrompt`, `upsertAuthProfile`, `upsertApiKeyProfile`, `writeOAuthCredentials`, OpenAI Codex auth-import helpers, deprecated `resolveOpenClawAgentDir` compatibility export |
| `plugin-sdk/provider-auth-runtime` | Runtime API-key resolution helpers for provider plugins |
| `plugin-sdk/provider-oauth-runtime` | Generic provider OAuth callback types, callback-page rendering, PKCE/state helpers, authorization-input parsing, token-expiry helpers, and abort helpers |
| `plugin-sdk/provider-auth-api-key` | API-key onboarding/profile-write helpers such as `upsertApiKeyProfile` |
| `plugin-sdk/provider-env-vars` | Provider auth env-var lookup helpers |
| `plugin-sdk/provider-model-shared` | `ProviderReplayFamily`, `buildProviderReplayFamilyHooks`, `normalizeModelCompat`, shared replay-policy builders, provider-endpoint helpers, and shared model-id normalization helpers |
| `plugin-sdk/provider-catalog-live-runtime` | Live provider model catalog helpers for guarded `/models`-style discovery: `buildLiveModelProviderConfig`, `fetchLiveProviderModelRows`, `getCachedLiveProviderModelRows`, `fetchLiveProviderModelIds`, `LiveModelCatalogHttpError`, `clearLiveCatalogCacheForTests`, model-id filtering, TTL cache, and static fallback |
| `plugin-sdk/provider-catalog-shared` | `findCatalogTemplate`, `buildSingleProviderApiKeyCatalog`, `buildManifestModelProviderConfig`, `supportsNativeStreamingUsageCompat`, `applyProviderNativeStreamingUsageCompat` |
| `plugin-sdk/provider-http` | Generic provider HTTP/endpoint capability helpers, provider HTTP errors, and audio transcription multipart form helpers |
| `plugin-sdk/provider-stream` | `ProviderStreamFamily`, `buildProviderStreamFamilyHooks`, `composeProviderStreamWrappers`, stream wrapper types, plain-text tool-call compat, and shared Anthropic/Bedrock/DeepSeek V4/Google/Kilocode/Moonshot/OpenAI/OpenRouter/Z.A.I/MiniMax/Copilot wrapper helpers |
| `plugin-sdk/provider-tools` | `ProviderToolCompatFamily`, `buildProviderToolCompatFamilyHooks`, and DeepSeek/Gemini/OpenAI schema cleanup + diagnostics |
| `plugin-sdk/provider-usage` | Provider usage snapshot types, shared usage fetch helpers, and provider fetchers such as `fetchClaudeUsage` |
| `plugin-sdk/embedding-providers` | General embedding provider types and read helpers, including `EmbeddingProviderAdapter`, `getEmbeddingProvider(...)`, and `listEmbeddingProviders(...)`; plugins register through `api.registerEmbeddingProvider(...)` so manifest ownership is enforced |
| `plugin-sdk/provider-web-search` | Web-search provider registration/cache/runtime helpers |
| `plugin-sdk/provider-web-fetch` | Web-fetch provider registration/cache helpers |
| `plugin-sdk/provider-transport-runtime` | Native provider transport helpers such as guarded fetch, transport message transforms, and writable transport event streams |
| `plugin-sdk/lmstudio`, `plugin-sdk/lmstudio-runtime` | Supported LM Studio provider/runtime facades for setup, catalog discovery, runtime model preparation, local server defaults, request headers, and loaded-model helpers |
| `plugin-sdk/self-hosted-provider-setup`, `plugin-sdk/provider-setup` | Focused OpenAI-compatible self-hosted provider setup + curated local/self-hosted provider setup helpers |

The provider accordion also includes `plugin-sdk/cli-backend` (CLI backend defaults + watchdog constants), `plugin-sdk/provider-result`-style auth-result builders (`provider-auth-result`), web-search/web-fetch *contract* subpaths (`provider-web-fetch-contract`, `provider-web-search-contract`, `provider-web-search-config-contract`), `plugin-sdk/provider-onboard` (onboarding config patch helpers), `plugin-sdk/global-singleton` (process-local singleton/map/cache helpers), `plugin-sdk/group-activation` (group activation mode + command parsing), and the deprecated `plugin-sdk/provider-zai-endpoint` facade. The cross-provider **usage-snapshot reporting contract** (the "Provider usage snapshots normally report one or more quota `windows`…" paragraph that follows this accordion) is documented in part 2, `oc_plugins_sdk_subpaths_runtime`.

**Source**: OpenClaw documentation — `plugins/sdk-subpaths` (mirror `inbox/openclaw_docs/plugins/sdk-subpaths.md`)
**Last Updated**: 2026-06-22
**Status**: Active
