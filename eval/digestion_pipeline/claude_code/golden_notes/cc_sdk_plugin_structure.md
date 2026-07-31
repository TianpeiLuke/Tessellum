---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - plugins
keywords:
  - plugin structure reference
  - plugin directory layout
  - claude-plugin plugin.json manifest
  - manifest optional auto-discovery
  - plugin component types
  - skills agents hooks mcp
  - legacy commands directory
  - sdk plugin
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/plugins
access_control_group: ["general"]
---

# Claude Agent SDK — Plugin Structure Reference

## Overview

A plugin loadable by the Claude Agent SDK is a **directory on disk** whose contents follow a conventional layout. The directory typically contains a `.claude-plugin/plugin.json` **manifest** file, but the manifest is **optional**: when it is omitted, Claude Code **auto-discovers** the plugin's components from the directory layout. The layout groups a plugin's extensions into four component types — **skills**, **agents**, **hooks**, and **MCP servers** — each living in its own conventional subdirectory or file. This is the static, on-disk shape of the thing the SDK's `plugins` loading option points at; see the sibling loading procedure in [cc_sdk_plugins](cc_sdk_plugins.md).

## Directory layout

A plugin directory can include the following components (only those present are loaded):

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (optional, components auto-discovered without it)
├── skills/                   # Agent Skills (invoked autonomously or via /skill-name)
│   └── my-skill/
│       └── SKILL.md
├── commands/                 # Legacy: use skills/ instead
│   └── custom-cmd.md
├── agents/                   # Custom agents
│   └── specialist.md
├── hooks/                    # Event handlers
│   └── hooks.json
└── .mcp.json                # MCP server definitions
```

The path supplied to the SDK should point to **this root directory** — the parent of `skills/`, `agents/`, `hooks/`, `commands/` (legacy), or `.claude-plugin/` — not a subdirectory.

## The four component types

A plugin packages Claude Code extensions of four kinds, which map onto the layout above:

- **Skills** (`skills/<name>/SKILL.md`) — model-invoked capabilities Claude uses autonomously, also invokable with `/skill-name`. This is the primary, non-legacy component directory; each skill lives in its own subdirectory containing a `SKILL.md` file.
- **Agents** (`agents/`) — specialized subagents for specific tasks.
- **Hooks** (`hooks/hooks.json`) — event handlers that respond to tool use and other events.
- **MCP servers** (`.mcp.json`) — external tool integrations via Model Context Protocol.

The `commands/` directory is a **legacy format**; new plugins should use `skills/` instead. Claude Code continues to support both formats for backward compatibility.

## The optional manifest

The `.claude-plugin/plugin.json` manifest is **optional**. When present, it declares the plugin (its `name` and metadata; the SDK init message reports each loaded plugin as `{ name, path }`). When **omitted**, Claude Code falls back to **auto-discovery**, inferring the plugin's components purely from which conventional directories and files exist. The detailed manifest schema and full plugin-development guide are out of scope here — see the complete plugin development guide at https://code.claude.com/docs/en/plugins and the technical specifications and schemas at https://code.claude.com/docs/en/plugins-reference.

**Source**: https://code.claude.com/docs/en/agent-sdk/plugins
**Last Updated**: 2026-06-13
**Status**: Active
