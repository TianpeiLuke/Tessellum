---
tags:
  - resource
  - documentation
  - hermes_agent
  - lifecycle_hooks
  - plugin_system
keywords:
  - plugin hook reference
  - ctx.register_hook
  - pre_tool_call block
  - pre_llm_call context injection
  - subagent_stop
  - transform_tool_result
  - BOOT.md gateway startup
  - shell hook worked examples
topics:
  - Hermes Agent
  - Event Hooks
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
access_control_group: ["general"]
---

# Hermes Plugin Hook Reference

## Overview

This is the **callback-signature reference for Hermes' plugin hooks**: the fourteen lifecycle hooks a [plugin](hermes_plugins_system.md) registers via `ctx.register_hook("<event>", callback)` inside `register()`. Plugin hooks fire in **both CLI and gateway** sessions (unlike gateway hooks, which are gateway-only). This note gives each hook's signature, fire site, return contract, and a canonical use case, then closes with two procedures that exercise the same surface: the **BOOT.md gateway-startup tutorial** and the **shell-hook worked examples** (drop-in scripts that ride the same dispatcher, no Python required). The three-system model, gateway-hook creation, and shell-hook config/consent/CLI surface are owned by [hermes_event_hooks](hermes_event_hooks.md).

## General Rules for All Hooks

- Callbacks receive **keyword arguments**. Always accept `**kwargs` for forward compatibility — new parameters may be added in future versions.
- If a callback **crashes**, it is logged and skipped — other hooks and the agent continue normally, so a misbehaving plugin can never break the agent.
- Only `pre_tool_call` (block), `pre_llm_call` (inject context), and the three `transform_*` hooks use their return value; all other hooks are fire-and-forget observers (see Quick Reference for exact return contracts).
- Observer callbacks receive `telemetry_schema_version` automatically, plus the `turn_id`, `api_request_id`, `task_id`, `session_id`, and `api_call_count` correlation fields. Treat `api_request_id` as an opaque identifier; do not parse its string format.

Registration is uniform across all fourteen hooks — `ctx.register_hook("<event>", callback)` inside `register(ctx)`:

```python
def register(ctx):
    ctx.register_hook("pre_tool_call", my_tool_observer)
    ctx.register_hook("pre_llm_call", my_memory_callback)
    ctx.register_hook("on_session_end", my_cleanup_callback)
```

## Quick Reference

| Hook | Fires when | Returns |
|------|-----------|---------|
| `pre_tool_call` | Before any tool executes | `{"action": "block", "message": str}` to veto the call |
| `post_tool_call` | After any tool returns | ignored |
| `pre_llm_call` | Once per turn, before the tool-calling loop | `{"context": str}` to prepend context to the user message |
| `post_llm_call` | Once per turn, after the tool-calling loop | ignored |
| `on_session_start` | New session created (first turn only) | ignored |
| `on_session_end` | Session ends | ignored |
| `on_session_finalize` | CLI/gateway tears down an active session | ignored |
| `on_session_reset` | Gateway swaps in a fresh session key (`/new`, `/reset`) | ignored |
| `subagent_stop` | A `delegate_task` child has exited | ignored |
| `pre_gateway_dispatch` | Gateway got a message, before auth + dispatch | `{"action": "skip" \| "rewrite" \| "allow", ...}` |
| `pre_approval_request` | Before an approval prompt is shown | ignored |
| `post_approval_response` | User responded to (or timed out) an approval prompt | ignored |
| `transform_tool_result` | After any tool returns, before it reaches the model | `str` to replace, `None` to pass through |
| `transform_terminal_output` | Inside `terminal`, before truncation/ANSI-strip/redact | `str` to replace, `None` to pass through |
| `transform_llm_output` | After the loop, before the final response is delivered | `str` to replace, `None`/empty to pass through |

## Tool-Loop Hooks

**`pre_tool_call`** — fires before every tool execution (built-in and plugin alike). Signature: `def cb(tool_name: str, args: dict, task_id: str, **kwargs)`. Fires in `model_tools.py` (`handle_function_call()`) before the handler runs — once per call. It is the canonical **tool-veto guardrail**: returning `{"action": "block", "message": "..."}` short-circuits the tool with `message` as the error returned to the model. The first matching block directive wins (Python plugins first, then shell hooks); any other return value is ignored. Use cases: blocking dangerous operations, rate limiting, per-user policy.

**`post_tool_call`** — fires after every tool returns. Signature: `def cb(tool_name: str, args: dict, result: str, task_id: str, duration_ms: int, **kwargs)`. `result` is always a JSON string; `duration_ms` is measured with `time.monotonic()` around `registry.dispatch()`. Fires once per call, including when the tool raised an unhandled exception (the caught error JSON is passed as `result`). Return ignored. Use cases: result logging, latency dashboards, per-tool budget alerts.

**`pre_llm_call`** — fires once per turn, before the tool-calling loop; the **only observer-class hook whose return value is used**. Signature includes `session_id, user_message, conversation_history, is_first_turn, model, platform`. Fires in `run_agent.py` (`run_conversation()`) after context compression but before the main `while` loop — once per turn, not per API call. Returning a dict with a `"context"` key (or a plain non-empty string) appends that text to the turn's **user message**; `None` injects nothing.

```python
return {"context": "Recalled memories:\n- User likes Python"}  # inject
return "Recalled memories:\n- User likes Python"                 # plain string (equivalent)
return None                                                       # no injection
```

Context is **always injected into the user message, never the system prompt** — this preserves the prompt cache (the system prompt stays identical across turns, so cached tokens are reused). All injection is ephemeral (added at API-call time only); the stored user message is never mutated. When multiple plugins return context, outputs are joined with double newlines in discovery order (alphabetical by directory). Use cases: memory recall, RAG context injection, guardrails.

**`post_llm_call`** — fires once per turn, after the loop completes and a final response is produced. Signature includes `session_id, user_message, assistant_response, conversation_history, model, platform`. Guarded by `if final_response and not interrupted`, so it does **not** fire on mid-turn interrupts or when the iteration limit is hit without a response. Return ignored. Use cases: syncing conversation data to external memory, turn-summary logging.

## Session-Lifecycle Hooks

- **`on_session_start`** — fires once when a brand-new session is created (`if not conversation_history`), after the system prompt is built but before the tool loop. Signature: `session_id, model, platform`. Use cases: init session-scoped state.
- **`on_session_end`** — fires at the end of every `run_conversation()` call regardless of outcome, plus from the CLI atexit handler when the agent was mid-turn (`_agent_running=True`) at quit (which reports `completed=False, interrupted=True`). Signature adds `completed: bool, interrupted: bool`. Use cases: flush buffers, persist state.
- **`on_session_finalize`** — fires when the CLI or gateway **tears down** an active session (`/new`, idle GC, CLI quit with an active agent) — the last chance to flush state before the session ID is gone. Signature: `session_id: str | None, platform`. Paired with `on_session_reset` on the gateway side.
- **`on_session_reset`** — fires when the gateway swaps in a **new session key** (`/new`, `/reset`, `/clear`, idle rotation). Signature: `session_id: str, platform` (already the rotated value). Gateway order: `on_session_finalize(old_id)` → swap → `on_session_reset(new_id)` → `on_session_start(new_id)`. Use cases: reset per-session caches keyed by `session_id`.

## Orchestration & Gateway-Flow Hooks

**`subagent_stop`** — fires once per child agent after `delegate_task` finishes (a batch of three children fires it three times, serialised on the parent thread). Signature: `parent_session_id, child_role: str | None, child_summary: str | None, child_status, duration_ms`. `child_status` is `"completed"`, `"failed"`, `"interrupted"`, or `"error"`. Fires in `tools/delegate_tool.py` after `ThreadPoolExecutor.as_completed()` drains all futures. With heavy delegation it fires many times per turn, so keep callbacks fast. Use cases: orchestration logging, child-duration billing.

**`pre_gateway_dispatch`** — fires once per incoming `MessageEvent`, after the internal-event guard but before auth/pairing and dispatch. Signature: `event, gateway, session_store`. Fires in `gateway/run.py` (`GatewayRunner._handle_message()`) right after `is_internal` is computed — **internal events skip the hook entirely**. The first recognized action dict wins; exceptions fall through to normal dispatch.

| Return | Effect |
|--------|--------|
| `{"action": "skip", "reason": "..."}` | Drop the message — no reply, no pairing, no auth. Plugin assumed to have handled it (e.g. silent-ingested). |
| `{"action": "rewrite", "text": "new text"}` | Replace `event.text`, then continue normal dispatch (e.g. collapse buffered ambient messages into one prompt). |
| `{"action": "allow"}` / `None` | Normal dispatch — full auth / pairing / agent-loop chain. |

Use cases: listen-only group chats, human handover (silent-ingest while owner handles the chat), policy routing.

**`pre_approval_request`** — fires before an approval request is shown, across every surface (CLI, Ink TUI, gateway platforms, ACP clients). Signature: `command, description, pattern_key, pattern_keys: list[str], session_key, surface` (`surface` is `"cli"` or `"gateway"`). Return ignored — observer-only, cannot veto; use `pre_tool_call` to block before approval. Use cases: desktop notifications, Slack webhooks, escalation.

**`post_approval_response`** — fires after the user responds (or the prompt times out). Same kwargs as `pre_approval_request` plus `choice`, one of `"once"`, `"session"`, `"always"`, `"deny"`, or `"timeout"`. Return ignored. Use cases: close the matching notification, record the final decision.

## Transform Hooks (Content Rewriters)

The three `transform_*` hooks each return a `str` to replace content, `None` to pass through.

- **`transform_tool_result`** — fires after any tool returns, before the result is appended to the conversation. Signature: `tool_name, arguments: dict, result: str, task_id: str | None`. `result` is post-truncation, post-ANSI-strip; applies to **every** tool. Use cases: redact PII, summarize long JSON, reshape `delegate_task` reports.
- **`transform_terminal_output`** — fires inside the `terminal` tool's output pipeline, **before** the 50 KB truncation, ANSI strip, and secret redaction (narrower and earlier than `transform_tool_result`). Signature: `command, output: str, exit_code: int, cwd, task_id: str | None`. Use cases: summarize massive output, strip caching-defeating timing noise.
- **`transform_llm_output`** — fires once per turn after the loop, before the final response is delivered. Signature: `response_text, session_id, model, platform`. Non-empty `str` replaces; `None`/empty passes through; **first non-empty wins**. Use cases: personality transforms, redacting identifiers, signature footers.

```python
import re
SECRET = re.compile(r"sk-[A-Za-z0-9]{32,}")

def redact_secrets(tool_name, result, **kwargs):
    if SECRET.search(result):
        return SECRET.sub("[REDACTED]", result)
    return None

def register(ctx):
    ctx.register_hook("transform_tool_result", redact_secrets)
```

## Tutorial: BOOT.md — A Gateway-Startup Checklist Hook

A popular community pattern: drop a Markdown checklist at `~/.hermes/BOOT.md` and run it once every gateway start (e.g. "check overnight cron failures and ping me on Discord"). Hermes ships **no** built-in BOOT.md hook — you wire it as a user-defined `gateway:startup` hook so the behavior is visible and opt-in. Three pieces: the `BOOT.md` file, a `gateway:startup` hook spawning a one-shot agent with the gateway's resolved model/credentials, and a `[SILENT]` convention so the agent can skip replying when there is nothing to report.

```python
"""Run ~/.hermes/BOOT.md on every gateway startup."""
import logging, threading
from pathlib import Path

logger = logging.getLogger("hooks.boot-md")
BOOT_FILE = Path.home() / ".hermes" / "BOOT.md"

def _run_boot_agent(content: str) -> None:
    try:
        from gateway.run import _resolve_gateway_model, _resolve_runtime_agent_kwargs
        from run_agent import AIAgent
        agent = AIAgent(
            model=_resolve_gateway_model(),
            **_resolve_runtime_agent_kwargs(),
            platform="gateway", quiet_mode=True,
            skip_context_files=True, skip_memory=True, max_iterations=20,
        )
        result = agent.run_conversation(_build_prompt(content))
        response = (result.get("final_response", "") or "").strip()
        if response.upper() not in {"[SILENT]", "SILENT", "NO_REPLY", "NO REPLY"}:
            logger.info("boot-md completed: %s", response[:200])
        else:
            logger.info("boot-md completed (nothing to report)")
    except Exception as e:
        logger.error("boot-md agent failed: %s", e)

async def handle(event_type: str, context: dict) -> None:
    if not BOOT_FILE.exists():
        return
    content = BOOT_FILE.read_text(encoding="utf-8").strip()
    if not content:
        return
    # Background thread so startup isn't blocked on a full agent turn.
    threading.Thread(target=_run_boot_agent, args=(content,),
                     name="boot-md", daemon=True).start()
```

The two key lines: `_resolve_gateway_model()` reads the gateway's configured model, and `_resolve_runtime_agent_kwargs()` resolves provider credentials the same way a normal gateway turn does (API keys, base URLs, OAuth tokens, credential pools). Without these, a bare `AIAgent()` falls back to built-in defaults and will 401 against any non-default endpoint. Restart with `hermes gateway restart`; delete `~/.hermes/BOOT.md` to disable. Earlier Hermes shipped this as a built-in spawning an agent with bare defaults on every boot — which is why it is now documented and opt-in.

## Shell-Hook Worked Examples

Shell hooks ride the same `invoke_hook()` dispatcher as plugin hooks (config/consent/protocol in [hermes_event_hooks](hermes_event_hooks.md)): each fires the matching plugin-hook event, pipes a JSON payload to stdin, and reads JSON from stdout. Four canonical scripts:

```yaml
# ~/.hermes/config.yaml
hooks:
  post_tool_call:                                  # 1. auto-format after writes
    - matcher: "write_file|patch"
      command: "~/.hermes/agent-hooks/auto-format.sh"
  pre_tool_call:                                   # 2. block destructive terminal
    - matcher: "terminal"
      command: "~/.hermes/agent-hooks/block-rm-rf.sh"
      timeout: 5
  pre_llm_call:                                    # 3. inject git status context
    - command: "~/.hermes/agent-hooks/inject-cwd-context.sh"
  subagent_stop:                                   # 4. log every subagent completion
    - command: "~/.hermes/agent-hooks/log-orchestration.sh"
```

```bash
#!/usr/bin/env bash
# 2. block-rm-rf.sh — veto a pre_tool_call
payload="$(cat -)"
cmd=$(echo "$payload" | jq -r '.tool_input.command // empty')
if echo "$cmd" | grep -qE 'rm[[:space:]]+-rf?[[:space:]]+/'; then
  printf '{"decision": "block", "reason": "blocked: rm -rf / is not permitted"}\n'
else
  printf '{}\n'
fi
```

Both block shapes are accepted and normalised internally: `{"decision": "block", "reason": ...}` (Claude-Code style) or `{"action": "block", "message": ...}` (Hermes-canonical); for `pre_llm_call`, return `{"context": "..."}`. The auto-format example reformats `*.py` on disk only — a later `read_file` picks up the formatted version. Malformed JSON, non-zero exit codes, and timeouts log a warning but never abort the agent loop. Python plugin hooks register first (`discover_and_load()`), shell hooks second (`register_from_config()`), so Python `pre_tool_call` block decisions take precedence and the first valid non-empty block wins.

**Source**: `inbox/hermes_agent_docs/user-guide/features/hooks.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
**Last Updated**: 2026-06-19
**Status**: Active
