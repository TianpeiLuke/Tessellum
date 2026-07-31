---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - hooks
keywords:
  - sdk hooks examples
  - modify tool input
  - block a tool
  - auto-approve read-only tools
  - register multiple hooks
  - multi-tool matchers
  - track subagent activity
  - webhook from hooks
  - forward notifications to slack
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/hooks
access_control_group: ["general"]
---

# Claude Code Agent SDK — Hook Examples

## Overview

This note collects the eight worked hook recipes from the Agent SDK hooks page — the common patterns an SDK application wires in to intercept and customize tool execution. Each example registers a callback under `options.hooks` (see [Hook Configuration](cc_sdk_hooks_configuration.md)) and returns an output object that allows, blocks, or rewrites the operation. The patterns cluster into three uses: transforming a tool call before it runs (modify input, sandbox redirect), gating a tool (block, auto-approve, layered checks), and observing the agent (track subagents, webhooks, Slack notifications).

Each recipe is shown here in one representative language (Python). The TypeScript equivalent for every example is available in the [TypeScript SDK reference](https://code.claude.com/docs/en/agent-sdk/typescript). All `PreToolUse` callbacks below return `{}` to allow an operation unchanged.

## Modify tool input (sandbox redirect)

Intercept `Write` calls and rewrite the `file_path` argument to prepend `/sandbox`, redirecting all file writes to a sandboxed directory. The callback returns `updatedInput` with the modified path plus `permissionDecision: "allow"` to auto-approve the rewritten operation. (When using `updatedInput` you must also set `permissionDecision: "allow"` to auto-approve, or `"ask"` to show the user; with `"defer"`, `updatedInput` is ignored. Always return a new object rather than mutating the original `tool_input`.)

```python
async def redirect_to_sandbox(input_data, tool_use_id, context):
    if input_data["hook_event_name"] != "PreToolUse":
        return {}

    if input_data["tool_name"] == "Write":
        original_path = input_data["tool_input"].get("file_path", "")
        return {
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "allow",
                "updatedInput": {
                    **input_data["tool_input"],
                    "file_path": f"/sandbox{original_path}",
                },
            }
        }
    return {}
```

## Add context and block a tool

Block writes to `/etc` and explain why to both the model and the user: `permissionDecision: "deny"` stops the tool call, `permissionDecisionReason` tells the model why (so it avoids retrying), and the top-level `systemMessage` shows the user what happened.

```python
async def block_etc_writes(input_data, tool_use_id, context):
    file_path = input_data["tool_input"].get("file_path", "")

    if file_path.startswith("/etc"):
        return {
            # Top-level field: message shown to the user
            "systemMessage": "Remember: system directories like /etc are protected.",
            # hookSpecificOutput: block the operation
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "deny",
                "permissionDecisionReason": "Writing to /etc is not allowed",
            },
        }
    return {}
```

## Auto-approve specific tools

By default the agent may prompt for permission before using certain tools. This recipe auto-approves read-only filesystem tools (`Read`, `Glob`, `Grep`) by returning `permissionDecision: "allow"`, letting them run without user confirmation while leaving all other tools subject to normal permission checks.

```python
async def auto_approve_read_only(input_data, tool_use_id, context):
    if input_data["hook_event_name"] != "PreToolUse":
        return {}

    read_only_tools = ["Read", "Glob", "Grep"]
    if input_data["tool_name"] in read_only_tools:
        return {
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "allow",
                "permissionDecisionReason": "Read-only tool auto-approved",
            }
        }
    return {}
```

## Register multiple hooks and multi-tool matchers

**Multiple hooks.** When an event fires, all matching hooks run **in parallel**. For permission decisions the most restrictive result wins: a single `deny` blocks the tool call regardless of what the other hooks return. Because completion order is non-deterministic, write each hook to act independently rather than relying on another having run first. Registering three independent checks for every tool call is just a list of matchers with no `matcher` pattern:

```python
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(hooks=[authorization_check]),
            HookMatcher(hooks=[input_validator]),
            HookMatcher(hooks=[audit_logger]),
        ]
    }
)
```

**Multi-tool matchers.** Share one callback across related tools by giving each matcher a different scope: a pipe-separated exact list (`Write|Edit|Delete`) triggers a callback only for file-modification tools; a regex (`^mcp__`) triggers an MCP-audit callback for any MCP tool; and an omitted matcher triggers a global logger for every tool call regardless of name.

## Track subagent activity

Use a `SubagentStop` hook to monitor when subagents finish their work. This recipe logs a summary each time a subagent completes — the subagent's `agent_id`, `agent_transcript_path`, the correlating `tool_use_id`, and `stop_hook_active`:

```python
async def subagent_tracker(input_data, tool_use_id, context):
    # Log subagent details when it finishes
    print(f"[SUBAGENT] Completed: {input_data['agent_id']}")
    print(f"  Transcript: {input_data['agent_transcript_path']}")
    print(f"  Tool use ID: {tool_use_id}")
    print(f"  Stop hook active: {input_data.get('stop_hook_active')}")
    return {}


options = ClaudeAgentOptions(
    hooks={"SubagentStop": [HookMatcher(hooks=[subagent_tracker])]}
)
```

## Make HTTP requests from hooks

Hooks can perform asynchronous operations like HTTP requests. **Catch errors inside the hook** instead of letting them propagate, since an unhandled exception can interrupt the agent. This recipe sends a webhook after each tool completes (`PostToolUse`), running the blocking HTTP call in a thread with `asyncio.to_thread` so it does not block the event loop, and swallowing any failure so a failed webhook does not stop the agent:

```python
async def webhook_notifier(input_data, tool_use_id, context):
    # Only fire after a tool completes (PostToolUse), not before
    if input_data["hook_event_name"] != "PostToolUse":
        return {}

    try:
        # Run the blocking HTTP call in a thread to avoid blocking the event loop
        await asyncio.to_thread(_send_webhook, input_data["tool_name"])
    except Exception as e:
        # Log the error but don't raise. A failed webhook shouldn't stop the agent
        print(f"Webhook request failed: {e}")

    return {}
```

## Forward notifications to Slack

Use a `Notification` hook to receive system notifications from the agent and forward them to an external service. Notifications fire for event types such as `permission_prompt` (Claude needs permission), `idle_prompt` (Claude is waiting for input), `auth_success` (authentication completed), and `elicitation_dialog` / `elicitation_complete` / `elicitation_response` (user-prompt elicitation flows). Each notification carries a human-readable `message` and optionally a `title`. The handler registers under `Notification` with no matcher, reads `input_data.get("message", "")`, POSTs it to a [Slack incoming webhook URL](https://api.slack.com/messaging/webhooks), and returns `{}` — `Notification` hooks do not modify agent behavior. As with the webhook recipe, the blocking send runs via `asyncio.to_thread` and errors are caught rather than raised.

**Source**: https://code.claude.com/docs/en/agent-sdk/hooks
**Last Updated**: 2026-06-13
**Status**: Active
