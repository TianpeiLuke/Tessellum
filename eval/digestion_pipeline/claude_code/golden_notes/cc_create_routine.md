---
tags:
  - resource
  - documentation
  - claude_code
  - routines
  - automation
keywords:
  - create a routine
  - routine creation form
  - claude/ branches
  - cloud environment
  - select a trigger
  - connectors and permissions
  - /schedule cli
  - autonomous cloud session
topics:
  - Claude Code
  - Routines
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/routines
access_control_group: ["general"]
---

# Claude Code — Create a Routine

## Overview

A routine is created from one of three surfaces — the web at `claude.ai/code/routines`, the Desktop app, or the CLI with `/schedule`. All three write to the same cloud account, so a routine created in one surface appears in the others immediately. The creation form sets up five things: the routine's **prompt** (with a model selector), one or more **repositories**, a cloud **environment**, one or more **triggers**, and the **connectors and permissions** that bound what the run can reach.

Because a routine runs autonomously as a full Claude Code cloud session — no permission-mode picker and no approval prompts during a run — the prompt must be self-contained and explicit about what to do and what success looks like, and every scope (repositories, environment, connectors) should be narrowed to only what the routine actually needs. This note is the step-by-step procedure for the web/Desktop form and the `/schedule` CLI form; trigger configuration detail lives in [`cc_routine_triggers.md`](cc_routine_triggers.md) and post-creation management in [`cc_manage_routines.md`](cc_manage_routines.md).

## Choosing the creation surface

Create a routine from the web at `claude.ai/code/routines`, from the Desktop app, or from the CLI. In the Desktop app, click **Routines** in the sidebar, then **New routine**, and choose **Remote**. Choosing **Local** instead creates a [Desktop scheduled task](https://code.claude.com/docs/en/desktop-scheduled-tasks) (covered in [`cc_desktop_scheduled_tasks.md`](cc_desktop_scheduled_tasks.md)), which runs on your machine rather than in the cloud.

Routines belong to your individual claude.ai account. They are not shared with teammates, and they count against your account's daily run allowance. Anything a routine does through your connected GitHub identity or connectors appears as you: commits and pull requests carry your GitHub user, and Slack messages, Linear tickets, or other connector actions use your linked accounts.

## Create from the web

The web form walks through the following steps:

1. **Open the creation form** — Visit `claude.ai/code/routines` and click **New routine**.
2. **Name the routine and write the prompt** — Give the routine a descriptive name and write the prompt Claude runs each time. The prompt is the most important part: the routine runs autonomously, so the prompt must be self-contained and explicit about what to do and what success looks like. The prompt input includes a **model selector**; Claude uses the selected model on every run.
3. **Select repositories** — Add one or more GitHub repositories for Claude to work in. Each repository is cloned at the start of a run, starting from the default branch. Claude creates `claude/`-prefixed branches for its changes.
4. **Select an environment** — Pick a [cloud environment](https://code.claude.com/docs/en/claude-code-on-the-web#the-cloud-environment) that controls **network access** (the level of internet access during each run), **environment variables** (API keys, tokens, or other secrets Claude can use), and a **setup script** (installs dependencies and tools; the result is cached so it does not re-run every session). A **Default** environment is provided with **Trusted** network access, which allows the default set of package registries, cloud provider APIs, container registries, and common development domains but blocks everything else. If the routine needs to reach your own services or a domain outside that list, edit the environment's network access before running, or create a separate environment first.
5. **Select a trigger** — Under **Select a trigger**, choose how the routine starts. You can pick one trigger type or combine several: **Schedule** (preset frequency for a recurring run, or a single one-off run at a timestamp), **GitHub event** (repository, event, optional filters), or **API** (select **API**, save the routine, then generate the URL and token afterward, since they depend on the routine ID). Full configuration detail for each type is in [`cc_routine_triggers.md`](cc_routine_triggers.md).
6. **Review connectors and permissions** — The **Connectors** and **Permissions** tabs at the bottom control what the routine can reach. Under Connectors, all of your connected [MCP connectors](https://code.claude.com/docs/en/mcp) are included by default; remove any the routine doesn't need (Claude can use every tool from an included connector, including writes, without asking during a run). Under Permissions, enable **Allow unrestricted branch pushes** for any repository where Claude should push to existing branches instead of only `claude/`-prefixed ones.
7. **Create the routine** — Click **Create**. The routine appears in the list and runs the next time one of its triggers matches. To start a run immediately, click **Run now** on the routine's detail page. Each run creates a new session alongside your other sessions, where you can see what Claude did, review changes, and create a pull request.

## What the autonomous run can reach

Routines run autonomously as full Claude Code cloud sessions: there is no permission-mode picker and no approval prompts during a run. The session can run shell commands, use [skills](https://code.claude.com/docs/en/skills) committed to the cloned repository, and call any connectors you include. What a routine can reach is determined by:

- the **repositories** you select and their branch-push setting,
- the **environment's** network access and variables, and
- the **connectors** you include.

Scope each of those to what the routine actually needs.

## Create from the CLI

Run `/schedule` in any session to create a scheduled routine conversationally. You can also pass a description directly:

```text
/schedule daily PR review at 9am
```

This works for a recurring routine like the above, or a one-off like `/schedule clean up feature flag in one week`. Claude walks through the same information the web form collects, then saves the routine to your account.

`/schedule` in the CLI creates **scheduled routines only**. To add an API or GitHub trigger, edit the routine on the web at `claude.ai/code/routines`.

The CLI also supports managing existing routines:

- `/schedule list` — see all routines
- `/schedule update` — change one
- `/schedule run` — trigger it immediately

**Source**: https://code.claude.com/docs/en/routines
**Last Updated**: 2026-06-13
**Status**: Active
