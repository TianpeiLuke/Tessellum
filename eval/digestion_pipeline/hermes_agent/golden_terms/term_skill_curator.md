---
tags:
  - resource
  - terminology
  - agentic_ai
  - self_improvement
  - skills
  - llm
keywords:
  - skill curator
  - curator
  - agent-created skills
  - skill lifecycle
  - skill staleness
  - skill consolidation
  - usage telemetry
topics:
  - agentic AI
  - agent skills
  - self-evolving agents
  - background maintenance
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://hermes-agent.nousresearch.com/docs/user-guide/features/curator
---

# Skill Curator

## Definition

The **skill curator** is a background maintenance loop that keeps an agent's library of **agent-created skills** healthy over time. It tracks how often each skill is viewed, used, and patched; moves long-unused skills through an `active → stale → archived` lifecycle; and periodically spawns a short auxiliary-model review that can consolidate overlapping skills or patch accumulated drift. It exists to solve the *forgetting / retirement* gap in a self-improving skill system: the [self-evolving agent](term_self_evolving_agent.md) loop creates new skills monotonically, so without a counterbalancing maintenance pass the catalog fills with narrow near-duplicates that pollute the prompt path and waste context-window tokens.

In the Hermes Agent (Nous Research) implementation that coined the term, the curator is the canonical example: each new umbrella skill the background self-improvement review writes lands in `~/.hermes/skills/`, and the curator periodically prunes and consolidates that growing library. The curator **never auto-deletes** — the worst outcome is archival into a recoverable `.archive/` directory, with a tar.gz snapshot taken before every mutating pass so an entire run can be rolled back. It is the skill-side analogue of the parallel background review that maintains an agent's long-term [memory](term_agentic_memory.md).

## Context

The curator is a feature of agent harnesses that support **agent-managed skills** — on-demand knowledge documents in the open [Agent Skills](https://agentskills.io) format (a `SKILL.md` file plus optional bundled resources, loaded via [progressive disclosure](term_skills.md)). It only governs skills explicitly marked **agent-created** (written by a background self-improvement fork), leaving hand-authored, user-directed, bundled, and hub-installed skills alone by default. It sits alongside other [agent harness](term_agentic_ai.md) subsystems — the skill system, the skills registry/hub, persistent memory, and the auxiliary-model task router — and shares plumbing with them (the same fork pattern as the memory self-improvement nudge; the same aux-model slot machinery as Vision/Compression/Session-Search).

Operationally the curator is triggered by an **inactivity check**, not a cron daemon: on session start and on a recurring tick inside the gateway's [cron](term_cron.md)-ticker thread, the harness checks whether enough wall-clock time has elapsed since the last run *and* whether the agent has been idle long enough, so on an active machine it naturally runs only during quiet stretches.

## Key Characteristics

- **Two-phase run.** Phase 1 is a deterministic **auto-transition** pass (no LLM): skills unused past a staleness threshold become `stale`, and skills unused past a longer threshold are archived. Phase 2 is an **opt-in LLM consolidation** pass: a forked agent surveys agent-created skills, reads any of them, and decides per-skill to keep, patch, consolidate overlapping skills into class-level umbrellas, or archive. Consolidation is off by default because it costs aux-model tokens and makes broad structural changes.
- **Usage telemetry sidecar.** A `.usage.json` file records per-skill counters — `view_count` (incremented on a skill-view tool call), `use_count` (incremented when the skill is loaded into a prompt), and `patch_count` (incremented on edits) — plus `last_used_at`, `state`, `pinned`, and `archived_at`. Using a sidecar rather than rewriting each skill's frontmatter avoids edit noise and merge conflicts.
- **Lifecycle state machine.** Each agent-created skill follows $\texttt{active} \rightarrow \texttt{stale} \rightarrow \texttt{archived}$, gated by least-recently-used recency thresholds. Archived skills are recoverable via an explicit restore command; the transition can also reverse on successful reuse.
- **Background fork execution.** When both inactivity gates pass, the curator spawns a background fork of the agent — a short-lived [subagent](term_subagent.md) running in its own prompt cache that never touches the active conversation. The review pass runs on a configurable auxiliary model so it can be routed to a cheaper LLM than the main chat model.
- **Safety: no deletion, full rollback.** Before every real pass the harness takes a tar.gz snapshot; a bad run is undone with a single rollback command, and the rollback itself snapshots first so it is reversible. Snapshots are pruned to a bounded keep-count.
- **Pinning + protected built-ins.** Pinning a skill exempts it from both auto-transitions and the agent's own delete tool. A small hardcoded set of *protected built-ins* (skills that back load-bearing slash-command UX) is filtered out of the candidate list entirely and is never archivable or consolidatable.
- **Per-run audit reports.** Every run writes a timestamped directory containing a machine-readable JSON log and a human-readable `REPORT.md` summarizing which skills transitioned, what the reviewer said, and any rename map produced by a consolidation wave.
- **Negative-claim revalidation (design intent).** The originating design (Hermes issue #7816) also targets environment-dependent *negative* claims a skill may have learned ("this tool does not work") with a TTL/revalidation mechanism, to avoid baking transient "learned helplessness" into permanent guidance.

## Related Terms


## References

- [Hermes Agent — Curator](https://hermes-agent.nousresearch.com/docs/user-guide/features/curator) — background maintenance for agent-created skills: usage tracking, staleness, archival, LLM-driven review, backups/rollback, pinning, telemetry, per-run reports
- [Hermes Agent — Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) — the self-improvement loop and `skill_manage` tool that create the agent-created skills the curator maintains
- [NousResearch/hermes-agent issue #7816 — Skill lifecycle management](https://github.com/NousResearch/hermes-agent/issues/7816) — original proposal and design discussion: sidecar telemetry, `active/stale/archived` states, no-auto-delete principle, negative-claim TTL revalidation
- [Agent Skills — Overview (agentskills.io)](https://agentskills.io) — the open `SKILL.md` skill format and progressive-disclosure loading model the curated skills conform to
- [Agent Skills — Specification (agentskills.io)](https://agentskills.io/specification) — formal skill-package layout (SKILL.md + scripts/references/assets) that consolidation must keep intact

---

**Last Updated**: June 19, 2026
**Status**: Active
**Domain**: Agentic AI, Agent Skills, Self-Improvement
