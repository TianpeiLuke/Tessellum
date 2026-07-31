---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - agent_loop
keywords:
  - resultmessage subtype
  - stop_reason
  - total_cost_usd
  - agent sdk hooks
  - pretooluse posttooluse
  - short-circuit tool call
  - handle the result
  - error_max_turns
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/agent-loop
access_control_group: ["general"]
---

# Agent SDK — Handling the Result and Loop Hooks

## Overview

When the Agent SDK loop ends, it yields a `ResultMessage` whose `subtype` field tells you whether the task succeeded or hit a limit, and carries the final text, cost, token usage, and session ID for tracking and resumption. Alongside the result, **hooks** are callbacks that fire at specific points in the loop — before a tool runs, after it returns, when the agent finishes — letting you observe, audit, or short-circuit the loop without consuming context.

This note documents the `ResultMessage` termination contract (subtypes, the conditionally-present `result` field, and the `stop_reason` field) and the loop's commonly-used hook events, then shows a combined end-to-end agent that applies these concepts together. Detailed cost interpretation, the full hook event list, and per-SDK availability live in dedicated pages (linked out).

## Handle the result

When the loop ends, the `ResultMessage` tells you what happened and gives you the output. The `subtype` field (available in both SDKs) is the primary way to check termination state:

| Result subtype | What happened | `result` field available? |
| :--- | :--- | :---: |
| `success` | Claude finished the task normally | Yes |
| `error_max_turns` | Hit the `maxTurns` limit before finishing | No |
| `error_max_budget_usd` | Hit the `maxBudgetUsd` limit before finishing | No |
| `error_during_execution` | An error interrupted the loop (for example, an API failure or cancelled request) | No |
| `error_max_structured_output_retries` | No valid structured output was produced within the configured retry limit: every attempt failed validation, or a model fallback retracted the completed output with no successful retry | No |

The `result` field (the final text output) is **only present on the `success` variant**, so always check the subtype before reading it. All result subtypes carry `total_cost_usd`, `usage`, `num_turns`, and `session_id` so you can track cost and resume even after errors. In Python, `total_cost_usd` and `usage` are typed as optional and may be `None` on some error paths, so guard before formatting them. Detailed interpretation of the `usage` fields is covered in [Tracking costs and usage](https://code.claude.com/docs/en/agent-sdk/cost-tracking).

The result also includes a `stop_reason` field (`string | null` in TypeScript, `str | None` in Python) indicating why the model stopped generating on its final turn. Common values are `end_turn` (model finished normally), `max_tokens` (hit the output token limit), and `refusal` (the model declined the request). On error result subtypes, `stop_reason` carries the value from the last assistant response before the loop ended. To detect refusals, check `stop_reason === "refusal"` (TypeScript) or `stop_reason == "refusal"` (Python). See the SDK language references for the full `ResultMessage` / `SDKResultMessage` type.

## Hooks

Hooks are callbacks that fire at specific points in the loop: before a tool runs, after it returns, when the agent finishes, and so on. Some commonly used hooks are:

| Hook | When it fires | Common uses |
| :--- | :--- | :--- |
| `PreToolUse` | Before a tool executes | Validate inputs, block dangerous commands |
| `PostToolUse` | After a tool returns | Audit outputs, trigger side effects |
| `UserPromptSubmit` | When a prompt is sent | Inject additional context into prompts |
| `Stop` | When the agent finishes | Validate the result, save session state |
| `SubagentStart` / `SubagentStop` | When a subagent spawns or completes | Track and aggregate parallel task results |
| `PreCompact` | Before context compaction | Archive full transcript before summarizing |

Two properties make hooks distinctive:

- **They run out-of-context.** Hooks run in your application process, not inside the agent's context window, so they don't consume context.
- **They can short-circuit the loop.** A `PreToolUse` hook that rejects a tool call prevents it from executing, and Claude receives the rejection message instead.

Both SDKs support all the events above. The TypeScript SDK includes additional events that Python does not yet support. The complete event list, per-SDK availability, and the full callback API are documented in [Control execution with hooks](https://code.claude.com/docs/en/agent-sdk/hooks).

## Put it all together

This example combines the key concepts from the agent loop into a single agent that fixes failing tests. It configures the agent with allowed tools (auto-approved so the agent runs autonomously), project settings, and safety limits on turns and reasoning effort. As the loop runs, it captures the session ID for potential resumption, handles the final result by branching on `subtype`, and prints the total cost.

```python Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def run_agent():
    session_id = None

    async for message in query(
        prompt="Find and fix the bug causing test failures in the auth module",
        options=ClaudeAgentOptions(
            allowed_tools=[
                "Read",
                "Edit",
                "Bash",
                "Glob",
                "Grep",
            ],  # Listing tools here auto-approves them (no prompting)
            setting_sources=[
                "project"
            ],  # Load CLAUDE.md, skills, hooks from current directory
            max_turns=30,  # Prevent runaway sessions
            effort="high",  # Thorough reasoning for complex debugging
        ),
    ):
        # Handle the final result
        if isinstance(message, ResultMessage):
            session_id = message.session_id  # Save for potential resumption

            if message.subtype == "success":
                print(f"Done: {message.result}")
            elif message.subtype == "error_max_turns":
                # Agent ran out of turns. Resume with a higher limit.
                print(f"Hit turn limit. Resume session {session_id} to continue.")
            elif message.subtype == "error_max_budget_usd":
                print("Hit budget limit.")
            else:
                print(f"Stopped: {message.subtype}")
            if message.total_cost_usd is not None:
                print(f"Cost: ${message.total_cost_usd:.4f}")


asyncio.run(run_agent())
```

The TypeScript form is equivalent: it iterates `query({ prompt, options })`, captures `session_id` from the init `SystemMessage` (`message.type === "system" && message.subtype === "init"`), and branches on `message.subtype` of the `result` message the same way. See the TypeScript SDK reference for the full dual-language listing.

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
