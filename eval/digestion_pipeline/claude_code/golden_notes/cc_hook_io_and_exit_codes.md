---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - io_contract
keywords:
  - hook input output
  - stdin json
  - exit code 2
  - blocking error
  - additionalcontext
  - decision control
  - systemmessage
  - terminalsequence
  - http response handling
  - hookspecificoutput
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

# Claude Code — Hook Input and Output (Exit Codes, JSON, Decision Control)

## Overview

Every Claude Code hook follows the same I/O contract: it receives JSON describing the event and communicates results back through an exit code, stdout, and stderr. Command hooks read the JSON on stdin and reply via exit code + stdout; HTTP hooks receive the same JSON as the POST body and reply via HTTP status code + response body; MCP-tool hooks have their text output treated like command-hook stdout. A hook signals its outcome two ways, and you must pick one per hook: **exit codes alone** (0 = success, 2 = blocking error, anything else = non-blocking error) or **exit 0 plus a JSON object on stdout** for finer-grained "decision control." JSON is only processed on exit 0; if you exit 2, any JSON is ignored.

This note documents the shared contract — the common stdin fields, exit-code semantics and the per-event exit-2 table, the HTTP status-code equivalents, and the universal + decision-control JSON fields. Per-event input schemas and the meaning of each decision field live in the event notes ([tool-loop events](cc_hook_tool_loop_events.md); session/lifecycle events are documented on the [source page](https://code.claude.com/docs/en/hooks)).

## Common input fields

Hook events receive these fields as JSON (on stdin for command hooks, as the POST body for HTTP hooks), in addition to the event-specific fields each event documents:

- `session_id` — current session identifier.
- `transcript_path` — path to the conversation JSON.
- `cwd` — current working directory when the hook is invoked.
- `permission_mode` — current permission mode: `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"`, or `"bypassPermissions"`. Not all events receive this field.
- `effort` — object with a `level` field (`"low"`/`"medium"`/`"high"`/`"xhigh"`/`"max"`) holding the active effort level for the turn; the downgraded level if the requested model effort exceeds support; also exposed as the `$CLAUDE_EFFORT` environment variable. Present for events in a tool-use context (`PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`) when the model supports the effort parameter.
- `hook_event_name` — name of the event that fired.

When running with `--agent` or inside a subagent, two more fields appear: `agent_id` (unique subagent identifier, present only when the hook fires inside a subagent call) and `agent_type` (the agent name, e.g. `"Explore"` or `"security-reviewer"`; for custom subagents this is the frontmatter `name`, not the filename). Only `SessionStart` hooks can receive a `model` field, and it is not guaranteed present; there is no `$CLAUDE_MODEL` environment variable.

A `PreToolUse` hook for a Bash command receives this on stdin (`tool_name`/`tool_input` are event-specific):

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

Note: as of v2.1.139, on macOS and Linux command hooks run in their own session without a controlling terminal — the hook and its children cannot open `/dev/tty` or send escape sequences directly. To surface a message to the user, return `systemMessage`; to trigger a notification, set a title, or ring the bell, return `terminalSequence` (below).

## Exit code output

For command hooks, the exit code tells Claude Code whether the action proceeds, is blocked, or is ignored:

- **Exit 0 — success.** Claude Code parses stdout for JSON output fields (JSON is only processed on exit 0). For most events stdout goes to the debug log but is not shown in the transcript; the exceptions are `UserPromptSubmit`, `UserPromptExpansion`, and `SessionStart`, where stdout is added as context Claude can see and act on.
- **Exit 2 — blocking error.** Claude Code ignores stdout (and any JSON in it); instead stderr text is fed back to Claude as an error message. The effect depends on the event (see table below).
- **Any other exit code — non-blocking error** (for most events). The transcript shows a `<hook name> hook error` notice followed by the first line of stderr; execution continues and the full stderr is written to the debug log.

A blocking command hook prints to stderr and exits 2:

```bash theme={null}
#!/bin/bash
# Reads JSON input from stdin, checks the command
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Blocking error: tool call is prevented
fi

exit 0  # No decision: the normal permission flow applies
```

Critically, for most events **only exit code 2 blocks** the action — Claude Code treats exit code 1 as a non-blocking error and proceeds, even though 1 is the conventional Unix failure code. To enforce a policy, use `exit 2`. The one exception is `WorktreeCreate`, where any non-zero exit code aborts worktree creation.

### Exit code 2 behavior per event

Exit 2 means "stop, don't do this," but the effect varies because some events represent blockable actions (a tool call not yet run) and others represent things already done. Blockable events: `PreToolUse` (blocks the tool call), `PermissionRequest` (denies the permission), `UserPromptSubmit` (blocks processing and erases the prompt), `UserPromptExpansion` (blocks the expansion), `Stop` (prevents Claude stopping, continues the conversation), `SubagentStop` (prevents the subagent stopping), `TeammateIdle` (teammate keeps working), `TaskCreated` (rolls back creation), `TaskCompleted` (prevents marking complete), `ConfigChange` (blocks the change except `policy_settings`), `PostToolBatch` (stops the agentic loop before the next model call), `PreCompact` (blocks compaction), `Elicitation` (denies it), `ElicitationResult` (action becomes decline), and `WorktreeCreate` (any non-zero exit fails creation). Non-blocking events only surface stderr (to Claude for `PostToolUse`/`PostToolUseFailure`; to the user only for `Notification`/`SubagentStart`/`SessionStart`/`Setup`/`SessionEnd`/`CwdChanged`/`FileChanged`/`PostCompact`); `PermissionDenied`, `StopFailure`, `InstructionsLoaded`, `WorktreeRemove`, and `MessageDisplay` ignore the exit code entirely. The full per-event table is on the [source page](https://code.claude.com/docs/en/hooks).

## HTTP response handling

HTTP hooks use HTTP status codes and response bodies instead of exit codes and stdout: **2xx empty body** = success (≈ exit 0, no output); **2xx plain-text body** = success, text added as context; **2xx JSON body** = success, parsed with the same JSON output schema as command hooks; **non-2xx status** = non-blocking error, execution continues; **connection failure or timeout** = non-blocking error, execution continues. Unlike command hooks, an HTTP hook cannot signal a blocking error through status codes alone — to block a tool call or deny a permission it must return a 2xx response whose JSON body carries `decision: "block"` or a `hookSpecificOutput` with `permissionDecision: "deny"`.

## JSON output

Exit codes only block or stay silent; JSON output gives finer control. Instead of exiting 2, exit 0 and print a single JSON object to stdout — and only that object (shell-profile startup text can break parsing). All hook output strings (`additionalContext`, `systemMessage`, plain stdout) are capped at 10,000 characters; overflow is saved to a file and replaced with a preview and file path. The JSON object supports three kinds of fields: **universal fields** (work across all events), top-level **`decision`/`reason`** (used by some events to block or give feedback), and **`hookSpecificOutput`** (a nested object for richer per-event control, requiring a `hookEventName` field set to the event name).

Universal fields: `continue` (default `true`; if `false`, Claude stops processing entirely after the hook runs, taking precedence over any event-specific decision); `stopReason` (message shown to the user when `continue` is `false`, not shown to Claude); `suppressOutput` (default `false`; hides stdout from the transcript but not the debug log); `systemMessage` (a warning message shown to the user); and `terminalSequence` (a terminal escape sequence Claude Code emits on your behalf — a desktop notification, window title, or bell). To stop Claude entirely regardless of event type:

```json theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

### Emit terminal notifications

Because hooks run without a controlling terminal, writing escape sequences directly to `/dev/tty` fails. Return the sequence in `terminalSequence` instead and Claude Code emits it through its own write path — race-free, working inside tmux/GNU screen and on Windows. The field is restricted to an allowlist: OSC `0`/`1`/`2` (window/icon titles), OSC `9` (iTerm2/ConEmu/Windows Terminal/WezTerm notifications, including `9;4` taskbar progress), OSC `99` (Kitty), OSC `777` (urxvt/Ghostty/Warp), and bare BEL; anything else (CSI cursor/color, OSC palette, OSC 8 hyperlinks, OSC 52 clipboard, OSC 1337) is rejected and the field ignored. `terminalSequence` requires Claude Code v2.1.141 or later. A `Notification` hook firing a desktop notification (octal `printf` keeps control bytes off the command line; `jq -n --arg` escapes the message):

```bash theme={null}
#!/bin/bash
# Notification hook: ping the desktop when Claude Code needs attention.
input=$(cat)
title="Claude Code"
body=$(jq -r '.message // "Needs your attention"' <<<"$input")
seq=$(printf '\033]777;notify;%s;%s\007' "$title" "$body")
jq -nc --arg seq "$seq" '{terminalSequence: $seq}'
```

### Add context for Claude

`additionalContext` passes a string from your hook into Claude's context window — Claude Code wraps it in a system reminder and inserts it where the hook fired; Claude reads it on the next model request but it does not appear as a chat message. Return it inside `hookSpecificOutput` alongside the event name:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "This file is generated. Edit src/schema.ts and run `bun generate` instead."
  }
}
```

Where the reminder appears depends on the event: `SessionStart`/`Setup`/`SubagentStart` place it at the start of the conversation; `UserPromptSubmit`/`UserPromptExpansion` alongside the submitted prompt; `PreToolUse`/`PostToolUse`/`PostToolUseFailure`/`PostToolBatch` next to the tool result; `Stop`/`SubagentStop` at the end of the turn (the conversation continues so Claude can act on the feedback). When several hooks return `additionalContext` for one event, Claude receives all values; values over 10,000 chars are written to a session-directory file and passed as a path plus preview. Use it for environment state, conditional project rules, and external data; for instructions that never change, prefer [CLAUDE.md](https://code.claude.com/docs/en/memory) (loads without a script). Write the text as factual statements ("The deployment target is production"), not imperative system commands — out-of-band-command phrasing can trip Claude's prompt-injection defenses, causing Claude to surface the text to you instead of using it as context. Once injected, the text is saved in the transcript, so `--continue`/`--resume` replays it for past mid-session turns (timestamps and SHAs go stale); only `SessionStart` hooks re-run on resume (with `source: "resume"`).

### Decision control

Not every event supports blocking through JSON, and those that do each use a different field pattern. The patterns are: **top-level `decision`** (`decision: "block"` + `reason`) for `UserPromptSubmit`, `UserPromptExpansion`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop`, `SubagentStop`, `ConfigChange`, and `PreCompact` (to allow, omit `decision` or exit 0 with no JSON); **exit code or `continue: false`** for `TeammateIdle`/`TaskCreated`/`TaskCompleted`; **`hookSpecificOutput`** for `PreToolUse` (`permissionDecision` allow/deny/ask/defer + `permissionDecisionReason`), `PermissionRequest` (`decision.behavior` allow/deny), `PermissionDenied` (`retry: true`), `Elicitation`/`ElicitationResult` (`action` accept/decline/cancel + `content`), and `MessageDisplay` (`displayContent` replaces displayed text, display-only); a **path return** for `WorktreeCreate`; **context only** for `SessionStart`/`Setup`/`SubagentStart` (`additionalContext`, plus `SessionStart`'s `initialUserMessage`/`watchPaths`/`sessionTitle`/`reloadSkills`); and **no decision control** for `WorktreeRemove`/`Notification`/`SessionEnd`/`PostCompact`/`InstructionsLoaded`/`StopFailure`/`CwdChanged`/`FileChanged`. A few events can also rewrite content: `PreToolUse` (`updatedInput` under `hookSpecificOutput` replaces a tool's arguments before it runs), `PermissionRequest` (`updatedInput` inside `decision`), and `PostToolUse` (`updatedToolOutput` replaces the result); `UserPromptSubmit` cannot replace the prompt, only inject `additionalContext`. For redaction/transformation, intercept at `PreToolUse` for outbound tool inputs and `PostToolUse` for inbound results. The simplest pattern — top-level decision — looks like:

```json theme={null}
{
  "decision": "block",
  "reason": "Test suite must pass before proceeding"
}
```

Per-field meaning for each tool-loop event is documented in [tool-loop events](cc_hook_tool_loop_events.md); session/lifecycle events and the full decision-control table are on the [source page](https://code.claude.com/docs/en/hooks).

**Source**: https://code.claude.com/docs/en/hooks
**Last Updated**: 2026-06-13
**Status**: Active
