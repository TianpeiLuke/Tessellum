---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - recipes
keywords:
  - hooks recipes
  - notification hook
  - desktop notification
  - auto-format code
  - posttooluse prettier
  - notification matcher values
  - jq tool_input
  - claude code settings.json
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

# Claude Code Hooks — Common Recipes (Notify, Auto-Format)

## Overview

The "What you can automate" section of the hooks guide is a catalog of ready-to-use configuration blocks you paste into a [settings file](cc_hooks_overview_and_setup.md). Each recipe runs code at a key point in Claude Code's lifecycle — format files after edits, block commands before they execute, send notifications when Claude needs input, inject context at session start, and more. This note covers the two most common, lowest-risk recipes: **getting a desktop notification when Claude needs your input**, and **auto-formatting code after every edit**. The remaining recipes are documented in sibling notes — guardrail and audit recipes (block protected files, re-inject context after compaction, audit configuration changes), and environment/permission recipes (reload environment on directory change, auto-approve specific prompts) in [cc_hooks_environment_and_permission_recipes](cc_hooks_environment_and_permission_recipes.md). For the full source guide covering all seven recipes, see the hooks guide (https://code.claude.com/docs/en/hooks-guide).

The full recipe index, in source order: get notified when Claude needs input · auto-format code after edits · block edits to protected files · re-inject context after compaction · audit configuration changes · reload environment when directory or files change · auto-approve specific permission prompts. For the full list of hook events, see the [Hooks reference](https://code.claude.com/docs/en/hooks). For a production example of hooks that run a separate model review and feed findings back into the session, see how the `security-guidance` plugin integrates with Claude Code (https://code.claude.com/docs/en/security-guidance).

## Get notified when Claude needs input

Get a desktop notification whenever Claude finishes working and needs your input, so you can switch to other tasks without checking the terminal. This hook uses the `Notification` event, which fires when Claude is waiting for input or permission. Each platform uses its native notification command. Add the matching block to `~/.claude/settings.json`.

**macOS** (uses `osascript`):

```json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

**Linux** (uses `notify-send`):

```json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
          }
        ]
      }
    ]
  }
}
```

**Windows (PowerShell)**:

```json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
          }
        ]
      }
    ]
  }
}
```

### Scope the notification with the matcher

The empty `matcher` fires on all notification types. To fire only on specific events, set it to one of these values:

| Matcher                | Fires when                                             |
| :--------------------- | :----------------------------------------------------- |
| `permission_prompt`    | Claude needs you to approve a tool use                 |
| `idle_prompt`          | Claude is done and waiting for your next prompt        |
| `auth_success`         | Authentication completes                               |
| `elicitation_dialog`   | An MCP server opens an elicitation form                |
| `elicitation_complete` | An MCP elicitation form is submitted or dismissed      |
| `elicitation_response` | An MCP elicitation response is sent back to the server |

Type `/hooks` and select `Notification` to confirm the hook is registered. For the full event schema, see the Notification reference (https://code.claude.com/docs/en/hooks).

### If no notification appears (macOS)

`osascript` routes notifications through the built-in Script Editor app. If Script Editor doesn't have notification permission, the command fails silently, and macOS won't prompt you to grant it. Run this in Terminal once to make Script Editor appear in your notification settings:

```bash theme={null}
osascript -e 'display notification "test"'
```

Nothing will appear yet. Open **System Settings > Notifications**, find **Script Editor** in the list, and turn on **Allow Notifications**. Run the command again to confirm the test notification appears.

## Auto-format code after edits

Automatically run [Prettier](https://prettier.io/) on every file Claude edits, so formatting stays consistent without manual intervention. This hook uses the `PostToolUse` event with an `Edit|Write` matcher, so it runs only after file-editing tools (not after every tool call). The command extracts the edited file path with [`jq`](https://jqlang.github.io/jq/) and passes it to Prettier. Add this to `.claude/settings.json` in your project root:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

The Bash examples on this page use `jq` for JSON parsing. Install it with `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu), or see `jq` downloads (https://jqlang.github.io/jq/download/).

**Source**: https://code.claude.com/docs/en/hooks-guide
**Last Updated**: 2026-06-13
**Status**: Active
