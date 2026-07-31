---
tags:
  - resource
  - documentation
  - hermes_agent
  - codex_runtime
  - tooling
keywords:
  - codex app-server runtime
  - codex built-in tools
  - hermes tool callback
  - native codex plugins
  - agent-loop tools unavailable
  - json-rpc over stdio
topics:
  - Hermes Agent
  - Codex App-Server Runtime
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/codex-app-server-runtime
access_control_group: ["general"]
---

# Hermes Agent — Codex Runtime Tool Model

## Overview

The Codex app-server runtime is an **opt-in alternate execution runtime** in which Hermes hands `openai/*` and `openai-codex/*` turns to the [Codex CLI app-server](https://github.com/openai/codex) instead of running its own tool loop. When it is on, terminal commands, file edits, sandboxing, and MCP tool calls all execute inside Codex's runtime, and Hermes becomes the shell around it (sessions DB, slash commands, gateway, memory and skill review). This note is the **tool-availability and architecture model** for that runtime; the companion enable/operate procedure is [hermes_codex_runtime_setup](hermes_codex_runtime_setup.md).

The central fact this model captures: when the runtime is on, the model running your turn has **three independent sources of tools** (Codex built-ins, auto-migrated native Codex plugins, and the `hermes-tools` MCP callback), and **four Hermes agent-loop tools that are unavailable** because a stateless MCP callback cannot drive them. The runtime never auto-engages — default behavior is unchanged unless you flip the flag.

## Why

The page motivates the runtime with five payoffs:

- Run OpenAI agent turns against your **ChatGPT subscription** (no API key required) using the same auth flow Codex CLI uses.
- Use **Codex's own toolset and sandbox** — `shell` for terminal/read/write/search, `apply_patch` for structured edits, `update_plan` for planning, all running inside seatbelt/landlock sandboxing.
- **Native Codex plugins** — Linear, GitHub, Gmail, Calendar, Canva, etc. — installed via `codex plugin` are auto-migrated and active in your Hermes session.
- **Hermes' richer tools come along** — web_search, web_extract, browser automation, vision, image generation, skills, and TTS work via an MCP callback. Codex calls back into Hermes for tools it doesn't have built in.
- **Memory and skill nudges keep working** — Codex's events are projected into Hermes' message shape so the self-improvement loop sees a normal-looking transcript.

## What Tools the Model Actually Has

When this runtime is on, the model running your turn has three independent sources of tools, plus a fourth group that is explicitly unavailable.

### 1. Codex's built-in toolset (always on)

These ship with `codex app-server` itself — no Hermes involvement, no MCP, no plugins. All five are available the moment the runtime starts:

- **`shell`** — runs arbitrary shell commands inside the sandbox. This is how the model reads files (`cat`, `head`, `tail`), writes them (`echo > foo`, heredocs), searches them (`find`, `rg`, `grep`), navigates directories (`ls`, `cd`), runs builds, manages processes, and anything else you'd do in bash.
- **`apply_patch`** — applies a structured multi-file diff in Codex's patch format. The model uses this for non-trivial code edits (adding a function, refactoring across files); shell heredocs are still available for one-off writes.
- **`update_plan`** — codex's internal todo / plan tracker. Equivalent of Hermes' `todo` tool, but managed entirely inside codex's runtime.
- **`view_image`** — load a local image file into the conversation so the model can see it.
- **`web_search`** — codex has its own built-in web search when configured. Hermes also exposes `web_search` (Firecrawl-backed) via the callback below; the model picks whichever it prefers.

So **anything you'd do via terminal — read/write/search/find/run — codex does natively**. The sandbox profile (`:workspace` by default on enable) controls what's writable.

### 2. Native Codex plugins (auto-migrated)

When you enable the runtime, Hermes queries codex's `plugin/list` RPC and writes a `[plugins."<name>@openai-curated"]` entry for every installed plugin; the plugins are managed by codex and authorized once via codex's own UI. Examples: **Linear**, **GitHub**, **Gmail**, **Google Calendar**, **Outlook calendar/email**, **Canva**, and whatever else you've installed via `codex plugin marketplace add openai-curated` + `codex plugin install ...`. What's NOT migrated: plugins you haven't installed yet, and ChatGPT app marketplace entries (`app/list`), which are already enabled inside codex by your account auth.

### 3. Hermes tool callback (MCP server in `~/.codex/config.toml`)

Hermes registers itself as an MCP server so codex can call back for tools codex doesn't ship with. Available via the callback:

- **`web_search`** / **`web_extract`** — Firecrawl-backed; tends to be cleaner than scraping for structured content.
- **`browser_navigate` / `browser_click` / `browser_type` / `browser_press` / `browser_snapshot` / `browser_scroll` / `browser_back` / `browser_get_images` / `browser_console` / `browser_vision`** — full browser automation via Camofox or Browserbase.
- **`vision_analyze`** — call a separate vision model to inspect an image (different from codex's `view_image` which loads it into the conversation).
- **`image_generate`** — image generation through Hermes' image_gen plugin chain.
- **`skill_view` / `skills_list`** — read from Hermes' skill library.
- **`text_to_speech`** — TTS through Hermes' configured provider.

When the model wants one of these, codex spawns the `hermes_tools_mcp_server` subprocess via stdio MCP, the call is dispatched through `model_tools.handle_function_call()` (same code path as Hermes' default runtime), and the result is returned to codex like any other MCP response.

### What's NOT available on this runtime

These four Hermes tools require the running `AIAgent` context (mid-loop state) to dispatch, and a stateless MCP callback can't drive them. Switch back to the default runtime (`/codex-runtime auto`) when you need any of them:

- **`delegate_task`** — spawn subagents
- **`memory`** — Hermes' persistent memory store
- **`session_search`** — cross-session search
- **`todo`** — Hermes' todo store (codex's `update_plan` is the in-runtime equivalent)

## Workflow Features (`/goal`, kanban, cron)

- **`/goal` (the Ralph loop) — works.** Goals persist in `state_meta` keyed by session id; the continuation prompt feeds back as a normal user message through `run_conversation()`, and codex executes the next turn natively. The goal judge runs via the auxiliary client (`auxiliary.goal_judge`), independent of the active runtime. Caveat: each continuation is a fresh codex turn, so codex re-evaluates command-approval policy from scratch — expect more prompts on long write-heavy goals; `default_permissions = ":workspace"` (set automatically on enable) keeps simple workspace writes from prompting.
- **Kanban (multi-agent worktree dispatch) — works, with one subtle dependency.** The dispatcher spawns each worker as a separate `hermes chat -q` subprocess that reads the user's config, so a global `model.openai_runtime: codex_app_server` brings workers up on the codex runtime too. Inside a worker, Codex's full toolset, the migrated plugins, and the Hermes callback all work. The worker handoff tools — `kanban_complete` / `kanban_block` / `kanban_comment` / `kanban_heartbeat` — work **because the MCP callback exposes them**; they read `HERMES_KANBAN_TASK` from env (set by the dispatcher, propagated through the codex subprocess to the `hermes-tools` MCP subprocess) and write to the per-board SQLite DB pinned by `HERMES_KANBAN_DB`. Without them, a worker could do its task but not report back. `kanban_show` / `kanban_list` are read-only; `kanban_create` / `kanban_unblock` / `kanban_link` are orchestrator-only. For app-server workers with `HERMES_KANBAN_TASK` present, Hermes passes narrow sandbox overrides: keep `workspace-write`, add the board DB directory plus every pinned Kanban path as extra writable roots, keep network disabled — avoiding the brittle `:danger-no-sandbox` workaround.
- **Cron jobs — not specifically tested.** Cron runs via `cronjob` → `AIAgent.run_conversation`, the same code path as the CLI. If the cron config has `openai_runtime: codex_app_server`, it runs on codex with the same rules (built-ins + plugins + callback work; agent-loop tools don't). If a cron job relies on those, scope it to a default-runtime profile.

## Trade-offs

The model side-by-side comparing the two runtimes (verbatim source table):

|  | Hermes default runtime | Codex app-server (opt-in) |
|---|---|---|
| `delegate_task` subagents | yes | not available — needs agent loop context |
| `memory`, `session_search`, `todo` | yes | not available — needs agent loop context |
| `web_search`, `web_extract` | yes | yes (via MCP callback) |
| Browser automation (Camofox/Browserbase) | yes | yes (via MCP callback) |
| `vision_analyze`, `image_generate` | yes | yes (via MCP callback) |
| `skill_view`, `skills_list` | yes | yes (via MCP callback) |
| `text_to_speech` | yes | yes (via MCP callback) |
| Codex `shell` (terminal/read/write/search/find/run) | — | yes (Codex built-in) |
| Codex `apply_patch` (structured multi-file edits) | — | yes (Codex built-in) |
| Codex `update_plan` (in-runtime todo) | — | yes (Codex built-in) |
| Codex `view_image` (load image into conversation) | — | yes (Codex built-in) |
| Codex sandbox (seatbelt/landlock, profiles) | — | yes (Codex built-in) |
| ChatGPT subscription auth | — | yes (via `openai-codex` provider) |
| Native Codex plugins (Linear, GitHub, etc.) | — | yes (auto-migrated) |
| User MCP servers | yes | yes (auto-migrated to codex) |
| Memory + skill review (background) | yes | yes (via item projection) |
| Multi-turn conversations | yes | yes |
| `/goal` (Ralph loop) | yes | yes |
| Kanban worker dispatch | yes | yes (via callback) |
| Kanban orchestrator tools | yes | yes (via callback) |
| All gateway platforms | yes | yes |
| Non-OpenAI providers | yes | n/a — OpenAI/Codex-scoped |

## Hermes Tool Callback (the MCP server)

Codex's built-in toolset covers shell/file ops/patches but doesn't have web search, browser automation, vision, image generation, etc. To keep those usable in a codex turn, Hermes registers itself as an MCP server in `~/.codex/config.toml`:

```toml
[mcp_servers.hermes-tools]
command = "/path/to/python"
args = ["-m", "agent.transports.hermes_tools_mcp_server"]
env = { HERMES_HOME = "/your/.hermes", PYTHONPATH = "...", HERMES_QUIET = "1" }
startup_timeout_sec = 30.0
tool_timeout_sec = 600.0
```

When the model calls `web_search` (or another exposed Hermes tool), codex spawns the `hermes_tools_mcp_server` subprocess via stdio, the request is dispatched through `model_tools.handle_function_call()`, and the result is projected back to codex like any other MCP response. **Available via the callback:** `web_search`, `web_extract`, `browser_*` automation, `vision_analyze`, `image_generate`, `skill_view`, `skills_list`, `text_to_speech` (the full browser set is listed in §What Tools above). **NOT available:** `delegate_task`, `memory`, `session_search`, `todo` (need the running `AIAgent` context).

## Architecture

The runtime forks at `AIAgent.run_conversation()`: when `api_mode == codex_app_server`, the turn routes to `CodexAppServerSession`, which speaks JSON-RPC over stdio to the codex app-server subprocess; otherwise it runs `chat_completions` / `codex_responses` (default). The subprocess hosts the built-in tools + sandbox and an MCP client (user MCP servers, native plugins, and `hermes-tools`); the `hermes-tools` arm calls back to the on-demand `hermes_tools_mcp_server.py` subprocess. Source diagram (verbatim, fenced — not Mermaid):

```
                ┌─── Hermes shell (CLI / TUI / gateway) ───┐
                │  sessions DB · slash commands · memory   │
                │  & skill review · cron · session pickers │
                └──┬──────────────────────────────────────┬┘
                   │ user_message               final     │
                   ▼                            text +    │
        ┌──────────────────────────────────┐   projected  │
        │  AIAgent.run_conversation()       │   messages   │
        │   if api_mode == codex_app_server │              │
        │     → CodexAppServerSession       │              │
        │   else: chat_completions / codex_responses (default)
        └────┬─────────────────────────────┘              │
             │ JSON-RPC over stdio                        │
             ▼                                            │
        ┌──────────────────────────────────┐              │
        │  codex app-server (subprocess)    │──────────────┘
        │   thread/start, turn/start        │
        │   item/* notifications            │
        │   shell + apply_patch + update_plan│
        │   view_image + sandbox            │
        │   ┌─────────────────────────┐     │
        │   │  MCP client             │     │
        │   │  ├─ user MCP servers    │     │
        │   │  ├─ native plugins      │     │
        │   │  │   (linear, github,   │     │
        │   │  │    gmail, calendar,  │     │
        │   │  │    canva, ...)       │     │
        │   │  └─ hermes-tools ───────┼─────────────────┐
        │   │       (callback to     │     │           │
        │   │        Hermes' richer  │     │           │
        │   │        tools)          │     │           │
        │   └─────────────────────────┘     │           │
        └──────────────────────────────────┘           │
                                                        │
                                                        ▼
        ┌──────────────────────────────────────────────────────────┐
        │  hermes_tools_mcp_server.py (subprocess on demand)        │
        │   web_search, web_extract, browser_*, vision_analyze,    │
        │   image_generate, skill_view, skills_list, text_to_speech│
        └──────────────────────────────────────────────────────────┘
```

For implementation details, see [PR #24182](https://github.com/NousResearch/hermes-agent/pull/24182) and the [Codex app-server protocol README](https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md).

**Source**: `inbox/hermes_agent_docs/user-guide/features/codex-app-server-runtime.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/codex-app-server-runtime
**Last Updated**: 2026-06-19
**Status**: Active
