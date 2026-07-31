---
tags:
  - resource
  - documentation
  - hermes_agent
  - git_worktrees
  - parallel_agents
keywords:
  - git worktree isolation
  - parallel hermes agents
  - hermes -w automatic worktree
  - per-worktree checkpoint history
  - shadow repo hash
  - safe worktree cleanup
topics:
  - Hermes Agent
  - Git Worktrees
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/git-worktrees
access_control_group: ["general"]
---

# Git Worktree Isolation

## Overview

Git worktree isolation is the recommended way to run **multiple Hermes agents safely on the same repository** without duplicating the entire repo. Because Hermes treats the current working directory as the project root, two agents in the same checkout can interfere — one may delete or rewrite files the other is using, and it becomes hard to attribute changes to an experiment. A worktree gives each agent its own branch, its own working directory, and its own Checkpoint Manager `/rollback` history (keyed by a shadow-repo hash derived from the worktree path). You can create worktrees manually with `git worktree add`, or let Hermes create a disposable one automatically with the `hermes -w` flag.

## Why Use Worktrees with Hermes?

Hermes treats the **current working directory** as the project root:

- CLI: the directory where you run `hermes` or `hermes chat`
- Messaging gateways: the directory set by `terminal.cwd` in `~/.hermes/config.yaml`

If you run multiple agents in the **same checkout**, their changes can interfere with each other: one agent may delete or rewrite files the other is using, and it becomes harder to understand which changes belong to which experiment.

With worktrees, each agent gets:

- Its **own branch and working directory**
- Its **own Checkpoint Manager history** for `/rollback`

The two ways Hermes reads the project root are: CLI (the invocation directory) and messaging gateways (`terminal.cwd`). Checkpoints/`/rollback` detail is owned by SP03b (`hermes_checkpoints_rollback`).

## Quick Start: Creating a Worktree

From your main repository (containing `.git/`), create a new worktree for a feature branch:

```bash
# From the main repo root
cd /path/to/your/repo

# Create a new branch and worktree in ../repo-feature
git worktree add ../repo-feature feature/hermes-experiment
```

This creates a new directory (`../repo-feature`) and a new branch (`feature/hermes-experiment`) checked out in that directory. Now you can `cd` into the new worktree and run Hermes there:

```bash
cd ../repo-feature

# Start Hermes in the worktree
hermes
```

Hermes will see `../repo-feature` as the project root, use that directory for context files, code edits, and tools, and use a **separate checkpoint history** for `/rollback` scoped to this worktree.

## Running Multiple Agents in Parallel

You can create multiple worktrees, each with its own branch:

```bash
cd /path/to/your/repo

git worktree add ../repo-experiment-a feature/hermes-a
git worktree add ../repo-experiment-b feature/hermes-b
```

In separate terminals:

```bash
# Terminal 1
cd ../repo-experiment-a
hermes

# Terminal 2
cd ../repo-experiment-b
hermes
```

Each Hermes process works on its own branch (`feature/hermes-a` vs `feature/hermes-b`), writes checkpoints under a different shadow repo hash (derived from the worktree path), and can use `/rollback` independently without affecting the other. This is especially useful when running batch refactors, trying different approaches to the same task, or pairing CLI + gateway sessions against the same upstream repo.

## Cleaning Up Worktrees Safely

When you are done with an experiment:

1. Decide whether to keep or discard the work.
2. If you want to keep it: merge the branch into your main branch as usual.
3. Remove the worktree:

```bash
cd /path/to/your/repo

# Remove the worktree directory and its reference
git worktree remove ../repo-feature
```

Notes:

- `git worktree remove` will refuse to remove a worktree with uncommitted changes unless you force it.
- Removing a worktree does **not** automatically delete the branch; you can delete or keep the branch using normal `git branch` commands.
- Hermes checkpoint data under `~/.hermes/checkpoints/` is not automatically pruned when you remove a worktree, but it is usually very small.

## Best Practices

- **One worktree per Hermes experiment** — create a dedicated branch/worktree for each substantial change; this keeps diffs focused and PRs small and reviewable.
- **Name branches after the experiment** — e.g. `feature/hermes-checkpoints-docs`, `feature/hermes-refactor-tests`.
- **Commit frequently** — use git commits for high-level milestones; use checkpoints and `/rollback` as a safety net for tool-driven edits in between.
- **Avoid running Hermes from the bare repo root when using worktrees** — prefer the worktree directories instead, so each agent has a clear scope.

## Using `hermes -w` (Automatic Worktree Mode)

Hermes has a built-in `-w` flag that **automatically creates a disposable git worktree** with its own branch. You don't need to set up worktrees manually — just `cd` into your repo and run:

```bash
cd /path/to/your/repo
hermes -w

# Or combine it with a single query
hermes -w -z "Fix issue #123"
```

Hermes will create a temporary worktree under `.worktrees/` inside your repo, check out an isolated branch (e.g. `hermes/hermes-<hash>`), and run the full CLI session inside that worktree. This is the easiest way to get worktree isolation. For parallel agents, open multiple terminals and run `hermes -w` in each — every invocation gets its own worktree and branch automatically.

## Putting It All Together

- Use **git worktrees** to give each Hermes session its own clean checkout.
- Use **branches** to capture the high-level history of your experiments.
- Use **checkpoints + `/rollback`** to recover from mistakes inside each worktree.

This combination gives strong guarantees that different agents and experiments do not step on each other, fast iteration cycles with easy recovery from bad edits, and clean, reviewable pull requests.

**Source**: `inbox/hermes_agent_docs/user-guide/git-worktrees.md` · https://hermes-agent.nousresearch.com/docs/user-guide/git-worktrees
**Last Updated**: 2026-06-19
**Status**: Active
