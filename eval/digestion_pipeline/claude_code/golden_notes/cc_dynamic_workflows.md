---
tags:
  - resource
  - documentation
  - claude_code
  - workflows
  - orchestration
keywords:
  - dynamic workflow
  - orchestrate subagents at scale
  - who holds the plan
  - script variables
  - deep-research
  - repeatable quality pattern
  - agent caps
  - isolated runtime
topics:
  - Claude Code
  - Workflows
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/workflows
access_control_group: ["general"]
---

# Dynamic Workflows — Orchestrate Subagents at Scale

## Overview

A **dynamic workflow** is a JavaScript script that orchestrates [subagents](../../term_dictionary/term_subagent.md) at scale. Claude writes the script for the task you describe, and a runtime executes it in the background while your session stays responsive. Reach for a workflow when a task needs more agents than one conversation can coordinate, or when you want the orchestration codified as a script you can read and rerun — examples include a codebase-wide bug sweep, a 500-file migration, a research question that needs sources cross-checked against each other, and a hard plan worth drafting from several independent angles before you commit to one.

The defining distinction among subagents, skills, agent teams, and workflows is **who holds the plan**. With subagents, skills, and agent teams, Claude is the orchestrator deciding turn by turn what to spawn next, and every result lands in a context window; a workflow moves the plan into code, so the script holds the loop, the branching, and the intermediate results, and Claude's context holds only the final answer. Dynamic workflows require Claude Code v2.1.154 or later and are available on all paid plans, with Anthropic API access, and on Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry. On Pro, you turn them on from the Dynamic workflows row in `/config`. For how to write, approve, save, and operate a workflow, see [cc_create_and_run_workflows](cc_create_and_run_workflows.md).

## When to Use a Workflow

[Subagents](../../term_dictionary/term_subagent.md), skills, agent teams, and workflows can all run a multi-step task. The difference is who holds the plan:

|                                  | Subagents                      | Skills                       | Agent teams                            | Workflows                            |
| :------------------------------- | :----------------------------- | :--------------------------- | :------------------------------------- | :----------------------------------- |
| What it is                       | A worker Claude spawns         | Instructions Claude follows  | A lead agent supervising peer sessions | A script the runtime executes        |
| Who decides what runs next       | Claude, turn by turn           | Claude, following the prompt | The lead agent, turn by turn           | The script                           |
| Where intermediate results live  | Claude's context window        | Claude's context window      | A shared task list                     | Script variables                     |
| What's repeatable                | The worker definition          | The instructions             | The team definition                    | The orchestration itself             |
| Scale                            | A few delegated tasks per turn | Same as subagents            | A handful of long-running peers        | Dozens to hundreds of agents per run |
| Interruption                     | Restarts the turn              | Restarts the turn            | Teammates keep running                 | Resumable in the same session        |

A workflow moves the plan into code. With subagents, skills, and agent teams, Claude is the orchestrator: it decides turn by turn what to spawn or assign next, and every result lands in a context window. A workflow script holds the loop, the branching, and the intermediate results itself, so Claude's context holds only the final answer.

Moving the plan into code also lets a workflow apply a **repeatable quality pattern**, not just run more agents: it can have independent agents adversarially review each other's findings before they're reported, or draft a plan from several angles and weigh them against each other, so you get a more trustworthy result than a single pass.

## Run a Bundled Workflow

The quickest way to see a workflow in action is to run `/deep-research`, the built-in workflow Claude Code includes for investigating a question across many sources. You'll see agents work through a set of phases in the background while your session stays free, and get one report at the end instead of a turn-by-turn transcript. The high-level run/approve/watch/read steps are documented in [cc_create_and_run_workflows](cc_create_and_run_workflows.md); the bundled workflow itself is described below.

### Bundled Workflows

Claude Code includes `/deep-research` as a built-in workflow:

| Command                     | What it does                                                                                                                                                                                                                                                            |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/deep-research <question>` | Fans out web searches on a question across several angles, fetches and cross-checks the sources it finds, votes on each claim, and returns a cited report with claims that didn't survive cross-checking filtered out. Requires the WebSearch tool to be available |

Workflows you save yourself become commands the same way and appear in `/` autocomplete alongside the bundled ones (see [cc_create_and_run_workflows](cc_create_and_run_workflows.md) for saving).

## How a Workflow Runs

The workflow runtime executes the script in an **isolated environment, separate from your conversation**. Intermediate results stay in script variables instead of landing in Claude's [context window](../../term_dictionary/term_context_window.md).

Every run writes its script to a file under your session's directory in `~/.claude/projects/`. Claude receives the path when the run starts, so you can ask for it. You can open that file to read the orchestration Claude wrote, diff it against a previous run's script, or edit it and ask Claude to relaunch from the edited version. The runtime tracks each agent's result as the run progresses, which is what makes a run resumable within the same session.

### Behavior and Limits

The runtime applies the following constraints:

| Constraint                                                           | Why                                                                                                            |
| :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------- |
| No mid-run user input                                                | Only agent permission prompts can pause a run. For sign-off between stages, run each stage as its own workflow |
| No direct filesystem or shell access from the workflow itself        | Agents read, write, and run commands. The script coordinates the agents                                        |
| Up to 16 concurrent agents, fewer on machines with limited CPU cores | Bounds local resource use                                                                                      |
| 1,000 agents total per run                                           | Prevents runaway loops                                                                                         |

**Source**: https://code.claude.com/docs/en/workflows
**Last Updated**: 2026-06-13
**Status**: Active
