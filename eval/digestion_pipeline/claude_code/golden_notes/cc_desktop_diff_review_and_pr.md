---
tags:
  - resource
  - documentation
  - claude_code
  - desktop
  - diff_review
keywords:
  - diff view
  - review code
  - pull request monitoring
  - auto-fix auto-merge
  - app preview
  - auto-verify
  - launch.json preview server
  - autoport port conflicts
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

# Claude Desktop — Diff Review, Code Review & PR Monitoring

## Overview

In the Claude Desktop **Code** tab, after Claude edits your code you move through a verify-and-review loop before and after opening a pull request. Claude can preview the running app in an embedded browser and **auto-verify** its own changes; you then review modifications file-by-file in the **diff view**, leave inline line comments, ask Claude to **Review code** for a self-review of high-signal issues, and finally **monitor pull request status** with optional auto-fix and auto-merge.

This note covers that workflow plus the **preview-server configuration** (`.claude/launch.json`) that backs the app-preview step — its configuration fields, the `program` vs `runtimeExecutable` choice, `autoPort` conflict handling, and `autoVerify`. The permission-mode and workspace-pane surfaces these features live alongside are documented in sibling notes.

## Preview your app

Claude can start a dev server and open an embedded browser to verify its changes. This works for frontend web apps as well as backend servers: Claude can test API endpoints, view server logs, and iterate on issues it finds. In most cases, Claude starts the server automatically after editing project files, but you can also ask Claude to preview at any time. By default, Claude auto-verifies changes after every edit.

The preview pane can also open static HTML files, PDFs, images, and videos from your project. Click an HTML, PDF, image, or video path in the chat to open it in preview.

From the preview pane, you can:

- Interact with your running app directly in the embedded browser.
- Watch Claude verify its own changes automatically: it takes screenshots, inspects the DOM, clicks elements, fills forms, and fixes issues it finds.
- Start or stop servers from the **Preview** dropdown in the session toolbar.
- Persist cookies and local storage across server restarts by selecting **Persist sessions** in the dropdown, so you don't have to re-login during development.
- Edit the server configuration or stop all servers at once.

Claude creates the initial server configuration based on your project. If your app uses a custom dev command, edit `.claude/launch.json` to match your setup (see [Configure preview servers](#configure-preview-servers)). To clear saved session data, toggle **Persist preview sessions** off in Settings → Claude Code. To disable preview entirely, toggle off **Preview** in Settings → Claude Code.

## Review changes with diff view

After Claude makes changes to your code, the diff view lets you review modifications file by file before creating a pull request.

When Claude changes files, a diff stats indicator appears showing the number of lines added and removed, such as `+12 -1`. Click this indicator to open the diff viewer, which displays a file list on the left and the changes for each file on the right.

To comment on specific lines, click any line in the diff to open a comment box. Type your feedback and press **Enter** to add the comment. After adding comments to multiple lines, submit all comments at once:

- **macOS**: press **Cmd+Enter**
- **Windows**: press **Ctrl+Enter**

Claude reads your comments and makes the requested changes, which appear as a new diff you can review.

## Review your code

In the diff view, click **Review code** in the top-right toolbar to ask Claude to evaluate the changes before you commit. Claude examines the current diffs and leaves comments directly in the diff view. You can respond to any comment or ask Claude to revise.

The review focuses on high-signal issues: compile errors, definite logic errors, security vulnerabilities, and obvious bugs. It does not flag style, formatting, pre-existing issues, or anything a linter would catch.

## Monitor pull request status

After you open a pull request, a CI status bar appears in the session. Claude Code uses the GitHub CLI to poll check results and surface failures.

- **Auto-fix**: when enabled, Claude automatically attempts to fix failing CI checks by reading the failure output and iterating.
- **Auto-merge**: when enabled, Claude merges the PR once all checks pass. The merge method is squash. Auto-merge must be enabled in your GitHub repository settings for this to work.

Use the **Auto-fix** and **Auto-merge** toggles in the CI status bar to enable either option. Claude Code also sends a desktop notification when CI finishes. To archive the session automatically once the PR merges or closes, turn on auto-archive in Settings → Claude Code.

> **Note:** PR monitoring requires the GitHub CLI (`gh`) to be installed and authenticated on your machine. If `gh` is not installed, Desktop prompts you to install it the first time you try to create a PR.

## Configure preview servers

Claude automatically detects your dev server setup and stores the configuration in `.claude/launch.json` at the root of the folder you selected when starting the session. Preview uses this folder as its working directory, so if you selected a parent folder, subfolders with their own dev servers won't be detected automatically. To work with a subfolder's server, either start a session in that folder directly or add a configuration manually.

To customize how your server starts — for example to use `yarn dev` instead of `npm run dev` or to change the port — edit the file manually or click **Edit configuration** in the Preview dropdown to open it in your code editor. The file supports JSON with comments.

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

You can define multiple configurations to run different servers from the same project, such as a frontend and an API.

### Auto-verify changes

When `autoVerify` is enabled, Claude automatically verifies code changes after editing files. It takes screenshots, checks for errors, and confirms changes work before completing its response.

Auto-verify is on by default. Disable it per-project by adding `"autoVerify": false` to `.claude/launch.json`, or toggle it from the **Preview** dropdown menu. When disabled, preview tools are still available and you can ask Claude to verify at any time; auto-verify makes it automatic after every edit.

```json theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

### Configuration fields

Each entry in the `configurations` array accepts the following fields:

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | A unique identifier for this server. |
| `runtimeExecutable` | string | The command to run, such as `npm`, `yarn`, or `node`. |
| `runtimeArgs` | string[] | Arguments passed to `runtimeExecutable`, such as `["run", "dev"]`. |
| `port` | number | The port your server listens on. Defaults to 3000. |
| `cwd` | string | Working directory relative to your project root. Defaults to the project root. Use `${workspaceFolder}` to reference the project root explicitly. |
| `env` | object | Additional environment variables as key-value pairs, such as `{ "NODE_ENV": "development" }`. Don't put secrets here since this file is committed to your repo; set dev-server secrets in the local environment editor instead. |
| `autoPort` | boolean | How to handle port conflicts (see below). |
| `program` | string | A script to run with `node` (see `program` vs `runtimeExecutable`). |
| `args` | string[] | Arguments passed to `program`. Only used when `program` is set. |

### When to use `program` vs `runtimeExecutable`

Use `runtimeExecutable` with `runtimeArgs` to start a dev server through a package manager. For example, `"runtimeExecutable": "npm"` with `"runtimeArgs": ["run", "dev"]` runs `npm run dev`.

Use `program` when you have a standalone script you want to run with `node` directly. For example, `"program": "server.js"` runs `node server.js`. Pass additional flags with `args`.

### Port conflicts

The `autoPort` field controls what happens when your preferred port is already in use:

- **`true`**: Claude finds and uses a free port automatically. Suitable for most dev servers.
- **`false`**: Claude fails with an error. Use this when your server must use a specific port, such as for OAuth callbacks or CORS allowlists.
- **Not set (default)**: Claude asks whether the server needs that exact port, then saves your answer.

When Claude picks a different port, it passes the assigned port to your server via the `PORT` environment variable.

### Examples

A multi-server monorepo configuration shows the fields working together: the frontend uses `autoPort: true` so it picks a free port if 3000 is taken, while the API server requires port 8080 exactly. (Single-server `runtimeExecutable` and `program`-based node-script configurations follow the same shape — see the first block above and the `program` vs `runtimeExecutable` section.)

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "frontend",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "cwd": "apps/web",
      "port": 3000,
      "autoPort": true
    },
    {
      "name": "api",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "start"],
      "cwd": "server",
      "port": 8080,
      "env": { "NODE_ENV": "development" },
      "autoPort": false
    }
  ]
}
```

**Source**: https://code.claude.com/docs/en/desktop
**Last Updated**: 2026-06-13
**Status**: Active
