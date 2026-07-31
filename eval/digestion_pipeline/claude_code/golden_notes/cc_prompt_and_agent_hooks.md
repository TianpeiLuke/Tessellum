---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - llm_judge
keywords:
  - prompt hook
  - agent hook
  - llm-as-judge hook
  - ok reason schema
  - $arguments placeholder
  - continueonblock
  - multi-criteria stop hook
  - experimental agent verifier
topics:
  - Claude Code
  - Hooks
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/hooks
access_control_group: ["general"]
---

# Claude Code Hooks — Prompt and Agent Hooks

## Overview

In addition to the deterministic command, HTTP, and MCP-tool [handler types](cc_hook_handler_types.md), Claude Code supports two LLM-based hook handler types that decide whether to allow or block an action by reasoning rather than by running fixed code. A **prompt hook** (`type: "prompt"`) sends the hook input plus your prompt to a Claude model for a single-turn yes/no evaluation. An **agent hook** (`type: "agent"`, experimental) spawns a subagent that can use tools like Read, Grep, and Glob over multiple turns to verify a condition before deciding. Both return the same structured `{ok, reason}` JSON decision, which Claude Code processes the same way for either type.

Not all events support every hook type. The set of events that support prompt and agent hooks is the subset that supports all five handler types — listed below.

## Which events support prompt and agent hooks

Prompt and agent hooks run only on events that support all five handler types (`command`, `http`, `mcp_tool`, `prompt`, and `agent`):

`PermissionDenied`, `PermissionRequest`, `PostToolBatch`, `PostToolUse`, `PostToolUseFailure`, `PreToolUse`, `Stop`, `SubagentStop`, `TaskCompleted`, `TaskCreated`, `TeammateIdle`, `UserPromptExpansion`, and `UserPromptSubmit`.

The remaining events support only command/HTTP/MCP-tool hooks (`ConfigChange`, `CwdChanged`, `Elicitation`, `ElicitationResult`, `FileChanged`, `InstructionsLoaded`, `Notification`, `PostCompact`, `PreCompact`, `SessionEnd`, `StopFailure`, `SubagentStart`, `WorktreeCreate`, `WorktreeRemove`), and `SessionStart` / `Setup` support only `command` and `mcp_tool`. (See [cc_hook_events_catalog](https://code.claude.com/docs/en/hooks) for the full event list.)

## Prompt-based hooks

A prompt hook does not execute a shell command. Instead it (1) sends the hook input and your prompt to a Claude model (Haiku by default), (2) the LLM responds with structured JSON containing a decision, and (3) Claude Code processes that decision automatically.

### Configuration

Set `type` to `"prompt"` and provide a `prompt` string instead of a `command`. Use the `$ARGUMENTS` placeholder to inject the hook's JSON input into your prompt text; if `$ARGUMENTS` is not present, the input JSON is appended to the prompt. This `Stop` hook asks the LLM to evaluate whether all tasks are complete before allowing Claude to finish:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

The prompt-hook-specific fields are: `type` (required, `"prompt"`); `prompt` (required); `model` (optional, defaults to a fast model); `timeout` (optional, default 30 seconds); and `continueOnBlock` (optional, default `false`). When the prompt returns `ok: false`, `continueOnBlock` feeds the reason back to Claude and continues the turn instead of stopping — it is implemented as `continue: true` on the resulting `decision: "block"`.

### Response schema

The LLM must respond with JSON containing an `ok` boolean and a `reason` string:

```json theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

`ok: true` allows the action; `ok: false` produces a `decision: "block"`. `reason` is required when `ok` is `false` and is used as the block reason.

What `ok: false` does depends on the event:

- `Stop` and `SubagentStop`: the reason is fed back to Claude as its next instruction and the turn continues.
- `PreToolUse`: the tool call is denied and the reason is returned to Claude as the tool error, equivalent to a command hook's `permissionDecision: "deny"`.
- `PostToolUse`: by default the turn ends and the reason appears as a warning line; set `continueOnBlock: true` to feed the reason back and continue.
- `PostToolBatch`, `UserPromptSubmit`, `UserPromptExpansion`: the turn ends and the reason appears as a warning line regardless of `continue`.
- `PostToolUseFailure`, `TaskCreated`, `TaskCompleted`: the reason is returned to Claude as a tool error, similar to `PreToolUse`.
- `TeammateIdle`: by default the teammate stops; `continueOnBlock: true` keeps it working.
- `PermissionRequest` and `PermissionDenied`: `ok: false` has no effect — use a command hook (`decision.behavior: "deny"` or `retry`) for these. Prompt and agent hooks run on `PermissionDenied` but their output is discarded.

For finer control on any event, use a command hook with the per-event fields in [cc_hook_io_and_exit_codes](cc_hook_io_and_exit_codes.md).

### Example: multi-criteria Stop hook

This `Stop` hook uses a detailed prompt that asks the model to check three completion criteria before allowing Claude to stop; if `ok` is `false`, Claude continues with the reason as its next instruction. `SubagentStop` hooks use the same format:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Agent-based hooks

Agent hooks are **experimental** — behavior and configuration may change, and the docs recommend command hooks for production workflows. An agent hook (`type: "agent"`) is like a prompt hook but with multi-turn tool access: instead of a single LLM call, it spawns a subagent that can read files, search code, and inspect the codebase to verify conditions. Agent hooks support the same events as prompt hooks.

### How agent hooks work

When an agent hook fires: (1) Claude Code spawns a subagent with your prompt and the hook's JSON input; (2) the subagent can use tools like Read, Grep, and Glob to investigate; (3) after up to **50 turns** the subagent returns a structured `{ "ok": true/false }` decision; (4) Claude Code processes the decision the same way as a prompt hook. Agent hooks are useful when verification requires inspecting actual files or test output, not just the hook input data alone.

### Agent hook configuration

Set `type` to `"agent"` and provide a `prompt` string. The fields are the same as prompt hooks — `type` (required, `"agent"`), `prompt` (required, with `$ARGUMENTS`), `model` (optional, fast model default), `timeout` (optional) — except the default `timeout` is **60 seconds** rather than 30. The response schema is identical: `{ "ok": true }` to allow or `{ "ok": false, "reason": "..." }` to block. This `Stop` hook verifies that all unit tests pass before allowing Claude to finish:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

**Source**: https://code.claude.com/docs/en/hooks
**Last Updated**: 2026-06-13
**Status**: Active
