---
tags:
  - resource
  - terminology
  - agentic_ai
  - genai
  - coding_assistant
  - cli
  - anthropic
keywords:
  - Claude Code
  - agentic coding
  - Anthropic
  - CLI coding assistant
  - agent harness
  - SWE-bench
  - Model Context Protocol
  - CLAUDE.md
topics:
  - agentic AI
  - software development tools
  - AI-assisted coding
language: markdown
date of note: 2026-03-31
status: active
building_block: concept
---

# Claude Code

## Definition

Claude Code is Anthropic's agentic coding tool that runs directly in the terminal as a CLI application. Unlike traditional code completion tools that suggest snippets, Claude Code operates as a full [agent harness](term_agent_harness.md) — it reads entire codebases, makes multi-file edits, executes shell commands, runs tests, manages git workflows, and creates pull requests, all through natural language instructions. Anthropic describes it as a "general-purpose agent harness."

Claude Code provides direct file system access and a bash execution sandbox, enabling it to autonomously implement features, debug issues, refactor code, and handle complex multi-step development tasks while maintaining human oversight through an approval-based permission model.

## Historical Context

| Date | Milestone |
|------|-----------|
| Feb 2025 | Introduced alongside Claude 3.7 Sonnet as a research preview (beta) |
| May 2025 | General availability — exits beta |
| Sep 2025 | Claude Code 2.0 launched with checkpoints, subagents, and Claude Agent SDK |
| Sep 2025 | Claude Sonnet 4.5 achieves 77.2% on SWE-bench, powering Claude Code |
| 2025-26 | MCP integration enables extensible tool connectivity; ecosystem of hooks, skills, and custom commands grows |

## Key Properties

- **Terminal-native**: Runs in the developer's terminal — no IDE plugin, remote server, or complex setup required
- **Agentic**: Doesn't just suggest code — actively implements changes, runs tests, commits, and creates PRs
- **Codebase-aware**: Understands entire project structure, not just the current file
- **Permission model**: Asks for human approval before executing potentially destructive operations
- **MCP-extensible**: Connects to external services (GitHub, databases, APIs) via [Model Context Protocol](term_mcp.md)
- **Session persistence**: Uses `CLAUDE.md` project files and progress logs for context across sessions
- **Subagent support** (v2.0): Can spawn parallel subagents for independent subtasks

## Architecture (as Agent Harness)

Claude Code exemplifies the [agent harness](term_agent_harness.md) pattern:

| Harness Component | Claude Code Implementation |
|-------------------|---------------------------|
| **Tool integration** | File read/write, bash execution, git operations, web search, MCP servers |
| **Memory & state** | `CLAUDE.md` (project context), `claude-progress.txt` (session handoff), conversation history |
| **Context engineering** | Automatic context compaction for long sessions; initializer prompt for first context window |
| **Planning** | Breaks complex tasks into subtasks; checkpoints for rollback (v2.0) |
| **Verification** | Runs tests, checks build output, iterates on failures automatically |

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-file editing** | Reads and modifies multiple files in a single operation |
| **Test execution** | Runs test suites and iterates on failures until passing |
| **Git workflows** | Commits, branches, creates PRs with descriptive messages |
| **`CLAUDE.md`** | Project-level configuration file providing persistent context, conventions, and instructions |
| **Custom slash commands** | User-defined commands (`.claude/commands/`) for repeatable workflows |
| **Hooks** | Pre/post execution hooks for custom validation and automation |
| **Checkpoints** (v2.0) | Snapshot and rollback capability for safe experimentation |
| **Subagents** (v2.0) | Parallel task execution via spawned sub-instances |

## Comparison with Similar Tools

| Tool | Developer | Approach | Key Difference |
|------|-----------|----------|---------------|
| **Claude Code** | Anthropic | Terminal CLI, agentic | Full agent harness with bash + file access |
| **[Kiro](term_kiro.md)** | Amazon | Terminal CLI, agentic | MCP-first, skills system, knowledge indexing, multi-agent |
| **GitHub Copilot** | GitHub/Microsoft | IDE plugin, completions | Primarily inline suggestions, agent mode added later |
| **Cursor** | Cursor Inc. | IDE (VS Code fork), agentic | Full IDE with integrated chat + composer |
| **Windsurf** | Codeium | IDE, agentic | Flow-based cascading actions |

## Related Terms

- **[Agent Harness](term_agent_harness.md)**: Claude Code is a canonical example of a coding agent harness
- **[Claude](term_claude.md)**: The underlying LLM family powering Claude Code
- **[Kiro](term_kiro.md)**: Amazon's analogous coding agent harness with MCP-first architecture
- **[MCP](term_mcp.md)**: Model Context Protocol — extensibility layer for tool integration
- **[Context Engineering](term_context_engineering.md)**: Core technique Claude Code uses for managing long sessions
- **[Agent SOP](term_agent_sop.md)**: `CLAUDE.md` files function as agent SOPs — persistent instructions guiding behavior

## References

### Internal Tutorials
- [Tutorial: Claude Code Getting Started (CLI)](../documentation/tutorials/tutorial_claude_code_getting_started.md) — Installation, AIM plugins, workflows, configuration

### External Sources

- [Anthropic (2024). "Effective harnesses for long-running agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — harness design patterns behind Claude Code
- [Anthropic (2025). Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) — official docs
- [DigitalApplied (2025). "Claude Sonnet 4.5, Code 2.0 & Agent SDK"](https://www.digitalapplied.com/blog/claude-sonnet-4-5-code-2-agent-sdk-guide) — Code 2.0 features overview
- [SpectrumAI (2025). "Claude Code Complete Guide"](https://spectrumailab.com/blog/claude-code-complete-guide-agentic-coding-2025) — installation, CLAUDE.md setup, workflows

---

**Last Updated**: 2026-03-31
