---
tags:
  - resource
  - documentation
  - claude_code
  - terminal
  - themes
keywords:
  - color theme
  - theme command
  - custom theme json
  - claude themes directory
  - color token reference
  - subagent colors
  - ansi color formats
  - theme hot reload
  - ultrathink ultraplan rainbow
topics:
  - Claude Code
  - Terminal Themes
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/terminal-config
access_control_group: ["general"]
---

# Claude Code — Terminal Color Themes

## Overview

Claude Code lets you match its interface colors to your terminal through the `/theme` command, and lets you define **custom themes** as JSON files that override individual color tokens. This note covers the theme-selection and custom-theme procedure from the terminal-config page: picking a built-in or auto theme, creating a custom theme file under `~/.claude/themes/`, the accepted color value formats, hot-reload behavior, and the full color-token reference (text/accent, status, input/mode indicators, diff rendering, fullscreen backgrounds, the usage meter, shimmer variants, the eight subagent colors, and the `ultrathink`/`ultraplan` rainbow gradient).

Theming controls only Claude Code's own interface colors — it does **not** control the terminal's color scheme, which the terminal application sets. The terminal symptom-fixes (Shift+Enter, Option-as-Meta, bell, tmux, paste) are a separate note: [cc_terminal_configuration](cc_terminal_configuration.md).

## Match the Color Theme

Use the `/theme` command, or the theme picker in `/config`, to choose a Claude Code theme that matches your terminal. Selecting the **auto** option detects your terminal's light or dark background, so the theme follows OS appearance changes whenever your terminal does. Claude Code does not control the terminal's own color scheme, which is set by the terminal application.

To customize what appears at the bottom of the interface, configure a [custom status line](https://code.claude.com/docs/en/statusline) that shows the current model, working directory, git branch, or other context.

## Create a Custom Theme

> Custom themes require Claude Code v2.1.118 or later.

In addition to the built-in presets, `/theme` lists any custom themes you have defined and any themes contributed by installed [plugins](https://code.claude.com/docs/en/plugins-reference). Select **New custom theme…** at the end of the list to create one interactively: you name the theme, then pick individual color tokens to override. Press `Ctrl+E` while a custom theme is highlighted to edit it.

Each custom theme is a JSON file in `~/.claude/themes/`. The filename without the `.json` extension is the theme's **slug**, and selecting the theme stores `custom:<slug>` as your theme preference. The file has three optional fields:

- `name` (string) — display label shown in `/theme`; defaults to the filename slug.
- `base` (string) — built-in preset the theme starts from: `dark`, `light`, `dark-daltonized`, `light-daltonized`, `dark-ansi`, or `light-ansi`. Defaults to `dark`.
- `overrides` (object) — map of color token names to color values. Tokens not listed here fall through to the base preset.

Color values accept `#rrggbb`, `#rgb`, `rgb(r,g,b)`, `ansi256(n)`, or `ansi:<name>` where `<name>` is one of the 16 standard ANSI color names such as `red` or `cyanBright`. Unknown tokens and invalid color values are ignored, so a typo cannot break rendering.

The following example keeps the dark preset but recolors the prompt accent, error text, and success text:

```json
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Claude Code watches `~/.claude/themes/` and **reloads when a file changes**, so edits made in your editor apply to a running session without a restart. The interactive editor in `/theme` shows the same tokens with a live preview, plus a few single-purpose accents such as onboarding screen colors that are omitted from the reference below.

## Color Token Reference

The example below combines tokens from several groups — the brand accent, the plan mode border, the diff backgrounds, and the fullscreen message background:

```json
{
  "name": "Midnight",
  "base": "dark",
  "overrides": {
    "claude": "#a78bfa",
    "planMode": "#38bdf8",
    "diffAdded": "#14532d",
    "diffRemoved": "#7f1d1d",
    "userMessageBackground": "#1e1b4b"
  }
}
```

The tokens settable in `overrides` are organized into the following groups:

- **Text and accent colors** — `claude` (primary brand accent, used for the spinner and assistant label), `text` (default foreground text), `inverseText` (text drawn on a colored background, such as status badges), `inactive` (secondary text such as hints, timestamps, disabled items), `subtle` (faint borders and de-emphasized secondary text), `suggestion` (autocomplete suggestions and selection highlight in pickers), `permission` (dialog borders, including permission prompts and pickers), and `remember` (memory and `CLAUDE.md` indicators).
- **Status colors** — `success` (success messages and passing checks), `error` (error messages and failures), `warning` (warnings, caution messages, and the auto mode border), and `merged` (merged pull request status).
- **Input box and mode indicators** — `promptBorder` (input box border in the default permission mode), `planMode` (plan mode accent and border), `autoAccept` (accept-edits mode accent and border), `bashBorder` (input box border when entering a `!` shell command), `ide` (IDE connection indicator), and `fastMode` (fast mode indicator).
- **Diff rendering** — `diffAdded`/`diffRemoved` (backgrounds of added/removed lines), `diffAddedDimmed`/`diffRemovedDimmed` (backgrounds of unchanged context near added/removed lines), and `diffAddedWord`/`diffRemovedWord` (word-level highlights within an added/removed line).
- **Fullscreen mode** — applies only in [fullscreen rendering mode](https://code.claude.com/docs/en/fullscreen), where messages have a background fill: `userMessageBackground`, `userMessageBackgroundHover`, `messageActionsBackground` (selected message when the action bar is open), `bashMessageBackgroundColor` (`!` shell command entries), `memoryBackgroundColor` (`#` memory entries), and `selectionBg` (text selected with the mouse).
- **Usage meter and speaker labels** — `rate_limit_fill`/`rate_limit_empty` (filled/unfilled portions of the `/usage` meter), `briefLabelYou` (color of the `You` label), and `briefLabelClaude` (color of the `Claude` label).

### Shimmer Variants

Several tokens have a paired **shimmer** variant that supplies the lighter color used in the spinner's animated gradient; override the shimmer alongside its base token if the animation looks mismatched. The paired tokens are `claude`/`claudeShimmer`, `warning`/`warningShimmer`, `permission`/`permissionShimmer`, `promptBorder`/`promptBorderShimmer`, `inactive`/`inactiveShimmer`, and `fastMode`/`fastModeShimmer`.

### Subagent Colors

Each [subagent](https://code.claude.com/docs/en/sub-agents) and parallel task is shown in one of **eight named colors** so you can tell them apart in the transcript. The token names follow the pattern `<color>_FOR_SUBAGENTS_ONLY`, where `<color>` is `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, or `cyan`. Override these to change what each named color looks like — for example, a subagent with `color: blue` in its definition is drawn using the `blue_FOR_SUBAGENTS_ONLY` value.

### Ultrathink and Ultraplan Rainbow Tokens

The [`ultrathink`](https://code.claude.com/docs/en/model-config) and [`ultraplan`](https://code.claude.com/docs/en/ultraplan) keywords in the prompt input are rendered with a **seven-color rainbow gradient**. The token names follow the pattern `rainbow_<color>` and `rainbow_<color>_shimmer`, where `<color>` is `red`, `orange`, `yellow`, `green`, `blue`, `indigo`, or `violet`.

**Source**: https://code.claude.com/docs/en/terminal-config
**Last Updated**: 2026-06-13
**Status**: Active
