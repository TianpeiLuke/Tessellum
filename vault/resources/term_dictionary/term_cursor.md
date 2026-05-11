---
tags:
  - resource
  - terminology
  - agentic_ai
  - genai
  - coding_assistant
  - ide
keywords:
  - Cursor
  - Cursor IDE
  - AI code editor
  - VS Code fork
  - agentic coding
  - Composer
  - vibe coding
  - agent harness
topics:
  - agentic AI
  - software development tools
  - AI-assisted coding
language: markdown
date of note: 2026-04-01
status: active
building_block: concept
---

# Cursor

## Definition

Cursor is an AI-native code editor built as a fork of Visual Studio Code, designed for AI-first development workflows. It integrates frontier LLMs (Claude, GPT, Gemini) directly into the editing experience with codebase-aware chat, multi-file editing via Composer, inline refactoring, and a full agentic mode that can plan, edit, and execute terminal commands across entire codebases.

Cursor functions as an [agent harness](term_agent_harness.md) embedded in an IDE — it wraps LLMs with file system access, terminal execution, codebase indexing, multi-agent parallel workflows, and an embedded browser with DOM tools. Andrej Karpathy used Cursor when he coined the term "vibe coding."

## Historical Context

| Date | Milestone |
|------|-----------|
| 2023 | Cursor launches as an AI-enhanced VS Code fork with inline completions and chat |
| 2024 | Composer feature introduced — multi-file editing with aggregated diffs |
| 2025 | Agent mode goes GA — multi-step autonomous workflows with guardrails and approvals |
| 2025 | Cursor 2.0 — parallel multi-agent workflow (8-agent limit via git worktrees), native Composer model, embedded browser |
| 2026 | Competes directly with Claude Code, GitHub Copilot agent mode, and Windsurf for agentic coding market |

## Key Properties

- **VS Code fork**: Inherits familiar interface, extensions, keybindings — low switching cost
- **AI-native**: AI is a core architectural component, not a plugin bolted on
- **Multi-model**: Supports Claude, GPT, Gemini, and proprietary Cursor models
- **Codebase indexing**: Indexes entire repositories for context-aware suggestions and chat
- **Agentic mode**: Plans multi-step tasks, edits files, runs terminal commands, iterates on errors
- **Multi-agent parallel**: Up to 8 agents operating in isolated git worktrees simultaneously (v2.0)
- **Privacy mode**: Zero-retention data routing option for enterprise use; SSO/SCIM support

## Key Features

| Feature | Description |
|---------|-------------|
| **Tab completions** | Context-aware multi-line code completions |
| **Chat** | Codebase-aware conversational interface for questions and edits |
| **Composer** | Multi-file editing with aggregated diffs and preview-before-apply |
| **Agent mode** | Autonomous multi-step workflows with terminal access and guardrails |
| **Inline edits** | Targeted refactoring with trustworthy diffs and selective apply |
| **`.cursorrules`** | Project-level configuration for coding conventions and AI behavior |
| **Background agents** | Parallel agents working on separate tasks in isolated worktrees |
| **Embedded browser** | Built-in browser with DOM inspection tools for frontend development |

## Architecture (as Agent Harness)

| Harness Component | Cursor Implementation |
|-------------------|----------------------|
| **Tool integration** | File read/write, terminal execution, embedded browser, extension ecosystem |
| **Memory & state** | Codebase index, conversation history, `.cursorrules` for persistent context |
| **Context engineering** | Automatic codebase retrieval, file relevance ranking, context window management |
| **Planning** | Agent mode decomposes tasks; background agents handle parallel subtasks |
| **Verification** | Preview-before-apply diffs, terminal output checking, iterative error fixing |

## Comparison with Similar Tools

| Tool | Type | Key Difference |
|------|------|---------------|
| **Cursor** | IDE (VS Code fork) | Full IDE with deep AI integration, multi-agent, embedded browser |
| **[Claude Code](term_claude_code.md)** | Terminal CLI | Lighter weight, no IDE — pure terminal agent harness |
| **[Kiro](term_kiro.md)** | Terminal CLI | MCP-first, skills system, knowledge indexing |
| **[Cline](term_cline.md)** | VS Code extension | Plugin approach — adds agent capabilities to existing VS Code |
| **GitHub Copilot** | IDE plugin | Primarily completions; agent mode added later |
| **Windsurf** | IDE (VS Code fork) | Flow-based cascading actions, similar architecture to Cursor |

## Related Terms

- **[Agent Harness](term_agent_harness.md)**: Cursor is an IDE-embedded agent harness
- **[Claude Code](term_claude_code.md)**: Primary competitor — terminal-based vs. IDE-based harness
- **[Kiro](term_kiro.md)**: Amazon's terminal-based coding agent harness
- **[Cline](term_cline.md)**: VS Code extension approach to agentic coding
- **[Context Engineering](term_context_engineering.md)**: Core technique for codebase-aware AI features
- **[MCP](term_mcp.md)**: Model Context Protocol — supported for tool extensibility

## References

### External Sources

- [Viberank (2025). "Cursor vs Claude Code vs GitHub Copilot"](https://www.viberank.app/blog/cursor-vs-claude-code-vs-copilot) — feature comparison
- [Skywork (2025). "Cursor 2.0 Ultimate Guide"](https://skywork.ai/blog/vibecoding/cursor-2-0-ultimate-guide-2025-ai-code-editing/) — v2.0 features and multi-agent workflow
- [DataCamp (2026). "Cursor vs VS Code"](https://www.datacamp.com/blog/cursor-vs-vs-code) — evolution from editor to agent platform
- [EngineLabs (2025). "Cursor AI In-Depth Review"](https://blog.enginelabs.ai/cursor-ai-an-in-depth-review) — developer experience review

---

**Last Updated**: 2026-04-01
