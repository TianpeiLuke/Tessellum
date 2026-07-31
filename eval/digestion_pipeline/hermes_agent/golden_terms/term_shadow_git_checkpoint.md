---
tags:
  - resource
  - terminology
  - systems
  - version_control
  - autonomous_agents
keywords:
  - shadow git checkpoint
  - shadow git repo
  - filesystem rollback
  - checkpoint manager
  - hermes checkpoints
  - rollback
  - content-addressable store
topics:
  - autonomous coding agents
  - version control
  - filesystem safety
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Shadow Git Checkpoint - Filesystem Rollback Store

## Definition

A **shadow git checkpoint** is a filesystem safety net in which an autonomous coding agent automatically snapshots a project's working tree *before* a destructive operation by committing it into a **separate, hidden git repository** — the "shadow" store — that lives outside and never touches the project's real `.git`. The mechanism lets the agent (and the user) restore the working directory to any prior snapshot with a single rollback command, undoing agent-driven edits without affecting normal version-control history. It originates in the Hermes Agent runtime, where an internal **Checkpoint Manager** maintains a single shared bare git repo under `~/.hermes/checkpoints/store/` and exposes restore via the in-session `/rollback` command and the `hermes checkpoints` CLI.

The "shadow" qualifier is load-bearing: because the snapshots are committed into a side repository keyed per-project rather than into the user's own `.git`, the agent gains an undo layer that is invisible to the project's real branches, commits, and remotes. In Hermes this is **opt-in** (default off) since the shadow store's storage grows non-trivially over time.

## Context

- **Origin / owner**: the [Hermes Agent](term_hermes_agent.md) runtime — an [autonomous coding agent](term_autonomous_coding_agents.md) harness — implements this as its Checkpoint Manager subsystem.
- **Where it appears in the pipeline**: the [agent harness](term_agent_harness.md) registers a `ensure_checkpoint()` hook that fires *before* file tools (`write_file`, `patch`) and destructive terminal commands (`rm`, `mv`, `sed -i`, `dd`, output redirects, `git reset`/`clean`/`checkout`) mutate the working tree.
- **User-facing surface**: in-session slash commands (`/rollback`, `/rollback <N>`, `/rollback diff <N>`, `/rollback <N> <file>`) plus a shell CLI (`hermes checkpoints status` / `prune` / `clear`) for inspecting and pruning the store.
- **Relationship to real VCS**: deliberately distinct from the user's project repository — it is an agent-safety overlay, recommended to be combined with git-worktree isolation when running multiple agents on one repo.
- **Analogous systems**: the same pattern appears in other autonomous coding agents (e.g. Cline's automatic checkpoints, Claude Code's file-checkpointing), where it serves as the recovery primitive for unattended agent edits.

## Key Characteristics

- **Single shared content-addressable store**: one bare git repo at `~/.hermes/checkpoints/store/` serves every project. Because git addresses objects by the SHA hash of their content, identical files and unchanged content across projects and across turns are stored only once (automatic deduplication) — the project's real `.git` is never touched.
- **Per-project refs**: each project gets its own checkpoint history under a ref like `refs/hermes/<project-hash>`, where `<hash>` is derived from the absolute path of the working directory; a per-project index (`indexes/<hash>`) and metadata (`projects/<hash>.json`) track the workdir, creation time, and last-touch.
- **Snapshot mechanics**: at most **one checkpoint per directory per conversation turn**, built by staging into the per-project index, building a tree, and committing via `commit-tree` + `update-ref`. No-change turns are skipped.
- **Restore semantics**: a `/rollback <N>` verifies the target commit, takes a **pre-rollback snapshot** (so the undo itself is reversible — "undo the undo"), restores tracked files, and **undoes the last conversation turn** so the agent's context matches the restored filesystem.
- **Retention governance**: config knobs `max_snapshots` (enforced by rewriting the per-project ref + `git gc --prune=now`), `max_total_size_mb` (oldest commit dropped round-robin when exceeded), `max_file_size_mb` (skip large files), plus `auto_prune` / `retention_days` / `delete_orphans` for startup sweeps.
- **Idempotent maintenance**: a `.last_prune` marker bounds the auto-prune sweep to at most once per `min_interval_hours`, making repeated startups idempotent.
- **Safety guards**: disabled transparently if `git` is absent from `PATH`; skips overly broad directories (`/`, `$HOME`) and repos exceeding 50,000 files; all internal errors are non-fatal (logged at debug, tools continue).
- **v1 → v2 migration**: pre-v2 per-directory shadow repos (which could not dedup and had a no-op pruner) are archived into `legacy-<timestamp>/` on first v2 run, reclaimable via `hermes checkpoints clear-legacy`.

## Related Terms


## References

- [Checkpoints and /rollback — Hermes Agent User Guide](https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback/)
- [Git Internals — Git Objects (content-addressable store, commit-tree)](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
- [Git Internals — Git References (refs and update-ref)](https://git-scm.com/book/en/v2/Git-Internals-Git-References)
- [git-worktree documentation (combining checkpoints with worktree isolation)](https://git-scm.com/docs/git-worktree)

---

**Last Updated**: 2026-06-19
**Status**: Active
