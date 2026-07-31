---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - capabilities
keywords:
  - openclaw tools skills plugins
  - capabilities routing page
  - built-in tool categories
  - api.registerTool contracts.tools
  - tool policy allow deny profile
  - tool search experimental
  - exec approvals elevated sandbox
  - missing tools troubleshooting
topics:
  - OpenClaw
  - Tools and Capabilities
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/tools
access_control_group: ["general"]
---

# OpenClaw — Tools, Skills, and Plugins Capabilities Overview

## Overview

This note captures the OpenClaw **Capabilities** routing page (`tools` source slug): the conceptual framework an operator uses to decide between **tools** (callable typed actions), **skills** (`SKILL.md` instruction packs), and **plugins** (runtime capabilities). It mirrors the source page's decision framework, the built-in tool-category table, plugin-provided tools and `api.registerTool`, how tool policy is enforced before the model call, the extension paths, and the missing-tool troubleshooting checklist. This is an overview and routing page; for the exhaustive tool policy, defaults, group membership, provider restrictions, and configuration fields, the source defers to the canonical *Tools and custom providers* reference (`/gateway/config-tools`).

## Start Here — the Routing Table

The page's purpose is to pick the right Capabilities surface, then adjust policy only when the agent should see fewer tools or needs explicit host access. For most agents, start with the built-in tool categories first. The page provides a "If you need to…" routing table that maps an intent to the surface to use first and what to read next:

| If you need to... | Use this first | Then read |
|---|---|---|
| Let an agent act with existing capabilities | Built-in tools | Tool categories |
| Control what an agent can call | Tool policy | Tools and custom providers (`/gateway/config-tools`) |
| Teach an agent a workflow | Skills | Skills (`/tools/skills`), Creating skills, Skill Workshop |
| Add a new integration or runtime surface | Plugins | Plugins (`/tools/plugin`), Build plugins |
| Run work later or in the background | Automation (`/automation`) | Automation overview |
| Coordinate multiple agents or harnesses | Sub-agents (`/tools/subagents`) | ACP agents, Agent send |
| Search a large OpenClaw tool catalog | Tool Search (`/tools/tool-search`) | Tool Search |

## Choose Tools, Skills, or Plugins

The page frames the choice as three distinct surfaces with non-overlapping jobs.

- **Use a tool when the agent needs to act.** A tool is a typed function the agent can call, such as `exec`, `browser`, `web_search`, `message`, or `image_generate`. Use tools when the agent needs to read data, change files, send messages, call a provider, or operate another system. Visible tools are sent to the model as structured function definitions. The model only sees tools that survive the active profile, allow/deny policy, provider restrictions, sandbox state, channel permissions, and plugin availability.
- **Use a skill when the agent needs instructions.** A skill is a `SKILL.md` instruction pack loaded into the agent prompt. Use a skill when the agent already has the tools it needs but needs a repeatable workflow, review rubric, command sequence, or operating constraint. Skills can live in a workspace, a shared skill directory, a managed OpenClaw skill root, or a plugin package.
- **Use a plugin when OpenClaw needs a new capability.** A plugin can add tools, skills, channels, model providers, speech, realtime voice, media generation, web search, web fetch, hooks, and other runtime capabilities. Use a plugin when the capability has code, credentials, lifecycle hooks, manifest metadata, or installable packaging. Existing plugins can be installed from ClawHub, npm, git, local directories, or archives.

## Built-in Tool Categories

The source lists representative tools so a reader can recognize each surface; it is explicitly **not** the full policy reference. For exact groups, defaults, and allow/deny semantics, the page points to *Tools and custom providers* (`/gateway/config-tools`). The ten built-in categories and their representative tools, verbatim from source:

| Category | Use when the agent needs to... | Representative tools |
|---|---|---|
| Runtime | Run commands, manage processes, or use provider-backed Python analysis | `exec`, `process`, `code_execution` |
| Files | Read and change workspace files | `read`, `write`, `edit`, `apply_patch` |
| Web | Search the web, search X posts, or fetch readable page content | `web_search`, `x_search`, `web_fetch` |
| Browser | Operate a browser session | `browser` |
| Messaging and channels | Send replies or channel actions | `message` |
| Sessions and agents | Inspect sessions, delegate work, steer another run, or report status | `sessions_*`, `subagents`, `agents_list`, `session_status`, `goal` |
| Automation | Schedule work or respond to background events | `cron`, `heartbeat_respond` |
| Gateway and nodes | Inspect Gateway state or paired target devices | `gateway`, `nodes` |
| Media | Analyze, generate, or speak media | `image`, `image_generate`, `music_generate`, `video_generate`, `tts` |
| Large OpenClaw catalogs | Search and call many eligible tools without sending every schema to the model | `tool_search_code`, `tool_search`, `tool_describe` |

A source note flags that **Tool Search is an experimental OpenClaw agent surface**: Codex harness runs use Codex-native code mode, native tool search, deferred dynamic tools, and nested tool calls instead of `tools.toolSearch`.

## Plugin-Provided Tools

Plugins can register additional tools. Plugin authors wire tools through `api.registerTool(...)` and the manifest's `contracts.tools`; the page directs authors to the *Plugin SDK* (`/plugins/sdk-overview`) and *Plugin manifest* (`/plugins/manifest`) for contract details. Common plugin-provided tools the page lists are: **Diffs** for rendering file and markdown diffs; **LLM Task** for JSON-only workflow steps; **Lobster** for typed workflows with resumable approvals; **Tokenjuice** for compacting noisy `exec` and `bash` tool output; **Tool Search** for discovering and calling large tool catalogs without putting every schema in the prompt; and **Canvas** for node Canvas control and A2UI rendering.

## Configure Access and Approvals

The page states the central policy invariant: **tool policy is enforced before the model call.** If policy removes a tool, the model does not receive that tool's schema for the turn. A run can lose tools because of global config, per-agent config, channel policy, provider restrictions, sandbox rules, channel/runtime policy, or plugin availability. The page routes the policy detail to dedicated references:

- *Tools and custom providers* (`/gateway/config-tools`) documents tool profiles, allow/deny lists, provider-specific restrictions, loop detection, and provider-backed tool settings.
- *Exec approvals* (`/tools/exec-approvals`) documents host command approval policy.
- *Elevated exec* (`/tools/elevated`) documents controlled execution outside the sandbox.
- *Sandbox vs tool policy vs elevated* (`/gateway/sandbox-vs-tool-policy-vs-elevated`) explains which layer controls file and process access.
- *Per-agent sandbox and tool restrictions* (`/tools/multi-agent-sandbox-tools`) documents agent-specific restrictions for delegated runs.

## Extend Capabilities

The page advises choosing the extension path by the job OpenClaw must do: install or manage an existing plugin with *Plugins* (`/tools/plugin`); build a new integration, provider, channel, tool, or hook with *Build plugins* (`/plugins/building-plugins`); add or tune reusable agent instructions with *Skills* (`/tools/skills`) and *Creating skills* (`/tools/creating-skills`); and use the *Plugin SDK* (`/plugins/sdk-overview`) and *Plugin manifest* (`/plugins/manifest`) when implementation contracts are needed.

## Troubleshoot Missing Tools

If the model cannot see or call a tool, the page prescribes starting with the **effective policy for the current turn** and walking a six-step checklist (verbatim from source):

1. Check the active profile, `tools.allow`, and `tools.deny` in *Tools and custom providers*.
2. Check provider-specific restrictions in *Tools and custom providers* and confirm the selected model provider supports the tool shape.
3. Check channel permissions, sandbox state, and elevated access with *Sandbox vs tool policy vs elevated* and *Elevated exec*.
4. Check whether the owning plugin is installed and enabled in *Plugins*.
5. For delegated runs, check per-agent restrictions in *Per-agent sandbox and tool restrictions*.
6. For large OpenClaw catalogs, confirm whether the run uses direct tool exposure or *Tool Search*.

**Source**: OpenClaw documentation — `tools` (mirror `inbox/openclaw_docs/tools.md`)
**Last Updated**: 2026-06-22
**Status**: Active
