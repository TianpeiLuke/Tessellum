---
tags:
  - resource
  - documentation
  - claude_code
  - scheduling
  - desktop
keywords:
  - desktop scheduled tasks
  - routines page
  - local scheduled task
  - schedule presets
  - keep computer awake
  - missed runs catch-up
  - per-task permission mode
  - scheduled-tasks skill.md
  - update_scheduled_task
  - worktree per run
topics:
  - Claude Code
  - Automation & Scheduling
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/desktop-scheduled-tasks
access_control_group: ["general"]
---

# Claude Code — Desktop Scheduled Tasks

## Overview

A **Desktop scheduled task** starts a fresh Claude Code session automatically on your machine at a time and frequency you choose — useful for recurring work like daily code reviews, dependency-update checks, or morning briefings that pull from your calendar and inbox. The Desktop app's **Routines** page creates both these *local* tasks (this note) and *remote* cloud routines (see [`cc_routines_overview`](cc_routines_overview.md)). A local task has direct access to your files and tools but only fires while the app is open and your computer is awake; a remote routine runs on Anthropic-managed infrastructure even when your computer is off and can also fire on API calls or GitHub events.

This is the procedure for creating, scheduling, running, and managing local Desktop scheduled tasks. For how the three scheduling surfaces (Cloud / Desktop / `/loop`) compare across machine-on, open-session, local-file, MCP, permission, and interval axes, see the hub note [`cc_scheduling_options_comparison`](cc_scheduling_options_comparison.md).

## Create a scheduled task

Click **Routines** in the sidebar, then click **New routine** and choose **Local**. Configure these fields:

| Field | Description |
| --- | --- |
| Name | Identifier for the task. Converted to lowercase kebab-case and used as the folder name on disk. Must be unique across your tasks. |
| Description | Short summary shown in the task list. |
| Instructions | What Claude should do when the task runs. Write this the same way you'd write any message in the prompt box. The instructions input includes pickers for the permission mode and model, and below it you select the working folder and whether to run in an isolated worktree. |
| Schedule | How often the task runs (see Schedule options below). |

A **folder is required** before you can save the task. If you haven't trusted that folder yet, Desktop prompts you to trust it before saving.

You can also create a task by describing what you want in any session. For example, "set up a daily code review that runs every morning at 9am" creates a recurring task, and "remind me at 3pm tomorrow to check the deploy" creates a one-time task that disables itself after it fires.

By default, scheduled tasks run against whatever state your working directory is in, including uncommitted changes. Enable the **worktree toggle** when creating the task to give each run its own isolated Git worktree, the same way parallel sessions work (worktrees are documented at https://code.claude.com/docs/en/desktop).

## Schedule options

Pick a preset from the Schedule control:

- **Manual** — no schedule; only runs when you click **Run now**. Useful for saving a prompt you trigger on demand.
- **Hourly** — runs every hour.
- **Daily** — shows a time picker, defaults to 9:00 AM local time.
- **Weekdays** — same as Daily but skips Saturday and Sunday.
- **Weekly** — shows a time picker and a day picker.

For intervals the picker doesn't offer — such as every 15 minutes, the first of each month, or a single run at a specific future time — ask Claude in any Desktop session to set the schedule. Use plain language; for example, "schedule a task to run all the tests every 6 hours."

## How scheduled tasks run

Scheduled tasks run on your machine. Desktop checks the schedule every minute while the app is open and starts a **fresh session** when a task is due, independent of any manual sessions you have open. Each task gets a small delay of a few minutes after the scheduled time to **stagger API traffic**; the delay is deterministic — the same task always starts at the same offset.

When a task fires, you get a desktop notification and a new session appears under a **Scheduled** section in the sidebar. Open it to see what Claude did, review changes, or respond to permission prompts. The session works like any other: Claude can edit files, run commands, create commits, and open pull requests.

Tasks only run while the desktop app is running and your computer is awake. If your computer sleeps through a scheduled time, the run is skipped. To prevent idle-sleep, enable **Keep computer awake** in Settings under **Desktop app → General**. Closing the laptop lid still puts it to sleep. For tasks that need to run even when your computer is off, or that should trigger on an API call or GitHub event, create a remote routine instead (see [`cc_routine_triggers`](cc_routine_triggers.md)).

## Missed runs

When the app starts or your computer wakes, Desktop checks whether each task missed any runs in the last seven days. If it did, Desktop starts **exactly one catch-up run** for the most recently missed time and discards anything older. A daily task that missed six days runs once on wake. Desktop shows a notification when a catch-up run starts.

Keep this in mind when writing prompts. A task scheduled for 9am might run at 11pm if your computer was asleep all day. If timing matters, add guardrails to the prompt itself, for example: "Only review today's commits. If it's after 5pm, skip the review and just post a summary of what was missed."

## Permissions for scheduled tasks

Each task has its own **permission mode**, which you set when creating or editing the task. Allow rules from `~/.claude/settings.json` also apply to scheduled task sessions. If a task runs in **Ask** mode and needs to run a tool it doesn't have permission for, the run **stalls** until you approve it. The session stays open in the sidebar so you can answer later.

To avoid stalls, click **Run now** after creating a task, watch for permission prompts, and select "always allow" for each one. Future runs of that task auto-approve the same tools without prompting. You can review and revoke these approvals from the task's detail page. (Permission modes themselves are documented at https://code.claude.com/docs/en/permissions.)

## Manage scheduled tasks

Click a task in the **Routines** list to open its detail page. From here you can:

- **Run now** — start the task immediately without waiting for the next scheduled time.
- **Status** — toggle between Active and Paused to pause or resume scheduled runs without deleting the task.
- **Edit** — change the instructions, schedule, folder, or other settings.
- **Review history** — see every past run, including skipped runs. Hover a skipped entry to see why: your computer was asleep, the previous run was still in progress, or other scheduled tasks were already running. Click **Show more** to load older entries.
- **Review allowed permissions** — see and revoke saved tool approvals for this task from the **Always allowed** panel.
- **Delete** — remove the task and archive all sessions it created. An **Also delete files on disk** checkbox appears in the confirmation dialog; check it to also remove the task's `SKILL.md` file and associated data from `~/.claude/scheduled-tasks/`.

You can also list, create, edit, and pause tasks by asking Claude in any Desktop session ("pause my dependency-audit task" or "show me my scheduled tasks"). To delete a task, use the **Delete** button on its detail page.

A scheduled task can also modify its own schedule or prompt from within a running session using the `update_scheduled_task` MCP tool. This lets a task **reschedule itself** based on what it finds — for example, rescheduling a code review to run earlier when it detects a release branch has been created.

To edit a task's prompt on disk, open `~/.claude/scheduled-tasks/<task-name>/SKILL.md` (or under `CLAUDE_CONFIG_DIR` if set). The file uses YAML frontmatter for `name` and `description`, with the prompt as the body. Changes take effect on the next run. Schedule, folder, model, and enabled state are **not** in this file — change them through the Edit form or ask Claude.

**Source**: https://code.claude.com/docs/en/desktop-scheduled-tasks
**Last Updated**: 2026-06-13
**Status**: Active
