---
title: Sub-Plan B10A — Claude Code Docs: Subagents & Agent Teams/View
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["agents", "sub-agents", "agent-teams", "agent-view"]
---

# Sub-Plan B10A: Subagents & Agent Teams/View

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The four "run agents in parallel" pages that document Claude Code's delegation and multi-agent surfaces:
the **comparison hub** (`agents`), **subagents** (the largest page, 8.6Kw — built-ins, definition,
configuration, work patterns, forks, examples), **agent teams** (experimental peer-coordinated sessions),
and **agent view** (`claude agents` background-session dashboard). P1 (Phase A) — subagents/teams are
core vocabulary that B10B (workflows/worktrees), B11 (automation) and the SDK sub-plans reference, so this
runs early. Glossary/vocabulary terms (Agent teams, Subagent, MCP) are routed per Pattern B, not re-digested.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 20,317 measured words. **Planned: 12 notes.**

## Content Strategy

- **Prioritize**: the subagent definition/configuration mechanics and the four-way "which parallelism approach" comparison that every later parallel-work page links (P1).
- **Group**: split the 8.6Kw `sub-agents` page (well over the 2,500w cap) into 5 BB-atomic notes — overview+built-ins (concept), definition+scope (procedure), configuration reference (procedure), work patterns (concept), forks (concept). Split the 6.9Kw `agent-view` page into 3 notes — monitor/dashboard (concept), dispatch+isolation (procedure), hosting/supervisor (concept). Split `agent-teams` into 2 — concepts/architecture (concept) + operation guide (procedure).
- **Skip / link-out (own other sub-plans)**: worktree mechanics → B10B (`worktrees.md`); dynamic workflows → B10B (`workflows.md`); hooks reference → B07A/B07B; permissions/permission-modes → B05A; MCP → B08A; skills → B06; costs/token-cost detail → B02A; routines/`/loop` → B11; desktop parallel sessions → B12A. These are referenced via links, never duplicated.
- **Glossary**: not re-digested into `cc_` term notes — vocabulary routes to existing term notes / their home sub-plan (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| agents | /agents | 956 | 0 | 3 | 0 | concept |
| sub-agents | /sub-agents | 8,598 | 27 | 6 | 26 | concept + procedure |
| agent-teams | /agent-teams | 3,910 | 11 | 8 | 19 | concept + procedure |
| agent-view | /agent-view | 6,853 | 17 | 6 | 23 | concept + procedure |

> **H2 lists (document order):**
> - **agents**: (intro comparison table) · Choose an approach · Check on running work · Learn more
> - **sub-agents**: Built-in subagents · Quickstart: create your first subagent · Configure subagents (H3 Use the /agents command, Choose the subagent scope, Write subagent files [+ Supported frontmatter fields], Choose a model, Control subagent capabilities [Available tools, Restrict which subagents can be spawned, Scope MCP servers, Permission modes, Preload skills, Enable persistent memory, Conditional rules with hooks, Disable specific subagents], Define hooks for subagents [Hooks in frontmatter, Project-level hooks]) · Work with subagents (H3 Understand automatic delegation, Invoke subagents explicitly, Run subagents in foreground or background, Common patterns, Choose between subagents and main conversation, Spawn nested subagents, Manage subagent context [What loads at startup, Resume subagents, Auto-compaction]) · Fork the current conversation (H3 Observe and steer running forks, How forks differ from named subagents, Limitations) · Example subagents (H3 Code reviewer, Debugger, Data scientist, Database query validator)
> - **agent-teams**: When to use agent teams (H3 Compare with subagents) · Enable agent teams · Start your first agent team · Control your agent team (H3 Choose a display mode, Specify teammates and models, Require plan approval, Talk to teammates directly, Assign and claim tasks, Shut down teammates, Clean up the team, Enforce quality gates with hooks) · How agent teams work (H3 How Claude starts agent teams, Architecture, Use subagent definitions for teammates, Permissions, Context and communication, Token usage) · Use case examples (H3 Run a parallel code review, Investigate with competing hypotheses) · Best practices (H3 Give teammates enough context, Choose team size, Size tasks, Wait for teammates, Start with research, Avoid file conflicts, Monitor and steer) · Troubleshooting · Limitations
> - **agent-view**: Quick start (Steps) · Monitor sessions with agent view (H3 Read session state, Row summaries, Pull request status, Peek and reply, Attach to a session, Organize the list, Filter sessions, Keyboard shortcuts) · Dispatch new agents (H3 From agent view, From inside a session, From your shell, How file edits are isolated, Set the model, Permission mode model and effort, Settings plugins and MCP servers) · Manage sessions from the shell · How background sessions are hosted (H3 The supervisor process, Where state is stored, Turn off agent view) · Troubleshooting · Limitations

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **12 notes** (matches master estimate).
Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_run_agents_in_parallel.md` | concept | agents: intro table, Choose an approach, Check on running work, Learn more | 600 | The four-way comparison hub: subagents / agent view / agent teams / dynamic workflows. Who coordinates, do workers talk, do tasks share files; the `/agents` vs `claude agents` vs `/tasks` vs `/workflows` check-on map. Worktrees + `/batch` as supporting tools. Links each home note. |
| 2 | `cc_subagents_overview.md` | concept | sub-agents: intro, "Subagents help you", Built-in subagents | 600 | What subagents are (own context window, custom system prompt, tool access, independent permissions) and why (preserve context, enforce constraints, reuse, specialize, control costs). The built-in roster: Explore, Plan, general-purpose, statusline-setup, claude-code-guide. CLAUDE.md/git-status skip for Explore/Plan. |
| 3 | `cc_create_a_subagent.md` | procedure | sub-agents: Quickstart, Configure (Use /agents, Choose the scope, Write subagent files) | 650 | How to create a subagent: `/agents` guided flow (Steps), the scope/priority table (managed > CLI > project > user > plugin), and the markdown-file format (YAML frontmatter + body system prompt). Restart-to-load rule; CLI `--agents` JSON. |
| 4 | `cc_subagent_configuration_reference.md` | procedure | sub-agents: Supported frontmatter fields, Choose a model, Control subagent capabilities, Define hooks for subagents | 900 | Reference for every frontmatter field; model-resolution order; tools/disallowedTools allowlist-denylist, `Agent(type)` spawn restriction, `mcpServers` scoping, permissionMode table + parent precedence, `skills` preload, `memory` scopes, conditional `PreToolUse` hooks, disable via `permissions.deny`, frontmatter vs settings.json hooks. |
| 5 | `cc_work_with_subagents.md` | concept | sub-agents: Work with subagents (delegation, invoke, fg/bg, common patterns, choose, nested, manage context) | 850 | Working patterns: automatic vs explicit delegation (natural language / @-mention / `--agent` session-wide), foreground vs background, isolate-high-volume / parallel-research / chain patterns, subagent-vs-main-conversation decision, nested subagents + depth limit, what loads at startup, resume, auto-compaction. |
| 6 | `cc_forked_subagents.md` | concept | sub-agents: Fork the current conversation (+ observe/steer, how forks differ, limitations) | 450 | A fork inherits the full conversation instead of starting fresh — drops input isolation but keeps output isolation. `/fork` directive, `CLAUDE_CODE_FORK_SUBAGENT`, panel controls, fork-vs-named-subagent table (context/prompt/model/permissions/prompt-cache), shared prompt cache, no nested forks. |
| 7 | `cc_subagent_examples.md` | procedure | sub-agents: Example subagents (Code reviewer, Debugger, Data scientist, DB query validator) | 550 | Four worked subagent definitions as starting templates: read-only code-reviewer, edit-capable debugger, model:sonnet data-scientist, and a `db-reader` whose `PreToolUse` hook validates read-only SQL. Best-practices tip (focused, detailed description, limit tools, version control). |
| 8 | `cc_agent_teams_overview.md` | concept | agent-teams: intro, When to use, Compare with subagents, How agent teams work (Architecture, Context/communication, Token usage), Limitations | 850 | What agent teams are (lead + teammates, shared task list, mailbox; experimental, off by default), when to use (research/review, new modules, competing hypotheses, cross-layer), subagent-vs-team comparison, architecture components + local storage, per-teammate context + messaging, token cost, current limitations. |
| 9 | `cc_orchestrate_agent_teams.md` | procedure | agent-teams: Enable, Start your first team, Control (display mode, models, plan approval, talk, assign/claim, shut down, clean up, hooks), use-case prompts, Best practices, Troubleshooting | 950 | How to run a team: enable env var, start in natural language, display modes (in-process / split panes / tmux / iTerm2), specify teammates+models, plan approval, message teammates, assign/claim tasks, shut down, clean up (always via lead), quality-gate hooks; team-size + task-size best practices; troubleshooting. |
| 10 | `cc_agent_view_monitor.md` | concept | agent-view: intro, Quick start, Monitor sessions (state, summaries, PR status, peek, attach, organize, filter, shortcuts), Limitations | 900 | The `claude agents` dashboard: what it is and the dispatch→peek→attach loop; session state icons (working/needs-input/idle/completed/failed/stopped) + process-shape icons; Haiku-class row summaries; PR-status colors; peek/reply, attach/detach, organize/pin/filter; keyboard shortcut reference; research-preview limitations. |
| 11 | `cc_dispatch_background_agents.md` | procedure | agent-view: Dispatch new agents (from view/session/shell, file isolation, set model, permission/model/effort, settings/plugins/MCP), Manage sessions from the shell | 900 | How to dispatch background sessions: from agent view input (prefixes/mentions, dispatch-to-directory), `/background`/`/bg`/`←` from a session, `claude --bg`/`--agent`/`--name`/`--exec` from the shell; worktree file isolation + `worktree.bgIsolation`; setting model/permission/effort; settings/plugin/MCP flags; the shell management commands (attach/logs/stop/respawn/rm/daemon). |
| 12 | `cc_background_session_hosting.md` | concept | agent-view: How background sessions are hosted (supervisor process, where state is stored, turn off agent view) | 500 | How background sessions persist without a terminal: the per-user supervisor process (auto-start, ~1h idle stop, pinned exemption, low-memory eviction, auto-updater restart), on-disk state layout (`daemon.log`, `roster.json`, `jobs/<id>/`), `CLAUDE_JOB_DIR`/`CLAUDE_CONFIG_DIR`, `claude daemon status`, and turning agent view off. |

**Estimate: 12 notes** — concept ×7 (notes 1,2,5,6,8,10,12), procedure ×5 (notes 3,4,7,9,11). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (20,317 words). New `cc_` notes: 12. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~8,700 (avg ~725/note). Code blocks: subagent/team/view examples copied verbatim where load-bearing (≤6/note cap respected; note 4 caps at 6 — overflow code is described, not inlined).
- **Building Block Distribution**: concept ×7 (notes 1,2,5,6,8,10,12) · procedure ×5 (notes 3,4,7,9,11). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_run_agents_in_parallel` (7 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a specialized agent that does a side task in its own context and returns a summary; relevance: the first of the four parallelism approaches the note compares ("delegated workers inside one session").
- [Multi-Agent (Multi-Agent Systems)](../../term_dictionary/term_multi_agent.md) — what-it-is: systems where multiple agents coordinate on a task; relevance: agent teams and dynamic workflows are the multi-agent rows of the note's comparison, distinguishing single-session delegation from multi-session coordination.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — what-it-is: patterns for coordinating multiple agents (supervisor vs peer); relevance: the note's "who coordinates the work?" axis (Claude inside one turn vs you handing off vs a lead vs a script) is exactly the orchestration-pattern choice this term enumerates.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the runtime wrapping the model with tools/context/execution; relevance: the note states "in every approach the workers are Claude sessions" — each parallel worker is a separate harness instance.
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — what-it-is: protocol exposing external tools to an agent; relevance: the note's closing rule is "to involve a different tool, expose it to Claude as an MCP server," the only way non-Claude workers enter these approaches.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: AI systems that plan and execute coding work independently; relevance: agent view and dynamic workflows run long tasks without you driving each step — the autonomous operating mode the note's "hand off and check back later" framing describes.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — what-it-is: establishing restore points for agent work; relevance: the note's "check on running work" commands (`/tasks`, `claude agents`, `/workflows`) are how you verify and recover parallel work, the operational discipline checkpointing supports.

### 2. `cc_subagents_overview` (7 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a specialized AI assistant handling a specific task type in its own context; relevance: this note IS the canonical product description of Claude Code subagents — the term is its definitional anchor.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the token budget an LLM session works within; relevance: the note's primary value claim is "preserve context" — each subagent runs in its own separate context window so verbose exploration never floods the main one.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the runtime that wraps the model with tools/permissions/context; relevance: each subagent is a self-contained harness ("its own context window with a custom system prompt, specific tool access, and independent permissions").
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — what-it-is: the mechanism by which a model invokes tools; relevance: built-in subagents are differentiated by tool access (Explore/Plan denied Write/Edit; general-purpose all tools), and "enforce constraints by limiting which tools a subagent can use" is a core benefit the note lists.
- [Chain of Thought (CoT)](../../term_dictionary/term_chain_of_thought.md) — what-it-is: step-by-step reasoning before answering; relevance: the Plan built-in subagent gathers research/reasoning before a plan is presented, and Explore picks a thoroughness level — the reasoning-depth control this term frames.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: AI systems that independently explore and modify code; relevance: the general-purpose built-in subagent does "complex, multi-step tasks that require both exploration and action" — the autonomous coding behavior this term defines.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: packaged repeatable instructions/workflows; relevance: the note's "Consider Skills instead" framing and the built-ins' skill-loading rules position subagents against skills as the two main customization surfaces.

### 3. `cc_create_a_subagent` (6 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a specialized agent defined by a markdown file with YAML frontmatter; relevance: this note is the creation procedure for that exact artifact (the `/agents` flow and the file format).
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the runtime configured by name/tools/model/system-prompt; relevance: creating a subagent is authoring a harness configuration — the frontmatter fields and body-as-system-prompt this note teaches.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: AIM skills, packaged markdown workflows; relevance: subagent definitions live alongside skills as markdown-with-frontmatter artifacts and can be distributed the same way (plugin scope), so the authoring/scoping model is shared.
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — what-it-is: protocol for connecting external tool servers; relevance: the `--agents` JSON and file frontmatter both accept `mcpServers`, so creation wires MCP access into the new subagent.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — what-it-is: how an agent invokes tools; relevance: the creation flow's "Select tools" step and the `tools` frontmatter field define the new subagent's tool-use surface.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive permission scoping for agent autonomy; relevance: the scope/priority table (managed > CLI > project > user > plugin) and managed-settings precedence are exactly the graduated-trust hierarchy governing who can define a subagent.

### 4. `cc_subagent_configuration_reference` (7 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a configurable specialized agent; relevance: this note is the exhaustive configuration reference for the subagent artifact (every frontmatter field and capability control).
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — what-it-is: the tool-invocation mechanism; relevance: the `tools`/`disallowedTools` allowlist-denylist resolution and the unavailable-tools list (AskUserQuestion, ExitPlanMode, etc.) are precisely tool-use scoping.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive permission modes for agent autonomy; relevance: the `permissionMode` table (default/acceptEdits/auto/dontAsk/bypassPermissions/plan) and the parent-precedence rule are the per-subagent graduated-trust controls.
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — what-it-is: external tool-server protocol; relevance: the `mcpServers` field (inline vs by-reference, strict-mcp-config, managed-MCP policies) is a full sub-section of this reference.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: packaged markdown knowledge/workflows; relevance: the `skills` frontmatter field preloads full skill content into the subagent's context, and the note documents its inverse relationship to `context: fork`.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — what-it-is: persistent cross-session memory for an agent; relevance: the `memory` field (user/project/local scopes, MEMORY.md curation, auto-enabled Read/Write/Edit) is the concrete agentic-memory mechanism this reference specifies.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the model-wrapping runtime configured here; relevance: model-resolution order, `maxTurns`, `effort`, `isolation`, `background`, and lifecycle hooks together define how the harness runs each subagent.

### 5. `cc_work_with_subagents` (7 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a delegated specialized agent; relevance: this note covers the day-to-day patterns for invoking and managing subagents (delegation, fg/bg, chaining, resume).
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the per-session token budget; relevance: "isolate high-volume operations" and "what loads at startup" are entirely about keeping verbose output out of the main context window — the note's central decision lens.
- [Sidechain Transcript](../../term_dictionary/term_sidechain_transcript.md) — what-it-is: a separate transcript file for a delegated/forked agent's turns; relevance: the note's "Manage subagent context" and "Resume subagents" sections describe subagent transcripts stored separately (`agent-{agentId}.jsonl`), persisting through main-conversation compaction — exactly the sidechain transcript concept.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — what-it-is: patterns for coordinating agents; relevance: the parallel-research, chain-subagents, and nested-subagent patterns are orchestration topologies (fan-out, pipeline, tree) this note demonstrates.
- [Compaction](../../term_dictionary/term_compaction.md) — what-it-is: summarizing context when the window fills; relevance: the note's "Auto-compaction" subsection states subagents compact with the same logic and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` as the main conversation.
- [Multi-Agent (Multi-Agent Systems)](../../term_dictionary/term_multi_agent.md) — what-it-is: coordinated multi-agent execution; relevance: "spawn nested subagents" and "run parallel research" scale one session into a tree of agents — the multi-agent topology the note's depth-limit rules govern.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — what-it-is: how an agent invokes tools; relevance: invocation patterns (@-mention, `--agent`, the Agent/Task tool) and background auto-deny behavior are tool-use mechanics this note explains.

### 6. `cc_forked_subagents` (6 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a delegated agent that normally starts with fresh context; relevance: a fork is a special subagent that inherits the full conversation instead — this note defines that variant against the base term.
- [Sidechain Transcript](../../term_dictionary/term_sidechain_transcript.md) — what-it-is: a separate transcript for a delegated agent's turns; relevance: a fork's own tool calls "stay out of your conversation and only its final result comes back" — the output-isolation-via-separate-transcript the term captures.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the per-session token budget; relevance: a fork drops input isolation (inherits full history) but keeps output isolation so "your main context window stays clean" — the core trade-off the note frames.
- [Prompt Caching - Bedrock Cached Prompt Prefix Optimization](../../term_dictionary/term_prompt_caching.md) — what-it-is: reusing a cached prompt prefix to cut cost/latency; relevance: the note states a fork's identical system prompt + tools mean "its first request reuses the parent's prompt cache," making forking cheaper than a fresh subagent.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the model-wrapping runtime; relevance: a fork shares the main session's system prompt, tools, and model — it is the same harness configuration spawned from the current state, the fork-vs-named-subagent table's contrast.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that run a side task independently; relevance: a fork runs a side task in the background while you keep working ("try several approaches in parallel from the same starting point") — autonomous parallel exploration.

### 7. `cc_subagent_examples` (6 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a markdown-defined specialized agent; relevance: this note is four worked subagent definitions (code-reviewer, debugger, data-scientist, db-reader) used as authoring templates.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — what-it-is: tool-invocation scoping; relevance: each example is differentiated by its `tools` line (read-only reviewer vs edit-capable debugger vs Bash-only db-reader) — the tool-restriction design the note teaches.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive control over what an agent may do; relevance: the db-reader example uses a `PreToolUse` hook to permit only read-only SQL — a finer-grained trust gate than the `tools` field alone provides.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the name/tools/model/system-prompt runtime; relevance: each example is a complete harness configuration (frontmatter + system-prompt body) the reader can copy and adapt.
- [Chain of Thought (CoT)](../../term_dictionary/term_chain_of_thought.md) — what-it-is: explicit step-by-step reasoning; relevance: the debugger and data-scientist prompts prescribe numbered "when invoked" workflows (capture → reproduce → isolate → fix → verify) — structured reasoning baked into the system prompt.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: packaged reusable workflows; relevance: the best-practices tip (focused, detailed description, limit tools, check into version control) mirrors skill-authoring discipline, and example subagents can be distributed like skills via plugins.

### 8. `cc_agent_teams_overview` (7 term notes)
- [Multi-Agent (Multi-Agent Systems)](../../term_dictionary/term_multi_agent.md) — what-it-is: systems of multiple coordinating agents; relevance: an agent team IS a multi-agent system — multiple Claude Code instances working together with shared tasks and direct messaging.
- [Multi-Agent Collaboration](../../term_dictionary/term_multi_agent_collaboration.md) — what-it-is: agents sharing findings and challenging each other; relevance: the strongest use cases (research/review, competing hypotheses) have teammates "share and challenge each other's findings" — the collaboration pattern this term defines.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — what-it-is: lead/peer coordination patterns; relevance: the architecture (team lead + teammates + shared task list + mailbox) and the lead's coordinate/assign/synthesize role is exactly the orchestration topology this term describes.
- [A2A (Agent2Agent Protocol)](../../term_dictionary/term_a2a.md) — what-it-is: direct agent-to-agent communication; relevance: the note's defining difference from subagents is that "teammates message each other directly" via the mailbox — peer-to-peer agent communication this term standardizes.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a delegated worker that reports only to the caller; relevance: the note's central "Compare with subagents" table contrasts teams (peer messaging, shared task list) against subagents (caller-only reporting).
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the per-session token budget; relevance: each teammate "has its own context window, fully independent," and token usage scales with teammate count — the note's cost and isolation lens.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the model-wrapping runtime; relevance: each teammate is "a separate Claude Code instance" — a full independent harness — which the note cites as the source of the higher token cost.

### 9. `cc_orchestrate_agent_teams` (7 term notes)
- [Multi-Agent (Multi-Agent Systems)](../../term_dictionary/term_multi_agent.md) — what-it-is: coordinated multiple agents; relevance: this note is the operating manual for running such a system (enable, start, control, clean up).
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — what-it-is: lead-coordinated assignment/delegation; relevance: the controls (assign vs self-claim tasks, plan approval, shut down, clean up via lead) are the concrete orchestration operations this term abstracts.
- [Multi-Agent Collaboration](../../term_dictionary/term_multi_agent_collaboration.md) — what-it-is: teammates working and conversing in parallel; relevance: the use-case prompts (parallel code review, adversarial competing-hypothesis debate) and "monitor and steer" best practice operationalize collaboration.
- [A2A (Agent2Agent Protocol)](../../term_dictionary/term_a2a.md) — what-it-is: direct inter-agent messaging; relevance: "talk to teammates directly" and shared-task-list claiming rely on the team's inter-agent messaging layer this term names.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a reusable agent definition; relevance: "use subagent definitions for teammates" lets a security-reviewer/test-runner subagent be spawned as a teammate, honoring its `tools`/`model` — the note documents that reuse path.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive permission control; relevance: teammates start with the lead's permission settings, plan-approval gates risky work, and pre-approving operations cuts permission-prompt friction — the trust controls this note configures.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the per-instance runtime; relevance: display modes, per-teammate model selection (`teammateMode`, Default teammate model), and effort all configure how each teammate harness runs.

### 10. `cc_agent_view_monitor` (6 term notes)
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that work without you watching each step; relevance: agent view is for "several independent tasks Claude can work on without you watching every step" — the autonomous-then-check-back mode this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a delegated worker inside a session; relevance: the note clarifies background sessions are full conversations, NOT subagents — subagents/teammates a session spawns "aren't listed as separate rows," a distinction the note draws explicitly.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — what-it-is: managing multiple agents from one place; relevance: agent view is the human-in-the-loop orchestration surface — one screen to dispatch, monitor state, peek, and step in only when a row needs you.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — what-it-is: restore points and status checks for agent work; relevance: the state grouping (Needs input / Working / Ready for review / Completed) and PR-status colors are how you check on and recover dispatched work without reading transcripts.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the per-session token budget; relevance: each background session is its own full conversation with its own context window, and the row's `done/total` count surfaces parallel work items within it.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the per-session runtime; relevance: each row is a distinct Claude Code session/harness, with its own model, permission mode, and worktree, monitored from the dashboard.

### 11. `cc_dispatch_background_agents` (6 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a named agent runnable as a session's main agent; relevance: dispatch accepts `<agent-name>`/`@<agent-name>`/`--agent` to run a custom subagent as the background session's main agent, with its frontmatter `permissionMode`/`model` applied.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the configurable session runtime; relevance: dispatching sets the new harness's model, permission mode, effort, settings, plugins, and MCP servers — the full launch configuration this note enumerates.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive permission scoping; relevance: dispatch resolves `defaultMode` vs the carried mode, and `bypassPermissions`/`auto` are refused until accepted interactively once — the trust gating this note specifies.
- [MCP - Model Context Protocol](../../term_dictionary/term_mcp.md) — what-it-is: external tool-server protocol; relevance: `--mcp-config`/`--strict-mcp-config` flags load MCP servers into agent view and pass them through to every dispatched session.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that run a task to completion on their own; relevance: `claude --bg "<prompt>"` and `--exec` launch a session/shell job that runs unattended — the autonomous dispatch this note operationalizes.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — what-it-is: status checks and recovery for running work; relevance: the shell management commands (`claude logs`/`attach`/`stop`/`respawn`/`rm`) are how you inspect, resume, and clean up dispatched work.

### 12. `cc_background_session_hosting` (6 term notes)
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the per-session runtime process; relevance: each background session is "its own Claude Code process, managed by the supervisor" — the note explains how those harness processes are hosted and restarted.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a spawned worker within a session; relevance: "a running background shell command, subagent, dynamic workflow, or monitor counts as active work," keeping the supervisor from stopping the session — subagent activity drives the hosting lifecycle.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that keep working unattended; relevance: the supervisor lets dispatched work keep going with no terminal attached, across sleep and binary updates — the unattended-execution substrate this term needs.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — what-it-is: persisting and restoring agent state; relevance: "session state persists on disk through auto-updates and supervisor restarts" and a stopped session restarts "from where it left off" — the checkpoint/restore behavior this note details.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the per-session conversation state; relevance: each session's transcript and state stay on disk (`jobs/<id>/state.json`) so its context survives process stop/restart, the persistence the note documents.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — what-it-is: durable per-agent state on disk; relevance: the on-disk layout (`roster.json`, `jobs/<id>/`, `CLAUDE_JOB_DIR/tmp`, `CLAUDE_CONFIG_DIR`) is the file-backed state that makes background sessions durable across restarts.

## Section Coverage Map

```
agents.md
├── (intro four-way comparison table) ──── → note 1 (cc_run_agents_in_parallel)
├── Choose an approach ──────────────────── → note 1
├── Check on running work ──────────────── → note 1 (/agents, claude agents, /tasks, /workflows)
└── Learn more (cards) ──────────────────── → note 1 (links to notes 2/8/10 + B10B workflows/worktrees)
sub-agents.md
├── (intro: what subagents are, "help you") → note 2 (cc_subagents_overview)
├── Built-in subagents ──────────────────── → note 2
├── Quickstart: create your first subagent ─ → note 3 (cc_create_a_subagent)
├── Configure subagents ─────────────────── → notes 3 + 4
│   ├── Use the /agents command ─────────── → note 3
│   ├── Choose the subagent scope ───────── → note 3
│   ├── Write subagent files ─────────────── → note 3
│   │   └── Supported frontmatter fields ── → note 4 (cc_subagent_configuration_reference)
│   ├── Choose a model ──────────────────── → note 4
│   ├── Control subagent capabilities ───── → note 4 (tools/restrict-spawn/MCP/perm-modes/skills/memory/hooks/disable)
│   └── Define hooks for subagents ──────── → note 4 (frontmatter + settings.json; full ref → B07A)
├── Work with subagents ─────────────────── → note 5 (cc_work_with_subagents)
│   ├── Understand automatic delegation ─── → note 5
│   ├── Invoke subagents explicitly ─────── → note 5
│   ├── Run subagents in foreground/bg ───── → note 5
│   ├── Common patterns ──────────────────── → note 5
│   ├── Choose between subagents / main ──── → note 5
│   ├── Spawn nested subagents ──────────── → note 5
│   └── Manage subagent context ──────────── → note 5 (what loads / resume / auto-compaction)
├── Fork the current conversation ───────── → note 6 (cc_forked_subagents)
│   ├── Observe and steer running forks ──── → note 6
│   ├── How forks differ from named subs ── → note 6
│   └── Limitations ──────────────────────── → note 6
└── Example subagents ───────────────────── → note 7 (cc_subagent_examples) [4 examples]
agent-teams.md
├── (intro + experimental Warning/Note) ─── → note 8 (cc_agent_teams_overview)
├── When to use agent teams ─────────────── → note 8
│   └── Compare with subagents ──────────── → note 8
├── Enable agent teams ──────────────────── → note 9 (cc_orchestrate_agent_teams)
├── Start your first agent team ──────────── → note 9
├── Control your agent team ─────────────── → note 9 (display/models/plan-approval/talk/assign/shutdown/cleanup/hooks)
├── How agent teams work ────────────────── → note 8 (architecture/context/comms/token-usage)
│   ├── How Claude starts agent teams ───── → note 9
│   ├── Architecture ─────────────────────── → note 8
│   ├── Use subagent definitions for mates ─ → note 9
│   ├── Permissions ──────────────────────── → note 9
│   ├── Context and communication ───────── → note 8
│   └── Token usage ──────────────────────── → note 8 (cost detail → B02A)
├── Use case examples ───────────────────── → note 9 (review / competing hypotheses)
├── Best practices ──────────────────────── → note 9
├── Troubleshooting ─────────────────────── → note 9
└── Limitations ─────────────────────────── → note 8
agent-view.md
├── (intro: what agent view is) ──────────── → note 10 (cc_agent_view_monitor)
├── Quick start (Steps) ─────────────────── → note 10
├── Monitor sessions with agent view ─────── → note 10
│   ├── Read session state ───────────────── → note 10
│   ├── Row summaries ────────────────────── → note 10 (Haiku-class model → B03B model-config)
│   ├── Pull request status ──────────────── → note 10
│   ├── Peek and reply ───────────────────── → note 10
│   ├── Attach to a session ──────────────── → note 10 (fullscreen → B04B)
│   ├── Organize the list ────────────────── → note 10
│   ├── Filter sessions ──────────────────── → note 10
│   └── Keyboard shortcuts ───────────────── → note 10
├── Dispatch new agents ─────────────────── → note 11 (cc_dispatch_background_agents)
│   ├── From agent view ──────────────────── → note 11
│   ├── From inside a session ────────────── → note 11
│   ├── From your shell ──────────────────── → note 11
│   ├── How file edits are isolated ──────── → note 11 (worktree mechanics → B10B worktrees.md)
│   ├── Set the model ────────────────────── → note 11
│   ├── Permission mode, model, and effort ─ → note 11 (perm detail → B05A)
│   └── Settings, plugins, and MCP servers ─ → note 11
├── Manage sessions from the shell ──────── → note 11
├── How background sessions are hosted ──── → note 12 (cc_background_session_hosting)
│   ├── The supervisor process ──────────── → note 12
│   ├── Where state is stored ────────────── → note 12 (CLAUDE_CONFIG_DIR → B03A env-vars)
│   └── Turn off agent view ──────────────── → note 12
├── Troubleshooting ─────────────────────── → note 10/11/12 (folded into owning note by topic)
└── Limitations ─────────────────────────── → note 10
```
No orphaned sections. Worktree mechanics (B10B), dynamic workflows (B10B), full hooks reference (B07A), permissions (B05A), MCP install (B08A), skills (B06), token-cost detail (B02A), model-config (B03B) are link-outs, never duplicated.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| sub-agents (8,598w >2500, 6 H2 / 26 H3, 27 code) | notes 2,3,4,5,6,7 (+ link-outs) | far exceeds density cap; distinct BBs — overview (concept), create (procedure), config reference (procedure), work patterns (concept), forks (concept), examples (procedure). Config reference isolated so its 6-code cap isn't blown by the work-patterns prose. |
| agent-teams (3,910w >2500, 8 H2 / 19 H3) | notes 8,9 | exceeds cap; concept (what/why/architecture/limits) vs procedure (enable/start/control/best-practices/troubleshoot) differ in BB and audience. |
| agent-view (6,853w >2500, 6 H2 / 23 H3, 17 code) | notes 10,11,12 | exceeds cap; monitor/dashboard (concept), dispatch+shell-management (procedure), hosting/supervisor (concept) are three separable topics; troubleshooting folded into the matching topic note. |
| agents (956w) | note 1 (kept whole) | small comparison hub; one concept note, no split needed. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_run_agents_in_parallel | concept | 600 | 0 | ✅ |
| 2 | cc_subagents_overview | concept | 600 | 0 | ✅ |
| 3 | cc_create_a_subagent | procedure | 650 | 3 | ✅ |
| 4 | cc_subagent_configuration_reference | procedure | 900 | 6 | ✅ (at code cap — overflow code described, not inlined) |
| 5 | cc_work_with_subagents | concept | 850 | 2 | ✅ |
| 6 | cc_forked_subagents | concept | 450 | 1 | ✅ |
| 7 | cc_subagent_examples | procedure | 550 | 4 | ✅ (4 example definitions; validator script described/abridged) |
| 8 | cc_agent_teams_overview | concept | 850 | 1 | ✅ |
| 9 | cc_orchestrate_agent_teams | procedure | 950 | 5 | ✅ |
| 10 | cc_agent_view_monitor | concept | 900 | 1 | ✅ |
| 11 | cc_dispatch_background_agents | procedure | 900 | 5 | ✅ |
| 12 | cc_background_session_hosting | concept | 500 | 1 | ✅ |

No note exceeds 950 words / 6 code / 400 lines. Note 4 is the only note at the 6-code cap; the executor must keep only the load-bearing frontmatter/YAML examples and describe overflow in prose. No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_run_agents_in_parallel cc_subagents_overview cc_create_a_subagent cc_subagent_configuration_reference cc_work_with_subagents cc_forked_subagents cc_subagent_examples cc_agent_teams_overview cc_orchestrate_agent_teams cc_agent_view_monitor cc_dispatch_background_agents cc_background_session_hosting"
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

Single phase (12 notes, all P1). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 12 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 12 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | confirm DB in-degree ≥1 for every new note after inlinks applied (anti-island, re-verify post-execution) | sqlite3 in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 12 rows** under a "Subagents & Multi-Agent" cluster + increments the
BB-distribution counts (concept ×7, procedure ×5).

## Undigested Terms Plan (Step 4e)

B10A creates **no new `term_dictionary` notes** — the vocabulary these pages introduce is covered by a
B10A `cc_` doc note, an existing substantive term note (link), or its home sub-plan (Pattern B). Dedup was
run across **both** `term_dictionary/` AND `resources/documentation/` (bm25 + dense + filename grep); no
`cc_` doc note duplicates an existing term note.

| Term / concept | Disposition |
|---|---|
| Agent teams | note 8 `cc_agent_teams_overview` (doc concept); links `term_multi_agent` / `term_a2a` |
| Subagent | existing `term_subagent` (link) — doc treatment in notes 2-7 |
| Forked subagent / fork | note 6 `cc_forked_subagents` (doc concept); links `term_subagent` / `term_sidechain_transcript` |
| Agent view / background session | notes 10-12 (doc concept) |
| Supervisor process / daemon | note 12 `cc_background_session_hosting` (doc concept; no standalone term — not a vault vocabulary concept) |
| Team lead / teammate / mailbox / shared task list | folded into notes 8-9; links `term_agent_orchestration` / `term_a2a` |
| MCP / Skills / Hooks / Permission mode / Worktree / Dynamic workflow / Compaction / Context window / Prompt cache | existing term notes (link) or home sub-plan (B08A/B06/B07A/B05A/B10B/B02A) — captured there, never inlined |
| Haiku-class model / model alias | linked to B03B `model-config`; existing `term_autonomous_coding_agents`/harness context |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/captions for
newly-surfaced non-glossary terms. Candidates surfaced — **"supervisor process / daemon"** (agent-view) and
**"mailbox"** (agent-teams) — both are CC-internal implementation nouns, not cross-cutting vault vocabulary;
they are documented inline in their owning `cc_` note and need no `term_dictionary` capture. **0 new B10A
`term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B10A authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do these concepts duplicate existing notes?) was
performed: `term_subagent`, `term_multi_agent`, `term_multi_agent_collaboration`, `term_agent_orchestration`,
`term_a2a`, `term_agent_as_a_tool`, `term_sidechain_transcript`, `term_agent_harness`,
`term_autonomous_coding_agents`, `term_mcp`, `term_skills`, `term_context_window`, `term_compaction`,
`term_graduated_trust`, `term_function_calling`, `term_prompt_caching`, `term_chain_of_thought`,
`term_agentic_memory`, `term_regular_checkpointing` all exist → linked, not recreated.

## Term-Note Authoring Requirements

**N/A for B10A** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks copied verbatim from source (YAML frontmatter, JSON settings, bash). One BB per note. Each note ≤400 lines (split a draft >350).
- Note 4 is at the 6-code cap: keep only load-bearing examples, describe overflow in prose.
- Cap dynamic-workflow fan-out at ~30 agents/run; embed manifests in the script.
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 inbound in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_subagent.md` | notes 2, 4, 5, 6 | subagent term → CC subagent overview / config reference / work patterns / forks |
| `term_dictionary/term_multi_agent.md` | notes 1, 8 | multi-agent term → CC parallelism hub / agent-teams overview |
| `term_dictionary/term_agent_orchestration.md` | notes 1, 9 | orchestration term → parallelism hub / orchestrate-teams procedure |
| `term_dictionary/term_a2a.md` | note 8 | A2A term → agent-teams inter-agent messaging |
| `term_dictionary/term_sidechain_transcript.md` | note 6 | sidechain-transcript term → forked subagents output isolation |
| `term_dictionary/term_agent_harness.md` | notes 3, 10, 12 | harness term → create-subagent / agent-view monitor / background hosting |
| `term_dictionary/term_autonomous_coding_agents.md` | notes 10, 11 | autonomous-agent term → agent-view monitor / dispatch |
| `projects/vault_note.md` | notes 8, 9 | vault's own multi-agent system → CC agent-teams concept/procedure |
| `resources/digest/digest_openclaw_10_lessons_agent_teams.md` | note 8 | agent-teams lessons digest → CC agent-teams overview |

## Follow-up Recommendations

- After the 12 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above (verify in-degree ≥1 per note); queue the 12 rows for `entry_claude_code_docs.md` under a "Subagents & Multi-Agent" cluster; `/tessellum-check-broken-links`.
- Add forward cross-links to B10B (`cc_worktrees`, `cc_dynamic_workflows`) and B07A (`cc_hooks`) once those sub-plans execute, completing the parallelism cluster.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | DONE 2026-06-13 — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | READY (9/9) — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B10A, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read in full from `inbox/claude_code_docs/`; measured words match the master's figures (agents 956 · sub-agents 8,598 · agent-teams 3,910 · agent-view 6,853 = 20,317). The 8.6Kw sub-agents page is >3× the 2,500w cap, forcing the documented 6-note split; agent-view (6.9Kw) and agent-teams (3.9Kw) likewise re-split. No >1.5× under-estimate beyond what the splits absorb.
- **Notes**: 12 (concept 7, procedure 5) — matches master estimate exactly. Splits documented in Split Decisions.
- **Step 2d new-term scan**: candidates "supervisor process/daemon" and "mailbox" surfaced → both CC-internal implementation nouns documented inline; **0 new B10A term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), G7/G8 discoverability rows, Inlinks table.
- **28-item checklist**: PASS (term-note items N/A — B10A authors no terms; entry-point + undigested-terms inherited from master).
- **Status**: augmented and self-reviewed to `ready` (9/9 below).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase) incl. G7/G8 discoverability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE); B10A contributes 12 rows under "Subagents & Multi-Agent". |
| CP4 | Plan size ≤30 / split | ✅ PASS | 12 notes; part of master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches existing `documentation/` notes exactly; body uses `## Overview` / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer convention. |
| CP6 | Borderline density → split | ✅ PASS | Largest note 950w / 6 code; note 4 flagged at code cap with overflow-prose instruction. The 8.6Kw/6.9Kw/3.9Kw pages were split rather than compressed. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` 2026-06-13: agents 956, sub-agents 8,598, agent-teams 3,910, agent-view 6,853 = 20,317 = master figure. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B10A authors 0 term notes; Undigested Terms Plan routes vocabulary (Pattern B, dedup across term_dictionary AND documentation/); Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check documented (19 existing terms linked, not recreated; no `cc_` doc note duplicates a term note). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `ready`.

**Source**: https://code.claude.com/docs/en/agents
**Last Updated**: 2026-06-13
**Status**: Active
