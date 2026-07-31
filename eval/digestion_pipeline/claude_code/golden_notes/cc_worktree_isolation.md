---
tags:
  - resource
  - documentation
  - claude_code
  - worktrees
  - isolation
keywords:
  - git worktree
  - worktree isolation
  - parallel sessions
  - --worktree flag
  - EnterWorktree
  - worktreeinclude
  - subagent isolation
  - worktree cleanup
  - non-git version control
topics:
  - Claude Code
  - Worktrees
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/worktrees
access_control_group: ["general"]
---

# Run Parallel Sessions with Worktrees

## Overview

A [git worktree](https://git-scm.com/docs/git-worktree) is a separate working directory with its own files and branch, sharing the same repository history and remote as your main checkout. Running each Claude Code session in its own worktree means edits in one session never touch files in another, so you can have Claude building a feature in one terminal while fixing a bug in a second. This page covers worktree isolation in the CLI and assumes a git repository (for other systems see [Non-git version control](#non-git-version-control)).

Worktrees are one of several ways to run Claude in parallel: they isolate **file edits**, while subagents and agent teams coordinate the **work itself**. The [desktop app](https://code.claude.com/docs/en/desktop) creates a worktree for every new session automatically.

## Start Claude in a Worktree

Pass `--worktree` or `-w` to create an isolated worktree and start Claude in it. By default the worktree is created under `.claude/worktrees/<value>/` at your repository root, on a new branch named `worktree-<value>`:

```bash
claude --worktree feature-auth
```

To put worktrees somewhere else, configure a [`WorktreeCreate` hook](#non-git-version-control). Run the command again with a different name in another terminal to start a second isolated session (e.g. `claude --worktree bugfix-123`). If you omit the name, Claude generates one such as `bright-running-fox`:

```bash
claude --worktree
```

You can also ask Claude to "work in a worktree" during a session, and it will create one with the [`EnterWorktree`](https://code.claude.com/docs/en/tools-reference) tool. Once in a worktree, Claude can switch directly to another one under `.claude/worktrees/` by calling `EnterWorktree` with the target path; the previous worktree stays on disk untouched.

Before using `--worktree` interactively in a directory for the first time, accept the workspace trust dialog by running `claude` once in that directory. If trust has not been accepted, `--worktree` exits with an error and prompts you to run `claude` first. Non-interactive runs with `-p` skip the [trust check](https://code.claude.com/docs/en/security), so `claude -p --worktree` proceeds without it. Add `.claude/worktrees/` to your `.gitignore` so worktree contents don't appear as untracked files in your main checkout.

### Choose the Base Branch

Worktrees branch from your repository's default branch, `origin/HEAD`, so they start from a clean tree matching the remote. If no remote is configured or the fetch fails, the worktree falls back to your current local `HEAD`. To always branch from local `HEAD` instead, set `worktree.baseRef` to `"head"` in [settings](https://code.claude.com/docs/en/settings). Setting `baseRef` to `"head"` makes new worktrees carry your unpushed commits and feature-branch state, which is useful when isolating subagents that need to operate on in-progress work. The setting accepts only `"fresh"` or `"head"`, not arbitrary git refs:

```json
{
  "worktree": {
    "baseRef": "head"
  }
}
```

To branch from a specific pull request, pass the PR number prefixed with `#`, or a full GitHub pull request URL (e.g. `claude --worktree "#1234"`). Claude Code fetches `pull/<number>/head` from `origin` and creates the worktree at `.claude/worktrees/pr-<number>`. For full control over how worktrees are created, configure a [`WorktreeCreate` hook](https://code.claude.com/docs/en/hooks), which replaces the default `git worktree` logic entirely.

## Copy Gitignored Files into Worktrees

A worktree is a fresh checkout, so untracked files like `.env` or `.env.local` from your main repository are not present. To copy them automatically when Claude creates a worktree, add a `.worktreeinclude` file to your project root. The file uses `.gitignore` syntax; only files that match a pattern **and** are also gitignored are copied, so tracked files are never duplicated:

```text
.env
.env.local
config/secrets.json
```

This applies to worktrees created with `--worktree`, subagent worktrees, and parallel sessions in the desktop app.

## Isolate Subagents with Worktrees

Subagents can run in their own worktrees so parallel edits don't conflict. Ask Claude to "use worktrees for your agents", or set it permanently on a [custom subagent](https://code.claude.com/docs/en/sub-agents) by adding `isolation: worktree` to the frontmatter. Each subagent gets a temporary worktree that is removed automatically when the subagent finishes without changes. Subagent worktrees use the same [base branch](#choose-the-base-branch) as `--worktree`, so they branch from your repository's default branch unless `worktree.baseRef` is set to `"head"`.

## Clean Up Worktrees

When you exit a worktree session, cleanup depends on whether you made changes:

- **No uncommitted changes, no untracked files, and no new commits**: the worktree and its branch are removed automatically. If the session has a [name](https://code.claude.com/docs/en/sessions), Claude prompts instead so you can keep the worktree for later.
- **Uncommitted changes, untracked files, or new commits exist**: Claude prompts you to keep or remove the worktree. Keeping preserves the directory and branch so you can return later. Removing deletes the worktree directory and its branch, discarding any uncommitted changes, untracked files, and commits.
- **Non-interactive runs**: worktrees created with `--worktree` alongside `-p` are not cleaned up automatically since there is no exit prompt. Remove them with `git worktree remove`.

Worktrees that Claude created for subagents and background sessions are removed automatically once they are older than your `cleanupPeriodDays` [setting](https://code.claude.com/docs/en/settings), provided they have no uncommitted changes, no untracked files, and no unpushed commits. Worktrees you create with `--worktree` are never removed by this sweep. While an agent is running, Claude runs `git worktree lock` on its worktree so that concurrent cleanup cannot remove it; the lock is released when the agent finishes. To clean up a worktree that the sweep keeps, run `git worktree remove`, adding `--force` if the worktree has uncommitted changes or untracked files.

## Manage Worktrees Manually

For full control over worktree location and branch configuration, create worktrees with Git directly. This is useful when you need to check out a specific existing branch or place the worktree outside the repository. Create one on a new branch with `git worktree add <path> -b <branch>`, or from an existing branch with `git worktree add <path> <branch>`; then `cd` into it and run `claude`. List worktrees with `git worktree list` and remove one with `git worktree remove`:

```bash
git worktree add ../project-feature-a -b feature-a
```

See the [Git worktree documentation](https://git-scm.com/docs/git-worktree) for the full command reference. Remember to initialize your development environment in each new worktree: install dependencies, set up virtual environments, or run whatever your project's setup requires.

## Non-git Version Control

Worktree isolation uses git by default. For SVN, Perforce, Mercurial, or other systems, configure [`WorktreeCreate` and `WorktreeRemove` hooks](https://code.claude.com/docs/en/hooks) to provide custom creation and cleanup logic. Because the hook replaces the default git behavior, [`.worktreeinclude`](#copy-gitignored-files-into-worktrees) is not processed when you use `--worktree`; copy any local configuration files inside your hook script instead.

This `WorktreeCreate` hook reads the worktree name from stdin, checks out a fresh SVN working copy, and prints the directory path so Claude Code can use it as the session's working directory:

```json
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

Pair it with a `WorktreeRemove` hook to clean up when the session ends. See the [hooks reference](https://code.claude.com/docs/en/hooks) for the input schema and a removal example.

**Source**: https://code.claude.com/docs/en/worktrees
**Last Updated**: 2026-06-13
**Status**: Active
