---
tags:
  - resource
  - documentation
  - claude_code
  - workflows
  - procedure
keywords:
  - have claude write a workflow
  - ultracode keyword
  - effort ultracode
  - approve the plan
  - save the workflow
  - workflows view
  - resume after a pause
  - turn workflows off
topics:
  - Claude Code
  - Workflows
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/workflows
access_control_group: ["general"]
---

# Make and Operate a Dynamic Workflow

## Overview

This note is the operational procedure for [dynamic workflows](https://code.claude.com/docs/en/workflows): how to have Claude **write** a workflow for your task, **approve** the plan before it runs, **watch** the run, **save** it for reuse, **pass input** to it, and **manage** runs (resume, cost, turn off). For the concept — what a workflow is and how it runs in an isolated runtime — see the companion concept note [`cc_dynamic_workflows.md`](cc_dynamic_workflows.md).

## Have Claude write a workflow

You can have Claude write a workflow for your task in two ways: ask for a workflow in your prompt, or let Claude decide with `ultracode`. You can also run a workflow command that already exists — a bundled workflow like `/deep-research`, or one you've saved.

### Ask for a workflow in your prompt

To run a single task as a workflow without changing the session's effort level, include the keyword `ultracode` in your prompt. Asking in your own words ("use a workflow" / "run a workflow") also works — Claude treats a direct request as the same opt-in. Before v2.1.160 the literal trigger keyword was `workflow`; natural-language requests work in both versions.

```text theme={null}
ultracode: audit every API endpoint under src/routes/ for missing auth checks
```

Claude Code highlights the keyword and writes a workflow script instead of working through the task turn by turn. To dismiss the highlight for this prompt, press `Option+W` (macOS) or `Alt+W` (Windows/Linux), or press backspace while the cursor is right after the highlighted keyword. To stop the keyword triggering at all, turn off **Ultracode keyword trigger** in `/config`. If you already have an orchestrator built another way (a folder of subagent prompts or a skill that fans work out), you can point Claude at it and ask for a workflow that does the same thing.

### Let Claude decide with ultracode

Ultracode is a setting that combines `xhigh` [reasoning effort](https://code.claude.com/docs/en/model-config) with automatic workflow orchestration. With it on, Claude plans a workflow for each substantive task instead of waiting for you to ask.

```text theme={null}
/effort ultracode
```

A single request can turn into several workflows in a row (understand the code, make the change, verify it). This applies to every task in the session, so each request uses more tokens and takes longer. Ultracode lasts for the current session and resets when you start a new one; drop back with `/effort high` for routine work. It's available only on models that support `xhigh` effort.

### Approve the plan before it runs

In the CLI, the per-run prompt shows the planned phases and these options: **Yes, run it**; **Yes, and don't ask again for `<name>` in `<path>`** (skip this prompt for this workflow in this project from now on); **View raw script**; **No**. `Ctrl+G` opens the script in your editor; `Tab` lets you adjust the prompt before the run starts. Whether you see this prompt depends on your [permission mode](https://code.claude.com/docs/en/permission-modes):

| Permission mode | When you're prompted |
| :--- | :--- |
| Default, accept edits | Every run, unless you've selected **Yes, and don't ask again** for that workflow in this project |
| Auto | First launch only; any **Yes** records consent in user settings, later launches don't prompt. Skipped entirely when ultracode is on |
| Bypass permissions, `claude -p`, Agent SDK | Never. The run starts immediately |

In the Desktop app, an approval card shows the name, phase list, and a token-usage caution with **Once**, **Always**, **Deny** actions. Your permission mode controls only the launch prompt — the subagents the workflow spawns always run in `acceptEdits` mode and inherit your [tool allowlist](https://code.claude.com/docs/en/settings), regardless of your session's mode, and file edits are auto-approved. Shell commands, web fetches, and MCP tools not in your allowlist can still prompt mid-run; add the commands the agents need to your allowlist before starting to avoid this on a long run.

### Save the workflow for reuse

Run `/workflows`, select the run, and press `s`. In the save dialog, `Tab` toggles between two locations: `.claude/workflows/` in your project (shared with everyone who clones the repo) or `~/.claude/workflows/` in your home directory (every project, visible only to you). Press Enter to save. The workflow then runs as `/<name>` in future sessions. If a project workflow and a personal workflow share a name, the project one runs.

### Pass input to a saved workflow

A saved workflow accepts input through the `args` parameter; the script reads it as a global named `args`. Use it to supply a research question, target paths, or a config object at invocation time:

```text theme={null}
> Run /triage-issues on issues 1024, 1025, and 1030
```

Claude passes the list as structured data, so the script can call array and object methods on `args` directly without parsing it first. If `args` is omitted, the global is `undefined`.

### Watch the run

Workflows run in the background, so the session stays responsive. Run `/workflows` to list running and completed workflows, then select one to open its progress view (each phase with its agent counts, token totals, and elapsed time). The footer key map: `↑`/`↓` select a phase or agent; `Enter` or `→` drill into a phase, then an agent, to read its prompt, recent tool calls, and result; `Esc` back out one level; `j`/`k` scroll within agent detail when it overflows; `p` pause or resume the run; `x` stop the selected agent (or the whole workflow when focus is on the run); `r` restart the selected running agent; `s` save the run's script as a command.

## Manage runs

Manage a run from the `/workflows` view or by expanding its progress line in the task panel below the input box.

**Resume after a pause** — If you stop a run, resume it: agents that already completed return their cached results, the rest run live. Resume from `/workflows` by selecting it and pressing `p`, or ask Claude to relaunch with the same script. Resume works only within the same session; if you exit Claude Code while a workflow is running, the next session starts it fresh.

**Cost** — A workflow spawns many agents, so a single run can use meaningfully more tokens than working through the task in conversation; runs count toward your plan's usage and rate limits. To gauge spend, run the workflow on a small slice first (one directory, a narrow question). The `/workflows` view shows each agent's token usage as the run progresses, and you can stop the run there without losing completed work; the runtime's agent caps bound a runaway script. Every agent uses your session's model unless the script routes a stage elsewhere: check `/model` before a large run, and ask Claude to use a smaller model for stages that don't need the strongest one. See [Manage costs](https://code.claude.com/docs/en/costs).

**Turn workflows off** — Workflows are available in the CLI, Desktop app, IDE extensions, non-interactive mode (`claude -p`), and the Agent SDK; the same disable settings apply on every surface. For yourself: toggle **Dynamic workflows** off in `/config`; set `"disableWorkflows": true` in `~/.claude/settings.json`; or set `CLAUDE_CODE_DISABLE_WORKFLOWS=1` (read at startup). For an organization, set `"disableWorkflows": true` in [managed settings](https://code.claude.com/docs/en/server-managed-settings) or use the admin-settings toggle. When disabled, the bundled workflow commands are unavailable, the `ultracode` keyword no longer triggers a run, and `ultracode` is removed from the `/effort` menu.

**Source**: https://code.claude.com/docs/en/workflows
**Last Updated**: 2026-06-13
**Status**: Active
