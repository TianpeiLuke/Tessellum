---
tags:
  - resource
  - terminology
  - systems
  - messaging
  - agents
keywords:
  - Silence Token
  - Intentional Silence Token
  - "[SILENT]"
  - SILENT
  - NO_REPLY
  - NO REPLY
topics:
  - messaging gateway
  - agent automation
  - delivery suppression
language: markdown
date of note: 2026-06-19
status: active
building_block: concept
access_control_group: ["general"]
related_wiki: https://hermes-agent.nousresearch.com/docs/user-guide/messaging
---

# Silence Token (Intentional Silence Token)

## Definition

A **silence token** is a sentinel value that an AI agent emits as its *entire* final response to tell the [Hermes](term_hermes_agent.md) messaging gateway to **suppress outbound delivery** — i.e., to send nothing to the chat surface. Hermes recognizes four normalized tokens: `[SILENT]`, `SILENT`, `NO_REPLY`, and `NO REPLY`. The mechanism gives an agent a first-class way to *intentionally say nothing* in contexts where any reply would be noise: group chats where the bot was not addressed, webhook/hook flows, and automation pipelines that should only speak when something actually changed.

The token is a **delivery decision, not a conversation-state edit**. When the agent's whole final turn is a silence token, the gateway drops the outbound message but still records the assistant turn (e.g. `assistant: [SILENT]`) in the per-chat session transcript, so the user→assistant→user alternation stays well-formed and subsequent turns retain correct context. It solves the problem of agents being forced to produce a visible reply on every invocation even when the correct behavior is to stay quiet.

## Context

Silence tokens are a cross-cutting concept of the Hermes **[messaging gateway](term_messaging_gateway.md)** — the single background process that fans 20+ chat-platform adapters (Telegram, Discord, Slack, …) into one shared agent. The suppression check lives in the gateway runner's **outbound delivery path** (the same `gateway/run.py` stage that handles streamed text and `[[as_document]]`/`MEDIA:` markers), so it applies uniformly across every platform adapter rather than being re-implemented per platform. It is most useful in three Hermes surfaces:

- **Group chats** — the agent can decline to reply when a message is side-channel chatter not directed at it,
  rather than interjecting on every group message.
- **Hooks and automation flows** — a scheduled or event-triggered turn (via the gateway cron tick) can run, make
  its decision, and emit a silence token when no user-visible action is warranted.
- **Conditional notifications** — "only ping me if something is down" style prompts, where the common case is
  no reply.

## Key Characteristics

- **Sentinel matching is exact and whole-response.** The *entire* normalized final response must equal one supported token. A message that merely *mentions* a token in prose — e.g. ``Use `[SILENT]` when nothing changed`` — is delivered normally. Formally, given the normalized final text $r$ and the supported token set $T = \{\texttt{[SILENT]},\ \texttt{SILENT},\ \texttt{NO\_REPLY},\ \texttt{NO REPLY}\}$, the gateway suppresses delivery iff $r \in T$.
- **Normalization before matching.** Whitespace is trimmed and case is folded before the equality test, so ` no_reply `, `No_Reply`, and `NO_REPLY` all match.
- **Transcript-preserving.** Suppression affects only the outbound channel; the silence turn is still persisted to the session store, keeping the dialogue alternation intact for future turns.
- **Failures are never silenced.** Failed turns still surface as errors — Hermes does not hide an error just because the error text happens to resemble a silence token. Silence is opt-in by the model's own output, not a swallow-everything default.
- **Multi-purpose by design.** The same token works for group-chat quiet behavior, webhook/hook flows, and automation pipelines, so platform adapters and skills share one convention.

## Related Terms


## References

- [Hermes — Messaging Gateway: Intentional Silence Tokens](https://hermes-agent.nousresearch.com/docs/user-guide/messaging)
- [Sentinel value (Wikipedia)](https://en.wikipedia.org/wiki/Sentinel_value)
