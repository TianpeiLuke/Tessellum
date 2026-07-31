---
tags:
  - resource
  - documentation
  - openclaw
  - tools
  - btw
keywords:
  - openclaw btw side question
  - /btw /side ephemeral
  - chat.side_result event
  - ephemeral side query
  - no transcript persistence
  - codex side thread fork
  - background context only
  - btw surface behavior tui channels control ui
topics:
  - OpenClaw
  - BTW Side Questions
language: markdown
date of note: 2026-06-22
status: active
building_block: concept
source_url: https://docs.openclaw.ai/tools/btw
access_control_group: ["general"]
---

# OpenClaw — The `/btw` Ephemeral Side-Question Tool

## Overview

This note describes the OpenClaw `/btw` tool (alias `/side`): a way to ask a quick side question about the **current session** without turning that question into normal conversation history. It is modeled after Claude Code's `/btw` behavior but adapted to OpenClaw's Gateway and multi-channel architecture. This note mirrors the `tools/btw` source page — covering what `/btw` does and explicitly does not do, how it supplies session context as background-only, the `chat.side_result` delivery model, the per-surface behavior (TUI / external channels / Control UI / web), and when (and when not) to use it.

## What It Does

When you send `/btw what changed?`, OpenClaw: (1) snapshots the current session context, (2) runs a separate ephemeral side query, (3) answers only the side question, (4) leaves the main run alone, (5) does **not** write the BTW question or answer to session history, and (6) emits the answer as a **live side result** rather than a normal assistant message.

The important mental model is: same session context; separate one-shot side query; same native harness transport when the session uses a native harness; no future context pollution; no transcript persistence.

For **Codex harness sessions**, BTW stays inside Codex by forking the active app-server thread as an ephemeral side thread. That keeps Codex OAuth and native thread behavior intact while still isolating the side answer from the parent transcript. Like Codex `/side`, the side thread keeps the current Codex permissions and native tool surface, with guardrails that tell the model not to treat inherited parent-thread work as active instructions.

For **CLI runtime aliases**, BTW uses the owning CLI backend in side-question mode instead of falling back to a direct provider call. OpenClaw seeds sanitized conversation context into a fresh one-shot CLI invocation, disables OpenClaw MCP tool bundling and reusable CLI session state for that invocation, and lets the backend add any CLI-native no-resume or no-tools flags it supports. Direct non-CLI runtimes keep the direct one-shot path.

## What It Does Not Do

`/btw` does **not**: create a new durable session; continue the unfinished main task; write BTW question/answer data to transcript history; appear in `chat.history`; or survive a reload. It is intentionally **ephemeral**.

## How Context Works

BTW uses the current session as **background context only**. If the main run is currently active, OpenClaw snapshots the current message state and includes the in-flight main prompt as background context, while explicitly telling the model to: answer only the side question; not resume or complete the unfinished main task; and not steer the parent conversation. That keeps BTW isolated from the main run while still making it aware of what the session is about.

## Delivery Model

BTW is **not** delivered as a normal assistant transcript message. At the Gateway protocol level, normal assistant chat uses the `chat` event, while BTW uses the `chat.side_result` event. This separation is intentional: if BTW reused the normal `chat` event path, clients would treat it like regular conversation history. Because BTW uses a separate live event and is not replayed from `chat.history`, it disappears after reload.

## Surface Behavior

### TUI

In TUI, BTW is rendered inline in the current session view, but it remains ephemeral: visibly distinct from a normal assistant reply; dismissible with `Enter` or `Esc`; and not replayed on reload.

### External Channels

On channels like Telegram, WhatsApp, and Discord, BTW is delivered as a clearly labeled one-off reply because those surfaces do not have a local ephemeral overlay concept. The answer is still treated as a side result, not normal session history.

### Control UI / Web

The Gateway emits BTW correctly as `chat.side_result`, and BTW is not included in `chat.history`, so the persistence contract is already correct for web. The current Control UI still needs a dedicated `chat.side_result` consumer to render BTW live in the browser. Until that client-side support lands, BTW is a Gateway-level feature with full TUI and external-channel behavior, but not yet a complete browser UX.

## When to Use BTW

Use `/btw` when you want: a quick clarification about the current work; a factual side answer while a long run is still in progress; or a temporary answer that should not become part of future session context. Example invocations:

```text
/btw what file are we editing?
/side what changed while the main run continued?
/btw what does this error mean?
/btw summarize the current task in one sentence
/btw what is 17 * 19?
```

## When Not to Use BTW

Do not use `/btw` when you want the answer to become part of the session's future working context. In that case, ask normally in the main session instead of using BTW.

**Source**: OpenClaw documentation — `tools/btw` (mirror `inbox/openclaw_docs/tools/btw.md`)
**Last Updated**: 2026-06-22
**Status**: Active
