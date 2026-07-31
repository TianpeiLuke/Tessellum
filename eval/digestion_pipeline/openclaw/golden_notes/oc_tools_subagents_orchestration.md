---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - subagents
keywords:
  - openclaw subagent orchestration
  - nested subagents maxSpawnDepth
  - orchestrator pattern announce chain
  - thread-bound subagent sessions
  - subagent tool policy by depth
  - subagent liveness recovery orphan
  - cascade stop subagents
  - subagent authentication agent id
topics:
  - OpenClaw
  - Sub-agent Orchestration
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/tools/subagents
access_control_group: ["general"]
---

# OpenClaw — Sub-agent Orchestration and Lifecycle

## Overview

This note models the **orchestration and lifecycle** half of OpenClaw sub-agents from the `tools/subagents` source page, covering every section from "Thread-bound sessions" onward: thread-binding controls and config, the nested-depth model with depth-level tool policy and the announce chain, per-agent-id authentication, the announce step (context block, stats line, why `sessions_history` is the safer recall path), liveness/orphan-recovery, stopping/cascade, and limitations. The complementary spawn/tool-surface half lives in [oc_tools_subagents_spawn](oc_tools_subagents_spawn.md).

A sub-agent is a background agent run spawned from an existing run; it executes in its own session keyed `agent:<agentId>:subagent:<uuid>`, is tracked as a background task, and when finished **announces** its result back to the requester chat channel. Orchestration is what happens around that run — its binding to a conversation, its place in a depth hierarchy, the credentials it resolves, the delivery path of its result, and how OpenClaw keeps the tree consistent across restarts.

## Thread-bound Sessions

When thread bindings are enabled for a channel, a sub-agent can stay **bound** to a thread so follow-up user messages there keep routing to the same session, turning a one-shot spawn into a persistent conversational lane. A thread-bound session is created by `sessions_spawn` with `thread: true` (optionally `mode: "session"`); because it branches the current conversation into a follow-up thread, it defaults to `context: "fork"`.

**Thread supporting channels.** Any channel with a session-binding adapter can support persistent thread-bound subagent sessions. Bundled adapters currently include **Discord threads, Matrix threads, Telegram forum topics, and current-conversation bindings for Feishu**; per-channel `threadBindings` keys control enablement, timeouts, and `spawnSessions`.

**Quick flow.** (1) Spawn with `thread: true`; (2) OpenClaw creates or binds a thread to that session target in the active channel; (3) replies and follow-ups in that thread route to the bound session; (4) `/session idle` inspects/updates inactivity auto-unfocus and `/session max-age` the hard cap; (5) `/unfocus` detaches manually.

**Manual controls.** These commands work only on channels supporting persistent thread bindings:

| Command | Effect |
| --- | --- |
| `/focus <target>` | Bind the current thread (or create one) to a sub-agent/session target |
| `/unfocus` | Remove the binding for the current bound thread |
| `/agents` | List active runs and binding state (`thread:<id>` or `unbound`) |
| `/session idle` | Inspect/update idle auto-unfocus (focused bound threads only) |
| `/session max-age` | Inspect/update hard cap (focused bound threads only) |

**Config switches.** The global default keys are `session.threadBindings.enabled`, `session.threadBindings.idleHours`, and `session.threadBindings.maxAgeHours`; channel overrides and spawn auto-bind keys are adapter-specific (see Thread supporting channels and the Configuration reference / Slash commands docs).

**Discovery.** Use `agents_list` to see which agent ids are currently allowed for `sessions_spawn`; the response includes each listed agent's effective model and embedded runtime metadata so callers can distinguish OpenClaw, Codex app-server, and other native runtimes. `allowAgents` entries must point at configured ids in `agents.list[]` (`["*"]` = any configured target plus the requester). If an agent config is deleted but its id remains in `allowAgents`, `sessions_spawn` rejects that id and `agents_list` omits it; run `openclaw doctor --fix` to clean stale entries, or add a minimal `agents.list[]` entry to keep the target spawnable.

**Allowlist fields.** `agents.list[].subagents.allowAgents` (`string[]`) lists agent ids targetable via explicit `agentId` (default: only the requester; include the requester id if you set a list but still want self-spawn), with `agents.defaults.subagents.allowAgents` as the default when the requester sets none. `agents.defaults.subagents.requireAgentId` (boolean, default `false`) blocks `sessions_spawn` calls that omit `agentId`, forcing explicit profile selection (per-agent override `agents.list[].subagents.requireAgentId`). `agents.defaults.subagents.announceTimeoutMs` (number, default `120000`) is the per-call timeout for gateway `agent` announce delivery — positive integer ms, clamped to the platform-safe timer maximum, with transient retries possibly extending the total wait beyond one timeout. If the requester session is sandboxed, `sessions_spawn` rejects targets that would run unsandboxed.

**Auto-archive.** Sub-agent sessions are automatically archived after `agents.defaults.subagents.archiveAfterMinutes` (default `60`); archive uses `sessions.delete` and renames the transcript to `*.deleted.<timestamp>` (same folder), and `cleanup: "delete"` archives immediately after announce (still keeping the transcript via rename). Auto-archive is best-effort (pending timers are lost on gateway restart) and applies equally to depth-1 and depth-2 sessions. Configured run timeouts do **not** auto-archive; they only stop the run, leaving the session until auto-archive. Browser cleanup is separate: tracked browser tabs/processes are best-effort closed when the run finishes, even if the transcript/session record is kept.

## Nested Sub-agents

By default sub-agents cannot spawn their own sub-agents (`maxSpawnDepth: 1`). Setting `maxSpawnDepth: 2` enables one level of nesting — the **orchestrator pattern** (main → orchestrator → worker sub-sub-agents).

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 2, // allow sub-agents to spawn children (default: 1)
        maxChildrenPerAgent: 5, // max active children per agent session (default: 5)
        maxConcurrent: 8, // global concurrency lane cap (default: 8)
        runTimeoutSeconds: 900, // default timeout for sessions_spawn (0 = no timeout)
        announceTimeoutMs: 120000, // per-call gateway announce timeout
      },
    },
  },
}
```

**Depth levels.** Each depth has a distinct session-key shape, role, and spawn capability:

| Depth | Session key shape | Role | Can spawn? |
| --- | --- | --- | --- |
| 0 | `agent:<id>:main` | Main agent | Always |
| 1 | `agent:<id>:subagent:<uuid>` | Sub-agent (orchestrator when depth 2 allowed) | Only if `maxSpawnDepth >= 2` |
| 2 | `agent:<id>:subagent:<uuid>:subagent:<uuid>` | Sub-sub-agent (leaf worker) | Never |

**Announce chain.** Results flow back up the chain: (1) a depth-2 worker finishes and announces to its depth-1 orchestrator parent; (2) the orchestrator synthesizes results, finishes, and announces to main; (3) main delivers to the user. Each level only sees announces from its direct children.

Operational guidance: start child work once and wait for completion events rather than poll-looping. `sessions_list` and `/subagents list` keep child-session relationships focused on live work — live children stay attached, ended children stay visible for a short recent window, and stale store-only links are ignored after their freshness window — preventing old `spawnedBy` / `parentSessionKey` metadata from resurrecting ghost children after restart. If a child completion event arrives after the final answer was sent, the correct follow-up is the silent token `NO_REPLY` / `no_reply`.

**Tool policy by depth.** Role and control scope are written into session metadata at spawn time, keeping flat or restored session keys from regaining orchestrator privileges. A **depth-1 orchestrator** (when `maxSpawnDepth >= 2`) gets `sessions_spawn`, `subagents`, `sessions_list`, and `sessions_history` to spawn children and inspect status, while other session/system tools stay denied. A **depth-1 leaf** (when `maxSpawnDepth == 1`) gets no session tools (the current default). A **depth-2 leaf worker** gets no session tools, `sessions_spawn` is always denied, and it cannot spawn further children.

**Per-agent spawn limit.** Each agent session (any depth) can have at most `maxChildrenPerAgent` (default `5`) active children, preventing runaway fan-out.

**Cascade stop.** Stopping a depth-1 orchestrator automatically stops its depth-2 children: `/stop` in the main chat stops all depth-1 agents and cascades to their children.

## Authentication

Sub-agent auth is resolved by **agent id**, not by session type. The session key is `agent:<agentId>:subagent:<uuid>`, the auth store loads from that agent's `agentDir`, and the main agent's auth profiles are merged in as an additive **fallback** (agent profiles override main profiles on conflicts, main profiles always remain available). Fully isolated auth per agent is not supported yet.

## Announce

Sub-agents report back via an **announce step** that runs inside the sub-agent session (not the requester session). If the sub-agent replies exactly `ANNOUNCE_SKIP`, nothing is posted; if the latest assistant text is the silent token `NO_REPLY` / `no_reply`, announce output is suppressed even if earlier progress was visible.

Delivery depends on requester depth: top-level requester sessions use a follow-up `agent` call with external delivery (`deliver=true`); nested requester subagent sessions receive an internal follow-up injection (`deliver=false`) so the orchestrator synthesizes child results in-session (falling back to that session's requester if the nested session is gone). For top-level sessions, completion-mode direct delivery resolves any bound conversation/thread route and hook override, then fills missing channel-target fields from the requester's stored route — keeping completions on the right chat/topic (and preserving thread/topic routing where adapters allow) even when the origin only identifies the channel. Child completion aggregation is scoped to the current requester run, preventing stale prior-run outputs from leaking in.

### Announce Context

Announce context is normalized to a stable internal event block:

| Field | Source |
| --- | --- |
| Source | `subagent` or `cron` |
| Session ids | Child session key/id |
| Type | Announce type + task label |
| Status | Derived from runtime outcome (`success`, `error`, `timeout`, or `unknown`) — **not** inferred from model text |
| Result content | Latest visible assistant text from the child |
| Follow-up | Instruction describing when to reply vs stay silent |

Terminal failed runs report failure status without replaying captured reply text; tool/toolResult output is not promoted into child result text.

### Stats Line

Announce payloads include a **stats line** at the end (even when wrapped): runtime (e.g. `runtime 5m12s`); token usage (input/output/total); estimated cost when model pricing is configured (`models.providers.*.models[].cost`); and `sessionKey`, `sessionId`, and the transcript path so the main agent can fetch history via `sessions_history` or inspect the file. This internal metadata is for orchestration only — user-facing replies should be in normal assistant voice.

### Why prefer `sessions_history`

`sessions_history` is the safer recall path because assistant recall is normalized first — stripping thinking tags; `<relevant-memories>` / `<relevant_memories>` scaffolding; plain-text tool-call XML payload blocks (`<tool_call>`, `<function_call>`, `<tool_calls>`, `<function_calls>`, including truncated payloads that never close cleanly); downgraded tool-call/result scaffolding and historical-context markers; leaked model control tokens (`<|assistant|>`, other ASCII `<|...|>`, full-width `<｜...｜>`); and malformed MiniMax tool-call XML. Credential/token-like text is redacted, long blocks can be truncated, and very large histories can drop older rows or replace an oversized row with `[sessions_history omitted: message too large]`. Raw on-disk transcript inspection is the fallback for the full byte-for-byte transcript.

## Liveness and Recovery

OpenClaw does not treat `endedAt` absence as proof that a sub-agent is still alive; unended runs older than the stale-run window stop counting as active/pending in `/subagents list`, status summaries, descendant completion gating, and per-session concurrency checks.

After a gateway restart, stale unended restored runs are pruned unless their child session is marked `abortedLastRun: true`. Those restart-aborted sessions remain recoverable through the sub-agent **orphan recovery flow**, which sends a synthetic resume message before clearing the aborted marker. Recovery is bounded per child session: if the same child is accepted for orphan recovery repeatedly inside the rapid re-wedge window, OpenClaw persists a **recovery tombstone** and stops auto-resuming it on later restarts. Run `openclaw tasks maintenance --apply` to reconcile the task record, or `openclaw doctor --fix` to clear stale aborted flags.

A failed spawn returning Gateway `PAIRING_REQUIRED` / `scope-upgrade` is a caller-context concern, not always a pairing-state bug: internal `sessions_spawn` coordination dispatches in process when the caller is already inside the gateway request context, so it does not open a loopback WebSocket or depend on the CLI's paired-device scope baseline. Callers outside the gateway process use the WebSocket fallback as `client.id: "gateway-client"` / `client.mode: "backend"` over direct loopback shared-token/password auth; remote callers, explicit `deviceIdentity` or device-token paths, and browser/node clients still need normal device approval for scope upgrades.

## Stopping

Sending `/stop` in the requester chat aborts the requester session and stops any active sub-agent runs spawned from it, cascading to nested children.

## Limitations

- Sub-agent announce is **best-effort**: a gateway restart loses pending "announce back" work.
- Sub-agents share the same gateway process resources; treat `maxConcurrent` as a safety valve.
- `sessions_spawn` is always non-blocking: it returns `{ status: "accepted", runId, childSessionKey }` immediately.
- Sub-agent context only injects `AGENTS.md` and `TOOLS.md` (no `SOUL.md`, `IDENTITY.md`, `USER.md`, `MEMORY.md`, `HEARTBEAT.md`, or `BOOTSTRAP.md`). Codex-native subagents follow the same boundary — `TOOLS.md` stays in inherited Codex thread instructions, while parent-only persona, identity, and user files are injected as turn-scoped collaboration instructions so children do not clone them.
- Maximum nesting depth is 5 (`maxSpawnDepth` range 1–5); depth 2 is recommended for most cases.
- `maxChildrenPerAgent` caps active children per session (default `5`, range `1–20`).

**Source**: OpenClaw documentation — `tools/subagents` (mirror `inbox/openclaw_docs/tools/subagents.md`)
**Last Updated**: 2026-06-22
**Status**: Active
