---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - sessions
keywords:
  - claude agent sdk sessions
  - claudesdkclient
  - continue true
  - resume session id
  - fork_session
  - capture session_id
  - list_sessions
  - get_session_messages
  - query session options
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/sessions
access_control_group: ["general"]
---

# Claude Agent SDK — Session Management API

## Overview

This note is the how-to for controlling SDK sessions through the `query()` option fields and the automatic-tracking interfaces. Session management comes into play when you send multiple prompts that should share context; within a single `query()` call the agent already takes as many turns as it needs (permission prompts and `AskUserQuestion` are handled in-loop and don't end the call). The conceptual model — what a session is and how continue/resume/fork differ — lives in [`cc_sdk_sessions_overview`](cc_sdk_sessions_overview.md); this note shows the API calls.

Two paths exist. **Automatic** tracking (`ClaudeSDKClient` in Python, `continue: true` in TypeScript) keeps a multi-turn conversation going within one process with no ID handling. **Manual** control uses `query()`/`ClaudeAgentOptions` option fields — capture the `session_id` off the result message, then pass it to `resume` (return to a session) or `resume` + `fork_session` (branch it). Enumeration helpers list and mutate sessions on disk.

## Automatic session management

Both SDKs offer an interface that tracks session state for you across calls, so you don't pass IDs around manually. Use these for multi-turn conversations within a single process.

### Python: `ClaudeSDKClient`

`ClaudeSDKClient` handles session IDs internally. Each call to `client.query()` automatically continues the same session. Call `client.receive_response()` to iterate over the messages for the current query. Use the client as an async context manager (`async with ClaudeSDKClient(options=options) as client:`) so connection setup and teardown are handled for you, or call `connect()` and `disconnect()` manually. Within one `async with` block, a first `client.query("Analyze the auth module")` captures the session ID internally, and a second `client.query("Now refactor it to use JWT")` automatically continues the same session — the second query has full context from the first without any explicit `resume` or session ID.

### TypeScript: `continue: true`

The TypeScript SDK doesn't have a session-holding client object like Python's `ClaudeSDKClient`. Instead, pass `continue: true` on each subsequent `query()` call and the SDK picks up the most recent session in the current directory — no ID tracking required. A first `query()` creates a fresh session; a second `query()` with `options: { continue: true, ... }` tells the SDK to find and resume the most recent session on disk, so the agent has full context from the first call.

> The experimental V2 session API, which provided `createSession()` with a `send` / `stream` pattern, was removed in TypeScript Agent SDK 0.3.142. Use the `query()` function and the session options described here instead.

## Use session options with `query()`

`continue`, `resume`, and `fork_session` are option fields you set on `query()` (`ClaudeAgentOptions` in Python, `Options` in TypeScript).

### Capture the session ID

Resume and fork require a session ID. Read it from the `session_id` field on the result message (`ResultMessage` in Python, `SDKResultMessage` in TypeScript), which is present on every result regardless of success or error. In TypeScript the ID is also available earlier as a direct field on the init `SystemMessage`; in Python it's nested inside `SystemMessage.data`.

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    session_id = None

    async for message in query(
        prompt="Analyze the auth module and suggest improvements",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep"],
        ),
    ):
        if isinstance(message, ResultMessage):
            session_id = message.session_id
            if message.subtype == "success":
                print(message.result)

    print(f"Session ID: {session_id}")
    return session_id


session_id = asyncio.run(main())
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

let sessionId: string | undefined;

for await (const message of query({
  prompt: "Analyze the auth module and suggest improvements",
  options: { allowedTools: ["Read", "Glob", "Grep"] }
})) {
  if (message.type === "result") {
    sessionId = message.session_id;
    if (message.subtype === "success") {
      console.log(message.result);
    }
  }
}

console.log(`Session ID: ${sessionId}`);
```

### Resume by ID

Pass a session ID to `resume` to return to that specific session. The agent picks up with full context from wherever the session left off. Common reasons to resume:

* **Follow up on a completed task.** The agent already analyzed something; now you want it to act on that analysis without re-reading files.
* **Recover from a limit.** The first run ended with `error_max_turns` or `error_max_budget_usd`; resume with a higher limit.
* **Restart your process.** You captured the ID before shutdown and want to restore the conversation.

```python Python theme={null}
# Earlier session analyzed the code; now build on that analysis
async for message in query(
    prompt="Now implement the refactoring you suggested",
    options=ClaudeAgentOptions(
        resume=session_id,
        allowed_tools=["Read", "Edit", "Write", "Glob", "Grep"],
    ),
):
    if isinstance(message, ResultMessage) and message.subtype == "success":
        print(message.result)
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const sessionId = "..."; // The ID you captured in the previous example

// Earlier session analyzed the code; now build on that analysis
for await (const message of query({
  prompt: "Now implement the refactoring you suggested",
  options: {
    resume: sessionId,
    allowedTools: ["Read", "Edit", "Write", "Glob", "Grep"]
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

A response that builds on the earlier analysis (instead of starting fresh) confirms the agent resumed the session with its prior context intact. If a `resume` call returns a fresh session instead of the expected history, the most common cause is a mismatched `cwd` (see the encoded-cwd path discussion in [`cc_sdk_sessions_overview`](cc_sdk_sessions_overview.md)).

### Fork to explore alternatives

Forking creates a new session that starts with a copy of the original's history but diverges from that point. The fork gets its own session ID; the original's ID and history stay unchanged. You end up with two independent sessions you can resume separately. Set both `resume=session_id` and `fork_session=True` (Python) / `forkSession: true` (TypeScript). The example below forks `session_id` to explore OAuth2 while leaving the JWT-focused thread intact, then resumes the original to continue down the JWT path:

```python Python theme={null}
# Fork: branch from session_id into a new session
forked_id = None
async for message in query(
    prompt="Instead of JWT, outline how OAuth2 would work for the auth module",
    options=ClaudeAgentOptions(
        resume=session_id,
        fork_session=True,
        max_turns=5,
    ),
):
    if isinstance(message, ResultMessage):
        forked_id = message.session_id  # The fork's ID, distinct from session_id
        if message.subtype == "success":
            print(message.result)

print(f"Forked session: {forked_id}")

# Original session is untouched; resuming it continues the JWT thread
async for message in query(
    prompt="Continue with the JWT approach",
    options=ClaudeAgentOptions(resume=session_id),
):
    if isinstance(message, ResultMessage) and message.subtype == "success":
        print(message.result)
```

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

const sessionId = "..."; // The ID you captured in the previous example

// Fork: branch from sessionId into a new session
let forkedId: string | undefined;

for await (const message of query({
  prompt: "Instead of JWT, outline how OAuth2 would work for the auth module",
  options: {
    resume: sessionId,
    forkSession: true,
    maxTurns: 5
  }
})) {
  if (message.type === "system" && message.subtype === "init") {
    forkedId = message.session_id; // The fork's ID, distinct from sessionId
  }
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}

console.log(`Forked session: ${forkedId}`);

// Original session is untouched; resuming it continues the JWT thread
for await (const message of query({
  prompt: "Continue with the JWT approach",
  options: { resume: sessionId }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

`forkedId` differs from the original session ID, and resuming the original session still continues the JWT thread — confirming the fork did not modify the original history. In TypeScript the fork's ID is read from the init `SystemMessage` (`message.type === "system" && message.subtype === "init"`) rather than the result message.

## Enumerate and mutate sessions

Both SDKs expose functions for enumerating sessions on disk and reading their messages: `listSessions()` and `getSessionMessages()` in TypeScript, `list_sessions()` and `get_session_messages()` in Python. Use them to build custom session pickers, cleanup logic, or transcript viewers.

Both SDKs also expose functions for looking up and mutating individual sessions: `get_session_info()`, `rename_session()`, and `tag_session()` in Python, and `getSessionInfo()`, `renameSession()`, and `tagSession()` in TypeScript. Use them to organize sessions by tag or give them human-readable titles. For the full option reference, see the Python `ClaudeAgentOptions` and TypeScript `Options` docs linked from the source page.

**Source**: https://code.claude.com/docs/en/agent-sdk/sessions
**Last Updated**: 2026-06-13
**Status**: Active
