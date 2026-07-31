---
tags:
  - resource
  - documentation
  - hermes_agent
  - configuration
  - context_management
keywords:
  - context compression threshold
  - context engine compressor lcm
  - iteration budget pressure
  - api timeout layers
  - file read safety
  - tool output truncation
  - global toolset disable
  - git worktree isolation
topics:
  - Hermes Agent
  - Configuration
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/configuration
access_control_group: ["general"]
---

# Hermes Agent — Runtime & Context-Window Settings

## Overview

This is the `config.yaml` cluster that governs how Hermes manages the model's **context window and runtime budget**: when to compress a long conversation, which context engine does it, how many iterations the agent gets per turn, the timeout layers around provider API calls, how big a single file read or tool output can be, how to disable a toolset everywhere at once, and how git worktrees isolate parallel agents. Every key here lives in `config.yaml` (compression has *no* environment variables); the timeout layer additionally exposes `HERMES_*` env overrides. These knobs all defend a single resource — the prompt's token budget — so a model with a 16K window and one with 200K+ are tuned through the same settings with opposite values.

## Context Compression

Hermes automatically compresses long conversations to stay within the model's context window. The compression summarizer is a separate LLM call you can point at any provider or endpoint. All compression settings live in `config.yaml` (no environment variables).

```yaml
compression:
  enabled: true                                     # Toggle compression on/off
  threshold: 0.50                                   # Compress at this % of context limit
  target_ratio: 0.20                                # Fraction of threshold to preserve as recent tail
  protect_last_n: 20                                # Min recent messages to keep uncompressed
  protect_first_n: 3                                # Non-system head messages pinned across compactions (0 = pin nothing)
  hygiene_hard_message_limit: 400                   # Gateway safety valve — see below

# The summarization model/provider is configured under auxiliary:
auxiliary:
  compression:
    model: ""                                       # Empty = use main chat model. Override with e.g. "google/gemini-3-flash-preview" for cheaper/faster compression.
    provider: "auto"                                # Provider: "auto", "openrouter", "nous", "codex", "main", etc.
    base_url: null                                  # Custom OpenAI-compatible endpoint (overrides provider)
```

Older configs with `compression.summary_model`, `compression.summary_provider`, and `compression.summary_base_url` are automatically migrated to `auxiliary.compression.*` on first load (config version 17) — no manual action needed.

`hygiene_hard_message_limit` is a gateway-only **pre-compression safety valve**. Runaway sessions with thousands of messages can hit model context limits before the normal percent-of-context threshold fires; when message count crosses this ceiling, Hermes forces compression regardless of token usage. Default `400` — raise it for platforms where very long sessions are normal, lower it to force more aggressive compression.

`protect_first_n` controls how many **non-system** head messages are pinned across every compaction. Default `3` — the opening user/assistant exchange survives every summarizer pass so the original goal stays visible. On long-running rolling-compaction sessions where the opening turn is no longer relevant, set `protect_first_n: 0` to pin nothing but the system prompt + summary + tail. The system prompt itself is always preserved regardless of this setting.

Editing `model.context_length` or any `compression.*` key in `config.yaml` on a running gateway takes effect on the next message — no gateway restart, no `/reset`, no session rotation required. The cached-agent signature includes these keys, so the gateway transparently rebuilds the agent on a change. API keys and tool/skill config still require the usual reload paths.

### Common setups and how the three knobs interact

Default (auto-detect) needs no configuration: `compression: {enabled: true, threshold: 0.50}` uses your main provider and main model. Override per-task for a cheaper model. The compression provider/endpoint interact as follows:

| `auxiliary.compression.provider` | `auxiliary.compression.base_url` | Result |
|---------------------|---------------------|--------|
| `auto` (default) | not set | Auto-detect best available provider |
| `nous` / `openrouter` / etc. | not set | Force that provider, use its auth |
| any | set | Use the custom endpoint directly (provider ignored) |

The summary model **must** have a context window at least as large as your main agent model's. The compressor sends the full middle section of the conversation to the summary model — if that model's window is smaller, the summarization call fails with a context-length error and the middle turns are **dropped without a summary**, losing conversation context silently. If you override the model, verify its context length meets or exceeds your main model's.

## Context Engine

The context engine controls how conversations are managed when approaching the model's token limit. The built-in `compressor` engine uses lossy summarization. Plugin engines can replace it with alternative strategies.

```yaml
context:
  engine: "compressor"    # default — built-in lossy summarization
  # engine: "lcm"         # a plugin engine (e.g., LCM for lossless context management) — must match the plugin's name
```

Plugin engines are **never auto-activated** — you must explicitly set `context.engine` to the plugin name. Available engines can be browsed and selected via `hermes plugins` → Provider Plugins → Context Engine. This single-select system is analogous to the one for memory plugins (see Memory Providers, SP05).

## Iteration Budget Pressure

When the agent works a complex task with many tool calls, it can burn through its iteration budget (default 90 turns) without realizing it's running low. Budget pressure automatically warns the model as it approaches the limit:

| Threshold | Level | What the model sees |
|-----------|-------|---------------------|
| **70%** | Caution | `[BUDGET: 63/90. 27 iterations left. Start consolidating.]` |
| **90%** | Warning | `[BUDGET WARNING: 81/90. Only 9 left. Respond NOW.]` |

Warnings are injected into the last tool result's JSON (as a `_budget_warning` field) rather than as separate messages — this preserves prompt caching and doesn't disrupt the conversation structure.

```yaml
agent:
  max_turns: 90                # Max iterations per conversation turn (default: 90)
  api_max_retries: 3           # Retries per provider before fallback engages (default: 3)
```

Budget pressure is enabled by default. When the budget is fully exhausted the CLI shows `⚠ Iteration budget reached (90/90) — response may be incomplete`, and if it runs out during active work the agent generates a summary of what was accomplished before stopping. `agent.api_max_retries` controls how many times Hermes retries a provider API call on transient errors (rate limits, connection drops, 5xx) **before** fallback-provider switching engages — default `3` (four attempts total); drop it to `0` so the first transient error on your primary immediately hands off to a configured fallback instead of churning retries against the flaky endpoint.

### API Timeouts

Hermes has separate timeout layers for streaming, plus a stale detector for non-streaming calls. The stale detectors auto-adjust for local providers only when you leave them at their implicit defaults.

| Timeout | Default | Local providers | Config / env |
|---------|---------|----------------|--------------|
| Socket read timeout | 120s | Auto-raised to 1800s | `HERMES_STREAM_READ_TIMEOUT` |
| Stale stream detection | 180s | Auto-disabled | `HERMES_STREAM_STALE_TIMEOUT` |
| Stale non-stream detection | 300s | Auto-disabled when left implicit | `providers.<id>.stale_timeout_seconds` or `HERMES_API_CALL_STALE_TIMEOUT` |
| API call (non-streaming) | 1800s | Unchanged | `providers.<id>.request_timeout_seconds` / `timeout_seconds` or `HERMES_API_TIMEOUT` |

The **socket read timeout** controls how long httpx waits for the next chunk of data; local LLMs can take minutes for prefill on large contexts before the first token, so Hermes raises this to 30 minutes when it detects a local endpoint (an explicit `HERMES_STREAM_READ_TIMEOUT` always wins). The **stale stream detection** kills connections that receive SSE keep-alive pings but no actual content, disabled entirely for local providers. The **stale non-stream detection** kills non-streaming calls that produce no response for too long, disabled by default on local endpoints to avoid false positives during long prefills unless you set an explicit value.

## Context Pressure Warnings

Separate from iteration budget pressure, context pressure tracks how close the conversation is to the **compaction threshold** — the point where compression fires to summarize older messages.

| Progress | Level | What happens |
|----------|-------|-------------|
| **≥ 60%** to threshold | Info | CLI shows a cyan progress bar; gateway sends an informational notice |
| **≥ 85%** to threshold | Warning | CLI shows a bold yellow bar; gateway warns compaction is imminent |

In the CLI it appears as a progress bar in the tool output feed (`◐ context ████████████░░░░░░░░ 62% to compaction  48k threshold (50%) · approaching compaction`); on messaging platforms a plain-text notice is sent. If auto-compression is disabled, the warning tells you context may be truncated instead. Context pressure is automatic — no configuration needed; it fires purely as a user-facing notification and does **not** modify the message stream or inject anything into the model's context.

## File Read Safety

Controls how much content a single `read_file` call can return. Reads that exceed the limit are rejected with an error telling the agent to use `offset` and `limit` for a smaller range, preventing a single read of a minified JS bundle or large data file from flooding the context window.

```yaml
file_read_max_chars: 100000  # default — ~25-35K tokens

# Large context model (200K+)
file_read_max_chars: 200000

# Small local model (16K context)
file_read_max_chars: 30000
```

The agent also deduplicates file reads automatically — if the same file region is read twice and the file hasn't changed, a lightweight stub is returned instead of re-sending the content. This **resets on context compression** so the agent can re-read files after their content is summarized away.

## Tool Output Truncation Limits

Three related caps control how much raw output a tool can return before Hermes truncates it:

```yaml
tool_output:
  max_bytes: 50000        # terminal output cap (chars)
  max_lines: 2000         # read_file pagination cap
  max_line_length: 2000   # per-line cap in read_file's line-numbered view
```

- **`max_bytes`** — When a `terminal` command produces more than this many characters of combined stdout/stderr, Hermes keeps the first 40% and last 60% and inserts a `[OUTPUT TRUNCATED]` notice between them. Default `50000` (≈12-15K tokens).
- **`max_lines`** — Upper bound on the `limit` parameter of a single `read_file` call; requests above this are clamped so one read can't flood the context window. Default `2000`.
- **`max_line_length`** — Per-line cap when `read_file` emits the line-numbered view; longer lines are truncated to this many chars followed by `... [truncated]`. Default `2000`.

Raise the limits on large-context models that can afford more raw output per call; lower them for small-context models to keep tool results compact.

## Global Toolset Disable

To suppress specific toolsets across the CLI and every gateway platform in one place, list their names under `agent.disabled_toolsets`:

```yaml
agent:
  disabled_toolsets:
    - memory       # hide memory tools + MEMORY_GUIDANCE injection
    - web          # no web_search / web_extract anywhere
```

This applies **after** per-platform tool config (`platform_toolsets` written by `hermes tools`), so a toolset listed here is always removed — even if a platform's saved config still lists it. Use it as a single "turn X off everywhere" switch rather than editing 15+ platform rows in the `hermes tools` UI. Leaving the list empty, or omitting the key, is a no-op.

## Git Worktree Isolation

Enable isolated git worktrees for running multiple agents in parallel on the same repo via the top-level key `worktree: true` (always create a worktree, same as `hermes -w`); the default `worktree: false` creates one only when the `-w` flag is passed.

When enabled, each CLI session creates a fresh worktree under `.worktrees/` with its own branch. Agents can edit files, commit, push, and create PRs without interfering with each other. Clean worktrees are removed on exit; dirty ones are kept for manual recovery. You can list gitignored files to copy into worktrees via `.worktreeinclude` in your repo root (e.g. `.env`, `.venv/`, `node_modules/`). Worktree internals are documented in SP03.

**Source**: `inbox/hermes_agent_docs/user-guide/configuration.md` · https://hermes-agent.nousresearch.com/docs/user-guide/configuration
**Last Updated**: 2026-06-19
**Status**: Active
