---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - cli_backend
keywords:
  - openclaw cli backend plugin
  - registerCliBackend
  - cliBackends manifest ownership
  - CliBackendConfig fields
  - ownsNativeCompaction opt-out
  - bundleMcp mcp tool bridge
  - acme-cli model ref
  - agents.defaults.cliBackends override
topics:
  - OpenClaw
  - Plugins
  - CLI Backend Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/plugins/cli-backend-plugins
access_control_group: ["general"]
---

# OpenClaw — Building CLI Backend Plugins

## Overview

This procedure note covers how to build an OpenClaw **CLI backend plugin** — a plugin that lets OpenClaw call a local AI CLI as a text-inference backend, exposed as a provider prefix in model refs (e.g. `acme-cli/acme-large`). It mirrors the `plugins/cli-backend-plugins` source page: what the plugin owns (three contracts), the minimal three-step `registerCliBackend` plugin, the `CliBackendConfig` launch/parse shape, the advanced backend hooks (including the `ownsNativeCompaction` opt-out), the loopback MCP tool bridge, user configuration overrides, verification commands, and the pre-ship checklist. Choose a CLI backend when the upstream integration is already a local command, when the CLI owns local login state, or when the CLI is a useful fallback if API providers are unavailable; if the upstream exposes a normal HTTP model API write a provider plugin instead, and if the upstream runtime owns complete agent sessions / tool events / compaction / background task state use an agent harness instead.

## What the Plugin Owns

A CLI backend plugin has three contracts, each in its own file:

| Contract | File | Purpose |
| --- | --- | --- |
| Package entry | `package.json` | Points OpenClaw at the plugin runtime module |
| Manifest ownership | `openclaw.plugin.json` | Declares the backend id before runtime loads |
| Runtime registration | `index.ts` | Calls `api.registerCliBackend(...)` with command defaults |

The manifest is discovery metadata: it does not execute the CLI and does not register runtime behavior. Runtime behavior starts only when the plugin entry calls `api.registerCliBackend(...)`.

## Minimal Backend Plugin

The minimal plugin is three steps. **Step 1 — create package metadata** (`package.json`): declare `type: "module"`, the `openclaw.extensions` entry array, `compat` (`pluginApi`, `minGatewayVersion`), `build` versions, and the `openclaw` dependency. Published packages must ship built JavaScript runtime files; if the source entry is `./src/index.ts`, add `openclaw.runtimeExtensions` pointing at the built JavaScript peer.

**Step 2 — declare backend ownership** (`openclaw.plugin.json`):

```json openclaw.plugin.json
{
  "id": "acme-cli",
  "name": "Acme CLI",
  "description": "Run Acme's local AI CLI through OpenClaw",
  "cliBackends": ["acme-cli"],
  "setup": {
    "cliBackends": ["acme-cli"],
    "requiresRuntime": false
  },
  "activation": {
    "onStartup": false
  },
  "configSchema": {
    "type": "object",
    "additionalProperties": false
  }
}
```

`cliBackends` is the runtime ownership list — it lets OpenClaw auto-load the plugin when config or model selection mentions `acme-cli/...`. `setup.cliBackends` is the descriptor-first setup surface; add it when model discovery, onboarding, or status should recognize the backend without loading plugin runtime, and use `requiresRuntime: false` only when those static descriptors are enough for setup.

**Step 3 — register the backend** (`index.ts`): import `definePluginEntry` and the `CliBackendPlugin` type plus the watchdog defaults, then call `api.registerCliBackend(...)` from `register(api)`:

```typescript index.ts
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import {
  CLI_FRESH_WATCHDOG_DEFAULTS,
  CLI_RESUME_WATCHDOG_DEFAULTS,
  type CliBackendPlugin,
} from "openclaw/plugin-sdk/cli-backend";

function buildAcmeCliBackend(): CliBackendPlugin {
  return {
    id: "acme-cli",
    liveTest: {
      defaultModelRef: "acme-cli/acme-large",
      defaultImageProbe: false,
      defaultMcpProbe: false,
      docker: { npmPackage: "@acme/acme-cli", binaryName: "acme" },
    },
    config: {
      command: "acme",
      args: ["chat", "--json"],
      output: "json",
      input: "stdin",
      modelArg: "--model",
      sessionArg: "--session",
      sessionMode: "existing",
      sessionIdFields: ["session_id", "conversation_id"],
      systemPromptFileArg: "--system-file",
      systemPromptWhen: "first",
      imageArg: "--image",
      imageMode: "repeat",
      reliability: {
        watchdog: {
          fresh: { ...CLI_FRESH_WATCHDOG_DEFAULTS },
          resume: { ...CLI_RESUME_WATCHDOG_DEFAULTS },
        },
      },
      serialize: true,
    },
  };
}

export default definePluginEntry({
  id: "acme-cli",
  name: "Acme CLI",
  description: "Run Acme's local AI CLI through OpenClaw",
  register(api) {
    api.registerCliBackend(buildAcmeCliBackend());
  },
});
```

The backend `id` must match the manifest `cliBackends` entry. The registered `config` is only the default; user config under `agents.defaults.cliBackends.acme-cli` is merged over it at runtime.

## Config Shape

`CliBackendConfig` describes how OpenClaw should launch and parse the CLI. Prefer the smallest static config that matches the CLI; add plugin callbacks only for behavior that really belongs to the backend.

| Field | Use |
| --- | --- |
| `command` | Binary name or absolute command path |
| `args` | Base argv for fresh runs |
| `resumeArgs` | Alternate argv for resumed sessions; supports `{sessionId}` |
| `output` / `resumeOutput` | Parser: `json`, `jsonl`, or `text` |
| `input` | Prompt transport: `arg` or `stdin` |
| `modelArg` | Flag used before the model id |
| `modelAliases` | Map OpenClaw model ids to CLI-native ids |
| `sessionArg` / `sessionArgs` | How to pass a session id |
| `sessionMode` | `always`, `existing`, or `none` |
| `sessionIdFields` | JSON fields OpenClaw reads from CLI output |
| `systemPromptArg` / `systemPromptFileArg` | System prompt transport |
| `systemPromptWhen` | `first`, `always`, or `never` |
| `imageArg` / `imageMode` | Image path support |
| `serialize` | Keep same-backend runs ordered |
| `reliability.watchdog` | No-output timeout tuning |

## Advanced Backend Hooks

`CliBackendPlugin` can also define provider-owned hooks. Keep these hooks provider-owned — do not add CLI-specific branches to core when a backend hook can express the behavior.

| Hook | Use |
| --- | --- |
| `normalizeConfig(config, context)` | Rewrite legacy user config after merge |
| `resolveExecutionArgs(ctx)` | Add request-scoped flags such as thinking effort or side-question isolation |
| `prepareExecution(ctx)` | Create temporary auth or config bridges before launch |
| `transformSystemPrompt(ctx)` | Apply a final CLI-specific system prompt transform |
| `textTransforms` | Bidirectional prompt/output replacements |
| `defaultAuthProfileId` | Prefer a specific OpenClaw auth profile |
| `authEpochMode` | Decide how auth changes invalidate stored CLI sessions |
| `nativeToolMode` | Declare whether the CLI has always-on native tools |
| `sideQuestionToolMode` | Declare disabled native tools for `/btw` side questions |
| `bundleMcp` / `bundleMcpMode` | Opt into OpenClaw's loopback MCP tool bridge |
| `ownsNativeCompaction` | Backend owns its own compaction — OpenClaw defers |

`ctx.executionMode` is `"agent"` for normal turns and `"side-question"` for ephemeral `/btw` calls; use it when the CLI needs different one-shot flags such as disabling native tools, session persistence, or resume behavior for BTW. If a backend normally has `nativeToolMode: "always-on"` but its side-question argv reliably disables those tools, also set `sideQuestionToolMode: "disabled"`; otherwise OpenClaw fails closed when BTW requires a no-tools CLI run.

### `ownsNativeCompaction`: Opting Out of OpenClaw Compaction

If your backend runs an agent that compacts its **own** transcript, set `ownsNativeCompaction: true` so OpenClaw's safeguard summarizer never runs against its sessions — the CLI compaction lifecycle returns a no-op and the turn proceeds. `claude-cli` declares it because Claude Code compacts internally with no harness endpoint; native-harness sessions such as Codex keep routing to their harness compaction endpoint instead. Only declare it when ALL of the following hold, or a deferred over-budget session can stay over budget / go stale (OpenClaw no longer rescues it): the backend reliably compacts or bounds its own transcript as it nears its window; it persists a resumable session so the compacted state survives turns (e.g. `--resume` / `--session-id`); and it is not a native-harness compaction session — matching `agentHarnessId` sessions route to the harness endpoint instead.

## MCP Tool Bridge

CLI backends do not receive OpenClaw tools by default. If the CLI can consume an MCP configuration, opt in explicitly with `bundleMcp: true` and a `bundleMcpMode`:

```typescript
return {
  id: "acme-cli",
  bundleMcp: true,
  bundleMcpMode: "codex-config-overrides",
  config: {
    command: "acme",
    args: ["chat", "--json"],
    output: "json",
  },
};
```

The supported bridge modes are `claude-config-file` (CLIs that accept an MCP config file), `codex-config-overrides` (CLIs that accept config overrides on argv), and `gemini-system-settings` (CLIs that read MCP settings from their system settings directory). Only enable the bridge when the CLI can actually consume it. If the CLI has its own built-in tool layer that cannot be disabled, set `nativeToolMode: "always-on"` so OpenClaw can fail closed when a caller requires no native tools.

## User Configuration

Users can override any backend default under `agents.defaults.cliBackends.<id>`. Document the minimum override users are likely to need — usually that is only `command` when the binary is outside `PATH`.

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "acme-cli": {
          command: "/opt/acme/bin/acme",
          args: ["chat", "--json", "--profile", "work"],
          modelAliases: { large: "acme-large-2026" },
        },
      },
      model: {
        primary: "openai/gpt-5.5",
        fallbacks: ["acme-cli/large"],
      },
    },
  },
}
```

## Verification

For bundled plugins, add a focused test around the builder and setup registration, then run the plugin's targeted test lane (`pnpm test extensions/acme-cli`). For local or installed plugins, verify discovery and one real model run:

```bash
openclaw plugins inspect acme-cli --runtime --json
openclaw agent --message "reply exactly: backend ok" --model acme-cli/acme-large
```

If the backend supports images or MCP, add a live smoke that proves those paths with the real CLI. Do not rely on static inspection for prompt, image, MCP, or session-resume behavior.

## Checklist

- `package.json` has `openclaw.extensions` and built runtime entries for published packages.
- `openclaw.plugin.json` declares `cliBackends` and intentional `activation.onStartup`.
- `setup.cliBackends` is present when setup/model discovery should see the backend cold.
- `api.registerCliBackend(...)` uses the same backend id as the manifest.
- User overrides under `agents.defaults.cliBackends.<id>` still win.
- Session, system prompt, image, and output parser settings match the real CLI contract.
- Targeted tests and at least one live CLI smoke prove the backend path.

**Source**: OpenClaw documentation — `plugins/cli-backend-plugins` (mirror `inbox/openclaw_docs/plugins/cli-backend-plugins.md`)
**Last Updated**: 2026-06-22
**Status**: Active
