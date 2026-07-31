---
tags:
  - resource
  - documentation
  - claude_code
  - parallelism
  - comparison
keywords:
  - run agents in parallel
  - subagents vs agent teams
  - agent view
  - dynamic workflows
  - who coordinates the work
  - check on running work
  - worktrees
  - mcp server
topics:
  - Claude Code
  - Parallelism
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agents
access_control_group: ["general"]
---

# Run Agents in Parallel

## Overview

Claude Code can take on multiple tasks at once through four approaches that parallelize work in different ways: **subagents**, **agent view**, **agent teams**, and **dynamic workflows**. The right one depends on whether you want to stay in each conversation yourself, hand tasks off and check back later, or have Claude coordinate a group of workers for you. In every approach the workers are Claude sessions; to involve a different tool, you expose it to Claude as an MCP server. Two more tools — worktrees and `/batch` — support this work without being a way to run agents themselves.

This note is the comparison hub: it lays out what each approach gives you, how to choose between them along three axes, and which command checks on each kind of running work. Each approach has its own home guide for setup and configuration.

## The Four Approaches

| Approach | What it gives you | Use it when |
| :--- | :--- | :--- |
| Subagents | Delegated workers inside one session that do a side task in their own context and return a summary | A side task would flood your main conversation with search results, logs, or file contents you won't reference again |
| Agent view | One screen to dispatch and monitor sessions running in the background, opened with `claude agents`. Research preview | You have several independent tasks and want to hand them off, check status at a glance, and step in only when one needs you |
| Agent teams | Multiple coordinated sessions with a shared task list and inter-agent messaging, managed by a lead. Experimental and disabled by default | You want Claude to split a project into pieces, assign them, and keep the workers in sync |
| Dynamic workflows | A script that runs many subagents and cross-checks their results, for work too big to coordinate one turn at a time or that needs more than a single pass | A job outgrows a handful of subagents, or you want findings verified against each other: a codebase-wide audit, a 500-file migration, cross-checked research, or a plan drafted from several angles |

In every approach the workers are Claude sessions. To involve a different tool, expose it to Claude as an MCP server.

### Supporting tools (not coordination styles)

- **Worktrees** give each session a separate git checkout, so parallel sessions never edit the same files. Use them for sessions you run yourself. Agent view moves each dispatched session into its own worktree automatically, and subagents you spawn can each get one too.
- **`/batch`** is a skill that has Claude split one large change into 5 to 30 worktree-isolated subagents that each open a pull request. It's a packaged use of subagents and worktrees, not a separate coordination style.

A few other features run Claude without you driving each step, but they solve a different problem than splitting work across agents: a background bash command runs one shell command without blocking the conversation (it doesn't spawn an agent); a forked subagent is a subagent that inherits your full conversation context instead of starting fresh (a way to spawn a subagent, not a separate surface); and a routine runs a session on a schedule in Anthropic's cloud, not in parallel on your machine.

> Running several sessions or subagents at once multiplies token usage. See Costs for usage and rate-limit details.

## Choose an Approach

The right approach depends on who coordinates the work, whether the workers need to communicate, and whether they edit the same files:

- **Who coordinates the work?**
  - Claude delegates and collects results inside one conversation: subagents
  - You hand off independent tasks and check back later: agent view
  - Claude plans, assigns, and supervises a group of workers: agent teams (experimental and disabled by default)
  - A script holds the plan instead of Claude's turn-by-turn judgment: dynamic workflows
- **Do the workers need to talk to each other?** Subagents report results back to the conversation that spawned them, and agent view sessions report only to you. Teammates in an agent team share a task list and message each other directly.
- **Do the tasks touch the same files?** Isolate the work with worktrees. Subagents and sessions you run yourself can each use a separate worktree. Agent teams don't isolate teammates in worktrees, so partition the work so each teammate owns a different set of files.

## Check on Running Work

The command for checking on running work depends on which approach you used:

- For **background sessions**, `claude agents` opens agent view: one screen showing every session, its state, and which ones need your input.
- For **subagents in the current session**, `/agents` opens a panel with a **Running** tab listing live subagents and a **Library** tab where you create and edit custom subagents. Despite the similar name, this is separate from `claude agents`.
- For **anything running in the background of the current session**, `/tasks` lists each item and lets you check on, attach to, or stop it.
- For **dynamic workflows**, `/workflows` lists running and completed runs, the phase each is in, and how many agents have finished.

For a desktop view of all your sessions, see parallel sessions in the desktop app.

## Learn More

Each guide covers setup and configuration for one approach:

- Create custom subagents: define reusable specialists and control which tools they can use ([cc_subagents_overview](cc_subagents_overview.md)).
- Manage agents with agent view: dispatch sessions, watch their state, and attach when one needs you ([cc_agent_view_monitor](cc_agent_view_monitor.md)).
- Orchestrate agent teams: set up a lead and teammates, assign tasks, and review their work ([cc_agent_teams_overview](cc_agent_teams_overview.md)).
- Orchestrate dynamic workflows: run a bundled workflow or have Claude write one that runs many subagents and verifies their findings against each other (https://code.claude.com/docs/en/workflows).
- Run parallel sessions with worktrees: start Claude in an isolated checkout, control what gets copied in, and clean up afterward (https://code.claude.com/docs/en/worktrees).

**Source**: https://code.claude.com/docs/en/agents
**Last Updated**: 2026-06-13
**Status**: Active
