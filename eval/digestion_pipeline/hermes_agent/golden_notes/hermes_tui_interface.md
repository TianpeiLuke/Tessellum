---
tags:
  - resource
  - documentation
  - hermes_agent
  - tui
  - user_interface
keywords:
  - hermes tui
  - terminal ui
  - live session switcher
  - collapsible banner
  - in-process gateway
  - alternate-screen rendering
topics:
  - Hermes Agent
  - TUI
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/tui
access_control_group: ["general"]
---

# Hermes Agent — TUI Interface

## Overview

The TUI is Hermes' modern terminal front-end — a mouse-friendly, overlay-rich surface backed by the **same Python runtime, sessions, and slash commands** as the [Classic CLI](hermes_cli_interface.md). It is the recommended way to run Hermes interactively: it paints a banner instantly, accepts non-blocking input before the agent is ready, renders pickers/approvals as modal overlays, and uses alternate-screen differential rendering so streaming never flickers. The classic CLI remains the shipped default; the TUI is opt-in via `--tui`, the `HERMES_TUI=1` env var, or a persistent `display.interface: tui` config key.

## Launch

Launch and resume flags mirror the CLI; the TUI runs as a Node subprocess of the Python CLI:

```bash
hermes --tui                                   # launch the TUI
hermes --tui -c                                # resume latest TUI session (falls back to latest classic)
hermes --tui -r 20260409_000000_aa11bb         # resume specific session by id
hermes --tui --resume "my t0p session"         # resume by title
hermes --tui --dev                             # run source directly, skip prebuild (TUI contributors)
```

It can also be enabled via env var (`export HERMES_TUI=1`, after which bare `hermes`/`hermes chat` use the TUI) or made the persistent default in `~/.hermes/config.yaml`:

```yaml
display:
  interface: tui   # "cli" (default) or "tui"
```

Explicit flags always win: `hermes --cli` drops to the classic REPL for one invocation, and `hermes --tui` / `HERMES_TUI=1` forces the TUI when the config default is `cli`.

## Why the TUI

The source lists the TUI's advantages over the classic REPL: **instant first frame** (banner paints before load completes); **non-blocking input** (type and queue before the session is ready — the first prompt sends the moment the agent comes online); **rich overlays** (model picker, session picker, approval/clarification prompts render as modal panels); a **live session panel** that fills in tools/skills progressively; **mouse-friendly selection** (drag-to-highlight with a uniform background, copy via the terminal's normal gesture); **alternate-screen rendering** (differential updates → no flicker when streaming, no scrollback clutter after quit); and **composer affordances** (inline paste-collapse, `Cmd+V`/`Ctrl+V` text paste with clipboard-image fallback, bracketed-paste safety, image/file-path attachment normalization). The same skins and personalities apply — switch mid-session with `/skin ares` or `/personality pirate` and the UI repaints live.

### Collapsible banner sections

The startup banner groups runtime info into four collapsible sections, each with a `▸`/`▾` chevron. Tools opens by default (most-checked at session start); Skills, System Prompt, and MCP Servers collapse by default so the banner stays compact. Click a header or chevron to toggle; state is local to the banner instance and resets to defaults on the next launch.

## Requirements

- **Node.js ≥ 20** — the TUI runs as a subprocess launched from the Python CLI; `hermes doctor` verifies this.
- **TTY** — like the classic CLI, piping stdin or non-interactive environments falls back to single-query mode.

On first launch Hermes installs the TUI's Node dependencies into `ui-tui/node_modules` (one-time). The bundle rebuilds automatically when sources are newer than the dist. Distributions shipping a prebuilt bundle can point Hermes at it (the directory must contain `dist/entry.js`):

```bash
export HERMES_TUI_DIR=/path/to/prebuilt/ui-tui
hermes --tui
```

## Keybindings & Slash Commands

Keybindings match the [Classic CLI](hermes_cli_interface.md) exactly. Behavioral differences: mouse-drag highlights with a uniform selection background; `Cmd+V`/`Ctrl+V` tries text paste, then OSC52/native clipboard reads, then image-attach; `/terminal-setup` installs VS Code/Cursor/Windsurf bindings; slash autocompletion opens as a floating panel; `Ctrl+X` opens the live session switcher (or deletes a highlighted queued message, with `Esc` cancelling); `Ctrl+G` / `Ctrl+X Ctrl+E` opens the input buffer in `$EDITOR`.

All slash commands work unchanged; a few are **TUI-owned** — producing richer output or rendering as overlays rather than inline panels:

| Command | TUI behavior |
|---------|--------------|
| `/help` | Overlay with categorized commands, arrow-key navigable |
| `/sessions` (alias `/switch`) | Live session switcher — list/switch/close/start TUI sessions |
| `/model` | Modal model picker grouped by provider, with cost hints |
| `/skin` | Live preview — theme change applies as you browse |
| `/details` | Toggle verbose tool-call details (global or per-section) |
| `/usage` | Rich token / cost / context panel |
| `/agents` (alias `/tasks`) | Observability overlay — live subagent tree with kill/pause, per-branch cost/token/file rollups, turn-by-turn history |
| `/reload` | Re-reads `~/.hermes/.env` so new API keys take effect without a restart |
| `/mouse [on\|off\|toggle\|wheel\|buttons\|all]` | Pick a mouse-tracking preset at runtime (persists to `display.mouse_tracking`) |

Every other slash command (installed skills, quick commands, personality toggles) works identically to the classic CLI.

## Live Session Switcher

The live session switcher turns one terminal into a dispatcher for several TUI sessions. It lists only sessions currently live in this TUI process; closed sessions remain saved transcripts reopenable with `/resume` or `hermes --tui --resume <id-or-title>`. Open it via `Ctrl+X`, `/sessions`/`/switch`, `/sessions new`, or by clicking the `N live sessions` count in the status line. Inside the switcher: `↑`/`↓` move selection; `Enter` switches; `Ctrl+D` closes the selected session; `Ctrl+N` starts a blank session; `Ctrl+R` refreshes the list; `Esc` closes. Selecting `+new`, typing a prompt, and pressing `Enter` dispatches a new live session (press `Tab` first to choose a model just for it).

## Rendering, Theming & Indicators

**LaTeX math rendering** is always-on: the TUI's markdown pipeline renders `$E = mc^2$` and `$$\frac{a}{b}$$` as Unicode-formatted math (unsupported syntax falls back to a copyable code span); the classic CLI keeps the raw TeX. **Light-terminal detection** swaps to the light theme in three priority layers — `HERMES_TUI_THEME` env var (`light`/`dark`/raw 6-char hex), then `COLORFGBG`, then an OSC 11 background probe (Ghostty, Warp, iTerm2, WezTerm, Kitty). The status-bar **busy indicator** is pluggable (default rotates Hermes' kawaii face palette every 2.5s):

```yaml
display:
  tui_status_indicator: kaomoji   # kaomoji | emoji | unicode | ascii
```

Or `/indicator emoji` in-session; styles ship with matched glyph widths so the status bar doesn't jitter.

## Auto-resume & Status Line

By default `hermes --tui` starts a fresh session each launch. Opt into re-attaching to the most recent (or a specific) TUI session with `export HERMES_TUI_RESUME=1` (or `=<session-id>`); unset it or pass `--resume <id>` to override per-launch. The status line tracks agent state in real time — `starting agent…`, `ready`, `thinking…`/`running…`, `interrupted`, `forging session…`/`resuming…` — with per-skin colors shared with the classic CLI. It also shows: the working directory with git branch (mtime-cached, updates on side-terminal `git checkout`), per-prompt elapsed time (`⏱ 12s/3m 45s` live, `⏲` frozen after the turn), `🗜️ N` (auto-compression count), `▶ N` (running `/background` tasks), and `⚠ YOLO` (auto-approving mode warning, also shown in the banner).

## Configuration

The TUI respects all standard Hermes config (`~/.hermes/config.yaml`, profiles, personalities, skins, quick commands, credential pools, memory providers, tool/skill enablement) — **no TUI-specific config file exists**. A handful of `display.*` keys tune the TUI surface:

```yaml
display:
  skin: default              # any built-in or custom skin
  personality: helpful
  details_mode: collapsed    # hidden | collapsed | expanded — global accordion default
  sections:                  # optional per-section overrides
    thinking: expanded
    tools: expanded
    activity: collapsed      # opt back IN to the activity panel (hidden by default)
  mouse_tracking: all        # off | wheel | buttons | all (wheel=scroll+click; buttons=+drag; all=+hover)
```

Runtime toggles: `/details [hidden|collapsed|expanded|cycle]` sets the global mode; `/details <section> [hidden|collapsed|expanded|reset]` overrides one section (`thinking`, `tools`, `subagents`, `activity`). **Default visibility** streams the turn as a live transcript: `thinking` **expanded**, `tools` **expanded**, `subagents` follows the global `details_mode` (collapsed), `activity` **hidden** (ambient meta is noise; tool failures still render inline, ambient errors surface via a floating-alert backstop). Per-section overrides win over both the section default and the global mode, so existing configs keep working.

## Sessions

Sessions are shared between the TUI and classic CLI — both write to the same `~/.hermes/state.db`. Start a session in one, resume in the other; the session picker surfaces sessions from both sources with a source tag. See [Sessions](hermes_sessions_lifecycle_resume.md) for lifecycle, search, compression, and export.

## How the TUI Talks to Its Gateway

By default the TUI spawns its own **in-process gateway**, so each TUI instance is self-contained — nothing to configure. The `HERMES_TUI_GATEWAY_URL` env var seen in the codebase/logs is an **internal wiring detail of the web dashboard**, not a user-facing remote-attach knob. When you open the dashboard's "Chat" tab (`hermes dashboard` → `/chat`), the dashboard's web server spawns an embedded TUI child and injects `HERMES_TUI_GATEWAY_URL` so the child attaches to the dashboard's own in-process `tui_gateway` over a loopback WebSocket (`/api/ws`). That endpoint exists only inside the dashboard server (`hermes_cli/web_server.py`) and is bound to that process's lifetime and auth. There is **no** "point any TUI at any standalone gateway port" mode — in particular the OpenAI-compatible API server (`hermes gateway` / `api_server`) does not serve `/api/ws` (it is the model-backend surface: `/v1/chat/completions`, `/v1/models`, …) and setting `HERMES_TUI_GATEWAY_URL` to that port will 404. To share sessions across surfaces, use the shared `state.db` or the dashboard's embedded chat — not a hand-set gateway URL.

## Reverting to the Classic CLI

Launching `hermes` (without `--tui`) stays on the classic CLI by default. To prefer the TUI on a machine, set `display.interface: tui` (persistent) or `HERMES_TUI=1` (per-shell). To go back, set `interface: cli` / unset the env var, or pass `hermes --cli` for a one-off. If the TUI fails to launch (no Node, missing bundle, TTY issue), Hermes prints a diagnostic and **falls back** rather than leaving you stuck.

**Source**: `inbox/hermes_agent_docs/user-guide/tui.md` · https://hermes-agent.nousresearch.com/docs/user-guide/tui
**Last Updated**: 2026-06-19
**Status**: Active
