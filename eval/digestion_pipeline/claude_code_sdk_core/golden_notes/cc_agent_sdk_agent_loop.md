---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - agent_loop
keywords:
  - agent loop
  - the loop at a glance
  - turns and messages
  - turn
  - tool-use turn
  - max_turns
  - max_budget_usd
  - receive evaluate execute repeat return
  - agent sdk loop
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

# Agent SDK — The Agent Loop

## Overview

The Agent SDK embeds Claude Code's autonomous agent loop in your own application, running **the same execution loop that powers Claude Code**: Claude evaluates your prompt, calls tools to take action, receives the results, and repeats until the task is complete. This note covers the loop's high-level shape ("The loop at a glance") and the mechanics of **turns** ("Turns and messages") — what one turn is, how a multi-turn session unfolds, and how to cap how far the loop runs with `max_turns` and `max_budget_usd`.

The SDK is a standalone package that gives programmatic control over tools, permissions, cost limits, and output; you do not need the Claude Code CLI installed to use it. Each stage of the loop surfaces as a typed message in the SDK's output stream — those message types, the tool-execution mechanics, the loop-control options, the context window, and the final result are documented in the sibling notes linked below.

## The loop at a glance

Every agent session follows the same cycle:

1. **Receive prompt.** Claude receives your prompt, along with the system prompt, tool definitions, and conversation history. The SDK yields a `SystemMessage` with subtype `"init"` containing session metadata.
2. **Evaluate and respond.** Claude evaluates the current state and determines how to proceed. It may respond with text, request one or more tool calls, or both. The SDK yields an `AssistantMessage` containing the text and any tool call requests.
3. **Execute tools.** The SDK runs each requested tool and collects the results. Each set of tool results feeds back to Claude for the next decision. You can use hooks to intercept, modify, or block tool calls before they run.
4. **Repeat.** Steps 2 and 3 repeat as a cycle. Each full cycle is one turn. Claude continues calling tools and processing results until it produces a response with no tool calls.
5. **Return result.** The SDK yields a final `AssistantMessage` with the text response (no tool calls), followed by a `ResultMessage` with the final text, token usage, cost, and session ID.

The number of turns scales with task complexity. A quick question ("what files are here?") might take one or two turns of calling `Glob` and responding with the results. A complex task ("refactor the auth module and update the tests") can chain dozens of tool calls across many turns, reading files, editing code, and running tests, with Claude adjusting its approach based on each result.

The five message types this cycle emits are covered in [Agent SDK — Message Types](cc_agent_sdk_message_types.md); the tool-execution step (step 3) is covered in [Agent SDK — Tool Execution](cc_agent_sdk_tool_execution.md); the final result (step 5) is covered in [Agent SDK — Result and Hooks](cc_agent_sdk_result_and_hooks.md).

## Turns and messages

A **turn** is one round trip inside the loop: Claude produces output that includes tool calls, the SDK executes those tools, and the results feed back to Claude automatically. This happens without yielding control back to your code. Turns continue until Claude produces output with no tool calls, at which point the loop ends and the final result is delivered.

### Example session

Consider what a full session might look like for the prompt "Fix the failing tests in auth.ts". First, the SDK sends your prompt to Claude and yields a `SystemMessage` with the session metadata. Then the loop begins:

1. **Turn 1:** Claude calls `Bash` to run `npm test`. The SDK yields an `AssistantMessage` with the tool call, executes the command, then yields a `UserMessage` with the output (three failures).
2. **Turn 2:** Claude calls `Read` on `auth.ts` and `auth.test.ts`. The SDK returns the file contents and yields an `AssistantMessage`.
3. **Turn 3:** Claude calls `Edit` to fix `auth.ts`, then calls `Bash` to re-run `npm test`. All three tests pass. The SDK yields an `AssistantMessage`.
4. **Final turn:** Claude produces a text-only response with no tool calls: "Fixed the auth bug, all three tests pass now." The SDK yields a final `AssistantMessage` with this text, then a `ResultMessage` with the same text plus cost and usage.

That was four turns: three with tool calls, one final text-only response.

### Capping the loop

You can cap the loop with `max_turns` / `maxTurns`, which **counts tool-use turns only**. For example, `max_turns=2` in the loop above would have stopped before the edit step. You can also use `max_budget_usd` / `maxBudgetUsd` to cap turns based on a spend threshold.

Without limits, the loop runs until Claude finishes on its own, which is fine for well-scoped tasks but can run long on open-ended prompts ("improve this codebase"). Setting a budget is a good default for production agents. The full option reference (turns/budget, effort level, permission mode, model) lives in [Agent SDK — Loop Controls](cc_agent_sdk_loop_controls.md).

### Sessions and continuity

Each interaction with the SDK creates or continues a **session**. The context window does not reset between turns within a session — everything accumulates across turns (covered in [Agent SDK — Context Window](cc_agent_sdk_context_window.md)). Capture the session ID from `ResultMessage.session_id` to resume later; see [Session management](https://code.claude.com/docs/en/agent-sdk/sessions) for the full resume, continue, and fork guide.

## Related Notes

### Related Notes (Claude Code Series)

- [Agent SDK Overview](cc_agent_sdk_overview.md) — relevance: the overview frames the SDK as "Claude Code as a library" that gives you "the same agent loop"; this note is the detailed teardown of that loop the overview introduces.
- [Agent SDK — Message Types](cc_agent_sdk_message_types.md) — relevance: each loop stage here (init, assistant turn, tool result, final result) surfaces as one of the five typed messages; this sibling documents the stream the loop emits, dissecting the same loop's "Message types" slice.
- [Agent SDK — Tool Execution](cc_agent_sdk_tool_execution.md) — relevance: step 3 of this loop ("Execute tools") is the action half the sibling expands — built-in tools, allowed/disallowed gating, and parallel vs sequential execution within a turn.
- [Agent SDK — Loop Controls](cc_agent_sdk_loop_controls.md) — relevance: this note introduces `max_turns`/`max_budget_usd` as the caps on the loop; the sibling is the full option reference (turns, budget, effort, permission mode, model) for shaping how far the loop runs.
- [Agent SDK — Handling the Result and Loop Hooks](cc_agent_sdk_result_and_hooks.md) — relevance: step 5 ("Return result") yields the `ResultMessage` the sibling documents, and hooks intercept the tool-execution step this loop describes ("use hooks to intercept, modify, or block tool calls").
- [Claude Code — The Agentic Loop](cc_agentic_loop.md) — relevance: the conceptual parent — Claude Code's gather-context / take-action / verify-results loop is the same cycle this SDK loop embeds programmatically; both describe Claude chaining tool calls and course-correcting per result.

### Related Notes (Out-of-Series)

- [Claude Code](../../term_dictionary/term_claude_code.md) — the SDK runs "the same execution loop that powers Claude Code"; relevance: the product term anchors the loop this note dissects.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — the agent harness (tools + context management + execution loop wrapping the LLM); relevance: the receive→evaluate→execute→repeat→return cycle is the harness's core control flow, documented here as its runtime cycle.
- [ReAct](../../term_dictionary/term_react.md) — the interleaved reason-act-observe pattern; relevance: the loop's evaluate-call-tool-observe-result-repeat cycle, where each tool result feeds the next decision, is exactly what ReAct formalizes.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — the class of agents that act multi-step without manual intervention; relevance: the note describes a complex task chaining "dozens of tool calls across many turns," Claude adjusting per result — the autonomous behavior this term defines.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — the model requesting tools whose results feed back; relevance: a "turn" is exactly one tool-use round trip, so function-calling is the unit the loop iterates on.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — controlling how an agent's loop runs; relevance: `max_turns`/`max_budget_usd` and the turn-by-turn control of when the loop stops are loop-orchestration controls this term frames.
- [Context Window](../../term_dictionary/term_context_window.md) — the total information available to Claude in a session; relevance: the loop accumulates conversation and tool I/O into the context window across turns within a session — the container the loop fills (detailed in the context-window note).
- [ACP (Agent Client Protocol)](../../term_dictionary/term_acp_agent_client_protocol.md) — the protocol for editor/agent communication; relevance: the loop's message-driven request/response cycle between host process and agent runtime parallels the agent-client protocol pattern this term describes.
- [Tool: Strands Agents — Open-Source AI Agents SDK](../../tools/tool_strands_agents.md) — relevance: an AWS agent SDK that, like the Agent SDK, packages the same model-reasons-then-tools loop into a library; the cross-vendor analog of the loop this note documents.
- [Agentic AI Golden Path — Agent Patterns](../org_docs/org_agentic_golden_path_agent_patterns.md) — relevance: its ReAct pattern is described as "an agentic loop where LLM decides when to exit or continue invoking tools" with the Observe→Think→Act→Exit flow — the same evaluate/execute/repeat-until-no-tool-calls cycle this note specifies.
- [Bedrock Agents: How It Works (Runtime Process)](../aws_bedrock/bedrock_agents_how_it_works.md) — relevance: AWS Bedrock's "Orchestration Loop" iteratively plans and executes actions until a Finish step, the hosted-service counterpart to the receive→evaluate→execute→repeat→return cycle here.
- [Bedrock Agents: Handle Fulfillment with Return Control](../aws_bedrock/bedrock_agents_action_handle_return_control.md) — relevance: return control's "agent predicts action → your app executes → send results back in another InvokeAgent request" is the tool-result-feedback mechanic of step 3/step 4, externalized to the caller instead of run by the SDK.
- [Project: 2-Step Account Recovery Reviewer Agent](../../../projects/project_account_recovery_agent.md) — relevance: a production AI agent that "replicates investigator workflows" and resolves tasks "automatically" — a real production application of the autonomous receive→act→repeat loop this note describes.

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
