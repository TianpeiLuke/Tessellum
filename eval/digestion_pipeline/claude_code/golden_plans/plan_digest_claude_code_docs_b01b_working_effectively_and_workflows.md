---
title: Sub-Plan B01B — Claude Code Docs: Working Effectively & Workflows
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["quickstart", "best-practices", "common-workflows"]
---

# Sub-Plan B01B: Working Effectively & Workflows

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 3 "how to actually use it" pages: the first-session quickstart walkthrough, the best-practices guide
(the densest page in the corpus — 5,246 words), and the common-workflows recipe collection. P1 (Phase A)
— these establish the operating doctrine (verification loop, explore-plan-code, context discipline,
fan-out) that later feature sub-plans reference. The **verification loop** glossary term is owned here per
the master's Undigested Terms ownership map.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 3 pages, 9,171 measured words. **Planned: 8 notes.**

## Content Strategy

- **Prioritize**: the operating-doctrine arguments every later sub-plan links — verification loop,
  explore-then-plan-then-code, context discipline, fan-out/automation (P1).
- **Group**: best-practices (5.2Kw, 9 H2) MUST split by topic/BB — verify-work (argument) · explore-plan-code
  (procedure) · prompting (argument) · environment-setup (procedure, but every sub-item links its home
  sub-plan rather than re-teaching) · session-management + failure-patterns (argument) · automate-and-scale
  (procedure). quickstart (8 numbered steps) stays as ONE procedure note + folds its commands/tips.
  common-workflows (prompt recipes + 5 short link-out sections) becomes ONE recipe note.
- **Skip / link-out (own other sub-plans)**: install methods → setup B17; surfaces (web/desktop/IDE/Slack) →
  B12/B13; CLAUDE.md mechanics → memory B02B; permissions/auto-mode/sandbox → B05A/B05B; skills → B06;
  hooks → B07; MCP → B08; subagents/agent-teams → B10A; worktrees/goal/workflows → B10B;
  headless/routines/scheduled → B11; checkpointing/sessions → B02B; context-window/costs → B02A;
  plan mode → B05A; code-review/ultrareview → B13B; chrome screenshots → B13A. Referenced via links, never duplicated.
- **Glossary**: "Verification loop" is the one glossary term owned here — digested as a `cc_` doc-concept
  note (note 2), not a `term_dictionary` capture (Pattern B; see Undigested Terms Plan). "Turn" is folded
  into note 2 and linked.

## Source Pages (Measured 2026-06-13, re-read)

All 3 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| quickstart | /quickstart | 1,612 | 24 | 13 | 0 | procedure |
| best-practices | /best-practices | 5,246 | 14 | 9 | 17 | argument/procedure |
| common-workflows | /common-workflows | 2,313 | 41 | 8 | 6 | procedure |

> **H2 lists (document order):**
> - **quickstart**: Before you begin · Step 1 Install · Step 2 Log in · Step 3 Start your first session · Step 4 Ask your first question · Step 5 Make your first code change · Step 6 Use Git · Step 7 Fix a bug or add a feature · Step 8 Test out other common workflows · Essential commands · Pro tips for beginners · What's next? · Getting help
> - **best-practices**: (intro: the context-window constraint) · Give Claude a way to verify its work · Explore first, then plan, then code · Provide specific context in your prompts (H3 Provide rich content) · Configure your environment (H3 Write an effective CLAUDE.md, Configure permissions, Use CLI tools, Connect MCP servers, Set up hooks, Create skills, Create custom subagents, Install plugins) · Communicate effectively (H3 Ask codebase questions, Let Claude interview you) · Manage your session (H3 Course-correct early and often, Manage context aggressively, Use subagents for investigation, Rewind with checkpoints, Resume conversations) · Automate and scale (H3 Run non-interactive mode, Run multiple Claude sessions, Fan out across files, Run autonomously with auto mode, Add an adversarial review step) · Avoid common failure patterns · Develop your intuition · Related resources
> - **common-workflows**: Prompt recipes (H3 Understand new codebases, Fix bugs efficiently, Refactor code, Work with tests, Create pull requests, Handle documentation, Work in notes and non-code folders, Work with images, Reference files and directories, Run Claude on a schedule, Ask Claude about its capabilities) · Resume previous conversations · Run parallel sessions with worktrees · Plan before editing · Delegate research to subagents · Pipe Claude into scripts · Next steps

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **8 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_quickstart.md` | procedure | quickstart: Steps 1–8 + Essential commands + Pro tips + Getting help | 600 | First-session walkthrough (install → login → start → ask → edit → git → bug/feature → other workflows); essential shell/session commands table; beginner tips. Install methods → setup (B17); surfaces → B12/B13. |
| 2 | `cc_verification_loop.md` | argument | best-practices: intro context constraint + Give Claude a way to verify its work | 550 | Why "looks done" is unreliable; the verification loop (you-as-loop vs self-closing check); test/build/lint/screenshot/diff as readable signals; how-hard-it-gates ladder (prompt / `/goal` / Stop hook / second-opinion subagent); show-evidence rule. Owns the "Verification loop" glossary term. |
| 3 | `cc_explore_plan_code.md` | procedure | best-practices: Explore first, then plan, then code | 400 | The 4-phase workflow (Explore in plan mode → Plan → Implement → Commit); when to skip planning (one-sentence-diff rule); `Ctrl+G` plan editing. Plan mode mechanics → B05A. |
| 4 | `cc_effective_prompting.md` | argument | best-practices: Provide specific context + Provide rich content; common-workflows: Reference files and directories, Work with images | 600 | Specific-context prompting (scope task / point to sources / reference patterns / describe symptom); vague-prompt exception; rich content (`@` refs, paste images, URLs, pipe data); `@` file/dir/MCP-resource semantics. |
| 5 | `cc_configure_your_environment.md` | procedure | best-practices: Configure your environment (CLAUDE.md, permissions, CLI tools, MCP, hooks, skills, subagents, plugins) | 650 | The per-project setup checklist: `/init` CLAUDE.md, configure permissions, install CLI tools (`gh`/`aws`/`gcloud`), `claude mcp add`, set up hooks, create skills, custom subagents, install plugins — each a pointer to its home sub-plan (B02B/B05A/B08/B07/B06/B10A/B09), NOT re-taught here. |
| 6 | `cc_manage_your_session.md` | argument | best-practices: Communicate effectively + Manage your session + Avoid common failure patterns + Develop your intuition | 650 | Communicating (ask-senior-engineer questions, let-Claude-interview-you → SPEC.md, fresh session); session discipline (course-correct early, `/clear` between tasks, manage context, subagents for investigation, checkpoints, resume); 5 common failure patterns + fixes; develop-intuition caveats. Checkpoint/session mechanics → B02B. |
| 7 | `cc_automate_and_scale.md` | procedure | best-practices: Automate and scale (non-interactive, multiple sessions, fan-out, auto mode, adversarial review) | 600 | Horizontal scaling: `claude -p` non-interactive (output formats), parallel sessions (worktrees/desktop/web/agent-teams), fan-out loop with `--allowedTools`, auto mode for unattended runs, adversarial-review subagent step (`/code-review`). Each mechanism → its home sub-plan (B11/B10B/B10A/B05A/B13B). |
| 8 | `cc_workflow_recipes.md` | procedure | common-workflows: Prompt recipes (explore / fix bugs / refactor / tests / PRs / docs / notes-folders / capabilities) + Resume / Worktrees / Plan / Delegate / Pipe section pointers | 650 | Copy-paste prompt recipes for everyday tasks (codebase overview, find code, fix bugs, refactor, tests, PRs, docs, non-code folders, ask-about-capabilities) plus the resume/worktree/plan/subagent/pipe link-out summaries. Images/@-refs → note 4; schedule → B11. |

**Estimate: 8 notes** — procedure ×5 (notes 1,3,5,7,8), argument ×3 (notes 2,4,6). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 3 (9,171 words). New `cc_` notes: 8. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~4,700 (avg ~585/note). Code blocks: ≤4/note (recipe/command snippets, well under the 6 cap).
- **Building Block Distribution**: procedure ×5 (notes 1,3,5,7,8) · argument ×3 (notes 2,4,6). No concept/model/empirical_observation in this sub-plan (these are doctrine/recipe pages).

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_quickstart` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the hands-on getting-started walkthrough for the Claude Code CLI itself, so the product term is its definitional anchor.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The walkthrough has Claude find files, propose edits, run tests, and resolve git operations from natural-language asks — the autonomous-coding-agent behaviors this term defines.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Starting `claude` in a project directory boots the harness that wires tools/context/execution around the model; the quickstart is the first contact with that harness.
- [Skills](../../term_dictionary/term_skills.md) — The quickstart's "how do I create custom skills" example question and the `/` shortcut tip introduce skills as the first customization surface a beginner meets.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Step 5 ("Claude always asks permission before modifying files; you can approve individually or enable Accept-all") and the `Shift+Tab` permission-mode tip are exactly the graduated-trust permission model.
- [Cursor](../../term_dictionary/term_cursor.md) — Cursor is a comparable agentic coding tool; it contextualizes the CLI-first getting-started experience this quickstart contrasts against IDE-centric onboarding.

### 2. `cc_verification_loop` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The verification-loop doctrine is Claude Code's central operating principle; the note documents how the product's agentic loop closes on a check rather than on "looks done."
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — A readable pass/fail check is what lets the autonomous agent run unattended and self-correct, the defining capability this term covers — the note's "session you walk away from" claim.
- [TDD (Test-Driven Development)](../../term_dictionary/term_tdd.md) — The note's strongest verification signal is a test suite Claude runs and iterates against until green — the test-first feedback loop TDD formalizes.
- [LLM-as-a-Judge](../../term_dictionary/term_llm_as_a_judge.md) — The "second opinion" / verification-subagent gate (a fresh model re-checks the result so the agent doing the work isn't grading it) is the LLM-as-a-judge evaluation pattern.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — A build exit code / linter / pipeline gate is the deterministic check the note recommends, and the Stop-hook gate mirrors a CI quality gate that blocks completion until it passes.
- [Context Window](../../term_dictionary/term_context_window.md) — The note opens with the context-window-fills-fast constraint that motivates giving Claude a self-closing check (so you are not the verification loop, consuming attention as context grows).
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The Stop hook and verification subagent are harness-level mechanisms that gate when a turn may end, so the harness term grounds the note's "deterministic gate" tier.

### 3. `cc_explore_plan_code` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The explore→plan→implement→commit workflow is a Claude Code operating procedure built on its plan mode and tool loop, so the product term anchors the note.
- [Natural Planning Model](../../term_dictionary/term_natural_planning_model.md) — Separating research/planning from execution to avoid solving the wrong problem is the explicit planning-before-action discipline this term names.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The workflow runs phase 1 in plan mode (read-only, no edits) then switches modes to implement — the progressive-permission escalation graduated trust defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The procedure governs how the autonomous agent is steered (plan, then let it implement and verify against its own plan) rather than jumping straight to edits.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Exploring first to build accurate context before planning, and editing the plan in `Ctrl+G`, is deliberate context-engineering so the implementation phase starts from the right understanding.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Plan mode is a harness execution mode that restricts the tool set to read-only during exploration; the harness term grounds the mode-switching the procedure relies on.

### 4. `cc_effective_prompting` (7 term notes)
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — The note is a prompt-engineering guide for an agentic coding tool: scope the task, point to sources, reference patterns, describe symptoms — the precise-instruction craft this term defines.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Referencing files with `@`, pasting images, giving URLs, and piping data are all deliberate context-construction moves — supplying the right context, not just the right wording.
- [Prompt Optimization](../../term_dictionary/term_prompt_optimization.md) — The before/after prompt table (vague → specific) is a worked prompt-optimization exercise showing how rewording reduces correction rounds.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The `@`-reference, image-paste, and pipe mechanisms are Claude-Code-specific input affordances, so the product term grounds the rich-content half of the note.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Precise prompts reduce corrections because the agent acts autonomously across files; vague prompts cost more when the agent runs without supervision — the autonomy the term covers.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The `@server:resource` rich-content form fetches data from connected MCP servers, tying effective prompting to MCP-provided context this term defines.
- [Context Window](../../term_dictionary/term_context_window.md) — `@` references and pasted content load directly into the context window; the note's rich-content choices are framed by their context-window cost.

### 5. `cc_configure_your_environment` (8 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note is the per-project setup checklist for Claude Code itself (`/init`, permissions, CLI tools, MCP, hooks, skills, subagents, plugins), so the product term is its anchor.
- [Skills](../../term_dictionary/term_skills.md) — "Create skills" is one checklist item: `SKILL.md` files in `.claude/skills/` give Claude domain knowledge and reusable workflows — exactly what this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — "Create custom subagents" defines specialized assistants in `.claude/agents/` with their own tools and context — the subagent mechanism this term covers.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — "Connect MCP servers" (`claude mcp add`) is a checklist step wiring external tools like Notion/Figma/databases — the MCP integration this term defines.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — "Configure permissions" (auto mode, `/permissions` allowlists, `/sandbox`) is the graduated-trust permission tuning this term names, central to reducing interruptions.
- [Context Window](../../term_dictionary/term_context_window.md) — The note's CLAUDE.md guidance ("loaded every session, keep it short, route sometimes-relevant knowledge to skills") is driven by the context-window budget this term covers.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The eight setup levers (CLAUDE.md, permissions, CLI, MCP, hooks, skills, subagents, plugins) all configure the harness around the model; the harness term grounds the checklist.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Hooks ("actions that must happen every time with zero exceptions") and CLI-tool access make the autonomous agent's unattended work deterministic and effective — capabilities this term covers.

### 6. `cc_manage_your_session` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note covers Claude-Code session controls (`/clear`, `/compact`, `/rewind`, `--continue`, `--resume`, `Esc`), so the product term anchors the session-management doctrine.
- [Context Window](../../term_dictionary/term_context_window.md) — Every tactic here (clear between tasks, compact aggressively, subagents for investigation) exists to manage the filling context window the note calls the fundamental constraint.
- [Compaction](../../term_dictionary/term_compaction.md) — "Manage context aggressively" details auto-compaction, `/compact <instructions>`, and CLAUDE.md compaction preservation rules — the compaction mechanism this term defines.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — "Rewind with checkpoints" (every prompt snapshots files; `/rewind` restores conversation/code/both) is the periodic-checkpoint-for-recovery discipline this term names.
- [Subagent](../../term_dictionary/term_subagent.md) — "Use subagents for investigation" delegates research to a separate context window that reports summaries, keeping the main conversation clean — the subagent capability this term covers.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The failure patterns (kitchen-sink session, over-specified CLAUDE.md, infinite exploration) and their fixes are context-engineering hygiene — curating what stays in the window.
- [Memento Pattern](../../term_dictionary/term_memento_pattern.md) — Checkpoints snapshot prior state so any change is reversible without external processes — the capture-and-restore-state design the memento pattern formalizes.

### 7. `cc_automate_and_scale` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents Claude Code's horizontal-scaling modes (`claude -p`, parallel sessions, fan-out, auto mode), so the product term anchors the automation doctrine.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Non-interactive `-p`, fan-out loops, and auto mode are how the autonomous agent runs unattended at scale — the unsupervised operating mode this term defines.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — "Run multiple Claude sessions" and the Writer/Reviewer pattern coordinate several independent Claude instances on shared work — the multi-agent-systems pattern this term defines.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — Agent teams (automated coordination with shared tasks, messaging, a team lead) and the fan-out loop are orchestration patterns this term enumerates.
- [Subagent](../../term_dictionary/term_subagent.md) — The adversarial-review step runs a reviewer in a fresh subagent context that sees only the diff, returning gaps to the implementing session — the subagent verification pattern this term covers.
- [LLM-as-a-Judge](../../term_dictionary/term_llm_as_a_judge.md) — The adversarial-review subagent ("a fresh model evaluates the result on its own terms; tell it to flag only correctness gaps") is the LLM-as-a-judge evaluation pattern, including its over-flagging caveat.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Auto mode (a classifier blocks scope escalation while letting routine work proceed) and `--allowedTools` scoping for unattended fan-out are the graduated-trust controls this term defines.

### 8. `cc_workflow_recipes` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note is a collection of Claude Code prompt recipes for everyday tasks (explore, debug, refactor, test, PR, docs), so the product term anchors it.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Each recipe drives the agent to locate code, apply changes, and run/verify tests from a short natural-language ask — the autonomous-coding behavior this term defines.
- [TDD (Test-Driven Development)](../../term_dictionary/term_tdd.md) — The "Work with tests" recipe (identify untested code → scaffold → edge cases → run and fix) and the "write a failing test then fix it" bug recipe are test-driven loops this term formalizes.
- [CI/CD](../../term_dictionary/term_ci_cd.md) — The "Create pull requests" recipe (`gh pr create`, session auto-linked to the PR) and "Pipe Claude into scripts" feed into the CI/CD review pipeline this term covers.
- [Subagent](../../term_dictionary/term_subagent.md) — The "Delegate research to subagents" recipe explores a large codebase in a separate context window and returns only findings — the subagent capability this term defines.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — Every recipe is a reusable prompt pattern (scope the ask, use domain language, request a glossary), which is applied prompt engineering for an agentic tool.

## Section Coverage Map

```
quickstart.md
├── Before you begin (prereqs) ─────────── → note 1 (cc_quickstart)
├── Step 1 Install ─────────────────────── → linked out (setup B17); summarized in note 1
├── Step 2 Log in ──────────────────────── → note 1 (→ authentication B14B)
├── Step 3 Start your first session ────── → note 1
├── Step 4 Ask your first question ──────── → note 1
├── Step 5 Make your first code change ──── → note 1
├── Step 6 Use Git with Claude Code ─────── → note 1
├── Step 7 Fix a bug or add a feature ───── → note 1
├── Step 8 Test out other common workflows  → note 1 (→ note 8 recipes)
├── Essential commands (tables) ─────────── → note 1 (full ref → CLI B03B)
├── Pro tips for beginners ──────────────── → note 1
├── What's next? (cards) ────────────────── → note 1 (links to B01A/this sub-plan)
└── Getting help ───────────────────────── → note 1
best-practices.md
├── (intro) context-window constraint ───── → note 2 (cc_verification_loop) intro (→ B02A context-window)
├── Give Claude a way to verify its work ── → note 2 (cc_verification_loop)
├── Explore first, then plan, then code ─── → note 3 (cc_explore_plan_code)
├── Provide specific context (+ rich) ───── → note 4 (cc_effective_prompting)
├── Configure your environment ──────────── → note 5 (cc_configure_your_environment)
│   ├── Write an effective CLAUDE.md ────── → note 5 (mechanics → memory B02B)
│   ├── Configure permissions ──────────── → note 5 (→ permissions B05A / sandbox B05B)
│   ├── Use CLI tools ──────────────────── → note 5
│   ├── Connect MCP servers ────────────── → note 5 (→ MCP B08A)
│   ├── Set up hooks ───────────────────── → note 5 (→ hooks B07B)
│   ├── Create skills ──────────────────── → note 5 (→ skills B06)
│   ├── Create custom subagents ────────── → note 5 (→ subagents B10A)
│   └── Install plugins ────────────────── → note 5 (→ plugins B09A)
├── Communicate effectively ─────────────── → note 6 (cc_manage_your_session)
│   ├── Ask codebase questions ─────────── → note 6 (→ note 8 recipes)
│   └── Let Claude interview you ───────── → note 6
├── Manage your session ─────────────────── → note 6
│   ├── Course-correct early and often ─── → note 6
│   ├── Manage context aggressively ────── → note 6 (→ compaction B02A / checkpointing B02B)
│   ├── Use subagents for investigation ── → note 6
│   ├── Rewind with checkpoints ────────── → note 6 (→ checkpointing B02B)
│   └── Resume conversations ───────────── → note 6 (→ sessions B02B)
├── Automate and scale ──────────────────── → note 7 (cc_automate_and_scale)
│   ├── Run non-interactive mode ───────── → note 7 (→ headless B11)
│   ├── Run multiple Claude sessions ───── → note 7 (→ worktrees B10B / agent-teams B10A / web B12B)
│   ├── Fan out across files ───────────── → note 7
│   ├── Run autonomously with auto mode ── → note 7 (→ permission-modes B05A)
│   └── Add an adversarial review step ─── → note 7 (→ code-review B13B / sub-agents B10A)
├── Avoid common failure patterns ───────── → note 6
├── Develop your intuition ──────────────── → note 6
└── Related resources (links) ───────────── → notes 2/5/8 (links)
common-workflows.md
├── Prompt recipes ──────────────────────── → note 8 (cc_workflow_recipes)
│   ├── Understand new codebases ───────── → note 8 (→ large-codebases B15A)
│   ├── Fix bugs efficiently ───────────── → note 8
│   ├── Refactor code ──────────────────── → note 8
│   ├── Work with tests ────────────────── → note 8
│   ├── Create pull requests ───────────── → note 8
│   ├── Handle documentation ───────────── → note 8
│   ├── Work in notes and non-code folders  → note 8
│   ├── Work with images ───────────────── → note 4 (rich content)
│   ├── Reference files and directories ── → note 4 (@-refs)
│   ├── Run Claude on a schedule (table) ─ → linked out (routines/scheduled B11)
│   └── Ask Claude about its capabilities  → note 8
├── Resume previous conversations ───────── → note 8 (→ sessions B02B)
├── Run parallel sessions with worktrees ── → note 8 (→ worktrees B10B / agent-view B10A)
├── Plan before editing ─────────────────── → note 8 (→ permission-modes B05A)
├── Delegate research to subagents ──────── → note 8 (→ sub-agents B10A)
├── Pipe Claude into scripts ────────────── → note 8 (→ headless B11)
└── Next steps (cards) ──────────────────── → note 8 (links)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| best-practices (5,246w >2500, 9 H2 mixed BB) | notes 2,3,4,5,6,7 + link-outs | far over the density cap; distinct BB/topics — verify-work (argument) · explore-plan-code (procedure) · prompting (argument) · environment-setup (procedure) · session-management+failures+intuition (argument) · automate-and-scale (procedure). Each environment/automation sub-item points to its home sub-plan rather than re-teaching. |
| quickstart (1,612w, 8 steps + commands + tips) | note 1 (single procedure) | one cohesive first-session procedure; under caps; install methods link out to B17, surfaces to B12/B13. |
| common-workflows (2,313w, recipes + 5 short link-out sections) | note 8 + 2 sections folded to note 4 | recipes are one procedure note; images + `@`-refs belong with the prompting/rich-content note 4 (avoids duplication); schedule table links out to B11. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_quickstart | procedure | 600 | 4 | ✅ |
| 2 | cc_verification_loop | argument | 550 | 2 | ✅ |
| 3 | cc_explore_plan_code | procedure | 400 | 4 | ✅ |
| 4 | cc_effective_prompting | argument | 600 | 3 | ✅ |
| 5 | cc_configure_your_environment | procedure | 650 | 4 | ✅ |
| 6 | cc_manage_your_session | argument | 650 | 2 | ✅ |
| 7 | cc_automate_and_scale | procedure | 600 | 5 | ✅ |
| 8 | cc_workflow_recipes | procedure | 650 | 4 | ✅ |

No note approaches the caps. Source code blocks are short command/recipe snippets; each note selects a
representative subset (≤5) rather than copying every fenced example — within the ≤6 cap and ≤400 lines.
No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_quickstart cc_verification_loop cc_explore_plan_code cc_effective_prompting cc_configure_your_environment cc_manage_your_session cc_automate_and_scale cc_workflow_recipes"
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

Single phase (8 notes, all P1). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 8 notes RECEIVES ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | re-verify in-degree ≥1 after reindex; no graph-island | DB in-degree query post-reindex |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 8 rows** under a "Foundations / Working effectively" cluster + increments the
BB-distribution counts (procedure +5, argument +3).

## Undigested Terms Plan (Step 2d)

b01b creates **no new `term_dictionary` notes** — the only glossary term these pages own ("Verification
loop") is digested as a b01b `cc_` doc-concept note (note 2, per the master's ownership map); every other
term is an existing substantive term note (link) or owned by its home sub-plan (Pattern B):

| Term (from pages) | Disposition |
|---|---|
| Verification loop | note 2 `cc_verification_loop` (doc concept — owned by B01B per master) |
| Turn | folded into note 2 / linked to glossary (B01A) |
| Plan mode | linked out to B05A (`permission-modes`); summarized in note 3 |
| CLAUDE.md / Auto memory | linked out to B02B (`memory`); referenced in note 5 |
| Permission allowlist / Auto mode | linked out to B05A (`permissions`/`permission-modes`); referenced in notes 5/7 |
| Sandboxing | link `term_sandbox` (exists) + B05B |
| Non-interactive / headless mode | linked out to B11 (`headless`); referenced in note 7 |
| Worktree | linked out to B10B (`worktrees`); referenced in notes 7/8 |
| Agent teams | linked out to B10A (`agent-teams`); referenced in note 7 |
| Checkpoint / Session | linked out to B02B (`checkpointing`/`sessions`); referenced in note 6 |
| Skill / Hook / Plugin / Subagent / MCP | existing term notes (link) + home sub-plans (B06/B07/B09/B10A/B08) |
| Context window / Compaction | existing term notes (link) + B02A |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 3 pages scanning emphasis/tables/callouts/tips
for newly-surfaced non-glossary terms. Candidates surfaced and resolved:
- **"`/goal` condition" / goal evaluator** — owned by B10B (`goal.md`); referenced in note 2, **not** captured here.
- **"dynamic workflow"** — owned by B10B (`workflows.md`); referenced in note 2, not captured here.
- **"`/btw` side-question overlay"** — owned by B04A (`interactive-mode.md`); referenced in note 6, not captured here.
- **"code intelligence plugin / LSP"** — owned by B09 (`discover-plugins#code-intelligence`) / B03B; referenced in notes 5/8, not captured here.
- **"AskUserQuestion tool"** — a built-in tool; owned by B03B (`tools-reference`); referenced in note 6, not captured here.

**0 new B01B `term_dictionary` captures.** All five are owned by other sub-plans (no orphan; consistent
with the master's corpus-wide ownership map).

**Collision / dedup check (cross-cutting term_dictionary AND documentation/):** "Verification loop" was
checked against both dirs via `bm25_search` + `dense_search` + filename grep — no existing `term_verification*`
note and no existing `cc_*`/documentation note covers it (target `claude_code/` folder does not yet exist;
recreated: `term_claude_code`, `term_mcp`, `term_subagent`, `term_context_window`, `term_compaction`,
`term_sandbox`, `term_skills`, `term_agent_harness`, `term_autonomous_coding_agents`,
`term_regular_checkpointing`, `term_graduated_trust`, `term_context_engineering`.

## Term-Note Authoring Requirements

**N/A for b01b** — it authors zero `term_dictionary` notes (all routed above; "Verification loop" becomes a
`cc_` doc-concept note, not a term note). The full requirements (YAML, file naming, required H2 sections,
and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (incl. G7/G8 discoverability) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim where copied; select a representative ≤5 subset per note (do not copy every fenced
  example). One BB per note. Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 — each new note
receives ≥1 inbound link from OUTSIDE `claude_code/`):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 2, 8 | product term → quickstart / verification-loop doctrine / recipe collection |
| `term_dictionary/term_autonomous_coding_agents.md` | notes 2, 7 | autonomy term → verification-loop + automate-and-scale doctrine |
| `term_dictionary/term_prompt_engineering.md` | note 4 | prompt-engineering term → CC effective-prompting guide |
| `term_dictionary/term_regular_checkpointing.md` | note 6 | checkpointing term → CC session-management rewind doctrine |
| `term_dictionary/term_tdd.md` | notes 2, 8 | TDD term → verification-loop + test-workflow recipes |
| `term_dictionary/term_graduated_trust.md` | notes 3, 5 | permission-mode term → explore-plan-code + configure-permissions |
| `documentation/tutorials/tutorial_claude_code_getting_started.md` | notes 1, 8 | getting-started tutorial → quickstart + workflow recipes (cross-folder inbound) |

Every one of the 8 notes appears as a target above ⇒ G7/G8 in-degree ≥1 satisfied by construction.

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above (verify DB
  in-degree ≥1 for all 8 — G7/G8); queue the 8 rows for `entry_claude_code_docs.md`;
  `/tessellum-check-broken-links`.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B01B, 2026-06-13)

- **Source re-read (Step 2)**: all 3 pages re-read from `inbox/claude_code_docs/`; measured words match the
  master's figures (quickstart 1,612 · best-practices 5,246 · common-workflows 2,313 = 9,171). best-practices
  at 5,246w is >2× the 2,500 cap ⇒ mandatory split into 6 notes (documented in Split Decisions); no other
  re-split forced.
- **Notes**: 8 (procedure 5, argument 3) — matches the master estimate. The best-practices split keeps each
  resulting note single-BB and well under caps.
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard —
  6–8 term notes per note (19 distinct `term_dictionary/` terms), each with a per-link relevancy statement.
  discarded (e.g. `term_adversarial_attack`, `term_gan`, `term_deny_first`, `term_write_ahead_log`,
- **Step 2d new-term scan**: 5 surfaced (`/goal`, dynamic workflow, `/btw`, code intelligence/LSP,
  AskUserQuestion) → all owned by other sub-plans (B10B/B04A/B09/B03B); **0 new B01B term captures**.
- **Dedup (Step 2b, cross-dir)**: ran `bm25` + `dense` + filename grep across `term_dictionary/` AND
  `documentation/`; no existing note duplicates any of the 8 planned `cc_` notes (target folder not yet
  created); "Verification loop" has no existing term/doc home → created as note 2.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), Inlinks (8 rows, every note a target ⇒ G7/G8 by construction), G8 gate row.
- **28-item checklist**: PASS (term-note items N/A — B01B authors no `term_dictionary` notes; entry-point +
  undigested-terms inherited from master).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7 + G8 discoverability (inbound in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B01B contributes 8 rows. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches existing `documentation/` notes exactly (master Format Definition, verbatim); body uses `## Overview` / source-mirrored H2s / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | best-practices (5,246w) split into 6; all 8 resulting notes 400–650w, ≤5 code — none borderline. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` 2026-06-13: quickstart 1,612 · best-practices 5,246 · common-workflows 2,313 = 9,171. (Master listed 9,171 total; per-page measured here.) |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B01B authors 0 term notes; Undigested Terms Plan routes every term (incl. "Verification loop" → note 2); Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new term slugs). Collision/dedup check documented: "Verification loop" has no existing `term_*`/`cc_*`/doc home (checked both dirs); 12 existing terms linked, not recreated. |
| CP9 | Discoverability (G7/G8 inbound in-degree ≥1) | ✅ PASS | Inlinks table lists ≥1 cross-folder inbound link to each of the 8 notes (every note is a target); G7/G8 satisfied by construction, verified by DB in-degree at finalization. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
