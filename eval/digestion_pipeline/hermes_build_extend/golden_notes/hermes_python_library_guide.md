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

## Related Notes

**Terms**
- [term_agent_orchestration](../../term_dictionary/term_agent_orchestration.md) — coordinating an agent's tool/LLM loop; relevance: `run_conversation` runs the orchestration loop the library exposes.
- [term_function_calling](../../term_dictionary/term_function_calling.md) — LLM tool/function invocation; relevance: the toolsets `enabled/disabled_toolsets` scope are function-calling tools.
- [term_autonomous_coding_agents](../../term_dictionary/term_autonomous_coding_agents.md) — self-directed coding agents; relevance: `AIAgent` is exactly such an agent driven programmatically.
- [term_agent_harness](../../term_dictionary/term_agent_harness.md) — the runtime wrapping an LLM into an agent; relevance: `AIAgent` is the programmatic harness this guide embeds.
- [term_multi_agent_systems](../../term_dictionary/term_multi_agent_systems.md) — multiple cooperating agents; relevance: `batch_runner` fans out many isolated agent instances.
- [term_session_persistence](../../term_dictionary/term_session_persistence.md) — carrying conversation state across turns; relevance: `conversation_history` persists the message list between calls.
- [term_context_window](../../term_dictionary/term_context_window.md) — the bounded token budget; relevance: `max_iterations` and message-history growth pressure the window.
- [term_idempotency](../../term_dictionary/term_idempotency.md) — repeatable, side-effect-safe runs; relevance: per-task fresh agents + `skip_memory` keep batch/stateless runs idempotent. (+fin: term_agent_trajectory [own SP06])

**Code-Repos**
- [repo_hermes_agent_agent_core](../../../areas/code_repos/repo_hermes_agent_agent_core.md) — `AIAgent` orchestrator + `chat()`/`run_conversation()` + conversation loop; relevance: the entire library API surface (constructor params, `final_response`/`messages`) is implemented here.
- [repo_hermes_agent_trajectory_research](../../../areas/code_repos/repo_hermes_agent_trajectory_research.md) — ShareGPT trajectory schema/canonicalize/export; relevance: `save_trajectories` writes via this module.
- [repo_hermes_agent_tools](../../../areas/code_repos/repo_hermes_agent_tools.md) — `enabled/disabled_toolsets` + tool registry; relevance: the Configuring-Tools section toggles toolsets here.
- [repo_hermes_agent_cli](../../../areas/code_repos/repo_hermes_agent_cli.md) — `batch_runner.py` + per-thread instance rule; relevance: the batch-processing + thread-safety notes are rooted here.
- [repo_hermes_agent](../../../areas/code_repos/repo_hermes_agent.md) — `pip install git+…` package + FastAPI/Discord/CI integration; relevance: the install + embedding examples target this package.

**Snippets**
- [snippet_hermes_agent_core_aiagent_orchestrator](../../code_snippets/snippet_hermes_agent_core_aiagent_orchestrator.md) — the `AIAgent` orchestrator; relevance: implements the constructor + `chat()`/`run_conversation()` API.
- [snippet_hermes_agent_core_run_agent_cli](../../code_snippets/snippet_hermes_agent_core_run_agent_cli.md) — agent-run entry point; relevance: the `from run_agent import AIAgent` entry the examples import.
- [snippet_hermes_agent_core_chat_helpers_max_iter](../../code_snippets/snippet_hermes_agent_core_chat_helpers_max_iter.md) — chat helpers + `max_iterations` bound; relevance: implements the iteration-limit constructor knob.
- [snippet_hermes_agent_batch_runner](../../code_snippets/snippet_hermes_agent_batch_runner.md) — `batch_runner.py`; relevance: the parallel batch-processing CLI this guide documents.
- [snippet_hermes_agent_batch_runner_spawn](../../code_snippets/snippet_hermes_agent_batch_runner_spawn.md) — batch agent spawn; relevance: the per-task fresh-instance thread-safety rule.
- [snippet_hermes_agent_batch_runner_queue](../../code_snippets/snippet_hermes_agent_batch_runner_queue.md) — batch work queue; relevance: how concurrent prompts are dispatched.
- [snippet_hermes_agent_batch_runner_aggregate](../../code_snippets/snippet_hermes_agent_batch_runner_aggregate.md) — batch result aggregation; relevance: collecting `results.jsonl` from many runs.
- [snippet_hermes_agent_trajectory_schema](../../code_snippets/snippet_hermes_agent_trajectory_schema.md) — ShareGPT trajectory schema; relevance: the JSONL format `save_trajectories` writes.
- [snippet_hermes_agent_trajectory_canonicalize](../../code_snippets/snippet_hermes_agent_trajectory_canonicalize.md) — trajectory canonicalization; relevance: how saved conversations are normalized to ShareGPT.
- [snippet_hermes_agent_core_conversation_loop_session_persist](../../code_snippets/snippet_hermes_agent_core_conversation_loop_session_persist.md) — session-persist conversation loop; relevance: the `conversation_history` multi-turn persistence path.

**Docs**
- [hermes_build_plugin_tutorial](hermes_build_plugin_tutorial.md) — the plugin walkthrough; relevance: the CLI-plugin route contrasted with the programmatic library route.
- [hermes_automation_blueprints_scheduled](hermes_automation_blueprints_scheduled.md) — scheduled blueprints; relevance: `cron` jobs vs the `batch_runner` programmatic batch.
- [hermes_use_mcp_guide](hermes_use_mcp_guide.md) — MCP usage; relevance: the toolsets the library enables/disables via `enabled/disabled_toolsets`.
- [hermes_tips_best_practices](hermes_tips_best_practices.md) — tips collection; relevance: the prompt-cache/cost levers that apply when embedding the agent.
- [hermes_work_with_skills_guide](hermes_work_with_skills_guide.md) — skills how-to; relevance: skills loaded through the embedded `AIAgent`.
- [cc_agent_sdk_overview](../claude_code/cc_agent_sdk_overview.md) — CC Agent SDK overview; relevance: closest analogue to embedding the agent.
- [cc_sdk_python_client](../claude_code/cc_sdk_python_client.md) — CC Python SDK client; relevance: analogue to `AIAgent`.
- [cc_sdk_python_entry_points](../claude_code/cc_sdk_python_entry_points.md) — CC SDK entry functions; relevance: analogue to `chat()`/`run_conversation()`.
- [cc_headless_mode](../claude_code/cc_headless_mode.md) — programmatic/headless runs; relevance: analogue to CI/batch embedding.
- [cc_headless_examples](../claude_code/cc_headless_examples.md) — headless integration examples; relevance: analogue to the FastAPI/Discord/CI examples.
- [cc_agent_sdk_agent_loop](../claude_code/cc_agent_sdk_agent_loop.md) — CC Agent SDK agent loop; relevance: analogue to the `run_conversation` orchestration loop (`final_response`+`messages`).
- [cc_agent_sdk_install_and_auth](../claude_code/cc_agent_sdk_install_and_auth.md) — CC Agent SDK install/auth; relevance: analogue to `pip install git+…` + key resolution for the library.

**Source**: `inbox/hermes_agent_docs/guides/python-library.md` · https://hermes-agent.nousresearch.com/docs/guides/python-library
**Last Updated**: 2026-06-19
**Status**: Active
