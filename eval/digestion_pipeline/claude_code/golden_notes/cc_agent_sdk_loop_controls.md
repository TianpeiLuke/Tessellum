---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - loop_controls
keywords:
  - control how the loop runs
  - max_turns
  - max_budget_usd
  - effort level
  - permission mode
  - claudeagentoptions
  - error subtypes
  - model selection
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/agent-loop
access_control_group: ["general"]
---

# Agent SDK — Controlling How the Loop Runs

## Overview

The Agent SDK lets you bound and shape the agent loop through four families of options on [`ClaudeAgentOptions`](https://code.claude.com/docs/en/agent-sdk/python#claudeagentoptions) (Python) / `Options` (TypeScript): how many **turns** the loop may take, how much it may **cost**, how deeply Claude **reasons** (effort), and whether tools require **approval** before running (permission mode). A fifth field, `model`, pins which model the loop uses. These knobs are how you keep an autonomous agent from running long on open-ended prompts and how you trade latency and token cost for reasoning depth or safety.

This note documents the option reference for those controls. The error subtypes that the loop returns when a turn or budget limit is hit are handled in [`cc_agent_sdk_result_and_hooks`](cc_agent_sdk_result_and_hooks.md), and the full permission rule syntax and precedence order live in the SDK [Permissions](https://code.claude.com/docs/en/agent-sdk/permissions) reference.

## Turns and budget

A *turn* is one tool-use round trip inside the loop, and you can cap how many of them run and how much the session costs:

| Option | What it controls | Default |
| :--- | :--- | :--- |
| Max turns (`max_turns` / `maxTurns`) | Maximum tool-use round trips | No limit |
| Max budget (`max_budget_usd` / `maxBudgetUsd`) | Maximum cost before stopping | No limit |

`max_turns` counts **tool-use turns only** — the final text-only response does not count against it. When either limit is hit, the SDK returns a `ResultMessage` with a corresponding error subtype (`error_max_turns` or `error_max_budget_usd`). See [`cc_agent_sdk_result_and_hooks`](cc_agent_sdk_result_and_hooks.md) for how to check these subtypes.

Without limits, the loop runs until Claude finishes on its own, which is fine for well-scoped tasks but can run long on open-ended prompts ("improve this codebase"). Setting a budget is a good default for production agents.

## Effort level

The `effort` option controls how much reasoning Claude applies. Lower effort levels use fewer tokens per turn and reduce cost. Not all models support the effort parameter.

| Level | Behavior | Good for |
| :--- | :--- | :--- |
| `"low"` | Minimal reasoning, fast responses | File lookups, listing directories |
| `"medium"` | Balanced reasoning | Routine edits, standard tasks |
| `"high"` | Thorough analysis | Refactors, debugging |
| `"xhigh"` | Extended reasoning depth | Coding and agentic tasks; recommended on Fable 5 and Opus 4.7+ |
| `"max"` | Maximum reasoning depth | Multi-step problems requiring deep analysis |

If you don't set `effort`, both SDKs leave the parameter unset and defer to the model's default behavior.

`effort` trades latency and token cost for reasoning depth *within each response*. [Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) is a separate feature that produces visible chain-of-thought blocks in the output. They are independent: you can set `effort: "low"` with extended thinking enabled, or `effort: "max"` without it.

Use lower effort for agents doing simple, well-scoped tasks (like listing files or running a single grep) to reduce cost and latency. Set `effort` in the top-level `query()` options for the whole session, or per subagent with the `effort` field on `AgentDefinition` to override the session level.

## Permission mode

The permission mode option (`permission_mode` in Python, `permissionMode` in TypeScript) controls whether the agent asks for approval before using tools. It governs what happens to tools that are **not** covered by allow or deny rules:

| Mode | Behavior |
| :--- | :--- |
| `"default"` | Tools not covered by allow rules trigger your approval callback; no callback means deny |
| `"acceptEdits"` | Auto-approves file edits and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`, etc.); other Bash commands follow default rules |
| `"plan"` | Claude explores and plans without editing your source files; file edits are never auto-approved and prompt through your `canUseTool` callback |
| `"dontAsk"` | Never prompts. Tools pre-approved by permission rules run, everything else is denied |
| `"auto"` (TypeScript only) | Uses a model classifier to approve or deny each tool call |
| `"bypassPermissions"` | Runs all allowed tools without asking, unless an explicit `ask` rule matches. Cannot be used when running as root on Unix. Use only in isolated environments where the agent's actions cannot affect systems you care about |

For interactive applications, use `"default"` with a tool approval callback to surface approval prompts. For autonomous agents on a dev machine, `"acceptEdits"` auto-approves file edits and common filesystem commands while still gating other `Bash` commands behind allow rules. Reserve `"bypassPermissions"` for CI, containers, or other isolated environments. See [Permissions](https://code.claude.com/docs/en/agent-sdk/permissions) for full details, and [`cc_agent_sdk_tool_execution`](cc_agent_sdk_tool_execution.md) for how permission mode interacts with `allowed_tools`/`disallowed_tools`.

## Model

If you don't set `model`, the SDK uses Claude Code's default, which depends on your authentication method and subscription. Set it explicitly (for example, `model="claude-sonnet-4-6"`) to pin a specific model or to use a smaller model for faster, cheaper agents. See [models](https://platform.claude.com/docs/en/about-claude/models) for available IDs.

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
