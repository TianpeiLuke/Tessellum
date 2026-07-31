---
tags:
  - resource
  - documentation
  - claude_code
  - quickstart
  - getting_started
keywords:
  - claude code quickstart
  - first session
  - install claude code
  - ask your first question
  - make your first code change
  - git with claude code
  - essential commands
  - pro tips for beginners
topics:
  - Claude Code
  - Getting Started
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/quickstart
access_control_group: ["general"]
---

# Claude Code — Quickstart

## Overview

This is the first-session walkthrough for the Claude Code terminal CLI: an eight-step path from installing the tool to making real code changes, running Git operations, and fixing bugs — all by talking to Claude in natural language. Before you begin, you need a terminal, a code project to work with, and a Claude subscription (Pro, Max, Team, or Enterprise), a Claude Console account, or access through a supported cloud provider.

The guide covers the terminal CLI specifically. Claude Code is also available on the [web](https://code.claude.com/docs/en/overview), as a [desktop app](https://code.claude.com/docs/en/desktop), in [VS Code](https://code.claude.com/docs/en/vs-code) and JetBrains IDEs, in [Slack](https://code.claude.com/docs/en/slack), and in CI/CD with GitHub Actions and GitLab.

## Step 1: Install Claude Code

Install with a native installer (recommended), Homebrew (`brew install --cask claude-code`), or WinGet (`winget install Anthropic.ClaudeCode`). The native install command on macOS, Linux, and WSL is:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Native installations auto-update in the background; Homebrew and WinGet installs do not. You can also install with apt, dnf, or apk. See the full [setup](https://code.claude.com/docs/en/setup) guide for all install methods and package managers.

## Step 2: Log in to your account

Claude Code requires an account. Start an interactive session with the `claude` command and you'll be prompted to log in on first use; follow the prompts to authenticate in your browser. To switch accounts or re-authenticate later, type `/login` inside the running session. You can log in with a Claude subscription (recommended), a Claude Console account (API access with pre-paid credits — a "Claude Code" workspace is auto-created for cost tracking), or an enterprise cloud provider (Amazon Bedrock, Google Vertex AI, Microsoft Foundry). Once logged in, credentials are stored and you won't need to log in again.

## Step 3: Start your first session

Open your terminal in any project directory and start Claude Code:

```bash
cd /path/to/your/project
claude
```

The prompt shows the version, current model, and working directory above it. Type `/help` for available commands or `/resume` to continue a previous conversation.

## Step 4: Ask your first question

Start by understanding your codebase — ask `what does this project do?`, `where is the main entry point?`, or `explain the folder structure`. You can also ask Claude about its own capabilities, e.g. `what can Claude Code do?` or `how do I create custom skills in Claude Code?`. Claude reads project files as needed; you don't have to manually add context.

## Step 5: Make your first code change

Ask for a simple task such as `add a hello world function to the main file`. Claude Code will (1) find the appropriate file, (2) show you the proposed changes, (3) ask for your approval, and (4) make the edit. Claude Code always asks for permission before modifying files — you can approve individual changes or enable "Accept all" mode for a session.

## Step 6: Use Git with Claude Code

Git operations are conversational. Ask `what files have I changed?`, `commit my changes with a descriptive message`, `create a new branch called feature/quickstart`, `show me the last 5 commits`, or `help me resolve merge conflicts`.

## Step 7: Fix a bug or add a feature

Describe what you want in natural language, e.g. `add input validation to the user registration form`, or fix an existing issue, e.g. `there's a bug where users can submit empty forms - fix it`. Claude Code locates the relevant code, understands the context, implements a solution, and runs tests if available.

## Step 8: Test out other common workflows

There are many ways to work with Claude — refactor code (`refactor the authentication module to use async/await instead of callbacks`), write tests, update documentation, or run a code review (`review my changes and suggest improvements`). Talk to Claude like a helpful colleague: describe what you want to achieve. For more, see the sibling [workflow recipes](cc_workflow_recipes.md) note.

## Essential commands

Shell commands run from your terminal to start or resume Claude Code; session commands run inside Claude Code after it starts.

| Command | What it does |
| --- | --- |
| `claude` | Start interactive mode |
| `claude "task"` | Run a one-time task |
| `claude -p "query"` | Run one-off query, then exit |
| `claude -c` | Continue most recent conversation in current directory |
| `claude -r` | Resume a previous conversation |
| `/clear` | Clear conversation history |
| `/help` | Show available commands |
| `/exit` or Ctrl+D | Exit Claude Code |

See the [CLI reference](https://code.claude.com/docs/en/cli-reference) for the complete list of shell commands and the [commands reference](https://code.claude.com/docs/en/commands) for the complete list of session commands.

## Pro tips for beginners

- **Be specific with your requests** — instead of "fix the bug", try "fix the login bug where users see a blank screen after entering wrong credentials".
- **Use step-by-step instructions** — break complex tasks into numbered steps.
- **Let Claude explore first** — before making changes, let Claude understand your code (e.g. `analyze the database schema`).
- **Save time with shortcuts** — type `/` to see all commands and skills, use Tab for command completion, press ↑ for command history, and press `Shift+Tab` to cycle permission modes.

## Getting help

In Claude Code, type `/help` or ask "how do I...". For deeper guidance, explore [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works), [best practices](https://code.claude.com/docs/en/best-practices), and the sibling notes on the [verification loop](cc_verification_loop.md) and [workflow recipes](cc_workflow_recipes.md).

**Source**: https://code.claude.com/docs/en/quickstart
**Last Updated**: 2026-06-13
**Status**: Active
