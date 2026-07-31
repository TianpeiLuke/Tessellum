---
tags:
  - resource
  - documentation
  - claude_code
  - sandboxing
  - permissions
keywords:
  - sandbox modes
  - auto-allow mode
  - regular permissions mode
  - dangerouslydisablesandbox escape hatch
  - allowunsandboxedcommands strict mode
  - deny rules ask rules
  - tmpdir session temp directory
  - sandboxed bash tool
topics:
  - Claude Code
  - Sandboxing
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/sandboxing
access_control_group: ["general"]
---

# Claude Code — Sandbox Modes

## Overview

Claude Code's sandboxed Bash tool offers **two sandbox modes** that decide how sandboxed commands are approved: **auto-allow mode**, which runs sandboxed commands without prompting, and **regular permissions mode**, which keeps the regular permission prompts even when commands are sandboxed. The mode is chosen on the Mode tab of the `/sandbox` panel. In both modes the sandbox enforces the *same* filesystem and network restrictions — the only difference is whether sandboxed commands are auto-approved or require explicit permission.

This note covers what each mode does, the always-on exceptions that still prompt even under auto-allow (deny rules, critical-path `rm`/`rmdir`, content-scoped ask rules), the `dangerouslyDisableSandbox` escape hatch for commands that cannot run sandboxed, the `allowUnsandboxedCommands: false` / **Strict sandbox mode** override that closes that hatch, and how the session temp directory (`$TMPDIR`) is handled.

## Auto-allow mode

In **auto-allow mode**, Bash commands attempt to run inside the sandbox and are automatically allowed without requiring permission. Commands that cannot be sandboxed — such as those needing network access to non-allowed hosts — fall back to the **regular permission flow**, where Claude Code checks your permission rules and prompts you for any command those rules do not already allow.

Even in auto-allow mode, the following still apply:

- Explicit **deny rules** are always respected.
- `rm` or `rmdir` commands that target `/`, your home directory, or other critical system paths still trigger a permission prompt.
- Content-scoped **ask rules** like `Bash(git push *)` still force a prompt even for sandboxed commands.
- A bare `Bash` ask rule, or the equivalent `Bash(*)` form, is skipped for commands that run sandboxed; it still applies to commands that fall back to the regular permission flow.

Auto-allow mode works **independently of your permission mode setting**. Even if you are not in "accept edits" mode, sandboxed Bash commands run automatically when auto-allow is enabled. This means Bash commands that modify files within the sandbox boundaries execute without prompting, even when file edit tools would normally require approval.

## Regular permissions mode

In **regular permissions mode**, all Bash commands go through the regular permission flow, even when sandboxed. This provides more control but requires more approvals.

In both modes, the sandbox enforces the same filesystem and network restrictions. The difference is only in whether sandboxed commands are auto-approved or require explicit permission.

## The session temp directory and `$TMPDIR`

The session temp directory is writable inside the sandbox by default, alongside the working directory. Claude Code sets `$TMPDIR` to this directory for sandboxed commands, so tools that write temporary files work without extra configuration.

Unsandboxed commands inherit your shell's `$TMPDIR` unchanged, which means sandboxed and unsandboxed commands resolve `$TMPDIR` to different directories. To pass temporary files between the two, write them under the working directory instead.

## The `dangerouslyDisableSandbox` escape hatch

Some commands cannot run inside the sandbox at all, such as tools that are incompatible with it or that need a host you have not allowed. Rather than failing the task or requiring you to turn sandboxing off, Claude Code includes an **escape hatch**: when a command fails because of sandbox restrictions, Claude analyzes the failure and may retry the command with the `dangerouslyDisableSandbox` parameter. The retried command runs outside the sandbox, so it goes through the regular permission flow and requires your approval.

## Strict sandbox mode (`allowUnsandboxedCommands: false`)

You can disable this escape hatch by setting `"allowUnsandboxedCommands": false` in your sandbox settings. When disabled — which the `/sandbox` **Overrides** tab shows as **Strict sandbox mode** — the `dangerouslyDisableSandbox` parameter is completely ignored, and all commands must run sandboxed or be explicitly listed in `excludedCommands`.

**Source**: https://code.claude.com/docs/en/sandboxing
**Last Updated**: 2026-06-13
**Status**: Active
