---
tags:
  - resource
  - terminology
  - ai_development
  - context_engineering
  - agentic_ai
  - hermes_agent
keywords:
  - AGENTS.md
  - project context file
  - agent instructions
  - coding agent conventions
  - progressive subdirectory discovery
  - Hermes Agent
topics:
  - AI-assisted development
  - context engineering
  - agent configuration
language: markdown
date of note: 2026-06-15
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://agents.md/
---

# AGENTS.md — Project Context File for AI Coding Agents

## Definition

**AGENTS.md** is an open, Markdown-formatted project context file that gives AI coding agents a predictable place to find the instructions, conventions, and architecture they need to work effectively in a repository. It is best understood as "a README for agents": where a `README.md` targets human contributors, `AGENTS.md` carries the operational detail an autonomous agent needs — build and test commands, code-style rules, testing instructions, security considerations, and PR/commit conventions. The format has no required schema; it is plain Markdown with whatever headings a project chooses, which keeps it tool-agnostic.

In the [Hermes Agent](term_hermes_agent.md) runtime, `AGENTS.md` is the primary *project* context file in a first-match priority chain (`.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`); the one matched file is read, security-scanned, truncated to a character budget, assembled under a `# Project Context` header, and injected into the system prompt at session start. It is distinct from a global persona file (Hermes loads `SOUL.md` independently as agent identity), and it is the conventions/architecture surface — not a per-tool config — for the agent loop.

## Context

`AGENTS.md` emerged from collaboration across the AI software-development ecosystem (OpenAI Codex, Amp, Google's Jules, Cursor, Factory) and is now stewarded by the Agentic AI Foundation under the Linux Foundation, giving it cross-vendor authority rather than being owned by any single agent harness. It is consumed by a broad set of agents — Codex, Jules, Cursor, Aider, goose, Gemini CLI, GitHub Copilot's coding agent, Windsurf, Devin, Junie, and others — and by [Hermes Agent](term_hermes_agent.md), which also detects `CLAUDE.md` for compatibility.

It is a key artifact of [context engineering](term_context_engineering.md) for [autonomous coding agents](term_autonomous_coding_agents.md), which is why nearly every coding [agent harness](term_agent_harness.md) reads it.

## Key Characteristics

- **README-for-agents pattern** — keeps detailed agent context out of the human-facing `README.md`, so each stays focused on its audience.
- **No required fields** — standard Markdown with freely chosen headings; common sections are project overview, build/test commands, code style, testing instructions, security considerations, and PR/commit guidelines.
- **Nearest-file precedence (progressive subdirectory discovery)** — in a monorepo, an `AGENTS.md` can live in each package; the agent reads the *nearest* file in the directory tree, and the closest file to an edited file wins on conflict. Hermes loads the working-directory file at startup and progressively discovers subdirectory files as the agent navigates (via `read_file` / `terminal` / `search_files` tool-call paths), walking up to five parent directories and checking each directory at most once.
- **Prompt-cache and budget friendly** — deferring subdirectory hints until they are relevant avoids system-prompt bloat and preserves prompt-cache stability across turns.
- **User prompts override the file** — direct chat instructions take precedence over `AGENTS.md` content.
- **Security-scanned before injection** — context files are checked for prompt-injection patterns (instruction-override phrases, hidden HTML/invisible characters, credential-exfiltration, secret-file access) and blocked if a threat is detected; this matters because a malicious `AGENTS.md` in a shared repo is an untrusted-input vector.
- **Size-bounded** — files exceeding the configured character limit (Hermes default ~20,000 chars / ~7,000 tokens) are head/tail truncated with a marker, since the file is re-read every turn.

## Related Terms


## References

- [AGENTS.md — open format for AI coding agents](https://agents.md/) — the canonical specification, supported-tools list, and nested-file precedence rules.
- [Hermes Agent — Context Files documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files/) — how Hermes discovers, scans, truncates, and injects `AGENTS.md`, including progressive subdirectory discovery and size limits.
- [Agentic AI Foundation (Linux Foundation)](https://www.linuxfoundation.org/) — current steward of the AGENTS.md standard.

---

**Last Updated**: 2026-06-15
**Status**: Active
