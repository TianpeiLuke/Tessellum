---
tags:
  - resource
  - documentation
  - claude_code
  - slack
  - delegation
keywords:
  - claude code in slack
  - delegate coding task
  - mention claude
  - automatic detection
  - routing to web session
  - context gathering
  - session flow
  - message actions
topics:
  - Claude Code
  - Slack
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/slack
access_control_group: ["general"]
---

# Claude Code in Slack

## Overview

**Claude Code in Slack** brings Claude Code directly into a Slack workspace. When you mention `@Claude` with a coding task, Claude automatically detects the intent and creates a Claude Code session **on the web**, letting you delegate development work without leaving your team conversations. The integration is built on the existing Claude for Slack app but adds **intelligent routing** to Claude Code on the web for coding-related requests.

This note covers what the surface is and how it behaves — use cases, automatic detection and context gathering, the session flow, the in-Slack UI elements, what is visible in Slack versus on the web, best practices, and current limitations. Setup (prerequisites, the 5 install steps, routing-mode choice) and the access/permissions model and troubleshooting live in the sibling procedure note [Claude Code in Slack — Setup & Routing](cc_slack_setup_and_routing.md).

## Use cases

- **Bug investigation and fixes**: Ask Claude to investigate and fix bugs as soon as they're reported in Slack channels.
- **Quick code reviews and modifications**: Have Claude implement small features or refactor code based on team feedback.
- **Collaborative debugging**: When team discussions provide crucial context (e.g., error reproductions or user reports), Claude can use that information to inform its debugging approach.
- **Parallel task execution**: Kick off coding tasks in Slack while you continue other work, receiving notifications when complete.

## How it works

### Automatic detection

When you mention @Claude in a Slack channel or thread, Claude automatically analyzes your message to determine if it's a coding task. If Claude detects coding intent, it routes your request to Claude Code on the web instead of responding as a regular chat assistant. You can also explicitly tell Claude to handle a request as a coding task, even if it isn't automatically detected.

Claude Code in Slack only works in channels (public or private). It does **not** work in direct messages (DMs).

### Context gathering

- **From threads**: When you @mention Claude in a thread, it gathers context from all messages in that thread to understand the full conversation.
- **From channels**: When mentioned directly in a channel, Claude looks at recent channel messages for relevant context.

This context helps Claude understand the problem, select the appropriate repository, and inform its approach to the task. Because Claude is given access to the conversation context and may follow directions from other messages in that context, the docs warn that you should only use Claude in **trusted** Slack conversations.

### Session flow

1. **Initiation**: You @mention Claude with a coding request.
2. **Detection**: Claude analyzes your message and detects coding intent.
3. **Session creation**: A new Claude Code session is created on claude.ai/code.
4. **Progress updates**: Claude posts status updates to your Slack thread as work progresses.
5. **Completion**: When finished, Claude @mentions you with a summary and action buttons.
6. **Review**: Click "View Session" to see the full transcript, or "Create PR" to open a pull request.

## User interface elements

### App Home

The App Home tab shows your connection status and lets you connect or disconnect your Claude account from Slack.

### Message actions

- **View Session**: Opens the full Claude Code session in your browser, where you can see all work performed, continue the session, or make additional requests.
- **Create PR**: Creates a pull request directly from the session's changes.
- **Retry as Code**: If Claude initially responds as a chat assistant but you wanted a coding session, click this button to retry the request as a Claude Code task.
- **Change Repo**: Lets you select a different repository if Claude chose incorrectly.

### Repository selection

Claude automatically selects a repository based on context from your Slack conversation. If multiple repositories could apply, Claude may display a dropdown allowing you to choose the correct one.

## What's accessible where

- **In Slack**: You'll see status updates, completion summaries, and action buttons. The full transcript is preserved and always accessible.
- **On the web**: The complete Claude Code session with full conversation history, all code changes, file operations, and the ability to continue the session or create pull requests.

For Enterprise and Team accounts, sessions created from Claude in Slack are automatically visible to the organization (see [Claude Code on the Web session sharing](https://code.claude.com/docs/en/claude-code-on-the-web)).

## Best practices

### Writing effective requests

- **Be specific**: Include file names, function names, or error messages when relevant.
- **Provide context**: Mention the repository or project if it's not clear from the conversation.
- **Define success**: Explain what "done" looks like — should Claude write tests? Update documentation? Create a PR?
- **Use threads**: Reply in threads when discussing bugs or features so Claude can gather the full context.

### When to use Slack vs. web

- **Use Slack when**: Context already exists in a Slack discussion, you want to kick off a task asynchronously, or you're collaborating with teammates who need visibility.
- **Use the web directly when**: You need to upload files, want real-time interaction during development, or are working on longer, more complex tasks.

## Current limitations

- **GitHub only**: Currently supports repositories on GitHub.
- **One PR at a time**: Each session can create one pull request.
- **Rate limits apply**: Sessions use your individual Claude plan's rate limits.
- **Web access required**: Users must have Claude Code on the web access; those without it will only get standard Claude chat responses.

**Source**: https://code.claude.com/docs/en/slack
**Last Updated**: 2026-06-13
**Status**: Active
