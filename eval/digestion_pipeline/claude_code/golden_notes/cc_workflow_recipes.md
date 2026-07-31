---
tags:
  - resource
  - documentation
  - claude_code
  - workflows
  - prompt_recipes
keywords:
  - prompt recipes
  - codebase overview
  - fix bugs efficiently
  - refactor code
  - work with tests
  - create pull requests
  - handle documentation
  - delegate research to subagents
  - pipe claude into scripts
topics:
  - Claude Code
  - Common Workflows
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/common-workflows
access_control_group: ["general"]
---

# Claude Code — Workflow Recipes

## Overview

This note collects the **prompt recipes** from Claude Code's common-workflows page — short, copy-paste prompt patterns for everyday development tasks (exploring unfamiliar code, fixing bugs, refactoring, writing tests, creating PRs, handling docs, working in non-code folders, and asking Claude about its own capabilities). Each recipe is a small staged sequence of natural-language asks that you adapt to your project; they work in any Claude Code surface. The page also closes with five short link-out sections — resume conversations, parallel worktree sessions, plan-before-editing, delegate research to subagents, and pipe Claude into scripts — summarized here as pointers to their home topics.

For higher-level prompting and context-management guidance behind these recipes, see [Effective Prompting](cc_effective_prompting.md), [Explore, Plan, Code](cc_explore_plan_code.md), and [Manage Your Session](cc_manage_your_session.md).

## Prompt Recipes

These are prompt patterns for everyday tasks. Each works in any Claude Code surface; adapt the wording to your project. Each recipe stages a sequence of asks — start broad, then narrow.

### Understand new codebases

For configuring Claude Code in a monorepo or large codebase, see the [Monorepos and large repos](https://code.claude.com/docs/en/large-codebases) guide.

- **Get a quick codebase overview** — `cd /path/to/project`, start `claude`, then ask `give me an overview of this codebase`. Dive deeper with `explain the main architecture patterns used here`, `what are the key data models?`, and `how is authentication handled?`. Tips: start with broad questions then narrow down; ask about coding conventions and patterns; request a glossary of project-specific terms.
- **Find relevant code** — `find the files that handle user authentication`, then `how do these authentication files work together?`, then `trace the login process from front-end to database`. Tips: be specific about what you are looking for; use domain language from the project; install a [code intelligence plugin](https://code.claude.com/docs/en/discover-plugins#code-intelligence) for precise "go to definition" / "find references" navigation.

### Fix bugs efficiently

When you have an error message and need to find and fix its source, share the error, ask for fixes, then apply:

```text
I'm seeing an error when I run npm test
```
```text
suggest a few ways to fix the @ts-ignore in user.ts
```
```text
update user.ts to add the null check you suggested
```

Tips: tell Claude the command to reproduce the issue so it can get a stack trace; mention reproduction steps; note whether the error is intermittent or consistent.

### Refactor code

To modernize old code, stage it: `find deprecated API usage in our codebase` → `suggest how to refactor utils.js to use modern JavaScript features` → `refactor utils.js to use ES2024 features while maintaining the same behavior` → `run tests for the refactored code`. Tips: ask Claude to explain the benefits of the modern approach; request backward compatibility when needed; refactor in small, testable increments.

### Work with tests

To add tests for uncovered code: `find functions in NotificationsService.swift that are not covered by tests` → `add tests for the notification service` → `add test cases for edge conditions in the notification service` → `run the new tests and fix any failures`.

Claude generates tests that follow your project's existing patterns and conventions — it examines your existing test files to match the style, frameworks, and assertion patterns already in use, so be specific about what behavior you want to verify. For comprehensive coverage, ask Claude to identify edge cases you might have missed (error conditions, boundary values, unexpected inputs).

### Create pull requests

Ask directly (`create a pr for my changes`) or guide it step-by-step: `summarize the changes I've made to the authentication module` → `create a pr` → `enhance the PR description with more context about the security improvements`.

When you create a PR using `gh pr create`, the session is automatically linked to that PR. To return to it later, run `claude --from-pr <number>` or paste the PR URL into the [`/resume` picker](https://code.claude.com/docs/en/sessions#use-the-session-picker) search. Review Claude's generated PR before submitting and ask it to highlight potential risks or considerations.

### Handle documentation

To add or update docs: `find functions without proper JSDoc comments in the auth module` → `add JSDoc comments to the undocumented functions in auth.js` → `improve the generated documentation with more context and examples` → `check if the documentation follows our project standards`. Tips: specify the documentation style (JSDoc, docstrings, etc.); ask for examples; request docs for public APIs, interfaces, and complex logic.

### Work in notes and non-code folders

Claude Code works in any directory. Run it inside a notes vault, a documentation folder, or any collection of markdown files to search, edit, and reorganize content the same way you would code. The `.claude/` directory and `CLAUDE.md` sit alongside other tools' config directories without conflict. Claude reads files fresh on each tool call, so it sees edits you make in another application the next time it reads that file.

### Ask Claude about its capabilities

Claude has built-in access to its documentation and can answer questions about its own features and limitations — for example:

```text
can Claude Code create pull requests?
how does Claude Code handle permissions?
what skills are available?
how do I use MCP with Claude Code?
how do I configure Claude Code for Amazon Bedrock?
what are the limitations of Claude Code?
```

Claude provides documentation-based answers to these questions. For hands-on demonstrations, run `/powerup` for interactive lessons with animated demos. Claude always has access to the latest Claude Code documentation regardless of the version you are using; ask specific questions to get detailed answers.

> **Folded out:** *Work with images* and *Reference files and directories* (`@`-refs and `@server:resource` MCP resources) live with the rich-content guidance in [Effective Prompting](cc_effective_prompting.md). *Run Claude on a schedule* (Routines / desktop scheduled tasks / GitHub Actions / `/loop`) is covered in [Non-interactive mode](https://code.claude.com/docs/en/headless) and [Routines](https://code.claude.com/docs/en/routines).

## Session and Scaling Recipes (link-outs)

The page closes with five short recipes that point to their full home topics:

- **Resume previous conversations** — when a task spans multiple sittings, `claude --continue` resumes the most recent session in the current directory (prints `No conversation found to continue` if none exists); `claude --resume` chooses from a list; `/resume` works inside a running session. See [Manage sessions](https://code.claude.com/docs/en/sessions) and [Manage Your Session](cc_manage_your_session.md).
- **Run parallel sessions with worktrees** — `claude --worktree feature-auth` starts an isolated checkout on its own branch; run it with a different name in a second terminal for a parallel session. See [Worktrees](https://code.claude.com/docs/en/worktrees) and, to monitor parallel sessions from one screen, [background agents](https://code.claude.com/docs/en/agent-view).
- **Plan before editing** — `claude --permission-mode plan` (or `Shift+Tab` mid-session) reads files and proposes a plan but makes no edits until you approve. See [Plan mode](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) and [Explore, Plan, Code](cc_explore_plan_code.md).
- **Delegate research to subagents** — `use a subagent to investigate how our auth system handles token refresh` reads files in a separate context window and reports only a summary, keeping your main context clean. See [Subagents](https://code.claude.com/docs/en/sub-agents).
- **Pipe Claude into scripts** — run Claude non-interactively for CI, pre-commit hooks, or batch processing; stdin/stdout work like any Unix tool, e.g. `git log --oneline -20 | claude -p "summarize these recent commits"`. See [Non-interactive mode](https://code.claude.com/docs/en/headless) and [Automate and Scale](cc_automate_and_scale.md).

**Source**: https://code.claude.com/docs/en/common-workflows
**Last Updated**: 2026-06-13
**Status**: Active
