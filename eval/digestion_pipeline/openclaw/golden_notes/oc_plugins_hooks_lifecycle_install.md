---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - hooks
keywords:
  - openclaw install hooks
  - before_install hook
  - security.installPolicy
  - gateway_start gateway_stop
  - cron_changed hook
  - gateway lifecycle hooks
  - hook deprecations
  - deactivate gateway_stop alias
topics:
  - OpenClaw
  - Plugin Hooks
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/hooks
access_control_group: ["general"]
---

# OpenClaw — Plugin Install + Gateway-Lifecycle Hooks and Upcoming Deprecations

## Overview

This note is the operational complement to the OpenClaw plugin-hook catalog: it covers the three lifecycle-oriented sections of the `plugins/hooks` source page that sit outside the per-turn runtime catalog — **Install hooks**, **Gateway lifecycle**, and **Upcoming deprecations**. It documents where `before_install` fires relative to `security.installPolicy`, how `gateway_start` / `gateway_stop` / `cron_changed` attach plugin-owned services and schedulers to the Gateway process lifecycle, and which hook-adjacent surfaces are deprecated and how to migrate off them before the next major release. The per-phase runtime hook types (agent-turn, tool-call policy, prompt/model, message, session) are owned by the sibling [oc_plugins_hooks_catalog](oc_plugins_hooks_catalog.md).

## Install hooks

Use `security.installPolicy` for operator-owned allow/block decisions. That policy runs from OpenClaw config, covers CLI install and update paths, and fails closed when enabled but unavailable. It is the primary host/enterprise security boundary for installs — `before_install` is not.

`before_install` is a **plugin-runtime lifecycle hook**. It runs after `security.installPolicy` only in the OpenClaw process where plugin hooks have already been loaded, such as Gateway-backed install flows. It is useful for plugin-owned observations, warnings, and compatibility checks, but it is not the primary enterprise or host security boundary for installs. The `builtinScan` field remains in the event payload for compatibility, but OpenClaw no longer runs built-in install-time dangerous-code blocking, so it is an empty `ok` result. A handler can return additional findings or `{ block: true, blockReason }` to stop the install in that process.

Guard behavior for `before_install`:

- `block: true` is terminal.
- `block: false` is treated as no decision.
- Handler failures block the install fail-closed.

## Gateway lifecycle

Use `gateway_start` for plugin services that need Gateway-owned state. The context exposes `ctx.config`, `ctx.workspaceDir`, and `ctx.getCron?.()` for cron inspection and updates. Use `gateway_stop` to clean up long-running resources. Do not rely on the internal `gateway:startup` hook for plugin-owned runtime services.

`cron_changed` fires for gateway-owned cron lifecycle events with a typed event payload covering the reasons `added`, `updated`, `removed`, `started`, `finished`, and `scheduled`. The event carries a `PluginHookGatewayCronJob` snapshot — including `state.nextRunAtMs`, `state.lastRunStatus`, and `state.lastError` when present — plus a `PluginHookGatewayCronDeliveryStatus` of `not-requested` | `delivered` | `not-delivered` | `unknown`. Removed events still carry the deleted job snapshot so external schedulers can reconcile state. Use `ctx.getCron?.()` and `ctx.config` from the runtime context when syncing external wake schedulers, and keep OpenClaw as the source of truth for due checks and execution.

Note that two adjacent lifecycle boundaries are documented on other surfaces of the same page: the `session_start` / `session_end` `shutdown` and `restart` reasons fire from the gateway shutdown finalizer when the process is stopped or restarted while sessions are still active (so memory or transcript stores can finalize ghost rows), and that finalizer is bounded so a slow plugin cannot block SIGTERM/SIGINT. Those session-boundary hooks are catalog-owned and detailed in [oc_plugins_hooks_catalog](oc_plugins_hooks_catalog.md); only the gateway-process hooks (`gateway_start` / `gateway_stop` / `cron_changed`) are detailed here.

## Upcoming deprecations

A few hook-adjacent surfaces are deprecated but still supported. Migrate before the next major release:

- **Plaintext channel envelopes** in `inbound_claim` and `message_received` handlers. Read `BodyForAgent` and the structured user-context blocks instead of parsing flat envelope text. See `Plaintext channel envelopes → BodyForAgent` at `/plugins/sdk-migration#active-deprecations`.
- **`before_agent_start`** remains for compatibility. New plugins should use `before_model_resolve` and `before_prompt_build` instead of the combined phase.
- **`subagent_spawning`** remains for compatibility with older plugins, but new plugins should not return thread routing from it. Core prepares `thread: true` subagent bindings through channel session-binding adapters before `subagent_spawned` fires.
- **`deactivate`** remains as a deprecated cleanup compatibility alias until after **2026-08-16**. New plugins should use `gateway_stop`.
- **`onResolution` in `before_tool_call`** now uses the typed `PluginApprovalResolution` union (`allow-once` / `allow-always` / `deny` / `timeout` / `cancelled`) instead of a free-form `string`.

For the full list — memory capability registration, provider thinking profile, external auth providers, provider discovery types, task runtime accessors, and the `command-auth` → `command-status` rename — see `Plugin SDK migration → Active deprecations` at `/plugins/sdk-migration#active-deprecations`.

**Source**: OpenClaw documentation — `plugins/hooks` (mirror `inbox/openclaw_docs/plugins/hooks.md`), sections Install hooks / Gateway lifecycle / Upcoming deprecations
**Last Updated**: 2026-06-22
**Status**: Active
