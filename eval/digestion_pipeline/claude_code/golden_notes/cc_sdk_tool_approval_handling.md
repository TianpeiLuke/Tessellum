---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - user_input
keywords:
  - canusetool callback
  - tool approval request
  - permissionresultallow
  - permissionresultdeny
  - updatedinput
  - updatedpermissions
  - approve and remember
  - pretooluse dummy hook
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/user-input
access_control_group: ["general"]
---

# Claude Code Agent SDK — Handle Tool Approval Requests

## Overview

When Claude wants to use a tool that is not auto-approved by [permission rules](https://code.claude.com/docs/en/agent-sdk/permissions) or modes, the `canUseTool` callback fires so your application can display the request and return the user's decision. This procedure covers the two response types the callback returns — **Allow** and **Deny** — and the six concrete response patterns built from them (approve, approve with changes, approve and remember, reject, suggest alternative, redirect entirely). Detecting *when* the callback fires (the two trigger cases) is covered in [cc_sdk_user_input_overview.md](cc_sdk_user_input_overview.md); the `AskUserQuestion` branch of the same callback is covered in [cc_sdk_clarifying_questions.md](cc_sdk_clarifying_questions.md).

A Python caveat applies throughout: `can_use_tool` requires [streaming mode](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode) and a `PreToolUse` hook that returns `{"continue_": True}` to keep the stream open — without it the stream closes before the permission callback can be invoked.

## Callback Arguments

Once you pass a `canUseTool` callback in your query options, it fires when Claude wants to use a tool that isn't auto-approved. The callback receives three arguments:

| Argument | Description |
| --- | --- |
| `toolName` | The name of the tool Claude wants to use (e.g., `"Bash"`, `"Write"`, `"Edit"`) |
| `input` | The parameters Claude is passing to the tool. Contents vary by tool. |
| `options` (TS) / `context` (Python) | Additional context including optional `suggestions` (proposed `PermissionUpdate` entries to avoid re-prompting) and a cancellation signal. In TypeScript, `signal` is an `AbortSignal`; in Python, the signal field is reserved for future use. |

The `input` object contains tool-specific parameters. Common examples: `Bash` → `command`, `description`, `timeout`; `Write` → `file_path`, `content`; `Edit` → `file_path`, `old_string`, `new_string`; `Read` → `file_path`, `offset`, `limit`. You display this information to the user so they can decide whether to allow or reject the action, then return the appropriate response.

## The Two Response Types

Your callback returns one of two response types. When allowing, pass the tool input (original or modified); when denying, provide a message explaining why — Claude sees this message and may adjust its approach.

| Response | Python | TypeScript |
| --- | --- | --- |
| **Allow** | `PermissionResultAllow(updated_input=...)` | `{ behavior: "allow", updatedInput }` |
| **Deny** | `PermissionResultDeny(message=...)` | `{ behavior: "deny", message }` |

```python Python
from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny

# Allow the tool to execute
return PermissionResultAllow(updated_input=input_data)

# Block the tool
return PermissionResultDeny(message="User rejected this action")
```

```typescript TypeScript
// Allow the tool to execute
return { behavior: "allow", updatedInput: input };

// Block the tool
return { behavior: "deny", message: "User rejected this action" };
```

## Procedure: Prompt the User and Return a Decision

The following Python example asks Claude to create and delete a test file. When Claude attempts each operation, the callback prints the tool request to the terminal and prompts for `y/n` approval. Any input other than `y` is treated as a denial. Note the dummy `PreToolUse` hook that keeps the stream open (the Python-only requirement above).

```python Python
import asyncio

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query
from claude_agent_sdk.types import (
    HookMatcher,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)


async def can_use_tool(
    tool_name: str, input_data: dict, context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    # Display the tool request
    print(f"\nTool: {tool_name}")
    if tool_name == "Bash":
        print(f"Command: {input_data.get('command')}")
        if input_data.get("description"):
            print(f"Description: {input_data.get('description')}")
    else:
        print(f"Input: {input_data}")

    # Get user approval
    response = input("Allow this action? (y/n): ")

    # Return allow or deny based on user's response
    if response.lower() == "y":
        # Allow: tool executes with the original (or modified) input
        return PermissionResultAllow(updated_input=input_data)
    else:
        # Deny: tool doesn't execute, Claude sees the message
        return PermissionResultDeny(message="User denied this action")


# Required workaround: dummy hook keeps the stream open for can_use_tool
async def dummy_hook(input_data, tool_use_id, context):
    return {"continue_": True}


async def prompt_stream():
    yield {
        "type": "user",
        "message": {
            "role": "user",
            "content": "Create a test file in /tmp and then delete it",
        },
    }


async def main():
    async for message in query(
        prompt=prompt_stream(),
        options=ClaudeAgentOptions(
            can_use_tool=can_use_tool,
            hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[dummy_hook])]},
        ),
    ):
        if isinstance(message, ResultMessage) and message.subtype == "success":
            print(message.result)


asyncio.run(main())
```

The TypeScript equivalent uses single-message input (no dummy hook needed): it iterates `query({ prompt: "...", options: { canUseTool: async (toolName, input) => { ... } } })`, prints the tool/command, prompts via `readline`, and returns `{ behavior: "allow", updatedInput: input }` on `y` or `{ behavior: "deny", message: "User denied this action" }` otherwise.

## The Six Response Patterns

Beyond a plain allow or deny, you can modify the tool's input or provide context that helps Claude adjust its approach. The six patterns all build on the two response types:

- **Approve** — let the tool execute as Claude requested. Pass through the `input` from your callback unchanged and the tool executes exactly as Claude requested.
- **Approve with changes** — modify the input before execution (e.g., sanitize paths, add constraints, scope access). Claude sees the result but isn't told you changed anything.
- **Approve and remember** — echo a suggested permission rule back so matching calls skip the prompt next time.
- **Reject** — block the tool and tell Claude why; Claude sees the message and may try a different approach.
- **Suggest alternative** — block but guide Claude toward what the user wants instead.
- **Redirect entirely** — use [streaming input](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode) to send Claude a completely new instruction, bypassing the current tool request.

### Approve with Changes

The user approves but wants to modify the request first. Useful for sanitizing parameters, adding constraints, or scoping access — here, scoping all Bash commands into a sandbox path before they execute:

```python Python
async def can_use_tool(tool_name, input_data, context):
    if tool_name == "Bash":
        # User approved, but scope all commands to sandbox
        sandboxed_input = {**input_data}
        sandboxed_input["command"] = input_data["command"].replace(
            "/tmp", "/tmp/sandbox"
        )
        return PermissionResultAllow(updated_input=sandboxed_input)
    return PermissionResultAllow(updated_input=input_data)
```

### Approve and Remember

The user approves and doesn't want to be asked again for this kind of call. The third callback argument carries `suggestions`, an array of ready-made `PermissionUpdate` entries; echo one back in `updatedPermissions` to apply it. A suggestion with the `localSettings` destination writes the rule to `.claude/settings.local.json` so future sessions skip the prompt for matching calls. The Python example requires `claude-agent-sdk` 0.1.80 or later.

```python Python
async def can_use_tool(tool_name, input_data, context):
    choice = await ask_user(f"Allow {tool_name}?", ["once", "always", "no"])

    if choice == "always":
        persist = [
            s for s in context.suggestions if s.destination == "localSettings"
        ]
        return PermissionResultAllow(
            updated_input=input_data, updated_permissions=persist
        )
    if choice == "once":
        return PermissionResultAllow(updated_input=input_data)
    return PermissionResultDeny(message="User declined")
```

The TypeScript form destructures `{ suggestions = [] }` from the third argument, filters `suggestions.filter((s) => s.destination === "localSettings")`, and returns `{ behavior: "allow", updatedInput: input, updatedPermissions: persist }`.

### Reject and Suggest Alternative

To **reject**, return `PermissionResultDeny(message=...)` / `{ behavior: "deny", message }` — block the tool and explain why. To **suggest an alternative**, deny with guidance instead of a flat refusal so Claude course-corrects. For example, when a Bash command contains `rm`, denying with the message `"User doesn't want to delete files. They asked if you could compress them into an archive instead."` blocks the deletion but steers Claude toward archiving. For a complete change of direction (**redirect entirely**) rather than a nudge, use streaming input to send Claude a new instruction directly.

**Source**: https://code.claude.com/docs/en/agent-sdk/user-input
**Last Updated**: 2026-06-13
**Status**: Active
