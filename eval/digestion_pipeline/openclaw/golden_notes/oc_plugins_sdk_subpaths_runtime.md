---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - sdk
keywords:
  - openclaw plugin sdk subpaths
  - auth and security subpaths
  - runtime and storage subpaths
  - capability and testing subpaths
  - memory subpaths
  - provider-oauth-runtime pkce
  - ssrf-policy ssrf-runtime
  - provider usage snapshot windows
  - plugin-test-api createTestPluginApi
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

# OpenClaw — Plugin SDK Subpaths (Auth/Security, Runtime/Storage, Capability/Testing, Memory)

## Overview

This note models part 2 of the OpenClaw plugin SDK subpath catalog: the `openclaw/plugin-sdk/*` import families for auth and security, runtime and storage, capability and testing, memory, and the reserved bundled-helper subpaths, plus the cross-provider usage-snapshot reporting contract. It is the runtime/security half of the catalog documented on the `plugins/sdk-subpaths` source page (the entry/channel/provider half lives in `oc_plugins_sdk_subpaths_core`). Each family below is a `<Accordion>` group of `Subpath → Key exports` rows in the source; this note mirrors those rows so a plugin author can find which narrow import owns auth, OAuth/PKCE, SSRF, the runtime/storage helpers, the capability (speech/media/realtime/generation) providers, repo-local test helpers, and the memory-host surface.

## The Public Subpath Model (part 2)

The plugin SDK is exposed as narrow public subpaths under `openclaw/plugin-sdk/`. Package `exports` are the public subset after subtracting repo-local test/internal subpaths listed in `scripts/lib/plugin-sdk-private-local-only-subpaths.json`; the generated entrypoint inventory is `scripts/lib/plugin-sdk-entrypoints.json`. Several families below intentionally include both maintained focused subpaths and **deprecated compatibility facades** (e.g. `infra-runtime`, `zod`, `webhook-path`) that stay exported for older plugins but should not be used by new code. Repo-local test-helper subpaths in the Capability and testing family (`plugin-test-api`, `channel-contract-testing`, `provider-test-contracts`, `test-env`, `test-fixtures`, etc.) are **no longer package exports** — they resolve only inside the OpenClaw repo's Vitest tests.

## Auth and security subpaths

The `Auth and security` accordion catalogs command-authorization, approval-runtime, SecretRef, security-runtime, SSRF, and webhook-ingress helpers. Selected rows, copied verbatim from source:

- `plugin-sdk/command-auth` — `resolveControlCommandGate`, command registry helpers including dynamic argument menu formatting, sender-authorization helpers.
- `plugin-sdk/command-status` — Command/help message builders such as `buildCommandsMessagePaginated`.
- `plugin-sdk/approval-auth-runtime` — Approver resolution and same-chat action-auth helpers.
- `plugin-sdk/approval-client-runtime` — Native exec approval profile/filter helpers.
- `plugin-sdk/approval-delivery-runtime` — Native approval capability/delivery adapters.
- `plugin-sdk/approval-gateway-runtime` — Shared approval gateway-resolution helper.
- `plugin-sdk/approval-handler-adapter-runtime` — Lightweight native approval adapter loading helpers for hot channel entrypoints.
- `plugin-sdk/approval-handler-runtime` — Broader approval handler runtime helpers; prefer the narrower adapter/gateway seams when they are enough.
- `plugin-sdk/approval-native-runtime` — Native approval target, account-binding, route-gate, forwarding fallback, and local native exec prompt suppression helpers.
- `plugin-sdk/approval-reaction-runtime` — Hardcoded approval reaction bindings, reaction prompt payloads, reaction target stores, and compatibility export for local native exec prompt suppression.
- `plugin-sdk/approval-reply-runtime` — Exec/plugin approval reply payload helpers.
- `plugin-sdk/approval-runtime` — Exec/plugin approval payload helpers, native approval routing/runtime helpers, and structured approval display helpers such as `formatApprovalDisplayPath`.
- `plugin-sdk/reply-dedupe` — Narrow inbound reply dedupe reset helpers.
- `plugin-sdk/channel-contract-testing` — Narrow channel contract test helpers without the broad testing barrel.
- `plugin-sdk/command-auth-native` — Native command auth, dynamic argument menu formatting, and native session-target helpers.
- `plugin-sdk/command-detection` — Shared command detection helpers.
- `plugin-sdk/command-primitives-runtime` — Lightweight command text predicates for hot channel paths.
- `plugin-sdk/command-surface` — Command-body normalization and command-surface helpers.
- `plugin-sdk/allow-from` — `formatAllowFromLowercase`.
- `plugin-sdk/channel-secret-runtime` — Narrow secret-contract collection helpers for channel/plugin secrets.
- `plugin-sdk/secret-ref-runtime` — Narrow `coerceSecretRef` and SecretRef typing helpers for secret-contract/config parsing.
- `plugin-sdk/secret-provider-integration` — Type-only SecretRef provider integration manifest and preset contracts for plugins that publish external secret provider presets.
- `plugin-sdk/security-runtime` — Shared trust, DM gating, and root-bounded file/path helpers (create-only writes, atomic file replacement, symlink-parent guards, external-content, sensitive-text redaction, constant-time secret comparison, secret-collection).
- `plugin-sdk/ssrf-policy` — Host allowlist and private-network SSRF policy helpers.
- `plugin-sdk/ssrf-dispatcher` — Narrow pinned-dispatcher helpers without the broad infra runtime surface.
- `plugin-sdk/ssrf-runtime` — Pinned-dispatcher, SSRF-guarded fetch, SSRF error, and SSRF policy helpers.
- `plugin-sdk/secret-input` — Secret input parsing.
- `plugin-sdk/webhook-ingress` — Webhook request/target helpers and raw websocket/body coercion.
- `plugin-sdk/webhook-request-guards` — Request body size/timeout helpers.

OAuth/PKCE for providers lives in the Provider family (`plugin-sdk/provider-oauth-runtime`, catalogued in part 1) but is exercised through these auth subpaths; the SSRF surface here (`ssrf-policy` / `ssrf-dispatcher` / `ssrf-runtime`) is the public face of OpenClaw's server-side-request-forgery defense.

## Runtime and storage subpaths

The largest accordion catalogs the broad runtime helpers, config-mutation, session/transcript stores, SQLite, routing, reply runtime, tool-payload, ACP runtime, and a long tail of narrow `*-runtime` helpers. Selected rows, copied verbatim:

- `plugin-sdk/runtime` — Broad runtime/logging/backup/plugin-install helpers.
- `plugin-sdk/runtime-env` — Narrow runtime env, logger, timeout, retry, and backoff helpers.
- `plugin-sdk/agent-harness-task-runtime` — Generic task lifecycle and completion delivery helpers for harness-backed agents using a host-issued task scope.
- `plugin-sdk/codex-mcp-projection` — Reserved bundled Codex helper for projecting user MCP server config into Codex thread config; not for third-party plugins.
- `plugin-sdk/codex-native-task-runtime` — Private bundled Codex helper for native task mirror/runtime wiring; not for third-party plugins.
- `plugin-sdk/runtime-store` — `createPluginRuntimeStore`.
- `plugin-sdk/plugin-runtime` — Shared plugin command/hook/http/interactive helpers.
- `plugin-sdk/hook-runtime` — Shared webhook/internal hook pipeline helpers.
- `plugin-sdk/lazy-runtime` — Lazy runtime helpers such as `createLazyRuntimeModule`, `createLazyRuntimeMethod`, and `createLazyRuntimeSurface`.
- `plugin-sdk/process-runtime` — Process exec helpers.
- `plugin-sdk/cli-runtime` — CLI formatting, wait, version, argument-invocation, and lazy command-group helpers.
- `plugin-sdk/gateway-method-runtime` — Reserved Gateway method dispatch helper for plugin HTTP routes declaring `contracts.gatewayMethodDispatch: ["authenticated-request"]`.
- `plugin-sdk/gateway-runtime` — Gateway client, event-loop-ready client start helper, gateway CLI RPC, gateway protocol errors, and channel-status patch helpers.
- `plugin-sdk/config-contracts` — Focused type-only config surface for plugin config shapes such as `OpenClawConfig` and channel/provider config types.
- `plugin-sdk/plugin-config-runtime` — Runtime plugin-config lookup helpers such as `requireRuntimeConfig`, `resolvePluginConfigObject`, and `resolveLivePluginConfigObject`.
- `plugin-sdk/config-mutation` — Transactional config mutation helpers such as `mutateConfigFile`, `replaceConfigFile`, and `logConfigUpdated`.
- `plugin-sdk/runtime-config-snapshot` — Current process config snapshot helpers such as `getRuntimeConfig`, `getRuntimeConfigSnapshot`, and test snapshot setters.
- `plugin-sdk/session-store-runtime` — Session workflow helpers (`getSessionEntry`, `listSessionEntries`, `patchSessionEntry`, `upsertSessionEntry`), legacy session store path/session-key helpers, updated-at reads, and transition-only whole-store/file-path compatibility helpers.
- `plugin-sdk/session-transcript-runtime` — Transcript identity, scoped target/read/write helpers, update publishing, write locks, and transcript memory hit keys.
- `plugin-sdk/sqlite-runtime` — Focused SQLite agent-schema, path, and transaction helpers for first-party runtime.
- `plugin-sdk/cron-store-runtime` — Cron store path/load/save helpers.
- `plugin-sdk/plugin-state-runtime` — Plugin sidecar SQLite keyed-state types plus centralized connection pragma and WAL maintenance setup for plugin-owned databases.
- `plugin-sdk/routing` — Route/session-key/account binding helpers such as `resolveAgentRoute`, `buildAgentSessionKey`, and `resolveDefaultAgentBoundAccountId`.
- `plugin-sdk/run-command` — Timed command runner with normalized stdout/stderr results.
- `plugin-sdk/tool-plugin` — Define a simple typed agent-tool plugin and expose static metadata for manifest generation.
- `plugin-sdk/tool-payload` — Extract normalized payloads from tool result objects.
- `plugin-sdk/tool-send` — Extract canonical send target fields from tool args.
- `plugin-sdk/sandbox` — Sandbox backend types and SSH/OpenShell command helpers, including fail-fast exec command preflight.
- `plugin-sdk/file-lock` — Re-entrant file-lock helpers.
- `plugin-sdk/acp-runtime` — ACP runtime/session and reply-dispatch helpers (with `acp-runtime-backend` and read-only `acp-binding-resolve-runtime` variants).
- `plugin-sdk/concurrency-runtime` — Bounded async task concurrency helper.
- `plugin-sdk/delivery-queue-runtime` — Outbound pending-delivery drain helper.
- `plugin-sdk/secure-random-runtime` — Secure token/UUID helpers.
- `plugin-sdk/exec-approvals-runtime` — Exec approval policy file helpers without the broad infra-runtime barrel.
- `plugin-sdk/infra-runtime` — Deprecated compatibility shim; use the focused runtime subpaths above.
- `plugin-sdk/fetch-runtime` — Wrapped fetch, proxy, EnvHttpProxyAgent option, and pinned lookup helpers.
- `plugin-sdk/session-binding-runtime` — Current conversation binding state without configured binding routing or pairing stores.
- `plugin-sdk/agent-runtime` — Agent dir/identity/workspace helpers, including `resolveAgentDir`, `resolveDefaultAgentDir`, and deprecated `resolveOpenClawAgentDir`.
- `plugin-sdk/keyed-async-queue` — `KeyedAsyncQueue`.

The family also exposes `plugin-sdk/agent-harness` (experimental trusted-plugin surface for low-level agent harnesses: harness types, active-run steer/abort, tool-bridge, tool-policy, terminal-outcome, and attempt-result helpers) plus narrow helpers such as `param-readers`, `heartbeat-runtime`, `error-runtime`, and `runtime-fetch`. Source notes a few rows (`approval-reaction-runtime`, `approval-runtime`, `session-store-runtime`, `sqlite-runtime`) appear in both this and the Auth/security view.

## Capability and testing subpaths

This accordion catalogs media, text-chunking, speech, realtime, generation (image/music/video), transcripts, webhook-targets, and the repo-local test-helper subpaths. Selected rows, copied verbatim:

- `plugin-sdk/media-runtime` — Shared media fetch/transform/store helpers including `saveRemoteMedia`, `saveResponseMedia`, `readRemoteMediaBuffer`, and deprecated `fetchRemoteMedia`; prefer store helpers before buffer reads when a URL should become OpenClaw media.
- `plugin-sdk/media-store` — Narrow media store helpers such as `saveMediaBuffer` and `saveMediaStream`.
- `plugin-sdk/media-understanding` — Media understanding provider types plus provider-facing image/audio/structured-extraction helper exports.
- `plugin-sdk/speech` — Speech provider types plus provider-facing directive, registry, validation, OpenAI-compatible TTS builder, and speech helper exports.
- `plugin-sdk/speech-core` — Shared speech provider types, registry, directive, normalization, and speech helper exports.
- `plugin-sdk/realtime-transcription` — Realtime transcription provider types, registry helpers, and shared WebSocket session helper.
- `plugin-sdk/realtime-bootstrap-context` — Realtime profile bootstrap helper for bounded `IDENTITY.md`, `USER.md`, and `SOUL.md` context injection.
- `plugin-sdk/realtime-voice` — Realtime voice provider types, registry helpers, and shared realtime voice behavior helpers, including output activity tracking.
- `plugin-sdk/image-generation` — Image generation provider types plus image asset/data URL helpers and the OpenAI-compatible image provider builder.
- `plugin-sdk/music-generation` — Music generation provider/request/result types.
- `plugin-sdk/video-generation` — Video generation provider/request/result types.
- `plugin-sdk/transcripts` — Shared transcripts source provider types, registry helpers, session descriptors, and utterance metadata.
- `plugin-sdk/webhook-targets` — Webhook target registry and route-install helpers.
- `plugin-sdk/webhook-path` — Deprecated compatibility alias; use `plugin-sdk/webhook-ingress`.
- `plugin-sdk/zod` — Deprecated compatibility re-export; import `zod` from `zod` directly.
- `plugin-sdk/testing` — Repo-local deprecated compatibility barrel for legacy OpenClaw tests. New repo tests should import focused local test subpaths such as `plugin-sdk/agent-runtime-test-contracts`, `plugin-sdk/plugin-test-runtime`, `plugin-sdk/channel-test-helpers`, `plugin-sdk/test-env`, or `plugin-sdk/test-fixtures` instead.
- `plugin-sdk/plugin-test-api` — Repo-local minimal `createTestPluginApi` helper for direct plugin registration unit tests without importing repo test helper bridges.
- `plugin-sdk/agent-runtime-test-contracts` — Repo-local native agent-runtime adapter contract fixtures (auth, delivery, fallback, tool-hook, prompt-overlay, schema, transcript projection).
- `plugin-sdk/channel-test-helpers` — Repo-local channel-oriented test helpers for actions/setup/status contracts, startup lifecycle, runtime mocks, outbound delivery, and hook registration.
- `plugin-sdk/provider-test-contracts` — Repo-local provider runtime, auth, discovery, onboard, catalog, media-capability, replay-policy, realtime-STT, web-search/fetch, and stream contract helpers.
- `plugin-sdk/provider-http-test-mocks` — Repo-local opt-in Vitest HTTP/auth mocks for provider tests exercising `plugin-sdk/provider-http`.
- `plugin-sdk/test-fixtures` — Repo-local generic CLI runtime capture, sandbox context, agent-message, module reload, bundled plugin path, chunking, auth-token, and typed-case fixtures.
- `plugin-sdk/test-node-mocks` — Repo-local Node builtin mock helpers for use inside Vitest `vi.mock("node:*")` factories.

## Memory subpaths

The `Memory` accordion catalogs the bundled memory-core surface and the memory-host engine/embeddings/storage/query/secret/status/runtime helpers (with several vendor-neutral aliases and deprecated compatibility aliases). Selected rows, copied verbatim:

- `plugin-sdk/memory-core` — Bundled memory-core helper surface for manager/config/file/CLI helpers.
- `plugin-sdk/memory-core-engine-runtime` — Memory index/search runtime facade.
- `plugin-sdk/memory-core-host-embedding-registry` — Lightweight memory embedding provider registry helpers.
- `plugin-sdk/memory-core-host-engine-foundation` — Memory host foundation engine exports.
- `plugin-sdk/memory-core-host-engine-embeddings` — Memory host embedding contracts, registry access, local provider, and generic batch/remote helpers. `registerMemoryEmbeddingProvider` on this surface is deprecated; use the generic embedding provider API for new providers.
- `plugin-sdk/memory-core-host-engine-storage` — Memory host storage engine exports.
- `plugin-sdk/memory-core-host-query` — Memory host query helpers.
- `plugin-sdk/memory-core-host-secret` — Memory host secret helpers.
- `plugin-sdk/memory-host-core` — Vendor-neutral alias for memory host core runtime helpers.
- `plugin-sdk/memory-host-events` — Vendor-neutral alias for memory host event journal helpers.
- `plugin-sdk/memory-host-markdown` — Shared managed-markdown helpers for memory-adjacent plugins.
- `plugin-sdk/memory-host-search` — Active memory runtime facade for search-manager access.

`plugin-sdk/memory-core-host-events`, `plugin-sdk/memory-host-files`, and `plugin-sdk/memory-host-status` are deprecated compatibility aliases pointing at `plugin-sdk/memory-host-events`, `plugin-sdk/memory-core-host-runtime-files`, and `plugin-sdk/memory-core-host-status` respectively.

## Reserved bundled-helper subpaths

Reserved bundled-helper SDK subpaths are narrow owner-specific surfaces for bundled plugin code. They are tracked in the SDK inventory so package builds and aliasing stay deterministic, but they are not general plugin authoring APIs. New reusable host contracts should use generic SDK subpaths such as `plugin-sdk/gateway-runtime`, `plugin-sdk/security-runtime`, and `plugin-sdk/plugin-config-runtime`. The two reserved subpaths are:

- `plugin-sdk/codex-mcp-projection` — Bundled Codex plugin helper for projecting user MCP server config into Codex app-server thread config.
- `plugin-sdk/codex-native-task-runtime` — Bundled Codex plugin helper for mirroring Codex app-server native subagents into OpenClaw task state.

Cross-owner extension imports of these reserved subpaths are blocked by package contract guardrails.

## Provider usage-snapshot reporting contract

The paragraph following the Provider accordion states the cross-provider usage-snapshot contract that the `plugin-sdk/provider-usage` family must satisfy. Provider usage snapshots normally report one or more quota `windows`, each with a label, percent used, and optional reset time. Providers that expose balance or account-state text instead of resettable quota windows should return `summary` with an empty `windows` array rather than fabricating percentages. OpenClaw displays that `summary` text in status output; use `error` only when the usage endpoint failed or returned no usable usage data.

**Source**: OpenClaw documentation — `plugins/sdk-subpaths` (mirror `inbox/openclaw_docs/plugins/sdk-subpaths.md`)
**Last Updated**: 2026-06-22
**Status**: Active
