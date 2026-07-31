---
tags:
  - resource
  - documentation
  - claude_code
  - verification_loop
  - best_practices
keywords:
  - verification loop
  - give claude a way to verify its work
  - looks done signal
  - pass or fail check
  - test build lint screenshot diff
  - goal condition stop hook
  - verification subagent second opinion
  - show evidence
  - context window fills fast
topics:
  - Claude Code
  - Best Practices
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/best-practices
access_control_group: ["general"]
---

# Claude Code — The Verification Loop

## Overview

Claude Code's best practices rest on one constraint: **the context window fills up fast, and performance degrades as it fills**. A single debugging session or codebase exploration can consume tens of thousands of tokens, and as the window fills Claude may start "forgetting" earlier instructions or making more mistakes — so context is the most important resource to manage. The first doctrine that follows from this constraint is the **verification loop**: because Claude stops when the work *looks* done, you should give it a check it can run so the loop closes on its own instead of consuming your attention as the human verifier. This note digests that argument — why "looks done" is unreliable, what counts as a readable check, and the ladder of how hard the check gates the stop.

## Why "Looks Done" Is Unreliable

Claude stops when the work looks done. Without a check it can run, "looks done" is the only signal available, and **you become the verification loop**: every mistake waits for you to notice it. Give Claude something that produces a **pass or fail**, and the loop closes on its own — Claude does the work, runs the check, reads the result, and iterates until the check passes. This is the difference between a session you have to watch and one you can walk away from.

## What Counts as a Check

The check is anything that returns a signal Claude can read in the conversation:

- a test suite,
- a build exit code,
- a linter,
- a script that diffs output against a fixture, or
- a [browser screenshot](https://code.claude.com/docs/en/chrome) compared against a design.

The best-practices guide frames three verification strategies as before/after prompt pairs: **provide verification criteria** (name example test cases and tell Claude to run the tests after implementing), **verify UI changes visually** (paste a screenshot, then have Claude screenshot its result, list differences, and fix them), and **address root causes, not symptoms** (paste the build error, fix it, verify the build succeeds, and don't suppress the error).

## How Hard the Check Gates the Stop

Once the check exists, decide how hard it gates the stop — each step trades setup for attention:

- **In one prompt** — ask Claude to run the check and iterate in the same message. The prompt version works on any task today.
- **Across a session** — set the check as a [`/goal` condition](https://code.claude.com/docs/en/goal). A separate evaluator re-checks it after every turn and Claude keeps working until it holds.
- **As a deterministic gate** — a [Stop hook](https://code.claude.com/docs/en/hooks) runs your check as a script and blocks the turn from ending until it passes. Claude Code overrides the hook and ends the turn after 8 consecutive blocks.
- **By a second opinion** — a [verification subagent](https://code.claude.com/docs/en/sub-agents) or a [dynamic workflow](https://code.claude.com/docs/en/workflows) has a fresh model try to refute the result, so the agent doing the work isn't the one grading it.

The `/goal` and Stop hook versions are what let an unattended run finish correctly without you.

## Show Evidence, Don't Assert

Have Claude **show evidence rather than asserting success**: the test output, the command it ran and what it returned, or a screenshot of the result. Reviewing evidence is faster than re-running the verification yourself, and — critically — it works for sessions you weren't watching. This is the same discipline that closes the [agentic loop](cc_agentic_loop.md)'s "verify results" phase, and it precedes the explore-then-plan-then-code procedure: a plan is only as good as the verification step that proves the implementation matches it.

**Source**: https://code.claude.com/docs/en/best-practices
**Last Updated**: 2026-06-13
**Status**: Active
