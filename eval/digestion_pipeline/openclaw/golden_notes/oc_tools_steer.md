---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - steer
keywords:
  - openclaw steer command
  - /steer /tell active run
  - steer vs queue mode
  - inject guidance active run
  - runtime steering boundary
  - /acp steer session
  - queue steer collect followup interrupt
topics:
  - OpenClaw
  - Agent Steering
language: markdown
date of note: 2026-06-22
status: active
building_block: procedure
source_url: https://docs.openclaw.ai/tools/steer
access_control_group: ["general"]
---

# OpenClaw — The `/steer` Command (Steer an Active Run)

## Overview

This note is the procedure for OpenClaw's `/steer` command (alias `/tell`): how to inject guidance into an agent run that is *already* working, without changing the session's stored queue mode. It mirrors the `tools/steer` source page — the header behavior, targeting the current session's active run, `/steer` vs the `/queue` modes, sub-agent visibility, and `/acp steer` for ACP harness sessions. `/steer` first tries to send guidance to an already-active run; it is for "adjust this run while it is still working" moments, and if the current runtime cannot accept steering, OpenClaw sends the message as a normal prompt instead of dropping it.

## Current session

Use the top-level `/steer` (or its alias `/tell`) to target the active run for the current session:

```text
/steer prefer the smaller patch and keep the tests focused
/tell summarize before making the next tool call
```

The behavior, per source, is exactly these four points: it targets only the current session's active run; it works independently of the session's `/queue` mode; it starts a normal turn with the same message when the session is idle or the active run cannot accept steering (the message is never dropped); and it uses the active runtime's steering path, so the model sees the guidance at the next supported runtime boundary (not necessarily instantly — guidance lands when the runtime reaches a point where it can accept it).

## Steer vs queue

`/steer` and the `/queue` modes both influence how a message reaches an active run, but they operate at different levels. `/queue steer` is a *stored session setting* that makes normal inbound messages try to steer the active run when they arrive while a run is active. `/steer <message>` is an *explicit command* that tries to inject that command's message into the active run at the next supported runtime boundary, regardless of the stored `/queue` setting. When that injection is not available, the `/steer` command prefix is stripped and `<message>` continues as a normal prompt.

The source gives this decision table for choosing between the explicit command and the four stored queue modes:

- Use `/steer <message>` when you want to guide the active run right now.
- Use `/queue steer` when you want future normal messages to steer active runs by default.
- Use `/queue collect` or `/queue followup` when future normal messages should wait for a later turn instead of steering the active run.
- Use `/queue interrupt` when the newest message should replace the active run instead of steering it.

For queue modes and steering boundaries, see the Command queue and Steering queue concept pages (linked in References).

## Sub-agents

Top-level `/steer` targets the current session's active run only. Sub-agents report back to their parent/requester session, and `/subagents` is for visibility only — it does not provide a steering surface into a child run. In other words, steering is scoped to the run you are in; you cannot directly `/steer` a spawned sub-agent from its lister.

## ACP sessions

When the target is an ACP harness session rather than the current session's native run, use `/acp steer` and select the session explicitly:

```text
/acp steer --session agent:main:acp:codex tighten the repro
```

See the ACP agents page (linked in References) for ACP session selection and runtime behavior.

**Source**: OpenClaw documentation — `tools/steer` (mirror `inbox/openclaw_docs/tools/steer.md`)
**Last Updated**: 2026-06-22
**Status**: Active
