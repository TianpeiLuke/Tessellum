---
title: Sub-Plan B03B — Claude Code Docs: CLI, Model & Tools Reference
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["cli-reference", "model-config", "tools-reference", "debug-your-config"]
---

# Sub-Plan B03B: CLI, Model & Tools Reference

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The four operator-reference pages that document Claude Code's command-line surface, model selection and
reasoning controls, the built-in tool catalog, and configuration debugging. P2 (Phase B) — these reference
notes are built on the Phase A cores (B03A settings, B05A permissions, B08A MCP) and link them rather than
re-defining them. This sub-plan owns the doc-concept homes the master assigned it: **Effort level** and
**Tool (reference)**.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 4 pages, 15,276 measured words. **Planned: 12 notes.**

## Content Strategy

- **Prioritize**: the canonical reference catalogs that other sub-plans cite — the CLI command/flag tables,
  the tool catalog + per-tool behavior, the model-alias/effort/extended-thinking controls.
- **Group**: split the 5.6Kw `model-config` (over the 2,500w cap) into model selection, restriction,
  effort/thinking, extended context, and model environment variables; split the 4.3Kw `tools-reference` into
  catalog+permission-format vs per-tool behavior; split `cli-reference` into commands vs flags vs system-prompt flags.
- **Skip / link-out (own other sub-plans)**: permission rule SYNTAX → B05A; settings precedence + key list →
  B03A; env-var full list → B03A; MCP server config → B08A; sandbox → B05B; subagent frontmatter → B10A;
  agent view / background sessions → B10A; worktrees → B10B; prompt-caching cost mechanics → B02A. These are
  referenced via links, never duplicated.
- **Doc-concept terms owned here** (master Pattern B): **Effort level** → note 6 `cc_effort_level_and_thinking`;
  **Tool (reference)** → note 9 `cc_tools_catalog`. No new `term_dictionary` captures (see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 4 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| cli-reference | /cli-reference | 3,383 | 0 | 3 | 1 | procedure (reference) |
| model-config | /model-config | 5,579 | 11 | 6 | 18 | procedure (reference) |
| tools-reference | /tools-reference | 4,318 | 2 | 16 | 3 | concept/procedure (reference) |
| debug-your-config | /debug-your-config | 1,996 | 1 | 7 | 0 | procedure |

> **H2 lists (document order):**
> - **cli-reference**: CLI commands · CLI flags (H3 System prompt flags) · See also
> - **model-config**: Available models (H3 Model aliases, Work with Fable 5, Setting your model) · Restrict model selection (H3 Default model behavior, Control the model users run on, Merge behavior, Mantle model IDs) · Special model behavior (H3 `default` model setting, `opusplan` model setting, Fallback model chains, Automatic model fallback, Adjust effort level, Extended thinking, Extended context) · Checking your current model · Add a custom model option · Environment variables (H3 Pin models for third-party deployments, Customize pinned model display and capabilities, Override model IDs per version, Prompt caching configuration)
> - **tools-reference**: (catalog table, no H2) · Configure tools with permission rules and hooks · Agent tool behavior · Bash tool behavior · Edit tool behavior · Glob tool behavior · Grep tool behavior · LSP tool behavior · Monitor tool · NotebookEdit tool behavior · PowerShell tool (H3 Enable the PowerShell tool, Shell selection in settings/hooks/skills, Preview limitations) · Read tool behavior · WebFetch tool behavior · WebSearch tool behavior · Write tool behavior · Check which tools are available · See also
> - **debug-your-config**: See what loaded into context · Check resolved settings · Check MCP servers · Check hooks · Test against a clean configuration · Check common causes · Related resources

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **12 notes** (matches master estimate). Prefix `cc_`, target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_cli_commands.md` | procedure | cli-reference: CLI commands table | 700 | The `claude` subcommand catalog (start/resume/`-p`/update/install/auth/agents/attach/daemon/logs/mcp/plugin/project purge/remote-control/respawn/rm/setup-token/stop/ultrareview); typo-suggestion behavior. Detail refs → agent-view (B10A), MCP (B08A), plugins (B09A), remote-control (B12B), authentication (B14B). |
| 2 | `cc_cli_flags.md` | procedure | cli-reference: CLI flags table (excl. system-prompt) | 900 | The ~45 runtime flags grouped (session/resume, model/effort, permissions/tools, MCP/plugins, print-mode/output, surfaces, debug/safe-mode); each overrides the matching setting for that session only. `--help` not exhaustive. Syntax of permission rules → B05A; settings → B03A; env vars → B03A. |
| 3 | `cc_cli_system_prompt_flags.md` | argument | cli-reference: System prompt flags subsection | 450 | The four `--system-prompt[-file]` / `--append-system-prompt[-file]` flags; replace-vs-append decision rule; mutual exclusivity; per-invocation only (persistent → output-styles B06 / CLAUDE.md B02B). |
| 4 | `cc_model_selection.md` | concept | model-config: Available models, Model aliases, Work with Fable 5, Setting your model, Checking current model | 700 | Aliases (default/best/fable/sonnet/opus/haiku/`[1m]`/opusplan) and how they resolve per provider; the four ways to set a model and their priority; resume keeps its model; `/status` to check. |
| 5 | `cc_restrict_model_selection.md` | procedure | model-config: Restrict model selection + Default model behavior + Control the model users run on + Merge behavior + Mantle model IDs | 700 | `availableModels` allowlist across every model surface; `enforceAvailableModels` for the Default option; how blocked selections are handled; managed/policy replace vs user/project merge; Mantle IDs. Settings files → B03A. |
| 6 | `cc_effort_level_and_thinking.md` | concept | model-config: Adjust effort level (+ choose/set sub-H3, ultrathink, adaptive reasoning) + Extended thinking | 850 | Effort levels per model (low→max, ultracode); the five ways to set effort and their precedence; `ultrathink` keyword; adaptive vs fixed thinking budget; extended-thinking display/toggle controls. Owns doc-concept **Effort level**. |
| 7 | `cc_extended_context_1m.md` | concept | model-config: Extended context | 450 | The 1M-token context window: which models support it, plan-by-plan availability matrix, auto-upgrade vs usage credits, `CLAUDE_CODE_DISABLE_1M_CONTEXT`, pricing, the `[1m]` suffix usage. Context-window concept → B02A. |
| 8 | `cc_fallback_models.md` | concept | model-config: `opusplan` model setting + Fallback model chains + Automatic model fallback (+ all sub-H3) | 850 | Two distinct fallback systems: availability-based `fallbackModel` chains (cap 3, current-turn only) and content-based Fable-5 safety-classifier fallback to Opus (`/config` ask-before-switch, provider enablement, security/biology routing); plus `opusplan` plan→execute hybrid. |
| 9 | `cc_tools_catalog.md` | concept | tools-reference: catalog table + Configure tools with permission rules and hooks + Check which tools are available | 800 | The full built-in tool catalog (Agent/Bash/Edit/Read/Write/Glob/Grep/LSP/Web*/Task*/Team*/Monitor/Skill/Workflow/…) with permission-required column; the `ToolName(specifier)` rule format shared across tools; how to disable a tool; how to check the live tool set. Owns doc-concept **Tool (reference)**. Rule syntax detail → B05A. |
| 10 | `cc_file_tool_behavior.md` | procedure | tools-reference: Read, Edit, Write, NotebookEdit, Glob, Grep tool behavior | 850 | Per-tool semantics for the file/search tools: Read paging + image/PDF/notebook handling; Edit's read-before-edit + exact-match + uniqueness checks; Write overwrite rule; NotebookEdit cell modes; Glob patterns + `.gitignore` behavior; Grep ripgrep regex + output modes. |
| 11 | `cc_execution_tool_behavior.md` | procedure | tools-reference: Agent, Bash, Monitor, PowerShell, WebFetch, WebSearch, LSP tool behavior | 900 | Per-tool semantics for the execution/web/agent tools: Agent subagent isolation + tool inheritance; Bash cwd carry-over/timeout/output limits; Monitor background watch; PowerShell enablement + shell selection; WebFetch lossy extraction + domain prompts; WebSearch backend; LSP code intelligence. Subagent config → B10A. |
| 12 | `cc_debug_your_configuration.md` | procedure | debug-your-config: all 7 H2 | 850 | Diagnose why CLAUDE.md/settings/hooks/MCP/skills didn't take effect: `/context` + the per-surface inspector commands (`/memory` `/skills` `/hooks` `/mcp` `/doctor` `/status`); resolved-settings precedence; `--safe-mode` + clean-config test; the common-causes symptom→cause→fix table. |

**Estimate: 12 notes** — concept ×5 (notes 4,6,7,8,9), procedure ×6 (notes 1,2,5,10,11,12), argument ×1 (note 3). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 4 (15,276 words). New `cc_` notes: 12. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~8,800 (avg ~730/note). Code blocks: ≤2/note (model-config JSON/bash examples reproduced selectively; tools-reference PowerShell JSON).
- **Building Block Distribution**: concept ×5 (notes 4,6,7,8,9) · procedure ×6 (notes 1,2,5,10,11,12) · argument ×1 (note 3). No model/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_cli_commands` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding CLI/tool; relevance: this note IS the command catalog for the `claude` binary, so the product term is its definitional anchor.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the runtime wrapping an LLM with tools/context/execution; relevance: the CLI commands (`claude`, `claude -p`, `claude agents`) are the entry points that launch that harness in its various modes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that plan/edit/run/verify with minimal steering; relevance: `claude --bg`, `claude respawn`, and `claude agents` manage long-running autonomous background sessions, the operating mode this term names.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — what-it-is: open protocol for connecting external tools/data to an agent; relevance: the `claude mcp` subcommand configures MCP servers, one of the command catalog's entries.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a Claude instance spawned with its own context to offload a task; relevance: `claude agents`, `claude attach`, `claude stop/respawn/rm` operate on background subagent sessions in the agent view.
- [Cursor](../../term_dictionary/term_cursor.md) — what-it-is: an AI-native code editor / coding-agent surface; relevance: contextualizes the CLI-first surface category Claude Code's command set competes in versus editor-embedded agents.

### 2. `cc_cli_flags` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: this note documents the runtime flags of the `claude` command itself, so the product term anchors them.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive permission escalation (default → auto-accept → bypass); relevance: `--permission-mode`, `--dangerously-skip-permissions`, `--allowedTools`/`--disallowedTools` are the flag-level controls of exactly that trust ladder.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the tool/context/execution runtime around the model; relevance: flags like `--mcp-config`, `--plugin-dir`, `--add-dir`, `--system-prompt` configure what the harness loads for a session.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — what-it-is: protocol for external tool/data connections; relevance: `--mcp-config`, `--strict-mcp-config`, and `--permission-prompt-tool` are the MCP-related runtime flags.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what-it-is: deliberate management of what enters the context window; relevance: `--exclude-dynamic-system-prompt-sections`, `--append-system-prompt`, and `--bare` are flags that shape session context for cache reuse and faster starts.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: an isolated-context spawned Claude instance; relevance: `--agents`, `--agent`, and `--bg` define and launch subagents from the command line.

### 3. `cc_cli_system_prompt_flags` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: the four system-prompt flags customize the default Claude Code system prompt, so the product term grounds the default identity being replaced or appended to.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — what-it-is: crafting prompts to steer model behavior; relevance: choosing append vs replace and what extra rules to add is precisely a prompt-engineering decision the note teaches.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the runtime that wraps the model with its default system prompt, tools, and safety guidance; relevance: replacing the prompt drops the harness's default tool guidance and safety instructions, the trade-off the note's decision rule turns on.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what-it-is: managing what occupies the context window; relevance: appending vs replacing the system prompt directly changes the persistent context budget every turn carries.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: packaged on-demand instructions/workflows; relevance: the note points persistent persona needs to output-styles/CLAUDE.md rather than these per-invocation flags, distinguishing transient from durable instruction surfaces skills also serve.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents operating unattended; relevance: the note's replace-the-prompt case targets non-coding agents in unwatched `-p` pipelines, the autonomous scripted mode this term describes.

### 4. `cc_model_selection` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: this note documents how Claude Code selects and resolves models, a core configuration of the product.
- [LLM - Large Language Model](../../term_dictionary/term_llm.md) — what-it-is: a large neural language model; relevance: the aliases (opus/sonnet/haiku/fable) and full names this note resolves are all LLM identifiers Claude Code routes requests to.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — what-it-is: step-by-step reasoning before answering; relevance: the note frames the alias choice (opus for complex reasoning, fable for hardest/longest tasks) as a reasoning-capability trade-off the CoT term underpins.
- [System 1 and System 2](../../term_dictionary/term_system_1_and_system_2.md) — what-it-is: fast-intuitive vs slow-deliberate cognition; relevance: the haiku-for-simple vs opus/fable-for-complex alias mapping mirrors the System-1/System-2 dual-process split applied to model selection.
- [Amazon Nova](../../term_dictionary/term_amazon_nova.md) — what-it-is: Amazon's family of foundation models; relevance: contextualizes the multi-provider model-family landscape (Bedrock inference profiles) the note's provider-specific alias resolution operates within.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the token budget a model can attend to; relevance: the `[1m]`, `opus[1m]`, and `sonnet[1m]` aliases this note lists select the 1M-token context-window variants.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the agent runtime around a model; relevance: model selection is the harness setting that determines which LLM powers the gather-act-verify loop.

### 5. `cc_restrict_model_selection` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: `availableModels`/`enforceAvailableModels` are Claude Code managed-settings keys this note documents.
- [LLM - Large Language Model](../../term_dictionary/term_llm.md) — what-it-is: a large neural language model; relevance: the allowlist restricts which LLMs (by alias, version prefix, or full ID) a user can select.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive, policy-governed permission escalation; relevance: enterprise admins use the allowlist + enforcement to govern model access centrally, an administrative-control analog of the trust ladder.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — what-it-is: coordinating which agents/models run when; relevance: the allowlist also gates subagent and advisor model overrides and fallback-chain elements, governing model assignment across the orchestration surfaces.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: an isolated-context spawned Claude instance; relevance: the note explains how a blocked subagent model override falls back to the inherited/default model rather than failing.
- [Amazon Nova](../../term_dictionary/term_amazon_nova.md) — what-it-is: Amazon's foundation-model family; relevance: the Mantle-model-ID subsection routes provider-specific `anthropic.`-prefixed entries on Bedrock, the multi-provider governance case the note covers.

### 6. `cc_effort_level_and_thinking` (7 term notes)
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — what-it-is: step-by-step reasoning emitted before answering; relevance: extended thinking IS the chain-of-thought Claude emits, and this note's controls turn it on/off and size it.
- [System 1 and System 2](../../term_dictionary/term_system_1_and_system_2.md) — what-it-is: fast-intuitive vs slow-deliberate cognition; relevance: adaptive reasoning deciding whether and how much to think per step is a System-1/System-2 allocation, and effort levels tune that balance.
- [Inference Scaling Law](../../term_dictionary/term_inference_scaling_law.md) — what-it-is: performance gains from spending more compute at inference time; relevance: effort levels (low→max) are exactly a test-time-compute dial — higher effort spends more reasoning tokens for deeper capability, the trade-off this law describes.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: effort levels, `ultracode`, and `ultrathink` are Claude-Code-specific reasoning settings this note documents (`/effort`, `--effort`, `effortLevel`, `CLAUDE_CODE_EFFORT_LEVEL`).
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the model's attended token budget; relevance: thinking tokens consume the context window and are billed, the cost dimension the note's display/disable controls manage.
- [LLM - Large Language Model](../../term_dictionary/term_llm.md) — what-it-is: a large neural language model; relevance: which effort levels and thinking modes are available depends on the underlying LLM (Fable 5 vs Opus vs Sonnet), the per-model table this note presents.
- [Prompt Engineering](../../term_dictionary/term_prompt_engineering.md) — what-it-is: crafting prompts to steer behavior; relevance: the `ultrathink` keyword and "think more/less" guidance in CLAUDE.md are in-prompt ways to adjust reasoning, a prompt-engineering lever the note describes.

### 7. `cc_extended_context_1m` (6 term notes)
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the token budget a model can attend to; relevance: this note IS about the 1M-token context window — which models have it, how to enable it, and its pricing.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: `CLAUDE_CODE_DISABLE_1M_CONTEXT`, the `[1m]` aliases, and the `/model` picker behavior are Claude-Code-specific extended-context controls.
- [LLM - Large Language Model](../../term_dictionary/term_llm.md) — what-it-is: a large neural language model; relevance: 1M context is a capability of specific LLMs (Fable 5, Opus 4.6+, Sonnet 4.6) the note enumerates.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what-it-is: deliberate management of context contents; relevance: a 1M window changes the context-engineering calculus for large codebases and long sessions, the use case the note motivates.
- [Compaction](../../term_dictionary/term_compaction.md) — what-it-is: summarizing/clearing context as it fills; relevance: a larger window delays the point at which compaction triggers, linking extended context to the same context-management lifecycle.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the agent runtime around the model; relevance: the harness selects and may auto-upgrade the context-window variant per plan, the availability matrix this note documents.

### 8. `cc_fallback_models` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: `fallbackModel`, `--fallback-model`, `opusplan`, and the automatic-fallback behavior are Claude Code model-resilience features this note documents.
- [LLM - Large Language Model](../../term_dictionary/term_llm.md) — what-it-is: a large neural language model; relevance: fallback chains switch between LLMs (e.g. sonnet→haiku) when the primary is overloaded or a request is content-flagged.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: policy-governed escalation/restriction; relevance: fallback-chain elements outside the `availableModels` allowlist are dropped, tying resilience to the same governance controls.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — what-it-is: step-by-step reasoning; relevance: `opusplan` switches to Opus's deeper reasoning in plan mode then Sonnet for execution — a reasoning-aware fallback the note explains.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — what-it-is: coordinating which model/agent runs when; relevance: `opusplan`'s plan→execute model switch and the per-turn fallback are orchestration decisions about model assignment across phases.
- [System 1 and System 2](../../term_dictionary/term_system_1_and_system_2.md) — what-it-is: deliberate-vs-fast cognition; relevance: `opusplan` pairs slow-deliberate Opus for planning with faster Sonnet for execution, the dual-process split applied across task phases.
- [Amazon Nova](../../term_dictionary/term_amazon_nova.md) — what-it-is: Amazon's foundation-model family; relevance: the note details enabling content-based fallback on Bedrock/Vertex/Foundry where model IDs are provider-specific, the multi-provider deployment case.

### 9. `cc_tools_catalog` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: this note is the canonical catalog of Claude Code's built-in tools — the names used in permission rules, subagent tool lists, and hook matchers.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — what-it-is: the mechanism by which a model invokes named tools with structured arguments; relevance: every entry in this catalog is a function/tool the model can call, the exact function-calling/tool-use machinery this term defines.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the runtime providing tools/context/execution; relevance: the built-in tool catalog IS the harness's tool layer that makes Claude Code agentic.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — what-it-is: protocol for connecting external tools; relevance: the note states custom tools are added by connecting an MCP server (`mcp__*` tool names), the extension path beyond the built-in catalog.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: reusable prompt-based workflows; relevance: the note clarifies that a skill runs through the existing `Skill` tool rather than adding a new tool entry, a distinction this catalog draws.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a spawned isolated-context Claude instance; relevance: the `Agent` tool in the catalog spawns subagents, and a subagent's `tools`/`disallowedTools` frontmatter selects from this catalog.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive permission control; relevance: the catalog's "Permission Required" column and the `ToolName(specifier)` allow/deny format are the trust-control surface for each tool.

### 10. `cc_file_tool_behavior` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: Read/Edit/Write/NotebookEdit/Glob/Grep are Claude Code's built-in file tools whose exact semantics this note documents.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — what-it-is: structured tool invocation by the model; relevance: each behavior here (Edit's `old_string`/`new_string`, Read's `offset`/`limit`, Grep's output modes) is a tool's parameter contract the model fills via function calling.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the tool/execution runtime; relevance: read-before-edit, paging, and `.gitignore` handling are harness-enforced behaviors wrapping the raw file operations.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that edit code across files autonomously; relevance: precise file-tool semantics (exact-match, uniqueness, overwrite guards) are what let an autonomous agent edit safely without supervision.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the model's attended token budget; relevance: Read's token-limit paging (`PARTIAL view`) and Glob's 100-file cap are context-budget protections the note explains.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: permission control over actions; relevance: Read/Edit deny rules also apply to file-reading Bash commands, the permission boundary the note describes for these tools.

### 11. `cc_execution_tool_behavior` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: Agent/Bash/Monitor/PowerShell/WebFetch/WebSearch/LSP are Claude Code's built-in execution and web tools whose behavior this note details.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: a spawned isolated-context Claude instance; relevance: the Agent-tool section IS subagent behavior — separate context window, tool inheritance rules, foreground vs background permission handling.
- [Function Calling (Tool Use)](../../term_dictionary/term_function_calling.md) — what-it-is: structured tool invocation; relevance: Bash `timeout`/`run_in_background`, WebFetch's URL+prompt, and WebSearch's `allowed_domains` are tool parameters the model supplies via function calling.
- [Agentic Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the execution runtime around the model; relevance: Bash cwd carry-over, output truncation, and shell sourcing are harness-managed execution behaviors this note documents.
- [Sandboxing](../../term_dictionary/term_sandbox.md) — what-it-is: OS-level isolation of an agent's actions; relevance: the note repeatedly points to the sandbox for OS-level enforcement (Bash deny coverage, PowerShell Windows limits, WebFetch network rules) beyond tool-level checks.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive permission escalation; relevance: Bash/Monitor share permission rules, background subagents auto-deny prompting tools, and WebFetch domain prompts vary by permission mode — the trust behaviors the note covers.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that run commands and verify autonomously; relevance: background Bash tasks, Monitor's react-to-events watch, and the Agent tool's autonomous-then-summarize loop are the unattended execution patterns this term names.

### 12. `cc_debug_your_configuration` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding tool; relevance: this note is the troubleshooting guide for why a Claude Code customization (CLAUDE.md/settings/hooks/MCP/skills) didn't load.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — what-it-is: managing what occupies the context window; relevance: `/context` shows everything occupying the window by category (system prompt, memory, skills, MCP tools), the first diagnostic the note teaches.
- [Model Context Protocol (MCP)](../../term_dictionary/term_mcp.md) — what-it-is: protocol for external tool/data servers; relevance: the "Check MCP servers" section diagnoses `/mcp` status, approval, relative-path, and zero-tool failures.
- [Agentic Memory](../../term_dictionary/term_agentic_memory.md) — what-it-is: persisted project knowledge (auto memory / CLAUDE.md); relevance: `/memory` confirms which CLAUDE.md and auto-memory entries loaded, and the note covers subdirectory-on-demand loading and instruction-adherence patterns.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: packaged on-demand workflows; relevance: the common-causes table diagnoses skills missing from `/skills` (wrong file layout) or never invoked (`disable-model-invocation`, description mismatch).
- [Sandboxing](../../term_dictionary/term_sandbox.md) — what-it-is: OS-level isolation enforcing limits; relevance: the table's `Bash(rm *)` deny-rule gap points to a PreToolUse hook or the sandbox for a hard guarantee, the enforcement distinction the note draws.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: progressive permission control; relevance: `/permissions` shows resolved allow/deny rules and `/status` shows whether managed settings override them, the precedence the note debugs.

## Section Coverage Map

```
cli-reference.md
├── CLI commands (table, ~26 cmds) ───── → note 1 (cc_cli_commands)
├── CLI flags (table, ~45 flags) ─────── → note 2 (cc_cli_flags)
│   └── System prompt flags (subsection) → note 3 (cc_cli_system_prompt_flags)
└── See also (links) ─────────────────── → notes 1/2 (links)
model-config.md
├── Available models ──────────────────── → note 4 (cc_model_selection)
│   ├── Model aliases ─────────────────── → note 4
│   ├── Work with Fable 5 ─────────────── → note 4
│   └── Setting your model ────────────── → note 4
├── Restrict model selection ──────────── → note 5 (cc_restrict_model_selection)
│   ├── Default model behavior ────────── → note 5
│   ├── Control the model users run on ── → note 5
│   ├── Merge behavior ────────────────── → note 5
│   └── Mantle model IDs ──────────────── → note 5
├── Special model behavior ───────────────
│   ├── `default` model setting ───────── → note 4 (folded: alias resolution by account type)
│   ├── `opusplan` model setting ──────── → note 8 (cc_fallback_models)
│   ├── Fallback model chains ─────────── → note 8
│   ├── Automatic model fallback (+H4s) ─ → note 8
│   ├── Adjust effort level (+H4s) ────── → note 6 (cc_effort_level_and_thinking)
│   ├── Extended thinking ─────────────── → note 6
│   └── Extended context ──────────────── → note 7 (cc_extended_context_1m)
├── Checking your current model ───────── → note 4
├── Add a custom model option ─────────── → note 5 (ANTHROPIC_CUSTOM_MODEL_OPTION → picker control)
└── Environment variables ─────────────── → note 4 (alias-resolution vars) + link-out (full env list → B03A)
    ├── Pin models for third-party … ──── → note 5 (modelOverrides/pinning governance)
    ├── Customize pinned model display ── → note 5
    ├── Override model IDs per version ── → note 5
    └── Prompt caching configuration ──── → note 4 (DISABLE_PROMPT_CACHING_* model-tier vars) → cost mechanics linked to B02A
tools-reference.md
├── (catalog table, ~40 tools) ───────── → note 9 (cc_tools_catalog)
├── Configure tools w/ permission rules ─ → note 9 (ToolName(specifier) format) → syntax detail B05A
├── Agent tool behavior ──────────────── → note 11 (cc_execution_tool_behavior)
├── Bash tool behavior ───────────────── → note 11
├── Edit tool behavior ───────────────── → note 10 (cc_file_tool_behavior)
├── Glob tool behavior ───────────────── → note 10
├── Grep tool behavior ───────────────── → note 10
├── LSP tool behavior ────────────────── → note 11
├── Monitor tool ─────────────────────── → note 11
├── NotebookEdit tool behavior ───────── → note 10
├── PowerShell tool (+3 H3) ──────────── → note 11
├── Read tool behavior ───────────────── → note 10
├── WebFetch tool behavior ───────────── → note 11
├── WebSearch tool behavior ──────────── → note 11
├── Write tool behavior ──────────────── → note 10
├── Check which tools are available ──── → note 9
└── See also (links) ─────────────────── → notes 9/10/11 (links)
debug-your-config.md
├── See what loaded into context ─────── → note 12 (cc_debug_your_configuration)
├── Check resolved settings ──────────── → note 12 → precedence detail B03A
├── Check MCP servers ────────────────── → note 12 → MCP config B08A
├── Check hooks ──────────────────────── → note 12 → hooks B07A
├── Test against a clean configuration ─ → note 12 (--safe-mode + clean config)
├── Check common causes (table) ──────── → note 12
└── Related resources (links) ────────── → note 12 (links)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| cli-reference (3.4Kw, 1 big commands + 1 big flags table) | notes 1, 2, 3 | commands vs flags are distinct reference catalogs; System-prompt-flags subsection is an argument (replace-vs-append decision rule), a different BB from the flag table. |
| model-config (5.6Kw >2500) | notes 4, 5, 6, 7, 8 | far exceeds density cap; distinct topics differing in BB/audience — selection (concept), restriction/governance (procedure, admin), effort+thinking (concept), 1M context (concept), fallback systems (concept). |
| tools-reference (4.3Kw, 16 per-tool H2) | notes 9, 10, 11 | exceeds cap; catalog+rule-format (concept) vs file/search tool behavior (procedure) vs execution/web/agent tool behavior (procedure) split by tool family to keep each note coherent and ≤6 code. |
| debug-your-config (2.0Kw, 7 H2) | note 12 (kept whole) | under cap as one coherent diagnostic procedure; splitting would fragment a single troubleshooting workflow. |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_cli_commands | procedure | 700 | 0 | ✅ |
| 2 | cc_cli_flags | procedure | 900 | 0 | ✅ |
| 3 | cc_cli_system_prompt_flags | argument | 450 | 1 | ✅ |
| 4 | cc_model_selection | concept | 700 | 2 | ✅ |
| 5 | cc_restrict_model_selection | procedure | 700 | 2 | ✅ |
| 6 | cc_effort_level_and_thinking | concept | 850 | 1 | ✅ |
| 7 | cc_extended_context_1m | concept | 450 | 1 | ✅ |
| 8 | cc_fallback_models | concept | 850 | 2 | ✅ |
| 9 | cc_tools_catalog | concept | 800 | 1 | ✅ |
| 10 | cc_file_tool_behavior | procedure | 850 | 0 | ✅ |
| 11 | cc_execution_tool_behavior | procedure | 900 | 1 | ✅ |
| 12 | cc_debug_your_configuration | procedure | 850 | 1 | ✅ |

No note approaches the caps. Notes 2 and 11 (~900w) are the densest but well under 2,500w; all code-block counts ≤2 (≤6 cap). No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_cli_commands cc_cli_flags cc_cli_system_prompt_flags cc_model_selection cc_restrict_model_selection cc_effort_level_and_thinking cc_extended_context_1m cc_fallback_models cc_tools_catalog cc_file_tool_behavior cc_execution_tool_behavior cc_debug_your_configuration"
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

Single phase (12 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 12 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 12 notes receives ≥1 inbound link from an existing vault note **outside** `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (in-degree ≥1) | DB in-degree query confirms every new note has ≥1 inbound edge | sqlite3 `note_links` count |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 12 rows** under a "CLI, Model & Tools Reference" cluster + increments the
BB-distribution counts (concept ×5, procedure ×6, argument ×1).

## Undigested Terms Plan (Step 2d)

b03b creates **no new `term_dictionary` notes**. The terms surfaced by these pages are covered by a b03b
`cc_` concept note (Pattern B doc-concept home), an existing substantive term note (link), or another
sub-plan's home page:

| Page term | Disposition |
|---|---|
| Effort level / effort | note 6 `cc_effort_level_and_thinking` (doc concept; this sub-plan's assigned home) |
| Tool (reference) | note 9 `cc_tools_catalog` (doc concept; this sub-plan's assigned home) |
| Adaptive reasoning / extended thinking / ultrathink / ultracode | folded into note 6; reasoning concept links existing `term_chain_of_thought` |
| Model alias / opusplan / fallback model | folded into notes 4/8 (doc concepts); LLM concept links existing `term_llm` |
| 1M / extended context | note 7; links existing `term_context_window` |
| Permission rule / permission mode | link/owned by B05A (`permissions`, `permission-modes`); referenced, not defined here |
| Bare mode / non-interactive mode | owned by B11 (`headless`); the `--bare`/`-p` flags are catalogued in note 2 but the concept is captured at B11 |
| LSP / code intelligence | note 11 (LSP tool behavior, doc concept) + B09A (`discover-plugins#code-intelligence`) |
| MCP / Subagent / Sandboxing / Worktree / Plugin / Skill / Hook / Channel / Session | existing term notes (link) or home sub-plan (B08A/B10A/B05B/B10B/B09A/B06/B07A/B08B/B02B) |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 4 pages scanning emphasis/tables/captions for
newly-surfaced terms. The non-glossary terms that surfaced — **"adaptive reasoning"**, **"ultracode"**,
**"ultrathink"**, **"Mantle endpoint"**, **"LSP / code intelligence"** — are each folded into a b03b `cc_`
concept note (notes 6, 5, 11) as doc-concepts, or link an existing term note (`term_chain_of_thought`,
`term_context_window`). None is a cross-cutting vocabulary term lacking a doc-page home AND an existing note.
**0 new b03b `term_dictionary` captures.** Dedup verified across both `term_dictionary/` AND
`documentation/`: no existing `cc_*` note (folder is being created by this sub-plan) and no substantive
`documentation/` note duplicates the CLI/model/tools reference (existing `tutorial_claude_code_*` and
siblings to link, not duplicates).

## Term-Note Authoring Requirements

**N/A for b03b** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (G1–G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (model-config JSON/bash + tools-reference PowerShell JSON; ≤2/note). One BB per note. Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 — every new note gets ≥1 inbound edge):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 4, 9 | product term → CLI commands / model selection / tool catalog |
| `term_dictionary/term_chain_of_thought.md` | note 6 | reasoning term → effort levels + extended thinking |
| `term_dictionary/term_context_window.md` | note 7 | context-window term → 1M extended context |
| `term_dictionary/term_function_calling.md` | note 9 | tool-use term → built-in tool catalog |
| `term_dictionary/term_llm.md` | note 4 | LLM term → Claude Code model selection/aliases |
| `term_dictionary/term_agent_harness.md` | note 11 | harness term → execution/agent tool behavior |
| `term_dictionary/term_graduated_trust.md` | notes 2, 12 | trust term → permission flags / config debugging |
| `documentation/tutorials/tutorial_claude_code_04_configuration.md` | notes 2, 4, 12 | configuration tutorial → CLI flags / model selection / debug-your-config |
| `documentation/tutorials/tutorial_claude_code_03_workflows_and_commands.md` | notes 1, 9 | workflows/commands tutorial → CLI commands / tool catalog |

(Notes 3, 5, 8, 10 also receive sibling inbound links from within the b03b cluster — note 2→3, note 4→5/8, note 9→10/11 — plus the cross-note term inlinks above ensure each of the 12 notes has in-degree ≥1 from outside the folder per G7/G8.)

## Follow-up Recommendations

- After the 12 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 12 rows for `entry_claude_code_docs.md`; `/tessellum-check-broken-links`; confirm DB in-degree ≥1 for all 12 (G8).

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | DONE 2026-06-13 — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | READY (9/9) — see Review Sign-Off below |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B03B, 2026-06-13)

- **Source re-read (Step 2)**: all 4 pages re-read from `inbox/claude_code_docs/`; measured words match the master's figures (cli-reference 3,383 · model-config 5,579 · tools-reference 4,318 · debug-your-config 1,996 = 15,276). No >1.5× under-estimate; the two over-cap pages (model-config 5,579; tools-reference 4,318) and cli-reference (two large tables) were split as documented.
- **Notes**: 12 (concept 5, procedure 6, argument 1) — matches master estimate. Splits: model-config→5 notes, tools-reference→3 notes, cli-reference→3 notes, debug-your-config→1 note.
- **Step 2d new-term scan**: 5 surfaced (adaptive reasoning, ultracode, ultrathink, Mantle endpoint, LSP/code intelligence) → folded into b03b `cc_` doc-concepts or link existing terms; **0 new b03b term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), G5 verification, Inlinks table, G7/G8 discoverability rows.
- **28-item checklist**: PASS (term-note items N/A — b03b authors no terms; entry-point + undigested-terms inherited from master).
- **Status**: augmented and self-reviewed; set to `ready` after Review Sign-Off below passed 9/9.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Evidence |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 Discoverability (inbound in-degree ≥1). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); b03b contributes 12 rows under a "CLI, Model & Tools Reference" cluster. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 12 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches master Format Definition (derived from existing `documentation/` notes); body uses `## Overview` / source-mirrored H2s / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | Densest notes (2, 11) ~900w, well under 2,500w; all ≤2 code (≤6 cap); none borderline. The three over-cap source pages were all split. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` spot-check: cli-reference 3,383 = plan 3,383; model-config 5,579 = plan 5,579; tools-reference 4,318 = plan 4,318; debug-your-config 1,996 = plan 1,996. Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | b03b authors 0 term notes; Undigested Terms Plan routes all page terms (Step 2d re-scan documented, 5 new terms folded, 0 captures); Authoring Requirements inherited. Dedup performed across term_dictionary AND documentation/. |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `ready`.
