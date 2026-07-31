---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - sdk_migration
keywords:
  - openclaw plugin-sdk import path reference
  - legacy to narrow subpath migration
  - plugin-sdk subpath table
  - deprecated compatibility facade
  - plugin-sdk channel-outbound config-runtime
  - openclaw plugin-sdk export map
  - narrowest import that matches the job
topics:
  - OpenClaw
  - Plugin SDK Migration
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/sdk-migration
access_control_group: ["general"]
---

# OpenClaw — Plugin-SDK Migration Import Path Reference

## Overview

This note models the **Import path reference** table from the OpenClaw `plugins/sdk-migration` source page: the lookup that maps each `plugin-sdk/<subpath>` to its **Purpose** and **Key exports**, and that flags deprecated broad/compat/branded import paths with their canonical narrow replacement. It is the row-by-row companion to the migration narrative (which explains *why* the broad surfaces are deprecated); this note is the *what-imports-where* model. The source explicitly states the table is **the common migration subset, not the full SDK surface** — the compiler entrypoint inventory lives in `scripts/lib/plugin-sdk-entrypoints.json`, and package exports are generated from the public subset. Every subpath below is reproduced verbatim from the source table.

## The reference is a three-column subpath map

Each row of the source table has three columns — **Import path** (`plugin-sdk/<subpath>`), **Purpose** (one-line description), and **Key exports** (the named functions/types/values, or a deprecation pointer). A plugin imports from a subpath as `import { … } from "openclaw/plugin-sdk/<subpath>"`. Two kinds of rows exist: **live narrow subpaths** that you should import from directly, and **deprecated facades/aliases** whose Key-exports cell is a `Use plugin-sdk/<replacement>` pointer rather than a list of exports. The governing rule the page states for reading this map is: **"Use the narrowest import that matches the job. If you cannot find an export, check the source at `src/plugin-sdk/` or ask maintainers which generic contract should own it."**

## Entry, config-schema, and provider-entry subpaths

The canonical entry and schema subpaths anchor every plugin:

| Import path | Purpose | Key exports |
| --- | --- | --- |
| `plugin-sdk/plugin-entry` | Canonical plugin entry helper | `definePluginEntry` |
| `plugin-sdk/core` | Legacy umbrella re-export for channel entry definitions/builders | `defineChannelPluginEntry`, `createChatChannelPlugin` |
| `plugin-sdk/config-schema` | Root config schema export | `OpenClawSchema` |
| `plugin-sdk/provider-entry` | Single-provider entry helper | `defineSingleProviderPluginEntry` |
| `plugin-sdk/channel-core` | Focused channel entry definitions and builders | `defineChannelPluginEntry`, `defineSetupPluginEntry`, `createChatChannelPlugin`, `createChannelPluginBase` |

`plugin-sdk/core` is the *legacy umbrella* for channel entry definitions/builders — the focused `plugin-sdk/channel-core` is the narrow replacement that also adds `defineSetupPluginEntry` and `createChannelPluginBase`.

## Setup and account subpaths

Setup-time helpers split across a narrow family, with `plugin-sdk/setup-adapter-runtime` flagged as a deprecated alias of `plugin-sdk/setup-runtime`:

- `plugin-sdk/setup` — Shared setup wizard helpers (setup translator, allowlist prompts, setup status builders).
- `plugin-sdk/setup-runtime` — Setup-time runtime helpers: `createSetupTranslator`, import-safe setup patch adapters, lookup-note helpers, `promptResolvedAllowFrom`, `splitSetupEntries`, delegated setup proxies.
- `plugin-sdk/setup-adapter-runtime` — Deprecated setup adapter alias → **Use `plugin-sdk/setup-runtime`**.
- `plugin-sdk/setup-tools` — Setup tooling helpers: `formatCliCommand`, `detectBinary`, `extractArchive`, `resolveBrewExecutable`, `formatDocsLink`, `CONFIG_DIR`.
- `plugin-sdk/account-core`, `plugin-sdk/account-id` (`DEFAULT_ACCOUNT_ID`, account-id normalization), `plugin-sdk/account-resolution`, `plugin-sdk/account-helpers` — multi-account / account-id / lookup / narrow account helpers.
- `plugin-sdk/channel-setup` — Setup wizard adapters: `createOptionalChannelSetupSurface`, `createOptionalChannelSetupAdapter`, `createOptionalChannelSetupWizard`, plus `DEFAULT_ACCOUNT_ID`, `createTopLevelChannelDmPolicy`, `setSetupChannelEnabled`, `splitSetupEntries`.

## Channel subpaths and the channel-outbound consolidation

The channel family is the largest, and several legacy facades all consolidate onto `plugin-sdk/channel-outbound`:

| Import path | Purpose | Key exports |
| --- | --- | --- |
| `plugin-sdk/channel-pairing` | DM pairing primitives | `createChannelPairingController` |
| `plugin-sdk/channel-reply-pipeline` | Reply prefix, typing, and source-delivery wiring | `createChannelReplyPipeline`, `resolveChannelSourceReplyDeliveryMode` |
| `plugin-sdk/channel-config-helpers` | Config adapter factories and DM access helpers | `createHybridChannelConfigAdapter`, `resolveChannelDmAccess`, `resolveChannelDmAllowFrom`, `resolveChannelDmPolicy`, `normalizeChannelDmPolicy`, `normalizeLegacyDmAliases` |
| `plugin-sdk/channel-config-schema` | Config schema builders | Shared channel config schema primitives and the generic builder only |
| `plugin-sdk/channel-policy` | Group/DM policy resolution | `resolveChannelGroupRequireMention` |
| `plugin-sdk/channel-inbound` | Inbound receive helpers | Context building, formatting, roots, runners, prepared reply dispatch, and dispatch predicates |
| `plugin-sdk/channel-outbound` | Outbound message lifecycle helpers | Message adapters, receipts, durable send helpers, live preview/streaming helpers, reply options, lifecycle helpers, outbound identity, and payload planning |

The deprecated channel facades and their replacements:

- `plugin-sdk/channel-lifecycle`, `plugin-sdk/outbound-send-deps`, `plugin-sdk/channel-streaming`, `plugin-sdk/outbound-runtime` — Deprecated compatibility facades → **Use `plugin-sdk/channel-outbound`**.
- `plugin-sdk/direct-dm`, `plugin-sdk/direct-dm-access` — Deprecated compatibility facades → **Use `plugin-sdk/channel-inbound`**.
- `plugin-sdk/channel-runtime` — Deprecated compatibility shim (legacy channel runtime utilities only).
- `plugin-sdk/messaging-targets` — Deprecated target parsing import path → **Use `plugin-sdk/channel-targets`** for generic target parsing, `plugin-sdk/channel-route` for route comparison, and plugin-owned `messaging.targetResolver` / `messaging.resolveOutboundSessionRoute` for provider-specific target resolution.
- `plugin-sdk/channel-config-schema-legacy` — Deprecated bundled config schemas → **Use `plugin-sdk/bundled-channel-config-schema`** (which itself is for OpenClaw-maintained bundled plugins only; new plugins must define plugin-local schemas).
- `plugin-sdk/webhook-path` — Deprecated webhook path alias → **Use `plugin-sdk/webhook-ingress`**.

Live narrow channel/inbound/outbound seams also include `plugin-sdk/inbound-envelope`, `plugin-sdk/outbound-media`, `plugin-sdk/thread-bindings-runtime`, `plugin-sdk/channel-send-result`, `plugin-sdk/channel-runtime-context`, `plugin-sdk/channel-config-primitives`, `plugin-sdk/channel-config-writes`, `plugin-sdk/channel-plugin-common`, `plugin-sdk/channel-status`, `plugin-sdk/telegram-command-config`, and `plugin-sdk/agent-media-payload` (legacy media payload helpers for legacy field layouts).

## Runtime, approval, security, and infra subpaths

The runtime family separates a broad `plugin-sdk/runtime` (Runtime/logging/backup/plugin-install helpers) from many narrow runtime seams:

- `plugin-sdk/runtime-store` — Persistent plugin storage: `createPluginRuntimeStore`.
- `plugin-sdk/runtime-env` — Narrow runtime env helpers (logger/runtime env, timeout, retry, backoff).
- `plugin-sdk/plugin-runtime`, `plugin-sdk/hook-runtime`, `plugin-sdk/process-runtime`, `plugin-sdk/cli-runtime` — plugin commands/hooks/http/interactive, hook pipeline, exec, and CLI runtime helpers.
- `plugin-sdk/lazy-runtime` — Lazy runtime helpers: `createLazyRuntimeModule`, `createLazyRuntimeMethod`, `createLazyRuntimeMethodBinder`, `createLazyRuntimeNamedExport`, `createLazyRuntimeSurface`.
- `plugin-sdk/gateway-runtime` — Gateway helpers (gateway client, event-loop-ready start helper, channel-status patch helpers).
- `plugin-sdk/config-runtime` — **Deprecated config compatibility shim** → Prefer `config-contracts`, `plugin-config-runtime`, `runtime-config-snapshot`, and `config-mutation`.
- The approval family is a wide set of narrow seams: `plugin-sdk/approval-runtime`, `approval-auth-runtime`, `approval-client-runtime`, `approval-delivery-runtime`, `approval-gateway-runtime`, `approval-handler-adapter-runtime`, `approval-handler-runtime` (prefer the narrower adapter/gateway seams when they are enough), `approval-native-runtime`, `approval-reply-runtime`.
- Security/network seams: `plugin-sdk/security-runtime` (trust, DM gating, root-bounded file/path, external-content, secret-collection helpers), `plugin-sdk/ssrf-policy`, `plugin-sdk/ssrf-runtime`, `plugin-sdk/file-access-runtime`, `plugin-sdk/fetch-runtime` (`resolveFetch`, proxy/`EnvHttpProxyAgent` helpers), `plugin-sdk/host-runtime` (`normalizeHostname`, `normalizeScpRemoteHost`).
- Utility runtimes: `plugin-sdk/system-event-runtime` (`enqueueSystemEvent`, `peekSystemEventEntries`), `heartbeat-runtime`, `delivery-queue-runtime` (`drainPendingDeliveries`), `channel-activity-runtime` (`recordChannelActivity`), `dedupe-runtime`, `transport-ready-runtime` (`waitForTransportReady`), `exec-approvals-runtime` (`loadExecApprovals`, `resolveExecApprovalsFromFile`, `ExecApprovalsFile`), `collection-runtime` (`pruneMapToMaxSize`), `diagnostic-runtime` (`isDiagnosticFlagEnabled`, `isDiagnosticsEnabled`), `error-runtime` (`formatUncaughtError`, `isApprovalNotFoundError`), `retry-runtime` (`RetryConfig`, `retryAsync`), and `keyed-async-queue` (`KeyedAsyncQueue`).

## Command, reply, routing, and tool-param subpaths

- `plugin-sdk/allow-from` (`formatAllowFromLowercase`, `mapAllowlistResolutionInputs`), `plugin-sdk/command-auth` (`resolveControlCommandGate`, sender-authorization, command registry incl. dynamic argument menu formatting), `plugin-sdk/command-status` (`buildCommandsMessage`, `buildCommandsMessagePaginated`, `buildHelpMessage`).
- `plugin-sdk/secret-input`, `plugin-sdk/webhook-ingress`, `plugin-sdk/webhook-request-guards`, `plugin-sdk/webhook-targets`.
- Reply family: `plugin-sdk/reply-runtime` (inbound dispatch, heartbeat, reply planner, chunking), `reply-dispatch-runtime`, `reply-history` (`createChannelHistoryWindow`; deprecated map-helper exports such as `buildPendingHistoryContextFromMap`, `recordPendingHistoryEntry`, `clearHistoryEntriesIfEnabled`), `reply-reference` (`createReplyReferencePlanner`), `reply-chunking`, `reply-payload`.
- `plugin-sdk/session-store-runtime`, `plugin-sdk/state-paths`, `plugin-sdk/routing` (`resolveAgentRoute`, `buildAgentSessionKey`, `resolveDefaultAgentBoundAccountId`, session-key normalization), `plugin-sdk/status-helpers`, `plugin-sdk/target-resolver-runtime`, `plugin-sdk/string-normalization-runtime`, `plugin-sdk/request-url`, `plugin-sdk/run-command`, `plugin-sdk/param-readers`, `plugin-sdk/tool-payload`, `plugin-sdk/tool-send`, `plugin-sdk/temp-path`, `plugin-sdk/logging-core`, `plugin-sdk/markdown-table-runtime`, `plugin-sdk/interactive-runtime`, `plugin-sdk/allowlist-config-edit`, `plugin-sdk/group-access`, `plugin-sdk/direct-dm-guard-policy`, `plugin-sdk/extension-shared`, `plugin-sdk/web-media`, `plugin-sdk/request-url`.

## Provider and media/speech subpaths

The provider family supplies model/replay/catalog/stream/tool/usage seams:

- `plugin-sdk/provider-setup` / `provider-self-hosted` → `plugin-sdk/self-hosted-provider-setup` (focused OpenAI-compatible self-hosted provider setup helpers).
- Provider auth: `provider-auth-runtime`, `provider-auth-api-key`, `provider-auth-result` (standard OAuth auth-result builder), `provider-selection-runtime`, `provider-env-vars`.
- `plugin-sdk/provider-model-shared` — `ProviderReplayFamily`, `buildProviderReplayFamilyHooks`, `normalizeModelCompat`, shared replay-policy builders, provider-endpoint helpers, model-id normalization.
- `plugin-sdk/provider-catalog-shared` — `findCatalogTemplate`, `buildSingleProviderApiKeyCatalog`, `buildManifestModelProviderConfig`, `supportsNativeStreamingUsageCompat`, `applyProviderNativeStreamingUsageCompat`.
- `plugin-sdk/provider-stream` — `ProviderStreamFamily`, `buildProviderStreamFamilyHooks`, `composeProviderStreamWrappers`, stream wrapper types, and shared Anthropic/Bedrock/DeepSeek V4/Google/Kilocode/Moonshot/OpenAI/OpenRouter/Z.A.I/MiniMax/Copilot wrapper helpers.
- `plugin-sdk/provider-tools` (`ProviderToolCompatFamily`, `buildProviderToolCompatFamilyHooks`, DeepSeek/Gemini/OpenAI schema cleanup), `provider-usage` (`fetchClaudeUsage`, `fetchGeminiUsage`, `fetchGithubCopilotUsage`), `provider-http`, `provider-web-fetch`, `provider-web-search` (+ `provider-web-search-config-contract`, `provider-web-search-contract` with `createWebSearchProviderContractFields`, `enablePluginInConfig`, `resolveProviderWebSearchPluginConfig`), `provider-onboard`, `provider-transport-runtime`.
- Media/speech: `plugin-sdk/media-runtime`, `media-generation-runtime`, `media-understanding`, `speech`, `speech-core`, `realtime-transcription`, `realtime-voice`, `image-generation` (+ `image-generation-core`), `music-generation` (+ `music-generation-core`), `video-generation` (+ `video-generation-core`), `web-media`.
- Deprecated text facade: `plugin-sdk/text-runtime` — Deprecated broad text compatibility export → **Use `string-coerce-runtime`, `text-chunking`, `text-utility-runtime`, and `logging-core`**.

## Memory subpaths and their aliases

The bundled memory-core family carries several deprecated aliases:

- Live: `plugin-sdk/memory-core`, `memory-core-engine-runtime`, `memory-core-host-embedding-registry`, `memory-core-host-engine-foundation`, `memory-core-host-engine-embeddings`, `memory-core-host-engine-qmd`, `memory-core-host-engine-storage`, `memory-core-host-multimodal`, `memory-core-host-query`, `memory-core-host-secret`, `memory-core-host-status`, `memory-core-host-runtime-cli`, `memory-core-host-runtime-core`, `memory-core-host-runtime-files`, plus vendor-neutral aliases `memory-host-core` and `memory-host-events`, and `memory-host-markdown` / `memory-host-search`.
- Deprecated aliases: `plugin-sdk/memory-core-host-events` → **Use `plugin-sdk/memory-host-events`**; `plugin-sdk/memory-host-files` → **Use `plugin-sdk/memory-core-host-runtime-files`**; `plugin-sdk/memory-host-status` → **Use `plugin-sdk/memory-core-host-status`**.

## Zod, testing, and the subset caveat

The deprecated `plugin-sdk/zod` re-export must be replaced by importing `zod` from `zod` directly. The `plugin-sdk/testing` row is a **repo-local deprecated compatibility barrel** — use focused repo-local test subpaths such as `plugin-sdk/plugin-test-runtime`, `plugin-sdk/channel-test-helpers`, `plugin-sdk/channel-target-testing`, `plugin-sdk/test-env`, and `plugin-sdk/test-fixtures`. Two source caveats close the table: **(1)** reserved bundled-plugin helper seams have been retired from the public SDK export map except for explicitly documented compatibility facades such as the deprecated `plugin-sdk/discord` shim retained for the published `@openclaw/discord@2026.3.13` package — owner-specific helpers live inside the owning plugin package, and shared host behavior should move through generic SDK contracts such as `plugin-sdk/gateway-runtime`, `plugin-sdk/security-runtime`, and `plugin-sdk/plugin-config-runtime`. **(2)** This table is intentionally the common migration subset; the compiler entrypoint inventory lives in `scripts/lib/plugin-sdk-entrypoints.json`, and package exports are generated from the public subset.

**Source**: OpenClaw documentation — `plugins/sdk-migration` § Import path reference (mirror `inbox/openclaw_docs/plugins/sdk-migration.md`)
**Last Updated**: 2026-06-22
**Status**: Active
