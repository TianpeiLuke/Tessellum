---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - sdk_migration
keywords:
  - openclaw plugin sdk migration
  - plugin-sdk/compat deprecated
  - infra-runtime config-runtime extension-api
  - registerEmbeddedExtensionFactory removed
  - mutateConfigFile afterWrite
  - registerAgentToolResultMiddleware
  - talk.session talk.client realtime voice
  - deactivate gateway_stop hook
  - removal timeline deprecation window
  - suppress plugin sdk compat warning
topics:
  - OpenClaw
  - Plugin SDK Migration
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/sdk-migration
access_control_group: ["general"]
---

# OpenClaw — Migrating Plugins to the Modern Plugin SDK

## Overview

This note is the **procedure** for migrating an OpenClaw plugin off the legacy broad backwards-compatibility surfaces onto the modern plugin SDK of focused, documented imports, mirroring the `plugins/sdk-migration` source page (excluding its standalone "Import path reference" table, owned by the sibling note [oc_plugins_sdk_migration_import_paths](oc_plugins_sdk_migration_import_paths.md)). It covers what changed and why, the Talk/realtime-voice migration plan, the compatibility policy, the step-by-step migration, the catalog of active deprecations, the removal timeline, and how to temporarily suppress the warnings.

## What Is Changing

OpenClaw moved from a broad backwards-compatibility layer to a modern plugin architecture with focused, documented imports. The old system exposed four wide-open surfaces, all now **deprecated** (they still work at runtime, but new plugins must not use them and existing plugins should migrate before the next major release removes them): `openclaw/plugin-sdk/compat` (a single import re-exporting dozens of helpers); `openclaw/plugin-sdk/infra-runtime` (a broad runtime barrel mixing system events, heartbeat, delivery queues, fetch/proxy/file helpers, approval types, and unrelated utilities); `openclaw/plugin-sdk/config-runtime` (a broad config barrel carrying deprecated direct load/write helpers); and `openclaw/extension-api` (a bridge giving direct access to host-side helpers like the embedded agent runner). Additionally, `api.registerEmbeddedExtensionFactory(...)` — an embedded-runner-only bundled extension hook that could observe events such as `tool_result` — has been **removed** (legacy registrations already no longer load); use tool-result middleware instead.

A defining rule frames the migration: OpenClaw does not remove or reinterpret documented plugin behavior in the same change that introduces a replacement — breaking contract changes must first go through a compatibility adapter, diagnostics, docs, and a deprecation window (this applies to SDK imports, manifest fields, setup APIs, hooks, and runtime registration). The backwards-compatibility layer will be removed in a future major release, and plugins still importing from these surfaces will break then.

## Why This Changed

The old broad-import approach caused three problems: **slow startup** (one helper loaded dozens of unrelated modules), **circular dependencies** (broad re-exports created import cycles), and an **unclear API surface** (no way to tell stable from internal exports). The modern SDK fixes this by making each import path a small, self-contained module with a clear purpose and documented contract. Legacy provider convenience seams for bundled channels are also gone: channel-branded helper seams were private mono-repo shortcuts, not stable contracts, so plugins should use narrow generic SDK subpaths and keep provider-owned helpers inside the owning plugin's own `api.ts`/`runtime-api.ts`.

## Talk and Realtime Voice Migration Plan

Realtime voice, telephony, meeting, and browser Talk code is moving from surface-local turn bookkeeping to a shared Talk session controller exported by `openclaw/plugin-sdk/realtime-voice`, which owns the common Talk event envelope, active/capture/output-audio turn state, recent event history, and stale-turn rejection; provider plugins keep owning vendor-specific realtime sessions and surface plugins keep owning capture, playback, telephony, and meeting quirks. This migration is intentionally breaking-clean: keep the shared controller primitives in `plugin-sdk/realtime-voice`; move bundled surfaces onto it (browser relay, managed-room handoff, voice-call realtime/streaming STT, Google Meet realtime, native push-to-talk); replace old Talk RPC families with the final `talk.session.*`/`talk.client.*` API; advertise one live Talk event channel `talk.event` in Gateway `hello-ok.features.events`; and delete the old realtime HTTP endpoint and request-time instruction override path. New code should not call `createTalkEventSequencer(...)` directly unless implementing a low-level adapter or test fixture — the shared controller guarantees turn-scoped events cannot be emitted without a turn id and stale `turnEnd`/`turnCancel` calls cannot clear a newer active turn. The target public API splits into a Gateway-owned session API and a client-owned provider session API:

```typescript
// Gateway-owned Talk session API.
await gateway.request("talk.session.create", { mode: "realtime", transport: "gateway-relay", brain: "agent-consult", sessionKey: "main" });
await gateway.request("talk.session.appendAudio", { sessionId, audioBase64 });
await gateway.request("talk.session.submitToolResult", { sessionId, callId, result: { status: "working" }, options: { willContinue: true } });
await gateway.request("talk.session.close", { sessionId });

// Client-owned provider session API.
await gateway.request("talk.client.create", { mode: "realtime", transport: "webrtc", brain: "agent-consult", sessionKey: "main" });
```

Browser-owned WebRTC/provider-websocket sessions use `talk.client.create` (the browser owns provider negotiation and media transport while the Gateway owns credentials, instructions, and tool policy), whereas `talk.session.*` is the common Gateway-managed surface for gateway-relay realtime, gateway-relay transcription, and managed-room native STT/TTS sessions; legacy configs placing realtime selectors beside `talk.provider`/`talk.providers` should be repaired with `openclaw doctor --fix`. The supported `talk.session.create` combinations are intentionally small — `realtime`/`gateway-relay`/`agent-consult`, `transcription`/`gateway-relay`/`none` (streaming STT only), `stt-tts`/`managed-room`/`agent-consult` (push-to-talk; client owns capture/playback, Gateway owns turn state), and `stt-tts`/`managed-room`/`direct-tools` (admin-only first-party room). The removed-method map replaces the old `talk.realtime.*`/`talk.transcription.*`/`talk.handoff.*` families with the unified surface: `talk.realtime.session` → `talk.client.create`; `talk.realtime.toolCall` → `talk.client.toolCall`; `relayAudio` → `talk.session.appendAudio`; `talk.realtime.relayCancel` → `talk.session.cancelOutput`/`cancelTurn`; `relayToolResult` → `talk.session.submitToolResult`; `relayStop` / `talk.handoff.revoke` → `talk.session.close`; `talk.transcription.session` → `talk.session.create({ mode: "transcription" })`; `talk.handoff.create` → `talk.session.create({ transport: "managed-room" })`; `talk.handoff.join` → `talk.session.join`. The narrow control vocabulary is `appendAudio`, `startTurn`/`endTurn`, `cancelTurn`, `cancelOutput`, `submitToolResult` (with `options.willContinue` or `options.suppressResponse`), `steer`, and `close`. Core owns session semantics; provider plugins own vendor session setup; surface plugins own telephony/meeting/device adapters — do not add provider or platform special cases in core.

## Compatibility Policy

For external plugins, compatibility work follows a strict order: (1) add the new contract; (2) keep the old behavior wired through a compatibility adapter; (3) emit a diagnostic naming the old path and replacement; (4) cover both paths in tests; (5) document the deprecation and migration path; (6) remove only after the announced migration window, usually in a major release. Maintainers audit the migration queue with `pnpm plugins:boundary-report` (`:summary` for compact counts, `--owner <id>` for one plugin/owner, `:ci` to fail a CI gate on due compatibility records, cross-owner reserved SDK imports, or unused reserved subpaths). If a manifest field is still accepted, authors can keep using it until docs and diagnostics say otherwise — new code should prefer the documented replacement, but existing plugins should not break during ordinary minor releases.

## How to Migrate

The migration is a sequence of focused steps.

**Step 1 — Migrate runtime config load/write helpers.** Bundled plugins should stop calling `api.runtime.config.loadConfig()` and `api.runtime.config.writeConfigFile(...)` directly; prefer config already passed into the active call path, use `api.runtime.config.current()` for the process snapshot in long-lived handlers, and use the tool context's `ctx.getRuntimeConfig()` inside `execute` so a tool created before a config write still sees refreshed config. Config writes must go through the transactional helpers and choose an after-write policy:

```typescript
await api.runtime.config.mutateConfigFile({
  afterWrite: { mode: "auto" },
  mutate(draft) {
    draft.plugins ??= {};
  },
});
```

Use `afterWrite: { mode: "restart", reason: "..." }` when the change requires a clean gateway restart, and `afterWrite: { mode: "none", reason: "..." }` only when the caller owns the follow-up and deliberately suppresses the reload planner; mutation results include a typed `followUp` summary, and the gateway remains responsible for applying or scheduling the restart. `loadConfig`/`writeConfigFile` remain deprecated compatibility helpers and warn once with the `runtime-config-load-write` code; bundled plugins are protected by scanner guardrails (`pnpm check:deprecated-api-usage`). New code should avoid the broad `openclaw/plugin-sdk/config-runtime` barrel and use the narrow subpath for the job (config types → `config-contracts`; loaded-config lookup → `plugin-config-runtime`; snapshot reads → `runtime-config-snapshot`; writes → `config-mutation`) — see [oc_plugins_sdk_runtime_config_utilities](oc_plugins_sdk_runtime_config_utilities.md).

**Step 2 — Migrate embedded tool-result extensions to middleware.** Bundled plugins must replace embedded-runner-only `api.registerEmbeddedExtensionFactory(...)` tool-result handlers with runtime-neutral middleware, declaring every targeted runtime:

```typescript
// OpenClaw and Codex runtime dynamic tools
api.registerAgentToolResultMiddleware(async (event) => {
  return compactToolResult(event);
}, {
  runtimes: ["openclaw", "codex"],
});
```

Update the plugin manifest at the same time so `"contracts": { "agentToolResultMiddleware": ["openclaw", "codex"] }`. Installed plugins can also register tool-result middleware when explicitly enabled and declaring every targeted runtime; undeclared installed registrations are rejected.

**Step 3 — Migrate approval-native handlers to capability facts.** Approval-capable channel plugins now expose native approval through `approvalCapability.nativeRuntime` plus the shared runtime-context registry: replace `approvalCapability.handler.loadRuntime(...)` with `approvalCapability.nativeRuntime`; move approval-specific auth/delivery off legacy `plugin.auth`/`plugin.approvals` onto `approvalCapability` (`ChannelPlugin.approvals` is removed from the public contract); `plugin.auth` remains for channel login/logout only; register channel-owned runtime objects (clients, tokens, Bolt apps) through `openclaw/plugin-sdk/channel-runtime-context`; do not send plugin-owned reroute notices (core now owns routed-elsewhere notices); and pass a real `createPluginRuntime().channel` surface into `createChannelManager(...)` — partial stubs are rejected.

**Step 4 — Audit Windows wrapper fallback behavior.** If the plugin uses `openclaw/plugin-sdk/windows-spawn`, unresolved Windows `.cmd`/`.bat` wrappers now fail closed unless you explicitly pass `allowShellFallback: true` to `applyWindowsSpawnProgramPolicy({ candidate, allowShellFallback: true })`; otherwise handle the thrown error.

**Step 5 — Find deprecated imports.** Search the plugin for each deprecated surface, then fix every hit:

```bash
grep -r "plugin-sdk/compat" my-plugin/
grep -r "plugin-sdk/infra-runtime" my-plugin/
grep -r "plugin-sdk/config-runtime" my-plugin/
grep -r "openclaw/extension-api" my-plugin/
```

**Step 6 — Replace with focused imports.** Each old-surface export maps to a specific modern import path (e.g. `createChannelReplyPipeline` → `plugin-sdk/channel-reply-pipeline`, `resolveControlCommandGate` → `plugin-sdk/command-auth`); the full table is in [oc_plugins_sdk_migration_import_paths](oc_plugins_sdk_migration_import_paths.md). For host-side helpers, use the injected runtime instead of importing directly — replace `import { runEmbeddedAgent } from "openclaw/extension-api"` with `api.runtime.agent.runEmbeddedAgent(...)`; the same applies to other bridge helpers (`resolveAgentDir`, `resolveAgentWorkspaceDir`, `resolveAgentIdentity`, `resolveThinkingDefault`, `resolveAgentTimeoutMs`, `ensureAgentWorkspace` → `api.runtime.agent.*`; session store helpers → `api.runtime.agent.session.*`).

**Step 7 — Replace broad infra-runtime imports.** `openclaw/plugin-sdk/infra-runtime` still exists for external compatibility, but new code should import the focused surface it needs (system events → `system-event-runtime`; heartbeat → `heartbeat-runtime`; delivery drain → `delivery-queue-runtime`; dispatcher-aware fetch → `runtime-fetch`; proxy/guarded fetch → `fetch-runtime`; approval types → `approval-runtime`; plus dedupe, file-access, ssrf-dispatcher, error, transport-ready, secure-random, concurrency, async-lock, file-lock runtimes); bundled plugins are scanner-guarded against the broad barrel.

**Step 8 — Migrate channel route helpers.** New channel route code should use `openclaw/plugin-sdk/channel-route`: older names remain compatibility aliases (`channelRouteIdentityKey` → `channelRouteDedupeKey`, `channelRouteKey` → `channelRouteCompactKey`, `ComparableChannelTarget` → `ChannelRouteParsedTarget`, `comparableChannelTargetsMatch` → `channelRouteTargetsMatchExact`, `comparableChannelTargetsShareRoute` → `channelRouteTargetsShareConversation`). The modern helpers normalize `{ channel, to, accountId, threadId }` across approvals, reply suppression, inbound dedupe, cron delivery, and session routing; do not add new uses of `ChannelMessagingAdapter.parseExplicitTarget` or `resolveChannelRouteTargetWithParser(...)` — new plugins use `messaging.targetResolver.resolveTarget(...)`, `messaging.inferTargetChatType(...)`, and `messaging.resolveOutboundSessionRoute(...)`.

**Step 9 — Build and test** with `pnpm build` then `pnpm test -- my-plugin/`.

## Active Deprecations (Old → Replacement)

Narrower deprecations apply across the plugin SDK, provider contract, runtime surface, and manifest — each still works today but will be removed in a future major release. Imports/commands/channels (old → new): `command-auth` help builders (`buildCommandsMessage`, `buildCommandsMessagePaginated`, `buildHelpMessage`) → `openclaw/plugin-sdk/command-status`; mention gating (`resolveInboundMentionRequirement` + `shouldDropInboundForMention`) → the single `resolveInboundMentionDecision({ facts, policy })`; `plugin-sdk/channel-runtime` shim → `plugin-sdk/channel-runtime-context`, and `channelActions*` → the semantic `presentation` surface; web-search provider `tool()` factory → `createTool(...)` on the plugin; plaintext channel envelopes (`formatInboundEnvelope`, `ChannelMessageForAgent.channelEnvelope`) → `BodyForAgent` plus structured user-context blocks.

Lifecycle/subagent hooks: `api.on("deactivate", handler)` → `api.on("gateway_stop", handler)` (same shutdown-cleanup contract, only the name changes; `deactivate` remains a deprecated alias until after **2026-08-16**); `api.on("subagent_spawning", handler)` returning `threadBindingReady`/`deliveryOrigin` → let core prepare `thread: true` subagent bindings through the channel session-binding adapter, using `api.on("subagent_spawned", handler)` only for post-launch observation (`subagent_spawning` remains a deprecated compatibility surface).

Provider/runtime/manifest deprecations (old → new):

- Four discovery type aliases → their catalog-era equivalents (`ProviderDiscoveryOrder`/`Context`/`Result` → `ProviderCatalogOrder`/`Context`/`Result`, `ProviderPluginDiscovery` → `ProviderPluginCatalog`); and the static `ProviderCapabilities` bag → explicit hooks (`buildReplayPolicy`, `normalizeToolSchemas`, `wrapStreamFn`).
- Three thinking-policy hooks (`isBinaryThinking`, `supportsXHighThinking`, `resolveDefaultThinkingLevel`) → one `resolveThinkingProfile(ctx)` returning a `ProviderThinkingProfile` (canonical `id`, optional `label`, ranked levels; stale stored values downgraded by rank).
- External auth hooks without manifest declaration → declare `contracts.externalAuthProviders` **and** implement `resolveExternalAuthProfiles(...)`; manifest `providerAuthEnvVars` → mirror the lookup into `setup.providers[].envVars`.
- Three memory calls (`registerMemoryPromptSection`, `registerMemoryFlushPlan`, `registerMemoryRuntime`) → one `registerMemoryCapability(pluginId, { promptBuilder, flushPlanResolver, runtime })`; `api.registerMemoryEmbeddingProvider(...)` + `contracts.memoryEmbeddingProviders` → `api.registerEmbeddingProvider(...)` + `contracts.embeddingProviders`.
- Subagent session types `SubagentRead*` → `SubagentGetSessionMessages*` and `readSession` → `getSessionMessages`; `runtime.tasks.flow` → `runtime.tasks.managedFlows` (`runtime.tasks.flows` for DTO reads only); the removed `api.registerEmbeddedExtensionFactory(...)` → `api.registerAgentToolResultMiddleware(...)` with `contracts.agentToolResultMiddleware`; and `OpenClawSchemaType` → the canonical `OpenClawConfig` from `openclaw/plugin-sdk/config-schema`.

Extension-level deprecations inside bundled plugins under `extensions/` are tracked in their own barrels and are not listed here.

## Removal Timeline

Two milestones: **Now** — deprecated surfaces emit runtime warnings; **next major release** — they are removed and plugins still using them fail. All core plugins are already migrated; external plugins should migrate before the next major release.

## Suppressing the Warnings Temporarily

While migrating, set these environment variables to silence the deprecation warnings — a temporary escape hatch, not a permanent solution:

```bash
OPENCLAW_SUPPRESS_PLUGIN_SDK_COMPAT_WARNING=1 openclaw gateway run
OPENCLAW_SUPPRESS_EXTENSION_API_WARNING=1 openclaw gateway run
```

**Source**: OpenClaw documentation — `plugins/sdk-migration` (mirror `inbox/openclaw_docs/plugins/sdk-migration.md`)
**Last Updated**: 2026-06-22
**Status**: Active
