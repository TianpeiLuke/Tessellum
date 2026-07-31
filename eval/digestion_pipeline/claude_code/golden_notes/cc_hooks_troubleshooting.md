---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - troubleshooting
keywords:
  - hooks troubleshooting
  - hook not firing
  - hook timeouts
  - stop hook block cap
  - stop_hook_active
  - json validation failed
  - hooks and permission modes
  - debug hooks
topics:
  - Claude Code
  - Hooks
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/hooks-guide
access_control_group: ["general"]
---

# Claude Code Hooks — Limitations and Troubleshooting

## Overview

Hooks have built-in constraints and a handful of common failure modes worth knowing before you rely on them. This note covers what hooks **cannot** do (communication channels, timeouts by type, `PostToolUse` cannot undo, `PermissionRequest` does not fire in `-p` mode, `Stop` fires on every response, parallel `updatedInput` races), how hooks interact with [permission modes](https://code.claude.com/docs/en/permissions) (a deny hook fires before any permission-mode check and cannot be loosened by `"allow"`), and step-by-step diagnosis recipes for the most common problems: a hook that never fires, a hook error in the transcript, an empty `/hooks` menu, the `Stop` hook block cap, the JSON-validation profile-echo bug, and the debug techniques (`--debug-file`, `Ctrl+O`, `/debug`) used to inspect hook execution.

This is the troubleshooting companion to the hooks guide; for setup see [cc_hooks_overview_and_setup](cc_hooks_overview_and_setup.md), for the stdin/stdout/exit-code contract see [cc_hooks_io_and_decision_control](cc_hooks_io_and_decision_control.md), and for full event schemas and the debug-log reference see the [Hooks reference](https://code.claude.com/docs/en/hooks).

## Limitations

* Command hooks communicate through stdout, stderr, and exit codes only. They cannot trigger `/` commands or tool calls. Text returned via `additionalContext` is injected as a system reminder that Claude reads as plain text. HTTP hooks communicate through the response body instead.
* Hook timeouts vary by type. Override per hook with the `timeout` field in seconds.
  * `command`, `http`, `mcp_tool`: 10 minutes. `UserPromptSubmit` lowers these to 30 seconds, and `MessageDisplay` lowers them to 10 seconds.
  * `prompt`: 30 seconds.
  * `agent`: 60 seconds.
* `PostToolUse` hooks cannot undo actions since the tool has already executed.
* `PermissionRequest` hooks do not fire in [non-interactive mode](https://code.claude.com/docs/en/headless) (`-p`). Use `PreToolUse` hooks for automated permission decisions.
* `Stop` hooks fire whenever Claude finishes responding, not only at task completion. They do not fire on user interrupts. API errors fire [StopFailure](https://code.claude.com/docs/en/hooks#stopfailure) instead.
* When multiple PreToolUse hooks return [`updatedInput`](https://code.claude.com/docs/en/hooks#pretooluse) to rewrite a tool's arguments, the last one to finish wins. Since hooks run in parallel, the order is non-deterministic. Avoid having more than one hook modify the same tool's input.

## Hooks and permission modes

PreToolUse hooks fire before any permission-mode check. A hook that returns `permissionDecision: "deny"` blocks the tool even in `bypassPermissions` mode or with `--dangerously-skip-permissions`. This lets you enforce policy that users cannot bypass by changing their permission mode.

The reverse is not true: a hook returning `"allow"` does not bypass deny rules from settings. Hooks can tighten restrictions but not loosen them past what permission rules allow.

## Hook not firing

The hook is configured but never executes.

* Run `/hooks` and confirm the hook appears under the correct event
* Check that the matcher pattern matches the tool name exactly (matchers are case-sensitive)
* Verify you're triggering the right event type (e.g., `PreToolUse` fires before tool execution, `PostToolUse` fires after)
* If using `PermissionRequest` hooks in non-interactive mode (`-p`), switch to `PreToolUse` instead

## Hook error in output

You see a message like "PreToolUse hook error: ..." in the transcript.

* Your script exited with a non-zero code unexpectedly. Test it manually by piping sample JSON:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
echo $?  # Check the exit code
```

* If you see "command not found", use absolute paths or `${CLAUDE_PROJECT_DIR}` to reference scripts. To avoid shell quoting entirely, add `"args": []` to switch to [exec form](https://code.claude.com/docs/en/hooks#exec-form-and-shell-form), which spawns the script directly without a shell
* If you see "jq: command not found", install `jq` or use Python/Node.js for JSON parsing
* If the script isn't running at all, make it executable: `chmod +x ./my-hook.sh`

## `/hooks` shows no hooks configured

You edited a settings file but the hooks don't appear in the menu.

* File edits are normally picked up automatically. If they haven't appeared after a few seconds, the file watcher may have missed the change: restart your session to force a reload.
* Verify your JSON is valid (trailing commas and comments are not allowed)
* Confirm the settings file is in the correct location: `.claude/settings.json` for project hooks, `~/.claude/settings.json` for global hooks

## Stop hook hits the block cap

Claude keeps working instead of stopping, then ends the turn with a warning that the `Stop` hook blocked too many consecutive times.

Claude Code overrides a `Stop` hook after it blocks 8 times in a row without progress. Your hook script needs to check whether it already triggered a continuation. Parse the `stop_hook_active` field from the JSON input and exit early if it's `true`:

```bash
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Allow Claude to stop
fi
# ... rest of your hook logic
```

If your hook legitimately needs more than eight iterations to converge, raise the cap with [`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`](https://code.claude.com/docs/en/env-vars).

## JSON validation failed

Claude Code shows a JSON parsing error even though your hook script outputs valid JSON.

When Claude Code runs a shell-form command hook (one without `args`), it spawns `sh -c` on macOS and Linux or Git Bash on Windows by default. This shell is non-interactive, but Git Bash and some configurations (such as `BASH_ENV` pointing at `~/.bashrc`) still source your profile. If that profile contains unconditional `echo` statements, the output gets prepended to your hook's JSON:

```text
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code tries to parse this as JSON and fails. To fix this, wrap echo statements in your shell profile so they only run in interactive shells:

```bash
# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

The `$-` variable contains shell flags, and `i` means interactive. Hooks run in non-interactive shells, so the echo is skipped.

## Debug techniques

The transcript view, toggled with `Ctrl+O`, shows a one-line summary for each hook that fired: success is silent, blocking errors show stderr, and non-blocking errors show a `<hook name> hook error` notice followed by the first line of stderr.

For full execution details including which hooks matched, their exit codes, stdout, and stderr, read the debug log. Start Claude Code with `claude --debug-file /tmp/claude.log` to write to a known path, then `tail -f /tmp/claude.log` in another terminal. If you started without that flag, run `/debug` mid-session to enable logging and find the log path.

**Source**: https://code.claude.com/docs/en/hooks-guide
**Last Updated**: 2026-06-13
**Status**: Active
