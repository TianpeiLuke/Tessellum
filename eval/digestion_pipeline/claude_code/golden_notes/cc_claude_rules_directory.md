---
tags:
  - resource
  - documentation
  - claude_code
  - memory
  - rules
keywords:
  - claude rules directory
  - path-specific rules
  - paths frontmatter
  - topic-scoped instructions
  - glob patterns
  - share rules with symlinks
  - user-level rules
  - rule load priority
topics:
  - Claude Code
  - Memory
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/memory
access_control_group: ["general"]
---

# Organize Rules with `.claude/rules/`

## Overview

For larger projects, you can organize instructions into multiple files using the `.claude/rules/` directory instead of one growing CLAUDE.md. Each rule is a topic-scoped markdown file, which keeps instructions modular and easier for teams to maintain. Rules can also be **scoped to specific file paths**, so they load into context only when Claude works with matching files — reducing noise and saving context space.

Like CLAUDE.md, rules are guidance Claude reads, not configuration Claude Code enforces. The page's Note also distinguishes rules from skills: rules load into context **every session** (or when matching files are opened), whereas [skills](https://code.claude.com/docs/en/skills) only load when you invoke them or when Claude determines they're relevant to your prompt. For task-specific instructions that don't need to be in context all the time, use a skill instead.

## Set up rules

Place markdown files in your project's `.claude/rules/` directory. Each file should cover one topic, with a descriptive filename like `testing.md` or `api-design.md`. All `.md` files are discovered recursively, so you can organize rules into subdirectories like `frontend/` or `backend/`:

```text
your-project/
├── .claude/
│   ├── CLAUDE.md           # Main project instructions
│   └── rules/
│       ├── code-style.md   # Code style guidelines
│       ├── testing.md      # Testing conventions
│       └── security.md     # Security requirements
```

Rules without `paths` frontmatter are loaded at launch with the **same priority as `.claude/CLAUDE.md`**.

## Path-specific rules

Rules can be scoped to specific files using YAML frontmatter with the `paths` field. These conditional rules only apply when Claude is working with files matching the specified patterns:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

Rules without a `paths` field are loaded unconditionally and apply to all files. Path-scoped rules trigger when Claude **reads files matching the pattern**, not on every tool use.

Use glob patterns in the `paths` field to match files by extension, directory, or any combination:

| Pattern                | Matches                                  |
| ---------------------- | ---------------------------------------- |
| `**/*.ts`              | All TypeScript files in any directory    |
| `src/**/*`             | All files under `src/` directory         |
| `*.md`                 | Markdown files in the project root       |
| `src/components/*.tsx` | React components in a specific directory |

You can specify multiple patterns and use brace expansion to match multiple extensions in one pattern — for example, listing `"src/**/*.{ts,tsx}"`, `"lib/**/*.ts"`, and `"tests/**/*.test.ts"` together under `paths`.

## Share rules across projects with symlinks

The `.claude/rules/` directory supports symlinks, so you can maintain a shared set of rules and link them into multiple projects. Symlinks are resolved and loaded normally, and **circular symlinks are detected and handled gracefully**.

This example links both a shared directory and an individual file:

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

## User-level rules

Personal rules in `~/.claude/rules/` apply to every project on your machine. Use them for preferences that aren't project-specific, such as a `preferences.md` for your personal coding preferences and a `workflows.md` for your preferred workflows.

User-level rules are **loaded before project rules, giving project rules higher priority**.

**Source**: https://code.claude.com/docs/en/memory
**Last Updated**: 2026-06-13
**Status**: Active
