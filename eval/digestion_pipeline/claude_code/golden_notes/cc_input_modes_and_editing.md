---
tags:
  - resource
  - documentation
  - claude_code
  - interactive_mode
  - input
keywords:
  - multiline input
  - vim editor mode
  - command history
  - reverse search
  - ctrl+r
  - shift+enter
  - text objects
  - visual mode
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

# Claude Code — Input Modes & Editing

## Overview

Beyond single-line typing, a Claude Code interactive session offers three richer ways to compose and edit a prompt: **multiline input** (five methods for entering line breaks without submitting), an optional **vim editor mode** (full NORMAL/INSERT/VISUAL editing with motions and text objects), and **command history** (per-working-directory recall plus `Ctrl+R` reverse search). These input mechanics let an operator draft long or structured prompts and reuse prior ones quickly, all inside the terminal prompt rather than an external editor.

This note covers the input/editing surface only. The terminal-side setup needed to make `Shift+Enter` and `Option+Enter` work is documented in [Terminal Configuration](cc_terminal_configuration.md); rebinding any of these keys is in [Keybindings Customization](cc_keybindings_customization.md); the broader keyboard-shortcut surface (interrupt/steer, mode toggles, transcript viewer) is in [Interactive Mode — Keyboard Shortcuts](cc_interactive_mode_keyboard_shortcuts.md).

## Multiline input

To enter a line break without submitting the prompt, use any of five methods:

| Method | Shortcut | Context |
| :--- | :--- | :--- |
| Quick escape | `\` + `Enter` | Works in all terminals |
| Option key | `Option+Enter` | After enabling Option as Meta on macOS |
| Shift+Enter | `Shift+Enter` | Native in iTerm2, WezTerm, Ghostty, Kitty, Warp, Apple Terminal, Windows Terminal |
| Control sequence | `Ctrl+J` | Works in any terminal without configuration |
| Paste mode | Paste directly | For code blocks, logs |

`Shift+Enter` works without configuration in iTerm2, WezTerm, Ghostty, Kitty, Warp, Apple Terminal, and Windows Terminal. For VS Code, Cursor, Devin Desktop, Alacritty, and Zed, run `/terminal-setup` to install the binding (see [Terminal Configuration](cc_terminal_configuration.md)). `Option+Enter` requires enabling Option as Meta on macOS.

## Vim editor mode

Vim-style editing is enabled via `/config` → Editor mode. It provides modal editing of the prompt input with NORMAL, INSERT, and VISUAL modes. Block-wise visual mode with `Ctrl+V` is not supported.

### Mode switching

`Esc` enters NORMAL mode from INSERT or VISUAL. From NORMAL mode: `i` inserts before the cursor, `I` at the beginning of the line, `a` after the cursor, `A` at the end of the line, `o` opens a line below, `O` opens a line above, `v` starts character-wise visual selection, and `V` starts line-wise visual selection.

### Navigation (NORMAL mode)

Movement uses the standard vim keys: `h`/`j`/`k`/`l` move left/down/up/right (`Space` also moves right). Word motions are `w` (next word), `e` (end of word), `b` (previous word). Line anchors are `0` (beginning of line), `$` (end of line), `^` (first non-blank character). Input anchors are `gg` (beginning of input) and `G` (end of input). Character search uses `f{char}` / `F{char}` (jump to next/previous occurrence) and `t{char}` / `T{char}` (jump to just before/after), with `;` repeating the last f/F/t/T motion and `,` repeating it in reverse. `/` opens reverse history search, the same as `Ctrl+R`.

In vim normal mode, if the cursor is at the beginning or end of input and cannot move further, `j`/`k` and the arrow keys navigate command history instead.

### Editing (NORMAL mode)

Deletion: `x` (character), `dd` (line), `D` (to end of line), and `dw`/`de`/`db` (word / to end / back). Change: `cc` (line), `C` (to end of line), `cw`/`ce`/`cb` (word / to end / back). Yank: `yy`/`Y` (line), `yw`/`ye`/`yb` (word / to end / back). Paste with `p` (after cursor) or `P` (before cursor). Other operators: `>>` / `<<` (indent / dedent line), `J` (join lines), `u` (undo), and `.` (repeat last change).

### Text objects (NORMAL mode)

Text objects combine with the operators `d`, `c`, and `y`: `iw`/`aw` (inner/around word), `iW`/`aW` (inner/around whitespace-delimited WORD), `i"`/`a"` and `i'`/`a'` (inner/around double or single quotes), and `i(`/`a(`, `i[`/`a[`, `i{`/`a{` (inner/around parentheses, brackets, braces).

### Visual mode

Press `v` for character-wise selection or `V` for line-wise selection. Motions extend the selection and operators act on it directly. Within VISUAL mode: `d`/`x` delete the selection, `y` yanks it, `c`/`s` change it, `p` replaces it with register contents, and `r{char}` replaces every selected character with `{char}`. `~`/`u`/`U` toggle, lowercase, or uppercase the selection; `>`/`<` indent or dedent selected lines; `J` joins them; `o` swaps cursor and anchor; text objects (`iw`/`aw`/`i"`/…) select a region; and `v`/`V` toggle between character-wise and line-wise selection or exit.

## Command history

Claude Code maintains command (prompt) history for the current session:

- Input history is stored **per working directory**.
- Input history **resets when you run `/clear`** to start a new session. The previous session's conversation is preserved and can be resumed.
- Submitting the same prompt twice in a row records one history entry, so pressing `Up` steps to the previous *distinct* prompt.
- Use `Up`/`Down` arrows to navigate (see [Interactive Mode — Keyboard Shortcuts](cc_interactive_mode_keyboard_shortcuts.md)).
- History expansion (`!`) is disabled by default.

### Reverse search with Ctrl+R

Press `Ctrl+R` to interactively search command history:

1. **Start search**: press `Ctrl+R` to activate reverse history search.
2. **Type query**: enter text to search for in previous commands; the search term is highlighted in matching results.
3. **Navigate matches**: press `Ctrl+R` again to cycle through older matches.
4. **Change scope**: search defaults to prompts from all projects. Press `Ctrl+S` to cycle the scope through this session, this project, and all projects.
5. **Accept match**: press `Tab` or `Esc` to accept the current match and continue editing, or `Enter` to accept and execute the command immediately.
6. **Cancel search**: press `Ctrl+C` to cancel and restore your original input, or `Backspace` on an empty search to cancel.

The search displays matching commands with the search term highlighted, so you can find and reuse previous inputs.

**Source**: https://code.claude.com/docs/en/interactive-mode
**Last Updated**: 2026-06-13
**Status**: Active
