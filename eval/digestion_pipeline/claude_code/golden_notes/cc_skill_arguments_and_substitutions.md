---
tags:
  - resource
  - documentation
  - claude_code
  - skills
  - arguments
keywords:
  - skill string substitution
  - arguments placeholder
  - indexed arguments
  - named arguments
  - claude session id
  - claude effort
  - claude skill dir
  - argument escaping
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

# Claude Code — Skill Arguments and String Substitutions

## Overview

Skills support **string substitution** for dynamic values in the skill content: when you or Claude invoke a skill, Claude Code expands a set of `$`-prefixed placeholders in the rendered `SKILL.md` before Claude sees it. Two related mechanisms are at play — **argument placeholders** (`$ARGUMENTS`, indexed `$ARGUMENTS[N]`/`$N`, and named `$name`) that carry whatever the user or Claude passes when invoking the skill, and **runtime variables** (`${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`) that expose the current session, effort level, and skill directory.

Both you and Claude can pass arguments when invoking a skill. Indexed arguments use shell-style quoting, and a literal `$` before a digit, `ARGUMENTS`, or a declared argument name can be escaped with a backslash. This note documents the available substitutions and how arguments are passed; the frontmatter fields that declare named arguments (`arguments`, `argument-hint`) are detailed in the [skill frontmatter reference](cc_skill_frontmatter_reference.md).

## Available String Substitutions

Skills support string substitution for dynamic values in the skill content:

| Variable | Description |
| :--- | :--- |
| `$ARGUMENTS` | All arguments passed when invoking the skill. If `$ARGUMENTS` is not present in the content, arguments are appended as `ARGUMENTS: <value>`. |
| `$ARGUMENTS[N]` | Access a specific argument by 0-based index, such as `$ARGUMENTS[0]` for the first argument. |
| `$N` | Shorthand for `$ARGUMENTS[N]`, such as `$0` for the first argument or `$1` for the second. |
| `$name` | Named argument declared in the `arguments` frontmatter list. Names map to positions in order, so with `arguments: [issue, branch]` the placeholder `$issue` expands to the first argument and `$branch` to the second. |
| `${CLAUDE_SESSION_ID}` | The current session ID. Useful for logging, creating session-specific files, or correlating skill output with sessions. |
| `${CLAUDE_EFFORT}` | The current effort level: `low`, `medium`, `high`, `xhigh`, or `max`. Ultracode is not a distinct level and reports as `xhigh`. Use this to adapt skill instructions to the active effort setting. |
| `${CLAUDE_SKILL_DIR}` | The directory containing the skill's `SKILL.md` file. For plugin skills, this is the skill's subdirectory within the plugin, not the plugin root. Use this in bash injection commands to reference scripts or files bundled with the skill, regardless of the current working directory. |

### Quoting and escaping

Indexed arguments use shell-style quoting, so wrap multi-word values in quotes to pass them as a single argument. For example, `/my-skill "hello world" second` makes `$0` expand to `hello world` and `$1` to `second`. The `$ARGUMENTS` placeholder always expands to the full argument string as typed.

To include a literal `$` before a digit, `ARGUMENTS`, or a declared argument name, such as `$1.00` in prose, escape it with a backslash: `\$1.00`. A backslash before any other `$` is left unchanged. Only a single backslash directly before the token escapes it. A doubled backslash such as `\\$1` leaves both backslashes in place, and `$1` still expands to the argument value.

### Example using substitutions

This skill mixes a runtime variable (`${CLAUDE_SESSION_ID}`) with the full-argument placeholder (`$ARGUMENTS`):

```yaml
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

## Pass Arguments to Skills

Both you and Claude can pass arguments when invoking a skill. Arguments are available via the `$ARGUMENTS` placeholder. This skill fixes a GitHub issue by number, where `$ARGUMENTS` gets replaced with whatever follows the skill name:

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

When you run `/fix-issue 123`, Claude receives "Fix GitHub issue 123 following our coding standards...". If you invoke a skill with arguments but the skill doesn't include `$ARGUMENTS`, Claude Code appends `ARGUMENTS: <your input>` to the end of the skill content so Claude still sees what you typed.

### Accessing individual arguments by position

To access individual arguments by position, use `$ARGUMENTS[N]` or the shorter `$N`. The following skill migrates a component from one framework to another using the indexed form:

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

Running `/migrate-component SearchBar React Vue` replaces `$ARGUMENTS[0]` with `SearchBar`, `$ARGUMENTS[1]` with `React`, and `$ARGUMENTS[2]` with `Vue`. The same skill can use the `$N` shorthand instead — `$0`, `$1`, and `$2` in place of `$ARGUMENTS[0]`, `$ARGUMENTS[1]`, and `$ARGUMENTS[2]` — and the body becomes "Migrate the `$0` component from `$1` to `$2`."

Named arguments declared in the `arguments` frontmatter give those positions readable names (`$name`); see the [skill frontmatter reference](cc_skill_frontmatter_reference.md) for declaring them. Argument-carrying placeholders also appear inside dynamic-context injection and forked-subagent skills — for example a forked research skill whose body is "Research `$ARGUMENTS` thoroughly" — covered in [skill dynamic context and subagent execution](cc_skill_dynamic_context_and_subagent.md).

**Source**: https://code.claude.com/docs/en/skills
**Last Updated**: 2026-06-13
**Status**: Active
