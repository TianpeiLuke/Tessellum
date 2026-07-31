---
tags:
  - resource
  - documentation
  - claude_code
  - context
  - extensions
keywords:
  - context cost by feature
  - context loading strategy
  - claude.md every request
  - skill descriptions at session start
  - mcp tool names deferred schemas
  - subagent isolated context window
  - hook zero context cost
  - disable-model-invocation
topics:
  - Claude Code
  - Context Costs
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/features-overview
access_control_group: ["general"]
---

# Claude Code — Context Cost by Feature

## Overview

Every extension you add to Claude Code consumes some of Claude's context. Too much can fill the context window, but it can also add noise that makes Claude less effective — skills may not trigger correctly, or Claude may lose track of your conventions. Understanding the trade-offs helps you build an effective setup. The key distinction is *when* each feature loads and *what* loads into context at that point. CLAUDE.md is the only feature whose full content rides along in every request; the others load lazily (descriptions, names, or nothing) and pull in their full content only when actually used.

## Context cost by feature

Each feature has a different loading strategy and context cost:

- **CLAUDE.md** — loads at **session start**; its **full content** loads; the cost applies to **every request**.
- **Skills** — load at **session start and when used**: descriptions load at start, full content loads when used. Cost is **low** (descriptions every request).
- **MCP servers** — load at **session start**: tool names load, full schemas load on demand. Cost is **low until a tool is used**.
- **Code intelligence** — loads **after file edits and on demand**: diagnostics after edits, symbol locations on lookup. Cost is **low** and it reduces file reads elsewhere.
- **Subagents** — load **when spawned**: a fresh context with specified skills. Cost is **isolated from the main session**.
- **Hooks** — load **on trigger**: nothing loads (they run externally). Cost is **zero, unless the hook returns additional context**.

By default, skill descriptions load at session start so Claude can decide when to use them. Setting `disable-model-invocation: true` in a skill's frontmatter hides it from Claude entirely until you invoke it manually, reducing its context cost to zero for skills you only trigger yourself. For a skill you didn't write, set `skillOverrides` in settings to do the same without editing its file.

## Understand how features load

Each feature loads at a different point in the session:

- **CLAUDE.md** — loads at session start. The full content of all CLAUDE.md files (managed, user, and project levels) loads. Claude reads CLAUDE.md from your working directory up to the root and discovers nested files in subdirectories as it accesses them. (Tip: keep CLAUDE.md under 200 lines; move reference material to skills, which load on-demand.)
- **Skills** — loading depends on configuration. By default, descriptions load at session start and full content loads when used; for user-only skills (`disable-model-invocation: true`), nothing loads until you invoke them. Claude matches your task against skill descriptions to decide which are relevant. In subagents, skills listed in the `skills` field are fully preloaded at launch rather than loaded on demand.
- **MCP servers** — load at session start: tool names from connected servers load, while full JSON schemas stay deferred until Claude needs a specific tool. Tool search is on by default, so idle MCP tools consume minimal context.
- **Code intelligence** — loads after file edits and on demand: type errors and warnings after each edit, plus definition, reference, and type information when Claude looks up a symbol. Symbol lookups often replace broad file reads, so net context use can go down.
- **Subagents** — load on demand, when you or Claude spawns one. The fresh, isolated context contains the agent's own system prompt (not the full Claude Code system prompt), full content of skills listed in its `skills:` field, CLAUDE.md and git status (except the built-in Explore and Plan agents omit both), and whatever the lead agent passes in the prompt. Subagents don't inherit your conversation history or invoked skills.
- **Hooks** — fire on trigger at specific lifecycle events (tool execution, session boundaries, prompt submission, permission requests, compaction). Nothing loads by default — hooks execute outside the main conversation — so cost is zero unless the hook returns output added as messages to your conversation.

**Source**: https://code.claude.com/docs/en/features-overview
**Last Updated**: 2026-06-13
**Status**: Active
