---
tags:
  - resource
  - documentation
  - claude_code
  - mcp
  - configuration
keywords:
  - mcp installation scopes
  - local scope
  - project scope
  - user scope
  - scope hierarchy and precedence
  - mcp.json
  - claude.json
  - environment variable expansion
  - team sharing version control
topics:
  - Claude Code
  - MCP
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/mcp
access_control_group: ["general"]
---

# Claude Code — MCP Installation Scopes

## Overview

An MCP server's **scope** controls two things: which projects the server loads in, and whether its configuration is shared with your team. Claude Code supports three scopes — **local**, **project**, and **user** — stored across two files (`~/.claude.json` and a project-root `.mcp.json`). A server's scope is fixed when you add it, so changing scope means removing the entry and re-adding it. When the same server is defined in more than one place, Claude Code connects once using a fixed five-level **precedence** order, and `.mcp.json` supports **environment variable expansion** so teams can share a config while keeping machine-specific paths and secrets out of version control.

## The three scopes

| Scope | Loads in | Shared with team | Stored in |
|-------|----------|------------------|-----------|
| Local | Current project only | No | `~/.claude.json` |
| Project | Current project only | Yes, via version control | `.mcp.json` in project root |
| User | All your projects | No | `~/.claude.json` |

Administrators can also deploy servers at the enterprise level via [managed configuration](cc_managed_mcp_configuration.md).

**Local scope** is the default. A local-scoped server loads only in the project where you added it and stays private to you, stored in `~/.claude.json` under that project's path, so the same server won't appear in your other projects. Use it for personal development servers, experimental configurations, or servers with credentials you don't want in version control. Note that "local scope" for MCP servers differs from general local settings: MCP local-scoped servers live in `~/.claude.json` (your home directory), while general local settings use `.claude/settings.local.json` in the project directory.

**Project scope** enables team collaboration by storing configurations in a `.mcp.json` file at the project root, designed to be checked into version control so all team members share the same MCP tools and services. Adding a project-scoped server creates or updates this file. For security, Claude Code prompts for approval before using project-scoped servers from `.mcp.json`; reset those approval choices with `claude mcp reset-project-choices`.

**User scope** servers are stored in `~/.claude.json` and provide cross-project accessibility — available across all projects on your machine while remaining private to your user account. This suits personal utility servers, development tools, or services you use frequently across different projects.

## Where servers are saved on disk

`claude mcp add` writes the server into one of the three scopes, stored across two files depending on the `--scope` flag. You don't need to edit these files directly, but knowing where they live helps with debugging and version control:

| Scope | File | Available to |
|-------|------|--------------|
| `local` | `~/.claude.json`, under the entry for this project | Only you, only this project. The default |
| `project` | `.mcp.json` in your project root | Everyone who clones the project |
| `user` | `~/.claude.json`, under the top-level `mcpServers` key | Only you, all projects |

On Windows, `~/.claude.json` resolves to `%USERPROFILE%\.claude.json`, typically `C:\Users\YourName\.claude.json`. If you've set `CLAUDE_CONFIG_DIR`, Claude Code reads `.claude.json` from inside that directory instead. Run `claude mcp get <name>` to see which scope holds a server's definition.

A local-scoped server is written into the entry for your current project inside `~/.claude.json`. Run from `/path/to/your/project`, the result looks like:

```json
{
  "projects": {
    "/path/to/your/project": {
      "mcpServers": {
        "stripe": {
          "type": "http",
          "url": "https://mcp.stripe.com"
        }
      }
    }
  }
}
```

## Choosing and changing scope

You pick a scope with the `--scope` flag (`local` default, `project`, or `user`) on `claude mcp add`. Because scope is fixed at add time, **changing scope means removing the entry and re-adding it** at the new scope — for example `claude mcp remove <name> --scope local` then re-adding with `--scope user` (active in every project, still private to you) or `--scope project` (writes to `.mcp.json` for sharing). After re-adding at project scope, commit `.mcp.json` to version control: teammates who clone the repository and start Claude Code see a prompt to approve the server, then it connects for them too.

## Scope hierarchy and precedence

When the same server is defined in more than one place, Claude Code connects to it once, using the definition from the highest-precedence source. **The entire server entry from that source is used; fields are not merged across scopes.** The precedence order is:

1. Local scope
2. Project scope
3. User scope
4. Plugin-provided servers
5. claude.ai connectors

The three scopes match duplicates **by name**. Plugins and connectors match **by endpoint**, so one that points at the same URL or command as a server above is treated as a duplicate.

## Environment variable expansion in `.mcp.json`

Claude Code supports environment variable expansion in `.mcp.json` files, letting teams share configurations while maintaining flexibility for machine-specific paths and sensitive values like API keys. Two syntaxes are supported: `${VAR}` expands to the value of environment variable `VAR`, and `${VAR:-default}` expands to `VAR` if set, otherwise uses `default`. Variables can be expanded in `command` (the server executable path), `args` (command-line arguments), `env` (variables passed to the server), `url` (for HTTP server types), and `headers` (for HTTP server authentication).

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

If a required environment variable is not set and has no default value, Claude Code will fail to parse the config. (Relatedly, `CLAUDE_PROJECT_DIR` referenced via `${VAR}` in a project- or user-scoped `.mcp.json` `command` or `args` requires a default such as `${CLAUDE_PROJECT_DIR:-.}` because it is set in the spawned server's environment, not Claude Code's own — see [MCP transports](cc_mcp_transports.md).)

**Source**: https://code.claude.com/docs/en/mcp
**Last Updated**: 2026-06-13
**Status**: Active
