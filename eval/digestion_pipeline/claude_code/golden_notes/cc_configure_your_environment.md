---
tags:
  - resource
  - documentation
  - claude_code
  - configuration
  - setup
keywords:
  - configure your environment
  - claude.md
  - configure permissions
  - cli tools
  - connect mcp servers
  - set up hooks
  - create skills
  - custom subagents
  - install plugins
topics:
  - Claude Code
  - Configuration
language: markdown
date of note: 2026-06-13
status: active
building_block: procedure
source_url: https://code.claude.com/docs/en/best-practices
access_control_group: ["general"]
---

# Configure Your Environment

## Overview

A few one-time setup steps make Claude Code significantly more effective across every session in a project. This note is the per-project setup checklist drawn from the best-practices guide: write an effective CLAUDE.md, configure permissions, use CLI tools, connect MCP servers, set up hooks, create skills, create custom subagents, and install plugins. Each lever configures the harness around the model rather than the model itself, and each compounds in value the more you invest in it.

Each item below is a pointer to its dedicated mechanism. The detailed mechanics live in their home documentation pages (linked inline); this checklist captures *what to do per project and why*, not the full reference for each feature. For a full overview of extension features and when to use each one, see [Extend Claude Code](https://code.claude.com/docs/en/features-overview).

## The Setup Checklist

### Write an effective CLAUDE.md

Run `/init` to generate a starter CLAUDE.md based on your current project structure, then refine over time. `/init` analyzes your codebase to detect build systems, test frameworks, and code patterns, giving you a solid foundation to refine.

CLAUDE.md is a special file Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules — persistent context Claude can't infer from code alone. There's no required format, but keep it short and human-readable:

```markdown CLAUDE.md
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

Because CLAUDE.md is loaded every session, only include things that apply broadly. For domain knowledge or workflows that are only relevant *sometimes*, use skills instead — Claude loads them on demand without bloating every conversation. Keep it concise: for each line, ask *"Would removing this cause Claude to make mistakes?"* If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions. The guide gives an include/exclude table (include: Bash commands Claude can't guess, non-default style rules, testing instructions, repo etiquette, project-specific architectural decisions, environment quirks, common gotchas; exclude: anything Claude can read from code, standard conventions, detailed API docs, frequently-changing info, file-by-file descriptions, self-evident practices).

CLAUDE.md files can import additional files using `@path/to/import` syntax, and can be placed in several locations: home folder (`~/.claude/CLAUDE.md`, applies to all sessions), project root (`./CLAUDE.md`, check into git to share), `./CLAUDE.local.md` (personal notes, add to `.gitignore`), parent directories (monorepos), and child directories (pulled in on demand). Check the shared CLAUDE.md into git, tune adherence with emphasis like "IMPORTANT" or "YOU MUST", and prune it regularly. Full CLAUDE.md mechanics: [CLAUDE.md memory](https://code.claude.com/docs/en/memory).

### Configure permissions

By default Claude Code requests permission for actions that might modify your system (file writes, Bash commands, MCP tools). This is safe but tedious — after the tenth approval you're clicking through rather than reviewing. There are three ways to reduce interruptions while keeping you in control:

- **Auto mode** — a separate classifier model reviews commands and blocks only what looks risky (scope escalation, unknown infrastructure, hostile-content-driven actions). Best when you trust a task's general direction but don't want to click through every step.
- **Permission allowlists** — permit specific tools you know are safe, like `npm run lint` or `git commit`, via `/permissions`.
- **Sandboxing** — `/sandbox` enables OS-level isolation restricting filesystem and network access, letting Claude work more freely within defined boundaries.

See [permission modes](https://code.claude.com/docs/en/permission-modes), [permission rules](https://code.claude.com/docs/en/permissions), and [sandboxing](https://code.claude.com/docs/en/sandboxing) for the full reference.

### Use CLI tools

CLI tools are the most context-efficient way to interact with external services. Tell Claude Code to use tools like `gh`, `aws`, `gcloud`, and `sentry-cli`. If you use GitHub, install the `gh` CLI — Claude knows how to use it for creating issues, opening pull requests, and reading comments; without it, Claude can still use the GitHub API but unauthenticated requests often hit rate limits. Claude is also effective at learning CLI tools it doesn't already know: try `Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`

### Connect MCP servers

Run `claude mcp add` to connect external tools like Notion, Figma, or your database. With MCP servers you can ask Claude to implement features from issue trackers, query databases, analyze monitoring data, integrate designs from Figma, and automate workflows. Full reference: [MCP](https://code.claude.com/docs/en/mcp).

### Set up hooks

Use hooks for actions that must happen *every time with zero exceptions*. Hooks run scripts automatically at specific points in Claude's workflow. Unlike CLAUDE.md instructions, which are advisory, hooks are deterministic and guarantee the action happens. Claude can write hooks for you — try *"Write a hook that runs eslint after every file edit"* or *"Write a hook that blocks writes to the migrations folder."* Edit `.claude/settings.json` directly to configure hooks by hand, and run `/hooks` to browse what's configured. Full reference: [Hooks](https://code.claude.com/docs/en/hooks-guide).

### Create skills

Create `SKILL.md` files in `.claude/skills/` to give Claude domain knowledge and reusable workflows. Skills extend Claude's knowledge with information specific to your project, team, or domain. Claude applies them automatically when relevant, or you can invoke them directly with `/skill-name`. Create a skill by adding a directory with a `SKILL.md` to `.claude/skills/`:

```markdown .claude/skills/api-conventions/SKILL.md
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

Skills can also define repeatable workflows you invoke directly (e.g. a `fix-issue` skill invoked with `/fix-issue 1234`). Use `disable-model-invocation: true` for workflows with side effects you want to trigger manually rather than have Claude invoke automatically. Full reference: [Skills](https://code.claude.com/docs/en/skills).

### Create custom subagents

Define specialized assistants in `.claude/agents/` that Claude can delegate to for isolated tasks. Subagents run in their own context with their own set of allowed tools — useful for tasks that read many files or need specialized focus without cluttering your main conversation:

```markdown .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Tell Claude to use subagents explicitly: *"Use a subagent to review this code for security issues."* Full reference: [Subagents](https://code.claude.com/docs/en/sub-agents).

### Install plugins

Run `/plugin` to browse the marketplace. Plugins bundle skills, hooks, subagents, and MCP servers into a single installable unit from the community and Anthropic — adding skills, tools, and integrations without configuration. If you work with a typed language, install a [code intelligence plugin](https://code.claude.com/docs/en/discover-plugins#code-intelligence) to give Claude precise symbol navigation and automatic error detection after edits. Full reference: [Plugins](https://code.claude.com/docs/en/plugins).

For guidance on choosing between skills, subagents, hooks, and MCP, see [Extend Claude Code](https://code.claude.com/docs/en/features-overview#match-features-to-your-goal).

**Source**: https://code.claude.com/docs/en/best-practices
**Last Updated**: 2026-06-13
**Status**: Active
