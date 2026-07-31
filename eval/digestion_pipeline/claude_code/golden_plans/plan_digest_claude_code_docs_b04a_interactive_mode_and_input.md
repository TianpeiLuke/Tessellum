---
title: Sub-Plan B04A — Claude Code Docs: Interactive Mode & Input
date: 2026-06-13
status: completed
source_url: https://code.claude.com/docs/en
master_plan: plan_digest_claude_code_docs_master.md
pages: ["interactive-mode", "keybindings", "terminal-config", "fast-mode", "voice-dictation"]
---

# Sub-Plan B04A: Interactive Mode & Input

> Self-contained sub-plan of [`plan_digest_claude_code_docs_master.md`](plan_digest_claude_code_docs_master.md).
> Structure mirrors the accepted PILOT [`plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md`](plan_digest_claude_code_docs_b01a_foundations_and_mental_model.md)
> section-for-section. Shared routing / format / dedup / gates / term-note authoring requirements are
> inherited from the master; this file extends, never overrides.

## Scope

The 5 pages that document how a human drives a Claude Code interactive (REPL) session: keyboard
shortcuts and input modes, customizable keybindings, terminal configuration (Shift+Enter, Option-as-Meta,
bell, tmux, themes, vim), fast mode (low-latency Opus), and voice dictation. P2 (Phase B) — these are
surface/input features built on the foundational vocabulary defined by Phase A cores. Reference-table
heavy; the digest preserves decision-relevant structure, not exhaustive keystroke transcription.

**Source**: Claude Code docs (`code.claude.com/docs/en`), 5 pages, 12,677 measured words. **Planned: 9 notes.**

## Content Strategy

- **Prioritize**: the input/control concepts a daily operator needs — interrupt/steer keys, multiline,
  shell mode, command history, vim mode, keybinding customization, fast-mode toggle, voice toggle.
- **Group**: split `interactive-mode` (3.6Kw, mixed) into shortcuts vs input-modes vs session-features;
  split `keybindings` (2.9Kw) into the procedure (config file mechanics) vs the action reference (tables);
  split `terminal-config` (2.6Kw) into terminal symptom-fixes vs the theme/custom-theme procedure. Keep
  `fast-mode` and `voice-dictation` each as one note.
- **Skip / link-out (own other sub-plans)**: full command list → `cc_commands` (B06); permission modes →
  B05A; fullscreen rendering / `/tui` → B04B; status line → B04B; checkpointing/rewind → B02B; settings
  keys + env vars → B03A; model-config / effort level → B03B; hooks (Notification hook) → B07A/B07B; prompt
  caching mechanism → B02A; data usage → B16. Referenced via links, never duplicated.
- **Terms**: no new `term_dictionary` captures (Pattern B); existing terms linked (see Undigested Terms Plan).

## Source Pages (Measured 2026-06-13, re-read)

All 5 pages re-read from `inbox/claude_code_docs/` (verbatim mirror of `code.claude.com/docs/en/<slug>.md`).

| Page | URL slug | Words | Code | H2 | H3 | Primary BB |
|------|----------|------:|-----:|---:|---:|-----------|
| interactive-mode | /interactive-mode | 3,577 | 4 | 9 | 16 | concept |
| keybindings | /keybindings | 2,871 | 4 | 8 | 21 | procedure/concept |
| terminal-config | /terminal-config | 2,639 | 7 | 8 | 1 | procedure |
| fast-mode | /fast-mode | 1,352 | 2 | 6 | 2 | concept |
| voice-dictation | /voice-dictation | 2,238 | 6 | 7 | 1 | procedure |

> **H2 lists (document order):**
> - **interactive-mode**: Keyboard shortcuts (H3 General controls, Text editing, Theme and display, Multiline input, Quick commands, Transcript viewer, Voice input) · Commands · Vim editor mode (H3 Mode switching, Navigation, Editing, Text objects, Visual mode) · Command history (H3 Reverse search with Ctrl+R) · Background bash commands (H3 How backgrounding works, Shell mode with `!` prefix) · Prompt suggestions · Side questions with /btw · Task list · Session recap · PR review status · See also
> - **keybindings**: Configuration file · Contexts · Available actions (H3 App/History/Chat/Autocomplete/Confirmation/Permission/Transcript/HistorySearch/Task/Theme/Help/Tabs/Attachments/Footer/MessageSelector/Diff/ModelPicker/Select/Plugin/Settings/Doctor/Voice/Scroll actions) · Keystroke syntax (H3 Modifiers, Uppercase letters, Chords, Special keys) · Unbind default shortcuts · Reserved shortcuts · Terminal conflicts · Vim mode interaction · Validation
> - **terminal-config**: Enter multiline prompts · Enable Option key shortcuts on macOS · Get a terminal bell or notification (H3 Play a sound with a Notification hook) · Configure tmux · Match the color theme (H3 Create a custom theme) · Switch to fullscreen rendering · Paste large content · Edit prompts with Vim keybindings · Related resources
> - **fast-mode**: Toggle fast mode · Understand the cost tradeoff · Decide when to use fast mode (H3 Fast mode vs effort level) · Requirements (H3 Enable fast mode for your organization, Require per-session opt-in) · Handle rate limits · Research preview · See also
> - **voice-dictation**: Requirements · Enable voice dictation · Hold to record · Tap to record and send · Change the dictation language · Rebind the dictation key · Troubleshooting (H3 Terminal not listed in macOS Microphone settings) · See also

## Planned Notes (LOCKED — Augmentation 2026-06-13)

Each note holds ONE building_block, ≤2,500 words, ≤6 code blocks, ≤400 lines. Prefix `cc_`, target
`resources/documentation/claude_code/`. **9 notes** (matches master estimate).

| # | Filename (`resources/documentation/claude_code/`) | BB | Source Section(s) | ~Words | Description |
|---|---|---|---|---:|---|
| 1 | `cc_interactive_mode_keyboard_shortcuts.md` | concept | interactive-mode: Keyboard shortcuts (General, Text editing, Theme/display, Quick commands, Transcript viewer, Voice input) | 650 | The keyboard-shortcut surface: interrupt/steer (Ctrl+C, Esc, Esc+Esc rewind), editing keys, mode toggles (Shift+Tab, Option+P/T/O), transcript viewer keys, `/ ! @` prefixes. Customization → note 4; rewind → B02B; permission modes → B05A. |
| 2 | `cc_input_modes_and_editing.md` | concept | interactive-mode: Multiline input, Vim editor mode, Command history (+ reverse search) | 700 | Five multiline methods; vim editor mode (modes/motions/text-objects/visual); per-dir command history + Ctrl+R reverse search (scope cycling). Terminal setup for Shift+Enter → note 6; rebinding → note 4. |
| 3 | `cc_interactive_session_features.md` | concept | interactive-mode: Background bash + shell `!`, Prompt suggestions, /btw, Task list, Session recap, PR review status | 700 | In-session helpers: background bash + `!` shell mode, grayed prompt suggestions, `/btw` ephemeral side questions, Ctrl+T task list, session recap, PR-review footer badge. Commands list → `cc_commands` (B06); subagent contrast → note links. |
| 4 | `cc_keybindings_customization.md` | procedure | keybindings: Configuration file, Keystroke syntax, Unbind, Reserved, Terminal conflicts, Vim mode interaction, Validation | 650 | How to customize: `~/.claude/keybindings.json` schema (`bindings` blocks by context), keystroke syntax (modifiers/chords/uppercase/special), unbind with `null`, reserved keys, tmux/screen conflicts, vim interaction, `/doctor` validation. Action names → note 5. |
| 5 | `cc_keybindings_action_reference.md` | concept | keybindings: Contexts, Available actions (all `namespace:action` tables) | 700 | Reference of bindable contexts (Global/Chat/Transcript/Scroll/…) and `namespace:action` actions with defaults (app/history/chat/scroll/voice/…). The vocabulary note 4's config file maps keys onto. |
| 6 | `cc_terminal_configuration.md` | procedure | terminal-config: multiline (Shift+Enter/`terminal-setup`), Option-as-Meta, bell/notification, tmux, fullscreen, paste | 650 | Symptom-driven terminal fixes: enable Shift+Enter (`/terminal-setup`), Option-as-Meta per terminal, terminal bell / desktop notification + Notification hook, tmux passthrough/extended-keys, large-paste collapse, switch-to-fullscreen pointer. Themes → note 7; fullscreen detail → B04B; hooks → B07. |
| 7 | `cc_terminal_themes.md` | procedure | terminal-config: Match the color theme, Create a custom theme (+ Color token reference) | 600 | Theme selection (`/theme`, auto light/dark) and custom themes: `~/.claude/themes/<slug>.json` (`name`/`base`/`overrides`), accepted color formats, hot-reload, the color-token groups (text/status/input/diff/fullscreen/usage/shimmer/subagent). |
| 8 | `cc_fast_mode.md` | concept | fast-mode: entire page | 600 | Low-latency Opus configuration (`/fast`, up to 2.5x faster, same quality, higher per-token cost); cost-tradeoff + prompt-cache interaction; when to use vs effort level; requirements (Anthropic API/subscription only, usage credits, admin enablement); per-session opt-in; rate-limit fallback; research preview. |
| 9 | `cc_voice_dictation.md` | procedure | voice-dictation: entire page | 700 | Speak prompts (`/voice` hold/tap modes); requirements (Claude.ai account, local mic, not on Bedrock/Vertex/Foundry/API-key/HIPAA); enable + settings; hold vs tap behavior; dictation language; rebind `voice:pushToTalk`; troubleshooting (mic permission, WSL, macOS tccutil). |

**Estimate: 9 notes** — concept ×5 (notes 1,2,3,5,8), procedure ×4 (notes 4,6,7,9). All single-BB, all within caps.

## Summary Statistics & Building Block Distribution

- Source pages: 5 (12,677 words). New `cc_` notes: 9. New `term_dictionary` notes: 0 (Pattern B).
- Est. total digest words: ~5,950 (avg ~660/note). Code blocks per note ≤4 (keybindings JSON, settings JSON, tmux/theme snippets) — well within the 6-block cap.
- **Building Block Distribution**: concept ×5 (notes 1,2,3,5,8) · procedure ×4 (notes 4,6,7,9). No model/argument/empirical_observation in this sub-plan.

## Per-Note Related Notes Mapping (LOCKED — Augmentation 2026-06-13)

> rendered in each note's `## Related Notes` reference section as `- [Term](../../term_dictionary/term_*.md) — relevance`.
> Sibling `cc_*` links + the entry-point back-link (`entry_claude_code_docs.md`, at finalization) are *additional*.

### 1. `cc_interactive_mode_keyboard_shortcuts` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The agentic coding CLI whose interactive REPL these shortcuts drive; the term is the product anchor for the entire keyboard-control surface this note documents.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The shortcuts are the human-control layer of the harness that wraps the model with tools; relevance: keys like Esc (interrupt mid-turn) and Shift+Tab (cycle permission modes) are how the operator steers the harness loop.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Shift+Tab / Alt+M cycle the permission modes (default, acceptEdits, plan, auto, bypassPermissions); relevance: this note's mode-toggle shortcut is the in-session control over the graduated-trust ladder.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — Option+T / Alt+T toggle extended thinking, the deliberate-reasoning mode; relevance: the note documents the keystroke that turns the thinking budget on or off per session.
- [Subagent](../../term_dictionary/term_subagent.md) — Ctrl+X Ctrl+K stops all running background subagents; relevance: the shortcut table includes subagent control, so the subagent concept grounds that row.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — Interrupt/steer keys (Ctrl+C, Esc) let a human redirect the agent mid-turn while it keeps prior work; relevance: this is the keyboard embodiment of human-in-the-loop oversight of an autonomous agent.

### 2. `cc_input_modes_and_editing` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The CLI whose prompt-input editing modes (multiline, vim, history) this note documents; the term anchors what is being edited.
- [Cursor](../../term_dictionary/term_cursor.md) — A peer AI coding tool with its own editor/input model; relevance: contextualizes Claude Code's choice of a terminal prompt with vim-style editing rather than an IDE editor surface.
- [Vibe Coding](../../term_dictionary/term_vibe_coding.md) — The fluid prompt-driven coding workflow; relevance: multiline composition, command history reuse, and reverse search are the input ergonomics that make the conversational vibe-coding loop fast.
- [Context Window](../../term_dictionary/term_context_window.md) — Command history is per-working-directory and resets on `/clear`; relevance: the note explains how a new session (fresh context window) relates to retained input history, linking input mechanics to context state.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Vim editor mode and multiline input operate at the harness's prompt-input layer; relevance: the harness is what interprets the typed/edited prompt before it reaches the model.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — Reverse search (Ctrl+R) and per-directory history treat each prompt as a reusable command; relevance: the encapsulate-a-request-as-an-object idea grounds the note's command-history mechanics.

### 3. `cc_interactive_session_features` (7 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The session whose in-flight helpers (background bash, `/btw`, task list, recap, PR badge) this note documents; the term anchors the session these features run in.
- [Subagent](../../term_dictionary/term_subagent.md) — The note explicitly frames `/btw` as the inverse of a subagent (full conversation visibility, no tools, vs empty context with full tools); relevance: the subagent concept is the contrast that defines what a side question is.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Background bash, task list, and shell `!` mode are harness capabilities that run alongside the model turn; relevance: the harness is what executes and tracks these out-of-band operations.
- [Compaction](../../term_dictionary/term_compaction.md) — The note states the task list persists across context compactions so Claude stays organized; relevance: compaction is the context-management event the task-list persistence is designed to survive.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — The task list tracks multi-step autonomous work and `/btw` runs while Claude is working; relevance: these features support the long-running autonomous-agent operating mode this term defines.
- [Context Window](../../term_dictionary/term_context_window.md) — `/btw` answers are ephemeral and never enter conversation history, and prompt suggestions reuse the prompt cache; relevance: both features are explicitly designed to avoid bloating the context window, the cost lens of this note.
- [Latency](../../term_dictionary/term_latency.md) — Prompt suggestions run as a low-cost background request that reuses the cache and are skipped when the cache is cold; relevance: the note's cost/latency tradeoffs for background helpers tie directly to response-latency concerns.

### 4. `cc_keybindings_customization` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The CLI whose shortcuts the `keybindings.json` file remaps; the term anchors what the customization targets.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Keybindings operate at the harness component level (toggle todos, submit, cancel) distinct from text-input vim motions; relevance: the note's vim-vs-keybindings separation is a statement about the harness's input architecture.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — Each binding maps a keystroke to a `namespace:action` (an encapsulated command); relevance: the keystroke-to-action indirection this note configures is a literal command-pattern dispatch table.
- [VS Code](../../term_dictionary/term_vscode.md) — The note's contexts/conflicts discussion references terminal-emulator behavior (VS Code among them) and `/terminal-setup`; relevance: VS Code is one of the host surfaces whose key handling affects which bindings work.
- [tmux conflicts → Multi-Agent](../../term_dictionary/term_multi_agent.md) — The note documents Ctrl+X Ctrl+K to stop background subagents and chord conflicts with tmux; relevance: managing multiple concurrent agent/task bindings is the multi-agent coordination surface keybindings expose.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `chat:cycleMode` (Shift+Tab) and `confirm:cycleMode` are bindable actions that cycle permission modes; relevance: the permission-mode ladder is one of the actions the keybindings file can rebind.

### 5. `cc_keybindings_action_reference` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The CLI whose complete bindable action vocabulary this reference enumerates; the term anchors the action namespaces.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — The contexts (Global/Chat/Transcript/Confirmation/Task/…) are the harness UI states each action set applies in; relevance: the action taxonomy is a map of the harness's interactive components.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — Every entry is a `namespace:action` identifier (app:interrupt, chat:submit, voice:pushToTalk); relevance: this note IS the catalog of commands the command-pattern dispatch resolves.
- [Subagent](../../term_dictionary/term_subagent.md) — `chat:killAgents` and `task:background` actions control background subagents/tasks; relevance: the subagent concept grounds the agent-control rows of the action reference.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `chat:cycleMode` / `confirm:cycleMode` cycle permission modes; relevance: the permission-mode ladder appears directly as bindable actions in this reference.
- [Voice Wake](../../term_dictionary/term_voice_wake.md) — `voice:pushToTalk` is a bindable Chat-context action enabled when dictation is on; relevance: the wake/activation-key concept grounds the voice-action row of this reference.

### 6. `cc_terminal_configuration` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The CLI whose terminal-side signal handling (Shift+Enter, Option-as-Meta, bell, tmux) this note fixes; the term anchors what the terminal feeds input to.
- [VS Code](../../term_dictionary/term_vscode.md) — The note's `/terminal-setup` writes Shift+Enter bindings and `macOptionIsMeta`/`gpuAcceleration` settings specifically for VS Code (and Cursor/Devin/Alacritty/Zed); relevance: VS Code is a primary terminal-config target.
- [Cursor](../../term_dictionary/term_cursor.md) — Cursor is one of the editors `/terminal-setup` configures for Shift+Enter; relevance: contextualizes the editor-terminal class the note's setup procedure targets.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Terminal config is about getting the host terminal to send correct signals to the harness; relevance: the harness is the consumer of the keys/notifications this terminal setup enables.
- [Latency](../../term_dictionary/term_latency.md) — The note recommends the `terminal_bell`/desktop notification so you can switch to other work while a long task runs; relevance: notifications mitigate perceived latency of long autonomous turns.
- [Human-in-the-Loop](../../term_dictionary/term_human_in_the_loop.md) — Notifications fire when Claude finishes or pauses for a permission prompt; relevance: the bell/notification setup is what summons the human back for human-in-the-loop approval.

### 7. `cc_terminal_themes` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — The CLI whose `/theme` system and custom-theme JSON this note documents; the term anchors the interface being themed.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Theme tokens color the harness's interactive elements (spinner, diff backgrounds, permission borders, mode indicators); relevance: the token reference is a map of the harness UI surfaces.
- [Subagent](../../term_dictionary/term_subagent.md) — The note documents eight `<color>_FOR_SUBAGENTS_ONLY` tokens that color each subagent/parallel task distinctly in the transcript; relevance: subagent color-coding is a dedicated theme-token group.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — Theme tokens include `planMode`, `autoAccept`, and the auto-mode `warning` border; relevance: the permission-mode indicators the theme colors are the visual signal of the trust ladder.
- [VS Code](../../term_dictionary/term_vscode.md) — The `ide` token colors the IDE connection indicator; relevance: the IDE surface (VS Code) has a dedicated theme token, tying themes to the editor integration.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — The `ultrathink`/`ultraplan` rainbow-gradient tokens render the deep-reasoning keywords; relevance: extended-thinking activation has its own theme rendering documented here.

### 8. `cc_fast_mode` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Fast mode is a Claude Code CLI feature (`/fast`); the term anchors the product whose latency it changes.
- [Latency](../../term_dictionary/term_latency.md) — Fast mode makes Opus up to 2.5x faster (lower response latency) at higher cost; relevance: latency reduction is the entire point of the feature this note documents.
- [Throughput](../../term_dictionary/term_throughput.md) — Fast mode prioritizes speed over cost efficiency via a different API configuration; relevance: the speed-vs-cost serving tradeoff is a throughput/latency engineering decision the note explains.
- [Prompt Caching](../../term_dictionary/term_prompt_caching.md) — The note details that enabling fast mode mid-conversation pays the full uncached input price once, tied to how fast mode interacts with the prompt cache; relevance: prompt caching is the cost mechanism behind the start-early recommendation.
- [Chain of Thought](../../term_dictionary/term_chain_of_thought.md) — The note compares fast mode vs effort level and notes Fable 5 always uses extended thinking; relevance: the effort/thinking dimension is the speed lever fast mode is contrasted against.
- [Context Window](../../term_dictionary/term_context_window.md) — Fast-mode pricing is flat across the full 1M-token context window and the first-enable cost scales with conversation depth; relevance: the context window is the unit the note's cost model is denominated in.

### 9. `cc_voice_dictation` (6 term notes)
- [Claude Code](../../term_dictionary/term_claude_code.md) — Voice dictation is a Claude Code CLI/VS Code feature (`/voice`); the term anchors the product the spoken prompts drive.
- [Realtime Transcription](../../term_dictionary/term_realtime_transcription.md) — Speech is transcribed live into the prompt input, dimmed until finalized, streamed to Anthropic's servers; relevance: this note IS Claude Code's real-time speech-to-text transcription feature.
- [Voice Wake](../../term_dictionary/term_voice_wake.md) — Dictation is triggered by a push-to-talk key (`voice:pushToTalk`, default Space) in hold or tap mode; relevance: the wake/activation-key trigger is the core interaction model this note documents.
- [Voice Call](../../term_dictionary/term_voice_call.md) — The feature captures microphone audio with hold/tap recording and silence/2-minute cutoffs; relevance: the voice-audio capture concepts ground the note's recording-session mechanics.
- [VS Code](../../term_dictionary/term_vscode.md) — The VS Code extension supports voice dictation with the same Claude.ai requirement but not in Remote/SSH/Dev-Container sessions; relevance: VS Code is a documented voice surface with its own constraints.
- [Latency](../../term_dictionary/term_latency.md) — Hold mode has a key-repeat warmup before recording while tap/modifier combos start on first keypress; relevance: the warmup-latency tradeoff between input modes is a usability point the note explains.

## Section Coverage Map

```
interactive-mode.md
├── Keyboard shortcuts (intro Note: Option-as-Meta) ─ → note 1 (+ → note 6 for terminal setup)
│   ├── General controls ───────────────────────── → note 1
│   ├── Text editing ───────────────────────────── → note 1
│   ├── Theme and display ──────────────────────── → note 1 (+ themes → note 7)
│   ├── Multiline input ────────────────────────── → note 2
│   ├── Quick commands (/ ! @) ─────────────────── → note 1 (shell ! detail → note 3)
│   ├── Transcript viewer ──────────────────────── → note 1 (rebind → note 4; fullscreen → B04B)
│   └── Voice input ────────────────────────────── → note 1 → note 9
├── Commands ─────────────────────────────────────  → linked out (cc_commands B06); summarized note 1/3
├── Vim editor mode (+ all H3) ─────────────────── → note 2
├── Command history (+ Reverse search Ctrl+R) ──── → note 2
├── Background bash commands (+ shell ! prefix) ── → note 3
├── Prompt suggestions ─────────────────────────── → note 3
├── Side questions with /btw ───────────────────── → note 3
├── Task list ──────────────────────────────────── → note 3
├── Session recap ──────────────────────────────── → note 3
├── PR review status ───────────────────────────── → note 3
└── See also ───────────────────────────────────── → notes 1/3 (links: skills B06, checkpointing B02B, CLI B03B, settings B03A, memory B02B)
keybindings.md
├── Configuration file ─────────────────────────── → note 4
├── Contexts ───────────────────────────────────── → note 5
├── Available actions (all 23 sub-tables) ──────── → note 5
├── Keystroke syntax (Modifiers/Uppercase/Chords/Special) → note 4
├── Unbind default shortcuts ───────────────────── → note 4
├── Reserved shortcuts ─────────────────────────── → note 4
├── Terminal conflicts ─────────────────────────── → note 4
├── Vim mode interaction ───────────────────────── → note 4 (vim key table → note 2)
└── Validation ─────────────────────────────────── → note 4
terminal-config.md
├── Enter multiline prompts ────────────────────── → note 6 (vim newline → note 2; rebind → note 4)
├── Enable Option key shortcuts on macOS ───────── → note 6
├── Get a terminal bell or notification ────────── → note 6
│   └── Play a sound with a Notification hook ──── → note 6 (full hook ref → B07A/B07B)
├── Configure tmux ─────────────────────────────── → note 6
├── Match the color theme ──────────────────────── → note 7
│   └── Create a custom theme (+ token reference) ─ → note 7
├── Switch to fullscreen rendering ─────────────── → note 6 pointer (full detail → B04B fullscreen.md)
├── Paste large content ────────────────────────── → note 6
├── Edit prompts with Vim keybindings ──────────── → note 2 (cross-linked from note 6)
└── Related resources ──────────────────────────── → notes 6/7 (links)
fast-mode.md
├── Toggle fast mode ───────────────────────────── → note 8
├── Understand the cost tradeoff ───────────────── → note 8 (prompt-cache mechanism → B02A)
├── Decide when to use fast mode (+ vs effort level) → note 8 (effort level → B03B)
├── Requirements (+ org enable, per-session opt-in) → note 8 (settings/env → B03A; cloud providers → B14A)
├── Handle rate limits ─────────────────────────── → note 8
├── Research preview ───────────────────────────── → note 8
└── See also ───────────────────────────────────── → note 8 (links: model-config B03B, costs B02A, statusline B04B)
voice-dictation.md
├── Requirements ───────────────────────────────── → note 9 (data usage → B16; providers → B14A; agent view → B10A)
├── Enable voice dictation ─────────────────────── → note 9
├── Hold to record ─────────────────────────────── → note 9
├── Tap to record and send ─────────────────────── → note 9
├── Change the dictation language ──────────────── → note 9
├── Rebind the dictation key ───────────────────── → note 9 (keybinding syntax → note 4/5)
├── Troubleshooting (+ macOS mic settings) ─────── → note 9
└── See also ───────────────────────────────────── → note 9 (links: keybindings note 4/5, settings B03A, interactive-mode note 1, commands B06)
```
No orphaned sections.

## Split Decisions

| Original | Split into | Rationale |
|---|---|---|
| interactive-mode (3.6Kw, 9 H2 mixed) | notes 1,2,3 + link-outs | distinct concepts: keyboard-shortcut surface (1) vs input/editing modes incl. vim+history (2) vs in-session features incl. background bash/`/btw`/task list/recap/PR (3); commands list owned by B06 |
| keybindings (2.9Kw, 23 action sub-tables) | notes 4,5 | the *procedure* (config-file mechanics, syntax, unbind, conflicts, validation) differs in BB from the *reference* (contexts + action tables); each within caps when separated |
| terminal-config (2.6Kw) | notes 6,7 | symptom-driven terminal fixes (6) vs the self-contained theme/custom-theme procedure with a long token reference (7); fullscreen detail owned by B04B |
| fast-mode (1.4Kw) | note 8 (no split) | under cap; single coherent concept |
| voice-dictation (2.2Kw) | note 9 (no split) | under cap; single coherent procedure (enable→modes→language→rebind→troubleshoot) |

## Density Re-Assessment (LOCKED — Augmentation 2026-06-13)

| # | Note | BB | ~Words | ~Code | Within caps? |
|---|---|---|---:|---:|---|
| 1 | cc_interactive_mode_keyboard_shortcuts | concept | 650 | 0 | ✅ |
| 2 | cc_input_modes_and_editing | concept | 700 | 0 | ✅ |
| 3 | cc_interactive_session_features | concept | 700 | 2 | ✅ |
| 4 | cc_keybindings_customization | procedure | 650 | 3 | ✅ |
| 5 | cc_keybindings_action_reference | concept | 700 | 0 | ✅ |
| 6 | cc_terminal_configuration | procedure | 650 | 3 | ✅ |
| 7 | cc_terminal_themes | procedure | 600 | 3 | ✅ |
| 8 | cc_fast_mode | concept | 600 | 2 | ✅ |
| 9 | cc_voice_dictation | procedure | 700 | 4 | ✅ |

No note approaches the caps (≤2,500w / ≤6 code / ≤400 lines). Source is reference-table-heavy; the digest
preserves decision-relevant structure (selected tables condensed to representative rows + prose), so no
over-compression and every H2/H3 maps to a note or an explicit link-out.

## Validation Scripts

```bash
CC=vault/resources/documentation/claude_code
NOTES="cc_interactive_mode_keyboard_shortcuts cc_input_modes_and_editing cc_interactive_session_features cc_keybindings_customization cc_keybindings_action_reference cc_terminal_configuration cc_terminal_themes cc_fast_mode cc_voice_dictation"
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

Single phase (9 notes, all P2). All gates must pass before commit.

| Gate | Check | Pass Criteria | Tool |
|---|---|---|---|
| G1-Format | YAML fields/order, ≤400L/≤2500w/≤6 code, single BB, H1, `## Overview`, `## Related Notes` | 0 errors | `/tessellum-check-note-format` + `check_yaml_frontmatter.py` |
| G2-Grounding | faithful to source page, no hallucination | diff vs `inbox/claude_code_docs/<page>` |
| G3-Density+Coverage | caps met; every mapped H2/H3 present | per-note check + coverage map |
| G4-CrossRef | links resolve, source_url present, entry row queued, inlinks listed | bash link-check |
| G5-Ghost | every Related Notes / inlink target exists in DB; redirect ghosts | sqlite3 vs `notes` |
| G6-Broken | 0 broken links touching the 9 notes | `/tessellum-check-broken-links` → `/tessellum-fix-broken-links` |
| G7-Discoverability | each of the 9 notes receives ≥1 inbound link from outside `claude_code/` (Inlinks table executed; DB in-degree ≥1) | DB in-degree query at finalization |
| G8-Discoverability (entry point) | each note linked from `entry_claude_code_docs.md` (B04A rows contributed) | DB in-degree query |

## Entry Point Decision (inherited from master)

No standalone entry point. Per master (>30 total notes), the series gets `0_entry_points/entry_claude_code_docs.md`;
this sub-plan **contributes its 9 rows** under an "Interactive Mode & Input" cluster + increments the
BB-distribution counts (concept +5, procedure +4). The entry-point back-link added to each note at finalization
satisfies G8.

## Undigested Terms Plan (Step 4e)

b04a creates **no new `term_dictionary` notes** — every vocabulary term on these pages is covered by a b04a
`cc_` doc-concept note, an existing substantive term note (link), or its home sub-plan (Pattern B). Dedup
performed across **both** `term_dictionary/` AND `resources/documentation/` (no `claude_code/` folder exists
yet, so no `cc_` collisions).

| Term on these pages | Disposition |
|---|---|
| Keyboard shortcut / input mode / multiline | note 1/2 `cc_interactive_*` (doc concept) |
| Vim editor mode | note 2 (doc concept) |
| Command history / reverse search | note 2 (doc concept) |
| Shell mode (`!`) / background bash | note 3 (doc concept) |
| Side question (`/btw`) / task list / session recap / PR review status | note 3 (doc concept) |
| Keybinding / context / action (`namespace:action`) | note 4/5 (doc concept) |
| Chord / modifier / reserved shortcut | note 4 (doc concept) |
| Theme / custom theme / color token | note 7 (doc concept) |
| Fast mode | note 8 (doc concept) |
| Voice dictation / hold mode / tap mode / push-to-talk | note 9 (doc concept) |
| Subagent / MCP | existing term notes (link `term_subagent`, `term_mcp`) |
| Permission mode | link `term_graduated_trust` (exists) |
| Extended thinking | link `term_chain_of_thought` (exists) |
| Effort level | owned by B03B (`model-config`) — captured/linked there |
| Fullscreen rendering / status line | owned by B04B — linked, not duplicated |
| Command (`/command`) | owned by B06 (`commands.md`) — linked there |
| Notification hook | owned by B07A/B07B (`hooks.md`/`hooks-guide.md`) — linked there |
| Prompt caching | link `term_prompt_caching` (exists); mechanism owned by B02A |
| Checkpoint / rewind | owned by B02B (`checkpointing.md`) — linked there |

**Augmentation Step 2d re-scan (2026-06-13):** re-read all 5 pages scanning emphasis/tables/captions/code for
newly-surfaced terms. Candidates surfaced — **"tmux / terminal multiplexer", "Option-as-Meta", "BCP 47
language code", "WSLg", "research preview"** — all judged either (a) generic tooling jargon needing no vault
term note, or (b) covered by a b04a `cc_` doc note (they ARE the subject of the section that owns them). No
genuine cross-cutting vocabulary term with no doc-page home AND no existing note surfaced. **0 new B04A
`term_dictionary` captures.**

**Step 10.5f Term-Slug Specificity + Collision Audit: N/A** — B04A authors zero term notes, so there are no
slugs to audit. The collision check that matters here (do these page concepts duplicate existing notes?) was
performed: `term_claude_code`, `term_mcp`, `term_subagent`, `term_graduated_trust`, `term_chain_of_thought`,
`term_prompt_caching`, `term_voice_wake`, `term_realtime_transcription`, `term_latency` all exist → linked,
not recreated.

## Term-Note Authoring Requirements

**N/A for b04a** — it authors zero term notes (all routed above). The full requirements (YAML, file naming,
inherited from the master and apply to sub-plans that DO capture terms.

## Pacing Rules (inherited from master)

- One phase; validate all 8 gates before commit.
- **Re-read the source page before writing each note** — do NOT work from memory.
- Code blocks verbatim (keybindings JSON, settings JSON, tmux/theme snippets copied exactly from source).
  One BB per note. Each note ≤400 lines (split if a draft >350).
- Commit + push after the phase (`git pull --rebase --autostash` first; no Claude co-author trailer).
- Reindex incrementally; verify `note_links` + 0 broken links before commit.

## Inlinks (existing notes → new notes)

Add at finalization so the cluster is reachable from the broader vault (anti-island; G7 in-degree ≥1):

| Existing Note | Inlink to Add | Rationale |
|---|---|---|
| `term_dictionary/term_claude_code.md` | notes 1, 4, 8, 9 | product term → CC interactive shortcuts / keybindings / fast mode / voice |
| `term_dictionary/term_graduated_trust.md` | note 1 | permission-mode term → CC shortcut that cycles modes (Shift+Tab) |
| `term_dictionary/term_prompt_caching.md` | note 8 | prompt-cache term → CC fast-mode cost interaction |
| `term_dictionary/term_realtime_transcription.md` | note 9 | transcription term → CC voice-dictation feature |
| `term_dictionary/term_voice_wake.md` | note 9 | push-to-talk term → CC `voice:pushToTalk` |
| `term_dictionary/term_vscode.md` | note 6 | VS Code term → CC terminal-setup for the integrated terminal |

## Follow-up Recommendations

- After the 9 notes land: `/tessellum-run-incremental-update`; add the reciprocal inlinks above; queue the 9 rows
  for `entry_claude_code_docs.md` under "Interactive Mode & Input"; `/tessellum-check-broken-links`.
- Cross-link siblings at finalization: note 6 ↔ B04B `cc_fullscreen`; note 8 ↔ B03B `cc_model_config`
  (effort level) and B02A `cc_prompt_caching`; notes 4/5 ↔ note 9 (voice rebind); note 3 ↔ B06 `cc_commands`.

## Pipeline Status (Per-Sub-Plan)

| Stage | Skill | Status |
|---|---|---|
| 1. Plan | `/tessellum-plan-digestion` | **DONE** |
| 2. Augment | `/tessellum-augment-digestion-plan` | **DONE 2026-06-13** — see Augmentation Report below |
| 3. Review | `/tessellum-review-digestion-plan` | **READY 2026-06-13** — see Review Sign-Off (9/9) |
| 4. Execute | `/tessellum-execute-digestion-plan` | pending |

## Augmentation Report (B04A, 2026-06-13)

- **Source re-read (Step 2)**: all 5 pages re-read in full from `inbox/claude_code_docs/`; measured words
  (interactive-mode 3,577 · keybindings 2,871 · terminal-config 2,639 · fast-mode 1,352 · voice-dictation
  2,238 = 12,677) match the master's figure exactly. No >1.5× under-estimate; no re-split forced.
- **Notes**: 9 (concept 5, procedure 4) — within master estimate. Splits: interactive-mode→3, keybindings→2,
  terminal-config→2, fast-mode→1, voice-dictation→1 (documented in Split Decisions).
- **Per-Note Related Notes Mapping (Step 8)**: built to the **≥6 relevancy-selected term-note** standard —
  6–7 term notes per note (15 distinct `term_dictionary/` terms), each with a per-link relevancy statement;
- **Step 2d new-term scan**: candidates surfaced (tmux, Option-as-Meta, BCP 47, WSLg, research preview) →
  generic jargon or owned by a b04a `cc_` doc note; **0 new B04A term captures**.
- **Dedup**: no `claude_code/` folder exists yet → 0 `cc_` collisions; 9 existing terms confirmed and linked
  (not recreated).
- **Sections added during augment**: Content Strategy, Summary Statistics & BB Distribution, Validation
  Scripts (bash), G5/G7/G8 verification notes, Inlinks table.
- **28-item checklist**: PASS (term-note items N/A — B04A authors no terms; entry-point + undigested-terms
  inherited from master).

## Review Sign-Off (`/tessellum-review-digestion-plan`, 2026-06-13)

| # | Checkpoint | Result | Note |
|---|---|---|---|
| CP2 | 8-GATE per batch (G1–G8) | ✅ PASS | 8 gate rows present (single phase), incl. G7/G8 discoverability. |
| CP3 | Entry point specified + size-decision | ✅ PASS | Inherits master CREATE `entry_claude_code_docs.md` (326 notes >30 → CREATE required); B04A contributes 9 rows under "Interactive Mode & Input". |
| CP4 | Plan size ≤30 / split | ✅ PASS | 9 notes; overall is master + 40 sub-plans. |
| CP5 | Note format aligned w/ target dir | ✅ PASS | YAML field order matches master Format Definition / existing `documentation/` notes; body uses `## Overview` / source-mirrored H2 / `## Related Notes` / `**Source**`/`**Last Updated**`/`**Status**` footer. |
| CP6 | Borderline density → split | ✅ PASS | All 9 notes 600–700w, ≤4 code — none borderline. |
| CP7 | Source words measured (not guessed) | ✅ PASS | `wc -w` re-measured: interactive-mode 3,577, keybindings 2,871, terminal-config 2,639, fast-mode 1,352, voice-dictation 2,238 = 12,677 = master figure (±0%). |
| CP8 | Undigested Terms Plan + Authoring Requirements | ✅ PASS (N/A scope) | B04A authors 0 term notes; Undigested Terms Plan routes every page term (doc note / existing term / home sub-plan); Authoring Requirements inherited. |
| CP8f | Term-slug specificity + collision audit | ✅ PASS | N/A (0 new slugs); page-concept collision check documented (9 existing terms linked, not recreated; 0 `cc_` collisions — folder empty). |

**RESULT: 9/9 PASS → READY FOR EXECUTION.** Status `ready`.
