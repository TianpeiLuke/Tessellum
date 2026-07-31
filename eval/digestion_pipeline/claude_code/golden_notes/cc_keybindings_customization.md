---
tags:
  - resource
  - documentation
  - claude_code
  - keybindings
  - customization
keywords:
  - keybindings customization
  - keybindings.json
  - keystroke syntax
  - chords and modifiers
  - unbind shortcut
  - reserved shortcuts
  - terminal multiplexer conflicts
  - vim mode interaction
  - keybinding validation
topics:
  - Claude Code
  - Keybindings
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/keybindings
access_control_group: ["general"]
---

# Customize Keyboard Shortcuts

## Overview

Claude Code supports customizable keyboard shortcuts through a `keybindings.json` configuration file (requires v2.1.18 or later; check with `claude --version`). Run `/keybindings` to create or open the file at `~/.claude/keybindings.json`. This note covers the *procedure* of customizing bindings — the config-file schema, keystroke syntax (modifiers, uppercase, chords, special keys), how to unbind defaults, which shortcuts are reserved, terminal-multiplexer conflicts, how keybindings interact with vim mode, and validation. The complete catalog of bindable contexts and `namespace:action` identifiers this file maps keys onto lives in the sibling reference note [cc_keybindings_action_reference](cc_keybindings_action_reference.md).

## Configuration file

The keybindings configuration file is an object with a `bindings` array. Each block specifies a context and a map of keystrokes to actions. Changes to the file are automatically detected and applied without restarting Claude Code.

| Field      | Description                                        |
| :--------- | :------------------------------------------------- |
| `$schema`  | Optional JSON Schema URL for editor autocompletion |
| `$docs`    | Optional documentation URL                         |
| `bindings` | Array of binding blocks by context                 |

This example binds `Ctrl+E` to open an external editor in the chat context, and unbinds `Ctrl+U`:

```json theme={null}
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

Each binding block names a **context** (e.g. `Global`, `Chat`, `Transcript`) where the bindings apply, and maps keystroke strings to `namespace:action` identifiers (e.g. `chat:submit`, `app:toggleTodos`). The full list of contexts and the actions available in each is in [cc_keybindings_action_reference](cc_keybindings_action_reference.md).

## Keystroke syntax

### Modifiers

Use modifier keys with the `+` separator:

* `ctrl` or `control` — Control key
* `shift` — Shift key
* `alt`, `opt`, `option`, or `meta` — Alt key on Windows and Linux, Option key on macOS
* `cmd`, `command`, `super`, or `win` — Command key on macOS, Windows key on Windows, Super key on Linux

The `cmd` group is only detected in terminals that report the Super modifier, such as those supporting the Kitty keyboard protocol or xterm's `modifyOtherKeys` mode. Most terminals do not send it, so use `ctrl` or `meta` for bindings you want to work everywhere. For example, `ctrl+k` is Ctrl + K, `shift+tab` is Shift + Tab, `meta+p` is Option + P on macOS / Alt + P elsewhere, and `ctrl+shift+c` combines multiple modifiers.

### Uppercase letters

A standalone uppercase letter implies Shift — `K` is equivalent to `shift+k`. This is useful for vim-style bindings where uppercase and lowercase keys have different meanings. Uppercase letters *with* modifiers (e.g. `ctrl+K`) are treated as stylistic and do **not** imply Shift: `ctrl+K` is the same as `ctrl+k`.

### Chords

Chords are sequences of keystrokes separated by spaces. For example, `ctrl+k ctrl+s` means press Ctrl+K, release, then Ctrl+S.

### Special keys

* `escape` or `esc` — Escape key
* `enter` or `return` — Enter key
* `tab` — Tab key
* `space` — Space bar
* `up`, `down`, `left`, `right` — Arrow keys
* `backspace`, `delete` — Delete keys

## Unbind default shortcuts

Set an action to `null` to unbind a default shortcut:

```json theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+s": null
      }
    }
  ]
}
```

This also works for chord bindings. Unbinding every chord that shares a prefix frees that prefix for use as a single-key binding:

```json theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+x ctrl+k": null,
        "ctrl+x ctrl+e": null,
        "ctrl+x": "chat:newline"
      }
    }
  ]
}
```

If you unbind some but not all chords on a prefix, pressing the prefix still enters chord-wait mode for the remaining bindings.

## Reserved shortcuts

These shortcuts cannot be rebound:

| Shortcut  | Reason                                         |
| :-------- | :--------------------------------------------- |
| Ctrl+C    | Hardcoded interrupt/cancel                     |
| Ctrl+D    | Hardcoded exit                                 |
| Ctrl+M    | Identical to Enter in terminals (both send CR) |
| Caps Lock | Not delivered to terminal applications         |

## Terminal conflicts

Some shortcuts may conflict with terminal multiplexers:

| Shortcut | Conflict                          |
| :------- | :-------------------------------- |
| Ctrl+B   | tmux prefix (press twice to send) |
| Ctrl+A   | GNU screen prefix                 |
| Ctrl+Z   | Unix process suspend (SIGTSTP)    |

## Vim mode interaction

When vim mode is enabled via `/config` → Editor mode, keybindings and vim mode operate independently:

* **Vim mode** handles input at the text input level (cursor movement, modes, motions).
* **Keybindings** handle actions at the component level (toggle todos, submit, etc.).
* The Escape key in vim mode switches INSERT to NORMAL mode; it does not trigger `chat:cancel`.
* Most Ctrl+key shortcuts pass through vim mode to the keybinding system.
* In vim NORMAL mode, `?` shows the help menu (vim behavior).
* In vim NORMAL mode, `/` opens history search, the same as Ctrl+R in standard mode.

The vim motion/text-object key table itself is documented in [cc_input_modes_and_editing](cc_input_modes_and_editing.md).

## Validation

Claude Code validates your keybindings and shows warnings for:

* Parse errors (invalid JSON or structure)
* Invalid context names
* Reserved shortcut conflicts
* Terminal multiplexer conflicts
* Duplicate bindings in the same context

Run `/doctor` to see any keybinding warnings.

**Source**: https://code.claude.com/docs/en/keybindings
**Last Updated**: 2026-06-13
**Status**: Active
