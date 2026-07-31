---
title: Sub-Plan B10B — Claude Code Docs: Workflows, Worktrees, Goal & Advisor
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["workflows", "worktrees", "goal", "advisor"]
---

# Sub-Plan B10B: Workflows, Worktrees, Goal & Advisor

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

Four orchestration/control pages that sit on top of the subagent primitive: **dynamic workflows**
(script-driven subagent orchestration at scale), **git worktrees** (file-edit isolation for parallel
sessions), **`/goal`** (run-until-condition-met loop), and the **advisor tool** (consult a stronger
model at decision points). P2 (Phase B) — these are features built on the cores defined in Phase A
(subagents, agent teams, model-config, hooks, settings, permissions), which are referenced via links,
never duplicated.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 7,076 measured words. **Planned: 6 notes.**

## Content Strategy

- **Prioritize**: the orchestration-vs-other-primitives decision (workflows vs subagents vs skills vs
  agent teams) and the advisor model-pairing rules — the load-bearing decision content of these pages.
- **Split**: `workflows.md` (2,748w >2500 cap) splits into a **concept** note (what/when/how-it-runs) and
  a **procedure** note (write/approve/save/manage). `advisor.md` splits into a **concept** note (what it
  is / when / consultation behavior) and a **procedure** note (enable / choose model / pairings / off /
  requirements) to keep one BB per note. `worktrees.md` and `goal.md` are each one procedure note.
- **Skip / link-out (own other sub-plans)**: the subagent/agent-team primitives → B10A (`sub-agents.md`,
  `agent-teams.md`, `agent-view.md`, `agents.md`); permission modes → B05A; settings/`disableWorkflows` →
  B03A; hooks (`WorktreeCreate`/`WorktreeRemove`/Stop-hook) → B07A/B07B; model-config/`opusplan`/effort →
  B03B; `/loop` & scheduled tasks → B11; prompt-caching → B02A; non-interactive `claude -p` → B11;
  desktop parallel sessions → B12A; costs → B02A. These are referenced via links, never duplicated.
- **Glossary**: not re-digested into `cc_` notes — terms route to existing term notes / their home
  sub-plan (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| workflows | /workflows | 2,748 | 4 | 6 | 11 | concept + procedure |
| worktrees | /worktrees | 1,328 | 12 | 7 | 1 | procedure |
| goal | /goal | 1,309 | 4 | 5 | 6 | procedure |
| advisor | /advisor | 1,691 | 4 | 11 | 4 | concept + procedure |

> **H2 lists (document order):**
> - **workflows**: When to use a workflow · Run a bundled workflow (H3 Bundled workflows, Watch the run) · Have Claude write a workflow (H3 Ask for a workflow in your prompt, Let Claude decide with ultracode, Approve the plan before it runs, Save the workflow for reuse, Pass input to a saved workflow) · How a workflow runs (H3 Behavior and limits) · Manage runs (H3 Resume after a pause, Cost, Turn workflows off) · Related resources
> - **worktrees**: Start Claude in a worktree (H3 Choose the base branch) · Copy gitignored files into worktrees · Isolate subagents with worktrees · Clean up worktrees · Manage worktrees manually · Non-git version control · See also
> - **goal**: Compare ways to keep a session running · Use `/goal` (H3 Set a goal, Write an effective condition, Check status, Clear a goal, Resume with an active goal, Run non-interactively) · How evaluation works · Requirements · See also
> - **advisor**: When to use the advisor · Enable the advisor (H3 Use the `/advisor` command, Set `advisorModel` in settings, Use the `--advisor` flag) · Choose an advisor model (H3 Common model pairings) · When Claude consults the advisor · What you see during a session · Cost · Impact on prompt caching · Requirements · Turn the advisor off · Compare with related features · See also

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **6 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_dynamic_workflows.md` | concept | workflows: When to use, Run a bundled workflow (intro + Bundled workflows), How a workflow runs (+ Behavior and limits) | 600 | What a dynamic workflow is (JS script orchestrating subagents at scale); the workflows-vs-subagents-vs-skills-vs-agent-teams "who holds the plan" comparison; the repeatable-quality-pattern argument; `/deep-research` bundled workflow; isolated runtime, script-variable intermediates, agent caps (16 concurrent / 1,000 total). Links B10A primitives. |
| 2 | `cc_create_and_run_workflows.md` | procedure | workflows: Have Claude write a workflow (all H3), Watch the run, Manage runs (Resume, Cost, Turn off) | 700 | How to make and operate a workflow: `ultracode` keyword vs `/effort ultracode`; approve-the-plan per-permission-mode prompt; `/workflows` progress view + key bindings; save to `.claude/workflows/` or `~/.claude/workflows/`; `args` input; resume after pause; cost control; disable (`/config`, `disableWorkflows`, `CLAUDE_CODE_DISABLE_WORKFLOWS`). Links B05A modes, B03A settings, B03B model. |
| 3 | `cc_worktree_isolation.md` | procedure | worktrees: all H2 (Start, Choose base branch, Copy gitignored, Isolate subagents, Clean up, Manage manually, Non-git VCS) | 650 | Run parallel sessions in isolated git worktrees: `--worktree`/`-w` flag, auto-generated names, `EnterWorktree` tool, base-branch (`worktree.baseRef` fresh/head, `#PR`), `.worktreeinclude`, subagent `isolation: worktree`, automatic cleanup vs `git worktree remove`, manual `git worktree` commands, `WorktreeCreate`/`WorktreeRemove` hooks for non-git VCS. Links B10A subagents, B07A hooks, B03A settings. |
| 4 | `cc_goal_command.md` | procedure | goal: all H2/H3 (Compare ways, Use `/goal`, Set/Write/Check/Clear/Resume/Non-interactive, How evaluation works, Requirements) | 650 | The `/goal` run-until-condition-met loop: a fast model re-checks the condition after every turn; compare with `/loop`, Stop hooks, auto mode; set/check/clear (aliases), write an effective condition (measurable end state, stated check, 4,000-char cap, turn/time clause), resume restores condition, `-p` runs to completion; evaluation = session-scoped prompt-based Stop hook on the small fast model (Haiku); trust + hook-setting requirements. Links B07A/B07B hooks, B11 loop, B05A auto mode. |
| 5 | `cc_advisor_tool.md` | concept | advisor: intro, When to use the advisor, When Claude consults the advisor, What you see during a session, Impact on prompt caching, Compare with related features | 600 | What the advisor tool is: a server-side tool pairing the main model with a stronger advisor model Claude consults at decision points (before committing, on recurring errors, before declaring done); receives full conversation, returns guidance Claude applies but can override when its own evidence contradicts; `Advising`/`Ctrl+O` transcript UX; does not invalidate prompt cache; compare-with advisor vs `opusplan` vs subagent-model vs `/model`. Links B03B model-config, B10A subagents, B02A prompt-caching. |
| 6 | `cc_configure_advisor_model.md` | procedure | advisor: Enable the advisor (all H3), Choose an advisor model (+ Common model pairings), Cost, Requirements, Turn the advisor off | 550 | How to set up the advisor: `/advisor` command, `advisorModel` setting, `--advisor` flag (precedence + error behavior); the accepted-advisor-per-main-model table (Haiku/Sonnet/Opus/Fable rules; advisor ≥ main); `opus`/`sonnet`/`fable` aliases + full model IDs; common pairings; cost (advisor-rate tokens at decision points); v2.1.98+ / Anthropic-API-only requirements; turn off (`/advisor off`, `CLAUDE_CODE_DISABLE_ADVISOR_TOOL`). Links B03B model-config, B03A env-vars, B14A providers. |

**Estimate: 6 notes** — concept ×2 (notes 1, 5), procedure ×4 (notes 2, 3, 4, 6). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (7,076 words). New `cc_` notes: 6. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~3,750 (avg ~625/note). Code blocks: ≤4 per note (verbatim from source; all within the ≤6 cap — see Density Re-Assessment).
- **Building Block Distribution**: concept ×2 (notes 1, 5) · procedure ×4 (notes 2, 3, 4, 6). No model/argument/empirical_observation in this sub-plan (the workflows "repeatable quality pattern" claim is folded into the note-1 concept Overview, not split into a standalone argument note).

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_dynamic_workflows` (7 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — A subagent is a worker Claude spawns with isolated context; the note defines a dynamic workflow as a script that orchestrates subagents "at scale" (dozens to hundreds), making the subagent the exact primitive this note builds on.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — The note's core distinction is *who holds the plan* — a workflow moves the orchestration into a script that owns the loop, branching, and intermediate results, which is precisely the agent-orchestration concept this term defines.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — A workflow run coordinates many independent Claude agents (up to 1,000 per run) toward one task, the multi-agent-systems pattern this term covers.
- [Fan-Out](../../term_dictionary/term_fan_out.md) — `/deep-research` "fans out web searches across several angles" and a workflow fans dozens-to-hundreds of agents from one script — the fan-out execution pattern this term names.
- [Scatter-Gather](../../term_dictionary/term_scatter_gather.md) — A workflow scatters work across parallel agents and gathers their results into script variables before returning one final answer, the scatter-gather pattern this term defines.
- [Context Window](../../term_dictionary/term_context_window.md) — The note's central trade-off is that a workflow keeps intermediate results in script variables instead of Claude's context window, so the main context holds only the final answer — directly the context-window concept.
- [Agent-as-a-Judge](../../term_dictionary/term_agent_as_a_judge.md) — The note's "repeatable quality pattern" has independent agents adversarially review each other's findings before reporting and vote on each claim — agents judging agents, the agent-as-a-judge pattern.

### 2. `cc_create_and_run_workflows` (6 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — The procedure operates a run that spawns subagents in `acceptEdits` mode inheriting your tool allowlist; the subagent is the worker the saved/written workflow orchestrates.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — Writing, saving, and rerunning a workflow script codifies the orchestration itself as a reusable command, the orchestration-as-artifact idea this term covers.
- [Fan-Out](../../term_dictionary/term_fan_out.md) — The note describes pointing Claude at an existing orchestrator (a folder of subagent prompts or a skill that fans work out) to generate a workflow — the fan-out execution this procedure produces.
- [Skills](../../term_dictionary/term_skills.md) — A saved workflow runs as a `/<name>` command alongside skills in `/` autocomplete and lives under `.claude/workflows/`, paralleling how skills are packaged and invoked.
- [Context Window](../../term_dictionary/term_context_window.md) — The Cost section frames per-stage model choice and the script-variable design as ways to keep token/context spend bounded, tying operation of the run to context-window economics.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — `ultracode` combines `xhigh` reasoning effort with automatic workflow orchestration; the reasoning-effort dial this procedure sets is the chain-of-thought depth control.

### 3. `cc_worktree_isolation` (6 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — A dedicated section sets `isolation: worktree` on a custom subagent so each subagent gets a temporary worktree; the subagent is the worker whose parallel edits worktrees keep from colliding.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — A worktree is an isolation boundary — a separate working directory whose edits never touch another session's files — the same isolate-execution goal sandboxing provides at the process level.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — Worktree cleanup hinges on whether uncommitted changes / new commits exist, and worktrees preserve a branch you can return to — the safe-restore-point discipline this term covers, applied to git state.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — Worktrees let many parallel Claude sessions (and the desktop app's per-session worktrees) edit the same repo without conflict, the multi-agent parallel-execution scenario this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Isolating each agent's file edits in its own checkout is what lets an autonomous coding agent build a feature in one terminal while another fixes a bug, the parallel-autonomy mode this term names.
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents a Claude Code CLI capability (`--worktree`, `EnterWorktree`, `.worktreeinclude`), so the product term is its definitional host.

### 4. `cc_goal_command` (7 term notes)
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — `/goal` makes Claude keep working across turns without per-step prompting until a verifiable end state holds — the autonomous, self-driving operating mode this term defines.
- [Agentic Evaluation](../../term_dictionary/term_agentic_evaluation.md) — After each turn a small fast model evaluates whether the condition is met and returns a yes/no plus a reason that guides the next turn — an agentic-evaluation loop, exactly this term.
- [Agent-as-a-Judge](../../term_dictionary/term_agent_as_a_judge.md) — The completion check is decided by a fresh evaluator model rather than the one doing the work, an independent model judging another agent's output — the agent-as-a-judge pattern.
- [LLM-as-a-Judge](../../term_dictionary/term_llm_as_a_judge.md) — The evaluator judges the condition only against what Claude has surfaced in the conversation (it runs no tools), the transcript-only LLM-as-a-judge evaluation this term covers.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — An effective condition states a measurable end state plus how Claude should prove it and a turn cap, structuring the reasoning Claude reports each turn — the chain-of-thought scaffolding this term names.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — `/goal` deliberately removes the per-turn human prompt (and pairs with auto mode to remove per-tool prompts), contrasting with the human-in-the-loop control this term defines; clear/Ctrl+C restore it.
- [Self-Evolving Agent](../../term_dictionary/term_self_evolving_agent.md) — The condition-check-then-keep-working loop, where each failed check feeds a reason back as guidance for the next attempt, is the iterate-toward-a-goal self-improvement behavior this term describes.

### 5. `cc_advisor_tool` (7 term notes)
- [Agent-as-a-Judge](../../term_dictionary/term_agent_as_a_judge.md) — The advisor is a second, typically stronger model that reviews the full conversation at decision points and returns guidance — one agent judging/advising another, the agent-as-a-judge pattern.
- [LLM-as-a-Judge](../../term_dictionary/term_llm_as_a_judge.md) — Consulting a stronger model before committing to an approach or before declaring a task done is an LLM evaluating the work, the LLM-as-a-judge use this term covers.
- [Ensemble](../../term_dictionary/term_ensemble.md) — Pairing a fast main model with a stronger advisor combines two models' strengths on one task — the model-ensemble idea this term defines, applied at decision points rather than every turn.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — The advisor fits tasks where "plan quality determines the outcome" and is escalated for planning and completion checks — the deliberate-reasoning step this term names, routed to a stronger model.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — A dedicated section explains that toggling the advisor does not invalidate the main model's prompt cache and the advisor's guidance is cached on later turns — directly the prompt-caching concept.
- [Subagent](../../term_dictionary/term_subagent.md) — The Compare-with-related-features table contrasts the advisor (decision-point guidance) with a subagent given a `model` (full delegated subtask), making the subagent the primary alternative this note positions against.
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents a Claude Code feature (`/advisor`, `--advisor`, `advisorModel`), so the product term is its definitional host.

### 6. `cc_configure_advisor_model` (6 term notes)
- [Agent-as-a-Judge](../../term_dictionary/term_agent_as_a_judge.md) — Configuring which stronger model acts as the reviewer of the main model's work is the setup step for the agent-as-a-judge pattern this note operationalizes.
- [Ensemble](../../term_dictionary/term_ensemble.md) — The accepted-advisor-per-main-model table (advisor must be ≥ the main model) defines valid two-model pairings, the model-ensemble combinations this term covers.
- [LLM-as-a-Judge](../../term_dictionary/term_llm_as_a_judge.md) — The pairings (e.g. Sonnet main + Opus advisor) wire up which model evaluates which, the configuration behind LLM-as-a-judge escalation.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — The "when to use" pairings escalate planning and ambiguous failures to the stronger advisor, routing the heavy reasoning this term names to the more capable model.
- [Subagent](../../term_dictionary/term_subagent.md) — The note relates advisor configuration to setting a `model` on a subagent (the Compare-with table), the alternative model-pairing mechanism this term defines.
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note configures a Claude Code feature via `/advisor`, `--advisor`, `advisorModel`, and `CLAUDE_CODE_DISABLE_ADVISOR_TOOL`, so the product term is its definitional host.

## Section Coverage Map

```
workflows.md
├── When to use a workflow (comparison table) ─ → note 1 (cc_dynamic_workflows)
├── Run a bundled workflow ──────────────────── → note 2 (Steps procedure) / intro → note 1
│   ├── Bundled workflows (/deep-research) ──── → note 1
│   └── Watch the run (/workflows + keys) ───── → note 2
├── Have Claude write a workflow ───────────── → note 2 (cc_create_and_run_workflows)
│   ├── Ask for a workflow in your prompt ───── → note 2
│   ├── Let Claude decide with ultracode ────── → note 2 (effort → B03B linked)
│   ├── Approve the plan before it runs ─────── → note 2 (permission modes → B05A linked)
│   ├── Save the workflow for reuse ─────────── → note 2
│   └── Pass input to a saved workflow (args) ─ → note 2
├── How a workflow runs ─────────────────────── → note 1
│   └── Behavior and limits (agent caps) ────── → note 1
├── Manage runs ─────────────────────────────── → note 2
│   ├── Resume after a pause ────────────────── → note 2
│   ├── Cost ────────────────────────────────── → note 2 (costs → B02A linked)
│   └── Turn workflows off (settings/env) ───── → note 2 (settings → B03A linked)
└── Related resources ───────────────────────── → notes 1/2 (links; agents/sub-agents → B10A)
worktrees.md
├── Start Claude in a worktree (--worktree) ── → note 3 (cc_worktree_isolation)
│   └── Choose the base branch (baseRef/#PR) ── → note 3
├── Copy gitignored files (.worktreeinclude) ─ → note 3
├── Isolate subagents with worktrees ───────── → note 3 (subagents → B10A linked)
├── Clean up worktrees ──────────────────────── → note 3 (cleanupPeriodDays → B03A linked)
├── Manage worktrees manually (git cmds) ───── → note 3
├── Non-git version control (Worktree hooks) ─ → note 3 (hooks → B07A linked)
└── See also ────────────────────────────────── → note 3 (links; sessions → B02B, desktop → B12A)
goal.md
├── Compare ways to keep a session running ─── → note 4 (cc_goal_command) (loop → B11, Stop hook → B07B, auto mode → B05A linked)
├── Use /goal ───────────────────────────────── → note 4
│   ├── Set a goal ──────────────────────────── → note 4
│   ├── Write an effective condition ────────── → note 4
│   ├── Check status ────────────────────────── → note 4
│   ├── Clear a goal ────────────────────────── → note 4
│   ├── Resume with an active goal ──────────── → note 4
│   └── Run non-interactively (-p) ──────────── → note 4 (headless → B11 linked)
├── How evaluation works (Stop hook/Haiku) ─── → note 4 (hooks → B07A, model-config → B03B linked)
├── Requirements (trust/disableAllHooks) ───── → note 4 (hooks → B07A linked)
└── See also ────────────────────────────────── → note 4 (links)
advisor.md
├── (intro: what the advisor tool is) ───────── → note 5 (cc_advisor_tool)
├── When to use the advisor ─────────────────── → note 5
├── Enable the advisor ──────────────────────── → note 6 (cc_configure_advisor_model)
│   ├── Use the /advisor command ────────────── → note 6
│   ├── Set advisorModel in settings ────────── → note 6 (settings → B03A linked)
│   └── Use the --advisor flag ──────────────── → note 6
├── Choose an advisor model ─────────────────── → note 6
│   └── Common model pairings ───────────────── → note 6 (model-config → B03B linked)
├── When Claude consults the advisor ────────── → note 5
├── What you see during a session ───────────── → note 5
├── Cost ────────────────────────────────────── → note 6 (costs → B02A linked)
├── Impact on prompt caching ────────────────── → note 5 (prompt-caching → B02A linked)
├── Requirements ────────────────────────────── → note 6 (providers → B14A linked)
├── Turn the advisor off (env var) ──────────── → note 6 (env-vars → B03A linked)
├── Compare with related features ───────────── → note 5 (opusplan/model → B03B, subagents → B10A linked)
└── See also ────────────────────────────────── → notes 5/6 (links)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| workflows.md (2,748w >2500 cap, 6 H2 mixed) | notes 1 (concept), 2 (procedure) | exceeds density cap; "what it is / when / how it runs" (concept) vs "write / approve / save / manage runs" (operational steps) are different BB types. |
| advisor.md (1,691w, 11 H2) | notes 5 (concept), 6 (procedure) | within word cap but cleanly separable: "what the advisor is / when / consultation behavior / cache impact / compare" (concept) vs "enable / choose model / pairings / cost / requirements / turn off" (configuration steps) — one BB per note. |
| worktrees.md (1,328w, 12 code) | note 3 (single) | code-dense but all one BB (procedure); 12 source fences trimmed to ≤6 representative blocks (see Density Re-Assessment). |
| goal.md (1,309w) | note 4 (single) | one BB (procedure), within all caps. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_dynamic_workflows | concept | 600 | 1 | ✅ |
| 2 | cc_create_and_run_workflows | procedure | 700 | 3 | ✅ |
| 3 | cc_worktree_isolation | procedure | 650 | 6 | ✅ |
| 4 | cc_goal_command | procedure | 650 | 4 | ✅ |
| 5 | cc_advisor_tool | concept | 600 | 0 | ✅ |
| 6 | cc_configure_advisor_model | procedure | 550 | 3 | ✅ |

No note exceeds the caps. The one density risk is **note 3** (`worktree.md` has 12 source code fences): the
plan caps it at **6 representative blocks** — keep `claude --worktree feature-auth`, the no-name form, the
`worktree.baseRef` JSON, the `.worktreeinclude` example, one representative `git worktree` command, and the
`WorktreeCreate` SVN-hook JSON; the remaining manual `git worktree add/list/remove` variants are described
in prose / a single fenced block, not one fence each. No over-compression — every H2/H3 maps to a note or an
explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_dynamic_workflows cc_create_and_run_workflows cc_worktree_isolation cc_goal_command cc_advisor_tool cc_configure_advisor_model"
# G1 format + G3 density
for n in $NOTES; do
  f="$CC/$n.md"; python3 scripts/check_note_format.py "$f" 2>&1 | grep -E 'ERROR|LINK-003' || echo "$n OK"
  lines=$(wc -l < "$f"); words=$(sed -n '/^---$/,/^---$/!p' "$f" | wc -w); cb=$(( $(grep -c '^```' "$f") / 2 ))
  [ "$lines" -gt 400 ] || [ "$words" -gt 2500 ] || [ "$cb" -gt 6 ] && echo "DENSITY WARNING: $n"
done
python3 scripts/check_yaml_frontmatter.py --path "$CC"
# G5 ghost: verify every internal .md link target exists in the DB
for n in $NOTES; do f="$CC/$n.md"
  grep -oE '\]\(([^)]+\.md)\)' "$f" | sed -E 's/.*\(([^)]+)\)/\1/' | while read l; do
    r=$(cd "$(dirname "$f")" && realpath -q -m "$l"); id=${r#*/the vault/}
    sqlite3 "$(python3 -c 'import sys;sys.path.insert(0,"scripts");from config import DB_PATH_STR;print(DB_PATH_STR)')" \
      "SELECT 1 FROM notes WHERE note_id='$id'" | grep -q 1 || echo "GHOST $n -> $l"
  done; done
```

## Per-Phase Validation Gate (G1–G8) — inherited from master

Single phase (6 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 6 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 6 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | post-reindex DB confirms in-degree ≥1 for all 6 notes (no graph island) | `note_links` query after reindex |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 6 rows** under an "Orchestration & Control" cluster (workflows, worktrees,
goal, advisor) + increments the BB-distribution counts (concept +2, procedure +4).

## Undigested Terms Plan (Step 4e)

b10b creates **no new `term_dictionary` notes**. Each Claude-Code vocabulary term on these pages is covered
by a b10b `cc_` doc note, an existing substantive term note (link), or its home sub-plan (Pattern B). Dedup
checked across **both** `term_dictionary/` AND `resources/documentation/` (no existing doc note covers
pages):

| Term on page | Disposition |
|---|---|
| Dynamic workflow / Workflow | note 1 `cc_dynamic_workflows` (doc concept) |
| `ultracode` (keyword / effort level) | note 2 `cc_create_and_run_workflows`; effort level → B03B (`model-config`) |
| `/deep-research` (bundled workflow) | note 1 / note 2 |
| Worktree / Worktree isolation | note 3 `cc_worktree_isolation` (doc concept) |
| `EnterWorktree` / `WorktreeCreate` / `WorktreeRemove` | note 3; hook reference → B07A (`hooks`) |
| `.worktreeinclude` | note 3 |
| `/goal` (completion condition) | note 4 `cc_goal_command` (doc concept) |
| Evaluator / small fast model | note 4 (links existing `term_agentic_evaluation` / `term_agent_as_a_judge`) |
| `/loop` | link-out → B11 (`scheduled-tasks`) |
| Stop hook | link-out → B07A/B07B (`hooks` / `hooks-guide`) |
| Auto mode | link-out → B05A (`auto-mode-config`) |
| Advisor tool / `advisorModel` | notes 5/6 `cc_advisor_tool` / `cc_configure_advisor_model` (doc concept) |
| `opusplan` | link-out → B03B (`model-config`) |
| Subagent / Agent teams | existing term `term_subagent`; pages owned by B10A |
| Sandboxing / Context window / Compaction / Prompt caching | existing term notes (link) |
| Settings layers / env vars (`disableWorkflows`, `CLAUDE_CODE_DISABLE_*`) | link-out → B03A |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/captions/`<Note>`
callouts for newly-surfaced terms. One borderline non-glossary term surfaced — **"advisor strategy"** (the
linked `claude.com/blog/the-advisor-strategy` external reference) — but it is the same concept as the advisor
tool (notes 5/6), an external URL, not a vault term. **0 new b10b `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — b10b authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do these page concepts duplicate existing vault notes?)
was performed: `term_subagent`, `term_agent_orchestration`, `term_multi_agent`, `term_sandbox`,
`term_context_window`, `term_compaction`, `term_prompt_caching`, `term_agent_as_a_judge`,
`term_llm_as_a_judge`, `term_agentic_evaluation` all exist → linked, not recreated; no existing
`documentation/` note covers any of the four pages.

## Term-Note Authoring Requirements

**N/A for b10b** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (incl. G7/G8 discoverability) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim from source (note 3 trims 12→6 representative fences per Density Re-Assessment). One BB per note. Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; satisfies G7/G8):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_subagent.md` | notes 1, 3 | subagent term → workflow orchestration of subagents + subagent worktree isolation |
| `term_dictionary/term_agent_orchestration.md` | note 1 | orchestration term → script-driven workflow orchestration treatment |
| `term_dictionary/term_agent_as_a_judge.md` | notes 4, 5 | agent-as-judge term → `/goal` evaluator + advisor consultation |
| `term_dictionary/term_claude_code.md` | notes 1, 3, 4, 5 | product term → CC orchestration/control features (workflows, worktrees, goal, advisor) |
| `term_dictionary/term_multi_agent.md` | note 1 | multi-agent term → workflows coordinating many agents per run |

## Follow-up Recommendations

- After the 6 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 6 rows for `entry_claude_code_docs.md` (Orchestration & Control cluster); `/tessellum-check-broken-links`; confirm DB in-degree ≥1 for all 6 (G7/G8).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B10B, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read from `inbox/claude_code_docs/`; measured words match the master's figures (workflows 2,748 · worktrees 1,328 · goal 1,309 · advisor 1,691 = 7,076). No >1.5× under-estimate; the two documented splits (workflows, advisor) are driven by the cap + BB-type separation.
- **Notes**: 6 (concept 2, procedure 4) — matches master estimate exactly. workflows split into concept+procedure (>2500 cap); advisor split into concept+procedure (clean BB boundary); worktrees + goal each single procedure note.
- **Step 2d new-term scan**: 1 borderline surfaced ("advisor strategy", external blog ref) → same concept as advisor tool, not a vault term; **0 new b10b term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), G5/G7/G8 verification rows, Density code-fence trim decision for note 3.
- **28-item checklist**: PASS (term-note items N/A — b10b authors no terms; entry-point + undigested-terms inherited from master).
- **Status**: augmented and reviewed; set to `ready` after the 9-checkpoint self-review below.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 discoverability (inbound in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); b10b contributes 6 rows (Orchestration & Control cluster). |
| CP4 | Plan size ≤30 / split | ✅ PASS | 6 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches the master Format Definition (derived from existing `documentation/` notes); body uses `## Overview` / source-mirrored H2s / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | workflows (2,748w >cap) split; advisor split on BB boundary; worktrees code-fence trim (12→6) documented; all 6 notes 550–700w, ≤6 code — none borderline after splits. |
| CP7 | Source words measured (not guessed) | ✅ PASS | Re-measured 2026-06-13: workflows 2,748 = plan 2,748; worktrees 1,328; goal 1,309; advisor 1,691; total 7,076 = master figure. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | b10b authors 0 term notes; Undigested Terms Plan routes every page term (dedup across term_dictionary AND documentation/); Authoring Requirements inherited. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
