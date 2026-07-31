---
tags:
  - resource
  - documentation
  - claude_code
  - agentic_loop
  - architecture
keywords:
  - agentic loop
  - gather context take action verify
  - agentic harness
  - models and tools
  - interrupt and steer
  - course-correcting
  - claude code architecture
topics:
  - Claude Code
  - Agentic Loop
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/how-claude-code-works
access_control_group: ["general"]
---

# Claude Code — The Agentic Loop

## Overview

Claude Code works through an **agentic loop**: when given a task, it cycles through three blended phases — **gather context**, **take action**, and **verify results** — using tools throughout. The loop adapts to the task (a codebase question may need only context gathering; a bug fix cycles all three phases repeatedly), and Claude chains dozens of actions together, deciding each step from what it learned in the previous one and course-correcting along the way. The loop is powered by two components — **models** that reason and **tools** that act — with Claude Code serving as the **agentic harness** around the model.

## The Three Phases

Claude works through three phases that blend together, using tools in each:

1. **Gather context** — e.g. searching files to understand the code.
2. **Take action** — e.g. editing files to make changes.
3. **Verify results** — e.g. running tests to check its work.

The loop adapts to what you ask: a question about your codebase might only need context gathering; a bug fix cycles through all three phases repeatedly; a refactor might involve extensive verification. Claude decides what each step requires based on what it learned from the previous step.

## You Are Part of the Loop

You can **interrupt at any point** to steer Claude in a different direction, provide additional context, or ask it to try a different approach. Claude works autonomously but stays responsive to your input.

## Models and Tools

The agentic loop is powered by two components:

- **Models that reason** — Claude Code uses Claude models to read code in any language, understand how components connect, and figure out what needs to change. For complex tasks it breaks work into steps, executes them, and adjusts based on what it learns. Multiple models offer different tradeoffs (Sonnet handles most coding tasks; Opus provides stronger reasoning for complex architectural decisions), switchable with `/model` mid-session or `claude --model <name>`. When the docs say "Claude chooses" or "Claude decides," it is the model reasoning.
- **Tools that act** — without tools Claude can only respond with text; with tools it can read code, edit files, run commands, search the web, and interact with external services. Each tool use returns information that feeds back into the loop, informing the next decision. (The five built-in tool categories are detailed in [Built-in Tools](cc_built_in_tools.md); the full list is the [tools reference](cc_built_in_tools.md).)

## The Agentic Harness

Claude Code serves as the **agentic harness** around Claude: it provides the tools, context management, and execution environment that turn a language model into a capable coding agent. The built-in tools are the foundation, and an extension layer sits on top of the core loop — skills extend what Claude knows, MCP connects external services, hooks automate workflows, and subagents offload tasks (see [Extending Claude Code](cc_extending_claude_code.md)).

**Source**: https://code.claude.com/docs/en/how-claude-code-works
**Last Updated**: 2026-06-13
**Status**: Active
