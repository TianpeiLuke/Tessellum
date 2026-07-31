---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - agent_harness
keywords:
  - openclaw agent harness sdk
  - agent harness plugin contract
  - runtimePlan policy bundle
  - registerAgentHarness selection policy
  - codex harness provider pairing
  - agentRuntime.id runtime strictness
  - native session transcript mirror
  - classifyAgentHarnessTerminalOutcome
topics:
  - OpenClaw
  - Agent Harness Plugins
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/plugins/sdk-agent-harness
access_control_group: ["general"]
---

# OpenClaw — Agent Harness Plugin SDK

## Overview

This note covers the OpenClaw **agent-harness plugin SDK** — the experimental, low-level executor surface that a bundled or trusted native plugin implements so a model family can run one prepared agent turn through its own native session runtime instead of OpenClaw's embedded runner. It mirrors the `plugins/sdk-agent-harness` source page: the harness definition and when to use it, the host-versus-harness ownership split (`params.runtimePlan`), registration, selection policy, the provider-plus-harness pairing exemplified by the bundled `codex` harness, runtime strictness, the transcript-mirror contract, tool/media result routing, and current limitations.

## What an agent harness is

An **agent harness** is the low-level executor for one prepared OpenClaw agent turn — explicitly *not* a model provider, *not* a channel, and *not* a tool registry (for the user-facing mental model see `/concepts/agent-runtimes`). The surface is for bundled or trusted native plugins only, and the contract is experimental because the parameter types intentionally mirror the current embedded runner.

## When to use a harness

Register an agent harness when a model family has its own native session runtime and the normal OpenClaw provider transport is the wrong abstraction. Three examples: a native coding-agent server that owns threads and compaction; a local CLI or daemon that must stream native plan/reasoning/tool events; and a model runtime that needs its own resume id in addition to the OpenClaw session transcript. The anti-pattern: do **not** register a harness just to add a new LLM API — for normal HTTP or WebSocket model APIs build a provider plugin instead (`/plugins/sdk-provider-plugins`).

## What core still owns (`params.runtimePlan`)

Before a harness is selected, OpenClaw has already resolved state the harness does not control: provider and model; runtime auth state; thinking level and context budget; the OpenClaw transcript/session file; workspace, sandbox, and tool policy; channel reply and streaming callbacks; and model fallback plus live model-switching policy. The split is intentional — a harness runs a prepared attempt; it does not pick providers, replace channel delivery, or switch models.

The prepared attempt also includes `params.runtimePlan`, an OpenClaw-owned policy bundle shared across OpenClaw and native harnesses. Its members: `runtimePlan.tools.normalize(...)` and `runtimePlan.tools.logDiagnostics(...)` for provider-aware tool schema policy; `runtimePlan.transcript.resolvePolicy(...)` for transcript sanitization and tool-call repair; `runtimePlan.delivery.isSilentPayload(...)` for shared `NO_REPLY` and media delivery suppression; `runtimePlan.outcome.classifyRunResult(...)` for model fallback classification; and `runtimePlan.observability` for resolved provider/model/harness metadata. Harnesses may use the plan to match OpenClaw behavior but must treat it as host-owned state — do not mutate it or use it to switch providers/models inside a turn.

## Register a harness

The import surface is `openclaw/plugin-sdk/agent-harness`. An `AgentHarness` object has an `id`, a `label`, a `supports(ctx)` predicate returning `{ supported: true, priority }` or `{ supported: false }` for a resolved provider, and an `async runAttempt(params)` that starts or resumes the native thread using prepared fields such as `params.prompt`, `params.tools`, `params.images`, `params.onPartialReply`, and `params.onAgentEvent`. It is wired in through a plugin entry's `register(api)` calling `api.registerAgentHarness(myHarness)`.

```typescript
import type { AgentHarness } from "openclaw/plugin-sdk/agent-harness";
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

const myHarness: AgentHarness = {
  id: "my-harness",
  label: "My native agent harness",

  supports(ctx) {
    return ctx.provider === "my-provider"
      ? { supported: true, priority: 100 }
      : { supported: false };
  },

  async runAttempt(params) {
    // Start or resume your native thread.
    // Use params.prompt, params.tools, params.images, params.onPartialReply,
    // params.onAgentEvent, and the other prepared attempt fields.
    return await runMyNativeTurn(params);
  },
};

export default definePluginEntry({
  id: "my-native-agent",
  name: "My Native Agent",
  description: "Runs selected models through a native agent daemon.",
  register(api) {
    api.registerAgentHarness(myHarness);
  },
});
```

## Selection policy

OpenClaw chooses a harness after provider/model resolution, in a four-step order: (1) model-scoped runtime policy wins; (2) provider-scoped runtime policy next; (3) `auto` asks registered harnesses if they support the resolved provider/model; (4) if none match, OpenClaw uses its embedded runtime. Plugin harness failures surface as run failures; in `auto` mode embedded fallback is used only when no registered plugin harness supports the resolved provider/model. Once a plugin harness has claimed a run, OpenClaw does not replay that turn through another runtime, because that can change auth/runtime semantics or duplicate side effects.

Whole-session and whole-agent runtime pins are ignored by selection — including stale session `agentHarnessId` values, `agents.defaults.agentRuntime`, `agents.list[].agentRuntime`, and `OPENCLAW_AGENT_RUNTIME`. `/status` shows the effective runtime selected from the route, and `agents/harness` debug logging plus the gateway's structured `agent harness selected` record (harness id, selection reason, runtime/fallback policy, per-candidate support result in `auto`) explain a surprising selection. The bundled Codex plugin registers `codex` as its harness id; core treats that as an ordinary plugin harness id, and Codex-specific aliases belong in the plugin or operator config, not the shared selector.

## Provider plus harness pairing

Most harnesses should also register a provider, which makes model refs, auth status, model metadata, and `/model` selection visible to the rest of OpenClaw; the harness then claims that provider in `supports(...)`. The bundled Codex plugin follows this pattern: preferred refs `openai/gpt-5.5`; legacy `codex/gpt-*` refs remain accepted for compatibility; harness id `codex`; auth is synthetic provider availability because the Codex harness owns the native Codex login/session; and for the app-server request OpenClaw sends the bare model id to Codex and lets the harness talk to the native app-server protocol.

The Codex plugin is additive: plain `openai/gpt-*` agent refs on the official OpenAI provider select the Codex harness by default, while older `codex/gpt-*` refs still select the Codex provider and harness for compatibility. For operator setup, model prefix examples, and Codex-only configs see the Codex Harness doc (`/plugins/codex-harness`). OpenClaw requires Codex app-server `0.125.0` or newer: the plugin checks the app-server initialize handshake and blocks older or unversioned servers (the `0.125.0` floor includes the native MCP hook payload support from Codex `0.124.0`).

### Tool-result middleware

Bundled plugins and explicitly enabled installed plugins with matching manifest contracts can attach runtime-neutral tool-result middleware through `api.registerAgentToolResultMiddleware(...)` when their manifest declares the targeted runtime ids in `contracts.agentToolResultMiddleware` — a trusted seam for async tool-result transforms that must run before OpenClaw or Codex feeds tool output back into the model. Legacy bundled plugins can still use `api.registerCodexAppServerExtensionFactory(...)` for Codex app-server-only middleware, but new transforms should use the runtime-neutral API; the embedded-runner-only `api.registerEmbeddedExtensionFactory(...)` hook has been removed.

### Terminal outcome classification

Native harnesses that own their own protocol projection can use `classifyAgentHarnessTerminalOutcome(...)` from `openclaw/plugin-sdk/agent-harness-runtime` when a completed turn produced no visible assistant text. The helper returns `empty`, `reasoning-only`, or `planning-only` so OpenClaw's fallback policy can decide whether to retry on a different model. `planning-only` requires the harness's explicit `planText` field — OpenClaw does not infer it from prose. The helper intentionally leaves prompt errors, in-flight turns, and intentional silent replies such as `NO_REPLY` unclassified.

### Agent-end side effects

Native harnesses must call `runAgentEndSideEffects(...)` from `openclaw/plugin-sdk/agent-harness-runtime` after finalizing an attempt; it dispatches the portable `agent_end` hook and OpenClaw's research capture without delaying interactive replies. Use `awaitAgentEndSideEffects(...)` for local, non-interactive runs where the attempt must not resolve until those side effects finish. Both accept the same `{ event, ctx }` payload as `runAgentHarnessAgentEndHook(...)`; their failures do not alter the attempt result.

### Native Codex harness mode

The bundled `codex` harness is the native Codex mode for embedded OpenClaw agent turns. Enable the bundled `codex` plugin first, and include `codex` in `plugins.allow` if your config uses a restrictive allowlist. Native app-server configs should use `openai/gpt-*`; legacy Codex model-ref routes should be repaired with `openclaw doctor --fix`, and legacy `codex/*` refs remain compatibility aliases. When this mode runs, Codex owns the native thread id, resume behavior, compaction, and app-server execution, while OpenClaw still owns the chat channel, visible transcript mirror, tool policy, approvals, media delivery, and session selection.

## Runtime strictness

By default, OpenClaw uses `auto` provider/model runtime policy: registered plugin harnesses can claim a provider/model pair, and the embedded runtime handles the turn when none match. Use an explicit provider/model plugin runtime such as `agentRuntime.id: "codex"` when missing harness selection should fail closed instead of routing through the embedded runtime — proving the Codex app-server path is actually in use. Selected plugin harness failures always fail hard, and Codex selection/runtime failures are not retried through another runtime; this does not block an explicit `agentRuntime.id: "openclaw"`.

For Codex-only embedded runs, the runtime is pinned on the provider:

```json
{
  "models": {
    "providers": {
      "openai": {
        "agentRuntime": {
          "id": "codex"
        }
      }
    }
  },
  "agents": {
    "defaults": {
      "model": "openai/gpt-5.5"
    }
  }
}
```

To use a CLI backend for one canonical model, the runtime is placed on that model entry (e.g. `anthropic/claude-opus-4-8` → `agentRuntime.id: "claude-cli"`); per-agent overrides use the same model-scoped shape under `agents.list[].models`. By contrast, legacy whole-agent examples at `agents.defaults.agentRuntime` are ignored. With an explicit plugin runtime, a session fails early when the requested harness is not registered, does not support the resolved provider/model, or fails before producing turn side effects. This setting only controls the embedded agent harness; it does not disable image, video, music, TTS, PDF, or other provider-specific model routing.

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-8",
      "models": {
        "anthropic/claude-opus-4-8": {
          "agentRuntime": {
            "id": "claude-cli"
          }
        }
      }
    }
  }
}
```

## Native sessions and transcript mirror

A harness may keep a native session id, thread id, or daemon-side resume token; keep that binding explicitly associated with the OpenClaw session, and keep mirroring user-visible assistant/tool output into the OpenClaw transcript. The transcript remains the compatibility layer for channel-visible session history, transcript search and indexing, switching back to the built-in OpenClaw harness on a later turn, and generic `/new`, `/reset`, and session-deletion behavior. If a harness stores a sidecar binding, implement `reset(...)` so OpenClaw can clear it when the owning session is reset.

## Tool and media results

Core constructs the OpenClaw tool list and passes it into the prepared attempt. When a harness executes a dynamic tool call, it must return the tool result through the harness result shape rather than sending channel media itself, keeping text, image, video, music, TTS, approval, and messaging-tool outputs on the same delivery path as OpenClaw-backed runs.

## Current limitations

Three caveats: the public import path is generic, but some attempt/result type aliases still carry legacy names for compatibility; third-party harness installation is experimental, so prefer provider plugins until you need a native session runtime; and harness switching is supported across turns but must not occur mid-turn after native tools, approvals, assistant text, or message sends start.

**Source**: OpenClaw documentation — `plugins/sdk-agent-harness` (mirror `inbox/openclaw_docs/plugins/sdk-agent-harness.md`)
**Last Updated**: 2026-06-22
**Status**: Active
