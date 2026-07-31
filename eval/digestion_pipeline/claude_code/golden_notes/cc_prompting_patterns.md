---
tags:
  - resource
  - documentation
  - claude_code
  - prompting
  - prompt_library
keywords:
  - prompting patterns
  - prompt library
  - describe the outcome not the steps
  - give it a way to check its own work
  - point at a reference
  - state the measurable target
  - give it the artifact
  - say how you want the answer
topics:
  - Claude Code
  - Prompting
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/prompt-library
access_control_group: ["general"]
---

# Claude Code — Prompting Patterns

## Overview

The **prompt library** is a collection of copy-paste prompts for Claude Code, tagged by task and role, meant for exploring ways of working you have not tried or as a starting point when you are not sure where to begin. The prompts themselves are starting points rather than scripts; the durable value is the **six reusable patterns** behind them. Recognizing these patterns lets you adapt any prompt to your own task and write your own.

This note distills those six patterns (the page's "What makes these prompts work" section), the library's purpose, and where the prompts come from. The interactive prompt-card widget on the page is implementation, not content, so it is not transcribed here.

## What Makes These Prompts Work

The prompts in the library share a few patterns. Recognizing them helps you adapt any prompt to your own task.

**Describe the outcome, not the steps.** Say what you want and let Claude find the files. The prompt works without naming a single file path.

```text
add rate limiting to the public API and make sure existing tests still pass
```

**Give it a way to check its own work.** Ask for run, test, compare, or verify in the same prompt so Claude iterates instead of stopping after one attempt.

```text
write the migration, run it against the dev database, and confirm the schema matches
```

**Point at a reference.** Name an existing file, test, or pattern to match so the new code is consistent with what you already have.

```text
add a settings page that follows the same layout as the profile page
```

**State the measurable target.** When the goal is performance or coverage, give the metric and threshold so completion is unambiguous.

> `get the bundle size under 200KB and show me what you removed`

**Give it the artifact.** Paste errors, logs, screenshots, and plan output directly in the prompt, or type `@` to reference a file. Claude reads the source instead of your description of it.

> `why is the build failing? @build.log`

**Say how you want the answer.** Name the format, length, or audience so the explanation fits how you will use it. To make a format the default for every response, set an [output style](cc_output_styles.md).

> `explain how the payment retry logic works as an HTML page with a diagram, then open it in my browser`

For more on each pattern, the page points to the [best practices](https://code.claude.com/docs/en/best-practices) guide.

## Where These Come From

The prompts are based on patterns from published Anthropic resources, and each prompt card in the library links to its source:

- **Common workflows** — step-by-step guides for the core tasks.
- **Best practices** — prompting patterns and project setup.
- **How Anthropic teams use Claude Code** — real workflows from engineering, product, design, and data teams, with deep dives on legal, marketing, and cybersecurity.
- **Scaling agentic coding guide** — the enterprise adoption guide.

For video walkthroughs of these patterns, the page links the free *Claude Code in Action* course on Anthropic Academy.

## Making a Prompt Repeatable

The page frames the prompts as starting points. Once one works for your project, the next step is making it repeatable: save it as a [skill](cc_skills_overview.md) so anyone on your team can run it as a `/command`, and record the conventions Claude learned in `CLAUDE.md` ([memory](https://code.claude.com/docs/en/memory)) so every session starts with that context instead of Claude relearning it. For larger or riskier changes, [plan mode](https://code.claude.com/docs/en/permission-modes) shows you the file list before any edits happen.

**Source**: https://code.claude.com/docs/en/prompt-library
**Last Updated**: 2026-06-13
**Status**: Active
