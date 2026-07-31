---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - agent_loop
keywords:
  - openclaw agent loop
  - agent loop lifecycle
  - runEmbeddedAgent
  - lifecycle assistant tool streams
  - agent.wait waitForAgentRun
  - session write lock
  - plugin hooks agent lifecycle
  - agent timeout hierarchy
topics:
  - OpenClaw
  - Agent Loop
language: markdown
date of note: 2026-06-22
status: active
building_block: model
source_url: https://docs.openclaw.ai/concepts/agent-loop
access_control_group: ["general"]
---

# OpenClaw — The Agent Loop Lifecycle

## Overview

This note models the OpenClaw **agent loop**: the single, serialized per-session run that turns an inbound message into actions and a final reply while keeping session state consistent. It covers the RPC entry points, the four-stage dispatch from `agent` through `runEmbeddedAgent`, the three event streams (`lifecycle` / `assistant` / `tool`), the internal and plugin hook points, queueing under the session write lock, reply shaping, compaction retries, and the timeout hierarchy — mirroring the `concepts/agent-loop` source page.

## Entry Points and Dispatch Flow

An OpenClaw loop is the full "real" run of an agent — intake → context assembly → model inference → tool execution → streaming replies → persistence — and is the authoritative path turning a message into a reply. It is entered through the Gateway RPC methods `agent` and `agent.wait`, or the `agent` CLI command. The run proceeds in four stages:

1. The **`agent` RPC** validates params, resolves the session (by `sessionKey` / `sessionId`), persists session metadata, and returns `{ runId, acceptedAt }` immediately — the run continues asynchronously.
2. **`agentCommand`** runs the agent: it resolves the model plus thinking/verbose/trace defaults, loads the skills snapshot, calls `runEmbeddedAgent` (the OpenClaw agent runtime), and emits a fallback **lifecycle end/error** if the embedded loop does not emit one itself.
3. **`runEmbeddedAgent`** serializes runs via per-session and optional global queues, resolves the model and auth profile, builds the OpenClaw session, subscribes to runtime events while streaming assistant/tool deltas, enforces the timeout (aborting the run if exceeded), and returns payloads plus usage metadata. For Codex app-server turns it aborts an accepted turn that stops producing app-server progress before a terminal event.
4. **`subscribeEmbeddedAgentSession`** bridges agent-runtime events onto the OpenClaw `agent` stream: tool events become `stream: "tool"`, assistant deltas become `stream: "assistant"`, and lifecycle events become `stream: "lifecycle"` with `phase: "start" | "end" | "error"`.

The waiting variant, **`agent.wait`**, uses `waitForAgentRun` to wait for the **lifecycle end/error** for a given `runId` and returns `{ status: ok|error|timeout, startedAt, endedAt, error? }`.

## Queueing, Concurrency, and the Session Write Lock

Runs are serialized per session key (a session lane) and optionally through a global lane, which prevents tool/session races and keeps session history consistent. Messaging channels can pick queue modes — steer, followup, collect, or interrupt — that feed this lane system. Transcript writes are additionally protected by a **session write lock** on the session file: the lock is process-aware and file-based, so it catches writers that bypass the in-process queue or come from another process. Transcript writers wait up to `session.writeLock.acquireTimeoutMs` (default `60000` ms) before reporting the session as busy. The lock is non-reentrant by default; a helper that intentionally nests acquisition of the same lock while preserving one logical writer must opt in with `allowReentrant: true`.

During session and workspace preparation the workspace is resolved and created (sandboxed runs may redirect to a sandbox workspace root), skills are loaded or reused from a snapshot and injected into env and prompt, and bootstrap/context files are resolved into the system-prompt report. The session write lock is acquired and `SessionManager` is opened before streaming; any later transcript rewrite, compaction, or truncation path must take the same lock before opening or mutating the transcript file.

## Hook Points

OpenClaw exposes two hook systems the loop passes through. **Internal hooks (Gateway hooks)** are event-driven scripts for commands and lifecycle events: `agent:bootstrap` runs while building bootstrap files before the system prompt is finalized (to add/remove bootstrap context files), and **command hooks** fire on `/new`, `/reset`, `/stop`, and other command events. **Plugin hooks** run inside the agent loop or gateway pipeline:

- `before_model_resolve` — runs pre-session (no `messages`) to deterministically override provider/model before model resolution.
- `before_prompt_build` — runs after session load (with `messages`) to inject `prependContext`, `systemPrompt`, `prependSystemContext`, or `appendSystemContext` before prompt submission.
- `before_agent_start` — legacy compatibility hook that may run in either phase; the explicit hooks above are preferred.
- `before_agent_reply` — runs after inline actions and before the LLM call, letting a plugin claim the turn with a synthetic reply or silence it.
- `agent_end` — inspects the final message list and run metadata after completion.
- `before_compaction` / `after_compaction` — observe or annotate compaction cycles.
- `before_tool_call` / `after_tool_call` — intercept tool params/results.
- `before_install` — inspects staged skill/plugin install material after operator install policy runs.
- `tool_result_persist` — synchronously transforms tool results before they are written to an OpenClaw-owned transcript.
- `message_received` / `message_sending` / `message_sent` — inbound and outbound message hooks.
- `session_start` / `session_end` and `gateway_start` / `gateway_stop` — session and gateway lifecycle boundaries.

For outbound/tool guards the decision rules are explicit: `before_tool_call` and `before_install` treat `{ block: true }` as terminal (stopping lower-priority handlers) and `{ block: false }` as a no-op that does not clear a prior block; `message_sending` treats `{ cancel: true }` as terminal and `{ cancel: false }` as a no-op. Operator-owned install allow/block decisions that must cover CLI install and update paths should use `security.installPolicy`, not `before_install`. Harnesses may adapt these hooks differently — the Codex app-server harness keeps OpenClaw plugin hooks as the compatibility contract for documented mirrored surfaces, while Codex native hooks remain a separate lower-level mechanism.

## Streaming, Tools, and Reply Shaping

Assistant deltas are streamed from the agent runtime and emitted as `assistant` events; block streaming can emit partial replies on either `text_end` or `message_end`, and reasoning streaming can be a separate stream or block replies. Tool start/update/end events are emitted on the `tool` stream, tool results are sanitized for size and image payloads before logging/emitting, and messaging-tool sends are tracked to suppress duplicate assistant confirmations. Final payloads are assembled from assistant text (and optional reasoning), inline tool summaries (when verbose and allowed), and assistant error text when the model errors; the silent token `NO_REPLY` / `no_reply` is filtered from outgoing payloads, messaging-tool duplicates are removed, and if no renderable payloads remain after a tool error a fallback tool-error reply is emitted (unless a messaging tool already sent a user-visible reply). The three event streams emitted today are `lifecycle` (from `subscribeEmbeddedAgentSession`, with a fallback from `agentCommand`), `assistant` (streamed deltas), and `tool` (streamed tool events). For chat channels, assistant deltas are buffered into chat `delta` messages and a chat `final` is emitted on lifecycle end/error.

## Compaction, Timeouts, and Early Exit

Auto-compaction emits `compaction` stream events and can trigger a retry; on retry, in-memory buffers and tool summaries are reset to avoid duplicate output. The timeout hierarchy spans several layers: `agent.wait` defaults to 30s (the wait only, overridable via `timeoutMs`); the agent runtime uses `agents.defaults.timeoutSeconds` (default 172800s / 48 hours) enforced by the `runEmbeddedAgent` abort timer; the cron runtime owns an isolated agent-turn `timeoutSeconds`, starting the timer at execution, aborting at the deadline, then running bounded cleanup before recording the timeout so a stale child session cannot keep the lane stuck. A model idle timeout aborts a model request when no chunks arrive before the idle window — `models.providers.<id>.timeoutSeconds` extends this idle watchdog for slow local/self-hosted providers but stays bounded by any lower `agents.defaults.timeoutSeconds` or run-specific timeout (default cap 120s when no agent default is configured; cron runs with no explicit timeout disable the idle watchdog and rely on the cron outer timeout). The same provider `timeoutSeconds` also governs that provider's HTTP fetches (connect, headers, body, SDK request timeout, guarded-fetch abort, and stream idle watchdog). Session liveness diagnostics (when enabled) classify long `processing` sessions via `diagnostics.stuckSessionWarnMs`: active runs/model/tool calls report `session.long_running`, active work with no recent progress reports `session.stalled`, and `session.stuck` is reserved for recoverable stale bookkeeping — stalled embedded runs are abort-drained only after `diagnostics.stuckSessionAbortMs` (default at least 5 minutes and 3× the warning threshold). A run can end early through agent timeout (abort), `AbortSignal` (cancel), Gateway disconnect or RPC timeout, or an `agent.wait` timeout (which is wait-only and does not stop the agent).

**Source**: OpenClaw documentation — `concepts/agent-loop` (mirror `inbox/openclaw_docs/concepts/agent-loop.md`)
**Last Updated**: 2026-06-22
**Status**: Active
