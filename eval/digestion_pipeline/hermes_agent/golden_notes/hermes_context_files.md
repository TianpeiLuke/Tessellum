---
tags:
  - resource
  - documentation
  - hermes_agent
  - context_files
  - prompt_construction
keywords:
  - context files
  - agents.md
  - progressive subdirectory discovery
  - prompt injection scan
  - first-match priority chain
  - context_file_max_chars
topics:
  - Hermes Agent
  - Context Files
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
access_control_group: ["general"]
---

# Hermes Agent — Context Files

## Overview

Context files are project-local (and one global) Markdown files that Hermes Agent **automatically discovers and injects into every conversation** to shape its behavior. Some — `.hermes.md`/`HERMES.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/*.mdc` — are discovered from the working directory; the global `SOUL.md` personality file is loaded from `HERMES_HOME` only. This note documents the **procedure** by which they are scanned, security-checked, truncated, assembled, and injected — at startup into the system prompt and progressively into the conversation as the agent navigates subdirectories. SOUL.md detail is covered in the personality note; this note owns the context-file loading mechanics.

## Supported Context Files

Hermes recognizes the following context files, each with its own discovery rule:

| File | Purpose | Discovery |
|------|---------|-----------|
| **.hermes.md** / **HERMES.md** | Project instructions (highest priority) | Walks to git root |
| **AGENTS.md** | Project instructions, conventions, architecture | CWD at startup + subdirectories progressively |
| **CLAUDE.md** | Claude Code context files (also detected) | CWD at startup + subdirectories progressively |
| **SOUL.md** | Global personality and tone customization for this Hermes instance | `HERMES_HOME/SOUL.md` only |
| **.cursorrules** | Cursor IDE coding conventions | CWD only |
| **.cursor/rules/*.mdc** | Cursor IDE rule modules | CWD only |

**Priority system:** Only **one** project context type is loaded per session (first match wins): `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`. **SOUL.md** is always loaded independently as the agent identity (slot #1).

## AGENTS.md

`AGENTS.md` is the primary project context file. It tells the agent how your project is structured, what conventions to follow, and any special instructions.

### Progressive Subdirectory Discovery

At session start, Hermes loads the `AGENTS.md` from your working directory into the system prompt. As the agent navigates into subdirectories during the session (via `read_file`, `terminal`, `search_files`, etc.), it **progressively discovers** context files in those directories and injects them into the conversation at the moment they become relevant.

```
my-project/
├── AGENTS.md              ← Loaded at startup (system prompt)
├── frontend/
│   └── AGENTS.md          ← Discovered when agent reads frontend/ files
├── backend/
│   └── AGENTS.md          ← Discovered when agent reads backend/ files
└── shared/
    └── AGENTS.md          ← Discovered when agent reads shared/ files
```

This approach has two advantages over loading everything at startup:
- **No system prompt bloat** — subdirectory hints only appear when needed
- **Prompt cache preservation** — the system prompt stays stable across turns

Each subdirectory is checked at most once per session. The discovery also walks up parent directories, so reading `backend/src/main.py` will discover `backend/AGENTS.md` even if `backend/src/` has no context file of its own. Subdirectory context files go through the same security scan as startup context files; malicious files are blocked.

### Example AGENTS.md

```markdown
# Project Context

This is a Next.js 14 web application with a Python FastAPI backend.

## Architecture
- Frontend: Next.js 14 with App Router in `/frontend`
- Backend: FastAPI in `/backend`, uses SQLAlchemy ORM
- Database: PostgreSQL 16
- Deployment: Docker Compose on a Hetzner VPS

## Conventions
- Use TypeScript strict mode for all frontend code
- Python code follows PEP 8, use type hints everywhere
- All API endpoints return JSON with `{data, error, meta}` shape
- Tests go in `__tests__/` directories (frontend) or `tests/` (backend)

## Important Notes
- Never modify migration files directly — use Alembic commands
- The `.env.local` file has real API keys, don't commit it
- Frontend port is 3000, backend is 8000, DB is 5432
```

## SOUL.md

`SOUL.md` controls the agent's personality, tone, and communication style (see the personality note for full details). It is loaded only from `HERMES_HOME`:

- `~/.hermes/SOUL.md`, or `$HERMES_HOME/SOUL.md` if you run Hermes with a custom home directory.

Important details:
- Hermes seeds a default `SOUL.md` automatically if one does not exist yet.
- Hermes loads `SOUL.md` **only** from `HERMES_HOME`; it does not probe the working directory for `SOUL.md`.
- If the file is empty, nothing from `SOUL.md` is added to the prompt.
- If the file has content, the content is injected verbatim after scanning and truncation.

## .cursorrules

Hermes is compatible with Cursor IDE's `.cursorrules` file and `.cursor/rules/*.mdc` rule modules. If these files exist in your project root and no higher-priority context file (`.hermes.md`, `AGENTS.md`, or `CLAUDE.md`) is found, they're loaded as the project context. This means your existing Cursor conventions automatically apply when using Hermes.

## How Context Files Are Loaded

### At startup (system prompt)

Context files are loaded by `build_context_files_prompt()` in `agent/prompt_builder.py`:

1. **Scan working directory** — checks for `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` (first match wins)
2. **Content is read** — each file is read as UTF-8 text
3. **Security scan** — content is checked for prompt injection patterns
4. **Truncation** — files exceeding `context_file_max_chars` characters (default 20,000) are head/tail truncated (70% head, 20% tail, with a marker in the middle)
5. **Assembly** — all sections are combined under a `# Project Context` header
6. **Injection** — the assembled content is added to the system prompt

### During the session (progressive discovery)

`SubdirectoryHintTracker` in `agent/subdirectory_hints.py` watches tool call arguments for file paths:

1. **Path extraction** — after each tool call, file paths are extracted from arguments (`path`, `workdir`, shell commands)
2. **Ancestor walk** — the directory and up to 5 parent directories are checked (stopping at already-visited directories)
3. **Hint loading** — if an `AGENTS.md`, `CLAUDE.md`, or `.cursorrules` is found, it's loaded (first match per directory)
4. **Security scan** — same prompt injection scan as startup files
5. **Truncation** — capped at 8,000 characters per file
6. **Injection** — appended to the tool result, so the model sees it in context naturally

The final prompt section looks roughly like:

```text
# Project Context

The following project context files have been loaded and should be followed:

## AGENTS.md

[Your AGENTS.md content here]

## .cursorrules

[Your .cursorrules content here]

[Your SOUL.md content here]
```

SOUL content is inserted directly, without extra wrapper text.

## Security: Prompt Injection Protection

All context files are scanned for potential prompt injection before being included. The scanner checks for: instruction override attempts ("ignore previous instructions", "disregard your rules"); deception patterns ("do not tell the user"); system prompt overrides ("system prompt override"); hidden HTML comments (`<!-- ignore instructions -->`); hidden div elements (`<div style="display:none">`); credential exfiltration (`curl ... $API_KEY`); secret file access (`cat .env`, `cat credentials`); and invisible characters (zero-width spaces, bidirectional overrides, word joiners).

If any threat pattern is detected, the file is blocked:

```
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

This scanner protects against common injection patterns, but it's not a substitute for reviewing context files in shared repositories — always validate `AGENTS.md` content in projects you didn't author.

## Size Limits

| Limit | Value |
|-------|-------|
| Max chars per file | `context_file_max_chars` (default 20,000, ~7,000 tokens) |
| Head truncation ratio | 70% |
| Tail truncation ratio | 20% |
| Truncation marker | 10% (shows char counts and suggests using file tools) |

When a file exceeds the configured limit, the truncation message reads:

```
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars. Use file tools to read the full file.]
```

## Tips for Effective Context Files

Best practices for `AGENTS.md`: keep it concise (stay under your configured `context_file_max_chars`; the agent reads it every turn); structure with `##` headers for architecture, conventions, important notes; include concrete examples (preferred code patterns, API shapes, naming conventions); mention what NOT to do ("never modify migration files directly"); list key paths and ports (the agent uses these for terminal commands); and update as the project evolves (stale context is worse than no context).

### Per-Subdirectory Context

For monorepos, put subdirectory-specific instructions in nested `AGENTS.md` files:

```markdown
<!-- frontend/AGENTS.md -->
# Frontend Context

- Use `pnpm` not `npm` for package management
- Components go in `src/components/`, pages in `src/app/`
- Use Tailwind CSS, never inline styles
- Run tests with `pnpm test`
```

**Source**: `inbox/hermes_agent_docs/user-guide/features/context-files.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
**Last Updated**: 2026-06-19
**Status**: Active
