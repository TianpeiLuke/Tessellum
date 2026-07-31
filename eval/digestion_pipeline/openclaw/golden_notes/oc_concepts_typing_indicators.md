---
tags:
  - resource
  - documentation
  - openclaw
  - concepts
  - typing_indicators
keywords:
  - openclaw typing indicators
  - typingmode never message thinking instant
  - typingintervalseconds refresh cadence
  - typing indicator defaults legacy behavior
  - heartbeat typing liveness
  - reasoninglevel stream thinking mode
  - no_reply silent token typing
  - agents.defaults.typingmode session override
topics:
  - OpenClaw
  - Typing Indicators
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/concepts/typing-indicators
access_control_group: ["general"]
---

# OpenClaw — Tuning Typing Indicators (`typingMode` + `typingIntervalSeconds`)

## Overview

This note is the procedure for tuning OpenClaw's chat typing indicators: the visual "agent is typing…" signal sent to a chat channel while a run is active. It mirrors the `concepts/typing-indicators` source page. Two knobs control the behavior — `agents.defaults.typingMode` controls **when** typing starts and `typingIntervalSeconds` controls **how often** it refreshes. The note covers the legacy default behavior when `typingMode` is unset, the four explicit modes (`never` / `instant` / `thinking` / `message`) and the "how early it fires" ordering, where to set the agent-level default versus a per-session override, and the edge-case rules for the silent reply token, reasoning streaming, and heartbeat typing.

## Defaults (legacy behavior when `typingMode` is unset)

When `agents.defaults.typingMode` is **unset**, OpenClaw keeps the legacy behavior, which varies by chat context:

- **Direct chats**: typing starts immediately once the model loop begins.
- **Group chats with a mention**: typing starts immediately.
- **Group chats without a mention**: typing starts only when message text begins streaming.
- **Heartbeat runs**: typing starts when the heartbeat run begins if the resolved heartbeat target is a typing-capable chat and typing is not disabled.

## Modes

Set `agents.defaults.typingMode` to one of the following four values:

- `never` — no typing indicator, ever.
- `instant` — start typing **as soon as the model loop begins**, even if the run later returns only the silent reply token.
- `thinking` — start typing on the **first reasoning delta** (requires `reasoningLevel: "stream"` for the run).
- `message` — start typing on the **first non-silent text delta** (ignores the `NO_REPLY` silent token).

The modes are ordered by how early the indicator fires. Order of "how early it fires": `never` → `message` → `thinking` → `instant`. That is, `never` fires not at all, `message` fires latest (only on the first visible text), `thinking` fires earlier (on the first reasoning delta), and `instant` fires earliest (as soon as the model loop begins).

## Configuration

Set the agent-level default with `agents.defaults.typingMode` (and the refresh cadence `typingIntervalSeconds`):

```json5
{
  agents: {
    defaults: {
      typingMode: "thinking",
      typingIntervalSeconds: 6,
    },
  },
}
```

Override the mode or cadence per session under `session`:

```json5
{
  session: {
    typingMode: "message",
    typingIntervalSeconds: 4,
  },
}
```

## Notes (edge-case rules)

The source page calls out the following rules that govern when the indicator does and does not fire:

- `message` mode won't show typing for silent-only replies when the whole payload is the exact silent token (for example `NO_REPLY` / `no_reply`, matched case-insensitively).
- `thinking` only fires if the run streams reasoning (`reasoningLevel: "stream"`). If the model doesn't emit reasoning deltas, typing won't start.
- Heartbeat typing is a liveness signal for the resolved delivery target. It starts at heartbeat run start instead of following `message` or `thinking` stream timing. Set `typingMode: "never"` to disable it.
- Heartbeats do not show typing when `target: "none"`, when the target cannot be resolved, when chat delivery is disabled for the heartbeat, or when the channel does not support typing.
- `typingIntervalSeconds` controls the **refresh cadence**, not the start time. The default is 6 seconds.

**Source**: OpenClaw documentation — `concepts/typing-indicators` (mirror `inbox/openclaw_docs/concepts/typing-indicators.md`)
**Last Updated**: 2026-06-22
**Status**: Active
