---
tags:
  - resource
  - documentation
  - hermes_agent
  - context_engine
  - plugin_authoring
keywords:
  - context engine plugin
  - ContextEngine ABC
  - ContextCompressor replacement
  - should_compress compress
  - single context engine
  - register_context_engine
topics:
  - Hermes Agent
  - Plugin Authoring
  - Context Management
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/context-engine-plugin
access_control_group: ["general"]
---

# Building a Context Engine Plugin

## Overview

A context engine plugin is a drop-in replacement for Hermes' built-in `ContextCompressor` — the component that decides *when* and *how* a conversation's message history gets compacted to stay inside the model's context window. Instead of editing the Hermes repo, a third party places a directory under `plugins/context_engine/<name>/`, subclasses the `ContextEngine` ABC (defined in `agent/context_engine.py`), and the agent swaps in that alternative strategy. The canonical example is a Lossless Context Management (LCM) engine that builds a knowledge DAG rather than doing lossy summarization.

Two rules govern the engine surface. First, **only one** context engine is active at a time — there is no fan-out or fallback chain. Second, plugin engines are **never auto-activated**: the user must explicitly set `context.engine` in `config.yaml` (or pick the engine via `hermes plugins`) for it to take over from the built-in compressor. The ABC the plugin implements is the same interface the default `ContextCompressor` satisfies, so the conversation loop calls the plugin exactly where it would have called the built-in compressor: `update_from_response()` after each LLM call, `should_compress()` each turn, and `compress()` when compaction fires. This note is the step-by-step authoring procedure; the *concept* of a pluggable context engine lives in `term_context_engine`, and the compression internals it replaces are covered by the SP18 context-compression docs.

## How it works

The agent's context management is built on the `ContextEngine` ABC in `agent/context_engine.py`; the built-in `ContextCompressor` is the default implementation, and plugin engines must implement the same interface. Only one engine can be active at a time, and selection is config-driven:

```yaml
# config.yaml
context:
  engine: "compressor"    # default built-in
  engine: "lcm"           # activates a plugin engine named "lcm"
```

Plugin engines are never auto-activated — the user must explicitly set `context.engine` to the plugin's `name`.

## Directory structure

Each context engine lives in `plugins/context_engine/<name>/`:

```
plugins/context_engine/lcm/
├── __init__.py      # exports the ContextEngine subclass
├── plugin.yaml      # metadata (name, description, version)
└── ...              # any other modules your engine needs
```

## The ContextEngine ABC

Your engine must implement four **required** members — `name`, `update_from_response`, `should_compress`, and `compress`:

```python
from agent.context_engine import ContextEngine

class LCMEngine(ContextEngine):

    @property
    def name(self) -> str:
        """Short identifier, e.g. 'lcm'. Must match config.yaml value."""
        return "lcm"

    def update_from_response(self, usage: dict) -> None:
        """Called after every LLM call with the usage dict.

        Update self.last_prompt_tokens, self.last_completion_tokens,
        self.last_total_tokens from the response.
        """

    def should_compress(self, prompt_tokens: int = None) -> bool:
        """Return True if compaction should fire this turn."""

    def compress(self, messages: list, current_tokens: int = None,
                 focus_topic: str = None) -> list:
        """Compact the message list and return a new (possibly shorter) list.

        The returned list must be a valid OpenAI-format message sequence.

        ``focus_topic`` is an optional topic string from manual
        ``/compress <focus>``; engines that support guided compression should
        prioritise preserving information related to it, others may ignore it.
        """
```

The agent reads these **class attributes** directly for display and logging, so the engine must keep them current: `last_prompt_tokens`, `last_completion_tokens`, `last_total_tokens`, `threshold_tokens` (when compression triggers), `context_length` (the model's full context window), and `compression_count` (how many times `compress()` has run).

The ABC also exposes **optional methods** with sensible defaults, overridden only as needed: `on_session_start(session_id, **kwargs)` (load persisted DAG/DB state), `on_session_end(session_id, messages)` (flush state, close connections), `on_session_reset()` (clear per-session state beyond the token-counter reset the default does), `update_model(model, context_length, ...)` (recompute budgets on model switch), `get_tool_schemas()` / `handle_tool_call(name, args, **kwargs)` (expose agent-callable engine tools — default returns `[]` / error JSON), `should_compress_preflight(messages)` (cheap pre-API estimate, default `False`), and `get_status()` (custom metrics; default returns a standard token/threshold dict).

## Engine tools

Context engines can expose tools the agent calls directly. Return schemas from `get_tool_schemas()` and handle calls in `handle_tool_call()`:

```python
def get_tool_schemas(self):
    return [{
        "name": "lcm_grep",
        "description": "Search the context knowledge graph",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"],
        },
    }]

def handle_tool_call(self, name, args, **kwargs):
    if name == "lcm_grep":
        results = self._search_dag(args["query"])
        return json.dumps({"results": results})
    return json.dumps({"error": f"Unknown tool: {name}"})
```

Engine tools are injected into the agent's tool list at startup and dispatched automatically — no registry registration needed.

## Registration

The recommended path is **via directory**: place the engine in `plugins/context_engine/<name>/` with an `__init__.py` that exports the `ContextEngine` subclass, and the discovery system finds and instantiates it automatically.

Alternatively, a general plugin can register an engine **via the general plugin system** in its `register(ctx)` hook:

```python
def register(ctx):
    engine = LCMEngine(context_length=200000)
    ctx.register_context_engine(engine)
```

Only one engine can be registered. A second plugin attempting to register is rejected with a warning.

## Lifecycle

The engine is driven through a fixed lifecycle: (1) instantiated on plugin load or directory discovery; (2) `on_session_start()` when a conversation begins; (3) `update_from_response()` after each API call; (4) `should_compress()` checked each turn; (5) `compress()` called when `should_compress()` returns True; (6) `on_session_end()` at a session boundary (CLI exit, `/reset`, gateway expiry). `on_session_reset()` is called on `/new` or `/reset` to clear per-session state without a full shutdown.

## Configuration

Users select the engine via `hermes plugins` → Provider Plugins → Context Engine, or by editing `config.yaml` so that `context.engine` matches the engine's `name` property (the same `context.engine: "lcm"` setting shown in How it works). The `compression` config block (`compression.threshold`, `compression.protect_last_n`, etc.) is specific to the built-in `ContextCompressor`. A plugin engine should define its own config format if needed, reading from `config.yaml` during initialization.

## Testing

The ABC ships a contract test you mirror — verify the engine satisfies the ABC and that `compress()` returns a valid OpenAI-format message list:

```python
from agent.context_engine import ContextEngine

def test_engine_satisfies_abc():
    engine = YourEngine(context_length=200000)
    assert isinstance(engine, ContextEngine)
    assert engine.name == "your-name"

def test_compress_returns_valid_messages():
    engine = YourEngine(context_length=200000)
    msgs = [{"role": "user", "content": "hello"}]
    result = engine.compress(msgs)
    assert isinstance(result, list)
    assert all("role" in m for m in result)
```

See `tests/agent/test_context_engine.py` for the full ABC contract test suite.

**Source**: `inbox/hermes_agent_docs/developer-guide/context-engine-plugin.md`
**Last Updated**: 2026-06-19
**Status**: Active
