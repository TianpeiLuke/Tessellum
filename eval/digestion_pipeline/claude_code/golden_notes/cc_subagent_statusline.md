---
tags:
  - resource
  - documentation
  - claude_code
  - statusline
  - subagent
keywords:
  - subagentStatusLine
  - agent panel
  - subagent status line
  - tasks array
  - per-row override
  - disableAllHooks
  - plugin default
topics:
  - Claude Code
  - Status Line
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/statusline
access_control_group: ["general"]
---

# Claude Code — Subagent Status Lines

## Overview

The `subagentStatusLine` setting renders a **custom row body for each subagent** shown in the agent panel below the prompt. It replaces the default `name · description · token count` row with formatting your own command produces. Like the main `statusLine`, it is a shell command that Claude Code runs and whose output it displays — but instead of a single status bar, it drives one row per visible subagent.

The command runs once per refresh tick with **all visible subagent rows passed as a single JSON object on stdin**, and your script emits **one JSON line per row it wants to override**. It is governed by the same trust and `disableAllHooks` gates as `statusLine`, and plugins can ship a default.

## The `subagentStatusLine` setting

Configure it as a `"command"`-type setting, exactly like `statusLine`:

```json
{
  "subagentStatusLine": {
    "type": "command",
    "command": "~/.claude/subagent-statusline.sh"
  }
}
```

When configured, it overrides the default agent-panel row rendering with whatever your command produces.

## Per-tick input JSON

The command runs once per refresh tick. All visible subagent rows are passed as a single JSON object on stdin. The input includes the [base hook fields](https://code.claude.com/docs/en/hooks#common-input-fields) plus:

- `columns` — the usable row width.
- `tasks` — an array, where each task carries `id`, `name`, `type`, `status`, `description`, `label`, `startTime`, `tokenCount`, `tokenSamples`, and `cwd`.

So a single invocation receives the full set of currently-visible subagent rows at once, not one invocation per row.

## Output contract: one JSON line per overridden row

Write **one JSON line to stdout per row you want to override**, in the form:

```json
{"id": "<task id>", "content": "<row body>"}
```

The `content` string is rendered as-is, including ANSI colors and OSC 8 hyperlinks. The output contract is selective:

- **Omit a task's `id`** to keep the default rendering for that row.
- **Emit an empty `content` string** to hide that row.

## Trust gates and plugin defaults

The **same trust and `disableAllHooks` gates that apply to `statusLine` apply here** — because `subagentStatusLine` also executes a shell command, it requires the workspace-trust acceptance, and setting `disableAllHooks` to `true` disables it.

Plugins can ship a default `subagentStatusLine` in their [`settings.json`](https://code.claude.com/docs/en/plugins-reference#standard-plugin-layout).

**Source**: https://code.claude.com/docs/en/statusline
**Last Updated**: 2026-06-13
**Status**: Active
