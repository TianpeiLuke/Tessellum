---
tags:
  - resource
  - documentation
  - hermes_agent
  - agent_loop
  - runtime_internals
keywords:
  - hermes agent loop
  - AIAgent orchestration
  - turn lifecycle
  - api modes
  - tool execution
  - fallback model
  - iteration budget
topics:
  - Hermes Agent
  - Agent Loop Internals
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop
access_control_group: ["general"]
---

# Hermes Agent Loop Internals

## Overview

The agent loop is Hermes' core orchestration engine — the `AIAgent` class in `run_agent.py` that drives every turn of an interaction from prompt assembly through tool dispatch to provider failover. It is the single behavior layer shared by all six entry points (CLI, gateway, cron, ACP, API server, subagents): each surface hands a user message to one `AIAgent` instance and the loop does the rest. `AIAgent` assembles the effective system prompt and tool schemas via `prompt_builder.py`, selects the correct provider/API mode, makes interruptible model calls, executes tool calls (sequentially or concurrently), maintains conversation history in OpenAI message format, and handles compression, retries, and fallback model switching. It tracks iteration budgets across parent and child agents and flushes persistent memory before context is lost. This note documents *how the loop behaves at runtime*; the implementing code lives in the `repo_hermes_agent_agent_core` modules and the `snippet_hermes_agent_core_*` corpus, which this note links down to.

## Two Entry Points

`AIAgent` exposes two callable entry points. `chat()` is a thin wrapper that returns the final response string; `run_conversation()` is the full interface returning a dict of messages, metadata, and usage stats:

```python
# Simple interface — returns final response string
response = agent.chat("Fix the bug in main.py")

# Full interface — returns dict with messages, metadata, usage stats
result = agent.run_conversation(
    user_message="Fix the bug in main.py",
    system_message=None,           # auto-built if omitted
    conversation_history=None,      # auto-loaded from session if omitted
    task_id="task_abc123"
)
```

`chat()` simply extracts the `final_response` field from the dict that `run_conversation()` returns. The full interface allows the system prompt to be supplied or auto-built and the conversation history to be passed in or auto-loaded from the session store.

## API Modes

Hermes supports three API execution modes, resolved from provider selection, explicit args, and base-URL heuristics:

| API mode | Used for | Client type |
|----------|----------|-------------|
| `chat_completions` | OpenAI-compatible endpoints (OpenRouter, custom, most providers) | `openai.OpenAI` |
| `codex_responses` | OpenAI Codex / Responses API | `openai.OpenAI` with Responses format |
| `anthropic_messages` | Native Anthropic Messages API | `anthropic.Anthropic` via adapter |

The mode determines how messages are formatted, how tool calls are structured, how responses are parsed, and how caching/streaming works. All three converge on the same internal message format (OpenAI-style `role`/`content`/`tool_calls` dicts) before and after API calls. Mode resolution follows a strict priority order: (1) explicit `api_mode` constructor arg (highest), (2) provider-specific detection (e.g., `anthropic` provider → `anthropic_messages`), (3) base-URL heuristics (e.g., `api.anthropic.com` → `anthropic_messages`), and (4) default `chat_completions`.

## Turn Lifecycle

Each iteration of the agent loop follows a fixed nine-step sequence. Steps 5 onward repeat while the model keeps returning tool calls:

```text
run_conversation()
  1. Generate task_id if not provided
  2. Append user message to conversation history
  3. Build or reuse cached system prompt (prompt_builder.py)
  4. Check if preflight compression is needed (>50% context)
  5. Build API messages from conversation history
     - chat_completions: OpenAI format as-is
     - codex_responses: convert to Responses API input items
     - anthropic_messages: convert via anthropic_adapter.py
  6. Inject ephemeral prompt layers (budget warnings, context pressure)
  7. Apply prompt caching markers if on Anthropic
  8. Make interruptible API call (_interruptible_api_call)
  9. Parse response:
     - If tool_calls: execute them, append results, loop back to step 5
     - If text response: persist session, flush memory if needed, return
```

### Message Format and Alternation Rules

All messages use OpenAI-compatible format internally — `{"role": "system", "content": ...}`, `{"role": "user", ...}`, `{"role": "assistant", "content": ..., "tool_calls": [...]}`, and `{"role": "tool", "tool_call_id": ..., "content": ...}`. Reasoning content from models that support extended thinking is stored in `assistant_msg["reasoning"]` and optionally surfaced via the `reasoning_callback`.

The loop enforces strict role alternation: after the system message the sequence runs `User → Assistant → User → Assistant → ...`; during tool calling it runs `Assistant (with tool_calls) → Tool → Tool → ... → Assistant`. There are **never** two assistant messages in a row and **never** two user messages in a row — **only** the `tool` role may have consecutive entries (parallel tool results). Providers validate these sequences and reject malformed histories.

## Interruptible API Calls

API requests are wrapped in `_interruptible_api_call()`, which runs the actual HTTP call on a background thread while the main thread monitors an interrupt event:

```text
┌────────────────────────────────────────────────────┐
│  Main thread                  API thread           │
│                                                    │
│   wait on:                     HTTP POST           │
│    - response ready     ───▶   to provider         │
│    - interrupt event                               │
│    - timeout                                       │
└────────────────────────────────────────────────────┘
```

When interrupted (the user sends a new message, issues `/stop`, or a signal arrives) the API thread is abandoned and its response discarded, the agent can process the new input or shut down cleanly, and no partial response is injected into conversation history.

## Tool Execution

When the model returns tool calls, the loop chooses between sequential and concurrent execution. A **single** tool call runs directly in the main thread; **multiple** tool calls run concurrently via a `ThreadPoolExecutor`. Tools marked interactive (e.g., `clarify`) force sequential execution, and results are reinserted in the original tool-call order regardless of completion order. Each tool call proceeds through the same flow: resolve the handler from `tools/registry.py`, fire the `pre_tool_call` plugin hook, check for a dangerous command via `tools/approval.py` (and if dangerous, invoke `approval_callback` and wait for the user), execute the handler with args + `task_id`, fire the `post_tool_call` hook, and append a `{"role": "tool", "content": result}` message to history.

Four tools are intercepted by `run_agent.py` *before* reaching `handle_function_call()` because they modify agent state directly and return synthetic results without going through the registry:

| Tool | Why intercepted |
|------|--------------------|
| `todo` | Reads/writes agent-local task state |
| `memory` | Writes to persistent memory files with character limits |
| `session_search` | Queries session history via the agent's session DB |
| `delegate_task` | Spawns subagent(s) with isolated context |

## Callback Surfaces

`AIAgent` supports platform-specific callbacks that drive real-time progress in the CLI, gateway, and ACP integrations. Each surface registers the callbacks it needs; the loop fires them at the documented points:

| Callback | When fired | Used by |
|----------|-----------|---------|
| `tool_progress_callback` | Before/after each tool execution | CLI spinner, gateway progress messages |
| `thinking_callback` | When model starts/stops thinking | CLI "thinking..." indicator |
| `reasoning_callback` | When model returns reasoning content | CLI reasoning display, gateway reasoning blocks |
| `clarify_callback` | When `clarify` tool is called | CLI input prompt, gateway interactive message |
| `step_callback` | After each complete agent turn | Gateway step tracking, ACP progress |
| `stream_delta_callback` | Each streaming token (when enabled) | CLI streaming display |
| `tool_gen_callback` | When tool call is parsed from stream | CLI tool preview in spinner |
| `status_callback` | State changes (thinking, executing, etc.) | ACP status updates |

## Budget and Fallback Behavior

The agent tracks iterations via `IterationBudget`: the default is 90 iterations (configurable via `agent.max_turns`); each agent gets its own budget, and subagents get independent budgets capped at `delegation.max_iterations` (default 50), so total iterations across parent + subagents can exceed the parent's cap. At 100% the agent stops and returns a summary of work done.

When the primary model fails — a 429 rate limit, a 5xx server error, or a 401/403 auth error — the loop activates fallback: it checks the `fallback_providers` list in config, tries each fallback in order, and on success continues the conversation with the new provider. On 401/403 it attempts a credential refresh before failing over. The fallback system also covers auxiliary tasks independently — vision, compression, and web extraction each have their own fallback chain configurable via the `auxiliary.*` config section.

## Compression and Persistence

Compression triggers in two places: **preflight** (before an API call) when the conversation exceeds 50% of the model's context window, and **gateway auto-compression** (more aggressive, between turns) when it exceeds 85%. During compression, memory is flushed to disk first to prevent data loss, middle conversation turns are summarized into a compact summary, the last N messages are preserved intact (`compression.protect_last_n`, default 20), tool-call/result message pairs are kept together (never split), and a new session lineage ID is generated — compression creates a "child" session.

After each turn, messages are saved to the session store (SQLite via `hermes_state.py`), memory changes are flushed to `MEMORY.md` / `USER.md`, and the session can be resumed later via `/resume` or `hermes chat --resume`.

## Key Source Files

The loop's behavior is implemented across the agent-core modules: `run_agent.py` (the `AIAgent` class — the complete agent loop), `agent/prompt_builder.py` (system-prompt assembly from memory, skills, context files, personality), `agent/context_engine.py` (the `ContextEngine` ABC for pluggable context management), `agent/context_compressor.py` (the default lossy-summarization engine), `agent/prompt_caching.py` (Anthropic prompt-caching markers and cache metrics), `agent/auxiliary_client.py` (the auxiliary LLM client for side tasks like vision and summarization), and `model_tools.py` (tool-schema collection and `handle_function_call()` dispatch).

**Source**: `inbox/hermes_agent_docs/developer-guide/agent-loop.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop
**Last Updated**: 2026-06-19
**Status**: Active
