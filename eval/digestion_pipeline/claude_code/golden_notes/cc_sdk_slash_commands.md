---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - slash_commands
keywords:
  - slash commands sdk
  - dispatch slash command prompt string
  - slash_commands system init
  - compact command sdk
  - clear command sdk
  - custom slash command markdown
  - argument placeholders $0 $1 $arguments
  - command namespacing
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/agent-sdk/slash-commands
access_control_group: ["general"]
---

# Slash Commands in the SDK

## Overview

Slash commands control a Claude Code session through special commands that start with `/` — compacting context, listing usage, or invoking custom commands. Through the Claude Agent SDK, you dispatch a slash command simply by including it in the **prompt string**, exactly like regular text. Only commands that work without an interactive terminal are dispatchable through the SDK; the `system/init` message lists the ones available in your session.

This note is the SDK-side dispatch procedure: discovering available commands from `system/init`, sending built-ins (`/compact`, `/clear`), and authoring custom commands as markdown files. The conceptual/CLI custom-command guide is owned by [Slash Commands](https://code.claude.com/docs/en/skills) and the B06 `cc_commands` note.

## Discovering Available Slash Commands

The SDK reports available slash commands in the **system initialization message**. Read it when the session starts — the list includes both built-ins and any custom commands found in the filesystem:

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage


async def main():
    async for message in query(prompt="Hello Claude", options=ClaudeAgentOptions(max_turns=1)):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            print("Available slash commands:", message.data["slash_commands"])
            # Example output: ["clear", "compact", "context", "usage"]


asyncio.run(main())
```

The TypeScript equivalent reads `message.slash_commands` when `message.type === "system" && message.subtype === "init"`.

## Sending Slash Commands

Send a slash command by putting it in the `prompt` field — no special API is needed:

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


async def main():
    # Send a slash command
    async for message in query(prompt="/compact", options=ClaudeAgentOptions(max_turns=1)):
        if isinstance(message, ResultMessage):
            print("Command executed:", message.result)


asyncio.run(main())
```

## Common Slash Commands

### `/compact` — Compact conversation history

`/compact` reduces conversation-history size by summarizing older messages while preserving important context. When it runs, the SDK emits a `system` message with subtype `compact_boundary` carrying `compact_metadata` (pre-compaction token count and the trigger):

```python Python theme={null}
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage


async def main():
    async for message in query(prompt="/compact", options=ClaudeAgentOptions(max_turns=1)):
        if isinstance(message, SystemMessage) and message.subtype == "compact_boundary":
            print("Compaction completed")
            print("Pre-compaction tokens:", message.data["compact_metadata"]["pre_tokens"])
            print("Trigger:", message.data["compact_metadata"]["trigger"])


asyncio.run(main())
```

### `/clear` — Reset conversation context

`/clear` resets the conversation to an empty context so subsequent prompts start with no prior history; the previous conversation remains on disk and can be returned to by passing its session ID to the [`resume` option](https://code.claude.com/docs/en/agent-sdk/sessions#resume-by-id). It is useful in [streaming input mode](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode), where multiple prompts share one connection. For one-shot `query()` calls each call already starts empty, so sending `/clear` has no practical effect — start a new `query()` instead. Per source, `/clear` in the SDK requires Claude Code v2.1.117 or later; in earlier versions it is omitted from `slash_commands`.

## Creating Custom Slash Commands

Custom commands are markdown files in designated directories, similar to how subagents are configured. The filename (without `.md`) becomes the command name, the file content defines what the command does, and optional YAML frontmatter provides configuration. Once a file exists in the filesystem, the command is automatically available through the SDK and appears in the `slash_commands` list.

> **Note (source):** `.claude/commands/` is the legacy format. The recommended format is `.claude/skills/<name>/SKILL.md`, which supports the same `/name` invocation plus autonomous invocation by Claude — see [Skills](cc_sdk_skills.md). The CLI continues to support both formats.

### File Locations

- **Project commands**: `.claude/commands/` — available only in the current project (legacy; prefer `.claude/skills/`).
- **Personal commands**: `~/.claude/commands/` — available across all your projects (legacy; prefer `~/.claude/skills/`).

### File Format and Frontmatter

A minimal command (e.g. `.claude/commands/refactor.md`) is just instruction text and creates `/refactor`. Frontmatter adds configuration — for example `.claude/commands/security-check.md`:

```markdown theme={null}
---
allowed-tools: Read, Grep, Glob
description: Run security vulnerability scan
model: claude-opus-4-7
---

Analyze the codebase for security vulnerabilities including:
- SQL injection risks
- XSS vulnerabilities
- Exposed credentials
- Insecure configurations
```

The `allowed-tools` frontmatter gates which tools the command may invoke (e.g. `Bash(git add *)`, `Read`, `Grep`); `description` and `argument-hint` document it; `model` overrides the model used.

### Advanced Features

Custom commands support dynamic content beyond static text:

- **Arguments and placeholders** — positional `$0`, `$1`, ... or `$ARGUMENTS` for the full argument string. A `fix-issue.md` body of `Fix issue #$0 with priority $1.` invoked as `/fix-issue 123 high` runs with `$0="123"` and `$1="high"`.
- **Bash command execution** — prefix a line with `!` to run a bash command and inline its output, e.g. `- Current status: !` then a backtick-wrapped `git status`. Pair with `allowed-tools: Bash(git status *), Bash(git commit *)` to authorize the calls.
- **File references** — prefix with `@` to inline a file's contents, e.g. `@package.json`, `@tsconfig.json`, `@.env`.

```markdown theme={null}
---
argument-hint: [issue-number] [priority]
description: Fix a GitHub issue
---

Fix issue #$0 with priority $1.
Check the issue description and implement the necessary changes.
```

### Organization with Namespacing

Subdirectories under `.claude/commands/` group commands: `frontend/component.md` creates `/component` shown as `(project:frontend)`, `backend/api-test.md` creates `/api-test (project:backend)`, and a top-level `review.md` creates `/review (project)`. The subdirectory appears in the command description but does **not** affect the command name itself.

### Practical Examples

The source ships ready-to-adapt patterns that combine these features: a **code-review** command using `allowed-tools: Read, Grep, Glob, Bash(git diff *)` with `!`-injected `git diff --name-only HEAD~1` / `git diff HEAD~1` and a review checklist; and a **test** command with `argument-hint: [test-pattern]` that detects the framework, runs tests matching `$ARGUMENTS`, fixes failures, and re-runs. Both are dispatched like any other command — `query(prompt="/code-review", ...)` or `query(prompt="/test auth", ...)`.

**Source**: https://code.claude.com/docs/en/agent-sdk/slash-commands
**Last Updated**: 2026-06-13
**Status**: Active
