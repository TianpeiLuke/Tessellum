---
tags:
  - resource
  - documentation
  - hermes_agent
  - persistent_memory
  - agent_state
keywords:
  - persistent memory
  - memory.md user.md
  - frozen system-prompt snapshot
  - memory tool actions
  - write_approval gate
  - capacity management
  - session search
topics:
  - Hermes Agent
  - Agent Memory
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
access_control_group: ["general"]
---

# Hermes Agent — Persistent Memory

## Overview

Persistent Memory is Hermes Agent's **bounded, self-curated long-term memory** that survives across sessions. It is built from two markdown files — `MEMORY.md` (the agent's personal notes) and `USER.md` (the user profile) — stored in `~/.hermes/memories/` and injected into the system prompt as a frozen snapshot at the start of every session. The agent manages it through the `memory` tool (add/replace/remove), keeps it under strict character limits, scans every entry for injection/exfiltration, and optionally gates writes behind `memory.write_approval`. It is distinct from `session_search` (unlimited SQLite/FTS5 recall of past conversations) and from the external memory-provider plugins that augment it.

## How It Works

Two files make up the agent's memory:

| File | Purpose | Char Limit |
|------|---------|------------|
| **MEMORY.md** | Agent's personal notes — environment facts, conventions, things learned | 2,200 chars (~800 tokens) |
| **USER.md** | User profile — your preferences, communication style, expectations | 1,375 chars (~500 tokens) |

Both are stored in `~/.hermes/memories/` and are injected into the system prompt as a frozen snapshot at session start. The agent manages its own memory via the `memory` tool — it can add, replace, or remove entries.

Character limits keep memory focused. Memory does **not** auto-compact: when a write would exceed the limit, the `memory` tool returns an error instead of silently dropping entries. The agent then makes room itself — consolidating or removing entries in the same turn before retrying (see What Happens When Memory is Full). `replace` is also bound by the limit: swapping an entry for a longer one can still overflow, so the new content must be shortened (or another entry removed) to fit.

## How Memory Appears in the System Prompt

At the start of every session, memory entries are loaded from disk and rendered into the system prompt as a frozen block:

```
══════════════════════════════════════════════
MEMORY (your personal notes) [67% — 1,474/2,200 chars]
══════════════════════════════════════════════
User's project is a Rust web service at ~/code/myapi using Axum + SQLx
§
This machine runs Ubuntu 22.04, has Docker and Podman installed
§
User prefers concise responses, dislikes verbose explanations
```

The format includes a header showing which store (MEMORY or USER PROFILE), the usage percentage and character counts (so the agent knows its capacity), and individual entries separated by `§` (section sign) delimiters; entries can be multiline.

**Frozen snapshot pattern:** the system-prompt injection is captured once at session start and never changes mid-session. This is intentional — it preserves the LLM's prefix cache for performance. When the agent adds/removes memory entries during a session, the changes are persisted to disk immediately but won't appear in the system prompt until the next session starts. Tool responses always show the live state.

## Memory Tool Actions

The agent uses the `memory` tool with these actions:

- **add** — Add a new memory entry.
- **replace** — Replace an existing entry with updated content (uses substring matching via `old_text`).
- **remove** — Remove an entry that's no longer relevant (uses substring matching via `old_text`).

There is no `read` action — memory content is automatically injected into the system prompt at session start, so the agent already sees its memories as part of its conversation context.

### Substring Matching

The `replace` and `remove` actions use short unique substring matching — you don't need the full entry text. The `old_text` parameter just needs to be a unique substring that identifies exactly one entry:

```python
# If memory contains "User prefers dark mode in all editors"
memory(action="replace", target="memory",
       old_text="dark mode",
       content="User prefers light mode in VS Code, dark mode in terminal")
```

If the substring matches multiple entries, an error is returned asking for a more specific match.

## Two Targets Explained

- **`memory` (agent's personal notes)** — for things the agent needs to remember about the environment, workflows, and lessons learned: environment facts (OS, tools, project structure), project conventions and configuration, tool quirks and workarounds discovered, completed-task diary entries, and skills/techniques that worked.
- **`user` (user profile)** — for the user's identity, preferences, and communication style: name/role/timezone, communication preferences (concise vs detailed, format), pet peeves and things to avoid, workflow habits, and technical skill level.

## What to Save vs Skip

The agent saves automatically — you don't need to ask. **Save proactively** when it learns: user preferences ("I prefer TypeScript over JavaScript" → `user`), environment facts ("This server runs Debian 12 with PostgreSQL 16" → `memory`), corrections ("Don't use `sudo` for Docker commands, user is in docker group" → `memory`), conventions, completed work ("Migrated database from MySQL to PostgreSQL on 2026-01-15"), and explicit requests.

**Skip:** trivial/obvious info, easily re-discovered facts (web-searchable), raw data dumps (large code blocks, log files, tables — too big for memory), session-specific ephemera (temporary paths, one-off debugging context), and information already in context files (`SOUL.md` and `AGENTS.md` content).

## Capacity Management

Memory has strict character limits to keep system prompts bounded:

| Store | Limit | Typical entries |
|-------|-------|----------------|
| memory | 2,200 chars | 8-15 entries |
| user | 1,375 chars | 5-10 entries |

### What Happens When Memory is Full

When you try to add an entry that would exceed the limit, the tool returns an error:

```json
{
  "success": false,
  "error": "Memory at 2,100/2,200 chars. Adding this entry (250 chars) would exceed the limit. Consolidate now: use 'replace' to merge overlapping entries into shorter ones or 'remove' stale or less important entries (see current_entries below), then retry this add — all in this turn.",
  "current_entries": ["..."],
  "usage": "2,100/2,200"
}
```

The agent then (1) reads the current entries shown in the error response, (2) identifies entries to remove or consolidate, (3) uses `replace` to merge related entries into shorter versions, and (4) retries the `add`. **Best practice:** when memory is above 80% capacity (visible in the system-prompt header), consolidate before adding. Compact, information-dense entries work best — packing several related facts into one entry, stating specific actionable conventions, or capturing a lesson-with-context — rather than vague ("User has a project") or verbose narrative entries.

## Duplicate Prevention

The memory system automatically rejects exact duplicate entries. If you try to add content that already exists, it returns success with a "no duplicate added" message.

## Security Scanning

Memory entries are scanned for injection and exfiltration patterns before being accepted, since they're injected into the system prompt. Content matching threat patterns (prompt injection, credential exfiltration, SSH backdoors) or containing invisible Unicode characters is blocked.

## Session Search

Beyond `MEMORY.md` and `USER.md`, the agent can search its past conversations using the `session_search` tool: all CLI and messaging sessions are stored in SQLite (`~/.hermes/state.db`) with FTS5 full-text search; queries return actual messages from the DB (no LLM summarization, no truncation); the agent can recall things discussed weeks ago even if they are not in active memory, and can scroll forward/backward inside any session it finds. `hermes sessions list` browses past sessions. Memory holds critical facts that should always be in context (instant, fixed ~1,300-token cost per session); session search answers "did we discuss X last week?" on demand for free. The three session-search calling shapes and response format are documented separately.

## Configuration

```yaml
# In ~/.hermes/config.yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200   # ~800 tokens
  user_char_limit: 1375     # ~500 tokens
  write_approval: false     # false = write freely (default) | true = require approval
```

## Controlling Memory Writes (`write_approval`)

By default the agent saves memory freely — including from the background self-improvement review that runs after a turn. Setting `memory.write_approval: true` is a simple on/off gate applied to **both** foreground turns and the background review: `false` (default) writes freely; `true` requires approval — in the interactive CLI foreground writes prompt inline, while everywhere else (messaging platforms, scripts, and the background review) writes are **staged** for review. To turn memory off entirely (not just gate it), set `memory_enabled: false`.

Review staged writes from the CLI or any messaging platform:

```
/memory pending             # list staged memory writes (auto ones tagged [auto])
/memory approve <id>        # apply one (or 'all')
/memory reject <id>         # drop one (or 'all')
/memory approval on         # turn the gate on (or 'off') and persist it
```

This is the answer to "the agent saved a wrong assumption about me": set `write_approval: true`, and every save — especially the unprompted background ones — waits for your yes/no before it ever enters your profile. A related `display.memory_notifications` setting (`off | on | verbose`) governs only the gateway chat notification (e.g. `💾 Memory updated`) surfaced after a background review writes a memory or skill — the review and the writes themselves are unaffected by it.

## Controlling Skill Writes (`skills.write_approval`)

Skills use the same on/off gate, but the review UX differs because a `SKILL.md` is far too large to read in a chat bubble. When `skills.write_approval: true`, skill writes (create / edit / patch / write_file / delete) always **stage** regardless of origin; you review a one-line gist inline (`/skills pending`, `/skills diff <id>`, `/skills approve <id>`, `/skills reject <id>`, `/skills approval on`), but the full diff stays out-of-band (CLI / dashboard / the staged file under `~/.hermes/pending/skills/<id>.json`). The full skill-gating story lives in the skills-hub / agent-managed-skills doc.

## External Memory Providers

For deeper, persistent memory that goes beyond `MEMORY.md` and `USER.md`, Hermes ships with 8 external memory-provider plugins — including Honcho, OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, and Supermemory. External providers run **alongside** built-in memory (never replacing it) and add capabilities like knowledge graphs, semantic search, automatic fact extraction, and cross-session user modeling. `hermes memory setup` picks and configures a provider; `hermes memory status` checks what's active. Full per-provider detail is in the memory-providers / Honcho and provider-catalog docs.

**Source**: `inbox/hermes_agent_docs/user-guide/features/memory.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
**Last Updated**: 2026-06-19
**Status**: Active
