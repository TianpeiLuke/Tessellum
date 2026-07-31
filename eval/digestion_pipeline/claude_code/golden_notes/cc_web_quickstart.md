---
tags:
  - resource
  - documentation
  - claude_code
  - web_surface
  - quickstart
keywords:
  - claude code on the web quickstart
  - connect github app
  - web-setup
  - cloud environment
  - permission mode accept edits plan
  - start a task
  - pre-fill sessions query params
  - review and iterate diff
topics:
  - Claude Code
  - Web Surface
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/web-quickstart
access_control_group: ["general"]
---

# Claude Code on the Web — Quickstart

## Overview

This is the onboarding procedure for [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) (the managed cloud surface; see also `cc_web_overview.md`). You connect a GitHub account, create a cloud environment, submit a task to a repository, then review the diff and iterate until the change is right. Setup is a one-time process. Everything below happens from [claude.ai/code](https://claude.ai/code) (browser or Claude mobile app), except the optional terminal-based connection path.

## Connect GitHub and create an environment

You can do the one-time setup from the browser or, if you use the GitHub CLI, from your terminal.

**Browser path:**

1. **Visit claude.ai/code** — go to [claude.ai/code](https://claude.ai/code) and sign in with your Anthropic account.
2. **Install the Claude GitHub App** — claude.ai/code prompts you to connect GitHub. Follow the prompt to install the Claude GitHub App and grant it access to your repositories. Cloud sessions work with existing GitHub repositories, so to start a new project, create an empty repository on GitHub first.
3. **Create your environment** — after connecting GitHub, you're prompted to create a cloud environment, which controls what network access Claude has during sessions and what runs when a new session is created. The form has these fields:
   - **Name**: a display label, useful when you have multiple environments for different projects or access levels.
   - **Network access**: controls what the session can reach on the internet. The default, `Trusted`, allows connections to common package registries (npm, PyPI, RubyGems) while blocking general internet access.
   - **Environment variables**: optional variables available in every session, in `.env` format. Don't wrap values in quotes (quotes are stored as part of the value). These are visible to anyone who can edit the environment.
   - **Setup script**: an optional Bash script that runs before Claude Code launches, e.g. to install system tools the cloud VM doesn't include (`apt install -y gh`). The result is cached so it doesn't re-run every session.

   For a first project, leave the defaults and click **Create environment**. You can edit it later or create additional environments.

### Connect from your terminal

If you already use the GitHub CLI (`gh`), set up Claude Code on the web without a browser. This requires the Claude Code CLI. `/web-setup` reads your local `gh` token, links it to your Claude account, and creates a default cloud environment if you don't have one. (Organizations with Zero Data Retention enabled cannot use `/web-setup` or other cloud session features; if the GitHub CLI isn't installed or authenticated, `/web-setup` opens the browser onboarding flow instead.)

1. **Authenticate with the GitHub CLI** — in your shell, run `gh auth login` if you haven't already.
2. **Sign in to Claude** — in the Claude Code CLI, run `/login` to sign in with your claude.ai account. Skip if already signed in.
3. **Run `/web-setup`** — in the Claude Code CLI, run `/web-setup`. This syncs your `gh` token to your Claude account and, if you have no cloud environment yet, creates one with Trusted network access and no setup script. Once it completes, you can start cloud sessions from your terminal with `--remote` or set up recurring tasks with `/schedule`.

## Start a task

With GitHub connected and an environment created, you're ready to submit tasks.

1. **Select a repository and branch** — from claude.ai/code or the Code tab in the Claude mobile app, click the repository selector below the input box and choose a repository. Each repository shows a branch selector; change it to start Claude from a feature branch instead of the default. You can add multiple repositories to work across them in one session.
2. **Choose a permission mode** — the mode dropdown next to the input defaults to **Accept edits**, where Claude makes changes and pushes a branch without stopping for approval. Switch to **Plan mode** to have Claude propose an approach and wait for your go-ahead before editing files. Cloud sessions don't offer Ask permissions or Bypass permissions. See [Permission modes](https://code.claude.com/docs/en/permission-modes) for the full list.
3. **Describe the task and submit** — type a description of what you want and press Enter. Be specific:
   - Name the file or function: "Fix the failing auth test in `tests/test_auth.py`" is better than "fix tests".
   - Paste error output if you have it.
   - Describe the expected behavior, not just the symptom.

   Claude clones the repositories, runs your setup script if configured, and starts working. Each task gets its own session and its own branch, so you don't need to wait for one to finish before starting another.

## Pre-fill sessions

You can prefill the prompt, repositories, and environment for a new session by adding query parameters to the claude.ai/code URL — useful for integrations such as an issue-tracker button that opens Claude Code with the issue description as the prompt. Parameters: `prompt` (prompt text; alias `q`), `prompt_url` (URL to fetch a long prompt from; must allow cross-origin requests; ignored when `prompt` is set), `repositories` (comma-separated `owner/repo` slugs; alias `repo`), and `environment` (name or ID to preselect). URL-encode each value:

```text
https://claude.ai/code?prompt=Fix%20the%20login%20bug&repositories=acme/webapp
```

## Review and iterate

When Claude finishes, review the changes, leave feedback on specific lines, and keep going until the diff looks right.

1. **Open the diff view** — a diff indicator shows lines added and removed across the session (e.g. `+42 -18`). Select it to open the diff view, with a file list on the left and changes on the right.
2. **Leave inline comments** — select any line in the diff, type your feedback, and press Enter. Comments queue up until you send your next message, then bundle with it (Claude sees "at `src/auth.ts:47`, don't catch the error here" alongside your main instruction), so you don't have to describe where the problem is.
3. **Create a pull request** — when the diff looks right, select **Create PR** at the top of the diff view. You can open it as a full PR, a draft, or jump to GitHub's compose page with a generated title and description.
4. **Keep iterating after the PR** — the session stays live after the PR is created. Paste CI failure output or reviewer comments into the chat and ask Claude to address them. To have Claude monitor the PR automatically, see Auto-fix pull requests (`cc_web_session_management.md`).

For setup problems (no repos appear, `/web-setup` errors, environment creation failures, setup-script failures), see cloud-session troubleshooting in `cc_web_security_and_limits.md`.

**Source**: https://code.claude.com/docs/en/web-quickstart
**Last Updated**: 2026-06-13
**Status**: Active
