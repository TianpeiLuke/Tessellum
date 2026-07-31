---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - plugins
keywords:
  - plugins option
  - local plugin loading
  - type local path
  - system init plugins
  - plugin skill namespace
  - plugin-name:skill-name
  - verify plugin installation
  - relative vs absolute path
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/plugins
access_control_group: ["general"]
---

# Loading Plugins in the Agent SDK

## Overview

Plugins are packages of Claude Code extensions — **skills**, **agents** (subagents), **hooks**, and **MCP servers** — that can be shared across projects. Through the Agent SDK, you load them programmatically by passing local directory paths to the `plugins` option of `query()`, adding all four extension types to an agent session at once. This note is the SDK-side loading procedure: how to supply plugin paths, verify they loaded, invoke namespaced plugin skills, and troubleshoot. The static directory layout a loadable plugin contains is documented in the sibling note [Plugin Structure Reference](cc_sdk_plugin_structure.md); full plugin authoring lives in the CLI docs ([Plugins](https://code.claude.com/docs/en/plugins), [Plugins reference](https://code.claude.com/docs/en/plugins-reference)).

## What are plugins?

A plugin can include four component types:

- **Skills**: model-invoked capabilities Claude uses autonomously (also invokable with `/skill-name`).
- **Agents**: specialized subagents for specific tasks.
- **Hooks**: event handlers that respond to tool use and other events.
- **MCP servers**: external tool integrations via Model Context Protocol.

The `commands/` directory is a **legacy** format — use `skills/` for new plugins (Claude Code still supports both for backward compatibility).

## Loading plugins

Load plugins by providing their local file system paths in the options configuration. The `type` field **must be `"local"`** — that is the only value the SDK accepts. To use a plugin distributed through a marketplace or remote repository, download it first and pass the local directory path. The SDK supports loading multiple plugins from different locations:

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    async for message in query(
        prompt="Hello",
        options=ClaudeAgentOptions(
            plugins=[
                {"type": "local", "path": "./my-plugin"},
                {"type": "local", "path": "/absolute/path/to/another-plugin"},
            ]
        ),
    ):
        # Plugin commands, agents, and other features are now available
        pass


asyncio.run(main())
```

The TypeScript equivalent passes the same `plugins: [{ type: "local", path: "./my-plugin" }, ...]` array to `query({ options })`.

### Path specifications

Plugin paths can be:

- **Relative paths**: resolved relative to the current working directory (e.g. `"./plugins/my-plugin"`).
- **Absolute paths**: full file system paths (e.g. `"/home/user/plugins/my-plugin"`).

The path must point to the plugin's **root directory** — the parent of `skills/`, `agents/`, `hooks/`, `commands/` (legacy), or `.claude-plugin/` — not a subdirectory.

## Verifying plugin installation

When plugins load successfully they appear in the **system initialization message**. Inspect the `init` message to confirm what loaded:

```python Python theme={null}
async for message in query(
    prompt="Hello",
    options=ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./my-plugin"}]
    ),
):
    if isinstance(message, SystemMessage) and message.subtype == "init":
        # Check loaded plugins
        print("Plugins:", message.data.get("plugins"))
        # Example: [{"name": "my-plugin", "path": "./my-plugin"}]

        # Plugin skills appear with the plugin name as a prefix
        print("Skills:", message.data.get("skills"))
        # Example: ["my-plugin:greet"]

        # Plugin commands use the same prefix, and skills appear here too
        print("Commands:", message.data.get("slash_commands"))
        # Example: ["compact", "context", "my-plugin:custom-command", "my-plugin:greet"]
```

In TypeScript the same fields are `message.plugins`, `message.skills`, and `message.slash_commands` on the `system`/`init` message. Three things confirm a load: the plugin appears in `plugins` (with its `name` and `path`), and its skills/commands appear in `skills` and `slash_commands` with the **plugin-name prefix**.

## Using plugin skills

Skills from plugins are automatically **namespaced with the plugin name** to avoid conflicts. To invoke one directly, send `/plugin-name:skill-name` as the prompt:

```python Python theme={null}
# Load a plugin with a custom /greet skill
async for message in query(
    prompt="/demo-plugin:greet",  # Use plugin skill with namespace
    options=ClaudeAgentOptions(
        plugins=[{"type": "local", "path": "./plugins/demo-plugin"}]
    ),
):
    # Claude executes the custom greeting skill from the plugin
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(f"Claude: {block.text}")
```

If you installed a plugin via the CLI (e.g. `/plugin install my-plugin@marketplace`), you can still use it in the SDK by providing its installation path — check `~/.claude/plugins/` for CLI-installed plugins.

## Complete example

A full flow combines loading, verifying via the `init` message, and reading the assistant response. It builds the plugin path with a path utility (`Path(__file__).parent / "plugins" / "demo-plugin"` in Python, `path.join(__dirname, "plugins", "my-plugin")` in TypeScript), passes it as `plugins=[{"type": "local", "path": str(plugin_path)}]` alongside `max_turns=3`, and prompts `"What custom commands do you have available?"`. On the `SystemMessage`/`init` it prints `plugins`, `skills`, and `slash_commands`; on each `AssistantMessage` it prints the text blocks.

## Common use cases

- **Development and testing** — load plugins during development without installing them globally: `plugins: [{ type: "local", path: "./dev-plugins/my-plugin" }]`.
- **Project-specific extensions** — include plugins in the project repository for team-wide consistency: `plugins: [{ type: "local", path: "./project-plugins/team-workflows" }]`.
- **Multiple plugin sources** — combine plugins from different locations, e.g. a project-local plugin plus a shared one under `~/.claude/custom-plugins/`.

## Troubleshooting

- **Plugin not loading** (does not appear in the init message): (1) check the path points to the plugin **root** directory (parent of `skills/`, `agents/`, `hooks/`, `commands/` (legacy), or `.claude-plugin/`); (2) validate `plugin.json` JSON syntax if the plugin includes a manifest; (3) check the plugin directory is readable (file permissions).
- **Skills not appearing** (plugin skills don't work): (1) invoke as `/plugin-name:skill-name` (use the namespace); (2) check the `init` message — verify the skill appears in `skills` with the correct namespace; (3) validate each skill has a `SKILL.md` in its own subdirectory under `skills/`, e.g. `skills/my-skill/SKILL.md`.
- **Path resolution issues** (relative paths don't work): (1) check the working directory — relative paths resolve from the current working directory; (2) use absolute paths for reliability; (3) use path utilities to construct paths correctly.

**Source**: https://code.claude.com/docs/en/agent-sdk/plugins
**Last Updated**: 2026-06-13
**Status**: Active
