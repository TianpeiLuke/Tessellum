---
tags:
  - resource
  - documentation
  - claude_code
  - web
  - move_tasks
keywords:
  - move tasks between web and terminal
  - remote flag
  - teleport
  - cloud session handoff
  - plan locally execute remotely
  - ccr force bundle
  - run tasks in parallel
  - teleport requirements
topics:
  - Claude Code
  - Web & Remote Surfaces
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/claude-code-on-the-web
access_control_group: ["general"]
---

# Move Tasks Between Web and Terminal

## Overview

The Claude Code CLI can hand work back and forth with [Claude Code on the web](cc_web_overview.md) as long as the CLI is signed in to the same claude.ai account. You can **start new cloud sessions from your terminal** with `--remote`, or **pull cloud sessions into your terminal** to continue locally with `--teleport`. Cloud sessions persist even if you close your laptop, and you can monitor them from anywhere including the Claude mobile app.

From the CLI, this handoff is **one-way**: you can pull cloud sessions into your terminal with `--teleport`, but you cannot push an existing terminal session to the web. The `--remote` flag instead creates a *new* cloud session for your current repository. (The [Desktop app](https://code.claude.com/docs/en/desktop) provides a **Continue in** menu that can send a local session to the web.)

## From terminal to web (`--remote`)

Start a cloud session from the command line with the `--remote` flag:

```bash
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

This creates a new cloud session on claude.ai. The session **clones your current directory's GitHub remote at your current branch**, so push first if you have local commits — the VM clones from GitHub rather than your machine. `--remote` works with a single repository at a time. The task runs in the cloud while you continue working locally.

`--remote` is unrelated to `--remote-control`: the latter exposes a local CLI session for monitoring from the web (see [Remote Control](cc_remote_control.md)). Use `/tasks` in the CLI to check progress, or open the session on claude.ai or the mobile app to steer Claude, give feedback, or answer questions like any other conversation.

### Tips for cloud tasks

- **Plan locally, execute remotely**: for complex tasks, start `claude --permission-mode plan` to collaborate on the approach. In plan mode Claude reads files and runs commands to explore but proposes a plan without editing source. Once satisfied, save the plan to the repo, commit, and push so the cloud VM can clone it, then start a cloud session for autonomous execution (e.g. `claude --remote "Execute the migration plan in docs/migration-plan.md"`). You keep control of strategy while Claude executes autonomously in the cloud.
- **Plan in the cloud with ultraplan**: to draft and review the plan itself in a web session, use [ultraplan](https://code.claude.com/docs/en/ultraplan) — Claude generates the plan on the web while you keep working, then you comment on sections in the browser and choose to execute remotely or send the plan back to your terminal.
- **Run tasks in parallel**: each `--remote` command creates its own cloud session that runs independently, so you can launch several at once (`claude --remote "Fix the flaky test in auth.spec.ts"`, `claude --remote "Update the API documentation"`, etc.) and they run simultaneously in separate sessions. Monitor them all with `/tasks`; when one completes, create a PR from the web or teleport it to your terminal.

### Send local repositories without GitHub

When you run `claude --remote` from a repository not connected to GitHub, Claude Code bundles your local repository and uploads it directly to the cloud session. The bundle includes your full repository history across all branches, plus any uncommitted changes to tracked files. This fallback activates automatically when GitHub access isn't available. To force it even when GitHub is connected, set `CCR_FORCE_BUNDLE=1`:

```bash
CCR_FORCE_BUNDLE=1 claude --remote "Run the test suite and fix any failures"
```

Bundled repositories must be a git repo with at least one commit and under 100 MB (larger repos fall back to bundling only the current branch, then to a single squashed snapshot of the working tree, and fail only if the snapshot is still too large). Untracked files are not included — run `git add` on files you want the cloud session to see. Sessions created from a bundle can't push back to a remote unless you also have [GitHub authentication](https://code.claude.com/docs/en/claude-code-on-the-web#github-authentication-options) configured.

## From web to terminal (`--teleport`)

Pull a cloud session into your terminal using any of these:

- **`--teleport`**: run `claude --teleport` for an interactive session picker, or `claude --teleport <session-id>` to resume a specific session directly. If you have uncommitted changes, you're prompted to stash them first.
- **`/teleport`**: inside an existing CLI session, run `/teleport` (or `/tp`) to open the same picker without restarting Claude Code.
- **From `/tasks`**: run `/tasks` to see your background sessions, then press **`t`** to teleport into one.
- **From the web interface**: select **Open in CLI** to copy a command you can paste into your terminal.

When you teleport a session, Claude verifies you're in the correct repository, fetches and checks out the branch from the cloud session, and loads the **full conversation history** into your terminal. `--teleport` is distinct from `--resume`: `--resume` reopens a conversation from this machine's local history and doesn't list cloud sessions, while `--teleport` pulls a cloud session and its branch.

### Teleport requirements

Teleport checks these before resuming a session; if any isn't met you see an error or a prompt to resolve it:

| Requirement | Details |
| --- | --- |
| Clean git state | Working directory must have no uncommitted changes. Teleport prompts you to stash if needed. |
| Correct repository | You must run `--teleport` from a checkout of the same repository, not a fork. |
| Branch available | The branch from the cloud session must have been pushed to the remote. Teleport automatically fetches and checks it out. |
| Same account | You must be authenticated to the same claude.ai account used in the cloud session. |

### `--teleport` is unavailable

Teleport requires claude.ai subscription authentication. If you're authenticated via API key, Bedrock, Vertex AI, or Microsoft Foundry, run `/login` to sign in with your claude.ai account instead. If you're already signed in via claude.ai and `--teleport` is still unavailable, your organization may have disabled cloud sessions.

**Source**: https://code.claude.com/docs/en/claude-code-on-the-web
**Last Updated**: 2026-06-13
**Status**: Active
