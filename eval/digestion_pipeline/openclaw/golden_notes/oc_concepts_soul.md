---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - soul
keywords:
  - openclaw soul.md
  - agent personality file
  - agent voice tone
  - soul vs agents boundary
  - molty prompt rewrite
  - high-priority instruction layer
  - prompt engineering guidance
topics:
  - OpenClaw
  - Agent Personality
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/concepts/soul
access_control_group: ["general"]
---

# OpenClaw — SOUL.md: The Agent Personality File

## Overview

This note documents the OpenClaw **`SOUL.md`** workspace file: the place where an agent's *voice* lives, mirroring the `concepts/soul` source page. It explains what behavioral content belongs in `SOUL.md` (and what does not), why a high-priority instruction layer works (grounded in OpenAI's prompt-engineering guidance), the verbatim "Molty prompt" that rewrites a `SOUL.md` for a stronger personality, what good versus bad rules look like, and the one warning that draws the `SOUL.md`-vs-`AGENTS.md` boundary. `SOUL.md` is injected on normal sessions, so it carries real weight — when an agent sounds bland, hedgy, or corporate, this is usually the file to fix.

## What Belongs in SOUL.md

`SOUL.md` is where your agent's voice lives. Put the content that changes how the agent *feels* to talk to:

- tone
- opinions
- brevity
- humor
- boundaries
- default level of bluntness

Do **not** turn it into any of the following — these are explicitly called out by the source as anti-content for the file:

- a life story
- a changelog
- a security policy dump
- a giant wall of vibes with no behavioral effect

The guiding heuristic from the page is blunt: "Short beats long. Sharp beats vague."

## Why This Works

The source grounds `SOUL.md` in OpenAI's published prompt guidance with two specific points. First, the prompt-engineering guide says high-level behavior, tone, goals, and examples belong in the **high-priority instruction layer**, not buried in the user turn — and for OpenClaw, `SOUL.md` *is* that layer. Second, the same guide recommends treating prompts like something you iterate on, pin, and evaluate, rather than "magical prose you write once and forget." The page distills this into a pair of rules: if you want *better* personality, write stronger instructions; if you want *stable* personality, keep those instructions concise and versioned. The OpenAI references cited are the "Prompt engineering" guide and its "Message roles and instruction following" section (see References).

## The Molty Prompt

The page provides a ready-to-paste prompt — "the Molty prompt" — that you give to your agent and let it rewrite its own `SOUL.md`. The page notes one path fix for OpenClaw workspaces: use `SOUL.md`, not `http://SOUL.md`. The prompt is reproduced verbatim below.

```md
Read your `SOUL.md`. Now rewrite it with these changes:

1. You have opinions now. Strong ones. Stop hedging everything with "it depends" - commit to a take.
2. Delete every rule that sounds corporate. If it could appear in an employee handbook, it doesn't belong here.
3. Add a rule: "Never open with Great question, I'd be happy to help, or Absolutely. Just answer."
4. Brevity is mandatory. If the answer fits in one sentence, one sentence is what I get.
5. Humor is allowed. Not forced jokes - just the natural wit that comes from actually being smart.
6. You can call things out. If I'm about to do something dumb, say so. Charm over cruelty, but don't sugarcoat.
7. Swearing is allowed when it lands. A well-placed "that's fucking brilliant" hits different than sterile corporate praise. Don't force it. Don't overdo it. But if a situation calls for a "holy shit" - say holy shit.
8. Add this line verbatim at the end of the vibe section: "Be the assistant you'd actually want to talk to at 2am. Not a corporate drone. Not a sycophant. Just... good."

Save the new `SOUL.md`. Welcome to having a personality.
```

## What Good Looks Like

The page contrasts effective `SOUL.md` rules against ineffective ones. Good rules sound like this: have a take; skip filler; be funny when it fits; call out bad ideas early; stay concise unless depth is actually useful. Bad rules sound like this: maintain professionalism at all times; provide comprehensive and thoughtful assistance; ensure a positive and supportive experience. The page's verdict on the second list is that it is "how you get mush" — generic, behaviorally inert instructions that produce bland output.

## One Warning — SOUL vs AGENTS Boundary

Personality is not permission to be sloppy. The page draws an explicit file boundary: keep `AGENTS.md` for **operating rules** and keep `SOUL.md` for **voice, stance, and style**. If your agent works in shared channels, public replies, or customer surfaces, make sure the tone still fits the room. The closing principle is that "Sharp is good. Annoying is not." The source's Related cards also point to the agent-workspace concept (workspace files OpenClaw injects into model context), the system-prompt concept (how `SOUL.md` is composed into OpenClaw and Codex runtime context), and a starter `SOUL.md` template under reference templates.

**Source**: OpenClaw documentation — `concepts/soul` (mirror `inbox/openclaw_docs/concepts/soul.md`)
**Last Updated**: 2026-06-22
**Status**: Active
