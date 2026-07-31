---
tags:
  - resource
  - documentation
  - openclaw
  - refactor
  - plugins
keywords:
  - openclaw canvas plugin refactor
  - canvas bundled experimental plugin
  - extensions/canvas openclaw.plugin.json
  - core vs plugin boundary
  - registerNodeCliFeature
  - pluginSurfaceUrls.canvas
  - plugins.entries.canvas.config.host
  - canvas doctor migration
  - plugin inventory check
topics:
  - OpenClaw
  - Refactor — Canvas Plugin
language: markdown
date of note: 2026-06-22
status: active
building_block: argument
source_url: https://docs.openclaw.ai/refactor/canvas
access_control_group: ["general"]
---

# OpenClaw — Canvas Plugin Refactor (Core → Bundled Experimental Plugin)

## Overview

This note captures the design argument of the OpenClaw `refactor/canvas` page: because Canvas is low-use and experimental, it should be treated as a **bundled plugin, not a core feature**, with all Canvas-specific behavior relocated under `extensions/canvas` while core keeps only generic gateway, node, HTTP, auth, config, and native-client plumbing. It mirrors that page's full structure — the Goal (what `extensions/canvas` must own while preserving paired-node behavior), Non-goals (what this refactor deliberately does NOT touch), the Current branch state (work already done plus known remaining core-owned surfaces), the Target shape (the explicit plugin-owns vs core-owns split), the Migration steps, the Audit checklist that gates "refactor complete", and the targeted Verification commands. The claim being argued is a boundary contract: Canvas behavior is plugin-owned, core exposes only generic seams, and the cut-over is verified by `rg` emptiness checks plus plugin-inventory / plugin-SDK API gates.

## Goal — Move Canvas Ownership to `extensions/canvas`

The goal is to move Canvas ownership to `extensions/canvas` **while preserving the current paired-node behavior**. Concretely, after the move the following must hold: the agent-facing `canvas` tool is registered by the Canvas plugin; Canvas node commands are allowed only when the Canvas plugin registers them; A2UI host/source files live under the Canvas plugin; Canvas document materialization lives under the Canvas plugin; the CLI command implementation lives under the Canvas plugin (or delegates through a plugin-owned runtime barrel); and docs plus the plugin inventory describe Canvas as experimental and plugin-backed. The boundary principle stated up front is that core may keep generic gateway, node, HTTP, auth, config, and native-client plumbing, but Canvas-specific behavior should live under `extensions/canvas`.

## Non-goals

The refactor is deliberately scoped to ownership/relocation, not redesign or deletion. Three non-goals are called out explicitly: do **not** redesign the native app Canvas UI in this refactor; do **not** remove Canvas protocol/client support from iOS, Android, or macOS unless a separate product decision says Canvas should be deleted; and do **not** build a broad plugin service framework only for Canvas unless at least one other bundled plugin needs the same seam. The last non-goal is the argument's guardrail against over-generalization — generic seams are extracted only when a second consumer justifies them, otherwise the work stays Canvas-local.

## Current branch state

The page records the relocation as already substantially executed on the branch. **Done** items include: added a bundled plugin package in `extensions/canvas`; added `extensions/canvas/openclaw.plugin.json`; moved the agent `canvas` tool from `src/agents/tools/canvas-tool.ts` to `extensions/canvas/src/tool.ts`; removed core registration of `createCanvasTool` from `src/agents/openclaw-tools.ts`; moved the Canvas host implementation from `src/canvas-host` to `extensions/canvas/src/host`; kept `extensions/canvas/runtime-api.ts` as the plugin-owned compatibility barrel for tests, packaging, and external public Canvas helpers; moved Canvas document materialization from `src/gateway/canvas-documents.ts` to `extensions/canvas/src/documents.ts`; moved the Canvas CLI implementation and A2UI JSONL helpers into `extensions/canvas/src/cli.ts`; and moved the Canvas host URL and scoped capability helpers into `extensions/canvas/src`.

It also moved Canvas node command defaults out of hardcoded core lists and into plugin `nodeInvokePolicies`; added plugin-owned Canvas host config at `plugins.entries.canvas.config.host`; moved Canvas and A2UI HTTP serving behind Canvas plugin HTTP route registration; added generic plugin WebSocket upgrade dispatch for plugin-owned HTTP routes; replaced Canvas-specific gateway host URL and node capability auth with generic hosted-plugin-surface and node-capability helpers; and added plugin-owned hosted media resolvers so Canvas document URLs resolve through the Canvas plugin instead of core importing Canvas document internals. It added `api.registerNodeCliFeature(...)` so Canvas can declare `openclaw nodes canvas` as a plugin-owned node feature without manually spelling the parent command path; removed production `src/**` imports of `extensions/canvas/runtime-api.js`; moved the A2UI bundle source from `apps/shared/OpenClawKit/Tools/CanvasA2UI` to `extensions/canvas/src/host/a2ui-app`; moved the A2UI build/copy implementation under `extensions/canvas/scripts` and replaced root build wiring with generic bundled-plugin asset hooks; removed the runtime legacy top-level `canvasHost` config alias; kept the Canvas doctor migration so `openclaw doctor --fix` rewrites old `canvasHost` configs into `plugins.entries.canvas.config.host`; updated the generated plugin inventory to include Canvas; and added plugin reference docs at `docs/plugins/reference/canvas.md`.

A notable compatibility break is recorded: old-agent Canvas protocol compatibility was removed behind gateway protocol v4. Native clients and gateways now use only `pluginSurfaceUrls.canvas` plus `node.pluginSurface.refresh`; the deprecated `canvasHostUrl`, `canvasCapability`, and `node.canvas.capability.refresh` path is **intentionally unsupported** in this experimental refactor.

**Known remaining core-owned Canvas surfaces** (not yet moved, intentionally): native app Canvas handlers under `apps/` still intentionally consume the Canvas plugin surface; native app Canvas protocol/client handlers under `apps/`; and published artifact output still uses `dist/canvas-host/a2ui` for backwards-compatible runtime lookup, but the copy step is now plugin-owned.

## Target shape — Plugin owns vs Core owns

The argument's target end-state is an explicit two-sided ownership split. **`extensions/canvas` should own**: the plugin manifest and package metadata; agent tool registration; node invoke command policy; the Canvas host and A2UI runtime; the Canvas A2UI bundle source and asset build/copy scripts; Canvas document creation and asset resolution; the Canvas CLI implementation; and the Canvas docs page and plugin inventory entry.

**Core should own only generic seams**: plugin discovery and registration; the generic agent tool registry; the generic node invoke policy registry; generic gateway HTTP/auth and WebSocket upgrade dispatch; generic hosted-plugin-surface URL resolution; generic hosted media resolver registration; generic node capability transport; generic config plumbing; and generic bundled-plugin asset hook discovery. Native apps may keep Canvas command handlers as clients of the protocol — they are not the plugin runtime owner. The recurring word "generic" is the boundary test: anything Canvas-specific belongs to the plugin, anything reusable by other plugins belongs to core.

## Migration steps

The page lists three migration steps to reach the target shape: (1) treat `plugins.entries.canvas.config.host` as the plugin-owned config surface; (2) update docs so Canvas is described as an experimental bundled plugin; and (3) run focused Canvas tests, plugin inventory checks, plugin SDK API checks, and build/type gates affected by runtime boundaries.

## Audit checklist — gates "refactor complete"

Before calling the refactor complete, the page requires a checklist of mostly-emptiness `rg` searches proving core no longer owns Canvas behavior, plus passing inventory/API/test gates. The emptiness searches are: `rg "src/canvas-host|../canvas-host"` returns no live source imports; `rg "canvas-tool|createCanvasTool" src` finds no core-owned Canvas tool implementation; `rg "canvas.present|canvas.snapshot|canvas.a2ui" src/gateway` finds no hardcoded allowlist defaults outside generic plugin policy tests; `rg "extensions/canvas/runtime-api" src --glob '!**/*.test.ts'` is empty; `rg "canvas-documents" src` is empty; `rg "registerNodesCanvasCommands|nodes-canvas" src` is empty (the Canvas plugin registers `openclaw nodes canvas` through nested plugin CLI metadata); `rg "createCanvasHostHandler|handleA2uiHttpRequest" src/gateway` returns no gateway runtime ownership; and `rg "apps/shared/OpenClawKit/Tools/CanvasA2UI|canvas-a2ui-copy|extensions/canvas/src/host/a2ui" scripts .github package.json` finds only compatibility wrappers or plugin-owned paths.

The remaining gates are: `pnpm plugins:inventory:check` passes; `pnpm plugin-sdk:api:check` passes (or generated API baselines are intentionally updated and reviewed); targeted Canvas tests pass; changed-lanes tests pass for Canvas host/A2UI paths; and the PR body explicitly says Canvas is experimental and plugin-backed.

## Verification commands

The page gives the targeted local checks to run while iterating (verbatim):

```sh
pnpm test extensions/canvas/src/host/server.test.ts extensions/canvas/src/host/server.state-dir.test.ts extensions/canvas/src/host/file-resolver.test.ts
pnpm test src/gateway/server.plugin-node-capability-auth.test.ts src/gateway/server-import-boundary.test.ts
pnpm test extensions/canvas/src/config-migration.test.ts src/commands/doctor-legacy-config.migrations.test.ts
pnpm test test/scripts/changed-lanes.test.ts test/scripts/build-all.test.ts extensions/canvas/scripts/bundle-a2ui.test.ts test/scripts/bundled-plugin-assets.test.ts extensions/canvas/scripts/copy-a2ui.test.ts src/infra/run-node.test.ts
pnpm tsgo:extensions
pnpm plugins:inventory:check
pnpm plugin-sdk:api:check
```

Run `pnpm build` before push if the runtime barrel, lazy import, packaging, or published plugin surfaces change.

**Source**: OpenClaw documentation — `refactor/canvas` (mirror `inbox/openclaw_docs/refactor/canvas.md`)
**Last Updated**: 2026-06-22
**Status**: Active
