---
tags:
  - resource
  - documentation
  - claude_code
  - agentic_loop
  - overview
keywords:
  - claude code overview
  - agentic coding tool
  - ai coding assistant
  - what claude code can do
  - claude code surfaces
  - use claude code everywhere
  - build features fix bugs
  - automate development tasks
topics:
  - Claude Code
  - Overview
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/overview
access_control_group: ["general"]
---

# Claude Code — Overview

## Overview

Claude Code is an agentic coding tool — an AI-powered coding assistant that reads your codebase, edits files, runs commands, and integrates with your development tools. It understands your entire codebase and can work across multiple files and tools to get things done, helping you build features, fix bugs, and automate development tasks. It is available across multiple surfaces — terminal, IDE, desktop app, and browser — so the same engine follows you wherever you work.

## What You Can Do

The source lists representative ways to use Claude Code:

- **Automate the work you keep putting off** — tedious tasks like writing tests for untested code, fixing lint errors across a project, resolving merge conflicts, updating dependencies, and writing release notes.
- **Build features and fix bugs** — describe what you want in plain language; Claude Code plans the approach, writes code across multiple files, and verifies it works. For bugs, it traces the issue, identifies the root cause, and implements a fix.
- **Create commits and pull requests** — it works directly with git to stage changes, write commit messages, create branches, and open pull requests.
- **Connect your tools with MCP** — read design docs, update tickets, pull data, or use custom tooling via the Model Context Protocol.
- **Customize with instructions, skills, and hooks** — `CLAUDE.md` instructions, shareable skills for repeatable workflows, and hooks that run shell commands around Claude Code actions.
- **Run agent teams and build custom agents** — spawn multiple agents that work in parallel, run background agents, or build fully custom workflows with the Agent SDK.
- **Pipe, script, and automate with the CLI** — composable and Unix-philosophy-following; pipe logs in, run it in CI, or chain it with other tools.
- **Schedule recurring tasks** — routines, desktop scheduled tasks, or in-session loops for work that repeats.
- **Work from anywhere** — sessions aren't tied to a single surface; move work between phone, browser, terminal, and desktop.

## Use Claude Code Everywhere

Each surface connects to the same underlying Claude Code engine, so your `CLAUDE.md` files, settings, and MCP servers work across all of them. Beyond the Terminal, VS Code, JetBrains, Desktop, and Web environments, Claude Code also integrates with CI/CD, chat, and browser workflows (for example, GitHub Actions for PR review, Slack for routing bug reports to PRs, and Chrome for debugging live web apps). See [Claude Code Platforms and Integrations](cc_platforms_and_integrations.md) for the full surface and integration map.

Installation and environment-specific setup are covered in the setup documentation (B17), and detailed per-surface walkthroughs live in the surfaces notes (B12). This note covers only what Claude Code is and the shape of its capabilities.

**Source**: https://code.claude.com/docs/en/overview
**Last Updated**: 2026-06-13
**Status**: Active
