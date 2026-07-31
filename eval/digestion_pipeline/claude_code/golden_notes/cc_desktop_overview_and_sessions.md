---
tags:
  - resource
  - documentation
  - claude_code
  - desktop
  - sessions
keywords:
  - claude desktop code tab
  - session
  - start a session
  - prompt box
  - interrupt and steer
  - mention files
  - parallel sessions
  - git worktrees
  - side chat
  - tasks pane
topics:
  - Claude Code
  - Desktop
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/desktop
access_control_group: ["general"]
---

# Claude Desktop — Code Tab Overview and Sessions

## Overview

The Claude Desktop app has three tabs — **Chat** for conversations, **Cowork** for Dispatch and longer agentic work, and **Code** for software development. In the Code tab, each conversation is a **session**: it has its own chat history, project folder, and code changes, independent of any other session. The sidebar lists your sessions and lets you run several in parallel. After installing, you launch Claude, sign in, and click the **Code** tab; on Windows the first open requires Git for Windows installed (restart the app after installing).

This note covers the day-to-day operating model of a Code-tab session — how to start one (Environment / Project folder / Model / Permission mode), drive it through the prompt box with interrupt-and-steer, add context via @mention and attachments, and manage multiple sessions in parallel (per-session Git worktree isolation), with side chats and the background-tasks pane. Permission modes are documented in [`cc_desktop_permission_modes`](cc_desktop_permission_modes.md); the verify/diff/review/PR loop in [`cc_desktop_diff_review_and_pr`](cc_desktop_diff_review_and_pr.md); pane layout, terminal, and computer use in [`cc_desktop_workspace_panes`](cc_desktop_workspace_panes.md).

## Start a session

Before you send your first message, configure four things in the prompt area:

- **Environment**: choose where Claude runs. Select **Local** for your machine, **Remote** for Anthropic-hosted cloud sessions, or an **SSH connection** for a remote machine you manage. (Environment configuration is documented in [`cc_desktop_environments_extend_and_enterprise`](cc_desktop_environments_extend_and_enterprise.md).)
- **Project folder**: select the folder or repository Claude works in. For cloud sessions, you can add multiple repositories.
- **Model**: pick a model from the dropdown next to the send button. You can change this during the session.
- **Permission mode**: choose how much autonomy Claude has from the mode selector. You can change this during the session.

Type your task and press **Enter** to start. Each session tracks its own context and changes independently.

## Work with code

Give Claude the right context, control how much it does on its own, and review what it changed.

### Use the prompt box

Type what you want Claude to do and press **Enter** to send. Claude reads your project files, makes changes, and runs commands based on your permission mode. You can redirect Claude at any point:

- Click the **stop** button to interrupt immediately.
- Or type a correction and press **Enter** to send it without stopping the running action. Claude reads the correction as soon as the current action completes and adjusts before its next step.

The **+** button next to the prompt box gives you access to file attachments, skills, connectors, and plugins. (Skills, connectors, and plugins are documented in [`cc_desktop_environments_extend_and_enterprise`](cc_desktop_environments_extend_and_enterprise.md).)

### Add files and context to prompts

The prompt box supports two ways to bring in external context:

- **@mention files**: type `@` followed by a filename to add a file to the conversation context. Claude can then read and reference that file. @mention is not available in cloud sessions.
- **Attach files**: attach images, PDFs, and other files to your prompt using the attachment button, or drag and drop files directly into the prompt. This is useful for sharing screenshots of bugs, design mockups, or reference documents.

## Manage sessions

Each session is an independent conversation with its own context and changes. You can run multiple sessions in parallel, branch off side chats, send work to the cloud, or let Dispatch start sessions for you from your phone. (Cloud/remote, continue-in-surface, and Dispatch sessions are documented in [`cc_desktop_environments_extend_and_enterprise`](cc_desktop_environments_extend_and_enterprise.md).)

### Work in parallel with sessions

Click **+ New session** in the sidebar, or press **Cmd+N** on macOS or **Ctrl+N** on Windows, to work on multiple tasks in parallel. Press **Ctrl+Tab** and **Ctrl+Shift+Tab** to cycle through sessions in the sidebar. For Git repositories, each session gets its own isolated copy of your project using Git worktrees, so changes in one session don't affect other sessions until you commit them. (Worktree mechanics are documented at the source: <https://code.claude.com/docs/en/worktrees>.)

To view two sessions at once, hold **Cmd** on macOS or **Ctrl** on Windows and click a session in the sidebar. The session opens in a second pane alongside the one you already have open. While the split is active, clicking another sidebar session replaces whichever pane has focus. Press **Cmd+\\** on macOS or **Ctrl+\\** on Windows to close the focused pane and return to a single session.

Worktrees are stored in `<project-root>/.claude/worktrees/` by default. You can change this to a custom directory in Settings → Claude Code under "Worktree location". You can also set a branch prefix that gets prepended to every worktree branch name, which is useful for keeping Claude-created branches organized. To remove a worktree when you're done, hover over the session in the sidebar and click the archive icon. To have sessions archive themselves when their pull request merges or closes, turn on **Auto-archive after PR merge or close** in Settings → Claude Code. Auto-archive only applies to local sessions that have finished running. To include gitignored files like `.env` in new worktrees, create a `.worktreeinclude` file in your project root.

Session isolation requires Git (most Macs include Git by default; on Windows it is required for the Code tab to work). Use the controls at the top of the sidebar to filter sessions by status, project, or environment, and to group sessions by project. To rename a session, click the session title in the toolbar at the top of the active session.

When context fills up, Claude automatically summarizes the conversation and continues working. You can also type `/compact` to trigger summarization earlier and free up context space. The desktop app sends an OS notification when a Code session finishes a task and you aren't currently viewing that session.

### Ask a side question without derailing the session

A side chat lets you ask Claude a question that uses your session's context but doesn't add anything back to the main conversation. Use it when you want to understand a piece of code, check an assumption, or explore an idea without steering the session off course.

Press **Cmd+;** on macOS or **Ctrl+;** on Windows to open a side chat, or type `/btw` in the prompt box. The side chat can read everything in the main thread up to that point. When you're done, close the side chat and continue the main session where you left off. Side chats are available in local and SSH sessions.

### Watch background tasks

The tasks pane shows the background work running inside the current session: **subagents**, **background shell commands**, and **dynamic workflows**. Open it from the **Views** menu or drag it into your layout.

Click any entry to see its output in the subagent pane or stop it. To see what other sessions are doing, use the sidebar.

**Source**: https://code.claude.com/docs/en/desktop
**Last Updated**: 2026-06-13
**Status**: Active
