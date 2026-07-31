---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - user_input
keywords:
  - canusetool callback
  - user input
  - tool approval
  - askuserquestion
  - pause execution
  - defer hook decision
  - permission rules
  - clarifying questions
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/user-input
access_control_group: ["general"]
---

# Claude Code Agent SDK — Detecting When Claude Needs User Input

## Overview

While working on a task, Claude sometimes needs to check in with users — it might need permission before deleting files, or need to ask which database to use for a new project. The Agent SDK surfaces these requests through a single mechanism: the **`canUseTool` callback** you pass in your query options. Claude requests user input in **two situations** — when it needs **permission to use a tool** (like deleting files or running commands), and when it has **clarifying questions** (via the `AskUserQuestion` tool). Both trigger your `canUseTool` callback, which **pauses execution until you return a response**.

This is different from normal conversation turns, where Claude finishes and waits for your next message. Here, the agent is mid-task and blocked on your decision. This note covers the callback model and how the two cases are detected; the actual response handling lives in the sibling procedure notes for [tool approval](cc_sdk_tool_approval_handling.md) and [clarifying questions](cc_sdk_clarifying_questions.md).

## The `canUseTool` callback model

You pass a `canUseTool` callback in your query options. The callback fires whenever Claude needs user input, receiving the **tool name** and **input** as arguments:

```python Python
async def handle_tool_request(tool_name, input_data, context):
    # Prompt user and return allow or deny
    ...


options = ClaudeAgentOptions(can_use_tool=handle_tool_request)
```

```typescript TypeScript
async function handleToolRequest(toolName, input, options) {
  // options includes { signal: AbortSignal, suggestions?: PermissionUpdate[] }
  // Prompt user and return allow or deny
}

const options = { canUseTool: handleToolRequest };
```

## The two trigger cases

The callback fires in two cases:

1. **Tool needs approval**: Claude wants to use a tool that isn't auto-approved by [permission rules](https://code.claude.com/docs/en/agent-sdk/permissions) or modes. Check `tool_name` for the tool (e.g., `"Bash"`, `"Write"`). Handling is covered in [tool approval requests](cc_sdk_tool_approval_handling.md).
2. **Claude asks a question**: Claude calls the `AskUserQuestion` tool. Check if `tool_name == "AskUserQuestion"` to handle it differently. If you specify a `tools` array, include `AskUserQuestion` for this to work. Handling is covered in [clarifying questions](cc_sdk_clarifying_questions.md).

For clarifying questions, **Claude generates the questions and options** — your role is to present them to users and return their selections. You can't add your own questions to this flow; if you need to ask users something yourself, do that separately in your application logic.

## Pausing, indefinite waits, and `defer`

The callback **can stay pending indefinitely**. Execution remains paused until your callback returns, and the SDK only cancels the wait when the query itself is cancelled. If a user might take longer to respond than your process can reasonably stay running, return the [`defer` hook decision](https://code.claude.com/docs/en/hooks#defer-a-tool-call-for-later), which lets the process exit and resume later from the persisted session.

## Hooks fire before `canUseTool`

To automatically allow or deny tools without prompting users, use [hooks](https://code.claude.com/docs/en/agent-sdk/hooks) instead. Hooks execute **before** `canUseTool` and can allow, deny, or modify requests based on your own logic. You can also use the [`PermissionRequest` hook](https://code.claude.com/docs/en/agent-sdk/hooks#available-hooks) to send external notifications (Slack, email, push) when Claude is waiting for approval.

**Source**: https://code.claude.com/docs/en/agent-sdk/user-input
**Last Updated**: 2026-06-13
**Status**: Active
