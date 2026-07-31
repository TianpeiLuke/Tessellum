---
tags:
  - resource
  - documentation
  - claude_code
  - headless
  - automation
keywords:
  - claude -p examples
  - headless cli patterns
  - pipe stdin through claude
  - output-format json json-schema
  - stream-json events
  - allowedTools auto-approve
  - append-system-prompt
  - continue resume conversations
topics:
  - Claude Code
  - Automation & Scheduling
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/headless
access_control_group: ["general"]
---

# Claude Code — Headless Examples & CLI Patterns

## Overview

This note collects the common `claude -p` (non-interactive) CLI patterns from the headless docs: piping data through Claude, wrapping Claude in a build script, getting structured output, streaming responses, auto-approving tools, creating a commit, customizing the system prompt, and continuing conversations. These are reusable invocation recipes for scripts and CI. The `-p` (or `--print`) flag runs any `claude` command non-interactively, and all [CLI flags](https://code.claude.com/docs/en/cli-reference) work with it.

For CI and other scripted calls, add `--bare` so the run does not pick up whatever happens to be configured locally — see the Bare-mode operating model section below for what it skips.

## Bare-Mode Operating Model

`--bare` reduces startup time by skipping auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and `CLAUDE.md`. Without it, `claude -p` loads the same context an interactive session would, including anything configured in the working directory or `~/.claude`. Bare mode is useful for CI and scripts where you need the same result on every machine — a hook in a teammate's `~/.claude` or an MCP server in the project's `.mcp.json` won't run, because bare mode never reads them, so only flags you pass explicitly take effect (for example `claude --bare -p "Summarize this file" --allowedTools "Read"`). In bare mode Claude has access to the Bash, file read, and file edit tools; to load anything else, pass it with a flag — `--append-system-prompt`/`--append-system-prompt-file` for system prompt additions, `--settings <file-or-json>`, `--mcp-config <file-or-json>` for MCP servers, `--agents <json>` for custom agents, and `--plugin-dir <path>`/`--plugin-url <url>` for a plugin. Bare mode skips OAuth and keychain reads, so Anthropic authentication must come from `ANTHROPIC_API_KEY` or an `apiKeyHelper` in the JSON passed to `--settings` (Bedrock, Vertex, and Foundry use their usual provider credentials). Anthropic recommends `--bare` for scripted and SDK calls, and it will become the default for `-p` in a future release.

If Claude starts a background Bash task during a `claude -p` run (for example a dev server or a watch build), that task is terminated about five seconds after Claude has returned its final result and stdin has closed; the grace period lets a task that finishes right after the result still deliver its output. Before v2.1.163, a never-exiting background process would hold the `claude -p` invocation open indefinitely.

## Pipe Data Through Claude

Non-interactive mode reads stdin, so you can pipe data in and redirect the response out like any other command-line tool. This example pipes a build log into Claude and writes the explanation to a file:

```bash
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

With `--output-format json`, the response payload includes `total_cost_usd` and a per-model cost breakdown, so scripted callers can track spend per invocation without consulting the usage dashboard. As of Claude Code v2.1.128, piped stdin is capped at 10MB; if you exceed the cap, Claude Code exits with a clear error and a non-zero status. To work with larger inputs, write the content to a file and reference the file path in your prompt instead of piping it.

## Add Claude to a Build Script

You can wrap a non-interactive call in a script to use Claude as a project-specific linter or reviewer. This `package.json` script pipes the diff against `main` into Claude and asks it to report typos. Piping the diff means Claude doesn't need Bash permission to read it, and the escaped double quotes keep the script portable to Windows:

```json
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

## Get Structured Output

Use `--output-format` to control how responses are returned:

- `text` (default): plain text output
- `json`: structured JSON with result, session ID, and metadata
- `stream-json`: newline-delimited JSON for real-time streaming

The plain JSON form (`claude -p "Summarize this project" --output-format json`) returns the text result in the `result` field with session metadata. To get output conforming to a specific schema, combine `--output-format json` with `--json-schema` and a JSON Schema definition; the response includes request metadata (session ID, usage, etc.) with the structured output in the `structured_output` field. This example extracts function names and returns them as an array of strings:

```bash
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

Use a tool like `jq` to parse the response and extract specific fields — for example `... --output-format json | jq -r '.result'` for the text result, or `| jq '.structured_output'` for the schema-constrained output.

## Stream Responses

Use `--output-format stream-json` with `--verbose` and `--include-partial-messages` to receive tokens as they're generated; each line is a JSON object representing an event (`claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages`). To display just the streaming text, pipe through `jq` filtering for text deltas — `-r` outputs raw strings (no quotes) and `-j` joins without newlines so tokens stream continuously:

```bash
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Three system events are worth handling in scripts. When an API request fails with a retryable error, Claude Code emits a `system/api_retry` event before retrying (fields include `attempt`, `max_retries`, `retry_delay_ms`, `error_status`, and an `error` category such as `rate_limit`, `overloaded`, or `server_error`) — use it to surface retry progress or implement custom backoff. The `system/init` event reports session metadata (model, tools, MCP servers, loaded plugins) and is the first event in the stream unless `CLAUDE_CODE_SYNC_PLUGIN_INSTALL` is set; its `plugins` and `plugin_errors` fields let you fail CI when a plugin did not load. When that env var is set, `system/plugin_install` events (with a `status` of `started`, `installed`, `failed`, or `completed`) precede `init` while marketplace plugins install, so you can surface install progress in your own UI.

## Auto-Approve Tools

Use `--allowedTools` to let Claude use certain tools without prompting — for example `claude -p "Run the test suite and fix any failures" --allowedTools "Bash,Read,Edit"` runs a test suite and fixes failures, allowing Bash, file read, and file edit without asking for permission. To set a baseline for the whole session instead of listing individual tools, pass a permission mode (`claude -p "Apply the lint fixes" --permission-mode acceptEdits`). `dontAsk` denies anything not in your `permissions.allow` rules or the read-only command set, which is useful for locked-down CI runs. `acceptEdits` lets Claude write files without prompting and auto-approves common filesystem commands such as `mkdir`, `touch`, `mv`, and `cp`; other shell commands and network requests still need an `--allowedTools` entry or a `permissions.allow` rule, otherwise the run aborts when one is attempted.

## Create a Commit

This example reviews staged changes and creates a commit with an appropriate message:

```bash
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

The `--allowedTools` flag uses permission rule syntax. The trailing ` *` enables prefix matching, so `Bash(git diff *)` allows any command starting with `git diff`. The space before `*` is important: without it, `Bash(git diff*)` would also match `git diff-index`. Note that user-invoked skills and custom commands work in `-p` mode (include `/skill-name` in the prompt string and Claude Code expands it before running), but built-in commands that open an interactive dialog, such as `/config` and `/login`, are not available in `-p` mode.

## Customize the System Prompt

Use `--append-system-prompt` to add instructions while keeping Claude Code's default behavior. This example pipes a PR diff to Claude and instructs it to review for security vulnerabilities: `gh pr diff "$1" | claude -p --append-system-prompt "You are a security engineer. Review for vulnerabilities." --output-format json`. See the system prompt flags reference for more options, including `--system-prompt` to fully replace the default prompt.

## Continue Conversations

Use `--continue` to continue the most recent conversation, or `--resume` with a session ID to continue a specific conversation. A first request (`claude -p "Review this codebase for performance issues"`) can be followed by chained prompts that add `--continue` (e.g. `claude -p "Now focus on the database queries" --continue`). If you're running multiple conversations, capture the session ID to resume a specific one:

```bash
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

Run both commands from the same directory: session ID lookup is scoped to the current project directory and its git worktrees.

**Source**: https://code.claude.com/docs/en/headless
**Last Updated**: 2026-06-13
**Status**: Active
