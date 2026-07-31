---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - tool_loop
keywords:
  - pretooluse hook
  - posttooluse hook
  - permissionrequest hook
  - permissiondecision allow deny ask defer
  - updatedinput updatedtooloutput
  - permission update entries
  - posttoolbatch
  - permissiondenied retry
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

# Claude Code Hooks — Tool-Loop Events

## Overview

Six hook events fire on **every tool call inside the agentic loop** — the per-tool-call cadence. They are: `PreToolUse` (before a call runs), `PermissionRequest` (when a permission dialog appears), `PostToolUse` (after a call succeeds), `PostToolUseFailure` (after a call fails), `PostToolBatch` (once after a parallel batch resolves), and `PermissionDenied` (when the auto-mode classifier denies a call). All except `PostToolBatch` match on `tool_name` with the same value set (`Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, `AskUserQuestion`, `ExitPlanMode`, and any `mcp__server__tool` names).

These events are where a hook participates in Claude Code's permission flow and where it can **rewrite** rather than only allow or block: `PreToolUse` deny/ask/defer and `updatedInput`, `PermissionRequest` allow/deny with permission-update entries, and `PostToolUse` `updatedToolOutput`. This note documents each event's input highlights and decision control; the full per-tool `tool_input` schemas and the cross-event exit-code table live at the source page and in [`cc_hook_io_and_exit_codes`](cc_hook_io_and_exit_codes.md). The navigational index of all 30 events is [`cc_hook_events_catalog`](cc_hook_events_catalog.md).

## PreToolUse

Runs after Claude creates tool parameters and before the tool call is processed — the one event that can stop a call before it happens. Input adds `tool_name`, `tool_input`, and `tool_use_id` to the common fields; the `tool_input` shape depends on the tool (e.g. `Bash` carries `command`/`description`/`timeout`/`run_in_background`; full per-tool tables → source page).

### PreToolUse decision control

Unlike events that use a top-level `decision`, `PreToolUse` returns its decision inside `hookSpecificOutput`, giving four outcomes plus input rewriting:

| Field | Meaning |
| :-- | :-- |
| `permissionDecision` | `"allow"` skips the prompt; `"deny"` prevents the call; `"ask"` prompts the user; `"defer"` exits gracefully so the call can be resumed later. Deny and ask rules are still evaluated regardless of what the hook returns |
| `permissionDecisionReason` | For allow/ask shown to the user (not Claude); for deny shown to Claude; for defer ignored |
| `updatedInput` | Replaces the **entire** tool input object before execution — include unchanged fields alongside modified ones. Combine with `"allow"` to auto-approve or `"ask"` to show the modified input |
| `additionalContext` | String added to Claude's context alongside the tool result; ignored for `"defer"` |

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

When multiple `PreToolUse` hooks return different decisions, precedence is `deny` > `defer` > `ask` > `allow`. When a hook returns `"ask"`, the prompt shows a source label (`[User]`, `[Project]`, `[Plugin]`, `[Local]`). Top-level `decision`/`reason` are deprecated for this event (`"approve"`/`"block"` map to `"allow"`/`"deny"`).

### Defer a tool call for later

`"defer"` is for integrations running `claude -p` as a subprocess (e.g. an Agent SDK app or custom UI): it lets the calling process pause Claude at a tool call, collect input through its own interface, and resume. It is honored only in non-interactive `-p` mode (interactive sessions log a warning and ignore it) and requires Claude Code v2.1.89+. The typical case is `AskUserQuestion` when there is no terminal to answer in:

1. Claude calls the tool; the `PreToolUse` hook fires and returns `"defer"`. The tool does not execute; the process exits with `stop_reason: "tool_deferred"`.
2. The calling process reads `deferred_tool_use` (carrying the tool's `id`, `name`, and the generated `input`), surfaces the question in its own UI, then runs `claude -p --resume <session-id>`.
3. The same call fires `PreToolUse` again; the hook returns `"allow"` with the answer in `updatedInput`, and the tool executes.

There is no timeout or retry limit; the session stays on disk subject to `cleanupPeriodDays` (30-day default sweep). `"defer"` only works when Claude makes a single tool call in the turn — with several at once it is ignored with a warning. If the deferred tool is gone on resume, the process exits with `stop_reason: "tool_deferred_unavailable"` and `is_error: true`.

## PermissionRequest

Runs when a permission dialog is about to be shown. Matches on tool name (same values as `PreToolUse`). Input gives `tool_name` and `tool_input` (but no `tool_use_id`) plus an optional `permission_suggestions` array — the "always allow" options the user would normally see.

### PermissionRequest decision control

Returns a `decision` object that allows or denies on the user's behalf:

| Field | Meaning |
| :-- | :-- |
| `behavior` | `"allow"` grants, `"deny"` denies. Deny and ask rules are still evaluated, so `"allow"` does not override a matching deny rule |
| `updatedInput` | Allow-only: replaces the entire input object; the modified input is re-evaluated against deny and ask rules |
| `updatedPermissions` | Allow-only: array of permission-update entries to apply |
| `message` | Deny-only: tells Claude why permission was denied |
| `interrupt` | Deny-only: if `true`, stops Claude |

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

### Permission update entries

The `updatedPermissions` output and the `permission_suggestions` input share one array of entry objects. Each entry has a `type` (which determines its other fields) and a `destination` (which controls where the change is written). Types: `addRules` / `replaceRules` / `removeRules` (each with `rules`, `behavior` of `"allow"`/`"deny"`/`"ask"`, `destination`), `setMode` (`mode`, `destination`), and `addDirectories` / `removeDirectories` (`directories`, `destination`). Destinations are `session` (in-memory), `localSettings`, `projectSettings`, and `userSettings`. A hook can echo back one of the `permission_suggestions` it received as its own `updatedPermissions`, equivalent to the user selecting that "always allow" option. (`setMode` with `bypassPermissions` only takes effect if the session was launched with bypass already available; permission-rule syntax → [permissions](https://code.claude.com/docs/en/permissions).)

## PostToolUse

Runs immediately after a tool completes successfully. Matches on tool name. Input includes `tool_input` (the arguments), `tool_response` (the result, shape depends on the tool), `tool_use_id`, and an optional `duration_ms`. Decision control fields:

| Field | Meaning |
| :-- | :-- |
| `decision` | `"block"` adds `reason` next to the tool result (Claude still sees the original output) |
| `reason` | Explanation shown to Claude when `decision` is `"block"` |
| `additionalContext` | String added to Claude's context alongside the result |
| `updatedToolOutput` | Replaces the tool's output before it reaches Claude; the value **must match the tool's output shape** |
| `updatedMCPToolOutput` | Replaces output for MCP tools only; prefer `updatedToolOutput`, which works for all tools |

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude",
    "updatedToolOutput": {
      "stdout": "[redacted]",
      "stderr": "",
      "interrupted": false,
      "isImage": false
    }
  }
}
```

`updatedToolOutput` only changes what Claude sees — the tool has already run, so files written, commands executed, or requests sent already took effect (telemetry also captures the original). For built-in tools a value not matching the output schema is ignored; MCP output is passed through unvalidated. To prevent or modify a call before it runs, use `PreToolUse` instead. For redaction/transformation, intercept inputs at `PreToolUse` and results at `PostToolUse`.

## PostToolUseFailure

Runs when a tool execution fails (throws an error or returns a failure result). Matches on tool name. Beyond the `PostToolUse` input fields, it adds top-level `error` (a string describing what went wrong), an optional `is_interrupt` boolean (whether a user interruption caused the failure), and optional `duration_ms`. Decision control offers only `additionalContext` — there is no blocking, since the tool already failed; use it to log failures, send alerts, or give corrective feedback.

## PostToolBatch

Runs once after every tool call in a batch resolves, before the next model request. `PostToolUse` fires once per tool (concurrently on parallel calls); `PostToolBatch` fires exactly once with the full batch, so it is the place to inject context that depends on the *set* of tools that ran. There is no matcher. Input adds `tool_calls`, an array describing every call (each with `tool_name`, `tool_input`, `tool_use_id`, `tool_response`). Note the `tool_response` shape differs from `PostToolUse`'s — `PostToolBatch` passes the serialized `tool_result` content the model sees (e.g. line-number-prefixed text for `Read`), not the structured output object. Decision control offers `additionalContext`; returning `decision: "block"` or `continue: false` stops the agentic loop before the next model call.

## PermissionDenied

Runs when the **auto-mode classifier** denies a tool call. It fires only in auto mode — not on a manually denied dialog, a `PreToolUse` block, or a matching `deny` rule. Input adds `tool_name`, `tool_input`, `tool_use_id`, and `reason` (the classifier's explanation). Decision control: returning `hookSpecificOutput.retry: true` tells the model it may retry the denied call.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

The denial itself is not reversed — `retry: true` only adds a message telling the model it may try again. If the hook returns no JSON or `retry: false`, the denial stands and the model receives the original rejection.

## Related Notes

- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — every event here fires around a tool call and matches on `tool_name`, so they instrument the tool-use mechanism directly.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — `PreToolUse.permissionDecision` (allow/deny/ask/defer) and `PermissionRequest.decision.behavior` (allow/deny) are how hooks participate in Claude Code's progressive-trust permission flow.
- [Deny-First (Default Deny)](../../term_dictionary/term_deny_first.md) — these are the deny-first enforcement points: a hook can deny a call before it runs (PreToolUse) or deny a permission (PermissionRequest), with silence never implying approval.
- [Reversibility-Weighted Risk Assessment](../../term_dictionary/term_reversibility_weighted_risk.md) — `PreToolUse` defer and the deny/ask escalation let a hook gate irreversible calls (e.g. destructive Bash) more tightly than reversible ones — the reversibility-weighted approval threshold.
- [Claude Code](../../term_dictionary/term_claude_code.md) — the tool-loop events are points in Claude Code's own agentic loop; the note documents that product behavior.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — these are the harness's per-tool-call callback sites inside the loop; `updatedInput`/`updatedToolOutput` let a hook rewrite what the harness passes to or returns from a tool.
- [Guardrails](../../term_dictionary/term_guardrails.md) — blocking a call, redacting its input at `PreToolUse`, or rewriting its output at `PostToolUse` are the deterministic guardrail patterns these events enable.
- [Hook Events Catalog](cc_hook_events_catalog.md) — the navigational index of all 30 events, including these 6 tool-loop rows and their cadence.
- [Hook I/O and Exit Codes](cc_hook_io_and_exit_codes.md) — the common stdin fields, the exit-code-2-per-event table, and the universal JSON output fields these decision objects extend.
- [Hook Matchers and Filters](cc_hook_matchers_and_filters.md) — how `tool_name` matchers and the `if` filter narrow which of these tool-loop hooks run.
- [Hook Session and Lifecycle Events](cc_hook_session_lifecycle_events.md) — the complementary session/turn/non-tool events for the other 24 catalog entries.

**Source**: https://code.claude.com/docs/en/hooks
**Last Updated**: 2026-06-13
**Status**: Active
