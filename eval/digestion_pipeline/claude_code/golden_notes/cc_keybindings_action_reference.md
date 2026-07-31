---
tags:
  - resource
  - documentation
  - claude_code
  - keybindings
  - action_reference
keywords:
  - keybindings action reference
  - namespace action format
  - binding contexts
  - app actions
  - chat actions
  - scroll actions
  - voice push to talk
  - cycle permission modes
topics:
  - Claude Code
  - Keybindings
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/keybindings
access_control_group: ["general"]
---

# Claude Code — Keybindings Action Reference

## Overview

Claude Code's customizable keyboard shortcuts are built from two vocabularies: **contexts** (the UI state a binding applies in — chat input, transcript viewer, permission dialog, fullscreen scroll, and so on) and **actions** (the operations a keystroke can trigger, written as `namespace:action`). This note is the reference catalog of both: it enumerates the bindable contexts and the per-context action sets with their default keystrokes, so you know which `namespace:action` identifiers exist to map keys onto.

This is the *vocabulary* note. The config-file mechanics that consume it — `~/.claude/keybindings.json` schema, keystroke syntax (modifiers/chords/uppercase), unbinding, reserved keys, terminal conflicts, vim interaction, and `/doctor` validation — live in [Keybindings Customization](cc_keybindings_customization.md). Actions follow a `namespace:action` format, such as `chat:submit` to send a message or `app:toggleTodos` to show the task list. Each context has its own specific set of available actions.

## Contexts

Each binding block in the keybindings file specifies a **context** where the bindings apply. The full set of contexts:

| Context | Description |
| :--- | :--- |
| `Global` | Applies everywhere in the app |
| `Chat` | Main chat input area |
| `Autocomplete` | Autocomplete menu is open |
| `Settings` | Settings menu |
| `Confirmation` | Permission and confirmation dialogs |
| `Tabs` | Tab navigation components |
| `Help` | Help menu is visible |
| `Transcript` | Transcript viewer |
| `HistorySearch` | History search mode (Ctrl+R) |
| `Task` | Background task is running |
| `ThemePicker` | Theme picker dialog |
| `Attachments` | Image attachment navigation in select dialogs |
| `Footer` | Footer indicator navigation (tasks, teams, diff) |
| `MessageSelector` | Rewind and summarize dialog message selection |
| `DiffDialog` | Diff viewer navigation |
| `ModelPicker` | Model picker effort level |
| `Select` | Generic select/list components |
| `Plugin` | Plugin dialog (browse, discover, manage) |
| `Scroll` | Conversation scrolling and text selection in fullscreen mode |
| `Doctor` | `/doctor` diagnostics screen |

## Available actions

Actions are grouped by the context (or context family) they apply in. The tables below give each `namespace:action` identifier with its default keystroke. Where a context exposes many near-identical navigation actions, representative rows are shown; the source page is authoritative for the exhaustive list.

### App actions (Global)

| Action | Default | Description |
| :--- | :--- | :--- |
| `app:interrupt` | Ctrl+C | Cancel current operation |
| `app:exit` | Ctrl+D | Exit Claude Code |
| `app:redraw` | (unbound) | Force terminal redraw |
| `app:toggleTodos` | Ctrl+T | Toggle task list visibility |
| `app:toggleTranscript` | Ctrl+O | Toggle verbose transcript |

### History actions

For navigating command history: `history:search` (Ctrl+R) opens history search, `history:previous` (Up) and `history:next` (Down) step through items.

### Chat actions (Chat)

| Action | Default | Description |
| :--- | :--- | :--- |
| `chat:cancel` | Escape | Cancel current input |
| `chat:killAgents` | Ctrl+X Ctrl+K | Stop all running background subagents in this session |
| `chat:cycleMode` | Shift+Tab* | Cycle permission modes |
| `chat:modelPicker` | Meta+P | Open model picker |
| `chat:fastMode` | Meta+O | Toggle fast mode |
| `chat:thinkingToggle` | Meta+T | Toggle extended thinking |
| `chat:submit` | Enter | Submit message |
| `chat:newline` | Ctrl+J | Insert a newline without submitting |
| `chat:externalEditor` | Ctrl+G, Ctrl+X Ctrl+E | Open in external editor |
| `chat:imagePaste` | Ctrl+V (Alt+V on Windows and WSL) | Paste image from clipboard. On WSL, both shortcuts are bound by default |

*On Windows without VT mode (Node <24.2.0/<22.17.0, Bun <1.2.23), `chat:cycleMode` defaults to Meta+M. The Chat context also provides `chat:clearInput` (Ctrl+L), `chat:clearScreen` (Cmd+K), `chat:undo`, and `chat:stash` (Ctrl+S).

### Autocomplete actions

`autocomplete:accept` (Tab), `autocomplete:dismiss` (Escape), `autocomplete:previous` (Up), `autocomplete:next` (Down).

### Confirmation and Permission actions (Confirmation)

The Confirmation context covers permission and confirmation dialogs: `confirm:yes` (Y, Enter), `confirm:no` (N, Escape), navigation (`confirm:previous`/`confirm:next`/`confirm:nextField`), `confirm:toggle` (Space), `confirm:cycleMode` (Shift+Tab, cycle permission modes), and `confirm:toggleExplanation` (Ctrl+E). Permission dialogs add `permission:toggleDebug` (unbound — the previous Ctrl+D default was removed in v2.1.146 because it shadowed `app:exit`).

### Transcript actions (Transcript)

`transcript:toggleShowAll` (Ctrl+E) and `transcript:exit` (q, Ctrl+C, Escape).

### History search actions (HistorySearch)

`historySearch:next` (Ctrl+R), `historySearch:accept` (Escape, Tab), `historySearch:cancel` (Ctrl+C), `historySearch:execute` (Enter), and `historySearch:cycleScope` (Ctrl+S — cycle scope: session, project, everywhere).

### Task actions (Task)

`task:background` (Ctrl+B, Ctrl+X Ctrl+B) backgrounds the current task. The Ctrl+X Ctrl+B chord requires v2.1.169 or later and avoids the tmux prefix conflict.

### Theme, Help, Tabs, Settings, Doctor, Plugin actions

- `theme:toggleSyntaxHighlighting` (Ctrl+T) in ThemePicker.
- `help:dismiss` (Escape) in Help.
- `tabs:next` (Tab, Right) and `tabs:previous` (Shift+Tab, Left) in Tabs.
- `settings:search` (/), `settings:retry` (R), `settings:close` (Enter — Escape discards) in Settings.
- `doctor:fix` (F) in Doctor — sends the diagnostics report to Claude to fix reported issues, only active when issues are found.
- `plugin:toggle` (Space), `plugin:install` (I), `plugin:favorite` (F) in Plugin.

### Attachments, Footer, MessageSelector, ModelPicker, Select, Diff actions

These navigation contexts share directional patterns. Examples: Attachments uses `attachments:next`/`previous`/`remove`/`exit`; Footer uses `footer:next`/`previous`/`up`/`down`/`openSelected`/`clearSelection`; MessageSelector (rewind/summarize) uses `messageSelector:up` (Up, K, Ctrl+P), `messageSelector:down` (Down, J, Ctrl+N), `messageSelector:top`, `messageSelector:bottom`, `messageSelector:select`; ModelPicker uses `modelPicker:decreaseEffort` (Left), `modelPicker:increaseEffort` (Right), `modelPicker:thisSessionOnly` (s); Select uses `select:next`/`previous`/`accept`/`cancel`; DiffDialog uses `diff:dismiss` (Escape), `diff:previousSource`/`nextSource`, `diff:previousFile`/`nextFile`, `diff:viewDetails` (Enter), `diff:back`. The diff detail view also binds pager-style keys to the standard scroll actions.

### Voice actions (Chat, when voice dictation is enabled)

| Action | Default | Description |
| :--- | :--- | :--- |
| `voice:pushToTalk` | Space | Dictate a prompt. Hold or tap depending on `/voice` mode |

This action is available in the Chat context only when [voice dictation](cc_voice_dictation.md) is enabled.

### Scroll actions (Scroll, when fullscreen rendering is enabled)

The Scroll context (active only in fullscreen rendering) provides line/page scrolling and text selection. Scroll examples: `scroll:pageUp` (PageUp), `scroll:pageDown` (PageDown), `scroll:top` (Ctrl+Home), `scroll:bottom` (Ctrl+End), plus `scroll:lineUp`/`scroll:lineDown` (unbound; triggered by mouse wheel) and vi-style `scroll:halfPageUp`/`halfPageDown` and `scroll:fullPageUp`/`fullPageDown`. Text selection: `selection:copy` (Ctrl+Shift+C / Cmd+C), `selection:clear`, and the `selection:extend*` family (`extendLeft` Shift+Left, `extendRight` Shift+Right, `extendUp` Shift+Up, `extendDown` Shift+Down, `extendLineStart` Shift+Home, `extendLineEnd` Shift+End).

**Source**: https://code.claude.com/docs/en/keybindings
**Last Updated**: 2026-06-13
**Status**: Active
