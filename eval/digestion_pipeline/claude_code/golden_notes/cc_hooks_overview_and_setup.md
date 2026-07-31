---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - setup
keywords:
  - claude code hooks
  - hooks block settings json
  - notification hook
  - hook lifecycle shell command
  - configure hook location
  - hook scope
  - disableAllHooks
  - hooks menu
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

# Claude Code Hooks — Overview and Setup

## Overview

Hooks are user-defined shell commands that execute at specific points in Claude Code's lifecycle. They provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them. Use hooks to enforce project rules, automate repetitive tasks, and integrate Claude Code with your existing tools. For decisions that require judgment rather than deterministic rules, you can also use prompt-based hooks or agent-based hooks that use a Claude model to evaluate conditions (see [cc_hooks_advanced_types.md](cc_hooks_advanced_types.md)).

This note covers what hooks are, how to create your first one, and where to put hooks so they have the scope you want. Hooks are one of several ways to extend Claude Code: skills give Claude additional instructions and executable commands ([/en/skills](https://code.claude.com/docs/en/skills)), subagents run tasks in isolated contexts ([/en/sub-agents](https://code.claude.com/docs/en/sub-agents)), and plugins package extensions to share across projects ([/en/plugins](https://code.claude.com/docs/en/plugins)). For full event schemas, JSON input/output formats, and advanced features like async hooks and MCP tool hooks, see the Hooks reference ([/en/hooks](https://code.claude.com/docs/en/hooks)).

## Set up your first hook

To create a hook, add a `hooks` block to a settings file. This walkthrough creates a desktop notification hook, so you get alerted whenever Claude is waiting for your input instead of watching the terminal.

**Step 1 — Add the hook to your settings.** Open `~/.claude/settings.json` and add a `Notification` hook. The example below uses `osascript` for macOS (see [cc_hooks_common_recipes.md](cc_hooks_common_recipes.md) for Linux and Windows commands):

```json
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

If your settings file already has a `hooks` key, add `Notification` as a sibling of the existing event keys rather than replacing the whole object. Each event name is a key inside the single `hooks` object. You can also ask Claude to write the hook for you by describing what you want in the CLI.

**Step 2 — Verify the configuration.** Type `/hooks` to open the hooks browser. You'll see a list of all available hook events, with a count next to each event that has hooks configured. Select `Notification` to confirm your new hook appears in the list. Selecting the hook shows its details: the event, matcher, type, source file, and command.

**Step 3 — Test the hook.** Press `Esc` to return to the CLI. Ask Claude to do something that requires permission, then switch away from the terminal. You should receive a desktop notification.

The `/hooks` menu is read-only. To add, modify, or remove hooks, edit your settings JSON directly or ask Claude to make the change.

## Configure hook location

Where you add a hook determines its scope:

| Location | Scope | Shareable |
| :--- | :--- | :--- |
| `~/.claude/settings.json` | All your projects | No, local to your machine |
| `.claude/settings.json` | Single project | Yes, can be committed to the repo |
| `.claude/settings.local.json` | Single project | No, gitignored when Claude Code creates it |
| Managed policy settings | Organization-wide | Yes, admin-controlled |
| Plugin `hooks/hooks.json` | When plugin is enabled | Yes, bundled with the plugin |
| Skill or agent frontmatter | While the skill or agent is active | Yes, defined in the component file |

Run `/hooks` in Claude Code to browse all configured hooks grouped by event. To disable hooks, set `"disableAllHooks": true` in your settings file. Hooks configured in managed settings still run unless `disableAllHooks` is also set there.

If you edit settings files directly while Claude Code is running, the file watcher normally picks up hook changes automatically.

## Learn more

For the full `/hooks` menu reference, event schemas, JSON output format, async hooks, and MCP tool hooks, see the Hooks reference ([/en/hooks](https://code.claude.com/docs/en/hooks)). Review security considerations before deploying hooks in shared or production environments ([/en/hooks#security-considerations](https://code.claude.com/docs/en/hooks#security-considerations)).

**Source**: https://code.claude.com/docs/en/hooks-guide
**Last Updated**: 2026-06-13
**Status**: Active
