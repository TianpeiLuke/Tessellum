---
tags:
  - resource
  - documentation
  - claude_code
  - hooks
  - session_lifecycle
keywords:
  - sessionstart hook
  - userpromptsubmit hook
  - stop hook decision control
  - claude_env_file
  - reloadskills sessiontitle
  - precompact postcompact
  - subagentstart subagentstop
  - elicitation elicitationresult
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

# Claude Code Hooks — Session and Lifecycle Events

## Overview

Of the 30 hook events Claude Code fires, six fire on every tool call inside the agentic loop (documented in [`cc_hook_tool_loop_events`](cc_hook_tool_loop_events.md)). The remaining **24 events** documented here fire at the session, turn, instruction-load, compaction, subagent, agent-team, worktree, and MCP-elicitation seams of a session. Grouped by cadence they are: **once per session** — `SessionStart`, `Setup`, `SessionEnd`; **per turn** — `UserPromptSubmit`, `UserPromptExpansion`, `Stop`, `StopFailure`; **display / notification** — `MessageDisplay`, `Notification`; **subagent + agent team** — `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `TeammateIdle`; **async / standalone** — `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`; **compaction** — `PreCompact`, `PostCompact`; and **MCP elicitation** — `Elicitation`, `ElicitationResult`.

Each event adds its own fields to the [common stdin fields](cc_hook_io_and_exit_codes.md) and offers a different level of control: some can block (`UserPromptSubmit`, `Stop`, `ConfigChange`, `PreCompact`, `TaskCreated`, `TaskCompleted`, `TeammateIdle`, `Elicitation`, `ElicitationResult`, `WorktreeCreate`), some only add context, and many are observe-only. This note summarizes when each fires and its decision control; full per-event input schemas live on the [source page](https://code.claude.com/docs/en/hooks). The navigational index of all 30 events is [`cc_hook_events_catalog`](cc_hook_events_catalog.md).

## Session-scope events

### SessionStart

Runs when Claude Code starts or resumes a session — for loading dev context or setting environment variables. It runs on every session, so keep hooks fast; only `command` and `mcp_tool` types are supported. The matcher filters on how the session started: `startup` (new), `resume` (`--resume`/`--continue`/`/resume`), `clear` (`/clear`), or `compact` (after compaction). Input adds `source` plus optional `model`, `agent_type`, and `session_title`.

Plain stdout is added as context, so a context-only hook can print directly. The JSON form adds event-specific fields beyond the universal ones:

| Field | Description |
| :-- | :-- |
| `additionalContext` | String added to Claude's context before the first prompt |
| `initialUserMessage` | Used as the first user message in `-p` (non-interactive) mode — creates a turn rather than attaching to one |
| `sessionTitle` | Sets the session title (same effect as `/rename`); applies only on `"startup"`/`"resume"` |
| `watchPaths` | Absolute paths to watch for `FileChanged` events this session |
| `reloadSkills` | When `true`, re-scans skill/command directories after the hook so newly-installed skills are available the same session |

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current branch: feat/auth-refactor\nUncommitted changes: src/auth.ts, src/login.tsx\nActive issue: #4211 Migrate to OAuth2",
    "sessionTitle": "auth-refactor"
  }
}
```

#### Persist environment variables

`SessionStart` hooks (and `Setup`, `CwdChanged`, `FileChanged`) receive the `CLAUDE_ENV_FILE` environment variable: a file path where appending `export` statements persists variables into every subsequent Bash command for the session. Use append (`>>`) to preserve variables other hooks set. To capture all changes from setup commands (e.g. `nvm use`), diff the exported environment before and after with `comm -13`.

```bash
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

### Setup

Fires only on `claude --init-only`, or `--init`/`--maintenance` in print mode (`-p`) — not on normal startup. Use it for one-time dependency installation or scheduled cleanup triggered from CI or scripts; for per-session init use `SessionStart`. The matcher filters on the triggering flag: `init` or `maintenance`. `--init-only` runs Setup plus `startup`-matcher `SessionStart` hooks then exits. Setup cannot block (exit 2 shows stderr to the user; otherwise stderr appears only with `--verbose`); pass context via `additionalContext` JSON. Setup hooks also have `CLAUDE_ENV_FILE`; only `command` and `mcp_tool` types are supported.

### SessionEnd

Runs when a session ends — for cleanup, logging stats, or saving state. Supports matchers filtering on the exit `reason`: `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, or `other`. It has no decision control (cannot block termination). The default timeout is 1.5 seconds (applies to exit, `/clear`, interactive `/resume`); the budget rises to the highest per-hook `timeout` in settings files, up to 60 seconds, or is overridden via `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`.

## Per-turn events

### UserPromptSubmit

Runs when the user submits a prompt, before Claude processes it — to add context, validate, or block prompts. Its default `command`/`http`/`mcp_tool` timeout is 30 seconds (vs the 600s default elsewhere) because it blocks model processing until it completes. Context can be added two ways on exit 0: plain non-JSON stdout (shown as hook output in the transcript) or the `additionalContext` JSON field (added more discretely). To block, return `decision: "block"`, which prevents processing and erases the prompt from context; `reason` is shown to the user, and `suppressOriginalPrompt: true` omits the original prompt from the block message. The hook can also set `sessionTitle`.

```json
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here",
    "sessionTitle": "My session title"
  }
}
```

### UserPromptExpansion

Runs when a user-typed slash command expands into a prompt before reaching Claude — to block specific commands, inject skill context, or log invocations. It covers the path `PreToolUse` misses: typing `/skillname` directly bypasses a `PreToolUse` `Skill`-tool hook, but `UserPromptExpansion` fires on it. Matches on `command_name` (empty matcher fires on every prompt-type slash command). Input adds `expansion_type` (`slash_command` for skill/custom commands, `mcp_prompt` for MCP-server prompts), `command_name`, `command_args`, `command_source`, and the original `prompt`. Decision control mirrors `UserPromptSubmit`: `decision: "block"` blocks the expansion, with `reason` and `additionalContext`.

### Stop

Runs when the main agent finishes responding (not on user interrupt; API errors fire `StopFailure` instead). Input adds `stop_hook_active` (`true` while already continuing from a stop hook — check it to avoid an unresolvable block; Claude Code caps continuations at 8 consecutive blocks), `last_assistant_message`, and the `background_tasks` / `session_crons` arrays (v2.1.145+) that distinguish "session done" from "paused waiting for background work". Decision control: `decision: "block"` (with required `reason`) prevents Claude from stopping and continues the conversation; alternatively `hookSpecificOutput.additionalContext` gives non-error feedback that continues the turn under the same loop protections but is labeled `Stop hook feedback` rather than a hook error.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "Please run the test suite before finishing"
  }
}
```

The `/goal` command is a built-in shortcut for a session-scoped prompt-based Stop hook.

### StopFailure

Runs instead of `Stop` when the turn ends due to an API error; output and exit code are ignored. The matcher filters on the `error` type: `rate_limit`, `overloaded`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, or `unknown`. Input adds `error`, optional `error_details`, and `last_assistant_message` (here the rendered API error string, not Claude's output). No decision control — for logging, alerts, or recovery only.

## Display and notification events

### MessageDisplay

Runs while an assistant message streams to screen, once per batch of newly-completed lines (a long message produces several calls). Use it to strip markdown, transform Agent SDK display text, or redact secrets. It is **display-only**: the replacement changes only what renders — the transcript and what Claude sees keep the original, and verbose mode shows the original. No matcher; fires for every text-bearing assistant message (tool-call-only responses do not trigger it). Default timeout is 10 seconds; on failure or timeout the original text is shown. Input adds `turn_id`, `message_id`, `index`, `final` (`true` on the last batch — the end-of-message signal), and `delta` (the new lines). Output: `displayContent` replaces the delta on screen (omit it to display the original). In non-interactive runs (Agent SDK, `claude -p`) it runs once per message with the full text. No decision control.

### Notification

Runs when Claude Code sends a notification — intended for side effects like forwarding to an external service; cannot block or modify notifications. Matches on notification type: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, or `elicitation_response` (empty matcher runs for all). Input adds `message`, optional `title`, and `notification_type`. Common JSON output fields such as `systemMessage` apply.

## Subagent and agent-team events

### SubagentStart / SubagentStop

`SubagentStart` runs when a subagent is spawned via the Agent tool; matchers filter by agent type name (built-ins `general-purpose`/`Explore`/`Plan`, or a custom subagent's frontmatter `name`). It cannot block creation but can inject `additionalContext` into the subagent's starting context. `SubagentStop` runs when a subagent finishes; input adds `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` (the subagent's own nested transcript), `last_assistant_message`, and the `background_tasks`/`session_crons` arrays (scoped to the parent session). It uses the same decision control as `Stop` — `decision: "block"` with a `reason` keeps the subagent running and delivers the reason as its next instruction. To inject context into the *parent* after a subagent returns, use a `PostToolUse` hook on the `Agent` tool instead. (For subagent-defined hooks, `Stop` auto-converts to `SubagentStop` — see [`cc_hook_handler_types`](cc_hook_handler_types.md).)

### TaskCreated / TaskCompleted

`TaskCreated` runs when a task is being created via the `TaskCreate` tool (to enforce naming conventions or required descriptions); `TaskCompleted` runs when a task is marked complete via `TaskUpdate`, or when an [agent-team](https://code.claude.com/docs/en/agent-teams) teammate finishes its turn with in-progress tasks (to enforce passing tests/lint before close). Neither supports matchers. Both share input fields `task_id`, `task_subject`, and optional `task_description`, `teammate_name`, `team_name`. Both control behavior two ways: **exit code 2** prevents the action (task not created / not completed) and feeds stderr back to the model as feedback; **JSON `{"continue": false, "stopReason": "..."}`** stops the teammate entirely, matching `Stop` behavior, with `stopReason` shown to the user.

### TeammateIdle

Runs when an agent-team teammate is about to go idle after finishing its turn — to enforce quality gates (passing lint, output files exist) before it stops. No matcher. Input adds `teammate_name` and `team_name`. Control mirrors the task events: **exit code 2** delivers stderr as feedback and the teammate keeps working; **`{"continue": false, "stopReason": "..."}`** stops it entirely.

## Async and standalone events

### InstructionsLoaded

Fires when a `CLAUDE.md` or `.claude/rules/*.md` file is loaded into context — at session start for eager files, and again on lazy loads (subdirectory nested `CLAUDE.md`, or conditional rules with matching `paths:` frontmatter). It runs asynchronously for observability; no blocking or decision control. The matcher runs against `load_reason`. Input adds `file_path`, `memory_type` (`User`/`Project`/`Local`/`Managed`), `load_reason` (`session_start`, `nested_traversal`, `path_glob_match`, `include`, or `compact` — the last fires when instruction files reload after compaction), and the optional `globs`, `trigger_file_path`, `parent_file_path`. Use it for audit logging or compliance tracking.

### ConfigChange

Runs when a configuration file changes during a session — to audit changes or block unauthorized modifications. The matcher filters on source: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, or `skills`. Input adds `source` and optional `file_path`. Decision control: exit 2 or `decision: "block"` (with `reason`) prevents the change from being applied to the running session — **except** `policy_settings`, which always take effect (hooks still fire for audit, but any blocking decision is ignored).

### CwdChanged

Runs when the working directory changes (e.g. Claude runs `cd`) — to reload environment, activate toolchains, or run setup; pairs with `FileChanged` for tools like direnv. No matcher; fires on every change. Has `CLAUDE_ENV_FILE`. Input adds `old_cwd` and `new_cwd`. Output: `watchPaths` (absolute paths) dynamically replaces the `FileChanged` watch list (returning an empty array clears it, typical on entering a new directory). No decision control.

### FileChanged

Runs when a watched file changes on disk. Its `matcher` serves two roles: it **builds the watch list** (split on `|`, each segment a literal filename in the working directory — regex is not useful since `^\.env` would watch a file literally named `^\.env`), and it **filters which hooks run** against the changed file's basename. Has `CLAUDE_ENV_FILE`. Input adds `file_path` and `event` (`change`, `add`, or `unlink`). Output: `watchPaths` dynamically updates the watch list. No decision control.

### WorktreeCreate / WorktreeRemove

`WorktreeCreate` fires when `claude --worktree` or a subagent's `isolation: "worktree"` creates an isolated working copy; configuring a hook **replaces** the default `git worktree` behavior (so `.worktreeinclude` is not processed — copy local config files inside the hook), letting you use SVN, Perforce, or Mercurial. It does not use the allow/block model: the hook must **return the absolute path** to the created worktree (command hooks print it on stdout; HTTP hooks return `hookSpecificOutput.worktreePath`); failure or a missing path fails creation, and uniquely **any** non-zero exit code aborts it. Input adds `name` (a slug). `WorktreeRemove` is the cleanup counterpart, firing on worktree removal; input adds `worktree_path`. It has no decision control (cannot block removal); failures are logged in debug mode only.

## Compaction events

### PreCompact / PostCompact

`PreCompact` runs before a compact operation; the matcher is `manual` (`/compact`) or `auto` (context-window-full). Exit 2 or `decision: "block"` blocks compaction — for manual, stderr is shown to the user. Blocking auto-compaction differs by timing: a proactive pre-limit compaction is skipped and the conversation continues uncompacted, but a recovery compaction (after the API already returned a context-limit error) surfaces the underlying error and the request fails. Input adds `trigger` and `custom_instructions` (the manual `/compact` argument; empty for auto). `PostCompact` runs after compaction completes — to log the summary or update external state. Same matcher values. Input adds `trigger` and `compact_summary` (the generated summary). No decision control.

## MCP elicitation events

### Elicitation / ElicitationResult

`Elicitation` runs when an MCP server requests user input mid-task; by default Claude Code shows an interactive dialog, but a hook can respond programmatically and skip it. The matcher matches the MCP server name. Input adds `mcp_server_name`, `message`, and optional `mode` (`form` or `url`), `url`, `elicitation_id`, and `requested_schema`. To respond, return `hookSpecificOutput` with `action` (`accept`/`decline`/`cancel`) and, for accept, a `content` object of form-field values; exit 2 denies the elicitation.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

`ElicitationResult` runs after a user responds to an elicitation, before the response is sent back to the server — to observe, modify, or block it. Same matcher. Input adds `mcp_server_name`, `action`, and optional `mode`, `elicitation_id`, `content`. Output overrides via `action` and `content`; exit 2 blocks the response, changing the effective action to `decline`.

## Related Notes

- [Claude Code](../../term_dictionary/term_claude_code.md) — these events span Claude Code's session, turn, instruction-load, and config lifecycle; relevance: the note documents that product behavior.
- [Agent Harness](../../term_dictionary/term_agent_harness.md) — SessionStart/Setup/Stop/SessionEnd and the `CLAUDE_ENV_FILE`/`reloadSkills`/`watchPaths` outputs configure the harness's environment, skill discovery, and watch list; relevance: they are the harness's lifecycle callback sites around the loop.
- [Compaction](../../term_dictionary/term_compaction.md) — `PreCompact`/`PostCompact` fire around context compaction (`manual`/`auto` matchers), and `InstructionsLoaded` re-fires with `load_reason:"compact"`; relevance: the compaction concept defines these events' triggers.
- [Subagent](../../term_dictionary/term_subagent.md) — `SubagentStart`/`SubagentStop` fire as subagents spawn and finish, and Stop-style `additionalContext` continues a subagent's turn; relevance: subagent-defined lifecycle events.
- [Multi-Agent](../../term_dictionary/term_multi_agent.md) — `TeammateIdle`, `TaskCreated`, and `TaskCompleted` are the agent-teams events where exit 2 blocks a teammate going idle or a task transitioning; relevance: the multi-agent execution model defines them.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — `SessionStart`/`UserPromptSubmit`/`UserPromptExpansion` inject `additionalContext` and `initialUserMessage` to shape what enters the model's context; relevance: context-engineering at lifecycle seams.
- [Context Window](../../term_dictionary/term_context_window.md) — `SessionStart` reloads context on resume, the compaction events bracket window-shrinking, and `additionalContext` adds to the window; relevance: all context-window-management touchpoints.
- [Hook Events Catalog](cc_hook_events_catalog.md) — the navigational index of all 30 events, including the 24 session/lifecycle rows here and their cadence.
- [Hook I/O and Exit Codes](cc_hook_io_and_exit_codes.md) — the common stdin fields, the exit-code-2-per-event table, and the universal JSON output fields these decision objects extend.
- [Hook Tool-Loop Events](cc_hook_tool_loop_events.md) — the complementary six per-tool-call events for the other catalog entries.

**Source**: https://code.claude.com/docs/en/hooks
**Last Updated**: 2026-06-13
**Status**: Active
