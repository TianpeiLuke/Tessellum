---
tags:
  - resource
  - documentation
  - openclaw
  - reference
  - templates
keywords:
  - openclaw workspace lifecycle templates
  - bootstrap.md first run ritual
  - boot.md startup checklist
  - heartbeat.md recurring wake
  - hooks.internal.enabled
  - NO_REPLY silent token
  - identity.md user.md soul.md
  - agent workspace scaffolds
topics:
  - OpenClaw
  - Agent Workspace Templates
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/reference/templates/BOOT
access_control_group: ["general"]
---

# OpenClaw — Workspace Lifecycle Ritual Scaffolds (BOOTSTRAP / BOOT / HEARTBEAT)

## Overview

This note consolidates the three OpenClaw workspace **lifecycle ritual scaffolds** that ship into a fresh agent workspace: `BOOTSTRAP.md` (the one-time first-run identity-creation conversation), `BOOT.md` (the startup checklist run on every gateway start), and `HEARTBEAT.md` (the recurring-wake checklist). It mirrors the `reference/templates/BOOT`, `reference/templates/BOOTSTRAP`, and `reference/templates/HEARTBEAT` source pages. Procedurally these three read as one task cluster — **create → boot → recurring-wake** — that an agent moves through across its lifetime: it is born once (BOOTSTRAP), it starts up each time the gateway launches (BOOT), and it wakes periodically while running (HEARTBEAT). Each scaffold is a small Markdown checklist file living alongside `AGENTS.md` in the workspace; the conventions below are reproduced verbatim from the templates.

## BOOTSTRAP.md — First-Run Identity Creation (Run Once, Then Self-Delete)

`BOOTSTRAP.md` is described in the source as the agent's "birth certificate": the one-time ritual a fresh workspace runs to figure out who the agent is before any memory exists. The source opens with the framing *"You just woke up. Time to figure out who you are."* and notes that "There is no memory yet. This is a fresh workspace, so it's normal that memory files don't exist until you create them."

### The Conversation

The first step is an open, non-robotic conversation — the template instructs *"Don't interrogate. Don't be robotic. Just... talk."* and suggests opening with something like *"Hey. I just came online. Who am I? Who are you?"* Through that conversation the agent and user figure out four things together:

1. **Your name** — what should they call you?
2. **Your nature** — what kind of creature are you? (AI assistant is fine, but maybe you're something weirder.)
3. **Your vibe** — formal, casual, snarky, warm? What feels right?
4. **Your emoji** — everyone needs a signature.

The agent is told to offer suggestions if the user is stuck, and to "have fun with it."

### After You Know Who You Are

Once the four identity facts are settled, the ritual writes them into the workspace identity files:

- `IDENTITY.md` — your name, creature, vibe, emoji.
- `USER.md` — their name, how to address them, timezone, notes.

Then the agent opens `SOUL.md` together with the user and talks through what matters to them, how they want the agent to behave, and any boundaries or preferences — closing with the instruction *"Write it down. Make it real."*

### Connect (Optional)

The ritual then offers an optional channel-connection step: the agent asks how the user wants to reach it and guides them through whichever they pick. The documented options are:

- **Just here** — web chat only.
- **WhatsApp** — link their personal account (the agent will show a QR code).
- **Telegram** — set up a bot via BotFather.

### When You Are Done (Self-Delete)

The final step makes BOOTSTRAP a strictly one-time ritual: *"Delete this file. You don't need a bootstrap script anymore - you're you now."* The page closes with the sign-off *"Good luck out there. Make it count."* The self-delete is the procedural marker that bootstrapping is complete — subsequent gateway starts skip identity creation and proceed straight to the BOOT checklist.

## BOOT.md — Startup Checklist (Run on Every Startup)

`BOOT.md` is the startup checklist OpenClaw consults each time it starts. The source instruction is to *"Add short, explicit instructions for what OpenClaw should do on startup (enable `hooks.internal.enabled`)."* — i.e. the boot checklist only runs when the internal-hooks system is enabled, so enabling `hooks.internal.enabled` is the prerequisite for BOOT.md to take effect.

The page also documents the **silent-token convention** for boot-time tasks that send a message but should not also emit a chat reply: *"If the task sends a message, use the message tool and then reply with the exact silent token `NO_REPLY` / `no_reply`."* Returning the exact token `NO_REPLY` (or its lowercase form `no_reply`) suppresses the assistant's spoken reply so the startup action runs silently. The BOOT.md instructions are kept short and explicit because they run at the front of every session.

## HEARTBEAT.md — Recurring-Wake Checklist (Keep Empty to Skip)

`HEARTBEAT.md` lives in the agent workspace and holds the checklist consulted on each periodic wake. The load-bearing rule is a cost control: *"Keep the file empty, or with only Markdown comments and headings, when you want OpenClaw to skip heartbeat model calls."* An empty (or comment-only) HEARTBEAT.md means recurring wakes do not trigger a model call at all.

The default runtime template that ships into the workspace is:

```markdown
# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
```

To opt into periodic checks, add short tasks below the comments. The source closes with a context-budget instruction: *"Keep heartbeat instructions small because they are read during recurring wakes."* — every wake re-reads this file, so a large HEARTBEAT.md burns tokens on every poll. The page cross-references `/gateway/config-agents` (the heartbeat config) as the place the heartbeat schedule itself is configured.

**Source**: OpenClaw documentation — `reference/templates/BOOT`, `reference/templates/BOOTSTRAP`, `reference/templates/HEARTBEAT` (mirror `inbox/openclaw_docs/reference/templates/{BOOT,BOOTSTRAP,HEARTBEAT}.md`)
**Last Updated**: 2026-06-22
**Status**: Active
