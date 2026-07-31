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

## Related Notes

### Related Notes (Claude Code Series)
- [Agent SDK — The Agent Loop](cc_agent_sdk_agent_loop.md) — relevance: the loop these options bound; introduces what a *turn* is and first presents `max_turns`/`max_budget_usd`. This note is the option reference that the loop note defers to.
- [Agent SDK — Tool Execution](cc_agent_sdk_tool_execution.md) — relevance: how `permission_mode` combines with `allowed_tools`/`disallowed_tools` to decide which tool calls actually run — the action half of the same loop these controls shape.
- [Agent SDK — Handling the Result and Loop Hooks](cc_agent_sdk_result_and_hooks.md) — relevance: documents the `error_max_turns`/`error_max_budget_usd` `ResultMessage` subtypes returned exactly when the turn/budget caps in this note are hit.
- [Claude Agent SDK — Permission Modes](cc_sdk_permission_modes.md) — relevance: the dedicated concept note for the six-mode `permission_mode` spectrum summarized here, including the subagent-inheritance caveat and where the mode sits in the evaluation pipeline.
- [`ClaudeAgentOptions` and Config Types (Python)](cc_sdk_python_options_and_config_types.md) — relevance: the master Python dataclass that carries `max_turns`, `max_budget_usd`, `permission_mode`, `model`, and the `EffortLevel`/`ThinkingConfig` types this note configures.
- [Agent SDK (TypeScript) — The `Options` Configuration Object](cc_sdk_typescript_options.md) — relevance: the TypeScript counterpart exposing `maxTurns`/`maxBudgetUsd`, `permissionMode`, effort, and `model` — the camelCase forms of the same loop controls.
- [Effort Level and Extended Thinking](cc_effort_level_and_thinking.md) — relevance: expands the `effort` dial (low→max plus `ultracode`) and the separate extended-thinking toggle, the same effort-vs-thinking distinction this note draws.
- [Model Selection](cc_model_selection.md) — relevance: details the `model` field — alias vs explicit name, provider/account resolution — that this note's Model section points to for picking a faster/cheaper loop model.

### Related Notes (Out-of-Series)
- [Claude Code](../../term_dictionary/term_claude_code.md) — relevance: loop controls are fields on `ClaudeAgentOptions` for the Claude-Code-derived loop; the product term anchors the options surface.
- [Agent Orchestration](../../term_dictionary/term_agent_orchestration.md) — relevance: `max_turns`/`max_budget_usd`/effort/model are the knobs for orchestrating how far, how deep, and how expensively the loop runs — the orchestration controls this term frames.
- [Graduated Trust](../../term_dictionary/term_graduated_trust.md) — relevance: the permission-mode table (`default`/`acceptEdits`/`plan`/`dontAsk`/`auto`/`bypassPermissions`) is the graduated-trust spectrum from prompt-everything to run-everything this term defines.
- [Chain-of-Thought](../../term_dictionary/term_chain_of_thought.md) — relevance: the `effort` levels (low→max) control how much reasoning Claude applies per turn, and the note distinguishes effort from visible extended-thinking chain-of-thought blocks — the term grounds that reasoning-depth dimension.
- [Context Engineering](../../term_dictionary/term_context_engineering.md) — relevance: lower effort and turn/budget caps are context-and-cost engineering levers; the note's guidance to tune effort/turns per task is applied context engineering.
- [Function Calling / Tool Use](../../term_dictionary/term_function_calling.md) — relevance: `max_turns` "counts tool-use turns only," so the budget controls are denominated in function-calling round trips this term names.
- [Autonomous Coding Agents](../../term_dictionary/term_autonomous_coding_agents.md) — relevance: budgets and turn caps exist to keep autonomous agents from "running long on open-ended prompts"; the controls bound exactly the autonomy this term defines.
- [Tool: Strands Agents — Open-Source AI Agents SDK](../../tools/tool_strands_agents.md) — relevance: a sibling agent SDK (AWS, model-driven orchestration) to compare against — Strands lets the FM decide step sequencing, while this note shows Claude's SDK exposing explicit turn/budget/effort caps over that same loop.
- [Project: Agent Platform](../../../projects/project_agent_platform.md) — relevance: the platform's human-in-the-loop (HITL) quality gate is the platform-level analogue of this note's `permission_mode` approval spectrum, and its dynamic step decomposition is what `max_turns`/`max_budget_usd` would bound.
- [Agentic AI Golden Path — Security Guidance](../org_docs/org_agentic_golden_path_security.md) — relevance: bounding autonomy via permission mode, turn caps, and budget limits is a concrete control for the agent-misuse/over-action risks this organizational security-review guidance asks builders to mitigate.
- [AgentCore Managed Harness [Preview]](../aws_bedrock_agentcore/bedrock_agentcore_harness.md) — relevance: a managed, config-based agent harness that abstracts the same orchestration/model-flexibility concerns this note tunes explicitly through `ClaudeAgentOptions`.

**Source**: https://code.claude.com/docs/en/agent-sdk/agent-loop
**Last Updated**: 2026-06-13
**Status**: Active
