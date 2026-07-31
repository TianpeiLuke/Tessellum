---
tags:
  - resource
  - documentation
  - hermes_agent
  - python_library
  - embedding
keywords:
  - hermes python library
  - AIAgent embedding
  - run_conversation
  - quiet_mode batch processing
  - enabled disabled toolsets
  - save_trajectories sharegpt
  - constructor parameters
topics:
  - Hermes Agent
  - Python Library
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/python-library
access_control_group: ["general"]
---

# Using Hermes as a Python Library

## Overview

This guide is the **how-to for embedding Hermes' `AIAgent` directly in your own Python code** — scripts, web apps, or automation pipelines — with no CLI required. Hermes is not just a terminal tool: you `pip install` it from the repo, `from run_agent import AIAgent`, and drive the same agent loop (tool calls, retries, memory) programmatically. The guide walks the two entry methods (`chat()` for a string-in/string-out call and `run_conversation()` for full control over the message history and metadata), the constructor knobs that scope tools and output, multi-turn state, trajectory capture, custom system prompts, parallel batch processing, and three integration patterns (FastAPI, Discord, CI/CD). The recurring discipline is two-fold: always set `quiet_mode=True` so CLI spinners don't pollute your output, and always create **one `AIAgent` per thread or task** because the instance holds non-thread-safe state. This is the usage layer over the embeddable agent — the orchestration internals it exposes live in the `repo_hermes_agent_agent_core` source modules.

## Installation

Install Hermes directly from the repository with `pip install git+https://github.com/NousResearch/hermes-agent.git` (or the same URL via `uv pip install`). The `requirements.txt` pin form is `hermes-agent @ git+https://github.com/NousResearch/hermes-agent.git`. The **same environment variables used by the CLI are required** when using Hermes as a library. At minimum, set `OPENROUTER_API_KEY` (or `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` if using direct provider access).

## Basic Usage

The simplest path is `chat()` — pass a message, get a string back. It handles the full conversation loop internally (tool calls, retries, everything) and returns just the final text. Always set `quiet_mode=True` when embedding to suppress CLI spinners, progress indicators, and other terminal noise.

```python
from run_agent import AIAgent

agent = AIAgent(
    model="anthropic/claude-sonnet-4.6",
    quiet_mode=True,
)
response = agent.chat("What is the capital of France?")
print(response)
```

## Full Conversation Control

For more control, call `run_conversation()` directly. It returns a dictionary with the full reply, message history, and metadata:

```python
result = agent.run_conversation(
    user_message="Search for recent Python 3.13 features",
    task_id="my-task-1",
)

print(result["final_response"])
print(f"Messages exchanged: {len(result['messages'])}")
```

The returned dictionary contains **`final_response`** (the agent's final text reply) and **`messages`** (the complete history — system, user, assistant, tool calls). The `task_id` you pass is stored on the instance for VM isolation but is **not** echoed back in the return dict. You can also pass a `system_message=` to `run_conversation()` to override the ephemeral system prompt for that one call.

## Configuring Tools

Scope which toolsets the agent can use via two constructor knobs: `enabled_toolsets=["web"]` is a whitelist for a minimal, locked-down agent (e.g. only web search for a research bot), while `disabled_toolsets=["terminal"]` is a blacklist when you want most capabilities but must restrict specific ones (e.g. no terminal in a shared environment). Pass either as a list to `AIAgent(...)` alongside `quiet_mode=True`.

## Multi-turn Conversations

Maintain state across turns by passing the previous result's `messages` list back in via `conversation_history`:

```python
result1 = agent.run_conversation("My name is Alice")
history = result1["messages"]

# Second turn — agent remembers the context
result2 = agent.run_conversation("What's my name?", conversation_history=history)
print(result2["final_response"])  # "Your name is Alice."
```

The agent copies `conversation_history` internally, so your original list is never mutated.

## Saving Trajectories & Custom System Prompts

Set `save_trajectories=True` to capture conversations in ShareGPT format — each conversation is appended as a single JSONL line to `trajectory_samples.jsonl`, useful for generating training data or debugging. Separately, `ephemeral_system_prompt` sets a custom system prompt that guides behavior but is **not** saved to trajectory files (keeping training data clean) — ideal for specialized agents (code reviewer, SQL assistant) sharing the same underlying tooling.

```python
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    save_trajectories=True,
    ephemeral_system_prompt="You are a SQL expert. Only answer database questions.",
    quiet_mode=True,
)
agent.chat("How do I write a JOIN query?")  # appended to trajectory_samples.jsonl
```

## Batch Processing

For many prompts in parallel, the bundled `batch_runner.py` manages concurrent `AIAgent` instances with resource isolation: `python batch_runner.py --input prompts.jsonl --output results.jsonl`. Each prompt gets its own `task_id` and isolated environment. For custom batch logic, build your own with `AIAgent` directly — the critical rule is a **fresh agent per task** for thread safety:

```python
import concurrent.futures
from run_agent import AIAgent

def process_prompt(prompt):
    # Create a fresh agent per task for thread safety
    agent = AIAgent(model="anthropic/claude-sonnet-4", quiet_mode=True, skip_memory=True)
    return agent.chat(prompt)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(process_prompt, prompts))
```

Never share an instance across concurrent calls: the agent maintains internal state (conversation history, tool sessions, iteration counters) that is not thread-safe.

## Integration Examples

Three patterns, all sharing the same embedding idiom — construct an `AIAgent` per request/event with `quiet_mode=True`, and for stateless services add `skip_context_files=True` + `skip_memory=True`:

- **FastAPI endpoint** — a `POST /chat` route constructs a fresh agent per request and returns `agent.chat(request.message)`; `skip_context_files`/`skip_memory` keep the endpoint stateless.
- **Discord bot** — on each `!hermes <query>` message, construct an agent with `platform="discord"` and reply with `response[:2000]` (Discord's message cap).
- **CI/CD pipeline step** — pipe a `git diff main...HEAD` into `agent.chat(...)` for an automated PR review, with `disabled_toolsets=["terminal", "browser"]` to lock the agent down in CI.

```python
@app.post("/chat")
async def chat(request: ChatRequest):
    agent = AIAgent(
        model=request.model,
        quiet_mode=True,
        skip_context_files=True,
        skip_memory=True,
    )
    return {"response": agent.chat(request.message)}
```

## Key Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | `""` | Model in OpenRouter format (defaults to empty; resolved from your hermes config at runtime) |
| `quiet_mode` | `bool` | `False` | Suppress CLI output |
| `enabled_toolsets` | `List[str]` | `None` | Whitelist specific toolsets |
| `disabled_toolsets` | `List[str]` | `None` | Blacklist specific toolsets |
| `save_trajectories` | `bool` | `False` | Save conversations to JSONL |
| `ephemeral_system_prompt` | `str` | `None` | Custom system prompt (not saved to trajectories) |
| `max_iterations` | `int` | `90` | Max tool-calling iterations per conversation |
| `skip_context_files` | `bool` | `False` | Skip loading AGENTS.md files |
| `skip_memory` | `bool` | `False` | Disable persistent memory read/write |
| `api_key` | `str` | `None` | API key (falls back to env vars) |
| `base_url` | `str` | `None` | Custom API endpoint URL |
| `platform` | `str` | `None` | Platform hint (`"discord"`, `"telegram"`, etc.) |

## Important Notes

- Set **`skip_context_files=True`** if you don't want `AGENTS.md` files from the working directory loaded into the system prompt; set **`skip_memory=True`** to prevent persistent-memory read/write (recommended for stateless API endpoints). The `platform` parameter injects platform-specific formatting hints so the agent adapts its output style.
- **Thread safety**: create one `AIAgent` per thread or task; never share an instance across concurrent calls.
- **Resource cleanup**: the agent automatically cleans up resources (terminal sessions, browser instances) when a conversation ends; in a long-lived process ensure each conversation completes normally.
- **Iteration limits**: the default `max_iterations=90` is generous — for simple Q&A, lower it (e.g. `max_iterations=10`) to prevent runaway tool-calling loops and control costs.

**Source**: `inbox/hermes_agent_docs/guides/python-library.md` · https://hermes-agent.nousresearch.com/docs/guides/python-library
**Last Updated**: 2026-06-19
**Status**: Active
