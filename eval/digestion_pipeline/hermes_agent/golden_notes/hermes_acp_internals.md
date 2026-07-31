---
tags:
  - resource
  - documentation
  - hermes_agent
  - acp
  - editor_integration
keywords:
  - acp adapter
  - hermes acp json-rpc stdio server
  - HermesACPAgent
  - SessionManager event bridge permission bridge
  - session fork cancel
  - runtime resolver auth reuse
  - editor cwd binding
  - fifo duplicate tool call tracking
topics:
  - Hermes Agent
  - Agent Client Protocol
language: markdown
date of note: 2026-06-19
status: active
building_block: model
source_url: https://hermes-agent.nousresearch.com/docs/developer-guide/acp-internals
access_control_group: ["general"]
---

# Hermes Agent — ACP Internals

## Overview

The ACP adapter is the layer that lets a code editor drive a Hermes Agent session over the **Agent Client Protocol (ACP)**: it wraps Hermes' *synchronous* `AIAgent` in an *asynchronous* JSON-RPC stdio server so editors (e.g. Zed) can open, prompt, cancel, and fork agent sessions. The adapter lives in the `acp_adapter/` package and is launched by `hermes acp` (or the `hermes-acp` script / `python -m acp_adapter`). It does not re-implement provider auth, session storage, or tool dispatch — it *bridges* the editor's async JSON-RPC world to Hermes' existing synchronous runtime: callbacks become `session_update` events, terminal approval prompts become ACP permission requests, and Hermes tools are rendered into editor-facing tool kinds (file diffs, shell text, previews). Stdout is reserved for ACP JSON-RPC transport; human-readable logs go to stderr. The key implementation files are `acp_adapter/entry.py`, `server.py`, `session.py`, `events.py`, `permissions.py`, `tools.py`, `auth.py`, and the registry manifest `acp_registry/agent.json`.

## Boot flow

`hermes acp` (or `hermes-acp` / `python -m acp_adapter`) routes into `acp_adapter.entry.main()`, which parses early flags, loads the environment, configures stderr logging, constructs the agent, and hands it to the ACP runtime:

```text
hermes acp / hermes-acp / python -m acp_adapter
  -> acp_adapter.entry.main()
  -> parse --version / --check / --setup before server startup
  -> load ~/.hermes/.env
  -> configure stderr logging
  -> construct HermesACPAgent
  -> acp.run_agent(agent, use_unstable_protocol=True)
```

The Zed ACP Registry path launches the same adapter through `uvx --from 'hermes-agent[acp]==<version>' hermes-acp`, pointed at the `hermes-agent` PyPI release.

## Major components

The adapter is five cooperating pieces:

- **`HermesACPAgent`** (`acp_adapter/server.py`) implements the ACP agent protocol. Responsibilities: initialize / authenticate; the `new`/`load`/`resume`/`fork`/`list`/`cancel` session methods; prompt execution; session model switching; and wiring sync `AIAgent` callbacks into ACP async notifications.
- **`SessionManager`** (`acp_adapter/session.py`) tracks live ACP sessions. Each session stores `session_id`, `agent`, `cwd`, `model`, `history`, and `cancel_event`. The manager is thread-safe and supports `create`, `get`, `remove`, `fork`, `list`, `cleanup`, and cwd updates.
- **Event bridge** (`acp_adapter/events.py`) converts `AIAgent` callbacks into ACP `session_update` events. The bridged callbacks are `tool_progress_callback`, `thinking_callback` (currently set to `None` in the ACP bridge — reasoning is forwarded through `step_callback` instead), and `step_callback`. Because `AIAgent` runs in a worker thread while ACP I/O lives on the main event loop, the bridge marshals events across threads with `asyncio.run_coroutine_threadsafe(...)`:

```python
asyncio.run_coroutine_threadsafe(...)
```

- **Permission bridge** (`acp_adapter/permissions.py`) adapts dangerous-terminal approval prompts into ACP permission requests. The option mapping is `allow_once` → Hermes `once`, `allow_always` → Hermes `always`, and reject options → Hermes `deny`. Timeouts and bridge failures **deny by default** (fail-closed).
- **Tool rendering helpers** (`acp_adapter/tools.py`) map Hermes tools to ACP tool kinds and build editor-facing content: `patch` / `write_file` → file diffs, `terminal` → shell command text, `read_file` / `search_files` → text previews, and large results → truncated text blocks for UI safety.

## Session lifecycle

A new session constructs an `AIAgent` pinned to the `acp` platform and the `hermes-acp` toolset, binding the task/session ID to a cwd override; a prompt extracts text from ACP content blocks, installs callbacks and the approval bridge, and runs the agent in a `ThreadPoolExecutor`:

```text
new_session(cwd)
  -> create SessionState
  -> create AIAgent(platform="acp", enabled_toolsets=["hermes-acp"])
  -> bind task_id/session_id to cwd override

prompt(..., session_id)
  -> extract text from ACP content blocks
  -> reset cancel event
  -> install callbacks + approval bridge
  -> run AIAgent in ThreadPoolExecutor
  -> update session history
  -> emit final agent message chunk
```

**Cancelation.** `cancel(session_id)` sets the session cancel event, calls `agent.interrupt()` when available, and causes the prompt response to return `stop_reason="cancelled"`.

**Forking.** `fork_session()` deep-copies message history into a new live session, preserving conversation state while giving the fork its own session ID and cwd.

## Provider/auth behavior

ACP does not implement its own auth store. Instead it reuses Hermes' runtime resolver (`acp_adapter/auth.py` → `hermes_cli/runtime_provider.py`), so ACP advertises and uses the currently configured Hermes provider/credentials. It also always advertises a terminal setup auth method (`hermes-setup`, args `--setup`) so first-run registry clients can open Hermes' interactive model/provider configuration before starting a normal ACP session.

## Working directory binding

ACP sessions carry an editor cwd. The session manager binds that cwd to the ACP session ID via task-scoped terminal/file overrides, so file and terminal tools operate relative to the editor workspace rather than the process working directory.

## Duplicate same-name tool calls

The event bridge tracks tool IDs **FIFO per tool name**, not just one ID per name. This matters for parallel same-name calls and repeated same-name calls in one step: without FIFO queues, completion events would attach to the wrong tool invocation.

## Approval callback restoration

ACP temporarily installs an approval callback on the terminal tool during prompt execution, then restores the previous callback afterward. This avoids leaving ACP session-specific approval handlers installed globally forever.

## Current limitations

- ACP sessions are persisted to the shared `~/.hermes/state.db` (SessionDB) and transparently restored across process restarts; they appear in `session_search`.
- Non-text prompt blocks are currently ignored for request-text extraction.
- Editor-specific UX varies by ACP client implementation.

**Source**: `inbox/hermes_agent_docs/developer-guide/acp-internals.md` · https://hermes-agent.nousresearch.com/docs/developer-guide/acp-internals
**Last Updated**: 2026-06-19
**Status**: Active
