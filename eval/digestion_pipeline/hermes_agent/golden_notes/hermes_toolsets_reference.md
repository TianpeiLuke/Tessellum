---
tags:
  - resource
  - documentation
  - hermes_agent
  - toolsets
  - tools
keywords:
  - hermes toolsets reference
  - core composite platform toolsets
  - dynamic mcp toolsets
  - configuring toolsets
  - wildcards capability gating
  - hermes tools command
topics:
  - Hermes Agent
  - Toolsets
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference
access_control_group: ["general"]
---

# Hermes Agent — Toolsets Reference

## Overview

A **toolset** in Hermes is a named bundle of tools that controls what the agent can do; toolsets are the primary mechanism for configuring tool availability per platform, per session, or per task. Every individual tool belongs to exactly one toolset, and enabling a toolset makes all of its tools available to the agent. This reference enumerates the three kinds of toolset — **core** (a single logical group of related tools, e.g. `file` bundles `read_file`/`write_file`/`patch`/`search_files`), **composite** (combines multiple core toolsets for a common scenario, e.g. `debugging` bundles file + terminal + web), and **platform** (a complete tool configuration for a deployment context, e.g. `hermes-cli` is the default for interactive CLI sessions) — plus the **dynamic** toolsets generated at runtime from MCP servers, plugins, and custom `config.yaml` definitions. It also documents the three configuration surfaces (the CLI `--toolsets` flag, the per-platform `config.yaml` list, and the interactive `hermes tools` UI), wildcard matching, the capability/workflow gating that overrides `all`/`*`, and how toolsets relate to the finer-grained `hermes tools` command. The individual tools each toolset bundles are documented in the [Tools Reference](hermes_tools_reference_core.md).

## How Toolsets Work

Every tool belongs to exactly one toolset. When you enable a toolset, all tools in that bundle become available to the agent. Toolsets come in three kinds:

- **Core** — A single logical group of related tools (e.g., `file` bundles `read_file`, `write_file`, `patch`, `search_files`).
- **Composite** — Combines multiple core toolsets for a common scenario (e.g., `debugging` bundles file, terminal, and web tools).
- **Platform** — A complete tool configuration for a specific deployment context (e.g., `hermes-cli` is the default for interactive CLI sessions).

## Configuring Toolsets

Toolsets can be activated on three surfaces — per-session via the CLI flag, per-platform via `config.yaml`, or interactively via the curses UI.

### Per-session (CLI)

```bash
hermes chat --toolsets web,file,terminal
hermes chat --toolsets debugging        # composite — expands to file + terminal + web
hermes chat --toolsets all              # everything
```

### Per-platform (config.yaml)

```yaml
toolsets:
  - hermes-cli          # default for CLI
  # - hermes-telegram   # override for Telegram gateway
```

### Interactive management

```bash
hermes tools                            # curses UI to enable/disable per platform
```

Or in-session: `/tools list`, `/tools disable browser`, `/tools enable homeassistant`.

## Core Toolsets

Core toolsets are the single logical groups of related tools. A representative selection (the source table lists all):

| Toolset | Tools | Purpose |
|---------|-------|---------|
| `browser` | `browser_back`, `browser_cdp`, `browser_click`, `browser_console`, `browser_dialog`, `browser_get_images`, `browser_navigate`, `browser_press`, `browser_scroll`, `browser_snapshot`, `browser_type`, `browser_vision`, `web_search` | Core browser automation. Includes `web_search` as a fallback. `browser_cdp`/`browser_dialog` are gated at runtime — registered only when a CDP endpoint is reachable at session start (via `/browser connect`, `browser.cdp_url` config, Browserbase, or Camofox). |
| `clarify` | `clarify` | Ask the user a question when the agent needs clarification. |
| `code_execution` | `execute_code` | Run Python scripts that call Hermes tools programmatically. |
| `cronjob` | `cronjob` | Schedule and manage recurring tasks. |
| `debugging` | composite (`file` + `terminal` + `web`) | Debug bundle — file, process/terminal, web extract/search. |
| `delegation` | `delegate_task` | Spawn isolated subagent instances for parallel work. |
| `discord` / `discord_admin` | `discord` / `discord_admin` | Core Discord text/embed/DM actions and moderation (gateway-only; active on `hermes-discord`). |
| `feishu_doc` / `feishu_drive` | `feishu_doc_read` / four `feishu_drive_*` comment ops | Feishu/Lark document read + drive comment operations (scoped to the comment agent). |
| `file` | `patch`, `read_file`, `search_files`, `write_file` | File reading, writing, searching, and editing. |
| `homeassistant` | `ha_call_service`, `ha_get_state`, `ha_list_entities`, `ha_list_services` | Smart home control via Home Assistant. Only available when `HASS_TOKEN` is set. |
| `computer_use` | `computer_use` | Background macOS desktop control via cua-driver. macOS only; requires `cua-driver` on `$PATH`. |
| `context_engine` | (varies) | Runtime tools exposed by the active context-engine plugin (empty until a plugin populates it). |
| `image_gen` / `video_gen` | `image_generate` / `video_generate` | Text-to-image (FAL.ai, opt-in OpenAI/xAI) and text/image-to-video (xAI Grok-Imagine, FAL.ai Veo 3.1 / Pixverse v6 / Kling O3). |
| `kanban` | nine `kanban_*` tools | Multi-agent coordination. Registered for dispatcher-spawned task workers (`HERMES_KANBAN_TASK`) and profiles that list `kanban` by name; the `all`/`*` wildcard does **not** enable it. |
| `memory` | `memory` | Persistent cross-session memory management. |
| `messaging` | `send_message` | Send messages to other platforms (Telegram, Discord, etc.) from within a session. |
| `moa` | `mixture_of_agents` | Multi-model consensus via Mixture of Agents. |
| `safe` | `image_generate`, `vision_analyze`, `web_extract`, `web_search` (via `includes`) | Read-only research + media generation. No file writes, no terminal, no code execution. |
| `search` / `web` | `web_search` / `web_extract` + `web_search` | Web search only, or search plus page-content extraction. |
| `session_search` | `session_search` | Search past conversation sessions. |
| `skills` | `skill_manage`, `skill_view`, `skills_list` | Skill CRUD and browsing. |
| `spotify` | seven `spotify_*` tools | Native Spotify control (playback, queue, search, playlists, albums, library). Registered by the bundled `spotify` plugin. |
| `terminal` | `process`, `terminal` | Shell command execution and background process management. |
| `todo` / `tts` / `vision` / `video` | `todo` / `text_to_speech` / `vision_analyze` / `video_analyze` | Task-list, text-to-speech, image analysis, and (opt-in) video understanding. |
| `x_search` | `x_search` | Search X (Twitter) via xAI's built-in Responses tool. Off by default; schema registered only when xAI credentials (SuperGrok OAuth or `XAI_API_KEY`) are configured. |
| `yuanbao` | five `yb_*` tools | Yuanbao DM/group actions and sticker search. Registered only on `hermes-yuanbao`. |

## Platform Toolsets

Platform toolsets define the complete tool configuration for a deployment target. Most messaging platforms use the same set as `hermes-cli`:

| Toolset | Differences from `hermes-cli` |
|---------|-------------------------------|
| `hermes-cli` | Full toolset — the default for interactive CLI sessions. Includes file, terminal, web, browser, memory, skills, vision, image_gen, todo, tts, delegation, code_execution, cronjob, session_search, clarify, and `safe` bundles plus the standard messaging tools. |
| `hermes-acp` | Drops `clarify`, `cronjob`, `image_generate`, `send_message`, `text_to_speech`, and all four Home Assistant tools. Focused on coding tasks in IDE context. |
| `hermes-api-server` | Drops `clarify`, `send_message`, and `text_to_speech`. Keeps everything else — suitable for programmatic access where user interaction isn't possible. |
| `hermes-discord` | Adds `discord` and `discord_admin` on top of `hermes-cli`. |
| `hermes-feishu` | Adds the five `feishu_doc_*` / `feishu_drive_*` tools (only used by the document-comment handler). |
| `hermes-yuanbao` | Adds the five `yb_*` tools (DM/group/sticker) on top of `hermes-cli`. |
| `hermes-homeassistant` | Same as `hermes-cli` (Home Assistant tools already present by default; activate when `HASS_TOKEN` is set). |
| `hermes-cron`, `hermes-telegram`, `hermes-slack`, `hermes-whatsapp`, `hermes-signal`, `hermes-matrix`, `hermes-mattermost`, `hermes-email`, `hermes-sms`, `hermes-bluebubbles`, `hermes-dingtalk`, `hermes-qqbot`, `hermes-wecom`, `hermes-wecom-callback`, `hermes-weixin`, `hermes-webhook` | Same as `hermes-cli`. |
| `hermes-gateway` | Internal gateway orchestrator toolset — union of every `hermes-<platform>` toolset; used when the gateway needs to accept any message source. |

## Dynamic Toolsets

### MCP server toolsets

Each configured MCP server generates a `mcp-<server>` toolset at runtime. For example, configuring a `github` MCP server creates a `mcp-github` toolset containing all tools that server exposes:

```yaml
# config.yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
```

This creates a `mcp-github` toolset you can reference in `--toolsets` or platform configs.

### Plugin and custom toolsets

Plugins register their own toolsets via `ctx.register_tool()` during plugin initialization; these appear alongside built-in toolsets and toggle the same way. You can also define project-specific bundles in `config.yaml`:

```yaml
toolsets:
  - hermes-cli
custom_toolsets:
  data-science:
    - file
    - terminal
    - code_execution
    - web
    - vision
```

### Wildcards

`all` or `*` expands to every registered toolset (built-in + dynamic + plugin). A handful of tools have an additional availability check on top of toolset membership and are **not** turned on by `all`/`*` alone:

- **Capability-gated** tools (browser, `computer_use`, `code_execution`, Feishu, Home Assistant, cronjob) appear only when their backend/credential prerequisite is configured.
- **Workflow-gated** tools — the `kanban` toolset — are deliberately opt-in. `all`/`*` does **not** enable kanban; you must list `kanban` explicitly (or be a dispatcher-spawned worker with `HERMES_KANBAN_TASK` set), because kanban tools mutate shared board state.

## Relationship to `hermes tools`

The `hermes tools` command provides a curses-based UI for toggling individual tools on or off per platform. This operates at the tool level (finer than toolsets) and persists to `config.yaml`. Disabled tools are filtered out even if their toolset is enabled. See [Tools Reference](hermes_tools_reference_core.md) for the complete list of individual tools and their parameters.

**Source**: `inbox/hermes_agent_docs/reference/toolsets-reference.md` · https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference
**Last Updated**: 2026-06-19
**Status**: Active
