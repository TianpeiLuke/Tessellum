---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - hook_types
keywords:
  - prompt-based hooks
  - agent-based hooks
  - http hooks
  - judgment-based hooks
  - haiku evaluation
  - ok reason decision
  - subagent verification
  - allowedenvvars
topics:
  - Claude Code
  - Hooks
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/hooks-guide
access_control_group: ["general"]
---

# Claude Code Hooks — Advanced (Non-Command) Hook Types

## Overview

Most Claude Code hooks use `"type": "command"` to run a deterministic shell command, but three other hook types handle decisions that require judgment or remote handling rather than fixed rules: **prompt-based hooks** (`type: "prompt"`), **agent-based hooks** (`type: "agent"`), and **HTTP hooks** (`type: "http"`). Prompt and agent hooks send the hook's input to a Claude model to evaluate a condition and return a yes/no decision; HTTP hooks POST the event data to an external endpoint that returns the decision. (A fifth type, `mcp_tool`, calls a tool on an already-connected MCP server — its fields are owned by the [Hooks reference](https://code.claude.com/docs/en/hooks#mcp-tool-hook-fields), not this note.)

These types extend the same event/matcher/I-O model the command hooks use; they differ only in *how the decision is produced*. Full configuration options for each live in the reference and are linked out below.

## Prompt-based hooks

For decisions that require judgment rather than deterministic rules, use `type: "prompt"` hooks. Instead of running a shell command, Claude Code sends your prompt and the hook's input data to a Claude model (Haiku by default) to make the decision. You can specify a different model with the `model` field if you need more capability.

The model's only job is to return a yes/no decision as JSON:

* `"ok": true`: the action proceeds
* `"ok": false`: what happens depends on the event:
  * `Stop` and `SubagentStop`: the `reason` is fed back to Claude so it keeps working
  * `PreToolUse`: the tool call is denied and the `reason` is returned to Claude as the tool error, so it can adjust and continue
  * `PostToolUse`, `PostToolBatch`, `UserPromptSubmit`, and `UserPromptExpansion`: the turn ends and the `reason` appears in the chat as a warning line

This example uses a `Stop` hook to ask the model whether all requested tasks are complete. If the model returns `"ok": false`, Claude keeps working and uses the `reason` as its next instruction:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

For full configuration options, see [Prompt-based hooks](https://code.claude.com/docs/en/hooks#prompt-based-hooks) in the reference.

## Agent-based hooks

> Agent hooks are **experimental**. Behavior and configuration may change in future releases. For production workflows, prefer command hooks ([command hook fields](https://code.claude.com/docs/en/hooks#command-hook-fields)).

When verification requires inspecting files or running commands, use `type: "agent"` hooks. Unlike prompt hooks which make a single LLM call, agent hooks spawn a subagent that can read files, search code, and use other tools to verify conditions before returning a decision.

Agent hooks use the same `"ok"` / `"reason"` response format as prompt hooks, but with a longer default timeout of 60 seconds and up to 50 tool-use turns.

This example verifies that tests pass before allowing Claude to stop:

```json
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

Use prompt hooks when the hook input data alone is enough to make a decision. Use agent hooks when you need to verify something against the actual state of the codebase.

For full configuration options, see [Agent-based hooks](https://code.claude.com/docs/en/hooks#agent-based-hooks) in the reference.

## HTTP hooks

Use `type: "http"` hooks to POST event data to an HTTP endpoint instead of running a shell command. The endpoint receives the same JSON that a command hook would receive on stdin, and returns results through the HTTP response body using the same JSON format.

HTTP hooks are useful when you want a web server, cloud function, or external service to handle hook logic: for example, a shared audit service that logs tool use events across a team.

This example posts every tool use to a local logging service:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

The endpoint should return a JSON response body using the same [output format](https://code.claude.com/docs/en/hooks#json-output) as command hooks. To block a tool call, return a 2xx response with the appropriate `hookSpecificOutput` fields. HTTP status codes alone cannot block actions.

Header values support environment variable interpolation using `$VAR_NAME` or `${VAR_NAME}` syntax. Only variables listed in the `allowedEnvVars` array are resolved; all other `$VAR` references remain empty.

For full configuration options and response handling, see [HTTP hooks](https://code.claude.com/docs/en/hooks#http-hook-fields) in the reference.

**Source**: https://code.claude.com/docs/en/hooks-guide
**Last Updated**: 2026-06-13
**Status**: Active
