---
tags:
  - resource
  - documentation
  - claude_code
  - automation
  - scaling
keywords:
  - automate and scale
  - non-interactive mode
  - claude -p
  - parallel sessions
  - fan out across files
  - allowedtools
  - auto mode
  - adversarial review subagent
topics:
  - Claude Code
  - Automation
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/best-practices
access_control_group: ["general"]
---

# Claude Code — Automate and Scale

## Overview

Everything in the best-practices guide up to this point assumes one human, one Claude, and one conversation. But Claude Code **scales horizontally**: once you're effective with one Claude, you can multiply output with parallel sessions, non-interactive mode, and fan-out patterns. This note is the procedure for that horizontal scaling — five mechanisms in increasing order of unattended autonomy: run **non-interactive mode** (`claude -p`) inside CI/scripts, run **multiple sessions** in parallel, **fan out** the same task across many files, run **autonomously with auto mode**, and **add an adversarial review step** so the work gets an independent check before you count it as done.

Each mechanism is summarized here as the operating procedure; the deeper mechanics live in their home pages — [non-interactive/headless mode](https://code.claude.com/docs/en/headless), [worktrees](https://code.claude.com/docs/en/worktrees), [agent teams](https://code.claude.com/docs/en/agent-teams), [permission modes / auto mode](https://code.claude.com/docs/en/permission-modes), and [sub-agents](https://code.claude.com/docs/en/sub-agents) — and are linked, not re-taught.

## Run non-interactive mode

> Tip: Use `claude -p "prompt"` in CI, pre-commit hooks, or scripts. Add `--output-format stream-json --verbose` for streaming JSON output.

With `claude -p "your prompt"` you run Claude non-interactively, without a session. [Non-interactive mode](https://code.claude.com/docs/en/headless) is how you integrate Claude into CI pipelines, pre-commit hooks, or any automated workflow. The output formats let you parse results programmatically: plain text, JSON, or streaming JSON.

```bash
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json --verbose
```

## Run multiple Claude sessions

> Tip: Run multiple Claude sessions in parallel to speed up development, run isolated experiments, or start complex workflows.

Pick the parallel approach that fits how much coordination you want to do yourself:

- **[Worktrees](https://code.claude.com/docs/en/worktrees)**: run separate CLI sessions in isolated git checkouts so edits don't collide.
- **[Desktop app](https://code.claude.com/docs/en/desktop)**: manage multiple local sessions visually, each in its own worktree.
- **[Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)**: run sessions on Anthropic-managed cloud infrastructure in isolated VMs.
- **[Agent teams](https://code.claude.com/docs/en/agent-teams)**: automated coordination of multiple sessions with shared tasks, messaging, and a team lead.

Beyond parallelizing work, multiple sessions enable quality-focused workflows. A fresh context improves code review since Claude won't be biased toward code it just wrote. For example, use a **Writer/Reviewer pattern**: Session A (Writer) implements the feature; Session B (Reviewer) reviews the implementation in a fresh context, looking for edge cases, race conditions, and consistency with existing patterns; then the Writer takes the review feedback and addresses the issues. You can do something similar with tests: have one Claude write tests, then another write code to pass them.

## Fan out across files

> Tip: Loop through tasks calling `claude -p` for each. Use `--allowedTools` to scope permissions for batch operations.

For large migrations or analyses, distribute work across many parallel Claude invocations:

1. **Generate a task list** — have Claude list all files that need migrating (e.g., `list all 2,000 Python files that need migrating`).
2. **Write a script to loop through the list** — call `claude -p` once per file, scoping permissions with `--allowedTools`.
3. **Test on a few files, then run at scale** — refine your prompt based on what goes wrong with the first 2-3 files, then run on the full set. The `--allowedTools` flag restricts what Claude can do, which matters when you're running unattended.

```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

You can also integrate Claude into existing data/processing pipelines:

```bash
claude -p "<your prompt>" --output-format json | your_command
```

Use `--verbose` for debugging during development, and turn it off in production.

## Run autonomously with auto mode

For uninterrupted execution with background safety checks, use [auto mode](https://code.claude.com/docs/en/permission-modes). A classifier model reviews commands before they run, blocking scope escalation, unknown infrastructure, and hostile-content-driven actions while letting routine work proceed without prompts.

```bash
claude --permission-mode auto -p "fix all lint errors"
```

For non-interactive runs with the `-p` flag, auto mode **aborts if the classifier repeatedly blocks actions**, since there is no user to fall back to. See [when auto mode falls back](https://code.claude.com/docs/en/permission-modes) for the thresholds.

## Add an adversarial review step

> Tip: Before treating a task as done, have a subagent review the diff in a fresh context and report gaps.

The longer Claude works unattended, the more an independent check matters before you count the work as done. A reviewer running in a fresh [subagent](https://code.claude.com/docs/en/sub-agents) context sees only the diff and the criteria you give it — not the reasoning that produced the change — so it evaluates the result on its own terms.

For a correctness check, run the bundled [`/code-review` skill](https://code.claude.com/docs/en/commands), which reviews the current diff for bugs in a fresh subagent and returns findings to the session. To check the diff against your plan instead, write the review prompt yourself — name the work to check, the plan to check it against, and what counts as a finding:

```text
Use a subagent to review the rate limiter diff against PLAN.md. Check that
every requirement is implemented, the listed edge cases have tests, and
nothing outside the task's scope changed. Report gaps, not style preferences.
```

Because the reviewer runs as a subagent, the implementing session receives the gaps directly and can fix them and re-review without you copying findings between windows. For longer autonomous runs, an [agent team](https://code.claude.com/docs/en/agent-teams) can keep this loop going across many tasks while you spot-check the recorded findings.

> Caveat: A reviewer prompted to find gaps will usually report some, even when the work is sound, because that is what it was asked to do. Chasing every finding leads to over-engineering — extra abstraction layers, defensive code, and tests for cases that can't happen. Tell the reviewer to flag only gaps that affect correctness or the stated requirements, and treat the rest as optional.

**Source**: https://code.claude.com/docs/en/best-practices
**Last Updated**: 2026-06-13
**Status**: Active
