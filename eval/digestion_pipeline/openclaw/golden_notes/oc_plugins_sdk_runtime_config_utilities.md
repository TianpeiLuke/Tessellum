---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - sdk_runtime
keywords:
  - api.runtime config
  - mutateConfigFile replaceConfigFile afterWrite
  - botLoopProtection guard
  - selectApplicableRuntimeConfig
  - createPluginRuntimeStore
  - runtime-config-snapshot subpath
  - openclaw plugin sdk runtime helpers
  - other top-level api fields
topics:
  - OpenClaw
  - Plugin SDK Runtime
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/sdk-runtime
access_control_group: ["general"]
---

# OpenClaw — Plugin SDK `api.runtime` Config and Utilities

## Overview

This note is the procedure for using the config-access, config-write, and shared-utility surfaces of the `api.runtime` object that OpenClaw injects into every plugin during `register(api)`. It mirrors the **Config loading and writes**, **Reusable runtime utilities**, **Storing runtime references**, and **Other top-level `api` fields** sections of the `plugins/sdk-runtime` source page. The complementary per-namespace catalog (`api.runtime.agent`, `llm`, `subagent`, `tts`, etc.) lives in the sibling reference note **[oc_plugins_sdk_runtime_namespaces](oc_plugins_sdk_runtime_namespaces.md)**. Throughout, a plugin obtains the runtime once inside its `register` callback: `const runtime = api.runtime;`.

## Config loading and writes

Prefer config that was **already passed into the active call path** — for example `api.config` during registration, or a `cfg` argument on channel/provider callbacks. This keeps one process snapshot flowing through the work instead of reparsing config on hot paths. Use `api.runtime.config.current()` only when a long-lived handler needs the current process snapshot and no config was passed to that function; the returned value is readonly, so clone it or use a mutation helper before editing. Tool factories receive `ctx.runtimeConfig` plus `ctx.getRuntimeConfig()` — use the getter inside a long-lived tool's `execute` callback when config can change after the tool definition was created.

Persist changes with `api.runtime.config.mutateConfigFile(...)` or `api.runtime.config.replaceConfigFile(...)`. Each write must choose an explicit `afterWrite` policy:

- `afterWrite: { mode: "auto" }` lets the gateway reload planner decide.
- `afterWrite: { mode: "restart", reason: "..." }` forces a clean restart when the writer knows hot reload is unsafe.
- `afterWrite: { mode: "none", reason: "..." }` suppresses automatic reload/restart only when the caller owns the follow-up.

The mutation helpers return `afterWrite` plus a typed `followUp` summary so callers can log or test whether they requested a restart; the gateway still owns *when* that restart actually happens. The accordion documents the `followUp` value shape, for example `{ mode: "restart", requiresRestart: true, reason }`. A minimal write:

```typescript
const cfg = api.runtime.config.current();
await api.runtime.config.mutateConfigFile({
  afterWrite: { mode: "auto" },
  mutate(draft) {
    draft.plugins ??= {};
  },
});
```

`api.runtime.config.loadConfig()` and `api.runtime.config.writeConfigFile(...)` are **deprecated compatibility helpers** under `runtime-config-load-write`. They warn once at runtime and remain available for old external plugins during the migration window. Bundled plugins must not use them: the config boundary guards fail if plugin code calls them or imports those helpers from plugin SDK subpaths.

For direct SDK imports, use the focused config subpaths instead of the broad `openclaw/plugin-sdk/config-runtime` compatibility barrel:

- `config-contracts` — for types.
- `plugin-config-runtime` — for already-loaded config assertions and plugin entry lookup.
- `runtime-config-snapshot` — for current process snapshots.
- `config-mutation` — for writes.

Bundled plugin tests should mock these focused subpaths directly instead of mocking the broad compatibility barrel. Internal OpenClaw runtime code follows the same direction: load config once at the CLI, gateway, or process boundary, then pass that value through. Successful mutation writes refresh the process runtime snapshot and advance its internal revision; long-lived caches should key off the **runtime-owned cache key** instead of serializing config locally. Long-lived runtime modules have a zero-tolerance scanner for ambient `loadConfig()` calls — use a passed `cfg`, a request `context.getRuntimeConfig()`, or `getRuntimeConfig()` at an explicit process boundary.

Provider and channel execution paths must use the **active runtime config snapshot**, not a file snapshot returned for config readback or editing. File snapshots preserve source values such as SecretRef markers for UI and writes; provider callbacks need the resolved runtime view. When a helper may be called with either the active source snapshot or the active runtime snapshot, route through `selectApplicableRuntimeConfig()` before reading credentials.

## Reusable runtime utilities

Use inbound `botLoopProtection` facts for bot-authored inbound messages. Core applies the shared in-memory sliding-window guard **before session record and dispatch**, without tying the policy to one channel. The guard tracks `(scopeId, conversationId, participant pair)` keys, counts both directions of a pair together, applies a cooldown once the window budget is exceeded, and prunes inactive entries opportunistically.

Channel plugins that expose this behavior to operators should prefer the shared `channels.defaults.botLoopProtection` shape for baseline budgets, then layer channel/provider-specific overrides on top. The shared config uses **seconds** because it is user-facing:

```typescript
type ChannelBotLoopProtectionConfig = {
  enabled?: boolean;
  maxEventsPerWindow?: number;
  windowSeconds?: number;
  cooldownSeconds?: number;
};
```

Pass normalized bot-pair facts with the resolved turn. Core resolves defaults, unit conversion, and `enabled` semantics:

```typescript
return {
  channel: "example",
  routeSessionKey,
  storePath,
  ctxPayload,
  recordInboundSession,
  runDispatch,
  botLoopProtection: {
    scopeId: "account-1",
    conversationId: "channel-1",
    senderId: "bot-a",
    receiverId: "bot-b",
    config: channelConfig.botLoopProtection,
    defaultsConfig: runtimeConfig.channels?.defaults?.botLoopProtection,
    defaultEnabled: allowBotsMode !== "off",
  },
};
```

Use `openclaw/plugin-sdk/pair-loop-guard-runtime` directly **only** for custom two-party event loops that do not go through the shared inbound reply runner.

## Storing runtime references

Use `createPluginRuntimeStore` to store the runtime reference for use *outside* the `register` callback. The source documents a three-step flow:

**Step 1 — Create the store.** Import from the narrow `runtime-store` subpath and create the store keyed by plugin id:

```typescript
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
import type { PluginRuntime } from "openclaw/plugin-sdk/runtime-store";

const store = createPluginRuntimeStore<PluginRuntime>({
  pluginId: "my-plugin",
  errorMessage: "my-plugin runtime not initialized",
});
```

**Step 2 — Wire into the entry point.** Pass `store.setRuntime` as the entry's `setRuntime` so the runtime is captured when the plugin loads:

```typescript
export default defineChannelPluginEntry({
  id: "my-plugin",
  name: "My Plugin",
  description: "Example",
  plugin: myPlugin,
  setRuntime: store.setRuntime,
});
```

**Step 3 — Access from other files.** Read the stored runtime with `store.getRuntime()` (throws if not initialized) or `store.tryGetRuntime()` (returns `null` if not initialized):

```typescript
export function getRuntime() {
  return store.getRuntime(); // throws if not initialized
}

export function tryGetRuntime() {
  return store.tryGetRuntime(); // returns null if not initialized
}
```

Prefer `pluginId` for the runtime-store identity. The lower-level `key` form is for uncommon cases where one plugin intentionally needs more than one runtime slot.

## Other top-level `api` fields

Beyond `api.runtime`, the API object also provides the following top-level fields (each grounded in the source `ParamField` entries):

- `api.id` (`string`) — Plugin id.
- `api.name` (`string`) — Plugin display name.
- `api.config` (`OpenClawConfig`) — Current config snapshot (active in-memory runtime snapshot when available).
- `api.pluginConfig` (`Record<string, unknown>`) — Plugin-specific config from `plugins.entries.<id>.config`.
- `api.logger` (`PluginLogger`) — Scoped logger (`debug`, `info`, `warn`, `error`).
- `api.registrationMode` (`PluginRegistrationMode`) — Current load mode; `"setup-runtime"` is the lightweight pre-full-entry startup/setup window.
- `api.resolvePath(input)` (`(string) => string`) — Resolve a path relative to the plugin root.

**Source**: OpenClaw documentation — `plugins/sdk-runtime` (mirror `inbox/openclaw_docs/plugins/sdk-runtime.md`), sections: Config loading and writes, Reusable runtime utilities, Storing runtime references, Other top-level `api` fields
**Last Updated**: 2026-06-22
**Status**: Active
