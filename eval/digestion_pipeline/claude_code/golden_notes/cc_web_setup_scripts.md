---
tags:
  - resource
  - documentation
  - claude_code
  - web
  - setup_scripts
keywords:
  - setup script
  - environment caching
  - sessionstart hook
  - cloud session provisioning
  - claude_code_remote
  - claude_env_file
  - dependency install
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

# Claude Code on the Web — Setup Scripts

## Overview

A **setup script** is a Bash script that runs when a new Claude Code on the web cloud session starts, **before Claude Code launches**, and is used to install dependencies, configure tools, or fetch anything the session needs that isn't pre-installed. Scripts run **as root on Ubuntu 24.04**, so `apt install` and most language package managers work. You add a setup script in the environment settings dialog's **Setup script** field.

This note covers how to author a setup script (exit-code semantics, the ~5-minute runtime budget), how **environment caching** snapshots the post-setup filesystem so later sessions start fast, when to use a setup script versus a repo-committed **SessionStart hook**, and how to install dependencies only in the cloud with a SessionStart hook gated on the `CLAUDE_CODE_REMOTE` environment variable.

## Authoring a Setup Script

This example installs the `gh` CLI, which isn't pre-installed:

```bash theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Key authoring rules from the source:

- **Exit code matters.** If the script exits non-zero, the session fails to start. Append `|| true` to non-critical commands to avoid blocking the session on an intermittent install failure.
- **Stay under ~5 minutes.** Keep the script's total runtime under roughly five minutes so the environment cache can build. Run independent installs in parallel with `&` and `wait`. If a single download won't fit in the five-minute limit, move it to a SessionStart hook that launches it in the background.
- **Network access is required for installs.** Setup scripts that install packages need network access to reach registries. The default **Trusted** network access allows connections to common package registries including npm, PyPI, RubyGems, and crates.io. Scripts will fail to install packages if your environment uses **None** network access.

## Environment Caching

The setup script runs the **first time** you start a session in an environment. After it completes, Anthropic snapshots the filesystem and reuses that snapshot as the starting point for later sessions. New sessions start with your dependencies, tools, and Docker images already on disk, and the setup script step is skipped — keeping startup fast even when the script installs large toolchains or pulls container images.

The cache captures **files, not running processes.** Anything the setup script writes to disk carries over. Services or containers it starts do not, so start those per session by asking Claude or with a SessionStart hook.

The setup script runs again to rebuild the cache when:

- you change the environment's setup script or allowed network hosts, **or**
- the cache reaches its expiry after roughly seven days.

Resuming an existing session never re-runs the setup script. You don't need to enable caching or manage snapshots yourself.

## Setup Scripts vs. SessionStart Hooks

Use a **setup script** to install things the cloud needs but your laptop already has, like a language runtime or CLI tool. Use a **SessionStart hook** (see [hooks#sessionstart](https://code.claude.com/docs/en/hooks)) for project setup that should run everywhere, cloud and local, like `npm install`. Both run at the start of a session but belong to different places:

|               | Setup scripts | SessionStart hooks |
| ------------- | ------------- | ------------------ |
| Attached to   | The cloud environment | Your repository |
| Configured in | Cloud environment UI | `.claude/settings.json` in your repo |
| Runs          | Before Claude Code launches, when no cached environment is available | After Claude Code launches, on every session including resumed |
| Scope         | Cloud environments only | Both local and cloud |

SessionStart hooks can also be defined in your user-level `~/.claude/settings.json` locally, but user-level settings don't carry over to cloud sessions. In the cloud, only hooks committed to the repo run.

## Install Dependencies with a SessionStart Hook

To install dependencies only in cloud sessions, add a SessionStart hook to your repo's `.claude/settings.json`. The source's example registers a `command`-type hook under `"SessionStart"` with `"matcher": "startup|resume"` that runs `"$CLAUDE_PROJECT_DIR"/scripts/install_pkgs.sh`. Create the script at `scripts/install_pkgs.sh` and make it executable with `chmod +x`.

The `CLAUDE_CODE_REMOTE` environment variable is set to `true` in cloud sessions, so you can use it to skip local execution:

```bash theme={null}
#!/bin/bash

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

SessionStart hooks have some limitations in cloud sessions:

- **No cloud-only scoping**: hooks run in both local and cloud sessions. To skip local execution, check the `CLAUDE_CODE_REMOTE` environment variable as shown above.
- **Requires network access**: install commands need to reach package registries. If your environment uses **None** network access, these hooks fail. The default allowlist under **Trusted** covers npm, PyPI, RubyGems, and crates.io.
- **Proxy compatibility**: all outbound traffic passes through a security proxy. Some package managers don't work correctly with this proxy. Bun is a known example.
- **Adds startup latency**: hooks run each time a session starts or resumes, unlike setup scripts which benefit from environment caching. Keep install scripts fast by checking whether dependencies are already present before reinstalling.

To persist environment variables for subsequent Bash commands, write to the file at `$CLAUDE_ENV_FILE` (see [SessionStart hooks](https://code.claude.com/docs/en/hooks) for details).

Replacing the base image with your own Docker image is not yet supported. Use a setup script to install what you need on top of the provided image, or run your image as a container alongside Claude with `docker compose`.

**Source**: https://code.claude.com/docs/en/claude-code-on-the-web
**Last Updated**: 2026-06-13
**Status**: Active
