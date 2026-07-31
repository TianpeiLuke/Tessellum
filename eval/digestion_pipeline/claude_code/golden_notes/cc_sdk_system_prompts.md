---
tags:
  - resource
  - documentation
  - claude_code
  - agent_sdk
  - system_prompts
keywords:
  - claude_code preset
  - custom system prompt
  - minimal default
  - append to preset
  - decide on a starting point
  - different from claude code
  - compare four approaches
  - sdk system prompt
topics:
  - Claude Code
  - Agent SDK
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts
access_control_group: ["general"]
---

# Claude Code Agent SDK — System Prompts: Choosing a Starting Point

## Overview

A **system prompt** is the initial instruction set that shapes how Claude behaves, what it can do, and how it responds throughout a conversation. The Claude Code Agent SDK exposes three starting points for it — a **minimal default**, the **`claude_code` preset** (the full CLI prompt), and a **custom string** — and lets you layer four customization methods (CLAUDE.md, output styles, `append`, custom prompt) on top. This note covers *how to choose*: the three starting points, the decision table for matching a starting point to your agent, what "different from Claude Code" means, and the four-method comparison matrix. The hands-on *how to apply* each method (loading CLAUDE.md, creating output styles, `append`, prompt-cache reuse, combining) is the sibling note [cc_sdk_customize_system_prompt](cc_sdk_customize_system_prompt.md).

The guiding rule: start from the `claude_code` preset for CLI- or IDE-like coding tools where a human watches and steers the work, and write your own prompt for agents with a different surface, identity, or permission model.

## How system prompts work

The Agent SDK has three starting points for the system prompt:

- **Minimal default** — when you don't set `systemPrompt` (TypeScript) or `system_prompt` (Python), the SDK uses a minimal prompt that covers tool calling but omits Claude Code's coding guidelines, response style, and project context. This differs from `claude -p`, which uses the full Claude Code prompt by default. If you're migrating from the CLI and want matching behavior, set the `claude_code` preset.
- **`claude_code` preset** — the full system prompt the Claude Code CLI uses: tool usage instructions, code style and formatting guidelines, response tone and verbosity rules, security and safety instructions, and context about the working directory and environment. Set `systemPrompt: { type: "preset", preset: "claude_code" }` in TypeScript or `system_prompt={"type": "preset", "preset": "claude_code"}` in Python, optionally with `append` to add your own instructions on the end.
- **Custom string** — a prompt you write yourself. The SDK sends only what you provide.

### Decide on a starting point

The deciding factor is how closely your agent resembles Claude Code: a coding agent operating in a repository, with a human watching streaming output and steering the work. The further your product is from that, the more you'll want to write your own prompt.

| You're building | Use | What you get |
| :--- | :--- | :--- |
| A CLI or IDE-like coding tool where a human watches and steers, and Claude Code's defaults are what you want | `claude_code` preset | The full Claude Code prompt: tool guidance, safety rules, terminal-friendly responses, repo-convention awareness |
| The same kind of tool, plus product-specific rules like coding standards, output format, or domain context | `claude_code` preset with `append` | Everything above, with your instructions added after the preset. Nothing is removed, so this is the lowest-risk customization |
| An agent with a different surface, identity, or permission model, or a non-coding agent | Custom prompt string | Only what you write. You take responsibility for replacing the tool guidance and safety instructions your agent still needs |
| A thin tool-calling loop with no agent persona, where you supply all behavior in the user prompt | No `systemPrompt` option | The minimal default: tool-calling support and nothing else |

"Different from Claude Code" usually means one of the following:

- **Different surface** — the output isn't read in a terminal by the person who triggered it. Chat UIs, structured-output consumers, and non-coding automation each need a prompt that matches how their output is rendered and reviewed. Unattended coding automation, like a CI job that fixes lint errors or reviews diffs, still fits the preset because the work itself is what the preset is written for.
- **Different identity** — the agent shouldn't present itself as Claude Code. A support bot, a data-analysis assistant, or any domain-specific agent needs its own name, scope, and persona.
- **Different permission model** — the agent runs autonomously without a human approving each step, or operates on a narrow set of resources. Claude Code's prompt assumes a human is in the loop with access to a full toolset.
- **Non-coding tasks** — most of Claude Code's prompt is coding guidance. For research, content, or operations agents, that guidance competes with the instructions you actually need.

## Compare the four approaches

The four customization methods — CLAUDE.md, output styles, `systemPrompt` with `append`, and a custom `systemPrompt` — differ in where they live, how they're shared, and what they preserve from the `claude_code` preset. The matrix below shows what each method preserves; the procedure for applying each is in [cc_sdk_customize_system_prompt](cc_sdk_customize_system_prompt.md).

| Feature | CLAUDE.md | Output Styles | `systemPrompt` with append | Custom `systemPrompt` |
| --- | --- | --- | --- | --- |
| **Persistence** | Per-project file | Saved as files | Session only | Session only |
| **Reusability** | Per-project | Across projects | Code duplication | Code duplication |
| **Management** | On filesystem | CLI + files | In code | In code |
| **Default tools** | Preserved | Preserved | Preserved | Lost (unless included) |
| **Built-in safety** | Maintained | Maintained | Maintained | Must be added |
| **Environment context** | Automatic | Automatic | Automatic | Must be provided |
| **Customization level** | Additions only | Replace or extend default | Additions only | Complete control |
| **Version control** | With project | Yes | With code | With code |
| **Scope** | Project-specific | User or project | Code session | Code session |

The key contrast: the preset (with or without `append`) and CLAUDE.md/output styles preserve the default tools, built-in safety instructions, and environment context automatically, whereas a fully custom `systemPrompt` gives you complete control but drops the default tools (unless re-included), requires safety to be added back, and requires environment context to be provided. "With append" means using `systemPrompt: { type: "preset", preset: "claude_code", append: "..." }` in TypeScript or `system_prompt={"type": "preset", "preset": "claude_code", "append": "..."}` in Python. CLAUDE.md does not change the system prompt itself — the SDK injects its content into the conversation as project context.

**Source**: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts
**Last Updated**: 2026-06-13
**Status**: Active
