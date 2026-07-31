---
tags:
  - resource
  - documentation
  - claude_code
  - skills
keywords:
  - skill
  - skill.md
  - agent skills standard
  - custom commands merged into skills
  - where skills live
  - skill precedence
  - live change detection
  - automatic skill discovery
  - additional directories
topics:
  - Claude Code
  - Skills
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/skills
access_control_group: ["general"]
---

# Claude Code — Skills Overview

## Overview

A **skill** is how you extend what Claude can do in Claude Code: you create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses a skill when relevant, or you can invoke one directly with `/skill-name`. A `SKILL.md` has two parts — **YAML frontmatter** that tells Claude when to use the skill, and **markdown content** with the instructions Claude follows when the skill runs. The defining trade-off versus CLAUDE.md is lazy loading: a skill's body loads only when it is used, so long reference material costs almost nothing until you need it, whereas CLAUDE.md content is always in context.

You create a skill when you keep pasting the same instructions, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact. This note covers what a skill is, the merge of custom commands into skills, the Agent Skills open standard, the four storage levels and their precedence, live change detection, automatic discovery from parent/nested directories, and skills loaded from additional directories.

## Custom Commands Merged Into Skills

Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Existing `.claude/commands/` files keep working. Skills add optional features that commands lack: a directory for supporting files, frontmatter to control whether you or Claude invokes them, and the ability for Claude to load them automatically when relevant. Skills are recommended over `.claude/commands/` files since they support these additional features.

For built-in commands like `/help` and `/compact`, and bundled prompt-based skills like `/debug` and `/code-review`, see the commands reference ([cc_commands_reference.md](cc_commands_reference.md)) and [cc_bundled_skills.md](cc_bundled_skills.md).

## Agent Skills Open Standard

Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard, which works across multiple AI tools. Claude Code extends the standard with additional features:

- **Invocation control** — restricting whether you, Claude, or both can trigger a skill (see [cc_skill_invocation_and_lifecycle.md](cc_skill_invocation_and_lifecycle.md)).
- **Subagent execution** — running a skill in a forked context (see [cc_skill_dynamic_context_and_subagent.md](cc_skill_dynamic_context_and_subagent.md)).
- **Dynamic context injection** — running shell commands to inline live data before Claude sees the skill (see [cc_skill_dynamic_context_and_subagent.md](cc_skill_dynamic_context_and_subagent.md)).

## Where Skills Live

Where you store a skill determines who can use it:

| Location   | Path                                                | Applies to                     |
| :--------- | :-------------------------------------------------- | :----------------------------- |
| Enterprise | See managed settings                                | All users in your organization |
| Personal   | `~/.claude/skills/<skill-name>/SKILL.md`            | All your projects              |
| Project    | `.claude/skills/<skill-name>/SKILL.md`              | This project only              |
| Plugin     | `<plugin>/skills/<skill-name>/SKILL.md`             | Where plugin is enabled        |

When skills share the same name across levels, **enterprise overrides personal, and personal overrides project**. Plugin skills use a `plugin-name:skill-name` namespace, so they cannot conflict with other levels. If you have files in `.claude/commands/`, those work the same way, but if a skill and a command share the same name, the skill takes precedence.

Adding a `.claude-plugin/plugin.json` to a skill folder loads it as a plugin named `<name>@skills-dir`, so it can bundle agents, hooks, and MCP servers; in a project's `.claude/skills/`, this requires accepting the workspace trust dialog first. Skills can also be distributed at different scopes by audience: **project skills** (commit `.claude/skills/` to version control), **plugins** (a `skills/` directory in your plugin), or **managed** (deploy organization-wide through managed settings, see https://code.claude.com/docs/en/settings).

## Live Change Detection

Claude Code watches skill directories for file changes. Adding, editing, or removing a skill under `~/.claude/skills/`, the project `.claude/skills/`, or a `.claude/skills/` inside an `--add-dir` directory takes effect **within the current session without restarting**. Creating a top-level skills directory that did not exist when the session started requires restarting Claude Code so the new directory can be watched.

Live change detection covers `SKILL.md` text only. For a skill folder that is also a plugin, changes to `hooks/`, `.mcp.json`, `agents/`, and `output-styles/` need `/reload-plugins` to take effect.

## Automatic Discovery From Parent and Nested Directories

Project skills load from `.claude/skills/` in your starting directory and in **every parent directory up to the repository root**, so starting Claude in a subdirectory still picks up skills defined at the root. When you work with files in subdirectories below your starting directory, Claude Code also discovers skills from **nested** `.claude/skills/` directories on demand. For example, editing a file in `packages/frontend/` makes Claude Code also look for skills in `packages/frontend/.claude/skills/`. This supports monorepo setups where packages have their own skills.

Each skill is a directory with `SKILL.md` as the required entrypoint:

```text
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

The `SKILL.md` contains the main instructions and is required. Other files are optional and let you build more powerful skills (templates, example outputs, scripts, or reference docs). Reference these files from your `SKILL.md` so Claude knows what they contain and when to load them (see [cc_create_a_skill.md](cc_create_a_skill.md)).

## Skills From Additional Directories

The `--add-dir` flag and `/add-dir` command grant file access rather than configuration discovery, but skills are an exception: `.claude/skills/` within an added directory is loaded automatically. **This exception applies only to `--add-dir` and `/add-dir`.** The `permissions.additionalDirectories` setting in `settings.json` grants file access only and does not load skills.

Other `.claude/` configuration such as subagents, commands, and output styles is **not** loaded from additional directories. CLAUDE.md files from `--add-dir` directories are also not loaded by default; to load them, set `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. For the complete list of what is and isn't loaded and recommended ways to share configuration, see https://code.claude.com/docs/en/permissions.

**Source**: https://code.claude.com/docs/en/skills
**Last Updated**: 2026-06-13
**Status**: Active
