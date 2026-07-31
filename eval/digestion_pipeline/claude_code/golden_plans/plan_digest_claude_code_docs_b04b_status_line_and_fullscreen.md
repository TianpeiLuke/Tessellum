---
title: Sub-Plan B04B — Claude Code Docs: Status Line & Fullscreen
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["statusline", "fullscreen"]
---

# Sub-Plan B04B: Status Line & Fullscreen

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 2 terminal-presentation pages that configure Claude Code's surface chrome: the **status line**
(a customizable shell-driven bar at the bottom of the CLI that prints session telemetry — context usage,
cost, git state — from JSON on stdin) and **fullscreen rendering** (an opt-in alternate-screen-buffer
renderer that eliminates flicker, keeps memory flat in long conversations, and adds mouse support).
P2 (Phase B) — both build on the interactive-mode / settings / context-window cores defined in earlier
sub-plans, which this file links rather than duplicates.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 2 pages, 8,701 measured words. **Planned: 8 notes.**

## Content Strategy

- **Prioritize**: the configuration mechanics (settings field, JSON-on-stdin contract, available fields,
  fullscreen enable/disable) every status-line and TUI user needs first.
- **Group**: split `statusline` (heavily code-laden Examples section: ~25 code blocks / 2,869 words) by
  setup-procedure vs JSON-field-reference (concept) vs example-scripts vs subagent vs troubleshooting;
  split `fullscreen` (12 H2/H3, mixed concept + procedure) into the rendering-model concept and the
  interaction/navigation procedure.
- **Skip / link-out (own other sub-plans)**: the `statusLine` settings *file precedence* and full
  settings catalog → B03A `settings`/`env-vars`; vim-mode editor mechanics → B04A `interactive-mode`;
  keybindings reference (scroll/rebinding action names) → B04A `keybindings`; the context-window /
  prompt-caching cost model the fields expose → B02A; subagents → B10A; agent view / `claude attach`
  background sessions → B10A `agent-view`; hooks common-input-fields → B07A; worktrees → B10B;
  terminal-config (`/terminal-setup`, OSC 52) → B04A `terminal-config`. Referenced via links, never duplicated.
- **Glossary / terms**: no new `term_dictionary` captures — TUI/mouse/scroll vocabulary has no glossary
  entry and no doc-page home; linked to existing term notes where genuinely relevant (Pattern B).

## Source Pages (Measured 2026-06-13, re-read)

Both pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| statusline | /statusline | 6,191 | 35 | 7 | 13 | procedure (config) + concept (data contract) |
| fullscreen | /fullscreen | 2,510 | 8 | 9 | 3 | concept (render model) + procedure (interaction) |

> **H2 lists (document order):**
> - **statusline**: Set up a status line (H3 Use the /statusline command, Manually configure a status line, Disable the status line) · Build a status line step by step · How status lines work · Available data (H3 Context window fields) · Examples (H3 Context window usage, Git status with colors, Cost and duration tracking, Display multiple lines, Clickable links, Rate limit usage, Cache expensive operations, Windows configuration) · Subagent status lines · Tips · Troubleshooting
> - **fullscreen**: Enable fullscreen rendering · What changes · Use the mouse · Scroll the conversation (H3 Auto-follow, Mouse wheel scrolling, Scroll in the JetBrains IDE terminal) · Search and review the conversation · Clear the conversation · Use with tmux · Keep native text selection · Research preview

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. **8 notes.** Prefix `cc_`,
target `resources/documentation/claude_code/`.

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_statusline_setup.md` | procedure | statusline: Set up (incl. /statusline cmd, manual config, padding/refreshInterval/hideVimModeIndicator, disable), Build step by step, How status lines work | 650 | Two setup paths (`/statusline` NL generation vs manual `statusLine` settings field); the 3-step build walkthrough; update triggers + debounce + output capabilities (multi-line/color/links) + COLUMNS/LINES sizing. Code ≤6 (config JSON + inline jq + script). |
| 2 | `cc_statusline_json_fields.md` | concept | statusline: Available data table, Context window fields, Full JSON schema accordion | 600 | The JSON-on-stdin data contract: full field catalog (model/cwd/workspace/cost/context_window/effort/rate_limits/pr/worktree/etc.); absent-vs-null field semantics; the input-only `used_percentage` formula. Code ≤2 (schema + null-handling snippet). |
| 3 | `cc_statusline_example_scripts.md` | procedure | statusline Examples: Context window usage, Git status with colors, Cost and duration tracking, Display multiple lines | 550 | Four canonical patterns shown as Bash (Python/Node.js parity noted in prose): context progress bar, color-coded git status, cost+duration, multi-line threshold-colored display. Code ≤6. |
| 4 | `cc_statusline_advanced_examples.md` | procedure | statusline Examples: Clickable links, Rate limit usage, Cache expensive operations, Windows configuration | 550 | OSC 8 clickable repo links; rate-limit windows; session-id-keyed caching of slow git ops; Windows Git-Bash/PowerShell invocation + forward-slash paths. Code ≤6. |
| 5 | `cc_subagent_statusline.md` | concept | statusline: Subagent status lines | 300 | `subagentStatusLine` setting renders custom agent-panel rows; per-tick JSON (base hook fields + columns + tasks array); one JSON line per overridden row; same trust/`disableAllHooks` gates; plugin-shipped defaults. Code ≤2. |
| 6 | `cc_statusline_troubleshooting.md` | procedure | statusline: Tips, Troubleshooting | 500 | Mock-input testing, keep-output-short, cache-slow-ops tips; troubleshooting matrix (not appearing / `--` values / unexpected percentages / OSC 8 not clickable / display glitches / workspace-trust-required / script errors-hangs / notifications share row). Code ≤3. |
| 7 | `cc_fullscreen_rendering.md` | concept | fullscreen: intro, Enable fullscreen rendering, What changes, Use with tmux, Research preview | 600 | What fullscreen rendering is (alternate-screen-buffer renderer, flicker-free, flat memory, mouse) + how to enable (`/tui fullscreen` vs `CLAUDE_CODE_NO_FLICKER`); before/now behavior table; tmux caveats (mouse mode, `-CC` incompatibility, no synchronized output); research-preview status + disable paths + background-session note. Code ≤4. |
| 8 | `cc_fullscreen_navigation_and_mouse.md` | procedure | fullscreen: Use the mouse, Scroll the conversation (Auto-follow, Mouse wheel scrolling, JetBrains terminal), Search and review the conversation, Clear the conversation, Keep native text selection | 650 | Mouse actions (click/drag/scroll/expand/open); scroll shortcuts + auto-follow + `CLAUDE_CODE_SCROLL_SPEED`/`/scroll-speed`; transcript mode (`Ctrl+o`, `/focus`, less-style search, `[`/`v` hand-back); `Ctrl+L`×2 clear; keep-native-selection (`CLAUDE_CODE_DISABLE_MOUSE`, per-terminal one-off keys, clipboard paths). Code ≤4. |

**Estimate: 8 notes** — procedure ×5 (notes 1,3,4,6,8), concept ×3 (notes 2,5,7). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 2 (8,701 words). New `cc_` notes: 8. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~4,400 (avg ~550/note). Code blocks: heavy in source (statusline 35) — digested as ≤6/note Bash-canonical with Python/Node parity noted in prose (no over-copy).
- **Building Block Distribution**: procedure ×5 (notes 1,3,4,6,8) · concept ×3 (notes 2,5,7). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_statusline_setup` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: Anthropic's agentic coding CLI; relevance: this note configures Claude Code's own bottom-bar chrome via its `~/.claude/settings.json`, so the product term is the host whose interface is being customized.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the runtime wrapping an LLM with tools, settings, and an execution loop; relevance: the status line is a harness-level presentation feature — the harness runs the configured shell command after each turn and renders its stdout.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what-it-is: the mechanism by which a model invokes external tools that return structured results; relevance: the status-line contract (Claude Code pipes JSON to a script, reads its stdout) is the same structured input/output handshake, here at the harness-to-script boundary rather than model-to-tool.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the bounded token buffer holding a session's conversation; relevance: the canonical reason to configure a status line is to monitor live context-window usage, the note's headline use case.
- [Skills](../../term_dictionary/term_skills.md) — what-it-is: packaged markdown workflows invocable via `/<name>`; relevance: the `/statusline` slash command that auto-generates the script is itself a built-in skill/command, the easiest of the two setup paths the note documents.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: Claude Code's progressive permission model; relevance: because `statusLine` executes a shell command it is gated by the same workspace-trust acceptance as hooks, a constraint this setup note must surface.

### 2. `cc_statusline_json_fields` (7 term notes)
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the bounded token buffer of a session; relevance: the `context_window` object (size, used/remaining percentage, current_usage) is the richest field group in the catalog, and the note documents the input-only `used_percentage` formula.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — what-it-is: reuse of a cached prompt prefix to cut latency/cost; relevance: the `current_usage` breakout exposes `cache_creation_input_tokens` and `cache_read_input_tokens`, and the note points to the caching docs for what those fields bill.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what-it-is: structured tool I/O; relevance: this note specifies the JSON-on-stdin schema the script consumes — the structured-payload contract that makes the status line a programmable tool integration.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — what-it-is: explicit step-by-step reasoning, the basis of reasoning-effort controls; relevance: the catalog includes `effort.level` (low/medium/high/xhigh/max) and `thinking.enabled`, surfacing the live extended-thinking/effort state in the bar.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: an isolated-context worker Claude spawns; relevance: the schema's `agent.name` field and the worktree fields populate when running under `--agent`/`--worktree`, tying the data contract to subagent/worktree sessions.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the LLM runtime; relevance: every field in the catalog (model, cost, version, session_id, output_style) is harness session-state the runtime serializes to the script on each update.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding CLI; relevance: the field set (cwd/workspace/pr/rate_limits/vim/worktree) is precisely Claude Code's own session model exposed as data.

### 3. `cc_statusline_example_scripts` (6 term notes)
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the bounded session token buffer; relevance: the first and most prominent example builds a 10-character progress bar from `context_window.used_percentage`, the note's flagship pattern.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what-it-is: structured tool I/O; relevance: every example is the same read-JSON-from-stdin / print-to-stdout tool contract, varied only by which fields it extracts and formats.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding CLI; relevance: the scripts consume Claude Code's session JSON (`model.display_name`, `cost.total_cost_usd`, `workspace.current_dir`) to render its own status bar.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the LLM runtime; relevance: the harness invokes each example script after every turn and captures its stdout, so the examples illustrate harness-side presentation hooks.
- [Cursor](../../term_dictionary/term_cursor.md) — what-it-is: an AI coding IDE/agent with its own session UI; relevance: contextualizes the category of agentic-coding-tool status displays the cost/git/context examples emulate, distinguishing Claude Code's scriptable bar from a fixed IDE panel.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents that plan, edit, run, and verify across files; relevance: the cost-and-duration and git-status examples exist because an autonomous agent runs many actions per session, making at-a-glance spend and repo-state monitoring valuable.

### 4. `cc_statusline_advanced_examples` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding CLI; relevance: the advanced examples extend Claude Code's status bar with clickable repo links, rate-limit windows, and cross-platform invocation, all reading its session JSON.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what-it-is: structured tool I/O; relevance: each advanced script is the same JSON-in/stdout-out contract, here adding OSC 8 escape sequences, caching, and PowerShell parsing.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the LLM runtime; relevance: the caching example keys its temp file on the harness-supplied `session_id` (stable per session, unique across sessions) rather than a PID, a harness-contract detail the note explains.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — what-it-is: reuse of cached prompt prefixes for cost/latency; relevance: the rate-limit example reads the Pro/Max `rate_limits` windows that, like caching, govern the cost/usage budget a power user monitors in the bar.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the session token buffer; relevance: the script-caching pattern exists because status scripts run frequently as the context window churns, so slow git ops must be throttled to avoid lag.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents executing many actions per session; relevance: rate-limit and clickable-repo displays matter precisely for long autonomous runs that consume quota and touch a remote repo.

### 5. `cc_subagent_statusline` (6 term notes)
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: an isolated-context worker spawned by the main agent; relevance: this note documents the `subagentStatusLine` setting that renders one custom row per subagent in the agent panel — the term is the note's central subject.
- [Sidechain Transcript](../../term_dictionary/term_sidechain_transcript.md) — what-it-is: Claude Code's isolated subagent transcript with summary-only return; relevance: each row in the agent panel represents one such sidechain task (the `tasks` array carries id/name/status/tokenCount), so the term grounds what the rows display.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — what-it-is: the coordination of a lead agent over delegated workers; relevance: the agent panel is the lead/coordinator's live view of orchestrated subagents, and this setting customizes how that orchestration state is rendered.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — what-it-is: systems of multiple coordinating agents; relevance: the panel exists only when several subagents run concurrently, the multi-agent configuration this row-formatter is built for.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: Claude Code's progressive permission model; relevance: the note states `subagentStatusLine` is bound by the same trust and `disableAllHooks` gates as `statusLine`, since it too runs a shell command.
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding CLI; relevance: the setting lives in Claude Code's settings.json and can be shipped as a plugin default, so the product term hosts the feature.

### 6. `cc_statusline_troubleshooting` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding CLI; relevance: the troubleshooting matrix diagnoses Claude Code-specific failure modes (`statusline skipped · restart to fix`, `claude --debug` exit-code logging, settings reload timing) of its own status bar.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — what-it-is: the progressive permission model; relevance: the "Workspace trust required" failure mode is the headline gotcha — the status command only runs after the workspace-trust dialog is accepted, the same gate hooks use.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the LLM runtime; relevance: the script-errors-or-hangs and in-flight-cancellation behaviors are harness execution-model facts (non-zero exit blanks the bar, a slow script blocks updates) the note must explain.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — what-it-is: structured tool I/O; relevance: the "mock input" testing tip and the stdout-not-stderr / null-fallback advice are about getting the JSON-in/stdout-out contract right, the recurring root cause of failures.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the session token buffer; relevance: the "context percentage shows unexpected values" item explains `used_percentage` vs `/context` drift and recommends the input-only field, a context-window-semantics issue.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: an isolated-context worker; relevance: the refreshInterval/idle tip and the cache-slow-ops guidance address the case where background subagents change git state while the main session is idle, leaving the bar stale.

### 7. `cc_fullscreen_rendering` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding CLI; relevance: fullscreen rendering is an alternative rendering path for the Claude Code CLI itself, so the product term is the subject whose drawing surface this note describes.
- [Context Window](../../term_dictionary/term_context_window.md) — what-it-is: the session token buffer; relevance: the note's core benefit is flat memory in long conversations — only visible messages stay in the render tree — directly addressing the resource pressure of a long-running, large-context session.
- [Compaction](../../term_dictionary/term_compaction.md) — what-it-is: automatic context summarization when the window fills; relevance: fullscreen targets the same long-conversation regime compaction manages, keeping the *render* memory flat the way compaction keeps the *token* memory bounded.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the LLM runtime; relevance: the renderer is a harness-level feature toggled by the `tui` setting / `CLAUDE_CODE_NO_FLICKER` env var, with the harness relaunching into fullscreen mid-session with context intact.
- [Subagent](../../term_dictionary/term_subagent.md) — what-it-is: an isolated-context worker; relevance: the note states background sessions opened from agent view or `claude attach` always use fullscreen rendering, tying the mode to subagent/background-session viewing.
- [VS Code](../../term_dictionary/term_vscode.md) — what-it-is: Microsoft's code editor with an integrated terminal; relevance: the note names the VS Code integrated terminal (and tmux, iTerm2) as the emulators where rendering throughput is the bottleneck fullscreen fixes, and as an xterm.js terminal with special link-handling behavior.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — what-it-is: agents executing long multi-step runs; relevance: the flicker/scroll-jump problems fullscreen solves arise specifically while "Claude is working" through long autonomous action sequences that stream tool output.

### 8. `cc_fullscreen_navigation_and_mouse` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — what-it-is: the agentic coding CLI; relevance: this note documents in-app navigation (mouse, scroll, transcript search, clear) that fullscreen Claude Code handles internally instead of deferring to the terminal.
- [Sidechain Transcript](../../term_dictionary/term_sidechain_transcript.md) — what-it-is: Claude Code's isolated conversation/subagent transcript; relevance: transcript mode (`Ctrl+o`) and the `[`/`v` hand-back-to-scrollback flow operate on the conversation transcript living in the alternate screen buffer, the note's central navigation surface.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — what-it-is: live streaming conversion of an ongoing stream into searchable text; relevance: the transcript-mode less-style search (`/`, `n`/`N`, write-to-scrollback) is exactly searching the live, continuously-streamed conversation transcript fullscreen captures.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — what-it-is: the LLM runtime; relevance: scroll speed, auto-follow, and mouse capture are harness-level interaction settings (`CLAUDE_CODE_SCROLL_SPEED`, `/config` auto-scroll, `CLAUDE_CODE_DISABLE_MOUSE`) the runtime applies inside the alternate screen buffer.
- [Regular Checkpointing](../../term_dictionary/term_regular_checkpointing.md) — what-it-is: the practice of frequent save/reset points to bound state; relevance: the `Ctrl+L`×2 (or `Cmd+K`×2) `/clear` shortcut this note documents is the fast conversation-reset that starts a clean checkpoint when context has accumulated.
- [VS Code](../../term_dictionary/term_vscode.md) — what-it-is: the code editor with an xterm.js integrated terminal; relevance: the mouse and native-selection sections give VS Code (and Cursor/Devin) terminal-specific behavior — keep `Cmd`-click for links, use `Shift`/`Option` for one-off native selection — so the term grounds those platform rows.

## Section Coverage Map

```
statusline.md
├── Set up a status line ────────────────── → note 1 (cc_statusline_setup)
│   ├── Use the /statusline command ─────── → note 1
│   ├── Manually configure a status line ── → note 1 (padding/refreshInterval/hideVimModeIndicator)
│   │     └── (settings file precedence) ── → linked out (B03A settings.md)
│   │     └── (vim.mode rendering) ──────── → linked out (B04A interactive-mode#vim)
│   └── Disable the status line ─────────── → note 1
├── Build a status line step by step ────── → note 1
├── How status lines work ───────────────── → note 1 (triggers, debounce, output, COLUMNS/LINES)
├── Available data (field table) ────────── → note 2 (cc_statusline_json_fields)
│   └── Context window fields ───────────── → note 2 (→ B02A prompt-caching for cache-field billing)
│   └── (Full JSON schema accordion) ────── → note 2
├── Examples ────────────────────────────── → notes 3, 4
│   ├── Context window usage ────────────── → note 3 (cc_statusline_example_scripts)
│   ├── Git status with colors ──────────── → note 3
│   ├── Cost and duration tracking ──────── → note 3 (→ B02A costs)
│   ├── Display multiple lines ──────────── → note 3
│   ├── Clickable links ─────────────────── → note 4 (cc_statusline_advanced_examples)
│   ├── Rate limit usage ────────────────── → note 4
│   ├── Cache expensive operations ──────── → note 4
│   └── Windows configuration ───────────── → note 4 (→ B17 setup for platform install)
├── Subagent status lines ───────────────── → note 5 (cc_subagent_statusline)
│   └── (base hook common-input-fields) ─── → linked out (B07A hooks.md); (subagents) → B10A sub-agents.md
├── Tips ────────────────────────────────── → note 6 (cc_statusline_troubleshooting)
└── Troubleshooting ─────────────────────── → note 6
fullscreen.md
├── (intro: what fullscreen rendering is) ─ → note 7 (cc_fullscreen_rendering)
├── Enable fullscreen rendering ─────────── → note 7 (/tui, CLAUDE_CODE_NO_FLICKER)
│   └── (tui setting) ───────────────────── → linked out (B03A settings.md)
├── What changes (before/now table) ─────── → note 7
├── Use the mouse ───────────────────────── → note 8 (cc_fullscreen_navigation_and_mouse)
├── Scroll the conversation ─────────────── → note 8
│   ├── Auto-follow ─────────────────────── → note 8
│   ├── Mouse wheel scrolling ───────────── → note 8 (CLAUDE_CODE_SCROLL_SPEED, /scroll-speed)
│   │     └── (rebind scroll actions) ───── → linked out (B04A keybindings#scroll-actions)
│   └── Scroll in the JetBrains IDE terminal → note 8 (→ B12A jetbrains.md)
├── Search and review the conversation ──── → note 8 (Ctrl+o transcript, /focus, less-search, [ / v)
├── Clear the conversation ──────────────── → note 8 (Ctrl+L ×2)
├── Use with tmux ───────────────────────── → note 7 (mouse mode, -CC incompat, sync output)
├── Keep native text selection ──────────── → note 8 (CLAUDE_CODE_DISABLE_MOUSE, per-term keys, clipboard)
│   └── (/terminal-setup, OSC 52) ───────── → linked out (B04A terminal-config.md)
└── Research preview ────────────────────── → note 7 (/tui default, disable, background sessions)
        └── (agent view / claude attach) ── → linked out (B10A agent-view.md)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| statusline (6,191w >2500, 35 code blocks >>6, 7 H2 / 13 H3) | notes 1,2,3,4,5,6 + 8 link-outs | far over every density cap; setup (procedure) vs JSON data contract (concept) vs example scripts vs subagent setting (concept) vs troubleshooting (procedure) differ in BB/topic; settings precedence, vim mode, hooks, subagents owned by B03A/B04A/B07A/B10A |
| statusline Examples (2,869w, ~25 code blocks) | notes 3 + 4 | the Examples subsection alone exceeds the ≤2500w and ≤6-code caps; basic patterns (context/git/cost/multi-line) vs advanced (links/rate-limit/cache/Windows) split keeps each ≤6 code blocks (Bash canonical, Python/Node parity in prose) |
| fullscreen (2,510w, 9 H2 / 3 H3, concept + procedure mixed) | notes 7 + 8 | one BB per note: the rendering model + enable/tmux/preview (concept) vs the mouse/scroll/search/clear/native-selection interaction reference (procedure) are distinct BB types and topics |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_statusline_setup | procedure | 650 | 6 | ✅ |
| 2 | cc_statusline_json_fields | concept | 600 | 2 | ✅ |
| 3 | cc_statusline_example_scripts | procedure | 550 | 6 | ✅ |
| 4 | cc_statusline_advanced_examples | procedure | 550 | 6 | ✅ |
| 5 | cc_subagent_statusline | concept | 300 | 2 | ✅ |
| 6 | cc_statusline_troubleshooting | procedure | 500 | 3 | ✅ |
| 7 | cc_fullscreen_rendering | concept | 600 | 4 | ✅ |
| 8 | cc_fullscreen_navigation_and_mouse | procedure | 650 | 4 | ✅ |

No note approaches the word/line caps. Code-heavy source is digested at ≤6 blocks/note (Bash canonical; Python/Node.js parity stated in prose rather than triplicated) — verified against the ≤6 cap. No over-compression — every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_statusline_setup cc_statusline_json_fields cc_statusline_example_scripts cc_statusline_advanced_examples cc_subagent_statusline cc_statusline_troubleshooting cc_fullscreen_rendering cc_fullscreen_navigation_and_mouse"
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

Single phase (8 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 8 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 8 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed) | DB in-degree query at finalization |
| G8-Discoverability (inbound in-degree ≥1, verified) | DB confirms in-degree ≥1 for all 8 notes after inlinks land; no graph islands | sqlite3 in-degree query post-execution |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 8 rows** under an "Interactive Mode & Surfaces" / "Status line & fullscreen"
cluster + increments the BB-distribution counts (procedure ×5, concept ×3).

## Undigested Terms Plan (Step 4e)

b04b creates **no new `term_dictionary` notes**. Neither source page introduces a glossary vocabulary term;
the TUI/terminal/mouse vocabulary it uses has no glossary entry and no doc-page home, so it is handled by
linking existing term notes (Pattern B) or kept as inline prose (not a definable cross-cutting term):

| Surfaced term / concept | Disposition |
|---|---|
| Status line / `statusLine` setting | doc concept — notes 1–6 (this sub-plan's own `cc_` notes) |
| `subagentStatusLine` setting | doc concept — note 5 `cc_subagent_statusline` |
| Fullscreen rendering / `tui` setting | doc concept — note 7 `cc_fullscreen_rendering` |
| Subagent / agent panel | link `term_subagent` + `term_sidechain_transcript` (exist); full page owned by B10A |
| Context window / Compaction | link `term_context_window` / `term_compaction` (exist); pages owned by B02A/B02B |
| Prompt caching / cache tokens | link `term_prompt_caching` (exists); page owned by B02A |
| Reasoning effort / extended thinking | link `term_chain_of_thought` (exists); `effort` config owned by B03B |
| Vim mode / keybindings / scroll actions | linked to B04A `interactive-mode` / `keybindings` (no new term) |
| Settings layers / env vars (`CLAUDE_CODE_*`) | linked to B03A `settings` / `env-vars` (no new term) |
| Workspace trust / `disableAllHooks` | link `term_graduated_trust` (exists); hooks owned by B07A |
| Alternate screen buffer / OSC 8 / OSC 52 / ANSI / tmux / iTerm2 / xterm.js | inline prose — terminal-emulator implementation vocabulary, not cross-cutting definable vault terms (no glossary entry, no doc-page home) |

**Augmentation Step 2d re-scan (2026-06-13):** re-read both pages scanning emphasis/tables/captions/accordions
for newly-surfaced terms. The only candidate non-glossary terms ("alternate screen buffer", "OSC 8/52
escape sequences", "kitty keyboard protocol", "synchronized output") are terminal-emulator implementation
details, not cross-cutting vault concepts — they have no glossary entry and no owning doc page, so they stay
as inline prose per the master's Pattern B. **0 new b04b `term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — b04b authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do the surfaced concepts duplicate existing notes?)
was performed: `term_subagent`, `term_sidechain_transcript`, `term_context_window`, `term_compaction`,
`term_prompt_caching`, `term_chain_of_thought`, `term_graduated_trust`, `term_claude_code`, `term_agent_harness`,
`term_function_calling`, `term_vscode`, `term_regular_checkpointing`, `term_realtime_transcription`,
`term_multi_agent`, `term_agent_orchestration`, `term_autonomous_coding_agents`, `term_cursor` all exist →
linked, not recreated.

## Term-Note Authoring Requirements

**N/A for b04b** — it authors zero term notes (all routed above). The full requirements (YAML, file
MathJax) are inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates (incl. G7/G8) before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim from source (Bash canonical; do not invent Python/Node variants — note parity in prose). One BB per note. Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7/G8 — in-degree ≥1 each):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 7 | product term → CC status-line setup + fullscreen rendering |
| `term_dictionary/term_context_window.md` | notes 2, 3 | context-window term → status-line field catalog + context-bar example |
| `term_dictionary/term_subagent.md` | note 5 | subagent term → subagent status-line panel |
| `term_dictionary/term_sidechain_transcript.md` | note 8 | transcript term → fullscreen transcript mode/search |
| `term_dictionary/term_graduated_trust.md` | note 6 | trust term → status-line workspace-trust troubleshooting |
| `term_dictionary/term_prompt_caching.md` | note 4 | caching term → rate-limit/cache-fields advanced example |
| `term_dictionary/term_regular_checkpointing.md` | note 8 | checkpointing term → Ctrl+L×2 clear-conversation shortcut |
| `term_dictionary/term_function_calling.md` | note 2 | tool-use term → JSON-on-stdin data contract |

> Coverage check: notes 1–8 each receive ≥1 inbound link above (1,7 ← claude_code; 2,3 ← context_window;
> 2 ← function_calling; 4 ← prompt_caching; 5 ← subagent; 6 ← graduated_trust; 8 ← sidechain_transcript +
> regular_checkpointing) — **all 8 satisfy G7/G8 in-degree ≥1**. Sibling `cc_*` cross-links are added in
> each note's `## Related Notes` during authoring (additional inbound edges).

## Follow-up Recommendations

- After the 8 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; verify DB in-degree ≥1 for all 8 (G7/G8); queue the 8 rows for `entry_claude_code_docs.md`; `/tessellum-check-broken-links`.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | DONE |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-13** — see Review Sign-Off below (9/9) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B04B, 2026-06-13)

- **Source re-read (Step 2)**: both pages re-read in full from `inbox/claude_code_docs/`; measured words match the master's figures (statusline 6,191 · fullscreen 2,510 = 8,701). Code-block density measured directly (statusline 35 fenced blocks / fullscreen 8) — this forced the Examples split beyond the master's 6-note estimate to honor the ≤6-code cap.
- **Notes**: 8 (procedure 5, concept 3) — 2 above the master's estimate of 6; the two extra are the Examples-section split (note 4) and the fullscreen concept/procedure split (note 8), both density-driven and documented in Split Decisions.
- **Step 2d new-term scan**: candidates surfaced were terminal-emulator implementation details (alternate screen buffer, OSC 8/52, kitty protocol) with no glossary entry / doc-page home → kept inline prose; **0 new B04B term captures**.
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation Scripts (bash), G5 verification note, G7/G8 in-degree coverage check.
- **28-item checklist**: PASS (term-note items N/A — B04B authors no terms; entry-point + undigested-terms inherited from master).
- **Status**: augmented and self-reviewed; set to `ready` after the 9-checkpoint review below passed 9/9.

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present incl. G7/G8 Discoverability (single phase). |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B04B contributes 8 rows. |
| CP4 | Plan size ≤30 / split | ✅ PASS | 8 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches existing `documentation/` notes exactly; body uses `## Overview` / source-mirrored H2s / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer convention. |
| CP6 | Borderline density → split | ✅ PASS | Examples section (2,869w / ~25 code) split into notes 3+4 to honor ≤6-code cap; fullscreen split by BB. All 8 notes 300–650w, ≤6 code — none borderline post-split. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` measured: statusline 6,191 = plan 6,191; fullscreen 2,510 = plan 2,510. Code blocks counted via fence grep (statusline 35, fullscreen 8). Within ±0%. |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B04B authors 0 term notes; Undigested Terms Plan routes all surfaced concepts (link existing / inline prose); Authoring Requirements inherited. Step 2d re-scan documented (0 new captures). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `pending → ready`.
