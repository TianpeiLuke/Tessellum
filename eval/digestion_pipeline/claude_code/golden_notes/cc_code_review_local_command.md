---
tags:
  - resource
  - documentation
  - claude_code
  - code_review
  - local_command
keywords:
  - code-review command
  - local diff review
  - effort levels
  - comment flag
  - fix flag
  - ref range review
  - simplify rename
  - ultra escalation
topics:
  - Claude Code
  - Code Review
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/code-review
access_control_group: ["general"]
---

# Claude Code — Review a Diff Locally with `/code-review`

## Overview

The `/code-review` slash command reviews a diff in your terminal **without installing the GitHub App** — run it in any Claude Code session. Unlike the managed [Code Review](cc_code_review.md) service that runs on a PR, the local command reviews the diff in front of you: by default your branch's commits ahead of its upstream plus any uncommitted working-tree changes. It reports correctness bugs plus reuse, simplification, and efficiency cleanups, and can post findings as inline PR comments (`--comment`) or apply them to your working tree (`--fix`). It is the local, pre-push counterpart to the managed service and to the cloud [ultrareview](cc_ultrareview.md).

## What it reviews by default

The `/code-review` command reviews a diff in your terminal without installing the GitHub App. Run it in any Claude Code session: it reports correctness bugs and reuse, simplification, and efficiency cleanups. By default the local review covers your branch's commits ahead of its upstream **plus any uncommitted changes in the working tree**.

Two flags change what happens with the findings:

- `--comment` — post findings as inline PR comments.
- `--fix` — apply the findings to your working tree after the review.

## Effort levels (precision vs. coverage)

Lower [effort levels](https://code.claude.com/docs/en/model-config) return **fewer, higher-confidence findings**, while `high` through `max` give **broader coverage and may include uncertain findings**. Without an effort argument, the review uses the session's current effort.

## Choosing a target

To review something other than the default diff, pass a target. Four target forms are supported:

- a **file path**
- a **PR number**
- a **branch name**
- a **ref range** such as `main...my-feature`

The ref-range form reviews the **committed diff a pull request from `my-feature` into `main` would contain**, regardless of how the branch's upstream is configured.

## Escalating to cloud ultrareview

`/code-review ultra --fix` runs the deeper [ultrareview](cc_ultrareview.md) in the cloud, then applies its findings to your working tree when they arrive back in your session. Ultrareview uses **its own scope**: your current branch against the repository's default branch, plus any uncommitted and staged changes in the working tree.

## `/simplify` rename history

The command was named `/simplify` before v2.1.147, when it applied fixes by default. From v2.1.154, `/simplify` runs a **separate cleanup-only review** that applies fixes without hunting for bugs. If you scripted `/simplify` for bug-finding, switch to `/code-review --fix`, which is unchanged.

**Source**: https://code.claude.com/docs/en/code-review
**Last Updated**: 2026-06-13
**Status**: Active
