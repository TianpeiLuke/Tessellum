---
tags:
  - resource
  - documentation
  - claude_code
  - memory
  - claude_md
keywords:
  - claude.md files
  - persistent instructions
  - claude.md scopes load order
  - write effective instructions
  - import additional files
  - claude.local.md
  - agents.md
  - how claude.md files load
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

# Claude Code — CLAUDE.md Files

## Overview

`CLAUDE.md` files are markdown files that give Claude persistent instructions for a project, your personal workflow, or your entire organization. You write these files in plain text, and Claude reads them at the start of every session. They are Claude Code's primary author-written memory mechanism (the complementary system being [auto memory](cc_auto_memory.md), which Claude writes itself).

This note covers what belongs in a CLAUDE.md, the four scopes/locations it can live in (in load order), how to write instructions Claude follows reliably, the `@path` import syntax and `CLAUDE.local.md`, the `AGENTS.md` interop pattern, and the directory-walk loading mechanics. For topic-scoped modular instructions see [`.claude/rules/`](cc_claude_rules_directory.md); for organization-wide deployment see [managing CLAUDE.md for large teams](cc_manage_claude_md_for_teams.md).

## When to add to CLAUDE.md

Treat CLAUDE.md as the place you write down what you'd otherwise re-explain. Add to it when:

* Claude makes the same mistake a second time
* A code review catches something Claude should have known about this codebase
* You type the same correction or clarification into chat that you typed last session
* A new teammate would need the same context to be productive

Keep it to facts Claude should hold in every session: build commands, conventions, project layout, "always do X" rules. If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a [skill](https://code.claude.com/docs/en/skills) or a [path-scoped rule](cc_claude_rules_directory.md) instead.

## Choose where to put CLAUDE.md files

CLAUDE.md files can live in several locations, each with a different scope. They load from broadest scope to most specific, so a project instruction appears in context after a user instruction.

| Scope | Location | Purpose | Shared with |
| --- | --- | --- | --- |
| **Managed policy** | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux/WSL: `/etc/claude-code/CLAUDE.md`; Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Organization-wide instructions managed by IT/DevOps | All users in organization |
| **User instructions** | `~/.claude/CLAUDE.md` | Personal preferences for all projects | Just you (all projects) |
| **Project instructions** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions for the project | Team members via source control |
| **Local instructions** | `./CLAUDE.local.md` | Personal project-specific preferences; add to `.gitignore` | Just you (current project) |

CLAUDE.md and CLAUDE.local.md files in the directory hierarchy above the working directory are loaded in full at launch. Files in subdirectories load on demand when Claude reads files in those directories. For large projects, break instructions into topic-specific files using [project rules](cc_claude_rules_directory.md).

## Set up a project CLAUDE.md

A project CLAUDE.md can be stored in either `./CLAUDE.md` or `./.claude/CLAUDE.md`. Add instructions that apply to anyone working on the project: build and test commands, coding standards, architectural decisions, naming conventions, and common workflows. These are shared with your team through version control, so focus on project-level standards rather than personal preferences.

Run `/init` to generate a starting CLAUDE.md automatically — Claude analyzes your codebase and creates a file with build commands, test instructions, and project conventions it discovers. If a CLAUDE.md already exists, `/init` suggests improvements rather than overwriting it. Setting `CLAUDE_CODE_NEW_INIT=1` enables an interactive multi-phase flow that asks which artifacts to set up (CLAUDE.md, skills, hooks), explores the codebase with a subagent, and presents a reviewable proposal before writing any files.

## Write effective instructions

CLAUDE.md files are loaded into the context window at the start of every session, consuming tokens alongside your conversation. Because they are context rather than enforced configuration, how you write instructions affects how reliably Claude follows them. Specific, concise, well-structured instructions work best.

* **Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence. If instructions are growing large, use [path-scoped rules](cc_claude_rules_directory.md) so they load only when Claude works with matching files. Splitting content into imports helps organization, but imported files still load and enter the context window at launch.
* **Structure**: use markdown headers and bullets to group related instructions. Organized sections are easier for Claude to follow than dense paragraphs.
* **Specificity**: write instructions concrete enough to verify — e.g., "Use 2-space indentation" instead of "Format code properly"; "Run `npm test` before committing" instead of "Test your changes"; "API handlers live in `src/api/handlers/`" instead of "Keep files organized."
* **Consistency**: if two rules contradict each other, Claude may pick one arbitrarily. Periodically review CLAUDE.md files, nested CLAUDE.md files in subdirectories, and `.claude/rules/` to remove outdated or conflicting instructions. In monorepos, use `claudeMdExcludes` to skip other teams' CLAUDE.md files (see [managing CLAUDE.md for large teams](cc_manage_claude_md_for_teams.md)).

## Import additional files

CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them. Both relative and absolute paths are allowed; relative paths resolve relative to the file containing the import, not the working directory. Imported files can recursively import other files, with a maximum depth of four hops.

```text
See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

For private per-project preferences that shouldn't be checked into version control, create a `CLAUDE.local.md` at the project root. It loads alongside `CLAUDE.md` and is treated the same way. Add `CLAUDE.local.md` to your `.gitignore` so it isn't committed; running `/init` and choosing the personal option does this for you.

If you work across multiple git worktrees of the same repository, a gitignored `CLAUDE.local.md` only exists in the worktree where you created it. To share personal instructions across worktrees, import a file from your home directory instead:

```text
# Individual Preferences
- @~/.claude/my-project-instructions.md
```

The first time Claude Code encounters external imports in a project, it shows an approval dialog listing the files. If you decline, the imports stay disabled and the dialog does not appear again.

## AGENTS.md

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If your repository already uses `AGENTS.md` for other coding agents, create a `CLAUDE.md` that imports it so both tools read the same instructions without duplicating them. You can add Claude-specific instructions below the import — Claude loads the imported file at session start, then appends the rest:

```markdown
@AGENTS.md

## Claude Code

Use plan mode for changes under `src/billing/`.
```

A symlink also works if you don't need to add Claude-specific content (`ln -s AGENTS.md CLAUDE.md`). On Windows, creating a symlink requires Administrator privileges or Developer Mode, so use the `@AGENTS.md` import instead. Running `/init` in a repo that already has an `AGENTS.md` reads it and incorporates the relevant parts into the generated `CLAUDE.md`; it also reads other tool configs like `.cursorrules`, `.devin/rules/`, and `.windsurfrules`.

## How CLAUDE.md files load

Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory, checking each directory for `CLAUDE.md` and `CLAUDE.local.md` files. Running Claude Code in `foo/bar/` loads instructions from `foo/bar/CLAUDE.md`, `foo/CLAUDE.md`, and any `CLAUDE.local.md` files alongside them.

All discovered files are concatenated into context rather than overriding each other. Across the directory tree, content is ordered from the filesystem root down to your working directory — for `foo/bar/`, `foo/CLAUDE.md` appears before `foo/bar/CLAUDE.md`, so instructions closer to where you launched Claude are read last. Within each directory, `CLAUDE.local.md` is appended after `CLAUDE.md`, so your personal notes are the last thing Claude reads at that level.

Claude also discovers `CLAUDE.md` and `CLAUDE.local.md` files in subdirectories under your current working directory. Instead of loading them at launch, they are included when Claude reads files in those subdirectories.

Block-level HTML comments (`<!-- maintainer notes -->`) in CLAUDE.md files are stripped before the content is injected into Claude's context — use them to leave notes for human maintainers without spending context tokens. Comments inside code blocks are preserved, and when you open a CLAUDE.md file directly with the Read tool, comments remain visible.

**Load from additional directories**: the `--add-dir` flag gives Claude access to directories outside your main working directory, but by default their CLAUDE.md files are not loaded. To also load memory files from those directories, set the `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` environment variable. This loads `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`, and `CLAUDE.local.md` from the additional directory (`CLAUDE.local.md` is skipped if you exclude `local` from `--setting-sources`).

**Source**: https://code.claude.com/docs/en/memory
**Last Updated**: 2026-06-13
**Status**: Active
