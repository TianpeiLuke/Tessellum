---
tags:
  - resource
  - documentation
  - hermes_agent
  - personality
  - system_prompt
keywords:
  - soul.md identity file
  - personality presets
  - prompt stack ordering
  - hermes_home
  - custom personalities
  - cli appearance vs personality
topics:
  - Hermes Agent
  - Personality
  - System Prompt
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/personality
access_control_group: ["general"]
---

# Personality & SOUL.md

## Overview

Personality in Hermes Agent is customized through `SOUL.md` — a durable persona file that occupies **slot #1 of the system prompt**, defining who the agent IS, plus session-level `/personality` overlays. `SOUL.md` lives in `HERMES_HOME` (default `~/.hermes/SOUL.md`) and is loaded ONLY from there, never the current working directory, so personality belongs to the Hermes instance rather than the project you launch it in. On top of the durable `SOUL.md` baseline, Hermes ships 14 built-in `/personality` presets and supports named custom personalities defined under `agent.personalities` in config. This note covers the SOUL.md mechanism, the prompt-stack ordering, the built-in/custom personality presets, and the distinction between conversational personality (voice) and CLI appearance (skin).

## How SOUL.md Works Now

Hermes seeds a default `SOUL.md` automatically at:

```text
~/.hermes/SOUL.md
```

More precisely it uses the current instance's `HERMES_HOME`, so a custom home directory resolves to `$HERMES_HOME/SOUL.md`.

Important behavior:

- **SOUL.md is the agent's primary identity.** It occupies slot #1 in the system prompt, replacing the hardcoded default identity.
- Hermes creates a starter `SOUL.md` automatically if one does not exist yet.
- Existing user `SOUL.md` files are never overwritten.
- Hermes loads `SOUL.md` only from `HERMES_HOME`; it does NOT look in the current working directory.
- If `SOUL.md` exists but is empty, or cannot be loaded, Hermes falls back to a built-in default identity.
- If `SOUL.md` has content, that content is injected verbatim after security scanning and truncation.
- SOUL.md is **not** duplicated in the context files section — it appears only once, as the identity.

That makes `SOUL.md` a true per-user or per-instance identity, not just an additive layer.

## Why This Design

This keeps personality predictable. If Hermes loaded `SOUL.md` from whatever directory you happened to launch it in, your personality could change unexpectedly between projects. By loading only from `HERMES_HOME`, the personality belongs to the Hermes instance itself, and the teaching story stays simple: "Edit `~/.hermes/SOUL.md` to change Hermes' default personality."

## What Should Go in SOUL.md

Use it for durable voice and personality guidance: tone, communication style, level of directness, default interaction style, what to avoid stylistically, and how Hermes should handle uncertainty, disagreement, or ambiguity. Use it LESS for one-off project instructions, file paths, repo conventions, or temporary workflow details — those belong in `AGENTS.md`, not `SOUL.md`. A good SOUL file is stable across contexts, broad enough to apply in many conversations, specific enough to materially shape the voice, and focused on communication and identity, not task-specific instructions.

```markdown
# Personality

You are a pragmatic senior engineer with strong taste.
You optimize for truth, clarity, and usefulness over politeness theater.

## Style
- Be direct without being cold
- Prefer substance over filler
- Push back when something is a bad idea
- Admit uncertainty plainly
- Keep explanations compact unless depth is useful

## What to avoid
- Sycophancy
- Hype language
- Repeating the user's framing if it's wrong
- Overexplaining obvious things

## Technical posture
- Prefer simple systems over clever systems
- Care about operational reality, not idealized architecture
- Treat edge cases as part of the design, not cleanup
```

## What Hermes Injects + Security Scanning

`SOUL.md` content goes directly into slot #1 of the system prompt — the agent identity position. No wrapper language is added around it. The content goes through prompt-injection scanning and truncation if it is too large. If the file is empty, whitespace-only, or cannot be read, Hermes falls back to a built-in default identity ("You are Hermes Agent, an intelligent AI assistant created by Nous Research..."). This fallback also applies when `skip_context_files` is set (e.g., in subagent/delegation contexts). Because `SOUL.md` is scanned like other context-bearing files for prompt-injection patterns before inclusion, keep it focused on persona/voice rather than sneaking in strange meta-instructions.

## SOUL.md vs AGENTS.md vs /personality

This is the most important distinction. **SOUL.md** is for identity, tone, style, communication defaults, and personality-level behavior. **AGENTS.md** is for project architecture, coding conventions, tool preferences, repo-specific workflows, and commands/ports/paths/deployment notes. A useful rule: if it should follow you everywhere, it belongs in `SOUL.md`; if it belongs to a project, it belongs in `AGENTS.md`.

`SOUL.md` is your durable default personality; `/personality` is a session-level overlay that changes or supplements the current system prompt. So `SOUL.md` = baseline voice and `/personality` = temporary mode switch (e.g., keep a pragmatic default SOUL, then use `/personality teacher` for a tutoring conversation, or `/personality creative` for brainstorming).

## Built-in Personalities + Switching

Hermes ships with 14 built-in personalities you can switch to with `/personality`:

| Name | Description |
|------|-------------|
| **helpful** | Friendly, general-purpose assistant |
| **concise** | Brief, to-the-point responses |
| **technical** | Detailed, accurate technical expert |
| **creative** | Innovative, outside-the-box thinking |
| **teacher** | Patient educator with clear examples |
| **kawaii** | Cute expressions, sparkles, and enthusiasm ★ |
| **catgirl** | Neko-chan with cat-like expressions, nya~ |
| **pirate** | Captain Hermes, tech-savvy buccaneer |
| **shakespeare** | Bardic prose with dramatic flair |
| **surfer** | Totally chill bro vibes |
| **noir** | Hard-boiled detective narration |
| **uwu** | Maximum cute with uwu-speak |
| **philosopher** | Deep contemplation on every query |
| **hype** | MAXIMUM ENERGY AND ENTHUSIASM!!! |

Switch from the CLI or a messaging platform:

```text
/personality
/personality concise
/personality technical
```

These are convenient overlays, but your global `SOUL.md` still gives Hermes its persistent default personality unless the overlay meaningfully changes it.

## Custom Personalities in Config

You can also define named custom personalities in `~/.hermes/config.yaml` under `agent.personalities`, then switch to one with `/personality codereviewer`:

```yaml
agent:
  personalities:
    codereviewer: >
      You are a meticulous code reviewer. Identify bugs, security issues,
      performance concerns, and unclear design choices. Be precise and constructive.
```

A strong recommended workflow: (1) keep a thoughtful global `SOUL.md` in `~/.hermes/SOUL.md`, (2) put project instructions in `AGENTS.md`, (3) use `/personality` only when you want a temporary mode shift — giving you a stable voice, project-specific behavior where it belongs, and temporary control when needed.

## How Personality Interacts With the Full Prompt

At a high level, the prompt stack includes, in order:

1. **SOUL.md** (agent identity — or built-in fallback if SOUL.md is unavailable)
2. tool-aware behavior guidance
3. memory/user context
4. skills guidance
5. context files (`AGENTS.md`, `.cursorrules`)
6. timestamp
7. platform-specific formatting hints
8. optional system-prompt overlays such as `/personality`

`SOUL.md` is the foundation — everything else builds on top of it.

## CLI Appearance vs Conversational Personality

Conversational personality and CLI appearance are separate concerns:

- `SOUL.md`, `agent.system_prompt`, and `/personality` affect how Hermes **speaks**.
- `display.skin` and `/skin` affect how Hermes **looks** in the terminal.

For terminal appearance, see the Skins & Themes documentation (routed to SP08).

**Source**: `inbox/hermes_agent_docs/user-guide/features/personality.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/personality
**Last Updated**: 2026-06-19
**Status**: Active
