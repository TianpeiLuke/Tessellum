---
tags:
  - resource
  - documentation
  - claude_code
  - extensions
  - agentic_loop
keywords:
  - extend claude code
  - extension layer
  - claude.md skills hooks mcp subagents plugins
  - match features to goal
  - build setup over time
  - feature trigger ladder
  - always-on context vs on-demand
topics:
  - Claude Code
  - Extensions
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/features-overview
access_control_group: ["general"]
---

# Extend Claude Code — The Extension Layer

## Overview

Claude Code pairs a model that reasons about code with [built-in tools](cc_built_in_tools.md) for file operations, search, execution, and web access, which cover most coding tasks. On top of that core [agentic loop](cc_agentic_loop.md) sits an **extension layer** — features you add to customize what Claude knows, connect it to external services, and automate workflows. Each extension plugs into a different part of the loop:

- **CLAUDE.md** adds persistent context Claude sees every session.
- **Skills** add reusable knowledge and invocable workflows.
- **Code intelligence** connects Claude to a language server for symbol-level navigation and live type errors.
- **MCP** connects Claude to external services and tools.
- **Subagents** run their own loops in isolated context, returning summaries.
- **Agent teams** coordinate multiple independent sessions with shared tasks and peer-to-peer messaging.
- **Hooks** fire on lifecycle events and can run a script, HTTP request, prompt, or subagent.
- **Plugins** and **marketplaces** package and distribute these features.

Skills are the most flexible extension: a skill is a markdown file containing knowledge, workflows, or instructions. You can invoke skills with a command like `/deploy`, or Claude can load them automatically when relevant. Skills run in your current conversation or in an isolated context via subagents.

If you are new to Claude Code, the docs recommend starting with CLAUDE.md for project conventions, then adding other extensions as specific triggers come up.

## Match features to your goal

Features span a spectrum: from always-on context that Claude sees every session, to on-demand capabilities you or Claude can invoke, to background automation that runs on specific events. The source maps each feature to when it makes sense:

- **CLAUDE.md** — persistent context loaded every conversation; use for project conventions and "always do X" rules (e.g. "Use pnpm, not npm. Run tests before committing.").
- **Skill** — instructions, knowledge, and workflows Claude can use; use for reusable content, reference docs, and repeatable tasks (e.g. a `/deploy` checklist or an API-docs skill).
- **Subagent** — isolated execution context that returns summarized results; use for context isolation, parallel tasks, and specialized workers (e.g. a research task that reads many files but returns only key findings).
- **Agent teams** — coordinate multiple independent Claude Code sessions; use for parallel research, new-feature development, and debugging with competing hypotheses.
- **Code intelligence** — language-server navigation and diagnostics; use for typed languages and large codebases where grep is slow or imprecise.
- **MCP** — connect to external services; use when Claude needs external data or actions (query a database, post to Slack, control a browser).
- **Hook** — script, HTTP request, prompt, or subagent triggered by events; use for automation that must run on every matching event (e.g. run ESLint after every file edit).

**Plugins** are the packaging layer: a plugin bundles skills, hooks, subagents, and MCP servers into a single installable unit. Plugin skills are namespaced (like `/my-plugin:review`) so multiple plugins can coexist. Use plugins to reuse the same setup across repositories or distribute to others via a marketplace.

For side-by-side comparisons of features that seem similar (Skill vs Subagent, CLAUDE.md vs Skill, Subagent vs Agent team, MCP vs Skill, Hook vs Skill), see [Feature Selection Guide](cc_feature_selection_guide.md). For how each feature loads and its context cost, see [How Features Load and Their Context Cost](cc_context_cost_by_feature.md).

## Build your setup over time

You don't need to configure everything up front. Each feature has a recognizable trigger, and most teams add them in roughly this order:

- Claude gets a convention or command wrong twice → add it to CLAUDE.md.
- You keep typing the same prompt to start a task → save it as a user-invocable skill.
- You paste the same playbook or multi-step procedure into chat for the third time → capture it as a skill.
- You keep copying data from a browser tab Claude can't see → connect that system as an MCP server.
- Claude reads many files to find where a symbol is defined or used → install a code intelligence plugin for your language.
- A side task floods your conversation with output you won't reference again → route it through a subagent.
- You want something to happen every time without asking → write a hook.
- A second repository needs the same setup → package it as a plugin.

The same triggers tell you when to update what you already have. A repeated mistake or a recurring review comment is a CLAUDE.md edit, not a one-off correction in chat. A workflow you keep tweaking by hand is a skill that needs another revision.

**Source**: https://code.claude.com/docs/en/features-overview
**Last Updated**: 2026-06-13
**Status**: Active
