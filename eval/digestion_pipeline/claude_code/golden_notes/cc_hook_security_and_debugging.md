---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - security
keywords:
  - hook security
  - full user permissions
  - trust boundary
  - validate and sanitize inputs
  - block path traversal
  - skip sensitive files
  - windows powershell hook
  - debug hooks
  - claude code debug log level
topics:
  - Claude Code
  - Hooks
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/hooks
access_control_group: ["general"]
---

# Claude Code — Hook Security and Debugging

## Overview

Command hooks are a powerful but dangerous Claude Code mechanism: they run shell commands with the system user's **full permissions**, so a careless or attacker-influenced hook can modify, delete, or read any file the user can. This note makes the argument that a hook is a trust boundary that must be operated defensively — validate inputs, quote variables, block path traversal, skip sensitive files — and shows the two operational affordances that support safe use: the Windows PowerShell `shell` option for cross-platform hooks, and the debug log for observing exactly which hooks matched and how they behaved. Hard allow/deny policy belongs in the [permission system](https://code.claude.com/docs/en/permissions), not a best-effort hook (see the `if`-filter caveat in [Matchers and filters](https://code.claude.com/docs/en/hooks)).

## Security considerations

### Disclaimer

Command hooks run with your system user's full permissions.

> **Warning:** Command hooks execute shell commands with your full user permissions. They can modify, delete, or access any files your user account can access. Review and test all hook commands before adding them to your configuration.

Because hook input can carry untrusted data (a tool's arguments or output flow into the hook on stdin), the hook is an enforcement point that must treat its input as adversarial. Context a hook injects via `additionalContext` is also a surface: text framed as out-of-band system commands can trip Claude's prompt-injection defenses, which is why hook output should be phrased as factual statements (see [I/O and exit codes](cc_hook_io_and_exit_codes.md)).

### Security best practices

Keep these practices in mind when writing hooks:

- **Validate and sanitize inputs**: never trust input data blindly.
- **Always quote shell variables**: use `"$VAR"` not `$VAR`.
- **Block path traversal**: check for `..` in file paths.
- **Use absolute paths**: specify full paths for scripts. In exec form, use `${CLAUDE_PROJECT_DIR}` and the path needs no quoting; in shell form, wrap it in double quotes.
- **Skip sensitive files**: avoid `.env`, `.git/`, keys, etc.

## Windows PowerShell tool

On Windows, you can run individual hooks in PowerShell by setting `"shell": "powershell"` on a command hook. Hooks spawn PowerShell directly, so this works regardless of whether `CLAUDE_CODE_USE_POWERSHELL_TOOL` is set. Claude Code auto-detects `pwsh.exe` (PowerShell 7+) with a fallback to `powershell.exe` (5.1).

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "Write-Host 'File written'"
          }
        ]
      }
    ]
  }
}
```

## Debug hooks

Hook execution details — including which hooks matched, their exit codes, and full stdout and stderr — are written to the debug log file. Start Claude Code with `claude --debug-file <path>` to write the log to a known location, or run `claude --debug` and read the log at `~/.claude/debug/<session-id>.txt`. The `--debug` flag does not print to the terminal.

```text theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

For more granular hook matching details, set `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose` to see additional log lines such as hook matcher counts and query matching.

For troubleshooting common issues like hooks not firing, Stop hooks that keep blocking, or configuration errors, see [Limitations and troubleshooting](https://code.claude.com/docs/en/hooks-guide#limitations-and-troubleshooting) in the guide. For a broader diagnostic walkthrough covering `/context`, `/doctor`, and settings precedence, see [Debug your config](https://code.claude.com/docs/en/debug-your-config).

**Source**: https://code.claude.com/docs/en/hooks
**Last Updated**: 2026-06-13
**Status**: Active
