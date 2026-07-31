---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - commitments
keywords:
  - openclaw commitments
  - inferred follow-up memory
  - commitments enabled maxperday
  - heartbeat commitment delivery
  - hidden background extraction pass
  - commitments vs reminders
  - openclaw commitments cli
  - operational memory check-in
topics:
  - OpenClaw
  - Commitments
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/commitments
access_control_group: ["general"]
---

# OpenClaw — Enabling and Managing Inferred Commitments

## Overview

This note is the procedure for OpenClaw **commitments**: short-lived inferred follow-up memories that let an agent notice a conversation created a future check-in opportunity and bring it back later, mirroring the `concepts/commitments` source page. Commitments sit between memory and automation — they are NOT durable facts like `MEMORY.md` and NOT exact reminders. This note covers the full operator workflow: enabling the off-by-default feature, the hidden background extraction pass, what is stored per commitment, heartbeat-clamped delivery, agent/channel scope, the `commitments.maxPerDay` cap, the `openclaw commitments` CLI for inspection/dismissal, how commitments differ from scheduled-task reminders, privacy/cost of the extra LLM pass, and the troubleshooting path when expected follow-ups do not appear.

## Enable commitments

Commitments are off by default. Enable them in config with two CLI `config set` calls:

```bash
openclaw config set commitments.enabled true
openclaw config set commitments.maxPerDay 3
```

The equivalent `openclaw.json` block sets the same two keys directly:

```json
{
  "commitments": {
    "enabled": true,
    "maxPerDay": 3
  }
}
```

`commitments.maxPerDay` limits how many inferred follow-ups can be delivered per agent session in a rolling day. The default is `3`.

## How it works

After an agent reply, OpenClaw may run a hidden background extraction pass in a separate context. That pass looks only for inferred follow-up commitments — it does not write into the visible conversation and it does not ask the main agent to reason about the extraction.

When it finds a high-confidence candidate, OpenClaw stores a commitment with: the agent id; the session key; the original channel and delivery target; a due window; a short suggested check-in; and non-instructional metadata for heartbeat to decide whether to send it.

Delivery happens through heartbeat. When a commitment becomes due, heartbeat adds the commitment to the heartbeat turn for the same agent and channel scope. The model can send one natural check-in or reply `HEARTBEAT_OK` to dismiss it. If heartbeat is configured with `target: "none"`, due commitments remain internal and do not send external check-ins. Commitment delivery prompts do not replay the original conversation text, and due commitment heartbeat turns run without OpenClaw tools.

OpenClaw never delivers an inferred commitment immediately after writing it. The due time is clamped to at least one heartbeat interval after the commitment is created, so the follow-up cannot echo back in the same moment it was inferred.

## Scope

Commitments are scoped to the exact agent and channel context where they were created. A follow-up inferred while talking to one agent in Discord is not delivered by another agent, another channel, or an unrelated session. This scope is part of the feature: natural check-ins should feel like the same conversation continuing, not like a global reminder system.

## Commitments vs reminders

Exact user requests already belong to the scheduler path; commitments are only for inferred follow-ups — the moments where the user did not ask for a reminder, but the conversation clearly created a useful future check-in. The source page tabulates which need routes to which mechanism:

| Need                                            | Use            |
| ----------------------------------------------- | -------------- |
| "Remind me at 3 PM"                             | Scheduled tasks |
| "Ping me in 20 minutes"                         | Scheduled tasks |
| "Run this report every weekday"                 | Scheduled tasks |
| "I have an interview tomorrow"                  | Commitments     |
| "I was up all night"                            | Commitments     |
| "Follow up if I do not answer this open thread" | Commitments     |

## Manage commitments

Use the `openclaw commitments` CLI to inspect and clear stored commitments. The page documents these invocations (see the `openclaw commitments` command reference at `/cli/commitments`):

```bash
openclaw commitments
openclaw commitments --all
openclaw commitments --agent main
openclaw commitments --status snoozed
openclaw commitments dismiss cm_abc123
```

The plain `openclaw commitments` form lists current commitments; `--all` includes pending, dismissed, snoozed, and expired records; `--agent main` scopes the listing to one agent; `--status snoozed` filters by record state; and `dismiss cm_abc123` clears a specific commitment by its id.

## Privacy and cost

Commitment extraction uses an LLM pass, so enabling it adds background model usage after eligible turns. The pass is hidden from the user-visible conversation, but it can read the recent exchange needed to decide whether a follow-up exists. Stored commitments are local OpenClaw state — they are operational memory, not long-term memory. Disable the feature with:

```bash
openclaw config set commitments.enabled false
```

## Troubleshooting

If expected follow-ups are not appearing, the page lists these checks: confirm `commitments.enabled` is `true`; check `openclaw commitments --all` for pending, dismissed, snoozed, or expired records; make sure heartbeat is running for the agent; check whether `commitments.maxPerDay` has already been reached for that agent session; and remember that exact reminders are skipped by commitment extraction and should appear under scheduled tasks instead.

**Source**: OpenClaw documentation — `concepts/commitments` (mirror `inbox/openclaw_docs/concepts/commitments.md`)
**Last Updated**: 2026-06-22
**Status**: Active
