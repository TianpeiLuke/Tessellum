---
tags:
  - resource
  - documentation
  - claude_code
  - web
  - sessions
keywords:
  - cloud session management
  - claude code on the web
  - manage context cloud
  - compact context
  - share sessions
  - archive delete sessions
  - auto-fix pull requests
  - review changes inline comments
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

# Claude Code on the Web — Session Management & Auto-fix

## Overview

Cloud sessions appear in the sidebar at `claude.ai/code`, where you manage them through their full lifecycle: manage the conversation context, review the changes Claude made, share a session with teammates, and archive or delete finished work. Because cloud sessions render in a browser/mobile UI rather than a terminal, only the subset of built-in commands that produce **text output** is available — interactive picker commands like `/model` and `/config` are not.

A cloud session can also keep working after you push: **Auto-fix pull requests** has Claude subscribe to GitHub activity on a PR and automatically respond to CI failures and review comments, pushing a fix when one is clear and asking you when a request is ambiguous.

## Manage context

Cloud sessions support [built-in commands](https://code.claude.com/docs/en/commands) that produce text output. Commands that open an interactive terminal picker, like `/model` or `/config`, are not available. For context management specifically:

| Command | Works in cloud sessions | Notes |
| :--- | :--- | :--- |
| `/compact` | Yes | Summarizes the conversation to free up context. Accepts optional focus instructions like `/compact keep the test output` |
| `/context` | Yes | Shows what's currently in the context window |
| `/clear` | No | Start a new session from the sidebar instead |

Auto-compaction runs automatically when the context window approaches capacity. To trigger it earlier, set `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` in your [environment variables](cc_cloud_environment.md). For example, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` compacts at 70% capacity instead of waiting until the window is nearly full. To change the effective window size for compaction calculations, use `CLAUDE_CODE_AUTO_COMPACT_WINDOW`.

[Subagents](https://code.claude.com/docs/en/sub-agents) work the same way they do locally. Claude can spawn them with the Task tool to offload research or parallel work into a separate context window, keeping the main conversation lighter. Subagents defined in your repo's `.claude/agents/` are picked up automatically. [Agent teams](https://code.claude.com/docs/en/agent-teams) are off by default but can be enabled by adding `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` to your environment variables.

## Review changes

Each session shows a diff indicator with lines added and removed, like `+42 -18`. Select it to open the diff view, leave inline comments on specific lines, and send them to Claude with your next message. See [Review and iterate](cc_web_quickstart.md) for the full walkthrough including PR creation. To have Claude monitor the PR for CI failures and review comments automatically, see Auto-fix pull requests below.

## Share sessions

To share a session, toggle its visibility according to the account type, then share the session link as-is. Recipients see the latest state when they open the link, but their view doesn't update in real time.

- **Enterprise or Team account**: the two visibility options are **Private** and **Team**. Team visibility makes the session visible to other members of your claude.ai organization. Repository access verification is enabled by default, based on the GitHub account connected to the recipient's account. Your account's display name is visible to all recipients with access. [Claude in Slack](https://code.claude.com/docs/en/slack) sessions are automatically shared with Team visibility.
- **Max or Pro account**: the two visibility options are **Private** and **Public**. Public visibility makes the session visible to any user logged into claude.ai. Check your session for sensitive content before sharing, since sessions may contain code and credentials from private GitHub repositories. Repository access verification is **not** enabled by default. To require recipients to have repository access, or to hide your name from shared sessions, go to **Settings > Claude Code > Sharing settings**.

## Archive sessions

Archive sessions to keep your session list organized. Archived sessions are hidden from the default session list but can be viewed by filtering for archived sessions. To archive a session, hover over it in the sidebar and select the archive icon.

## Delete sessions

Deleting a session permanently removes the session and its data; this action cannot be undone. You can delete a session in two ways:

- **From the sidebar**: filter for archived sessions, then hover over the session and select the delete icon.
- **From the session menu**: open a session, select the dropdown next to the session title, and select **Delete**.

You will be asked to confirm before a session is deleted.

## Auto-fix pull requests

Claude can watch a pull request and automatically respond to CI failures and review comments. Claude subscribes to GitHub activity on the PR, and when a check fails or a reviewer leaves a comment, Claude investigates and pushes a fix if one is clear. **Auto-fix requires the Claude GitHub App to be installed on your repository** (install it from the GitHub App page or when prompted during setup); it relies on the App to receive PR webhooks.

There are a few ways to turn on auto-fix depending on where the PR came from and the device you're using:

- **PRs created in Claude Code on the web**: open the CI status bar and select **Auto-fix**.
- **From your terminal**: run `/autofix-pr` while on the PR's branch. Claude Code detects the open PR with `gh`, spawns a web session, and turns on auto-fix in one step.
- **From the mobile app**: tell Claude to auto-fix the PR, e.g. "watch this PR and fix any CI failures or review comments".
- **Any existing PR**: paste the PR URL into a session and tell Claude to auto-fix it.

Auto-fix is a per-PR toggle. To stop monitoring, open the CI status bar in the web session and clear the **Auto-fix** toggle, or tell Claude to stop watching the PR.

### How Claude responds to PR activity

When auto-fix is active, Claude receives GitHub events for the PR including new review comments and CI check failures. For each event, Claude investigates and decides how to proceed:

- **Clear fixes**: if Claude is confident in a fix and it doesn't conflict with earlier instructions, Claude makes the change, pushes it, and explains what was done in the session.
- **Ambiguous requests**: if a reviewer's comment could be interpreted multiple ways or involves something architecturally significant, Claude asks you before acting.
- **Duplicate or no-action events**: if an event is a duplicate or requires no change, Claude notes it in the session and moves on.

GitHub does not emit a webhook when the base branch advances and creates a merge conflict, so auto-fix cannot react to conflicts on its own — open the session and ask Claude to rebase. Claude may reply to review comment threads on GitHub as part of resolving them. These replies are posted using your GitHub account, so they appear under your username, but each reply is labeled as coming from Claude Code so reviewers know it was written by the agent and not by you directly.

> **Warning** — If your repository uses comment-triggered automation such as Atlantis, Terraform Cloud, or custom GitHub Actions that run on `issue_comment` events, be aware that Claude can reply on your behalf, which can trigger those workflows. Review your repository's automation before enabling auto-fix, and consider disabling auto-fix for repositories where a PR comment can deploy infrastructure or run privileged operations.

**Source**: https://code.claude.com/docs/en/claude-code-on-the-web
**Last Updated**: 2026-06-13
**Status**: Active
