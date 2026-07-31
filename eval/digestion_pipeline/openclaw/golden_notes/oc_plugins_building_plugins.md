---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - building_plugins
keywords:
  - openclaw building plugins
  - first openclaw plugin tutorial
  - definePluginEntry registerTool
  - openclaw.plugin.json manifest contracts.tools
  - openclaw plugins install clawhub
  - plugin sdk import subpaths
  - tools.allow optional tools
  - pre-submission checklist beta blocker
topics:
  - OpenClaw
  - Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/building-plugins
access_control_group: ["general"]
---

# OpenClaw — Building Your First Plugin

## Overview

This note is the step-by-step **procedure** for building your first OpenClaw plugin, mirroring the `plugins/building-plugins` source page. Plugins extend OpenClaw without changing core: a plugin can add a messaging channel, model provider, local CLI backend, agent tool, hook, media provider, or another plugin-owned capability. You do NOT need to add an external plugin to the OpenClaw repository — publish the package to ClawHub and users install it with `openclaw plugins install clawhub:<package-name>` (bare package specs still install from npm during the launch cutover; use the `clawhub:` prefix when you want ClawHub resolution). It covers the runtime requirements, choosing a plugin shape, the smallest working quickstart (package metadata → manifest → entry point → test → publish → install), registering required vs optional tools, SDK import conventions, the pre-submission checklist, testing against beta releases, and next steps.

## Requirements

Before building, satisfy the runtime and tooling prerequisites:

- Use **Node 22.19** or newer and a package manager such as `npm` or `pnpm`.
- Be familiar with **TypeScript ESM modules**.
- For in-repo bundled plugin work, clone the repository and run `pnpm install`. Source-checkout plugin development is **pnpm-only** because OpenClaw loads bundled plugins from `extensions/*` workspace packages.

## Choose the Plugin Shape

The page routes you to a shape-specific guide via a card group (each card is a link-out to another plugins doc page):

- **Channel plugin** (`/plugins/sdk-channel-plugins`) — connect OpenClaw to a messaging platform.
- **Provider plugin** (`/plugins/sdk-provider-plugins`) — add a model, media, search, fetch, speech, or realtime provider.
- **CLI backend plugin** (`/plugins/cli-backend-plugins`) — run a local AI CLI through OpenClaw model fallback.
- **Tool plugin** (`/plugins/tool-plugins`) — register agent tools.

The quickstart below builds a **minimal tool plugin** by registering one required agent tool — the shortest useful plugin shape.

## Quickstart

The quickstart is a six-step sequence that shows the package, manifest, entry point, and local proof.

### Step 1 — Create package metadata

Two files declare the package and the plugin manifest. `package.json` carries the `openclaw` metadata block (`extensions` entry list, `compat` floors, and `build` versions); `openclaw.plugin.json` is the manifest:

```jsonc
// package.json
{
  "name": "@myorg/openclaw-my-plugin",
  "version": "1.0.0",
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"],
    "compat": {
      "pluginApi": ">=2026.3.24-beta.2",
      "minGatewayVersion": "2026.3.24-beta.2"
    },
    "build": {
      "openclawVersion": "2026.3.24-beta.2",
      "pluginSdkVersion": "2026.3.24-beta.2"
    }
  }
}

// openclaw.plugin.json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "description": "Adds a custom tool to OpenClaw",
  "contracts": {
    "tools": ["my_tool"]
  },
  "activation": {
    "onStartup": true
  },
  "configSchema": {
    "type": "object",
    "additionalProperties": false
  }
}
```

Published external plugins should point runtime entries at **built JavaScript files** (see SDK entry points for the full entry-point contract). Every plugin needs a manifest, even when it has no config. Runtime tools must appear in `contracts.tools` so OpenClaw can discover ownership without eagerly loading every plugin runtime. Set `activation.onStartup` intentionally; this example starts on Gateway startup. Host-trusted plugin surfaces are also manifest-gated and require explicit enablement for installed plugins: if an installed plugin registers `api.registerAgentToolResultMiddleware(...)`, declare each target runtime in `contracts.agentToolResultMiddleware`; if it registers `api.registerTrustedToolPolicy(...)`, declare each policy id in `contracts.trustedToolPolicies` — these declarations keep install-time inspection and runtime registration aligned.

### Step 2 — Register the tool

The entry point uses `definePluginEntry` and registers the tool inside `register(api)`:

```typescript index.ts
import { Type } from "typebox";
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "my-plugin",
  name: "My Plugin",
  description: "Adds a custom tool to OpenClaw",
  register(api) {
    api.registerTool({
      name: "my_tool",
      description: "Echo one input value",
      parameters: Type.Object({ input: Type.String() }),
      async execute(_id, params) {
        return {
          content: [{ type: "text", text: `Got: ${params.input}` }],
        };
      },
    });
  },
});
```

Use `definePluginEntry` for non-channel plugins; channel plugins use `defineChannelPluginEntry`.

### Step 3 — Test the runtime

For an installed or external plugin, inspect the loaded runtime with `openclaw plugins inspect my-plugin --runtime --json`. If the plugin registers a CLI command, run that command too — for example, a demo command should have an execution proof such as `openclaw demo-plugin ping`. For a bundled plugin in this repository, OpenClaw discovers source-checkout plugin packages from the `extensions/*` workspace; run the closest targeted test, then validate and publish through ClawHub (dry-run first; the canonical ClawHub snippets live in `docs/snippets/plugin-publish/`), and finally install the published package:

```bash
# Step 3 — Test the runtime (bundled plugin)
pnpm test -- extensions/my-plugin/
pnpm check
# Step 4 — Publish
clawhub package publish your-org/your-plugin --dry-run
clawhub package publish your-org/your-plugin
# Step 5 — Install
openclaw plugins install clawhub:your-org/your-plugin
```

## Registering Tools

Tools can be **required** or **optional**. Required tools are always available when the plugin is enabled; optional tools require user opt-in. Register an optional tool by passing `{ optional: true }` as the second argument to `api.registerTool(...)`:

```typescript
register(api) {
  api.registerTool(
    {
      name: "workflow_tool",
      description: "Run a workflow",
      parameters: Type.Object({ pipeline: Type.String() }),
      async execute(_id, params) {
        return { content: [{ type: "text", text: params.pipeline }] };
      },
    },
    { optional: true },
  );
}
```

Every tool registered with `api.registerTool(...)` must also be declared in the plugin manifest under `contracts.tools`, with optional tools mirrored under `toolMetadata.<tool>.optional`. Users then opt in via `tools.allow` (a tool name, or a plugin id for all of that plugin's tools):

```json5
{
  tools: { allow: ["workflow_tool"] }, // or ["my-plugin"] for all tools from one plugin
}
```

Optional tools control whether a tool is exposed to the model; use **plugin permission requests** when a tool or hook should ask for approval after the model selects it and before the action runs. Use optional tools for side effects, unusual binaries, or capabilities that should not be exposed by default. Tool names must not conflict with core tools — conflicts are skipped and reported in plugin diagnostics, and malformed registrations (including tool descriptors without `parameters`) are skipped and reported the same way. Registered tools are typed functions the model can call after policy and allowlist checks pass. Tool factories receive a runtime-supplied context object; use `ctx.activeModel` when a tool needs to log, display, or adapt to the active model for the current turn (the object can include `provider`, `modelId`, and `modelRef`), but treat it as informational runtime metadata, NOT as a security boundary against the local operator, installed plugin code, or a modified OpenClaw runtime — sensitive local tools should still require an explicit plugin or operator opt-in and fail closed when active-model metadata is missing or unsuitable. The manifest declares ownership and discovery; execution still calls the live registered tool implementation, so keep `toolMetadata.<tool>.optional: true` aligned with `api.registerTool(..., { optional: true })` so OpenClaw can avoid loading that plugin runtime until the tool is explicitly allowlisted.

## Import Conventions

Import from **focused SDK subpaths**, not the deprecated root barrel:

```typescript
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
```

Do NOT import from the deprecated root barrel `import { definePluginEntry } from "openclaw/plugin-sdk";`. Within your plugin package, use local barrel files such as `api.ts` and `runtime-api.ts` for internal imports; do not import your own plugin through an SDK path, and keep provider-specific helpers in the provider package unless the seam is truly generic. Custom Gateway RPC methods are an advanced entry point — keep them on a plugin-specific prefix, because core admin namespaces such as `config.*`, `exec.approvals.*`, `operator.admin.*`, `wizard.*`, and `update.*` stay reserved and resolve to `operator.admin`; the `openclaw/plugin-sdk/gateway-method-runtime` bridge is reserved for plugin HTTP routes that declare `contracts.gatewayMethodDispatch: ["authenticated-request"]`. For the full import map, see the Plugin SDK overview.

## Pre-Submission Checklist

Before submitting, verify each item:

- `package.json` has correct `openclaw` metadata.
- `openclaw.plugin.json` manifest is present and valid.
- Entry point uses `defineChannelPluginEntry` or `definePluginEntry`.
- All imports use focused `plugin-sdk/<subpath>` paths.
- Internal imports use local modules, not SDK self-imports.
- Tests pass (`pnpm test -- <bundled-plugin-root>/my-plugin/`).
- `pnpm check` passes (in-repo plugins).

## Test Against Beta Releases

To keep a published plugin green across releases, follow the beta-testing loop:

1. Watch for GitHub release tags on `openclaw/openclaw` and subscribe via `Watch` > `Releases`. Beta tags look like `v2026.3.N-beta.1`. You can also turn on notifications for the official OpenClaw X account `@openclaw` for release announcements.
2. Test your plugin against the beta tag as soon as it appears — the window before stable is typically only a few hours.
3. Post in your plugin's thread in the `plugin-forum` Discord channel after testing with either `all good` or what broke; if you do not have a thread yet, create one.
4. If something breaks, open or update an issue titled `Beta blocker: <plugin-name> - <summary>` and apply the `beta-blocker` label, and put the issue link in your thread.
5. Open a PR to `main` titled `fix(<plugin-id>): beta blocker - <summary>` and link the issue in both the PR and your Discord thread. Contributors cannot label PRs, so the title is the PR-side signal for maintainers and automation; blockers with a PR get merged, blockers without one might ship anyway, and maintainers watch these threads during beta testing.
6. Silence means green. If you miss the window, your fix likely lands in the next cycle.

## Next Steps

The page closes with link-outs to the deeper plugin docs: Channel Plugins (`/plugins/sdk-channel-plugins`), Provider Plugins (`/plugins/sdk-provider-plugins`), CLI Backend Plugins (`/plugins/cli-backend-plugins`), SDK Overview (`/plugins/sdk-overview`, the import map and registration API reference), Runtime Helpers (`/plugins/sdk-runtime`, TTS/search/subagent via `api.runtime`), Testing (`/plugins/sdk-testing`), and the full Plugin Manifest schema reference (`/plugins/manifest`).

**Source**: OpenClaw documentation — `plugins/building-plugins` (mirror `inbox/openclaw_docs/plugins/building-plugins.md`)
**Last Updated**: 2026-06-22
**Status**: Active
