---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - system_prompt
keywords:
  - openclaw system prompt
  - buildAgentSystemPrompt
  - prompt assembly layers
  - provider prompt contributions
  - prompt cache boundary
  - prompt modes minimal
  - prompt snapshots
  - fixed prompt sections
topics:
  - OpenClaw
  - System Prompt
language: markdown
date of note: 2026-06-23
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/system-prompt
access_control_group: ["general"]
---

# OpenClaw — System Prompt Structure & Assembly

## Overview

This note models *what* the OpenClaw system prompt contains and *how* it is assembled — the first half of the `concepts/system-prompt` page (split from the workspace-injection / time / skills / documentation procedure, which lives in [oc_concepts_system_prompt_injection](oc_concepts_system_prompt_injection.md)). It covers the OpenClaw-owned prompt, the three-layer assembly path, provider prompt contributions, the fixed Structure sections, the per-run prompt modes, and the committed prompt snapshots.

## OpenClaw-Owned Prompt and Three-Layer Assembly

OpenClaw builds a custom system prompt for every agent run; the prompt is **OpenClaw-owned** and does not use a runtime default prompt. Assembly has three layers:

- **`buildAgentSystemPrompt`** renders the prompt from explicit inputs. It is meant to stay a pure renderer and should not read global config directly.
- **`resolveAgentSystemPromptConfig`** resolves config-backed prompt knobs such as owner display, TTS hints, model aliases, memory citation mode, and sub-agent delegation mode for a specific agent.
- **Runtime adapters** (embedded, CLI, command/export previews, compaction) gather live facts — tools, sandbox state, channel capabilities, context files, and provider prompt contributions — then call the configured prompt facade.

This keeps exported/debug prompt surfaces aligned with live runs without turning every runtime-specific detail into one monolithic builder.

## Provider Contributions and Model Overlays

Provider plugins can contribute cache-aware prompt guidance without replacing the full OpenClaw-owned prompt. The provider runtime can replace a small set of named core sections (`interaction_style`, `tool_call_style`, `execution_bias`), inject a **stable prefix** above the prompt cache boundary, and inject a **dynamic suffix** below it. Provider-owned contributions are for model-family-specific tuning; legacy `before_prompt_build` prompt mutation is kept for compatibility or truly global changes, not normal provider behavior. The OpenAI GPT-5 family overlay, for example, keeps the core execution rule small and adds model-specific guidance for persona latching, concise output, tool discipline, parallel lookup, deliverable coverage, verification, missing context, and terminal-tool hygiene.

## Fixed Structure Sections

The prompt is intentionally compact and uses fixed sections: **Tooling** (structured-tool source-of-truth reminder plus runtime tool-use guidance), **Execution Bias** (act in-turn, continue until done or blocked, recover from weak tool results, check mutable state live, verify before finalizing), **Safety** (a short guardrail reminder against power-seeking or bypassing oversight), **Skills** (when available — how to load skill instructions on demand), **OpenClaw Control** (prefer the `gateway` tool for config/restart work; avoid inventing CLI commands), **OpenClaw Self-Update** (inspect config with `config.schema.lookup`, patch with `config.patch`, replace with `config.apply`, run `update.run` only on explicit request; the `gateway` tool refuses to rewrite `tools.exec.ask` / `tools.exec.security` and their legacy `tools.bash.*` aliases), **Workspace**, **Documentation**, **Workspace Files (injected)**, **Sandbox** (when enabled), **Current Date & Time** (time zone only — cache-stable), **Assistant Output Directives**, **Heartbeats**, **Runtime**, and **Reasoning** (visibility level + `/reasoning` toggle).

The Tooling section also carries runtime guidance for long-running work: use cron for future follow-up instead of `exec` sleep loops / `yieldMs` tricks / repeated `process` polling; use `exec`/`process` only for commands that start now and run in the background; rely on the push-based wake path when automatic completion wake is enabled; use `process` to inspect a running command; prefer `sessions_spawn` for larger tasks (completion is push-based and auto-announces); and never poll `subagents list` / `sessions_list` to wait for completion. When the experimental `update_plan` tool is enabled, Tooling tells the model to use it only for non-trivial multi-step work, keep exactly one `in_progress` step, and avoid repeating the whole plan after each update. Safety guardrails here are **advisory** — they guide behavior but do not enforce policy; tool policy, exec approvals, sandboxing, and channel allowlists are the hard enforcement, and operators can disable the advisory text by design.

## Cache Boundary and Section Ordering

OpenClaw keeps large stable content — including **Project Context** — above the internal prompt cache boundary, and appends volatile channel/session sections (Control UI embed guidance, **Messaging**, **Voice**, **Group Chat Context**, **Reactions**, **Heartbeats**, **Runtime**) below it, so local backends with prefix caches can reuse the stable workspace prefix across channel turns. Tool descriptions should likewise avoid embedding current channel names when the accepted schema already carries that runtime detail. `agents.defaults.subagents.delegationMode` can strengthen the delegation guidance: the default `suggest` keeps the baseline nudge, while `prefer` adds a dedicated **Sub-Agent Delegation** section telling the main agent to act as a responsive coordinator and push anything beyond a direct reply through `sessions_spawn` (prompt-only; tool policy still controls availability). On channels with native approval cards/buttons, the runtime prompt tells the agent to rely on the native approval UI first and include a manual `/approve` command only when the tool result says chat approvals are unavailable.

## Prompt Modes

OpenClaw can render smaller system prompts for sub-agents. The runtime sets a `promptMode` per run (not a user-facing config):

- **`full`** (default): includes all sections above.
- **`minimal`** (sub-agents): omits **Memory Recall**, **OpenClaw Self-Update**, **Model Aliases**, **User Identity**, **Assistant Output Directives**, **Messaging**, **Silent Replies**, and **Heartbeats**; Tooling, **Safety**, **Skills** (when supplied), Workspace, Sandbox, Current Date & Time (when known), Runtime, and injected context stay available. Extra injected prompts are labeled **Subagent Context** instead of **Group Chat Context**.
- **`none`**: returns only the base identity line.

For channel auto-reply runs, OpenClaw omits the generic **Silent Replies** section when direct, group, or message-tool-only context owns the visible-reply contract; only the old automatic group/channel mode shows `NO_REPLY`.

## Prompt Snapshots

OpenClaw keeps committed prompt snapshots for the Codex runtime happy path under `test/fixtures/agents/prompt-snapshots/codex-runtime-happy-path/`. They render selected app-server thread/turn params plus a reconstructed model-bound prompt layer stack for Telegram direct, Discord group, and heartbeat turns, including a pinned Codex `gpt-5.5` model prompt fixture, the Codex happy-path permission developer text, OpenClaw developer instructions, turn-scoped collaboration-mode instructions, user turn input, and references to the dynamic tool specs. Refresh the pinned Codex model fixture with `pnpm prompt:snapshots:sync-codex-model` (it looks for `$CODEX_HOME/models_cache.json`, then `~/.codex/models_cache.json`, then the maintainer checkout `~/code/codex/codex-rs/models-manager/models.json`; `--catalog <path>` overrides). These snapshots are not a byte-for-byte raw OpenAI request capture — Codex can add runtime-owned context (`AGENTS.md`, environment context, memories, app/plugin instructions, Default collaboration-mode instructions) inside its runtime after OpenClaw sends thread/turn params. Regenerate with `pnpm prompt:snapshots:gen` and verify drift with `pnpm prompt:snapshots:check`; CI runs the drift check in the boundary shard.

**Source**: OpenClaw documentation — `concepts/system-prompt` (structure/assembly half; mirror `inbox/openclaw_docs/concepts/system-prompt.md`)
**Last Updated**: 2026-06-23
**Status**: Active
