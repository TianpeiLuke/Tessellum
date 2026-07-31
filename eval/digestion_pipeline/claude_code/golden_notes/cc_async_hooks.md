---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - async
keywords:
  - async hook
  - run hooks in the background
  - asyncRewake
  - additionalContext next turn
  - non-blocking hook
  - background command hook
  - hook timeout
  - run tests after file changes
topics:
  - Claude Code
  - Hooks
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/hooks
access_control_group: ["general"]
---

# Claude Code — Async Hooks (Run Hooks in the Background)

## Overview

By default, hooks block Claude's execution until they complete. For long-running tasks like deployments, test suites, or external API calls, setting `"async": true` on a `command` hook runs it in the background while Claude keeps working. Because the action the hook would have controlled has already completed by the time the hook finishes, async hooks **cannot block or control behavior** — response fields like `decision`, `permissionDecision`, and `continue` have no effect. Instead, an async hook reports back by emitting `additionalContext`, which Claude reads on the **next conversation turn**.

This note is the procedure for configuring and reasoning about async/background command hooks. For the synchronous handler-type schema (`command`/`http`/`mcp_tool`/`prompt`/`agent`) see [cc_hook_handler_types](cc_hook_handler_types.md); for the per-tool-call events where async hooks most often fire see [cc_hook_tool_loop_events](cc_hook_tool_loop_events.md).

## Configure an async hook

Add `"async": true` to a command hook's configuration to run it in the background without blocking Claude. **This field is only available on `type: "command"` hooks.**

The hook below runs a test script after every `Write` tool call. Claude continues working immediately while `run-tests.sh` executes for up to 120 seconds; when the script finishes, its output is delivered on the next conversation turn:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

The `timeout` field sets the maximum time in seconds for the background process. If not specified, async hooks use the same 10-minute (600s) default as sync command hooks.

### The `asyncRewake` field

A related command-hook field, `asyncRewake`, runs the hook in the background and **wakes Claude on exit code 2** (it implies `async`). The hook's stderr — or stdout if stderr is empty — is shown to Claude as a system reminder so it can react to a long-running background failure. This is the mechanism that lets a background job interrupt an otherwise-idle session (see Limitations below).

## How async hooks execute

When an async hook fires, Claude Code starts the hook process and immediately continues without waiting for it to finish. The hook receives the same JSON input via stdin as a synchronous hook.

After the background process exits, if the hook produced a JSON response with an `additionalContext` field, that content is delivered to Claude as context on the next conversation turn. A `systemMessage` field is shown to **you**, not to Claude.

Async hook completion notifications are suppressed by default. To see them, enable verbose mode with `Ctrl+O` or start Claude Code with `--verbose`.

## Example: run tests after file changes

This hook starts a test suite in the background whenever Claude writes a file, then reports the results back to Claude when the tests finish. The script reads the hook input from stdin, filters to source files, runs the suite, and emits the result via `additionalContext` inside `hookSpecificOutput`. Save it to `.claude/hooks/run-tests-async.sh` and make it executable with `chmod +x`:

```bash theme={null}
#!/bin/bash
# run-tests-async.sh

# Read hook input from stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only run tests for source files
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Run tests and report results to Claude via additionalContext
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  MSG="Tests passed after editing $FILE_PATH"
else
  MSG="Tests failed after editing $FILE_PATH: $RESULT"
fi
jq -nc --arg msg "$MSG" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $msg}}'
```

The matching settings entry adds `async: true` so Claude keeps working while tests run. It is registered in `.claude/settings.json` under `PostToolUse` with a `Write|Edit` matcher, the `${CLAUDE_PROJECT_DIR}/.claude/hooks/run-tests-async.sh` command in exec form (`args: []`), and `timeout: 300` — the full JSON block is in the source page.

## Limitations

Async hooks have several constraints compared to synchronous hooks:

- **Command hooks only.** Only `type: "command"` hooks support `async`. Prompt-based hooks cannot run asynchronously.
- **Cannot block or return decisions.** By the time the hook completes, the triggering action has already proceeded, so `decision`, `permissionDecision`, and `continue` have no effect.
- **Output arrives next turn.** Hook output is delivered on the next conversation turn. If the session is idle, the response waits until the next user interaction. The exception is an `asyncRewake` hook that exits with code 2, which wakes Claude immediately even when the session is idle.
- **No deduplication.** Each execution creates a separate background process; there is no deduplication across multiple firings of the same async hook.

**Source**: https://code.claude.com/docs/en/hooks
**Last Updated**: 2026-06-13
**Status**: Active
