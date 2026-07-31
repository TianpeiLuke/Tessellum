---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - skills
keywords:
  - sdk skills
  - skills option
  - setting_sources
  - settingSources
  - skill tool
  - allowedTools
  - skill locations
  - filesystem skills
  - skill discovery
  - tool restrictions
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/skills
access_control_group: ["general"]
---

# Loading Agent Skills in the SDK

## Overview

Agent Skills extend Claude with specialized capabilities packaged as `SKILL.md` files (instructions, a `description`, and optional supporting resources) that Claude autonomously invokes when relevant. Unlike subagents, Skills cannot be registered programmatically — the SDK provides no programmatic registration API, so Skills must exist as **filesystem artifacts** under `.claude/skills/`. This note is the SDK-side procedure for discovering those filesystem Skills, enabling them via the `skills` option in `query()`, and controlling their tool access. (For the Skill primitive itself and the full `SKILL.md` authoring guide, see the Claude Code [Skills](https://code.claude.com/docs/en/skills) page.)

## How Skills Work with the SDK

When using the Claude Agent SDK, Skills are:

1. **Defined as filesystem artifacts** — created as `SKILL.md` files in specific directories (`.claude/skills/`).
2. **Loaded from filesystem** — governed by `settingSources` (TypeScript) or `setting_sources` (Python).
3. **Automatically discovered** — once filesystem settings are loaded, Skill *metadata* is discovered at startup from user and project directories; full content is loaded only when triggered.
4. **Model-invoked** — Claude autonomously chooses when to use them based on context.
5. **Filtered via the `skills` option** — discovered skills are enabled by default; pass a list of names, `"all"`, or `[]` to control which are available in the session.

With default `query()` options, the SDK loads user and project sources, so skills in `~/.claude/skills/`, `<cwd>/.claude/skills/`, and `.claude/skills/` in any parent directory of `<cwd>` up to the repository root are available. If you set `settingSources` explicitly, include `'user'` or `'project'` to keep skill discovery, or use the [`plugins` option](cc_sdk_plugins.md) to load skills from a specific path.

## Using Skills with the SDK

Set the `skills` option on `query()` to control which Skills are available. When omitted, discovered Skills are enabled and the Skill tool is available, matching CLI behavior. Pass `"all"` to enable every discovered Skill, a list of names to enable only those, or `[]` to disable all. When you set `skills`, the SDK adds the **Skill** tool to `allowedTools` automatically. If you also pass an explicit `tools` list, include `"Skill"` so Claude can invoke skills.

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    options = ClaudeAgentOptions(
        cwd="/path/to/project",  # Project with .claude/skills/
        setting_sources=["user", "project"],  # Load Skills from filesystem
        skills="all",  # Enable every discovered Skill
        allowed_tools=["Read", "Write", "Bash"],
    )

    async for message in query(
        prompt="Help me process this PDF document", options=options
    ):
        print(message)


asyncio.run(main())
```

To enable only specific Skills, pass their names — names match the `name` field in `SKILL.md` or the Skill's directory name (use `plugin:skill` for plugin-provided Skills):

```python Python theme={null}
options = ClaudeAgentOptions(skills=["pdf", "docx"])
```

The `skills` option **is a context filter, not a sandbox**. Unlisted Skills are hidden from the model and rejected by the Skill tool, but their files remain on disk and are reachable through Read and Bash.

## Skill Locations

Skills load from filesystem directories based on the `settingSources`/`setting_sources` configuration:

- **Project Skills** (`.claude/skills/`) — shared with your team via git; loaded when `setting_sources` includes `"project"`.
- **User Skills** (`~/.claude/skills/`) — personal Skills across all projects; loaded when `setting_sources` includes `"user"`.
- **Plugin Skills** — bundled with installed Claude Code plugins.

## Creating Skills

Skills are directories containing a `SKILL.md` file with YAML frontmatter and Markdown content; the `description` field determines when Claude invokes the Skill. Example directory structure:

```bash theme={null}
.claude/skills/processing-pdfs/
└── SKILL.md
```

Full `SKILL.md` structure, multi-file Skills, and examples are covered in the [Agent Skills in Claude Code](https://code.claude.com/docs/en/skills) guide.

## Tool Restrictions

The `allowed-tools` frontmatter field in `SKILL.md` is **only supported when using the Claude Code CLI directly — it does not apply when using Skills through the SDK**. In SDK applications, control tool access through the main `allowedTools` option; without a `canUseTool` callback, anything not in the list is denied:

```python Python theme={null}
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # Load Skills from filesystem
    skills="all",
    allowed_tools=["Read", "Grep", "Glob"],
)

async for message in query(prompt="Analyze the codebase structure", options=options):
    print(message)
```

The TypeScript equivalent adds `permissionMode: "dontAsk"` to deny anything not in `allowedTools`.

## Discovering and Testing Skills

To see which Skills are available, simply ask Claude (e.g. prompt `"What Skills are available?"` with `setting_sources=["user", "project"]` and `skills="all"`); Claude lists the Skills based on the current working directory and installed plugins. To **test** a Skill, ask a question that matches its `description` (e.g. `"Extract text from invoice.pdf"`) — Claude automatically invokes the relevant Skill when the description matches the request.

## Troubleshooting

- **Skills Not Found** — Skills are discovered through the `user` and `project` setting sources. Setting `setting_sources=[]` excludes them (Skills not loaded); use `setting_sources=["user", "project"]` to load them. Also confirm `cwd` points at or below the directory containing `.claude/skills/`, within the same repository. Verify the filesystem location with `ls .claude/skills/*/SKILL.md` (project) or `ls ~/.claude/skills/*/SKILL.md` (personal).
- **Skill Not Being Used** — if you passed a `skills` list, confirm the skill's name is included (`[]` disables all); ensure the `description` is specific and includes relevant keywords.
- **Additional** — for general Skills troubleshooting (YAML syntax, debugging), see the [Claude Code Skills troubleshooting section](https://code.claude.com/docs/en/skills#troubleshooting).

**Source**: https://code.claude.com/docs/en/agent-sdk/skills
**Last Updated**: 2026-06-13
**Status**: Active
