---
tags:
  - resource
  - documentation
  - claude_code
  - large_codebases
  - strategy
keywords:
  - large codebase strategy
  - monorepo configuration
  - context window degradation
  - layered independent settings
  - where to start claude
  - root vs subdirectory launch
  - cross-package change sequencing
  - save plan to file
topics:
  - Claude Code
  - Large Codebases
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/large-codebases
access_control_group: ["general"]
---

# Claude Code in a Large Codebase — Strategy and Where to Start

## Overview

A large codebase can be one repository with millions of lines or a monorepo with many packages. Claude Code works at any size, but as a codebase grows, **the defaults tuned for smaller projects fill the context window with instructions and file reads unrelated to the task**, costing tokens and degrading Claude's performance. The strategic response is to **scope Claude to the part of the codebase a task touches**.

This note is the strategic overview: the argument for *why* the configuration matters, the **layering principle** that ties the individual settings together, the **root-vs-subdirectory launch** trade-off that determines where settings files live, and how to **scope and sequence a change that spans packages**. The concrete per-setting mechanics live in the sibling notes — [CLAUDE.md layering](cc_large_codebase_claude_md_layering.md), [reducing reads and worktrees](cc_large_codebase_reduce_reads_and_worktrees.md), and [skills and plugins](cc_large_codebase_skills_and_plugins.md).

## Why Defaults Degrade at Scale

Two distinct costs grow with the codebase, and both consume context:

- **Instructions**: a single root CLAUDE.md tends to grow to cover every subsystem's conventions, spending context on instructions unrelated to the current task — or it stays too generic to be useful.
- **File reads**: file reads are another cost that grows with the codebase; finding where a symbol is defined or used can cost many file reads and grep calls.

The guide addresses individual developers and engineering teams, and each setting notes whether it is **personal to your machine** or **committed to the repository** so a team can share a baseline while individuals add overrides.

## The Layering Principle

Each setting the guide describes is **independent**. The settings **layer rather than replace each other**, so you apply whichever fit your repository rather than adopting all of them at once. The settings table summarizes the menu — each row maps a goal to the mechanism that achieves it:

| I want to | Use |
| :--- | :--- |
| Load only the conventions for the code you touch, instead of one root file covering every subsystem | Per-directory CLAUDE.md files |
| Exclude CLAUDE.md files for packages you never work in | `claudeMdExcludes` |
| Block Claude from opening build output, generated code, and vendored dependencies | `Read` deny rules in `permissions.deny` |
| Find a symbol's definition or callers through the language server instead of scanning files | A code intelligence plugin |
| Check out only the directories a task needs when Claude creates a worktree | `worktree.sparsePaths` |
| Read and edit a sibling package or another repository from the same session | `--add-dir` or `additionalDirectories` |
| Give Claude procedures specific to one area that load only when relevant | Per-directory skills |
| Replace many per-directory CLAUDE.md files with one set of conventions everyone installs | A plugin in an internal marketplace |

The first four rows are detailed in [CLAUDE.md layering](cc_large_codebase_claude_md_layering.md) and [reducing reads and worktrees](cc_large_codebase_reduce_reads_and_worktrees.md); the worktree/access rows in [reducing reads and worktrees](cc_large_codebase_reduce_reads_and_worktrees.md); the skills/plugin rows in [skills and plugins](cc_large_codebase_skills_and_plugins.md). For workflow techniques that keep context small in any repository — such as running exploration in a subagent so file reads stay out of the main conversation — see [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices). For organization-wide rollout, see [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup).

### The Example Monorepo

Every code sample across the large-codebase pages refers to one example monorepo with three packages. The same patterns work in a large single-tree codebase: where an example uses `packages/api/`, substitute your own subsystem directory such as `src/backend/` or `lib/core/`.

```text
monorepo/
  CLAUDE.md                     # root instructions
  packages/
    api/
      CLAUDE.md                 # API-specific instructions
      .claude/skills/
      src/
    web/
      CLAUDE.md                 # frontend-specific instructions
      .claude/skills/
      src/
    shared/
      CLAUDE.md                 # shared library instructions
      src/
```

## Choose Where to Start Claude

Where you launch `claude` is the foundational decision — read it before applying any other setting, because it determines which files Claude can read and edit without an additional permission grant, which CLAUDE.md files load into context at startup, and which project settings apply.

| Start from | File access | CLAUDE.md loaded at launch | Use when |
| :--- | :--- | :--- | :--- |
| Repository root | Every file | Root only; subdirectory files load on demand when Claude reads there | Tasks span multiple packages or subsystems |
| A subdirectory | That subtree only, until you grant more | That directory's plus every ancestor's | Work is scoped to one package or subsystem |

A subtle but important rule: project settings in `.claude/settings.json` load **only from your starting directory** and are **not inherited from parent directories** the way CLAUDE.md files are. A `.claude/settings.json` at the repository root applies only when you start from the root. Each per-setting note states whether its settings file belongs at the repository root or in the subdirectory you start from, and whether it is committed or kept local.

## Scope and Plan Changes That Span Packages

Configuration controls *what Claude sees*. When a single change touches several packages — such as updating a shared type along with every call site that uses it — *how you scope and sequence the task* also affects the result. Two techniques keep a cross-package change consistent:

- **Give Claude the whole change in one session**: handing over the shared edit and its call sites together keeps the decisions behind each edit consistent, rather than re-deriving them per package.
- **Save the plan to a file before editing**: plan first, and ask Claude to write the plan to a markdown file in the repository. A long cross-package session [compacts its context](https://code.claude.com/docs/en/context-window) along the way, and the saved plan survives where conversation history may not.

## Next Steps

Once the configuration is in place, you can refine it: use [hooks](https://code.claude.com/docs/en/hooks-guide) to run per-directory linters or type-checkers after Claude edits files; review [Manage costs effectively](https://code.claude.com/docs/en/costs) to understand how codebase size affects token usage and to set spend limits before a wider rollout; and read [How Claude Code works in large codebases](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start) on the Claude blog for organizational rollout patterns and ownership models that sit above the per-repository configuration. The mechanics referenced above are split across notes 4–6 in this series.

**Source**: https://code.claude.com/docs/en/large-codebases
**Last Updated**: 2026-06-13
**Status**: Active
