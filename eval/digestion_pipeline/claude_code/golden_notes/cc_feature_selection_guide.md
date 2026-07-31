---
tags:
  - resource
  - documentation
  - claude_code
  - extensions
  - feature_selection
keywords:
  - skill vs subagent
  - claude.md vs skill vs rules
  - subagent vs agent team
  - mcp vs skill
  - hook vs skill
  - feature layering precedence
  - combine features
  - extension selection guide
topics:
  - Claude Code
  - Extension Selection
language: markdown
date of note: 2026-06-13
status: active
building_block: argument
source_url: https://code.claude.com/docs/en/features-overview
access_control_group: ["general"]
---

# Choosing Between Claude Code Extensions

## Overview

Several Claude Code extensions can seem to overlap, so the official overview offers head-to-head comparisons to tell them apart, rules for how the same feature layers when defined at multiple levels, and patterns for combining features. The guiding principle is that each extension solves a distinct problem — always-on context (CLAUDE.md), on-demand knowledge and workflows (skills), external connections (MCP), context isolation (subagents), and automation (hooks) — so the choice follows from which problem you have. This note covers the decision logic only; for what each feature *is* and how it loads, see the linked feature notes and [Extending Claude Code](cc_extending_claude_code.md).

## Compare Similar Features

**Skill vs Subagent.** Skills are reusable instructions, knowledge, or workflows you can load into any context and share across contexts; they add to your main window. Subagents are isolated workers with their own context window — work happens separately and only a summary returns. Use a subagent when you need context isolation or your main window is filling up (it might read dozens of files but return only a summary), or when intermediate work need not stay visible. Skills come in two flavors: *reference* skills provide knowledge Claude uses throughout the session, and *action* skills tell Claude to do something specific (like `/deploy`). The two combine: a subagent can preload skills via its `skills:` field, and a skill can run isolated using `context: fork`.

**CLAUDE.md vs Skill.** Both store instructions but load differently. CLAUDE.md loads every session automatically and cannot trigger workflows; skills load on demand and can be triggered with `/<name>`. Put it in CLAUDE.md if Claude should always know it (coding conventions, build commands, project structure, "never do X" rules). Put it in a skill if it is reference material needed only sometimes (API docs, style guides) or a `/<name>` workflow (deploy, review, release). Rule of thumb: keep CLAUDE.md under 200 lines; if it grows, move reference content to skills or split into `.claude/rules/` files.

**CLAUDE.md vs Rules vs Skills.** All three store instructions but load differently: CLAUDE.md loads every session (whole project), `.claude/rules/` load every session or when matching files open (can be scoped to file paths), and skills load on demand (task-specific). Use rules with `paths` frontmatter to keep CLAUDE.md focused — they only load when Claude works with matching files, saving context.

**Subagent vs Agent team.** Both parallelize work but differ architecturally. A subagent runs inside your session and reports results back to the main agent only; the main agent manages all work, and token cost is lower because results are summarized back. An agent team is fully independent sessions whose teammates message each other directly and self-coordinate via a shared task list, at higher token cost. Use a subagent for a quick, focused worker; use an agent team when teammates must share findings, challenge each other, and coordinate. Transition point: if parallel subagents hit context limits or need to talk to each other, agent teams are the next step. (Agent teams are experimental and disabled by default.)

**MCP vs Skill.** They solve different problems and work well together. MCP is a protocol that connects Claude to external services, providing tools and data access with connection and authentication handled by the server. A skill provides knowledge about how to use those tools effectively, plus triggerable workflows. Example: an MCP server connects Claude to your database; a skill teaches Claude your data model, common query patterns, and which tables to use.

**Hook vs Skill.** A hook fires on a lifecycle event (`PostToolUse`, `SessionStart`, etc.) running a shell command, HTTP request, LLM prompt, or subagent; its trigger is guaranteed and deterministic. A skill is instructions Claude reads and interprets, so its outcome can vary. Use a hook when the action must happen the same way every time and needs no reasoning (format on save, reject `rm -rf /`, post a Slack message on session end); use a skill when Claude should decide how to apply the steps or the content is knowledge. Put guardrails in hooks: an instruction like "never edit `.env`" in CLAUDE.md or a skill is a request, not a guarantee — a `PreToolUse` hook that blocks the edit is enforcement.

## How Features Layer

Features can be defined at multiple levels — user-wide, per-project, via plugins, or through managed policies — and CLAUDE.md files can nest in subdirectories. When the same feature exists at multiple levels:

- **CLAUDE.md files** are additive: all levels contribute content simultaneously; on conflict Claude uses judgment, with more specific instructions typically taking precedence.
- **Skills and subagents** override by name: managed > user > project for skills; managed > CLI flag > project > user > plugin for subagents. Plugin skills are namespaced to avoid conflicts.
- **MCP servers** override by name: local > project > user.
- **Hooks** merge: all registered hooks fire for their matching events regardless of source.

## Combine Features

Real setups combine extensions because each handles what it is best at — e.g. CLAUDE.md for conventions, a skill for the deployment workflow, MCP to connect a database, and a hook to run linting after every edit. Common patterns:

- **Skill + MCP** — MCP provides the connection; a skill teaches Claude how to use it well (MCP connects the database, the skill documents schema and query patterns).
- **Skill + Subagent** — a skill spawns subagents for parallel work (an `/audit` skill kicks off security, performance, and style subagents in isolated context).
- **CLAUDE.md + Skills** — CLAUDE.md holds always-on rules, skills hold reference material loaded on demand ("follow our API conventions" in CLAUDE.md, the full style guide in a skill).
- **Hook + MCP** — a hook triggers external actions through MCP (a post-edit hook sends a Slack notification when Claude modifies critical files).

**Source**: https://code.claude.com/docs/en/features-overview
**Last Updated**: 2026-06-13
**Status**: Active
