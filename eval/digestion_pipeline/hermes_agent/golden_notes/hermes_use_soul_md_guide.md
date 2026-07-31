---
tags:
  - resource
  - documentation
  - hermes_agent
  - identity
  - configuration
keywords:
  - SOUL.md
  - agent identity
  - system prompt slot 1
  - personality vs soul
  - AGENTS.md vs SOUL.md
  - prompt injection scan
topics:
  - Hermes Agent
  - Agent Identity
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes
access_control_group: ["general"]
---

# Use SOUL.md with Hermes

## Overview

`SOUL.md` is the **primary identity file** for a Hermes Agent instance — the practical how-to for shaping how a given Hermes "feels" across every session. It is the first thing placed in the system prompt (slot #1): it defines who the agent is, how it speaks, and what it avoids stylistically. Edit it when you want Hermes to feel like the same assistant every time, or to replace the built-in Hermes persona entirely with your own voice. This note is the *usage* procedure — where the file lives, how Hermes loads and protects it, what belongs in it (vs `AGENTS.md` and `/personality`), and how to troubleshoot it. The SOUL/persona *concept* is owned by the personality feature page; this guide covers the day-to-day workflow of authoring and tuning the file.

## What SOUL.md is (and is not) for

Use `SOUL.md` for durable, broadly-applicable style: tone, personality, communication style, how direct or warm Hermes should be, what it should avoid stylistically, and how it should relate to uncertainty, disagreement, and ambiguity. In short — *who Hermes is and how Hermes speaks.*

Do **not** put repo-specific coding conventions, file paths, commands, service ports, architecture notes, or project workflow instructions in it — those belong in `AGENTS.md`. The rule of thumb: if it should apply everywhere, it goes in `SOUL.md`; if it only belongs to one project, it goes in `AGENTS.md`.

## Where it lives

Hermes uses only the global SOUL file for the current instance:

```text
~/.hermes/SOUL.md
```

If you run Hermes with a custom home directory, it becomes `$HERMES_HOME/SOUL.md`.

## First-run behavior

Hermes automatically seeds a starter `SOUL.md` if one does not already exist, so most users begin with a real, editable file. Two guarantees: if you already have a `SOUL.md`, Hermes **does not overwrite it**; and if the file exists but is empty, Hermes adds nothing from it to the prompt.

## How Hermes uses it

When Hermes starts a session it reads `SOUL.md` from `HERMES_HOME`, scans it for prompt-injection patterns, truncates it if needed, and uses it as the **agent identity** — slot #1 in the system prompt. This means `SOUL.md` *completely replaces* the built-in default identity text. If the file is missing, empty, or cannot be loaded, Hermes falls back to a built-in default identity. No wrapper language is added around the file — the content itself is what matters, so write the way you want the agent to think and speak.

## A good first edit and example styles

If you do nothing else, change a few lines so the file feels like you — even four lines noticeably changes how Hermes feels:

```markdown
You are direct, calm, and technically precise.
Prefer substance over politeness theater.
Push back clearly when an idea is weak.
Keep answers compact unless deeper detail is useful.
```

The source ships four example voices to copy from — **pragmatic engineer**, **research partner**, **teacher/explainer**, and **tough reviewer** — each pairing an identity line with `## Style` and `## Avoid` sections. A suggested (optional) structure for a fuller file:

```markdown
# Identity
Who Hermes is.

# Style
How Hermes should sound.

# Avoid
What Hermes should not do.

# Defaults
How Hermes should behave when ambiguity appears.
```

A **strong** `SOUL.md` is stable, broadly applicable, specific in voice, and not overloaded with temporary instructions. A **weak** one is full of project details, contradictory, micro-manages every response shape, or is generic filler like "be helpful" — Hermes already tries to be helpful and clear, so `SOUL.md` should add real personality, not restate defaults.

## SOUL.md vs /personality vs AGENTS.md

These are complementary, not competing:

- **`SOUL.md` vs `/personality`** — `SOUL.md` is your *durable baseline*; `/personality` is a *temporary mode switch*. Example: your default SOUL is pragmatic and direct, you run `/personality teacher` for one session, then switch back without touching the base voice file.
- **`SOUL.md` vs `AGENTS.md`** — the most common mistake. Identity/style ("Be direct.", "Avoid hype language.", "Push back when the user is wrong.") goes in `SOUL.md`; project facts ("Use pytest, not unittest.", "Frontend lives in `frontend/`.", "The API runs on port 8000.") go in `AGENTS.md`.

## How to edit it and a practical workflow

Edit with any editor, then restart Hermes or start a new session:

```bash
nano ~/.hermes/SOUL.md
```

The recommended iterative workflow: (1) start with the seeded default; (2) trim anything that does not feel like the voice you want; (3) add 4–8 lines that clearly define tone and defaults; (4) talk to Hermes for a while; (5) adjust based on what still feels off. This works better than trying to design the perfect personality in one shot.

## Troubleshooting

- **Edited SOUL.md but Hermes sounds the same** — confirm you edited `~/.hermes/SOUL.md` (or `$HERMES_HOME/SOUL.md`), not a repo-local file; the file is not empty; the session was restarted; and no `/personality` overlay is dominating.
- **Hermes ignores parts of SOUL.md** — higher-priority instructions may override it, the file may contain conflicting guidance, it may be too long and got truncated, or some text resembled prompt-injection content and was blocked/altered by the scanner.
- **SOUL.md became too project-specific** — move project instructions into `AGENTS.md` and keep `SOUL.md` focused on identity and style.

**Source**: `inbox/hermes_agent_docs/guides/use-soul-with-hermes.md` · https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes
**Last Updated**: 2026-06-19
**Status**: Active
