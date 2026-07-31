---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - registration_api
keywords:
  - openclaw plugin registration api
  - openclawpluginapi register
  - registerprovider registerchannel registertool
  - host hooks workflow plugins
  - gateway discovery registration
  - cli backend registration
  - exclusive memory slots
  - hook decision semantics
  - api object fields runtime
topics:
  - OpenClaw
  - Plugin SDK
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/plugins/sdk-overview
access_control_group: ["general"]
---

# OpenClaw — Plugin SDK Registration API (`OpenClawPluginApi`)

## Overview

This note models the **Registration API** half of the OpenClaw plugin SDK overview page (`plugins/sdk-overview`): the `register(api)` callback receives an `OpenClawPluginApi` object, and this catalogs every method on it plus its plain data fields. It mirrors the source's `## Registration API` section and all sub-method groups (capability, tools/commands, infrastructure, host hooks, gateway discovery, CLI registration and backend, exclusive slots, deprecated memory adapters, events/lifecycle, hook decision semantics, `api` object fields). The import / subpath / internal-module half is in [oc_plugins_sdk_overview_imports](oc_plugins_sdk_overview_imports.md).

## Capability registration

A plugin registers a capability by calling the matching `api.register*` method inside `register(api)`; each maps to a host capability:

| Method | What it registers |
| --- | --- |
| `api.registerProvider(...)` | Text inference (LLM) |
| `api.registerAgentHarness(...)` | Experimental low-level agent executor |
| `api.registerCliBackend(...)` | Local CLI inference backend |
| `api.registerChannel(...)` | Messaging channel |
| `api.registerEmbeddingProvider(...)` | Reusable vector embedding provider |
| `api.registerSpeechProvider(...)` | Text-to-speech / STT synthesis |
| `api.registerRealtimeTranscriptionProvider(...)` | Streaming realtime transcription |
| `api.registerRealtimeVoiceProvider(...)` | Duplex realtime voice sessions |
| `api.registerMediaUnderstandingProvider(...)` | Image/audio/video analysis |
| `api.registerImageGenerationProvider(...)` | Image generation |
| `api.registerMusicGenerationProvider(...)` | Music generation |
| `api.registerVideoGenerationProvider(...)` | Video generation |
| `api.registerWebFetchProvider(...)` | Web fetch / scrape provider |
| `api.registerWebSearchProvider(...)` | Web search |

Providers registered with `api.registerEmbeddingProvider(...)` must also be listed in `contracts.embeddingProviders` in the manifest — the generic reusable-vector surface memory search can consume; the older `api.registerMemoryEmbeddingProvider(...)` / `contracts.memoryEmbeddingProviders` seam is deprecated compatibility. Memory providers exposing a runtime `batchEmbed(...)` stay on per-file batching unless their runtime sets `sourceWideBatchEmbed: true`, which lets the host submit chunks from multiple dirty files and enabled sources in one `batchEmbed(...)` call up to host batch limits. JSONL batch adapters must split jobs before both upload-size and request-count caps; the provider returns one embedding per chunk in `batch.chunks` order; omit the flag for file-local batches or unpreserved ordering.

## Tools and commands

Use `defineToolPlugin` (see [oc_plugins_sdk_entrypoints](oc_plugins_sdk_entrypoints.md)) for tool-only plugins with fixed names, or `api.registerTool(...)` directly for mixed plugins or dynamic registration:

| Method | What it registers |
| --- | --- |
| `api.registerTool(tool, opts?)` | Agent tool (required or `{ optional: true }`) |
| `api.registerCommand(def)` | Custom command (bypasses the LLM) |

Plugin commands can set `agentPromptGuidance` for a short, command-owned routing hint; keep that text about the command itself, not provider- or plugin-specific policy. Guidance entries are legacy strings (every surface) or structured entries with a scoped `surfaces` array:

```ts
agentPromptGuidance: [
  "Global command hint.",
  { text: "Only show this in the main OpenClaw prompt.", surfaces: ["openclaw_main"] },
];
```

Structured `surfaces` may include `openclaw_main`, `codex_app_server`, `cli_backend`, `acp_backend`, or `subagent`; `pi_main` remains a deprecated alias for `openclaw_main`. Omit `surfaces` for intentional all-surface guidance; an empty `surfaces` array is rejected so accidental scope loss does not become global prompt text. Native Codex app-server developer instructions are stricter: only guidance scoped to `codex_app_server` is promoted into that higher-priority lane, while legacy string and unscoped structured guidance stay available to non-Codex surfaces.

## Infrastructure

Infrastructure methods register gateway/runtime plumbing — HTTP/RPC endpoints, services, hooks, and tool-result/memory middleware:

| Method | What it registers |
| --- | --- |
| `api.registerHook(events, handler, opts?)` | Event hook |
| `api.registerHttpRoute(params)` | Gateway HTTP endpoint |
| `api.registerGatewayMethod(name, handler)` | Gateway RPC method |
| `api.registerGatewayDiscoveryService(service)` | Local Gateway discovery advertiser |
| `api.registerCli(registrar, opts?)` | CLI subcommand |
| `api.registerNodeCliFeature(registrar, opts?)` | Node feature CLI under `openclaw nodes` |
| `api.registerService(service)` | Background service |
| `api.registerInteractiveHandler(registration)` | Interactive handler |
| `api.registerAgentToolResultMiddleware(...)` | Runtime tool-result middleware |
| `api.registerMemoryPromptSupplement(builder)` | Additive memory-adjacent prompt section |
| `api.registerMemoryCorpusSupplement(adapter)` | Additive memory search/read corpus |

Tool-result middleware (`api.registerAgentToolResultMiddleware(...)`) is the trusted runtime-neutral seam for async output reducers (such as tokenjuice) that rewrite a tool result after execution, before the runtime feeds it back to the model. Only bundled plugins and explicitly enabled installed plugins with matching manifest contracts may use it: plugins must declare `contracts.agentToolResultMiddleware` per targeted runtime (e.g. `["openclaw", "codex"]`); the old embedded-runner-only path is removed.

## Host hooks for workflow plugins

Host hooks are the SDK seams for plugins that participate in the host lifecycle, not only adding a provider, channel, or tool. They are generic contracts usable by Plan Mode, approval workflows, workspace policy gates, monitors, setup wizards, and UI companions.

| Method | Contract it owns |
| --- | --- |
| `api.session.state.registerSessionExtension(...)` | Plugin-owned, JSON-compatible session state projected through Gateway sessions |
| `api.session.workflow.enqueueNextTurnInjection(...)` | Durable exactly-once context injected into the next agent turn for one session |
| `api.registerTrustedToolPolicy(...)` | Manifest-gated trusted pre-plugin tool policy that can block or rewrite tool params |
| `api.registerToolMetadata(...)` | Tool catalog display metadata without changing the tool implementation |
| `api.registerCommand(...)` | Scoped plugin commands; results can set `continueAgent: true`; Discord native commands support `descriptionLocalizations` |
| `api.session.controls.registerControlUiDescriptor(...)` | Control UI contribution descriptors for session, tool, run, or settings surfaces |
| `api.lifecycle.registerRuntimeLifecycle(...)` | Cleanup callbacks for plugin-owned runtime resources on reset/delete/reload paths |
| `api.agent.events.registerAgentEventSubscription(...)` | Sanitized event subscriptions for workflow state and monitors |
| `api.runContext.setRunContext(...)` / `getRunContext(...)` / `clearRunContext(...)` | Per-run plugin scratch state cleared on terminal run lifecycle |
| `api.session.workflow.registerSessionSchedulerJob(...)` | Cleanup metadata for plugin-owned scheduler jobs; does not schedule work or create task records |
| `api.session.workflow.sendSessionAttachment(...)` | Bundled-only host-mediated file attachment delivery to the active direct-outbound session route |
| `api.session.workflow.scheduleSessionTurn(...)` / `unscheduleSessionTurnsByTag(...)` | Bundled-only Cron-backed scheduled session turns plus tag-based cleanup |
| `api.session.controls.registerSessionAction(...)` | Typed session actions clients can dispatch through the Gateway |

New code should use the grouped namespaces above (plus `api.agent.events.emitAgentEvent(...)`); the equivalent flat methods (`api.registerSessionExtension`, `api.enqueueNextTurnInjection`, `api.registerControlUiDescriptor`, `api.registerRuntimeLifecycle`, `api.registerAgentEventSubscription`, `api.emitAgentEvent`, `api.setRunContext`/`getRunContext`/`clearRunContext`, `api.registerSessionSchedulerJob`, `api.registerSessionAction`, `api.sendSessionAttachment`, `api.scheduleSessionTurn`, `api.unscheduleSessionTurnsByTag`) remain only as deprecated compatibility aliases. `scheduleSessionTurn(...)` is a session-scoped convenience over the Gateway Cron scheduler: Cron owns timing and creates the task record; the SDK only constrains target session, plugin-owned naming, and cleanup — use `api.runtime.tasks.managedFlows` inside the turn for durable multi-step Task Flow.

The contracts intentionally split authority. External plugins can own session extensions, UI descriptors, commands, tool metadata, next-turn injections, and normal hooks. Trusted tool policies run before `before_tool_call` hooks and are host-trusted: bundled policies run first; installed-plugin policies require explicit enablement plus local ids in `contracts.trustedToolPolicies`, run next in plugin-load order, with ids scoped to the registering plugin. Reserved command ownership is bundled-only (external plugins use their own names/aliases), and `allowPromptInjection=false` disables prompt-mutating hooks (`agent_turn_prepare`, `before_prompt_build`, `heartbeat_prompt_contribution`, prompt fields from legacy `before_agent_start`, and `enqueueNextTurnInjection`). Reserved core admin namespaces (`config.*`, `exec.approvals.*`, `wizard.*`, `update.*`) always stay `operator.admin` even when a plugin assigns a narrower gateway scope; prefer plugin-specific prefixes.

## Gateway discovery, CLI registration, and CLI backend

`api.registerGatewayDiscoveryService(...)` lets a plugin advertise the active Gateway on a local discovery transport such as mDNS/Bonjour; OpenClaw calls it during Gateway startup when local discovery is enabled, passes the current Gateway ports and non-secret TXT hint data, and calls the returned `stop` handler at shutdown. Discovery is a routing hint only — plugins must not treat advertised TXT values as secrets or auth; Gateway auth and TLS pinning own trust.

```typescript
api.registerGatewayDiscoveryService({
  id: "my-discovery",
  async advertise(ctx) {
    const handle = await startMyAdvertiser({
      gatewayPort: ctx.gatewayPort,
      tls: ctx.gatewayTlsEnabled,
      displayName: ctx.machineDisplayName,
    });
    return { stop: () => handle.stop() };
  },
});
```

`api.registerCli(registrar, opts?)` accepts three kinds of command metadata: `commands` (explicit names owned by the registrar), `descriptors` (parse-time descriptors for CLI help, routing, and lazy plugin CLI registration), and `parentPath` (optional parent path for nested groups, such as `["nodes"]`; nested commands receive the resolved parent as `program`). For paired-node features prefer `api.registerNodeCliFeature(registrar, opts?)`, a wrapper around `api.registerCli(..., { parentPath: ["nodes"] })` that makes commands such as `openclaw nodes canvas` explicit plugin-owned node features. To keep a command lazy-loaded in the root CLI path, provide `descriptors` covering every top-level root the registrar exposes; use `commands` alone only without lazy root registration (the eager path installs no parse-time placeholders).

```typescript
api.registerCli(
  async ({ program }) => {
    const { registerMatrixCli } = await import("./src/cli.js");
    registerMatrixCli({ program });
  },
  {
    descriptors: [
      {
        name: "matrix",
        description: "Manage Matrix accounts, verification, devices, and profile state",
        hasSubcommands: true,
      },
    ],
  },
);
```

`api.registerCliBackend(...)` lets a plugin own the default config for a local AI CLI backend such as `claude-cli` or `my-cli`. The backend `id` becomes the provider prefix in model refs like `my-cli/gpt-5`; `config` uses the `agents.defaults.cliBackends.<id>` shape, and user config still wins since OpenClaw merges that key over the plugin default before running the CLI. Use `normalizeConfig` for post-merge compatibility rewrites (e.g. old flag shapes) and `resolveExecutionArgs` for request-scoped argv rewrites in the CLI dialect — that hook receives `ctx.executionMode`, where `"side-question"` adds backend-native isolation flags for ephemeral `/btw` calls; if those flags disable native tools for an always-on CLI, declare `sideQuestionToolMode: "disabled"`.

## Exclusive slots and deprecated memory embedding adapters

Exclusive-slot methods register capabilities of which only one is active:

| Method | What it registers |
| --- | --- |
| `api.registerContextEngine(id, factory)` | Context engine (one active at a time); lifecycle callbacks receive `runtimeSettings` when the host can provide model/provider/mode diagnostics, and older strict engines are retried without that key |
| `api.registerMemoryCapability(capability)` | Unified memory capability |
| `api.registerMemoryPromptSection(builder)` | Memory prompt section builder |
| `api.registerMemoryFlushPlan(resolver)` | Memory flush plan resolver |
| `api.registerMemoryRuntime(runtime)` | Memory runtime adapter |

`registerMemoryCapability` is the preferred exclusive memory-plugin API and may also expose `publicArtifacts.listArtifacts(...)` so companion plugins consume exported memory artifacts through `openclaw/plugin-sdk/memory-host-core` instead of reaching into a memory plugin's private layout; `registerMemoryPromptSection`, `registerMemoryFlushPlan`, and `registerMemoryRuntime` are legacy-compatible exclusive memory-plugin APIs, and `MemoryFlushPlan.model` can pin the flush turn to an exact `provider/model` ref (such as `ollama/qwen3:8b`) without inheriting the active fallback chain. The deprecated `api.registerMemoryEmbeddingProvider(adapter)` registers a memory embedding adapter for the active plugin; new providers should use `api.registerEmbeddingProvider(...)` and `contracts.embeddingProviders`. Existing memory-specific providers keep working during migration, but plugin inspection reports this as compatibility debt.


## Events, lifecycle, and hook decision semantics

| Method | What it does |
| --- | --- |
| `api.on(hookName, handler, opts?)` | Typed lifecycle hook |
| `api.onConversationBindingResolved(handler)` | Conversation binding callback |

`before_install` is a plugin-runtime lifecycle hook, not the operator install policy surface — use `security.installPolicy` when an allow/block decision must cover CLI and Gateway-backed install/update paths. Hook return-value rules:

- `before_tool_call` / `before_install`: `{ block: true }` is terminal (lower-priority handlers skipped); `{ block: false }` is no decision (same as omitting `block`).
- `reply_dispatch`: `{ handled: true, ... }` is terminal — lower-priority handlers and the default model dispatch are skipped.
- `message_sending`: `{ cancel: true }` is terminal, `{ cancel: false }` is no decision; use typed `replyToId`/`threadId` routing before channel-specific `metadata`.
- `message_received`: use the typed `threadId` field for inbound thread/topic routing; keep `metadata` for channel extras.
- `gateway_start`: use `ctx.config`, `ctx.workspaceDir`, `ctx.getCron?.()` for gateway-owned startup state, not internal `gateway:startup` hooks.
- `cron_changed`: observe gateway-owned cron changes via `event.job?.state?.nextRunAtMs` and `ctx.getCron?.()`, keeping OpenClaw the source of truth.

See [OpenClaw Docs — Plugin hooks](https://docs.openclaw.ai/plugins/hooks) for examples and common hook names.

## API object fields

Besides methods, the `api` object exposes these plain data fields read inside `register(api)`:

| Field | Type | Description |
| --- | --- | --- |
| `api.id` | `string` | Plugin id |
| `api.name` | `string` | Display name |
| `api.version` | `string?` | Plugin version (optional) |
| `api.description` | `string?` | Plugin description (optional) |
| `api.source` | `string` | Plugin source path |
| `api.rootDir` | `string?` | Plugin root directory (optional) |
| `api.config` | `OpenClawConfig` | Current config snapshot (active in-memory runtime snapshot when available) |
| `api.pluginConfig` | `Record<string, unknown>` | Plugin-specific config from `plugins.entries.<id>.config` |
| `api.runtime` | `PluginRuntime` | Runtime helpers (see [oc_plugins_sdk_runtime_namespaces](oc_plugins_sdk_runtime_namespaces.md)) |
| `api.logger` | `PluginLogger` | Scoped logger (`debug`, `info`, `warn`, `error`) |
| `api.registrationMode` | `PluginRegistrationMode` | Current load mode; `"setup-runtime"` is the lightweight pre-full-entry setup window |
| `api.resolvePath(input)` | `(string) => string` | Resolve path relative to plugin root |

**Source**: OpenClaw documentation — `plugins/sdk-overview` (mirror `inbox/openclaw_docs/plugins/sdk-overview.md`), Registration API section
**Last Updated**: 2026-06-22
**Status**: Active
