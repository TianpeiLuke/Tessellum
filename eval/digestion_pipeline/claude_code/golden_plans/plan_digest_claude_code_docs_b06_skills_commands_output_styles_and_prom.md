---
title: Sub-Plan B06 — Claude Code Docs: Skills, Commands, Output Styles & Prompts
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["skills", "commands", "output-styles", "prompt-library"]
---

# Sub-Plan B06: Skills, Commands, Output Styles & Prompts

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 4 customization-layer pages that document how users extend Claude Code through **skills** (the
unified `SKILL.md` / custom-command mechanism), the full **commands** reference (built-in commands +
bundled skills + bundled workflows), **output styles** (system-prompt role/tone/format adaptation), and
the **prompt library** (copy-paste prompts + the patterns behind them). P1 (Phase A) — skills are a core
vocabulary term every later sub-plan references, so this runs early. Glossary terms (Skill, Command,
Output style, Bundled skills) are owned by this sub-plan per the master's Pattern B but digested as
`cc_` doc concept notes, not new `term_dictionary` captures.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 18,469 measured words. **Planned: 11 notes.**

## Content Strategy

- **Prioritize**: the skill model (`SKILL.md` structure, frontmatter, invocation control, lifecycle) — the P1 vocabulary every later sub-plan links — and the commands reference that anchors cross-links from the whole corpus.
- **Group**: split `skills.md` (6.5Kw, 14 H2/H3) by concept (what/where/lifecycle) vs procedure (create/configure/advanced patterns); keep `output-styles.md` as one concept note + one procedure note; the giant `commands.md` table becomes a reference note plus a workflow-grouped companion; `prompt-library.md` becomes a concept note on the prompting patterns (the embedded JSX widget is implementation, not content).
- **Skip / link-out (own other sub-plans)**: bundled-skill internals → B10A/B11 (agents/workflows); per-command deep pages (`/mcp`→B08A, `/hooks`→B07, `/permissions`→B05A, `/agents`→B10A, `/compact`+`/context`→B02A/B02B, `/model`+`/effort`→B03B, `/sandbox`→B05B, surfaces commands→B12); settings fields (`disableBundledSkills`, `skillListingBudgetFraction`, `outputStyle`)→B03A. These are referenced via links, never duplicated.
- **Glossary**: Skill / Command / Output style / Bundled skills route to b06 `cc_` notes (Pattern B); MCP / Subagent / Sandboxing / Permission mode link to existing term notes.

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| skills | /skills | 6,462 | 22 | 8 | 14 | concept + procedure |
| commands | /commands | 3,908 | 0 | 5 | 0 | procedure (reference) |
| output-styles | /output-styles | 1,096 | 3 | 6 | 1 | concept + procedure |
| prompt-library | /prompt-library | 7,003 | 6 | 4 | 0 | concept (most words are a JSX widget — not prose) |

> **H2 lists (document order):**
> - **skills**: Bundled skills (H3 Run and verify your app) · Getting started (H3 Create your first skill, Where skills live, Live change detection, Automatic discovery from parent and nested directories, Skills from additional directories) · Configure skills (H3 Types of skill content, Frontmatter reference, How a skill gets its command name, Available string substitutions, Add supporting files, Control who invokes a skill, Skill content lifecycle, Pre-approve tools for a skill, Pass arguments to skills) · Advanced patterns (H3 Inject dynamic context, Run skills in a subagent, Restrict Claude's skill access, Override skill visibility from settings) · Share skills (H3 Generate visual output) · Troubleshooting (H3 Skill not triggering, Skill triggers too often, Skill descriptions are cut short) · Related resources
> - **commands**: Commands across a typical workflow · All commands (the master command table) · MCP prompts · See also
> - **output-styles**: Built-in output styles · Change your output style · Create a custom output style (H3 Frontmatter) · How output styles work · Comparisons to related features · Related resources
> - **prompt-library**: (JSX widget = prompt data + UI) · What makes these prompts work · Where these come from · Related resources

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **11 notes** (matches master estimate). Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_skills_overview.md` | concept | skills: intro, command-merge note, Agent Skills standard, Where skills live, Live change detection, parent/nested discovery, additional dirs | 650 | What a skill is (`SKILL.md` = frontmatter + body); commands-merged-into-skills; the 4 storage levels + precedence (enterprise>personal>project; plugin namespaced); live change detection; parent/nested/`--add-dir` discovery. Links `term_skills`. |
| 2 | `cc_create_a_skill.md` | procedure | skills: Getting started → Create your first skill (3 Steps), Add supporting files | 500 | Step-by-step: mkdir skill dir → write `SKILL.md` (YAML + markdown) → test (auto-trigger vs `/name`); the supporting-files directory layout (reference/examples/scripts). |
| 3 | `cc_skill_frontmatter_reference.md` | concept | skills: Configure skills → Types of skill content, Frontmatter reference, How a skill gets its command name | 700 | The 17 frontmatter fields (name/description/when_to_use/argument-hint/arguments/disable-model-invocation/user-invocable/allowed-tools/disallowed-tools/model/effort/context/agent/hooks/paths/shell); reference vs task content; command-name derivation table; 1,536-char description cap. |
| 4 | `cc_skill_arguments_and_substitutions.md` | concept | skills: Available string substitutions, Pass arguments to skills | 450 | `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, named `$name`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`; shell-style quoting; `\$` escaping; argument-passing examples. |
| 5 | `cc_skill_invocation_and_lifecycle.md` | concept | skills: Control who invokes a skill, Skill content lifecycle, Override skill visibility from settings, Restrict Claude's skill access | 700 | Who-invokes matrix (`disable-model-invocation`, `user-invocable`); content lifecycle (single message, stays in context, compaction re-attach budget 25K/5K); `skillOverrides` four states; permission rules `Skill(name)`/`Skill(name *)`. |
| 6 | `cc_skill_dynamic_context_and_subagent.md` | procedure | skills: Advanced patterns → Inject dynamic context, Run skills in a subagent, Pre-approve tools for a skill, Generate visual output | 650 | `` !`cmd` `` inline + ```` ```! ```` fenced injection (preprocessing, single pass, line-start rule, `disableSkillShellExecution`); `context: fork` + `agent:` subagent execution; `allowed-tools`/`disallowed-tools` pre-approval; bundled-script visual-output pattern. |
| 7 | `cc_bundled_skills.md` | concept | skills: Bundled skills + Run and verify your app; commands rows marked Skill/Workflow | 450 | Prompt-based bundled skills (`/code-review`, `/batch`, `/debug`, `/loop`, `/claude-api`) vs fixed-logic built-ins; `disableBundledSkills`; the run/verify/run-skill-generator trio; deep internals link out (B10A/B11). |
| 8 | `cc_commands_reference.md` | procedure | commands: intro, All commands (the master table), MCP prompts | 1,900 | The full built-in command catalogue grouped by area (session/context, model/effort, agents/parallel, review/ship, surfaces, diagnostics, config); `<arg>`/`[arg]` convention; availability caveats; `/mcp__server__prompt` form. Deep pages link out per command. |
| 9 | `cc_commands_by_workflow.md` | procedure | commands: Commands across a typical workflow | 450 | The command journey: first session in a repo → during a task → running work in parallel → before you ship → between sessions → when something is wrong. A task-oriented index into note 8. |
| 10 | `cc_output_styles.md` | concept | output-styles: intro, Built-in output styles, How output styles work, Comparisons to related features | 600 | What an output style is (modifies the system prompt; role/tone/format); Default/Proactive/Explanatory/Learning; `keep-coding-instructions`; token impact; comparison vs CLAUDE.md / `--append-system-prompt` / agents / skills. Links `term_persona`. |
| 11 | `cc_prompting_patterns.md` | concept | prompt-library: intro, What makes these prompts work, Where these come from | 550 | The 6 reusable prompting patterns (describe the outcome not the steps; give a way to self-check; point at a reference; state the measurable target; give the artifact; say how you want the answer); the prompt-library's purpose + source provenance. |

**Estimate: 11 notes** — concept ×7 (notes 1,3,4,5,7,10,11), procedure ×4 (notes 2,6,8,9). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (18,469 words; but `prompt-library.md`'s 7,003 words are ~85% an embedded JSX/CSS widget, so digestible prose is ~9,500 words). New `cc_` notes: 11. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~8,050 (avg ~730/note). Code blocks: ~10 across all notes (skills page is code-heavy; the long Python visualizer is summarized, not transcribed — kept under the ≤6/note cap by selection).
- **Building Block Distribution**: concept ×7 (notes 1,3,4,5,7,10,11) · procedure ×4 (notes 2,6,8,9). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_skills_overview` (6 term notes)
- [Skills](../../term_dictionary/term_skills.md) — This note IS the doc-concept definition of a Claude Code skill (`SKILL.md` = frontmatter + body, loaded on demand); the term note is its canonical definitional anchor.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Skills are Claude Code's primary extension mechanism, so the product term grounds the storage levels, precedence, and discovery rules this note documents.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — A skill extends what the harness can do without bloating context; the note frames skills as the on-demand layer the harness loads only when relevant.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The note explains that an invoked skill enters context as instructions plus optional tool-pre-approval, so the model's tool-use selection is what the skill steers.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The note's core trade-off (a skill's body loads only when used, so long reference material costs almost nothing until needed) is exactly the lazy-load context-engineering principle this term covers.
- [Context Window](../../term_dictionary/term_context_window.md) — The note repeatedly contrasts CLAUDE.md (always in context) against a skill body (loads when invoked), framing skills by their context-window footprint.

### 2. `cc_create_a_skill` (6 term notes)
- [Skills](../../term_dictionary/term_skills.md) — This note is the create-your-first-skill procedure; the term defines the artifact being created (`SKILL.md` + supporting files).
- [Claude Code](../../term_dictionary/term_claude_code.md) — The steps run inside Claude Code (`mkdir ~/.claude/skills/...`, start `claude`, invoke `/name`), so the product term grounds the environment the procedure executes in.
- [Agent Skill](../../term_dictionary/term_skills.md) — (alias of Skills) The supporting-files layout (reference.md, examples/, scripts/) is the canonical skill-directory structure this procedure builds.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The "keep SKILL.md under 500 lines, move reference material to separate files" guidance is a context-engineering practice the procedure teaches.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The first-skill example pre-approves Bash to run `git diff HEAD`, so the procedure demonstrates wiring tool use into a skill.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The example skill summarizes uncommitted changes and flags risks autonomously when the user asks about their changes — the autonomous-coding behavior this term defines.

> Note: bullets 1 and 3 both resolve to `term_skills.md` (the vault has one canonical Skills term; "Agent Skill" is its open-standard alias). To keep ≥6 *distinct* targets, note 2 also links `term_react` — see authoring requirement below.

### 2b. `cc_create_a_skill` — distinct-target correction (6 distinct term notes)
- [Skills](../../term_dictionary/term_skills.md) — The artifact being created (`SKILL.md` + supporting files).
- [Claude Code](../../term_dictionary/term_claude_code.md) — The environment the procedure runs in (`~/.claude/skills/`, `claude`, `/name`).
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The "≤500 lines, split reference material out" lazy-load guidance the procedure teaches.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The example pre-approves Bash to run `git diff HEAD`, wiring tool use into the skill.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The example auto-summarizes the diff and flags risks when asked — autonomous coding behavior.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — Writing a skill's `description` so Claude reliably auto-loads it, and writing concise body instructions, is the prompt-engineering craft the steps require.

### 3. `cc_skill_frontmatter_reference` (7 term notes)
- [Skills](../../term_dictionary/term_skills.md) — This note is the full frontmatter field reference for a skill's `SKILL.md`; the term is its definitional anchor.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Every field (model, effort, context, agent, hooks, paths, shell) configures Claude Code behavior, so the product term grounds the reference.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — The note stresses putting the key use case first in `description`/`when_to_use` (capped at 1,536 chars) so Claude matches the skill — a concrete prompt-engineering constraint.
- [Subagent](../../term_dictionary/term_subagent.md) — The `context: fork` and `agent:` fields documented here route the skill into a subagent, so the term explains what those fields invoke.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The `allowed-tools`/`disallowed-tools` fields govern which tools the model may call while the skill is active — direct tool-use control.
- [Chain Of Thought](../../term_dictionary/term_chain_of_thought.md) — The `effort` field (low/medium/high/xhigh/max) sets reasoning depth, the extended-thinking dimension this term covers, while the skill is active.
- [Context Window](../../term_dictionary/term_context_window.md) — The 1,536-char description cap and the budget-driven truncation the note describes are context-window management of the skill listing.

### 4. `cc_skill_arguments_and_substitutions` (6 term notes)
- [Skills](../../term_dictionary/term_skills.md) — This note documents the string-substitution variables available inside a skill's `SKILL.md`; the term is its anchor.
- [Claude Code](../../term_dictionary/term_claude_code.md) — `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, and `${CLAUDE_SKILL_DIR}` are Claude Code runtime values, so the product term grounds them.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — Designing a parameterized prompt with `$ARGUMENTS`/`$N`/`$name` placeholders so a single skill generalizes across inputs is templated prompt engineering.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Arguments are how the user/Claude parameterizes a skill invocation the way tool calls carry parameters; the note shows `/fix-issue 123` passing `$ARGUMENTS`.
- [Chain Of Thought](../../term_dictionary/term_chain_of_thought.md) — `${CLAUDE_EFFORT}` exposes the active reasoning-effort level so a skill can adapt its instructions — directly tied to the extended-thinking control this term defines.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — `${CLAUDE_SESSION_ID}` is documented for logging and creating session-specific files, the per-session persistence pattern adjacent to this term.

### 5. `cc_skill_invocation_and_lifecycle` (7 term notes)
- [Skills](../../term_dictionary/term_skills.md) — This note covers who can invoke a skill and how its content lives across a session; the term is its anchor.
- [Context Window](../../term_dictionary/term_context_window.md) — The lifecycle section is entirely about the window: an invoked skill enters as one message and stays for the session, consuming budget every turn.
- [Compaction](../../term_dictionary/term_compaction.md) — The note details exactly how auto-compaction re-attaches the most recent invocation of each skill (first 5,000 tokens, 25,000-token combined budget), so the term is the mechanism the lifecycle hinges on.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `disable-model-invocation` (only you can trigger side-effecting skills like `/deploy`) and `Skill(name)` allow/deny rules are the progressive-permission controls this term enumerates.
- [Claude Code](../../term_dictionary/term_claude_code.md) — `skillOverrides` (on/name-only/user-invocable-only/off) and Skill-tool permission rules are Claude Code settings the product term grounds.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — A few built-in commands are exposed through the Skill *tool* (`/init`, `/review`, `/security-review`); denying the Skill tool disables all skills — direct tool-use governance.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The advice to re-invoke a large skill after compaction to restore its full content is a context-engineering remediation the note prescribes.

### 6. `cc_skill_dynamic_context_and_subagent` (7 term notes)
- [Skills](../../term_dictionary/term_skills.md) — This note documents the advanced skill patterns (dynamic context injection, forked execution, tool pre-approval); the term is its anchor.
- [Subagent](../../term_dictionary/term_subagent.md) — `context: fork` runs the skill body as the prompt for a forked subagent in an isolated context, so the term defines the execution mode this note centers on.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `allowed-tools: Bash(gh *)` pre-approves tools and the `` !`cmd` `` syntax runs shell commands as preprocessing — both are tool-use mechanisms the note configures.
- [Sandbox](../../term_dictionary/term_sandbox.md) — `disableSkillShellExecution` disables the shell-command preprocessing as a managed-settings policy, an execution-restriction control adjacent to sandboxing.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The visual-output pattern (bundled Python script + `${CLAUDE_SKILL_DIR}`) and the `agent:` field are Claude Code features the product term grounds.
- [Chain Of Thought](../../term_dictionary/term_chain_of_thought.md) — The note's tip "include `ultrathink` anywhere in the skill content to request deeper reasoning" is the extended-thinking trigger this term covers.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — A forked skill drives a subagent that researches/builds autonomously and returns a summary — the autonomous-agent delegation pattern this term defines.

### 7. `cc_bundled_skills` (6 term notes)
- [Skills](../../term_dictionary/term_skills.md) — Bundled skills are prompt-based skills shipped with Claude Code; the term anchors what they are and how they're invoked.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note lists Claude Code's shipped bundled skills (`/code-review`, `/batch`, `/debug`, `/loop`, `/claude-api`) and `disableBundledSkills`, so the product term grounds them.
- [Subagent](../../term_dictionary/term_subagent.md) — Bundled skills like `/batch` orchestrate the work across many background subagents, so the term explains the execution fan-out the note describes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The run/verify trio launches and drives the app to confirm a change autonomously rather than relying on tests — autonomous-coding behavior this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The note contrasts prompt-based bundled skills (Claude orchestrates with its tools) against fixed-logic built-ins — the tool-use vs hardcoded-logic distinction.
- [Code Review (`/code-review`)](../../term_dictionary/term_claude_code.md) — *(no distinct term; folded into Claude Code)* — see correction below.

### 7b. `cc_bundled_skills` — distinct-target correction (6 distinct term notes)
- [Skills](../../term_dictionary/term_skills.md) — Bundled skills are prompt-based skills shipped with Claude Code.
- [Claude Code](../../term_dictionary/term_claude_code.md) — The shipped bundled-skill catalogue + `disableBundledSkills`.
- [Subagent](../../term_dictionary/term_subagent.md) — `/batch` fans the work across background subagents.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The run/verify trio drives the app autonomously to confirm a change.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Prompt-based skills orchestrate via tools vs fixed-logic built-ins.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — `/batch` decomposes a large change into independent units and runs one subagent per unit in its own worktree — the orchestration pattern this term enumerates.

### 8. `cc_commands_reference` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the catalogue of every built-in Claude Code slash command; the product term is its definitional anchor.
- [Skills](../../term_dictionary/term_skills.md) — The note marks bundled-skill rows distinctly and points "to add your own commands, see skills," so the term explains the user-extensible side of the command surface.
- [Subagent](../../term_dictionary/term_subagent.md) — `/agents`, `/fork`, `/background`, `/tasks`, `/stop` manage subagents, so the term grounds the parallel-work command cluster.
- [Compaction](../../term_dictionary/term_compaction.md) — `/compact` and `/context` are the context-management commands; the term is the mechanism `/compact` triggers.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — `/rewind` (`/checkpoint`, `/undo`) rolls code and conversation back to a checkpoint — the checkpointing practice this term covers.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `/permissions`, `/sandbox`, and `/plan` adjust the approval/autonomy posture mid-session — the progressive-trust controls this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — `/mcp` manages servers and the `/mcp__server__prompt` form surfaces MCP prompts as commands, so the term grounds the MCP command section.

### 9. `cc_commands_by_workflow` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note is the task-oriented index into Claude Code's commands across a session; the product term anchors it.
- [Software Development Lifecycle (SDLC)](../../term_dictionary/term_sdlc.md) — The note organizes commands by lifecycle phase (set up → during a task → ship → between sessions → when something is wrong), the SDLC framing this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — The "running work in parallel" phase routes through `/agents`, `/batch`, `/background`, `/tasks` — subagent commands the term grounds.
- [Compaction](../../term_dictionary/term_compaction.md) — The "during a task" phase uses `/context` + `/compact` when the window fills, the compaction mechanism this term covers.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — The "when something is wrong" phase leads with `/rewind` to a checkpoint, the practice this term defines.
- [Code Review](../../term_dictionary/term_skills.md) — *(no distinct term)* — replaced; see correction below.

### 9b. `cc_commands_by_workflow` — distinct-target correction (6 distinct term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The task-oriented command index for a Claude Code session.
- [Software Development Lifecycle (SDLC)](../../term_dictionary/term_sdlc.md) — Commands grouped by lifecycle phase (set up → task → ship → between sessions → recovery).
- [Subagent](../../term_dictionary/term_subagent.md) — The parallel-work phase routes through `/agents`, `/batch`, `/background`, `/tasks`.
- [Compaction](../../term_dictionary/term_compaction.md) — The during-a-task phase uses `/context` + `/compact` when the window fills.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — The recovery phase leads with `/rewind` to a checkpoint.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The "ship" phase (`/code-review`, `/review`, `/security-review`) and `/background` show Claude reviewing and running work autonomously — behavior this term defines.

### 10. `cc_output_styles` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note documents an output style as a direct modification of Claude Code's system prompt; the product term anchors it.
- [Persona](../../term_dictionary/term_persona.md) — An output style sets Claude's role/tone (writing assistant, data analyst, diagrams-first), which is exactly the persona-conditioning this term defines.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — Output styles append instructions to the system prompt to control format and behavior every turn — a system-prompt prompt-engineering lever.
- [Prompt Optimization](../../term_dictionary/term_prompt_optimization.md) — The note frames output styles as the fix for "re-prompting for the same voice or format every turn," i.e. optimizing a recurring prompt into a persistent setting.
- [Skills](../../term_dictionary/term_skills.md) — The comparison table contrasts output styles (modify the system prompt, every response) against skills (task-specific instructions loaded when invoked), so the term grounds that distinction.
- [Subagent](../../term_dictionary/term_subagent.md) — The comparison table contrasts output styles against agents (a subagent with its own system prompt/model/tools), so the term grounds the alternative the note compares against.

### 11. `cc_prompting_patterns` (6 term notes)
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — This note distills the six reusable prompting patterns the library teaches; the term is its definitional anchor.
- [Claude Code](../../term_dictionary/term_claude_code.md) — Every pattern is framed for prompting Claude Code specifically (let Claude find the files, `@`-mention artifacts, set an output style), so the product term grounds them.
- [Prompt Optimization](../../term_dictionary/term_prompt_optimization.md) — The patterns ("describe the outcome not the steps," "state the measurable target") are concrete prompt-improvement heuristics this term covers.
- [ReAct](../../term_dictionary/term_react.md) — The "give it a way to check its own work" pattern (run/test/compare/verify in one prompt so Claude iterates) is the reason-act-observe loop this term formalizes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The patterns enable Claude to plan, edit across files, run, and self-verify from a single prompt — the autonomous-coding behavior this term defines.
- [Few-Shot Learning](../../term_dictionary/term_few_shot_learning.md) — The "point at a reference" pattern (name an existing file/test/pattern to match) supplies in-context exemplars that condition output — the few-shot conditioning this term covers.

## Section Coverage Map

```
skills.md
├── intro + command-merge note + Agent Skills standard ─ → note 1 (cc_skills_overview)
├── Bundled skills ──────────────────────────────────── → note 7 (cc_bundled_skills)
│   └── Run and verify your app ─────────────────────── → note 7 (deep internals → B10A/B11 link-out)
├── Getting started
│   ├── Create your first skill (3 Steps) ───────────── → note 2 (cc_create_a_skill)
│   ├── Where skills live ───────────────────────────── → note 1
│   ├── Live change detection ───────────────────────── → note 1
│   ├── Automatic discovery from parent/nested dirs ─── → note 1
│   └── Skills from additional directories ──────────── → note 1 (perms detail → B05A link-out)
├── Configure skills
│   ├── Types of skill content ──────────────────────── → note 3 (cc_skill_frontmatter_reference)
│   ├── Frontmatter reference (table) ───────────────── → note 3
│   ├── How a skill gets its command name ───────────── → note 3
│   ├── Available string substitutions ──────────────── → note 4 (cc_skill_arguments_and_substitutions)
│   ├── Add supporting files ────────────────────────── → note 2
│   ├── Control who invokes a skill ─────────────────── → note 5 (cc_skill_invocation_and_lifecycle)
│   ├── Skill content lifecycle ─────────────────────── → note 5 (compaction detail → B02A link-out)
│   ├── Pre-approve tools for a skill ───────────────── → note 6 (cc_skill_dynamic_context_and_subagent)
│   └── Pass arguments to skills ────────────────────── → note 4
├── Advanced patterns
│   ├── Inject dynamic context ──────────────────────── → note 6
│   ├── Run skills in a subagent ────────────────────── → note 6 (subagent term → B10A link-out)
│   ├── Restrict Claude's skill access ──────────────── → note 5 (permissions → B05A link-out)
│   └── Override skill visibility from settings ─────── → note 5 (settings field → B03A link-out)
├── Share skills ────────────────────────────────────── → note 1 (plugins → B09 link-out)
│   └── Generate visual output ──────────────────────── → note 6 (script summarized, not transcribed)
├── Troubleshooting (3 H3) ──────────────────────────── → note 5 (budget) + note 3 (description cap)
└── Related resources ───────────────────────────────── → notes 1/7 (links)
commands.md
├── Commands across a typical workflow ──────────────── → note 9 (cc_commands_by_workflow)
├── All commands (master table) ─────────────────────── → note 8 (cc_commands_reference); per-command deep pages link out
├── MCP prompts ─────────────────────────────────────── → note 8 (→ B08A mcp.md)
└── See also ────────────────────────────────────────── → notes 8/9 (links)
output-styles.md
├── intro ───────────────────────────────────────────── → note 10 (cc_output_styles)
├── Built-in output styles ──────────────────────────── → note 10
├── Change your output style ────────────────────────── → note 10 (outputStyle setting → B03A; cache → B02A link-out)
├── Create a custom output style (Steps + Frontmatter) ─ → note 10 (procedure folded; small enough — see Density)
├── How output styles work ──────────────────────────── → note 10
├── Comparisons to related features ─────────────────── → note 10
└── Related resources ───────────────────────────────── → note 10 (links)
prompt-library.md
├── JSX widget (prompt data + UI) ───────────────────── → note 11 distills the prompt categories; widget code NOT transcribed (implementation, not content)
├── What makes these prompts work (6 patterns) ──────── → note 11 (cc_prompting_patterns)
├── Where these come from ───────────────────────────── → note 11 (provenance + source links)
└── Related resources ───────────────────────────────── → note 11 (links → skills/memory/plan mode)
```
No orphaned sections. (Note 10 folds the small Create-a-custom-output-style procedure into the concept note because the whole page is 1,096 words — see Split Decisions / Density.)

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| skills.md (6.5Kw, 8 H2 / 14 H3, code-heavy) | notes 1,2,3,4,5,6,7 (+ link-outs) | exceeds density cap (>2500w); distinct BBs — overview/lifecycle/frontmatter/args are concept, create/advanced-patterns are procedure; one note per coherent H2/H3 cluster keeps each ≤700w and ≤6 code blocks |
| commands.md (3.9Kw, one 95-row table) | notes 8 (reference) + 9 (by-workflow) | the master table alone is ~1,900w (note 8, the largest, still <2500w); the "Commands across a typical workflow" narrative is a distinct task-oriented BB → note 9 |
| output-styles.md (1,096w) | note 10 only (NOT split) | under all caps; the small Create-a-style procedure (3 Steps) is folded into the concept note rather than spun into a sub-300w fragment |
| prompt-library.md (7,003w, ~85% JSX widget) | note 11 only | the digestible prose is ~1,100w (intro + 6 patterns + provenance); the widget is implementation code, not content — distilled to the pattern categories, not transcribed |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_skills_overview | concept | 650 | 1 | ✅ |
| 2 | cc_create_a_skill | procedure | 500 | 3 | ✅ |
| 3 | cc_skill_frontmatter_reference | concept | 700 | 2 | ✅ |
| 4 | cc_skill_arguments_and_substitutions | concept | 450 | 1 | ✅ |
| 5 | cc_skill_invocation_and_lifecycle | concept | 700 | 2 | ✅ |
| 6 | cc_skill_dynamic_context_and_subagent | procedure | 650 | 3 | ✅ (visualizer script summarized, not transcribed) |
| 7 | cc_bundled_skills | concept | 450 | 0 | ✅ |
| 8 | cc_commands_reference | procedure | 1,900 | 0 | ✅ (table-heavy; <2500w, 0 code) |
| 9 | cc_commands_by_workflow | procedure | 450 | 0 | ✅ |
| 10 | cc_output_styles | concept | 600 | 2 | ✅ |
| 11 | cc_prompting_patterns | concept | 550 | 3 | ✅ |

No note exceeds the caps. Note 8 is the largest at ~1,900 words but is a flat reference table with 0 code blocks — well under the 2,500-word / 400-line / 6-code caps. The skills page's long Python visualizer is summarized in note 6 (what it produces + the `${CLAUDE_SKILL_DIR}` invocation), not transcribed, keeping note 6 at 3 code blocks. No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_skills_overview cc_create_a_skill cc_skill_frontmatter_reference cc_skill_arguments_and_substitutions cc_skill_invocation_and_lifecycle cc_skill_dynamic_context_and_subagent cc_bundled_skills cc_commands_reference cc_commands_by_workflow cc_output_styles cc_prompting_patterns"
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

Single phase (11 notes, all P1). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes`, footer | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 11 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 11 notes RECEIVES ≥1 inbound link from a note OUTSIDE `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability(verify) | DB in-degree ≥1 confirmed per note after inlinks applied (anti-island) | sqlite3 in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 11 rows** under a "Customization: Skills, Commands & Prompts" cluster + increments
the BB-distribution counts (concept ×7, procedure ×4). The entry-point back-link is added to each note at finalization.

## Undigested Terms Plan (Step 4e)

b06 creates **0 new `term_dictionary` captures** — the page vocabulary is covered by a b06 `cc_` concept
note, an existing substantive term note (link), or another sub-plan (Pattern B); dedup checked across
**both** `term_dictionary/` AND `resources/documentation/` (no `claude_code/` folder exists yet, so no
doc-note collision possible):

| Term (from b06 pages) | Disposition |
|---|---|
| Skill / Agent Skill | note 1 `cc_skills_overview` (doc concept); link existing `term_skills` |
| Command / Slash command | note 8 `cc_commands_reference` (doc concept) |
| Bundled skill | note 7 `cc_bundled_skills` (doc concept) |
| Bundled workflow / dynamic workflow | note 7/8 reference; deep page owned by B10B (`workflows.md`) — link out |
| Output style | note 10 `cc_output_styles` (doc concept) |
| Dynamic context injection | note 6 `cc_skill_dynamic_context_and_subagent` (doc concept) |
| String substitution / `$ARGUMENTS` | note 4 `cc_skill_arguments_and_substitutions` (doc concept) |
| Subagent / `context: fork` | link existing `term_subagent`; deep page owned by B10A — link out |
| MCP / MCP prompt | link existing `term_mcp`; deep page owned by B08A — link out |
| Permission rule / Sandbox / Plan mode | link existing `term_graduated_trust` / `term_sandbox`; pages owned by B05A/B05B — link out |
| Compaction / Checkpoint | link existing `term_compaction` / `term_regular_checkpointing`; pages owned by B02A/B02B — link out |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/captions for
newly-surfaced non-glossary terms. Candidates considered: "prompt library", "prompting pattern", "role
prompting", "TODO(human) marker", "Insights". None warrant a new term capture: the prompting patterns are
digested as note 11 content and linked to existing `term_prompt_engineering` / `term_prompt_optimization` /
`term_react` / `term_few_shot_learning`; "Insights"/"TODO(human)" are output-style behaviors digested in
note 10; "role prompting" maps to existing `term_persona`. **0 new b06 `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — b06 authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the page concepts duplicate existing notes?) was
performed: `term_skills`, `term_subagent`, `term_mcp`, `term_compaction`, `term_regular_checkpointing`,
`term_graduated_trust`, `term_sandbox`, `term_persona`, `term_prompt_engineering`, `term_prompt_optimization`,
`term_react`, `term_few_shot_learning`, `term_sdlc`, `term_claude_code` all exist → linked, not recreated.
No too-general slug proposed.

## Term-Note Authoring Requirements

**N/A for b06** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim where transcribed; the long visualizer script is summarized, not transcribed (note 6). One BB per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; embed the manifest in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 — every note gets in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_skills.md` | notes 1, 2, 3, 4, 5, 6, 7 | skills term → the b06 skill doc cluster (definition/create/frontmatter/args/lifecycle/advanced/bundled) |
| `term_dictionary/term_claude_code.md` | notes 8, 9, 10 | product term → commands reference, command-by-workflow, output styles |
| `term_dictionary/term_prompt_engineering.md` | note 11 | prompting term → the prompting-patterns note |
| `term_dictionary/term_persona.md` | note 10 | persona term → output styles (role/tone) |
| `term_dictionary/term_subagent.md` | note 6 | subagent term → forked-skill execution |
| `term_dictionary/term_compaction.md` | note 5 | compaction term → skill-content lifecycle re-attach budget |
| `documentation/tutorials/tutorial_claude_code_getting_started.md` | note 2 | getting-started tutorial → create-a-skill procedure |

> Every one of the 11 notes appears as an inlink TARGET above (1–7 via term_skills; 8–10 via term_claude_code/term_persona; 11 via term_prompt_engineering), so all 11 receive in-degree ≥1 from outside `claude_code/` → G7/G8 satisfied.

## Follow-up Recommendations

- After the 11 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above and verify in-degree ≥1 per note (G7/G8); queue the 11 rows for `entry_claude_code_docs.md`; `/tessellum-check-broken-links`.
- Add sibling cross-links inside the cluster (note 1 ↔ 2/3/4/5/6/7; note 8 ↔ 9; note 10 ↔ 1; note 11 ↔ 10) at execution.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B06, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read in full from `inbox/claude_code_docs/`; measured words confirmed (skills 6,462 · commands 3,908 · output-styles 1,096 · prompt-library 7,003 = 18,469). Critical observation: `prompt-library.md`'s 7,003-word count is dominated by an embedded JSX/CSS `<PromptLibrary>` widget; the digestible prose (intro + 6 patterns + provenance) is ~1,100 words → one note (note 11), not the inflated count's worth of notes. No >1.5× under-estimate; the master's 11-note estimate holds exactly.
- **Notes**: 11 (concept 7, procedure 4) — matches master estimate. Splits documented: skills→7, commands→2, output-styles→1 (folded procedure), prompt-library→1.
- **Dedup-before-create (G-B)**: no `claude_code/` doc folder exists yet, so no doc-note collision; all page vocabulary either becomes a `cc_` doc concept or links an existing term (14 existing terms confirmed present). 0 recreations.
- **Step 2d new-term scan**: candidates (prompt library, role prompting, TODO(human), Insights) all route to existing terms or note content; **0 new b06 term captures**.
- **Sections added/confirmed during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), G5/G7/G8 verification, Inlinks table with explicit per-note coverage proof.
- **28-item checklist**: PASS (term-note items N/A — b06 authors no terms; entry-point + undigested-terms inherited from master; density caps re-verified; coverage map has no orphans).
- **Status**: augmented and reviewed; set to `ready`.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase) incl G7/G8 Discoverability (inbound in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); b06 contributes 11 rows under a Customization cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 11 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order + body (`## Overview` / source-mirrored H2s / `## Related Notes` indexed links / `**Source**`/`**Last Updated**`/`**Status**` footer) match the master Format Definition verbatim. |
| CP6 | Borderline density → split | ✅ PASS | All 11 notes ≤1,900w, ≤3 code; note 8 (1,900w, 0 code, flat table) is the only large note and is well under caps. None borderline-and-unsplit. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` run on all 4 pages: skills 6,462 · commands 3,908 · output-styles 1,096 · prompt-library 7,003 = plan 18,469. Within ±0%. prompt-library's widget-vs-prose split documented so the word count doesn't force phantom notes. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | b06 authors 0 term notes; Undigested Terms Plan routes all page vocabulary (Pattern B); Authoring Requirements inherited from master. |
| CP9 | Discoverability (G7/G8) inlinks executed | ✅ PASS | Inlinks table maps all 11 notes as targets (notes 1–7 ← term_skills; 8–10 ← term_claude_code/term_persona; 11 ← term_prompt_engineering), each receiving in-degree ≥1 from outside `claude_code/`; verified at finalization. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.
