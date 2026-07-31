---
tags:
  - resource
  - documentation
  - claude_code
  - terminal
  - configuration
keywords:
  - terminal configuration
  - shift+enter multiline
  - terminal-setup
  - option as meta key
  - terminal bell notification
  - tmux passthrough
  - extended keys
  - paste large content
  - fullscreen rendering
topics:
  - Claude Code
  - Terminal Configuration
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/terminal-config
access_control_group: ["general"]
---

# Claude Code — Terminal Configuration

## Overview

Claude Code works in any terminal without configuration; this page is a symptom-driven reference for when a specific terminal behavior is not what you expect. Its scope is getting the **host terminal to send the right signals to Claude Code** — distinct from [keybindings](https://code.claude.com/docs/en/keybindings), which change which keys Claude Code itself responds to. Each section below maps to one symptom: Shift+Enter submitting instead of inserting a newline, Option-key shortcuts doing nothing on macOS, no sound or alert when Claude finishes, running inside tmux, display flicker, and large pastes.

This note covers the terminal-fix procedures. Color theming and custom themes (the `/theme` command and the `~/.claude/themes/<slug>.json` token reference) live in their own section of the same source page — see [Match the color theme](https://code.claude.com/docs/en/terminal-config#match-the-color-theme) — and the full Vim prompt-editing key table is in [cc_input_modes_and_editing](cc_input_modes_and_editing.md).

## Enter Multiline Prompts

Pressing Enter submits your message. To add a line break without submitting, press **Ctrl+J**, or type `\` and then press Enter — both work in every terminal with no setup.

In most terminals you can also press **Shift+Enter**, but support varies by terminal emulator:

| Terminal | Shift+Enter for newline |
| :--- | :--- |
| Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal, Windows Terminal | Works without setup |
| VS Code, Cursor, Devin Desktop, Alacritty, Zed | Run `/terminal-setup` once |
| gnome-terminal, JetBrains IDEs such as PyCharm and Android Studio | Not available; use Ctrl+J or `\` then Enter |

For VS Code, Cursor, Devin Desktop, Alacritty, and Zed, `/terminal-setup` writes Shift+Enter and other keybindings into the terminal's configuration file. Existing bindings are left in place; if you see a message such as `VSCode terminal Shift+Enter key binding already configured`, no change was made. Run `/terminal-setup` **directly in the host terminal** rather than inside tmux or screen, since it needs to write to the host terminal's configuration. In VS Code, Cursor, and Devin Desktop it also updates two editor settings: it sets `terminal.integrated.gpuAcceleration` to `"off"` to prevent garbled text in the integrated terminal, and sets `terminal.integrated.mouseWheelScrollSensitivity` for smoother scrolling in fullscreen mode. To undo the GPU acceleration change, set it back to `"auto"` and reload the editor window.

If you are running inside tmux, Shift+Enter also requires the tmux configuration below even when the outer terminal supports it. To bind newline to a different key, or to swap behavior so Enter inserts a newline and Shift+Enter submits, map the `chat:newline` and `chat:submit` actions in your [keybindings file](https://code.claude.com/docs/en/keybindings).

## Enable Option Key Shortcuts on macOS

Some Claude Code shortcuts use the Option key, such as Option+Enter for a newline or Option+P to switch models. On macOS, most terminals do not send Option as a modifier by default, so these shortcuts do nothing until you enable it. The setting is usually labeled **"Use Option as Meta Key"**; Meta is the historical Unix name for the key now labeled Option or Alt.

- **Apple Terminal** — Open Settings → Profiles → Keyboard and check "Use Option as Meta Key". If you accepted Claude Code's first-run prompt offering "Option+Enter for newlines and visual bell", this is already done: that prompt runs `/terminal-setup`, which enables Option as Meta and switches the audio bell to a visual screen flash in your Apple Terminal profile.
- **iTerm2** — Open Settings → Profiles → Keys → General and set Left Option key and Right Option key to "Esc+". Running `/terminal-setup` in iTerm2 also enables "Applications in terminal may access clipboard" (Settings → General → Selection) so `/copy` can write to the system clipboard; it detects iTerm2 even when run from inside tmux. Restart iTerm2 for the change to take effect.
- **VS Code** — Add `"terminal.integrated.macOptionIsMeta": true` to your VS Code settings.
- **Ghostty, Kitty, and other terminals** — look for an Option-as-Alt or Option-as-Meta setting in the terminal's configuration file.

## Get a Terminal Bell or Notification

When Claude finishes a task or pauses for a permission prompt, it fires a notification event. Surfacing this as a terminal bell or desktop notification lets you switch to other work while a long task runs.

By default Claude Code sends a **desktop notification only in Ghostty, Kitty, and iTerm2**. In other terminals, set [`preferredNotifChannel`](https://code.claude.com/docs/en/settings) to `"terminal_bell"` to ring the terminal bell instead, or configure a Notification hook for a custom sound or command. The desktop notification reaches your local machine over SSH, so a remote session can still alert you. Ghostty and Kitty forward it to your OS notification center without further setup. iTerm2 requires enabling forwarding: go to Settings → Profiles → Terminal, check "Notification Center Alerts", then click "Filter Alerts" and enable "Send escape sequence-generated alerts". If notifications still do not appear, confirm the terminal application has notification permission in your OS settings, and if you are running inside tmux, enable passthrough (see below).

### Play a Sound with a Notification Hook

In any terminal you can configure a [Notification hook](https://code.claude.com/docs/en/hooks-guide) to play a sound or run a custom command when Claude needs your attention. Hooks run alongside the built-in notification rather than replacing it, so terminals that do not receive a desktop notification, such as Warp or the VS Code integrated terminal, can use a hook or set `preferredNotifChannel` to `"terminal_bell"` instead. The example below plays a system sound on macOS (the linked hooks guide has desktop-notification commands for macOS, Linux, and Windows):

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{ "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff" }]
      }
    ]
  }
}
```

## Configure tmux

When Claude Code runs inside tmux, two things break by default: Shift+Enter submits instead of inserting a newline, and desktop notifications and the progress bar never reach the outer terminal. Add these lines to `~/.tmux.conf`, then run `tmux source-file ~/.tmux.conf` to apply them to the running server:

```bash
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

The `allow-passthrough` line lets notifications and progress updates reach the outer terminal instead of being swallowed by tmux. The `extended-keys` lines let tmux distinguish Shift+Enter from plain Enter so the newline shortcut works.

## Switch to Fullscreen Rendering

If the display flickers or the scroll position jumps while Claude is working, switch to [fullscreen rendering mode](https://code.claude.com/docs/en/fullscreen). It draws to a separate screen the terminal reserves for full-screen apps instead of appending to your normal scrollback, which keeps memory usage flat and adds mouse support for scrolling and selection. In this mode you scroll with the mouse or PageUp inside Claude Code rather than with your terminal's native scrollback.

Run `/tui fullscreen` to switch in the current session with your conversation intact. To make it the default, set the `CLAUDE_CODE_NO_FLICKER` environment variable before starting Claude Code:

```bash
CLAUDE_CODE_NO_FLICKER=1 claude
```

The same variable can be set in PowerShell (`$env:CLAUDE_CODE_NO_FLICKER = "1"; claude`) or persisted under the `env` key in `~/.claude/settings.json`. Full details on scrolling, search, and copy in fullscreen mode live in the dedicated [fullscreen rendering page](https://code.claude.com/docs/en/fullscreen).

## Paste Large Content

When you paste more than 10,000 characters into the prompt, Claude Code collapses the input to a `[Pasted text]` placeholder so the input box stays usable. The full content is still sent to Claude when you submit. The VS Code integrated terminal can drop characters from very large pastes before they reach Claude Code, so prefer file-based workflows there: for very large inputs such as entire files or long logs, write the content to a file and ask Claude to read it instead of pasting. This keeps the conversation transcript readable and lets Claude reference the file by path in later turns.

**Source**: https://code.claude.com/docs/en/terminal-config
**Last Updated**: 2026-06-13
**Status**: Active
