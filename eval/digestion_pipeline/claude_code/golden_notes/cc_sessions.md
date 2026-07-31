---
tags:
  - resource
  - documentation
  - claude_code
  - sessions
  - state
keywords:
  - session
  - resume a session
  - session picker
  - branch a session
  - fork session
  - name your sessions
  - manage context within a session
  - export session
  - jsonl transcript
topics:
  - Claude Code
  - Sessions
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/sessions
access_control_group: ["general"]
---

# Claude Code — Sessions

## Overview

A **session** is a saved conversation tied to a project directory. Claude Code stores it locally as you work, so you can resume where you left off, branch to try a different approach, or switch between tasks. Sessions are saved continuously to local transcript files, so you can return to one after exiting or running `/clear`.

This note covers the CLI session lifecycle: resuming a previous conversation (by flag, name, or PR), naming sessions, browsing them with the `/resume` picker, branching to try a different approach, managing context within a session, and exporting and locating session data on disk. The desktop app, Claude Code on the web, and the VS Code extension each maintain their own separate session history.

## Resume a Session

Use these entry points to return to a prior conversation:

| Command                     | What it does                                                       |
| :-------------------------- | :----------------------------------------------------------------- |
| `claude --continue`         | Resumes the most recent session in the current directory           |
| `claude --resume`           | Opens the session picker                                           |
| `claude --resume <name>`    | Resumes the named session directly                                 |
| `claude --from-pr <number>` | Resumes the session linked to that pull request                    |
| `/resume`                   | Switches to a different conversation from inside an active session |

Sessions created with `claude -p` (non-interactive mode) or the Agent SDK do not appear in the session picker, but you can still resume one by passing its session ID to `claude --resume <session-id>`. Run this from the directory the session was started in: session ID lookup is scoped to the current project directory and its git worktrees, so a session created elsewhere reports `No conversation found with session ID: <session-id>`.

### Where the Session Picker Looks

Sessions are stored per project directory. By default the session picker shows interactive sessions from the current worktree, plus sessions started elsewhere that added the current directory with `/add-dir`. From v2.1.169, moving a session with `/cd` relocates it to the new directory's project storage, so it appears in that directory's picker afterward. Use `Ctrl+W` to widen to all worktrees of the repository or `Ctrl+A` to widen to every project on this machine.

Selecting a session from another worktree of the same repository resumes it in place. Selecting a session from an unrelated project copies a `cd` and resume command to your clipboard instead.

Resuming by name resolves across the current repository and its worktrees. Both forms look for an exact match and resume it directly even if it lives in a different worktree:

| Command                  | Exact match      | Ambiguous name                                                              |
| :----------------------- | :--------------- | :-------------------------------------------------------------------------- |
| `claude --resume <name>` | Resumes directly | Opens the session picker with the name pre-filled as a search term          |
| `/resume <name>`         | Resumes directly | Reports an error; run `/resume` with no argument to open the session picker |

## Name Your Sessions

Descriptive names make sessions findable in the session picker and resumable by name. This matters most when working on several tasks in parallel.

| When                    | How to set the name                                                                       |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| At startup              | `claude -n auth-refactor`                                                                 |
| During a session        | `/rename auth-refactor`. The name also appears on the prompt bar                          |
| From the session picker | Highlight a session and press `Ctrl+R`                                                     |
| On plan accept          | Accepting a plan in plan mode names the session from the plan content unless already set  |

Once named, return to it with `claude --resume <name>` or `/resume <name>`. See *Resume a Session* for how name resolution behaves across worktrees.

## Use the Session Picker

Run `/resume` inside a session, or `claude --resume` with no arguments, to open the interactive session picker. Keyboard shortcuts navigate, search, and widen the list: `↑`/`↓` navigate between sessions; `→`/`←` expand or collapse grouped sessions; `Enter` resumes the highlighted session; `Space` previews session content (`Ctrl+V` also works on terminals that capture it as paste); `Ctrl+R` renames; `/` or any printable character other than `Space` enters search mode and filters (paste a GitHub, GitHub Enterprise, GitLab, or Bitbucket pull/merge request URL to find the session that created it); `Ctrl+A` shows sessions from all projects on this machine (press again to return to the current repository); `Ctrl+W` shows sessions from all worktrees of the current repository (press again to return; only shown in multi-worktree repositories); `Ctrl+B` filters to sessions from the current git branch (press again to show all branches); `Esc` exits the picker or search mode.

Each row shows the session name if set, otherwise the conversation summary or first prompt, along with time since last activity, message count, and git branch. Project path appears after you widen to all projects with `Ctrl+A`. Forked sessions created with `/branch`, `/rewind`, or `--fork-session` are grouped under their root session; press `→` to expand a group.

## Branch a Session

Branching creates a copy of the conversation so far and switches you into it, leaving the original intact. Use it to try a different approach without losing the path you were on. From inside a session, run `/branch` with an optional name:

```text
/branch try-streaming-approach
```

From the command line, combine `--continue` or `--resume` with `--fork-session`:

```bash
claude --continue --fork-session
```

The original session is unchanged and remains available in the session picker. The `/branch` confirmation prints two session IDs: the new branch you are now in and the original. To return to the original, pass its ID to `/resume`, use the session picker, or run `/resume <original-name>`. Permissions you approved with "allow for this session" do not carry over to the new branch. If you resume the same session in two terminals without forking, messages from both interleave into one transcript.

For checkpoint-based rewind within a single session, see [Checkpointing](cc_checkpointing.md).

## Manage Context Within a Session

These commands control what's in the context window without leaving the session:

- **`/clear`**: start fresh with an empty context. The previous conversation is saved and resumable.
- **`/compact [instructions]`**: replace history with a summary, optionally focused on what you specify.
- **`/context`**: show what is currently consuming context.

For how compaction interacts with CLAUDE.md, skills, and rules, see the [context window guide](https://code.claude.com/docs/en/context-window). For strategies on when to clear versus compact, see [Best practices](https://code.claude.com/docs/en/best-practices).

## Export and Locate Session Data

Run `/export` to copy the current conversation to your clipboard or save it as a plain-text file, with messages and tool outputs rendered as readable text. Pass a filename to write directly to that file.

Transcripts are stored as JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`, where `<project>` is derived from your working directory path. Each line is a JSON object for a message, tool use, or metadata entry. To store sessions somewhere other than `~/.claude`, set [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/en/env-vars). These local files are removed after 30 days by default; change this with [`cleanupPeriodDays`](https://code.claude.com/docs/en/settings).

To suppress transcript writes entirely, set [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](https://code.claude.com/docs/en/env-vars), or in non-interactive mode use `--no-session-persistence`.

**Source**: https://code.claude.com/docs/en/sessions
**Last Updated**: 2026-06-13
**Status**: Active
