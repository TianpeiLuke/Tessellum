---
tags:
  - resource
  - documentation
  - claude_code
  - agent_teams
  - multi_agent
keywords:
  - agent teams
  - team lead and teammates
  - shared task list
  - mailbox messaging
  - compare subagents agent teams
  - experimental disabled by default
  - independent context window
  - token usage scales
topics:
  - Claude Code
  - Agent Teams
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-teams
access_control_group: ["general"]
---

# Claude Code — Agent Teams Overview

## Overview

**Agent teams** let you coordinate multiple Claude Code instances working together. One session acts as the **team lead** — coordinating work, assigning tasks, and synthesizing results — while **teammates** work independently, each in its own context window, and communicate directly with each other. Unlike subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead.

Agent teams are **experimental and disabled by default**. You enable them by adding `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to your `settings.json` or environment. They require Claude Code v2.1.32 or later (check with `claude --version`) and have known limitations around session resumption, task coordination, and shutdown behavior. This note covers what agent teams are, when to use them, how they compare to subagents, and their architecture, communication model, token cost, and current limitations. For the operating procedure (enabling, starting, and controlling a team), see [Orchestrate Agent Teams](cc_orchestrate_agent_teams.md).

## When to Use Agent Teams

Agent teams are most effective for tasks where parallel exploration adds real value. The strongest use cases are:

- **Research and review**: multiple teammates can investigate different aspects of a problem simultaneously, then share and challenge each other's findings.
- **New modules or features**: teammates can each own a separate piece without stepping on each other.
- **Debugging with competing hypotheses**: teammates test different theories in parallel and converge on the answer faster.
- **Cross-layer coordination**: changes that span frontend, backend, and tests, each owned by a different teammate.

Agent teams add coordination overhead and use significantly more tokens than a single session. They work best when teammates can operate independently. For sequential tasks, same-file edits, or work with many dependencies, a single session or [subagents](https://code.claude.com/docs/en/sub-agents) are more effective.

### Compare with Subagents

Both agent teams and subagents let you parallelize work, but they operate differently. The deciding question is whether your workers need to communicate with each other. Subagents only report results back to the main agent and never talk to each other; in agent teams, teammates share a task list, claim work, and communicate directly.

|                   | Subagents                                        | Agent teams                                         |
| :---------------- | :----------------------------------------------- | :-------------------------------------------------- |
| **Context**       | Own context window; results return to the caller | Own context window; fully independent               |
| **Communication** | Report results back to the main agent only       | Teammates message each other directly               |
| **Coordination**  | Main agent manages all work                      | Shared task list with self-coordination             |
| **Best for**      | Focused tasks where only the result matters      | Complex work requiring discussion and collaboration |
| **Token cost**    | Lower: results summarized back to main context   | Higher: each teammate is a separate Claude instance |

Use subagents when you need quick, focused workers that report back. Use agent teams when teammates need to share findings, challenge each other, and coordinate on their own.

## How Agent Teams Work

### Architecture

An agent team consists of four components:

| Component     | Role                                                                                       |
| :------------ | :----------------------------------------------------------------------------------------- |
| **Team lead** | The main Claude Code session that creates the team, spawns teammates, and coordinates work |
| **Teammates** | Separate Claude Code instances that each work on assigned tasks                            |
| **Task list** | Shared list of work items that teammates claim and complete                                |
| **Mailbox**   | Messaging system for communication between agents                                          |

Teammate messages arrive at the lead automatically. The system manages task dependencies automatically: when a teammate completes a task that other tasks depend on, blocked tasks unblock without manual intervention.

Teams and tasks are stored locally — team config at `~/.claude/teams/{team-name}/config.json` and the task list at `~/.claude/tasks/{team-name}/`. Claude Code generates both automatically when you create a team and updates them as teammates join, go idle, or leave. Both directories exist only while the team is active; they are removed when the team is cleaned up or when the session ends. The team config holds runtime state such as session IDs and tmux pane IDs, so don't edit it by hand or pre-author it — changes are overwritten on the next state update. The config contains a `members` array with each teammate's name, agent ID, and agent type, which teammates can read to discover other team members. There is no project-level equivalent: a file like `.claude/teams/teams.json` in your project directory is treated as an ordinary file, not configuration. To define reusable teammate roles, use subagent definitions instead (see [Orchestrate Agent Teams](cc_orchestrate_agent_teams.md)).

### Context and Communication

Each teammate has its own context window. When spawned, a teammate loads the same project context as a regular session — CLAUDE.md, MCP servers, and skills — plus the spawn prompt from the lead. The lead's conversation history does not carry over.

Teammates share information through several mechanisms:

- **Automatic message delivery**: when teammates send messages, they're delivered automatically to recipients. The lead doesn't need to poll for updates.
- **Idle notifications**: when a teammate finishes and stops, it automatically notifies the lead.
- **Shared task list**: all agents can see task status and claim available work.
- **Teammate messaging**: send a message to one specific teammate by name. To reach everyone, send one message per recipient.

The lead assigns every teammate a name when it spawns them, and any teammate can message any other by that name. To get predictable names you can reference in later prompts, tell the lead what to call each teammate in your spawn instruction.

### Token Usage

Agent teams use significantly more tokens than a single session. Each teammate has its own context window, and token usage scales with the number of active teammates. For research, review, and new feature work, the extra tokens are usually worthwhile; for routine tasks, a single session is more cost-effective. See the [agent team token costs](https://code.claude.com/docs/en/costs) guidance for usage detail.

## Limitations

Agent teams are experimental. Current limitations to be aware of:

- **No session resumption with in-process teammates**: `/resume` and `/rewind` do not restore in-process teammates. After resuming a session, the lead may attempt to message teammates that no longer exist; if this happens, tell the lead to spawn new teammates.
- **Task status can lag**: teammates sometimes fail to mark tasks as completed, which blocks dependent tasks. If a task appears stuck, check whether the work is actually done and update the task status manually or tell the lead to nudge the teammate.
- **Shutdown can be slow**: teammates finish their current request or tool call before shutting down, which can take time.
- **One team at a time**: a lead can only manage one team. Clean up the current team before creating a new one.
- **No nested teams**: teammates cannot spawn their own teams or teammates. Only the lead can manage the team.
- **Lead is fixed**: the session that creates the team is the lead for its lifetime. You can't promote a teammate to lead or transfer leadership.
- **Permissions set at spawn**: all teammates start with the lead's permission mode. You can change individual teammate modes after spawning, but you can't set per-teammate modes at spawn time.
- **Split panes require tmux or iTerm2**: the default in-process mode works in any terminal. Split-pane mode isn't supported in VS Code's integrated terminal, Windows Terminal, or Ghostty.

CLAUDE.md works normally — teammates read CLAUDE.md files from their working directory, so you can use it to provide project-specific guidance to all teammates.

**Source**: https://code.claude.com/docs/en/agent-teams
**Last Updated**: 2026-06-13
**Status**: Active
