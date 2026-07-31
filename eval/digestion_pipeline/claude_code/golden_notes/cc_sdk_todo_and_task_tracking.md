---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - todo_tracking
keywords:
  - sdk todo tracking
  - task tools migration
  - todowrite
  - taskcreate taskupdate
  - todo lifecycle
  - claude_code_enable_tasks
  - monitoring tool_use blocks
  - real-time progress display
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/todo-tracking
access_control_group: ["general"]
---

# Claude Code Agent SDK — Todo and Task Tracking

## Overview

The Claude Agent SDK includes **built-in todo functionality** that gives a structured way to manage tasks and display progress to users during complex, multi-step runs. Todo updates surface as `tool_use` blocks in the assistant message stream, so application code can monitor them and render real-time progress without asking the agent to report status.

As of **TypeScript Agent SDK 0.3.142 and Claude Code v2.1.142**, sessions use the structured **Task tools** (`TaskCreate`, `TaskUpdate`, `TaskGet`, `TaskList`) instead of the single `TodoWrite` call; the Task tools are the default for new sessions, and monitoring code must change to a keyed map (see [Migrate to Task tools](#migrate-to-task-tools)). Setting `CLAUDE_CODE_ENABLE_TASKS=0` re-enables `TodoWrite` for sessions that have not migrated yet.

## Todo Lifecycle

Todos follow a predictable lifecycle:

1. **Created** as `pending` when tasks are identified
2. **Activated** to `in_progress` when work begins
3. **Completed** when the task finishes successfully
4. **Removed** when all tasks in a group are completed

## When Todos Are Used

The SDK automatically creates todos for:

- **Complex multi-step tasks** requiring 3 or more distinct actions
- **User-provided task lists** when multiple items are mentioned
- **Non-trivial operations** that benefit from progress tracking
- **Explicit requests** when users ask for todo organization

## Monitoring and Displaying Todos

Todo updates are reflected in the assistant message stream. Monitoring code iterates the `query()` results, and for each `assistant` message inspects its content blocks for a `tool_use` block named `TodoWrite`; the current list lives in `block.input.todos`, where each todo has `content`, `status` (`pending` / `in_progress` / `completed`), and an `activeForm` (the in-progress phrasing). Because `TodoWrite` is no longer the default, the monitoring examples set `CLAUDE_CODE_ENABLE_TASKS=0` so these `tool_use` blocks still appear; without it the SDK uses Task tools instead.

The minimal monitoring loop (Python) reads each `TodoWrite` call and prints a status line per todo:

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ToolUseBlock

async for message in query(
    prompt="Optimize my React app performance and track progress with todos",
    # Re-enable TodoWrite, which this example monitors. Without it, the SDK uses
    # Task tools instead and these tool_use blocks never appear.
    options=ClaudeAgentOptions(max_turns=15, env={"CLAUDE_CODE_ENABLE_TASKS": "0"}),
):
    # Todo updates are reflected in the message stream
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock) and block.name == "TodoWrite":
                todos = block.input["todos"]

                print("Todo Status Update:")
                for i, todo in enumerate(todos):
                    status = (
                        "✅"
                        if todo["status"] == "completed"
                        else "🔧"
                        if todo["status"] == "in_progress"
                        else "❌"
                    )
                    print(f"{i + 1}. {status} {todo['content']}")
```

For a **real-time progress display**, the SDK docs wrap the same pattern in a `TodoTracker` class that stores the latest `todos` on each `TodoWrite` and renders a `completed/total` count plus the `activeForm` of any in-progress item (TypeScript and Python variants are provided in the source).

## Migrate to Task tools

The Task tools split the single `TodoWrite` call into **`TaskCreate`** for each new item and **`TaskUpdate`** for each status change, with **`TaskList`** and **`TaskGet`** available for the model to read back the current list. Monitoring code still inspects `tool_use` blocks in the assistant stream, but maintains a **map keyed by task ID** instead of replacing the whole list on every call. The Task tools are the default as of TypeScript Agent SDK 0.3.142 and Claude Code v2.1.142, so no `options.env` change is needed.

Key differences between the two interfaces:

| With `TodoWrite` | With Task tools |
| --- | --- |
| One tool call rewrites the full `todos` array | `TaskCreate` adds one item, `TaskUpdate` patches one item by `taskId` |
| Match `block.name === "TodoWrite"` | Match `block.name === "TaskCreate"` or `"TaskUpdate"` |
| Item shape: `{ content, status, activeForm }` | `TaskCreate` input: `{ subject, description, activeForm?, metadata? }`. `TaskUpdate` input: `{ taskId, status?, subject?, description?, activeForm?, addBlocks?, addBlockedBy?, owner?, metadata? }`. `status` is `"pending"`, `"in_progress"`, or `"completed"`; set `status: "deleted"` to delete |
| Render `block.input.todos` directly | Accumulate items across calls, or read a snapshot from a `TaskList` tool result |

The assigned task ID is **not** in the `TaskCreate` input — it comes back in the matching `tool_result` as `{ task: { id, subject } }`, so monitoring code must capture it from the result block to key its map. The minimal Task-tools monitoring loop (Python) matches the new tool names:

```python
from claude_agent_sdk import query, AssistantMessage, ToolUseBlock

async for message in query(
    prompt="Optimize my React app performance",
):
    if not isinstance(message, AssistantMessage):
        continue
    for block in message.content:
        if not isinstance(block, ToolUseBlock):
            continue
        if block.name == "TaskCreate":
            print(f"+ {block.input['subject']}")
        elif block.name == "TaskUpdate" and block.input.get("status"):
            print(f"  {block.input['taskId']} -> {block.input['status']}")
```

To render a complete list, watch for a `TaskList` tool result in the stream, or accumulate `TaskCreate` results and `TaskUpdate` inputs into a map.

**Source**: https://code.claude.com/docs/en/agent-sdk/todo-tracking
**Last Updated**: 2026-06-13
**Status**: Active
