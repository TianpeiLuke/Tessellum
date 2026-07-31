---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - hooks
keywords:
  - sdk hooks
  - hook callback functions
  - agent events
  - pretooluse posttooluse
  - how hooks work
  - available hooks
  - hook event table
  - subagent hooks
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/hooks
access_control_group: ["general"]
---

# Claude Code Agent SDK — Hooks Overview

## Overview

In the Claude Agent SDK, **hooks** are callback functions that run your code in response to agent events — a tool being called, a session starting, or execution stopping. They let an SDK application block dangerous operations before they execute (destructive shell commands, unauthorized file access), log and audit every tool call, transform inputs and outputs (sanitize data, inject credentials, redirect file paths), require human approval for sensitive actions, and track session lifecycle to manage state or send notifications.

This note covers the conceptual model: the five-step flow by which the SDK fires an event, collects registered hooks, filters them with matchers, executes their callbacks, and acts on the returned decision — and the table of available hook events with their Python/TypeScript availability. How to register and configure hooks (the `options.hooks` map, matcher rules, and callback input/output shapes) is covered in [Configure Hooks](cc_sdk_hooks_configuration.md); recipe patterns are in [Examples](cc_sdk_hooks_examples.md); diagnostics for common issues are documented in the [Claude Code hooks SDK guide](https://code.claude.com/docs/en/agent-sdk/hooks). The full JSON input/output schemas and matcher-pattern reference live in the [Claude Code hooks reference](https://code.claude.com/docs/en/hooks).

## How hooks work

A hook fires through a five-step flow:

1. **An event fires** — something happens during agent execution and the SDK fires an event: a tool is about to be called (`PreToolUse`), a tool returned a result (`PostToolUse`), a subagent started or stopped, the agent is idle, or execution finished.
2. **The SDK collects registered hooks** — the SDK checks for hooks registered for that event type. This includes callback hooks passed in `options.hooks` and shell command hooks from settings files when the corresponding `settingSources` / `setting_sources` entry is enabled (which it is for default `query()` options).
3. **Matchers filter which hooks run** — if a hook has a `matcher` pattern (like `"Write|Edit"`), the SDK tests it against the event's target (for example, the tool name). Hooks without a matcher run for every event of that type.
4. **Callback functions execute** — each matching hook's callback receives input about what is happening: the tool name, its arguments, the session ID, and other event-specific details.
5. **Your callback returns a decision** — after performing any operations (logging, API calls, validation), the callback returns an output object that tells the agent what to do: allow the operation, block it, modify the input, or inject context into the conversation.

The following example puts these steps together. It registers a `PreToolUse` hook (step 1) with a `"Write|Edit"` matcher (step 3) so the callback only fires for file-writing tools. When triggered, the callback receives the tool's input (step 4), checks if the file path targets a `.env` file, and returns `permissionDecision: "deny"` to block the operation (step 5):

```python
import asyncio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeSDKClient,
    ClaudeAgentOptions,
    HookMatcher,
    ResultMessage,
)


# Define a hook callback that receives tool call details
async def protect_env_files(input_data, tool_use_id, context):
    # Extract the file path from the tool's input arguments
    file_path = input_data["tool_input"].get("file_path", "")
    file_name = file_path.split("/")[-1]

    # Block the operation if targeting a .env file
    if file_name == ".env":
        return {
            "hookSpecificOutput": {
                "hookEventName": input_data["hook_event_name"],
                "permissionDecision": "deny",
                "permissionDecisionReason": "Cannot modify .env files",
            }
        }

    # Return empty object to allow the operation
    return {}


async def main():
    options = ClaudeAgentOptions(
        hooks={
            # Register the hook for PreToolUse events
            # The matcher filters to only Write and Edit tool calls
            "PreToolUse": [HookMatcher(matcher="Write|Edit", hooks=[protect_env_files])]
        }
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("Update the database configuration")
        async for message in client.receive_response():
            # Filter for assistant and result messages
            if isinstance(message, (AssistantMessage, ResultMessage)):
                print(message)


asyncio.run(main())
```

The TypeScript equivalent (using the `query()` API and the `HookCallback` type) is available in the TypeScript SDK reference.

## Available hooks

The SDK provides hooks for different stages of agent execution. Some hooks are available in both SDKs, while others are TypeScript-only.

| Hook Event | Python SDK | TypeScript SDK | What triggers it | Example use case |
| --- | --- | --- | --- | --- |
| `PreToolUse` | Yes | Yes | Tool call request (can block or modify) | Block dangerous shell commands |
| `PostToolUse` | Yes | Yes | Tool execution result | Log all file changes to audit trail |
| `PostToolUseFailure` | Yes | Yes | Tool execution failure | Handle or log tool errors |
| `PostToolBatch` | No | Yes | A full batch of tool calls resolves, once per batch before the next model call | Inject conventions once for the whole batch |
| `UserPromptSubmit` | Yes | Yes | User prompt submission | Inject additional context into prompts |
| `MessageDisplay` | No | Yes | An assistant message with text completes, once per message with the full message text | Redact or reformat the displayed text without changing the transcript |
| `Stop` | Yes | Yes | Agent execution stop | Save session state before exit |
| `SubagentStart` | Yes | Yes | Subagent initialization | Track parallel task spawning |
| `SubagentStop` | Yes | Yes | Subagent completion | Aggregate results from parallel tasks |
| `PreCompact` | Yes | Yes | Conversation compaction request | Archive full transcript before summarizing |
| `PermissionRequest` | Yes | Yes | Permission dialog would be displayed | Custom permission handling |
| `SessionStart` | No | Yes | Session initialization | Initialize logging and telemetry |
| `SessionEnd` | No | Yes | Session termination | Clean up temporary resources |
| `Notification` | Yes | Yes | Agent status messages | Send agent status updates to Slack or PagerDuty |
| `Setup` | No | Yes | Session setup/maintenance | Run initialization tasks |
| `TeammateIdle` | No | Yes | Teammate becomes idle | Reassign work or notify |
| `TaskCompleted` | No | Yes | Background task completes | Aggregate results from parallel tasks |
| `ConfigChange` | No | Yes | Configuration file changes | Reload settings dynamically |
| `WorktreeCreate` | No | Yes | Git worktree created | Track isolated workspaces |
| `WorktreeRemove` | No | Yes | Git worktree removed | Clean up workspace resources |

The TypeScript-only events (`PostToolBatch`, `MessageDisplay`, `SessionStart`, `SessionEnd`, `Setup`, `TeammateIdle`, `TaskCompleted`, `ConfigChange`, `WorktreeCreate`, `WorktreeRemove`) are not available as SDK callback hooks in Python; some, such as `SessionStart`/`SessionEnd`, can instead be registered as shell command hooks in settings files (see the [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)).

**Source**: https://code.claude.com/docs/en/agent-sdk/hooks
**Last Updated**: 2026-06-13
**Status**: Active
