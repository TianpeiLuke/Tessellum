---
tags:
  - resource
  - documentation
  - claude_code
  - workflow
  - plan_mode
keywords:
  - explore first then plan then code
  - four-phase workflow
  - plan mode
  - separate research from implementation
  - ctrl+g plan editing
  - when to skip planning
  - one-sentence diff
topics:
  - Claude Code
  - Workflow
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/best-practices
access_control_group: ["general"]
---

# Claude Code — Explore First, Then Plan, Then Code

## Overview

Letting Claude jump straight to coding can produce code that solves the wrong problem. The recommended workflow separates research and planning from implementation so the implementation phase starts from accurate understanding rather than a guess. It runs in four phases — **Explore**, **Plan**, **Implement**, **Commit** — with the first phase in [plan mode](https://code.claude.com/docs/en/permission-modes) (read-only, no edits) before switching modes to write code.

Plan mode is useful but adds overhead, so it is applied selectively: planning pays off when the approach is uncertain, the change spans multiple files, or the code is unfamiliar; it is skipped when the scope is clear and the fix is small.

## The Four-Phase Workflow

The recommended workflow has four phases:

### 1. Explore

Enter plan mode. Claude reads files and answers questions without making changes.

```txt claude (plan mode)
read /src/auth and understand how we handle sessions and login.
also look at how we manage environment variables for secrets.
```

### 2. Plan

Ask Claude to create a detailed implementation plan.

```txt claude (plan mode)
I want to add Google OAuth. What files need to change?
What's the session flow? Create a plan.
```

Press `Ctrl+G` to open the plan in your text editor for direct editing before Claude proceeds.

### 3. Implement

Switch out of plan mode and let Claude code, verifying against its plan.

```txt claude (default mode)
implement the OAuth flow from your plan. write tests for the
callback handler, run the test suite and fix any failures.
```

### 4. Commit

Ask Claude to commit with a descriptive message and create a PR.

```txt claude (default mode)
commit with a descriptive message and open a PR
```

## When to Skip Planning

Plan mode is useful, but also adds overhead. For tasks where the scope is clear and the fix is small — like fixing a typo, adding a log line, or renaming a variable — ask Claude to do it directly.

Planning is most useful when you are uncertain about the approach, when the change modifies multiple files, or when you are unfamiliar with the code being modified. The rule of thumb: **if you could describe the diff in one sentence, skip the plan.**

**Source**: https://code.claude.com/docs/en/best-practices
**Last Updated**: 2026-06-13
**Status**: Active
