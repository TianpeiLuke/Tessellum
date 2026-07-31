---
tags:
  - resource
  - documentation
  - claude_code
  - interactive_mode
  - keyboard_shortcuts
keywords:
  - keyboard shortcuts
  - interrupt and steer
  - esc esc rewind
  - cycle permission modes
  - toggle extended thinking
  - transcript viewer
  - shell mode prefix
  - voice input shortcut
topics:
  - Claude Code
  - Interactive Mode
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/interactive-mode
access_control_group: ["general"]
---

# Claude Code — Interactive Mode Keyboard Shortcuts

## Overview

Claude Code's interactive (REPL) session is driven by a surface of keyboard shortcuts that let a human start, steer, interrupt, and inspect the agent without leaving the terminal. This note documents that shortcut surface: **general controls** (interrupt, exit, mode toggles, transcript), **text-editing** keys, the **theme/display** toggle, the **quick-command prefixes** (`/`, `!`, `@`), the **transcript viewer** keys, and the **voice-input** trigger.

Shortcuts may vary by platform and terminal. On macOS, the `Option`/`Alt` shortcuts (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) require configuring **Option as Meta** in the terminal (iTerm2, Apple Terminal, or VS Code) — see [Terminal configuration](cc_terminal_configuration.md). Multiline-input methods and vim editor mode live in [Input modes and editing](cc_input_modes_and_editing.md); in-session helpers (background bash, `/btw`, task list) live in [Interactive session features](cc_interactive_session_features.md); rebinding any of these keys is covered in [Keybindings customization](cc_keybindings_customization.md).

## General controls

The interrupt/steer and mode-toggle keys are the operator's primary controls:

- `Ctrl+C` — Interrupt a running operation, or clear input. If nothing is running, the first press clears the prompt input and a second press exits Claude Code.
- `Esc` — Interrupt Claude. Stops the current response or tool call mid-turn so you can redirect; Claude keeps the work done so far.
- `Esc` + `Esc` — Clear input draft, or rewind. With text in the input, double `Esc` clears it and saves the draft to history so `Up` recalls it. When the input is empty, double `Esc` opens the rewind menu to restore or summarize code and conversation from a previous point (see [Checkpointing](https://code.claude.com/docs/en/checkpointing)).
- `Ctrl+D` — Exit Claude Code session (EOF signal).
- `Ctrl+X Ctrl+K` — Stop all running background subagents in this session; press twice within 3 seconds to confirm.
- `Ctrl+G` or `Ctrl+X Ctrl+E` — Open your prompt or custom response in your default text editor (`Ctrl+X Ctrl+E` is the readline-native binding).
- `Ctrl+L` — Redraw screen. Forces a full terminal redraw while keeping input and conversation history; use it to recover a garbled or partially blank display.
- `Ctrl+O` — Toggle the transcript viewer (detailed tool usage; also expands collapsed MCP calls).
- `Ctrl+R` — Reverse search command history (see [Input modes and editing](cc_input_modes_and_editing.md)).
- `Ctrl+V` / `Cmd+V` (iTerm2) / `Alt+V` (Windows and WSL) — Paste image from clipboard, inserting an `[Image #N]` chip at the cursor.
- `Ctrl+B` — Background running tasks (tmux users press twice); see [Interactive session features](cc_interactive_session_features.md).
- `Ctrl+T` — Toggle the task list in the terminal status area.
- `Left/Right arrows` — Cycle through dialog tabs in permission dialogs and menus.
- `Up/Down arrows` or `Ctrl+P`/`Ctrl+N` — Move the cursor within multi-row input first, then navigate command history once the cursor is on the first or last visual row.

The mode-toggle keys switch session behavior in place:

- `Shift+Tab` or `Alt+M` (some configurations) — Cycle permission modes through `default`, `acceptEdits`, `plan`, and any modes you have enabled such as `auto` or `bypassPermissions` (see [permission modes](https://code.claude.com/docs/en/permission-modes)).
- `Option+P` (macOS) / `Alt+P` (Windows/Linux) — Switch model without clearing your prompt.
- `Option+T` (macOS) / `Alt+T` (Windows/Linux) — Toggle extended thinking mode (no effect on Fable 5, which always uses extended thinking).
- `Option+O` (macOS) / `Alt+O` (Windows/Linux) — Toggle [fast mode](cc_fast_mode.md).

## Text editing

Emacs/readline-style editing keys operate on the prompt input; deletions store text for pasting with `Ctrl+Y`:

- `Ctrl+A` / `Ctrl+E` — Move cursor to start / end of the current logical line (in multiline input).
- `Ctrl+K` — Delete to end of line (stores deleted text).
- `Ctrl+U` — Delete from cursor to line start (stores deleted text; repeat to clear across lines in multiline input). On macOS, iTerm2 and Terminal.app map `Cmd+Backspace` to this.
- `Ctrl+W` — Delete previous word (stores deleted text). On Windows, `Ctrl+Backspace` also deletes the previous word.
- `Ctrl+Y` — Paste text deleted with `Ctrl+K`, `Ctrl+U`, or `Ctrl+W`.
- `Alt+Y` (after `Ctrl+Y`) — Cycle paste history. Requires Option as Meta on macOS.
- `Alt+B` / `Alt+F` — Move cursor back / forward one word. Requires Option as Meta on macOS.

## Theme and display

- `Ctrl+T` — Toggle syntax highlighting for code blocks. This works **only inside the `/theme` picker menu** and controls whether code in Claude's responses uses syntax coloring. (Outside the picker, `Ctrl+T` toggles the task list — see General controls.) Theme selection and custom themes are documented under [Match the color theme](https://code.claude.com/docs/en/terminal-config).

## Quick commands

Three single-character prefixes at the start of the input switch how the line is interpreted:

| Prefix | Behavior |
| :----- | :------- |
| `/` at start | Command or skill — opens the command/skill picker (full list in [commands](https://code.claude.com/docs/en/commands)) |
| `!` at start | Shell mode — run commands directly and add execution output to the session (detail in [Interactive session features](cc_interactive_session_features.md)) |
| `@` | File path mention — triggers file-path autocomplete |

## Transcript viewer

When the transcript viewer is open (toggled with `Ctrl+O`), these shortcuts apply. In fullscreen rendering, press `?` to show the full shortcut reference panel inside the viewer:

- `?` — Toggle the keyboard-shortcut help panel (requires fullscreen rendering).
- `{` / `}` — Jump to the previous or next user prompt, like vim paragraph motion (requires fullscreen rendering).
- `Ctrl+E` — Toggle show all content. Rebindable via `transcript:toggleShowAll` (see [Keybindings customization](cc_keybindings_customization.md)).
- `[` — Write the full conversation to your terminal's native scrollback so `Cmd+F`, tmux copy mode, and other native tools can search it (requires fullscreen rendering).
- `v` — Write the conversation to a temporary file and open it in `$VISUAL` or `$EDITOR` (requires fullscreen rendering).
- `q`, `Ctrl+C`, `Esc` — Exit transcript view. All three are rebindable via `transcript:exit`.

Fullscreen rendering detail is documented separately at [fullscreen rendering](https://code.claude.com/docs/en/fullscreen).

## Voice input

- Hold or tap `Space` — Voice dictation. Requires [voice dictation](cc_voice_dictation.md) to be enabled; hold to record, or run `/voice tap` for tap-to-toggle. The key is rebindable.

**Source**: https://code.claude.com/docs/en/interactive-mode
**Last Updated**: 2026-06-13
**Status**: Active
