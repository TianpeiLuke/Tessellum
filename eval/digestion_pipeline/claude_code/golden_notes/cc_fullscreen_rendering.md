---
tags:
  - resource
  - documentation
  - claude_code
  - fullscreen
  - rendering
keywords:
  - fullscreen rendering
  - alternate screen buffer
  - flicker-free
  - tui setting
  - claude_code_no_flicker
  - flat memory long conversations
  - tmux compatibility
  - research preview
topics:
  - Claude Code
  - Fullscreen Rendering
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/fullscreen
access_control_group: ["general"]
---

# Claude Code — Fullscreen Rendering

## Overview

**Fullscreen rendering** is an alternative rendering path for the Claude Code CLI that eliminates flicker, keeps memory usage flat in long conversations, and adds mouse support. It draws the interface on the terminal's **alternate screen buffer** — the way `vim` or `htop` do — and only renders messages that are currently visible, which reduces the amount of data sent to the terminal on each update. The term *fullscreen* describes how Claude Code takes over the terminal's drawing surface; it has nothing to do with maximizing the terminal window and works at any window size.

It is an opt-in **research preview** and requires Claude Code v2.1.89 or later. The difference is most noticeable in terminal emulators where rendering throughput is the bottleneck, such as the VS Code integrated terminal, tmux, and iTerm2. If the terminal scroll position jumps to the top while Claude is working, or the screen flashes as tool output streams in, this mode addresses those problems. This note covers the rendering model, how to enable it, what changes, tmux caveats, and its research-preview status; the in-app mouse, scroll, search, and clear interactions are documented in the sibling [Fullscreen Navigation and Mouse](cc_fullscreen_navigation_and_mouse.md) note.

## Enable fullscreen rendering

Run `/tui fullscreen` inside any Claude Code conversation. The CLI saves the [`tui` setting](https://code.claude.com/docs/en/settings) and relaunches into fullscreen with the conversation intact, so the renderer can be switched mid-session without losing context. Run `/tui` with no argument to print which renderer is active.

The `CLAUDE_CODE_NO_FLICKER` environment variable can also be set before starting Claude Code (used on versions before v2.1.110):

```bash
CLAUDE_CODE_NO_FLICKER=1 claude
```

The `tui` setting and the environment variable are equivalent. The `/tui` command clears `CLAUDE_CODE_NO_FLICKER` from the relaunched process so the setting it writes takes effect.

## What changes

Fullscreen rendering changes how the CLI draws to the terminal. The input box stays fixed at the bottom of the screen instead of moving as output streams in — if the input stays put while Claude is working, fullscreen rendering is active. Only visible messages are kept in the render tree, so **memory stays constant regardless of conversation length**.

Because the conversation lives in the alternate screen buffer instead of the terminal's scrollback, a few things work differently:

| Before | Now | Details |
| :--- | :--- | :--- |
| `Cmd+f` or tmux search to find text | `Ctrl+o` for transcript mode, then `/` to search or `[` to write to scrollback | Search and review the conversation |
| Terminal's native click-and-drag to select and copy | In-app selection, copies automatically on mouse release | Use the mouse |
| `Cmd`-click to open a URL | Click the URL | Use the mouse |

If mouse capture interferes with a workflow, it can be turned off while keeping the flicker-free rendering. The detailed mouse, scroll, transcript-search, and clear behaviors referenced in this table are in [Fullscreen Navigation and Mouse](cc_fullscreen_navigation_and_mouse.md).

## Use with tmux

Fullscreen rendering works inside tmux, with three caveats.

**Mouse wheel scrolling requires tmux's mouse mode.** If `~/.tmux.conf` does not already enable it, add this line and reload the config:

```bash
set -g mouse on
```

Without mouse mode, wheel events go to tmux instead of Claude Code. Keyboard scrolling with `PgUp` and `PgDn` works either way. Claude Code prints a one-time hint at startup if it detects tmux with mouse mode off.

**Fullscreen rendering is incompatible with iTerm2's tmux integration mode** — the mode entered with `tmux -CC`. In integration mode, iTerm2 renders each tmux pane as a native split rather than letting tmux draw to the terminal; the alternate screen buffer and mouse tracking do not work correctly there (the mouse wheel does nothing, and double-click can corrupt the terminal state). Do not enable fullscreen rendering in `tmux -CC` sessions. Regular tmux inside iTerm2, without `-CC`, works fine.

**tmux does not support synchronized output**, so there may be more flicker during redraws than when running Claude Code directly in the terminal. If the flicker is noticeable, especially over SSH, run Claude Code in its own terminal tab outside tmux.

## Research preview

Fullscreen rendering is a research preview feature, and behavior may change based on feedback. It has been tested on common terminal emulators, but rendering issues may appear on less common terminals or unusual configurations. To report a problem, run `/feedback` inside Claude Code, or open an issue on the [claude-code GitHub repo](https://github.com/anthropics/claude-code/issues), including the terminal emulator name and version.

To turn fullscreen rendering off, run `/tui default`, or unset `CLAUDE_CODE_NO_FLICKER` if it was enabled that way. To force the classic renderer regardless of the saved `tui` setting, set `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1`. The classic renderer keeps the conversation in the terminal's native scrollback so `Cmd+f` and tmux copy mode work as usual.

Background sessions opened from [agent view](https://code.claude.com/docs/en/agent-view) or `claude attach` **always use fullscreen rendering**. The attaching terminal enters the alternate screen buffer to show the session, and the classic renderer has no scrollback or mouse handling there, so the `tui` setting and `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN` do not apply to them.

**Source**: https://code.claude.com/docs/en/fullscreen
**Last Updated**: 2026-06-13
**Status**: Active
