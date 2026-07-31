---
tags:
  - resource
  - documentation
  - claude_code
  - ci_cd
  - cloud_planning
keywords:
  - ultraplan
  - cloud plan mode
  - claude code on the web
  - teleport back to terminal
  - plan review browser
  - inline comments plan
  - execute on the web
  - research preview
topics:
  - Claude Code
  - CI/CD
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/ultraplan
access_control_group: ["general"]
---

# Plan in the Cloud with ultraplan

## Overview

**ultraplan** hands a planning task from your local Claude Code CLI to a [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) session running in [plan mode](https://code.claude.com/docs/en/permission-modes). Claude drafts the plan in the cloud while your terminal stays free; when the plan is ready you open it in your browser to comment on specific sections, ask for revisions, and choose where to execute. It is useful when you want a richer review surface than the terminal — targeted per-section feedback, hands-off drafting, and flexible execution (run on the web and open a PR, or send the plan back to your terminal).

ultraplan is in **research preview** and requires Claude Code v2.1.91 or later; behavior may change based on feedback. It requires a Claude Code on the web account and a GitHub repository, and because it runs on Anthropic's cloud infrastructure it is **not available** on Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry. The cloud session runs in your account's default cloud environment; if you don't have one yet, ultraplan creates one automatically on first launch.

## Launch ultraplan from the CLI

From a local CLI session you can launch ultraplan three ways:

- **Command** — run `/ultraplan` followed by your prompt.
- **Keyword** — include the word `ultraplan` anywhere in a normal prompt.
- **From a local plan** — when Claude finishes a local plan and shows the approval dialog, choose **No, refine with Ultraplan on Claude Code on the web** to send the draft to the cloud for further iteration.

For example, to plan a service migration with the command:

```
/ultraplan migrate the auth service from sessions to JWTs
```

The command and keyword paths open a confirmation dialog before launching; the local-plan path skips it because that selection already serves as confirmation. If [Remote Control](https://code.claude.com/docs/en/remote-control) is active, it disconnects when ultraplan starts because both features occupy the claude.ai/code interface and only one can be connected at a time.

After the cloud session launches, the CLI prompt input shows a status indicator while the cloud session works:

| Status | Meaning |
| :--- | :--- |
| `◇ ultraplan` | Claude is researching your codebase and drafting the plan |
| `◇ ultraplan needs your input` | Claude has a clarifying question; open the session link to respond |
| `◆ ultraplan ready` | The plan is ready to review in your browser |

Run `/tasks` and select the ultraplan entry to open a detail view with the session link, agent activity, and a **Stop ultraplan** action. Stopping archives the cloud session and clears the indicator; nothing is saved to your terminal.

## Review and revise the plan in your browser

When the status changes to `◆ ultraplan ready`, open the session link to view the plan on claude.ai. It appears in a dedicated review view with:

- **Inline comments** — highlight any passage and leave a comment for Claude to address.
- **Emoji reactions** — react to a section to signal approval or concern without writing a full comment.
- **Outline sidebar** — jump between sections of the plan.

When you ask Claude to address your comments, it revises the plan and presents an updated draft. You can iterate as many times as needed before choosing where to execute.

## Choose where to execute

When the plan looks right, you choose from the browser whether Claude implements it in the same cloud session or sends it back to your waiting terminal.

### Execute on the web

Select **Approve Claude's plan and start coding** in your browser to have Claude implement it in the same Claude Code on the web session. Your terminal shows a confirmation, the status indicator clears, and the work continues in the cloud. When implementation finishes, review the diff and create a pull request from the web interface.

### Send the plan back to your terminal

Select **Approve plan and teleport back to terminal** to implement the plan locally with full access to your environment. This option appears when the session was launched from your CLI and the terminal is still polling; the web session is archived so it doesn't continue working in parallel. Your terminal shows the plan in a dialog titled **Ultraplan approved** with three options:

- **Implement here** — inject the plan into your current conversation and continue from where you left off.
- **Start new session** — clear the current conversation and begin fresh with only the plan as context.
- **Cancel** — save the plan to a file without executing it; Claude prints the file path so you can return to it later.

If you start a new session, Claude prints a `claude --resume` command at the top so you can return to your previous conversation later.

**Source**: https://code.claude.com/docs/en/ultraplan
**Last Updated**: 2026-06-13
**Status**: Active
