---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - guardrails
keywords:
  - block edits to protected files
  - pretooluse exit 2
  - protect-files.sh
  - re-inject context after compaction
  - sessionstart compact matcher
  - audit configuration changes
  - configchange hook
  - claude config audit log
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

# Claude Code Hooks — Guardrail and Audit Recipes

## Overview

This note collects three ready-to-use hook recipes from the "What you can automate" section of the hooks guide that enforce project rules and record activity: **block edits to protected files**, **re-inject context after compaction**, and **audit configuration changes**. Each is a configuration block you paste into a [settings file](cc_hooks_overview_and_setup.md), runs at a specific point in Claude Code's lifecycle, and turns a deterministic rule into an action that always happens rather than one Claude must choose to take. The lower-risk notification and auto-format recipes are in [cc_hooks_common_recipes](cc_hooks_common_recipes.md); environment-reload and auto-approve recipes are in [cc_hooks_environment_and_permission_recipes](cc_hooks_environment_and_permission_recipes.md).

These recipes rely on the exit-code and matcher mechanics covered in [cc_hooks_io_and_decision_control](cc_hooks_io_and_decision_control.md) and [cc_hooks_matchers_and_filtering](cc_hooks_matchers_and_filtering.md). For full event schemas (`#configchange` and others), see the [Hooks reference](https://code.claude.com/docs/en/hooks).

## Block edits to protected files

This recipe prevents Claude from modifying sensitive files like `.env`, `package-lock.json`, or anything in `.git/`. Claude receives feedback explaining why the edit was blocked, so it can adjust its approach. The example uses a separate script file that the hook calls: the script checks the target file path against a list of protected patterns and exits with code 2 to block the edit.

**Step 1 — Create the hook script.** Save this to `.claude/hooks/protect-files.sh`:

```bash
#!/bin/bash
# protect-files.sh

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done

exit 0
```

**Step 2 — Make the script executable (macOS/Linux).** Hook scripts must be executable for Claude Code to run them:

```bash
chmod +x .claude/hooks/protect-files.sh
```

**Step 3 — Register the hook.** Add a `PreToolUse` hook to `.claude/settings.json` that runs the script before any `Edit` or `Write` tool call:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

## Re-inject context after compaction

When Claude's context window fills up, compaction summarizes the conversation to free space, which can lose important details. Use a `SessionStart` hook with a `compact` matcher to re-inject critical context after every compaction. Any text the command writes to stdout is added to Claude's context. This example reminds Claude of project conventions and recent work; add it to `.claude/settings.json` in your project root:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

You can replace the `echo` with any command that produces dynamic output, like `git log --oneline -5` to show recent commits. For injecting context on every session start, the guide suggests using [CLAUDE.md](https://code.claude.com/docs/en/memory) instead; for environment variables, see `CLAUDE_ENV_FILE` in the [Hooks reference](https://code.claude.com/docs/en/hooks).

## Audit configuration changes

This recipe tracks when settings or skills files change during a session. The `ConfigChange` event fires when an external process or editor modifies a configuration file, so you can log changes for compliance or block unauthorized modifications. The example appends each change to an audit log; add it to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

The matcher filters by configuration type: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, or `skills`. To block a change from taking effect, exit with code 2 or return `{"decision": "block"}`. See the [ConfigChange reference](https://code.claude.com/docs/en/hooks) for the full input schema.

**Source**: https://code.claude.com/docs/en/hooks-guide
**Last Updated**: 2026-06-13
**Status**: Active
