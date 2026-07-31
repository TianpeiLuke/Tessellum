---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
keywords:
  - claude code hooks
  - hook lifecycle
  - hook cadences
  - matcher group
  - hook handler
  - pretooluse resolution
  - hook configuration nesting
  - deterministic guardrail
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

# Claude Code Hooks — Overview

## Overview

**Hooks** are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle. When a lifecycle event fires and a matcher matches, Claude Code passes JSON context about the event to the hook handler (on stdin for command hooks, as the POST body for HTTP hooks); the handler inspects the input, takes action, and optionally returns a decision that can allow, block, or modify what happens next. Hooks are the deterministic, user-pluggable callback layer wrapped around the model loop — they let an autonomous coding agent enforce policy without a human in every iteration.

This note covers what a hook is, the three lifecycle *cadences*, the three-level configuration nesting, and an annotated walkthrough of how one hook resolves. The event catalog lives in [cc_hook_events_catalog](cc_hook_events_catalog.md); matcher/filter syntax in [cc_hook_matchers_and_filters](cc_hook_matchers_and_filters.md); handler types in [cc_hook_handler_types](cc_hook_handler_types.md); the I/O contract in [cc_hook_io_and_exit_codes](cc_hook_io_and_exit_codes.md). For a quickstart guide with examples, see the [hooks guide](https://code.claude.com/docs/en/hooks-guide).

## Hook lifecycle and cadences

Hooks fire at specific points during a Claude Code session. Events fall into three **cadences**:

- **Once per session** — `SessionStart`, `SessionEnd`.
- **Once per turn** — `UserPromptSubmit`, `Stop`, `StopFailure`.
- **On every tool call inside the agentic loop** — `PreToolUse`, `PostToolUse`.

The full set of events (30) and when each fires is enumerated in [cc_hook_events_catalog](cc_hook_events_catalog.md).

## How a hook resolves

Consider a `PreToolUse` hook that blocks destructive shell commands. The `matcher` narrows to Bash tool calls and the `if` condition narrows further to Bash subcommands matching `rm *`, so `block-rm.sh` only spawns when both filters match:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

When Claude Code decides to run `Bash "rm -rf /tmp/build"`, resolution proceeds in five steps:

1. **Event fires** — `PreToolUse` fires and Claude Code sends the tool input as JSON on stdin: `{ "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }`.
2. **Matcher checks** — the matcher `"Bash"` matches the tool name, so the hook group activates. Omitting the matcher or using `"*"` activates the group on every occurrence of the event.
3. **`if` condition checks** — `"Bash(rm *)"` matches `rm -rf /tmp/build`, so this handler spawns. Had the command been `npm test`, the `if` check would fail and `block-rm.sh` would never run, avoiding the process-spawn overhead. The `if` field is optional; without it, every handler in the matched group runs.
4. **Hook handler runs** — the script reads stdin, finds `rm -rf`, and prints a decision to stdout:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook"
  }
}
```

5. **Claude Code acts on the result** — it reads the JSON decision, blocks the tool call, and shows Claude the reason.

Exit code 0 with no output means the hook has no decision to report, so the tool call continues through the normal permission flow. A `PreToolUse` hook can *deny* the call, but staying silent does not *approve* it.

## Configuration: three levels of nesting

Hooks are defined in JSON settings files. The configuration has three levels of nesting:

1. Choose a **hook event** to respond to, like `PreToolUse` or `Stop`.
2. Add a **matcher group** to filter when it fires, like "only for the Bash tool".
3. Define one or more **hook handlers** — the shell command, HTTP endpoint, MCP tool, prompt, or agent — to run when matched.

The docs use precise terms for each level: **hook event** for the lifecycle point, **matcher group** for the filter, and **hook handler** for the thing that runs. "Hook" on its own refers to the general feature. Where you define a hook (user/project/local settings, managed policy, plugin `hooks/hooks.json`, or skill/agent frontmatter) determines its scope; see [cc_hook_handler_types](cc_hook_handler_types.md) for handler locations and the settings-file resolution order at [settings](https://code.claude.com/docs/en/settings).

## Related Notes

- [Claude Code](../../term_dictionary/term_claude_code.md) — Hooks are a Claude Code feature; this note is the entry point to Claude Code's hook subsystem, so the product term is its definitional anchor.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — Hooks fire at lifecycle points the harness exposes (session/turn/tool-call); they are the harness's user-pluggable callback layer around the model loop.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — The flagship hook example (`PreToolUse` blocking `rm -rf`) intercepts a tool call; hooks gate the tool-use mechanism this term defines.
- [Guardrails](../../term_dictionary/term_guardrails.md) — Hooks are the deterministic-guardrail mechanism in Claude Code: shell/HTTP/LLM checks that run automatically to allow, block, or modify actions.
- [Command Pattern](../../term_dictionary/term_command_pattern.md) — A hook handler encapsulates a request (event JSON in, decision out) as a runnable object registered against a lifecycle point — the encapsulate-request-as-object intent the Command pattern describes.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — The note frames hooks against the normal permission flow; a `PreToolUse` hook can deny but staying silent does not approve, tightening the progressive-trust permission model this term defines.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — Hooks are how an autonomous coding agent is made safe and deterministic at scale — they enforce policy on the agent's autonomous tool calls without a human in every loop.

**Source**: https://code.claude.com/docs/en/hooks
**Last Updated**: 2026-06-13
**Status**: Active
