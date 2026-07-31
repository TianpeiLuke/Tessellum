---
tags:
  - resource
  - documentation
  - claude_code
  - skills
  - frontmatter
keywords:
  - skill frontmatter reference
  - skill.md yaml fields
  - reference vs task content
  - description and when_to_use
  - 1536 character cap
  - command name derivation
  - allowed-tools disallowed-tools
  - context fork agent
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

# Claude Code — Skill Frontmatter Reference

## Overview

A Claude Code skill is configured through **YAML frontmatter** at the top of its `SKILL.md` file (between `---` markers) plus the markdown content that follows. All frontmatter fields are optional; only `description` is recommended so Claude knows when to apply the skill. This note is the field-by-field reference for that frontmatter: the two broad content types (reference vs task), every configurable field, and how the command you type to invoke a skill is derived from where the file lives rather than from the `name` field.

The frontmatter is where a skill declares its identity (`name`, `description`, `when_to_use`), its invocation controls (`disable-model-invocation`, `user-invocable`), its tool and model behavior (`allowed-tools`, `disallowed-tools`, `model`, `effort`), and its execution shape (`context`, `agent`, `hooks`, `paths`, `shell`). A minimal example:

```yaml
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read Grep
---

Your skill instructions here...
```

## Types of Skill Content

Skill files can contain any instructions, but thinking about how you want to invoke a skill helps guide what to include. The source distinguishes two broad shapes:

- **Reference content** adds knowledge Claude applies to your current work — conventions, patterns, style guides, domain knowledge. This content runs inline so Claude can use it alongside your conversation context (for example, an `api-conventions` skill that lists RESTful naming rules and consistent error formats).
- **Task content** gives Claude step-by-step instructions for a specific action, like deployments, commits, or code generation. These are often actions you want to invoke directly with `/skill-name` rather than letting Claude decide when to run them; add `disable-model-invocation: true` to prevent Claude from triggering them automatically. A task skill commonly also sets `context: fork` to run in isolation.

Beyond choosing reference vs task, two further decisions guide the content: how you want the skill invoked (by you, by Claude, or both) and where you want it to run (inline or in a subagent). For complex skills, you can move detail into supporting files to keep the main skill focused.

Keep the body concise. Once a skill loads, its content stays in context across turns, so every line is a recurring token cost. State what to do rather than narrating how or why, applying the same conciseness test used for CLAUDE.md content.

## Frontmatter Reference

The full set of frontmatter fields. All are optional; `description` is recommended.

| Field | Required | Description |
| :-- | :-- | :-- |
| `name` | No | Display name shown in skill listings. Defaults to the directory name. Differs from the name you type to invoke the skill (see command-name derivation below). |
| `description` | Recommended | What the skill does and when to use it. Claude uses this to decide when to apply the skill. If omitted, uses the first paragraph of markdown content. Put the key use case first: the combined `description` and `when_to_use` text is truncated at **1,536 characters** in the skill listing to reduce context usage. |
| `when_to_use` | No | Additional context for when Claude should invoke the skill, such as trigger phrases or example requests. Appended to `description` in the listing and counts toward the 1,536-character cap. |
| `argument-hint` | No | Hint shown during autocomplete to indicate expected arguments. Example: `[issue-number]` or `[filename] [format]`. |
| `arguments` | No | Named positional arguments for `$name` substitution in the skill content. Accepts a space-separated string or a YAML list. Names map to argument positions in order. |
| `disable-model-invocation` | No | Set to `true` to prevent Claude from automatically loading this skill. Use for workflows you trigger manually with `/name`. Also prevents the skill from being preloaded into subagents. Default: `false`. |
| `user-invocable` | No | Set to `false` to hide from the `/` menu. Use for background knowledge users shouldn't invoke directly. Default: `true`. |
| `allowed-tools` | No | Tools Claude can use without asking permission when this skill is active. Accepts a space- or comma-separated string, or a YAML list. |
| `disallowed-tools` | No | Tools removed from Claude's available pool while this skill is active. Use for autonomous skills that should never call certain tools (such as `AskUserQuestion` for a background loop). Accepts a space- or comma-separated string, or a YAML list. The restriction clears when you send your next message. |
| `model` | No | Model to use when this skill is active. The override applies for the rest of the current turn and is not saved to settings; the session model resumes on your next prompt. Accepts the same values as `/model`, or `inherit` to keep the active model. |
| `effort` | No | Effort level when this skill is active. Overrides the session effort level. Default: inherits from session. Options: `low`, `medium`, `high`, `xhigh`, `max`; available levels depend on the model. |
| `context` | No | Set to `fork` to run in a forked subagent context. |
| `agent` | No | Which subagent type to use when `context: fork` is set. |
| `hooks` | No | Hooks scoped to this skill's lifecycle. |
| `paths` | No | Glob patterns that limit when this skill is activated. Accepts a comma-separated string or a YAML list. When set, Claude loads the skill automatically only when working with files matching the patterns. Uses the same format as path-specific memory rules. |
| `shell` | No | Shell to use for `` !`command` `` and ` ```! ` blocks in this skill. Accepts `bash` (default) or `powershell`. Setting `powershell` runs inline shell commands via PowerShell on Windows. Requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. |

The 1,536-character cap on `description` + `when_to_use` matters because skill descriptions are loaded into context so Claude knows what is available. When you have many skills, descriptions are shortened to fit the listing's character budget (which scales at 1% of the model's context window), and when it overflows the keywords Claude needs to match a request can be stripped. Putting the key use case first keeps the most matchable text inside the cap. The cap itself is configurable with the `maxSkillDescriptionChars` setting.

> Several fields route to areas owned by other sub-plans and are linked rather than duplicated here: the `model`/`effort` values are documented under [model configuration](https://code.claude.com/docs/en/model-config); `hooks` format under [hooks](https://code.claude.com/docs/en/hooks); `paths` format under [memory](https://code.claude.com/docs/en/memory); and the `skillListingBudgetFraction`/`maxSkillDescriptionChars` settings under [settings](https://code.claude.com/docs/en/settings).

## How a Skill Gets Its Command Name

The command you type to invoke a skill comes from **where the skill file lives**, not from the `name` field. The frontmatter `name` field sets the display label shown in skill listings and — except for a plugin-root `SKILL.md` — does not change what you type after `/`.

| Skill location | Command name source | Example |
| :-- | :-- | :-- |
| Skill directory under `~/.claude/skills/` or `.claude/skills/` | Directory name | `.claude/skills/deploy-staging/SKILL.md` → `/deploy-staging` |
| File under `.claude/commands/` | File name without extension | `.claude/commands/deploy.md` → `/deploy` |
| Plugin `skills/` subdirectory | Directory name, namespaced by plugin | `my-plugin/skills/review/SKILL.md` → `/my-plugin:review` |
| Plugin root `SKILL.md` | Frontmatter `name`, with the plugin directory name as a fallback | `my-plugin/SKILL.md` with `name: review` → `/my-plugin:review` |

The plugin-root case is the one place where `name` does set the command name, because there is no skill directory to take it from. If `name` is not set in the plugin-root frontmatter, the plugin's directory name is used instead.

**Source**: https://code.claude.com/docs/en/skills
**Last Updated**: 2026-06-13
**Status**: Active
