---
tags:
  - resource
  - terminology
  - agentic_ai
  - llm
keywords:
  - persistent goal
  - standing goal
  - /goal
  - Ralph loop
  - Ralph Wiggum loop
  - goal judge
  - continuation loop
  - autonomous continuation
topics:
  - agentic AI
  - autonomous agents
  - agent control loop
  - LLM-as-a-judge
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://hermes-agent.nousresearch.com/docs/user-guide/features/goals
---

# Persistent Goal (Standing Objective / Ralph Loop)

## Definition

A **persistent goal** is a standing objective an autonomous agent keeps working toward across multiple turns, automatically re-prompting itself after each turn until the goal is satisfied, paused, cleared, or a turn budget is exhausted. Instead of doing one turn and stopping — the default request-response behavior of an LLM agent — a persistent goal makes the agent self-continue: after each completed turn a lightweight evaluator decides whether the objective is met, and if not, the agent is fed a continuation prompt and takes the next step on its own. It solves the operator-fatigue problem where a user would otherwise have to repeatedly type "keep going" to drive a multi-step task (fix every lint error, port a feature with tests until CI is green, exhaustively investigate an issue) to completion.

In the Hermes Agent, this is exposed as the `/goal` command and is explicitly framed as the project's take on the **Ralph loop** (a.k.a. the "Ralph Wiggum" technique). The Ralph loop, popularized by Geoffrey Huntley, is at its simplest a shell loop — `while :; do cat PROMPT.md | claude-code; done` — that repeatedly feeds a standing objective to a coding agent until the work is done; its defining property is "keep a goal alive across turns and don't stop until it's achieved." Persistent-goal implementations differ in whether each iteration runs with **fresh context** (the canonical Ralph variant, which resets context every loop to avoid context-window exhaustion) or **shared session context** (Hermes' variant, which appends a continuation prompt to the same session to preserve the prompt cache).

## Context

The persistent-goal pattern is implemented across several autonomous agent harnesses:

- **Hermes Agent (Nous Research)** — the `/goal` command sets a standing objective with a default 20-turn budget; `/subgoal` appends acceptance criteria mid-loop. The implementation is independent of, but inspired by, Codex CLI 0.128.0's `/goal` by Eric Traut (OpenAI). It uses a central `CommandDef` registry, `SessionDB.state_meta` persistence keyed by `goal:<session_id>`, an auxiliary-client judge, and adapter-FIFO continuation that runs identically on the CLI and every gateway platform (Telegram, Discord, Slack, Matrix, Signal, WhatsApp, SMS, iMessage, Webhook, API server, web dashboard).
- **Codex CLI / Claude Code / ralph-orchestrator** — analogous standing-objective commands and "ralph-loop" plugins (Anthropic's `ralph-loop` plugin runs a continuous autonomous loop with a `maxIterations` setting; ralph-orchestrator keeps multi-backend agents "in a loop until the task is done").

## Key Characteristics

- **Per-turn judge verdict**: After each turn an auxiliary model is given the goal text plus the agent's most recent final response and returns strict JSON `{"done": <bool>, "reason": "<one sentence>"}`. The judge is deliberately conservative — it marks `done` only when completion is explicitly confirmed, the deliverable is clearly produced, or the goal is unachievable/blocked (treated as done so budget is not burned on impossible tasks).
- **Fail-open semantics**: If the judge errors (network blip, malformed response, unavailable client), the verdict defaults to `continue` — a broken judge never wedges progress. The turn budget is the real backstop.
- **Turn budget**: A bounded number of continuation turns (default 20, `goals.max_turns`); on exhaustion the loop auto-pauses with instructions to resume or clear. Given a goal $g$ and per-turn judge $J$, the loop terminates at turn $T = \min(\,\inf\{t : J(g, r_t) = \text{done}\},\ B\,)$ where $r_t$ is the turn-$t$ response and $B$ is the budget.
- **Mid-loop criteria refinement**: Additional acceptance criteria can be appended without resetting the loop (Hermes `/subgoal`); the judge prompt is rewritten so the goal is not done until the original objective AND every added criterion are met.
- **User preemption**: A real user message always takes priority over a queued continuation; the judge re-runs after the user's turn, so a message that happens to complete the goal is caught.
- **Persistence across resume**: Goal and sub-criteria state is stored durably (Hermes `SessionDB.state_meta`) so the standing objective survives a session restart / `/resume`.
- **Prompt-cache preservation (shared-context variant)**: The continuation is a plain user-role append that does not mutate the system prompt or swap toolsets, so a 20-turn goal costs the same cache-wise as 20 normal turns — contrasted with the fresh-context Ralph variant that intentionally resets context each loop.
- **Backpressure for correctness**: In the Ralph tradition, generation is cheap and verification is the hard part; type systems, tests, and static analyzers act as guardrails that reject invalid output, keeping the loop's feedback signal trustworthy.

## Related Terms


## References

- [Hermes Agent — Persistent Goals (`/goal`)](https://hermes-agent.nousresearch.com/docs/user-guide/features/goals)
- [Geoffrey Huntley — "Ralph Wiggum as a software engineer" (the Ralph loop)](https://ghuntley.com/ralph/)
- [Codex CLI (OpenAI) — `/goal` standing-objective command](https://github.com/openai/codex)
- [snarktank/ralph — original autonomous AI agent loop implementation](https://github.com/snarktank/ralph)
- [ralph-orchestrator — multi-backend "keep agents in a loop until done" framework](https://github.com/mikeyobrien/ralph-orchestrator)

---

**Last Updated**: 2026-06-19
**Status**: Active
