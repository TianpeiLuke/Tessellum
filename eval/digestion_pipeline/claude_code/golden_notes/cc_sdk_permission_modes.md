---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - permissions
keywords:
  - permission mode
  - acceptedits
  - dontask
  - bypasspermissions
  - plan mode
  - set_permission_mode
  - subagent inheritance
  - claudeagentoptions
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/permissions
access_control_group: ["general"]
---

# Claude Agent SDK — Permission Modes

## Overview

**Permission modes** provide global control over how Claude uses tools in the Agent SDK. The active mode is the fourth step of the [permission evaluation flow](cc_sdk_permissions_evaluation.md) (after hooks, deny rules, and ask rules, before allow rules and the `canUseTool` callback) and dictates the default disposition of any tool call that reaches it. You set the mode once when calling `query()`, or change it dynamically during a streaming session as trust builds.

The SDK supports six modes spanning a graduated-trust range from prompt-everything (`default`) to full autonomous access (`bypassPermissions`). Higher-autonomy modes (`bypassPermissions`, `acceptEdits`, `auto`) carry a subagent-inheritance caveat, and even the most permissive modes remain subject to the higher-priority deny rules, explicit `ask` rules, and hooks evaluated before the mode check.

## Available modes

The SDK supports these permission modes:

| Mode | Description | Tool behavior |
| :--- | :--- | :--- |
| `default` | Standard permission behavior | No auto-approvals; unmatched tools trigger your `canUseTool` callback |
| `dontAsk` | Deny instead of prompting | Anything not pre-approved by `allowed_tools` or rules is denied; `canUseTool` is never called |
| `acceptEdits` | Auto-accept file edits | File edits and filesystem operations (`mkdir`, `rm`, `mv`, etc.) are automatically approved |
| `bypassPermissions` | Bypass permission checks | Tools run without permission prompts, unless an explicit `ask` rule matches (use with caution) |
| `plan` | Planning mode | Claude explores and plans without editing your source files; file edits are never auto-approved and prompt through your `canUseTool` callback |
| `auto` (TypeScript only) | Model-classified approvals | A model classifier approves or denies each tool call. See [Auto mode](https://code.claude.com/docs/en/permission-modes) for availability |

**Subagent inheritance.** When the parent uses `bypassPermissions`, `acceptEdits`, or `auto`, all subagents inherit that mode and it cannot be overridden per subagent. Subagents may have different system prompts and less constrained behavior than your main agent, so inheriting `bypassPermissions` grants them full, autonomous system access. An explicit `ask` rule still forces a prompt.

## Set permission mode

You can set the permission mode once when starting a query, or change it dynamically while the session is active.

**At query time.** Pass `permission_mode` (Python) or `permissionMode` (TypeScript) when creating a query. This mode applies for the entire session unless changed dynamically.

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    async for message in query(
        prompt="Help me refactor this code",
        options=ClaudeAgentOptions(
            permission_mode="default",  # Set the mode here
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)


asyncio.run(main())
```

**During streaming.** Call `set_permission_mode()` (Python) or `setPermissionMode()` (TypeScript) to change the mode mid-session. The new mode takes effect immediately for all subsequent tool requests. This lets you start restrictive and loosen permissions as trust builds — for example switching to `acceptEdits` after reviewing Claude's initial approach.

```python Python theme={null}
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions


async def main():
    async with ClaudeSDKClient(
        options=ClaudeAgentOptions(
            permission_mode="default",  # Start in default mode
        )
    ) as client:
        await client.query("Help me refactor this code")

        # Change mode dynamically mid-session
        await client.set_permission_mode("acceptEdits")

        # Process messages with the new permission mode
        async for message in client.receive_response():
            if hasattr(message, "result"):
                print(message.result)


asyncio.run(main())
```

> The TypeScript equivalent (`permissionMode` option, `setPermissionMode()`) is available in the TypeScript SDK reference.

## Mode details

### Accept edits mode (`acceptEdits`)

Auto-approves file operations so Claude can edit code without prompting. Other tools (like Bash commands that aren't filesystem operations) still require normal permissions.

Auto-approved operations:

- File edits (Edit, Write tools)
- Filesystem commands: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`

Both apply only to paths inside the working directory or `additionalDirectories`. Paths outside that scope and writes to protected paths still prompt.

**Use when:** you trust Claude's edits and want faster iteration, such as during prototyping or when working in an isolated directory.

### Don't ask mode (`dontAsk`)

Converts any permission prompt into a denial. Tools pre-approved by `allowed_tools`, `settings.json` allow rules, or a hook run as normal. Everything else is denied without calling `canUseTool`.

**Use when:** you want a fixed, explicit tool surface for a headless agent and prefer a hard deny over silent reliance on `canUseTool` being absent.

### Bypass permissions mode (`bypassPermissions`)

Auto-approves all tool uses without prompts. Hooks still execute and can block operations if needed.

Use with extreme caution. Claude has full system access in this mode. Only use in controlled environments where you trust all possible operations. `allowed_tools` does not constrain this mode — every tool is approved, not just the ones you listed. Deny rules (`disallowed_tools`), explicit `ask` rules, and hooks are evaluated before the mode check and can still block a tool.

### Plan mode (`plan`)

Claude explores the codebase and produces a plan without editing your source files. Read-only tools run as in default mode. File edits are never auto-approved in plan mode, even when an allow rule matches — they prompt through your `canUseTool` callback instead. Claude may use `AskUserQuestion` to clarify requirements before finalizing the plan (handling these prompts is covered in [Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input)).

**Use when:** you want Claude to propose changes without executing them, such as during code review or when you need to approve changes before they're made.

**Source**: https://code.claude.com/docs/en/agent-sdk/permissions
**Last Updated**: 2026-06-13
**Status**: Active
