---
title: Sub-Plan co02 — OpenClaw Docs: Concepts (commitments, compaction, context, context-engine, delegate, dreaming, experimental)
date: 2026-06-20
status: completed
source_url: https://docs.openclaw.ai/
master_plan: plan_digest_openclaw_docs_master.md
pages: ["concepts/commitments", "concepts/compaction", "concepts/context", "concepts/context-engine", "concepts/delegate-architecture", "concepts/dreaming", "concepts/experimental-features"]
---

# Sub-Plan co02: Concepts

> Self-contained sub-plan of [`plan_digest_openclaw_docs_master.md`](plan_digest_openclaw_docs_master.md). Shared
> routing (`resources/documentation/openclaw/`, `oc_*`), format (YAML field order, `## Overview` → body → `## Related Notes` → `## References`), dedup (3-way vs term_dictionary / documentation / repo_openclaw*), 9-GATE validation, cross-refs, and entry-point wiring (`entry_openclaw_docs.md`, W1) are ALL inherited from the master and not re-derived here.

## Scope

The 7 second-batch Concepts pages covering OpenClaw's **memory / context / runtime-behavior internals**:
inferred follow-up memory (commitments), conversation summarization (compaction), what the model sees and
how it is built (context), the pluggable context-assembly subsystem (context-engine), organizational
named-agent deployment (delegate-architecture), background memory consolidation (dreaming), and the opt-in
preview-flag policy (experimental-features). **Priority P1 (Phase A)** — these define the
context/compaction/memory/runtime vocabulary that the CLI, gateway, tools, and plugins sub-plans reference.
The code-side counterparts (`repo_openclaw_memory`, `repo_openclaw_agents`, `repo_openclaw_sessions`) and the
`snippet_openclaw_context_engine_*` / `snippet_openclaw_memory_*` / `snippet_openclaw_agents_compaction_*`
snippets are LINKED, not recreated.

**Source**: OpenClaw docs, 7 pages, **9,417 measured words**. **Planned: 7 notes** (1 per page; no splits).

## Source Pages (Measured 2026-06-20, mirror `inbox/openclaw_docs/`)

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| commitments | concepts/commitments | 767 | 4 | 8 | 0 | procedure |
| compaction | concepts/compaction | 1,164 | 6 | 8 | 6 | procedure |
| context | concepts/context | 1,295 | 2 | 11 | 3 | concept |
| context-engine | concepts/context-engine | 2,146 | 8 | 8 | 8 | model (concept) |
| delegate-architecture | concepts/delegate-architecture | 1,692 | 9 | 8 | 12 | procedure |
| dreaming | concepts/dreaming | 1,505 | 6 | 13 | 0 | procedure |
| experimental-features | concepts/experimental-features | 848 | 3 | 4 | 5 | concept |

Totals: **9,417 words · 38 code fences · 60 H2 · 34 H3**. No page exceeds the 2,500-word split threshold
(largest = context-engine at 2,146w); no page mixes building blocks badly enough to force a split (see Split
Decisions). One source page → one note.

## Content Strategy

- **Prioritize**: the context/compaction pair (`context` = concept of what the model sees; `compaction` =
  procedure to keep it inside the window) and `context-engine` (the pluggable assembly/compaction interface
  the rest of the runtime extends) — these are the highest-reuse architecture concepts and are referenced by
  CLI (`/context`, `/compact`), gateway (config), and plugins (engine slot) sub-plans.
- **Split**: none. Each page is a single coherent building block under the 2,500-word cap (see Split
  Decisions for the per-page rationale, including why the 2,146-word context-engine page stays one note).
- **Link-out (do not duplicate)**: memory mechanics → `concepts/memory*` (co03/co04, planned); session
  lifecycle / pruning → `concepts/session`, `concepts/session-pruning` (co06, planned); heartbeat delivery →
  `gateway/heartbeat` (gw03, planned); scheduled tasks/cron → `automation/cron-jobs` (au01, planned); system
  prompt → `concepts/system-prompt` (co07, planned); multi-agent routing → `concepts/multi-agent` (co05,
  planned); sandboxing → `gateway/sandboxing` (gw05, planned); session-management deep dive →
  `reference/session-management-compaction` (rf03, planned). These targets are referenced as prose pointers
  and as sibling-`oc_*` "(planned)" Related-Notes candidates, never re-explained inline.
- **Existing terms LINKED, never redefined**: `term_compaction`, `term_context_window`, `term_context_engine`,
  `term_context_engineering`, `term_memory_dreaming`, `term_agentic_memory`, `term_episodic_memory`,
  `term_progressive_summarization`, `term_subagent`, `term_heartbeat`, `term_delegated_identity`,
  `term_delegate_task`, `term_prompt_injection`, `term_sandbox`, `term_feature_flags`, `term_cron`,

## Planned Notes

| # | Filename (`resources/documentation/openclaw/`) | BB | Source page/section | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `oc_concepts_commitments.md` | procedure | commitments.md: all H2 (Enable, How it works, Scope, Commitments vs reminders, Manage, Privacy and cost, Troubleshooting) | 600 | Enabling and managing OpenClaw inferred-commitment follow-ups: the hidden background extraction pass, heartbeat-clamped delivery, agent/channel scope, `commitments.maxPerDay`, the `openclaw commitments` CLI, and how commitments differ from exact reminders/scheduled tasks. |
| 2 | `oc_concepts_compaction.md` | procedure | compaction.md: all H2/H3 (How it works, Auto-compaction, Manual compaction, Configuration + 6 H3, Pluggable providers, Compaction vs pruning, Troubleshooting) | 700 | How OpenClaw compacts older conversation turns into a summary to stay inside the context window: auto-compaction + overflow signatures, `/compact`, the `agents.defaults.compaction.*` knobs (separate model, identifier preservation, byte guard, successor transcripts, memory flush), pluggable compaction providers, and compaction-vs-pruning. |
| 3 | `oc_concepts_context.md` | concept | context.md: all H2/H3 (Quick start + `/context list`/`detail`/`map`, What counts, system-prompt build, Project Context injection, Skills/Tools costs, directives, persistence, what `/context` reports) | 700 | What "context" is in OpenClaw — everything sent to the model for a run, bounded by the context window — and how to inspect it: the `/context list`/`detail`/`map` views, what counts toward the window, how the system prompt and injected workspace (Project Context) files are built, tool-schema vs tool-list cost, and what persists across messages. |
| 4 | `oc_concepts_context_engine.md` | model | context-engine.md: all H2/H3 (Quick start, How it works 4 lifecycle points, Subagent lifecycle, system-prompt addition, legacy engine, Plugin engines, ContextEngine interface, runtime settings, host requirements, failure isolation, ownsCompaction, config reference, relationship to compaction/memory, Tips) | 750 | The pluggable context-engine subsystem: the four-point lifecycle (ingest / assemble / compact / after-turn), the `ContextEngine` interface (required + optional members, `AssembleResult`, `promptAuthority`), the built-in `legacy` engine, the `plugins.slots.contextEngine` selection slot, `ownsCompaction` semantics, runtime settings, host requirements, and failure isolation/quarantine. |
| 5 | `oc_concepts_delegate_architecture.md` | procedure | delegate-architecture.md: all H2/H3 (What is a delegate, Why, Capability tiers 1-3, Prerequisites: hard blocks/tool restrictions/sandbox/audit, Setting up 4 steps with M365 + Google Workspace, Example org assistant, Scaling pattern) | 750 | Running OpenClaw as a named organizational delegate that acts "on behalf of" people under its own identity: the three capability tiers, hardening prerequisites (hard blocks, per-agent tool policy, sandbox isolation, audit trail), identity-provider delegation setup for Microsoft 365 and Google Workspace, channel bindings, and the least-privilege scaling pattern. |
| 6 | `oc_concepts_dreaming.md` | procedure | dreaming.md: all H2 (What dreaming writes, Phase model light/deep/REM, transcript ingestion, Dream Diary + backfill, Deep ranking signals, QA shadow trial, Scheduling, Quick start, Slash command, CLI workflow, Key defaults, Dreams UI, blocked troubleshooting) | 700 | OpenClaw's opt-in background memory-consolidation system in `memory-core`: the light/deep/REM phase model, what each phase writes (`DREAMS.md` diary vs `MEMORY.md` promotion), the six weighted deep-ranking signals, the report-only QA shadow trial, scheduling/cadence, enabling via config + `/dreaming` slash command + `openclaw memory promote` CLI, and the "blocked" heartbeat troubleshooting path. |
| 7 | `oc_concepts_experimental_features.md` | concept | experimental-features.md: all H2/H3 (treat-differently rules, Currently documented flags table, Local model lean mode + Why/When-on/When-off/Enable, Experimental does not mean hidden) | 550 | What experimental flags mean in OpenClaw — opt-in preview surfaces behind explicit `.experimental` keys whose shape may change — the currently documented flags table (localModelLean, sessionMemory, sandboxExecServer, planTool), the local-model lean-mode workaround in depth (which three tools it drops and why, when to use it), and the "experimental is documented, not hidden" config-hygiene principle. |

Filename rule applied (master Step 3.6): `oc_` + full slug with `/` and `-` → `_`
(`concepts/commitments` → `oc_concepts_commitments.md`; `concepts/context-engine` →
`oc_concepts_context_engine.md`; `concepts/delegate-architecture` →
`oc_concepts_delegate_architecture.md`; `concepts/experimental-features` →
`oc_concepts_experimental_features.md`). No aspect suffixes — no page split.

## Section Coverage Map

```
commitments.md (767w)
├── Enable commitments ─────────────────────────── → note 1 (oc_concepts_commitments)
├── How it works (hidden extraction, heartbeat) ── → note 1
├── Scope (agent/channel) ──────────────────────── → note 1
├── Commitments vs reminders (table) ───────────── → note 1
├── Manage commitments (CLI) ───────────────────── → note 1
├── Privacy and cost ───────────────────────────── → note 1
└── Troubleshooting ────────────────────────────── → note 1
compaction.md (1,164w)
├── How it works (chunk/tool-pair safety) ──────── → note 2 (oc_concepts_compaction)
├── Auto-compaction (+ overflow signatures) ────── → note 2
├── Manual compaction (/compact) ───────────────── → note 2
├── Configuration ──────────────────────────────── → note 2
│   ├── Using a different model ─────────────────── → note 2
│   ├── Identifier preservation ─────────────────── → note 2
│   ├── Active transcript byte guard ────────────── → note 2
│   ├── Successor transcripts ───────────────────── → note 2
│   ├── Compaction notices ──────────────────────── → note 2
│   └── Memory flush ────────────────────────────── → note 2
├── Pluggable compaction providers ─────────────── → note 2
├── Compaction vs pruning (table) ──────────────── → note 2
└── Troubleshooting ────────────────────────────── → note 2
context.md (1,295w)
├── Quick start (inspect context) ──────────────── → note 3 (oc_concepts_context)
├── Example output (list / detail / map H3) ────── → note 3
├── What counts toward the context window ───────── → note 3
├── How OpenClaw builds the system prompt ───────── → note 3
├── Injected workspace files (Project Context) ─── → note 3
├── Skills: injected vs loaded on-demand ────────── → note 3
├── Tools: there are two costs ─────────────────── → note 3
├── Commands, directives, inline shortcuts ─────── → note 3
├── Sessions, compaction, and pruning ──────────── → note 3
└── What /context actually reports ─────────────── → note 3
context-engine.md (2,146w)
├── Quick start (Steps) ────────────────────────── → note 4 (oc_concepts_context_engine)
├── How it works (4 lifecycle points) ──────────── → note 4
│   ├── Subagent lifecycle ──────────────────────── → note 4
│   └── System prompt addition ──────────────────── → note 4
├── The legacy engine ──────────────────────────── → note 4
├── Plugin engines (registerContextEngine) ─────── → note 4
│   ├── The ContextEngine interface ─────────────── → note 4
│   ├── Runtime settings ────────────────────────── → note 4
│   ├── Host requirements ───────────────────────── → note 4
│   ├── Failure isolation ───────────────────────── → note 4
│   └── ownsCompaction ──────────────────────────── → note 4
├── Configuration reference ────────────────────── → note 4
├── Relationship to compaction and memory ──────── → note 4
└── Tips ───────────────────────────────────────── → note 4
delegate-architecture.md (1,692w)
├── What is a delegate? ────────────────────────── → note 5 (oc_concepts_delegate_architecture)
├── Why delegates? (table) ─────────────────────── → note 5
├── Capability tiers (Tier 1/2/3 H3) ───────────── → note 5
├── Prerequisites: isolation and hardening ─────── → note 5
│   ├── Hard blocks / Tool restrictions ─────────── → note 5
│   ├── Sandbox isolation / Audit trail ─────────── → note 5
├── Setting up a delegate (steps 1-4: M365, GWS) ─ → note 5
├── Example: organizational assistant ──────────── → note 5
└── Scaling pattern ────────────────────────────── → note 5
dreaming.md (1,505w)
├── What dreaming writes ───────────────────────── → note 6 (oc_concepts_dreaming)
├── Phase model (light/deep/REM table) ─────────── → note 6
├── Session transcript ingestion ───────────────── → note 6
├── Dream Diary (+ backfill commands) ──────────── → note 6
├── Deep ranking signals (6-signal table) ──────── → note 6
├── QA shadow trial report coverage ────────────── → note 6
├── Scheduling / Quick start / Slash command ───── → note 6
├── CLI workflow / Key defaults / Dreams UI ────── → note 6
└── Dreaming never runs: status shows blocked ──── → note 6
experimental-features.md (848w)
├── (intro: treat-differently rules) ───────────── → note 7 (oc_concepts_experimental_features)
├── Currently documented flags (table) ─────────── → note 7
├── Local model lean mode ──────────────────────── → note 7
│   ├── Why these three tools / When on / off ───── → note 7
│   └── Enable ──────────────────────────────────── → note 7
└── Experimental does not mean hidden ──────────── → note 7
```
No orphaned sections — every H2/H3 maps to a note. Link-out targets (memory, session, heartbeat, cron,
system-prompt, multi-agent, sandboxing, session-management-compaction) are referenced, not duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| (none) | — | All 7 pages are single-BB and under the 2,500-word cap. The largest, `context-engine.md` (2,146w / 8 code), is a single cohesive plugin-interface model (one lifecycle + one interface contract) — splitting would fragment the ingest→assemble→compact→after-turn story and the required/optional interface tables; kept as one ≤6-code-block note by reproducing only the 2 most load-bearing snippets (the `registerContextEngine` factory + the config slot) and prose-summarizing the rest. `delegate-architecture.md` (1,692w / 9 code) mixes a concept (capability tiers) with a setup procedure, but the setup is the dominant BB and the tiers are its motivating frame — kept as one procedure note (select ≤6 of the 9 fences: tool policy, sandbox, M365 send-on-behalf, GWS scopes, bindings, example). |

## Summary Statistics & Building Block Distribution

- Source pages: **7** (9,417 measured words, 38 code fences). New `oc_` notes: **7**. New `term_dictionary`
  notes: **0** (see Undigested Terms Plan).
- BB distribution: **procedure ×4** (commitments, compaction, delegate-architecture, dreaming) · **concept ×2**
  (context, experimental-features) · **model ×1** (context-engine — the pluggable interface contract).
- Est. digest words ~**4,750** (avg ~680/note); all ≤750w, well under the 2,500-word cap. Each note keeps
  ≤6 code blocks by selecting the most load-bearing config/snippet examples verbatim and prose-summarizing
  the remainder (context-engine 8→6, delegate 9→6).
- Cross-refs (LOCKED at xref-augment 2026-06-21, raised floors): each note lists **≥8 relevancy-selected
  `repo_openclaw*` + sibling `oc_*` (planned, this series). See `## Per-Note Related Notes Mapping (LOCKED …)`.
  counts: commitments 10t·11s·10d · compaction 10t·12s·11d · context 10t·11s·11d · context_engine 10t·11s·11d
  · delegate_architecture 10t·11s·11d · dreaming 10t·11s·10d · experimental_features 10t·11s·10d.

## Per-Note Related Notes Mapping (LOCKED — xref-augment 2026-06-21)

> **Standard:** ≥8 terms · ≥10 snippets · ≥10 docs per note, relevance-selected (re-read each source page),
> on 2026-06-21 (all returned 1). Sibling `oc_*` docs in this series do not exist yet → cited "(planned, this
> `cc_*`, pi `pi_*`, hermes_agent `hermes_*`, band `band_*` coding-agent corpora). ALL snippets are existing
> `../../term_dictionary/`, sibling oc_ → `oc_Y.md`, other doc → `../<folder>/`, repo →
> `../../../areas/code_repos/`, snippet → `../../code_snippets/`, analysis → `../../analysis_thoughts/`,
> entry → `../../../0_entry_points/`. Render each link in the note's `## Related Notes` as
> `- [Name](relpath.md) — <what it is>; relevance: <why THIS note>`.

### oc_concepts_commitments (10t · 11s · 10d)

**Terms** (`../../term_dictionary/`)
- [term_heartbeat](../../term_dictionary/term_heartbeat.md) — periodic background agent turn; relevance: heartbeat is the sole delivery channel for due commitments and clamps the due window to ≥1 interval.
- [term_cron](../../term_dictionary/term_cron.md) — cron-expression scheduling; relevance: the "Commitments vs reminders" table routes exact `Remind me at 3PM` requests to scheduled tasks/cron, not commitments.
- [term_agentic_memory](../../term_dictionary/term_agentic_memory.md) — durable agent memory layer; relevance: commitments are operational memory distinct from durable `MEMORY.md` facts — this contrast is the whole framing.
- [term_episodic_memory](../../term_dictionary/term_episodic_memory.md) — conversation-bound event memory; relevance: a commitment is a conversation-scoped follow-up obligation, the canonical episodic-memory pattern.
- [term_workflow_memory](../../term_dictionary/term_workflow_memory.md) — open-loop task tracking; relevance: commitments track "open loops" the conversation created (interview follow-up, unanswered thread).
- [term_feature_flags](../../term_dictionary/term_feature_flags.md) — opt-in config toggles; relevance: `commitments.enabled`/`maxPerDay` are off-by-default opt-in flags.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: the hidden background extraction pass is an extra LLM call per eligible turn (the privacy/cost note).
- [term_session_data](../../term_dictionary/term_session_data.md) — per-session state; relevance: a commitment is stored with agent id + session key + channel target as local OpenClaw session state.
- [term_persistent_goal](../../term_dictionary/term_persistent_goal.md) — long-lived agent objective; relevance: an inferred commitment is a short-lived goal-to-revisit, the lightweight cousin of a persistent goal.
- [term_dm_policy](../../term_dictionary/term_dm_policy.md) — direct-message delivery policy; relevance: commitment delivery respects the agent/channel scope and the `target: "none"` no-external-send case.

**Docs**
- [cc_loop_scheduled_tasks](../claude_code/cc_loop_scheduled_tasks.md) — Claude Code scheduled/loop tasks; relevance: the exact-reminder counterpart that commitments deliberately do NOT cover.
- [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — scheduled-task execution semantics; relevance: clarifies the explicit-schedule path commitments contrast against.
- [hermes_cron_scheduling](../hermes_agent/hermes_cron_scheduling.md) — Hermes cron scheduling; relevance: analog scheduled-delivery surface for exact reminders.
- [hermes_guide_daily_briefing_bot](../hermes_agent/hermes_guide_daily_briefing_bot.md) — scheduled briefing pattern; relevance: shows the proactive scheduled-delivery use case adjacent to inferred check-ins.
- [cc_auto_memory](../claude_code/cc_auto_memory.md) — automatic memory capture; relevance: parallel "agent infers something worth remembering" background pass.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — Hermes durable memory; relevance: the durable-memory layer commitments are explicitly NOT (operational vs long-term).
- [oc_concepts_memory](oc_concepts_memory.md) — OpenClaw memory overview (planned, this series, co03); relevance: home doc for the durable-memory contrast referenced inline.
- [oc_gateway_heartbeat](oc_gateway_heartbeat.md) — heartbeat delivery (planned, this series, gw03); relevance: home doc for the heartbeat mechanism that delivers commitments.
- [oc_automation_cron_jobs](oc_automation_cron_jobs.md) — scheduled tasks (planned, this series, au01); relevance: home doc for the exact-reminder alternative.
- [oc_cli_commitments](oc_cli_commitments.md) — `openclaw commitments` CLI (planned, this series, cl02); relevance: command reference for inspecting/dismissing stored commitments.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — `memory-core` package; relevance: commitments are operational memory state managed alongside the memory layer.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the post-reply extraction pass and heartbeat-turn delivery live in the agent runtime.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — agent memory-search call; relevance: the recall surface adjacent to commitment storage.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory event records; relevance: the event/record shape commitments are persisted as.
- [snippet_openclaw_gateway_chat_heartbeat_buffered_delta](../../code_snippets/snippet_openclaw_gateway_chat_heartbeat_buffered_delta.md) — heartbeat delta buffering; relevance: heartbeat-turn plumbing that carries due commitments.
- [snippet_openclaw_gateway_server_cron_service_notifications](../../code_snippets/snippet_openclaw_gateway_server_cron_service_notifications.md) — cron service notifications; relevance: scheduled-delivery counterpart for exact reminders.
- [snippet_hermes_agent_cron_job_state](../../code_snippets/snippet_hermes_agent_cron_job_state.md) — cron job persisted state; relevance: state model for the scheduled-task alternative.
- [snippet_hermes_agent_cron_job_crud](../../code_snippets/snippet_hermes_agent_cron_job_crud.md) — cron job create/read/update/delete; relevance: lifecycle ops analog to `openclaw commitments` management.
- [snippet_hermes_agent_cron_run_job_execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md) — cron job execution; relevance: due-time firing analog to commitment delivery.
- [snippet_hermes_agent_tools_cronjob_handoff](../../code_snippets/snippet_hermes_agent_tools_cronjob_handoff.md) — cron tool handoff; relevance: how a scheduled obligation is injected into an agent turn (parallel to heartbeat injecting a commitment).
- [snippet_hermes_agent_gw_session_context](../../code_snippets/snippet_hermes_agent_gw_session_context.md) — gateway session context; relevance: the agent/session/channel scoping a commitment is bound to.

### oc_concepts_compaction (10t · 12s · 11d)

**Terms** (`../../term_dictionary/`)
- [term_compaction](../../term_dictionary/term_compaction.md) — conversation summarization to fit the window; relevance: this IS the term the page documents (LINK only, mechanics digested here).
- [term_context_window](../../term_dictionary/term_context_window.md) — model token limit; relevance: compaction's entire purpose is staying inside the context window.
- [term_progressive_summarization](../../term_dictionary/term_progressive_summarization.md) — summarize-older-into-one-entry; relevance: the core compaction algorithm — older turns collapse into a compact summary entry.
- [term_model_failover](../../term_dictionary/term_model_failover.md) — fallback model chain; relevance: a model-eligible compaction error retries through the session fallback chain.
- [term_claude](../../term_dictionary/term_claude.md) — Anthropic Claude models; relevance: the worked compaction-model example is `openrouter/anthropic/claude-sonnet-4-6`.
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: built-in compaction is an LLM summarization pass (a separate model can be configured).
- [term_context_engine](../../term_dictionary/term_context_engine.md) — pluggable context-assembly subsystem; relevance: compaction is one responsibility of the context engine; pluggable providers register `registerCompactionProvider()`.
- [term_session_data](../../term_dictionary/term_session_data.md) — session transcript/state; relevance: the summary is saved into the session transcript; successor transcripts + byte guard operate on session JSONL.
- [term_prompt_caching](../../term_dictionary/term_prompt_caching.md) — provider-side prompt cache; relevance: `/context` distinguishes high prompt/cache usage from compactable history; provider-side context mgmt interacts with the byte guard.
- [term_memory_information_density](../../term_dictionary/term_memory_information_density.md) — token-budget framing; relevance: compaction is a density-management lever (summarize to free window tokens).

**Docs**
- [cc_what_survives_compaction](../claude_code/cc_what_survives_compaction.md) — what persists through compaction; relevance: direct Claude Code analog — what is kept vs summarized.
- [cc_context_window_anatomy](../claude_code/cc_context_window_anatomy.md) — context window breakdown; relevance: the window pressure compaction relieves.
- [cc_manage_your_session](../claude_code/cc_manage_your_session.md) — session management; relevance: `/compact`-equivalent session controls.
- [cc_checkpointing](../claude_code/cc_checkpointing.md) — session checkpointing; relevance: analog of OpenClaw successor-transcript checkpoint metadata.
- [pi_compaction](../pi/pi_compaction.md) — Pi compaction; relevance: sibling coding-agent compaction implementation for comparison.
- [pi_compaction_extensions](../pi/pi_compaction_extensions.md) — Pi pluggable compaction; relevance: analog of OpenClaw pluggable compaction providers.
- [hermes_context_compression_caching](../hermes_agent/hermes_context_compression_caching.md) — Hermes context compression; relevance: closest analog — compression + caching interplay.
- [oc_concepts_context](oc_concepts_context.md) — what the model sees (this series, note 3); relevance: compaction changes what `context` reports; cross-link pair.
- [oc_concepts_context_engine](oc_concepts_context_engine.md) — pluggable engine (this series, note 4); relevance: the engine owns/delegates `compact()`; pluggable-provider relationship.
- [oc_concepts_session_pruning](oc_concepts_session_pruning.md) — pruning (planned, this series, co06); relevance: the lighter-weight complement contrasted in the Compaction-vs-pruning table.
- [oc_reference_session_management_compaction](oc_reference_session_management_compaction.md) — deep dive (planned, this series, rf03); relevance: the page's own "full reference" pointer for reserve tokens/identifier policy.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: auto-compaction, overflow retry, and the `agents.defaults.compaction.*` knobs live here.
- [repo_openclaw_sessions](../../../areas/code_repos/repo_openclaw_sessions.md) — session store; relevance: compaction writes the summary + successor transcript into the session store.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_agents_compaction_chunk_safety](../../code_snippets/snippet_openclaw_agents_compaction_chunk_safety.md) — tool-pair chunk safety; relevance: implements the "keep tool calls paired with toolResults" boundary move described in How it works.
- [snippet_openclaw_agents_compaction_identifier_handoff](../../code_snippets/snippet_openclaw_agents_compaction_identifier_handoff.md) — identifier preservation; relevance: implements `identifierPolicy` strict/off/custom.
- [snippet_openclaw_agents_failover_error](../../code_snippets/snippet_openclaw_agents_failover_error.md) — failover error handling; relevance: the model-fallback-eligible error path compaction retries through.
- [snippet_openclaw_gateway_sessions_compact_reset](../../code_snippets/snippet_openclaw_gateway_sessions_compact_reset.md) — compact/reset session; relevance: `/compact` and `/new` clean-slate flows.
- [snippet_hermes_agent_core_conversation_compression_strategy](../../code_snippets/snippet_hermes_agent_core_conversation_compression_strategy.md) — compression strategy; relevance: analog summarization strategy selection.
- [snippet_hermes_agent_core_conversation_compression_entry](../../code_snippets/snippet_hermes_agent_core_conversation_compression_entry.md) — compression entry point; relevance: analog trigger of a compaction pass.
- [snippet_hermes_agent_core_manual_compression_feedback](../../code_snippets/snippet_hermes_agent_core_manual_compression_feedback.md) — manual compression w/ guidance; relevance: analog of `/compact Focus on <topic>` guided summary.
- [snippet_hermes_agent_core_conversation_loop_context_overflow](../../code_snippets/snippet_hermes_agent_core_conversation_loop_context_overflow.md) — overflow detection; relevance: implements the context-overflow-error → compact-and-retry path.
- [snippet_hermes_agent_core_conversation_loop_payload_too_large](../../code_snippets/snippet_hermes_agent_core_conversation_loop_payload_too_large.md) — payload-too-large recovery; relevance: matches `request_too_large` overflow signature handling.
- [snippet_hermes_agent_core_conversation_loop_length_recovery](../../code_snippets/snippet_hermes_agent_core_conversation_loop_length_recovery.md) — length-error recovery; relevance: matches "input is too long for the model" signature.
- [snippet_openclaw_gateway_session_fs_transcript_candidate_scan](../../code_snippets/snippet_openclaw_gateway_session_fs_transcript_candidate_scan.md) — transcript candidate scan; relevance: successor/checkpoint transcript selection after compaction.
- [snippet_hermes_agent_core_conversation_loop_turn_hydration](../../code_snippets/snippet_hermes_agent_core_conversation_loop_turn_hydration.md) — turn rehydration; relevance: rebuilding context from summary + recent tail (keepRecentTokens behavior).

### oc_concepts_context (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [term_context_window](../../term_dictionary/term_context_window.md) — model token limit; relevance: context IS everything sent to the model, bounded by the window — the page's opening definition.
- [term_context_engineering](../../term_dictionary/term_context_engineering.md) — discipline of curating what the model sees; relevance: the page is the OpenClaw operationalization of context engineering (system prompt + history + tools).
- [term_context_engine](../../term_dictionary/term_context_engine.md) — pluggable assembly subsystem; relevance: the page notes the `legacy` engine assembles context and a plugin can take over.
- [term_compaction](../../term_dictionary/term_compaction.md) — summarization to fit window; relevance: one of the persistence mechanisms in "Sessions, compaction, and pruning".
- [term_subagent](../../term_dictionary/term_subagent.md) — child agent run; relevance: context is managed across subagent boundaries (engine hooks referenced).
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: context is what the LLM receives each run (system prompt + history + tool schemas).
- [term_memory_information_density](../../term_dictionary/term_memory_information_density.md) — token-budget framing; relevance: "what counts toward the window" and tool-schema-vs-text cost are density accounting.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool/function schemas; relevance: tool schemas (JSON) count toward context even though not shown as text — the "two costs" of tools.
- [term_prompt_caching](../../term_dictionary/term_prompt_caching.md) — provider-side cache; relevance: `/context` reports cached session tokens and distinguishes cache usage from compactable history.
- [term_session_data](../../term_dictionary/term_session_data.md) — session transcript/state; relevance: what persists across messages (normal history vs compaction vs pruning) is session state.

**Docs**
- [cc_context_window_anatomy](../claude_code/cc_context_window_anatomy.md) — context window breakdown; relevance: direct analog of "what counts toward the context window".
- [cc_context_cost_by_feature](../claude_code/cc_context_cost_by_feature.md) — per-feature context cost; relevance: analog of the tool-schema / skill-list / system-prompt cost accounting.
- [cc_agent_sdk_context_window](../claude_code/cc_agent_sdk_context_window.md) — SDK context window; relevance: programmatic view of the same window-budget concept.
- [cc_reduce_token_usage](../claude_code/cc_reduce_token_usage.md) — reducing token usage; relevance: the practical "reduce context overhead" goal of `/context`/`/compact`.
- [pi_sessions](../pi/pi_sessions.md) — Pi session model; relevance: sibling-agent persistence model (history/compaction/pruning).
- [hermes_runtime_context_settings](../hermes_agent/hermes_runtime_context_settings.md) — Hermes context settings; relevance: analog of bootstrap injection caps + truncation knobs.
- [hermes_prompt_assembly](../hermes_agent/hermes_prompt_assembly.md) — Hermes prompt assembly; relevance: analog of "how OpenClaw builds the system prompt" each run.
- [oc_concepts_context_engine](oc_concepts_context_engine.md) — pluggable engine (this series, note 4); relevance: the assembly machinery behind context; cross-link pair.
- [oc_concepts_compaction](oc_concepts_compaction.md) — compaction (this series, note 2); relevance: one of the three persistence mechanisms; cross-link pair.
- [oc_concepts_system_prompt](oc_concepts_system_prompt.md) — system prompt (planned, this series, co07); relevance: the page defers the full system-prompt breakdown here.
- [oc_tools_slash_commands](oc_tools_slash_commands.md) — slash commands (planned, this series, to07); relevance: the page defers `/status`/`/context`/directive behavior here.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: system-prompt build, bootstrap injection, tool-schema accounting, and `/context` reporting live here.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_agents_context_lookup](../../code_snippets/snippet_openclaw_agents_context_lookup.md) — context lookup; relevance: backs the `/context` breakdown reporting.
- [snippet_openclaw_agents_system_prompt_context_injection](../../code_snippets/snippet_openclaw_agents_system_prompt_context_injection.md) — system-prompt injection; relevance: implements Project Context workspace-file injection.
- [snippet_openclaw_agents_context_window_guard](../../code_snippets/snippet_openclaw_agents_context_window_guard.md) — window guard; relevance: the budget guard that decides what fits in the window.
- [snippet_openclaw_agents_bootstrap_budget](../../code_snippets/snippet_openclaw_agents_bootstrap_budget.md) — bootstrap budget; relevance: implements `bootstrapMaxChars`/`bootstrapTotalMaxChars` per-file + total caps.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — system-prompt modes; relevance: run vs estimate system-prompt report modes `/context` reports.
- [snippet_hermes_agent_core_prompt_builder_context_loaders](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_loaders.md) — prompt context loaders; relevance: analog of injected-workspace-file loading.
- [snippet_hermes_agent_core_prompt_builder_context_helpers](../../code_snippets/snippet_hermes_agent_core_prompt_builder_context_helpers.md) — prompt context helpers; relevance: analog system-prompt assembly helpers.
- [snippet_hermes_agent_core_prompt_caching](../../code_snippets/snippet_hermes_agent_core_prompt_caching.md) — prompt caching; relevance: cached-token reporting analog.
- [snippet_slipbox_context_assembler](../../code_snippets/snippet_slipbox_context_assembler.md) — knowledge base context assembler; relevance: in-house analog of run-time context assembly from sources.

### oc_concepts_context_engine (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [term_context_engine](../../term_dictionary/term_context_engine.md) — pluggable context-assembly subsystem; relevance: this IS the subject — the `ContextEngine` interface, lifecycle, and selection slot (LINK only).
- [term_context_engineering](../../term_dictionary/term_context_engineering.md) — curating what the model sees; relevance: the engine is the pluggable mechanism that performs context engineering at the four lifecycle points.
- [term_compaction](../../term_dictionary/term_compaction.md) — summarization to fit window; relevance: `compact()` is a required interface member; `ownsCompaction` controls who runs it.
- [term_subagent](../../term_dictionary/term_subagent.md) — child agent run; relevance: optional `prepareSubagentSpawn`/`onSubagentEnded` hooks manage context across subagent boundaries.
- [term_plugin_sdk](../../term_dictionary/term_plugin_sdk.md) — plugin SDK surface; relevance: engines import `openclaw/plugin-sdk/core` (`buildMemorySystemPromptAddition`, `delegateCompactionToRuntime`).
- [term_plugin_manifest](../../term_dictionary/term_plugin_manifest.md) — plugin manifest/`kind`; relevance: a context engine is a `kind: "context-engine"` plugin selected via `plugins.slots.contextEngine`.
- [term_progressive_summarization](../../term_dictionary/term_progressive_summarization.md) — summarize-older-into-one; relevance: the legacy engine's built-in compaction strategy plugin engines can replace.
- [term_dense_retrieval](../../term_dictionary/term_dense_retrieval.md) — vector retrieval; relevance: a plugin engine can implement vector-retrieval assembly ("DAG summaries, vector retrieval, etc.").
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — registered provider plugin; relevance: context engines register via the same plugin-API factory pattern as providers.
- [term_lru_cache](../../term_dictionary/term_lru_cache.md) — bounded cache eviction; relevance: an engine's own data store (ingest/index) needs eviction/budget policy analogous to LRU.

**Docs**
- [cc_sdk_plugins](../claude_code/cc_sdk_plugins.md) — Claude Code SDK plugins; relevance: direct analog of registering a plugin that extends the runtime.
- [cc_plugin_components](../claude_code/cc_plugin_components.md) — plugin component model; relevance: analog of the engine `info`/required-vs-optional member structure.
- [cc_sdk_plugin_structure](../claude_code/cc_sdk_plugin_structure.md) — plugin structure; relevance: analog factory/registration shape.
- [cc_what_survives_compaction](../claude_code/cc_what_survives_compaction.md) — compaction survival; relevance: the engine's `compact()` decides what survives.
- [pi_compaction_extensions](../pi/pi_compaction_extensions.md) — Pi pluggable compaction; relevance: closest sibling — pluggable compaction/context extension interface.
- [hermes_context_engine_plugin](../hermes_agent/hermes_context_engine_plugin.md) — Hermes context-engine plugin; relevance: near-identical concept — a pluggable context engine in a sibling agent.
- [hermes_plugin_extensions_hooks](../hermes_agent/hermes_plugin_extensions_hooks.md) — Hermes plugin hooks; relevance: analog of the four lifecycle hooks (ingest/assemble/compact/afterTurn).
- [oc_concepts_compaction](oc_concepts_compaction.md) — compaction (this series, note 2); relevance: "Relationship to compaction" — compaction is one engine responsibility.
- [oc_concepts_context](oc_concepts_context.md) — context (this series, note 3); relevance: the engine produces what `context` reports; cross-link pair.
- [oc_concepts_memory](oc_concepts_memory.md) — memory plugins (planned, this series, co03); relevance: "Memory plugins are separate from context engines" — the `plugins.slots.memory` contrast.
- [oc_plugins_architecture](oc_plugins_architecture.md) — plugin architecture (planned, this series, pl01); relevance: the page's "registering context engine plugins" pointer.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: assemble/compact lifecycle, runtimeSettings, failure isolation/quarantine live in the runtime.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — plugin/extensions package; relevance: `registerContextEngine` and the plugin-SDK core are exported here.
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory-core; relevance: `buildMemorySystemPromptAddition` / `memory-host-core` an engine pulls active-memory prompt sections from.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_context_engine_delegate](../../code_snippets/snippet_openclaw_context_engine_delegate.md) — context-engine delegate; relevance: implements delegating-mode (`ownsCompaction:false` + `delegateCompactionToRuntime`).
- [snippet_openclaw_context_engine_registry_factories](../../code_snippets/snippet_openclaw_context_engine_registry_factories.md) — engine registry factories; relevance: implements `registerContextEngine(id, factory)` registration.
- [snippet_openclaw_context_engine_registry_compat](../../code_snippets/snippet_openclaw_context_engine_registry_compat.md) — registry compat; relevance: implements the `runtimeSettings` retry-without-it backward-compat path.
- [snippet_openclaw_gateway_server_plugins_fallback_context](../../code_snippets/snippet_openclaw_gateway_server_plugins_fallback_context.md) — plugin fallback to context; relevance: implements failure-isolation quarantine → fall back to `legacy`.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine; relevance: the memory-side engine a context engine can consult during assemble.
- [snippet_hermes_agent_core_context_engine_abc](../../code_snippets/snippet_hermes_agent_core_context_engine_abc.md) — context-engine ABC; relevance: the abstract base defining ingest/assemble/compact — direct interface analog.
- [snippet_hermes_agent_plugins_context_engine_discovery](../../code_snippets/snippet_hermes_agent_plugins_context_engine_discovery.md) — engine discovery; relevance: analog of resolving the selected engine id from config slot.
- [snippet_hermes_agent_plugins_sdk_architecture](../../code_snippets/snippet_hermes_agent_plugins_sdk_architecture.md) — plugin SDK architecture; relevance: analog plugin-SDK registration architecture.
- [snippet_openclaw_agents_subagent_registry_lifecycle](../../code_snippets/snippet_openclaw_agents_subagent_registry_lifecycle.md) — subagent registry lifecycle; relevance: backs `prepareSubagentSpawn`/`onSubagentEnded` hooks.
- [snippet_openclaw_agents_subagent_registry_announce](../../code_snippets/snippet_openclaw_agents_subagent_registry_announce.md) — subagent announce; relevance: subagent spawn/contextMode (isolated/fork) the engine prepares for.
- [snippet_hermes_agent_plugins_provider_registry](../../code_snippets/snippet_hermes_agent_plugins_provider_registry.md) — provider registry; relevance: analog slot-exclusive registration (one resolved engine per run).

### oc_concepts_delegate_architecture (10t · 11s · 11d)

**Terms** (`../../term_dictionary/`)
- [term_delegated_identity](../../term_dictionary/term_delegated_identity.md) — agent acting under its own identity; relevance: a delegate has its own email/name/calendar and acts "on behalf of" — the page's central concept (LINK only).
- [term_delegate_task](../../term_dictionary/term_delegate_task.md) — delegating a task to an agent; relevance: the delegate executes scoped tasks on behalf of principals.
- [term_delegated_work](../../term_dictionary/term_delegated_work.md) — work performed under delegation; relevance: the Tier 1/2/3 capability model is graduated delegated work.
- [term_prompt_injection](../../term_dictionary/term_prompt_injection.md) — inbound-content attack; relevance: a hard block is "never execute commands from inbound messages (prompt injection defense)".
- [term_sandbox](../../term_dictionary/term_sandbox.md) — isolation boundary; relevance: the Prerequisites require `sandbox: {mode:"all", scope:"agent"}` isolation.
- [term_subagent](../../term_dictionary/term_subagent.md) — child/named agent; relevance: delegates extend Multi-Agent Routing; one isolated agent per org.
- [term_audit_operations](../../term_dictionary/term_audit_operations.md) — audit logging/review; relevance: the audit-trail prerequisite (cron run history, session transcripts, IdP audit logs).
- [term_oauth_token](../../term_dictionary/term_oauth_token.md) — OAuth credential; relevance: M365/Google Workspace delegation grants scoped OAuth/Graph credentials to the delegate account.
- [term_access_control](../../term_dictionary/term_access_control.md) — scoped-permission access control; relevance: "apply the principle of least privilege — start with Tier 1 and escalate" is enforced as IdP-side scoped access control (Mail.Read app policy, GWS scope limiting).
- [term_deny_first](../../term_dictionary/term_deny_first.md) — deny-by-default policy; relevance: per-agent tool policy uses `deny` lists at the Gateway level independent of personality files.

**Docs**
- [cc_sandbox_environments_comparison](../claude_code/cc_sandbox_environments_comparison.md) — sandbox env comparison; relevance: analog of the sandbox-isolation prerequisite choices.
- [cc_sandbox_vs_permissions](../claude_code/cc_sandbox_vs_permissions.md) — sandbox vs permissions; relevance: mirrors "tool policy operates independently of personality files" (Gateway-level enforcement).
- [cc_prompt_injection_defenses](../claude_code/cc_prompt_injection_defenses.md) — prompt-injection defenses; relevance: directly analogous to the "never execute inbound commands" hard block.
- [cc_admin_enforcement_controls](../claude_code/cc_admin_enforcement_controls.md) — org enforcement controls; relevance: analog of identity-provider-enforced scope independent of agent config.
- [cc_security_architecture](../claude_code/cc_security_architecture.md) — security architecture; relevance: the layered hardening (hard blocks → tool policy → sandbox → audit) maps to a defense-in-depth model.
- [pi_security_model](../pi/pi_security_model.md) — Pi security model; relevance: sibling-agent threat/permission model for an autonomous agent.
- [hermes_subagent_delegation](../hermes_agent/hermes_subagent_delegation.md) — Hermes subagent delegation; relevance: closest analog — delegating work to a named/isolated agent.
- [oc_concepts_multi_agent](oc_concepts_multi_agent.md) — multi-agent routing (planned, this series, co05); relevance: the page explicitly "extends Multi-Agent Routing" + uses its bindings/auth isolation.
- [oc_gateway_sandboxing](oc_gateway_sandboxing.md) — sandboxing (planned, this series, gw05); relevance: the page's "See Sandboxing" pointer for the isolation prerequisite.
- [oc_automation_standing_orders](oc_automation_standing_orders.md) — standing orders (planned, this series, au01); relevance: Tier 3 autonomy runs `AGENTS.md` standing orders.
- [oc_tools_subagents](oc_tools_subagents.md) — sub-agents (planned, this series, to07); relevance: the page's "Sub-agents" Related pointer.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: `agents.list[]`, bindings, per-agent `agentDir`/auth isolation are runtime features.
- [repo_openclaw_security](../../../areas/code_repos/repo_openclaw_security.md) — security package; relevance: tool policy, dangerous-tool deny, external-content handling enforce the hard blocks.
- [repo_openclaw_gateway](../../../areas/code_repos/repo_openclaw_gateway.md) — gateway; relevance: Gateway-level tool policy and channel bindings route inbound messages to the delegate.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — per-agent tool policy; relevance: implements the `tools.allow`/`deny` Gateway-level boundary.
- [snippet_openclaw_agents_identity](../../code_snippets/snippet_openclaw_agents_identity.md) — agent identity; relevance: implements the delegate's own `identity: {name}` (display name on outbound messages).
- [snippet_openclaw_agents_auth_profiles_order_credential](../../code_snippets/snippet_openclaw_agents_auth_profiles_order_credential.md) — auth-profile credential order; relevance: implements the delegate's own `auth-profiles.json` isolation.
- [snippet_openclaw_security_dangerous_tools_deny](../../code_snippets/snippet_openclaw_security_dangerous_tools_deny.md) — dangerous-tools deny; relevance: enforces the non-negotiable hard blocks.
- [snippet_openclaw_security_external_content](../../code_snippets/snippet_openclaw_security_external_content.md) — external-content handling; relevance: the prompt-injection / untrusted-inbound defense.
- [snippet_openclaw_security_audit_exec_runtime](../../code_snippets/snippet_openclaw_security_audit_exec_runtime.md) — audit exec runtime; relevance: the audit-trail prerequisite for delegate actions.
- [snippet_hermes_agent_tools_delegate_prompt](../../code_snippets/snippet_hermes_agent_tools_delegate_prompt.md) — delegate prompt; relevance: analog of the on-behalf-of delegation framing.
- [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — delegate spawn; relevance: analog of creating an isolated delegate agent.
- [snippet_hermes_agent_tools_credential_files](../../code_snippets/snippet_hermes_agent_tools_credential_files.md) — credential files; relevance: per-agent credential isolation analog (never share the main agentDir).
- [snippet_openclaw_sessions_send_policy](../../code_snippets/snippet_openclaw_sessions_send_policy.md) — send policy; relevance: the Tier-1 "draft, never send without approval" outbound gate.

**Analysis** (`../../analysis_thoughts/`)

### oc_concepts_dreaming (10t · 11s · 10d)

**Terms** (`../../term_dictionary/`)
- [term_memory_dreaming](../../term_dictionary/term_memory_dreaming.md) — background memory-consolidation phases; relevance: this IS the subject — light/deep/REM consolidation in `memory-core` (LINK only).
- [term_agentic_memory](../../term_dictionary/term_agentic_memory.md) — durable agent memory; relevance: deep phase promotes durable candidates into `MEMORY.md` (the long-term store).
- [term_episodic_memory](../../term_dictionary/term_episodic_memory.md) — event/session memory; relevance: dreaming ingests redacted session transcripts + daily memory signals (episodic source material).
- [term_progressive_summarization](../../term_dictionary/term_progressive_summarization.md) — staged summarization/promotion; relevance: the light→deep→REM staging and promotion is progressive consolidation.
- [term_information_retrieval](../../term_dictionary/term_information_retrieval.md) — retrieval-quality scoring; relevance: the Relevance (0.30) deep-ranking signal is "average retrieval quality for the entry".
- [term_cron](../../term_dictionary/term_cron.md) — cron scheduling; relevance: `memory-core` auto-manages one cron job (`dreaming.frequency: "0 3 * * *"`) for the sweep.
- [term_subagent](../../term_dictionary/term_subagent.md) — child agent turn; relevance: the Dream Diary runs a best-effort background subagent turn (`dreaming.model`).
- [term_feature_flags](../../term_dictionary/term_feature_flags.md) — opt-in toggle; relevance: dreaming is opt-in / disabled by default (`dreaming.enabled`).
- [term_heartbeat](../../term_dictionary/term_heartbeat.md) — periodic agent turn; relevance: "Dreaming never runs: blocked" is caused by the default-agent heartbeat not firing.
- [term_plugmem](../../term_dictionary/term_plugmem.md) — pluggable memory store; relevance: `memory-core` is configured under `plugins.entries.memory-core.config.dreaming` (a memory plugin).

**Docs**
- [cc_memory_overview](../claude_code/cc_memory_overview.md) — memory overview; relevance: direct analog of the durable-memory layer dreaming promotes into.
- [cc_auto_memory](../claude_code/cc_auto_memory.md) — automatic memory; relevance: closest analog — automatic background promotion of strong signals.
- [cc_background_session_hosting](../claude_code/cc_background_session_hosting.md) — background session hosting; relevance: analog of the background sweep that runs without a user turn.
- [hermes_persistent_memory](../hermes_agent/hermes_persistent_memory.md) — Hermes durable memory; relevance: analog persistent-memory promotion target.
- [hermes_memory_provider_catalog](../hermes_agent/hermes_memory_provider_catalog.md) — memory provider catalog; relevance: `memory-core` is one such pluggable memory provider.
- [hermes_session_search_storage](../hermes_agent/hermes_session_search_storage.md) — session search/storage; relevance: analog of ingesting redacted session transcripts into the consolidation corpus.
- [oc_concepts_memory](oc_concepts_memory.md) — memory overview (planned, this series, co03); relevance: dreaming's parent system; `MEMORY.md` durable store home doc.
- [oc_concepts_memory_search](oc_concepts_memory_search.md) — memory search (planned, this series, co04); relevance: the recall/retrieval surface whose quality feeds the Relevance ranking signal.
- [oc_cli_memory](oc_cli_memory.md) — `openclaw memory` CLI (planned, this series, cl04); relevance: home doc for `memory promote`/`promote-explain`/`rem-harness`/`status --deep`.
- [oc_reference_memory_config](oc_reference_memory_config.md) — memory config reference (planned, this series, rf02); relevance: the page's "full key list" pointer for phase thresholds/storage.

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_memory](../../../areas/code_repos/repo_openclaw_memory.md) — memory-core; relevance: dreaming, phases, Dream Diary, deep ranking, and promotion all live in `memory-core`.
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: the background subagent turn + heartbeat-gated sweep run through the agent runtime.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_memory_dreaming_constants](../../code_snippets/snippet_openclaw_memory_dreaming_constants.md) — dreaming constants; relevance: the six weighted deep-ranking signal weights + thresholds.
- [snippet_openclaw_memory_dreaming_resolvers](../../code_snippets/snippet_openclaw_memory_dreaming_resolvers.md) — dreaming resolvers; relevance: phase resolution (light/deep/REM) + candidate ranking logic.
- [snippet_openclaw_gateway_doctor_memory_dreaming_preview](../../code_snippets/snippet_openclaw_gateway_doctor_memory_dreaming_preview.md) — doctor dreaming preview; relevance: backs `/dreaming status` + Dreams UI state.
- [snippet_openclaw_gateway_doctor_dream_diary_repair_cron](../../code_snippets/snippet_openclaw_gateway_doctor_dream_diary_repair_cron.md) — dream-diary repair cron; relevance: the auto-managed dreaming-sweep cron + diary backfill/repair.
- [snippet_openclaw_memory_engine](../../code_snippets/snippet_openclaw_memory_engine.md) — memory engine; relevance: the engine that rehydrates snippets from daily files before deep-phase writes.
- [snippet_openclaw_memory_events](../../code_snippets/snippet_openclaw_memory_events.md) — memory events; relevance: short-term recall signals/reinforcement the phases accumulate.
- [snippet_openclaw_memory_runtime](../../code_snippets/snippet_openclaw_memory_runtime.md) — memory runtime; relevance: the `memory-core` runtime orchestrating the sweep.
- [snippet_openclaw_memory_host_session_files_classify](../../code_snippets/snippet_openclaw_memory_host_session_files_classify.md) — session-file classify; relevance: classifying/redacting session transcripts before ingestion.
- [snippet_hermes_agent_core_curator_transitions](../../code_snippets/snippet_hermes_agent_core_curator_transitions.md) — curator phase transitions; relevance: analog of the staged light→REM→deep phase transitions.
- [snippet_openclaw_memory_embedding_inputs](../../code_snippets/snippet_openclaw_memory_embedding_inputs.md) — memory embedding inputs; relevance: the conceptual-richness / recall-quality inputs feeding ranking.

### oc_concepts_experimental_features (10t · 11s · 10d)

**Terms** (`../../term_dictionary/`)
- [term_feature_flags](../../term_dictionary/term_feature_flags.md) — opt-in config toggles; relevance: experimental flags ARE the subject — `.experimental` opt-in preview surfaces (LINK only).
- [term_llm](../../term_dictionary/term_llm.md) — large language model; relevance: lean mode exists for weaker local-model backends that choke on the full tool surface.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — tool/function schemas; relevance: the three dropped tools have the largest schemas; lean mode is about tool-call payload pressure (400 on payload size).
- [term_tool_registry](../../term_dictionary/term_tool_registry.md) — tool catalog/search gating; relevance: lean mode defaults large catalogs behind `tool_search`/`tool_describe`/`tool_call` (Tool Search).
- [term_context_window](../../term_dictionary/term_context_window.md) — model token limit; relevance: lean mode keeps tool schemas from "crowding out conversation history" on small-context backends.
- [term_memory_information_density](../../term_dictionary/term_memory_information_density.md) — token-budget framing; relevance: the schema-vs-history budget trade-off lean mode manages.
- [term_session_data](../../term_dictionary/term_session_data.md) — session state/memory; relevance: the `sessionMemory` experimental flag indexes prior session transcripts.
- [term_structured_output](../../term_dictionary/term_structured_output.md) — structured tool/plan output; relevance: the `planTool` experimental flag exposes the structured `update_plan` tool.
- [term_tool_descriptor](../../term_dictionary/term_tool_descriptor.md) — tool schema/descriptor; relevance: lean mode trims the descriptor surface; descriptors are what crowd the prompt.
- [term_provider_plugin](../../term_dictionary/term_provider_plugin.md) — provider/plugin surface; relevance: the `codex.config...sandboxExecServer` experimental flag targets the Codex harness plugin.

**Docs**
- [cc_cli_flags](../claude_code/cc_cli_flags.md) — CLI flags; relevance: analog of opt-in preview flags surfaced explicitly in config.
- [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — execution tool behavior; relevance: analog of how trimming the tool surface changes agent-turn behavior.
- [cc_sdk_typescript_query_object](../claude_code/cc_sdk_typescript_query_object.md) — SDK query object; relevance: analog config surface where experimental/preview options live.
- [hermes_tool_search](../hermes_agent/hermes_tool_search.md) — Hermes Tool Search; relevance: direct analog of the Tool Search default lean mode enables.
- [hermes_tools_toolsets](../hermes_agent/hermes_tools_toolsets.md) — toolsets; relevance: analog of narrowing the active tool surface (lean-mode counterpart to `tools.profile`).
- [hermes_tips_best_practices](../hermes_agent/hermes_tips_best_practices.md) — tips/best practices; relevance: "prefer the stable path; test experimental in a smaller environment" hygiene guidance.
- [oc_gateway_local_models](oc_gateway_local_models.md) — local models (planned, this series, gw03); relevance: the `localModelLean` flag's home doc (the page's "More" pointer).
- [oc_tools_tool_search](oc_tools_tool_search.md) — tool search (planned, this series, to08); relevance: the structured Tool Search controls lean mode defaults to.
- [oc_gateway_config_tools](oc_gateway_config_tools.md) — tools config (planned, this series, gw01); relevance: home of `tools.experimental.planTool` referenced in the flags table.
- [oc_concepts_features](oc_concepts_features.md) — features overview (planned, this series, co03); relevance: the page's "Features" Related pointer (stable vs experimental surfaces).

**Repos** (`../../../areas/code_repos/`)
- [repo_openclaw_agents](../../../areas/code_repos/repo_openclaw_agents.md) — agent runtime; relevance: `agents.defaults.experimental.localModelLean` tool-surface trimming runs in the runtime.
- [repo_openclaw_extensions](../../../areas/code_repos/repo_openclaw_extensions.md) — extensions; relevance: the Codex-harness `sandboxExecServer` experimental flag targets a plugin extension.

**Snippets** (`../../code_snippets/`)
- [snippet_openclaw_agents_tool_catalog](../../code_snippets/snippet_openclaw_agents_tool_catalog.md) — tool catalog; relevance: the catalog lean mode keeps behind Tool Search.
- [snippet_openclaw_agents_system_prompt_modes](../../code_snippets/snippet_openclaw_agents_system_prompt_modes.md) — system-prompt modes; relevance: lean mode changes which tools are listed in the system prompt.
- [snippet_openclaw_agents_tool_policy](../../code_snippets/snippet_openclaw_agents_tool_policy.md) — tool policy; relevance: the stable `tools.allow`/`deny`/`profile` knobs lean mode is contrasted with.
- [snippet_hermes_agent_tools_registry](../../code_snippets/snippet_hermes_agent_tools_registry.md) — tools registry; relevance: analog registry that lean mode gates behind Tool Search.
- [snippet_hermes_agent_cli_tools_policy](../../code_snippets/snippet_hermes_agent_cli_tools_policy.md) — CLI tools policy; relevance: analog of `openclaw status --deep` confirming the trimmed tool list.
- [snippet_hermes_agent_model_tools_capability_probe](../../code_snippets/snippet_hermes_agent_model_tools_capability_probe.md) — model tool-capability probe; relevance: analog of `compat.supportsTools:false` escape hatch detection.
- [snippet_hermes_agent_model_tools_introspection](../../code_snippets/snippet_hermes_agent_model_tools_introspection.md) — model tool introspection; relevance: probing whether a backend tolerates the full tool surface (lean-mode signal chain).
- [snippet_hermes_agent_toolsets_definitions](../../code_snippets/snippet_hermes_agent_toolsets_definitions.md) — toolset definitions; relevance: analog of which tools form the default vs trimmed surface.
- [snippet_hermes_agent_core_tool_executor_concurrent](../../code_snippets/snippet_hermes_agent_core_tool_executor_concurrent.md) — concurrent tool executor; relevance: the tool-execution path affected by trimming `browser`/`cron`/`message`.
- [snippet_openclaw_agents_memory_search](../../code_snippets/snippet_openclaw_agents_memory_search.md) — memory search; relevance: the `sessionMemory` experimental flag indexes prior transcripts for `memory_search`.
- [snippet_openclaw_skills_planner](../../code_snippets/snippet_openclaw_skills_planner.md) — skills planner; relevance: analog of the structured `update_plan` planTool for multi-step work tracking.

## Undigested Terms Plan

| Term | Disposition |
|------|-------------|
| commitment (inferred follow-up) | Digested as `oc_concepts_commitments.md` (its home doc page). Not a `term_dictionary` capture. |
| compaction | Existing `term_compaction` — LINK only; mechanics digested in `oc_concepts_compaction.md`. |
| context / context window | Existing `term_context_window` + `term_context_engineering` — LINK only; the OpenClaw-specific meaning digested in `oc_concepts_context.md`. |
| context engine | Existing `term_context_engine` — LINK only; the pluggable interface digested in `oc_concepts_context_engine.md`. |
| delegate / delegate architecture | Existing `term_delegated_identity` / `term_delegate_task` / `term_delegated_work` — LINK only; the OpenClaw deployment pattern digested in `oc_concepts_delegate_architecture.md`. |
| dreaming (light/deep/REM, Dream Diary) | Existing `term_memory_dreaming` — LINK only; mechanics digested in `oc_concepts_dreaming.md`. |
| experimental features / feature flags | Existing `term_feature_flags` — LINK only; the OpenClaw flag policy + lean mode digested in `oc_concepts_experimental_features.md`. |
| heartbeat / cron / scheduled tasks | Existing `term_heartbeat` / `term_cron` — LINK only (delivery + reminder vocabulary); home docs in gw03/au01. |
| memory flush / memory promotion | Link existing `term_agentic_memory` / `term_progressive_summarization`; home doc `concepts/memory` (co03), not a new term. |
| local model lean mode / Tool Search | Config behavior; link `term_tool_registry` / `term_llm`; home docs gw03 (local-models) / to08 (tool-search). Not promoted. |
| pluggable compaction provider | Config surface of `oc_concepts_compaction.md`; link `term_context_engine`. Not a new term. |
| Microsoft 365 / Google Workspace delegation | Provider-specific setup detail inside `oc_concepts_delegate_architecture.md`; not promoted to terms. |

**New `term_dictionary` captures planned: 0.** All concept vocabulary on these 7 pages either (a) has its
home as an `oc_*` doc note in this sub-plan, or (b) already has a substantive existing term note to LINK. No
genuinely cross-cutting, vault-reusable term lacks both a doc-page home and an existing note, so no
`/tessellum-capture-term-note` is triggered and no `acronym_glossary_*.md` edit is required (consistent with the
master's near-0 expectation and the claude_code/pi precedents).

## Term-Note Authoring Requirements

**N/A (0 new terms).** This sub-plan authors zero `term_dictionary` notes; it only LINKS existing terms.
The master's multi-source-research term-authoring mandate does not apply. (Inherited from master — if augment
Step 2d surfaces a genuinely reusable new term, this section is replaced with the per-term research mandate
and the chosen `acronym_glossary_*.md`.)

## Per-Phase Validation Gate (G1–G9) — inherited from master

Single execution phase (7 notes, P1). All gates must PASS before commit.

| Gate | Check | Tooling |
|------|-------|---------|
| G1 | Format: YAML field order/forbidden fields, `## Overview` + `## Related Notes` present, footer bold lines | `/tessellum-check-note-format` + `scripts/check_yaml_frontmatter.py` |
| G2 | Grounding: every claim traces to `inbox/openclaw_docs/concepts/<page>.md` (no invented config keys/flags) | diff vs mirror source |
| G3 | Density + Coverage: each note ≤400 lines / ≤2,500 words / ≤6 code blocks, single BB; all H2/H3 from the Coverage Map present | `wc -w` + fence count + Section Coverage Map |
| G4 | Cross-Reference: ≥6 relevancy-selected term links + repo/sibling/doc/snippet links per note, each with a relevance statement, indexed `[text](path.md)` form | manual + `note_links` query |
| G5 | Ghost-reference: every Related-Notes target resolves to an existing note (or a "(planned)" sibling in this/other co0x sub-plan) | `/tessellum-fix-ghost-references` + DB check |
| G6 | Broken-link fix: relative paths correct from `resources/documentation/openclaw/` | `/tessellum-fix-broken-links` |
| G7/G8 | Discoverability: each new note RECEIVES ≥1 inbound link from outside `documentation/openclaw/` (in-degree ≥1, anti-island) — via `entry_openclaw_docs.md` + repo/term inlinks | `note_links` in-degree query |
| G9 | Prose integrity — no mid-paragraph hard-wrap: a prose line ending mid-sentence (`[a-z0-9,;:)]`) MUST NOT be immediately followed by another prose line; each paragraph stays on ONE logical source line (break only at paragraph end / list / table / code). Applies to authored note bodies AND `## Overview`/`## Related Notes` prose. | `/tessellum-check-note-format` PROSE-001 (error) — part of G1; verify 0 PROSE-001 per note |

## Validation Scripts

```bash
DB=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
GATE_DIR=the vault/resources/documentation/openclaw
REQ_SECTIONS="## Overview|## Related Notes"
REQUIRE_SOURCE_URL=1
SIBLING_PREFIX="oc_"
NOTES="oc_concepts_commitments oc_concepts_compaction oc_concepts_context oc_concepts_context_engine oc_concepts_delegate_architecture oc_concepts_dreaming oc_concepts_experimental_features"

for n in ${=NOTES}; do
  f="$GATE_DIR/$n.md"
  [ -f "$f" ] || { echo "MISSING FILE: $n"; continue; }
  # G1 format + broken-link (LINK-003)
  python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n FORMAT OK"
  # required sections present
  for sec in ${(s:|:)REQ_SECTIONS}; do grep -qF "$sec" "$f" || echo "$n MISSING SECTION: $sec"; done
  # source_url present (G2 grounding marker)
  [ "$REQUIRE_SOURCE_URL" = 1 ] && { grep -q '^source_url: https://docs.openclaw.ai/' "$f" || echo "$n MISSING source_url"; }
  # G3 density: words (body only) + code blocks
  words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  { [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ]; } && echo "DENSITY WARNING: $n ($words w / $cb code)"
  # G4 sibling-prefix cross-ref present
  grep -q "$SIBLING_PREFIX" "$f" || echo "$n NO SIBLING ($SIBLING_PREFIX) LINK"
done

# YAML frontmatter sweep across the folder
python3 scripts/check_yaml_frontmatter.py --path "$GATE_DIR"

# G5 ghost / G8 in-degree (post-reindex)
bash scripts/update_notes_database.sh --force
for n in ${=NOTES}; do
  [ "${indeg:-0}" -ge 1 ] || echo "ISLAND (in_degree<1): $n"
done
```

## Density Re-Assessment

| # | Note | BB | ~Words | Source code fences | Code kept (≤6) | Within caps? |
|---|---|---|---:|---:|---:|---|
| 1 | oc_concepts_commitments | procedure | 600 | 4 | ≤4 | ✅ |
| 2 | oc_concepts_compaction | procedure | 700 | 6 | ≤6 | ✅ |
| 3 | oc_concepts_context | concept | 700 | 2 | ≤2 | ✅ |
| 4 | oc_concepts_context_engine | model | 750 | 8 | 6 (factory + slot + 4 selected) | ✅ |
| 5 | oc_concepts_delegate_architecture | procedure | 750 | 9 | 6 (tool policy, sandbox, M365, GWS, bindings, example) | ✅ |
| 6 | oc_concepts_dreaming | procedure | 700 | 6 | ≤6 | ✅ |
| 7 | oc_concepts_experimental_features | concept | 550 | 3 | ≤3 | ✅ |

No note approaches the 2,500-word / 400-line cap. The two code-heavy pages (context-engine 8 fences, delegate
9 fences) are trimmed to ≤6 by reproducing only the most load-bearing config/code blocks verbatim and
prose-summarizing the remainder; no information loss (all config keys still named, just not all fenced).

## Entry Point Decision (inherited from master)

Contributes **7 rows** to `entry_openclaw_docs.md` (CREATED as the W1 master pre-step before any sub-plan
executes) under the **Concepts** section (co02 cluster). Each new note receives its entry-point back-link at
finalization, satisfying G7/G8 (≥1 inbound link from outside `documentation/openclaw/`). No new entry point is
created by this sub-plan; the master hub already crosses the >30-note threshold corpus-wide.

## Inlinks (existing notes → new notes)

Candidate outside-folder inbound links (DB-verify at execution; satisfy G7/G8 in-degree ≥1):

- `entry_openclaw_docs.md` (planned, W1) → all 7 notes (primary anti-island link).
- `repo_openclaw_memory.md` → notes 1, 6 (commitments + dreaming live in `memory-core`).
- `repo_openclaw_agents.md` → notes 2, 3, 4, 5, 7 (compaction/context/engine/delegate/experimental runtime).
- `repo_openclaw_sessions.md` → note 2 (compaction writes session transcripts).
- `repo_openclaw_extensions.md` → note 4 (context-engine plugin registration).
- `repo_openclaw_security.md` → note 5 (delegate hardening / tool policy / sandbox).
- `term_compaction.md` → note 2; `term_context_engine.md` → note 4; `term_context_window.md` → note 3;
  `term_memory_dreaming.md` → note 6; `term_delegated_identity.md` → note 5; `term_feature_flags.md` → notes 1, 7.
  `counter_openclaw_autonomy_breaks_slipbox_gates.md` → note 5 (delegate autonomy boundary).

## Pacing Rules (inherited from master)

One execution phase, 7 notes (≤30 fan-out cap, no sub-batching needed). Re-read each source page before
authoring; reproduce config snippets verbatim; one BB per note; ≤6 code blocks. Run all 8 gates before commit.
`git pull --rebase --autostash origin main` first; commit + push the wave together; no Claude co-author
trailer. Reindex incrementally (`bash scripts/update_notes_database.sh --force`) and verify `note_links` +
0 broken links + in-degree ≥1 before committing.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-20** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-21** (xref mapping locked at raised floors) |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-21 — READY (9/9)** |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (2026-06-21)

**Scope of this augment run:** xref-augment — re-read all 7 source pages under
`inbox/openclaw_docs/concepts/` (measured words match the plan's Source table exactly: 767 / 1,164 / 1,295 /
2,146 / 1,692 / 1,505 / 848 = 9,417), then replaced the PLAN-stage `## Candidate Cross-References` pools with
a **LOCKED Per-Note Related Notes Mapping at RAISED floors** (≥8 terms · ≥10 snippets · ≥10 docs per note,

**What was locked (per-note achieved counts):**

| Note | Terms | Snippets | Docs (existing + planned) | Repos | Analysis | Floors met |
|---|---:|---:|---|---:|---:|---|
| oc_concepts_commitments | 10 | 11 | 10 (6 + 4) | 2 | 0 | ✅ |
| oc_concepts_compaction | 10 | 12 | 11 (7 + 4) | 2 | 0 | ✅ |
| oc_concepts_context | 10 | 11 | 11 (7 + 4) | 1 | 0 | ✅ |
| oc_concepts_context_engine | 10 | 11 | 11 (7 + 4) | 3 | 0 | ✅ |
| oc_concepts_delegate_architecture | 10 | 11 | 11 (7 + 4) | 3 | 2 | ✅ |
| oc_concepts_dreaming | 10 | 11 | 10 (6 + 4) | 2 | 0 | ✅ |
| oc_concepts_experimental_features | 10 | 11 | 10 (6 + 4) | 2 | 0 | ✅ |

**Verification performed (2026-06-21):**
  returned 1. Terms (term_dictionary), docs (claude_code/pi/hermes_agent/band), snippets (code_snippets),
  repos (areas/code_repos), and analysis/counter/thought notes all confirmed present.
- Programmatic ghost-sweep of the full LOCKED section: **239 → 240 markdown `.md` links, 211 EXISTING
  satisfying the "≥5 of 10 docs existing" rule; the remaining 4 docs/note are sibling `oc_*` "(planned, this
  series)" with correct relative-path slugs per the master filename rule.
- Relative-path conventions confirmed to resolve from
  `resources/documentation/openclaw/oc_X.md`: term `../../term_dictionary/`, sibling `oc_Y.md`, other doc
  `../<folder>/`, repo `../../../areas/code_repos/`, snippet `../../code_snippets/`, analysis
  `../../analysis_thoughts/`.

**New-term candidates surfaced (Step 2d re-read):** **0 new `term_dictionary` captures.** The re-read of all
7 pages confirmed the master/sub-plan design decision — every OpenClaw concept on these pages either has its
home as an `oc_*` doc note in this sub-plan or already has a substantive existing term note to LINK. One
candidate slug, `term_least_privilege`, was considered for the delegate note (the page's explicit "principle
of least privilege" mandate) but a vault existence check returned MISSING, AND the concept is already
substantively covered by the existing `term_access_control.md` (IdP-side scoped access: Mail.Read app policy,
GWS scope limiting) — so it was **rejected (collision: link existing `term_access_control` instead of
creating)**, consistent with the master's near-0 new-term expectation. Best-fit glossary had a new term been
created would have been `acronym_glossary_ai_ml.md` (agentic/LLM glossary); not triggered. Undigested Terms
Plan unchanged: **0 new captures.**

**Issues / notes for execution:** none blocking. The 23 planned `oc_*` sibling docs do not exist yet (this
series + co03/co04/co05/co06/co07/gw01/gw03/gw05/au01/cl02/cl04/pl01/to07/to08/rf02/rf03 are all "pending"
in the master index); they are correctly cited "(planned, this series)" and will resolve as their sub-plans
execute. At execution, G5 ghost-detection will flag any still-unbuilt `oc_*` target — expected and handled by
the master's cross-sub-plan "(planned)" convention; the executor links to the entry point + existing notes
and leaves planned siblings as forward references that fill in over the wave.

## Review Sign-Off (/tessellum-review-digestion-plan, 2026-06-21)

Read-only final review against the 9 mandatory checkpoints. Source pages spot-checked (CP7) by re-measuring
`wc -w` against the plan's Source table.

| CP | Checkpoint | Verdict | Evidence |
|---|---|---|---|
| CP1 | Related Notes step (≥8 terms + floors) | **PASS** | `## Per-Note Related Notes Mapping (LOCKED …)` present; every note has 10 terms (≥8), 11–12 snippets (≥10), 10–11 docs (≥10, ≥5 existing), each link rendered `- [Name](relpath.md) — desc; relevance: …` with a per-link relevancy statement. 0 bare links. |
| CP2 | 9-GATE present per batch (G1–G6 + G7/G8 + G9) | **PASS** | `## Per-Phase Validation Gate (G1–G9)` table lists G1 format, G2 grounding (diff vs `inbox/openclaw_docs/concepts/<page>`), G3 density+coverage, G4 cross-ref, G5 ghost (`/tessellum-fix-ghost-references` + DB), G6 broken-link (`/tessellum-fix-broken-links`), G7/G8 discoverability (in-degree ≥1). Single execution phase; M=1 table ≥ N=1 phase. |
| CP4 | Plan size manageable | **PASS** | 7 planned notes ≤ 30; single execution phase; no sub-batching needed (≤30 fan-out cap). |
| CP5 | Format derived (not invented) | **PASS** | Format inherited from master `## Format Definition (Shared)`, derived from existing `claude_code/` (`cc_*`) + `pi/` (`pi_*`) doc corpora: `## Overview` opener (not `## Definition`), `## Related Notes` reference section, footer `**Source**`/`**Last Updated**`/`**Status**`, fixed YAML field order, forbidden-field list. Matches actual target-sibling notes. |
| CP6 | Density / borderline → split | **PASS** | `## Density Re-Assessment`: all 7 notes 550–750 est. words, ≤6 code blocks (context-engine 8→6, delegate 9→6 by selecting load-bearing fences), single BB each; none approaches the 2,500-word / 400-line cap. No borderline note left unaddressed. |
| CP7 | Source word counts measured | **PASS** | Re-measured `wc -w` on all 7 mirror pages: 767 / 1,164 / 1,295 / 2,146 / 1,692 / 1,505 / 848 — **exact match** to the plan's Source table (ratio 1.00). No under-estimation; largest page (2,146w) under the 2,500 split threshold. |
| CP8 | Undigested terms + authoring reqs | **PASS** | `## Undigested Terms Plan` present (12 rows, all dispositioned LINK-existing or digest-as-oc_doc); **0 new captures** → `## Term-Note Authoring Requirements` correctly N/A with the inherited-mandate fallback clause. Augment Step 2d re-scan surfaced 0 new terms. |
| CP8f | Slug specificity / collision audit | **PASS** | Collision audit performed across term_dictionary AND documentation/: the only candidate slug (`term_least_privilege`) flagged — MISSING in vault + duplicates substantive `term_access_control.md` → REJECTED, rerouted to link existing (recorded in Augmentation Report). No too-general slugs created; no doc-note duplicates an existing term note. |
| CP9 | Discoverability / inlinks | **PASS** | `## Inlinks (existing notes → new notes)` maps every new note to ≥1 outside-folder inbound link (`entry_openclaw_docs` → all 7; `repo_openclaw_*` → notes per package; `term_*` → notes; analysis/counter → notes 4/5). G7/G8 in-degree ≥1 in the gate table; inlink addition is a gated execution step, not "recommended". |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status advanced `pending` → `ready`.
