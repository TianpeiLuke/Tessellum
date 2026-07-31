---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - sdk_runtime
keywords:
  - api.runtime namespaces
  - openclaw plugin runtime helpers
  - runEmbeddedAgent runtime
  - api.runtime.subagent
  - api.runtime.tts mediaUnderstanding
  - api.runtime.nodes invoke
  - api.runtime.state openKeyedStore
  - tasks.managedFlows task flow
  - api.runtime.channel mentions media
topics:
  - OpenClaw
  - Plugin SDK Runtime
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/sdk-runtime
access_control_group: ["general"]
---

# OpenClaw — `api.runtime` Namespaces (Plugin Runtime Helpers)

## Overview

This note models the **runtime namespaces** of the `api.runtime` object that OpenClaw injects into every plugin during registration — the host-owned helper surface a plugin reaches for instead of importing host internals directly. It covers the 19 namespaces enumerated in the `<AccordionGroup>` of the `plugins/sdk-runtime` source page: `agent` (+ `agent.session`, `agent.defaults`), `llm`, `subagent`, `nodes`, `tasks.managedFlows`, `tts`, `mediaUnderstanding` (with the `stt` alias), `imageGeneration`, `webSearch`, `media`, `config`, `system`, `events`, `logging`, `modelAuth`, `state`, `tools`, and `channel` (`channel.media`, `channel.mentions`). The config/utility half of the same page (config loading/writes, reusable utilities, runtime-reference storage, other top-level `api` fields) lives in the sibling note `oc_plugins_sdk_runtime_config_utilities`; this note is the namespace *reference* model.

The reference is grounded entirely in the mirror page; each namespace below names its concrete methods and the operator opt-in / compatibility-alias caveats called out in the source. Plugins obtain the object via `const runtime = api.runtime;` inside `register(api) { ... }`.

## `api.runtime.agent`

Agent identity, directories, and session management. Resolution helpers: `resolveAgentDir(cfg)`, `resolveAgentWorkspaceDir(cfg)`, `resolveAgentIdentity(cfg)`, `resolveAgentTimeoutMs(cfg)`, and `ensureAgentWorkspace(cfg)`. Thinking-level helpers: `resolveThinkingDefault({ cfg, provider, model })`, `resolveThinkingPolicy({ provider, model })` (returns the provider/model's supported thinking levels plus an optional default — provider plugins own the model-specific profile through their thinking hooks, so tool plugins call this instead of duplicating provider lists), and `normalizeThinkingLevel(...)` (converts user text such as `on`, `x-high`, or `extra high` to the canonical stored level before checking it against the resolved policy).

`runEmbeddedAgent({ sessionId, runId, sessionFile, workspaceDir, prompt, timeoutMs })` is the neutral helper for starting a normal OpenClaw agent turn from plugin code; it uses the same provider/model resolution and agent-harness selection as channel-triggered replies. `runEmbeddedPiAgent(...)` remains a deprecated compatibility alias for existing plugins — new code should use `runEmbeddedAgent(...)`.

```typescript
const agentDir = api.runtime.agent.resolveAgentDir(cfg);
const result = await api.runtime.agent.runEmbeddedAgent({
  sessionId: "my-plugin:task-1",
  runId: crypto.randomUUID(),
  sessionFile: path.join(agentDir, "sessions", "my-plugin-task-1.jsonl"),
  workspaceDir: api.runtime.agent.resolveAgentWorkspaceDir(cfg),
  prompt: "Summarize the latest changes",
  timeoutMs: api.runtime.agent.resolveAgentTimeoutMs(cfg),
});
```

### `api.runtime.agent.session`

Session-store helpers that address sessions by agent/session identity, so plugins do not depend on the legacy `sessions.json` storage shape: `getSessionEntry({ agentId, sessionKey })`, `listSessionEntries({ agentId })`, `patchSessionEntry({ agentId, sessionKey, update })`, and `upsertSessionEntry(...)`. Use `preserveActivity: true` for metadata-only patches that should not refresh session activity, and `replaceEntry: true` only when the callback returns a complete entry and deleted fields must stay deleted. For transcript reads/writes, import `openclaw/plugin-sdk/session-transcript-runtime` and use `resolveSessionTranscriptIdentity(...)`, `resolveSessionTranscriptTarget(...)`, `readSessionTranscriptEvents(...)`, `appendSessionTranscriptMessageByIdentity(...)`, `publishSessionTranscriptUpdateByIdentity(...)`, or `withSessionTranscriptWriteLock(...)` with `{ agentId, sessionKey, sessionId }`; pass `sessionFile` only when adapting code that already receives an active transcript artifact. `loadSessionStore(...)`, `saveSessionStore(...)`, `updateSessionStore(...)`, and `resolveSessionFilePath(...)` are compatibility helpers for plugins that still intentionally depend on the legacy whole-store/transcript-file shape — new plugin code must not use them.

### `api.runtime.agent.defaults`

Default model and provider constants: `api.runtime.agent.defaults.model` (e.g. `"anthropic/claude-sonnet-4-6"`) and `api.runtime.agent.defaults.provider` (e.g. `"anthropic"`).

## `api.runtime.llm`

Run a host-owned text completion without importing provider internals or duplicating OpenClaw model/auth/base-URL preparation, via `api.runtime.llm.complete({ messages, purpose, maxTokens, temperature })`. The helper uses the same simple-completion preparation path as OpenClaw's built-in runtime and the host-owned runtime config snapshot; context engines receive a session-bound `llm.complete` capability so model calls use the active session's agent and do not silently fall back to the default agent. The result includes provider/model/agent attribution plus normalized token, cache, and estimated cost usage when available. Model overrides require operator opt-in via `plugins.entries.<id>.llm.allowModelOverride: true`; `plugins.entries.<id>.llm.allowedModels` restricts trusted plugins to specific canonical `provider/model` targets; cross-agent completions require `plugins.entries.<id>.llm.allowAgentIdOverride: true`.

## `api.runtime.subagent`

Launch and manage background subagent runs: `run({ sessionKey, message, provider?, model?, deliver })` returns `{ runId }`; `waitForRun({ runId, timeoutMs })` blocks for completion; `getSessionMessages({ sessionKey, limit })` reads session messages; `deleteSession({ sessionKey })` removes a session. Model overrides (`provider`/`model`) require operator opt-in via `plugins.entries.<id>.subagent.allowModelOverride: true` — untrusted plugins can still run subagents, but override requests are rejected. `deleteSession(...)` can delete sessions created by the same plugin through `api.runtime.subagent.run(...)`; deleting arbitrary user or operator sessions still requires an admin-scoped Gateway request.

```typescript
const { runId } = await api.runtime.subagent.run({
  sessionKey: "agent:main:subagent:search-helper",
  message: "Expand this query into focused follow-up searches.",
  provider: "openai", // optional override
  model: "gpt-4.1-mini", // optional override
  deliver: false,
});
const result = await api.runtime.subagent.waitForRun({ runId, timeoutMs: 30000 });
```

## `api.runtime.nodes`

List connected nodes and invoke a node-host command from Gateway-loaded plugin code or from plugin CLI commands — used when a plugin owns local work on a paired device (e.g. a browser or audio bridge on another Mac): `list({ connected })` and `invoke({ nodeId, command, params, timeoutMs })`. Inside the Gateway this runtime is in-process; in plugin CLI commands it calls the configured Gateway over RPC, so commands such as `openclaw googlemeet recover-tab` can inspect paired nodes from the terminal. Node commands still go through normal Gateway node pairing, command allowlists, plugin node-invoke policies, and node-local command handling. Plugins that expose dangerous node-host commands should register a node-invoke policy with `api.registerNodeInvokePolicy(...)`, which runs in the Gateway after command-allowlist checks and before the command is forwarded to the node, so direct `node.invoke` calls and higher-level plugin tools share the same enforcement path.

## `api.runtime.tasks.managedFlows`

Bind a Task Flow runtime to an existing OpenClaw session key or trusted tool context, then create and manage Task Flows without passing an owner on every call. Task Flow tracks durable multi-step workflow state and is *not* a scheduler — use Cron or `api.session.workflow.scheduleSessionTurn(...)` for future wakeups, then use `managedFlows` from the scheduled turn when that work needs flow state, child tasks, waits, or cancellation. Core methods: `fromToolContext(ctx)`, `createManaged({ controllerId, goal })`, `runTask({ flowId, runtime, childSessionKey, task, status, startedAt })`, and `setWaiting({ flowId, expectedRevision, currentStep, waitJson })`. Use `bindSession({ sessionKey, requesterOrigin })` when you already have a trusted OpenClaw session key from your own binding layer; do not bind from raw user input.

## `api.runtime.tts`

Text-to-speech synthesis using core `messages.tts` configuration and provider selection, returning a PCM audio buffer plus sample rate: `textToSpeech({ text, cfg })`, `textToSpeechTelephony({ text, cfg })` (telephony-optimized), and `listVoices({ provider, cfg })`.

```typescript
const clip = await api.runtime.tts.textToSpeech({
  text: "Hello from OpenClaw",
  cfg: api.config,
});
const voices = await api.runtime.tts.listVoices({
  provider: "elevenlabs",
  cfg: api.config,
});
```

## `api.runtime.mediaUnderstanding`

Image, audio, and video analysis: `describeImageFile({ filePath, cfg, agentDir })`, `transcribeAudioFile({ filePath, cfg, mime? })`, `describeVideoFile({ filePath, cfg })`, generic `runFile({ filePath, cfg })`, and `extractStructuredWithModel({ provider, model, input, instructions, schemaName, jsonSchema, cfg })` for structured extraction through a specific provider/model (include at least one image; text inputs are supplemental context). It returns `{ text: undefined }` when no output is produced (e.g. skipped input). `api.runtime.stt.transcribeAudioFile(...)` remains a compatibility alias for `api.runtime.mediaUnderstanding.transcribeAudioFile(...)`.

## `api.runtime.imageGeneration`

Image generation: `generate({ prompt, cfg })` and `listProviders({ cfg })`.

## `api.runtime.webSearch`

Web search: `listProviders({ config })` and `search({ config, args: { query, count } })`. (Note the `config` parameter name, distinct from the `cfg` used by the media/tts helpers.)

## `api.runtime.media`

Low-level media utilities: `loadWebMedia(url)`, `detectMime(buffer)`, `mediaKindFromMime("image/jpeg")` (returns e.g. `"image"`), `isVoiceCompatibleAudio(filePath)`, `getImageMetadata(filePath)`, `resizeToJpeg(buffer, { maxWidth })`, and QR helpers `renderQrTerminal(url)`, `renderQrPngBase64(url, { scale, marginModules })` (`scale` 1-12, `marginModules` 0-16), `renderQrPngDataUrl(url)`, and `writeQrPngTempFile(url, { tmpRoot, dirPrefix, fileName })`.

## `api.runtime.config`

Current runtime config snapshot and transactional config writes — prefer config already passed into the active call path; use `current()` only when the handler needs the process snapshot directly. `mutateConfigFile(...)` and `replaceConfigFile(...)` return a `followUp` value, for example `{ mode: "restart", requiresRestart: true, reason }`, which records the writer intent without taking restart control away from the gateway. (The full config-write `afterWrite` policy model is documented in `oc_plugins_sdk_runtime_config_utilities`.)

## `api.runtime.system`

System-level utilities: `enqueueSystemEvent(event)`, `requestHeartbeat({ source, intent, reason })`, `requestHeartbeatNow({ reason })` (deprecated compatibility alias), `runCommandWithTimeout(cmd, args, opts)`, and `formatNativeDependencyHint(pkg)`. `runCommandWithTimeout(...)` returns captured `stdout`/`stderr`, optional truncation counts, `code`, `signal`, `killed`, `termination`, and `noOutputTimedOut`. Timeout and no-output-timeout results report `code: 124` when the child process does not provide a non-zero exit code; non-timeout signal exits can still return `code: null`, so use `termination` and `noOutputTimedOut` to distinguish timeout reasons.

## `api.runtime.events`

Event subscriptions: `onAgentEvent((event) => { ... })` and `onSessionTranscriptUpdate((update) => { ... })`.

## `api.runtime.logging`

Logging: `shouldLogVerbose()` and `getChildLogger({ plugin }, { level })`.

## `api.runtime.modelAuth`

Model and provider auth resolution: `getApiKeyForModel({ model, cfg })` and `resolveApiKeyForProvider({ provider, cfg })`.

## `api.runtime.state`

State directory resolution and SQLite-backed keyed storage: `resolveStateDir(process.env)` and `openKeyedStore<T>({ namespace, maxEntries, defaultTtlMs })`. The keyed store exposes `register`, `registerIfAbsent`, `lookup`, `consume`, and `clear`. Keyed stores survive restarts and are isolated by the runtime-bound plugin id. `registerIfAbsent(...)` is for atomic dedupe claims: it returns `true` when the key was missing or expired and registered, or `false` when a live value already exists without overwriting its value, creation time, or TTL. Limits: `maxEntries` per namespace, 6,000 live rows per plugin, JSON values under 64KB, and optional TTL expiry. When a write would exceed the plugin row cap, the runtime may evict the oldest live rows from the namespace being written; sibling namespaces are not evicted for that write, and the write still fails if the namespace cannot free enough rows. Bundled plugins only in this release.

```typescript
const store = api.runtime.state.openKeyedStore<MyRecord>({
  namespace: "my-feature",
  maxEntries: 200,
  defaultTtlMs: 15 * 60_000,
});
const claimed = await store.registerIfAbsent("dedupe-key", { value: "first" });
```

## `api.runtime.tools`

Memory tool factories and CLI: `createMemoryGetTool(...)`, `createMemorySearchTool(...)`, and `registerMemoryCli(...)`.

## `api.runtime.channel`

Channel-specific runtime helpers, available when a channel plugin is loaded. `api.runtime.channel.media` is the preferred surface for channel media downloads and storage: `saveRemoteMedia({ url, subdir, maxBytes, filePathHint })` (when a remote URL should become OpenClaw media), `saveResponseMedia(...)` (when the plugin already fetched a `Response` with plugin-owned auth/redirect/allowlist handling), and `readRemoteMediaBuffer(...)` (only when the plugin needs raw bytes for inspection, transforms, decryption, or reupload); `fetchRemoteMedia(...)` remains a deprecated compatibility alias for `readRemoteMediaBuffer(...)`.

`api.runtime.channel.mentions` is the shared inbound mention-policy surface for bundled channel plugins that use runtime injection. Available mention helpers: `buildMentionRegexes`, `matchesMentionPatterns`, `matchesMentionWithExplicit`, `implicitMentionKindWhen`, and `resolveInboundMentionDecision`. It intentionally does not expose the older `resolveMentionGating*` compatibility helpers — prefer the normalized `{ facts, policy }` path.

```typescript
const decision = api.runtime.channel.mentions.resolveInboundMentionDecision({
  facts: {
    canDetectMention: true,
    wasMentioned: mentionMatch.matched,
    implicitMentionKinds: api.runtime.channel.mentions.implicitMentionKindWhen(
      "reply_to_bot",
      isReplyToBot,
    ),
  },
  policy: { isGroup, requireMention, allowTextCommands, hasControlCommand, commandAuthorized },
});
```

**Source**: OpenClaw documentation — `plugins/sdk-runtime` (mirror `inbox/openclaw_docs/plugins/sdk-runtime.md`, "Runtime namespaces" section)
**Last Updated**: 2026-06-22
**Status**: Active
