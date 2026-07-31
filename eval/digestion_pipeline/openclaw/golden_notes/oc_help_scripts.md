---
tags:
  - resource
  - documentation
  - openclaw
  - help
  - scripts
keywords:
  - openclaw scripts directory
  - repo helper scripts
  - prefer cli over scripts
  - auth monitoring scripts
  - gh-read github app token
  - openclaw_gh_read env vars
  - github app installation token
  - repo resolution order
topics:
  - OpenClaw
  - Help
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/help/scripts
access_control_group: ["general"]
---

# OpenClaw — Repository Helper Scripts (`scripts/`)

## Overview

This note documents OpenClaw's `scripts/` helper directory and the operator conventions for using it, mirroring the `help/scripts` source page. It covers the four sections of that page: the usage conventions (scripts are optional, prefer the CLI, scripts are host-specific), the auth-monitoring extras for systemd/Termux phone workflows, the `gh-read` GitHub-App read-token helper with its required/optional env vars and repo-resolution order, and the guidance for when you add new scripts. The `scripts/` directory holds helper scripts for local workflows and ops tasks; use them when a task is clearly tied to a script, and otherwise prefer the CLI.

## Conventions

The `scripts/` directory contains helper scripts for local workflows and ops tasks. The page states three conventions for working with them:

- Scripts are **optional** unless referenced in docs or release checklists.
- Prefer CLI surfaces when they exist (example: auth monitoring uses `openclaw models status --check`).
- Assume scripts are host-specific; read them before running on a new machine.

The operative rule is that a script is only the right tool when a task is clearly tied to a script; otherwise the CLI is preferred over running a repo script.

## Auth monitoring scripts

Auth monitoring is covered in the gateway Authentication doc (`/gateway/authentication`). The scripts under `scripts/` are optional extras for systemd/Termux phone workflows. They are not the primary path — auth monitoring itself uses the CLI surface `openclaw models status --check`, and the `scripts/` extras only exist to support systemd / Termux phone setups.

## GitHub read helper (`gh-read`)

Use `scripts/gh-read` when you want `gh` to use a GitHub App installation token for repo-scoped read calls while leaving normal `gh` on your personal login for write actions. This splits read access (a scoped GitHub-App installation token) from write actions (your personal `gh` login).

### Required env

- `OPENCLAW_GH_READ_APP_ID`
- `OPENCLAW_GH_READ_PRIVATE_KEY_FILE`

### Optional env

- `OPENCLAW_GH_READ_INSTALLATION_ID` — set when you want to skip repo-based installation lookup.
- `OPENCLAW_GH_READ_PERMISSIONS` — a comma-separated override for the read permission subset to request.

### Repo resolution order

`gh-read` resolves which repository to scope the token to in this order:

- `gh ... -R owner/repo`
- `GH_REPO`
- `git remote origin`

### Examples

```
scripts/gh-read pr view 123
scripts/gh-read run list -R openclaw/openclaw
scripts/gh-read api repos/openclaw/openclaw/pulls/123
```

## When adding scripts

When you add a script to the `scripts/` directory:

- Keep scripts focused and documented.
- Add a short entry in the relevant doc (or create one if missing).

**Source**: OpenClaw documentation — `help/scripts` (mirror `inbox/openclaw_docs/help/scripts.md`)
**Last Updated**: 2026-06-22
**Status**: Active
