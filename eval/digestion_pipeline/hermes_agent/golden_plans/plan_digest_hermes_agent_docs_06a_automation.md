---
title: Hermes Agent Docs Digestion — Sub-Plan 06a — Automation & Multi-Agent (scheduling / delegation / code-exec / goals / batch)
date: 2026-06-15
revised: 2026-06-19
mirror_commit: c253b07
status: completed
master_plan: plan_digest_hermes_agent_docs_master.md
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/
pages:
  - user-guide/features/cron.md
  - user-guide/features/delegation.md
  - user-guide/features/code-execution.md
  - user-guide/features/goals.md
  - user-guide/features/batch-processing.md
---

# Sub-Plan 06a: Automation & Multi-Agent (scheduling / delegation / code-exec / goals / batch)

> Self-contained sub-plan (canonical Steps 2–8), AUGMENTED + REVIEWED 2026-06-15. Inherits shared
> Routing, Note Format Definition, Dedup Policy, Cross-References, 8-GATE, Pacing from
> [the master](plan_digest_hermes_agent_docs_master.md). **Part a of the SP06 split** — SP06b owns the
> heavier pages (kanban / kanban-tutorial / hooks / plugins / built-in-plugins). This file is the ONLY
> place SP06a's note filenames/BBs/coverage are defined.

## Scope

The unattended/agentic-execution surface of Hermes Agent: scheduled tasks (`cronjob`), subagent
delegation (`delegate_task`), programmatic Python tool-calling (`execute_code`), standing-objective
loops (`/goal`, the Ralph loop), and offline trajectory generation at scale (`batch_runner.py`). Source =
5 mirrored pages in `inbox/hermes_agent_docs/user-guide/features/` (all substantive). **P2 / features**.
These pages cross-link DOWN to the existing code layer (`repo_hermes_agent_cron`, `repo_hermes_agent_tools`,
`repo_hermes_agent_trajectory_research`, the `snippet_hermes_agent_{cron,tools_delegate,tools_code_exec,batch_runner,trajectory}_*`
corpus) and SIDEWAYS to SP02 config (`hermes_security_skill_memory_settings` holds the delegation/code-exec/cron
config blocks) and SP09 (provider recovery / credential pools).

## Content Strategy

- **One BB per note.** `cron.md` (3861w, 37 code) mixes a procedural lifecycle workflow with a distinct
  data-flow/gating *model* (no-agent mode, `wakeAgent` gates, `context_from` chaining, toolset selection,
  provider recovery) → split into 2 (see Split Decisions). The other four pages are single-BB → 1 note each.
- **Do NOT duplicate** content owned by other sub-plans → **link-outs**, not copied content: the
  delegation/code-exec/cron/goals *config blocks* (SP02 `hermes_security_skill_memory_settings` +
  `hermes_model_aux_provider_config`); fallback-provider + credential-pool internals (SP09); the kanban
  multi-profile board + hooks + plugins (SP06b); per-platform delivery threading (SP11–13); auxiliary-model
  resolution for the goal judge (SP02). Each note links these rather than re-documenting them.
- **Collision (augment): the `delegate_task` subagent-spawn TOOL is NOT covered by any existing term** —
  the two `term_deleg*` hits (`term_delegated_identity`, `term_delegated_work`,
  both active) are unrelated abuse/auth concepts (classic LIKE false-positives). The owned
  `term_delegate_task` capture is NEW; `term_subagent` (active) is LINKED, not recreated.
- **Collision: no `term_goal`/`term_ralph*` exists** → owned `term_persistent_goal` is NEW.
- **Collision: no `term_execut*`/`term_code_exec*`/`term_rpc` term covers the `execute_code` RPC sandbox**
  (`term_rpc` is the generic protocol concept, LINKED not recreated) → owned `term_code_execution_tool` is NEW.
- **Collision: no `term_traject*`/`term_sharegpt` exists** → owned `term_agent_trajectory` is NEW.

## Source Pages (Measured 2026-06-15, from local mirror — `wc`)

| Page | Words | Code | Dominant BB | → Notes |
|------|------:|-----:|-------------|---------|
| user-guide/features/cron.md | 3861 | 37 | MIXED procedure+model | 2 (split) |
| user-guide/features/delegation.md | 2007 | 11 | procedure | 1 |
| user-guide/features/code-execution.md | 1661 | 10 | procedure | 1 |
| user-guide/features/goals.md | 1601 | 5 | procedure | 1 |
| user-guide/features/batch-processing.md | 1176 | 7 | model | 1 |

## Planned Notes (LOCKED)

All notes → `resources/documentation/hermes_agent/`, prefix `hermes_`. **6 notes.**

| # | Filename | BB | Source section(s) | ~Words | Description |
|---|----------|----|--------------------|-------:|-------------|
| 1 | `hermes_cron_scheduling.md` | procedure | cron §What cron can do now, §Creating scheduled tasks (/cron, CLI, NL), §Skill-backed cron jobs, §Running a job inside a project directory (`workdir`), §Editing jobs, §Lifecycle actions (+name-based lookup), §How it works (gateway scheduler), §Delivery options (+routing intent `all`, Telegram cron topic, response wrapping), §Self-contained prompts, §Security, §Schedule formats, §Repeat behavior, §Job storage | ~1400 | The `cronjob` lifecycle: create one-shot/recurring/NL jobs (`/cron`, `hermes cron`, plain chat), attach skills, set `workdir`, edit/pause/resume/run/remove by id-or-name, the 60s gateway-daemon scheduler tick, delivery targets (+`all` fan-out, Telegram cron topic, `wrap_response`), schedule formats (relative/interval/cron-expr/ISO), repeat semantics, `jobs.json` storage, prompt-injection scanning. |
| 2 | `hermes_cron_advanced_jobs.md` | model | cron §No-agent mode (script-only jobs), §Script timeout, §Skipping the agent entirely (`wakeAgent` + cheap pre-run gates: file-change / external-flag / SQL-count), §Chaining jobs with `context_from`, §Provider recovery, §Toolsets available to cron jobs (+`enabled_toolsets`), §Silent suppression (`[SILENT]`) | ~1300 | The cost-control + data-flow model around cron: `no_agent=True` script-only ticks, the `{"wakeAgent": false}` $0 pre-run gate (3 recipes), `context_from` job-chaining (collect→triage→ship), per-job `enabled_toolsets` to shrink the tool-schema prompt, fallback/credential-pool provider recovery, and `[SILENT]` delivery suppression for quiet monitors. |
| 3 | `hermes_subagent_delegation.md` | procedure | delegation §Single Task, §Parallel Batch, §How Subagent Context Works, §Practical Examples, §Batch Mode Details, §Model Override, §Toolset Selection Tips, §Max Iterations, §Child Timeout, §Monitoring (`/agents`), §Depth Limit and Nested Orchestration, §Lifetime and Durability, §Key Properties, §Delegation vs execute_code, §Configuration | ~1500 | The `delegate_task` tool: spawn isolated child AIAgents with fresh context + restricted toolsets, single vs parallel batch (default 3 concurrent via ThreadPoolExecutor), the "subagents know nothing" context-passing rule, blocked toolsets, max-iterations + child-timeout (default no wall-clock cap), `/agents` monitor, leaf-vs-orchestrator depth (`max_spawn_depth`), synchronous non-durable lifetime, and delegation-vs-execute_code decision rule. |
| 4 | `hermes_code_execution.md` | procedure | code-execution §How It Works, §When the Agent Uses This, §Practical Examples, §Execution Mode (project/strict), §Resource Limits, §How Tool Calls Work Inside Scripts, §Error Handling, §Security (env scrubbing, skill passthrough, `HERMES_*` vars), §execute_code vs terminal, §Platform Support | ~1400 | The `execute_code` tool: agent-authored Python that calls Hermes tools over a Unix-domain-socket RPC, collapsing multi-step workflows into one LLM turn (only `print()` returns to context). `project` vs `strict` mode, resource limits (300s / 50KB / 50 tool calls), the 7-tool RPC whitelist + recursion block, env-secret scrubbing + skill `required_environment_variables` passthrough + the four operational `HERMES_*` vars, execute_code-vs-terminal, Linux/macOS-only. |
| 5 | `hermes_persistent_goals.md` | procedure | goals §When to use it, §Quick start, §Commands, §Adding criteria mid-goal (`/subgoal`), §Behavior details (judge, fail-open, turn budget, preempt, mid-run safety, persistence, prompt cache), §Configuration (+choosing the judge model), §Example walkthrough, §When the judge gets it wrong, §Attribution | ~1300 | `/goal`: a standing objective that survives turns — after each turn an auxiliary judge model returns `{"done","reason"}`; on `continue` Hermes auto-feeds a continuation prompt until done / paused / 20-turn budget. Hermes' take on the Ralph loop: create/status/pause/resume/clear + `/subgoal` mid-loop criteria, conservative fail-open judge, `SessionDB.state_meta` persistence across `/resume`, prompt-cache-preserving continuation, cheap judge-model override. |
| 6 | `hermes_batch_processing.md` | model | batch-processing §Overview, §Quick Start, §Dataset Format, §Configuration Options (+Provider Routing, Reasoning Control, Advanced), §Toolset Distributions, §Output Format (+Trajectory Format), §Checkpointing (+How Resume Works), §Quality Filtering, §Statistics, §Use Cases | ~1100 | `batch_runner.py`: run the agent across thousands of JSONL prompts in parallel to produce **ShareGPT-format trajectory data** for fine-tuning/eval. The data model: dataset format (+per-prompt container `image`/`cwd`), `--num_workers` parallelism, independent per-toolset distribution sampling, the trajectory JSON schema (conversations + tool_stats + reasoning coverage), content-based resume checkpointing, no-reasoning/corrupted-entry quality filters, and aggregate statistics. |

**SP06a totals:** 6 notes · procedure 4 · model 2 · concept 0 (concepts owned by term notes — 4 owned by this SP, rest existing).
5 source pages digested (all substantive), 0 skipped.

## Summary Statistics & Building Block Distribution

- Notes: 6 · procedure 4 · model 2 · concept 0 (the 4 Hermes-specific concepts are owned term captures `term_persistent_goal`, `term_delegate_task`, `term_agent_trajectory`, `term_code_execution_tool`).
- Source: 5 digested pages (~10.3K words) → ~8.0K words of notes (modest compression via link-outs to SP02 config / SP09 providers / SP06b kanban+hooks).
- BB mix: procedure 67%, model 33%.
- Owned term captures: 4 (all NEW, DB-confirmed absent 2026-06-15). Existing terms linked: term_cron, term_cron_expression, term_subagent, term_multi_agent_systems, term_agent_orchestration, term_autonomous_coding_agents (+ broader verified pool below).

## Section Coverage Map

```
cron.md (3861w)
├── What cron can do now / Creating scheduled tasks (/cron, CLI, NL) ── → Note 1
├── Skill-backed cron jobs (single / multiple) ──────────────────────── → Note 1 (skills→SP05)
├── Running a job inside a project directory (workdir, serialization) ─ → Note 1
├── Editing jobs / Lifecycle actions (+name-based lookup) ───────────── → Note 1
├── How it works (gateway scheduler tick, jobs.json load) ──────────── → Note 1 (gateway internals→SP18)
├── Delivery options (+routing intent `all`, Telegram cron topic, wrapping) → Note 1 (per-platform→SP11-13)
├── Self-contained prompts / Security / Schedule formats / Repeat / Job storage → Note 1
├── No-agent mode (script-only jobs) / Script timeout ──────────────── → Note 2
├── Skipping the agent (`wakeAgent` + file/flag/SQL pre-run gates) ──── → Note 2
├── Chaining jobs with `context_from` (collect→triage→ship) ────────── → Note 2
├── Provider recovery (fallback + credential pool rotation) ────────── → Note 2 (fallback/pools→SP09)
├── Toolsets available to cron jobs (+`enabled_toolsets`) ──────────── → Note 2 (tools UI→SP05)
└── Silent suppression (`[SILENT]`) ───────────────────────────────── → Note 2 (silence-token concept→SP11 [own])
delegation.md (2007w) ── ALL sections ────────────────────────────────── → Note 3 (config block→SP02; execute_code→Note 4; cron durable→Note 1)
code-execution.md (1661w) ── ALL sections ────────────────────────────── → Note 4 (security passthrough→SP03; config mode→SP02; delegation→Note 3)
goals.md (1601w) ── ALL sections ─────────────────────────────────────── → Note 5 (auxiliary judge model→SP02; config→SP02)
batch-processing.md (1176w) ── ALL sections ──────────────────────────── → Note 6 (Nous Portal→SP14; backends docker/modal/singularity→SP02/SP03)
```

No source H2/H3 orphaned. All 5 pages fully covered; feature-overlap detail intentionally routed to owning SPs as link-outs.

## Split Decisions

| Original | Split into | Rationale |
|----------|-----------|-----------|
| cron.md (3861w, 37 code) | Note 1 `hermes_cron_scheduling` (procedure: lifecycle/create/edit/deliver/schedule) + Note 2 `hermes_cron_advanced_jobs` (model: no-agent/wakeAgent-gates/context_from/toolset-budget/provider-recovery/[SILENT]) | >2500w AND BB-mixing — a step-by-step job-management procedure vs the cost-control + data-flow model around gating/chaining/recovery. Each half keeps ≤6 curated code blocks (37 source blocks → curate load-bearing examples). |

The other four pages (delegation 2007w, code-execution 1661w, goals 1601w, batch-processing 1176w) are each ≤2500w and single-BB → 1 note each, no split.

## Collision & Dedup Audit (Step 10.5f — generalized to ALL planned notes; searched term_dictionary AND documentation/)

| Planned note / owned slug | Synonym/LIKE hits found | Verdict | Action |
|---|---|---|---|
| owned `term_delegate_task` | `term_delegated_identity` (active), `term_delegated_work` (active) | **NOT a dup** — those are auth-delegation / work-delegation, unrelated to the subagent-spawn tool (LIKE false-positives) | CAPTURE new `term_delegate_task`; LINK `term_subagent` (active). |
| owned `term_persistent_goal` | none (`term_%goal%`, `term_%ralph%` → 0 rows) | **NOT a dup** — no goal/Ralph-loop term exists | CAPTURE new `term_persistent_goal`. |
| owned `term_code_execution_tool` | none (`term_%execut%`, `term_%code_exec%` → 0 rows); `term_rpc` (active) is the generic protocol | **NOT a dup** — no term covers the `execute_code` RPC sandbox | CAPTURE new `term_code_execution_tool`; LINK `term_rpc`, `term_sandbox`. |
| owned `term_agent_trajectory` | none (`term_%traject%`, `term_%sharegpt%` → 0 rows) | **NOT a dup** — no trajectory/ShareGPT term exists | CAPTURE new `term_agent_trajectory`; LINK `term_fine_tuning`, `term_synthetic_data`. |
| `hermes_cron_scheduling`, `hermes_cron_advanced_jobs` | `term_cron` (active), `term_cron_expression` (active) | **NOT a dup** — those are the generic concept; these are Hermes' user-facing `cronjob` procedure + model | CREATE; LINK both terms. |
| `hermes_subagent_delegation` | `term_subagent`, `term_multi_agent_systems`, `term_agent_orchestration` (active) | **NOT a dup** — component concepts the note uses | CREATE; LINK all three. |
| `hermes_code_execution`, `hermes_persistent_goals`, `hermes_batch_processing` | no substantive term/doc note covers these procedures; no `hermes_agent/` doc notes exist yet | NEW | CREATE. |

DB synonym scan run across `term_dictionary/` AND `documentation/` for each planned slug + each owned term-slug's keywords (2026-06-15); **0 substantive same-concept duplicates** — the 2 `term_deleg*` hits are confirmed unrelated by name+status, and the goal/exec/trajectory scans returned 0 rows. New `hermes_agent/` folder → no doc-doc collisions (intra-series links resolve at finalization).

## Per-Note Related Notes Mapping (FINALIZED — FOUR-FLOOR: ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc per note)

> **FOUR-FLOOR standard set 2026-06-19** (user directive — supersedes both the 2026-06-14 floor of ≥8 term + ≥8
> snippet + ≥5 doc AND the interim 2026-06-19 wording of ≥8 term + ≥5 code-repo + ≥10 doc with snippets as bonus):
> each note's `## Related Notes` carries **four counted, relevancy-selected groups** —
> SOURCE-CODE modules that implement what this doc documents),
> implementation-corpus code this note documents; **now a COUNTED floor, promoted from the prior "bonus" group and
> raised from 8 to ≥10**), and
> **≥10 documentation notes** (`../../documentation/`, sibling `hermes_*` in this series + analogous
> `claude_code/cc_*` agent-tool docs + other relevant existing doc notes)** —
> all relevancy-selected, each rendered as `- [Name](path.md) — what-it-is; relevance: why-it-matters-here`.
> finalization (G5/G8) and are allowed un-verified. The 4 owned terms (`term_persistent_goal`, `term_delegate_task`,
> `term_agent_trajectory`, `term_code_execution_tool`) and other-SP not-yet-existing terms are marked `[own]` in the
> `(+fin …)` list, **EXCLUDED from the ≥8 term floor** (they don't exist yet — captured this SP / by their owner,
> linked at finalization).

**Note 1 `hermes_cron_scheduling`** (procedure)
- Terms (8): [term_cron](../../term_dictionary/term_cron.md) — the scheduling concept; relevance: the `cronjob` tool wraps cron-style recurring/one-shot scheduling. [term_cron_expression](../../term_dictionary/term_cron_expression.md) — 5-field crontab syntax; relevance: one of the four accepted schedule formats (`0 9 * * 1-5`). [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — unattended agent class; relevance: cron runs a fresh `AIAgent` to completion with no human in the loop each tick. [term_agent_orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating agent runs; relevance: the 60s gateway scheduler orchestrates which due jobs fire each tick. [term_skill_manifest](../../term_dictionary/term_skill_manifest.md) — skill frontmatter; relevance: `--skill`/`skills=[...]` attach skill manifests that load before the prompt runs. [term_skills](../../term_dictionary/term_skills.md) — reusable workflow packs; relevance: skill-backed jobs inherit reusable workflows without inlining text. [term_idempotency](../../term_dictionary/term_idempotency.md) — repeatable side-effect-safe runs; relevance: atomic `jobs.json` writes + the `.tick.lock` file lock keep job batches from double-running. [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable session state; relevance: jobs persist in `~/.hermes/cron/jobs.json` and each run is a fresh isolated session. (+fin: term_messaging_gateway [own SP11], term_silence_token [own SP11])
- Code-Repos (5): [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — the cron scheduler/storage module; relevance: implements `jobs.json` load, `next_run_at` checks, the 60s tick, repeat/schedule parsing, and atomic job writes this page documents. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the tool layer; relevance: hosts the single `cronjob` action-style tool (create/list/edit/pause/resume/run/remove) the agent uses. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the standalone CLI; relevance: implements `hermes cron create/list/edit/...` and the in-chat `/cron` command surface. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — the gateway daemon + delivery adapters; relevance: the gateway ticks the scheduler and routes cron output to `origin`/`telegram`/`all`/etc. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `AIAgent` core; relevance: each due job starts a fresh `AIAgent` session, optionally injecting attached skills, and runs the prompt to completion.
- Docs (10): [hermes_cron_advanced_jobs](hermes_cron_advanced_jobs.md) — sibling SP06a note; relevance: the no-agent/`wakeAgent`/`context_from`/provider-recovery model that extends this lifecycle. [hermes_subagent_delegation](hermes_subagent_delegation.md) — sibling SP06a note; relevance: `cronjob` is the durable alternative to synchronous `delegate_task`. [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — sibling SP02 config note; relevance: holds the `cron:` config block (`wrap_response`, `script_timeout_seconds`) and skill settings. [hermes_config_files_precedence](hermes_config_files_precedence.md) — sibling SP02 config note; relevance: where `~/.hermes/config.yaml` cron keys and env-var override order resolve. [hermes_messaging_media_settings](hermes_messaging_media_settings.md) — sibling SP08a note; relevance: cron delivery routes through the messaging/media delivery layer (`TELEGRAM_CRON_THREAD_ID`, fan-out). [hermes_guide_automate_with_cron](hermes_guide_automate_with_cron.md) — sibling SP16 guide; relevance: the worked-example automation guide for this exact feature. [hermes_guide_cron_script_only](hermes_guide_cron_script_only.md) — sibling SP16 guide; relevance: the linked Script-Only Cron Jobs guide referenced in §No-agent mode. [hermes_gateway_operations](hermes_gateway_operations.md) — sibling SP18 note; relevance: `hermes gateway install`/foreground operation that runs the scheduler. [cc_desktop_scheduled_tasks](../claude_code/cc_desktop_scheduled_tasks.md) — Claude Code analogue; relevance: the closest external agent-tool scheduled-task feature for comparison. [cc_scheduled_task_execution_model](../claude_code/cc_scheduled_task_execution_model.md) — Claude Code analogue; relevance: analogous tick/fresh-session scheduled-execution model.
- Snippets (11): [snippet_hermes_agent_cli_cron](../../code_snippets/snippet_hermes_agent_cli_cron.md) — the `hermes cron`/`/cron` CLI surface; relevance: implements `create/list/edit/pause/resume/run/remove` and the positional schedule+prompt parsing this page documents. [snippet_hermes_agent_cron_job_crud](../../code_snippets/snippet_hermes_agent_cron_job_crud.md) — job create/update/delete; relevance: the `jobs.json` mutation operations behind every lifecycle verb. [snippet_hermes_agent_cron_job_schema](../../code_snippets/snippet_hermes_agent_cron_job_schema.md) — the persisted job record; relevance: defines `schedule`/`prompt`/`skills`/`workdir`/`deliver`/`repeat`/`model`/`provider` fields stored per job. [snippet_hermes_agent_cron_job_validate](../../code_snippets/snippet_hermes_agent_cron_job_validate.md) — create/update validation; relevance: enforces the absolute-existing-`workdir` rule and rejects malformed schedules at create/update time. [snippet_hermes_agent_cron_tick](../../code_snippets/snippet_hermes_agent_cron_tick.md) — the 60s scheduler tick; relevance: loads jobs, checks `next_run_at`, and the `.tick.lock` overlap guard this page's §How it works describes. [snippet_hermes_agent_cron_run_job_setup](../../code_snippets/snippet_hermes_agent_cron_run_job_setup.md) — fresh-session setup; relevance: starts a fresh `AIAgent` per due job and injects attached skills before the prompt runs. [snippet_hermes_agent_gw_runner_cron](../../code_snippets/snippet_hermes_agent_gw_runner_cron.md) — the gateway cron runner; relevance: the gateway daemon hook that ticks the scheduler every 60s. [snippet_hermes_agent_tools_cronjob_register](../../code_snippets/snippet_hermes_agent_tools_cronjob_register.md) — `cronjob`-tool registration; relevance: registers the single action-style `cronjob` tool the agent uses to create/edit jobs in chat. [snippet_hermes_agent_tools_cronjob_handoff](../../code_snippets/snippet_hermes_agent_tools_cronjob_handoff.md) — tool→scheduler handoff; relevance: routes the agent's `cronjob(...)` call into the scheduler store. [snippet_hermes_agent_cron_helpers](../../code_snippets/snippet_hermes_agent_cron_helpers.md) — schedule/name-lookup helpers; relevance: parses relative/interval/cron-expr/ISO formats and the case-insensitive name-or-ID resolution. [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery; relevance: routes the final response to `origin`/`local`/`telegram`/`all`/etc. and applies `wrap_response`.

**Note 2 `hermes_cron_advanced_jobs`** (model)
- Terms (8): [term_cron](../../term_dictionary/term_cron.md) — the scheduling concept; relevance: these advanced features are per-tick behaviors of cron jobs. [term_failover](../../term_dictionary/term_failover.md) — switching to a backup on error; relevance: §Provider recovery falls back to an alternate provider when the primary is rate-limited/errors. [term_round_robin](../../term_dictionary/term_round_robin.md) — cyclic rotation; relevance: credential-pool rotation cycles to the next key for the same provider. [term_rate_limiting](../../term_dictionary/term_rate_limiting.md) — request throttling; relevance: provider recovery exists precisely so a single rate-limited key won't fail a high-frequency run. [term_idempotency](../../term_dictionary/term_idempotency.md) — side-effect-safe repeats; relevance: the file/flag/SQL `wakeAgent` gates make polls safe to re-run at $0 when state is unchanged. [term_etl](../../term_dictionary/term_etl.md) — extract-transform-load staging; relevance: `context_from` chaining models a collect→triage→ship ETL pipeline across isolated jobs. [term_fault_tolerance](../../term_dictionary/term_fault_tolerance.md) — graceful failure handling; relevance: no-agent error alerts + provider recovery keep a broken watchdog/run from failing silently. [term_data_pipeline](../../term_dictionary/term_data_pipeline.md) — staged multi-step data flow; relevance: the fan-out/fan-in `context_from` chains are an explicit cron data pipeline. (+fin: term_fallback_provider [own SP09], term_credential_pool [own SP09], term_silence_token [own SP11])
- Code-Repos (5): [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — the cron module; relevance: implements `no_agent` script-only ticks, the `wakeAgent` JSON gate, `context_from` output injection, `enabled_toolsets`, and `[SILENT]` suppression. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider/credential layer; relevance: implements the fallback-provider + credential-pool rotation that cron jobs inherit for recovery. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `AIAgent` core; relevance: hosts the toolset-schema assembly that `enabled_toolsets` shrinks for cost control and the error classification that triggers recovery. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway + delivery; relevance: enforces the silent-tick / `[SILENT]` delivery suppression and verbatim no-agent stdout delivery. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the tool layer; relevance: the `cronjob` tool schema exposes `no_agent`, `script`, `context_from`, and `enabled_toolsets` to the agent.
- Docs (10): [hermes_cron_scheduling](hermes_cron_scheduling.md) — sibling SP06a note; relevance: the base cron lifecycle these advanced behaviors extend. [hermes_subagent_delegation](hermes_subagent_delegation.md) — sibling SP06a note; relevance: a hard `child_timeout` is recommended for unattended cron-driven delegation. [hermes_code_execution](hermes_code_execution.md) — sibling SP06a note; relevance: pre-run gate scripts share the `~/.hermes/scripts/` sandboxing rule with the code-exec sandbox. [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) — sibling SP02 config note; relevance: `fallback_providers`/`fallback_model` config the recovery path reads. [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — sibling SP02 config note; relevance: the `cron:` config block (`script_timeout_seconds`) and toolset settings live here. [hermes_fallback_providers](hermes_fallback_providers.md) — sibling SP09 note; relevance: concept home for the fallback-provider chain cron inherits. [hermes_credential_pools](hermes_credential_pools.md) — sibling SP09 note; relevance: concept home for the credential-pool rotation strategy cron inherits. [hermes_guide_cron_troubleshooting](hermes_guide_cron_troubleshooting.md) — sibling SP16 guide; relevance: operational guide for diagnosing gated/failing cron jobs. [cc_loop_scheduled_tasks](../claude_code/cc_loop_scheduled_tasks.md) — Claude Code analogue; relevance: analogous recurring-task gating/scheduling model. [cc_fallback_models](../claude_code/cc_fallback_models.md) — Claude Code analogue; relevance: the closest external analogue to provider-recovery fallback.
- Snippets (11): [snippet_hermes_agent_cron_run_job_execute](../../code_snippets/snippet_hermes_agent_cron_run_job_execute.md) — the per-tick job execution path; relevance: runs `no_agent` script-only ticks, evaluates the `{"wakeAgent": false}` gate, and prepends `context_from` outputs. [snippet_hermes_agent_cron_helpers](../../code_snippets/snippet_hermes_agent_cron_helpers.md) — cron helpers; relevance: the script-timeout resolution (`HERMES_CRON_SCRIPT_TIMEOUT`→config→120s) and `~/.hermes/scripts/` sandboxing rule. [snippet_hermes_agent_cron_job_state](../../code_snippets/snippet_hermes_agent_cron_job_state.md) — per-job run state; relevance: records `last_run_at` the file-change `wakeAgent` gate compares against and stores most-recent output for `context_from`. [snippet_hermes_agent_gw_delivery](../../code_snippets/snippet_hermes_agent_gw_delivery.md) — gateway delivery; relevance: enforces `[SILENT]` suppression, the empty-stdout silent tick, and verbatim no-agent stdout delivery. [snippet_hermes_agent_core_credential_pool_selection](../../code_snippets/snippet_hermes_agent_core_credential_pool_selection.md) — credential-pool selection; relevance: the next-key rotation cron jobs inherit when a key is rate-limited. [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential sourcing; relevance: assembles the per-provider key pool that provider recovery rotates through. [snippet_hermes_agent_core_chat_helpers_activate_fallback](../../code_snippets/snippet_hermes_agent_core_chat_helpers_activate_fallback.md) — fallback activation; relevance: switches to `fallback_providers`/`fallback_model` when the primary errors — the recovery path cron inherits. [snippet_hermes_agent_core_error_classifier_taxonomy](../../code_snippets/snippet_hermes_agent_core_error_classifier_taxonomy.md) — error taxonomy; relevance: classifies provider errors (rate-limit vs fatal) that decide whether to rotate/fall back. [snippet_hermes_agent_core_error_classifier_backoff](../../code_snippets/snippet_hermes_agent_core_error_classifier_backoff.md) — retry backoff; relevance: the backoff schedule between recovery attempts on a high-frequency cron run. [snippet_hermes_agent_core_error_classifier_provider_maps](../../code_snippets/snippet_hermes_agent_core_error_classifier_provider_maps.md) — per-provider error maps; relevance: maps raw provider error shapes to the taxonomy that triggers recovery. [snippet_hermes_agent_gw_runner_errors](../../code_snippets/snippet_hermes_agent_gw_runner_errors.md) — gateway error alerts; relevance: emits the error-alert delivery for non-zero-exit/timeout no-agent jobs so a broken watchdog can't fail silently.

**Note 3 `hermes_subagent_delegation`** (procedure)
- Terms (8): [term_subagent](../../term_dictionary/term_subagent.md) — child agent entity; relevance: `delegate_task` spawns isolated child `AIAgent` subagents with fresh context and their own terminal sessions. [term_multi_agent_systems](../../term_dictionary/term_multi_agent_systems.md) — coordinating multiple agents; relevance: parallel batch delegation is a multi-agent fan-out (up to 3 concurrent by default). [term_agent_orchestration](../../term_dictionary/term_agent_orchestration.md) — orchestrating sub-tasks; relevance: `role="orchestrator"` children can themselves delegate, forming nested orchestration trees bounded by `max_spawn_depth`. [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — unattended task agents; relevance: each subagent works independently to completion under its iteration budget. [term_context_window](../../term_dictionary/term_context_window.md) — bounded LLM context; relevance: only the child's final summary re-enters the parent context, keeping token usage efficient. [term_function_calling](../../term_dictionary/term_function_calling.md) — tool-call iteration; relevance: `max_iterations` (default 50) caps how many tool-calling turns a child takes. [term_failover](../../term_dictionary/term_failover.md) — backup on error; relevance: children inherit the parent's credential pool, enabling key rotation on rate limits. [term_human_in_the_loop](../../term_dictionary/term_human_in_the_loop.md) — user-in-loop control; relevance: the `clarify` toolset is blocked for subagents — leaves cannot interact with the user. (+fin: term_delegate_task [own this SP], term_code_execution_tool [own this SP])
- Code-Repos (5): [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the tool layer; relevance: implements the `delegate_task` tool — single vs `tasks=[...]` batch, `toolsets`/`role`/`max_iterations`/`child_timeout_seconds`, and the blocked-toolset list. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `AIAgent` core + orchestrator; relevance: builds the child's focused system prompt, runs the isolated conversation, the `ThreadPoolExecutor` concurrency pool, and result-ordering by task index. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider/credential layer; relevance: children inherit the parent's API key, provider config, and credential pool for rate-limit rotation. [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — TUI + gateway; relevance: implements the `/agents` (`/tasks`) overlay live tree, per-branch cost/token rollups, and kill/pause controls. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the CLI; relevance: renders the CLI tree-view progress display and per-task completion lines for running subagents.
- Docs (10): [hermes_code_execution](hermes_code_execution.md) — sibling SP06a note; relevance: the §Delegation vs execute_code decision boundary (reasoning vs mechanical). [hermes_cron_scheduling](hermes_cron_scheduling.md) — sibling SP06a note; relevance: `cronjob` is the durable alternative for work that must outlive the synchronous parent turn. [hermes_cron_advanced_jobs](hermes_cron_advanced_jobs.md) — sibling SP06a note; relevance: `child_timeout_seconds` is recommended for cost control on unattended cron-driven delegation. [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — sibling SP02 config note; relevance: holds the `delegation:` config block (`max_iterations`, `max_concurrent_children`, `max_spawn_depth`, model/provider override). [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling SP02 config note; relevance: child timeout / heartbeat-staleness / interrupt-propagation runtime behavior. [hermes_guide_delegation_patterns](hermes_guide_delegation_patterns.md) — sibling SP16 guide; relevance: worked delegation-pattern recipes (parallel research, review-and-fix). [hermes_agent_loop](hermes_agent_loop.md) — sibling SP18 note; relevance: the per-turn agent loop each subagent runs to completion. [cc_subagents_overview](../claude_code/cc_subagents_overview.md) — Claude Code analogue; relevance: the closest external subagent concept for comparison. [cc_orchestrate_agent_teams](../claude_code/cc_orchestrate_agent_teams.md) — Claude Code analogue; relevance: analogous orchestrator/leaf multi-agent fan-out. [cc_run_agents_in_parallel](../claude_code/cc_run_agents_in_parallel.md) — Claude Code analogue; relevance: analogous parallel-batch concurrency model.
- Snippets (10): [snippet_hermes_agent_tools_delegate_spawn](../../code_snippets/snippet_hermes_agent_tools_delegate_spawn.md) — the `delegate_task` spawn path; relevance: implements single vs `tasks=[...]` batch, the blocked-toolset list, `max_iterations`/`child_timeout_seconds`, and own-terminal-per-child. [snippet_hermes_agent_tools_delegate_prompt](../../code_snippets/snippet_hermes_agent_tools_delegate_prompt.md) — child prompt build; relevance: builds the focused system prompt from `goal`+`context` and the structured-summary instruction. [snippet_hermes_agent_tools_delegate_aggregate](../../code_snippets/snippet_hermes_agent_tools_delegate_aggregate.md) — result aggregation; relevance: sorts results by task index to match input order and returns only each child's final summary to the parent. [snippet_hermes_agent_tools_delegate_anti_recursion](../../code_snippets/snippet_hermes_agent_tools_delegate_anti_recursion.md) — depth/recursion guard; relevance: enforces leaf-vs-orchestrator roles and `max_spawn_depth` so leaves cannot delegate further. [snippet_hermes_agent_core_aiagent_orchestrator](../../code_snippets/snippet_hermes_agent_core_aiagent_orchestrator.md) — the orchestrator core; relevance: runs each child's isolated `AIAgent` conversation and the nested-orchestration tree. [snippet_hermes_agent_core_chat_helpers_streaming_delegates](../../code_snippets/snippet_hermes_agent_core_chat_helpers_streaming_delegates.md) — delegate progress streaming; relevance: relays per-subagent tool-call progress to the parent's callback (the `/agents` tree feed). [snippet_hermes_agent_core_chat_helpers_max_iter](../../code_snippets/snippet_hermes_agent_core_chat_helpers_max_iter.md) — iteration budget; relevance: caps each child at `max_iterations` (default 50) tool-calling turns. [snippet_hermes_agent_core_tool_executor_concurrent](../../code_snippets/snippet_hermes_agent_core_tool_executor_concurrent.md) — concurrent executor; relevance: the `ThreadPoolExecutor` pool that runs up to `max_concurrent_children` (default 3) in parallel. [snippet_hermes_agent_core_tool_executor_sequential](../../code_snippets/snippet_hermes_agent_core_tool_executor_sequential.md) — sequential executor; relevance: the single-task delegation path that runs directly without thread-pool overhead. [snippet_hermes_agent_core_credential_pool_selection](../../code_snippets/snippet_hermes_agent_core_credential_pool_selection.md) — credential-pool selection; relevance: children inherit the parent's credential pool for key rotation on rate limits.

**Note 4 `hermes_code_execution`** (procedure)
- Terms (8): [term_rpc](../../term_dictionary/term_rpc.md) — remote-procedure-call protocol; relevance: script tool calls travel over a Unix-domain-socket RPC to the parent's `handle_function_call` and back. [term_sandbox](../../term_dictionary/term_sandbox.md) — isolated execution environment; relevance: the script runs in a child process with a minimal scrubbed environment in `project`/`strict` modes. [term_function_calling](../../term_dictionary/term_function_calling.md) — programmatic tool invocation; relevance: `execute_code` is programmatic tool-calling that collapses multi-step tool workflows into one LLM turn. [term_prompt_injection](../../term_dictionary/term_prompt_injection.md) — adversarial prompt attacks; relevance: the 7-tool whitelist + secret-stripping defend against injection-driven tool/secret abuse. [term_pii](../../term_dictionary/term_pii.md) — sensitive identifiers; relevance: env vars matching KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL/AUTH are stripped to prevent leaking secrets to arbitrary code. [term_content_exfiltration](../../term_dictionary/term_content_exfiltration.md) — unauthorized data egress; relevance: stripping credentials + blocking recursion/`delegate_task`/MCP/`send_message` defends against exfiltration via agent-authored code. [term_context_window](../../term_dictionary/term_context_window.md) — bounded LLM context; relevance: only `print()` output returns — intermediate tool results never enter the context window. [term_idempotency](../../term_dictionary/term_idempotency.md) — repeatable safe runs; relevance: temp staging dir + process-group kill ensure clean, repeatable execution on timeout/interrupt. (+fin: term_code_execution_tool [own this SP], term_delegate_task [own this SP])
- Code-Repos (5): [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the tool layer; relevance: implements the `execute_code` tool, the `hermes_tools.py` RPC stub generation, the 7-tool whitelist, and the recursion/`delegate_task`/MCP block. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `AIAgent` core; relevance: hosts `handle_function_call` (the RPC dispatch target), env-secret scrubbing, resource limits (timeout/stdout/tool-call caps), and the `project`/`strict` interpreter resolver. [repo_hermes_agent_skills](../../../areas/code_repos/repo_hermes_agent_skills.md) — the skills system; relevance: implements `required_environment_variables` passthrough from skill frontmatter into the child process. [repo_hermes_agent_mcp_toolsets](../../../areas/code_repos/repo_hermes_agent_mcp_toolsets.md) — MCP/toolset registry; relevance: defines which tools exist and why MCP tools are excluded from the in-script RPC whitelist. [repo_hermes_agent_cron](../../../areas/code_repos/repo_hermes_agent_cron.md) — the cron module; relevance: cron jobs with `workdir` set make `execute_code` (and terminal/file tools) run from that directory.
- Docs (10): [hermes_subagent_delegation](hermes_subagent_delegation.md) — sibling SP06a note; relevance: the §execute_code vs delegate_task boundary (mechanical vs reasoning). [hermes_security_skill_memory_settings](hermes_security_skill_memory_settings.md) — sibling SP02 config note; relevance: holds the `code_execution:` block (`mode`, `timeout`, `max_tool_calls`) and `terminal.env_passthrough` allowlist. [hermes_security_isolation_credentials](hermes_security_isolation_credentials.md) — sibling SP03 security note; relevance: concept home for env-var passthrough and the secret-stripping security guarantee. [hermes_terminal_backends](hermes_terminal_backends.md) — sibling SP02/SP08 note; relevance: §execute_code vs terminal — when to use each, shared working directory. [hermes_cron_advanced_jobs](hermes_cron_advanced_jobs.md) — sibling SP06a note; relevance: pre-run gate scripts share the `~/.hermes/scripts/` sandboxing rule. [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling SP02 config note; relevance: the operational `HERMES_*` vars (`HERMES_HOME`/`PROFILE`/`CONFIG`/`ENV`) the child receives. [hermes_agent_tools](hermes_agent_tools.md) — sibling repo-doc note; relevance: the broader tool catalog `execute_code` belongs to. [cc_execution_tool_behavior](../claude_code/cc_execution_tool_behavior.md) — Claude Code analogue; relevance: analogous code-execution tool behavior. [cc_sandbox_modes](../claude_code/cc_sandbox_modes.md) — Claude Code analogue; relevance: analogous project-vs-strict sandbox-mode model. [cc_prompt_injection_defenses](../claude_code/cc_prompt_injection_defenses.md) — Claude Code analogue; relevance: analogous secret-scrubbing / injection-defense posture for executed code.
- Snippets (10): [snippet_hermes_agent_tools_code_exec_sandbox](../../code_snippets/snippet_hermes_agent_tools_code_exec_sandbox.md) — the `execute_code` sandbox; relevance: implements the child-process Unix-socket RPC, env-secret scrubbing, the temp staging dir, and process-group kill on timeout. [snippet_hermes_agent_tools_code_exec_languages](../../code_snippets/snippet_hermes_agent_tools_code_exec_languages.md) — interpreter selection; relevance: the `project`/`strict` interpreter resolver (`VIRTUAL_ENV`/`CONDA_PREFIX` vs `sys.executable`) this page's §Execution Mode describes. [snippet_hermes_agent_tools_code_exec_result](../../code_snippets/snippet_hermes_agent_tools_code_exec_result.md) — result handling; relevance: returns only `print()` output plus `status`/`tool_calls_made`/`duration_seconds`, applying the 50KB stdout cap. [snippet_hermes_agent_core_redact_patterns](../../code_snippets/snippet_hermes_agent_core_redact_patterns.md) — secret-redaction patterns; relevance: the KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL/AUTH name match that strips env vars from the child. [snippet_hermes_agent_core_tool_guardrails_schema](../../code_snippets/snippet_hermes_agent_core_tool_guardrails_schema.md) — tool guardrails; relevance: the 7-tool RPC whitelist and the recursion/`delegate_task`/MCP/`send_message` block. [snippet_hermes_agent_core_file_safety](../../code_snippets/snippet_hermes_agent_core_file_safety.md) — file-access safety; relevance: bounds the read/write/patch file tools the in-script RPC can reach. [snippet_hermes_agent_core_message_sanitization](../../code_snippets/snippet_hermes_agent_core_message_sanitization.md) — message sanitization; relevance: scrubs script output before it re-enters the LLM context. [snippet_hermes_agent_tools_file_operations_a](../../code_snippets/snippet_hermes_agent_tools_file_operations_a.md) — RPC file ops; relevance: the `read_file`/`write_file`/`search_files`/`patch` tools reachable from inside the script. [snippet_hermes_agent_core_credential_sources](../../code_snippets/snippet_hermes_agent_core_credential_sources.md) — credential sourcing; relevance: the provider credentials deliberately NOT passed into the scrubbed child environment. [snippet_hermes_agent_tools_schema_sanitizer](../../code_snippets/snippet_hermes_agent_tools_schema_sanitizer.md) — tool-schema sanitizer; relevance: shapes the `hermes_tools.py` RPC stub's exposed function surface.

**Note 5 `hermes_persistent_goals`** (procedure)
- Terms (8): [term_llm_as_a_judge](../../term_dictionary/term_llm_as_a_judge.md) — model-as-evaluator pattern; relevance: after every turn an auxiliary judge model returns strict JSON `{"done","reason"}` deciding whether to continue. [term_self_evolving_agent](../../term_dictionary/term_self_evolving_agent.md) — self-directed iteration; relevance: `/goal` keeps the agent iterating on its own objective without per-turn re-prompting. [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — unattended task agents; relevance: the loop auto-feeds a continuation prompt until done/paused/budget — the agent drives itself. [term_session_persistence](../../term_dictionary/term_session_persistence.md) — durable session state; relevance: goal + subgoal state lives in `SessionDB.state_meta` keyed by `goal:<session_id>`, surviving `/resume`. [term_prompt_caching](../../term_dictionary/term_prompt_caching.md) — KV-cache reuse; relevance: the continuation is a plain user-role append that does not invalidate the prompt cache — 20-turn goals cost the same cache-wise as 20 normal turns. [term_human_in_the_loop](../../term_dictionary/term_human_in_the_loop.md) — user-in-loop control; relevance: any real user message always preempts the continuation loop, and the turn budget backstops a runaway loop. [term_agent_harness](../../term_dictionary/term_agent_harness.md) — agent runtime scaffold; relevance: the central `CommandDef` registry + adapter-FIFO continuation is the harness wiring for the loop. [term_agentic_ai](../../term_dictionary/term_agentic_ai.md) — goal-directed AI; relevance: this is Hermes' take on the Ralph-loop agentic pattern (keep a goal alive across turns). (+fin: term_persistent_goal [own this SP], term_provider_routing [own SP09])
- Code-Repos (5): [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `AIAgent` core; relevance: implements the per-turn goal judge call, the continuation-prompt append, fail-open verdict handling, the turn budget, and mid-run preempt. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the CLI; relevance: implements `/goal` and `/subgoal` command parsing, the `⊙`/`↻`/`✓`/`⏸` status lines, and `_pending_input` preempt ordering. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider/aux-model layer; relevance: resolves the `goal_judge` auxiliary task to the main model or a cheap override provider/model. [repo_hermes_agent_gateway_messaging](../../../areas/code_repos/repo_hermes_agent_gateway_messaging.md) — gateway + adapters; relevance: the adapter-FIFO continuation that runs `/goal` identically across Telegram/Discord/Slack/etc., and hosts the `SessionDB.state_meta` persistence backing goal/subgoal survival across `/resume`. [repo_hermes_agent_tui_gateway](../../../areas/code_repos/repo_hermes_agent_tui_gateway.md) — TUI + gateway; relevance: renders the `⊙ Goal set` / `↻ Continuing toward goal` / `✓ Goal achieved` / `⏸ Goal paused` status lines as the loop fires.
- Docs (10): [hermes_cron_scheduling](hermes_cron_scheduling.md) — sibling SP06a note; relevance: a contrasting unattended-execution surface (scheduled vs in-session standing goal). [hermes_subagent_delegation](hermes_subagent_delegation.md) — sibling SP06a note; relevance: another fan-out mechanism a goal turn may invoke. [hermes_session_search_storage](hermes_session_search_storage.md) — sibling SP05 note; relevance: the `SessionDB` storage layer that holds `state_meta` goal state. [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) — sibling SP02 config note; relevance: the `auxiliary.goal_judge` model override and Auxiliary Models resolution. [hermes_runtime_context_settings](hermes_runtime_context_settings.md) — sibling SP02 config note; relevance: `goals.max_turns` budget and continuation runtime behavior. [hermes_guide_automate_with_cron](hermes_guide_automate_with_cron.md) — sibling SP16 guide; relevance: companion automation guide for unattended iterative work. [hermes_agent_loop](hermes_agent_loop.md) — sibling SP18 note; relevance: the per-turn loop the goal judge gates after each turn. [cc_goal_command](../claude_code/cc_goal_command.md) — Claude Code analogue; relevance: the closest external `/goal` standing-objective command. [cc_verification_loop](../claude_code/cc_verification_loop.md) — Claude Code analogue; relevance: analogous iterate-until-verified loop pattern. [cc_agentic_loop](../claude_code/cc_agentic_loop.md) — Claude Code analogue; relevance: analogous agentic continuation-loop model.
- Snippets (10): [snippet_hermes_agent_cli_goals](../../code_snippets/snippet_hermes_agent_cli_goals.md) — `/goal` + `/subgoal` commands; relevance: implements set/status/pause/resume/clear, the `⊙`/`↻`/`✓`/`⏸` status lines, and `_pending_input` preempt ordering. [snippet_hermes_agent_core_auxiliary_auth_resolution](../../code_snippets/snippet_hermes_agent_core_auxiliary_auth_resolution.md) — auxiliary-model resolution; relevance: resolves the `goal_judge` task to the main model or a cheap override provider/model. [snippet_hermes_agent_core_hermes_state](../../code_snippets/snippet_hermes_agent_core_hermes_state.md) — `SessionDB` state layer; relevance: the `state_meta` store keyed by `goal:<session_id>` that survives `/resume`. [snippet_hermes_agent_core_hermes_state_schema](../../code_snippets/snippet_hermes_agent_core_hermes_state_schema.md) — state schema; relevance: defines the goal/subgoal record shape persisted alongside the session. [snippet_hermes_agent_core_hermes_state_writes](../../code_snippets/snippet_hermes_agent_core_hermes_state_writes.md) — state writes; relevance: persists goal/subgoal updates each turn so the loop survives a restart. [snippet_hermes_agent_core_conversation_loop_main_loop_entry](../../code_snippets/snippet_hermes_agent_core_conversation_loop_main_loop_entry.md) — per-turn loop entry; relevance: the turn the goal judge gates after each completion. [snippet_hermes_agent_core_conversation_loop_session_persist](../../code_snippets/snippet_hermes_agent_core_conversation_loop_session_persist.md) — session persist; relevance: writes session/goal state at the end of each turn for `/resume`. [snippet_hermes_agent_core_run_agent_cli](../../code_snippets/snippet_hermes_agent_core_run_agent_cli.md) — CLI run-agent; relevance: feeds the continuation prompt back as a plain user-role append (prompt-cache-preserving) when the judge says `continue`. [snippet_hermes_agent_core_auxiliary_pool_content](../../code_snippets/snippet_hermes_agent_core_auxiliary_pool_content.md) — auxiliary client pool; relevance: the small per-turn judge call (~200 tokens) routes through the aux-client pool. [snippet_hermes_agent_core_auxiliary_diagnostics](../../code_snippets/snippet_hermes_agent_core_auxiliary_diagnostics.md) — auxiliary diagnostics; relevance: surfaces aux-client errors so the fail-open `continue` verdict can be diagnosed.

**Note 6 `hermes_batch_processing`** (model)
- Terms (8): [term_fine_tuning](../../term_dictionary/term_fine_tuning.md) — supervised model adaptation; relevance: batch generation's primary purpose is producing ShareGPT trajectories for fine-tuning. [term_synthetic_data](../../term_dictionary/term_synthetic_data.md) — model-generated training data; relevance: the agent runs over thousands of prompts to synthesize tool-use trajectory data. [term_huggingface](../../term_dictionary/term_huggingface.md) — HF dataset/model ecosystem; relevance: tool stats are normalized to a consistent schema for HuggingFace datasets compatibility. [term_evaluation_harness](../../term_dictionary/term_evaluation_harness.md) — standardized eval runner; relevance: the Model Evaluation use case runs a fixed eval suite to measure tool-use quality. [term_few_shot_learning](../../term_dictionary/term_few_shot_learning.md) — in-context priming; relevance: `--prefill_messages_file` supplies few-shot prefill messages priming each run. [term_function_calling](../../term_dictionary/term_function_calling.md) — tool-call iteration; relevance: each trajectory captures tool_calls + `tool_stats` (count/success/failure) per tool. [term_dag](../../term_dictionary/term_dag.md) — directed acyclic flow; relevance: the scan→filter→re-batch→process→merge resume flow is a collect→process DAG. [term_fault_tolerance](../../term_dictionary/term_fault_tolerance.md) — graceful failure recovery; relevance: content-based checkpoint resume re-tries only failed prompts even if dataset order changes. (+fin: term_agent_trajectory [own this SP], term_nous_portal [own SP14])
- Code-Repos (5): [repo_hermes_agent_trajectory_research](../../../areas/code_repos/repo_hermes_agent_trajectory_research.md) — the trajectory/batch module; relevance: implements `batch_runner.py` — JSONL ingest, `--num_workers` parallelism, the ShareGPT trajectory schema, checkpointing/resume, quality filtering, and statistics this page documents. [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — the `AIAgent` core; relevance: each prompt runs through a full isolated agent session (`--max_turns` tool-calling iterations) producing the conversation trace. [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — the tool layer; relevance: toolset-distribution sampling draws from the registered toolsets, and tool_stats/tool_error_counts come from this layer. [repo_hermes_agent_providers_adapters](../../../areas/code_repos/repo_hermes_agent_providers_adapters.md) — provider/routing layer; relevance: implements `--model`/`--base_url`/OpenRouter provider-routing (`--providers_allowed/ignored/order/sort`) and reasoning-effort control. [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — the CLI; relevance: parses the `python batch_runner.py` flag surface (`--dataset_file`, `--batch_size`, `--run_name`, `--resume`, `--list_distributions`).
- Docs (10): [hermes_subagent_delegation](hermes_subagent_delegation.md) — sibling SP06a note; relevance: another parallel-fan-out execution mechanism (in-turn vs offline batch). [hermes_cron_advanced_jobs](hermes_cron_advanced_jobs.md) — sibling SP06a note; relevance: shares the parallel-worker + fault-tolerant resume pattern. [hermes_code_execution](hermes_code_execution.md) — sibling SP06a note; relevance: batch trajectories capture tool-call sequences the same tool layer produces. [hermes_terminal_backends](hermes_terminal_backends.md) — sibling SP02/SP08 note; relevance: per-prompt `image`/`cwd` container backends (Docker/Modal/Singularity) for each prompt's sandbox. [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md) — sibling SP02 config note; relevance: model/provider/base_url selection the batch runner reuses. [hermes_nous_portal_subscription](hermes_nous_portal_subscription.md) — sibling SP14 note; relevance: the Predictable-cost-at-scale tip recommends a Nous Portal subscription for stable cost-per-trajectory. [hermes_session_search_storage](hermes_session_search_storage.md) — sibling SP05 note; relevance: per-prompt isolated sessions whose traces become the output. [cc_headless_examples](../claude_code/cc_headless_examples.md) — Claude Code analogue; relevance: analogous headless batch/automation invocation. [cc_automate_and_scale](../claude_code/cc_automate_and_scale.md) — Claude Code analogue; relevance: analogous run-at-scale automation pattern. [cc_checkpointing](../claude_code/cc_checkpointing.md) — Claude Code analogue; relevance: analogous checkpoint/resume fault-tolerance model.
- Snippets (10): [snippet_hermes_agent_batch_runner](../../code_snippets/snippet_hermes_agent_batch_runner.md) — the `batch_runner.py` entry; relevance: implements JSONL ingest, the `--num_workers` parallel run, and the `data/<run_name>/` output layout this page documents. [snippet_hermes_agent_batch_runner_queue](../../code_snippets/snippet_hermes_agent_batch_runner_queue.md) — the work queue; relevance: batches prompts and drives the content-based-resume scan→filter→re-batch flow. [snippet_hermes_agent_batch_runner_spawn](../../code_snippets/snippet_hermes_agent_batch_runner_spawn.md) — per-prompt worker spawn; relevance: launches each prompt's isolated agent session with its `image`/`cwd` container backend. [snippet_hermes_agent_batch_runner_aggregate](../../code_snippets/snippet_hermes_agent_batch_runner_aggregate.md) — result aggregation; relevance: merges all `batch_*.jsonl` into `trajectories.jsonl` and emits `statistics.json`. [snippet_hermes_agent_trajectory_schema](../../code_snippets/snippet_hermes_agent_trajectory_schema.md) — the trajectory JSON schema; relevance: defines the ShareGPT `conversations` + `tool_stats` + reasoning-coverage record this page specifies. [snippet_hermes_agent_trajectory_canonicalize](../../code_snippets/snippet_hermes_agent_trajectory_canonicalize.md) — schema canonicalization; relevance: normalizes tool stats to all-tools-with-zero-defaults for HuggingFace dataset compatibility. [snippet_hermes_agent_trajectory_redact_export](../../code_snippets/snippet_hermes_agent_trajectory_redact_export.md) — redacted export; relevance: strips the `--ephemeral_system_prompt` and secrets before writing trajectories. [snippet_hermes_agent_trajectory_overlap_suppression](../../code_snippets/snippet_hermes_agent_trajectory_overlap_suppression.md) — overlap/quality suppression; relevance: the no-reasoning + corrupted-entry (hallucinated-tool) quality filters applied at merge. [snippet_hermes_agent_toolset_distributions](../../code_snippets/snippet_hermes_agent_toolset_distributions.md) — toolset distributions; relevance: the independent per-toolset probability sampling (`--distribution`/`--list_distributions`) this page describes. [snippet_hermes_agent_trajectory_config_dataclasses](../../code_snippets/snippet_hermes_agent_trajectory_config_dataclasses.md) — batch/trajectory config dataclasses; relevance: the typed config behind the `batch_runner.py` flag surface (model/provider-routing/reasoning-effort).


## Density Re-Assessment (LOCKED — re-read confirmed 2026-06-15)

Re-read all 5 source pages from `inbox/hermes_agent_docs/user-guide/features/`; measured counts match the
Source Pages table (cron 3861, delegation 2007, code-execution 1661, goals 1601, batch-processing 1176 —
no >50% estimate misses). Per-note:

| Note | BB | ~Words | ~Code | Within caps? |
|------|----|-------:|------:|--------------|
| 1 cron-scheduling | procedure | 1400 | ≤6 (curate from cron lifecycle blocks; delivery table in prose) | ✓ |
| 2 cron-advanced-jobs | model | 1300 | ≤6 (curate from no-agent/wakeAgent/context_from blocks) | ✓ |
| 3 subagent-delegation | procedure | 1500 | ≤6 (curate from 11 delegate_task blocks; toolset table in prose) | ✓ |
| 4 code-execution | procedure | 1400 | ≤6 (curate from 10 execute_code blocks) | ✓ |
| 5 persistent-goals | procedure | 1300 | ≤5 (commands/judge config/walkthrough) | ✓ |
| 6 batch-processing | model | 1100 | ≤6 (curate from CLI + trajectory-JSON blocks) | ✓ |

No further splits needed — all 6 notes ≤2500w. The cron.md split (Note 1 + Note 2) keeps each half a single
topically-cohesive BB cluster ≤6 curated code blocks (37 source blocks → load-bearing examples kept verbatim,
the rest summarized in prose). If any note exceeds 350 lines during writing, STOP and split.

## Documentation-Note Authoring Spec (Step 10.6 — derived from `cc_*.md`, inherited from master)

Notes follow the master's Note Format Definition (derived from `resources/documentation/claude_code/cc_*.md`,
the closest sibling external-agent-docs folder — verified field order against `cc_admin_enforcement_controls.md`
and `cc_sandbox_modes.md`): YAML field order `tags → keywords → topics → language → date of note → status →
building_block → source_url → access_control_group`; body `# Title → ## Overview (opener leading with what it IS,
NOT ## Definition) → source-mirrored H2s → ## Related Notes (indexed markdown links, each
`- [Name](path.md) — what-it-is; relevance: …`; FOUR-FLOOR **≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc**, all counted) → footer
**Source** / **Last Updated** / **Status: Active** (plain bold, no heading)`. One BB/note; caps ≤2500w
/≤6 code/≤400 lines. Forbidden YAML fields per master (`title`, `category`, `created`, `updated`, `source`,
`parent`, `author`, `related_wiki`, `note_second_category`). Year tags quoted. No wiki/markdown links in YAML.
Not invented — matches existing `cc_` notes.

## Undigested Terms Plan (SP06a)

**SP06a OWNS 4 new term captures** (DB-confirmed absent 2026-06-15; capture via `/tessellum-capture-term-note`
BEFORE writing the digest notes — Pattern B interleaved). Each capture runs the three-way existence check
(absent → full capture) and follows the full Term-Note Authoring Requirements below.

| Term slug | Concept | Capture Phase | Stub or Full | Best-fit glossary | Source page(s) |
|---|---|---|---|---|---|
| `term_persistent_goal` | standing-objective loop (Ralph loop): aux-judge per-turn `{done,reason}` + auto-continuation until done/paused/budget | Phase 1 (before Note 5) | full | `acronym_glossary_llm.md` | features/goals.md |
| `term_delegate_task` | subagent spawn tool: isolated child AIAgents, restricted toolsets, leaf/orchestrator depth, summary-only return (links `term_subagent`) | Phase 1 (before Note 3) | full | `acronym_glossary_llm.md` | features/delegation.md |
| `term_agent_trajectory` | ShareGPT-format agent run trace (conversations + tool_stats + reasoning coverage) for fine-tuning/eval | Phase 1 (before Note 6) | full | `acronym_glossary_llm.md` | features/batch-processing.md |
| `term_code_execution_tool` | `execute_code` RPC Python sandbox: agent-authored Python calling Hermes tools over a Unix socket, scrubbed env, 7-tool whitelist | Phase 1 (before Note 4) | full | `acronym_glossary_developer.md` | features/code-execution.md |


| Term | Decision | Owner | Note |
|------|----------|-------|------|
| `term_cron`, `term_cron_expression` | LINK | (existing) | generic scheduling concepts; Notes 1/2 are Hermes' `cronjob` procedure/model. |
| `term_subagent`, `term_multi_agent_systems`, `term_agent_orchestration` | LINK | (existing) | component concepts of Note 3 delegation. |
| `term_autonomous_coding_agents`, `term_agent_harness`, `term_agentic_ai`, `term_self_evolving_agent` | LINK | (existing) | the agent-class concepts these features extend. |
| `term_rpc`, `term_sandbox`, `term_function_calling`, `term_prompt_injection`, `term_pii` | LINK | (existing) | Note 4 code-exec component/security concepts. |
| `term_fine_tuning`, `term_synthetic_data`, `term_huggingface`, `term_evaluation_harness`, `term_few_shot_learning` | LINK | (existing) | Note 6 batch/trajectory component concepts. |
| `term_fallback_provider`, `term_provider_routing`, `term_credential_pool` | LINK only (+fin, `[own]`) | SP09 | provider recovery is configured here, concept home is SP09. |
| `term_messaging_gateway`, `term_silence_token` | LINK only (+fin, `[own]`) | SP11 | cron delivery targets the gateway; `[SILENT]` token concept owned by SP11. |
| `term_nous_portal` | LINK only (+fin, `[own]`) | SP14 | batch cost-control tip references the Portal subscription. |

### Renamed (general → specific)

| Original candidate slug | Renamed to | Reason (specificity audit) |
|---|---|---|
| `term_goal` (would be too general — collides with OKR/objective/goal-conditioned-RL "goal") | `term_persistent_goal` | scope-qualified to the standing-objective continuation-loop concept (Ralph loop), per master inventory. |
| `term_trajectory` (too general — collides with RL state-action "trajectory" / physics) | `term_agent_trajectory` | scope-qualified to the ShareGPT agent-run-trace artifact. |
| `term_code_execution` (too general — bare "code execution" is a generic CS concept) | `term_code_execution_tool` | scope-qualified to the `execute_code` RPC sandbox TOOL. |

### Removed (substantive vault notes already cover the concept — link instead of create)

| Candidate (would-be) slug | Existing note (path, status) | Action |
|---|---|---|
| `term_delegation` / `term_subagent_delegation` | `term_subagent.md` (active) | Not captured as a separate delegation concept — `term_delegate_task` is the TOOL (distinct, owned); `term_subagent` is the entity (LINK). The `term_deleg*` LIKE hits (`term_delegated_identity`, `term_delegated_work`, both active) are UNRELATED concepts — confirmed by reading their names/status; NOT removed-as-dup, just non-colliding. |
| `term_scheduled_tasks` (would duplicate) | `term_cron.md` + `term_cron_expression.md` (active) | Not captured — link the existing terms from Notes 1/2. |
| `term_execute_code_rpc` (would duplicate the owned slug) | n/a | Not a separate note — folded into the owned `term_code_execution_tool`. |

## Term-Note Authoring Requirements (Per Undigested Term — Inherited from `/tessellum-capture-term-note` canonical)

Every owned term (`term_persistent_goal`, `term_delegate_task`, `term_agent_trajectory`,
`term_code_execution_tool`) MUST be authored via **`/tessellum-capture-term-note <term>`** (interactive or via
ENRICHER_INPUTS), NOT inline-authored within a digest note. The capture skill enforces the requirements below;
this plan invokes them.

### YAML Frontmatter (Required Fields)

```yaml
---
tags:
  - resource
  - terminology
  - <domain_tag_1>          # e.g., llm, agentic_ai
  - <domain_tag_2>
keywords:
  - <ACRONYM or canonical name>
  - <Full Name>
  - <variant_spellings>
topics:
  - <topic_1>
  - <topic_2>
language: markdown
date of note: 2026-06-15
status: active
building_block: concept       # MUST be concept for term notes
access_control_group: ["general"]
related_wiki: <primary_url_or_null>
---
```

### Required H1 + H2 Sections (in order)

`# <Canonical Name>` H1 → `## Definition` (1-2 paragraphs: what it is, the problem it solves, who uses it) →
`## Context` (Hermes Agent subsystem + analogous multi-agent/RL systems that use the concept) →
`## Key Characteristics` (distinctive properties) → `## Performance / Metrics` (OPTIONAL — only if found) →
`## Related Terms` (**8-15 vault term-note links minimum**, INDEXED `**[Term Name](term_X.md)** — description`,
≥3 in-domain + ≥3 cross-domain) → `## References` (EXTERNAL URLs ONLY; NO `term_*.md` links here).


The Hermes doc page is ONE viewpoint. Each capture MUST research across multiple sources:
4. **External (≥2 of):** Wikipedia, the original method/source (e.g. Codex CLI 0.128.0 `/goal` for `term_persistent_goal`; ShareGPT format for `term_agent_trajectory`; OpenAI/Anthropic tool-use docs for `term_delegate_task`/`term_code_execution_tool`), upstream `NousResearch/hermes-agent` source, top arXiv result on the method.
5. **Vault cross-reference:** `/tessellum-search-notes <term>` + DB query for in-domain + cross-domain related terms.

If research returns nothing substantive: ask the user for a direct URL OR mark `status: stub` +
`research_pending: true` — do NOT silently emit a digest-doc-only stub.

### Cross-Domain Diversity for Related Terms (8-15 links minimum)

≥3 in-domain + ≥3 cross-domain (Foundation / Application / Analogy / Contrast / Successor-Predecessor /
Component), e.g.: `term_persistent_goal` → Foundation `term_agent_harness`, Contrast `term_delegate_task`
(durable vs synchronous), Successor of the Ralph-loop pattern; `term_delegate_task` → Component `term_subagent`,
Contrast `term_code_execution_tool`, Analogy map-reduce fan-out; `term_agent_trajectory` → Application
`term_fine_tuning`, Foundation `term_synthetic_data`, Contrast eval-vs-training data; `term_code_execution_tool`
→ Component `term_rpc`/`term_sandbox`, Contrast `term_delegate_task` (mechanical-vs-reasoning).

### Math Notation, Fleeting Content, Glossary, Naming, Depth, Backlinks (inherited verbatim)

- **Math**: any formula in MathJax (`$...$` / `$$...$$`); preserve verbatim, never paraphrase. (These 4 terms are largely non-mathematical; apply only if a formula appears.)
- **Fleeting content guard**: strip person aliases (`@iankar8` → "a contributor"), bare ETAs, bare dollar amounts, headcounts, reporting lines (add temporal qualifier if kept).
- **Glossary entry** (4-5 sentence Description MAX, bold the single most important fact, NO metrics): `term_persistent_goal`/`term_delegate_task`/`term_agent_trajectory` → `acronym_glossary_llm.md`; `term_code_execution_tool` → `acronym_glossary_developer.md`. Use the exact `**Full Name** / **Description** / **Documentation** / **Wiki** / **Related**` template.
- **File naming**: canonical slugs as listed (already normalized).
- **Depth-scaled Related Terms minimums**: 8 (simple 40-80L) / 10 (moderate 80-150L) / 12 (complex 150-250L). Target 8-10 (these are moderate-depth feature concepts).
- **Backlink expansion (Step 6 — REVERSE)**: add the new term to 5-10 existing in-domain + cross-domain term notes' `## Related Terms`; convert 1-2 plain-text mentions in existing non-term notes to links.
- **>200-line decomposition** (Step 7): if a capture exceeds 200 lines, decompose (Procedure→`sop_*`, Model/Argument→`thought_*`), KEEP concept+navigation in parent.

### ENRICHER_INPUTS Non-Interactive Pattern

For interleaved batch dispatch from `/tessellum-execute-digestion-plan`, supply `ENRICHER_INPUTS` (key_terms,
acronym, domain context keywords, summary_snippets from the source page, references) + `SOURCE CONTENT`
(verbatim excerpt). Capture still REQUIRES Steps 3d (in-domain) + 3e (cross-domain) related-terms from the

### Acceptance — a capture is NOT done if

Single-source (digest-doc-only) trapped scope · `## Related Terms` < depth-scaled minimum · no cross-domain
diversity · no Step-6e inlink expansion · `## References` contains `term_*.md` links · `## Related Terms`
contains external URLs · section ordering violated · forbidden YAML field · `building_block` ≠ concept ·
fleeting content unqualified · glossary Description > 5 sentences or has metrics · note > 200 lines without
Step-7 decomposition · non-canonical filename · substantive note OVERWRITTEN (data loss) · research dry with
no user-prompt fallback · any plain-text math instead of MathJax.

## Execution Phases (per-phase 8-GATE)

- **Phase 1 (owned term captures — Pattern B, BEFORE digest notes):** `/tessellum-capture-term-note` for
  `term_persistent_goal`, `term_delegate_task`, `term_agent_trajectory`, `term_code_execution_tool` →
  reindex → verify each exists (G5 pre-check for the notes that link them). GATE G1–G8 on the term notes.
- **Phase 2 (cron cluster, P2 pilot):** Notes 1, 2. Pilot Note 1 first → reindex → verify
  format/ghost/in-degree BEFORE Note 2. GATE G1–G8.
- **Phase 3 (multi-agent + automation notes):** Notes 3, 4, 5, 6. GATE G1–G8.
- **Phase 3b (inlinks — EXECUTED, not recommended):** add the inlink-table edits (G8).

Each phase: G1 `/tessellum-check-note-format` · G2 diff vs `inbox/hermes_agent_docs/<page>` (code verbatim
for kept blocks) · G3 density+coverage · G4 cross-refs + entry-point row · **G5 ghost (Script 4, DB-verify
every ref — owned terms must be captured FIRST)** · **G6 broken-links (`/tessellum-check-broken-links`→`/tessellum-fix-broken-links`)**
· G7 single-BB · **G8 in-degree ≥1 from outside the folder**.

## Validation Scripts

```bash
DB_PATH=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import DB_PATH_STR;print(DB_PATH_STR)")
VAULT=$(python3 -c "import sys;sys.path.insert(0,'scripts');from config import VAULT_PATH_STR;print(VAULT_PATH_STR)")
TARGET="$VAULT/resources/documentation/hermes_agent"; PREFIX="hermes_"
# Script 1: format + density
for f in "$TARGET"/${PREFIX}cron_scheduling.md "$TARGET"/${PREFIX}cron_advanced_jobs.md "$TARGET"/${PREFIX}subagent_delegation.md "$TARGET"/${PREFIX}code_execution.md "$TARGET"/${PREFIX}persistent_goals.md "$TARGET"/${PREFIX}batch_processing.md; do
  python3 scripts/check_note_format.py "$f";
  w=$(sed -n '/^---$/,/^---$/!p' "$f"|wc -w); c=$(( $(grep -c '^```' "$f")/2 )); l=$(wc -l <"$f")
  [ "$w" -gt 2500 ]||[ "$c" -gt 6 ]||[ "$l" -gt 400 ] && echo "DENSITY: $(basename $f)"; done
# Script 4: G5 ghost detection
for f in "$TARGET"/${PREFIX}cron_scheduling.md "$TARGET"/${PREFIX}cron_advanced_jobs.md "$TARGET"/${PREFIX}subagent_delegation.md "$TARGET"/${PREFIX}code_execution.md "$TARGET"/${PREFIX}persistent_goals.md "$TARGET"/${PREFIX}batch_processing.md; do
  grep -oE '\]\(([^)]+\.md)[^)]*\)' "$f"|sed -E 's/.*\(([^)]+\.md).*/\1/'|while read l; do
  c=$(echo "$l"|sed -E 's/#.*$//'); r=$(cd "$(dirname "$f")"&&realpath -q -m "$c" 2>/dev/null); [ -z "$r" ]&&continue
# G8: in-degree ≥1 from outside the folder (incl. the 4 owned term captures)
for n in hermes_cron_scheduling hermes_cron_advanced_jobs hermes_subagent_delegation hermes_code_execution hermes_persistent_goals hermes_batch_processing; do
for t in term_persistent_goal term_delegate_task term_agent_trajectory term_code_execution_tool; do
  echo -n "$t indeg: "; sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM note_links WHERE target_id='resources/term_dictionary/$t.md';"; done
```

## Entry Point Decision (inherited)

Contributes 6 rows to the new `0_entry_points/entry_hermes_agent_docs.md` (CREATE — master Step 4c,
>30-note series) under an "Automation & Multi-Agent" section. Parent hub back-link in
`entry_research_and_ai_hub.md` is handled at master level. SP06a does NOT create a separate entry point —
the >30-note corpus shares the single master-created `entry_hermes_agent_docs.md` (matches the >30 threshold).

## Inlinks (existing notes → new notes) — G8

| Existing note | → New note | Rationale |
|---------------|-----------|-----------|
| `repo_hermes_agent_cron.md` | → `hermes_cron_scheduling`, `hermes_cron_advanced_jobs` | cron repo ↔ cron usage docs |
| `repo_hermes_agent_tools.md` | → `hermes_subagent_delegation`, `hermes_code_execution` | tools repo (`delegate_task`/`execute_code`) ↔ tool usage docs |
| `repo_hermes_agent_trajectory_research.md` | → `hermes_batch_processing` | trajectory/batch repo ↔ batch-processing doc |
| `repo_hermes_agent_agent_core.md` | → `hermes_persistent_goals`, `hermes_subagent_delegation` | agent core (loop/orchestrator) ↔ goal-loop + delegation docs |
| `repo_hermes_agent.md` | → `hermes_cron_scheduling` | implementation ↔ automation usage |
| `term_cron.md` | → `hermes_cron_scheduling`, `hermes_cron_advanced_jobs` | concept term → user-facing cron docs |
| `term_subagent.md` | → `hermes_subagent_delegation` | concept term → delegation doc |
| `term_autonomous_coding_agents.md` | → `hermes_persistent_goals` | agent-class term → standing-goal-loop doc |
| `entry_code_snippets_hermes_agent.md` | → `hermes_cron_scheduling`, `hermes_subagent_delegation`, `hermes_batch_processing` | code layer ↔ docs layer |
| `entry_hermes_agent_docs.md` (new, master) | → all 6 notes + the 4 owned term notes | navigation hub |

Guarantees every new note (6 docs + 4 owned terms) in-degree ≥1 from outside the folder (G8). Inlink addition
is a gated execution phase (Phase 3b), not a recommendation. The 4 owned term captures also gain inbound links
from the digest notes' `## Related Notes` (Phase 1 before Phase 3) and from the Step-6e term-note backlink
expansion in their captures.

## Pacing Rules (inherited)

Capture the 4 owned terms FIRST (Phase 1) so the digest notes' Related-Notes links resolve at G5. Pilot Note 1
(`hermes_cron_scheduling`) → reindex → verify format/ghost/in-degree BEFORE the rest. Commit per phase
(per-wave commits for multi-agent runs). Re-read the source page before writing each note — do NOT work from
memory. Code blocks verbatim for kept blocks; curate code-heavy notes (cron 37, delegation 11, code-exec 10)
to ≤6 load-bearing examples, summarize the rest in prose. If a note exceeds 350 lines during writing, STOP and
split. If multi-agent: agents return note content, master writes serially where there is write-contention; ≤30
agents/run; embed the manifest in the workflow script.

## Follow-up Recommendations

- After SP06a lands: run `/tessellum-run-incremental-update`, then `/tessellum-add-inlinks`; add the 6 rows + 4 owned-term mentions to the master-created entry point; backfill the `repo_hermes_agent_*` / `term_*` inlinks (G8); run `/tessellum-check-broken-links` → `/tessellum-fix-broken-links`.
- Cross-link with SP06b once it lands: `hermes_cron_advanced_jobs` ↔ kanban multi-agent board; `hermes_subagent_delegation` ↔ hooks/plugins lifecycle.
- Cross-link with SP02 (config), SP09 (provider recovery / credential pools), SP14 (Nous Portal batch cost) — bidirectional config/concept links once those SPs are executed.
- Consider one `thought_` note comparing Hermes' docs-stated delegation/code-exec model vs the code-digestion findings in `snippet_hermes_agent_tools_delegate_*` / `snippet_hermes_agent_tools_code_exec_*`.

## Augmentation Report

- Density re-read: counts match measured (cron 3861, delegation 2007, code-execution 1661, goals 1601, batch-processing 1176); **1 split** (cron→2 on BB-mixing + >2500w); the other 4 pages → 1 note each. All 6 notes ≤2500w; code-heavy notes curated to ≤6 blocks.
- Collision audit: **0 doc-note removals**; 4 owned term slugs CAPTURED (all DB-absent); 3 specificity renames recorded (`term_goal→term_persistent_goal`, `term_trajectory→term_agent_trajectory`, `term_code_execution→term_code_execution_tool`); 2 `term_deleg*` LIKE hits confirmed non-colliding.
- Owned-term captures: 4 (Pattern B, Phase 1 before digest notes), excluded from the ≥8 term floor as `[own]` forward-refs in mappings.
- Entry-point decision: shares master-created `entry_hermes_agent_docs.md` (>30-note series) — matches threshold.

## 31-Item Checklist

PASS 31/31. (Objective ✓ Routing ✓ Source measured ✓ Content Strategy ✓ Coverage Map (no orphans) ✓ Split
Decisions ✓ Planned Notes ✓ Size Assessment ✓ Summary Stats ✓ BB Distribution ✓ Per-note Cross-Refs (FOUR-FLOOR ≥8 term /
4 owned terms) ✓ Phase GATEs incl G5/G6/G8 ✓ Note Format Def
(derived) ✓ Validation Scripts ✓ Pacing ✓ Density Re-Assessment (re-read) ✓ Follow-up ✓ Undigested Terms Plan
(4 owned) ✓ Capture Phase per term (Phase 1, no TBD) ✓ best-fit glossary per term (llm ×3 / developer ×1, all
exist) ✓ Term-Note Auth Reqs (multi-source mandate, must-language) ✓ invokes capture-term-note per term ✓
Entry-Point Decision ✓ matches size threshold ✓ Slug Specificity (3 renames recorded) ✓ Slug Collision (4 owned
verified absent; 2 `term_deleg*` LIKE false-positives confirmed) ✓ dedup generalized to ALL notes incl doc,
searched term_dictionary AND documentation/ ✓ G8 in every phase + inlinks EXECUTED (Phase 3b) ✓ Doc-Note
Authoring Spec derived ✓).

## Review Sign-Off

**Re-reviewed 2026-06-19 (FOUR-FLOOR re-augmentation) — READY FOR EXECUTION (9/9 checkpoints pass).**
Independent review of the four-floor re-augmentation: per-note link counts measured programmatically (all 6 notes
= 8 term / 5 code-repo / 10 doc / 10–11 snippet, every link carries a `relevance:` clause). Anti-fabrication:
exempt (created later, resolve at G5/G8). CP7 source counts re-measured from `inbox/hermes_agent_docs/` (3861/2007/1661/1601/1176
— ratio 1.00). Minimal factual fix applied: corrected the collision-audit "3 `term_deleg*` hits" → "2" (the
`term_dns_delegation` note does not exist in the DB; it was never a cited cross-ref, so no floor/ghost impact — the
NOT-a-dup verdict is unchanged). No other changes; no gate weakened; `status:` unchanged.

**Reviewed 2026-06-15 — READY FOR EXECUTION (9/9 checkpoints pass).**

| CP | Check | Result | Evidence |
|----|-------|--------|----------|
| CP2 | 8-GATE per batch (G1-G6,G8) | PASS | 4 phases (incl. Phase 1 term captures + Phase 3b inlinks), each G1–G8 incl G5-ghost + G6-broken + G8-discoverability. |
| CP3 | Entry point specified | PASS | Shares master-created `entry_hermes_agent_docs.md` (6 rows under an Automation & Multi-Agent section); parent hub at master level (matches >30 threshold). |
| CP4 | Plan size manageable | PASS | 6 notes ≤30; master holds the corpus-level split (SP06 split into a/b). |
| CP5 | Note format aligned + DERIVED | PASS | Doc-Note Authoring Spec derived from `cc_*.md` (verified vs `cc_admin_enforcement_controls.md`/`cc_sandbox_modes.md`); not invented. |
| CP6 | Borderline density → split | PASS | cron.md→2 (BB-mixing + >2500w); other 4 pages ≤2500w single-BB → 1 note each; all ≤2500w; code-heavy notes curated ≤6. |
| CP7 | Source counts measured | PASS | Re-read 2026-06-15: cron 3861, delegation 2007, code-execution 1661, goals 1601, batch-processing 1176 — measured == plan (ratio 1.00). |
| CP8 | Undigested Terms + Authoring Reqs | PASS | SP06a OWNS 4 captures (`term_persistent_goal`, `term_delegate_task`, `term_agent_trajectory`, `term_code_execution_tool`); each has Capture Phase (Phase 1, no TBD) + verified best-fit glossary; Term-Note Authoring Requirements present with multi-source must-language mandate + ENRICHER_INPUTS; invokes `/tessellum-capture-term-note` per term. |
| CP8f | Slug specificity + all-notes collision audit | PASS | Collision & Dedup Audit covers all 6 doc notes + 4 owned slugs (term_dictionary AND documentation/); 4 owned slugs DB-confirmed absent; 2 `term_deleg*` LIKE false-positives confirmed non-colliding; Renamed (3) + Removed sub-tables present. |
| CP9 | Discoverability — inbound links (G8) | PASS | Inlinks table covers all 6 notes + 4 owned terms from repo_*/term_*/entry_* outside the folder; inlink addition is gated Phase 3b, not a recommendation; G8 script checks owned-term in-degree too. |

**RESULT: 9/9 → READY FOR EXECUTION (re-confirmed 2026-06-19 against the FOUR-FLOOR standard ≥8 term / ≥5 code-repo / ≥10 snippet / ≥10 doc per note).**

## Re-Sync Note (2026-06-19)

The local doc mirror `inbox/hermes_agent_docs/` was re-synced from upstream `NousResearch/hermes-agent`
`website/docs/` — pin moved from `95715dc` to `c253b07` (now byte-identical to upstream `main` HEAD). All 5 of
this sub-plan's owned pages were independently re-measured (BODY-only word count after stripping YAML
frontmatter; code-block count = `^\s*```` lines ÷ 2) and the word/code counts are **UNCHANGED** vs the
2026-06-15 Source Pages table:

- `user-guide/features/cron.md` — 3861w/37code (unchanged)
- `user-guide/features/delegation.md` — 2007w/11code (unchanged)
- `user-guide/features/code-execution.md` — 1661w/10code (unchanged)
- `user-guide/features/goals.md` — 1601w/5code (unchanged)
- `user-guide/features/batch-processing.md` — 1176w/7code (unchanged)

No planned-note, split (cron→2), density (all 6 notes ≤2500w / ≤6 code / ≤400 lines), or cross-ref
(now FOUR-FLOOR ≥8 term + ≥5 code-repo + ≥10 snippet + ≥10 doc, all counted, set 2026-06-19) decision is affected.
**Plan remains READY** — provenance class (zero count drift).

## Pipeline Status (Per-Sub-Plan)


**Source**: `inbox/hermes_agent_docs/user-guide/features/{cron,delegation,code-execution,goals,batch-processing}.md`
**Last Updated**: 2026-06-15 (re-verified 2026-06-19, mirror c253b07)
**Status**: Ready (augmented + reviewed)
