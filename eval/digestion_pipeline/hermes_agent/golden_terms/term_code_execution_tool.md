---
tags:
  - resource
  - terminology
  - agentic_ai
  - llm_tools
  - developer_tools
keywords:
  - Code Execution Tool
  - execute_code
  - programmatic tool calling
  - code mode
  - RPC code sandbox
  - hermes_tools
topics:
  - agentic AI tools
  - programmatic tool calling
  - sandboxed code execution
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# Code Execution Tool - Programmatic Tool Calling Sandbox (`execute_code`)

## Definition

A **code execution tool** is an agent tool that lets a large-language-model agent *author and run a program* (typically Python) which itself calls the agent's other tools **programmatically over an in-process channel**, instead of the model emitting a separate tool call per step. The canonical instance is the [Hermes Agent](term_hermes_agent.md) `execute_code` tool: the agent writes a script with `from hermes_tools import ...`, Hermes generates a `hermes_tools.py` RPC stub, opens a Unix-domain-socket listener thread, and runs the script in a child process — every in-script tool call is serialized to JSON, sent over the socket to the parent's `handle_function_call` handler, and the parsed result is returned. The problem it solves is *context-window bloat and round-trip latency*: only the script's `print()` output re-enters the model context, so intermediate tool results (large search payloads, file contents, transcripts) never consume tokens, and N chained operations execute in **one** LLM turn rather than N model round-trips.

This is the *tool* realization of the broader "code mode" / programmatic-tool-calling pattern (distinct from the general [Code Interpreter](term_code_interpreter.md) capability, which is generate-then-execute code for *data analysis*; a code execution tool is specifically about orchestrating *other tools* in code). It is the natural fit when a task needs 3+ tool calls with processing logic — loops, conditional branching, or bulk filtering — between them.

## Context

In Hermes Agent, `execute_code` is one of the registered tools (alongside `delegate_task`, `terminal`, file tools); the [agent harness](term_agent_harness.md) exposes it through the model's [function calling](term_function_calling.md) interface inside a [ReAct](term_react.md)-style loop. Its configuration block (`code_execution.mode`, `timeout`, `max_tool_calls`) lives in `~/.hermes/config.yaml`, and skill `required_environment_variables` passthrough flows into its child process.

The same pattern is widely adopted across the industry. Anthropic's "code execution with MCP" guidance reports cutting a workflow from ~150,000 tokens to ~2,000 (≈98.7%) by having the agent write code against tool APIs and filter results in the sandbox; their production guidance cites ~37% token reduction from programmatic tool calling and 85%+ from deferred tool-definition loading. Cloudflare's "Code Mode" covers 2,500 endpoints with just 2 tools in ~1K tokens. In all of these, the tool sits behind a [sandbox backend](term_sandbox_backend.md) with credential-scrubbing defaults that strip [PII](term_pii.md) and secrets, because running agent-authored code is a data-compromise and [prompt-injection](term_prompt_injection.md) surface.

## Key Characteristics

- **Programmatic tool orchestration**: the script calls registered tools in code (loops, conditionals, variable reuse), collapsing multi-step workflows into a single agent turn — the defining difference from a sequence of direct JSON tool calls.
- **Print-only context return**: only stdout from `print()` re-enters the model; intermediate tool outputs stay in the sandbox, which is what produces the large token savings.
- **In-process RPC channel**: in Hermes, an `execute_code` script reaches tools over a Unix-domain-socket RPC to the parent's `handle_function_call` — calls behave identically to normal tool calls (same rate limits, same error handling).
- **Restricted tool whitelist**: only a curated subset is callable in-script (Hermes: `web_search`, `web_extract`, `read_file`, `write_file`, `search_files`, `patch`, foreground `terminal`); recursion (`execute_code`), `delegate_task`, and MCP tools are blocked to prevent fan-out and exfiltration loops.
- **Execution modes**: `project` (default — session working dir, active `VIRTUAL_ENV`/`CONDA_PREFIX` interpreter, falls back to `sys.executable`) vs `strict` (isolated temp staging dir, Hermes's own interpreter, maximum reproducibility). Mode changes *where/which interpreter*, not *which credentials or tools*.
- **Resource limits**: timeout (300s, SIGTERM→SIGKILL after 5s grace), stdout cap (50 KB), stderr cap (10 KB), and a tool-call cap (50/execution) — all configurable.
- **Environment scrubbing**: the child runs with a minimal environment; variables whose names contain `KEY`/`TOKEN`/`SECRET`/`PASSWORD`/`CREDENTIAL`/`PASSWD`/`AUTH` are stripped. Only safe system vars and four operational `HERMES_*` names pass through; skills opt secrets back in via `required_environment_variables`.
- **Structured result + clean teardown**: returns `status` (success/error/timeout/interrupted), `output`, `tool_calls_made`, `duration_seconds`; the child runs in its own process group for clean kill on timeout/interrupt. Requires Unix domain sockets — Linux/macOS only.

## Related Terms


## References

- [Code execution with MCP — Anthropic Engineering](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Hermes Agent — Code Execution (Programmatic Tool Calling)](https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution/)
- [Cloudflare — Code Mode: the better way to use MCP](https://blog.cloudflare.com/code-mode/)
