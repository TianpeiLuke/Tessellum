---
tags:
  - resource
  - documentation
  - hermes_agent
  - tools
  - reference
keywords:
  - hermes built-in tools
  - core agent toolset
  - file terminal code_execution tools
  - cronjob delegation memory
  - skill_view skill_manage skills_list
  - mcp dynamic tools
topics:
  - Hermes Agent
  - Tools Reference
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/reference/tools-reference
access_control_group: ["general"]
---

# Hermes Agent — Built-in Tools Reference (Core Agent Toolsets)

## Overview

This is the **registry of Hermes' core agent tools** — the local, model-agnostic capabilities every Hermes session can call without a platform or external credential: the `file`, `terminal`, `code_execution`, `cronjob`, `delegation`, `memory`, `session_search`, `skills`, `todo`, `clarify`, `moa`, and `vision` toolsets. It is one half of the built-in tools registry; the platform/media/browser tools (browser, computer_use, image/video gen, web, kanban, messaging, Discord, Spotify, Feishu, Yuanbao) live in the companion note. The source page documents Hermes' built-in tools grouped by toolset, noting that **availability varies by platform, credentials, and enabled toolsets**. These are the schema-guarded functions the agent loop exposes to the model as callable tools (function-calling); each row below carries the tool's exact registry name and its one-line description verbatim from the reference, plus its gating requirement when one exists. Tools listed here generally have **no environment requirement** (the `Requires environment` column is empty) — they are the agent's always-available local primitives.

## Quick Counts (current registry)

The reference opens with a quick count of the whole registry — **~71 tools** spanning all toolsets. The core-agent tools documented in this note are the always-available "standalone" tools plus the small grouped toolsets:

- **4 file tools** — `patch`, `read_file`, `search_files`, `write_file`.
- **2 terminal tools** — `terminal`, `process`.
- **Standalone tools** — `memory`, `clarify`, `delegate_task`, `execute_code`, `cronjob`, `session_search`, `skill_view` / `skill_manage` / `skills_list`, `vision_analyze`, `mixture_of_agents`, `todo`.

(The platform-tool counts — 10+2 browser, 4 Home Assistant, 5 Feishu, 7 Spotify, 5 Yuanbao, 9 kanban, 2 Discord, plus `send_message`, `image_generate`, `video_generate`, `video_analyze`, `text_to_speech`, `computer_use` — are documented in the platform/media companion note.)

## MCP Dynamic Tools

Beyond built-in tools, Hermes can load tools dynamically from MCP servers. MCP tools appear with the prefix `mcp_<server>_` (for example, `mcp_github_create_issue` for the `github` MCP server). These are not part of the built-in registry — they are registered at session start from the configured `mcp_servers`. See the MCP integration feature pages and the `hermes_mcp_config_reference` note for the server-config schema and tool-naming rules.

## `file` toolset

The local filesystem tools. Hermes steers the model toward these instead of shell `cat`/`grep`/`sed` so output is structured (line numbers, unified diffs) and edits are fuzzy-matched.

| Tool | Description |
|------|-------------|
| `patch` | Targeted find-and-replace edits in files. Use this instead of sed/awk in terminal. Uses fuzzy matching (9 strategies) so minor whitespace/indentation differences won't break it. Returns a unified diff. Auto-runs syntax checks after editing. |
| `read_file` | Read a text file with line numbers and pagination. Use this instead of cat/head/tail in terminal. Output format: `LINE_NUM\|CONTENT`. Suggests similar filenames if not found. Use offset and limit for large files. Cannot read images. |
| `search_files` | Search file contents or find files by name. Use this instead of grep/rg/find/ls in terminal. Ripgrep-backed, faster than shell equivalents. Content search (`target='content'`): regex search inside files with full-match or other output modes. |
| `write_file` | Write content to a file, completely replacing existing content. Use this instead of echo/cat heredoc in terminal. Creates parent directories automatically. OVERWRITES the entire file — use `patch` for targeted edits. |

## `terminal` toolset

| Tool | Description |
|------|-------------|
| `terminal` | Execute shell commands on a Linux environment. Filesystem persists between calls. Set `background=true` for long-running servers. Set `notify_on_complete=true` (with `background=true`) to get an automatic notification when the process finishes — no polling needed. Do NOT use cat/head/tail — use read_file. Do NOT use grep/rg/find — use search_files. |
| `process` | Manage background processes started with `terminal(background=true)`. Actions: `'list'` (show all), `'poll'` (check status + new output), `'log'` (full output with pagination), `'wait'` (block until done or timeout), `'kill'` (terminate), `'write'` (send input). |

## `code_execution` toolset

| Tool | Description |
|------|-------------|
| `execute_code` | Run a Python script that can call Hermes tools programmatically. Use this when you need 3+ tool calls with processing logic between them, need to filter/reduce large tool outputs before they enter your context, or need conditional branching across tool calls. |

## `cronjob` toolset

| Tool | Description |
|------|-------------|
| `cronjob` | Unified scheduled-task manager. Use `action="create"`, `"list"`, `"update"`, `"pause"`, `"resume"`, `"run"`, or `"remove"` to manage jobs. Supports skill-backed jobs with one or more attached skills, and `skills=[]` on update clears attached skills. Cron runs happen in fresh sessions with no current-chat context. |

## `delegation` toolset

| Tool | Description |
|------|-------------|
| `delegate_task` | Spawn one or more subagents to work on tasks in isolated contexts. Each subagent gets its own conversation, terminal session, and toolset. Only the final summary is returned — intermediate tool results never enter your context window. |

## `memory` toolset

| Tool | Description |
|------|-------------|
| `memory` | Save important information to persistent memory that survives across sessions. Your memory appears in your system prompt at session start — it's how you remember things about the user and your environment between conversations. |

The source also notes that **Honcho tools** (`honcho_profile`, `honcho_search`, `honcho_context`, `honcho_reasoning`, `honcho_conclude`) are **no longer built-in** — they ship via the Honcho memory-provider plugin (`plugins/memory/honcho/`) and are installed through the Memory Providers feature, not the core registry.

## `session_search` toolset

| Tool | Description |
|------|-------------|
| `session_search` | Search past sessions stored in the local session DB, or scroll inside one. FTS5-backed retrieval; returns actual messages from the DB (no LLM calls). Three shapes: discovery (pass `query`), scroll (pass `session_id` + `around_message_id`), browse (no args). |

## `skills` toolset

| Tool | Description |
|------|-------------|
| `skill_view` | Load a skill's full content or access its linked files (references, templates, scripts). First call returns SKILL.md content plus a manifest of linked files. Skills let the agent load information about specific tasks and workflows. |
| `skill_manage` | Manage skills (create, update, delete). Skills are your procedural memory — reusable approaches for recurring task types. New skills go to `~/.hermes/skills/`; existing skills can be modified wherever they live. |
| `skills_list` | List available skills (name + description). Use `skill_view(name)` to load full content. |

## `todo`, `clarify`, `moa`, `vision` toolsets

The remaining single-tool core toolsets — task tracking, user prompting, multi-model routing, and image analysis:

| Tool | Toolset | Description |
|------|---------|-------------|
| `todo` | `todo` | Manage your task list for the current session. Use for complex tasks with 3+ steps or when the user provides multiple tasks. Call with no parameters to read the current list. Provide a `todos` array to create/update items. |
| `clarify` | `clarify` | Ask the user a question when you need clarification, feedback, or a decision before proceeding. Two modes: multiple-choice (up to 4 choices plus an "Other" free-text option) or open-ended. |
| `mixture_of_agents` | `moa` | Route a hard problem through multiple frontier LLMs collaboratively. Makes 5 API calls (4 reference models + 1 aggregator) with maximum reasoning effort — use sparingly for genuinely difficult problems (complex math, advanced algorithms). Requires `OPENROUTER_API_KEY`. |
| `vision_analyze` | `vision` | Analyze images using AI vision. On vision-capable main models, returns the raw image pixels as a multimodal tool result so the model sees them natively on its next turn. On text-only main models, falls back to an auxiliary vision model that describes the image and returns the description as text. Signature is identical either way. |

**Source**: `inbox/hermes_agent_docs/reference/tools-reference.md` · https://hermes-agent.nousresearch.com/docs/reference/tools-reference
**Last Updated**: 2026-06-19
**Status**: Active
