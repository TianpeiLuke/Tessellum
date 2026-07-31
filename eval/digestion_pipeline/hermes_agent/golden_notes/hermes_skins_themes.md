---
tags:
  - resource
  - documentation
  - hermes_agent
  - customization
  - cli
keywords:
  - skins and themes
  - skin command
  - display.skin config
  - built-in skins
  - configurable keys
  - custom skin yaml
  - hermes mod
topics:
  - Hermes Agent
  - Customization
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/skins
access_control_group: ["general"]
---

# Hermes Agent — Skins & Themes

## Overview

A **skin** is the CLI's visual-presentation layer in Hermes Agent: it controls banner colors, spinner faces and verbs, response-box labels, branding text strings, and the tool-activity prefix. Skins are deliberately separate from **personality** — personality changes the agent's *tone and wording* (a conversational concern), whereas a skin changes only the CLI's *appearance*. This note is the procedure for applying a skin (`/skin` for the session vs `display.skin` in `config.yaml` for the permanent default), the catalog of nine built-in skins, the complete surface of configurable keys (colors, spinner, branding, and top-level keys), how to author a custom skin as a YAML file under `~/.hermes/skins/` that inherits from `default`, the community **Hermes Mod** visual editor, and the precedence/fallback rules. The `config.yaml` TUI status-bar config the colors feed into is owned elsewhere (link-out); this note documents the skin surface itself.

## Change skins

Apply a skin for the current session with the `/skin` slash command, or set a permanent default in config.

```bash
/skin                # show the current skin and list available skins
/skin ares           # switch to a built-in skin
/skin mytheme        # switch to a custom skin from ~/.hermes/skins/mytheme.yaml
```

To make a skin the permanent default, set it in `~/.hermes/config.yaml`:

```yaml
display:
  skin: default
```

`/skin` changes are session-only and take effect immediately for the current session; the `display.skin` config key sets the permanent default (precedence summarized in Operational notes below).

## Built-in skins

Nine skins ship with Hermes. Each defines an `agent_name` branding string and a visual character; several override the spinner verbs and banner ASCII art:

| Skin | Description | Agent branding |
|------|-------------|----------------|
| `default` | Classic Hermes — gold and kawaii; warm gold borders, cornsilk text, kawaii spinner faces, caduceus banner | `Hermes Agent` |
| `ares` | War-god theme — deep crimson + bronze; aggressive spinner verbs ("forging", "marching", "tempering steel"); sword-and-shield ASCII banner | `Ares Agent` |
| `mono` | Monochrome — all grays, no color (borders `#555555`, text `#c9d1d9`); for minimal terminals / screen recordings | `Hermes Agent` |
| `slate` | Cool blue, developer-focused — royal blue borders (`#4169e1`), soft blue text; uses default spinner faces | `Hermes Agent` |
| `daylight` | Light theme for bright terminals — dark slate text, blue borders, pale status surfaces, light completion menu | `Hermes Agent` |
| `warm-lightmode` | Warm brown/gold text for light backgrounds — dark brown text, saddle-brown accents, cream status surfaces | `Hermes Agent` |
| `poseidon` | Ocean-god theme — deep blue to seafoam; ocean spinners ("charting currents", "sounding the depth"); trident banner | `Poseidon Agent` |
| `sisyphus` | Austere grayscale with persistence — light grays, stark contrast; boulder spinners ("pushing uphill", "resetting the boulder", "enduring the loop"); boulder-and-hill banner | `Sisyphus Agent` |
| `charizard` | Volcanic theme — burnt orange to ember; fire spinners ("banking into the draft", "measuring burn"); dragon-silhouette banner | `Charizard Agent` |

## Complete list of configurable keys

A skin is a set of keys across four groups. Values not specified inherit from `default`.

**Colors (`colors:`)** — hex strings controlling every color in the CLI. The full set (with `default`-skin values): `banner_border` (`#CD7F32` bronze), `banner_title` (`#FFD700` gold), `banner_accent` (`#FFBF00` amber — section headers), `banner_dim` (`#B8860B` — separators/secondary labels), `banner_text` (`#FFF8DC` cornsilk — body text), `ui_accent` (`#FFBF00` — highlights/active elements), `ui_label` (`#4dd0e1` teal), `ui_ok` (`#4caf50` green — success), `ui_error` (`#ef5350` red), `ui_warn` (`#ffa726` orange — caution/approval prompts), `prompt` (`#FFF8DC`), `input_rule` (`#CD7F32` — rule above the input area), `response_border` (`#FFD700` — agent response box, ANSI escape), `session_label` (`#DAA520`), `session_border` (`#8B8682`), `status_bar_bg` (`#1a1a2e` — TUI status/usage bar), `voice_status_bg` (`#1a1a2e` — voice-mode status badge), `selection_bg` (`#333355` — mouse-selection highlighter; falls back to `completion_menu_current_bg` when unset), `completion_menu_bg` (`#1a1a2e`), `completion_menu_current_bg` (`#333355` — active row), `completion_menu_meta_bg` (`#1a1a2e`), and `completion_menu_meta_current_bg` (`#333355` — active meta column).

**Spinner (`spinner:`)** — the animation shown while waiting for API responses: `waiting_faces` (list of faces cycled while waiting, e.g. `["(⚔)", "(⛨)", "(▲)"]`), `thinking_faces` (faces cycled during model reasoning), `thinking_verbs` (verbs in spinner messages, e.g. `["forging", "plotting", "hammering plans"]`), and `wings` (list of `[left, right]` bracket pairs around the spinner). When spinner values are empty (as in `default` and `mono`), hardcoded defaults from `display.py` are used.

**Branding (`branding:`)** — text strings: `agent_name` (`Hermes Agent` — banner title + status display), `welcome` (CLI-startup message), `goodbye` (exit message, `Goodbye! ⚕`), `response_label` (response-box header label, ` ⚕ Hermes `), `prompt_symbol` (`❯` — bare token before the user prompt; renderers add a trailing space), and `help_header` (`(^_^)? Available Commands`).

**Other top-level keys** — `tool_prefix` (string, `┊` — prefixed to tool-output lines), `tool_emojis` (dict `{tool_name: emoji}` — per-tool emoji overrides for spinners/progress, default `{}`), `banner_logo` (Rich-markup ASCII art logo replacing the default `HERMES_AGENT` banner), and `banner_hero` (Rich-markup hero art replacing the default caduceus art).

## Custom skins

Create a YAML file under `~/.hermes/skins/`. User skins inherit any missing values from the built-in `default` skin, so you only specify keys you want to change. The full template shows every key (delete any you don't need):

```yaml
# ~/.hermes/skins/mytheme.yaml
name: mytheme
description: My custom theme

colors:
  banner_border: "#CD7F32"
  banner_title: "#FFD700"
  banner_accent: "#FFBF00"
  ui_accent: "#FFBF00"
  ui_ok: "#4caf50"
  ui_error: "#ef5350"
  status_bar_bg: "#1a1a2e"
  voice_status_bg: "#1a1a2e"
  completion_menu_bg: "#1a1a2e"
  completion_menu_current_bg: "#333355"

spinner:
  waiting_faces: ["(⚔)", "(⛨)", "(▲)"]
  thinking_verbs: ["processing", "analyzing", "computing", "evaluating"]
  wings:
    - ["⟪⚡", "⚡⟫"]

branding:
  agent_name: "My Agent"
  welcome: "Welcome to My Agent! Type your message or /help for commands."
  goodbye: "See you later! ⚡"
  response_label: " ⚡ My Agent "
  prompt_symbol: "⚡"
  help_header: "(⚡) Available Commands"

tool_prefix: "┊"

tool_emojis:
  terminal: "⚔"
  web_search: "🔮"
  read_file: "📄"

# banner_logo / banner_hero: Rich-markup ASCII art (optional)
```

Because everything inherits from `default`, a minimal skin only needs to change what is different:

```yaml
name: cyberpunk
description: Neon terminal theme

colors:
  banner_border: "#FF00FF"
  banner_title: "#00FFFF"
  banner_accent: "#FF1493"

spinner:
  thinking_verbs: ["jacking in", "decrypting", "uploading"]
  wings:
    - ["⟨⚡", "⚡⟩"]

branding:
  agent_name: "Cyber Agent"
  response_label: " ⚡ Cyber "

tool_prefix: "▏"
```

## Hermes Mod — visual skin editor

[Hermes Mod](https://github.com/cocktailpeanut/hermes-mod) is a community-built web UI for creating and managing skins visually — a point-and-click editor with live preview instead of hand-writing YAML. It lists all built-in and custom skins, opens any skin into a visual editor exposing every Hermes skin field (colors, spinner, branding, tool prefix, tool emojis), generates `banner_logo` text art from a text prompt, converts uploaded images (PNG/JPG/GIF/WEBP) into `banner_hero` ASCII art with multiple render styles (braille, ASCII ramp, blocks, dots), saves directly to `~/.hermes/skins/`, activates a skin by updating `~/.hermes/config.yaml`, and shows the generated YAML plus a live preview.

Install via Pinokio (1-click from [pinokio.computer](https://pinokio.computer)), `npx -y hermes-mod` (quickest from terminal), or a manual `git clone` + `npm install` + `npm start`. Usage: start the app, open **Skin Studio**, choose a built-in/custom skin to edit, generate a logo and/or upload hero art (pick a render style + width), edit colors/spinner/branding, **Save** to write the YAML, then **Activate** to set it current (updates `display.skin` in `config.yaml`). Hermes Mod respects the `HERMES_HOME` environment variable, so it works with profiles too.

## Operational notes

- Built-in skins load from `hermes_cli/skin_engine.py`.
- Unknown skins automatically fall back to `default`.
- `/skin` updates the active CLI theme immediately for the current session.
- User skins in `~/.hermes/skins/` take precedence over built-in skins with the same name.
- Skin changes via `/skin` are session-only; to make a skin your permanent default, set it in `config.yaml`.
- The `banner_logo` and `banner_hero` fields support Rich console markup (e.g. `[bold #FF0000]text[/]`) for colored ASCII art.

**Source**: `inbox/hermes_agent_docs/user-guide/features/skins.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/skins
**Last Updated**: 2026-06-19
**Status**: Active
