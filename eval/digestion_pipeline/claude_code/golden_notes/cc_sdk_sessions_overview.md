---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - sessions
keywords:
  - sdk session
  - conversation history
  - continue resume fork
  - session persistence
  - encoded cwd
  - jsonl transcript
  - resume across hosts
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/sessions
access_control_group: ["general"]
---

# Claude Code Agent SDK — Sessions Overview

## Overview

A **session** is the conversation history the SDK accumulates while your agent works: your prompt, every tool call the agent made, every tool result, and every response. The SDK writes it to disk automatically so you can return to it later. Returning to a session means the agent has full context from before — files it already read, analysis it already performed, decisions it already made — so you can ask a follow-up question, recover from an interruption, or branch off to try a different approach.

Sessions persist the **conversation**, not the filesystem. To snapshot and revert file changes the agent made, use [file checkpointing](https://code.claude.com/docs/en/agent-sdk/file-checkpointing) instead. This note covers when session handling matters, how `continue` / `resume` / `fork` differ, and the on-disk layout that makes resuming across hosts possible. The `query()`/`ClaudeAgentOptions` API that applies these options is covered in [Session Management API](cc_sdk_session_management_api.md).

## Choose an Approach

How much session handling you need depends on your application's shape. Session management comes into play when you send multiple prompts that should share context. Within a single `query()` call, the agent already takes as many turns as it needs, and permission prompts and `AskUserQuestion` are handled in-loop (they don't end the call).

| What you're building | What to use |
| :--- | :--- |
| One-shot task: single prompt, no follow-up | Nothing extra. One `query()` call handles it. |
| Multi-turn chat in one process | `ClaudeSDKClient` (Python) or `continue: true` (TypeScript). The SDK tracks the session for you with no ID handling. |
| Pick up where you left off after a process restart | `continue_conversation=True` (Python) / `continue: true` (TypeScript). Resumes the most recent session in the directory, no ID needed. |
| Resume a specific past session (not the most recent) | Capture the session ID and pass it to `resume`. |
| Try an alternative approach without losing the original | Fork the session. |
| Stateless task, don't want anything written to disk (TypeScript only) | Set `persistSession: false`. The session exists only in memory for the duration of the call. Python always persists to disk. |

## Continue, Resume, and Fork

Continue, resume, and fork are option fields you set on `query()` (`ClaudeAgentOptions` in Python, `Options` in TypeScript). **Continue** and **resume** both pick up an existing session and add to it; the difference is how they find that session:

- **Continue** finds the most recent session in the current directory. You don't track anything. Works well when your app runs one conversation at a time.
- **Resume** takes a specific session ID. You track the ID. Required when you have multiple sessions (for example, one per user in a multi-user app) or want to return to one that isn't the most recent.

**Fork** is different: it creates a **new** session that starts with a copy of the original's history but diverges from that point. The fork gets its own session ID; the original's ID and history stay unchanged. You end up with two independent sessions you can resume separately. Forking branches the conversation history, not the filesystem — if a forked agent edits files, those changes are real and visible to any session working in the same directory. Use fork to try a different direction while keeping the option to go back.

## Resume Across Hosts

Session files are local to the machine that created them. Sessions are stored under `~/.claude/projects/<encoded-cwd>/*.jsonl`, or under `$CLAUDE_CONFIG_DIR/projects/<encoded-cwd>/*.jsonl` if you set the `CLAUDE_CONFIG_DIR` environment variable. Here `<encoded-cwd>` is the absolute working directory with every non-alphanumeric character replaced by `-` (so `/Users/me/proj` becomes `-Users-me-proj`). If a `resume` call returns a fresh session instead of the expected history, the most common cause is a mismatched `cwd`: if your resume call runs from a different directory, the SDK looks in the wrong place, and the session file also needs to exist on the current machine.

To resume a session on a different host (CI workers, ephemeral containers, serverless), you have two options:

- **Move the session file.** Persist `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` from the first run and restore it to the same path on the new host before calling `resume`. The `cwd` must match.
- **Don't rely on session resume.** Capture the results you need (analysis output, decisions, file diffs) as application state and pass them into a fresh session's prompt. This is often more robust than shipping transcript files around.

For multi-host or serverless deployments, mirror transcripts to shared storage with a `SessionStore` adapter (see [Session Store](cc_sdk_session_store.md)). Broader multi-host hosting and deployment patterns are covered in the [hosting guide](https://code.claude.com/docs/en/agent-sdk/hosting). Both SDKs also expose functions for enumerating sessions on disk, reading their messages, and mutating individual sessions — those helpers (`list_sessions`/`listSessions`, `get_session_messages`/`getSessionMessages`, and the rename/tag functions) are documented in [Session Management API](cc_sdk_session_management_api.md).

**Source**: https://code.claude.com/docs/en/agent-sdk/sessions
**Last Updated**: 2026-06-13
**Status**: Active
