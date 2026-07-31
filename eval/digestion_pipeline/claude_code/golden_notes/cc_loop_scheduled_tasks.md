---
tags:
  - resource
  - documentation
  - claude_code
  - scheduled_tasks
  - loop
keywords:
  - /loop bundled skill
  - run a prompt repeatedly
  - fixed interval loop
  - claude chooses the interval
  - built-in maintenance prompt
  - loop.md default prompt
  - stop a loop with esc
  - one-time reminder
topics:
  - Claude Code
  - Scheduled Tasks
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/scheduled-tasks
access_control_group: ["general"]
---

# Claude Code — Run a Prompt Repeatedly with /loop

## Overview

The `/loop` bundled skill is the quickest way to run a prompt on repeat while a Claude Code session stays open. Both the interval and the prompt are optional, and what you provide determines how the loop behaves: an interval plus a prompt runs on a fixed cron schedule, a prompt alone runs at an interval Claude chooses each iteration, and a bare `/loop` runs the built-in maintenance prompt (or your `loop.md` if one exists). For one-shot work rather than a repeat, you describe a one-time reminder in natural language and Claude schedules a single-fire task that deletes itself after running. These are all session-scoped tasks — they live in the current conversation; the execution semantics (firing, jitter, expiry, cron tools) are covered in [`cc_scheduled_task_execution_model`](cc_scheduled_task_execution_model.md), and how `/loop` compares to cloud and Desktop scheduling is in [`cc_scheduling_options_comparison`](cc_scheduling_options_comparison.md).

## The three /loop modes

What you pass to `/loop` selects one of three behaviors:

| What you provide | Example | What happens |
| :--- | :--- | :--- |
| Interval and prompt | `/loop 5m check the deploy` | Your prompt runs on a fixed schedule |
| Prompt only | `/loop check the deploy` | Your prompt runs at an interval Claude chooses each iteration |
| Interval only, or nothing | `/loop` | The built-in maintenance prompt runs, or your `loop.md` if one exists |

You can also pass another command or skill as the prompt — for example `/loop 20m /review-pr 1234` — to re-run a saved skill or command each iteration.

### Run on a fixed interval

When you supply an interval, Claude converts it to a cron expression, schedules the job, and confirms the cadence and job ID.

```text theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

The interval can lead the prompt as a bare token like `30m`, or trail it as a clause like `every 2 hours`. Supported units are `s` for seconds, `m` for minutes, `h` for hours, and `d` for days. Seconds are rounded up to the nearest minute since cron has one-minute granularity. Intervals that don't map to a clean cron step, such as `7m` or `90m`, are rounded to the nearest interval that does, and Claude tells you what it picked.

### Let Claude choose the interval

When you omit the interval, Claude chooses one dynamically instead of running on a fixed cron schedule. After each iteration it picks a delay between one minute and one hour based on what it observed: short waits while a build is finishing or a PR is active, longer waits when nothing is pending. The chosen delay and the reason for it are printed at the end of each iteration.

```text theme={null}
/loop check whether CI passed and address any review comments
```

When you ask for a dynamic `/loop` schedule, Claude may use the [Monitor tool](https://code.claude.com/docs/en/tools-reference) directly. Monitor runs a background script and streams each output line back, which avoids polling altogether and is often more token-efficient and responsive than re-running a prompt on an interval. A dynamically scheduled loop appears in your scheduled task list like any other task, so you can list or cancel it the same way. The jitter rules don't apply to it, but the seven-day expiry does: the loop ends automatically seven days after you start it (see [`cc_scheduled_task_execution_model`](cc_scheduled_task_execution_model.md)).

### Run the built-in maintenance prompt

When you omit the prompt, Claude uses a built-in maintenance prompt instead of one you supply. On each iteration it works through the following, in order:

- continue any unfinished work from the conversation
- tend to the current branch's pull request: review comments, failed CI runs, merge conflicts
- run cleanup passes such as bug hunts or simplification when nothing else is pending

Claude does not start new initiatives outside that scope, and irreversible actions such as pushing or deleting only proceed when they continue something the transcript already authorized.

```text theme={null}
/loop
```

A bare `/loop` runs this prompt at a dynamically chosen interval. Add an interval, for example `/loop 15m`, to run it on a fixed schedule instead. To replace the built-in prompt with your own default, use `loop.md` (below).

### Customize the default prompt with loop.md

A `loop.md` file replaces the built-in maintenance prompt with your own instructions. It defines a single default prompt for bare `/loop`, not a list of separate scheduled tasks, and is ignored whenever you supply a prompt on the command line. To schedule additional prompts alongside it, use `/loop <prompt>` or ask Claude directly. Claude looks for the file in two locations and uses the first one it finds:

| Path | Scope |
| :--- | :--- |
| `.claude/loop.md` | Project-level. Takes precedence when both files exist. |
| `~/.claude/loop.md` | User-level. Applies in any project that does not define its own. |

The file is plain Markdown with no required structure — write it as if you were typing the `/loop` prompt directly. The following example keeps a release branch healthy:

```markdown title=".claude/loop.md" theme={null}
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

Edits to `loop.md` take effect on the next iteration, so you can refine the instructions while a loop is running. When no `loop.md` exists in either location, the loop falls back to the built-in maintenance prompt. Keep the file concise: content beyond 25,000 bytes is truncated.

### Stop a loop

To stop a `/loop` while it is waiting for the next iteration, press `Esc`. This clears the pending wakeup so the loop does not fire again. Tasks you scheduled by asking Claude directly are not affected by `Esc` and stay in place until you delete them. In self-paced mode (when Claude chooses the interval), Claude can also end the loop on its own by not scheduling the next wakeup once the task is provably complete. Loops on a fixed interval keep running until you stop them or seven days elapse.

## Set a one-time reminder

For one-shot reminders, describe what you want in natural language instead of using `/loop`. Claude schedules a single-fire task that deletes itself after running, pinning the fire time to a specific minute and hour using a cron expression, and confirms when it will fire.

```text theme={null}
remind me at 3pm to push the release branch

in 45 minutes, check whether the integration tests passed
```

## Managed-platform caveats

On Bedrock, Vertex AI, and Microsoft Foundry, `/loop` behaves differently in the prompt-only and prompt-less modes:

- A prompt with no interval runs on a fixed 10-minute schedule instead of a dynamically chosen one.
- `/loop` with no prompt prints the usage message instead of running the maintenance prompt.
- `loop.md` isn't read, and `/loop` with no prompt prints the usage message instead.

Scheduled tasks (and therefore `/loop`) require Claude Code v2.1.72 or later; check your version with `claude --version`.

**Source**: https://code.claude.com/docs/en/scheduled-tasks
**Last Updated**: 2026-06-13
**Status**: Active
