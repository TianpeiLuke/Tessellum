---
tags:
  - resource
  - documentation
  - claude_code
  - permissions
  - hooks
keywords:
  - pretooluse hook permission evaluation
  - deny-first precedence preserved
  - exit code 2 block
  - working directories
  - additional directories
  - add-dir flag
  - additionaldirectories setting
  - cd session relocation
topics:
  - Claude Code
  - Permissions
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/permissions
access_control_group: ["general"]
---

# Claude Code — Permission Hooks and Working Directories

## Overview

Two mechanisms extend Claude Code's permission system beyond static allow/ask/deny rules: **PreToolUse hooks**, which run custom shell logic to evaluate a tool call at runtime, and **working directories**, which define the file-access boundary the permission rules apply within. Hooks can deny a tool call, force a prompt, or skip the prompt — but they never bypass the deny-first precedence that the rules enforce. Working directories start at the launch directory and can be extended at startup, mid-session, or persistently, with additional directories following the same per-mode permission rules.

This note covers the conceptual interaction of these two features with the permission model. Hook *authoring* (writing the hook scripts, the `PreToolUse`/`PermissionRequest`/`PermissionDenied` event contracts) is documented in the [Hooks guide](https://code.claude.com/docs/en/hooks-guide); CLI flag reference (`--add-dir`) and the `/cd` / `/add-dir` command reference are documented in the [commands reference](https://code.claude.com/docs/en/commands).

## Extend permissions with hooks

[Claude Code hooks](https://code.claude.com/docs/en/hooks-guide) register custom shell commands that perform permission evaluation at runtime. When Claude Code makes a tool call, **PreToolUse hooks run before the permission prompt**. The hook output can:

- **deny** the tool call,
- **force a prompt**, or
- **skip the prompt** to let the call proceed.

Hook decisions do **not** bypass permission rules. Deny and ask rules are evaluated regardless of what a PreToolUse hook returns, so a matching deny rule blocks the call and a matching ask rule still prompts even when the hook returned `"allow"` or `"ask"`. This preserves the deny-first precedence described under Manage permissions (see [`cc_permission_system_and_rules`](cc_permission_system_and_rules.md)), **including deny rules set in managed settings** (see [`cc_managed_permission_settings_and_precedence`](cc_managed_permission_settings_and_precedence.md)).

A blocking hook also takes precedence over allow rules. **A hook that exits with code 2 stops the tool call before permission rules are evaluated**, so the block applies even when an allow rule would otherwise let the call proceed. To run all Bash commands without prompts except for a few you want blocked, add `"Bash"` to your allow list and register a PreToolUse hook that rejects those specific commands.

## Working directories

By default, Claude has access to files in the directory where it was launched. You can extend this access three ways:

- **During startup**: use the `--add-dir <path>` CLI argument.
- **During session**: use the `/add-dir` command.
- **Persistent configuration**: add to `additionalDirectories` in [settings files](https://code.claude.com/docs/en/settings#settings-files).

Files in additional directories follow the **same permission rules** as the original working directory: they become readable without prompts, and file-editing permissions follow the current permission mode (see [`cc_permission_modes_overview`](cc_permission_modes_overview.md)).

To change the session's primary working directory instead of adding another, use `/cd`. The `/cd` command requires Claude Code v2.1.169 or later. Unlike `/add-dir`, it **relocates the session**: the new directory's `CLAUDE.md` is loaded and `--resume` finds the session from there.

### Additional directories grant file access, not configuration

Adding a directory extends where Claude can read and edit files. It does **not** make that directory a full configuration root: most `.claude/` configuration is not discovered from additional directories, though a few types are loaded as exceptions.

These exceptions apply **only** to directories added with the `--add-dir` flag or the `/add-dir` command. Directories listed in `permissions.additionalDirectories` in a settings file grant **file access only** and do not load any configuration.

The following configuration types are loaded from `--add-dir` directories:

- **Skills** in `.claude/skills/` — loaded, with live reload.
- **Plugin settings** in `.claude/settings.json` — `enabledPlugins` and `extraKnownMarketplaces` only.
- **CLAUDE.md files, `.claude/rules/`, and `CLAUDE.local.md`** — loaded only when `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` is set. `CLAUDE.local.md` additionally requires the `local` setting source, which is enabled by default.

Subagents, commands, and output styles are discovered from the current working directory and its parents, your user directory at `~/.claude/`, and managed settings. Hooks and other `settings.json` keys load from the current working directory's `.claude/` folder with no parent-directory fallback, alongside your user `~/.claude/settings.json` and managed settings. To share that configuration across projects, use one of these approaches:

- **User-level configuration**: place files in `~/.claude/agents/`, `~/.claude/output-styles/`, or `~/.claude/settings.json` to make them available in every project.
- **Plugins**: package and distribute configuration as a plugin that teams can install.
- **Launch from the config directory**: run Claude Code from the directory containing the `.claude/` configuration you want.

**Source**: https://code.claude.com/docs/en/permissions
**Last Updated**: 2026-06-13
**Status**: Active
