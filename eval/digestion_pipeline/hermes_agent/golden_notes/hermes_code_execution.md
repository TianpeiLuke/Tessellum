---
tags:
  - resource
  - documentation
  - hermes_agent
  - code_execution
  - automation
keywords:
  - execute_code
  - programmatic tool calling
  - hermes_tools RPC stub
  - Unix domain socket
  - project vs strict mode
  - environment scrubbing
topics:
  - Hermes Agent
  - Code Execution
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution
access_control_group: ["general"]
---

# Code Execution (Programmatic Tool Calling)

## Overview

`execute_code` is the Hermes Agent tool that lets the agent **write a Python script that calls other Hermes tools programmatically, collapsing a multi-step workflow into a single LLM turn**. Instead of the model issuing one tool call, reading the result back into context, reasoning, and issuing the next call — repeated for every step — the agent authors one script that loops, filters, and branches over tool results locally. The script runs in a child process on the agent host and talks to Hermes over a Unix domain socket RPC. The decisive benefit is token economy: only the script's `print()` output returns to the LLM, so intermediate tool results (search hits, file contents, build logs) never enter the context window. This is the mechanical-workflow counterpart to `delegate_task` (which is for spawning reasoning-capable child agents) and a tighter, RPC-mediated sibling of the raw `terminal` tool. It runs on Linux and macOS only.

## How It Works

The execution flow is a fixed five-step handshake between the script's child process and the parent Hermes process:

1. The agent writes a Python script using `from hermes_tools import ...`
2. Hermes generates a `hermes_tools.py` stub module with RPC functions
3. Hermes opens a Unix domain socket and starts an RPC listener thread
4. The script runs in a child process — tool calls travel over the socket back to Hermes
5. Only the script's `print()` output is returned to the LLM; intermediate tool results never enter the context window

```python
# The agent can write scripts like:
from hermes_tools import web_search, web_extract

results = web_search("Python 3.13 features", limit=5)
for r in results["data"]["web"]:
    content = web_extract([r["url"]])
    # ... filter and process ...
print(summary)
```

**Available tools inside scripts:** `web_search`, `web_extract`, `read_file`, `write_file`, `search_files`, `patch`, `terminal` (foreground only).

## When the Agent Uses This

The agent reaches for `execute_code` when a task has:

- **3+ tool calls** with processing logic between them
- Bulk data filtering or conditional branching
- Loops over results

The key benefit is again token usage: intermediate tool results never enter the context window — only the final `print()` output comes back, dramatically reducing token consumption.

## Practical Examples

The source gives four worked patterns: a **data-processing pipeline** (`search_files` + `read_file` to gather config previews into JSON), **multi-step web research** (the canonical case below), **bulk file refactoring** (`search_files` + `patch` with `replace_all=True` to fix a deprecated API across many files), and a **build-and-test pipeline** (`terminal` to run `pytest`, then parse pass/fail counts). All four share the same shape: many tool calls, in-script Python logic between them, and a single `print()` of the distilled result. The web-research example is representative:

```python
from hermes_tools import web_search, web_extract
import json

# Search, extract, and summarize in one turn
results = web_search("Rust async runtime comparison 2025", limit=5)
summaries = []
for r in results["data"]["web"]:
    page = web_extract([r["url"]])
    for p in page.get("results", []):
        if p.get("content"):
            summaries.append({
                "title": r["title"],
                "url": r["url"],
                "excerpt": p["content"][:500]
            })

print(json.dumps(summaries, indent=2))
```

## Execution Mode

`execute_code` has two execution modes controlled by `code_execution.mode` in `~/.hermes/config.yaml`:

| Mode | Working directory | Python interpreter |
|------|-------------------|--------------------|
| **`project`** (default) | The session's working directory (same as `terminal()`) | Active `VIRTUAL_ENV` / `CONDA_PREFIX` python, falling back to Hermes's own python |
| `strict` | A temp staging directory isolated from the user's project | `sys.executable` (Hermes's own python) |

**Leave it on `project`** when you want `import pandas`, `from my_project import foo`, or relative paths like `open(".env")` to work the same way they do in `terminal()` — almost always what you want. **Flip to `strict`** when you need maximum reproducibility: the same interpreter every session regardless of which venv the user activated, and scripts quarantined from the project tree (no risk of accidentally reading project files through a relative path).

```yaml
# ~/.hermes/config.yaml
code_execution:
  mode: project   # or "strict"
```

Fallback behavior in `project` mode: if `VIRTUAL_ENV` / `CONDA_PREFIX` is unset, broken, or points at a Python older than 3.8, the resolver falls back cleanly to `sys.executable` — it never leaves the agent without a working interpreter. The security-critical invariants are **identical across both modes**: environment scrubbing (API keys, tokens, credentials stripped), the tool whitelist (scripts cannot call `execute_code` recursively, `delegate_task`, or MCP tools), and resource limits (timeout, stdout cap, tool-call cap). Switching mode changes where scripts run and which interpreter runs them, not what credentials they can see or which tools they can call.

## Resource Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| **Timeout** | 5 minutes (300s) | Script is killed with SIGTERM, then SIGKILL after 5s grace |
| **Stdout** | 50 KB | Output truncated with `[output truncated at 50KB]` notice |
| **Stderr** | 10 KB | Included in output on non-zero exit for debugging |
| **Tool calls** | 50 per execution | Error returned when limit reached |

All limits are configurable via `config.yaml`:

```yaml
# In ~/.hermes/config.yaml
code_execution:
  mode: project      # project (default) | strict
  timeout: 300       # Max seconds per script (default: 300)
  max_tool_calls: 50 # Max tool calls per execution (default: 50)
```

## How Tool Calls Work Inside Scripts

When a script calls a function like `web_search("query")`:

1. The call is serialized to JSON and sent over a Unix domain socket to the parent process
2. The parent dispatches through the standard `handle_function_call` handler
3. The result is sent back over the socket
4. The function returns the parsed result

This means tool calls inside scripts behave **identically to normal tool calls** — same rate limits, same error handling, same capabilities. The only restriction is that `terminal()` is foreground-only (no `background` or `pty` parameters).

## Error Handling

When a script fails, the agent receives structured error information:

- **Non-zero exit code**: stderr is included in the output so the agent sees the full traceback
- **Timeout**: Script is killed and the agent sees `"Script timed out after 300s and was killed."`
- **Interruption**: If the user sends a new message during execution, the script is terminated and the agent sees `[execution interrupted — user sent a new message]`
- **Tool call limit**: When the 50-call limit is hit, subsequent tool calls return an error message

The response always includes `status` (success/error/timeout/interrupted), `output`, `tool_calls_made`, and `duration_seconds`.

## Security

> **Security Model (danger):** The child process runs with a **minimal environment**. API keys, tokens, and credentials are stripped by default. The script accesses tools exclusively via the RPC channel — it cannot read secrets from environment variables unless explicitly allowed.

Environment variables containing `KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `CREDENTIAL`, `PASSWD`, or `AUTH` in their names are excluded. Only safe system variables (`PATH`, `HOME`, `LANG`, `SHELL`, `PYTHONPATH`, `VIRTUAL_ENV`, etc.) are passed through.

### Skill Environment Variable Passthrough

When a skill declares `required_environment_variables` in its frontmatter, those variables are **automatically passed through** to both `execute_code` and `terminal` child processes after the skill is loaded. This lets skills use their declared API keys without weakening the security posture for arbitrary code. For non-skill use cases, you can explicitly allowlist variables in `config.yaml`:

```yaml
terminal:
  env_passthrough:
    - MY_CUSTOM_KEY
    - ANOTHER_TOKEN
```

### `HERMES_*` variables in the child

The child process receives only a small, fixed set of operational `HERMES_*` variables by exact name: `HERMES_HOME`, `HERMES_PROFILE`, `HERMES_CONFIG`, and `HERMES_ENV` (plus `HERMES_RPC_DIR` / `HERMES_RPC_SOCKET` / `TZ` / `HOME`, which Hermes injects explicitly so the RPC channel works).

**Behavior change (note):** Earlier versions passed **any** variable whose name began with `HERMES_` through to the child. That broad prefix was removed for security hardening — it could leak `HERMES_*`-named configuration that doesn't match a secret substring (for example `HERMES_BASE_URL`, `HERMES_KANBAN_DB`, or a `HERMES_*_WEBHOOK` endpoint) into arbitrary sandboxed code. If an `execute_code` script — or a repo/plugin module it imports at import time — relied on a `HERMES_*` variable outside the four operational names, it will now find that variable **unset** in the child. The drop is intentional, not a bug.

To **opt a variable back in explicitly**, add the exact name to the per-machine `terminal.env_passthrough` allowlist in `config.yaml`, or declare it per-skill in `required_environment_variables`; both routes pass the variable through `execute_code` *and* `terminal` children, and neither weakens the secret-stripping guarantee (Hermes-managed provider credentials can never be re-allowed this way):

```yaml
required_environment_variables:
  - HERMES_KANBAN_DB
```

**Diagnosing it:** when the child drops one or more non-allowlisted `HERMES_*` variables, Hermes emits a one-line `debug` log naming them and pointing at the `env_passthrough` escape hatch. Run with debug logging (`hermes logs --level DEBUG`, or check `~/.hermes/logs/agent.log`) and look for `execute_code: dropped N non-allowlisted HERMES_* var(s)`.

Hermes always writes the script and the auto-generated `hermes_tools.py` RPC stub into a temp staging directory that is cleaned up after execution. In `strict` mode the script also *runs* there; in `project` mode it runs in the session's working directory (the staging directory stays on `PYTHONPATH` so imports still resolve). The child process runs in its own process group so it can be cleanly killed on timeout or interruption.

## execute_code vs terminal

| Use Case | execute_code | terminal |
|----------|-------------|----------|
| Multi-step workflows with tool calls between | ✅ | ❌ |
| Simple shell command | ❌ | ✅ |
| Filtering/processing large tool outputs | ✅ | ❌ |
| Running a build or test suite | ❌ | ✅ |
| Looping over search results | ✅ | ❌ |
| Interactive/background processes | ❌ | ✅ |
| Needs API keys in environment | ⚠️ Only via passthrough | ✅ (most pass through) |

**Rule of thumb:** Use `execute_code` when you need to call Hermes tools programmatically with logic between calls. Use `terminal` for running shell commands, builds, and processes.

## Platform Support

Code execution requires Unix domain sockets and is available on **Linux and macOS only**. It is automatically disabled on Windows — the agent falls back to regular sequential tool calls.

**Source**: `inbox/hermes_agent_docs/user-guide/features/code-execution.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution
**Last Updated**: 2026-06-19
**Status**: Active
