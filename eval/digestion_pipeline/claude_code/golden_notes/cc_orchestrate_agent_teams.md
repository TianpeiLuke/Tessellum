---
tags:
  - resource
  - documentation
  - claude_code
  - agent_teams
  - orchestration
keywords:
  - orchestrate agent teams
  - team lead
  - shared task list
  - assign and claim tasks
  - display mode
  - plan approval
  - clean up the team
  - subagent definitions for teammates
  - quality gate hooks
topics:
  - Claude Code
  - Agent Teams
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-teams
access_control_group: ["general"]
---

# Orchestrate Agent Teams in Claude Code

## Overview

This is the operating manual for running an agent team — a set of Claude Code instances where one session is the **team lead** that spawns and coordinates **teammates** working in parallel. Because agent teams are experimental and disabled by default, the workflow begins by enabling them, then driving the lead entirely in natural language: it handles team creation, task assignment, and delegation based on your instructions. The concept-level "what/why/architecture" treatment lives in [`cc_agent_teams_overview`](cc_agent_teams_overview.md); this note covers enabling, starting, controlling (display modes, models, plan approval, messaging, task assignment, shutdown, cleanup, quality-gate hooks), reusing subagent definitions, permissions, the use-case prompts, best practices, and troubleshooting.

Agent teams require Claude Code v2.1.32 or later (`claude --version`).

## Enable agent teams

Agent teams are disabled by default. Enable them by setting `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to `1`, either in your shell environment or through `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Start your first agent team

After enabling, tell Claude to create an agent team and describe the task and team structure in natural language. Claude creates the team, spawns teammates, and coordinates work based on your prompt. There are two ways teams get started:

- **You request a team**: give Claude a task that benefits from parallel work and explicitly ask for an agent team.
- **Claude proposes a team**: if Claude determines your task would benefit from parallel work, it may suggest creating one. You confirm before it proceeds.

In both cases you stay in control — Claude won't create a team without your approval. An example that works well because the three roles are independent and can explore without waiting on each other:

```text
I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
```

Claude then creates a team with a shared task list, spawns teammates, has them explore, synthesizes findings, and attempts to clean up when finished. The lead's terminal lists all teammates and what they're working on. Use **Shift+Down** to cycle through teammates and message them directly; after the last teammate, Shift+Down wraps back to the lead.

## Control your agent team

Tell the lead what you want in natural language; it handles coordination, task assignment, and delegation.

### Choose a display mode

Two display modes are supported:

- **In-process**: all teammates run inside your main terminal. Use Shift+Down to cycle through teammates and type to message them directly. Works in any terminal, no extra setup.
- **Split panes**: each teammate gets its own pane so you can see everyone's output at once and click into a pane to interact. Requires `tmux` or iTerm2.

The default is `"auto"`, which uses split panes if you're already in a tmux session or your terminal is iTerm2, and in-process otherwise. The `"tmux"` setting enables split-pane mode and auto-detects tmux vs iTerm2. Override via `teammateMode` in `~/.claude/settings.json` (e.g. `"teammateMode": "in-process"`), or force in-process for a single session:

```bash
claude --teammate-mode in-process
```

Split-pane mode requires either tmux or iTerm2 with the `it2` CLI. Install tmux through your system package manager; for iTerm2 install the `it2` CLI then enable the Python API in **iTerm2 → Settings → General → Magic → Enable Python API**. (`tmux -CC` in iTerm2 is the suggested tmux entrypoint.)

### Specify teammates and models

Claude decides how many teammates to spawn based on your task, or you can specify exactly what you want, including the model per teammate:

```text
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

Teammates don't inherit the lead's `/model` selection by default. To change the model used when the prompt doesn't specify one, set **Default teammate model** in `/config`. Pick **Default (leader's model)** to have teammates follow the lead's current model.

### Require plan approval for teammates

For complex or risky tasks, require teammates to plan before implementing. The teammate works in read-only plan mode until the lead approves: e.g. "Spawn an architect teammate to refactor the authentication module. Require plan approval before they make any changes." When a teammate finishes planning, it sends a plan-approval request to the lead, which approves it or rejects it with feedback; if rejected, the teammate stays in plan mode, revises, and resubmits. The lead makes approval decisions autonomously — to influence its judgment, give criteria in your prompt (e.g. "only approve plans that include test coverage").

### Talk to teammates directly

Each teammate is a full, independent Claude Code session you can message directly to add instructions, ask follow-ups, or redirect:

- **In-process mode**: Shift+Down to cycle through teammates, then type to send a message. Press Enter to view a teammate's session, Escape to interrupt its current turn, Ctrl+T to toggle the task list.
- **Split-pane mode**: click into a teammate's pane to interact with its session directly.

### Assign and claim tasks

The shared task list coordinates work. The lead creates tasks; teammates work through them. Tasks have three states — **pending, in progress, completed** — and can depend on other tasks: a pending task with unresolved dependencies cannot be claimed until those dependencies complete. Work is distributed two ways:

- **Lead assigns**: tell the lead which task to give to which teammate.
- **Self-claim**: after finishing a task, a teammate picks up the next unassigned, unblocked task on its own.

Task claiming uses **file locking** to prevent race conditions when multiple teammates try to claim the same task simultaneously.

### Shut down teammates

To gracefully end a teammate's session, refer to it by name (e.g. "Ask the researcher teammate to shut down"). The lead sends a shutdown request; the teammate can approve and exit gracefully, or reject with an explanation.

### Clean up the team

When done, ask the lead to clean up (e.g. "Clean up the team"). This removes the shared team resources. When the lead runs cleanup, it checks for active teammates and **fails if any are still running**, so shut them down first. Claude often cleans up on its own when the work is done, so a later cleanup request may report nothing to clean up. **Always use the lead to clean up** — teammates should not run cleanup because their team context may not resolve correctly, potentially leaving resources inconsistent.

### Enforce quality gates with hooks

Use hooks to enforce rules when teammates finish work or tasks change state (full hooks reference at https://code.claude.com/docs/en/hooks):

- `TeammateIdle`: runs when a teammate is about to go idle. Exit with code 2 to send feedback and keep the teammate working.
- `TaskCreated`: runs when a task is being created. Exit with code 2 to prevent creation and send feedback.
- `TaskCompleted`: runs when a task is being marked complete. Exit with code 2 to prevent completion and send feedback.

## Use subagent definitions for teammates

When spawning a teammate, you can reference a [subagent](https://code.claude.com/docs/en/sub-agents) type from any subagent scope (project, user, plugin, or CLI-defined). This lets you define a role once — e.g. a security-reviewer or test-runner — and reuse it both as a delegated subagent and as a teammate. Mention it by name (e.g. "Spawn a teammate using the security-reviewer agent type to audit the auth module"). The teammate honors that definition's `tools` allowlist and `model`, and the definition's body is **appended** to the teammate's system prompt as additional instructions rather than replacing it. Team coordination tools such as `SendMessage` and the task-management tools are always available even when `tools` restricts other tools. Note: the `skills` and `mcpServers` frontmatter fields are **not** applied when a definition runs as a teammate — teammates load skills and MCP servers from project and user settings, like a regular session.

## Permissions

Teammates start with the lead's permission settings. If the lead runs with `--dangerously-skip-permissions`, all teammates do too. After spawning, you can change individual teammate modes, but you **cannot set per-teammate modes at spawn time**.

## Use case examples

**Run a parallel code review** — assign each reviewer a distinct lens so they don't overlap; the lead synthesizes across all three after they finish:

```text
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

**Investigate with competing hypotheses** — make teammates explicitly adversarial so each investigates its own theory and challenges the others', countering the anchoring bias of sequential investigation:

```text
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

The theory that survives multiple independent investigators trying to disprove each other is much more likely to be the actual root cause.

## Best practices

- **Give teammates enough context**: teammates load project context automatically (CLAUDE.md, MCP servers, skills) but don't inherit the lead's conversation history, so include task-specific details in the spawn prompt.
- **Choose an appropriate team size**: no hard limit, but token costs scale linearly, coordination overhead increases, and there are diminishing returns. Start with **3-5 teammates** for most workflows. Having **5-6 tasks per teammate** keeps everyone productive without excessive context switching (15 independent tasks → 3 teammates is a good start). Three focused teammates often outperform five scattered ones.
- **Size tasks appropriately**: too small wastes coordination overhead; too large risks long stretches without check-ins; "just right" is a self-contained unit producing a clear deliverable (a function, a test file, a review). If the lead isn't creating enough tasks, ask it to split the work smaller.
- **Wait for teammates to finish**: if the lead starts implementing itself, tell it "Wait for your teammates to complete their tasks before proceeding."
- **Start with research and review**: clear-boundary, no-code tasks (review a PR, research a library, investigate a bug) show the value of parallel exploration without parallel-implementation coordination challenges.
- **Avoid file conflicts**: break work so each teammate owns a different set of files; two teammates editing the same file leads to overwrites.
- **Monitor and steer**: check progress, redirect approaches that aren't working, and synthesize findings as they arrive — running unattended too long increases the risk of wasted effort.

## Troubleshooting

- **Teammates not appearing**: in in-process mode they may be running but not visible — press Shift+Down to cycle. Confirm the task was complex enough to warrant a team. For split panes, ensure tmux is installed (`which tmux`); for iTerm2 verify the `it2` CLI is installed and the Python API is enabled.
- **Too many permission prompts**: teammate requests bubble up to the lead. Pre-approve common operations in your permission settings before spawning to reduce interruptions.
- **Teammates stopping on errors**: check their output (Shift+Down or clicking the pane), then give additional instructions or spawn a replacement teammate.
- **Lead shuts down before work is done**: tell it to keep going; you can also tell it to wait for teammates before proceeding.
- **Orphaned tmux sessions**: if a tmux session persists after the team ends, list with `tmux ls` and end it with `tmux kill-session -t <session-name>`.

**Source**: https://code.claude.com/docs/en/agent-teams
**Last Updated**: 2026-06-13
**Status**: Active
