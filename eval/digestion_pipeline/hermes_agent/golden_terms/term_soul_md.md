---
tags:
  - resource
  - terminology
  - agentic_systems
  - agent_config
  - llm
keywords:
  - soul.md
  - hermes soul file
  - agent identity file
  - system prompt slot 1
  - durable persona
topics:
  - agentic AI systems
  - prompt engineering
  - agent configuration
language: markdown
date of note: 2026-06-15
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: null
---

# SOUL.md - Hermes Agent Durable Identity File

## Definition

**SOUL.md** is the durable, global **persona / identity file** for a [Hermes Agent](term_hermes_agent.md) instance — the Nous Research self-improving autonomous agent framework. It is the *first* content placed into the agent's system prompt (slot #1), defining who the agent is, how it speaks, and what it stylistically avoids. Unlike a generic context file that adds project facts, `SOUL.md` content **replaces** the hardcoded built-in identity text rather than merely layering on top of it; if the file has content, that content is injected verbatim (after security scanning and truncation) as the agent identity, with no wrapper language added around it.

The file is loaded **only** from the instance's home directory — `~/.hermes/SOUL.md`, or `$HERMES_HOME/SOUL.md` under a custom home. Hermes deliberately does *not* look in the current working directory, so the persona belongs to the Hermes *instance* and never changes unexpectedly between projects. On first run Hermes seeds a starter `SOUL.md` (never overwriting an existing one); if the file is missing, empty, whitespace-only, or unreadable, Hermes falls back to a built-in default identity ("You are Hermes Agent, an intelligent AI assistant created by Nous Research...").

## Context

`SOUL.md` is documented across two Hermes pages — `guides/use-soul-with-hermes.md` and `user-guide/features/personality.md` — and is owned by the SP05 knowledge/memory/skills digestion plan as the identity half of Hermes' context-file family. In the prompt-stack assembly (handled in `repo_hermes_agent_agent_core`'s prompt builder), `SOUL.md` occupies slot #1, followed by tool guidance, [persistent/agentic memory](term_agentic_memory.md), skills guidance, project [context files](term_context_files.md), a timestamp, platform hints, and finally any `/personality` overlay. It is the conceptual analogue of Claude Code's `CLAUDE.md` / steering files in [Claude](term_claude.md)-family harnesses — but where those carry *project* context, `SOUL.md` carries *identity* and follows the user everywhere.

The clean division of labor is the most common point of confusion: identity and voice ("be direct", "avoid hype", "push back when the user is wrong") belong in `SOUL.md`, while repo-specific conventions, file paths, commands, and architecture notes belong in `AGENTS.md` (the project context file — a [steering-file](term_steering_files.md)-style artifact). `SOUL.md` is the durable baseline; the `/personality` command (14 built-in presets plus custom `agent.personalities`) is a temporary, per-session overlay that does not mutate the base voice file.

## Key Characteristics

- **Slot #1 identity, not an additive layer**: occupies the first system-prompt position and *replaces* the default built-in identity text; it is not duplicated in the context-files section — it appears exactly once, as the identity.
- **HERMES_HOME-scoped loading**: read only from `~/.hermes/SOUL.md` or `$HERMES_HOME/SOUL.md`, never from the working directory, so persona is tied to the instance and is stable across projects.
- **First-run seeding, never clobbered**: a starter file is auto-created when absent; an existing user file is never overwritten; an empty file contributes nothing.
- **Graceful fallback**: missing, empty, or unreadable → built-in default identity. The same fallback applies when `skip_context_files` is set (e.g. subagent / delegation contexts).
- **Security-scanned + truncated**: like other context-bearing files, `SOUL.md` is checked for [prompt-injection](term_prompt_injection.md) patterns before inclusion and head/tail truncated to a max-character budget; injection-resembling text may be blocked or altered.
- **Identity vs project context**: voice/tone/defaults → `SOUL.md`; coding conventions/paths/commands → [AGENTS.md](term_agents_md.md).
- **Durable baseline vs temporary overlay**: `SOUL.md` is the stable persona; `/personality` is a per-session mode switch layered on top, leaving the base file untouched.
- **A strong SOUL is** stable, broadly applicable, and specific in voice — not overloaded with temporary instructions or generic "be helpful" filler.

## Related Terms


## References
- [Use SOUL.md with Hermes (Hermes Agent docs)](https://github.com/NousResearch)
- [Personality & SOUL.md (Hermes Agent docs)](https://github.com/NousResearch)
- [Nous Research](https://nousresearch.com/)
- [Anthropic — Claude Code memory / CLAUDE.md (analogous identity/context file)](https://docs.anthropic.com/en/docs/claude-code/memory)
