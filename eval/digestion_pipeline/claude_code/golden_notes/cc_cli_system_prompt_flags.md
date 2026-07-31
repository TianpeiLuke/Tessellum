---
tags:
  - resource
  - documentation
  - claude_code
  - cli_reference
  - system_prompt
keywords:
  - system prompt flags
  - append system prompt
  - replace system prompt
  - system-prompt-file
  - per-invocation customization
  - default identity
  - coding assistant prompt
topics:
  - Claude Code
  - CLI reference
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/cli-reference
access_control_group: ["general"]
---

# Claude Code — System Prompt Flags (Append vs Replace)

## Overview

Claude Code provides **four CLI flags for customizing the system prompt**, and the central decision they pose is whether to **append** to Claude Code's default identity or **replace** it entirely. The argument the docs make: choose based on whether Claude Code's default identity (a coding assistant with built-in tool guidance, safety instructions, and coding conventions) still fits your task. Append when Claude should stay that coding assistant but also follow extra rules; replace when the surface, identity, or permission model differs from Claude Code's. All four flags apply only to the current invocation — persistent personas and project conventions belong elsewhere.

## The four flags

All four work in both interactive and non-interactive modes:

| Flag                          | Behavior                                    | Example                                                 |
| :---------------------------- | :------------------------------------------ | :------------------------------------------------------ |
| `--system-prompt`             | Replaces the entire default prompt          | `claude --system-prompt "You are a Python expert"`      |
| `--system-prompt-file`        | Replaces with file contents                 | `claude --system-prompt-file ./prompts/review.txt`      |
| `--append-system-prompt`      | Appends to the default prompt               | `claude --append-system-prompt "Always use TypeScript"` |
| `--append-system-prompt-file` | Appends file contents to the default prompt | `claude --append-system-prompt-file ./style-rules.txt`  |

The two replacement flags (`--system-prompt`, `--system-prompt-file`) take text inline or from a file; the two append flags add to whatever the default prompt is, inline or from a file.

## Mutual exclusivity and combination

`--system-prompt` and `--system-prompt-file` are **mutually exclusive** — you cannot replace with both inline text and a file in the same invocation. The append flags **can be combined with either replacement flag**, so you may replace the base prompt and still append additional rules on top of the replacement.

## The decision rule: append vs replace

Choose based on whether Claude Code's default identity still fits your task:

- **Use an append flag** when Claude should remain a coding assistant that also follows your extra rules: per-invocation instructions, output formatting, or domain context for a `-p` script. Appending **preserves the default tool guidance, safety instructions, and coding conventions**, so you only supply what differs.
- **Use a replacement flag** when the surface, identity, or permission model differs from Claude Code's — like a non-coding agent in a pipeline that no human watches. Replacing **drops all of the default prompt**, including tool guidance and safety instructions, so you take responsibility for whatever your task still needs.

The trade-off is therefore one of inheritance versus control: appending inherits the harness's safety and tool guidance for free; replacing buys full control of identity at the cost of having to re-supply anything the task still requires.

## Scope: per-invocation only

These flags apply **only to the current invocation**. The docs route durable needs elsewhere:

- For **persistent personas** you can switch between and share across a project, use [output styles](https://code.claude.com/docs/en/output-styles).
- For **project conventions** Claude should always follow, use [CLAUDE.md](https://code.claude.com/docs/en/memory).

The [Agent SDK guide on system prompts](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts) covers the same append-vs-replace decision in more depth.

**Source**: https://code.claude.com/docs/en/cli-reference
**Last Updated**: 2026-06-13
**Status**: Active
