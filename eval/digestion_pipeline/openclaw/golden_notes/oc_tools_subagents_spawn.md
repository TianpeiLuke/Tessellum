---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - subagents
keywords:
  - openclaw sessions_spawn
  - subagent spawn contract
  - sessions_yield wait primitive
  - isolated vs fork context mode
  - subagent tool policy
  - sessions_spawn parameters
  - subagent concurrency lane
  - taskName targeting
topics:
  - OpenClaw
  - Sub-agents
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/subagents
access_control_group: ["general"]
---

# OpenClaw — Spawning Sub-agents (`sessions_spawn`, `sessions_yield`, `subagents`)

## Overview

This note is the procedural spawn/delegation contract for OpenClaw sub-agents: background agent runs spawned from an existing run that execute in their own session and announce results back to the requester chat. It covers the `/subagents` inspection command and its thread-binding controls, the `isolated` vs `fork` context modes, the three delegation tools — `sessions_spawn` (the non-blocking spawn, parameters, defaults, delegation-prompt mode, `taskName` targeting), `sessions_yield` (the wait primitive), and `subagents` (the lister) — plus the sub-agent tool-restriction policy and the `subagent` concurrency lane. It mirrors the `tools/subagents` source through Concurrency; the orchestration/lifecycle half (thread-bound session model, nesting, authentication, announce internals, liveness, stopping, limitations) lives in the sibling note.

## Sub-agent Model and Primary Goals

A sub-agent is a background agent run spawned from an existing agent run. It runs in its own session keyed `agent:<agentId>:subagent:<uuid>` and, when finished, **announces** its result back to the requester chat channel. Each sub-agent run is tracked as a background task. The primary goals are: parallelize "research / long task / slow tool" work without blocking the main run; keep sub-agents isolated by default (session separation + optional sandboxing); keep the tool surface hard to misuse (sub-agents do **not** get session tools by default); and support configurable nesting depth for orchestrator patterns.

**Cost note (per source):** each sub-agent has its own context and token usage by default. For heavy or repetitive tasks, set a cheaper model for sub-agents and keep the main agent on a higher-quality model (via `agents.defaults.subagents.model` or per-agent overrides). When a child genuinely needs the requester's current transcript, the agent can request `context: "fork"` on that one spawn. Thread-bound subagent sessions default to `context: "fork"` because they branch the current conversation into a follow-up thread.

## Slash Command: `/subagents`

Use `/subagents` to inspect sub-agent runs for the **current session**:

```text
/subagents list
/subagents log <id|#> [limit] [tools]
/subagents info <id|#>
```

`/subagents info` shows run metadata (status, timestamps, session id, transcript path, cleanup). Use `sessions_history` for a bounded, safety-filtered recall view; inspect the transcript path on disk for the raw full transcript.

### Thread binding controls

These commands work on channels that support persistent thread bindings (see the orchestration note's thread-supporting-channels section): `/focus <subagent-label|session-key|session-id|session-label>`, `/unfocus`, `/agents`, `/session idle <duration|off>`, and `/session max-age <duration|off>`.

### Spawn behavior

Agents start background sub-agents with `sessions_spawn`. Sub-agent completions return as internal parent-session events; the parent/requester agent decides whether a user-facing update is needed. Spawning is **non-blocking and push-based**: `sessions_spawn` returns a run id immediately, and on completion the sub-agent reports back to the parent/requester session. Agent turns that need child results should call `sessions_yield` after spawning required work — that ends the current turn and lets completion events arrive as the next model-visible message. Because completion is push-based, once spawned you do **not** poll `/subagents list`, `sessions_list`, or `sessions_history` in a loop just to wait; inspect status only on-demand for debugging. Child output is a report/evidence for the requester agent to synthesize — not user-authored instruction text, and it cannot override system, developer, or user policy. On completion, OpenClaw best-effort closes tracked browser tabs/processes opened by that session before the announce cleanup flow continues.

Per-run modes are set on the spawn: `--model` and `--thinking` override defaults for that run; use `info`/`log` to inspect details after completion. For persistent thread-bound sessions, use `sessions_spawn` with `thread: true` and `mode: "session"`; if the channel does not support thread bindings, use `mode: "run"` instead of retrying impossible thread-bound combinations. For ACP harness sessions (Claude Code, Gemini CLI, OpenCode, or explicit Codex ACP/acpx), use `runtime: "acp"` when the tool advertises that runtime; when the `codex` plugin is enabled, Codex chat/thread control should prefer `/codex ...` over ACP unless the user explicitly asks for ACP/acpx. OpenClaw hides `runtime: "acp"` until ACP is enabled, the requester is not sandboxed, and a backend plugin such as `acpx` is loaded.

## Context Modes

Native sub-agents start isolated unless the caller explicitly asks to fork the current transcript. There are two context modes:

- **`isolated`** (default) — for fresh research, independent implementation, slow tool work, or anything briefed in the task text. Creates a clean child transcript and keeps token use lower.
- **`fork`** — for work that depends on the current conversation, prior tool results, or nuanced instructions already in the requester transcript. Branches the requester transcript into the child session before the child starts.

Use `fork` sparingly. It is for context-sensitive delegation, not a replacement for writing a clear task prompt.

## Tool: `sessions_spawn`

`sessions_spawn` starts a sub-agent run with `deliver: false` on the global `subagent` lane, then runs an announce step and posts the announce reply to the requester chat channel. Availability depends on the caller's effective tool policy: the `coding` and `full` profiles expose `sessions_spawn` by default; the `messaging` profile does not — add `tools.alsoAllow: ["sessions_spawn", "sessions_yield", "subagents"]` or use `tools.profile: "coding"`. Channel/group, provider, sandbox, and per-agent allow/deny policies can still remove the tool after the profile stage. Use `/tools` from the same session to confirm the effective tool list.

**Defaults:**

- **Model:** native sub-agents inherit the caller unless you set `agents.defaults.subagents.model` (or per-agent `agents.list[].subagents.model`). ACP runtime spawns use the same configured subagent model when present; otherwise the ACP harness keeps its own default. An explicit `sessions_spawn.model` still wins.
- **Thinking:** native sub-agents inherit the caller unless you set `agents.defaults.subagents.thinking` (or per-agent `agents.list[].subagents.thinking`). ACP runtime spawns also apply `agents.defaults.models["provider/model"].params.thinking` for the selected model. An explicit `sessions_spawn.thinking` still wins.
- **Run timeout:** OpenClaw uses `agents.defaults.subagents.runTimeoutSeconds` when set; otherwise it falls back to `0` (no timeout). `sessions_spawn` does not accept per-call timeout overrides.
- **Task delivery:** native sub-agents receive the delegated task in their first visible `[Subagent Task]` message. The sub-agent system prompt carries runtime rules and routing context, not a hidden duplicate of the task.

Accepted native sub-agent spawns include resolved child model metadata in the tool result: `resolvedModel` holds the applied model ref and `resolvedProvider` holds the provider prefix when the ref has one.

### Delegation prompt mode

`agents.defaults.subagents.delegationMode` controls prompt guidance only; it does not change tool policy or enforce delegation. `suggest` (default) keeps the standard prompt nudge to use sub-agents for larger or slower work; `prefer` tells the main agent to stay responsive and delegate anything more involved than a direct reply through `sessions_spawn`. Per-agent override: `agents.list[].subagents.delegationMode`.

```json5
{
  agents: {
    defaults: {
      subagents: {
        delegationMode: "prefer",
        maxConcurrent: 4,
      },
    },
    list: [
      {
        id: "coordinator",
        subagents: { delegationMode: "prefer" },
      },
    ],
  },
}
```

### Tool parameters

| Parameter | Type | Default | Meaning (verbatim from source) |
|---|---|---|---|
| `task` | `string` (required) | — | The task description for the sub-agent. |
| `taskName` | `string` | — | Optional stable handle for identifying a specific child in later status output. Must match `[a-z][a-z0-9_-]{0,63}` and cannot be reserved targets such as `last` or `all`. |
| `label` | `string` | — | Optional human-readable label. |
| `agentId` | `string` | — | Spawn under another configured agent id when allowed by `subagents.allowAgents`. |
| `cwd` | `string` | — | Optional task working directory for the child run. Native sub-agents still load bootstrap files from the target agent workspace; `cwd` only changes where runtime tools and CLI harnesses do the delegated work. |
| `runtime` | `"subagent" \| "acp"` | `subagent` | `acp` is only for external ACP harnesses (`claude`, `droid`, `gemini`, `opencode`, or explicitly requested Codex ACP/acpx) and for `agents.list[]` entries whose `runtime.type` is `acp`. |
| `resumeSessionId` | `string` | — | ACP-only. Resumes an existing ACP harness session when `runtime: "acp"`; ignored for native sub-agent spawns. |
| `streamTo` | `"parent"` | — | ACP-only. Streams ACP run output to the parent session when `runtime: "acp"`; omit for native sub-agent spawns. |
| `model` | `string` | — | Override the sub-agent model. Invalid values are skipped and the sub-agent runs on the default model with a warning in the tool result. |
| `thinking` | `string` | — | Override thinking level for the sub-agent run. |
| `thread` | `boolean` | `false` | When `true`, requests channel thread binding for this sub-agent session. |
| `mode` | `"run" \| "session"` | `run` | If `thread: true` and `mode` omitted, default becomes `session`. `mode: "session"` requires `thread: true`. If thread binding is unavailable for the requester channel, use `mode: "run"`. |
| `cleanup` | `"delete" \| "keep"` | `keep` | `"delete"` archives immediately after announce (still keeps the transcript via rename). |
| `sandbox` | `"inherit" \| "require"` | `inherit` | `require` rejects spawn unless the target child runtime is sandboxed. |
| `context` | `"isolated" \| "fork"` | `isolated` | `fork` branches the requester's current transcript into the child session. Native sub-agents only. Thread-bound spawns default to `fork`; non-thread spawns default to `isolated`. |

Per the source warning, `sessions_spawn` does **not** accept channel-delivery params (`target`, `channel`, `to`, `threadId`, `replyTo`, `transport`). Native sub-agents report their latest assistant turn back to the requester; external delivery stays with the parent/requester agent.

### Task names and targeting

`taskName` is a model-facing handle for orchestration, not a session key. Use it for stable child names such as `review_subagents`, `linux_validation`, or `docs_update` when a coordinator may need to inspect that child later. Target resolution accepts exact `taskName` matches and unambiguous prefixes; matching is scoped to the same active/recent target window used by numbered `/subagents` targets, so a stale completed child does not make a reused handle ambiguous. If two active or recent children share a `taskName`, the target is ambiguous — use the list index, session key, or run id instead. The reserved targets `last` and `all` are not valid `taskName` values because they already have control meanings.

## Tool: `sessions_yield`

`sessions_yield` ends the current model turn and waits for runtime events — primarily sub-agent completion events — to arrive as the next message. Use it after spawning required child work when the requester cannot produce a final answer until those completions arrive. It is the waiting primitive: do not replace it with polling loops over `subagents`, `sessions_list`, `sessions_history`, shell `sleep`, or process polling. Only use `sessions_yield` when the session's effective tool list includes it; some minimal or custom tool profiles expose `sessions_spawn` and `subagents` without `sessions_yield`, and in that case you must not invent a polling loop just to wait for completion.

When active children exist, OpenClaw injects a compact runtime-generated `Active Subagents` prompt block into normal turns so the requester can see the current child sessions, run ids, statuses, labels, tasks, and `taskName` aliases without polling. The task and label fields in that block are quoted as data, not instructions, because they can originate from user/model-provided spawn arguments.

## Tool: `subagents`

The `subagents` tool lists spawned sub-agent runs owned by the requester session. It is scoped to the current requester; a child can only see its own controlled children. Use `subagents` for on-demand status and debugging; use `sessions_yield` to wait for completion events.

## Tool Policy

Sub-agents use the same profile and tool-policy pipeline as the parent or target agent first; then OpenClaw applies the sub-agent restriction layer. With no restrictive `tools.profile`, sub-agents get **all tools except the message tool, session tools, and system tools** — specifically denied are `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, and `message`. `sessions_history` remains a bounded, sanitized recall view here too — not a raw transcript dump. When `maxSpawnDepth >= 2`, depth-1 orchestrator sub-agents additionally receive `sessions_spawn`, `subagents`, `sessions_list`, and `sessions_history` to manage their children.

### Override via config

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxConcurrent: 1,
      },
    },
  },
  tools: {
    subagents: {
      tools: {
        // deny wins
        deny: ["gateway", "cron"],
        // if allow is set, it becomes allow-only (deny still wins)
        // allow: ["read", "exec", "process"]
      },
    },
  },
}
```

`tools.subagents.tools.allow` is a final allow-only filter: it can narrow the already-resolved tool set, but cannot **add back** a tool removed by `tools.profile`. For example, `tools.profile: "coding"` includes `web_search`/`web_fetch` but not the `browser` tool; to let coding-profile sub-agents use browser automation, add browser at the profile stage with `tools.alsoAllow: ["browser"]`. Use per-agent `agents.list[].tools.alsoAllow: ["browser"]` when only one agent should get browser automation.

## Concurrency

Sub-agents use a dedicated in-process queue lane:

- **Lane name:** `subagent`
- **Concurrency:** `agents.defaults.subagents.maxConcurrent` (default `8`)

**Source**: OpenClaw documentation — `tools/subagents` (mirror `inbox/openclaw_docs/tools/subagents.md`)
**Last Updated**: 2026-06-22
**Status**: Active
