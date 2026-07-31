---
tags:
  - resource
  - documentation
  - hermes_agent
  - cli
  - terminal_interface
keywords:
  - hermes cli interface
  - terminal repl
  - status bar context bar
  - slash commands quick commands
  - keybindings multiline input
  - personalities busy input mode
topics:
  - Hermes Agent
  - CLI Interface
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/cli
access_control_group: ["general"]
---

# Hermes Agent — CLI Interface

## Overview

The Hermes Agent CLI is a full terminal user interface (a REPL, not a web UI) for driving the agent from the command line. It provides multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output — built for people who live in the terminal. This note documents the day-to-day interactive surface: launch flags, the persistent status bar and its context-color thresholds, keybindings, slash/quick/skill commands, personalities, multiline input (and the `Shift+Enter` compatibility matrix), interrupting/steering/queuing (plus `Ctrl+Z` suspend), the tool-progress feed, and quiet mode. Session resume, `/background`, storage, and compression are split into the companion note [hermes_cli_session_background](hermes_cli_session_background.md).

## Running the CLI

The first-time setup is one command — `hermes setup --portal` — after which you can `hermes chat`. Launch flags:

```bash
# Start an interactive session (default)
hermes

# Single query mode (non-interactive)
hermes chat -q "Hello"

# With a specific model
hermes chat --model "anthropic/claude-sonnet-4"

# With a specific provider
hermes chat --provider nous        # Use Nous Portal
hermes chat --provider openrouter  # Force OpenRouter

# With specific toolsets
hermes chat --toolsets "web,terminal,skills"

# Start with one or more skills preloaded
hermes -s hermes-agent-dev,github-auth
hermes chat -s github-pr-workflow -q "open a draft PR"

# Resume previous sessions
hermes --continue             # Resume the most recent CLI session (-c)
hermes --resume <session_id>  # Resume a specific session by ID (-r)

# Verbose mode (debug output)
hermes chat --verbose

# Isolated git worktree (for running multiple agents in parallel)
hermes -w                         # Interactive mode in worktree
hermes -w -z "Fix issue #123"     # Single query in worktree
```

Hermes also ships a modern TUI with modal overlays, mouse selection, and non-blocking input, launched with `hermes --tui` — see [hermes_tui_interface](hermes_tui_interface.md). The `-c`/`-r` resume flags and `/background` ops are documented in [hermes_cli_session_background](hermes_cli_session_background.md).

## Interface Layout

The welcome banner shows your model, terminal backend, working directory, available tools, and installed skills at a glance.

### Status Bar

A persistent status bar sits above the input area, updating in real time:

```
 ⚕ claude-sonnet-4-20250514 │ 12.4K/200K │ [██████░░░░] 6% │ $0.06 │ 15m
```

| Element | Description |
|---------|-------------|
| Model name | Current model (truncated if longer than 26 chars) |
| Token count | Context tokens used / max context window |
| Context bar | Visual fill indicator with color-coded thresholds |
| Cost | Estimated session cost (or `n/a` for unknown/zero-priced models) |
| 🗜️ N | **Context compression count** — how many times the running session has been auto-compressed. Appears once the first compression fires. |
| ▶ N | **Active background tasks** — how many `/background` prompts are still running in the current session. Appears whenever at least one task is in flight. |
| Duration | Elapsed session time |
| ⚠ YOLO | **YOLO mode warning** — shown whenever `HERMES_YOLO_MODE` is on (either `hermes --yolo` at launch or `/yolo` toggled mid-session). Mirrors the banner-line warning so you can't forget you're in auto-approve mode. |

The bar adapts to terminal width — full layout at ≥ 76 columns, compact at 52–75, minimal (model + duration, plus the YOLO badge when active) below 52.

**Context color coding:**

| Color | Threshold | Meaning |
|-------|-----------|---------|
| Green | < 50% | Plenty of room |
| Yellow | 50–80% | Getting full |
| Orange | 80–95% | Approaching limit |
| Red | ≥ 95% | Near overflow — consider `/compress` |

Use `/usage` for a detailed breakdown including per-category costs (input vs output tokens).

### Session Resume Display

When resuming a previous session (`hermes -c` or `hermes --resume <id>`), a "Previous Conversation" panel appears between the banner and the input prompt, showing a compact recap of the conversation history. Full resume detail and configuration is documented in [hermes_sessions_lifecycle_resume](hermes_sessions_lifecycle_resume.md).

## Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Alt+Enter`, `Ctrl+J`, or `Shift+Enter` | New line (multi-line input). `Shift+Enter` requires a terminal that distinguishes it from `Enter` — see below. On Windows Terminal, `Alt+Enter` is captured by the terminal (fullscreen toggle); use `Ctrl+Enter` or `Ctrl+J` instead. |
| `Alt+V` | Paste an image from the clipboard when supported by the terminal |
| `Ctrl+V` | Paste text and opportunistically attach clipboard images |
| `Ctrl+B` | Start/stop voice recording when voice mode is enabled (`voice.record_key`, default: `ctrl+b`) |
| `Ctrl+G` | Open the current input buffer in `$EDITOR` (vim/nvim/nano/VS Code/etc.). Save and quit to send the edited text as the next prompt — ideal for long, multi-paragraph prompts. |
| `Ctrl+X Ctrl+E` | Emacs-style alternate binding for the external editor (same behavior as `Ctrl+G`). |
| `Ctrl+C` | Interrupt agent (double-press within 2s to force exit) |
| `Ctrl+D` | Exit |
| `Ctrl+Z` | Suspend Hermes to background (Unix only). Run `fg` in the shell to resume. |
| `Tab` | Accept auto-suggestion (ghost text) or autocomplete slash commands |

**Multiline paste preview.** When you paste a multi-line block, the CLI echoes a compact single-line preview (`[pasted: 47 lines, 1,842 chars — press Enter to send]`) instead of dumping the whole payload into the scrollback. The full content is still what gets sent; this is just display polish.

**Markdown stripping in final responses.** The CLI strips the most verbose markdown fences and `**bold**` / `*italic*` wrappers from *final* agent replies so they render as readable terminal prose rather than raw source. Code blocks and lists are preserved. This does not affect gateway platforms or tool results — they keep their markdown for native rendering.

## Slash Commands

Type `/` to see the autocomplete dropdown. Hermes supports a large set of CLI slash commands, dynamic skill commands, and user-defined quick commands. Common examples include `/help` (command help), `/model` (show/change the current model), `/tools` (list available tools), `/skills browse`, `/background <prompt>`, `/skin`, `/voice on`, `/voice tts`, `/reasoning high`, `/title My Session`, `/status` (model/profile/tokens/duration + a local Session recap block, pure local compute), and `/sessions` (an interactive session picker inside the classic CLI — type to filter, arrow keys to navigate, Enter to resume). Commands are case-insensitive (`/HELP` == `/help`), and installed skills also become slash commands automatically. The full built-in CLI and messaging command lists live in the Slash Commands Reference (owned by SP20).

## Quick Commands

You can define custom commands that run shell commands instantly without invoking the LLM. These work in both the CLI and messaging platforms (Telegram, Discord, etc.):

```yaml
# ~/.hermes/config.yaml
quick_commands:
  status:
    type: exec
    command: systemctl status hermes-agent
  gpu:
    type: exec
    command: nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader
  restart:
    type: alias
    target: /gateway restart
```

Then type `/status`, `/gpu`, or `/restart` in any chat. More examples are in [hermes_messaging_media_settings](hermes_messaging_media_settings.md).

## Preloading Skills at Launch

If you already know which skills you want active for the session, pass them at launch time. Hermes loads each named skill into the session prompt before the first turn; the flag works in both interactive and single-query mode:

```bash
hermes -s hermes-agent-dev,github-auth
hermes chat -s github-pr-workflow -s github-auth
```

## Skill Slash Commands

Every installed skill in `~/.hermes/skills/` is automatically registered as a slash command — the skill name becomes the command (e.g. `/gif-search funny cats`, `/axolotl help me fine-tune Llama 3 on my dataset`, `/github-pr-workflow create a PR for the auth refactor`). Typing just the skill name (e.g. `/excalidraw`) loads it and lets the agent ask what you need.

## Personalities

Set a predefined personality to change the agent's tone (`/personality pirate`, `/personality kawaii`, `/personality concise`). Built-in personalities include: `helpful`, `concise`, `technical`, `creative`, `teacher`, `kawaii`, `catgirl`, `pirate`, `shakespeare`, `surfer`, `noir`, `uwu`, `philosopher`, `hype`. You can also define custom personalities in `~/.hermes/config.yaml`:

```yaml
personalities:
  helpful: "You are a helpful, friendly AI assistant."
  kawaii: "You are a kawaii assistant! Use cute expressions..."
  pirate: "Arrr! Ye be talkin' to Captain Hermes..."
  # Add your own!
```

## Multi-line Input

There are two ways to enter multi-line messages: (1) **`Alt+Enter`, `Ctrl+J`, or `Shift+Enter`** inserts a new line; (2) **backslash continuation** — end a line with `\` to continue. Pasting multi-line text is also supported directly.

### Shift+Enter compatibility

Most terminals send the same byte sequence for `Enter` and `Shift+Enter` by default, so applications cannot distinguish them. Hermes recognises `Shift+Enter` only when the terminal sends a distinct sequence via the Kitty keyboard protocol or xterm's `modifyOtherKeys` mode.

| Terminal | Status |
|---|---|
| Kitty, foot, WezTerm, Ghostty | Distinct `Shift+Enter` enabled by default |
| iTerm2 (recent), Alacritty, VS Code terminal, Warp | Supported once the Kitty protocol is enabled in settings |
| Windows Terminal Preview 1.25+ | Supported once the Kitty protocol is enabled in settings |
| macOS Terminal.app, stock Windows Terminal (stable) | Not supported — `Shift+Enter` is indistinguishable from `Enter` |

Where the terminal cannot distinguish them, `Alt+Enter` and `Ctrl+J` continue to work everywhere. On Windows Terminal specifically, `Alt+Enter` is captured by the terminal (toggles fullscreen) and never reaches Hermes — use `Ctrl+Enter` (delivered as `Ctrl+J`) or `Ctrl+J` directly for a newline.

## Interrupting the Agent

You can interrupt the agent at any point: type a new message + Enter while the agent is working (it interrupts and processes your new instructions); `Ctrl+C` interrupts the current operation (press twice within 2s to force exit). In-progress terminal commands are killed immediately (SIGTERM, then SIGKILL after 1s). Multiple messages typed during interrupt are combined into one prompt.

### Busy Input Mode

The `display.busy_input_mode` config key controls what happens when you press Enter while the agent is working:

| Mode | Behavior |
|------|----------|
| `"interrupt"` (default) | Your message interrupts the current operation and is processed immediately |
| `"queue"` | Your message is silently queued and sent as the next turn after the agent finishes |
| `"steer"` | Your message is injected into the current run via `/steer`, arriving at the agent after the next tool call — no interrupt, no new turn |

```yaml
# ~/.hermes/config.yaml
display:
  busy_input_mode: "steer"   # or "queue" or "interrupt" (default)
```

`"queue"` mode is useful when you want to prepare follow-up messages without accidentally canceling in-flight work. `"steer"` mode is useful when you want to redirect the agent mid-task without interrupting. Unknown values fall back to `"interrupt"`. `"steer"` has two automatic fallbacks: if the agent hasn't started yet, or if images are attached, the message falls back to `"queue"` behavior so nothing is lost. You can also change it inside the CLI with `/busy queue`, `/busy steer`, `/busy interrupt`, or `/busy status`. The very first time you press Enter while Hermes is working, it prints a one-line reminder explaining the `/busy` knob; it fires once per install (latched by `onboarding.seen.busy_input_prompt` in `config.yaml` — delete that key to see it again).

### Suspending to Background

On Unix systems, press **`Ctrl+Z`** to suspend Hermes to the background — just like any terminal process. The shell prints `Hermes Agent has been suspended. Run `fg` to bring Hermes Agent back.` Type `fg` in your shell to resume the session exactly where you left off. This is not supported on Windows.

## Tool Progress Display

The CLI shows animated feedback as the agent works — a kawaii thinking animation during API calls (e.g. `◜ (｡•́︿•̀｡) pondering... (1.2s)`) and a tool execution feed showing each tool call with its emoji, arguments, and elapsed time (e.g. `┊ 💻 terminal `ls -la` (0.3s)`, `┊ 🔍 web_search (1.2s)`, `┊ 📄 web_extract (2.1s)`). Cycle through display modes with `/verbose`: `off → new → all → verbose`. This command can also be enabled for messaging platforms (see [hermes_messaging_media_settings](hermes_messaging_media_settings.md)).

### Tool Preview Length

The `display.tool_preview_length` config key controls the maximum number of characters shown in tool call preview lines (e.g. file paths, terminal commands). The default is `0`, which means no limit — full paths and commands are shown. This is useful on narrow terminals or when tool arguments contain very long file paths.

## Quiet Mode

By default, the CLI runs in quiet mode which suppresses verbose logging from tools, enables kawaii-style animated feedback, and keeps output clean and user-friendly. For debug output, use `hermes chat --verbose`.

**Source**: `inbox/hermes_agent_docs/user-guide/cli.md` · https://hermes-agent.nousresearch.com/docs/user-guide/cli
**Last Updated**: 2026-06-19
**Status**: Active
