---
tags:
  - resource
  - terminology
  - agentic_ai
  - software_development
  - version_control
keywords:
  - git worktree agents
  - parallel agents
  - isolated checkout
  - git worktree
  - hermes -w
  - worktree isolation
topics:
  - agentic AI
  - version control
  - parallel agent execution
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Git Worktree Agents - Parallel Coding Agents via Isolated Git Worktrees

## Definition

**Git worktree agents** is the pattern of running multiple autonomous coding agents safely on the *same* git repository by giving each agent its own **git worktree** — a separate checked-out working directory and branch that shares the single underlying `.git` object store. A git worktree (`git worktree add <path> <branch>`) creates a linked working tree with its own private `HEAD` and `index` while reusing the repository's shared objects and refs, so two agents never overwrite each other's files or fight over a single checkout. The pattern is the standard isolation primitive for parallel agent execution: each agent operates inside a clean, branch-scoped directory and can be merged, discarded, or rolled back independently of its siblings.

In agent harnesses such as Hermes Agent, the current working directory is treated as the project root, so a per-agent worktree directly scopes the agent's file edits, terminal commands, context files, and — critically — its checkpoint/rollback history. Hermes derives a per-worktree shadow-repo hash from the worktree path, giving each parallel agent an independent `/rollback` timeline. Hermes also exposes `hermes -w` (automatic worktree mode), which creates a disposable worktree with an isolated branch under `.worktrees/` so a user need not set worktrees up manually.

## Context

- **Agent harnesses**: Hermes Agent (`hermes -w`, per-worktree checkpoint history), and analogously Claude Code (worktree isolation, parallel-agent workflows) and other autonomous coding agents use worktrees as the recommended parallel-execution isolation mechanism.
- **Where it appears**: batch refactors run by multiple agents; trying several approaches to one task in parallel; pairing a CLI session and a messaging-gateway session against the same upstream repo; keeping experimental refactors off the main branch.
- **Relationship to checkpoints**: complements (does not replace) git commits and the harness's checkpoint/rollback safety net — worktrees isolate *between* agents, checkpoints recover *within* an agent's session.
- **Cleanup**: `git worktree remove <path>` drops the worktree (refusing if dirty unless forced); the branch and any harness checkpoint data persist until explicitly pruned.

## Key Characteristics

- **Own branch + working directory per agent**: each worktree checks out a distinct branch (e.g. `feature/hermes-a` vs `feature/hermes-b`) in its own directory, so file edits and tools are scoped to that agent.
- **Shared object store, private state**: linked worktrees share `refs/` and the `.git` object database with the main worktree but keep per-worktree `HEAD` and `index` (`$GIT_DIR/worktrees/<name>`), so they are cheap — no full repository duplication.
- **Same branch cannot be checked out twice**: `git worktree add` refuses a branch already checked out in another worktree (override with `--force`), which enforces non-interference.
- **Per-worktree checkpoint history**: agent harnesses scope rollback state to the worktree (in Hermes, a shadow-repo hash derived from the worktree path), so each agent's `/rollback` is independent.
- **Automatic disposable mode**: `hermes -w` creates a throwaway worktree + branch under `.worktrees/` (e.g. `hermes/hermes-<hash>`); combine with a single query (`hermes -w -z "Fix issue #123"`) for one-shot isolated runs.
- **Safe cleanup**: `git worktree remove` only removes clean worktrees unless forced; removing a worktree does not delete its branch or harness checkpoints.
- **Reviewable diffs**: one worktree per experiment keeps each agent's changes on a focused branch, producing small, reviewable pull requests.

## Related Terms


## References

- [git-worktree — Official Git Documentation](https://git-scm.com/docs/git-worktree)
- [Hermes Agent — Git Worktrees User Guide](https://hermes-agent.nousresearch.com/docs/user-guide/git-worktrees)
- [Run parallel Claude Code sessions with Git worktrees — Anthropic Docs](https://docs.anthropic.com/en/docs/claude-code/common-workflows)

---

**Last Updated**: 2026-06-19
**Status**: Active
