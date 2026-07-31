---
tags:
  - resource
  - documentation
  - claude_code
  - settings
  - permissions
keywords:
  - permission settings
  - permissions allow ask deny
  - permission rule syntax
  - attribution settings
  - git commit trailers
  - file suggestion settings
  - additionalDirectories
  - defaultMode
topics:
  - Claude Code
  - Settings
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/settings
access_control_group: ["general"]
---

# Claude Code — Permission, Attribution & File Suggestion Settings

## Overview

This note covers four grouped `settings.json` sub-tables that govern how Claude Code is allowed to act and how it identifies its work: **permission settings** (the `permissions.*` keys that allow/ask/deny tool use, grant extra directories, and set the default mode), the **quick permission rule syntax** (the `Tool` / `Tool(specifier)` format and evaluation order), **attribution settings** (the `attribution.{commit,pr}` git trailers and PR text), and **file suggestion settings** (a custom `@`-autocomplete command). These are procedural reference fields — one purpose per key.

The full permission rule syntax (wildcard behavior, tool-specific Read/Edit/WebFetch/MCP/Agent patterns, Bash security limitations) is owned by the permissions page and is linked out rather than duplicated here. Sandbox filesystem/network keys and excluding sensitive files via `permissions.deny` are documented in the sibling [Sandbox Settings](cc_sandbox_settings.md) note.

## Permission settings

The `permissions` object holds the keys that control which tools Claude Code may run and where it may read/write:

| Key | Description | Example |
| :-- | :-- | :-- |
| `allow` | Array of permission rules to allow tool use. Tool-name globs are supported only in the tool position after a literal `mcp__<server>__` prefix, such as `mcp__github__get_*`; the server segment must be glob-free. | `[ "Bash(git diff *)" ]` |
| `ask` | Array of permission rules to ask for confirmation upon tool use. | `[ "Bash(git push *)" ]` |
| `deny` | Array of permission rules to deny tool use. Use this to exclude sensitive files from Claude Code access. Tool names accept glob patterns: `"*"` denies every tool and `"mcp__*"` denies all MCP tools. | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories` | Additional working directories for file access. Most `.claude/` configuration is not discovered from these directories. | `[ "../docs/" ]` |
| `defaultMode` | Default permission mode when opening Claude Code. Valid values: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. As of Claude Code v2.1.142, `auto` is ignored when set in project or local settings (`.claude/settings.json`, `.claude/settings.local.json`) so a repository cannot grant itself auto mode — set it in `~/.claude/settings.json` instead. The `--permission-mode` CLI flag overrides this setting for a single session. | `"acceptEdits"` |
| `disableBypassPermissionsMode` | Set to `"disable"` to prevent `bypassPermissions` mode from being activated. This disables the `--dangerously-skip-permissions` command-line flag. Typically placed in managed settings to enforce organizational policy, but works from any scope. | `"disable"` |
| `skipDangerousModePermissionPrompt` | Skip the confirmation prompt shown before entering bypass permissions mode via `--dangerously-skip-permissions` or `defaultMode: "bypassPermissions"`. Ignored when set in project settings (`.claude/settings.json`) to prevent untrusted repositories from auto-bypassing the prompt. | `true` |

Unlike most scalar settings, permission rules **merge across scopes** rather than override (managed, local, project, and user `allow`/`ask`/`deny` arrays are combined), as noted in [Settings Scopes and Precedence](cc_settings_scopes_and_precedence.md).

## Permission rule syntax (quick)

Permission rules follow the format `Tool` or `Tool(specifier)`. Rules are evaluated in order: **deny rules first, then ask, then allow.** The first match determines the outcome regardless of rule specificity.

Quick examples:

| Rule | Effect |
| :-- | :-- |
| `Bash` | Matches all Bash commands |
| `Bash(npm run *)` | Matches commands starting with `npm run` |
| `Read(./.env)` | Matches reading the `.env` file |
| `WebFetch(domain:example.com)` | Matches fetch requests to example.com |

For the complete rule syntax reference — including wildcard behavior, tool-specific patterns for Read, Edit, WebFetch, MCP, and Agent rules, and security limitations of Bash patterns — see the [full Permission rule syntax](https://code.claude.com/docs/en/permissions).

## Attribution settings

Claude Code adds attribution to git commits and pull requests. These are configured separately under the `attribution` key:

- Commits use [git trailers](https://git-scm.com/docs/git-interpret-trailers) (like `Co-Authored-By`) by default, which can be customized or disabled.
- Pull request descriptions are plain text.

| Key | Description |
| :-- | :-- |
| `commit` | Attribution for git commits, including any trailers. Empty string hides commit attribution. |
| `pr` | Attribution for pull request descriptions. Empty string hides pull request attribution. |

**Default commit attribution** (the model name in the trailer reflects the active model for the session):

```text
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Default pull request attribution:**

```text
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Example** `settings.json` overriding both:

```json
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

The `attribution` setting takes precedence over the deprecated `includeCoAuthoredBy` setting. To hide all attribution, set `commit` and `pr` to empty strings.

## File suggestion settings

The `fileSuggestion` key configures a custom command for `@` file path autocomplete. The built-in file suggestion uses fast filesystem traversal, but large monorepos may benefit from project-specific indexing such as a pre-built file index or custom tooling.

The command runs with the same environment variables as hooks, including `CLAUDE_PROJECT_DIR`. It receives JSON via stdin with a `query` field (e.g. `{"query": "src/comp"}`) and must output newline-separated file paths to stdout (currently limited to 15). An example custom script:

```bash
#!/bin/bash
query=$(cat | jq -r '.query')
# Replace your-repo-file-index with your own file search command
your-repo-file-index --query "$query" | head -20
```

**Source**: https://code.claude.com/docs/en/settings
**Last Updated**: 2026-06-13
**Status**: Active
