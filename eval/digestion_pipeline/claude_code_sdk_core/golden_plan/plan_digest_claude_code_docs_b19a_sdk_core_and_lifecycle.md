---
title: Sub-Plan B19A — Claude Code Docs: Agent SDK Core & Lifecycle
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["agent-sdk/overview", "agent-sdk/quickstart", "agent-sdk/agent-loop", "agent-sdk/claude-code-features", "agent-sdk/migration-guide"]
---

# Sub-Plan B19A: Agent SDK Core & Lifecycle

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 5 foundational Agent SDK pages that introduce what the SDK is, how to build a first agent, the
mechanics of the agent loop (turns, messages, tools, context window, results, hooks), how to load
Claude Code filesystem features into SDK agents, and how to migrate from the old Claude Code SDK. P2
(Phase B) — these define the SDK vocabulary the other SDK sub-plans (B19B/B19C/B20*/B21*) reference, so
this is the entry point into the SDK series. SDK details that have dedicated pages (sessions, streaming,
custom tools, permissions reference, skills-in-SDK, hosting, language refs) are linked out, never
duplicated.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 5 pages, 11,899 measured words. **Planned: 11 notes.**

## Content Strategy

- **Prioritize**: the agent-loop mechanics (turns/messages/tool-execution/context/result) and the
  `query()`/`ClaudeAgentOptions` entry point that every later SDK sub-plan links (the SDK's core
  vocabulary).
- **Group**: split the large `agent-loop` page (4.2Kw, 23 H2/H3) into loop-mechanics vs tool-execution vs
  loop-control vs context-window vs result+hooks; split `overview` into identity/capabilities (concept),
  install (procedure), and the tool-comparison (argument); split `claude-code-features` into
  settingSources mechanics (procedure) and the choose-the-right-feature decision (argument). Keep
  `quickstart` as one build-an-agent procedure + a key-concepts concept note.
- **Skip / link-out (own other sub-plans)**: sessions deep-dive → B19B `agent-sdk/sessions`; streaming →
  B19C; custom tools → B20A; MCP-in-SDK → B20A; skills-in-SDK → B20B; subagents-in-SDK → B20B;
  hooks-in-SDK reference → B20C; permissions-in-SDK reference → B20C; structured-output retries → B19C
  `agent-sdk/structured-outputs`; cost-tracking → B21A; hosting/secure-deployment → B21A; Python/TS
  language refs → B21B/B21C; modifying-system-prompts → B19B; provider env-vars (Bedrock/Vertex/Azure) →
  B14A. These are referenced via links, never duplicated.
- **Glossary/terms**: no new `term_dictionary` captures — SDK concepts are digested as `cc_` doc notes
  and link existing term notes (Pattern B; see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 5 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| agent-sdk/overview | /agent-sdk/overview | 2,568 | 0* | 8 | 1 | concept/procedure/argument |
| agent-sdk/quickstart | /agent-sdk/quickstart | 1,709 | 4 | 7 | 4 | procedure/concept |
| agent-sdk/agent-loop | /agent-sdk/agent-loop | 4,228 | 0* | 11 | 12 | concept |
| agent-sdk/claude-code-features | /agent-sdk/claude-code-features | 2,278 | 0* | 6 | 2 | procedure/argument |
| agent-sdk/migration-guide | /agent-sdk/migration-guide | 1,116 | 20 | 7 | 5 | procedure/concept |

> *Code count from raw ` ``` ` fences. `overview`, `agent-loop`, and `claude-code-features` wrap code in
> `<CodeGroup>`/`<Accordion>` MDX components whose inner fences `grep -c '^```'` did not count at the line
> start; each is code-rich (Python+TypeScript snippet pairs). Notes derived from them keep ≤6 distilled
> code blocks each (caps enforced in Density Re-Assessment).

> **H2 lists (document order):**
> - **overview**: Get started · Capabilities (H3 Claude Code features) · Compare the Agent SDK to other Claude tools · Changelog · Reporting bugs · Branding guidelines · License and terms · Next steps
> - **quickstart**: Prerequisites · Setup · Create a buggy file · Build an agent that finds and fixes bugs (H3 Run your agent, Try other prompts, Customize your agent) · Key concepts · Troubleshooting (H3 thinking.type.enabled error) · Next steps
> - **agent-loop**: The loop at a glance · Turns and messages · Message types (H3 Handle messages) · Tool execution (H3 Built-in tools, Tool permissions, Parallel tool execution) · Control how the loop runs (H3 Turns and budget, Effort level, Permission mode, Model) · The context window (H3 What consumes context, Automatic compaction, Keep context efficient) · Sessions and continuity · Handle the result · Hooks · Put it all together · Next steps
> - **claude-code-features**: Control filesystem settings with settingSources (H3 What settingSources does not control) · Project instructions CLAUDE.md and rules (H3 CLAUDE.md load locations) · Skills · Hooks (H3 When to use which hook type) · Choose the right feature · Related resources
> - **migration-guide**: Overview · What's Changed · Migration Steps (H3 TypeScript/JavaScript, Python) · Breaking changes (H3 ClaudeCodeOptions rename, System prompt no longer default, Settings sources default) · Why the Rename? · Getting Help · Next Steps

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **11 notes** (matches master estimate). Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_agent_sdk_overview.md` | concept | overview: intro, Capabilities (tabs), Claude Code features | 600 | What the Agent SDK is (Claude Code as a library, Python+TS); `query()`/`ClaudeAgentOptions` entry point; capability tour (built-in tools, hooks, subagents, MCP, permissions, sessions); filesystem-feature loading → note 9. Credit-billing note. |
| 2 | `cc_agent_sdk_install_and_auth.md` | procedure | overview: Get started (install, API key, run first agent) | 450 | Install (npm / pip; Python 3.10+); set `ANTHROPIC_API_KEY`; third-party providers (Bedrock/AWS/Vertex/Azure env vars → B14A); run-first-agent snippet. |
| 3 | `cc_agent_sdk_compare_to_other_tools.md` | argument | overview: Compare the Agent SDK to other Claude tools | 450 | SDK vs Client SDK (built-in vs hand-rolled tool loop); SDK vs CLI (interface, when to use each); SDK vs Managed Agents (in-process library vs hosted REST). When-to-choose guidance. |
| 4 | `cc_agent_sdk_quickstart_bug_fixer.md` | procedure | quickstart: Prerequisites, Setup, buggy file, Build/Run agent, Customize | 600 | Step-by-step: project + install + `.env`; create buggy `utils.py`; write `agent.py`/`agent.ts` with `query()`; run; customize (web search / system prompt / Bash). Links note 5 for tool/mode tables. |
| 5 | `cc_agent_sdk_tools_and_permission_modes.md` | concept | quickstart: Key concepts; agent-loop: Tool permissions (intro) | 450 | The `allowedTools` capability ladder (read-only / modify / full automation); permission-mode table (`acceptEdits`/`dontAsk`/`auto`/`bypassPermissions`/`default`); full ref → B20C. |
| 6 | `cc_agent_sdk_agent_loop.md` | concept | agent-loop: loop at a glance, Turns and messages | 550 | The 5-step gather→evaluate→execute→repeat→return cycle; what a turn is; `max_turns`/`max_budget_usd` stopping; one-vs-many-turn examples. |
| 7 | `cc_agent_sdk_message_types.md` | concept | agent-loop: Message types, Handle messages | 500 | The 5 core message types (`SystemMessage`/`AssistantMessage`/`UserMessage`/`StreamEvent`/`ResultMessage`); Python `isinstance` vs TS `.type`/`.message`; which to handle per use case. |
| 8 | `cc_agent_sdk_tool_execution.md` | concept | agent-loop: Tool execution (Built-in tools, Tool permissions, Parallel) | 500 | Built-in tool categories table (file/search/execution/web/discovery/orchestration); `allowed`/`disallowed`/`permission_mode` interplay; parallel read-only vs sequential write tools; `readOnlyHint`. |
| 9 | `cc_agent_sdk_loop_controls.md` | concept | agent-loop: Control how the loop runs (Turns and budget, Effort, Permission mode, Model) | 600 | Turn/budget caps + error subtypes; effort levels table (low→max); permission-mode table; model selection default. All `ClaudeAgentOptions` fields. |
| 10 | `cc_agent_sdk_context_window.md` | concept | agent-loop: The context window (What consumes, Automatic compaction, Keep efficient) | 600 | What accumulates per request; prompt-caching of stable prefix; compaction + `compact_boundary` + `PreCompact`/`/compact`; efficiency strategies (subagents, scoped tools, MCP costs, lower effort). |
| 11 | `cc_agent_sdk_result_and_hooks.md` | concept | agent-loop: Handle the result, Hooks; Put it all together | 550 | `ResultMessage` subtypes table + `stop_reason`/`total_cost_usd`/`usage`; loop hooks table (`PreToolUse`…`PreCompact`); hooks run out-of-context and can short-circuit; combined end-to-end example. |
| 12 | `cc_agent_sdk_settingsources.md` | procedure | claude-code-features: settingSources, What it doesn't control, CLAUDE.md, Skills, Hooks loading | 700 | `settingSources` opt-in list (`user`/`project`/`local`); what loads where; inputs read regardless (managed policy, `~/.claude.json`, auto memory, claude.ai MCP) + multi-tenant warning; CLAUDE.md load locations; skill/hook filesystem loading. |
| 13 | `cc_agent_sdk_choose_a_feature.md` | argument | claude-code-features: Choose the right feature; When to use which hook type | 450 | Goal→feature decision table (CLAUDE.md / skills / subagents / agent teams / hooks / MCP) with SDK surface; filesystem-vs-programmatic hook choice; subagents-vs-agent-teams distinction. |
| 14 | `cc_agent_sdk_migration_guide.md` | procedure | migration-guide: all sections | 600 | Rename Claude Code SDK → Agent SDK; TS + Python migration steps (uninstall/install/imports/types); breaking changes (`ClaudeCodeOptions`→`ClaudeAgentOptions`, system prompt no longer default, settingSources default history); why the rename. |

> Note: the table lists 14 rows but locks at **11 notes** — see Split Decisions and the Density
> Re-Assessment. Rows 5 and 8 are merged into the surviving note 8 (`cc_agent_sdk_tool_execution`); rows
> 6 and 7 are kept distinct; the final locked set is renumbered 1–11 below.

**FINAL LOCKED SET (11 notes, renumbered):**

| # | Filename | BB | ~Words |
|---|---|---|---:|
| 1 | `cc_agent_sdk_overview.md` | concept | 600 |
| 2 | `cc_agent_sdk_install_and_auth.md` | procedure | 450 |
| 3 | `cc_agent_sdk_compare_to_other_tools.md` | argument | 450 |
| 4 | `cc_agent_sdk_quickstart_bug_fixer.md` | procedure | 600 |
| 5 | `cc_agent_sdk_agent_loop.md` | concept | 600 |
| 6 | `cc_agent_sdk_message_types.md` | concept | 500 |
| 7 | `cc_agent_sdk_tool_execution.md` | concept | 600 |
| 8 | `cc_agent_sdk_loop_controls.md` | concept | 650 |
| 9 | `cc_agent_sdk_context_window.md` | concept | 600 |
| 10 | `cc_agent_sdk_result_and_hooks.md` | concept | 550 |
| 11 | `cc_agent_sdk_settingsources_and_features.md` | procedure | 750 |

> The locked set folds the draft's quickstart key-concepts (row 5) into `cc_agent_sdk_loop_controls`
> (permission modes) + `cc_agent_sdk_tool_execution` (tool ladder), and folds the
> choose-a-feature argument (row 13) + migration-guide (row 14) reasoning into a single
> settingSources-and-features procedure note plus a forward-link, keeping the count at the master's 11.
> **All subsequent sections use this FINAL LOCKED SET numbering (1–11).**

**Estimate: 11 notes** — concept ×7 (notes 1,5,6,7,8,9,10), procedure ×3 (notes 2,4,11), argument ×1 (note 3). All single-BB, all within caps. (Migration content folds into note 11's "Migrate from the old SDK" section as a procedure, kept ≤cap.)

## Summary Statistics & Building Block Distribution

- Source pages: 5 (11,899 words). New `cc_` notes: 11. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~5,950 (avg ~540/note). Distilled code blocks: ≤6 per note (snippet pairs from code-rich source kept minimal).
- **Building Block Distribution**: concept ×7 (notes 1,5,6,7,8,9,10) · procedure ×3 (notes 2,4,11) · argument ×1 (note 3). No model/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.
> Term existence verified via `ls .../term_dictionary/<slug>.md` (all PASS).

### 1. `cc_agent_sdk_overview` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Claude Code is the agentic coding tool whose tools/agent loop/context management this SDK exposes as a library; the page literally frames the SDK as "Claude Code as a library," so the term is the definitional anchor.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The SDK is precisely the agent harness (tools + context management + execution loop wrapping the LLM) made programmatic in Python/TypeScript; this note documents that harness as a packaged dependency.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The page's headline is agents that "autonomously read files, run commands, search the web, edit code"; the SDK is the tooling for building exactly the autonomous-coding-agent category this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The Capabilities tab dedicates an MCP section (connect databases/browsers/APIs as tools) and lists MCP among the SDK's first-class extension surfaces, making MCP a capability this overview teaches.
- [Subagent](../../term_dictionary/term_subagent.md) — A Capabilities tab covers spawning specialized subagents via `AgentDefinition`/the Agent tool, with `parent_tool_use_id` tracking — a core SDK capability the overview introduces.
- [Skills](../../term_dictionary/term_skills.md) — The "Claude Code features" table lists Skills (`.claude/skills/*/SKILL.md`) as a filesystem feature the SDK loads, one of the extension surfaces this overview enumerates.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The SDK's value proposition is that Claude "handles tool execution" for you — the built-in agentic tool-use loop this note describes is the function-calling/tool-use mechanism made automatic.

### 2. `cc_agent_sdk_install_and_auth` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — This note installs and authenticates the Agent SDK, which is Claude Code packaged as a library; the TS package even bundles the native Claude Code binary, so the product term grounds the install.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Installing the SDK package is installing the agent harness runtime into your own process; the note's setup steps wire up that harness with credentials.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Authentication unlocks the SDK's MCP-connected tools; the note's provider/credential setup is the prerequisite for the SDK's MCP and tool capabilities to run.
- [Bedrock Agents](../../term_dictionary/term_bedrock_agents.md) — The note documents the `CLAUDE_CODE_USE_BEDROCK=1` provider path and AWS credential setup; Bedrock is one of the third-party auth backends, so the term grounds that provider option.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The install/auth steps culminate in running a first autonomous agent that lists/edits files; the term defines the class of agent this setup enables.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The run-first-agent snippet pre-approves built-in tools (`Bash`, `Glob`) so Claude can call them — the function-calling/tool-use loop this note's final step exercises.

### 3. `cc_agent_sdk_compare_to_other_tools` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The comparison's anchor: SDK vs Claude Code CLI is "same capabilities, different interface," so the Claude Code term defines the shared engine all three options share.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The decisive difference vs the Client SDK is that the Agent SDK ships the harness (built-in tool loop) while the Client SDK makes you hand-roll it; the harness term is the axis of this comparison.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The note's central code contrast is the Client SDK's manual `while stop_reason == "tool_use"` loop vs the Agent SDK's automatic tool handling — the function-calling loop is exactly what's automated.
- [Bedrock Agents](../../term_dictionary/term_bedrock_agents.md) — The SDK-vs-Managed-Agents comparison (in-process library vs hosted, managed-sandbox REST service) parallels the managed-agent-service pattern Bedrock Agents represents, contextualizing the hosted-vs-self-hosted trade-off.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — Choosing among Client SDK / Agent SDK / CLI / Managed Agents is an orchestration-architecture decision (who runs the loop, who executes tools, where state lives) — the trade-offs this term frames.
- [Sandbox](../../term_dictionary/term_sandbox.md) — The Managed-Agents column's key difference is "a managed sandbox per session" run by Anthropic vs files on your own infrastructure; sandboxing is the isolation dimension distinguishing the options.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Every option compared is a way to run autonomous coding/agentic work; the term defines the category the page is comparing delivery mechanisms for.

### 4. `cc_agent_sdk_quickstart_bug_fixer` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The quickstart builds an agent on the Agent SDK (Claude Code as a library); the product term anchors the engine the tutorial drives.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The whole tutorial is "build an AI agent that reads your code, finds bugs, and fixes them, all without manual intervention" — the autonomous-coding-agent behavior this term names.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The `query()` call the tutorial centers on starts the agent harness loop (the SDK handles tool execution, context, retries); the harness term explains what `query()` is driving.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The agent autonomously calls `Read`/`Edit`/`Glob` to fix the buggy file — the function-calling/tool-use loop the tutorial demonstrates end to end.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The tutorial uses `permission_mode="acceptEdits"` to auto-approve file edits while gating other actions — the graduated, scope-by-trust permission model this term defines.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — The "Try other prompts" / custom system-prompt steps show how prompt wording steers the agent's behavior, a direct application of prompt engineering to the SDK.

### 5. `cc_agent_sdk_agent_loop` (8 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The page states the SDK runs "the same execution loop that powers Claude Code"; the product term anchors the loop this note dissects.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The loop (receive→evaluate→execute→repeat→return) is the agent harness's core control flow; this note documents the harness's runtime cycle.
- [ReAct](../../term_dictionary/term_react.md) — The loop's evaluate-call-tool-observe-result-repeat cycle, where each tool result feeds the next decision, is the interleaved reason-act-observe pattern ReAct formalizes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The note describes a complex task chaining "dozens of tool calls across many turns," Claude adjusting per result — the autonomous multi-step behavior this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — A "turn" is exactly one tool-use round trip (Claude requests tools, SDK executes, results feed back); function-calling is the unit the loop iterates on.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — `max_turns`/`max_budget_usd` and the turn-by-turn control of when the loop stops are loop-orchestration controls this term frames.
- [Context Window](../../term_dictionary/term_context_window.md) — The note explains the loop accumulates conversation/tool I/O into the context window across turns within a session — the container the loop fills (detailed in note 9).
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — The loop's message-driven request/response cycle between host process and agent runtime parallels the agent-client protocol pattern this term describes for editor/agent communication.

### 6. `cc_agent_sdk_message_types` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The five message types are the Agent SDK's (Claude Code's library form) public streaming surface; the product term anchors the API this note documents.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — `SystemMessage`/`AssistantMessage`/`UserMessage`/`StreamEvent`/`ResultMessage` are the harness's emitted lifecycle events; the harness term frames what produces this message stream.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `AssistantMessage` carries tool-call blocks and `UserMessage` carries tool results — the function-calling request/response pair surfaced as message types.
- [Structured Output](../../term_dictionary/term_structured_output.md) — `ResultMessage` exposes a typed `subtype`/`result`/`usage` schema and an `error_max_structured_output_retries` subtype; the note's typed-result handling is the structured-output contract this term defines.
- [ReAct](../../term_dictionary/term_react.md) — The message sequence (`AssistantMessage` action → `UserMessage` observation → next `AssistantMessage`) is the observable trace of the reason-act-observe cycle this term names.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — `AssistantMessage` tool-call blocks reference tool names/inputs defined by tool descriptors; the term grounds the tool-definition side of the messages this note parses.

### 7. `cc_agent_sdk_tool_execution` (8 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note documents the built-in tools that "power Claude Code," exposed in the SDK; the product term anchors the tool set.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — Tool execution IS the function-calling mechanism: Claude requests tools, the SDK runs them, results feed back; the note's core subject.
- [Tool Descriptor](../../term_dictionary/term_tool_descriptor.md) — Each built-in tool and custom tool is defined by a descriptor (name, schema, `readOnlyHint` annotation); the term grounds the tool-definition layer the note's parallel-execution rule keys off.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Built-in tools (file/search/execution/web/discovery/orchestration) are the harness's tool layer that turns the model into an agent; the harness term frames the capability set.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The `allowed_tools`/`disallowed_tools`/`permission_mode` interplay that decides which tool calls run is the graduated-trust permission gating this term defines.
- [Deny-First](../../term_dictionary/term_deny_first.md) — `disallowed_tools` blocks listed tools "regardless of other settings," and unlisted tools require approval — the deny-by-default / deny-takes-precedence posture this term names.
- [Subagent](../../term_dictionary/term_subagent.md) — The orchestration tool row (`Agent`, `Skill`, `TaskCreate`) includes spawning subagents; the term grounds that built-in orchestration capability.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — Beyond built-ins, the note says you connect external services via MCP servers and that MCP read-only tools can run in parallel; MCP extends the tool set the note describes.

### 8. `cc_agent_sdk_loop_controls` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Loop controls are fields on `ClaudeAgentOptions` for the Claude-Code-derived loop; the product term anchors the options surface.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — `max_turns`/`max_budget_usd`/effort/model are the knobs for orchestrating how far, how deep, and how expensively the loop runs — the orchestration controls this term frames.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The permission-mode table (`default`/`acceptEdits`/`plan`/`dontAsk`/`auto`/`bypassPermissions`) is the graduated-trust spectrum from prompt-everything to run-everything this term defines.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — The `effort` levels (low→max) control how much reasoning Claude applies per turn, and the note distinguishes effort from visible extended-thinking chain-of-thought blocks — the term grounds that reasoning-depth dimension.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — Lower effort and turn/budget caps are context-and-cost engineering levers; the note's guidance to tune effort/turns per task is applied context engineering.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `max_turns` "counts tool-use turns only," so the budget controls are denominated in function-calling round trips this term names.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Budgets and turn caps exist to keep autonomous agents from "running long on open-ended prompts"; the controls bound exactly the autonomy this term defines.

### 9. `cc_agent_sdk_context_window` (7 term notes)
- [Context Window](../../term_dictionary/term_context_window.md) — This note IS the SDK's context-window page: what accumulates, the per-source cost table, and limits — the term is its definitional anchor.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — The note states stable prefixes (system prompt, tool definitions, CLAUDE.md) are automatically prompt-cached to cut cost/latency for repeated prefixes — the mechanism this term defines.
- [Compaction](../../term_dictionary/term_compaction.md) — The note's Automatic Compaction section (summarize older history, `compact_boundary` message, `PreCompact` hook, `/compact`) is exactly the compaction mechanism this term names.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The "Keep context efficient" strategies (subagents, scoped tools, watch MCP costs, lower effort) are textbook context-engineering practices this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — The top efficiency strategy is offloading subtasks to subagents that start with fresh context and return only a summary, so the main window grows by the summary not the transcript — the isolation property this term defines.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The note warns MCP tool schemas can consume significant context unless deferred by tool search; MCP is a major context-cost source the note tracks.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — The note notes that persistent rules belong in CLAUDE.md (re-injected every request, survives compaction) rather than the prompt — the agentic-memory persistence mechanism this term describes.

### 10. `cc_agent_sdk_result_and_hooks` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The `ResultMessage` and loop hooks are the Claude-Code-derived SDK's termination and lifecycle surface; the product term anchors the API.
- [Structured Output](../../term_dictionary/term_structured_output.md) — The `ResultMessage` subtype table (`success`/`error_max_turns`/`error_max_budget_usd`/…/`error_max_structured_output_retries`) plus typed `total_cost_usd`/`usage`/`stop_reason` is the structured-result contract this term defines.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Hooks fire "at specific points in the loop" run by the harness; the harness term frames the lifecycle this note hooks into.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — `PreToolUse`/`PostToolUse` hooks bracket each tool call and can short-circuit it (rejection becomes the tool result) — the function-calling step the hooks intercept.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — A `PreToolUse` hook that rejects a tool call is a programmatic graduated-trust gate (block dangerous commands before they run) this term defines.
- [Subagent](../../term_dictionary/term_subagent.md) — The hooks table includes `SubagentStart`/`SubagentStop` for tracking spawned subagents; the term grounds those subagent-lifecycle hook events.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — The note stresses hooks "run in your application process, not inside the agent's context window, so they don't consume context" — a deliberate context-engineering property this term frames.

### 11. `cc_agent_sdk_settingsources_and_features` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The note loads Claude Code's filesystem features (CLAUDE.md, rules, skills, hooks) into SDK agents and covers migrating from the old Claude Code SDK; the product term anchors both.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — `settingSources` loads CLAUDE.md/rules as persistent project context and the note documents auto-memory at `~/.claude/projects/<project>/memory/` loaded into the system prompt — the agentic-memory mechanism this term defines.
- [Skills](../../term_dictionary/term_skills.md) — The note explains skills are discovered via `settingSources`, load on demand (description at start, full content when relevant), and need the `Skill` tool enabled — the skills mechanism this term defines.
- [Sandbox](../../term_dictionary/term_sandbox.md) — The multi-tenant warning (inputs read regardless of `settingSources`; use `settingSources: []` + disable auto memory + per-tenant filesystem) is the isolation/sandboxing guidance this term frames.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Filesystem hooks loaded via `settingSources` can deny tool calls (`permissionDecision: "deny"`), wiring the project's graduated-trust permission rules into the SDK agent.
- [MCP (Model Context Protocol)](../../term_dictionary/term_mcp.md) — The note's "inputs read regardless" table and choose-a-feature row both cover MCP servers (claude.ai connectors loaded by subscription auth; `mcpServers` for structured external access) — MCP is one feature the note routes.
- [Schema Evolution](../../term_dictionary/term_schema_evolution.md) — The folded migration section documents a versioned breaking change (`ClaudeCodeOptions`→`ClaudeAgentOptions`, package rename, default behavior shifts across v0.0.x→v0.1.0→revert) — the schema/API evolution-and-migration discipline this term defines.

> **Term-pool note:** `term_sdk` was a search candidate but is **NOT in the DB** (verified MISSING) — it
> is therefore EXCLUDED from every link set and from the bullet lists above. Note 1's locked links are 7
> verified terms (Claude Code, Agent Harness, Autonomous Coding Agents, MCP, Subagent, Skills, Function
> Calling). No ghost term appears in any locked list below or in any note's bullet list.

**Locked verified term set (per note, ghost-free):**

|---|---|---|---:|
| 1 | cc_agent_sdk_overview | claude_code, agent_harness, autonomous_coding_agents, mcp, subagent, skills, function_calling | 7 |
| 2 | cc_agent_sdk_install_and_auth | claude_code, agent_harness, mcp, bedrock_agents, autonomous_coding_agents, function_calling | 6 |
| 3 | cc_agent_sdk_compare_to_other_tools | claude_code, agent_harness, function_calling, bedrock_agents, agent_orchestration, sandbox, autonomous_coding_agents | 7 |
| 4 | cc_agent_sdk_quickstart_bug_fixer | claude_code, autonomous_coding_agents, agent_harness, function_calling, graduated_trust, prompt_engineering | 6 |
| 5 | cc_agent_sdk_agent_loop | claude_code, agent_harness, react, autonomous_coding_agents, function_calling, agent_orchestration, context_window, acp | 8 |
| 6 | cc_agent_sdk_message_types | claude_code, agent_harness, function_calling, structured_output, react, tool_descriptor | 6 |
| 7 | cc_agent_sdk_tool_execution | claude_code, function_calling, tool_descriptor, agent_harness, graduated_trust, deny_first, subagent, mcp | 8 |
| 8 | cc_agent_sdk_loop_controls | claude_code, agent_orchestration, graduated_trust, chain_of_thought, context_engineering, function_calling, autonomous_coding_agents | 7 |
| 9 | cc_agent_sdk_context_window | context_window, prompt_caching, compaction, context_engineering, subagent, mcp, agentic_memory | 7 |
| 10 | cc_agent_sdk_result_and_hooks | claude_code, structured_output, agent_harness, function_calling, graduated_trust, subagent, context_engineering | 7 |
| 11 | cc_agent_sdk_settingsources_and_features | claude_code, agentic_memory, skills, sandbox, graduated_trust, mcp, schema_evolution | 7 |


## Section Coverage Map

```
agent-sdk/overview.md
├── intro + first snippet ──────────────── → note 1 (cc_agent_sdk_overview)
├── Get started (install, API key, run) ── → note 2 (cc_agent_sdk_install_and_auth); providers → B14A
├── Capabilities (tabs) ────────────────── → note 1 (capability tour; deep dives link out)
│   ├── Hooks tab ──────────────────────── → note 1 → note 10 + B20C
│   ├── Subagents tab ──────────────────── → note 1 → B20B
│   ├── MCP tab ────────────────────────── → note 1 → B20A
│   ├── Permissions tab ────────────────── → note 1 → note 8 + B20C
│   └── Sessions tab ───────────────────── → note 1 → B19B
├── Claude Code features (table) ───────── → note 1 → note 11
├── Compare the Agent SDK to other tools ─ → note 3 (cc_agent_sdk_compare_to_other_tools)
├── Changelog / Reporting bugs ─────────── → note 1 (References, external links)
├── Branding guidelines / License ──────── → note 1 (brief mention) / → B16 legal (link)
└── Next steps (cards) ─────────────────── → notes 1/2/4 (links)
agent-sdk/quickstart.md
├── Prerequisites / Setup ──────────────── → note 4 (cc_agent_sdk_quickstart_bug_fixer)
├── Create a buggy file ────────────────── → note 4
├── Build / Run agent + Try / Customize ── → note 4
├── Key concepts: Tools table ──────────── → note 7 (cc_agent_sdk_tool_execution)
├── Key concepts: Permission modes table ─ → note 8 (cc_agent_sdk_loop_controls)
├── Troubleshooting (thinking.type error) ─ → note 4 (brief) → B17 troubleshooting (link)
└── Next steps (cards) ─────────────────── → note 4 (links)
agent-sdk/agent-loop.md
├── The loop at a glance ───────────────── → note 5 (cc_agent_sdk_agent_loop)
├── Turns and messages ─────────────────── → note 5
├── Message types (+ Handle messages) ──── → note 6 (cc_agent_sdk_message_types)
├── Tool execution (built-in/perm/parallel)→ note 7 (cc_agent_sdk_tool_execution)
├── Control how the loop runs ──────────── → note 8 (cc_agent_sdk_loop_controls)
│   ├── Turns and budget / Effort / Model ─ → note 8
│   └── Permission mode ─────────────────── → note 8 (full ref → B20C)
├── The context window ─────────────────── → note 9 (cc_agent_sdk_context_window)
│   ├── What consumes / Automatic compaction → note 9
│   └── Keep context efficient ──────────── → note 9
├── Sessions and continuity ────────────── → note 5 (brief) → B19B sessions (link)
├── Handle the result ──────────────────── → note 10 (cc_agent_sdk_result_and_hooks)
├── Hooks ──────────────────────────────── → note 10 (overview) → B20C full hooks (link)
├── Put it all together ────────────────── → note 10 (combined example)
└── Next steps ─────────────────────────── → notes 5–10 (links)
agent-sdk/claude-code-features.md
├── Control filesystem with settingSources → note 11 (cc_agent_sdk_settingsources_and_features)
│   └── What settingSources does not control → note 11
├── Project instructions (CLAUDE.md/rules) → note 11
│   └── CLAUDE.md load locations ────────── → note 11
├── Skills ─────────────────────────────── → note 11 (loading) → B20B skills-in-SDK (link)
├── Hooks (+ When to use which hook type) ─ → note 11 (loading/choice) → note 10 / B20C (link)
├── Choose the right feature ───────────── → note 11 (decision table)
└── Related resources ──────────────────── → note 11 (links)
agent-sdk/migration-guide.md
├── Overview / What's Changed ──────────── → note 11 ("Migrate from the old SDK" section)
├── Migration Steps (TS / Python) ──────── → note 11
├── Breaking changes ───────────────────── → note 11
│   ├── ClaudeCodeOptions rename ────────── → note 11
│   ├── System prompt no longer default ─── → note 11 (brief) → B19B system-prompts (link)
│   └── Settings sources default ────────── → note 11 (ties to settingSources)
├── Why the Rename? ────────────────────── → note 11
└── Getting Help / Next Steps ──────────── → note 11 (links)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| agent-sdk/overview (2.6Kw, code-rich, mixed BB) | notes 1,2,3 | distinct BB: identity/capabilities (concept) vs install (procedure) vs tool comparison (argument); each ≤cap, capability deep-dives link out to B19B/B20A/B20B/B20C |
| agent-sdk/agent-loop (4.2Kw >2500, 23 H2/H3) | notes 5,6,7,8,9,10 + link-outs | exceeds density cap by >1.5×; six distinct concepts (loop mechanics / message types / tool execution / loop controls / context window / result+hooks); sessions deep-dive owned by B19B, full hooks/permissions ref by B20C |
| agent-sdk/claude-code-features + migration-guide (2.3Kw + 1.1Kw) | note 11 (procedure) | both are filesystem-feature/config procedures; the choose-a-feature argument folds in as a decision table, migration folds in as a "Migrate from the old SDK" section; combined ≤cap (≤750w est.) — see Density Re-Assessment |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_agent_sdk_overview | concept | 600 | ≤4 | ✅ |
| 2 | cc_agent_sdk_install_and_auth | procedure | 450 | ≤3 | ✅ |
| 3 | cc_agent_sdk_compare_to_other_tools | argument | 450 | ≤2 | ✅ |
| 4 | cc_agent_sdk_quickstart_bug_fixer | procedure | 600 | ≤6 | ✅ |
| 5 | cc_agent_sdk_agent_loop | concept | 600 | ≤1 | ✅ |
| 6 | cc_agent_sdk_message_types | concept | 500 | ≤2 | ✅ |
| 7 | cc_agent_sdk_tool_execution | concept | 600 | ≤1 | ✅ |
| 8 | cc_agent_sdk_loop_controls | concept | 650 | ≤2 | ✅ |
| 9 | cc_agent_sdk_context_window | concept | 600 | ≤2 | ✅ |
| 10 | cc_agent_sdk_result_and_hooks | concept | 550 | ≤2 | ✅ |
| 11 | cc_agent_sdk_settingsources_and_features | procedure | 750 | ≤6 | ✅ |

Note 11 is the densest (folds claude-code-features + migration-guide); at ~750 words and ≤6 distilled
code blocks it stays within all caps. The source pages are code-rich (Python+TypeScript snippet pairs
inside MDX `<CodeGroup>`), so each note keeps ONLY the minimum distilled snippets (one language or one
representative pair) to stay ≤6 code blocks; full dual-language code lives in the B21B/B21C language
references. No note approaches the 2,500-word / 400-line caps. No over-compression — every H2/H3 maps to
a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_agent_sdk_overview cc_agent_sdk_install_and_auth cc_agent_sdk_compare_to_other_tools cc_agent_sdk_quickstart_bug_fixer cc_agent_sdk_agent_loop cc_agent_sdk_message_types cc_agent_sdk_tool_execution cc_agent_sdk_loop_controls cc_agent_sdk_context_window cc_agent_sdk_result_and_hooks cc_agent_sdk_settingsources_and_features"
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

Single phase (11 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/agent-sdk/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 11 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 11 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1) | DB confirms in-degree ≥1 for all 11 after inlinks applied | `note_links` in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 11 rows** under an "Agent SDK" cluster + increments the BB-distribution
counts (concept ×7, procedure ×3, argument ×1). The entry-point back-link is added to each note at
finalization (the hub is created as a pre-step before the first sub-plan executes, per master G-G).

## Undigested Terms Plan (Step 4e)

b19a creates **0 new `term_dictionary` notes** — SDK vocabulary is digested as `cc_` doc concept notes
and links existing substantive term notes (Pattern B), with dedup checked across **both**
`term_dictionary/` AND `resources/documentation/` (the `claude_code/` folder is empty; no existing
`agent_sdk` doc note exists anywhere → no recreate risk):

| SDK term / concept | Disposition |
|---|---|
| Agent SDK / Claude Agent SDK | note 1 `cc_agent_sdk_overview` (doc concept); links `term_claude_code` + `term_agent_harness` (exist) |
| Agent loop / turn | note 5 `cc_agent_sdk_agent_loop` (doc concept); links `term_react` + `term_function_calling` (exist) |
| Message types (SystemMessage/AssistantMessage/UserMessage/StreamEvent/ResultMessage) | note 6 (doc concept) |
| Built-in tools / tool execution / parallel execution | note 7 (doc concept); links `term_function_calling` + `term_tool_descriptor` (exist) |
| Effort level | note 8; links `term_chain_of_thought` (exists) — extended thinking |
| Permission mode | note 8; links `term_graduated_trust` (exists) |
| Context window / compaction / prompt caching | note 9; link `term_context_window` + `term_compaction` + `term_prompt_caching` (exist) |
| Result subtype / stop_reason / structured output | note 10; links `term_structured_output` (exists) |
| Hooks (SDK) | note 10 overview; full ref owned by B20C `agent-sdk/hooks` |
| settingSources / CLAUDE.md / rules / skills loading | note 11; links `term_skills` + `term_agentic_memory` (exist) |
| Managed Agents / Client SDK | note 3 (doc concept, comparison); links `term_bedrock_agents` (exists, managed-agent analog) |
| Migration / rename / breaking changes | note 11 "Migrate from the old SDK"; links `term_schema_evolution` (exists) |
| Sessions / streaming / system prompts / custom tools / MCP-in-SDK / hosting / cost-tracking | owned by home sub-plan (B19B/B19C/B20A/B20C/B21A) — captured there, linked out |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 5 pages scanning emphasis/tables/captions for
newly-surfaced non-glossary terms. Candidates surfaced and resolved: "effort level" → links
`term_chain_of_thought` (extended-thinking dimension); "structured output" → links existing
`term_structured_output`; "prompt caching" → links existing `term_prompt_caching`; "Managed Agents" →
links existing `term_bedrock_agents` (closest managed-agent-service analog, no dedicated CC term needed);
"settingSources" → digested as a doc concept in note 11 (no standalone term). One candidate term —
"Software Development Kit / SDK" — has **no existing term note** (`term_sdk` MISSING in DB) and is a
generic industry term whose CC-specific sense is fully captured by note 1; per the master's
0-new-term-dictionary design decision it is **NOT** captured as a new term note (generic, non-specific
slug; would duplicate note 1's coverage). **0 new B19A `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B19A authors zero term notes, so there are
no new slugs to audit. The collision check that matters here (do the SDK concepts duplicate existing
notes?) was performed across `term_dictionary/` AND `documentation/`: all 17 linked terms exist and are
substantive (linked, not recreated); the `claude_code/` doc folder is empty and no `agent_sdk` doc note
exists anywhere in `documentation/`, so no `cc_` note duplicates an existing doc or term note.

## Term-Note Authoring Requirements

**N/A for b19a** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply only to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks distilled verbatim from source (keep ≤6/note; full dual-language code → B21B/B21C). One BB
  per note. Each note ≤400 lines (split if a draft >350).
- Cap dynamic-workflow fan-out at ~30 agents/run; commit + push after the phase
  (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 5 | product term → Agent SDK overview + agent-loop (the library/loop form of Claude Code) |
| `term_dictionary/term_agent_harness.md` | notes 1, 5 | harness term → SDK overview + agent-loop (harness as a packaged library) |
| `term_dictionary/term_autonomous_coding_agents.md` | note 4 | autonomous-agent term → the quickstart bug-fixing agent |
| `term_dictionary/term_context_window.md` | note 9 | context-window term → SDK per-source context-cost + compaction |
| `term_dictionary/term_structured_output.md` | notes 6, 10 | structured-output term → SDK message types + ResultMessage subtypes |
| `term_dictionary/term_function_calling.md` | note 7 | tool-use term → SDK tool-execution mechanics |
| `term_dictionary/term_schema_evolution.md` | note 11 | API-evolution term → SDK migration / breaking-changes section |
| `documentation/tutorials/tutorial_claude_code_getting_started.md` | notes 1, 4 | getting-started tutorial → SDK overview + quickstart |

These guarantee every one of the 11 notes (1,4,5,6,7,9,10,11 directly; 2,3,8 via sibling `cc_*` inlinks
from notes 1/5/4 within the cluster plus the entry-point hub row) receives ≥1 inbound link. At
finalization, also add intra-cluster sibling links (note 1 → notes 2,3; note 5 → notes 6,7,8,9,10; note
4 → note 5) so notes 2,3,8 satisfy G7/G8 with an out-of-source inbound edge from the entry-point hub plus
a sibling edge.

## Follow-up Recommendations

- After the 11 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the
  11 rows for `entry_claude_code_docs.md` (Agent SDK cluster); `/tessellum-check-broken-links`; verify DB
  in-degree ≥1 for all 11 (G7/G8).
- Cross-link to sibling SDK sub-plans (B19B sessions/system-prompts, B19C streaming/structured-output,
  B20A custom-tools/MCP, B20B skills/subagents, B20C hooks/permissions, B21A hosting, B21B/B21C language
  refs) once those execute.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE 2026-06-13** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **DONE 2026-06-13 — READY (9/9)** — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B19A, 2026-06-13)

- **Source re-read (Step 2)**: all 5 pages re-read fully from `inbox/claude_code_docs/agent-sdk/`;
  measured words match the master's figure (overview 2,568 · quickstart 1,709 · agent-loop 4,228 ·
  claude-code-features 2,278 · migration-guide 1,116 = 11,899). `agent-loop` is >1.5× the density cap →
  re-split into 6 notes (5–10); `overview` split into 3 (identity/install/comparison); `claude-code-features`
  + `migration-guide` folded into one procedure note (11).
- **Notes**: 11 (concept 7, procedure 3, argument 1) — matches master estimate. Splits documented.
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard
  PASS)** — `term_sdk` candidate found MISSING and EXCLUDED before locking; relpaths `../../term_dictionary/`.
- **Dedup (G-B)**: checked across `term_dictionary/` AND `documentation/` — `claude_code/` folder empty,
  no existing `agent_sdk` doc note anywhere → 0 recreate risk; all 17 linked terms are substantive
  existing notes (linked, not recreated).
- **Step 2d new-term scan**: candidates resolved to existing terms (chain_of_thought, structured_output,
  prompt_caching, bedrock_agents) or doc concepts; `term_sdk` generic & MISSING → not captured; **0 new
  B19A term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), locked verified-term table, G5/G7/G8 verification rows.
- **28-item checklist**: PASS (term-note items N/A — B19A authors no terms; entry-point + undigested-terms
  inherited from master).
- **Status**: augmented + reviewed; set to `ready` after the 9/9 self-review below.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (>30 notes → CREATE required); B19A contributes 11 rows under an Agent SDK cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 11 notes; part of master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | Inherits master Format Definition VERBATIM (YAML field order, `## Overview` opener, source-mirrored H2s, `## Related Notes` indexed links, `**Source**`/`**Last Updated**`/`**Status**` footer). |
| CP6 | Borderline density → split | ✅ PASS | `agent-loop` (4.2Kw >2500, >1.5×) split into 6; `overview` split into 3; note 11 (folded) re-assessed at ~750w/≤6 code — within caps; none borderline-unsplit. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` re-measured 2026-06-13: overview 2,568 · quickstart 1,709 · agent-loop 4,228 · claude-code-features 2,278 · migration-guide 1,116 = 11,899 = master figure. ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B19A authors 0 term notes; Undigested Terms Plan routes every SDK term (existing-term link / doc concept / home sub-plan); Authoring Requirements inherited. |
| CP8f / CP9 | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); collision check across `term_dictionary/` AND `documentation/` documented (17 existing terms linked; empty `claude_code/` folder + no existing `agent_sdk` doc note → no duplicate `cc_` note); `term_sdk` ghost candidate excluded. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status set to `ready`.

**Source**: https://code.claude.com/docs/en/agent-sdk/overview
**Last Updated**: 2026-06-13
**Status**: Ready
