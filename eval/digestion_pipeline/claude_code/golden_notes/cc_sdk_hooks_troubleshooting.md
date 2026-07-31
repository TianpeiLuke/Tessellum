---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - hooks
keywords:
  - sdk hooks troubleshooting
  - hook not firing
  - matcher not filtering
  - hook timeout
  - tool blocked unexpectedly
  - modified input not applied
  - session hooks python
  - subagent permission prompts
  - recursive hook loops
  - systemmessage not appearing
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

# Claude Code Agent SDK — Hook Troubleshooting

## Overview

This note collects the nine "Fix common issues" diagnostics from the Agent SDK hooks page — the failure modes an SDK application hits when wiring hooks in via `options.hooks` (see [Hook Configuration](cc_sdk_hooks_configuration.md)) and the recipes from [Hook Examples](cc_sdk_hooks_examples.md). Each diagnostic names a symptom (a hook silently never runs, a matcher matches the wrong tools, a tool gets blocked, a message never surfaces) and gives the concrete check or fix. The issues cluster into registration/matching problems, decision-output problems, and subagent-specific problems.

## Hook not firing

When a registered hook never runs, check the registration:

- Verify the hook event name is correct and **case-sensitive** (`PreToolUse`, not `preToolUse`).
- Check that the matcher pattern matches the tool name exactly.
- Ensure the hook is under the correct event type in `options.hooks`.
- For non-tool hooks like `Stop` and `SubagentStop`, matchers match against different fields (see the matcher patterns in the [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)).
- Hooks may not fire when the agent hits the `max_turns` limit, because the session ends before hooks can execute.

## Matcher not filtering as expected

Matchers match only **tool names**, not file paths or other arguments. To filter by file path, check `tool_input.file_path` inside the hook itself:

```typescript
const myHook: HookCallback = async (input, toolUseID, { signal }) => {
  const preInput = input as PreToolUseHookInput;
  const toolInput = preInput.tool_input as Record<string, unknown>;
  const filePath = toolInput?.file_path as string;
  if (!filePath?.endsWith(".md")) return {}; // Skip non-markdown files
  // Process markdown files...
  return {};
};
```

## Hook timeout

- Increase the `timeout` value in the `HookMatcher` configuration.
- Use the `AbortSignal` from the third callback argument to handle cancellation gracefully in TypeScript.

## Tool blocked unexpectedly

- Check all `PreToolUse` hooks for `permissionDecision: 'deny'` returns.
- Add logging to the hooks to see what `permissionDecisionReason` they return.
- Verify matcher patterns aren't too broad (an empty matcher matches all tools).

## Modified input not applied

Ensure `updatedInput` sits **inside** `hookSpecificOutput`, not at the top level. Return `permissionDecision: 'allow'` to auto-approve the modified input (or `'ask'` to show it to the user), and include `hookEventName` to identify which hook type the output is for:

```typescript
return {
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "allow",
    updatedInput: { command: "new command" }
  }
};
```

## Session hooks not available in Python

`SessionStart` and `SessionEnd` can be registered as SDK callback hooks in TypeScript, but are **not available in the Python SDK** (`HookEvent` omits them). In Python they are only available as shell command hooks defined in settings files (for example, `.claude/settings.json`). To load shell command hooks from an SDK application, include the appropriate setting source with `setting_sources` (Python) or `settingSources` (TypeScript), e.g. `setting_sources=["project"]` loads `.claude/settings.json` including hooks. To run initialization logic as a Python SDK callback instead, use the first message from `client.receive_response()` as the trigger.

## Subagent permission prompts multiplying

When spawning multiple subagents, each one may request permissions separately — subagents do **not** automatically inherit parent-agent permissions. To avoid repeated prompts, use `PreToolUse` hooks to auto-approve specific tools, or configure permission rules that apply to subagent sessions.

## Recursive hook loops with subagents

A `UserPromptSubmit` hook that spawns subagents can create infinite loops if those subagents trigger the same hook. To prevent this:

- Check for a subagent indicator in the hook input before spawning.
- Use a shared variable or session state to track whether you're already inside a subagent.
- Scope hooks to only run for the top-level agent session.

## systemMessage not appearing in output

The `systemMessage` field shows a message to the user, not the model. By default the SDK does **not** surface hook output in the message stream, so the message may not appear unless you set `includeHookEvents` (`include_hook_events` in Python). To pass context to the model instead, return `additionalContext`. If you need to surface hook decisions to your application reliably, log them separately or use a dedicated output channel.

**Source**: https://code.claude.com/docs/en/agent-sdk/hooks
**Last Updated**: 2026-06-13
**Status**: Active
