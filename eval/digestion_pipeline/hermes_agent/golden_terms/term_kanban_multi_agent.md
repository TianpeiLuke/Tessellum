---
tags:
  - resource
  - terminology
  - agent_systems
  - multi_agent
keywords:
  - Kanban Multi-Agent
  - Hermes Kanban
  - multi-agent board
  - durable task board
  - kanban.db
  - multi-agent profile collaboration
  - dispatcher
  - task runs
topics:
  - agentic AI
  - multi-agent coordination
  - work queue
  - agent orchestration
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban/
---

# Kanban Multi-Agent — Durable Multi-Profile Agent Task Board

## Definition

**Kanban Multi-Agent** (Hermes Kanban) is a durable, SQLite-backed task board that lets multiple named agent profiles collaborate on work as independent OS processes, without the fragility of in-process subagent swarms. Introduced by the Hermes agent (Nous Research), it stores every task as a row in a shared database (`~/.hermes/kanban.db`), every handoff as a row any profile or human can read and write, and runs each worker as a full process with its own identity and persistent memory. It is the coordination primitive for workloads a single fork-join delegation call cannot cover: research triage with a human in the loop, scheduled recurring operations, persistent "digital twin" assistants, engineering pipelines (decompose → implement → review → iterate), and fleet work (one specialist serving N subjects).

Unlike the generic Agile Kanban methodology (visualizing human work and limiting work-in-progress), this is a *multi-agent execution substrate*: a durable work queue plus a state machine where a long-lived **dispatcher** promotes ready tasks, atomically claims them, and spawns the assigned profile as a worker. It solves the problem that anonymous in-context subagents lose their audit trail on context compression, cannot survive restarts, and cannot accept mid-flight human input.

## Context

The term originates in the **Hermes agent** framework by **Nous Research**, where the board has two front doors over the same `kanban_db` layer: agents drive it through a dedicated `kanban_*` toolset (`kanban_show`, `kanban_complete`, `kanban_block`, `kanban_heartbeat`, `kanban_create`, `kanban_link`, ...), while humans, scripts, and cron drive it through the `hermes kanban …` CLI, the `/kanban` gateway slash command, or a bundled dashboard plugin. The **dispatcher** runs inside the Hermes gateway process by default and sweeps all boards on a fixed tick (60 s default).

In the broader knowledge-graph context, Kanban Multi-Agent is the agent-systems specialization of three foundational ideas: the generic [Kanban](term_kanban.md) board metaphor (status columns: `triage → todo → ready → running → blocked → done → archived`), the durable [message queue](term_message_queue.md) (durable rows, competing-consumers claim), and the blackboard-style [multi-agent systems](term_multi_agent_systems.md) coordination pattern where heterogeneous workers communicate indirectly through shared state rather than direct messaging. It contrasts with synchronous fork-join delegation (a function call that blocks until a child returns).

## Key Characteristics

- **Durable shared state.** The board is a SQLite DB (`kanban.db`, WAL mode) holding `tasks`, `task_links`, comments, `task_runs`, and an append-only `task_events` log. State survives process restarts and is queryable forever — no audit trail lost to context compression.
- **Task vs. run separation.** A *task* is a logical unit of work; a *run* is one attempt. Each claim opens a `task_runs` row pointed to by `tasks.current_run_id`; a task attempted three times has three run rows, giving full attempt history for postmortems and per-attempt metadata.
- **Dispatcher with competing-consumers claim.** Every tick the dispatcher reclaims stale/crashed workers, promotes `todo → ready` when all parent links are `done`, atomically claims a `ready` task (`BEGIN IMMEDIATE`), and spawns the assigned profile with `HERMES_KANBAN_TASK` set — which flips on the `kanban_*` toolset in that worker's schema.
- **Structured handoff.** A worker closes a run with `kanban_complete(summary=..., metadata={...})`; downstream children read the most-recent completed run's `summary` + `metadata` of each parent, and a retrying worker reads its own prior attempts so it does not repeat a failed path.
- **Resilience built in.** A *circuit breaker* auto-blocks a task after `kanban.failure_limit` (default 2) consecutive spawn/run failures with `gave_up`; *crash detection* (`kill(pid, 0)`) reclaims a worker whose PID died before TTL; a *respawn guard* refuses to re-spawn on `blocker_auth` / `recent_success` / `active_pr`.
- **Multi-board + multi-tenant isolation.** Boards are the hard isolation boundary (separate DB per slug; workers see only their board via `HERMES_KANBAN_BOARD`); tenants are a soft namespace filter within a board.
- **Human-in-the-loop at any point.** Comments are the durable inter-agent protocol; a worker can `kanban_block(reason=...)` to escalate, and a human `/kanban unblock` (even mid-turn — `/kanban` bypasses the running-agent guard) re-queues it.
- **Single-host by design.** `kanban.db` is local; crash detection assumes host-local PIDs. Cross-host fan-out is out of scope — run an independent board per host.
- **Eight-plus collaboration patterns** emerge with no new primitives: fan-out, pipeline, voting/quorum, long-running journal, human-in-the-loop, `@mention` routing, thread-scoped workspace, fleet farming, and triage specifier.

## Related Terms


## References

- [Hermes Kanban (Multi-Agent Board) — feature docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban/)
- [Hermes Kanban tutorial — four user stories](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial/)
- [Blackboard system (Wikipedia)](https://en.wikipedia.org/wiki/Blackboard_system)
- [Message queue (Wikipedia)](https://en.wikipedia.org/wiki/Message_queue)
- [Competing Consumers pattern (Microsoft Azure Architecture Center)](https://learn.microsoft.com/en-us/azure/architecture/patterns/competing-consumers)

---

**Last Updated**: 2026-06-19
**Status**: Active
