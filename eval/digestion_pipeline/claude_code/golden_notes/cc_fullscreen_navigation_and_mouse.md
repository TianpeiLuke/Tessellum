---
tags:
  - resource
  - documentation
  - claude_code
  - fullscreen
  - navigation
keywords:
  - fullscreen mouse support
  - scroll the conversation
  - auto-follow
  - transcript mode
  - claude_code_scroll_speed
  - claude_code_disable_mouse
  - keep native text selection
  - clear the conversation
topics:
  - Claude Code
  - Fullscreen
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/fullscreen
access_control_group: ["general"]
---

# Claude Code — Fullscreen Navigation and Mouse

## Overview

When fullscreen rendering is active (see [Fullscreen Rendering](cc_fullscreen_rendering.md)), the conversation lives in the terminal's alternate screen buffer instead of the native scrollback, so Claude Code handles mouse, scrolling, search, and clearing inside the app rather than deferring to the terminal. This note is the interaction reference: how to use the mouse, scroll and control auto-follow, enter transcript mode to search or hand the conversation back to your terminal, clear the conversation, and opt out of mouse capture to keep native text selection while keeping the flicker-free rendering.

## Use the mouse

Fullscreen rendering captures mouse events and handles them inside Claude Code:

- **Click in the prompt input** to position your cursor anywhere in the text you're typing.
- **Click a suggestion** in the `/` command or `@` file list to accept it. Hovering highlights the row under your cursor.
- **Click a collapsed tool result** to expand it and see the full output. Click again to collapse. The tool call and its result expand together. Only messages that have more to show are clickable.
- **Click a URL or file path** to open it. File paths in tool output (like those printed after an Edit or Write) open in your default application; plain `http://` and `https://` URLs open in your browser. In most terminals this replaces native `Cmd`-click or `Ctrl`-click, which mouse capture intercepts. In the VS Code integrated terminal and similar xterm.js-based terminals, keep using `Cmd`-click — Claude Code defers to the terminal's own link handler there to avoid opening links twice.
- **Click and drag** to select text anywhere in the conversation. Double-click selects a word (matching iTerm2's word boundaries, so a file path selects as one unit); triple-click selects the line.
- **Scroll with the mouse wheel** to move through the conversation.

Selected text copies to your clipboard automatically on mouse release. To turn this off, toggle **Copy on select** in `/config`; with it off, press `Ctrl+Shift+c` to copy manually. On terminals that support the kitty keyboard protocol (kitty, WezTerm, Ghostty, iTerm2), `Cmd+c` also works. If a selection is active, `Ctrl+c` copies instead of cancelling. With a selection active, hold `Shift` and press the arrow keys to extend it from the keyboard: `Shift+↑`/`Shift+↓` scroll the viewport when the selection reaches the top or bottom edge, and `Shift+Home`/`Shift+End` extend to the start or end of the current line.

## Scroll the conversation

Fullscreen rendering handles scrolling inside the app. Use these shortcuts to navigate:

| Shortcut        | Action                                               |
| :-------------- | :--------------------------------------------------- |
| `PgUp` / `PgDn` | Scroll up or down by half a screen                   |
| `Ctrl+Home`     | Jump to the start of the conversation                |
| `Ctrl+End`      | Jump to the latest message and re-enable auto-follow |
| Mouse wheel     | Scroll a few lines at a time                         |

On keyboards without dedicated `PgUp`, `PgDn`, `Home`, or `End` keys (like MacBook keyboards), hold `Fn` with the arrow keys: `Fn+↑` sends `PgUp`, `Fn+↓` sends `PgDn`, `Fn+←` sends `Home`, and `Fn+→` sends `End`, making `Ctrl+Fn+→` the jump-to-bottom shortcut. If that feels awkward, scroll to the bottom with the mouse wheel to resume following, or rebind `scroll:bottom`. These actions are rebindable — see the [Scroll actions](https://code.claude.com/docs/en/keybindings) keybindings reference for the full list of action names, including half-page and full-page variants that have no default binding.

### Auto-follow

Scrolling up pauses auto-follow so new output does not pull you back to the bottom. Press `Ctrl+End` or scroll to the bottom to resume following. To turn auto-follow off entirely so the view stays where you leave it, open `/config` and set **Auto-scroll** to off; the view then never jumps to the bottom on its own. Permission prompts and other dialogs that need a response still scroll into view regardless of this setting.

### Mouse wheel scrolling

Mouse wheel scrolling requires your terminal to forward mouse events to Claude Code. Most terminals do this whenever an application requests it. iTerm2 makes it a per-profile setting: if the wheel does nothing but `PgUp` and `PgDn` work, open Settings → Profiles → Terminal and turn on **Enable mouse reporting** (the same setting is also required for click-to-expand and text selection).

If wheel scrolling feels slow, your terminal may be sending one scroll event per physical notch with no multiplier. Some terminals (Ghostty, iTerm2 with faster scrolling enabled) already amplify wheel events; others — including the VS Code integrated terminal — send exactly one event per notch, and Claude Code cannot detect which. Set `CLAUDE_CODE_SCROLL_SPEED` to multiply the base scroll distance:

```bash
export CLAUDE_CODE_SCROLL_SPEED=3
```

A value of `3` matches the default in `vim` and similar applications. The setting accepts values from 1 to 20, plus fractional values below 1 (such as `0.5`) to slow accelerated trackpad and wheel scrolling. To adjust interactively, run `/scroll-speed`: the dialog shows a ruler you can scroll while open, press `←`/`→` to adjust, `r` to reset to the auto-detected default, and `Enter` to save. It writes the same value the env var sets, persisted to `~/.claude/settings.json`, and is not available in the JetBrains IDE terminal. Separately from base speed, Claude Code accelerates the scroll rate when you spin the wheel quickly. To turn acceleration off and keep a constant rate per notch, set `wheelScrollAccelerationEnabled` to `false` in `settings.json` (requires Claude Code v2.1.174 or later).

### Scroll in the JetBrains IDE terminal

In the JetBrains IDE terminal, Claude Code applies its own scroll handling and ignores `CLAUDE_CODE_SCROLL_SPEED`, because the terminal sends scroll events at a much higher rate than other emulators, so a multiplier tuned elsewhere overshoots. In 2025.2 the terminal also has scroll-wheel bugs that produce spurious arrow keys and wrong-direction events; Claude Code detects these at runtime and mitigates them automatically, so trackpad and mouse wheel scrolling work without configuration (a hint shows the first time you scroll if the bug is detected). For the best scroll experience, upgrade to 2025.3 or later.

## Search and review the conversation

`Ctrl+o` toggles between the normal prompt and **transcript mode**. For a quieter view that shows only your last prompt, a one-line summary of tool calls with edit diffstats, and the final response, run `/focus` (the setting persists across sessions; run `/focus` again to turn it off). Transcript mode gains `less`-style navigation and search:

| Key                                  | Action                                                                                                 |
| :----------------------------------- | :----------------------------------------------------------------------------------------------------- |
| `/`                                  | Open search. Type to find matches, `Enter` to accept, `Esc` to cancel and restore your scroll position |
| `n` / `N`                            | Jump to next or previous match. Works after you've closed the search bar                               |
| `j` / `k` or `↑` / `↓`               | Scroll one line                                                                                        |
| `g` / `G` or `Home` / `End`          | Jump to top or bottom                                                                                  |
| `Ctrl+u` / `Ctrl+d`                  | Scroll half a page                                                                                     |
| `Ctrl+b` / `Ctrl+f` or `Space` / `b` | Scroll a full page                                                                                     |
| `Ctrl+o`, `Esc`, or `q`              | Exit transcript mode and return to the prompt                                                          |

Your terminal's `Cmd+f` and tmux search don't see the conversation because it lives in the alternate screen buffer, not the native scrollback. To hand the content back to your terminal, press `Ctrl+o` to enter transcript mode first, then:

- **`[`** writes the full conversation into your terminal's native scrollback buffer, with all tool output expanded. The conversation is now ordinary text in your terminal, so `Cmd+f`, tmux copy mode, and any other native tool can search or select it. Long sessions may pause for a moment while this happens. This lasts until you exit transcript mode with `Esc` or `q` (which returns you to fullscreen rendering); the next `Ctrl+o` starts fresh.
- **`v`** writes the conversation to a temporary file and opens it in `$VISUAL` or `$EDITOR`.

Press `Esc` or `q` to return to the prompt.

## Clear the conversation

Press `Ctrl+L` twice within two seconds to run `/clear` and start a new conversation. The first press redraws the screen and shows a hint; the second press clears the conversation. On macOS, double-pressing `Cmd+K` also runs `/clear`.

## Keep native text selection

Mouse capture is the most common friction point, especially over SSH or inside tmux. When Claude Code captures mouse events, your terminal's native copy-on-select stops working: the selection you make with click-and-drag exists inside Claude Code, not your terminal's selection buffer, so tmux copy mode, Kitty hints, and similar tools don't see it.

Claude Code writes the selection to your system clipboard, and the path depends on your setup. On a local session it runs a native clipboard tool: **macOS** uses `pbcopy`; **Linux** uses `wl-copy` on Wayland, or `xclip`/`xsel` on X11 (whichever is installed — it writes both the clipboard and the PRIMARY selection so middle-click paste works); **Windows and WSL** use PowerShell `Set-Clipboard`. Inside tmux it also writes to the tmux paste buffer; over SSH it falls back to OSC 52 escape sequences. A toast after each copy tells you which path was used. Some terminals block OSC 52 by default — iTerm2 blocks it until you enable Settings → General → Selection → "Applications in terminal may access clipboard"; running `/terminal-setup` in iTerm2 enables this for you (see [terminal configuration](https://code.claude.com/docs/en/terminal-config)).

For a **one-off native selection**, the key to hold depends on your terminal: **Terminal.app** → `Fn`; **iTerm2** → `Option`; **VS Code, Cursor, and Devin Desktop** → `Shift` (or `Option` on macOS with `terminal.integrated.macOptionClickForcesSelection` enabled); **most other terminals** → `Shift`. Hold that key while you click and drag — your terminal handles the selection itself instead of passing it to Claude Code, so copy shortcuts like `Cmd+C` work on what you select. Claude Code shows the correct key in its on-screen hint; over SSH or inside tmux it can't always detect the connecting terminal, so the hint lists the candidate keys instead.

If you rely on native selection all the time, set `CLAUDE_CODE_DISABLE_MOUSE=1` to opt out of mouse capture while keeping the flicker-free rendering and flat memory:

```bash
CLAUDE_CODE_NO_FLICKER=1 CLAUDE_CODE_DISABLE_MOUSE=1 claude
```

With mouse capture disabled, keyboard scrolling with `PgUp`, `PgDn`, `Ctrl+Home`, and `Ctrl+End` still works, and your terminal handles selection natively. You lose click-to-position-cursor, click-to-expand tool output, URL clicking, and wheel scrolling inside Claude Code.

**Source**: https://code.claude.com/docs/en/fullscreen
**Last Updated**: 2026-06-13
**Status**: Active
