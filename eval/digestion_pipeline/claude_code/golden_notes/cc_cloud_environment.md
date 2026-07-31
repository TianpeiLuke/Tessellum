---
tags:
  - resource
  - documentation
  - claude_code
  - cloud_environment
  - web
keywords:
  - cloud environment
  - fresh per-session vm
  - what carries over
  - installed tools
  - claude_code_remote_session_id
  - resource limits
  - configure environment
  - remote-env
topics:
  - Claude Code
  - Cloud Environment
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/claude-code-on-the-web
access_control_group: ["general"]
---

# Claude Code on the Web — The Cloud Environment

## Overview

Each Claude Code on the web session runs in a **fresh Anthropic-managed VM with your repository cloned**. Because the session starts from a clean clone, the rule for what is available is simple: anything **committed to the repo** carries over, while anything **installed or configured only on your own machine** does not. The VM ships with common language runtimes, build tools, and databases pre-installed, plus built-in GitHub tools that authenticate through a proxy so your token never enters the container.

This note covers the environment model: the carries-over table, the pre-installed toolchain, the built-in GitHub issue/PR tools, linking artifacts back to a session via `CLAUDE_CODE_REMOTE_SESSION_ID`, running tests/services/packages, the resource ceilings, and how to configure environments (network access, variables, setup script, and the `/remote-env` default).

## What's available in cloud sessions

Cloud sessions start from a fresh clone of your repository. Anything committed to the repo is available; anything installed or configured only on your own machine is not.

**Available (part of the clone):**

- Your repo's `CLAUDE.md`
- Your repo's `.claude/settings.json` hooks
- Your repo's `.mcp.json` MCP servers
- Your repo's `.claude/rules/`
- Your repo's `.claude/skills/`, `.claude/agents/`, `.claude/commands/`
- Plugins declared in `.claude/settings.json` — installed at session start from the marketplace you declared (requires network access to reach the marketplace source)

**Not available:**

- Your user `~/.claude/CLAUDE.md` — lives on your machine, not in the repo
- Your user `~/.claude/skills/`, `~/.claude/agents/`, `~/.claude/commands/` — commit them to the repo's `.claude/` directory instead. Skills you enable on claude.ai are loaded into cloud sessions automatically.
- Plugins enabled only in your user settings — user-scoped `enabledPlugins` lives in `~/.claude/settings.json`; declare them in the repo's `.claude/settings.json` instead
- MCP servers you added with `claude mcp add` — these write to your local user config, not the repo; declare the server in `.mcp.json` instead
- Static API tokens and credentials — no dedicated secrets store exists yet
- Interactive auth like AWS SSO — not supported; SSO requires browser-based login that can't run in a cloud session

To make configuration available in cloud sessions, commit it to the repo. A dedicated secrets store is not yet available. Both environment variables and setup scripts are stored in the environment configuration, **visible to anyone who can edit that environment** — add secrets as environment variables with that visibility in mind.

## Installed tools

Cloud sessions come with common language runtimes, build tools, and databases pre-installed, by category:

- **Python** — Python 3.x with pip, poetry, uv, black, mypy, pytest, ruff
- **Node.js** — 20, 21, and 22 via nvm, with npm, yarn, pnpm, bun, eslint, prettier, chromedriver
- **Ruby** — 3.1, 3.2, 3.3 with gem, bundler, rbenv
- **PHP** — 8.4 with Composer
- **Java** — OpenJDK 21 with Maven and Gradle
- **Go** — latest stable with module support
- **Rust** — rustc and cargo
- **C/C++** — GCC, Clang, cmake, ninja, conan
- **Docker** — docker, dockerd, docker compose
- **Databases** — PostgreSQL 16, Redis 7.0
- **Utilities** — git, jq, yq, ripgrep, tmux, vim, nano

Bun is installed but has known proxy compatibility issues for package fetching. For exact versions, ask Claude to run `check-tools` in a cloud session — this command only exists in cloud sessions.

## Work with GitHub issues and pull requests

Cloud sessions include **built-in GitHub tools** that let Claude read issues, list pull requests, fetch diffs, and post comments without any setup. These tools authenticate through the GitHub proxy using whichever method you configured under GitHub authentication options, so your token never enters the container.

The `gh` CLI is **not** pre-installed. If you need a `gh` command the built-in tools don't cover (like `gh release` or `gh workflow run`), install and authenticate it yourself: add `apt update && apt install -y gh` to your setup script, then add a `GH_TOKEN` environment variable with a GitHub personal access token to your environment settings (`gh` reads `GH_TOKEN` automatically, so no `gh auth login` step is needed).

## Link artifacts back to the session

Each cloud session has a transcript URL on claude.ai, and the session can read its own ID from the `CLAUDE_CODE_REMOTE_SESSION_ID` environment variable. Use this to put a traceable link in PR bodies, commit messages, Slack posts, or generated reports so a reviewer can open the run that produced them.

The variable's value uses a `cse_` prefix, while the transcript URL path takes the same ID with a `session_` prefix — substitute the prefix when building the link. The following command prints the URL:

```bash
echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID/#cse_/session_}"
```

## Run tests, start services, and add packages

Claude runs tests as part of working on a task — ask for it in your prompt (e.g. "fix the failing tests in `tests/`"). Test runners like pytest, jest, and cargo test work out of the box since they're pre-installed.

PostgreSQL and Redis are pre-installed but **not running by default** — ask Claude to start each one during the session (e.g. `service postgresql start`, `service redis-server start`). Docker is available for containerized services; network access to pull images follows your environment's access level, and the Trusted defaults include Docker Hub and other common registries.

If your images are large or slow to pull, add `docker compose pull` or `docker compose build` to your setup script. The pulled images are saved in the cached environment, so each new session has them on disk; the cache stores files only, not running processes, so Claude still starts the containers each session. Likewise, packages installed via a setup script are cached and available at the start of every session without reinstalling. You can also ask Claude to install packages mid-session, but those installs don't carry over to other sessions.

## Resource limits

Cloud sessions run with approximate resource ceilings that may change over time: **4 vCPUs, 16 GB of RAM, 30 GB of disk**. Tasks requiring significantly more memory, such as large build jobs or memory-intensive tests, may fail or be terminated. For workloads beyond these limits, use [Remote Control](cc_remote_control.md) to run Claude Code on your own hardware.

## Configure your environment

Environments control network access, environment variables, and the setup script that runs before a session starts. You can manage environments from the web interface or the terminal:

- **Add an environment** — select the current environment to open the selector, then select **Add environment**. The dialog includes name, network access level, environment variables, and setup script.
- **Edit an environment** — select the cloud icon showing the current environment's name to open the selector, hover over an environment, and click the settings icon on the right.
- **Archive an environment** — open the environment for editing and select **Archive**. Archived environments are hidden from the selector but existing sessions keep running.
- **Set the default for `--remote`** — run `/remote-env` in your terminal. If you have a single environment, this command shows your current configuration. `/remote-env` only selects the default; add, edit, and archive environments from the web interface.

Environment variables use `.env` format with one `KEY=value` pair per line. Don't wrap values in quotes, since quotes are stored as part of the value:

```text
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgres://localhost:5432/myapp
```

**Source**: https://code.claude.com/docs/en/claude-code-on-the-web
**Last Updated**: 2026-06-13
**Status**: Active
