---
tags:
  - resource
  - documentation
  - hermes_agent
  - automation
  - agentic_ai
keywords:
  - persistent goals
  - "/goal"
  - "/subgoal"
  - Ralph loop
  - goal judge
  - standing objective
  - turn budget
topics:
  - Hermes Agent
  - Automation
language: markdown
date of note: 2026-06-19
status: active
building_block: procedure
source_url: https://hermes-agent.nousresearch.com/docs/user-guide/features/goals
access_control_group: ["general"]
---

# Persistent Goals (`/goal`)

## Overview

`/goal` is a **standing objective that survives across turns**: you give Hermes one goal, and after every turn a lightweight auxiliary judge model checks whether that goal is satisfied by the assistant's last response. If not, Hermes automatically feeds a continuation prompt back into the *same* session and keeps working — until the goal is achieved, you pause or clear it, or a turn budget runs out. It is Hermes' take on the **Ralph loop**, directly inspired by Codex CLI 0.128.0's `/goal` (Eric Traut, OpenAI): the idea of keeping a goal alive across turns and not stopping until it is achieved is theirs, while the implementation here is independent and adapted to Hermes' architecture (central `CommandDef` registry, `SessionDB.state_meta` persistence, auxiliary-client judge, adapter-FIFO continuation on the gateway side).

Reach for `/goal` on tasks where you would otherwise have to keep saying "keep going" — e.g. "fix every lint error in `src/` and verify `ruff check` passes", "port feature X from repo Y including tests and get CI green", or "build a small CLI and test it against the photos/ folder". Tasks where the agent does one turn and stops do not need `/goal`.

## Quick start

Set a goal and the first turn kicks off immediately — no separate message needed:

```
/goal Fix every failing test in tests/hermes_cli/ and make sure scripts/run_tests.sh passes for that directory
```

The loop you observe:

1. **Goal accepted** — `⊙ Goal set (20-turn budget): <your goal>`
2. **Turn 1 runs** — Hermes works as if you'd sent the goal as a normal message.
3. **Judge runs** — after the turn, the judge model decides `done` or `continue`.
4. **Loop fires if needed** — on `continue` you see `↻ Continuing toward goal (1/20): <judge's reason>` and Hermes takes the next step automatically.
5. **Terminates** — eventually either `✓ Goal achieved: <reason>` or `⏸ Goal paused — N/20 turns used`.

## Commands

| Command | What it does |
|---|---|
| `/goal <text>` | Set (or replace) the standing goal. Kicks off the first turn immediately. |
| `/goal` or `/goal status` | Show the current goal, its status, and turns used. |
| `/goal pause` | Stop the auto-continuation loop without clearing the goal. |
| `/goal resume` | Resume the loop (resets the turn counter back to zero). |
| `/goal clear` | Drop the goal entirely. |

`/goal` works identically on the CLI and every gateway platform (Telegram, Discord, Slack, Matrix, Signal, WhatsApp, SMS, iMessage, Webhook, API server, and the web dashboard).

## Adding criteria mid-goal: `/subgoal`

While a goal is active, `/subgoal <text>` appends extra acceptance criteria **without resetting the loop**. Each call adds one numbered item; on the next turn the **continuation prompt** the agent sees includes the original goal plus an "Additional criteria the user added mid-loop" block, and the **judge prompt** is rewritten so the verdict must consider every subgoal — the goal is not marked done until the original objective *and* every subgoal are met.

| Command | What it does |
|---|---|
| `/subgoal <text>` | Append a new criterion to the active goal. Requires an active `/goal`. |
| `/subgoal` (no args) | Show the current numbered subgoal list. |
| `/subgoal remove <N>` | Remove the Nth subgoal (1-based). |
| `/subgoal clear` | Drop every subgoal but keep the original goal intact. |

Subgoals are persisted alongside the goal in `SessionDB.state_meta`, so they survive `/resume`. Setting a new `/goal <text>` replaces the goal and clears the subgoal list; `/goal clear` does the same. Use this when you start a loop ("fix the failing tests") and partway through also want it to "add a regression test for the bug you just patched" — `/subgoal add a regression test` tightens success criteria without breaking the running loop.

## Behavior details

**The judge.** After every turn Hermes calls an auxiliary model with: the standing goal text, the agent's most recent final response (last ~4 KB of text), and a system prompt telling the judge to reply with strict JSON `{"done": <bool>, "reason": "<one-sentence rationale>"}`. The judge is deliberately conservative — it marks a goal `done` only when the response **explicitly** confirms completion, when the final deliverable is clearly produced, or when the goal is unachievable/blocked (treated as DONE with a block reason so budget is not burned on impossible tasks).

**Fail-open semantics.** If the judge errors (network blip, malformed response, unavailable aux client), Hermes treats the verdict as `continue` — a broken judge never wedges progress. The turn budget is the real backstop.

**Turn budget.** Default is 20 continuation turns (`goals.max_turns` in `config.yaml`). When the budget is hit, Hermes auto-pauses and tells you how to proceed:

```
⏸ Goal paused — 20/20 turns used. Use /goal resume to keep going, or /goal clear to stop.
```

`/goal resume` resets the counter to zero, so you can keep going in measured chunks.

**User messages always preempt.** Any real message you send while a goal is active takes priority over the continuation loop. On the CLI your message lands in `_pending_input` ahead of the queued continuation; on the gateway it goes through the adapter FIFO the same way. The judge runs again after your turn — so if your message happens to complete the goal, the judge catches it and stops.

**Mid-run safety (gateway).** While an agent is already running, `/goal status`, `/goal pause`, and `/goal clear` are safe — they only touch control-plane state and don't interrupt the current turn. Setting a **new** goal mid-run (`/goal <new text>`) is rejected with a message telling you to `/stop` first, so the old continuation can't race the new one.

**Persistence.** Goal state lives in `SessionDB.state_meta` keyed by `goal:<session_id>`. `/resume` picks up right where you left off — set a goal, close your laptop, come back tomorrow, `/resume`, and the goal is still standing exactly as you left it (active, paused, or done).

**Prompt cache.** The continuation prompt is a plain user-role message appended to history. It does **not** mutate the system prompt, swap toolsets, or touch the conversation in any way that invalidates Hermes' prompt cache. Running a 20-turn goal costs the same cache-wise as 20 turns of normal conversation.

## Configuration

Add to `~/.hermes/config.yaml`:

```yaml
goals:
  # Max continuation turns before Hermes auto-pauses and asks you to
  # /goal resume. Default 20. Lower this if you want tighter loops;
  # raise it for long-running refactors.
  max_turns: 20
```

**Choosing the judge model.** The judge uses the `goal_judge` auxiliary task. By default it resolves to your main model (see Auxiliary Models in [hermes_model_aux_provider_config](hermes_model_aux_provider_config.md)). To route the judge to a cheap fast model and keep costs down, add an override:

```yaml
auxiliary:
  goal_judge:
    provider: openrouter
    model: google/gemini-3-flash-preview
```

The judge call is small (~200 output tokens) and runs once per turn, so a cheap fast model is usually the right call.

## Example walkthrough

A four-file goal completing across four turns with a single `/goal` invocation:

```
You: /goal Create four files /tmp/note_{1..4}.txt, one per turn, each containing its number as text

  ⊙ Goal set (20-turn budget): Create four files /tmp/note_{1..4}.txt, one per turn, each containing its number as text

Hermes: Creating /tmp/note_1.txt now.
  💻 echo "1" > /tmp/note_1.txt   (0.1s)
  I've created /tmp/note_1.txt with the content "1". I'll continue with the remaining files on the next turn as you specified.

  ↻ Continuing toward goal (1/20): Only 1 of 4 files has been created; 3 files remain.

Hermes: [Continuing toward your standing goal]
  💻 echo "2" > /tmp/note_2.txt   (0.1s)
  Created /tmp/note_2.txt. Two more to go.

  ↻ Continuing toward goal (2/20): 2 of 4 files created; 2 remain.

  ... (turns 3 and 4 create note_3.txt and note_4.txt) ...

  ✓ Goal achieved: All four files were created with the specified content, completing the goal.
```

Four turns, one `/goal` invocation, zero "keep going" prompts from you.

## When the judge gets it wrong

No judge is perfect. Two failure modes to watch for:

- **False negative — judge says continue when the goal is actually done.** The turn budget catches this. You'll see `⏸ Goal paused` and can `/goal clear` or just send a new message.
- **False positive — judge says done when work remains.** You'll see `✓ Goal achieved` but you know better. Send a follow-up message to continue, or re-set the goal more precisely with `/goal <more specific text>`. The judge's system prompt is deliberately conservative to make false positives rarer than false negatives.

If a verdict is unconvincing, the reason text in the `↻ Continuing toward goal` or `✓ Goal achieved` line tells you exactly what the judge saw — usually enough to diagnose whether the goal text was ambiguous or the model's response was.

**Source**: `inbox/hermes_agent_docs/user-guide/features/goals.md` · https://hermes-agent.nousresearch.com/docs/user-guide/features/goals
**Last Updated**: 2026-06-19
**Status**: Active
