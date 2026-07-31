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

## Related Notes

### Related Notes (Claude Code Series)
- [Agent SDK — How the Agent Loop Works](cc_agent_sdk_agent_loop.md) — relevance: the receive-evaluate-execute-repeat-return cycle that yields the `ResultMessage` this note's "Handle the result" section dissects and fires the hooks it documents; this note is the loop's termination + lifecycle half
- [Agent SDK — Controlling How the Loop Runs](cc_agent_sdk_loop_controls.md) — relevance: the `max_turns`/`max_budget_usd`/`effort` caps whose limits produce the `error_max_turns`/`error_max_budget_usd` result subtypes here; that note explicitly defers the error-subtype handling to this one
- [Agent SDK — Message Types](cc_agent_sdk_message_types.md) — relevance: `ResultMessage` is one of the five core message types; this note documents its terminating-message contract (subtype, `result`, `stop_reason`) in depth while that note frames the whole stream
- [Claude Code Agent SDK — Hooks Overview](cc_sdk_hooks_overview.md) — relevance: the conceptual model for the hook callbacks this note's "Hooks" section summarizes — the five-step fire/collect/match/execute/decide flow and the full per-SDK event-availability table
- [SDK Cost and Usage Tracking](cc_sdk_cost_and_usage_tracking.md) — relevance: expands the `total_cost_usd`/`usage` fields this note says every `ResultMessage` subtype carries, including the client-side-estimate caveat behind the "guard before formatting" note here
- [Claude Code Hooks — Tool-Loop Events](cc_hook_tool_loop_events.md) — relevance: the CLI-side detail of the `PreToolUse`/`PostToolUse` short-circuit-and-rewrite mechanics this note introduces, with the full decision-control and `updatedInput`/`updatedToolOutput` schemas

### Related Notes (Out-of-Series)
- [Claude Code](../../term_dictionary/term_claude_code.md) — relevance: the `ResultMessage` and loop hooks are the Claude-Code-derived SDK's termination and lifecycle surface; the product term anchors the API
- [Structured Output](../../term_dictionary/term_structured_output.md) — relevance: the `ResultMessage` subtype table (incl. `error_max_structured_output_retries`) plus typed `total_cost_usd`/`usage`/`stop_reason` is the structured-result contract this term defines
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — relevance: hooks fire "at specific points in the loop" run by the harness; the harness term frames the lifecycle this note hooks into
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — relevance: `PreToolUse`/`PostToolUse` hooks bracket each tool call and can short-circuit it (rejection becomes the tool result) — the function-calling step the hooks intercept
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — relevance: a `PreToolUse` hook that rejects a tool call is a programmatic graduated-trust gate (block dangerous commands before they run) this term defines
- [Subagent](../../term_dictionary/term_subagent.md) — relevance: the hooks table includes `SubagentStart`/`SubagentStop` for tracking spawned subagents; the term grounds those subagent-lifecycle hook events
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — relevance: the note stresses hooks "run in your application process, not inside the agent's context window, so they don't consume context" — a deliberate context-engineering property this term frames
- [Observability (Agent Systems)](../../term_dictionary/term_observability_agent_systems.md) — relevance: `PostToolUse` audit hooks, the out-of-context observe-only hooks, and the per-result `usage`/`total_cost_usd`/`session_id` fields are the agent-observability surface (token/cost tracking, trajectory tracing) this term defines
- [Tool: Strands Agents — Open-Source AI Agents SDK](../../tools/tool_strands_agents.md) — relevance: a directly comparable agent SDK (AWS, model-driven loop) — useful contrast for how a different SDK exposes its loop termination and tool-interception surface versus the Agent SDK's `ResultMessage`/hooks
- [AgentCore Observability — Architecture and Overview](../aws_bedrock_agentcore/bedrock_agentcore_observability_overview.md) — relevance: the production tracing/auditing/debugging surface that records each step of an agent workflow — the AWS analogue to using `PostToolUse` hooks and the result's `usage`/cost fields to observe a deployed agent
- [Bedrock Agents: Trace Events Structure](../aws_bedrock/bedrock_agents_trace_structure.md) — relevance: each agent invocation returns a step-by-step trace plus `sessionId` for debugging behavior — a parallel to how this note's `ResultMessage` carries `session_id` and how observe-only hooks expose the loop's internal steps
- [AgentCore Sessions — Usage and Lifecycle](../aws_bedrock_agentcore/bedrock_agentcore_sessions_usage.md) — relevance: session lifecycle states and correct session-ID use mirror this note's capturing `message.session_id` from the `ResultMessage` to resume after an `error_max_turns` termination
- *(No project note is closely relevant: the domain-specific multi-agent projects, e.g. the auditing and callout agents, build on agents but do not document the SDK's `ResultMessage` termination contract or loop-hook events.)*

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
