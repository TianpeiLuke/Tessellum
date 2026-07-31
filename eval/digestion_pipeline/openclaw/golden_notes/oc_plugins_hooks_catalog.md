---
tags:
  - resource
  - documentation
  - openclaw
  - plugins
  - hooks
keywords:
  - openclaw plugin hooks
  - api.on register hook
  - before_tool_call require approval
  - tool call policy block rewrite
  - resolve_exec_env exec environment
  - tool_result_persist details
  - before_agent_run before_prompt_build
  - message_sending reply_payload_sending
  - session extensions next-turn injection
  - hooks timeoutMs priority
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

# OpenClaw — Plugin Hook Catalog (Registering, Tool, Prompt, and Message Hooks)

## Overview

This note is the procedure for registering and using OpenClaw **plugin hooks** — in-process extension points a plugin uses to inspect or change agent runs, tool calls, message flow, and session state. It mirrors the runtime-hooks half of the `plugins/hooks` source page: `api.on(...)` registration with timeout/priority ordering, the per-surface hook catalog, debug runtime hooks, the `before_tool_call` tool-call policy plus exec-environment and tool-result-persistence sub-hooks, the prompt-and-model hooks, session extensions / next-turn injections, and message-delivery hooks. Install / gateway-lifecycle hooks and upcoming deprecations are the companion note [oc_plugins_hooks_lifecycle_install](oc_plugins_hooks_lifecycle_install.md). Plugin hooks differ from operator-installed **internal hooks** (`HOOK.md` scripts for command/Gateway events such as `/new`, `/reset`, `/stop`, `agent:bootstrap`, `gateway:startup`), documented at `/automation/hooks`.

## Quick start — registering hooks

Register typed plugin hooks with `api.on(...)` from your plugin entry (exported via `definePluginEntry`). The example below claims `before_tool_call` for `web_search` and requires approval before it runs:

```typescript
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

export default definePluginEntry({
  id: "tool-preflight",
  name: "Tool Preflight",
  register(api) {
    api.on(
      "before_tool_call",
      async (event) => {
        if (event.toolName !== "web_search") {
          return;
        }

        return {
          requireApproval: {
            title: "Run web search",
            description: `Allow search query: ${String(event.params.query ?? "")}`,
            severity: "info",
            timeoutMs: 60_000,
            timeoutBehavior: "deny",
          },
        };
      },
      { priority: 50 },
    );
  },
});
```

Hook handlers run **sequentially in descending `priority`** (higher runs first); same-priority hooks keep registration order. `api.on(name, handler, opts?)` accepts `priority` and `timeoutMs` (an optional per-hook budget — the runner aborts that handler after the budget elapses and continues, rather than letting slow work consume the caller's model timeout; omit it for the default observation/decision timeout). Each hook receives `event.context.pluginConfig`, the resolved config for the registering plugin, injected per handler without mutating the shared event.

Operators can set hook budgets without patching plugin code via `plugins.entries.<id>.hooks`:

```json
{
  "plugins": {
    "entries": {
      "my-plugin": {
        "hooks": {
          "timeoutMs": 30000,
          "timeouts": {
            "before_prompt_build": 90000,
            "agent_end": 60000
          }
        }
      }
    }
  }
}
```

Precedence: `hooks.timeouts.<hookName>` overrides `hooks.timeoutMs`, which overrides the plugin-authored `api.on(..., { timeoutMs })` value. Each configured value must be a positive integer ≤ **600000** ms. Prefer per-hook overrides for known slow hooks so one plugin does not get a longer budget across the board.

## Hook catalog

Hooks are grouped by the surface they extend. Names in **bold** accept a **decision result** (block, cancel, override, require approval); all others are observation-only.

**Agent turn** — `before_model_resolve` (override provider/model before session messages load); `agent_turn_prepare` (consume queued turn injections, add same-turn context before prompt hooks); `before_prompt_build` (add dynamic/system-prompt context before the model call); `before_agent_start` (compatibility-only combined phase); **`before_agent_run`** (inspect the final prompt/messages before submission, optionally block); **`before_agent_reply`** (short-circuit the turn with a synthetic reply or silence); **`before_agent_finalize`** (inspect the natural final answer, request one more pass); `agent_end` (observe final messages, success state, duration); `heartbeat_prompt_contribution` (add heartbeat-only context).

**Conversation observation** — `model_call_started` / `model_call_ended` (sanitized provider/model call metadata, timing, outcome, bounded request-id hashes — no prompt/response content); `llm_input` (system prompt, prompt, history); `llm_output` (provider output, usage, resolved `contextTokenBudget`).

**Tools** — **`before_tool_call`** (rewrite params, block, or require approval); `after_tool_call` (observe results, errors, duration); `resolve_exec_env` (contribute plugin-owned env vars to `exec`); **`tool_result_persist`** (rewrite the assistant message from a tool result); **`before_message_write`** (inspect/block an in-progress message write — rare).

**Messages and delivery** — **`inbound_claim`** (claim an inbound message before routing, for synthetic replies); `message_received` (observe inbound content/sender/thread/metadata); **`message_sending`** (rewrite outbound content or cancel); **`reply_payload_sending`** (mutate/cancel normalized reply payloads); `message_sent` (observe delivery success/failure); **`before_dispatch`** (inspect/rewrite an outbound dispatch before channel handoff); **`reply_dispatch`** (participate in the final reply-dispatch pipeline).

**Sessions and compaction** — `session_start` / `session_end` (lifecycle boundaries; `reason` ∈ `new`, `reset`, `idle`, `daily`, `compaction`, `deleted`, `shutdown`, `restart`, `unknown`); `before_compaction` / `after_compaction` (observe/annotate compaction); `before_reset` (observe `/reset` or programmatic resets).

**Subagents** — `subagent_spawned` / `subagent_ended` (observe launch/completion; `subagent_spawned` includes `resolvedModel` and `resolvedProvider` when the child's native model is resolved before launch); `subagent_delivery_target` (compatibility hook for completion delivery when no core session binding projects a route); `subagent_spawning` (deprecated — core now prepares `thread: true` subagent bindings via channel session-binding adapters before `subagent_spawned`).

**Lifecycle** — `gateway_start` / `gateway_stop`, `deactivate` (deprecated alias for `gateway_stop`), `cron_changed`, and **`before_install`** are detailed in the lifecycle/install companion note (see Related Notes).

## Debug runtime hooks

Use `before_model_resolve` to switch the provider or model for a turn — it runs before model resolution, whereas `llm_output` only runs after a model attempt produces assistant output. To verify the effective session model, inspect runtime registrations then use `openclaw sessions` or Gateway session/status surfaces. When debugging provider payloads, start the Gateway with `--raw-stream` and `--raw-stream-path <path>` to write raw stream events to jsonl.

### Exec environment hook

`resolve_exec_env` lets plugins contribute environment variables to `exec` invocations after the base exec environment is built and before the command runs. It receives `event.sessionKey`, `event.toolName` (currently always `"exec"`), `event.host` (`"gateway"`, `"sandbox"`, or `"node"`), and context fields such as `ctx.agentId`, `ctx.sessionKey`, `ctx.messageProvider`, `ctx.channelId`. Return a `Record<string, string>` to merge in; handlers run in priority order, later results overriding earlier ones for the same key. Output is filtered through the host exec-environment key policy first — invalid keys, `PATH`, and dangerous override keys (`LD_*`, `DYLD_*`, `NODE_OPTIONS`, proxy and TLS override variables) are dropped; the filtered env is included in gateway approval/audit metadata and forwarded to node-host execution.

### Tool result persistence

Tool results can include structured `details` for UI rendering, diagnostics, media routing, or plugin-owned metadata. Treat `details` as runtime metadata, not prompt content: OpenClaw strips `toolResult.details` before provider replay and compaction input; persisted entries keep only bounded `details` (oversized ones become a summary plus `persistedDetailsTruncated: true`); `tool_result_persist` and `before_message_write` run before the final persistence cap. Keep returned `details` small and put model-visible tool output in `content`.

## Tool call policy

`before_tool_call` receives `event.toolName`, `event.params`, optional `event.toolKind` and `event.toolInputKind` (host-authoritative discriminators for tools that share names — e.g. outer code-mode `exec` uses `toolKind: "code_mode_exec"` with `toolInputKind: "javascript" | "typescript"` when known), optional `event.derivedPaths` (best-effort host-derived target-path hints for well-known envelopes such as `apply_patch`; may be incomplete/over-approximate), optional `event.runId` and `event.toolCallId`, and context fields such as `ctx.agentId`, `ctx.sessionKey`, `ctx.sessionId`, `ctx.runId`, `ctx.jobId` (cron runs), `ctx.toolKind`, `ctx.toolInputKind`, `ctx.trace`. It can return:

```typescript
type BeforeToolCallResult = {
  params?: Record<string, unknown>;
  block?: boolean;
  blockReason?: string;
  requireApproval?: {
    title: string;
    description: string;
    severity?: "info" | "warning" | "critical";
    timeoutMs?: number;
    timeoutBehavior?: "allow" | "deny";
    allowedDecisions?: Array<"allow-once" | "allow-always" | "deny">;
    pluginId?: string;
    onResolution?: (
      decision: "allow-once" | "allow-always" | "deny" | "timeout" | "cancelled",
    ) => Promise<void> | void;
  };
};
```

Guard behavior: `block: true` is terminal and skips lower-priority handlers; `block: false` is no decision; `params` rewrites the tool parameters for execution; `requireApproval` pauses the run and asks the user through plugin approvals (the `/approve` command approves both exec and plugin approvals; in Codex app-server report-mode native `PreToolUse` relays it defers to the matching app-server approval request); a lower-priority `block: true` can still block after a higher-priority approval request; `onResolution` receives the resolved decision — `allow-once`, `allow-always`, `deny`, `timeout`, or `cancelled`.

Plugins needing host-level policy register **trusted tool policies** with `api.registerTrustedToolPolicy(...)`, which run before ordinary `before_tool_call` hooks and normal decisions (bundled trusted policies first, installed-plugin trusted policies next in plugin-load order, then ordinary `before_tool_call` hooks). Installed plugins must be explicitly enabled and declare every policy id in `contracts.trustedToolPolicies` (undeclared ids rejected; ids scoped per plugin). Use this tier only for host-trusted gates such as workspace policy or budget enforcement.

## Prompt and model hooks

Use the phase-specific hooks for new plugins: `before_model_resolve` receives only the prompt and attachment metadata, returns `providerOverride` or `modelOverride`; `agent_turn_prepare` receives the prompt, prepared session messages, and exactly-once queued injections drained for this session, returns `prependContext` or `appendContext`; `before_prompt_build` receives the prompt and session messages, returns `prependContext`, `appendContext`, `systemPrompt`, `prependSystemContext`, or `appendSystemContext`; `heartbeat_prompt_contribution` runs only for heartbeat turns, returns `prependContext` or `appendContext` (for background monitors). `before_agent_start` remains a legacy combined-phase compatibility hook — prefer the explicit hooks above.

`before_agent_run` runs after prompt construction and before any model input (including prompt-local image loading and `llm_input` observation). It receives the user input as `prompt`, plus session history `messages` and the active system prompt. Return `{ outcome: "block", reason, message? }` to stop the run before the model reads the prompt — `reason` is internal, `message` is the user-facing replacement; the only supported outcomes are `pass` and `block` (unsupported shapes fail closed). On block, OpenClaw stores only the replacement text in `message.content` plus non-sensitive block metadata (blocking plugin id, timestamp); the original user text is not retained, and internal block reasons are excluded from transcript, history, broadcast, log, and diagnostics.

`before_agent_start` and `agent_end` include `event.runId` (also on `ctx.runId`) when identifiable; cron runs also expose `ctx.jobId`, and channel-originated runs expose `ctx.messageProvider` (e.g. `discord`, `telegram`) and `ctx.channelId` when derivable. `agent_end` is an observation hook: Gateway/persistent-harness paths run it fire-and-forget, while one-shot CLI paths wait for the hook promise before cleanup so trusted plugins can flush observability; the runner applies a **30 second** timeout (logged, OpenClaw continues — it does not cancel plugin-owned network work unless the plugin uses its own abort signal).

Use `model_call_started` and `model_call_ended` for provider-call telemetry that must not receive raw prompts, history, responses, headers, request bodies, or provider request IDs. They include `runId`, `callId`, `provider`, `model`, optional `api`/`transport`, terminal `durationMs`/`outcome`, and `upstreamRequestIdHash` (a bounded request-id hash when derivable); with resolved context-window metadata they also include `contextTokenBudget` (effective budget after model/config/agent caps) plus `contextWindowSource` and `contextWindowReferenceTokens` when a lower cap applied.

`before_agent_finalize` runs only when a harness is about to accept a natural final answer — not the `/stop` cancellation path and not when the user aborts. Return `{ action: "revise", reason }` for one more model pass, `{ action: "finalize", reason? }` to force finalization, or omit a result to continue (Codex native `Stop` hooks relay into this hook as `before_agent_finalize` decisions). With `action: "revise"`, plugins can include `retry` metadata (type `BeforeAgentFinalizeRetry`) to make the extra pass bounded and replay-safe: `instruction` (appended to the revision reason), `idempotencyKey` (counts retries for the same request across equivalent finalize decisions), and `maxAttempts` (caps extra passes). Non-bundled plugins needing raw conversation hooks (`before_model_resolve`, `before_agent_reply`, `llm_input`, `llm_output`, `before_agent_finalize`, `agent_end`, `before_agent_run`) must set `plugins.entries.<id>.hooks.allowConversationAccess: true`; prompt-mutating hooks and durable next-turn injections can be disabled with `plugins.entries.<id>.hooks.allowPromptInjection=false`.

### Session extensions and next-turn injections

Workflow plugins persist small JSON-compatible session state with `api.registerSessionExtension(...)` and update it through the Gateway `sessions.pluginPatch` method; session rows project that state through `pluginExtensions`, letting Control UI and other clients render plugin-owned status without learning plugin internals. Use `api.enqueueNextTurnInjection(...)` when a plugin needs durable context to reach the next model turn exactly once — OpenClaw drains queued injections before prompt hooks, drops expired ones, and deduplicates by `idempotencyKey` per plugin (the seam for approval resumes, policy summaries, background-monitor deltas, and command continuations the model should see next turn without becoming permanent system-prompt text). Cleanup is part of the contract: session-extension and runtime-lifecycle cleanup callbacks receive `reset`, `delete`, `disable`, or `restart`; reset/delete/disable remove the plugin's persistent state and pending injections, while restart keeps durable session state and lets callbacks release scheduler jobs, run context, and other out-of-band resources for the old generation.

## Message hooks

Use message hooks for channel-level routing and delivery policy: `message_received` observes inbound content, sender, `threadId`, `messageId`, `senderId`, optional run/session correlation, and metadata; `message_sending` rewrites `content` or returns `{ cancel: true }`; `reply_payload_sending` rewrites normalized `ReplyPayload` objects (`presentation`, `delivery`, media refs, text) or returns `{ cancel: true }`; `message_sent` observes final success/failure. For audio-only TTS replies, `content` may carry the hidden spoken transcript with no visible text/caption — rewriting it updates the hook-visible transcript only. `reply_payload_sending` may include `usageState`, a best-effort live per-turn model/usage/context snapshot (omitted for durable delivery and uncorrelated replies).

Message hook contexts expose stable correlation fields when available: `ctx.sessionKey`, `ctx.runId`, `ctx.messageId`, `ctx.senderId`, `ctx.trace`, `ctx.traceId`, `ctx.spanId`, `ctx.parentSpanId`, `ctx.callDepth`. Inbound and `before_dispatch` contexts also expose quoted-reply metadata: `replyToId`, `replyToIdFull`, `replyToBody`, `replyToSender`, `replyToIsQuote`. Prefer these first-class fields (and typed `threadId` / `replyToId`) over legacy metadata.

Decision rules: `message_sending` `cancel: true` is terminal, `cancel: false` is no decision; rewritten `content` continues to lower-priority hooks unless a later hook cancels; `reply_payload_sending` runs after normalization and before channel delivery (handlers sequential, each seeing higher-priority output) and cannot grant local media trust (`trustedLocalMedia` not exposed); `message_sending` can return `cancelReason` + bounded `metadata` (new lifecycle APIs surface a suppressed delivery with reason `cancelled_by_message_sending_hook`; legacy delivery returns an empty array); `message_sent` is observation-only (failures logged, not propagated).

**Source**: OpenClaw documentation — `plugins/hooks` (mirror `inbox/openclaw_docs/plugins/hooks.md`)
**Last Updated**: 2026-06-22
**Status**: Active
